import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Sistem Pertanian Terpadu - AgriSensa",
    page_icon="🌳",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






# Header
st.title(" Sistem Pertanian Terpadu")
st.markdown("**Integrated Farming Systems untuk Keberlanjutan dan Ketahanan**")

# Main tabs
tab_intro, tab_agroforestry, tab_livestock, tab_aquaponics, tab_circular = st.tabs([
    "📖 Pengenalan",
    "🌳 Agroforestri",
    "🐄 Integrasi Tanaman-Ternak",
    "🐟 Akuaponik",
    "♻️ Ekonomi Sirkular"
])

# ===== TAB 1: PENGENALAN =====
with tab_intro:
    st.header("📖 Pengenalan Sistem Pertanian Terpadu")
    
    st.markdown("""
    ### Apa itu Sistem Pertanian Terpadu?
    
    **Sistem Pertanian Terpadu (Integrated Farming System/IFS)** adalah pendekatan holistik yang **mengintegrasikan berbagai komponen pertanian** (tanaman, ternak, ikan, pohon) dalam satu sistem yang **saling mendukung dan berkelanjutan**.
    
    **Prinsip Dasar:**
    - 🔄 **Siklus Tertutup** (closed-loop): Limbah = Sumber daya
    - 🌿 **Diversifikasi**: Multiple income streams
    - ⚖️ **Sinergi**: 1 + 1 = 3 (output > input)
    - 🌍 **Keberlanjutan**: Jangka panjang, ramah lingkungan
    - 💪 **Ketahanan**: Resilient terhadap shock (harga, iklim, hama)
    
    ---
    
    ## 🎯 MENGAPA PERTANIAN TERPADU?
    
    ### **1. EKONOMI:**
    ```
    ✅ Diversifikasi pendapatan (5-10 sumber!)
    ✅ Risiko lebih rendah (jika 1 gagal, ada yang lain)
    ✅ Pendapatan lebih stabil (sepanjang tahun)
    ✅ Profit margin lebih tinggi (20-40% vs monokultur)
    ✅ Efisiensi biaya (reuse limbah = hemat input)
    ```
    
    **Data Ilmiah:**
    - **FAO (2014):** IFS meningkatkan pendapatan petani **30-50%** vs monokultur
    - **ICRAF (2019):** Agroforestri meningkatkan income **2-3x** dalam 5-10 tahun
    - **WorldFish (2018):** Integrated rice-fish meningkatkan profit **25-35%**
    
    ---
    
    ### **2. EKOLOGI:**
    ```
    ✅ Biodiversitas tinggi (habitat untuk berbagai spesies)
    ✅ Kesehatan tanah lebih baik (organic matter, mikroba)
    ✅ Siklus nutrisi efisien (N, P, K recycle)
    ✅ Emisi GHG lebih rendah (carbon sequestration)
    ✅ Resiliensi iklim (adaptasi & mitigasi)
    ```
    
    **Data Ilmiah:**
    - **Nature (2017):** Agroforestri menyerap **0.5-3 ton CO₂/ha/tahun**
    - **Science (2018):** Integrated farming meningkatkan biodiversitas **40-60%**
    - **IPCC (2019):** IFS mengurangi emisi GHG **20-30%** vs konvensional
    
    ---
    
    ### **3. SOSIAL:**
    ```
    ✅ Ketahanan pangan (diversified food sources)
    ✅ Nutrisi lebih baik (protein, vitamin dari berbagai sumber)
    ✅ Lapangan kerja (labor-intensive, year-round)
    ✅ Pengetahuan lokal (traditional wisdom + modern science)
    ✅ Community resilience (mutual support)
    ```
    
    ---
    
    ## 🌍 JENIS SISTEM PERTANIAN TERPADU
    
    ### **1. AGROFORESTRI (Agro + Forestry)**
    ```
    Integrasi: Pohon + Tanaman + (Ternak/Ikan)
    
    Contoh:
    - Kopi + Pohon pelindung (Lamtoro, Sengon)
    - Kakao + Kelapa + Pisang
    - Padi + Ikan + Bebek (Mina Padi)
    
    Keuntungan:
    - Diversifikasi pendapatan
    - Perbaiki iklim mikro (shade, humidity)
    - Carbon sequestration
    - Kayu untuk bahan bakar/bangunan
    ```
    
    ---
    
    ### **2. INTEGRASI TANAMAN-TERNAK (Crop-Livestock)**
    ```
    Integrasi: Tanaman ↔ Ternak
    
    Siklus:
    - Tanaman → Pakan ternak
    - Ternak → Pupuk kandang → Tanaman
    - Ternak → Tenaga kerja (bajak sawah)
    
    Contoh:
    - Padi + Sapi (jerami padi → pakan, kotoran → pupuk)
    - Jagung + Ayam (jagung afkir → pakan, kotoran → kompos)
    - Rumput + Kambing (cut & carry system)
    
    Keuntungan:
    - Hemat pupuk kimia (50-70%)
    - Hemat pakan (gunakan limbah tanaman)
    - Diversifikasi (tanaman + daging/susu/telur)
    ```
    
    ---
    
    ### **3. AKUAPONIK (Aquaculture + Hydroponics)**
    ```
    Integrasi: Ikan + Tanaman (hidroponik)
    
    Siklus:
    - Ikan → Kotoran (ammonia)
    - Bakteri → Konversi ammonia → nitrat
    - Nitrat → Nutrisi tanaman
    - Tanaman → Filter air → Ikan
    
    Contoh:
    - Lele + Kangkung
    - Nila + Selada
    - Gurame + Tomat
    
    Keuntungan:
    - Hemat air (90% vs konvensional)
    - Hemat nutrisi (dari ikan)
    - Dual income (ikan + sayuran)
    - Organic (no pesticide)
    ```
    
    ---
    
    ### **4. PERMACULTURE (Permanent Agriculture)**
    ```
    Prinsip: Design sistem yang meniru ekosistem alami
    → Self-sustaining, regenerative, resilient
    ```
    
    **Filosofi:**
    ```
    "Work WITH nature, not AGAINST nature"
    - Observe & interact
    - Catch & store energy
    - Obtain a yield
    - Self-regulation & feedback
    - Use renewable resources
    - Produce no waste
    - Design from patterns to details
    - Integrate rather than segregate
    - Use small & slow solutions
    - Value diversity
    - Use edges & value the marginal
    - Creatively use & respond to change
    ```
    
    **3 Etika Permakultur:**
    ```
    1. EARTH CARE (Peduli Bumi)
       - Tanah sehat = Tanaman sehat = Manusia sehat
       - Regenerasi, bukan degradasi
    
    2. PEOPLE CARE (Peduli Manusia)
       - Kebutuhan dasar: Makanan, air, shelter, energi
       - Kesehatan & kesejahteraan
    
    3. FAIR SHARE (Berbagi Adil)
       - Surplus untuk komunitas
       - Limits to consumption
       - Redistribusi kelebihan
    ```
    
    ---
    
    ### **ZONA PERMAKULTUR:**
    
    **Zona 0: RUMAH (Center)**
    ```
    - Pusat aktivitas
    - Energy hub (solar panel, biogas)
    - Water storage (tangki air hujan)
    - Composting toilet
    
    Prinsip: Maximum efficiency
    ```
    
    **Zona 1: INTENSIF (Daily Visit)**
    ```
    Jarak: 0-10 m dari rumah
    
    Tanaman:
    - Sayuran harian (selada, bayam, kangkung)
    - Herbs (basil, mint, cilantro)
    - Salad greens
    
    Ternak:
    - Ayam (5-10 ekor) - telur harian
    
    Infrastruktur:
    - Raised beds
    - Vertical garden
    - Compost bin
    - Worm farm
    
    Maintenance: Harian (panen, siram, panen telur)
    ```
    
    **Zona 2: SEMI-INTENSIF (Weekly Visit)**
    ```
    Jarak: 10-50 m
    
    Tanaman:
    - Buah-buahan (pisang, pepaya, mangga)
    - Tanaman tahunan (singkong, ubi)
    - Perennial vegetables (katuk, kelor)
    
    Ternak:
    - Kambing/domba (5-10 ekor)
    - Bebek (kolam kecil)
    
    Infrastruktur:
    - Mulch garden
    - Swales (water harvesting)
    - Small pond
    
    Maintenance: Mingguan (panen, pruning)
    ```
    
    **Zona 3: PRODUKSI UTAMA (Monthly Visit)**
    ```
    Jarak: 50-200 m
    
    Tanaman:
    - Padi/jagung (staple crops)
    - Orchard (durian, rambutan, alpukat)
    - Timber trees (jati, mahoni)
    
    Ternak:
    - Sapi (2-5 ekor)
    - Silvopasture
    
    Maintenance: Bulanan (seasonal work)
    ```
    
    **Zona 4: HUTAN PRODUKSI (Seasonal Visit)**
    ```
    Jarak: 200-500 m
    
    Tanaman:
    - Timber (kayu bangunan)
    - HHBK (madu, rotan, gaharu)
    - Medicinal plants
    
    Ternak:
    - Free-range (ayam kampung)
    
    Maintenance: Seasonal (panen, thinning)
    ```
    
    **Zona 5: WILDERNESS (No Intervention)**
    ```
    Jarak: >500 m
    
    Fungsi:
    - Konservasi
    - Biodiversitas
    - Seed bank (genetic diversity)
    - Spiritual/recreational
    
    Maintenance: None (let nature do its work)
    ```
    
    ---
    
    ### **GUILD DESIGN (Companion Planting):**
    
    **Konsep:**
    ```
    Guild = Kelompok tanaman yang saling mendukung
    → Meniru ekosistem hutan
    ```
    
    **Contoh: FRUIT TREE GUILD**
    ```
    Center: Pohon buah (mangga, alpukat)
    
    Layer 1 - Nitrogen Fixer:
    - Lamtoro, gamal (N-fixation)
    - Jarak: 2-3 m dari center
    
    Layer 2 - Dynamic Accumulator:
    - Comfrey, katuk (deep roots, nutrient pump)
    - Jarak: 1-2 m
    
    Layer 3 - Ground Cover:
    - Sweet potato, kacang tanah
    - Suppress weeds, living mulch
    
    Layer 4 - Pest Repellent:
    - Marigold, basil, lemongrass
    - Attract beneficial insects
    
    Layer 5 - Pollinator Attractor:
    - Bunga matahari, cosmos
    - Attract bees, butterflies
    
    Hasil:
    ✅ No fertilizer (N-fixation + nutrient cycling)
    ✅ No herbicide (ground cover suppress weeds)
    ✅ No pesticide (companion plants repel pests)
    ✅ High biodiversity (habitat for beneficial insects)
    ```
    
    ---
    
    ### **WATER MANAGEMENT:**
    
    **A. SWALES (Parit Kontur):**
    ```
    Prinsip:
    - Parit mengikuti kontur (level)
    - Tangkap air hujan → Infiltrasi → Groundwater recharge
    
    Desain:
    - Lebar: 0.5-1 m
    - Kedalaman: 0.3-0.5 m
    - Jarak: 10-30 m (tergantung kemiringan)
    - Tanaman: Pohon di berm (gundukan)
    
    Keuntungan:
    ✅ Cegah erosi
    ✅ Recharge groundwater
    ✅ Microclimate (humidity ↑)
    ✅ Passive irrigation
    
    Referensi:
    - Yeomans, P. A. (1954). The Keyline Plan.
    ```
    
    **B. PONDS (Kolam):**
    ```
    Fungsi:
    - Water storage (irigasi)
    - Aquaculture (ikan, bebek)
    - Microclimate (cooling)
    - Wildlife habitat
    - Fire protection
    
    Desain:
    - Lokasi: Titik terendah (gravity-fed)
    - Ukuran: 100-500 m² (tergantung kebutuhan)
    - Kedalaman: 1.5-2 m (avoid mosquito)
    - Edge: Gradual slope (wildlife access)
    
    Tanaman:
    - Eceng gondok (biofilter)
    - Kangkung air (pakan)
    - Lotus (estetika)
    ```
    
    **C. RAIN WATER HARVESTING:**
    ```
    - Atap rumah → Talang → Tangki (5,000-10,000 L)
    - Potensi: 1 mm hujan × 100 m² atap = 100 L
    - Jakarta (2,000 mm/tahun): 200,000 L/tahun!
    ```
    
    ---
    
    ### **IMPLEMENTASI PERMAKULTUR:**
    
    **Tahap 1: OBSERVASI (1-12 bulan)**
    ```
    - Pola matahari (sun path)
    - Pola angin (wind direction)
    - Aliran air (water flow)
    - Tanah (soil type, pH)
    - Existing vegetation
    - Wildlife
    
    Tools:
    - Kompas (orientasi)
    - Clinometer (kemiringan)
    - Soil test kit
    - Notebook (catat pola)
    ```
    
    **Tahap 2: DESIGN (1-3 bulan)**
    ```
    - Buat peta (scale 1:100 atau 1:500)
    - Tentukan zona (0-5)
    - Design water management (swales, ponds)
    - Pilih tanaman (guild design)
    - Plan infrastructure (paths, fences)
    
    Tools:
    - Graph paper
    - Pencil & eraser
    - Ruler & compass
    ```
    
    **Tahap 3: IMPLEMENTASI (Bertahap)**
    ```
    Tahun 1:
    - Zona 0-1 (rumah, sayuran intensif)
    - Water harvesting (tangki, swales)
    - Compost system
    
    Tahun 2:
    - Zona 2 (buah, ternak kecil)
    - Pond
    - Perennial vegetables
    
    Tahun 3-5:
    - Zona 3-4 (orchard, hutan produksi)
    - Timber trees
    - Silvopasture
    
    Prinsip: Small & slow solutions!
    ```
    
    ---
    
    ### **EKONOMI PERMAKULTUR:**
    
    **Kasus: Permaculture Farm 1 Ha**
    ```
    INVESTASI (Tahun 0-2): Rp 50-100 juta
    - Infrastruktur (swales, ponds, fences)
    - Bibit (pohon, sayuran, ternak)
    - Tools
    
    PENDAPATAN (Tahun 5+):
    - Zona 1 (sayuran): Rp 20-30 juta/tahun
    - Zona 2 (buah, telur): Rp 30-50 juta/tahun
    - Zona 3 (padi, daging): Rp 40-60 juta/tahun
    - Zona 4 (kayu, HHBK): Rp 10-20 juta/tahun
    
    TOTAL: Rp 100-160 juta/tahun
    
    HEMAT:
    - Pupuk: 80-90% (recycle)
    - Pestisida: 90-100% (biodiversity)
    - Air: 50-70% (water harvesting)
    - Energi: 50-80% (biogas, solar)
    
    ROI: 3-5 tahun
    
    Bonus:
    ✅ Food security (diversified)
    ✅ Resilience (climate, market)
    ✅ Quality of life (beautiful, peaceful)
    ✅ Legacy (regenerative, sustainable)
    ```
    
    **Keuntungan:**
    ```
    ✅ Efisiensi energi (minimize input)
    ✅ Resiliensi tinggi (diverse, redundant)
    ✅ Estetika (beautiful, livable)
    ✅ Keberlanjutan (regenerative)
    ✅ Low maintenance (self-regulating)
    ```
    
    **Referensi:**
    - **Mollison, B., & Holmgren, D. (1978).** Permaculture One. Tagari Publications.
    - **Holmgren, D. (2002).** Permaculture: Principles and Pathways Beyond Sustainability.
    - **Whitefield, P. (2004).** The Earth Care Manual. Permanent Publications.
    
    ---
    
    ### **5. EKONOMI SIRKULAR (Circular Economy)**
    ```
    Prinsip: Zero waste, everything is resource
    
    Contoh:
    - Limbah tanaman → Kompos/Pakan → Tanaman/Ternak
    - Kotoran ternak → Biogas → Energi + Pupuk
    - Air limbah → Biofilter (tanaman air) → Irigasi
    - Limbah organik → BSF (Black Soldier Fly) → Pakan
    
    Keuntungan:
    - Minimize waste (90-100% recycle)
    - Hemat biaya input (50-70%)
    - Additional income (biogas, kompos, BSF)
    - Ramah lingkungan (no pollution)
    ```
    
    ---
    
    ## 📊 PERBANDINGAN MONOKULTUR VS TERPADU
    
    | Aspek | Monokultur | Pertanian Terpadu |
    |-------|------------|-------------------|
    | **Pendapatan** | 1 sumber | 5-10 sumber |
    | **Risiko** | Tinggi (all eggs in one basket) | Rendah (diversified) |
    | **Stabilitas** | Fluktuatif (musiman) | Stabil (year-round) |
    | **Input Eksternal** | Tinggi (pupuk, pestisida) | Rendah (recycle) |
    | **Biodiversitas** | Rendah (1-2 spesies) | Tinggi (10-50 spesies) |
    | **Kesehatan Tanah** | Menurun (degradasi) | Meningkat (organic matter) |
    | **Emisi GHG** | Tinggi | Rendah (carbon sink) |
    | **Ketahanan Iklim** | Rentan | Resilient |
    | **Profit Margin** | 10-20% | 30-50% |
    
    ---
    
    ## 💡 TIPS MEMULAI PERTANIAN TERPADU
    
    **1. Mulai Kecil:**
    ```
    - Jangan langsung kompleks (overwhelmed!)
    - Mulai dengan 2-3 komponen
    - Contoh: Sayuran + Ayam + Kompos
    - Expand bertahap (1-2 komponen/tahun)
    ```
    
    **2. Pilih Komponen yang Saling Mendukung:**
    ```
    - Tanaman → Pakan ternak
    - Ternak → Pupuk tanaman
    - Limbah → Sumber daya
    ```
    
    **3. Perhatikan Skala:**
    ```
    - Lahan <1000 m²: Sayuran + Ayam + Ikan
    - Lahan 1000-5000 m²: + Kambing + Buah
    - Lahan >5000 m²: + Sapi + Agroforestri
    ```
    
    **4. Belajar dari Petani Sukses:**
    ```
    - Kunjungi farm terpadu
    - Join komunitas (online/offline)
    - Ikuti pelatihan
    ```
    
    **5. Monitor & Evaluasi:**
    ```
    - Catat input-output (ekonomi)
    - Amati kesehatan tanah, tanaman, ternak
    - Adjust sistem (continuous improvement)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **FAO. (2014).** Building a common vision for sustainable food and agriculture. FAO, Rome.
    
    2. **ICRAF. (2019).** Agroforestry for landscape restoration. World Agroforestry Centre.
    
    3. **Pretty, J., et al. (2018).** Global assessment of agricultural system redesign for sustainable intensification. Nature Sustainability, 1, 441-446.
    
    4. **IPCC. (2019).** Climate Change and Land. Special Report.
    
    5. **Altieri, M. A. (1999).** The ecological role of biodiversity in agroecosystems. Agriculture, Ecosystems & Environment, 74, 19-31.
    
    """)

