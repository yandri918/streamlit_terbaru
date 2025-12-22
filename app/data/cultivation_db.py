"""Comprehensive cultivation knowledge database for AgriSensa.

This module contains detailed cultivation guides for 17 commodities including:
- Vegetables (8): Tomat, Terung, Mentimun, Kangkung, Sawi, Selada, Bayam, Kubis
- Legumes (3): Kacang Tanah, Kedelai, Kacang Panjang
- Cucurbits (2): Melon, Semangka
- Tubers (1): Kentang
- Fruits (3): Stroberi, Buah Tin, Buah Naga

Each guide includes complete SOP and business analysis.
"""

def get_new_commodities():
    """Return dictionary of 17 new commodity cultivation guides."""
    return {
        'tomat': {
            "name": "Tomat (Solanum lycopersicum)",
            "icon": "🍅",
            "description": "Tomat adalah sayuran buah bernilai ekonomi tinggi dengan permintaan pasar yang stabil.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Buat bedengan tinggi 30-40 cm, lebar 100-120 cm untuk drainase optimal.",
                    "pH optimal 6.0-7.0. Jika pH <6.0, aplikasikan kapur Dolomit 1-2 ton/ha.",
                    "Aplikasi pupuk kandang matang 20-30 ton/ha 2 minggu sebelum tanam.",
                    "Pasang mulsa plastik hitam-perak untuk kontrol gulma dan penyakit tanah."
                ],
                "2. Pembibitan": [
                    "Media semai: tanah:kompos:arang sekam (1:1:1), sterilkan dengan fungisida.",
                    "Semai di tray 72 lubang atau polybag kecil.",
                    "Bibit siap tanam umur 25-30 hari (5-6 helai daun sejati, tinggi 15-20 cm).",
                    "Hardening off 3-5 hari sebelum pindah tanam."
                ],
                "3. Penanaman & Pemeliharaan": [
                    "Jarak tanam 60x50 cm atau 70x40 cm (populasi 33.000-40.000 tanaman/ha).",
                    "Tanam sore hari, siram segera setelah tanam.",
                    "Pasang ajir/turus setinggi 1.5-2 m pada 7-10 HST.",
                    "Pemangkasan: buang tunas air, sisakan 1-2 batang utama.",
                    "Penyiraman rutin pagi/sore, hindari genangan."
                ],
                "4. Pemupukan": [
                    "Pupuk dasar (saat tanam): 200 kg Urea/ha + 300 kg SP-36/ha + 150 kg KCl/ha.",
                    "Pemupukan susulan I (14 HST): 100 kg Urea/ha + 100 kg KCl/ha.",
                    "Pemupukan susulan II (28 HST): 100 kg Urea/ha + 150 kg KCl/ha.",
                    "Pemupukan susulan III (42 HST): 50 kg Urea/ha + 100 kg KCl/ha.",
                    "Kombinasi dengan NPK 16-16-16 (kocor 5 g/L setiap 10 hari)."
                ],
                "5. Panen & Pasca Panen": [
                    "Panen pertama 60-70 HST, panen berkala setiap 3-5 hari.",
                    "Kriteria panen: warna merah/oranye 70-80%, tekstur keras-kenyal.",
                    "Panen pagi hari (06.00-09.00) untuk kesegaran optimal.",
                    "Sortasi: buah utuh, bebas penyakit, seragam.",
                    "Simpan suhu ruang (1-2 hari) atau cold storage 10-12°C (7-10 hari)."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Tomat per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "3500 tanaman"},
                "costs": [
                    {"item": "Benih Hibrida", "amount": "100 gram", "cost": 800000},
                    {"item": "Pupuk Kandang", "amount": "2.5 ton", "cost": 2000000},
                    {"item": "Pupuk Anorganik", "amount": "Paket lengkap", "cost": 1500000},
                    {"item": "Mulsa & Ajir", "amount": "Paket", "cost": 800000},
                    {"item": "Pestisida", "amount": "5 bulan", "cost": 1500000},
                    {"item": "Tenaga Kerja", "amount": "5 bulan", "cost": 6000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 7000},
                    {"scenario": "Optimal", "total_yield_kg": 12000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 6000},
                    {"price_level": "Harga Normal", "price_per_kg": 10000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 15000}
                ]
            }
        },
        'kacang_tanah': {
            "name": "Kacang Tanah (Arachis hypogaea)",
            "icon": "🥜",
            "description": "Kacang tanah adalah tanaman legum penghasil minyak dan protein nabati bernilai ekonomi tinggi.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Olah tanah sedalam 20-30 cm hingga gembur.",
                    "Buat bedengan lebar 100-120 cm, tinggi 20-30 cm untuk drainase.",
                    "pH optimal 6.0-6.5. Jika asam, kapur 1-1.5 ton/ha.",
                    "Aplikasi pupuk kandang 1-2 ton/ha 2 minggu sebelum tanam.",
                    "Tanah berpasir/lempung berpasir terbaik untuk pembentukan polong."
                ],
                "2. Penanaman": [
                    "Gunakan benih bersertifikat varietas unggul (Hypoma 1, Kelinci, Bison).",
                    "Jarak tanam 40x15 cm atau 40x20 cm (2 biji/lubang).",
                    "Kedalaman tanam 3-5 cm, tutup tanah tipis.",
                    "Kebutuhan benih 80-100 kg/ha.",
                    "Tanam awal musim hujan atau dengan irigasi memadai."
                ],
                "3. Pemeliharaan": [
                    "Penyiangan I (15-20 HST) bersamaan dengan pembumbunan ringan.",
                    "Penyiangan II (35-40 HST) + pembumbunan untuk memberi ruang polong.",
                    "Pengairan: Kritis saat pembungaan (30-40 HST) dan pembentukan polong.",
                    "Hentikan air 10-14 hari sebelum panen untuk pengeringan polong.",
                    "Pengendalian hama penggerek polong dengan Trichogramma atau Bt."
                ],
                "4. Pemupukan": [
                    "Pupuk dasar saat tanam: 50 kg Urea/ha + 100 kg SP-36/ha + 50 kg KCl/ha.",
                    "Pupuk susulan (30 HST): 50 kg Urea/ha + 50 kg KCl/ha.",
                    "Kacang tanah bisa mengikat N dari udara (Rhizobium), jadi N sedang saja.",
                    "Aplikasi boron (Borax) 10 kg/ha untuk meningkatkan isi polong.",
                    "Kalsium penting: aplikasi kapur/gypsum 200-300 kg/ha saat berbunga."
                ],
                "5. Panen & Pasca Panen": [
                    "Umur panen 90-110 hari (varietas tergantung).",
                    "Kriteria panen: daun menguning 75%, polong keras, biji penuh.",
                    "Cabut tanaman pagi hari, biarkan kering angin 2-3 hari.",
                    "Rontokkan polong, jemur hingga kadar air 9-10%.",
                    "Simpan di tempat kering, hindari serangan jamur aflatoksin."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Kacang Tanah per 1 Hektar",
                "assumptions": {"Luas_Lahan": "1 hektar", "Populasi_Tanaman": "250,000 tanaman"},
                "costs": [
                    {"item": "Benih Bersertifikat", "amount": "90 kg", "cost": 1800000},
                    {"item": "Pupuk Kandang", "amount": "1.5 ton", "cost": 1200000},
                    {"item": "Pupuk Anorganik", "amount": "Urea 100kg, SP-36 100kg, KCl 100kg", "cost": 1000000},
                    {"item": "Kapur/Gypsum", "amount": "300 kg", "cost": 300000},
                    {"item": "Pestisida", "amount": "Paket 4 bulan", "cost": 800000},
                    {"item": "Tenaga Kerja", "amount": "Tanam, rawat, panen", "cost": 4000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 1500},
                    {"scenario": "Optimal", "total_yield_kg": 2500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 12000},
                    {"price_level": "Harga Normal", "price_per_kg": 16000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 22000}
                ]
            }
        },
        'kentang': {
            "name": "Kentang (Solanum tuberosum)",
            "icon": "🥔",
            "description": "Kentang adalah tanaman umbi bernilai tinggi, cocok dataran tinggi (>1000 mdpl).",
            "sop": {
                "1. Persiapan Lahan": [
                    "Kentang cocok dataran tinggi 1000-3000 mdpl, suhu 15-20°C.",
                    "Olah tanah dalam (30-40 cm), buat bedengan tinggi 30-40 cm.",
                    "pH optimal 5.0-6.0 (sedikit asam). Jika basa, aplikasikan sulfur.",
                    "Pupuk kandang matang 20-30 ton/ha campur dengan tanah bedengan.",
                    "Drainase sempurna sangat penting, hindari genangan."
                ],
                "2. Persiapan Bibit & Penanaman": [
                    "Gunakan umbi bibit bersertifikat G3/G4 (Granola, Atlantik, Medians).",
                    "Potong umbi besar jadi 2-4 bagian (min 30 g/potong, ada mata tunas).",
                    "Jemur potongan 1-2 hari, celup fungisida sebelum tanam.",
                    "Jarak tanam 70x30 cm atau 60x40 cm (populasi 47.000-55.000/ha).",
                    "Tanam sedalam 10-15 cm, tutup tanah dan mulsa."
                ],
                "3. Pemeliharaan": [
                    "Pembumbunan pertama 21 HST, kedua 42 HST (penting untuk umbi).",
                    "Penyiraman teratur, jaga kelembaban 70-80%, hindari kering/becek.",
                    "Pengendalian penyakit (late blight, early blight) dengan fungisida preventif.",
                    "Roguing tanaman sakit virus segera untuk cegah penyebaran.",
                    "Aplikasi ZPT (Rootone, Gandasil) untuk merangsang pembentukan umbi."
                ],
                "4. Pemupukan": [
                    "Pupuk dasar: 200 kg Urea/ha + 400 kg SP-36/ha + 200 kg KCl/ha.",
                    "Pupuk susulan I (21 HST): 150 kg Urea/ha + 100 kg KCl/ha.",
                    "Pupuk susulan II (42 HST): 100 kg Urea/ha + 150 kg KCl/ha.",
                    "Kalium tinggi penting untuk kualitas umbi dan ketahanan simpan.",
                    "Aplikasi unsur mikro (Zn, B) via semprot daun setiap 14 hari."
                ],
                "5. Panen & Pasca Panen": [
                    "Umur panen 90-120 hari (tergantung varietas).",
                    "Kriteria: 75-90% daun menguning, kulit umbi keras.",
                    "Hentikan air 10 hari sebelum panen untuk pengerasan kulit.",
                    "Panen pagi/sore, hindari luka mekanis pada umbi.",
                    "Curing (pelukaan kulit): angin-anginkan 3-5 hari di tempat gelap.",
                    "Simpan suhu 4-10°C, RH 85-90%, hindari cahaya (cegah solanin)."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Kentang per 1 Hektar",
                "assumptions": {"Luas_Lahan": "1 hektar", "Populasi_Tanaman": "50,000 tanaman"},
                "costs": [
                    {"item": "Bibit Umbi G3/G4", "amount": "1.5-2 ton", "cost": 12000000},
                    {"item": "Pupuk Kandang", "amount": "25 ton", "cost": 5000000},
                    {"item": "Pupuk Anorganik", "amount": "Urea 450kg, SP-36 400kg, KCl 450kg", "cost": 3500000},
                    {"item": "Pestisida & Fungisida", "amount": "4 bulan intensif", "cost": 3000000},
                    {"item": "Mulsa", "amount": "Paket", "cost": 1500000},
                    {"item": "Tenaga Kerja", "amount": "Tanam, rawat, panen", "cost": 8000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 15000},
                    {"scenario": "Optimal", "total_yield_kg": 25000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 7000},
                    {"price_level": "Harga Normal", "price_per_kg": 10000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 15000}
                ]
            }
        },
        'buah_naga': {
            "name": "Buah Naga (Hylocereus undatus)",
            "icon": "🐉",
            "description": "Buah naga adalah tanaman kaktus buah bernilai tinggi dengan permintaan ekspor yang baik.",
            "sop": {
                "1. Persiapan Lahan & Tiang Panjat": [
                    "Cocok dataran rendah-menengah (0-1000 mdpl), suhu 26-36°C.",
                    "Buat lubang tanam 60x60x60 cm, jarak 3x2.5 m atau 2.5x2.5 m.",
                    "pH optimal 6.0-7.0, tanah gembur, drainase baik (tahan kering, takut becek).",
                    "Pasang tiang panjat beton/kayu keras tinggi 2-2.5 m per titik tanam.",
                    "Buat ring/ban bekas di puncak tiang untuk tempat sulur menyebar."
                ],
                "2. Pembibitan & Penanaman": [
                    "Bibit dari stek batang (30-40 cm), keringkan 3-5 hari sebelum tanam.",
                    "Tanam stek 10-15 cm dalam tanah, ikat longgar ke tiang panjat.",
                    "Umur bibit siap panen pertama 10-12 bulan setelah tanam.",
                    "Populasi 1300-1600 tanaman/ha.",
                    "Aplikasi pupuk kandang 10-15 kg/lubang saat tanam."
                ],
                "3. Pemeliharaan": [
                    "Pemangkasan: potong cabang sakit/kering, bentuk tajuk payung.",
                    "Ikat sulur ke tiang secara teratur agar tidak roboh.",
                    "Penyiraman: Intensif fase vegetatif, kurangi saat berbunga (stress air = rangsang bunga).",
                    "Sanitasi: buang bunga/buah busuk, jaga kebersihan areal.",
                    "Mulsa jerami/plastik untuk kontrol gulma dan jaga kelembaban."
                ],
                "4. Pemupukan": [
                    "Pupuk dasar (tanam): 10-15 kg pupuk kandang/tanaman.",
                    "Fase vegetatif (0-8 bulan): NPK tinggi N (25-7-7) 50 g/tanaman/bulan.",
                    "Fase berbunga & berbuah: NPK seimbang (16-16-16) atau 15-15-15, 100 g/tanaman/bulan.",
                    "Aplikasi KNO3 (0.5-1%) semprot untuk rangsang pembungaan.",
                    "Pupuk organik cair/kompos setiap 3 bulan untuk kualitas buah."
                ],
                "5. Panen & Pasca Panen": [
                    "Panen pertama 10-12 bulan, panen rutin setiap bulan setelahnya.",
                    "Kriteria: warna merah/merah muda merata, jumbai layu, 30-35 hari setelah bunga.",
                    "Panen pagi/sore dengan gunting, sisakan tangkai 2-3 cm.",
                    "Sortasi: buah mulus, berat min 350-400 g, bebas cacat.",
                    "Simpan suhu ruang 3-5 hari atau cold storage 10-12°C (2 minggu).",
                    "Potensi hasil 1-1.5 kg/tanaman/bulan atau 15-20 ton/ha/tahun."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Buah Naga per 1000 m² (Tahun Ke-2 dan seterusnya)",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "150 tanaman"},
                "costs": [
                    {"item": "Bibit Stek (investasi awal tahun 1)", "amount": "150 stek", "cost": 3000000},
                    {"item": "Tiang Panjat (investasi awal)", "amount": "150 tiang beton", "cost": 7500000},
                    {"item": "Pupuk Kandang & Anorganik", "amount": "Tahunan", "cost": 3000000},
                    {"item": "Pestisida & Fungisida", "amount": "Tahunan", "cost": 1500000},
                    {"item": "Tenaga Kerja", "amount": "Pemeliharaan & panen", "cost": 6000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif (tahun ke-2+)", "total_yield_kg": 2000},
                    {"scenario": "Optimal (tahun ke-3+)", "total_yield_kg": 3500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 15000},
                    {"price_level": "Harga Normal", "price_per_kg": 25000},
                    {"price_level": "Harga Tinggi (ekspor)", "price_per_kg": 40000}
                ]
            }
        },
        'terung': {
            "name": "Terung (Solanum melongena)",
            "icon": "🍆",
            "description": "Terung adalah sayuran buah yang populer di masakan Asia.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan tinggi 30-40 cm, lebar 100-120 cm, pH 6.0-6.8.",
                    "Aplikasi pupuk kandang 20 ton/ha 2 minggu sebelum tanam.",
                    "Pasang mulsa plastik hitam untuk kontrol gulma."
                ],
                "2. Pembibitan": [
                    "Semai dalam tray dengan media tanah:kompos:arang sekam (1:1:1).",
                    "Bibit siap tanam umur 25-30 hari, tinggi 15-20 cm.",
                    "Hardening off 3-5 hari sebelum penanaman lapangan."
                ],
                "3. Penanaman & Pemeliharaan": [
                    "Jarak tanam 60x45 cm (populasi ~35.000 tanaman/ha).",
                    "Tanam sore hari, siram segera.",
                    "Pasang ajir setinggi 1.5 m pada 7-10 HST.",
                    "Pemangkasan tunas samping, sisakan 2-3 batang utama.",
                    "Penyiraman rutin, hindari genangan."
                ],
                "4. Pemupukan": [
                    "Pupuk dasar: 150 kg Urea/ha + 200 kg SP-36/ha + 100 kg KCl/ha.",
                    "Pemupukan susulan I (14 HST): 80 kg Urea/ha + 80 kg KCl/ha.",
                    "Pemupukan susulan II (28 HST): 80 kg Urea/ha + 80 kg KCl/ha.",
                    "Aplikasi NPK 16-16-16 5 g/L tiap 10 hari."
                ],
                "5. Panen & Pasca Panen": [
                    "Panen 60-70 HST, buah berukuran 10-15 cm, kulit mengkilap.",
                    "Sortasi buah tanpa cacat, simpan pada suhu 12-15°C.",
                    "Penyimpanan maksimal 7 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Terung per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "3500 tanaman"},
                "costs": [
                    {"item": "Benih Terung", "amount": "100 gram", "cost": 600000},
                    {"item": "Pupuk Kandang", "amount": "2 ton", "cost": 1500000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 1200000},
                    {"item": "Mulsa & Ajir", "amount": "Paket", "cost": 500000},
                    {"item": "Tenaga Kerja", "amount": "5 bulan", "cost": 4000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 5000},
                    {"scenario": "Optimal", "total_yield_kg": 8000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 8000},
                    {"price_level": "Harga Normal", "price_per_kg": 12000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 18000}
                ]
            }
        },
        'mentimun': {
            "name": "Mentimun (Cucumis sativus)",
            "icon": "🥒",
            "description": "Mentimun adalah sayuran segar yang banyak dikonsumsi mentah atau dalam acar.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 30-40 cm, lebar 100-120 cm, pH 6.0-6.5.",
                    "Aplikasi pupuk kandang 15 ton/ha.",
                    "Pasang mulsa plastik transparan untuk menjaga kelembaban."
                ],
                "2. Pembibitan": [
                    "Semai dalam tray dengan media tanah:kompos (1:1).",
                    "Bibit siap tanam 20-25 hari, tinggi 10-15 cm.",
                    "Hardening off 2-3 hari."
                ],
                "3. Penanaman & Pemeliharaan": [
                    "Jarak tanam 30x30 cm (populasi ~110.000 tanaman/ha).",
                    "Tanam pagi hari, siram langsung.",
                    "Pasang ajir setinggi 1 m.",
                    "Pemangkasan tunas samping untuk sirkulasi udara.",
                    "Penyiraman teratur, hindari overwatering."
                ],
                "4. Pemupukan": [
                    "Pupuk dasar: 100 kg Urea/ha + 150 kg SP-36/ha + 80 kg KCl/ha.",
                    "Pemupukan susulan I (14 HST): 60 kg Urea/ha + 60 kg KCl/ha.",
                    "Pemupukan susulan II (28 HST): 60 kg Urea/ha + 60 kg KCl/ha.",
                    "Aplikasi NPK 16-16-16 4 g/L tiap 10 hari."
                ],
                "5. Panen & Pasca Panen": [
                    "Panen 45-55 HST, panjang buah 15-20 cm, kulit hijau mengkilap.",
                    "Sortasi buah tanpa noda, simpan pada suhu 10-12°C.",
                    "Maksimum penyimpanan 5 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Mentimun per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "11000 tanaman"},
                "costs": [
                    {"item": "Benih Mentimun", "amount": "150 gram", "cost": 500000},
                    {"item": "Pupuk Kandang", "amount": "1.5 ton", "cost": 1200000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 1000000},
                    {"item": "Mulsa", "amount": "Paket", "cost": 400000},
                    {"item": "Tenaga Kerja", "amount": "5 bulan", "cost": 3500000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 4000},
                    {"scenario": "Optimal", "total_yield_kg": 6500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 7000},
                    {"price_level": "Harga Normal", "price_per_kg": 10000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 15000}
                ]
            }
        },
        'kangkung': {
            "name": "Kangkung (Ipomoea aquatica)",
            "icon": "🥬",
            "description": "Kangkung adalah sayuran air yang tumbuh cepat dan populer di Asia Tenggara.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 20-30 cm, pH 6.0-6.5, tanah gembur.",
                    "Aplikasi pupuk kandang 10 ton/ha.",
                    "Siapkan aliran air mengalir terus-menerus."
                ],
                "2. Penanaman": [
                    "Tanam stek 30-40 cm, kedalaman 5 cm.",
                    "Jarak tanam 20x20 cm.",
                    "Siram langsung setelah tanam."
                ],
                "3. Pemeliharaan": [
                    "Penyiraman terus-menerus, pastikan air tidak tergenang.",
                    "Pemupukan susulan tiap 2 minggu dengan NPK 15-15-15.",
                    "Pengendalian hama (kutang) dengan insektisida organik bila diperlukan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 25-30 hari setelah tanam, tinggi 30-40 cm.",
                    "Potong bagian atas tanaman, sisakan akar untuk regrowth.",
                    "Cuci bersih, simpan pada suhu 4-6°C, maksimal 3 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Kangkung per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "5000 tanaman"},
                "costs": [
                    {"item": "Stek Kangkung", "amount": "200 gram", "cost": 300000},
                    {"item": "Pupuk Kandang", "amount": "1 ton", "cost": 800000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 600000},
                    {"item": "Tenaga Kerja", "amount": "2 bulan", "cost": 1500000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 2500},
                    {"scenario": "Optimal", "total_yield_kg": 4000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 5000},
                    {"price_level": "Harga Normal", "price_per_kg": 8000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 12000}
                ]
            }
        },
        'sawi': {
            "name": "Sawi (Brassica rapa)",
            "icon": "🥬",
            "description": "Sawi adalah sayuran daun yang cepat tumbuh dan serbaguna.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 20-30 cm, pH 6.0-6.5, tambahkan kompos.",
                    "Aplikasi pupuk kandang 12 ton/ha.",
                    "Pastikan drainase baik."
                ],
                "2. Penanaman": [
                    "Sebar benih langsung atau tanam bibit 5-7 cm dalam.",
                    "Jarak tanam 20x20 cm.",
                    "Sirami setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 15-15-15 tiap 2 minggu.",
                    "Pengendalian hama kutu daun dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 30-45 hari setelah tanam, daun berukuran 15-20 cm.",
                    "Potong daun bagian atas, sisakan akar untuk regrowth.",
                    "Cuci bersih, simpan pada suhu 4-6°C, maksimal 5 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Sawi per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "6000 tanaman"},
                "costs": [
                    {"item": "Benih Sawi", "amount": "150 gram", "cost": 400000},
                    {"item": "Pupuk Kandang", "amount": "1.2 ton", "cost": 900000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 700000},
                    {"item": "Tenaga Kerja", "amount": "2 bulan", "cost": 1300000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 3000},
                    {"scenario": "Optimal", "total_yield_kg": 5000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 6000},
                    {"price_level": "Harga Normal", "price_per_kg": 9000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 13000}
                ]
            }
        },
        'selada': {
            "name": "Selada (Lactuca sativa)",
            "icon": "🥬",
            "description": "Selada adalah sayuran daun yang populer untuk salad.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 15-20 cm, pH 6.0-6.5, tambahkan kompos.",
                    "Aplikasi pupuk kandang 8 ton/ha.",
                    "Pastikan drainase baik."
                ],
                "2. Penanaman": [
                    "Sebar benih secara merata, tutup tipis dengan tanah.",
                    "Jarak tanam 20x20 cm.",
                    "Sirami lembut setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 15-15-15 tiap 2 minggu.",
                    "Pengendalian hama kutu daun dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 30-45 hari setelah tanam, daun berukuran 15-20 cm.",
                    "Potong bagian luar, sisakan inti untuk pertumbuhan lanjutan.",
                    "Cuci bersih, simpan pada suhu 4-6°C, maksimal 7 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Selada per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "8000 tanaman"},
                "costs": [
                    {"item": "Benih Selada", "amount": "200 gram", "cost": 350000},
                    {"item": "Pupuk Kandang", "amount": "0.8 ton", "cost": 600000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 500000},
                    {"item": "Tenaga Kerja", "amount": "2 bulan", "cost": 1200000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 2500},
                    {"scenario": "Optimal", "total_yield_kg": 4000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 5000},
                    {"price_level": "Harga Normal", "price_per_kg": 8000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 12000}
                ]
            }
        },
        'bayam': {
            "name": "Bayam (Spinacia oleracea)",
            "icon": "🥬",
            "description": "Bayam adalah sayuran daun hijau kaya zat besi.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 15-20 cm, pH 6.0-6.8, tambahkan kompos.",
                    "Aplikasi pupuk kandang 10 ton/ha.",
                    "Pastikan drainase baik."
                ],
                "2. Penanaman": [
                    "Sebar benih tipis, tutup tipis dengan tanah.",
                    "Jarak tanam 20x20 cm.",
                    "Sirami lembut setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 15-15-15 tiap 2 minggu.",
                    "Pengendalian hama kutu daun dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 30-40 hari setelah tanam, daun berukuran 10-15 cm.",
                    "Potong bagian atas, sisakan akar untuk regrowth.",
                    "Cuci bersih, simpan pada suhu 4-6°C, maksimal 5 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Bayam per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "7000 tanaman"},
                "costs": [
                    {"item": "Benih Bayam", "amount": "180 gram", "cost": 300000},
                    {"item": "Pupuk Kandang", "amount": "1 ton", "cost": 800000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 600000},
                    {"item": "Tenaga Kerja", "amount": "2 bulan", "cost": 1300000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 2800},
                    {"scenario": "Optimal", "total_yield_kg": 4500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 6000},
                    {"price_level": "Harga Normal", "price_per_kg": 9000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 13000}
                ]
            }
        },
        'kubis': {
            "name": "Kubis (Brassica oleracea var. capitata)",
            "icon": "🥬",
            "description": "Kubis adalah sayuran kepala yang tahan lama dan serbaguna.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 30-40 cm, pH 6.0-6.5, tambahkan kompos.",
                    "Aplikasi pupuk kandang 15 ton/ha.",
                    "Pastikan drainase baik."
                ],
                "2. Penanaman": [
                    "Tanam bibit 5-7 cm dalam, jarak 45x45 cm.",
                    "Sirami setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 16-16-16 tiap 3 minggu.",
                    "Pengendalian hama kutu daun dan ulat dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 80-100 hari setelah tanam, kepala berat 1-2 kg.",
                    "Potong bagian bawah batang, bersihkan daun luar.",
                    "Simpan pada suhu 0-4°C, maksimal 2 minggu."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Kubis per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "2500 tanaman"},
                "costs": [
                    {"item": "Bibit Kubis", "amount": "250 gram", "cost": 400000},
                    {"item": "Pupuk Kandang", "amount": "1.5 ton", "cost": 900000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 800000},
                    {"item": "Tenaga Kerja", "amount": "3 bulan", "cost": 2000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 3000},
                    {"scenario": "Optimal", "total_yield_kg": 5000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 7000},
                    {"price_level": "Harga Normal", "price_per_kg": 11000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 15000}
                ]
            }
        },
        'kedelai': {
            "name": "Kedelai (Glycine max)",
            "icon": "🌱",
            "description": "Kedelai adalah legum penting untuk produksi kedelai dan tempe.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 20-30 cm, pH 6.0-6.5, tambahkan kompos.",
                    "Aplikasi pupuk kandang 12 ton/ha.",
                    "Pastikan drainase baik."
                ],
                "2. Penanaman": [
                    "Tanam benih 3-5 cm dalam, jarak 30x10 cm.",
                    "Kebutuhan benih 80-100 kg/ha.",
                    "Sirami setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 15-15-15 tiap 3 minggu.",
                    "Pengendalian hama kutu daun dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 90-110 hari setelah tanam, biji matang berwarna kuning.",
                    "Rontokkan tanaman, keringkan 2-3 hari.",
                    "Simpan biji pada suhu 15°C, RH 65%, maksimal 6 bulan."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Kedelai per 1 Hektar",
                "assumptions": {"Luas_Lahan": "1 hektar", "Populasi_Tanaman": "300,000 tanaman"},
                "costs": [
                    {"item": "Benih Kedelai", "amount": "120 kg", "cost": 1500000},
                    {"item": "Pupuk Kandang", "amount": "2 ton", "cost": 1200000},
                    {"item": "Pupuk Anorganik", "amount": "Urea 150kg, SP-36 150kg, KCl 150kg", "cost": 1300000},
                    {"item": "Tenaga Kerja", "amount": "Tanam, rawat, panen", "cost": 5000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 1500},
                    {"scenario": "Optimal", "total_yield_kg": 2500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 12000},
                    {"price_level": "Harga Normal", "price_per_kg": 16000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 22000}
                ]
            }
        },
        'kacang_panjang': {
            "name": "Kacang Panjang (Vigna unguiculata)",
            "icon": "🌱",
            "description": "Kacang panjang adalah sayuran polong yang populer di masakan Asia.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 20-30 cm, pH 6.0-6.5, tambahkan kompos.",
                    "Aplikasi pupuk kandang 10 ton/ha.",
                    "Pastikan drainase baik."
                ],
                "2. Penanaman": [
                    "Tanam biji 2-3 cm dalam, jarak 30x10 cm.",
                    "Kebutuhan benih 60-80 kg/ha.",
                    "Sirami setelah penanaman.",
                    "Jaga gulma."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 15-15-15 tiap 2 minggu.",
                    "Pengendalian hama kutu daun dan ulat dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 60-70 hari setelah tanam, polong panjang 30-40 cm.",
                    "Potong polong dengan gunting, hindari merobek tanaman.",
                    "Simpan pada suhu 4-6°C, maksimal 5 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Kacang Panjang per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "12000 tanaman"},
                "costs": [
                    {"item": "Benih Kacang Panjang", "amount": "150 gram", "cost": 400000},
                    {"item": "Pupuk Kandang", "amount": "1 ton", "cost": 800000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 600000},
                    {"item": "Tenaga Kerja", "amount": "2 bulan", "cost": 1500000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 2000},
                    {"scenario": "Optimal", "total_yield_kg": 3500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 8000},
                    {"price_level": "Harga Normal", "price_per_kg": 12000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 18000}
                ]
            }
        },
        'melon': {
            "name": "Melon (Cucumis melo)",
            "icon": "🍈",
            "description": "Melon adalah buah musiman yang manis dan berair.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 30-40 cm, pH 6.0-6.5, tambahkan kompos.",
                    "Aplikasi pupuk kandang 20 ton/ha.",
                    "Pasang mulsa plastik hitam."
                ],
                "2. Penanaman": [
                    "Tanam bibit 30-40 cm dalam, jarak 150x150 cm.",
                    "Sirami setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 16-16-16 tiap 4 minggu.",
                    "Pengendalian hama kutu daun dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 90-110 hari setelah tanam, kulit menguning, aroma harum.",
                    "Potong buah dengan pisau bersih, hindari memotong batang.",
                    "Simpan pada suhu 10-12°C, maksimal 7 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Melon per 1 Hektar",
                "assumptions": {"Luas_Lahan": "1 hektar", "Populasi_Tanaman": "400 tanaman"},
                "costs": [
                    {"item": "Bibit Melon", "amount": "400 buah", "cost": 2000000},
                    {"item": "Pupuk Kandang", "amount": "3 ton", "cost": 1500000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 1200000},
                    {"item": "Tenaga Kerja", "amount": "Tanam, rawat, panen", "cost": 2500000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 5000},
                    {"scenario": "Optimal", "total_yield_kg": 8000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 15000},
                    {"price_level": "Harga Normal", "price_per_kg": 20000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 30000}
                ]
            }
        },
        'semangka': {
            "name": "Semangka (Citrullus lanatus)",
            "icon": "🍉",
            "description": "Semangka adalah buah segar berair yang populer di musim panas.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 30-40 cm, pH 6.0-6.5, tambahkan kompos.",
                    "Aplikasi pupuk kandang 25 ton/ha.",
                    "Pasang mulsa plastik hitam."
                ],
                "2. Penanaman": [
                    "Tanam bibit 30-40 cm dalam, jarak 150x150 cm.",
                    "Sirami setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 16-16-16 tiap 4 minggu.",
                    "Pengendalian hama kutu daun dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 80-100 hari setelah tanam, kulit menguning, suara tembus.",
                    "Potong buah dengan pisau bersih, hindari memotong batang.",
                    "Simpan pada suhu 10-12°C, maksimal 10 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Semangka per 1 Hektar",
                "assumptions": {"Luas_Lahan": "1 hektar", "Populasi_Tanaman": "500 tanaman"},
                "costs": [
                    {"item": "Bibit Semangka", "amount": "500 buah", "cost": 2500000},
                    {"item": "Pupuk Kandang", "amount": "3 ton", "cost": 1500000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 1300000},
                    {"item": "Tenaga Kerja", "amount": "Tanam, rawat, panen", "cost": 2600000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 4000},
                    {"scenario": "Optimal", "total_yield_kg": 7000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 12000},
                    {"price_level": "Harga Normal", "price_per_kg": 17000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 25000}
                ]
            }
        },
        'stroberi': {
            "name": "Stroberi (Fragaria × ananassa)",
            "icon": "🍓",
            "description": "Stroberi adalah buah beri manis yang populer untuk konsumsi segar dan olahan.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 20-30 cm, pH 5.5-6.5, tambahkan kompos.",
                    "Aplikasi pupuk kandang 8 ton/ha.",
                    "Pasang mulsa plastik hitam."
                ],
                "2. Penanaman": [
                    "Tanam stolon (runners) 30 cm antar tanaman, jarak 30x30 cm.",
                    "Sirami setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 15-15-15 tiap 3 minggu.",
                    "Pengendalian hama kutu daun dan jamur dengan insektisida/fungisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 60-70 hari setelah tanam, buah merah matang.",
                    "Petik buah dengan hati-hati, hindari merusak tanaman.",
                    "Simpan pada suhu 0-2°C, maksimal 5 hari."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Stroberi per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "1500 tanaman"},
                "costs": [
                    {"item": "Stolon Stroberi", "amount": "1500 buah", "cost": 2500000},
                    {"item": "Pupuk Kandang", "amount": "0.8 ton", "cost": 900000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 800000},
                    {"item": "Tenaga Kerja", "amount": "3 bulan", "cost": 3000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 2000},
                    {"scenario": "Optimal", "total_yield_kg": 3500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 25000},
                    {"price_level": "Harga Normal", "price_per_kg": 35000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 50000}
                ]
            }
        },
        'buah_tin': {
            "name": "Buah Tin (Ficus carica)",
            "icon": "🍐",
            "description": "Buah tin adalah buah manis yang dapat dimakan segar atau dikeringkan.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan 30-40 cm, pH 6.0-7.0, tambahkan kompos.",
                    "Aplikasi pupuk kandang 10 ton/ha.",
                    "Tanam di area dengan sinar matahari penuh."
                ],
                "2. Penanaman": [
                    "Tanam bibit 1-2 m tinggi, jarak 4x4 m.",
                    "Sirami setelah penanaman."
                ],
                "3. Pemeliharaan": [
                    "Pemupukan susulan NPK 16-16-16 tiap 6 bulan.",
                    "Pengendalian hama kutu daun dengan insektisida organik bila diperlukan.",
                    "Penyiraman teratur, hindari genangan."
                ],
                "4. Panen & Pasca Panen": [
                    "Panen 2-3 tahun setelah penanaman, buah matang berwarna coklat keunguan.",
                    "Petik buah dengan tangan, hindari memotong batang.",
                    "Simpan pada suhu ruang atau keringkan untuk tin kering."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Buah Tin per 1 Hektar",
                "assumptions": {"Luas_Lahan": "1 hektar", "Populasi_Tanaman": "150 pohon"},
                "costs": [
                    {"item": "Bibit Tin", "amount": "150 pohon", "cost": 3000000},
                    {"item": "Pupuk Kandang", "amount": "2 ton", "cost": 1200000},
                    {"item": "Pupuk Anorganik", "amount": "Paket", "cost": 1000000},
                    {"item": "Tenaga Kerja", "amount": "Pemeliharaan & panen", "cost": 2500000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 5000},
                    {"scenario": "Optimal", "total_yield_kg": 9000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Harga Rendah", "price_per_kg": 15000},
                    {"price_level": "Harga Normal", "price_per_kg": 25000},
                    {"price_level": "Harga Tinggi", "price_per_kg": 35000}
                ]
            }
        },
        'wortel': {
            "name": "Wortel (Daucus carota)",
            "icon": "🥕",
            "description": "Wortel adalah sayuran umbi kaya vitamin A yang populer.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Tanah gembur, subur, drainase baik, pH 5.5-6.5.",
                    "Cangkul tanah sedalam 30-40 cm, buang batu/kerikil agar umbi lurus.",
                    "Bedengan lebar 100-120 cm, tinggi 20-30 cm.",
                    "Pupuk kandang 15-20 ton/ha, campur rata."
                ],
                "2. Penanaman": [
                    "Benih langsung disebar atau dilarik (jarak larikan 20 cm).",
                    "Campur benih dengan pasir halus agar sebaran merata.",
                    "Tutup tanah tipis 0.5-1 cm.",
                    "Siram perlahan agar benih tidak hanyut."
                ],
                "3. Pemeliharaan": [
                    "Penjarangan tanaman pada umur 2-3 minggu, jarak antar tanaman 5-8 cm.",
                    "Penyiangan gulma sangat penting di awal pertumbuhan.",
                    "Pembumbunan bersamaan dengan penyiangan.",
                    "Penyiraman rutin, tanah harus selalu lembab tapi tidak becek."
                ],
                "4. Pemupukan": [
                    "Pupuk dasar: Urea 50 kg, SP-36 100 kg, KCl 50 kg per ha.",
                    "Susulan (1 bulan): Urea 50 kg, KCl 50 kg per ha.",
                    "Hindari N berlebihan agar umbi tidak pecah/bercabang."
                ],
                "5. Panen": [
                    "Panen umur 3-4 bulan tergantung varietas.",
                    "Cabut umbi dengan hati-hati, potong daun.",
                    "Cuci bersih dan sortasi berdasarkan ukuran."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Wortel per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "Populasi rapat"},
                "costs": [
                    {"item": "Benih", "amount": "500 gr", "cost": 800000},
                    {"item": "Pupuk Kandang", "amount": "2 ton", "cost": 1500000},
                    {"item": "Pupuk Kimia", "amount": "Paket", "cost": 600000},
                    {"item": "Tenaga Kerja", "amount": "Borongan", "cost": 2500000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 2000},
                    {"scenario": "Optimal", "total_yield_kg": 3500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Rendah", "price_per_kg": 3000},
                    {"price_level": "Normal", "price_per_kg": 5000},
                    {"price_level": "Tinggi", "price_per_kg": 8000}
                ]
            }
        },
        'brokoli': {
            "name": "Brokoli (Brassica oleracea var. italica)",
            "icon": "🥦",
            "description": "Brokoli adalah sayuran bunga bernilai tinggi, cocok dataran tinggi.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Cocok di dataran tinggi >800 mdpl, suhu dingin.",
                    "Bedengan lebar 100 cm, pH 6.0-7.0 (kapur jika asam).",
                    "Pupuk kandang 20 ton/ha."
                ],
                "2. Persemaian": [
                    "Semai di tray/polybag, media tanah:kompos 1:1.",
                    "Pindah tanam umur 3-4 minggu (3-4 daun)."
                ],
                "3. Penanaman": [
                    "Jarak tanam 50x50 cm atau 60x50 cm.",
                    "Tanam sore hari, padatkan tanah sekitar akar."
                ],
                "4. Pemeliharaan": [
                    "Penyiraman rutin.",
                    "Perempelan tunas samping.",
                    "Pengendalian ulat (Plutella, Crocidolomia) sangat intensif."
                ],
                "5. Panen": [
                    "Panen 60-70 HST saat bunga padat dan hijau tua.",
                    "Potong tangkai bunga bersama daun pelindung.",
                    "Segera dinginkan/simpan sejuk."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Brokoli per 1000 m²",
                "assumptions": {"Luas_Lahan": "1000 m²", "Populasi_Tanaman": "3000 tanaman"},
                "costs": [
                    {"item": "Benih Hibrida", "amount": "2 sachet", "cost": 400000},
                    {"item": "Pupuk & Obat", "amount": "Paket", "cost": 2000000},
                    {"item": "Tenaga Kerja", "amount": "Intensif", "cost": 3000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 1000},
                    {"scenario": "Optimal", "total_yield_kg": 1500}
                ],
                "revenue_scenarios": [
                    {"price_level": "Rendah", "price_per_kg": 8000},
                    {"price_level": "Normal", "price_per_kg": 15000},
                    {"price_level": "Tinggi", "price_per_kg": 25000}
                ]
            }
        },
        'pisang': {
            "name": "Pisang (Musa paradisiaca)",
            "icon": "🍌",
            "description": "Pisang adalah buah tropis populer, sumber energi dan kalium.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Lubang tanam 50x50x50 cm, jarak 3x3 m.",
                    "Isi lubang dengan pupuk kandang 10-20 kg, biarkan 2 minggu."
                ],
                "2. Penanaman": [
                    "Gunakan bibit bonggol atau kultur jaringan bebas penyakit (layu fusarium/darah).",
                    "Tanam tegak, tutup tanah sebatas leher akar."
                ],
                "3. Pemeliharaan": [
                    "Penjarangan anakan: sisakan 1 induk + 1-2 anakan beda umur.",
                    "Sanitasi daun kering.",
                    "Pembungkusan buah (brongsong) saat sisir terakhir muncul.",
                    "Potong jantung pisang setelah buah terbentuk lengkap."
                ],
                "4. Pemupukan": [
                    "3 bulan sekali: Urea, SP-36, KCl (200g, 100g, 200g per rumpun).",
                    "Tambahkan pupuk organik setahun sekali."
                ],
                "5. Panen": [
                    "Panen 3-4 bulan setelah berbunga.",
                    "Buah tumpul, siku hilang.",
                    "Tandan dipotong, jangan jatuhkan buah."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Pisang per 1 Hektar",
                "assumptions": {"Luas_Lahan": "1 Ha", "Populasi_Tanaman": "1000 rumpun"},
                "costs": [
                    {"item": "Bibit", "amount": "1000 btg", "cost": 10000000},
                    {"item": "Pupuk", "amount": "Per tahun", "cost": 5000000},
                    {"item": "Tenaga Kerja", "amount": "Per tahun", "cost": 6000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 15000},
                    {"scenario": "Optimal", "total_yield_kg": 25000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Rendah", "price_per_kg": 2000},
                    {"price_level": "Normal", "price_per_kg": 3500},
                    {"price_level": "Tinggi", "price_per_kg": 5000}
                ]
            }
        },
        'pepaya': {
            "name": "Pepaya (Carica papaya)",
            "icon": "🥭",
            "description": "Pepaya (California/Calina) cepat berbuah dan menguntungkan.",
            "sop": {
                "1. Persiapan Lahan": [
                    "Bedengan lebar 1-1.5 m, tinggi 30-40 cm (sangat tidak tahan genangan).",
                    "Jarak tanam 2.5x2.5 m.",
                    "Pupuk kandang 10-20 kg/lubang."
                ],
                "2. Penanaman": [
                    "Bibit umur 1.5-2 bulan (polybag).",
                    "Tanam sore hari."
                ],
                "3. Pemeliharaan": [
                    "Penyiraman penting di musim kemarau.",
                    "Penyiangan piringan akar.",
                    "Seleksi bunga/buah (penjarangan) jika terlalu lebat."
                ],
                "4. Pemupukan": [
                    "N, P, K, Mg rutin setiap 2-3 bulan.",
                    "Boron penting untuk kualitas buah."
                ],
                "5. Panen": [
                    "Mulai panen umur 7-8 bulan.",
                    "Petik saat semburat kuning 10-20% (untuk kirim jauh).",
                    "Panen setiap minggu."
                ]
            },
            "business_analysis": {
                "title": "Analisis Usaha Tani Pepaya per 1 Hektar",
                "assumptions": {"Luas_Lahan": "1 Ha", "Populasi_Tanaman": "1200 tanaman"},
                "costs": [
                    {"item": "Bibit", "amount": "1500 btg", "cost": 3000000},
                    {"item": "Pupuk", "amount": "Intensif", "cost": 8000000},
                    {"item": "Tenaga Kerja", "amount": "Rutin", "cost": 7000000}
                ],
                "yield_potential": [
                    {"scenario": "Konservatif", "total_yield_kg": 40000},
                    {"scenario": "Optimal", "total_yield_kg": 60000}
                ],
                "revenue_scenarios": [
                    {"price_level": "Rendah", "price_per_kg": 2000},
                    {"price_level": "Normal", "price_per_kg": 3500},
                    {"price_level": "Tinggi", "price_per_kg": 5000}
                ]
            }
        }
    }
