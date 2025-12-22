# 📂 Cara Mengakses Database AgriMap

## 🗄️ Lokasi File Database

Database AgriMap menggunakan **JSON files** yang tersimpan di folder `instance/`:

```
instance/
├── agrimap_polygons.json      # Data polygon lahan
├── agrimap_npk_data.json       # Data NPK tanah
└── agrimap_markers.json        # Marker di peta
```

---

## 📖 Cara Akses Database

### 1️⃣ **Melalui Python Code**

#### Import Database Class
```python
from app.data.agrimap_db import AgriMapDatabase

# Inisialisasi database
db = AgriMapDatabase()
```

#### Membaca Data Polygon
```python
# Get semua polygon
polygons = db.get_polygons()
print(f"Total lahan: {len(polygons)}")

for polygon in polygons:
    print(f"Nama: {polygon['name']}")
    print(f"Luas: {polygon['area_sqm']} m² ({polygon['area_hectares']} ha)")
    print(f"Koordinat: {polygon['coordinates']}")
    print("---")

# Get polygon by ID
polygon = db.get_polygon_by_id('polygon-id-here')
if polygon:
    print(polygon)
```

#### Membaca Data NPK
```python
# Get semua data NPK
npk_data = db.get_npk_data()

for data in npk_data:
    print(f"Lokasi: ({data['latitude']}, {data['longitude']})")
    print(f"N: {data['n_value']}, P: {data['p_value']}, K: {data['k_value']}")
    print(f"Tanggal: {data['created_at']}")
    print("---")

# Get NPK data untuk polygon tertentu
polygon_npk = db.get_npk_data(polygon_id='polygon-id-here')

# Cari NPK terdekat dengan lokasi
nearby_npk = db.get_npk_by_location(
    latitude=-6.2088,
    longitude=106.8456,
    radius_km=5.0
)
```

#### Menyimpan Data Baru
```python
# Simpan polygon baru
new_polygon = db.save_polygon(
    name="Lahan Padi Barat",
    coordinates=[[[106.8, -6.2], [106.81, -6.2], [106.81, -6.21], [106.8, -6.21]]],
    area_sqm=10000,
    ph=6.5,
    notes="Lahan subur"
)
print(f"Polygon tersimpan dengan ID: {new_polygon['id']}")

# Simpan data NPK
new_npk = db.save_npk_data(
    latitude=-6.2088,
    longitude=106.8456,
    n_value=45,
    p_value=30,
    k_value=40,
    notes="Sampling pagi hari"
)
print(f"NPK data tersimpan dengan ID: {new_npk['id']}")
```

---

### 2️⃣ **Melalui API Endpoints**

#### Get All Polygons
```bash
curl http://localhost:5000/api/agrimap/polygons
```

Response:
```json
{
  "success": true,
  "data": [
    {
      "id": "uuid-here",
      "name": "Lahan Padi Utara",
      "area_sqm": 5000,
      "area_hectares": 0.5,
      "coordinates": [...],
      "created_at": "2025-11-30T19:00:00"
    }
  ]
}
```

#### Get All NPK Data
```bash
curl http://localhost:5000/api/agrimap/npk-data
```

#### Get NPK Data by Polygon
```bash
curl "http://localhost:5000/api/agrimap/npk-data?polygon_id=polygon-uuid"
```

#### Get Nearby NPK Data
```bash
curl "http://localhost:5000/api/agrimap/npk-data/nearby?lat=-6.2088&lon=106.8456&radius=5"
```

#### Get Statistics
```bash
curl http://localhost:5000/api/agrimap/statistics
```

Response:
```json
{
  "success": true,
  "data": {
    "total_polygons": 3,
    "total_area_sqm": 15000,
    "total_area_hectares": 1.5,
    "total_npk_samples": 8,
    "total_markers": 5
  }
}
```

---

### 3️⃣ **Langsung Edit File JSON**

