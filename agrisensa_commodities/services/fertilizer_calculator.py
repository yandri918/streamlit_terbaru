# -*- coding: utf-8 -*-
"""
Fertilizer Calculator Engine
Calculation functions for phase-based fertilizer requirements
and application methods (Tugal, Kocor, Semprot)
"""

import sys
import os

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.fertilizer_database import (
    get_crop_data, 
    FERTILIZER_CONTENT,
    HARD_CROPS,
    FRUIT_TREES
)

# ========== PHASE-BASED NPK CALCULATIONS ==========

def get_current_phase(crop_name, tree_age_years):
    """
    Determine current growth phase based on tree age
    
    Args:
        crop_name: Name of the crop
        tree_age_years: Age of tree in years
    
    Returns:
        dict: Phase data including NPK requirements
    """
    crop_data = get_crop_data(crop_name)
    if not crop_data:
        return None
    
    # Convert age to months for comparison
    tree_age_months = tree_age_years * 12
    
    # Find matching phase
    for phase in crop_data['phases']:
        age_range = phase['age_range']
        
        # Parse age range
        if '-' in age_range:
            if age_range.startswith('>'):
                # e.g., ">3 tahun"
                min_age = float(age_range.replace('>', '').split()[0]) * 12
                if tree_age_months >= min_age:
                    return phase
            else:
                # e.g., "0-1 tahun" or "1-2 tahun"
                parts = age_range.split('-')
                min_age = float(parts[0]) * 12
                max_age = float(parts[1].split()[0]) * 12
                if min_age <= tree_age_months < max_age:
                    return phase
        else:
            # Single age like "0-1 tahun"
            continue
    
    # If no match, return last phase (mature)
    return crop_data['phases'][-1] if crop_data['phases'] else None


def calculate_phase_requirements(crop_name, tree_age_years, num_trees):
    """
    Calculate total NPK requirements based on tree age and phase
    
    Args:
        crop_name: Name of the crop
        tree_age_years: Age of trees in years
        num_trees: Number of trees
    
    Returns:
        dict: {
            "phase_name": str,
            "npk_per_tree": {"N": g, "P": g, "K": g},
            "npk_total": {"N": kg, "P": kg, "K": kg},
            "application_frequency": int,
            "application_methods": list,
            "notes": str
        }
    """
    phase = get_current_phase(crop_name, tree_age_years)
    if not phase:
        return None
    
    # Get NPK per tree per year (in grams)
    npk_per_tree = phase['npk_per_tree_per_year']
    
    # Calculate total (convert to kg)
    npk_total = {
        "N": (npk_per_tree.get("N", 0) * num_trees) / 1000,
        "P": (npk_per_tree.get("P", 0) * num_trees) / 1000,
        "K": (npk_per_tree.get("K", 0) * num_trees) / 1000
    }
    
    # Add Mg if present
    if "Mg" in npk_per_tree:
        npk_total["Mg"] = (npk_per_tree.get("Mg", 0) * num_trees) / 1000
    
    return {
        "phase_name": phase['phase_name'],
        "age_range": phase['age_range'],
        "npk_per_tree": npk_per_tree,
        "npk_total": npk_total,
        "application_frequency": phase['application_frequency'],
        "application_methods": phase['application_methods'],
        "notes": phase['notes'],
        "source": phase.get('source', 'Scientific Research')
    }


# ========== FERTILIZER PRODUCT CALCULATIONS ==========

def calculate_fertilizer_amounts(npk_needed, fertilizer_type):
    """
    Calculate amount of specific fertilizer needed to meet NPK requirements
    
    Args:
        npk_needed: dict with N, P, K in kg
        fertilizer_type: Name of fertilizer product
    
    Returns:
        dict: Amount needed in kg for each nutrient
    """
    if fertilizer_type not in FERTILIZER_CONTENT:
        return None
    
    fertilizer = FERTILIZER_CONTENT[fertilizer_type]
    
    results = {}
    
    # Calculate for N
    if fertilizer['N'] > 0 and npk_needed.get('N', 0) > 0:
        results['N'] = npk_needed['N'] / (fertilizer['N'] / 100)
    else:
        results['N'] = 0
    
    # Calculate for P
    if fertilizer['P'] > 0 and npk_needed.get('P', 0) > 0:
        results['P'] = npk_needed['P'] / (fertilizer['P'] / 100)
    else:
        results['P'] = 0
    
    # Calculate for K
    if fertilizer['K'] > 0 and npk_needed.get('K', 0) > 0:
        results['K'] = npk_needed['K'] / (fertilizer['K'] / 100)
    else:
        results['K'] = 0
    
    return results


