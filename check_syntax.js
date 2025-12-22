const baseUrl = "";
const apiPrefix = "/api";

// DEBUG: Check if JS is loaded
console.log("JS Loaded");
alert("DEBUG: JS LOADED SUCCESSFULLY! Klik OK untuk melanjutkan.");

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

function openTab(evt, tabName, btn) {
    var i, tabcontent, tablinks;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tab-button");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "block";
    if (btn) {
        btn.className += " active";
    } else if (evt && evt.currentTarget) {
        evt.currentTarget.className += " active";
    }
}

// Robust Initialization
function logToPage(message) {
    const logDiv = document.getElementById('debug-log');
    if (logDiv) {
        const entry = document.createElement('div');
        entry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        entry.style.borderBottom = "1px solid #ddd";
        logDiv.appendChild(entry);
        logDiv.scrollTop = logDiv.scrollHeight;
    }
    console.log(message);
}

function initDashboard() {
    logToPage("🚀 Initializing Dashboard Logic...");

    // Visual Debugging: Green underline on title to prove JS ran
    const title = document.querySelector('h1');
    if (title) {
        title.style.borderBottom = "5px solid #4caf50";
        title.setAttribute('title', 'JS Active');
    }

    // --- Modul 9: Dasbor Rekomendasi Terpadu ---
    const integratedForm = document.getElementById('integrated-recommendation-form');
    const resultIntegratedDiv = document.getElementById('result-integrated');

    if (integratedForm) {
        logToPage("✅ Modul 9 Form Found");
        integratedForm.style.borderLeft = "5px solid #4caf50"; // Visual confirmation
        integratedForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            logToPage('📝 Modul 9: Integrated Recommendation form submitted!');

            // Create result div if it doesn't exist (it might be missing in HTML)
            let targetDiv = resultIntegratedDiv;
            if (!targetDiv) {
                targetDiv = document.createElement('div');
                targetDiv.id = 'result-integrated';
                targetDiv.className = 'result-box';
                targetDiv.style.marginTop = '20px';
                integratedForm.parentNode.appendChild(targetDiv);
            }

            targetDiv.innerHTML = '<p>Sedang memproses rekomendasi terpadu...</p>';

            const requestData = {
                ketinggian: document.getElementById('ketinggian-select').value,
                iklim: document.getElementById('iklim-select').value,
                fase: document.getElementById('fase-select').value,
                masalah: document.getElementById('masalah-select').value
            };

            try {
                logToPage(`Fetching: ${baseUrl}${apiPrefix}/recommendation/integrated`);
                const response = await fetch(`${baseUrl}${apiPrefix}/recommendation/integrated`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });

                logToPage(`Response Status: ${response.status}`);
                const data = await response.json();
                logToPage(`Data Received: ${JSON.stringify(data).substring(0, 50)}...`);

                if (data.success) {
                    const rec = data.data;
                    let html = `<h3>🌱 Hasil Rekomendasi Terpadu</h3>`;

                    // 1. Bibit
                    html += `<h4>🌾 Rekomendasi Bibit & Varietas</h4>
                    <p><strong>Kriteria:</strong> ${rec.bibit.kriteria}</p>
                    <p><strong>Contoh Varietas:</strong> ${rec.bibit.rekomendasi.join(', ')}</p>
                    <p><em>Tips: ${rec.bibit.tips}</em></p>`;

                    // 2. Pemupukan
                    html += `<h4>🧪 Rekomendasi Pemupukan (${rec.pemupukan.fase})</h4>
                    <ul>
                        <li><strong>Rasio NPK:</strong> ${rec.pemupukan.rasio_npk}</li>
                        <li><strong>Aplikasi Tanah:</strong> ${rec.pemupukan.aplikasi_tanah}</li>
                        <li><strong>Aplikasi Daun:</strong> ${rec.pemupukan.aplikasi_daun}</li>
                    </ul>`;

                    // 3. Pengendalian
                    html += `<h4>🛡️ Pengendalian Hama & Penyakit</h4>`;
                    if (rec.pengendalian) {
                        if (typeof rec.pengendalian === 'string') {
                            html += `<p>${rec.pengendalian}</p>`;
                        } else {
                            const p = rec.pengendalian;
                            html += `<h5>${p.strategy.name}</h5>
                            <p>${p.strategy.description}</p>
                            <ul>`;
                            if (p.strategy.cycles) {
                                p.strategy.cycles.forEach(c => {
                                    html += `<li><strong>${c.weeks}:</strong> ${c.level} - ${c.active_ingredient}</li>`;
                                });
                            }
                            html += `</ul>`;

                            if (p.protocol) {
                                html += `<h5>${p.protocol.title}</h5>
                                <ul>`;
                                p.protocol.steps.forEach(step => {
                                    html += `<li>${step}</li>`;
                                });
                                html += `</ul>`;
                            }
                        }
                    } else {
                        html += `<p>Tidak ada rekomendasi pengendalian spesifik.</p>`;
                    }

                    targetDiv.innerHTML = html;
                } else {
                    targetDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${data.error}</p>`;
                }
            } catch (error) {
                console.error("Error:", error);
                logToPage(`Error: ${error.message}`);
                targetDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> Gagal terhubung ke server.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 1 (Analisis BWD) ---
    const formBwd = document.getElementById('upload-form');
    const resultBwdDiv = document.getElementById('result-bwd');
    const bwdInput = document.getElementById('bwd-input');
    if (formBwd) {
        formBwd.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('📝 Modul 1: BWD Analysis: Form submitted!');
            resultBwdDiv.innerHTML = '<p>Menganalisis gambar...</p>';
            const formData = new FormData(formBwd);
            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/analysis/bwd`, {
                    method: 'POST',
                    body: formData
                });
                if (!response.ok && response.status !== 201) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (data.success) {
                    resultBwdDiv.innerHTML =
                        `<p><strong>Skor BWD:</strong> ${data.bwd_score} | <strong>Kepercayaan:</strong>
                        ${data.confidence_percent}%
                    </p>`;
                    if (bwdInput) bwdInput.value = data.bwd_score;
                } else {
                    resultBwdDiv.innerHTML =
                        `<p style="color: red;"><strong>Error:</strong> ${data.message || data.error}</p>`;
                }
            } catch (error) {
                console.error("Error:", error);
                resultBwdDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> Gagal terhubung.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 12 (Panduan Budidaya) ---
    const guideForm = document.getElementById('guide-form');
    const resultGuideDiv = document.getElementById('result-guide');

    if (guideForm) {
        guideForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const guideSelect = document.getElementById('guide-commodity-select');
            if (!guideSelect.value) return;

            resultGuideDiv.style.display = 'block';
            resultGuideDiv.innerHTML = '<p>Memuat panduan...</p>';

            try {
                const commodity = guideSelect.value;
                const response = await fetch(`${baseUrl}${apiPrefix}/knowledge/guide/${commodity}`);
                const data = await response.json();

                if (data.success) {
                    const gd = data.data;
                    let html = `<h2>${gd.icon} Panduan Lengkap: ${gd.name}</h2>
                    <p>${gd.description}</p>`;
                    html += '<div class="tabs">';
                    html +=
                        `<button class="tab-button active" onclick="openTab(event, 'sop-budidaya', this)">SOP
                            Budidaya</button>`;
                    html +=
                        `<button class="tab-button" onclick="openTab(event, 'analisis-bisnis', this)">Analisis
                            Bisnis</button>`;
                    html += '</div>';
                    html += `<div id="sop-budidaya" class="tab-content active">`;
                    for (const [phase, steps] of Object.entries(gd.sop)) {
                        html += `<h3>${phase}</h3>
                        <ul>`;
                        steps.forEach(step => {
                            html += `<li>${step}</li>`;
                        });
                        html += `</ul>`;
                    }
                    html += `
                    </div>`;
                    const analysis = gd.business_analysis;
                    html +=
                        `<div id="analisis-bisnis" class="tab-content">
                        <h3>${analysis.title}</h3>
                        <p><strong>Asumsi:</strong> Lahan ${analysis.assumptions.Luas_Lahan}, populasi
                            ${analysis.assumptions.Populasi_Tanaman}.</p>`;
                    html +=
                        `<h4>Estimasi Biaya Produksi</h4>
                        <table>
                            <tr>
                                <th>Komponen</th>
                                <th>Kebutuhan</th>
                                <th style="text-align:right;">Biaya</th>
                            </tr>`;
                    let totalCost = 0;
                    analysis.costs.forEach(i => {
                        html +=
                            `<tr>
                                <td>${i.item}</td>
                                <td>${i.amount}</td>
                                <td class="cost">${formatRupiah(i.cost)}</td>
                            </tr>`;
                        totalCost += i.cost;
                    });
                    html +=
                        `<tr>
                                <td colspan="2" class="total-cost"><strong>Total Biaya</strong></td>
                                <td class="total-cost"><strong>${formatRupiah(totalCost)}</strong></td>
                            </tr>
                        </table>`;
                    html +=
                        `<h4>Simulasi Pendapatan</h4>
                        <table>
                            <tr>
                                <th>Skenario Harga</th>
                                <th>Panen Konservatif</th>
                                <th>Panen Optimal</th>
                            </tr>`;
                    analysis.revenue_scenarios.forEach(s => {
                        const revCons = analysis.yield_potential[0].total_yield_kg * s.price_per_kg;
                        const revOpt = analysis.yield_potential[1].total_yield_kg * s.price_per_kg;
                        html +=
                            `<tr>
                                <td>${s.price_level} (${formatRupiah(s.price_per_kg)}/kg)</td>
                                <td>${formatRupiah(revCons)}</td>
                                <td>${formatRupiah(revOpt)}</td>
                            </tr>`;
                    });
                    html += `
                        </table><br><small><strong>Disclaimer:</strong> Angka ini adalah estimasi.</small>
                    </div>`;
                    resultGuideDiv.innerHTML = html;
                } else {
                    resultGuideDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                }
            } catch (error) {
                console.error("Error:", error);
                resultGuideDiv.innerHTML = `<p style="color: red;">Gagal terhubung.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 13 (Pusat Pengetahuan pH) ---
    const showPhBtn = document.getElementById('show-ph-info-btn');
    const resultPhDiv = document.getElementById('result-ph-info');
    if (showPhBtn) {
        showPhBtn.addEventListener('click', async (event) => {
            event.preventDefault();
            if (resultPhDiv.style.display === 'block') {
                resultPhDiv.style.display = 'none';
                showPhBtn.textContent = 'Tampilkan Informasi Lengkap';
                return;
            }
            resultPhDiv.style.display = 'block';
            showPhBtn.textContent = 'Sembunyikan Informasi';
            resultPhDiv.innerHTML = '<p>Memuat informasi...</p>';
            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/knowledge/ph-info`);
                if (!response.ok && response.status !== 201) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                if (data.success) {
                    const pd = data.data;
                    let html = `<h2>${pd.icon} ${pd.title}</h2>
                    <div class="tabs">`;
                    Object.keys(pd.sections).forEach((k, i) => {
                        html +=
                            `<button class="tab-button ${i === 0 ? 'active' : ''}"
                            onclick="openTab(event, 'ph-${k.replace(/[^a-zA-Z0-9]/g, '-')}', this)">${pd.sections[k].title}</button>`;
                    });
                    html += '</div>';
                    Object.entries(pd.sections).forEach(([k, s], i) => {
                        html +=
                            `<div id="ph-${k.replace(/[^a-zA-Z0-9]/g, '-')}" class="tab-content ${i === 0 ? 'active' : ''}">
                        <ul>`;
                        s.content.forEach(item => {
                            html += `<li>${item}</li>`;
                        });
                        html += `</ul>
                    </div>`;
                    });
                    resultPhDiv.innerHTML = html;
                } else {
                    resultPhDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
                }
            } catch (error) {
                console.error("Error:", error);
                resultPhDiv.innerHTML = `<p style="color: red;">Gagal terhubung.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 14 (Rekomendasi Tanaman) ---
    const cropForm = document.getElementById('crop-recommendation-form');
    const resultCropDiv = document.getElementById('result-crop');
    if (cropForm) {
        cropForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            resultCropDiv.innerHTML = '<p>Menganalisis data dan mencari rekomendasi terbaik...</p>';
            const requestData = {
                n_value: document.getElementById('crop-n-input').value,
                p_value: document.getElementById('crop-p-input').value,
                k_value: document.getElementById('crop-k-input').value,
                temperature: document.getElementById('crop-temp-input').value,
                humidity: document.getElementById('crop-humidity-input').value,
                ph: document.getElementById('crop-ph-input').value,
                rainfall: document.getElementById('crop-rainfall-input').value
            };
            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/ml/recommend-crop`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
                const responseData = await response.json();
                if (responseData.success) {
                    resultCropDiv.innerHTML =
                        `<h3>Rekomendasi Tanaman Optimal</h3>
                    <p style="font-size: 1.5em; text-align: center; font-weight: bold; color: var(--primary-color);">
                        ${responseData.recommended_crop}</p>
                    <p><small>Rekomendasi ini dihasilkan oleh model Machine Learning berdasarkan data yang Anda
                            masukkan.</small></p>`;
                } else {
                    resultCropDiv.innerHTML =
                        `<p style="color: red;"><strong>Error:</strong> ${responseData.error}</p>`;
                }
            } catch (error) {
                console.error("Error:", error);
                resultCropDiv.innerHTML =
                    `<p style="color: red;"><strong>Error:</strong> Tidak dapat terhubung ke server.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 15 (Prediksi Panen) ---
    const yieldForm = document.getElementById('yield-prediction-form');
    const resultYieldDiv = document.getElementById('result-yield');
    if (yieldForm) {
        yieldForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            resultYieldDiv.innerHTML = '<p>Menganalisis data dan membuat prediksi...</p>';
            const requestData = {
                nitrogen: document.getElementById('yield-n-input').value,
                phosphorus: document.getElementById('yield-p-input').value,
                potassium: document.getElementById('yield-k-input').value,
                temperature: document.getElementById('yield-temp-input').value,
                rainfall: document.getElementById('yield-rainfall-input').value,
                ph: document.getElementById('yield-ph-input').value,
            };
            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/ml/predict-yield`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
                const responseData = await response.json();
                if (responseData.success) {
                    resultYieldDiv.innerHTML =
                        `<h3>Estimasi Potensi Hasil Panen</h3>
                    <p style="font-size: 1.8em; text-align: center; font-weight: bold; color: var(--primary-color);">
                        ${responseData.predicted_yield_ton_ha} ton/ha</p>
                    <p><small>Estimasi ini dihasilkan oleh model Machine Learning berdasarkan data yang Anda
                            masukkan.</small>
                    </p>`;
                } else {
                    resultYieldDiv.innerHTML =
                        `<p style="color: red;"><strong>Error:</strong> ${responseData.error}</p>`;
                }
            } catch (error) {
                console.error("Error:", error);
                resultYieldDiv.innerHTML =
                    `<p style="color: red;"><strong>Error:</strong> Tidak dapat terhubung ke server.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 16 (Prediksi Panen XAI) ---
    const xaiYieldForm = document.getElementById('xai-yield-prediction-form');
    const resultXaiYieldDiv = document.getElementById('result-xai-yield');
    let importanceChart;
    if (xaiYieldForm) {
        xaiYieldForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            resultXaiYieldDiv.style.display = 'block';
            resultXaiYieldDiv.innerHTML = '<p>Menganalisis data dengan XAI...</p>';

            const requestData = {
                nitrogen: document.getElementById('xai-nitrogen').value,
                phosphorus: document.getElementById('xai-phosphorus').value,
                potassium: document.getElementById('xai-potassium').value,
                temperature: document.getElementById('xai-temperature').value,
                rainfall: document.getElementById('xai-rainfall').value,
                ph: document.getElementById('xai-ph').value,
            };

            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/ml/predict-yield-advanced`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
                const data = await response.json();

                if (data.success) {
                    if (importanceChart) {
                        importanceChart.destroy();
                    }

                    let htmlResult = `
                    <h3>Hasil Prediksi & Analisis</h3>
                    <p style="font-size: 1.8em; text-align: center; font-weight: bold; color: var(--primary-color);">
                        Estimasi Panen: ${data.predicted_yield_ton_ha} ton/ha
                    </p>

                    <h4>Faktor Pendorong & Penghambat (Analisis SHAP)</h4>
                    <p>Analisis ini menjelaskan mengapa prediksi Anda berbeda dari rata-rata (${data.base_value}
                        ton/ha).</p>
                    <ul class="item-list">`;

                    for (const [feature, value] of Object.entries(data.shap_values)) {
                        const change = value / 1000;
                        const direction = change >= 0 ? 'Meningkatkan' : 'Menurunkan';
                        const cssClass = change >= 0 ? 'shap-positive' : 'shap-negative';
                        htmlResult += `<li class="shap-item"><span>${feature}</span> <span
                                class="${cssClass}">${direction}
                                estimasi sebesar ${Math.abs(change).toFixed(2)} ton/ha</span></li>`;
                    }

                    htmlResult += `</ul>

                    <h4>Faktor Paling Berpengaruh (Secara Umum)</h4>
                    <canvas id="importance-chart"></canvas>
                    `;

                    resultXaiYieldDiv.innerHTML = htmlResult;

                    const chartCtx = document.getElementById('importance-chart').getContext('2d');
                    const labels = data.feature_importances.map(item => item[0]);
                    const values = data.feature_importances.map(item => item[1]);

                    importanceChart = new Chart(chartCtx, {
                        type: 'bar',
                        data: {
                            labels: labels,
                            datasets: [{
                                label: 'Tingkat Kepentingan',
                                data: values,
                                backgroundColor: 'rgba(76, 175, 80, 0.6)',
                                borderColor: 'rgba(46, 125, 50, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            indexAxis: 'y',
                            responsive: true,
                            plugins: {
                                legend: {
                                    display: false
                                },
                                title: {
                                    display: true,
                                    text: 'Faktor yang Paling Memengaruhi Hasil Panen'
                                }
                            }
                        }
                    });

                } else {
                    resultXaiYieldDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${data.error}</p>`;
                }
            } catch (error) {
                console.error('Error fetching XAI prediction:', error);
                resultXaiYieldDiv.innerHTML =
                    `<p style="color: red;"><strong>Error:</strong> Tidak dapat terhubung ke server.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 17 (Kalkulator Konversi Pupuk) ---
    const fertConversionForm = document.getElementById('fertilizer-conversion-form');
    const resultFertConversionDiv = document.getElementById('result-fertilizer-conversion');
    if (fertConversionForm) {
        fertConversionForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            resultFertConversionDiv.innerHTML = '<p>Menghitung konversi...</p>';
            const requestData = {
                nutrient_needed: document.getElementById('nutrient-needed-select').value,
                nutrient_amount_kg: document.getElementById('nutrient-amount-input').value,
                fertilizer_type: document.getElementById('fertilizer-type-select').value
            };
            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/ml/calculate-fertilizer-bags`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestData)
                });
                const data = await response.json();
                if (data.success) {
                    resultFertConversionDiv.innerHTML = `<h3>Hasil Perhitungan</h3>
                    <p>Untuk memenuhi kebutuhan <strong>${data.nutrient_amount_kg} kg</strong> unsur hara
                        <strong>${data.nutrient_needed}</strong>, Anda memerlukan:
                    </p>
                    <p style="font-size: 1.8em; text-align: center; font-weight: bold; color: var(--primary-color);">
                        ${data.required_fertilizer_kg} kg pupuk ${data.fertilizer_name}</p>`;
                } else {
                    resultFertConversionDiv.innerHTML =
                        `<p style="color: red;"><strong>Error:</strong> ${data.error}</p>`;
                }
            } catch (error) {
                console.error("Error:", error);
                resultFertConversionDiv.innerHTML =
                    `<p style="color: red;"><strong>Error:</strong> Tidak dapat terhubung ke server.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 18 (Diagnostik Gejala Cerdas) ---
    const startBtn = document.getElementById('start-diagnostic-btn');
    const questionsDiv = document.getElementById('diagnostic-questions');
    const resultDiv = document.getElementById('diagnostic-result');
    let diagnosticTree = null;
    if (startBtn) {
        async function startDiagnostic() {
            startBtn.style.display = 'none';
            questionsDiv.style.display = 'block';
            resultDiv.style.display = 'none';
            resultDiv.innerHTML = '';
            questionsDiv.innerHTML = '<p>Memuat data diagnostik...</p>';
            try {
                if (!diagnosticTree) {
                    const response = await fetch(`${baseUrl}${apiPrefix}/knowledge/diagnostic-tree`);
                    const responseData = await response.json();
                    if (responseData.success) {
                        diagnosticTree = responseData.data;
                    } else {
                        throw new Error(responseData.error);
                    }
                }
                renderQuestion(diagnosticTree.start, []);
            } catch (error) {
                console.error("Error:", error);
                questionsDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${error.message}</p>`;
            }
        }

        function renderQuestion(node, path) {
            questionsDiv.innerHTML = `<h4>${node.question}</h4>`;
            for (const [key, nextNode] of Object.entries(node.options)) {
                const button = document.createElement('button');
                button.textContent = key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
                button.classList.add('option-button');
                button.onclick = () => {
                    if (typeof nextNode === 'string') {
                        renderResult(nextNode);
                    } else {
                        renderQuestion(nextNode, [...path, key]);
                    }
                };
                questionsDiv.appendChild(button);
            }
        }

        function renderResult(diagnosis) {
            questionsDiv.style.display = 'none';
            resultDiv.style.display = 'block';
            resultDiv.innerHTML =
                `<h3>Hasil Diagnosis</h3>
                    <p>${diagnosis}</p><button class="option-button" id="restart-diagnostic-btn">Mulai Lagi</button>`;
            document.getElementById('restart-diagnostic-btn').onclick = () => {
                startBtn.style.display = 'block';
                questionsDiv.style.display = 'none';
                resultDiv.style.display = 'none';
                return;
            }
        };

        startBtn.addEventListener('click', startDiagnostic);
    }

    // --- Logika untuk Modul 19 (Perencana Hasil Panen) ---
    const yieldPlanForm = document.getElementById('yield-plan-form');
    const resultYieldPlanDiv = document.getElementById('result-yield-plan');
    if (yieldPlanForm) {
        yieldPlanForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            resultYieldPlanDiv.innerHTML = '<p>Mencari resep lahan optimal...</p>';
            const requestData = {
                commodity: document.getElementById('plan-commodity-select').value,
                target_yield: document.getElementById('plan-target-yield-input').value
            };
            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/ml/generate-yield-plan`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });
                const data = await response.json();
                if (data.success) {
                    let htmlResult = `<h3>Rekomendasi Kondisi Lahan</h3>
                    <p>Untuk mencapai target panen sekitar <strong>${requestData.target_yield} ton/ha</strong>, berikut
                        adalah
                        resep kondisi lahan berdasarkan data kami yang paling mendekati:</p>
                    <ul class="item-list mt-4">`;
                    for (const [key, value] of Object.entries(data.plan)) {
                        htmlResult += `<li class="plan-item"><span class="plan-item-label">${key}</span><span
                                class="plan-item-value">${value}</span></li>`;
                    }
                    htmlResult += `</ul><br><small><strong>Disclaimer:</strong> Ini adalah target berdasarkan data
                        historis,
                        bukan jaminan.</small>`;
                    resultYieldPlanDiv.innerHTML = htmlResult;
                } else {
                    resultYieldPlanDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${data.error}</p>`;
                }
            } catch (error) {
                console.error("Error:", error);
                resultYieldPlanDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> Gagal terhubung ke
                        server.
                    </p>`;
            }
        });
    }


    // --- Logika untuk Modul 21 (Analis Risiko Keberhasilan) ---
    const successPredictionForm = document.getElementById('success-prediction-form');
    const resultSuccessPredictionDiv = document.getElementById('result-success-prediction');
    if (successPredictionForm) {
        successPredictionForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('📝 Modul 21: Success Prediction form submitted!');
            resultSuccessPredictionDiv.innerHTML = '<p>Menganalisis probabilitas keberhasilan...</p>';
            const requestData = {
                nitrogen: document.getElementById('sp-nitrogen').value,
                phosphorus: document.getElementById('sp-phosphorus').value,
                potassium: document.getElementById('sp-potassium').value,
                temperature: document.getElementById('sp-temperature').value,
                rainfall: document.getElementById('sp-rainfall').value,
                ph: document.getElementById('sp-ph').value,
                penggunaan_benih: document.getElementById('sp-benih').value,
                aplikasi_organik: document.getElementById('sp-organik').value,
                manajemen_gulma: document.getElementById('sp-gulma').value
            };
            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/ml/predict-success`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(requestData)
                });
                const data = await response.json();
                if (data.success) {
                    const statusColor = data.status === "Berhasil" ? "text-green-600" : "text-red-600";
                    resultSuccessPredictionDiv.innerHTML = `
                    <h3>Hasil Analisis Risiko</h3>
                    <p>Berdasarkan parameter yang Anda masukkan, status rencana tanam Anda adalah:</p>
                    <p style="font-size: 1.8em; text-align: center; font-weight: bold;" class="${statusColor}">
                        ${data.status}
                    </p>
                    <p class="text-center">Dengan probabilitas keberhasilan sebesar
                        <strong>${data.probability_of_success}%</strong>
                    </p>`;
                } else {
                    resultSuccessPredictionDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> ${data.error}
                    </p>`;
                }
            } catch (error) {
                console.error('Error fetching success probability:', error);
                resultSuccessPredictionDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> Tidak dapat
                        terhubung
                        ke server.</p>`;
            }
        });
    }

    // --- Logika untuk Modul 20 (Dokter Tanaman Canggih - Roboflow AI) ---
    const advancedDiseaseForm = document.getElementById('advanced-disease-form');
    const resultAdvancedDiseaseDiv = document.getElementById('result-advanced-disease');
    if (advancedDiseaseForm) {
        advancedDiseaseForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            console.log('📝 Modul 20: Roboflow form submitted!');
            resultAdvancedDiseaseDiv.innerHTML = '<p>Menganalisis dengan Roboflow AI...</p>';
            const fileInput = document.getElementById('disease-image-input');
            const file = fileInput.files[0];
            if (!file) {
                resultAdvancedDiseaseDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> Silakan pilih
                file
                        gambar terlebih dahulu.</p > `;
                return;
            }
            const formData = new FormData();
            formData.append('file', file);
            try {
                const response = await fetch(`${baseUrl}${apiPrefix}/analysis/disease-advanced`, {
                    method: 'POST',
                    body: formData
                });
                const backendResponse = await response.json();
                if (backendResponse.success) {
                    displayRoboflowResults(backendResponse.data);
                } else {
                    resultAdvancedDiseaseDiv.innerHTML = `<p style="color: red;"><strong>Error dari server:</strong>
                        ${backendResponse.error || 'Gagal menganalisis.'}</p>`;
                }
            } catch (error) {
                console.error('Error calling backend for advanced analysis:', error);
                resultAdvancedDiseaseDiv.innerHTML = `<p style="color: red;"><strong>Error:</strong> Tidak dapat
                        terhubung
                        ke server backend Anda.</p>`;
            }
        });

        function displayRoboflowResults(results) {
            let html = '<h3>Hasil Diagnosis dari Roboflow AI</h3>';
            if (results && results.outputs && results.outputs.length > 0) {
                html += '<ul style="list-style-type: none; padding-left: 0;">';
                results.outputs.forEach((output, index) => {
                    const detection = output.detection;
                    const classification = output.classification;
                    html += `<li class="mb-4 p-4 border rounded-lg bg-white">`;
                    html += `<strong class="text-lg text-emerald-700">Deteksi #${index + 1}</strong><br>`;
                    if (detection && detection.predictions && detection.predictions.length > 0) {
                        const pred = detection.predictions[0];
                        html += `<strong>Objek Terdeteksi:</strong> ${pred.class} (Kepercayaan:
                            ${Math.round(pred.confidence
                            * 100)}%)<br>`;
                    } else {
                        html += `<strong>Objek Terdeteksi:</strong> Tidak ada.<br>`;
                    }
                    if (classification && classification.predictions && classification.predictions.length > 0) {
                        const topClass = classification.predictions[0];
                        html += `<strong>Klasifikasi Penyakit:</strong> ${topClass.class} (Kepercayaan:
                            ${Math.round(topClass.confidence * 100)}%)`;
                    } else {
                        html += `<strong>Klasifikasi Penyakit:</strong> Tidak ada.`;
                    }
                    html += `</li>`;
                });
                html += '</ul>';
            } else {
                html += '<p>Tidak ada hasil deteksi atau klasifikasi yang ditemukan dalam gambar.</p>';
            }
            resultAdvancedDiseaseDiv.innerHTML = html;
        }
    }
}


// Run initialization when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDashboard);
} else {
    initDashboard();
}
