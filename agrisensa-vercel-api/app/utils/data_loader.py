"""Data loader utility for loading datasets and knowledge bases."""
import os
import pandas as pd
from flask import current_app


class DataLoader:
    """Utility class for loading data files."""
    
    @staticmethod
    def load_eda_dataset():
        """Load EDA dataset for yield planning."""
        try:
            dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'EDA_500.csv')
            if os.path.exists(dataset_path):
                return pd.read_csv(dataset_path)
            return None
        except Exception as e:
            current_app.logger.error(f"Failed to load EDA dataset: {e}")
            return None
    
    @staticmethod
    def get_fertilizer_data():
        """Get fertilizer composition data."""
        return {
            # Pupuk Anorganik
            "urea": {"name": "Urea", "content": {"N": 0.46, "P": 0, "K": 0}, "type": "anorganik"},
            "sp36": {"name": "SP-36", "content": {"N": 0, "P": 0.158, "K": 0}, "type": "anorganik"},
            "kcl": {"name": "KCL (MOP)", "content": {"N": 0, "P": 0, "K": 0.50}, "type": "anorganik"},
            "npk_mutiara": {"name": "NPK Mutiara (16-16-16)", "content": {"N": 0.16, "P": 0.07, "K": 0.13}, "type": "anorganik"},
            
            # Pupuk Organik
            "kompos": {"name": "Kompos", "content": {"N": 0.015, "P": 0.01, "K": 0.015}, "type": "organik"},
            "pupuk_kandang_sapi": {"name": "Pupuk Kandang Sapi", "content": {"N": 0.005, "P": 0.0025, "K": 0.005}, "type": "organik"},
            "pupuk_kandang_ayam": {"name": "Pupuk Kandang Ayam", "content": {"N": 0.015, "P": 0.013, "K": 0.008}, "type": "organik"},
            "pupuk_kandang_kambing": {"name": "Pupuk Kandang Kambing", "content": {"N": 0.007, "P": 0.003, "K": 0.009}, "type": "organik"},
            "bokashi": {"name": "Bokashi", "content": {"N": 0.02, "P": 0.015, "K": 0.018}, "type": "organik"},
            "vermikompos": {"name": "Vermikompos (Kascing)", "content": {"N": 0.02, "P": 0.018, "K": 0.015}, "type": "organik"}
        }
    
    @staticmethod
    def get_knowledge_base():
        """Get agricultural knowledge base."""
        return {
            "padi": {
                "name": "Padi",
                "icon": "🌾",
                "data": {
                    "Persiapan Lahan": [
                        "Olah tanah sempurna: Bajak sedalam 20-25 cm, lalu garu.",
                        "Perbaikan pH: Jika masam (pH < 6), aplikasikan Dolomit 1-2 ton/ha.",
                        "Pupuk Dasar: Berikan kompos 5-10 ton/ha dan SP-36."
                    ],
                    "Persemaian & Penanaman": [
                        "Perlakuan Benih: Rendam benih dalam larutan PGPR.",
                        "Sistem Tanam: Terapkan Jajar Legowo untuk meningkatkan populasi.",
                        "Umur Bibit: Pindahkan bibit pada umur 15-21 HSS."
                    ]
                }
            },
            "cabai": {
                "name": "Cabai",
                "icon": "🌶️",
                "data": {
                    "Persiapan Lahan": [
                        "Buat bedengan tinggi (30-40 cm).",
                        "Pastikan pH di rentang 6.0 - 7.0 dengan Dolomit.",
                        "Gunakan mulsa plastik perak-hitam."
                    ]
                }
            },
            "jagung": {
                "name": "Jagung",
                "icon": "🌽",
                "data": {
                    "Persiapan Lahan": [
                        "Bajak tanah sedalam 15-20 cm.",
                        "Berikan pupuk kandang/kompos sebagai pupuk dasar."
                    ]
                }
            }
        }
    
    @staticmethod
    def get_fertilizer_dosage_db():
        """Get fertilizer dosage database."""
        return {
            "padi": {
                "name": "Padi",
                "complex_schedule": {
                    "Fase Vegetatif (0-30 HST)": {
                        "Urea": 100, "SP-36": 100, "KCL": 50,
                        "notes": "Aplikasi saat umur 7-10 HST dan 21 HST."
                    },
                    "Fase Generatif (31-60 HST)": {
                        "Urea": 125, "SP-36": 25, "KCL": 25,
                        "notes": "Aplikasi saat pembentukan malai (primordia)."
                    }
                },
                "anorganik_kg_ha": {"Urea": 225, "SP-36": 125, "KCL": 75}, # Total for backward compatibility
                "organik_ton_ha": {"Pupuk Kandang Sapi": 10, "Pupuk Kandang Ayam": 5},
                "dolomit_ton_ha_asam": 1.5
            },
            "jagung": {
                "name": "Jagung",
                "complex_schedule": {
                    "Dasar (0 HST)": {
                        "Urea": 100, "SP-36": 125, "KCL": 25,
                        "notes": "Campur dengan tanah saat tanam."
                    },
                    "Vegetatif (21-30 HST)": {
                        "Urea": 100, "KCL": 25,
                        "notes": "Tugalkan 5-10 cm dari batang."
                    },
                    "Generatif (45-50 HST)": {
                        "Urea": 50, "KCL": 25,
                        "notes": "Saat pembentukan tongkol."
                    }
                },
                "anorganik_kg_ha": {"Urea": 250, "SP-36": 125, "KCL": 75},
                "organik_ton_ha": {"Pupuk Kandang Sapi": 10, "Pupuk Kandang Ayam": 7},
                "dolomit_ton_ha_asam": 1.5
            },
            "cabai": {
                "name": "Cabai",
                "complex_schedule": {
                    "Dasar (Pre-Plant)": {
                        "SP-36": 150, "KCL": 100, "ZA": 100,
                        "notes": "Aduk rata di bedengan 1 minggu sebelum tanam."
                    },
                    "Vegetatif (1-4 MST)": {
                        "NPK 16-16-16": 200, "Urea": 50,
                        "notes": "Kocor setiap minggu (5 gram/tanaman)."
                    },
                    "Generatif (5-12 MST)": {
                        "NPK 16-16-16": 300, "KCL": 100, "MKP": 50,
                        "notes": "Tugalkan atau kocor interval 10 hari."
                    }
                },
                "anorganik_kg_ha": {"Urea": 150, "SP-36": 250, "KCL": 200},
                "organik_ton_ha": {"Pupuk Kandang Sapi": 15, "Pupuk Kandang Ayam": 10},
                "dolomit_ton_ha_asam": 2.0
            },
            "tomat": {
                "name": "Tomat",
                "complex_schedule": {
                    "Dasar": {
                        "SP-36": 200, "KCL": 100, "ZA": 100,
                        "notes": "Tabur di bedengan."
                    },
                    "Susulan 1 (15 HST)": {
                        "NPK 16-16-16": 150,
                        "notes": "Kocor di sekitar akar."
                    },
                    "Susulan 2 (30 HST)": {
                        "NPK 16-16-16": 150, "KCL": 50,
                        "notes": "Saat mulai berbunga."
                    },
                    "Susulan 3 (45 HST)": {
                        "KCL": 100, "KNO3 Merah": 50,
                        "notes": "Pembesaran buah."
                    }
                },
                "anorganik_kg_ha": {"Urea": 100, "SP-36": 200, "KCL": 250},
                "organik_ton_ha": {"Pupuk Kandang Sapi": 15},
                "dolomit_ton_ha_asam": 1.5
            },
            "bawang_merah": {
                "name": "Bawang Merah",
                "complex_schedule": {
                    "Dasar": {
                        "SP-36": 150, "KCL": 50,
                        "notes": "Campur tanah bedengan."
                    },
                    "Susulan 1 (10-15 HST)": {
                        "NPK 16-16-16": 200,
                        "notes": "Tabur merata."
                    },
                    "Susulan 2 (30-35 HST)": {
                        "NPK 16-16-16": 100, "KCL": 100, "ZA": 100,
                        "notes": "Fase pembentukan umbi."
                    }
                },
                "anorganik_kg_ha": {"NPK 16-16-16": 300, "SP-36": 150, "KCL": 150},
                "organik_ton_ha": {"Pupuk Kandang Ayam": 10},
                "dolomit_ton_ha_asam": 1.0
            },
            "kentang": {
                "name": "Kentang",
                "complex_schedule": {
                    "Dasar": {
                        "SP-36": 250, "KCL": 150, "Urea": 100,
                        "notes": "Berikan di garitan tanam."
                    },
                    "Susulan 1 (30 HST)": {
                        "NPK 15-15-15": 300, "ZA": 100,
                        "notes": "Saat pembumbunan pertama."
                    },
                    "Susulan 2 (50 HST)": {
                        "KCL": 100, "ZK": 50,
                        "notes": "Fase pengisian umbi."
                    }
                },
                "anorganik_kg_ha": {"Urea": 200, "SP-36": 250, "KCL": 250},
                "organik_ton_ha": {"Pupuk Kandang Sapi": 20},
                "dolomit_ton_ha_asam": 2.0
            },
            "melon": {
                "name": "Melon",
                "complex_schedule": {
                    "Dasar": {
                        "NPK 16-16-16": 150, "SP-36": 100,
                        "notes": "Aduk di lubang tanam."
                    },
                    "Vegetatif (1-3 MST)": {
                        "NPK 16-16-16": 100, "KNO3 Merah": 50,
                        "notes": "Kocor rutin."
                    },
                    "Generatif (4-7 MST)": {
                        "KNO3 Putih": 100, "MKP": 50, "Kalsium": 50,
                        "notes": "Fokus pembentukan jaring dan manis buah."
                    }
                },
                "anorganik_kg_ha": {"NPK 16-16-16": 250, "SP-36": 100, "KNO3": 150},
                "organik_ton_ha": {"Pupuk Kandang Ayam": 15},
                "dolomit_ton_ha_asam": 1.5
            },
            "semangka": {
                "name": "Semangka",
                "complex_schedule": {
                    "Dasar": {
                        "NPK 15-15-15": 150, "SP-36": 100,
                        "notes": "Dasar bedengan."
                    },
                    "Vegetatif (7-21 HST)": {
                        "Urea": 50, "NPK 15-15-15": 100,
                        "notes": "Kocor untuk memacu sulur."
                    },
                    "Generatif (30-50 HST)": {
                        "KCL": 100, "NPK 15-15-15": 100,
                        "notes": "Pembesaran buah."
                    }
                },
                "anorganik_kg_ha": {"NPK 15-15-15": 250, "Urea": 100, "KCL": 150},
                "organik_ton_ha": {"Pupuk Kandang Sapi": 15},
                "dolomit_ton_ha_asam": 1.5
            },
            "kedelai": {
                "name": "Kedelai",
                "complex_schedule": {
                    "Dasar (0 HST)": {
                        "Urea": 25, "SP-36": 100, "KCL": 50,
                        "notes": "Sebar merata saat olah tanah."
                    },
                    "Susulan (20-25 HST)": {
                        "Urea": 25, "KCL": 25,
                        "notes": "Jika pertumbuhan kurang subur."
                    }
                },
                "anorganik_kg_ha": {"Urea": 50, "SP-36": 100, "KCL": 75},
                "organik_ton_ha": {"Pupuk Kandang Sapi": 8, "Pupuk Kandang Ayam": 5},
                "dolomit_ton_ha_asam": 1.5
            }
        }
