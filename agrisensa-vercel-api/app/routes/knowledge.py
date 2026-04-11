"""Knowledge base routes for agricultural information."""
from flask import Blueprint, request, jsonify
from app import limiter
from app.services.knowledge_service import KnowledgeService

knowledge_bp = Blueprint('knowledge', __name__)


@knowledge_bp.route('/crop/<commodity>', methods=['GET'])
@limiter.limit("50 per hour")
def get_crop_knowledge(commodity):
    """Get knowledge base for specific crop."""
    try:
        knowledge = KnowledgeService.get_crop_knowledge(commodity)
        
        if not knowledge:
            return jsonify({
                'success': False,
                'error': 'Knowledge not found for this commodity'
            }), 404
        
        return jsonify({
            'success': True,
            'data': knowledge
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get knowledge',
            'message': str(e)
        }), 500


@knowledge_bp.route('/commodities', methods=['GET'])
@limiter.limit("50 per hour")
def get_commodities():
    """Get list of all available commodities."""
    try:
        commodities = KnowledgeService.get_all_commodities()
        
        return jsonify({
            'success': True,
            'data': commodities
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get commodities',
            'message': str(e)
        }), 500


@knowledge_bp.route('/guide/<commodity>', methods=['GET'])
@limiter.limit("50 per hour")
def get_commodity_guide(commodity):
    """Get comprehensive guide for specific commodity."""
    try:
        guide = KnowledgeService.get_commodity_guide(commodity)
        
        if not guide:
            return jsonify({
                'success': False,
                'error': 'Guide not available for this commodity'
            }), 404
        
        return jsonify({
            'success': True,
            'data': guide
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get guide',
            'message': str(e)
        }), 500


@knowledge_bp.route('/ph-info', methods=['GET'])
@limiter.limit("50 per hour")
def get_ph_info():
    """Get pH knowledge base information."""
    try:
        info = KnowledgeService.get_ph_knowledge()
        
        return jsonify({
            'success': True,
            'data': info
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get pH information',
            'message': str(e)
        }), 500


@knowledge_bp.route('/diagnostic-tree', methods=['GET'])
@limiter.limit("50 per hour")
def get_diagnostic_tree():
    """Get plant disease diagnostic decision tree."""
    try:
        tree = KnowledgeService.get_diagnostic_tree()
        
        return jsonify({
            'success': True,
            'data': tree
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get diagnostic tree',
            'message': str(e)
        }), 500


@knowledge_bp.route('/fertilizer-data', methods=['GET'])
@limiter.limit("50 per hour")
def get_fertilizer_data():
    """Get fertilizer composition data."""
    try:
        data = KnowledgeService.get_fertilizer_data()
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get fertilizer data',
            'message': str(e)
        }), 500
