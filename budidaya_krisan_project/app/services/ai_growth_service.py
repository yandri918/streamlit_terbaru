"""
AI Growth Service — Budidaya Krisan Pro
Wraps existing ML models from utils/ai_growth_models.py into
FastAPI-compatible service functions.
"""
import sys
import os
from typing import Dict, List, Optional, Tuple
import numpy as np

# Ensure utils/ is importable from project root
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

try:
    from utils.ai_growth_models import GrowthPredictor, AnomalyDetector
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False


# ============================================================
# Standar Pertumbuhan Krisan Spray Jepang (Balithi Reference)
# Sumber: BSIP (Balai Pengkajian Teknologi Pertanian)
# ============================================================
GROWTH_STANDARDS: Dict[int, Dict] = {
    1:  {"height_ideal": 8,  "height_min": 5,  "height_max": 12,  "phase": "Adaptasi Stek"},
    2:  {"height_ideal": 14, "height_min": 10, "height_max": 18,  "phase": "Pertumbuhan Akar"},
    3:  {"height_ideal": 20, "height_min": 15, "height_max": 26,  "phase": "Vegetatif Awal"},
    4:  {"height_ideal": 27, "height_min": 21, "height_max": 33,  "phase": "Vegetatif Aktif"},
    5:  {"height_ideal": 34, "height_min": 27, "height_max": 41,  "phase": "Vegetatif Aktif"},
    6:  {"height_ideal": 41, "height_min": 33, "height_max": 49,  "phase": "Vegetatif Akhir"},
    7:  {"height_ideal": 47, "height_min": 38, "height_max": 55,  "phase": "Pinching"},
    8:  {"height_ideal": 52, "height_min": 43, "height_max": 61,  "phase": "Pasca Pinching"},
    9:  {"height_ideal": 56, "height_min": 46, "height_max": 65,  "phase": "Induksi Bunga"},
    10: {"height_ideal": 59, "height_min": 49, "height_max": 68,  "phase": "Kuncup Terbentuk"},
    11: {"height_ideal": 62, "height_min": 52, "height_max": 71,  "phase": "Kuncup Berkembang"},
    12: {"height_ideal": 65, "height_min": 55, "height_max": 74,  "phase": "Bunga Mekar"},
    13: {"height_ideal": 68, "height_min": 58, "height_max": 77,  "phase": "Bunga Mekar Penuh"},
    14: {"height_ideal": 71, "height_min": 61, "height_max": 80,  "phase": "Siap Panen"},
    15: {"height_ideal": 73, "height_min": 63, "height_max": 82,  "phase": "Panen Optimal"},
    16: {"height_ideal": 75, "height_min": 65, "height_max": 85,  "phase": "Panen Akhir"},
}


def get_standard_for_week(week: int) -> Dict:
    """Return growth standard for a given week."""
    if week in GROWTH_STANDARDS:
        return GROWTH_STANDARDS[week]
    elif week > 16:
        return GROWTH_STANDARDS[16]
    else:
        return GROWTH_STANDARDS[1]


def compute_growth_deviation(actual_height: float, week: int) -> float:
    """
    Hitung deviasi pertumbuhan vs standar ideal.
    ΔH(%) = (H_aktual - H_ideal) / H_ideal × 100
    """
    std = get_standard_for_week(week)
    ideal = std["height_ideal"]
    if ideal == 0:
        return 0.0
    return round(((actual_height - ideal) / ideal) * 100, 2)


def predict_growth(weeks: List[int], heights: List[float], weeks_ahead: int = 4) -> Optional[Dict]:
    """
    Predict future growth using polynomial regression.
    Returns predictions with confidence intervals.
    """
    if not ML_AVAILABLE or len(weeks) < 3:
        return _simple_linear_prediction(weeks, heights, weeks_ahead)

    try:
        predictor = GrowthPredictor(degree=3)
        predictor.fit(weeks, heights)
        result = predictor.predict(weeks_ahead=weeks_ahead)
        return result
    except Exception:
        return _simple_linear_prediction(weeks, heights, weeks_ahead)


def _simple_linear_prediction(weeks: List[int], heights: List[float], weeks_ahead: int) -> Dict:
    """Fallback simple linear prediction when ML unavailable."""
    if len(weeks) < 2:
        return {"predictions": [], "weeks": [], "confidence_lower": [], "confidence_upper": []}

    n = len(weeks)
    x = np.array(weeks, dtype=float)
    y = np.array(heights, dtype=float)
    slope = np.polyfit(x, y, 1)

    future_weeks = [max(weeks) + i for i in range(1, weeks_ahead + 1)]
    predictions = [float(np.polyval(slope, w)) for w in future_weeks]
    margin = np.std(y) * 1.2

    return {
        "predictions": [round(p, 2) for p in predictions],
        "weeks": future_weeks,
        "confidence_lower": [round(max(0, p - margin), 2) for p in predictions],
        "confidence_upper": [round(p + margin, 2) for p in predictions],
        "harvest_week_estimate": _estimate_harvest_week(predictions, future_weeks),
    }


def _estimate_harvest_week(predictions: List[float], weeks: List[int]) -> Optional[int]:
    """Estimate which week the plant reaches harvest height (65cm+)."""
    HARVEST_HEIGHT = 65.0
    for w, h in zip(weeks, predictions):
        if h >= HARVEST_HEIGHT:
            return w
    return None


def detect_anomalies(growth_data: List[Dict]) -> List[Dict]:
    """
    Detect growth anomalies using Isolation Forest.
    Returns list of records with anomaly flags.
    """
    if not ML_AVAILABLE or len(growth_data) < 5:
        return _rule_based_anomaly_detection(growth_data)

    try:
        detector = AnomalyDetector(contamination=0.15)
        standards_list = [get_standard_for_week(r.get("week_number", 1)) for r in growth_data]
        result = detector.detect(growth_data, standards_list)
        return result
    except Exception:
        return _rule_based_anomaly_detection(growth_data)


def _rule_based_anomaly_detection(growth_data: List[Dict]) -> List[Dict]:
    """Rule-based anomaly detection as fallback."""
    results = []
    for record in growth_data:
        week = record.get("week_number", 1)
        height = record.get("plant_height_cm", 0)
        std = get_standard_for_week(week)

        anomaly = False
        anomaly_type = None

        if height < std["height_min"]:
            anomaly = True
            deviation = abs(height - std["height_ideal"]) / std["height_ideal"] * 100
            anomaly_type = "STUNTED" if deviation > 30 else "SLOW_GROWTH"
        elif height > std["height_max"] * 1.15:
            anomaly = True
            anomaly_type = "EXCESSIVE_GROWTH"

        results.append({
            **record,
            "anomaly_detected": anomaly,
            "anomaly_type": anomaly_type,
        })
    return results


def get_all_standards() -> Dict[int, Dict]:
    return GROWTH_STANDARDS
