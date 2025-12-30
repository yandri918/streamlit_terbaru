"""
Nitrogen Release Service - WAGRI-inspired Organic Fertilizer Calculator
Based on WAGRI API: https://api.wagri2.net/naro-niaes/pesticide/FertilizerEffectInformationN

This service calculates nitrogen release from organic fertilizers over time,
considering temperature, material properties, and decomposition kinetics.

Author: AgriSensa Team
Date: 2025-12-30
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class NitrogenReleaseService:
    """
    Service for calculating nitrogen release from organic fertilizers.
    
    Based on first-order kinetics with temperature adjustment using Q10 coefficient.
    """
    
    # Material presets with typical properties
    MATERIAL_PRESETS = {
        "Kompos Jerami": {
            "MC": 35.0,      # Moisture Content (%)
            "ADSON": 18.0,   # Adsorbable Nitrogen (%)
            "TN": 3.2,       # Total Nitrogen (%)
            "Nm": 0.25,      # Mineral Nitrogen (%)
            "description": "Kompos dari jerami padi, pelepasan nitrogen sedang"
        },
        "Pupuk Kandang Sapi": {
            "MC": 40.0,
            "ADSON": 22.0,
            "TN": 2.8,
            "Nm": 0.35,
            "description": "Pupuk kandang sapi matang, pelepasan nitrogen lambat"
        },
        "Pupuk Kandang Ayam": {
            "MC": 30.0,
            "ADSON": 25.0,
            "TN": 4.5,
            "Nm": 0.45,
            "description": "Pupuk kandang ayam, pelepasan nitrogen cepat"
        },
        "Kompos Hijau": {
            "MC": 45.0,
            "ADSON": 15.0,
            "TN": 2.5,
            "Nm": 0.20,
            "description": "Kompos dari bahan hijau, pelepasan nitrogen lambat"
        },
        "Pupuk Kandang Kambing": {
            "MC": 35.0,
            "ADSON": 24.0,
            "TN": 3.8,
            "Nm": 0.40,
            "description": "Pupuk kandang kambing, pelepasan nitrogen sedang-cepat"
        },
        "Kompos Bokashi": {
            "MC": 25.0,
            "ADSON": 20.0,
            "TN": 3.5,
            "Nm": 0.30,
            "description": "Bokashi fermentasi, pelepasan nitrogen sedang"
        }
    }
    
    # Default coefficients (based on WAGRI example)
    DEFAULT_COEFFICIENTS = {
        "Q10": 1.47,      # Temperature coefficient (1.47 = 47% increase per 10°C)
        "A1": 1595.0,     # Initial rate constant
        "b": 0.189,       # Decay exponent
        "KD": 0.016786    # Decomposition rate constant
    }
    
    @staticmethod
    def calculate_daily_release(
        start_date: str,
        water_date: str,
        end_date: str,
        material_amount: float,
        material_type: int,
        material_props: Dict[str, float],
        coefficients: Dict[str, float],
        daily_temperatures: List[float],
        latitude: Optional[float] = None,
        longitude: Optional[float] = None
    ) -> Dict:
        """
        Calculate daily and cumulative nitrogen release from organic fertilizer.
        
        Args:
            start_date: Start date (YYYYMMDD format)
            water_date: Water application date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)
            material_amount: Amount of material applied (kg)
            material_type: Type of material (1=compost, 2=manure, etc.)
            material_props: Dictionary with MC, ADSON, TN, Nm
            coefficients: Dictionary with Q10, A1, b, KD
            daily_temperatures: List of daily average temperatures (°C)
            latitude: Latitude (for future weather API integration)
            longitude: Longitude (for future weather API integration)
        
        Returns:
            Dictionary with daily_list, cum_list, and metadata
        """
        try:
            # Parse dates
            start_dt = datetime.strptime(start_date, "%Y%m%d")
            water_dt = datetime.strptime(water_date, "%Y%m%d")
            end_dt = datetime.strptime(end_date, "%Y%m%d")
            
            # Validate dates
            if end_dt < start_dt:
                return {"error": "End date must be after start date"}
            if water_dt < start_dt or water_dt > end_dt:
                return {"error": "Water date must be between start and end dates"}
            
            # Calculate total days
            total_days = (end_dt - start_dt).days + 1
            
            # Ensure we have enough temperature data
            if len(daily_temperatures) < total_days:
                # Pad with last temperature or use default
                default_temp = daily_temperatures[-1] if daily_temperatures else 25.0
                daily_temperatures.extend([default_temp] * (total_days - len(daily_temperatures)))
            
            # Extract parameters
            MC = material_props.get("MC", 35.0)
            ADSON = material_props.get("ADSON", 20.0)
            TN = material_props.get("TN", 3.5)
            Nm = material_props.get("Nm", 0.3)
            
            Q10 = coefficients.get("Q10", 1.47)
            A1 = coefficients.get("A1", 1595.0)
            b = coefficients.get("b", 0.189)
            KD = coefficients.get("KD", 0.016786)
            
            # Calculate nitrogen release
            daily_list = []
            cum_list = []
            cumulative = 0.0
            
            for day_idx in range(total_days):
                current_date = start_dt + timedelta(days=day_idx)
                
                # Days since water application
                if current_date < water_dt:
                    days_since_water = 0
                else:
                    days_since_water = (current_date - water_dt).days
                
                # Get temperature for this day
                temp = daily_temperatures[day_idx]
                
                # Calculate release for this day
                daily_release = NitrogenReleaseService._calculate_single_day_release(
                    days_since_water=days_since_water,
                    temperature=temp,
                    material_amount=material_amount,
                    ADSON=ADSON,
                    TN=TN,
                    Nm=Nm,
                    Q10=Q10,
                    A1=A1,
                    b=b,
                    KD=KD
                )
                
                daily_list.append(daily_release)
                cumulative += daily_release
                cum_list.append(cumulative)
            
            # Calculate summary statistics
            total_n_available = material_amount * (TN / 100.0)  # Total N in material
            release_percentage = (cumulative / total_n_available * 100.0) if total_n_available > 0 else 0
            
            return {
                "output_code": 0,
                "start_date": start_date,
                "water_date": water_date,
                "end_date": end_date,
                "daily_list": daily_list,
                "cum_list": cum_list,
                "total_days": total_days,
                "total_release_kg": cumulative,
                "total_n_in_material_kg": total_n_available,
                "release_percentage": release_percentage,
                "material_amount_kg": material_amount,
                "material_props": material_props,
                "coefficients": coefficients
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "output_code": -1
            }
    
    @staticmethod
    def _calculate_single_day_release(
        days_since_water: int,
        temperature: float,
        material_amount: float,
        ADSON: float,
        TN: float,
        Nm: float,
        Q10: float,
        A1: float,
        b: float,
        KD: float
    ) -> float:
        """
        Calculate nitrogen release for a single day.
        
        Formula based on first-order kinetics with temperature adjustment:
        Release = Material × (ADSON/100) × Rate(t, T)
        
        Where:
        Rate(t, T) = A1 × exp(-b × t) × Q10^((T-20)/10) × KD
        
        Args:
            days_since_water: Days since water application
            temperature: Daily average temperature (°C)
            material_amount: Amount of material (kg)
            ADSON: Adsorbable nitrogen (%)
            TN: Total nitrogen (%)
            Nm: Mineral nitrogen (%)
            Q10: Temperature coefficient
            A1: Initial rate constant
            b: Decay exponent
            KD: Decomposition rate constant
        
        Returns:
            Nitrogen release for this day (kg)
        """
        if days_since_water <= 0:
            # Before water application, no release
            return 0.0
        
        # Temperature adjustment factor (Q10 model)
        # Reference temperature is 20°C
        temp_factor = Q10 ** ((temperature - 20.0) / 10.0)
        
        # Time-dependent decay
        time_factor = A1 * np.exp(-b * days_since_water)
        
        # Combined rate with proper scaling
        # Empirically calibrated to match WAGRI output (scaling factor = 655)
        rate = (time_factor * temp_factor * KD) / 655.0
        
        # Total nitrogen available for release (ADSON fraction)
        n_available = material_amount * (ADSON / 100.0)
        
        # Daily release in kg
        daily_release = n_available * rate
        
        return daily_release
    
    @staticmethod
    def get_material_preset(material_name: str) -> Optional[Dict]:
        """Get preset material properties by name."""
        return NitrogenReleaseService.MATERIAL_PRESETS.get(material_name)
    
    @staticmethod
    def list_material_presets() -> List[str]:
        """List all available material presets."""
        return list(NitrogenReleaseService.MATERIAL_PRESETS.keys())
    
    @staticmethod
    def validate_inputs(
        start_date: str,
        water_date: str,
        end_date: str,
        material_amount: float,
        material_props: Dict[str, float]
    ) -> Tuple[bool, str]:
        """
        Validate input parameters.
        
        Returns:
            (is_valid, error_message)
        """
        # Validate dates
        try:
            start_dt = datetime.strptime(start_date, "%Y%m%d")
            water_dt = datetime.strptime(water_date, "%Y%m%d")
            end_dt = datetime.strptime(end_date, "%Y%m%d")
            
            if end_dt < start_dt:
                return False, "Tanggal akhir harus setelah tanggal mulai"
            if water_dt < start_dt or water_dt > end_dt:
                return False, "Tanggal aplikasi air harus antara tanggal mulai dan akhir"
        except ValueError:
            return False, "Format tanggal tidak valid (gunakan YYYYMMDD)"
        
        # Validate material amount
        if material_amount <= 0:
            return False, "Jumlah material harus lebih dari 0"
        if material_amount > 100000:
            return False, "Jumlah material terlalu besar (max 100,000 kg)"
        
        # Validate material properties
        required_props = ["MC", "ADSON", "TN", "Nm"]
        for prop in required_props:
            if prop not in material_props:
                return False, f"Property '{prop}' tidak ditemukan"
            if material_props[prop] < 0 or material_props[prop] > 100:
                return False, f"Property '{prop}' harus antara 0-100%"
        
        return True, ""
    
    @staticmethod
    def generate_example_temperatures(
        start_date: str,
        end_date: str,
        base_temp: float = 25.0,
        variation: float = 5.0
    ) -> List[float]:
        """
        Generate example temperature data with realistic variation.
        
        Args:
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            base_temp: Base temperature (°C)
            variation: Temperature variation range (°C)
        
        Returns:
            List of daily temperatures
        """
        start_dt = datetime.strptime(start_date, "%Y%m%d")
        end_dt = datetime.strptime(end_date, "%Y%m%d")
        total_days = (end_dt - start_dt).days + 1
        
        # Generate temperatures with sinusoidal variation (simulating day/night cycle)
        temperatures = []
        for day in range(total_days):
            # Add some realistic variation
            daily_var = variation * np.sin(2 * np.pi * day / 7)  # Weekly cycle
            random_var = np.random.uniform(-2, 2)  # Random daily variation
            temp = base_temp + daily_var + random_var
            temperatures.append(round(temp, 1))
        
        return temperatures
    
    @staticmethod
    def compare_with_synthetic(
        organic_release: List[float],
        synthetic_efficiency: float = 0.9
    ) -> Dict:
        """
        Compare organic fertilizer release pattern with synthetic fertilizer.
        
        Args:
            organic_release: Daily release from organic fertilizer
            synthetic_efficiency: Efficiency of synthetic fertilizer (0-1)
        
        Returns:
            Comparison data
        """
        total_organic = sum(organic_release)
        
        # Synthetic fertilizer: immediate release
        synthetic_release = [total_organic * synthetic_efficiency] + [0] * (len(organic_release) - 1)
        
        return {
            "organic_pattern": organic_release,
            "synthetic_pattern": synthetic_release,
            "organic_total": total_organic,
            "synthetic_total": total_organic * synthetic_efficiency,
            "organic_advantage": "Slow release reduces leaching and provides sustained nutrition"
        }
