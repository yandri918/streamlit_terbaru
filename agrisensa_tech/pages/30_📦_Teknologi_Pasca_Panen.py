import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Teknologi Pasca Panen - AgriSensa",
    page_icon="📦",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Header
st.title("📦 Teknologi Pasca Panen")
st.markdown("**Optimasi Penanganan, Penyimpanan, dan Pengolahan Hasil Pertanian**")

# Main tabs
tab_harvest, tab_storage, tab_processing, tab_quality, tab_value = st.tabs([
    "🌾 Pemanenan",
    "🏪 Penyimpanan", 
    "⚙️ Pengolahan",
    "✅ Kontrol Kualitas",
    "💎 Produk Nilai Tambah"
])

# ===== TAB 1: PEMANENAN =====
with tab_harvest:
    st.header("🌾 Teknik Pemanenan")
    
    st.markdown("""
    ### Definisi Pemanenan
    
    **Pemanenan** adalah proses **pengambilan hasil pertanian** dari tanaman pada saat yang tepat untuk mendapatkan **kualitas dan kuantitas optimal**.
    
    **Tujuan:**
    - ✅ Maksimalkan hasil panen (yield)
    - ✅ Optimalkan kualitas produk
    - ✅ Minimalkan kehilangan (losses)
    - ✅ Perpanjang shelf-life
    
    **Referensi:**
    - Kader, A. A. (2002). Postharvest Technology of Horticultural Crops. UC ANR Publications.
    
    ---
    
    ## 📅 WAKTU PANEN (HARVEST TIMING)
    
    ### **Indeks Kematangan (Maturity Indices)**
    
    **1. Indeks Visual:**
    ```
    - Warna kulit/daging
    - Ukuran buah
    - Bentuk
    - Gloss (kilap permukaan)
    - Abscission (mudah lepas dari tangkai)
    ```
    
    **2. Indeks Fisik:**
    ```
    - Kekerasan (firmness) - Penetrometer
    - Berat jenis (specific gravity)
    - Tekstur
    ```
    
    **3. Indeks Kimia:**
    ```
    - Total Soluble Solids (TSS/°Brix)
    - Titratable Acidity (TA)
    - TSS/TA ratio
    - Starch content (iodine test)
    - Dry matter content
    ```
    
    **4. Indeks Fisiologis:**
    ```
    - Respiration rate
    - Ethylene production
    - Heat units (Growing Degree Days)
    - Days After Anthesis (DAA)
    ```
    
    **Referensi:**
    - Watada, A. E., et al. (1984). HortScience, 19(1), 20-21
    
    ---
    
    ## 🌾 CONTOH INDEKS KEMATANGAN BERBAGAI KOMODITAS
    
    ### **BUAH-BUAHAN:**
    
    | Komoditas | Indeks Utama | Nilai Optimal | Metode |
    |-----------|--------------|---------------|--------|
    | **Tomat** | Warna + Firmness | Breaker-Pink | Visual + Penetrometer |
    | **Mangga** | TSS + Warna | 12-14°Brix | Refractometer |
    | **Pisang** | Diameter + Warna | 3/4 full, hijau | Caliper |
    | **Apel** | Firmness + TSS | 60-70 N, 12-14°Brix | Penetrometer + Refractometer |
    | **Jeruk** | TSS/TA ratio | 8-12 | Lab analysis |
    | **Alpukat** | Dry matter | 20-25% | Oven drying |
    
    ### **SAYURAN:**
    
    | Komoditas | Indeks Utama | Nilai Optimal | Metode |
    |-----------|--------------|---------------|--------|
    | **Cabai** | Warna + Ukuran | Merah penuh | Visual |
    | **Tomat** | Warna | Breaker-Red | Color chart |
    | **Kentang** | Skin set + Umur | 90-120 hari | Visual + Calendar |
    | **Wortel** | Diameter + Warna | 2-4 cm, orange | Caliper + Visual |
    | **Brokoli** | Ukuran + Kompak | 10-15 cm, tight | Visual |
    
    ### **PADI & SEREALIA:**
    
    | Komoditas | Indeks Utama | Nilai Optimal | Metode |
    |-----------|--------------|---------------|--------|
    | **Padi** | Kadar air + Warna | 20-25%, kuning | Moisture meter |
    | **Jagung** | Kadar air + Black layer | 18-22% | Moisture meter + Visual |
    | **Gandum** | Kadar air + Warna | 12-14% | Moisture meter |
    
    ---
    
    ## ⏰ WAKTU PANEN OPTIMAL
    
    ### **Waktu Hari:**
    
    **PAGI (6-9 AM):** ✅ TERBAIK
    ```
    Keuntungan:
    - Suhu rendah (produk sejuk)
    - Turgor tinggi (kesegaran maksimal)
    - Transpirasi rendah
    - Kadar gula tinggi (akumulasi malam)
    
    Cocok untuk:
    - Sayuran daun (lettuce, spinach)
    - Bunga potong
    - Buah lunak (strawberry, raspberry)
    ```
    
    **SIANG (10 AM - 3 PM):** ⚠️ HINDARI
    ```
    Masalah:
    - Suhu tinggi (stress panas)
    - Transpirasi tinggi (kehilangan air)
    - Turgor rendah (layu)
    - Kualitas menurun
    ```
    
    **SORE (4-6 PM):** ✅ BAIK
    ```
    Keuntungan:
    - Suhu mulai turun
    - Turgor recovery
    
    Cocok untuk:
    - Buah keras (apel, mangga)
    - Umbi-umbian
    ```
    
    ---
    
    ## 🛠️ METODE PEMANENAN
    
    ### **1. MANUAL (Hand Harvesting)**
    
    **Keuntungan:**
    ```
    ✅ Selektif (pilih yang matang)
    ✅ Kerusakan minimal
    ✅ Cocok untuk buah lunak
    ✅ Fleksibel
    ```
    
    **Kekurangan:**
    ```
    ❌ Lambat
    ❌ Biaya tenaga kerja tinggi
    ❌ Tidak konsisten
    ❌ Tergantung ketersediaan pekerja
    ```
    
    **Cocok untuk:**
    - Buah lunak (strawberry, tomat)
    - Bunga potong
    - Sayuran premium
    
    **Teknik Manual:**
    
    **A. Petik Tangan (Hand Picking):**
    ```
    - Pegang buah dengan lembut
    - Putar dan tarik (twist & pull)
    - Jangan menarik paksa
    - Hindari memar/luka
    ```
    
    **B. Gunting/Pisau:**
    ```
    - Potong tangkai 1-2 cm dari buah
    - Pisau tajam (clean cut)
    - Sterilisasi alat (hindari infeksi)
    ```
    
    **C. Panen Bertahap (Multiple Harvest):**
    ```
    - Panen 2-3x per minggu
    - Pilih yang sudah matang
    - Sisakan yang belum matang
    
    Cocok untuk: Tomat, cabai, timun
    ```
    
    ---
    
    ### **2. MEKANIS (Mechanical Harvesting)**
    
    **Keuntungan:**
    ```
    ✅ Cepat (efisien waktu)
    ✅ Hemat biaya (skala besar)
    ✅ Konsisten
    ✅ Tidak tergantung tenaga kerja
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi awal tinggi
    ❌ Kerusakan lebih banyak
    ❌ Tidak selektif
    ❌ Perlu varietas khusus
    ```
    
    **Jenis Mesin:**
    
    **A. Combine Harvester (Padi, Gandum):**
    ```
    Fungsi:
    - Potong tanaman
    - Pisahkan biji dari jerami
    - Bersihkan
    - Kumpulkan biji
    
    Kapasitas: 1-2 ha/jam
    ```
    
    **B. Shaker (Buah Pohon):**
    ```
    Prinsip:
    - Getarkan pohon
    - Buah jatuh ke jaring
    
    Cocok untuk: Kopi, kelapa sawit, zaitun
    ```
    
    **C. Conveyor Belt (Sayuran Akar):**
    ```
    Prinsip:
    - Gali tanah
    - Pisahkan umbi
    - Angkut dengan belt
    
    Cocok untuk: Kentang, wortel, bawang
    ```
    
    ---
    
    ## 📦 WADAH PANEN (HARVEST CONTAINERS)
    
    ### **Kriteria Wadah Ideal:**
    
    ```
    ✅ Bersih (tidak kontaminasi)
    ✅ Kuat (tahan beban)
    ✅ Ventilasi baik (sirkulasi udara)
    ✅ Permukaan halus (tidak melukai)
    ✅ Mudah dibersihkan
    ✅ Ukuran sesuai (tidak terlalu besar)
    ```
    
    ### **Jenis Wadah:**
    
    **1. Keranjang Plastik (Crates):**
    ```
    Keuntungan:
    - Kuat, tahan lama
    - Mudah dibersihkan
    - Stackable (hemat ruang)
    - Ventilasi baik
    
    Kapasitas: 10-20 kg
    Cocok untuk: Tomat, apel, jeruk
    ```
    
    **2. Karung (Sacks):**
    ```
    Keuntungan:
    - Murah
    - Ringan
    - Mudah didapat
    
    Kekurangan:
    - Ventilasi kurang
    - Mudah rusak
    - Susah dibersihkan
    
    Cocok untuk: Padi, jagung, kacang
    ```
    
    **3. Kardus (Cartons):**
    ```
    Keuntungan:
    - Ringan
    - Bisa custom size
    - Proteksi baik
    
    Kekurangan:
    - Sekali pakai
    - Tidak tahan air
    
    Cocok untuk: Buah premium, export
    ```
    
    **4. Bucket/Ember:**
    ```
    Cocok untuk:
    - Buah lunak (strawberry)
    - Panen skala kecil
    
    Kapasitas: 5-10 kg
    ```
    
    ---
    
    ## ⚠️ KESALAHAN UMUM SAAT PANEN
    
    ### **1. Panen Terlalu Dini:**
    ```
    Masalah:
    - Ukuran kecil
    - Rasa kurang manis
    - Tidak bisa matang sempurna
    - Nilai jual rendah
    
    Contoh: Mangga dipanen hijau (tidak akan manis)
    ```
    
    ### **2. Panen Terlalu Lambat:**
    ```
    Masalah:
    - Over-ripe (terlalu matang)
    - Mudah busuk
    - Shelf-life pendek
    - Susah ditransport
    
    Contoh: Pisang dipanen kuning (cepat busuk)
    ```
    
    ### **3. Panen Saat Hujan/Basah:**
    ```
    Masalah:
    - Kadar air tinggi
    - Mudah busuk (jamur, bakteri)
    - Sulit disimpan
    
    Solusi: Tunggu kering (2-3 jam setelah hujan)
    ```
    
    ### **4. Penanganan Kasar:**
    ```
    Masalah:
    - Memar (bruising)
    - Luka (wounds)
    - Pintu masuk patogen
    - Kualitas menurun
    
    Solusi:
    - Panen hati-hati
    - Wadah berlapis (padding)
    - Jangan lempar/jatuhkan
    ```
    
    ### **5. Tumpuk Terlalu Tinggi:**
    ```
    Masalah:
    - Produk di bawah tertekan
    - Memar, pecah
    - Panas (respirasi tinggi)
    
    Solusi:
    - Maksimal 3-4 lapis
    - Gunakan wadah kecil
    ```
    
    ---
    
    ## 💡 BEST PRACTICES PEMANENAN
    
    ### **Sebelum Panen:**
    
    ```
    1. PERSIAPAN ALAT:
       - Bersihkan wadah
       - Sterilisasi pisau/gunting
       - Siapkan label
    
    2. CEK CUACA:
       - Hindari hujan
       - Pilih pagi/sore
    
    3. TRAINING PEKERJA:
       - Cara panen yang benar
       - Kriteria kematangan
       - Handling yang lembut
    ```
    
    ### **Saat Panen:**
    
    ```
    1. SELEKTIF:
       - Pilih yang matang optimal
       - Sisihkan yang rusak/sakit
    
    2. HATI-HATI:
       - Jangan melukai produk
       - Jangan menarik paksa
    
    3. CEPAT:
       - Minimize field heat
       - Langsung ke tempat teduh
    
    4. BERSIH:
       - Hindari kontaminasi tanah
       - Jangan campur dengan sampah
    ```
    
    ### **Setelah Panen:**
    
    ```
    1. SEGERA DINGINKAN:
       - Turunkan suhu (pre-cooling)
       - Kurangi respirasi
    
    2. SORTASI:
       - Pisahkan berdasarkan kualitas
       - Buang yang rusak
    
    3. GRADING:
       - Kelompokkan berdasarkan ukuran
       - Seragamkan kualitas
    
    4. PACKING:
       - Wadah bersih
       - Jangan terlalu penuh
       - Label yang jelas
    ```
    
    ---
    
    ## 📊 KEHILANGAN SAAT PANEN (HARVEST LOSSES)
    
    ### **Sumber Kehilangan:**
    
    | Sumber | Persentase | Penyebab | Solusi |
    |--------|------------|----------|--------|
    | **Mekanis** | 5-15% | Memar, luka, pecah | Handling lembut |
    | **Fisiologis** | 3-10% | Over-ripe, under-ripe | Timing tepat |
    | **Patologis** | 2-8% | Jamur, bakteri | Sanitasi, cepat dinginkan |
    | **Tertinggal** | 1-5% | Tidak terpanen | Panen menyeluruh |
    | **Total** | **11-38%** | Kombinasi | Manajemen baik |
    
    **Target:** Kehilangan < 10%
    
    ---
    
    ## 🎯 STUDI KASUS
    
    ### **Kasus 1: Panen Tomat**
    
    ```
    KONDISI:
    - Varietas: Tomat beef
    - Tujuan: Pasar lokal (2-3 hari transport)
    
    PROTOKOL:
    1. Indeks: Breaker stage (mulai merah)
    2. Waktu: Pagi (6-8 AM)
    3. Metode: Manual (hand picking)
    4. Wadah: Crate plastik (berlapis foam)
    5. Kapasitas: Maksimal 10 kg/crate
    6. Sortasi: Langsung di lapangan
    7. Pre-cooling: Simpan di tempat teduh
    8. Transport: Dalam 4 jam
    
    HASIL:
    - Kehilangan: < 5%
    - Kualitas: Grade A 80%
    - Shelf-life: 7-10 hari
    ```
    
    ### **Kasus 2: Panen Padi**
    
    ```
    KONDISI:
    - Varietas: IR64
    - Luas: 1 ha
    - Tujuan: Dijual sebagai gabah kering
    
    PROTOKOL:
    1. Indeks: Kadar air 20-22%
    2. Waktu: Pagi (setelah embun kering)
    3. Metode: Combine harvester
    4. Langsung perontokan
    5. Jemur hingga 14% kadar air
    6. Simpan dalam karung
    
    HASIL:
    - Efisiensi: 1 ha/2 jam
    - Kehilangan: < 8%
    - Kualitas: Beras kepala 60-65%
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Kader, A. A. (2002).** Postharvest Technology of Horticultural Crops, 3rd Edition. UC ANR Publications.
    
    2. **Watada, A. E., et al. (1984).** Terminology for the description of developmental stages of horticultural crops. HortScience, 19(1), 20-21.
    
    3. **Wills, R. B. H., et al. (2007).** Postharvest: An Introduction to the Physiology and Handling of Fruit and Vegetables, 5th Edition.
    
    4. **FAO. (2011).** Global Food Losses and Food Waste. FAO, Rome.
    
    """)

