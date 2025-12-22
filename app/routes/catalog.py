from flask import Blueprint, jsonify, render_template
from app.data.fertilizer_catalog_db import FertilizerCatalogDB

catalog_bp = Blueprint('catalog', __name__)

@catalog_bp.route('/api/catalog/fertilizers', methods=['GET'])
def get_fertilizer_catalog():
    """Get the full fertilizer catalog."""
    try:
        catalog = FertilizerCatalogDB.get_catalog()
        return jsonify({
            'success': True,
            'data': catalog
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@catalog_bp.route('/modules/katalog-pupuk')
def view_catalog():
    """Render the fertilizer catalog page."""
    return render_template('modules/katalog_pupuk.html')
