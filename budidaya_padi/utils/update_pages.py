"""
Script to remove emojis from all page files and rename them
"""

import os
import re
import shutil
from pathlib import Path

# Define the pages directory
pages_dir = Path(r"c:\Users\yandr\OneDrive\Desktop\agrisensa-api\budidaya_padi\pages")

# Icon mapping for each page
ICON_MAPPING = {
    "RAB_Calculator": ("calculator", "RAB Calculator"),
    "Panduan_Budidaya": ("book-open", "Panduan Budidaya"),
    "Hama_Penyakit": ("bug", "Hama & Penyakit"),
    "SOP_Budidaya": ("clipboard-list", "SOP Budidaya"),
    "Kalkulator_Pupuk": ("flask", "Kalkulator Pupuk"),
    "Kalender_Tanam": ("calendar-alt", "Kalender Tanam"),
    "Analisis_Bisnis": ("chart-line", "Analisis Bisnis"),
    "Varietas_Padi": ("seedling", "Varietas Padi"),
    "Manajemen_Air": ("tint", "Manajemen Air"),
    "Analisis_Tanah": ("vial", "Analisis Tanah"),
    "Strategi_Semprot": ("spray-can", "Strategi Semprot"),
    "Monitoring_Logbook": ("book", "Monitoring Logbook"),
    "Mekanisasi": ("tractor", "Mekanisasi"),
    "Monitoring_Cuaca": ("cloud-sun", "Monitoring Cuaca"),
}

def remove_emojis(text):
    """Remove all emojis from text"""
    # Emoji pattern
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

def update_page_file(filepath, icon_name, page_title):
    """Update a single page file to remove emojis and add design system"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove emojis from entire content
    content = remove_emojis(content)
    
    # Add design system import after other imports
    if 'from design_system import' not in content:
        # Find the last import statement
        import_pattern = r'(import .*\n)(\n# Page config)'
        replacement = r'\1\nimport sys\nfrom pathlib import Path\n\n# Add utils to path\nif str(Path(__file__).parent.parent / "utils") not in sys.path:\n    sys.path.append(str(Path(__file__).parent.parent / "utils"))\n\nfrom design_system import apply_design_system, icon, COLORS\n\2'
        content = re.sub(import_pattern, replacement, content)
    
    # Add apply_design_system() after page config
    if 'apply_design_system()' not in content:
        content = re.sub(
            r'(\)\n\n)(# Header|st\.title)',
            r'\1# Apply Design System\napply_design_system()\n\n\2',
            content
        )
    
    # Update page title with icon
    content = re.sub(
        r'st\.title\(["\'].*?["\']',
        f'st.title(f"{{icon(\'{icon_name}\', size=\'lg\')}} {page_title}"',
        content,
        count=1
    )
    
    # Update tab labels (remove emojis, keep text)
    content = re.sub(r'st\.tabs\(\[(.*?)\]\)', lambda m: f'st.tabs([{remove_emojis(m.group(1))}])', content)
    
    # Update st.header, st.subheader calls
    content = re.sub(r'st\.header\("(.*?)"\)', lambda m: f'st.header("{remove_emojis(m.group(1))}")', content)
    content = re.sub(r'st\.subheader\("(.*?)"\)', lambda m: f'st.subheader("{remove_emojis(m.group(1))}")', content)
    
    # Update st.markdown headers
    content = re.sub(r'st\.markdown\("###? (.*?)"\)', lambda m: f'st.markdown("### {remove_emojis(m.group(1))}")', content)
    content = re.sub(r'st\.markdown\("\*\*(.*?)\*\*"\)', lambda m: f'st.markdown("**{remove_emojis(m.group(1))}**")', content)
    
    # Update button labels
    content = re.sub(r'st\.button\("(.*?)"', lambda m: f'st.button("{remove_emojis(m.group(1))}"', content)
    
    return content

def main():
    """Main function to process all page files"""
    
    # Get all page files
    page_files = list(pages_dir.glob("*.py"))
    
    print(f"Found {len(page_files)} page files")
    
    for old_path in page_files:
        filename = old_path.name
        print(f"\nProcessing: {filename}")
        
        # Extract the base name (remove number prefix and emoji)
        # Pattern: 01_💰_RAB_Calculator.py -> RAB_Calculator
        match = re.search(r'\d+_.*?_(.+)\.py', filename)
        if not match:
            print(f"  Skipping {filename} - doesn't match pattern")
            continue
        
        base_name = match.group(1)
        
        # Get icon and title
        if base_name not in ICON_MAPPING:
            print(f"  Warning: No icon mapping for {base_name}")
            continue
        
        icon_name, page_title = ICON_MAPPING[base_name]
        
        # Create new filename (keep number prefix, remove emoji)
        number_prefix = filename.split('_')[0]
        new_filename = f"{number_prefix}_{base_name}.py"
        new_path = pages_dir / new_filename
        
        print(f"  New name: {new_filename}")
        print(f"  Icon: {icon_name}")
        
        # Update file content
        try:
            updated_content = update_page_file(old_path, icon_name, page_title)
            
            # Write to new file
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"  ✓ Updated and saved")
            
            # Remove old file if different name
            if old_path != new_path:
                old_path.unlink()
                print(f"  ✓ Removed old file")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("Processing complete!")

if __name__ == "__main__":
    main()
