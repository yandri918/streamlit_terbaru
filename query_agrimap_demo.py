"""
Script untuk query dan eksplorasi database AgriMap
Jalankan: python query_agrimap_demo.py
"""

from app.data.agrimap_db import AgriMapDatabase
from app.services.agrimap_service import AgriMapService
import json
from datetime import datetime

def main():
    print("=" * 60)
    print("🗺️  AGRIMAP DATABASE EXPLORER")
    print("=" * 60)
    print()
    
    # Inisialisasi
    db = AgriMapDatabase()
    service = AgriMapService()
    
    # 1. STATISTIK KESELURUHAN
    print("📊 STATISTIK KESELURUHAN")
    print("-" * 60)
    stats = db.get_statistics()
    print(f"Total Lahan Tersimpan    : {stats['total_polygons']}")
    print(f"Total Area               : {stats['total_area_sqm']:,.0f} m² ({stats['total_area_hectares']} ha)")
    print(f"Total Sampel NPK         : {stats['total_npk_samples']}")
    print(f"Total Marker             : {stats['total_markers']}")
    print()
    
    # 2. DAFTAR LAHAN (POLYGONS)
    print("📍 DAFTAR LAHAN")
    print("-" * 60)
    polygons = db.get_polygons()
    
    if polygons:
        for i, p in enumerate(polygons, 1):
            print(f"{i}. {p['name']}")
            print(f"   ID       : {p['id']}")
            print(f"   Luas     : {p['area_sqm']:,.0f} m² ({p['area_hectares']} ha)")
            print(f"   pH       : {p.get('ph', 'N/A')}")
            print(f"   Dibuat   : {p['created_at']}")
            if p.get('notes'):
                print(f"   Catatan  : {p['notes']}")
            print()
    else:
        print("   Belum ada lahan tersimpan.")
        print("   Buka http://localhost:5000/modules/peta-data-tanah untuk menambah lahan.")
        print()
    
    # 3. DATA NPK
    print("🧪 DATA NPK TANAH")
    print("-" * 60)
    npk_data = db.get_npk_data()
    
    if npk_data:
        for i, npk in enumerate(npk_data, 1):
            print(f"{i}. Lokasi: ({npk['latitude']:.6f}, {npk['longitude']:.6f})")
            print(f"   N = {npk['n_value']}, P = {npk['p_value']}, K = {npk['k_value']}")
            
            # Analisis
            analysis = service.analyze_npk_values(
                npk['n_value'], 
                npk['p_value'], 
                npk['k_value']
            )
            
            print(f"   Status: ", end="")
            for nutrient, data in analysis['analysis'].items():
                print(f"{nutrient}={data['status']} ", end="")
            print()
            
            if npk.get('notes'):
                print(f"   Catatan: {npk['notes']}")
            print(f"   Tanggal: {npk['created_at']}")
            print()
        
        # Hitung rata-rata
        avg_n = sum(d['n_value'] for d in npk_data) / len(npk_data)
        avg_p = sum(d['p_value'] for d in npk_data) / len(npk_data)
        avg_k = sum(d['k_value'] for d in npk_data) / len(npk_data)
        
        print(f"📈 Rata-rata NPK: N={avg_n:.1f}, P={avg_p:.1f}, K={avg_k:.1f}")
        print()
    else:
        print("   Belum ada data NPK tersimpan.")
        print("   Gunakan tab 'Data NPK' di AgriMap untuk menambah data.")
        print()
    
    # 4. MARKER
    print("📌 MARKER DI PETA")
    print("-" * 60)
    markers = db.get_markers()
    
    if markers:
        marker_types = {}
        for marker in markers:
            mtype = marker['type']
            marker_types[mtype] = marker_types.get(mtype, 0) + 1
        
        for mtype, count in marker_types.items():
            print(f"   {mtype}: {count} marker")
        print()
    else:
        print("   Belum ada marker.")
        print()
    
    # 5. ANALISIS LANJUTAN
    if npk_data:
        print("🔬 ANALISIS LANJUTAN")
        print("-" * 60)
        
        # NPK dengan kondisi rendah
        low_nutrients = []
        for npk in npk_data:
            analysis = service.analyze_npk_values(
                npk['n_value'], 
                npk['p_value'], 
                npk['k_value']
            )
            if analysis['overall']['deficiencies']:
                low_nutrients.append({
                    'location': (npk['latitude'], npk['longitude']),
                    'deficiencies': analysis['overall']['deficiencies']
                })
        
        if low_nutrients:
            print(f"⚠️  {len(low_nutrients)} lokasi memerlukan perhatian:")
            for loc in low_nutrients:
                print(f"   Lokasi ({loc['location'][0]:.4f}, {loc['location'][1]:.4f})")
                print(f"   Kekurangan: {', '.join(loc['deficiencies'])}")
                print()
        else:
            print("✅ Semua lokasi dalam kondisi optimal!")
            print()
    
    # 6. EXPORT DATA
    print("💾 EXPORT DATA")
    print("-" * 60)
    
    export_data = {
        'exported_at': datetime.now().isoformat(),
        'statistics': stats,
        'polygons': polygons,
        'npk_data': npk_data,
        'markers': markers
    }
    
    export_file = 'agrimap_export.json'
    with open(export_file, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Data berhasil di-export ke: {export_file}")
    print()
    
    # 7. REKOMENDASI
    print("💡 REKOMENDASI")
    print("-" * 60)
    
    if not polygons:
        print("   1. Buka AgriMap dan gambar polygon untuk lahan Anda")
    
    if not npk_data:
        print("   2. Tambahkan data NPK tanah untuk analisis yang lebih baik")
    
    if polygons and npk_data:
        print("   ✅ Data sudah lengkap!")
        print("   - Gunakan heatmap untuk visualisasi kualitas tanah")
        print("   - Klik 'Hitung Pupuk' untuk rekomendasi pemupukan")
        print("   - Export data untuk analisis lebih lanjut")
    
    print()
    print("=" * 60)
    print("Selesai! Terima kasih telah menggunakan AgriMap 🌾")
    print("=" * 60)

if __name__ == '__main__':
    main()
