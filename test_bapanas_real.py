
import requests
import json
import sys
import os

# Add parent dir to path to import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agrisensa_streamlit.utils.bapanas_constants import API_CONFIG

def test_connection():
    url = f"{API_CONFIG['BASE_URL']}/harga-pangan-informasi"
    
    print(f"Testing connection to: {url}")
    print("Using headers:", json.dumps(API_CONFIG['HEADERS'], indent=2))
    
    params = {
        "level_harga_id": 1
        # Intentionally leaving province empty to get national or default
    }
    
    try:
        response = requests.get(
            url, 
            headers=API_CONFIG['HEADERS'], 
            params=params,
            timeout=10
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ SUCCESS! Data received.")
            print("\nSample Response Structure:")
            print(json.dumps(data, indent=2)[:1000]) # Print first 1000 chars
            
            # Additional analysis of structure
            if 'data' in data:
                print(f"\nNumber of records: {len(data['data'])}")
                if len(data['data']) > 0:
                    print("First record keys:", data['data'][0].keys())
        else:
            print("\n❌ FAILED to get 200 OK")
            print(response.text[:500])
            
    except Exception as e:
        print(f"\n❌ EXCEPTION: {e}")

if __name__ == "__main__":
    test_connection()
