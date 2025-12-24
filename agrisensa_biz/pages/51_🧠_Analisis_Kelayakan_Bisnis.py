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
        ["Toko Pertanian (Farm Shop)", "Greenhouse Komersial", "Distributor Pupuk", "Pengolahan Hasil Panen", "Agrowisata"]
    )
    
    location_name = st.text_input("Nama Lokasi / Area", "Kec. Pujon, Malang")
    
    st.subheader("💰 Permodalan")
    own_capital = st.number_input("Modal Sendiri (Rp)", 0, 10_000_000_000, 100_000_000, 10_000_000)
    loan_amount = st.number_input("Pengajuan Kredit (Rp)", 0, 10_000_000_000, 50_000_000, 10_000_000)
    
    total_capital = own_capital + loan_amount
    st.metric("Total Modal", f"Rp {total_capital:,.0f}")

# ==================== 2. INPUT PARAMETER (TABS) ====================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌍 Lokasi & Geo",
    "🌱 Agronomi & Lahan",
    "👥 Pasar & Kompetisi",
    "💰 Finansial (5C)",
    "⚖️ Legal & Risiko",
    "📊 Laporan Final"
])

# --- TAB 1: GEO-SPASIAL ---
with tab1:
    st.subheader("📍 Analisis Lokasi & Geografis")
    # ... (Code for Tab 1 remains mostly same, just standardizing header if needed)
    
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
    # ... (Keep existing 5C logic)
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

# --- TAB 5: LEGAL ---
with tab5:
    st.subheader("⚖️ Legalitas & Risiko")
    legal_docs = st.multiselect("Dokumen Legal", ["NIB", "NPWP", "Izin Lokasi", "AMDAL", "Sertifikat Halal", "Akta PT/CV"])
    social_accept = st.select_slider("Penerimaan Warga", options=["Menolak", "Netral", "Mendukung", "Sangat Mendukung"], value="Mendukung")

