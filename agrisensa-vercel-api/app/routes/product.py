"""Product routes for QR code traceability."""
from flask import Blueprint, render_template, request, jsonify
import json
import base64

product_bp = Blueprint('product', __name__)


def decode_product_data(encoded_data):
    """Decode base64 encoded product data."""
    try:
        # Ensure correct padding for base64
        encoded_data = encoded_data.rstrip('=')
        padding = 4 - (len(encoded_data) % 4)
        if padding != 4:
            encoded_data += '=' * padding
            
        decoded_bytes = base64.urlsafe_b64decode(encoded_data)
        decoded_str = decoded_bytes.decode('utf-8')
        data = json.loads(decoded_str)
        
        # Log success for debugging
        print(f"[DECODE SUCCESS] Keys: {list(data.keys())}")
        return data
    except Exception as e:
        # Log error for debugging
        print(f"[DECODE ERROR] {type(e).__name__}: {str(e)}")
        print(f"[DECODE ERROR] Input length: {len(encoded_data)}")
        return None


@product_bp.route('/product/<batch_id>')
def product_passport(batch_id):
    """Display product passport page using query parameters."""
    
    # Manual query string parsing (Vercel workaround)
    from urllib.parse import parse_qs, unquote
    
    query_string = request.query_string.decode('utf-8')
    params = parse_qs(query_string)
    
    # Helper to get first value from parsed params
    def get_param(key, default=''):
        values = params.get(key, [default])
        return values[0] if values else default
    
    # Debug log
    print(f"DEBUG - batch_id: {batch_id}")
    print(f"DEBUG - query_string: {query_string}")
    print(f"DEBUG - parsed params: {params}")
    
    # Extract data from manually parsed query parameters
    product = {
        'batch_id': get_param('batch_id', batch_id),
        'name': get_param('name', 'Produk AgriSensa'),
        'variety': get_param('variety', ''),
        'farmer': get_param('farmer', 'Petani Indonesia'),
        'location': get_param('location', 'Indonesia'),
        'harvest_date': get_param('harvest_date', ''),
        'weight': get_param('weight', '1 kg'),
        'emoji': '🌾',
        'price': None,
        'certifications': ['Organik', 'Fresh', 'Lokal'],
        'avg_temp': get_param('avg_temp', ''),
        'avg_hum': get_param('avg_hum', ''),
        'sun_hours': get_param('sun_hours', ''),
        'notes': get_param('notes', ''),
        'milestones': []
    }
    
    # Parse price if present
    price_str = get_param('price')
    if price_str and price_str not in ['None', '']:
        try:
            product['price'] = float(price_str)
        except:
            pass
    
    # Parse milestones JSON if present
    milestones_json = get_param('milestones')
    if milestones_json:
        try:
            product['milestones'] = json.loads(unquote(milestones_json))
        except Exception as e:
            print(f"DEBUG - Milestones parse error: {e}")
            print(f"DEBUG - Milestones raw: {milestones_json}")
            pass
    
    print(f"DEBUG - Final product dict keys: {product.keys()}")
    print(f"DEBUG - avg_temp value: '{product['avg_temp']}'")
    
    return render_template('product_passport.html', product=product)


@product_bp.route('/api/product/generate-url', methods=['POST'])
def generate_product_url():
    """
    Generate a product passport URL for QR code.
    Expects JSON with product data.
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    # Create query string from data
    params = []
    if data.get('name'):
        params.append(f"name={data['name']}")
    if data.get('variety'):
        params.append(f"variety={data['variety']}")
    if data.get('farmer'):
        params.append(f"farmer={data['farmer']}")
    if data.get('location'):
        params.append(f"location={data['location']}")
    if data.get('harvest_date'):
        params.append(f"harvest_date={data['harvest_date']}")
    if data.get('weight'):
        params.append(f"weight={data['weight']}")
    if data.get('price'):
        params.append(f"price={data['price']}")
    if data.get('emoji'):
        params.append(f"emoji={data['emoji']}")
    
    batch_id = data.get('batch_id', 'BATCH001')
    query_string = '&'.join(params)
    
    base_url = request.host_url.rstrip('/')
    url = f"{base_url}/product/{batch_id}"
    if query_string:
        url += f"?{query_string}"
    
    return jsonify({
        'success': True,
        'url': url,
        'batch_id': batch_id
    })
