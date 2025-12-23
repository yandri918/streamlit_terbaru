"""
Feed Formulation Methods
Pearson Square, Linear Programming, and Trial & Error methods
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy.optimize import linprog

# ==========================================
# 📐 PEARSON SQUARE METHOD
# ==========================================

def pearson_square(target_nutrient: float, 
                   ingredient1_name: str, ingredient1_nutrient: float,
                   ingredient2_name: str, ingredient2_nutrient: float) -> Dict:
    """
    Pearson Square method for 2-ingredient formulation
    
    Args:
        target_nutrient: Target nutrient level (e.g., 18% CP)
        ingredient1_name: Name of first ingredient
        ingredient1_nutrient: Nutrient content of first ingredient
        ingredient2_name: Name of second ingredient
        ingredient2_nutrient: Nutrient content of second ingredient
    
    Returns:
        Dictionary with proportions and analysis
    """
    
    # Validation
    if ingredient1_nutrient == ingredient2_nutrient:
        return {"error": "Kedua bahan memiliki kandungan nutrisi yang sama. Pearson Square tidak dapat digunakan."}
    
    if not (min(ingredient1_nutrient, ingredient2_nutrient) <= target_nutrient <= max(ingredient1_nutrient, ingredient2_nutrient)):
        return {"error": f"Target nutrisi ({target_nutrient}%) harus berada di antara {min(ingredient1_nutrient, ingredient2_nutrient)}% dan {max(ingredient1_nutrient, ingredient2_nutrient)}%"}
    
    # Calculate parts
    part1 = abs(target_nutrient - ingredient2_nutrient)
    part2 = abs(target_nutrient - ingredient1_nutrient)
    total_parts = part1 + part2
    
    # Calculate percentages
    pct1 = (part1 / total_parts) * 100
    pct2 = (part2 / total_parts) * 100
    
    # Verify
    calculated_nutrient = (pct1/100 * ingredient1_nutrient) + (pct2/100 * ingredient2_nutrient)
    
    return {
        "ingredient1": ingredient1_name,
        "ingredient1_parts": part1,
        "ingredient1_percentage": round(pct1, 2),
        "ingredient2": ingredient2_name,
        "ingredient2_parts": part2,
        "ingredient2_percentage": round(pct2, 2),
        "total_parts": total_parts,
        "target_nutrient": target_nutrient,
        "calculated_nutrient": round(calculated_nutrient, 2),
        "accuracy": "Perfect" if abs(calculated_nutrient - target_nutrient) < 0.01 else "Good"
    }

# ==========================================
# 🎯 LINEAR PROGRAMMING (LEAST-COST)
# ==========================================

def least_cost_formulation(
    ingredients: Dict[str, Dict],
    requirements: Dict[str, Tuple[float, float]],
    total_weight: float = 100.0,
    animal_type: str = "cattle"
) -> Dict:
    """
    Linear Programming for least-cost feed formulation
    
    Args:
        ingredients: Dictionary of available ingredients with nutritional data and prices
        requirements: Dictionary of nutrient requirements {nutrient: (min, max)}
        total_weight: Total weight of formulation (default 100 kg)
        animal_type: Type of animal for energy calculation
    
    Returns:
        Optimal formulation with costs and nutritional analysis
    """
    
    try:
        ingredient_names = list(ingredients.keys())
        n_ingredients = len(ingredient_names)
        
        # Objective function: minimize cost
        costs = [ingredients[ing]['price_per_kg'] for ing in ingredient_names]
        
        # Inequality constraints (A_ub @ x <= b_ub)
        A_ub = []
        b_ub = []
        
        # Equality constraints (A_eq @ x == b_eq)
        A_eq = []
        b_eq = []
        
        # Total weight constraint (equality)
        A_eq.append([1.0] * n_ingredients)
        b_eq.append(total_weight)
        
        # Nutrient constraints
        for nutrient, (min_val, max_val) in requirements.items():
            # Get nutrient values for each ingredient
            nutrient_values = []
            for ing in ingredient_names:
                val = ingredients[ing].get(nutrient, 0.0)
                # Convert percentage to absolute if needed
                if nutrient in ['crude_protein', 'crude_fiber', 'ether_extract', 'ash', 'calcium', 'phosphorus']:
                    val = val / 100.0  # Convert % to decimal
                nutrient_values.append(val)
            
            # Minimum constraint: sum(nutrient_i * x_i) >= min_val
            # Rewrite as: -sum(nutrient_i * x_i) <= -min_val
            if min_val is not None and min_val > 0:
                A_ub.append([-v for v in nutrient_values])
                b_ub.append(-min_val * total_weight if nutrient in ['crude_protein', 'crude_fiber'] else -min_val)
            
            # Maximum constraint: sum(nutrient_i * x_i) <= max_val
            if max_val is not None and max_val < float('inf'):
                A_ub.append(nutrient_values)
                b_ub.append(max_val * total_weight if nutrient in ['crude_protein', 'crude_fiber'] else max_val)
        
        # Bounds for each ingredient (0 to total_weight)
        bounds = [(0, total_weight) for _ in range(n_ingredients)]
        
        # Solve
        result = linprog(
            c=costs,
            A_ub=A_ub if A_ub else None,
            b_ub=b_ub if b_ub else None,
            A_eq=A_eq,
            b_eq=b_eq,
            bounds=bounds,
            method='highs'
        )
        
        if not result.success:
            return {
                "error": "Tidak dapat menemukan solusi optimal. Coba relaksasi constraint atau tambah bahan pakan.",
                "message": result.message
            }
        
        # Parse results
        formulation = {}
        total_cost = 0
        
        for i, ing_name in enumerate(ingredient_names):
            weight = result.x[i]
            if weight > 0.01:  # Only include significant amounts
                percentage = (weight / total_weight) * 100
                cost = weight * ingredients[ing_name]['price_per_kg']
                formulation[ing_name] = {
                    "weight_kg": round(weight, 2),
                    "percentage": round(percentage, 2),
                    "cost_idr": round(cost, 0)
                }
                total_cost += cost
        
        # Calculate nutritional composition
        nutritional_analysis = calculate_formulation_nutrients(formulation, ingredients, total_weight)
        
        return {
            "success": True,
            "formulation": formulation,
            "total_cost": round(total_cost, 0),
            "cost_per_kg": round(total_cost / total_weight, 0),
            "nutritional_analysis": nutritional_analysis,
            "constraints_met": check_constraints(nutritional_analysis, requirements)
        }
        
    except Exception as e:
        return {
            "error": f"Error dalam optimasi: {str(e)}",
            "success": False
        }

def calculate_formulation_nutrients(formulation: Dict, ingredients: Dict, total_weight: float) -> Dict:
    """Calculate nutritional composition of formulation"""
    
    nutrients = {
        "crude_protein": 0,
        "crude_fiber": 0,
        "ether_extract": 0,
        "ash": 0,
        "tdn": 0,
        "de_ruminant": 0,
        "me_ruminant": 0,
        "calcium": 0,
        "phosphorus": 0,
        "lysine": 0,
        "methionine": 0
    }
    
    for ing_name, data in formulation.items():
        weight = data['weight_kg']
        proportion = weight / total_weight
        
        ing_data = ingredients[ing_name]
        for nutrient in nutrients.keys():
            nutrients[nutrient] += ing_data.get(nutrient, 0) * proportion
    
    return {k: round(v, 2) for k, v in nutrients.items()}

def check_constraints(nutritional_analysis: Dict, requirements: Dict) -> Dict:
    """Check if nutritional analysis meets requirements"""
    
    results = {}
    for nutrient, (min_val, max_val) in requirements.items():
        actual = nutritional_analysis.get(nutrient, 0)
        
        if min_val is not None and max_val is not None:
            met = min_val <= actual <= max_val
            status = "✅ Met" if met else "❌ Not Met"
        elif min_val is not None:
            met = actual >= min_val
            status = "✅ Met" if met else "❌ Too Low"
        elif max_val is not None:
            met = actual <= max_val
            status = "✅ Met" if met else "❌ Too High"
        else:
            status = "ℹ️ No constraint"
        
        results[nutrient] = {
            "actual": actual,
            "required": f"{min_val if min_val else 'N/A'} - {max_val if max_val else 'N/A'}",
            "status": status
        }
    
    return results

# ==========================================
# 🧮 DIGESTIBILITY CALCULATORS
# ==========================================

def calculate_tdn(crude_protein: float, crude_fiber: float, nfe: float, ether_extract: float,
                  cp_digestibility: float = 0.70, cf_digestibility: float = 0.50,
                  nfe_digestibility: float = 0.75, ee_digestibility: float = 0.80) -> float:
    """
    Calculate Total Digestible Nutrients (TDN)
    
    TDN = (CP_dig × CP%) + (CF_dig × CF%) + (NFE_dig × NFE%) + (EE_dig × EE% × 2.25)
    
    Args:
        crude_protein, crude_fiber, nfe, ether_extract: Nutrient percentages
        digestibility coefficients: Default values for each nutrient
    
    Returns:
        TDN percentage
    """
    
    tdn = (cp_digestibility * crude_protein) + \
          (cf_digestibility * crude_fiber) + \
          (nfe_digestibility * nfe) + \
          (ee_digestibility * ether_extract * 2.25)
    
    return round(tdn, 2)

def calculate_de(tdn: float) -> float:
    """
    Calculate Digestible Energy (DE) from TDN
    DE (Mcal/kg) = TDN (%) × 0.04409
    """
    return round(tdn * 0.04409, 2)

def calculate_me_ruminant(de: float) -> float:
    """
    Calculate Metabolizable Energy for Ruminants
    ME = DE × 0.82
    """
    return round(de * 0.82, 2)

def calculate_me_poultry(de: float) -> float:
    """
    Calculate Metabolizable Energy for Poultry
    ME = DE × 0.94 (higher efficiency than ruminants)
    """
    return round(de * 0.94, 2)

def calculate_ne_lactation(me: float) -> float:
    """
    Calculate Net Energy for Lactation
    NE_l = 0.703 × ME - 0.19
    """
    return round(0.703 * me - 0.19, 2)

def calculate_ne_maintenance(me: float) -> float:
    """
    Calculate Net Energy for Maintenance
    NE_m = 1.37 × ME - 0.138 × ME² + 0.0105 × ME³ - 1.12
    """
    ne_m = 1.37 * me - 0.138 * (me ** 2) + 0.0105 * (me ** 3) - 1.12
    return round(ne_m, 2)

def calculate_ne_gain(me: float) -> float:
    """
    Calculate Net Energy for Gain
    NE_g = 1.42 × ME - 0.174 × ME² + 0.0122 × ME³ - 1.65
    """
    ne_g = 1.42 * me - 0.174 * (me ** 2) + 0.0122 * (me ** 3) - 1.65
    return round(ne_g, 2)

def full_energy_analysis(tdn: float) -> Dict:
    """
    Complete energy analysis from TDN
    """
    de = calculate_de(tdn)
    me_ruminant = calculate_me_ruminant(de)
    me_poultry = calculate_me_poultry(de)
    ne_l = calculate_ne_lactation(me_ruminant)
    ne_m = calculate_ne_maintenance(me_ruminant)
    ne_g = calculate_ne_gain(me_ruminant)
    
    return {
        "tdn_percent": tdn,
        "de_mcal_kg": de,
        "me_ruminant_mcal_kg": me_ruminant,
        "me_poultry_mcal_kg": me_poultry,
        "ne_lactation_mcal_kg": ne_l,
        "ne_maintenance_mcal_kg": ne_m,
        "ne_gain_mcal_kg": ne_g
    }
