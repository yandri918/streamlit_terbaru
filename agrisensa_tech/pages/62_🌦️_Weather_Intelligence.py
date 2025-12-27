import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.weather_service import WeatherService
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Weather Intelligence",
    page_icon="🌦️",
    layout="wide"
)

user = require_auth()
show_user_info_sidebar()

service = WeatherService()

st.title("🌦️ Weather Intelligence Center")
st.markdown("""
**Cuaca Real-Time & Prediksi 7 Hari** | Powered by Open-Meteo API (Free & Unlimited)
""")

# --- SIDEBAR: LOCATION CONFIG ---
st.sidebar.header("📍 Lokasi Kebun")

# Preset locations
presets = {
    "Jakarta": (-6.2088, 106.8456),
    "Bandung": (-6.9175, 107.6191),
    "Surabaya": (-7.2575, 112.7521),
    "Yogyakarta": (-7.7956, 110.3695),
    "Malang": (-7.9666, 112.6326),
    "Bogor": (-6.5971, 106.8060),
    "Custom": None
}

location = st.sidebar.selectbox("Pilih Lokasi:", list(presets.keys()))

if location == "Custom":
    lat = st.sidebar.number_input("Latitude:", -90.0, 90.0, -6.2088, step=0.0001, format="%.4f")
    lon = st.sidebar.number_input("Longitude:", -180.0, 180.0, 106.8456, step=0.0001, format="%.4f")
else:
    lat, lon = presets[location]
    st.sidebar.info(f"📌 **{location}**\nLat: {lat:.4f}, Lon: {lon:.4f}")

# Fetch weather data
with st.spinner("Mengambil data cuaca..."):
    weather_data = service.get_weather_forecast(lat, lon)

if not weather_data:
    st.error("❌ Gagal mengambil data cuaca. Cek koneksi internet Anda.")
    st.stop()

# --- CURRENT WEATHER ---
st.markdown("### 🌡️ Kondisi Saat Ini")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Suhu", f"{weather_data['current_temp']:.1f}°C", 
              help="Suhu udara saat ini")
with col2:
    st.metric("Kelembapan", f"{weather_data['current_humidity']}%",
              help="Kelembapan relatif")
with col3:
    st.metric("Hujan", f"{weather_data['current_rain']:.1f} mm/jam",
              help="Intensitas hujan saat ini")
with col4:
    st.metric("Angin", f"{weather_data['wind_speed']:.1f} km/jam",
              help="Kecepatan angin")

# --- AGRICULTURAL ALERTS ---
alerts = service.get_agricultural_alerts(weather_data)

if alerts:
    st.markdown("### ⚠️ Peringatan Agronomi")
    
    for alert in alerts:
        if alert['type'] == 'warning':
            st.error(f"{alert['icon']} **{alert['title']}**\n\n{alert['message']}\n\n💡 **Tindakan:** {alert['action']}")
        elif alert['type'] == 'caution':
            st.warning(f"{alert['icon']} **{alert['title']}**\n\n{alert['message']}\n\n💡 **Tindakan:** {alert['action']}")
        else:
            st.info(f"{alert['icon']} **{alert['title']}**\n\n{alert['message']}\n\n💡 **Tindakan:** {alert['action']}")

# --- 7-DAY FORECAST ---
st.markdown("### 📅 Prediksi 7 Hari")

forecast = service.get_7day_forecast(weather_data)

if forecast:
    # Create DataFrame for display
    df_forecast = pd.DataFrame(forecast)
    df_forecast['date'] = pd.to_datetime(df_forecast['date']).dt.strftime('%a, %d %b')
    df_forecast = df_forecast.rename(columns={
        'date': 'Tanggal',
        'temp_max': 'Maks (°C)',
        'temp_min': 'Min (°C)',
        'rain_mm': 'Hujan (mm)',
        'rain_prob': 'Prob. Hujan (%)'
    })
    
    st.dataframe(
        df_forecast[['Tanggal', 'Maks (°C)', 'Min (°C)', 'Hujan (mm)', 'Prob. Hujan (%)']],
        use_container_width=True,
        hide_index=True
    )
    
    # Visual chart
    import plotly.graph_objects as go
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_forecast['Tanggal'],
        y=df_forecast['Maks (°C)'],
        mode='lines+markers',
        name='Suhu Maks',
        line=dict(color='#ef4444', width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_forecast['Tanggal'],
        y=df_forecast['Min (°C)'],
        mode='lines+markers',
        name='Suhu Min',
        line=dict(color='#3b82f6', width=2),
        marker=dict(size=8)
    ))
    
    fig.add_trace(go.Bar(
        x=df_forecast['Tanggal'],
        y=df_forecast['Hujan (mm)'],
        name='Curah Hujan',
        marker=dict(color='#10b981'),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Tren Suhu & Curah Hujan",
        xaxis_title="Tanggal",
        yaxis=dict(title="Suhu (°C)"),
        yaxis2=dict(title="Hujan (mm)", overlaying='y', side='right'),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# --- ADDITIONAL INFO ---
st.markdown("### 📊 Informasi Tambahan")

col_a, col_b = st.columns(2)

with col_a:
    st.metric("Estimasi Hujan Musiman", f"{weather_data['seasonal_rain_est']} mm",
              help="Proyeksi curah hujan untuk 4 bulan ke depan")
    
with col_b:
    rec = service.get_planting_recommendation(weather_data)
    st.info(f"**Rekomendasi Tanam:**\n\n{rec}")

# --- FOOTER ---
st.markdown("---")
st.caption("🌐 Data cuaca dari Open-Meteo API | Update otomatis setiap refresh halaman")
