"""
Script to fix import issues in all page files
Updates import statements to work with Streamlit Cloud
"""

import os
import re
from pathlib import Path

# Define the pages directory
pages_dir = Path(r"c:\Users\yandr\OneDrive\Desktop\agrisensa-api\budidaya_padi\pages")
app_file = Path(r"c:\Users\yandr\OneDrive\Desktop\agrisensa-api\budidaya_padi\app.py")

def fix_imports(filepath):
    """Fix import statements to use simpler approach"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the complex path manipulation with a simpler try-except approach
    old_import_pattern = r'''import sys
from pathlib import Path

# Add utils to path.*?
if str\(Path\(__file__\)\.parent.*?\) not in sys\.path:
    sys\.path\.append\(str\(Path\(__file__\)\.parent.*?\)\)

from design_system import apply_design_system, icon, COLORS'''
    
    new_import = '''import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
    from design_system import apply_design_system, icon, COLORS'''
    
    content = re.sub(old_import_pattern, new_import, content, flags=re.DOTALL)
    
    return content

def fix_app_imports(filepath):
    """Fix imports in app.py"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the import section
    old_pattern = r'''import sys
from pathlib import Path

# Add utils to path for design system
if str\(Path\(__file__\)\.parent / 'utils'\) not in sys\.path:
    sys\.path\.append\(str\(Path\(__file__\)\.parent / 'utils'\)\)

from design_system import apply_design_system, icon, COLORS, ICONS'''
    
    new_import = '''import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS, ICONS
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent / "utils"))
    from design_system import apply_design_system, icon, COLORS, ICONS'''
    
    content = re.sub(old_pattern, new_import, content, flags=re.DOTALL)
    
    return content

def main():
    """Main function to process all files"""
    
    # Fix app.py
    print("Fixing app.py imports...")
    try:
        updated_content = fix_app_imports(app_file)
        with open(app_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("  ✓ Fixed app.py")
    except Exception as e:
        print(f"  ✗ Error in app.py: {e}")
    
    # Fix all page files
    page_files = list(pages_dir.glob("*.py"))
    print(f"\nFound {len(page_files)} page files")
    
    for filepath in page_files:
        filename = filepath.name
        print(f"\nProcessing: {filename}")
        
        try:
            updated_content = fix_imports(filepath)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            print(f"  ✓ Fixed imports")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\n" + "="*50)
    print("Import fix complete!")

if __name__ == "__main__":
    main()
