import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="SOP Documentation Center",
    page_icon="📚",
    layout="wide"
)

# user = require_auth()
# show_user_info_sidebar()

# Custom CSS
st.markdown("""
<style>
    .sop-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .commodity-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .phase-section {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #10b981;
    }
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="sop-header">
    <h1>📚 SOP Documentation Center</h1>
    <p>Standard Operating Procedures - Precision Farming</p>
    <p><strong>Standar: MHI + GAP + ISO 22000</strong></p>
</div>
""", unsafe_allow_html=True)

# Tabs for each commodity
tab1, tab2, tab3, tab4 = st.tabs([
    "🍈 Melon (25 T/ha)",
    "🌶️ Cabai (18 T/ha)", 
    "🌾 Padi (10 T/ha)",
    "📊 Komparasi"
])

# ===== TAB 1: MELON =====
with tab1:
    st.markdown("## 🍈 SOP Melon Eksklusif MHI - Target 25 Ton/Ha")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><h3>20,000</h3><p>Tanaman/Ha</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h3>70 Hari</h3><p>Siklus Tanam</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h3>>13%</h3><p>Target Brix</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><h3>Rp 375 Jt</h3><p>Revenue/Ha</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 📋 Spesifikasi Teknis")
    with st.expander("📌 Detail Spesifikasi", expanded=True):
        st.markdown("""
        - **Varietas**: Golden Aroma, Stella, Action
        - **Jarak Tanam**: 50 cm x 100 cm (dalam bedengan x antar bedengan)
        - **Sistem**: Greenhouse/Screenhouse + Irigasi Tetes
        - **Substrat**: Cocopeat + Sekam (70:30) atau Tanah Lempung Berpasir
        - **Target Grade**: A Export (Brix >13%, Netting sempurna)
        """)
    
    st.markdown("### 🧪 Jadwal Fertigasi (4 Fase)")
    
    # Fase 1
    with st.expander("🌱 Fase 1: Vegetatif (HST 0-25)", expanded=False):
        st.markdown("""
        **Target EC**: 1.8 mS/cm  
        **Volume Air**: 0.8 L/tanaman/hari (5-8x pulse)
        
        **Formula Pupuk (per 1000L tangki)**:
        - Calcium Nitrate: 800 g → N: 180 ppm, Ca: 150 ppm
        - KNO3: 400 g → K: 200 ppm
        - MKP (0-52-34): 200 g → P: 60 ppm
        - MgSO4: 300 g → Mg: 50 ppm
        
        **Tugas Mandor**:
        - ✅ Pewiwilan tunas air (setiap 3 hari)
        - ✅ Lilit sulur ke tali rafia
        - ✅ Aplikasi pupuk N-Ca rutin
        - ✅ Monitor EC larutan (1.6-2.0 mS/cm)
        """)
    
    # Fase 2
    with st.expander("🌸 Fase 2: Pembungaan & Polinasi (HST 26-35)", expanded=False):
        st.markdown("""
        **Target EC**: 2.0 mS/cm  
        **Volume Air**: 1.0 L/tanaman/hari
        
        **Nutrisi**:
        - N: 120 ppm | P: 80 ppm | K: 220 ppm | Ca: 180 ppm
        
        **Tugas KRITIS**:
        - 🐝 Introduksi lebah Trigona (1 koloni/1000m²)
        - ⛔ STOP semua pestisida H-3 hingga H+5 polinasi
        - ✂️ Seleksi bunga: 1 bunga per ketiak daun
        - 🌡️ Jaga suhu 25-28°C (ventilasi optimal)
        - 💧 Spray Kalsium Boron (2 ml/L) setiap 2 hari
        """)
    
    # Fase 3
    with st.expander("🍈 Fase 3: Pembesaran Buah (HST 36-55)", expanded=False):
        st.markdown("""
        **Target EC**: 2.2 mS/cm  
        **Volume Air**: 1.5 L/tanaman/hari
        
        **Nutrisi**:
        - N: 150 ppm | P: 70 ppm | K: 300 ppm (K DOMINAN) | Ca: 200 ppm
        
        **Tugas KRITIS**:
        - 🎯 Topging (seleksi 1 buah terbaik/tanaman) H+10 fruit set
        - 🕸️ Gantung buah dengan jaring plastik
        - 📊 Monitor Brix mingguan (refraktometer)
        - ✨ Cek netting: harus mulai muncul H+40
        - 🐛 Pengendalian ulat/lalat buah (trap + spray)
        """)
    
    # Fase 4
    with st.expander("🍯 Fase 4: Pematangan (HST 56-70)", expanded=False):
        st.markdown("""
        **Target EC**: 1.8 mS/cm (turunkan)  
        **Volume Air**: 0.8 L/tanaman/hari (DRY DOWN)
        
        **Nutrisi**:
        - N: 80 ppm (KURANGI drastis) | P: 60 ppm | K: 350 ppm (K SANGAT TINGGI)
        
        **Strategi Water Stress**:
        - 💧 Kurangi frekuensi irigasi (3-4x/hari → 2x/hari)
        - ⛔ Stop N total H-10 panen
        - 🍯 Target Brix >13% (cek setiap 3 hari)
        - ✂️ Panen saat slip (pecah tangkai), aroma harum
        
        **Indikator Panen**:
        - Netting sempurna 100%
        - Warna kulit kuning keemasan
        - Aroma khas melon kuat
        - Tangkai mulai retak (slip)
        """)
    
    st.markdown("### 🐛 Pengendalian Hama & Penyakit")
    with st.expander("📋 Protokol IPM", expanded=False):
        st.markdown("""
        | Hama/Penyakit | Bahan Aktif | Dosis | Rotasi |
        |---------------|-------------|-------|--------|
        | Kutu Daun | Imidacloprid 200 WP | 0.5 g/L | Acetamiprid (minggu ke-2) |
        | Thrips | Abamectin 18 EC | 1 ml/L | Spinosad (minggu ke-2) |
        | Powdery Mildew | Sulfur 80 WP | 2 g/L | Azoxystrobin (minggu ke-2) |
        | Downy Mildew | Metalaxyl + Mancozeb | 2 g/L | Cymoxanil (minggu ke-2) |
        | Lalat Buah | Trap metil eugenol | 1 botol/500m² | + Deltamethrin spray |
        
        **Prinsip Rotasi**: Ganti FRAC code setiap 7-10 hari untuk hindari resistensi
        """)

