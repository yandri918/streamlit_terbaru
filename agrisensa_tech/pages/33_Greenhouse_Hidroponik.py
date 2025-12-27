import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Greenhouse & Hidroponik - AgriSensa",
    page_icon="🏠",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Header
st.title("🏠 Greenhouse & Sistem Hidroponik")
st.markdown("**Teknologi Budidaya Terkendali untuk Tanaman Bernilai Tinggi**")

# Main tabs
tab_greenhouse, tab_hydro, tab_nutrients, tab_climate, tab_economics, tab_3k, tab_krisan = st.tabs([
    "🏠 Greenhouse",
    "💧 Sistem Hidroponik",
    "🧪 Nutrisi & pH",
    "🌡️ Kontrol Iklim",
    "💰 Analisis Ekonomi",
    "🚀 Manajemen 3K (Sustainable)",
    "🌸 Krisan Spray Jepang"
])

# ===== TAB 1: GREENHOUSE =====
with tab_greenhouse:
    st.header("🏠 Teknologi Greenhouse")
    
    st.markdown("""
    ### Apa itu Greenhouse?
    
    **Greenhouse (rumah kaca)** adalah struktur tertutup dengan atap dan dinding transparan yang **mengontrol lingkungan** untuk pertumbuhan tanaman optimal.
    
    **Keuntungan:**
    - ✅ **Kontrol penuh** iklim (suhu, kelembaban, cahaya)
    - ✅ **Produktivitas tinggi** (2-3x vs open field)
    - ✅ **Kualitas premium** (bersih, seragam)
    - ✅ **Panen sepanjang tahun** (tidak tergantung musim)
    - ✅ **Hemat air** (30-50% vs open field)
    - ✅ **Hemat pestisida** (80-90%, terlindung hama)
    - ✅ **Premium price** (2-5x harga pasar)
    
    **Kekurangan:**
    ```
    ❌ Investasi awal tinggi (Rp 200-800 juta/1000 m²)
    ❌ Biaya operasional tinggi (listrik, cooling)
    ❌ Perlu skill teknis
    ❌ Maintenance rutin
    ```
    
    ---
    
    ## 🏗️ JENIS GREENHOUSE
    
    ### **1. GREENHOUSE SEDERHANA (Low-Tech)**
    
    **A. Tunnel Plastik (Polytunnel):**
    ```
    Struktur:
    - Rangka: Bambu/pipa PVC
    - Atap: Plastik UV (200 micron)
    - Dinding: Plastik/insect net
    - Ventilasi: Manual (buka tutup plastik)
    
    Dimensi:
    - Lebar: 6-8 m
    - Panjang: 20-50 m
    - Tinggi: 3-4 m
    
    Biaya:
    - Rp 150-250K/m²
    - Total 1000 m²: Rp 150-250 juta
    
    Cocok untuk:
    - Sayuran (tomat, cabai, melon)
    - Dataran rendah-menengah
    - Petani pemula
    ```
    
    **Keuntungan:**
    ```
    ✅ Murah
    ✅ Mudah bangun (DIY)
    ✅ Fleksibel (bisa pindah)
    ```
    
    **Kekurangan:**
    ```
    ❌ Kontrol iklim terbatas
    ❌ Panas (>40°C di dataran rendah)
    ❌ Plastik perlu ganti (2-3 tahun)
    ```
    
    ---
    
    **B. Screenhouse (Insect Net House):**
    ```
    Struktur:
    - Rangka: Besi hollow/pipa galvanis
    - Atap & dinding: Insect net (50 mesh)
    - Ventilasi: Alami (angin)
    
    Biaya:
    - Rp 200-350K/m²
    - Total 1000 m²: Rp 200-350 juta
    
    Cocok untuk:
    - Sayuran organik
    - Bibit tanaman
    - Area dengan hama tinggi
    ```
    
    **Keuntungan:**
    ```
    ✅ Sirkulasi udara baik (tidak panas)
    ✅ Lindungi dari hama (90%)
    ✅ Tahan lama (net 5-7 tahun)
    ```
    
    **Kekurangan:**
    ```
    ❌ Tidak lindungi dari hujan/angin kencang
    ❌ Kontrol suhu minimal
    ```
    
    ---
    
    ### **2. GREENHOUSE MODERN (High-Tech)**
    
    **A. Multi-Span Greenhouse:**
    ```
    Struktur:
    - Rangka: Besi galvanis (tahan 15-20 tahun)
    - Atap: Polycarbonat/kaca
    - Dinding: Polycarbonat/plastik UV
    - Ventilasi: Otomatis (roof vent, side vent)
    - Cooling: Evaporative cooling (cooling pad + fan)
    - Heating: Heater (jika perlu)
    
    Dimensi:
    - Lebar span: 8-12 m
    - Jumlah span: 3-10
    - Tinggi: 4-6 m
    
    Biaya:
    - Rp 500-800K/m²
    - Total 1000 m²: Rp 500-800 juta
    
    Cocok untuk:
    - Tomat, paprika, timun (high-value)
    - Bunga potong
    - Skala komersial
    ```
    
    **Keuntungan:**
    ```
    ✅ Kontrol iklim penuh (suhu, RH, CO₂)
    ✅ Produktivitas sangat tinggi (3-5x open field)
    ✅ Kualitas export
    ✅ Tahan lama (20+ tahun)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi sangat tinggi
    ❌ Biaya operasional tinggi (listrik)
    ❌ Perlu teknisi terlatih
    ```
    
    ---
    
    **B. Venlo Greenhouse (Dutch Style):**
    ```
    Ciri khas:
    - Atap kaca (glass)
    - Roof angle: 22-26° (optimal untuk cahaya)
    - Gutter: Aluminium (drainase hujan)
    - Fully automated (climate, irrigation, fertigation)
    
    Biaya:
    - Rp 800-1,500K/m²
    - Total 1000 m²: Rp 800 juta - 1.5 miliar
    
    Cocok untuk:
    - Tomat, paprika (export quality)
    - Bunga potong (mawar, anggrek)
    - Skala besar (>5000 m²)
    ```
    
    **Keuntungan:**
    ```
    ✅ Transmisi cahaya maksimal (90%)
    ✅ Umur panjang (30+ tahun)
    ✅ Presisi tinggi (sensor, automation)
    ✅ Yield tertinggi (50-100 kg/m²/tahun untuk tomat!)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi tertinggi
    ❌ Perlu expertise tinggi
    ❌ Tidak cocok untuk dataran rendah (terlalu panas)
    ```
    
    ---
    
    ## 📊 PERBANDINGAN GREENHOUSE
    
    | Tipe | Investasi (Rp/m²) | Kontrol Iklim | Produktivitas | Umur | Cocok untuk |
    |------|-------------------|---------------|---------------|------|-------------|
    | **Polytunnel** | 150-250K | Rendah | 2x open field | 5-10 tahun | Pemula, dataran tinggi |
    | **Screenhouse** | 200-350K | Minimal | 1.5x open field | 10-15 tahun | Organik, bibit |
    | **Multi-Span** | 500-800K | Tinggi | 3-5x open field | 20+ tahun | Komersial |
    | **Venlo** | 800-1,500K | Sangat tinggi | 5-10x open field | 30+ tahun | Export, skala besar |
    
    ---
    
    ## 💡 TIPS MEMILIH GREENHOUSE
    
    **1. Sesuaikan dengan Budget:**
    ```
    - Budget <Rp 300 juta: Polytunnel/Screenhouse
    - Budget Rp 300-800 juta: Multi-Span
    - Budget >Rp 800 juta: Venlo
    ```
    
    **2. Pertimbangkan Lokasi:**
    ```
    - Dataran rendah (0-500 m): Perlu cooling kuat
    - Dataran menengah (500-1000 m): Ideal untuk greenhouse
    - Dataran tinggi (>1000 m): Perlu heating (malam hari)
    ```
    
    **3. Pilih Tanaman Bernilai Tinggi:**
    ```
    - Tomat cherry: Rp 30-50K/kg
    - Paprika: Rp 40-80K/kg
    - Melon premium: Rp 50-100K/kg
    - Strawberry: Rp 80-150K/kg
    - Bunga potong: Rp 5-20K/tangkai
    
    ROI: 2-4 tahun (jika dikelola baik)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Nelson, P. V. (2011).** Greenhouse Operation and Management, 7th Edition. Prentice Hall.
    
    2. **Hanan, J. J. (1998).** Greenhouses: Advanced Technology for Protected Horticulture. CRC Press.
    
    3. **Bakker, J. C., et al. (1995).** Greenhouse Climate Control. Wageningen Academic Publishers.
    
    """)

# ===== TAB 2: SISTEM HIDROPONIK =====
with tab_hydro:
    st.header("💧 Sistem Hidroponik")
    
    st.markdown("""
    ### Apa itu Hidroponik?
    
    **Hidroponik** adalah metode budidaya tanaman **tanpa tanah**, menggunakan **larutan nutrisi** dalam air sebagai media tumbuh.
    
    **Keuntungan:**
    - ✅ **Hemat air** (90% vs tanah!)
    - ✅ **Pertumbuhan cepat** (30-50% lebih cepat)
    - ✅ **Yield tinggi** (2-3x vs tanah)
    - ✅ **Bersih** (no soil-borne disease)
    - ✅ **Efisien lahan** (vertikal farming)
    - ✅ **Kontrol nutrisi** presisi
    
    **Kekurangan:**
    ```
    ❌ Investasi awal tinggi
    ❌ Perlu skill (nutrisi, pH, EC)
    ❌ Risiko system failure (pompa mati = tanaman mati)
    ❌ Biaya listrik (pompa 24/7)
    ```
    
    ---
    
    ## 🌊 JENIS SISTEM HIDROPONIK
    
    ### **1. NFT (Nutrient Film Technique)**
    
    **Prinsip:**
    ```
    Larutan nutrisi mengalir tipis (film) di dasar pipa miring
    → Akar menyerap nutrisi + oksigen
    → Larutan kembali ke tangki (recirculating)
    ```
    
    **Komponen:**
    ```
    1. Tangki nutrisi (100-200 L)
    2. Pompa submersible (30-50 watt)
    3. Pipa NFT (diameter 3-4 inch, panjang 3-6 m)
    4. Kemiringan: 1-3% (1-3 cm per meter)
    5. Net pot (diameter 5 cm)
    6. Rockwool/cocopeat (media semai)
    ```
    
    **Desain:**
    ```
    Contoh: Selada 100 lubang
    
    - Pipa: 10 batang @ 3 m (10 lubang/pipa)
    - Jarak lubang: 25 cm
    - Kemiringan: 2% (6 cm drop per 3 m)
    - Pompa: 40 watt, 2000 L/jam
    - Flow rate: 1-2 L/menit per pipa
    - Tangki: 150 L
    
    Biaya:
    - Pipa PVC: Rp 50K × 10 = Rp 500K
    - Net pot: Rp 1K × 100 = Rp 100K
    - Pompa: Rp 300K
    - Tangki: Rp 200K
    - Rangka: Rp 500K
    - Nutrisi (1 bulan): Rp 200K
    
    TOTAL: Rp 1.8 juta (100 lubang)
    = Rp 18K/lubang
    ```
    
    **Cocok untuk:**
    - Selada, kangkung, sawi, bayam
    - Tanaman daun (leafy greens)
    - Pertumbuhan cepat (25-35 hari)
    
    **Keuntungan:**
    ```
    ✅ Hemat air (recirculating)
    ✅ Oksigenasi baik (akar tidak terendam)
    ✅ Pertumbuhan cepat
    ```
    
    **Kekurangan:**
    ```
    ❌ Pompa harus 24/7 (jika mati 2-3 jam = tanaman layu)
    ❌ Perlu kemiringan presisi
    ❌ Tidak cocok untuk tanaman besar (tomat, cabai)
    ```
    
    ---
    
    ### **2. DFT (Deep Flow Technique)**
    
    **Prinsip:**
    ```
    Larutan nutrisi mengalir dalam (deep) di pipa/talang
    → Akar terendam sebagian
    → Lebih toleran jika pompa mati (buffer 6-12 jam)
    ```
    
    **Perbedaan dengan NFT:**
    ```
    NFT: Film tipis (1-2 mm), akar tidak terendam
    DFT: Kedalaman 3-5 cm, akar terendam sebagian
    
    DFT lebih aman untuk pemula!
    ```
    
    **Desain:**
    ```
    - Pipa/talang: Diameter 4-6 inch
    - Kedalaman air: 3-5 cm
    - Kemiringan: 1-2%
    - Pompa: Bisa intermittent (on 15 menit, off 15 menit)
    
    Biaya: Sama dengan NFT (Rp 18-20K/lubang)
    ```
    
    **Cocok untuk:**
    - Selada, kangkung, pakcoy
    - Pemula (lebih toleran error)
    
    ---
    
    ### **3. WICK SYSTEM (Sistem Sumbu)**
    
    **Prinsip:**
    ```
    Larutan nutrisi diserap melalui sumbu (wick) dari tangki ke media
    → PASIF (no pump, no electricity!)
    → Paling sederhana
    ```
    
    **Komponen:**
    ```
    1. Wadah (pot/botol bekas)
    2. Media: Cocopeat/sekam bakar
    3. Sumbu: Kain flanel/sumbu kompor (diameter 1 cm)
    4. Tangki nutrisi (di bawah pot)
    ```
    
    **Desain:**
    ```
    Contoh: Cabai 20 pot
    
    - Pot: Diameter 20 cm
    - Media: Cocopeat 2 L/pot
    - Sumbu: 2-3 sumbu/pot
    - Tangki: 10 L (untuk 5 pot)
    
    Biaya:
    - Pot: Rp 5K × 20 = Rp 100K
    - Cocopeat: Rp 200K
    - Sumbu: Rp 50K
    - Tangki: Rp 100K
    - Nutrisi: Rp 200K
    
    TOTAL: Rp 650K (20 pot)
    = Rp 32K/pot
    ```
    
    **Cocok untuk:**
    - Cabai, tomat (tanaman buah)
    - Skala kecil (hobi, rumahan)
    - Area tanpa listrik
    
    **Keuntungan:**
    ```
    ✅ Paling murah
    ✅ No listrik (hemat!)
    ✅ Mudah maintenance
    ✅ Cocok untuk pemula
    ```
    
    **Kekurangan:**
    ```
    ❌ Pertumbuhan lebih lambat (vs NFT/DFT)
    ❌ Tidak cocok untuk tanaman besar (akar banyak)
    ❌ Perlu ganti sumbu (3-6 bulan)
    ```
    
    ---
    
    ### **4. DRIP SYSTEM (Sistem Tetes)**
    
    **Prinsip:**
    ```
    Larutan nutrisi diteteskan ke media (cocopeat/perlite)
    → Excess drainage kembali ke tangki (recirculating)
    → Cocok untuk tanaman besar
    ```
    
    **Komponen:**
    ```
    1. Tangki nutrisi (200-500 L)
    2. Pompa + timer (on/off otomatis)
    3. Mainline + lateral (pipa 1/2 inch)
    4. Dripper (2-4 L/jam)
    5. Pot/polybag (10-20 L)
    6. Media: Cocopeat + perlite (70:30)
    7. Drainage tray (kumpulkan excess)
    ```
    
    **Desain:**
    ```
    Contoh: Tomat 50 tanaman
    
    - Pot: 15 L/tanaman
    - Media: Cocopeat + perlite
    - Dripper: 2 L/jam, 2 dripper/tanaman
    - Timer: On 5 menit, off 30 menit (siang)
    - Pompa: 60 watt
    
    Biaya:
    - Pot 15L: Rp 15K × 50 = Rp 750K
    - Media: Rp 1 juta
    - Drip system: Rp 2 juta
    - Pompa + timer: Rp 800K
    - Tangki: Rp 500K
    - Rangka: Rp 2 juta
    
    TOTAL: Rp 7 juta (50 tanaman)
    = Rp 140K/tanaman
    ```
    
    **Cocok untuk:**
    - Tomat, paprika, melon, timun
    - Tanaman buah (high-value)
    - Greenhouse
    
    **Keuntungan:**
    ```
    ✅ Cocok untuk tanaman besar
    ✅ Oksigenasi baik (media porous)
    ✅ Toleran jika pompa mati (buffer 1-2 hari)
    ✅ Scalable (mudah expand)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi tinggi
    ❌ Perlu ganti media (6-12 bulan)
    ❌ Risiko clogging (dripper tersumbat)
    ```
    
    ---
    
    ### **5. AEROPONICS**
    
    **Prinsip:**
    ```
    Akar digantung di udara
    → Larutan nutrisi disemprotkan (mist/spray)
    → Oksigenasi MAKSIMAL!
    ```
    
    **Komponen:**
    ```
    1. Chamber (box kedap cahaya)
    2. Mist nozzle (spray 360°)
    3. Pompa tekanan tinggi (60-80 PSI)
    4. Timer (on 5 detik, off 5 menit)
    ```
    
    **Biaya:**
    ```
    Sangat mahal (Rp 200-300K/lubang)
    Hanya untuk research/high-tech farm
    ```
    
    **Keuntungan:**
    ```
    ✅ Pertumbuhan TERCEPAT (50% lebih cepat vs NFT)
    ✅ Oksigenasi maksimal
    ✅ Hemat air (95% vs tanah)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi tertinggi
    ❌ Sangat sensitif (pompa mati 30 menit = tanaman mati)
    ❌ Perlu expertise tinggi
    ```
    
    ---
    
    ## 📊 PERBANDINGAN SISTEM HIDROPONIK
    
    | Sistem | Investasi/lubang | Listrik | Kesulitan | Pertumbuhan | Cocok untuk |
    |--------|------------------|---------|-----------|-------------|-------------|
    | **NFT** | Rp 18-20K | 24/7 | Sedang | Cepat | Selada, kangkung |
    | **DFT** | Rp 18-20K | Intermittent | Mudah | Cepat | Selada (pemula) |
    | **Wick** | Rp 30-40K | No | Sangat mudah | Sedang | Cabai, tomat (hobi) |
    | **Drip** | Rp 140-200K | Intermittent | Sedang | Cepat | Tomat, paprika (komersial) |
    | **Aeroponics** | Rp 200-300K | 24/7 | Sangat sulit | Sangat cepat | Research |
    
    ---
    
    ## 💡 TIPS MEMILIH SISTEM
    
    **Pilih NFT/DFT jika:**
    ```
    ✅ Tanaman daun (selada, kangkung)
    ✅ Ingin cepat panen (25-35 hari)
    ✅ Skala menengah (100-1000 lubang)
    ```
    
    **Pilih WICK jika:**
    ```
    ✅ Pemula (paling mudah!)
    ✅ Skala kecil (hobi)
    ✅ No budget untuk listrik
    ✅ Tanaman buah (cabai, tomat)
    ```
    
    **Pilih DRIP jika:**
    ```
    ✅ Tanaman buah bernilai tinggi
    ✅ Greenhouse
    ✅ Skala komersial
    ✅ Punya budget (ROI 1-2 tahun)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Resh, H. M. (2012).** Hydroponic Food Production, 7th Edition. CRC Press.
    
    2. **Jones, J. B. (2005).** Hydroponics: A Practical Guide for the Soilless Grower. CRC Press.
    
    3. **Savvas, D., & Passam, H. (2002).** Hydroponic Production of Vegetables and Ornamentals. Embryo Publications.
    
    """)

