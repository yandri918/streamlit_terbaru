# -*- coding: utf-8 -*-
"""
Weather Service for Fertilizer Calculator
Provides simulated weather data and fertilization timing recommendations
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

def get_simulated_weather(location: str = "Indonesia") -> Dict:
    """
    Generate simulated current weather data
    
    Args:
        location: Location name (for display only in demo mode)
    
    Returns:
        Dictionary with current weather conditions
    """
    # Simulate tropical climate (Indonesia)
    current_temp = random.randint(24, 33)  # Celsius
    humidity = random.randint(65, 95)  # Percentage
    rainfall_today = random.choice([0, 0, 0, 2, 5, 10, 15, 25])  # mm
    wind_speed = random.randint(5, 20)  # km/h
    
    # Weather condition based on rainfall
    if rainfall_today == 0:
        condition = "Cerah"
        icon = "☀️"
    elif rainfall_today < 10:
        condition = "Berawan"
        icon = "⛅"
    else:
        condition = "Hujan"
        icon = "🌧️"
    
    return {
        "location": location,
        "temperature": current_temp,
        "humidity": humidity,
        "rainfall": rainfall_today,
        "wind_speed": wind_speed,
        "condition": condition,
        "icon": icon,
        "timestamp": datetime.now()
    }


def get_7day_forecast(location: str = "Indonesia") -> List[Dict]:
    """
    Generate simulated 7-day weather forecast
    
    Args:
        location: Location name
    
    Returns:
        List of daily forecast dictionaries
    """
    forecast = []
    today = datetime.now()
    
    for i in range(7):
        date = today + timedelta(days=i)
        
        # Simulate weather patterns
        temp_min = random.randint(22, 26)
        temp_max = random.randint(28, 34)
        
        # Rainfall probability (higher in certain days)
        if i in [2, 5]:  # Simulate rainy days
            rainfall = random.randint(15, 50)
            rain_prob = random.randint(70, 95)
        elif i in [1, 4]:
            rainfall = random.randint(5, 15)
            rain_prob = random.randint(40, 60)
        else:
            rainfall = random.randint(0, 5)
            rain_prob = random.randint(10, 30)
        
        # Condition
        if rainfall > 20:
            condition = "Hujan Lebat"
            icon = "🌧️"
        elif rainfall > 5:
            condition = "Hujan Ringan"
            icon = "🌦️"
        elif rain_prob > 50:
            condition = "Berawan"
            icon = "⛅"
        else:
            condition = "Cerah"
            icon = "☀️"
        
        forecast.append({
            "date": date,
            "day_name": date.strftime("%A"),
            "temp_min": temp_min,
            "temp_max": temp_max,
            "rainfall": rainfall,
            "rain_probability": rain_prob,
            "condition": condition,
            "icon": icon
        })
    
    return forecast


def check_fertilization_timing(weather_data: Dict, forecast: List[Dict]) -> Tuple[bool, str, List[str]]:
    """
    Analyze weather conditions and provide fertilization timing recommendations
    
    Args:
        weather_data: Current weather dictionary
        forecast: 7-day forecast list
    
    Returns:
        Tuple of (is_safe, recommendation, reasons)
    """
    reasons = []
    is_safe = True
    
    # Check current conditions
    if weather_data['rainfall'] > 10:
        is_safe = False
        reasons.append("❌ Hujan saat ini terlalu deras (>10mm)")
    
    if weather_data['temperature'] > 32:
        reasons.append("⚠️ Suhu sangat tinggi (>32°C) - hindari aplikasi siang hari")
    
    # Check next 3 days forecast
    heavy_rain_coming = False
    for day in forecast[:3]:
        if day['rainfall'] > 20:
            heavy_rain_coming = True
            is_safe = False
            reasons.append(f"❌ Hujan lebat diprediksi pada {day['day_name']} ({day['rainfall']}mm)")
    
    # Check for good windows
    good_days = []
    for i, day in enumerate(forecast[:7]):
        if day['rainfall'] < 5 and day['rain_probability'] < 40:
            good_days.append(day['day_name'])
    
    if good_days:
        reasons.append(f"✅ Hari baik untuk pemupukan: {', '.join(good_days[:3])}")
    
    # Generate recommendation
    if is_safe and not heavy_rain_coming:
        if weather_data['rainfall'] == 0:
            recommendation = "🟢 SANGAT BAIK - Kondisi ideal untuk pemupukan"
        else:
            recommendation = "🟡 BAIK - Bisa dilakukan dengan hati-hati"
    else:
        recommendation = "🔴 TUNDA - Tunggu kondisi lebih baik"
    
    return is_safe, recommendation, reasons


def get_method_specific_recommendations(weather_data: Dict, forecast: List[Dict]) -> Dict[str, Dict]:
    """
    Get weather-based recommendations for each fertilization method
    
    Args:
        weather_data: Current weather
        forecast: 7-day forecast
    
    Returns:
        Dictionary with recommendations per method
    """
    recommendations = {}
    
    # Tugal (Solid application)
    tugal_safe = weather_data['rainfall'] < 15
    tugal_rec = {
        "safe": tugal_safe,
        "recommendation": "✅ Aman" if tugal_safe else "⚠️ Tunda",
        "notes": [
            "Aplikasi padat relatif aman dalam hujan ringan",
            "Hindari jika tanah terlalu basah (genangan)",
            "Terbaik saat tanah lembab tapi tidak becek"
        ]
    }
    
    # Kocor (Liquid drench)
    kocor_safe = weather_data['rainfall'] < 10 and forecast[0]['rainfall'] < 10
    kocor_rec = {
        "safe": kocor_safe,
        "recommendation": "✅ Aman" if kocor_safe else "❌ Tunda",
        "notes": [
            "Hindari saat hujan - larutan akan tercuci",
            "Terbaik saat tanah lembab (pagi/sore)",
            "Tunggu 24 jam setelah hujan lebat"
        ]
    }
    
    # Semprot (Foliar spray)
    semprot_safe = (weather_data['rainfall'] == 0 and 
                    weather_data['wind_speed'] < 15 and
                    forecast[0]['rain_probability'] < 30)
    semprot_rec = {
        "safe": semprot_safe,
        "recommendation": "✅ Aman" if semprot_safe else "❌ Tunda",
        "notes": [
            "HARUS cerah - tidak boleh ada hujan",
            "Angin <15 km/jam untuk aplikasi merata",
            "Semprot pagi (06:00-09:00) atau sore (16:00-18:00)",
            "Tunggu minimal 4 jam sebelum hujan"
        ]
    }
    
    # Organik
    organik_safe = True  # Organic is generally safe anytime
    organik_rec = {
        "safe": organik_safe,
        "recommendation": "✅ Aman",
        "notes": [
            "Pupuk organik bisa diaplikasikan kapan saja",
            "Lebih baik saat awal musim hujan",
            "Hujan membantu dekomposisi pupuk organik"
        ]
    }
    
    recommendations["Tugal"] = tugal_rec
    recommendations["Kocor"] = kocor_rec
    recommendations["Semprot"] = semprot_rec
    recommendations["Organik"] = organik_rec
    
    return recommendations


def get_seasonal_tips(month: int) -> List[str]:
    """
    Get seasonal fertilization tips based on month
    
    Args:
        month: Month number (1-12)
    
    Returns:
        List of seasonal tips
    """
    # Indonesia has 2 seasons: Dry (Apr-Sep) and Wet (Oct-Mar)
    if month in [4, 5, 6, 7, 8, 9]:
        # Dry season
        return [
            "🌞 Musim Kemarau - Perhatikan ketersediaan air",
            "💧 Aplikasi kocor lebih efektif (tanah kering)",
            "⏰ Pemupukan pagi/sore untuk menghindari penguapan",
            "🌱 Pertimbangkan mulsa untuk retensi kelembaban"
        ]
    else:
        # Wet season
        return [
            "🌧️ Musim Hujan - Hati-hati pencucian nutrisi",
            "🔸 Tugal lebih aman dari kocor/semprot",
            "📅 Pilih jeda hujan untuk aplikasi",
            "🌿 Waktu ideal untuk pupuk organik"
        ]