# ===== TAB 2: CABAI =====
with tab2:
    st.markdown("## 🌶️ SOP Cabai Merah Intensif - Target 18 Ton/Ha")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><h3>18,000</h3><p>Tanaman/Ha</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h3>120 Hari</h3><p>Siklus Tanam</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h3>>12 cm</h3><p>Panjang Buah</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><h3>Rp 450 Jt</h3><p>Revenue/Ha</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 📋 Spesifikasi Teknis")
    with st.expander("📌 Detail Spesifikasi", expanded=True):
        st.markdown("""
        - **Varietas**: Lado F1, Gada F1, Laris F1 (tahan virus)
        - **Jarak Tanam**: 60 cm x 60 cm (double row)
        - **Sistem**: Mulsa plastik hitam-perak + Irigasi tetes + Tali gawar
        - **Target**: Buah merah 80%, panjang >12 cm, diameter >2 cm
        """)
    
    st.markdown("### 🧪 Jadwal Pemupukan (4 Fase)")
    
    # Fase 1
    with st.expander("🌱 Fase 1: Vegetatif (HST 0-30)", expanded=False):
        st.markdown("""
        **Pupuk Dasar (sebelum tanam)**:
        - Pupuk Kandang: 20 ton/ha (fermentasi sempurna)
        - Dolomit: 1 ton/ha (jika pH <6.0)
        - SP-36: 200 kg/ha
        - KCl: 150 kg/ha
        
        **Fertigasi Mingguan**:
        - NPK 16-16-16: 200 kg/ha (50 kg/minggu)
        - Calcium Nitrate: 100 kg/ha (25 kg/minggu)
        - Target EC: 1.5 mS/cm
        
        **Tugas Mandor**:
        - ✂️ Rempel tunas di bawah cabang Y
        - 🎋 Pasang ajir bambu 1.5m atau tali gawar
        - 🛡️ Aplikasi mulsa plastik hitam-perak
        - 🐛 Monitor Kutu Kebul (vektor virus kuning)
        """)
    
    # Fase 2
    with st.expander("🌸 Fase 2: Pembungaan (HST 31-50)", expanded=False):
        st.markdown("""
        **Fertigasi**:
        - KNO3: 150 kg/ha
        - Calcium Nitrate: 200 kg/ha
        - MKP (0-52-34): 50 kg/ha
        - Target EC: 2.0 mS/cm
        
        **Spray Foliar (2-3x/minggu)**:
        - Kalsium Boron: 2 g/L (ANTI-RONTOK)
        - Asam Amino: 1 ml/L
        
        **Tugas KRITIS**:
        - 🕸️ Pasang tali gawar vertikal (sistem V)
        - 🪰 Trap lalat buah (metil eugenol, 1 botol/500m²)
        - 🧪 Cek pH tanah (target 6.0-6.5)
        - 🦠 Roguing tanaman terinfeksi virus (bakar!)
        """)
    
    # Fase 3
    with st.expander("🌶️ Fase 3: Pembesaran Buah (HST 51-80)", expanded=False):
        st.markdown("""
        **Fertigasi**:
        - KNO3: 200 kg/ha
        - KCl: 150 kg/ha
        - MKP: 30 kg/ha
        - Target EC: 2.5 mS/cm
        
        **Tugas KRITIS**:
        - 💧 Irigasi 2x/hari (pagi 06:00, sore 16:00)
        - 🍄 Fungisida rotasi FRAC:
          - Minggu 1: Azoxystrobin (FRAC 11)
          - Minggu 2: Difenoconazole (FRAC 3)
          - Minggu 3: Mancozeb (FRAC M3)
        - 🧹 Sanitasi: buang buah busuk, gulma
        - 📊 Monitor EC larutan (2.0-2.5 mS/cm)
        """)
    
    # Fase 4
    with st.expander("🌶️ Fase 4: Panen Raya (HST 81-120)", expanded=False):
        st.markdown("""
        **Fertigasi Maintenance**:
        - NPK 15-15-15: 150 kg/ha/bulan
        - KCl: 100 kg/ha/bulan
        
        **Protokol Panen**:
        - 📅 Interval 3-4 hari (merah 80%)
        - 📏 Sortasi:
          - Grade A: >12 cm, diameter >2 cm
          - Grade B: 8-12 cm
          - Reject: <8 cm, cacat, busuk
        - 🔄 Rotasi pestisida (hindari resistensi)
        - 🪱 Cek nematoda (gejala layu, akar bengkak)
        """)

