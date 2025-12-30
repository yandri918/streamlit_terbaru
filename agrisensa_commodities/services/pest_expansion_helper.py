"""
Helper module to load pest database expansion
"""

def get_expansion_data():
    """Returns dictionary with all expansion entries"""
    
    expansion = {
        "corn_pests": [
            # Corn Earworm
            {
                "id": "corn_earworm",
                "name_id": "Ulat Tongkol",
                "name_en": "Corn Earworm",
                "scientific": "Helicoverpa armigera",
                "type": "pest",
                "severity": "high",
                "symptoms": [
                    "Tongkol berlubang",
                    "Biji dimakan",
                    "Kotoran ulat di tongkol",
                    "Penurunan kualitas 30-50%"
                ],
                "damage_stage": ["Generatif"],
                "control": {
                    "cultural": [
                        "Tanam serempak",
                        "Pasang perangkap feromon",
                        "Petik tongkol terserang"
                    ],
                    "biological": [
                        "Trichogramma spp.",
                        "NPV (Nuclear Polyhedrosis Virus)",
                        "Chrysoperla carnea"
                    ],
                    "chemical": [
                        "Emamektin benzoat 5 WG (0.5 g/L)",
                        "Indoxacarb 15 EC (0.5 ml/L)",
                        "Spinetoram 12 SC (0.5 ml/L)"
                    ]
                },
                "economic_threshold": "5% tongkol terserang",
                "peak_season": "Fase pembentukan tongkol"
            }
            # Add more corn pests here...
        ],
        "corn_diseases": [
            # Add corn diseases...
        ],
        # Add tomato, chili, soybean...
    }
    
    return expansion
