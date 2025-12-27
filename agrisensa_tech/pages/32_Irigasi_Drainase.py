import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Irigasi & Drainase - AgriSensa",
    page_icon="💧",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






# Header
st.title("💧 Irigasi & Manajemen Air Pertanian")
st.markdown("**Sistem Irigasi Modern, Perhitungan Kebutuhan Air, dan Teknologi Jepang untuk Indonesia**")

# Main tabs
tab_systems, tab_calculation, tab_drainage, tab_japanese, tab_tools = st.tabs([
    "🚿 Sistem Irigasi",
    "📊 Perhitungan Kebutuhan Air",
    "🌊 Drainase",
    "🇯🇵 Teknologi Jepang",
    "🛠️ Tools & Calculator"
])

# ===== TAB 1: SISTEM IRIGASI =====
with tab_systems:
    st.header("🚿 Sistem Irigasi Modern")
    
    st.markdown("""
    ### Definisi
    
    **Irigasi** adalah pemberian **air secara teratur** ke lahan pertanian untuk **memenuhi kebutuhan air tanaman** dan **meningkatkan produktivitas**.
    
    **Tujuan:**
    - ✅ Memenuhi kebutuhan air tanaman
    - ✅ Meningkatkan hasil panen
    - ✅ Efisiensi penggunaan air
    - ✅ Mengurangi biaya tenaga kerja
    - ✅ Meningkatkan kualitas produk
    
    **Referensi:**
    - FAO. (2002). Irrigation Manual. FAO, Rome.
    
    ---
    
    ## 💧 SISTEM IRIGASI PERMUKAAN (Surface Irrigation)
    
    ### **1. IRIGASI GENANGAN (Basin/Flood Irrigation)**
    
    **Prinsip:**
    ```
    Air dialirkan ke petak sawah → Digenangkan
    → Meresap ke tanah → Diserap akar
    ```
    
    **Karakteristik:**
    ```
    Kedalaman genangan: 5-10 cm
    Frekuensi: Kontinyu (padi) atau periodik (palawija)
    Efisiensi: 40-60% (banyak kehilangan)
    ```
    
    **Keuntungan:**
    ```
    ✅ Murah (no equipment)
    ✅ Mudah (tradisional)
    ✅ Cocok untuk padi sawah
    ✅ Kontrol gulma (genangan)
    ```
    
    **Kekurangan:**
    ```
    ❌ Efisiensi rendah (evaporasi, perkolasi)
    ❌ Butuh air banyak
    ❌ Perlu lahan datar
    ❌ Kehilangan nutrisi (leaching)
    ```
    
    **Cocok untuk:**
    - Padi sawah
    - Lahan datar
    - Air melimpah
    
    ---
    
    ### **2. IRIGASI ALUR (Furrow Irrigation)**
    
    **Prinsip:**
    ```
    Air dialirkan melalui alur/parit di antara bedengan
    → Meresap ke samping → Diserap akar
    ```
    
    **Dimensi Alur:**
    ```
    Lebar: 30-60 cm
    Kedalaman: 15-30 cm
    Jarak antar alur: 60-100 cm (tergantung tanaman)
    Panjang alur: 50-200 m (tergantung kemiringan)
    ```
    
    **Keuntungan:**
    ```
    ✅ Lebih efisien dari genangan (60-70%)
    ✅ Murah
    ✅ Cocok untuk tanaman baris (jagung, kedelai)
    ✅ Bisa untuk lahan miring (0.5-2%)
    ```
    
    **Kekurangan:**
    ```
    ❌ Distribusi air tidak seragam
    ❌ Butuh tenaga kerja (buat alur)
    ❌ Erosi (jika kemiringan terlalu besar)
    ```
    
    ---
    
    ## 💦 IRIGASI TETES (Drip Irrigation)
    
    ### **Prinsip:**
    
    ```
    Air dialirkan melalui pipa → Dripper (emitter)
    → Tetes langsung ke zona akar
    → Efisiensi SANGAT TINGGI!
    ```
    
    ### **Komponen:**
    
    **1. Sumber Air:**
    ```
    - Sumur, sungai, waduk
    - Tangki penampung (elevated atau dengan pompa)
    ```
    
    **2. Pompa (jika perlu):**
    ```
    - Tekanan: 0.5-2 bar (5-20 m head)
    - Kapasitas: Sesuai kebutuhan (L/jam)
    ```
    
    **3. Filter:**
    ```
    - Screen filter (120-200 mesh)
    - Disk filter
    - Sand filter (untuk air kotor)
    
    PENTING: Cegah penyumbatan dripper!
    ```
    
    **4. Fertilizer Tank (Venturi Injector):**
    ```
    - Untuk fertigation (pupuk cair)
    - Injeksi otomatis saat irigasi
    ```
    
    **5. Mainline & Submain:**
    ```
    - PVC pipe (diameter 1-2 inch)
    - Distribusi air ke lateral
    ```
    
    **6. Lateral Line:**
    ```
    - PE pipe (diameter 12-16 mm)
    - Dengan dripper built-in atau external
    ```
    
    **7. Dripper (Emitter):**
    ```
    - Debit: 1-4 L/jam per dripper
    - Jarak: 20-50 cm (tergantung tanaman)
    - Tipe: Pressure compensating (PC) atau non-PC
    ```
    
    ---
    
    ### **Desain Sistem Drip:**
    
    **Contoh: Tomat 1 Ha**
    
    ```
    PARAMETER:
    - Jarak tanam: 60 cm * 40 cm
    - Populasi: 41,667 tanaman/ha
    - Kebutuhan air: 5 mm/hari = 50 m³/ha/hari
    - Jam operasi: 2 jam/hari
    
    DESAIN:
    1. Lateral spacing: 60 cm (1 lateral per baris)
    2. Dripper spacing: 40 cm (1 dripper per tanaman)
    3. Dripper discharge: 2 L/jam
    4. Jumlah dripper: 41,667
    5. Total debit: 41,667 * 2 = 83,334 L/jam = 83.3 m³/jam
    6. Waktu irigasi: 50 m³ / 83.3 m³/jam = 0.6 jam = 36 menit
    
    BIAYA (Estimasi):
    - Dripper line: Rp 3,000/m * 16,667 m = Rp 50 juta
    - Mainline & fitting: Rp 20 juta
    - Filter & injector: Rp 10 juta
    - Pompa (jika perlu): Rp 15 juta
    - Instalasi: Rp 10 juta
    
    TOTAL: Rp 105 juta/ha
    
    ROI: 2-3 tahun (hemat air 50%, pupuk 30%, tenaga kerja 70%)
    ```
    
    ---
    
    ### **Keuntungan Drip Irrigation:**
    
    ```
    ✅ Efisiensi air SANGAT TINGGI (85-95%)
    ✅ Hemat air 40-70% vs furrow
    ✅ Fertigation (pupuk cair langsung ke akar)
    ✅ Hemat pupuk 30-50%
    ✅ Hemat tenaga kerja (otomatis)
    ✅ Hasil ↑ 20-50% (air & nutrisi optimal)
    ✅ Kualitas ↑ (seragam)
    ✅ Cocok untuk lahan miring
    ✅ Kurangi gulma (area kering tidak ditumbuhi)
    ✅ Kurangi penyakit (daun tidak basah)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi awal tinggi (Rp 80-150 juta/ha)
    ❌ Perlu maintenance (filter, dripper)
    ❌ Risiko penyumbatan (air kotor)
    ❌ Perlu skill (desain, operasi)
    ```
    
    **Cocok untuk:**
    - Sayuran (tomat, cabai, melon)
    - Buah (strawberry, anggur)
    - Greenhouse/polytunnel
    - Lahan kering/miring
    - Air terbatas
    
    ---
    
    ## 🌧️ IRIGASI SPRINKLER (Sprinkler Irrigation)
    
    ### **Prinsip:**
    
    ```
    Air dipompa → Pipa → Sprinkler head
    → Semprotkan seperti hujan
    → Merata di permukaan tanah
    ```
    
    ### **Jenis Sprinkler:**
    
    **1. Fixed Sprinkler (Portable):**
    ```
    - Sprinkler dipasang di pipa portable
    - Dipindah-pindah manual
    - Murah (Rp 20-40 juta/ha)
    - Cocok untuk: Skala kecil, sayuran
    ```
    
    **2. Semi-Permanent:**
    ```
    - Mainline tetap (buried)
    - Lateral portable
    - Sedang (Rp 40-80 juta/ha)
    ```
    
    **3. Permanent (Solid Set):**
    ```
    - Semua pipa tetap (buried)
    - Otomatis (timer/controller)
    - Mahal (Rp 100-200 juta/ha)
    - Cocok untuk: Golf course, landscape
    ```
    
    **4. Center Pivot:**
    ```
    - Lateral berputar mengelilingi pivot
    - Otomatis, skala besar (>10 ha)
    - Sangat mahal (Rp 500 juta - 2 miliar)
    - Cocok untuk: Jagung, gandum (lahan luas)
    ```
    
    ---
    
    ### **Desain Sprinkler:**
    
    **Contoh: Jagung 1 Ha**
    
    ```
    PARAMETER:
    - Kebutuhan air: 6 mm/hari = 60 m³/ha/hari
    - Sprinkler discharge: 500 L/jam
    - Radius coverage: 10 m
    - Spacing: 12 m * 12 m (overlap 20%)
    
    DESAIN:
    1. Jumlah sprinkler: 100 m * 100 m / (12 * 12) = 70 sprinkler
    2. Total debit: 70 * 500 = 35,000 L/jam = 35 m³/jam
    3. Waktu irigasi: 60 m³ / 35 m³/jam = 1.7 jam
    4. Tekanan: 2-3 bar (20-30 m head)
    5. Pompa: 35 m³/jam @ 30 m head = 3.5 HP
    
    BIAYA:
    - Sprinkler head: Rp 200K * 70 = Rp 14 juta
    - Pipa PVC: Rp 15 juta
    - Pompa: Rp 10 juta
    - Instalasi: Rp 6 juta
    
    TOTAL: Rp 45 juta/ha
    ```
    
    ---
    
    ### **Keuntungan Sprinkler:**
    
    ```
    ✅ Efisiensi sedang-tinggi (70-85%)
    ✅ Distribusi merata
    ✅ Cocok untuk lahan miring (hingga 20%)
    ✅ Bisa untuk berbagai tanaman
    ✅ Bisa untuk frost protection (semprot air saat dingin)
    ✅ Lebih murah dari drip (untuk tanaman rapat)
    ```
    
    **Kekurangan:**
    ```
    ❌ Evaporasi tinggi (jika siang hari, angin kencang)
    ❌ Distribusi tidak seragam (jika angin)
    ❌ Basahi daun (risiko penyakit)
    ❌ Butuh tekanan tinggi (pompa besar)
    ```
    
    **Cocok untuk:**
    - Jagung, gandum, kedelai
    - Rumput, landscape
    - Lahan luas
    
    ---
    
    ## 📊 PERBANDINGAN SISTEM IRIGASI
    
    | Sistem | Efisiensi | Investasi | Tenaga Kerja | Cocok untuk | Hemat Air |
    |--------|-----------|-----------|--------------|-------------|-----------|
    | **Genangan** | 40-60% | Sangat murah | Tinggi | Padi sawah | ❌ |
    | **Alur (Furrow)** | 60-70% | Murah | Sedang | Jagung, kedelai | ⚠️ |
    | **Tetes (Drip)** | 85-95% | Mahal | Rendah | Sayuran, buah | ✅✅✅ |
    | **Sprinkler** | 70-85% | Sedang | Rendah | Jagung, rumput | ✅✅ |
    | **Center Pivot** | 75-90% | Sangat mahal | Sangat rendah | Lahan luas | ✅✅ |
    
    ---
    
    ## 💡 TIPS PEMILIHAN SISTEM
    
    **Pilih GENANGAN jika:**
    ```
    ✅ Padi sawah
    ✅ Air melimpah
    ✅ Modal terbatas
    ✅ Lahan datar
    ```
    
    **Pilih DRIP jika:**
    ```
    ✅ Sayuran/buah bernilai tinggi
    ✅ Air terbatas (PENTING!)
    ✅ Ingin hemat pupuk (fertigation)
    ✅ Lahan miring
    ✅ Punya modal (ROI 2-3 tahun)
    ```
    
    **Pilih SPRINKLER jika:**
    ```
    ✅ Tanaman rapat (jagung, gandum)
    ✅ Lahan luas
    ✅ Lahan miring
    ✅ Modal sedang
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **FAO. (2002).** Irrigation Manual. FAO, Rome.
    
    2. **Keller, J., & Bliesner, R. D. (1990).** Sprinkle and Trickle Irrigation. Van Nostrand Reinhold.
    
    3. **Nakayama, F. S., & Bucks, D. A. (1986).** Trickle Irrigation for Crop Production. Elsevier.
    
    """)

