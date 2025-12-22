"""Legacy routes for backward compatibility with old frontend."""
from flask import Blueprint, request, jsonify, send_from_directory, current_app, render_template
from werkzeug.utils import secure_filename
import os
import uuid
from inference_sdk import InferenceHTTPClient
from app.services.analysis_service import AnalysisService
from app.services.recommendation_service import RecommendationService
from app.services.knowledge_service import KnowledgeService
from app.services.market_service import MarketService
from app.services.ml_service import MLService
from app.services.chatbot_service import ChatbotService
from app.models.npk_reading import NpkReading
from app import db

legacy_bp = Blueprint('legacy', __name__)

# Initialize services
analysis_service = AnalysisService()
recommendation_service = RecommendationService()
knowledge_service = KnowledgeService()
market_service = MarketService()
ml_service = MLService()
chatbot_service = ChatbotService()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads', 'pdfs')
TEMP_IMAGE_FOLDER = os.path.join(BASE_DIR, 'uploads', 'temp_images')
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@legacy_bp.route('/analyze', methods=['POST'])
def analyze_bwd_endpoint():
    """Legacy BWD analysis endpoint."""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'Tidak ada file'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'File tidak dipilih'}), 400
        
        result = analysis_service.analyze_leaf_image(file.read())
        
        if result is None:
            return jsonify({'success': False, 'message': 'Tidak ada objek daun yang terdeteksi'}), 400
        
        return jsonify({
            'success': True,
            'bwd_score': result['bwd_score'],
            'bwd_status': result.get('bwd_status', 'N/A'),
            'avg_hue_value': result['avg_hue'],
            'confidence_percent': result['confidence'],
            'disease_analysis': result.get('disease_analysis', {}),
            'recommendation': result.get('recommendation', '')
        }), 200
            
    except Exception as e:
        current_app.logger.error(f"Error in /analyze: {e}", exc_info=True)
        return jsonify({'error': 'Kesalahan internal saat menganalisis gambar.'}), 500


