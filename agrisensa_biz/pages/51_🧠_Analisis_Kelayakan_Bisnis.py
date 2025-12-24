import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌍 Lokasi & Geo-Spasial",
    "👥 Analisis Pasar",
    "💰 Finansial & Kredit (5C)",
    "⚖️ Legal & Risiko",
    "📊 Hasil Analisis (Report)"
])

# --- TAB 1: GEO-SPASIAL ---
with tab1:
    st.subheader("📍 Analisis Lokasi & Geografis")
    
    col_geo1, col_geo2 = st.columns([1.5, 1])
    
    with col_geo1:
        st.info("Pilih titik lokasi usaha pada peta untuk analisis otomatis.")
        # Dummy Map (Malang)
        m = folium.Map(location=[-7.85, 112.5], zoom_start=11)
        folium.Marker(
            [-7.85, 112.5], 
            popup="Lokasi Usaha", 
            icon=folium.Icon(color="green", icon="leaf")
        ).add_to(m)
        st_data = st_folium(m, height=400, width="100%")
    
    with col_geo2:
        st.markdown("#### 🌦️ Parameter Lingkungan")
        
        # Simulated Data (In real app, fetch from API based on Lat/Long)
        elevation = st.slider("Ketinggian (mdpl)", 0, 2500, 800)
        avg_temp = 28 - (elevation / 100 * 0.6) # Adiabatic lapse rate
        st.metric("Estimasi Suhu Rata-rata", f"{avg_temp:.1f}°C")
        
        road_access = st.selectbox("Aksesibilitas Jalan", ["Jalan Tanah", "Jalan Makadam", "Jalan Aspal Kecil", "Jalan Raya Provinsi", "Dekat Tol"])
        disaster_risk = st.select_slider("Risiko Bencana (Banjir/Longsor)", options=["Sangat Rendah", "Rendah", "Sedang", "Tinggi", "Sangat Tinggi"], value="Rendah")
        
        water_source = st.checkbox("Ada Sumber Air Sepanjang Tahun?", value=True)
        electricity = st.checkbox("Listrik 3 Phase Tersedia?", value=True)

# --- TAB 2: PASAR ---
with tab2:
    st.subheader("👥 Potensi Pasar & Kompetisi")
    
    col_mkt1, col_mkt2 = st.columns(2)
    
    with col_mkt1:
        st.markdown("#### 🎯 Target Pasar")
        catchment_radius = st.slider("Radius Layanan (km)", 1, 50, 5)
        farmer_count = st.number_input("Estimasi Jumlah Petani di Area (KK)", 100, 50000, 1500)
        land_area = st.number_input("Estimasi Luas Lahan Potensial (Ha)", 10, 10000, 500)
        
    with col_mkt2:
        st.markdown("#### ⚔️ Kompetisi")
        competitor_count = st.number_input("Jumlah Kompetitor Direct (Serupa)", 0, 50, 3)
        market_growth = st.slider("Pertumbuhan Pasar Tahunan (%)", -10, 50, 10)
        
        unique_selling = st.multiselect(
            "Keunggulan Kompetitif (USP)",
            ["Harga Lebih Murah", "Layanan Antar", "Konsultasi Gratis", "Teknologi Modern", "Kredit Tempo", "Stok Lengkap"]
        )

