"""
AgriSensa - BMKG Excel Files Merger
====================================
Script untuk menggabungkan multiple file Excel BMKG menjadi 1 CSV

Author: Yandri
Date: 2024-12-26
"""

import pandas as pd
import glob
import os
from datetime import datetime


def merge_bmkg_excel_files(input_folder, output_file):
    """
    Merge multiple BMKG Excel files into one CSV
    
    Args:
        input_folder (str): Folder containing BMKG Excel files
        output_file (str): Output CSV file path
    """
    print("=" * 60)
    print("🔗 AgriSensa - BMKG Files Merger")
    print("=" * 60)
    
    # Create input folder if not exists
    os.makedirs(input_folder, exist_ok=True)
    
    # Find all Excel files
    excel_files = glob.glob(os.path.join(input_folder, "*.xlsx"))
    excel_files += glob.glob(os.path.join(input_folder, "*.xls"))
    
    if not excel_files:
        print(f"\n❌ No Excel files found in: {input_folder}")
        print("\n📝 Instructions:")
        print("1. Download data from: https://dataonline.bmkg.go.id")
        print("2. Save Excel files to:", input_folder)
        print("3. Run this script again")
        return None
    
    print(f"\n📂 Found {len(excel_files)} Excel files")
    
    # List to store all dataframes
    all_data = []
    errors = []
    
    for file in excel_files:
        filename = os.path.basename(file)
        print(f"\n📄 Processing: {filename}")
        
        try:
            # Read Excel file
            df = pd.read_excel(file)
            
            # Show columns for first file
            if len(all_data) == 0:
                print(f"   Columns: {list(df.columns)}")
            
            # Append to list
            all_data.append(df)
            print(f"   ✅ Loaded {len(df)} rows")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            errors.append((filename, str(e)))
    
    if not all_data:
        print("\n❌ No data could be loaded!")
        return None
    
    # Merge all dataframes
    print(f"\n🔗 Merging {len(all_data)} files...")
    merged_df = pd.concat(all_data, ignore_index=True)
    print(f"✅ Total rows: {len(merged_df)}")
    
    # Detect and rename columns
    print("\n🔧 Detecting column names...")
    
    # Common BMKG column names (case-insensitive)
    column_mapping = {}
    
    for col in merged_df.columns:
        col_lower = col.lower().strip()
        
        # Date column
        if any(x in col_lower for x in ['tanggal', 'date', 'tgl']):
            column_mapping[col] = 'date'
        
        # Rainfall (RR = Rain Rate)
        elif col_lower in ['rr', 'curah hujan', 'rainfall', 'ch']:
            column_mapping[col] = 'curah_hujan_mm'
        
        # Temperature average
        elif any(x in col_lower for x in ['tavg', 't avg', 'suhu rata', 'temp avg']):
            column_mapping[col] = 'suhu_rata_c'
        
        # Humidity
        elif any(x in col_lower for x in ['rh_avg', 'rh avg', 'kelembaban', 'humidity']):
            column_mapping[col] = 'kelembaban_persen'
        
        # Rainy days
        elif any(x in col_lower for x in ['hari hujan', 'rainy days', 'hh']):
            column_mapping[col] = 'hari_hujan'
    
    print(f"   Detected mappings: {column_mapping}")
    
    # Rename columns
    merged_df = merged_df.rename(columns=column_mapping)
    
    # Ensure we have date column
    if 'date' not in merged_df.columns:
        print("\n⚠️ Warning: 'date' column not found!")
        print("   Available columns:", list(merged_df.columns))
        print("   Please rename manually or update column_mapping in script")
        
        # Try to find date column manually
        date_col = None
        for col in merged_df.columns:
            if 'tanggal' in col.lower() or 'date' in col.lower():
                date_col = col
                break
        
        if date_col:
            merged_df = merged_df.rename(columns={date_col: 'date'})
            print(f"   Auto-renamed '{date_col}' to 'date'")
    
    # Convert date to datetime
    if 'date' in merged_df.columns:
        print("\n📅 Converting dates...")
        merged_df['date'] = pd.to_datetime(merged_df['date'], errors='coerce')
        
        # Remove rows with invalid dates
        invalid_dates = merged_df['date'].isna().sum()
        if invalid_dates > 0:
            print(f"   ⚠️ Removing {invalid_dates} rows with invalid dates")
            merged_df = merged_df.dropna(subset=['date'])
        
        # Extract year and month
        merged_df['year'] = merged_df['date'].dt.year
        merged_df['month'] = merged_df['date'].dt.month
        
        # Sort by date
        merged_df = merged_df.sort_values('date')
        
        print(f"   ✅ Date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
    
    # Save to CSV
    print(f"\n💾 Saving to: {output_file}")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    merged_df.to_csv(output_file, index=False, encoding='utf-8-sig')
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ MERGE COMPLETE!")
    print("=" * 60)
    print(f"Total Records: {len(merged_df)}")
    print(f"Columns: {list(merged_df.columns)}")
    
    if 'date' in merged_df.columns:
        print(f"Date Range: {merged_df['date'].min().date()} to {merged_df['date'].max().date()}")
    
    if errors:
        print(f"\n⚠️ Errors encountered: {len(errors)}")
        for filename, error in errors:
            print(f"   - {filename}: {error}")
    
    print(f"\n📁 Output file: {output_file}")
    print("\n📝 Next Step:")
    print("   python data_analysis/scripts/2_merge_weather_price.py")
    
    return merged_df


def main():
    """Main execution"""
    # Paths
    base_dir = os.path.join(os.path.dirname(__file__), '..')
    input_folder = os.path.join(base_dir, 'data', 'raw', 'bmkg_downloads')
    output_file = os.path.join(base_dir, 'data', 'raw', 'curah_hujan_2022_2024.csv')
    
    # Run merger
    merge_bmkg_excel_files(input_folder, output_file)


if __name__ == "__main__":
    main()
