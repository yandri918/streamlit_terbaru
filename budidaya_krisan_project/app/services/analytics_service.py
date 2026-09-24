"""
Analytics Service — KPI Aggregator for Budidaya Krisan Pro
"""
from typing import Dict, List, Optional
from app.services.db import get_db, rows_to_list


def get_dashboard_summary(variety_filter: Optional[str] = None, days: Optional[int] = None) -> Dict:
    """Aggregate KPI metrics for the dashboard cards."""
    where_clauses = []
    params = []

    if variety_filter:
        where_clauses.append("b.variety_name = ?")
        params.append(variety_filter)
    if days:
        from datetime import datetime, timedelta
        cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        where_clauses.append("b.planting_date >= ?")
        params.append(cutoff)

    where_sql = " AND ".join(where_clauses)
    if where_sql:
        where_sql = "WHERE " + where_sql

    with get_db() as conn:
        # Active batches
        active_batches = conn.execute(
            f"SELECT COUNT(*) as cnt, SUM(plant_count) as total_plants, COUNT(DISTINCT variety_name) as varieties "
            f"FROM cultivation_batches b {where_sql} AND status='active'"
            if where_sql else
            "SELECT COUNT(*) as cnt, SUM(plant_count) as total_plants, COUNT(DISTINCT variety_name) as varieties "
            "FROM cultivation_batches WHERE status='active'",
            params if where_sql else []
        ).fetchone()

        # Average health score
        avg_health = conn.execute(
            "SELECT AVG(g.health_score) as avg_score FROM growth_records g "
            "JOIN cultivation_batches b ON g.batch_id = b.id "
            f"{where_sql}",
            params
        ).fetchone()

        # Next harvest batch
        next_harvest = conn.execute(
            "SELECT batch_code, variety_name, target_harvest_date FROM cultivation_batches "
            "WHERE status='active' ORDER BY target_harvest_date ASC LIMIT 1"
        ).fetchone()

        # Harvest financials
        financials = conn.execute(
            "SELECT SUM(gross_revenue) as total_revenue, SUM(net_profit) as total_profit, "
            "AVG(roi_pct) as avg_roi FROM harvest_records"
        ).fetchone()

        # Latest growth records for trend
        latest_records = conn.execute(
            "SELECT g.* FROM growth_records g JOIN cultivation_batches b ON g.batch_id=b.id "
            "WHERE b.status='active' ORDER BY g.recording_date DESC LIMIT 20"
        ).fetchall()

        total_plants = active_batches["total_plants"] or 0
        avg_land = conn.execute(
            "SELECT AVG(land_area_m2) as avg_land FROM cultivation_batches WHERE status='active'"
        ).fetchone()
        estimated_revenue = int(total_plants * 4 * 0.65 * 25000)  # stems/plant × grade A pct × price

    return {
        "total_active_batches": active_batches["cnt"] or 0,
        "total_plants": int(total_plants),
        "active_varieties": active_batches["varieties"] or 0,
        "avg_health_score": round(avg_health["avg_score"] or 0, 1),
        "next_harvest_batch": dict(next_harvest) if next_harvest else None,
        "total_harvest_revenue": int(financials["total_revenue"] or 0),
        "total_harvest_profit": int(financials["total_profit"] or 0),
        "avg_roi_pct": round(financials["avg_roi"] or 0, 1),
        "estimated_active_revenue": estimated_revenue,
        "avg_land_area_m2": round(avg_land["avg_land"] or 0, 1),
    }


def get_growth_chart_data(batch_id: Optional[str] = None) -> Dict:
    """Get growth curve data (actual vs ideal) for Chart.js."""
    from app.services.ai_growth_service import GROWTH_STANDARDS

    with get_db() as conn:
        if batch_id:
            records = conn.execute(
                "SELECT week_number, plant_height_cm, health_score, recording_date "
                "FROM growth_records WHERE batch_id=? ORDER BY week_number",
                [batch_id]
            ).fetchall()
        else:
            records = conn.execute(
                "SELECT week_number, AVG(plant_height_cm) as plant_height_cm, "
                "AVG(health_score) as health_score "
                "FROM growth_records GROUP BY week_number ORDER BY week_number"
            ).fetchall()

    actual_weeks = [r["week_number"] for r in records]
    actual_heights = [round(r["plant_height_cm"] or 0, 1) for r in records]
    health_scores = [round(r["health_score"] or 0, 1) for r in records]

    # Build ideal curve for weeks 1-16
    ideal_weeks = list(GROWTH_STANDARDS.keys())
    ideal_heights = [GROWTH_STANDARDS[w]["height_ideal"] for w in ideal_weeks]
    ideal_min = [GROWTH_STANDARDS[w]["height_min"] for w in ideal_weeks]
    ideal_max = [GROWTH_STANDARDS[w]["height_max"] for w in ideal_weeks]

    return {
        "actual": {"weeks": actual_weeks, "heights": actual_heights},
        "ideal": {"weeks": ideal_weeks, "heights": ideal_heights, "min": ideal_min, "max": ideal_max},
        "health_scores": {"weeks": actual_weeks, "scores": health_scores},
    }


def get_financial_chart_data() -> Dict:
    """Get financial data for bar chart (per harvest)."""
    with get_db() as conn:
        records = conn.execute(
            "SELECT variety_name, SUM(gross_revenue) as revenue, "
            "SUM(production_cost) as cost, SUM(net_profit) as profit, "
            "AVG(roi_pct) as roi "
            "FROM harvest_records GROUP BY variety_name ORDER BY profit DESC LIMIT 8"
        ).fetchall()

    return {
        "labels": [r["variety_name"] for r in records],
        "revenue": [int(r["revenue"] or 0) for r in records],
        "cost": [int(r["cost"] or 0) for r in records],
        "profit": [int(r["profit"] or 0) for r in records],
        "roi": [round(r["roi"] or 0, 1) for r in records],
    }


def get_grade_distribution() -> Dict:
    """Get grade distribution for doughnut chart."""
    with get_db() as conn:
        total = conn.execute(
            "SELECT SUM(grade_a_stems) as a, SUM(grade_b_stems) as b, "
            "SUM(grade_c_stems) as c FROM harvest_records"
        ).fetchone()

    a = int(total["a"] or 0)
    b = int(total["b"] or 0)
    c = int(total["c"] or 0)
    grand = max(1, a + b + c)

    return {
        "grade_a": a, "grade_b": b, "grade_c": c,
        "grade_a_pct": round(a / grand * 100, 1),
        "grade_b_pct": round(b / grand * 100, 1),
        "grade_c_pct": round(c / grand * 100, 1),
    }