# ===== TAB 2: PERHITUNGAN KEBUTUHAN AIR =====
with tab_calculation:
    st.header("📊 Perhitungan Kebutuhan Air Tanaman")
    
    st.markdown("""
    ### Konsep Dasar
    
    **Evapotranspirasi (ET)** = **Evaporasi** (penguapan dari tanah) + **Transpirasi** (penguapan dari tanaman)
    
    ```
    ET = Evaporasi + Transpirasi
    
    ET tanaman (ETc) = ET0 * Kc
    
    Dimana:
    - ET0 = Evapotranspirasi referensi (mm/hari)
    - Kc = Koefisien tanaman (crop coefficient)
    ```
    
    ---
    
    ## 🌤️ EVAPOTRANSPIRASI REFERENSI (ET0)
    
    ### **Metode Penman-Monteith (FAO-56)**
    
    **Formula:**
    ```
    ET0 = (0.408 Δ (Rn - G) + γ (900/(T+273)) u2 (es - ea)) / (Δ + γ (1 + 0.34 u2))
    
    Dimana:
    - Rn = Net radiation (MJ/m²/hari)
    - G = Soil heat flux (MJ/m²/hari) ≈ 0 (harian)
    - T = Suhu rata-rata (°C)
    - u2 = Kecepatan angin 2 m (m/s)
    - es = Tekanan uap jenuh (kPa)
    - ea = Tekanan uap aktual (kPa)
    - Δ = Slope vapor pressure curve (kPa/°C)
    - γ = Psychrometric constant (kPa/°C)
    ```
    
    **Data yang Dibutuhkan:**
    - Suhu min & max (°C)
    - Kelembaban relatif (%)
    - Kecepatan angin (m/s)
    - Radiasi matahari (MJ/m²/hari) atau sunshine hours
    - Lokasi (latitude, altitude)
    
    **Referensi:**
    - Allen, R. G., et al. (1998). Crop Evapotranspiration. FAO Irrigation and Drainage Paper 56.
    
    ---
    
    ### **Metode Sederhana (Blaney-Criddle)**
    
    **Jika data terbatas:**
    ```
    ET0 = p * (0.46 T + 8)
    
    Dimana:
    - p = Persentase jam siang dari total tahunan (tergantung latitude & bulan)
    - T = Suhu rata-rata (°C)
    ```
    
    **Contoh:**
    ```
    Lokasi: Jakarta (6°S)
    Bulan: Januari
    Suhu rata-rata: 27°C
    p = 0.27 (dari tabel FAO)
    
    ET0 = 0.27 * (0.46 * 27 + 8)
        = 0.27 * 20.42
        = 5.5 mm/hari
    ```
    
    ---
    
    ### **Nilai ET0 Tipikal Indonesia:**
    
    | Lokasi | ET0 (mm/hari) | Keterangan |
    |--------|---------------|------------|
    | **Dataran rendah (0-500 m)** | 4-6 | Panas, kelembaban tinggi |
    | **Dataran sedang (500-1000 m)** | 3-5 | Sedang |
    | **Dataran tinggi (>1000 m)** | 2-4 | Sejuk |
    | **Musim kemarau** | 5-7 | Radiasi tinggi, RH rendah |
    | **Musim hujan** | 3-5 | Radiasi rendah, RH tinggi |
    
    ---
    
    ## 🌾 KOEFISIEN TANAMAN (Kc)
    
    ### **Konsep:**
    
    ```
    Kc = ETc / ET0
    
    Kc bervariasi tergantung:
    - Jenis tanaman
    - Fase pertumbuhan
    - Iklim
    ```
    
    ### **Fase Pertumbuhan:**
    
    **1. Initial (Awal):**
    ```
    - Dari tanam sampai 10% tutupan kanopi
    - Kc rendah (0.3-0.5)
    - Evaporasi > Transpirasi
    ```
    
    **2. Development (Perkembangan):**
    ```
    - 10% sampai 70-80% tutupan kanopi
    - Kc meningkat (0.5-1.0)
    ```
    
    **3. Mid-season (Pertengahan):**
    ```
    - Tutupan penuh sampai awal pematangan
    - Kc maksimum (1.0-1.3)
    - Transpirasi maksimum
    ```
    
    **4. Late-season (Akhir):**
    ```
    - Pematangan sampai panen
    - Kc menurun (0.6-0.9)
    - Tanaman mulai mengering
    ```
    
    ---
    
    ### **Nilai Kc untuk Berbagai Tanaman:**
    
    **PADI:**
    ```
    Initial (0-20 hari): Kc = 1.05 (genangan)
    Development (20-40 hari): Kc = 1.10
    Mid-season (40-90 hari): Kc = 1.20
    Late-season (90-120 hari): Kc = 0.90
    
    Rata-rata: Kc = 1.05
    ```
    
    **JAGUNG:**
    ```
    Initial (0-20 hari): Kc = 0.30
    Development (20-50 hari): Kc = 0.70
    Mid-season (50-90 hari): Kc = 1.20
    Late-season (90-110 hari): Kc = 0.60
    
    Rata-rata: Kc = 0.80
    ```
    
    **TOMAT:**
    ```
    Initial (0-25 hari): Kc = 0.60
    Development (25-40 hari): Kc = 0.85
    Mid-season (40-80 hari): Kc = 1.15
    Late-season (80-110 hari): Kc = 0.80
    
    Rata-rata: Kc = 0.90
    ```
    
    **CABAI:**
    ```
    Initial (0-30 hari): Kc = 0.60
    Development (30-50 hari): Kc = 0.90
    Mid-season (50-100 hari): Kc = 1.05
    Late-season (100-120 hari): Kc = 0.90
    
    Rata-rata: Kc = 0.90
    ```
    
    **KEDELAI:**
    ```
    Initial (0-20 hari): Kc = 0.40
    Development (20-35 hari): Kc = 0.70
    Mid-season (35-75 hari): Kc = 1.15
    Late-season (75-95 hari): Kc = 0.50
    
    Rata-rata: Kc = 0.75
    ```
    
    ---
    
    ## 💧 PERHITUNGAN KEBUTUHAN AIR IRIGASI
    
    ### **Formula:**
    
    ```
    ETc = ET0 * Kc
    
    Kebutuhan Air Irigasi (mm/hari) = ETc - Pe + LR
    
    Dimana:
    - ETc = Evapotranspirasi tanaman (mm/hari)
    - Pe = Curah hujan efektif (mm/hari)
    - LR = Leaching requirement (mm/hari) - untuk salinitas
    ```
    
    ### **Curah Hujan Efektif (Pe):**
    
    ```
    Pe = 0.8 * P - 25  (jika P > 75 mm/bulan)
    Pe = 0.6 * P       (jika P < 75 mm/bulan)
    
    Dimana P = Curah hujan total (mm/bulan)
    ```
    
    ---
    
    ### **Contoh Perhitungan:**
    
    **Kasus: Tomat di Bogor (Musim Kemarau)**
    
    ```
    DATA:
    - ET0 = 5 mm/hari (dataran rendah, musim kemarau)
    - Fase: Mid-season (hari ke-50)
    - Kc = 1.15
    - Curah hujan: 50 mm/bulan = 1.7 mm/hari
    - Efisiensi irigasi: 85% (drip)
    
    PERHITUNGAN:
    1. ETc = ET0 * Kc
         = 5 * 1.15
         = 5.75 mm/hari
    
    2. Pe = 0.6 * 1.7 = 1.0 mm/hari
    
    3. Kebutuhan air netto = ETc - Pe
                            = 5.75 - 1.0
                            = 4.75 mm/hari
    
    4. Kebutuhan air kotor = 4.75 / 0.85
                           = 5.6 mm/hari
                           = 56 m³/ha/hari
    
    5. Jika irigasi 2 jam/hari:
       Debit = 56 m³/ha / 2 jam
             = 28 m³/ha/jam
             = 28,000 L/ha/jam
    
    6. Jika 40,000 tanaman/ha, 1 dripper/tanaman, 2 L/jam:
       Total debit = 40,000 * 2 = 80,000 L/jam
       Waktu irigasi = 28,000 / 80,000 = 0.35 jam = 21 menit
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Allen, R. G., et al. (1998).** Crop Evapotranspiration - Guidelines for computing crop water requirements. FAO Irrigation and Drainage Paper 56.
    
    2. **Doorenbos, J., & Pruitt, W. O. (1977).** Crop water requirements. FAO Irrigation and Drainage Paper 24.
    
    """)

