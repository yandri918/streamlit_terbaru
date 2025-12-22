
import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Import config directly
sys.path.append(os.path.join(os.getcwd(), 'agrisensa_streamlit'))
from utils.bapanas_constants import API_CONFIG

def debug_endpoint_content_check():
    print("🕵️ DEBUGGING BAPANAS CONTENT CHECK")
    print("==================================")
    
    base_url = API_CONFIG["BASE_URL"]
    headers = API_CONFIG["HEADERS"]
    url = f"{base_url}/harga-pangan-grafik"
    
    # Variation 2: Testing Indonesian Keys (SUCCESS CANDIDATE)
    print("\n[2] Testing Indonesian Keys...")
    params2 = {
        "level_harga_id": 1, 
        "provinsi_id": 15, 
        "komoditas_id": 2,
        "tanggal_awal": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        "tanggal_akhir": datetime.now().strftime("%Y-%m-%d")
    }
    try:
        r = requests.get(url, headers=headers, params=params2, timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            try:
                data = r.json()
                print("Response Keys:", data.keys())
                if "data" in data and len(data["data"]) > 0:
                    print("First Data Point:", data["data"][0])
                else:
                    print("Full Response:", str(data)[:500])
            except:
                print("Response Text (Not JSON):", r.text[:500])
    except Exception as e: print(e)

if __name__ == "__main__":
    debug_endpoint_content_check()
