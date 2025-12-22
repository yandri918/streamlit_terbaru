
import requests
import json
import time

def check_endpoint(name, url, method="GET", params=None, headers=None):
    print(f"\n🔍 Checking {name}...")
    print(f"   URL: {url}")
    
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    if headers:
        default_headers.update(headers)
        
    try:
        start_time = time.time()
        if method == "GET":
            response = requests.get(url, params=params, headers=default_headers, timeout=10)
        else:
            response = requests.post(url, json=params, headers=default_headers, timeout=10)
            
        elapsed = time.time() - start_time
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Time: {elapsed:.2f}s")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("   ✅ SUCCESS: JSON Response received")
                # Print sample structure
                str_data = json.dumps(data, indent=2)
                print(f"   Sample Data: {str_data[:200]}...")
                return True
            except json.JSONDecodeError:
                print("   ⚠️  WARNING: Response is not JSON (Likely HTML)")
                return False
        else:
            print("   ❌ FAILED: Non-200 status code")
            return False
            
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)}")
        return False

# --- LIST OF KNOWN INDONESIAN PRICE ENDPOINTS (HIDDEN APIs) ---

print("="*50)
print("🕵️  AGRISENSA AGRI-PRICE API CHECKER")
print("="*50)
print("Mencoba melakukan ping ke berbagai sumber data pemerintah...")

# 1. PIHPS Nasional (Bank Indonesia) - Known Mobile API endpoint
check_endpoint(
    "PIHPS Nasional (Mobile API)",
    "https://hargapangan.id/api/v1/price/latest/1",  # 1 indicates a commodity ID usually
    headers={"Accept": "application/json"}
)

# 2. Bapanas (Badan Pangan Nasional) - Panel Harga
check_endpoint(
    "Badan Pangan Nasional (Panel Harga)",
    "https://panelharga.badanpangan.go.id/data/kabkota-bulanan",
    headers={"X-Requested-With": "XMLHttpRequest"}
)

# 3. Siskaperbapo (Jawa Timur) - Very reliable local data
check_endpoint(
    "Siskaperbapo (Jawa Timur)",
    "https://siskaperbapo.jatimprov.go.id/harga/tabel.json",
    headers={
        "Referer": "https://siskaperbapo.jatimprov.go.id/harga/tabel",
        "X-Requested-With": "XMLHttpRequest"
    }
)

# 4. Info Pangan Jakarta
check_endpoint(
    "Info Pangan Jakarta",
    "https://infopangan.jakarta.go.id/api/price/series_by_location",
    headers={"api-key": "guest"}  # Sometimes required
)

print("\n" + "="*50)
print("💡 TIPS FOR USER:")
print("1. Jika salah satu di atas SUKSES (✅), gunakan URL tersebut di aplikasi.")
print("2. Jika gagal, website tersebut mungkin menggunakan proteksi (Cloudflare/WAF).")
print("3. Gunakan teknik 'Inspect Element > Network' di browser untuk update URL.")
print("="*50)
