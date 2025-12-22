import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from datetime import datetime

# Page Config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Agrowisata Petik Langsung Pro",
    page_icon="🍓",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .status-card {
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #ff4b4b;
        background-color: white;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🍓 Agrowisata Petik Langsung Premium V2")
st.markdown("""
**Transformasi Lahan Menjadi Destinasi Wisata Bernilai Tinggi!**
Modul ini menggabungkan konsep *Experience Economy* dengan *High-Precision Agriculture*. 
Fokus pada integrasi: **Tourism, Production, and Nursery (Yamasa Style).**
""")

st.markdown("---")

# TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📍 Analisis Kelayakan",
    "🍇 Panduan Komoditas", 
    "💰 Bisnis & ROI",
    "📋 Manajemen & SOP",
    "📅 Kalender Ops",
    "🌱 Yamasa Nursery",
    "🏛️ Masterplan & Edu",
    "📡 IoT Smart Farm"
])

# --- TAB 1: ANALISIS KELAYAKAN ---
with tab1:
    st.header("📍 Cek Kesesuaian & Skor Kelayakan")
    st.caption("Gunakan data presisi untuk meminimalkan risiko investasi.")
    
    col_loc1, col_loc2 = st.columns([1, 2])
    
    with col_loc1:
        st.subheader("🛠️ Parameter Lingkungan")
        altitude = st.number_input("Ketinggian Lokasi (mdpl)", 0, 3000, 500, step=50)
        temp_avg = st.slider("Rata-rata Suhu Harian (°C)", 10, 40, 25)
        soil_ph = st.slider("pH Tanah", 3.0, 9.0, 6.0, 0.1)
        humidity = st.slider("Kelembaban Rata-rata (%)", 30, 100, 70)
        
    with col_loc2:
        st.subheader("📊 Hasil Analisis Spesifik")
        
        # Scoring Logic (Simplified)
        score_strawberry = 0
        if altitude >= 1000: score_strawberry += 40
        elif 700 <= altitude < 1000: score_strawberry += 20
        
        if 15 <= temp_avg <= 22: score_strawberry += 30
        if 5.5 <= soil_ph <= 6.5: score_strawberry += 20
        if humidity >= 70: score_strawberry += 10
        
        score_melon = 0
        if altitude < 700: score_melon += 30
        if 25 <= temp_avg <= 32: score_melon += 40
        if 6.0 <= soil_ph <= 7.0: score_melon += 20
        if humidity <= 75: score_melon += 10

        score_grapes = 0
        if altitude < 1000: score_grapes += 30
        if 25 <= temp_avg <= 35: score_grapes += 40
        if 6.0 <= soil_ph <= 7.5: score_grapes += 20
        if humidity <= 70: score_grapes += 10

        # Display Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Strawberry Suitability", f"{score_strawberry}%")
        m2.metric("Melon Suitability", f"{score_melon}%")
        m3.metric("Grapes Suitability", f"{score_grapes}%")

        # Gauge Chart
        fig_score = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = max(score_strawberry, score_melon, score_grapes),
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Highest Feasibility Score"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps' : [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "gray"},
                    {'range': [80, 100], 'color': "limegreen"}],
            }
        ))
        fig_score.update_layout(height=300)
        st.plotly_chart(fig_score, use_container_width=True)

        if max(score_strawberry, score_melon, score_grapes) < 50:
            st.error("⚠️ Lokasi ini memiliki tantangan tinggi. Disarankan menggunakan Greenhouse dengan kontrol iklim total.")
        elif max(score_strawberry, score_melon, score_grapes) < 80:
            st.warning("✅ Lokasi cukup baik, namun perlu penyesuaian teknis di beberapa parameter.")
        else:
            st.success("⭐ LOKASI PRIMA! Potensi hasil maksimal dengan input minimal.")

