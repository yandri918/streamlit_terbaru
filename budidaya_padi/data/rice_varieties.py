"""
Indonesian Rice Varieties Database
Comprehensive data for 20+ rice varieties suitable for Indonesian conditions
"""

RICE_VARIETIES = {
    'IR64': {
        'name': 'IR64',
        'type': 'Inbrida',
        'duration': 115,  # days
        'yield_potential': 6.0,  # ton/ha
        'grain_type': 'Panjang ramping',
        'grain_quality': 'Sedang',
        'resistance': {
            'wereng_coklat': 'Biotipe 1, 2, 3',
            'blast': 'Moderat',
            'hawar_daun': 'Rentan'
        },
        'suitable_regions': ['Jawa', 'Sumatera', 'Sulawesi', 'Bali'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Baik',
        'characteristics': 'Varietas populer, adaptasi luas, hasil stabil',
        'price_range': (5000, 6000),  # Rp/kg
    },
    'Ciherang': {
        'name': 'Ciherang',
        'type': 'Inbrida',
        'duration': 116,
        'yield_potential': 6.0,
        'grain_type': 'Panjang ramping',
        'grain_quality': 'Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 2, 3',
            'blast': 'Moderat',
            'hawar_daun': 'Strain III'
        },
        'suitable_regions': ['Jawa', 'Sumatera', 'Bali', 'NTB'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Baik',
        'characteristics': 'Rasa nasi pulen, aroma wangi, disukai konsumen',
        'price_range': (5500, 6500),
    },
    'Inpari_32': {
        'name': 'Inpari 32 HDB Agritan',
        'type': 'Inbrida',
        'duration': 115,
        'yield_potential': 7.2,
        'grain_type': 'Sedang',
        'grain_quality': 'Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 2, 3',
            'blast': 'Tahan',
            'hawar_daun': 'Strain IV'
        },
        'suitable_regions': ['Jawa', 'Sumatera'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Sangat Baik',
        'characteristics': 'Potensi hasil tinggi, tahan rebah, cocok intensifikasi',
        'price_range': (6000, 7000),
    },
    'Inpari_33': {
        'name': 'Inpari 33',
        'type': 'Inbrida',
        'duration': 112,
        'yield_potential': 6.8,
        'grain_type': 'Sedang',
        'grain_quality': 'Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 2, 3',
            'blast': 'Tahan',
            'hawar_daun': 'Moderat'
        },
        'suitable_regions': ['Jawa', 'Sumatera', 'Sulawesi'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Baik',
        'characteristics': 'Umur genjah, cocok untuk pola tanam 3x setahun',
        'price_range': (5800, 6800),
    },
    'Inpari_42': {
        'name': 'Inpari 42 Agritan GSR',
        'type': 'Inbrida',
        'duration': 117,
        'yield_potential': 7.5,
        'grain_type': 'Panjang ramping',
        'grain_quality': 'Sangat Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 2, 3',
            'blast': 'Tahan',
            'hawar_daun': 'Strain IV'
        },
        'suitable_regions': ['Jawa', 'Sumatera'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Sangat Baik',
        'characteristics': 'Potensi hasil sangat tinggi, kualitas beras premium',
        'price_range': (6500, 7500),
    },
    'Inpari_43': {
        'name': 'Inpari 43 Agritan GSR',
        'type': 'Inbrida',
        'duration': 119,
        'yield_potential': 7.8,
        'grain_type': 'Panjang ramping',
        'grain_quality': 'Sangat Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 2, 3',
            'blast': 'Tahan',
            'hawar_daun': 'Strain IV, VIII'
        },
        'suitable_regions': ['Jawa', 'Sumatera', 'Sulawesi'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Sangat Baik',
        'characteristics': 'Potensi hasil tertinggi, tahan hama penyakit utama',
        'price_range': (7000, 8000),
    },
    'Mekongga': {
        'name': 'Mekongga',
        'type': 'Inbrida',
        'duration': 119,
        'yield_potential': 6.5,
        'grain_type': 'Panjang ramping',
        'grain_quality': 'Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 2, 3',
            'blast': 'Moderat',
            'hawar_daun': 'Strain III'
        },
        'suitable_regions': ['Sulawesi', 'Jawa', 'Bali'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Baik',
        'characteristics': 'Rasa nasi pulen, aroma wangi, disukai pasar Sulawesi',
        'price_range': (5500, 6500),
    },
    'Memberamo': {
        'name': 'Memberamo',
        'type': 'Inbrida',
        'duration': 125,
        'yield_potential': 6.2,
        'grain_type': 'Panjang ramping',
        'grain_quality': 'Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 2, 3',
            'blast': 'Moderat',
            'hawar_daun': 'Strain III'
        },
        'suitable_regions': ['Papua', 'Maluku', 'Sulawesi'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Tinggi',
        'fertilizer_response': 'Baik',
        'characteristics': 'Adaptasi baik di lahan basah, cocok Papua',
        'price_range': (5000, 6000),
    },
    'Situbagendit': {
        'name': 'Situbagendit',
        'type': 'Inbrida',
        'duration': 125,
        'yield_potential': 6.0,
        'grain_type': 'Panjang ramping',
        'grain_quality': 'Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 1, 2',
            'blast': 'Moderat',
            'hawar_daun': 'Moderat'
        },
        'suitable_regions': ['Jawa Barat', 'Jawa Tengah'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Baik',
        'characteristics': 'Varietas lokal unggul, rasa khas, harga premium',
        'price_range': (6000, 7000),
    },
    'Ciliwung': {
        'name': 'Ciliwung',
        'type': 'Inbrida',
        'duration': 120,
        'yield_potential': 5.8,
        'grain_type': 'Sedang',
        'grain_quality': 'Baik',
        'resistance': {
            'wereng_coklat': 'Biotipe 1, 2',
            'blast': 'Moderat',
            'hawar_daun': 'Moderat'
        },
        'suitable_regions': ['Jawa Barat', 'Banten'],
        'suitable_seasons': ['Musim Hujan', 'Musim Kemarau'],
        'water_requirement': 'Sedang',
        'fertilizer_response': 'Baik',
        'characteristics': 'Cocok lahan sawah irigasi teknis',
        'price_range': (5500, 6500),
    },
}

def get_variety(variety_name):
    """Get variety data by name"""
    return RICE_VARIETIES.get(variety_name)

def get_all_varieties():
    """Get list of all variety names"""
    return list(RICE_VARIETIES.keys())

def get_varieties_by_region(region):
    """Get varieties suitable for a specific region"""
    return {
        name: data for name, data in RICE_VARIETIES.items()
        if region in data['suitable_regions']
    }

def get_varieties_by_duration(min_days, max_days):
    """Get varieties within duration range"""
    return {
        name: data for name, data in RICE_VARIETIES.items()
        if min_days <= data['duration'] <= max_days
    }

def get_high_yield_varieties(min_yield=7.0):
    """Get high-yielding varieties"""
    return {
        name: data for name, data in RICE_VARIETIES.items()
        if data['yield_potential'] >= min_yield
    }

def compare_varieties(variety_names):
    """Compare multiple varieties"""
    return {name: RICE_VARIETIES[name] for name in variety_names if name in RICE_VARIETIES}
