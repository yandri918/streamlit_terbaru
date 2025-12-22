import requests
import json

keys = [
    "IodjgVq4blMDdQzuHRSrioXmhLk5flLk", # Key 1
    "AsFwMfmMBh5XFdWl2lXYfVor9IEshzuB"  # Key 2
]

endpoints = [
    "/komoditas",
    "/commodities",
    "/harga",
    "/prices",
    "/latest",
    "/daily",
    "/market",
    "/list",
    "/get-prices",
    "/api/komoditas",
    "/api/prices",
    "/v1/prices",
    "/v1/komoditas",
    "/food-price",
    "/pangan"
]

# Base URLs to try
base_urls = [
    "https://BigView.api.apilogy.id/harga-pangan/1.0.0",
    "https://BigView.api.apilogy.id/harga-pangan",
    "https://BigView.api.apilogy.id",
    "https://api.apilogy.id/harga-pangan"
]

for key in keys:
    print(f"\n--- Testing Key: {key[:5]}... ---")
    headers = {
        "apikey": key,
        "Accept": "application/json"
    }
    
    for base in base_urls:
        for ep in endpoints:
            if ep.startswith("/") and base.endswith("/"):
                full_url = f"{base}{ep[1:]}"
            elif not ep.startswith("/") and not base.endswith("/"):
                full_url = f"{base}/{ep}"
            else:
                full_url = f"{base}{ep}"
                
            # print(f"Testing: {full_url}") # Reduce noise
            try:
                response = requests.get(full_url, headers=headers, verify=False, timeout=3)
                if response.status_code != 404:
                    print(f"\n[FOUND!] URL: {full_url}")
                    print(f"Status: {response.status_code}")
                    print(response.text[:500])
                    if response.status_code == 200:
                        exit() # Stop completely if success
            except Exception as e:
                pass # Ignore connection errors for invalid domains