# --- TAB 2: PANDUAN TANAMAN ---
with tab2:
    st.header("🍇 Panduan Komoditas Agrowisata")
    
    # 1. Anggur
    with st.expander("🍇 Anggur Import (Industrial Scale)", expanded=True):
        st.markdown("""
        **Transformasi Produksi:** Dari hobi menjadi industri berbasis data.
        
        *   **Varietas High-Value:** 
            *   *Shine Muscat:* Tekstur crunchy, aroma muscat kuat, harga premium.
            *   *Tamaki:* Sangat manis, kulit tipis.
            *   *Autumn Royal:* Tanpa biji (seedless), buah besar hitam.
        *   **Parameter Kualitas (Target Industri):**
            *   **Brix Level:** Min 18-22% (Sangat Manis).
            *   **Firmness:** Buah harus garing/crunchy (tidak lembek).
            *   **Uniformity:** Berat dompolan seragam 500-800 gram.
        *   **Sistem Konstruksi:** 
            *   *Y-System:* Sirkulasi udara maksimal, mudah perawatan.
            *   *T-System:* Estetik, buah menggantung rapi untuk wisata.
        """)
        
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.info("**Scientific Parameter - Vegetatif:**\n- EC Nutrisi: 1.2 - 1.5 mS/cm\n- pH: 5.5 - 6.5\n- Humidity: 60-70%")
        with col_g2:
            st.success("**Scientific Parameter - Generatif:**\n- EC Nutrisi: 2.0 - 2.5 mS/cm\n- Target Brix: >18%\n- Humidity: 50-60%")
        
    # 2. Melon
    with st.expander("🍈 Melon Premium (Eksklusif)", expanded=False):
        st.markdown("""
        **Kenapa Melon?** Kesan mewah, panen serentak, rasa sangat manis (Honey Globe/Golden).
        
        *   **Varietas:** Intanon (Kulit kuning net), Fujisawa, Golden Aroma.
        *   **Sistem Tanam:** Hidroponik Fertigasi (Drip) di Polybag.
        *   **Kaya Visual:** Sistem *Single Stem* (satu pohon satu buah) yang digantung rapi sangat indah difoto.
        *   **Kunci Sukses:** Greenhouse steril (Insect Net) untuk cegah lalat buah.
        """)
        
    # 3. Strawberry
    with st.expander("🍓 Strawberry (Everlasting Favorite)", expanded=False):
        st.markdown("""
        **Kenapa Strawberry?** Ikon agrowisata keluarga. Anak-anak sangat suka memetiknya.
        
        *   **Varietas:** Mencir (Tahan agak panas), California (Besar), Sweet Charlie (Manis).
        *   **Sistem Tanam:** 
            *   *Polybag Bertingkat (Gunungan):* Hemat tempat, estetik.
            *   *Gantung (Hanging):* Unik, buah tidak kotor kena tanah.
        *   **Kunci Sukses:** Pupuk Kalium tinggi saat berbunga, buang sulur (runner) agar fokus ke buah.
        """)
        
    # 4. Bunga & Refugia (Moved to end)
    with st.expander("🌻 Bunga Estetik & Refugia (Wajib Ada!)", expanded=False):
        st.markdown("""
        **Fungsi Ganda:** Spot Selfie + Rumah Predator Alami.
        *   **Marigold/Kenikir:** Usir nematoda tanah & kutu kebul.
        *   **Zinnia/Matahari:** Menarik polinator & musuh alami ulat.
        """)

