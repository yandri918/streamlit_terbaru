"""
Weather API Integration using Open-Meteo
Free weather API with no API key required
"""
import requests
import pandas as pd
from datetime import datetime, timedelta

# Open-Meteo API endpoints
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
HISTORICAL_URL = "https://archive-api.open-meteo.com/v1/archive"

def search_city(city_name):
    """
    Search for city coordinates using geocoding API
    
    Args:
        city_name: Name of the city to search
    
    Returns:
        List of matching cities with coordinates
    """
    try:
        params = {
            "name": city_name,
            "count": 5,
            "language": "en",
            "format": "json"
        }
        
        response = requests.get(GEOCODING_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data:
            cities = []
            for result in data["results"]:
                cities.append({
                    "name": result.get("name", ""),
                    "country": result.get("country", ""),
                    "latitude": result.get("latitude"),
                    "longitude": result.get("longitude"),
                    "admin1": result.get("admin1", ""),  # State/Province
                    "population": result.get("population", 0)
                })
            return cities
        return []
    except Exception as e:
        print(f"Error searching city: {e}")
        return []

def get_current_weather(lat, lon):
    """
    Get current weather for a location
    
    Args:
        lat: Latitude
        lon: Longitude
    
    Returns:
        Dictionary with current weather data
    """
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "weather_code",
                "cloud_cover",
                "pressure_msl",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m"
            ],
            "daily": [
                "sunrise",
                "sunset",
                "sunshine_duration"
            ],
            "timezone": "auto",
            "forecast_days": 1
        }
        
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "current" in data:
            current = data["current"]
            daily = data.get("daily", {})
            
            # Get today's astronomical data
            sunrise = daily.get("sunrise", [None])[0] if daily else None
            sunset = daily.get("sunset", [None])[0] if daily else None
            sunshine_duration = daily.get("sunshine_duration", [0])[0] if daily else 0
            
            return {
                "temperature": current.get("temperature_2m"),
                "feels_like": current.get("apparent_temperature"),
                "humidity": current.get("relative_humidity_2m"),
                "precipitation": current.get("precipitation"),
                "weather_code": current.get("weather_code"),
                "cloud_cover": current.get("cloud_cover"),
                "pressure": current.get("pressure_msl"),
                "wind_speed": current.get("wind_speed_10m"),
                "wind_direction": current.get("wind_direction_10m"),
                "wind_gusts": current.get("wind_gusts_10m"),
                "time": current.get("time"),
                "timezone": data.get("timezone", "UTC"),
                "sunrise": sunrise,
                "sunset": sunset,
                "sunshine_duration": sunshine_duration
            }
        return None
    except Exception as e:
        print(f"Error fetching current weather: {e}")
        return None

def get_daily_forecast(lat, lon, days=7):
    """
    Get daily weather forecast
    
    Args:
        lat: Latitude
        lon: Longitude
        days: Number of days to forecast (1-16)
    
    Returns:
        DataFrame with daily forecast
    """
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "wind_direction_10m_dominant",
                "sunrise",
                "sunset",
                "uv_index_max"
            ],
            "timezone": "auto",
            "forecast_days": days
        }
        
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "daily" in data:
            df = pd.DataFrame(data["daily"])
            df['time'] = pd.to_datetime(df['time'])
            return df
        return None
    except Exception as e:
        print(f"Error fetching daily forecast: {e}")
        return None

def get_hourly_forecast(lat, lon, hours=48):
    """
    Get hourly weather forecast
    
    Args:
        lat: Latitude
        lon: Longitude
        hours: Number of hours to forecast (max 384)
    
    Returns:
        DataFrame with hourly forecast
    """
    try:
        # Calculate forecast days needed
        forecast_days = min(16, (hours // 24) + 1)
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation_probability",
                "precipitation",
                "weather_code",
                "cloud_cover",
                "visibility",
                "wind_speed_10m",
                "wind_direction_10m",
                "wind_gusts_10m"
            ],
            "timezone": "auto",
            "forecast_days": forecast_days
        }
        
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "hourly" in data:
            df = pd.DataFrame(data["hourly"])
            df['time'] = pd.to_datetime(df['time'])
            # Limit to requested hours
            df = df.head(hours)
            return df
        return None
    except Exception as e:
        print(f"Error fetching hourly forecast: {e}")
        return None

def get_historical_weather(lat, lon, start_date, end_date):
    """
    Get historical weather data
    
    Args:
        lat: Latitude
        lon: Longitude
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        DataFrame with historical weather data
    """
    try:
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": [
                "weather_code",
                "temperature_2m_max",
                "temperature_2m_min",
                "temperature_2m_mean",
                "apparent_temperature_max",
                "apparent_temperature_min",
                "precipitation_sum",
                "wind_speed_10m_max",
                "wind_gusts_10m_max",
                "uv_index_max",
                "uv_index_clear_sky_max"
            ],
            "timezone": "auto"
        }
        
        response = requests.get(HISTORICAL_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if "daily" in data:
            df = pd.DataFrame(data["daily"])
            df['time'] = pd.to_datetime(df['time'])
            return df
        return None
    except Exception as e:
        print(f"Error fetching historical weather: {e}")
        return None

# Weather code descriptions
WEATHER_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow fall",
    73: "Moderate snow fall",
    75: "Heavy snow fall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
}

def get_weather_description(code):
    """Get weather description from code"""
    return WEATHER_CODES.get(code, "Unknown")

def get_weather_emoji(code):
    """Get weather emoji from code"""
    if code == 0:
        return "☀️"
    elif code in [1, 2]:
        return "⛅"
    elif code == 3:
        return "☁️"
    elif code in [45, 48]:
        return "🌫️"
    elif code in [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82]:
        return "🌧️"
    elif code in [71, 73, 75, 77, 85, 86]:
        return "❄️"
    elif code in [95, 96, 99]:
        return "⛈️"
    return "🌤️"
