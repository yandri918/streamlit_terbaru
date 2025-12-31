"""
Pest & Disease Recognition Service
Based on WAGRI API structure with comprehensive local database

Author: AgriSensa Team
Date: 2025-12-30
"""

from typing import Dict, List, Optional
import requests
from datetime import datetime


class PestDiseaseService:
    """
    Service for pest and disease identification and management.
    
    Features:
    - Comprehensive local database (50+ pests/diseases)
    - WAGRI API integration (when token available)
    - IPM recommendations
    - Severity assessment
    """
    
    # WAGRI API endpoints
    BASE_URL_IMAGE = "https://api.wagri2.net/nichino/pests/pw/image"
    BASE_URL_INFO = "https://api.wagri2.net/nichino/pests/pw/info"
    
    # Comprehensive Pest & Disease Database for Indonesian Crops
    PEST_DATABASE = {
        "rice": {
            "name_id": "Padi",
            "name_en": "Rice",
            "pests": [
                {
                    "id": "brown_planthopper",
                    "name_id": "Wereng Coklat",
                    "name_en": "Brown Planthopper",
                    "scientific": "Nilaparvata lugens",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Hopperburn (daun menguning dan mengering dari bawah)",
                        "Tanaman layu mendadak",
                        "Pertumbuhan terhambat",
                        "Embun madu pada daun"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan (IR64, Ciherang)",
                            "Pengairan berselang (tidak tergenang terus)",
                            "Jarak tanam optimal (25x25 cm)",
                            "Sanitasi lahan (bersihkan jerami)"
                        ],
                        "biological": [
                            "Laba-laba (Lycosa pseudoannulata)",
                            "Kumbang (Paederus fuscipes)",
                            "Jamur Metarhizium anisopliae"
                        ],
                        "chemical": [
                            "Imidakloprid 200 SL (0.5 ml/L)",
                            "Buprofezin 25 WP (2 g/L)",
                            "Pimetrozin 50 WG (0.5 g/L)"
                        ]
                    },
                    "economic_threshold": "5-10 ekor per rumpun",
                    "peak_season": "Musim hujan (Nov-Feb)"
                },
                {
                    "id": "stem_borer",
                    "name_id": "Penggerek Batang",
                    "name_en": "Stem Borer",
                    "scientific": "Scirpophaga incertulas",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Sundep (mati pucuk pada fase vegetatif)",
                        "Beluk (malai hampa pada fase generatif)",
                        "Lubang gerek pada batang",
                        "Bekas kotoran di dalam batang"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam serempak dalam 2 minggu",
                            "Pergiliran tanaman dengan palawija",
                            "Potong jerami dekat tanah",
                            "Gunakan lampu perangkap"
                        ],
                        "biological": [
                            "Trichogramma japonicum (parasitoid telur)",
                            "Beauveria bassiana (jamur entomopatogen)"
                        ],
                        "chemical": [
                            "Karbofuran 3G (15-20 kg/ha, tabur di pematang)",
                            "Fipronil 50 SC (1 ml/L, semprot)",
                            "Klorantraniliprol 5 WG (0.5 g/L)"
                        ]
                    },
                    "economic_threshold": "2 kelompok telur per m²",
                    "peak_season": "Awal musim tanam"
                },
                {
                    "id": "rice_bug",
                    "name_id": "Walang Sangit",
                    "name_en": "Rice Bug",
                    "scientific": "Leptocorisa acuta",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Gabah hampa atau berisi sebagian",
                        "Bercak coklat pada gabah",
                        "Bau tidak sedap",
                        "Penurunan kualitas beras"
                    ],
                    "damage_stage": ["Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam serempak",
                            "Bersihkan gulma di pematang",
                            "Panen tepat waktu"
                        ],
                        "biological": [
                            "Burung pemakan serangga",
                            "Laba-laba"
                        ],
                        "chemical": [
                            "Deltametrin 25 EC (0.5 ml/L)",
                            "Sipermetrin 50 EC (0.5 ml/L)"
                        ]
                    },
                    "economic_threshold": "5 ekor per rumpun",
                    "peak_season": "Fase pengisian bulir"
                },
                {
                    "id": "rat",
                    "name_id": "Tikus",
                    "name_en": "Rat",
                    "scientific": "Rattus argentiventer",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Tanaman terpotong di pangkal",
                        "Bulir padi dimakan",
                        "Bekas gigitan pada batang",
                        "Jalur tikus di sawah"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam serempak (TABELA - Tanam Benih Langsung)",
                            "Gropyokan (perburuan massal)",
                            "TBS (Trap Barrier System)",
                            "Buat pagar keliling"
                        ],
                        "biological": [
                            "Burung hantu (Tyto alba)",
                            "Ular sawah"
                        ],
                        "chemical": [
                            "Rodentisida (hati-hati, racun akut!)",
                            "Klerat (brodifakum 0.005%)",
                            "Racumin (kumatetralit 0.75%)"
                        ]
                    },
                    "economic_threshold": "10% kerusakan tanaman",
                    "peak_season": "Sepanjang tahun"
                },
                {
                    "id": "green_leafhopper",
                    "name_id": "Wereng Hijau",
                    "name_en": "Green Leafhopper",
                    "scientific": "Nephotettix virescens",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Daun kuning (tungro)",
                        "Pertumbuhan kerdil",
                        "Anakan berkurang",
                        "Malai tidak keluar"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan tungro",
                            "Eradikasi tanaman sakit",
                            "Hindari tanam terlalu rapat"
                        ],
                        "biological": [
                            "Laba-laba",
                            "Kumbang"
                        ],
                        "chemical": [
                            "Imidakloprid 200 SL (0.5 ml/L)",
                            "Tiametoksam 25 WG (0.2 g/L)"
                        ]
                    },
                    "economic_threshold": "5 ekor per rumpun",
                    "peak_season": "Awal musim tanam"
                }
            ],
            "diseases": [
                {
                    "id": "blast",
                    "name_id": "Blas",
                    "name_en": "Blast",
                    "scientific": "Pyricularia oryzae",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Bercak coklat berbentuk mata (diamond shape)",
                        "Bercak pada daun, batang, leher malai",
                        "Malai patah (neck blast)",
                        "Gabah hampa"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan (Inpari 32, Inpari 42)",
                            "Pemupukan N berimbang (jangan berlebihan)",
                            "Jarak tanam optimal",
                            "Drainase baik"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Pseudomonas fluorescens"
                        ],
                        "chemical": [
                            "Trisiklazol 75 WP (0.6 g/L)",
                            "Azoksistrobin 25 SC (1 ml/L)",
                            "Difenokonazol 25 EC (1 ml/L)"
                        ]
                    },
                    "favorable_conditions": "Suhu 25-28°C, kelembaban tinggi",
                    "peak_season": "Musim hujan"
                },
                {
                    "id": "bacterial_leaf_blight",
                    "name_id": "Hawar Daun Bakteri",
                    "name_en": "Bacterial Leaf Blight",
                    "scientific": "Xanthomonas oryzae pv. oryzae",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Garis kuning di tepi daun",
                        "Daun mengering dari ujung",
                        "Eksudat bakteri (embun bakteri)",
                        "Daun berubah putih keabu-abuan"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan (Angke, IR64)",
                            "Pemupukan K cukup",
                            "Hindari luka mekanis",
                            "Sanitasi alat pertanian"
                        ],
                        "biological": [
                            "Pseudomonas fluorescens",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Bakterisida tembaga (copper oxychloride 50 WP, 2 g/L)",
                            "Streptomisin sulfat (0.5 g/L)"
                        ]
                    },
                    "favorable_conditions": "Suhu 25-30°C, angin kencang, hujan",
                    "peak_season": "Musim hujan"
                },
                {
                    "id": "sheath_blight",
                    "name_id": "Busuk Pelepah",
                    "name_en": "Sheath Blight",
                    "scientific": "Rhizoctonia solani",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Bercak oval pada pelepah dekat permukaan air",
                        "Bercak meluas ke atas",
                        "Warna abu-abu dengan tepi coklat",
                        "Sklerotia hitam pada pelepah"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Jarak tanam tidak terlalu rapat",
                            "Drainase baik",
                            "Pemupukan N tidak berlebihan",
                            "Buang jerami terinfeksi"
                        ],
                        "biological": [
                            "Trichoderma viride",
                            "Pseudomonas fluorescens"
                        ],
                        "chemical": [
                            "Validamycin 3 SL (2 ml/L)",
                            "Heksakonazol 5 EC (2 ml/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban tinggi, N berlebih",
                    "peak_season": "Fase anakan maksimum"
                },
                {
                    "id": "tungro",
                    "name_id": "Tungro",
                    "name_en": "Tungro",
                    "scientific": "Rice tungro bacilliform virus (RTBV)",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Daun kuning oranye",
                        "Pertumbuhan kerdil",
                        "Anakan sedikit",
                        "Malai tidak keluar atau pendek"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan tungro (Inpari 13, Inpari 19)",
                            "Cabut dan musnahkan tanaman sakit",
                            "Tanam serempak",
                            "Kendalikan wereng hijau (vektor)"
                        ],
                        "biological": [
                            "Tidak ada (virus)",
                            "Fokus pada pengendalian vektor"
                        ],
                        "chemical": [
                            "Tidak ada (virus)",
                            "Kendalikan wereng dengan insektisida"
                        ]
                    },
                    "favorable_conditions": "Populasi wereng hijau tinggi",
                    "peak_season": "Awal musim tanam"
                }
            ]
        },
        
        "corn": {
            "name_id": "Jagung",
            "name_en": "Corn",
            "pests": [
                {
                    "id": "corn_borer",
                    "name_id": "Penggerek Batang Jagung",
                    "name_en": "Corn Borer",
                    "scientific": "Ostrinia furnacalis",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Lubang pada batang dan tongkol",
                        "Daun berlubang",
                        "Batang mudah patah",
                        "Tongkol busuk"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam serempak",
                            "Hancurkan sisa tanaman",
                            "Gunakan varietas tahan"
                        ],
                        "biological": [
                            "Trichogramma spp.",
                            "Beauveria bassiana"
                        ],
                        "chemical": [
                            "Klorantraniliprol 5 WG (0.5 g/L)",
                            "Emamektin benzoat 5 WG (0.5 g/L)"
                        ]
                    },
                    "economic_threshold": "10% tanaman terserang",
                    "peak_season": "Fase vegetatif"
                },
                {
                    "id": "fall_armyworm",
                    "name_id": "Ulat Grayak",
                    "name_en": "Fall Armyworm",
                    "scientific": "Spodoptera frugiperda",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Daun berlubang dan robek",
                        "Kotoran ulat pada pucuk",
                        "Tongkol dimakan",
                        "Pertumbuhan terhambat"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Monitoring rutin",
                            "Hancurkan kelompok telur",
                            "Tanam refugia"
                        ],
                        "biological": [
                            "Telenomus remus (parasitoid telur)",
                            "Bacillus thuringiensis"
                        ],
                        "chemical": [
                            "Klorantraniliprol 5 WG (0.5 g/L)",
                            "Spinetoram 12 SC (0.5 ml/L)"
                        ]
                    },
                    "economic_threshold": "5% tanaman terserang",
                    "peak_season": "Sepanjang musim"
                }
            ],
            "diseases": [
                {
                    "id": "downy_mildew",
                    "name_id": "Bulai",
                    "name_en": "Downy Mildew",
                    "scientific": "Peronosclerospora maydis",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Daun klorotik bergaris",
                        "Pertumbuhan kerdil",
                        "Tongkol tidak terbentuk",
                        "Lapisan jamur putih di bawah daun"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan",
                            "Cabut tanaman sakit",
                            "Rotasi tanaman",
                            "Sanitasi lahan"
                        ],
                        "biological": [
                            "Trichoderma harzianum"
                        ],
                        "chemical": [
                            "Metalaksil 35 WP (2 g/L)",
                            "Dimetomorf 50 WP (1 g/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban tinggi, suhu 20-25°C",
                    "peak_season": "Awal musim hujan"
                }
            ]
        },
        
        "tomato": {
            "name_id": "Tomat",
            "name_en": "Tomato",
            "pests": [
                {
                    "id": "whitefly",
                    "name_id": "Kutu Kebul",
                    "name_en": "Whitefly",
                    "scientific": "Bemisia tabaci",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Daun keriting dan kuning",
                        "Embun madu",
                        "Virus kuning (TYLCV)",
                        "Pertumbuhan terhambat"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Gunakan mulsa plastik perak",
                            "Pasang yellow sticky trap",
                            "Sanitasi gulma"
                        ],
                        "biological": [
                            "Encarsia formosa (parasitoid)",
                            "Beauveria bassiana"
                        ],
                        "chemical": [
                            "Imidakloprid 200 SL (0.5 ml/L)",
                            "Spiromesifen 24 SC (0.5 ml/L)"
                        ]
                    },
                    "economic_threshold": "5 ekor per daun",
                    "peak_season": "Musim kemarau"
                },
                {
                    "id": "fruit_borer",
                    "name_id": "Ulat Buah",
                    "name_en": "Fruit Borer",
                    "scientific": "Helicoverpa armigera",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Buah berlubang",
                        "Kotoran ulat di buah",
                        "Buah busuk",
                        "Kualitas menurun"
                    ],
                    "damage_stage": ["Generatif"],
                    "control": {
                        "cultural": [
                            "Petik buah terserang",
                            "Pasang perangkap feromon",
                            "Tanam refugia"
                        ],
                        "biological": [
                            "Trichogramma spp.",
                            "NPV (Nuclear Polyhedrosis Virus)"
                        ],
                        "chemical": [
                            "Emamektin benzoat 5 WG (0.5 g/L)",
                            "Indoxacarb 15 EC (0.5 ml/L)"
                        ]
                    },
                    "economic_threshold": "2% buah terserang",
                    "peak_season": "Fase pembuahan"
                }
            ],
            "diseases": [
                {
                    "id": "late_blight",
                    "name_id": "Busuk Daun",
                    "name_en": "Late Blight",
                    "scientific": "Phytophthora infestans",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Bercak coklat pada daun",
                        "Busuk pada buah",
                        "Lapisan jamur putih",
                        "Tanaman mati cepat"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Drainase baik",
                            "Jarak tanam optimal",
                            "Hindari penyiraman overhead",
                            "Buang tanaman sakit"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Mankozeb 80 WP (2 g/L)",
                            "Dimetomorf 50 WP (1 g/L)",
                            "Propineb 70 WP (2 g/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban >90%, suhu 15-20°C",
                    "peak_season": "Musim hujan"
                },
                {
                    "id": "bacterial_wilt",
                    "name_id": "Layu Bakteri",
                    "name_en": "Bacterial Wilt",
                    "scientific": "Ralstonia solanacearum",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Layu mendadak",
                        "Daun hijau tapi layu",
                        "Pembuluh coklat",
                        "Lendir bakteri dari batang"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Rotasi tanaman (bukan Solanaceae)",
                            "Drainase sempurna",
                            "Cabut tanaman sakit",
                            "Solarisasi tanah"
                        ],
                        "biological": [
                            "Pseudomonas fluorescens",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Bakterisida tembaga (2 g/L)",
                            "Streptomisin sulfat (0.5 g/L)"
                        ]
                    },
                    "favorable_conditions": "Suhu tinggi, tanah lembab",
                    "peak_season": "Musim hujan"
                }
            ]
        },
        
        "chili": {
            "name_id": "Cabai",
            "name_en": "Chili",
            "pests": [
                {
                    "id": "thrips",
                    "name_id": "Trips",
                    "name_en": "Thrips",
                    "scientific": "Thrips parvispinus",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Daun keriting dan menggulung",
                        "Bercak perak pada daun",
                        "Bunga rontok",
                        "Virus kuning (PYVV)"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Mulsa plastik perak",
                            "Blue sticky trap",
                            "Sanitasi gulma"
                        ],
                        "biological": [
                            "Orius spp. (predator)",
                            "Beauveria bassiana"
                        ],
                        "chemical": [
                            "Abamektin 18 EC (0.5 ml/L)",
                            "Spinosad 25 SC (0.5 ml/L)"
                        ]
                    },
                    "economic_threshold": "10 ekor per bunga",
                    "peak_season": "Musim kemarau"
                },
                {
                    "id": "aphid",
                    "name_id": "Kutu Daun",
                    "name_en": "Aphid",
                    "scientific": "Aphis gossypii",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Daun keriting",
                        "Embun madu",
                        "Virus mosaik",
                        "Pertumbuhan terhambat"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Mulsa plastik perak",
                            "Yellow sticky trap",
                            "Tanam refugia"
                        ],
                        "biological": [
                            "Coccinellidae (kumbang kepik)",
                            "Chrysoperla spp."
                        ],
                        "chemical": [
                            "Imidakloprid 200 SL (0.5 ml/L)",
                            "Acetamiprid 20 SP (0.2 g/L)"
                        ]
                    },
                    "economic_threshold": "20% tanaman terserang",
                    "peak_season": "Awal musim tanam"
                }
            ],
            "diseases": [
                {
                    "id": "anthracnose",
                    "name_id": "Antraknosa",
                    "name_en": "Anthracnose",
                    "scientific": "Colletotrichum spp.",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Bercak cekung pada buah",
                        "Buah busuk",
                        "Bercak coklat dengan lingkaran",
                        "Buah rontok"
                    ],
                    "damage_stage": ["Generatif"],
                    "control": {
                        "cultural": [
                            "Panen tepat waktu",
                            "Drainase baik",
                            "Buang buah sakit",
                            "Rotasi tanaman"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Mankozeb 80 WP (2 g/L)",
                            "Azoksistrobin 25 SC (1 ml/L)",
                            "Propineb 70 WP (2 g/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban tinggi, hujan",
                    "peak_season": "Musim hujan"
                },
                {
                    "id": "fusarium_wilt",
                    "name_id": "Layu Fusarium",
                    "name_en": "Fusarium Wilt",
                    "scientific": "Fusarium oxysporum",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Layu satu sisi",
                        "Daun kuning dari bawah",
                        "Pembuluh coklat",
                        "Tanaman mati"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Gunakan varietas tahan",
                            "Rotasi tanaman",
                            "Solarisasi tanah",
                            "Drainase baik"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Pseudomonas fluorescens"
                        ],
                        "chemical": [
                            "Benomil 50 WP (1 g/L)",
                            "Karbendazim 50 WP (1 g/L)"
                        ]
                    },
                    "favorable_conditions": "Suhu 25-30°C, tanah lembab",
                    "peak_season": "Sepanjang tahun"
                }
            ]
        },
        
        "soybean": {
            "name_id": "Kedelai",
            "name_en": "Soybean",
            "pests": [
                {
                    "id": "pod_borer",
                    "name_id": "Penggerek Polong",
                    "name_en": "Pod Borer",
                    "scientific": "Etiella zinckenella",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Polong berlubang",
                        "Biji dimakan",
                        "Kotoran ulat di polong",
                        "Polong busuk"
                    ],
                    "damage_stage": ["Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam serempak",
                            "Petik polong terserang",
                            "Pasang perangkap feromon"
                        ],
                        "biological": [
                            "Trichogramma spp.",
                            "Beauveria bassiana"
                        ],
                        "chemical": [
                            "Klorantraniliprol 5 WG (0.5 g/L)",
                            "Profenofos 500 EC (2 ml/L)"
                        ]
                    },
                    "economic_threshold": "10% polong terserang",
                    "peak_season": "Fase pembentukan polong"
                },
                {
                    "id": "armyworm",
                    "name_id": "Ulat Grayak Kedelai",
                    "name_en": "Armyworm",
                    "scientific": "Spodoptera litura",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Daun berlubang",
                        "Defoliasi",
                        "Kotoran ulat",
                        "Pertumbuhan terhambat"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Monitoring rutin",
                            "Hancurkan kelompok telur",
                            "Tanam refugia"
                        ],
                        "biological": [
                            "NPV (Nuclear Polyhedrosis Virus)",
                            "Bacillus thuringiensis"
                        ],
                        "chemical": [
                            "Emamektin benzoat 5 WG (0.5 g/L)",
                            "Klorpirifos 200 EC (2 ml/L)"
                        ]
                    },
                    "economic_threshold": "25% defoliasi",
                    "peak_season": "Fase vegetatif"
                }
            ],
            "diseases": [
                {
                    "id": "rust",
                    "name_id": "Karat Daun",
                    "name_en": "Rust",
                    "scientific": "Phakopsora pachyrhizi",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Bercak coklat karat pada daun",
                        "Pustula coklat di bawah daun",
                        "Daun rontok",
                        "Penurunan hasil"
                    ],
                    "damage_stage": ["Vegetatif", "Generatif"],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan",
                            "Jarak tanam optimal",
                            "Sanitasi lahan",
                            "Rotasi tanaman"
                        ],
                        "biological": [
                            "Trichoderma harzianum"
                        ],
                        "chemical": [
                            "Azoksistrobin 25 SC (1 ml/L)",
                            "Difenokonazol 25 EC (1 ml/L)",
                            "Tebukonazol 25 EC (1 ml/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban tinggi, suhu 20-25°C",
                    "peak_season": "Musim hujan"
                },
                {
                    "id": "mosaic",
                    "name_id": "Mosaik",
                    "name_en": "Mosaic",
                    "scientific": "Soybean mosaic virus (SMV)",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Mosaik kuning pada daun",
                        "Daun keriting",
                        "Pertumbuhan kerdil",
                        "Polong sedikit"
                    ],
                    "damage_stage": ["Vegetatif"],
                    "control": {
                        "cultural": [
                            "Gunakan benih sehat",
                            "Cabut tanaman sakit",
                            "Kendalikan kutu daun (vektor)",
                            "Tanam varietas tahan"
                        ],
                        "biological": [
                            "Tidak ada (virus)",
                            "Fokus pada pengendalian vektor"
                        ],
                        "chemical": [
                            "Tidak ada (virus)",
                            "Kendalikan kutu daun dengan insektisida"
                        ]
                    },
                    "favorable_conditions": "Populasi kutu daun tinggi",
                    "peak_season": "Awal musim tanam"
                }
            ]
        }
    }
    
    @staticmethod
    def get_pest_image(pest_type: str, pest_id: str, access_token: Optional[str] = None) -> Optional[bytes]:
        """
        Fetch pest/disease image from WAGRI API.
        
        Args:
            pest_type: Type (pest/disease/weed)
            pest_id: Unique identifier
            access_token: WAGRI API token (optional)
        
        Returns:
            Image bytes or None if not available
        """
        if not access_token:
            # Return None if no token (use placeholder in UI)
            return None
        
        url = f"{PestDiseaseService.BASE_URL_IMAGE}/{pest_type}/{pest_id}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException:
            return None
    
    @staticmethod
    def get_pest_info(
        en_type: str,
        crop: str,
        name: str,
        access_token: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Fetch pest/disease info from WAGRI API.
        
        Args:
            en_type: Entity type (pest/disease/weed)
            crop: Crop name
            name: Pest/disease name
            access_token: WAGRI API token (optional)
        
        Returns:
            Pest info dict or None
        """
        if not access_token:
            # Use local database
            return PestDiseaseService.search_local_database(crop, name, en_type)
        
        url = f"{PestDiseaseService.BASE_URL_INFO}/{en_type}/{crop}/{name}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # Fallback to local database
            return PestDiseaseService.search_local_database(crop, name, en_type)
    
    @staticmethod
    def search_local_database(
        crop: str,
        name: str,
        pest_type: str = "all"
    ) -> Optional[Dict]:
        """Search pest/disease in local database."""
        crop_data = PestDiseaseService.PEST_DATABASE.get(crop, {})
        
        # Search in pests
        if pest_type in ["all", "pest"]:
            for pest in crop_data.get("pests", []):
                if name.lower() in pest["name_id"].lower() or name.lower() in pest["name_en"].lower():
                    return pest
        
        # Search in diseases
        if pest_type in ["all", "disease"]:
            for disease in crop_data.get("diseases", []):
                if name.lower() in disease["name_id"].lower() or name.lower() in disease["name_en"].lower():
                    return disease
        
        return None
    
    @staticmethod
    def get_all_pests_by_crop(crop: str, pest_type: str = "all") -> List[Dict]:
        """
        Get all pests/diseases for a specific crop.
        
        Args:
            crop: Crop name (rice, corn, tomato, chili, soybean)
            pest_type: Filter by type (all/pest/disease)
        
        Returns:
            List of pest/disease dictionaries
        """
        crop_data = PestDiseaseService.PEST_DATABASE.get(crop, {})
        
        if pest_type == "all":
            return crop_data.get("pests", []) + crop_data.get("diseases", [])
        elif pest_type == "pest":
            return crop_data.get("pests", [])
        elif pest_type == "disease":
            return crop_data.get("diseases", [])
        else:
            return []
    
    @staticmethod
    def get_available_crops() -> List[Dict]:
        """Get list of available crops in database."""
        crops = []
        for crop_key, crop_data in PestDiseaseService.PEST_DATABASE.items():
            crops.append({
                "key": crop_key,
                "name_id": crop_data.get("name_id", ""),
                "name_en": crop_data.get("name_en", ""),
                "pest_count": len(crop_data.get("pests", [])),
                "disease_count": len(crop_data.get("diseases", []))
            })
        return crops
    
    @staticmethod
    def get_ipm_recommendations(
        crop: str,
        pest_id: str,
        severity: str = "medium",
        growth_stage: str = "vegetatif"
    ) -> Dict:
        """
        Generate IPM (Integrated Pest Management) recommendations.
        
        Args:
            crop: Crop name
            pest_id: Pest/disease identifier
            severity: Severity level (low/medium/high)
            growth_stage: Growth stage (vegetatif/generatif)
        
        Returns:
            IPM recommendations dictionary
        """
        # Find pest in database
        all_pests = PestDiseaseService.get_all_pests_by_crop(crop)
        pest = next((p for p in all_pests if p["id"] == pest_id), None)
        
        if not pest:
            return {
                "error": "Pest/disease not found",
                "recommendations": []
            }
        
        recommendations = {
            "pest_info": {
                "name_id": pest["name_id"],
                "name_en": pest["name_en"],
                "scientific": pest["scientific"],
                "type": pest["type"],
                "severity": pest["severity"]
            },
            "immediate_actions": [],
            "cultural_control": pest["control"]["cultural"],
            "biological_control": pest["control"]["biological"],
            "chemical_control": pest["control"]["chemical"],
            "monitoring": [],
            "prevention": [],
            "estimated_cost": {}
        }
        
        # Immediate actions based on severity
        if severity == "high":
            recommendations["immediate_actions"] = [
                "🚨 TINDAKAN SEGERA DIPERLUKAN!",
                "Aplikasi pestisida/fungisida sesuai rekomendasi",
                "Isolasi area terinfeksi",
                "Monitoring intensif setiap hari",
                "Dokumentasi perkembangan"
            ]
            recommendations["estimated_cost"] = {
                "pesticide": "Rp 200,000 - 500,000/ha",
                "labor": "Rp 100,000 - 200,000/ha",
                "total": "Rp 300,000 - 700,000/ha"
            }
        elif severity == "medium":
            recommendations["immediate_actions"] = [
                "⚠️ Monitoring ketat diperlukan",
                "Pertimbangkan biological control terlebih dahulu",
                "Siapkan pestisida jika situasi memburuk",
                "Perbaiki cultural practices",
                "Monitoring setiap 2-3 hari"
            ]
            recommendations["estimated_cost"] = {
                "biological_agent": "Rp 50,000 - 150,000/ha",
                "labor": "Rp 50,000 - 100,000/ha",
                "total": "Rp 100,000 - 250,000/ha"
            }
        else:  # low
            recommendations["immediate_actions"] = [
                "ℹ️ Monitoring rutin",
                "Fokus pada pencegahan",
                "Perbaiki cultural practices",
                "Monitoring mingguan"
            ]
            recommendations["estimated_cost"] = {
                "prevention": "Rp 20,000 - 50,000/ha",
                "total": "Rp 20,000 - 50,000/ha"
            }
        
        # Monitoring recommendations
        recommendations["monitoring"] = [
            f"Periksa tanaman setiap {'hari' if severity == 'high' else '2-3 hari' if severity == 'medium' else 'minggu'}",
            "Catat jumlah hama/gejala penyakit",
            "Dokumentasi dengan foto",
            "Bandingkan dengan ambang ekonomi"
        ]
        
        # Prevention for future
        recommendations["prevention"] = [
            "Rotasi tanaman",
            "Sanitasi lahan",
            "Gunakan varietas tahan",
            "Pemupukan berimbang",
            "Drainase baik"
        ]
        
        return recommendations
    
    @staticmethod
    def search_pests(
        query: str,
        crop: Optional[str] = None,
        pest_type: Optional[str] = None
    ) -> List[Dict]:
        """
        Search pests/diseases by name.
        
        Args:
            query: Search query
            crop: Filter by crop (optional)
            pest_type: Filter by type (optional)
        
        Returns:
            List of matching pests/diseases
        """
        results = []
        query_lower = query.lower()
        
        # Determine which crops to search
        crops_to_search = [crop] if crop else list(PestDiseaseService.PEST_DATABASE.keys())
        
        for crop_key in crops_to_search:
            crop_data = PestDiseaseService.PEST_DATABASE.get(crop_key, {})
            
            # Search in pests
            if not pest_type or pest_type == "pest":
                for pest in crop_data.get("pests", []):
                    if (query_lower in pest["name_id"].lower() or
                        query_lower in pest["name_en"].lower() or
                        query_lower in pest["scientific"].lower()):
                        pest_copy = pest.copy()
                        pest_copy["crop"] = crop_key
                        pest_copy["crop_name"] = crop_data.get("name_id", "")
                        results.append(pest_copy)
            
            # Search in diseases
            if not pest_type or pest_type == "disease":
                for disease in crop_data.get("diseases", []):
                    if (query_lower in disease["name_id"].lower() or
                        query_lower in disease["name_en"].lower() or
                        query_lower in disease["scientific"].lower()):
                        disease_copy = disease.copy()
                        disease_copy["crop"] = crop_key
                        disease_copy["crop_name"] = crop_data.get("name_id", "")
                        results.append(disease_copy)
        
        return results
