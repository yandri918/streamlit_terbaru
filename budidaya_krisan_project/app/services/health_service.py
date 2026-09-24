"""
Health Scoring Service — Budidaya Krisan Pro
Wraps HealthScorer from utils/health_scoring.py with
fallback multi-factor weighted algorithm.
"""
import sys
import os
from typing import Dict, List, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from utils.health_scoring import HealthScorer, HealthDiagnostics
    HEALTH_LIB_AVAILABLE = True
except ImportError:
    HEALTH_LIB_AVAILABLE = False

from app.services.ai_growth_service import get_standard_for_week, compute_growth_deviation

# Score thresholds
GRADE_THRESHOLDS = {"A": 80, "B": 60, "C": 40, "D": 20}


def compute_health_score(
    week: int,
    height: float,
    leaf_count: Optional[int] = None,
    stem_diameter: Optional[float] = None,
    branch_count: Optional[int] = None,
    temperature: Optional[float] = None,
    humidity: Optional[float] = None,
    history: Optional[List[Dict]] = None,
) -> Dict:
    """
    Multi-factor weighted health score (0-100):
    - Growth Score     (35%): Tinggi aktual vs standar ideal minggu
    - Morphology Score (25%): Daun, diameter batang, jumlah cabang
    - Environment Score(20%): Suhu & kelembaban optimal
    - Consistency Score(15%): Konsistensi tren pertumbuhan
    - Prediction Score (5%):  Deviasi dari ideal
    """
    std = get_standard_for_week(week)
    deviation = compute_growth_deviation(height, week)

    # 1. Growth Score (35%)
    ideal = std["height_ideal"]
    h_min, h_max = std["height_min"], std["height_max"]
    if h_min <= height <= h_max:
        growth_score = 90 + min(10, (1 - abs(deviation) / 30) * 10)
    elif height < h_min:
        deficit_pct = abs(height - ideal) / ideal * 100
        growth_score = max(0, 90 - deficit_pct * 2)
    else:
        excess_pct = (height - h_max) / h_max * 100
        growth_score = max(50, 90 - excess_pct)
    growth_score = min(100, max(0, growth_score))

    # 2. Morphology Score (25%)
    morph_score = 70.0
    if leaf_count is not None:
        ideal_leaves = max(6, week * 2)
        leaf_ratio = min(leaf_count / ideal_leaves, 1.5)
        morph_score += min(15, leaf_ratio * 10)
    if stem_diameter is not None:
        ideal_diam = 4 + week * 0.35
        diam_ratio = stem_diameter / ideal_diam
        morph_score += min(10, min(diam_ratio, 1.2) * 8)
    if branch_count is not None and week >= 7:
        ideal_branches = 4
        morph_score += min(5, (branch_count / ideal_branches) * 5)
    morph_score = min(100, max(0, morph_score))

    # 3. Environment Score (20%)
    env_score = 75.0
    if temperature is not None:
        # Optimal: 15-22°C untuk krisan dataran tinggi
        if 15 <= temperature <= 22:
            env_score += 20
        elif 10 <= temperature <= 25:
            env_score += 10
        else:
            env_score -= 15
    if humidity is not None:
        # Optimal: 70-85% RH
        if 70 <= humidity <= 85:
            env_score += 5
        elif 60 <= humidity <= 90:
            env_score += 2
    env_score = min(100, max(0, env_score))

    # 4. Consistency Score (15%)
    consistency_score = 70.0
    if history and len(history) >= 2:
        heights = [r.get("plant_height_cm", 0) for r in history[-4:]]
        heights.append(height)
        if len(heights) >= 3:
            diffs = [heights[i+1] - heights[i] for i in range(len(heights)-1)]
            avg_diff = sum(diffs) / len(diffs)
            if avg_diff > 0:
                consistency_score = min(100, 70 + avg_diff * 1.5)
            else:
                consistency_score = max(20, 70 + avg_diff * 3)
    consistency_score = min(100, max(0, consistency_score))

    # 5. Prediction Score (5%)
    pred_score = max(0, 100 - abs(deviation) * 2)

    # Weighted total
    total = (
        growth_score * 0.35 +
        morph_score * 0.25 +
        env_score * 0.20 +
        consistency_score * 0.15 +
        pred_score * 0.05
    )
    total = round(min(100, max(0, total)), 1)

    # Determine grade
    grade = "F"
    for g, threshold in GRADE_THRESHOLDS.items():
        if total >= threshold:
            grade = g
            break

    return {
        "total_score": total,
        "ai_grade": grade,
        "growth_deviation_pct": round(deviation, 2),
        "breakdown": {
            "growth_score": round(growth_score, 1),
            "morphology_score": round(morph_score, 1),
            "environment_score": round(env_score, 1),
            "consistency_score": round(consistency_score, 1),
            "prediction_score": round(pred_score, 1),
        },
    }


