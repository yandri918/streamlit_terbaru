
import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Import config directly
sys.path.append(os.path.join(os.getcwd(), 'agrisensa_streamlit'))
from utils.bapanas_constants import API_CONFIG

def debug_params_permutation():
    print("🕵️ PARAMETER PERMUTATION TEST")
    print("===========================")
    
    base_url = API_CONFIG["BASE_URL"]
    headers = API_CONFIG["HEADERS"]
    url = f"{base_url}/harga-pangan-grafik"
    
    start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = datetime.now().strftime("%Y-%m-%d")
    
    scenarios = [
        {
            "name": "Standard Mix (Indo Keys)",
            "params": {
                "level_harga_id": 1, 
                "provinsi_id": 15, 
                "komoditas_id": 2,
                "tanggal_awal": start_date,
                "tanggal_akhir": end_date
            }
        },
        {
            "name": "English Keys only",
            "params": {
                "level_harga_id": 1, 
                "province_id": 15, 
                "commodity_id": 2,
                "start_date": start_date,
                "end_date": end_date
            }
        },
        {
            "name": "Mixed (province_id + komoditas_id)",
            "params": {
                "level_harga_id": 1, 
                "province_id": 15, 
                "komoditas_id": 2,
                "tanggal_awal": start_date,
                "tanggal_akhir": end_date
            }
        },
        {
             "name": "Use 'type' param mentioned in response",
             "params": {
                "level_harga_id": 1, 
                "provinsi_id": 15, 
                "komoditas_id": 2,
                "type": 1, # Guessing
                "tanggal_awal": start_date,
                "tanggal_akhir": end_date
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
                        return # Stop if found
                elif isinstance(data, list):
                     print(f"   List returned: len={len(data)}")
        except Exception as e:
            print(f"   Error: {e}")

if __name__ == "__main__":
    debug_params_permutation()
