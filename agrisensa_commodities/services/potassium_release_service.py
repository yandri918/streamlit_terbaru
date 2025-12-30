"""
Potassium (K) Release Service for Organic Fertilizers
Based on WAGRI FertilizerEffectInformationK API

Author: AgriSensa Team
Date: 2025-12-30
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional


class PotassiumReleaseService:
    """
    Service for calculating potassium availability from organic fertilizers.
    Based on WAGRI methodology - K is immediately available (like P).
    """
    
    # WAGRI scaling factor (calibrated from example data)
    SCALING_FACTOR = 0.955
    
    # WAGRI Material Types (13 types)
    MATERIAL_TYPES = {
        1: "Kompos Kotoran Sapi",
        2: "Kompos Kotoran Babi",
        3: "Kompos Kotoran Ayam",
        4: "Residu Minyak Sayur",
        5: "Residu Ikan",
        6: "Tepung Tulang",
        7: "Dedak Padi",
        8: "Rumput (Gandum Hitam, Gandum, Rumput Jepang)",
        9: "Rumput (Sorgum, Rumput Sudan)",
        10: "Silangan (Mustard Putih, Mustard Hitam)",
        11: "Kacang-kacangan (Vetch Berbulu, Semanggi Merah)",
        12: "Kacang-kacangan (Crotararia)",
        13: "Asteraceae (Bunga Matahari)"
    }
    
    # Material Presets with typical TK (Total Potassium) values
    MATERIAL_PRESETS = {
        "Kompos Kotoran Sapi": {
            "MC": 40.0,
            "TK": 1.2,
            "material_type": 1,
            "category": "Kompos Kotoran Ternak",
            "description": "K rendah, cocok untuk tanah dengan K tinggi"
        },
        "Kompos Kotoran Babi": {
            "MC": 35.0,
            "TK": 1.8,
            "material_type": 2,
            "category": "Kompos Kotoran Ternak",
            "description": "K sedang, balance NPK baik"
        },
        "Kompos Kotoran Ayam": {
            "MC": 30.0,
            "TK": 2.5,
            "material_type": 3,
            "category": "Kompos Kotoran Ternak",
            "description": "K tinggi, cocok untuk tanaman buah"
        },
        "Residu Minyak Sayur": {
            "MC": 20.0,
            "TK": 1.5,
            "material_type": 4,
            "category": "Bahan Komersial",
            "description": "K sedang, kaya nitrogen"
        },
        "Residu Ikan": {
            "MC": 25.0,
            "TK": 1.0,
            "material_type": 5,
            "category": "Bahan Komersial",
            "description": "K rendah, tinggi N dan P"
        },
        "Tepung Tulang": {
            "MC": 10.0,
            "TK": 0.5,
            "material_type": 6,
            "category": "Bahan Komersial",
            "description": "K sangat rendah, fokus P dan Ca"
        },
        "Dedak Padi": {
            "MC": 15.0,
            "TK": 1.2,
            "material_type": 7,
            "category": "Bahan Komersial",
            "description": "K sedang, sumber silika"
        },
        "Rumput Gandum": {
            "MC": 70.0,
            "TK": 2.8,
            "material_type": 8,
            "category": "Pupuk Hijau",
            "description": "K tinggi, pupuk hijau musim dingin"
        },
        "Rumput Sorgum": {
            "MC": 75.0,
            "TK": 3.2,
            "material_type": 9,
            "category": "Pupuk Hijau",
            "description": "K sangat tinggi, biomassa besar"
        },
        "Mustard": {
            "MC": 80.0,
            "TK": 2.5,
            "material_type": 10,
            "category": "Pupuk Hijau",
            "description": "K tinggi, biofumigant"
        },
        "Vetch": {
            "MC": 75.0,
            "TK": 2.0,
            "material_type": 11,
            "category": "Pupuk Hijau",
            "description": "K sedang, fiksasi N tinggi"
        },
        "Crotararia": {
            "MC": 78.0,
            "TK": 2.2,
            "material_type": 12,
            "category": "Pupuk Hijau",
            "description": "K sedang-tinggi, nematisida"
        },
        "Bunga Matahari": {
            "MC": 72.0,
            "TK": 3.5,
            "material_type": 13,
            "category": "Pupuk Hijau",
            "description": "K sangat tinggi, akumulator K"
        }
    }
    
    # Default coefficients
    DEFAULT_COEFFICIENTS = {
        "Region_PK": 1,    # Indonesia = 1
        "FE_K": 70         # 70% efficiency (typical for organic K)
    }
    
    @staticmethod
    def calculate_k_release(
        start_date: str,
        end_date: str,
        material_amount: float,
        material_type: int,
        material_props: dict,
        coefficients: dict
    ) -> Dict:
        """
        Calculate potassium availability from organic fertilizer.
        
        Unlike nitrogen, K is immediately available and constant over time (like P).
        
        Args:
            start_date: Start date (YYYYMMDD)
            end_date: End date (YYYYMMDD)
            material_amount: Amount of material (kg)
            material_type: WAGRI material type (1-13)
            material_props: {"MC": float, "TK": float}
            coefficients: {"FE_K": float, "Region_PK": float}
        
        Returns:
            Dictionary with K availability data
        """
        # Extract parameters
        MC = material_props.get("MC", 35.0)
        TK = material_props.get("TK", 2.0)
        
        FE_K = coefficients.get("FE_K", 70)
        Region_PK = coefficients.get("Region_PK", 1)
        
        # Calculate total K in material
        total_k = material_amount * (TK / 100.0)
        
        # Calculate available K (with WAGRI scaling factor)
        available_k = total_k * (FE_K / 100.0) * Region_PK * PotassiumReleaseService.SCALING_FACTOR
        
        # K is constant throughout the period (no daily variation)
        total_days = (datetime.strptime(end_date, "%Y%m%d") - 
                     datetime.strptime(start_date, "%Y%m%d")).days + 1
        
        cum_list = [available_k] * total_days  # Constant value
        
        return {
            "output_code": 0,
            "start_date": start_date,
            "end_date": end_date,
            "cum_list": cum_list,
            "total_days": total_days,
            "total_k_in_material": total_k,
            "available_k": available_k,
            "availability_percentage": FE_K,
            "material_amount": material_amount,
            "material_type": material_type,
            "material_type_name": PotassiumReleaseService.MATERIAL_TYPES.get(material_type, "Unknown"),
            "material_props": material_props,
            "coefficients": coefficients
        }
    
    @staticmethod
    def convert_k_to_k2o(k_amount: float) -> float:
        """
        Convert K to K2O.
        K2O = K × 1.205
        """
        return k_amount * 1.205
    
    @staticmethod
    def convert_k2o_to_k(k2o_amount: float) -> float:
        """
        Convert K2O to K.
        K = K2O / 1.205
        """
        return k2o_amount / 1.205
    
    @staticmethod
    def compare_with_synthetic(
        organic_k: float,
        synthetic_type: str = "KCl"
    ) -> Dict:
        """
        Compare organic K with synthetic fertilizer.
        
        Args:
            organic_k: Available K from organic (kg)
            synthetic_type: Type of synthetic (KCl, K2SO4, NPK, KNO3)
        
        Returns:
            Comparison data
        """
        # Synthetic K content (as K2O)
        synthetic_k2o_content = {
            "KCl": 60.0,        # 60% K2O (Muriate of Potash)
            "K2SO4": 50.0,      # 50% K2O (Sulfate of Potash - premium)
            "NPK 15-15-15": 15.0,
            "NPK 16-16-16": 16.0,
            "KNO3": 46.0        # 46% K2O + 13% N (Potassium Nitrate)
        }
        
        # Additional info for each fertilizer
        fertilizer_info = {
            "KCl": "Pupuk K paling umum, harga ekonomis",
            "K2SO4": "Premium (tanpa Cl), cocok untuk tanaman sensitif",
            "NPK 15-15-15": "Pupuk lengkap, praktis",
            "NPK 16-16-16": "Pupuk lengkap konsentrasi tinggi",
            "KNO3": "Premium + bonus Nitrogen, larut sempurna"
        }
        
        k2o_content = synthetic_k2o_content.get(synthetic_type, 60.0)
        
        # Convert organic K to K2O for comparison
        organic_k2o = PotassiumReleaseService.convert_k_to_k2o(organic_k)
        
        # Calculate equivalent synthetic fertilizer needed
        synthetic_needed = organic_k2o / (k2o_content / 100.0)
        
        return {
            "organic_k": organic_k,
            "organic_k2o": organic_k2o,
            "synthetic_type": synthetic_type,
            "synthetic_k2o_content": k2o_content,
            "synthetic_needed_kg": synthetic_needed,
            "fertilizer_info": fertilizer_info.get(synthetic_type, ""),
            "advantage": "Pupuk organik menyediakan K + memperbaiki CEC tanah + mengurangi leaching"
        }
    
    @staticmethod
    def recommend_split_application(
        available_k: float,
        crop_type: str = "general",
        soil_type: str = "medium"
    ) -> Dict:
        """
        Recommend split application schedule for K.
        
        Unlike P (once), K should be split 2-3 times to:
        - Prevent luxury consumption
        - Reduce leaching losses (especially in sandy soils)
        - Match crop demand curve
        
        Args:
            available_k: Total K available (kg)
            crop_type: Type of crop (rice, corn, vegetables, fruits, general)
            soil_type: Soil texture (sandy, medium, clay)
        
        Returns:
            Split application schedule
        """
        # Adjust splits based on soil type
        if soil_type == "sandy":
            # Sandy soil: More splits to reduce leaching
            base_splits = 3
        elif soil_type == "clay":
            # Clay soil: Fewer splits OK (high CEC)
            base_splits = 2
        else:
            # Medium soil
            base_splits = 2
        
        if crop_type == "rice":
            # Padi: 3 kali (basal, tillering, panicle)
            return {
                "splits": 3,
                "reason": "Padi membutuhkan K di 3 fase kritis",
                "schedule": [
                    {
                        "timing": "Basal (sebelum tanam)",
                        "percentage": 40,
                        "amount_k": available_k * 0.4,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.4),
                        "notes": "Campur dengan tanah saat olah tanah"
                    },
                    {
                        "timing": "Tillering (3-4 minggu)",
                        "percentage": 30,
                        "amount_k": available_k * 0.3,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.3),
                        "notes": "Top dress saat anakan aktif"
                    },
                    {
                        "timing": "Panicle initiation (6-7 minggu)",
                        "percentage": 30,
                        "amount_k": available_k * 0.3,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.3),
                        "notes": "Untuk pengisian bulir optimal"
                    }
                ]
            }
        elif crop_type == "corn":
            # Jagung: 2 kali (basal, V6-V8)
            return {
                "splits": 2,
                "reason": "Jagung butuh K tinggi saat vegetatif dan generatif",
                "schedule": [
                    {
                        "timing": "Basal (saat tanam)",
                        "percentage": 50,
                        "amount_k": available_k * 0.5,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.5),
                        "notes": "Band placement dekat baris tanam"
                    },
                    {
                        "timing": "V6-V8 (4-5 minggu)",
                        "percentage": 50,
                        "amount_k": available_k * 0.5,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.5),
                        "notes": "Side dress sebelum fase reproduktif"
                    }
                ]
            }
        elif crop_type == "vegetables":
            # Sayuran: 2-3 kali tergantung soil
            splits = base_splits
            if splits == 3:
                return {
                    "splits": 3,
                    "reason": "Sayuran di tanah berpasir perlu aplikasi bertahap",
                    "schedule": [
                        {
                            "timing": "Basal (sebelum tanam)",
                            "percentage": 40,
                            "amount_k": available_k * 0.4,
                            "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.4),
                            "notes": "Campur dengan media tanam"
                        },
                        {
                            "timing": "2-3 minggu setelah tanam",
                            "percentage": 30,
                            "amount_k": available_k * 0.3,
                            "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.3),
                            "notes": "Fertigasi atau top dress"
                        },
                        {
                            "timing": "4-5 minggu setelah tanam",
                            "percentage": 30,
                            "amount_k": available_k * 0.3,
                            "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.3),
                            "notes": "Saat pembentukan hasil"
                        }
                    ]
                }
            else:
                return {
                    "splits": 2,
                    "reason": "Sayuran di tanah medium cukup 2 kali aplikasi",
                    "schedule": [
                        {
                            "timing": "Basal (sebelum tanam)",
                            "percentage": 60,
                            "amount_k": available_k * 0.6,
                            "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.6),
                            "notes": "Campur dengan media tanam"
                        },
                        {
                            "timing": "3-4 minggu setelah tanam",
                            "percentage": 40,
                            "amount_k": available_k * 0.4,
                            "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.4),
                            "notes": "Saat pertumbuhan aktif"
                        }
                    ]
                }
        elif crop_type == "fruits":
            # Buah: 2 kali (vegetatif, generatif)
            return {
                "splits": 2,
                "reason": "Tanaman buah butuh K tinggi saat pembuahan",
                "schedule": [
                    {
                        "timing": "Awal musim (vegetatif)",
                        "percentage": 40,
                        "amount_k": available_k * 0.4,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.4),
                        "notes": "Untuk pertumbuhan tunas dan daun"
                    },
                    {
                        "timing": "Saat pembungaan/pembuahan",
                        "percentage": 60,
                        "amount_k": available_k * 0.6,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.6),
                        "notes": "Untuk kualitas buah (ukuran, warna, rasa)"
                    }
                ]
            }
        else:
            # General: 2 kali
            return {
                "splits": 2,
                "reason": "Aplikasi standar untuk tanaman umum",
                "schedule": [
                    {
                        "timing": "Basal (saat tanam)",
                        "percentage": 60,
                        "amount_k": available_k * 0.6,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.6),
                        "notes": "Aplikasi dasar"
                    },
                    {
                        "timing": "Mid-season (4-6 minggu)",
                        "percentage": 40,
                        "amount_k": available_k * 0.4,
                        "amount_k2o": PotassiumReleaseService.convert_k_to_k2o(available_k * 0.4),
                        "notes": "Top dress saat pertumbuhan aktif"
                    }
                ]
            }
    
    @staticmethod
    def list_material_presets() -> List[str]:
        """Get list of available material presets."""
        return list(PotassiumReleaseService.MATERIAL_PRESETS.keys())
    
    @staticmethod
    def get_material_preset(material_name: str) -> Dict:
        """Get preset data for a specific material."""
        return PotassiumReleaseService.MATERIAL_PRESETS.get(material_name, {})
    
    @staticmethod
    def validate_inputs(
        start_date: str,
        end_date: str,
        material_amount: float,
        material_props: dict
    ) -> tuple:
        """
        Validate input parameters.
        
        Returns:
            (is_valid: bool, error_message: str)
        """
        try:
            # Validate dates
            start_dt = datetime.strptime(start_date, "%Y%m%d")
            end_dt = datetime.strptime(end_date, "%Y%m%d")
            
            if end_dt <= start_dt:
                return False, "End date must be after start date"
            
            # Validate material amount
            if material_amount <= 0:
                return False, "Material amount must be positive"
            
            # Validate material properties
            if "TK" not in material_props:
                return False, "TK (Total Potassium) is required"
            
            if material_props["TK"] < 0 or material_props["TK"] > 10:
                return False, "TK must be between 0 and 10%"
            
            return True, ""
            
        except ValueError as e:
            return False, f"Invalid input: {str(e)}"
