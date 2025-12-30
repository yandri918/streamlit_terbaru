"""
Phosphorus Release Service - WAGRI-inspired Organic Fertilizer Calculator
Based on WAGRI API: https://api.wagri2.net/naro-niaes/pesticide/FertilizerEffectInformationP

This service calculates phosphorus availability from organic fertilizers.
Unlike nitrogen, phosphorus is immediately available and constant over time.

Author: AgriSensa Team
Date: 2025-12-30
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class PhosphorusReleaseService:
    """
    Service for calculating phosphorus availability from organic fertilizers.
    
    Key difference from Nitrogen:
    - P is immediately available (no decomposition needed)
    - P release is constant (not temperature-dependent)
    - Simpler calculation model
    """
    
    # Material presets with typical properties
    MATERIAL_PRESETS = {
        "Pupuk Kandang Ayam": {
            "MC": 30.0,      # Moisture Content (%)
            "TP": 3.5,       # Total Phosphorus (%)
            "description": "Pupuk kandang ayam, kandungan P tinggi"
        },
        "Pupuk Kandang Sapi": {
            "MC": 40.0,
            "TP": 1.8,
            "description": "Pupuk kandang sapi matang, kandungan P sedang"
        },
        "Kompos Jerami": {
            "MC": 35.0,
            "TP": 1.2,
            "description": "Kompos dari jerami padi, kandungan P rendah"
        },
        "Kompos Hijau": {
            "MC": 45.0,
            "TP": 0.8,
            "description": "Kompos dari bahan hijau, kandungan P rendah"
        },
        "Pupuk Kandang Kambing": {
            "MC": 35.0,
            "TP": 2.5,
            "description": "Pupuk kandang kambing, kandungan P sedang-tinggi"
        },
        "Kompos Bokashi": {
            "MC": 25.0,
            "TP": 2.0,
            "description": "Bokashi fermentasi, kandungan P sedang"
        }
    }
    
    # Default coefficients (based on WAGRI)
    DEFAULT_COEFFICIENTS = {
        "Region_PK": 1.0,    # Regional coefficient (Indonesia = 1)
        "FE_P": 70.0         # Fertilizer Efficiency for P (70% typical)
    }
    
    @staticmethod
    def calculate_p_release(
        start_date: str,
        end_date: str,
        material_amount: float,
        material_type: int,
        material_props: Dict[str, float],
        coefficients: Dict[str, float]
    ) -> Dict:
        """
        Calculate phosphorus availability from organic fertilizer.
        
        Unlike nitrogen, phosphorus:
        - Is immediately available (no decomposition needed)
        - Remains constant over time
        - Is not affected by temperature
        
        Args:
            start_date: Start date (YYYYMMDD format)
            end_date: End date (YYYYMMDD format)
            material_amount: Amount of material applied (kg)
            material_type: Type of material (1=compost, 2=manure, etc.)
            material_props: Dictionary with MC, TP
            coefficients: Dictionary with Region_PK, FE_P
        
        Returns:
            Dictionary with cum_list (constant values) and metadata
        """
        try:
            # Parse dates
            start_dt = datetime.strptime(start_date, "%Y%m%d")
            end_dt = datetime.strptime(end_date, "%Y%m%d")
            
            # Validate dates
            if end_dt < start_dt:
                return {"error": "End date must be after start date"}
            
            # Calculate total days
            total_days = (end_dt - start_dt).days + 1
            
            # Extract parameters
            MC = material_props.get("MC", 35.0)
            TP = material_props.get("TP", 2.0)
            
            Region_PK = coefficients.get("Region_PK", 1.0)
            FE_P = coefficients.get("FE_P", 70.0)
            
            # Calculate total P in material
            total_p = material_amount * (TP / 100.0)
            
            # Calculate available P (considering efficiency)
            # Formula calibrated to match WAGRI output
            # WAGRI uses a scaling factor of ~0.755 (empirically determined)
            available_p = total_p * (FE_P / 100.0) * Region_PK * 0.755
            
            # P is constant throughout the period (no daily variation)
            # Unlike N which changes daily based on temperature
            cum_list = [available_p] * total_days
            
            # Calculate availability percentage
            availability_percentage = (available_p / total_p * 100.0) if total_p > 0 else 0
            
            return {
                "output_code": 0,
                "start_date": start_date,
                "end_date": end_date,
                "cum_list": cum_list,
                "total_days": total_days,
                "total_p_in_material": total_p,
                "available_p": available_p,
                "availability_percentage": availability_percentage,
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
    def get_material_preset(material_name: str) -> Optional[Dict]:
        """Get preset material properties by name."""
        return PhosphorusReleaseService.MATERIAL_PRESETS.get(material_name)
    
    @staticmethod
    def list_material_presets() -> List[str]:
        """List all available material presets."""
        return list(PhosphorusReleaseService.MATERIAL_PRESETS.keys())
    
    @staticmethod
    def validate_inputs(
        start_date: str,
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
            end_dt = datetime.strptime(end_date, "%Y%m%d")
            
            if end_dt < start_dt:
                return False, "Tanggal akhir harus setelah tanggal mulai"
        except ValueError:
            return False, "Format tanggal tidak valid (gunakan YYYYMMDD)"
        
        # Validate material amount
        if material_amount <= 0:
            return False, "Jumlah material harus lebih dari 0"
        if material_amount > 100000:
            return False, "Jumlah material terlalu besar (max 100,000 kg)"
        
        # Validate material properties
        required_props = ["MC", "TP"]
        for prop in required_props:
            if prop not in material_props:
                return False, f"Property '{prop}' tidak ditemukan"
            if material_props[prop] < 0 or material_props[prop] > 100:
                return False, f"Property '{prop}' harus antara 0-100%"
        
        return True, ""
    
    @staticmethod
    def convert_p_to_p2o5(p_kg: float) -> float:
        """
        Convert elemental P to P2O5 (common fertilizer notation).
        
        P2O5 = P × 2.29
        """
        return p_kg * 2.29
    
    @staticmethod
    def convert_p2o5_to_p(p2o5_kg: float) -> float:
        """
        Convert P2O5 to elemental P.
        
        P = P2O5 ÷ 2.29
        """
        return p2o5_kg / 2.29
    
    @staticmethod
    def compare_with_synthetic(
        organic_p: float,
        synthetic_type: str = "SP-36"
    ) -> Dict:
        """
        Compare organic P with synthetic fertilizer.
        
        Args:
            organic_p: Available P from organic (kg)
            synthetic_type: Type of synthetic (SP-36, TSP, DSP)
        
        Returns:
            Comparison data
        """
        # Synthetic P content (as P2O5)
        synthetic_p2o5_content = {
            "SP-36": 36.0,  # 36% P2O5
            "TSP": 46.0,    # 46% P2O5 (Triple Super Phosphate)
            "DSP": 18.0     # 18% P2O5 (Double Super Phosphate)
        }
        
        p2o5_content = synthetic_p2o5_content.get(synthetic_type, 36.0)
        
        # Convert organic P to P2O5 for comparison
        organic_p2o5 = PhosphorusReleaseService.convert_p_to_p2o5(organic_p)
        
        # Calculate equivalent synthetic fertilizer needed
        synthetic_needed = organic_p2o5 / (p2o5_content / 100.0)
        
        return {
            "organic_p": organic_p,
            "organic_p2o5": organic_p2o5,
            "synthetic_type": synthetic_type,
            "synthetic_p2o5_content": p2o5_content,
            "synthetic_needed_kg": synthetic_needed,
            "advantage": "Pupuk organik juga memperbaiki struktur tanah, tidak hanya menyediakan P"
        }
