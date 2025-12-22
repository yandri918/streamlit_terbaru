"""Add Cabe Rawit Merah to chili pepper options."""

# Update AgriShop HTML
with open('templates/modules/agrishop.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add cabe rawit merah after cabe rawit hijau
content = content.replace(
    '<option value="cabe_rawit_hijau">Cabe Rawit Hijau</option>',
    '<option value="cabe_rawit_hijau">Cabe Rawit Hijau</option>\n                        <option value="cabe_rawit_merah">Cabe Rawit Merah</option>'
)

# Also update the second occurrence (in the form)
content = content.replace(
    '<option value="cabe_rawit_hijau">Cabe Rawit Hijau</option>\n                            <option value="cabe_hijau_besar">',
    '<option value="cabe_rawit_hijau">Cabe Rawit Hijau</option>\n                            <option value="cabe_rawit_merah">Cabe Rawit Merah</option>\n                            <option value="cabe_hijau_besar">'
)

# Add to emoji mapping
content = content.replace(
    "'cabe_rawit_hijau': '🌶️',",
    "'cabe_rawit_hijau': '🌶️',\n                'cabe_rawit_merah': '🌶️',"
)

with open('templates/modules/agrishop.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated AgriShop with Cabe Rawit Merah")

# Update Harvest Database HTML
with open('templates/modules/harvest_database.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add cabe rawit merah
content = content.replace(
    '<option value="cabe_rawit_hijau">Cabe Rawit Hijau</option>',
    '<option value="cabe_rawit_hijau">Cabe Rawit Hijau</option>\n                            <option value="cabe_rawit_merah">Cabe Rawit Merah</option>'
)

# Add to emoji mapping
content = content.replace(
    "'cabe_rawit_hijau': '🌶️',",
    "'cabe_rawit_hijau': '🌶️',\n                'cabe_rawit_merah': '🌶️',"
)

with open('templates/modules/harvest_database.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated Harvest Database with Cabe Rawit Merah")
print("\n✅ Cabe Rawit Merah berhasil ditambahkan!")
print("Total: 6 jenis cabe")
