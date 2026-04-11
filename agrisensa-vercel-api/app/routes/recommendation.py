"""Recommendation routes for fertilizer and crop recommendations."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.recommendation import Recommendation
from app.services.recommendation_service import RecommendationService

recommendation_bp = Blueprint('recommendation', __name__)


@recommendation_bp.route('/fertilizer', methods=['POST'])
@limiter.limit("30 per hour")
def get_fertilizer_recommendation():
    """Get fertilizer recommendation based on soil and crop data."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['ph_tanah', 'skor_bwd', 'kelembaban_tanah', 'umur_tanaman_hari']
        if not isinstance(data, dict) or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        # Get recommendation
        recommendation = RecommendationService.get_fertilizer_recommendation(data)
        
        # Save recommendation if user is authenticated
        try:
            user_id = get_jwt_identity()
            rec = Recommendation(
                user_id=user_id,
                recommendation_type='fertilizer',
                input_data=data,
                recommendation_data=recommendation,
                crop_type=data.get('crop_type')
            )
            db.session.add(rec)
            db.session.commit()
        except:
            pass  # Allow anonymous recommendations
        
        return jsonify({
            'success': True,
            'recommendation': recommendation
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Recommendation failed',
            'message': str(e)
        }), 500


@recommendation_bp.route('/calculate-fertilizer', methods=['POST'])
@limiter.limit("30 per hour")
def calculate_fertilizer():
    """Calculate fertilizer dosage for specific crop and area."""
    try:
        data = request.get_json()
        
        required_fields = ['commodity', 'area_sqm', 'ph_tanah']
        if not isinstance(data, dict) or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        
        result = RecommendationService.calculate_fertilizer_dosage(
            commodity=data['commodity'],
            area_sqm=float(data['area_sqm']),
            ph_tanah=float(data['ph_tanah'])
        )
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'Commodity not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Calculation failed',
            'message': str(e)
        }), 500


@recommendation_bp.route('/integrated', methods=['POST'])
@limiter.limit("30 per hour")
def get_integrated_recommendation():
    """Get integrated recommendation (bibit, pemupukan, penyemprotan)."""
    try:
        data = request.get_json()
        
        if not isinstance(data, dict):
            return jsonify({
                'success': False,
                'error': 'Invalid JSON payload'
            }), 400
        
        ketinggian = data.get('ketinggian')
        iklim = data.get('iklim')
        fase = data.get('fase')
        masalah = data.get('masalah')
        
        result = RecommendationService.get_integrated_recommendation(
            ketinggian=ketinggian,
            iklim=iklim,
            fase=fase,
            masalah=masalah
        )
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Recommendation failed',
            'message': str(e)
        }), 500


@recommendation_bp.route('/spraying', methods=['POST'])
@limiter.limit("30 per hour")
def get_spraying_recommendation():
    """Get spraying strategy recommendation for pest control."""
    try:
        data = request.get_json()
        
        if not isinstance(data, dict) or not data.get('pest'):
            return jsonify({
                'success': False,
                'error': 'Pest type is required'
            }), 400
        
        result = RecommendationService.get_spraying_recommendation(data['pest'])
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'Strategy not found for this pest'
            }), 404
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Recommendation failed',
            'message': str(e)
        }), 500


@recommendation_bp.route('/history', methods=['GET'])
@jwt_required()
def get_recommendation_history():
    """Get recommendation history for current user."""
    try:
        user_id = get_jwt_identity()
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        rec_type = request.args.get('type')
        
        query = Recommendation.query.filter_by(user_id=user_id)
        
        if rec_type:
            query = query.filter_by(recommendation_type=rec_type)
        
        recommendations = query.order_by(Recommendation.timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'recommendations': [r.to_dict() for r in recommendations.items],
            'total': recommendations.total,
            'page': recommendations.page,
            'pages': recommendations.pages
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get recommendation history',
            'message': str(e)
        }), 500

@recommendation_bp.route('/recommendation', methods=['POST'])
@limiter.limit("30 per hour")
def recommendation_endpoint():
    """Handle fertilizer recommendation from frontend form.
    Expects JSON with keys: ph, area_sqm, commodity.
    Returns dosage calculation result.
    """
    try:
        data = request.get_json()
        required_fields = ['ph', 'area_sqm', 'commodity']
        if not isinstance(data, dict) or not all(f in data for f in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields',
                'required': required_fields
            }), 400
        # Map to service parameters
        result = RecommendationService.calculate_fertilizer_dosage(
            commodity=data['commodity'],
            area_sqm=float(data['area_sqm']),
            ph_tanah=float(data['ph'])
        )
        if not result:
            return jsonify({
                'success': False,
                'error': 'Commodity not found'
            }), 404
        return jsonify({
            'success': True,
            'data': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Recommendation failed',
            'message': str(e)
        }), 500
