"""
Script to remove authentication requirements from all modules except ecommerce
"""
import os
import re

# Directories to process
DIRECTORIES = [
    r'c:\Users\yandr\OneDrive\Desktop\agrisensa-api\agrisensa_tech',
    r'c:\Users\yandr\OneDrive\Desktop\agrisensa-api\agrisensa_eco',
    r'c:\Users\yandr\OneDrive\Desktop\agrisensa-api\agrisensa_commodities',
    r'c:\Users\yandr\OneDrive\Desktop\agrisensa-api\agrisensa_livestock'
]

def remove_auth_from_file(filepath):
    """Remove auth requirements from a Python file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Comment out the import line
        content = re.sub(
            r'^from utils\.auth import require_auth, show_user_info_sidebar$',
            r'# from utils.auth import require_auth, show_user_info_sidebar',
            content,
            flags=re.MULTILINE
        )
        
        # Comment out require_auth() call
        content = re.sub(
            r'^user = require_auth\(\)$',
            r'# user = require_auth()',
            content,
            flags=re.MULTILINE
        )
        
        # Comment out show_user_info_sidebar() call
        content = re.sub(
            r'^show_user_info_sidebar\(\)$',
            r'# show_user_info_sidebar()',
            content,
            flags=re.MULTILINE
        )
        
        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"[OK] Modified: {filepath}")
            return True
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def process_directory(directory):
    """Process all Python files in a directory"""
    files_modified = 0
    
    # Process Home.py
    home_file = os.path.join(directory, 'Home.py')
    if os.path.exists(home_file):
        if remove_auth_from_file(home_file):
            files_modified += 1
    
    # Process all files in pages directory
    pages_dir = os.path.join(directory, 'pages')
    if os.path.exists(pages_dir):
        for filename in os.listdir(pages_dir):
            if filename.endswith('.py'):
                filepath = os.path.join(pages_dir, filename)
                if remove_auth_from_file(filepath):
                    files_modified += 1
    
    return files_modified

if __name__ == '__main__':
    print("=" * 60)
    print("Removing Authentication Requirements")
    print("=" * 60)
    
    total_modified = 0
    
    for directory in DIRECTORIES:
        if os.path.exists(directory):
            print(f"\nProcessing: {os.path.basename(directory)}")
            print("-" * 60)
            modified = process_directory(directory)
            total_modified += modified
            print(f"Files modified: {modified}")
    
    print("\n" + "=" * 60)
    print(f"Total files modified: {total_modified}")
    print("=" * 60)
