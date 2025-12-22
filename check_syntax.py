import os
import sys

# Add current directory to path
sys.path.append(os.getcwd())

try:
    print("Attempting to import create_app...")
    from app import create_app
    print("Import successful.")
    
    print("Attempting to create app instance...")
    app = create_app('development')
    print("App creation successful.")
    
except Exception as e:
    print(f"❌ CRITICAL ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
