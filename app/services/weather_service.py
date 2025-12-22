"""Weather service using Open-Meteo API (free, unlimited, no API key)."""
import requests
from datetime import datetime, timedelta


class WeatherService:
    """Service for fetching weather data from Open-Meteo API."""
    
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1"
    
    def get_current_weather(self, latitude, longitude):
        """
        Get current weather for given coordinates.
        
        Args:
            latitude (float): Latitude
            longitude (float): Longitude
            
        Returns:
            dict: Current weather data
        """
        url = f"{self.base_url}/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'current_weather': True,
            'timezone': 'Asia/Jakarta'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'current_weather' in data:
                current = data['current_weather']
                return {
                    'success': True,
                    'temperature': current.get('temperature'),
                    'windspeed': current.get('windspeed'),
                    'winddirection': current.get('winddirection'),
                    'weathercode': current.get('weathercode'),
                    'time': current.get('time')
                }
            return {'success': False, 'error': 'No current weather data'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_forecast(self, latitude, longitude, days=7):
        """
        Get weather forecast for given coordinates.
        
        Args:
            latitude (float): Latitude
            longitude (float): Longitude
            days (int): Number of days (max 16)
            
        Returns:
            dict: Forecast data
        """
        url = f"{self.base_url}/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,windspeed_10m_max',
            'forecast_days': min(days, 16),
            'timezone': 'Asia/Jakarta'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'daily' in data:
                daily = data['daily']
                forecast = []
                for i in range(len(daily['time'])):
                    forecast.append({
                        'date': daily['time'][i],
                        'temp_max': daily['temperature_2m_max'][i],
                        'temp_min': daily['temperature_2m_min'][i],
                        'precipitation': daily['precipitation_sum'][i],
                        'rain': daily['rain_sum'][i],
                        'windspeed': daily['windspeed_10m_max'][i]
                    })
                return {
                    'success': True,
                    'forecast': forecast
                }
            return {'success': False, 'error': 'No forecast data'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_soil_data(self, latitude, longitude):
        """
        Get soil temperature and moisture data.
        
        Args:
            latitude (float): Latitude
            longitude (float): Longitude
            
        Returns:
            dict: Soil data
        """
        url = f"{self.base_url}/forecast"
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'daily': 'soil_temperature_0cm,soil_moisture_0_to_1cm',
            'forecast_days': 1,
            'timezone': 'Asia/Jakarta'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if 'daily' in data:
                daily = data['daily']
                return {
                    'success': True,
                    'soil_temperature': daily['soil_temperature_0cm'][0] if daily['soil_temperature_0cm'] else None,
                    'soil_moisture': daily['soil_moisture_0_to_1cm'][0] if daily['soil_moisture_0_to_1cm'] else None
                }
            return {'success': False, 'error': 'No soil data'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_agricultural_recommendations(self, latitude, longitude):
        """
        Get agricultural recommendations based on weather.
        
        Args:
            latitude (float): Latitude
            longitude (float): Longitude
            
        Returns:
            dict: Recommendations
        """
        # Get current weather and forecast
        current = self.get_current_weather(latitude, longitude)
        forecast = self.get_forecast(latitude, longitude, days=3)
        soil = self.get_soil_data(latitude, longitude)
        
        recommendations = []
        
        if current.get('success'):
            temp = current.get('temperature', 0)
            wind = current.get('windspeed', 0)
            
            # Temperature recommendations
            if temp > 35:
                recommendations.append("⚠️ Suhu sangat tinggi. Pertimbangkan irigasi tambahan.")
            elif temp < 15:
                recommendations.append("❄️ Suhu rendah. Hindari penanaman tanaman sensitif dingin.")
            
            # Wind recommendations
            if wind > 20:
                recommendations.append("💨 Angin kencang. Tunda penyemprotan pestisida.")
            elif wind < 5:
                recommendations.append("✅ Angin tenang. Kondisi baik untuk penyemprotan.")
        
        if forecast.get('success'):
            forecast_data = forecast.get('forecast', [])
            if forecast_data:
                # Check for rain in next 24 hours
                rain_tomorrow = forecast_data[0].get('rain', 0) if len(forecast_data) > 0 else 0
                if rain_tomorrow > 5:
                    recommendations.append("🌧️ Hujan diprediksi besok. Tunda pemupukan dan penyemprotan.")
                elif rain_tomorrow == 0:
                    recommendations.append("☀️ Tidak ada hujan diprediksi. Waktu baik untuk aplikasi pupuk/pestisida.")
        
        if soil.get('success'):
            moisture = soil.get('soil_moisture', 0)
            if moisture and moisture < 20:
                recommendations.append("💧 Kelembaban tanah rendah. Pertimbangkan irigasi.")
            elif moisture and moisture > 80:
                recommendations.append("💦 Kelembaban tanah tinggi. Hindari irigasi berlebihan.")
        
        if not recommendations:
            recommendations.append("✅ Kondisi cuaca normal untuk aktivitas pertanian.")
        
        return {
            'success': True,
            'recommendations': recommendations,
            'current_weather': current,
            'forecast': forecast,
            'soil_data': soil
        }
