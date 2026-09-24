"""
Monitoring Router — Growth Records & Harvest Data
POST /api/v1/monitoring              - Record weekly growth data (with AI scoring)
GET  /api/v1/monitoring              - List growth records
GET  /api/v1/monitoring/{id}         - Get growth record detail
PATCH /api/v1/monitoring/{id}        - Update growth record
DELETE /api/v1/monitoring/{id}       - Delete growth record
GET  /api/v1/monitoring/export/csv   - Export CSV
GET  /api/v1/monitoring/{id}/report  - Generate HTML/PDF report
POST /api/v1/monitoring/harvest      - Record harvest data
GET  /api/v1/monitoring/harvest/list - List harvest records
"""
import csv
import io
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import HTMLResponse, StreamingResponse

from app.schemas.common import ApiResponse
from app.schemas.monitoring import GrowthRecordCreate, GrowthRecordUpdate, HarvestRecordCreate
from app.services.db import get_db, new_id, row_to_dict, rows_to_list
from app.services.ai_growth_service import compute_growth_deviation, predict_growth, detect_anomalies
from app.services.health_service import compute_health_score, get_health_recommendations
from app.services.report_service import generate_report_html
from app.services.notification_service import send_growth_notification

router = APIRouter(prefix="/monitoring", tags=["Monitoring"])


