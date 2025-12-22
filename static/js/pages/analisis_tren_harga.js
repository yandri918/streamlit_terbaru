const baseUrl = "";
const apiPrefix = "/api";

function formatRupiah(angka) {
    var number_string = angka.toString(),
        sisa = number_string.length % 3,
        rupiah = number_string.substr(0, sisa),
        ribuan = number_string.substr(sisa).match(/\d{3}/g);

    if (ribuan) {
        separator = sisa ? '.' : '';
        rupiah += separator + ribuan.join('.');
    }
    return 'Rp ' + rupiah;
}



document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('price-trend-form');
    const commoditySelect = document.getElementById('commodity-select');
    const periodSelect = document.getElementById('period-select');
    const predictionResult = document.getElementById('prediction-result');
    const chartStatus = document.getElementById('chart-status');
    const chartCaption = document.getElementById('chart-caption');

    let trendChart = null;
    let currentHistoricalData = null; // Store fetched historical data

    // Set min date to tomorrow
    const dateInput = document.getElementById('target-date');
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    dateInput.min = tomorrow.toISOString().split('T')[0];

    // Set max date to 1 year from now
    const nextYear = new Date();
    nextYear.setFullYear(nextYear.getFullYear() + 1);
    dateInput.max = nextYear.toISOString().split('T')[0];

    // Function to fetch and render data
    async function fetchAndRenderData() {
        const commodity = commoditySelect.value;
        const range = periodSelect ? periodSelect.value : 30;

        if (!commodity) return;

        // Reset UI
        predictionResult.style.display = 'none';
        chartStatus.textContent = 'Memuat data...';
        chartStatus.className = 'text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded';

        try {
            const response = await fetch(`${baseUrl}${apiPrefix}/market/historical`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ commodity, range: parseInt(range) })
            });

            const data = await response.json();

            if (data.success) {
                currentHistoricalData = data; // Save for later use
                renderChart(data.labels, data.prices, null, null);

                chartStatus.textContent = `Data Historis (${range} Hari)`;
                chartStatus.className = 'text-xs text-green-600 bg-green-100 px-2 py-1 rounded';
                chartCaption.textContent = `Grafik pergerakan harga ${commoditySelect.options[commoditySelect.selectedIndex].text} dalam ${range} hari terakhir.`;
            } else {
                chartStatus.textContent = 'Gagal memuat data';
                chartStatus.className = 'text-xs text-red-600 bg-red-100 px-2 py-1 rounded';
            }
        } catch (error) {
            console.error('Error fetching historical data:', error);
            chartStatus.textContent = 'Error koneksi';
            chartStatus.className = 'text-xs text-red-600 bg-red-100 px-2 py-1 rounded';
        }
    }

    // --- FEATURE 1: MONITORING (Auto-load Historical Data) ---
    commoditySelect.addEventListener('change', fetchAndRenderData);

    // Listen for period changes too
    if (periodSelect) {
        periodSelect.addEventListener('change', fetchAndRenderData);
    }

    // --- FEATURE 2: FORECASTING (Prediction) ---
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.textContent;
        submitBtn.textContent = 'Menganalisis...';
        submitBtn.disabled = true;

        try {
            const commodity = commoditySelect.value;
            const date = document.getElementById('target-date').value;

            const response = await fetch(`${baseUrl}${apiPrefix}/market/predict`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ commodity, date })
            });

            const data = await response.json();

            if (data.success) {
                displayPredictionResult(data.data);
            } else {
                alert('Error: ' + (data.error || 'Gagal melakukan prediksi'));
            }

        } catch (error) {
            console.error('Error:', error);
            alert('Terjadi kesalahan saat menghubungi server.');
        } finally {
            submitBtn.textContent = originalBtnText;
            submitBtn.disabled = false;
        }
    });

    function displayPredictionResult(data) {
        predictionResult.style.display = 'block';

        // Update Text Info
        document.getElementById('result-date').textContent = data.prediction_date;
        document.getElementById('result-price').textContent = formatRupiah(data.predicted_price);
        document.getElementById('current-price').textContent = formatRupiah(data.current_price);
        document.getElementById('result-insight').textContent = data.insight;

        // Update Badge
        const badge = document.getElementById('result-trend-badge');
        badge.className = 'trend-indicator'; // Reset class
        badge.textContent = data.trend;

        if (data.trend.includes('Naik')) {
            badge.classList.add('trend-up');
            badge.innerHTML = '↗ ' + data.trend;
        } else if (data.trend.includes('Turun')) {
            badge.classList.add('trend-down');
            badge.innerHTML = '↘ ' + data.trend;
        } else {
            badge.classList.add('trend-stable');
            badge.innerHTML = '→ ' + data.trend;
        }

        // Update Chart with Prediction
        // Use data from prediction response which includes historical data
        renderChart(
            data.historical_data.labels,
            data.historical_data.prices,
            data.prediction_date,
            data.predicted_price
        );

        chartStatus.textContent = 'Data Historis + Prediksi';
        chartStatus.className = 'text-xs text-purple-600 bg-purple-100 px-2 py-1 rounded font-medium';
        chartCaption.innerHTML = `Grafik menunjukkan data historis dan titik prediksi pada <strong>${data.prediction_date}</strong>.`;

        // Scroll to result
        predictionResult.scrollIntoView({ behavior: 'smooth' });
    }

    function renderChart(labels, prices, predictionDate, predictionPrice) {
        const ctx = document.getElementById('trendChart').getContext('2d');

        if (trendChart) {
            trendChart.destroy();
        }

        // Prepare datasets
        const datasets = [{
            label: 'Harga Historis',
            data: prices,
            borderColor: '#4caf50',
            backgroundColor: 'rgba(76, 175, 80, 0.1)',
            borderWidth: 2,
            tension: 0.3,
            pointRadius: 2,
            fill: true
        }];

        // Add prediction dataset if available
        let chartLabels = [...labels];

        if (predictionDate && predictionPrice !== null) {
            chartLabels.push(predictionDate);

            // Create prediction line connecting last historical point to prediction
            const lastHistPrice = prices[prices.length - 1];
            const predictionData = new Array(prices.length - 1).fill(null);
            predictionData.push(lastHistPrice);
            predictionData.push(predictionPrice);

            datasets.push({
                label: 'Prediksi AI',
                data: predictionData,
                borderColor: '#ff9800',
                borderDash: [5, 5],
                borderWidth: 2,
                pointRadius: 5,
                pointBackgroundColor: '#ff9800',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                fill: false
            });
        }

        trendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: chartLabels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false,
                },
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += formatRupiah(context.parsed.y);
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: false,
                        ticks: {
                            callback: function (value) {
                                // Shorten large numbers for y-axis
                                return (value / 1000) + 'k';
                            }
                        },
                        grid: {
                            color: '#f3f4f6'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
});
