"""
Health Scoring System for Chrysanthemum Plants
Multi-factor algorithm to assess plant health (0-100 scale)
"""

import numpy as np
from datetime import datetime


class HealthScorer:
    """Calculate comprehensive plant health score"""
    
    # Weights for different factors
    WEIGHTS = {
        'growth': 0.30,
        'morphology': 0.25,
        'environment': 0.20,
        'consistency': 0.15,
        'predictive': 0.10
    }
    
    def __init__(self, standards):
        """
        Initialize health scorer
        
        Args:
            standards: dict of standard growth values by week
        """
        self.standards = standards
    
    def calculate_growth_score(self, plant_data, week):
        """
        Score based on height relative to ideal
        
        Returns: score (0-100)
        """
        actual_height = plant_data.get('height', 0)
        ideal_height = self.standards.get(week, {}).get('h', actual_height)
        
        if ideal_height == 0:
            return 50
        
        height_ratio = actual_height / ideal_height
        
        # Optimal range: 0.9 - 1.1 (90-110% of ideal)
        if 0.9 <= height_ratio <= 1.1:
            score = 100
        elif 0.8 <= height_ratio < 0.9 or 1.1 < height_ratio <= 1.2:
            score = 85
        elif 0.7 <= height_ratio < 0.8 or 1.2 < height_ratio <= 1.3:
            score = 70
        elif 0.6 <= height_ratio < 0.7 or 1.3 < height_ratio <= 1.4:
            score = 50
        else:
            score = max(0, 30 - abs(height_ratio - 1.0) * 50)
        
        return score
    
    def calculate_morphology_score(self, plant_data, week):
        """
        Score based on leaves, stem diameter, and overall structure
        
        Returns: score (0-100)
        """
        actual_leaves = plant_data.get('leaves', 0)
        ideal_leaves = self.standards.get(week, {}).get('l', actual_leaves)
        diameter = plant_data.get('diameter', 0)
        
        # Leaf count score
        if ideal_leaves > 0:
            leaf_ratio = actual_leaves / ideal_leaves
            leaf_score = min(100, max(0, leaf_ratio * 100))
        else:
            leaf_score = 50
        
        # Stem diameter score (ideal: 4-6mm)
        if 4.0 <= diameter <= 6.0:
            diameter_score = 100
        elif 3.0 <= diameter < 4.0 or 6.0 < diameter <= 7.0:
            diameter_score = 80
        elif 2.5 <= diameter < 3.0 or 7.0 < diameter <= 8.0:
            diameter_score = 60
        else:
            diameter_score = max(0, 40 - abs(diameter - 5.0) * 10)
        
        # Combined morphology score
        morphology_score = (leaf_score * 0.6 + diameter_score * 0.4)
        
        return morphology_score
    
    def calculate_environment_score(self, plant_data):
        """
        Score based on temperature and humidity suitability
        
        Returns: score (0-100)
        """
        temp = plant_data.get('temp', 21)
        humidity = plant_data.get('humidity', 67.5)
        
        # Temperature score (ideal: 18-24°C)
        if 18 <= temp <= 24:
            temp_score = 100
        elif 15 <= temp < 18 or 24 < temp <= 28:
            temp_score = 80 - abs(temp - 21) * 3
        else:
            temp_score = max(0, 50 - abs(temp - 21) * 5)
        
        # Humidity score (ideal: 60-75%)
        if 60 <= humidity <= 75:
            humid_score = 100
        elif 50 <= humidity < 60 or 75 < humidity <= 85:
            humid_score = 80 - abs(humidity - 67.5) * 2
        else:
            humid_score = max(0, 50 - abs(humidity - 67.5) * 2)
        
        # Combined environment score
        environment_score = (temp_score * 0.5 + humid_score * 0.5)
        
        return environment_score
    
    def calculate_consistency_score(self, growth_history):
        """
        Score based on growth rate consistency
        
        Args:
            growth_history: list of historical measurements
            
        Returns: score (0-100)
        """
        if len(growth_history) < 3:
            return 100  # Not enough data, assume consistent
        
        # Calculate week-over-week growth rates
        growth_rates = []
        for i in range(1, len(growth_history)):
            prev_height = growth_history[i-1].get('height', 0)
            curr_height = growth_history[i].get('height', 0)
            rate = curr_height - prev_height
            growth_rates.append(rate)
        
        if len(growth_rates) < 2:
            return 100
        
        # Calculate coefficient of variation
        mean_rate = np.mean(growth_rates)
        std_rate = np.std(growth_rates)
        
        if mean_rate == 0:
            return 50
        
        cv = std_rate / mean_rate
        
        # Convert to score (lower CV = higher score)
        # CV of 0.2 = 100, CV of 1.0 = 0
        score = max(0, min(100, 100 * (1 - cv / 1.0)))
        
        return score
    
    def calculate_predictive_score(self, plant_data, week, prediction_result=None):
        """
        Score based on predicted future performance
        
        Args:
            plant_data: current plant data
            week: current week
            prediction_result: result from GrowthPredictor
            
        Returns: score (0-100)
        """
        # If no prediction available, use current trajectory
        if prediction_result is None:
            current_height = plant_data.get('height', 0)
            ideal_height = self.standards.get(week, {}).get('h', current_height)
            
            if ideal_height > 0:
                trajectory_score = min(100, (current_height / ideal_height) * 100)
            else:
                trajectory_score = 50
            
            return trajectory_score
        
        # Use prediction to assess future performance
        predicted_heights = prediction_result.get('predictions', [])
        
        if not predicted_heights:
            return 50
        
        # Check if predicted to reach target height (100cm) by week 12
        target_height = 100
        target_week = 12
        
        if len(predicted_heights) > 0:
            final_predicted = predicted_heights[-1]
            
            if final_predicted >= target_height:
                score = 100
            elif final_predicted >= target_height * 0.9:
                score = 85
            elif final_predicted >= target_height * 0.8:
                score = 70
            else:
                score = max(0, (final_predicted / target_height) * 100)
        else:
            score = 50
        
        return score
    
    def calculate_total_score(self, plant_data, week, growth_history=None, prediction_result=None):
        """
        Calculate comprehensive health score
        
        Args:
            plant_data: current plant measurements
            week: current week number
            growth_history: list of historical measurements (optional)
            prediction_result: ML prediction result (optional)
            
        Returns:
            dict with total_score, breakdown, and grade
        """
        scores = {}
        
        # Calculate individual scores
        scores['growth'] = self.calculate_growth_score(plant_data, week)
        scores['morphology'] = self.calculate_morphology_score(plant_data, week)
        scores['environment'] = self.calculate_environment_score(plant_data)
        
        if growth_history and len(growth_history) >= 3:
            scores['consistency'] = self.calculate_consistency_score(growth_history)
        else:
            scores['consistency'] = 100  # Default for insufficient data
        
        scores['predictive'] = self.calculate_predictive_score(plant_data, week, prediction_result)
        
        # Calculate weighted total
        total_score = sum(scores[k] * self.WEIGHTS[k] for k in scores)
        
        # Determine grade
        if total_score >= 90:
            grade = 'A'
            status = 'Excellent'
            color = '#10b981'
        elif total_score >= 80:
            grade = 'B'
            status = 'Good'
            color = '#22c55e'
        elif total_score >= 70:
            grade = 'C'
            status = 'Fair'
            color = '#eab308'
        elif total_score >= 60:
            grade = 'D'
            status = 'Poor'
            color = '#f97316'
        else:
            grade = 'F'
            status = 'Critical'
            color = '#ef4444'
        
        return {
            'total_score': round(total_score, 1),
            'grade': grade,
            'status': status,
            'color': color,
            'breakdown': {k: round(v, 1) for k, v in scores.items()},
            'weights': self.WEIGHTS
        }


