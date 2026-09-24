"""
Analytics Router — KPI Summary & AI Benchmark Insights
GET /api/v1/analytics/summary     - Dashboard KPI aggregation
GET /api/v1/analytics/ai-insights - AI benchmark evaluator
GET /api/v1/analytics/growth-chart - Growth curve data for Chart.js
GET /api/v1/analytics/financial   - Financial chart data
GET /api/v1/analytics/grades      - Grade distribution for doughnut
GET /api/v1/analytics/predict     - AI growth prediction
"""
from fastapi import APIRouter, Query
from typing import Optional

from app.schemas.common import ApiResponse
from app.services.analytics_service import (
    get_dashboard_summary, get_growth_chart_data,
    get_financial_chart_data, get_grade_distribution
)
from app.services.ai_insight_service import get_ai_insights
from app.services.ai_growth_service import predict_growth
from app.services.db import get_db, rows_to_list

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=ApiResponse)
def dashboard_summary(
    variety: Optional[str] = Query(None),
    days: Optional[int] = Query(None),
):
    data = get_dashboard_summary(variety_filter=variety, days=days)
    return ApiResponse.ok(data)


@router.get("/ai-insights", response_model=ApiResponse)
def ai_insights(variety: Optional[str] = Query(None)):
    data = get_ai_insights(variety_filter=variety)
    return ApiResponse.ok(data)


@router.get("/growth-chart", response_model=ApiResponse)
def growth_chart(batch_id: Optional[str] = Query(None)):
    data = get_growth_chart_data(batch_id=batch_id)
    return ApiResponse.ok(data)


@router.get("/financial", response_model=ApiResponse)
def financial_chart():
    data = get_financial_chart_data()
    return ApiResponse.ok(data)


@router.get("/grades", response_model=ApiResponse)
def grade_distribution():
    data = get_grade_distribution()
    return ApiResponse.ok(data)


@router.get("/predict", response_model=ApiResponse)
def predict_future_growth(batch_id: str = Query(...), weeks_ahead: int = Query(4, ge=1, le=8)):
    with get_db() as conn:
        records = rows_to_list(conn.execute(
            "SELECT week_number, plant_height_cm FROM growth_records "
            "WHERE batch_id=? ORDER BY week_number", [batch_id]
        ).fetchall())

    if len(records) < 2:
        return ApiResponse.ok({"predictions": [], "message": "Minimal 2 data pertumbuhan diperlukan."})

    weeks = [r["week_number"] for r in records]
    heights = [r["plant_height_cm"] for r in records]

    prediction = predict_growth(weeks, heights, weeks_ahead=weeks_ahead)
    return ApiResponse.ok(prediction)
