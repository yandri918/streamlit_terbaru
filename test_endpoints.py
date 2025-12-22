"""
Script untuk test semua endpoint legacy
"""
import requests
import json

BASE_URL = "http://localhost:5000"

def test_endpoint(method, endpoint, data=None, files=None):
    """Test satu endpoint."""
    try:
        if method == 'GET':
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
        elif method == 'POST':
            if files:
                response = requests.post(f"{BASE_URL}{endpoint}", files=files, timeout=5)
            elif data:
                response = requests.post(f"{BASE_URL}{endpoint}", json=data, timeout=5)
            else:
                response = requests.post(f"{BASE_URL}{endpoint}", timeout=5)
        else:
            return False, "Unknown method"
        
        # Accept both 200 and 201 as success
        if response.status_code in [200, 201]:
            try:
                result = response.json()
                # Check if response has success field
                if isinstance(result, dict) and result.get('success'):
                    return True, result
                elif isinstance(result, dict):
                    return True, result
                return True, result
            except:
                return True, response.text
        else:
            return False, f"Status {response.status_code}: {response.text}"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.ConnectionError:
        return False, "Connection Error - Server mungkin tidak berjalan"
    except Exception as e:
        return False, str(e)

def main():
    """Test semua endpoint."""
    print("=" * 60)
    print("TEST SEMUA ENDPOINT LEGACY")
    print("=" * 60)
    
    endpoints = [
        ("GET", "/get-ticker-prices", None),
        ("GET", "/get-ph-info", None),
        ("GET", "/get-diagnostic-tree", None),
        ("GET", "/get-pdfs", None),
        ("POST", "/get-prices", {"commodity": "cabai_merah_keriting"}),
        ("POST", "/get-knowledge", {"commodity": "cabai"}),
        ("POST", "/analyze-npk", {"n_value": 50, "p_value": 30, "k_value": 40}),
    ]
    
    results = []
    for method, endpoint, data in endpoints:
        print(f"\n🔍 Testing {method} {endpoint}...")
        success, result = test_endpoint(method, endpoint, data)
        if success:
            print(f"   ✅ SUCCESS")
            if isinstance(result, dict) and 'success' in result:
                print(f"   Response success: {result.get('success')}")
        else:
            print(f"   ❌ FAILED: {result}")
        results.append((endpoint, success, result))
    
    print("\n" + "=" * 60)
    print("RINGKASAN:")
    success_count = sum(1 for _, success, _ in results if success)
    print(f"✅ Berhasil: {success_count}/{len(results)}")
    print(f"❌ Gagal: {len(results) - success_count}/{len(results)}")
    print("=" * 60)

if __name__ == '__main__':
    main()

