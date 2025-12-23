
import requests
import pandas as pd
from datetime import datetime, timedelta
import sys
import os

# Robust import strategy for Streamlit + Script usage
try:
    from agrisensa_streamlit.utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING
except ImportError:
    try:
        # Try relative import (if run as package)
        from ..utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING
    except ImportError:
        # Final fallback: add parent dir to path (if run as script)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if parent_dir not in sys.path:
            sys.path.insert(0, parent_dir)
        from utils.bapanas_constants import API_CONFIG, COMMODITY_MAPPING

class BapanasService:
    def __init__(self):
        self.base_url = API_CONFIG["BASE_URL"]
        self.headers = API_CONFIG["HEADERS"]
    
    def get_latest_prices(self, province_id=None, city_id=None):
        """
        Fetch latest prices from Bapanas API
        """
        endpoint = f"{self.base_url}/harga-pangan-informasi"
        
        params = {
            "level_harga_id": 1  # 1 for consumer/retail prices
        }
        
        if province_id and str(province_id) != "0":
            params["province_id"] = province_id
        
        if city_id:
            params["city_id"] = city_id
            
        try:
            response = requests.get(
                endpoint, 
                headers=self.headers, 
                params=params, 
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("status") == "success":
                    return self._parse_price_response(result.get("data", []))
                else:
                    return None
            else:
                return None
                
        except Exception as e:
            print(f"Connection Error: {e}")
            return None
    
    def _parse_price_response(self, data_list):
        """
        Parse success response from API
        Returns DataFrame with standard columns
        """
        if not data_list:
            return None
            
        parsed_data = []
        today_date = datetime.now()
        yesterday_date = today_date - timedelta(days=1)
        
        for item in data_list:
            try:
                # Add Today's Price
                parsed_data.append({
                    'commodity': item.get('name'),
                    'price': float(item.get('today', 0)),
                    'date': today_date,
                    'unit': item.get('satuan', 'Rp/kg')
                })
                
                # Add Yesterday's Price (for trend)
                if item.get('yesterday'):
                    parse_yesterday = item.get('yesterday_date')
                    date_obj = yesterday_date
                    
                    if parse_yesterday:
                        try:
                            date_obj = datetime.strptime(parse_yesterday, '%d-%m-%Y')
                        except:
                            pass
                            
                    parsed_data.append({
                        'commodity': item.get('name'),
                        'price': float(item.get('yesterday', 0)),
                        'date': date_obj,
                        'unit': item.get('satuan', 'Rp/kg')
                    })
            except:
                continue
                
        return pd.DataFrame(parsed_data)

    def get_commodity_list(self):
        return list(COMMODITY_MAPPING.keys())

    def get_price_map_data(self, commodity_id=2, level_id=3):
        """
        Fetch spatial price data from harga-peta-provinsi endpoint.
        Uses 'rata_rata_geometrik' as the price value.
        """
        endpoint = f"{self.base_url}/harga-peta-provinsi"
        
        # Date: Today
        today_str = datetime.now().strftime("%d/%m/%Y")
        period = f"{today_str} - {today_str}"
        
        params = {
            "level_harga_id": level_id,
            "komoditas_id": commodity_id,
            "period_date": period,
            "multi_status_map[0]": "",
            "multi_province_id[0]": ""
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=15)
            if response.status_code == 200:
                result = response.json()
                if "data" in result:
                    return self._parse_map_response(result['data'])
            return None
        except Exception as e:
            print(f"Map API Error: {e}")
            return None

    def _parse_map_response(self, data_list):
        """
        Parse map data into DataFrame with Lat/Lon and Price
        """
        parsed_data = []
        for item in data_list:
            try:
                # Parse LatLong "lat,lon"
                ll = item.get('latlong', '').split(',')
                if len(ll) != 2: continue
                
                lat = float(ll[0])
                lon = float(ll[1])
                
                # Parse Price (rata_rata_geometrik or average)
                # 'rata_rata_geometrik' seems to be the numeric value from debug
                price = item.get('rata_rata_geometrik', 0)
                
                # Ensure price is valid number
                try:
                    price = float(price)
                except:
                    price = 0
                
                if price > 0:
                    parsed_data.append({
                        'province': item.get('province_name'),
                        'lat': lat,
                        'lon': lon,
                        'price': price,
                        'level': item.get('level_harga', '?'),
                        'status': item.get('status_map', 'Normal')
                    })
            except:
                continue
                
        return pd.DataFrame(parsed_data)
