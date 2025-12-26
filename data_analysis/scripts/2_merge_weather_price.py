"""
AgriSensa - Weather & Price Data Merger
========================================
Script untuk menggabungkan data curah hujan (BMKG) dengan harga komoditi (BAPANAS)

Author: Yandri
Date: 2024-12-26
"""

import pandas as pd
import os
from datetime import datetime


def load_weather_data(filepath):
    """
    Load weather data from BMKG CSV
    
    Expected columns:
    - Tahun (Year)
    - Bulan (Month) 
    - Curah_Hujan_mm (Rainfall in mm)
    - Hari_Hujan (Rainy days)
    - Suhu_Rata_C (Average temperature)
    - Kelembaban_Persen (Humidity %)
    """
    print(f"\n📂 Loading weather data from: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        print("\n⚠️ Please download data from BMKG first:")
        print("   1. Visit: https://dataonline.bmkg.go.id/home")
        print("   2. Download curah hujan bulanan 2022-2024")
        print("   3. Save to: data/raw/curah_hujan_2022_2024.csv")
        return None
    
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Loaded {len(df)} weather records")
        print(f"📅 Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"❌ Error loading weather data: {e}")
        return None


def load_price_data(filepath):
    """Load price data from BAPANAS"""
    print(f"\n📂 Loading price data from: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"❌ File not found: {filepath}")
        print("\n⚠️ Please run script 1 first:")
        print("   python 1_fetch_bapanas_historical.py")
        return None
    
    try:
        df = pd.read_csv(filepath)
        
        # Convert date column if exists
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['year'] = df['date'].dt.year
            df['month'] = df['date'].dt.month
        
        print(f"✅ Loaded {len(df)} price records")
        print(f"📅 Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"❌ Error loading price data: {e}")
        return None


def merge_data(df_weather, df_price):
    """
    Merge weather and price data on year-month
    """
    print("\n🔗 Merging weather and price data...")
    
    # Ensure both have year and month columns
    if 'year' not in df_weather.columns or 'month' not in df_weather.columns:
        print("❌ Weather data must have 'year' and 'month' columns")
        return None
    
    if 'year' not in df_price.columns or 'month' not in df_price.columns:
        print("❌ Price data must have 'year' and 'month' columns")
        return None
    
    # Merge on year-month
    df_merged = pd.merge(
        df_price,
        df_weather,
        on=['year', 'month'],
        how='left'
    )
    
    print(f"✅ Merged dataset: {len(df_merged)} records")
    print(f"📊 Columns: {list(df_merged.columns)}")
    
    return df_merged


def add_seasonal_features(df):
    """
    Add seasonal features based on domain knowledge
    """
    print("\n🌦️ Adding seasonal features...")
    
    # Season classification
    def get_season(month):
        if month in [6, 7, 8]:
            return 'Kemarau'
        elif month in [11, 12, 1, 2, 3]:
            return 'Hujan'
        elif month in [9, 10]:
            return 'Transisi_Hujan'
        else:  # 4, 5
            return 'Transisi_Kemarau'
    
    df['season'] = df['month'].apply(get_season)
    
    # Nataru flag (December-January)
    df['is_nataru'] = df['month'].isin([12, 1]).astype(int)
    
    # Pest risk indicators (based on user's insight)
    def get_pest_risk(month):
        if month in [6, 7, 8]:  # Kemarau
            return 'High_Thrips_Kutu'
        elif month in [11, 12, 1, 2, 3]:  # Hujan
            return 'High_Jamur_Patek'
        elif month in [9, 10]:  # Transisi
            return 'Double_Trouble'
        else:
            return 'Medium'
    
    df['pest_risk_type'] = df['month'].apply(get_pest_risk)
    
    # Month name (Indonesian)
    month_names = {
        1: 'Januari', 2: 'Februari', 3: 'Maret', 4: 'April',
        5: 'Mei', 6: 'Juni', 7: 'Juli', 8: 'Agustus',
        9: 'September', 10: 'Oktober', 11: 'November', 12: 'Desember'
    }
    df['month_name'] = df['month'].map(month_names)
    
    print("✅ Added features: season, is_nataru, pest_risk_type, month_name")
    
    return df


def create_pivot_tables(df, output_dir):
    """Create useful pivot tables for analysis"""
    print("\n📊 Creating pivot tables...")
    
    # Average price by month and commodity
    pivot_price = df.pivot_table(
        values='price',
        index='month_name',
        columns='commodity',
        aggfunc='mean'
    )
    
    filepath = os.path.join(output_dir, 'pivot_price_by_month.csv')
    pivot_price.to_csv(filepath)
    print(f"💾 Saved: {filepath}")
    
    # Average price by season
    pivot_season = df.pivot_table(
        values='price',
        index='season',
        columns='commodity',
        aggfunc='mean'
    )
    
    filepath = os.path.join(output_dir, 'pivot_price_by_season.csv')
    pivot_season.to_csv(filepath)
    print(f"💾 Saved: {filepath}")
    
    return pivot_price, pivot_season


def main():
    """Main execution"""
    print("=" * 60)
    print("🔗 AgriSensa - Weather & Price Data Merger")
    print("=" * 60)
    
    # Paths
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    weather_file = os.path.join(base_dir, 'data', 'raw', 'curah_hujan_2022_2024.csv')
    price_file = os.path.join(base_dir, 'data', 'raw', 'harga_bapanas_raw', 'bapanas_historical_2022_2024_MOCK.csv')
    output_dir = os.path.join(base_dir, 'data', 'processed')
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Load data
    df_weather = load_weather_data(weather_file)
    df_price = load_price_data(price_file)
    
    if df_weather is None:
        print("\n⚠️ Weather data not found. Creating sample weather data...")
        # Create sample weather data
        df_weather = create_sample_weather_data()
        # Save sample
        sample_path = os.path.join(base_dir, 'data', 'raw', 'curah_hujan_2022_2024_SAMPLE.csv')
        df_weather.to_csv(sample_path, index=False)
        print(f"💾 Saved sample weather data to: {sample_path}")
        print("📝 You can replace this with real BMKG data later")
    
    if df_price is None:
        print("\n❌ Price data not found. Please run script 1 first.")
        return
    
    # Merge data
    df_merged = merge_data(df_weather, df_price)
    
    if df_merged is None:
        return
    
    # Add seasonal features
    df_merged = add_seasonal_features(df_merged)
    
    # Save merged dataset
    output_file = os.path.join(output_dir, 'dataset_training.csv')
    df_merged.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n💾 Saved merged dataset to: {output_file}")
    
    # Create pivot tables
    create_pivot_tables(df_merged, output_dir)
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 DATASET SUMMARY")
    print("=" * 60)
    print(f"Total Records: {len(df_merged)}")
    print(f"Date Range: {df_merged['year'].min()}-{df_merged['year'].max()}")
    print(f"Commodities: {df_merged['commodity'].nunique()}")
    print(f"Seasons: {df_merged['season'].unique()}")
    
    print("\n✅ DATA MERGE COMPLETE!")
    print("\n📝 Next Step:")
    print("   python 3_exploratory_analysis.py")


def create_sample_weather_data():
    """Create sample weather data for demonstration"""
    import random
    
    data = []
    for year in [2022, 2023, 2024]:
        for month in range(1, 13):
            # Seasonal rainfall pattern
            if month in [11, 12, 1, 2, 3]:  # Hujan
                rainfall = random.randint(200, 400)
                rainy_days = random.randint(15, 25)
                humidity = random.randint(75, 90)
                temp = random.randint(24, 28)
            elif month in [6, 7, 8]:  # Kemarau
                rainfall = random.randint(20, 80)
                rainy_days = random.randint(2, 8)
                humidity = random.randint(50, 70)
                temp = random.randint(28, 33)
            else:  # Transisi
                rainfall = random.randint(100, 200)
                rainy_days = random.randint(8, 15)
                humidity = random.randint(65, 80)
                temp = random.randint(26, 30)
            
            data.append({
                'year': year,
                'month': month,
                'curah_hujan_mm': rainfall,
                'hari_hujan': rainy_days,
                'suhu_rata_c': temp,
                'kelembaban_persen': humidity
            })
    
    return pd.DataFrame(data)


if __name__ == "__main__":
    main()
