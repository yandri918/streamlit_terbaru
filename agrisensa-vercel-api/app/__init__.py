"""Super minimal Flask app for Product Passport - No database."""
import os
from flask import Flask, render_template, request, jsonify

def create_app():
    """Create minimal Flask app for product passport only."""
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    app = Flask(__name__, template_folder=template_dir)
    
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'message': 'AgriSensa Product Passport API',
            'usage': '/product/BATCH001?name=Produk&farmer=Petani&location=Lokasi'
        })
    
    @app.route('/product/<batch_id>')
    def product_passport(batch_id):
        """Display product passport page."""
        product = {
            'batch_id': batch_id,
            'name': request.args.get('name', 'Produk AgriSensa'),
            'variety': request.args.get('variety', ''),
            'farmer': request.args.get('farmer', 'Petani Indonesia'),
            'location': request.args.get('location', 'Indonesia'),
            'harvest_date': request.args.get('harvest_date', ''),
            'weight': request.args.get('weight', ''),
            'price': request.args.get('price', type=float),
            'emoji': request.args.get('emoji', '🌾'),
            'certifications': request.args.getlist('cert') or ['Organik', 'Fresh', 'Lokal'],
            # Lab Results
            'cn_ratio': request.args.get('cn_ratio', ''),
            'ph_level': request.args.get('ph_level', ''),
            'nitrogen': request.args.get('nitrogen', ''),
            'phosphate': request.args.get('phosphate', ''),
            'kalium': request.args.get('kalium', ''),
            'grade': request.args.get('grade', '')
        }
        return render_template('product_passport.html', product=product)
    
    @app.route('/api/health')
    def health():
        return jsonify({'status': 'ok'})
    
    return app
