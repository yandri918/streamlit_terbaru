"""
Carbon Calculator Service
Calculate carbon sequestration potential for various agricultural practices
"""

class CarbonCalculator:
    """Calculate carbon sequestration based on IPCC Tier 1 coefficients"""
    
    # IPCC Tier 1 coefficients (simplified for Indonesia)
    CARBON_COEFFICIENTS = {
        'agroforestry': {
            'biomass_ton_per_tree_per_year': 0.05,
            'carbon_fraction': 0.47,
            'co2_conversion': 3.67  # CO2 = C * 3.67
        },
        'no_till': {
            'soil_carbon_increase_ton_per_ha_per_year': 0.3
        },
        'biochar': {
            'biochar_ton_per_ha_per_year': 2,
            'carbon_content': 0.7,
            'stability_factor': 0.9  # 90% stable for 100+ years
        },
        'cover_crop': {
            'biomass_ton_per_ha_per_year': 3,
            'carbon_fraction': 0.4
        }
    }
    
    def calculate_agroforestry_carbon(self, area_ha, tree_density, years):
        """Calculate carbon from agroforestry"""
        coef = self.CARBON_COEFFICIENTS['agroforestry']
        
        # Biomass accumulation
        biomass_per_ha = tree_density * coef['biomass_ton_per_tree_per_year'] * years
        
        # Carbon content
        carbon_ton = biomass_per_ha * coef['carbon_fraction']
        
        # CO2 equivalent
        co2_ton = carbon_ton * coef['co2_conversion']
        
        # Total for area
        total_co2 = co2_ton * area_ha
        
        return {
            'total_co2_ton': round(total_co2, 2),
            'annual_co2_ton': round(total_co2 / years, 2),
            'area_ha': area_ha,
            'years': years,
            'tree_equivalent': round(total_co2 / 0.2, 0),  # 1 tree = ~0.2 ton CO2/year
            'car_km_equivalent': round(total_co2 / 0.12 * 1000, 0)  # 1 km = ~0.12 kg CO2
        }
    
    def calculate_no_till_carbon(self, area_ha, years):
        """Calculate carbon from no-till farming"""
        coef = self.CARBON_COEFFICIENTS['no_till']
        
        annual_sequestration = coef['soil_carbon_increase_ton_per_ha_per_year']
        total_co2 = annual_sequestration * area_ha * years * 3.67
        
        return {
            'total_co2_ton': round(total_co2, 2),
            'annual_co2_ton': round(total_co2 / years, 2),
            'area_ha': area_ha,
            'years': years
        }
    
    def calculate_biochar_carbon(self, area_ha, years):
        """Calculate carbon from biochar application"""
        coef = self.CARBON_COEFFICIENTS['biochar']
        
        biochar_annual = coef['biochar_ton_per_ha_per_year']
        carbon_content = biochar_annual * coef['carbon_content']
        stable_carbon = carbon_content * coef['stability_factor']
        co2_annual = stable_carbon * 3.67
        
        total_co2 = co2_annual * area_ha * years
        
        return {
            'total_co2_ton': round(total_co2, 2),
            'annual_co2_ton': round(co2_annual * area_ha, 2),
            'area_ha': area_ha,
            'years': years
        }
    
    def calculate_cover_crop_carbon(self, area_ha, years):
        """Calculate carbon from cover crop"""
        coef = self.CARBON_COEFFICIENTS['cover_crop']
        
        biomass_annual = coef['biomass_ton_per_ha_per_year']
        carbon_annual = biomass_annual * coef['carbon_fraction']
        co2_annual = carbon_annual * 3.67
        
        total_co2 = co2_annual * area_ha * years
        
        return {
            'total_co2_ton': round(total_co2, 2),
            'annual_co2_ton': round(co2_annual * area_ha, 2),
            'area_ha': area_ha,
            'years': years
        }
    
    def estimate_value(self, co2_ton, price_per_ton=100000):
        """Estimate economic value of carbon credits"""
        return {
            'co2_ton': co2_ton,
            'price_per_ton': price_per_ton,
            'total_value': round(co2_ton * price_per_ton, 0),
            'annual_value': round(co2_ton * price_per_ton, 0)  # Will be divided by years in caller
        }