# --- TAB 3: FINANSIAL (5C) ---
with tab3:
    st.subheader("💰 Analisis Kelayakan Kredit (Metode 5C)")
    st.caption("Parameter ini digunakan bank untuk menilai kelayakan pinjaman modal.")
    
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("#### 1. Character & Capacity")
        exp_years = st.number_input("Pengalaman Usaha (Tahun)", 0, 50, 5)
        mgmt_team = st.selectbox("Kualitas Tim Manajemen", ["One Man Show", "Ada Tim Kecil", "Profesional Lengkap"])
        credit_history = st.selectbox("Riwayat Kredit (SLIK)", ["Belum Ada", "Pernah Nunggak", "Lancar", "Sangat Baik"])
        
    with c2:
        st.markdown("#### 2. Capital, Collateral & Condition")
        der = (loan_amount / own_capital) if own_capital > 0 else 99
        st.metric("Debt to Equity Ratio (DER)", f"{der:.2f}x", delta="Sehat < 2.0" if der < 2.0 else "Risiko Tinggi", delta_color="inverse")
        
        collateral_value = st.number_input("Nilai Agunan / Jaminan (Rp)", 0, 20_000_000_000, 100_000_000)
        coverage_ratio = (collateral_value / loan_amount * 100) if loan_amount > 0 else 100
        st.progress(min(coverage_ratio/200, 1.0), text=f"Coverage Ratio: {coverage_ratio:.1f}%")
        
        economic_cond = st.selectbox("Kondisi Ekonomi Sektor", ["Resesi", "Stabil", "Bertumbuh Pesat"], index=2)

# --- TAB 4: LEGAL ---
with tab4:
    st.subheader("⚖️ Legalitas & Risiko Regulasi")
    
    legal_docs = st.multiselect(
        "Dokumen Legal Dimiliki",
        ["NIB (Nomor Induk Berusaha)", "NPWP", "Izin Lokasi/PKKPR", "AMDAL / UKL-UPL", "Sertifikat Halal/Organik", "Akta Pendirian PT/CV"]
    )
    
    social_accept = st.select_slider("Penerimaan Masyarakat Sekitar", options=["Menolak", "Netral", "Mendukung", "Sangat Mendukung"], value="Mendukung")

# --- TAB 5: REPORT ---
with tab5:
    st.subheader("📊 Laporan Analisis Kelayakan")
    
    # --- SCORING ENGINE ---
    scores = {}
    
    # 1. Geo Score
    geo_score = 0
    if road_access in ["Jalan Raya Provinsi", "Dekat Tol"]: geo_score += 40
    elif road_access in ["Jalan Aspal Kecil"]: geo_score += 30
    else: geo_score += 10
    
    if disaster_risk == "Sangat Rendah": geo_score += 30
    elif disaster_risk == "Rendah": geo_score += 25
    else: geo_score -= 20
    
    if water_source and electricity: geo_score += 30
    scores['Geografis & Teknis'] = min(geo_score, 100)
    
    # 2. Market Score
    mkt_score = 0
    market_size = farmer_count * 10 # heuristic points
    mkt_score += min(market_size / 200, 40)
    
    comp_penalty = competitor_count * 5
    mkt_score += max(30 - comp_penalty, 0)
    
    usp_bonus = len(unique_selling) * 5
    mkt_score += min(usp_bonus, 30)
    scores['Pasar & Kompetisi'] = min(mkt_score, 100)
    
    # 3. Financial Score (5C)
    fin_score = 0
    if credit_history == "Sangat Baik": fin_score += 30
    elif credit_history == "Lancar": fin_score += 20
    
    if der < 1.0: fin_score += 25
    elif der < 2.0: fin_score += 15
    
    if coverage_ratio >= 120: fin_score += 25
    elif coverage_ratio >= 100: fin_score += 20
    
    fin_score += min(exp_years * 2, 20)
    scores['Finansial & Kredit'] = min(fin_score, 100)
    
    # 4. Legal Score
    leg_score = len(legal_docs) * 15
    if social_accept == "Sangat Mendukung": leg_score += 20
    elif social_accept == "Mendukung": leg_score += 10
    scores['Legalitas & Risiko'] = min(leg_score, 100)
    
    # --- RESULT ---
    df_score = pd.DataFrame(list(scores.items()), columns=['Kriteria', 'Nilai'])
    
    # Weighted Final Score
    weights = {'Geografis & Teknis': 0.20, 'Pasar & Kompetisi': 0.30, 'Finansial & Kredit': 0.35, 'Legalitas & Risiko': 0.15}
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

