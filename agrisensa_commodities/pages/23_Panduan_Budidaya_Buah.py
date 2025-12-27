import streamlit as st
import pandas as pd
import plotly.express as px

# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Panduan Budidaya Buah", page_icon="🍎", layout="wide")

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================


# ==========================================
# 🌳 DATABASE BUAH TROPIS
# ==========================================
fruit_data = {
    "Durian (Si Raja Buah)": {
        "icon": "🧀",
        "desc": "Durian (*Durio zibethinus*) adalah komoditas buah premium dengan nilai ekonomi tinggi.",
        "syarat": {
            "Iklim": "Curah hujan 1500-2500 mm/tahun, Suhu 23-30°C",
            "Fase Kering": "Butuh 1-3 bulan kering (<60 mm hujan) untuk memicu pembungaan",
            "Ketinggian": "100 - 800 mdpl (Optimal 400-600 mdpl)",
            "Tanah": "Lempung berpasir, subur, gembur, pH 6.0-7.0, Drainase baik (tidak tahan tergenang)"
        },
        "tanam": {
            "Jarak Tanam": "8x8 m (Populasi ~156 pohon/ha) atau 10x10 m (Populasi ~100 pohon/ha)",
            "Lubang Tanam": "60x60x60 cm atau 80x80x80 cm. Biarkan terbuka 2 minggu, campur pupuk kandang 20kg + Dolomit 0.5kg",
            "Bibit": "Gunakan bibit okulasi/sambung pucuk tinggi >80cm, bebas penyakit, daun hijau tua mengkilap"
        },
        "pupuk": {
            "TBM (1-3 th)": "NPK 16-16-16: 200g - 1kg per pohon/tahun (dibagi 4x aplikasi)",
            "TM (>4 th)": "Awal musim hujan (NPK Tinggi N), Menjelang bunga (Tinggi P & K), Pasca Panen (Organik + NPK seimbang)",
            "Boost Buah": "KNO3 Putih saat pentil buah seukuran kelereng"
        },
        "hama": [
            {"nama": "Penggerek Buah", "gejala": "Lubang pada buah, kotoran ulat", "solusi": "Sanitasi buah rontok, Perangkap feromon, Insektisida Deltamethrin"},
            {"nama": "Kanker Batang", "gejala": "Kulit batang mengeluarkan lendir/gumosis", "solusi": "Kerok kulit sakit, olesi fungisida berbahan aktif Tembaga/Mankozeb"}
        ],
        "panen": "Jatuh sendiri (matang fisiologis sempurna) atau petik tua (tangkai mengeras, duri renggang) untuk kiriman jauh. Durasi matang 115-125 hari setelah bunga mekar (tergantung varietas)."
    },
    "Mangga (Export Quality)": {
        "icon": "🥭",
        "desc": "Mangga (*Mangifera indica*) sangat potensial untuk pasar lokal dan ekspor, terutama varietas Gedong Gincu dan Arumanis.",
        "syarat": {
            "Iklim": "Bulan kering 3-4 bulan sangat penting untuk pembungaan. Curah hujan <1500 mm/tahun optimal.",
            "Ketinggian": "0 - 500 mdpl (Dataran Rendah)",
            "Tanah": "Tanah aluvial/latosol, solum dalam (>1m), pH 5.5-7.5"
        },
        "tanam": {
            "Jarak Tanam": "8x8 m atau 10x10 m (Tanpa pangkas), 4x5 m (High Density Planting dengan manajemen tajuk intensif)",
            "Lubang Tanam": "60x60x60 cm. Campurkan 20kg kompos matang.",
            "Waktu": "Awal musim hujan"
        },
        "pupuk": {
            "TBM": "Urea:SP36:KCl (1:1:1) mulai 200g/pohon umur 1 th, naik bertahap.",
            "Induksi Bunga": "ZPT Paklobutrazol (aplikasi siram tanah) pada tanaman sehat umur >3-4 tahun saat daun tua (dorman).",
            "Pembesaran": "Pupuk K tinggi (KNO3) saat buah sebesar telur ayam."
        },
        "hama": [
            {"nama": "Lalat Buah", "gejala": "Buah busuk, ada belatung di dalam", "solusi": "Bungkus buah (brongsong) sejak dini, Perangkap Metil Eugenol"},
            {"nama": "Wereng Mangga", "gejala": "Bunga kering dan rontok, embun jelaga", "solusi": "Insektisida Imidakloprid sebelum bunga mekar sempurna"}
        ],
        "panen": "Petik saat pangkal buah membengkak rata, lekukan ujung hilang, dan kulit mulai berbedak. 85-95% tingkat kematangan untuk pasar jauh."
    },
    "Alpukat (Superfood)": {
        "icon": "🥑",
        "desc": "Alpukat (*Persea americana*) kini menjadi primadona karena tren hidup sehat. Varietas mentega dan aligator sangat diminati.",
        "syarat": {
            "Iklim": "Suhu optimal 20-28°C. Angin kencang dapat merusak percabangan lunak.",
            "Ketinggian": "200 - 1000 mdpl (Tergantung ras: Ras Meksiko tahan dingin, Ras Hindia Barat dataran rendah)",
            "Tanah": "Wajib gembur dan TIDAK BOLEH TERGENANG air sama sekali. pH 6.0-7.0."
        },
        "tanam": {
            "Jarak Tanam": "6x7 m atau 8x8 m",
            "Persiapan": "Buat guludan/busut jika tanah datar untuk hindari genangan air hujan (drainase adalah kunci).",
            "Bibit": "Sambung pucuk, umur >6 bulan di polybag."
        },
        "pupuk": {
            "TBM": "NPK 15-15-15, 4x setahun. Dosis 50g (th 1) naik ke 200g (th 2).",
            "TM": "NPK 12-12-17 + TE saat berbunga dan berbuah. Tambahan Boron penting untuk cegah buah bengkok.",
            "Organik": "Mutlak perlu 20kg/pohon setiap tahun."
        },
        "hama": [
            {"nama": "Ulat Kipat", "gejala": "Daun habis dimakan ulat besar", "solusi": "Kutif manual kepompong, Insektisida kontak"},
            {"nama": "Busuk Akar (Phytophthora)", "gejala": "Daun layu mendadak, akar membusuk", "solusi": "Drainase diperbaiki, Trichoderma pada tanah, Bubur Bordeaux"}
        ],
        "panen": "Warna kulit buah tua (kusam/tidak mengkilap), jika diguncang biji berbunyi (pada beberapa varietas). Petik dengan gunting, sisakan tangkai cm."
    },
    "Manggis (Queen of Fruits)": {
        "icon": "👸",
        "desc": "Manggis (*Garcinia mangostana*) adalah tanaman asli nusantara dengan pertumbuhan lambat namun umur produktif sangat panjang.",
        "syarat": {
            "Iklim": "Lembab tinggi, curah hujan merata >2000 mm/th. Tidak tahan kering ekstrem.",
            "Ketinggian": "100 - 600 mdpl",
            "Naungan": "WAJIB ada naungan (pisang/waru) pada 2-3 tahun pertama karena tidak tahan terik matahari langsung."
        },
        "tanam": {
            "Jarak Tanam": "10x10 m",
            "Lubang Tanam": "Ukuran besar 100x100x50 cm karena perakaran manggis sedikit dan lambat.",
            "Naungan": "Siapkan naungan buatan (paraneti) atau tanaman sela sebelum tanam."
        },
        "pupuk": {
            "Slow Release": "Gunakan pupuk lepas lambat atau organik tinggi karena serapan akar lambat.",
            "Fase": "TBM fokus N untuk daun. TM butuh KCl tinggi untuk kualitas daging buah."
        },
        "hama": [
            {"nama": "Getah Kuning", "gejala": "Getah kuning pada kulit dan daging buah (buah pahit/keras)", "solusi": "Hindari benturan, jaga ketersediaan air tanah stabil, pemupukan Ca dan B"},
            {"nama": "Burik Buah", "gejala": "Kulit buah kasar kecoklatan", "solusi": "Kendalikan Thrips dengan insektisida abamektin saat berbunga"}
        ],
        "panen": "Warna kulit ungu kemerahan (indeks warna 2-3) untuk ekspor. Ungu pekat (indeks 5-6) untuk konsumsi langsung."
    },
     "Jeruk (High Demand)": {
        "icon": "🍊",
        "desc": "Jeruk (Siam, Keprok, Pamelo) adalah buah paling banyak dikonsumsi harian.",
        "syarat": {
            "Iklim": "Suhu 25-30°C. Perbedaan suhu siang-malam membantu warna kulit cerah.",
            "Ketinggian": "0 - 1200 mdpl (Siam dataran rendah, Keprok dataran tinggi)",
            "Tanah": "Andosol atau Latosol. pH 5.5 - 6.5. Tidak tahan genangan."
        },
        "tanam": {
            "Jarak Tanam": "3x4 m atau 5x5 m",
            "Lubang Tanam": "60x60x60 cm.",
            "Sistem": "Tanam di atas gundukan/bedengan jika lahan datar (sistem surjan)."
        },
        "pupuk": {
            "Berimbang": "Jeruk sangat responsif terhadap pupuk kandang dan mikro (Zn, Fe, Mn).",
            "Defisiensi": "Perhatikan gejala kuning daun (kurang N/Mg/Fe) yang sering muncul."
        },
        "hama": [
            {"nama": "CVPD (Huanglongbing)", "gejala": "Daun belang kuning, tulang daun hijau, buah kecil asimetris", "solusi": "TIDAK ADA OBAT. Cegah kutu loncat (Diaphorina citri) sebagai vektor. Gunakan bibit bebas penyakit."},
            {"nama": "Lalat Buah", "gejala": "Buah busuk gugur", "solusi": "Perangkap, Petik bubur sanitasi, Insektisida sistemik terbatas"}
        ],
        "panen": "Buah mulai menguning >30-50%, rasio gula:asam optimal. Panen dengan gunting, jangan ditarik."
    },
    "Klengkeng (New Kristal/Kateki)": {
        "icon": "🌑",
        "desc": "Klengkeng (*Dimocarpus longan*) varietas New Kristal memiliki daging tebal, biji kecil, dan sangat produktif dengan induksi KClO3.",
        "syarat": {
            "Iklim": "Dataran rendah hingga menengah. Butuh penyinaran penuh.",
            "Ketinggian": "0 - 900 mdpl (Optimal 200-600 mdpl)",
            "Tanah": "Lempung berpasir, pH 5.5-6.5. Tahan kekeringan lebih baik daripada durian."
        },
        "tanam": {
            "Jarak Tanam": "6x6 m atau 8x8 m. Bisa sistem plantera (tabulampot) skala kebun.",
            "Lubang Tanam": "60x60x60 cm. Campur pupuk kandang + kapur.",
            "Booster": "Wajib induksi pembuahan dengan KClO3 (Potasium Klorat) agar berbuah serempak."
        },
        "pupuk": {
            "Vegetatif": "NPK 16-16-16 rutin 3 bulan sekali.",
            "Generatif": "Aplikasi Booster (siram/semprot) saat daun tua. Susul dengan MKP dan KNO3 untuk pembesaran buah."
        },
        "hama": [
            {"nama": "Kelelawar (Codot)", "gejala": "Buah habis dimakan saat malam", "solusi": "Pemberongsongan (wajib) dengan jaring paranet seluruh tajuk (sistem kerodong)."},
            {"nama": "Penggerek Batang", "gejala": "Lubang pada batang utama, keluar serbuk kayu", "solusi": "Suntik insektisida sistemik ke lubang aktif, tutup dengan kapas/lilin."}
        ],
        "panen": "6 bulan setelah aplikasi booster. Kulit buah halus, warna coklat terang, rasa manis maksimal."
    },
    "Anggur Import (Tropical Viticulture)": {
        "icon": "🍇",
        "desc": "Anggur meja (*Table Grape*) varietas import (Jupiter, Transfiguration, Julian) kini dapat dibuahkan 3x setahun di iklim tropis Indonesia.",
        "syarat": {
            "Iklim": "Panas terik (Full Sun), curah hujan rendah. WAJIB atap UV/Greenhouse untuk hasil premium tanpa jamur.",
            "Ketinggian": "0 - 800 mdpl. Dataran rendah hasil lebih manis.",
            "Media Tanam": "Sangat porous (Sekam bakar, pasir, kompos). Tidak boleh becek/padat."
        },
        "tanam": {
            "Sistem": "Teralis (Pagar) atau Para-para (Atap). Jarak tanam 1.5 - 3 m antar pohon.",
            "Bibit": "Guntung (Rootstock) tahan nematoda + Entres varietas import (Grafting).",
            "Pruning": "Kunci pembuahan adalah PANGKAS TOTAL (Foundation Pruning -> Production Pruning)."
        },
        "pupuk": {
            "Mingguan": "NPK Seimbang + MgSO4 (Vegetatif). MKP + KNO3 + Boron (Generatif - 1 bulan sebelum pangkas).",
            "Organik": "Asam Humat dan POC rutin kocor."
        },
        "hama": [
            {"nama": "Jamur Downy/Powdery Mildew", "gejala": "Serbuk putih/kuning pada daun, daun kering", "solusi": "Fungisida kontak & sistemik bergantian (Mankozeb/Amistartop). Atap UV sangat membantu."},
            {"nama": "Kutu Perisai/Scale", "gejala": "Bintik putih/coklat pada batang, batang mati", "solusi": "Sikat batang dengan sikat gigi + insektisida/sabun cuci piring."}
        ],
        "panen": "90-120 hari setelah pangkas pembuahan (HSP). Rasa manis brix >18, warna sempurna."
    },
    "Jambu Kristal (Fast Cash Flow)": {
        "icon": "🍐",
        "desc": "Jambu Kristal (*Psidium guajava*) adalah pilihan terbaik untuk perputaran modal cepat. Berbuah sepanjang tahun tanpa kenal musim.",
        "syarat": {
            "Iklim": "Tropis basah maupun kering. Sangat adaptif.",
            "Ketinggian": "0 - 1000 mdpl",
            "Tanah": "Toleran terhadap berbagai jenis tanah, asal tidak tergenang."
        },
        "tanam": {
            "Jarak Tanam": "3x3 m atau 2.5x2.5 m (Padat). Penjarangan tajuk sangat sering.",
            "Bibit": "Cangkok atau Okulasi.",
            "Perawatan": "Pembungkusan buah (brongsong) saat ukuran bola pingpong adalah WAJIB untuk mulus."
        },
        "pupuk": {
            "Rutin": "NPK 16-16-16 setiap bulan 50-100g/pohon.",
            "Mikro": "Semprot pupuk daun mikro lengkap agar daun tidak klorosis (kuning)."
        },
        "hama": [
            {"nama": "Lalat Buah", "gejala": "Buah busuk berbelatung", "solusi": "Bungkus buah (Fruit cover) plastik bening + koran/styrofoam sejak dini."},
            {"nama": "Kutu Putih", "gejala": "Putih-putih pada pucuk daun dan buah", "solusi": "Insektisida Imidakloprid atau deterjen cair."}
        ],
        "panen": "Panen mingguan! Tiada henti sepanjang tahun. Sangat baik untuk cashflow harian/mingguan."
    },
    "Pisang Cavendish (Export)": {
        "icon": "🍌",
        "desc": "Pisang Cavendish adalah standar pisang meja dunia. Pasar supermarket dan ekspor sangat terbuka lebar.",
        "syarat": {
            "Iklim": "Curah hujan merata, hindari angin topan (batang mudah patah).",
            "Ketinggian": "0 - 400 mdpl optimal untuk ukuran buah besar.",
            "Tanah": "Subur, gembur, kaya bahan organik."
        },
        "tanam": {
            "Jarak Tanam": "2x2 m atau 2.5x2.5 m.",
            "Bibit": "Kultur Jaringan (Wajib untuk bebas penyakit layu).",
            "Perawatan": "Suntik jantung (insektisida), brongsong tandan, dan potong jantung jantan."
        },
        "pupuk": {
            "Kalium Tinggi": "Pisang adalah 'penyedot Kalium'. Gunakan KCl/ZK dosis tinggi saat buah keluar.",
            "Dosis": "Urea 200g, SP36 150g, KCl 300g per rumpun per tahun."
        },
        "hama": [
            {"nama": "Layu Fusarium (Panama Disease)", "gejala": "Daun kuning layu, bonggol busuk merah", "solusi": "TIDAK ADA OBAT. Gunakan bibit resisten, trichoderma, dan karantina lahan."},
            {"nama": "Burik Buah (Scab/Thrips)", "gejala": "Kulit buah bintik hitam kasar", "solusi": "Suntik jantung, bungkus tandan dengan plastik biru/perak."}
        ],
        "panen": "Jantung keluar -> Panen 3 bulan kemudian. Tebang pohon induk, sisakan 1 anakan (sistem 1 induk 1 anak)."
    },
    "Pepaya Calina (California)": {
        "icon": "🥭",
        "desc": "Pepaya Calina (IPB-9) adalah pepaya pendek, manis, dan tahan simpan. Panen mulai bulan ke-7.",
        "syarat": {
            "Iklim": "Panas, hujan sedang. Akar sangat sensitif busuk jika tergenang air 1 hari saja.",
            "Ketinggian": "0 - 600 mdpl.",
            "Drainase": "Wajib bedengan tinggi agar air cepat tuntas."
        },
        "tanam": {
            "Jarak Tanam": "2.5 x 2.5 m.",
            "Benih": "Biji murni varietas Calina (jangan ambil dari buah pasar, genetik menurun).",
            "Seleksi": "Saat berbunga (bulan ke-3), buang pohon betina (buah bulat), pertahankan pohon hermafrodit (buah lonjong - laku di pasar)."
        },
        "pupuk": {
            "Mingguan": "Pupuk NPK kocor setiap selasa. Pupuk kandang setiap 3 bulan.",
            "Boron": "Kekurangan boron membuat buah benjol-benjol tidak rata."
        },
        "hama": [
            {"nama": "Kutu Putih (Paracoccus)", "gejala": "Pohon hitam jelaga, buah tertutup lapisan lilin putih", "solusi": "Semprot air sabun + minyak, Insektisida Profenofos."},
            {"nama": "Virus Kuning (Gemini/Ringspot)", "gejala": "Daun kuning keriting, buah ada cincin", "solusi": "Cabut dan bakar pohon sakit. Kendalikan vektor kutu daun Aphids."}
        ],
        "panen": "Mulai panen umur 7-8 bulan. Panen setiap minggu selama 2-3 tahun produktif."
    },
    "Kopi (Robusta & Arabica)": {
        "icon": "☕",
        "desc": "Kopi adalah komoditas global. Robusta untuk dataran rendah, Arabica untuk dataran tinggi dengan cita rasa khas.",
        "syarat": {
            "Iklim": "Robusta: 24-30°C (Panas). Arabica: 16-20°C (Sejuk).",
            "Ketinggian": "Robusta: 0-800 mdpl. Arabica: 800-2000 mdpl (Wajib).",
            "Naungan": "Butuh tanaman penaung (Lamtoro/Dadap) untuk menjaga kelembaban dan kualitas buah."
        },
        "tanam": {
            "Jarak Tanam": "2.5 x 2.5 m (Populasi 1600/ha).",
            "Lubang": "60x60x60 cm. Campurkan pupuk kandang.",
            "Pemangkasan": "KUNCI PRODUKSI. Pangkas bentuk (1-3 th) dan Pangkas produksi (buang wiwilan/cabang cacing)."
        },
        "pupuk": {
            "TBM": "Urea 50g/pohon (th 1). Naikkan dosis NPK bertahap.",
            "TM": "NPK 15-15-15 (2x setahun). Tambahkan dolomit karena tanah kopi cenderung asam."
        },
        "hama": [
            {"nama": "PBKo (Penggerek Buah Kopi)", "gejala": "Buah berlubang, biji hampa", "solusi": "Petik merah serentak (lelesan), pasang perangkap alkohol/feromon. Beauveria bassiana."},
            {"nama": "Karat Daun (Hemileia)", "gejala": "Bercak kuning serbuk di bawah daun", "solusi": "Pangkas daun sakit, semprot fungisida Tembaga (Copper). Ganti varietas tahan (S795/Lini S)."}
        ],
        "panen": "Panen hanya buah MERAH (Red Cherry) untuk kualitas premium (Fine Robusta/Specialty Arabica)."
    },
    "Kakao / Coklat (MCC Clones)": {
        "icon": "🍫",
        "desc": "Kakao (*Theobroma cacao*) klon unggul (MCC 02/Sulawesi) sangat produktif dan tahan hama. ",
        "syarat": {
            "Iklim": "Curah hujan 1500-2500 mm. Tidak tahan angin kencang.",
            "Ketinggian": "0 - 600 mdpl.",
            "Naungan": "Wajib ada penaung sementara (pisang) dan tetap (kelapa/lamtoro) intensitas 30-50%."
        },
        "tanam": {
            "Jarak Tanam": "3x3 m.",
            "Teknik": "Sambung Samping (Side Grafting) pada pohon tua untuk rehabilitasi cepat.",
            "Klon": "MCC 02 (Biji besar, tahan VSD)."
        },
        "pupuk": {
            "Organik": "Limbah kulit kakao dikomposkan dan dikembalikan ke kebun (Siklus hara).",
            "Kimia": "NPK 12-12-17 + 2 MgO. Kakao butuh Magnesium tinggi."
        },
        "hama": [
            {"nama": "PBK (Penggerek Buah Kakao)", "gejala": "Buah masak tidak merata, biji lengket", "solusi": "Sarungisasi (bungkus buah) saat kecil. Panen sering."},
            {"nama": "VSD (Vascular Streak Dieback)", "gejala": "Ranting kering, daun gugur tersisa tulang", "solusi": "Pangkas ranting sakit sampai batas sehat + 20cm. Gunakan klon tahan (MCC)."}
        ],
        "panen": "Buah berubah warna (Hijau -> Kuning / Merah -> Jingga). Pecah buah, ambil biji, fermentasi 5 hari untuk aroma coklat asli."
    },
    "Teh (Pucuk Pilihan)": {
        "icon": "🍵",
        "desc": "Teh (*Camellia sinensis*) diambil pucuk mudanya. Perkebunan teh juga bisa jadi agrowisata.",
        "syarat": {
            "Iklim": "Sejuk, curah hujan tinggi, kabut membantu kualitas.",
            "Ketinggian": "800 - 2000 mdpl (Makin tinggi makin baik kualitasnya).",
            "Tanah": "Andosol, pH 4.5-5.6 (Sangat Asam)."
        },
        "tanam": {
            "Jarak Tanam": "120 x 60 cm (Baris Ganda) mengikuti kontur.",
            "Bentuk": "Pangkas meja (plucking table) setinggi pinggang pemetik."
        },
        "pupuk": {
            "Nitrogen": "Sangat butuh Urea/ZA untuk pertumbuhan daun cepat.",
            "Sulfur": "Wajib ada unsur S untuk aroma teh."
        },
        "hama": [
            {"nama": "Empoasca (Wereng Teh)", "gejala": "Tepi daun kuning kecoklatan (Hopperburn)", "solusi": "Insektisida nabati, perekat kuning."},
            {"nama": "Cacar Daun (Blister)", "gejala": "Bintik bening/merah pada daun muda", "solusi": "Petik habis pucuk sakit, fungisida mankozeb saat cuaca ekstrim."}
        ],
        "panen": "Rumus P+2 (Peko + 2 Daun Muda) atau P+3. Rotasi petik 7-14 hari tergantung elevasi."
    },
    "Rambutan (Binjai/Rapiah)": {
        "icon": "🔴",
        "desc": "Rambutan (*Nephelium lappaceum*) adalah buah asli tropis. Binjai (manis, ngelotok) dan Rapiah (kecil, manis, kering) paling laku.",
        "syarat": {
            "Iklim": "Tropis basah. Musim kering jelas dibutuhkan untuk bunga.",
            "Ketinggian": "0 - 500 mdpl (Dataran Rendah).",
            "Air": "Tahan genangan sebentar, tapi sebaiknya drainase baik."
        },
        "tanam": {
            "Jarak Tanam": "10 x 10 m (Tajuk lebar).",
            "Bibit": "Okulasi mata tunas.",
            "Kelamin": "Pastikan bibit hermaprodit/betina produktif."
        },
        "pupuk": {
            "Pasca Panen": "NPK + Organik untuk pemulihan.",
            "Bunga": "Pupuk P & K tinggi saat daun tua untuk memicu bunga."
        },
        "hama": [
            {"nama": "Ulat Buah/Biji", "gejala": "Buah berlubang, kotoran ulat di kulit", "solusi": "Sanitasi kebun, semprot saat pentil buah."},
            {"nama": "Jamur Upas", "gejala": "Cabang merah bata/merah jambu, mati", "solusi": "Kerok kulit sakit, oles fungisida tembaga."}
        ],
        "panen": "Warna kulit merah merata (Binjai) atau hijau kekuningan (Rapiah). Panen setandan."
    },
    "Duku / Langsat (Palembang)": {
        "icon": "🌕",
        "desc": "Duku (*Lansium domesticum*) varietas Palembang/Komering. Manis, biji kecil/tidak ada. Pohon berumur sangat panjang.",
        "syarat": {
            "Iklim": "Teduh, lembab. Tidak tahan panas terik langsung saat muda.",
            "Ketinggian": "0 - 600 mdpl.",
            "Tanah": "Lempung liat berhumus tinggi."
        },
        "tanam": {
            "Jarak Tanam": "8 x 8 m.",
            "Naungan": "Wajib naungan rapat saat bibit (1-3 tahun).",
            "Waktu": "Sangat lambat (Juvenile phase lama), baru berbuah umur 10-15 tahun dari biji (7-8 th dari sambung)."
        },
        "pupuk": {
            "Organik": "Sangat suka serasah daun/kompos tebal di bawah tajuk.",
            "Kimia": "NPK standar setahun sekali awal hujan."
        },
        "hama": [
            {"nama": "Penggerek Batang", "gejala": "Lubang pada dahan utama", "solusi": "Suntik insektisida."},
            {"nama": "Kelelawar", "gejala": "Memakan buah masak", "solusi": "Jaring/Net pelindung."}
        ],
        "panen": "1x setahun. Panen dengan memanjat, potong tandan dengan pisau, JANGAN digoyang (buah rontok cepat busuk)."
    }
}

