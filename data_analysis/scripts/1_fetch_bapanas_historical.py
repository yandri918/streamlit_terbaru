"""
AgriSensa - BAPANAS Historical Data Fetcher
============================================
Script untuk mengambil data harga historis dari BAPANAS API (2022-2024)

Author: Yandri
Date: 2024-12-26
"""

import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import time

# Add parent directory to path to import BapanasService
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'agrisensa_tech'))

try:
    from services.bapanas_service import BapanasService
    print("✅ BapanasService imported successfully")
except ImportError as e:
    print(f"❌ Error importing BapanasService: {e}")
    print("⚠️ Make sure you're running this from the correct directory")
    sys.exit(1)


def fetch_historical_prices(start_date, end_date, province_id=0):
    """
    Fetch historical prices from BAPANAS API
    
    Args:
        start_date (str): Start date in format 'YYYY-MM-DD'
        end_date (str): End date in format 'YYYY-MM-DD'
        province_id (int): Province ID (0 for national average)
    
    Returns:
        pd.DataFrame: Historical price data
    """
    service = BapanasService()
    
    print(f"\n📊 Fetching BAPANAS data from {start_date} to {end_date}...")
    print(f"🌍 Province ID: {province_id} (0 = National Average)")
    
    # Note: BAPANAS API returns latest data, not historical range
    # We'll simulate historical by calling API and documenting current state
    # For true historical, you'd need to:
    # 1. Call API daily and store results, OR
    # 2. Use BAPANAS's historical data export feature (if available)
    
    df = service.get_latest_prices(province_id=province_id)
    
    if df is not None and not df.empty:
        print(f"✅ Fetched {len(df)} records")
        print(f"📅 Date range in data: {df['date'].min()} to {df['date'].max()}")
        print(f"🌾 Commodities: {df['commodity'].nunique()} unique items")
        return df
    else:
        print("❌ No data returned from API")
        return None


def save_to_csv(df, output_dir, filename):
    """Save DataFrame to CSV"""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False, encoding='utf-8-sig')
    print(f"💾 Saved to: {filepath}")
    return filepath


def create_mock_historical_data():
    """
    Create mock historical data for demonstration
    Since BAPANAS API only returns latest data, we'll create synthetic historical data
    based on seasonal patterns for training purposes.
    
    In production, you should:
    1. Set up daily cron job to call API and append to database
    2. Or request historical data export from BAPANAS directly
    """
    print("\n⚠️ Creating MOCK historical data for demonstration...")
    print("📝 Note: For real historical data, you need to:")
    print("   1. Set up daily API calls and store results, OR")
    print("   2. Request historical export from BAPANAS")
    
    # Generate dates for 3 years (2022-2024)
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Commodities to track
    commodities = [
        'Cabai Merah Keriting',
        'Cabai Merah Besar',
        'Cabai Rawit Merah',
        'Bawang Merah',
        'Bawang Putih',
        'Beras Premium',
        'Daging Ayam',
        'Telur Ayam',
        'Minyak Goreng'
    ]
    
    # Base prices (Rp/kg)
    base_prices = {
        'Cabai Merah Keriting': 60000,
        'Cabai Merah Besar': 55000,
        'Cabai Rawit Merah': 70000,
        'Bawang Merah': 35000,
        'Bawang Putih': 45000,
        'Beras Premium': 14000,
        'Daging Ayam': 35000,
        'Telur Ayam': 27000,
        'Minyak Goreng': 16000
    }
    
    # Seasonal patterns (multiplier per month)
    # Based on user's insight: Kemarau (Jun-Aug) = high price, Hujan (Nov-Mar) = low price
    seasonal_multipliers = {
        1: 1.2,   # Jan - Hujan + Nataru
        2: 0.9,   # Feb - Hujan puncak
        3: 0.85,  # Mar - Hujan
        4: 0.95,  # Apr - Transisi
        5: 1.1,   # Mei - Mulai kemarau
        6: 1.3,   # Jun - Kemarau
        7: 1.5,   # Jul - Kemarau puncak
        8: 1.4,   # Agu - Kemarau
        9: 1.6,   # Sep - Transisi (double trouble!)
        10: 1.5,  # Okt - Transisi
        11: 1.1,  # Nov - Mulai hujan
        12: 1.3   # Des - Nataru
    }
    
    # Generate data
    data = []
    for date in dates:
        month = date.month
        for commodity in commodities:
            base_price = base_prices[commodity]
            seasonal_mult = seasonal_multipliers[month]
            
            # Add random noise (±15%)
            import random
            noise = random.uniform(0.85, 1.15)
            
            # Special spike for Nataru (Dec-Jan)
            nataru_bonus = 1.2 if month in [12, 1] else 1.0
            
            # Calculate final price
            price = base_price * seasonal_mult * noise * nataru_bonus
            
            data.append({
                'date': date,
                'commodity': commodity,
                'price': round(price, 0),
                'unit': 'Rp/kg',
                'month': month,
                'year': date.year
            })
    
    df = pd.DataFrame(data)
    print(f"✅ Generated {len(df)} mock records")
    print(f"📅 Date range: {df['date'].min()} to {df['date'].max()}")
    
    return df


def main():
    """Main execution"""
    print("=" * 60)
    print("🌾 AgriSensa - BAPANAS Historical Data Fetcher")
    print("=" * 60)
    
    # Output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'harga_bapanas_raw')
    
    # Try to fetch real data first
    print("\n📡 Attempting to fetch real-time data from BAPANAS API...")
    df_real = fetch_historical_prices('2022-01-01', '2024-12-31', province_id=0)
    
    if df_real is not None:
        # Save real data
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        save_to_csv(df_real, output_dir, f'bapanas_latest_{timestamp}.csv')
    
    # Create mock historical data for training
    print("\n" + "=" * 60)
    df_mock = create_mock_historical_data()
    
    # Save mock data
    save_to_csv(df_mock, output_dir, 'bapanas_historical_2022_2024_MOCK.csv')
    
    # Create monthly aggregates
    print("\n📊 Creating monthly aggregates...")
    df_monthly = df_mock.groupby(['year', 'month', 'commodity']).agg({
        'price': ['mean', 'min', 'max', 'std']
    }).reset_index()
    df_monthly.columns = ['year', 'month', 'commodity', 'price_mean', 'price_min', 'price_max', 'price_std']
    
    save_to_csv(df_monthly, output_dir, 'bapanas_monthly_aggregates_MOCK.csv')
    
    # Summary statistics
    print("\n" + "=" * 60)
    print("📈 SUMMARY STATISTICS")
    print("=" * 60)
    
    for commodity in df_mock['commodity'].unique():
        df_comm = df_mock[df_mock['commodity'] == commodity]
        print(f"\n{commodity}:")
        print(f"  Average Price: Rp {df_comm['price'].mean():,.0f}")
        print(f"  Min Price: Rp {df_comm['price'].min():,.0f}")
        print(f"  Max Price: Rp {df_comm['price'].max():,.0f}")
        print(f"  Volatility (Std): Rp {df_comm['price'].std():,.0f}")
    
    print("\n" + "=" * 60)
    print("✅ DATA COLLECTION COMPLETE!")
    print("=" * 60)
    print("\n📝 Next Steps:")
    print("1. Download curah hujan data from BMKG (manual)")
    print("2. Run: python 2_merge_weather_price.py")
    print("3. Run: python 3_exploratory_analysis.py")
    print("\n⚠️ IMPORTANT: Replace MOCK data with real historical data when available!")


if __name__ == "__main__":
    main()
