import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_integrated_recommendation(client):
    """Test the integrated recommendation endpoint."""
    payload = {
        "ketinggian": "dataran_rendah",
        "iklim": "tropis",
        "fase": "vegetatif",
        "masalah": "ulat_grayak"
    }
    
    response = client.post('/api/recommendation/integrated', json=payload)
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'data' in data
    
    rec = data['data']
    assert 'bibit' in rec
    assert 'pemupukan' in rec
    assert 'pengendalian' in rec
    
    # Check specific values based on input
    assert rec['pengendalian'] is not None
    assert 'strategy' in rec['pengendalian']
    assert "Ulat Grayak" in rec['pengendalian']['strategy']['name']
    assert rec['bibit']['kriteria'] is not None
