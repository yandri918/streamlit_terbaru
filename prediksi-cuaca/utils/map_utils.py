"""
Folium map utilities for weather visualization
"""
import folium
from folium import plugins
import streamlit as st

# Popular Indonesian cities
POPULAR_CITIES = [
    {"name": "Jakarta", "lat": -6.2088, "lon": 106.8456},
    {"name": "Surabaya", "lat": -7.2575, "lon": 112.7521},
    {"name": "Bandung", "lat": -6.9175, "lon": 107.6191},
    {"name": "Medan", "lat": 3.5952, "lon": 98.6722},
    {"name": "Semarang", "lat": -6.9667, "lon": 110.4167},
    {"name": "Makassar", "lat": -5.1477, "lon": 119.4327},
    {"name": "Palembang", "lat": -2.9761, "lon": 104.7754},
    {"name": "Denpasar", "lat": -8.6705, "lon": 115.2126},
    {"name": "Yogyakarta", "lat": -7.7956, "lon": 110.3695},
    {"name": "Malang", "lat": -7.9666, "lon": 112.6326}
]

def create_base_map(center=None, zoom=5):
    """
    Create base Folium map
    
    Args:
        center: [lat, lon] for map center, defaults to Indonesia
        zoom: Initial zoom level
    
    Returns:
        Folium map object
    """
    if center is None:
        center = [-2.5, 118.0]  # Center of Indonesia
    
    # Create map
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add layer control
    folium.TileLayer('CartoDB positron', name='Light Map').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Dark Map').add_to(m)
    
    # Plugins removed to avoid serialization errors in deployment
    # plugins.Fullscreen(
    #     position='topright',
    #     title='Full Screen',
    #     title_cancel='Exit Full Screen',
    #     force_separate_button=True
    # ).add_to(m)
    
    # Add locate control
    # plugins.LocateControl(auto_start=False).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    return m

def add_weather_marker(map_obj, lat, lon, weather_data=None, popup_text=None):
    """
    Add weather marker to map
    
    Args:
        map_obj: Folium map object
        lat: Latitude
        lon: Longitude
        weather_data: Dictionary with weather information
        popup_text: Custom popup text
    
    Returns:
        Updated map object
    """
    if popup_text is None and weather_data:
        # Create popup from weather data
        from utils.weather_api import get_weather_emoji, get_weather_description
        
        emoji = get_weather_emoji(weather_data.get('weather_code', 0))
        description = get_weather_description(weather_data.get('weather_code', 0))
        temp = weather_data.get('temperature', 'N/A')
        
        popup_text = f"""
        <div style="font-family: Arial; min-width: 200px;">
            <h4 style="margin: 0; color: #2c3e50;">{emoji} Weather</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>Condition:</b> {description}</p>
            <p style="margin: 5px 0;"><b>Temperature:</b> {temp}°C</p>
            <p style="margin: 5px 0;"><b>Humidity:</b> {weather_data.get('humidity', 'N/A')}%</p>
            <p style="margin: 5px 0;"><b>Wind:</b> {weather_data.get('wind_speed', 'N/A')} km/h</p>
        </div>
        """
    elif popup_text is None:
        popup_text = f"<b>Location:</b><br>Lat: {lat:.4f}<br>Lon: {lon:.4f}"
    
    # Add marker
    folium.Marker(
        location=[lat, lon],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color='red', icon='cloud', prefix='fa')
    ).add_to(map_obj)
    
    return map_obj

def add_popular_cities(map_obj, show_markers=True):
    """
    Add popular cities to map
    
    Args:
        map_obj: Folium map object
        show_markers: Whether to show city markers
    
    Returns:
        Updated map object
    """
    if show_markers:
        for city in POPULAR_CITIES:
            folium.CircleMarker(
                location=[city['lat'], city['lon']],
                radius=5,
                popup=f"<b>{city['name']}</b>",
                color='blue',
                fill=True,
                fillColor='lightblue',
                fillOpacity=0.6
            ).add_to(map_obj)
    
    return map_obj

def create_weather_heatmap(map_obj, locations_data):
    """
    Create temperature heatmap overlay
    
    Args:
        map_obj: Folium map object
        locations_data: List of [lat, lon, temperature] values
    
    Returns:
        Updated map object
    """
    if locations_data and len(locations_data) > 0:
        plugins.HeatMap(
            locations_data,
            name='Temperature Heatmap',
            min_opacity=0.3,
            max_zoom=13,
            radius=25,
            blur=15,
            gradient={
                0.0: 'blue',
                0.5: 'lime',
                1.0: 'red'
            }
        ).add_to(map_obj)
    
    return map_obj

def add_click_handler(map_obj):
    """
    Add click handler to map (for Streamlit integration)
    Note: Actual click handling is done via streamlit-folium
    
    Args:
        map_obj: Folium map object
    
    Returns:
        Updated map object
    """
    # Click functionality is handled by streamlit-folium
    # This function is placeholder for future enhancements
    return map_obj
