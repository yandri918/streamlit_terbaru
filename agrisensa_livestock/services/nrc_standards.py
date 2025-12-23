"""
NRC (National Research Council) Nutritional Standards
Requirements for cattle, poultry, goats, and sheep
"""

from typing import Dict, Tuple

# ==========================================
# 🐄 BEEF CATTLE NRC STANDARDS
# ==========================================

def get_beef_cattle_requirements(body_weight_kg: float, adg_kg: float = 0.8, 
                                 sex: str = "steer") -> Dict:
    """
    Get NRC requirements for beef cattle
    
    Args:
        body_weight_kg: Current body weight in kg
        adg_kg: Average daily gain target in kg/day
        sex: "steer", "heifer", or "bull"
    
    Returns:
        Dictionary of nutritional requirements
    """
    
    # Dry Matter Intake (DMI) estimation
    # DMI (kg/day) = BW^0.75 × (0.1493 × NEm_req / NEm_diet)
    # Simplified: DMI ≈ 2.5% of body weight for growing cattle
    dmi_kg = body_weight_kg * 0.025
    
    # Energy requirements (Mcal/day)
    # NE_m = 0.077 × BW^0.75
    ne_m_req = 0.077 * (body_weight_kg ** 0.75)
    
    # NE_g = 0.0635 × BW^0.75 × ADG^1.097
    ne_g_req = 0.0635 * (body_weight_kg ** 0.75) * (adg_kg ** 1.097)
    
    total_ne_req = ne_m_req + ne_g_req
    
    # Protein requirements (g/day)
    # CP = (BW^0.75 × 3.8) + (ADG × 200)
    cp_req_g = (body_weight_kg ** 0.75) * 3.8 + (adg_kg * 200)
    cp_req_pct = (cp_req_g / (dmi_kg * 1000)) * 100
    
    # Mineral requirements
    ca_req_g = 0.016 * body_weight_kg + (adg_kg * 7.1)  # g/day
    p_req_g = 0.016 * body_weight_kg + (adg_kg * 3.9)   # g/day
    
    ca_req_pct = (ca_req_g / (dmi_kg * 1000)) * 100
    p_req_pct = (p_req_g / (dmi_kg * 1000)) * 100
    
    return {
        "animal_type": "Beef Cattle",
        "body_weight_kg": body_weight_kg,
        "adg_target_kg": adg_kg,
        "sex": sex,
        "dmi_kg_day": round(dmi_kg, 2),
        "ne_maintenance_mcal": round(ne_m_req, 2),
        "ne_gain_mcal": round(ne_g_req, 2),
        "total_ne_mcal": round(total_ne_req, 2),
        "crude_protein_percent": round(cp_req_pct, 2),
        "crude_protein_g_day": round(cp_req_g, 0),
        "calcium_percent": round(ca_req_pct, 2),
        "calcium_g_day": round(ca_req_g, 1),
        "phosphorus_percent": round(p_req_pct, 2),
        "phosphorus_g_day": round(p_req_g, 1),
        "crude_fiber_min_percent": 15.0,  # Minimum for rumen health
        "crude_fiber_max_percent": 30.0
    }

# ==========================================
# 🥛 DAIRY CATTLE NRC STANDARDS
# ==========================================

