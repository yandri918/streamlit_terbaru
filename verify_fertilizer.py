import sys
import os
import json
from app.services.recommendation_service import RecommendationService

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def verify_fertilizer_enhancement():
    print("Testing Fertilizer Calculator Enhancement...")
    
    # Test Cases
    test_cases = [
        {"commodity": "cabai", "area": 1000, "ph": 6.5},
        {"commodity": "tomat", "area": 2000, "ph": 5.5}, # Acidic soil test
        {"commodity": "melon", "area": 500, "ph": 7.0}
    ]
    
    all_passed = True
    
    for case in test_cases:
        print(f"\nTesting {case['commodity']} (Area: {case['area']}m2, pH: {case['ph']})...")
        try:
            result = RecommendationService.calculate_fertilizer_dosage(
                commodity=case['commodity'],
                area_sqm=case['area'],
                ph_tanah=case['ph']
            )
            
            if not result:
                print(f"❌ Failed: No result returned for {case['commodity']}")
                all_passed = False
                continue
                
            # Check for schedule
            if "schedule" in result and result["schedule"]:
                print(f"✅ Schedule found with {len(result['schedule'])} stages.")
                for stage, details in result["schedule"].items():
                    print(f"   - {stage}: {details['fertilizers']}")
            else:
                print("❌ Failed: No schedule found in result.")
                all_passed = False
                
            # Check for totals
            if "anorganik" in result and result["anorganik"]:
                print(f"✅ Totals calculated: {result['anorganik']}")
            else:
                print("❌ Failed: No totals found.")
                all_passed = False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            all_passed = False
            
    if all_passed:
        print("\n🎉 All Fertilizer Enhancement Tests Passed!")
        return True
    else:
        print("\n❌ Some tests failed.")
        return False

if __name__ == "__main__":
    verify_fertilizer_enhancement()
