"""
Weather Alerts & Warnings
Monitor extreme weather conditions and get alerts
"""
import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_current_weather, get_daily_forecast, get_hourly_forecast, get_weather_description

# Page configuration
st.set_page_config(
    page_title="Weather Alerts",
    page_icon="⚠️",
    layout="wide"
)

# Header
st.title("⚠️ Weather Alerts & Warnings")
st.markdown("**Monitor extreme weather conditions and get real-time alerts**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Sidebar - Alert thresholds
st.sidebar.markdown("### ⚙️ Alert Thresholds")

temp_high = st.sidebar.slider("High Temperature Alert (°C)", 25, 45, 35)
temp_low = st.sidebar.slider("Low Temperature Alert (°C)", -10, 15, 5)
wind_high = st.sidebar.slider("High Wind Speed Alert (km/h)", 30, 100, 50)
precip_high = st.sidebar.slider("High Precipitation Alert (mm)", 10, 100, 30)
humidity_high = st.sidebar.slider("High Humidity Alert (%)", 70, 100, 85)

# Fetch weather data
with st.spinner("Analyzing weather conditions..."):
    current_weather = get_current_weather(
        st.session_state['selected_lat'],
        st.session_state['selected_lon']
    )
    
    daily_forecast = get_daily_forecast(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        days=7
    )
    
    hourly_forecast = get_hourly_forecast(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        hours=24
    )

# Analyze alerts
alerts = []

if current_weather:
    # Temperature alerts
    if current_weather.get('temperature', 0) > temp_high:
        alerts.append({
            'severity': 'high',
            'type': 'Temperature',
            'icon': '🌡️',
            'title': 'High Temperature Warning',
            'message': f"Current temperature ({current_weather['temperature']:.1f}°C) exceeds threshold ({temp_high}°C)",
            'time': 'Now'
        })
    
    if current_weather.get('temperature', 100) < temp_low:
        alerts.append({
            'severity': 'high',
            'type': 'Temperature',
            'icon': '❄️',
            'title': 'Low Temperature Warning',
            'message': f"Current temperature ({current_weather['temperature']:.1f}°C) below threshold ({temp_low}°C)",
            'time': 'Now'
        })
    
    # Wind alerts
    if current_weather.get('wind_speed', 0) > wind_high:
        alerts.append({
            'severity': 'high',
            'type': 'Wind',
            'icon': '🌬️',
            'title': 'High Wind Speed Warning',
            'message': f"Wind speed ({current_weather['wind_speed']:.1f} km/h) exceeds threshold ({wind_high} km/h)",
            'time': 'Now'
        })
    
    # Humidity alerts
    if current_weather.get('humidity', 0) > humidity_high:
        alerts.append({
            'severity': 'medium',
            'type': 'Humidity',
            'icon': '💧',
            'title': 'High Humidity Alert',
            'message': f"Humidity ({current_weather['humidity']:.0f}%) exceeds threshold ({humidity_high}%)",
            'time': 'Now'
        })

# Check forecast for upcoming alerts
if daily_forecast is not None:
    for idx, row in daily_forecast.iterrows():
        day_name = row['time'].strftime('%A, %b %d')
        
        # High temperature forecast
        if row['temperature_2m_max'] > temp_high:
            alerts.append({
                'severity': 'medium',
                'type': 'Temperature',
                'icon': '🌡️',
                'title': f'High Temperature Expected - {day_name}',
                'message': f"Expected max temperature: {row['temperature_2m_max']:.1f}°C (threshold: {temp_high}°C)",
                'time': day_name
            })
        
        # High precipitation forecast
        if row['precipitation_sum'] > precip_high:
            alerts.append({
                'severity': 'medium',
                'type': 'Precipitation',
                'icon': '🌧️',
                'title': f'Heavy Rain Expected - {day_name}',
                'message': f"Expected precipitation: {row['precipitation_sum']:.1f} mm (threshold: {precip_high} mm)",
                'time': day_name
            })
        
        # High wind forecast
        if row['wind_speed_10m_max'] > wind_high:
            alerts.append({
                'severity': 'medium',
                'type': 'Wind',
                'icon': '🌬️',
                'title': f'Strong Winds Expected - {day_name}',
                'message': f"Expected wind speed: {row['wind_speed_10m_max']:.1f} km/h (threshold: {wind_high} km/h)",
                'time': day_name
            })

# Display alerts
st.markdown("## 🚨 Active Alerts")

if alerts:
    # Count by severity
    high_severity = len([a for a in alerts if a['severity'] == 'high'])
    medium_severity = len([a for a in alerts if a['severity'] == 'medium'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Alerts", len(alerts))
    with col2:
        st.metric("High Severity", high_severity, delta=None)
    with col3:
        st.metric("Medium Severity", medium_severity, delta=None)
    
    st.markdown("---")
    
    # Display alerts by severity
    high_alerts = [a for a in alerts if a['severity'] == 'high']
    medium_alerts = [a for a in alerts if a['severity'] == 'medium']
    
    if high_alerts:
        st.markdown("### 🔴 High Severity Alerts")
        for alert in high_alerts:
            st.markdown(f"""
            <div style="background: #fed7d7; border-left: 4px solid #e53e3e; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
                <h4 style="color: #c53030; margin: 0;">
                    {alert['icon']} {alert['title']}
                </h4>
                <p style="color: #742a2a; margin: 0.5rem 0 0 0;">
                    {alert['message']}
                </p>
                <p style="color: #9b2c2c; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                    <b>Time:</b> {alert['time']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    if medium_alerts:
        st.markdown("### 🟡 Medium Severity Alerts")
        for alert in medium_alerts:
            st.markdown(f"""
            <div style="background: #fef5e7; border-left: 4px solid #ed8936; padding: 1.5rem; border-radius: 8px; margin: 1rem 0;">
                <h4 style="color: #c05621; margin: 0;">
                    {alert['icon']} {alert['title']}
                </h4>
                <p style="color: #7c2d12; margin: 0.5rem 0 0 0;">
                    {alert['message']}
                </p>
                <p style="color: #9c4221; font-size: 0.9rem; margin: 0.5rem 0 0 0;">
                    <b>Time:</b> {alert['time']}
                </p>
            </div>
            """, unsafe_allow_html=True)
    
else:
    st.success("✅ No weather alerts at this time. Conditions are within normal ranges.")

st.markdown("---")

# Weather Safety Tips
st.markdown("## 💡 Weather Safety Tips")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🌡️ Extreme Temperature
    - **High Heat:** Stay hydrated, avoid outdoor activities during peak hours
    - **Cold:** Dress in layers, protect extremities
    - **Heat Index:** Consider both temperature and humidity
    
    ### 🌬️ High Winds
    - Secure loose objects outdoors
    - Avoid driving high-profile vehicles
    - Stay away from trees and power lines
    """)

with col2:
    st.markdown("""
    ### 🌧️ Heavy Precipitation
    - Avoid flood-prone areas
    - Don't drive through standing water
    - Keep emergency supplies ready
    
    ### ⛈️ Thunderstorms
    - Stay indoors during storms
    - Avoid using electrical appliances
    - Stay away from windows
    """)

st.markdown("---")

# Alert Statistics
if alerts:
    st.markdown("## 📊 Alert Statistics")
    
    # Count by type
    alert_types = pd.DataFrame(alerts)
    type_counts = alert_types['type'].value_counts()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Alerts by Type:**")
        for alert_type, count in type_counts.items():
            st.markdown(f"- **{alert_type}:** {count} alert(s)")
    
    with col2:
        st.markdown("**Alert Timeline:**")
        time_counts = alert_types['time'].value_counts()
        for time, count in time_counts.items():
            st.markdown(f"- **{time}:** {count} alert(s)")

st.markdown("---")

# Current Conditions Summary
if current_weather:
    st.markdown("## 🌤️ Current Conditions Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        temp_status = "🔴" if current_weather.get('temperature', 0) > temp_high or current_weather.get('temperature', 100) < temp_low else "🟢"
        st.metric(
            "Temperature",
            f"{current_weather.get('temperature', 'N/A')}°C",
            delta=f"{temp_status} Status"
        )
    
    with col2:
        wind_status = "🔴" if current_weather.get('wind_speed', 0) > wind_high else "🟢"
        st.metric(
            "Wind Speed",
            f"{current_weather.get('wind_speed', 'N/A')} km/h",
            delta=f"{wind_status} Status"
        )
    
    with col3:
        humidity_status = "🔴" if current_weather.get('humidity', 0) > humidity_high else "🟢"
        st.metric(
            "Humidity",
            f"{current_weather.get('humidity', 'N/A')}%",
            delta=f"{humidity_status} Status"
        )
    
    with col4:
        st.metric(
            "Pressure",
            f"{current_weather.get('pressure', 'N/A')} hPa",
            delta="🟢 Status"
        )

st.markdown("---")

# Quick navigation
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌤️ Current Weather", use_container_width=True):
        st.switch_page("pages/02_🌤️_Current_Weather.py")

with col2:
    if st.button("📅 7-Day Forecast", use_container_width=True):
        st.switch_page("pages/03_📅_7-Day_Forecast.py")

with col3:
    if st.button("🗺️ Change Location", use_container_width=True):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