# ===== TAB 3: NUTRISI & pH =====
with tab_nutrients:
    st.header("🧪 Nutrisi & Manajemen pH")
    
    st.markdown("""
    ### Nutrisi Hidroponik
    
    Tanaman hidroponik perlu **16 elemen esensial** dari larutan nutrisi:
    
    **Makronutrien (banyak):**
    - N (Nitrogen), P (Fosfor), K (Kalium)
    - Ca (Kalsium), Mg (Magnesium), S (Sulfur)
    
    **Mikronutrien (sedikit):**
    - Fe (Besi), Mn (Mangan), Zn (Seng), Cu (Tembaga)
    - B (Boron), Mo (Molibdenum), Cl (Klorin)
    
    ---
    
    ## 🧪 AB MIX (Nutrisi Hidroponik)
    
    ### **Apa itu AB Mix?**
    
    **AB Mix** adalah nutrisi hidroponik yang terdiri dari **2 larutan terpisah**:
    - **Pekkat A:** Ca(NO₃)₂, Fe-EDTA
    - **Pekkat B:** KNO₃, KH₂PO₄, MgSO₄, mikronutrien
    
    **Mengapa dipisah?**
    ```
    Jika dicampur langsung (konsentrasi tinggi):
    Ca²⁺ + SO₄²⁻ → CaSO₄ (gypsum, mengendap!)
    Ca²⁺ + PO₄³⁻ → Ca₃(PO₄)₂ (mengendap!)
    
    Jadi HARUS dipisah, baru dicampur di tangki (konsentrasi rendah)
    ```
    
    ---
    
    ### **Cara Membuat Larutan Nutrisi:**
    
    **1. Beli AB Mix (Paling Mudah):**
    ```
    Merek: AB Mix Hydro, Growmore, dll
    Harga: Rp 50-100K/kg (cukup untuk 500-1000 L)
    
    Cara pakai:
    1. Isi tangki dengan air (100 L)
    2. Larutkan Pekkat A: 50-100 gram → aduk
    3. Larutkan Pekkat B: 50-100 gram → aduk
    4. Ukur EC: Target 1.5-2.5 mS/cm
    5. Ukur pH: Target 5.5-6.5
    6. Adjust jika perlu
    ```
    
    **2. Buat Sendiri (Advanced):**
    ```
    Formula Selada (per 1000 L):
    
    PEKKAT A (1000x):
    - Ca(NO₃)₂·4H₂O: 944 g
    - Fe-EDTA: 79 g
    - Air: 1 L
    
    PEKKAT B (1000x):
    - KNO₃: 809 g
    - KH₂PO₄: 263 g
    - MgSO₄·7H₂O: 493 g
    - MnSO₄·H₂O: 2.13 g
    - ZnSO₄·7H₂O: 0.22 g
    - CuSO₄·5H₂O: 0.08 g
    - H₃BO₃: 2.86 g
    - Na₂MoO₄·2H₂O: 0.02 g
    - Air: 1 L
    
    Cara pakai:
    - Tambahkan 1 mL Pekkat A per 1 L air
    - Tambahkan 1 mL Pekkat B per 1 L air
    - EC: 1.8-2.2 mS/cm
    - pH: 5.8-6.2
    ```
    
    ---
    
    ## 📊 EC (Electrical Conductivity)
    
    ### **Apa itu EC?**
    
    **EC** = Konduktivitas listrik larutan = **ukuran konsentrasi nutrisi**
    
    ```
    EC tinggi = Nutrisi pekat (>2.5 mS/cm)
    EC rendah = Nutrisi encer (<1.0 mS/cm)
    ```
    
    ### **EC Optimal untuk Berbagai Tanaman:**
    
    | Tanaman | EC (mS/cm) | Keterangan |
    |---------|------------|------------|
    | **Selada** | 1.2-1.8 | Rendah (leafy greens) |
    | **Kangkung** | 1.5-2.0 | Rendah-sedang |
    | **Tomat** | 2.0-3.5 | Sedang-tinggi |
    | **Cabai** | 2.0-3.0 | Sedang-tinggi |
    | **Paprika** | 2.5-3.5 | Tinggi |
    | **Melon** | 2.0-2.5 | Sedang |
    | **Strawberry** | 1.8-2.2 | Sedang |
    
    ### **Cara Mengukur EC:**
    ```
    1. Beli EC meter (Rp 200-500K)
    2. Kalibrasi dengan larutan standar (1.413 mS/cm)
    3. Celupkan probe ke larutan nutrisi
    4. Baca nilai EC
    
    Jika EC terlalu rendah: Tambah AB Mix
    Jika EC terlalu tinggi: Tambah air
    ```
    
    ---
    
    ## 🧪 pH (Potential of Hydrogen)
    
    ### **Mengapa pH Penting?**
    
    **pH** mengontrol **ketersediaan nutrisi**:
    
    ```
    pH terlalu rendah (<5.0):
    - Fe, Mn, Zn larut berlebihan (toxic!)
    - Ca, Mg sulit diserap
    
    pH terlalu tinggi (>7.0):
    - Fe, Mn, Zn mengendap (defisiensi!)
    - P sulit diserap
    
    pH OPTIMAL: 5.5-6.5 (semua nutrisi tersedia)
    ```
    
    ### **pH Optimal untuk Berbagai Tanaman:**
    
    | Tanaman | pH Optimal | Toleransi |
    |---------|------------|-----------|
    | **Selada** | 5.5-6.5 | Luas |
    | **Tomat** | 6.0-6.5 | Sedang |
    | **Cabai** | 6.0-6.5 | Sedang |
    | **Strawberry** | 5.5-6.0 | Sempit (acidic) |
    | **Melon** | 6.0-6.5 | Sedang |
    
    ### **Cara Mengukur & Adjust pH:**
    
    **1. Ukur pH:**
    ```
    - pH meter digital (Rp 200-500K)
    - pH test kit (Rp 50-100K, kurang akurat)
    ```
    
    **2. Adjust pH:**
    ```
    Jika pH terlalu tinggi (>6.5):
    - Tambah pH Down (asam fosfat/nitrat)
    - Dosis: 1-5 mL per 10 L (cek bertahap!)
    
    Jika pH terlalu rendah (<5.5):
    - Tambah pH Up (kalium hidroksida)
    - Dosis: 1-5 mL per 10 L
    
    PENTING: Adjust sedikit-sedikit, cek ulang!
    ```
    
    ---
    
    ## 🩺 DIAGNOSA DEFISIENSI NUTRISI
    
    ### **Nitrogen (N) - Defisiensi:**
    ```
    Gejala:
    - Daun tua menguning (dari bawah)
    - Pertumbuhan lambat
    - Batang kurus
    
    Solusi:
    - Tambah KNO₃ atau Ca(NO₃)₂
    - Naikkan EC
    ```
    
    ### **Fosfor (P) - Defisiensi:**
    ```
    Gejala:
    - Daun tua ungu/kemerahan
    - Akar lemah
    - Bunga/buah sedikit
    
    Solusi:
    - Tambah KH₂PO₄
    - Cek pH (P tidak tersedia jika pH >7)
    ```
    
    ### **Kalium (K) - Defisiensi:**
    ```
    Gejala:
    - Tepi daun tua coklat/kering (necrosis)
    - Buah kecil, tidak manis
    
    Solusi:
    - Tambah KNO₃ atau K₂SO₄
    ```
    
    ### **Kalsium (Ca) - Defisiensi:**
    ```
    Gejala:
    - Daun muda keriting/kering
    - Blossom end rot (tomat, paprika)
    - Ujung akar mati
    
    Solusi:
    - Tambah Ca(NO₃)₂
    - Cek EC (jangan terlalu tinggi, hambat Ca)
    ```
    
    ### **Besi (Fe) - Defisiensi:**
    ```
    Gejala:
    - Daun muda kuning, tulang daun hijau (chlorosis)
    - Pertumbuhan terhambat
    
    Solusi:
    - Tambah Fe-EDTA
    - Turunkan pH (Fe tidak tersedia jika pH >7)
    ```
    
    ---
    
    ## 💡 TIPS MANAJEMEN NUTRISI
    
    **1. Monitoring Rutin:**
    ```
    - Cek EC & pH: 2x sehari (pagi & sore)
    - Ganti larutan: 2-4 minggu (atau jika EC tidak stabil)
    - Bersihkan tangki: Setiap ganti larutan
    ```
    
    **2. Kualitas Air:**
    ```
    - Air sumur/PAM: Cek EC awal (harus <0.5 mS/cm)
    - Jika EC tinggi: Pakai RO water atau air hujan
    - Jika air keras (Ca/Mg tinggi): Adjust formula
    ```
    
    **3. Suhu Larutan:**
    ```
    - Optimal: 18-22°C
    - Jika >28°C: Oksigen rendah (akar busuk)
    - Solusi: Chiller atau ganti larutan lebih sering
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Resh, H. M. (2012).** Hydroponic Food Production, 7th Edition. CRC Press.
    
    2. **Jones, J. B. (2005).** Hydroponics: A Practical Guide for the Soilless Grower. CRC Press.
    
    """)