# ===== TAB 3: DRAINASE =====
with tab_drainage:
    st.header("🌊 Sistem Drainase Pertanian")
    
    st.markdown("""
    ### Definisi
    
    **Drainase** adalah **pembuangan kelebihan air** dari lahan pertanian untuk **mencegah genangan** dan **menjaga aerasi tanah**.
    
    **Tujuan:**
    - ✅ Cegah genangan (waterlogging)
    - ✅ Jaga aerasi akar (oksigen)
    - ✅ Kurangi salinitas (leaching)
    - ✅ Perpanjang musim tanam
    - ✅ Tingkatkan produktivitas
    
    ---
    
    ## 🚿 JENIS DRAINASE
    
    ### **1. DRAINASE PERMUKAAN (Surface Drainage)**
    
    **Prinsip:**
    ```
    Air limpasan dialirkan melalui saluran terbuka
    → Ke outlet (sungai, laut)
    ```
    
    **Komponen:**
    
    **A. Parit Lapangan (Field Ditch):**
    ```
    - Kedalaman: 30-60 cm
    - Lebar atas: 60-100 cm
    - Lebar bawah: 30-50 cm
    - Jarak: 50-200 m (tergantung kemiringan & tanah)
    - Kemiringan: 0.1-0.5%
    ```
    
    **B. Parit Pengumpul (Collector Drain):**
    ```
    - Kedalaman: 60-100 cm
    - Lebar: 100-200 cm
    - Kemiringan: 0.1-0.3%
    ```
    
    **C. Saluran Utama (Main Drain):**
    ```
    - Kedalaman: 1-2 m
    - Lebar: 2-5 m
    - Kemiringan: 0.05-0.2%
    ```
    
    **Keuntungan:**
    ```
    ✅ Murah (manual excavation)
    ✅ Mudah maintenance
    ✅ Cocok untuk lahan datar
    ```
    
    **Kekurangan:**
    ```
    ❌ Kurangi luas tanam (parit ambil lahan)
    ❌ Perlu maintenance rutin (sedimen, gulma)
    ❌ Tidak efektif untuk tanah berat (clay)
    ```
    
    ---
    
    ### **2. DRAINASE BAWAH TANAH (Subsurface Drainage)**
    
    **Prinsip:**
    ```
    Pipa berlubang ditanam di bawah tanah
    → Air tanah masuk pipa → Dialirkan ke outlet
    ```
    
    **Komponen:**
    
    **A. Pipa Lateral:**
    ```
    - Material: PVC perforated, corrugated HDPE
    - Diameter: 75-150 mm
    - Kedalaman: 80-120 cm
    - Jarak: 10-30 m (tergantung tanah)
    - Kemiringan: 0.1-0.3%
    ```
    
    **B. Pipa Pengumpul:**
    ```
    - Diameter: 150-300 mm
    - Kedalaman: 100-150 cm
    ```
    
    **C. Envelope (Filter):**
    ```
    - Gravel (kerikil) atau geotextile
    - Cegah penyumbatan pipa
    ```
    
    **Desain:**
    
    **Jarak Pipa (Spacing):**
    ```
    Hooghoudt Equation:
    
    L = √(8 K d h + 4 K h²) / q
    
    Dimana:
    - L = Jarak antar pipa (m)
    - K = Hydraulic conductivity (m/hari)
    - d = Equivalent depth (m)
    - h = Water table height (m)
    - q = Drainage rate (m/hari)
    
    Nilai Tipikal:
    - Tanah pasir (K = 1-5 m/hari): L = 20-30 m
    - Tanah lempung (K = 0.1-0.5 m/hari): L = 10-15 m
    - Tanah liat (K = 0.01-0.1 m/hari): L = 5-10 m
    ```
    
    **Biaya:**
    ```
    - Pipa PVC: Rp 50-100K/m
    - Gravel: Rp 200K/m³
    - Excavation: Rp 50K/m
    - Instalasi: Rp 30-50 juta/ha
    
    TOTAL: Rp 80-150 juta/ha
    
    Lifetime: 30-50 tahun
    ```
    
    **Keuntungan:**
    ```
    ✅ Tidak kurangi luas tanam
    ✅ Efektif untuk tanah berat
    ✅ Maintenance minimal
    ✅ Jangka panjang (30-50 tahun)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi tinggi
    ❌ Perlu skill (desain, instalasi)
    ❌ Sulit perbaikan (jika rusak)
    ```
    
    ---
    
    ## 📊 KRITERIA DRAINASE
    
    ### **Kedalaman Water Table:**
    
    | Tanaman | Kedalaman Min (cm) | Keterangan |
    |---------|-------------------|------------|
    | **Padi sawah** | 0-10 | Toleran genangan |
    | **Jagung** | 40-60 | Sensitif genangan |
    | **Kedelai** | 40-60 | Sensitif genangan |
    | **Sayuran** | 50-80 | Sangat sensitif |
    | **Buah (pohon)** | 80-120 | Akar dalam |
    
    ### **Drainage Coefficient:**
    
    ```
    Drainage rate (mm/hari) = Curah hujan 24 jam / Waktu drainase
    
    Contoh:
    - Curah hujan ekstrem: 100 mm/24 jam
    - Target: Drainase dalam 24 jam
    - Drainage rate = 100 / 24 = 4.2 mm/hari
    ```
    
    ---
    
    ## 💡 TIPS DRAINASE
    
    **1. Survey Lahan:**
    ```
    - Topografi (kemiringan, low spot)
    - Jenis tanah (tekstur, permeabilitas)
    - Water table (kedalaman, fluktuasi)
    - Outlet (sungai, laut)
    ```
    
    **2. Kombinasi Sistem:**
    ```
    - Surface drainage untuk hujan ekstrem
    - Subsurface drainage untuk water table
    ```
    
    **3. Maintenance:**
    ```
    - Bersihkan parit (sedimen, gulma)
    - Cek pipa (penyumbatan)
    - Perbaiki erosi
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **FAO. (1985).** Water Quality for Agriculture. FAO Irrigation and Drainage Paper 29.
    
    2. **Skaggs, R. W., et al. (2012).** Agricultural Drainage. ASA-CSSA-SSSA.
    
    """)