def calculate_single_fertilizer_mix(npk_needed):
    """
    Calculate combination of Urea, SP-36, and KCl to meet NPK needs
    
    Args:
        npk_needed: dict with N, P, K in kg
    
    Returns:
        dict: {
            "urea_kg": float,
            "sp36_kg": float,
            "kcl_kg": float,
            "total_cost": float
        }
    """
    # Urea for N (46% N)
    urea_kg = npk_needed.get('N', 0) / 0.46
    
    # SP-36 for P (36% P2O5)
    sp36_kg = npk_needed.get('P', 0) / 0.36
    
    # KCl for K (60% K2O)
    kcl_kg = npk_needed.get('K', 0) / 0.60
    
    # Calculate costs
    urea_cost = urea_kg * FERTILIZER_CONTENT['Urea']['price_per_kg']
    sp36_cost = sp36_kg * FERTILIZER_CONTENT['SP-36']['price_per_kg']
    kcl_cost = kcl_kg * FERTILIZER_CONTENT['KCl']['price_per_kg']
    
    return {
        "urea_kg": urea_kg,
        "sp36_kg": sp36_kg,
        "kcl_kg": kcl_kg,
        "urea_cost": urea_cost,
        "sp36_cost": sp36_cost,
        "kcl_cost": kcl_cost,
        "total_cost": urea_cost + sp36_cost + kcl_cost,
        "total_kg": urea_kg + sp36_kg + kcl_kg
    }


def calculate_compound_fertilizer(npk_needed, fertilizer_type="NPK 15-15-15"):
    """
    Calculate amount of compound NPK fertilizer needed
    
    Args:
        npk_needed: dict with N, P, K in kg
        fertilizer_type: Type of NPK compound
    
    Returns:
        dict: Amount and cost
    """
    if fertilizer_type not in FERTILIZER_CONTENT:
        return None
    
    fertilizer = FERTILIZER_CONTENT[fertilizer_type]
    
    # Calculate based on each nutrient, take the maximum
    n_based = npk_needed.get('N', 0) / (fertilizer['N'] / 100) if fertilizer['N'] > 0 else 0
    p_based = npk_needed.get('P', 0) / (fertilizer['P'] / 100) if fertilizer['P'] > 0 else 0
    k_based = npk_needed.get('K', 0) / (fertilizer['K'] / 100) if fertilizer['K'] > 0 else 0
    
    # Take maximum to ensure all nutrients are met
    total_kg = max(n_based, p_based, k_based)
    total_cost = total_kg * fertilizer['price_per_kg']
    
    return {
        "fertilizer_type": fertilizer_type,
        "total_kg": total_kg,
        "total_cost": total_cost,
        "price_per_kg": fertilizer['price_per_kg']
    }


# ========== APPLICATION METHOD CALCULATIONS ==========

def calculate_tugal_application(total_kg, num_trees, applications_per_year):
    """
    Calculate solid fertilizer application (Tugal/Placement method)
    
    Args:
        total_kg: Total fertilizer needed per year (kg)
        num_trees: Number of trees
        applications_per_year: Frequency of application
    
    Returns:
        dict: Application details
    """
    # Per tree per year
    per_tree_per_year_kg = total_kg / num_trees
    per_tree_per_year_g = per_tree_per_year_kg * 1000
    
    # Per tree per application
    per_tree_per_app_g = per_tree_per_year_g / applications_per_year
    
    # Total per application
    total_per_app_kg = total_kg / applications_per_year
    
    return {
        "method": "Tugal (Padat)",
        "per_tree_per_year_g": per_tree_per_year_g,
        "per_tree_per_app_g": per_tree_per_app_g,
        "total_per_year_kg": total_kg,
        "total_per_app_kg": total_per_app_kg,
        "applications_per_year": applications_per_year,
        "instructions": f"Taburkan {per_tree_per_app_g:.0f} gram pupuk melingkar di bawah tajuk pohon (radius 1-2 meter dari batang). Aplikasi {applications_per_year}x per tahun."
    }