# ===== TAB 4: KONTROL IKLIM =====
with tab_climate:
    st.header("🌡️ Kontrol Iklim Greenhouse")
    
    st.markdown("""
    ### Mengapa Kontrol Iklim Penting?
    
    **Iklim optimal** = **Produktivitas maksimal**
    
    **Parameter Kritis:**
    - 🌡️ **Suhu:** 20-30°C (optimal untuk fotosintesis)
    - 💧 **Kelembaban (RH):** 60-80%
    - ☀️ **Cahaya:** 30,000-50,000 lux
    - 🌬️ **CO₂:** 400-1000 ppm
    - 💨 **Ventilasi:** 40-60 air changes/hour
    
    ---
    
    ## 🌡️ KONTROL SUHU
    
    ### **1. COOLING (Pendinginan)**
    
    **A. Evaporative Cooling (Cooling Pad + Fan):**
    ```
    Prinsip:
    Air menguap → Serap panas → Suhu turun 5-10°C
    
    Komponen:
    - Cooling pad (cellulose, 10-15 cm tebal)
    - Fan exhaust (diameter 50-100 cm)
    - Pompa air (sirkulasi ke pad)
    
    Dimensi:
    - Greenhouse 1000 m²:
      * Cooling pad: 20 m² (2m × 10m)
      * Fan: 10 unit @ 1 HP
      * Pompa: 0.5 HP
    
    Biaya:
    - Cooling pad: Rp 500K/m² × 20 = Rp 10 juta
    - Fan: Rp 3 juta × 10 = Rp 30 juta
    - Pompa + pipa: Rp 5 juta
    
    TOTAL: Rp 45 juta
    
    Operasional:
    - Listrik: 10 HP × 8 jam × Rp 1500/kWh = Rp 90K/hari
    - Air: 500 L/hari
    
    Efektivitas:
    - Turunkan suhu: 5-10°C
    - Naikkan RH: 70-90%
    - Cocok untuk: Dataran rendah-menengah
    ```
    
    **B. Fog System (Kabut):**
    ```
    Prinsip:
    Semprotkan air halus (mist) → Evaporasi cepat → Suhu turun
    
    Komponen:
    - Pompa tekanan tinggi (60-80 bar)
    - Nozzle fog (0.2 mm)
    - Pipa high-pressure
    
    Biaya:
    - Rp 50-100 juta/1000 m²
    
    Efektivitas:
    - Turunkan suhu: 3-7°C
    - Naikkan RH: 80-95%
    - Cocok untuk: Greenhouse high-tech
    ```
    
    **C. Shading (Naungan):**
    ```
    - Shade net (50-70% shading)
    - Whitewash (kapur di atap)
    - Retractable screen (otomatis)
    
    Efektivitas:
    - Turunkan suhu: 2-5°C
    - Kurangi cahaya: 50-70%
    - Murah: Rp 50-100K/m²
    ```
    
    ---
    
    ### **2. HEATING (Pemanasan)**
    
    **Kapan Perlu Heating?**
    ```
    - Dataran tinggi (>1000 m)
    - Suhu malam <15°C
    - Tanaman sensitif dingin (tomat, paprika)
    ```
    
    **Jenis Heater:**
    
    **A. Gas Heater:**
    ```
    - Bahan bakar: LPG
    - Kapasitas: 10-50 kW
    - Biaya: Rp 10-30 juta/unit
    - Operasional: Rp 50-200K/hari (tergantung suhu)
    ```
    
    **B. Electric Heater:**
    ```
    - Listrik: 5-20 kW
    - Biaya: Rp 5-15 juta/unit
    - Operasional: Rp 100-400K/hari (mahal!)
    ```
    
    **C. Thermal Screen:**
    ```
    - Layar insulasi (buka siang, tutup malam)
    - Hemat energi: 30-50%
    - Biaya: Rp 200-400K/m²
    ```
    
    ---
    
    ## 💧 KONTROL KELEMBABAN (RH)
    
    ### **RH Optimal:**
    ```
    - Siang hari: 60-70%
    - Malam hari: 70-80%
    
    RH terlalu rendah (<50%):
    - Transpirasi berlebihan
    - Tanaman stress
    - Solusi: Fog system, evaporative cooling
    
    RH terlalu tinggi (>90%):
    - Penyakit jamur (botrytis, powdery mildew)
    - Solusi: Ventilasi, heating (malam hari)
    ```
    
    ---
    
    ## 💨 VENTILASI
    
    ### **Mengapa Ventilasi Penting?**
    ```
    - Buang panas berlebih
    - Buang kelembaban berlebih
    - Supply CO₂ segar
    - Cegah penyakit
    ```
    
    ### **Jenis Ventilasi:**
    
    **A. Natural Ventilation:**
    ```
    - Roof vent (atap buka-tutup)
    - Side vent (dinding buka-tutup)
    - Murah (no listrik)
    - Cocok untuk: Dataran tinggi, polytunnel
    ```
    
    **B. Forced Ventilation:**
    ```
    - Fan exhaust + inlet
    - Air changes: 40-60x/hour
    - Cocok untuk: Dataran rendah, greenhouse modern
    ```
    
    ---
    
    ## 🌬️ CO₂ ENRICHMENT
    
    ### **Mengapa CO₂?**
    ```
    - Atmosfer normal: 400 ppm
    - Optimal untuk fotosintesis: 800-1000 ppm
    - Yield increase: 20-30%!
    ```
    
    ### **Cara Menambah CO₂:**
    
    **A. CO₂ Generator (Bakar LPG):**
    ```
    - Produksi: 1 kg LPG = 3 kg CO₂
    - Biaya: Rp 20-50 juta/unit
    - Operasional: Rp 50-100K/hari
    ```
    
    **B. CO₂ Cylinder:**
    ```
    - Tabung CO₂ (50 kg)
    - Biaya: Rp 500K/tabung
    - Durasi: 1-2 minggu (1000 m²)
    ```
    
    **Kapan Inject CO₂?**
    ```
    - Pagi-siang (saat fotosintesis)
    - Jangan malam (no fotosintesis)
    - Tutup ventilasi (jangan buang CO₂)
    ```
    
    ---
    
    ## 🤖 AUTOMATION & SENSORS
    
    ### **Sensor:**
    ```
    - Suhu & RH: Rp 500K-2 juta
    - Cahaya (lux): Rp 1-3 juta
    - CO₂: Rp 5-15 juta
    - EC & pH: Rp 2-5 juta
    ```
    
    ### **Controller:**
    ```
    - Climate controller (PLC):
      * Input: Sensor data
      * Output: On/off fan, heater, fog, vent
      * Biaya: Rp 10-50 juta
    
    - Smartphone app (IoT):
      * Monitor real-time
      * Remote control
      * Biaya: Rp 5-20 juta
    ```
    
    ### **Keuntungan Automation:**
    ```
    ✅ Presisi tinggi (±1°C, ±5% RH)
    ✅ Hemat tenaga kerja (80-90%)
    ✅ Hemat energi (on/off sesuai kebutuhan)
    ✅ Data logging (analisis)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Bakker, J. C., et al. (1995).** Greenhouse Climate Control. Wageningen Academic Publishers.
    
    2. **Bot, G. P. A., & Van de Braak, N. J. (1995).** Physics of Greenhouse Climate. IMAG-DLO.
    
    """)

# ===== TAB 5: ANALISIS EKONOMI =====
with tab_economics:
    st.header("💰 Analisis Ekonomi Greenhouse & Hidroponik")
    
    st.markdown("""
    ## 💰 ANALISIS EKONOMI
    
    ### Contoh Kasus: Tomat Cherry Greenhouse 1000 m²
    
    **INVESTASI AWAL:**
    ```
    1. Greenhouse (Multi-Span):
       - Struktur: Rp 500 juta
       - Cooling system: Rp 45 juta
       - Automation: Rp 20 juta
    
    2. Sistem Hidroponik (Drip):
       - 2000 tanaman × Rp 140K = Rp 280 juta
    
    3. Lain-lain:
       - Instalasi listrik: Rp 20 juta
       - Tools & equipment: Rp 10 juta
    
    TOTAL INVESTASI: Rp 875 juta
    ```
    
    **BIAYA OPERASIONAL (per tahun):**
    ```
    1. Benih: 4 siklus × 2000 × Rp 2K = Rp 16 juta
    2. Nutrisi: 12 bulan × Rp 2 juta = Rp 24 juta
    3. Listrik: 12 bulan × Rp 3 juta = Rp 36 juta
    4. Tenaga kerja: 3 orang × Rp 4 juta × 12 = Rp 144 juta
    5. Maintenance: Rp 20 juta
    6. Lain-lain: Rp 10 juta
    
    TOTAL BIAYA OPERASIONAL: Rp 250 juta/tahun
    ```
    
    **PENDAPATAN:**
    ```
    - Yield: 40 kg/m²/tahun × 1000 m² = 40,000 kg
    - Harga: Rp 40,000/kg (rata-rata)
    - REVENUE: Rp 1.6 miliar/tahun
    ```
    
    **PROFIT:**
    ```
    - Revenue: Rp 1.6 miliar
    - Biaya operasional: Rp 250 juta
    - PROFIT: Rp 1.35 miliar/tahun
    
    ROI: Rp 875 juta / Rp 1.35 miliar = 0.65 tahun = 8 bulan!
    ```
    
    ---
    
    ## 📊 INTERACTIVE CALCULATOR
    
    ### Greenhouse ROI Calculator
    """)
    
    # ROI Calculator
    st.subheader("💰 Greenhouse ROI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**INVESTASI:**")
        area = st.number_input("Luas Greenhouse (m²):", min_value=100, max_value=10000, value=1000, step=100)
        greenhouse_cost = st.number_input("Biaya Greenhouse (Rp/m²):", min_value=150000, max_value=1500000, value=500000, step=50000)
        hydro_cost_per_plant = st.number_input("Biaya Hidroponik per Tanaman (Rp):", min_value=50000, max_value=300000, value=140000, step=10000)
        plants_per_m2 = st.number_input("Populasi (tanaman/m²):", min_value=1.0, max_value=10.0, value=2.0, step=0.5)
        
    with col2:
        st.markdown("**OPERASIONAL & HASIL:**")
        yield_per_m2 = st.number_input("Yield (kg/m²/tahun):", min_value=10.0, max_value=100.0, value=40.0, step=5.0)
        price_per_kg = st.number_input("Harga Jual (Rp/kg):", min_value=10000, max_value=200000, value=40000, step=5000)
        opex_percent = st.number_input("Biaya Operasional (% dari revenue):", min_value=10, max_value=50, value=15, step=5)
        
    # Calculations
    total_plants = int(area * plants_per_m2)
    greenhouse_investment = area * greenhouse_cost
    hydro_investment = total_plants * hydro_cost_per_plant
    other_investment = (greenhouse_investment + hydro_investment) * 0.1  # 10% for other costs
    total_investment = greenhouse_investment + hydro_investment + other_investment
    
    total_yield = area * yield_per_m2
    revenue = total_yield * price_per_kg
    opex = revenue * (opex_percent / 100)
    profit = revenue - opex
    roi_years = total_investment / profit if profit > 0 else 0
    roi_months = roi_years * 12
    
    # Display Results
    st.markdown("---")
    st.subheader("📊 HASIL ANALISIS:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Investasi", f"Rp {total_investment/1e9:.2f} M")
        st.metric("Populasi Tanaman", f"{total_plants:,}")
        
    with col2:
        st.metric("Revenue/Tahun", f"Rp {revenue/1e9:.2f} M")
        st.metric("Profit/Tahun", f"Rp {profit/1e9:.2f} M")
        
    with col3:
        st.metric("ROI (Tahun)", f"{roi_years:.1f} tahun")
        st.metric("ROI (Bulan)", f"{roi_months:.0f} bulan")
        
    # Profitability Assessment
    if roi_months < 12:
        st.success(f"✅ **SANGAT MENGUNTUNGKAN!** ROI hanya {roi_months:.0f} bulan!")
    elif roi_months < 24:
        st.info(f"✅ **MENGUNTUNGKAN** - ROI {roi_months:.0f} bulan (layak investasi)")
    elif roi_months < 36:
        st.warning(f"⚠️ **CUKUP MENGUNTUNGKAN** - ROI {roi_months:.0f} bulan (perlu optimasi)")
    else:
        st.error(f"❌ **KURANG MENGUNTUNGKAN** - ROI {roi_months:.0f} bulan (terlalu lama)")
    
    st.markdown("---")
    
    st.markdown("""
    ## 📚 REFERENSI
    
    1. **Nelson, P. V. (2011).** Greenhouse Operation and Management, 7th Edition. Prentice Hall.
    
    2. **Resh, H. M. (2012).** Hydroponic Food Production, 7th Edition. CRC Press.
    
    3. **Jovicich, E., et al. (2004).** Greenhouse Tomato Production. University of Florida IFAS Extension.
    
    **Disclaimer:** Hasil analisis bersifat estimasi. Untuk analisis detail, konsultasikan dengan ahli greenhouse/hidroponik.
    """)