# ===== TAB 2: PENYIMPANAN =====
with tab_storage:
    st.header("🏪 Teknologi Penyimpanan")
    
    st.markdown("""
    ### Tujuan Penyimpanan
    
    **Penyimpanan** adalah proses **mempertahankan kualitas** produk pertanian setelah panen untuk **memperpanjang shelf-life** dan **mengurangi kehilangan**.
    
    **Tujuan:**
    - ✅ Perpanjang masa simpan (shelf-life)
    - ✅ Pertahankan kualitas (nutrisi, rasa, tekstur)
    - ✅ Stabilkan harga (supply kontinyu)
    - ✅ Kurangi kehilangan (losses)
    - ✅ Tambah nilai (value addition)
    
    **Referensi:**
    - Thompson, J. F., et al. (2008). Commercial Cooling of Fruits, Vegetables, and Flowers. UC ANR Publications.
    
    ---
    
    ## 🌡️ FAKTOR YANG MEMPENGARUHI PENYIMPANAN
    
    ### **1. SUHU (Temperature)**
    
    **Prinsip:**
    ```
    Suhu ↓ → Respirasi ↓ → Shelf-life ↑
    
    Setiap penurunan 10°C → Respirasi ↓ 50-70%
    (Q10 = 2-3)
    ```
    
    **Suhu Optimal Berbagai Komoditas:**
    
    | Komoditas | Suhu Optimal | RH Optimal | Shelf-Life |
    |-----------|--------------|------------|------------|
    | **Tomat (Mature Green)** | 12-15°C | 90-95% | 2-3 minggu |
    | **Tomat (Ripe)** | 8-10°C | 90-95% | 1 minggu |
    | **Apel** | 0-4°C | 90-95% | 3-6 bulan |
    | **Pisang** | 13-15°C | 90-95% | 2-4 minggu |
    | **Mangga** | 10-13°C | 85-90% | 2-3 minggu |
    | **Kentang** | 4-7°C | 90-95% | 4-6 bulan |
    | **Wortel** | 0-2°C | 95-100% | 4-6 bulan |
    | **Lettuce** | 0-2°C | 95-100% | 2-3 minggu |
    | **Cabai** | 7-10°C | 90-95% | 2-3 minggu |
    | **Bawang** | 0-2°C | 65-70% | 6-8 bulan |
    
    **PENTING:**
    - Setiap komoditas punya suhu optimal berbeda!
    - Terlalu rendah → Chilling injury
    - Terlalu tinggi → Cepat busuk
    
    ---
    
    ### **2. KELEMBABAN (Relative Humidity - RH)**
    
    **Fungsi:**
    ```
    RH tinggi → Transpirasi ↓ → Kehilangan air ↓
    RH rendah → Transpirasi ↑ → Wilting (layu)
    ```
    
    **Kategori:**
    
    **A. RH Tinggi (90-95%):**
    ```
    Cocok untuk:
    - Sayuran daun (lettuce, spinach)
    - Buah lunak (strawberry)
    - Umbi-umbian (wortel, kentang)
    
    Tujuan: Cegah kehilangan air
    ```
    
    **B. RH Sedang (85-90%):**
    ```
    Cocok untuk:
    - Buah klimakterik (tomat, mangga)
    - Sayuran buah (cabai, terong)
    ```
    
    **C. RH Rendah (65-70%):**
    ```
    Cocok untuk:
    - Bawang, bawang putih
    - Kacang-kacangan
    
    Tujuan: Cegah jamur
    ```
    
    ---
    
    ### **3. ATMOSFER (Atmosphere)**
    
    **Udara Normal:**
    ```
    - O₂: 21%
    - CO₂: 0.03%
    - N₂: 78%
    ```
    
    **Modified Atmosphere (MA):**
    ```
    - O₂: 2-5% (↓)
    - CO₂: 3-10% (↑)
    - N₂: Balance
    
    Efek:
    - Respirasi ↓
    - Ethylene production ↓
    - Senescence ↓
    - Shelf-life ↑
    ```
    
    **Controlled Atmosphere (CA):**
    ```
    Seperti MA, tapi:
    - Kontrol presisi
    - Monitoring kontinyu
    - Adjust otomatis
    
    Cocok untuk: Apel, pir (storage jangka panjang)
    ```
    
    **Referensi:**
    - Kader, A. A., & Saltveit, M. E. (2003). Postharvest Physiology and Pathology of Vegetables, 2nd Edition.
    
    ---
    
    ## 🧊 METODE PENDINGINAN (COOLING METHODS)
    
    ### **1. Room Cooling**
    
    **Prinsip:**
    ```
    Produk disimpan di ruang dingin
    Pendinginan pasif (lambat)
    ```
    
    **Karakteristik:**
    ```
    - Lambat (12-24 jam)
    - Murah
    - Cocok untuk produk tidak mudah rusak
    
    Contoh: Kentang, bawang, labu
    ```
    
    ---
    
    ### **2. Forced-Air Cooling**
    
    **Prinsip:**
    ```
    Udara dingin dipaksa melewati produk
    Pendinginan cepat
    ```
    
    **Karakteristik:**
    ```
    - Cepat (2-6 jam)
    - Efisien
    - Cocok untuk produk dalam wadah
    
    Contoh: Tomat, apel, jeruk
    ```
    
    **Setup:**
    ```
    Produk dalam crate → Stack dengan gap
    → Fan menarik udara dingin melewati produk
    → Panas terbuang
    ```
    
    ---
    
    ### **3. Hydrocooling**
    
    **Prinsip:**
    ```
    Produk disemprot/direndam air dingin (0-2°C)
    Pendinginan sangat cepat
    ```
    
    **Karakteristik:**
    ```
    - Sangat cepat (15-30 menit)
    - Efektif
    - Cocok untuk produk tahan air
    
    Contoh: Wortel, selada, brokoli
    ```
    
    **TIDAK cocok untuk:**
    - Produk mudah rusak oleh air
    - Produk dengan wax coating
    
    ---
    
    ### **4. Vacuum Cooling**
    
    **Prinsip:**
    ```
    Tekanan ↓ → Titik didih air ↓
    → Air menguap → Panas terserap
    → Produk dingin
    ```
    
    **Karakteristik:**
    ```
    - Sangat cepat (20-30 menit)
    - Cocok untuk sayuran daun (luas permukaan besar)
    
    Contoh: Lettuce, spinach, celery
    ```
    
    **Kekurangan:**
    - Kehilangan air 2-4%
    - Investasi tinggi
    
    ---
    
    ### **5. Evaporative Cooling**
    
    **Prinsip:**
    ```
    Air menguap → Serap panas → Suhu turun
    ```
    
    **Karakteristik:**
    ```
    - Murah (low-tech)
    - Cocok untuk daerah kering
    - Penurunan suhu 5-10°C
    
    Contoh: Pot-in-pot cooler, wet gunny sack
    ```
    
    **Cocok untuk:**
    - Petani kecil
    - Daerah tanpa listrik
    - Storage sementara
    
    ---
    
    ## 📦 JENIS PENYIMPANAN
    
    ### **1. AMBIENT STORAGE (Suhu Ruang)**
    
    **Kondisi:**
    ```
    - Suhu: 20-30°C
    - RH: 60-80%
    - Ventilasi alami
    ```
    
    **Cocok untuk:**
    ```
    - Bawang, bawang putih
    - Labu, ubi jalar
    - Kacang-kacangan kering
    - Padi, jagung (kering)
    ```
    
    **Shelf-life:** 1-6 bulan (tergantung komoditas)
    
    ---
    
    ### **2. COLD STORAGE (Penyimpanan Dingin)**
    
    **Kondisi:**
    ```
    - Suhu: 0-15°C (tergantung komoditas)
    - RH: 85-95%
    - Ventilasi terkontrol
    ```
    
    **Cocok untuk:**
    ```
    - Buah-buahan (apel, jeruk, anggur)
    - Sayuran (wortel, kentang, lettuce)
    - Bunga potong
    ```
    
    **Shelf-life:** 1 minggu - 6 bulan
    
    **Jenis:**
    
    **A. Walk-in Cold Room:**
    ```
    - Kapasitas: 5-50 ton
    - Suhu: 0-15°C
    - Cocok untuk: Komersial
    ```
    
    **B. Refrigerated Container:**
    ```
    - Kapasitas: 10-30 ton
    - Mobile
    - Cocok untuk: Transport + storage
    ```
    
    **C. Household Refrigerator:**
    ```
    - Kapasitas: 100-500 kg
    - Cocok untuk: Petani kecil, retail
    ```
    
    ---
    
    ### **3. CONTROLLED ATMOSPHERE (CA) STORAGE**
    
    **Kondisi:**
    ```
    - Suhu: 0-4°C
    - RH: 90-95%
    - O₂: 1-5%
    - CO₂: 1-5%
    ```
    
    **Cocok untuk:**
    ```
    - Apel (storage 6-12 bulan)
    - Pir
    - Kiwi
    ```
    
    **Keuntungan:**
    ```
    ✅ Shelf-life sangat panjang
    ✅ Kualitas terjaga
    ✅ Kehilangan minimal
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi sangat tinggi
    ❌ Operasional kompleks
    ❌ Perlu monitoring ketat
    ```
    
    ---
    
    ## ⚠️ MASALAH PENYIMPANAN & SOLUSI
    
    ### **1. CHILLING INJURY (Kerusakan Dingin)**
    
    **Penyebab:**
    ```
    Suhu terlalu rendah untuk komoditas sensitif dingin
    ```
    
    **Gejala:**
    ```
    - Pitting (bintik-bintik)
    - Discoloration (perubahan warna)
    - Water-soaking
    - Gagal matang
    - Mudah busuk
    ```
    
    **Komoditas Sensitif:**
    ```
    - Pisang (< 13°C)
    - Mangga (< 10°C)
    - Tomat (< 10°C)
    - Timun (< 7°C)
    - Alpukat (< 4°C)
    ```
    
    **Solusi:**
    ```
    ✅ Simpan pada suhu optimal (lihat tabel)
    ✅ Jangan terlalu rendah!
    ✅ Gradual cooling (bertahap)
    ```
    
    ---
    
    ### **2. FREEZING INJURY (Kerusakan Beku)**
    
    **Penyebab:**
    ```
    Suhu < 0°C → Kristal es terbentuk
    → Pecah sel → Rusak
    ```
    
    **Gejala:**
    ```
    - Water-soaking
    - Tekstur lembek
    - Tidak bisa recovery
    ```
    
    **Solusi:**
    ```
    ✅ Jangan simpan < 0°C (kecuali untuk freezing)
    ✅ Monitor suhu ketat
    ```
    
    ---
    
    ### **3. WILTING (Layu)**
    
    **Penyebab:**
    ```
    Kehilangan air (transpirasi) > penyerapan
    RH rendah
    ```
    
    **Gejala:**
    ```
    - Daun layu
    - Kulit keriput
    - Berat turun
    - Kualitas menurun
    ```
    
    **Solusi:**
    ```
    ✅ RH tinggi (90-95%)
    ✅ Packaging (reduce transpirasi)
    ✅ Waxing (coating)
    ✅ Suhu rendah
    ```
    
    ---
    
    ### **4. DECAY (Pembusukan)**
    
    **Penyebab:**
    ```
    Jamur, bakteri
    Kondisi: Suhu tinggi, RH tinggi, luka
    ```
    
    **Patogen Umum:**
    ```
    - Botrytis (gray mold)
    - Penicillium (blue/green mold)
    - Rhizopus (soft rot)
    - Erwinia (bacterial soft rot)
    ```
    
    **Solusi:**
    ```
    ✅ Sanitasi (bersih)
    ✅ Suhu rendah (slow down growth)
    ✅ Handling hati-hati (avoid wounds)
    ✅ Sortasi (buang yang rusak)
    ✅ Fungisida (jika perlu)
    ```
    
    ---
    
    ## 💡 BEST PRACTICES PENYIMPANAN
    
    ### **Sebelum Simpan:**
    
    ```
    1. PRE-COOLING:
       - Dinginkan segera setelah panen
       - Turunkan field heat
       - Target: Suhu optimal dalam 4-6 jam
    
    2. SORTASI:
       - Buang yang rusak/sakit
       - Pisahkan berdasarkan kematangan
    
    3. CLEANING:
       - Bersihkan kotoran
       - Cuci (jika perlu)
       - Keringkan
    
    4. TREATMENT (Optional):
       - Fungisida
       - Waxing
       - 1-MCP (anti-ethylene)
    ```
    
    ### **Saat Penyimpanan:**
    
    ```
    1. MONITORING:
       - Cek suhu & RH harian
       - Catat data
       - Adjust jika perlu
    
    2. VENTILASI:
       - Sirkulasi udara baik
       - Hindari hot spots
    
    3. STACKING:
       - Jangan terlalu rapat
       - Beri jarak untuk airflow
       - Maksimal 2-3 meter tinggi
    
    4. ROTASI:
       - FIFO (First In First Out)
       - Jual yang lama dulu
    
    5. INSPEKSI:
       - Cek kondisi produk
       - Buang yang busuk
       - Cegah penyebaran
    ```
    
    ---
    
    ## 📊 KEHILANGAN SAAT PENYIMPANAN
    
    ### **Sumber Kehilangan:**
    
    | Sumber | Persentase | Penyebab | Solusi |
    |--------|------------|----------|--------|
    | **Respirasi** | 2-5% | Kehilangan berat | Suhu rendah |
    | **Transpirasi** | 3-8% | Kehilangan air | RH tinggi |
    | **Decay** | 5-20% | Jamur, bakteri | Sanitasi, suhu rendah |
    | **Sprouting** | 1-5% | Kentang, bawang | Suhu optimal, inhibitor |
    | **Mechanical** | 1-3% | Handling | Hati-hati |
    | **Total** | **12-41%** | Kombinasi | Manajemen baik |
    
    **Target:** Kehilangan < 10%
    
    ---
    
    ## 🎯 STUDI KASUS
    
    ### **Kasus 1: Cold Storage Apel**
    
    ```
    KONDISI:
    - Varietas: Fuji
    - Volume: 10 ton
    - Target: Storage 6 bulan
    
    PROTOKOL:
    1. Panen: Saat optimal maturity
    2. Pre-cooling: Forced-air (4-6 jam)
    3. Sortasi: Grade A, B, C
    4. Treatment: Waxing + fungisida
    5. Storage:
       - Suhu: 0-2°C
       - RH: 90-95%
       - Ventilasi: Baik
    6. Monitoring: Harian (suhu, RH)
    7. Inspeksi: Mingguan (decay)
    
    HASIL:
    - Shelf-life: 6 bulan
    - Kehilangan: < 8%
    - Kualitas: 90% Grade A
    - Firmness: Terjaga
    ```
    
    ### **Kasus 2: Ambient Storage Bawang**
    
    ```
    KONDISI:
    - Varietas: Bawang merah
    - Volume: 1 ton
    - Target: Storage 3 bulan
    
    PROTOKOL:
    1. Panen: Saat daun rebah 80%
    2. Curing: Jemur 7-10 hari (kadar air 12-14%)
    3. Sortasi: Buang yang rusak
    4. Storage:
       - Suhu: Ambient (25-30°C)
       - RH: 65-70% (rendah!)
       - Ventilasi: Baik
       - Wadah: Karung jaring (breathable)
    5. Monitoring: Mingguan
    
    HASIL:
    - Shelf-life: 3 bulan
    - Kehilangan: < 15%
    - Sprouting: Minimal
    - Kualitas: Baik
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Thompson, J. F., et al. (2008).** Commercial Cooling of Fruits, Vegetables, and Flowers. UC ANR Publications.
    
    2. **Kader, A. A., & Saltveit, M. E. (2003).** Postharvest Physiology and Pathology of Vegetables, 2nd Edition.
    
    3. **Wills, R. B. H., et al. (2007).** Postharvest: An Introduction to the Physiology and Handling of Fruit and Vegetables, 5th Edition.
    
    4. **ASHRAE. (2010).** Refrigeration Handbook. American Society of Heating, Refrigerating and Air-Conditioning Engineers.
    
    """)

