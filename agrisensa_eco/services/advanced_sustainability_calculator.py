"""
Advanced Sustainability Calculator
Ecosystem services valuation, precision conservation, and ESG metrics
"""

class AdvancedSustainabilityCalculator:
    """Calculate ecosystem services value and ESG metrics"""
    
    # Ecosystem services valuation (Rp/ha/year)
    ECOSYSTEM_SERVICES_VALUES = {
        'carbon_sequestration': {
            'forest': 5000000,  # Rp 5 juta/ha/year
            'agroforestry': 3000000,
            'cropland': 500000,
            'grassland': 1000000
        },
        'water_regulation': {
            'forest': 3000000,
            'agroforestry': 2000000,
            'wetland': 4000000,
            'cropland': 500000
        },
        'soil_conservation': {
            'forest': 2000000,
            'agroforestry': 1500000,
            'terraced_cropland': 1000000,
            'cropland': 300000
        },
        'pollination': {
            'diverse_agroforestry': 2000000,
            'organic_farm': 1500000,
            'conventional_farm': 500000
        },
        'biodiversity_habitat': {
            'forest': 4000000,
            'agroforestry': 2500000,
            'organic_farm': 1000000,
            'conventional_farm': 300000
        }
    }
    
    def calculate_ecosystem_services_value(self, land_type, area_ha, services_selected):
        """Calculate total ecosystem services value"""
        
        total_value = 0
        breakdown = {}
        
        for service in services_selected:
            if service in self.ECOSYSTEM_SERVICES_VALUES:
                service_values = self.ECOSYSTEM_SERVICES_VALUES[service]
                value_per_ha = service_values.get(land_type, 0)
                total_service_value = value_per_ha * area_ha
                
                breakdown[service] = {
                    'value_per_ha': value_per_ha,
                    'total_value': total_service_value
                }
                total_value += total_service_value
        
        return {
            'total_annual_value': total_value,
            'value_per_ha': total_value / area_ha if area_ha > 0 else 0,
            'breakdown': breakdown,
            'area_ha': area_ha,
            'land_type': land_type
        }
    
    def calculate_precision_conservation_savings(self, area_ha, current_application_rate, 
                                                 optimal_application_rate, input_price):
        """Calculate savings from variable rate application"""
        
        # Current total input
        current_total = area_ha * current_application_rate
        
        # Optimal total (assuming 20% variation across field)
        # Some areas need more, some less, average is optimal rate
        optimal_total = area_ha * optimal_application_rate
        
        # Savings
        input_saved = current_total - optimal_total
        cost_saved = input_saved * input_price
        
        # Yield improvement (better targeted application)
        yield_improvement_pct = 5  # Conservative estimate
        
        return {
            'current_total_kg': current_total,
            'optimal_total_kg': optimal_total,
            'input_saved_kg': input_saved,
            'cost_saved': cost_saved,
            'savings_pct': (input_saved / current_total * 100) if current_total > 0 else 0,
            'yield_improvement_pct': yield_improvement_pct
        }
    
    def calculate_esg_score(self, environmental_metrics, social_metrics, governance_metrics):
        """Calculate overall ESG score (0-100)"""
        
        # Environmental score (40% weight)
        env_score = (
            environmental_metrics.get('carbon_footprint_reduction', 0) * 0.3 +
            environmental_metrics.get('water_efficiency', 0) * 0.25 +
            environmental_metrics.get('biodiversity_index', 0) * 0.25 +
            environmental_metrics.get('waste_reduction', 0) * 0.2
        )
        
        # Social score (30% weight)
        soc_score = (
            social_metrics.get('fair_labor', 0) * 0.4 +
            social_metrics.get('community_engagement', 0) * 0.3 +
            social_metrics.get('food_security', 0) * 0.3
        )
        
        # Governance score (30% weight)
        gov_score = (
            governance_metrics.get('certification_compliance', 0) * 0.4 +
            governance_metrics.get('traceability', 0) * 0.3 +
            governance_metrics.get('transparency', 0) * 0.3
        )
        
        # Overall ESG score
        overall_score = (env_score * 0.4) + (soc_score * 0.3) + (gov_score * 0.3)
        
        return {
            'overall_score': round(overall_score, 1),
            'environmental_score': round(env_score, 1),
            'social_score': round(soc_score, 1),
            'governance_score': round(gov_score, 1),
            'rating': self._get_esg_rating(overall_score)
        }
    
    def _get_esg_rating(self, score):
        """Convert ESG score to rating"""
        if score >= 85:
            return 'AAA (Excellent)'
        elif score >= 75:
            return 'AA (Very Good)'
        elif score >= 65:
            return 'A (Good)'
        elif score >= 55:
            return 'BBB (Fair)'
        elif score >= 45:
            return 'BB (Below Average)'
        else:
            return 'B (Poor)'
    
    # Indigenous knowledge database
    INDIGENOUS_PRACTICES = {
        'Pranata Mangsa (Jawa)': {
            'description': 'Sistem kalender pertanian tradisional Jawa berdasarkan posisi bintang',
            'application': 'Penentuan waktu tanam dan panen',
            'relevance': 'Masih relevan untuk prediksi musim',
            'region': 'Jawa Tengah, Jawa Timur'
        },
        'Subak (Bali)': {
            'description': 'Sistem irigasi tradisional berbasis komunitas',
            'application': 'Manajemen air sawah secara kolektif',
            'relevance': 'Model untuk water governance',
            'region': 'Bali'
        },
        'Huma (Sunda)': {
            'description': 'Sistem ladang berpindah berkelanjutan',
            'application': 'Rotasi lahan untuk regenerasi tanah',
            'relevance': 'Prinsip regenerative agriculture',
            'region': 'Jawa Barat'
        },
        'Sasi (Maluku)': {
            'description': 'Larangan adat untuk konservasi sumber daya',
            'application': 'Perlindungan musiman untuk regenerasi',
            'relevance': 'Community-based conservation',
            'region': 'Maluku'
        },
        'Mina Padi': {
            'description': 'Integrasi ikan dan padi dalam satu lahan',
            'application': 'Diversifikasi pendapatan, kontrol hama alami',
            'relevance': 'Integrated farming system',
            'region': 'Seluruh Indonesia'
        }
    }
