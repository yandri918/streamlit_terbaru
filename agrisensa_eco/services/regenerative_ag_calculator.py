"""
Regenerative Agriculture Calculator
Soil health assessment and regenerative practice recommendations
"""

class RegenerativeAgCalculator:
    """Calculate soil health scores and regenerative agriculture metrics"""
    
    # Soil health scoring thresholds
    SOIL_HEALTH_THRESHOLDS = {
        'c_organic': {'poor': 1.0, 'fair': 2.0, 'good': 3.0, 'excellent': 4.0},  # %
        'ph': {'acidic': 5.5, 'slightly_acidic': 6.0, 'neutral': 7.0, 'alkaline': 7.5},
        'n_total': {'poor': 0.1, 'fair': 0.15, 'good': 0.2, 'excellent': 0.3},  # %
        'p_available': {'poor': 10, 'fair': 20, 'good': 30, 'excellent': 50},  # ppm
        'k_available': {'poor': 100, 'fair': 150, 'good': 200, 'excellent': 300}  # ppm
    }
    
    # Cover crop database
    COVER_CROPS = {
        'Legume': {
            'Kacang Hijau': {'season': 'Kemarau', 'benefit': 'Fiksasi N, Biomassa tinggi', 'duration': 60},
            'Kacang Tunggak': {'season': 'Sepanjang tahun', 'benefit': 'Tahan kering, Fiksasi N', 'duration': 70},
            'Kedelai Edamame': {'season': 'Hujan', 'benefit': 'Fiksasi N, Pakan ternak', 'duration': 80}
        },
        'Grass': {
            'Sorghum': {'season': 'Kemarau', 'benefit': 'Biomassa tinggi, Tahan kering', 'duration': 90},
            'Oat': {'season': 'Hujan', 'benefit': 'Cepat tumbuh, Pakan ternak', 'duration': 60},
            'Rye': {'season': 'Hujan', 'benefit': 'Tekan gulma, Biomassa tinggi', 'duration': 70}
        },
        'Brassica': {
            'Mustard': {'season': 'Sepanjang tahun', 'benefit': 'Biofumigasi, Cepat tumbuh', 'duration': 50},
            'Radish': {'season': 'Sepanjang tahun', 'benefit': 'Penetrasi tanah, Biomassa', 'duration': 60}
        }
    }
    
    def calculate_soil_health_score(self, c_organic, ph, n_total, p_available, k_available):
        """Calculate overall soil health score (0-100)"""
        
        scores = {}
        
        # C-Organic score
        if c_organic >= self.SOIL_HEALTH_THRESHOLDS['c_organic']['excellent']:
            scores['c_organic'] = 100
        elif c_organic >= self.SOIL_HEALTH_THRESHOLDS['c_organic']['good']:
            scores['c_organic'] = 80
        elif c_organic >= self.SOIL_HEALTH_THRESHOLDS['c_organic']['fair']:
            scores['c_organic'] = 60
        else:
            scores['c_organic'] = 40
        
        # pH score (optimal range: 6.0-7.0)
        if 6.0 <= ph <= 7.0:
            scores['ph'] = 100
        elif 5.5 <= ph < 6.0 or 7.0 < ph <= 7.5:
            scores['ph'] = 80
        elif 5.0 <= ph < 5.5 or 7.5 < ph <= 8.0:
            scores['ph'] = 60
        else:
            scores['ph'] = 40
        
        # N-Total score
        if n_total >= self.SOIL_HEALTH_THRESHOLDS['n_total']['excellent']:
            scores['n_total'] = 100
        elif n_total >= self.SOIL_HEALTH_THRESHOLDS['n_total']['good']:
            scores['n_total'] = 80
        elif n_total >= self.SOIL_HEALTH_THRESHOLDS['n_total']['fair']:
            scores['n_total'] = 60
        else:
            scores['n_total'] = 40
        
        # P-Available score
        if p_available >= self.SOIL_HEALTH_THRESHOLDS['p_available']['excellent']:
            scores['p_available'] = 100
        elif p_available >= self.SOIL_HEALTH_THRESHOLDS['p_available']['good']:
            scores['p_available'] = 80
        elif p_available >= self.SOIL_HEALTH_THRESHOLDS['p_available']['fair']:
            scores['p_available'] = 60
        else:
            scores['p_available'] = 40
        
        # K-Available score
        if k_available >= self.SOIL_HEALTH_THRESHOLDS['k_available']['excellent']:
            scores['k_available'] = 100
        elif k_available >= self.SOIL_HEALTH_THRESHOLDS['k_available']['good']:
            scores['k_available'] = 80
        elif k_available >= self.SOIL_HEALTH_THRESHOLDS['k_available']['fair']:
            scores['k_available'] = 60
        else:
            scores['k_available'] = 40
        
        # Overall score (weighted average)
        overall_score = (
            scores['c_organic'] * 0.3 +  # C-organic most important
            scores['ph'] * 0.2 +
            scores['n_total'] * 0.2 +
            scores['p_available'] * 0.15 +
            scores['k_available'] * 0.15
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'individual_scores': scores,
            'rating': self._get_rating(overall_score),
            'recommendations': self._get_recommendations(scores, c_organic, ph)
        }
    
    def _get_rating(self, score):
        """Get rating based on score"""
        if score >= 85:
            return 'Excellent'
        elif score >= 70:
            return 'Good'
        elif score >= 55:
            return 'Fair'
        else:
            return 'Poor'
    
    def _get_recommendations(self, scores, c_organic, ph):
        """Generate recommendations based on scores"""
        recs = []
        
        if scores['c_organic'] < 70:
            recs.append("Tambahkan kompos 5-10 ton/ha untuk meningkatkan C-organik")
            recs.append("Tanam cover crop untuk menambah biomassa")
        
        if ph < 5.5:
            recs.append(f"Tanah terlalu asam (pH {ph:.1f}). Aplikasi kapur 1-2 ton/ha")
        elif ph > 7.5:
            recs.append(f"Tanah terlalu alkali (pH {ph:.1f}). Aplikasi sulfur atau bahan organik")
        
        if scores['n_total'] < 70:
            recs.append("Tanam legume cover crop untuk fiksasi nitrogen")
        
        if scores['p_available'] < 70:
            recs.append("Aplikasi pupuk P (SP-36) atau rock phosphate")
        
        if scores['k_available'] < 70:
            recs.append("Aplikasi pupuk K (KCl) atau abu kayu")
        
        return recs
    
    def recommend_cover_crop(self, season, primary_goal):
        """Recommend cover crop based on season and goal"""
        
        recommendations = []
        
        for category, crops in self.COVER_CROPS.items():
            for crop_name, crop_info in crops.items():
                if season in crop_info['season'] or crop_info['season'] == 'Sepanjang tahun':
                    if primary_goal.lower() in crop_info['benefit'].lower():
                        recommendations.append({
                            'name': crop_name,
                            'category': category,
                            'season': crop_info['season'],
                            'benefit': crop_info['benefit'],
                            'duration': crop_info['duration']
                        })
        
        return recommendations if recommendations else self._get_default_recommendations(season)
    
    def _get_default_recommendations(self, season):
        """Get default recommendations if no specific match"""
        defaults = []
        for category, crops in self.COVER_CROPS.items():
            for crop_name, crop_info in crops.items():
                if season in crop_info['season'] or crop_info['season'] == 'Sepanjang tahun':
                    defaults.append({
                        'name': crop_name,
                        'category': category,
                        'season': crop_info['season'],
                        'benefit': crop_info['benefit'],
                        'duration': crop_info['duration']
                    })
        return defaults[:3]  # Return top 3
    
    def calculate_crop_rotation_benefit(self, rotation_years):
        """Calculate benefits of crop rotation"""
        
        # Simplified benefit calculation
        benefits = {
            'pest_reduction_pct': min(30 + (rotation_years * 10), 70),
            'soil_health_improvement_pct': min(20 + (rotation_years * 8), 50),
            'yield_increase_pct': min(15 + (rotation_years * 5), 35),
            'fertilizer_savings_pct': min(10 + (rotation_years * 5), 30)
        }
        
        return benefits
