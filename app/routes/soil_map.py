"""Routes for soil map and weather integration."""
from flask import Blueprint, render_template, request, jsonify
from app.services.weather_service import WeatherService
from app.services.agrimap_service import AgriMapService

soil_map_bp = Blueprint('soil_map', __name__)
weather_service = WeatherService()
agrimap_service = AgriMapService()


@soil_map_bp.route('/modules/peta-data-tanah')
def peta_data_tanah():
    """Render soil data map page."""
    return render_template('modules/peta_data_tanah.html')


# ========== WEATHER API (existing) ==========

@soil_map_bp.route('/api/weather/current')
def get_current_weather():
    """Get current weather for coordinates."""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        return jsonify({'success': False, 'error': 'Missing lat/lon parameters'}), 400
    
    result = weather_service.get_current_weather(lat, lon)
    return jsonify(result)


@soil_map_bp.route('/api/weather/forecast')
def get_forecast():
    """Get weather forecast for coordinates."""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    days = request.args.get('days', default=7, type=int)
    
    if not lat or not lon:
        return jsonify({'success': False, 'error': 'Missing lat/lon parameters'}), 400
    
    result = weather_service.get_forecast(lat, lon, days)
    return jsonify(result)


@soil_map_bp.route('/api/weather/soil')
def get_soil_weather():
    """Get soil temperature and moisture."""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        return jsonify({'success': False, 'error': 'Missing lat/lon parameters'}), 400
    
    result = weather_service.get_soil_data(lat, lon)
    return jsonify(result)


@soil_map_bp.route('/api/weather/recommendations')
def get_recommendations():
    """Get agricultural recommendations based on weather."""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if not lat or not lon:
        return jsonify({'success': False, 'error': 'Missing lat/lon parameters'}), 400
    
    result = weather_service.get_agricultural_recommendations(lat, lon)
    return jsonify(result)


# ========== AGRIMAP API (new) ==========

# Polygon endpoints
@soil_map_bp.route('/api/agrimap/polygons', methods=['GET'])
def get_polygons():
    """Get all saved polygons."""
    try:
        polygons = agrimap_service.db.get_polygons()
        return jsonify({'success': True, 'data': polygons})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/polygon', methods=['POST'])
def save_polygon():
    """Save a new polygon."""
    try:
        data = request.get_json()
        
        required = ['name', 'coordinates', 'area_sqm']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        polygon = agrimap_service.db.save_polygon(
            name=data['name'],
            coordinates=data['coordinates'],
            area_sqm=data['area_sqm'],
            soil_type=data.get('soil_type'),
            ph=data.get('ph'),
            notes=data.get('notes')
        )
        
        return jsonify({'success': True, 'data': polygon})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/polygon/<polygon_id>', methods=['GET'])
def get_polygon(polygon_id):
    """Get polygon by ID with NPK summary."""
    try:
        result = agrimap_service.get_polygon_with_npk_summary(polygon_id)
        if result.get('success'):
            return jsonify(result)
        return jsonify(result), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/polygon/<polygon_id>', methods=['PUT'])
