
import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_price_trend_page_route(client):
    """Test that the price trend analysis page loads correctly."""
    response = client.get('/modules/analisis-tren-harga')
    assert response.status_code == 200
    assert b'Analisis Tren Harga' in response.data

def test_market_predict_endpoint(client):
    """Test the market prediction endpoint."""
    # Test valid request
    data = {
        'commodity': 'cabai_merah_keriting',
        'date': '2025-12-25' # Future date
    }
    response = client.post('/api/market/predict', json=data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert 'predicted_price' in json_data['data']
    assert 'trend' in json_data['data']
    assert 'insight' in json_data['data']

    # Test invalid commodity
    data_invalid = {
        'commodity': 'invalid_commodity',
        'date': '2025-12-25'
    }
    response = client.post('/api/market/predict', json=data_invalid)
    assert response.status_code == 400 # Or 404 depending on implementation, checking for failure

    # Test past date (should fail or handle gracefully, implementation says error)
    data_past = {
        'commodity': 'cabai_merah_keriting',
        'date': '2020-01-01'
    }
    response = client.post('/api/market/predict', json=data_past)
    assert response.status_code == 400
