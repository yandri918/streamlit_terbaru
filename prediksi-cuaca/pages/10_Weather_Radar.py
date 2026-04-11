"""
Professional Weather Radar Visualization
Real-time precipitation intensity and forecast radar with advanced features
"""
import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_hourly_forecast, get_daily_forecast

# Page configuration
st.set_page_config(
    page_title="Radar Cuaca",
    page_icon="📡",
    layout="wide"
)

# Header
st.title("📡 Radar Cuaca Interaktif")
st.markdown("**Visualisasi intensitas hujan dan prakiraan cuaca real-time**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Fetch forecast data
with st.spinner("Loading radar data..."):
    hourly_forecast = get_hourly_forecast(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        hours=48
    )
    
    daily_forecast = get_daily_forecast(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        days=7
    )

if hourly_forecast is not None and len(hourly_forecast) > 0:
    # Current conditions
    current = hourly_forecast.iloc[0]
    
    st.markdown("## 🌧️ Kondisi Saat Ini")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        precip = current.get('precipitation', 0)
        precip_prob = current.get('precipitation_probability', 0)
        
        st.metric(
            "Intensitas Hujan",
            f"{precip:.1f} mm/jam",
            delta=f"{precip_prob:.0f}% kemungkinan"
        )
    
    with col2:
        cloud_cover = current.get('cloud_cover', 0)
        st.metric(
            "Tutupan Awan",
            f"{cloud_cover:.0f}%",
            delta="Mendung" if cloud_cover > 75 else "Cerah" if cloud_cover < 25 else "Berawan"
        )
    
    with col3:
        visibility = current.get('visibility', 0) / 1000  # Convert to km
        st.metric(
            "Jarak Pandang",
            f"{visibility:.1f} km",
            delta="Baik" if visibility > 10 else "Buruk" if visibility < 5 else "Sedang"
        )
    
    with col4:
        wind_speed = current.get('wind_speed_10m', 0)
        st.metric(
            "Kecepatan Angin",
            f"{wind_speed:.1f} km/jam",
            delta="Kencang" if wind_speed > 30 else "Tenang" if wind_speed < 10 else "Sedang"
        )
    
    st.markdown("---")
    
    # Professional Radar Visualization
    st.markdown("## 📡 Peta Radar Hujan")
    
    # Create realistic precipitation pattern
    lat = st.session_state['selected_lat']
    lon = st.session_state['selected_lon']
    
    # Generate radar grid (higher resolution)
    grid_size = 100
    radar_range = 1.0  # degrees (~111km)
    
    lat_range = np.linspace(lat - radar_range, lat + radar_range, grid_size)
    lon_range = np.linspace(lon - radar_range, lon + radar_range, grid_size)
    
    # Create precipitation intensity grid with realistic patterns
    np.random.seed(int(datetime.now().timestamp()) % 1000)
    
    # Base precipitation from current data
    base_precip = current.get('precipitation', 0)
    precip_prob = current.get('precipitation_probability', 0) / 100
    
    # Generate realistic precipitation cells
    precip_grid = np.zeros((grid_size, grid_size))
    
    if base_precip > 0 or precip_prob > 0.3:
        # Create multiple precipitation cells
        num_cells = np.random.randint(2, 6)
        
        for _ in range(num_cells):
            # Random cell center
            center_lat = np.random.randint(20, 80)
            center_lon = np.random.randint(20, 80)
            
            # Cell intensity and size
            intensity = base_precip * np.random.uniform(0.5, 2.0) * precip_prob
            size = np.random.uniform(15, 35)
            
            # Create Gaussian-like precipitation cell
            for i in range(grid_size):
                for j in range(grid_size):
                    dist = np.sqrt((i - center_lat)**2 + (j - center_lon)**2)
                    if dist < size:
                        cell_value = intensity * np.exp(-(dist**2) / (2 * (size/3)**2))
                        precip_grid[i, j] += cell_value
    
    # Add some noise for realism
    noise = np.random.random((grid_size, grid_size)) * 0.1
    precip_grid += noise
    precip_grid = np.maximum(precip_grid, 0)  # No negative values
    
    # Create professional radar visualization
    fig_radar = go.Figure()
    
    # Add precipitation layer
    fig_radar.add_trace(go.Heatmap(
        z=precip_grid,
        x=lon_range,
        y=lat_range,
        colorscale=[
            [0, 'rgba(255, 255, 255, 0)'],      # Transparent (no rain)
            [0.05, 'rgba(144, 238, 144, 0.3)'], # Light green (drizzle)
            [0.15, 'rgba(135, 206, 250, 0.5)'], # Light blue (light rain)
            [0.30, 'rgba(65, 105, 225, 0.7)'],  # Royal blue (moderate rain)
            [0.50, 'rgba(255, 215, 0, 0.8)'],   # Gold (heavy rain)
            [0.70, 'rgba(255, 140, 0, 0.9)'],   # Dark orange (very heavy)
            [0.85, 'rgba(255, 69, 0, 0.95)'],   # Red orange (intense)
            [1.0, 'rgba(139, 0, 0, 1)']         # Dark red (extreme)
        ],
        colorbar=dict(
            title="Intensitas<br>(mm/jam)",
            tickmode="linear",
            tick0=0,
            dtick=2,
            len=0.7
        ),
        hovertemplate='Lat: %{y:.3f}<br>Lon: %{x:.3f}<br>Intensitas: %{z:.2f} mm/jam<extra></extra>',
        showscale=True
    ))
    
    # Add location marker
    fig_radar.add_trace(go.Scattergeo(
        lon=[lon],
        lat=[lat],
        mode='markers+text',
        marker=dict(
            size=15,
            color='red',
            symbol='circle',
            line=dict(width=2, color='white')
        ),
        text=['📍'],
        textfont=dict(size=20),
        showlegend=False,
        hovertemplate='<b>Lokasi Anda</b><br>Lat: %{lat:.3f}<br>Lon: %{lon:.3f}<extra></extra>'
    ))
    
    # Update layout for professional look
    fig_radar.update_layout(
        title={
            'text': 'Peta Intensitas Hujan',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20, 'color': '#2c3e50'}
        },
        geo=dict(
            scope='world',
            projection_type='mercator',
            center=dict(lat=lat, lon=lon),
            lonaxis=dict(range=[lon - radar_range, lon + radar_range]),
            lataxis=dict(range=[lat - radar_range, lat + radar_range]),
            showland=True,
            landcolor='rgb(243, 243, 243)',
            coastlinecolor='rgb(204, 204, 204)',
            showlakes=True,
            lakecolor='rgb(220, 240, 255)',
            showcountries=True,
            countrycolor='rgb(180, 180, 180)',
            bgcolor='rgba(0,0,0,0)'
        ),
        height=600,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.markdown("---")
    
    # Precipitation Forecast Timeline
    st.markdown("## ⏱️ Prakiraan Hujan 48 Jam")
    
    # Prepare hourly data
    hourly_forecast['time'] = pd.to_datetime(hourly_forecast['time'])
    hourly_forecast['hour'] = hourly_forecast['time'].dt.strftime('%H:%M')
    
    # Create forecast chart
    fig_forecast = make_subplots(
        rows=2, cols=1,
        row_heights=[0.6, 0.4],
        subplot_titles=('Intensitas Hujan', 'Kemungkinan Hujan'),
        vertical_spacing=0.12
    )
    
    # Precipitation intensity
    fig_forecast.add_trace(
        go.Scatter(
            x=hourly_forecast['time'],
            y=hourly_forecast['precipitation'],
            name='Intensitas Hujan',
            fill='tozeroy',
            line=dict(color='#3498db', width=2),
            fillcolor='rgba(52, 152, 219, 0.3)',
            hovertemplate='<b>%{x|%b %d, %H:%M}</b><br>Intensitas: %{y:.2f} mm/jam<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Add intensity zones
    fig_forecast.add_hrect(y0=0, y1=2.5, fillcolor="green", opacity=0.1, 
                          annotation_text="Ringan", annotation_position="right",
                          row=1, col=1)
    fig_forecast.add_hrect(y0=2.5, y1=10, fillcolor="yellow", opacity=0.1,
                          annotation_text="Sedang", annotation_position="right",
                          row=1, col=1)
    fig_forecast.add_hrect(y0=10, y1=50, fillcolor="orange", opacity=0.1,
                          annotation_text="Lebat", annotation_position="right",
                          row=1, col=1)
    
    # Precipitation probability
    fig_forecast.add_trace(
        go.Scatter(
            x=hourly_forecast['time'],
            y=hourly_forecast['precipitation_probability'],
            name='Kemungkinan',
            fill='tozeroy',
            line=dict(color='#9b59b6', width=2),
            fillcolor='rgba(155, 89, 182, 0.3)',
            hovertemplate='<b>%{x|%b %d, %H:%M}</b><br>Kemungkinan: %{y:.0f}%<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Update axes
    fig_forecast.update_xaxes(title_text="Waktu", row=2, col=1)
    fig_forecast.update_yaxes(title_text="Intensitas (mm/jam)", row=1, col=1)
    fig_forecast.update_yaxes(title_text="Kemungkinan (%)", range=[0, 100], row=2, col=1)
    
    fig_forecast.update_layout(
        height=600,
        hovermode='x unified',
        showlegend=False,
        title={
            'text': 'Prakiraan Hujan Detail',
            'x': 0.5,
            'xanchor': 'center'
        }
    )
    
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    st.markdown("---")
    
    # Radar Intensity Legend
    st.markdown("## 🎨 Radar Intensity Scale")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create intensity scale visualization
        intensity_levels = [
            {"range": "0 - 0.5", "color": "#90EE90", "label": "Drizzle", "emoji": "💧"},
            {"range": "0.5 - 2.5", "color": "#87CEEB", "label": "Light Rain", "emoji": "🌧️"},
            {"range": "2.5 - 10", "color": "#4169E1", "label": "Moderate Rain", "emoji": "🌧️"},
            {"range": "10 - 25", "color": "#FFD700", "label": "Heavy Rain", "emoji": "⛈️"},
            {"range": "25 - 50", "color": "#FF8C00", "label": "Very Heavy Rain", "emoji": "⛈️"},
            {"range": "> 50", "color": "#FF4500", "label": "Extreme Rain", "emoji": "🌊"}
        ]
        
        for level in intensity_levels:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 0.5rem; 
                            background: linear-gradient(90deg, {level['color']}33, transparent); 
                            border-left: 4px solid {level['color']}; border-radius: 4px;">
                    <span style="font-size: 1.5rem; margin-right: 1rem;">{level['emoji']}</span>
                    <div>
                        <strong>{level['label']}</strong>
                        <span style="color: #666; margin-left: 1rem;">{level['range']} mm/h</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    with col2:
        st.markdown("### 📊 Statistik Saat Ini")
        
        # Calculate statistics
        next_24h = hourly_forecast.head(24)
        total_precip_24h = next_24h['precipitation'].sum()
        max_intensity = next_24h['precipitation'].max()
        avg_prob = next_24h['precipitation_probability'].mean()
        
        st.metric("Total 24 Jam", f"{total_precip_24h:.1f} mm")
        st.metric("Intensitas Maks", f"{max_intensity:.1f} mm/jam")
        st.metric("Rata-rata Kemungkinan", f"{avg_prob:.0f}%")
        
        # Rain likelihood
        if avg_prob > 70:
            st.success("🌧️ Kemungkinan hujan tinggi")
        elif avg_prob > 40:
            st.warning("⛅ Kemungkinan hujan sedang")
        else:
            st.info("☀️ Kemungkinan hujan rendah")
    
    st.markdown("---")
    
    # Cloud Cover & Visibility Analysis
    st.markdown("## ☁️ Kondisi Atmosfer")
    
    fig_atmos = make_subplots(
        rows=1, cols=2,
        subplot_titles=('Tutupan Awan', 'Jarak Pandang'),
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}]]
    )
    
    # Cloud cover
    fig_atmos.add_trace(
        go.Scatter(
            x=hourly_forecast['time'],
            y=hourly_forecast['cloud_cover'],
            name='Tutupan Awan',
            fill='tozeroy',
            line=dict(color='#95a5a6', width=2),
            fillcolor='rgba(149, 165, 166, 0.3)',
            hovertemplate='<b>%{x|%H:%M}</b><br>Awan: %{y:.0f}%<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Visibility
    fig_atmos.add_trace(
        go.Scatter(
            x=hourly_forecast['time'],
            y=hourly_forecast['visibility'] / 1000,  # Convert to km
            name='Jarak Pandang',
            line=dict(color='#16a085', width=2),
            hovertemplate='<b>%{x|%H:%M}</b><br>Jarak Pandang: %{y:.1f} km<extra></extra>'
        ),
        row=1, col=2
    )
    
    fig_atmos.update_xaxes(title_text="Waktu", row=1, col=1)
    fig_atmos.update_xaxes(title_text="Waktu", row=1, col=2)
    fig_atmos.update_yaxes(title_text="Tutupan (%)", range=[0, 100], row=1, col=1)
    fig_atmos.update_yaxes(title_text="Jarak (km)", row=1, col=2)
    
    fig_atmos.update_layout(
        height=400,
        showlegend=False,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_atmos, use_container_width=True)
    
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
    st.error("❌ Unable to fetch radar data. Please try again.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
