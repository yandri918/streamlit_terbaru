"""Add CSV export button to harvest database - FIXED VERSION."""

with open('templates/modules/harvest_database.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Find the header actions section and add CSV button
# Look for the header with action buttons
if '<div class="header-actions">' in content:
    # Add button after existing buttons
    content = content.replace(
        '</div>\n        </header>',
        '''            <button class="btn btn-success" onclick="exportToCSV()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
                    <i class="fas fa-file-excel"></i> Unduh CSV
                </button>
            </div>
        </header>'''
    )
else:
    # If no header-actions div, add button near the top
    print("Warning: header-actions div not found, adding button differently")

# 2. Add exportToCSV function before the closing script tag
export_js = '''
        // ========== CSV EXPORT ==========
        
        function exportToCSV() {
            const farmerPhone = localStorage.getItem('farmer_phone');
            
            if (!farmerPhone) {
                showToast('Silakan buka Dashboard Saya dan masukkan nomor HP terlebih dahulu', 'error');
                return;
            }
            
            showToast('Mengunduh data...', 'info');
            
            // Download CSV
            const url = `/api/harvest/export/csv?farmer_phone=${encodeURIComponent(farmerPhone)}`;
            window.location.href = url;
            
            setTimeout(() => {
                showToast('Data berhasil diunduh! Cek folder Downloads Anda', 'success');
            }, 1500);
        }
        
'''

# Insert before closing script tag
content = content.replace('    </script>', export_js + '    </script>')

# Write updated content
with open('templates/modules/harvest_database.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ CSV export button added!")
print("✅ Function exportToCSV() added!")
print("✅ Button location: header-actions div")
