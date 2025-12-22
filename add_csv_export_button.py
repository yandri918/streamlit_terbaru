"""Add CSV export button to harvest database frontend."""

with open('templates/modules/harvest_database.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add export button next to "Dashboard Saya" button
export_button = '''
                <button class="btn btn-success" onclick="exportToCSV()">
                    <i class="fas fa-file-excel"></i> Unduh CSV
                </button>'''

content = content.replace(
    '''<button class="btn btn-secondary" onclick="showMyDashboard()">
                    <i class="fas fa-user"></i> Dashboard Saya
                </button>''',
    '''<button class="btn btn-secondary" onclick="showMyDashboard()">
                    <i class="fas fa-user"></i> Dashboard Saya
                </button>
                ''' + export_button
)

# 2. Add exportToCSV function
export_function = '''
        // ========== CSV EXPORT ==========
        
        function exportToCSV() {
            const farmerPhone = localStorage.getItem('farmer_phone');
            
            if (!farmerPhone) {
                showToast('Masukkan nomor HP di Dashboard Saya terlebih dahulu', 'error');
                return;
            }
            
            // Show loading
            showToast('Mengunduh data...', 'info');
            
            // Download CSV
            const url = `/api/harvest/export/csv?farmer_phone=${encodeURIComponent(farmerPhone)}`;
            window.location.href = url;
            
            setTimeout(() => {
                showToast('Data berhasil diunduh!', 'success');
            }, 1000);
        }
        
        function exportAllToCSV() {
            showToast('Mengunduh semua data...', 'info');
            window.location.href = '/api/harvest/export/csv';
            
            setTimeout(() => {
                showToast('Data berhasil diunduh!', 'success');
            }, 1000);
        }
'''

# Insert before submitRecord function
content = content.replace(
    '        // ========== COST CALCULATION ==========',
    export_function + '\n        // ========== COST CALCULATION =========='
)

# Write updated content
with open('templates/modules/harvest_database.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Added CSV export button!")
print("✅ Petani bisa unduh data panen ke Excel/CSV")
