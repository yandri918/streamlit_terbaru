import os
import re

def clean_filename(filename):
    # Remove emojis (non-ascii characters)
    clean = re.sub(r'[^\x00-\x7F]+', '', filename)
    # Remove double underscores resulting from emoji removal
    clean = clean.replace('__', '_')
    # Remove leading underscore if present (e.g. _RAB.py)
    if clean.startswith('_'):
        clean = clean[1:]
    return clean

folder = 'pages'
files = [f for f in os.listdir(folder) if f.endswith('.py')]
files.sort()

print("Renaming Plan:")
for filename in files:
    new_name = clean_filename(filename)
    if new_name != filename:
        print(f"{filename} -> {new_name}")
        old_path = os.path.join(folder, filename)
        new_path = os.path.join(folder, new_name)
        try:
            os.rename(old_path, new_path)
        except OSError as e:
            print(f"Error renaming {filename}: {e}")