# --- TAB 3: BISNIS & ROI ---
with tab3:
    st.header("💰 Simulasi Investasi & Keuntungan")
    st.info("Agrowisata adalah bisnis padat modal di awal, namun memiliki margin tinggi karena menjual 'pengalaman'.")
    
    # Simulation Mode
    sim_mode = st.radio("Skenario Simulasi", ["Konservatif", "Moderat", "Optimis"], horizontal=True)
    multiplier = {"Konservatif": 0.8, "Moderat": 1.0, "Optimis": 1.3}
    
    col_biz1, col_biz2 = st.columns(2)
    
    with col_biz1:
        st.subheader("🏗️ Investasi Awal (CAPEX)")
        gh_size = st.number_input("Luas Greenhouse (m2)", 0, 10000, 500)
        gh_cost_m2 = st.number_input("Biaya Bangun GH (Rp/m2)", 0, 1000000, 350000)
        system_cost = st.number_input("Sistem Irigasi & Media (Total Rp)", 0, 500000000, 50000000)
        legal_marketing = st.number_input("Legalitas & Branding (Rp)", 0, 100000000, 25000000)
        
        capex_total = (gh_size * gh_cost_m2) + system_cost + legal_marketing
        st.markdown(f"**Total CAPEX: Rp {capex_total:,.0f}**")

    with col_biz2:
        st.subheader("🎟️ Target Operasional (Bulanan)")
        htm_price = st.number_input("Harga Tiket Masuk (Rp)", 0, 100000, 20000)
        visitors_month = st.number_input("Target Pengunjung / Bulan", 0, 10000, 1000) * multiplier[sim_mode]
        fruit_sales_kg = st.number_input("Rata-rata Beli Buah (kg/orang)", 0.0, 5.0, 0.7)
        fruit_price = st.number_input("Harga Jual Buah (Rp/kg)", 0, 200000, 100000)
        
        st.subheader("💸 Biaya Operasional (OPEX/Bulan)")
        labor_cost = st.number_input("Tenaga Kerja (Rp/Bulan)", 0, 100000000, 15000000)
        utility_fert = st.number_input("Listrik & Pupuk (Rp/Bulan)", 0, 50000000, 7000000)
        opex_total = labor_cost + utility_fert
        
    # Financial Analysis
    st.markdown("---")
    rev_ticket = visitors_month * htm_price
    rev_fruit = visitors_month * fruit_sales_kg * fruit_price
    revenue_month = rev_ticket + rev_fruit
    profit_month = revenue_month - opex_total
    
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue/Bulan", f"Rp {revenue_month:,.0f}")
    m2.metric("Profit/Bulan", f"Rp {profit_month:,.0f}")
    
    # Payback Period Calculation
    if profit_month > 0:
        payback_months = capex_total / profit_month
        m3.metric("Payback Period", f"{payback_months:.1f} Bulan")
        m4.metric("ROI (1 Thn)", f"{(profit_month * 12 / capex_total * 100):.1f}%")
    else:
        st.error("⚠️ Operasional masih defisit. Perlu menaikkan harga tiket atau target pengunjung.")

    # --- NEW: INDUSTRIAL RAB DETAIL ---
    st.markdown("### 📊 Rincian Detail RAB Anggur Skala Industri")
    with st.expander("📑 Lihat Detail Komponen Biaya (Scientific & Industrial)"):
        area_ha = (gh_size / 10000)
        st.write(f"Estimasi untuk luas {gh_size} m² ({area_ha:.2f} Ha)")
        
        rab_cols = st.columns(2)
        with rab_cols[0]:
            st.markdown("""
            **A. Capex (Infrastruktur Industri):**
            1. **Greenhouse Standard IPB/Yamasa:** Rp 350k - 500k/m²
            2. **Otomasi Irigasi (Fertigasi Drip):** IoT Based, Solenoid valve.
            3. **Konstruksi Trellis Baja Ringan:** Sistem Y/T.
            4. **Bibit Import Grafts (Rootstock RM/DOX):** Rp 150k - 250k/pohon.
            5. **Lab QC Sederhana:** Refraktometer (Brix), pH/EC Meter, Soil Tester.
            """)
        with rab_cols[1]:
            st.markdown("""
            **B. Opex (Maintenance Saintifik):**
            1. **Nutrisi AB Mix Khusus Anggur:** Rp 15k - 25k / baki-liter pekatan.
            2. **Fungisida/Insektisida Preventif:** Rotasi bahan aktif.
            3. **Labor (Crop Manager & Maintenance):** Standar teknis tinggi.
            4. **Listrik (Pompa & IoT):** 24 Jam.
            """)
            
        # Table of Assumptions
        rab_data = {
            "Komponen": ["Greenhouse + UV 200mic", "System Fertigasi IoT", "Bibit Premium (Siap Buah)", "Media Tanam (Cocopeat/Sekam)", "Trellis & Wiring"],
            "Estimasi Biaya (Persen)": ["60%", "15%", "10%", "5%", "10%"]
        }
        st.table(pd.DataFrame(rab_data))

    # Chart Profit Projection
    months = np.arange(1, 25)
    cumulative_profit = (profit_month * months) - capex_total
    
    fig_roi = go.Figure()
    fig_roi.add_trace(go.Scatter(x=months, y=cumulative_profit, mode='lines+markers', name='Arus Kas Kumulatif'))
    fig_roi.add_trace(go.Scatter(x=months, y=[0]*24, mode='lines', name='Break Even Point', line=dict(color='red', dash='dash')))
    fig_roi.update_layout(title="Proyeksi Break Even Point (2 Tahun)", xaxis_title="Bulan", yaxis_title="Saldo Kas (Rp)")
    st.plotly_chart(fig_roi, use_container_width=True)

