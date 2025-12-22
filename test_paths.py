
import os

# Simulate legacy.py location
# c:\Users\yandr\OneDrive\Desktop\agrisensa-api\app\routes\legacy.py
# We are running this script from root, so we need to simulate the depth

ROOT_DIR = os.getcwd()
print(f"ROOT_DIR: {ROOT_DIR}")

# Logic used in legacy.py
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Since we can't easily simulate __file__ of a different location, we'll just verify the construction from root

UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'uploads', 'pdfs')
PDF_FILE = os.path.join(UPLOAD_FOLDER, 'ASAT_CF_id-compressed.pdf')

print(f"UPLOAD_FOLDER: {UPLOAD_FOLDER}")
print(f"PDF_FILE: {PDF_FILE}")
print(f"Exists: {os.path.exists(PDF_FILE)}")
