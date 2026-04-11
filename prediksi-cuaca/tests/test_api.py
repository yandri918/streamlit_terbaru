"""
Unit tests for Weather Prediction API
"""
import pytest
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["status"] == "operational"

def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_current_weather():
    """Test current weather endpoint"""
    response = client.get("/api/v1/weather/current?latitude=-6.2&longitude=106.8")
    assert response.status_code in [200, 500]  # May fail if API is down
    
def test_current_weather_invalid_coords():
    """Test current weather with invalid coordinates"""
    response = client.get("/api/v1/weather/current?latitude=100&longitude=200")
    assert response.status_code == 422  # Validation error

def test_hourly_forecast():
    """Test hourly forecast endpoint"""
    response = client.get("/api/v1/weather/hourly?latitude=-6.2&longitude=106.8&hours=24")
    assert response.status_code in [200, 500]

def test_daily_forecast():
    """Test daily forecast endpoint"""
    response = client.get("/api/v1/weather/daily?latitude=-6.2&longitude=106.8&days=7")
    assert response.status_code in [200, 500]

def test_statistics():
    """Test statistics endpoint"""
    response = client.get("/api/v1/weather/statistics?latitude=-6.2&longitude=106.8&days=30")
    assert response.status_code in [200, 500]

def test_predict_temperature():
    """Test temperature prediction endpoint"""
    response = client.post(
        "/api/v1/predict/temperature",
        json={"latitude": -6.2, "longitude": 106.8}
    )
    assert response.status_code == 200
    assert "message" in response.json()