# ===== TAB 2: AGROFORESTRI =====
with tab_agroforestry:
    st.header("🌳 Sistem Agroforestri")
    
    st.markdown("""
    ### Apa itu Agroforestri?
    
    **Agroforestri** adalah sistem penggunaan lahan yang **mengintegrasikan pohon dengan tanaman pertanian dan/atau ternak** dalam satu lahan untuk meningkatkan produktivitas, keberlanjutan, dan ketahanan.
    
    **Komponen:**
    - 🌳 **Pohon:** Kayu, buah, HHBK (Hasil Hutan Bukan Kayu)
    - 🌾 **Tanaman:** Pangan, hortikultura, perkebunan
    - 🐄 **Ternak:** (opsional) Sapi, kambing, ayam
    
    ---
    
    ## 🌳 JENIS AGROFORESTRI
    
    ### **1. AGRISILVICULTURE (Tanaman + Pohon)**
    
    **A. Alley Cropping (Lorong):**
    ```
    Desain:
    - Barisan pohon (spacing 5-10 m)
    - Tanaman di lorong (lebar 5-10 m)
    
    Contoh:
    - Lamtoro (N-fixing) + Jagung
    - Sengon + Padi gogo
    - Gliricidia + Sayuran
    
    Keuntungan:
    ✅ Pohon → Mulch, N-fixation
    ✅ Tanaman → Income jangka pendek
    ✅ Kayu → Income jangka panjang (5-10 tahun)
    ```
    
    **B. Taungya (Tumpangsari Kehutanan):**
    ```
    Desain:
    - Tanam pohon + tanaman semusim (tahun 1-3)
    - Setelah pohon besar → Tanaman dihentikan
    
    Contoh:
    - Jati + Jagung (tahun 1-2)
    - Mahoni + Kedelai (tahun 1-3)
    
    Keuntungan:
    ✅ Petani dapat income sambil pohon tumbuh
    ✅ Maintenance pohon (penyiangan) gratis
    ```
    
    **C. Multistrata (Berlapis):**
    ```
    Desain:
    - Strata 1 (0-2 m): Sayuran, rempah
    - Strata 2 (2-5 m): Pisang, pepaya
    - Strata 3 (5-15 m): Kopi, kakao
    - Strata 4 (>15 m): Kelapa, durian, petai
    
    Contoh:
    - Kopi + Pisang + Lamtoro + Durian
    - Kakao + Kelapa + Cengkeh
    
    Keuntungan:
    ✅ Diversifikasi maksimal (5-10 komoditas)
    ✅ Iklim mikro optimal (shade, humidity)
    ✅ Biodiversitas tinggi
    ✅ Carbon sequestration tinggi (1-3 ton CO₂/ha/tahun)
    ```
    
    ---
    
    ### **2. SILVOPASTURE (Pohon + Ternak)**
    
    **Prinsip:**
    ```
    Pohon → Shade untuk ternak + Pakan (daun)
    Ternak → Pupuk untuk pohon
    Rumput → Pakan ternak
    ```
    
    **Desain:**
    ```
    - Pohon: Spacing 10-20 m (shade 30-50%)
    - Rumput: Brachiaria, Setaria, Panicum
    - Ternak: Sapi, kambing, domba
    - Stocking rate: 1-3 ekor/ha
    
    Contoh:
    - Kelapa + Rumput + Sapi
    - Lamtoro + Rumput + Kambing
    - Kaliandra + Rumput + Domba
    ```
    
    **Keuntungan:**
    ```
    ✅ Ternak lebih sehat (shade, stress ↓)
    ✅ Produksi susu/daging ↑ 10-20%
    ✅ Pohon tumbuh lebih cepat (pupuk dari ternak)
    ✅ Kayu + Daging/Susu (dual income)
    ```
    
    **Data Ilmiah:**
    - **ICRAF (2018):** Silvopasture meningkatkan produksi daging **15-25%** vs pasture biasa
    - **Agroforestry Systems (2019):** Shade mengurangi heat stress ternak, meningkatkan feed intake **10-15%**
    
    ---
    
    ### **3. AGROSILVOPASTURE (Tanaman + Pohon + Ternak)**
    
    **Prinsip:**
    ```
    Integrasi penuh: Tanaman + Pohon + Ternak
    → Sinergi maksimal!
    ```
    
    **Contoh:**
    ```
    - Kelapa + Kakao + Sapi
    - Karet + Nanas + Kambing
    - Jati + Jagung + Ayam kampung
    ```
    
    **Siklus:**
    ```
    1. Pohon → Shade, mulch, kayu
    2. Tanaman → Pakan ternak (jerami, daun)
    3. Ternak → Pupuk untuk pohon & tanaman
    4. Ternak → Tenaga kerja (bajak)
    5. Semua → Diversifikasi income
    ```
    
    ---
    
    ## 📊 DESAIN AGROFORESTRI KOPI
    
    ### **Kopi + Pohon Pelindung (Shade Coffee)**
    
    **Mengapa Perlu Shade?**
    ```
    - Kopi arabika optimal: 50-70% shade
    - Kopi robusta optimal: 30-50% shade
    
    Manfaat shade:
    ✅ Suhu lebih stabil (tidak ekstrem)
    ✅ Kelembaban lebih tinggi
    ✅ Kualitas biji lebih baik (slow maturation)
    ✅ Harga lebih tinggi (specialty coffee)
    ✅ Biodiversitas tinggi (bird-friendly)
    ```
    
    **Pohon Pelindung:**
    
    **A. Legume Trees (N-fixing):**
    ```
    - Lamtoro (Leucaena leucocephala)
    - Gamal (Gliricidia sepium)
    - Dadap (Erythrina spp.)
    
    Keuntungan:
    ✅ Fiksasi N: 50-200 kg N/ha/tahun
    ✅ Hemat pupuk urea 50-70%
    ✅ Mulch (daun gugur)
    
    Spacing: 6-10 m
    Populasi: 100-250 pohon/ha
    ```
    
    **B. Fruit Trees:**
    ```
    - Durian, Alpukat, Rambutan
    - Pisang, Pepaya
    
    Keuntungan:
    ✅ Dual income (kopi + buah)
    ✅ Diversifikasi
    
    Spacing: 10-15 m
    Populasi: 50-100 pohon/ha
    ```
    
    **C. Timber Trees:**
    ```
    - Sengon, Jabon, Mahoni
    - Jati, Merbau
    
    Keuntungan:
    ✅ Kayu untuk jangka panjang (10-20 tahun)
    ✅ Tabungan (savings)
    
    Spacing: 10-20 m
    Populasi: 25-100 pohon/ha
    ```
    
    **Desain Contoh (1 Ha):**
    ```
    - Kopi: 1,600 pohon (spacing 2.5 × 2.5 m)
    - Lamtoro: 150 pohon (shade 50%)
    - Durian: 25 pohon
    - Pisang: 100 pohon (fill gaps)
    
    TOTAL: 1,875 pohon/ha
    
    Income (tahun ke-5):
    - Kopi: 1.5 ton × Rp 30K = Rp 45 juta
    - Pisang: 1,000 tandan × Rp 15K = Rp 15 juta
    - Durian: 500 kg × Rp 25K = Rp 12.5 juta
    
    TOTAL: Rp 72.5 juta/tahun
    vs Kopi monokultur: Rp 40-50 juta/tahun
    
    Increase: 45-80%!
    ```
    
    ---
    
    ## 💰 ANALISIS EKONOMI AGROFORESTRI
    
    ### **Kasus: Kakao + Kelapa + Pisang (1 Ha)**
    
    **INVESTASI (Tahun 0):**
    ```
    - Bibit kakao (1,000 @ Rp 5K): Rp 5 juta
    - Bibit kelapa (100 @ Rp 25K): Rp 2.5 juta
    - Bibit pisang (200 @ Rp 10K): Rp 2 juta
    - Pupuk & pestisida: Rp 3 juta
    - Tenaga kerja: Rp 5 juta
    
    TOTAL: Rp 17.5 juta
    ```
    
    **PENDAPATAN (per tahun):**
    
    | Tahun | Pisang | Kakao | Kelapa | TOTAL | Kumulatif |
    |-------|--------|-------|--------|-------|-----------|
    | 1 | Rp 10M | - | - | Rp 10M | Rp 10M |
    | 2 | Rp 15M | - | - | Rp 15M | Rp 25M |
    | 3 | Rp 15M | Rp 10M | - | Rp 25M | Rp 50M |
    | 4 | Rp 15M | Rp 20M | - | Rp 35M | Rp 85M |
    | 5 | Rp 15M | Rp 30M | Rp 15M | Rp 60M | Rp 145M |
    | 6+ | Rp 15M | Rp 40M | Rp 20M | Rp 75M | - |
    
    **ROI:** Tahun ke-2 (break-even)
    **Profit (tahun 6+):** Rp 75M/tahun
    
    vs **Kakao monokultur:** Rp 40-50M/tahun
    **Increase:** 50-90%!
    
    ---
    
    ## 📚 REFERENSI
    
    1. **ICRAF. (2019).** Agroforestry for landscape restoration. World Agroforestry Centre.
    
    2. **Nair, P. K. R. (1993).** An Introduction to Agroforestry. Kluwer Academic Publishers.
    
    3. **Jose, S., et al. (2019).** Agroforestry for sustainable agriculture. Burleigh Dodds Science Publishing.
    
    4. **Somarriba, E., et al. (2004).** Biodiversity conservation in neotropical coffee (Coffea arabica) plantations. Agroforestry Systems, 61, 189-198.
    
    """)

