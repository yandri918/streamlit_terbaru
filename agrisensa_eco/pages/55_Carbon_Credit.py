import streamlit as st
import sys
import os
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.carbon_calculator import CarbonCalculator
# from utils.auth import require_auth, show_user_info_sidebar

# Page config
st.set_page_config(
    page_title="Carbon Credit Marketplace",
    page_icon="💰",
    layout="wide"
)

# Authentication
# user = require_auth()
# show_user_info_sidebar()

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0fdf4;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .result-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(16, 185, 129, 0.3);
        margin: 20px 0;
    }
    .info-box {
        background: #e0f2fe;
        border-left: 4px solid #0284c7;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💰 Carbon Credit Marketplace")
st.markdown("""
Platform untuk menghitung, mendaftarkan, dan menjual kredit karbon dari praktik pertanian berkelanjutan Anda.
Dapatkan penghasilan tambahan sambil menyelamatkan planet! 🌍
""")

st.markdown("---")

# Initialize calculator
calc = CarbonCalculator()

# Tabs
tab1, tab2, tab3 = st.tabs([
    "🧮 Kalkulator Karbon",
    "🛒 Marketplace (Coming Soon)",
    "📚 Panduan"
])

# ===== TAB 1: CARBON CALCULATOR =====
with tab1:
    st.subheader("Hitung Potensi Kredit Karbon Lahan Anda")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Input Data Lahan")
        
        area_ha = st.number_input(
            "Luas Lahan (ha)",
            min_value=0.1,
            max_value=1000.0,
            value=5.0,
            step=0.5,
            help="Luas lahan yang akan digunakan untuk praktik berkelanjutan"
        )
        
        practice_type = st.selectbox(
            "Jenis Praktik Berkelanjutan",
            options=["Agroforestri", "No-Till Farming", "Biochar", "Cover Crop"],
            help="Pilih jenis praktik yang akan/sudah diterapkan"
        )
        
        if practice_type == "Agroforestri":
            tree_density = st.number_input(
                "Jumlah Pohon per Hektar",
                min_value=50,
                max_value=1000,
                value=400,
                step=50,
                help="Jumlah pohon yang ditanam per hektar"
            )
        
        years = st.number_input(
            "Durasi Proyek (tahun)",
            min_value=1,
            max_value=30,
            value=10,
            step=1,
            help="Berapa lama proyek akan berjalan"
        )
        
        price_per_ton = st.number_input(
            "Harga Kredit Karbon (Rp/ton CO₂)",
            min_value=50000,
            max_value=200000,
            value=100000,
            step=10000,
            help="Estimasi harga jual kredit karbon"
        )
    
    with col2:
        st.markdown("### 🌳 Tentang Praktik")
        
        if practice_type == "Agroforestri":
            st.info("""
            **Agroforestri (Wanatani)**
            
            Kombinasi tanaman pertanian dengan pohon. Pohon menyerap CO₂ dari atmosfer dan menyimpannya dalam biomassa.
            
            ✅ **Keuntungan:**
            - Penghasilan dari kayu/buah
            - Tanah lebih subur
            - Biodiversitas meningkat
            - Kredit karbon tinggi
            
            📊 **Potensi:** 2-5 ton CO₂/ha/tahun
            """)
        
        elif practice_type == "No-Till Farming":
            st.info("""
            **No-Till Farming (Tanpa Olah Tanah)**
            
            Menanam tanpa membajak tanah. Karbon tersimpan di dalam tanah tidak terlepas ke atmosfer.
            
            ✅ **Keuntungan:**
            - Hemat biaya traktor
            - Tanah lebih sehat
            - Air tersimpan lebih baik
            - Erosi berkurang
            
            📊 **Potensi:** 0.3-0.5 ton CO₂/ha/tahun
            """)
        
        elif practice_type == "Biochar":
            st.info("""
            **Biochar (Arang Hayati)**
            
            Arang dari limbah pertanian yang dimasukkan ke tanah. Karbon tersimpan ratusan tahun.
            
            ✅ **Keuntungan:**
            - Tanah lebih subur
            - Retensi air meningkat
            - Mikroba tanah berkembang
            - Karbon stabil lama
            
            📊 **Potensi:** 4-6 ton CO₂/ha/tahun
            """)
        
        else:  # Cover Crop
            st.info("""
            **Cover Crop (Tanaman Penutup)**
            
            Menanam tanaman penutup tanah di luar musim utama. Biomassa menyerap CO₂.
            
            ✅ **Keuntungan:**
            - Tanah tidak gundul
            - Hara tidak tercuci
            - Gulma terkontrol
            - Pakan ternak (bonus)
            
            📊 **Potensi:** 3-5 ton CO₂/ha/tahun
            """)
    
    # Calculate button
    if st.button("🧮 Hitung Potensi Karbon", type="primary", use_container_width=True):
        
        # Calculate based on practice type
        if practice_type == "Agroforestri":
            result = calc.calculate_agroforestry_carbon(area_ha, tree_density, years)
        elif practice_type == "No-Till Farming":
            result = calc.calculate_no_till_carbon(area_ha, years)
        elif practice_type == "Biochar":
            result = calc.calculate_biochar_carbon(area_ha, years)
        else:  # Cover Crop
            result = calc.calculate_cover_crop_carbon(area_ha, years)
        
        # Calculate value
        value = calc.estimate_value(result['annual_co2_ton'], price_per_ton)
        
        # Display results
        st.markdown("---")
        st.markdown("### 📊 Hasil Estimasi")
        
        # Metrics
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.metric(
                "Total Karbon",
                f"{result['total_co2_ton']} ton CO₂",
                f"{years} tahun"
            )
        
        with col_m2:
            st.metric(
                "Per Tahun",
                f"{result['annual_co2_ton']} ton CO₂",
                "per tahun"
            )
        
        with col_m3:
            st.metric(
                "Nilai Total",
                f"Rp {result['total_co2_ton'] * price_per_ton:,.0f}",
                f"{years} tahun"
            )
        
        with col_m4:
            st.metric(
                "Nilai Tahunan",
                f"Rp {value['annual_value']:,.0f}",
                "per tahun"
            )
        
        # Equivalents (if available)
        if 'tree_equivalent' in result:
            st.markdown("### 🌍 Setara Dengan:")
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                st.success(f"🌳 **{result['tree_equivalent']:,.0f} pohon dewasa** yang tumbuh selama 10 tahun")
            
            with col_e2:
                st.success(f"🚗 **{result['car_km_equivalent']:,.0f} km** perjalanan mobil")
        
        # Recommendations
        st.markdown("### 💡 Langkah Selanjutnya")
        st.markdown("""
        1. **Dokumentasi**: Foto lahan, bukti kepemilikan, rencana tanam
        2. **Registrasi**: Daftarkan proyek Anda (fitur segera hadir)
        3. **Verifikasi**: Tim kami akan verifikasi via satelit
        4. **Listing**: Kredit Anda akan muncul di marketplace
        5. **Penjualan**: Terima pembayaran dari perusahaan pembeli
        
        💰 **Fee AgriSensa**: 10-15% dari nilai transaksi
        """)


# ===== TAB 2: MARKETPLACE =====
with tab2:
    st.subheader("🛒 Marketplace Kredit Karbon")
    
    st.info("""
    🚧 **Coming Soon!**
    
    Marketplace sedang dalam pengembangan. Fitur yang akan tersedia:
    
    - 🔍 Browse kredit karbon dari berbagai proyek
    - 📍 Filter berdasarkan lokasi, harga, volume
    - ✅ Verifikasi via satelit (Sentinel-2)
    - 💳 Payment gateway terintegrasi
    - 📄 Sertifikat digital otomatis
    - 🔗 Blockchain untuk transparansi (future)
    
    **Target Launch**: Q2 2025
    """)
    
    # Sample listings (mockup)
    st.markdown("### 📋 Preview: Contoh Listing")
    
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h4>🌳 Proyek Agroforestri Brebes</h4>
            <p><strong>Lokasi:</strong> Brebes, Jawa Tengah</p>
            <p><strong>Luas:</strong> 10 ha | <strong>Pohon:</strong> Mahoni, Sengon</p>
            <p><strong>Kredit Tersedia:</strong> 50 ton CO₂</p>
            <p><strong>Harga:</strong> Rp 95,000/ton</p>
            <p>✅ <em>Verified by Satellite</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_l2:
        st.markdown("""
        <div style="background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h4>🌾 Proyek No-Till Garut</h4>
            <p><strong>Lokasi:</strong> Garut, Jawa Barat</p>
            <p><strong>Luas:</strong> 5 ha | <strong>Crop:</strong> Jagung, Kedelai</p>
            <p><strong>Kredit Tersedia:</strong> 15 ton CO₂</p>
            <p><strong>Harga:</strong> Rp 85,000/ton</p>
            <p>✅ <em>Verified by Field Audit</em></p>
        </div>
        """, unsafe_allow_html=True)


# ===== TAB 3: PANDUAN =====
with tab3:
    st.subheader("📚 Panduan Carbon Credit")
    
    with st.expander("❓ Apa itu Kredit Karbon?"):
        st.markdown("""
        **Kredit Karbon** adalah sertifikat yang mewakili pengurangan atau penyerapan 1 ton CO₂ dari atmosfer.
        
        Perusahaan yang menghasilkan emisi CO₂ dapat membeli kredit karbon untuk "offset" (mengimbangi) emisi mereka.
        
        **Contoh:**
        - Pabrik menghasilkan 1000 ton CO₂/tahun
        - Pabrik beli 1000 kredit karbon dari petani
        - Emisi pabrik = "net zero" (nol bersih)
        """)
    
    with st.expander("💰 Berapa Harga Kredit Karbon?"):
        st.markdown("""
        Harga kredit karbon bervariasi tergantung:
        
        - **Jenis Proyek**: Agroforestri lebih mahal dari no-till
        - **Verifikasi**: Verified lebih mahal
        - **Lokasi**: Indonesia vs global market
        - **Buyer**: Voluntary vs compliance market
        
        **Range Harga (Indonesia):**
        - Rp 50,000 - 150,000 per ton CO₂
        - Rata-rata: Rp 100,000 per ton CO₂
        
        **Global Market:**
        - $5 - $50 per ton CO₂
        - Premium projects: >$100 per ton
        """)
    
    with st.expander("✅ Bagaimana Verifikasi Dilakukan?"):
        st.markdown("""
        AgriSensa menggunakan 2 metode verifikasi:
        
        **1. Satellite Verification (Otomatis)**
        - Data dari Sentinel-2 (ESA)
        - NDVI (Normalized Difference Vegetation Index)
        - Deteksi pertumbuhan vegetasi
        - Update setiap 5 hari
        
        **2. Field Audit (Manual)**
        - Kunjungan lapangan oleh verifier
        - Pengukuran diameter pohon
        - Soil sampling
        - Dokumentasi foto/video
        
        **Timeline:**
        - Satellite: 3-7 hari
        - Field audit: 2-4 minggu
        """)
    
    with st.expander("📋 Syarat Mendaftar Proyek"):
        st.markdown("""
        **Dokumen yang Diperlukan:**
        
        1. ✅ Bukti kepemilikan/sewa lahan
        2. ✅ Foto lahan (sebelum & sesudah)
        3. ✅ Rencana tanam (jenis pohon/praktik)
        4. ✅ Koordinat GPS lahan
        5. ✅ KTP pemilik lahan
        
        **Kriteria Proyek:**
        
        - Minimal 1 ha
        - Durasi minimal 5 tahun
        - Tidak ada deforestasi sebelumnya
        - Praktik berkelanjutan terbukti
        """)
    
    with st.expander("🌍 Dampak Lingkungan"):
        st.markdown("""
        **Manfaat Carbon Credit untuk Lingkungan:**
        
        🌳 **Reforestasi**: Jutaan pohon ditanam
        💧 **Konservasi Air**: Hutan menyimpan air
        🦋 **Biodiversitas**: Habitat satwa liar
        🌾 **Tanah Sehat**: Karbon tersimpan di tanah
        🌡️ **Climate Change**: Kurangi pemanasan global
        
        **Target Global:**
        - Net Zero 2050 (Paris Agreement)
        - Indonesia: Net Zero 2060
        - Pertanian: Kontributor utama solusi
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>💚 <strong>AgriSensa Carbon Credit Marketplace</strong></p>
    <p>Menyelamatkan Planet, Meningkatkan Profit</p>
    <p><small>Powered by IPCC Tier 1 Methodology | Verified by Sentinel-2 Satellite</small></p>
</div>
""", unsafe_allow_html=True)
