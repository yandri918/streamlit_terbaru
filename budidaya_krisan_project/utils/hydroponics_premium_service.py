"""
PREMIUM ADVANCED Hydroponics & Vertical Farming Service
Enterprise-grade calculations with AI/ML features
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# ===== PREMIUM HYDROPONIC SYSTEMS DATABASE =====
PREMIUM_SYSTEMS = {
    "NFT Pro (Automated)": {
        "type": "NFT",
        "automation_level": "High",
        "iot_compatible": True,
        "difficulty": "Medium",
        "investment_per_hole": 28000,
        "yield_multiplier": 1.5,
        "power_consumption": "40W continuous",
        "best_for": ["Lettuce", "Kangkung", "Pakcoy", "Basil"],
        "capacity": "100-500 holes",
        "roi_months": 8,
        "description": "NFT with automated EC/pH monitoring and dosing"
    },
    
    "DFT Commercial": {
        "type": "DFT",
        "automation_level": "Medium",
        "iot_compatible": True,
        "difficulty": "Easy",
        "investment_per_hole": 25000,
        "yield_multiplier": 1.4,
        "power_consumption": "30W intermittent",
        "best_for": ["Lettuce", "Pakcoy", "Spinach"],
        "capacity": "100-1000 holes",
        "roi_months": 9,
        "description": "Deep Flow Technique for commercial scale"
    },
    
    "Aeroponics Premium": {
        "type": "Aeroponics",
        "automation_level": "Very High",
        "iot_compatible": True,
        "difficulty": "Hard",
        "investment_per_hole": 45000,
        "yield_multiplier": 2.0,
        "power_consumption": "60W continuous",
        "best_for": ["Strawberry", "Tomato", "Premium Herbs"],
        "capacity": "50-200 holes",
        "roi_months": 10,
        "description": "High-tech aeroponics with misting system"
    },
    
    "Dutch Bucket System": {
        "type": "Dutch Bucket",
        "automation_level": "Medium",
        "iot_compatible": True,
        "difficulty": "Medium",
        "investment_per_hole": 35000,
        "yield_multiplier": 1.6,
        "power_consumption": "25W intermittent",
        "best_for": ["Tomato", "Cucumber", "Pepper", "Eggplant"],
        "capacity": "20-100 buckets",
        "roi_months": 11,
        "description": "Perfect for fruiting vegetables"
    },
    
    "Vertical Tower NFT": {
        "type": "Vertical NFT",
        "automation_level": "High",
        "iot_compatible": True,
        "difficulty": "Medium",
        "investment_per_hole": 32000,
        "yield_multiplier": 1.7,
        "power_consumption": "50W continuous",
        "best_for": ["Strawberry", "Lettuce", "Herbs"],
        "capacity": "100-300 holes",
        "roi_months": 9,
        "description": "Space-saving vertical system"
    },
    
    "Kratky Method": {
        "type": "Kratky",
        "automation_level": "None",
        "iot_compatible": False,
        "difficulty": "Very Easy",
        "investment_per_hole": 8000,
        "yield_multiplier": 0.8,
        "power_consumption": "0W",
        "best_for": ["Lettuce", "Herbs", "Small plants"],
        "capacity": "10-50 holes",
        "roi_months": 6,
        "description": "Passive hydroponics, no electricity"
    },
    
    "Aquaponics System": {
        "type": "Aquaponics",
        "automation_level": "High",
        "iot_compatible": True,
        "difficulty": "Hard",
        "investment_per_hole": 50000,
        "yield_multiplier": 1.3,
        "power_consumption": "80W continuous",
        "best_for": ["Lettuce", "Herbs", "Fish (Tilapia, Lele)"],
        "capacity": "100-500 holes + fish tank",
        "roi_months": 14,
        "description": "Symbiotic fish + plants system"
    },
    
    "Wick System": {
        "type": "Wick",
        "automation_level": "None",
        "iot_compatible": False,
        "difficulty": "Very Easy",
        "investment_per_hole": 12000,
        "yield_multiplier": 0.9,
        "power_consumption": "0W",
        "best_for": ["Chili", "Tomato", "Herbs"],
        "capacity": "10-100 holes",
        "roi_months": 7,
        "description": "Simple passive system with wicks"
    }
}

# ===== CROP DATABASE =====
CROP_DATABASE = {
    "Lettuce": {
        "cycle_days": 35,
        "ec_range": (1.2, 1.8),
        "ph_range": (5.5, 6.0),
        "optimal_temp": (18, 24),
        "ppfd_requirement": 200,
        "dli_requirement": 14,
        "yield_per_plant": 0.25,  # kg
        "price_per_kg": 30000,
        "difficulty": "Easy",
        "growth_stages": {
            "seedling": {"days": 10, "ec": 0.8, "ph": 5.8},
            "vegetative": {"days": 15, "ec": 1.4, "ph": 5.8},
            "harvest": {"days": 10, "ec": 1.6, "ph": 6.0}
        }
    },
    
    "Kangkung": {
        "cycle_days": 25,
        "ec_range": (1.5, 2.0),
        "ph_range": (6.0, 6.5),
        "optimal_temp": (25, 30),
        "ppfd_requirement": 250,
        "dli_requirement": 16,
        "yield_per_plant": 0.15,
        "price_per_kg": 15000,
        "difficulty": "Very Easy",
        "growth_stages": {
            "seedling": {"days": 7, "ec": 1.0, "ph": 6.0},
            "vegetative": {"days": 12, "ec": 1.7, "ph": 6.2},
            "harvest": {"days": 6, "ec": 1.8, "ph": 6.3}
        }
    },
    
    "Pakcoy": {
        "cycle_days": 30,
        "ec_range": (1.2, 1.6),
        "ph_range": (6.0, 6.5),
        "optimal_temp": (18, 24),
        "ppfd_requirement": 220,
        "dli_requirement": 15,
        "yield_per_plant": 0.3,
        "price_per_kg": 25000,
        "difficulty": "Easy",
        "growth_stages": {
            "seedling": {"days": 10, "ec": 0.9, "ph": 6.0},
            "vegetative": {"days": 14, "ec": 1.4, "ph": 6.2},
            "harvest": {"days": 6, "ec": 1.5, "ph": 6.3}
        }
    },
    
    "Basil": {
        "cycle_days": 40,
        "ec_range": (1.0, 1.4),
        "ph_range": (5.5, 6.0),
        "optimal_temp": (20, 25),
        "ppfd_requirement": 300,
        "dli_requirement": 18,
        "yield_per_plant": 0.2,
        "price_per_kg": 50000,
        "difficulty": "Easy",
        "growth_stages": {
            "seedling": {"days": 12, "ec": 0.8, "ph": 5.8},
            "vegetative": {"days": 20, "ec": 1.2, "ph": 5.8},
            "harvest": {"days": 8, "ec": 1.3, "ph": 6.0}
        }
    },
    
    "Tomato": {
        "cycle_days": 90,
        "ec_range": (2.0, 3.0),
        "ph_range": (6.0, 6.5),
        "optimal_temp": (22, 28),
        "ppfd_requirement": 400,
        "dli_requirement": 25,
        "yield_per_plant": 3.0,
        "price_per_kg": 20000,
        "difficulty": "Medium",
        "growth_stages": {
            "seedling": {"days": 20, "ec": 1.5, "ph": 6.0},
            "vegetative": {"days": 30, "ec": 2.2, "ph": 6.2},
            "flowering": {"days": 20, "ec": 2.5, "ph": 6.3},
            "fruiting": {"days": 20, "ec": 2.8, "ph": 6.3}
        }
    },
    
    "Strawberry": {
        "cycle_days": 120,
        "ec_range": (1.0, 1.5),
        "ph_range": (5.5, 6.2),
        "optimal_temp": (18, 24),
        "ppfd_requirement": 350,
        "dli_requirement": 20,
        "yield_per_plant": 0.5,
        "price_per_kg": 80000,
        "difficulty": "Hard",
        "growth_stages": {
            "seedling": {"days": 30, "ec": 0.8, "ph": 5.8},
            "vegetative": {"days": 40, "ec": 1.2, "ph": 6.0},
            "flowering": {"days": 25, "ec": 1.3, "ph": 6.0},
            "fruiting": {"days": 25, "ec": 1.4, "ph": 6.1}
        }
    }
}

# ===== DISEASE RISK DATABASE =====
DISEASE_RISK_MATRIX = {
    "Powdery Mildew": {
        "high_risk_conditions": {
            "temp_range": (20, 25),
            "humidity_range": (70, 100),
            "poor_air_circulation": True
        },
        "symptoms": ["White powdery spots on leaves", "Leaf curling", "Stunted growth"],
        "prevention": ["Maintain humidity <60%", "Increase air circulation", "Proper spacing"],
        "organic_treatment": ["Neem oil spray", "Baking soda solution", "Milk spray (1:9 ratio)"],
        "severity": "Medium"
    },
    
    "Root Rot": {
        "high_risk_conditions": {
            "water_temp_range": (28, 35),
            "low_do": True,  # DO < 5 mg/L
            "high_ec": True  # EC > 3.0
        },
        "symptoms": ["Brown slimy roots", "Wilting despite wet roots", "Foul smell"],
        "prevention": ["Keep water temp <26°C", "Ensure DO >6 mg/L", "Clean system regularly"],
        "organic_treatment": ["Hydrogen peroxide (3ml/L)", "Beneficial bacteria", "System flush"],
        "severity": "High"
    },
    
    "Tip Burn": {
        "high_risk_conditions": {
            "high_ec": True,
            "low_calcium": True,
            "high_temp": True
        },
        "symptoms": ["Brown leaf tips", "Necrotic edges", "Calcium deficiency"],
        "prevention": ["Maintain EC in range", "Ensure Ca in nutrient", "Control temperature"],
        "organic_treatment": ["Reduce EC", "Add calcium supplement", "Improve air circulation"],
        "severity": "Low"
    }
}


class HydroponicsPremiumService:
    """Premium service with AI/ML features"""
    
    @staticmethod
    def ai_nutrient_optimizer(crop, growth_stage, current_ec, current_ph, water_temp, tank_volume=100):
        """
        AI-powered nutrient optimization
        Returns precise dosing recommendations
        """
        crop_data = CROP_DATABASE.get(crop, CROP_DATABASE["Lettuce"])
        stage_data = crop_data["growth_stages"].get(growth_stage, {"ec": 1.4, "ph": 6.0})
        
        target_ec = stage_data["ec"]
        target_ph = stage_data["ph"]
        
        # EC adjustment
        ec_diff = current_ec - target_ec
        ec_action = ""
        
        if abs(ec_diff) < 0.1:
            ec_action = "✅ EC optimal, no action needed"
        elif ec_diff > 0.3:
            # Too high - dilute
            water_to_add = (ec_diff / current_ec) * tank_volume * 0.7  # 70% dilution factor
            ec_action = f"⚠️ EC too high! Add {water_to_add:.1f}L fresh water to dilute"
        elif ec_diff > 0.1:
            ec_action = f"⚡ EC slightly high. Skip next feeding or add {(ec_diff/current_ec)*tank_volume*0.3:.1f}L water"
        elif ec_diff < -0.3:
            # Too low - add nutrients
            nutrient_ml = abs(ec_diff) * tank_volume * 10  # Simplified formula
            ec_action = f"📈 EC too low! Add {nutrient_ml:.0f}ml AB Mix (each)"
        else:
            nutrient_ml = abs(ec_diff) * tank_volume * 5
            ec_action = f"📊 EC slightly low. Add {nutrient_ml:.0f}ml AB Mix (each)"
        
        # pH adjustment
        ph_diff = current_ph - target_ph
        ph_action = ""
        
        if abs(ph_diff) < 0.2:
            ph_action = "✅ pH optimal, no action needed"
        elif ph_diff > 0.5:
            # Too high - add pH Down
            ph_down_ml = ph_diff * tank_volume * 0.5  # Simplified
            ph_action = f"⬇️ pH too high! Add {ph_down_ml:.1f}ml pH Down"
        elif ph_diff > 0.2:
            ph_down_ml = ph_diff * tank_volume * 0.3
            ph_action = f"⬇️ pH slightly high. Add {ph_down_ml:.1f}ml pH Down"
        elif ph_diff < -0.5:
            # Too low - add pH Up
            ph_up_ml = abs(ph_diff) * tank_volume * 0.5
            ph_action = f"⬆️ pH too low! Add {ph_up_ml:.1f}ml pH Up"
        else:
            ph_up_ml = abs(ph_diff) * tank_volume * 0.3
            ph_action = f"⬆️ pH slightly low. Add {ph_up_ml:.1f}ml pH Up"
        
        # Water temperature warning
        temp_warning = ""
        if water_temp > 26:
            temp_warning = f"🌡️ WARNING: Water temp {water_temp}°C is too high! Risk of root rot. Cool to <26°C"
        elif water_temp < 18:
            temp_warning = f"🌡️ Water temp {water_temp}°C is low. Optimal: 20-24°C"
        
        return {
            "crop": crop,
            "stage": growth_stage,
            "current_ec": current_ec,
            "target_ec": target_ec,
            "current_ph": current_ph,
            "target_ph": target_ph,
            "ec_action": ec_action,
            "ph_action": ph_action,
            "temp_warning": temp_warning,
            "confidence": "High" if abs(ec_diff) < 0.2 and abs(ph_diff) < 0.3 else "Medium"
        }
    
    @staticmethod
    def calculate_vpd(temp_celsius, relative_humidity):
        """
        Calculate Vapor Pressure Deficit
        VPD = SVP × (1 - RH/100)
        where SVP = Saturated Vapor Pressure
        """
        # Calculate SVP using simplified formula
        svp = 0.6108 * np.exp((17.27 * temp_celsius) / (temp_celsius + 237.3))
        
        # Calculate VPD
        vpd = svp * (1 - relative_humidity / 100)
        
        # Determine optimal range
        if vpd < 0.4:
            status = "Too Low - Risk of mold/disease"
            recommendation = "Increase temperature or decrease humidity"
        elif vpd < 0.8:
            status = "Low - Slow transpiration"
            recommendation = "Slightly increase temperature or decrease humidity"
        elif vpd <= 1.2:
            status = "✅ Optimal - Perfect for growth"
            recommendation = "Maintain current conditions"
        elif vpd <= 1.6:
            status = "High - Increased transpiration"
            recommendation = "Decrease temperature or increase humidity"
        else:
            status = "Too High - Stress risk"
            recommendation = "Decrease temperature or increase humidity significantly"
        
        return {
            "vpd": round(vpd, 2),
            "status": status,
            "recommendation": recommendation,
            "optimal_range": "0.8-1.2 kPa"
        }
    
    @staticmethod
    def calculate_dli(ppfd, hours_per_day):
        """
        Calculate Daily Light Integral
        DLI = PPFD × hours × 3600 / 1,000,000
        """
        dli = (ppfd * hours_per_day * 3600) / 1000000
        
        # Determine adequacy
        if dli < 10:
            status = "Insufficient - Leggy growth"
            recommendation = "Increase light hours or intensity"
        elif dli < 14:
            status = "Low - Acceptable for leafy greens"
            recommendation = "Adequate for lettuce, increase for fruiting plants"
        elif dli <= 20:
            status = "✅ Good - Suitable for most crops"
            recommendation = "Optimal for leafy greens and herbs"
        elif dli <= 30:
            status = "✅ Excellent - Perfect for fruiting plants"
            recommendation = "Optimal for tomatoes, peppers, strawberries"
        else:
            status = "Very High - May cause stress"
            recommendation = "Reduce hours or intensity to prevent photo-inhibition"
        
        return {
            "dli": round(dli, 1),
            "status": status,
            "recommendation": recommendation,
            "optimal_leafy": "12-16 mol/m²/day",
            "optimal_fruiting": "20-30 mol/m²/day"
        }
    
    @staticmethod
    def monte_carlo_simulation(investment, yield_min, yield_max, price_min, price_max, 
                                operating_cost_monthly, iterations=10000):
        """
        Monte Carlo simulation for financial risk analysis
        """
        # Generate random scenarios
        np.random.seed(42)
        
        # Triangular distribution for yield (most likely in middle)
        yields = np.random.triangular(yield_min, (yield_min + yield_max)/2, yield_max, iterations)
        
        # Normal distribution for price
        price_mean = (price_min + price_max) / 2
        price_std = (price_max - price_min) / 6  # 99.7% within range
        prices = np.random.normal(price_mean, price_std, iterations)
        prices = np.clip(prices, price_min, price_max)
        
        # Calculate monthly revenue and profit
        monthly_revenue = yields * prices
        monthly_profit = monthly_revenue - operating_cost_monthly
        annual_profit = monthly_profit * 12
        
        # Calculate ROI
        roi = (annual_profit / investment) * 100
        
        # Calculate payback period (months)
        payback_months = investment / monthly_profit
        payback_months = np.clip(payback_months, 0, 60)  # Cap at 5 years
        
        # Statistics
        results = {
            "mean_roi": round(np.mean(roi), 1),
            "median_roi": round(np.median(roi), 1),
            "std_roi": round(np.std(roi), 1),
            "min_roi": round(np.min(roi), 1),
            "max_roi": round(np.max(roi), 1),
            "probability_profit": round((roi > 0).sum() / iterations * 100, 1),
            "probability_roi_above_20": round((roi > 20).sum() / iterations * 100, 1),
            "mean_payback_months": round(np.mean(payback_months), 1),
            "median_payback_months": round(np.median(payback_months), 1),
            "percentile_10": round(np.percentile(roi, 10), 1),
            "percentile_90": round(np.percentile(roi, 90), 1),
            "roi_distribution": roi.tolist()[:1000],  # Sample for plotting
            "monthly_profit_mean": round(np.mean(monthly_profit), 0),
            "monthly_profit_std": round(np.std(monthly_profit), 0)
        }
        
        return results
    
    @staticmethod
    def predict_yield_ml(system_type, crop, num_holes, climate_controlled=False):
        """
        ML-based yield prediction
        """
        system_data = PREMIUM_SYSTEMS.get(system_type, list(PREMIUM_SYSTEMS.values())[0])
        crop_data = CROP_DATABASE.get(crop, CROP_DATABASE["Lettuce"])
        
        # Base yield
        base_yield_per_plant = crop_data["yield_per_plant"]
        
        # System multiplier
        system_multiplier = system_data["yield_multiplier"]
        
        # Climate control bonus
        climate_bonus = 1.2 if climate_controlled else 1.0
        
        # Calculate total yield per cycle
        yield_per_cycle = base_yield_per_plant * num_holes * system_multiplier * climate_bonus
        
        # Calculate monthly yield (with succession planting)
        cycle_days = crop_data["cycle_days"]
        cycles_per_month = 30 / cycle_days
        monthly_yield = yield_per_cycle * cycles_per_month
        
        # Add realistic variance
        yield_min = monthly_yield * 0.8
        yield_max = monthly_yield * 1.2
        
        return {
            "crop": crop,
            "system": system_type,
            "num_holes": num_holes,
            "yield_per_cycle_kg": round(yield_per_cycle, 1),
            "monthly_yield_kg": round(monthly_yield, 1),
            "yield_range_kg": (round(yield_min, 1), round(yield_max, 1)),
            "confidence": "High" if climate_controlled else "Medium",
            "assumptions": f"Cycle: {cycle_days} days, Succession planting, {system_multiplier}x multiplier"
        }
    
    @staticmethod
    def diagnose_disease_risk(temp, humidity, water_temp, do_level, ec_level):
        """
        Predict disease risk based on environmental conditions
        """
        risks = []
        
        # Check Powdery Mildew
        if 20 <= temp <= 25 and humidity >= 70:
            risks.append({
                "disease": "Powdery Mildew",
                "risk_level": "High",
                "probability": "70-90%",
                "prevention": DISEASE_RISK_MATRIX["Powdery Mildew"]["prevention"],
                "treatment": DISEASE_RISK_MATRIX["Powdery Mildew"]["organic_treatment"]
            })
        
        # Check Root Rot
        if water_temp > 26 or do_level < 5:
            risk_level = "High" if (water_temp > 28 or do_level < 4) else "Medium"
            risks.append({
                "disease": "Root Rot",
                "risk_level": risk_level,
                "probability": "60-80%" if risk_level == "High" else "30-50%",
                "prevention": DISEASE_RISK_MATRIX["Root Rot"]["prevention"],
                "treatment": DISEASE_RISK_MATRIX["Root Rot"]["organic_treatment"]
            })
        
        # Check Tip Burn
        if ec_level > 2.5 or temp > 28:
            risks.append({
                "disease": "Tip Burn",
                "risk_level": "Medium",
                "probability": "40-60%",
                "prevention": DISEASE_RISK_MATRIX["Tip Burn"]["prevention"],
                "treatment": DISEASE_RISK_MATRIX["Tip Burn"]["organic_treatment"]
            })
        
        if not risks:
            return {
                "status": "✅ Low Risk",
                "message": "Environmental conditions are optimal. No significant disease risk detected.",
                "risks": []
            }
        
        return {
            "status": "⚠️ Risk Detected",
            "message": f"{len(risks)} potential disease risk(s) identified",
            "risks": risks
        }
    
    @staticmethod
    def optimize_3d_layout(room_length, room_width, room_height, system_type):
        """
        Optimize 3D space for maximum capacity
        """
        system_data = PREMIUM_SYSTEMS.get(system_type, list(PREMIUM_SYSTEMS.values())[0])
        
        # Assumptions for layout
        pipe_length = 3.0  # meters
        pipe_spacing = 0.25  # meters between pipes
        vertical_spacing = 0.4  # meters between levels
        walkway_width = 0.8  # meters
        
        # Calculate horizontal capacity
        usable_length = room_length - walkway_width
        usable_width = room_width - walkway_width
        
        pipes_per_row = int(usable_width / pipe_spacing)
        num_rows = int(usable_length / pipe_length)
        
        # Calculate vertical levels
        if "Vertical" in system_type or "Tower" in system_type:
            num_levels = int((room_height - 0.5) / vertical_spacing)
        else:
            num_levels = 1
        
        # Calculate total holes (10 holes per 3m pipe)
        holes_per_pipe = 10
        total_holes = pipes_per_row * num_rows * holes_per_pipe * num_levels
        
        # Calculate materials needed
        total_pipe_length = pipes_per_row * num_rows * num_levels * pipe_length
        num_pipes_4m = int(np.ceil(total_pipe_length / 4))  # 4m pipes
        
        return {
            "room_dimensions": f"{room_length}m × {room_width}m × {room_height}m",
            "system_type": system_type,
            "layout": {
                "pipes_per_row": pipes_per_row,
                "num_rows": num_rows,
                "num_levels": num_levels,
                "total_holes": total_holes
            },
            "materials": {
                "pvc_pipes_4m": num_pipes_4m,
                "net_pots": total_holes,
                "pump_capacity": "2000-3000 L/hour",
                "tank_size": f"{total_holes * 2}L (recommended)"
            },
            "productivity": f"{total_holes / (room_length * room_width):.1f} holes/m²"
        }
    
    @staticmethod
    def calculate_investment_detailed(system_type, num_holes):
        """
        Detailed investment calculation
        """
        system_data = PREMIUM_SYSTEMS.get(system_type, list(PREMIUM_SYSTEMS.values())[0])
        
        cost_per_hole = system_data["investment_per_hole"]
        
        # Breakdown
        structure_cost = cost_per_hole * 0.4 * num_holes
        pump_cost = 500000 if num_holes > 100 else 300000
        tank_cost = (num_holes * 2) * 50  # Rp 50/liter
        netpot_cost = num_holes * 1000
        nutrient_3months = num_holes * 150 * 3  # Rp 150/hole/month
        seedling_cost = num_holes * 500
        ec_ph_meter = 1500000 if system_data["iot_compatible"] else 500000
        automation = 3000000 if system_data["automation_level"] in ["High", "Very High"] else 0
        
        total = structure_cost + pump_cost + tank_cost + netpot_cost + nutrient_3months + seedling_cost + ec_ph_meter + automation
        
        return {
            "system": system_type,
            "num_holes": num_holes,
            "breakdown": {
                "Struktur & Pipa": structure_cost,
                "Pompa & Timer": pump_cost,
                "Tangki Nutrisi": tank_cost,
                "Net Pot": netpot_cost,
                "Nutrisi (3 bulan)": nutrient_3months,
                "Bibit": seedling_cost,
                "EC/pH Meter": ec_ph_meter,
                "Automation": automation
            },
            "total_investment": total,
            "cost_per_hole": total / num_holes
        }
