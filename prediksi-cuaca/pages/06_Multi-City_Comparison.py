"""
Multi-City Weather Comparison
Compare weather conditions across multiple cities
"""
import streamlit as st
import sys
import os
import pandas as pd
import altair as alt
import plotly.graph_objects as go

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_current_weather, search_city, get_daily_forecast, get_weather_emoji, get_weather_description
from utils.map_utils import POPULAR_CITIES

# Page configuration
st.set_page_config(
    page_title="Multi-City Comparison",
    page_icon="🌍",
    layout="wide"
)

# Header
st.title("🌍 Multi-City Weather Comparison")
st.markdown("**Compare weather conditions across multiple cities simultaneously**")
st.markdown("---")

# Initialize session state for cities
if 'comparison_cities' not in st.session_state:
    st.session_state['comparison_cities'] = []

# Sidebar - Add cities
st.sidebar.markdown("### ➕ Add Cities to Compare")

# Quick add from popular cities
st.sidebar.markdown("**Popular Cities:**")
for city in POPULAR_CITIES[:5]:
    if st.sidebar.button(f"➕ {city['name']}", key=f"add_{city['name']}"):
        if len(st.session_state['comparison_cities']) < 5:
            city_data = {
                'name': city['name'],
                'lat': city['lat'],
                'lon': city['lon']
            }
            if city_data not in st.session_state['comparison_cities']:
                st.session_state['comparison_cities'].append(city_data)
                st.rerun()
        else:
            st.sidebar.warning("Maximum 5 cities allowed")

# Search and add custom city
st.sidebar.markdown("---")
st.sidebar.markdown("**Search City:**")
search_query = st.sidebar.text_input("Enter city name", key="city_search")

if search_query:
    cities = search_city(search_query)
    if cities:
        for idx, city in enumerate(cities[:3]):
            city_name = f"{city['name']}, {city['country']}"
            if st.sidebar.button(f"➕ {city_name}", key=f"search_{idx}"):
                if len(st.session_state['comparison_cities']) < 5:
                    city_data = {
                        'name': city_name,
                        'lat': city['latitude'],
                        'lon': city['longitude']
                    }
                    if city_data not in st.session_state['comparison_cities']:
                        st.session_state['comparison_cities'].append(city_data)
                        st.rerun()

# Display selected cities
st.sidebar.markdown("---")
st.sidebar.markdown("### 📍 Selected Cities")

if st.session_state['comparison_cities']:
    for idx, city in enumerate(st.session_state['comparison_cities']):
        col1, col2 = st.sidebar.columns([3, 1])
        with col1:
            st.text(city['name'])
        with col2:
            if st.button("❌", key=f"remove_{idx}"):
                st.session_state['comparison_cities'].pop(idx)
                st.rerun()
    
    if st.sidebar.button("🗑️ Clear All"):
        st.session_state['comparison_cities'] = []
        st.rerun()
else:
    st.sidebar.info("No cities selected. Add cities to compare.")

# Main content
if len(st.session_state['comparison_cities']) < 2:
    st.info("👈 Please add at least 2 cities from the sidebar to start comparing weather data.")
    st.stop()

# Fetch weather data for all cities
with st.spinner("Fetching weather data for all cities..."):
    weather_data = []
    forecast_data = []
    
    for city in st.session_state['comparison_cities']:
        # Current weather
        current = get_current_weather(city['lat'], city['lon'])
        if current:
            current['city'] = city['name']
            weather_data.append(current)
        
        # Forecast
        forecast = get_daily_forecast(city['lat'], city['lon'], days=7)
        if forecast is not None:
            forecast['city'] = city['name']
            forecast_data.append(forecast)

