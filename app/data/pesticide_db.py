"""Database of pesticide active ingredients.
Source: IRAC, FRAC, and Indonesian Agricultural Ministry Guidelines.
"""

class PesticideDatabase:
    """Static database for pesticide active ingredients."""
    
    @staticmethod
    def get_all_pesticides():
        """Return dictionary of active ingredients."""
        return {
            # INSEKTISIDA (INSECTICIDES)
            "abamektin": {
                "id": "abamektin",
                "name": "Abamektin",
                "type": "Insektisida",
                "group": "Avermectin",
                "irac_code": "6",
                "mode_of_action": "Kontak & Lambung, Translaminar",
                "description": "Insektisida antibiotik yang bekerja dengan menghambat transmisi sinyal saraf serangga (saluran klorida). Sangat efektif untuk hama pengisap dan pengerat.",
                "targets": ["Thrips", "Kutu Daun", "Tungau (Mites)", "Penggerek Daun (Leafminer)", "Ulat Grayak", "Wereng Coklat"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 7,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Semprotkan saat populasi hama mencapai ambang batas. Jangan campur dengan fungisida berbahan aktif sulfur. Efektif untuk hama yang bersembunyi di balik daun."
            },
            "imidakloprid": {
                "id": "imidakloprid",
                "name": "Imidakloprid",
                "type": "Insektisida",
                "group": "Neonicotinoid",
                "irac_code": "4A",
                "mode_of_action": "Sistemik",
                "description": "Insektisida sistemik yang bekerja pada reseptor asetilkolin nikotinik. Diserap akar dan daun, lalu didistribusikan ke seluruh tanaman.",
                "targets": ["Wereng Coklat", "Kutu Kebul", "Aphids", "Kutu Daun", "Lalat Buah", "Rayap"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 14,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Dapat diaplikasikan semprot atau kocor (drenching). Sangat toksik terhadap lebah, hindari aplikasi saat tanaman berbunga."
            },
            "spinetoram": {
                "id": "spinetoram",
                "name": "Spinetoram",
                "type": "Insektisida",
                "group": "Spinosyn",
                "irac_code": "5",
                "mode_of_action": "Kontak & Lambung",
                "description": "Turunan produk fermentasi bakteri tanah Saccharopolyspora spinosa. Bekerja cepat melumpuhkan sistem saraf serangga.",
                "targets": ["Thrips", "Ulat Grayak", "Penggerek Buah", "Ulat Daun"],
                "safety": {
                    "toxicity_class": "Biru (Cukup Berbahaya)",
                    "phi_days": 3,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Gunakan rotasi dengan grup lain untuk mencegah resistensi thrips. Relatif aman untuk musuh alami tertentu."
            },
            "klorantraniliprol": {
                "id": "klorantraniliprol",
                "name": "Klorantraniliprol",
                "type": "Insektisida",
                "group": "Diamida",
                "irac_code": "28",
                "mode_of_action": "Sistemik & Kontak",
                "description": "Insektisida modern yang bekerja pada reseptor ryanodine, menyebabkan penghentian makan yang cepat dan kelumpuhan otot.",
                "targets": ["Penggerek Batang Padi", "Ulat Grayak", "Ulat Buah", "Penggulung Daun", "Ulat Krop"],
                "safety": {
                    "toxicity_class": "Hijau (Cukup Aman)",
                    "phi_days": 3,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Efektifitas jangka panjang (residu lama). Aman untuk musuh alami. Cocok untuk program PHT."
            },
            "fipronil": {
                "id": "fipronil",
                "name": "Fipronil",
                "type": "Insektisida",
                "group": "Phenylpyrazole",
                "irac_code": "2B",
                "mode_of_action": "Sistemik & Kontak",
                "description": "Menghambat reseptor GABA pada sistem saraf pusat serangga. Efektif pada dosis rendah.",
                "targets": ["Wereng Coklat", "Rayap", "Semut", "Penggerek Batang", "Orong-orong"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 14,
                    "signal_word": "BERBAHAYA"
                },
                "usage": "Sangat efektif untuk perlakuan benih (seed treatment) atau semprot. Sangat toksik bagi ikan dan lebah."
            },
            "sipermetrin": {
                "id": "sipermetrin",
                "name": "Sipermetrin",
                "type": "Insektisida",
                "group": "Piretroit Sintetik",
                "irac_code": "3A",
                "mode_of_action": "Kontak (Knockdown)",
                "description": "Insektisida racun kontak yang bekerja sangat cepat (efek knockdown). Spektrum luas namun residu singkat.",
                "targets": ["Ulat Grayak", "Walang Sangit", "Kepik", "Lalat Buah", "Ulat Tanah"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 7,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Gunakan sore hari. Hati-hati menyebabkan resurgensi (ledakan hama) jika digunakan berlebihan pada wereng."
            },
            "dimehipo": {
                "id": "dimehipo",
                "name": "Dimehipo",
                "type": "Insektisida",
                "group": "Nereistoxin analogue",
                "irac_code": "14",
                "mode_of_action": "Sistemik, Kontak & Lambung",
                "description": "Insektisida sistemik yang diserap tanaman. Efektif untuk hama penggerek dan pengisap.",
                "targets": ["Penggerek Batang Padi", "Wereng", "Hama Putih Palsu"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 14,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Dapat dicampur dengan insektisida lain untuk memperluas spektrum."
            },
            "diafentiuron": {
                "id": "diafentiuron",
                "name": "Diafentiuron",
                "type": "Insektisida & Akarisida",
                "group": "Thiourea",
                "irac_code": "12A",
                "mode_of_action": "Kontak & Pernafasan",
                "description": "Menghambat sintesis ATP mitokondria. Efektif untuk hama yang resisten terhadap organofosfat dan piretroid.",
                "targets": ["Kutu Kebul", "Tungau", "Kutu Daun", "Ulat Daun Kubis"],
                "safety": {
                    "toxicity_class": "Biru (Cukup Berbahaya)",
                    "phi_days": 7,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Memerlukan sinar matahari untuk aktivasi (fotodegradasi menjadi bentuk aktif). Semprotkan pagi hari saat cerah."
            },
            "azadirachtin": {
                "id": "azadirachtin",
                "name": "Azadirachtin (Mimba)",
                "type": "Insektisida Nabati",
                "group": "Botanical",
                "irac_code": "UN (Unknown)",
                "mode_of_action": "Penghambat Makan & Tumbuh",
                "description": "Ekstrak biji mimba. Mengganggu hormon ecdysone (ganti kulit) dan bersifat antifeedant (penolak makan).",
                "targets": ["Ulat", "Kutu Daun", "Thrips", "Lalat Buah"],
                "safety": {
                    "toxicity_class": "Hijau (Aman)",
                    "phi_days": 0,
                    "signal_word": "AMAN"
                },
                "usage": "Aman untuk pertanian organik. Aplikasi sore hari untuk menghindari degradasi UV cepat."
            },

            # FUNGISIDA (FUNGICIDES)
            "mankozeb": {
                "id": "mankozeb",
                "name": "Mankozeb",
                "type": "Fungisida",
                "group": "Dithiocarbamate",
                "irac_code": "M3",
                "mode_of_action": "Kontak (Protektif)",
                "description": "Fungisida protektif multi-site yang membentuk lapisan pelindung pada permukaan daun. Mencegah spora jamur berkecambah.",
                "targets": ["Busuk Daun (Phytophthora)", "Bercak Daun", "Antraknosa", "Embun Bulu", "Karat Daun"],
                "safety": {
                    "toxicity_class": "Biru (Cukup Berbahaya)",
                    "phi_days": 7,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Aplikasi preventif sebelum gejala muncul. Tidak mudah resisten. Mengandung Mn dan Zn sebagai nutrisi mikro."
            },
            "azoksistrobin": {
                "id": "azoksistrobin",
                "name": "Azoksistrobin",
                "type": "Fungisida",
                "group": "Strobilurin",
                "irac_code": "11",
                "mode_of_action": "Sistemik & Translaminar",
                "description": "Menghambat respirasi mitokondria jamur. Memiliki efek 'greening' (menghijaukan daun) dan meningkatkan kualitas hasil.",
                "targets": ["Blas Padi", "Antraknosa", "Embun Tepung", "Bercak Ungu", "Bercak Coklat"],
                "safety": {
                    "toxicity_class": "Hijau (Cukup Aman)",
                    "phi_days": 3,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Gunakan maksimal 2 kali per musim untuk mencegah resistensi. Sering dicampur dengan Difenokonazol (Top)."
            },
            "difenokonazol": {
                "id": "difenokonazol",
                "name": "Difenokonazol",
                "type": "Fungisida",
                "group": "Triazol",
                "irac_code": "3",
                "mode_of_action": "Sistemik",
                "description": "Menghambat biosintesis ergosterol pada dinding sel jamur. Efektif menyembuhkan (kuratif) dan melindungi.",
                "targets": ["Bercak Daun", "Blas Padi", "Busuk Batang", "Karat Daun", "Bercak Ungu"],
                "safety": {
                    "toxicity_class": "Biru (Cukup Berbahaya)",
                    "phi_days": 14,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Sangat kuat sebagai kuratif. Dapat menghambat pertumbuhan tanaman (stunting) jika dosis berlebih pada fase muda."
            },
            "klorotalonil": {
                "id": "klorotalonil",
                "name": "Klorotalonil",
                "type": "Fungisida",
                "group": "Chloronitrile",
                "irac_code": "M5",
                "mode_of_action": "Kontak",
                "description": "Fungisida kontak berspektrum luas. Tahan tercuci air hujan (rainfastness baik).",
                "targets": ["Busuk Daun", "Antraknosa", "Bercak Daun Alternaria", "Embun Bulu"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 7,
                    "signal_word": "BERBAHAYA"
                },
                "usage": "Bagus untuk musim hujan karena daya lekat kuat. Aplikasi interval 7 hari."
            },
            "propineb": {
                "id": "propineb",
                "name": "Propineb",
                "type": "Fungisida",
                "group": "Dithiocarbamate",
                "irac_code": "M3",
                "mode_of_action": "Kontak",
                "description": "Fungisida kontak yang mengandung Zinc (Seng) tinggi, baik untuk pertumbuhan tanaman.",
                "targets": ["Bercak Daun", "Busuk Daun", "Antraknosa", "Embun Bulu"],
                "safety": {
                    "toxicity_class": "Biru (Cukup Berbahaya)",
                    "phi_days": 7,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Aplikasi preventif. Membantu menghijaukan daun karena kandungan Zn."
            },
            "benomil": {
                "id": "benomil",
                "name": "Benomil",
                "type": "Fungisida",
                "group": "Benzimidazole",
                "irac_code": "1",
                "mode_of_action": "Sistemik",
                "description": "Fungisida sistemik kuratif dan protektif. Menghambat pembelahan sel jamur.",
                "targets": ["Antraknosa", "Layu Fusarium", "Bercak Daun", "Busuk Buah"],
                "safety": {
                    "toxicity_class": "Biru (Cukup Berbahaya)",
                    "phi_days": 14,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Rawan resistensi, jangan gunakan terus menerus. Efektif untuk perlakuan benih."
            },

            # HERBISIDA (HERBICIDES)
            "glifosat": {
                "id": "glifosat",
                "name": "Glifosat",
                "type": "Herbisida",
                "group": "Glycine",
                "irac_code": "G (9)",
                "mode_of_action": "Sistemik Purna Tumbuh",
                "description": "Herbisida non-selektif yang mematikan seluruh bagian gulma sampai ke akar. Menghambat enzim EPSP synthase.",
                "targets": ["Alang-alang", "Teki", "Gulma Berdaun Lebar & Sempit Tahunan"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 14,
                    "signal_word": "BERBAHAYA"
                },
                "usage": "Jangan sampai mengenai tanaman utama. Butuh waktu 7-10 hari untuk gulma mati total (sistemik lambat)."
            },
            "parakuat": {
                "id": "parakuat",
                "name": "Parakuat Diklorida",
                "type": "Herbisida",
                "group": "Bipyridylium",
                "irac_code": "D (22)",
                "mode_of_action": "Kontak Purna Tumbuh",
                "description": "Herbisida kontak yang membakar bagian hijau gulma dengan cepat (gosong).",
                "targets": ["Gulma Berdaun Lebar", "Pakis", "Gulma Sempit"],
                "safety": {
                    "toxicity_class": "Merah (Sangat Berbahaya)",
                    "phi_days": 1,
                    "signal_word": "SANGAT BERACUN"
                },
                "usage": "Efek terlihat dalam hitungan jam. Tidak mematikan akar tanaman keras. Hati-hati, sangat beracun bagi manusia (dilarang di beberapa negara)."
            },
            "24d": {
                "id": "24d",
                "name": "2,4-D",
                "type": "Herbisida",
                "group": "Phenoxy-carboxylate",
                "irac_code": "O (4)",
                "mode_of_action": "Sistemik Selektif",
                "description": "Herbisida selektif untuk gulma berdaun lebar. Aman bagi tanaman rumput-rumputan (Padi, Jagung, Tebu).",
                "targets": ["Gulma Berdaun Lebar", "Eceng Gondok", "Genjer", "Kangkung Liar"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 14,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Gunakan pada tanaman padi/jagung untuk mengendalikan gulma daun lebar. Jangan gunakan dekat tanaman sayuran (cabai/tomat) karena uapnya bisa merusak (drifting)."
            },

            # BAKTERISIDA (BACTERICIDES)
            "tembaga_hidroksida": {
                "id": "tembaga_hidroksida",
                "name": "Tembaga Hidroksida",
                "type": "Bakterisida & Fungisida",
                "group": "Inorganik",
                "irac_code": "M1",
                "mode_of_action": "Kontak",
                "description": "Bahan aktif tembaga yang efektif melawan bakteri dan jamur. Ion tembaga merusak enzim sel patogen.",
                "targets": ["Hawar Daun Bakteri (Kresek)", "Busuk Buah", "Antraknosa", "Busuk Lunak"],
                "safety": {
                    "toxicity_class": "Biru (Cukup Berbahaya)",
                    "phi_days": 7,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Jangan campur dengan insektisida asam kuat. Bisa menyebabkan fitotoksik pada bunga/pupus muda."
            },
            "streptomisin": {
                "id": "streptomisin",
                "name": "Streptomisin Sulfat",
                "type": "Bakterisida",
                "group": "Antibiotik",
                "irac_code": "25",
                "mode_of_action": "Sistemik",
                "description": "Antibiotik pertanian untuk mengendalikan penyakit bakteri. Menghambat sintesis protein bakteri.",
                "targets": ["Hawar Daun Bakteri (Kresek)", "Layu Bakteri", "Busuk Basah"],
                "safety": {
                    "toxicity_class": "Kuning (Berbahaya)",
                    "phi_days": 14,
                    "signal_word": "PERHATIAN"
                },
                "usage": "Gunakan secara bijak untuk mencegah resistensi bakteri. Sering dikombinasikan dengan Oksitetrasiklin."
            }
        }
