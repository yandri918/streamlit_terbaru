"""
Historical Weather Analysis
Analyze weather trends and patterns over time
"""
import streamlit as st
import sys
import os
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_historical_weather, get_weather_emoji, get_weather_description

# Page configuration
st.set_page_config(
    page_title="Historical Analysis",
    page_icon="📊",
    layout="wide"
)

# Header
st.title("📊 Historical Weather Analysis")
st.markdown("**Analyze weather trends and patterns over time**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Sidebar - Date range selection
st.sidebar.markdown("### 📅 Select Date Range")

date_range = st.sidebar.selectbox(
    "Quick Select",
    ["Last 7 Days", "Last 14 Days", "Last 30 Days", "Custom Range"]
)

if date_range == "Custom Range":
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now() - timedelta(days=1)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now() - timedelta(days=1),
            max_value=datetime.now() - timedelta(days=1)
        )
else:
    days_map = {
        "Last 7 Days": 7,
        "Last 14 Days": 14,
        "Last 30 Days": 30
    }
    days = days_map[date_range]
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=days)

# Fetch historical data
with st.spinner(f"Fetching historical data from {start_date} to {end_date}..."):
    historical_df = get_historical_weather(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

if historical_df is not None and len(historical_df) > 0:
    # Statistics Summary
    st.markdown("### 📈 Statistical Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_temp = historical_df['temperature_2m_mean'].mean()
        st.metric(
            "Average Temperature",
            f"{avg_temp:.1f}°C",
            delta=None
        )
    
    with col2:
        max_temp = historical_df['temperature_2m_max'].max()
        st.metric(
            "Highest Temperature",
            f"{max_temp:.1f}°C",
            delta=None
        )
    
    with col3:
        min_temp = historical_df['temperature_2m_min'].min()
        st.metric(
            "Lowest Temperature",
            f"{min_temp:.1f}°C",
            delta=None
        )
    
    with col4:
        total_precip = historical_df['precipitation_sum'].sum()
        st.metric(
            "Total Precipitation",
            f"{total_precip:.1f} mm",
            delta=None
        )
    
    st.markdown("---")
    
    # Temperature Trends
    st.markdown("### 🌡️ Temperature Trends Over Time")
    
    # Prepare data
    chart_data = historical_df.copy()
    chart_data['date'] = pd.to_datetime(chart_data['time'])
    
    # Create multi-line chart
    base = alt.Chart(chart_data).encode(
        x=alt.X('date:T', title='Date')
    )
    
    max_line = base.mark_line(color='#e53e3e', strokeWidth=2).encode(
        y=alt.Y('temperature_2m_max:Q', title='Temperature (°C)'),
        tooltip=['date:T', 'temperature_2m_max:Q', 'temperature_2m_min:Q', 'temperature_2m_mean:Q']
    )
    
    min_line = base.mark_line(color='#4299e1', strokeWidth=2).encode(
        y='temperature_2m_min:Q'
    )
    
    mean_line = base.mark_line(color='#48bb78', strokeWidth=2, strokeDash=[5, 5]).encode(
        y='temperature_2m_mean:Q'
    )
    
    # Area between max and min
    area = base.mark_area(opacity=0.2, color='#cbd5e0').encode(
        y='temperature_2m_max:Q',
        y2='temperature_2m_min:Q'
    )
    
    temp_chart = (area + max_line + min_line + mean_line).properties(
        height=400
    ).interactive()
    
    st.altair_chart(temp_chart, use_container_width=True)
    
    # Legend
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔴 **Max Temperature**")
    with col2:
        st.markdown("🔵 **Min Temperature**")
    with col3:
        st.markdown("🟢 **Mean Temperature** (dashed)")
    
    st.markdown("---")
    
    # Precipitation Analysis
    st.markdown("### 💧 Precipitation Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Daily precipitation bar chart
        precip_chart = alt.Chart(chart_data).mark_bar().encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('precipitation_sum:Q', title='Precipitation (mm)'),
            color=alt.Color('precipitation_sum:Q', scale=alt.Scale(scheme='blues'), legend=None),
            tooltip=['date:T', 'precipitation_sum:Q']
        ).properties(
            height=300,
            title='Daily Precipitation'
        )
        
        st.altair_chart(precip_chart, use_container_width=True)
    
    with col2:
        # Precipitation statistics
        rainy_days = len(chart_data[chart_data['precipitation_sum'] > 0])
        avg_precip = chart_data[chart_data['precipitation_sum'] > 0]['precipitation_sum'].mean()
        max_precip = chart_data['precipitation_sum'].max()
        
        st.markdown(f"""
        **Precipitation Statistics:**
        
        - **Rainy Days:** {rainy_days} days ({rainy_days/len(chart_data)*100:.1f}%)
        - **Average Precipitation** (on rainy days): {avg_precip:.1f} mm
        - **Maximum Daily Precipitation:** {max_precip:.1f} mm
        - **Total Precipitation:** {total_precip:.1f} mm
        """)
    
    st.markdown("---")
    
    # Temperature Distribution
    st.markdown("### 📊 Temperature Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Histogram
        hist_chart = alt.Chart(chart_data).mark_bar(opacity=0.7).encode(
            x=alt.X('temperature_2m_mean:Q', bin=alt.Bin(maxbins=20), title='Temperature (°C)'),
            y=alt.Y('count()', title='Frequency'),
            color=alt.value('#667eea')
        ).properties(
            height=300,
            title='Temperature Distribution'
        )
        
        st.altair_chart(hist_chart, use_container_width=True)
    
    with col2:
        # Box plot using Plotly
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=chart_data['temperature_2m_max'],
            name='Max Temp',
            marker_color='#e53e3e'
        ))
        
        fig.add_trace(go.Box(
            y=chart_data['temperature_2m_mean'],
            name='Mean Temp',
            marker_color='#48bb78'
        ))
        
        fig.add_trace(go.Box(
            y=chart_data['temperature_2m_min'],
            name='Min Temp',
            marker_color='#4299e1'
        ))
        
        fig.update_layout(
            title='Temperature Box Plot',
            yaxis_title='Temperature (°C)',
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Wind Speed Analysis
    st.markdown("### 🌬️ Wind Speed Analysis")
    
    wind_chart = alt.Chart(chart_data).mark_area(
        line={'color': '#9f7aea'},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color='#9f7aea', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('wind_speed_10m_max:Q', title='Max Wind Speed (km/h)'),
        tooltip=['date:T', 'wind_speed_10m_max:Q']
    ).properties(
        height=300
    )
    
    st.altair_chart(wind_chart, use_container_width=True)
    
    # Wind statistics
    avg_wind = chart_data['wind_speed_10m_max'].mean()
    max_wind = chart_data['wind_speed_10m_max'].max()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Average Max Wind Speed", f"{avg_wind:.1f} km/h")
    with col2:
        st.metric("Highest Wind Speed", f"{max_wind:.1f} km/h")
    
    st.markdown("---")
    
    # Data Table
    st.markdown("### 📋 Historical Data Table")
    
    display_df = chart_data.copy()
    display_df['Date'] = display_df['date'].dt.strftime('%Y-%m-%d (%A)')
    display_df['Weather'] = display_df['weather_code'].apply(lambda x: f"{get_weather_emoji(x)} {get_weather_description(x)}")
    display_df['Temp Range'] = display_df.apply(lambda x: f"{x['temperature_2m_min']:.1f}° - {x['temperature_2m_max']:.1f}°", axis=1)
    display_df['Avg Temp'] = display_df['temperature_2m_mean'].apply(lambda x: f"{x:.1f}°C")
    display_df['Precipitation'] = display_df['precipitation_sum'].apply(lambda x: f"{x:.1f} mm")
    display_df['Max Wind'] = display_df['wind_speed_10m_max'].apply(lambda x: f"{x:.1f} km/h")
    
    st.dataframe(
        display_df[['Date', 'Weather', 'Temp Range', 'Avg Temp', 'Precipitation', 'Max Wind']],
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = display_df[['Date', 'Weather', 'Temp Range', 'Avg Temp', 'Precipitation', 'Max Wind']].to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"weather_history_{start_date}_{end_date}.csv",
        mime="text/csv"
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
    st.error("❌ Unable to fetch historical data. Please try again or select a different date range.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
