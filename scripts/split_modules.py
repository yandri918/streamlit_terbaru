import os
from bs4 import BeautifulSoup

# Define paths
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), '..', 'templates')
MODULES_DIR = os.path.join(TEMPLATES_DIR, 'modules')
INDEX_FILE = os.path.join(TEMPLATES_DIR, 'index.html')

# Ensure modules directory exists
os.makedirs(MODULES_DIR, exist_ok=True)

# Read and parse the original index.html
with open(INDEX_FILE, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Find all module divs
modules = soup.find_all('div', class_='module')

# Extract CSS and JavaScript
css_style = soup.find('style').prettify()
javascript_block = soup.find('script', {'src': None}).prettify()

def create_slug(title):
    """Creates a URL-friendly slug from a module title."""
    # Remove emoji and leading/trailing whitespace
    title = ''.join(c for c in title if c.isalnum() or c.isspace())
    # Replace spaces with underscores and convert to lowercase
    return title.strip().replace(' ', '_').lower()

# Process each module
for module_div in modules:
    h2_tag = module_div.find('h2')
    if not h2_tag:
        continue

    # Extract title and create a slug
    # Example: "🔬 Modul 1: Dokter Tanaman" -> "modul_1_dokter_tanaman"
    full_title = h2_tag.get_text(strip=True)
    simple_title = full_title.split(':')[-1].strip()
    slug = create_slug(simple_title)
    file_path = os.path.join(MODULES_DIR, f"{slug}.html")

    # Create a new soup for the module page
    module_soup = BeautifulSoup(f"""
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{full_title} - Agrisensa</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    {css_style}
</head>
<body>
    <div class="container mx-auto p-4 md:p-8">
        <a href="/dashboard" style="display: inline-block; margin-bottom: 20px; color: var(--primary-color); text-decoration: none; font-weight: 500;">&larr; Kembali ke Dasbor</a>
    </div>
</body>
</html>
    """, 'html.parser')

    # Insert the module div into the body
    module_soup.body.find('div').append(module_div)

    # Append the JavaScript block
    script_tag = BeautifulSoup(javascript_block, 'html.parser')
    module_soup.body.append(script_tag)

    # Write the new file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(module_soup))

    print(f"Created module page: {file_path}")

print("Module extraction complete.")
