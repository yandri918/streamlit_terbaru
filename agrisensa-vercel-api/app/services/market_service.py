"""Market service for commodity price data."""
import random
from datetime import datetime, timedelta


class MarketService:
    """Service for market price data."""
    
    # Database harga dasar (per 25 November 2025)
    PRICE_DB = {
        # --- Sayuran & Bumbu ---
        "cabai_merah_keriting": {"name": "Cabai Merah Keriting", "unit": "kg", "base": 45000},
        "cabai_rawit_merah": {"name": "Cabai Rawit Merah", "unit": "kg", "base": 65000},
        "bawang_merah": {"name": "Bawang Merah", "unit": "kg", "base": 30000},
        "bawang_putih": {"name": "Bawang Putih", "unit": "kg", "base": 42000},
        "tomat": {"name": "Tomat", "unit": "kg", "base": 12000},
        "kentang": {"name": "Kentang", "unit": "kg", "base": 18000},
        "wortel": {"name": "Wortel", "unit": "kg", "base": 14000},
        "kubis": {"name": "Kubis", "unit": "kg", "base": 8000},
        
        # --- Sembako / Pangan Pokok ---
        "beras_premium": {"name": "Beras Premium", "unit": "kg", "base": 16000},
        "beras_medium": {"name": "Beras Medium", "unit": "kg", "base": 14500},
        "gula_pasir": {"name": "Gula Pasir", "unit": "kg", "base": 18500},
        "minyak_goreng_kemasan": {"name": "Minyak Goreng Kemasan", "unit": "liter", "base": 21500},
        "minyak_goreng_curah": {"name": "Minyak Goreng Curah", "unit": "liter", "base": 18000},
        "telur_ayam": {"name": "Telur Ayam Ras", "unit": "kg", "base": 28000},
        "daging_ayam": {"name": "Daging Ayam Ras", "unit": "kg", "base": 39000},
        "daging_sapi": {"name": "Daging Sapi Murni", "unit": "kg", "base": 135000},
        "tepung_terigu": {"name": "Tepung Terigu", "unit": "kg", "base": 13000},
        
        # --- Palawija ---
        "jagung_pipilan": {"name": "Jagung Pipilan", "unit": "kg", "base": 5500},
        "kedelai": {"name": "Kedelai Impor", "unit": "kg", "base": 10500},
        "kacang_tanah": {"name": "Kacang Tanah", "unit": "kg", "base": 28000},
        "ubi_kayu": {"name": "Ubi Kayu", "unit": "kg", "base": 4500},
    }

    @classmethod
    def get_current_prices(cls, commodity):
        """Get current market prices for commodity."""
        base_data = cls.PRICE_DB.get(commodity)
        if not base_data:
            return None
        
        # Simulate market variations
        base_price = base_data["base"]
        return {
            "name": base_data["name"],
            "unit": base_data["unit"],
            "prices": {
                "Pasar Tradisional": int(base_price * random.uniform(0.98, 1.02)), # +/- 2%
                "Pasar Modern": int(base_price * random.uniform(1.10, 1.15)),      # +10-15%
                "Tingkat Petani/Produsen": int(base_price * random.uniform(0.75, 0.85)) # -15-25%
            }
        }
    
    @staticmethod
    def get_ticker_prices():
        """Get ticker prices for multiple commodities (Simulated Real-time)."""
        ticker_items = [
            {"id": "cabai_merah_keriting", "name": "Cabai Merah", "base": 45000},
            {"id": "bawang_merah", "name": "Bawang Merah", "base": 30000},
            {"id": "beras_medium", "name": "Beras Medium", "base": 14500},
            {"id": "gula_pasir", "name": "Gula Pasir", "base": 18500},
            {"id": "minyak_goreng_curah", "name": "Minyak Curah", "base": 18000},
            {"id": "telur_ayam", "name": "Telur Ayam", "base": 28000},
            {"id": "daging_ayam", "name": "Daging Ayam", "base": 39000},
            {"id": "daging_sapi", "name": "Daging Sapi", "base": 135000}
        ]
        
        live_data = []
        for item in ticker_items:
            # Random fluctuation for "live" feel
            variation = random.uniform(-0.03, 0.03)
            price = int(item["base"] * (1 + variation))
            live_data.append({
                "name": item["name"],
                "price": price,
                "unit": "kg" if "liter" not in item.get("unit", "kg") else "liter" # Simplification
            })
        
        return live_data
    
    @classmethod
    def get_historical_prices(cls, commodity, days):
        """Get historical price data with realistic trends."""
        base_data = cls.PRICE_DB.get(commodity)
        if not base_data:
            return None
            
        base_price = base_data["base"]
        
        labels = []
        prices = []
        
        # Generate trend
        # We'll use a random walk but with a slight trend component to look realistic
        current_price = base_price
        today = datetime.now()
        
        # Create a trend curve (e.g., slight inflation or seasonal dip)
        trend_factor = random.choice([-0.001, 0.001, 0]) 
        
        for i in range(days):
            date = today - timedelta(days=days - i - 1)
            labels.append(date.strftime('%d %b'))
            
            # Random daily fluctuation
            daily_volatility = 0.02 if "cabai" in commodity or "bawang" in commodity else 0.005 # Volatile vs Stable items
            change = random.uniform(-daily_volatility, daily_volatility) + trend_factor
            
            current_price = current_price * (1 + change)
            prices.append(int(current_price))
        
        return {
            "labels": labels,
            "prices": prices
        }

    @classmethod
    def predict_price_trend(cls, commodity, target_date_str):
        """
        Predict price trend using Linear Regression.
        
        Args:
            commodity (str): Commodity ID.
            target_date_str (str): Target date in 'YYYY-MM-DD' format.
            
        Returns:
            dict: Prediction result including price, trend, and insight.
        """
        try:
            from sklearn.linear_model import LinearRegression
            import numpy as np
        except ImportError:
            return {"error": "scikit-learn not installed"}

        # 1. Generate 1 year of historical data (synthetic)
        history = cls.get_historical_prices(commodity, 365)
        if not history:
            return None

        prices = history['prices']
        
        # Prepare data for Linear Regression
        # X = Days from start (0 to 364), y = Price
        X = np.array(range(len(prices))).reshape(-1, 1)
        y = np.array(prices)

        # 2. Train Model
        model = LinearRegression()
        model.fit(X, y)

        # 3. Calculate days to target date
        today = datetime.now()
        target_date = datetime.strptime(target_date_str, '%Y-%m-%d')
        days_diff = (target_date - today).days
        
        if days_diff < 0:
            return {"error": "Target date must be in the future"}

        # Target X is 365 (today) + days_diff
        target_X = np.array([[365 + days_diff]])
        predicted_price = int(model.predict(target_X)[0])

        # 4. Analyze Trend
        slope = model.coef_[0]
        if slope > 50:
            trend = "Naik Tajam"
            insight = "Harga diperkirakan akan melonjak signifikan. Disarankan untuk segera membeli atau mengamankan stok."
        elif slope > 10:
            trend = "Naik"
            insight = "Tren harga menunjukkan kenaikan moderat. Waspadai potensi kenaikan biaya produksi."
        elif slope < -50:
            trend = "Turun Tajam"
            insight = "Harga diperkirakan akan anjlok. Potensi keuntungan bagi pembeli, namun risiko bagi produsen."
        elif slope < -10:
            trend = "Turun"
            insight = "Tren harga cenderung menurun. Waktu yang baik untuk menunggu harga lebih rendah."
        else:
            trend = "Stabil"
            insight = "Harga relatif stabil. Pergerakan harga tidak signifikan dalam jangka pendek."

        return {
            "commodity_name": cls.PRICE_DB[commodity]["name"],
            "current_price": prices[-1],
            "predicted_price": predicted_price,
            "prediction_date": target_date.strftime('%d %B %Y'),
            "trend": trend,
            "insight": insight,
            "historical_data": {
                "labels": history['labels'][-30:], # Last 30 days for chart
                "prices": prices[-30:]
            }
        }

    @classmethod
    def get_forecast(cls, commodity, days=7):
        """
        Get price forecast for the next N days.
        """
        try:
            from sklearn.linear_model import LinearRegression
            import numpy as np
        except ImportError:
            return None

        # 1. Get historical data
        history = cls.get_historical_prices(commodity, 365)
        if not history:
            return None

        prices = history['prices']
        X = np.array(range(len(prices))).reshape(-1, 1)
        y = np.array(prices)

        # 2. Train Model
        model = LinearRegression()
        model.fit(X, y)

        # 3. Predict Future
        last_day_index = len(prices)
        future_X = np.array(range(last_day_index, last_day_index + days)).reshape(-1, 1)
        predictions = model.predict(future_X)

        # 4. Format Result
        forecast_data = []
        today = datetime.now()
        
        for i, price in enumerate(predictions):
            date = today + timedelta(days=i+1)
            forecast_data.append({
                "date": date.strftime('%d %b'),
                "price": int(price)
            })
            
        return {
            "commodity": cls.PRICE_DB[commodity]["name"],
            "forecast": forecast_data,
            "trend": "naik" if model.coef_[0] > 0 else "turun"
        }
