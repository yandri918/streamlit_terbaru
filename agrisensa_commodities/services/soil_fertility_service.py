# Soil Fertility & Nutrient Management Service
# Based on scientific literature and Albrecht's Base Saturation Method

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class SoilFertilityService:
    """
    Comprehensive soil fertility analysis service
    Based on:
    - Albrecht, W.A. (1975) - Base Saturation Method
    - Troug, E. (1946) - Nutrient Availability by pH
    - Liebig's Law of Minimum
    """
    
    # Ideal base saturation percentages (Albrecht method)
    IDEAL_BASE_SATURATION = {
        'Ca': 65,  # Calcium
        'Mg': 10,  # Magnesium
        'K': 5,    # Potassium
        'Na': 0.5, # Sodium
        'H': 10,   # Hydrogen (acidity)
        'Other': 9.5
    }
    
    # Nutrient sufficiency ranges (ppm or %)
    NUTRIENT_RANGES = {
        'N': {'very_low': (0, 20), 'low': (20, 40), 'medium': (40, 60), 'high': (60, 80), 'very_high': (80, 200)},
        'P': {'very_low': (0, 10), 'low': (10, 20), 'medium': (20, 40), 'high': (40, 60), 'very_high': (60, 150)},
        'K': {'very_low': (0, 100), 'low': (100, 200), 'medium': (200, 300), 'high': (300, 400), 'very_high': (400, 800)},
        'Ca': {'very_low': (0, 500), 'low': (500, 1000), 'medium': (1000, 2000), 'high': (2000, 3000), 'very_high': (3000, 6000)},
        'Mg': {'very_low': (0, 100), 'low': (100, 200), 'medium': (200, 300), 'high': (300, 400), 'very_high': (400, 800)},
        'S': {'very_low': (0, 10), 'low': (10, 20), 'medium': (20, 40), 'high': (40, 60), 'very_high': (60, 100)},
    }
    
    # Micronutrient ranges (ppm)
    MICRONUTRIENT_RANGES = {
        'Fe': {'deficient': (0, 2.5), 'low': (2.5, 4.5), 'sufficient': (4.5, 10), 'high': (10, 50)},
        'Mn': {'deficient': (0, 1), 'low': (1, 5), 'sufficient': (5, 20), 'high': (20, 100)},
        'Cu': {'deficient': (0, 0.2), 'low': (0.2, 0.5), 'sufficient': (0.5, 2), 'high': (2, 10)},
        'Zn': {'deficient': (0, 0.5), 'low': (0.5, 1), 'sufficient': (1, 5), 'high': (5, 20)},
        'B': {'deficient': (0, 0.2), 'low': (0.2, 0.5), 'sufficient': (0.5, 2), 'high': (2, 5)},
        'Mo': {'deficient': (0, 0.05), 'low': (0.05, 0.1), 'sufficient': (0.1, 0.5), 'high': (0.5, 2)},
    }
    
    @staticmethod
    def classify_nutrient_level(nutrient: str, value: float, is_micro: bool = False) -> str:
        """Classify nutrient level based on value"""
        ranges = SoilFertilityService.MICRONUTRIENT_RANGES if is_micro else SoilFertilityService.NUTRIENT_RANGES
        
        if nutrient not in ranges:
            return "Unknown"
        
        for level, (min_val, max_val) in ranges[nutrient].items():
            if min_val <= value < max_val:
                return level.replace('_', ' ').title()
        
        return "Very High" if not is_micro else "High"
    
    @staticmethod
    def calculate_base_saturation(ca_meq: float, mg_meq: float, k_meq: float, na_meq: float, cec: float) -> Dict:
        """
        Calculate base saturation percentages
        
        Args:
            ca_meq: Calcium in meq/100g
            mg_meq: Magnesium in meq/100g
            k_meq: Potassium in meq/100g
            na_meq: Sodium in meq/100g
            cec: Cation Exchange Capacity in meq/100g
            
        Returns:
            Dictionary with base saturation percentages and analysis
        """
        if cec <= 0:
            return {'error': 'CEC must be greater than 0'}
        
        # Calculate percentages
        ca_sat = (ca_meq / cec) * 100
        mg_sat = (mg_meq / cec) * 100
        k_sat = (k_meq / cec) * 100
        na_sat = (na_meq / cec) * 100
        
        total_bases = ca_sat + mg_sat + k_sat + na_sat
        h_sat = 100 - total_bases  # Hydrogen saturation (acidity)
        
        # Calculate ratios
        ca_mg_ratio = ca_meq / mg_meq if mg_meq > 0 else 0
        ca_k_ratio = ca_meq / k_meq if k_meq > 0 else 0
        mg_k_ratio = mg_meq / k_meq if k_meq > 0 else 0
        
        # Ideal ratios (Albrecht)
        ideal_ca_mg = 6.5  # 65:10
        ideal_ca_k = 13    # 65:5
        ideal_mg_k = 2     # 10:5
        
        return {
            'actual': {
                'Ca': round(ca_sat, 2),
                'Mg': round(mg_sat, 2),
                'K': round(k_sat, 2),
                'Na': round(na_sat, 2),
                'H': round(h_sat, 2)
            },
            'ideal': SoilFertilityService.IDEAL_BASE_SATURATION,
            'ratios': {
                'Ca:Mg': round(ca_mg_ratio, 2),
                'Ca:K': round(ca_k_ratio, 2),
                'Mg:K': round(mg_k_ratio, 2)
            },
            'ideal_ratios': {
                'Ca:Mg': ideal_ca_mg,
                'Ca:K': ideal_ca_k,
                'Mg:K': ideal_mg_k
            },
            'total_base_saturation': round(total_bases, 2)
        }
    
    @staticmethod
    def get_nutrient_availability_by_ph(ph: float) -> Dict:
        """
        Calculate relative nutrient availability at given pH
        Based on Troug diagram (1946)
        
        Returns availability as percentage (0-100)
        """
        # Optimal pH ranges for each nutrient
        # Values are approximations from Troug diagram
        
        def availability_curve(ph_val, optimal_ph, width):
            """Gaussian-like curve for availability"""
            return 100 * np.exp(-((ph_val - optimal_ph) ** 2) / (2 * width ** 2))
        
        availability = {
            'N': availability_curve(ph, 6.5, 1.5),
            'P': availability_curve(ph, 6.5, 1.0),
            'K': availability_curve(ph, 6.5, 2.0),
            'S': availability_curve(ph, 6.5, 1.5),
            'Ca': availability_curve(ph, 7.0, 1.5),
            'Mg': availability_curve(ph, 7.0, 1.5),
            'Fe': availability_curve(ph, 5.5, 1.0),
            'Mn': availability_curve(ph, 5.5, 1.0),
            'B': availability_curve(ph, 6.0, 1.5),
            'Cu': availability_curve(ph, 5.5, 1.0),
            'Zn': availability_curve(ph, 6.0, 1.0),
            'Mo': availability_curve(ph, 7.0, 1.0),
        }
        
        return {k: round(min(v, 100), 1) for k, v in availability.items()}
    
    @staticmethod
    def identify_limiting_nutrient(soil_data: Dict) -> Dict:
        """
        Apply Liebig's Law of Minimum to identify limiting nutrient
        
        Args:
            soil_data: Dictionary with nutrient values
            
        Returns:
            Analysis of limiting factors
        """
        # Calculate sufficiency index for each nutrient (0-100)
        sufficiency = {}
        
        for nutrient in ['N', 'P', 'K', 'Ca', 'Mg', 'S']:
            if nutrient not in soil_data:
                continue
            
            value = soil_data[nutrient]
            ranges = SoilFertilityService.NUTRIENT_RANGES[nutrient]
            
            # Calculate sufficiency as percentage of high range
            high_min = ranges['high'][0]
            if value >= high_min:
                sufficiency[nutrient] = 100
            else:
                # Linear interpolation
                medium_max = ranges['medium'][1]
                if value >= medium_max:
                    sufficiency[nutrient] = 70 + (value - medium_max) / (high_min - medium_max) * 30
                else:
                    low_max = ranges['low'][1]
                    if value >= low_max:
                        sufficiency[nutrient] = 40 + (value - low_max) / (medium_max - low_max) * 30
                    else:
                        sufficiency[nutrient] = (value / low_max) * 40
        
        if not sufficiency:
            return {'error': 'No nutrient data provided'}
        
        # Find limiting nutrient (lowest sufficiency)
        limiting = min(sufficiency, key=sufficiency.get)
        
        return {
            'limiting_nutrient': limiting,
            'sufficiency_index': round(sufficiency[limiting], 1),
            'all_sufficiency': {k: round(v, 1) for k, v in sufficiency.items()},
            'interpretation': SoilFertilityService._interpret_limiting_nutrient(limiting, sufficiency[limiting])
        }
    
    @staticmethod
    def _interpret_limiting_nutrient(nutrient: str, sufficiency: float) -> str:
        """Provide interpretation of limiting nutrient"""
        interpretations = {
            'N': "Nitrogen is essential for vegetative growth and protein synthesis. Deficiency causes yellowing of older leaves (chlorosis).",
            'P': "Phosphorus is crucial for root development, flowering, and energy transfer. Deficiency causes purple discoloration and stunted growth.",
            'K': "Potassium regulates water balance, disease resistance, and fruit quality. Deficiency causes marginal leaf burn and weak stems.",
            'Ca': "Calcium is vital for cell wall structure and root growth. Deficiency causes blossom end rot and tip burn.",
            'Mg': "Magnesium is the central atom in chlorophyll. Deficiency causes interveinal chlorosis in older leaves.",
            'S': "Sulfur is needed for protein synthesis and enzyme function. Deficiency causes yellowing of young leaves."
        }
        
        severity = "severe" if sufficiency < 40 else "moderate" if sufficiency < 70 else "mild"
        
        return f"{interpretations.get(nutrient, 'Unknown nutrient')} Current sufficiency is {sufficiency:.1f}% ({severity} limitation)."
    
    @staticmethod
    def calculate_fertilizer_recommendation(soil_data: Dict, target_yield: float, crop: str = "general") -> Dict:
        """
        Calculate fertilizer recommendations based on soil test and target yield
        
        Args:
            soil_data: Current soil nutrient levels
            target_yield: Target crop yield (ton/ha)
            crop: Crop type for specific requirements
            
        Returns:
            Fertilizer recommendations
        """
        # Simplified nutrient uptake per ton of yield (kg/ton)
        # These are general values, should be crop-specific in production
        nutrient_uptake = {
            'N': 20,   # kg N per ton yield
            'P2O5': 10, # kg P2O5 per ton yield
            'K2O': 25,  # kg K2O per ton yield
        }
        
        # Calculate nutrient requirements
        n_required = target_yield * nutrient_uptake['N']
        p_required = target_yield * nutrient_uptake['P2O5']
        k_required = target_yield * nutrient_uptake['K2O']
        
        # Subtract available nutrients (with efficiency factor)
        efficiency = 0.6  # 60% of soil nutrients available
        
        n_available = soil_data.get('N', 0) * efficiency
        p_available = soil_data.get('P', 0) * 2.29 * efficiency  # Convert P to P2O5
        k_available = soil_data.get('K', 0) * 1.2 * efficiency   # Convert K to K2O
        
        n_needed = max(0, n_required - n_available)
        p_needed = max(0, p_required - p_available)
        k_needed = max(0, k_required - k_available)
        
        return {
            'requirements': {
                'N': round(n_required, 1),
                'P2O5': round(p_required, 1),
                'K2O': round(k_required, 1)
            },
            'available': {
                'N': round(n_available, 1),
                'P2O5': round(p_available, 1),
                'K2O': round(k_available, 1)
            },
            'needed': {
                'N': round(n_needed, 1),
                'P2O5': round(p_needed, 1),
                'K2O': round(k_needed, 1)
            },
            'products': SoilFertilityService._recommend_products(n_needed, p_needed, k_needed)
        }
    
    @staticmethod
    def _recommend_products(n: float, p: float, k: float) -> List[Dict]:
        """Recommend specific fertilizer products"""
        products = []
        
        # Urea for N (46% N)
        if n > 0:
            urea_kg = n / 0.46
            products.append({
                'product': 'Urea',
                'formula': '46-0-0',
                'amount_kg': round(urea_kg, 1),
                'provides': f"{round(n, 1)} kg N"
            })
        
        # SP-36 for P (36% P2O5)
        if p > 0:
            sp36_kg = p / 0.36
            products.append({
                'product': 'SP-36',
                'formula': '0-36-0',
                'amount_kg': round(sp36_kg, 1),
                'provides': f"{round(p, 1)} kg P2O5"
            })
        
        # KCl for K (60% K2O)
        if k > 0:
            kcl_kg = k / 0.60
            products.append({
                'product': 'KCl',
                'formula': '0-0-60',
                'amount_kg': round(kcl_kg, 1),
                'provides': f"{round(k, 1)} kg K2O"
            })
        
        # NPK compound option
        if n > 0 and p > 0 and k > 0:
            # Use 15-15-15 as base
            limiting = min(n/15, p/15, k/15)
            npk_kg = limiting * 100
            
            products.append({
                'product': 'NPK 15-15-15 (Compound)',
                'formula': '15-15-15',
                'amount_kg': round(npk_kg, 1),
                'provides': f"{round(npk_kg*0.15, 1)} kg each of N-P2O5-K2O",
                'note': 'May need supplemental single nutrients'
            })
        
        return products
