"""
Script untuk clear cache Streamlit dan restart module 12
"""
import os
import shutil
import subprocess
import sys

# Get the agrisensa-api directory
base_dir = r"c:\Users\yandr\OneDrive\Desktop\agrisensa-api"
os.chdir(base_dir)

# Clear Streamlit cache
cache_dir = os.path.join(os.path.expanduser("~"), ".streamlit", "cache")
if os.path.exists(cache_dir):
    print(f"🗑️ Clearing Streamlit cache: {cache_dir}")
    try:
        shutil.rmtree(cache_dir)
        print("✅ Cache cleared!")
    except Exception as e:
        print(f"⚠️ Could not clear cache: {e}")

# Clear __pycache__
pycache_dirs = []
for root, dirs, files in os.walk("agrisensa_streamlit"):
    if "__pycache__" in dirs:
        pycache_dir = os.path.join(root, "__pycache__")
        pycache_dirs.append(pycache_dir)

for pycache in pycache_dirs:
    print(f"🗑️ Removing {pycache}")
    try:
        shutil.rmtree(pycache)
    except Exception as e:
        print(f"⚠️ Could not remove: {e}")

print("\n✅ Cache cleared! Now you can run:")
print("   streamlit run agrisensa_streamlit/Home.py")
print("\nOr directly test Module 12:")
print('   streamlit run "agrisensa_streamlit/pages/12_🔬_Asisten_Penelitian.py"')