if weather_data:
    # Current Weather Comparison
    st.markdown("## 🌤️ Current Weather Comparison")
    
    # Create comparison table
    comparison_df = pd.DataFrame(weather_data)
    
    # Display as cards
    cols = st.columns(len(weather_data))
    
    for idx, (col, data) in enumerate(zip(cols, weather_data)):
        with col:
            emoji = get_weather_emoji(data.get('weather_code', 0))
            description = get_weather_description(data.get('weather_code', 0))
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.5rem; border-radius: 12px; color: white; text-align: center;">
                <h4 style="margin: 0;">{data['city']}</h4>
                <div style="font-size: 3rem; margin: 1rem 0;">{emoji}</div>
                <h2 style="margin: 0.5rem 0;">{data.get('temperature', 'N/A')}°C</h2>
                <p style="opacity: 0.9; margin: 0;">{description}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="background: #f7fafc; padding: 1rem; border-radius: 8px; margin-top: 1rem;">
                <p style="margin: 0.3rem 0;"><b>Feels Like:</b> {data.get('feels_like', 'N/A')}°C</p>
                <p style="margin: 0.3rem 0;"><b>Humidity:</b> {data.get('humidity', 'N/A')}%</p>
                <p style="margin: 0.3rem 0;"><b>Wind:</b> {data.get('wind_speed', 'N/A')} km/h</p>
                <p style="margin: 0.3rem 0;"><b>Pressure:</b> {data.get('pressure', 'N/A')} hPa</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Temperature Comparison Chart
    st.markdown("### 🌡️ Temperature Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Bar chart
        temp_chart = alt.Chart(comparison_df).mark_bar().encode(
            x=alt.X('city:N', title='City'),
            y=alt.Y('temperature:Q', title='Temperature (°C)'),
            color=alt.Color('temperature:Q', scale=alt.Scale(scheme='redyellowblue', reverse=True), legend=None),
            tooltip=['city', 'temperature', 'feels_like']
        ).properties(
            height=300,
            title='Current Temperature'
        )
        
        st.altair_chart(temp_chart, use_container_width=True)
    
    with col2:
        # Radar chart for multiple metrics
        fig = go.Figure()
        
        for data in weather_data:
            fig.add_trace(go.Scatterpolar(
                r=[
                    data.get('temperature', 0),
                    data.get('humidity', 0),
                    data.get('wind_speed', 0),
                    data.get('pressure', 1000) - 950,  # Normalize pressure
                    data.get('cloud_cover', 0)
                ],
                theta=['Temperature', 'Humidity', 'Wind Speed', 'Pressure', 'Cloud Cover'],
                fill='toself',
                name=data['city']
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            title='Weather Metrics Comparison',
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Comparison Table
    st.markdown("### 📋 Detailed Comparison Table")
    
    display_df = comparison_df.copy()
    display_df['City'] = display_df['city']
    display_df['Weather'] = display_df['weather_code'].apply(lambda x: f"{get_weather_emoji(x)} {get_weather_description(x)}")
    display_df['Temperature'] = display_df['temperature'].apply(lambda x: f"{x:.1f}°C")
    display_df['Feels Like'] = display_df['feels_like'].apply(lambda x: f"{x:.1f}°C")
    display_df['Humidity'] = display_df['humidity'].apply(lambda x: f"{x:.0f}%")
    display_df['Wind Speed'] = display_df['wind_speed'].apply(lambda x: f"{x:.1f} km/h")
    display_df['Pressure'] = display_df['pressure'].apply(lambda x: f"{x:.0f} hPa")
    display_df['Cloud Cover'] = display_df['cloud_cover'].apply(lambda x: f"{x:.0f}%")
    
    st.dataframe(
        display_df[['City', 'Weather', 'Temperature', 'Feels Like', 'Humidity', 'Wind Speed', 'Pressure', 'Cloud Cover']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")

# Forecast Comparison
if forecast_data:
    st.markdown("## 📅 7-Day Forecast Comparison")
    
    # Combine all forecast data
    all_forecasts = pd.concat(forecast_data, ignore_index=True)
    all_forecasts['date'] = pd.to_datetime(all_forecasts['time']).dt.strftime('%m/%d')
    
    # Temperature forecast comparison
    st.markdown("### 🌡️ Temperature Forecast Trends")
    
    # Create line chart for max temperatures
    temp_forecast_chart = alt.Chart(all_forecasts).mark_line(point=True).encode(
        x=alt.X('date:N', title='Date'),
        y=alt.Y('temperature_2m_max:Q', title='Max Temperature (°C)'),
        color=alt.Color('city:N', title='City'),
        tooltip=['city', 'date', 'temperature_2m_max', 'temperature_2m_min']
    ).properties(
        height=400
    ).interactive()
    
    st.altair_chart(temp_forecast_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Precipitation comparison
    st.markdown("### 💧 Precipitation Forecast Comparison")
    
    precip_chart = alt.Chart(all_forecasts).mark_bar().encode(
        x=alt.X('date:N', title='Date'),
        y=alt.Y('precipitation_sum:Q', title='Precipitation (mm)'),
        color=alt.Color('city:N', title='City'),
        xOffset='city:N',
        tooltip=['city', 'date', 'precipitation_sum', 'precipitation_probability_max']
    ).properties(
        height=400
    )
    
    st.altair_chart(precip_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Best/Worst Weather Ranking
    st.markdown("### 🏆 Weather Rankings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🌡️ Warmest Cities (Current)**")
        warmest = comparison_df.nlargest(len(comparison_df), 'temperature')[['city', 'temperature']]
        for idx, row in warmest.iterrows():
            st.markdown(f"{idx+1}. **{row['city']}** - {row['temperature']:.1f}°C")
    
    with col2:
        st.markdown("**❄️ Coolest Cities (Current)**")
        coolest = comparison_df.nsmallest(len(comparison_df), 'temperature')[['city', 'temperature']]
        for idx, row in coolest.iterrows():
            st.markdown(f"{idx+1}. **{row['city']}** - {row['temperature']:.1f}°C")
    
    st.markdown("---")
    
    # Export data
    csv = display_df[['City', 'Weather', 'Temperature', 'Feels Like', 'Humidity', 'Wind Speed', 'Pressure']].to_csv(index=False)
    st.download_button(
        label="📥 Download Comparison as CSV",
        data=csv,
        file_name="weather_comparison.csv",
        mime="text/csv"
    )

else:
    st.warning("Unable to fetch forecast data for comparison.")

# Quick navigation
st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌤️ Current Weather", use_container_width=True):
        st.switch_page("pages/02_🌤️_Current_Weather.py")

with col2:
    if st.button("📅 7-Day Forecast", use_container_width=True):
        st.switch_page("pages/03_📅_7-Day_Forecast.py")

with col3:
    if st.button("🗺️ Interactive Map", use_container_width=True):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
