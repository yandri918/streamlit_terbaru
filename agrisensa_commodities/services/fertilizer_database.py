# -*- coding: utf-8 -*-
"""
Fertilizer Database for Hard Crops & Fruit Trees
Scientific data based on research from:
- Indonesian Oil Palm Research Institute (IOPRI)
- TNAU, IPB, UGM Agricultural Universities
- Haifa, Yara Fertilizer Research
- Peer-reviewed journals on tropical fruit cultivation
"""

# ========== FERTILIZER PRODUCT DATABASE ==========

FERTILIZER_CONTENT = {
    # Chemical Fertilizers - Single Nutrient
    "Urea": {
        "N": 46, "P": 0, "K": 0,
        "price_per_kg": 2500,
        "type": "kimia",
        "form": "granular",
        "safe_foliar_conc": 0.5,  # % for foliar spray
        "safe_drench_conc": 1.0   # % for drench
    },
    "SP-36": {
        "N": 0, "P": 36, "K": 0,
        "price_per_kg": 3000,
        "type": "kimia",
        "form": "granular",
        "safe_foliar_conc": 0.5,
        "safe_drench_conc": 1.0
    },
    "KCl": {
        "N": 0, "P": 0, "K": 60,
        "price_per_kg": 2800,
        "type": "kimia",
        "form": "granular",
        "safe_foliar_conc": 0.5,
        "safe_drench_conc": 1.0
    },
    "ZA (Amonium Sulfat)": {
        "N": 21, "P": 0, "K": 0, "S": 24,
        "price_per_kg": 2200,
        "type": "kimia",
        "form": "granular",
        "safe_foliar_conc": 0.5,
        "safe_drench_conc": 1.0
    },
    
    # Chemical Fertilizers - Compound NPK
    "NPK 15-15-15": {
        "N": 15, "P": 15, "K": 15,
        "price_per_kg": 3500,
        "type": "kimia",
        "form": "granular",
        "safe_foliar_conc": 1.0,
        "safe_drench_conc": 1.5
    },
    "NPK 16-16-16": {
        "N": 16, "P": 16, "K": 16,
        "price_per_kg": 3600,
        "type": "kimia",
        "form": "granular",
        "safe_foliar_conc": 1.0,
        "safe_drench_conc": 1.5
    },
    "NPK 12-12-17+2MgO": {
        "N": 12, "P": 12, "K": 17, "Mg": 2,
        "price_per_kg": 3800,
        "type": "kimia",
        "form": "granular",
        "safe_foliar_conc": 1.0,
        "safe_drench_conc": 1.5,
        "notes": "Ideal untuk kakao (butuh Mg tinggi)"
    },
    
    # Premium Water-Soluble Fertilizers
    "KNO3 (Kalium Nitrat)": {
        "N": 13, "P": 0, "K": 46,
        "price_per_kg": 15000,
        "type": "kimia",
        "form": "water_soluble",
        "safe_foliar_conc": 0.5,
        "safe_drench_conc": 1.0,
        "notes": "Untuk induksi bunga dan pembesaran buah"
    },
    "MKP (Mono Kalium Fosfat)": {
        "N": 0, "P": 52, "K": 34,
        "price_per_kg": 25000,
        "type": "kimia",
        "form": "water_soluble",
        "safe_foliar_conc": 0.5,
        "safe_drench_conc": 1.0,
        "notes": "Premium - P+K tinggi untuk pembungaan"
    },
    "Ca(NO3)2 (Kalsium Nitrat)": {
        "N": 15.5, "P": 0, "K": 0, "Ca": 19,
        "price_per_kg": 12000,
        "type": "kimia",
        "form": "water_soluble",
        "safe_foliar_conc": 0.5,
        "safe_drench_conc": 1.0,
        "notes": "Untuk cegah blossom end rot pada tomat/buah"
    },
    
    # Organic Fertilizers
    "Pupuk Kandang Sapi": {
        "N": 1.5, "P": 1.0, "K": 1.5,
        "price_per_kg": 500,
        "type": "organik",
        "form": "solid",
        "safe_foliar_conc": 0,  # Not for foliar
        "safe_drench_conc": 0,  # Not for drench (use solid only)
        "notes": "Aplikasi padat saja, 20-30 kg/pohon/tahun"
    },
    "Kompos": {
        "N": 2.0, "P": 1.5, "K": 2.0,
        "price_per_kg": 800,
        "type": "organik",
        "form": "solid",
        "safe_foliar_conc": 0,
        "safe_drench_conc": 0,
        "notes": "Aplikasi padat, perbaikan struktur tanah"
    },
    "Kascing (Vermicompost)": {
        "N": 2.5, "P": 2.0, "K": 1.5,
        "price_per_kg": 2000,
        "type": "organik",
        "form": "solid",
        "safe_foliar_conc": 0,
        "safe_drench_conc": 0,
        "notes": "Premium organik, kaya mikroba"
    },
    "Guano": {
        "N": 10, "P": 12, "K": 2,
        "price_per_kg": 5000,
        "type": "organik",
        "form": "solid",
        "safe_foliar_conc": 0,
        "safe_drench_conc": 0,
        "notes": "Organik tinggi P, dari kotoran kelelawar"
    }
}

