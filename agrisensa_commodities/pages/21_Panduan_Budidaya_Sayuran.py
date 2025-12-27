# Panduan Budidaya Lengkap Sayuran
# Step-by-step guide untuk berbagai jenis sayuran

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Panduan Budidaya Sayuran", page_icon="🥬", layout="wide")

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================


import sys
import os

# Add parent directory to path for imports (required for Streamlit Cloud)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.crop_service import CropService

# ========== DATABASE BUDIDAYA SAYURAN ==========

SAYURAN_DATABASE = {
    "Cabai Merah": {
        "kategori": "Sayuran Buah",
        "nama_latin": "Capsicum annuum",
        "umur_panen": "90-120 hari",
        "hasil_panen": "15-25 ton/ha",
        
        "persiapan_lahan": {
            "langkah": [
                "Bersihkan lahan dari gulma dan sisa tanaman",
                "Gemburkan tanah dengan cangkul/traktor (kedalaman 30-40 cm)",
                "Buat bedengan lebar 100-120 cm, tinggi 30-40 cm",
                "Jarak antar bedengan 50-60 cm",
                "Aplikasikan pupuk kandang 20-30 ton/ha (2-3 minggu sebelum tanam)",
                "Aplikasikan kapur 1-2 ton/ha jika pH <6.0",
                "Pasang mulsa plastik hitam perak (opsional tapi sangat dianjurkan)"
            ],
            "waktu": "3-4 minggu sebelum tanam",
            "tips": "Mulsa plastik mengurangi gulma 90% dan meningkatkan hasil 30-40%!"
        },
        
        "persemaian": {
            "langkah": [
                "Siapkan media semai: tanah + kompos + sekam (1:1:1)",
                "Gunakan tray semai 72 lubang atau polybag kecil",
                "Rendam benih dalam air hangat 3-4 jam",
                "Tanam benih kedalaman 0.5-1 cm, 1 benih/lubang",
                "Siram dengan sprayer halus 2x sehari",
                "Letakkan di tempat teduh dengan naungan 50%",
                "Bibit siap pindah umur 21-30 hari (4-6 daun sejati)"
            ],
            "kebutuhan_benih": "200-300 gram/ha",
            "waktu": "21-30 hari",
            "tips": "Rendam benih dalam POC/MOL sebelum semai untuk vigor lebih baik!"
        },
        
        "penanaman": {
            "langkah": [
                "Buat lubang tanam diameter 10 cm, kedalaman 10-15 cm",
                "Jarak tanam: 60 x 60 cm atau 70 x 50 cm",
                "Aplikasikan pupuk dasar di lubang tanam:",
                "  - NPK 15-15-15: 5-10 gram/lubang",
                "  - Pupuk kandang matang: 1 genggam/lubang",
                "Pindahkan bibit dengan hati-hati (jangan rusak akar)",
                "Tanam sore hari (hindari siang hari)",
                "Siram langsung setelah tanam",
                "Pasang ajir/lanjaran setinggi 1.5-2 meter"
            ],
            "populasi": "22.000-28.000 tanaman/ha",
            "waktu_tanam": "Awal musim hujan atau dengan irigasi",
            "tips": "Tanam sore hari dan siram untuk mengurangi stress transplanting!"
        },
        
        "pemupukan": {
            "jadwal": [
                {
                    "waktu": "Dasar (saat tanam)",
                    "pupuk": "NPK 15-15-15: 200-300 kg/ha + Pupuk kandang 20-30 ton/ha"
                },
                {
                    "waktu": "14 HST",
                    "pupuk": "Urea 100 kg/ha + KCl 50 kg/ha (kocor)"
                },
                {
                    "waktu": "28 HST",
                    "pupuk": "NPK 16-16-16: 150 kg/ha (kocor)"
                },
                {
                    "waktu": "42 HST (mulai berbunga)",
                    "pupuk": "NPK 15-15-15: 150 kg/ha + KCl 100 kg/ha"
                },
                {
                    "waktu": "56 HST dan seterusnya (setiap 2 minggu)",
                    "pupuk": "NPK 15-15-15: 100 kg/ha + KCl 100 kg/ha"
                }
            ],
            "pupuk_daun": "Semprot pupuk daun NPK + mikronutrien setiap 7-10 hari",
            "tips": "Tingkatkan K saat berbuah untuk buah besar dan berkualitas!"
        },
        
        "pengairan": {
            "sistem": "Drip irrigation (terbaik) atau kocor manual",
            "frekuensi": [
                "Fase vegetatif (0-40 HST): Setiap 2-3 hari",
                "Fase generatif (>40 HST): Setiap 1-2 hari",
                "Musim kemarau: Setiap hari",
                "Saat berbunga: Jangan sampai kekeringan!"
            ],
            "volume": "200-300 ml/tanaman/hari",
            "tips": "Drip irrigation hemat air 50% dan hasil meningkat 30%!"
        },
        
        "pemeliharaan": {
            "penyiangan": "Setiap 2 minggu atau gunakan mulsa plastik",
            "pewiwilan": "Buang tunas air di bawah cabang utama",
            "pemangkasan": "Pangkas daun tua dan sakit untuk sirkulasi udara",
            "perempelan": "Buang buah cacat/kecil untuk fokus ke buah bagus",
            "tips": "Pewiwilan rutin meningkatkan hasil 20-30%!"
        },
        
        "hama_penyakit": {
            "hama_utama": [
                "Thrips - gunakan mulsa perak + perangkap kuning",
                "Kutu daun - semprot mimba atau bawang putih",
                "Ulat grayak - BTI atau tangkap manual",
                "Lalat buah - perangkap methyl eugenol"
            ],
            "penyakit_utama": [
                "Layu bakteri - preventif: varietas tahan + rotasi tanaman",
                "Antraknosa - fungisida nabati (kunyit+jahe) preventif",
                "Busuk buah - sanitasi + drainase baik"
            ],
            "tips": "Preventif lebih baik! Monitoring rutin setiap 2-3 hari!"
        },
        
        "panen": {
            "ciri_panen": [
                "Buah berwarna merah penuh (untuk cabai merah)",
                "Kulit mengkilap dan keras",
                "Umur 90-120 hari setelah tanam",
                "Panen pertama umur 75-80 hari"
            ],
            "cara_panen": "Petik dengan tangkai, gunakan gunting/pisau tajam",
            "frekuensi": "Setiap 2-3 hari sekali",
            "masa_panen": "3-4 bulan (panen berkali-kali)",
            "tips": "Panen pagi hari untuk kesegaran maksimal!"
        },
        
        "pascapanen": {
            "sortasi": "Pisahkan berdasarkan ukuran dan kualitas (A, B, C)",
            "pencucian": "Cuci dengan air bersih, tiriskan",
            "pengemasan": "Keranjang plastik berlubang atau karung jaring",
            "penyimpanan": "Suhu ruang: 3-5 hari, Kulkas: 7-10 hari",
            "tips": "Jangan tumpuk terlalu tinggi, cabai mudah memar!"
        },
        
        "analisis_usaha": {
            "biaya_produksi": {
                "Sewa lahan (1 ha, 6 bulan)": "Rp 5.000.000",
                "Benih": "Rp 500.000",
                "Pupuk kandang": "Rp 6.000.000",
                "Pupuk kimia": "Rp 8.000.000",
                "Pestisida": "Rp 3.000.000",
                "Mulsa plastik": "Rp 4.000.000",
                "Ajir/lanjaran": "Rp 3.000.000",
                "Tenaga kerja": "Rp 15.000.000",
                "Lain-lain": "Rp 3.500.000",
                "TOTAL": "Rp 48.000.000"
            },
            "pendapatan": {
                "Hasil panen": "20 ton/ha",
                "Harga jual": "Rp 15.000/kg (rata-rata)",
                "Total pendapatan": "Rp 300.000.000"
            },
            "keuntungan": {
                "Pendapatan": "Rp 300.000.000",
                "Biaya": "Rp 48.000.000",
                "Keuntungan bersih": "Rp 252.000.000",
                "ROI": "525%",
                "B/C Ratio": "6.25"
            },
            "tips": "Harga cabai fluktuatif! Panen saat harga tinggi untuk profit maksimal!"
        }
    },
    
    "Tomat": {
        "kategori": "Sayuran Buah",
        "nama_latin": "Solanum lycopersicum",
        "umur_panen": "60-90 hari",
        "hasil_panen": "30-50 ton/ha",
        
        "persiapan_lahan": {
            "langkah": [
                "Bersihkan lahan dari gulma",
                "Gemburkan tanah kedalaman 30-40 cm",
                "Buat bedengan lebar 100-120 cm, tinggi 30-40 cm",
                "Jarak antar bedengan 60 cm",
                "Aplikasikan pupuk kandang 30-40 ton/ha",
                "Aplikasikan kapur 1-2 ton/ha + dolomit untuk Ca",
                "Pasang mulsa plastik hitam perak"
            ],
            "waktu": "3-4 minggu sebelum tanam",
            "tips": "Dolomit penting untuk cegah blossom end rot (ujung buah busuk)!"
        },
        
        "persemaian": {
            "langkah": [
                "Media semai: tanah + kompos + sekam (1:1:1)",
                "Tray semai 72 lubang",
                "Tanam benih kedalaman 0.5 cm",
                "Siram 2x sehari dengan sprayer halus",
                "Naungan 50% sampai berkecambah",
                "Bibit siap pindah umur 21-25 hari (4-5 daun)"
            ],
            "kebutuhan_benih": "150-200 gram/ha",
            "waktu": "21-25 hari",
            "tips": "Bibit tomat lebih cepat dari cabai, jangan terlalu tua di persemaian!"
        },
        
        "penanaman": {
            "langkah": [
                "Jarak tanam: 60 x 50 cm atau 70 x 40 cm",
                "Lubang tanam diameter 10 cm, kedalaman 15 cm",
                "Pupuk dasar: NPK 15-15-15 (10 g/lubang) + pupuk kandang",
                "Tanam sore hari",
                "Siram langsung",
                "Pasang ajir setinggi 1.5-2 meter"
            ],
            "populasi": "28.000-33.000 tanaman/ha",
            "waktu_tanam": "Dataran tinggi: sepanjang tahun, Dataran rendah: musim kemarau",
            "tips": "Tomat dataran tinggi lebih manis dan tahan lama!"
        },
        
        "pemupukan": {
            "jadwal": [
                {
                    "waktu": "Dasar (saat tanam)",
                    "pupuk": "NPK 15-15-15: 300-400 kg/ha + Pupuk kandang 30-40 ton/ha"
                },
                {
                    "waktu": "10 HST",
                    "pupuk": "Urea 100 kg/ha + KCl 50 kg/ha"
                },
                {
                    "waktu": "20 HST",
                    "pupuk": "NPK 16-16-16: 150 kg/ha"
                },
                {
                    "waktu": "30 HST (mulai berbunga)",
                    "pupuk": "NPK 15-15-15: 150 kg/ha + KCl 100 kg/ha + Ca(NO3)2 50 kg/ha"
                },
                {
                    "waktu": "40 HST dan seterusnya (setiap 10 hari)",
                    "pupuk": "NPK 15-15-15: 100 kg/ha + KCl 100 kg/ha + Ca(NO3)2 50 kg/ha"
                }
            ],
            "pupuk_daun": "NPK + Ca + B setiap 7 hari untuk cegah blossom end rot",
            "tips": "Ca sangat penting! Kekurangan Ca = ujung buah busuk (blossom end rot)!"
        },
        
        "pengairan": {
            "sistem": "Drip irrigation (sangat dianjurkan)",
            "frekuensi": [
                "Fase vegetatif: Setiap 2 hari",
                "Fase berbunga: Setiap hari (JANGAN sampai stress air!)",
                "Fase berbuah: Setiap hari",
                "Kurangi air saat buah mulai matang (untuk rasa manis)"
            ],
            "volume": "300-400 ml/tanaman/hari",
            "tips": "Pengairan tidak teratur = buah pecah! Konsisten sangat penting!"
        },
        
        "pemeliharaan": {
            "penyiangan": "Gunakan mulsa plastik (sangat efektif)",
            "pewiwilan": "Buang tunas air setiap minggu (PENTING!)",
            "pemangkasan": "Sistem 1-2 batang utama, buang cabang lain",
            "perempelan": "Buang buah kecil/cacat, sisakan 4-6 buah/tandan",
            "tips": "Pewiwilan rutin = buah besar dan berkualitas! Jangan malas wiwil!"
        },
        
        "hama_penyakit": {
            "hama_utama": [
                "Ulat buah - BTI + perangkap feromon",
                "Kutu daun - mulsa perak + mimba",
                "Thrips - perangkap kuning + bawang putih",
                "Tungau - semprot air keras + predator alami"
            ],
            "penyakit_utama": [
                "Layu bakteri - varietas tahan + rotasi + sanitasi",
                "Busuk daun (late blight) - fungisida preventif + drainase",
                "Blossom end rot - Ca cukup + pengairan teratur",
                "Virus - kendalikan thrips + cabut tanaman sakit"
            ],
            "tips": "Blossom end rot BUKAN penyakit! Itu defisiensi Ca + stress air!"
        },
        
        "panen": {
            "ciri_panen": [
                "Buah berwarna merah penuh (untuk tomat merah)",
                "Kulit mengkilap",
                "Umur 60-75 hari setelah tanam",
                "Panen pertama umur 55-60 hari"
            ],
            "cara_panen": "Petik dengan tangkai, pagi hari",
            "frekuensi": "Setiap 2-3 hari",
            "masa_panen": "2-3 bulan",
            "tips": "Panen saat 80% merah untuk transportasi jauh, 100% merah untuk lokal!"
        },
        
        "pascapanen": {
            "sortasi": "Grade A (>100g), B (70-100g), C (<70g)",
            "pencucian": "Cuci lembut, jangan gosok",
            "pengemasan": "Keranjang plastik + alas koran",
            "penyimpanan": "Suhu ruang: 5-7 hari, Kulkas: 10-14 hari",
            "tips": "Jangan simpan di kulkas jika belum matang! Rasa jadi hambar!"
        },
        
        "analisis_usaha": {
            "biaya_produksi": {
                "Sewa lahan (1 ha, 4 bulan)": "Rp 4.000.000",
                "Benih": "Rp 3.000.000",
                "Pupuk kandang": "Rp 8.000.000",
                "Pupuk kimia": "Rp 10.000.000",
                "Pestisida": "Rp 4.000.000",
                "Mulsa + ajir": "Rp 7.000.000",
                "Tenaga kerja": "Rp 20.000.000",
                "Lain-lain": "Rp 4.000.000",
                "TOTAL": "Rp 60.000.000"
            },
            "pendapatan": {
                "Hasil panen": "40 ton/ha",
                "Harga jual": "Rp 8.000/kg (rata-rata)",
                "Total pendapatan": "Rp 320.000.000"
            },
            "keuntungan": {
                "Pendapatan": "Rp 320.000.000",
                "Biaya": "Rp 60.000.000",
                "Keuntungan bersih": "Rp 260.000.000",
                "ROI": "433%",
                "B/C Ratio": "5.33"
            },
            "tips": "Tomat dataran tinggi harga lebih stabil dan kualitas lebih baik!"
        }
    },
    
    "Kangkung": {
        "kategori": "Sayuran Daun",
        "nama_latin": "Ipomoea aquatica",
        "umur_panen": "25-30 hari",
        "hasil_panen": "15-20 ton/ha",
        
        "persiapan_lahan": {
            "langkah": [
                "Bersihkan lahan",
                "Gemburkan tanah kedalaman 20-30 cm",
                "Buat bedengan lebar 100 cm, tinggi 20-30 cm",
                "Jarak antar bedengan 30-40 cm",
                "Aplikasikan pupuk kandang 10-15 ton/ha",
                "Ratakan bedengan"
            ],
            "waktu": "1-2 minggu sebelum tanam",
            "tips": "Kangkung tumbuh cepat, tidak perlu persiapan rumit!"
        },
        
        "penanaman": {
            "metode": "Sebar benih langsung atau tugal",
            "langkah": [
                "Rendam benih 12-24 jam untuk mempercepat perkecambahan",
                "Sebar benih merata atau tugal jarak 5x5 cm",
                "Tutup tipis dengan tanah/kompos",
                "Siram dengan gembor halus",
                "Benih berkecambah 3-5 hari"
            ],
            "kebutuhan_benih": "10-15 kg/ha (sebar), 5-8 kg/ha (tugal)",
            "waktu_tanam": "Sepanjang tahun",
            "tips": "Rendam benih untuk perkecambahan seragam!"
        },
        
        "pemupukan": {
            "jadwal": [
                {
                    "waktu": "Dasar (saat tanam)",
                    "pupuk": "Pupuk kandang 10-15 ton/ha + Urea 50 kg/ha"
                },
                {
                    "waktu": "10 HST",
                    "pupuk": "Urea 100 kg/ha (kocor atau tabur)"
                },
                {
                    "waktu": "20 HST (jika panen >30 hari)",
                    "pupuk": "Urea 50 kg/ha"
                }
            ],
            "pupuk_organik": "POC/MOL setiap 5 hari untuk pertumbuhan maksimal",
            "tips": "Kangkung suka N tinggi! Urea atau POC sangat efektif!"
        },
        
        "pengairan": {
            "sistem": "Genangan (kangkung air) atau kocor (kangkung darat)",
            "frekuensi": [
                "Kangkung air: Tergenang terus (5-10 cm)",
                "Kangkung darat: Siram 2x sehari (pagi & sore)"
            ],
            "tips": "Kangkung air lebih cepat tumbuh tapi perlu air banyak!"
        },
        
        "pemeliharaan": {
            "penyiangan": "Sekali saat umur 10-15 hari",
            "penjarangan": "Jika terlalu rapat, jarang saat umur 7 hari",
            "tips": "Kangkung tumbuh cepat, pemeliharaan minimal!"
        },
        
        "hama_penyakit": {
            "hama_utama": [
                "Ulat daun - BTI atau tangkap manual",
                "Kutu daun - semprot air keras atau sabun"
            ],
            "penyakit_utama": [
                "Karat putih - hindari genangan berlebihan",
                "Busuk akar - drainase baik"
            ],
            "tips": "Kangkung jarang terserang hama berat, sangat mudah!"
        },
        
        "panen": {
            "ciri_panen": [
                "Umur 25-30 hari",
                "Tinggi 25-30 cm",
                "Daun hijau segar"
            ],
            "cara_panen": "Cabut seluruh tanaman atau potong 5 cm dari pangkal",
            "frekuensi": "Sekali panen (cabut) atau 2-3x panen (potong)",
            "tips": "Panen pagi hari untuk kesegaran maksimal!"
        },
        
        "pascapanen": {
            "sortasi": "Buang daun kuning/rusak",
            "pencucian": "Cuci bersih",
            "pengemasan": "Ikat per 250-500 gram",
            "penyimpanan": "Suhu ruang: 1-2 hari, Kulkas: 3-5 hari",
            "tips": "Kangkung cepat layu, jual segera setelah panen!"
        },
        
        "analisis_usaha": {
            "biaya_produksi": {
                "Sewa lahan (1 ha, 1 bulan)": "Rp 500.000",
                "Benih": "Rp 300.000",
                "Pupuk kandang": "Rp 3.000.000",
                "Pupuk kimia": "Rp 1.000.000",
                "Pestisida": "Rp 200.000",
                "Tenaga kerja": "Rp 3.000.000",
                "Lain-lain": "Rp 500.000",
                "TOTAL": "Rp 8.500.000"
            },
            "pendapatan": {
                "Hasil panen": "18 ton/ha",
                "Harga jual": "Rp 3.000/kg",
                "Total pendapatan": "Rp 54.000.000"
            },
            "keuntungan": {
                "Pendapatan": "Rp 54.000.000",
                "Biaya": "Rp 8.500.000",
                "Keuntungan bersih": "Rp 45.500.000",
                "ROI": "535%",
                "B/C Ratio": "6.35"
            },
            "tips": "Kangkung = cash crop! Cepat panen, cepat untung, bisa 12x setahun!"
        }
    }
}