# ==========================================
# 🏗️ UI LAYOUT
# ==========================================

# Sidebar (Moved to Main for better visibility)
# st.sidebar.header("Pilih Komoditas")
# selected_fruit = st.sidebar.selectbox("Jenis Tanaman Buah", list(fruit_data.keys()))

st.info(f"💡 Tersedia **{len(fruit_data)}** Komoditas (Buah & Perkebunan) dalam database. Silakan pilih di bawah ini:")
selected_fruit = st.selectbox("👇 Pilih Komoditas Budidaya:", list(fruit_data.keys()))

# DATA LOAD
data = fruit_data[selected_fruit]

# Safe Data Extraction to prevent Crashes
syarat = data.get('syarat', {})
tanam = data.get('tanam', {})
pupuk = data.get('pupuk', {})
hama = data.get('hama', [])
panen_info = data.get('panen', '-')

# MAIN HEADER
col_header1, col_header2 = st.columns([1, 4])
with col_header1:
    st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{data['icon']}</h1>", unsafe_allow_html=True)
with col_header2:
    st.title(f"{selected_fruit}")
    st.markdown(data['desc'])
    
st.divider()

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🌱 Syarat Tumbuh", "🚜 Teknis Penanaman", "🧪 Pemupukan & Perawatan", "🛡️ Hama & Penyakit", "💰 Analisis Singkat"])