# --- TAB 4: MANAJEMEN & SOP ---
with tab4:
    st.header("📋 Standard Operating Procedure (SOP)")
    st.markdown("""
    Bisnis Agrowisata yang sukses bergantung pada **Disiplin Eksekusi** dan **Kenyamanan Wisatawan**.
    """)
    
    col_sop1, col_sop2 = st.columns(2)
    
    with col_sop1:
        with st.expander("🛡️ SOP Budidaya Anggur Saintifik", expanded=True):
            st.markdown("""
            **1. Fase Pruning (Pemangkasan):**
            - *Foundation Pruning:* Pembentukan cabang tersier (10-15 mata tunas).
            - *Production Pruning:* Pemangkasan untuk bunga (Long/Medium/Short pruning sesuai varietas).
            - *H-7 Pruning:* Pemberian nutrisi MKP & KNO3 Putih dosis tinggi.
            
            **2. Manajemen Nutrisi (Fertigasi):**
            - **Fase Grow:** Perbandingan N:P:K (3:1:1) - EC 1.5.
            - **Fase Fruit:** Perbandingan N:P:K (1:2:3) - EC 2.5.
            - **pH Control:** Wajib 5.8 - 6.2 (Kunci serapan unsur hara).
            
            **3. Penjarangan Buah (Berry Thinning):**
            - Wajib dilakukan saat buah sebesar biji kacang hijau.
            - Buang 30-50% buah agar sisa buah membesar maksimal & anti-jamur.
            """)
            
        with st.expander("🧺 Protokol Biosecurity (Wisatawan)"):
            st.markdown("""
            1. **Footbath:** Wajib desinfeksi alas kaki.
            2. **Strict No Smoking:** Asap merusak stomata tanaman anggur.
            3. **Steril Tools:** Gunting petik direndam alkohol 70% tiap batch.
            """)

    with col_sop2:
        with st.expander("🌡️ Parameter Lingkungan Industri"):
            st.markdown("""
            - **Intensitas Cahaya:** 35k - 45k Lux (Gunakan Parameter PAR jika ada).
            - **VPD (Vapor Pressure Deficit):** Target 0.8 - 1.2 kPa (Optimasi transpirasi).
            - **CO2 Level:** Target 400-800 ppm.
            """)
            
        with st.expander("🤳 Integrated Marketing & Edu"):
            st.markdown("""
            1. **Brix Testing Show:** Pengunjung diajak tes kemanisan buah sendiri.
            2. **Pruning Experience:** Workshop memangkas dengan bimbingan.
            3. **Digital Labeling:** Setiap pohon punya history budidaya digital (Scan QR).
            """)

# --- TAB 5: KALENDER OPERASIONAL ---
with tab5:
    st.header("📅 Kalender Budidaya & Liburan")
    st.caption("Penyelarasan masa panen dengan puncak musim liburan nasional (High Season).")
    
    # Simple Calendar Data
    cal_data = {
        "Bulan": ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Ags", "Sep", "Okt", "Nop", "Des"],
        "Status Tanaman": ["Vegetatif", "Vegetatif", "Generatif (Pruning)", "Masa Panen", "Masa Panen", "Masa Istirahat", 
                           "Vegetatif", "Vegetatif", "Generatif", "Masa Panen", "Masa Panen", "Peak Season (Des)"],
        "Level Pengunjung": ["Low", "Low", "Medium (Puasa)", "High (Lebaran)", "Medium", "High (Sekolah)", 
                             "High", "Medium", "Low", "Medium", "High", "Extreme (Nataru)"]
    }
    df_cal = pd.DataFrame(cal_data)
    
    # Highlight Peak Seasons
    def highlight_peak(s):
        return ['background-color: #ffcccc' if v in ['High', 'Extreme'] else '' for v in s]
    
    st.table(df_cal.style.apply(highlight_peak, subset=['Level Pengunjung']))
    
    st.info("""
    **💡 Tip Strategis:**
    *Lakukan Pruning (pemangkasan pembuahan) Anggur 100-110 hari SEBELUM Idul Fitri atau Libur Natal agar buah matang sempurna tepat saat ribuan orang mencari tempat wisata.*
    """)

