"""
Script to add proper imports to all page files that are missing them
"""

import os
import re
from pathlib import Path

# Define the pages directory
pages_dir = Path(r"c:\Users\yandr\OneDrive\Desktop\agrisensa-api\budidaya_padi\pages")

IMPORT_BLOCK = '''import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
    from design_system import apply_design_system, icon, COLORS

'''

def fix_page_imports(filepath):
    """Add imports if missing"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if imports are already there
    if 'from utils.design_system import' in content or 'from design_system import' in content:
        print(f"  ✓ Imports already present")
        return content
    
    # Find the st.set_page_config line
    match = re.search(r'(st\.set_page_config\([^)]+\))', content)
    
    if match:
        # Insert imports before set_page_config
        insert_pos = match.start()
        content = content[:insert_pos] + IMPORT_BLOCK + content[insert_pos:]
        print(f"  ✓ Added imports")
    else:
        print(f"  ✗ Could not find set_page_config")
    
    return content

def main():
    """Main function to process all page files"""
    
    # Get all page files
    page_files = list(pages_dir.glob("*.py"))
    
    print(f"Found {len(page_files)} page files\n")
    
    for filepath in page_files:
        filename = filepath.name
        print(f"Processing: {filename}")
        
        try:
            updated_content = fix_page_imports(filepath)
            
            # Write back to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("Import addition complete!")

if __name__ == "__main__":
    main()