def update_polygon(polygon_id):
    """Update polygon data."""
    try:
        data = request.get_json()
        success = agrimap_service.db.update_polygon(polygon_id, data)
        
        if success:
            return jsonify({'success': True, 'message': 'Polygon updated'})
        return jsonify({'success': False, 'error': 'Polygon not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/polygon/<polygon_id>', methods=['DELETE'])
def delete_polygon(polygon_id):
    """Delete polygon."""
    try:
        success = agrimap_service.db.delete_polygon(polygon_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Polygon deleted'})
        return jsonify({'success': False, 'error': 'Polygon not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# NPK Data endpoints
@soil_map_bp.route('/api/agrimap/npk-data', methods=['POST'])
def save_npk_data():
    """Save NPK soil data."""
    try:
        data = request.get_json()
        
        required = ['latitude', 'longitude', 'n_value', 'p_value', 'k_value']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        npk_data = agrimap_service.db.save_npk_data(
            latitude=data['latitude'],
            longitude=data['longitude'],
            n_value=data['n_value'],
            p_value=data['p_value'],
            k_value=data['k_value'],
            polygon_id=data.get('polygon_id'),
            crop_type=data.get('crop_type'),
            soil_texture=data.get('soil_texture'),
            ph=data.get('ph'),
            soil_temperature=data.get('soil_temperature'),
            soil_moisture=data.get('soil_moisture'),
            notes=data.get('notes')
        )
        
        # Also analyze the NPK values
        analysis = agrimap_service.analyze_npk_values(
            data['n_value'],
            data['p_value'],
            data['k_value']
        )
        
        return jsonify({
            'success': True,
            'data': npk_data,
            'analysis': analysis
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/npk-data', methods=['GET'])
def get_npk_data():
    """Get NPK data, optionally filtered by polygon_id."""
    try:
        polygon_id = request.args.get('polygon_id')
        npk_data = agrimap_service.db.get_npk_data(polygon_id=polygon_id)
        return jsonify({'success': True, 'data': npk_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/npk-data/nearby', methods=['GET'])
def get_nearby_npk():
    """Get NPK data near a location."""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        radius = request.args.get('radius', default=1.0, type=float)
        
        if not lat or not lon:
            return jsonify({'success': False, 'error': 'Missing lat/lon'}), 400
        
        npk_data = agrimap_service.db.get_npk_by_location(lat, lon, radius)
        return jsonify({'success': True, 'data': npk_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/npk-data/<npk_id>', methods=['DELETE'])
def delete_npk_data(npk_id):
    """Delete NPK data."""
    try:
        success = agrimap_service.db.delete_npk_data(npk_id)
        
        if success:
            return jsonify({'success': True, 'message': 'NPK data deleted'})
        return jsonify({'success': False, 'error': 'NPK data not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Marker endpoints
@soil_map_bp.route('/api/agrimap/markers', methods=['GET'])
def get_markers():
    """Get markers, optionally filtered."""
    try:
        polygon_id = request.args.get('polygon_id')
        marker_type = request.args.get('type')
        
        markers = agrimap_service.db.get_markers(
            polygon_id=polygon_id,
            marker_type=marker_type
        )
        return jsonify({'success': True, 'data': markers})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/marker', methods=['POST'])
def add_marker():
    """Add a new marker."""
    try:
        data = request.get_json()
        
        required = ['type', 'latitude', 'longitude', 'title']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        marker = agrimap_service.db.add_marker(
            marker_type=data['type'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            title=data['title'],
            description=data.get('description'),
            polygon_id=data.get('polygon_id')
        )
        
        return jsonify({'success': True, 'data': marker})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/marker/<marker_id>', methods=['DELETE'])
def delete_marker(marker_id):
    """Delete marker."""
    try:
        success = agrimap_service.db.delete_marker(marker_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Marker deleted'})
        return jsonify({'success': False, 'error': 'Marker not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Analysis endpoints
@soil_map_bp.route('/api/agrimap/analyze-npk', methods=['POST'])
def analyze_npk():
    """Analyze NPK values."""
    try:
        data = request.get_json()
        
        required = ['n_value', 'p_value', 'k_value']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400
        
        analysis = agrimap_service.analyze_npk_values(
            data['n_value'],
            data['p_value'],
            data['k_value']
        )
        
        return jsonify({'success': True, 'analysis': analysis})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/crop-suitability', methods=['GET'])
def get_crop_suitability():
    """Get crop suitability for a location."""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        n = request.args.get('n', type=float)
        p = request.args.get('p', type=float)
        k = request.args.get('k', type=float)
        
        if not lat or not lon:
            return jsonify({'success': False, 'error': 'Missing lat/lon'}), 400
        
        result = agrimap_service.get_crop_suitability(lat, lon, n, p, k)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# Integration endpoints
@soil_map_bp.route('/api/agrimap/fertilizer-data/<polygon_id>', methods=['GET'])
def get_fertilizer_data(polygon_id):
    """Get data for fertilizer calculator integration."""
    try:
        result = agrimap_service.prepare_fertilizer_data(polygon_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/heatmap-data', methods=['GET'])
def get_heatmap_data():
    """Get NPK heatmap data for visualization."""
    try:
        heatmap_data = agrimap_service.generate_npk_heatmap_data()
        return jsonify({'success': True, 'data': heatmap_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@soil_map_bp.route('/api/agrimap/statistics', methods=['GET'])
def get_statistics():
    """Get overall AgriMap statistics."""
    try:
        stats = agrimap_service.db.get_statistics()
        return jsonify({'success': True, 'data': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