# MERGE WITH CENTRALIZED CROP SERVICE
# We overlay data from the service if available
# This ensures new "Guide" data added in CropService appears here automatically
for crop_name in CropService.get_all_crops():
    service_guide = CropService.get_guide_data(crop_name)
    if service_guide:
        # If the crop already exists, update it. If not, create it.
        # But wait, the service guide structure might be partial.
        # For now, let's just update if keys exist, or add if it matches structure.
        # Simplest integration: If 'guide' data in service has 'analisis_usaha', we can use it.
        if crop_name in SAYURAN_DATABASE:
             SAYURAN_DATABASE[crop_name].update(service_guide)
        elif 'kategori' in service_guide: # Only add if it looks like a full guide object
             SAYURAN_DATABASE[crop_name] = service_guide

# ========== HELPER FUNCTIONS ==========

def create_timeline(umur_panen):
    """Create timeline visualization"""
    days = int(umur_panen.split('-')[0])
    milestones = [
        {"day": 0, "event": "Tanam"},
        {"day": int(days * 0.1), "event": "Penyiangan 1"},
        {"day": int(days * 0.3), "event": "Pemupukan 1"},
        {"day": int(days * 0.5), "event": "Pemupukan 2"},
        {"day": int(days * 0.7), "event": "Berbunga"},
        {"day": days, "event": "Panen"}
    ]
    return milestones

