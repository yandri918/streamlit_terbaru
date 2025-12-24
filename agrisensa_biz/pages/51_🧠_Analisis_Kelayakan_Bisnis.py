import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import requests
import time
import random

st.set_page_config(page_title="Analisis Kelayakan Bisnis", page_icon="🧠", layout="wide")

# CSS Styling
st.markdown("""
<style>
    .score-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-big {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0284c7;
    }
    .metric-label {
        font-size: 1rem;
        color: #64748b;
        font-weight: 500;
    }
    .risk-high { color: #ef4444; }
    .risk-med { color: #f59e0b; }
    .risk-low { color: #10b981; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 Sistem Pendukung Keputusan (SPK) Agribisnis")
st.markdown("---")

# ==================== 1. SIDEBAR CONFIG ====================
with st.sidebar:
    st.header("⚙️ Profil Bisnis")
    
    biz_type = st.selectbox(
        "Jenis Usaha",
        ["Toko Pertanian (Farm Shop)", "Greenhouse Komersial", "Distributor Pupuk", "Pengolahan Hasil Panen", "Agrowisata", "Commercial Nursery (Pembibitan)", "Integrated Nursery & Farm Shop (Toko & Pembibitan)"],
        key="biz_type_main"
    )
    
    # VISUAL INDICATOR
    if biz_type == "Commercial Nursery (Pembibitan)":
        st.success("🧬 **Mode Nursery Aktif**: Parameter disesuaikan untuk sensitivitas bibit (Suhu Sejuk & Jalan Halus diutamakan).")
    elif biz_type == "Integrated Nursery & Farm Shop (Toko & Pembibitan)":
        st.info("🏪➕🌱 **Mode Terintegrasi**: Analisis gabungan Toko Pertanian (Omzet Harian) + Pembibitan (Seasonal). Skenario Cross-selling aktif.")
    
    location_name = st.text_input("Nama Lokasi / Area", "Kec. Pujon, Malang")
    
    st.subheader("💰 Permodalan")
    own_capital = st.number_input("Modal Sendiri (Rp)", 0, 10_000_000_000, 100_000_000, 10_000_000)
    loan_amount = st.number_input("Pengajuan Kredit (Rp)", 0, 10_000_000_000, 50_000_000, 10_000_000)
    
    total_capital = own_capital + loan_amount
    st.metric("Total Modal", f"Rp {total_capital:,.0f}")

# ==================== 2. INPUT PARAMETER (TABS) ====================
tab1, tab2, tab3, tab4, tab5, tab7, tab6 = st.tabs([
    "🌍 Lokasi & Geo",
    "🌱 Agronomi & Lahan",
    "👥 Pasar & Operasional",
    "💰 Finansial (5C)",
    "⚖️ Legal & Risiko",
    "📈 Ekon. Makro & Kebijakan",
    "📊 Laporan Final"
])

# --- TAB 1: GEO-SPASIAL ---
with tab1:
    st.subheader("📍 Analisis Lokasi & Geografis")
    
    col_geo1, col_geo2 = st.columns([1.5, 1])
    
    with col_geo1:
        st.info("Klik di peta untuk menentukan lokasi persis usaha Anda.")
        
        # Initialize default coords in session
        if 'biz_lat' not in st.session_state: st.session_state.biz_lat = -7.85
        if 'biz_lon' not in st.session_state: st.session_state.biz_lon = 112.5
        
        # Base Map
        m = folium.Map(location=[st.session_state.biz_lat, st.session_state.biz_lon], zoom_start=13)
        m.add_child(folium.LatLngPopup())
        
        folium.Marker(
            [st.session_state.biz_lat, st.session_state.biz_lon],
            popup="Lokasi Terpilih",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)
        
        st_data = st_folium(m, height=450, width="100%", key="folium_map")
        
        if st_data and st_data.get("last_clicked"):
            lat_click = st_data["last_clicked"]["lat"]
            lng_click = st_data["last_clicked"]["lng"]
            
            if (lat_click != st.session_state.biz_lat) or (lng_click != st.session_state.biz_lon):
                st.session_state.biz_lat = lat_click
                st.session_state.biz_lon = lng_click
                st.rerun()

        st.caption(f"Koordinat: {st.session_state.biz_lat:.5f}, {st.session_state.biz_lon:.5f}")
    
    with col_geo2:
        st.markdown("#### 🌦️ Parameter Lingkungan (Live)")
        
        @st.cache_data(ttl=3600)
        def get_enviro_data(lat, lon):
            try:
                url_weather = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
                r_weather = requests.get(url_weather, timeout=3).json()
                temp = r_weather.get('current_weather', {}).get('temperature', 28.0)
                
                url_elev = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
                r_elev = requests.get(url_elev, timeout=3).json()
                elevation = r_elev.get('elevation', [500])[0]
                return temp, elevation
            except:
                return 28.0, 500.0

        with st.spinner("Mengambil data satelit..."):
            real_temp, real_elev = get_enviro_data(st.session_state.biz_lat, st.session_state.biz_lon)

        m1, m2 = st.columns(2)
        with m1: st.metric("Ketinggian", f"{real_elev:.0f} mdpl")
        with m2: st.metric("Suhu", f"{real_temp:.1f}°C")
        
        # Define vars for downstream logic
        elevation = real_elev
        avg_temp = real_temp
        
        st.divider()
        road_access = st.selectbox("Aksesibilitas Jalan", ["Jalan Tanah", "Jalan Makadam", "Jalan Aspal Kecil", "Jalan Raya Provinsi", "Dekat Tol"])
        disaster_risk = st.select_slider("Risiko Bencana", options=["Sangat Rendah", "Rendah", "Sedang", "Tinggi", "Sangat Tinggi"], value="Rendah")

# --- TAB 2: AGRONOMI (NEW) ---
with tab2:
    st.subheader("🌱 Analisis Agronomi & Potensi Lahan")
    st.info("Data detail teknis lahan untuk akurasi kelayakan budidaya.")
    
    agro1, agro2 = st.columns(2)
    
    with agro1:
        st.markdown("#### 🗺️ Kluster & Sentra")
        sentra_type = st.selectbox(
            "📍 Zona Sentra Budidaya",
            ["Bukan Sentra (Pioneer)", "Sentra Padi/Palawija", "Sentra Hortikultura (Sayur)", "Sentra Buah-buahan", "Sentra Tanaman Hias", "Kawasan Industri/Perumahan"],
            help="Apakah lokasi ini sudah terkenal sebagai pusat komoditas tertentu?"
        )
        
        land_class = st.selectbox(
            "🏆 Kelas Kesesuaian Lahan (FAO)",
            ["S1 - Sangat Sesuai", "S2 - Cukup Sesuai", "S3 - Sesuai Marginal", "N - Tidak Sesuai"],
            index=1,
            help="S1: Tanpa pembatas serius. N: Memiliki pembatas permanen."
        )
        
        topography = st.selectbox("⛰️ Topografi / Kemiringan", ["Datar (0-3%)", "Landai (3-8%)", "Berombak (8-15%)", "Berbukit (>15%)"])

        # NURSERY SPECIFIC INPUTS
        if biz_type == "Commercial Nursery (Pembibitan)":
            st.markdown("---")
            st.markdown("🧬 **Kapasitas Produksi**")
            nursery_capacity = st.number_input("Target Produksi (Tray/Bulan)", 100, 100000, 1000)
            germination_rate = st.slider("Target Daya Berkecambah (%)", 70, 99, 90)

    with agro2:
        st.markdown("#### 🧪 Parameter Tanah & Air")
        
        ph_level = st.slider("Derajat Keasaman (pH Tanah)", 4.0, 9.0, 6.5, 0.1)
        
        col_soil = st.columns(3)
        with col_soil[0]:
            n_status = st.selectbox("Status N", ["Rendah", "Sedang", "Tinggi"], index=1)
        with col_soil[1]:
            p_status = st.selectbox("Status P", ["Rendah", "Sedang", "Tinggi"], index=1)
        with col_soil[2]:
            k_status = st.selectbox("Status K", ["Rendah", "Sedang", "Tinggi"], index=1)
            
        irrigation_type = st.selectbox(
            "💧 Sumber Irigasi Utama",
            ["Tadah Hujan (Non-Teknis)", "Sumur Bor / Pompa", "Irigasi Teknis (Bendungan)", "Mata Air Gravitasi"],
            index=2
        )
        
        st.divider()
        st.markdown("#### 🐛 Riwayat Hama & Penyakit (Endemik)")
        pest_risk_level = st.select_slider(
            "Tingkat Risiko Serangan Hama di Area Ini",
            options=["Nihil", "Rendah", "Sedang", "Tinggi (Endemik)", "Sangat Tinggi (Wabah)"],
            value="Rendah"
        )
        
        historical_pests = st.multiselect(
            "Jenis Hama/Penyakit yang Sering Muncul",
            ["Layu Fusarium/Bakteri", "Lalat Buah", "Thrips/Tungau", "Tikus", "Wereng", "Akar Gada", "Virus (Gemini/Kuning)", "Tidak Ada"]
        )

# --- TAB 3: PASAR & OPERASIONAL ---
with tab3:
    st.subheader("👥 Analisis Pasar & Operasional")
    
    col_mkt1, col_mkt2 = st.columns(2)
    
    with col_mkt1:
        st.markdown("#### 🎯 Potensi Pasar")
        catchment_radius = st.slider("Radius Layanan (km)", 1, 50, 5)
        farmer_count = st.number_input("Estimasi Jumlah Petani di Area (KK)", 100, 50000, 1500)
        land_area = st.number_input("Estimasi Luas Lahan Potensial (Ha)", 10, 10000, 500)
        
        st.divider()
        st.markdown("#### 🚚 Logistik & Rantai Pasok")
        dist_to_market = st.number_input("Jarak ke Pasar Induk / Terminal (km)", 1, 200, 10)
        supplier_access = st.selectbox("Akses Supplier (Pupuk/Benih)", ["Sangat Mudah (Ada di Desa)", "Sedang (Kecamatan)", "Sulit (Harus ke Kota)"])
        backup_suppliers = st.number_input("Jml Alternatif Supplier", 0, 10, 2, help="Jumlah supplier cadangan jika supplier utama kolaps")
        
        st.divider()
        st.markdown("#### 📡 Kesiapan Teknologi")
        internet_signal = st.selectbox("Sinyal Internet", ["4G/LTE Kuat", "Fiber Optic Ready", "3G/Tidak Stabil", "Blank Spot"])
        
    with col_mkt2:
        st.markdown("#### ⚔️ Kompetisi")
        competitor_count = st.number_input("Jumlah Kompetitor Direct", 0, 50, 3)
        market_growth = st.slider("Pertumbuhan Pasar Tahunan (%)", -10, 50, 10)
        unique_selling = st.multiselect("Keunggulan Kompetitif (USP)", ["Harga Murah", "Layanan Antar", "Konsultasi", "Teknologi", "Kredit", "Stok Lengkap"])
        
        # INTEGRATED SCENARIO LOGIC
        if biz_type == "Integrated Nursery & Farm Shop (Toko & Pembibitan)":
            st.markdown("---")
            st.markdown("#### 🔄 Simulasi Terintegrasi (Toko + Bibit)")
            st.caption("Hitung potensi 'Cross-Selling': Menjual bibit sendiri ke pelanggan toko.")
            
            w_col1, w_col2 = st.columns(2)
            with w_col1:
                target_lahan_ha = st.number_input("Target Luas Lahan Pelanggan (Ha)", 1, 1000, 50, help="Total luas lahan milik pelanggan tetap toko Anda.")
                populasi_per_ha = st.number_input("Rata-rata Populasi/Ha", 10000, 50000, 20000, help="Misal Cabai/Tomat ~20rb populasi.")
            
            with w_col2:
                capture_rate = st.slider("Target Market Share Bibit (%)", 5, 100, 20, help="Berapa % pelanggan toko yg akan beli bibit dari Anda?")
                margin_bibit = st.number_input("Margin Profit per Bibit (Rp)", 50, 2000, 200, help="Keuntungan bersih per tanaman.")
            
            # Calculation
            total_market_bibit = target_lahan_ha * populasi_per_ha
            captured_bibit = total_market_bibit * (capture_rate / 100)
            potential_profit_nursery = captured_bibit * margin_bibit
            
            st.info(f"""
            **Analisis Potensi Sinergi:**
            - Total Kebutuhan Pasar: **{int(total_market_bibit):,} bibit/musim**
            - Target Penjualan Anda: **{int(captured_bibit):,} bibit**
            - 💰 **Potensi Profit Tambahan Nursery: Rp {int(potential_profit_nursery):,}/musim**
            """)
        
        st.divider()
        st.markdown("#### 👷 Ketenagakerjaan")
        labor_avail = st.select_slider("Ketersediaan Tenaga Kerja Tani", ["Sangat Langka", "Langka", "Cukup", "Melimpah"], value="Cukup")
        labor_cost = st.number_input("Upah Harian Rata-rata (Rp)", 50_000, 250_000, 80_000, 5_000)
        
        st.divider()
        st.markdown("#### 🛡️ Risiko Non-Teknis (Advance)")
        rtrw_zone = st.selectbox("Zona Tata Ruang (RTRW)", ["Hijau (Pertanian)", "Kuning (Pemukiman)", "Merah (Kawasan Lindung/Rawan)"])
        social_risk = st.selectbox("Risiko Sosial/Keamanan", ["Aman Kondusif", "Rawan Pencurian", "Sering Konflik Lahan"])

# --- TAB 4: FINANSIAL (5C) ---
with tab4:
    st.subheader("💰 Analisis Kelayakan Kredit (Metode 5C)")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 1. Character & Capacity")
        exp_years = st.number_input("Pengalaman Usaha (Tahun)", 0, 50, 5)
        mgmt_team = st.selectbox("Kualitas Tim", ["One Man Show", "Ada Tim Kecil", "Profesional Lengkap"])
        credit_history = st.selectbox("Riwayat Kredit (SLIK)", ["Belum Ada", "Pernah Nunggak", "Lancar", "Sangat Baik"])
    with c2:
        st.markdown("#### 2. Capital, Collateral & Condition")
        der = (loan_amount / own_capital) if own_capital > 0 else 99
        st.metric("Debt to Equity Ratio", f"{der:.2f}x")
        collateral_value = st.number_input("Nilai Agunan (Rp)", 0, 50_000_000_000, 100_000_000)
        coverage_ratio = (collateral_value / loan_amount * 100) if loan_amount > 0 else 100
        st.progress(min(coverage_ratio/200, 1.0), text=f"Coverage: {coverage_ratio:.1f}%")
        economic_cond = st.selectbox("Kondisi Ekonomi", ["Resesi", "Stabil", "Bertumbuh"], index=2)

# --- TAB 5: LEGAL (Duplicate Removed, already in Tabs List but logic below) ---
with tab5:
    st.subheader("⚖️ Legalitas & Risiko")
    legal_docs = st.multiselect("Dokumen Legal", ["NIB", "NPWP", "Izin Lokasi", "AMDAL", "Sertifikat Halal", "Akta PT/CV"])
    social_accept = st.select_slider("Penerimaan Warga", options=["Menolak", "Netral", "Mendukung", "Sangat Mendukung"], value="Mendukung")

# --- TAB 7: EKONOMI MAKRO & KEBIJAKAN (NEW) ---
with tab7:
    st.subheader("📈 Analisis Ekonomi Makro & Kebijakan")
    st.info("Parameter profesional untuk analisis dampak lingkungan ekonomi eksternal dan kebijakan pemerintah.")
    
    ec1, ec2 = st.columns(2)
    
    with ec1:
        st.markdown("#### 🌏 Indikator Makroekonomi")
        inflation_rate = st.number_input("Tingkat Inflasi Tahunan (%)", 0.0, 20.0, 3.5, 0.1, help="Inflasi tinggi menggerus daya beli dan meningkatkan biaya input.")
        gdp_growth = st.number_input("Pertumbuhan Ekonomi Regional (%)", -5.0, 15.0, 5.0, 0.1, help="Korelasi positif dengan demand produk sekunder/tersier.")
        bi_rate = st.number_input("Suku Bunga Acuan (BI Rate) %", 2.0, 15.0, 6.0, 0.25, help="Basis perhitungan Cost of Fund untuk kredit.")
        exchange_rate_volatility = st.selectbox("Volatilitas Kurs (IDR/USD)", ["Stabil", "Fluktuatif Sedang", "Sangat Gejolak"], help="Penting jika Anda menggunakan pupuk impor atau orientasi ekspor.")
        
    with ec2:
        st.markdown("#### 🏛️ Kebijakan Pemerintah")
        gov_support = st.multiselect("Dukungan Pemerintah Sektor Ini", ["Subsidi Pupuk/Pakan", "Bantuan Alsintan", "KUR (Bunga Rendah)", "Proteksi Impor", "Tax Allowance/Holiday"])
        import_policy = st.selectbox("Kebijakan Perdagangan", ["Bebas Impor (Kompetisi Tinggi)", "Pembatasan Impor (Proteksi)", "Netral"])
        
        st.divider()
        st.markdown("#### 🔬 Struktur Pasar (Mikro)")
        market_structure = st.selectbox("Struktur Persaingan Industri", 
            ["Persaingan Sempurna (Banyak Penjual/Pembeli)", "Oligopoli (Dikuasai Pemain Besar)", "Monopoli (Dikuasai 1 Pihak)", "Niche Market (Spesifik)"],
            help="Menentukan Pricing Power Anda."
        )
        price_elasticity = st.selectbox("Elastisitas Harga Produk", ["Inelastis (Bebutuhan Pokok)", "Elastis (Barang Mewah/Sekunder)"], help="Inelastis: Harga naik, orang tetap beli (Padi/Jagung). Elastis: Harga naik, orang kurangi beli (Bunga/Buah Mahal).")

# --- TAB 6: REPORT & INTELLIGENCE ---
with tab6:
    st.subheader("📊 Laporan Analisis & Simulasi Cerdas")
    
    # --- 1. SCORING ENGINE FUNCTION ---
    def calculate_raw_metrics(params):
        # Helper to calc score for any biz type
        s = {}
        
        # A. GEO
        geo = 0
        if params['road'] in ["Jalan Raya Provinsi", "Dekat Tol"]: geo += 40
        elif params['road'] == "Jalan Aspal Kecil": geo += 30
        else: geo += 15
        if params['disaster'] in ["Sangat Rendah", "Rendah"]: geo += 30
        else: geo -= 10
        # Agrowisata specific
        if params['type'] == "Agrowisata":
            if params['elev'] > 800: geo += 30
        if params['type'] == "Commercial Nursery (Pembibitan)":
             # Nursery needs cool climate or adaptable
            if params['elev'] > 500: geo += 15
            # Nursery needs good road for transporting fragile seedlings
            if params['road'] == "Jalan Tanah": geo -= 20
        
        # Integrated specific
        if params['type'] == "Integrated Nursery & Farm Shop (Toko & Pembibitan)":
            # Very strong model if road is good (customers come) + climate good
            if params['road'] in ["Jalan Raya Provinsi", "Dekat Tol"]: geo += 10
            if params['elev'] > 400: geo += 10 
        
        s['Geografis'] = min(geo + 20, 100)
        
        # B. AGRONOMY
        agro = 0
        if params['land'] == "S1 - Sangat Sesuai": agro += 40
        elif params['land'] == "S2 - Cukup Sesuai": agro += 30
        
        # Greenhouse tech bonus
        if params['type'] == "Greenhouse Komersial": agro += 20
        # Nursery tech bonus (needs clean environment)
        if params['type'] == "Commercial Nursery (Pembibitan)": agro += 10
        if params['type'] == "Integrated Nursery & Farm Shop (Toko & Pembibitan)": agro += 15 # Synergy efficiency
        
        # Pest Penalty
        if params['pest'] == "Tinggi (Endemik)": 
            agro -= 15 if params['type'] != "Greenhouse Komersial" else 5
        elif params['pest'] == "Sangat Tinggi (Wabah)": 
            agro -= 30 if params['type'] != "Greenhouse Komersial" else 10
            
        s['Agronomi'] = max(0, min(agro + 20, 100))
        
        # C. PASAR & OPS
        ops = 0
        mkt_base = (params['farmers']/100) + (params['area']/10)
        ops += min(mkt_base, 30)
        ops += max(20 - (params['competitor']*5), 0)
        
        # Labor
        if params['labor_av'] in ["Cukup", "Melimpah"]: ops += 10
        elif params['labor_av'] == "Sangat Langka": ops -= 15
        
        # Logistics
        if params['dist_mkt'] < 20: ops += 10
        if params['supplier'] == "Sangat Mudah (Ada di Desa)": ops += 10
        
        # Tech
        if params['inet'] in ["4G/LTE Kuat", "Fiber Optic Ready"]: ops += 10
        
        s['PasarOps'] = min(ops + 10, 100)
        
        # D. FINANCIAL
        fin = 0
        if params['credit'] == "Sangat Baik": fin += 30
        if params['der'] < 2.0: fin += 25
        if params['cov'] >= 110: fin += 25
        s['Finansial'] = min(fin, 100)
        
        # E. LEGAL & RISK
        leg = 50
        if params['zone'] == "Hijau (Pertanian)": leg += 30
        elif params['zone'] == "Merah (Kawasan Lindung/Rawan)": leg -= 80
        if params['social'] == "Sering Konflik Lahan": leg -= 40
        s['Legal'] = max(0, min(leg, 100))
        
        # F. EKONOMI & KEBIJAKAN (NEW)
        eco = 50 # Base neutral
        
        # Macro
        if params['gdp'] > 5.0: eco += 10
        if params['inflasi'] > 5.0: eco -= 10 # High inflation penalty
        elif params['inflasi'] < 2.0: eco -= 5 # Deflation risk (low demand)
        
        # Policy
        eco += len(params['gov']) * 10
        if params['import'] == "Pembatasan Impor (Proteksi)": eco += 15
        elif params['import'] == "Bebas Impor (Kompetisi Tinggi)": eco -= 10
        
        # Micro
        if params['struk'] == "Niche Market (Spesifik)": eco += 20 # High pricing power
        elif params['struk'] == "Persaingan Sempurna (Banyak Penjual/Pembeli)": eco += 0 # Neutral, price taker
        elif params['struk'] == "Oligopoli (Dikuasai Pemain Besar)": eco -= 10 # Hard to enter
        
        s['Ekonomi'] = max(0, min(eco, 100))
        
        return s

    # Gather Current Params
    current_params = {
        'type': biz_type,
        'road': road_access, 'disaster': disaster_risk, 'elev': elevation if 'elevation' in locals() else 500,
        'land': land_class, 'pest': pest_risk_level,
        'farmers': farmer_count, 'area': land_area, 'competitor': competitor_count,
        'dist_mkt': dist_to_market if 'dist_to_market' in locals() else 10, 
        'supplier': supplier_access if 'supplier_access' in locals() else "Sedang",
        'labor_av': labor_avail if 'labor_avail' in locals() else "Cukup", 
        'inet': internet_signal if 'internet_signal' in locals() else "4G/LTE Kuat",
        'credit': credit_history, 'der': der, 'cov': coverage_ratio,
        'zone': rtrw_zone if 'rtrw_zone' in locals() else "Hijau (Pertanian)", 
        'social': social_risk if 'social_risk' in locals() else "Aman Kondusif",
        # New Economic Params
        'inflasi': inflation_rate, 'gdp': gdp_growth, 'gov': gov_support,
        'import': import_policy, 'struk': market_structure,
        # Integrated Params (Safeguarded with .get or default)
        'target_lahan': target_lahan_ha if 'target_lahan_ha' in locals() else 0,
        'capture_rate': capture_rate if 'capture_rate' in locals() else 0,
        'margin_bibit': margin_bibit if 'margin_bibit' in locals() else 0,
        'populasi_ha': populasi_per_ha if 'populasi_per_ha' in locals() else 0
    }
    
    # Calculate Scores
    scores_current = calculate_raw_metrics(current_params)
    
    # Weighting (Updated)
    weights = {
        'Geografis': 0.15, 'Agronomi': 0.20, 'PasarOps': 0.20, 
        'Finansial': 0.20, 'Legal': 0.10, 'Ekonomi': 0.15
    }
    final_score = sum(scores_current[k] * weights[k] for k in scores_current)
    
    # --- LAYOUT UPPER ---
    r1, r2 = st.columns([1, 1.5])
    
    with r1:
        st.markdown(f"""
        <div class="score-card">
            <div class="metric-label">SKOR KELAYAKAN ({biz_type})</div>
            <div class="metric-big" style="color: {'#10b981' if final_score >= 75 else '#f59e0b' if final_score >= 50 else '#ef4444'}">
                {final_score:.1f}
            </div>
            <div style="margin-top: 10px; font-weight: bold;">
                {'✅ RECOMMENDED' if final_score >= 75 else '⚠️ WARNING' if final_score >= 50 else '❌ HIGH RISK'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Kesimpulan & Saran AI")
        
        # Generic Logic
        if final_score >= 75:
            base_msg = "✅ **GO PROJECT!** Lokasi dan kondisi makro sangat mendukung."
        elif final_score >= 50:
            base_msg = "⚠️ **PROCEED WITH CAUTION.** Perlu strategi mitigasi di aspek skor rendah."
        else:
            base_msg = "❌ **NO GO.** Risiko terlalu tinggi, cari lokasi atau model bisnis lain."
            
        st.write(base_msg)
        
        # Integrated Specific Insight
        if current_params['type'] == "Integrated Nursery & Farm Shop (Toko & Pembibitan)":
            potensi_bibit = (current_params['target_lahan'] * current_params['populasi_ha']) * (current_params['capture_rate']/100) * current_params['margin_bibit']
            st.info(f"""
            💡 **Insight Skenario Terintegrasi:**
            AI mendeteksi potensi **Additional Income Rp {int(potensi_bibit/1000_000):,} Juta** per musim dari penjualan bibit ke pelanggan toko.
            
            **Saran:** Fokuskan marketing pada bundling "Beli Pupuk Gratis Konsultasi Bibit" untuk mencapai capture rate {current_params['capture_rate']}%.
            """)

    with r2:
        # --- COMPARATIVE ANALYSIS ---
        st.markdown("#### 🆚 Perbandingan Peluang Usaha")
        other_types = ["Toko Pertanian (Farm Shop)", "Greenhouse Komersial", "Distributor Pupuk", "Pengolahan Hasil Panen", "Agrowisata", "Commercial Nursery (Pembibitan)"]
        comp_res = []
        
        for ot in other_types:
            p = current_params.copy()
            p['type'] = ot
            s = calculate_raw_metrics(p)
            f = sum(s[k] * weights[k] for k in s)
            comp_res.append({'Jenis': ot, 'Skor': f})
            
        df_comp = pd.DataFrame(comp_res).sort_values('Skor', ascending=True)
        colors = ['#0284c7' if x == biz_type else '#cbd5e1' for x in df_comp['Jenis']]
        # Green for winner
        max_s = df_comp['Skor'].max()
        colors = ['#10b981' if s == max_s else c for s, c in zip(df_comp['Skor'], colors)]
        
        fig = go.Figure(go.Bar(
            x=df_comp['Skor'], y=df_comp['Jenis'], orientation='h',
            marker_color=colors, text=df_comp['Skor'].apply(lambda x: f"{x:.1f}")
        ))
        fig.update_layout(height=250, margin=dict(l=0, r=0, t=0, b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    
    # --- MONTE CARLO SIMULATION ---
    st.subheader("🎲 Simulasi Risiko (Monte Carlo Analysis)")
    
    st.markdown("""
    **Apa itu Monte Carlo?**  
    Teknik ini memprediksi **masa depan bisnis Anda dalam 1.000 skenario berbeda**.  
    Di dunia nyata, harga bisa jatuh, hama bisa menyerang, dan cuaca bisa ekstrem. Simulasi ini mengacak semua faktor risiko tersebut untuk melihat:
    1.  **Seberapa besar peluang Anda BANGKRUT?**
    2.  **Seberapa besar peluang Anda SUKSES BESAR?**
    """)
    
    if st.button("Jalankan Simulasi Risiko", type="primary"):
        with st.spinner("Mengacak 1.000 kemungkinan kejadian (Hama, Cuaca, Harga)..."):
            sim_scores = []
            
            # Risk Volatility Logic
            # Base volatility
            risk_volatility = 10 
            
            # Penalties increase volatility (uncertainty)
            if disaster_risk != "Rendah": risk_volatility += 10
            if pest_risk_level in ["Tinggi (Endemik)", "Sangat Tinggi (Wabah)"]: risk_volatility += 15
            if economic_cond == "Resesi": risk_volatility += 10
            
            for _ in range(1000):
                # Randomize key factors (Normal Distribution)
                noise = np.random.normal(0, risk_volatility)
                sim_score = min(100, max(0, final_score + noise))
                sim_scores.append(sim_score)
            
            # Analytics
            success_prob = sum(1 for x in sim_scores if x >= 70) / 10
            worst_case = np.percentile(sim_scores, 5) # 5th percentile
            best_case = np.percentile(sim_scores, 95) # 95th percentile
            
            st.divider()
            
            mc1, mc2 = st.columns([2, 1.2])
            with mc1:
                fig_mc = go.Figure(data=[go.Histogram(
                    x=sim_scores, 
                    nbinsx=40, 
                    marker_color='#3b82f6',
                    opacity=0.75,
                    name='Distribusi Skor'
                )])
                fig_mc.add_vline(x=70, line_dash="dash", line_color="#10b981", annotation_text="Target Aman (70)", annotation_position="top right")
                fig_mc.add_vline(x=50, line_dash="dot", line_color="#ef4444", annotation_text="Batas Bahaya (50)", annotation_position="top left")
                
                fig_mc.update_layout(
                    title="Peta Probabilitas Nasib Bisnis Anda",
                    xaxis_title="Kemungkinan Skor Akhir",
                    yaxis_title="Frekuensi Kejadian",
                    height=350,
                    margin=dict(t=50, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_mc, use_container_width=True)
            
            with mc2:
                st.markdown("#### 📊 Ringkasan Risiko")
                
                st.metric(
                    "Peluang Sukses (>70)", 
                    f"{success_prob:.1f}%",
                    help="Persentase kemungkinan skor Anda tetap di atas 70 meski kondisi buruk terjadi."
                )
                
                st.metric(
                    "Skenario Terburuk (Bad Day)", 
                    f"{worst_case:.1f}",
                    delta=f"{worst_case - final_score:.1f}",
                    help="Skor Anda jika hama menyerang & harga anjlok (probabilitas 5% terburuk)."
                )
                
                st.metric(
                    "Skenario Terbaik (Lucky Day)", 
                    f"{best_case:.1f}",
                    delta=f"{best_case - final_score:.1f}",
                    help="Skor Anda jika panen raya & harga tinggi (probabilitas 5% terbaik)."
                )
                
                if success_prob >= 80:
                    st.success("✅ **Investasi Sangat Aman**\nMeskipun badai datang, bisnis ini kemungkinan besar tetap untung.")
                elif success_prob >= 50:
                    st.warning("⚠️ **Perlu Cadangan Modal**\nAda risiko 50:50 bisnis ini performanya drop di bawah standar saat kondisi sulit.")
                else:
                    st.error("❌ **Spekulasi Tinggi**\nTerlalu berbahaya. Kemungkinan besar gagal jika ada sedikit saja gangguan.")

    st.divider()
    
    # --- ADVANCED VISUALIZATION (BI) ---
    with st.expander("📈 Visualisasi Lanjutan (Advanced BI)", expanded=True):
        st.subheader("Analisis Sensitivitas & Break-Even")
        
        bi1, bi2 = st.columns(2)
        
        with bi1:
            st.markdown("#### 🔥 Heatmap Sensitivitas Profit")
            st.caption("Apa yang terjadi jika **Biaya Operasional Naik** vs **Harga Jual Turun**?")
            
            # Data for Heatmap
            x_price = [0.8, 0.9, 1.0, 1.1, 1.2] # Price variation
            y_cost = [0.8, 0.9, 1.0, 1.1, 1.2] # Cost variation
            z_profit = []
            
            base_profit = total_capital * 0.2 # Dummy profit calc
            
            for c in y_cost:
                row = []
                for p in x_price:
                    # Simulated profit impact
                    # Higher Price (p>1) = Higher Profit
                    # Higher Cost (c>1) = Lower Profit
                    factor = (p * 1.5) - (c * 0.5) 
                    val = base_profit * factor
                    row.append(val)
                z_profit.append(row)
                
            fig_heat = go.Figure(data=go.Heatmap(
                z=z_profit,
                x=["-20%", "-10%", "Normal", "+10%", "+20%"],
                y=["-20%", "-10%", "Normal", "+10%", "+20%"],
                colorscale='RdBu', 
                colorbar=dict(title='Margin Keuntungan')
            ))
            
            fig_heat.update_layout(
                title="Zona Aman Bisnis (Safety Zone)",
                xaxis_title="Perubahan Harga Jual",
                yaxis_title="Perubahan Biaya Operasional",
                height=350
            )
            st.plotly_chart(fig_heat, use_container_width=True)
            st.caption("ℹ️ **Cara Baca:** Area **Biru** adalah zona aman (Untung). Area **Merah** adalah zona bahaya (Rugi).")
            
        with bi2:
            st.markdown("#### 📉 Break-Even Point (BEP) Simulator")
            st.caption("Titik di mana Modal Balik (Revenue = Cost)")
            
            # Simple BEP Simulation
            units = np.linspace(0, 10000, 100)
            fixed_cost = total_capital * 0.1 # Assumed 10% capex as fixed op cost equivalent
            var_cost_per_unit = 15000
            price_per_unit = 25000
            
            total_revenue = units * price_per_unit
            total_cost = fixed_cost + (units * var_cost_per_unit)
            
            fig_bep = go.Figure()
            fig_bep.add_trace(go.Scatter(x=units, y=total_revenue, name="Pendapatan (Revenue)", line=dict(color='green')))
            fig_bep.add_trace(go.Scatter(x=units, y=total_cost, name="Total Biaya (Cost)", line=dict(color='red', dash='dash')))
            
            # Find intersection
            bep_unit = fixed_cost / (price_per_unit - var_cost_per_unit)
            
            fig_bep.add_vline(x=bep_unit, line_dash="dot", annotation_text=f"BEP: {int(bep_unit):,} Unit")
            
            fig_bep.update_layout(
                title="Titik Impas (BEP)",
                xaxis_title="Volume Penjualan (Unit)",
                yaxis_title="Nilai (Rp)",
                height=350,
                showlegend=True
            )
            st.plotly_chart(fig_bep, use_container_width=True)
            st.info(f"💡 Anda harus menjual minimal **{int(bep_unit):,} unit** produk agar balik modal operasional.")

    st.divider()

    # --- INVENTORY MIX STRATEGY ---
    with st.expander("📦 Strategi Inventori & Diversifikasi Produk (Cashflow Optimizer)", expanded=True):
        st.subheader("Rekomendasi Proporsi Barang & Cross-Selling")
        st.info("Berdasarkan kondisi ekonomi makro (Inflasi/Daya Beli) dan profil risiko lokasi, berikut adalah komposisi stok yang disarankan untuk memaksimalkan profit sekaligus menjaga arus kas harian.")
        
        inv1, inv2 = st.columns([1.5, 1])
        
        with inv2:
            st.markdown("#### 🛒 Analisis Proporsi")
            
            # Logic for Inventory Mix
            # Base Mix
            pct_main = 50 # Core (Pupuk/Benih)
            pct_secondary = 30 # Tools/Pesticide
            pct_diversify = 20 # Sembako/Consumer
            
            # Adjust based on Macro
            if inflation_rate > 5.0:
                # High inflation: People buy only essentials
                pct_main += 15
                pct_secondary -= 10
                pct_diversify -= 5
                inv_note = "Inflasi tinggi! Fokus ke barang Inelastis (Pupuk/Benih Utama)."
            elif gdp_growth > 6.0:
                # High Growth: People buy hobbies/premium
                pct_main -= 10
                pct_secondary += 20
                pct_diversify -= 10
                inv_note = "Ekonomi tumbuh! Perbanyak stok Alat Modern & Hobi."
            else:
                inv_note = "Kondisi stabil. Pertahankan bauran produk seimbang."
            
            # Adjust based on Location Risk (If risk high, need fast cash from Sembako)
            if final_score < 60:
                pct_diversify += 15
                pct_main -= 10
                pct_secondary -= 5
                inv_note += " Risiko bisnis agak tinggi, perbesar porsi Sembako untuk Cashflow harian aman."
                
            # Normalize
            total_pct = pct_main + pct_secondary + pct_diversify
            pct_main = (pct_main / total_pct) * 100
            pct_secondary = (pct_secondary / total_pct) * 100
            pct_diversify = (pct_diversify / total_pct) * 100
            
            st.write(f"**Strategi:** {inv_note}")
            
            # Specific Items
            st.markdown("**Top 3 Barang Tambahan (Sembako/Lainnya):**")
            if 'farmer_count' in locals() and farmer_count > 2000:
                st.markdown("1. 🍚 **Beras & Minyak Goreng**: Traffic generator utama bagi keluarga petani.")
            else:
                st.markdown("1. ☕ **Kopi Sachet & Minuman Dingin**: Wajib ada jika lokasi dekat lahan kerja.")
                
            if internet_signal == "Blank Spot":
                st.markdown("2. 🎟️ **Pulsa & Token Listrik**: Sangat dicari di area minim sinyal/akses.")
            else:
                st.markdown("2. 💊 **Obat Pertanian Ringan (P3K)**: Margin tinggi.")
                
            st.markdown("3. ⛽ **BBM Eceran (Pertamini)**: Jika jauh dari SPBU (>5km), ini adalah 'Emas Hitam'.")

        with inv1:
            # Pie Chart
            labels = ['Produk Utama (Pupuk/Benih)', 'Pendukung (Alat/Obat)', 'Diversifikasi (Sembako/FMCG)']
            values = [pct_main, pct_secondary, pct_diversify]
            colors = ['#10b981', '#3b82f6', '#f59e0b']
            
            fig_inv = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, marker_colors=colors)])
            fig_inv.update_layout(title="Rekomendasi Bauran Stok (Inventory Mix)", height=300, margin=dict(t=30, b=0))
            st.plotly_chart(fig_inv, use_container_width=True)
