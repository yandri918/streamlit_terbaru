
import requests
import pandas as pd
from datetime import datetime

class WeatherService:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        
    def get_weather_forecast(self, lat, lon):
        """
        Get weather data from Open-Meteo API
        Returns dictionary with current and daily forecast
        """
        try:
            params = {
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,relative_humidity_2m,rain,weather_code,wind_speed_10m",
                "hourly": "temperature_2m,rain,soil_temperature_0cm,soil_moisture_0_to_1cm",
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,rain_sum,precipitation_probability_max,et0_fao_evapotranspiration",
                "timezone": "auto"
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._process_weather_data(data)
            else:
                return None
                
        except Exception as e:
            print(f"Weather API Error: {e}")
            return None

    def _process_weather_data(self, raw_data):
        """Process API response into structured Insight object"""
        current = raw_data.get('current', {})
        daily = raw_data.get('daily', {})
        hourly = raw_data.get('hourly', {})
        
        # Calculate seasonal rain estimate (simple projection)
        daily_rains = daily.get('rain_sum', [0])
        avg_rain_week = sum(daily_rains[:7]) / 7 if daily_rains else 0
        seasonal_rain_est = avg_rain_week * 30 * 4  # Estimate for 4 months (Crop cycle)
        # Clamp to realistic tropical values
        seasonal_rain_est = max(500, min(seasonal_rain_est, 4000)) 
        
        # Determine Rain Risk
        max_rain_prob = max(daily.get('precipitation_probability_max', [0])[:3])
        rain_risk = "Tinggi" if max_rain_prob > 70 or current.get('rain', 0) > 0 else "Rendah"
        
        return {
            "current_temp": current.get('temperature_2m', 27.0),
            "current_rain": current.get('rain', 0.0),
            "current_humidity": current.get('relative_humidity_2m', 80),
            "wind_speed": current.get('wind_speed_10m', 0),
            "seasonal_rain_est": int(seasonal_rain_est),
            "rain_risk_3d": rain_risk,
            "soil_moisture": hourly.get('soil_moisture_0_to_1cm', [0.3])[0], # Approx current
            "raw_daily": daily
        }

    def get_planting_recommendation(self, weather_data):
        """Simple logic for planting suitability"""
        if not weather_data: return "Data tidak tersedia"
        
        risk = weather_data['rain_risk_3d']
        rain = weather_data['current_rain']
        
        if rain > 5:
            return "⛔ TUNDA TANAM: Hujan lebat saat ini."
        elif risk == "Tinggi":
            return "⚠️ WASPADA: Risiko hujan tinggi dalam 3 hari kedepan."
        else:
            return "✅ AMAN: Kondisi cuaca mendukung untuk aktivitas tanam."
    
    def get_7day_forecast(self, weather_data):
        """Extract and format 7-day forecast from daily data."""
        if not weather_data or 'raw_daily' not in weather_data:
            return []
        
        daily = weather_data['raw_daily']
        forecast = []
        
        for i in range(min(7, len(daily.get('time', [])))):
            forecast.append({
                'date': daily['time'][i],
                'temp_max': daily['temperature_2m_max'][i],
                'temp_min': daily['temperature_2m_min'][i],
                'rain_mm': daily['rain_sum'][i],
                'rain_prob': daily['precipitation_probability_max'][i],
                'weather_code': daily['weather_code'][i]
            })
        
        return forecast
    
    def get_agricultural_alerts(self, weather_data):
        """Generate smart alerts based on weather conditions."""
        alerts = []
        
        if not weather_data:
            return alerts
        
        # Current rain alert
        if weather_data['current_rain'] > 5:
            alerts.append({
                'type': 'warning',
                'icon': '🌧️',
                'title': 'Hujan Lebat Saat Ini',
                'message': f"Intensitas: {weather_data['current_rain']:.1f} mm/jam",
                'action': 'Tunda penyemprotan & pemupukan daun. Cek drainase.'
            })
        
        # High temperature alert
        if weather_data['current_temp'] > 33:
            alerts.append({
                'type': 'caution',
                'icon': '☀️',
                'title': 'Suhu Tinggi',
                'message': f"Suhu: {weather_data['current_temp']:.1f}°C",
                'action': 'Tingkatkan frekuensi irigasi. Pertimbangkan naungan.'
            })
        
        # High humidity (disease risk)
        if weather_data['current_humidity'] > 85:
            alerts.append({
                'type': 'info',
                'icon': '💧',
                'title': 'Kelembapan Tinggi',
                'message': f"Kelembapan: {weather_data['current_humidity']}%",
                'action': 'Risiko penyakit jamur meningkat. Siapkan fungisida preventif.'
            })
        
        # Wind speed alert
        if weather_data['wind_speed'] > 20:
            alerts.append({
                'type': 'warning',
                'icon': '💨',
                'title': 'Angin Kencang',
                'message': f"Kecepatan angin: {weather_data['wind_speed']:.1f} km/jam",
                'action': 'Periksa struktur greenhouse & ajir tanaman.'
            })
        
        return alerts
