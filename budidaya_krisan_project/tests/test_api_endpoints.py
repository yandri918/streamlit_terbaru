import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "database" in data
    assert data["database"]["engine"] in ["sqlite", "postgresql"]
    assert data["database"]["status"] == "connected"


def test_list_varieties_endpoint():
    resp = client.get("/api/v1/batches/varieties")
    assert resp.status_code == 200
    varieties = resp.json()["data"]
    assert len(varieties) >= 8
    names = [v["name"] for v in varieties]
    assert "Fiji White" in names
    assert "Reagent Pink" in names


def test_list_batches_endpoint():
    resp = client.get("/api/v1/batches")
    assert resp.status_code == 200
    batches = resp.json()["data"]
    assert len(batches) >= 1
    assert any(b["variety_name"] in ["Fiji White", "Fiji Yellow", "Reagent Pink"] for b in batches)


def test_analytics_summary_endpoint():
    resp = client.get("/api/v1/analytics/summary")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "total_active_batches" in data
    assert "total_plants" in data
    assert "avg_health_score" in data


def test_analytics_ai_insights_endpoint():
    resp = client.get("/api/v1/analytics/ai-insights")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "composite_score" in data
    assert "rating_stars" in data
    assert "recommendations" in data


def test_growth_chart_endpoint():
    resp = client.get("/api/v1/analytics/growth-chart")
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert "actual" in data
    assert "ideal" in data
    assert "health_scores" in data
    assert "weeks" in data["actual"]
    assert "heights" in data["actual"]


def test_production_economic_calculator():
    resp = client.post("/api/v1/production/calculate", json={
        "land_area_m2": 600.0,
        "plant_density": 48.0,
        "expected_stems_per_plant": 3.5,
        "grade_a_pct": 0.70,
        "grade_b_pct": 0.25,
        "grade_c_pct": 0.05,
        "grade_a_price": 2800,
        "grade_b_price": 2200,
        "grade_c_price": 1000,
        "production_cost_per_m2": 75000,
        "cycle_count_per_year": 3,
    })
    assert resp.status_code == 200
    result = resp.json()["data"]
    assert result["total_plants"] == 28800
    assert result["total_stems"] == 100800
    assert result["gross_revenue"] > 0
    assert result["roi_pct"] > 0
