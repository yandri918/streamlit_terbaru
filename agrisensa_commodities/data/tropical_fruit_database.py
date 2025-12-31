"""
Tropical Fruit Database for Off-Season Cultivation
Comprehensive data for premium tropical fruits with scientific references
"""

TROPICAL_FRUITS_DB = {
    "durian": {
        "name_id": "Durian",
        "name_en": "Durian",
        "scientific": "Durio zibethinus",
        "nickname": "Si Raja Buah",
        "icon": "🧀",
        
        "market_info": {
            "normal_season": "Desember - Februari",
            "off_season_target": "Juni - Agustus",
            "price_normal": 30000,  # Rp/kg
            "price_offseason": 100000,  # Rp/kg
            "price_multiplier": 3.3,
            "export_potential": "Sangat Tinggi (China, Singapura)",
        },
        
        "cultivation_params": {
            "flowering_trigger": "Stres air + PBZ",
            "water_stress_duration": "8-12 minggu",
            "pbz_dosage": "2-5 gram/pohon",
            "pbz_timing": "3-4 bulan sebelum target pembungaan",
            "success_rate": "70-85%",
        },
        
        "water_stress_protocol": {
            "phase_1": {
                "name": "Pengeringan Total",
                "duration": "4-6 minggu",
                "action": "Hentikan irigasi total",
                "indicator": "Kelembaban tanah < 30% kapasitas lapang",
            },
            "phase_2": {
                "name": "Stres Ekstrem",
                "duration": "2-4 minggu",
                "action": "Biarkan daun layu siang hari",
                "indicator": "Leaf water potential: -1.5 to -2.0 MPa",
            },
            "phase_3": {
                "name": "Pemulihan Mendadak",
                "duration": "2-4 minggu",
                "action": "Siram intensif + pupuk P-K tinggi",
                "indicator": "Shock fisiologis memicu pembungaan",
            },
        },
        
        "fertilization_program": {
            "pre_stress": {
                "npk_ratio": "15-5-15",
                "dosage": "2-3 kg/pohon",
                "frequency": "Setiap 2 minggu (2 bulan)",
                "organic": "20-30 kg/pohon",
            },
            "pre_flowering": {
                "npk_ratio": "10-20-20",
                "dosage": "2 kg/pohon",
                "timing": "1 bulan sebelum stres air",
                "micronutrients": "Zn, B, Mg",
            },
            "flowering_fruiting": {
                "npk_ratio": "12-12-17",
                "dosage": "1.5 kg/pohon/bulan",
                "boron": "50-100 ppm (foliar)",
                "calcium": "200-300 ppm",
                "magnesium": "100-150 ppm",
            },
        },
        
        "economic_analysis": {
            "normal_production": "80-100 kg/pohon",
            "offseason_production": "60-80 kg/pohon",
            "normal_revenue": 2700000,  # Rp
            "offseason_revenue": 7000000,  # Rp
            "extra_cost": 750000,  # Rp
            "net_profit_increase": 3550000,  # Rp
            "roi_percentage": 473,
        },
        
        "references": [
            {
                "title": "Effect of water stress on flowering in durian",
                "authors": "Wanitchakorn, R., et al.",
                "journal": "Scientia Horticulturae",
                "year": 2000,
                "doi": "10.1016/S0304-4238(99)00143-8",
            },
            {
                "title": "Paclobutrazol induces flowering in durian",
                "authors": "Aron, Y., et al.",
                "journal": "HortScience",
                "year": 2007,
            },
            {
                "title": "Durian: King of Tropical Fruit",
                "authors": "Subhadrabandhu, S. & Yapwattanaphun, C.",
                "journal": "Horticultural Reviews",
                "year": 2001,
            },
        ],
    },
    
    "mangosteen": {
        "name_id": "Manggis",
        "name_en": "Mangosteen",
        "scientific": "Garcinia mangostana",
        "nickname": "Ratu Buah",
        "icon": "🟣",
        
        "market_info": {
            "normal_season": "November - Januari",
            "off_season_target": "Mei - Juli",
            "price_normal": 40000,
            "price_offseason": 120000,
            "price_multiplier": 3.0,
            "export_potential": "Sangat Tinggi (China, Jepang, Eropa)",
        },
        
        "cultivation_params": {
            "flowering_trigger": "Stres air + Pruning",
            "water_stress_duration": "6-10 minggu",
            "pbz_dosage": "1-3 gram/pohon",
            "pbz_timing": "4-5 bulan sebelum target",
            "success_rate": "60-75%",
        },
        
        "water_stress_protocol": {
            "phase_1": {
                "name": "Pengeringan Bertahap",
                "duration": "3-4 minggu",
                "action": "Kurangi irigasi 50%",
                "indicator": "Kelembaban tanah 40-50%",
            },
            "phase_2": {
                "name": "Stres Moderat",
                "duration": "3-4 minggu",
                "action": "Hentikan irigasi",
                "indicator": "Daun mulai kusam, sedikit layu",
            },
            "phase_3": {
                "name": "Pemulihan",
                "duration": "2-3 minggu",
                "action": "Siram normal + pupuk",
                "indicator": "Tunas bunga muncul",
            },
        },
        
        "fertilization_program": {
            "pre_stress": {
                "npk_ratio": "12-6-12",
                "dosage": "1.5-2 kg/pohon",
                "frequency": "Bulanan",
                "organic": "15-20 kg/pohon",
            },
            "pre_flowering": {
                "npk_ratio": "8-20-20",
                "dosage": "1.5 kg/pohon",
                "timing": "2 minggu sebelum stres",
                "micronutrients": "B, Mn, Zn",
            },
            "flowering_fruiting": {
                "npk_ratio": "10-10-15",
                "dosage": "1 kg/pohon/bulan",
                "boron": "30-50 ppm",
                "calcium": "150-200 ppm",
                "magnesium": "80-100 ppm",
            },
        },
        
        "economic_analysis": {
            "normal_production": "40-60 kg/pohon",
            "offseason_production": "30-45 kg/pohon",
            "normal_revenue": 2200000,
            "offseason_revenue": 4800000,
            "extra_cost": 500000,
            "net_profit_increase": 2100000,
            "roi_percentage": 420,
        },
        
        "references": [
            {
                "title": "Flowering and fruiting manipulation in mangosteen",
                "authors": "Yaacob, O. & Tindall, H.D.",
                "journal": "Tropical Fruits",
                "year": 1995,
            },
            {
                "title": "Mangosteen cultivation in Southeast Asia",
                "authors": "Osman, M.B. & Milan, A.R.",
                "journal": "Fruits",
                "year": 2006,
            },
        ],
    },
    
    "rambutan": {
        "name_id": "Rambutan",
        "name_en": "Rambutan",
        "scientific": "Nephelium lappaceum",
        "nickname": "Buah Berbulu",
        "icon": "🔴",
        
        "market_info": {
            "normal_season": "November - Februari",
            "off_season_target": "Mei - Agustus",
            "price_normal": 15000,
            "price_offseason": 40000,
            "price_multiplier": 2.7,
            "export_potential": "Tinggi (Thailand, Malaysia)",
        },
        
        "cultivation_params": {
            "flowering_trigger": "Stres air + PBZ",
            "water_stress_duration": "6-8 minggu",
            "pbz_dosage": "2-4 gram/pohon",
            "pbz_timing": "3 bulan sebelum target",
            "success_rate": "75-85%",
        },
        
        "water_stress_protocol": {
            "phase_1": {
                "name": "Pengeringan",
                "duration": "3-4 minggu",
                "action": "Hentikan irigasi",
                "indicator": "Tanah kering, daun mulai layu siang",
            },
            "phase_2": {
                "name": "Stres Lanjutan",
                "duration": "2-3 minggu",
                "action": "Pertahankan kondisi kering",
                "indicator": "Daun layu siang, pulih malam",
            },
            "phase_3": {
                "name": "Pemulihan",
                "duration": "1-2 minggu",
                "action": "Siram intensif + pupuk P-K",
                "indicator": "Tunas bunga dalam 2-3 minggu",
            },
        },
        
        "fertilization_program": {
            "pre_stress": {
                "npk_ratio": "15-5-15",
                "dosage": "1.5-2 kg/pohon",
                "frequency": "Setiap 3 minggu",
                "organic": "15-20 kg/pohon",
            },
            "pre_flowering": {
                "npk_ratio": "10-20-15",
                "dosage": "1.5 kg/pohon",
                "timing": "2 minggu sebelum stres",
                "micronutrients": "B, Zn",
            },
            "flowering_fruiting": {
                "npk_ratio": "12-10-15",
                "dosage": "1 kg/pohon/bulan",
                "boron": "40-60 ppm",
                "calcium": "150-200 ppm",
            },
        },
        
        "economic_analysis": {
            "normal_production": "60-80 kg/pohon",
            "offseason_production": "45-60 kg/pohon",
            "normal_revenue": 1050000,
            "offseason_revenue": 2200000,
            "extra_cost": 400000,
            "net_profit_increase": 750000,
            "roi_percentage": 188,
        },
        
        "references": [
            {
                "title": "Rambutan cultivation and off-season production",
                "authors": "Tindall, H.D.",
                "journal": "Tropical Fruit Production",
                "year": 1994,
            },
            {
                "title": "Effect of paclobutrazol on rambutan flowering",
                "authors": "Menzel, C.M. & Simpson, D.R.",
                "journal": "Scientia Horticulturae",
                "year": 1994,
            },
        ],
    },
    
    "longan": {
        "name_id": "Kelengkeng",
        "name_en": "Longan",
        "scientific": "Dimocarpus longan",
        "nickname": "Mata Naga",
        "icon": "🟤",
        
        "market_info": {
            "normal_season": "Januari - Maret",
            "off_season_target": "Juli - September",
            "price_normal": 25000,
            "price_offseason": 70000,
            "price_multiplier": 2.8,
            "export_potential": "Sangat Tinggi (China, Taiwan, Singapura)",
        },
        
        "cultivation_params": {
            "flowering_trigger": "Stres air + Suhu rendah + PBZ",
            "water_stress_duration": "6-10 minggu",
            "pbz_dosage": "3-6 gram/pohon",
            "pbz_timing": "4 bulan sebelum target",
            "success_rate": "80-90%",
            "special_note": "Kelengkeng paling responsif terhadap PBZ",
        },
        
        "water_stress_protocol": {
            "phase_1": {
                "name": "Pengeringan Awal",
                "duration": "3-4 minggu",
                "action": "Kurangi irigasi 70%",
                "indicator": "Kelembaban tanah 30-40%",
            },
            "phase_2": {
                "name": "Stres Penuh",
                "duration": "3-4 minggu",
                "action": "Hentikan irigasi total",
                "indicator": "Daun layu siang, daun tua rontok",
            },
            "phase_3": {
                "name": "Pemulihan + Cold Shock",
                "duration": "2-3 minggu",
                "action": "Siram intensif + pupuk + KClO3 (optional)",
                "indicator": "Tunas bunga muncul 10-14 hari",
            },
        },
        
        "fertilization_program": {
            "pre_stress": {
                "npk_ratio": "15-5-10",
                "dosage": "2 kg/pohon",
                "frequency": "Setiap 3 minggu",
                "organic": "20 kg/pohon",
            },
            "pre_flowering": {
                "npk_ratio": "8-24-16",
                "dosage": "2 kg/pohon",
                "timing": "1 bulan sebelum stres",
                "micronutrients": "B, Zn, Mn",
                "special": "High P untuk inisiasi bunga",
            },
            "flowering_fruiting": {
                "npk_ratio": "10-12-18",
                "dosage": "1.5 kg/pohon/bulan",
                "boron": "50-80 ppm (critical!)",
                "calcium": "200-250 ppm",
                "magnesium": "100-120 ppm",
            },
        },
        
        "special_techniques": {
            "kclo3_application": {
                "name": "Potassium Chlorate (KClO3)",
                "dosage": "3-5 gram/liter air",
                "volume": "5-10 liter/pohon",
                "timing": "Saat pemulihan dari stres air",
                "effect": "Meningkatkan pembungaan 20-30%",
                "caution": "Hati-hati, bisa toxic jika overdosis",
            },
            "girdling": {
                "name": "Pelukaan Kulit Batang",
                "method": "Sayat melingkar 1/3 keliling batang",
                "depth": "Hingga kambium",
                "timing": "2 minggu sebelum stres air",
                "effect": "Akumulasi karbohidrat untuk bunga",
            },
        },
        
        "economic_analysis": {
            "normal_production": "50-70 kg/pohon",
            "offseason_production": "40-55 kg/pohon",
            "normal_revenue": 1500000,
            "offseason_revenue": 3500000,
            "extra_cost": 600000,
            "net_profit_increase": 1400000,
            "roi_percentage": 233,
        },
        
        "references": [
            {
                "title": "Longan production in Thailand",
                "authors": "Subhadrabandhu, S. & Yapwattanaphun, C.",
                "journal": "Acta Horticulturae",
                "year": 2003,
            },
            {
                "title": "Effect of paclobutrazol and potassium chlorate on longan",
                "authors": "Menzel, C.M.",
                "journal": "Scientia Horticulturae",
                "year": 2002,
            },
            {
                "title": "Off-season production of longan",
                "authors": "Tongumpai, P., et al.",
                "journal": "Acta Horticulturae",
                "year": 2001,
            },
        ],
    },
    
    "mango": {
        "name_id": "Mangga",
        "name_en": "Mango",
        "scientific": "Mangifera indica",
        "nickname": "Buah Tropis Favorit",
        "icon": "🥭",
        
        "market_info": {
            "normal_season": "September - November",
            "off_season_target": "Maret - Mei",
            "price_normal": 20000,
            "price_offseason": 50000,
            "price_multiplier": 2.5,
            "export_potential": "Sangat Tinggi (Global market)",
        },
        
        "cultivation_params": {
            "flowering_trigger": "Stres air + PBZ + Pruning",
            "water_stress_duration": "8-12 minggu",
            "pbz_dosage": "2-5 gram/pohon",
            "pbz_timing": "3-4 bulan sebelum target",
            "success_rate": "70-80%",
        },
        
        "water_stress_protocol": {
            "phase_1": {
                "name": "Pengeringan Bertahap",
                "duration": "4-5 minggu",
                "action": "Kurangi irigasi bertahap",
                "indicator": "Kelembaban tanah turun ke 30%",
            },
            "phase_2": {
                "name": "Stres Penuh",
                "duration": "3-5 minggu",
                "action": "Hentikan irigasi total",
                "indicator": "Daun layu, pertumbuhan vegetatif stop",
            },
            "phase_3": {
                "name": "Pemulihan",
                "duration": "2-3 minggu",
                "action": "Siram + pupuk P-K tinggi",
                "indicator": "Tunas bunga dalam 3-4 minggu",
            },
        },
        
        "fertilization_program": {
            "pre_stress": {
                "npk_ratio": "15-5-15",
                "dosage": "2-3 kg/pohon",
                "frequency": "Bulanan",
                "organic": "20-25 kg/pohon",
            },
            "pre_flowering": {
                "npk_ratio": "10-20-20",
                "dosage": "2 kg/pohon",
                "timing": "2 minggu sebelum stres",
                "micronutrients": "B, Zn, Cu",
            },
            "flowering_fruiting": {
                "npk_ratio": "12-10-15",
                "dosage": "1.5 kg/pohon/bulan",
                "boron": "40-60 ppm",
                "calcium": "150-200 ppm",
                "zinc": "50-80 ppm",
            },
        },
        
        "economic_analysis": {
            "normal_production": "80-120 kg/pohon",
            "offseason_production": "60-90 kg/pohon",
            "normal_revenue": 2000000,
            "offseason_revenue": 4000000,
            "extra_cost": 500000,
            "net_profit_increase": 1500000,
            "roi_percentage": 300,
        },
        
        "references": [
            {
                "title": "Mango production and off-season flowering",
                "authors": "Davenport, T.L.",
                "journal": "HortScience",
                "year": 2007,
            },
            {
                "title": "Effect of paclobutrazol on mango flowering",
                "authors": "Kulkarni, V.J.",
                "journal": "Acta Horticulturae",
                "year": 1988,
            },
        ],
    },
}

# Get list of available fruits
def get_fruit_list():
    """Return list of available fruits"""
    return list(TROPICAL_FRUITS_DB.keys())

# Get fruit data
def get_fruit_data(fruit_key):
    """Get complete data for a specific fruit"""
    return TROPICAL_FRUITS_DB.get(fruit_key, None)
