import requests
import json

BASE_URL = "http://localhost:5000"

commodities = [
    "cabai_merah_keriting", "cabai_rawit_merah", "bawang_merah", "bawang_putih",
    "tomat", "kentang", "wortel", "kubis",
    "beras_premium", "beras_medium", "gula_pasir", "minyak_goreng_kemasan",
    "daging_ayam", "telur_ayam", "daging_sapi",
    "jagung_pipilan", "kedelai", "kacang_tanah", "ubi_kayu"
]

def test_get_prices():
    print("Testing /get-prices endpoint for all commodities...")
    all_passed = True
    
    for commodity in commodities:
        try:
            response = requests.post(
                f"{BASE_URL}/get-prices",
                json={"commodity": commodity},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    print(f"✅ {commodity}: OK ({data['data']['name']} - {data['data']['unit']})")
                else:
                    print(f"❌ {commodity}: Failed (API Error: {data.get('error')})")
                    all_passed = False
            else:
                print(f"❌ {commodity}: Failed (Status Code: {response.status_code})")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {commodity}: Error ({str(e)})")
            all_passed = False
            
    if all_passed:
        print("\n🎉 All commodities verified successfully!")
    else:
        print("\n⚠️ Some commodities failed verification.")

if __name__ == "__main__":
    test_get_prices()
