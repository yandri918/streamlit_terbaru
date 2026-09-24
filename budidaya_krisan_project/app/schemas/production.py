"""
Production & Population Schemas — Budidaya Krisan Pro
Includes house population calculator & economic production schemas.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class HousePopulationInput(BaseModel):
    house_name: str = Field("House 1", description="Nama greenhouse / house")
    beds: int = Field(12, ge=1, le=100, description="Jumlah bedengan dalam house")
    bed_length: float = Field(50.0, ge=1.0, le=200.0, description="Panjang bedengan (meter)")
    bed_width: float = Field(100.0, ge=10.0, le=300.0, description="Lebar bedengan (cm)")
    rows_per_bed: int = Field(6, ge=1, le=20, description="Jumlah baris per bedengan")
    plant_spacing: float = Field(12.5, ge=5.0, le=50.0, description="Jarak tanam dalam baris (cm)")
    survival_rate: float = Field(85.0, ge=0.0, le=100.0, description="Estimasi survival rate (%)")
    stems_per_plant: float = Field(3.5, ge=0.1, le=20.0, description="Estimasi tangkai per tanaman")
    beds_putih: Optional[int] = Field(None, ge=0, description="Jumlah bedengan varietas putih")
    beds_pink: Optional[int] = Field(None, ge=0, description="Jumlah bedengan varietas pink")
    beds_kuning: Optional[int] = Field(None, ge=0, description="Jumlah bedengan varietas kuning")


class MultiHousePopulationInput(BaseModel):
    houses: List[HousePopulationInput] = Field(..., description="Daftar konfigurasi house")


class ProductionCalcInput(BaseModel):
    land_area_m2: float = Field(..., gt=0, json_schema_extra={"example": 100})
    plant_density: float = Field(64.0, description="Tanaman per m2", json_schema_extra={"example": 64})
    expected_stems_per_plant: float = Field(4.0, json_schema_extra={"example": 4})
    grade_a_pct: float = Field(0.65, ge=0, le=1)
    grade_b_pct: float = Field(0.25, ge=0, le=1)
    grade_c_pct: float = Field(0.10, ge=0, le=1)
    grade_a_price: int = Field(25000, ge=0)
    grade_b_price: int = Field(18000, ge=0)
    grade_c_price: int = Field(10000, ge=0)
    production_cost_per_m2: int = Field(75000, ge=0)
    cycle_count_per_year: int = Field(3, ge=1, le=5)


class ProductionCalcResult(BaseModel):
    land_area_m2: float
    total_plants: int
    total_stems: int
    grade_a_stems: int
    grade_b_stems: int
    grade_c_stems: int
    gross_revenue: int
    production_cost: int
    net_profit: int
    roi_pct: float
    bep_per_stem: float
    productivity_stems_per_m2: float
    annual_revenue: int
    annual_profit: int