def get_dairy_cattle_requirements(body_weight_kg: float, milk_production_kg: float = 20.0,
                                  milk_fat_pct: float = 3.5, days_in_milk: int = 100) -> Dict:
    """
    Get NRC requirements for dairy cattle
    
    Args:
        body_weight_kg: Current body weight in kg
        milk_production_kg: Daily milk production in kg
        milk_fat_pct: Milk fat percentage
        days_in_milk: Days since calving
    
    Returns:
        Dictionary of nutritional requirements
    """
    
    # DMI estimation for lactating cows
    # DMI (kg) = (0.372 × FCM + 0.0968 × BW^0.75) × (1 - e^(-0.192 × (DIM + 3.67)))
    # Simplified: DMI ≈ 3-4% of BW for high producers
    fcm = milk_production_kg * (0.4 + 0.15 * milk_fat_pct)  # Fat-corrected milk
    dmi_kg = (0.372 * fcm + 0.0968 * (body_weight_kg ** 0.75))
    
    # Energy requirements
    # NE_m = 0.080 × BW^0.75
    ne_m_req = 0.080 * (body_weight_kg ** 0.75)
    
    # NE_l = Milk_kg × (0.0929 × Fat% + 0.0563 × Protein% + 0.0395 × Lactose%)
    # Simplified using fat only: NE_l ≈ Milk_kg × (0.36 + 0.0969 × Fat%)
    ne_l_req = milk_production_kg * (0.36 + 0.0969 * milk_fat_pct)
    
    total_ne_req = ne_m_req + ne_l_req
    
    # Protein requirements
    # MP (Metabolizable Protein) = (BW^0.75 × 4.0) + (Milk_kg × 64.8)
    mp_req_g = (body_weight_kg ** 0.75) * 4.0 + (milk_production_kg * 64.8)
    
    # Convert MP to CP (assuming 64% efficiency)
    cp_req_g = mp_req_g / 0.64
    cp_req_pct = (cp_req_g / (dmi_kg * 1000)) * 100
    
    # Mineral requirements
    ca_req_g = 0.031 * body_weight_kg + (milk_production_kg * 1.22)
    p_req_g = 0.016 * body_weight_kg + (milk_production_kg * 0.90)
    
    ca_req_pct = (ca_req_g / (dmi_kg * 1000)) * 100
    p_req_pct = (p_req_g / (dmi_kg * 1000)) * 100
    
    return {
        "animal_type": "Dairy Cattle",
        "body_weight_kg": body_weight_kg,
        "milk_production_kg": milk_production_kg,
        "milk_fat_percent": milk_fat_pct,
        "days_in_milk": days_in_milk,
        "dmi_kg_day": round(dmi_kg, 2),
        "ne_maintenance_mcal": round(ne_m_req, 2),
        "ne_lactation_mcal": round(ne_l_req, 2),
        "total_ne_mcal": round(total_ne_req, 2),
        "crude_protein_percent": round(cp_req_pct, 2),
        "crude_protein_g_day": round(cp_req_g, 0),
        "calcium_percent": round(ca_req_pct, 2),
        "calcium_g_day": round(ca_req_g, 1),
        "phosphorus_percent": round(p_req_pct, 2),
        "phosphorus_g_day": round(p_req_g, 1),
        "crude_fiber_min_percent": 17.0,
        "crude_fiber_max_percent": 25.0,
        "ndf_min_percent": 28.0,  # Neutral Detergent Fiber
        "adf_max_percent": 21.0   # Acid Detergent Fiber
    }

# ==========================================
# 🐓 BROILER NRC STANDARDS
# ==========================================

def get_broiler_requirements(age_days: int, target_weight_g: int = 2000) -> Dict:
    """
    Get NRC requirements for broiler chickens
    
    Args:
        age_days: Age in days
        target_weight_g: Target market weight in grams
    
    Returns:
        Dictionary of nutritional requirements
    """
    
    # Determine phase
    if age_days <= 10:
        phase = "Pre-Starter"
        me_kcal = 3000
        cp_pct = 23.0
        lysine_pct = 1.44
        meth_cys_pct = 1.05
        ca_pct = 1.00
        p_avail_pct = 0.50
    elif age_days <= 21:
        phase = "Starter"
        me_kcal = 3000
        cp_pct = 21.5
        lysine_pct = 1.26
        meth_cys_pct = 0.94
        ca_pct = 0.90
        p_avail_pct = 0.45
    elif age_days <= 35:
        phase = "Grower"
        me_kcal = 3100
        cp_pct = 19.5
        lysine_pct = 1.13
        meth_cys_pct = 0.84
        ca_pct = 0.80
        p_avail_pct = 0.40
    else:
        phase = "Finisher"
        me_kcal = 3150
        cp_pct = 18.0
        lysine_pct = 1.01
        meth_cys_pct = 0.75
        ca_pct = 0.75
        p_avail_pct = 0.35
    
    # Other amino acids (as % of lysine - ideal protein concept)
    threonine_pct = lysine_pct * 0.65
    tryptophan_pct = lysine_pct * 0.16
    arginine_pct = lysine_pct * 1.05
    
    return {
        "animal_type": "Broiler",
        "age_days": age_days,
        "phase": phase,
        "me_kcal_kg": me_kcal,
        "crude_protein_percent": cp_pct,
        "lysine_percent": lysine_pct,
        "methionine_cystine_percent": meth_cys_pct,
        "threonine_percent": round(threonine_pct, 2),
        "tryptophan_percent": round(tryptophan_pct, 2),
        "arginine_percent": round(arginine_pct, 2),
        "calcium_percent": ca_pct,
        "phosphorus_available_percent": p_avail_pct,
        "sodium_percent": 0.16,
        "chloride_percent": 0.16,
        "crude_fiber_max_percent": 5.0
    }

