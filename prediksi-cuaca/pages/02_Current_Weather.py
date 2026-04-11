"""
Advanced Current Weather Dashboard
Comprehensive real-time weather information with advanced features
"""
import streamlit as st
import sys
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import pandas as pd
import numpy as np

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_current_weather, get_weather_emoji, get_weather_description, get_hourly_forecast
from utils.moon_phase import calculate_moon_phase

# Page configuration
st.set_page_config(
    page_title="Cuaca Saat Ini",
    page_icon="🌤️",
    layout="wide"
)

# Utility functions
def get_comfort_level(temp, humidity):
    """Calculate weather comfort level"""
    # Heat index calculation
    if temp >= 27:
        hi = -8.78469475556 + 1.61139411*temp + 2.33854883889*humidity
        hi += -0.14611605*temp*humidity + -0.012308094*temp*temp
        hi += -0.0164248277778*humidity*humidity + 0.002211732*temp*temp*humidity
        hi += 0.00072546*temp*humidity*humidity + -0.000003582*temp*temp*humidity*humidity
        
        if hi < 27:
            return "Nyaman", "#48bb78", "😊"
        elif hi < 32:
            return "Cukup Nyaman", "#ed8936", "😐"
        elif hi < 41:
            return "Tidak Nyaman", "#dd6b20", "😰"
        else:
            return "Sangat Tidak Nyaman", "#c53030", "🥵"
    else:
        if temp < 10:
            return "Dingin", "#4299e1", "🥶"
        elif temp < 20:
            return "Sejuk", "#48bb78", "😊"
        else:
            return "Nyaman", "#48bb78", "😊"

def get_uv_risk(hour):
    """Estimate UV risk based on time of day"""
    if 10 <= hour <= 16:
        return "Tinggi", "#e53e3e", "☀️"
    elif 8 <= hour < 10 or 16 < hour <= 18:
        return "Sedang", "#ed8936", "🌤️"
    else:
        return "Rendah", "#48bb78", "🌙"

def get_air_quality_estimate(visibility, humidity):
    """Estimate air quality from visibility and humidity"""
    if visibility > 10000:
        return "Baik", "#48bb78", "😊", 50
    elif visibility > 5000:
        return "Sedang", "#ed8936", "😐", 100
    else:
        return "Buruk", "#e53e3e", "😷", 150

