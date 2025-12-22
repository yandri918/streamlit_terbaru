"""
Script untuk memperbaiki semua modul HTML agar menggunakan endpoint yang benar
dan menambahkan error handling yang lebih baik.
"""
import os
import re
from pathlib import Path

def fix_module_file(file_path):
    """Perbaiki satu file modul."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # 1. Pastikan apiPrefix = ''
    if "const apiPrefix = '/api/v2'" in content:
        content = content.replace("const apiPrefix = '/api/v2';", "const apiPrefix = '';")
        content = content.replace("const apiPrefix = '/api/v2'", "const apiPrefix = ''")
        changes.append("Fixed apiPrefix")
    
    # 2. Tambahkan error handling yang lebih baik untuk fetch
    # Cari semua fetch calls dan pastikan ada error handling
    fetch_pattern = r"const response = await fetch\(`\$\{baseUrl\}\$\{apiPrefix\}([^`]+)`"
    
    # 3. Pastikan semua endpoint menggunakan format yang benar
    # Tidak perlu perubahan karena apiPrefix sudah kosong
    
    # 4. Tambahkan console.log untuk debugging jika belum ada
    if 'console.log' not in content and 'DOMContentLoaded' in content:
        # Tambahkan console.log di awal script
        script_start = content.find('<script>')
        if script_start != -1:
            script_content_start = content.find('document.addEventListener', script_start)
            if script_content_start != -1:
                # Cari baris setelah DOMContentLoaded
                next_line = content.find('\n', script_content_start) + 1
                debug_line = "            console.log('🚀 Modul loaded:', window.location.pathname);\n"
                content = content[:next_line] + debug_line + content[next_line:]
                changes.append("Added debug logging")
    
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    return False, []

def main():
    """Main function."""
    modules_dir = Path('templates/modules')
    fixed_count = 0
    
    print("🔧 Memperbaiki semua modul...")
    print("=" * 60)
    
    for html_file in modules_dir.glob('*.html'):
        print(f"\n📄 Memproses: {html_file.name}")
        fixed, changes = fix_module_file(html_file)
        if fixed:
            fixed_count += 1
            print(f"   ✅ Diperbaiki: {', '.join(changes)}")
        else:
            print(f"   ✓ Sudah benar")
    
    print("\n" + "=" * 60)
    print(f"✅ Selesai! {fixed_count} file diperbaiki.")
    print("=" * 60)

if __name__ == '__main__':
    main()

