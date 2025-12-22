"""Test script for fertilizer recommendation endpoint."""
import requests
import json

# Simulate the frontend request
test_data = {
    "ph": 5,
    "area_sqm": 233,
    "commodity": "jagung"
}

url = 'http://localhost:5000/recommendation'
headers = {'Content-Type': 'application/json'}

print(f"Testing fertilizer recommendation endpoint: {url}")
print(f"Input data: {json.dumps(test_data, indent=2)}")

try:
    response = requests.post(url, headers=headers, json=test_data)
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        print("Response JSON:")
        print(json.dumps(response.json(), indent=2))
    else:
        print(f"Error Response: {response.text}")
        
except Exception as e:
    print(f"\nError executing request: {e}")
    print("Make sure the server is running on http://localhost:5000")
