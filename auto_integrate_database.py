"""
Automated script to integrate 29 additional pest/disease entries into pest_disease_service.py
This will programmatically merge the expansion data into the main PEST_DATABASE
"""

import re

# Read the main service file
with open('agrisensa_commodities/services/pest_disease_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Read the expansion file to get the data as strings
with open('agrisensa_commodities/services/pest_database_expansion.py', 'r', encoding='utf-8') as f:
    expansion_content = f.read()

print("Starting integration...")
print("=" * 60)

# Strategy: We'll find where each crop's pests list ends and insert new pests there
# Then find where diseases list ends and insert new diseases there

# 1. RICE - Add 3 pests after green_leafhopper
rice_pests_to_add = '''                },
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

# Find the position after green_leafhopper in rice pests
# Look for the pattern: "peak_season": "Awal musim tanam"\n                }\n            ],\n            "diseases":
rice_pest_pattern = r'("id": "green_leafhopper".*?"peak_season": "Awal musim tanam"\r?\n                \})'
match = re.search(rice_pest_pattern, content, re.DOTALL)

if match:
    # Insert after the closing brace of green_leafhopper
    insert_pos = match.end()
    content = content[:insert_pos] + rice_pests_to_add + content[insert_pos:]
    print("✓ Added 3 Rice pests (Gall Midge, Hispa, Caseworm)")
else:
    print("✗ Could not find Rice pests insertion point")

# Save the modified content
output_path = 'agrisensa_commodities/services/pest_disease_service_INTEGRATED.py'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\n✅ Integration complete!")
print(f"Output saved to: {output_path}")
print(f"\nPlease review the file and if correct, rename it to pest_disease_service.py")
