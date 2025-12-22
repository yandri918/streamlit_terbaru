
import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Import config directly
sys.path.append(os.path.join(os.getcwd(), 'agrisensa_streamlit'))
from utils.bapanas_constants import API_CONFIG

def debug_final_attempts():
    print("🕵️ FINAL ATTEMPTS: DATE FORMAT & LOCATION")
    print("========================================")
    
    base_url = API_CONFIG["BASE_URL"]
    headers = API_CONFIG["HEADERS"]
    url = f"{base_url}/harga-pangan-grafik"
    
    start_dt = datetime.now() - timedelta(days=30)
    end_dt = datetime.now()
    
    # Formats
    fmt_dash_rev = "%d-%m-%Y" # 31-01-2024
    fmt_slash = "%Y/%m/%d"
    
    scenarios = [
        {
            "name": "Date: DD-MM-YYYY (Indo Standard)",
            "params": {
                "level_harga_id": 1, 
                "provinsi_id": 15, 
                "komoditas_id": 2,
                "tanggal_awal": start_dt.strftime(fmt_dash_rev),
                "tanggal_akhir": end_dt.strftime(fmt_dash_rev)
            }
        },
        {
            "name": "Location: National (provinsi_id=0)",
            "params": {
                "level_harga_id": 1, 
                "provinsi_id": 0,  # Try 0
                "komoditas_id": 2,
                "tanggal_awal": start_dt.strftime("%Y-%m-%d"), # Back to ISO
                "tanggal_akhir": end_dt.strftime("%Y-%m-%d")
            }
        },
         {
            "name": "Location: Jakarta (provinsi_id=11)",
            "params": {
                "level_harga_id": 1, 
                "provinsi_id": 11, 
                "komoditas_id": 2,
                "tanggal_awal": start_dt.strftime("%Y-%m-%d"),
                "tanggal_akhir": end_dt.strftime("%Y-%m-%d")
            }
        },
        {
             "name": "Key: komoditas vs komoditas_id",
             "params": {
                "level_harga_id": 1, 
                "provinsi_id": 15, 
                "komoditas": 2, # Changed key
                "tanggal_awal": start_dt.strftime("%Y-%m-%d"),
                "tanggal_akhir": end_dt.strftime("%Y-%m-%d")
             }
        }
    ]
    
    for sc in scenarios:
        print(f"\n👉 Testing: {sc['name']}")
        try:
            r = requests.get(url, headers=headers, params=sc['params'], timeout=5)
            print(f"   Status: {r.status_code}")
            if r.status_code == 200:
                data = r.json()
                if "data" in data and isinstance(data['data'], dict):
                    points = data['data'].get('hargaratarata', [])
                    print(f"   Points Count: {len(points)}")
                    if len(points) > 0:
                        print("   ✅ DATA FOUND:", points[:1])
                        return
                    
                    # ALSO CHECK FOR ERROR MESSAGES IN DATA
                    if not points:
                        print("   Config returned:", str(data['data'].get('setting_harga', []))[:100])
                        
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    debug_final_attempts()
