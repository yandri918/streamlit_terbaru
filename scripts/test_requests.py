import requests, json

base = 'http://127.0.0.1:5000'

def p(label, resp):
    try:
        print(label, resp.status_code, resp.json())
    except Exception:
        print(label, resp.status_code, resp.text[:500])

# 1) Health
try:
    r = requests.get(base + '/health', timeout=5)
    p('HEALTH', r)
except Exception as e:
    print('HEALTH ERROR', e)

# 2) Recommendation fertilizer
try:
    payload = {"ph_tanah":6.5, "skor_bwd":1, "kelembaban_tanah":60, "umur_tanaman_hari":30}
    r = requests.post(base + '/api/recommendation/fertilizer', json=payload, timeout=8)
    p('RECO FERT', r)
except Exception as e:
    print('RECO FERT ERROR', e)

# 3) Spraying (modul 10)
try:
    r = requests.post(base + '/api/recommendation/spraying', json={"pest":"thrips"}, timeout=8)
    p('SPRAYING', r)
except Exception as e:
    print('SPRAYING ERROR', e)

# 4) Legacy spraying (modul 10)
try:
    r = requests.post(base + '/api/legacy/get-spraying-recommendation', json={"pest":"thrips"}, timeout=8)
    p('LEGACY SPRAYING', r)
except Exception as e:
    print('LEGACY SPRAYING ERROR', e)

# 5) Analysis BWD (modul 1) - kirim gambar hijau dummy
try:
    import numpy as np, cv2, tempfile
    img = (np.zeros((100,100,3), dtype=np.uint8))
    img[:]= (0,255,0)
    tmp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    cv2.imwrite(tmp.name, img)
    with open(tmp.name, 'rb') as f:
        files = {'file': ('leaf.png', f, 'image/png')}
        r = requests.post(base + '/api/analysis/bwd', files=files, timeout=8)
        p('ANALYZE BWD', r)
except Exception as e:
    print('ANALYZE BWD ERROR', e)


