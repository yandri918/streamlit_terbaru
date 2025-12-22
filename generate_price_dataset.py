"""Generate 1-year realistic price dataset for Indonesian commodities."""
import csv
import random
from datetime import datetime, timedelta
import math

# Base prices (November 2025 reference)
COMMODITIES = {
    "cabai_merah_keriting": {"name": "Cabai Merah Keriting", "base": 45000, "volatility": 0.25, "seasonal": True},
    "cabai_rawit_merah": {"name": "Cabai Rawit Merah", "base": 65000, "volatility": 0.30, "seasonal": True},
    "bawang_merah": {"name": "Bawang Merah", "base": 30000, "volatility": 0.20, "seasonal": True},
    "bawang_putih": {"name": "Bawang Putih", "base": 42000, "volatility": 0.15, "seasonal": False},
    "tomat": {"name": "Tomat", "base": 12000, "volatility": 0.18, "seasonal": True},
    "kentang": {"name": "Kentang", "base": 18000, "volatility": 0.12, "seasonal": False},
    "wortel": {"name": "Wortel", "base": 14000, "volatility": 0.10, "seasonal": False},
    "kubis": {"name": "Kubis", "base": 8000, "volatility": 0.15, "seasonal": False},
    "beras_premium": {"name": "Beras Premium", "base": 16000, "volatility": 0.08, "seasonal": False},
    "beras_medium": {"name": "Beras Medium", "base": 14500, "volatility": 0.08, "seasonal": False},
    "gula_pasir": {"name": "Gula Pasir", "base": 18500, "volatility": 0.10, "seasonal": False},
    "minyak_goreng_kemasan": {"name": "Minyak Goreng Kemasan", "base": 21500, "volatility": 0.12, "seasonal": False},
    "telur_ayam": {"name": "Telur Ayam Ras", "base": 28000, "volatility": 0.15, "seasonal": False},
    "daging_ayam": {"name": "Daging Ayam Ras", "base": 39000, "volatility": 0.12, "seasonal": False},
    "daging_sapi": {"name": "Daging Sapi Murni", "base": 135000, "volatility": 0.10, "seasonal": False},
    "jagung_pipilan": {"name": "Jagung Pipilan", "base": 5500, "volatility": 0.15, "seasonal": True},
    "kedelai": {"name": "Kedelai Impor", "base": 10500, "volatility": 0.12, "seasonal": False},
}

def generate_seasonal_factor(day_of_year, is_seasonal):
    """Generate seasonal price factor (1.0 = normal, >1 = high season, <1 = low season)."""
    if not is_seasonal:
        return 1.0
    
    # Simulate seasonal pattern (sine wave with 365-day period)
    # Peak around day 180 (mid-year), low around day 0/365
    seasonal = 1.0 + 0.15 * math.sin(2 * math.pi * day_of_year / 365)
    return seasonal

def generate_price_history(commodity_id, commodity_data, start_date, days=365):
    """Generate realistic price history for a commodity."""
    prices = []
    base_price = commodity_data["base"]
    volatility = commodity_data["volatility"]
    is_seasonal = commodity_data["seasonal"]
    
    # Random walk with drift
    current_price = base_price
    
    for i in range(days):
        date = start_date + timedelta(days=i)
        day_of_year = date.timetuple().tm_yday
        
        # Seasonal factor
        seasonal_factor = generate_seasonal_factor(day_of_year, is_seasonal)
        
        # Random daily change (mean-reverting random walk)
        daily_change = random.gauss(0, volatility * 0.02)  # 2% daily std dev
        mean_reversion = (base_price - current_price) * 0.05  # Pull back to base
        
        current_price = current_price * (1 + daily_change) + mean_reversion
        
        # Apply seasonal factor
        final_price = int(current_price * seasonal_factor)
        
        prices.append({
            "date": date.strftime("%Y-%m-%d"),
            "commodity_id": commodity_id,
            "commodity_name": commodity_data["name"],
            "price": final_price,
            "day_of_year": day_of_year
        })
    
    return prices

# Generate dataset
print("Generating 1-year price dataset...")
start_date = datetime(2024, 11, 26)  # 1 year ago from now
all_data = []

for commodity_id, commodity_data in COMMODITIES.items():
    print(f"  Generating {commodity_data['name']}...")
    prices = generate_price_history(commodity_id, commodity_data, start_date)
    all_data.extend(prices)

# Save to CSV
output_file = "app/data/price_history_1year.csv"
print(f"\nSaving to {output_file}...")

with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['date', 'commodity_id', 'commodity_name', 'price', 'day_of_year']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(all_data)

print(f"✅ Dataset created: {len(all_data)} records")
print(f"   - Commodities: {len(COMMODITIES)}")
print(f"   - Days: 365")
print(f"   - Total records: {len(all_data)}")
