
import sys
import os
import pandas as pd
from datetime import datetime

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agrisensa_streamlit.services.bapanas_service import BapanasService
from agrisensa_streamlit.utils.bapanas_constants import PROVINCE_MAPPING

def simulate_page_run():
    print("="*50)
    print("🚀 SIMULASI LOGIC HALAMAN 6 (BAPANAS INTEGRATION)")
    print("="*50)
    
    service = BapanasService()
    
    # 1. Test National Data
    print("\n[1] Fetching NATIONAL Data...")
    df_nasional = service.get_latest_prices(province_id=0)
    if df_nasional is not None:
        print(f"✅ Success! Count: {len(df_nasional)} items")
        print(df_nasional.head(3).to_string())
    else:
        print("❌ Failed to fetch National data")
        
    # 2. Test Specific Province (Jawa Timur = 15)
    province_name = "Jawa Timur"
    province_id = PROVINCE_MAPPING[province_name]
    
    print(f"\n[2] Fetching {province_name} (ID: {province_id})...")
    df_jatim = service.get_latest_prices(province_id=province_id)
    
    if df_jatim is not None:
        print(f"✅ Success! Count: {len(df_jatim)} items")
        
        # Check specific commodity
        beras = df_jatim[df_jatim['commodity'].str.contains("Beras Medium", na=False)]
        if not beras.empty:
            print(f"   ℹ️ Harga Beras Medium di {province_name}: Rp {beras.iloc[0]['price']:,.0f}")
        
        cabe = df_jatim[df_jatim['commodity'].str.contains("Cabai Rawit", na=False)]
        if not cabe.empty:
            print(f"   ℹ️ Harga Cabai Rawit di {province_name}: Rp {cabe.iloc[0]['price']:,.0f}")
    else:
        print("❌ Failed to fetch Province data")

if __name__ == "__main__":
    simulate_page_run()