# ========== MAIN APP ==========

st.title("🥬 Panduan Budidaya Lengkap Sayuran")
st.markdown("**Step-by-step guide untuk sukses budidaya sayuran**")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📖 Panduan Lengkap",
    "📊 Perbandingan Sayuran",
    "💰 Analisis Usaha",
    "🗓️ Smart Schedule & RAB"
])

# TAB 1: FULL GUIDE
with tab1:
    st.header("📖 Panduan Budidaya Step-by-Step")
    
    selected_crop = st.selectbox(
        "Pilih Sayuran:",
        sorted(list(SAYURAN_DATABASE.keys()))
    )
    
    if selected_crop:
        data = SAYURAN_DATABASE[selected_crop]
        
        # Header
        st.subheader(f"🌱 {selected_crop}")
        st.caption(f"*{data['nama_latin']}* - {data['kategori']}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Umur Panen", data['umur_panen'])
        
        with col2:
            st.metric("Hasil Panen", data['hasil_panen'])
        
        with col3:
            keuntungan = data['analisis_usaha']['keuntungan']['Keuntungan bersih']
            st.metric("Keuntungan/ha", keuntungan)
        
        st.markdown("---")
        
        # Step-by-step guide
        steps = [
            ("1️⃣ Persiapan Lahan", "persiapan_lahan"),
            ("2️⃣ Persemaian", "persemaian") if "persemaian" in data else None,
            ("3️⃣ Penanaman", "penanaman"),
            ("4️⃣ Pemupukan", "pemupukan"),
            ("5️⃣ Pengairan", "pengairan"),
            ("6️⃣ Pemeliharaan", "pemeliharaan"),
            ("7️⃣ Hama & Penyakit", "hama_penyakit"),
            ("8️⃣ Panen", "panen"),
            ("9️⃣ Pascapanen", "pascapanen")
        ]
        
        steps = [s for s in steps if s is not None]
        
        for step_name, step_key in steps:
            with st.expander(f"**{step_name}**", expanded=False):
                step_data = data[step_key]
                
                if step_key == "persiapan_lahan":
                    st.markdown(f"**Waktu:** {step_data['waktu']}")
                    st.markdown("**Langkah-langkah:**")
                    for i, langkah in enumerate(step_data['langkah'], 1):
                        st.markdown(f"{i}. {langkah}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")
                
                elif step_key == "persemaian":
                    st.markdown(f"**Kebutuhan Benih:** {step_data['kebutuhan_benih']}")
                    st.markdown(f"**Waktu:** {step_data['waktu']}")
                    st.markdown("**Langkah-langkah:**")
                    for i, langkah in enumerate(step_data['langkah'], 1):
                        st.markdown(f"{i}. {langkah}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")
                
                elif step_key == "penanaman":
                    if "metode" in step_data:
                        st.markdown(f"**Metode:** {step_data['metode']}")
                    if "populasi" in step_data:
                        st.markdown(f"**Populasi:** {step_data['populasi']}")
                    if "kebutuhan_benih" in step_data:
                        st.markdown(f"**Kebutuhan Benih:** {step_data['kebutuhan_benih']}")
                    st.markdown(f"**Waktu Tanam:** {step_data['waktu_tanam']}")
                    st.markdown("**Langkah-langkah:**")
                    for i, langkah in enumerate(step_data['langkah'], 1):
                        st.markdown(f"{i}. {langkah}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")
                
                elif step_key == "pemupukan":
                    st.markdown("**Jadwal Pemupukan:**")
                    for jadwal in step_data['jadwal']:
                        st.markdown(f"- **{jadwal['waktu']}:** {jadwal['pupuk']}")
                    if "pupuk_daun" in step_data:
                        st.markdown(f"\n**Pupuk Daun:** {step_data['pupuk_daun']}")
                    if "pupuk_organik" in step_data:
                        st.markdown(f"\n**Pupuk Organik:** {step_data['pupuk_organik']}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")
                
                elif step_key == "pengairan":
                    st.markdown(f"**Sistem:** {step_data['sistem']}")
                    st.markdown("**Frekuensi:**")
                    for freq in step_data['frekuensi']:
                        st.markdown(f"- {freq}")
                    if "volume" in step_data:
                        st.markdown(f"\n**Volume:** {step_data['volume']}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")
                
                elif step_key == "pemeliharaan":
                    for key, value in step_data.items():
                        if key != "tips":
                            st.markdown(f"**{key.title()}:** {value}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")
                
                elif step_key == "hama_penyakit":
                    st.markdown("**Hama Utama:**")
                    for hama in step_data['hama_utama']:
                        st.markdown(f"- {hama}")
                    st.markdown("\n**Penyakit Utama:**")
                    for penyakit in step_data['penyakit_utama']:
                        st.markdown(f"- {penyakit}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")
                
                elif step_key == "panen":
                    st.markdown("**Ciri Siap Panen:**")
                    for ciri in step_data['ciri_panen']:
                        st.markdown(f"- {ciri}")
                    st.markdown(f"\n**Cara Panen:** {step_data['cara_panen']}")
                    st.markdown(f"**Frekuensi:** {step_data['frekuensi']}")
                    if "masa_panen" in step_data:
                        st.markdown(f"**Masa Panen:** {step_data['masa_panen']}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")
                
                elif step_key == "pascapanen":
                    for key, value in step_data.items():
                        if key != "tips":
                            st.markdown(f"**{key.title()}:** {value}")
                    st.info(f"💡 **Tips:** {step_data['tips']}")

