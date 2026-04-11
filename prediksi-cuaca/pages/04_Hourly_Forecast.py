"""
Hourly Weather Forecast
Detailed 48-hour weather predictions
"""
import streamlit as st
import sys
import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_hourly_forecast, get_weather_emoji, get_weather_description

# Page configuration
st.set_page_config(
    page_title="Hourly Forecast",
    page_icon="⏰",
    layout="wide"
)

# Header
st.title("⏰ Hourly Weather Forecast")
st.markdown("**Detailed 48-hour weather predictions**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Sidebar - Forecast hours selection
hours = st.sidebar.slider("Forecast Hours", min_value=12, max_value=48, value=24, step=6)

# Fetch hourly forecast
with st.spinner(f"Fetching {hours}-hour forecast..."):
    hourly_df = get_hourly_forecast(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        hours=hours
    )

if hourly_df is not None and len(hourly_df) > 0:
    # Temperature and Feels Like chart
    st.markdown("### 🌡️ Temperature & Feels Like")
    
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    
    fig.add_trace(
        go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['temperature_2m'],
            name='Temperature',
            line=dict(color='#e53e3e', width=2),
            mode='lines+markers'
        )
    )
    
    fig.add_trace(
        go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['apparent_temperature'],
            name='Feels Like',
            line=dict(color='#4299e1', width=2, dash='dash'),
            mode='lines'
        )
    )
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        xaxis_title='Time',
        yaxis_title='Temperature (°C)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Precipitation and Humidity
    st.markdown("### 💧 Precipitation & Humidity")
    
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig2.add_trace(
        go.Bar(
            x=hourly_df['time'],
            y=hourly_df['precipitation_probability'],
            name='Precipitation Probability',
            marker_color='#4299e1',
            opacity=0.6
        ),
        secondary_y=False
    )
    
    fig2.add_trace(
        go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['relative_humidity_2m'],
            name='Humidity',
            line=dict(color='#48bb78', width=2),
            mode='lines'
        ),
        secondary_y=True
    )
    
    fig2.update_xaxes(title_text='Time')
    fig2.update_yaxes(title_text='Precipitation Probability (%)', secondary_y=False)
    fig2.update_yaxes(title_text='Humidity (%)', secondary_y=True)
    
    fig2.update_layout(
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # Wind Speed
    st.markdown("### 🌬️ Wind Speed & Gusts")
    
    fig3 = go.Figure()
    
    fig3.add_trace(
        go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['wind_speed_10m'],
            name='Wind Speed',
            fill='tozeroy',
            line=dict(color='#9f7aea', width=2)
        )
    )
    
    fig3.add_trace(
        go.Scatter(
            x=hourly_df['time'],
            y=hourly_df['wind_gusts_10m'],
            name='Wind Gusts',
            line=dict(color='#ed8936', width=2, dash='dot')
        )
    )
    
    fig3.update_layout(
        height=350,
        hovermode='x unified',
        xaxis_title='Time',
        yaxis_title='Wind Speed (km/h)'
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # Hourly details table
    st.markdown("### 📋 Hourly Details")
    
    # Show every 3 hours for better readability
    display_df = hourly_df[::3].copy()
    display_df['Time'] = display_df['time'].dt.strftime('%m/%d %H:%M')
    display_df['Weather'] = display_df['weather_code'].apply(lambda x: f"{get_weather_emoji(x)} {get_weather_description(x)}")
    display_df['Temp'] = display_df['temperature_2m'].apply(lambda x: f"{x:.1f}°C")
    display_df['Feels'] = display_df['apparent_temperature'].apply(lambda x: f"{x:.1f}°C")
    display_df['Precip'] = display_df['precipitation_probability'].apply(lambda x: f"{x:.0f}%")
    display_df['Humidity'] = display_df['relative_humidity_2m'].apply(lambda x: f"{x:.0f}%")
    display_df['Wind'] = display_df['wind_speed_10m'].apply(lambda x: f"{x:.1f} km/h")
    
    st.dataframe(
        display_df[['Time', 'Weather', 'Temp', 'Feels', 'Precip', 'Humidity', 'Wind']],
        use_container_width=True,
        hide_index=True
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

else:
    st.error("❌ Unable to fetch hourly forecast data. Please try again or select a different location.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
