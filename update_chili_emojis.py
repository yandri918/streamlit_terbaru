"""Update emoji mappings for chili peppers in HTML files."""

# Update AgriShop HTML
with open('templates/modules/agrishop.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the emoji mapping
content = content.replace(
    "'cabai': '🌶️',",
    "'cabe_merah_keriting': '🌶️',\n                'cabe_merah_besar': '🌶️',\n                'cabe_rawit_hijau': '🌶️',\n                'cabe_hijau_besar': '🌶️',\n                'cabe_keriting_hijau': '🌶️',"
)

with open('templates/modules/agrishop.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated AgriShop emoji mappings")

# Update Harvest Database HTML  
with open('templates/modules/harvest_database.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "'cabai': '🌶️',",
    "'cabe_merah_keriting': '🌶️',\n                'cabe_merah_besar': '🌶️',\n                'cabe_rawit_hijau': '🌶️',\n                'cabe_hijau_besar': '🌶️',\n                'cabe_keriting_hijau': '🌶️',"
)

with open('templates/modules/harvest_database.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Updated Harvest Database emoji mappings")
print("\n✅ All chili pepper updates complete!")
