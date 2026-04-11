"""Price scraper for PIHPS (Bank Indonesia) data."""
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class PIHPSScraper:
    """Scraper for Bank Indonesia PIHPS price data."""
    
    BASE_URL = "https://www.bi.go.id"
    DATA_ENDPOINT = "/hargapangan/WebSite/Home/GetChartData"
    
    # Mapping of commodity names (Indonesian to internal keys)
    COMMODITY_MAP = {
        "Beras Premium": "beras_premium",
        "Beras Medium": "beras_medium",
        "Bawang Merah Ukuran Sedang": "bawang_merah",
        "Bawang Putih Ukuran Sedang": "bawang_putih",
        "Cabai Merah Keriting": "cabai_merah_keriting",
        "Cabai Merah Besar": "cabai_merah_besar",
        "Cabai Rawit Hijau": "cabai_rawit_hijau",
        "Cabai Rawit Merah": "cabai_rawit_merah",
        "Daging Ayam Ras Segar": "ayam_ras",
        "Daging Sapi Kualitas 1": "daging_sapi",
        "Telur Ayam Ras Segar": "telur_ayam",
        "Minyak Goreng Curah": "minyak_goreng",
        "Gula Pasir Lokal": "gula_pasir",
        "Jagung Pipilan Kering": "jagung_pipilan"
    }
    
    @classmethod
    def fetch_commodity_price(cls, commodity_name, max_retries=2):
        """
        Fetch current price for a specific commodity.
        
        Args:
            commodity_name: Indonesian name of commodity (e.g., "Bawang Merah Ukuran Sedang")
            max_retries: Number of retry attempts if request fails
            
        Returns:
            dict: {"name": str, "price": int, "unit": str, "date": str} or None
        """
        for attempt in range(max_retries):
            try:
                # Generate temp_id (seems to be timestamp-based)
                temp_id = str(int(datetime.now().timestamp() * 1000))
                
                params = {
                    "tempId": temp_id,
                    "comName": commodity_name,
                    "forInfo": "true"
                }
                
                response = requests.get(
                    f"{cls.BASE_URL}{cls.DATA_ENDPOINT}",
                    params=params,
                    timeout=3  # Reduced from 10 to 3 seconds
                )
                response.raise_for_status()
                
                data = response.json()
                
                # The API returns an array with price info
                if data and len(data) > 0:
                    latest = data[0]  # Most recent data point
                    return {
                        "name": commodity_name,
                        "price": int(float(latest.get("harga", 0))),
                        "unit": "kg",  # Most commodities are per kg
                        "date": latest.get("date", "")
                    }
                
                return None
                
            except Exception as e:
                if attempt == max_retries - 1:  # Last attempt
                    logger.error(f"Error fetching price for {commodity_name}: {e}")
                # Otherwise, retry silently
                continue
        
        return None
    
    @classmethod
    def fetch_ticker_prices(cls, commodities=None):
        """
        Fetch prices for multiple commodities for ticker display.
        
        Args:
            commodities: List of commodity names. If None, uses default set.
            
        Returns:
            list: [{"name": str, "price": int, "unit": str}, ...]
        """
        if commodities is None:
            # Default commodities for ticker - expanded list
            commodities = [
                "Beras Premium",
                "Beras Medium",
                "Bawang Merah Ukuran Sedang",
                "Bawang Putih Ukuran Sedang",
                "Cabai Merah Keriting",
                "Cabai Merah Besar",
                "Cabai Rawit Hijau",
                "Cabai Rawit Merah",
                "Daging Ayam Ras Segar",
                "Daging Sapi Kualitas 1",
                "Telur Ayam Ras Segar",
                "Minyak Goreng Curah",
                "Gula Pasir Lokal",
                "Jagung Pipilan Kering"
            ]
        
        # Use ThreadPoolExecutor for concurrent requests (faster)
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        ticker_data = []
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all fetch tasks
            future_to_commodity = {
                executor.submit(cls.fetch_commodity_price, commodity): commodity 
                for commodity in commodities
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_commodity):
                price_info = future.result()
                if price_info:
                    # Simplify name for ticker
                    simple_name = price_info["name"].replace(" Ukuran Sedang", "").replace(" Segar", "").replace(" Kering", "")
                    ticker_data.append({
                        "name": simple_name,
                        "price": price_info["price"],
                        "unit": price_info["unit"]
                    })
        
        return ticker_data
