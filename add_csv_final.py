"""Add CSV export button - FINAL VERSION."""

with open('templates/modules/harvest_database.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with "Dashboard Saya" button and add CSV button after it
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'Dashboard Saya' in line and '</button>' in line:
        # Add CSV button on next line
        indent = '                '
        csv_button = f'{indent}<button class="btn btn-success" onclick="exportToCSV()" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">\n'
        csv_button += f'{indent}    <i class="fas fa-file-excel"></i> Unduh CSV\n'
        csv_button += f'{indent}</button>\n'
        new_lines.append(csv_button)

# Find closing script tag and add function before it
final_lines = []
for i, line in enumerate(new_lines):
    if line.strip() == '</script>':
        # Add CSV function before closing script
        csv_function = '''
        // ========== CSV EXPORT ==========
        
        function exportToCSV() {
            const farmerPhone = localStorage.getItem('harvest_farmer_phone');
            
            if (!farmerPhone) {
                showToast('error', 'Silakan buka Dashboard Saya dan masukkan nomor HP terlebih dahulu');
                return;
            }
            
            showToast('success', 'Mengunduh data...');
            
            // Download CSV
            const url = `/api/harvest/export/csv?farmer_phone=${encodeURIComponent(farmerPhone)}`;
            window.location.href = url;
            
            setTimeout(() => {
                showToast('success', 'Data berhasil diunduh! Cek folder Downloads Anda');
            }, 1500);
        }
        
'''
        final_lines.append(csv_function)
    final_lines.append(line)

# Write back
with open('templates/modules/harvest_database.html', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("✅ CSV export button added successfully!")
print("✅ CSV export function added successfully!")