# ===== TAB 3: PENGOLAHAN =====
with tab_processing:
    st.header("⚙️ Teknologi Pengolahan")
    
    st.markdown("""
    ### Tujuan Pengolahan
    
    **Pengolahan** adalah proses **mengubah produk segar** menjadi **produk olahan** untuk **memperpanjang shelf-life** dan **menambah nilai**.
    
    **Tujuan:**
    - ✅ Perpanjang shelf-life (bulan-tahun)
    - ✅ Kurangi kehilangan (losses)
    - ✅ Tambah nilai (value addition)
    - ✅ Diversifikasi produk
    - ✅ Stabilkan harga
    
    **Referensi:**
    - Fellows, P. J. (2009). Food Processing Technology, 3rd Edition. Woodhead Publishing.
    
    ---
    
    ## 🌞 PENGERINGAN (DRYING)
    
    ### **Prinsip:**
    ```
    Kurangi kadar air → Aktivitas air (aw) ↓
    → Mikroba tidak bisa tumbuh → Shelf-life ↑
    ```
    
    **Target Kadar Air:**
    - Buah kering: 15-20%
    - Sayuran kering: 4-8%
    - Rempah: 8-12%
    
    ---
    
    ### **Metode Pengeringan:**
    
    ### **1. SUN DRYING (Penjemuran)**
    
    **Prinsip:**
    ```
    Sinar matahari → Panas → Air menguap
    ```
    
    **Keuntungan:**
    ```
    ✅ Murah (no cost)
    ✅ Mudah (low-tech)
    ✅ Cocok untuk petani kecil
    ```
    
    **Kekurangan:**
    ```
    ❌ Lambat (2-7 hari)
    ❌ Tergantung cuaca
    ❌ Kontaminasi (debu, serangga)
    ❌ Kualitas tidak konsisten
    ```
    
    **Protokol:**
    ```
    1. Cuci bersih produk
    2. Potong tipis (3-5 mm) untuk percepat
    3. Blanching (optional, untuk sayuran)
    4. Jemur di atas para-para/nampan
    5. Tutup dengan kain kasa (cegah serangga)
    6. Balik setiap 2-3 jam
    7. Jemur 2-7 hari (tergantung produk)
    8. Simpan dalam wadah kedap udara
    
    Cocok untuk: Cabai, ikan asin, kerupuk
    ```
    
    ---
    
    ### **2. OVEN DRYING (Pengering Oven)**
    
    **Prinsip:**
    ```
    Panas terkontrol (40-70°C) → Air menguap
    ```
    
    **Keuntungan:**
    ```
    ✅ Cepat (6-24 jam)
    ✅ Terkontrol (suhu, waktu)
    ✅ Tidak tergantung cuaca
    ✅ Kualitas baik
    ```
    
    **Kekurangan:**
    ```
    ❌ Biaya energi
    ❌ Investasi awal
    ```
    
    **Protokol:**
    ```
    1. Persiapan produk (cuci, potong)
    2. Blanching (untuk sayuran)
    3. Atur suhu:
       - Buah: 50-60°C
       - Sayuran: 50-70°C
       - Rempah: 40-50°C
    4. Keringkan 6-24 jam
    5. Cek kadar air (target tercapai)
    6. Dinginkan, simpan
    
    Cocok untuk: Buah kering, sayuran kering, rempah
    ```
    
    ---
    
    ### **3. FREEZE DRYING (Pengeringan Beku)**
    
    **Prinsip:**
    ```
    Beku (-40°C) → Vakum → Es langsung jadi uap (sublimasi)
    → Produk kering tanpa panas
    ```
    
    **Keuntungan:**
    ```
    ✅ Kualitas TERBAIK (warna, rasa, nutrisi)
    ✅ Rehydrasi cepat
    ✅ Shelf-life sangat panjang (tahun)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi sangat tinggi
    ❌ Biaya operasional tinggi
    ❌ Kompleks
    ```
    
    **Cocok untuk:**
    - Produk premium (kopi instan, buah kering premium)
    - Farmasi, nutraceuticals
    
    ---
    
    ## 🥫 PENGALENGAN (CANNING)
    
    ### **Prinsip:**
    ```
    Panas tinggi (100-121°C) → Bunuh mikroba
    → Seal kedap udara → Shelf-life panjang
    ```
    
    **Jenis:**
    
    ### **1. Water Bath Canning**
    
    **Kondisi:**
    ```
    - Suhu: 100°C (air mendidih)
    - Waktu: 10-90 menit
    - Cocok untuk: Produk asam (pH < 4.6)
    ```
    
    **Produk:**
    - Buah kalengan (nanas, leci)
    - Selai, jelly
    - Pickles (acar)
    - Saus tomat
    
    **Protokol:**
    ```
    1. Persiapan produk (cuci, kupas, potong)
    2. Blanching (jika perlu)
    3. Isi dalam jar/kaleng steril
    4. Tambahkan sirup/brine
    5. Tutup (headspace 1 cm)
    6. Proses dalam air mendidih (10-90 menit)
    7. Dinginkan
    8. Cek seal (tutup cekung)
    9. Label, simpan
    
    Shelf-life: 1-2 tahun
    ```
    
    ---
    
    ### **2. Pressure Canning**
    
    **Kondisi:**
    ```
    - Suhu: 116-121°C (pressure cooker)
    - Tekanan: 10-15 psi
    - Waktu: 20-90 menit
    - Cocok untuk: Produk non-asam (pH > 4.6)
    ```
    
    **Produk:**
    - Sayuran kalengan (jagung, kacang)
    - Daging kalengan
    - Sup, stew
    
    **PENTING:**
    ```
    ⚠️ Produk non-asam HARUS pressure canning!
    ⚠️ Water bath TIDAK cukup (risiko botulism)
    ⚠️ Ikuti waktu & suhu yang tepat
    ```
    
    ---
    
    ## ❄️ PEMBEKUAN (FREEZING)
    
    ### **Prinsip:**
    ```
    Suhu ≤ -18°C → Aktivitas mikroba & enzim STOP
    → Shelf-life panjang
    ```
    
    **Keuntungan:**
    ```
    ✅ Kualitas sangat baik (warna, rasa, nutrisi)
    ✅ Shelf-life panjang (6-12 bulan)
    ✅ Mudah
    ```
    
    **Kekurangan:**
    ```
    ❌ Perlu freezer (biaya listrik)
    ❌ Tekstur berubah (untuk beberapa produk)
    ❌ Tidak bisa untuk semua produk
    ```
    
    ---
    
    ### **Metode Pembekuan:**
    
    ### **1. Slow Freezing (Freezer Rumah)**
    
    **Kondisi:**
    ```
    - Suhu: -18 sampai -24°C
    - Waktu: 3-24 jam
    ```
    
    **Karakteristik:**
    ```
    - Kristal es besar → Pecah sel → Tekstur lembek
    - Cocok untuk: Produk yang akan dimasak lagi
    ```
    
    ---
    
    ### **2. Quick Freezing (Blast Freezer)**
    
    **Kondisi:**
    ```
    - Suhu: -30 sampai -40°C
    - Waktu: 15-60 menit
    ```
    
    **Karakteristik:**
    ```
    - Kristal es kecil → Minimal kerusakan sel
    - Kualitas TERBAIK
    - Cocok untuk: Produk premium, export
    ```
    
    ---
    
    ### **Protokol Pembekuan:**
    
    ```
    1. PERSIAPAN:
       - Pilih produk segar, kualitas baik
       - Cuci bersih
    
    2. BLANCHING (untuk sayuran):
       - Rebus air mendidih
       - Celup sayuran 1-3 menit
       - Langsung celup air es
       - Tiriskan
       
       Tujuan: Inaktivasi enzim (cegah perubahan warna/rasa)
    
    3. PACKAGING:
       - Plastik freezer bag (kedap udara)
       - Buang udara (vacuum jika ada)
       - Label (nama, tanggal)
    
    4. FREEZING:
       - Masukkan freezer (-18°C atau lebih rendah)
       - Jangan tumpuk terlalu banyak (airflow)
    
    5. STORAGE:
       - Suhu: -18°C atau lebih rendah
       - Shelf-life: 6-12 bulan
    
    Cocok untuk: Sayuran, buah, daging, ikan
    ```
    
    ---
    
    ## 🍯 FERMENTASI
    
    ### **Prinsip:**
    ```
    Mikroba (bakteri, ragi) → Fermentasi
    → Produk baru (asam, alkohol, CO₂)
    → Pengawetan + flavor
    ```
    
    **Jenis Fermentasi:**
    
    ### **1. Fermentasi Asam Laktat**
    
    **Proses:**
    ```
    Gula → Bakteri asam laktat → Asam laktat
    → pH ↓ → Pengawetan
    ```
    
    **Produk:**
    - Acar (pickles)
    - Kimchi
    - Sauerkraut
    - Yogurt
    
    **Protokol Acar:**
    ```
    1. Cuci sayuran (timun, wortel, dll)
    2. Potong sesuai selera
    3. Buat brine:
       - Air: 1 liter
       - Garam: 30-50 gram (3-5%)
       - Gula: 20 gram (optional)
       - Rempah: sesuai selera
    4. Masukkan sayuran dalam jar
    5. Tuang brine (terendam semua)
    6. Tutup (tidak kedap udara, CO₂ harus keluar)
    7. Fermentasi 3-7 hari (suhu ruang)
    8. Cek rasa (asam)
    9. Simpan di kulkas (stop fermentasi)
    
    Shelf-life: 3-6 bulan (kulkas)
    ```
    
    ---
    
    ### **2. Fermentasi Alkohol**
    
    **Proses:**
    ```
    Gula → Ragi → Etanol + CO₂
    ```
    
    **Produk:**
    - Wine (anggur)
    - Cider (apel)
    - Beer
    - Tape (singkong, ketan)
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Fellows, P. J. (2009).** Food Processing Technology, 3rd Edition. Woodhead Publishing.
    
    2. **Rahman, M. S. (2007).** Handbook of Food Preservation, 2nd Edition. CRC Press.
    
    3. **Brennan, J. G. (2006).** Food Processing Handbook. Wiley-VCH.
    
    """)