def calculate_kocor_solution(fertilizer_kg, num_trees, applications_per_year, 
                             liters_per_tree=2, fertilizer_type="NPK 15-15-15"):
    """
    Calculate drench solution (Kocor method)
    
    Args:
        fertilizer_kg: Total fertilizer needed per year (kg)
        num_trees: Number of trees
        applications_per_year: Frequency
        liters_per_tree: Solution volume per tree (default 2L)
        fertilizer_type: Type of fertilizer for safety check
    
    Returns:
        dict: Solution preparation details
    """
    # Get safe concentration limit
    safe_conc = FERTILIZER_CONTENT.get(fertilizer_type, {}).get('safe_drench_conc', 1.0)
    
    # Per application
    fertilizer_per_app_kg = fertilizer_kg / applications_per_year
    fertilizer_per_app_g = fertilizer_per_app_kg * 1000
    
    # Total solution volume per application
    total_solution_liters = num_trees * liters_per_tree
    
    # Concentration (%)
    concentration_percent = (fertilizer_per_app_g / total_solution_liters) / 10
    
    # Check if safe
    is_safe = concentration_percent <= safe_conc
    
    # For 16L tank
    tanks_needed = total_solution_liters / 16
    fertilizer_per_tank_g = fertilizer_per_app_g / tanks_needed if tanks_needed > 0 else 0
    water_per_tank_L = 16
    
    return {
        "method": "Kocor (Larutan Siram)",
        "concentration_percent": concentration_percent,
        "safe_concentration": safe_conc,
        "is_safe": is_safe,
        "solution_per_tree_L": liters_per_tree,
        "total_solution_per_app_L": total_solution_liters,
        "fertilizer_per_app_g": fertilizer_per_app_g,
        "applications_per_year": applications_per_year,
        "tanks_16L_needed": tanks_needed,
        "fertilizer_per_tank_g": fertilizer_per_tank_g,
        "water_per_tank_L": water_per_tank_L,
        "instructions": f"Larutkan {fertilizer_per_tank_g:.0f} gram pupuk dalam {water_per_tank_L}L air (konsentrasi {concentration_percent:.2f}%). Siram {liters_per_tree}L per pohon. Aplikasi {applications_per_year}x per tahun."
    }


def calculate_semprot_solution(fertilizer_kg, area_ha, applications_per_year,
                               spray_volume_per_ha=400, fertilizer_type="NPK 15-15-15"):
    """
    Calculate foliar spray solution (Semprot method)
    IMPORTANT: Concentrations are LOWER than drench to prevent leaf burn
    
    Args:
        fertilizer_kg: Total fertilizer needed per year (kg)
        area_ha: Area in hectares
        applications_per_year: Frequency
        spray_volume_per_ha: Spray volume (L/ha), default 400L
        fertilizer_type: Type of fertilizer for safety check
    
    Returns:
        dict: Spray solution details
    """
    # Get safe concentration limit (foliar is lower than drench!)
    safe_conc = FERTILIZER_CONTENT.get(fertilizer_type, {}).get('safe_foliar_conc', 0.5)
    
    # Per application
    fertilizer_per_app_kg = fertilizer_kg / applications_per_year
    fertilizer_per_app_g = fertilizer_per_app_kg * 1000
    
    # Total spray volume per application
    total_spray_volume_L = area_ha * spray_volume_per_ha
    
    # Concentration (%)
    concentration_percent = (fertilizer_per_app_g / total_spray_volume_L) / 10
    
    # Check if safe
    is_safe = concentration_percent <= safe_conc
    
    # Recommended concentration (use safe limit)
    recommended_conc = min(concentration_percent, safe_conc)
    recommended_fertilizer_g = (recommended_conc * total_spray_volume_L * 10)
    
    # For 16L tank
    tanks_needed = total_spray_volume_L / 16
    fertilizer_per_tank_g = recommended_fertilizer_g / tanks_needed if tanks_needed > 0 else 0
    
    return {
        "method": "Semprot (Foliar Spray)",
        "concentration_percent": concentration_percent,
        "recommended_concentration": recommended_conc,
        "safe_concentration": safe_conc,
        "is_safe": is_safe,
        "spray_volume_per_ha_L": spray_volume_per_ha,
        "total_spray_volume_L": total_spray_volume_L,
        "fertilizer_needed_g": recommended_fertilizer_g,
        "applications_per_year": applications_per_year,
        "tanks_16L_needed": tanks_needed,
        "fertilizer_per_tank_g": fertilizer_per_tank_g,
        "water_per_tank_L": 16,
        "warning": "⚠️ PENTING: Konsentrasi semprot HARUS lebih rendah dari kocor untuk mencegah leaf burn!" if not is_safe else "",
        "instructions": f"Larutkan {fertilizer_per_tank_g:.0f} gram pupuk dalam 16L air (konsentrasi {recommended_conc:.2f}%). Semprot merata pada daun. Aplikasi {applications_per_year}x per tahun. JANGAN semprot saat terik matahari!"
    }