# TAB 1: SYARAT TUMBUH
with tab1:
    st.subheader("Kondisi Lingkungan Optimal")
    col_env1, col_env2 = st.columns(2)
    
    with col_env1:
        st.info(f"**🌡️ Iklim & Curah Hujan**\n\n{syarat.get('Iklim', '-')}")
        st.warning(f"**⛰️ Ketinggian Tempat (mdpl)**\n\n{syarat.get('Ketinggian', '-')}")
        
    with col_env2:
        # Robust access for Soil/Medium info
        media_info = syarat.get('Tanah', syarat.get('Media Tanam', syarat.get('Naungan', syarat.get('Air', '-'))))
        lbl_tanah = "Media Tanam" if "Media" in syarat else ("Naungan" if "Naungan" in syarat else "Kondisi Tanah")
        
        st.success(f"**🏞️ {lbl_tanah}**\n\n{media_info}")
        if "Fase Kering" in syarat:
            st.error(f"**☀️ Catatan Khusus**\n\n{syarat['Fase Kering']}")

# TAB 2: TEKNIS TANAM
with tab2:
    st.subheader("Standar Operasional Penanaman")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("### 📏 Jarak / Sistem")
        # Fix KeyError for crops without 'Jarak Tanam' (e.g. Anggur uses 'Sistem')
        jarak = tanam.get('Jarak Tanam', tanam.get('Sistem', '-'))
        st.write(jarak)
    with c2:
        st.markdown("### 🕳️ Lubang / Teknik")
        # Safe access with multiple fallbacks
        lubang = tanam.get('Lubang Tanam', tanam.get('Lubang', tanam.get('Teknik', tanam.get('Sistem', '-'))))
        st.write(lubang)
    with c3:
        st.markdown("### 🌱 Bibit / Perawatan")
        # Safe access with multiple fallbacks
        bibit = tanam.get('Bibit', tanam.get('Waktu', tanam.get('Klon', tanam.get('Bentuk', tanam.get('Perawatan', '-')))))
        st.write(bibit)
        
    st.caption("💡 *Tips: Sebaiknya lubang tanam disiapkan 2-4 minggu sebelum penanaman agar gas racun tanah hilang dan pupuk kandang matang.*")