# ===== TAB 6: MANAJEMEN 3K (SUSTAINABLE) =====
with tab_3k:
    st.header("🚀 Sustainable Greenhouse Management (3K)")
    st.markdown("""
    **Kontinuitas, Kualitas, & Kuantitas** — Kunci sukses menembus pasar modern dan ekspor dengan margin tinggi.
    """)

    # Custom CSS for 3K Dashboard
    st.markdown("""
    <style>
    .pillar-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #10b981;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        height: 100%;
    }
    .pillar-title {
        color: #065f46;
        font-weight: bold;
        font-size: 1.2rem;
        margin-bottom: 10px;
    }
    .kpi-box {
        background: #f0fdf4;
        border: 1px solid #10b981;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # 3K Pillars Overview
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        st.markdown("""<div class="pillar-card"><div class="pillar-title">🔁 Kontinuitas</div>
        Pasokan rutin tanpa putus. Menggunakan sistem <b>Batch / Staggered Planting</b> agar panen tersedia setiap minggu/bulan.</div>""", unsafe_allow_html=True)
    with col_p2:
        st.markdown("""<div class="pillar-card"><div class="pillar-title">🌟 Kualitas</div>
        Standar pasar modern (Grade A). Kontrol nutrisi presisi, IPM tanpa pestisida kimia berbahaya, dan sortasi ketat.</div>""", unsafe_allow_html=True)
    with col_p3:
        st.markdown("""<div class="pillar-card"><div class="pillar-title">📊 Kuantitas</div>
        Yield maksimal per m². Optimalisasi populasi dan efisiensi GH untuk mengejar target tonase pasar.</div>""", unsafe_allow_html=True)

    st.divider()

    # --- SECTION: RAB GREENHOUSE ---
    st.subheader("💰 Rincian RAB Greenhouse & Investasi")
    
    m_col1, m_col2 = st.columns([1, 2])
    
    with m_col1:
        st.info("Input Parameter GH Standar Modern:")
        area_3k = st.number_input("Luas Area (m²)", 100, 10000, 500, step=100, key="area_3k")
        tipe_gh_3k = st.selectbox("Tipe Struktur GH", ["Multi-Span (Galvanis)", "Venlo (Kaca/Advanced)", "Polytunnel Premium"], index=0)
        komoditas_3k = st.selectbox("Komoditas Unggulan", ["Melon Premium (Intanon)", "Tomat Cherry (Ruby)", "Selada Hidroponik (Batavia)", "Paprika Unggul"], index=0)
        
    with m_col2:
        # RAB Calculation Logic
        base_prices = {
            "Multi-Span (Galvanis)": 650000,
            "Venlo (Kaca/Advanced)": 1200000,
            "Polytunnel Premium": 350000
        }
        struct_cost = area_3k * base_prices[tipe_gh_3k]
        
        # Technology Packages (IoT, Cooling, Fertigation)
        tech_cost = area_3k * 150000 # Asumsi Rp 150rb/m2 untuk sistem otomatisasi
        irrigation_cost = area_3k * 100000 # Rp 100rb/m2 untuk Drip/NFT
        
        total_capex = struct_cost + tech_cost + irrigation_cost
        
        st.write("#### 📊 Estimasi Investasi Awal (CAPEX)")
        rab_df = pd.DataFrame({
            "Komponen": ["Struktur & Atap", "Teknologi (IoT & Cooling)", "Sistem Irigasi & Fertigasi", "Lain-lain (Tools/Listrik)"],
            "Biaya (Rp)": [struct_cost, tech_cost, irrigation_cost, total_capex * 0.05]
        })
        st.table(rab_df.style.format({"Biaya (Rp)": "Rp {:,.0f}"}))
        st.success(f"**Total Investasi: Rp {total_capex * 1.05:,.0f}**")

    st.divider()

    # --- SECTION: ROTASI TERBAIK ---
    st.subheader("🔁 Perencanaan Rotasi (Putaran Terbaik)")
    st.info("Sistem Staggered Planting: Membagi GH menjadi beberapa blok/putaran agar panen rutin harian/mingguan.")
    
    r_col1, r_col2 = st.columns(2)
    
    with r_col1:
        siklus_hari = st.slider("Lama Siklus Tanam (Hari dari Semai ke Panen)", 30, 120, 75 if "Melon" in komoditas_3k else 35)
        jumlah_blok = st.number_input("Jumlah Putaran / Blok GH", 2, 12, 4 if "Melon" in komoditas_3k else 8, help="Berapa banyak gelombang tanam")
        target_panen_minggu = st.number_input("Target Panen per Minggu (kg)", 10, 5000, 200)

    with r_col2:
        # Rotation Analysis
        interval_tanam = siklus_hari / jumlah_blok
        st.markdown(f"""
        <div class="kpi-box">
            <h3>Strategi Rotasi</h3>
            <p>Interval Tanam: <b>Setiap {interval_tanam:.1f} Hari</b></p>
            <p>Frekuensi Panen: <b>{365/interval_tanam:.0f} Kali / Tahun</b></p>
            <p>Luas per Blok: <b>{area_3k/jumlah_blok:.1f} m²</b></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Simple Visual Timeline
        timeline_data = []
        for i in range(int(jumlah_blok)):
            timeline_data.append({"Blok": f"Blok {i+1}", "Status": "Tanam", "Minggu Ke": i * (interval_tanam/7)})
        
        st.caption("Visualisasi Gelombang Tanam (Staggered):")
        fig_rot = px.bar(timeline_data, x="Minggu Ke", y="Blok", color="Blok", orientation='h', title="Timeline Rotasi 3K")
        st.plotly_chart(fig_rot, use_container_width=True)

    st.divider()

    # --- SECTION: MANAJEMEN TOTAL ---
    st.subheader("📊 Dashboard Manajemen Total (Dashboard 3K)")
    
    d_col1, d_col2, d_col3 = st.columns(3)
    
    # Simulation Data
    yield_est = (area_3k * 15) if "Melon" in komoditas_3k else (area_3k * 25) # kg per tahun
    rev_est = yield_est * (40000 if "Melon" in komoditas_3k else 20000)
    
    with d_col1:
        st.metric("Skor Kontinuitas", "95%", delta="Tinggi")
        st.caption("Pasokan konsisten ke supermarket")
    with d_col2:
        st.metric("Rasio Kualitas (Grade A)", "88%", delta="5% Up")
        st.caption("Produk memenuhi standar modern market")
    with d_col3:
        st.metric("Efisiensi Kuantitas", f"{yield_est/area_3k:.1f} kg/m²", delta="Optimal")
        st.caption("Produktivitas per unit luas")

    st.markdown("---")
    
    # Checklist Management
    with st.expander("📝 SOP Harian Manajemen 3K (Modern Market Standards)"):
        st.checkbox("1. Monitoring EC & pH (Kualitas) - Pagi & Sore")
        st.checkbox("2. Cek Logbook Rotasi (Kontinuitas) - Apakah jadwal tanam blok berikutnya sudah siap?")
        st.checkbox("3. Pengendalian Hama Preventif (Kualitas) - Gunakan Trap & Insect Net")
        st.checkbox("4. Optimalisasi Pruning (Kuantitas) - Pastikan asimilasi hanya ke buah/daun utama")
        st.checkbox("5. QC Packing (Kualitas) - Berat seragam, NO residu pestisida, Labeling")

    st.success("Sistem Manajemen 3K Aktif: Siap mensuplai pasar modern secara berkelanjutan.")

    st.divider()

    # --- SECTION: SUPPLIER SUPERMARKET SIMULATION ---
    st.subheader("🏢 Simulasi Bisnis: Supplier Supermarket (Consignment)")
    st.markdown("""
    Model bisnis konsinyasi memiliki tantangan **Cash Flow (Modal Kerja)** karena pembayaran biasanya tertunda (Mati 1 Nota/Tempo).
    """)

    s_col1, s_col2 = st.columns([1, 2])
    
    with s_col1:
        st.info("⚙️ Parameter Pengiriman:")
        kapasitas_mingguan = st.number_input("Kapasitas Pengiriman (kg/minggu)", 50, 1000, 200, step=50)
        harga_supplier = st.number_input("Harga Jual ke Supermarket (Rp/kg)", 10000, 100000, 45000, step=1000)
        biaya_ops_per_kg = st.number_input("Biaya Ops + Packing (Rp/kg)", 2000, 20000, 8000, step=500)
        gap_pembayaran = st.selectbox("Model Pembayaran (Term of Payment)", ["Mati 1 Nota (Tempo 2 Minggu)", "Tempo 1 Bulan", "Cash on Delivery (Jarang)"], index=0)
        
        # Risk factor (Retur/Susut di Toko)
        retur_factor = st.slider("Estimasi Retur/Susut di Rak Toko (%)", 0, 20, 5)

        # ==========================================
        # 🔄 GLOBAL SYNC (For Strategic Report)
        # ==========================================
        st.session_state['global_3k_sim'] = {
            "komoditas": komoditas_3k,
            "kapasitas_mingguan": kapasitas_mingguan,
            "harga_supplier": harga_supplier,
            "biaya_ops": biaya_ops_per_kg,
            "gap_pembayaran": gap_pembayaran,
            "retur_factor": retur_factor,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    
    with s_col2:
        # Business Simulation Logic (12 Weeks)
        weeks = list(range(1, 13))
        income = []
        expense = []
        net_cashflow = []
        cumulative_cash = []
        
        current_cumulative = 0
        payment_lag = 2 if "1 Nota" in gap_pembayaran else (4 if "1 Bulan" in gap_pembayaran else 0)
        
        for w in weeks:
            # Operational Cost is every week
            ops_cost = kapasitas_mingguan * biaya_ops_per_kg
            expense.append(ops_cost)
            
            # Revenue depends on lag and retur
            if w > payment_lag:
                revenue = kapasitas_mingguan * harga_supplier * (1 - (retur_factor/100))
            else:
                revenue = 0
            income.append(revenue)
            
            weekly_net = revenue - ops_cost
            net_cashflow.append(weekly_net)
            
            current_cumulative += weekly_net
            cumulative_cash.append(current_cumulative)
            
        # Charting
        sim_df = pd.DataFrame({
            "Minggu": weeks,
            "Pendapatan (Rp)": income,
            "Biaya Ops (Rp)": expense,
            "Arus Kas Kumulatif (Rp)": cumulative_cash
        })
        
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Bar(x=sim_df["Minggu"], y=sim_df["Pendapatan (Rp)"], name="Pendapatan (Paid)", marker_color='#10b981'))
        fig_sim.add_trace(go.Bar(x=sim_df["Minggu"], y=sim_df["Biaya Ops (Rp)"], name="Biaya Ops", marker_color='#ef4444'))
        fig_sim.add_trace(go.Scatter(x=sim_df["Minggu"], y=sim_df["Arus Kas Kumulatif (Rp)"], name="Saldo Kas Kumulatif", line=dict(color='#3b82f6', width=4)))
        
        fig_sim.update_layout(title="Proyeksi Cash Flow Supplier (12 Minggu)", barmode='group', xaxis_title="Minggu Ke-")
        st.plotly_chart(fig_sim, use_container_width=True)
        
        working_capital_needed = abs(min(cumulative_cash)) if min(cumulative_cash) < 0 else 0
        
        st.warning(f"""
        💡 **Analisis Modal Kerja:**
        Anda membutuhkan modal kerja minimal **Rp {working_capital_needed:,.0f}** untuk membiayai operasional selama masa tunggu pembayaran (Mati 1 Nota).
        """)

    st.divider()

# ===== TAB 7: KRISAN SPRAY JEPANG =====
with tab_krisan:
    st.header("🌸 Budidaya Krisan Spray Jepang")
    st.markdown("**Panduan Lengkap SOP Budidaya dari Hulu hingga Hilir**")
    
    # Sub-tabs
    kr_timeline, kr_lahan, kr_bibit, kr_net, kr_irigasi, kr_lampu, kr_dambo, kr_panen, kr_pasca, kr_grading = st.tabs([
        "📋 Timeline",
        "🌱 Persiapan Lahan",
        "🌿 Bibit & Tanam",
        "🕸️ Sistem Net",
        "💧 Irigasi & Nutrisi",
        "💡 Sistem Lampu",
        "🔥 Mesin Dambo",
        "🌾 Panen",
        "✂️ Pasca Panen",
        "📦 Grading & Packing"
    ])
    
    # ========== SUB-TAB 1: TIMELINE ==========
    with kr_timeline:
        st.subheader("📋 Timeline Budidaya Krisan Spray (90-120 Hari)")
        
        st.markdown("""
        ### 🎯 Overview Siklus Tanam
        
        | Fase | Durasi | Aktivitas Utama |
        |:-----|:-------|:----------------|
        | **Persiapan Lahan** | 14 hari | Olah tanah, solarisasi, bedengan |
        | **Vegetatif** | 30-45 hari | Long Day (16 jam), pertumbuhan batang |
        | **Transisi** | 7-10 hari | Mulai Short Day, inisiasi bunga |
        | **Generatif** | 45-60 hari | Short Day, pembungaan |
        | **Panen** | 1-3 hari | Potong, grading, packing |
        
        ---
        
        ### 📅 Timeline Detail per Hari
        """)
        
        # Visual timeline
        timeline_data = pd.DataFrame({
            "HST": [0, 7, 14, 21, 28, 35, 42, 56, 70, 84, 100, 110],
            "Aktivitas": [
                "Tanam bibit",
                "Pemasangan Net 1 (15cm)",
                "Pupuk dasar NPK 16-16-16",
                "Net 2 (30cm), Mulai Long Day",
                "Net 3 (45cm), Penyemprotan rutin",
                "Switch ke Short Day",
                "Net 4 (60cm), Pupuk NPK 10-30-20",
                "Kuncup mulai terlihat",
                "Net 5 (75cm), Pupuk NPK 10-10-40",
                "Warna bunga mulai muncul",
                "Panen Grade 60-80",
                "Panen Grade 100-160"
            ],
            "Fase": ["Start", "Vegetatif", "Vegetatif", "Vegetatif", "Vegetatif", 
                    "Transisi", "Generatif", "Generatif", "Generatif", "Generatif",
                    "Panen", "Panen"]
        })
        
        fig_timeline = go.Figure()
        
        colors = {"Start": "#10b981", "Vegetatif": "#3b82f6", "Transisi": "#f59e0b", 
                  "Generatif": "#8b5cf6", "Panen": "#ef4444"}
        
        for fase in timeline_data["Fase"].unique():
            df = timeline_data[timeline_data["Fase"] == fase]
            fig_timeline.add_trace(go.Scatter(
                x=df["HST"],
                y=[1] * len(df),
                mode="markers+text",
                marker=dict(size=20, color=colors[fase]),
                text=df["Aktivitas"],
                textposition="top center",
                name=fase
            ))
        
        fig_timeline.update_layout(
            title="Timeline Budidaya Krisan Spray",
            xaxis_title="Hari Setelah Tanam (HST)",
            yaxis_visible=False,
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
    # ========== SUB-TAB 2: PERSIAPAN LAHAN ==========
    with kr_lahan:
        st.subheader("🌱 Persiapan Lahan")
        
        st.markdown("""
        ### 1️⃣ Olah Tanah
        
        | Langkah | Detail | Durasi |
        |:--------|:-------|:-------|
        | **Pembersihan** | Bersihkan sisa tanaman, gulma, akar | 1 hari |
        | **Pencangkulan** | Kedalaman 30-40 cm | 1-2 hari |
        | **Penggemburan** | Gunakan traktor mini/cangkul | 1 hari |
        | **Pemupukan Dasar** | Pupuk kandang 10-20 ton/ha | 1 hari |
        | **Pencampuran** | Aduk rata pupuk dengan tanah | 1 hari |
        
        ---
        
        ### 2️⃣ Solarisasi (Penutupan Plastik)
        
        **Tujuan:**
        - Sterilisasi tanah dari patogen
        - Matikan gulma dan benih gulma
        - Tingkatkan suhu tanah (50-60°C)
        
        **Cara:**
        ```
        1. Siram tanah hingga basah merata
        2. Tutup dengan plastik transparan (UV 200 micron)
        3. Tekan pinggir dengan tanah/batu
        4. Biarkan 10-14 hari (cuaca cerah)
        5. Buka plastik, anginkan 2-3 hari sebelum tanam
        ```
        
        ---
        
        ### 3️⃣ Pembuatan Bedengan
        
        | Parameter | Ukuran |
        |:----------|:-------|
        | **Lebar bedengan** | 100-120 cm |
        | **Tinggi bedengan** | 20-30 cm |
        | **Jarak antar bedengan** | 40-50 cm |
        | **Panjang** | Sesuai greenhouse |
        
        **Tips:**
        - Permukaan rata dan padat
        - Kemiringan drainase 1-2%
        - Pasang selang irigasi sebelum tanam
        """)
        
    # ========== SUB-TAB 3: BIBIT & TANAM ==========
    with kr_bibit:
        st.subheader("🌿 Penyiapan Bibit & Tanam")
        
        st.markdown("""
        ### 1️⃣ Sumber Bibit
        
        **Dari Mother Plant (Indukan):**
        ```
        - Pilih tanaman induk sehat, produktif
        - Umur indukan: 3-6 bulan
        - Potong stek pucuk 8-10 cm (3-4 daun)
        - Buang daun bawah, sisakan 2-3 daun atas
        ```
        
        ---
        
        ### 2️⃣ Perlakuan Stek
        
        | Langkah | Detail |
        |:--------|:-------|
        | **Hormon** | Celup pangkal ke IBA 500-1000 ppm (5 detik) |
        | **Media Rooting** | Cocopeat : Perlite = 1:1 |
        | **Wadah** | Tray semai 72-128 lubang |
        | **Kelembaban** | Tutup plastik/misting, RH 80-90% |
        | **Durasi** | 10-14 hari sampai berakar |
        
        ---
        
        ### 3️⃣ Jarak Tanam
        
        | Konfigurasi | Jarak | Populasi |
        |:------------|:------|:---------|
        | **Standar** | 12.5 × 12.5 cm | 64 tanaman/m² |
        | **Rapat** | 10 × 10 cm | 100 tanaman/m² |
        | **Longgar** | 15 × 15 cm | 44 tanaman/m² |
        
        ---
        
        ### 4️⃣ Teknik Tanam
        
        ```
        1. Buat lubang tanam kedalaman 3-5 cm
        2. Masukkan bibit berakar
        3. Padatkan tanah di sekitar pangkal
        4. Siram langsung setelah tanam
        5. Pasang mulsa plastik hitam perak (opsional)
        ```
        """)
        
    # ========== SUB-TAB 4: SISTEM NET ==========
    with kr_net:
        st.subheader("🕸️ Sistem Penopang Net")
        
        st.markdown("""
        ### 🎯 Fungsi Net
        
        - **Menegakkan batang** agar tidak rebah
        - **Menjaga kerapatan** jarak tanam
        - **Memudahkan panen** dengan batang lurus
        
        ---
        
        ### 📐 Spesifikasi Net
        
        | Parameter | Ukuran |
        |:----------|:-------|
        | **Bahan** | Jaring nylon/plastik |
        | **Mesh Size** | 12.5 × 12.5 cm |
        | **Lebar** | Sesuai bedengan (100-120 cm) |
        | **Layer** | 4-5 layer bertahap |
        """)
        
        st.markdown("### 📅 Jadwal Angkat Net")
        
        net_schedule = pd.DataFrame({
            "Layer": ["Net 1", "Net 2", "Net 3", "Net 4", "Net 5"],
            "HST": [7, 21, 35, 49, 63],
            "Tinggi (cm)": [15, 30, 45, 60, 75],
            "Keterangan": [
                "Pasang pertama, tanaman masih pendek",
                "Tanaman mulai tinggi, angkat net",
                "Fase vegetatif aktif",
                "Mulai generatif, batang mengeras",
                "Posisi final, siap panen"
            ]
        })
        
        st.dataframe(net_schedule, use_container_width=True, hide_index=True)
        
        st.info("""
        💡 **Tips:**
        - Angkat net perlahan (jangan sampai batang patah)
        - Pastikan semua tanaman masuk lubang net
        - Gunakan tiang bambu/besi sebagai penyangga net
        """)
        
    # ========== SUB-TAB 5: IRIGASI & NUTRISI ==========
    with kr_irigasi:
        st.subheader("💧 Sistem Irigasi & Pemupukan")
        
        st.markdown("""
        ### 1️⃣ Sistem Irigasi Nozzle/Sprinkler
        
        | Parameter | Setting |
        |:----------|:--------|
        | **Tipe** | Sprinkler overhead / Nozzle misting |
        | **Tekanan** | 2-3 bar |
        | **Frekuensi** | 2-3x/hari |
        | **Durasi** | 5-10 menit/sesi |
        | **Waktu** | Pagi (06:00), Siang (12:00), Sore (16:00) |
        
        ---
        
        ### 2️⃣ Pola Pupuk Dasar
        """)
        
        pupuk_schedule = pd.DataFrame({
            "Fase": ["Vegetatif", "Vegetatif", "Transisi", "Generatif", "Generatif"],
            "HST": ["7-28", "28-35", "35-42", "42-70", "70+"],
            "Pupuk": ["NPK 16-16-16", "NPK 16-16-16 + Urea", "NPK 10-30-20", "NPK 10-10-40", "KNO₃"],
            "Dosis": ["2-3 g/L", "2 g/L + 1 g/L", "2 g/L", "2-3 g/L", "1-2 g/L"],
            "Frekuensi": ["2x/minggu", "2x/minggu", "2x/minggu", "2x/minggu", "1x/minggu"],
            "Tujuan": ["Pertumbuhan awal", "Dorong vegetatif", "Inisiasi bunga", "Pembungaan", "Warna bunga"]
        })
        
        st.dataframe(pupuk_schedule, use_container_width=True, hide_index=True)
        
        st.markdown("""
        ---
        
        ### 3️⃣ Penyemprotan Rutin
        
        | Aplikasi | Bahan | Frekuensi |
        |:---------|:------|:----------|
        | **Fungisida** | Mancozeb, Propineb | 1x/minggu |
        | **Insektisida** | Abamectin, Imidacloprid | 1x/minggu |
        | **Pupuk Daun** | Gandasil D/B | 1x/minggu |
        | **ZPT** | Gibberellin (opsional) | 2x selama vegetatif |
        """)
        
    # ========== SUB-TAB 6: SISTEM LAMPU ==========
    with kr_lampu:
        st.subheader("💡 Sistem Lampu Otomatis (Photoperiod)")
        
        st.markdown("""
        ### 🎯 Prinsip Photoperiod Krisan
        
        Krisan adalah **Short Day Plant** (tanaman hari pendek):
        - **Long Day (LD)**: 16+ jam terang → tetap VEGETATIF
        - **Short Day (SD)**: 10-12 jam terang → BERBUNGA
        
        ---
        
        ### 💡 Pengaturan Lampu
        
        | Fase | Durasi Terang | Durasi | Tujuan |
        |:-----|:--------------|:-------|:-------|
        | **Long Day** | 16-18 jam | HST 1-35 | Pertumbuhan batang tinggi |
        | **Transisi** | 14 jam | HST 35-42 | Penyesuaian |
        | **Short Day** | 10-12 jam | HST 42+ | Induksi pembungaan |
        
        ---
        
        ### ⚙️ Setup Teknis
        
        | Parameter | Rekomendasi |
        |:----------|:------------|
        | **Tipe Lampu** | LED grow light / Incandescent 100W |
        | **Intensitas** | Minimal 10 lux di permukaan tanaman |
        | **Tinggi Lampu** | 2-3 m dari permukaan tanah |
        | **Jarak Antar Lampu** | 3-4 m |
        | **Timer** | Digital timer ON/OFF otomatis |
        
        ---
        
        ### ⏰ Contoh Setting Timer
        
        **Long Day (HST 1-35):**
        ```
        Lampu ON : 04:00 - 08:00 (4 jam pagi)
        Lampu ON : 17:00 - 21:00 (4 jam sore)
        Total    : 8 jam tambahan + 8 jam siang = 16 jam terang
        ```
        
        **Short Day (HST 42+):**
        ```
        Lampu OFF, andalkan cahaya matahari alami
        Durasi terang alami: ~11-12 jam
        ```
        """)
        
    # ========== SUB-TAB 7: MESIN DAMBO ==========
    with kr_dambo:
        st.subheader("🔥 Mesin Dambo (Pengasapan CO₂)")
        
        st.markdown("""
        ### 🎯 Fungsi Mesin Dambo
        
        1. **Meningkatkan CO₂** di greenhouse (optimal 800-1200 ppm)
        2. **Pengendalian hama** melalui asap
        3. **Meningkatkan fotosintesis** → bunga lebih besar
        
        ---
        
        ### ⚙️ Spesifikasi Mesin Dambo
        
        | Parameter | Nilai |
        |:----------|:------|
        | **Bahan Bakar** | Solar / Minyak Tanah |
        | **Konsumsi BBM** | 0.5 - 1 Liter/jam |
        | **Kapasitas** | 1 unit per 500-1000 m² |
        | **Output** | Asap CO₂ + uap air |
        
        ---
        
        ### ⏰ Jadwal Pengoperasian
        """)
        
        dambo_schedule = pd.DataFrame({
            "Parameter": ["Waktu Operasi", "Durasi", "Frekuensi", "Fase Aktif"],
            "Setting": ["21:00 - 05:00 (malam)", "2-3 jam/malam", "2-3x per minggu", "HST 14 - Panen"]
        })
        
        st.dataframe(dambo_schedule, use_container_width=True, hide_index=True)
        
        st.markdown("""
        ---
        
        ### 📊 Kalkulasi Bahan Bakar
        """)
        
        dambo_col1, dambo_col2 = st.columns(2)
        
        with dambo_col1:
            durasi_per_malam = st.number_input("Durasi per Malam (jam)", 1.0, 5.0, 2.5, 0.5)
            frekuensi_minggu = st.number_input("Frekuensi per Minggu", 1, 7, 3, 1)
            durasi_tanam = st.number_input("Durasi Tanam (minggu)", 8, 16, 12, 1)
            harga_bbm = st.number_input("Harga BBM (Rp/L)", 5000, 20000, 7000, 500)
        
        with dambo_col2:
            konsumsi_per_jam = 0.75  # L/jam (rata-rata)
            total_jam = durasi_per_malam * frekuensi_minggu * durasi_tanam
            total_bbm = total_jam * konsumsi_per_jam
            total_biaya = total_bbm * harga_bbm
            
            st.metric("Total Jam Operasi", f"{total_jam:.0f} jam")
            st.metric("Total BBM", f"{total_bbm:.1f} Liter")
            st.metric("Total Biaya BBM", f"Rp {total_biaya:,.0f}")
        
    # ========== SUB-TAB 8: PANEN ==========
    with kr_panen:
        st.subheader("🌾 Panen")
        
        st.markdown("""
        ### 📅 Waktu Panen Berdasarkan Durasi Tanam
        
        | Durasi | Grade Target | Karakteristik |
        |:-------|:-------------|:--------------|
        | **90 hari** | Grade 60-80 | Batang pendek, bunga kecil |
        | **100 hari** | Grade 80-100 | Batang sedang, bunga sedang |
        | **110 hari** | Grade 100-120 | Batang tinggi, bunga besar |
        | **120 hari** | Grade 120-160 | Batang premium, bunga premium |
        
        ---
        
        ### ✅ Kriteria Panen
        
        | Kriteria | Standar |
        |:---------|:--------|
        | **Tahap Bunga** | 2-3 kuntum bunga sudah mekar |
        | **Warna** | Warna bunga sudah optimal/stabil |
        | **Kekuatan Batang** | Batang keras, tidak mudah patah |
        | **Waktu Panen** | Pagi hari (05:00-08:00) sebelum matahari terik |
        
        ---
        
        ### 🔪 Teknik Panen
        
        ```
        1. Siram tanaman sehari sebelum panen (sore hari)
        2. Panen pagi hari (tangkai lebih segar)
        3. Potong di pangkal batang dekat tanah
        4. Langsung masukkan ke ember berisi air bersih
        5. Pindahkan ke tempat teduh untuk processing
        ```
        """)
        
    # ========== SUB-TAB 9: PASCA PANEN ==========
    with kr_pasca:
        st.subheader("✂️ Penanganan Pasca Panen")
        
        st.markdown("""
        ### 📋 Alur Pasca Panen
        
        ```
        Panen → Rendam → Ratakan → Potong → Ikat → Plastik → Packing
        ```
        
        ---
        
        ### 1️⃣ Perendaman
        
        | Parameter | Detail |
        |:----------|:-------|
        | **Wadah** | Ember besar / bak plastik |
        | **Larutan** | Air bersih + preservative (Chrysal/Floralife) |
        | **Durasi** | 2-4 jam (hidrasi) |
        | **Suhu** | Air dingin (15-20°C) |
        
        ---
        
        ### 2️⃣ Perataan (Grading Awal)
        
        - Ratakan tinggi batang di meja sortir
        - Kelompokkan berdasarkan tinggi (90cm, 80cm, 70cm)
        - Pisahkan bunga rusak/cacat
        
        ---
        
        ### 3️⃣ Pemotongan
        
        | Alat | Fungsi |
        |:-----|:-------|
        | **Mesin Potong** | Potong pangkal batang rata (sesuai ukuran grade) |
        | **Gunting Tajam** | Potong manual untuk grade rusak |
        
        **Panjang Standar:**
        - Grade A: 90 cm
        - Grade B (rusak sedikit): 80 cm
        - Grade C (rusak): 70 cm
        
        ---
        
        ### 4️⃣ Pengikatan
        
        | Parameter | Standar |
        |:----------|:--------|
        | **Alat Ikat** | Karet gelang / tali plastik |
        | **Posisi Ikat** | 2 titik (10 cm dari pangkal, 30 cm dari pangkal) |
        | **Jumlah per Ikat** | Sesuai grade (60/80/100/120/160 batang) |
        
        ---
        
        ### 5️⃣ Pemasangan Plastik Pelindung
        
        ```
        - Plastik sleeve transparan (panjang 50-70 cm)
        - Masukkan dari atas (bunga masuk duluan)
        - Fungsi: Lindungi bunga dari benturan
        ```
        """)
        
    # ========== SUB-TAB 10: GRADING & PACKING ==========
    with kr_grading:
        st.subheader("📦 Sistem Grading & Packing")
        
        st.markdown("""
        ### 🎯 Sistem Grading Krisan Spray
        
        **Angka Grade = Jumlah Batang per Ikat (Bundle)**
        
        > Contoh: **Grade 80** = 1 ikat berisi **80 batang** krisan
        
        ---
        
        ### ✅ Grade Normal (Kualitas A) - Panjang 90 cm
        """)
        
        grade_normal = pd.DataFrame({
            "Grade": [60, 80, 100, 120, 160],
            "Jumlah Batang": ["60 batang/ikat", "80 batang/ikat", "100 batang/ikat", "120 batang/ikat", "160 batang/ikat"],
            "Panjang": ["90 cm", "90 cm", "90 cm", "90 cm", "90 cm"],
            "Keterangan": ["Ekonomis", "Standar", "Premium", "Super", "Jumbo"]
        })
        
        st.dataframe(grade_normal, use_container_width=True, hide_index=True)
        
        st.markdown("""
        ---
        
        ### ⚠️ Grade Rusak/BS (Kualitas B) - Panjang di Bawah Standar
        """)
        
        grade_rusak = pd.DataFrame({
            "Grade": ["R-80", "R-100", "R-160", "R-200"],
            "Jumlah Batang": ["80 batang", "100 batang", "160 batang", "200 batang"],
            "Panjang": ["80 cm", "80 cm", "70 cm", "70 cm"],
            "Alasan": ["Sedikit pendek", "Sedikit pendek", "Pendek", "Sangat pendek"],
            "Pasar": ["Lokal", "Lokal", "Lokal", "Lokal"]
        })
        
        st.dataframe(grade_rusak, use_container_width=True, hide_index=True)
        
        st.markdown("""
        ---
        
        ### 📦 Standar Packing
        
        | Kemasan | Isi | Keterangan |
        |:--------|:----|:-----------|
        | **Karton Box** | 10-20 ikat | Untuk ekspor/jarak jauh |
        | **Bucket** | 5-10 ikat | Untuk pasar lokal |
        | **Plastik Wrap** | Per ikat | Perlindungan tambahan |
        """)
        
        st.divider()
        
        # ========== ENHANCED CALCULATORS ==========
        st.subheader("🧮 Kalkulator Budidaya Krisan Spray")
        
        calc_tabs = st.tabs(["🌱 Populasi Tanaman", "💧 Nozzle & Irigasi", "💰 RAB Lengkap", "🤖 AI Optimasi"])
        
        # ===== TAB 1: POPULASI TANAMAN =====
        with calc_tabs[0]:
            st.markdown("### 🌱 Kalkulator Populasi Berdasarkan Bedengan")
            
            pop_col1, pop_col2, pop_col3 = st.columns(3)
            
            with pop_col1:
                st.markdown("**Dimensi Bedengan:**")
                panjang_bedengan = st.number_input("Panjang Bedengan (m)", 5, 100, 30, 5, key="panjang_bed")
                jumlah_bedengan = st.number_input("Jumlah Bedengan", 1, 100, 10, 1)
                lebar_bedengan = st.number_input("Lebar Bedengan (cm)", 80, 150, 100, 10, key="lebar_bed")
            
            with pop_col2:
                st.markdown("**Konfigurasi Tanam:**")
                baris_per_bedengan = st.number_input("Jumlah Baris per Bedengan", 4, 12, 8, 1)
                jarak_dalam_baris = st.number_input("Jarak Dalam Baris (cm)", 8, 20, 12, 1)
                st.caption(f"💡 Jarak antar baris ≈ {lebar_bedengan / baris_per_bedengan:.1f} cm")
            
            with pop_col3:
                st.markdown("**Hasil Perhitungan:**")
                # Plants per row per bed
                tanaman_per_baris = int((panjang_bedengan * 100) / jarak_dalam_baris)
                # Plants per bed
                tanaman_per_bedengan = tanaman_per_baris * baris_per_bedengan
                # Total plants
                total_populasi = tanaman_per_bedengan * jumlah_bedengan
                # Area
                luas_bedengan = (lebar_bedengan/100) * panjang_bedengan
                total_luas = luas_bedengan * jumlah_bedengan
                populasi_per_m2 = total_populasi / total_luas if total_luas > 0 else 0
                
                st.metric("Tanaman per Bedengan", f"{tanaman_per_bedengan:,}")
                st.metric("🌿 Total Populasi", f"{total_populasi:,}")
                st.metric("Kepadatan", f"{populasi_per_m2:.0f}/m²")
            
            st.success(f"""
            **Ringkasan Populasi:**
            - Bedengan: {lebar_bedengan}cm × {panjang_bedengan}m = {luas_bedengan:.1f} m² × {jumlah_bedengan} = **{total_luas:.0f} m²**
            - Konfigurasi: {baris_per_bedengan} baris × {tanaman_per_baris} tanaman (jarak {jarak_dalam_baris}cm)
            - Per bedengan: **{tanaman_per_bedengan:,} tanaman**
            - Total: **{total_populasi:,} tanaman** ({populasi_per_m2:.0f}/m²)
            """)
        
        # ===== TAB 2: NOZZLE & IRIGASI =====
        with calc_tabs[1]:
            st.markdown("### 💧 Kalkulator Nozzle & Sistem Irigasi")
            
            noz_col1, noz_col2 = st.columns(2)
            
            with noz_col1:
                st.markdown("**Pipa Irigasi:**")
                panjang_pipa = st.number_input("Panjang Pipa per Bedengan (m)", 5, 100, 30, 5, key="pipa")
                jarak_nozzle = st.number_input("Jarak Antar Nozzle (cm)", 20, 50, 30, 5)
                jumlah_pipa = st.number_input("Jumlah Pipa (= Jumlah Bedengan)", 1, 100, 10, 1, key="jml_pipa")
                
                st.markdown("**Harga Komponen:**")
                harga_nozzle = st.number_input("Harga per Nozzle (Rp)", 1000, 10000, 3000, 500)
                harga_pipa_per_m = st.number_input("Harga Pipa per Meter (Rp)", 5000, 50000, 15000, 1000)
            
            with noz_col2:
                st.markdown("**Hasil Perhitungan:**")
                # Nozzle per pipe
                nozzle_per_pipa = int((panjang_pipa * 100) / jarak_nozzle)
                # Total nozzle
                total_nozzle = nozzle_per_pipa * jumlah_pipa
                # Total pipe length
                total_panjang_pipa = panjang_pipa * jumlah_pipa
                # Costs
                biaya_nozzle = total_nozzle * harga_nozzle
                biaya_pipa = total_panjang_pipa * harga_pipa_per_m
                total_irigasi = biaya_nozzle + biaya_pipa
                
                st.metric("Nozzle per Pipa", f"{nozzle_per_pipa} unit")
                st.metric("💧 Total Nozzle", f"{total_nozzle:,} unit")
                st.metric("Total Pipa", f"{total_panjang_pipa:,} m")
            
            st.divider()
            
            irg_cost1, irg_cost2, irg_cost3 = st.columns(3)
            with irg_cost1:
                st.metric("Biaya Nozzle", f"Rp {biaya_nozzle:,}")
            with irg_cost2:
                st.metric("Biaya Pipa", f"Rp {biaya_pipa:,}")
            with irg_cost3:
                st.metric("💰 Total Irigasi", f"Rp {total_irigasi:,}")
        
        # ===== TAB 3: RAB LENGKAP =====
        with calc_tabs[2]:
            st.markdown("### 💰 Rencana Anggaran Biaya (RAB) Lengkap")
            
            # Show synced data from other tabs
            st.success(f"""
            **📊 Data Tersinkronisasi dari Tab Lain:**
            - 🌱 Populasi: **{total_populasi:,} tanaman** | Luas: **{total_luas:.0f} m²**
            - 💧 Irigasi: **{total_nozzle:,} nozzle** | Biaya Instalasi: **Rp {total_irigasi:,}**
            """)
            
            # ===== SECTION 1: MODAL / CAPEX (Investasi Awal) =====
            with st.expander("🏗️ **INVESTASI MODAL (CAPEX)** - Aset Jangka Panjang", expanded=True):
                st.caption("Modal awal tidak dihitung dalam ROI per siklus, tapi diperhitungkan sebagai penyusutan")
                
                capex_col1, capex_col2 = st.columns(2)
                
                with capex_col1:
                    st.markdown("**🏠 Infrastruktur:**")
                    modal_greenhouse = st.number_input("Biaya Greenhouse (Rp)", 10000000, 500000000, 100000000, 5000000)
                    modal_irigasi = total_irigasi  # From synced tab
                    st.metric("Biaya Sistem Irigasi (Sync)", f"Rp {modal_irigasi:,}")
                    modal_lampu = st.number_input("Biaya Instalasi Lampu (Rp)", 1000000, 50000000, 10000000, 1000000)
                
                with capex_col2:
                    st.markdown("**⚙️ Peralatan & Penyusutan:**")
                    modal_peralatan = st.number_input("Biaya Peralatan Lain (Rp)", 0, 50000000, 5000000, 1000000)
                    umur_ekonomis = st.number_input("Umur Ekonomis Aset (tahun)", 3, 20, 10, 1)
                    siklus_per_tahun = st.number_input("Jumlah Siklus per Tahun", 2, 4, 3, 1)
                
                # Calculate CAPEX totals and depreciation
                total_modal = modal_greenhouse + modal_irigasi + modal_lampu + modal_peralatan
                penyusutan_per_tahun = total_modal / umur_ekonomis
                penyusutan_per_siklus = penyusutan_per_tahun / siklus_per_tahun
                
                capex_result1, capex_result2, capex_result3 = st.columns(3)
                with capex_result1:
                    st.metric("💰 Total Modal", f"Rp {total_modal:,.0f}")
                with capex_result2:
                    st.metric("📉 Penyusutan/Tahun", f"Rp {penyusutan_per_tahun:,.0f}")
                with capex_result3:
                    st.metric("📉 Penyusutan/Siklus", f"Rp {penyusutan_per_siklus:,.0f}")
            
            st.divider()
            
            # ===== SECTION 2: BIAYA OPERASIONAL / OPEX (Per Siklus) =====
            st.markdown("### 📋 BIAYA OPERASIONAL (OPEX) - Per Siklus Tanam")
            
            rab_col1, rab_col2 = st.columns(2)
            
            with rab_col1:
                st.markdown("**🌱 Bahan Tanam:**")
                harga_bibit = st.number_input("Harga Bibit (Rp/batang)", 100, 1000, 300, 50)
                
                st.markdown("**🧪 Pupuk & Pestisida:**")
                biaya_pupuk_per_m2 = st.number_input("Biaya Pupuk (Rp/m²/siklus)", 500, 5000, 1500, 100)
                biaya_pestisida_per_m2 = st.number_input("Biaya Pestisida (Rp/m²/siklus)", 500, 3000, 1000, 100)
                
                st.markdown("**💡 Listrik & Utilitas:**")
                biaya_listrik_per_bulan = st.number_input("Biaya Listrik (Rp/bulan)", 500000, 5000000, 1500000, 100000)
                durasi_tanam_bulan = st.number_input("Durasi Tanam (bulan)", 3, 5, 4, 1)
            
            with rab_col2:
                st.markdown("**👷 Tenaga Kerja (Termasuk Tanam):**")
                jumlah_pekerja = st.number_input("Jumlah Pekerja", 1, 20, 3, 1)
                upah_per_bulan = st.number_input("Upah per Pekerja (Rp/bulan)", 1000000, 5000000, 2500000, 100000)
                st.caption("💡 Upah tanam sudah termasuk dalam biaya tenaga kerja")
                
                st.markdown("**🔥 Operasional Lainnya:**")
                biaya_dambo = st.number_input("Biaya BBM Dambo (Rp/siklus)", 100000, 1000000, 300000, 50000)
                biaya_packing = st.number_input("Biaya Packing (Rp/ikat)", 500, 3000, 1500, 100)
                biaya_lainnya = st.number_input("Biaya Lain-lain (Rp)", 0, 5000000, 500000, 100000)
            
            st.divider()
            
            # Use synced values directly
            pop_for_rab = total_populasi
            luas_for_rab = total_luas
            
            st.markdown("**📊 Parameter Pendapatan:**")
            rab_rev_col1, rab_rev_col2, rab_rev_col3 = st.columns(3)
            with rab_rev_col1:
                survival_rab = st.slider("Survival Rate (%)", 70, 95, 85, 5, key="surv_rab")
            with rab_rev_col2:
                grade_rab = st.selectbox("Grade Rata-rata", [60, 80, 100, 120, 160], index=1, key="grade_rab")
            with rab_rev_col3:
                harga_jual_rab = st.number_input("Harga Jual (Rp/ikat)", 50000, 200000, 80000, 5000, key="harga_rab")
            
            st.divider()
            st.markdown("### 📊 Hasil Perhitungan RAB")
            
            # Calculate OPEX costs (no more biaya_tanam_total, merged into TK)
            biaya_bibit_total = pop_for_rab * harga_bibit
            biaya_pupuk_total = luas_for_rab * biaya_pupuk_per_m2
            biaya_pestisida_total = luas_for_rab * biaya_pestisida_per_m2
            biaya_listrik_total = biaya_listrik_per_bulan * durasi_tanam_bulan
            biaya_tenaga_kerja = jumlah_pekerja * upah_per_bulan * durasi_tanam_bulan  # Now includes all labor
            
            # Revenue
            tanaman_panen_rab = pop_for_rab * (survival_rab / 100)
            jumlah_ikat_rab = tanaman_panen_rab / grade_rab
            pendapatan_kotor = jumlah_ikat_rab * harga_jual_rab
            biaya_packing_total = jumlah_ikat_rab * biaya_packing
            
            # Total OPEX (includes depreciation, NOT full modal)
            total_opex = (biaya_bibit_total + biaya_pupuk_total + biaya_pestisida_total + 
                          biaya_listrik_total + biaya_tenaga_kerja + 
                          penyusutan_per_siklus + biaya_dambo + biaya_packing_total + biaya_lainnya)
            
            laba_operasional = pendapatan_kotor - total_opex
            roi_operasional = (laba_operasional / total_opex) * 100 if total_opex > 0 else 0
            
            # Payback period
            payback_siklus = total_modal / laba_operasional if laba_operasional > 0 else float('inf')
            payback_tahun = payback_siklus / siklus_per_tahun if laba_operasional > 0 else float('inf')
            
            # Display RAB Table (OPEX only, with depreciation)
            rab_data = pd.DataFrame({
                "Komponen": [
                    "🌱 Bibit", "🧪 Pupuk", "🧴 Pestisida",
                    "💡 Listrik", "👷 Tenaga Kerja", "📉 Penyusutan", 
                    "🔥 Dambo", "📦 Packing", "📋 Lain-lain"
                ],
                "Biaya (Rp)": [
                    biaya_bibit_total, biaya_pupuk_total, biaya_pestisida_total,
                    biaya_listrik_total, biaya_tenaga_kerja, penyusutan_per_siklus,
                    biaya_dambo, biaya_packing_total, biaya_lainnya
                ]
            })
            
            st.dataframe(rab_data, use_container_width=True, hide_index=True)
            
            # Keep total_biaya for backward compatibility with other sections
            total_biaya = total_opex
            
            rab_result1, rab_result2, rab_result3, rab_result4 = st.columns(4)
            with rab_result1:
                st.metric("Total OPEX", f"Rp {total_opex:,.0f}")
            with rab_result2:
                st.metric("Pendapatan", f"Rp {pendapatan_kotor:,.0f}")
            with rab_result3:
                st.metric("Laba Operasional", f"Rp {laba_operasional:,.0f}", 
                         delta="Profit" if laba_operasional > 0 else "Loss")
            with rab_result4:
                st.metric("ROI per Siklus", f"{roi_operasional:.1f}%")
            
            # Payback Period Analysis
            st.divider()
            st.markdown("### 📈 Analisis Payback Period")
            
            payback_col1, payback_col2, payback_col3 = st.columns(3)
            with payback_col1:
                st.metric("💰 Total Modal", f"Rp {total_modal:,.0f}")
            with payback_col2:
                if payback_siklus != float('inf'):
                    st.metric("🔄 Payback (Siklus)", f"{payback_siklus:.1f} siklus")
                else:
                    st.metric("🔄 Payback (Siklus)", "∞ (Rugi)")
            with payback_col3:
                if payback_tahun != float('inf'):
                    st.metric("📅 Payback (Tahun)", f"{payback_tahun:.1f} tahun")
                else:
                    st.metric("📅 Payback (Tahun)", "∞ (Rugi)")
            
            # Keep these for backward compatibility with grading section
            laba_bersih = laba_operasional
            roi = roi_operasional
            
            # ===== BIAYA PER BATANG =====
            st.divider()
            st.markdown("### 💰 Analisis Biaya per Batang")
            
            biaya_per_batang = total_biaya / pop_for_rab if pop_for_rab > 0 else 0
            biaya_per_batang_panen = total_biaya / tanaman_panen_rab if tanaman_panen_rab > 0 else 0
            
            bpb_col1, bpb_col2, bpb_col3 = st.columns(3)
            with bpb_col1:
                st.metric("💵 Biaya per Batang (Tanam)", f"Rp {biaya_per_batang:,.0f}")
            with bpb_col2:
                st.metric("💵 Biaya per Batang (Panen)", f"Rp {biaya_per_batang_panen:,.0f}")
            with bpb_col3:
                margin_per_batang = (harga_jual_rab / grade_rab) - biaya_per_batang_panen
                st.metric("📈 Margin per Batang", f"Rp {margin_per_batang:,.0f}",
                         delta="Profit" if margin_per_batang > 0 else "Loss")
            
            # ===== INPUT HASIL GRADING =====
            st.divider()
            st.markdown("### 📦 Input Hasil Grading Aktual")
            
            st.info(f"💡 Masukkan hasil grading dari panen. Potensi tanaman panen: **{tanaman_panen_rab:,.0f}** batang")
            
            # Default prices per grade
            default_prices = {
                60: 60000,
                80: 80000,
                100: 100000,
                120: 120000,
                160: 160000
            }
            
            # Default prices for B-grade (rusak) - lower prices for shorter stems
            default_prices_rusak = {
                "R-80": 40000,    # 80 batang, panjang 80cm
                "R-100": 50000,   # 100 batang, panjang 80cm
                "R-160": 60000,   # 160 batang, panjang 70cm
                "R-200": 70000    # 200 batang, panjang 70cm
            }
            
            # Stem counts for rusak grades
            rusak_batang = {
                "R-80": 80,
                "R-100": 100,
                "R-160": 160,
                "R-200": 200
            }
            
            use_custom_prices = st.checkbox("Sesuaikan harga per grade", value=False)
            
            # ===== GRADE NORMAL (Panjang 90cm) =====
            st.markdown("#### ✅ Grade Normal (Panjang 90 cm)")
            grading_cols = st.columns(5)
            grades = [60, 80, 100, 120, 160]
            grade_inputs = {}
            grade_prices = {}
            
            for i, grade in enumerate(grades):
                with grading_cols[i]:
                    st.markdown(f"**Grade {grade}**")
                    grade_inputs[grade] = st.number_input(
                        f"Jumlah Ikat", min_value=0, max_value=1000, value=0, 
                        key=f"grade_{grade}_qty"
                    )
                    if use_custom_prices:
                        grade_prices[grade] = st.number_input(
                            f"Harga (Rp)", min_value=30000, max_value=200000, 
                            value=default_prices[grade], step=5000, key=f"grade_{grade}_price"
                        )
                    else:
                        grade_prices[grade] = default_prices[grade]
                        st.caption(f"Rp {default_prices[grade]:,}")
            
            # ===== GRADE RUSAK / B-GRADE (Panjang < 90cm) =====
            st.markdown("#### ⚠️ Grade Rusak/BS (Panjang 70-80 cm)")
            st.caption("Untuk bunga dengan batang lebih pendek dari standar")
            
            rusak_cols = st.columns(4)
            grades_rusak = ["R-80", "R-100", "R-160", "R-200"]
            rusak_inputs = {}
            rusak_prices = {}
            
            for i, grade in enumerate(grades_rusak):
                with rusak_cols[i]:
                    panjang = "80cm" if grade in ["R-80", "R-100"] else "70cm"
                    st.markdown(f"**{grade}**")
                    st.caption(f"({rusak_batang[grade]} btg, {panjang})")
                    rusak_inputs[grade] = st.number_input(
                        f"Jml Ikat", min_value=0, max_value=500, value=0, 
                        key=f"grade_{grade}_qty"
                    )
                    if use_custom_prices:
                        rusak_prices[grade] = st.number_input(
                            f"Harga", min_value=20000, max_value=100000, 
                            value=default_prices_rusak[grade], step=5000, key=f"grade_{grade}_price"
                        )
                    else:
                        rusak_prices[grade] = default_prices_rusak[grade]
                        st.caption(f"Rp {default_prices_rusak[grade]:,}")
            
            # Calculate grading results (normal + rusak)
            total_ikat_normal = sum(grade_inputs.values())
            total_batang_normal = sum(grade * qty for grade, qty in grade_inputs.items())
            total_pendapatan_normal = sum(grade_prices[g] * grade_inputs[g] for g in grades)
            
            total_ikat_rusak = sum(rusak_inputs.values())
            total_batang_rusak = sum(rusak_batang[g] * rusak_inputs[g] for g in grades_rusak)
            total_pendapatan_rusak = sum(rusak_prices[g] * rusak_inputs[g] for g in grades_rusak)
            
            # Combined totals
            total_ikat_grading = total_ikat_normal + total_ikat_rusak
            total_batang_grading = total_batang_normal + total_batang_rusak
            total_pendapatan_grading = total_pendapatan_normal + total_pendapatan_rusak
            
            # ===== VALIDATION: Check against potential harvest =====
            potensi_panen = int(tanaman_panen_rab)
            persen_terisi = (total_batang_grading / potensi_panen * 100) if potensi_panen > 0 else 0
            sisa_batang = potensi_panen - total_batang_grading
            
            st.markdown("---")
            st.markdown(f"**📊 Progress Grading:** {total_batang_grading:,} / {potensi_panen:,} batang")
            
            # Progress bar with color coding
            if persen_terisi <= 100:
                st.progress(min(persen_terisi / 100, 1.0))
                if persen_terisi == 0:
                    st.info(f"💡 Masukkan data grading. Tersedia: **{potensi_panen:,}** batang")
                elif persen_terisi < 85:
                    st.info(f"📝 Sudah diinput: **{persen_terisi:.1f}%** | Sisa: **{sisa_batang:,}** batang")
                elif persen_terisi < 100:
                    st.success(f"✅ Hampir lengkap: **{persen_terisi:.1f}%** | Sisa: **{sisa_batang:,}** batang")
                else:
                    st.success(f"✅ Grading selesai: **100%** ({total_batang_grading:,} batang)")
            else:
                st.progress(1.0)
                selisih = total_batang_grading - potensi_panen
                st.error(f"""
                ⚠️ **MELEBIHI BATAS!** Input grading ({total_batang_grading:,} btg) melebihi potensi panen ({potensi_panen:,} btg)
                
                Kelebihan: **{selisih:,} batang** ({persen_terisi - 100:.1f}% lebih)
                
                Silakan kurangi jumlah ikat pada salah satu grade.
                """)
            st.markdown("### 📊 Visualisasi & Hasil Grading")
            
            if total_ikat_grading > 0:
                viz_col1, viz_col2 = st.columns([2, 1])
                
                with viz_col1:
                    # Pie chart for grade distribution (normal + rusak)
                    # Normal grades data
                    normal_data = [
                        {"Grade": f"Grade {g} (90cm)", "Batang": g * grade_inputs[g], "Tipe": "Normal"}
                        for g in grades if grade_inputs[g] > 0
                    ]
                    # Rusak grades data
                    rusak_data = [
                        {"Grade": f"{g} ({('80cm' if g in ['R-80', 'R-100'] else '70cm')})", 
                         "Batang": rusak_batang[g] * rusak_inputs[g], "Tipe": "Rusak"}
                        for g in grades_rusak if rusak_inputs[g] > 0
                    ]
                    
                    all_grade_data = pd.DataFrame(normal_data + rusak_data)
                    
                    if len(all_grade_data) > 0:
                        fig_grade = px.pie(
                            all_grade_data, 
                            values="Batang", 
                            names="Grade",
                            title="Distribusi Batang per Grade (Normal + Rusak)",
                            color="Tipe",
                            color_discrete_map={"Normal": "#10b981", "Rusak": "#f59e0b"}
                        )
                        st.plotly_chart(fig_grade, use_container_width=True)
                        
                        # Show breakdown
                        brk_col1, brk_col2 = st.columns(2)
                        with brk_col1:
                            st.metric("✅ Normal", f"{total_batang_normal:,} btg", 
                                     delta=f"{total_ikat_normal} ikat")
                        with brk_col2:
                            st.metric("⚠️ Rusak", f"{total_batang_rusak:,} btg", 
                                     delta=f"{total_ikat_rusak} ikat")
                
                with viz_col2:
                    st.markdown("**📈 Ringkasan Hasil:**")
                    st.metric("Total Ikat", f"{total_ikat_grading:,}")
                    st.metric("Total Batang", f"{total_batang_grading:,}")
                    st.metric("💰 Pendapatan Aktual", f"Rp {total_pendapatan_grading:,}")
                    
                    # Comparison
                    laba_aktual = total_pendapatan_grading - total_biaya
                    roi_aktual = (laba_aktual / total_biaya) * 100 if total_biaya > 0 else 0
                    st.metric("Laba Aktual", f"Rp {laba_aktual:,.0f}",
                             delta="Profit" if laba_aktual > 0 else "Loss")
                    st.metric("ROI Aktual", f"{roi_aktual:.1f}%")
                
                # Comparison table
                st.divider()
                st.markdown("### 📊 Perbandingan: Potensi vs Aktual")
                
                comparison_data = pd.DataFrame({
                    "Metrik": [
                        "Tanaman Tanam", 
                        "Tanaman Panen (Est vs Aktual)", 
                        "Rp/Pendapatan",
                        "Laba Bersih",
                        "ROI"
                    ],
                    "Potensi (Estimasi)": [
                        f"{pop_for_rab:,.0f}",
                        f"{tanaman_panen_rab:,.0f}",
                        f"Rp {pendapatan_kotor:,.0f}",
                        f"Rp {laba_bersih:,.0f}",
                        f"{roi:.1f}%"
                    ],
                    "Aktual (Grading)": [
                        f"{pop_for_rab:,.0f}",
                        f"{total_batang_grading:,.0f}",
                        f"Rp {total_pendapatan_grading:,.0f}",
                        f"Rp {laba_aktual:,.0f}",
                        f"{roi_aktual:.1f}%"
                    ],
                    "Selisih": [
                        "0",
                        f"{total_batang_grading - tanaman_panen_rab:+,.0f}",
                        f"Rp {total_pendapatan_grading - pendapatan_kotor:+,.0f}",
                        f"Rp {laba_aktual - laba_bersih:+,.0f}",
                        f"{roi_aktual - roi:+.1f}%"
                    ]
                })
                
                st.dataframe(comparison_data, use_container_width=True, hide_index=True)
                
                # Survival comparison
                survival_aktual = (total_batang_grading / pop_for_rab) * 100 if pop_for_rab > 0 else 0
                
                surv_col1, surv_col2, surv_col3 = st.columns(3)
                with surv_col1:
                    st.metric("Survival Target", f"{survival_rab}%")
                with surv_col2:
                    st.metric("Survival Aktual", f"{survival_aktual:.1f}%")
                with surv_col3:
                    diff = survival_aktual - survival_rab
                    st.metric("Selisih", f"{diff:+.1f}%", 
                             delta="Lebih Baik" if diff > 0 else "Kurang")
                
                # ===== EXPORT & HISTORY SECTION =====
                st.divider()
                st.markdown("### 📥 Export & Histori Panen")
                
                exp_col1, exp_col2 = st.columns(2)
                
                with exp_col1:
                    st.markdown("#### 📊 Export RAB ke Excel")
                    
                    # Prepare export data
                    export_rab = pd.DataFrame({
                        "Kategori": ["CAPEX", "CAPEX", "CAPEX", "CAPEX", "CAPEX", 
                                    "OPEX", "OPEX", "OPEX", "OPEX", "OPEX", "OPEX", "OPEX", "OPEX", "OPEX",
                                    "HASIL", "HASIL", "HASIL", "HASIL"],
                        "Komponen": [
                            "Greenhouse", "Irigasi", "Lampu", "Peralatan", "Total Modal",
                            "Bibit", "Pupuk", "Pestisida", "Listrik", "Tenaga Kerja", 
                            "Penyusutan", "Dambo", "Packing", "Lain-lain",
                            "Pendapatan Kotor", "Total OPEX", "Laba Operasional", "ROI"
                        ],
                        "Nilai (Rp)": [
                            modal_greenhouse, modal_irigasi, modal_lampu, modal_peralatan, total_modal,
                            biaya_bibit_total, biaya_pupuk_total, biaya_pestisida_total, 
                            biaya_listrik_total, biaya_tenaga_kerja, penyusutan_per_siklus,
                            biaya_dambo, biaya_packing_total, biaya_lainnya,
                            pendapatan_kotor, total_opex, laba_operasional, f"{roi_operasional:.1f}%"
                        ]
                    })
                    
                    # Create grading export
                    export_grading = pd.DataFrame({
                        "Tipe": ["Normal"]*5 + ["Rusak"]*4,
                        "Grade": [60, 80, 100, 120, 160, "R-80", "R-100", "R-160", "R-200"],
                        "Jumlah Ikat": [grade_inputs.get(g, 0) for g in grades] + 
                                      [rusak_inputs.get(g, 0) for g in grades_rusak],
                        "Total Batang": [g * grade_inputs.get(g, 0) for g in grades] +
                                       [rusak_batang[g] * rusak_inputs.get(g, 0) for g in grades_rusak]
                    })
                    
                    # Download buttons
                    from io import BytesIO
                    
                    def to_excel():
                        output = BytesIO()
                        with pd.ExcelWriter(output, engine='openpyxl') as writer:
                            export_rab.to_excel(writer, sheet_name='RAB', index=False)
                            export_grading.to_excel(writer, sheet_name='Grading', index=False)
                        return output.getvalue()
                    
                    excel_data = to_excel()
                    st.download_button(
                        label="📥 Download RAB (Excel)",
                        data=excel_data,
                        file_name=f"RAB_Krisan_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                
                with exp_col2:
                    st.markdown("#### 📅 Simpan ke Histori Panen")
                    
                    # Initialize history in session state
                    if 'krisan_history' not in st.session_state:
                        st.session_state.krisan_history = []
                    
                    nama_siklus = st.text_input("Nama Siklus (contoh: Siklus Jan 2024)", 
                                               value=f"Siklus {datetime.datetime.now().strftime('%b %Y')}")
                    
                    if st.button("💾 Simpan ke Histori", type="primary"):
                        record = {
                            "nama": nama_siklus,
                            "tanggal": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "populasi": int(pop_for_rab),
                            "batang_panen": int(total_batang_grading),
                            "survival": round(survival_aktual, 1),
                            "pendapatan": int(total_pendapatan_grading),
                            "laba": int(laba_aktual),
                            "roi": round(roi_aktual, 1),
                            "normal_ikat": int(total_ikat_normal),
                            "rusak_ikat": int(total_ikat_rusak)
                        }
                        st.session_state.krisan_history.append(record)
                        st.success(f"✅ Disimpan: {nama_siklus}")
                
                # Show history
                if st.session_state.get('krisan_history'):
                    st.divider()
                    st.markdown("#### 📈 Histori Panen")
                    
                    history_df = pd.DataFrame(st.session_state.krisan_history)
                    history_df["Survival"] = history_df["survival"].astype(str) + "%"
                    history_df["ROI"] = history_df["roi"].astype(str) + "%"
                    history_df["Pendapatan"] = history_df["pendapatan"].apply(lambda x: f"Rp {x:,}")
                    history_df["Laba"] = history_df["laba"].apply(lambda x: f"Rp {x:,}")
                    
                    display_df = history_df[["nama", "tanggal", "batang_panen", "Survival", "Pendapatan", "Laba", "ROI"]]
                    display_df.columns = ["Siklus", "Tanggal", "Batang", "Survival", "Pendapatan", "Laba", "ROI"]
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                    
                    # Stats summary
                    if len(st.session_state.krisan_history) > 1:
                        hist_stats1, hist_stats2, hist_stats3 = st.columns(3)
                        with hist_stats1:
                            avg_roi = sum(r['roi'] for r in st.session_state.krisan_history) / len(st.session_state.krisan_history)
                            st.metric("Rata-rata ROI", f"{avg_roi:.1f}%")
                        with hist_stats2:
                            avg_surv = sum(r['survival'] for r in st.session_state.krisan_history) / len(st.session_state.krisan_history)
                            st.metric("Rata-rata Survival", f"{avg_surv:.1f}%")
                        with hist_stats3:
                            total_laba = sum(r['laba'] for r in st.session_state.krisan_history)
                            st.metric("Total Laba Kumulatif", f"Rp {total_laba:,}")
                    
                    if st.button("🗑️ Hapus Semua Histori"):
                        st.session_state.krisan_history = []
                        st.rerun()
            else:
                st.warning("⚠️ Masukkan data grading untuk melihat visualisasi dan perbandingan")
        
        # ===== TAB 4: AI OPTIMASI =====
        with calc_tabs[3]:
            st.markdown("### 🤖 AI Optimasi Budidaya Krisan")
            
            st.info("💡 AI akan menganalisis parameter Anda dan memberikan rekomendasi optimasi")
            
            if st.button("🔍 Jalankan Analisis AI", type="primary", use_container_width=True):
                
                with st.spinner("AI sedang menganalisis data..."):
                    import time
                    time.sleep(1)
                
                st.success("✅ Analisis AI Selesai!")
                
                # AI Recommendations based on current parameters
                recommendations = []
                optimizations = []
                potential_savings = 0
                
                # Analyze plant density
                if populasi_per_m2 < 55:
                    recommendations.append({
                        "area": "Kepadatan Tanam",
                        "issue": f"Kepadatan saat ini {populasi_per_m2:.0f}/m² terlalu rendah",
                        "action": "Kurangi jarak tanam menjadi 10×10cm untuk 100 tanaman/m²",
                        "impact": f"+{int((100-populasi_per_m2) * total_luas)} tanaman potensial"
                    })
                elif populasi_per_m2 > 80:
                    recommendations.append({
                        "area": "Kepadatan Tanam",
                        "issue": f"Kepadatan {populasi_per_m2:.0f}/m² terlalu tinggi",
                        "action": "Risiko penyakit tinggi, pertimbangkan 64/m²",
                        "impact": "Kualitas bunga lebih baik, harga jual lebih tinggi"
                    })
                
                # Analyze nozzle spacing
                if jarak_nozzle > 35:
                    recommendations.append({
                        "area": "Sistem Irigasi",
                        "issue": f"Jarak nozzle {jarak_nozzle}cm terlalu lebar",
                        "action": "Kurangi ke 25-30cm untuk penyiraman merata",
                        "impact": "Mengurangi dead spots, tanaman lebih seragam"
                    })
                
                # Analyze labor cost
                labor_pct = (biaya_tenaga_kerja / total_biaya) * 100 if total_biaya > 0 else 0
                if labor_pct > 40:
                    savings = biaya_tenaga_kerja * 0.2
                    potential_savings += savings
                    recommendations.append({
                        "area": "Tenaga Kerja",
                        "issue": f"Biaya TK {labor_pct:.0f}% dari total (terlalu tinggi)",
                        "action": "Otomatisasi irigasi & timer lampu untuk efisiensi",
                        "impact": f"Potensi hemat Rp {savings:,.0f}/siklus"
                    })
                
                # Analyze grade - 80 and 100 are optimal targets
                if grade_rab == 60:
                    optimizations.append({
                        "area": "Grade Target",
                        "current": f"Grade {grade_rab}",
                        "target": "Grade 80 atau 100",
                        "action": "Perpanjang durasi tanam, tingkatkan nutrisi untuk grade lebih tinggi",
                        "impact": "Grade 80/100 memberikan keseimbangan optimal yield & harga"
                    })
                elif grade_rab in [80, 100]:
                    optimizations.append({
                        "area": "Grade Target",
                        "current": f"Grade {grade_rab}",
                        "target": "✅ Sudah Optimal",
                        "action": "Pertahankan! Grade 80 dan 100 adalah target terbaik",
                        "impact": "Keseimbangan produktivitas, kualitas, dan harga pasar terbaik"
                    })
                elif grade_rab > 100:
                    recommendations.append({
                        "area": "Grade Target",
                        "issue": f"Grade {grade_rab} mungkin terlalu tinggi",
                        "action": "Grade 80-100 lebih efisien (durasi lebih pendek, rotasi lebih cepat)",
                        "impact": "Lebih banyak siklus per tahun = total pendapatan lebih tinggi"
                    })
                
                # Analyze survival rate
                if survival_rab < 88:
                    extra_plants = pop_for_rab * ((90 - survival_rab) / 100)
                    extra_revenue = (extra_plants / grade_rab) * harga_jual_rab
                    optimizations.append({
                        "area": "Survival Rate",
                        "current": f"{survival_rab}%",
                        "target": "90%+",
                        "action": "Tingkatkan sanitasi, IPM rutin, monitoring harian",
                        "impact": f"+{extra_plants:.0f} tanaman = +Rp {extra_revenue:,.0f}"
                    })
                
                # Display AI Results
                st.markdown("### 📋 Rekomendasi Perbaikan")
                
                if recommendations:
                    for rec in recommendations:
                        st.markdown(f"""
                        <div style="background: #fef3c7; padding: 1rem; border-radius: 8px; 
                                    border-left: 4px solid #f59e0b; margin: 0.5rem 0;">
                            <h4 style="margin: 0; color: #92400e;">⚠️ {rec['area']}</h4>
                            <p style="margin: 0.25rem 0;"><strong>Masalah:</strong> {rec['issue']}</p>
                            <p style="margin: 0.25rem 0;"><strong>Aksi:</strong> {rec['action']}</p>
                            <p style="color: #059669; margin: 0;"><strong>Dampak:</strong> {rec['impact']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                st.markdown("### 🚀 Optimasi Potensial")
                
                if optimizations:
                    for opt in optimizations:
                        st.markdown(f"""
                        <div style="background: #d1fae5; padding: 1rem; border-radius: 8px; 
                                    border-left: 4px solid #10b981; margin: 0.5rem 0;">
                            <h4 style="margin: 0; color: #065f46;">💡 {opt['area']}</h4>
                            <p style="margin: 0.25rem 0;">Saat ini: <strong>{opt['current']}</strong> → Target: <strong>{opt['target']}</strong></p>
                            <p style="margin: 0.25rem 0;"><strong>Aksi:</strong> {opt['action']}</p>
                            <p style="color: #059669; margin: 0;"><strong>Dampak:</strong> {opt['impact']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Summary
                st.divider()
                ai_col1, ai_col2 = st.columns(2)
                
                with ai_col1:
                    st.metric("Total Potensi Penghematan", f"Rp {potential_savings:,.0f}")
                
                with ai_col2:
                    new_laba = laba_bersih + potential_savings
                    new_roi = (new_laba / (total_biaya - potential_savings)) * 100
                    st.metric("Proyeksi ROI Setelah Optimasi", f"{new_roi:.1f}%", 
                             delta=f"+{new_roi - roi:.1f}%")

st.markdown("---")
st.caption("AgriSensa Sustainable Greenhouse - Membangun Pertanian yang Terukur dan Berkelanjutan.")

