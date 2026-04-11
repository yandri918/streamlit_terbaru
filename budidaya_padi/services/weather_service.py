"""
Weather Monitoring Service
Fetches weather data from Open-Meteo API
"""

import requests
import pandas as pd
from datetime import datetime
import streamlit as st

class WeatherService:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_forecast(self, lat, lon):
        """
        Get 7-day forecast for agriculture
        Params:
            latitude, longitude
        Returns:
            Dictionary with current and daily forecast data
        """
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": ["temperature_2m", "relative_humidity_2m", "is_day", "rain", "wind_speed_10m"],
                "hourly": ["temperature_2m", "relative_humidity_2m", "rain", "wind_speed_10m", "soil_temperature_0cm"],
                "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "rain_sum", "wind_speed_10m_max", "et0_fao_evapotranspiration"],
                "timezone": "auto"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._process_data(data)
            else:
                return None
                
        except Exception as e:
            st.error(f"Error fetching weather: {e}")
            return None

    def _process_data(self, data):
        """Process raw API response into usable structure"""
        
        # Current Conditions
        current = data.get("current", {})
        
        # Daily Forecast
        daily = data.get("daily", {})
        df_daily = pd.DataFrame({
            "date": pd.to_datetime(daily.get("time", [])),
            "temp_max": daily.get("temperature_2m_max", []),
            "temp_min": daily.get("temperature_2m_min", []),
            "rain_sum": daily.get("rain_sum", []),
            "wind_max": daily.get("wind_speed_10m_max", []),
            "et0": daily.get("et0_fao_evapotranspiration", []),
            "code": daily.get("weather_code", [])
        })
        
        # Hourly Forecast (Next 24h)
        hourly = data.get("hourly", {})
        df_hourly = pd.DataFrame({
            "time": pd.to_datetime(hourly.get("time", [])),
            "temp": hourly.get("temperature_2m", []),
            "rain": hourly.get("rain", []),
            "wind": hourly.get("wind_speed_10m", [])
        }).iloc[:24] # Taking only next 24 hours
        
        return {
            "current": {
                "temp": current.get("temperature_2m"),
                "humidity": current.get("relative_humidity_2m"),
                "rain": current.get("rain"), # mm (preceding hour)
                "wind": current.get("wind_speed_10m"),
                "is_day": current.get("is_day")
            },
            "daily": df_daily,
            "hourly": df_hourly,
            "units": data.get("current_units", {})
        }
    
    def get_agronomy_recommendation(self, current_data):
        """Generate recommendation based on current weather"""
        recs = []
        alerts = []
        
        wind = current_data["wind"]
        rain = current_data["rain"]
        temp = current_data["temp"]
        hum = current_data["humidity"]
        
        # Spraying Logic
        if wind > 15:
            alerts.append(f"⚠️ Angin kencang ({wind} km/h). TUNDA penyemprotan!")
        elif rain > 0.5:
            alerts.append("⚠️ Sedang hujan. JANGAN menyemprot pestisida kontak.")
        elif temp > 32:
            recs.append("🌡️ Suhu panas. Hindari menyemprot siang hari (penguapan tinggi & stomata menutup).")
        else:
            recs.append("✅ Kondisi AMAN untuk penyemprotan.")
            
        # Disease Logic
        if hum > 85 and temp < 28:
            alerts.append("🍄 Kelembaban tinggi + Suhu sejuk = Waspada Jamur (Blas/Busuk Pelepah).")
            
        return recs, alerts
