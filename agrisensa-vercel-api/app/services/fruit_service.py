"""Fruit crops service for comprehensive fruit cultivation information."""


class FruitService:
    """Service for fruit crop cultivation guides and information."""
    
    # Comprehensive fruit crops database
    FRUIT_DATABASE = {
        "mangga": {
            "name": "Mangga",
            "scientific_name": "Mangifera indica",
            "icon": "🥭",
            "description": "Mangga adalah buah tropis bernilai ekonomi tinggi dengan permintaan pasar yang stabil.",
            "varieties": [
                "Gedong Gincu - Manis, harum, cocok untuk pasar premium",
                "Arumanis - Daging tebal, serat sedikit, favorit ekspor",
                "Manalagi - Rasa manis, produktivitas tinggi",
                "Cengkir - Tahan penyakit, cocok dataran rendah"
            ],
            "growing_requirements": {
                "altitude": "0-700 mdpl (optimal 200-600 mdpl)",
                "temperature": "24-30°C",
                "rainfall": "1000-2000 mm/tahun dengan musim kering 2-3 bulan",
                "soil_ph": "5.5-7.5",
                "soil_type": "Lempung berpasir, drainase baik"
            },
            "cultivation_guide": {
                "Pembibitan": [
                    "Gunakan bibit okulasi/sambung pucuk dari induk unggul",
                    "Bibit siap tanam umur 6-8 bulan, tinggi 60-80 cm",
                    "Pilih bibit sehat, batang lurus, daun hijau segar"
                ],
                "Penanaman": [
                    "Jarak tanam 8x8 m atau 10x10 m (tergantung varietas)",
                    "Lubang tanam 80x80x80 cm, buat 1-2 bulan sebelum tanam",
                    "Campur tanah galian dengan pupuk kandang 20-30 kg + Dolomit 500g",
                    "Tanam di awal musim hujan"
                ],
                "Pemupukan": [
                    "Tahun 1-3: NPK 15-15-15 (1-3 kg/pohon/tahun)",
                    "Tahun 4+: NPK 15-15-15 (5-10 kg/pohon/tahun)",
                    "Aplikasi 2-3 kali per tahun (awal hujan, akhir hujan, setelah panen)",
                    "Tambahkan pupuk organik 20-40 kg/pohon/tahun"
                ],
                "Pemeliharaan": [
                    "Pemangkasan bentuk saat tanaman muda",
                    "Pemangkasan produksi setelah panen (buang cabang kering/sakit)",
                    "Penyiraman intensif saat pembungaan dan pembesaran buah",
                    "Penjarangan buah: sisakan 1-2 buah per malai"
                ]
            },
            "pests_diseases": {
                "Lalat Buah": {
                    "symptoms": "Buah berlubang, berulat, busuk",
                    "control": "Perangkap petrogenol, pembungkusan buah muda, sanitasi buah jatuh"
                },
                "Antraknosa": {
                    "symptoms": "Bercak hitam pada buah, daun, ranting",
                    "control": "Fungisida Mankozeb/Azoksistrobin, sanitasi kebun"
                },
                "Embun Jelaga": {
                    "symptoms": "Lapisan hitam seperti jelaga pada daun/buah",
                    "control": "Kendalikan kutu sebagai vektor, semprot fungisida"
                },
                "Trips": {
                    "symptoms": "Buah muda rontok, kulit buah kasar",
                    "control": "Insektisida Abamektin, jaga kelembaban"
                }
            },
            "harvest_postharvest": {
                "harvest_age": "90-120 hari setelah bunga mekar (tergantung varietas)",
                "harvest_signs": "Warna kulit mulai berubah, tangkai buah mudah lepas, aroma harum",
                "postharvest": [
                    "Panen pagi hari, sisakan tangkai 2-3 cm",
                    "Sortasi berdasarkan ukuran dan kualitas",
                    "Peram dengan karbit untuk mempercepat matang (opsional)",
                    "Simpan di ruang sejuk (12-15°C) untuk memperpanjang umur simpan"
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Mangga per 1 Hektar (100 pohon)",
                "investment_costs": [
                    {"item": "Bibit Okulasi", "quantity": "100 pohon", "unit_price": 50000, "total": 5000000},
                    {"item": "Persiapan Lahan & Lubang Tanam", "quantity": "1 ha", "unit_price": 3000000, "total": 3000000},
                    {"item": "Pupuk Dasar (tahun 1)", "quantity": "Paket", "unit_price": 2000000, "total": 2000000},
                    {"item": "Tenaga Kerja Tanam", "quantity": "10 HOK", "unit_price": 100000, "total": 1000000}
                ],
                "annual_costs": [
                    {"item": "Pupuk NPK", "quantity": "500 kg", "unit_price": 8000, "total": 4000000},
                    {"item": "Pupuk Organik", "quantity": "2 ton", "unit_price": 1000000, "total": 2000000},
                    {"item": "Pestisida/Fungisida", "quantity": "Paket", "unit_price": 1500000, "total": 1500000},
                    {"item": "Tenaga Kerja Pemeliharaan", "quantity": "24 HOK/tahun", "unit_price": 100000, "total": 2400000},
                    {"item": "Panen & Pasca Panen", "quantity": "Paket", "unit_price": 2000000, "total": 2000000}
                ],
                "production_timeline": "Mulai berbuah tahun ke-3, produktif penuh tahun ke-5",
                "yield_potential": [
                    {"year": "Tahun 3", "yield_per_tree_kg": 20, "total_yield_kg": 2000, "price_per_kg": 15000},
                    {"year": "Tahun 5+", "yield_per_tree_kg": 80, "total_yield_kg": 8000, "price_per_kg": 15000}
                ],
                "roi_notes": "ROI positif mulai tahun ke-4. Umur ekonomis 20-30 tahun."
            }
        },
        "jeruk": {
            "name": "Jeruk",
            "scientific_name": "Citrus sp.",
            "icon": "🍊",
            "description": "Jeruk adalah buah sitrus dengan kandungan vitamin C tinggi, permintaan pasar sepanjang tahun.",
            "varieties": [
                "Keprok Batu 55 - Manis, produktif, tahan penyakit",
                "Siam Pontianak - Tanpa biji, manis, cocok dataran rendah",
                "Santang Madu - Sangat manis, ukuran sedang",
                "Lemon Cui - Asam segar, untuk minuman"
            ],
            "growing_requirements": {
                "altitude": "200-1200 mdpl (optimal 400-800 mdpl)",
                "temperature": "20-30°C",
                "rainfall": "1500-2500 mm/tahun, merata",
                "soil_ph": "5.5-6.5",
                "soil_type": "Lempung berdrainase baik, kaya bahan organik"
            },
            "cultivation_guide": {
                "Pembibitan": [
                    "Gunakan bibit okulasi/sambung dari induk bersertifikat",
                    "Batang bawah: Japansche Citroen (JC) atau Rough Lemon",
                    "Bibit siap tanam umur 8-12 bulan"
                ],
                "Penanaman": [
                    "Jarak tanam 5x5 m atau 6x6 m",
                    "Lubang tanam 60x60x60 cm",
                    "Campur tanah dengan pupuk kandang 15-20 kg + Dolomit 300g",
                    "Tanam di awal musim hujan, hindari genangan air"
                ],
                "Pemupukan": [
                    "Tahun 1: NPK 15-15-15 (500g/pohon/tahun)",
                    "Tahun 2-3: NPK 15-15-15 (1-2 kg/pohon/tahun)",
                    "Tahun 4+: NPK 15-15-15 (3-5 kg/pohon/tahun)",
                    "Aplikasi 3-4 kali per tahun, hindari saat kemarau panjang"
                ],
                "Pemeliharaan": [
                    "Pemangkasan bentuk untuk tajuk terbuka",
                    "Buang tunas air dan cabang yang tumbuh ke dalam",
                    "Penyiraman rutin saat musim kering",
                    "Mulsa untuk menjaga kelembaban tanah"
                ]
            },
            "pests_diseases": {
                "CVPD (Citrus Vein Phloem Degeneration)": {
                    "symptoms": "Daun menguning, buah kecil asam, pohon mati perlahan",
                    "control": "Gunakan bibit bebas CVPD, kendalikan kutu loncat (vektor), cabut pohon terinfeksi"
                },
                "Kutu Loncat (Diaphorina citri)": {
                    "symptoms": "Daun keriting, pertumbuhan terhambat",
                    "control": "Insektisida Imidakloprid, monitoring rutin"
                },
                "Ulat Penggerek Buah": {
                    "symptoms": "Buah berlubang, rontok prematur",
                    "control": "Sanitasi buah jatuh, insektisida Klorpirifos"
                },
                "Embun Jelaga": {
                    "symptoms": "Lapisan hitam pada daun",
                    "control": "Kendalikan kutu sebagai vektor"
                }
            },
            "harvest_postharvest": {
                "harvest_age": "6-8 bulan setelah bunga mekar",
                "harvest_signs": "Warna kulit orange penuh, rasa manis optimal",
                "postharvest": [
                    "Panen dengan gunting, hindari merusak tangkai",
                    "Sortasi: Grade A (besar, mulus), Grade B (sedang), Grade C (kecil/cacat)",
                    "Simpan di ruang sejuk untuk memperpanjang kesegaran",
                    "Hindari tumpukan terlalu tinggi (max 3 lapis)"
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Jeruk per 1 Hektar (400 pohon)",
                "investment_costs": [
                    {"item": "Bibit Okulasi", "quantity": "400 pohon", "unit_price": 35000, "total": 14000000},
                    {"item": "Persiapan Lahan", "quantity": "1 ha", "unit_price": 2500000, "total": 2500000},
                    {"item": "Pupuk Dasar", "quantity": "Paket", "unit_price": 1500000, "total": 1500000}
                ],
                "annual_costs": [
                    {"item": "Pupuk NPK", "quantity": "800 kg", "unit_price": 8000, "total": 6400000},
                    {"item": "Pestisida", "quantity": "Paket", "unit_price": 2000000, "total": 2000000},
                    {"item": "Tenaga Kerja", "quantity": "30 HOK/tahun", "unit_price": 100000, "total": 3000000}
                ],
                "production_timeline": "Mulai berbuah tahun ke-3, produktif penuh tahun ke-5",
                "yield_potential": [
                    {"year": "Tahun 3", "yield_per_tree_kg": 15, "total_yield_kg": 6000, "price_per_kg": 12000},
                    {"year": "Tahun 5+", "yield_per_tree_kg": 40, "total_yield_kg": 16000, "price_per_kg": 12000}
                ],
                "roi_notes": "ROI positif tahun ke-4. Umur ekonomis 15-20 tahun."
            }
        },
        "pepaya": {
            "name": "Pepaya",
            "scientific_name": "Carica papaya",
            "icon": "🍈",
            "description": "Pepaya adalah buah cepat panen dengan permintaan tinggi untuk konsumsi segar dan industri.",
            "varieties": [
                "California - Daging orange, manis, ukuran besar",
                "Bangkok - Daging merah, sangat manis",
                "IPB-9 - Produktif, tahan penyakit",
                "Red Lady - Hibrida, kualitas premium"
            ],
            "growing_requirements": {
                "altitude": "0-700 mdpl",
                "temperature": "22-32°C",
                "rainfall": "1000-2000 mm/tahun, merata",
                "soil_ph": "6.0-7.0",
                "soil_type": "Gembur, drainase sempurna, tidak tergenang"
            },
            "cultivation_guide": {
                "Pembibitan": [
                    "Semai benih di polybag, media tanah:kompos (1:1)",
                    "Bibit siap tanam umur 1.5-2 bulan (4-6 daun sejati)",
                    "Pilih bibit sehat, batang kokoh"
                ],
                "Penanaman": [
                    "Jarak tanam 2x2 m atau 2.5x2.5 m",
                    "Lubang tanam 50x50x50 cm",
                    "Campur tanah dengan pupuk kandang 10 kg",
                    "Tanam 2-3 bibit per lubang, seleksi setelah berbunga (sisakan 1 pohon hermafrodit)"
                ],
                "Pemupukan": [
                    "Umur 1-3 bulan: NPK 16-16-16 (50g/pohon/bulan)",
                    "Umur 4-6 bulan: NPK 16-16-16 (100g/pohon/bulan)",
                    "Umur 7+ bulan: NPK 16-16-16 (150-200g/pohon/bulan)",
                    "Tambahkan pupuk organik cair setiap 2 minggu"
                ],
                "Pemeliharaan": [
                    "Penyiraman rutin, jaga kelembaban tanah",
                    "Buang daun tua/kuning secara berkala",
                    "Penjarangan buah jika terlalu lebat",
                    "Sanitasi: buang buah busuk/terserang penyakit"
                ]
            },
            "pests_diseases": {
                "Virus Mosaik (Papaya Ring Spot Virus)": {
                    "symptoms": "Daun mosaik kuning-hijau, buah berbintik, pertumbuhan kerdil",
                    "control": "Gunakan varietas tahan, kendalikan kutu daun (vektor), cabut tanaman sakit"
                },
                "Antraknosa": {
                    "symptoms": "Bercak hitam pada buah matang",
                    "control": "Fungisida Mankozeb preventif, panen tepat waktu"
                },
                "Kutu Daun": {
                    "symptoms": "Daun keriting, vektor virus",
                    "control": "Insektisida Imidakloprid, monitoring intensif"
                },
                "Busuk Akar": {
                    "symptoms": "Layu mendadak, akar hitam busuk",
                    "control": "Perbaiki drainase, hindari genangan, fungisida tanah"
                }
            },
            "harvest_postharvest": {
                "harvest_age": "8-10 bulan setelah tanam (buah pertama), panen rutin setiap minggu",
                "harvest_signs": "Warna kulit mulai kuning (1-2 garis), buah keras tapi matang",
                "postharvest": [
                    "Panen pagi hari dengan pisau tajam",
                    "Hindari memar, getah dapat merusak kulit buah",
                    "Peram di ruang teduh untuk mempercepat matang",
                    "Umur simpan 5-7 hari pada suhu ruang"
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Pepaya per 1 Hektar (1600 pohon)",
                "investment_costs": [
                    {"item": "Benih/Bibit", "quantity": "1600 pohon", "unit_price": 2000, "total": 3200000},
                    {"item": "Persiapan Lahan", "quantity": "1 ha", "unit_price": 2000000, "total": 2000000},
                    {"item": "Pupuk Dasar", "quantity": "Paket", "unit_price": 1000000, "total": 1000000}
                ],
                "annual_costs": [
                    {"item": "Pupuk NPK", "quantity": "2 ton", "unit_price": 8000, "total": 16000000},
                    {"item": "Pestisida", "quantity": "Paket", "unit_price": 1500000, "total": 1500000},
                    {"item": "Tenaga Kerja", "quantity": "40 HOK/tahun", "unit_price": 100000, "total": 4000000}
                ],
                "production_timeline": "Mulai panen bulan ke-8, produktif 2-3 tahun",
                "yield_potential": [
                    {"year": "Tahun 1 (10 bulan)", "yield_per_tree_kg": 30, "total_yield_kg": 48000, "price_per_kg": 5000},
                    {"year": "Tahun 2", "yield_per_tree_kg": 50, "total_yield_kg": 80000, "price_per_kg": 5000}
                ],
                "roi_notes": "ROI sangat cepat (8-12 bulan). Umur ekonomis 2-3 tahun, lalu replanting."
            }
        },
        "pisang": {
            "name": "Pisang",
            "scientific_name": "Musa sp.",
            "icon": "🍌",
            "description": "Pisang adalah buah tropis dengan permintaan tinggi, cocok untuk konsumsi segar dan olahan.",
            "varieties": ["Cavendish - Ekspor, ukuran besar", "Ambon - Manis, populer lokal", "Raja - Aroma khas, premium"],
            "growing_requirements": {"altitude": "0-1500 mdpl", "temperature": "20-35°C", "rainfall": "2000-3000 mm/tahun", "soil_ph": "5.5-7.0", "soil_type": "Gembur, drainase baik"},
            "cultivation_guide": {
                "Pembibitan": ["Gunakan anakan dari induk produktif", "Pilih anakan pedang (tinggi 100-150 cm)"],
                "Penanaman": ["Jarak tanam 3x3 m", "Lubang 50x50x50 cm", "Campur pupuk kandang 10 kg"],
                "Pemupukan": ["Umur 2 bulan: NPK 200g/pohon", "Umur 4-6 bulan: NPK 300-400g/pohon", "Pupuk organik 20 kg/pohon/tahun"],
                "Pemeliharaan": ["Buang daun kering", "Potong jantung pisang setelah sisir terakhir", "Penyiraman rutin"]
            },
            "pests_diseases": {
                "Layu Panama": {"symptoms": "Daun kuning, layu, tanaman mati", "control": "Gunakan varietas tahan, sanitasi kebun"},
                "Penggerek Bonggol": {"symptoms": "Bonggol berlubang, tanaman roboh", "control": "Insektisida Karbofuran granul"},
                "Bercak Daun": {"symptoms": "Bercak coklat pada daun", "control": "Fungisida Mankozeb"}
            },
            "harvest_postharvest": {"harvest_age": "10-12 bulan setelah tanam", "harvest_signs": "Buah penuh, sudut buah mulai tumpul", "postharvest": ["Panen saat 75-80% matang", "Peram dengan karbit 1-2 hari", "Simpan di ruang sejuk"]},
            "business_analysis": {
                "title": "Analisis Usaha Pisang per 1 Hektar (1100 pohon)",
                "investment_costs": [{"item": "Bibit Anakan", "quantity": "1100 pohon", "unit_price": 5000, "total": 5500000}],
                "annual_costs": [{"item": "Pupuk & Pestisida", "quantity": "Paket", "unit_price": 8000000, "total": 8000000}],
                "production_timeline": "Panen pertama bulan ke-10, panen rutin setiap bulan dari anakan",
                "yield_potential": [{"year": "Tahun 1", "yield_per_tree_kg": 25, "total_yield_kg": 27500, "price_per_kg": 8000}],
                "roi_notes": "ROI cepat (10-12 bulan). Produktif 5-7 tahun."
            }
        },
        "durian": {
            "name": "Durian",
            "scientific_name": "Durio zibethinus",
            "icon": "🌰",
            "description": "Durian adalah raja buah dengan harga premium dan permintaan tinggi.",
            "varieties": ["Monthong - Daging tebal, manis", "Musang King - Premium, harga tinggi", "Petruk - Lokal unggul"],
            "growing_requirements": {"altitude": "50-600 mdpl", "temperature": "24-30°C", "rainfall": "1500-2500 mm/tahun", "soil_ph": "5.0-6.5", "soil_type": "Lempung dalam, drainase baik"},
            "cultivation_guide": {
                "Pembibitan": ["Gunakan bibit sambung/okulasi", "Bibit siap tanam umur 1-1.5 tahun"],
                "Penanaman": ["Jarak tanam 10x10 m atau 12x12 m", "Lubang 100x100x100 cm", "Pupuk kandang 40-50 kg"],
                "Pemupukan": ["Tahun 1-3: NPK 2-5 kg/pohon/tahun", "Tahun 4+: NPK 10-15 kg/pohon/tahun"],
                "Pemeliharaan": ["Pemangkasan cabang tidak produktif", "Penyiraman saat kemarau", "Mulsa untuk jaga kelembaban"]
            },
            "pests_diseases": {
                "Penggerek Buah": {"symptoms": "Buah berlubang, busuk", "control": "Sanitasi, insektisida sistemik"},
                "Busuk Akar": {"symptoms": "Daun kuning, pohon layu", "control": "Perbaiki drainase, fungisida tanah"},
                "Kutu Putih": {"symptoms": "Daun keriting, pertumbuhan terhambat", "control": "Insektisida Imidakloprid"}
            },
            "harvest_postharvest": {"harvest_age": "110-120 hari setelah bunga mekar", "harvest_signs": "Warna kulit berubah, aroma khas, tangkai kering", "postharvest": ["Panen saat jatuh atau hampir jatuh", "Simpan 2-3 hari untuk matang sempurna", "Jual segera untuk kesegaran optimal"]},
            "business_analysis": {
                "title": "Analisis Usaha Durian per 1 Hektar (100 pohon)",
                "investment_costs": [{"item": "Bibit Sambung", "quantity": "100 pohon", "unit_price": 150000, "total": 15000000}],
                "annual_costs": [{"item": "Pupuk & Perawatan", "quantity": "Paket", "unit_price": 10000000, "total": 10000000}],
                "production_timeline": "Mulai berbuah tahun ke-5, produktif penuh tahun ke-8",
                "yield_potential": [{"year": "Tahun 5", "yield_per_tree_kg": 30, "total_yield_kg": 3000, "price_per_kg": 40000}, {"year": "Tahun 8+", "yield_per_tree_kg": 80, "total_yield_kg": 8000, "price_per_kg": 40000}],
                "roi_notes": "Investasi besar, ROI tahun ke-7. Umur ekonomis 30+ tahun. Harga premium."
            }
        },
        "rambutan": {
            "name": "Rambutan",
            "scientific_name": "Nephelium lappaceum",
            "icon": "🍇",
            "description": "Rambutan adalah buah tropis populer dengan permintaan stabil.",
            "varieties": ["Binjai - Manis, daging tebal", "Rapiah - Produktif, tahan penyakit", "Lebak Bulus - Ukuran besar"],
            "growing_requirements": {"altitude": "0-600 mdpl", "temperature": "22-30°C", "rainfall": "2000-3000 mm/tahun", "soil_ph": "5.0-6.5", "soil_type": "Lempung berpasir, drainase baik"},
            "cultivation_guide": {
                "Pembibitan": ["Gunakan bibit sambung/cangkok", "Bibit siap tanam umur 8-12 bulan"],
                "Penanaman": ["Jarak tanam 8x8 m atau 10x10 m", "Lubang 60x60x60 cm", "Pupuk kandang 20 kg"],
                "Pemupukan": ["Tahun 1-3: NPK 1-3 kg/pohon/tahun", "Tahun 4+: NPK 5-8 kg/pohon/tahun"],
                "Pemeliharaan": ["Pemangkasan cabang tidak produktif", "Penyiraman saat kemarau", "Penjarangan buah jika terlalu lebat"]
            },
            "pests_diseases": {
                "Penggerek Buah": {"symptoms": "Buah berlubang, berulat", "control": "Sanitasi, pembungkusan buah"},
                "Antraknosa": {"symptoms": "Bercak hitam pada buah", "control": "Fungisida Mankozeb"},
                "Kutu Daun": {"symptoms": "Daun keriting", "control": "Insektisida Imidakloprid"}
            },
            "harvest_postharvest": {"harvest_age": "90-100 hari setelah bunga mekar", "harvest_signs": "Warna kulit merah penuh, rambut tidak mudah rontok", "postharvest": ["Panen dengan gunting, sisakan tangkai", "Sortasi berdasarkan ukuran", "Simpan di ruang sejuk, umur simpan 5-7 hari"]},
            "business_analysis": {
                "title": "Analisis Usaha Rambutan per 1 Hektar (100 pohon)",
                "investment_costs": [{"item": "Bibit Sambung", "quantity": "100 pohon", "unit_price": 50000, "total": 5000000}],
                "annual_costs": [{"item": "Pupuk & Perawatan", "quantity": "Paket", "unit_price": 6000000, "total": 6000000}],
                "production_timeline": "Mulai berbuah tahun ke-4, produktif penuh tahun ke-6",
                "yield_potential": [{"year": "Tahun 4", "yield_per_tree_kg": 30, "total_yield_kg": 3000, "price_per_kg": 12000}, {"year": "Tahun 6+", "yield_per_tree_kg": 80, "total_yield_kg": 8000, "price_per_kg": 12000}],
                "roi_notes": "ROI tahun ke-5. Umur ekonomis 20-25 tahun."
            }
        },
        "melon": {
            "name": "Melon",
            "scientific_name": "Cucumis melo",
            "icon": "🍈",
            "description": "Melon adalah buah musiman dengan harga jual tinggi dan masa tanam pendek.",
            "varieties": ["Action - Jingga, manis", "Sky Rocket - Hijau, tahan penyakit", "Glamour - Premium, ekspor"],
            "growing_requirements": {"altitude": "200-800 mdpl", "temperature": "25-30°C", "rainfall": "600-1200 mm/tahun (irigasi)", "soil_ph": "6.0-7.0", "soil_type": "Gembur, drainase sempurna"},
            "cultivation_guide": {
                "Pembibitan": ["Semai benih di tray/polybag", "Bibit siap tanam umur 10-14 hari"],
                "Penanaman": ["Jarak tanam 1.5x0.5 m (sistem bedengan)", "Gunakan mulsa plastik hitam-perak", "Buat bedengan tinggi 30-40 cm"],
                "Pemupukan": ["Pupuk dasar: NPK 15-15-15 (300 kg/ha)", "Pupuk susulan: NPK tinggi K setiap minggu via fertigasi", "Pupuk organik cair 2x seminggu"],
                "Pemeliharaan": ["Pemangkasan tunas samping", "Sisakan 2-3 buah per tanaman", "Penyiraman via drip irrigation", "Pasang jaring untuk gantung buah"]
            },
            "pests_diseases": {
                "Layu Fusarium": {"symptoms": "Tanaman layu mendadak", "control": "Rotasi tanaman, fungisida tanah"},
                "Kutu Daun": {"symptoms": "Daun keriting, vektor virus", "control": "Insektisida Imidakloprid"},
                "Embun Tepung": {"symptoms": "Lapisan putih pada daun", "control": "Fungisida Sulfur"}
            },
            "harvest_postharvest": {"harvest_age": "60-70 hari setelah tanam", "harvest_signs": "Warna kulit berubah, aroma harum, tangkai mudah lepas", "postharvest": ["Panen pagi hari", "Sortasi: Grade A (>1.5 kg), Grade B (1-1.5 kg)", "Simpan di ruang sejuk 10-15°C"]},
            "business_analysis": {
                "title": "Analisis Usaha Melon per 1 Hektar (6000 tanaman)",
                "investment_costs": [{"item": "Benih Hibrida", "quantity": "6000 biji", "unit_price": 5000, "total": 30000000}, {"item": "Mulsa & Drip", "quantity": "1 ha", "unit_price": 15000000, "total": 15000000}],
                "annual_costs": [{"item": "Pupuk & Pestisida", "quantity": "Paket", "unit_price": 20000000, "total": 20000000}],
                "production_timeline": "Panen 60-70 hari, bisa 3-4 kali per tahun",
                "yield_potential": [{"year": "Per Musim", "yield_per_tree_kg": 2, "total_yield_kg": 12000, "price_per_kg": 15000}],
                "roi_notes": "ROI sangat cepat (2-3 bulan per siklus). Butuh modal besar, untung besar."
            }
        },
        "semangka": {
            "name": "Semangka",
            "scientific_name": "Citrullus lanatus",
            "icon": "🍉",
            "description": "Semangka adalah buah musiman dengan permintaan tinggi saat musim panas.",
            "varieties": ["Inul - Merah, manis", "Kuning - Daging kuning, segar", "Tanpa Biji - Premium, praktis"],
            "growing_requirements": {"altitude": "0-800 mdpl", "temperature": "25-32°C", "rainfall": "400-800 mm/tahun (irigasi)", "soil_ph": "5.5-7.0", "soil_type": "Berpasir, drainase sempurna"},
            "cultivation_guide": {
                "Pembibitan": ["Semai benih langsung di bedengan atau polybag", "Bibit siap tanam umur 7-10 hari"],
                "Penanaman": ["Jarak tanam 3x1 m (sistem bedengan)", "Gunakan mulsa plastik", "Bedengan tinggi 30 cm, lebar 1.5 m"],
                "Pemupukan": ["Pupuk dasar: Kompos 10 ton/ha + NPK 200 kg/ha", "Pupuk susulan: NPK tinggi K setiap 10 hari", "Kurangi pupuk N saat berbuah"],
                "Pemeliharaan": ["Pemangkasan tunas samping (opsional)", "Sisakan 2-3 buah per tanaman", "Penyiraman rutin, kurangi saat buah matang", "Balik buah secara berkala"]
            },
            "pests_diseases": {
                "Layu Bakteri": {"symptoms": "Tanaman layu, batang busuk", "control": "Rotasi tanaman, sanitasi"},
                "Kutu Daun": {"symptoms": "Daun keriting", "control": "Insektisida Imidakloprid"},
                "Antraknosa": {"symptoms": "Bercak pada buah", "control": "Fungisida Mankozeb"}
            },
            "harvest_postharvest": {"harvest_age": "65-75 hari setelah tanam", "harvest_signs": "Sulur dekat tangkai kering, suara plong saat diketuk", "postharvest": ["Panen pagi/sore hari", "Sortasi berdasarkan ukuran", "Simpan di tempat teduh, umur simpan 7-14 hari"]},
            "business_analysis": {
                "title": "Analisis Usaha Semangka per 1 Hektar (3000 tanaman)",
                "investment_costs": [{"item": "Benih", "quantity": "3000 biji", "unit_price": 2000, "total": 6000000}, {"item": "Mulsa", "quantity": "1 ha", "unit_price": 5000000, "total": 5000000}],
                "annual_costs": [{"item": "Pupuk & Pestisida", "quantity": "Paket", "unit_price": 12000000, "total": 12000000}],
                "production_timeline": "Panen 65-75 hari, bisa 2-3 kali per tahun",
                "yield_potential": [{"year": "Per Musim", "yield_per_tree_kg": 8, "total_yield_kg": 24000, "price_per_kg": 4000}],
                "roi_notes": "ROI cepat (2-3 bulan per siklus). Cocok untuk rotasi tanaman."
            }
        },
        "kelengkeng": {
            "name": "Kelengkeng",
            "scientific_name": "Dimocarpus longan",
            "icon": "🫒",
            "description": "Kelengkeng adalah buah premium dengan permintaan tinggi dan harga stabil.",
            "varieties": ["Diamond River - Manis, daging tebal", "Pingpong - Ukuran besar", "Itoh - Produktif, tahan penyakit"],
            "growing_requirements": {"altitude": "200-1000 mdpl", "temperature": "20-30°C", "rainfall": "1500-2500 mm/tahun", "soil_ph": "5.5-6.5", "soil_type": "Lempung dalam, drainase baik"},
            "cultivation_guide": {
                "Pembibitan": ["Gunakan bibit cangkok/sambung", "Bibit siap tanam umur 8-12 bulan"],
                "Penanaman": ["Jarak tanam 8x8 m atau 10x10 m", "Lubang 80x80x80 cm", "Pupuk kandang 30 kg + Dolomit 500g"],
                "Pemupukan": ["Tahun 1-3: NPK 2-4 kg/pohon/tahun", "Tahun 4+: NPK 8-12 kg/pohon/tahun", "Aplikasi 3-4 kali per tahun"],
                "Pemeliharaan": ["Pemangkasan cabang tidak produktif", "Penyiraman saat kemarau", "Induksi bunga dengan KClO3 (untuk varietas tertentu)"]
            },
            "pests_diseases": {
                "Penggerek Buah": {"symptoms": "Buah berlubang, busuk", "control": "Sanitasi, insektisida sistemik"},
                "Embun Jelaga": {"symptoms": "Lapisan hitam pada daun", "control": "Kendalikan kutu, fungisida"},
                "Kutu Loncat": {"symptoms": "Daun keriting", "control": "Insektisida Imidakloprid"}
            },
            "harvest_postharvest": {"harvest_age": "110-130 hari setelah bunga mekar", "harvest_signs": "Warna kulit coklat penuh, rasa manis optimal", "postharvest": ["Panen dengan gunting, sisakan tangkai", "Sortasi berdasarkan ukuran", "Simpan di ruang sejuk, umur simpan 7-10 hari"]},
            "business_analysis": {
                "title": "Analisis Usaha Kelengkeng per 1 Hektar (100 pohon)",
                "investment_costs": [{"item": "Bibit Cangkok", "quantity": "100 pohon", "unit_price": 100000, "total": 10000000}],
                "annual_costs": [{"item": "Pupuk & Perawatan", "quantity": "Paket", "unit_price": 8000000, "total": 8000000}],
                "production_timeline": "Mulai berbuah tahun ke-3, produktif penuh tahun ke-5",
                "yield_potential": [{"year": "Tahun 3", "yield_per_tree_kg": 20, "total_yield_kg": 2000, "price_per_kg": 25000}, {"year": "Tahun 5+", "yield_per_tree_kg": 60, "total_yield_kg": 6000, "price_per_kg": 25000}],
                "roi_notes": "ROI tahun ke-4. Umur ekonomis 20-30 tahun. Harga premium."
            }
        }
    }
    
    @staticmethod
    def get_fruit_list():
        """Get list of all available fruits."""
        return [
            {"id": key, "name": value["name"], "icon": value["icon"]}
            for key, value in FruitService.FRUIT_DATABASE.items()
        ]
    
    @staticmethod
    def get_fruit_info(fruit_id):
        """Get comprehensive information for specific fruit."""
        return FruitService.FRUIT_DATABASE.get(fruit_id)
