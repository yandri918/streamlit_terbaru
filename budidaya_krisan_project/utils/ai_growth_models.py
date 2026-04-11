"""
AI Growth Models for Chrysanthemum Cultivation
Machine Learning models for growth prediction and anomaly detection
"""

import numpy as np
import pandas as pd
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
from sklearn.pipeline import make_pipeline
from scipy import stats
from datetime import datetime, timedelta


class GrowthPredictor:
    """Polynomial regression model for growth prediction"""
    
    def __init__(self, degree=3):
        self.degree = degree
        self.model = None
        self.std_error = None
        
    def fit(self, weeks, heights):
        """
        Fit polynomial regression model
        
        Args:
            weeks: array of week numbers
            heights: array of plant heights
        """
        X = np.array(weeks).reshape(-1, 1)
        y = np.array(heights)
        
        # Create polynomial regression model
        self.model = make_pipeline(
            PolynomialFeatures(self.degree),
            LinearRegression()
        )
        self.model.fit(X, y)
        
        # Calculate standard error for confidence intervals
        predictions = self.model.predict(X)
        residuals = y - predictions
        self.std_error = np.std(residuals)
        
        return self
    
    def predict(self, weeks_ahead=4, current_week=1):
        """
        Predict future growth
        
        Args:
            weeks_ahead: number of weeks to predict
            current_week: current week number
            
        Returns:
            dict with predictions, upper_bound, lower_bound
        """
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        future_weeks = np.array(range(current_week + 1, current_week + weeks_ahead + 1)).reshape(-1, 1)
        predictions = self.model.predict(future_weeks)
        
        # Calculate 95% confidence interval
        confidence = 1.96 * self.std_error
        upper_bound = predictions + confidence
        lower_bound = predictions - confidence
        
        return {
            'weeks': future_weeks.flatten().tolist(),
            'predictions': predictions.tolist(),
            'upper_bound': upper_bound.tolist(),
            'lower_bound': lower_bound.tolist(),
            'confidence_interval': confidence
        }
    
    def get_fitted_curve(self, weeks):
        """Get fitted curve for visualization"""
        if self.model is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        X = np.array(weeks).reshape(-1, 1)
        return self.model.predict(X).tolist()


class AnomalyDetector:
    """Isolation Forest for anomaly detection in growth data"""
    
    def __init__(self, contamination=0.1):
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.feature_names = []
        
    def prepare_features(self, growth_data, standards):
        """
        Prepare features for anomaly detection
        
        Args:
            growth_data: DataFrame with columns [week, height, leaves, diameter]
            standards: dict of standard growth values by week
            
        Returns:
            numpy array of features
        """
        features = []
        self.feature_names = ['height', 'leaves', 'diameter', 'growth_rate', 'height_deviation']
        
        for i, row in growth_data.iterrows():
            week = row['week']
            height = row['height']
            leaves = row['leaves']
            diameter = row['diameter']
            
            # Calculate growth rate
            if i > 0:
                prev_height = growth_data.iloc[i-1]['height']
                growth_rate = height - prev_height
            else:
                growth_rate = 0
            
            # Deviation from standard
            std_height = standards.get(week, {}).get('h', height)
            if std_height > 0:
                height_deviation = (height - std_height) / std_height
            else:
                height_deviation = 0
            
            features.append([height, leaves, diameter, growth_rate, height_deviation])
        
        return np.array(features)
    
    def detect(self, growth_data, standards):
        """
        Detect anomalies in growth data
        
        Args:
            growth_data: DataFrame with growth measurements
            standards: dict of standard growth values
            
        Returns:
            dict with anomaly_indices, predictions, scores
        """
        features = self.prepare_features(growth_data, standards)
        
        # Fit and predict
        predictions = self.model.fit_predict(features)
        scores = self.model.score_samples(features)
        
        # -1 = anomaly, 1 = normal
        anomaly_indices = [i for i, pred in enumerate(predictions) if pred == -1]
        
        # Get anomaly details
        anomalies = []
        for idx in anomaly_indices:
            row = growth_data.iloc[idx]
            anomalies.append({
                'index': idx,
                'week': row['week'],
                'height': row['height'],
                'score': scores[idx],
                'severity': 'HIGH' if scores[idx] < -0.5 else 'MEDIUM'
            })
        
        return {
            'anomaly_indices': anomaly_indices,
            'predictions': predictions.tolist(),
            'scores': scores.tolist(),
            'anomalies': anomalies,
            'total_anomalies': len(anomaly_indices)
        }


