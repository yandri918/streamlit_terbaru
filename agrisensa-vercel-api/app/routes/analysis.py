"""Analysis routes for leaf and soil analysis."""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, limiter
from app.models.npk_reading import NpkReading
from app.services.analysis_service import AnalysisService
from werkzeug.utils import secure_filename
from inference_sdk import InferenceHTTPClient
import base64
import os
import uuid

analysis_bp = Blueprint('analysis', __name__)


@analysis_bp.route('/bwd', methods=['POST'])
@limiter.limit("20 per hour")
def analyze_bwd():
    """Analyze leaf image for BWD (Blade Width Detection) score."""
    try:
        image_bytes = None
        
        # Prefer form-data file
        if 'file' in request.files:
            file = request.files['file']
            if file.filename == '':
                return jsonify({'success': False, 'error': 'No file selected'}), 400
            image_bytes = file.read()
        else:
            # Fallback: JSON with base64 image
            data = request.get_json(silent=True) or {}
            b64 = data.get('image_base64')
            if b64:
                try:
                    image_bytes = base64.b64decode(b64.split(',')[-1])
                except Exception:
                    return jsonify({'success': False, 'error': 'Invalid base64 image'}), 400
        
        if not image_bytes:
            return jsonify({'success': False, 'error': 'No image provided (file or image_base64)'}), 400
        
        result = AnalysisService.analyze_leaf_image(image_bytes)
        
        if result is None:
            return jsonify({'success': False, 'message': 'No leaf-like area detected (green mask empty)'}), 400
        
        return jsonify({
            'success': True,
            'bwd_score': result['bwd_score'],
            'bwd_status': result['bwd_status'],
            'avg_hue_value': result['avg_hue'],
            'confidence_percent': result['confidence'],
            'disease_analysis': result['disease_analysis'],
            'recommendation': result['recommendation']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Analysis failed',
            'message': str(e)
        }), 500


@analysis_bp.route('/npk', methods=['POST'])
@limiter.limit("30 per hour")
def analyze_npk():
    """Analyze NPK values and store reading."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['n_value', 'p_value', 'k_value']
        if not isinstance(data, dict) or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required NPK values'
            }), 400
        
        # Get user ID if authenticated
        user_id = None
        try:
            user_id = get_jwt_identity()
        except:
            pass  # Allow anonymous analysis
        
        # Create NPK reading
        reading = NpkReading(
            user_id=user_id,
            n_value=int(data['n_value']),
            p_value=int(data['p_value']),
            k_value=int(data['k_value']),
            ph_value=data.get('ph_value'),
            temperature=data.get('temperature'),
            humidity=data.get('humidity'),
            location=data.get('location')
        )
        
        # Analyze NPK values
        analysis = AnalysisService.analyze_npk_values(
            reading.n_value,
            reading.p_value,
            reading.k_value
        )
        
        reading.analysis_result = analysis
        
        db.session.add(reading)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'reading_id': reading.id,
            'analysis': analysis
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'NPK analysis failed',
            'message': str(e)
        }), 500


@analysis_bp.route('/npk/history', methods=['GET'])
@jwt_required()
def get_npk_history():
    """Get NPK reading history for current user."""
    try:
        user_id = get_jwt_identity()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Query readings
        readings = NpkReading.query.filter_by(user_id=user_id)\
            .order_by(NpkReading.timestamp.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'readings': [r.to_dict() for r in readings.items],
            'total': readings.total,
            'page': readings.page,
            'pages': readings.pages
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get NPK history',
            'message': str(e)
        }), 500


@analysis_bp.route('/disease-advanced', methods=['POST'])
@limiter.limit("20 per hour")
def analyze_disease_advanced():
    """Analyze plant disease using Roboflow AI."""
    try:
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400
        
        # Check file extension
        allowed_extensions = {'png', 'jpg', 'jpeg'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only PNG, JPG, JPEG allowed.'
            }), 400
        
        # Save temporary file
        temp_folder = current_app.config.get('TEMP_IMAGE_FOLDER', 'uploads/temp_images')
        os.makedirs(temp_folder, exist_ok=True)
        
        filename = secure_filename(f"{uuid.uuid4()}.jpg")
        temp_path = os.path.join(temp_folder, filename)
        file.save(temp_path)
        
        try:
            # Initialize Roboflow client
            roboflow_api_key = os.environ.get('ROBOFLOW_API_KEY', 'your_roboflow_key_here')
            client = InferenceHTTPClient(
                api_url="https://serverless.roboflow.com",
                api_key=roboflow_api_key
            )
            
            # Run workflow
            result = client.run_workflow(
                workspace_name="andriyanto39",
                workflow_id="detect-and-classify",
                images={"image": temp_path},
                use_cache=True
            )
            
            return jsonify({
                'success': True,
                'data': result
            }), 200
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
                current_app.logger.info(f"Temporary file removed: {temp_path}")
        
    except Exception as e:
        current_app.logger.error(f"Error in /disease-advanced: {e}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Disease analysis failed',
            'message': str(e)
        }), 500
