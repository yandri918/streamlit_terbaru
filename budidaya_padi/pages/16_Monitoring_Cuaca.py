"""
 Weather Monitoring - Environmental Science
Real-time weather data and forecast for precision farming
"""

import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium
import sys
from pathlib import Path

# Add services to path
if str(Path(__file__).parent.parent) not in sys.path:
    sys.path.append(str(Path(__file__).parent.parent))

from services.weather_service import WeatherService

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
    from design_system import apply_design_system, icon, COLORS

st.set_page_config(page_title="Cuaca Lahan", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('cloud-sun', size='lg')} Monitoring Cuaca</h1>", unsafe_allow_html=True)
st.markdown("**Data cuaca presisi (Suhu, Hujan, Angin) untuk keputusan budidaya yang akurat**")
st.markdown("---")

# Layout
col_control, col_content = st.columns([1, 2])

with col_control:
    st.subheader(" Lokasi Lahan")
    
    # Initialize session state for lat/lon
    if 'lat' not in st.session_state: st.session_state.lat = -7.5 # Default Java
    if 'lon' not in st.session_state: st.session_state.lon = 110.5
    
    # Map
    m = folium.Map(location=[st.session_state.lat, st.session_state.lon], zoom_start=9)
    # Add marker
    folium.Marker([st.session_state.lat, st.session_state.lon], tooltip="Lokasi Sawah").add_to(m)
    # Click listener
    m.add_child(folium.LatLngPopup())
    
    map_output = st_folium(m, height=250, use_container_width=True)
    
    # Update lat/lon if map clicked (Check if not None first!)
    if map_output and map_output.get('last_clicked'):
        st.session_state.lat = map_output['last_clicked']['lat']
        st.session_state.lon = map_output['last_clicked']['lon']
        
    lat = st.number_input("Latitude", value=st.session_state.lat, format="%.6f")
    lon = st.number_input("Longitude", value=st.session_state.lon, format="%.6f")
    
    if st.button(" Update Cuaca", type="primary"):
        st.rerun()

    st.markdown("---")
    st.info(" **Tips:** Klik pada peta untuk memilih lokasi sawah Anda secara spesifik.")

with col_content:
    st.subheader(f"Data Cuaca Real-time")
    
    with st.spinner("Mengambil data satelit..."):
        service = WeatherService()
        weather = service.get_forecast(lat, lon)
        
    if weather:
        curr = weather['current']
        recs, alerts = service.get_agronomy_recommendation(curr)
        
        # 1. Alert System
        if alerts:
            for alert in alerts:
                st.error(alert)
        
        # 2. Main Metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Suhu", f"{curr['temp']} °C", "Udara")
        col2.metric("Curah Hujan", f"{curr['rain']} mm", "Jam terakhir")
        col3.metric("Kelembaban", f"{curr['humidity']} %", "RH")
        col4.metric("Angin", f"{curr['wind']} km/h", "Kecepatan")
        
        # 3. Recommendations
        st.markdown("### ‍ Rekomendasi Agronomis")
        if recs:
            for rec in recs:
                st.success(rec)
        
        # 4. Forecast Chart (Rainfall & Temp)
        st.markdown("###  Prakiraan 7 Hari Kedepan")
        
        df_daily = weather['daily']
        # Map weather codes to emoji (Simplified)
        def get_icon(code):
            if code <= 3: return ""
            elif code <= 65: return ""
            elif code > 65: return ""
            return ""
            
        df_daily['icon'] = df_daily['code'].apply(get_icon)
        
        # Create combo chart
        base = alt.Chart(df_daily).encode(x=alt.X('date:T', axis=alt.Axis(format='%a %d')))
        
        bar = base.mark_bar(color='#4FC3F7', opacity=0.6).encode(
            y=alt.Y('rain_sum', title='Curah Hujan (mm)'),
            tooltip=['date', 'rain_sum', 'temp_max']
        )
        
        line = base.mark_line(color='#FF7043', point=True).encode(
            y=alt.Y('temp_max', title='Suhu Max (°C)')
        )
        
        chart = (bar + line).resolve_scale(y='independent').properties(title="Tren Hujan & Suhu")
        
        st.altair_chart(chart, use_container_width=True)
        
        # Table View
        st.dataframe(
            df_daily[['date', 'icon', 'rain_sum', 'temp_max', 'wind_max', 'et0']],
            column_config={
                "date": "Tanggal",
                "icon": "Cuaca",
                "rain_sum": st.column_config.NumberColumn("Hujan (mm)", format="%.1f"),
                "temp_max": st.column_config.NumberColumn("Suhu Max (°C)", format="%.1f"),
                "wind_max": st.column_config.NumberColumn("Angin Max (km/h)", format="%.1f"),
                "et0": st.column_config.NumberColumn("Evapotranspirasi (mm)", format="%.1f")
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.error("Gagal mengambil data cuaca. Periksa koneksi internet.")
