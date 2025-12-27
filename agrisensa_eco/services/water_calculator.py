"""
Water Calculator Service
Calculate water footprint and irrigation needs based on FAO standards
"""

class WaterCalculator:
    """Calculate water footprint and irrigation requirements"""
    
    # FAO Crop Water Requirements (mm/season) for Indonesia
    CROP_WATER_REQUIREMENTS = {
        'Padi': {'total_mm': 1200, 'duration_days': 120},
        'Jagung': {'total_mm': 500, 'duration_days': 100},
        'Cabai Merah': {'total_mm': 600, 'duration_days': 120},
        'Cabai Rawit': {'total_mm': 550, 'duration_days': 100},
        'Tomat': {'total_mm': 400, 'duration_days': 90},
        'Terong': {'total_mm': 450, 'duration_days': 80},
        'Bawang Merah': {'total_mm': 350, 'duration_days': 70},
        'Kedelai': {'total_mm': 450, 'duration_days': 80},
        'Kacang Tanah': {'total_mm': 400, 'duration_days': 90}
    }
    
    def calculate_water_footprint(self, crop, area_ha, yield_kg):
        """Calculate water footprint (L/kg)"""
        
        req = self.CROP_WATER_REQUIREMENTS.get(crop, {'total_mm': 500, 'duration_days': 100})
        
        # Total water used (m³)
        total_water_m3 = (req['total_mm'] / 1000) * (area_ha * 10000)
        
        # Water footprint (L/kg)
        if yield_kg > 0:
            water_footprint = (total_water_m3 * 1000) / yield_kg
        else:
            water_footprint = 0
        
        return {
            'total_water_m3': round(total_water_m3, 2),
            'water_footprint_l_per_kg': round(water_footprint, 2),
            'crop': crop,
            'area_ha': area_ha,
            'yield_kg': yield_kg,
            'duration_days': req['duration_days']
        }
    
    def calculate_irrigation_need(self, crop, area_ha, rainfall_mm, soil_type='loam'):
        """Calculate irrigation water needed"""
        
        req = self.CROP_WATER_REQUIREMENTS.get(crop, {'total_mm': 500, 'duration_days': 100})
        
        # Effective rainfall (80% of total)
        effective_rainfall = rainfall_mm * 0.8
        
        # Irrigation deficit
        irrigation_deficit = max(0, req['total_mm'] - effective_rainfall)
        
        # Soil water holding capacity adjustment
        soil_factors = {
            'sandy': 0.9,  # Need more frequent irrigation
            'loam': 1.0,
            'clay': 1.1   # Can hold more water
        }
        
        factor = soil_factors.get(soil_type, 1.0)
        irrigation_need_mm = irrigation_deficit * factor
        
        # Convert to m³ for area
        irrigation_m3 = (irrigation_need_mm / 1000) * (area_ha * 10000)
        
        return {
            'irrigation_need_mm': round(irrigation_need_mm, 2),
            'irrigation_need_m3': round(irrigation_m3, 2),
            'rainfall_contribution_pct': round((effective_rainfall / req['total_mm']) * 100, 1) if req['total_mm'] > 0 else 0,
            'crop': crop,
            'area_ha': area_ha
        }
    
    def calculate_drip_irrigation_roi(self, area_ha, water_saved_pct=40, investment_per_ha=15000000):
        """Calculate ROI for drip irrigation investment"""
        
        # Assumptions
        water_cost_per_m3 = 500  # Rp/m³
        annual_water_use_m3 = 12000 * area_ha  # Average for vegetables
        
        # Savings
        water_saved_m3 = annual_water_use_m3 * (water_saved_pct / 100)
        annual_savings = water_saved_m3 * water_cost_per_m3
        
        # Yield increase (typically 15-25% with drip)
        yield_increase_pct = 20
        
        # Investment
        total_investment = investment_per_ha * area_ha
        
        # Payback period
        if annual_savings > 0:
            payback_years = total_investment / annual_savings
        else:
            payback_years = 999
        
        return {
            'investment': round(total_investment, 0),
            'annual_water_saved_m3': round(water_saved_m3, 2),
            'annual_cost_savings': round(annual_savings, 0),
            'yield_increase_pct': yield_increase_pct,
            'payback_years': round(payback_years, 1),
            'roi_5_years_pct': round(((annual_savings * 5) / total_investment - 1) * 100, 1) if total_investment > 0 else 0
        }
    
    def calculate_rainwater_harvesting(self, roof_area_m2, annual_rainfall_mm):
        """Calculate rainwater harvesting potential"""
        
        # Collection efficiency (typically 75-85%)
        efficiency = 0.8
        
        # Potential collection (m³/year)
        potential_m3 = (roof_area_m2 * annual_rainfall_mm / 1000) * efficiency
        
        # Recommended tank size (3 months storage)
        tank_size_m3 = potential_m3 / 4
        
        # Cost estimate (Rp 1.5 juta per m³ for tank)
        tank_cost = tank_size_m3 * 1500000
        
        return {
            'annual_collection_m3': round(potential_m3, 2),
            'recommended_tank_m3': round(tank_size_m3, 1),
            'estimated_cost': round(tank_cost, 0),
            'roof_area_m2': roof_area_m2,
            'annual_rainfall_mm': annual_rainfall_mm
        }
