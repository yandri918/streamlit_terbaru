# -*- coding: utf-8 -*-
"""
Map Service for Fertilizer Calculator
Provides interactive Folium maps for farm location selection
"""

import folium
from folium import plugins
from typing import Tuple, Optional
import streamlit as st
from streamlit_folium import st_folium

# Default locations (Indonesia agricultural regions)
DEFAULT_LOCATIONS = {
    "Jakarta": (-6.2088, 106.8456),
    "Surabaya": (-7.2575, 112.7521),
    "Medan": (3.5952, 98.6722),
    "Bandung": (-6.9175, 107.6191),
    "Makassar": (-5.1477, 119.4327),
    "Palembang": (-2.9761, 104.7754),
    "Pekanbaru": (0.5071, 101.4478),
    "Banjarmasin": (-3.3194, 114.5906),
    "Pontianak": (-0.0263, 109.3425),
    "Manado": (1.4748, 124.8421)
}

def create_location_picker_map(
    center_lat: float = -2.5,
    center_lon: float = 118.0,
    zoom: int = 5
) -> folium.Map:
    """
    Create an interactive map for selecting farm location
    
    Args:
        center_lat: Center latitude (default: Indonesia center)
        center_lon: Center longitude (default: Indonesia center)
        zoom: Initial zoom level
    
    Returns:
        Folium map object
    """
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    
    # Add alternative tile layers
    folium.TileLayer('Stamen Terrain', name='Terrain').add_to(m)
    folium.TileLayer('Stamen Toner', name='Toner').add_to(m)
    folium.TileLayer('CartoDB positron', name='Light').add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add click marker
    m.add_child(folium.LatLngPopup())
    
    # Add fullscreen button
    plugins.Fullscreen().add_to(m)
    
    # Add measure control
    plugins.MeasureControl(position='topleft').add_to(m)
    
    return m


def create_farm_map_with_weather(
    latitude: float,
    longitude: float,
    farm_name: str = "Lokasi Kebun",
    weather_data: Optional[dict] = None,
    zoom: int = 13
) -> folium.Map:
    """
    Create a detailed farm map with weather information
    
    Args:
        latitude: Farm latitude
        longitude: Farm longitude
        farm_name: Name of the farm
        weather_data: Weather data dictionary
        zoom: Zoom level
    
    Returns:
        Folium map object
    """
    # Create base map
    m = folium.Map(
        location=[latitude, longitude],
        zoom_start=zoom,
        tiles='OpenStreetMap'
    )
    
    # Add satellite layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Create popup content
    if weather_data:
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 0; color: #2E7D32;">{farm_name}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>📍 Koordinat:</b><br>
            Lat: {latitude:.4f}<br>
            Lon: {longitude:.4f}</p>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>🌡️ Cuaca:</b><br>
            {weather_data.get('icon', '☀️')} {weather_data.get('condition', 'N/A')}<br>
            Suhu: {weather_data.get('temperature', 'N/A')}°C<br>
            Hujan: {weather_data.get('rainfall', 0)} mm<br>
            Angin: {weather_data.get('wind_speed', 'N/A')} km/h</p>
        </div>
        """
    else:
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 0; color: #2E7D32;">{farm_name}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>📍 Koordinat:</b><br>
            Lat: {latitude:.4f}<br>
            Lon: {longitude:.4f}</p>
        </div>
        """
    
    # Add farm marker
    folium.Marker(
        location=[latitude, longitude],
        popup=folium.Popup(popup_html, max_width=250),
        tooltip=farm_name,
        icon=folium.Icon(color='green', icon='leaf', prefix='fa')
    ).add_to(m)
    
    # Add circle to show approximate farm area
    folium.Circle(
        location=[latitude, longitude],
        radius=500,  # 500 meters
        color='green',
        fill=True,
        fillColor='green',
        fillOpacity=0.1,
        popup='Area Estimasi Kebun'
    ).add_to(m)
    
    # Add layer control
    folium.LayerControl().add_to(m)
    
    # Add fullscreen
    plugins.Fullscreen().add_to(m)
    
    return m


def add_weather_markers(
    map_obj: folium.Map,
    locations: list,
    weather_data_list: list
) -> folium.Map:
    """
    Add weather markers to existing map
    
    Args:
        map_obj: Folium map object
        locations: List of (lat, lon, name) tuples
        weather_data_list: List of weather data dictionaries
    
    Returns:
        Updated Folium map object
    """
    for (lat, lon, name), weather in zip(locations, weather_data_list):
        # Create weather icon based on condition
        icon_color = 'blue'
        if weather.get('rainfall', 0) > 10:
            icon_color = 'red'
        elif weather.get('rainfall', 0) > 5:
            icon_color = 'orange'
        
        popup_html = f"""
        <div style="font-family: Arial;">
            <h5>{name}</h5>
            <p>{weather.get('icon', '☀️')} {weather.get('condition', 'N/A')}<br>
            🌡️ {weather.get('temperature', 'N/A')}°C<br>
            💧 {weather.get('rainfall', 0)} mm</p>
        </div>
        """
        
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"{name}: {weather.get('condition', 'N/A')}",
            icon=folium.Icon(color=icon_color, icon='cloud')
        ).add_to(map_obj)
    
    return map_obj


def get_location_from_name(location_name: str) -> Optional[Tuple[float, float]]:
    """
    Get coordinates from predefined location name
    
    Args:
        location_name: Name of the location
    
    Returns:
        Tuple of (latitude, longitude) or None
    """
    return DEFAULT_LOCATIONS.get(location_name)


def render_interactive_map(
    map_obj: folium.Map,
    height: int = 500,
    width: Optional[int] = None
) -> dict:
    """
    Render Folium map in Streamlit with interaction
    
    Args:
        map_obj: Folium map object
        height: Map height in pixels
        width: Map width in pixels (None for full width)
    
    Returns:
        Dictionary with map interaction data
    """
    return st_folium(
        map_obj,
        height=height,
        width=width,
        returned_objects=["last_clicked"]
    )
