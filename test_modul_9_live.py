import requests
import json

url = "http://localhost:5000/get-integrated-recommendation"
payload = {
    "ketinggian": "dataran_rendah",
    "iklim": "tropis",
    "fase": "vegetatif",
    "masalah": "thrips"
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print("Response JSON keys:", data.keys())
        if 'data' in data:
            print("Data keys:", data['data'].keys())
            print("Bibit type:", type(data['data'].get('bibit')))
            print("Bibit content:", data['data'].get('bibit'))
            
            if isinstance(data['data'].get('bibit'), dict):
                print("BACKEND IS NEW (UPDATED)")
            else:
                print("BACKEND IS OLD (NOT UPDATED)")
        else:
            print("No data key found")
    else:
        print("Error response:", response.text)
except Exception as e:
    print(f"Connection failed: {e}")