# ========== ORGANIC + CHEMICAL COMBINATION ==========

def calculate_organic_chemical_mix(npk_needed, organic_ratio=0.3):
    """
    Calculate 30% organic + 70% chemical fertilizer combination
    
    Args:
        npk_needed: dict with N, P, K in kg
        organic_ratio: Ratio of organic (default 0.3 = 30%)
    
    Returns:
        dict: Organic and chemical amounts
    """
    chemical_ratio = 1 - organic_ratio
    
    # Split NPK needs
    npk_organic = {
        "N": npk_needed.get('N', 0) * organic_ratio,
        "P": npk_needed.get('P', 0) * organic_ratio,
        "K": npk_needed.get('K', 0) * organic_ratio
    }
    
    npk_chemical = {
        "N": npk_needed.get('N', 0) * chemical_ratio,
        "P": npk_needed.get('P', 0) * chemical_ratio,
        "K": npk_needed.get('K', 0) * chemical_ratio
    }
    
    # Calculate organic fertilizer (using Pupuk Kandang Sapi)
    # Pupuk Kandang: N=1.5%, P=1%, K=1.5%
    organic_n = npk_organic['N'] / 0.015
    organic_p = npk_organic['P'] / 0.010
    organic_k = npk_organic['K'] / 0.015
    organic_kg = max(organic_n, organic_p, organic_k)
    organic_cost = organic_kg * FERTILIZER_CONTENT['Pupuk Kandang Sapi']['price_per_kg']
    
    # Calculate chemical fertilizer (using single mix)
    chemical_mix = calculate_single_fertilizer_mix(npk_chemical)
    
    total_cost = organic_cost + chemical_mix['total_cost']
    
    return {
        "organic_ratio": organic_ratio * 100,
        "chemical_ratio": chemical_ratio * 100,
        "organic_kg": organic_kg,
        "organic_cost": organic_cost,
        "chemical_urea_kg": chemical_mix['urea_kg'],
        "chemical_sp36_kg": chemical_mix['sp36_kg'],
        "chemical_kcl_kg": chemical_mix['kcl_kg'],
        "chemical_cost": chemical_mix['total_cost'],
        "total_cost": total_cost,
        "benefits": "Kombinasi organik + kimia meningkatkan kesehatan tanah jangka panjang, struktur tanah lebih baik, dan aktivitas mikroba meningkat."
    }


# ========== COST ANALYSIS ==========

def calculate_fertilizer_costs(fertilizer_amounts, fertilizer_types):
    """
    Calculate total costs for different fertilizer strategies
    
    Args:
        fertilizer_amounts: dict of fertilizer amounts
        fertilizer_types: list of fertilizer types used
    
    Returns:
        dict: Cost breakdown
    """
    total_cost = 0
    breakdown = {}
    
    for fert_type in fertilizer_types:
        if fert_type in fertilizer_amounts and fert_type in FERTILIZER_CONTENT:
            amount = fertilizer_amounts[fert_type]
            price = FERTILIZER_CONTENT[fert_type]['price_per_kg']
            cost = amount * price
            breakdown[fert_type] = {
                "amount_kg": amount,
                "price_per_kg": price,
                "total_cost": cost
            }
            total_cost += cost
    
    return {
        "breakdown": breakdown,
        "total_cost": total_cost
    }


# ========== CONVERSION UTILITIES ==========

def ppm_to_percent(ppm):
    """Convert ppm to percentage"""
    return ppm / 10000


def percent_to_ppm(percent):
    """Convert percentage to ppm"""
    return percent * 10000


def grams_per_liter_to_percent(g_per_L):
    """Convert g/L to percentage"""
    return g_per_L / 10
