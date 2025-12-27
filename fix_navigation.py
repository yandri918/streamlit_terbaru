# -*- coding: utf-8 -*-
# Script to fix Streamlit navigation issues by removing emoji from filenames
import os
import sys
from pathlib import Path
import re

# Force UTF-8 output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def remove_emoji_from_filename(filename):
    """Remove emoji and special characters from filename, keep only ASCII"""
    clean_name = re.sub(r'[^\x00-\x7F]+', '_', filename)
    clean_name = re.sub(r'_+', '_', clean_name)
    clean_name = re.sub(r'_+\.', '.', clean_name)
    return clean_name

def fix_pages_directory(pages_dir):
    """Rename all files in pages directory to ASCII-safe names"""
    pages_path = Path(pages_dir)
    
    if not pages_path.exists():
        return []
    
    renamed_files = []
    
    for file_path in pages_path.glob("*.py"):
        old_name = file_path.name
        new_name = remove_emoji_from_filename(old_name)
        
        if old_name != new_name:
            new_path = file_path.parent / new_name
            
            if new_path.exists():
                continue
            
            try:
                file_path.rename(new_path)
                renamed_files.append((old_name, new_name))
            except Exception:
                pass
    
    return renamed_files

if __name__ == "__main__":
    modules = [
        "agrisensa_tech/pages",
        "agrisensa_eco/pages",
        "agrisensa_biz/pages",
        "agrisensa_commodities/pages",
        "agrisensa_livestock/pages"
    ]
    
    print("Fixing Streamlit Navigation...")
    
    all_renamed = []
    
    for module in modules:
        renamed = fix_pages_directory(module)
        if renamed:
            print(f"Module: {module} - {len(renamed)} files renamed")
            all_renamed.extend(renamed)
    
    print(f"\nTotal: {len(all_renamed)} files renamed")
    
    if all_renamed:
        print("\nNOTE: Update navigation links in Home.py files!")