# Custom CSS
st.markdown("""
<style>
    .weather-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        border: 2px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .comfort-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.5rem;
    }
    
    .alert-box {
        background: #fff5f5;
        border-left: 4px solid #e53e3e;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌤️ Dashboard Cuaca Saat Ini")
st.markdown("**Informasi cuaca real-time dengan analisis lengkap**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ Belum ada lokasi yang dipilih. Silakan pilih lokasi dari halaman Peta Interaktif terlebih dahulu.")
    if st.button("🗺️ Ke Peta Interaktif"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Lokasi:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Fetch current weather and hourly forecast
with st.spinner("Mengambil data cuaca..."):
    weather = get_current_weather(
        st.session_state['selected_lat'],
        st.session_state['selected_lon']
    )
    
    hourly_forecast = get_hourly_forecast(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        hours=12
    )

if weather:
    emoji = get_weather_emoji(weather.get('weather_code', 0))
    description = get_weather_description(weather.get('weather_code', 0))
    
    # Get current time from API
    timezone = weather.get('timezone', 'UTC')
    current_time_str = weather.get('time', '')
    
    if current_time_str:
        try:
            current_time = datetime.fromisoformat(current_time_str.replace('Z', '+00:00'))
            time_display = current_time.strftime('%H:%M:%S')
            date_display = current_time.strftime('%A, %d %B %Y')
            current_hour = current_time.hour
        except:
            current_time = datetime.now()
            time_display = current_time.strftime('%H:%M:%S')
            date_display = current_time.strftime('%A, %d %B %Y')
            current_hour = current_time.hour
    else:
        current_time = datetime.now()
        time_display = current_time.strftime('%H:%M:%S')
        date_display = current_time.strftime('%A, %d %B %Y')
        current_hour = current_time.hour
    
    # Calculate comfort and other indices
    temp = weather.get('temperature', 0)
    humidity = weather.get('humidity', 0)
    comfort_level, comfort_color, comfort_emoji = get_comfort_level(temp, humidity)
    uv_risk, uv_color, uv_emoji = get_uv_risk(current_hour)
    
    # Main weather hero section
    st.markdown(f"""
    <div class="weather-hero">
        <div style="font-size: 6rem; margin-bottom: 1rem;">{emoji}</div>
        <h2 style="margin: 0.5rem 0; font-size: 2rem;">{description}</h2>
        <h1 style="font-size: 5rem; margin: 1rem 0; font-weight: bold;">{temp}°C</h1>
        <p style="font-size: 1.3rem; opacity: 0.9;">Terasa seperti {weather.get('feels_like', 'N/A')}°C</p>
        <div style="margin-top: 1.5rem; font-size: 1rem; opacity: 0.8;">
            <p style="margin: 0.3rem 0;">{date_display}</p>
            <p style="margin: 0.3rem 0; font-size: 1.5rem; font-weight: bold;">{time_display}</p>
            <p style="margin: 0.3rem 0;">Zona Waktu: {timezone}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Comfort & Health Indicators
    st.markdown("## 🌡️ Indikator Kenyamanan & Kesehatan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: {comfort_color}22; padding: 1.5rem; border-radius: 12px; border: 2px solid {comfort_color};">
            <div style="font-size: 3rem; text-align: center;">{comfort_emoji}</div>
            <h3 style="text-align: center; color: {comfort_color}; margin: 0.5rem 0;">Tingkat Kenyamanan</h3>
            <p style="text-align: center; font-size: 1.2rem; font-weight: bold; margin: 0;">{comfort_level}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: {uv_color}22; padding: 1.5rem; border-radius: 12px; border: 2px solid {uv_color};">
            <div style="font-size: 3rem; text-align: center;">{uv_emoji}</div>
            <h3 style="text-align: center; color: {uv_color}; margin: 0.5rem 0;">Risiko UV</h3>
            <p style="text-align: center; font-size: 1.2rem; font-weight: bold; margin: 0;">{uv_risk}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Air quality estimate
        visibility = weather.get('cloud_cover', 50)  # Using cloud cover as proxy
        aq_level, aq_color, aq_emoji, aqi = get_air_quality_estimate(10000 - visibility*100, humidity)
        
        st.markdown(f"""
        <div style="background: {aq_color}22; padding: 1.5rem; border-radius: 12px; border: 2px solid {aq_color};">
            <div style="font-size: 3rem; text-align: center;">{aq_emoji}</div>
            <h3 style="text-align: center; color: {aq_color}; margin: 0.5rem 0;">Kualitas Udara</h3>
            <p style="text-align: center; font-size: 1.2rem; font-weight: bold; margin: 0;">{aq_level}</p>
            <p style="text-align: center; font-size: 0.9rem; color: #666; margin: 0.5rem 0;">AQI: ~{aqi}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed Current Conditions
    st.markdown("## 📊 Kondisi Detail Saat Ini")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "💧 Kelembaban",
            f"{humidity}%",
            delta="Optimal" if 40 <= humidity <= 60 else "Tinggi" if humidity > 60 else "Rendah"
        )
    
    with col2:
        wind_speed = weather.get('wind_speed', 0)
        st.metric(
            "🌬️ Kecepatan Angin",
            f"{wind_speed:.1f} km/jam",
            delta="Kencang" if wind_speed > 30 else "Tenang"
        )
    
    with col3:
        pressure = weather.get('pressure', 0)
        st.metric(
            "🔽 Tekanan Udara",
            f"{pressure:.0f} hPa",
            delta="Tinggi" if pressure > 1013 else "Rendah"
        )
    
    with col4:
        cloud_cover = weather.get('cloud_cover', 0)
        st.metric(
            "☁️ Tutupan Awan",
            f"{cloud_cover}%",
            delta="Mendung" if cloud_cover > 75 else "Cerah"
        )
    
    st.markdown("---")
    
    # Atmospheric Analysis
    st.markdown("## 🌍 Analisis Atmosfer")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create gauge chart for humidity
        fig_humidity = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=humidity,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Kelembaban Relatif (%)"},
            delta={'reference': 50},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "#3498db"},
                'steps': [
                    {'range': [0, 30], 'color': "#ffeaa7"},
                    {'range': [30, 60], 'color': "#55efc4"},
                    {'range': [60, 100], 'color': "#74b9ff"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        
        fig_humidity.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_humidity, use_container_width=True)
    
    with col2:
        # Create gauge chart for pressure
        fig_pressure = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=pressure,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Tekanan Atmosfer (hPa)"},
            delta={'reference': 1013},
            gauge={
                'axis': {'range': [950, 1050]},
                'bar': {'color': "#9b59b6"},
                'steps': [
                    {'range': [950, 1000], 'color': "#ffcccc"},
                    {'range': [1000, 1020], 'color': "#ccffcc"},
                    {'range': [1020, 1050], 'color': "#ccccff"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 1030
                }
            }
        ))
        
        fig_pressure.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_pressure, use_container_width=True)
    
    st.markdown("---")
    
    # Wind Analysis
    st.markdown("## 💨 Analisis Angin")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Wind compass
        wind_direction = weather.get('wind_direction', 0)
        wind_gusts = weather.get('wind_gusts', 0)
        
        # Create wind rose
        fig_wind = go.Figure()
        
        fig_wind.add_trace(go.Scatterpolar(
            r=[wind_speed],
            theta=[wind_direction],
            mode='markers',
            marker=dict(size=20, color='#e74c3c'),
            name='Angin Saat Ini'
        ))
        
        fig_wind.update_layout(
            polar=dict(
                radialaxis=dict(range=[0, max(50, wind_speed + 10)], showticklabels=True),
                angularaxis=dict(direction="clockwise")
            ),
            title="Kompas Angin",
            height=400
        )
        
        st.plotly_chart(fig_wind, use_container_width=True)
    
    with col2:
        st.markdown("### 🌬️ Detail Angin")
        
        # Wind direction in text
        directions = ['Utara', 'Timur Laut', 'Timur', 'Tenggara', 'Selatan', 'Barat Daya', 'Barat', 'Barat Laut']
        direction_idx = int((wind_direction + 22.5) / 45) % 8
        direction_text = directions[direction_idx]
        
        st.markdown(f"""
        <div style="background: #f7fafc; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
            <h4 style="margin: 0 0 1rem 0;">Informasi Angin</h4>
            <p style="margin: 0.5rem 0;"><strong>Arah:</strong> {direction_text} ({wind_direction}°)</p>
            <p style="margin: 0.5rem 0;"><strong>Kecepatan:</strong> {wind_speed:.1f} km/jam</p>
            <p style="margin: 0.5rem 0;"><strong>Hembusan:</strong> {wind_gusts:.1f} km/jam</p>
            <p style="margin: 0.5rem 0;"><strong>Skala Beaufort:</strong> {min(12, int(wind_speed / 5))}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Wind strength indicator
        if wind_speed < 5:
            wind_desc = "Tenang - Ideal untuk aktivitas luar ruangan"
        elif wind_speed < 20:
            wind_desc = "Sepoi-sepoi - Nyaman untuk aktivitas"
        elif wind_speed < 40:
            wind_desc = "Sedang - Berhati-hati saat beraktivitas"
        else:
            wind_desc = "Kencang - Hindari aktivitas luar ruangan"
        
        st.info(f"💨 **{wind_desc}**")
    
    st.markdown("---")
    
    # Hourly Mini Forecast
    if hourly_forecast is not None and len(hourly_forecast) > 0:
        st.markdown("## ⏰ Prakiraan 12 Jam Ke Depan")
        
        hourly_forecast['time'] = pd.to_datetime(hourly_forecast['time'])
        hourly_forecast['hour'] = hourly_forecast['time'].dt.strftime('%H:%M')
        
        # Create hourly forecast chart
        fig_hourly = make_subplots(
            rows=2, cols=1,
            row_heights=[0.6, 0.4],
            subplot_titles=('Suhu & Terasa Seperti', 'Kemungkinan Hujan'),
            vertical_spacing=0.15
        )
        
        # Temperature
        fig_hourly.add_trace(
            go.Scatter(
                x=hourly_forecast['time'],
                y=hourly_forecast['temperature_2m'],
                name='Suhu Aktual',
                line=dict(color='#e74c3c', width=3),
                mode='lines+markers'
            ),
            row=1, col=1
        )
        
        fig_hourly.add_trace(
            go.Scatter(
                x=hourly_forecast['time'],
                y=hourly_forecast['apparent_temperature'],
                name='Terasa Seperti',
                line=dict(color='#3498db', width=2, dash='dash'),
                mode='lines'
            ),
            row=1, col=1
        )
        
        # Precipitation probability
        fig_hourly.add_trace(
            go.Bar(
                x=hourly_forecast['time'],
                y=hourly_forecast['precipitation_probability'],
                name='Kemungkinan Hujan',
                marker_color='#3498db',
                opacity=0.7
            ),
            row=2, col=1
        )
        
        fig_hourly.update_xaxes(title_text="Waktu", row=2, col=1)
        fig_hourly.update_yaxes(title_text="Suhu (°C)", row=1, col=1)
        fig_hourly.update_yaxes(title_text="Kemungkinan (%)", range=[0, 100], row=2, col=1)
        
        fig_hourly.update_layout(
            height=500,
            hovermode='x unified',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig_hourly, use_container_width=True)
    
    st.markdown("---")
    
    # Astronomical Data
    st.markdown("## 🌙 Data Astronomi")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        sunrise = weather.get('sunrise', '')
        sunset = weather.get('sunset', '')
        
        if sunrise and sunset:
            try:
                sunrise_time = datetime.fromisoformat(sunrise.replace('Z', '+00:00')).strftime('%H:%M')
                sunset_time = datetime.fromisoformat(sunset.replace('Z', '+00:00')).strftime('%H:%M')
            except:
                sunrise_time = "N/A"
                sunset_time = "N/A"
        else:
            sunrise_time = "N/A"
            sunset_time = "N/A"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 1.5rem; border-radius: 12px; color: white;">
            <h4 style="margin: 0 0 1rem 0;">☀️ Matahari</h4>
            <p style="margin: 0.5rem 0;"><strong>Terbit:</strong> {sunrise_time}</p>
            <p style="margin: 0.5rem 0;"><strong>Terbenam:</strong> {sunset_time}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        sunshine_duration = weather.get('sunshine_duration', 0)
        sunshine_hours = sunshine_duration / 3600 if sunshine_duration else 0
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 1.5rem; border-radius: 12px; color: white;">
            <h4 style="margin: 0 0 1rem 0;">🌞 Durasi Sinar</h4>
            <p style="margin: 0.5rem 0;"><strong>Hari Ini:</strong> {sunshine_hours:.1f} jam</p>
            <p style="margin: 0.5rem 0;"><strong>Persentase:</strong> {(sunshine_hours/12*100):.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        moon_phase = calculate_moon_phase()
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); padding: 1.5rem; border-radius: 12px; color: #2c3e50;">
            <h4 style="margin: 0 0 1rem 0;">🌙 Fase Bulan</h4>
            <div style="font-size: 3rem; text-align: center; margin: 0.5rem 0;">{moon_phase['emoji']}</div>
            <p style="margin: 0.5rem 0; text-align: center;"><strong>{moon_phase['phase_name']}</strong></p>
            <p style="margin: 0.5rem 0; text-align: center; font-size: 0.9rem;">Iluminasi: {moon_phase['illumination']:.0f}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Weather Alerts & Recommendations
    st.markdown("## ⚠️ Rekomendasi & Peringatan")
    
    alerts = []
    
    # Temperature alerts
    if temp > 35:
        alerts.append(("🔥 Suhu Sangat Panas", "Hindari aktivitas berat di luar ruangan. Minum banyak air.", "#e53e3e"))
    elif temp < 10:
        alerts.append(("🥶 Suhu Dingin", "Kenakan pakaian hangat saat keluar.", "#4299e1"))
    
    # Wind alerts
    if wind_speed > 40:
        alerts.append(("💨 Angin Kencang", "Berhati-hati saat berkendara. Amankan barang-barang ringan.", "#ed8936"))
    
    # Humidity alerts
    if humidity > 80:
        alerts.append(("💧 Kelembaban Tinggi", "Udara terasa lembab. Gunakan AC atau dehumidifier.", "#3498db"))
    elif humidity < 30:
        alerts.append(("🏜️ Kelembaban Rendah", "Udara kering. Gunakan pelembab udara.", "#f39c12"))
    
    # UV alerts
    if uv_risk == "Tinggi":
        alerts.append(("☀️ Risiko UV Tinggi", "Gunakan tabir surya SPF 30+. Hindari sinar matahari langsung 10:00-16:00.", "#e67e22"))
    
    if alerts:
        for title, message, color in alerts:
            st.markdown(f"""
            <div style="background: {color}22; border-left: 4px solid {color}; padding: 1rem; border-radius: 4px; margin: 0.5rem 0;">
                <h4 style="margin: 0 0 0.5rem 0; color: {color};">{title}</h4>
                <p style="margin: 0; color: #2c3e50;">{message}</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Tidak ada peringatan cuaca. Kondisi aman untuk beraktivitas.")
    
    st.markdown("---")
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📅 Prakiraan 7 Hari", use_container_width=True):
            st.switch_page("pages/03_📅_7-Day_Forecast.py")
    
    with col2:
        if st.button("📡 Radar Cuaca", use_container_width=True):
            st.switch_page("pages/10_📡_Weather_Radar.py")
    
    with col3:
        if st.button("🗺️ Ganti Lokasi", use_container_width=True):
            st.switch_page("pages/01_🗺️_Interactive_Map.py")

else:
    st.error("❌ Tidak dapat mengambil data cuaca. Silakan coba lagi.")
    if st.button("🗺️ Pilih Lokasi Lain"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