# ===== TAB 3: INTEGRASI TANAMAN-TERNAK =====
with tab_livestock:
    st.header("🐄 Integrasi Tanaman-Ternak")
    
    st.markdown("""
    ### Mengapa Integrasi Tanaman-Ternak?
    
    **Sinergi:**
    - 🌾 **Tanaman** → Pakan ternak (jerami, daun, limbah)
    - 🐄 **Ternak** → Pupuk kandang → Tanaman
    - 🐄 **Ternak** → Tenaga kerja (bajak sawah)
    - 💰 **Diversifikasi** → Tanaman + Daging/Susu/Telur
    
    **Keuntungan:**
    ```
    ✅ Hemat pupuk kimia: 50-70%
    ✅ Hemat pakan: 30-50% (gunakan limbah tanaman)
    ✅ Pendapatan lebih stabil (diversified)
    ✅ Kesehatan tanah lebih baik (organic matter)
    ✅ Emisi GHG lebih rendah (manure management)
    ```
    
    ---
    
    ## 🌾 SISTEM INTEGRASI
    
    ### **1. PADI + SAPI**
    
    **Siklus:**
    ```
    1. Padi → Jerami (5-7 ton/ha)
    2. Jerami → Pakan sapi (fermentasi/amoniasi)
    3. Sapi → Kotoran (10-15 ton/tahun/ekor)
    4. Kotoran → Kompos → Pupuk padi
    5. Sapi → Bajak sawah (tenaga kerja)
    ```
    
    **Desain (1 Ha Padi + 2 Ekor Sapi):**
    ```
    PADI:
    - Luas: 1 ha
    - Hasil: 6 ton GKP/ha
    - Jerami: 6 ton/ha
    
    SAPI:
    - Populasi: 2 ekor
    - Pakan: Jerami (fermentasi) + Rumput
    - Kotoran: 20-30 ton/tahun
    - Kompos: 10-15 ton/tahun (setelah composting)
    
    PUPUK:
    - Kompos: 10 ton/ha (cukup untuk 1 ha!)
    - Hemat urea: 50-70% (N dari kompos)
    - Hemat NPK: 30-50%
    ```
    
    **EKONOMI:**
    ```
    PENDAPATAN:
    - Padi: 6 ton × Rp 5,000 = Rp 30 juta
    - Sapi (pertambahan bobot): 2 ekor × 150 kg × Rp 50K = Rp 15 juta
    
    TOTAL: Rp 45 juta/tahun
    
    vs Padi monokultur: Rp 30 juta/tahun
    Increase: 50%!
    
    HEMAT BIAYA:
    - Pupuk: Rp 3-5 juta/tahun
    - Bajak: Rp 2-3 juta/tahun
    
    TOTAL HEMAT: Rp 5-8 juta/tahun
    ```
    
    ---
    
    ### **2. JAGUNG + AYAM**
    
    **Siklus:**
    ```
    1. Jagung → Biji afkir + Tongkol → Pakan ayam
    2. Ayam → Kotoran → Kompos → Pupuk jagung
    3. Ayam → Telur/Daging
    ```
    
    **Desain (1 Ha Jagung + 500 Ekor Ayam Layer):**
    ```
    JAGUNG:
    - Luas: 1 ha
    - Hasil: 8 ton pipilan kering
    - Afkir (10%): 800 kg → Pakan ayam
    - Tongkol: 2 ton → Pakan ayam (fermentasi)
    
    AYAM LAYER:
    - Populasi: 500 ekor
    - Produksi telur: 80% × 500 × 365 = 146,000 butir/tahun
    - Pakan: Jagung afkir + Konsentrat
    - Kotoran: 15-20 ton/tahun
    
    KOMPOS:
    - Kotoran ayam: 15 ton/tahun
    - Cukup untuk 1 ha jagung!
    ```
    
    **EKONOMI:**
    ```
    PENDAPATAN:
    - Jagung: 7.2 ton (90%) × Rp 4,000 = Rp 28.8 juta
    - Telur: 146,000 × Rp 1,500 = Rp 219 juta
    
    TOTAL: Rp 247.8 juta/tahun
    
    BIAYA OPERASIONAL:
    - Pakan ayam (konsentrat): Rp 150 juta
    - Pupuk jagung: Rp 5 juta (hemat 50%)
    - Lain-lain: Rp 20 juta
    
    TOTAL BIAYA: Rp 175 juta
    
    PROFIT: Rp 72.8 juta/tahun
    
    vs Jagung monokultur: Rp 15-20 juta/tahun
    Increase: 300-400%!
    ```
    
    ---
    
    ### **3. RUMPUT + KAMBING (Cut & Carry)**
    
    **Prinsip:**
    ```
    - Rumput ditanam intensif (Napier, Setaria)
    - Dipotong (cut) → Dibawa (carry) ke kandang
    - Kambing dikandangkan (zero grazing)
    - Kotoran dikumpulkan → Kompos
    ```
    
    **Desain (1 Ha Rumput + 20 Ekor Kambing):**
    ```
    RUMPUT:
    - Jenis: Napier grass (Pennisetum purpureum)
    - Produksi: 200-300 ton segar/ha/tahun
    - Panen: Setiap 45-60 hari
    - Kebutuhan: 20 ekor × 10 kg/hari × 365 = 73 ton/tahun
    - Surplus: 127-227 ton (dijual atau untuk ternak lain)
    
    KAMBING:
    - Populasi: 20 ekor induk
    - Anak: 20 × 2 × 1.5 = 60 ekor/tahun
    - Dijual (umur 6-8 bulan): 60 × 25 kg × Rp 50K = Rp 75 juta
    - Kotoran: 10-15 ton/tahun
    ```
    
    **EKONOMI:**
    ```
    PENDAPATAN:
    - Kambing: Rp 75 juta/tahun
    - Rumput surplus (dijual): Rp 10-15 juta
    
    TOTAL: Rp 85-90 juta/tahun
    
    BIAYA:
    - Konsentrat: Rp 20 juta
    - Obat-obatan: Rp 5 juta
    - Tenaga kerja: Rp 15 juta
    
    TOTAL BIAYA: Rp 40 juta
    
    PROFIT: Rp 45-50 juta/tahun
    
    ROI: 1-2 tahun
    ```
    
    ---
    
    ## 💩 MANAJEMEN PUPUK KANDANG
    
    ### **Komposisi Pupuk Kandang:**
    
    | Ternak | N (%) | P₂O₅ (%) | K₂O (%) | C/N Ratio |
    |--------|-------|----------|---------|-----------|
    | **Sapi** | 0.5-0.7 | 0.3-0.5 | 0.5-0.7 | 15-25 |
    | **Kambing** | 0.8-1.2 | 0.5-0.8 | 0.8-1.2 | 12-20 |
    | **Ayam** | 1.5-2.5 | 1.5-2.0 | 0.8-1.2 | 8-15 |
    | **Babi** | 0.6-0.8 | 0.5-0.7 | 0.4-0.6 | 15-20 |
    
    ### **Cara Membuat Kompos:**
    
    **Bahan:**
    ```
    - Kotoran ternak: 1,000 kg
    - Jerami/sekam: 200 kg (C/N ratio 50-80)
    - EM4/Decomposer: 1 L
    - Air: Secukupnya (kelembaban 50-60%)
    ```
    
    **Proses:**
    ```
    1. Campur kotoran + jerami
    2. Siram dengan EM4 (dilarutkan)
    3. Tumpuk (tinggi 1-1.5 m)
    4. Tutup dengan terpal
    5. Balik setiap 7 hari
    6. Matang: 21-30 hari (warna hitam, tidak bau)
    
    Hasil: 600-700 kg kompos matang
    (susut 30-40%)
    ```
    
    **Dosis Aplikasi:**
    ```
    - Padi: 5-10 ton/ha
    - Jagung: 5-10 ton/ha
    - Sayuran: 10-20 ton/ha
    - Buah: 20-40 kg/pohon
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Devendra, C., & Thomas, D. (2002).** Crop-animal interactions in mixed farming systems in Asia. Agricultural Systems, 71, 27-40.
    
    2. **Herrero, M., et al. (2010).** Smart investments in sustainable food production. Science, 327, 822-825.
    
    3. **FAO. (2001).** Mixed crop-livestock farming: A review of traditional technologies. FAO Animal Production and Health Papers.
    
    """)