# ==========================================
# 🥚 LAYER NRC STANDARDS
# ==========================================

def get_layer_requirements(age_weeks: int, production_rate_pct: float = 85.0) -> Dict:
    """
    Get NRC requirements for layer chickens
    
    Args:
        age_weeks: Age in weeks
        production_rate_pct: Egg production rate (%)
    
    Returns:
        Dictionary of nutritional requirements
    """
    
    if age_weeks < 18:
        phase = "Grower"
        me_kcal = 2850
        cp_pct = 16.0
        lysine_pct = 0.70
        meth_cys_pct = 0.60
        ca_pct = 0.90
        p_avail_pct = 0.35
    elif age_weeks < 45:
        phase = "Layer Phase 1"
        me_kcal = 2750
        cp_pct = 17.0
        lysine_pct = 0.80
        meth_cys_pct = 0.70
        ca_pct = 3.80
        p_avail_pct = 0.32
    else:
        phase = "Layer Phase 2"
        me_kcal = 2750
        cp_pct = 16.5
        lysine_pct = 0.75
        meth_cys_pct = 0.68
        ca_pct = 4.00
        p_avail_pct = 0.32
    
    # Adjust for production rate
    if production_rate_pct > 90:
        cp_pct += 0.5
        lysine_pct += 0.05
    
    return {
        "animal_type": "Layer",
        "age_weeks": age_weeks,
        "phase": phase,
        "production_rate_percent": production_rate_pct,
        "me_kcal_kg": me_kcal,
        "crude_protein_percent": cp_pct,
        "lysine_percent": lysine_pct,
        "methionine_cystine_percent": meth_cys_pct,
        "calcium_percent": ca_pct,
        "phosphorus_available_percent": p_avail_pct,
        "sodium_percent": 0.15,
        "linoleic_acid_percent": 1.0,
        "crude_fiber_max_percent": 7.0
    }

# ==========================================
# 🐐 GOAT NRC STANDARDS
# ==========================================

def get_goat_requirements(body_weight_kg: float, adg_kg: float = 0.15,
                          production_type: str = "meat") -> Dict:
    """
    Get NRC requirements for goats
    
    Args:
        body_weight_kg: Current body weight in kg
        adg_kg: Average daily gain in kg/day
        production_type: "meat", "dairy", or "maintenance"
    
    Returns:
        Dictionary of nutritional requirements
    """
    
    # DMI estimation: 3-5% of body weight
    dmi_kg = body_weight_kg * 0.04
    
    # Energy requirements (Mcal/day)
    # ME_m = 0.106 × BW^0.75
    me_m_req = 0.106 * (body_weight_kg ** 0.75)
    
    # ME_g = 0.0112 × BW^0.75 × ADG
    me_g_req = 0.0112 * (body_weight_kg ** 0.75) * adg_kg * 1000  # ADG in grams
    
    total_me_req = me_m_req + me_g_req
    
    # Protein requirements
    if production_type == "meat":
        cp_pct = 14.0 + (adg_kg * 20)
    elif production_type == "dairy":
        cp_pct = 16.0
    else:
        cp_pct = 10.0
    
    # Mineral requirements
    ca_pct = 0.60 if production_type == "dairy" else 0.40
    p_pct = 0.40 if production_type == "dairy" else 0.28
    
    return {
        "animal_type": "Goat",
        "body_weight_kg": body_weight_kg,
        "adg_target_kg": adg_kg,
        "production_type": production_type,
        "dmi_kg_day": round(dmi_kg, 2),
        "me_maintenance_mcal": round(me_m_req, 2),
        "me_gain_mcal": round(me_g_req, 2),
        "total_me_mcal": round(total_me_req, 2),
        "crude_protein_percent": round(cp_pct, 2),
        "calcium_percent": ca_pct,
        "phosphorus_percent": p_pct,
        "crude_fiber_min_percent": 12.0,
        "crude_fiber_max_percent": 25.0
    }

# ==========================================
# 🐑 SHEEP NRC STANDARDS
# ==========================================