# --- TAB 6: YAMASA NURSERY ---
with tab6:
    st.header("🌱 Yamasa Seedling Business Simulation")
    st.markdown("""
    **Inspirasi: Yamasa No Niwa, Japan.** 
    Pusat pembibitan modern yang mengutamakan kemurnian genetika (Genetic Purity) dan efisiensi ruang produksi.
    """)
    
    with st.expander("🌳 Mother Plant Management (Blok Fondasi)", expanded=True):
        st.markdown("""
        Pohon induk (Mother Plant) adalah aset terpenting. 
        - **Karantina Ketat:** Area terpisah dari jalur pengunjung.
        - **Virus-Free Testing:** Uji lab berkala untuk memastikan bebas virus mosaik.
        - **Scion Production:** Target 50-100 mata tunas (scion) per pohon induk per tahun.
        """)
    
    col_nur1, col_nur2 = st.columns([1, 1])
    
    with col_nur1:
        st.subheader("🏭 Kapasitas Produksi")
        tray_type = st.selectbox("Jenis Tray Semai", ["105 Holes", "128 Holes", "200 Holes"])
        num_trays = st.number_input("Jumlah Tray per Batch", 1, 5000, 100)
        seed_cost_item = st.number_input("Harga Benih per Butir (Rp)", 10, 5000, 500)
        maintenance_cost_tray = st.number_input("Biaya Rawat per Tray (Rp)", 0, 50000, 15000)
        
        total_seeds = int(tray_type.split()[0]) * num_trays
        total_prod_cost = (total_seeds * seed_cost_item) + (num_trays * maintenance_cost_tray)
        
        st.markdown(f"**Total Kapasitas: {total_seeds:,.0f} Bibit**")
        st.markdown(f"**Total Biaya Produksi: Rp {total_prod_cost:,.0f}**")

    with col_nur2:
        st.subheader("📈 Simulasi Penjualan (Dual Stream)")
        
        # Stream 1: Retail Merchandise (Wisatawan)
        with st.expander("🛍️ 1. Penjualan Souvenir (Wisatawan)", expanded=True):
            retail_percent = st.slider("% Stok untuk Wisatawan", 0, 100, 20)
            
            # Age Standards
            age_options = {
                "🌿 Muda (10-15 HSS)": 1.0,
                "🪴 Standar (20-30 HSS)": 1.5,
                "🌳 Premium (40+ HSS - Siap Buah)": 2.5
            }
            selected_age = st.selectbox("Standar Usia Bibit", list(age_options.keys()))
            base_retail_price = st.number_input("Harga Dasar Bibit (Rp/Pohon)", 1000, 10000, 3000)
            
            # Potting Parameters
            pot_cost = st.number_input("Biaya Pot & Media Estetik (Rp/Unit)", 0, 20000, 5000)
            packaging_cost = st.number_input("Biaya Label & Packaging (Rp/Unit)", 0, 5000, 1000)
            
            retail_price_per_unit = (base_retail_price * age_options[selected_age]) + pot_cost + packaging_cost
            st.info(f"**Harga Jual Retail: Rp {retail_price_per_unit:,.0f} / Pot**")
        
        # Stream 2: B2B / Farm Supply (Petani)
        with st.expander("🚜 2. Penjualan B2B (Petani/Mitra)", expanded=True):
            b2b_percent = st.slider("% Stok untuk Petani", 0, (100-retail_percent), 60)
            
            # Pricing per Tray/Baki
            tray_price = st.number_input("Harga Jual per Baki (Rp)", 10000, 500000, 150000, help="Satu baki sesuai kapasitas tray yang dipilih")
            
            # Derived price per seedling for calculation
            seedlings_per_tray = int(tray_type.split()[0])
            b2b_price_per_seedling = tray_price / seedlings_per_tray
            st.info(f"**Ekuivalen: Rp {b2b_price_per_seedling:,.0f} / Bibit**")
        
        # Calculation
        qty_retail = (retail_percent/100) * total_seeds
        qty_b2b_trays = (b2b_percent/100) * num_trays
        
        rev_retail = qty_retail * retail_price_per_unit
        rev_b2b = qty_b2b_trays * tray_price
        
        rev_nursery = rev_retail + rev_b2b
        profit_nursery = rev_nursery - total_prod_cost
        
    st.markdown("---")
    res_n1, res_n2, res_n3 = st.columns(3)
    res_n1.metric("Total Omzet Nursery", f"Rp {rev_nursery:,.0f}")
    res_n2.metric("Laba Bersih Nursery", f"Rp {profit_nursery:,.0f}")
    res_n3.metric("Margin Keuntungan", f"{(profit_nursery/rev_nursery*100):.1f}%" if rev_nursery > 0 else "0%")

    with st.expander("🇯🇵 Yamasa Standards Checklist (Japan Quality)"):
        st.checkbox("Kebersihan Lantai: Bebas lumut, tanah, dan genangan air (Sanitation First).", value=True)
        st.checkbox("Pencahayaan: Minimal 30.000 Lux / DLI (Daily Light Integral) optimal.", value=True)
        st.checkbox("Pelabelan Digital: QR Code di setiap tray untuk traceability.", value=True)
        st.checkbox("Uniformity: Tinggi dan diameter batang (calliper) seragam >95%.", value=True)
        st.checkbox("Grafting Success Rate: Target minimal 90% keberhasilan.", value=True)
        st.success("✅ Memenuhi Standar Yamasa No Niwa")

