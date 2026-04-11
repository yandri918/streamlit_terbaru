"""Pesticide knowledge routes."""
from flask import Blueprint, request, jsonify
from app import limiter
from app.services.pesticide_service import PesticideService

pesticide_bp = Blueprint('pesticide', __name__)


@pesticide_bp.route('/all', methods=['GET'])
@limiter.limit("50 per hour")
def get_all_pesticides():
    """Get list of all pesticide active ingredients."""
    try:
        pesticides = PesticideService.get_all_pesticides()
        # Convert dict to list for frontend
        pesticide_list = list(pesticides.values())
        
        return jsonify({
            'success': True,
            'data': pesticide_list
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get pesticides',
            'message': str(e)
        }), 500


@pesticide_bp.route('/detail/<pesticide_id>', methods=['GET'])
@limiter.limit("50 per hour")
def get_pesticide_detail(pesticide_id):
    """Get details for a specific pesticide."""
    try:
        pesticide = PesticideService.get_pesticide_by_id(pesticide_id)
        
        if not pesticide:
            return jsonify({
                'success': False,
                'error': 'Pesticide not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': pesticide
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get pesticide detail',
            'message': str(e)
        }), 500


@pesticide_bp.route('/search', methods=['GET'])
@limiter.limit("50 per hour")
def search_pesticides():
    """Search pesticides."""
    try:
        query = request.args.get('q', '')
        if not query:
            return get_all_pesticides()
            
        results = PesticideService.search_pesticides(query)
        
        return jsonify({
            'success': True,
            'data': results
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to search pesticides',
            'message': str(e)
        }), 500
