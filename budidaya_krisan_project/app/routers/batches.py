"""
Batches Router — Cultivation Batch CRUD
POST /api/v1/batches            - Create new cultivation batch
GET  /api/v1/batches            - List all batches
GET  /api/v1/batches/{id}       - Get batch detail
PATCH /api/v1/batches/{id}      - Update batch
GET  /api/v1/batches/varieties  - List available varieties
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from app.schemas.common import ApiResponse
from app.schemas.monitoring import BatchCreate, BatchUpdate
from app.services.db import get_db, new_id, row_to_dict, rows_to_list
from datetime import datetime

from app.services.population_service import calculate_house_population

router = APIRouter(prefix="/batches", tags=["Batches"])


@router.post("", response_model=ApiResponse)
def create_batch(payload: BatchCreate):
    batch_id = new_id()
    now = datetime.now().isoformat()

    # Calculate plant count & land area from official house logic
    pop = calculate_house_population(
        beds=payload.beds_count or 12,
        bed_length=payload.bed_length_m or 50.0,
        rows_per_bed=payload.rows_per_bed or 6,
        plant_spacing=payload.plant_spacing_cm or 12.5,
        house_name=payload.house_name or "House 1",
    )
    final_plant_count = payload.plant_count if payload.plant_count is not None else pop["results"]["total_plants"]
    final_land_area = payload.land_area_m2 if payload.land_area_m2 is not None else pop["results"]["total_bed_area_m2"]

    # Generate sequential batch code
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) as c FROM cultivation_batches").fetchone()["c"]
        year = datetime.now().year
        batch_code = f"KRISAN-{year}-{str(count + 1).zfill(3)}"

        # Try to find variety_id by name
        variety = conn.execute(
            "SELECT id FROM varieties WHERE name=?", [payload.variety_name]
        ).fetchone()
        variety_id = variety["id"] if variety else None

        conn.execute(
            """INSERT INTO cultivation_batches
               (id, batch_code, variety_id, variety_name, planting_date, target_harvest_date,
                land_area_m2, plant_count, house_name, beds_count, bed_length_m,
                row_count, plant_spacing_cm, notes, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            [batch_id, batch_code, variety_id, payload.variety_name,
             payload.planting_date, payload.target_harvest_date,
             final_land_area, final_plant_count,
             payload.house_name or "House 1", payload.beds_count or 12,
             payload.bed_length_m or 50.0, payload.rows_per_bed or 6,
             payload.plant_spacing_cm or 12.5,
             payload.notes, now, now]
        )
        batch = row_to_dict(conn.execute(
            "SELECT * FROM cultivation_batches WHERE id=?", [batch_id]
        ).fetchone())

    return ApiResponse.ok(batch, f"Batch {batch_code} ({payload.house_name or 'House 1'}, {final_plant_count:,} tanaman) berhasil dibuat.")


@router.get("", response_model=ApiResponse)
def list_batches(
    status: Optional[str] = Query(None),
    variety: Optional[str] = Query(None),
    limit: int = Query(50, le=200),
):
    with get_db() as conn:
        sql = "SELECT * FROM cultivation_batches WHERE 1=1"
        params = []
        if status:
            sql += " AND status=?"
            params.append(status)
        if variety:
            sql += " AND variety_name LIKE ?"
            params.append(f"%{variety}%")
        sql += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        batches = rows_to_list(conn.execute(sql, params).fetchall())
    return ApiResponse.ok(batches)


@router.get("/varieties", response_model=ApiResponse)
def list_varieties():
    with get_db() as conn:
        varieties = rows_to_list(conn.execute(
            "SELECT * FROM varieties ORDER BY name"
        ).fetchall())
    return ApiResponse.ok(varieties)


@router.get("/{batch_id}", response_model=ApiResponse)
def get_batch(batch_id: str):
    with get_db() as conn:
        batch = row_to_dict(conn.execute(
            "SELECT * FROM cultivation_batches WHERE id=?", [batch_id]
        ).fetchone())
        if not batch:
            raise HTTPException(404, "Batch tidak ditemukan.")
        # Attach growth record count
        count = conn.execute(
            "SELECT COUNT(*) as c FROM growth_records WHERE batch_id=?", [batch_id]
        ).fetchone()["c"]
        batch["growth_record_count"] = count
    return ApiResponse.ok(batch)


@router.patch("/{batch_id}", response_model=ApiResponse)
def update_batch(batch_id: str, payload: BatchUpdate):
    with get_db() as conn:
        batch = conn.execute(
            "SELECT id FROM cultivation_batches WHERE id=?", [batch_id]
        ).fetchone()
        if not batch:
            raise HTTPException(404, "Batch tidak ditemukan.")

        updates = {}
        if payload.status is not None:
            updates["status"] = payload.status
        if payload.notes is not None:
            updates["notes"] = payload.notes
        if payload.target_harvest_date is not None:
            updates["target_harvest_date"] = payload.target_harvest_date

        if updates:
            updates["updated_at"] = datetime.now().isoformat()
            set_sql = ", ".join(f"{k}=?" for k in updates)
            conn.execute(
                f"UPDATE cultivation_batches SET {set_sql} WHERE id=?",
                list(updates.values()) + [batch_id]
            )

        updated = row_to_dict(conn.execute(
            "SELECT * FROM cultivation_batches WHERE id=?", [batch_id]
        ).fetchone())
    return ApiResponse.ok(updated, "Batch berhasil diperbarui.")


@router.delete("/{batch_id}", response_model=ApiResponse)
def delete_batch(batch_id: str):
    with get_db() as conn:
        batch = conn.execute(
            "SELECT batch_code FROM cultivation_batches WHERE id=?", [batch_id]
        ).fetchone()
        if not batch:
            raise HTTPException(404, "Batch tidak ditemukan.")
        conn.execute("DELETE FROM cultivation_batches WHERE id=?", [batch_id])
    return ApiResponse.ok(None, f"Batch {batch['batch_code']} berhasil dihapus.")