def get_sheep_requirements(body_weight_kg: float, adg_kg: float = 0.20,
                           production_type: str = "meat") -> Dict:
    """
    Get NRC requirements for sheep
    
    Args:
        body_weight_kg: Current body weight in kg
        adg_kg: Average daily gain in kg/day
        production_type: "meat", "wool", or "maintenance"
    
    Returns:
        Dictionary of nutritional requirements
    """
    
    # DMI estimation: 3-4% of body weight
    dmi_kg = body_weight_kg * 0.035
    
    # Energy requirements (Mcal/day)
    # ME_m = 0.106 × BW^0.75
    me_m_req = 0.106 * (body_weight_kg ** 0.75)
    
    # ME_g = 0.0112 × BW^0.75 × ADG
    me_g_req = 0.0112 * (body_weight_kg ** 0.75) * adg_kg * 1000
    
    total_me_req = me_m_req + me_g_req
    
    # Protein requirements
    if production_type == "meat":
        cp_pct = 13.0 + (adg_kg * 15)
    elif production_type == "wool":
        cp_pct = 15.0
    else:
        cp_pct = 9.0
    
    # Mineral requirements
    ca_pct = 0.40
    p_pct = 0.28
    
    return {
        "animal_type": "Sheep",
        "body_weight_kg": body_weight_kg,
        "adg_target_kg": adg_kg,
        "production_type": production_type,
        "dmi_kg_day": round(dmi_kg, 2),
        "me_maintenance_mcal": round(me_m_req, 2),
        "me_gain_mcal": round(me_g_req, 2),
        "total_me_mcal": round(total_me_req, 2),
        "crude_protein_percent": round(cp_pct, 2),
        "calcium_percent": ca_pct,
        "phosphorus_percent": p_pct,
        "crude_fiber_min_percent": 12.0,
        "crude_fiber_max_percent": 25.0
    }

# ==========================================
# 🧬 AMINO ACID BALANCING (POULTRY)
# ==========================================

IDEAL_PROTEIN_RATIOS = {
    "Broiler Starter": {
        "lysine": 100,
        "methionine_cystine": 74,
        "threonine": 65,
        "tryptophan": 16,
        "arginine": 105,
        "valine": 77,
        "isoleucine": 67,
        "leucine": 109
    },
    "Broiler Grower": {
        "lysine": 100,
        "methionine_cystine": 74,
        "threonine": 65,
        "tryptophan": 16,
        "arginine": 105,
        "valine": 77,
        "isoleucine": 67,
        "leucine": 109
    },
    "Broiler Finisher": {
        "lysine": 100,
        "methionine_cystine": 74,
        "threonine": 67,
        "tryptophan": 17,
        "arginine": 108,
        "valine": 79,
        "isoleucine": 69,
        "leucine": 112
    },
    "Layer": {
        "lysine": 100,
        "methionine_cystine": 88,
        "threonine": 67,
        "tryptophan": 20,
        "arginine": 105,
        "valine": 82,
        "isoleucine": 75,
        "leucine": 115
    }
}

def check_amino_acid_balance(formulation_aa: Dict, phase: str = "Broiler Starter") -> Dict:
    """
    Check if amino acid profile meets ideal protein ratios
    
    Args:
        formulation_aa: Dictionary of amino acid levels in formulation
        phase: Production phase
    
    Returns:
        Analysis of amino acid balance
    """
    
    if phase not in IDEAL_PROTEIN_RATIOS:
        return {"error": f"Phase '{phase}' not found in ideal protein database"}
    
    ideal_ratios = IDEAL_PROTEIN_RATIOS[phase]
    lysine_level = formulation_aa.get("lysine", 0)
    
    if lysine_level == 0:
        return {"error": "Lysine level must be > 0"}
    
    analysis = {}
    for aa, ideal_ratio in ideal_ratios.items():
        if aa == "lysine":
            analysis[aa] = {
                "actual_percent": lysine_level,
                "ideal_ratio": 100,
                "actual_ratio": 100,
                "status": "✅ Reference AA"
            }
        else:
            actual_level = formulation_aa.get(aa, 0)
            actual_ratio = (actual_level / lysine_level) * 100
            ideal = ideal_ratio
            
            if actual_ratio >= ideal * 0.95:  # Within 5% is acceptable
                status = "✅ Balanced"
            elif actual_ratio >= ideal * 0.85:
                status = "⚠️ Slightly Low"
            else:
                status = "❌ Deficient"
            
            analysis[aa] = {
                "actual_percent": actual_level,
                "ideal_ratio": ideal,
                "actual_ratio": round(actual_ratio, 1),
                "status": status,
                "deficiency": round(max(0, (ideal/100 * lysine_level) - actual_level), 3)
            }
    
    return analysis