# ===== TAB 3: PADI =====
with tab3:
    st.markdown("## 🌾 SOP Padi Sawah Super Intensif - Target 10 Ton/Ha GKG")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-box"><h3>160,000</h3><p>Rumpun/Ha</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-box"><h3>105 Hari</h3><p>Siklus Tanam</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-box"><h3>>28 gram</h3><p>Bobot 1000 Butir</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-box"><h3>Rp 60 Jt</h3><p>Revenue/Ha</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 📋 Spesifikasi Teknis")
    with st.expander("📌 Detail Spesifikasi", expanded=True):
        st.markdown("""
        - **Varietas**: Inpari 32, Inpari 42, Ciherang (umur 115-120 hari)
        - **Sistem Tanam**: Jajar Legowo 2:1 (25 cm x 12.5 cm x 50 cm lorong)
        - **Bibit**: Muda (15-21 HSS), 1-2 batang/lubang
        - **Target**: GKG 10 ton/ha, rendemen 65%, kadar air 14%
        """)
    
    st.markdown("### 🧪 Jadwal Pemupukan (4 Fase)")
    
    # Persiapan
    with st.expander("🚜 Persiapan Lahan (H-14 s/d H-0)", expanded=False):
        st.markdown("""
        **Pengolahan Tanah**:
        - Bajak 2x (kedalaman 20-25 cm)
        - Garu 2x (tanah lumpur sempurna)
        - Ratakan dengan papan perata
        
        **Pemupukan Organik**:
        - Kompos: 2 ton/ha ATAU
        - Pupuk kandang: 3 ton/ha (fermentasi sempurna)
        - Kapur pertanian: 500 kg/ha (jika pH <5.5)
        
        **Pengairan**: Macak-macak (genangan 2-3 cm)
        """)
    
    # Fase 1
    with st.expander("🌱 Fase 1: Vegetatif/Anakan (HST 0-40)", expanded=False):
        st.markdown("""
        **Pupuk Dasar (H-0, sebelum tanam)**:
        - Urea: 100 kg/ha
        - SP-36: 150 kg/ha
        - KCl: 100 kg/ha
        - ZA: 50 kg/ha (untuk tanah masam)
        
        **Pupuk Susulan I (HST 21)**:
        - Urea: 100 kg/ha
        - NPK Phonska (15-15-15): 150 kg/ha
        
        **Tugas KRITIS**:
        - 🌱 Tanam Jajar Legowo 2:1 (2 baris : 1 lorong)
        - 💧 Pengairan macak-macak (0-10 HST)
        - 💧 Genangan 2-3 cm (10-40 HST)
        - 🌿 Penyiangan I (HST 15-20) + herbisida selektif
        - 🐌 Monitor keong mas & penggerek batang
        - 🎯 Target: 25-30 anakan produktif/rumpun
        """)
    
    # Fase 2
    with st.expander("🌾 Fase 2: Primordia/Bunting (HST 41-65)", expanded=False):
        st.markdown("""
        **Pupuk Susulan II (HST 42)**:
        - Urea: 75 kg/ha
        - KCl: 75 kg/ha
        
        **Aplikasi Khusus (HST 45-50)**:
        - MKP (0-52-34): 2 kg/ha (spray foliar)
        - ZPT Giberelin: 1 tablet/15L (perpanjangan malai)
        
        **Tugas KRITIS**:
        - 💧 Genangan 5-7 cm (FASE KRITIS!)
        - 🌿 Penyiangan II (HST 40-45)
        - 🐛 Monitor hama:
          - Penggerek batang (Scirpophaga)
          - Wereng coklat (Nilaparvata)
          - Hawar daun bakteri
          - Blast (Pyricularia)
        - 📊 SPAD Meter: kadar N daun (target >35)
        """)
    
    # Fase 3
    with st.expander("🌾 Fase 3: Pengisian Bulir (HST 66-90)", expanded=False):
        st.markdown("""
        **Pupuk Susulan III (HST 70)**:
        - KCl: 50 kg/ha
        - MKP: 2 kg/ha (spray)
        
        **Spray Foliar (2x/minggu)**:
        - Pupuk daun P-K tinggi (NPK 10-50-40): 2 g/L
        
        **Manajemen Air AWD (Alternate Wetting Drying)**:
        - 3 hari kering (tanah retak 1-2 cm)
        - 1 hari basah (genangan 3 cm)
        
        **Tugas KRITIS**:
        - 🍃 Jaga daun bendera tetap hijau
        - 🦅 Halau burung (jaring/orang-orangan)
        - 🐛 Monitor Walang Sangit & Kepinding Tanah
        - 🐭 TBS (Trap Barrier System) untuk tikus
        - 🎯 Target: Bobot 1000 butir >28 gram
        """)
    
    # Fase 4
    with st.expander("🌾 Fase 4: Pematangan & Panen (HST 91-105)", expanded=False):
        st.markdown("""
        **Tugas KRITIS**:
        - 💧 Keringkan lahan total (10-14 hari sebelum panen)
        - ✅ Cek kematangan:
          - 90% bulir kuning
          - Kadar air 22-24%
          - Batang mulai rebah
        
        **Protokol Panen**:
        - ⏰ Panen pagi hari (06:00-10:00)
        - 🚜 Combine harvester (losses 2-3%) ATAU
        - ✂️ Sabit bergerigi + perontok (losses 5-7%)
        - ⚡ Perontokan segera (max 24 jam)
        
        **Pengeringan**:
        - ☀️ Jemur: 3-4 hari (kadar air 14%)
        - 🔥 Dryer: 8-12 jam (suhu 40-45°C)
        
        **Evaluasi**:
        - 📊 Hitung GKG (Gabah Kering Giling)
        - 📈 Rendemen (target 65%)
        - 📉 Losses (target <5%)
        - 🌾 Kualitas beras (% kepala vs patah)
        """)

