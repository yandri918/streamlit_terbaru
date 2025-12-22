
import sys
import os

# Add the project root to the python path
sys.path.append(os.getcwd())

try:
    from app.data.pest_disease_db import PestDiseaseDatabase
    print("Successfully imported PestDiseaseDatabase")
    
    print("Calling get_pest_list()...")
    pest_list = PestDiseaseDatabase.get_pest_list()
    print(f"Success! Retrieved {len(pest_list)} items.")
    for p in pest_list[:3]:
        print(p)
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