# TAB 2: COMPARISON
with tab2:
    st.header("📊 Perbandingan Sayuran")
    
    # Create comparison table
    comparison_data = []
    for nama, data in SAYURAN_DATABASE.items():
        comparison_data.append({
            "Sayuran": nama,
            "Kategori": data['kategori'],
            "Umur Panen": data['umur_panen'],
            "Hasil (ton/ha)": data['hasil_panen'],
            "Biaya (Rp)": data['analisis_usaha']['biaya_produksi']['TOTAL'],
            "Pendapatan (Rp)": data['analisis_usaha']['pendapatan']['Total pendapatan'],
            "Keuntungan (Rp)": data['analisis_usaha']['keuntungan']['Keuntungan bersih'],
            "ROI": data['analisis_usaha']['keuntungan']['ROI']
        })
    
    df = pd.DataFrame(comparison_data)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Visualization
    st.subheader("📈 Visualisasi Perbandingan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.bar(df, x='Sayuran', y='Keuntungan (Rp)', 
                      title='Keuntungan per Hektar',
                      color='Sayuran')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(df, x='Sayuran', y='ROI', 
                      title='Return on Investment (%)',
                      color='Sayuran')
        st.plotly_chart(fig2, use_container_width=True)

# TAB 3: BUSINESS ANALYSIS
with tab3:
    st.header("💰 Analisis Usaha Tani")
    
    selected_crop_business = st.selectbox(
        "Pilih Sayuran untuk Analisis:",
        sorted(list(SAYURAN_DATABASE.keys())),
        key="business"
    )
    
    if selected_crop_business:
        data = SAYURAN_DATABASE[selected_crop_business]
        analisis = data['analisis_usaha']
        
        st.subheader(f"💼 Analisis Usaha: {selected_crop_business}")
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Biaya", analisis['biaya_produksi']['TOTAL'])
        
        with col2:
            st.metric("Pendapatan", analisis['pendapatan']['Total pendapatan'])
        
        with col3:
            st.metric("Keuntungan", analisis['keuntungan']['Keuntungan bersih'])
        
        with col4:
            st.metric("ROI", analisis['keuntungan']['ROI'])
        
        st.markdown("---")
        
        # Detailed breakdown
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 💸 Rincian Biaya Produksi")
            for item, biaya in analisis['biaya_produksi'].items():
                if item != "TOTAL":
                    st.markdown(f"- **{item}:** {biaya}")
            st.success(f"**TOTAL BIAYA:** {analisis['biaya_produksi']['TOTAL']}")
        
        with col2:
            st.markdown("### 💰 Rincian Pendapatan")
            for item, value in analisis['pendapatan'].items():
                st.markdown(f"- **{item}:** {value}")
        
        st.markdown("---")
        
        # Profit calculation
        st.markdown("### 📊 Perhitungan Keuntungan")
        
        pendapatan = int(analisis['pendapatan']['Total pendapatan'].replace('Rp ', '').replace('.', ''))
        biaya = int(analisis['biaya_produksi']['TOTAL'].replace('Rp ', '').replace('.', ''))
        keuntungan = pendapatan - biaya
        
        # Pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['Keuntungan', 'Biaya'],
            values=[keuntungan, biaya],
            hole=.3,
            marker_colors=['#00CC00', '#FF6B6B']
        )])
        
        fig.update_layout(title="Proporsi Keuntungan vs Biaya")
        st.plotly_chart(fig, use_container_width=True)
        
        st.info(f"💡 **Tips:** {analisis['tips']}")
        
        # Custom calculator
        st.markdown("---")
        st.markdown("### 🧮 Kalkulator Keuntungan Custom")
        
        col1, col2 = st.columns(2)
        
        # Helper function to extract price from string
        def extract_price(price_str):
            """Extract numeric price from string like 'Rp 15.000/kg (rata-rata)' or 'Rp 3.000/kg'"""
            import re
            # Remove 'Rp' and everything after '/kg'
            cleaned = price_str.replace('Rp', '').split('/kg')[0].strip()
            # Remove dots (thousand separator) and any remaining non-digits
            cleaned = re.sub(r'[^\d]', '', cleaned)
            return int(cleaned) if cleaned else 15000  # default fallback
        
        with col1:
            luas_custom = st.number_input("Luas Lahan (ha)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
            default_harga = extract_price(analisis['pendapatan']['Harga jual'])
            harga_custom = st.number_input("Harga Jual (Rp/kg)", min_value=1000, max_value=100000, 
                                          value=default_harga, 
                                          step=1000)
        
        with col2:
            hasil_custom = st.number_input("Hasil Panen (ton/ha)", min_value=1.0, max_value=100.0, 
                                          value=float(analisis['pendapatan']['Hasil panen'].split()[0]), 
                                          step=1.0)
        
        if st.button("💵 Hitung Keuntungan", type="primary"):
            biaya_per_ha = biaya
            total_biaya_custom = biaya_per_ha * luas_custom
            total_hasil_custom = hasil_custom * luas_custom * 1000  # kg
            total_pendapatan_custom = total_hasil_custom * harga_custom
            total_keuntungan_custom = total_pendapatan_custom - total_biaya_custom
            roi_custom = (total_keuntungan_custom / total_biaya_custom) * 100
            
            st.success("### 📊 Hasil Perhitungan Custom")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Biaya", f"Rp {total_biaya_custom:,.0f}")
            
            with col2:
                st.metric("Total Pendapatan", f"Rp {total_pendapatan_custom:,.0f}")
            
            with col3:
                st.metric("Keuntungan Bersih", f"Rp {total_keuntungan_custom:,.0f}")
            
# TAB 4: SMART OPERATION (SCHEDULE & RAB)
with tab4:
    st.header("🗓️ Smart Schedule & Auto-RAB")
    st.markdown("""
    **Fitur Lanjutan:** Konversi rencana "Target Tanam" dari Modul Market Commerce menjadi **Jadwal Kerja** & **Anggaran Biaya** riil.
    """)
    
    col_op1, col_op2 = st.columns([1, 2])
    
    with col_op1:
        st.subheader("⚙️ Parameter Operasional")
        
        # Determine default from forecast key if present (future integration)
        op_crop = st.selectbox("Komoditas Target", sorted(list(SAYURAN_DATABASE.keys())), key="op_crop")
        op_area = st.number_input("Luas Lahan (Ha)", 0.1, 100.0, 1.0, step=0.1, key="op_area")
        op_start_date = st.date_input("Tanggal Mulai Tanam", datetime.now())
        
        st.info(f"Basis Data: **{op_crop}** di lahan **{op_area} Ha**")
        
        # --- AUTO RAB CALCULATION ---
        st.divider()
        st.subheader("💰 Estimasi Anggaran (RAB)")
        
        if op_crop in SAYURAN_DATABASE:
            cost_base = SAYURAN_DATABASE[op_crop]['analisis_usaha']['biaya_produksi']
            total_cost_base = int(cost_base['TOTAL'].replace('Rp ', '').replace('.', ''))
            
            # Simple Scaling (Linear)
            total_rab = total_cost_base * op_area
            
            st.metric("Total Kebutuhan Modal", f"Rp {total_rab:,.0f}")
            
            # Breakdown
            st.markdown("**Rincian Belanja:**")
            cost_breakdown = []
            for k, v in cost_base.items():
                if k != "TOTAL":
                    val_clean = int(v.replace('Rp ', '').replace('.', ''))
                    val_scaled = val_clean * op_area
                    cost_breakdown.append({"Item": k, "Biaya": val_scaled})
                    
            df_cost = pd.DataFrame(cost_breakdown)
            st.dataframe(df_cost.style.format({"Biaya": "Rp {:,.0f}"}), use_container_width=True, hide_index=True)
        
    with col_op2:
        st.subheader("📅 Kalender Kerja Harian (SOP)")
        st.caption("Dibuat otomatis berdasarkan Tanggal Mulai Tanam Anda.")
        
        schedule_data = []
        
        if op_crop in SAYURAN_DATABASE:
            data = SAYURAN_DATABASE[op_crop]
            
            # 1. Persiapan Lahan (H-21 to H-1)
            prep_days = 21
            start_prep = op_start_date - timedelta(days=prep_days)
            schedule_data.append({"Tanggal": start_prep, "Kegiatan": "Mulai Olah Lahan", "Detail": "Bersihkan lahan & buat bedengan awal", "Fase": "Persiapan"})
            schedule_data.append({"Tanggal": op_start_date - timedelta(days=7), "Kegiatan": "Pemberian Pupuk Dasar", "Detail": "Aduk pupuk kandang + kapur di bedengan", "Fase": "Persiapan"})
            
            # 2. Persemaian (Concurrent with Prep often, but let's simplify)
            if 'persemaian' in data:
                seed_days = 21 # avg
                start_seed = op_start_date - timedelta(days=seed_days) 
                schedule_data.append({"Tanggal": start_seed, "Kegiatan": "Semaikan Benih", "Detail": "Rendam benih & masukkan tray semai", "Fase": "Persemaian"})
            
            # 3. Tanam (Day 0)
            schedule_data.append({"Tanggal": op_start_date, "Kegiatan": "PINDAH TANAM (Transplanting)", "Detail": "Pindahkan bibit ke lahan utama sore hari", "Fase": "Tanam"})
            
            # 4. Pemupukan Susulan (Iterate 'jadwal' list)
            if 'pemupukan' in data and 'jadwal' in data['pemupukan']:
                for item in data['pemupukan']['jadwal']:
                    day_str = item['waktu'].split(' ')[0] # Extract "14" from "14 HST"
                    if day_str.isdigit():
                        days_after = int(day_str)
                        sched_date = op_start_date + timedelta(days=days_after)
                        schedule_data.append({"Tanggal": sched_date, "Kegiatan": f"Pemupukan: {item['waktu']}", "Detail": item['pupuk'], "Fase": "Perawatan"})
            
            # 5. Panen (Estimate)
            harvest_range = data['umur_panen'].split('-') # "90-120 hari"
            first_harvest = int(harvest_range[0].split()[0])
            harvest_date = op_start_date + timedelta(days=first_harvest)
            schedule_data.append({"Tanggal": harvest_date, "Kegiatan": "PANEN PERDANA 🌟", "Detail": "Cek kematangan buah/sayur", "Fase": "Panen"})
            
            # Sort & Display
            df_sched = pd.DataFrame(schedule_data).sort_values(by="Tanggal")
            
            # Highlight current/upcoming
            today = datetime.now().date()
            
            # Render Timeline View
            for idx, row in df_sched.iterrows():
                d = row['Tanggal']
                is_past = d < today if isinstance(d, datetime) else d < datetime.combine(today, datetime.min.time()).date() # type safety
                
                # Check formatting
                date_fmt = d.strftime("%d %b %Y") if hasattr(d, 'strftime') else d
                
                icon = "⬜"
                bg_color = "#f2f2f2"
                if row['Fase'] == "Panen": icon, bg_color = "💰", "#dcfce7"
                elif row['Fase'] == "Tanam": icon, bg_color = "🌱", "#dbeafe"
                elif row['Fase'] == "Persiapan": icon, bg_color = "🚜", "#ffedd5"
                
                st.markdown(f"""
                <div style='background-color: {bg_color}; padding: 10px; border-radius: 5px; margin-bottom: 5px; border-left: 4px solid #666;'>
                    <strong>{icon} {date_fmt}</strong> - {row['Kegiatan']} <br>
                    <small>{row['Detail']}</small>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Export Button
            csv_sched = df_sched.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Download Jadwal Kerja (CSV)", csv_sched, "jadwal_tani_smart.csv", "text/csv")

# Footer
st.markdown("---")
st.caption("""
🥬 **Panduan Budidaya Sayuran** - Step-by-step guide untuk sukses bertani sayuran

💡 **Integrasi dengan Modul Lain:**
- 🌍 **pH Tanah & Ketinggian** - Cek kesesuaian lahan
- 🧮 **Kalkulator Pupuk** - Hitung kebutuhan pupuk
- 🐛 **Panduan Hama & Penyakit** - Pengendalian OPT
- 🌿 **Pestisida Nabati** - Formula pestisida alami

⚠️ **Disclaimer:** Informasi ini bersifat edukatif. Hasil aktual dapat bervariasi tergantung kondisi lokal, cuaca, dan manajemen. Konsultasikan dengan PPL untuk rekomendasi spesifik.

🌱 **Prinsip Sukses:** Persiapan Matang + Pemeliharaan Rutin + Monitoring Ketat = Panen Melimpah!

📚 **Referensi:** Balai Penelitian Tanaman Sayuran, Kementerian Pertanian RI, Pengalaman Petani Sukses
""")