Anda bisa langsung membuka dan edit file JSON:

#### Buka File
```bash
# Windows
notepad instance\agrimap_npk_data.json

# Atau dengan VS Code
code instance\agrimap_npk_data.json
```

#### Format Data NPK
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "latitude": -6.2088,
    "longitude": 106.8456,
    "n_value": 45.5,
    "p_value": 30.2,
    "k_value": 40.8,
    "polygon_id": null,
    "notes": "Sampling pagi hari",
    "created_at": "2025-11-30T19:00:00"
  }
]
```

#### Format Data Polygon
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "name": "Lahan Padi Utara",
    "coordinates": [
      [
        [106.8, -6.2],
        [106.81, -6.2],
        [106.81, -6.21],
        [106.8, -6.21],
        [106.8, -6.2]
      ]
    ],
    "area_sqm": 5000,
    "area_hectares": 0.5,
    "soil_type": "lempung",
    "ph": 6.5,
    "notes": "Lahan subur",
    "created_at": "2025-11-30T19:00:00",
    "updated_at": "2025-11-30T19:00:00"
  }
]
```

---

### 4️⃣ **Melalui Python Script**

Buat script untuk query data:

```python
# query_agrimap.py
from app.data.agrimap_db import AgriMapDatabase
import json

db = AgriMapDatabase()

# Get statistics
stats = db.get_statistics()
print("=== STATISTIK AGRIMAP ===")
print(f"Total Lahan: {stats['total_polygons']}")
print(f"Total Area: {stats['total_area_hectares']} hektar")
print(f"Total Sampel NPK: {stats['total_npk_samples']}")
print()

# Show all polygons
print("=== DAFTAR LAHAN ===")
polygons = db.get_polygons()
for p in polygons:
    print(f"{p['name']}: {p['area_hectares']} ha")
print()

# Show all NPK data
print("=== DATA NPK ===")
npk_data = db.get_npk_data()
for npk in npk_data:
    print(f"Lokasi: ({npk['latitude']}, {npk['longitude']})")
    print(f"  N={npk['n_value']}, P={npk['p_value']}, K={npk['k_value']}")
    if npk['notes']:
        print(f"  Catatan: {npk['notes']}")
    print()

# Export to JSON
with open('agrimap_export.json', 'w', encoding='utf-8') as f:
    json.dump({
        'polygons': polygons,
        'npk_data': npk_data,
        'statistics': stats
    }, f, ensure_ascii=False, indent=2)
print("✅ Data exported to agrimap_export.json")
```

Jalankan:
```bash
python query_agrimap.py
```

---

### 5️⃣ **Melalui Service Layer (Recommended)**

Untuk analisis lebih advanced, gunakan service layer:

```python
from app.services.agrimap_service import AgriMapService

service = AgriMapService()

# Analisis NPK
analysis = service.analyze_npk_values(
    n_value=45,
    p_value=30,
    k_value=40
)
print("Analisis NPK:")
print(analysis)

# Rekomendasi tanaman berdasarkan lokasi
suitability = service.get_crop_suitability(
    latitude=-6.2088,
    longitude=106.8456,
    n_value=45,
    p_value=30,
    k_value=40
)
print("\nTanaman yang cocok:")
for crop in suitability['suitable_crops']:
    print(f"- {crop['icon']} {crop['name']}: {crop['suitability']}")

# Generate heatmap data
heatmap = service.generate_npk_heatmap_data()
print(f"\nHeatmap points: {len(heatmap)}")

# Prepare data untuk kalkulator pupuk
fert_data = service.prepare_fertilizer_data('polygon-id-here')
if fert_data['success']:
    print(f"\nData untuk kalkulator pupuk:")
    print(f"Luas: {fert_data['area_sqm']} m²")
    if fert_data['npk_data']:
        print(f"NPK rata-rata: N={fert_data['npk_data']['n']}, "
              f"P={fert_data['npk_data']['p']}, K={fert_data['npk_data']['k']}")
```