# ===== TAB 4: TEKNOLOGI JEPANG =====
with tab_japanese:
    st.header("🇯🇵 Teknologi Manajemen Air Gaya Jepang")
    
    st.markdown("""
    ### Filosofi Jepang: "Mizu wa Inochi" (水は命)
    
    **"Air adalah Kehidupan"**
    
    Jepang memiliki **budaya manajemen air** yang sangat maju, dikembangkan selama **ribuan tahun** untuk:
    - ✅ Efisiensi maksimal (air terbatas di pulau)
    - ✅ Kualitas tinggi (beras premium)
    - ✅ Keberlanjutan (generasi mendatang)
    - ✅ Harmoni dengan alam
    
    ---
    
    ## 🌾 SISTEM SAWAH JEPANG (Paddy Field System)
    
    ### **1. ROTASI SAWAH-LAHAN KERING (Paddy-Upland Rotation)**
    
    **Konsep:**
    ```
    Rotasi antara padi sawah (genangan) dan tanaman lahan kering
    → Perbaiki struktur tanah
    → Kurangi hama & penyakit
    → Tingkatkan produktivitas
    ```
    
    **Pola Rotasi:**
    
    **Tahun 1-2: PADI SAWAH**
    ```
    - Genangan 5-10 cm
    - 2x panen/tahun (musim panas + musim dingin)
    - Varietas: Koshihikari, Sasanishiki (premium)
    ```
    
    **Tahun 3: LAHAN KERING (Upland)**
    ```
    - Drainase total (kering)
    - Tanaman: Gandum, kedelai, sayuran
    - Perbaiki aerasi tanah
    - Putus siklus hama padi
    ```
    
    **Tahun 4-5: PADI SAWAH**
    ```
    - Kembali ke genangan
    - Produktivitas meningkat 10-20%!
    ```
    
    **Keuntungan:**
    ```
    ✅ Hasil padi ↑ 10-20% (setelah rotasi)
    ✅ Struktur tanah lebih baik
    ✅ Hama & penyakit ↓
    ✅ Diversifikasi pendapatan
    ✅ Keberlanjutan jangka panjang
    ```
    
    **Adaptasi untuk Indonesia:**
    ```
    Pola:
    - 2 musim padi (MT I & MT II)
    - 1 musim palawija (MT III)
    
    Contoh:
    - Jan-Apr: Padi (MT I)
    - Mei-Agu: Padi (MT II)
    - Sep-Des: Jagung/Kedelai (MT III)
    
    Ulangi setiap 2-3 tahun
    ```
    
    ---
    
    ### **2. SISTEM FOFIFA (Flood-Drain Cycle)**
    
    **Konsep:**
    ```
    Siklus genangan-pengeringan berkala
    → Optimasi pertumbuhan padi
    → Hemat air 20-30%!
    ```
    
    **Protokol:**
    
    **Fase 1: TANAM - ANAKAN (0-30 hari)**
    ```
    - Genangan: 3-5 cm (dangkal)
    - Tujuan: Kontrol gulma, suhu stabil
    ```
    
    **Fase 2: ANAKAN MAKSIMUM (30-50 hari)**
    ```
    - KERING (Mid-season drainage)
    - Durasi: 7-10 hari
    - Tujuan:
      * Aerasi akar (oksigen)
      * Kurangi anakan tidak produktif
      * Perkuat batang (tahan rebah)
      * Hemat air!
    ```
    
    **Fase 3: BUNTING - BERBUNGA (50-80 hari)**
    ```
    - Genangan: 5-10 cm (dalam)
    - PENTING: Jangan kering (kritis untuk pembentukan gabah)
    ```
    
    **Fase 4: PENGISIAN BULIR (80-100 hari)**
    ```
    - Genangan: 3-5 cm (dangkal)
    - Intermittent (genang-kering bergantian)
    ```
    
    **Fase 5: PEMATANGAN (100-120 hari)**
    ```
    - KERING total
    - 10-14 hari sebelum panen
    - Tujuan: Mudah panen, kualitas gabah baik
    ```
    
    **Hasil:**
    ```
    ✅ Hemat air: 20-30% vs genangan kontinyu
    ✅ Hasil sama atau lebih tinggi (+5-10%)
    ✅ Kualitas beras lebih baik
    ✅ Emisi metana ↓ 40-50% (lingkungan)
    ✅ Batang lebih kuat (tahan rebah)
    ```
    
    **Referensi:**
    - Bouman, B. A. M., et al. (2007). Rice: Feeding the billions. Water for Food, Water for Life.
    
    ---
    
    ### **3. SISTEM IRIGASI OTOMATIS (Automated Irrigation)**
    
    **Teknologi:**
    
    **A. Water Level Sensor:**
    ```
    - Sensor di sawah (float switch atau ultrasonic)
    - Monitor kedalaman air real-time
    - Auto on/off pompa/pintu air
    
    Setting:
    - Batas bawah: 3 cm → Pompa ON
    - Batas atas: 8 cm → Pompa OFF
    ```
    
    **B. Soil Moisture Sensor (untuk lahan kering):**
    ```
    - Tensiometer atau capacitance sensor
    - Monitor kelembaban tanah
    - Auto irigasi jika kering
    
    Setting:
    - Threshold: -30 kPa (sayuran)
    - Threshold: -50 kPa (jagung)
    ```
    
    **C. Weather Station Integration:**
    ```
    - Data cuaca real-time (hujan, suhu, RH)
    - Prediksi ET0
    - Auto adjust jadwal irigasi
    
    Contoh:
    - Jika hujan >10 mm → Skip irigasi
    - Jika suhu >35°C → Tambah irigasi
    ```
    
    **Keuntungan:**
    ```
    ✅ Hemat air 30-50%
    ✅ Hemat tenaga kerja 80-90%
    ✅ Presisi tinggi (optimal untuk tanaman)
    ✅ Remote monitoring (smartphone)
    ```
    
    **Biaya:**
    ```
    - Water level sensor: Rp 2-5 juta
    - Soil moisture sensor: Rp 3-8 juta
    - Controller + valve: Rp 5-10 juta
    - Weather station: Rp 10-30 juta
    
    TOTAL: Rp 20-50 juta/ha
    
    ROI: 3-5 tahun (hemat air + tenaga kerja)
    ```
    
    ---
    
    ### **4. SISTEM TANGGUL PRESISI (Precision Leveling)**
    
    **Konsep:**
    ```
    Ratakan lahan dengan presisi tinggi (±2 cm)
    → Distribusi air merata
    → Hemat air, hasil seragam
    ```
    
    **Teknologi:**
    
    **Laser Land Leveling:**
    ```
    - Traktor dengan blade + laser receiver
    - Laser transmitter (rotating laser)
    - Otomatis adjust blade untuk ratakan tanah
    - Presisi: ±2 cm
    
    Biaya:
    - Sewa alat: Rp 1-2 juta/ha
    - Beli alat: Rp 200-500 juta (untuk kontraktor)
    ```
    
    **Keuntungan:**
    ```
    ✅ Hemat air 20-40% (distribusi merata)
    ✅ Hasil ↑ 10-25% (pertumbuhan seragam)
    ✅ Hemat benih 5-10% (kedalaman tanam seragam)
    ✅ Hemat pupuk 10-15% (tidak terkonsentrasi di low spot)
    ✅ Mudah panen (seragam)
    ```
    
    **Adaptasi Indonesia:**
    ```
    - Prioritas: Sawah irigasi teknis
    - Lakukan sebelum musim tanam
    - Kombinasi dengan rotasi (saat upland)
    ```
    
    ---
    
    ### **5. SISTEM DAUR ULANG AIR (Water Recycling)**
    
    **Konsep:**
    ```
    Air drainase dikumpulkan → Filter → Reuse untuk irigasi
    → Zero waste water!
    ```
    
    **Komponen:**
    
    **A. Kolam Penampung (Reservoir):**
    ```
    - Tampung air drainase
    - Volume: 100-500 m³/ha
    - Kedalaman: 2-3 m
    ```
    
    **B. Filter:**
    ```
    - Sedimentasi (settling pond)
    - Sand filter (jika perlu)
    - Buang sedimen & kontaminan
    ```
    
    **C. Pompa Recirculation:**
    ```
    - Pompa air kembali ke sawah
    - Otomatis (sensor level)
    ```
    
    **Keuntungan:**
    ```
    ✅ Hemat air 40-60% (reuse)
    ✅ Kurangi polusi (nutrien tidak ke sungai)
    ✅ Daur ulang nutrien (pupuk)
    ✅ Keberlanjutan
    ```
    
    **Aplikasi:**
    ```
    - Greenhouse (closed system)
    - Sawah intensif (high-value crops)
    - Area dengan air terbatas
    ```
    
    ---
    
    ## 🌱 ADAPTASI UNTUK INDONESIA
    
    ### **Prioritas Teknologi:**
    
    **1. FOFIFA System (Flood-Drain Cycle):**
    ```
    ✅ Mudah implementasi (no equipment)
    ✅ Hemat air 20-30%
    ✅ Cocok untuk semua petani
    
    ACTION:
    - Edukasi petani (penyuluhan)
    - Demonstrasi plot (BPTP)
    - Monitoring & evaluasi
    ```
    
    **2. Paddy-Upland Rotation:**
    ```
    ✅ Perbaiki produktivitas jangka panjang
    ✅ Diversifikasi pendapatan
    
    ACTION:
    - Pilot project (kelompok tani)
    - Subsidi benih palawija
    - Jaminan pasar (koperasi)
    ```
    
    **3. Precision Leveling:**
    ```
    ✅ ROI cepat (1-2 tahun)
    ✅ Hemat air + hasil ↑
    
    ACTION:
    - Subsidi alat (pemerintah)
    - Kontraktor jasa (UPJA)
    - Prioritas sawah irigasi teknis
    ```
    
    **4. Automated Irrigation:**
    ```
    ✅ Untuk high-value crops (sayuran, buah)
    ✅ Greenhouse/polytunnel
    
    ACTION:
    - Pilot project (petani maju)
    - Pelatihan teknologi
    - Akses kredit (KUR)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Bouman, B. A. M., et al. (2007).** Rice: Feeding the billions. Water for Food, Water for Life. IWMI.
    
    2. **Tabuchi, T. (2001).** Paddy Field Irrigation and Drainage in Japan. JSIDRE.
    
    3. **JIRCAS. (2010).** Water-Saving Irrigation for Rice. Japan International Research Center for Agricultural Sciences.
    
    """)

