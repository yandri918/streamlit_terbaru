"""
Production Router — Population & Economics Calculator
POST /api/v1/production/house-population       - Calculate population for 1 house
POST /api/v1/production/multi-house-population - Calculate population across multiple houses
POST /api/v1/production/calculate              - Economic calculator (RAB, revenue, ROI)
"""
from fastapi import APIRouter
from app.schemas.common import ApiResponse
from app.schemas.production import (
    HousePopulationInput,
    MultiHousePopulationInput,
    ProductionCalcInput,
    ProductionCalcResult,
)
from app.services.population_service import (
    calculate_house_population,
    calculate_multi_house_summary,
)

router = APIRouter(prefix="/production", tags=["Production & Population"])


@router.post("/house-population", response_model=ApiResponse)
def calculate_house(payload: HousePopulationInput):
    """
    Hitung populasi tanaman per house sesuai rumus standar krisan spray:
    - Tanaman/baris = int((panjang_bedeng * 100) / jarak_tanam)
    - Tanaman/bedeng = tanaman/baris * baris_per_bedeng
    - Total tanaman/house = tanaman/bedeng * jumlah_bedengan
    """
    result = calculate_house_population(
        beds=payload.beds,
        bed_length=payload.bed_length,
        bed_width=payload.bed_width,
        rows_per_bed=payload.rows_per_bed,
        plant_spacing=payload.plant_spacing,
        survival_rate=payload.survival_rate,
        stems_per_plant=payload.stems_per_plant,
        beds_putih=payload.beds_putih,
        beds_pink=payload.beds_pink,
        beds_kuning=payload.beds_kuning,
        house_name=payload.house_name,
    )
    return ApiResponse.ok(result, f"Kalkulasi populasi {payload.house_name} berhasil dihitung.")


@router.post("/multi-house-population", response_model=ApiResponse)
def calculate_multi_house(payload: MultiHousePopulationInput):
    """
    Kalkulasi agregat untuk beberapa house (House 1, House 2, dst).
    """
    house_dicts = [h.model_dump() for h in payload.houses]
    result = calculate_multi_house_summary(house_dicts)
    return ApiResponse.ok(result, f"Kalkulasi {len(payload.houses)} house berhasil dihitung.")


@router.post("/calculate", response_model=ApiResponse)
def calculate_production_economics(payload: ProductionCalcInput):
    """
    Kalkulator estimasi ekonomi produksi krisan spray.
    """
    total_plants = int(payload.land_area_m2 * payload.plant_density)
    total_stems = int(total_plants * payload.expected_stems_per_plant)

    grade_a = int(total_stems * payload.grade_a_pct)
    grade_b = int(total_stems * payload.grade_b_pct)
    grade_c = total_stems - (grade_a + grade_b)

    gross_revenue = (
        grade_a * payload.grade_a_price +
        grade_b * payload.grade_b_price +
        grade_c * payload.grade_c_price
    )
    production_cost = int(payload.land_area_m2 * payload.production_cost_per_m2)
    net_profit = gross_revenue - production_cost
    roi = round((net_profit / max(1, production_cost)) * 100, 2)
    bep = round(production_cost / max(1, total_stems), 2)
    productivity = round(total_stems / max(1.0, payload.land_area_m2), 2)
    annual_revenue = gross_revenue * payload.cycle_count_per_year
    annual_profit = net_profit * payload.cycle_count_per_year

    result = ProductionCalcResult(
        land_area_m2=payload.land_area_m2,
        total_plants=total_plants,
        total_stems=total_stems,
        grade_a_stems=grade_a,
        grade_b_stems=grade_b,
        grade_c_stems=grade_c,
        gross_revenue=gross_revenue,
        production_cost=production_cost,
        net_profit=net_profit,
        roi_pct=roi,
        bep_per_stem=bep,
        productivity_stems_per_m2=productivity,
        annual_revenue=annual_revenue,
        annual_profit=annual_profit,
    )
    return ApiResponse.ok(result.model_dump(), "Kalkulasi produksi berhasil dilakukan.")
