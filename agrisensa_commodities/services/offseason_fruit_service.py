"""
Off-Season Tropical Fruit Service
Provides calculators and protocol generators for off-season cultivation
"""

import sys
from pathlib import Path
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.data.tropical_fruit_database import TROPICAL_FRUITS_DB, get_fruit_data
from datetime import datetime, timedelta
import pandas as pd


class OffSeasonFruitService:
    """Service for off-season tropical fruit cultivation"""
    
    def __init__(self):
        self.fruits_db = TROPICAL_FRUITS_DB
    
    def get_available_fruits(self):
        """Get list of available fruits"""
        return [
            {
                "key": key,
                "name": data["name_id"],
                "scientific": data["scientific"],
                "icon": data["icon"],
                "nickname": data["nickname"]
            }
            for key, data in self.fruits_db.items()
        ]
    
    def get_fruit_info(self, fruit_key):
        """Get complete fruit information"""
        return get_fruit_data(fruit_key)
    
    def calculate_roi(self, fruit_key, num_trees=100):
        """Calculate ROI for off-season production"""
        fruit = get_fruit_data(fruit_key)
        if not fruit:
            return None
        
        econ = fruit["economic_analysis"]
        
        # Normal season
        normal_revenue_total = econ["normal_revenue"] * num_trees
        normal_cost = 0  # Baseline
        normal_profit = normal_revenue_total
        
        # Off-season
        offseason_revenue_total = econ["offseason_revenue"] * num_trees
        offseason_cost = econ["extra_cost"] * num_trees
        offseason_profit = offseason_revenue_total - offseason_cost
        
        # Comparison
        profit_increase = offseason_profit - normal_profit
        roi = (profit_increase / offseason_cost * 100) if offseason_cost > 0 else 0
        
        return {
            "num_trees": num_trees,
            "normal": {
                "revenue": normal_revenue_total,
                "cost": normal_cost,
                "profit": normal_profit,
                "per_tree": econ["normal_revenue"]
            },
            "offseason": {
                "revenue": offseason_revenue_total,
                "cost": offseason_cost,
                "profit": offseason_profit,
                "per_tree": econ["offseason_revenue"]
            },
            "comparison": {
                "profit_increase": profit_increase,
                "roi_percentage": roi,
                "revenue_multiplier": fruit["market_info"]["price_multiplier"]
            }
        }
    
    def generate_water_stress_schedule(self, fruit_key, start_date):
        """Generate water stress protocol schedule"""
        fruit = get_fruit_data(fruit_key)
        if not fruit:
            return None
        
        protocol = fruit["water_stress_protocol"]
        schedule = []
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        
        for phase_key in ["phase_1", "phase_2", "phase_3"]:
            phase = protocol[phase_key]
            
            # Parse duration (e.g., "4-6 minggu" -> take average)
            duration_str = phase["duration"]
            if "-" in duration_str:
                min_weeks, max_weeks = duration_str.split("-")
                weeks = (int(min_weeks) + int(max_weeks.split()[0])) / 2
            else:
                weeks = int(duration_str.split()[0])
            
            end_date = current_date + timedelta(weeks=weeks)
            
            schedule.append({
                "phase": phase["name"],
                "start_date": current_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "duration_weeks": weeks,
                "action": phase["action"],
                "indicator": phase["indicator"]
            })
            
            current_date = end_date
        
        # Add expected flowering date
        flowering_date = current_date + timedelta(weeks=2)
        harvest_date = flowering_date + timedelta(weeks=16)  # ~4 months
        
        return {
            "schedule": schedule,
            "expected_flowering": flowering_date.strftime("%Y-%m-%d"),
            "expected_harvest": harvest_date.strftime("%Y-%m-%d"),
            "total_duration_weeks": sum([s["duration_weeks"] for s in schedule])
        }
    
    def calculate_pbz_dosage(self, fruit_key, tree_age_years, tree_circumference_cm):
        """Calculate PBZ dosage based on tree size"""
        fruit = get_fruit_data(fruit_key)
        if not fruit:
            return None
        
        params = fruit["cultivation_params"]
        dosage_range = params["pbz_dosage"]
        
        # Parse dosage range
        if "-" in dosage_range:
            min_dose, max_dose = dosage_range.split("-")
            min_dose = float(min_dose)
            max_dose = float(max_dose.split()[0])
        else:
            min_dose = max_dose = float(dosage_range.split()[0])
        
        # Calculate based on tree age and size
        if tree_age_years < 5:
            dosage = min_dose
        elif tree_age_years > 15:
            dosage = max_dose
        else:
            # Linear interpolation
            dosage = min_dose + (max_dose - min_dose) * (tree_age_years - 5) / 10
        
        # Adjust for tree size (circumference)
        if tree_circumference_cm < 50:
            dosage *= 0.8
        elif tree_circumference_cm > 100:
            dosage *= 1.2
        
        return {
            "dosage_grams": round(dosage, 2),
            "dosage_range": dosage_range,
            "application_method": "Soil drench atau injeksi batang",
            "timing": params["pbz_timing"],
            "safety_note": "⚠️ Jangan overdosis! PBZ bisa hambat pertumbuhan permanen",
            "dilution": f"{dosage} gram dalam 5-10 liter air per pohon"
        }
    
    def generate_fertilization_schedule(self, fruit_key, start_date, num_months=6):
        """Generate fertilization schedule"""
        fruit = get_fruit_data(fruit_key)
        if not fruit:
            return None
        
        fert_program = fruit["fertilization_program"]
        schedule = []
        current_date = datetime.strptime(start_date, "%Y-%m-%d")
        
        # Pre-stress phase (2 months)
        for month in range(2):
            schedule.append({
                "date": (current_date + timedelta(days=month*30)).strftime("%Y-%m-%d"),
                "phase": "Pre-Stress (Vegetatif)",
                "npk_ratio": fert_program["pre_stress"]["npk_ratio"],
                "dosage": fert_program["pre_stress"]["dosage"],
                "organic": fert_program["pre_stress"]["organic"] if month == 0 else "-",
                "notes": "Pupuk dasar untuk pertumbuhan"
            })
        
        # Pre-flowering (1 application)
        schedule.append({
            "date": (current_date + timedelta(days=60)).strftime("%Y-%m-%d"),
            "phase": "Pre-Flowering",
            "npk_ratio": fert_program["pre_flowering"]["npk_ratio"],
            "dosage": fert_program["pre_flowering"]["dosage"],
            "organic": "-",
            "notes": "Tinggi P-K untuk inisiasi bunga + " + fert_program["pre_flowering"]["micronutrients"]
        })
        
        # Flowering & fruiting (monthly)
        for month in range(3):
            schedule.append({
                "date": (current_date + timedelta(days=90+month*30)).strftime("%Y-%m-%d"),
                "phase": "Flowering & Fruiting",
                "npk_ratio": fert_program["flowering_fruiting"]["npk_ratio"],
                "dosage": fert_program["flowering_fruiting"]["dosage"],
                "organic": "-",
                "notes": f"Foliar: B {fert_program['flowering_fruiting']['boron']}, Ca {fert_program['flowering_fruiting']['calcium']}"
            })
        
        return schedule
    
    def get_market_timing_recommendation(self, fruit_key, current_month):
        """Get market timing recommendation"""
        fruit = get_fruit_data(fruit_key)
        if not fruit:
            return None
        
        market = fruit["market_info"]
        
        # Parse normal season
        normal_season = market["normal_season"]
        off_season_target = market["off_season_target"]
        
        return {
            "fruit": fruit["name_id"],
            "normal_season": normal_season,
            "normal_price": f"Rp {market['price_normal']:,}/kg",
            "off_season_target": off_season_target,
            "off_season_price": f"Rp {market['price_offseason']:,}/kg",
            "price_multiplier": f"{market['price_multiplier']}x",
            "export_potential": market["export_potential"],
            "recommendation": self._get_timing_advice(current_month, normal_season, off_season_target)
        }
    
    def _get_timing_advice(self, current_month, normal_season, off_season_target):
        """Generate timing advice based on current month"""
        # Simple logic - can be enhanced
        month_names = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                      "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        
        current_month_name = month_names[current_month - 1]
        
        if "Juni" in off_season_target or "Juli" in off_season_target:
            if current_month in [1, 2, 3]:
                return f"✅ Waktu IDEAL untuk mulai program off-season (target panen {off_season_target})"
            elif current_month in [4, 5, 6]:
                return f"⚠️ Sudah agak terlambat, tapi masih bisa dicoba"
            else:
                return f"❌ Terlalu terlambat untuk target {off_season_target}, tunggu tahun depan"
        
        return "Konsultasikan dengan kalender tanam untuk timing optimal"
    
    def get_scientific_references(self, fruit_key):
        """Get scientific references for a fruit"""
        fruit = get_fruit_data(fruit_key)
        if not fruit:
            return []
        
        return fruit.get("references", [])
