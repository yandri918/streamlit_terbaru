"""
Budidaya Padi - Rice Cultivation Management System
Comprehensive application for rice farming with AI, ML, and advanced analytics
"""

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta
import time
import random
import sys
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS, ICONS
except ImportError:
    sys.path.insert(0, str(Path(__file__).parent / "utils"))
    from design_system import apply_design_system, icon, COLORS, ICONS

# Page config
st.set_page_config(
    page_title="AgriSensa Padi",
    page_icon="🌾",  # Keep for browser tab only
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Design System
apply_design_system()



# Helper for Time Greeting (WIB - UTC+7)
def get_greeting():
    # Streamlit Cloud is usually UTC. Adjust to WIB (UTC+7)
    utc_now = datetime.utcnow()
    wib_now = utc_now + timedelta(hours=7)
    hour = wib_now.hour
    
    if 4 <= hour < 11: return "Sugeng Enjang (Selamat Pagi)"
    elif 11 <= hour < 15: return "Sugeng Siang (Selamat Siang)"
    elif 15 <= hour < 18: return "Sugeng Sonten (Selamat Sore)"
    else: return "Sugeng Dalu (Selamat Malam)"

# Helper for Primbon
def get_pasaran():
    epoch = datetime(2024, 1, 1) # Monday Pahing
    # Use WIB for date checking too
    utc_now = datetime.utcnow()
    wib_now = utc_now + timedelta(hours=7)
    
    delta = (wib_now - epoch).days
    pasarans = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"]
    return pasarans[delta % 5]

# --- DASHBOARD CONTENT ---

# Initialize services
import sys
from pathlib import Path
if str(Path(__file__).parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent))

from services.market_service import MarketService

@st.cache_data(ttl=3600) # Cache for 1 hour
def fetch_market_data():
    service = MarketService()
    return service.get_rice_prices()

market_data = fetch_market_data()

# 1. Header Section
greeting = get_greeting()
pasaran = get_pasaran()
# Use WIB for display
wib_now = datetime.utcnow() + timedelta(hours=7)
today_str = wib_now.strftime("%A, %d %B %Y")

st.markdown(f"""
<div class='dashboard-header'>
    <h1>{icon('seedling', size='lg')} {greeting}, Pak Tani!</h1>
    <p>Selamat datang di Command Center AgriSensa. Mari cek kondisi lahan hari ini.</p>
    <div class='weather-widget'>
        {icon('calendar', style='far')} {today_str} • {icon('om', style='fab')} {pasaran} • {icon('cloud-sun')} Cerah Berawan (28°C)
    </div>
</div>
""", unsafe_allow_html=True)

# 2. Main Metrics & Alerts
col_alert, col_market = st.columns([2, 1])

with col_alert:
    # Pranata Mangsa Alert (Simulated logic from Calendar Module)
    st.markdown(f"""
    <div class='alert-card'>
        <strong>{icon('alert', color='#E65100')} Peringatan Dini (Mangsa Kalima):</strong><br>
        Curah hujan mulai tinggi. Waspada serangan <strong>Wereng Coklat</strong> dan penyakit <strong>Blas</strong>. 
        Segera cek drainase sawah!
    </div>
    """, unsafe_allow_html=True)
    
    # Financial Summary (Mock from Logbook)
    st.markdown(f"<h3>{icon('money')} Status Keuangan Bulan Ini</h3>", unsafe_allow_html=True)
    f_col1, f_col2, f_col3 = st.columns(3)
    f_col1.metric("Pengeluaran", "Rp 1.500.000", "Pupuk & Upah")
    f_col2.metric("Pemasukan (Est)", "Rp 0", "-")
    f_col3.metric("Saldo Kas", "Rp 8.500.000", "Aman")

