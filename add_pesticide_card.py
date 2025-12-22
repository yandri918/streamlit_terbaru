import re

# Read the file
with open('templates/home.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line with "pustaka-dokumen" and add pesticide card after its closing </a>
pesticide_card_lines = [
    '\n',
    '            <a href="/modules/pesticide-knowledge" class="module-card">\n',
    '                <div class="module-icon">🧪</div>\n',
    '                <h3 class="module-title">Info Pestisida</h3>\n',
    '                <p class="module-desc">Direktori bahan aktif, cara kerja, dan keamanan.</p>\n',
    '                <span class="module-link">Cari Bahan Aktif</span>\n',
    '            </a>\n'
]

# Find the index where we need to insert (after Pustaka Dokumen)
insert_index = None
for i, line in enumerate(lines):
    if 'pustaka-dokumen' in line:
        # Find the closing </a> tag for this card
        for j in range(i, min(i+10, len(lines))):
            if '</a>' in lines[j] and 'href' not in lines[j]:
                insert_index = j + 1
                break
        break

if insert_index:
    # Insert the pesticide card
    lines[insert_index:insert_index] = pesticide_card_lines
    
    # Write back
    with open('templates/home.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'✅ Pesticide card added successfully after line {insert_index}!')
else:
    print('❌ Could not find insertion point')
