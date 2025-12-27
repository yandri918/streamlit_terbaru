import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.microbe_production_service import MicrobeProductionService
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Mikroba & Biofertilizer Production",
    page_icon="🦠",
    layout="wide"
)

user = require_auth()
show_user_info_sidebar()

# Initialize service
service = MicrobeProductionService()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
    }
    .protocol-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        margin: 15px 0;
    }
    .microbe-box {
        background: white;
        padding: 15px;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🦠 Mikroba & Biofertilizer Production Center</h1>
    <p>Produksi Pupuk Hayati & Agen Biokontrol Berkualitas Tinggi</p>
    <p><strong>Standar: SNI 7763:2018 | ISO 17025</strong></p>
</div>
""", unsafe_allow_html=True)

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab_qc, tab_calc = st.tabs([
    "🐮 ROTAN",
    "🦠 MOL", 
    "🌱 PGPR",
    "🍄 Trichoderma",
    "🐛 Beauveria",
    "🦗 Metarhizium",
    "🌾 N-Fixers",
    "🔬 Quality Control",
    "💰 Business Calculator"
])

# ===== TAB 1: ROTAN =====
with tab1:
    st.header("🐮 ROTAN (Ramuan Organik Tanaman)")
    st.info("**Bioaktivator Super** dengan 18+ mikroba menguntungkan dari cairan rumen sapi")
    
    # Subtabs for ROTAN
    rotan_tab1, rotan_tab2, rotan_tab3, rotan_tab4 = st.tabs([
        "Bioaktivator", "POC Premium", "Perbanyakan Masal", "Kandungan Mikroba"
    ])
    
    with rotan_tab1:
        st.subheader("🐮 ROTAN Bioaktivator (Cairan Rumen Sapi)")
        
        col1, col2 = st.columns([1, 1.2])
        
        with col1:
            st.markdown("#### 🥦 Bahan-Bahan")
            st.warning("**Bahan Utama:**")
            st.markdown("""
            - **Cairan Rumen Sapi**: 2 Liter
            - **Molase** (Tetes Tebu): 2 Liter  
            - **Air Rebusan Dedak**: 4 Liter
            - **Urine Ternak** (fermentasi 1 minggu): 4 Liter
            
            **Bahan Tambahan:**
            - Ragi Tape: 2-3 butir
            - Terasi: ½ - 1 ons
            - Buah Nanas: 1 buah
            """)
            
        with col2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1. **Air Dedak**: Rebus 1 kg dedak + 5L air, dinginkan, saring (ambil 4L)
            2. **Campur Utama**: Rumen 2L + Molase 2L, aduk rata
            3. **Tambah Dedak**: Masukkan air dedak 4L
            4. **Haluskan**: Parut nanas + encerkan terasi, masukkan
            5. **Ragi**: Hancurkan 2-3 butir ragi tape, masukkan
            6. **Urine**: Tambahkan 4L urine ternak
            7. **Fermentasi**: Tutup rapat (anaerob), simpan **14 hari**
            """)
        
        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.success("✅ **Ciri Berhasil:**")
            st.markdown("- Bau fermentasi harum/asam segar\n- Warna kuning kecoklatan\n- Tidak keruh")
        with col_b:
            st.error("❌ **Ciri Gagal:**")
            st.markdown("- Bau busuk (got/bangkai)\n- Warna coklat kehitaman\n- Banyak jamur hitam/abu")
    
    with rotan_tab2:
        st.subheader("🍎 POC ROTAN Premium (Multi-Fruit Formula)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🥦 Bahan-Bahan")
            st.markdown("""
            **Buah-buahan:**
            - Pisang: 5 buah
            - Pepaya: 1 buah
            - Nanas: 1 buah
            - Mangga: 2 buah
            - Melon/Semangka: 1 buah
            
            **Sayuran:**
            - Kangkung Air: 3 ikat
            - Kacang Panjang: 3 ikat
            - Jagung Muda: 2 buah
            
            **Tambahan:**
            - Air Kelapa: 5 L
            - Air Leri: 3 L
            - Gula Kelapa: 1 kg
            - Usus Ikan: 2 ons
            - Ragi: 3 butir
            """)
        
        with col2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1. **Blender**: Haluskan semua buah + sayuran seperti jus
            2. **Rebus Gula**: Didihkan gula kelapa + 1L air, dinginkan
            3. **Campur**: Jus + Gula cair + Air kelapa + Air leri + Usus ikan + Ragi
            4. **Wadah**: Simpan di wadah **Tembikar/Plastik** (JANGAN logam!)
            5. **Fermentasi**: Tutup rapat, **10-14 hari**
            6. **Perawatan**: Buka & aduk setiap **2 hari sekali** (5 menit)
            """)
            
            st.success("✅ **Hasil**: Bau asam harum tape, tidak ada gas")
            st.info("💡 **Ampas jangan dibuang!** Masih kaya mikroba")
    
    with rotan_tab3:
        st.subheader("📈 Perbanyakan Masal ROTAN")
        st.markdown("**1 Liter biang → 100 Liter POC kualitas SAMA!**")
        
        # Calculator
        st.markdown("#### 🧮 Kalkulator Perbanyakan")
        col_calc1, col_calc2 = st.columns(2)
        with col_calc1:
            biang_vol = st.number_input("Volume Biang ROTAN (Liter)", 1, 100, 1)
        with col_calc2:
            target_vol = st.number_input("Target Volume (Liter)", 10, 10000, 100)
        
        if st.button("Hitung Kebutuhan Bahan"):
            result = service.calculate_mass_multiplication(biang_vol, target_vol)
            
            st.success(f"**Hasil Perhitungan untuk {target_vol} Liter:**")
            
            col_r1, col_r2 = st.columns(2)
            with col_r1:
                st.markdown("**Bahan yang Dibutuhkan:**")
                for ingredient, qty in result['ingredients'].items():
                    st.write(f"- {ingredient}: {qty:.1f} {'L' if 'Air' in ingredient else 'kg'}")
            
            with col_r2:
                st.metric("Total Biaya", f"Rp {result['estimated_cost']:,.0f}")
                st.metric("Biaya per Liter", f"Rp {result['cost_per_liter']:,.0f}")
                st.metric("Waktu Fermentasi", f"{result['fermentation_days']} hari")
    
    with rotan_tab4:
        st.subheader("🧬 Kandungan Mikroba ROTAN")
        
        microbe_data = {
            'Kategori': [
                'Selulolitik', 'Selulolitik', 'Selulolitik',
                'Penambat N', 'Penambat N', 'Penambat N',
                'Pelarut P', 'Pelarut P', 'Pelarut P',
                'ZPT Producer', 'ZPT Producer'
            ],
            'Mikroba': [
                'Bacteroides succinogenes', 'Cillobacterium cellulosolvens', 'Lactobacillus sp.',
                'Azotobacter sp.', 'Azospirillum sp.', 'Nitrosomonas sp.',
                'Aspergillus niger', 'Bacillus subtilis', 'Bacillus megatherium',
                'Acetobacter sp.', 'Actinomycetes sp.'
            ],
            'Fungsi Utama': [
                'Pengurai selulosa → asam organik', 'Pengurai serat kasar', 'Fermentasi asam laktat',
                'Fiksasi N₂ (20-40 kg/ha/tahun)', 'Fiksasi N₂ + IAA (25% ↑ akar)', 'Nitrifikasi NH₃→NO₂',
                'Solubilisasi P (30-50%)', 'Pelarut P + biocontrol', 'Mobilisasi P (40 kg/ha)',
                'Produksi IAA (auxin)', 'Antibiotik + fitohormon'
            ]
        }
        
        df_microbe = pd.DataFrame(microbe_data)
        st.dataframe(df_microbe, use_container_width=True, hide_index=True)
        
        st.info("""
        📚 **Referensi Ilmiah:**
        - Weimer et al. (1990). *Applied and Environmental Microbiology*
        - Kennedy et al. (2004). *Soil Biology and Biochemistry*
        - Vassilev et al. (2006). *Applied Microbiology and Biotechnology*
        """)

# ===== TAB 2: MOL =====
with tab2:
    st.header("🦠 MOL (Mikro Organisme Lokal)")
    st.info("Kumpulan resep MOL sederhana menggunakan bahan lokal")
    
    mol_type = st.selectbox("Pilih Jenis MOL:", [
        "MOL Sayuran (Vegetatif)",
        "MOL Buah (Generatif)", 
        "MOL Rebung Bambu (Giberelin)",
        "MOL Keong Mas (Asam Amino)",
        "MOL Bonggol Pisang (Sitokinin)",
        "MOL Sabut Kelapa (Kalium)",
        "MOL Gedebok Pisang (Fosfat)"
    ])
    
    mol_recipes = {
        "MOL Sayuran (Vegetatif)": {
            "bahan": "Sayuran beragam 3kg, Gula merah 0.5kg, Garam 150g, Air leri 3L, Air kelapa 2L",
            "cara": "1. Cincang/blender sayuran\n2. Campur semua, kocok 3-5 menit\n3. Simpan tertutup, tempat teduh\n4. Fermentasi 14 hari",
            "dosis": "1L MOL : 10L Air (10%)",
            "fungsi": "Pupuk fase vegetatif (pertumbuhan daun)"
        },
        "MOL Buah (Generatif)": {
            "bahan": "Buah matang 2kg (pepaya/mangga/pisang), Gula merah 0.5kg, Air kelapa 5L",
            "cara": "1. Cincang/blender buah\n2. Campur semua, kocok\n3. Simpan tertutup\n4. Fermentasi 14 hari",
            "dosis": "1L MOL : 10L Air (10%)",
            "fungsi": "Pupuk fase generatif (pembuahan) + booster manis"
        },
        "MOL Rebung Bambu (Giberelin)": {
            "bahan": "Rebung bambu 1kg, Air leri 5L, Gula merah 0.5kg",
            "cara": "1. Iris tipis rebung\n2. Campur dengan gula + air leri\n3. Kocok, buka tutup tiap pagi (buang gas)\n4. Siap 15 hari",
            "dosis": "Kompos: 1:5 | Tanaman: 1:15",
            "fungsi": "Perangsang tumbuh (Giberelin) + dekomposer"
        },
        "MOL Keong Mas (Asam Amino)": {
            "bahan": "Keong mas hidup 1kg, Buah maja ½ buah (atau gula 0.5kg), Air kelapa 5L",
            "cara": "1. Tumbuk halus keong (cangkang+daging)\n2. Tumbuk maja/gula\n3. Campur dengan air kelapa\n4. Kocok, buka tutup tiap pagi\n5. Siap 15 hari",
            "dosis": "Kompos: 1:5 + gula | Tanaman: 1L/tangki",
            "fungsi": "Sumber asam amino + dekomposer"
        },
        "MOL Bonggol Pisang (Sitokinin)": {
            "bahan": "Bonggol pisang 1kg, Gula merah 0.5 ons, Air leri 5L",
            "cara": "1. Potong kecil bonggol\n2. Larutkan gula + air leri\n3. Campur, tutup rapat\n4. Buka tiap 2 hari (buang gas)\n5. Fermentasi 14 hari",
            "dosis": "1L MOL : 10L Air (10%)",
            "fungsi": "Perangsang akar & tunas (Sitokinin)"
        },
        "MOL Sabut Kelapa (Kalium)": {
            "bahan": "Sabut kelapa, Air bersih",
            "cara": "1. Masukkan sabut ke drum\n2. Isi air sampai terendam\n3. Tutup rapat\n4. Biarkan 2 minggu\n5. Air coklat hitam siap pakai",
            "dosis": "1L MOL : 10L Air (10%)",
            "fungsi": "Pupuk K (Kalium) untuk pembuahan"
        },
        "MOL Gedebok Pisang (Fosfat)": {
            "bahan": "Batang pisang 2kg, Air nira 1L (atau gula jawa 0.5kg)",
            "cara": "1. Potong batang pisang\n2. Campur ¾ nira/gula\n3. Padatkan di baskom\n4. Siram sisa nira di atas\n5. Tutup, 2 minggu\n6. Peras airnya",
            "dosis": "1L MOL : 100L Air (1:100)",
            "fungsi": "Sumber fosfat + penguat batang"
        }
    }
    
    recipe = mol_recipes[mol_type]
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🥦 Bahan-Bahan")
        st.markdown(recipe['bahan'])
        
        st.markdown("#### 🎯 Fungsi")
        st.success(recipe['fungsi'])
    
    with col2:
        st.markdown("#### 🥣 Cara Pembuatan")
        st.markdown(recipe['cara'])
        
        st.markdown("#### 💉 Dosis Aplikasi")
        st.info(recipe['dosis'])

# ===== TAB 3: PGPR =====
with tab3:
    st.header("🌱 PGPR (Plant Growth Promoting Rhizobacteria)")
    st.info("Bakteri perangsang pertumbuhan tanaman yang hidup di rhizosphere")
    
    st.markdown("### 🦠 Spesies PGPR Utama")
    
    pgpr_data = {
        'Spesies': [
            'Pseudomonas fluorescens',
            'Bacillus subtilis',
            'Bacillus amyloliquefaciens',
            'Paenibacillus polymyxa'
        ],
        'Fungsi Utama': [
            'Biocontrol + Siderophore + HCN',
            'Pelarut P + Antibiotik (surfactin)',
            'Lipopeptide + ISR (Induced Systemic Resistance)',
            'N-fixation + P-solubilization + Antibiotik'
        ],
        'Efektivitas': [
            'Menekan penyakit layu 40-60%',
            'Dual function (nutrisi + biocontrol)',
            'Meningkatkan ketahanan tanaman',
            'All-in-one biofertilizer'
        ],
        'Target CFU': [
            '10⁸ - 10⁹ CFU/ml',
            '10⁸ - 10⁹ CFU/ml',
            '10⁸ - 10⁹ CFU/ml',
            '10⁸ - 10⁹ CFU/ml'
        ]
    }
    
    df_pgpr = pd.DataFrame(pgpr_data)
    st.dataframe(df_pgpr, use_container_width=True, hide_index=True)
    
    st.markdown("### 📋 Protokol Produksi")
    
    with st.expander("🔬 Isolasi dari Rhizosphere", expanded=True):
        st.markdown("""
        **Langkah-langkah:**
        1. **Sampling**: Ambil akar tanaman sehat + tanah rhizosphere
        2. **Serial Dilution**: 10⁻¹ hingga 10⁻⁹
        3. **Plating**: Nutrient Agar, inkubasi 28°C, 24-48 jam
        4. **Screening**: Uji antagonis, pelarut P, produksi IAA
        5. **Purifikasi**: Streak plate hingga kultur murni
        6. **Identifikasi**: 16S rRNA sequencing
        """)
    
    with st.expander("🧫 Mass Multiplication"):
        st.markdown("""
        **Media Kultur:**
        - Nutrient Broth: 8 g/L
        - Yeast Extract: 2 g/L
        - NaCl: 5 g/L
        - pH: 7.0
        
        **Kondisi Fermentasi:**
        - Suhu: 28-30°C
        - Agitasi: 150 rpm
        - Waktu: 48-72 jam
        - Target: 10⁸ - 10⁹ CFU/ml
        
        **Carrier Material:**
        - Peat moss (gambut)
        - Vermiculite
        - Biochar
        - Ratio: 1L kultur : 1kg carrier
        """)

# ===== TAB 4: Trichoderma =====
with tab4:
    st.header("🍄 Trichoderma sp. (Biocontrol Fungi)")
    st.info("Jamur antagonis untuk pengendalian penyakit tanah")
    
    tri_tab1, tri_tab2, tri_tab3 = st.tabs([
        "Isolasi Alami", "Produksi Massal", "Quality Control"
    ])
    
    with tri_tab1:
        st.subheader("🎍 Metode Isolasi Bambu (Tradisional)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🍚 Bahan")
            st.markdown("""
            - Nasi basi: 1 mangkuk (minimal 1 hari 1 malam)
            - Bambu: 3 ruas (baru ditebang lebih baik)
            - Pengikat: Tali/karet ban
            """)
            
            st.markdown("#### 🥣 Cara")
            st.markdown("""
            1. Potong bambu 3 ruas, belah dua
            2. Lubangi batas ruas (seukuran kelingking)
            3. **Cuci dengan air mengalir** (JANGAN PDAM!)
            4. Isi nasi basi di ruas tengah
            5. Tutup, ikat erat
            6. Kubur di hutan bambu (7-10 cm)
            7. Tunggu **7-10 hari**
            8. Panen: Jamur putih seperti kapas = Trichoderma!
            """)
        
        with col2:
            st.success("✅ **Hasil**: Nasi ditumbuhi jamur putih (biang Trichoderma)")
            st.warning("⚠️ **Penting**: Lokasi harus hutan bambu/dapuran bambu tanah subur")
    
    with tri_tab2:
        st.subheader("🏭 Produksi Massal (Substrate)")
        
        st.markdown("""
        **Substrate Formula:**
        - Rice bran (dedak): 70%
        - Corn meal (tepung jagung): 20%
        - Sawdust (serbuk gergaji): 10%
        - Kadar air: 60-65%
        
        **Prosedur:**
        1. **Mixing**: Campur semua bahan, tambah air hingga 60-65%
        2. **Sterilisasi**: Autoclave 121°C, 15 psi, 60 menit
        3. **Cooling**: Dinginkan hingga suhu ruang
        4. **Inokulasi**: Tambahkan biang Trichoderma (5-10%)
        5. **Inkubasi**: 25-28°C, 7-14 hari
        6. **Panen**: Spora hijau penuh, aroma jamur segar
        
        **Target**: 10⁷ - 10⁸ spores/gram
        """)
    
    with tri_tab3:
        st.subheader("🔬 Quality Control")
        
        st.markdown("""
        **Spore Counting (Hemocytometer):**
        1. Ambil 1g kultur + 9ml air steril
        2. Vortex 5 menit
        3. Serial dilution 10⁻⁴
        4. Teteskan ke hemocytometer
        5. Hitung di mikroskop (400x)
        6. Formula: Spores/ml = (Count × Dilution × 10⁴) / Volume
        
        **Viability Test:**
        - Germination test: >80% (inkubasi 24 jam)
        - Purity: No contamination (visual + microscope)
        
        **Antagonistic Activity:**
        - Dual culture test vs Fusarium/Rhizoctonia
        - Inhibition zone: >50% = Good
        """)

# ===== TAB 5: Beauveria =====
with tab5:
    st.header("🐛 Beauveria bassiana (Entomopathogenic Fungi)")
    st.info("Jamur patogen serangga (White Muscardine Disease)")
    
    st.markdown("### 🎯 Target Hama")
    st.markdown("""
    - Kutu daun (Aphids)
    - Thrips
    - Whitefly (Kutu kebul)
    - Ulat (Caterpillars)
    - Wereng (Planthoppers)
    """)
    
    st.markdown("### ⚙️ Mekanisme Kerja")
    
    mechanism_steps = [
        "1. **Adhesi**: Spora menempel ke kutikula serangga",
        "2. **Penetrasi**: Enzim protease + kitinase menembus kutikula",
        "3. **Kolonisasi**: Hifa tumbuh di hemolimf (darah serangga)",
        "4. **Toksin**: Produksi beauvericin (mengganggu mitokondria)",
        "5. **Kematian**: Serangga mati 7-14 hari (white muscardine)"
    ]
    
    for step in mechanism_steps:
        st.markdown(step)
    
    st.markdown("### 📋 Produksi")
    
    with st.expander("🍚 Substrate (Rice-based)"):
        st.markdown("""
        **Formula:**
        - Beras putih: 1 kg
        - Air: 1.2 L
        - Kadar air akhir: 50-55%
        
        **Prosedur:**
        1. Rendam beras 12 jam
        2. Kukus 30 menit
        3. Dinginkan
        4. Inokulasi biang Beauveria (5%)
        5. Inkubasi 25-28°C, 14-21 hari
        6. Panen: Warna putih penuh
        
        **Target**: 10⁸ conidia/ml
        """)
    
    st.markdown("### 💉 Aplikasi")
    st.markdown("""
    - **Dosis**: 2 ml/L air (10⁸ conidia/ml)
    - **Waktu**: Sore hari (hindari UV)
    - **Interval**: 7-10 hari
    - **Efektivitas**: 70-90% mortalitas (7-14 hari)
    """)

# ===== TAB 6: Metarhizium =====
with tab6:
    st.header("🦗 Metarhizium anisopliae (Green Muscardine)")
    st.info("Jamur patogen untuk hama tanah")
    
    st.markdown("### 🎯 Target Hama Tanah")
    st.markdown("""
    - White grub (uret)
    - Termite (rayap)
    - Nematoda
    - Soil-dwelling beetles
    """)
    
    st.markdown("### 🌟 Keunggulan")
    st.success("""
    - Persistensi di tanah lebih lama (6-12 bulan)
    - Toleran UV dan suhu tinggi
    - Dapat tumbuh sebagai endofit (kolonisasi internal tanaman)
    - Dual action: Biocontrol + Plant growth promotion
    """)
    
    st.markdown("### 📋 Produksi (Similar to Beauveria)")
    st.markdown("""
    **Substrate**: Rice/corn-based
    **Inkubasi**: 14-21 hari, 25-28°C
    **Indikator**: Warna hijau (green muscardine)
    **Target**: 10⁸ conidia/ml
    
    **Formulasi:**
    - WP (Wettable Powder): Untuk spray
    - SC (Suspension Concentrate): Untuk soil drench
    - Granular: Untuk aplikasi tanah
    """)

# ===== TAB 7: N-Fixers =====
with tab7:
    st.header("🌾 Nitrogen Fixers (Penambat Nitrogen)")
    st.info("Mikroba yang mengubah N₂ atmosfer menjadi NH₃ (tersedia tanaman)")
    
    nfixer_data = {
        'Spesies': [
            'Azotobacter chroococcum',
            'Azospirillum brasilense',
            'Rhizobium leguminosarum',
            'Frankia sp.'
        ],
        'Tipe': [
            'Free-living (non-simbiosis)',
            'Associative (rhizosphere)',
            'Symbiotic (legum)',
            'Symbiotic (non-legum)'
        ],
        'Kapasitas N-Fixation': [
            '20-40 kg N/ha/tahun',
            '15-30 kg N/ha/tahun',
            '100-300 kg N/ha/tahun',
            '50-150 kg N/ha/tahun'
        ],
        'Target Tanaman': [
            'Padi, jagung, sayuran',
            'Padi, jagung, gandum',
            'Kedelai, kacang tanah, kacang hijau',
            'Casuarina, Alnus (pionir)'
        ],
        'Manfaat Tambahan': [
            'Produksi vitamin B',
            'Produksi IAA (25% ↑ akar)',
            'Nodul akar (bakteroid)',
            'Tanaman pionir (reklamasi)'
        ]
    }
    
    df_nfixer = pd.DataFrame(nfixer_data)
    st.dataframe(df_nfixer, use_container_width=True, hide_index=True)
    
    st.markdown("### ⚙️ Mekanisme Fiksasi N₂")
    st.markdown("""
    **Enzim Nitrogenase (Fe-Mo protein):**
    ```
    N₂ + 8H⁺ + 8e⁻ + 16 ATP → 2NH₃ + H₂ + 16 ADP + 16 Pi
    ```
    
    **Kondisi Optimal:**
    - Suhu: 25-30°C
    - pH: 6.0-7.5
    - Anaerobic (nitrogenase sensitif O₂)
    - Energi tinggi (16 ATP per N₂)
    """)

# ===== TAB 8: Quality Control =====
with tab_qc:
    st.header("🔬 Quality Control Laboratory")
    
    qc_tab1, qc_tab2, qc_tab3 = st.tabs([
        "CFU Counting", "Contamination Check", "Shelf Life Test"
    ])
    
    with qc_tab1:
        st.subheader("🧮 CFU (Colony Forming Unit) Calculator")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            dilution = st.selectbox("Dilution Factor", [10**i for i in range(1, 10)], index=6)
        with col2:
            colony_count = st.number_input("Colony Count", 1, 300, 50)
        with col3:
            plating_vol = st.number_input("Plating Volume (ml)", 0.01, 1.0, 0.1)
        
        if st.button("Calculate CFU"):
            cfu = service.calculate_cfu(dilution, colony_count, plating_vol)
            
            st.success(f"**CFU/ml**: {cfu:.2e}")
            
            # Quality assessment
            if cfu >= 1e8:
                st.success("✅ **Excellent Quality** (≥10⁸ CFU/ml)")
            elif cfu >= 1e7:
                st.info("✓ **Good Quality** (10⁷ - 10⁸ CFU/ml)")
            elif cfu >= 1e6:
                st.warning("⚠️ **Acceptable** (10⁶ - 10⁷ CFU/ml)")
            else:
                st.error("❌ **Below Standard** (<10⁶ CFU/ml)")
        
        st.markdown("---")
        st.markdown("### 📋 Serial Dilution Protocol")
        st.markdown("""
        1. Ambil 1 ml sampel + 9 ml air steril (10⁻¹)
        2. Vortex 30 detik
        3. Ambil 1 ml dari 10⁻¹ + 9 ml air steril (10⁻²)
        4. Ulangi hingga 10⁻⁹
        5. Plating: 0.1 ml pada Nutrient Agar
        6. Inkubasi: 28°C, 24-48 jam
        7. Hitung koloni (30-300 koloni = valid)
        """)
    
    with qc_tab2:
        st.subheader("🔍 Contamination Identification")
        
        contam_data = {
            'Kontaminan': [
                'Aspergillus (Black mold)',
                'Penicillium (Blue-green)',
                'Rhizopus (Gray mold)',
                'Bacteria (Slimy)',
                'Yeast (Shiny colonies)'
            ],
            'Warna': [
                'Hitam',
                'Biru-hijau',
                'Abu-abu',
                'Putih/kuning (lendir)',
                'Krem/putih (mengkilap)'
            ],
            'Bau': [
                'Apek/musty',
                'Asam/fermentasi',
                'Busuk',
                'Asam tajam',
                'Ragi/tape'
            ],
            'Tindakan': [
                'Discard, sterilisasi ulang',
                'Discard, cek pH',
                'Discard, cek kelembaban',
                'Discard, cek suhu',
                'Acceptable (jika MOL)'
            ]
        }
        
        df_contam = pd.DataFrame(contam_data)
        st.dataframe(df_contam, use_container_width=True, hide_index=True)
    
    with qc_tab3:
        st.subheader("📅 Shelf Life Testing")
        
        st.markdown("""
        **Standard Shelf Life:**
        - Liquid formulation: 3-6 bulan (4°C)
        - Powder formulation: 12 bulan (cool, dry)
        - Carrier-based: 12 bulan (room temp)
        
        **Accelerated Aging Test:**
        1. Store at 37°C for 14 days
        2. Test CFU every 7 days
        3. Acceptable: <1 log reduction
        4. Extrapolate to room temp shelf life
        
        **Storage Conditions:**
        - Temperature: 4-25°C
        - Humidity: <60% RH
        - Light: Dark (avoid UV)
        - Container: Airtight, opaque
        """)

# ===== TAB 9: Business Calculator =====
with tab_calc:
    st.header("💰 Business Calculator")
    
    calc_tab1, calc_tab2, calc_tab3 = st.tabs([
        "Production Cost", "ROI Analysis", "Market Size"
    ])
    
    with calc_tab1:
        st.subheader("💵 Production Cost Analysis")
        st.info("📝 **Customize harga sesuai kondisi pasar lokal Anda**")
        
        # Product selection with categories
        st.markdown("#### 🎯 Pilih Produk")
        
        product_categories = {
            "🐮 ROTAN & POC": [
                "ROTAN_Bioactivator",
                "POC_ROTAN_Premium",
                "POC_Rumen_Kambing",
                "POC_Urine_Kelinci"
            ],
            "🦠 MOL (Mikro Organisme Lokal)": [
                "MOL_Sayuran",
                "MOL_Buah",
                "MOL_Rebung_Bambu",
                "MOL_Bonggol_Pisang",
                "MOL_Keong_Mas"
            ],
            "🍄 Biocontrol Fungi": [
                "Trichoderma",
                "Beauveria_bassiana",
                "Metarhizium_anisopliae"
            ],
            "🌱 PGPR & N-Fixers": [
                "PGPR_Liquid",
                "PGPR_Carrier",
                "Azotobacter"
            ]
        }
        
        # Flatten for selectbox
        all_products = []
        product_labels = {}
        for category, products in product_categories.items():
            for product in products:
                label = f"{category} → {product.replace('_', ' ')}"
                all_products.append(product)
                product_labels[label] = product
        
        selected_label = st.selectbox(
            "Pilih Produk",
            list(product_labels.keys()),
            label_visibility="collapsed"
        )
        product_type = product_labels[selected_label]
        
        # Get base data
        product_data = service.COST_DATABASE[product_type]
        
        st.markdown("---")
        st.markdown("### 🧾 Rincian Bahan Baku (Editable)")
        st.caption(f"**Output per batch**: {product_data['output_volume']} L/kg | **Fermentasi**: {product_data['fermentation_days']} hari")
        
        # Create editable material list
        materials_custom = {}
        total_material_cost_per_batch = 0
        
        st.markdown("#### 📦 Bahan-bahan:")
        
        # Display materials in a table format with editable prices
        for material, data in product_data['raw_materials'].items():
            col1, col2, col3, col4 = st.columns([3, 1, 2, 2])
            
            with col1:
                st.write(f"**{material}**")
            with col2:
                qty = st.number_input(
                    f"Qty",
                    value=float(data['qty']),
                    min_value=0.0,
                    step=0.1,
                    key=f"qty_{material}_{product_type}",
                    label_visibility="collapsed"
                )
            with col3:
                st.write(f"{data['unit']}")
            with col4:
                price = st.number_input(
                    f"Harga (Rp)",
                    value=data['price'],
                    min_value=0,
                    step=1000,
                    key=f"price_{material}_{product_type}",
                    label_visibility="collapsed"
                )
            
            material_total = qty * price
            total_material_cost_per_batch += material_total
            materials_custom[material] = {
                'qty': qty,
                'unit': data['unit'],
                'price': price,
                'total': material_total
            }
        
        st.markdown("---")
        st.markdown("### 💰 Biaya Produksi Lainnya (Editable)")
        
        col_other1, col_other2 = st.columns(2)
        
        with col_other1:
            labor_cost_per_batch = st.number_input(
                "💼 Biaya Tenaga Kerja per Batch (Rp)",
                value=50000,
                min_value=0,
                step=5000,
                help="Biaya untuk 1 batch produksi"
            )
            
            utilities_per_batch = st.number_input(
                "⚡ Utilities per Batch (Rp)",
                value=25000,
                min_value=0,
                step=5000,
                help="Listrik, air, gas untuk 1 batch"
            )
        
        with col_other2:
            packaging_per_liter = st.number_input(
                "📦 Packaging per Liter (Rp)",
                value=2000,
                min_value=0,
                step=500,
                help="Botol, label, box per liter"
            )
            
            overhead_percent = st.number_input(
                "🏢 Overhead (%)",
                value=10.0,
                min_value=0.0,
                max_value=50.0,
                step=1.0,
                help="Sewa, administrasi, dll"
            )
        
        st.markdown("---")
        st.markdown("### 📊 Kalkulator Volume Produksi")
        
        col_vol1, col_vol2 = st.columns(2)
        with col_vol1:
            target_volume = st.number_input(
                "Target Volume Produksi (Liter/Kg)",
                min_value=10,
                max_value=100000,
                value=100,
                step=10
            )
        with col_vol2:
            num_batches = target_volume / product_data['output_volume']
            st.metric("Jumlah Batch Diperlukan", f"{num_batches:.1f}")
        
        if st.button("🧮 Hitung Total Biaya Produksi", type="primary"):
            # Calculate total costs
            total_material_cost = total_material_cost_per_batch * num_batches
            total_labor = labor_cost_per_batch * num_batches
            total_utilities = utilities_per_batch * num_batches
            total_packaging = packaging_per_liter * target_volume
            
            subtotal = total_material_cost + total_labor + total_utilities + total_packaging
            overhead_cost = subtotal * (overhead_percent / 100)
            grand_total = subtotal + overhead_cost
            
            cost_per_unit = grand_total / target_volume
            
            # Display results
            st.success("✅ **Hasil Perhitungan**")
            
            # Summary metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            with col_m1:
                st.metric("Total Biaya", f"Rp {grand_total:,.0f}")
            with col_m2:
                st.metric("Biaya per Liter", f"Rp {cost_per_unit:,.0f}")
            with col_m3:
                st.metric("Volume Produksi", f"{target_volume} L")
            with col_m4:
                st.metric("Jumlah Batch", f"{num_batches:.1f}")
            
            st.markdown("---")
            
            # Detailed breakdown table
            st.markdown("### 📋 Rincian Biaya Detail")
            
            breakdown_data = {
                'Kategori': [
                    '🥦 Bahan Baku',
                    '💼 Tenaga Kerja',
                    '⚡ Utilities',
                    '📦 Packaging',
                    '🏢 Overhead',
                    '**TOTAL**'
                ],
                'Biaya (Rp)': [
                    f"Rp {total_material_cost:,.0f}",
                    f"Rp {total_labor:,.0f}",
                    f"Rp {total_utilities:,.0f}",
                    f"Rp {total_packaging:,.0f}",
                    f"Rp {overhead_cost:,.0f}",
                    f"**Rp {grand_total:,.0f}**"
                ],
                'Persentase': [
                    f"{(total_material_cost/grand_total*100):.1f}%",
                    f"{(total_labor/grand_total*100):.1f}%",
                    f"{(total_utilities/grand_total*100):.1f}%",
                    f"{(total_packaging/grand_total*100):.1f}%",
                    f"{(overhead_cost/grand_total*100):.1f}%",
                    "100%"
                ]
            }
            
            df_breakdown = pd.DataFrame(breakdown_data)
            st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            
            # Material details table
            with st.expander("📦 Detail Bahan Baku per Komponen"):
                material_details = {
                    'Bahan': [],
                    'Qty': [],
                    'Unit': [],
                    'Harga Satuan': [],
                    'Total per Batch': [],
                    'Total Produksi': []
                }
                
                for material, data in materials_custom.items():
                    material_details['Bahan'].append(material)
                    material_details['Qty'].append(f"{data['qty']:.2f}")
                    material_details['Unit'].append(data['unit'])
                    material_details['Harga Satuan'].append(f"Rp {data['price']:,.0f}")
                    material_details['Total per Batch'].append(f"Rp {data['total']:,.0f}")
                    material_details['Total Produksi'].append(f"Rp {data['total'] * num_batches:,.0f}")
                
                df_materials = pd.DataFrame(material_details)
                st.dataframe(df_materials, use_container_width=True, hide_index=True)
            
            # Visualization
            st.markdown("---")
            st.markdown("### 📊 Visualisasi Breakdown Biaya")
            
            col_chart1, col_chart2 = st.columns(2)
            
            with col_chart1:
                # Pie chart
                pie_data = {
                    'Category': ['Bahan Baku', 'Tenaga Kerja', 'Utilities', 'Packaging', 'Overhead'],
                    'Cost': [
                        total_material_cost,
                        total_labor,
                        total_utilities,
                        total_packaging,
                        overhead_cost
                    ]
                }
                
                fig_pie = px.pie(
                    pie_data,
                    values='Cost',
                    names='Category',
                    title='Proporsi Biaya',
                    color_discrete_sequence=px.colors.sequential.RdBu
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_chart2:
                # Bar chart
                fig_bar = px.bar(
                    pie_data,
                    x='Category',
                    y='Cost',
                    title='Breakdown Biaya per Kategori',
                    labels={'Cost': 'Biaya (Rp)', 'Category': 'Kategori'},
                    color='Cost',
                    color_continuous_scale='Blues'
                )
                fig_bar.update_layout(showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
            
            # Pricing recommendation
            st.markdown("---")
            st.markdown("### 💡 Rekomendasi Harga Jual")
            
            col_price1, col_price2, col_price3 = st.columns(3)
            
            with col_price1:
                st.info("**Margin 30%**")
                selling_price_30 = cost_per_unit * 1.3
                st.metric("Harga Jual", f"Rp {selling_price_30:,.0f}/L")
                st.caption("Untuk pasar kompetitif")
            
            with col_price2:
                st.success("**Margin 50%**")
                selling_price_50 = cost_per_unit * 1.5
                st.metric("Harga Jual", f"Rp {selling_price_50:,.0f}/L")
                st.caption("Standar industri")
            
            with col_price3:
                st.warning("**Margin 100%**")
                selling_price_100 = cost_per_unit * 2.0
                st.metric("Harga Jual", f"Rp {selling_price_100:,.0f}/L")
                st.caption("Premium/Retail")

    
    with calc_tab2:
        st.subheader("📊 ROI Analysis")
        
        scale = st.selectbox("Business Scale", ["Small", "Medium", "Large"])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            monthly_prod = st.number_input("Monthly Production (L)", 100, 50000, 
                                          500 if scale=="Small" else 3000 if scale=="Medium" else 15000)
        with col2:
            price_per_liter = st.number_input("Selling Price (Rp/L)", 10000, 200000, 40000)
        with col3:
            cost_per_liter = st.number_input("Production Cost (Rp/L)", 5000, 100000, 15000)
        
        investment = service.EQUIPMENT_COST[scale]['Total']
        
        if st.button("Calculate ROI"):
            roi_result = service.calculate_roi(
                investment, monthly_prod, price_per_liter, cost_per_liter
            )
            
            st.success(f"**Investment Required**: Rp {investment:,.0f}")
            
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            with col_r1:
                st.metric("Monthly Revenue", f"Rp {roi_result['monthly_revenue']:,.0f}")
            with col_r2:
                st.metric("Monthly Profit", f"Rp {roi_result['monthly_profit']:,.0f}")
            with col_r3:
                st.metric("ROI", f"{roi_result['roi_percent']:.1f}%")
            with col_r4:
                st.metric("Payback Period", f"{roi_result['payback_period_years']:.1f} years")
            
            # Projection chart
            months = list(range(1, 25))
            cumulative_profit = [roi_result['monthly_profit'] * m for m in months]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=months, y=cumulative_profit, 
                                    mode='lines+markers', name='Cumulative Profit'))
            fig.add_hline(y=investment, line_dash="dash", line_color="red", 
                         annotation_text="Break-even")
            fig.update_layout(title="Profit Projection (24 Months)",
                            xaxis_title="Month", yaxis_title="Cumulative Profit (Rp)")
            st.plotly_chart(fig, use_container_width=True)
    
    with calc_tab3:
        st.subheader("📈 Market Size Estimation")
        
        st.markdown("""
        ### 🎯 Target Market Segments
        
        **1. Organic Farmers** (30% market)
        - Price sensitivity: Medium
        - Volume: High
        - Preferred: ROTAN, MOL, Trichoderma
        
        **2. Conventional Farmers** (50% market)
        - Price sensitivity: High
        - Volume: Very high
        - Preferred: PGPR, N-Fixers (cost reduction)
        
        **3. Home Gardeners** (15% market)
        - Price sensitivity: Low
        - Volume: Low
        - Preferred: Ready-to-use liquid
        
        **4. Commercial Greenhouses** (5% market)
        - Price sensitivity: Low
        - Volume: Medium
        - Preferred: Trichoderma, Beauveria (IPM)
        
        ### 💰 Pricing Strategy
        
        | Segment | Product | Price Range |
        |---------|---------|-------------|
        | B2B (Farmer groups) | Bulk (20L+) | Rp 25,000 - 50,000/L |
        | B2C (Retail) | Bottle (1L) | Rp 50,000 - 100,000/L |
        | Premium (Certified) | Organic certified | Rp 100,000 - 200,000/L |
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p><strong>🦠 Mikroba & Biofertilizer Production Center</strong></p>
    <p>Standar: SNI 7763:2018 | ISO 17025 | Organic Certified</p>
    <p><small>Referensi: 50+ peer-reviewed scientific journals</small></p>
</div>
""", unsafe_allow_html=True)