# --- TAB 7: MASTERPLAN & EDUKASI ---
with tab7:
    st.header("🏛️ Masterplan & Workshop Edukasi")
    st.markdown("""
    **Transformasi Kebun Menjadi Kampus Alam.** 
    Mengoptimalkan nilai lahan melalui zonasi spasial dan monetisasi pengetahuan.
    """)
    
    col_mp1, col_mp2 = st.columns([1, 1])
    
    with col_mp1:
        st.subheader("🗺️ Zonasi Spasial (Masterplan)")
        with st.expander("📍 Pembagian Area Strategis", expanded=True):
            st.markdown("""
            1. **Zona Produksi (Backstage):** Area tertutup untuk budidaya intensif. Terpisah dari jalur umum untuk menjaga biosecurity.
            2. **Zona Showroom (Nursery):** Area display bibit estetik (Yamasa Style). Tempat wisatawan belajar dan membeli bibit.
            3. **Zona Experience (Pick-Your-Own):** Jalur lebar (1.5m+) dengan spot foto terintegrasi di antara tanaman.
            4. **Zona Edukasi (Workshop Hub):** Ruang terbuka/semi-terbuka dengan bangku kayu untuk kegiatan belajar berkelompok.
            """)
        
        st.info("""
        **💡 Visitor Flow Tip:** 
        Pastikan alur pengunjung berbentuk **Loop (Satu Arah)**. Mulai dari Edukasi -> Petik Buah -> Terakhir melewati Showroom Bibit (Nursery) untuk memicu *Emotional Buying*.
        """)

    with col_mp2:
        st.subheader("🎓 Simulasi Workshop Edukasi")
        workshop_price = st.number_input("Biaya Workshop per Orang (Rp)", 50000, 500000, 150000)
        pax_per_class = st.number_input("Kapasitas per Kelas (Orang)", 1, 100, 20)
        classes_per_month = st.number_input("Jumlah Kelas per Bulan", 1, 30, 4)
        
        # Costs
        material_cost_pax = st.number_input("Biaya Bahan per Orang (Rp)", 0, 100000, 35000, help="Bibit, media, pot, handout")
        instruction_cost_class = st.number_input("Biaya Instruktor per Kelas (Rp)", 0, 1000000, 150000)
        
        # Calculation
        total_pax = pax_per_class * classes_per_month
        rev_workshop = total_pax * workshop_price
        total_workshop_cost = (total_pax * material_cost_pax) + (classes_per_month * instruction_cost_class)
        profit_workshop = rev_workshop - total_workshop_cost
        
        st.markdown("---")
        m_w1, m_w2 = st.columns(2)
        m_w1.metric("Laba Bersih Workshop", f"Rp {profit_workshop:,.0f}")
        m_w2.metric("Margin Workshop", f"{(profit_workshop/rev_workshop*100):.1f}%" if rev_workshop > 0 else "0%")
        
        st.success("✅ Workshop adalah pendapatan 'Low Risk' dengan profit tinggi.")

