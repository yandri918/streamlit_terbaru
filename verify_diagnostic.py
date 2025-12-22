import sys
import os
from flask import Flask

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from app.data.pest_disease_db import PestDiseaseDatabase

def verify_diagnostic_logic():
    print("Testing Diagnostic Logic...")
    
    # 1. Test Tree Structure
    try:
        tree = PestDiseaseDatabase.get_diagnostic_tree()
        print("✅ get_diagnostic_tree() returned data.")
        
        # Check basic structure
        if "Daun" in tree and "Batang" in tree:
            print("✅ Tree has top-level keys (Daun, Batang).")
        else:
            print("❌ Tree missing top-level keys.")
            return False
            
        # Check depth (Daun -> Berlubang -> Detail -> Result)
        symptom = tree["Daun"].get("Berlubang / Rusak Fisik")
        if symptom:
            print("✅ Tree has Level 2 (Symptoms).")
            detail = list(symptom.values())[0]
            if isinstance(detail, str):
                print(f"✅ Tree leaf node is a string (Pest ID): {detail}")
            else:
                print("❌ Tree leaf node is not a string.")
                return False
        else:
            print("❌ Tree missing specific symptom key.")
            return False
            
    except Exception as e:
        print(f"❌ Error getting tree: {e}")
        return False

    # 2. Test Result Retrieval
    try:
        pest_id = "ulat_grayak"
        detail = PestDiseaseDatabase.get_pest_detail(pest_id)
        if detail and detail['name']:
            print(f"✅ get_pest_detail('{pest_id}') returned: {detail['name']}")
        else:
            print(f"❌ get_pest_detail('{pest_id}') returned None or empty.")
            return False
    except Exception as e:
        print(f"❌ Error getting detail: {e}")
        return False
        
    print("\n🎉 All Diagnostic Logic Tests Passed!")
    return True

if __name__ == "__main__":
    verify_diagnostic_logic()
