"""Comprehensive pest and disease database for AgriSensa.

Version: 2.0 - Updated with complete pest/disease data
Last updated: 2025-11-24
"""


class PestDiseaseDatabase:
    """Comprehensive pest and disease information with prevention strategies."""
    


    


    @staticmethod
    def get_all_pests():
        """Return full pest and disease dictionary (sample entries)."""
        return {
# Duplicated pest data removed; use get_all_pests method
            "ulat_grayak": {
                "name": "Ulat Grayak (Spodoptera litura / S. frugiperda)",
                "type": "pest",
                "icon": "🐛",
                "category": "Hama Pemakan Daun",
                "target_crops": ["Cabai", "Bawang", "Tomat", "Jagung", "Kedelai", "Padi"],
                "symptoms": [
                    "Daun berlubang tidak beraturan, transparan (jendela) pada serangan awal",
                    "Serangan berat: daun habis tersisa tulang daun",
                    "Larva aktif makan pada malam hari",
                    "Kotoran larva di sekitar tanaman",
                    "Pucuk tanaman putus (pada jagung)"
                ],
                "damage": "Defoliasi berat, kegagalan panen, kerusakan tongkol jagung",
                "control_methods": {
                    "cultural": [
                        "Sanitasi gulma inang di sekitar lahan",
                        "Pengolahan tanah intensif untuk mematikan pupa",
                        "Tanam serentak",
                        "Rotasi tanaman bukan inang"
                    ],
                    "mechanical": [
                        "Kumpulkan dan musnahkan kelompok telur dan larva",
                        "Pasang perangkap feromon (Exi/Sexava) 16-24 buah/ha",
                        "Pasang light trap"
                    ],
                    "biological": [
                        "SlNPV (Spodoptera litura Nuclear Polyhedrosis Virus)",
                        "Bacillus thuringiensis (Bt) strain aizawai/kurstaki",
                        "Musuh alami: Trichogramma spp., Telenomus spp."
                    ],
                    "chemical": [
                        "Emamektin benzoat (IRAC Grup 6)",
                        "Klorantraniliprol (Grup 28)",
                        "Spinetoram (Grup 5)",
                        "Indoksakarb (Grup 22A)",
                        "Rotasi bahan aktif untuk cegah resistensi"
                    ]
                },
                "prevention": [
                    "Monitor rutin keberadaan kelompok telur",
                    "Jaga kebersihan lahan",
                    "Hindari tanam bertahap di satu hamparan",
                    "Pemanfaatan tanaman refugia untuk musuh alami"
                ],
                "lifecycle": "20-30 hari, sangat cepat berkembang biak",
                "economic_threshold": "1 kelompok telur/10 tanaman atau kerusakan daun >12.5%"
            },

            "ulat_tanah": {
                "name": "Ulat Tanah (Agrotis ipsilon)",
                "type": "pest",
                "icon": "🐛",
                "category": "Hama Bibit/Tanah",
                "target_crops": ["Cabai", "Tomat", "Jagung", "Sayuran Daun"],
                "symptoms": [
                    "Batang tanaman muda terpotong di pangkal",
                    "Tanaman layu dan roboh tiba-tiba",
                    "Larva bersembunyi di dalam tanah sekitar batang pada siang hari",
                    "Aktif memotong pada malam hari"
                ],
                "damage": "Kematian tanaman muda (bibit) di lapangan, penyulaman tinggi",
                "control_methods": {
                    "cultural": [
                        "Pengolahan tanah sempurna, jemur tanah",
                        "Bersihkan gulma sebelum tanam",
                        "Tanam serentak"
                    ],
                    "mechanical": [
                        "Cari dan bunuh larva di sekitar tanaman yang terpotong (pagi hari)",
                        "Pasang perangkap umpan (dedak + insektisida)"
                    ],
                    "biological": [
                        "Bacillus thuringiensis (Bt)",
                        "Nematoda entomopatogen (Steinernema spp.)",
                        "Musuh alami: Botrytis sp. (jamur)"
                    ],
                    "chemical": [
                        "Perlakuan benih/bibit",
                        "Aplikasi insektisida butiran (Karbofuran) di lubang tanam (hati-hati)",
                        "Semprot pangkal batang: Klorpirifos (jika diizinkan) atau Deltametrin (sore hari)"
                    ]
                },
                "prevention": [
                    "Olah tanah baik untuk memutus siklus",
                    "Jaga kebersihan lahan dari gulma",
                    "Pasang penghalang plastik di pangkal batang (untuk skala kecil)"
                ],
                "lifecycle": "30-45 hari",
                "economic_threshold": "5% tanaman terpotong"
            },

            "wereng_coklat": {
                "name": "Wereng Coklat (Nilaparvata lugens)",
                "type": "pest",
                "icon": "🦗",
                "category": "Hama Pengisap",
                "target_crops": ["Padi"],
                "symptoms": [
                    "Daun menguning dari ujung dan mengering (hopperburn)",
                    "Tanaman kerdil dan tidak berbuah",
                    "Terdapat serangga kecil coklat di pangkal batang",
                    "Serangan berat menyebabkan tanaman roboh"
                ],
                "damage": "Menghisap cairan tanaman dan menularkan virus tungro/kerdil",
                "control_methods": {
                    "cultural": [
                        "Penanaman serentak dalam 2 minggu untuk memutus siklus",
                        "Gunakan varietas tahan (Ciherang, Mekongga, Inpari 32)",
                        "Pengairan berselang (intermittent) untuk mengurangi kelembaban",
                        "Pemupukan berimbang, hindari N berlebihan"
                    ],
                    "mechanical": [
                        "Gunakan jaring/kain kasa pada saat migrasi wereng",
                        "Pasang lampu perangkap malam hari"
                    ],
                    "biological": [
                        "Lestarikan predator alami: laba-laba, kepik, kumbang carabid",
                        "Aplikasi Beauveria bassiana atau Metarhizium anisopliae"
                    ],
                    "chemical": [
                        "Minggu 1-3: Imidakloprid (sistemik, IRAC Grup 4A)",
                        "Minggu 4-6: Buprofezin (perusak pergantian kulit, IRAC Grup 16)",
                        "Darurat: Pimet rozin atau Sihalotrin (kontak cepat)"
                    ]
                },
                "prevention": [
                    "Tanam varietas tahan wereng bersertifikat",
                    "Hindari pemupukan Urea berlebihan (maksimal 250 kg/ha/musim)",
                    "Jaga kebersihan pematang dari gulma inang",
                    "Monitor populasi sejak fase vegetatif awal",
                    "Gunakan padi varietas berbeda secara rotasi untuk menghindari adaptasi hama"
                ],
                "lifecycle": "21-30 hari dari telur hingga dewasa. Puncak populasi pada fase bunting-berbunga padi.",
                "economic_threshold": "2-5 ekor per rumpun pada fase vegetatif; 10 ekor per rumpun pada fase generatif"
            },
            
            "penggerek_batang": {
                "name": "Penggerek Batang Padi (Scirpophaga spp.)",
                "type": "pest",
                "icon": "🐛",
                "category": "Hama Perusak Batang",
                "target_crops": ["Padi"],
                "symptoms": [
                    "Sundep (dead heart): anakan mati dengan daun tengah mengering",
                    "Beluk (white head): malai putih kosong tidak berisi",
                    "Lubang gerek pada batang dengan bekas kotoran",
                    "Tanaman mudah rebah"
                ],
                "damage": "Larva menggerek batang dari dalam, merusak jaringan pengangkut",
                "control_methods": {
                    "cultural": [
                        "Pergiliran tanaman padi-palawija",
                        "Olah tanah sempurna untuk membunuh pupa di jerami",
                        "Kelola pengairan untuk menenggelamkan pupa",
                        "Pangkas padi ratun (hindari padi ratun sebagai inang)"
                    ],
                    "mechanical": [
                        "Petik dan bunuh kelompok telur di daun",
                        "Buang anakan sundep dan beluk, bakar atau benamkan dalam air",
                        "Pasang light trap (lampu TL + bak air) pada malam hari"
                    ],
                    "biological": [
                        "Trichogramma spp. (parasitoid telur): 100.000 ekor/ha setiap minggu",
                        "Beauveria bassiana untuk larva",
                        "Lestarikan predator: laba-laba, kepik, katak"
                    ],
                    "chemical": [
                        "Preventif sejak 14 HST: Karbofuran granul 17kg/ha",
                        "Semprot: Klorantraniliprol (sistemik, Grup 28) atau Fipronil (Grup 2B)",
                        "Rotasi dengan Sipermetrin (kontak, Grup 3)"
                    ]
                },
                "prevention": [
                    "Tanam varietas tahan: Memberamo, Ciherang, IR64",
                    "Hindari tanam terlalu rapat (gunakan jarak tanam 25x25 cm)",
                    "Aplikasi pemupukan seimbang",
                    "Sanitasi lahan: bakar jerami terinfeksi",
                    "Hindari penanaman berurutan (padi-padi) tanpa jeda"
                ],
                "lifecycle": "35-50 hari, dewasa aktif malam hari",
                "economic_threshold": "1-2 kelompok telur per m²; 5% sundep atau 10% beluk"
            },
            
            "thrips": {
                "name": "Thrips (Thrips tabaci, Frankliniella spp.)",
                "type": "pest",
                "icon": "🪲",
                "category": "Hama Pengisap & Vektor Virus",
                "target_crops": ["Cabai", "Bawang", "Tomat", "Mentimun"],
                "symptoms": [
                    "Daun muda keriting, kaku seperti kayu",
                    "Bercak perak atau perunggu di permukaan daun",
                    "Daun muda kerdil dan menggulung",
                    "Bunga dan pucuk rontok",
                    "Buah cacat (bekas gigitan berwarna keperakan)"
                ],
                "damage": "Mengisap cairan sel, menularkan Tomato Spotted Wilt Virus (TSWV) pada tomat dan cabai",
                "control_methods": {
                    "cultural": [
                        "Mulsa plastik perak untuk menolak thrips",
                        "Buang gulma sekitar pertanaman",
                        "Hindari penanaman tumpang sari yang meningkatkan kelembaban",
                        "Sanitasi: buang bagian tanaman terinfeksi virus"
                    ],
                    "mechanical": [
                        "Pasang perangkap kuning lengket (yellow sticky trap) 40 buah/ha",
                        "Kain kasa jaring insektisida (mesh 40) pada pembibitan",
                        "Penyemprotan air bertekanan untuk mengurangi populasi"
                    ],
                    "biological": [
                        "Predator alami: Orius spp., Amblyseius swirskii",
                        "Jamur entomopatogen: Beauveria bassiana, Metar hizium anisopliae",
                        "Nematoda: Steinernema feltiae"
                    ],
                    "chemical": [
                        "Minggu 1-3: Abamektin (translaminar, IRAC Grup 6) 0.5 ml/L",
                        "Minggu 4-6: Spinosad (sistemik terbatas, Grup 5) 0.5 ml/L",
                        "Minggu 7-9: Imidakloprid (sistemik, Grup 4A) 0.3 g/L",
                        "Rotasi dengan: Fipronil (Grup 2B) atau Diafentiuron (Grup 12A)"
                    ]
                },
                "prevention": [
                    "Tanam bibit sehat dan bebas thrips",
                    "Aplikasi mulsa plastik perak-hitam sejak awal",
                    "Isolasi pertanaman baru dari lahan lama (min 500 m)",
                    "Monitor dengan perangkap kuning sejak transplanting",
                    "Semprot preventif sejak 7 HST dengan insektisida rotasi",
                    "Karantina bibit baru selama 7-14 hari"
                ],
                "lifecycle": "14-21 hari, reproduksi cepat pada kondisi kering dan hangat (28-30°C)",
                "economic_threshold": "5-10 ekor per daun atau 2 thrips per bunga"
            },
            
            "lalat_buah": {
                "name": "Lalat Buah (Bactrocera spp.)",
                "type": "pest",
                "icon": "🪰",
                "category": "Hama Buah",
                "target_crops": ["Cabai", "Mangga", "Jambu", "Belimbing", "Tomat"],
                "symptoms": [
                    "Lubang kecil di permukaan buah (bekas tusukan ovipositor)",
                    "Buah busuk dan rontok prematur",
                    "Larva (belatung) di dalam daging buah",
                    "Bercak coklat di sekitar lubang tusukan"
                ],
                "damage": "Betina bertelur di dalam buah, larva memakan daging buah dari dalam",
                "control_methods": {
                    "cultural": [
                        "Panen buah tepat waktu (jangan terlalu masak di pohon)",
                        "Kumpulkan dan musnahkan buah jatuh/terserang setiap hari",
                        "Bersihkan gulma dan buah liar di sekitar",
                        "Pembrongsongan buah untuk cabai besar"
                    ],
                    "mechanical": [
                        "Perangkap Metil Eugenol (petrogenol) untuk jantan: 40  buah/ha",
                        "Perangkap protein: cairan gula + insektisida",
                        "Pembungkusan buah dengan plastik/kertas parapin"
                    ],
                    "biological": [
                        "Parasitoid: Fopius arisanus, Diachasmimorpha longicaudata",
                        "Predator: semut, kumbang, laba-laba",
                        "Jamur entomopatogen: Metarhizium anisopliae"
                    ],
                    "chemical": [
                        "Umpan beracun (protein + insektisida): Metomil atau Malation",
                        "Semprot preventif saat bunga mekar: Dimethoat (sistemik)",
                        "Rotasi: Sipermetrin (kontak) atau Abamektin"
                    ]
                },
                "prevention": [
                    "Pasang perangkap Metil Eugenol sejak bunga mekar",
                    "Sanitasi kebun: musnahkan buah busuk",
                    "Tanam tanaman perangkap di pinggir (singkong, labu)",
                    "Pembrongsongan buah sejak pentil (diameter 1-2 cm)",
                    "Hindari varietas yang terlalu rentan",
                    "Panen pagi hari saat lalat belum aktif"
                ],
                "lifecycle": "21-35 hari tergantung suhu. Puncak aktivitas pagi (7-10) dan sore (15-17)",
                "economic_threshold": "5% buah terserang"
            },
            
            # PENYAKIT JAMUR (FUNGAL DISEASES)
            "blas": {
                "name": "Blas Padi / Blast (Pyricularia oryzae)",
                "type": "disease",
                "icon": "🦠",
                "category": "Penyakit Jamur",
                "target_crops": ["Padi"],
                "symptoms": [
                    "Blas daun: bercak coklat berbentuk belah ketupat dengan tepi coklat tua dan tengah abu-abu",
                    "Blas leher: pangkal malai coklat kehitaman, malai tidak berisi",
                    "Blas buku: buku batang patah berwarna coklat kehitaman",
                    "Daun mengering dan tanaman rebah"
                ],
                "damage": "Kehilangan hasil 10-90% tergantung tingkat serangan dan stadium tanaman",
                "control_methods": {
                    "cultural": [
                        "Gunakan varietas tahan: Inpari 30, Inpari 32, Mekongga",
                        "Pergiliran varietas setiap 2-3 musim",
                        "Pemupukan berimbang (hindari N berlebihan pada fase vegetatif)",
                        "Pengaturan jarak tanam tidak terlalu rapat (25x25 cm)",
                        "Pengairan berselang untuk mengurangi kelembaban"
                    ],
                    "mechanical": [
                        "Buang bagian tanaman terinfeksi",
                        "Bakar jerami terinfeksi setelah panen",
                        "Olah tanah sempurna"
                    ],
                    "biological": [
                        "Bakteri antagonis: Pseudomonas fluorescens",
                        "Jamur antagonis: Trichoderma spp.",
                        "Aplikasi agens hayati sejak persemaian"
                    ],
                    "chemical": [
                        "Preventif (14-21 HST): Mankozeb (kontak, FRAC M3) 2 g/L",
                        "Kuratif: Trisiklazol (sistemik, FRAC I1) 0.6 g/L",
                        "Rotasi: Azoksistrobin (FRAC 11) atau Difenokonazol (FRAC 3)",
                        "Aplikasi setiap 7-10 hari saat kondisi lembab"
                    ]
                },
                "prevention": [
                    "Tanam benih/bibit sehat bersertifikat",
                    "Perlakuan benih dengan Mankozeb atau Trichoderma sebelum semai",
                    "Hindari pemupukan N tinggi di atas 200 kg Urea/ha",
                    "Jaga sirkulasi udara dengan jarak tanam optimal",
                    "Monitoring rutin terutama saat kelembaban tinggi (>85%)",
                    "Aplikasi fungisida preventif saat musim hujan"
                ],
                "favorable_conditions": "Kelembaban >85%, suhu 25-28°C, embun pagi berlimpah",
                "peak_season": "Musim hujan, terutama bulan Desember - Maret"
            },

            "blast_padi": {
                "name": "Blas Padi / Blast (Pyricularia oryzae)",
                "type": "disease",
                "icon": "🦠",
                "category": "Penyakit Jamur",
                "target_crops": ["Padi"],
                "symptoms": [
                    "Blas daun: bercak coklat berbentuk belah ketupat dengan tepi coklat tua dan tengah abu-abu",
                    "Blas leher: pangkal malai coklat kehitaman, malai tidak berisi",
                    "Blas buku: buku batang patah berwarna coklat kehitaman",
                    "Daun mengering dan tanaman rebah"
                ],
                "damage": "Kehilangan hasil 10-90% tergantung tingkat serangan dan stadium tanaman",
                "control_methods": {
                    "cultural": [
                        "Gunakan varietas tahan: Inpari 30, Inpari 32, Mekongga",
                        "Pergiliran varietas setiap 2-3 musim",
                        "Pemupukan berimbang (hindari N berlebihan pada fase vegetatif)",
                        "Pengaturan jarak tanam tidak terlalu rapat (25x25 cm)",
                        "Pengairan berselang untuk mengurangi kelembaban"
                    ],
                    "mechanical": [
                        "Buang bagian tanaman terinfeksi",
                        "Bakar jerami terinfeksi setelah panen",
                        "Olah tanah sempurna"
                    ],
                    "biological": [
                        "Bakteri antagonis: Pseudomonas fluorescens",
                        "Jamur antagonis: Trichoderma spp.",
                        "Aplikasi agens hayati sejak persemaian"
                    ],
                    "chemical": [
                        "Preventif (14-21 HST): Mankozeb (kontak, FRAC M3) 2 g/L",
                        "Kuratif: Trisiklazol (sistemik, FRAC I1) 0.6 g/L",
                        "Rotasi: Azoksistrobin (FRAC 11) atau Difenokonazol (FRAC 3)",
                        "Aplikasi setiap 7-10 hari saat kondisi lembab"
                    ]
                },
                "prevention": [
                    "Tanam benih/bibit sehat bersertifikat",
                    "Perlakuan benih dengan Mankozeb atau Trichoderma sebelum semai",
                    "Hindari pemupukan N tinggi di atas 200 kg Urea/ha",
                    "Jaga sirkulasi udara dengan jarak tanam optimal",
                    "Monitoring rutin terutama saat kelembaban tinggi (>85%)",
                    "Aplikasi fungisida preventif saat musim hujan"
                ],
                "favorable_conditions": "Kelembaban >85%, suhu 25-28°C, embun pagi berlimpah",
                "peak_season": "Musim hujan, terutama bulan Desember - Maret"
            },
            
            "antraknosa": {
                "name": "Antraknosa / Anthracnose (Colletotrichum spp.)",
                "type": "disease",
                "icon": "🍂",
                "category": "Penyakit Jamur",
                "target_crops": ["Cabai", "Tomat", "Mangga", "Pepaya", "Alpukat"],
                "symptoms": [
                    "Bercak cekung berwarna coklat kehitaman pada buah masak",
                    "Bercak basah dan membusuk dengan bintik hitam (konidium jamur)",
                    "Daun: bercak coklat dengan lingkaran konsentris",
                    "Buah rontok prematur"
                ],
                "damage": "Busuk buah pasca panen, kerugian hingga 30-60%",
                "control_methods": {
                    "cultural": [
                        "Panen buah tepat waktu (jangan terlalu masak di pohon)",
                        "Hindari luka mekanis saat panen dan pengemasan",
                        "Kurangi kelembaban dengan jarak tanam optimal",
                        "Sanitasi: buang buah/daun terinfeksi",
                        "Drainase baik untuk mengurangi kelembaban tanah"
                    ],
                    "mechanical": [
                        "Cuci buah dengan air bersih setelah panen",
                        "Rendam air panas 50-52°C selama 5 menit (untuk buah tertentu)",
                        "Simpan pada suhu rendah 10-13°C"
                    ],
                    "biological": [
                        "Bakteri antagonis: Bacillus subtilis",
                        "Jamur antagonis: Trichoderma harzianum",
                        "Aplikasi pada bunga dan buah muda"
                    ],
                    "chemical": [
                        "Preventif: Mankozeb (kontak, FRAC M3) 2 g/L setiap 7 hari",
                        "Kuratif: Difenokonazol atau Propineb (FRAC 3) 1 ml/L",
                        "Rotasi: Klorotalonil (FRAC M5) atau Azoksistrobin (FRAC 11)",
                        "Pasca panen: Benomil atau Prochloraz"
                    ]
                },
                "prevention": [
                    "Tanam varietas tahan (untuk cabai: Lado, Hot Beauty)",
                    "Aplikasi fungisida preventif sejak bunga mekar",
                    "Mulsa plastik untuk mengurangi percikan air hujan",
                    "Pemupukan K dan Ca cukup untuk ketahanan kulit buah",
                    "Hindari penyiraman overhead saat berbuah",
                    "Pemangkasan untuk sirkulasi udara",
                    "Panen dengan alat bersih dan steril"
                ],
                "favorable_conditions": "Kelembaban >80%, suhu 25-30°C, hujan deras, embun berat",
                "peak_season": "Musim hujan dan transisi hujan-kemarau"
            },
            
            "busuk_daun": {
                "name": "Busuk Daun / Late Blight (Phytophthora infestans)",
                "type": "disease",
                "icon": "🍂",
                "category": "Penyakit Jamur (Oomycetes)",
                "target_crops": ["Tomat", "Kentang", "Cabai"],
                "symptoms": [
                    "Bercak basah kehitaman di tepi atau ujung daun",
                    "Bercak meluas cepat, daun mengering seperti terbakar",
                    "Bulu halus putih (miselium) di permukaan bawah daun saat lembab",
                    "Batang dan buah juga membusuk basah"
                ],
                "damage": "Kematian tanaman sangat cepat (2-3 hari) pada kondisi lembab, gagal panen total",
                "control_methods": {
                    "cultural": [
                        "Hindari kelembaban tinggi, jarak tanam lebar",
                        "Gunakan naungan plastik (greenhouse) saat musim hujan",
                        "Sanitasi: buang daun/buah sakit segera",
                        "Hindari irigasi curah (sprinkler)",
                        "Rotasi tanaman non-solanaceae"
                    ],
                    "mechanical": [
                        "Pangkas daun bawah untuk sirkulasi udara",
                        "Pasang mulsa plastik perak-hitam",
                        "Eradikasi tanaman sakit parah"
                    ],
                    "biological": [
                        "Trichoderma harzianum aplikasi tanah",
                        "Pseudomonas fluorescens aplikasi foliar",
                        "Ekstrak bawang putih (fungisida nabati)"
                    ],
                    "chemical": [
                        "Preventif: Mankozeb (FRAC M3) atau Klorotalonil (M5)",
                        "Kuratif: Simoksanil (FRAC 27) + Mankozeb",
                        "Sistemik: Dimetomorf (FRAC 40) atau Propamokarb (FRAC 28)",
                        "Rotasi ketat, aplikasi 3-5 hari sekali saat hujan"
                    ]
                },
                "prevention": [
                    "Tanam varietas toleran (Golden, Permata)",
                    "Aplikasi fungisida kontak preventif sebelum hujan",
                    "Jaga drainase lahan agar tidak becek",
                    "Monitoring harian saat cuaca mendung/hujan",
                    "Karantina bibit baru"
                ],
                "favorable_conditions": "Suhu sejuk 18-22°C, kelembaban >90%, hujan/kabut",
                "peak_season": "Musim hujan terus-menerus"
            },

            "hawar_daun_bakteri": {
                "name": "Hawar Daun Bakteri / BLB (Xanthomonas oryzae pv. oryzae)",
                "type": "disease",
                "icon": "🦠",
                "category": "Penyakit Bakteri",
                "target_crops": ["Padi"],
                "symptoms": [
                    "Garis kuning kehijauan di tepi daun yang membesar dan memanjang",
                    "Berubah menjadi garis coklat sampai ujung daun",
                    "Daun mengering dari ujung ke pangkal",
                    "Serangan berat: seluruh daun mengering",
                    "Eksudasi bakteri: lendir berwarna kuning keputihan di pagi hari"
                ],
                "damage": "Penurunan hasil 20-80% tergantung stadi um serangan",
                "control_methods": {
                    "cultural": [
                        "Gunakan varietas tahan: TN1, Inpari 13, Ciherang",
                        "Pergiliran varietas untuk menghindari adaptasi patogen",
                        "Perlakuan benih dengan bakterisida atau air panas 52-54°C, 15 menit",
                        "Pemupukan berimbang (hindari N berlebihan)",
                        "Pengairan terputus untuk mengurangi kelembaban",
                        "Olah tanah sempurna untuk menguburkan jerami terinfeksi"
                    ],
                    "mechanical": [
                        "Buang dan bakar bagian tanaman terinfeksi",
                        "Sanitasi alat pertanian",
                        "Hindari luka pada daun saat pemupukan/penyemprotan"
                    ],
                    "biological": [
                        "Bakteriofag: virus pemakan bakteri Xanthomonas",
                        "Bakteri antagonis: Pseudomonas fluorescens, Bacillus spp.",
                        "Aplikasi saat awal gejala"
                    ],
                    "chemical": [
                        "Bakterisida tembaga: Copper hydroxide atau Copper oxychloride 2-3 g/L",
                        "Antibiotik: Oksitetrasiklin atau Streptomisin sulfat (terbatas)",
                        "Aplikasi setiap 7 hari saat kondisi lembab tinggi"
                    ]
                },
                "prevention": [
                    "Tanam benih bersertifikat bebas penyakit",
                    "Perlakuan benih sebelum semai",
                    "Hindari kerusakan mekanis pada daun",
                    "Jaga kebersihan pematang dari gulma",
                    "Hindari pengairan terus-menerus (gunakan macak-macak)",
                    "Pemupukan N tidak berlebihan",
                    "Monitoring sejak fase vegetatif awal"
                ],
                "favorable_conditions": "Kelembaban >80%, suhu 25-34°C, angin kencang, luka pada daun",
                "peak_season": "Musim hujan dengan angin kencang, fase anakan maksimum"
            },
            
            "layu_fusarium": {
                "name": "Layu Fusarium (Fusarium oxysporum)",
                "type": "disease",
                "icon": "🥀",
                "category": "Penyakit Jamur Tanah",
                "target_crops": ["Tomat", "Cabai", "Terung", "Pisang", "Semangka"],
                "symptoms": [
                    "Daun layu pada siang hari, segar pada pagi/malam (stadium awal)",
                   "Layu permanen, daun menguning dari bawah ke atas",
                    "Batang dipotong: pembuluh kayu berwarna coklat",
                    "Tanaman mati dalam 7-14 hari setelah gejala muncul"
                ],
                "damage": "Kematian tanaman 10-100%, terutama pada lahan dengan riwayat penyakit",
                "control_methods": {
                    "cultural": [
                        "Rotasi tanaman dengan non-host (jagung, padi) selama 2-3 tahun",
                        "Gunakan varietas tahan (untuk tomat: Permata, Chung, Fortuna)",
                        "Solarisasi tanah: tutup dengan plastik transparan 4-6 minggu",
                        "Pengapuran: Dolomit 1-2 ton/ha untuk pH 6.5-7.0",
                        "Buat bedengan tinggi untuk drainase optimal",
                        "Hindari genangan air"
                    ],
                    "mechanical": [
                        "Cabut dan musnahkan tanaman terinfeksi (bakar, jangan kompos)",
                        "Sterilisasi alat pertanian dengan disinfektan",
                        "Gunakan mulsa plastik untuk mencegah percikan tanah"
                    ],
                    "biological": [
                        "Trichoderma spp.: 20-50 g/tanaman saat tanam atau kocor",
                        "Pseudomonas fluorescens: rendam akar bibit sebelum tanam",
                        "Bacillus subtilis: aplikasi ke lubang tanam",
                        "Mikoriza: meningkatkan ketahanan tanaman"
                    ],
                    "chemical": [
                        "Perlakuan tanah: Benomil, Karbendazim, atau Metalaksil",
                        "Sistemik: Fosetil-Al atau Propamokarb 2-3 ml/L (kocor)",
                        "Aplikasi 2-3 kali dengan interval 7-10 hari"
                    ]
                },
                "prevention": [
                    "Gunakan bibit sehat dan media tanam steril",
                    "Perlakuan bibit dengan Trichoderma sebelum tanam",
                    "Tanam pada lahan bebas riwayat penyakit atau setelah rotasi",
                    "Solarisasi tanah sebelum tanam",
                    "Drainase baik dan hindari over-irrigation",
                    "Pemupukan berimbang dengan K dan Ca cukup",
                    "Monitoring dan roguing (cabut) tanaman sakit sejak dini"
                ],
                "favorable_conditions": "Suhu 25-30°C, pH tanah asam (4.5-6.0), kelembaban tanah tinggi",
                "peak_season": "Sepanjang tahun, terutama pada lahan bekas solanaceae"
            },
            
            "virus_kuning_cabai": {
                "name": "Virus Kuning Cabai / Gemini Virus (Begomovirus)",
                "type": "disease",
                "icon": "🦟",
                "category": "Penyakit Virus",
                "target_crops": ["Cabai", "Tomat"],
                "symptoms": [
                    "Daun muda menguning total atau berbercak kuning",
                    "Daun menggulung ke atas, menebal dan kaku",
                    "Tanaman kerdil, internodus memendek",
                    "Bunga rontok, buah tidak terbentuk atau kecil",
                    "Pertumbuhan terhambat total"
                ],
                "damage": "Kehilangan hasil hingga 100% jika terinfeksi sejak muda",
                "control_methods": {
                    "cultural": [
                        "Gunakan varietas toleran: Laris, Tit Super, Hot Beauty",
                        "Eradikasi tanaman sakit sejak awal (< 14 HST)",
                        "Hindari penanaman cabai berurutan tanpa jeda",
                        "Pembibitan dalam screen house (kasa mesh 40)",
                        "Isolasi pertanaman baru min 500 m dari lahan lama",
                        "Buang gulma inang virus (solanaceae liar)"
                    ],
                    "mechanical": [
                        "Pasang mulsa plastik perak untuk menolak kutu kebul",
                        "Pasang perangkap kuning lengket 40-60 buah/ha",
                        "Screen house untuk pembibitan",
                        "Karantina bibit 7-14 hari sebelum tanam"
                    ],
                    "biological": [
                        "Predator kutu kebul: Encarsia formosa (parasitoid), Orius spp.",
                        "Jamur entomopatogen: Beauveria bassiana, Verticillium lecanii",
                        "Aplikasi sejak awal pertanaman"
                    ],
                    "chemical": [
                        "Pengendalian vektor (kutu kebul/whitefly):",
                        "Sistemik: Imidakloprid 0.3 g/L atau Tiametoksam 0.2 g/L",
                        "Kontak: Spinosad 0.5 ml/L atau Piridaben 1.5 ml/L",
                        "Rotasi 3 kelompok IRAC berbeda",
                        "Semprot rutin 3-5 hari sekali hingga 60 HST",
                        "Tidak ada insektisida untuk virus, fokus pada vektor"
                    ]
                },
                "prevention": [
                    "Tanam bibit sehat dengan sertifikat bebas virus",
                    "Aplikasi mulsa perak sejak tanam",
                    "Semprot imidakloprid preventif sejak 7 HST",
                    "Monitoring kutu kebul dengan perangkap kuning",
                    "Roguing tanaman sakit <20% serangan; jika >20% bongkar total",
                    "Sanitasi purnatanam: bongkar semua tanaman, biarkan lahan bera 4-6 minggu",
                    "Hindari penanaman solanaceae (tomat, terung) di sekitar"
                ],
                "favorable_conditions": "Suhu tinggi 28-35°C, kondisi kering, populasi kutu kebul tinggi",
                "peak_season": "Musim kemarau (April-Oktober), terutama puncak kemarau Juli-Agustus"
            },
            
            # HAMA HORTIKULTURA TAMBAHAN
            "kutu_daun": {
                "name": "Kutu Daun / Aphids (Aphis gossypii, Myzus persicae)",
                "type": "pest",
                "icon": "🐜",
                "category": "Hama Pengisap & Vektor Virus",
                "target_crops": ["Cabai", "Tomat", "Sawi", "Selada", "Kacang Panjang", "Mawar", "Krisan"],
                "symptoms": [
                    "Koloni kutu daun (hijau, hitam, atau kuning) di pucuk dan daun muda",
                    "Daun keriting dan menggulung ke bawah",
                    "Embun jelaga (lapisan hitam) dari kotoran kutu (honeydew)",
                    "Pertumbuhan terhambat, tanaman kerdil",
                    "Daun menguning dan layu"
                ],
                "damage": "Menghisap cairan tanaman, menularkan virus mosaik, layu, dan kerdil",
                "control_methods": {
                    "cultural": [
                        "Tanam varietas toleran",
                        "Buang gulma inang kutu daun",
                        "Hindari pemupukan N berlebihan yang memacu pucuk lunak",
                        "Rotasi tanaman dengan non-host (rumput-rumputan)",
                        "Jaring anti serangga pada pembibitan"
                    ],
                    "mechanical": [
                        "Semprot air bertekanan untuk mengurangi populasi",
                        "Pasang perangkap kuning lengket 30-40 buah/ha",
                        "Pemotongan dan pemusnahan bagian terserang berat",
                        "Kain kasa mesh 40 pada screen house"
                    ],
                    "biological": [
                        "Predator: Coccinellidae (kepik), Chrysopa (lacewing), Syrphidae (lalat kembang)",
                        "Parasitoid: Aphidius colemani, Aphidius ervi",
                        "Jamur: Verticillium lecanii, Beauveria bassiana",
                        "Aplikasi Neem oil (azadirachtin) 3-5 ml/L"
                    ],
                    "chemical": [
                        "Sistemik: Imidakloprid 0.25 g/L atau Tiametoksam 0.2 g/L",
                        "Kontak: Pirimikarb (selektif kutu daun, IRAC 1A) 0.5 g/L",
                        "Rotasi: Spirotetramat (IRAC 23) atau Flonikamid (Grup 9C)",
                        "Aplikasi setiap 5-7 hari saat populasi tinggi"
                    ]
                },
                "prevention": [
                    "Monitoring rutin sejak fase vegetatif awal",
                    "Pasang perangkap kuning untuk deteksi dini",
                    "Hindari penanaman terlalu rapat",
                    "Lestarikan musuh alami (jangan semprot insektisida broad-spectrum)",
                    "Aplikasi Neem oil preventif setiap 10 hari",
                    "Karantina tanaman baru 7-14 hari"
                ],
                "lifecycle": "7-14 hari, reproduksi parthenogenesis (tanpa kawin) sangat cepat",
                "economic_threshold": "10-20 kutu/daun pada fase vegetatif; 5 kutu/daun pada berbunga",
                "favorable_conditions": "Suhu 20-27°C, kelembaban sedang, pucuk muda berlimpah",
                "peak_season": "Musim kemarau dan transisi kemarau-hujan"
            },
            
            "penggerek_daun": {
                "name": "Penggerek Daun / Leaf Miner (Liriomyza spp.)",
                "type": "pest",
                "icon": "🪱",
                "category": "Hama Perusak Daun",
                "target_crops": ["Tomat", "Terung", "Mentimun", "Kangkung", "Bayam", "Selada", "Krisan"],
                "symptoms": [
                    "Terowongan berkelok-kelok berwarna putih di permukaan daun",
                    "Bintik tusukan kecil  di daun (bekas ovipositor betina)",
                    "Daun berlubang dan menguning",
                    "Produktivitas fotosintesis menurun",
                    "Serangan berat: seluruh daun rusak"
                ],
                "damage": "Larva menggerek daun dari dalam, merusak jaringan mesofil",
                "control_methods": {
                    "cultural": [
                        "Rotasi tanaman dengan monocot (jagung, padi)",
                        "Buang dan musnahkan daun terserang",
                        "Hindari penanaman  terus-menerus tanpa jeda",
                        "Panen sisa tanaman dan musnahkan",
                        "Sanitasi gulma inang"
                    ],
                    "mechanical": [
                        "Petik dan hancurkan daun berliang setiap hari",
                        "Pasang perangkap kuning lengket 40-60 buah/ha",
                        "Jaring serangga mesh 25 pada screen house",
                        "Pemotongan daun terserang berat"
                    ],
                    "biological": [
                        "Parasitoid: Diglyphus isaea, Dacnusa sibirica, Opius spp.",
                        "Nematoda entomopatogen: Steinernema feltiae",
                        "Jamur: Beauveria bassiana aplikasi foliar",
                        "Pelepasan parasitoid 1000-2000 ekor/ha/minggu"
                    ],
                    "chemical": [
                        "Sistemik translaminar: Abamektin 0.5-0.75 ml/L (IRAC Grup 6)",
                        "Cyromazine (penghambat kitin, Grup 17) 0.4 g/L",
                        "Spinosad 0.5 ml/L (Grup 5) efektif pada larva",
                        "Rotasi 3 kelompok IRAC, aplikasi 5-7 hari"
                    ]
                },
                "prevention": [
                    "Screen house untuk pembibitan",
                    "Monitor dengan perangkap kuning sejak tanam",
                    "Aplikasi preventif Azadirachtin (Neem) 3 ml/L",
                    "Hindari lahan bekas solanaceae atau cucurbitaceae",
                    "Lestarikan parasitoid dengan mengurangi insektisida broad-spectrum",
                    "Jeda tanam minimal 2-3 minggu"
                ],
                "lifecycle": "14-21 hari dari telur hingga dewasa, bisa 10-15 generasi/tahun",
                "economic_threshold": "30% daun terliang atau 2-3 liang baru/daun/minggu",
                "favorable_conditions": "Suhu 25-30°C, kelembaban sedang, daun muda berlimpah",
                "peak_season": "Sepanjang tahun, puncak saat musim kemarau"
            },
            
            "embun_tepung": {
                "name": "Embun Tepung / Powdery Mildew (Oidium spp., Erysiphe spp.)",
                "type": "disease",
                "icon": "☁️",
                "category": "Penyakit Jamur",
                "target_crops": ["Mentimun", "Melon", "Semangka", "Labu", "Terung", "Mawar", "Krisan", "Stroberi"],
                "symptoms": [
                    "Bercak putih seperti bedak/tepung di permukaan daun",
                    "Mulai dari bawah, menyebar ke daun atas",
                    "Daun menguning, mengering, dan rontok",
                    "Batang dan bunga juga bisa terinfeksi",
                    "Pertumbuhan terhambat, buah kecil"
                ],
                "damage": "Mengurangi fotosintesis 40-70%, penurunan hasil 20-50%",
                "control_methods": {
                    "cultural": [
                        "Gunakan varietas tahan (untuk mentimun: Harmony, Venus)",
                        "Jarak tanam optimal untuk sirkulasi udara (60-80 cm)",
                        "Hindari penyiraman overhead/sprinkle r",
                        "Pemupukan berimbang, hindari N berlebihan",
                        "Pemangkasan daun bawah untuk aliran udara",
                        "Buang sisa tanaman setelah panen"
                    ],
                    "mechanical": [
                        "Petik dan musnahkan daun terinfeksi awal",
                        "Kurangi kelembaban dengan ventilasi greenhouse",
                        "Penyiangan gulma untuk sirkulasi udara",
                        "Hindari tanaman terlalu rimbun"
                    ],
                    "biological": [
                        "Bacillus subtilis strain QST 713",
                        "Trichoderma harzianum aplikasi foliar",
                        "Ampelomyces quisqualis (parasit jamur embun tepung)",
                        "Larutan susu 10% (1:10) seminggu 2x"
                    ],
                    "chemical": [
                        "Preventif: Sulfur 80% WP 2-3 g/L (FRAC M2)",
                        "Kuratif: Triademefon (FRAC 3) 0.5 g/L atau Difenokonazol 1 ml/L",
                        "Sistemik: Azoksistrobin (FRAC 11) atau Piraklostrobin",
                        "Rotasi 3 kelompok FRAC, aplikasi 7-10 hari"
                    ]
                },
                "prevention": [
                    "Tanam varietas tahan",
                    "Aplikasi sulfur preventif sejak 14 HST",
                    "Jaga kelembaban <80% dengan ventilasi",
                    "Hindari tanaman terlalu rapat",
                    "Penyiraman pagi hari agar daun cepat kering",
                    "Monitoring dan aplikasi dini saat gejala pertama",
                    "Rotasi fungisida untuk mencegah resistensi"
                ],
                "favorable_conditions": "Kelembaban 50-80% (tidak perlu air bebas), suhu 20-25°C, teduh",
                "peak_season": "Musim kemarau dengan embun pagi, greenhouse dengan ventilasi buruk"
            },
            
            "embun_bulu": {
                "name": " Embun Bulu / Downy Mildew (Peronospora spp., Pseudoperonospora cubensis)",
                "type": "disease",
                "icon": "💧",
                "category": "Penyakit Jamur",
                "target_crops": ["Mentimun", "Melon", "Semangka", "Bawang", "Selada", "Bayam", "Anggur"],
                "symptoms": [
                    "Bercak kuning pucat di permukaan atas daun",
                    "Jamur putih keunguan di permukaan bawah daun",
                    "Daun mengering dan rontok dari bawah ke atas",
                    "Pertumbuhan terhambat, tanaman kerdil",
                    "Serangan berat: tanaman mati"
                ],
                "damage": "Penurunan hasil 30-80%, terutama saat musim hujan",
                "control_methods": {
                    "cultural": [
                        "Gunakan varietas tahan/toleran",
                        "Jarak tanam lebar untuk sirkulasi udara",
                        "Drainase baik, hindari genangan",
                        "Hindari penyiraman overhead sore/malam",
                        "Rotasi tanaman minimal 2 tahun",
                        "Sanitasi: musnahkan sisa tanaman"
                    ],
                    "mechanical": [
                        "Petik daun terinfeksi segera",
                        "Kurangi kelembaban dengan mulsa plastik",
                        "Pemangkasan untuk sirkulasi udara",
                        "Greenhouse: pastikan ventilasi baik"
                    ],
                    "biological": [
                        "Bacillus subtilis",
                        "Trichoderma spp. aplikasi tanah dan foliar",
                        "Pseudomonas fluorescens",
                        "Aplikasi sejak fase vegetatif"
                    ],
                    "chemical": [
                        "Preventif: Mankozeb (FRAC M3) 2 g/L atau Prop ineb",
                        "Kuratif sistemik: Metalaksil-M + Mankozeb (FRAC 4+M3)",
                        "Dimetomorf (FRAC 40) 1 ml/L atau Siazofamid",
                        "Aplikasi setiap 5-7 hari saat kondisi lembab"
                    ]
                },
                "prevention": [
                    "Tanam varietas tahan",
                    "Aplikasi fungisida preventif sejak 10 HST",
                    "Penyiraman pagi hari, hindari sore/malam",
                    "Jaga kelembaban <85% dengan drainase dan mulsa",
                    "Monitoring ketat saat musim hujan",
                    "Hindari penanaman saat puncak musim hujan",
                    "Rotasi fungisida sistemik dan kontak"
                ],
                "favorable_conditions": "Kelembaban >90%, suhu 15-22°C, embun berat, air bebas di daun",
                "peak_season": "Musim hujan, pagi hari dengan embun berat"
            },
            
            "penggerek_polong": {
                "name": "Penggerek Polong / Pod Borer (Maruca vitrata, Helicoverpa armigera)",
                "type": "pest",
                "icon": "🐛",
                "category": "Hama Perusak Polong & Buah",
                "target_crops": ["Kacang Panjang", "Kedelai", "Kacang Tanah", "Kacang Merah", "Buncis"],
                "symptoms": [
                    "Lubang gerek pada polong muda",
                    "Kotoran larva di dalam polong",
                    "Biji rusak dan berlubang",
                    "Polong hampa atau isi tidak penuh",
                    "Bunga rontok (larva makan bunga)"
                ],
                "damage": "Kerusakan polong 20-80%, penurunan kualitas biji akibat lubang dan kotoran",
                "control_methods": {
                    "cultural": [
                        "Tanam varietas tahan (untuk kacang tanah: Hypoma 1, Kelinci)",
                        "Tanam serentak dalam 2 minggu",
                        "Sanitasi: kumpulkan polong jatuh dan musnahkan",
                        "Rotasi dengan tanaman non-legume",
                        "Olah tanah dalam untuk membunuh pupa",
                        "Hindari penanaman beruntun"
                    ],
                    "mechanical": [
                        "Petik dan musnahkan polong terserang",
                        "Pasang light trap saat malam hari",
                        "Panen tepat waktu untuk mengurangi siklus berikutnya",
                        "Penggo dokan tanah menjelang panen"
                    ],
                    "biological": [
                        "Trichogramma chilonis (parasitoid telur) 100.000/ha 4x",
                        "NPV (Nuclear Polyhedrosis Virus) untuk Helicoverpa",
                        "Bacillus thuringiensis (Bt) strain kurstaki 1-2 g/L",
                        "Predator: Chrysopa, Coccinellidae"
                    ],
                    "chemical": [
                        "Preventif saat bunga mekar: Klorantraniliprol (IRAC Grup 28) 0.25 ml/L",
                        "Profenofos (Grup 1B) 2 ml/L atau Sipermetrin (Grup 3)",
                        "Emamektin benzoat (Grup 6) 0.5 g/L untuk larva",
                        "Aplikasi 5-7 hari saat pembungaan hingga polong muda"
                    ]
                },
                "prevention": [
                    "Monitor ngengat dengan light trap sejak berbunga",
                    "Aplikasi Bt preventif sejak bunga mekar",
                    "Pelepasan Trichogramma 4x mulai awal bunga",
                    "Jarak tanam optimal (40x20 cm untuk kacang panjang)",
                    "Panen segera saat polong masak",
                    "Bersihkan lahan setelah panen, olah tanah dalam",
                    "Hindari tanam kacang-kacangan beruntun"
                ],
                "lifecycle": "25-35 hari, bisa 4-6 generasi/tahun",
                "economic_threshold": "1-2 ngengat/light trap/malam atau 5% polong terlubang",
                "favorable_conditions": "Suhu 25-30°C, populasi tinggi saat berbunga",
                "peak_season": "Musim kemarau, puncak saat fase pembentukan polong"
            },
            
            "kutu_kebul": {
                "name": "Kutu Kebul / Whitefly (Bemisia tabaci, Trialeurodes vaporariorum)",
                "type": "pest",
                "icon": "🦟",
                "category": "Hama Pengisap & Vektor Virus Utama",
                "target_crops": ["Cabai", "Tomat", "Terung", "Kacang Panjang", "Mentimun", "Pepaya", "Singkong"],
                "symptoms": [
                    "Serangga kecil putih terbang saat tanaman diganggu",
                    "Nimfa pipih berwarna putih kehijauan di bawah daun",
                    "Daun menguning dan menggulung",
                    "Embun jelaga (fumagine) dari kotoran kutu",
                    "Gejala virus: daun keriting, mosaik, kerdil"
                ],
                "damage": "Menghisap cairan, menularkan Begomovirus (virus kuning, keriting, mosaik) - kerugian hingga 100%",
                "control_methods": {
                    "cultural": [
                        "Gunakan varietas toleran virus",
                        "Eradikasi tanaman sakit dari virus sejak dini",
                        "Isolasi pertanaman min 500 m dari lahan lama",
                        "Buang gulma inang (solanaceae liar, euphorbiaceae)",
                        "Pembibitan dalam screen house mesh 40",
                        "Hindari penanaman beruntun tanpa jeda 4-6 minggu"
                    ],
                    "mechanical": [
                        "Mulsa plastik perak untuk tolak kutu kebul",
                        "Perangkap kuning lengket 60-80 buah/ha",
                        "Screen house/net house untuk pembibitan",
                        "Karantina bibit 10-14 hari",
                        "Semprot air kuat untuk kurangi populasi nimfa"
                    ],
                    "biological": [
                        "Parasitoid: Encarsia formosa, Eretmocerus eremicus",
                        "Predator: Delphastus catalinae, Chrysopa",
                        "Jamur: Beauveria bassiana, Verticillium lecanii, Paecilomyces fumosoroseus",
                        "Aplikasi jamur setiap 5-7 hari"
                    ],
                    "chemical": [
                        "Sistemik: Imidakloprid 0.3 g/L atau Tiametoksam 0.2 g/L (IRAC 4A)",
                        "Penghambat pertumbuhan: Buprofezin (Grup 16) 1 g/L atau Piriproksifen",
                        "Kontak: Spiromesifen (Grup 23) atau Piridaben (Grup 21)",
                        "Rotasi ketat 3-4 kelompok IRAC, semprot 3-5 hari sekali hingga 60 HST",
                        "Aplikasi malam/sore untuk nimfa di bawah daun"
                    ]
                },
                "prevention": [
                    "Mulsa perak aplikasi sejak tanam",
                    "Screen house untuk pembibitan (mesh 40 anti-kutu kebul)",
                    "Pas ang perangkap kuning sejak tanam untuk monitor",
                    "Semprot preventif imidakloprid sejak 7 HST",
                    "Roguing tanaman virus <20%; bongkar total >20%",
                    "Sanitasi purnatanam: bongkar semua tanaman, bera 4-6 minggu",
                    "Hindari tanam solanaceae beruntun",
                    "Zona buffer dengan tanaman non-inang"
                ],
                "lifecycle": "18-30 hari, reproduksi sangat cepat terutama musim kering",
                "economic_threshold": "1-2 dewasa/daun atau 5 nimfa/daun (sebelum virus muncul)",
                "favorable_conditions": "Suhu 25-32°C, kondisi kering, tanaman muda",
                "peak_season": "Musim kemarau (April-Oktober), puncak Juli-Agustus"
            },
            
            "layu_bakteri": {
                "name": "Layu Bakteri / Bacterial Wilt (Ralstonia solanacearum)",
                "type": "disease",
                "icon": "🦠",
                "category": "Penyakit Bakteri Tanah",
                "target_crops": ["Tomat", "Terung", "Cabai", "Kentang", "Tembakau", "Pisang", "Jahe"],
                "symptoms": [
                    "Layu mendadak saat siang, segar pagi/malam (awal)",
                    "Layu permanen seluruh tanaman",
                    "Batang dipotong: keluar lendir bakteri putih keabu-abuan",
                    "Tes gelas: batang dalam air, keluar lendir seperti asap",
                    "Pembuluh kayu coklat",
                    "Tanaman mati 3-7 hari"
                ],
                "damage": "Kematian tanaman 10-90%, terutama lahan endemik, kerugian ekonomi sangat tinggi",
                "control_methods": {
                    "cultural": [
                        "Rotasi dengan monokot (padi, jagung) min 3-4 tahun",
                        "Gunakan varietas tahan (untuk tomat: Mutiara, CLN-1462A, Hawaii 7996)",
                        "Solarisasi tanah plastik transparan 6-8 minggu",
                        "Pengapuran berat: Dolomit 2-3 ton/ha untuk pH >7.0",
                        "Bedengan tinggi 30-40 cm, drainase sempurna",
                        "Hindari luka akar (nematoda, pengolahan)",
                        "Jangan tanam solanaceae 4-5 tahun di lahan endemik"
                    ],
                    "mechanical": [
                        "Eradikasi tanaman sakit secepatnya (bakar + desinfeksi tanah)",
                        "Sterilisasi alat dengan kaporit 1% atau lisol",
                        "Mulsa plastik untuk cegah percikan tanah",
                        "Buat zona karantina di sekitar tanaman sakit",
                        "Hindari penyiraman berlebihan"
                    ],
                    "biological": [
                        "Trichoderma spp. + Pseudomonas fluorescens kocor lubang tanam",
                        "Bacillus subtilis aplikasi tanah dan kocor",
                        "PGPR (Plant Growth Promoting Rhizobacteria) campuran",
                        "Bakteriofag spesifik Ralstonia (masih penelitian)"
                    ],
                    "chemical": [
                        "Perlakuan tanah: Copper hydroxide atau Copper oxychloride kocor",
                        "Bakterisida Streptomisin sulfat 1-2 g/L (kocor, terbatas)",
                        "Klorin dioksida atau Kalsium hipoklorit untuk desinfeksi tanah",
                        "Efektivitas rendah jika sudah ada di tanah"
                    ]
                },
                "prevention": [
                    "PALING PENTING: JANGAN TANAM DI LAHAN BEKAS LAYU BAKTERI",
                    "Gunakan bibit sehat, media steril baru",
                    "Perlakuan bibit dengan Trichoderma + Pseudomonas",
                    "Solarisasi tanah sebelum tanam (lahan suspect)",
                    "Pengapuran berat (pH >7.0 menghambat bakteri)",
                    "Drainase sempurna, hindari genangan",
                    "Control nematoda (vektor) dengan nematisida atau biokontrol",
                    "Rotasi PANJANG min 4 tahun dengan non-solanaceae",
                    "Monitoring dan eradikasi dini (<5% serangan)",
                    "Desinfeksi alat dan sepatu sebelum masuk lahan"
                ],
                "favorable_conditions": "Suhu 28-32°C, pH tanah 6.0-7.0, kelembaban tanah tinggi, luka akar",
                "peak_season": "Musim hujan dan awal kemarau (suhu tinggi + tanah lembab)"
            },
            
            "nematoda_puru_akar": {
                "name": "Nematoda Puru Akar / Root-Knot Nematode (Meloidogyne spp.)",
                "type": "pest",
                "icon": "🪱",
                "category": "Hama Akar (Nematoda)",
                "target_crops": ["Tomat", "Cabai", "Terung", "Mentimun", "Wortel", "Selada", "Stroberi", "Mawar"],
                "symptoms": [
                    "Tanaman kerdil, pertumbuhan lambat",
                    "Daun menguning (defisiensi N), layu siang hari",
                    "Produktivitas rendah, buah kecil",
                    "Akar: puru/benjolan (galls) seperti mutiara di sepanjang akar",
                    "Akar bercabang berlebihan (root proliferation)",
                    "Sistem akar rusak, mudah dicabut"
                ],
                "damage": "Penurunan hasil 20-80%, terutama tanaman muda terserang berat",
                "control_methods": {
                    "cultural": [
                        "Rotasi dengan monokot (padi, jagung) atau Tagetes (kenikir) min 2 tahun",
                        "Gunakan varietas tahan (untuk tomat: TMGR-1542, Nematex)",
                        "Solarisasi tanah: plastik transparan 4-6 minggu musim kemarau",
                        "Aplikasi bahan organik tinggi: kompos 20-30 ton/ha atau pupuk hijau",
                        "Tanam Tagetes (French marigold) sebagai tanaman perangkap/pengelabui",
                        "Bera tanah minimal 2-3 bulan dengan pengolahan berulang"
                    ],
                    "mechanical": [
                        "Cabut dan bakar tanaman terserang berat beserta akar",
                        "Galian akar hati-hati untuk tidak sebarkan nematoda",
                        "Pengolahan tanah dalam dan berulang",
                        "Solarisasi kombinasi dengan pengolahan",
                        "Gunakan media tanam steril untuk pembibitan"
                    ],
                    "biological": [
                        "Paecilomyces lilacinus (jamur parasit nematoda) 10-20 g/tanaman",
                        "Pochonia chlamydosporia (parasit telur nematoda)",
                        "Trichoderma spp. + Pseudomonas fluorescens",
                        "Nematoda predator: Mononchus, Iotonchus",
                        "Bakteri Pasteuria penetrans (parasit nematoda)"
                    ],
                    "chemical": [
                        "Nematisida fumigan: Metam sodium (cair, aplikasi 2-3 minggu sebelum tanam)",
                        "Nematisida non-fumigan: Carbofuran granul 1-2 kg/ha (terbatas)",
                        "Fluensulfone (nematisida modern) 3-5 L/ha",
                        "PENTING: Penggunaan nematisida harus ijin dan sangat hati-hati (toksik)"
                    ]
                },
                "prevention": [
                    "Gunakan bibit sehat, media steril untuk persemaian",
                    "Rotasi tanaman dengan Tagetes, rumput Sudan, atau monokot",
                    "Solarisasi tanah sebelum tanam",
                    "Aplikasi bahan organik tinggi (C/N tinggi)",
                    "Irigasi terkelola (hindari over-watering)",
                    "Sterilisasi alat dan alas kaki sebelum masuk lahan",
                    "Monitoring rutin: cek akar tanaman sampel setiap bulan",
                    "Tanam varietas tahan/toleran",
                    "Aplikasi agens biokontrol preventif"
                ],
                "lifecycle": "25-30 hari pada suhu optimal, bisa 4-6 generasi/musim tanam",
                "economic_threshold": "1 juvenile/100 cm³ tanah (sebelum tanam); gejala pada 5-10% tanaman",
                "favorable_conditions": "Suhu 25-30°C, tanah berpasir/ringan, pH 6.0-7.0, kelembaban sedang",
                "peak_season": "Sepanjang tahun, puncak saat suhu hangat dan tanah lembab"
            }
        }

    
    @staticmethod
    def get_pest_list():
        """Get list of all pests and diseases."""
        db = PestDiseaseDatabase.get_all_pests()
        pest_list = []
        
        for key, data in db.items():
            pest_list.append({
                "id": key,
                "name": data["name"],
                "type": data["type"],
                "icon": data["icon"],
                "category": data["category"],
                "target_crops": ", ".join(data["target_crops"])
            })
        
        return pest_list
    
    @staticmethod
    def get_pest_detail(pest_id):
        """Get detailed information for specific pest."""
        db = PestDiseaseDatabase.get_all_pests()
        return db.get(pest_id)

    @staticmethod
    def get_diagnostic_tree():
        """
        Return the decision tree for smart diagnostics.
        Structure: Part -> Symptom -> Detail -> Result (Pest ID)
        """
        return {
            "Daun": {
                "Berlubang / Rusak Fisik": {
                    "Lubang tidak beraturan, transparan (jendela)": "ulat_grayak",
                    "Daun menggulung, ada ulat di dalam": "ulat_grayak",
                    "Terowongan putih berkelok-kelok": "penggerek_daun",
                    "Daun muda keriting/kaku": "thrips"
                },
                "Bercak / Noda": {
                    "Bercak coklat belah ketupat (seperti mata)": "blas",
                    "Bercak basah kehitaman, meluas cepat": "busuk_daun",
                    "Bercak coklat dengan lingkaran konsentris": "antraknosa",
                    "Bercak putih seperti tepung/bedak": "embun_tepung",
                    "Garis kuning/coklat dari tepi daun": "hawar_daun_bakteri"
                },
                "Perubahan Warna / Bentuk": {
                    "Menguning total, kerdil, daun kaku": "virus_kuning_cabai",
                    "Menguning dari ujung (seperti terbakar)": "wereng_coklat",
                    "Daun keriting, ada kutu di balik daun": "kutu_daun",
                    "Layu pada siang hari, segar pagi/sore": "layu_fusarium"
                }
            },
            "Batang": {
                "Busuk / Berubah Warna": {
                    "Pangkal batang membusuk/hitam": "busuk_daun",
                    "Batang patah/rebah, ada lubang gerek": "penggerek_batang",
                    "Pembuluh kayu berwarna coklat (saat dipotong)": "layu_fusarium"
                },
                "Kerusakan Fisik": {
                    "Batang muda terpotong di pangkal (tanaman roboh)": "ulat_tanah",
                    "Ada lubang kecil dengan kotoran ulat": "penggerek_batang"
                }
            },
            "Buah": {
                "Busuk": {
                    "Bercak cekung coklat kehitaman (patek)": "antraknosa",
                    "Busuk basah, ada belatung di dalam": "lalat_buah",
                    "Busuk ujung buah": "busuk_daun"
                },
                "Cacat Fisik": {
                    "Buah bengkok/kerdil": "thrips",
                    "Ada lubang tusukan kecil": "lalat_buah",
                    "Buah rontok prematur": "lalat_buah"
                }
            },
            "Akar / Seluruh Tanaman": {
                "Layu / Mati": {
                    "Layu mendadak (siang hari), lalu mati": "layu_fusarium",
                    "Kerdil, kuning, tidak tumbuh": "virus_kuning_cabai",
                    "Tanaman roboh serentak (seperti terbakar)": "wereng_coklat",
                    "Bengkak pada akar (puru)": "nematoda_bengkak_akar"
                }
            }
        }
