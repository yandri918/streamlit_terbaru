import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_fertilizer_recommendation(client):
    """Test the /api/recommendation/fertilizer endpoint."""
    payload = {
        "ph_tanah": 6.5,
        "skor_bwd": 40,
        "kelembaban_tanah": 60,
        "umur_tanaman_hari": 45
    }
    response = client.post('/api/recommendation/fertilizer', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'recommendation' in data
    assert 'rekomendasi_utama' in data['recommendation']
    assert 'rekomendasi_pupuk_ml' in data['recommendation']

def test_calculate_fertilizer(client):
    """Test the /api/recommendation/calculate-fertilizer endpoint."""
    payload = {
        "commodity": "padi",
        "area_sqm": 1000,
        "ph_tanah": 6.0
    }
    response = client.post('/api/recommendation/calculate-fertilizer', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert data['data']['commodity_name'] == "Padi"
    assert 'anorganik' in data['data']

def test_calculate_fertilizer_invalid_commodity(client):
    """Test /api/recommendation/calculate-fertilizer with invalid commodity."""
    payload = {
        "commodity": "invalid_crop",
        "area_sqm": 1000,
        "ph_tanah": 6.0
    }
    response = client.post('/api/recommendation/calculate-fertilizer', json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert data['error'] == 'Commodity not found'

def test_spraying_recommendation(client):
    """Test the /api/recommendation/spraying endpoint."""
    payload = {
        "pest": "thrips"
    }
    response = client.post('/api/recommendation/spraying', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    assert 'strategy' in data['data']
    assert data['data']['strategy']['name'] == "Strategi Pengendalian Thrips"

def test_spraying_recommendation_invalid_pest(client):
    """Test /api/recommendation/spraying with invalid pest."""
    payload = {
        "pest": "invalid_pest"
    }
    response = client.post('/api/recommendation/spraying', json=payload)
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert data['error'] == 'Strategy not found for this pest'
