from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class BatchCreate(BaseModel):
    variety_name: str = Field(..., json_schema_extra={"example": "Fiji White"})
    planting_date: str = Field(..., json_schema_extra={"example": "2026-07-01"})
    target_harvest_date: str = Field(..., json_schema_extra={"example": "2026-10-21"})
    land_area_m2: Optional[float] = Field(None, gt=0, description="Luas lahan/bedengan (m2)")
    plant_count: Optional[int] = Field(None, gt=0, description="Total tanaman dalam batch/house")
    house_name: Optional[str] = Field("House 1", description="Nama greenhouse")
    beds_count: Optional[int] = Field(12, ge=1, description="Jumlah bedengan dalam house")
    bed_length_m: Optional[float] = Field(50.0, ge=1.0, description="Panjang bedengan (meter)")
    rows_per_bed: Optional[int] = Field(6, ge=1, description="Jumlah baris per bedengan")
    plant_spacing_cm: Optional[float] = Field(12.5, ge=1.0, description="Jarak tanam dalam baris (cm)")
    notes: Optional[str] = None


class BatchUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None
    target_harvest_date: Optional[str] = None


class GrowthRecordCreate(BaseModel):
    batch_id: str = Field(..., description="ID batch tanam")
    week_number: int = Field(..., ge=1, le=20)
    recording_date: str = Field(..., json_schema_extra={"example": "2026-08-05"})
    plant_height_cm: float = Field(..., gt=0, json_schema_extra={"example": 32.5})
    leaf_count: Optional[int] = Field(None, ge=0)
    stem_diameter_mm: Optional[float] = Field(None, ge=0)
    branch_count: Optional[int] = Field(None, ge=0)
    bud_count: Optional[int] = Field(0, ge=0)
    temperature_c: Optional[float] = Field(None)
    humidity_pct: Optional[float] = Field(None, ge=0, le=100)
    weather_condition: Optional[str] = Field("cerah")
    notes: Optional[str] = None


class GrowthRecordUpdate(BaseModel):
    plant_height_cm: Optional[float] = None
    leaf_count: Optional[int] = None
    stem_diameter_mm: Optional[float] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class HarvestRecordCreate(BaseModel):
    batch_id: str
    harvest_date: str
    total_stems: int = Field(..., gt=0)
    grade_a_stems: int = Field(0, ge=0)
    grade_b_stems: int = Field(0, ge=0)
    grade_c_stems: int = Field(0, ge=0)
    grade_a_price: int = Field(0, ge=0)
    grade_b_price: int = Field(0, ge=0)
    grade_c_price: int = Field(0, ge=0)
    production_cost: int = Field(0, ge=0)
    notes: Optional[str] = None
