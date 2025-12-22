
import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Import config directly
sys.path.append(os.path.join(os.getcwd(), 'agrisensa_streamlit'))
from utils.bapanas_constants import API_CONFIG

def debug_map_price_field_level3():
    print("🕵️ DEBUGGING LEVEL 3 PRICE")
    
    base_url = API_CONFIG["BASE_URL"]
    headers = API_CONFIG["HEADERS"]
    url = f"{base_url}/harga-peta-provinsi"
    
    today_str = datetime.now().strftime("%d/%m/%Y")
    period = f"{today_str} - {today_str}"
    
    params = {
        "level_harga_id": 3, # Checking if 3 is Retail?
        "komoditas_id": 2, # Beras Premium
        "period_date": period,
        "multi_status_map[0]": "",
        "multi_province_id[0]": ""
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if "data" in data and len(data['data']) > 0:
                item = data['data'][0]
                print(f"Province: {item.get('province_name')}")
                print(f"Price (Geometrik): {item.get('rata_rata_geometrik')}")
                print(f"Level: {item.get('level_harga')}")
            else:
                 print("Empty data")
        else:
             print("Status:", r.status_code)
    except Exception as e: print(e)

if __name__ == "__main__":
    debug_map_price_field_level3()