# TAB 3: PEMUPUKAN
with tab3:
    st.subheader("Manajemen Nutrisi")
    st.markdown("Pupuk adalah kunci produksi buah. Berikan berimbang Organik dan Kimia.")
    
    col_p1, col_p2 = st.columns([2, 1])
    
    with col_p1:
        st.markdown("#### 📅 Jadwal & Dosis Referensi")
        for fase, desc in pupuk.items():
            st.success(f"**{fase}**: {desc}")
            
    with col_p2:
        st.markdown("#### 🧮 Kalkulator Pupuk NPK")
        st.caption("Hitung estimasi kebutuhan per tahun")
        umur = st.number_input("Umur Tanaman (Tahun)", 1, 30, 5)
        jml_pohon = st.number_input("Jumlah Pohon", 1, 1000, 10)
        
        # Simple Logic Estimation
        if umur <= 3:
            perpohon = 0.5 * umur # approx kg/th
        else:
            perpohon = 2.0 + ((umur-3)*0.5) # naik 0.5kg tiap tahun produktif
            if perpohon > 6: perpohon = 6 # max cap
            
        total_kebutuhan = perpohon * jml_pohon
        
        st.metric("Estimasi NPK/Pohon/Th", f"{perpohon:.1f} kg")
        st.metric("Total Pupuk 1 Kebun", f"{total_kebutuhan:.1f} kg")
        st.caption("*Ini adalah estimasi kasar. Sesuaikan dengan kondisi tanah.*")

