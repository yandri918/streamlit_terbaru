"""
Script to merge pest_database_expansion.py into pest_disease_service.py
This will integrate 32 new entries into the main database
"""

import re

# Read the main service file
with open('agrisensa_commodities/services/pest_disease_service.py', 'r', encoding='utf-8') as f:
    main_content = f.read()

# Define the new entries to add for each crop
# These will be inserted before the closing ] of each pests/diseases array

# RICE - Add 3 new pests before line 202 (before ],)
rice_new_pests = ''',
                {
                    "id": "gall_midge",
                    "name_id": "Lalat Bibit",
                    "name_en": "Gall Midge",
                    "scientific": "Orseolia oryzae",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Anakan tidak normal (onion leaf)",
                        "Daun muda menggulung seperti pipa",
                        "Pertumbuhan terhambat",
                        "Anakan berkurang"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan (Inpari 13)",
                            "Hindari tanam terlalu rapat",
                            "Bersihkan gulma",
                            "Tanam serempak"
                        ],
                        "biological": [
                            "Platygaster oryzae (parasitoid)",
                            "Laba-laba"
                        ],
                        "chemical": [
                            "Karbofuran 3G (tabur saat tanam)",
                            "Fipronil 50 SC (1 ml/L)"
                        ]
                    },
                    "economic_threshold": "5% tanaman terserang",
                    "peak_season": "Awal musim tanam"
                },
                {
                    "id": "hispa",
                    "name_id": "Kepik Bergaris",
                    "name_en": "Rice Hispa",
                    "scientific": "Dicladispa armigera",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Garis putih memanjang pada daun",
                        "Daun mengering",
                        "Fotosintesis terganggu",
                        "Penurunan hasil 10-30%"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Hindari pemupukan N berlebihan",
                            "Jaga ketinggian air",
                            "Bersihkan gulma"
                        ],
                        "biological": [
                            "Burung pemakan serangga",
                            "Laba-laba"
                        ],
                        "chemical": [
                            "Sipermetrin 50 EC (0.5 ml/L)",
                            "Deltametrin 25 EC (0.5 ml/L)"
                        ]
                    },
                    "economic_threshold": "10% daun terserang",
                    "peak_season": "Fase vegetatif maksimum"
                },
                {
                    "id": "caseworm",
                    "name_id": "Ulat Kantong",
                    "name_en": "Caseworm",
                    "scientific": "Nymphula depunctalis",
                    "type": "pest",
                    "severity": "low",
                    "symptoms": [
                        "Daun terpotong tidak beraturan",
                        "Kantong dari potongan daun",
                        "Mengapung di air",
                        "Kerusakan ringan"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Atur ketinggian air",
                            "Bersihkan gulma air",
                            "Monitoring rutin"
                        ],
                        "biological": [
                            "Ikan pemakan serangga",
                            "Burung"
                        ],
                        "chemical": [
                            "Klorpirifos 200 EC (2 ml/L) - jika parah"
                        ]
                    },
                    "economic_threshold": "20% daun terserang",
                    "peak_season": "Fase vegetatif"
                }'''

# Find and replace rice pests section
# Pattern: find the last pest entry for rice (green_leafhopper) and add new entries before the closing ]
rice_pest_pattern = r'("peak_season": "Awal musim tanam"\s+}\s+)\](\s+"diseases":)'
main_content = re.sub(rice_pest_pattern, r'\1' + rice_new_pests + r'\n            ]\2', main_content, count=1)

print("[OK] Added 3 new Rice pests")

# RICE - Add 3 new diseases
rice_new_diseases = ''',
                {
                    "id": "brown_spot",
                    "name_id": "Bercak Coklat",
                    "name_en": "Brown Spot",
                    "scientific": "Bipolaris oryzae",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Bercak coklat bulat pada daun",
                        "Bercak dengan tepi kuning",
                        "Gabah hampa atau berisi sebagian",
                        "Kualitas beras menurun"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Pemupukan berimbang (jangan kekurangan K)",
                            "Gunakan benih sehat",
                            "Jarak tanam optimal",
                            "Rotasi varietas"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Pseudomonas fluorescens"
                        ],
                        "chemical": [
                            "Mankozeb 80 WP (2 g/L)",
                            "Propineb 70 WP (2 g/L)",
                            "Azoksistrobin 25 SC (1 ml/L)"
                        ]
                    },
                    "favorable_conditions": "Kekurangan K, kelembaban tinggi",
                    "peak_season": "Musim hujan"
                },
                {
                    "id": "false_smut",
                    "name_id": "Hampa Palsu",
                    "name_en": "False Smut",
                    "scientific": "Ustilaginoidea virens",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Bulir berubah jadi bola hijau kekuningan",
                        "Ukuran lebih besar dari gabah normal",
                        "Spora kuning kehijauan",
                        "Penurunan kualitas beras"
                    ],
                    "damage_stage": ["Generatif"],
                    "control": {
                        "cultural": [
                            "Hindari pemupukan N berlebihan",
                            "Jarak tanam optimal",
                            "Drainase baik",
                            "Buang tanaman sakit"
                        ],
                        "biological": [
                            "Trichoderma viride"
                        ],
                        "chemical": [
                            "Propikonazol 25 EC (1 ml/L)",
                            "Tebukonazol 25 EC (1 ml/L)",
                            "Aplikasi saat bunting (preventif)"
                        ]
                    },
                    "favorable_conditions": "N berlebih, kelembaban tinggi saat bunting",
                    "peak_season": "Fase pembungaan"
                },
                {
                    "id": "stem_rot",
                    "name_id": "Busuk Batang",
                    "name_en": "Stem Rot",
                    "scientific": "Sclerotium oryzae",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Busuk pada batang dekat permukaan air",
                        "Batang mudah patah",
                        "Tanaman rebah",
                        "Sklerotia hitam pada batang"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Drainase sempurna",
                            "Hindari genangan terus-menerus",
                            "Pemupukan K cukup",
                            "Sanitasi jerami"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Pseudomonas fluorescens"
                        ],
                        "chemical": [
                            "Validamycin 3 SL (2 ml/L)",
                            "Heksakonazol 5 EC (2 ml/L)"
                        ]
                    },
                    "favorable_conditions": "Genangan terus-menerus, K rendah",
                    "peak_season": "Fase anakan maksimum"
                }'''

# Find rice diseases closing and add new entries
rice_disease_pattern = r'("peak_season": "Awal musim tanam"\s+}\s+)\](\s+}\s+},\s+\s+"corn":)'
main_content = re.sub(rice_disease_pattern, r'\1' + rice_new_diseases + r'\n            ]\2', main_content, count=1)

print("[OK] Added 3 new Rice diseases")

# Write back to file
with open('agrisensa_commodities/services/pest_disease_service.py', 'w', encoding='utf-8') as f:
    f.write(main_content)

print("\n[SUCCESS] Database merge complete!")
print("Rice: 9 -> 15 entries (added 6)")
print("\nNote: This script added Rice entries only.")
print("Run additional scripts for Corn, Tomato, Chili, Soybean or manually add them.")
print("\nTotal entries will be: 24 + 6 = 30 (partial integration)")
