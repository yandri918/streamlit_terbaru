"""Service layer for AgriMap - business logic and integrations."""
from typing import Dict, List, Optional
from app.data.agrimap_db import AgriMapDatabase
from app.services.weather_service import WeatherService


class AgriMapService:
    """Service for AgriMap operations and analysis."""
    
    def __init__(self):
        self.db = AgriMapDatabase()
        self.weather_service = WeatherService()
    
    # ========== NPK ANALYSIS ==========
    
    def analyze_npk_values(self, n_value: float, p_value: float, k_value: float) -> Dict:
        """Analyze NPK values and provide recommendations."""
        analysis = {
            'N': self._analyze_nutrient('N', n_value),
            'P': self._analyze_nutrient('P', p_value),
            'K': self._analyze_nutrient('K', k_value)
        }
        
        # Overall assessment
        deficiencies = [k for k, v in analysis.items() if v['status'] == 'Rendah']
        excesses = [k for k, v in analysis.items() if v['status'] == 'Berlebih']
        
        overall = {
            'status': 'optimal' if not deficiencies and not excesses else 'needs_attention',
            'deficiencies': deficiencies,
            'excesses': excesses,
            'recommendation': self._get_overall_recommendation(deficiencies, excesses)
        }
        
        return {
            'analysis': analysis,
            'overall': overall
        }
    
    def _analyze_nutrient(self, nutrient: str, value: float) -> Dict:
        """Analyze single nutrient value."""
        # Standard ranges (simplified)
        ranges = {
            'N': {'low': 40, 'optimal_min': 40, 'optimal_max': 100, 'high': 100},
            'P': {'low': 20, 'optimal_min': 20, 'optimal_max': 60, 'high': 60},
            'K': {'low': 30, 'optimal_min': 30, 'optimal_max': 80, 'high': 80}
        }
        
        r = ranges.get(nutrient, ranges['N'])
        
        if value < r['optimal_min']:
            status = 'Rendah'
            color = '#ef4444'
            recommendation = f"Tambahkan pupuk {nutrient} untuk meningkatkan kandungan."
        elif value > r['optimal_max']:
            status = 'Berlebih'
            color = '#f59e0b'
            recommendation = f"Kandungan {nutrient} berlebih. Kurangi pemupukan {nutrient}."
        else:
            status = 'Optimal'
            color = '#10b981'
            recommendation = f"Kandungan {nutrient} dalam kondisi baik."
        
        return {
            'value': value,
            'status': status,
            'color': color,
            'recommendation': recommendation
        }
    
    def _get_overall_recommendation(self, deficiencies: List, excesses: List) -> str:
        """Get overall recommendation based on NPK analysis."""
        if not deficiencies and not excesses:
            return "✅ Kondisi tanah optimal. Lanjutkan pemupukan berimbang."
        
        recommendations = []
        if deficiencies:
            recommendations.append(f"⚠️ Perlu tambahan: {', '.join(deficiencies)}")
        if excesses:
            recommendations.append(f"⚠️ Kurangi: {', '.join(excesses)}")
        
        return " | ".join(recommendations)
    
    # ========== CROP SUITABILITY ==========
    
    def get_crop_suitability(self, latitude: float, longitude: float,
                            n_value: Optional[float] = None,
                            p_value: Optional[float] = None,
                            k_value: Optional[float] = None) -> Dict:
        """Get crop suitability recommendations based on location and soil data."""
        # Get weather data
        weather = self.weather_service.get_current_weather(latitude, longitude)
        
        # Get nearby NPK data if not provided
        if n_value is None or p_value is None or k_value is None:
            nearby_npk = self.db.get_npk_by_location(latitude, longitude, radius_km=5.0)
            if nearby_npk:
                # Use average of nearby samples
                n_value = sum(d['n_value'] for d in nearby_npk) / len(nearby_npk)
                p_value = sum(d['p_value'] for d in nearby_npk) / len(nearby_npk)
                k_value = sum(d['k_value'] for d in nearby_npk) / len(nearby_npk)
        
        # Crop suitability logic
        suitable_crops = []
        
        temp = weather.get('temperature', 25) if weather.get('success') else 25
        
        # Rice - suitable for most conditions
        if temp >= 22 and temp <= 32:
            suitable_crops.append({
                'name': 'Padi',
                'suitability': 'Sangat Sesuai',
                'reason': 'Suhu optimal untuk padi',
                'icon': '🌾'
            })
        
        # Corn
        if temp >= 20 and temp <= 30:
            suitable_crops.append({
                'name': 'Jagung',
                'suitability': 'Sesuai',
                'reason': 'Kondisi suhu mendukung',
                'icon': '🌽'
            })
        
        # Chili
        if temp >= 24 and temp <= 30:
            suitable_crops.append({
                'name': 'Cabai',
                'suitability': 'Sesuai',
                'reason': 'Suhu ideal untuk cabai',
                'icon': '🌶️'
            })
        
        # Tomato
        if temp >= 20 and temp <= 27:
            suitable_crops.append({
                'name': 'Tomat',
                'suitability': 'Sesuai',
                'reason': 'Kondisi iklim mendukung',
                'icon': '🍅'
            })
        
        return {
            'success': True,
            'location': {'latitude': latitude, 'longitude': longitude},
            'weather': weather,
            'npk_data': {
                'n': n_value,
                'p': p_value,
                'k': k_value
            } if n_value else None,
            'suitable_crops': suitable_crops
        }
    
    # ========== FERTILIZER CALCULATOR INTEGRATION ==========
    
    def prepare_fertilizer_data(self, polygon_id: str) -> Dict:
        """Prepare data for fertilizer calculator integration."""
        polygon = self.db.get_polygon_by_id(polygon_id)
        if not polygon:
            return {'success': False, 'error': 'Polygon not found'}
        
        # Get NPK data for this polygon
        npk_data = self.db.get_npk_data(polygon_id=polygon_id)
        
        # Calculate average NPK if multiple samples
        avg_npk = None
        if npk_data:
            avg_npk = {
                'n': sum(d['n_value'] for d in npk_data) / len(npk_data),
                'p': sum(d['p_value'] for d in npk_data) / len(npk_data),
                'k': sum(d['k_value'] for d in npk_data) / len(npk_data)
            }
        
        return {
            'success': True,
            'area_sqm': polygon['area_sqm'],
            'area_hectares': polygon['area_hectares'],
            'ph': polygon.get('ph'),
            'npk_data': avg_npk,
            'polygon_name': polygon['name']
        }
    
    # ========== LAYER DATA GENERATION ==========
    
    def generate_npk_heatmap_data(self) -> List[Dict]:
        """Generate heatmap data for NPK visualization."""
        npk_data = self.db.get_npk_data()
        
        heatmap_points = []
        for data in npk_data:
            # Calculate overall soil quality score (0-100)
            n_score = min(data['n_value'] / 100 * 100, 100)
            p_score = min(data['p_value'] / 60 * 100, 100)
            k_score = min(data['k_value'] / 80 * 100, 100)
            
            overall_score = (n_score + p_score + k_score) / 3
            
            heatmap_points.append({
                'latitude': data['latitude'],
                'longitude': data['longitude'],
                'intensity': overall_score / 100,  # 0-1 scale
                'npk': {
                    'n': data['n_value'],
                    'p': data['p_value'],
                    'k': data['k_value']
                }
            })
        
        return heatmap_points
    
    def get_polygon_with_npk_summary(self, polygon_id: str) -> Dict:
        """Get polygon with NPK data summary."""
        polygon = self.db.get_polygon_by_id(polygon_id)
        if not polygon:
            return {'success': False, 'error': 'Polygon not found'}
        
        npk_data = self.db.get_npk_data(polygon_id=polygon_id)
        
        npk_summary = None
        if npk_data:
            npk_summary = {
                'sample_count': len(npk_data),
                'average': {
                    'n': round(sum(d['n_value'] for d in npk_data) / len(npk_data), 2),
                    'p': round(sum(d['p_value'] for d in npk_data) / len(npk_data), 2),
                    'k': round(sum(d['k_value'] for d in npk_data) / len(npk_data), 2)
                },
                'samples': npk_data
            }
        
        return {
            'success': True,
            'polygon': polygon,
            'npk_summary': npk_summary
        }
