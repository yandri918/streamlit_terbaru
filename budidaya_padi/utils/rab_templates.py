"""
Template Management for RAB Calculator
Pre-defined and custom budget templates
"""

import json
from pathlib import Path

# Pre-defined templates
TEMPLATES = {
    "Konvensional Standar": {
        "description": "Budidaya padi konvensional dengan input standar",
        "costs_per_ha": {
            "persiapan_lahan": 2000000,
            "bibit": 1500000,
            "pupuk_urea": 1200000,
            "pupuk_npk": 1500000,
            "pupuk_organik": 800000,
            "pestisida": 1000000,
            "herbisida": 500000,
            "tenaga_kerja_tanam": 2000000,
            "tenaga_kerja_rawat": 1500000,
            "tenaga_kerja_panen": 3000000,
            "lainnya": 500000
        },
        "target_produksi": 6.0,
        "metode_tanam": "Transplanting (Pindah Tanam)"
    },
    
    "Organik": {
        "description": "Budidaya padi organik tanpa pestisida kimia",
        "costs_per_ha": {
            "persiapan_lahan": 2200000,
            "bibit": 1800000,
            "pupuk_urea": 0,
            "pupuk_npk": 0,
            "pupuk_organik": 3000000,
            "pestisida": 0,
            "herbisida": 0,
            "tenaga_kerja_tanam": 2500000,
            "tenaga_kerja_rawat": 2000000,
            "tenaga_kerja_panen": 3500000,
            "lainnya": 800000
        },
        "target_produksi": 4.5,
        "metode_tanam": "SRI (System of Rice Intensification)"
    },
    
    "SRI Intensif": {
        "description": "System of Rice Intensification dengan manajemen intensif",
        "costs_per_ha": {
            "persiapan_lahan": 2500000,
            "bibit": 1000000,
            "pupuk_urea": 1000000,
            "pupuk_npk": 1800000,
            "pupuk_organik": 1500000,
            "pestisida": 1200000,
            "herbisida": 600000,
            "tenaga_kerja_tanam": 2800000,
            "tenaga_kerja_rawat": 2200000,
            "tenaga_kerja_panen": 3500000,
            "lainnya": 700000
        },
        "target_produksi": 8.0,
        "metode_tanam": "SRI (System of Rice Intensification)"
    },
    
    "Jajar Legowo Intensif": {
        "description": "Jajar Legowo 4:1 dengan input tinggi",
        "costs_per_ha": {
            "persiapan_lahan": 2300000,
            "bibit": 1700000,
            "pupuk_urea": 1400000,
            "pupuk_npk": 1800000,
            "pupuk_organik": 1000000,
            "pestisida": 1300000,
            "herbisida": 700000,
            "tenaga_kerja_tanam": 2500000,
            "tenaga_kerja_rawat": 1800000,
            "tenaga_kerja_panen": 3200000,
            "lainnya": 600000
        },
        "target_produksi": 7.5,
        "metode_tanam": "Jajar Legowo 4:1"
    },
    
    "Low Input": {
        "description": "Budidaya dengan input minimal untuk efisiensi biaya",
        "costs_per_ha": {
            "persiapan_lahan": 1500000,
            "bibit": 1200000,
            "pupuk_urea": 800000,
            "pupuk_npk": 1000000,
            "pupuk_organik": 500000,
            "pestisida": 600000,
            "herbisida": 300000,
            "tenaga_kerja_tanam": 1500000,
            "tenaga_kerja_rawat": 1000000,
            "tenaga_kerja_panen": 2500000,
            "lainnya": 300000
        },
        "target_produksi": 4.0,
        "metode_tanam": "Direct Seeding (Tabela)"
    }
}

def get_template_names():
    """Get list of available template names"""
    return list(TEMPLATES.keys())

def get_template(name):
    """Get template data by name"""
    return TEMPLATES.get(name)

def save_custom_template(name, data, filepath="custom_templates.json"):
    """Save a custom template to JSON file"""
    try:
        # Load existing custom templates
        custom_templates = {}
        if Path(filepath).exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                custom_templates = json.load(f)
        
        # Add new template
        custom_templates[name] = data
        
        # Save back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(custom_templates, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving template: {e}")
        return False

def load_custom_templates(filepath="custom_templates.json"):
    """Load custom templates from JSON file"""
    try:
        if Path(filepath).exists():
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        print(f"Error loading templates: {e}")
        return {}

def get_all_templates():
    """Get all templates (pre-defined + custom)"""
    all_templates = TEMPLATES.copy()
    custom = load_custom_templates()
    all_templates.update(custom)
    return all_templates

# Benchmark data for comparison
REGIONAL_BENCHMARKS = {
    "Jawa Barat": {
        "avg_cost_per_ha": 15000000,
        "avg_productivity": 6.2,
        "avg_cost_per_kg": 2420,
        "avg_roi": 45
    },
    "Jawa Tengah": {
        "avg_cost_per_ha": 14500000,
        "avg_productivity": 6.5,
        "avg_cost_per_kg": 2230,
        "avg_roi": 48
    },
    "Jawa Timur": {
        "avg_cost_per_ha": 14800000,
        "avg_productivity": 6.3,
        "avg_cost_per_kg": 2350,
        "avg_roi": 46
    },
    "Sulawesi Selatan": {
        "avg_cost_per_ha": 13500000,
        "avg_productivity": 5.8,
        "avg_cost_per_kg": 2330,
        "avg_roi": 42
    },
    "Sumatera Utara": {
        "avg_cost_per_ha": 14000000,
        "avg_productivity": 5.5,
        "avg_cost_per_kg": 2545,
        "avg_roi": 40
    }
}

def get_regional_benchmark(region):
    """Get benchmark data for a region"""
    return REGIONAL_BENCHMARKS.get(region, REGIONAL_BENCHMARKS["Jawa Barat"])

def calculate_efficiency_score(actual_data, benchmark_data):
    """Calculate efficiency score compared to benchmark"""
    scores = {}
    
    # Cost efficiency (lower is better)
    cost_ratio = actual_data['biaya_per_kg'] / benchmark_data['avg_cost_per_kg']
    scores['cost_efficiency'] = max(0, min(100, (2 - cost_ratio) * 50))
    
    # Productivity efficiency (higher is better)
    prod_ratio = actual_data['target_produksi'] / benchmark_data['avg_productivity']
    scores['productivity_efficiency'] = min(100, prod_ratio * 50)
    
    # ROI efficiency (higher is better)
    roi_ratio = actual_data['roi'] / benchmark_data['avg_roi']
    scores['roi_efficiency'] = min(100, roi_ratio * 50)
    
    # Overall score
    scores['overall'] = (scores['cost_efficiency'] + scores['productivity_efficiency'] + scores['roi_efficiency']) / 3
    
    return scores