# ===== TAB 4: KONTROL KUALITAS =====
with tab_quality:
    st.header("✅ Kontrol Kualitas")
    
    st.markdown("""
    ### Definisi Kualitas
    
    **Kualitas** adalah **tingkat kesempurnaan** produk yang memenuhi **standar** dan **ekspektasi konsumen**.
    
    **Aspek Kualitas:**
    - ✅ Appearance (penampilan)
    - ✅ Texture (tekstur)
    - ✅ Flavor (rasa & aroma)
    - ✅ Nutritional value (nilai gizi)
    - ✅ Safety (keamanan)
    
    **Referensi:**
    - Shewfelt, R. L., & Bruckner, B. (2000). Fruit and Vegetable Quality. CRC Press.
    
    ---
    
    ## 📏 GRADING (PENGGOLONGAN)
    
    ### **Tujuan:**
    ```
    - Seragamkan kualitas
    - Tentukan harga
    - Penuhi standar pasar
    - Fasilitasi perdagangan
    ```
    
    ### **Parameter Grading:**
    
    ### **1. UKURAN (Size)**
    
    **Metode:**
    ```
    - Diameter (mm/cm)
    - Berat (gram/kg)
    - Panjang (cm)
    ```
    
    **Contoh (Tomat):**
    ```
    - Extra Large (XL): > 80 mm
    - Large (L): 70-80 mm
    - Medium (M): 60-70 mm
    - Small (S): 50-60 mm
    ```
    
    ---
    
    ### **2. WARNA (Color)**
    
    **Metode:**
    ```
    - Visual (color chart)
    - Colorimeter (L*, a*, b*)
    ```
    
    **Contoh (Tomat):**
    ```
    - Green: Hijau penuh
    - Breaker: Mulai berubah
    - Turning: 10-30% merah
    - Pink: 30-60% merah
    - Light Red: 60-90% merah
    - Red: > 90% merah
    ```
    
    ---
    
    ### **3. KERUSAKAN (Defects)**
    
    **Jenis Kerusakan:**
    
    **A. Minor Defects (Cacat Ringan):**
    ```
    - Goresan kecil
    - Bentuk sedikit tidak normal
    - Warna tidak seragam
    
    Toleransi: 10-20% (tergantung grade)
    ```
    
    **B. Major Defects (Cacat Berat):**
    ```
    - Memar besar
    - Busuk
    - Serangga
    - Penyakit
    
    Toleransi: 0-5% (tergantung grade)
    ```
    
    ---
    
    ### **Sistem Grading:**
    
    **GRADE A (Premium):**
    ```
    - Ukuran: Seragam, besar
    - Warna: Optimal, seragam
    - Bentuk: Normal, menarik
    - Defects: Minimal (< 5% minor, 0% major)
    - Harga: Tertinggi (100%)
    
    Target: Export, supermarket premium
    ```
    
    **GRADE B (Standard):**
    ```
    - Ukuran: Cukup seragam
    - Warna: Baik
    - Bentuk: Cukup normal
    - Defects: Sedang (10-15% minor, < 5% major)
    - Harga: Sedang (70-80%)
    
    Target: Pasar lokal, supermarket
    ```
    
    **GRADE C (Processing):**
    ```
    - Ukuran: Tidak seragam
    - Warna: Bervariasi
    - Bentuk: Tidak normal
    - Defects: Tinggi (> 20% minor, 5-10% major)
    - Harga: Rendah (40-50%)
    
    Target: Industri pengolahan (saus, jus)
    ```
    
    **REJECT (Tolak):**
    ```
    - Busuk, penyakit
    - Kerusakan berat
    - Tidak layak konsumsi
    
    Tindakan: Buang atau kompos
    ```
    
    ---
    
    ## 🔬 PENGUJIAN KUALITAS (QUALITY TESTING)
    
    ### **1. UJI FISIK**
    
    **A. Kekerasan (Firmness):**
    ```
    Alat: Penetrometer
    Satuan: Newton (N) atau kg/cm²
    
    Contoh (Apel):
    - Keras: > 70 N
    - Sedang: 50-70 N
    - Lunak: < 50 N
    ```
    
    **B. Warna:**
    ```
    Alat: Colorimeter
    Parameter: L* (lightness), a* (red-green), b* (yellow-blue)
    ```
    
    **C. Ukuran & Berat:**
    ```
    Alat: Caliper, timbangan
    ```
    
    ---
    
    ### **2. UJI KIMIA**
    
    **A. Total Soluble Solids (TSS/°Brix):**
    ```
    Alat: Refractometer
    Satuan: °Brix (% gula)
    
    Contoh:
    - Mangga matang: 12-18°Brix
    - Jeruk: 10-14°Brix
    - Tomat: 4-6°Brix
    ```
    
    **B. Titratable Acidity (TA):**
    ```
    Metode: Titrasi dengan NaOH
    Satuan: % asam (citric, malic, dll)
    
    Contoh:
    - Jeruk: 0.8-1.5% citric acid
    - Apel: 0.3-0.8% malic acid
    ```
    
    **C. TSS/TA Ratio:**
    ```
    Indikator: Keseimbangan manis-asam
    
    Optimal:
    - Jeruk: 8-12
    - Apel: 15-25
    - Mangga: 20-30
    ```
    
    **D. Kadar Air:**
    ```
    Metode: Oven drying (105°C, 24 jam)
    Atau: Moisture meter
    
    Contoh:
    - Padi: 14% (aman simpan)
    - Buah kering: 15-20%
    - Sayuran kering: 4-8%
    ```
    
    ---
    
    ### **3. UJI MIKROBIOLOGI**
    
    **Parameter:**
    
    **A. Total Plate Count (TPC):**
    ```
    Indikator: Total bakteri
    Satuan: CFU/g (Colony Forming Units)
    
    Standar (buah segar):
    - Baik: < 10⁴ CFU/g
    - Cukup: 10⁴-10⁵ CFU/g
    - Buruk: > 10⁵ CFU/g
    ```
    
    **B. Coliform:**
    ```
    Indikator: Kontaminasi fecal
    
    Standar: < 10 MPN/g (Most Probable Number)
    ```
    
    **C. E. coli:**
    ```
    Indikator: Kontaminasi fecal langsung
    
    Standar: Negatif (0/g)
    ```
    
    **D. Salmonella:**
    ```
    Patogen berbahaya
    
    Standar: Negatif (0/25g)
    ```
    
    ---
    
    ## 📋 STANDAR KUALITAS
    
    ### **Standar Internasional:**
    
    **1. CODEX ALIMENTARIUS:**
    ```
    - Standar FAO/WHO
    - Berlaku internasional
    - Mencakup: Kualitas, keamanan, labeling
    ```
    
    **2. ISO (International Organization for Standardization):**
    ```
    - ISO 22000: Food Safety Management
    - ISO 9001: Quality Management
    ```
    
    **3. GlobalGAP:**
    ```
    - Good Agricultural Practices
    - Untuk produk segar (buah, sayur)
    - Sertifikasi untuk export
    ```
    
    ---
    
    ### **Standar Nasional (Indonesia):**
    
    **1. SNI (Standar Nasional Indonesia):**
    ```
    Contoh:
    - SNI 3166: Beras
    - SNI 01-3553: Air minum
    - SNI 01-2891: Cara uji makanan
    ```
    
    **2. BPOM (Badan POM):**
    ```
    - Registrasi produk olahan
    - Sertifikasi keamanan pangan
    - Label nutrisi
    ```
    
    ---
    
    ## 🎯 IMPLEMENTASI KONTROL KUALITAS
    
    ### **1. SORTASI (Sorting)**
    
    **Tujuan:**
    ```
    Pisahkan produk berdasarkan kualitas
    ```
    
    **Metode:**
    
    **A. Manual:**
    ```
    - Pekerja memilah satu per satu
    - Berdasarkan visual, touch
    - Cocok untuk: Skala kecil, produk lunak
    ```
    
    **B. Mekanis:**
    ```
    - Conveyor belt + sensor
    - Berdasarkan: Ukuran, warna, berat
    - Cocok untuk: Skala besar, produk keras
    ```
    
    ---
    
    ### **2. GRADING (Penggolongan)**
    
    **Protokol:**
    ```
    1. Tentukan parameter (ukuran, warna, defects)
    2. Buat standar grade (A, B, C)
    3. Training pekerja
    4. Sortasi & grading
    5. Labeling (grade, tanggal, asal)
    6. Packing terpisah per grade
    ```
    
    ---
    
    ### **3. SAMPLING & TESTING**
    
    **Protokol:**
    ```
    1. SAMPLING:
       - Random sampling
       - Ukuran sample: 5-10% dari batch
       - Atau: Statistik (n = √N)
    
    2. TESTING:
       - Fisik: Firmness, warna, ukuran
       - Kimia: Brix, TA, kadar air
       - Mikrobiologi: TPC, coliform (jika perlu)
    
    3. EVALUASI:
       - Bandingkan dengan standar
       - Accept/Reject batch
    
    4. DOKUMENTASI:
       - Catat hasil
       - Traceability
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Shewfelt, R. L., & Bruckner, B. (2000).** Fruit and Vegetable Quality. CRC Press.
    
    2. **FAO/WHO. (2020).** Codex Alimentarius. FAO, Rome.
    
    3. **ISO 22000:2018.** Food Safety Management Systems. International Organization for Standardization.
    
    """)

