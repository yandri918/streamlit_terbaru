"""
Climate Adaptation Calculator
Climate risk assessment and adaptation strategies
"""

class ClimateAdaptationCalculator:
    """Calculate climate risks and recommend adaptation strategies"""
    
    # Climate risk factors by region type
    CLIMATE_RISKS = {
        'coastal': {
            'flood': 'high', 'drought': 'low', 'heat_stress': 'medium',
            'sea_level_rise': 'high', 'salinity': 'high'
        },
        'lowland': {
            'flood': 'high', 'drought': 'medium', 'heat_stress': 'high',
            'sea_level_rise': 'low', 'salinity': 'low'
        },
        'highland': {
            'flood': 'low', 'drought': 'low', 'heat_stress': 'low',
            'sea_level_rise': 'low', 'salinity': 'low', 'frost': 'medium'
        },
        'dryland': {
            'flood': 'low', 'drought': 'very_high', 'heat_stress': 'very_high',
            'sea_level_rise': 'low', 'salinity': 'medium'
        }
    }
    
    # Climate-smart crop varieties
    CLIMATE_SMART_CROPS = {
        'drought_tolerant': {
            'Sorghum': {'water_need': 'low', 'heat_tolerance': 'high', 'yield_potential': 'medium'},
            'Millet': {'water_need': 'very_low', 'heat_tolerance': 'very_high', 'yield_potential': 'medium'},
            'Cassava': {'water_need': 'low', 'heat_tolerance': 'high', 'yield_potential': 'high'},
            'Kacang Tunggak': {'water_need': 'low', 'heat_tolerance': 'high', 'yield_potential': 'medium'}
        },
        'flood_tolerant': {
            'Padi Rawa': {'water_tolerance': 'very_high', 'submersion_days': 14, 'yield_potential': 'medium'},
            'Kangkung': {'water_tolerance': 'high', 'submersion_days': 30, 'yield_potential': 'high'}
        },
        'heat_tolerant': {
            'Okra': {'optimal_temp': '25-35°C', 'heat_tolerance': 'very_high', 'yield_potential': 'high'},
            'Terong': {'optimal_temp': '24-32°C', 'heat_tolerance': 'high', 'yield_potential': 'high'},
            'Cowpea': {'optimal_temp': '25-35°C', 'heat_tolerance': 'very_high', 'yield_potential': 'medium'}
        }
    }
    
    def assess_climate_risk(self, region_type, rainfall_annual_mm, temp_avg_c, elevation_m):
        """Assess climate risks for a location"""
        
        # Get base risks for region type
        base_risks = self.CLIMATE_RISKS.get(region_type, self.CLIMATE_RISKS['lowland'])
        
        # Adjust based on actual conditions
        adjusted_risks = base_risks.copy()
        
        # Drought risk adjustment
        if rainfall_annual_mm < 1000:
            adjusted_risks['drought'] = self._increase_risk_level(adjusted_risks.get('drought', 'medium'))
        elif rainfall_annual_mm > 3000:
            adjusted_risks['flood'] = self._increase_risk_level(adjusted_risks.get('flood', 'medium'))
        
        # Heat stress adjustment
        if temp_avg_c > 28:
            adjusted_risks['heat_stress'] = self._increase_risk_level(adjusted_risks.get('heat_stress', 'medium'))
        
        # Calculate overall risk score
        risk_scores = {
            'very_low': 1, 'low': 2, 'medium': 3, 'high': 4, 'very_high': 5
        }
        
        total_score = sum(risk_scores.get(risk, 3) for risk in adjusted_risks.values())
        max_score = len(adjusted_risks) * 5
        overall_risk_pct = (total_score / max_score) * 100
        
        return {
            'overall_risk_pct': round(overall_risk_pct, 1),
            'risk_level': self._get_risk_level(overall_risk_pct),
            'individual_risks': adjusted_risks,
            'primary_threats': self._get_primary_threats(adjusted_risks),
            'adaptation_strategies': self._get_adaptation_strategies(adjusted_risks)
        }
    
    def _increase_risk_level(self, current_level):
        """Increase risk level by one step"""
        levels = ['very_low', 'low', 'medium', 'high', 'very_high']
        try:
            current_index = levels.index(current_level)
            return levels[min(current_index + 1, len(levels) - 1)]
        except ValueError:
            return 'medium'
    
    def _get_risk_level(self, risk_pct):
        """Convert percentage to risk level"""
        if risk_pct >= 80:
            return 'Very High'
        elif risk_pct >= 60:
            return 'High'
        elif risk_pct >= 40:
            return 'Medium'
        elif risk_pct >= 20:
            return 'Low'
        else:
            return 'Very Low'
    
    def _get_primary_threats(self, risks):
        """Identify top 3 threats"""
        risk_scores = {'very_high': 5, 'high': 4, 'medium': 3, 'low': 2, 'very_low': 1}
        sorted_risks = sorted(risks.items(), key=lambda x: risk_scores.get(x[1], 0), reverse=True)
        return [risk[0] for risk in sorted_risks[:3]]
    
    def _get_adaptation_strategies(self, risks):
        """Recommend adaptation strategies based on risks"""
        strategies = []
        
        if risks.get('drought', 'low') in ['high', 'very_high']:
            strategies.extend([
                "Tanam varietas tahan kering (Sorghum, Millet)",
                "Implementasi irigasi tetes",
                "Mulching untuk konservasi air",
                "Rainwater harvesting"
            ])
        
        if risks.get('flood', 'low') in ['high', 'very_high']:
            strategies.extend([
                "Tanam padi rawa atau varietas tahan banjir",
                "Buat raised beds (bedengan tinggi)",
                "Drainage system yang baik",
                "Diversifikasi dengan akuakultur"
            ])
        
        if risks.get('heat_stress', 'low') in ['high', 'very_high']:
            strategies.extend([
                "Tanam varietas tahan panas (Okra, Terong)",
                "Agroforestri untuk naungan",
                "Irigasi pada pagi/sore hari",
                "Mulching untuk mengurangi suhu tanah"
            ])
        
        return strategies[:5]  # Return top 5
    
    def recommend_climate_smart_crop(self, primary_risk):
        """Recommend crops based on primary climate risk"""
        
        if 'drought' in primary_risk.lower():
            return self.CLIMATE_SMART_CROPS['drought_tolerant']
        elif 'flood' in primary_risk.lower():
            return self.CLIMATE_SMART_CROPS['flood_tolerant']
        elif 'heat' in primary_risk.lower():
            return self.CLIMATE_SMART_CROPS['heat_tolerant']
        else:
            # Return drought-tolerant as default (most common issue)
            return self.CLIMATE_SMART_CROPS['drought_tolerant']
    
    def calculate_insurance_premium(self, crop_value, risk_level):
        """Calculate estimated insurance premium"""
        
        # Base premium rates (% of crop value)
        premium_rates = {
            'Very Low': 0.02,  # 2%
            'Low': 0.03,       # 3%
            'Medium': 0.05,    # 5%
            'High': 0.08,      # 8%
            'Very High': 0.12  # 12%
        }
        
        rate = premium_rates.get(risk_level, 0.05)
        premium = crop_value * rate
        
        return {
            'premium': round(premium, 0),
            'rate_pct': rate * 100,
            'crop_value': crop_value,
            'risk_level': risk_level
        }