class HealthDiagnostics:
    """Diagnose specific health issues based on symptoms"""
    
    @staticmethod
    def diagnose_nutrient_deficiency(plant_data, week, standards):
        """
        Diagnose potential nutrient deficiencies
        
        Returns: list of deficiency warnings
        """
        warnings = []
        
        height = plant_data.get('height', 0)
        leaves = plant_data.get('leaves', 0)
        diameter = plant_data.get('diameter', 0)
        
        ideal_height = standards.get(week, {}).get('h', height)
        ideal_leaves = standards.get(week, {}).get('l', leaves)
        
        # Nitrogen deficiency (stunted growth + few leaves)
        if height < ideal_height * 0.8 and leaves < ideal_leaves * 0.8:
            warnings.append({
                'nutrient': 'Nitrogen (N)',
                'severity': 'HIGH',
                'symptoms': 'Stunted growth, pale/yellow lower leaves, reduced leaf count',
                'recommendation': 'Apply high-N fertilizer (20-10-10) @ 2g/L, 2x per week',
                'expected_recovery': '1-2 weeks'
            })
        
        # Phosphorus deficiency (slow growth + thin stems)
        if diameter < 3.0 and week > 4:
            warnings.append({
                'nutrient': 'Phosphorus (P)',
                'severity': 'MEDIUM',
                'symptoms': 'Thin stems, slow root development, dark green/purple leaves',
                'recommendation': 'Apply high-P fertilizer (10-52-10) @ 1.5g/L weekly',
                'expected_recovery': '2-3 weeks'
            })
        
        # Potassium deficiency (weak stems + leaf edges brown)
        if diameter < 3.5 and week > 6:
            warnings.append({
                'nutrient': 'Potassium (K)',
                'severity': 'MEDIUM',
                'symptoms': 'Weak stems, leaf edge burn, poor flower quality',
                'recommendation': 'Apply KNO3 @ 1.5g/L or high-K fertilizer (10-10-30)',
                'expected_recovery': '1-2 weeks'
            })
        
        return warnings
    
    @staticmethod
    def diagnose_environmental_stress(plant_data):
        """
        Diagnose environmental stress conditions
        
        Returns: list of stress warnings
        """
        warnings = []
        
        temp = plant_data.get('temp', 21)
        humidity = plant_data.get('humidity', 67.5)
        
        # Heat stress
        if temp > 28:
            warnings.append({
                'stress_type': 'Heat Stress',
                'severity': 'HIGH' if temp > 32 else 'MEDIUM',
                'symptoms': 'Wilting, small flowers, faded colors, leaf burn',
                'recommendation': 'Increase misting, use shade net 30-40%, improve ventilation',
                'immediate_action': 'Mist plants every 2 hours during peak heat'
            })
        
        # Cold stress
        if temp < 15:
            warnings.append({
                'stress_type': 'Cold Stress',
                'severity': 'HIGH' if temp < 12 else 'MEDIUM',
                'symptoms': 'Slow growth, purple discoloration, delayed flowering',
                'recommendation': 'Use thermal screens at night, consider heating system',
                'immediate_action': 'Close greenhouse vents, use dambo heater if available'
            })
        
        # High humidity (disease risk)
        if humidity > 85:
            warnings.append({
                'stress_type': 'High Humidity',
                'severity': 'HIGH',
                'symptoms': 'Fungal disease risk (white rust, powdery mildew)',
                'recommendation': 'Increase air circulation, reduce watering, apply preventive fungicide',
                'immediate_action': 'Open vents, run fans, avoid overhead watering'
            })
        
        # Low humidity (water stress)
        if humidity < 50:
            warnings.append({
                'stress_type': 'Low Humidity',
                'severity': 'MEDIUM',
                'symptoms': 'Leaf tip burn, wilting, reduced growth',
                'recommendation': 'Increase misting frequency, wet floor/paths, reduce ventilation',
                'immediate_action': 'Mist plants and wet greenhouse floor'
            })
        
        return warnings
    
    @staticmethod
    def get_health_recommendations(health_score_result, diagnostics):
        """
        Generate prioritized recommendations based on health assessment
        
        Args:
            health_score_result: result from HealthScorer.calculate_total_score()
            diagnostics: dict with nutrient and environmental warnings
            
        Returns:
            list of prioritized recommendations
        """
        recommendations = []
        
        total_score = health_score_result['total_score']
        breakdown = health_score_result['breakdown']
        
        # Critical score - immediate action needed
        if total_score < 60:
            recommendations.append({
                'priority': 'CRITICAL',
                'category': 'Overall Health',
                'action': 'Immediate intervention required',
                'details': 'Plant health is critically low. Review all parameters and take corrective action within 24 hours.',
                'icon': '🚨'
            })
        
        # Growth score low
        if breakdown['growth'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Growth',
                'action': 'Boost growth rate',
                'details': 'Increase nitrogen fertilization, check root health, verify adequate light duration',
                'icon': '📈'
            })
        
        # Morphology score low
        if breakdown['morphology'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Plant Structure',
                'action': 'Improve plant morphology',
                'details': 'Adjust NPK ratio, ensure proper pinching, check for pest damage',
                'icon': '🌿'
            })
        
        # Environment score low
        if breakdown['environment'] < 70:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Environment',
                'action': 'Optimize growing conditions',
                'details': 'Adjust temperature and humidity to optimal range (18-24°C, 60-75% RH)',
                'icon': '🌡️'
            })
        
        # Add nutrient deficiency warnings
        for warning in diagnostics.get('nutrient_warnings', []):
            recommendations.append({
                'priority': warning['severity'],
                'category': 'Nutrient',
                'action': f"Address {warning['nutrient']} deficiency",
                'details': warning['recommendation'],
                'icon': '🧪'
            })
        
        # Add environmental stress warnings
        for warning in diagnostics.get('environmental_warnings', []):
            recommendations.append({
                'priority': warning['severity'],
                'category': 'Environment',
                'action': f"Mitigate {warning['stress_type']}",
                'details': warning['immediate_action'],
                'icon': '⚠️'
            })
        
        # Sort by priority
        priority_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, 'INFO': 4}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 5))
        
        return recommendations
