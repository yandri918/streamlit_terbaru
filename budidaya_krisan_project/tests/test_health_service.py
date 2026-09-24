import pytest
from app.services.health_service import compute_health_score, get_health_recommendations


def test_compute_health_score_optimal_vegetative():
    """Week 4 with ideal height (26cm) and optimal environment should score high (Grade A)."""
    res = compute_health_score(
        week=4,
        height=26.0,
        leaf_count=12,
        stem_diameter=5.5,
        branch_count=0,
        temperature=18.5,
        humidity=78.0,
    )
    assert res["total_score"] >= 80.0
    assert res["ai_grade"] == "A"
    assert abs(res["growth_deviation_pct"]) < 10.0
    assert res["breakdown"]["growth_score"] >= 90.0
    assert res["breakdown"]["environment_score"] >= 90.0


def test_compute_health_score_stunted_growth():
    """Stunted height (far below minimum) should yield a lower score and critical or high recommendations."""
    res = compute_health_score(
        week=7,
        height=20.0,  # Ideal is ~48cm, min is ~38cm
        leaf_count=8,
        stem_diameter=4.0,
        branch_count=1,
        temperature=12.0,
        humidity=55.0,
    )
    assert res["total_score"] < 80.0
    assert res["growth_deviation_pct"] < -20.0

    recs = get_health_recommendations(res, week=7, height=20.0)
    assert any(r["priority"] in ["HIGH", "CRITICAL"] for r in recs)
    # Week 7 specific recommendation for pinching
    assert any(r["title"] == "Minggu 7 — Waktu Pinching" for r in recs)


def test_compute_health_score_week_9_short_day_recommendation():
    """Week 9 should trigger short day photoperiod advice."""
    res = compute_health_score(
        week=9,
        height=65.0,
        leaf_count=20,
        stem_diameter=7.5,
        branch_count=4,
        temperature=19.0,
        humidity=75.0,
    )
    recs = get_health_recommendations(res, week=9, height=65.0)
    assert any(r["title"] == "Minggu 9 — Mulai Short Day Treatment" for r in recs)


def test_compute_health_score_with_history_consistency():
    """History of consistent positive growth should reward consistency score."""
    history = [
        {"plant_height_cm": 12.0},
        {"plant_height_cm": 16.5},
        {"plant_height_cm": 21.0},
    ]
    res = compute_health_score(
        week=4,
        height=26.0,
        history=history,
    )
    assert res["breakdown"]["consistency_score"] >= 70.0