# ===== TAB 5: TOOLS & CALCULATOR =====
with tab_tools:
    st.header("🛠️ Tools & Calculator")
    
    st.markdown("""
    ### Fitur yang Tersedia:
    - 💧 ET0 Calculator (Penman-Monteith)
    - 🌾 Crop Water Requirement Calculator
    - 💦 Drip System Designer
    - 🌧️ Sprinkler System Designer
    
    ---
    """)
    
    # ET0 CALCULATOR
    st.subheader("💧 ET0 Calculator (Simplified)")
    
    st.markdown("""
    **Metode Blaney-Criddle (untuk data terbatas)**
    
    Formula: ET0 = p * (0.46 T + 8)
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        temp_avg = st.number_input("Suhu Rata-rata (°C):", min_value=10.0, max_value=40.0, value=27.0, step=0.5)
        
        latitude = st.selectbox("Latitude (approx):", [
            "0-10° (Ekuator)",
            "10-20° (Tropis)",
            "20-30° (Subtropis)"
        ])
        
        month = st.selectbox("Bulan:", [
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ])
    
    with col2:
        # p value (simplified, for equator)
        p_values = {
            "Januari": 0.27, "Februari": 0.26, "Maret": 0.27,
            "April": 0.27, "Mei": 0.27, "Juni": 0.27,
            "Juli": 0.27, "Agustus": 0.27, "September": 0.27,
            "Oktober": 0.27, "November": 0.27, "Desember": 0.27
        }
        
        p = p_values[month]
        et0 = p * (0.46 * temp_avg + 8)
        
        st.metric("ET0 (mm/hari)", f"{et0:.2f}")
        st.info(f"""
        **Interpretasi:**
        - ET0 = {et0:.2f} mm/hari
        - Kategori: {"Rendah" if et0 < 3 else "Sedang" if et0 < 5 else "Tinggi"}
        - Kebutuhan air tanaman = ET0 * Kc
        """)
    
    st.markdown("---")
    
    # CROP WATER REQUIREMENT CALCULATOR
    st.subheader("🌾 Crop Water Requirement Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        crop = st.selectbox("Pilih Tanaman:", [
            "Padi", "Jagung", "Tomat", "Cabai", "Kedelai", "Melon"
        ])
        
        growth_stage = st.selectbox("Fase Pertumbuhan:", [
            "Initial (Awal)",
            "Development (Perkembangan)",
            "Mid-season (Pertengahan)",
            "Late-season (Akhir)"
        ])
    
    with col2:
        et0_input = st.number_input("ET0 (mm/hari):", min_value=1.0, max_value=10.0, value=5.0, step=0.1)
        rainfall = st.number_input("Curah Hujan (mm/hari):", min_value=0.0, max_value=50.0, value=0.0, step=0.5)
    
    with col3:
        # Kc values
        kc_values = {
            "Padi": {"Initial (Awal)": 1.05, "Development (Perkembangan)": 1.10, "Mid-season (Pertengahan)": 1.20, "Late-season (Akhir)": 0.90},
            "Jagung": {"Initial (Awal)": 0.30, "Development (Perkembangan)": 0.70, "Mid-season (Pertengahan)": 1.20, "Late-season (Akhir)": 0.60},
            "Tomat": {"Initial (Awal)": 0.60, "Development (Perkembangan)": 0.85, "Mid-season (Pertengahan)": 1.15, "Late-season (Akhir)": 0.80},
            "Cabai": {"Initial (Awal)": 0.60, "Development (Perkembangan)": 0.90, "Mid-season (Pertengahan)": 1.05, "Late-season (Akhir)": 0.90},
            "Kedelai": {"Initial (Awal)": 0.40, "Development (Perkembangan)": 0.70, "Mid-season (Pertengahan)": 1.15, "Late-season (Akhir)": 0.50},
            "Melon": {"Initial (Awal)": 0.50, "Development (Perkembangan)": 0.85, "Mid-season (Pertengahan)": 1.05, "Late-season (Akhir)": 0.75}
        }
        
        kc = kc_values[crop][growth_stage]
        etc = et0_input * kc
        pe = 0.6 * rainfall if rainfall < 2.5 else 0.8 * rainfall - 0.8
        net_irrigation = max(0, etc - pe)
        
        st.metric("Kc (Koefisien Tanaman)", f"{kc:.2f}")
        st.metric("ETc (mm/hari)", f"{etc:.2f}")
        st.metric("Kebutuhan Irigasi Netto", f"{net_irrigation:.2f} mm/hari")
        st.info(f"= {net_irrigation * 10:.0f} m³/ha/hari")
    
    st.markdown("---")
    
    # DRIP SYSTEM DESIGNER
    st.subheader("💦 Drip System Designer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        area_ha = st.number_input("Luas Lahan (ha):", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        plant_spacing_row = st.number_input("Jarak Tanam Antar Baris (cm):", min_value=30, max_value=200, value=60, step=10)
        plant_spacing_plant = st.number_input("Jarak Tanam Dalam Baris (cm):", min_value=20, max_value=100, value=40, step=5)
        water_req = st.number_input("Kebutuhan Air (mm/hari):", min_value=1.0, max_value=10.0, value=5.0, step=0.5)
    
    with col2:
        dripper_discharge = st.number_input("Debit Dripper (L/jam):", min_value=1.0, max_value=4.0, value=2.0, step=0.5)
        irrigation_hours = st.number_input("Jam Operasi (jam/hari):", min_value=1.0, max_value=8.0, value=2.0, step=0.5)
        
        # Calculations
        population = (10000 / (plant_spacing_row * plant_spacing_plant)) * area_ha * 10000
        total_drippers = population
        total_discharge = total_drippers * dripper_discharge / 1000  # m³/jam
        water_applied = total_discharge * irrigation_hours / area_ha  # m³/ha/hari
        water_applied_mm = water_applied / 10  # mm/hari
        
        lateral_length = (100 / (plant_spacing_row / 100)) * area_ha * 100  # m
        
        st.success(f"""
        **Hasil Desain:**
        
        - Populasi tanaman: {population:,.0f} tanaman
        - Jumlah dripper: {total_drippers:,.0f}
        - Total debit: {total_discharge:.1f} m³/jam
        - Air yang diberikan: {water_applied_mm:.1f} mm/hari
        - Panjang lateral: {lateral_length:,.0f} m
        
        **Status:** {"✅ Cukup" if water_applied_mm >= water_req else "⚠️ Kurang - Tambah jam operasi"}
        """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 📚 SUMBER DATA
    
    Calculator ini menggunakan formula dari:
    - FAO Irrigation and Drainage Paper 56
    - Blaney-Criddle Method
    - Standard drip irrigation design
    
    **Disclaimer:** Hasil bersifat estimasi. Untuk desain detail, konsultasikan dengan ahli irigasi.
    """)