# --- TAB 8: IOT SMART FARM ---
with tab8:
    st.header("📡 IoT & Smart Farm Command Center")
    st.markdown("""
    **Transformasi Kebun Menjadi Digital Twin.** 
    Pantau kondisi tanaman secara real-time dan berikan pengalaman interaktif bagi pengunjung.
    """)
    
    # Simulate Live Data Stream
    import random
    import time

    col_iot1, col_iot2 = st.columns([1, 2])
    
    with col_iot1:
        st.subheader("📟 Real-time Monitoring")
        st.caption("Data disimulasikan dari sensor IoT di lapangan.")
        
        # Simulated metrics with small random fluctuations
        temp_iot = 24.5 + random.uniform(-0.5, 0.5)
        hum_iot = 72.0 + random.uniform(-1, 1)
        ec_iot = 1.8 + random.uniform(-0.05, 0.05)
        light_iot = 45000 + random.randint(-500, 500)
        
        st.metric("Suhu Udara (°C)", f"{temp_iot:.1f}", f"{random.uniform(-0.2, 0.2):.1f}")
        st.metric("Kelembaban Media (%)", f"{hum_iot:.1f}", f"{random.uniform(-0.5, 0.5):.1f}")
        st.metric("Nutrisi / EC (mS/cm)", f"{ec_iot:.2f}", f"{random.uniform(-0.01, 0.01):.2f}")
        st.metric("Intensitas Cahaya (Lux)", f"{light_iot:,}", f"{random.randint(-100, 100)}")

    with col_iot2:
        st.subheader("📲 Simulasi Scan QR Pengunjung")
        st.info("Pilih ID Tanaman seolah-olah Anda sedang scan QR Code di lahan.")
        
        plant_id = st.selectbox("Pilih Kode QR Tanaman:", [f"AGRI-MELON-{i:03d}" for i in range(1, 11)])
        
        # Plant Status Generation
        health_status = random.choice(["Optimal", "Sangat Baik", "Perlu Perhatian"])
        vga_status = random.choice(["Vegetatif Akhir", "Pembesaran Buah", "Pematangan"])
        days_to_harvest = random.randint(5, 45)
        
        st.markdown(f"""
        <div style="background-color: white; padding: 20px; border-radius: 15px; border: 2px solid #4CAF50;">
            <h3 style="color: #2E7D32;">🌱 Profil Pintar: {plant_id}</h3>
            <hr>
            <p><b>Kondisi Kesehatan:</b> <span style="color: {'green' if health_status != 'Perlu Perhatian' else 'orange'};">{health_status}</span></p>
            <p><b>Fase Pertumbuhan:</b> {vga_status}</p>
            <p><b>Estimasi Panen:</b> {days_to_harvest} hari lagi</p>
            <p><b>Varian:</b> Melon Intanon RZ (Premium)</p>
            <hr>
            <p style="font-size: 0.8em; color: gray;">*Data ini diakses oleh pengunjung melalui scan QR Code di setiap poli bag.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("🛠️ Konfigurasi Sistem IoT"):
            st.markdown("""
            **Infrastruktur yang Digunakan:**
            - **Nodes:** ESP32 + Sensor DHT22 & Soil Moisture.
            - **Gateway:** Raspberry Pi 4 (Edge Computing).
            - **Cloud:** Real-time Firebase / MQTT Broker.
            - **Dashboard:** Streamlit Cloud Integration.
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center;">
    <p><b>Advanced Agrowisata & Nursery Control System</b></p>
    <p>© 2025 AgriSensa - Terinspirasi oleh Inovasi Pertanian Global</p>
</div>
""", unsafe_allow_html=True)
