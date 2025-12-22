"""Main routes for AgriSensa API."""
from flask import Blueprint, render_template, jsonify, current_app

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/home')
def home():
    """Render the new landing page with module overview."""
    return render_template('home.html')

@main_bp.route('/dashboard')
def dashboard():
    """Redirect dashboard to home page."""
    return render_template('home.html')



@main_bp.route('/modules/analisis-npk-manual')
def analisis_npk_manual():
    return render_template('modules/analisis_npk_manual.html')

@main_bp.route('/modules/katalog-pupuk')
def katalog_pupuk():
    return render_template('modules/katalog_pupuk.html')

@main_bp.route('/fruit-guide')
def fruit_guide():
    return render_template('fruit_guide.html')

@main_bp.route('/modules/analis-risiko-keberhasilan-ai')
def analis_risiko_keberhasilan_ai():
    return render_template('modules/analis_risiko_keberhasilan_ai.html')

@main_bp.route('/modules/analisis-tren-harga')
def analisis_tren_harga():
    return render_template('modules/analisis_tren_harga.html')

@main_bp.route('/modules/asisten-agronomi')
def asisten_agronomi():
    return render_template('modules/asisten_agronomi.html')

@main_bp.route('/modules/basis-pengetahuan-budidaya')
def basis_pengetahuan_budidaya():
    return render_template('modules/basis_pengetahuan_budidaya.html')

@main_bp.route('/modules/pesticide-knowledge')
def pesticide_knowledge():
    return render_template('modules/pesticide_knowledge.html')

@main_bp.route('/modules/pestisida-nabati')
def pestisida_nabati():
    return render_template('modules/pestisida_nabati.html')

@main_bp.route('/modules/bwd-analysis')
def bwd_analysis():
    return render_template('modules/bwd_analysis.html')

@main_bp.route('/modules/crop-rec')
def crop_rec():
    return render_template('modules/crop_rec.html')

@main_bp.route('/modules/dasbor-rekomendasi-terpadu')
def dasbor_rekomendasi_terpadu():
    return render_template('modules/dasbor_rekomendasi_terpadu.html')

@main_bp.route('/modules/diagnostik-gejala-cerdas')
def diagnostik_gejala_cerdas():
    return render_template('modules/diagnostik_gejala_cerdas.html')

@main_bp.route('/modules/dokter-tanaman-canggih-roboflow-ai')
def dokter_tanaman_canggih_roboflow_ai():
    return render_template('modules/dokter_tanaman_canggih_roboflow_ai.html')

@main_bp.route('/modules/dokter-tanaman')
def dokter_tanaman():
    return render_template('modules/dokter_tanaman.html')

@main_bp.route('/modules/dokter-tanaman-asisten-agronomi')
def dokter_tanaman_asisten_agronomi():
    return render_template('modules/dokter_tanaman_asisten_agronomi.html')

@main_bp.route('/modules/ensiklopedia-komoditas-cerdas')
def ensiklopedia_komoditas_cerdas():
    return render_template('modules/ensiklopedia_komoditas_cerdas.html')

@main_bp.route('/modules/fertilizer-rec')
def fertilizer_rec():
    return render_template('modules/fertilizer_rec.html')

@main_bp.route('/modules/intelijen-harga-pasar')
def intelijen_harga_pasar():
    return render_template('modules/intelijen_harga_pasar.html')

@main_bp.route('/modules/intelijen-prediktif-xai')
def intelijen_prediktif_xai():
    return render_template('modules/intelijen_prediktif_xai.html')

@main_bp.route('/modules/kalkulator-konversi-pupuk')
def kalkulator_konversi_pupuk():
    return render_template('modules/kalkulator_konversi_pupuk.html')

@main_bp.route('/modules/kalkulator-pupuk-holistik')
def kalkulator_pupuk_holistik():
    return render_template('modules/kalkulator_pupuk_holistik.html')

@main_bp.route('/modules/perencana-hasil-panen-ai')
def perencana_hasil_panen_ai():
    return render_template('modules/perencana_hasil_panen_ai.html')

@main_bp.route('/modules/pest-guide')
def pest_guide():
    return render_template('modules/pest_guide.html')

@main_bp.route('/modules/prediksi-hasil-panen-cerdas')
def prediksi_hasil_panen_cerdas():
    return render_template('modules/prediksi_hasil_panen_cerdas.html')

@main_bp.route('/modules/price-intel')
def price_intel():
    return render_template('modules/price_intel.html')

@main_bp.route('/modules/pusat-pengetahuan-pertanian')
def pusat_pengetahuan_pertanian():
    return render_template('modules/pusat_pengetahuan_pertanian.html')

@main_bp.route('/modules/pusat-pengetahuan-ph-tanah')
def pusat_pengetahuan_ph_tanah():
    return render_template('modules/pusat_pengetahuan_ph_tanah.html')

@main_bp.route('/modules/pustaka-dokumen')
def pustaka_dokumen():
    return render_template('modules/pustaka_dokumen.html')

@main_bp.route('/modules/rekomendasi-tanaman-cerdas-agrimap-ai')
def rekomendasi_tanaman_cerdas_agrimap_ai():
    return render_template('modules/rekomendasi_tanaman_cerdas_agrimap_ai.html')

@main_bp.route('/modules/strategi-penyemprotan-cerdas')
def strategi_penyemprotan_cerdas():
    return render_template('modules/strategi_penyemprotan_cerdas.html')


@main_bp.route('/modules-coming-soon')
@main_bp.route('/coming-soon')
def modules_coming_soon():
    """Display 15+ additional modules coming soon."""
    return render_template('modules_coming_soon.html')


@main_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'message': 'AgriSensa API is running'
    }), 200


@main_bp.route('/api/info')
def api_info():
    """API information endpoint."""
    return jsonify({
        'success': True,
        'api_name': 'AgriSensa API',
        'version': '2.0.0',
        'description': 'Smart Agriculture Platform for Indonesian Farmers',
        'endpoints': {
            'auth': '/api/auth',
            'analysis': '/api/analysis',
            'recommendation': '/api/recommendation',
            'knowledge': '/api/knowledge',
            'market': '/api/market',
            'ml': '/api/ml'
        }
    }), 200


@main_bp.route('/test')
def test_page():
    """Render test page for debugging."""
    return render_template('test.html')



@main_bp.route('/modules/chatbot')
def chatbot():
    return render_template('modules/chatbot.html')


@main_bp.route('/sw.js')
def service_worker():
    """Serve the service worker from root."""
    return current_app.send_static_file('sw.js')


@main_bp.route('/manifest.json')
def manifest():
    """Serve the manifest from root."""
    return current_app.send_static_file('manifest.json')