# ===== TAB 4: AKUAPONIK =====
with tab_aquaponics:
    st.header("🐟 Sistem Akuaponik")
    
    st.markdown("""
    ### Apa itu Akuaponik?
    
    **Akuaponik** = **Aquaculture** (budidaya ikan) + **Hydroponics** (tanaman tanpa tanah)
    
    **Prinsip:**
    ```
    1. Ikan → Kotoran (ammonia - NH₃)
    2. Bakteri nitrifikasi → Konversi NH₃ → Nitrit (NO₂⁻) → Nitrat (NO₃⁻)
    3. Nitrat → Nutrisi tanaman
    4. Tanaman → Serap nitrat → Filter air
    5. Air bersih → Kembali ke ikan
    
    CLOSED LOOP: Zero waste water!
    ```
    
    **Keuntungan:**
    ```
    ✅ Hemat air: 90% vs konvensional
    ✅ Hemat nutrisi: Dari ikan (no AB mix)
    ✅ Dual income: Ikan + Sayuran
    ✅ Organic: No pesticide, no chemical fertilizer
    ✅ Efisien lahan: Vertikal farming
    ✅ Pertumbuhan cepat: 30-50% lebih cepat vs tanah
    ```
    
    ---
    
    ## 🐟 KOMPONEN AKUAPONIK
    
    ### **1. FISH TANK (Kolam Ikan)**
    ```
    - Volume: 500-2,000 L
    - Bentuk: Bulat/persegi (avoid dead zones)
    - Material: Fiber, terpal, beton
    - Aerasi: Air pump + air stone (DO >5 mg/L)
    - Kedalaman: 60-100 cm
    ```
    
    ### **2. BIOFILTER**
    ```
    Fungsi: Konversi ammonia → nitrat
    
    Media:
    - Bio ball, K1 media, lava rock
    - Luas permukaan tinggi (untuk bakteri)
    
    Volume: 10-20% dari fish tank
    
    Bakteri:
    - Nitrosomonas: NH₃ → NO₂⁻
    - Nitrobacter: NO₂⁻ → NO₃⁻
    
    Cycling time: 3-6 minggu (establish bacteria)
    ```
    
    ### **3. GROW BED (Media Tanaman)**
    ```
    Jenis:
    
    A. Media Bed:
    - Media: Hydroton, kerikil, lava rock
    - Kedalaman: 20-30 cm
    - Flood & drain (bell siphon)
    
    B. NFT (Nutrient Film Technique):
    - Pipa PVC 3-4 inch
    - Aliran tipis (1-2 mm)
    
    C. DWC (Deep Water Culture):
    - Rakit styrofoam
    - Akar terendam (aerasi kuat)
    
    Volume: 1:1 dengan fish tank
    ```
    
    ### **4. POMPA & PIPA**
    ```
    - Pompa submersible: 30-100 watt
    - Flow rate: 1-2x volume tank/jam
    - Pipa: PVC 1-2 inch
    - Filter mekanik: Sebelum biofilter (buang kotoran padat)
    ```
    
    ---
    
    ## 🐟 RASIO IKAN : TANAMAN
    
    ### **Feeding Rate Method:**
    ```
    Formula:
    Luas grow bed (m²) = Pakan ikan (gram/hari) / 50-100
    
    Contoh:
    - Ikan: 100 ekor lele (100 gram/ekor)
    - Pakan: 3% bobot = 300 gram/hari
    - Grow bed: 300 / 60 = 5 m²
    
    Tanaman: 5 m² × 25 lubang/m² = 125 tanaman
    ```
    
    ### **Stocking Density:**
    ```
    - Lele: 50-100 ekor/m³ (high density)
    - Nila: 20-40 ekor/m³ (medium)
    - Gurame: 10-20 ekor/m³ (low)
    - Mas: 20-30 ekor/m³ (medium)
    
    Catatan: Perlu aerasi kuat untuk high density!
    ```
    
    ---
    
    ## 🐟 JENIS IKAN & TANAMAN
    
    ### **IKAN:**
    
    **A. Lele (Catfish):**
    ```
    ✅ Toleran kualitas air rendah
    ✅ Pertumbuhan cepat (3-4 bulan → 100 gram)
    ✅ Harga bagus (Rp 20-25K/kg)
    ✅ Pakan murah (pelet)
    
    ❌ Produksi ammonia tinggi (perlu biofilter kuat)
    ```
    
    **B. Nila (Tilapia):**
    ```
    ✅ Paling populer untuk akuaponik
    ✅ Toleran suhu luas (20-35°C)
    ✅ Omnivora (makan apa saja)
    ✅ Pertumbuhan cepat (4-6 bulan → 200-300 gram)
    
    ❌ Reproduksi cepat (overpopulation)
    ```
    
    **C. Gurame:**
    ```
    ✅ Harga tinggi (Rp 40-60K/kg)
    ✅ Rasa enak
    
    ❌ Pertumbuhan lambat (8-12 bulan → 500 gram)
    ❌ Sensitif kualitas air
    ```
    
    ### **TANAMAN:**
    
    **A. Leafy Greens (Daun):**
    ```
    ✅ Selada, kangkung, sawi, bayam
    ✅ Pertumbuhan cepat (25-35 hari)
    ✅ Nutrisi requirement rendah
    ✅ Cocok untuk pemula
    ```
    
    **B. Herbs (Rempah):**
    ```
    ✅ Basil, mint, cilantro
    ✅ Harga tinggi (Rp 30-50K/kg)
    ✅ Aroma kuat (premium market)
    ```
    
    **C. Fruiting Plants (Buah):**
    ```
    ✅ Tomat, cabai, terong, timun
    ✅ Harga tinggi
    
    ❌ Nutrisi requirement tinggi (perlu supplement K, Ca)
    ❌ Pertumbuhan lebih lama (60-90 hari)
    ```
    
    ---
    
    ## 💰 ANALISIS EKONOMI AKUAPONIK
    
    ### **Kasus: Lele + Kangkung (Skala Rumahan)**
    
    **INVESTASI:**
    ```
    - Fish tank (1000 L): Rp 1.5 juta
    - Biofilter: Rp 500K
    - Grow bed NFT (100 lubang): Rp 2 juta
    - Pompa + aerator: Rp 1 juta
    - Pipa & fitting: Rp 500K
    
    TOTAL: Rp 5.5 juta
    ```
    
    **OPERASIONAL (per siklus 3 bulan):**
    ```
    IKAN (100 ekor lele):
    - Benih: 100 × Rp 500 = Rp 50K
    - Pakan: 90 hari × 300 gram × Rp 8K/kg = Rp 216K
    - Listrik: 90 hari × 100 watt × 10 jam × Rp 1.5K/kWh = Rp 135K
    
    TANAMAN (100 kangkung, 3 siklus):
    - Benih: 3 × 100 × Rp 100 = Rp 30K
    
    TOTAL BIAYA: Rp 431K/3 bulan
    ```
    
    **PENDAPATAN (per 3 bulan):**
    ```
    IKAN:
    - Lele: 100 ekor × 100 gram × Rp 25K/kg = Rp 250K
    
    TANAMAN (3 siklus @ 30 hari):
    - Kangkung: 3 × 100 × 200 gram × Rp 10K/kg = Rp 600K
    
    TOTAL: Rp 850K/3 bulan
    ```
    
    **PROFIT:**
    ```
    - Revenue: Rp 850K
    - Biaya: Rp 431K
    - PROFIT: Rp 419K/3 bulan = Rp 140K/bulan
    
    ROI: Rp 5.5 juta / (Rp 419K × 4) = 3.3 tahun
    
    Catatan: Skala kecil, ROI agak lama
    Untuk profit lebih besar, scale up!
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Rakocy, J. E., et al. (2006).** Aquaponics - Integrating Fish and Plant Culture. SRAC Publication No. 454.
    
    2. **Somerville, C., et al. (2014).** Small-scale aquaponic food production. FAO Fisheries and Aquaculture Technical Paper No. 589.
    
    3. **Love, D. C., et al. (2015).** Commercial aquaponics production and profitability. Aquaculture, 435, 67-74.
    
    """)