# TAB 4: HAMA PENYAKIT
with tab4:
    st.subheader("Musuh Alami & Pengendaliannya")
    
    for h in hama:
        with st.expander(f"🔴 {h['nama']}"):
            c_h1, c_h2 = st.columns([1, 2])
            with c_h1:
                st.markdown("**Gejala Serangan:**")
                st.write(h['gejala'])
            with c_h2:
                st.markdown("**Pengendalian Efektif:**")
                st.write(h['solusi'])

# TAB 5: ANALISIS DAN PANEN
with tab5:
    col_end1, col_end2 = st.columns(2)
    with col_end1:
        st.subheader("🧺 Kriteria Panen")
        st.info(panen_info)
        
    with col_end2:
        st.subheader("📈 Potensi Ekonomi")
        st.write("Simulasi sederhana hasil panen per musim.")
        
        harga = st.number_input("Harga Jual per Kg (Rp)", 5000, 200000, 25000, step=1000)
        hasil_pohon = st.slider("Estimasi Hasil per Pohon (kg)", 10, 200, 50)
        total_populasi = st.number_input("Populasi Tanaman", 1, 10000, 100)
        
        omzet = harga * hasil_pohon * total_populasi
        st.metric("Potensi Omzet/Musim", f"Rp {omzet:,.0f}")