class GrowthRateAnalyzer:
    """Analyze growth rate patterns and trends"""
    
    @staticmethod
    def calculate_growth_rate(growth_data):
        """Calculate week-over-week growth rate"""
        if len(growth_data) < 2:
            return []
        
        rates = []
        for i in range(1, len(growth_data)):
            prev_height = growth_data.iloc[i-1]['height']
            curr_height = growth_data.iloc[i]['height']
            rate = curr_height - prev_height
            rates.append(rate)
        
        return rates
    
    @staticmethod
    def detect_growth_slowdown(growth_data, threshold=0.5):
        """
        Detect if growth is slowing down significantly
        
        Args:
            growth_data: DataFrame with growth measurements
            threshold: minimum acceptable growth rate (cm/week)
            
        Returns:
            dict with slowdown status and recommendations
        """
        rates = GrowthRateAnalyzer.calculate_growth_rate(growth_data)
        
        if len(rates) < 2:
            return {'slowdown': False, 'message': 'Insufficient data'}
        
        # Check last 2 weeks
        recent_rates = rates[-2:]
        avg_recent = np.mean(recent_rates)
        
        if avg_recent < threshold:
            return {
                'slowdown': True,
                'avg_rate': avg_recent,
                'message': f'Growth slowing: {avg_recent:.1f} cm/week (expected > {threshold})',
                'recommendations': [
                    'Check EC and pH of nutrient solution',
                    'Verify root health for root rot',
                    'Increase nitrogen if in vegetative phase',
                    'Check for pest damage (thrips, aphids)'
                ]
            }
        else:
            return {
                'slowdown': False,
                'avg_rate': avg_recent,
                'message': f'Growth rate healthy: {avg_recent:.1f} cm/week'
            }
    
    @staticmethod
    def calculate_consistency_score(growth_data):
        """
        Calculate consistency score (0-100)
        Lower variance = higher score
        """
        rates = GrowthRateAnalyzer.calculate_growth_rate(growth_data)
        
        if len(rates) < 3:
            return 100  # Not enough data, assume consistent
        
        # Calculate coefficient of variation
        mean_rate = np.mean(rates)
        std_rate = np.std(rates)
        
        if mean_rate == 0:
            return 50
        
        cv = std_rate / mean_rate
        
        # Convert to 0-100 scale (lower CV = higher score)
        # CV of 0.2 = 100, CV of 1.0 = 0
        score = max(0, min(100, 100 * (1 - cv / 1.0)))
        
        return score


class HarvestPredictor:
    """Predict optimal harvest date based on growth trajectory"""
    
    @staticmethod
    def predict_harvest_date(growth_data, target_height=100, start_date=None):
        """
        Predict when plant will reach harvest height
        
        Args:
            growth_data: DataFrame with growth measurements
            target_height: target height for harvest (cm)
            start_date: planting start date
            
        Returns:
            dict with predicted week and date
        """
        if len(growth_data) < 3:
            return {'status': 'insufficient_data'}
        
        # Fit growth model
        predictor = GrowthPredictor(degree=3)
        predictor.fit(growth_data['week'].values, growth_data['height'].values)
        
        # Find week when target height is reached
        current_week = growth_data['week'].max()
        max_week = 16  # Maximum growth period
        
        for week in range(int(current_week) + 1, max_week + 1):
            predicted_height = predictor.model.predict([[week]])[0]
            
            if predicted_height >= target_height:
                # Calculate date if start_date provided
                if start_date:
                    harvest_date = start_date + timedelta(weeks=week)
                    date_str = harvest_date.strftime('%Y-%m-%d')
                else:
                    date_str = None
                
                return {
                    'status': 'predicted',
                    'harvest_week': week,
                    'harvest_date': date_str,
                    'predicted_height': predicted_height,
                    'confidence': 'HIGH' if week <= 15 else 'MEDIUM'
                }
        
        return {
            'status': 'delayed',
            'message': f'Plant may not reach {target_height}cm within normal period',
            'current_trajectory': 'below_target'
        }
    
    @staticmethod
    def estimate_harvest_window(growth_data, variety='standard'):
        """
        Estimate harvest window based on variety and growth stage
        
        Args:
            growth_data: DataFrame with growth measurements
            variety: chrysanthemum variety type
            
        Returns:
            dict with harvest window information
        """
        current_week = growth_data['week'].max()
        current_height = growth_data['height'].max()
        
        # Standard harvest parameters
        harvest_params = {
            'standard': {'min_week': 12, 'max_week': 15, 'min_height': 95},
            'spray': {'min_week': 10, 'max_week': 13, 'min_height': 85},
            'disbud': {'min_week': 14, 'max_week': 16, 'min_height': 100}
        }
        
        params = harvest_params.get(variety, harvest_params['standard'])
        
        # Calculate readiness
        weeks_to_min = max(0, params['min_week'] - current_week)
        height_gap = max(0, params['min_height'] - current_height)
        
        if current_week >= params['min_week'] and current_height >= params['min_height']:
            status = 'READY'
            message = 'Plant is ready for harvest'
        elif current_week < params['min_week']:
            status = 'GROWING'
            message = f'{weeks_to_min} weeks until minimum harvest window'
        else:
            status = 'DELAYED'
            message = f'Height below target: {height_gap:.1f}cm gap'
        
        return {
            'status': status,
            'message': message,
            'current_week': current_week,
            'current_height': current_height,
            'target_week_range': f"{params['min_week']}-{params['max_week']}",
            'target_height': params['min_height'],
            'weeks_remaining': weeks_to_min
        }


# Utility functions
def smooth_data(values, window=3):
    """Apply moving average smoothing"""
    if len(values) < window:
        return values
    
    smoothed = []
    for i in range(len(values)):
        start = max(0, i - window // 2)
        end = min(len(values), i + window // 2 + 1)
        smoothed.append(np.mean(values[start:end]))
    
    return smoothed


def calculate_r_squared(actual, predicted):
    """Calculate R² score for model fit"""
    ss_res = np.sum((actual - predicted) ** 2)
    ss_tot = np.sum((actual - np.mean(actual)) ** 2)
    
    if ss_tot == 0:
        return 0
    
    r2 = 1 - (ss_res / ss_tot)
    return r2