def get_health_recommendations(health_result: Dict, week: int, height: float) -> List[Dict]:
    """Generate priority-ranked recommendations based on health result."""
    score = health_result.get("total_score", 0)
    deviation = health_result.get("growth_deviation_pct", 0)
    breakdown = health_result.get("breakdown", {})
    recs = []

    # Critical alerts
    if score < 40:
        recs.append({"priority": "CRITICAL", "icon": "🚨",
            "title": "Kondisi Tanaman Kritis",
            "action": "Lakukan pemeriksaan menyeluruh segera. Cek akar, hama, dan kondisi media tanam."})

    # Growth deviation
    if deviation < -20:
        recs.append({"priority": "HIGH", "icon": "📉",
            "title": f"Pertumbuhan Jauh Tertinggal ({abs(deviation):.1f}% di bawah standar)",
            "action": "Tingkatkan dosis Nitrogen (N) 20-25%. Pastikan irigasi cukup dan tidak ada kompetisi antar tanaman."})
    elif deviation < -10:
        recs.append({"priority": "MEDIUM", "icon": "⚠️",
            "title": f"Pertumbuhan Sedikit Tertinggal ({abs(deviation):.1f}%)",
            "action": "Tambahkan pupuk N-P-K 25:7:7 setiap 5 hari. Pastikan drainase baik."})
    elif deviation > 20:
        recs.append({"priority": "MEDIUM", "icon": "📈",
            "title": f"Pertumbuhan Melebihi Standar ({deviation:.1f}%)",
            "action": "Kurangi nitrogen, tambahkan kalium (K) untuk memperkuat batang. Awasi potensi etiolasi."})

    # Environment
    env_score = breakdown.get("environment_score", 0)
    if env_score < 60:
        recs.append({"priority": "HIGH", "icon": "🌡️",
            "title": "Lingkungan Tidak Optimal",
            "action": "Sesuaikan ventilasi greenhouse. Target: suhu 15-22°C, kelembaban 70-85% RH."})

    # Morphology
    morph_score = breakdown.get("morphology_score", 0)
    if morph_score < 55:
        recs.append({"priority": "MEDIUM", "icon": "🌿",
            "title": "Perkembangan Morfologi Kurang Baik",
            "action": "Cek ketersediaan Fosfor (P) dan Kalsium (Ca). Pertimbangkan foliar spray ZA + Boron."})

    # Week-specific advice
    if week == 7:
        recs.append({"priority": "INFO", "icon": "✂️",
            "title": "Minggu 7 — Waktu Pinching",
            "action": "Lakukan pinching (pemotongan pucuk) untuk mendorong pembentukan cabang produktif."})
    elif week == 9:
        recs.append({"priority": "INFO", "icon": "🌙",
            "title": "Minggu 9 — Mulai Short Day Treatment",
            "action": "Pasang plastik hitam 13-14 jam/hari untuk menginduksi pembungaan (photoperiod)."})
    elif week >= 14:
        recs.append({"priority": "INFO", "icon": "🌸",
            "title": "Mendekati Waktu Panen",
            "action": "Monitor kematangan bunga (50-60% mekar). Siapkan sarana panen dan penanganan pasca panen."})

    if not recs:
        recs.append({"priority": "INFO", "icon": "✅",
            "title": "Pertumbuhan Berjalan Optimal",
            "action": "Pertahankan jadwal pemupukan dan irigasi saat ini. Lanjutkan monitoring mingguan."})

    return recs
