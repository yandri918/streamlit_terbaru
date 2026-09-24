import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.population_service import calculate_house_population, calculate_multi_house_summary

client = TestClient(app)


def test_calculate_house_population_standard():
    """Standard 12 beds, 50m length, 6 rows, 12.5cm spacing"""
    res = calculate_house_population(
        beds=12,
        bed_length=50.0,
        bed_width=100.0,
        rows_per_bed=6,
        plant_spacing=12.5,
        survival_rate=85.0,
        stems_per_plant=3.5,
        beds_putih=4,
        beds_pink=4,
        beds_kuning=4,
    )
    r = res["results"]
    assert r["plants_per_row"] == 400
    assert r["plants_per_bed"] == 2400
    assert r["total_plants"] == 28800
    assert r["total_bed_area_m2"] == 600.0
    assert r["actual_density_per_m2"] == 48.0
    assert r["surviving_plants"] == 24480
    assert r["total_stems"] == 85680

    v = res["varieties"]
    assert v["putih"]["plants"] == 9600
    assert v["pink"]["plants"] == 9600
    assert v["kuning"]["plants"] == 9600


def test_api_house_population_endpoint():
    resp = client.post("/api/v1/production/house-population", json={
        "house_name": "House 1",
        "beds": 12,
        "bed_length": 50.0,
        "bed_width": 100.0,
        "rows_per_bed": 6,
        "plant_spacing": 12.5,
        "survival_rate": 85.0,
        "stems_per_plant": 3.5,
        "beds_putih": 4,
        "beds_pink": 4,
        "beds_kuning": 4,
    })
    assert resp.status_code == 200
    data = resp.json()["data"]
    assert data["results"]["total_plants"] == 28800
    assert data["results"]["total_stems"] == 85680


def test_api_batch_creation_auto_calculates_population():
    resp = client.post("/api/v1/batches", json={
        "variety_name": "Fiji White",
        "planting_date": "2026-10-01",
        "target_harvest_date": "2027-01-21",
        "house_name": "House 1",
        "beds_count": 12,
        "bed_length_m": 50.0,
        "rows_per_bed": 6,
        "plant_spacing_cm": 12.5,
    })
    assert resp.status_code == 200
    batch = resp.json()["data"]
    assert batch["plant_count"] == 28800
    assert batch["land_area_m2"] == 600.0
    assert batch["house_name"] == "House 1"
