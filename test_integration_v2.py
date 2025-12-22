
import sys
import os
import pandas as pd

# Add path to access services
sys.path.append(os.path.join(os.getcwd(), 'agrisensa_streamlit'))

from services.bapanas_service import BapanasService
from services.weather_service import WeatherService
from utils.bapanas_constants import PROVINCE_MAPPING

def simulate_harvest_planner_integration():
    print("🚀 SIMULATION: Integrated Harvest Planner Logic (v3.3 with Mapping)")
    print("================================================================")
    
    # 1. Init Services
    bapanas = BapanasService()
    weather = WeatherService()
    
    # 2. Simulate User Inputs
    # Testing MAPPING logic: "Padi (Inpari 32)" -> should map to "Beras Premium" or "GKG"
    selected_crop_input = "Padi (Inpari 32)"
    mapped_bapanas_name = "Beras Premium" # As defined in CROP_TO_BAPANAS_MAP in the page logic
    
    province_name = "Jawa Timur"
    province_id = PROVINCE_MAPPING[province_name]
    lat, lon = -7.25, 112.75 
    
    print(f"\n📍 Scenario:")
    print(f"   Crop Input: {selected_crop_input}")
    print(f"   Expected Map: {mapped_bapanas_name}")
    print(f"   Province: {province_name} (ID: {province_id})")
    print(f"   Location: {lat}, {lon}")
    
    # 3. Fetch Price (Bapanas)
    print("\n[1] Fetching Real-time Price (Bapanas)...")
    price_df = bapanas.get_latest_prices(province_id=province_id)
    
    market_price = 0
    
    if price_df is not None:
        # Simulate the logic in Modul 16: Check Map FIRST
        match = price_df[price_df['commodity'].str.contains(mapped_bapanas_name, case=False, na=False)]
        
        if not match.empty:
            market_price = match.iloc[0]['price']
            commodity_found = match.iloc[0]['commodity']
            print(f"   ✅ Price Found for '{commodity_found}': Rp {market_price:,} /kg")
        else:
            print(f"   ⚠️ Price not found for '{mapped_bapanas_name}'.")
    else:
        print("   ❌ Failed to fetch price.")
        
    # 4. Fetch Weather (Open-Meteo)
    print("\n[2] Fetching Real-time Weather (Open-Meteo)...")
    w_insight = weather.get_weather_forecast(lat, lon)
    
    rain_risk = "Unknown"
    
    if w_insight:
        temp = w_insight['current_temp']
        rain_est = w_insight['seasonal_rain_est']
        rain_risk = w_insight['rain_risk_3d']
        print(f"   ✅ Weather Data Parsed:")
        print(f"      - Temp: {temp}°C")
        print(f"      - Est Seasonal Rain: {rain_est} mm")
        print(f"      - Rain Risk (3 Days): {rain_risk}")
    else:
        print("   ❌ Failed to fetch weather.")

    # 5. Generate Strategic Insight (The Logic Fusion)
    print("\n[3] Generating Strategic Insight...")
    
    # Simulate Trend Logic (since API v2 static snapshot for now)
    simulated_trends = ["Naik 📈", "Stabil ➖", "Turun 📉"]
    
    for trend_sim in simulated_trends:
        print(f"\n   --- Scenario: Price Trend {trend_sim} + Rain Risk {rain_risk} ---")
        
        advice = "Netral"
        if "Naik" in trend_sim and rain_risk == "Rendah":
            advice = "🚀 PELUANG EMAS (Golden Opportunity)"
        elif "Naik" in trend_sim and rain_risk == "Tinggi":
            advice = "⚠️ HIGH RISK HIGH REWARD"
        elif "Turun" in trend_sim and rain_risk == "Tinggi":
            advice = "⛔ SITUASI TIDAK MENGUNTUNGKAN"
        elif "Turun" in trend_sim and rain_risk == "Rendah":
             advice = "🛡️ STRATEGI DEFENSIF"
             
        print(f"   💡 AI Advice: {advice}")

if __name__ == "__main__":
    simulate_harvest_planner_integration()
