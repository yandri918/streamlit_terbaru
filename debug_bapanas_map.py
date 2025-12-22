
import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Import config directly
sys.path.append(os.path.join(os.getcwd(), 'agrisensa_streamlit'))
from utils.bapanas_constants import API_CONFIG

def debug_new_endpoint():
    print("🕵️ DEBUGGING HARGA-PETA-PROVINSI")
    print("================================")
    
    base_url = API_CONFIG["BASE_URL"]
    headers = API_CONFIG["HEADERS"]
    url = f"{base_url}/harga-peta-provinsi"
    
    # 1. Replicate User's Request Exactly (but with known Commodity ID 2 for Rice if 109 is obscure)
    # Actually, 109 might be valid. Let's try ID 2 (Beras Premium) first as we know it exists.
    # And ID 1 (Retail Price).
    
    # Date format: 10/12/2025 - 10/12/2025 (URL decoded)
    # Using current date for safety
    today = datetime.now()
    # today_str = today.strftime("%d/%m/%Y")
    # For testing, let's use a known recent range to ensure data
    today_str = datetime.now().strftime("%d/%m/%Y")
    
    period = f"{today_str} - {today_str}"
    
    params = {
        "level_harga_id": 1, # Retail
        "komoditas_id": 2, # Beras Premium
        "period_date": period,
        "multi_status_map[0]": "",
        "multi_province_id[0]": ""
    }
    
    print("\n[1] Testing with Known Commodity (ID 2)...")
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            if "data" in data and isinstance(data['data'], list) and len(data['data']) > 0:
                print(f"✅ SUCCESS! Found {len(data['data'])} records.")
                print("Sample:", str(data['data'][0])[:200])
            else:
                 print("Response Keys:", data.keys())
                 print("Data field:", str(data.get('data'))[:500])
        else:
             print("text:", r.text[:200])
    except Exception as e: print(e)
    
    # 2. Try User's Exact Params (ID 109 - Cabai Rawit Merah??)
    # 10/12/2025 is future... user might mean 10/12/2024? Or server time is weird?
    # User's log says "Wed, 10 Dec 2025". Wait. The user's metadata says "2025".
    # Ok, I will trust the system time.
    
    print("\n[2] Testing User's Exact Params (ID 109)...")
    date_future = "10/12/2025 - 10/12/2025" # Explicitly testing the user's dates
    params_user = {
        "level_harga_id": 3, # User used 3
        "komoditas_id": 109,
        "period_date": date_future,
        "multi_status_map[0]": "",
        "multi_province_id[0]": ""
    }
    try:
        r = requests.get(url, headers=headers, params=params_user, timeout=10)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
             data = r.json()
             if "data" in data and len(data['data']) > 0:
                print(f"✅ SUCCESS! Found {len(data['data'])} records.")
                print("Sample:", str(data['data'][0])[:200])
             else:
                print("Data Empty:", str(data.get('data')))
    except Exception as e: print(e)

if __name__ == "__main__":
    debug_new_endpoint()
