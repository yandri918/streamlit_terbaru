"""
Rice Pest and Disease Database
Extracted from AgriSensa Commodities comprehensive database
"""

# Rice Pest Database - Comprehensive data for 8 major pests and 7 major diseases
RICE_PESTS = [
    {
        "id": "brown_planthopper",
        "name_id": "Wereng Coklat",
        "name_en": "Brown Planthopper",
        "scientific": "Nilaparvata lugens",
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
                "Tanam varietas tahan (IR64, Ciherang, Inpari 32, 42, 43)",
                "Pengairan berselang (tidak tergenang terus)",
                "Jarak tanam optimal (25x25 cm atau Jajar Legowo)",
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
    },
    {
        "id": "gall_midge",
        "name_id": "Lalat Bibit",
        "name_en": "Gall Midge",
        "scientific": "Orseolia oryzae",
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
    }
]

RICE_DISEASES = [
    {
        "id": "blast",
        "name_id": "Blas",
        "name_en": "Blast",
        "scientific": "Pyricularia oryzae",
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
    },
    {
        "id": "brown_spot",
        "name_id": "Bercak Coklat",
        "name_en": "Brown Spot",
        "scientific": "Bipolaris oryzae",
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
    }
]


def get_all_pests():
    """Get all rice pest entries"""
    return RICE_PESTS


def get_all_diseases():
    """Get all rice disease entries"""
    return RICE_DISEASES


def search_by_symptom(query):
    """Search pest/disease by symptom"""
    results = []
    query_lower = query.lower()
    
    # Search in pests
    for pest in RICE_PESTS:
        for symptom in pest["symptoms"]:
            if query_lower in symptom.lower():
                results.append(pest)
                break
    
    # Search in diseases
    for disease in RICE_DISEASES:
        for symptom in disease["symptoms"]:
            if query_lower in symptom.lower():
                results.append(disease)
                break
    
    return results


def get_by_id(pest_disease_id):
    """Get specific pest/disease by ID"""
    # Search in pests
    for pest in RICE_PESTS:
        if pest["id"] == pest_disease_id:
            return pest
    
    # Search in diseases
    for disease in RICE_DISEASES:
        if disease["id"] == pest_disease_id:
            return disease
    
    return None
