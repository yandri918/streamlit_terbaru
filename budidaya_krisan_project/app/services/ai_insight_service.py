"""
AI Insight Service — AgriSensa-style Benchmark Evaluator for Budidaya Krisan Pro
Evaluates cultivation performance against Balithi chrysanthemum standards.
"""
from typing import Dict, List, Optional
from app.services.db import get_db
from app.services.ai_growth_service import GROWTH_STANDARDS

# Standard references (Balai Penelitian Tanaman Hias / Balithi)
KRISAN_BENCHMARKS = {
    "standard_name": "Standar Balithi — Krisan Spray Jepang",
    "standard_yield_stems_per_m2": 25,        # tangkai/m²/siklus
    "standard_health_score_threshold": 75,     # skor ≥ 75 = baik
    "standard_grade_a_pct": 65,               # % Grade A ideal
    "standard_loss_rate_pct": 8,              # % susut wajar
    "standard_cycle_days": 112,               # hari standar 1 siklus
    "standard_roi_pct": 60,                   # ROI minimum sehat
}


def get_ai_insights(variety_filter: Optional[str] = None) -> Dict:
    """
    Benchmark AI evaluator — evaluates actual cultivation vs Balithi standard.
    Returns composite score, rating stars, status, and recommendations.
    """
    with get_db() as conn:
        # Actual productivity
        harvest_data = conn.execute(
            "SELECT h.total_stems, h.grade_a_stems, h.grade_b_stems, h.grade_c_stems, "
            "h.roi_pct, h.marketable_yield_pct, h.loss_rate_pct, b.land_area_m2 "
            "FROM harvest_records h JOIN cultivation_batches b ON h.batch_id=b.id"
            + (" WHERE b.variety_name=?" if variety_filter else ""),
            [variety_filter] if variety_filter else []
        ).fetchall()

        avg_health = conn.execute(
            "SELECT AVG(health_score) as avg FROM growth_records"
        ).fetchone()

        active_count = conn.execute(
            "SELECT COUNT(*) as cnt FROM cultivation_batches WHERE status='active'"
        ).fetchone()

    # Compute actual metrics
    if harvest_data:
        total_stems = sum(r["total_stems"] for r in harvest_data)
        total_area = sum(r["land_area_m2"] for r in harvest_data)
        total_grade_a = sum(r["grade_a_stems"] for r in harvest_data)
        avg_roi = sum(r["roi_pct"] for r in harvest_data) / len(harvest_data)
        avg_loss = sum(r["loss_rate_pct"] for r in harvest_data) / len(harvest_data)
        actual_yield_per_m2 = round(total_stems / max(1, total_area), 2)
        actual_grade_a_pct = round(total_grade_a / max(1, total_stems) * 100, 1)
    else:
        actual_yield_per_m2 = 0
        actual_grade_a_pct = 0
        avg_roi = 0
        avg_loss = 0

    avg_health_score = round(avg_health["avg"] or 0, 1)
    std_yield = KRISAN_BENCHMARKS["standard_yield_stems_per_m2"]

    # Deviation formula: ΔP(%) = (aktual - standar) / standar × 100
    if std_yield > 0 and actual_yield_per_m2 > 0:
        deviation_pct = round((actual_yield_per_m2 - std_yield) / std_yield * 100, 2)
    else:
        deviation_pct = 0.0

    # Composite Score (0-100) — multi-criteria
    scores = []
    # Yield score
    if actual_yield_per_m2 > 0:
        yield_score = min(100, (actual_yield_per_m2 / std_yield) * 80)
        scores.append(yield_score)
    # Health score
    scores.append(min(100, avg_health_score))
    # Grade A score
    if actual_grade_a_pct > 0:
        scores.append(min(100, actual_grade_a_pct / KRISAN_BENCHMARKS["standard_grade_a_pct"] * 75))
    # ROI score
    if avg_roi > 0:
        scores.append(min(100, avg_roi / KRISAN_BENCHMARKS["standard_roi_pct"] * 80))
    # Loss rate score (inverse)
    if avg_loss > 0:
        loss_score = max(0, 100 - (avg_loss - KRISAN_BENCHMARKS["standard_loss_rate_pct"]) * 5)
        scores.append(loss_score)

    composite_score = round(sum(scores) / len(scores) if scores else 50, 1)

    # Rating stars (1-5)
    rating = 5 if composite_score >= 85 else (
             4 if composite_score >= 70 else (
             3 if composite_score >= 55 else (
             2 if composite_score >= 35 else 1)))

    status_map = {5: "Sangat Unggul", 4: "Baik", 3: "Cukup", 2: "Perlu Perbaikan", 1: "Kritis"}

    # Recommendations
    recommendations = _generate_recommendations(
        deviation_pct, avg_health_score, actual_grade_a_pct,
        avg_roi, avg_loss, active_count["cnt"]
    )

    return {
        "benchmark_name": KRISAN_BENCHMARKS["standard_name"],
        "standard_yield_stems_per_m2": std_yield,
        "actual_yield_stems_per_m2": actual_yield_per_m2,
        "deviation_pct": deviation_pct,
        "avg_health_score": avg_health_score,
        "actual_grade_a_pct": actual_grade_a_pct,
        "avg_roi_pct": round(avg_roi, 1),
        "avg_loss_rate_pct": round(avg_loss, 1),
        "composite_score": composite_score,
        "rating_stars": rating,
        "status": status_map[rating],
        "active_batches": active_count["cnt"],
        "has_harvest_data": len(harvest_data) > 0,
        "recommendations": recommendations,
    }


def _generate_recommendations(
    deviation: float, health: float, grade_a_pct: float,
    roi: float, loss: float, active_count: int
) -> List[str]:
    recs = []

    if active_count == 0:
        recs.append("🌱 Mulai batch tanam pertama Anda. Rekam data pertumbuhan mingguan untuk mendapatkan analisis AI.")
        return recs

    if deviation < -15:
        recs.append(f"📉 Produktivitas {abs(deviation):.1f}% di bawah standar Balithi. Evaluasi kepadatan tanam dan program pemupukan NPK.")
    elif deviation > 15:
        recs.append(f"✅ Produktivitas {deviation:.1f}% di atas standar nasional. Pertahankan praktik budidaya terbaik ini.")

    if health < 65:
        recs.append("⚠️ Rata-rata health score rendah. Tingkatkan pemantauan hama-penyakit dan kondisi lingkungan greenhouse.")
    elif health >= 80:
        recs.append("🏆 Health score sangat baik. Konsistensi program pemupukan dan irigasi terbukti efektif.")

    if grade_a_pct > 0 and grade_a_pct < 50:
        recs.append(f"🎯 Grade A hanya {grade_a_pct:.1f}%. Optimalkan nutrisi Ca-B (Kalsium-Boron) untuk meningkatkan kualitas bunga.")
    elif grade_a_pct >= 70:
        recs.append(f"🌸 Grade A mencapai {grade_a_pct:.1f}% — melampaui standar 65%. Kualitas produksi sangat baik.")

    if roi > 0 and roi < 40:
        recs.append(f"💰 ROI {roi:.1f}% masih di bawah optimal. Evaluasi efisiensi biaya produksi dan harga jual per tangkai.")

    if loss > 12:
        recs.append(f"📦 Susut pascapanen {loss:.1f}% melebihi toleransi 8%. Perbaiki teknik grading, penyimpanan suhu dingin, dan transportasi.")

    recs.append("📅 Rekam data pertumbuhan setiap minggu untuk prediksi panen yang lebih akurat.")

    return recs[:5]
