"""
 SOP Budidaya Padi - Standard Operating Procedures
Complete SOP for rice cultivation from land preparation to harvest
"""

import streamlit as st
import pandas as pd

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
    from design_system import apply_design_system, icon, COLORS

st.set_page_config(page_title="SOP Budidaya", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('clipboard-list', size='lg')} SOP Budidaya</h1>", unsafe_allow_html=True)
st.markdown("**Standard Operating Procedure lengkap budidaya padi**")
st.markdown("---")

# Tabs for different phases
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    " Persiapan", " Tanam", " Pemeliharaan", " Panen", " Checklist"
])

with tab1:
    st.header(" SOP Persiapan Lahan & Bibit")
    
    st.subheader("A. Persiapan Lahan")
    
    sop_lahan = pd.DataFrame({
        'No': [1, 2, 3, 4, 5],
        'Kegiatan': [
            'Pembersihan lahan',
            'Pengolahan tanah I (bajak)',
            'Pengolahan tanah II (garu)',
            'Pemupukan dasar',
            'Perataan & penggenangan'
        ],
        'Waktu': [
            '3-4 minggu sebelum tanam',
            '2-3 minggu sebelum tanam',
            '1-2 minggu sebelum tanam',
            '1 minggu sebelum tanam',
            '3-5 hari sebelum tanam'
        ],
        'Detail': [
            'Bersihkan gulma, jerami, ratakan pematang',
            'Bajak sedalam 15-20 cm, 2x bolak-balik',
            'Garu hingga lumpur halus dan rata',
            'Pupuk organik 2-3 ton/ha, ratakan',
            'Ratakan, genangan air 5-10 cm'
        ]
    })
    
    st.dataframe(sop_lahan, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("B. Persiapan Bibit")
    
    sop_bibit = pd.DataFrame({
        'No': [1, 2, 3, 4, 5],
        'Kegiatan': [
            'Pemilihan benih',
            'Perendaman benih',
            'Peram benih',
            'Penyemaian',
            'Perawatan semai'
        ],
        'Waktu': [
            '25 hari sebelum tanam',
            '24 hari sebelum tanam',
            '22 hari sebelum tanam',
            '20 hari sebelum tanam',
            '0-20 hari'
        ],
        'Detail': [
            'Benih bersertifikat, 25-30 kg/ha',
            'Rendam 24 jam, buang yang mengapung',
            'Tiriskan, peram 48 jam hingga berkecambah',
            'Sebar di bedengan, tutup tipis dengan tanah',
            'Siram pagi/sore, jaga kelembaban'
        ]
    })
    
    st.dataframe(sop_bibit, use_container_width=True, hide_index=True)

with tab2:
    st.header(" SOP Penanaman")
    
    sop_tanam = pd.DataFrame({
        'No': [1, 2, 3, 4, 5, 6],
        'Kegiatan': [
            'Pencabutan bibit',
            'Sortir bibit',
            'Penanaman',
            'Jarak tanam',
            'Kedalaman tanam',
            'Penyulaman'
        ],
        'Standar': [
            'Umur 18-25 hari, tinggi 20-25 cm',
            'Pilih bibit sehat, 4-5 daun',
            'Pagi hari (7-10 pagi)',
            '25x25 cm atau Jajar Legowo',
            '2-3 cm, jangan terlalu dalam',
            '7-10 hari setelah tanam'
        ],
        'Keterangan': [
            'Cabut hati-hati, jangan rusak akar',
            'Buang bibit sakit/kerdil',
            'Hindari siang hari (stress)',
            '2-3 bibit per lubang',
            'Akar tertutup tanah, tidak terlalu dalam',
            'Ganti bibit mati/tidak tumbuh'
        ]
    })
    
    st.dataframe(sop_tanam, use_container_width=True, hide_index=True)

with tab3:
    st.header(" SOP Pemeliharaan")
    
    st.subheader("A. Pengairan")
    
    sop_air = pd.DataFrame({
        'Fase': ['Vegetatif (0-60 HST)', 'Generatif (60-90 HST)', 'Pemasakan (90-120 HST)'],
        'Genangan': ['3-5 cm', '5-10 cm', 'Dikurangi bertahap'],
        'Keterangan': [
            'Jaga kelembaban, jangan kering',
            'Penting saat pembungaan, jangan kering',
            'Keringkan 2 minggu sebelum panen'
        ]
    })
    
    st.dataframe(sop_air, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("B. Pemupukan")
    
    sop_pupuk = pd.DataFrame({
        'Waktu': ['0 HST (Dasar)', '10-15 HST', '30-35 HST', '50-55 HST'],
        'Urea (kg/ha)': [0, 100, 100, 50],
        'NPK (kg/ha)': [200, 0, 100, 0],
        'SP-36 (kg/ha)': [100, 0, 0, 0],
        'Cara Aplikasi': [
            'Campur tanah saat olah lahan',
            'Tabur merata, genangan 3-5 cm',
            'Tabur merata, genangan 3-5 cm',
            'Tabur merata, genangan 5-10 cm'
        ]
    })
    
    st.dataframe(sop_pupuk, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("C. Penyiangan")
    
    st.markdown("""
    - **Waktu:** 2-3 minggu setelah tanam, ulangi 4-5 minggu setelah tanam
    - **Cara:** Manual (gasrok) atau herbisida
    - **Tujuan:** Kurangi kompetisi gulma, aerasi tanah
    """)
    
    st.markdown("---")
    
    st.subheader("D. Pengendalian Hama/Penyakit")
    
    st.markdown("""
    - **Monitoring:** 2x seminggu, catat populasi hama
    - **Ambang ekonomi:** Aplikasi pestisida jika melewati ambang
    - **Cara aplikasi:** Pagi (7-9) atau sore (15-17), gunakan APD
    - **Rotasi:** Ganti jenis pestisida untuk hindari resistensi
    """)

with tab4:
    st.header(" SOP Panen & Pasca Panen")
    
    st.subheader("A. Panen")
    
    sop_panen = pd.DataFrame({
        'No': [1, 2, 3, 4, 5],
        'Kegiatan': [
            'Penentuan waktu panen',
            'Persiapan alat',
            'Pemotongan',
            'Pengikatan',
            'Perontokan'
        ],
        'Standar': [
            'Gabah kuning 90-95%, kadar air 22-26%',
            'Sabit/mesin panen bersih dan tajam',
            'Potong 15-20 cm dari pangkal',
            'Ikat dalam bundel, jangan terlalu besar',
            'Maksimal 24 jam setelah potong'
        ],
        'Keterangan': [
            'Pagi hari (7-10), hindari hujan',
            'Bersihkan dari kotoran',
            'Hindari gabah rontok',
            'Mudah diangkut dan dirontok',
            'Hindari kehilangan hasil'
        ]
    })
    
    st.dataframe(sop_panen, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("B. Pasca Panen")
    
    sop_pasca = pd.DataFrame({
        'No': [1, 2, 3, 4],
        'Kegiatan': [
            'Pengeringan',
            'Pembersihan',
            'Penyimpanan',
            'Penggilingan'
        ],
        'Standar': [
            'Kadar air 14%, jemur 2-3 hari',
            'Bersihkan dari kotoran, gabah hampa',
            'Tempat kering, ventilasi baik',
            'Rendemen 60-65%'
        ],
        'Keterangan': [
            'Bolak-balik teratur, hindari hujan',
            'Gunakan ayakan atau mesin',
            'Cek berkala, fumigasi jika perlu',
            'Sortasi kualitas beras'
        ]
    })
    
    st.dataframe(sop_pasca, use_container_width=True, hide_index=True)

with tab5:
    st.header(" Checklist Budidaya Padi")
    
    st.markdown("###  Checklist Persiapan")
    
    prep_checks = [
        "Lahan dibersihkan dari gulma dan sisa tanaman",
        "Tanah dibajak 2-3 kali hingga gembur",
        "Pupuk dasar sudah diaplikasikan",
        "Lahan diratakan dan digenangi",
        "Benih bersertifikat sudah disiapkan",
        "Persemaian sudah dibuat",
        "Bibit umur 18-25 hari siap tanam"
    ]
    
    for check in prep_checks:
        st.checkbox(check, key=f"prep_{check[:20]}")
    
    st.markdown("---")
    st.markdown("###  Checklist Pemeliharaan")
    
    maint_checks = [
        "Penyulaman sudah dilakukan (7-10 HST)",
        "Pemupukan I sudah dilakukan (10-15 HST)",
        "Penyiangan I sudah dilakukan (20-25 HST)",
        "Pemupukan II sudah dilakukan (30-35 HST)",
        "Penyiangan II sudah dilakukan (40-45 HST)",
        "Pemupukan III sudah dilakukan (50-55 HST)",
        "Monitoring hama/penyakit rutin 2x/minggu",
        "Pengairan sesuai fase pertumbuhan"
    ]
    
    for check in maint_checks:
        st.checkbox(check, key=f"maint_{check[:20]}")
    
    st.markdown("---")
    st.markdown("###  Checklist Panen")
    
    harvest_checks = [
        "Gabah sudah menguning 90-95%",
        "Kadar air 22-26% (cek dengan moisture meter)",
        "Alat panen sudah disiapkan",
        "Cuaca cerah (tidak hujan)",
        "Panen dilakukan pagi hari",
        "Perontokan maksimal 24 jam setelah potong",
        "Pengeringan hingga kadar air 14%",
        "Penyimpanan di tempat kering dan bersih"
    ]
    
    for check in harvest_checks:
        st.checkbox(check, key=f"harvest_{check[:20]}")

st.markdown("---")
st.success(" **Penting:** Ikuti SOP dengan konsisten untuk hasil optimal dan kualitas terbaik")
