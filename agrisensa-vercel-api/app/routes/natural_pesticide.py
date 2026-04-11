"""Natural pesticide knowledge routes."""
from flask import Blueprint, request, jsonify
from app import limiter
from app.services.natural_pesticide_service import NaturalPesticideService

natural_pesticide_bp = Blueprint('natural_pesticide', __name__)


@natural_pesticide_bp.route('/all', methods=['GET'])
@limiter.limit("50 per hour")
def get_all_plants():
    """Get all natural pesticide plants."""
    try:
        plants = NaturalPesticideService.get_all_plants()
        # Convert dict to list for frontend
        plant_list = list(plants.values())
        
        return jsonify({
            'success': True,
            'data': plant_list,
            'count': len(plant_list)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get plants',
            'message': str(e)
        }), 500


@natural_pesticide_bp.route('/list', methods=['GET'])
@limiter.limit("50 per hour")
def get_plant_list():
    """Get simplified list of plants for browsing."""
    try:
        plants = NaturalPesticideService.get_plant_list()
        
        return jsonify({
            'success': True,
            'data': plants,
            'count': len(plants)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get plant list',
            'message': str(e)
        }), 500


@natural_pesticide_bp.route('/detail/<plant_id>', methods=['GET'])
@limiter.limit("50 per hour")
def get_plant_detail(plant_id):
    """Get details for a specific plant."""
    try:
        plant = NaturalPesticideService.get_plant_by_id(plant_id)
        
        if not plant:
            return jsonify({
                'success': False,
                'error': 'Plant not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': plant
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get plant detail',
            'message': str(e)
        }), 500


@natural_pesticide_bp.route('/search', methods=['GET'])
@limiter.limit("50 per hour")
def search_plants():
    """Search plants by name, pest, or chemical compound."""
    try:
        query = request.args.get('q', '')
        if not query:
            return get_plant_list()
            
        results = NaturalPesticideService.search_plants(query)
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'query': query
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to search plants',
            'message': str(e)
        }), 500


@natural_pesticide_bp.route('/by-pest/<pest_name>', methods=['GET'])
@limiter.limit("50 per hour")
def get_by_pest(pest_name):
    """Get plants that control specific pest."""
    try:
        results = NaturalPesticideService.get_by_pest(pest_name)
        
        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'pest': pest_name
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get plants by pest',
            'message': str(e)
        }), 500


@natural_pesticide_bp.route('/formulations/<plant_id>', methods=['GET'])
@limiter.limit("50 per hour")
def get_formulations(plant_id):
    """Get formulation methods for a plant."""
    try:
        result = NaturalPesticideService.get_formulations(plant_id)
        
        if not result:
            return jsonify({
                'success': False,
                'error': 'Plant not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': result
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get formulations',
            'message': str(e)
        }), 500


@natural_pesticide_bp.route('/pests', methods=['GET'])
@limiter.limit("50 per hour")
def get_all_pests():
    """Get list of all pests that can be controlled."""
    try:
        pests = NaturalPesticideService.get_all_pests()
        
        return jsonify({
            'success': True,
            'data': pests,
            'count': len(pests)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get pests',
            'message': str(e)
        }), 500


@natural_pesticide_bp.route('/plant-parts', methods=['GET'])
@limiter.limit("50 per hour")
def get_plant_parts():
    """Get list of all plant parts used."""
    try:
        parts = NaturalPesticideService.get_all_plant_parts()
        
        return jsonify({
            'success': True,
            'data': parts,
            'count': len(parts)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get plant parts',
            'message': str(e)
        }), 500
