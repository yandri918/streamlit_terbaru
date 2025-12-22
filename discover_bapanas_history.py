
import requests
import json
import sys
import os
from datetime import datetime, timedelta

# Import config directly
sys.path.append(os.path.join(os.getcwd(), 'agrisensa_streamlit'))
from utils.bapanas_constants import API_CONFIG, PROVINCE_MAPPING, COMMODITY_MAPPING

def test_historical_endpoints():
    print("🚀 BAPANAS V2 HISTORICAL DISCOVERY")
    print("==================================")
    
    base_url = API_CONFIG["BASE_URL"]
    headers = API_CONFIG["HEADERS"]
    
    # Common endpoint patterns for Bapanas V2 (reverse engineered)
    potential_endpoints = [
        "harga-pangan-grafik",
        "harga-grafik",
        "grafik-harga",
        "harga-pangan-gabungan",
        "transaksi/harga-pangan-grafik" # Sometimes hidden in sub-paths
    ]
    
    # Test Parameters (Standard commodity & location)
    # Beras Premium (2), Jatim (15)
    params = {
        "level_harga_id": 1,
        "province_id": 15,
        "commodity_id": 2, # Beras Premium
        "k_id": 2, # Sometimes used as commodity id key
        "komoditas_id": 2,
        "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        "end_date": datetime.now().strftime("%Y-%m-%d")
    }
    
    for ep in potential_endpoints:
        url = f"{base_url}/{ep}"
        print(f"\n🔍 Testing: {url}")
        
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=5)
            print(f"   Status: {resp.status_code}")
            
            if resp.status_code == 200:
                data = resp.json()
                # Check if it looks like a list of points
                if isinstance(data, dict):
                    keys = list(data.keys())
                    print(f"   Keys: {keys}")
                    if "data" in data and len(data["data"]) > 0:
                        print("   ✅ SUCCESS! Data found.")
                        print("   Sample:", str(data["data"])[:200])
                        return ep # Found it
                elif isinstance(data, list) and len(data) > 0:
                     print("   ✅ SUCCESS! List found.")
                     return ep
            else:
                print("   ❌ Invalid Response")
                
        except Exception as e:
            print(f"   ⚠️ Error: {e}")

    return None

if __name__ == "__main__":
    found_ep = test_historical_endpoints()
    if found_ep:
        print(f"\n🎉 WINNER: Endpoint '{found_ep}' is valid!")
    else:
        print("\n😔 No standard historical endpoint guessed. Might need deeper sniffing.")
