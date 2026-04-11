"""
Interactive Weather Map
Click anywhere on the map to get weather information
"""
import streamlit as st
import sys
import os
from streamlit_folium import st_folium

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.map_utils import create_base_map, add_weather_marker, add_popular_cities, POPULAR_CITIES
from utils.weather_api import get_current_weather, search_city, get_weather_emoji, get_weather_description

# Page configuration
st.set_page_config(
    page_title="Interactive Weather Map",
    page_icon="🗺️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .location-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin: 1rem 0;
    }
    
    .weather-display {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🗺️ Interactive Weather Map")
st.markdown("**Click anywhere on the map to get instant weather information**")

st.markdown("---")

# Sidebar - Location Search
st.sidebar.markdown("### 🔍 Search Location")

search_query = st.sidebar.text_input("Enter city name", placeholder="e.g., Jakarta, London, Tokyo")

if search_query:
    with st.sidebar:
        with st.spinner(f"Searching for {search_query}..."):
            cities = search_city(search_query)
            
            if cities:
                st.success(f"Found {len(cities)} result(s)")
                
                for idx, city in enumerate(cities):
                    city_name = f"{city['name']}, {city.get('admin1', '')}, {city['country']}"
                    if st.button(f"📍 {city_name}", key=f"city_{idx}"):
                        st.session_state['selected_lat'] = city['latitude']
                        st.session_state['selected_lon'] = city['longitude']
                        st.session_state['selected_location'] = city_name
                        st.rerun()
            else:
                st.warning("No cities found. Try a different search term.")

# Sidebar - Popular Cities
st.sidebar.markdown("---")
st.sidebar.markdown("### 🌆 Popular Cities")

for city in POPULAR_CITIES[:5]:  # Show top 5
    if st.sidebar.button(f"📍 {city['name']}", key=f"popular_{city['name']}"):
        st.session_state['selected_lat'] = city['lat']
        st.session_state['selected_lon'] = city['lon']
        st.session_state['selected_location'] = city['name']
        st.rerun()

# Initialize session state
if 'selected_lat' not in st.session_state:
    st.session_state['selected_lat'] = -6.2088  # Jakarta default
    st.session_state['selected_lon'] = 106.8456
    st.session_state['selected_location'] = "Jakarta"

# Create map
st.markdown("### 🗺️ Click on the map to select a location")

# Determine map center
center = [st.session_state['selected_lat'], st.session_state['selected_lon']]

# Create base map
m = create_base_map(center=center, zoom=10)

# Add popular cities markers
m = add_popular_cities(m, show_markers=True)

# Get current weather for selected location
current_weather = get_current_weather(
    st.session_state['selected_lat'],
    st.session_state['selected_lon']
)

# Add marker for selected location
if current_weather:
    m = add_weather_marker(
        m,
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        current_weather
    )

# Display map
map_data = st_folium(
    m,
    width=None,
    height=500,
    returned_objects=["last_clicked"]
)

# Handle map clicks
if map_data and map_data.get("last_clicked"):
    clicked_lat = map_data["last_clicked"]["lat"]
    clicked_lon = map_data["last_clicked"]["lng"]
    
    # Update session state
    if (clicked_lat != st.session_state['selected_lat'] or 
        clicked_lon != st.session_state['selected_lon']):
        st.session_state['selected_lat'] = clicked_lat
        st.session_state['selected_lon'] = clicked_lon
        st.session_state['selected_location'] = f"Lat: {clicked_lat:.4f}, Lon: {clicked_lon:.4f}"
        st.rerun()

st.markdown("---")

# Display current location info
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown(f"""
    <div class="location-card">
        <h3>📍 Selected Location</h3>
        <p style="font-size: 1.1rem; margin: 0.5rem 0;">
            <b>{st.session_state['selected_location']}</b>
        </p>
        <p style="font-size: 0.9rem; opacity: 0.9; margin: 0;">
            Lat: {st.session_state['selected_lat']:.4f}<br>
            Lon: {st.session_state['selected_lon']:.4f}
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if current_weather:
        emoji = get_weather_emoji(current_weather.get('weather_code', 0))
        description = get_weather_description(current_weather.get('weather_code', 0))
        
        st.markdown(f"""
        <div class="weather-display">
            <h3>{emoji} Current Weather</h3>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-top: 1rem;">
                <div>
                    <p style="margin: 0.5rem 0;"><b>Condition:</b> {description}</p>
                    <p style="margin: 0.5rem 0;"><b>Temperature:</b> {current_weather.get('temperature', 'N/A')}°C</p>
                    <p style="margin: 0.5rem 0;"><b>Feels Like:</b> {current_weather.get('feels_like', 'N/A')}°C</p>
                </div>
                <div>
                    <p style="margin: 0.5rem 0;"><b>Humidity:</b> {current_weather.get('humidity', 'N/A')}%</p>
                    <p style="margin: 0.5rem 0;"><b>Wind Speed:</b> {current_weather.get('wind_speed', 'N/A')} km/h</p>
                    <p style="margin: 0.5rem 0;"><b>Pressure:</b> {current_weather.get('pressure', 'N/A')} hPa</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Unable to fetch weather data for this location")

st.markdown("---")

# Quick actions
st.markdown("### 🎯 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🌤️ View Detailed Weather", use_container_width=True):
        st.switch_page("pages/02_🌤️_Current_Weather.py")

with col2:
    if st.button("📅 View 7-Day Forecast", use_container_width=True):
        st.switch_page("pages/03_📅_7-Day_Forecast.py")

with col3:
    if st.button("⏰ View Hourly Forecast", use_container_width=True):
        st.switch_page("pages/04_⏰_Hourly_Forecast.py")

# Instructions
st.markdown("---")
st.markdown("""
### 💡 How to Use

1. **Click anywhere** on the map to select a location
2. **Search** for a city using the search bar in the sidebar
3. **Quick select** from popular Indonesian cities
4. View **current weather** for the selected location
5. Navigate to other pages for **detailed forecasts**

**Tip:** Blue markers show popular cities. Click them for quick selection!
""")