@legacy_bp.route('/recommendation', methods=['POST'])
def recommendation_endpoint():
    """Fertilizer recommendation endpoint - supports multiple input formats."""
    try:
        data = request.get_json()
        
        # Format 1: New combined module (ph_tanah, skor_bwd, kelembaban_tanah, umur_tanaman_hari)
        if 'ph_tanah' in data and 'skor_bwd' in data:
            # Use the complex recommendation service
            recommendation = recommendation_service.get_fertilizer_recommendation(data)
            return jsonify({'success': True, 'recommendation': recommendation})
        
        # Format 2: Simplified form (ph, area_sqm, commodity)
        elif 'ph' in data and 'area_sqm' in data and 'commodity' in data:
            # Use the calculate_fertilizer_dosage method for simplified input
            ph = float(data['ph'])
            area_sqm = float(data['area_sqm'])
            commodity = data['commodity'].lower()
            
            result = recommendation_service.calculate_fertilizer_dosage(
                commodity=commodity,
                area_sqm=area_sqm,
                ph_tanah=ph
            )
            
            if not result:
                return jsonify({
                    'success': False,
                    'error': f'Data untuk komoditas "{commodity}" tidak ditemukan. Silakan pilih Padi, Jagung, atau Kedelai.'
                }), 404
            
            
            # Format the recommendation as structured data for better display
            recommendation_data = {
                'commodity_name': result['commodity_name'],
                'area_sqm': result['area_sqm'],
                'area_ha': round(result['area_sqm']/10000, 4),
                'ph': ph,
                'organik': result['organik'],
                'anorganik': result['anorganik'],
                'perbaikan_tanah': result['perbaikan_tanah'],
                'ph_warning': ph < 6.0
            }
            
            return jsonify({
                'success': True,
                'recommendation': recommendation_data
            })
        
        # Format 3: Original complex recommendation for backward compatibility
        else:
            recommendation = recommendation_service.get_fertilizer_recommendation(data)
            return jsonify({'success': True, 'recommendation': recommendation})
        
    except Exception as e:
        current_app.logger.error(f"Error in /recommendation: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat menghitung rekomendasi.'}), 500


@legacy_bp.route('/analyze-npk', methods=['POST'])
def analyze_npk_endpoint():
    """Legacy NPK analysis endpoint."""
    try:
        data = request.get_json()
        n, p, k = int(data['n_value']), int(data['p_value']), int(data['k_value'])
        
        # Analyze NPK values
        analysis = analysis_service.analyze_npk_values(n, p, k)
        
        # Try to save to database if available
        if current_app.config.get('DATABASE_AVAILABLE', False):
            try:
                user_id = None  # Hindari FK error jika tabel users tidak tersedia
                reading = NpkReading(n_value=n, p_value=p, k_value=k, user_id=user_id)
                reading.analysis_result = analysis
                db.session.add(reading)
                db.session.commit()
                current_app.logger.info("NPK reading saved to database")
            except Exception as db_error:
                current_app.logger.warning(f"Failed to save NPK reading to database: {db_error}")
                # Continue without saving - don't fail the request
                db.session.rollback()
        
        return jsonify({
            'success': True,
            'analysis': analysis
        }), 201
    except Exception as e:
        current_app.logger.error(f"Error in /analyze-npk: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat menganalisis NPK.'}), 500


@legacy_bp.route('/get-prices', methods=['POST'])
def get_prices_endpoint():
    """Legacy market prices endpoint."""
    try:
        data = request.get_json()
        commodity_id = data.get('commodity')
        price_data = market_service.get_current_prices(commodity_id)
        if not price_data:
            return jsonify({'success': False, 'error': 'Data harga tidak ditemukan'}), 404
        return jsonify({'success': True, 'data': price_data})
    except Exception as e:
        current_app.logger.error(f"Error in /get-prices: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal pada data harga.'}), 500


@legacy_bp.route('/get-knowledge', methods=['POST'])
def get_knowledge_endpoint():
    """Legacy knowledge base endpoint."""
    try:
        data = request.get_json()
        commodity_id = data.get('commodity')
        knowledge_data = knowledge_service.get_crop_knowledge(commodity_id)
        if not knowledge_data:
            return jsonify({'success': False, 'error': 'Informasi tidak ditemukan'}), 404
        return jsonify({'success': True, 'data': knowledge_data})
    except Exception as e:
        current_app.logger.error(f"Error in /get-knowledge: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal pada basis pengetahuan.'}), 500


@legacy_bp.route('/commodities', methods=['GET'])
def get_commodities_endpoint():
    """Legacy commodities list endpoint."""
    try:
        commodities = knowledge_service.get_all_commodities()
        return jsonify({'success': True, 'data': commodities})
    except Exception as e:
        current_app.logger.error(f"Error in /commodities: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat memuat daftar komoditas.'}), 500


@legacy_bp.route('/calculate-fertilizer', methods=['POST'])
def calculate_fertilizer_endpoint():
    """Legacy fertilizer calculator endpoint."""
    try:
        data = request.get_json()
        commodity_id = data.get('commodity')
        area_sqm = float(data.get('area_sqm', 0))
        ph_tanah = float(data.get('ph_tanah', 7.0))
        
        soil_texture = data.get('soil_texture', 'lempung')
        target_yield = float(data.get('target_yield', 0))
        inventory = data.get('inventory', [])
        previous_crop = data.get('previous_crop', 'bukan_legum')
        
        if not commodity_id or area_sqm <= 0:
            return jsonify({'success': False, 'error': 'Input tidak valid.'}), 400
            
        dosage_data = recommendation_service.calculate_fertilizer_dosage(
            commodity_id, area_sqm, ph_tanah, 
            soil_texture=soil_texture, 
            target_yield=target_yield, 
            inventory=inventory, 
            previous_crop=previous_crop
        )
        
        if not dosage_data:
            return jsonify({'success': False, 'error': 'Data dosis tidak ditemukan.'}), 404
            
        return jsonify({
            'success': True,
            'data': {
                'perbaikan_tanah': dosage_data.get('perbaikan_tanah', {}),
                'organik': dosage_data.get('organik', {}),
                'anorganik': dosage_data.get('anorganik', {})
            },
            'commodity_name': dosage_data.get('commodity_name'),
            'area_sqm': dosage_data.get('area_sqm')
        })
    except Exception as e:
        current_app.logger.error(f"Error in /calculate-fertilizer: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat menghitung.'}), 500


@legacy_bp.route('/upload-pdf', methods=['POST'])
def upload_pdf_endpoint():
    """Legacy PDF upload endpoint."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Tidak ada file'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'File tidak dipilih'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return jsonify({'success': True, 'message': f'File {filename} berhasil diunggah.'})
    return jsonify({'success': False, 'error': 'Tipe file tidak diizinkan. Harap unggah PDF.'}), 400


@legacy_bp.route('/get-pdfs', methods=['GET'])
def get_pdfs_endpoint():
    """Legacy get PDFs list endpoint."""
    try:
        files = [f for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        return jsonify({'success': True, 'files': sorted(files)})
    except Exception as e:
        current_app.logger.error(f"Error in /get-pdfs: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Gagal memuat daftar dokumen.'}), 500


@legacy_bp.route('/view-pdf/<path:filename>')
def view_pdf_endpoint(filename):
    """Legacy view PDF endpoint."""
    return send_from_directory(UPLOAD_FOLDER, filename)


@legacy_bp.route('/get-integrated-recommendation', methods=['POST'])
def get_integrated_recommendation_endpoint():
    """Legacy integrated recommendation endpoint."""
    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({'success': False, 'error': 'Payload JSON tidak valid'}), 400
        ketinggian = data.get('ketinggian')
        iklim = data.get('iklim')
        fase = data.get('fase')
        masalah = data.get('masalah')
        recommendation_data = recommendation_service.get_integrated_recommendation(ketinggian, iklim, fase, masalah)
        return jsonify({'success': True, 'data': recommendation_data})
    except Exception as e:
        current_app.logger.error(f"Error in /get-integrated-recommendation: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat memproses rekomendasi.'}), 500


@legacy_bp.route('/get-spraying-recommendation', methods=['POST'])
def get_spraying_recommendation_endpoint():
    """Get comprehensive pest/disease information."""
    try:
        from app.data.pest_disease_db import PestDiseaseDatabase
        
        data = request.get_json()
        pest = data.get('pest') or data.get('commodity')
        if not pest:
            return jsonify({'success': False, 'error': 'Hama/penyakit tidak dipilih'}), 400
        
        pest_data = PestDiseaseDatabase.get_pest_detail(pest)
        if not pest_data:
            return jsonify({'success': False, 'error': 'Data tidak ditemukan.'}), 404
            
        # Transform data if it doesn't have the expected structure
        if 'strategy' not in pest_data:
            # Generate cycles from chemical control methods
            cycles = []
            chemicals = pest_data.get('control_methods', {}).get('chemical', [])
            for i, chem in enumerate(chemicals):
                # Simple parsing logic
                parts = chem.split(':')
                weeks = parts[0] if len(parts) > 1 else f"Tahap {i+1}"
                desc = parts[1] if len(parts) > 1 else chem
                
                cycles.append({
                    "weeks": weeks.strip(),
                    "level": "Intervensi Kimia",
                    "active_ingredient": desc.strip(),
                    "irac_code": "Lihat label kemasan", # Placeholder if not parsed
                    "sop": "Semprot dengan nozzle kabut, gunakan APD lengkap."
                })
                
            transformed_data = {
                "strategy": {
                    "name": f"Strategi Pengendalian {pest_data['name']}",
                    "description": pest_data.get('damage', 'Strategi pengendalian hama terpadu.'),
                    "cycles": cycles
                },
                "protocol": {
                    "title": "Protokol Pencegahan & Kultur Teknis",
                    "steps": pest_data.get('prevention', []) + pest_data.get('control_methods', {}).get('cultural', [])
                }
            }
            return jsonify({'success': True, 'data': transformed_data})
            
        return jsonify({'success': True, 'data': pest_data})
    except Exception as e:
        current_app.logger.error(f"Error in /get-spraying-recommendation: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat memproses rekomendasi.'}), 500


@legacy_bp.route('/get-pest-list', methods=['GET'])
def get_pest_list_endpoint():
    """Get list of all pests and diseases."""
    try:
        from app.data.pest_disease_db import PestDiseaseDatabase
        
        pest_list = PestDiseaseDatabase.get_pest_list()
        return jsonify({'success': True, 'data': pest_list})
    except Exception as e:
        current_app.logger.error(f"Error in /get-pest-list: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal.'}), 500


@legacy_bp.route('/get-pest-detail', methods=['POST'])
def get_pest_detail_endpoint():
    """Get detailed information for a specific pest/disease (raw data)."""
    try:
        from app.data.pest_disease_db import PestDiseaseDatabase
        
        data = request.get_json()
        pest_id = data.get('pest')
        if not pest_id:
            return jsonify({'success': False, 'error': 'Hama/penyakit tidak dipilih'}), 400
        
        pest_data = PestDiseaseDatabase.get_pest_detail(pest_id)
        if not pest_data:
            return jsonify({'success': False, 'error': 'Data tidak ditemukan.'}), 404
            
        return jsonify({'success': True, 'data': pest_data})
    except Exception as e:
        current_app.logger.error(f"Error in /get-pest-detail: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal.'}), 500


@legacy_bp.route('/get-ticker-prices', methods=['GET'])
def get_ticker_prices_endpoint():
    """Legacy ticker prices endpoint."""
    try:
        # Use timeout untuk menghindari hang
        import signal
        
        # Get ticker data dengan fallback cepat
        ticker_data = market_service.get_ticker_prices()
        
        # Pastikan data dalam format yang benar
        if not ticker_data:
            # Fallback data
            ticker_data = [
                {"name": "Cabai Merah", "price": 45000, "unit": "kg"},
                {"name": "Bawang Merah", "price": 30000, "unit": "kg"},
                {"name": "Jagung Pipilan", "price": 5500, "unit": "kg"},
                {"name": "Beras Medium", "price": 12000, "unit": "kg"}
            ]
        
        return jsonify({'success': True, 'data': ticker_data})
    except Exception as e:
        current_app.logger.error(f"Error in /get-ticker-prices: {e}", exc_info=True)
        # Return fallback data instead of error
        fallback_data = [
            {"name": "Cabai Merah", "price": 45000, "unit": "kg"},
            {"name": "Bawang Merah", "price": 30000, "unit": "kg"},
            {"name": "Jagung Pipilan", "price": 5500, "unit": "kg"},
            {"name": "Beras Medium", "price": 12000, "unit": "kg"}
        ]
        return jsonify({'success': True, 'data': fallback_data})




@legacy_bp.route('/get-commodity-guide', methods=['POST'])
def get_commodity_guide_endpoint():
    """Legacy commodity guide endpoint."""
    try:
        data = request.get_json()
        commodity = data.get('commodity')
        guide = knowledge_service.get_commodity_guide(commodity)
        if not guide:
            return jsonify({'success': False, 'error': 'Panduan untuk komoditas ini belum tersedia.'}), 404
        return jsonify({'success': True, 'data': guide})
    except Exception as e:
        current_app.logger.error(f"Error in /get-commodity-guide: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat memuat panduan.'}), 500


@legacy_bp.route('/get-ph-info', methods=['GET'])
def get_ph_info_endpoint():
    """Legacy pH knowledge base endpoint."""
    try:
        info = knowledge_service.get_ph_knowledge()
        return jsonify({'success': True, 'data': info})
    except Exception as e:
        current_app.logger.error(f"Error in /get-ph-info: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat memuat informasi pH.'}), 500


@legacy_bp.route('/recommend-crop', methods=['POST'])
def recommend_crop_endpoint():
    try:
        data = request.get_json()
        prediction = ml_service.recommend_crop(data)
        return jsonify({'success': True, 'recommended_crop': prediction})
    except Exception as e:
        current_app.logger.error(f"Error di /recommend-crop: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat membuat rekomendasi tanaman.'}), 500


@legacy_bp.route('/predict-yield', methods=['POST'])
def predict_yield_endpoint():
    """Legacy yield prediction endpoint."""
    try:
        data = request.get_json()
        prediction = ml_service.predict_yield(data)
        return jsonify({'success': True, 'predicted_yield_ton_ha': prediction})
    except Exception as e:
        current_app.logger.error(f"Error di /predict-yield: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat membuat prediksi panen.'}), 500


@legacy_bp.route('/predict-yield-advanced', methods=['POST'])
def predict_yield_advanced_endpoint():
    """Legacy XAI yield prediction endpoint."""
    try:
        data = request.get_json()
        result = ml_service.predict_yield_advanced(data)
        return jsonify({'success': True, **result})
    except Exception as e:
        current_app.logger.error(f"Error di /predict-yield-advanced: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat membuat prediksi XAI.'}), 500


@legacy_bp.route('/calculate-fertilizer-bags', methods=['POST'])
def calculate_fertilizer_bags_endpoint():
    """Legacy fertilizer conversion endpoint."""
    try:
        data = request.get_json()
        result = ml_service.calculate_fertilizer_bags(
            data['nutrient_needed'],
            float(data['nutrient_amount_kg']),
            data['fertilizer_type']
        )
        if not result:
            return jsonify({'success': False, 'error': 'Kalkulasi gagal. Periksa tipe pupuk dan nutrisi.'}), 400
        return jsonify({'success': True, 'required_fertilizer_kg': result['required_kg'], **data})
    except Exception as e:
        current_app.logger.error(f"Error di /calculate-fertilizer-bags: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat menghitung.'}), 500


@legacy_bp.route('/get-diagnostic-tree', methods=['GET'])
def get_diagnostic_tree_endpoint():
    """Legacy diagnostic tree endpoint."""
    try:
        tree = knowledge_service.get_diagnostic_tree()
        return jsonify({'success': True, 'data': tree})
    except Exception as e:
        current_app.logger.error(f"Error di /get-diagnostic-tree: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat memuat data diagnostik.'}), 500


@legacy_bp.route('/generate-yield-plan', methods=['POST'])
def generate_yield_plan_endpoint():
    """Legacy yield planning endpoint with commodity support."""
    try:
        data = request.get_json()
        commodity = data.get('commodity', 'umum')
        target_yield = float(data.get('target_yield', 0))
        
        if target_yield <= 0:
            return jsonify({'success': False, 'error': 'Target hasil panen harus lebih dari 0.'}), 400
        
        plan = ml_service.generate_yield_plan(commodity=commodity, target_yield_ton_ha=target_yield)
        if not plan:
            return jsonify({'success': False, 'error': 'Tidak ditemukan data yang cocok untuk target panen tersebut.'}), 404
        return jsonify({'success': True, 'plan': plan})
    except Exception as e:
        current_app.logger.error(f"Error di /generate-yield-plan: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat membuat rencana panen.'}), 500


# --- ENDPOINT BARU UNTUK MODUL 20, 21, & 22 ---

@legacy_bp.route('/analyze-research', methods=['POST'])
def analyze_research_endpoint():
    """Endpoint for agronomy research analysis (Modul 22)."""
    try:
        from app.services.research_service import ResearchService
        data = request.get_json()
        
        # Validation
        if not data or 'parameters' not in data:
            return jsonify({'success': False, 'error': 'Data tidak lengkap.'}), 400
            
        results = ResearchService.analyze_ral(data)
        return jsonify({'success': True, 'data': results})
    except Exception as e:
        current_app.logger.error(f"Error in /analyze-research: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat analisis statistik.'}), 500

@legacy_bp.route('/modules/asisten_penelitian')
def asisten_penelitian_page():
    """Render Asisten Penelitian page."""
    return render_template('modules/asisten_penelitian.html')

@legacy_bp.route('/modules/analisis_npk_manual')
def analisis_npk_manual_page():
    """Render Analisis NPK Manual page."""
    return render_template('modules/analisis_npk_manual.html')



@legacy_bp.route('/predict-success', methods=['POST'])
def predict_success_endpoint():
    """Legacy success probability endpoint (Modul 21)."""
    try:
        data = request.get_json()
        result = ml_service.predict_success(data)
        return jsonify({'success': True, **result})
    except Exception as e:
        current_app.logger.error(f"Error di /predict-success: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat membuat analisis risiko.'}), 500


@legacy_bp.route('/analyze-disease-advanced', methods=['POST'])
def analyze_disease_advanced_endpoint():
    """Legacy advanced disease analysis endpoint (Modul 20)."""
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'Tidak ada file yang diunggah.'}), 400
    
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'Tipe file tidak valid.'}), 400

    temp_path = None
    try:
        filename = secure_filename(f"{uuid.uuid4()}.jpg")
        temp_path = os.path.join(TEMP_IMAGE_FOLDER, filename)
        file.save(temp_path)
        current_app.logger.info(f"File sementara disimpan di: {temp_path}")

        client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key=os.environ.get('ROBOFLOW_API_KEY', 'your_roboflow_key_here')
        )

        current_app.logger.info("Menjalankan workflow Roboflow...")
        result = client.run_workflow(
            workspace_name="andriyanto39",
            workflow_id="detect-and-classify",
            images={"image": temp_path},
            use_cache=True
        )
        current_app.logger.info("Workflow Roboflow berhasil dijalankan.")
        
        return jsonify({'success': True, 'data': result})

    except Exception as e:
        current_app.logger.error(f"Error di /analyze-disease-advanced: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal saat berkomunikasi dengan layanan AI.'}), 500
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            current_app.logger.info(f"File sementara dihapus: {temp_path}")


@legacy_bp.route('/get-fruit-list', methods=['GET'])
def get_fruit_list_endpoint():
    """Get list of all available fruits."""
    try:
        from app.services.fruit_service import FruitService
        fruits = FruitService.get_fruit_list()
        return jsonify({'success': True, 'data': fruits})
    except Exception as e:
        current_app.logger.error(f"Error in /get-fruit-list: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@legacy_bp.route('/get-fruit-info', methods=['POST'])
def get_fruit_info_endpoint():
    """Get comprehensive information for specific fruit."""
    try:
        from app.services.fruit_service import FruitService
        
        data = request.get_json()
        fruit_id = data.get('fruit_id')
        
        if not fruit_id:
            return jsonify({'success': False, 'error': 'fruit_id is required'}), 400
        
        fruit_info = FruitService.get_fruit_info(fruit_id)
        
        if not fruit_info:
            return jsonify({'success': False, 'error': 'Fruit not found'}), 404
        
        return jsonify({'success': True, 'data': fruit_info})
        
    except Exception as e:
        current_app.logger.error(f"Error in /get-fruit-info: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal server'}), 500


@legacy_bp.route('/get-commodity-list', methods=['GET'])
def get_commodity_list_endpoint():
    """Get list of all available commodities for the encyclopedia."""
    try:
        commodities = knowledge_service.get_all_commodities()
        return jsonify({'success': True, 'data': commodities})
    except Exception as e:
        current_app.logger.error(f"Error in /get-commodity-list: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal.'}), 500


@legacy_bp.route('/get-historical-prices', methods=['POST'])
def get_historical_prices_endpoint():
    """Get historical prices for a commodity."""
    try:
        data = request.get_json()
        commodity = data.get('commodity')
        days = int(data.get('range', 30))  # Default to 30 days if not specified
        
        if not commodity:
            return jsonify({'success': False, 'error': 'Komoditas tidak dipilih'}), 400
            
        history = market_service.get_historical_prices(commodity, days=days)
        if not history:
             return jsonify({'success': False, 'error': 'Data tidak ditemukan'}), 404
             
        return jsonify({'success': True, 'data': history})
    except Exception as e:
        current_app.logger.error(f"Error in /get-historical-prices: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal.'}), 500


@legacy_bp.route('/predict-price-trend', methods=['POST'])
def predict_price_trend_endpoint():
    """Predict price trend for a commodity."""
    try:
        data = request.get_json()
        commodity = data.get('commodity')
        days = data.get('days', 7)
        
        if not commodity:
            return jsonify({'success': False, 'error': 'Komoditas tidak dipilih'}), 400
            
        forecast = market_service.get_forecast(commodity, days=days)
        if not forecast:
             return jsonify({'success': False, 'error': 'Gagal membuat prediksi'}), 500
             
        return jsonify({'success': True, 'data': forecast})
    except Exception as e:
        current_app.logger.error(f"Error in /predict-price-trend: {e}", exc_info=True)
        return jsonify({'success': False, 'error': 'Kesalahan internal.'}), 500


@legacy_bp.route('/chat', methods=['POST'])
def chat_endpoint():
    """Chat with AgriBot (Gemini)."""
    try:
        data = request.get_json()
        message = data.get('message')
        
        if not message:
            return jsonify({'success': False, 'error': 'Pesan tidak boleh kosong'}), 400
            
        response = chatbot_service.get_response(message)
        return jsonify({'success': True, 'response': response})
    except Exception as e:
        current_app.logger.error(f"Error in /chat: {e}", exc_info=True)
        return jsonify({'success': False, 'error': f'Kesalahan internal: {str(e)}'}), 500