---

## 🔧 Operasi Database Lengkap

### Polygon Operations
```python
# CREATE
polygon = db.save_polygon(name, coordinates, area_sqm, ph, notes)

# READ
all_polygons = db.get_polygons()
one_polygon = db.get_polygon_by_id(polygon_id)

# UPDATE
db.update_polygon(polygon_id, {'ph': 7.0, 'notes': 'Updated'})

# DELETE
db.delete_polygon(polygon_id)
```

### NPK Data Operations
```python
# CREATE
npk = db.save_npk_data(lat, lon, n, p, k, polygon_id, notes)

# READ
all_npk = db.get_npk_data()
polygon_npk = db.get_npk_data(polygon_id=polygon_id)
nearby_npk = db.get_npk_by_location(lat, lon, radius_km)

# DELETE
db.delete_npk_data(npk_id)
```

### Marker Operations
```python
# CREATE
marker = db.add_marker(type, lat, lon, title, description, polygon_id)

# READ
all_markers = db.get_markers()
polygon_markers = db.get_markers(polygon_id=polygon_id)
type_markers = db.get_markers(marker_type='npk_sample')

# DELETE
db.delete_marker(marker_id)
```

---

## 📊 Contoh Query Praktis

### 1. Cari lahan terluas
```python
polygons = db.get_polygons()
largest = max(polygons, key=lambda p: p['area_sqm'])
print(f"Lahan terluas: {largest['name']} ({largest['area_hectares']} ha)")
```

### 2. Hitung rata-rata NPK
```python
npk_data = db.get_npk_data()
if npk_data:
    avg_n = sum(d['n_value'] for d in npk_data) / len(npk_data)
    avg_p = sum(d['p_value'] for d in npk_data) / len(npk_data)
    avg_k = sum(d['k_value'] for d in npk_data) / len(npk_data)
    print(f"Rata-rata NPK: N={avg_n:.1f}, P={avg_p:.1f}, K={avg_k:.1f}")
```

### 3. Filter NPK berdasarkan kondisi
```python
npk_data = db.get_npk_data()

# NPK dengan nitrogen rendah
low_n = [d for d in npk_data if d['n_value'] < 40]
print(f"Lokasi dengan N rendah: {len(low_n)}")

# NPK optimal (semua nutrient dalam range)
optimal = [d for d in npk_data 
           if 40 <= d['n_value'] <= 100 
           and 20 <= d['p_value'] <= 60 
           and 30 <= d['k_value'] <= 80]
print(f"Lokasi dengan NPK optimal: {len(optimal)}")
```

---

## 🔐 Backup & Restore

### Backup Database
```bash
# Windows
xcopy instance\agrimap_*.json backup\ /Y

# Atau dengan Python
python -c "import shutil; shutil.copytree('instance', 'backup_agrimap', dirs_exist_ok=True)"
```

### Restore Database
```bash
# Windows
xcopy backup\agrimap_*.json instance\ /Y
```

---

## 💡 Tips

1. **Selalu backup** sebelum edit manual file JSON
2. **Gunakan API** untuk operasi CRUD yang aman
3. **Gunakan Service Layer** untuk analisis dan logika bisnis
4. **Validasi data** sebelum menyimpan
5. **Check file permissions** jika ada error write

---

## 🚨 Troubleshooting

### File tidak ditemukan
```python
import os
print(os.path.exists('instance/agrimap_npk_data.json'))
# Jika False, file belum dibuat. Jalankan aplikasi sekali untuk inisialisasi
```

### Permission denied
```bash
# Pastikan folder instance writable
# Windows: Right-click folder → Properties → Security
```

### Data corrupt
```python
# Reset database (HATI-HATI: menghapus semua data!)
import json
with open('instance/agrimap_npk_data.json', 'w') as f:
    json.dump([], f)
```

---

Semoga membantu! 🎉
