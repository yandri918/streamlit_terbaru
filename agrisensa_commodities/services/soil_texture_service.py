# Soil Texture & Structure Service
# Based on USDA Soil Texture Classification and Saxton & Rawls equations

import numpy as np
from typing import Dict, Tuple, List

class SoilTextureService:
    """
    Comprehensive soil texture and structure analysis service
    Based on:
    - USDA Soil Texture Triangle
    - Saxton & Rawls (2006) - Water retention equations
    - USDA-NRCS - Bulk density standards
    """
    
    # USDA Texture Triangle boundaries (sand, silt, clay percentages)
    TEXTURE_CLASSES = {
        'Sand': {
            'description': 'Coarse, gritty texture. Drains quickly, low water holding capacity.',
            'sand_range': (85, 100),
            'management': 'Frequent irrigation, organic matter addition, mulching',
            'crops': 'Root crops, melons, peanuts',
            'color': '#F4A460'
        },
        'Loamy Sand': {
            'description': 'Slightly better water retention than sand, still coarse.',
            'sand_range': (70, 90),
            'management': 'Regular irrigation, cover crops, compost',
            'crops': 'Vegetables, potatoes, carrots',
            'color': '#DEB887'
        },
        'Sandy Loam': {
            'description': 'Good drainage, moderate water holding. Easy to work.',
            'sand_range': (50, 70),
            'management': 'Balanced fertilization, moderate irrigation',
            'crops': 'Most vegetables, corn, soybeans',
            'color': '#D2B48C'
        },
        'Loam': {
            'description': 'IDEAL! Balanced sand-silt-clay. Best for most crops.',
            'sand_range': (23, 52),
            'management': 'Maintain organic matter, standard practices',
            'crops': 'All crops thrive',
            'color': '#8B4513'
        },
        'Silt Loam': {
            'description': 'Smooth, silky texture. Good water and nutrient retention.',
            'sand_range': (0, 50),
            'management': 'Prevent crusting, avoid compaction',
            'crops': 'Grains, vegetables, fruits',
            'color': '#A0522D'
        },
        'Silt': {
            'description': 'Very smooth, holds water well. Can crust easily.',
            'sand_range': (0, 20),
            'management': 'Organic matter, avoid working when wet',
            'crops': 'Grains, pasture',
            'color': '#CD853F'
        },
        'Sandy Clay Loam': {
            'description': 'Moderate water holding, can be sticky when wet.',
            'sand_range': (45, 80),
            'management': 'Gypsum for structure, deep tillage',
            'crops': 'Cotton, sorghum, pasture',
            'color': '#BC8F8F'
        },
        'Clay Loam': {
            'description': 'Good nutrient retention, can be heavy and sticky.',
            'sand_range': (20, 45),
            'management': 'Avoid compaction, drainage improvement',
            'crops': 'Rice, wheat, pasture',
            'color': '#A0522D'
        },
        'Silty Clay Loam': {
            'description': 'High water and nutrient holding. Slow drainage.',
            'sand_range': (0, 20),
            'management': 'Drainage tiles, raised beds',
            'crops': 'Rice, pasture, trees',
            'color': '#8B7355'
        },
        'Sandy Clay': {
            'description': 'Heavy when wet, hard when dry. Difficult to work.',
            'sand_range': (45, 65),
            'management': 'Organic matter, gypsum, deep rooted cover crops',
            'crops': 'Pasture, drought-tolerant crops',
            'color': '#A0826D'
        },
        'Silty Clay': {
            'description': 'Very fine texture, high water holding, poor drainage.',
            'sand_range': (0, 20),
            'management': 'Drainage systems, raised beds, organic matter',
            'crops': 'Rice, wetland crops',
            'color': '#8B7D6B'
        },
        'Clay': {
            'description': 'Very fine, sticky when wet, hard when dry. Excellent nutrients.',
            'sand_range': (0, 45),
            'management': 'Gypsum, organic matter, avoid working when wet',
            'crops': 'Rice, sugarcane, pasture',
            'color': '#654321'
        }
    }
    
    @staticmethod
    def classify_texture(sand: float, silt: float, clay: float) -> Dict:
        """
        Classify soil texture using USDA triangle
        
        Args:
            sand: Sand percentage (0-100)
            silt: Silt percentage (0-100)
            clay: Clay percentage (0-100)
            
        Returns:
            Texture classification and properties
        """
        # Validate inputs
        total = sand + silt + clay
        if not (99 <= total <= 101):
            return {'error': f'Percentages must sum to 100 (current: {total:.1f})'}
        
        # Normalize to exactly 100
        factor = 100 / total
        sand *= factor
        silt *= factor
        clay *= factor
        
        # USDA Classification logic
        texture_class = SoilTextureService._determine_texture_class(sand, silt, clay)
        
        return {
            'class': texture_class,
            'sand': round(sand, 1),
            'silt': round(silt, 1),
            'clay': round(clay, 1),
            'properties': SoilTextureService.TEXTURE_CLASSES.get(texture_class, {}),
            'coordinates': {
                'sand': sand,
                'silt': silt,
                'clay': clay
            }
        }
    
    @staticmethod
    def _determine_texture_class(sand: float, silt: float, clay: float) -> str:
        """Determine USDA texture class based on percentages"""
        
        # Clay (>40% clay)
        if clay >= 40:
            if sand >= 45:
                return 'Sandy Clay'
            elif silt >= 40:
                return 'Silty Clay'
            else:
                return 'Clay'
        
        # Clay Loam (27-40% clay)
        elif clay >= 27:
            if sand >= 20 and sand <= 45:
                return 'Clay Loam'
            elif sand > 45:
                return 'Sandy Clay Loam'
            else:
                return 'Silty Clay Loam'
        
        # Loam (7-27% clay)
        elif clay >= 7:
            if sand >= 52:
                return 'Sandy Loam'
            elif silt >= 50 or (silt >= 28 and clay < 20):
                return 'Silt Loam'
            else:
                return 'Loam'
        
        # Sandy textures (<7% clay)
        else:
            if silt >= 50:
                return 'Silt'
            elif sand >= 85:
                return 'Sand'
            else:
                return 'Loamy Sand'
    
    @staticmethod
    def calculate_bulk_density_properties(bulk_density: float, particle_density: float = 2.65) -> Dict:
        """
        Calculate soil porosity and related properties
        
        Args:
            bulk_density: Soil bulk density (g/cm³)
            particle_density: Particle density (g/cm³), default 2.65 for mineral soils
            
        Returns:
            Porosity, air-filled porosity, and compaction status
        """
        # Calculate total porosity
        total_porosity = (1 - (bulk_density / particle_density)) * 100
        
        # Classify compaction status
        if bulk_density < 1.0:
            compaction = 'Very Loose (Organic-rich)'
            status = 'excellent'
        elif bulk_density < 1.3:
            compaction = 'Loose (Good structure)'
            status = 'good'
        elif bulk_density < 1.6:
            compaction = 'Moderate (Acceptable)'
            status = 'moderate'
        elif bulk_density < 1.8:
            compaction = 'Compact (Restricted root growth)'
            status = 'poor'
        else:
            compaction = 'Very Compact (Severe restriction)'
            status = 'critical'
        
        # Ideal bulk density ranges by texture
        ideal_ranges = {
            'Sandy': (1.4, 1.6),
            'Loamy': (1.1, 1.4),
            'Clayey': (1.0, 1.3)
        }
        
        return {
            'bulk_density': round(bulk_density, 2),
            'total_porosity': round(total_porosity, 1),
            'compaction_status': compaction,
            'status_level': status,
            'ideal_bd_range': ideal_ranges,
            'interpretation': SoilTextureService._interpret_bulk_density(bulk_density, total_porosity)
        }
    
    @staticmethod
    def _interpret_bulk_density(bd: float, porosity: float) -> str:
        """Provide interpretation of bulk density"""
        if bd < 1.3:
            return f"Excellent soil structure with {porosity:.1f}% porosity. Good for root growth and water infiltration."
        elif bd < 1.6:
            return f"Acceptable structure with {porosity:.1f}% porosity. Monitor for compaction in high-traffic areas."
        elif bd < 1.8:
            return f"Compacted soil with only {porosity:.1f}% porosity. Root growth may be restricted. Consider deep tillage or subsoiling."
        else:
            return f"Severely compacted with only {porosity:.1f}% porosity. Immediate remediation needed. Use deep ripping and organic matter."
    
    @staticmethod
    def calculate_water_holding_capacity(sand: float, clay: float, organic_matter: float = 2.0) -> Dict:
        """
        Calculate water holding capacity using Saxton & Rawls (2006) equations
        
        Args:
            sand: Sand percentage
            silt: Silt percentage  
            clay: Clay percentage
            organic_matter: Organic matter percentage (default 2%)
            
        Returns:
            Field capacity, wilting point, available water capacity
        """
        # Convert to fractions
        sand_frac = sand / 100
        clay_frac = clay / 100
        om_frac = organic_matter / 100
        
        # Saxton & Rawls equations for water retention
        # Field Capacity (FC) at -33 kPa
        theta_33 = (-0.251 * sand_frac) + (0.195 * clay_frac) + (0.011 * om_frac) + \
                   (0.006 * sand_frac * om_frac) - (0.027 * clay_frac * om_frac) + \
                   (0.452 * sand_frac * clay_frac) + 0.299
        
        # Wilting Point (WP) at -1500 kPa
        theta_1500 = (-0.024 * sand_frac) + (0.487 * clay_frac) + (0.006 * om_frac) + \
                     (0.005 * sand_frac * om_frac) - (0.013 * clay_frac * om_frac) + \
                     (0.068 * sand_frac * clay_frac) + 0.031
        
        # Available Water Capacity (AWC)
        awc = theta_33 - theta_1500
        
        # Convert to mm/m (multiply by 1000)
        fc_mm = theta_33 * 1000
        wp_mm = theta_1500 * 1000
        awc_mm = awc * 1000
        
        # Classify AWC
        if awc_mm < 100:
            awc_class = 'Low (Frequent irrigation needed)'
        elif awc_mm < 150:
            awc_class = 'Moderate (Regular irrigation)'
        elif awc_mm < 200:
            awc_class = 'Good (Moderate irrigation)'
        else:
            awc_class = 'High (Infrequent irrigation)'
        
        return {
            'field_capacity': round(fc_mm, 1),
            'wilting_point': round(wp_mm, 1),
            'available_water_capacity': round(awc_mm, 1),
            'awc_classification': awc_class,
            'interpretation': f"This soil can hold {awc_mm:.0f} mm of plant-available water per meter of soil depth. {awc_class}."
        }
    
    @staticmethod
    def estimate_infiltration_rate(texture_class: str, structure: str = 'moderate') -> Dict:
        """
        Estimate infiltration rate based on texture and structure
        
        Args:
            texture_class: USDA texture class
            structure: Soil structure (poor, moderate, good)
            
        Returns:
            Infiltration rate and classification
        """
        # Base infiltration rates (mm/hr) by texture
        base_rates = {
            'Sand': 50,
            'Loamy Sand': 25,
            'Sandy Loam': 13,
            'Loam': 8,
            'Silt Loam': 6.5,
            'Silt': 5,
            'Sandy Clay Loam': 4,
            'Clay Loam': 2.5,
            'Silty Clay Loam': 1.5,
            'Sandy Clay': 1.2,
            'Silty Clay': 1.0,
            'Clay': 0.5
        }
        
        base_rate = base_rates.get(texture_class, 5)
        
        # Adjust for structure
        structure_multipliers = {
            'poor': 0.5,
            'moderate': 1.0,
            'good': 1.5
        }
        
        multiplier = structure_multipliers.get(structure.lower(), 1.0)
        infiltration_rate = base_rate * multiplier
        
        # Classify infiltration
        if infiltration_rate < 1:
            classification = 'Very Slow (Drainage problems likely)'
            risk = 'High runoff and erosion risk'
        elif infiltration_rate < 5:
            classification = 'Slow (Moderate drainage)'
            risk = 'Moderate runoff risk'
        elif infiltration_rate < 15:
            classification = 'Moderate (Good drainage)'
            risk = 'Low runoff risk'
        elif infiltration_rate < 50:
            classification = 'Rapid (Excellent drainage)'
            risk = 'Low runoff, may need frequent irrigation'
        else:
            classification = 'Very Rapid (Excessive drainage)'
            risk = 'Very low runoff, frequent irrigation needed'
        
        return {
            'infiltration_rate': round(infiltration_rate, 2),
            'classification': classification,
            'runoff_risk': risk,
            'recommendations': SoilTextureService._get_infiltration_recommendations(infiltration_rate)
        }
    
    @staticmethod
    def _get_infiltration_recommendations(rate: float) -> List[str]:
        """Get management recommendations based on infiltration rate"""
        if rate < 1:
            return [
                "Install drainage tiles or ditches",
                "Use raised beds",
                "Add organic matter to improve structure",
                "Avoid compaction",
                "Consider gypsum application for clay soils"
            ]
        elif rate < 5:
            return [
                "Maintain organic matter levels",
                "Avoid working soil when wet",
                "Use cover crops",
                "Monitor for waterlogging"
            ]
        elif rate < 15:
            return [
                "Maintain current practices",
                "Regular organic matter additions",
                "Standard irrigation scheduling"
            ]
        else:
            return [
                "Frequent irrigation may be needed",
                "Use mulch to reduce evaporation",
                "Add organic matter to improve water retention",
                "Consider drip irrigation"
            ]
    
    @staticmethod
    def get_texture_triangle_coordinates() -> Dict:
        """
        Get coordinates for USDA texture triangle boundaries
        Returns coordinates for plotting the triangle
        """
        # Define texture class boundaries for plotting
        # This is a simplified version - full implementation would have all boundaries
        boundaries = {
            'Clay': [(0, 0, 100), (0, 40, 60), (45, 0, 55), (0, 0, 100)],
            'Sandy Clay': [(45, 0, 55), (65, 0, 35), (45, 35, 20), (45, 0, 55)],
            'Silty Clay': [(0, 40, 60), (0, 60, 40), (20, 40, 40), (0, 40, 60)],
            'Clay Loam': [(20, 20, 60), (45, 20, 35), (45, 35, 20), (20, 40, 40), (20, 20, 60)],
            'Sandy Clay Loam': [(45, 20, 35), (65, 20, 15), (80, 0, 20), (45, 35, 20), (45, 20, 35)],
            'Silty Clay Loam': [(0, 40, 60), (20, 40, 40), (20, 60, 20), (0, 60, 40), (0, 40, 60)],
            'Loam': [(23, 28, 49), (52, 28, 20), (52, 41, 7), (23, 50, 27), (23, 28, 49)],
            'Sandy Loam': [(52, 28, 20), (70, 15, 15), (85, 0, 15), (52, 41, 7), (52, 28, 20)],
            'Silt Loam': [(0, 50, 50), (23, 50, 27), (50, 50, 0), (0, 88, 12), (0, 50, 50)],
            'Sand': [(85, 0, 15), (100, 0, 0), (90, 10, 0), (85, 0, 15)],
            'Loamy Sand': [(70, 15, 15), (85, 0, 15), (90, 10, 0), (85, 15, 0), (70, 15, 15)],
            'Silt': [(0, 88, 12), (0, 100, 0), (20, 80, 0), (0, 88, 12)]
        }
        
        return boundaries
