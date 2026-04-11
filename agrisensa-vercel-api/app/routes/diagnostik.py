from flask import Blueprint, jsonify, render_template
from app.data.pest_disease_db import PestDiseaseDatabase

diagnostic_bp = Blueprint('diagnostic', __name__)

@diagnostic_bp.route('/tree', methods=['GET'])
def get_diagnostic_tree():
    """Get the diagnostic decision tree."""
    try:
        tree = PestDiseaseDatabase.get_diagnostic_tree()
        return jsonify({
            'success': True,
            'data': tree
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@diagnostic_bp.route('/result/<pest_id>', methods=['GET'])
def get_diagnostic_result(pest_id):
    """Get detailed result for a specific pest ID."""
    try:
        detail = PestDiseaseDatabase.get_pest_detail(pest_id)
        if not detail:
            return jsonify({
                'success': False,
                'error': 'Pest not found'
            }), 404
            
        return jsonify({
            'success': True,
            'data': detail
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
