"""
Population & House Calculation Service — Budidaya Krisan Pro
Implements exact population formulas from Kalkulator Produksi (pages/3_📊_Kalkulator_Produksi.py):
- plants_per_row = int((bed_length * 100) / plant_spacing)
- plants_per_bed = plants_per_row * rows_per_bed
- total_plants_house = plants_per_bed * beds_per_house
- bed_area_m2 = bed_length * (bed_width / 100) * beds_per_house
- actual_density = total_plants / bed_area_m2
- surviving_plants = int(total_plants * (survival_rate / 100))
- total_stems = int(surviving_plants * stems_per_plant)
- variety breakdown (Putih, Pink, Kuning)
"""
from typing import Dict, List, Optional, Any


# Master standard constants
DEFAULT_BEDS_PER_HOUSE = 12
DEFAULT_BED_LENGTH_M = 50.0
DEFAULT_BED_WIDTH_CM = 100.0
DEFAULT_ROWS_PER_BED = 6
DEFAULT_PLANT_SPACING_CM = 12.5
DEFAULT_SURVIVAL_RATE_PCT = 85.0
DEFAULT_STEMS_PER_PLANT = 3.5


def calculate_house_population(
    beds: int = DEFAULT_BEDS_PER_HOUSE,
    bed_length: float = DEFAULT_BED_LENGTH_M,
    bed_width: float = DEFAULT_BED_WIDTH_CM,
    rows_per_bed: int = DEFAULT_ROWS_PER_BED,
    plant_spacing: float = DEFAULT_PLANT_SPACING_CM,
    survival_rate: float = DEFAULT_SURVIVAL_RATE_PCT,
    stems_per_plant: float = DEFAULT_STEMS_PER_PLANT,
    beds_putih: Optional[int] = None,
    beds_pink: Optional[int] = None,
    beds_kuning: Optional[int] = None,
    house_name: str = "House 1",
) -> Dict[str, Any]:
    """
    Hitung populasi tanaman untuk 1 house greenhouse krisan spray
    sesuai logika asli Kalkulator Produksi.
    """
    # Guard zero / negative
    beds = max(1, int(beds))
    bed_length = max(1.0, float(bed_length))
    bed_width = max(10.0, float(bed_width))
    rows_per_bed = max(1, int(rows_per_bed))
    plant_spacing = max(1.0, float(plant_spacing))
    survival_rate = max(0.0, min(100.0, float(survival_rate)))
    stems_per_plant = max(0.1, float(stems_per_plant))

    # Core formulas from original Streamlit app
    plants_per_row = int((bed_length * 100.0) / plant_spacing)
    plants_per_bed = plants_per_row * rows_per_bed
    total_plants = plants_per_bed * beds

    bed_area_single_m2 = round(bed_length * (bed_width / 100.0), 2)
    total_bed_area_m2 = round(bed_area_single_m2 * beds, 2)

    actual_density = round(total_plants / total_bed_area_m2, 2) if total_bed_area_m2 > 0 else 0.0
    surviving_plants = int(total_plants * (survival_rate / 100.0))
    total_stems = int(surviving_plants * stems_per_plant)

    # Variety distribution (default split if not provided: 1/3 each)
    if beds_putih is None and beds_pink is None and beds_kuning is None:
        p_beds = beds // 3
        k_beds = beds // 3
        y_beds = beds - (p_beds + k_beds)
    else:
        p_beds = max(0, int(beds_putih or 0))
        k_beds = max(0, int(beds_pink or 0))
        y_beds = max(0, int(beds_kuning or 0))

    variety_breakdown = {
        "putih": {
            "beds": p_beds,
            "plants": p_beds * plants_per_bed,
            "stems_est": int(p_beds * plants_per_bed * (survival_rate / 100.0) * stems_per_plant),
        },
        "pink": {
            "beds": k_beds,
            "plants": k_beds * plants_per_bed,
            "stems_est": int(k_beds * plants_per_bed * (survival_rate / 100.0) * stems_per_plant),
        },
        "kuning": {
            "beds": y_beds,
            "plants": y_beds * plants_per_bed,
            "stems_est": int(y_beds * plants_per_bed * (survival_rate / 100.0) * stems_per_plant),
        },
    }

    return {
        "house_name": house_name,
        "parameters": {
            "beds": beds,
            "bed_length_m": bed_length,
            "bed_width_cm": bed_width,
            "rows_per_bed": rows_per_bed,
            "plant_spacing_cm": plant_spacing,
            "survival_rate_pct": survival_rate,
            "stems_per_plant": stems_per_plant,
        },
        "results": {
            "plants_per_row": plants_per_row,
            "plants_per_bed": plants_per_bed,
            "total_plants": total_plants,
            "bed_area_single_m2": bed_area_single_m2,
            "total_bed_area_m2": total_bed_area_m2,
            "actual_density_per_m2": actual_density,
            "surviving_plants": surviving_plants,
            "total_stems": total_stems,
        },
        "varieties": variety_breakdown,
        "is_variety_beds_valid": (p_beds + k_beds + y_beds) == beds,
    }


def calculate_multi_house_summary(houses: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Agregasi kalkulasi populasi untuk beberapa house (House 1, House 2, ... House N).
    """
    total_houses = len(houses)
    total_beds = 0
    total_plants = 0
    total_bed_area_m2 = 0.0
    total_surviving = 0
    total_stems = 0
    total_putih_plants = 0
    total_pink_plants = 0
    total_kuning_plants = 0

    house_results = []
    for idx, h in enumerate(houses):
        res = calculate_house_population(
            beds=h.get("beds", DEFAULT_BEDS_PER_HOUSE),
            bed_length=h.get("bed_length", DEFAULT_BED_LENGTH_M),
            bed_width=h.get("bed_width", DEFAULT_BED_WIDTH_CM),
            rows_per_bed=h.get("rows_per_bed", DEFAULT_ROWS_PER_BED),
            plant_spacing=h.get("plant_spacing", DEFAULT_PLANT_SPACING_CM),
            survival_rate=h.get("survival_rate", DEFAULT_SURVIVAL_RATE_PCT),
            stems_per_plant=h.get("stems_per_plant", DEFAULT_STEMS_PER_PLANT),
            beds_putih=h.get("beds_putih"),
            beds_pink=h.get("beds_pink"),
            beds_kuning=h.get("beds_kuning"),
            house_name=h.get("name", f"House {idx + 1}"),
        )
        house_results.append(res)
        total_beds += res["parameters"]["beds"]
        total_plants += res["results"]["total_plants"]
        total_bed_area_m2 += res["results"]["total_bed_area_m2"]
        total_surviving += res["results"]["surviving_plants"]
        total_stems += res["results"]["total_stems"]
        total_putih_plants += res["varieties"]["putih"]["plants"]
        total_pink_plants += res["varieties"]["pink"]["plants"]
        total_kuning_plants += res["varieties"]["kuning"]["plants"]

    avg_density = round(total_plants / total_bed_area_m2, 2) if total_bed_area_m2 > 0 else 0.0

    return {
        "total_houses": total_houses,
        "total_beds": total_beds,
        "total_plants": total_plants,
        "total_bed_area_m2": round(total_bed_area_m2, 2),
        "average_density_per_m2": avg_density,
        "total_surviving_plants": total_surviving,
        "total_stems_estimate": total_stems,
        "variety_totals": {
            "putih_plants": total_putih_plants,
            "pink_plants": total_pink_plants,
            "kuning_plants": total_kuning_plants,
        },
        "houses": house_results,
    }
