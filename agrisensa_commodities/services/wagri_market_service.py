"""
WAGRI Market Intelligence Service
Integrates with WAGRI API for Japan wholesale market data
Focus on Indonesian export commodities

Based on: https://api.wagri2.net/MaffOpenData/market/FreshWholesaleMarketSurveyByNational
Author: AgriSensa Team
Date: 2025-12-30
"""

import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
import os
from pathlib import Path


class WagriMarketService:
    """
    Service for fetching and analyzing Japan wholesale market data from WAGRI API.
    """
    
    BASE_URL = "https://api.wagri2.net/MaffOpenData/market/FreshWholesaleMarketSurveyByNational/Get"
    
    # Cache directory
    CACHE_DIR = Path(__file__).parent.parent / "data" / "wagri_cache"
    
    # Exchange rate (JPY to IDR) - can be updated
    EXCHANGE_RATE_JPY_TO_IDR = 105.0
    
    def __init__(self):
        """Initialize service and ensure cache directory exists."""
        self.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        self._ensure_cache_files()
    
    def _ensure_cache_files(self):
        """Create cache files if they don't exist."""
        latest_cache = self.CACHE_DIR / "prices_latest.json"
        if not latest_cache.exists():
            latest_cache.write_text(json.dumps({}))
        
        history_dir = self.CACHE_DIR / "prices_history"
        history_dir.mkdir(exist_ok=True)
    
    @staticmethod
    def fetch_commodity_data(market_survey_id: str) -> Optional[Dict]:
        """
        Fetch commodity data from WAGRI API by MarketSurveyId.
        
        Args:
            market_survey_id: Unique ID for market survey entry
        
        Returns:
            Dictionary with market data or None if failed
        """
        try:
            url = f"{WagriMarketService.BASE_URL}/{market_survey_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error fetching data: Status {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching WAGRI data: {str(e)}")
            return None
    
    @staticmethod
    def convert_jpy_to_idr(jpy_amount: float) -> float:
        """Convert JPY to IDR using current exchange rate."""
        return jpy_amount * WagriMarketService.EXCHANGE_RATE_JPY_TO_IDR
    
    @staticmethod
    def convert_idr_to_jpy(idr_amount: float) -> float:
        """Convert IDR to JPY using current exchange rate."""
        return idr_amount / WagriMarketService.EXCHANGE_RATE_JPY_TO_IDR
    
    def calculate_export_margin(
        self,
        japan_price_jpy: float,
        indonesia_production_cost: float,
        packaging_cost: float = 5000,
        transport_to_port: float = 3000,
        air_freight_per_kg: float = 80000,
        customs_duty: float = 10000,
        certification_cost: float = 2000
    ) -> Dict:
        """
        Calculate export margin and profitability.
        
        Args:
            japan_price_jpy: Current price in Japan (JPY per kg)
            indonesia_production_cost: Production cost in Indonesia (IDR per kg)
            packaging_cost: Packaging cost (IDR)
            transport_to_port: Transport to port (IDR)
            air_freight_per_kg: Air freight cost (IDR per kg)
            customs_duty: Customs duty (IDR)
            certification_cost: Certification cost (IDR)
        
        Returns:
            Dictionary with margin analysis
        """
        # Convert Japan price to IDR
        japan_price_idr = self.convert_jpy_to_idr(japan_price_jpy)
        
        # Calculate total Indonesia cost
        total_indonesia_cost = (
            indonesia_production_cost +
            packaging_cost +
            transport_to_port
        )
        
        # Calculate total export cost
        total_export_cost = (
            air_freight_per_kg +
            customs_duty +
            certification_cost
        )
        
        # Total cost
        total_cost = total_indonesia_cost + total_export_cost
        
        # Margin calculations
        gross_margin = japan_price_idr - total_cost
        margin_percentage = (gross_margin / japan_price_idr * 100) if japan_price_idr > 0 else 0
        
        # Profitability score
        if margin_percentage > 40:
            profitability = "Sangat Menguntungkan"
            score = 5
        elif margin_percentage > 25:
            profitability = "Menguntungkan"
            score = 4
        elif margin_percentage > 10:
            profitability = "Cukup Menguntungkan"
            score = 3
        elif margin_percentage > 0:
            profitability = "Kurang Menguntungkan"
            score = 2
        else:
            profitability = "Tidak Menguntungkan"
            score = 1
        
        return {
            "japan_price_jpy": japan_price_jpy,
            "japan_price_idr": japan_price_idr,
            "indonesia_cost": total_indonesia_cost,
            "export_cost": total_export_cost,
            "total_cost": total_cost,
            "gross_margin": gross_margin,
            "margin_percentage": margin_percentage,
            "profitability": profitability,
            "profitability_score": score,
            "roi_percentage": (gross_margin / total_cost * 100) if total_cost > 0 else 0,
            "cost_breakdown": {
                "production": indonesia_production_cost,
                "packaging": packaging_cost,
                "transport": transport_to_port,
                "air_freight": air_freight_per_kg,
                "customs": customs_duty,
                "certification": certification_cost
            }
        }
    
    def cache_price_data(self, commodity_code: str, data: Dict):
        """
        Cache price data for a commodity.
        
        Args:
            commodity_code: Item code (e.g., "33100")
            data: Market data to cache
        """
        # Update latest prices cache
        latest_cache_file = self.CACHE_DIR / "prices_latest.json"
        
        try:
            with open(latest_cache_file, 'r') as f:
                latest_cache = json.load(f)
        except:
            latest_cache = {}
        
        latest_cache[commodity_code] = {
            "data": data,
            "timestamp": datetime.now().isoformat()
        }
        
        with open(latest_cache_file, 'w') as f:
            json.dump(latest_cache, f, indent=2)
        
        # Update historical data
        history_file = self.CACHE_DIR / "prices_history" / f"{commodity_code}.json"
        
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
        except:
            history = []
        
        history.append({
            "date": data.get("TargetDate", datetime.now().isoformat()),
            "price": data.get("AveragePrice"),
            "volume": data.get("TradingVolume"),
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 90 days
        history = history[-90:]
        
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_cached_price(self, commodity_code: str) -> Optional[Dict]:
        """
        Get cached price data for a commodity.
        
        Args:
            commodity_code: Item code
        
        Returns:
            Cached data or None
        """
        latest_cache_file = self.CACHE_DIR / "prices_latest.json"
        
        try:
            with open(latest_cache_file, 'r') as f:
                latest_cache = json.load(f)
            
            if commodity_code in latest_cache:
                cached = latest_cache[commodity_code]
                # Check if cache is fresh (< 1 hour)
                cache_time = datetime.fromisoformat(cached["timestamp"])
                if datetime.now() - cache_time < timedelta(hours=1):
                    return cached["data"]
        except:
            pass
        
        return None
    
    def get_price_history(self, commodity_code: str, days: int = 30) -> List[Dict]:
        """
        Get price history for a commodity.
        
        Args:
            commodity_code: Item code
            days: Number of days to retrieve
        
        Returns:
            List of historical price data
        """
        history_file = self.CACHE_DIR / "prices_history" / f"{commodity_code}.json"
        
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
            
            # Return last N days
            return history[-days:]
        except:
            return []
    
    def calculate_price_trend(self, commodity_code: str, days: int = 7) -> Dict:
        """
        Calculate price trend for a commodity.
        
        Args:
            commodity_code: Item code
            days: Number of days for trend analysis
        
        Returns:
            Trend analysis data
        """
        history = self.get_price_history(commodity_code, days)
        
        if len(history) < 2:
            return {
                "trend": "Unknown",
                "change_percentage": 0,
                "direction": "stable"
            }
        
        # Get first and last prices
        first_price = history[0].get("price", 0)
        last_price = history[-1].get("price", 0)
        
        if first_price == 0:
            return {
                "trend": "Unknown",
                "change_percentage": 0,
                "direction": "stable"
            }
        
        # Calculate change
        change = last_price - first_price
        change_percentage = (change / first_price) * 100
        
        # Determine direction
        if change_percentage > 5:
            direction = "rising"
            trend = "📈 Naik"
        elif change_percentage < -5:
            direction = "falling"
            trend = "📉 Turun"
        else:
            direction = "stable"
            trend = "→ Stabil"
        
        return {
            "trend": trend,
            "change_percentage": change_percentage,
            "direction": direction,
            "first_price": first_price,
            "last_price": last_price,
            "change_amount": change
        }
    
    @staticmethod
    def format_price_idr(amount: float) -> str:
        """Format price in IDR with thousand separators."""
        return f"Rp {amount:,.0f}".replace(",", ".")
    
    @staticmethod
    def format_price_jpy(amount: float) -> str:
        """Format price in JPY with thousand separators."""
        return f"¥{amount:,.0f}".replace(",", ".")