@router.post("", response_model=ApiResponse)
def record_growth(payload: GrowthRecordCreate):
    """Record weekly growth data with automatic AI health scoring."""
    with get_db() as conn:
        # Verify batch exists
        batch = row_to_dict(conn.execute(
            "SELECT * FROM cultivation_batches WHERE id=?", [payload.batch_id]
        ).fetchone())
        if not batch:
            raise HTTPException(404, "Batch tidak ditemukan.")

        # Check duplicate week
        existing = conn.execute(
            "SELECT id FROM growth_records WHERE batch_id=? AND week_number=?",
            [payload.batch_id, payload.week_number]
        ).fetchone()

        # Fetch history for consistency scoring
        history = rows_to_list(conn.execute(
            "SELECT plant_height_cm, week_number FROM growth_records "
            "WHERE batch_id=? ORDER BY week_number", [payload.batch_id]
        ).fetchall())

    # Compute health score & deviation
    health_result = compute_health_score(
        week=payload.week_number,
        height=payload.plant_height_cm,
        leaf_count=payload.leaf_count,
        stem_diameter=payload.stem_diameter_mm,
        branch_count=payload.branch_count,
        temperature=payload.temperature_c,
        humidity=payload.humidity_pct,
        history=history,
    )
    deviation = compute_growth_deviation(payload.plant_height_cm, payload.week_number)

    # Rule-based anomaly detection
    is_anomaly = abs(deviation) > 30
    anomaly_type = "STUNTED" if deviation < -30 else ("EXCESSIVE" if deviation > 30 else None)

    record_id = new_id()
    now = datetime.now().isoformat()

    with get_db() as conn:
        if existing:
            # Update existing record for this week
            conn.execute(
                """UPDATE growth_records SET
                   plant_height_cm=?, leaf_count=?, stem_diameter_mm=?, branch_count=?,
                   bud_count=?, health_score=?, ai_grade=?, growth_deviation_pct=?,
                   anomaly_detected=?, anomaly_type=?,
                   temperature_c=?, humidity_pct=?, weather_condition=?,
                   notes=?, recording_date=?
                   WHERE batch_id=? AND week_number=?""",
                [payload.plant_height_cm, payload.leaf_count, payload.stem_diameter_mm,
                 payload.branch_count, payload.bud_count or 0,
                 health_result["total_score"], health_result["ai_grade"], deviation,
                 1 if is_anomaly else 0, anomaly_type,
                 payload.temperature_c, payload.humidity_pct, payload.weather_condition,
                 payload.notes, payload.recording_date,
                 payload.batch_id, payload.week_number]
            )
            record = row_to_dict(conn.execute(
                "SELECT * FROM growth_records WHERE batch_id=? AND week_number=?",
                [payload.batch_id, payload.week_number]
            ).fetchone())
        else:
            conn.execute(
                """INSERT INTO growth_records
                   (id, batch_id, batch_code, variety_name, week_number, recording_date,
                    plant_height_cm, leaf_count, stem_diameter_mm, branch_count, bud_count,
                    health_score, ai_grade, growth_deviation_pct,
                    anomaly_detected, anomaly_type,
                    temperature_c, humidity_pct, weather_condition, notes, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [record_id, payload.batch_id, batch["batch_code"], batch["variety_name"],
                 payload.week_number, payload.recording_date,
                 payload.plant_height_cm, payload.leaf_count, payload.stem_diameter_mm,
                 payload.branch_count, payload.bud_count or 0,
                 health_result["total_score"], health_result["ai_grade"], deviation,
                 1 if is_anomaly else 0, anomaly_type,
                 payload.temperature_c, payload.humidity_pct, payload.weather_condition,
                 payload.notes, now]
            )
            record = row_to_dict(conn.execute(
                "SELECT * FROM growth_records WHERE id=?", [record_id]
            ).fetchone())

    # Generate recommendations
    recommendations = get_health_recommendations(health_result, payload.week_number, payload.plant_height_cm)
    record["health_breakdown"] = health_result.get("breakdown", {})
    record["recommendations"] = recommendations

    # Send webhook notification (async-ish via fire-and-forget)
    try:
        send_growth_notification(
            batch["batch_code"], batch["variety_name"],
            payload.week_number, payload.plant_height_cm,
            health_result["total_score"], health_result["ai_grade"], deviation
        )
    except Exception:
        pass

    return ApiResponse.ok(record, "Data pertumbuhan berhasil disimpan dengan analisis AI.")


@router.get("", response_model=ApiResponse)
def list_growth_records(
    batch_id: Optional[str] = Query(None),
    variety: Optional[str] = Query(None),
    limit: int = Query(100, le=500),
):
    with get_db() as conn:
        sql = ("SELECT g.*, b.land_area_m2, b.plant_count FROM growth_records g "
               "JOIN cultivation_batches b ON g.batch_id=b.id WHERE 1=1")
        params = []
        if batch_id:
            sql += " AND g.batch_id=?"
            params.append(batch_id)
        if variety:
            sql += " AND g.variety_name LIKE ?"
            params.append(f"%{variety}%")
        sql += " ORDER BY g.recording_date DESC, g.week_number DESC LIMIT ?"
        params.append(limit)
        records = rows_to_list(conn.execute(sql, params).fetchall())
    return ApiResponse.ok(records)


@router.get("/export/csv")
def export_csv(batch_id: Optional[str] = Query(None)):
    with get_db() as conn:
        sql = ("SELECT g.batch_code, g.variety_name, g.week_number, g.recording_date, "
               "g.plant_height_cm, g.leaf_count, g.stem_diameter_mm, g.branch_count, "
               "g.health_score, g.ai_grade, g.growth_deviation_pct, "
               "g.anomaly_detected, g.anomaly_type, g.temperature_c, g.humidity_pct, "
               "g.weather_condition, g.notes FROM growth_records g "
               "JOIN cultivation_batches b ON g.batch_id=b.id WHERE 1=1")
        params = []
        if batch_id:
            sql += " AND g.batch_id=?"
            params.append(batch_id)
        sql += " ORDER BY g.batch_code, g.week_number"
        records = rows_to_list(conn.execute(sql, params).fetchall())

    output = io.StringIO()
    output.write("\ufeff")  # UTF-8 BOM for Excel
    if records:
        writer = csv.DictWriter(output, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    filename = f"krisan_monitoring_{datetime.now().strftime('%Y%m%d')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/{record_id}/report", response_class=HTMLResponse)
def get_report(record_id: str):
    with get_db() as conn:
        record = row_to_dict(conn.execute(
            "SELECT * FROM growth_records WHERE id=?", [record_id]
        ).fetchone())
        if not record:
            raise HTTPException(404, "Record tidak ditemukan.")
        batch = row_to_dict(conn.execute(
            "SELECT * FROM cultivation_batches WHERE id=?", [record["batch_id"]]
        ).fetchone())
        all_growth = rows_to_list(conn.execute(
            "SELECT * FROM growth_records WHERE batch_id=? ORDER BY week_number",
            [record["batch_id"]]
        ).fetchall())
        harvest = row_to_dict(conn.execute(
            "SELECT * FROM harvest_records WHERE batch_id=? LIMIT 1", [record["batch_id"]]
        ).fetchone() or {})

    html = generate_report_html(batch, all_growth, harvest or None)
    return HTMLResponse(html)


@router.get("/batch/{batch_id}/report", response_class=HTMLResponse)
def get_batch_report(batch_id: str):
    with get_db() as conn:
        batch = row_to_dict(conn.execute(
            "SELECT * FROM cultivation_batches WHERE id=?", [batch_id]
        ).fetchone())
        if not batch:
            raise HTTPException(404, "Batch tidak ditemukan.")
        growth_records = rows_to_list(conn.execute(
            "SELECT * FROM growth_records WHERE batch_id=? ORDER BY week_number", [batch_id]
        ).fetchall())
        harvest = row_to_dict(conn.execute(
            "SELECT * FROM harvest_records WHERE batch_id=? LIMIT 1", [batch_id]
        ).fetchone() or {})
    html = generate_report_html(batch, growth_records, harvest or None)
    return HTMLResponse(html)


@router.post("/harvest", response_model=ApiResponse)
def record_harvest(payload: HarvestRecordCreate):
    with get_db() as conn:
        batch = row_to_dict(conn.execute(
            "SELECT * FROM cultivation_batches WHERE id=?", [payload.batch_id]
        ).fetchone())
        if not batch:
            raise HTTPException(404, "Batch tidak ditemukan.")

    # Compute financials
    gross = (payload.grade_a_stems * payload.grade_a_price +
             payload.grade_b_stems * payload.grade_b_price +
             payload.grade_c_stems * payload.grade_c_price)
    net = gross - payload.production_cost
    roi = round((net / max(1, payload.production_cost)) * 100, 2)
    bep = round(payload.production_cost / max(1, payload.total_stems), 2)
    marketable = round((payload.grade_a_stems + payload.grade_b_stems) / max(1, payload.total_stems) * 100, 1)
    loss_rate = round(payload.grade_c_stems / max(1, payload.total_stems) * 100, 1)

    record_id = new_id()
    with get_db() as conn:
        conn.execute(
            """INSERT INTO harvest_records
               (id, batch_id, batch_code, variety_name, harvest_date,
                total_stems, grade_a_stems, grade_b_stems, grade_c_stems,
                grade_a_price, grade_b_price, grade_c_price,
                gross_revenue, production_cost, net_profit, roi_pct,
                bep_per_stem, marketable_yield_pct, loss_rate_pct, notes)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            [record_id, payload.batch_id, batch["batch_code"], batch["variety_name"],
             payload.harvest_date, payload.total_stems,
             payload.grade_a_stems, payload.grade_b_stems, payload.grade_c_stems,
             payload.grade_a_price, payload.grade_b_price, payload.grade_c_price,
             gross, payload.production_cost, net, roi, bep, marketable, loss_rate,
             payload.notes]
        )
        # Mark batch as harvested
        conn.execute(
            "UPDATE cultivation_batches SET status='harvested', updated_at=? WHERE id=?",
            [datetime.now().isoformat(), payload.batch_id]
        )
        record = row_to_dict(conn.execute(
            "SELECT * FROM harvest_records WHERE id=?", [record_id]
        ).fetchone())
    return ApiResponse.ok(record, "Data panen berhasil dicatat.")


@router.get("/harvest/list", response_model=ApiResponse)
def list_harvests(limit: int = Query(50)):
    with get_db() as conn:
        records = rows_to_list(conn.execute(
            "SELECT * FROM harvest_records ORDER BY harvest_date DESC LIMIT ?", [limit]
        ).fetchall())
    return ApiResponse.ok(records)
