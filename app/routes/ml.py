"""Machine Learning routes for predictions and recommendations."""
from flask import Blueprint, request, jsonify
from app import limiter
from app.services.ml_service import MLService

ml_bp = Blueprint('ml', __name__)


@ml_bp.route('/recommend-crop', methods=['POST'])
@limiter.limit("30 per hour")
def recommend_crop():
    """Recommend crop based on soil and climate data."""
    try:
        data = request.get_json()
        
        required_fields = ['n_value', 'p_value', 'k_value', 'temperature', 'humidity', 'ph', 'rainfall']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        prediction = MLService.recommend_crop(data)
        
        return jsonify({
            'success': True,
            'recommended_crop': prediction
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Crop recommendation failed',
            'message': str(e)
        }), 500


@ml_bp.route('/predict-yield', methods=['POST'])
@limiter.limit("30 per hour")
def predict_yield():
    """Predict crop yield based on input parameters."""
    try:
        data = request.get_json()
        
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'rainfall', 'ph']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        prediction = MLService.predict_yield(data)
        
        return jsonify({
            'success': True,
            'predicted_yield_ton_ha': prediction
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Yield prediction failed',
            'message': str(e)
        }), 500


@ml_bp.route('/predict-yield-advanced', methods=['POST'])
@limiter.limit("20 per hour")
def predict_yield_advanced():
    """Predict yield with explainable AI (SHAP values)."""
    try:
        data = request.get_json()
        
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'rainfall', 'ph']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        result = MLService.predict_yield_advanced(data)
        
        return jsonify({
            'success': True,
            'predicted_yield_ton_ha': result['predicted_yield_ton_ha'],
            'feature_importances': result['feature_importances'],
            'shap_values': result['shap_values'],
            'base_value': result['base_value']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Advanced prediction failed',
            'message': str(e)
        }), 500


@ml_bp.route('/generate-yield-plan', methods=['POST'])
@limiter.limit("20 per hour")
def generate_yield_plan():
    """Generate plan to achieve target yield."""
    try:
        data = request.get_json()
        
        if not data.get('commodity') or not data.get('target_yield'):
            return jsonify({
                'success': False,
                'error': 'Commodity and target_yield are required'
            }), 400
        
        plan = MLService.generate_yield_plan(
            data['commodity'],
            float(data['target_yield'])
        )
        
        if not plan:
            return jsonify({
                'success': False,
                'error': 'Could not generate plan for target yield'
            }), 404
        
        return jsonify({
            'success': True,
            'plan': plan
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Plan generation failed',
            'message': str(e)
        }), 500


@ml_bp.route('/calculate-fertilizer-bags', methods=['POST'])
@limiter.limit("30 per hour")
def calculate_fertilizer_bags():
    """Calculate fertilizer bags needed for nutrient requirement."""
    try:
        data = request.get_json()
        
        required_fields = ['nutrient_needed', 'nutrient_amount_kg', 'fertilizer_type']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        result = MLService.calculate_fertilizer_bags(
            data['nutrient_needed'],
            float(data['nutrient_amount_kg']),
            data['fertilizer_type']
        )
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'Calculation failed. Check fertilizer type and nutrient.'
            }), 400
        
        return jsonify({
            'success': True,
            'required_fertilizer_kg': result['required_kg'],
            'fertilizer_name': result['fertilizer_name'],
            'nutrient_needed': result['nutrient_needed'],
            'nutrient_amount_kg': result['nutrient_amount_kg']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Calculation failed',
            'message': str(e)
        }), 500


@ml_bp.route('/predict-success', methods=['POST'])
@limiter.limit("30 per hour")
def predict_success():
    """Predict success probability for crop cultivation."""
    try:
        data = request.get_json()
        
        required_fields = ['nitrogen', 'phosphorus', 'potassium', 'temperature', 'rainfall', 'ph']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        result = MLService.predict_success(data)
        
        return jsonify({
            'success': True,
            'status': result['status'],
            'probability_of_success': result['probability_of_success']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Success prediction failed',
            'message': str(e)
        }), 500