# ===== TAB 5: EKONOMI SIRKULAR =====
with tab_circular:
    st.header("♻️ Ekonomi Sirkular dalam Pertanian")
    
    st.markdown("""
    ### Apa itu Ekonomi Sirkular?
    
    **Ekonomi Sirkular** adalah sistem ekonomi yang **meminimalkan limbah** dengan **mengubah limbah menjadi sumber daya** dalam siklus tertutup.
    
    **Prinsip:**
    - ♻️ **Reduce:** Kurangi input eksternal
    - ♻️ **Reuse:** Gunakan ulang material
    - ♻️ **Recycle:** Daur ulang limbah → Sumber daya
    - ♻️ **Regenerate:** Perbaiki sistem alami
    
    **Dalam Pertanian:**
    ```
    Limbah tanaman → Kompos/Pakan → Tanaman/Ternak
    Kotoran ternak → Biogas → Energi + Pupuk
    Air limbah → Biofilter → Irigasi
    Limbah organik → BSF → Pakan ternak
    
    GOAL: ZERO WASTE!
    ```
    
    ---
    
    ## 🔥 BIOGAS DARI KOTORAN TERNAK
    
    ### **Prinsip:**
    ```
    Kotoran ternak + Air → Digester (anaerobic)
    → Biogas (CH₄ 60-70%, CO₂ 30-40%)
    → Energi (masak, listrik)
    → Slurry (pupuk organik cair)
    ```
    
    ### **Desain Biodigester (Skala Rumah Tangga):**
    
    **A. Fixed Dome (Model China):**
    ```
    - Volume: 4-8 m³
    - Material: Beton/bata
    - Lifetime: 20-30 tahun
    - Biaya: Rp 10-15 juta
    
    Keuntungan:
    ✅ Tahan lama
    ✅ No maintenance
    
    Kekurangan:
    ❌ Biaya awal tinggi
    ❌ Perlu skill konstruksi
    ```
    
    **B. Floating Drum (Model India):**
    ```
    - Volume: 2-6 m³
    - Material: Drum besi + tangki beton
    - Lifetime: 10-15 tahun
    - Biaya: Rp 5-10 juta
    
    Keuntungan:
    ✅ Lebih murah
    ✅ Mudah monitoring (drum naik = gas penuh)
    
    Kekurangan:
    ❌ Drum bisa karat (perlu cat)
    ```
    
    **C. Balloon/Bag (Model Taiwan):**
    ```
    - Volume: 2-10 m³
    - Material: Plastik PVC/HDPE
    - Lifetime: 3-5 tahun
    - Biaya: Rp 2-5 juta
    
    Keuntungan:
    ✅ Paling murah
    ✅ Portable
    
    Kekurangan:
    ❌ Tidak tahan lama
    ❌ Mudah bocor
    ```
    
    ---
    
    ### **Produksi Biogas:**
    
    **Input:**
    ```
    - Kotoran sapi: 10 kg/hari (1 ekor)
    - Air: 10 L (rasio 1:1)
    - Retention time: 30-40 hari
    
    Volume digester: 10 kg × 40 hari = 400 kg = 4 m³
    ```
    
    **Output:**
    ```
    - Biogas: 0.3-0.4 m³/kg kotoran
      = 10 kg × 0.35 = 3.5 m³/hari
    
    - Setara LPG: 3.5 m³ × 0.6 = 2.1 kg LPG/hari
      = Rp 20K/hari = Rp 600K/bulan
    
    - Slurry (pupuk cair): 10 L/hari
      = 300 L/bulan
      = Cukup untuk 0.5-1 ha!
    ```
    
    **EKONOMI:**
    ```
    INVESTASI: Rp 10 juta (fixed dome)
    
    HEMAT:
    - LPG: Rp 600K/bulan = Rp 7.2 juta/tahun
    - Pupuk: Rp 2-3 juta/tahun
    
    TOTAL HEMAT: Rp 9-10 juta/tahun
    
    ROI: 1 tahun!
    ```
    
    ---
    
    ## 🪰 BSF (Black Soldier Fly) untuk Pakan
    
    ### **Apa itu BSF?**
    
    **Black Soldier Fly (Hermetia illucens)** adalah lalat yang **larvanya** dapat **mengkonversi limbah organik** menjadi **protein tinggi** untuk pakan ternak.
    
    **Keuntungan:**
    ```
    ✅ Protein tinggi: 40-45% (setara tepung ikan!)
    ✅ Lemak: 30-35% (energi tinggi)
    ✅ Konversi cepat: 10-14 hari (telur → larva siap panen)
    ✅ Waste reduction: 80-90% (limbah jadi maggot + kompos)
    ✅ No smell: BSF tidak bau (vs lalat biasa)
    ✅ Self-harvesting: Larva crawl out (mudah panen)
    ```
    
    ### **Siklus BSF:**
    ```
    1. Telur (3-4 hari) → Larva
    2. Larva (10-14 hari) → Makan limbah organik
    3. Pre-pupa (crawl out) → Panen!
    4. Pupa (7-14 hari) → Adult fly
    5. Adult (5-8 hari) → Kawin, bertelur → Mati
    
    Total cycle: 30-40 hari
    ```
    
    ### **Budidaya BSF:**
    
    **A. Breeding Cage (Kandang Kawin):**
    ```
    - Ukuran: 2 × 2 × 2 m
    - Material: Kasa nyamuk
    - Populasi: 1,000-5,000 adult flies
    - Egg trap: Kardus bergelombang
    - Telur: 500-1,000 butir/betina
    ```
    
    **B. Rearing Bin (Bak Larva):**
    ```
    - Ukuran: 1 × 0.5 × 0.3 m
    - Material: Plastik/kayu
    - Kapasitas: 10-20 kg limbah
    - Populasi: 5,000-10,000 larva
    - Panen: 1-2 kg maggot/bin (setelah 10-14 hari)
    ```
    
    **C. Limbah Organik:**
    ```
    - Sisa dapur, sayuran busuk
    - Kotoran ternak (ayam, babi)
    - Limbah pasar
    - Ampas tahu, onggok
    
    Rasio: 1 kg telur → 10 kg maggot (dari 100 kg limbah)
    Konversi: 10:1 (10 kg limbah → 1 kg maggot)
    ```
    
    ---
    
    ### **EKONOMI BSF:**
    
    **Skala Kecil (100 kg limbah/hari):**
    ```
    INVESTASI:
    - Breeding cage: Rp 2 juta
    - Rearing bins (10 unit): Rp 1 juta
    - Starter colony: Rp 500K
    
    TOTAL: Rp 3.5 juta
    
    PRODUKSI:
    - Limbah: 100 kg/hari
    - Maggot: 10 kg/hari (fresh)
    - Maggot kering: 3 kg/hari (30% moisture)
    
    PENDAPATAN:
    - Maggot segar: 10 kg × Rp 5K = Rp 50K/hari
    - atau Maggot kering: 3 kg × Rp 20K = Rp 60K/hari
    
    Per bulan: Rp 1.5-1.8 juta
    
    BIAYA:
    - Limbah: Gratis (dari pasar/rumah tangga)
    - Tenaga kerja: Rp 500K/bulan
    
    PROFIT: Rp 1-1.3 juta/bulan
    
    ROI: 3-4 bulan
    ```
    
    ---
    
    ## 💧 ZERO WASTE WATER
    
    ### **Sistem Biofilter:**
    ```
    1. Air limbah (grey water) → Settling tank (sedimentasi)
    2. Settling tank → Biofilter (tanaman air)
    3. Biofilter → Storage tank (air bersih)
    4. Storage tank → Irigasi
    
    Tanaman biofilter:
    - Eceng gondok (Water hyacinth)
    - Kangkung air
    - Kiambang (Duckweed)
    
    Removal efficiency:
    - BOD: 80-90%
    - N: 70-80%
    - P: 60-70%
    
    Bonus: Tanaman biofilter → Pakan ternak!
    ```
    
    ---
    
    ## 📊 CONTOH FARM ZERO WASTE
    
    ### **Integrated Farm (1 Ha):**
    ```
    KOMPONEN:
    1. Padi (0.5 ha) → Jerami
    2. Sayuran (0.3 ha) → Limbah
    3. Sapi (5 ekor) → Kotoran
    4. Ayam (500 ekor) → Kotoran
    5. Kolam ikan (0.2 ha) → Air limbah
    
    SIKLUS:
    - Jerami → Pakan sapi (fermentasi)
    - Limbah sayuran → BSF → Pakan ayam
    - Kotoran sapi → Biogas → Energi + Slurry
    - Kotoran ayam → Kompos → Pupuk padi/sayuran
    - Slurry → Pupuk cair → Padi/sayuran
    - Air kolam → Irigasi padi/sayuran
    
    ZERO WASTE:
    - Limbah organik: 100% recycle (BSF + kompos)
    - Kotoran: 100% recycle (biogas + pupuk)
    - Air: 90% recycle (biofilter + irigasi)
    
    HEMAT:
    - Pupuk kimia: 70-80%
    - Pakan: 30-50%
    - Energi (LPG): 100%
    - Air: 50-60%
    
    ADDITIONAL INCOME:
    - Biogas: Rp 3-5 juta/tahun (hemat LPG)
    - Maggot BSF: Rp 10-15 juta/tahun
    - Kompos (dijual): Rp 5-10 juta/tahun
    
    TOTAL ADDITIONAL: Rp 18-30 juta/tahun
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Ellen MacArthur Foundation. (2013).** Towards the Circular Economy. EMF.
    
    2. **FAO. (2013).** Biogas Technology: A Training Manual. FAO.
    
    3. **Diener, S., et al. (2011).** Conversion of organic material by black soldier fly larvae. Waste Management, 31, 2222-2229.
    
    4. **Pretty, J., et al. (2018).** Global assessment of agricultural system redesign for sustainable intensification. Nature Sustainability, 1, 441-446.
    
    """)
