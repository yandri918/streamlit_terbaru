"""Market data routes for commodity prices."""
from flask import Blueprint, request, jsonify
from app import limiter
from app.services.market_service import MarketService

market_bp = Blueprint('market', __name__)


@market_bp.route('/prices', methods=['POST'])
@limiter.limit("50 per hour")
def get_prices():
    """Get current market prices for commodity."""
    try:
        data = request.get_json()
        
        if not data.get('commodity'):
            return jsonify({
                'success': False,
                'error': 'Commodity is required'
            }), 400
        
        prices = MarketService.get_current_prices(data['commodity'])
        
        if not prices:
            return jsonify({
                'success': False,
                'error': 'Price data not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': prices
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get prices',
            'message': str(e)
        }), 500


@market_bp.route('/ticker', methods=['GET'])
@limiter.limit("100 per hour")
def get_ticker_prices():
    """Get ticker prices for multiple commodities."""
    try:
        ticker_data = MarketService.get_ticker_prices()
        
        return jsonify({
            'success': True,
            'data': ticker_data
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get ticker prices',
            'message': str(e)
        }), 500


@market_bp.route('/historical', methods=['POST'])
@limiter.limit("50 per hour")
def get_historical_prices():
    """Get historical price data for commodity."""
    try:
        data = request.get_json()
        
        if not data.get('commodity'):
            return jsonify({
                'success': False,
                'error': 'Commodity is required'
            }), 400
        
        time_range = int(data.get('range', 30))
        
        historical_data = MarketService.get_historical_prices(
            data['commodity'],
            time_range
        )
        
        if not historical_data:
            return jsonify({
                'success': False,
                'error': 'Historical data not found'
            }), 404
        
        return jsonify({
            'success': True,
            'labels': historical_data['labels'],
            'prices': historical_data['prices']
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to get historical prices',
            'message': str(e)
        }), 500
@market_bp.route('/predict', methods=['POST'])
@limiter.limit("20 per hour")
def predict_price():
    """Predict future price trend."""
    try:
        data = request.get_json()
        
        if not data.get('commodity') or not data.get('date'):
            return jsonify({
                'success': False,
                'error': 'Commodity and target date are required'
            }), 400
            
        prediction = MarketService.predict_price_trend(
            data['commodity'],
            data['date']
        )
        
        if not prediction:
            return jsonify({
                'success': False,
                'error': 'Prediction failed or invalid commodity'
            }), 400
            
        if "error" in prediction:
             return jsonify({
                'success': False,
                'error': prediction["error"]
            }), 400
            
        return jsonify({
            'success': True,
            'data': prediction
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Failed to predict price',
            'message': str(e)
        }), 500