with col_market:
    # Build dynamic HTML for prices
    gkp = market_data['gkp']
    beras = market_data['beras_medium']
    
    gkp_arrow = "▲" if gkp['change'] >= 0 else "▼"
    gkp_color = "green" if gkp['change'] >= 0 else "red"
    
    beras_arrow = "▲" if beras['change'] >= 0 else "▼"
    beras_color = "green" if beras['change'] >= 0 else "red"
    
    st.markdown(f"<h3>{icon('chart-line')} Harga Pasar (Live)</h3>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='price-ticker'>
        {icon('seedling')} GKP (Gabah Kering Panen)<br>
        <span style='font-size: 1.5rem'>Rp {gkp['price']:,.0f} / kg</span><br>
        <span style='color: {gkp_color}'>{gkp_arrow} Rp {abs(gkp['change']):,.0f} (Hari ini)</span>
    </div>
    <div class='price-ticker'>
        {icon('seedling')} Beras Medium<br>
        <span style='font-size: 1.5rem'>Rp {beras['price']:,.0f} / kg</span><br>
        <span style='color: {beras_color}'>{beras_arrow} Rp {abs(beras['change']):,.0f} (Hari ini)</span>
    </div>
    """, unsafe_allow_html=True)
    st.caption("Sumber: Bapanas (Nasional)")

# 3. Quick Actions Grid
st.markdown("---")
st.markdown(f"<h2>{icon('rocket')} Menu Cepat (Quick Actions)</h2>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"<div class='feature-btn'><i class='fas fa-vial' style='font-size: 2.5rem; color: {COLORS['primary']}'></i><h3>Analisis Tanah</h3><p style='color: {COLORS['gray_600']}'>Cek status hara tanah & rekomendasi pupuk</p><p style='font-size: 0.9rem; color: {COLORS['gray_500']}'>Module 10</p></div>", unsafe_allow_html=True)

with c2:
    st.markdown(f"<div class='feature-btn'><i class='fas fa-bug' style='font-size: 2.5rem; color: {COLORS['primary']}'></i><h3>Dokter Tanaman</h3><p style='color: {COLORS['gray_600']}'>Identifikasi hama & cari obatnya</p><p style='font-size: 0.9rem; color: {COLORS['gray_500']}'>Module 03</p></div>", unsafe_allow_html=True)

with c3:
    st.markdown(f"<div class='feature-btn'><i class='fas fa-calendar-alt' style='font-size: 2.5rem; color: {COLORS['primary']}'></i><h3>Kalender Tanam</h3><p style='color: {COLORS['gray_600']}'>Cek hari baik & jadwal tanam</p><p style='font-size: 0.9rem; color: {COLORS['gray_500']}'>Module 06</p></div>", unsafe_allow_html=True)

with c4:
    st.markdown(f"<div class='feature-btn'><i class='fas fa-book' style='font-size: 2.5rem; color: {COLORS['primary']}'></i><h3>Monitoring Logbook</h3><p style='color: {COLORS['gray_600']}'>Catat pengeluaran & kegiatan hari ini</p><p style='font-size: 0.9rem; color: {COLORS['gray_500']}'>Module 12</p></div>", unsafe_allow_html=True)

# 4. Chart Visualization (Mini Dashboard)
st.markdown("---")
st.markdown(f"<h2>{icon('chart-bar')} Tren Pertumbuhan & Cuaca</h2>", unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Dummy Growth Data
    growth_data = pd.DataFrame({
        'HST': [10, 20, 30, 40, 50],
        'Tinggi (cm)': [15, 25, 45, 60, 85]
    })
    
    chart = alt.Chart(growth_data).mark_line(point=True, color='#2E7D32').encode(
        x='HST',
        y='Tinggi (cm)',
        tooltip=['HST', 'Tinggi (cm)']
    ).properties(title="Grafik Tinggi Tanaman (Petak A)")
    st.altair_chart(chart, use_container_width=True)

with chart_col2:
    # Mock Weather Forecast
    weather_df = pd.DataFrame({
        'Hari': ['Sen', 'Sel', 'Rab', 'Kam', 'Jum'],
        'Peluang Hujan (%)': [80, 60, 20, 10, 40],
        'Suhu (°C)': [27, 28, 30, 31, 29]
    })
    
    bar = alt.Chart(weather_df).mark_bar(color='#90CAF9').encode(
        x=alt.X('Hari', sort=None),
        y='Peluang Hujan (%)',
        tooltip=['Hari', 'Peluang Hujan (%)']
    ).properties(title="Prakiraan Hujan 5 Hari Kedepan")
    st.altair_chart(bar, use_container_width=True)

# Footer
st.markdown("---")
st.caption("© 2026 AgriSensa Padi - Sistem Cerdas Sahabat Petani")
