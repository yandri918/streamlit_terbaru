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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                },
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                    "peak_season": "Awal musim tanam",
                    "source": "Balai Penelitian Padi, 2024"
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                    "peak_season": "Fase vegetatif maksimum",
                    "source": "Syngenta Indonesia, 2024"
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                    "peak_season": "Fase vegetatif",
                    "source": "BASF Agricultural Solutions, 2024"
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                },
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "peak_season": "Musim hujan",
                    "source": "Bayer CropScience Indonesia, 2024"
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
                    "damage_stage": [
                        "Generatif"
                    ],
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
                    "peak_season": "Fase pembungaan",
                    "source": "Kementerian Pertanian RI, 2024"
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "peak_season": "Fase anakan maksimum",
                    "source": "Balitbangtan, 2024"
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                },
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
                    "damage_stage": [
                        "Generatif"
                    ],
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
                    "peak_season": "Fase pembentukan tongkol",
                    "source": "Bayer CropScience, 2024"
                },
                {
                    "id": "aphid_corn",
                    "name_id": "Kutu Daun Jagung",
                    "name_en": "Corn Aphid",
                    "scientific": "Rhopalosiphum maidis",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Koloni kutu pada pucuk dan tongkol",
                        "Embun madu",
                        "Daun keriting",
                        "Vektor virus mosaik"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Tanam refugia",
                            "Hindari tanam terlalu rapat",
                            "Monitoring rutin"
                        ],
                        "biological": [
                            "Coccinellidae (kumbang kepik)",
                            "Chrysoperla spp.",
                            "Aphidius spp. (parasitoid)"
                        ],
                        "chemical": [
                            "Imidakloprid 200 SL (0.5 ml/L)",
                            "Acetamiprid 20 SP (0.2 g/L)",
                            "Tiametoksam 25 WG (0.2 g/L)"
                        ]
                    },
                    "economic_threshold": "30% tanaman terserang",
                    "peak_season": "Fase vegetatif",
                    "source": "Syngenta Indonesia, 2024"
                },
                {
                    "id": "cutworm",
                    "name_id": "Ulat Tanah",
                    "name_en": "Cutworm",
                    "scientific": "Agrotis ipsilon",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Tanaman muda terpotong di pangkal",
                        "Tanaman rebah",
                        "Lubang pada batang muda",
                        "Kerusakan di malam hari"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Olah tanah sempurna",
                            "Bersihkan gulma",
                            "Tanam trap crop (sawi)",
                            "Hand picking malam hari"
                        ],
                        "biological": [
                            "Beauveria bassiana",
                            "Bacillus thuringiensis"
                        ],
                        "chemical": [
                            "Klorpirifos 200 EC (2 ml/L, siram pangkal)",
                            "Karbofuran 3G (tabur saat tanam)"
                        ]
                    },
                    "economic_threshold": "10% tanaman terserang",
                    "peak_season": "Awal musim tanam",
                    "source": "BASF Agricultural Solutions, 2024"
                },
                {
                    "id": "grasshopper",
                    "name_id": "Belalang",
                    "name_en": "Grasshopper",
                    "scientific": "Locusta migratoria",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Daun berlubang tidak beraturan",
                        "Defoliasi berat jika serangan massal",
                        "Pertumbuhan terhambat",
                        "Penurunan hasil 20-40%"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Bersihkan gulma di sekitar lahan",
                            "Tanam serempak",
                            "Monitoring populasi"
                        ],
                        "biological": [
                            "Burung pemakan serangga",
                            "Metarhizium anisopliae"
                        ],
                        "chemical": [
                            "Sipermetrin 50 EC (0.5 ml/L)",
                            "Deltametrin 25 EC (0.5 ml/L)"
                        ]
                    },
                    "economic_threshold": "5 ekor per tanaman",
                    "peak_season": "Musim kemarau",
                    "source": "Kementerian Pertanian RI, 2024"
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                },
                {
                    "id": "leaf_blight",
                    "name_id": "Hawar Daun",
                    "name_en": "Northern Corn Leaf Blight",
                    "scientific": "Exserohilum turcicum",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Bercak memanjang abu-abu pada daun",
                        "Bercak meluas dan menyatu",
                        "Daun mengering",
                        "Penurunan hasil 30-70%"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan",
                            "Rotasi tanaman",
                            "Sanitasi sisa tanaman",
                            "Jarak tanam optimal"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Azoksistrobin 25 SC (1 ml/L)",
                            "Difenokonazol 25 EC (1 ml/L)",
                            "Mankozeb 80 WP (2 g/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban tinggi, suhu 20-27°C",
                    "peak_season": "Musim hujan",
                    "source": "Bayer CropScience, 2024"
                },
                {
                    "id": "rust_corn",
                    "name_id": "Karat Daun Jagung",
                    "name_en": "Common Rust",
                    "scientific": "Puccinia sorghi",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Pustula coklat kemerahan pada daun",
                        "Pustula di kedua sisi daun",
                        "Daun menguning dan mengering",
                        "Penurunan hasil 10-30%"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan",
                            "Pemupukan berimbang",
                            "Jarak tanam optimal"
                        ],
                        "biological": [
                            "Trichoderma harzianum"
                        ],
                        "chemical": [
                            "Azoksistrobin 25 SC (1 ml/L)",
                            "Tebukonazol 25 EC (1 ml/L)",
                            "Propikonazol 25 EC (1 ml/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban tinggi, suhu 16-23°C",
                    "peak_season": "Musim hujan",
                    "source": "Syngenta Indonesia, 2024"
                },
                {
                    "id": "stalk_rot",
                    "name_id": "Busuk Batang Jagung",
                    "name_en": "Stalk Rot",
                    "scientific": "Fusarium verticillioides",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Batang busuk dari dalam",
                        "Batang mudah patah",
                        "Tanaman rebah",
                        "Tongkol tidak terisi penuh"
                    ],
                    "damage_stage": [
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Tanam varietas tahan",
                            "Pemupukan K cukup",
                            "Hindari populasi terlalu tinggi",
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
                    "favorable_conditions": "Stress tanaman, K rendah",
                    "peak_season": "Fase pengisian biji",
                    "source": "BASF Agricultural Solutions, 2024"
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Generatif"
                    ],
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
                },
                {
                    "id": "leafminer",
                    "name_id": "Lalat Pengorok Daun",
                    "name_en": "Leafminer",
                    "scientific": "Liriomyza spp.",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Garis-garis putih berkelok pada daun",
                        "Daun menguning",
                        "Fotosintesis terganggu",
                        "Penurunan hasil 10-20%"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Pasang yellow sticky trap",
                            "Sanitasi gulma",
                            "Rotasi tanaman",
                            "Hindari tanam terlalu rapat"
                        ],
                        "biological": [
                            "Diglyphus isaea (parasitoid)",
                            "Dacnusa sibirica (parasitoid)"
                        ],
                        "chemical": [
                            "Abamektin 18 EC (0.5 ml/L)",
                            "Cyromazine 75 WP (0.5 g/L)",
                            "Spinosad 25 SC (0.5 ml/L)"
                        ]
                    },
                    "economic_threshold": "3 larva per daun",
                    "peak_season": "Sepanjang tahun",
                    "source": "Syngenta Indonesia, 2024"
                },
                {
                    "id": "spider_mite",
                    "name_id": "Tungau Merah",
                    "name_en": "Two-spotted Spider Mite",
                    "scientific": "Tetranychus urticae",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Bintik kuning pada daun",
                        "Jaring laba-laba halus",
                        "Daun kering dan rontok",
                        "Penurunan hasil 30-50%"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Jaga kelembaban",
                            "Penyiraman overhead",
                            "Hindari stress air",
                            "Sanitasi gulma"
                        ],
                        "biological": [
                            "Phytoseiulus persimilis (predator)",
                            "Amblyseius californicus (predator)"
                        ],
                        "chemical": [
                            "Abamektin 18 EC (0.5 ml/L)",
                            "Spiromesifen 24 SC (0.5 ml/L)",
                            "Propargite 73 EC (2 ml/L)"
                        ]
                    },
                    "economic_threshold": "5 tungau per daun",
                    "peak_season": "Musim kemarau",
                    "source": "Bayer CropScience, 2024"
                },
                {
                    "id": "nematode",
                    "name_id": "Nematoda Puru Akar",
                    "name_en": "Root-knot Nematode",
                    "scientific": "Meloidogyne spp.",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Puru pada akar",
                        "Pertumbuhan kerdil",
                        "Daun kuning",
                        "Layu siang hari"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Rotasi dengan non-host (jagung)",
                            "Solarisasi tanah",
                            "Gunakan varietas tahan",
                            "Sanitasi akar terinfeksi"
                        ],
                        "biological": [
                            "Paecilomyces lilacinus",
                            "Trichoderma harzianum",
                            "Pochonia chlamydosporia"
                        ],
                        "chemical": [
                            "Karbofuran 3G (20 kg/ha, aplikasi tanah)",
                            "Fenamifos 10 G (aplikasi saat tanam)"
                        ]
                    },
                    "economic_threshold": "10% tanaman terserang",
                    "peak_season": "Sepanjang tahun",
                    "source": "BASF Agricultural Solutions, 2024"
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                },
                {
                    "id": "early_blight",
                    "name_id": "Bercak Daun Awal",
                    "name_en": "Early Blight",
                    "scientific": "Alternaria solani",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Bercak coklat dengan lingkaran konsentris",
                        "Bercak mulai dari daun bawah",
                        "Daun menguning dan rontok",
                        "Bercak pada buah"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Rotasi tanaman (bukan Solanaceae)",
                            "Sanitasi sisa tanaman",
                            "Hindari penyiraman overhead",
                            "Mulsa plastik"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Mankozeb 80 WP (2 g/L)",
                            "Azoksistrobin 25 SC (1 ml/L)",
                            "Difenokonazol 25 EC (1 ml/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban tinggi, suhu 24-29°C",
                    "peak_season": "Musim hujan",
                    "source": "Bayer CropScience, 2024"
                },
                {
                    "id": "fusarium_wilt_tomato",
                    "name_id": "Layu Fusarium Tomat",
                    "name_en": "Fusarium Wilt",
                    "scientific": "Fusarium oxysporum f.sp. lycopersici",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Layu satu sisi tanaman",
                        "Daun kuning dari bawah",
                        "Pembuluh coklat (potong batang)",
                        "Tanaman mati"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Gunakan varietas tahan",
                            "Rotasi tanaman",
                            "Solarisasi tanah",
                            "pH tanah 6.5-7.0"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Pseudomonas fluorescens",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Benomil 50 WP (1 g/L, siram)",
                            "Karbendazim 50 WP (1 g/L, siram)"
                        ]
                    },
                    "favorable_conditions": "Suhu 25-30°C, pH rendah",
                    "peak_season": "Sepanjang tahun",
                    "source": "Syngenta Indonesia, 2024"
                },
                {
                    "id": "virus_tylcv",
                    "name_id": "Virus Kuning Keriting",
                    "name_en": "Tomato Yellow Leaf Curl Virus",
                    "scientific": "TYLCV",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Daun menggulung ke atas",
                        "Daun kuning",
                        "Pertumbuhan kerdil",
                        "Bunga rontok, buah sedikit"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Gunakan varietas tahan",
                            "Mulsa plastik perak",
                            "Cabut tanaman sakit",
                            "Kendalikan kutu kebul (vektor)"
                        ],
                        "biological": [
                            "Tidak ada (virus)",
                            "Fokus pada pengendalian vektor"
                        ],
                        "chemical": [
                            "Tidak ada (virus)",
                            "Kendalikan kutu kebul dengan Imidakloprid"
                        ]
                    },
                    "favorable_conditions": "Populasi kutu kebul tinggi",
                    "peak_season": "Musim kemarau",
                    "source": "Kementerian Pertanian RI, 2024"
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                },
                {
                    "id": "mite_chili",
                    "name_id": "Tungau Kuning",
                    "name_en": "Yellow Mite",
                    "scientific": "Polyphagotarsonemus latus",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Daun muda menggulung ke bawah",
                        "Daun kaku dan rapuh",
                        "Pertumbuhan terhambat",
                        "Bunga rontok"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Hindari stress air",
                            "Jaga kelembaban",
                            "Sanitasi gulma",
                            "Monitoring rutin"
                        ],
                        "biological": [
                            "Amblyseius spp. (predator)",
                            "Beauveria bassiana"
                        ],
                        "chemical": [
                            "Abamektin 18 EC (0.5 ml/L)",
                            "Spiromesifen 24 SC (0.5 ml/L)",
                            "Propargite 73 EC (2 ml/L)"
                        ]
                    },
                    "economic_threshold": "3 tungau per pucuk",
                    "peak_season": "Musim kemarau",
                    "source": "Bayer CropScience, 2024"
                },
                {
                    "id": "fruit_fly",
                    "name_id": "Lalat Buah",
                    "name_en": "Fruit Fly",
                    "scientific": "Bactrocera spp.",
                    "type": "pest",
                    "severity": "high",
                    "symptoms": [
                        "Buah berlubang kecil",
                        "Buah busuk",
                        "Larva di dalam buah",
                        "Penurunan kualitas 40-60%"
                    ],
                    "damage_stage": [
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Petik buah terserang",
                            "Pasang perangkap metil eugenol",
                            "Bungkus buah",
                            "Sanitasi buah jatuh"
                        ],
                        "biological": [
                            "Fopius arisanus (parasitoid)",
                            "Beauveria bassiana"
                        ],
                        "chemical": [
                            "Spinosad 25 SC (0.5 ml/L)",
                            "Malathion 57 EC (2 ml/L)",
                            "Aplikasi spot spray"
                        ]
                    },
                    "economic_threshold": "2% buah terserang",
                    "peak_season": "Fase pembuahan",
                    "source": "Syngenta Indonesia, 2024"
                },
                {
                    "id": "leafhopper",
                    "name_id": "Wereng Hijau Cabai",
                    "name_en": "Leafhopper",
                    "scientific": "Empoasca spp.",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Daun keriting",
                        "Tepi daun terbakar (hopperburn)",
                        "Pertumbuhan terhambat",
                        "Vektor penyakit"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Mulsa plastik perak",
                            "Yellow sticky trap",
                            "Tanam refugia"
                        ],
                        "biological": [
                            "Laba-laba",
                            "Beauveria bassiana"
                        ],
                        "chemical": [
                            "Imidakloprid 200 SL (0.5 ml/L)",
                            "Tiametoksam 25 WG (0.2 g/L)"
                        ]
                    },
                    "economic_threshold": "10 ekor per tanaman",
                    "peak_season": "Awal musim tanam",
                    "source": "BASF Agricultural Solutions, 2024"
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
                    "damage_stage": [
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                },
                {
                    "id": "powdery_mildew",
                    "name_id": "Embun Tepung",
                    "name_en": "Powdery Mildew",
                    "scientific": "Leveillula taurica",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Lapisan putih seperti tepung pada daun",
                        "Daun menguning",
                        "Daun rontok",
                        "Penurunan hasil 20-30%"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Jarak tanam optimal",
                            "Hindari kelembaban berlebihan",
                            "Sanitasi daun sakit",
                            "Pemupukan berimbang"
                        ],
                        "biological": [
                            "Ampelomyces quisqualis",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Sulfur 80 WP (2 g/L)",
                            "Azoksistrobin 25 SC (1 ml/L)",
                            "Difenokonazol 25 EC (1 ml/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban sedang, suhu 20-25°C",
                    "peak_season": "Musim kemarau",
                    "source": "Bayer CropScience, 2024"
                },
                {
                    "id": "bacterial_spot",
                    "name_id": "Bercak Bakteri",
                    "name_en": "Bacterial Spot",
                    "scientific": "Xanthomonas campestris pv. vesicatoria",
                    "type": "disease",
                    "severity": "high",
                    "symptoms": [
                        "Bercak coklat dengan halo kuning",
                        "Bercak pada daun dan buah",
                        "Daun rontok",
                        "Buah cacat"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Gunakan benih sehat",
                            "Hindari penyiraman overhead",
                            "Sanitasi alat",
                            "Rotasi tanaman"
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
                    "favorable_conditions": "Hujan, angin, suhu 25-30°C",
                    "peak_season": "Musim hujan",
                    "source": "Syngenta Indonesia, 2024"
                },
                {
                    "id": "virus_cmv",
                    "name_id": "Virus Mosaik Mentimun",
                    "name_en": "Cucumber Mosaic Virus",
                    "scientific": "CMV",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Mosaik kuning pada daun",
                        "Daun keriting",
                        "Buah cacat",
                        "Pertumbuhan kerdil"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Gunakan varietas tahan",
                            "Cabut tanaman sakit",
                            "Kendalikan kutu daun (vektor)",
                            "Mulsa plastik perak"
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
                    "peak_season": "Awal musim tanam",
                    "source": "Kementerian Pertanian RI, 2024"
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
                    "damage_stage": [
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                },
                {
                    "id": "bean_fly",
                    "name_id": "Lalat Kacang",
                    "name_en": "Bean Fly",
                    "scientific": "Ophiomyia phaseoli",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Garis-garis pada batang muda",
                        "Batang bengkok",
                        "Tanaman mati (serangan berat)",
                        "Penurunan populasi tanaman"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Tanam serempak",
                            "Gunakan benih berlapis insektisida",
                            "Olah tanah sempurna",
                            "Monitoring rutin"
                        ],
                        "biological": [
                            "Opius spp. (parasitoid)"
                        ],
                        "chemical": [
                            "Karbofuran 3G (saat tanam)",
                            "Imidakloprid 200 SL (seed treatment)"
                        ]
                    },
                    "economic_threshold": "10% tanaman terserang",
                    "peak_season": "Awal musim tanam",
                    "source": "Bayer CropScience, 2024"
                },
                {
                    "id": "whitefly_soybean",
                    "name_id": "Kutu Kebul Kedelai",
                    "name_en": "Whitefly",
                    "scientific": "Bemisia tabaci",
                    "type": "pest",
                    "severity": "medium",
                    "symptoms": [
                        "Daun kuning",
                        "Embun madu",
                        "Vektor virus",
                        "Pertumbuhan terhambat"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Mulsa plastik perak",
                            "Yellow sticky trap",
                            "Sanitasi gulma",
                            "Tanam refugia"
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
                    "peak_season": "Musim kemarau",
                    "source": "Syngenta Indonesia, 2024"
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
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
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
                    "damage_stage": [
                        "Vegetatif"
                    ],
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
                },
                {
                    "id": "downy_mildew_soybean",
                    "name_id": "Embun Bulu",
                    "name_en": "Downy Mildew",
                    "scientific": "Peronospora manshurica",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Bercak kuning pada daun",
                        "Lapisan abu-abu di bawah daun",
                        "Daun rontok",
                        "Penurunan hasil 10-20%"
                    ],
                    "damage_stage": [
                        "Vegetatif"
                    ],
                    "control": {
                        "cultural": [
                            "Gunakan benih sehat",
                            "Rotasi tanaman",
                            "Jarak tanam optimal",
                            "Drainase baik"
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
                    "peak_season": "Musim hujan",
                    "source": "BASF Agricultural Solutions, 2024"
                },
                {
                    "id": "frogeye_leaf_spot",
                    "name_id": "Bercak Daun Cercospora",
                    "name_en": "Frogeye Leaf Spot",
                    "scientific": "Cercospora sojina",
                    "type": "disease",
                    "severity": "medium",
                    "symptoms": [
                        "Bercak coklat dengan tepi ungu",
                        "Bercak bulat seperti mata katak",
                        "Daun rontok",
                        "Penurunan hasil 15-25%"
                    ],
                    "damage_stage": [
                        "Vegetatif",
                        "Generatif"
                    ],
                    "control": {
                        "cultural": [
                            "Rotasi tanaman",
                            "Gunakan varietas tahan",
                            "Sanitasi sisa tanaman",
                            "Jarak tanam optimal"
                        ],
                        "biological": [
                            "Trichoderma harzianum",
                            "Bacillus subtilis"
                        ],
                        "chemical": [
                            "Azoksistrobin 25 SC (1 ml/L)",
                            "Difenokonazol 25 EC (1 ml/L)",
                            "Mankozeb 80 WP (2 g/L)"
                        ]
                    },
                    "favorable_conditions": "Kelembaban tinggi, suhu 25-30°C",
                    "peak_season": "Musim hujan",
                    "source": "Kementerian Pertanian RI, 2024"
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