# --- TAB 6: REPORT ---
with tab6:
    st.subheader("📊 Laporan Analisis Kelayakan")
    
    scores = {}
    
    # 1. Geo Score
    geo_score = 0
    if road_access in ["Jalan Raya Provinsi", "Dekat Tol"]: geo_score += 40
    elif road_access == "Jalan Aspal Kecil": geo_score += 30
    else: geo_score += 15
    if disaster_risk in ["Sangat Rendah", "Rendah"]: geo_score += 30
    else: geo_score -= 10
    scores['Geografis'] = min(geo_score + 30, 100)
    
    # 2. Agronomy Score (NEW)
    agro_score = 0
    # Land Class
    if land_class == "S1 - Sangat Sesuai": agro_score += 40
    elif land_class == "S2 - Cukup Sesuai": agro_score += 30
    elif land_class == "N - Tidak Sesuai": agro_score -= 20
    # Sentra Bonus
    if sentra_type != "Bukan Sentra (Pioneer)": agro_score += 10
    # Irrigation
    if irrigation_type in ["Irigasi Teknis (Bendungan)", "Mata Air Gravitasi"]: agro_score += 30
    elif irrigation_type == "Sumur Bor / Pompa": agro_score += 20
    # pH ideal (6-7)
    if 6.0 <= ph_level <= 7.0: agro_score += 20
    
    # Pest Penalty (NEW)
    if pest_risk_level == "Tinggi (Endemik)": agro_score -= 15
    elif pest_risk_level == "Sangat Tinggi (Wabah)": agro_score -= 30
    
    scores['Agronomi & Lahan'] = max(0, min(agro_score, 100))
    
    # 3. Market Score
    mkt_score = 0
    market_point = (farmer_count / 100) + (land_area / 10)
    mkt_score += min(market_point, 40)
    mkt_score += max(30 - (competitor_count * 5), 0)
    if len(unique_selling) >= 3: mkt_score += 20
    scores['Pasar'] = min(mkt_score + 10, 100)
    
    # 4. Financial
    fin_score = 0
    if credit_history == "Sangat Baik": fin_score += 30
    if der < 2.0: fin_score += 25
    if coverage_ratio >= 110: fin_score += 25
    if exp_years > 3: fin_score += 20
    scores['Finansial'] = min(fin_score, 100)
    
    # 5. Legal
    scores['Legal'] = min(len(legal_docs) * 20 + 20, 100)
    
    # --- RESULT ---
    df_score = pd.DataFrame(list(scores.items()), columns=['Kriteria', 'Nilai'])
    
    # Final Calc
    weights = {'Geografis': 0.15, 'Agronomi & Lahan': 0.25, 'Pasar': 0.20, 'Finansial': 0.30, 'Legal': 0.10}
    final_score = sum(scores[k] * weights[k] for k in scores)
    
    # Layout
    r1, r2 = st.columns([1, 1.5])
    
    with r1:
        st.markdown(f"""
        <div class="score-card">
            <div class="metric-label">SKOR KELAYAKAN BISNIS</div>
            <div class="metric-big" style="color: {'#10b981' if final_score >= 75 else '#f59e0b' if final_score >= 50 else '#ef4444'}">
                {final_score:.1f} / 100
            </div>
            <div style="margin-top: 10px; font-weight: bold;">
                {'✅ SANGAT LAYAK (RECOMMENDED)' if final_score >= 75 else '⚠️ LAYAK DENGAN CATATAN' if final_score >= 50 else '❌ BERISIKO TINGGI (NOT RECOMMENDED)'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Kesimpulan AI")
        if final_score >= 75:
            st.success("Bisnis ini memiliki prospek sangat cerah. Fondasi lokasi, pasar, dan finansial sangat kuat. Direkomendasikan untuk segera eksekusi.")
        elif final_score >= 50:
            st.warning("Bisnis ini potensial namun memiliki risiko yang perlu dimitigasi, terutama pada aspek dengan skor terendah. Perbaiki parameter sebelum mengajukan kredit besar.")
        else:
            st.error("Rencana bisnis ini belum matang atau lokasi kurang strategis. Sebaiknya evaluasi ulang model bisnis atau cari lokasi alternatif.")

        if loan_amount > 0:
            credit_grade = "A (Prime)" if final_score >= 80 else "B (Good)" if final_score >= 70 else "C (Fair)" if final_score >= 60 else "D (Subprime)"
            st.info(f"🏷️ **Prediksi Rating Kredit:** {credit_grade}")
            
        # --- SMART RECOMMENDATION ENGINE ---
        st.markdown("### 💡 Rekomendasi AI Jenis Usaha")
        
        recommendations = []
        
        # 1. Check Greenhouse Potential
        if total_capital > 500_000_000 and pest_risk_level in ["Tinggi (Endemik)", "Sangat Tinggi (Wabah)"]:
            recommendations.append(("Greenhouse Modern", "Area ini endemik hama tinggi. Greenhouse adalah solusi terbaik untuk memproteksi modal tanaman Anda."))
        
        # 2. Check Farm Shop Potential
        if road_access in ["Jalan Raya Provinsi", "Dekat Tol"] and farmer_count > 1000 and competitor_count < 5:
            recommendations.append(("Toko Pertanian (Farm Shop)", "Lokasi sangat strategis untuk retail. Basis petani besar namun kompetisi masih rendah."))
            
        # 3. Check Agrowisata Potential
        if elevation > 800 and disaster_risk in ["Sangat Rendah", "Rendah"] and road_access != "Jalan Tanah":
            recommendations.append(("Agrowisata & Petik Buah", "Ketinggian >800mdpl (Sejuk) + Akses bagus + Risiko rendah = Sempurna untuk wisata."))
            
        # 4. Check Trading/Distributor
        if sentra_type != "Bukan Sentra (Pioneer)" and road_access not in ["Jalan Tanah", "Jalan Makadam"]:
            recommendations.append(("Distributor/Offtaker", "Manfaatkan status 'Sentra Budidaya' untuk menjadi pengepul/distributor skala besar."))

        if recommendations:
            st.info(f"Mengingat kondisi (Hama: {pest_risk_level}, Lokasi, Modal), kami menyarankan pivot ke:")
            for rec, reason in recommendations:
                st.markdown(f"- **{rec}**: {reason}")
        else:
            st.caption("Model bisnis yang Anda pilih ("+biz_type+") sudah cukup moderat untuk kondisi ini.")

    with r2:
        # Radar Chart
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=df_score['Nilai'],
            theta=df_score['Kriteria'],
            fill='toself',
            name='Skor Bisnis Anda',
            line_color='#0284c7'
        ))
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=False,
            title="Peta Kekuatan Bisnis (Radar Chart)"
        )
        st.plotly_chart(fig, use_container_width=True)

