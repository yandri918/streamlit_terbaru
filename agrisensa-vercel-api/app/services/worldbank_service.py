"""World Bank Food Price Service."""
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class WorldBankService:
    """Service for fetching food prices from World Bank RTFP API."""
    
    BASE_URL = "https://microdata.worldbank.org/index.php/api/tables/data/FCV/IDN_2021_RTFP_V02_M"
    
    # Mapping komoditas Indonesia ke World Bank product names
    COMMODITY_MAP = {
        "cabai_merah_keriting": "chili",
        "cabai_rawit_merah": "chili",
        "bawang_merah": "onions",
        "bawang_putih": "garlic",
        "tomat": "tomato",  # Might not be available
        "kentang": "potato",  # Might not be available
        "beras_premium": "rice",
        "beras_medium": "rice",
        "gula_pasir": "sugar",
        "minyak_goreng_kemasan": "oil",
        "minyak_goreng_curah": "oil",
        "telur_ayam": "eggs",
        "daging_ayam": "chicken meat",
        "daging_sapi": "beef"
    }
    
    @classmethod
    def fetch_latest_prices(cls, limit=1000):
        """Fetch latest food prices from World Bank API."""
        try:
            params = {
                'limit': limit,
                'format': 'json'
            }
            
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # DEBUG: Print structure
            print(f"\n[DEBUG] Response keys: {data.keys() if isinstance(data, dict) else 'Not a dict'}")
            if isinstance(data, dict) and 'data' in data:
                print(f"[DEBUG] Data length: {len(data['data'])}")
                if data['data']:
                    print(f"[DEBUG] First record keys: {data['data'][0].keys()}")
                    print(f"[DEBUG] First record sample: {data['data'][0]}")
            elif isinstance(data, list):
                print(f"[DEBUG] Response is a list with {len(data)} items")
                if data:
                    print(f"[DEBUG] First item: {data[0]}")
            
            logger.info(f"Fetched {len(data.get('data', []))} price records from World Bank")
            return data
            
        except Exception as e:
            logger.error(f"Error fetching World Bank data: {e}")
            print(f"[ERROR] {e}")
            return None
    
    @classmethod
    def get_price_for_commodity(cls, commodity_id):
        """Get current price for a specific commodity."""
        # Map to World Bank product name
        wb_product = cls.COMMODITY_MAP.get(commodity_id)
        if not wb_product:
            logger.warning(f"Commodity {commodity_id} not mapped to World Bank product")
            return None
        
        # Fetch data
        data = cls.fetch_latest_prices(limit=500)
        if not data or 'data' not in data:
            return None
        
        # Filter for the specific product and get recent prices
        prices = []
        for record in data['data']:
            product_name = record.get('product', '').lower()
            if wb_product.lower() in product_name:
                try:
                    price = float(record.get('price', 0))
                    market = record.get('market', 'Unknown Market')
                    date = record.get('date', '')
                    
                    if price > 0:
                        prices.append({
                            'price': price,
                            'market': market,
                            'date': date,
                            'product': record.get('product')
                        })
                except (ValueError, TypeError):
                    continue
        
        if not prices:
            logger.warning(f"No price data found for {wb_product}")
            return None
        
        # Sort by date (most recent first) and get average of recent prices
        prices.sort(key=lambda x: x['date'], reverse=True)
        recent_prices = prices[:10]  # Take 10 most recent
        
        avg_price = sum(p['price'] for p in recent_prices) / len(recent_prices)
        
        return {
            'average_price': int(avg_price),
            'sample_size': len(recent_prices),
            'latest_date': recent_prices[0]['date'] if recent_prices else None,
            'markets': list(set(p['market'] for p in recent_prices))
        }
    
    @classmethod
    def get_all_available_products(cls):
        """Get list of all available products in the dataset."""
        data = cls.fetch_latest_prices(limit=100)
        if not data or 'data' not in data:
            return []
        
        products = set()
        for record in data['data']:
            product = record.get('product', '')
            if product:
                products.add(product)
        
        return sorted(list(products))