# ===== TAB 4: KOMPARASI =====
with tab4:
    st.markdown("## 📊 Analisis Komparatif 3 Komoditas")
    
    # Comparison table
    comparison_data = {
        'Parameter': [
            'Target Yield',
            'Populasi',
            'Siklus (hari)',
            'Sistem Irigasi',
            'Pupuk N Total',
            'Pupuk P Total',
            'Pupuk K Total',
            'Investasi/Ha',
            'Revenue/Ha',
            'Margin (%)'
        ],
        'Melon 🍈': [
            '25 T/ha',
            '20,000',
            '70',
            'Tetes (pulse)',
            '550 kg',
            '270 kg',
            '1,070 kg',
            'Rp 150 jt',
            'Rp 375 jt',
            '60%'
        ],
        'Cabai 🌶️': [
            '18 T/ha',
            '18,000',
            '120',
            'Tetes (2x/hari)',
            '600 kg',
            '250 kg',
            '650 kg',
            'Rp 80 jt',
            'Rp 450 jt',
            '82%'
        ],
        'Padi 🌾': [
            '10 T/ha GKG',
            '160,000',
            '105',
            'Genangan/AWD',
            '275 kg',
            '150 kg',
            '325 kg',
            'Rp 25 jt',
            'Rp 60 jt',
            '58%'
        ]
    }
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)
    
    st.markdown("### 🎯 Key Success Factors")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="commodity-card">
        <h4>🍈 Melon</h4>
        <ol>
        <li><strong>Polinasi sempurna</strong> (lebah + manual)</li>
        <li><strong>EC control ketat</strong> (1.8-2.2 mS/cm)</li>
        <li><strong>Water stress</strong> (fase akhir untuk Brix)</li>
        <li><strong>Topging tepat waktu</strong> (1 buah/tanaman)</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="commodity-card">
        <h4>🌶️ Cabai</h4>
        <ol>
        <li><strong>Kalsium tinggi</strong> (anti-rontok bunga)</li>
        <li><strong>Rotasi fungisida</strong> (FRAC code berbeda)</li>
        <li><strong>Sanitasi ketat</strong> (virus & nematoda)</li>
        <li><strong>Panen tepat waktu</strong> (merah 80%)</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="commodity-card">
        <h4>🌾 Padi</h4>
        <ol>
        <li><strong>Bibit muda</strong> (15-21 HSS)</li>
        <li><strong>Jajar Legowo 2:1</strong> (populasi optimal)</li>
        <li><strong>AWD irrigation</strong> (efisiensi air)</li>
        <li><strong>Pemupukan berimbang</strong> (N-P-K sesuai fase)</li>
        </ol>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📥 Download Dokumentasi")
    
    st.info("""
    📄 **Dokumen SOP Lengkap** tersedia di:  
    `agrisensa_tech/docs/SOP_Precision_Farming.md`
    
    Dokumen mencakup:
    - Formula pupuk detail per fase
    - Protokol IPM lengkap
    - Manajemen air komprehensif
    - Evaluasi hasil panen
    - Referensi standar (MHI + GAP + ISO 22000)
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p><strong>📚 AgriSensa SOP Documentation Center</strong></p>
    <p>Precision Farming Standards | Version 2.0 (2024)</p>
    <p><small>Standar: MHI + GAP + ISO 22000</small></p>
</div>
""", unsafe_allow_html=True)
