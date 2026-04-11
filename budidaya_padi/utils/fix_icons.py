"""
Script to fix icon display issues in all page files
Replaces st.title() with st.markdown() for proper HTML rendering
"""

import os
import re
from pathlib import Path

# Define the pages directory
pages_dir = Path(r"c:\Users\yandr\OneDrive\Desktop\agrisensa-api\budidaya_padi\pages")

def fix_page_file(filepath):
    """Fix icon rendering in a single page file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace st.title(f"{icon(...)} Title") with st.markdown for proper HTML rendering
    # Pattern: st.title(f"{icon('name', ...)} Title")
    pattern = r'st\.title\(f"\{icon\((.*?)\)\}\s*(.*?)"\)'
    
    def replacement(match):
        icon_args = match.group(1)
        title_text = match.group(2)
        return f"st.markdown(f\"<h1 style='margin-bottom: 0;'>{{icon({icon_args})}} {title_text}</h1>\", unsafe_allow_html=True)"
    
    content = re.sub(pattern, replacement, content)
    
    # Also fix any st.header or st.subheader with icons (though less common)
    pattern_header = r'st\.header\(f"\{icon\((.*?)\)\}\s*(.*?)"\)'
    def replacement_header(match):
        icon_args = match.group(1)
        title_text = match.group(2)
        return f"st.markdown(f\"<h2>{{icon({icon_args})}} {title_text}</h2>\", unsafe_allow_html=True)"
    
    content = re.sub(pattern_header, replacement_header, content)
    
    return content

def main():
    """Main function to process all page files"""
    
    # Get all page files
    page_files = list(pages_dir.glob("*.py"))
    
    print(f"Found {len(page_files)} page files")
    
    for filepath in page_files:
        filename = filepath.name
        print(f"\nProcessing: {filename}")
        
        try:
            updated_content = fix_page_file(filepath)
            
            # Write back to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"  ✓ Fixed icon rendering")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("Icon fix complete!")

if __name__ == "__main__":
    main()