# ===== TAB 5: PRODUK NILAI TAMBAH =====
with tab_value:
    st.header("💎 Produk Nilai Tambah")
    
    st.markdown("""
    ### Definisi
    
    **Produk nilai tambah** adalah produk yang **diproses lebih lanjut** dari produk segar untuk **meningkatkan nilai ekonomi**.
    
    **Keuntungan:**
    - ✅ Harga jual lebih tinggi (2-10x)
    - ✅ Shelf-life lebih panjang
    - ✅ Diversifikasi produk
    - ✅ Kurangi kehilangan
    - ✅ Peluang pasar lebih luas
    
    ---
    
    ## 🍓 SELAI & JELLY
    
    ### **Perbedaan:**
    
    **SELAI (Jam):**
    ```
    - Menggunakan buah utuh/potongan
    - Tekstur: Kental dengan potongan buah
    - Contoh: Selai strawberry, nanas
    ```
    
    **JELLY:**
    ```
    - Menggunakan sari buah (tanpa ampas)
    - Tekstur: Jernih, kenyal
    - Contoh: Jelly anggur, apel
    ```
    
    ---
    
    ### **RESEP SELAI STRAWBERRY:**
    
    ```
    BAHAN:
    - Strawberry segar: 1 kg
    - Gula pasir: 600-800 gram (60-80%)
    - Asam sitrat: 2 gram (atau jus lemon 2 sdm)
    - Pectin: 10 gram (optional, untuk kekentalan)
    
    ALAT:
    - Panci stainless steel
    - Sendok kayu
    - Jar steril
    - Termometer
    
    CARA:
    1. Cuci strawberry, buang tangkai
    2. Potong kecil-kecil
    3. Masukkan dalam panci
    4. Tambahkan gula, aduk
    5. Panaskan dengan api sedang
    6. Aduk terus (cegah gosong)
    7. Tambahkan asam sitrat
    8. Masak hingga 104-105°C (atau uji kekentalan)
    9. Angkat, dinginkan sedikit
    10. Tuang dalam jar steril (panas)
    11. Tutup rapat
    12. Balik jar (vacuum seal)
    13. Dinginkan
    
    UJI KEKENTALAN:
    - Teteskan di piring dingin
    - Jika mengental & tidak menyebar → Siap
    
    HASIL:
    - Yield: ~1.2 kg selai
    - Shelf-life: 6-12 bulan (unopened)
    - Harga jual: 3-5x harga buah segar
    ```
    
    ---
    
    ## 🥤 JUS & SIRUP
    
    ### **JUS (Juice):**
    
    **Jenis:**
    
    **A. Fresh Juice (100% buah):**
    ```
    - Tanpa tambahan gula/air
    - Shelf-life: 1-3 hari (kulkas)
    - Harga: Tertinggi
    ```
    
    **B. Juice Drink (25-99% buah):**
    ```
    - Tambahan air, gula
    - Shelf-life: 3-7 hari (kulkas)
    - Harga: Sedang
    ```
    
    **C. Pasteurized Juice:**
    ```
    - Dipanaskan 72°C, 15 detik
    - Shelf-life: 2-4 minggu (kulkas)
    - Kualitas: Baik
    ```
    
    ---
    
    ### **RESEP JUS JERUK PASTEURISASI:**
    
    ```
    BAHAN:
    - Jeruk segar: 2 kg
    - Gula: 100 gram (optional)
    - Asam askorbat (Vit C): 1 gram (antioksidan)
    
    CARA:
    1. Cuci jeruk
    2. Peras (manual atau juicer)
    3. Saring (buang ampas)
    4. Tambahkan gula (jika suka), aduk
    5. Tambahkan asam askorbat
    6. PASTEURISASI:
       - Panaskan 72°C, 15 detik
       - Atau 63°C, 30 menit
    7. Dinginkan cepat (ice bath)
    8. Tuang dalam botol steril
    9. Tutup rapat
    10. Simpan kulkas (4°C)
    
    HASIL:
    - Yield: ~1.2 liter jus
    - Shelf-life: 2-4 minggu (kulkas)
    - Harga jual: 2-3x harga jeruk segar
    ```
    
    ---
    
    ### **SIRUP (Syrup):**
    
    **Karakteristik:**
    ```
    - Konsentrasi gula tinggi (50-70%)
    - Shelf-life: 6-12 bulan
    - Cara pakai: Encerkan dengan air
    ```
    
    **RESEP SIRUP MARKISA:**
    
    ```
    BAHAN:
    - Sari markisa: 500 ml
    - Gula pasir: 1 kg
    - Air: 500 ml
    - Asam sitrat: 2 gram
    - Natrium benzoat: 1 gram (pengawet)
    
    CARA:
    1. Rebus air + gula → Sirup gula
    2. Dinginkan
    3. Campur dengan sari markisa
    4. Tambahkan asam sitrat + natrium benzoat
    5. Aduk rata
    6. Saring
    7. Tuang dalam botol steril
    8. Tutup rapat
    
    HASIL:
    - Yield: ~1.5 liter sirup
    - Shelf-life: 6-12 bulan
    - Cara pakai: 1 bagian sirup + 5-7 bagian air
    ```
    
    ---
    
    ## 🍟 KERIPIK (CHIPS)
    
    ### **Jenis:**
    
    **A. Keripik Goreng:**
    ```
    - Metode: Deep frying (160-180°C)
    - Contoh: Keripik pisang, singkong, kentang
    - Shelf-life: 1-3 bulan
    ```
    
    **B. Keripik Vakum:**
    ```
    - Metode: Vacuum frying (90-120°C, vakum)
    - Keuntungan: Warna cerah, nutrisi terjaga, less oil
    - Contoh: Keripik buah (nanas, apel, nangka)
    - Shelf-life: 3-6 bulan
    ```
    
    ---
    
    ### **RESEP KERIPIK PISANG:**
    
    ```
    BAHAN:
    - Pisang mentah (kepok): 2 kg
    - Minyak goreng: 2 liter
    - Garam: 1 sdm (optional)
    - Kunyit: 1 sdt (untuk warna)
    
    CARA:
    1. Kupas pisang
    2. Iris tipis (1-2 mm) dengan slicer
    3. Rendam air garam + kunyit (10 menit)
    4. Tiriskan, keringkan
    5. Panaskan minyak (160-170°C)
    6. Goreng hingga kuning kecoklatan (5-7 menit)
    7. Tiriskan
    8. Dinginkan
    9. Kemas dalam plastik kedap udara
    
    HASIL:
    - Yield: ~400 gram keripik
    - Shelf-life: 1-3 bulan (kedap udara)
    - Harga jual: 5-8x harga pisang segar
    ```
    
    ---
    
    ## 🥫 PRODUK LAINNYA
    
    ### **1. MANISAN (Candied Fruit):**
    
    ```
    Prinsip: Osmosis (gula tinggi → air keluar)
    
    Contoh: Manisan mangga, kedondong, carica
    
    Protokol:
    1. Potong buah
    2. Blanching
    3. Rendam sirup gula (bertahap, 30% → 70%)
    4. Tiriskan
    5. Jemur/oven (semi-kering)
    6. Kemas
    
    Shelf-life: 3-6 bulan
    ```
    
    ---
    
    ### **2. ACAR (Pickles):**
    
    ```
    Prinsip: Asam (pH rendah) → Pengawetan
    
    Contoh: Acar timun, wortel, cabai
    
    Protokol:
    1. Cuci sayuran
    2. Potong
    3. Buat brine (air + garam + cuka + gula + rempah)
    4. Masukkan sayuran dalam jar
    5. Tuang brine (panas)
    6. Tutup rapat
    7. Pasteurisasi (water bath, 10-15 menit)
    8. Dinginkan
    
    Shelf-life: 6-12 bulan
    ```
    
    ---
    
    ### **3. SAUS (Sauce):**
    
    ```
    Contoh: Saus tomat, saus cabai, saus BBQ
    
    RESEP SAUS TOMAT:
    
    BAHAN:
    - Tomat matang: 2 kg
    - Bawang putih: 50 gram
    - Gula: 200 gram
    - Garam: 20 gram
    - Cuka: 100 ml
    - Rempah: sesuai selera
    
    CARA:
    1. Blender tomat
    2. Masak dengan bawang putih + rempah
    3. Tambahkan gula, garam, cuka
    4. Masak hingga kental (1-2 jam)
    5. Saring (optional, untuk tekstur halus)
    6. Tuang dalam botol steril (panas)
    7. Tutup rapat
    8. Pasteurisasi (water bath, 15 menit)
    
    Shelf-life: 6-12 bulan
    ```
    
    ---
    
    ## 💰 ANALISIS EKONOMI
    
    ### **Contoh: Selai Strawberry**
    
    ```
    BIAYA PRODUKSI (per 1 kg selai):
    
    Bahan Baku:
    - Strawberry: 1 kg × Rp 30,000 = Rp 30,000
    - Gula: 0.7 kg × Rp 15,000 = Rp 10,500
    - Pectin, asam: Rp 2,000
    - Jar + label: Rp 5,000
    - Gas/listrik: Rp 2,000
    - Tenaga kerja: Rp 5,000
    
    TOTAL BIAYA: Rp 54,500
    
    HARGA JUAL:
    - Retail: Rp 80,000-100,000/kg
    - Wholesale: Rp 65,000-75,000/kg
    
    PROFIT MARGIN:
    - Retail: 47-83% (Rp 25,500-45,500/kg)
    - Wholesale: 19-38% (Rp 10,500-20,500/kg)
    
    ROI (Return on Investment):
    - Retail: 47-83%
    - Wholesale: 19-38%
    
    BREAK-EVEN POINT:
    - Jika produksi 100 kg/bulan
    - Fixed cost: Rp 2,000,000 (alat, sewa)
    - BEP: ~40-50 kg/bulan
    ```
    
    **KESIMPULAN:**
    ```
    ✅ Produk nilai tambah SANGAT MENGUNTUNGKAN!
    ✅ Margin 2-10x dari produk segar
    ✅ Shelf-life panjang (fleksibilitas penjualan)
    ✅ Peluang pasar luas (retail, wholesale, export)
    ```
    
    ---
    
    ## 💡 TIPS SUKSES
    
    **1. KUALITAS:**
    ```
    - Gunakan bahan baku berkualitas
    - Sanitasi ketat
    - Konsistensi rasa
    ```
    
    **2. PACKAGING:**
    ```
    - Menarik (label, desain)
    - Informatif (komposisi, expired date, BPOM)
    - Aman (kedap udara, food-grade)
    ```
    
    **3. LEGALITAS:**
    ```
    - Izin PIRT (Pangan Industri Rumah Tangga)
    - Atau BPOM (untuk skala besar)
    - Sertifikat Halal (jika target muslim)
    ```
    
    **4. MARKETING:**
    ```
    - Branding (nama, logo unik)
    - Online (marketplace, sosmed)
    - Offline (toko, bazaar)
    - Sampling (biarkan orang coba)
    ```
    
    **5. INOVASI:**
    ```
    - Varian rasa baru
    - Packaging unik
    - Kolaborasi (gift set)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Fellows, P. J. (2009).** Food Processing Technology, 3rd Edition. Woodhead Publishing.
    
    2. **Arthey, D., & Ashurst, P. R. (1996).** Fruit Processing. Springer.
    
    3. **Hui, Y. H. (2006).** Handbook of Fruits and Fruit Processing. Blackwell Publishing.
    
    """)


