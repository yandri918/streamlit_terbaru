"""Script to build Harvest Database HTML with Chart.js visualizations."""

html_content = '''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Database Penyimpanan Hasil Panen | AgriSensa</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        /* Header */
        .header {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
        }

        .header h1 {
            color: #2d3748;
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        .header p {
            color: #718096;
            font-size: 1.1rem;
        }

        .header-actions {
            display: flex;
            gap: 15px;
            margin-top: 20px;
            flex-wrap: wrap;
        }

        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            text-decoration: none;
            display: inline-block;
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        .btn-primary {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
        }

        .btn-primary:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(16, 185, 129, 0.4);
        }

        .btn-secondary {
            background: #e2e8f0;
            color: #2d3748;
        }

        .btn-danger {
            background: #f56565;
            color: white;
        }

        .btn-small {
            padding: 6px 12px;
            font-size: 0.85rem;
        }

        /* Statistics Cards */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }

        .stat-card h3 {
            color: #718096;
            font-size: 0.9rem;
            margin-bottom: 10px;
            font-weight: 600;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 800;
            color: #2d3748;
        }

        .stat-icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }

        /* Charts Section */
        .charts-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }

        .chart-card {
            background: white;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }

        .chart-card h3 {
            color: #2d3748;
            margin-bottom: 20px;
            font-size: 1.3rem;
        }

        .chart-container {
            position: relative;
            height: 300px;
        }

        /* Records Table */
        .records-section {
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
        }

        .records-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .records-header h2 {
            color: #2d3748;
            font-size: 1.8rem;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        thead {
            background: #f7fafc;
        }

        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }

        th {
            font-weight: 600;
            color: #4a5568;
        }

        tbody tr:hover {
            background: #f7fafc;
        }

        .expandable-row {
            background: #f7fafc;
        }

        .criteria-table {
            margin: 10px 0;
            font-size: 0.9rem;
        }

        .criteria-table th,
        .criteria-table td {
            padding: 8px;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(5px);
            overflow-y: auto;
        }

        .modal.active {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .modal-content {
            background: white;
            border-radius: 20px;
            padding: 30px;
            max-width: 700px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            animation: modalSlideIn 0.3s ease-out;
        }

        @keyframes modalSlideIn {
            from {
                transform: translateY(-50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
        }

        .modal-header h2 {
            color: #2d3748;
            font-size: 1.8rem;
        }

        .close-modal {
            background: none;
            border: none;
            font-size: 2rem;
            color: #718096;
            cursor: pointer;
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            color: #4a5568;
            font-weight: 600;
            margin-bottom: 8px;
        }

        .form-group input,
        .form-group select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e2e8f0;
            border-radius: 8px;
            font-size: 1rem;
        }

        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        /* Criteria Section */
        .criteria-section {
            background: #f7fafc;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .criteria-item {
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            border: 2px solid #e2e8f0;
        }

        .criteria-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }

        /* Toast */
        .toast-container {
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 2000;
        }

        .toast {
            background: white;
            border-radius: 10px;
            padding: 15px 20px;
            margin-bottom: 10px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            display: flex;
            align-items: center;
            gap: 12px;
            min-width: 300px;
            animation: toastSlideIn 0.3s ease-out;
        }

        @keyframes toastSlideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        .toast-success {
            border-left: 4px solid #10b981;
        }

        .toast-error {
            border-left: 4px solid #f56565;
        }

        /* Loading */
        .loading {
            text-align: center;
            padding: 40px;
            color: #10b981;
        }

        .spinner {
            border: 4px solid #e2e8f0;
            border-top: 4px solid #10b981;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 15px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #718096;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header h1 {
                font-size: 2rem;
            }

            .charts-section {
                grid-template-columns: 1fr;
            }

            .form-row {
                grid-template-columns: 1fr;
            }

            table {
                font-size: 0.85rem;
            }

            th, td {
                padding: 10px;
            }
        }
    </style>
</head>

<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 Database Penyimpanan Hasil Panen</h1>
            <p>Catat dan visualisasikan data hasil panen Anda</p>
            <div class="header-actions">
                <button class="btn btn-primary" onclick="showAddRecordModal()">
                    <i class="fas fa-plus"></i> Tambah Data Panen
                </button>
                <button class="btn btn-secondary" onclick="showMyDashboard()">
                    <i class="fas fa-user"></i> Dashboard Saya
                </button>
                <a href="/" class="btn btn-secondary">
                    <i class="fas fa-home"></i> Kembali ke Beranda
                </a>
            </div>
        </div>

        <!-- Statistics Cards -->
        <div class="stats-grid" id="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📝</div>
                <h3>Total Catatan</h3>
                <div class="stat-value" id="stat-records">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚖️</div>
                <h3>Total Panen (kg)</h3>
                <div class="stat-value" id="stat-quantity">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <h3>Total Nilai (Rp)</h3>
                <div class="stat-value" id="stat-value">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <h3>Rata-rata Harga (Rp/kg)</h3>
                <div class="stat-value" id="stat-avg-price">-</div>
            </div>
        </div>

        <!-- Charts Section -->
        <div class="charts-section">
            <div class="chart-card">
                <h3><i class="fas fa-chart-pie"></i> Distribusi Komoditas</h3>
                <div class="chart-container">
                    <canvas id="commodityChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3><i class="fas fa-chart-bar"></i> Distribusi Ukuran</h3>
                <div class="chart-container">
                    <canvas id="sizeChart"></canvas>
                </div>
            </div>
            <div class="chart-card">
                <h3><i class="fas fa-chart-line"></i> Trend Panen Bulanan</h3>
                <div class="chart-container">
                    <canvas id="monthlyChart"></canvas>
                </div>
            </div>
        </div>

        <!-- Records Table -->
        <div class="records-section">
            <div class="records-header">
                <h2>Catatan Hasil Panen</h2>
            </div>
            <div id="records-container">
                <div class="loading">
                    <div class="spinner"></div>
                    Memuat data...
                </div>
            </div>
        </div>
    </div>

    <!-- Add/Edit Record Modal -->
    <div id="record-modal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2><i class="fas fa-plus-circle"></i> Tambah Data Panen</h2>
                <button class="close-modal" onclick="closeModal('record-modal')">&times;</button>
            </div>

            <form id="record-form" onsubmit="submitRecord(event)">
                <div class="form-group">
                    <label>Nama Petani *</label>
                    <input type="text" id="farmer-name" required>
                </div>

                <div class="form-group">
                    <label>Nomor WhatsApp *</label>
                    <input type="tel" id="farmer-phone" placeholder="08xxxxxxxxxx" required>
                </div>

                <div class="form-row">
                    <div class="form-group">
                        <label>Komoditas *</label>
                        <select id="commodity" required>
                            <option value="">Pilih Komoditas</option>
                            <option value="padi">Padi</option>
                            <option value="jagung">Jagung</option>
                            <option value="cabai">Cabai</option>
                            <option value="tomat">Tomat</option>
                            <option value="kentang">Kentang</option>
                            <option value="bawang">Bawang Merah</option>
                            <option value="kedelai">Kedelai</option>
                            <option value="kacang">Kacang Tanah</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>Tanggal Panen *</label>
                        <input type="date" id="harvest-date" required>
                    </div>
                </div>

                <div class="form-group">
                    <label>Lokasi *</label>
                    <input type="text" id="location" placeholder="Contoh: Desa Sukamaju, Kec. Cianjur" required>
                </div>

                <div class="criteria-section">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h3 style="color: #2d3748; font-size: 1.1rem;">Kriteria Hasil Panen</h3>
                        <button type="button" class="btn btn-primary btn-small" onclick="addCriterion()">
                            <i class="fas fa-plus"></i> Tambah Kriteria
                        </button>
                    </div>
                    <div id="criteria-container"></div>
                </div>

                <div style="display: flex; gap: 10px; margin-top: 25px;">
                    <button type="submit" class="btn btn-primary" style="flex: 1;">
                        <i class="fas fa-check"></i> Simpan Data
                    </button>
                    <button type="button" class="btn btn-secondary" onclick="closeModal('record-modal')">
                        <i class="fas fa-times"></i> Batal
                    </button>
                </div>
            </form>
        </div>
    </div>

    <!-- Toast Container -->
    <div class="toast-container" id="toast-container"></div>

    <script>
        let allRecords = [];
        let criteriaCount = 0;
        let charts = {};

        // Load data on page load
        document.addEventListener('DOMContentLoaded', () => {
            loadRecords();
            loadFarmerInfoFromStorage();
        });

        // ========== DATA LOADING ==========

        async function loadRecords(farmerPhone = null) {
            try {
                let url = '/api/harvest/records';
                if (farmerPhone) {
                    url += `?farmer_phone=${farmerPhone}`;
                }

                const response = await fetch(url);
                const result = await response.json();

                if (result.success) {
                    allRecords = result.data;
                    displayRecords(allRecords);
                    await loadStatistics(farmerPhone);
                    await loadCharts(farmerPhone);
                } else {
                    showError('Gagal memuat data');
                }
            } catch (error) {
                console.error('Error loading records:', error);
                showError('Terjadi kesalahan saat memuat data');
            }
        }

        async function loadStatistics(farmerPhone = null) {
            try {
                let url = '/api/harvest/statistics';
                if (farmerPhone) {
                    url += `?farmer_phone=${farmerPhone}`;
                }

                const response = await fetch(url);
                const result = await response.json();

                if (result.success) {
                    const stats = result.data;
                    document.getElementById('stat-records').textContent = stats.total_records;
                    document.getElementById('stat-quantity').textContent = stats.total_quantity_kg.toLocaleString('id-ID');
                    document.getElementById('stat-value').textContent = 'Rp ' + Math.round(stats.total_value / 1000) + 'K';
                    document.getElementById('stat-avg-price').textContent = 'Rp ' + Math.round(stats.avg_price_per_kg).toLocaleString('id-ID');
                }
            } catch (error) {
                console.error('Error loading statistics:', error);
            }
        }

        async function loadCharts(farmerPhone = null) {
            try {
                let url = '/api/harvest/chart-data';
                if (farmerPhone) {
                    url += `?farmer_phone=${farmerPhone}`;
                }

                const response = await fetch(url);
                const result = await response.json();

                if (result.success) {
                    const data = result.data;
                    createCommodityChart(data.commodity_distribution);
                    createSizeChart(data.size_distribution);
                    createMonthlyChart(data.monthly_trend);
                }
            } catch (error) {
                console.error('Error loading charts:', error);
            }
        }

        // ========== CHARTS ==========

        function createCommodityChart(data) {
            const ctx = document.getElementById('commodityChart');
            
            if (charts.commodity) {
                charts.commodity.destroy();
            }

            charts.commodity = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: data.labels,
                    datasets: [{
                        data: data.data,
                        backgroundColor: [
                            '#10b981', '#3b82f6', '#f59e0b', '#ef4444',
                            '#8b5cf6', '#ec4899', '#14b8a6', '#f97316'
                        ]
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }

        function createSizeChart(data) {
            const ctx = document.getElementById('sizeChart');
            
            if (charts.size) {
                charts.size.destroy();
            }

            charts.size = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Jumlah (kg)',
                        data: data.quantities,
                        backgroundColor: '#10b981'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        function createMonthlyChart(data) {
            const ctx = document.getElementById('monthlyChart');
            
            if (charts.monthly) {
                charts.monthly.destroy();
            }

            charts.monthly = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: data.labels,
                    datasets: [{
                        label: 'Jumlah Panen (kg)',
                        data: data.quantities,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }

        // ========== RECORDS DISPLAY ==========

        function displayRecords(records) {
            const container = document.getElementById('records-container');

            if (records.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <div style="font-size: 5rem; margin-bottom: 20px;">📝</div>
                        <h3>Belum Ada Data</h3>
                        <p>Mulai catat hasil panen Anda</p>
                        <button class="btn btn-primary" onclick="showAddRecordModal()" style="margin-top: 20px;">
                            <i class="fas fa-plus"></i> Tambah Data Pertama
                        </button>
                    </div>
                `;
                return;
            }

            let html = `
                <table>
                    <thead>
                        <tr>
                            <th>Tanggal</th>
                            <th>Komoditas</th>
                            <th>Lokasi</th>
                            <th>Total (kg)</th>
                            <th>Nilai (Rp)</th>
                            <th>Aksi</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            records.forEach(record => {
                html += `
                    <tr onclick="toggleDetails('${record.id}')" style="cursor: pointer;">
                        <td>${record.harvest_date}</td>
                        <td>${record.commodity}</td>
                        <td>${record.location}</td>
                        <td>${record.total_quantity} kg</td>
                        <td>Rp ${record.total_value.toLocaleString('id-ID')}</td>
                        <td>
                            <button class="btn btn-danger btn-small" onclick="event.stopPropagation(); deleteRecord('${record.id}')">
                                <i class="fas fa-trash"></i>
                            </button>
                        </td>
                    </tr>
                    <tr id="details-${record.id}" class="expandable-row" style="display: none;">
                        <td colspan="6">
                            <strong>Detail Kriteria:</strong>
                            <table class="criteria-table">
                                <thead>
                                    <tr>
                                        <th>Ukuran</th>
                                        <th>Jumlah (kg)</th>
                                        <th>Harga/kg</th>
                                        <th>Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${record.criteria.map(c => `
                                        <tr>
                                            <td>${c.size}</td>
                                            <td>${c.quantity_kg} kg</td>
                                            <td>Rp ${c.price_per_kg.toLocaleString('id-ID')}</td>
                                            <td>Rp ${c.total.toLocaleString('id-ID')}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </td>
                    </tr>
                `;
            });

            html += '</tbody></table>';
            container.innerHTML = html;
        }

        function toggleDetails(recordId) {
            const row = document.getElementById(`details-${recordId}`);
            row.style.display = row.style.display === 'none' ? 'table-row' : 'none';
        }

        // ========== ADD/EDIT RECORD ==========

        function showAddRecordModal() {
            document.getElementById('record-modal').classList.add('active');
            criteriaCount = 0;
            document.getElementById('criteria-container').innerHTML = '';
            addCriterion(); // Add first criterion by default
        }

        function addCriterion() {
            criteriaCount++;
            const container = document.getElementById('criteria-container');
            
            const criterionHtml = `
                <div class="criteria-item" id="criterion-${criteriaCount}">
                    <div class="criteria-header">
                        <strong>Kriteria #${criteriaCount}</strong>
                        <button type="button" class="btn btn-danger btn-small" onclick="removeCriterion(${criteriaCount})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                    <div class="form-group">
                        <label>Ukuran/Grade *</label>
                        <select class="criterion-size" required>
                            <option value="">Pilih Ukuran</option>
                            <option value="A (Besar)">A (Besar)</option>
                            <option value="B (Sedang)">B (Sedang)</option>
                            <option value="C (Kecil)">C (Kecil)</option>
                            <option value="Premium">Premium</option>
                            <option value="Standar">Standar</option>
                            <option value="Ekonomis">Ekonomis</option>
                        </select>
                    </div>
                    <div class="form-row">
                        <div class="form-group">
                            <label>Jumlah (kg) *</label>
                            <input type="number" class="criterion-quantity" step="0.1" min="0.1" required>
                        </div>
                        <div class="form-group">
                            <label>Harga per kg (Rp) *</label>
                            <input type="number" class="criterion-price" step="100" min="100" required>
                        </div>
                    </div>
                </div>
            `;
            
            container.insertAdjacentHTML('beforeend', criterionHtml);
        }

        function removeCriterion(id) {
            const element = document.getElementById(`criterion-${id}`);
            if (element) {
                element.remove();
            }
        }

        async function submitRecord(event) {
            event.preventDefault();

            const submitBtn = event.target.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Menyimpan...';

            // Collect criteria
            const criteriaElements = document.querySelectorAll('.criteria-item');
            const criteria = [];
            
            criteriaElements.forEach(el => {
                const size = el.querySelector('.criterion-size').value;
                const quantity = parseFloat(el.querySelector('.criterion-quantity').value);
                const price = parseFloat(el.querySelector('.criterion-price').value);
                
                if (size && quantity && price) {
                    criteria.push({
                        size: size,
                        quantity_kg: quantity,
                        price_per_kg: price
                    });
                }
            });

            if (criteria.length === 0) {
                showToast('error', 'Minimal satu kriteria harus diisi');
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Simpan Data';
                return;
            }

            const recordData = {
                farmer_name: document.getElementById('farmer-name').value,
                farmer_phone: document.getElementById('farmer-phone').value,
                commodity: document.getElementById('commodity').value,
                location: document.getElementById('location').value,
                harvest_date: document.getElementById('harvest-date').value,
                criteria: criteria
            };

            try {
                const response = await fetch('/api/harvest/records', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(recordData)
                });

                const result = await response.json();

                if (result.success) {
                    showToast('success', 'Data berhasil disimpan!');
                    closeModal('record-modal');
                    document.getElementById('record-form').reset();
                    
                    // Save farmer info
                    saveFarmerInfo(recordData.farmer_name, recordData.farmer_phone);
                    
                    // Reload data
                    await loadRecords();
                } else {
                    showToast('error', result.error || 'Gagal menyimpan data');
                }
            } catch (error) {
                console.error('Error submitting record:', error);
                showToast('error', 'Terjadi kesalahan saat menyimpan data');
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerHTML = '<i class="fas fa-check"></i> Simpan Data';
            }
        }

        async function deleteRecord(recordId) {
            if (!confirm('Yakin ingin menghapus data ini?')) {
                return;
            }

            try {
                const response = await fetch(`/api/harvest/records/${recordId}`, {
                    method: 'DELETE'
                });

                const result = await response.json();

                if (result.success) {
                    showToast('success', 'Data berhasil dihapus');
                    await loadRecords();
                } else {
                    showToast('error', 'Gagal menghapus data');
                }
            } catch (error) {
                console.error('Error deleting record:', error);
                showToast('error', 'Terjadi kesalahan');
            }
        }

        // ========== MY DASHBOARD ==========

        function showMyDashboard() {
            const phone = prompt('Masukkan nomor WhatsApp Anda:');
            if (phone) {
                localStorage.setItem('harvest_farmer_phone', phone);
                loadRecords(phone);
                showToast('success', 'Menampilkan data Anda');
            }
        }

        // ========== UTILITIES ==========

        function closeModal(modalId) {
            document.getElementById(modalId).classList.remove('active');
        }

        function showToast(type, message) {
            const container = document.getElementById('toast-container');
            const toast = document.createElement('div');
            toast.className = `toast toast-${type}`;

            const icons = {
                success: '✅',
                error: '❌'
            };

            toast.innerHTML = `
                <div style="font-size: 1.5rem;">${icons[type]}</div>
                <div>${message}</div>
            `;

            container.appendChild(toast);

            setTimeout(() => {
                toast.remove();
            }, 4000);
        }

        function showError(message) {
            const container = document.getElementById('records-container');
            container.innerHTML = `
                <div class="empty-state">
                    <div style="font-size: 5rem; margin-bottom: 20px;">⚠️</div>
                    <h3>Terjadi Kesalahan</h3>
                    <p>${message}</p>
                    <button class="btn btn-primary" onclick="loadRecords()">
                        <i class="fas fa-redo"></i> Coba Lagi
                    </button>
                </div>
            `;
        }

        function saveFarmerInfo(name, phone) {
            localStorage.setItem('harvest_farmer_name', name);
            localStorage.setItem('harvest_farmer_phone', phone);
        }

        function loadFarmerInfoFromStorage() {
            const savedName = localStorage.getItem('harvest_farmer_name');
            const savedPhone = localStorage.setItem('harvest_farmer_phone');

            if (savedName) document.getElementById('farmer-name').value = savedName;
            if (savedPhone) document.getElementById('farmer-phone').value = savedPhone;
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            if (event.target.classList.contains('modal')) {
                event.target.classList.remove('active');
            }
        }
    </script>
</body>
</html>
'''

# Write to file
with open('templates/modules/harvest_database.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Harvest Database HTML created successfully!")
