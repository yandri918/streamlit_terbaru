import pytest
from app.services.ai_insight_service import get_ai_insights, KRISAN_BENCHMARKS


def test_ai_insights_structure():
    """Verify AI benchmark evaluation returns all expected metrics and ratings."""
    insights = get_ai_insights()

    assert "benchmark_name" in insights
    assert "composite_score" in insights
    assert "rating_stars" in insights
    assert "status" in insights
    assert "recommendations" in insights

    assert insights["benchmark_name"] == KRISAN_BENCHMARKS["standard_name"]
    assert 1 <= insights["rating_stars"] <= 5
    assert isinstance(insights["composite_score"], float)
    assert len(insights["recommendations"]) >= 1


def test_ai_insights_with_variety_filter():
    """AI insights filtered by variety should return valid evaluations."""
    insights = get_ai_insights(variety_filter="Reagent Pink")
    assert insights["rating_stars"] in [1, 2, 3, 4, 5]
    assert isinstance(insights["status"], str)
