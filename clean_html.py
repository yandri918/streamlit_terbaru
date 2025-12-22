"""Clean up harvest_database.html by removing content after the first </html>."""

file_path = 'templates/modules/harvest_database.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find the first occurrence of </html>
end_tag = '</html>'
idx = content.find(end_tag)

if idx != -1:
    # Keep content up to and including </html>
    clean_content = content[:idx + len(end_tag)]
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(clean_content)
    
    print(f"✅ File cleaned! Truncated at character {idx}")
else:
    print("⚠️ </html> tag not found!")