# ========== HARD CROPS DATABASE ==========

HARD_CROPS = {
    "Kelapa Sawit": {
        "latin_name": "Elaeis guineensis",
        "category": "Tanaman Keras",
        "phases": [
            {
                "phase_name": "Nursery (Pembibitan)",
                "age_range": "0-1 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 31.35, "P": 31.35, "K": 40.60, "Mg": 19.90},  # grams
                "application_frequency": 12,  # monthly
                "application_methods": ["kocor"],
                "notes": "Fase pembibitan, pupuk NPK 50% dosis standar sangat efisien",
                "source": "Indonesian Oil Palm Research Institute (IOPRI)"
            },
            {
                "phase_name": "TBM Tahun 1",
                "age_range": "1-2 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 500, "P": 250, "K": 500},  # grams
                "application_frequency": 4,  # quarterly
                "application_methods": ["tugal", "kocor"],
                "notes": "Fokus pertumbuhan vegetatif, N tinggi",
                "source": "IOPRI, Malaysian Palm Oil Board"
            },
            {
                "phase_name": "TBM Tahun 2",
                "age_range": "2-3 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 750, "P": 375, "K": 750},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pertumbuhan pesat, tingkatkan dosis bertahap",
                "source": "IOPRI"
            },
            {
                "phase_name": "TBM Tahun 3",
                "age_range": "3-4 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 1000, "P": 500, "K": 1000},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Persiapan memasuki fase produktif",
                "source": "IOPRI"
            },
            {
                "phase_name": "TM Tahun 4-10",
                "age_range": "4-10 tahun",
                "duration_months": 84,
                "npk_per_tree_per_year": {"N": 1500, "P": 750, "K": 2000},
                "application_frequency": 2,  # semi-annual
                "application_methods": ["tugal", "kocor", "semprot"],
                "notes": "Produktif optimal, K tinggi untuk kualitas TBS (Tandan Buah Segar)",
                "source": "IOPRI, Haifa Group"
            },
            {
                "phase_name": "TM Tahun >10",
                "age_range": ">10 tahun",
                "duration_months": 240,  # 20 years
                "npk_per_tree_per_year": {"N": 1200, "P": 600, "K": 1800},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor", "semprot"],
                "notes": "Maintenance, dosis sedikit turun",
                "source": "IOPRI"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": ["KNO3 (Kalium Nitrat)"]
        },
        "spacing": "9x9 m (Populasi 143 pohon/ha)",
        "first_harvest": "30-36 bulan setelah tanam"
    },
    
    "Kakao": {
        "latin_name": "Theobroma cacao",
        "category": "Tanaman Keras",
        "phases": [
            {
                "phase_name": "TBM Tahun 1",
                "age_range": "0-1 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 100, "P": 50, "K": 100, "Mg": 20},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Fase pembentukan tajuk, butuh naungan",
                "source": "ICCRI (Indonesian Coffee and Cocoa Research Institute)"
            },
            {
                "phase_name": "TBM Tahun 2",
                "age_range": "1-2 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 200, "P": 100, "K": 200, "Mg": 40},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pertumbuhan vegetatif aktif",
                "source": "ICCRI"
            },
            {
                "phase_name": "TBM Tahun 3",
                "age_range": "2-3 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 300, "P": 150, "K": 300, "Mg": 60},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Mulai berbunga, persiapan produktif",
                "source": "ICCRI"
            },
            {
                "phase_name": "TM Produktif",
                "age_range": ">3 tahun",
                "duration_months": 300,  # 25 years
                "npk_per_tree_per_year": {"N": 400, "P": 200, "K": 500, "Mg": 80},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor", "semprot"],
                "notes": "Kakao butuh Mg tinggi! Gunakan NPK 12-12-17+2MgO",
                "source": "ICCRI, Yara Fertilizer"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 12-12-17+2MgO"],
            "organic": ["Pupuk Kandang Sapi", "Kompos", "Kulit Kakao Terkompos"],
            "premium": ["KNO3 (Kalium Nitrat)", "MKP (Mono Kalium Fosfat)"]
        },
        "spacing": "3x3 m (Populasi 1,111 pohon/ha)",
        "first_harvest": "30-36 bulan setelah tanam"
    },
    
    "Kopi Robusta": {
        "latin_name": "Coffea canephora",
        "category": "Tanaman Keras",
        "phases": [
            {
                "phase_name": "TBM Tahun 1",
                "age_range": "0-1 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 50, "P": 25, "K": 50},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Fase pembentukan akar dan batang",
                "source": "ICCRI"
            },
            {
                "phase_name": "TBM Tahun 2",
                "age_range": "1-2 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 100, "P": 50, "K": 100},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pertumbuhan cabang primer",
                "source": "ICCRI"
            },
            {
                "phase_name": "TM Produktif",
                "age_range": ">2 tahun",
                "duration_months": 180,  # 15 years
                "npk_per_tree_per_year": {"N": 200, "P": 100, "K": 200},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor", "semprot"],
                "notes": "Aplikasi setelah panen untuk pemulihan",
                "source": "ICCRI, TNAU"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos", "Kulit Kopi Terkompos"],
            "premium": ["KNO3 (Kalium Nitrat)"]
        },
        "spacing": "2.5x2.5 m (Populasi 1,600 pohon/ha)",
        "first_harvest": "24-30 bulan setelah tanam"
    },
    
    "Kopi Arabika": {
        "latin_name": "Coffea arabica",
        "category": "Tanaman Keras",
        "phases": [
            {
                "phase_name": "TBM Tahun 1",
                "age_range": "0-1 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 40, "P": 20, "K": 40},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Butuh naungan, dataran tinggi 800-2000 mdpl",
                "source": "ICCRI"
            },
            {
                "phase_name": "TBM Tahun 2",
                "age_range": "1-2 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 80, "P": 40, "K": 80},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pertumbuhan vegetatif",
                "source": "ICCRI"
            },
            {
                "phase_name": "TM Produktif",
                "age_range": ">2 tahun",
                "duration_months": 180,
                "npk_per_tree_per_year": {"N": 150, "P": 75, "K": 150},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor", "semprot"],
                "notes": "Specialty coffee, kualitas tergantung nutrisi seimbang",
                "source": "ICCRI"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": ["KNO3 (Kalium Nitrat)", "Ca(NO3)2 (Kalsium Nitrat)"]
        },
        "spacing": "2.5x2.5 m (Populasi 1,600 pohon/ha)",
        "first_harvest": "30-36 bulan setelah tanam"
    },
    
    "Karet": {
        "latin_name": "Hevea brasiliensis",
        "category": "Tanaman Keras",
        "phases": [
            {
                "phase_name": "TBM Tahun 1-2",
                "age_range": "0-2 tahun",
                "duration_months": 24,
                "npk_per_tree_per_year": {"N": 200, "P": 100, "K": 150},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Fase pertumbuhan batang",
                "source": "Rubber Research Institute"
            },
            {
                "phase_name": "TBM Tahun 3-5",
                "age_range": "2-5 tahun",
                "duration_months": 36,
                "npk_per_tree_per_year": {"N": 400, "P": 200, "K": 300},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor"],
                "notes": "Persiapan sadap",
                "source": "Rubber Research Institute"
            },
            {
                "phase_name": "TM Produktif",
                "age_range": ">5 tahun",
                "duration_months": 300,  # 25 years
                "npk_per_tree_per_year": {"N": 600, "P": 300, "K": 450},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor"],
                "notes": "Fase penyadapan, N tinggi untuk produksi lateks",
                "source": "Rubber Research Institute"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": []
        },
        "spacing": "6x3 m atau 7x3 m (Populasi 476-555 pohon/ha)",
        "first_harvest": "60-72 bulan (mulai sadap)"
    },
    
    "Kelapa": {
        "latin_name": "Cocos nucifera",
        "category": "Tanaman Keras",
        "phases": [
            {
                "phase_name": "TBM Tahun 1-2",
                "age_range": "0-2 tahun",
                "duration_months": 24,
                "npk_per_tree_per_year": {"N": 200, "P": 100, "K": 300},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Kelapa suka K tinggi sejak awal",
                "source": "Coconut Research Institute"
            },
            {
                "phase_name": "TBM Tahun 3-4",
                "age_range": "2-4 tahun",
                "duration_months": 24,
                "npk_per_tree_per_year": {"N": 400, "P": 200, "K": 600},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor"],
                "notes": "Persiapan berbuah",
                "source": "Coconut Research Institute"
            },
            {
                "phase_name": "TM Produktif",
                "age_range": ">4 tahun",
                "duration_months": 600,  # 50 years
                "npk_per_tree_per_year": {"N": 600, "P": 300, "K": 900},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor", "semprot"],
                "notes": "K sangat tinggi untuk kualitas air kelapa dan kopra",
                "source": "Coconut Research Institute, TNAU"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": ["KNO3 (Kalium Nitrat)"]
        },
        "spacing": "9x9 m atau 8x8 m (Populasi 123-156 pohon/ha)",
        "first_harvest": "48-60 bulan setelah tanam"
    }
}

# ========== FRUIT TREES DATABASE ==========

FRUIT_TREES = {
    "Mangga": {
        "latin_name": "Mangifera indica",
        "category": "Tanaman Buah",
        "phases": [
            {
                "phase_name": "TBM Tahun 1",
                "age_range": "0-1 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 113, "P": 50, "K": 100},
                "application_frequency": 6,  # every 2 months
                "application_methods": ["tugal", "kocor"],
                "notes": "Fokus pertumbuhan akar dan batang",
                "source": "TNAU, Mango.org"
            },
            {
                "phase_name": "TBM Tahun 2",
                "age_range": "1-2 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 150, "P": 75, "K": 150},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pertumbuhan tajuk",
                "source": "TNAU"
            },
            {
                "phase_name": "TBM Tahun 3",
                "age_range": "2-3 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 200, "P": 100, "K": 200},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Persiapan berbuah",
                "source": "TNAU"
            },
            {
                "phase_name": "TM - Awal Musim Hujan",
                "age_range": ">3 tahun",
                "duration_months": 3,
                "npk_per_tree_per_year": {"N": 250, "P": 160, "K": 200},
                "application_frequency": 1,
                "application_methods": ["tugal", "kocor"],
                "notes": "NPK tinggi N untuk flush vegetatif",
                "source": "TNAU, Haifa Group"
            },
            {
                "phase_name": "TM - Induksi Bunga",
                "age_range": ">3 tahun",
                "duration_months": 2,
                "npk_per_tree_per_year": {"N": 0, "P": 200, "K": 400},
                "application_frequency": 2,
                "application_methods": ["kocor", "semprot"],
                "notes": "KNO3 foliar spray untuk induksi bunga, kurangi N",
                "source": "Haifa Group, TNAU"
            },
            {
                "phase_name": "TM - Pembesaran Buah",
                "age_range": ">3 tahun",
                "duration_months": 3,
                "npk_per_tree_per_year": {"N": 0, "P": 0, "K": 600},
                "application_frequency": 3,
                "application_methods": ["kocor", "semprot"],
                "notes": "K tinggi untuk ukuran dan kualitas buah",
                "source": "TNAU, Haifa Group"
            },
            {
                "phase_name": "TM - Pasca Panen",
                "age_range": ">3 tahun",
                "duration_months": 4,
                "npk_per_tree_per_year": {"N": 250, "P": 160, "K": 600},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pemulihan pohon, organik + NPK seimbang",
                "source": "TNAU"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": ["KNO3 (Kalium Nitrat)", "MKP (Mono Kalium Fosfat)"]
        },
        "spacing": "8x8 m atau 10x10 m (Populasi 100-156 pohon/ha)",
        "first_harvest": "36-48 bulan setelah tanam (dari okulasi)"
    },
    
    "Durian": {
        "latin_name": "Durio zibethinus",
        "category": "Tanaman Buah",
        "phases": [
            {
                "phase_name": "TBM Tahun 1-2",
                "age_range": "0-2 tahun",
                "duration_months": 24,
                "npk_per_tree_per_year": {"N": 300, "P": 150, "K": 150},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "N tinggi untuk pertumbuhan daun",
                "source": "Haifa Group, IPB"
            },
            {
                "phase_name": "TBM Tahun 3-4",
                "age_range": "2-4 tahun",
                "duration_months": 24,
                "npk_per_tree_per_year": {"N": 500, "P": 250, "K": 300},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Persiapan fase produktif",
                "source": "Haifa Group"
            },
            {
                "phase_name": "TM - Pre-flowering",
                "age_range": ">4 tahun",
                "duration_months": 2,
                "npk_per_tree_per_year": {"N": 200, "P": 400, "K": 600},
                "application_frequency": 2,
                "application_methods": ["kocor", "semprot"],
                "notes": "Turunkan N, tingkatkan P & K",
                "source": "Haifa Group"
            },
            {
                "phase_name": "TM - Flowering & Fruit Set",
                "age_range": ">4 tahun",
                "duration_months": 2,
                "npk_per_tree_per_year": {"N": 150, "P": 300, "K": 800},
                "application_frequency": 2,
                "application_methods": ["kocor", "semprot"],
                "notes": "NPK 9-27-27 atau MKP untuk fruit set",
                "source": "Haifa Group"
            },
            {
                "phase_name": "TM - Fruit Development",
                "age_range": ">4 tahun",
                "duration_months": 3,
                "npk_per_tree_per_year": {"N": 200, "P": 100, "K": 1000},
                "application_frequency": 3,
                "application_methods": ["kocor", "semprot"],
                "notes": "K sangat tinggi untuk ukuran dan kualitas daging buah",
                "source": "Haifa Group, Growplant.org"
            },
            {
                "phase_name": "TM - Fruit Maturation",
                "age_range": ">4 tahun",
                "duration_months": 1,
                "npk_per_tree_per_year": {"N": 0, "P": 0, "K": 400},
                "application_frequency": 2,
                "application_methods": ["semprot"],
                "notes": "Foliar K untuk kualitas akhir",
                "source": "Haifa Group"
            },
            {
                "phase_name": "TM - Post-harvest Recovery",
                "age_range": ">4 tahun",
                "duration_months": 2,
                "npk_per_tree_per_year": {"N": 400, "P": 200, "K": 400},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pemulihan tajuk, NPK seimbang + organik",
                "source": "Haifa Group"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": ["KNO3 (Kalium Nitrat)", "MKP (Mono Kalium Fosfat)", "NPK 9-27-27", "NPK 14-7-28"]
        },
        "spacing": "8x8 m atau 10x10 m (Populasi 100-156 pohon/ha)",
        "first_harvest": "48-60 bulan setelah tanam (dari okulasi)"
    },
    
    "Jeruk": {
        "latin_name": "Citrus spp.",
        "category": "Tanaman Buah",
        "phases": [
            {
                "phase_name": "TBM Tahun 1",
                "age_range": "0-1 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 100, "P": 50, "K": 50},
                "application_frequency": 6,
                "application_methods": ["tugal", "kocor"],
                "notes": "N tinggi untuk daun sehat",
                "source": "Yara Fertilizer, TNAU"
            },
            {
                "phase_name": "TBM Tahun 2",
                "age_range": "1-2 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 150, "P": 75, "K": 75},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pertumbuhan tajuk",
                "source": "Yara Fertilizer"
            },
            {
                "phase_name": "TM - Early Spring (Budbreak)",
                "age_range": ">2 tahun",
                "duration_months": 2,
                "npk_per_tree_per_year": {"N": 150, "P": 150, "K": 150},
                "application_frequency": 1,
                "application_methods": ["tugal", "kocor"],
                "notes": "NPK seimbang untuk flush awal",
                "source": "Yara Fertilizer"
            },
            {
                "phase_name": "TM - Pre-flowering",
                "age_range": ">2 tahun",
                "duration_months": 1,
                "npk_per_tree_per_year": {"N": 50, "P": 300, "K": 50},
                "application_frequency": 1,
                "application_methods": ["kocor", "semprot"],
                "notes": "P tinggi untuk energi bunga",
                "source": "Yara Fertilizer"
            },
            {
                "phase_name": "TM - Flowering & Fruit Set",
                "age_range": ">2 tahun",
                "duration_months": 2,
                "npk_per_tree_per_year": {"N": 150, "P": 150, "K": 150},
                "application_frequency": 2,
                "application_methods": ["kocor", "semprot"],
                "notes": "NPK seimbang + Ca untuk cegah fruit drop",
                "source": "Yara Fertilizer, Citrus Australia"
            },
            {
                "phase_name": "TM - Fruit Development",
                "age_range": ">2 tahun",
                "duration_months": 4,
                "npk_per_tree_per_year": {"N": 100, "P": 50, "K": 400},
                "application_frequency": 4,
                "application_methods": ["kocor", "semprot"],
                "notes": "K tinggi untuk ukuran, rasa manis, warna",
                "source": "Yara Fertilizer"
            },
            {
                "phase_name": "TM - Late Season",
                "age_range": ">2 tahun",
                "duration_months": 3,
                "npk_per_tree_per_year": {"N": 100, "P": 50, "K": 300},
                "application_frequency": 2,
                "application_methods": ["kocor", "semprot"],
                "notes": "Maintain K untuk kualitas",
                "source": "Yara Fertilizer"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": ["KNO3 (Kalium Nitrat)", "MKP (Mono Kalium Fosfat)", "Ca(NO3)2 (Kalsium Nitrat)"]
        },
        "spacing": "5x5 m atau 6x6 m (Populasi 278-400 pohon/ha)",
        "first_harvest": "24-36 bulan setelah tanam (dari okulasi)",
        "notes": "Jeruk sangat responsif terhadap mikro (Zn, Fe, Mn). Perhatikan CVPD!"
    },
    
    "Rambutan": {
        "latin_name": "Nephelium lappaceum",
        "category": "Tanaman Buah",
        "phases": [
            {
                "phase_name": "TBM Tahun 1-3",
                "age_range": "0-3 tahun",
                "duration_months": 36,
                "npk_per_tree_per_year": {"N": 200, "P": 100, "K": 150},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pertumbuhan vegetatif",
                "source": "IPB, Local Research"
            },
            {
                "phase_name": "TM - Pasca Panen",
                "age_range": ">3 tahun",
                "duration_months": 6,
                "npk_per_tree_per_year": {"N": 400, "P": 200, "K": 300},
                "application_frequency": 2,
                "application_methods": ["tugal", "kocor"],
                "notes": "NPK + organik untuk pemulihan",
                "source": "IPB"
            },
            {
                "phase_name": "TM - Induksi Bunga",
                "age_range": ">3 tahun",
                "duration_months": 3,
                "npk_per_tree_per_year": {"N": 100, "P": 300, "K": 500},
                "application_frequency": 3,
                "application_methods": ["kocor", "semprot"],
                "notes": "P & K tinggi saat daun tua",
                "source": "IPB"
            },
            {
                "phase_name": "TM - Pembesaran Buah",
                "age_range": ">3 tahun",
                "duration_months": 3,
                "npk_per_tree_per_year": {"N": 100, "P": 100, "K": 400},
                "application_frequency": 3,
                "application_methods": ["kocor", "semprot"],
                "notes": "K untuk ukuran dan rasa manis",
                "source": "IPB"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 15-15-15"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": ["KNO3 (Kalium Nitrat)"]
        },
        "spacing": "10x10 m (Populasi 100 pohon/ha)",
        "first_harvest": "48-60 bulan setelah tanam (dari okulasi)"
    },
    
    "Alpukat": {
        "latin_name": "Persea americana",
        "category": "Tanaman Buah",
        "phases": [
            {
                "phase_name": "TBM Tahun 1",
                "age_range": "0-1 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 50, "P": 25, "K": 50},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Drainase WAJIB sempurna, tidak tahan genangan",
                "source": "Agriculture Institute"
            },
            {
                "phase_name": "TBM Tahun 2",
                "age_range": "1-2 tahun",
                "duration_months": 12,
                "npk_per_tree_per_year": {"N": 200, "P": 100, "K": 100},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor"],
                "notes": "Pertumbuhan vegetatif",
                "source": "Agriculture Institute"
            },
            {
                "phase_name": "TM Produktif",
                "age_range": ">2 tahun",
                "duration_months": 240,
                "npk_per_tree_per_year": {"N": 400, "P": 200, "K": 400},
                "application_frequency": 4,
                "application_methods": ["tugal", "kocor", "semprot"],
                "notes": "NPK 12-12-17 + Boron untuk cegah buah bengkok. Organik 20kg/pohon/tahun WAJIB",
                "source": "Agriculture Institute"
            }
        ],
        "recommended_fertilizers": {
            "chemical": ["Urea", "SP-36", "KCl", "NPK 12-12-17+2MgO"],
            "organic": ["Pupuk Kandang Sapi", "Kompos"],
            "premium": ["KNO3 (Kalium Nitrat)"]
        },
        "spacing": "8x8 m (Populasi 156 pohon/ha)",
        "first_harvest": "36-48 bulan setelah tanam",
        "notes": "Alpukat SANGAT sensitif genangan air. Buat guludan/busut!"
    }
}

# Helper function to get crop data
def get_crop_data(crop_name):
    """Get crop data from either hard crops or fruit trees database"""
    if crop_name in HARD_CROPS:
        return HARD_CROPS[crop_name]
    elif crop_name in FRUIT_TREES:
        return FRUIT_TREES[crop_name]
    else:
        return None

def get_all_crops():
    """Get list of all available crops"""
    return list(HARD_CROPS.keys()) + list(FRUIT_TREES.keys())

def get_crop_category(crop_name):
    """Get category of a crop"""
    crop_data = get_crop_data(crop_name)
    return crop_data['category'] if crop_data else None
