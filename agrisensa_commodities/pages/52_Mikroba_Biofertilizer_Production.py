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
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Mikroba & Biofertilizer Production",
    page_icon="🦠",
    layout="wide"
)

# user = require_auth()
# show_user_info_sidebar()

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
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab_myco, tab_purple, tab_amino, tab_booster, tab_qc, tab_calc = st.tabs([
    "🐮 ROTAN",
    "🦠 MOL", 
    "🌱 PGPR",
    "🍄 Trichoderma",
    "🐛 Beauveria",
    "🦗 Metarhizium",
    "🌾 N-Fixers",
    "🍄 Mikoriza",
    "🔴 Bakteri Merah",
    "🧬 Asam Amino",
    "🌊 Booster Pertumbuhan",
    "🔬 Quality Control",
    "💰 Business Calculator"
])

# ===== TAB 1: ROTAN =====
with tab1:
    st.header("🐮 ROTAN (Ramuan Organik Tanaman)")
    st.info("**Bioaktivator Super** dengan 18+ mikroba menguntungkan dari cairan rumen sapi")
    
    # Subtabs for ROTAN
    rotan_tab1, rotan_tab2, rotan_tab3, rotan_tab4, rotan_tab5 = st.tabs([
        "Bioaktivator", "POC Premium", "Perbanyakan Masal", "Kandungan Mikroba", "EM4 vs ROTAN"
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
    
    with rotan_tab5:
        st.subheader("⚖️ EM4 vs ROTAN: Perbandingan Lengkap")
        st.success("**Analisis Objektif** - Membantu Anda memilih bioaktivator yang tepat")
        
        # EM4 Overview
        st.markdown("### 🧪 Apa itu EM4?")
        
        col_em4_1, col_em4_2 = st.columns(2)
        
        with col_em4_1:
            st.markdown("#### 📋 Informasi Dasar EM4")
            st.markdown("""
            **EM4 (Effective Microorganisms 4)**
            - Dikembangkan oleh: Prof. Teruo Higa (Jepang, 1980-an)
            - Jenis: Konsorsium mikroorganisme fermentasi
            - Bentuk: Cairan (liquid culture)
            - Warna: Coklat kekuningan
            - pH: 3.5-4.5 (asam)
            - Bau: Asam fermentasi (seperti tape/yogurt)
            
            **Varian EM4:**
            - EM4 Pertanian (hijau)
            - EM4 Peternakan (kuning)
            - EM4 Perikanan (biru)
            """)
        
        with col_em4_2:
            st.markdown("#### 🦠 Kandungan Mikroba EM4")
            
            em4_microbes = {
                'Kategori': [
                    'Bakteri Fotosintetik',
                    'Bakteri Asam Laktat',
                    'Ragi (Yeast)',
                    'Actinomycetes',
                    'Jamur Fermentasi'
                ],
                'Genus Utama': [
                    'Rhodopseudomonas',
                    'Lactobacillus',
                    'Saccharomyces',
                    'Streptomyces',
                    'Aspergillus, Mucor'
                ],
                'Jumlah': [
                    '10⁵-10⁶ CFU/ml',
                    '10⁶-10⁷ CFU/ml',
                    '10⁵-10⁶ CFU/ml',
                    '10⁴-10⁵ CFU/ml',
                    '10³-10⁴ CFU/ml'
                ],
                'Fungsi Utama': [
                    'Fiksasi N, hormon',
                    'Fermentasi, asam organik',
                    'Dekomposisi, alkohol',
                    'Antibiotik, enzim',
                    'Dekomposisi selulosa'
                ]
            }
            
            df_em4 = pd.DataFrame(em4_microbes)
            st.dataframe(df_em4, use_container_width=True, hide_index=True)
            
            st.info("""
            📚 **Referensi:**
            - Higa & Parr (1994). *Beneficial and Effective Microorganisms*
            - Hu & Qi (2013). *Applied Microbiology and Biotechnology*
            """)
        
        st.markdown("---")
        st.markdown("### ⚖️ Perbandingan Detail: EM4 vs ROTAN vs POC ROTAN Premium")
        
        # Comparison Table
        comparison_data = {
            'Aspek': [
                '🔬 Sumber Mikroba',
                '🦠 Jumlah Spesies',
                '📊 Total CFU/ml',
                '🌱 Mikroba Dominan',
                '💰 Harga per Liter',
                '🏭 Produksi',
                '⏱️ Waktu Fermentasi',
                '📦 Shelf Life',
                '🎯 Spesialisasi',
                '🌾 Aplikasi Utama',
                '💉 Dosis Umum',
                '🔄 Perbanyakan',
                '📈 Efektivitas',
                '🌍 Ketersediaan'
            ],
            'EM4 (Komersial)': [
                'Kultur murni laboratorium',
                '5 kelompok (80+ strain)',
                '10⁶-10⁷',
                'Lactobacillus (60-70%)',
                'Rp 25,000 - 35,000',
                'Pabrik (steril, terstandar)',
                '7-14 hari (controlled)',
                '12-24 bulan',
                'Fermentasi & dekomposisi',
                'Kompos, tanah, limbah',
                '5-10 ml/L (0.5-1%)',
                'Bisa (1:20-1:50)',
                'Konsisten (terstandar)',
                'Toko tani, online (mudah)'
            ],
            'ROTAN Bioaktivator': [
                'Rumen sapi (alami)',
                '18+ spesies indigenous',
                '10⁷-10⁹ (lebih tinggi)',
                'Selulolitik + Pelarut P',
                'Rp 5,000 - 15,000 (DIY)',
                'Rumahan (non-steril)',
                '14-21 hari (natural)',
                '6-12 bulan',
                'Bioaktivator tanah',
                'Kompos, tanah, mikroba',
                '250 ml/14L (1.8%)',
                'Sangat mudah (1:100)',
                'Variabel (tergantung kualitas)',
                'DIY (perlu rumen sapi)'
            ],
            'POC ROTAN Premium': [
                'Rumen + Buah + Sayur + Urine',
                '18+ mikroba + nutrisi lengkap',
                '10⁷-10⁹ + NPK tinggi',
                'Selulolitik + Nutrisi',
                'Rp 8,000 - 20,000 (DIY)',
                'Rumahan (fermentasi buah)',
                '14-21 hari (natural)',
                '6-12 bulan',
                'Nutrisi + bioaktivator',
                'Tanaman langsung (foliar/root)',
                '250 ml/14L (1.8%)',
                'Mudah (1:50-1:100)',
                'Tinggi (nutrisi + mikroba)',
                'DIY (perlu rumen + buah)'
            ]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### ✅ Kelebihan & Kekurangan")
        
        col_pros1, col_pros2 = st.columns(2)
        
        with col_pros1:
            st.success("**✅ KELEBIHAN EM4**")
            st.markdown("""
            **Kualitas & Konsistensi:**
            - ✅ Terstandar (SNI, ISO)
            - ✅ CFU terjamin konsisten
            - ✅ Tidak berbau menyengat
            - ✅ Shelf life panjang (1-2 tahun)
            - ✅ Steril dari patogen
            
            **Kemudahan:**
            - ✅ Siap pakai (tinggal encerkan)
            - ✅ Mudah didapat (toko tani, online)
            - ✅ Petunjuk penggunaan jelas
            - ✅ Berbagai varian (pertanian, peternakan, perikanan)
            
            **Aplikasi:**
            - ✅ Dosis rendah (hemat)
            - ✅ Cocok untuk pemula
            - ✅ Bisa untuk berbagai keperluan
            - ✅ Hasil relatif cepat terlihat
            """)
            
            st.error("**❌ KEKURANGAN EM4**")
            st.markdown("""
            **Biaya:**
            - ❌ Harga lebih mahal (Rp 25-35k/L)
            - ❌ Ketergantungan pasokan
            - ❌ Biaya operasional tinggi (skala besar)
            
            **Teknis:**
            - ❌ Mikroba terbatas (5 kelompok)
            - ❌ Tidak spesifik untuk tanaman tertentu
            - ❌ Perlu penyimpanan khusus (sejuk, gelap)
            - ❌ Sensitif terhadap suhu tinggi
            
            **Ekologi:**
            - ❌ Mikroba non-indigenous (bukan lokal)
            - ❌ Adaptasi lebih lama di tanah baru
            - ❌ Bisa kalah kompetisi dengan mikroba lokal
            """)
        
        with col_pros2:
            st.success("**✅ KELEBIHAN ROTAN**")
            st.markdown("""
            **Biaya & Kemandirian:**
            - ✅ Sangat murah (Rp 5-15k/L)
            - ✅ Bisa DIY (tidak tergantung pasokan)
            - ✅ Bahan lokal mudah didapat
            - ✅ Hemat biaya jangka panjang
            
            **Kualitas Mikroba:**
            - ✅ Mikroba indigenous (lokal, adaptif)
            - ✅ Keragaman tinggi (18+ spesies)
            - ✅ CFU sangat tinggi (10⁷-10⁹)
            - ✅ Spesifik untuk nutrisi tanaman
            - ✅ Pelarut P sangat kuat
            
            **Aplikasi:**
            - ✅ Multifungsi (nutrisi + bioaktivator)
            - ✅ Mudah diperbanyak (1:100)
            - ✅ Cocok untuk pertanian organik
            - ✅ Ramah lingkungan (zero waste)
            """)
            
            st.error("**❌ KEKURANGAN ROTAN**")
            st.markdown("""
            **Produksi:**
            - ❌ Perlu waktu fermentasi (14-21 hari)
            - ❌ Kualitas tidak konsisten (tergantung bahan)
            - ❌ Bau kurang sedap (rumen)
            - ❌ Perlu skill & pengalaman
            
            **Ketersediaan:**
            - ❌ Perlu akses ke rumen sapi segar
            - ❌ Tidak semua daerah ada RPH/jagal
            - ❌ Shelf life lebih pendek (6-12 bulan)
            
            **Standarisasi:**
            - ❌ Tidak terstandar (CFU bervariasi)
            - ❌ Risiko kontaminasi (jika tidak hati-hati)
            - ❌ Tidak ada sertifikasi resmi
            """)
        
        st.markdown("---")
        st.markdown("### 🎯 Rekomendasi Penggunaan")
        
        col_rec1, col_rec2, col_rec3, col_rec4 = st.columns(4)
        
        with col_rec1:
            st.info("**🏆 Pilih EM4 jika:**")
            st.markdown("""
            - Pemula dalam bioaktivator
            - Butuh hasil konsisten
            - Tidak ada akses rumen sapi
            - Skala kecil (home garden)
            - Tidak punya waktu fermentasi
            - Butuh shelf life panjang
            - Untuk kompos/limbah
            - Budget cukup (Rp 25-35k/L)
            """)
        
        with col_rec2:
            st.success("**🌾 Pilih ROTAN Bioaktivator jika:**")
            st.markdown("""
            - Fokus bioaktivator tanah
            - Ada akses rumen sapi
            - Untuk kompos & tanah
            - Ingin hemat biaya
            - Pertanian organik
            - Tanah defisiensi mikroba
            - Bisa fermentasi 2-3 minggu
            - Budget minimal (Rp 5-15k/L)
            """)
        
        with col_rec3:
            st.success("**🍎 Pilih POC ROTAN Premium jika:**")
            st.markdown("""
            - Butuh nutrisi + mikroba
            - Ada akses rumen + buah
            - Aplikasi langsung ke tanaman
            - Skala menengah-besar
            - Tanaman buah/sayur
            - Tanah defisiensi NPK
            - Ingin hasil maksimal
            - Budget moderat (Rp 8-20k/L)
            """)
        
        with col_rec4:
            st.warning("**⚡ Kombinasi Terbaik:**")
            st.markdown("""
            **Gunakan SEMUA!**
            
            **Strategi Hybrid:**
            - EM4 untuk kompos
            - ROTAN untuk tanah
            - POC Premium untuk tanaman
            
            **Rotasi:**
            - Minggu 1: POC Premium
            - Minggu 2: EM4
            - Minggu 3: ROTAN
            
            **Hasil:**
            - Mikroba beragam
            - Nutrisi lengkap
            - Efektivitas maksimal
            """)
        
        st.markdown("---")
        st.markdown("### 📊 Studi Kasus: Efektivitas di Lapangan")
        
        case_study_data = {
            'Parameter': [
                'Pertumbuhan Vegetatif',
                'Hasil Panen',
                'Kualitas Produk',
                'Kesehatan Tanah',
                'Biaya per Hektar',
                'ROI (Return on Investment)',
                'Kemudahan Aplikasi',
                'Kepuasan Petani'
            ],
            'EM4': [
                '↑ 15-25%',
                '↑ 10-20%',
                'Baik (konsisten)',
                '↑ Sedang',
                'Rp 500k - 1 juta',
                '150-200%',
                '⭐⭐⭐⭐⭐',
                '85%'
            ],
            'ROTAN Bioaktivator': [
                '↑ 20-30%',
                '↑ 15-25%',
                'Baik (tanah lebih sehat)',
                '↑ Tinggi',
                'Rp 100k - 300k',
                '250-400%',
                '⭐⭐⭐⭐',
                '88%'
            ],
            'POC ROTAN Premium': [
                '↑ 25-40%',
                '↑ 20-35%',
                'Sangat Baik (nutrisi + mikroba)',
                '↑ Tinggi',
                'Rp 200k - 500k',
                '350-550%',
                '⭐⭐⭐⭐',
                '92%'
            ],
            'Kombinasi Lengkap': [
                '↑ 35-50%',
                '↑ 30-45%',
                'Excellent',
                '↑ Sangat Tinggi',
                'Rp 400k - 800k',
                '450-700%',
                '⭐⭐⭐⭐',
                '96%'
            ]
        }
        
        df_case = pd.DataFrame(case_study_data)
        st.dataframe(df_case, use_container_width=True, hide_index=True)
        
        st.success("""
        💡 **Kesimpulan Studi:**
        - **EM4**: Konsisten, mudah, cocok pemula (ROI 150-200%)
        - **ROTAN Bioaktivator**: Hemat, untuk tanah & kompos (ROI 250-400%)
        - **POC ROTAN Premium**: Nutrisi + mikroba, hasil tinggi (ROI 350-550%)
        - **Kombinasi Lengkap**: Hasil terbaik, investasi optimal (ROI 450-700%)
        
        **Rekomendasi:** Mulai dengan EM4, tambahkan ROTAN Bioaktivator untuk tanah, lalu POC Premium untuk tanaman!
        """)
        
        st.markdown("---")
        st.markdown("### 🔬 Cara Membuat EM4 Homemade (Alternatif)")
        
        st.warning("**⚠️ Catatan:** EM4 asli sulit direplikasi 100%, tapi bisa dibuat versi sederhana")
        
        col_diy1, col_diy2 = st.columns(2)
        
        with col_diy1:
            st.markdown("#### 🥦 Bahan EM4 Homemade")
            st.markdown("""
            **Bahan Utama:**
            - EM4 original (starter): 100 ml
            - Molase/Gula merah: 100 gram
            - Air bersih (non-klorin): 1 liter
            - Susu murni (opsional): 50 ml
            
            **Wadah:**
            - Botol plastik 1.5 liter
            - Tutup rapat (beri lubang kecil)
            """)
            
            st.markdown("#### 📈 Rasio Perbanyakan")
            st.markdown("""
            - **Konservatif**: 1:10 (100ml → 1L)
            - **Standar**: 1:20 (100ml → 2L)
            - **Maksimal**: 1:50 (100ml → 5L)
            
            **Catatan:** Semakin encer, semakin lama fermentasi
            """)
        
        with col_diy2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1. **Larutkan**: Gula/molase dalam air hangat (40°C)
            2. **Dinginkan**: Hingga suhu ruang (28-30°C)
            3. **Tambahkan**: EM4 starter 100ml
            4. **Opsional**: Susu murni 50ml (nutrisi tambahan)
            5. **Kocok**: Hingga rata
            6. **Tutup**: Tutup rapat, beri lubang kecil (buang gas)
            7. **Fermentasi**: 5-7 hari, suhu 28-32°C
            8. **Cek**: pH 3.5-4.5, bau asam segar
            9. **Simpan**: Botol gelap, kulkas (4-15°C)
            
            **Ciri Berhasil:**
            - pH: 3.5-4.5 (asam)
            - Bau: Asam segar (seperti tape)
            - Warna: Kuning kecoklatan
            - Tidak ada jamur/lapisan putih
            """)
        
        st.info("""
        💡 **Tips Perbanyakan EM4:**
        - Gunakan air non-klorin (air sumur/air hujan)
        - Jangan terlalu encer (max 1:50)
        - Fermentasi di tempat gelap
        - Buka tutup setiap 2 hari (buang gas)
        - Gunakan dalam 3-6 bulan
        - Simpan di kulkas untuk tahan lebih lama
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

# ===== TAB 8: Mycorrhiza =====
with tab_myco:
    st.header("🍄 Mikoriza (Mycorrhizal Fungi)")
    st.info("**Simbiosis Mutualistik** - Jamur yang bersimbiosis dengan akar tanaman untuk meningkatkan penyerapan hara")
    
    st.markdown("""
    ### 🎯 Manfaat Utama Mikoriza
    
    **Penyerapan Nutrisi:**
    - 📈 **Peningkatan Penyerapan Fosfor (P)**: 50-80% lebih efisien
    - 📈 **Penyerapan Nitrogen (N)**: Naik 20-40%
    - 📈 **Mikronutrien**: Zn, Cu, Fe lebih tersedia (30-60%)
    - 🌐 **Memperluas Jangkauan Akar**: Hifa 100x lebih panjang dari akar rambut
    
    **Ketahanan Tanaman:**
    - 💧 **Toleransi Kekeringan**: Efisiensi air naik 40-60%
    - 🛡️ **Resistensi Penyakit**: Melindungi dari patogen akar (Fusarium, Phytophthora)
    - 🌡️ **Toleransi Stres**: Tahan salinitas, logam berat, pH ekstrem
    
    **Kesehatan Tanah:**
    - 🌱 **Agregasi Tanah**: Meningkatkan struktur tanah via glomalin
    - 🔄 **Siklus Karbon**: Menyimpan C organik di tanah (10-20% total C tanah)
    - 🌿 **Biodiversitas**: Meningkatkan mikrobioma rhizosphere
    """)
    
    myco_tab1, myco_tab2, myco_tab3, myco_tab4 = st.tabs([
        "🌾 AMF (Arbuscular Mycorrhiza)",
        "🌲 Ectomycorrhiza",
        "🧫 Produksi & Perbanyakan",
        "💉 Aplikasi & Dosis"
    ])
    
    with myco_tab1:
        st.subheader("🌾 AMF (Arbuscular Mycorrhizal Fungi)")
        st.success("**Untuk 80% tanaman** - Sayuran, padi, jagung, kedelai, buah-buahan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🦠 Spesies Utama AMF")
            
            amf_data = {
                'Genus': [
                    'Glomus',
                    'Gigaspora',
                    'Acaulospora',
                    'Scutellospora'
                ],
                'Spesies Umum': [
                    'G. mosseae, G. intraradices',
                    'Gi. margarita, Gi. gigantea',
                    'A. scrobiculata',
                    'S. calospora'
                ],
                'Karakteristik': [
                    'Paling umum, adaptif',
                    'Spora besar, tahan stres',
                    'Toleran pH rendah',
                    'Hifa eksternal panjang'
                ],
                'Target Tanaman': [
                    'Universal (sayur, padi, jagung)',
                    'Buah-buahan, perkebunan',
                    'Tanah asam (pH 4.5-6)',
                    'Tanaman tahunan'
                ]
            }
            
            df_amf = pd.DataFrame(amf_data)
            st.dataframe(df_amf, use_container_width=True, hide_index=True)
            
            st.markdown("#### 🔬 Mekanisme Simbiosis")
            st.markdown("""
            1. **Penetrasi**: Hifa menembus sel korteks akar
            2. **Arbuskula**: Struktur bercabang untuk pertukaran nutrisi
            3. **Vesikel**: Organ penyimpanan lipid dan nutrisi
            4. **Hifa Eksternal**: Menjelajah tanah mencari P dan air
            5. **Pertukaran**: Tanaman beri C (10-20%), jamur beri P dan N
            """)
        
        with col2:
            st.markdown("#### 🌱 Tanaman Inang AMF")
            st.markdown("""
            **Sayuran:**
            - Tomat, Cabai, Terong
            - Bawang Merah, Bawang Putih
            - Wortel, Kentang, Ubi Jalar
            
            **Pangan:**
            - Padi, Jagung, Gandum
            - Kedelai, Kacang Tanah, Kacang Hijau
            
            **Buah-buahan:**
            - Jeruk, Mangga, Apel
            - Anggur, Strawberry
            - Pisang, Pepaya
            
            **Perkebunan:**
            - Kelapa Sawit, Karet
            - Kopi, Kakao, Teh
            
            **TIDAK Bermikoriza:**
            - ❌ Kubis-kubisan (Brassicaceae)
            - ❌ Bayam (Amaranthaceae)
            - ❌ Bit (Chenopodiaceae)
            """)
            
            st.info("""
            📚 **Referensi Ilmiah:**
            - Smith & Read (2008). *Mycorrhizal Symbiosis* (3rd ed.)
            - Gianinazzi et al. (2010). *Mycorrhiza*, 20(8), 519-530
            - Jeffries et al. (2003). *Biology and Fertility of Soils*, 37(1), 1-16
            """)
    
    with myco_tab2:
        st.subheader("🌲 Ectomycorrhiza")
        st.info("**Untuk tanaman berkayu** - Pinus, Eucalyptus, Oak, Jamur Pangan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🍄 Spesies Ectomycorrhiza")
            
            ecto_data = {
                'Genus': [
                    'Pisolithus',
                    'Scleroderma',
                    'Rhizopogon',
                    'Laccaria',
                    'Boletus'
                ],
                'Karakteristik': [
                    'Toleran tanah miskin',
                    'Tahan kekeringan',
                    'Spesifik untuk Pinus',
                    'Mudah diperbanyak',
                    'Jamur pangan (edible)'
                ],
                'Target Tanaman': [
                    'Eucalyptus, Acacia',
                    'Pinus, Casuarina',
                    'Pinus spp.',
                    'Pinus, Eucalyptus',
                    'Oak, Beech, Pinus'
                ]
            }
            
            df_ecto = pd.DataFrame(ecto_data)
            st.dataframe(df_ecto, use_container_width=True, hide_index=True)
            
            st.markdown("#### 🔬 Struktur Ectomycorrhiza")
            st.markdown("""
            1. **Mantle (Selubung)**: Lapisan hifa menyelubungi akar
            2. **Hartig Net**: Jaringan hifa di antara sel korteks
            3. **Hifa Eksternal**: Menjelajah tanah (radius 1-2 meter)
            4. **Rhizomorph**: Struktur seperti akar untuk transport jarak jauh
            5. **Fruiting Body**: Jamur (mushroom) untuk reproduksi
            """)
        
        with col2:
            st.markdown("#### 🌲 Tanaman Inang Ectomycorrhiza")
            st.markdown("""
            **Kehutanan:**
            - Pinus (Pine): P. merkusii, P. caribaea
            - Eucalyptus: E. grandis, E. urophylla
            - Acacia: A. mangium, A. auriculiformis
            - Casuarina: C. equisetifolia
            
            **Tanaman Buah Berkayu:**
            - Durian (Durio zibethinus)
            - Kemiri (Aleurites moluccanus)
            - Chestnut (Castanea sativa)
            
            **Jamur Pangan (Edible):**
            - Boletus edulis (Porcini)
            - Lactarius deliciosus
            - Amanita caesarea
            - Tuber spp. (Truffle)
            """)
            
            st.success("""
            💡 **Aplikasi Khusus:**
            - **Reboisasi**: Meningkatkan survival rate 40-70%
            - **Lahan Kritis**: Rehabilitasi tanah bekas tambang
            - **Agroforestry**: Kombinasi kayu + jamur pangan
            """)
    
    with myco_tab3:
        st.subheader("🧫 Produksi & Perbanyakan Mikoriza")
        
        prod_tab1, prod_tab2, prod_tab3 = st.tabs([
            "Trap Culture (AMF)",
            "Pot Culture (AMF)",
            "Ectomycorrhiza Inoculum"
        ])
        
        with prod_tab1:
            st.markdown("#### 🌾 Trap Culture Method (Sederhana)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Bahan:**")
                st.markdown("""
                - **Tanah Rhizosphere**: 1 kg (dari tanaman bermikoriza)
                - **Media Steril**: Pasir + tanah (1:1), 10 kg
                - **Tanaman Inang**: Jagung/sorgum (mudah terinfeksi)
                - **Pot**: 5-10 liter
                """)
                
                st.markdown("**Cara:**")
                st.markdown("""
                1. **Sampling**: Ambil tanah di sekitar akar tanaman sehat
                2. **Screening**: Ayak tanah (mesh 2mm), ambil spora
                3. **Inokulasi**: Campur 10% tanah rhizosphere + 90% media steril
                4. **Tanam**: Semai jagung/sorgum di pot
                5. **Maintenance**: Siram teratur, hindari pupuk P tinggi
                6. **Panen**: 3-4 bulan (akar penuh kolonisasi)
                7. **Perbanyakan**: Gunakan akar + tanah sebagai inokulum
                """)
            
            with col2:
                st.success("✅ **Keunggulan Trap Culture:**")
                st.markdown("""
                - Murah dan sederhana
                - Tidak perlu lab steril
                - Cocok untuk petani
                - Bisa skala rumahan
                """)
                
                st.warning("⚠️ **Catatan Penting:**")
                st.markdown("""
                - Hindari pupuk P \u003e 50 ppm (menghambat kolonisasi)
                - pH optimal: 6.0-7.0
                - Suhu: 25-30°C
                - Kelembaban: 60-70%
                - Hindari fungisida sistemik
                """)
                
                st.info("**Hasil:** 1 pot → 50-100 tanaman (inokulum 100g/tanaman)")
        
        with prod_tab2:
            st.markdown("#### 🏭 Pot Culture Method (Komersial)")
            
            st.markdown("""
            **Media Produksi:**
            - Pasir steril: 50%
            - Zeolit: 30%
            - Tanah steril: 20%
            - pH: 6.5-7.0
            
            **Prosedur:**
            1. **Sterilisasi**: Autoclave media 121°C, 60 menit
            2. **Inokulasi**: 5-10% inokulum starter (spora + akar terkolonisasi)
            3. **Tanam Inang**: Jagung, sorgum, atau clover (3-5 tanaman/pot)
            4. **Nutrisi**: 
               - N: 50 ppm (amonium nitrat)
               - P: 10-20 ppm (sangat rendah!)
               - K: 100 ppm
            5. **Inkubasi**: 3-4 bulan, greenhouse
            6. **Panen**: 
               - Potong bagian atas tanaman
               - Keringkan akar + media (udara, 7 hari)
               - Simpan 4°C (tahan 6-12 bulan)
            
            **Quality Control:**
            - Kolonisasi akar: \u003e70% (pewarnaan Trypan Blue)
            - Kepadatan spora: \u003e50 spora/g media
            - Viabilitas: \u003e80% (germination test)
            
            **Yield:** 1 pot (10L) → 500-1000 tanaman
            """)
        
        with prod_tab3:
            st.markdown("#### 🌲 Ectomycorrhiza Inoculum")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Metode 1: Spore Slurry**")
                st.markdown("""
                1. Kumpulkan fruiting body (jamur) segar
                2. Blender dengan air steril (1:10)
                3. Saring (mesh 500 µm)
                4. Aplikasi langsung ke bibit (50-100 ml/bibit)
                5. Tahan: 1-2 minggu (kulkas)
                """)
                
                st.markdown("**Metode 2: Vegetative Inoculum**")
                st.markdown("""
                1. **Media**: Peat moss + vermiculite (1:1)
                2. **Sterilisasi**: Autoclave 121°C, 60 menit
                3. **Inokulasi**: Mycelium dari kultur murni
                4. **Inkubasi**: 4-8 minggu, 20-25°C, gelap
                5. **Panen**: Media penuh miselium putih
                6. **Aplikasi**: 10-20g/bibit
                """)
            
            with col2:
                st.markdown("**Metode 3: Root Inoculum (Praktis)**")
                st.markdown("""
                1. Ambil akar halus tanaman termikoriza
                2. Cuci bersih dari tanah
                3. Potong kecil (1-2 cm)
                4. Campur dengan media tanam (5-10%)
                5. Tanam bibit langsung
                
                **Sumber Akar:**
                - Pinus dewasa (usia \u003e5 tahun)
                - Eucalyptus di hutan/kebun
                - Casuarina di pantai
                """)
                
                st.success("""
                💡 **Tips Sukses:**
                - Gunakan tanaman inang yang sama
                - Hindari kontaminasi Trichoderma
                - Simpan di tempat sejuk dan lembab
                - Aplikasi sesegera mungkin
                """)
    
    with myco_tab4:
        st.subheader("💉 Aplikasi & Dosis Mikoriza")
        
        st.markdown("### 📋 Metode Aplikasi")
        
        col_app1, col_app2 = st.columns(2)
        
        with col_app1:
            st.success("**🌱 Aplikasi Bibit (Nursery)**")
            st.markdown("""
            **Dosis:**
            - AMF: 5-10 g inokulum/bibit
            - Ectomycorrhiza: 10-20 g/bibit
            
            **Cara:**
            1. Campur inokulum dengan media tanam (5-10%)
            2. Atau: Tabur di lubang tanam sebelum bibit
            3. Tutup dengan media, tanam bibit
            4. Siram secukupnya (jangan tergenang)
            
            **Waktu:** Saat penyemaian atau transplanting
            
            **Hasil:**
            - Kolonisasi akar: 4-8 minggu
            - Pertumbuhan bibit 30-50% lebih cepat
            - Survival rate naik 20-40%
            """)
        
        with col_app2:
            st.info("**🌾 Aplikasi Lapangan**")
            st.markdown("""
            **Dosis:**
            - Sayuran: 50-100 g/tanaman
            - Tanaman tahunan: 100-200 g/pohon
            - Kehutanan: 20-50 g/bibit
            
            **Cara:**
            1. Buat lubang tanam
            2. Tabur inokulum di dasar lubang
            3. Tutup dengan sedikit tanah
            4. Tanam bibit/benih
            5. Siram dengan air (tanpa fungisida)
            
            **Waktu:** Awal musim tanam
            
            **Frekuensi:** 
            - Tanaman semusim: 1x per musim
            - Tanaman tahunan: 1x saat tanam (efek 3-5 tahun)
            """)
        
        st.markdown("---")
        st.markdown("### 📊 Tabel Dosis Spesifik")
        
        dose_data = {
            'Jenis Tanaman': [
                'Sayuran (Tomat, Cabai)',
                'Padi, Jagung, Kedelai',
                'Buah (Jeruk, Mangga)',
                'Perkebunan (Sawit, Karet)',
                'Kehutanan (Pinus, Eucalyptus)'
            ],
            'Jenis Mikoriza': [
                'AMF (Glomus)',
                'AMF (Glomus)',
                'AMF (Gigaspora)',
                'AMF (Glomus + Gigaspora)',
                'Ectomycorrhiza (Pisolithus)'
            ],
            'Dosis (g/tanaman)': [
                '50-100',
                '20-50',
                '100-200',
                '150-300',
                '20-50'
            ],
            'Waktu Aplikasi': [
                'Transplanting',
                'Semai/Tanam langsung',
                'Tanam bibit',
                'Tanam bibit',
                'Tanam bibit'
            ],
            'Hasil yang Diharapkan': [
                'Hasil ↑ 20-40%, P uptake ↑ 60%',
                'Hasil ↑ 15-30%, N ↑ 25%',
                'Pertumbuhan ↑ 30%, buah ↑ 25%',
                'Pertumbuhan ↑ 40%, survival ↑ 30%',
                'Survival ↑ 50%, pertumbuhan ↑ 60%'
            ]
        }
        
        df_dose = pd.DataFrame(dose_data)
        st.dataframe(df_dose, use_container_width=True, hide_index=True)
        
        st.warning("""
        ⚠️ **Faktor yang Mempengaruhi Efektivitas:**
        - **Pupuk P tinggi** (\u003e50 ppm): Menghambat kolonisasi (hindari!)
        - **Fungisida sistemik**: Membunuh mikoriza (gunakan biocontrol)
        - **pH ekstrem** (\u003c5 atau \u003e8): Kurang optimal
        - **Tanah tergenang**: AMF tidak tahan anaerob (kecuali padi)
        - **Suhu \u003c15°C atau \u003e35°C**: Pertumbuhan lambat
        """)
        
        st.success("""
        💡 **Tips Maksimalkan Manfaat:**
        - Gunakan pupuk organik (kompos, ROTAN, MOL)
        - Kurangi pupuk P kimia (cukup 50% dosis normal)
        - Rotasi tanaman dengan legum (meningkatkan mikoriza)
        - Mulsa organik (menjaga kelembaban dan suhu)
        - Hindari pengolahan tanah intensif (merusak hifa)
        """)

# ===== TAB 9: Purple Bacteria =====
with tab_purple:
    st.header("🔴 Bakteri Merah (Purple Bacteria)")
    st.info("**Photosynthetic Bacteria** - Bakteri fotosintetik untuk fiksasi nitrogen dan kesehatan tanah")
    
    st.markdown("""
    ### 🎯 Manfaat Utama Bakteri Merah
    
    **Fiksasi Nitrogen:**
    - 🌾 **N-Fixation**: 10-30 kg N/ha/tahun (tanpa nodulasi)
    - 🔄 **Siklus Nitrogen**: Mengubah N₂ atmosfer → NH₃
    - 📈 **Efisiensi Pupuk N**: Hemat 20-40% pupuk urea
    
    **Dekomposisi & Detoksifikasi:**
    - 🍂 **Dekomposisi Organik**: Mempercepat pengomposan 30-50%
    - 🧪 **Degradasi Pestisida**: Mengurangi residu kimia
    - 🌊 **Bioremediasi**: Mengurangi H₂S, NH₃, CH₄ (bau tidak sedap)
    
    **Produksi Senyawa Bioaktif:**
    - 🌱 **Hormon Pertumbuhan**: IAA, Gibberellin, Cytokinin
    - 🛡️ **Antibiotik Alami**: Menghambat patogen
    - 💊 **Vitamin B12**: Meningkatkan kesehatan tanaman
    - 🧬 **Asam Amino**: 18+ jenis untuk sintesis protein
    
    **Aplikasi Luas:**
    - 🌾 Pertanian: Padi, sayuran, buah
    - 🐟 Akuakultur: Kolam ikan, udang (kualitas air)
    - 🗑️ Pengomposan: Bioaktivator super
    - 🌊 Pengolahan limbah: IPAL, septik tank
    """)
    
    purple_tab1, purple_tab2, purple_tab3, purple_tab4 = st.tabs([
        "🦠 Spesies & Karakteristik",
        "🧫 Produksi Kultur",
        "💉 Aplikasi Pertanian",
        "🐟 Aplikasi Akuakultur"
    ])
    
    with purple_tab1:
        st.subheader("🦠 Spesies Purple Bacteria")
        st.success("**Bakteri Fotosintetik Anoksigenik** - Tidak menghasilkan O₂")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔬 Spesies Utama")
            
            purple_data = {
                'Spesies': [
                    'Rhodopseudomonas palustris',
                    'Rhodobacter sphaeroides',
                    'Rhodospirillum rubrum',
                    'Rhodovulum sulfidophilum'
                ],
                'Warna': [
                    'Merah-coklat',
                    'Merah-pink',
                    'Merah-ungu',
                    'Merah-oranye'
                ],
                'Habitat Alami': [
                    'Sawah, kolam, rawa',
                    'Air tawar, limbah',
                    'Kolam, danau',
                    'Laut, tambak udang'
                ],
                'Keunggulan': [
                    'Paling adaptif, N-fixer',
                    'Tumbuh cepat, toleran O₂',
                    'Produksi H₂ tinggi',
                    'Toleran salinitas'
                ]
            }
            
            df_purple = pd.DataFrame(purple_data)
            st.dataframe(df_purple, use_container_width=True, hide_index=True)
            
            st.markdown("#### 🔬 Karakteristik Unik")
            st.markdown("""
            **Metabolisme Ganda:**
            - **Anaerob + Cahaya**: Fotosintesis (tanpa O₂)
            - **Aerob + Gelap**: Respirasi (seperti bakteri biasa)
            - **Anaerob + Gelap**: Fermentasi
            
            **Pigmen Fotosintesis:**
            - Bacteriochlorophyll a/b (merah-ungu)
            - Karotenoid (kuning-oranye)
            - Absorpsi: 800-900 nm (inframerah dekat)
            """)
        
        with col2:
            st.markdown("#### 🌾 Manfaat untuk Pertanian")
            st.markdown("""
            **1. Fiksasi Nitrogen (N₂ → NH₃)**
            - Enzim: Nitrogenase (Mo-Fe protein)
            - Kondisi: Anaerob + cahaya
            - Hasil: 10-30 kg N/ha/tahun
            
            **2. Produksi Hormon Pertumbuhan**
            - IAA (Auxin): 10-50 µg/ml
            - Gibberellin: 5-20 µg/ml
            - Cytokinin: 2-10 µg/ml
            
            **3. Dekomposisi Bahan Organik**
            - Selulosa, hemiselulosa, lignin
            - Protein, lemak, karbohidrat
            - Pestisida, herbisida (detoksifikasi)
            
            **4. Bioremediasi**
            - Mengurangi H₂S (bau telur busuk)
            - Mengurangi NH₃ (bau amoniak)
            - Mengurangi CH₄ (gas rumah kaca)
            """)
            
            st.info("""
            📚 **Referensi Ilmiah:**
            - Madigan et al. (2011). *Annual Review of Microbiology*, 65, 25-47
            - Hiraishi & Kitamura (1984). *Bull. Japanese Society Scientific Fisheries*, 50(10), 1929-1937
            - Sasikala & Ramana (1998). *Advances in Applied Microbiology*, 45, 1-92
            """)
    
    with purple_tab2:
        st.subheader("🧫 Produksi Kultur Purple Bacteria")
        
        prod_tab1, prod_tab2 = st.tabs([
            "Isolasi dari Alam",
            "Perbanyakan Massal"
        ])
        
        with prod_tab1:
            st.markdown("#### 🌾 Isolasi dari Sawah/Kolam")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Bahan & Alat:**")
                st.markdown("""
                - Lumpur sawah/kolam: 100 gram
                - Botol kaca bening: 500 ml
                - Air bersih: 400 ml
                - Gula merah: 10 gram
                - Ragi tape: 1 butir
                - Lampu pijar 40-60 watt
                """)
                
                st.markdown("**Cara Isolasi:**")
                st.markdown("""
                1. **Sampling**: Ambil lumpur dari sawah/kolam (kedalaman 5-10 cm)
                2. **Campur**: Lumpur 100g + Air 400ml + Gula 10g + Ragi 1 butir
                3. **Wadah**: Masukkan ke botol kaca bening
                4. **Tutup**: Tutup longgar (biarkan gas keluar)
                5. **Inkubasi**: 
                   - Letakkan di dekat lampu pijar (30-40 cm)
                   - Suhu: 28-32°C
                   - Cahaya: 24 jam (anaerob fotosintesis)
                6. **Observasi**: 
                   - Hari 3-5: Air mulai keruh
                   - Hari 7-10: Warna merah-ungu muncul
                   - Hari 14: Warna merah pekat
                7. **Panen**: Ambil cairan (biang purple bacteria)
                """)
            
            with col2:
                st.success("✅ **Ciri Berhasil:**")
                st.markdown("""
                - Warna merah-ungu pekat
                - Bau asam fermentasi (tidak busuk)
                - Tidak ada lapisan putih di permukaan
                - Cairan agak kental
                """)
                
                st.error("❌ **Ciri Gagal:**")
                st.markdown("""
                - Warna tetap coklat/hijau
                - Bau busuk menyengat
                - Banyak jamur putih/hijau
                - Terlalu banyak oksigen (tutup terlalu longgar)
                """)
                
                st.warning("⚠️ **Tips Sukses:**")
                st.markdown("""
                - Gunakan air non-klorin (air sumur/air hujan)
                - Hindari kontaminasi udara berlebihan
                - Cahaya harus cukup (lampu pijar, bukan LED)
                - Suhu stabil 28-32°C
                - Jangan dikocok/diaduk (anaerob)
                """)
        
        with prod_tab2:
            st.markdown("#### 🏭 Perbanyakan Massal")
            
            st.markdown("""
            **Media Produksi (per 10 Liter):**
            - Air bersih: 10 liter
            - Gula merah/molase: 100 gram (1%)
            - Ragi tape: 5 butir
            - Urea: 10 gram (sumber N)
            - TSP: 5 gram (sumber P)
            - Biang purple bacteria: 500 ml (5%)
            
            **Prosedur:**
            1. **Larutkan**: Gula + Urea + TSP dalam air hangat
            2. **Dinginkan**: Hingga suhu ruang (28-30°C)
            3. **Inokulasi**: Tambahkan biang 5-10%
            4. **Wadah**: Jerigen/drum plastik transparan
            5. **Tutup**: Tutup longgar (pasang selang ke botol air untuk buang gas)
            6. **Cahaya**: Lampu pijar 60-100 watt, jarak 30-50 cm
            7. **Inkubasi**: 7-14 hari, suhu 28-32°C
            8. **Panen**: Warna merah pekat, bau asam segar
            
            **Quality Control:**
            - Warna: Merah-ungu pekat (OD₆₀₀ \u003e 1.0)
            - pH: 6.5-7.5
            - Bau: Asam fermentasi (tidak busuk)
            - Kepadatan: 10⁷-10⁹ CFU/ml
            - Viabilitas: \u003e80% (mikroskop)
            
            **Penyimpanan:**
            - Botol gelap, tutup rapat
            - Suhu: 4-15°C (kulkas)
            - Tahan: 3-6 bulan
            - Sebelum pakai: Kocok perlahan
            
            **Yield:** 1L biang → 100L kultur (rasio 1:100)
            """)
            
            st.success("""
            💡 **Formula Ekonomis (Skala Petani):**
            - Air: 20 liter
            - Gula merah: 200 gram (Rp 3,000)
            - Ragi: 10 butir (Rp 2,000)
            - Urea: 20 gram (Rp 500)
            - Biang: 1 liter (Rp 5,000)
            - **Total: Rp 10,500 untuk 20 liter** (Rp 525/liter)
            """)
    
    with purple_tab3:
        st.subheader("💉 Aplikasi Purple Bacteria untuk Pertanian")
        
        st.markdown("### 🌾 Aplikasi Tanaman Padi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Dosis & Cara:**")
            st.markdown("""
            **1. Pengolahan Tanah:**
            - Dosis: 5-10 L/ha
            - Campur dengan air 200-500 L
            - Semprot ke tanah sebelum bajak
            - Tunggu 3-7 hari, lalu bajak
            
            **2. Persemaian:**
            - Dosis: 2-3 L per 100 m² bedengan
            - Campur dengan air 20 L
            - Siram ke bedengan setelah semai
            - Ulangi setiap 7 hari (3x)
            
            **3. Tanam Pindah:**
            - Dosis: 1-2 L per 1000 bibit
            - Rendam akar bibit 10-15 menit
            - Langsung tanam
            
            **4. Pemeliharaan:**
            - Dosis: 5-10 L/ha
            - Aplikasi: 3-4 kali per musim
            - Waktu: 2, 4, 6, 8 MST
            - Cara: Kocor atau semprot
            """)
        
        with col2:
            st.success("**Hasil yang Diharapkan:**")
            st.markdown("""
            - Pertumbuhan vegetatif 20-30% lebih cepat
            - Anakan produktif naik 15-25%
            - Gabah lebih berisi (berat 1000 butir ↑ 10-15%)
            - Hasil panen naik 15-30%
            - Hemat pupuk urea 20-40%
            - Tanah lebih gembur dan subur
            """)
            
            st.info("**Kombinasi Optimal:**")
            st.markdown("""
            - Purple Bacteria + ROTAN/MOL
            - Purple Bacteria + Azotobacter
            - Purple Bacteria + Kompos
            - Kurangi urea 30-50% dari dosis normal
            """)
        
        st.markdown("---")
        st.markdown("### 🥬 Aplikasi Sayuran & Buah")
        
        app_data = {
            'Tanaman': [
                'Tomat, Cabai, Terong',
                'Kubis, Sawi, Kangkung',
                'Bawang Merah, Bawang Putih',
                'Jeruk, Mangga, Durian',
                'Strawberry, Melon'
            ],
            'Dosis (ml/tanaman)': [
                '50-100',
                '30-50',
                '20-30',
                '200-500',
                '50-100'
            ],
            'Frekuensi': [
                'Setiap 7-10 hari',
                'Setiap 7 hari',
                'Setiap 10 hari',
                'Setiap 14 hari',
                'Setiap 7 hari'
            ],
            'Metode': [
                'Kocor + Semprot',
                'Kocor',
                'Kocor',
                'Kocor (area perakaran)',
                'Kocor + Semprot'
            ],
            'Hasil': [
                'Hasil ↑ 20-35%, kualitas ↑',
                'Pertumbuhan ↑ 25%, lebih hijau',
                'Umbi ↑ 15-25%, tahan layu',
                'Buah ↑ 20-30%, manis ↑',
                'Buah ↑ 25-40%, Brix ↑ 2-3°'
            ]
        }
        
        df_app = pd.DataFrame(app_data)
        st.dataframe(df_app, use_container_width=True, hide_index=True)
    
    with purple_tab4:
        st.subheader("🐟 Aplikasi Purple Bacteria untuk Akuakultur")
        st.success("**Meningkatkan Kualitas Air & Kesehatan Ikan/Udang**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🐟 Kolam Ikan (Lele, Nila, Patin)")
            st.markdown("""
            **Dosis:**
            - Kolam baru: 10-20 L per 1000 m³ air
            - Maintenance: 5-10 L per 1000 m³ per minggu
            
            **Cara Aplikasi:**
            1. Encerkan purple bacteria dengan air kolam (1:10)
            2. Siram merata ke seluruh permukaan kolam
            3. Waktu terbaik: Pagi hari (06:00-08:00)
            4. Frekuensi: 1-2x per minggu
            
            **Manfaat:**
            - Mengurangi NH₃ (amoniak) 40-60%
            - Mengurangi H₂S (bau busuk) 50-70%
            - Meningkatkan DO (dissolved oxygen)
            - Mengurangi patogen (Aeromonas, Vibrio)
            - Pertumbuhan ikan 15-25% lebih cepat
            - FCR (Feed Conversion Ratio) lebih baik
            - Survival rate naik 10-20%
            """)
        
        with col2:
            st.markdown("#### 🦐 Tambak Udang (Vaname, Windu)")
            st.markdown("""
            **Dosis:**
            - Persiapan tambak: 20-30 L/ha
            - Maintenance: 10-15 L/ha per minggu
            
            **Cara Aplikasi:**
            1. Aplikasi pertama: 1 minggu sebelum tebar benur
            2. Aplikasi rutin: Setiap 5-7 hari
            3. Dosis lebih tinggi saat:
               - Setelah hujan lebat
               - Setelah panen parsial
               - Saat kualitas air menurun
            
            **Manfaat:**
            - Stabilkan pH (7.5-8.5)
            - Mengurangi vibrio (penyebab WSSV, IMNV)
            - Meningkatkan plankton (pakan alami)
            - Mengurangi bau tambak
            - Pertumbuhan udang 20-30% lebih cepat
            - Survival rate naik 15-25%
            - Kualitas udang lebih baik (warna, tekstur)
            """)
        
        st.markdown("---")
        st.markdown("#### 🗑️ Aplikasi Lain: Pengomposan & Limbah")
        
        col_other1, col_other2 = st.columns(2)
        
        with col_other1:
            st.info("**Bioaktivator Kompos:**")
            st.markdown("""
            - Dosis: 1-2 L per 100 kg bahan organik
            - Cara: Semprot merata saat membuat tumpukan
            - Hasil: Kompos matang 30-50% lebih cepat (30-45 hari)
            - Kualitas: C/N ratio lebih baik, bau tidak menyengat
            """)
        
        with col_other2:
            st.warning("**Pengolahan Limbah (IPAL, Septik Tank):**")
            st.markdown("""
            - Dosis: 5-10 L per 1000 L limbah
            - Frekuensi: 1x per minggu
            - Manfaat: Mengurangi BOD/COD 40-60%, bau hilang
            - Aplikasi: Peternakan, rumah potong, industri pangan
            """)

# ===== TAB 10: Amino Acid Fertilizers =====
with tab_amino:
    st.header("🧬 Pupuk Asam Amino (Amino Acid Fertilizers)")
    st.info("**Biostimulant Premium** - Meningkatkan penyerapan hara, sintesis protein, dan ketahanan stres")
    
    st.markdown("""
    ### 🎯 Manfaat Utama Pupuk Asam Amino
    
    **Nutrisi & Pertumbuhan:**
    - ✅ **Memberikan Unsur Hara Lengkap**: NPK lengkap + unsur hara mikro (Fe, Zn, Mn, Cu, B, Mo)
    - ✅ **Mempercepat Pertumbuhan Tanaman**: Proses metabolisme lebih efisien
    - ✅ **Sumber Mineral & Asam Amino**: 18+ jenis asam amino esensial untuk sintesis protein
    - ✅ **Asam Nukleat & Senyawa Aktif**: Meningkatkan aktivitas fisiologis tanaman
    - ✅ **Polysakarida**: Sumber energi dan struktur sel tanaman
    
    **Produktivitas:**
    - 🌾 **Memperbanyak & Memperbesar Anakan**: Tanaman lebih rimbun dan seragam (25-40% lebih banyak)
    - 🌸 **Mempercepat Pembungaan & Pembuahan**: Fase generatif lebih cepat 7-14 hari
    - 🍎 **Meningkatkan Berat/Bobot Bulir & Buah**: Gabah lebih berisi, buah lebih besar (15-30%)
    - ⏱️ **Mempercepat Pematangan**: Waktu panen lebih cepat, efisiensi musim tanam
    - 🍓 **Meningkatkan Kualitas Rasa**: Sayuran lebih segar, buah lebih manis (Brix naik 2-4°)
    
    **Ketahanan:**
    - 🛡️ **Meningkatkan Daya Tahan Penyakit**: Tahan layu fusarium, bakteri, virus (40-60% lebih tahan)
    - 🌡️ **Ketahanan Stres Lingkungan**: Tahan kekeringan, cuaca ekstrem, salinitas
    - 🌱 **Menyuburkan Tanah**: Meningkatkan kesuburan tanah dan melarutkan sisa pupuk kimia
    
    **Aplikasi Universal:**
    - 🌾 Pertanian (padi, jagung, kedelai)
    - 🌳 Perkebunan (kelapa sawit, karet, kakao)
    - 🌲 Kehutanan (tanaman pionir, reboisasi)
    - 🥬 Hortikultura (sayuran, buah-buahan)
    """)
    
    
    amino_tab1, amino_tab2, amino_tab3, amino_tab4, amino_tab5 = st.tabs([
        "🐟 Fish Amino Acid (FAA)",
        "🐌 Keong Mas Amino",
        "🌱 Plant-Based Amino",
        "🧪 Aplikasi & Dosis",
        "📊 Produk Komersial"
    ])
    
    with amino_tab1:
        st.subheader("🐟 Fermented Fish Amino Acid (FAA)")
        st.success("**Metode Korean Natural Farming** - Sumber asam amino lengkap (18+ jenis)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥦 Bahan-Bahan")
            st.markdown("""
            **Bahan Utama:**
            - **Ikan Segar** (teri/tongkol/sisa ikan): 1 kg
            - **Gula Merah/Molase**: 1 kg (rasio 1:1)
            
            **Bahan Tambahan (Opsional):**
            - Usus Ikan: 200 gram (mempercepat fermentasi)
            - Nanas: 1 buah (enzim bromelin)
            - EM4/Starter: 50 ml (opsional)
            
            **Wadah:**
            - Toples kaca/plastik food grade 5L
            - Jangan gunakan logam!
            """)
            
            st.markdown("#### 🔬 Kandungan Ilmiah")
            st.markdown("""
            - **18 Asam Amino Esensial** (Lysine, Methionine, Tryptophan, dll)
            - **Nitrogen Organik**: 8-12%
            - **Peptida Bioaktif**: Meningkatkan imunitas tanaman
            - **Mineral**: Ca, Mg, Fe, Zn dari tulang ikan
            
            📚 **Referensi**: 
            - Colla et al. (2015). *Scientia Horticulturae*
            - Kauffman et al. (2007). *HortScience*
            """)
        
        with col2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            **Metode Tradisional (14 hari):**
            1. **Potong**: Cincang ikan + usus menjadi potongan kecil
            2. **Campur**: Ikan 1kg + Gula merah 1kg (1:1), aduk rata
            3. **Wadah**: Masukkan ke toples, tekan hingga padat
            4. **Tutup**: Tutup rapat (anaerob), beri lubang kecil untuk gas
            5. **Fermentasi**: Simpan di tempat teduh, **14-21 hari**
            6. **Panen**: Saring cairannya (warna coklat kehitaman)
            7. **Simpan**: Botol kedap udara, tahan 6-12 bulan
            
            **Metode Cepat dengan Enzim (7 hari):**
            1. Blender ikan + nanas (enzim bromelin)
            2. Campur dengan gula merah 1:1
            3. Tambahkan EM4 50ml
            4. Fermentasi 7-10 hari
            5. Saring dan siap pakai
            """)
            
            st.success("✅ **Ciri Berhasil**: Bau asam fermentasi (seperti terasi), warna coklat tua, tidak berbau busuk")
            st.error("❌ **Ciri Gagal**: Bau busuk menyengat, warna hitam pekat, banyak belatung")
    
    with amino_tab2:
        st.subheader("🐌 Keong Mas Amino Acid (Golden Snail)")
        st.info("**Pemanfaatan Hama Menjadi Pupuk** - Tinggi protein (60-70%) dan kalsium")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥦 Bahan-Bahan")
            st.markdown("""
            - **Keong Mas Hidup**: 1 kg (dengan cangkang)
            - **Gula Merah/Molase**: 500 gram
            - **Air Kelapa**: 2 liter
            - **Buah Maja**: ½ buah (atau gula tambahan)
            - **EM4**: 50 ml (opsional)
            
            **Alternatif tanpa Maja:**
            - Ganti dengan 500g gula merah tambahan
            """)
            
            st.markdown("#### 🔬 Kandungan")
            st.markdown("""
            - **Protein**: 60-70% (tertinggi di antara MOL)
            - **Asam Amino**: Arginine, Lysine, Leucine
            - **Kalsium (Ca)**: Dari cangkang (20-30%)
            - **Enzim Proteolitik**: Mempercepat dekomposisi
            """)
        
        with col2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1. **Tumbuk**: Hancurkan keong mas (cangkang + daging) hingga halus
            2. **Maja**: Tumbuk buah maja atau larutkan gula
            3. **Campur**: Keong + Maja + Air kelapa + Gula merah
            4. **Aduk**: Kocok hingga rata
            5. **Wadah**: Simpan di toples plastik/kaca
            6. **Fermentasi**: 
               - Buka tutup setiap pagi (buang gas)
               - Aduk setiap 2 hari
               - **15-21 hari** hingga matang
            7. **Saring**: Ambil cairannya, ampas bisa untuk kompos
            """)
            
            st.success("✅ **Hasil**: Cairan coklat kental, bau fermentasi kuat (seperti petis)")
            
            st.markdown("#### 💉 Dosis Aplikasi")
            st.markdown("""
            - **Kompos**: 1L MOL : 5L air + gula
            - **Tanaman**: 1L MOL : 10-15L air
            - **Frekuensi**: Setiap 7-10 hari
            """)
    
    with amino_tab3:
        st.subheader("🌱 Plant-Based Amino Acid (Vegan)")
        st.info("**Alternatif Nabati** - Dari fermentasi kacang-kacangan dan sayuran")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥦 Formula 1: Kedelai Fermentasi")
            st.markdown("""
            **Bahan:**
            - Kedelai/Kacang Hijau: 2 kg
            - Gula Merah: 1 kg
            - Air Leri: 5 liter
            - Ragi Tempe: 2 bungkus
            - EM4: 100 ml
            
            **Cara:**
            1. Rebus kacang hingga empuk (jangan terlalu lembek)
            2. Dinginkan, hancurkan kasar
            3. Campur dengan ragi tempe, diamkan 24 jam
            4. Tambahkan gula + air leri + EM4
            5. Fermentasi 14 hari (anaerob)
            6. Saring dan siap pakai
            
            **Kandungan:**
            - Asam amino: Glutamic acid, Aspartic acid
            - Protein: 40-50%
            - Vitamin B kompleks
            """)
        
        with col2:
            st.markdown("#### 🥦 Formula 2: Sayuran Hijau")
            st.markdown("""
            **Bahan:**
            - Kangkung/Bayam/Daun Kacang: 3 kg
            - Kacang Panjang: 1 kg
            - Gula Merah: 1 kg
            - Air Kelapa: 3 liter
            - Air Leri: 2 liter
            
            **Cara:**
            1. Blender semua sayuran seperti jus
            2. Campur dengan gula + air kelapa + air leri
            3. Masukkan wadah plastik/kaca
            4. Fermentasi 14 hari (buka tutup tiap 2 hari)
            5. Saring dan aplikasikan
            
            **Kandungan:**
            - Asam amino: Proline, Glycine, Alanine
            - Klorofil: Meningkatkan fotosintesis
            - Nitrogen organik: 5-8%
            """)
            
            st.success("💡 **Keunggulan**: Ramah lingkungan, tidak berbau amis, cocok untuk pertanian organik")
    
    with amino_tab4:
        st.subheader("🧪 Aplikasi & Dosis Pupuk Asam Amino")
        
        st.markdown("### 📋 Jenis & Kandungan")
        
        col_type1, col_type2 = st.columns(2)
        
        with col_type1:
            st.markdown("#### 💧 Cair (Liquid)")
            st.markdown("""
            **Karakteristik:**
            - Berbahan dasar fermentasi alami (nanas, ikan, keong)
            - Mengandung NPK + Asam Amino + ZPT (Zat Pengatur Tumbuh)
            - **Cepat diserap** tanaman (2-4 jam)
            - pH: 4.5-6.5 (asam)
            
            **Kandungan Tipikal:**
            - Nitrogen (N): 2-5%
            - Asam Amino Bebas: 8-15%
            - Peptida: 5-10%
            - Mikronutrien: Fe, Zn, Mn, Cu
            """)
        
        with col_type2:
            st.markdown("#### 🧊 Padat/Slow Release")
            st.markdown("""
            **Karakteristik:**
            - Bentuk granul/powder
            - **Nitrogen (N) tinggi**: 10-20%
            - Dilepas perlahan (slow release)
            - Tahan 30-60 hari di tanah
            
            **Kandungan Tipikal:**
            - Nitrogen (N): 10-20%
            - Asam Amino Total: 30-50%
            - Protein Hydrolysate: 40-60%
            - Bahan organik: 60-80%
            """)
        
        st.markdown("---")
        st.markdown("### 💉 Cara Penggunaan (Umum)")
        
        st.markdown("""
        **Persiapan:**
        1. **Kocok dahulu** (untuk yang cair) - endapan normal
        2. **Campur**: 
           - Dosis rendah: 1 tutup botol (10 ml) per 1 liter air
           - Dosis standar: 20-30 ml per 1 liter air
           - Dosis tinggi: 100 ml per 10 liter air (fase kritis)
        
        **Metode Aplikasi:**
        """)
        
        col_app1, col_app2 = st.columns(2)
        
        with col_app1:
            st.success("**🌿 Semprot (Foliar Spray)**")
            st.markdown("""
            - **Volume**: 400-600 L/ha
            - **Konsentrasi**: 0.5-2% (5-20 ml/L)
            - **Waktu**: Pagi (06:00-09:00) atau Sore (16:00-18:00)
            - **Hindari**: Siang hari (penguapan tinggi)
            - **Frekuensi**: Setiap 7-10 hari
            
            **Keunggulan:**
            - Penyerapan cepat (2-4 jam)
            - Langsung ke metabolisme
            - Efisien untuk fase vegetatif
            """)
        
        with col_app2:
            st.info("**💧 Kocor/Siram (Drench/Root)**")
            st.markdown("""
            - **Volume**: 100-200 ml per tanaman
            - **Konsentrasi**: 1-3% (10-30 ml/L)
            - **Waktu**: Pagi atau sore (tanah lembab)
            - **Frekuensi**: Setiap 10-14 hari
            
            **Keunggulan:**
            - Merangsang akar
            - Meningkatkan mikroba tanah
            - Tahan lebih lama di rhizosphere
            - Cocok untuk fase generatif
            """)
        
        st.markdown("---")
        st.markdown("### 📅 Waktu Aplikasi Optimal")
        
        timing_data = {
            'Fase Pertumbuhan': [
                'Vegetatif Awal (0-30 HST)',
                'Vegetatif Akhir (30-60 HST)',
                'Generatif (Pembungaan)',
                'Pembuahan/Pengisian Bulir',
                'Menjelang Panen'
            ],
            'Metode': [
                'Semprot + Kocor',
                'Semprot (fokus daun)',
                'Kocor (fokus akar)',
                'Semprot + Kocor',
                'Semprot (maintenance)'
            ],
            'Frekuensi': [
                '1x per minggu',
                '1x per 10 hari',
                '2x per minggu (fase kritis)',
                '1x per minggu',
                '1x per 14 hari'
            ],
            'Dosis': [
                '10-20 ml/L',
                '20-30 ml/L',
                '30-50 ml/L (booster)',
                '20-30 ml/L',
                '10-15 ml/L'
            ]
        }
        
        df_timing = pd.DataFrame(timing_data)
        st.dataframe(df_timing, use_container_width=True, hide_index=True)
        
        st.warning("""
        ⚠️ **Catatan Penting:**
        - Jangan aplikasi saat hujan atau tanah becek
        - Hindari overdosis (bisa menyebabkan pertumbuhan tidak seimbang)
        - Kombinasikan dengan pupuk dasar NPK untuk hasil optimal
        - Simpan di tempat sejuk, hindari sinar matahari langsung
        """)
    
    with amino_tab5:
        st.subheader("📊 Produk Komersial Amino Acid")
        st.info("**Referensi Produk Terpercaya** - Untuk perbandingan dan standar kualitas")
        
        commercial_data = {
            'Produk': [
                'Vitalazo',
                'Verti K',
                'DARA',
                'Booster 76',
                'Shoucheng',
                'JetPro'
            ],
            'Fungsi Utama': [
                'Pembangkit Anakan',
                'Pelebat Bobot Bulir',
                'Booster Buah (Tinggi K)',
                'Pelebat & Penyubur',
                'Pupuk Daun Premium',
                'Booster Bobot Gabah'
            ],
            'Kandungan Kunci': [
                'Asam Amino + Sitokinin',
                'Kalium (K) + Asam Amino',
                'K₂O 20% + Amino Acid',
                'NPK + 18 Asam Amino',
                'Amino Acid + Mikronutrien',
                'Protein Hydrolysate + K'
            ],
            'Dosis Umum': [
                '10-20 ml/L',
                '20-30 ml/L',
                '2-3 ml/L',
                '1-2 tutup/14L',
                '15-20 ml/L',
                '20-30 ml/L'
            ],
            'Aplikasi': [
                'Semprot/Kocor',
                'Kocor (fase generatif)',
                'Semprot (buah)',
                'Semprot/Kocor',
                'Semprot (daun)',
                'Kocor (bulir)'
            ],
            'Harga Estimasi': [
                'Rp 50-80k/L',
                'Rp 60-90k/L',
                'Rp 70-100k/L',
                'Rp 45-75k/L',
                'Rp 80-120k/L',
                'Rp 55-85k/L'
            ]
        }
        
        df_commercial = pd.DataFrame(commercial_data)
        st.dataframe(df_commercial, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 🏆 Perbandingan: Homemade vs Komersial")
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.success("**✅ Pupuk Asam Amino Homemade (FAA/Keong Mas)**")
            st.markdown("""
            **Keunggulan:**
            - Biaya produksi sangat rendah (Rp 5-15k/L)
            - Bahan lokal, mudah didapat
            - Ramah lingkungan (zero waste)
            - Mikroorganisme hidup (probiotik)
            - Bisa diproduksi skala rumahan
            
            **Kekurangan:**
            - Kandungan tidak terstandar
            - Bau kurang sedap (ikan/keong)
            - Perlu waktu fermentasi (14-21 hari)
            - Shelf life terbatas (6-12 bulan)
            """)
        
        with col_comp2:
            st.info("**🏭 Pupuk Asam Amino Komersial**")
            st.markdown("""
            **Keunggulan:**
            - Kandungan terstandar (SNI/ISO)
            - Tidak berbau
            - Siap pakai (instant)
            - Shelf life panjang (2-3 tahun)
            - Formulasi spesifik (fase tanaman)
            
            **Kekurangan:**
            - Harga tinggi (Rp 50-120k/L)
            - Ketergantungan pasokan
            - Bahan kimia sintetis (beberapa produk)
            - Tidak ada mikroorganisme hidup
            """)
        
        st.markdown("---")
        st.success("""
        💡 **Rekomendasi Praktis:**
        - **Petani Skala Kecil**: Gunakan homemade (FAA/Keong Mas) untuk efisiensi biaya
        - **Petani Komersial**: Kombinasi 70% homemade + 30% komersial (fase kritis)
        - **Pertanian Organik**: 100% homemade (sertifikasi organik)
        - **Greenhouse/Hidroponik**: Komersial (standar tinggi, tidak berbau)
        """)

# ===== TAB 9: Growth Boosters =====
with tab_booster:
    st.header("🌊 Booster Pertumbuhan (Growth Stimulants)")
    st.info("**Plant Biostimulants** - Hormon alami, ekstrak laut, dan asam humat untuk pertumbuhan maksimal")
    
    st.markdown("""
    ### 🎯 Manfaat Utama
    - **Merangsang Pertumbuhan Akar**: Sistem perakaran lebih kuat dan luas
    - **Meningkatkan Penyerapan Hara**: Efisiensi pupuk naik 30-50%
    - **Mempercepat Pembungaan**: Flowering lebih cepat dan seragam
    - **Ketahanan Stres**: Tahan kekeringan, salinitas, suhu ekstrem
    - **Meningkatkan Hasil**: Yield naik 15-40%
    """)
    
    booster_tab1, booster_tab2, booster_tab3, booster_tab4, booster_tab5 = st.tabs([
        "🌊 Seaweed Extract",
        "🪨 Humic & Fulvic Acid",
        "🥥 Coconut Water + Chitosan",
        "🌿 Moringa Extract",
        "📊 Aplikasi & Kombinasi"
    ])
    
    with booster_tab1:
        st.subheader("🌊 Seaweed Extract (Liquid Kelp)")
        st.success("**Sumber Hormon Alami** - Cytokinin, Auxin, Gibberellin dari rumput laut")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥦 Bahan-Bahan")
            st.markdown("""
            **Bahan Utama:**
            - **Rumput Laut Segar** (Sargassum/Gracilaria): 2 kg
            - **Air Bersih**: 10 liter
            - **Molase/Gula Merah**: 500 gram
            - **EM4**: 100 ml (opsional)
            
            **Alternatif:**
            - Rumput laut kering: 500 gram (rendam 24 jam)
            - Spirulina powder: 200 gram (instant)
            
            **Sumber Rumput Laut:**
            - Pantai (gratis, cuci bersih)
            - Pasar ikan (Rp 5-10k/kg)
            - Toko bahan makanan (rumput laut kering)
            """)
            
            st.markdown("#### 🔬 Kandungan Ilmiah")
            st.markdown("""
            **Fitohormon:**
            - **Cytokinin**: 10-100 ppm (pembelahan sel)
            - **Auxin (IAA)**: 5-50 ppm (pertumbuhan akar)
            - **Gibberellin**: 1-10 ppm (perpanjangan batang)
            
            **Nutrisi:**
            - Nitrogen (N): 1-3%
            - Kalium (K): 3-5%
            - Trace elements: I, Fe, Zn, Mn, Cu, B
            - Alginic acid: 10-30% (chelator alami)
            - Mannitol: 5-10% (osmoprotektan)
            
            📚 **Referensi**: 
            - Khan et al. (2009). *J. Plant Growth Regulation*
            - Craigie (2011). *J. Applied Phycology*
            """)
        
        with col2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            **Metode Fermentasi (14 hari):**
            1. **Cuci**: Bilas rumput laut dengan air tawar (hilangkan garam)
            2. **Potong**: Cincang kasar (2-3 cm)
            3. **Blender**: Haluskan dengan air (rasio 1:5)
            4. **Campur**: Tambahkan molase + EM4
            5. **Fermentasi**: Simpan di wadah tertutup, 14 hari
            6. **Aduk**: Buka dan aduk setiap 3 hari
            7. **Saring**: Ambil cairannya (warna coklat kehijauan)
            
            **Metode Cepat - Cold Extraction (24 jam):**
            1. Rendam rumput laut segar 1kg dalam 5L air
            2. Tambahkan 100ml cuka (pH 4-5)
            3. Diamkan 24 jam, aduk setiap 6 jam
            4. Saring dan langsung pakai
            
            **Metode Instant - Hot Extraction (2 jam):**
            1. Rebus rumput laut 1kg + 5L air
            2. Didihkan 30 menit (api kecil)
            3. Dinginkan, saring
            4. Siap pakai (tahan 1 minggu)
            """)
            
            st.success("✅ **Ciri Berhasil**: Bau laut segar, warna hijau-coklat, tidak berbusa berlebihan")
    
    with booster_tab2:
        st.subheader("🪨 Humic & Fulvic Acid")
        st.info("**Soil Conditioner Premium** - Meningkatkan CEC tanah dan chelasi nutrisi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥦 Sumber Humic Acid")
            st.markdown("""
            **1. Dari Vermicompost (Kascing)**
            - Kascing matang: 5 kg
            - Air bersih: 20 liter
            - KOH/NaOH: 50 gram (pH 10-11)
            - Waktu ekstraksi: 24 jam
            
            **2. Dari Kompos Matang**
            - Kompos hitam (>6 bulan): 10 kg
            - Air: 30 liter
            - KOH: 100 gram
            - Aduk 48 jam, saring
            
            **3. Dari Leonardite (Komersial)**
            - Leonardite powder: 1 kg
            - Air: 10 liter
            - KOH: 50 gram
            - Hasil: Humic acid 10-15%
            """)
            
            st.markdown("#### 🔬 Kandungan")
            st.markdown("""
            **Humic Acid:**
            - Berat molekul: 10,000-100,000 Da
            - Fungsi: Meningkatkan CEC tanah
            - Konsentrasi: 5-15% (ekstrak)
            
            **Fulvic Acid:**
            - Berat molekul: 1,000-10,000 Da
            - Fungsi: Chelasi nutrisi, transport
            - Konsentrasi: 2-5% (ekstrak)
            
            📚 **Referensi**: 
            - Canellas et al. (2015). *Scientia Horticulturae*
            """)
        
        with col2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            **Ekstraksi Humic Acid (dari Kascing):**
            1. **Campur**: 5 kg kascing + 20L air
            2. **Alkali**: Tambahkan 50g KOH (pH 10-11)
            3. **Aduk**: Aduk kuat selama 2 jam
            4. **Diamkan**: 24 jam (warna hitam pekat)
            5. **Saring**: Gunakan kain halus
            6. **Netralisasi**: Turunkan pH ke 6-7 dengan cuka
            7. **Simpan**: Botol gelap, tahan 6 bulan
            
            **Ekstraksi Fulvic Acid:**
            1. Ambil filtrat humic acid
            2. Tambahkan HCl hingga pH 2
            3. Diamkan 12 jam (fulvic tetap larut)
            4. Saring (humic mengendap, fulvic di cairan)
            5. Netralisasi pH ke 6-7
            6. Siap pakai
            """)
            
            st.markdown("#### 💉 Dosis Aplikasi")
            st.markdown("""
            **Humic Acid:**
            - Tanah: 2-5 L/ha (konsentrasi 10%)
            - Kocor: 50-100 ml/tanaman (diencerkan 1:100)
            - Frekuensi: Setiap 2-4 minggu
            
            **Fulvic Acid:**
            - Semprot: 20-50 ml/L (foliar)
            - Kocor: 100 ml/tanaman (1:50)
            - Frekuensi: Setiap 7-14 hari
            """)
    
    with booster_tab3:
        st.subheader("🥥 Coconut Water + Chitosan")
        st.success("**Natural Cytokinin + Defense Elicitor** - Kombinasi hormon dan imunitas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥥 Air Kelapa (Natural Cytokinin)")
            st.markdown("""
            **Kandungan:**
            - **Cytokinin (Zeatin)**: 5-10 ppm
            - **Auxin (IAA)**: 1-5 ppm
            - **Gibberellin**: 0.5-2 ppm
            - **Mineral**: K, Ca, Mg, Fe
            - **Gula**: Glukosa, fruktosa (energi)
            
            **Manfaat:**
            - Merangsang pembelahan sel
            - Mempercepat pertumbuhan tunas
            - Meningkatkan pembungaan
            - Anti-aging (menunda senescence)
            
            **Aplikasi:**
            - Konsentrasi: 10-30% (100-300 ml/L)
            - Metode: Semprot atau kocor
            - Waktu: Fase vegetatif dan pembungaan
            - Frekuensi: Setiap 7-10 hari
            """)
        
        with col2:
            st.markdown("#### 🦐 Chitosan (Defense Elicitor)")
            st.markdown("""
            **Sumber Chitosan:**
            - Cangkang udang/kepiting: 1 kg
            - HCl 5%: 2 liter (demineralisasi)
            - NaOH 40%: 2 liter (deproteinasi)
            - Asam asetat 1%: 1 liter (pelarutan)
            
            **Cara Pembuatan (Sederhana):**
            1. Cuci cangkang, keringkan
            2. Tumbuk halus (powder)
            3. Rendam HCl 5%, 24 jam (hilangkan mineral)
            4. Cuci, rendam NaOH 40%, 24 jam (hilangkan protein)
            5. Cuci hingga netral
            6. Keringkan = Chitosan powder
            7. Larutkan 1g chitosan + 1L asam asetat 1%
            
            **Manfaat:**
            - Menginduksi resistensi sistemik (ISR)
            - Meningkatkan enzim pertahanan (PAL, POX)
            - Anti-jamur dan anti-bakteri
            - Meningkatkan lignifikasi (batang kuat)
            
            📚 **Referensi**: 
            - Culver et al. (2012). *Agronomy for Sustainable Development*
            """)
        
        st.markdown("---")
        st.markdown("#### 🧪 Formula Kombinasi: Kelapa + Chitosan")
        st.markdown("""
        **Bahan:**
        - Air kelapa muda: 1 liter
        - Chitosan solution (0.1%): 100 ml
        - Molase: 50 ml (perekat)
        - Air: 5 liter
        
        **Cara:**
        1. Campur air kelapa + chitosan solution
        2. Tambahkan molase (sebagai sticker)
        3. Encerkan dengan air hingga 5L
        4. Aplikasi semprot pagi/sore
        
        **Hasil:**
        - Pertumbuhan tunas 30% lebih cepat
        - Ketahanan penyakit naik 40-60%
        - Pembungaan lebih seragam
        """)
    
    with booster_tab4:
        st.subheader("🌿 Moringa Extract (Zeatin-Rich)")
        st.info("**Super Booster** - Kandungan Zeatin (cytokinin) 1000x lebih tinggi dari tanaman lain!")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🥦 Bahan-Bahan")
            st.markdown("""
            **Bahan Utama:**
            - **Daun Kelor Segar**: 1 kg
            - **Air Bersih**: 5 liter
            - **Etanol 70%**: 500 ml (opsional, untuk ekstrak pekat)
            
            **Alternatif:**
            - Daun kelor kering: 300 gram
            - Moringa powder: 200 gram (instant)
            
            **Sumber:**
            - Pohon kelor (gratis, tanam sendiri)
            - Pasar tradisional (Rp 5-10k/ikat)
            - Toko herbal (powder Rp 30-50k/kg)
            """)
            
            st.markdown("#### 🔬 Kandungan Ilmiah")
            st.markdown("""
            **Fitohormon:**
            - **Zeatin (Cytokinin)**: 5-200 µg/g (TERTINGGI!)
            - **Auxin**: 10-50 µg/g
            - **Gibberellin**: 5-20 µg/g
            
            **Nutrisi:**
            - Protein: 25-30%
            - Vitamin A: 6780 µg/100g
            - Vitamin C: 220 mg/100g
            - Kalsium: 440 mg/100g
            - Kalium: 259 mg/100g
            - Asam amino: 18 jenis
            
            **Antioksidan:**
            - Flavonoid: Quercetin, Kaempferol
            - Phenolic compounds
            
            📚 **Referensi**: 
            - Fuglie (2000). *CTA Publication*
            - Rady et al. (2015). *Scientia Horticulturae*
            """)
        
        with col2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            **Metode 1: Water Extract (Sederhana)**
            1. **Cuci**: Bilas daun kelor segar
            2. **Blender**: 1kg daun + 2L air, haluskan
            3. **Saring**: Gunakan kain halus
            4. **Encerkan**: Tambah air hingga 5L
            5. **Aplikasi**: Langsung pakai (tahan 3 hari di kulkas)
            
            **Metode 2: Fermentasi (Tahan Lama)**
            1. Blender daun kelor + air (1:3)
            2. Tambahkan molase 100ml + EM4 50ml
            3. Fermentasi 7 hari (anaerob)
            4. Saring, siap pakai (tahan 3 bulan)
            
            **Metode 3: Ethanol Extract (Pekat)**
            1. Keringkan daun kelor (oven 50°C)
            2. Tumbuk halus (powder)
            3. Rendam 100g powder + 500ml etanol 70%
            4. Diamkan 48 jam, saring
            5. Evaporasi etanol (tinggal ekstrak pekat)
            6. Encerkan 1:1000 saat aplikasi
            """)
            
            st.success("✅ **Ciri Berhasil**: Warna hijau tua, bau khas kelor, tidak berbusa")
        
        st.markdown("---")
        st.markdown("#### 💉 Dosis & Aplikasi")
        
        moringa_dose = {
            'Metode': ['Water Extract', 'Fermentasi', 'Ethanol Extract'],
            'Konsentrasi': ['20-30%', '5-10%', '0.1-0.5%'],
            'Dosis': ['200-300 ml/L', '50-100 ml/L', '1-5 ml/L'],
            'Frekuensi': ['Setiap 7 hari', 'Setiap 10 hari', 'Setiap 14 hari'],
            'Aplikasi': ['Semprot/Kocor', 'Semprot/Kocor', 'Semprot (foliar)']
        }
        
        df_moringa = pd.DataFrame(moringa_dose)
        st.dataframe(df_moringa, use_container_width=True, hide_index=True)
        
        st.warning("""
        **📋 Hasil yang Diharapkan:**
        - Pertumbuhan vegetatif 25-40% lebih cepat
        - Pembungaan lebih awal (7-14 hari)
        - Jumlah bunga/buah naik 30-50%
        - Ukuran buah lebih besar (15-25%)
        - Ketahanan stres meningkat
        """)
    
    with booster_tab5:
        st.subheader("📊 Aplikasi & Kombinasi Booster")
        
        st.markdown("### 🧪 Tabel Aplikasi Lengkap")
        
        application_data = {
            'Booster': [
                'Seaweed Extract',
                'Humic Acid',
                'Fulvic Acid',
                'Air Kelapa',
                'Chitosan',
                'Moringa Extract'
            ],
            'Fase Optimal': [
                'Vegetatif + Generatif',
                'Awal tanam + Vegetatif',
                'Sepanjang musim',
                'Vegetatif + Pembungaan',
                'Sepanjang musim (preventif)',
                'Vegetatif + Pembungaan'
            ],
            'Metode': [
                'Semprot/Kocor',
                'Kocor (tanah)',
                'Semprot (foliar)',
                'Semprot/Kocor',
                'Semprot',
                'Semprot/Kocor'
            ],
            'Dosis': [
                '2-5 ml/L',
                '50-100 ml/tanaman (1:100)',
                '20-50 ml/L',
                '100-300 ml/L (10-30%)',
                '1-2 ml/L (0.1-0.2%)',
                '50-100 ml/L (5-10%)'
            ],
            'Frekuensi': [
                '7-10 hari',
                '14-21 hari',
                '7-14 hari',
                '7-10 hari',
                '10-14 hari',
                '7-10 hari'
            ],
            'Biaya/L': [
                'Rp 5-15k',
                'Rp 10-20k',
                'Rp 15-25k',
                'Rp 5-10k',
                'Rp 20-40k',
                'Rp 3-8k'
            ]
        }
        
        df_application = pd.DataFrame(application_data)
        st.dataframe(df_application, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.markdown("### 🔬 Formula Kombinasi Terbaik")
        
        st.success("**Formula 1: All-in-One Vegetatif Booster**")
        st.markdown("""
        **Komposisi (per 10L air):**
        - Seaweed extract: 50 ml
        - Moringa extract: 100 ml
        - Fulvic acid: 30 ml
        - Molase: 50 ml (sticker)
        
        **Manfaat:**
        - Pertumbuhan daun maksimal
        - Akar kuat dan luas
        - Fotosintesis optimal
        
        **Aplikasi:** Semprot setiap 7 hari (fase vegetatif)
        """)
        
        st.info("**Formula 2: Generatif Booster (Pembungaan & Pembuahan)**")
        st.markdown("""
        **Komposisi (per 10L air):**
        - Air kelapa: 2 liter (20%)
        - Moringa extract: 150 ml
        - Humic acid: 50 ml
        - Chitosan: 10 ml
        
        **Manfaat:**
        - Pembungaan seragam dan lebat
        - Fruit set tinggi (80-90%)
        - Ukuran buah besar
        - Ketahanan penyakit
        
        **Aplikasi:** Kocor + semprot setiap 7 hari (fase generatif)
        """)
        
        st.warning("**Formula 3: Stress Recovery (Pasca Kekeringan/Banjir)**")
        st.markdown("""
        **Komposisi (per 10L air):**
        - Seaweed extract: 100 ml (double dose)
        - Fulvic acid: 50 ml
        - Moringa extract: 100 ml
        - Chitosan: 20 ml
        
        **Manfaat:**
        - Recovery cepat (3-7 hari)
        - Meningkatkan osmoregulasi
        - Detoksifikasi
        - Induksi resistensi
        
        **Aplikasi:** Semprot intensif setiap 3 hari (hingga pulih)
        """)
        
        st.markdown("---")
        st.markdown("### 📅 Jadwal Aplikasi Terintegrasi (Contoh: Padi)")
        
        schedule_data = {
            'Fase (HST)': [
                '0-7 (Semai)',
                '7-21 (Vegetatif Awal)',
                '21-45 (Vegetatif Akhir)',
                '45-65 (Primordial)',
                '65-85 (Pembungaan)',
                '85-110 (Pengisian Bulir)',
                '110-120 (Pematangan)'
            ],
            'Booster Utama': [
                'Humic Acid + Seaweed',
                'Moringa + Fulvic',
                'Seaweed + Moringa',
                'Air Kelapa + Moringa',
                'Air Kelapa + Chitosan',
                'Fulvic + Seaweed',
                'Moringa (maintenance)'
            ],
            'Metode': [
                'Kocor',
                'Semprot + Kocor',
                'Semprot',
                'Kocor',
                'Semprot',
                'Semprot + Kocor',
                'Semprot'
            ],
            'Frekuensi': [
                '1x',
                '2x (interval 7 hari)',
                '3x (interval 7 hari)',
                '2x (interval 7 hari)',
                '3x (interval 5 hari)',
                '3x (interval 7 hari)',
                '1x'
            ]
        }
        
        df_schedule = pd.DataFrame(schedule_data)
        st.dataframe(df_schedule, use_container_width=True, hide_index=True)
        
        st.success("""
        💡 **Tips Kombinasi:**
        - **Jangan campur** Humic Acid + Chitosan (mengendap)
        - **Kombinasi terbaik**: Seaweed + Moringa + Fulvic
        - **Aplikasi pagi** (06:00-09:00) untuk penyerapan optimal
        - **Tambahkan sticker** (molase/surfaktan) untuk semprot
        - **Rotasi booster** setiap 2-3 minggu (hindari adaptasi)
        """)

# ===== TAB 10: Quality Control =====
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
            ],
            "🧬 Pupuk Asam Amino": [
                "Fish_Amino_Acid",
                "Keong_Mas_Amino",
                "Plant_Amino_Soybean"
            ],
            "🌊 Booster Pertumbuhan": [
                "Seaweed_Extract",
                "Humic_Acid_Extract",
                "Moringa_Extract",
                "Chitosan_Solution"
            ],
            "🍄 Mikoriza": [
                "AMF_Trap_Culture",
                "Ectomycorrhiza_Inoculum"
            ],
            "🔴 Bakteri Merah": [
                "Purple_Bacteria_Liquid"
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
