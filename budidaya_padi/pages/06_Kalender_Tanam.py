"""
 Kalender Tanam - Rice Planting Calendar
Season-based planting recommendations
"""

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime, timedelta

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

st.set_page_config(page_title="Kalender Tanam", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('calendar-alt', size='lg')} Kalender Tanam</h1>", unsafe_allow_html=True)
st.markdown("**Rekomendasi waktu tanam berdasarkan musim dan pola hujan**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([" Kalender", " Pola Musim", " Rekomendasi"])

with tab1:
    st.header(" Kalender Tanam Padi")
    
    # Input
    col1, col2 = st.columns(2)
    
    with col1:
        region = st.selectbox("Pilih Region", [
            "Jawa Barat", "Jawa Tengah", "Jawa Timur",
            "Sumatera Utara", "Sumatera Selatan",
            "Sulawesi Selatan", "Bali"
        ])
    
    with col2:
        irrigation = st.selectbox("Jenis Irigasi", [
            "Irigasi Teknis (Air Tersedia Sepanjang Tahun)",
            "Irigasi Sederhana (Tergantung Hujan)",
            "Tadah Hujan"
        ])
    
    st.markdown("---")
    
    # Planting calendar
    st.subheader(" Jadwal Tanam Optimal")
    
    # --- PRANATA MANGSA LOGIC ---
    def get_pranata_mangsa(date):
        day = date.day
        month = date.month
        
        if (month == 6 and day >= 22) or (month == 8 and day <= 1):
            return "Kasa (I)", "Masa kering, daun gugur, belalang bertelur. Mulai olah tanah kering.", " Kering"
        elif (month == 8 and day >= 2) or (month == 8 and day <= 24):
            return "Karo (II)", "Tanah merekah, pohon randu bersemi. Persiapan palawija.", " Kering/Pancaroba"
        elif (month == 8 and day >= 25) or (month == 9 and day <= 17):
            return "Katelu (III)", "Sumur kering, angin kencang. Panen palawija.", " Kering Panas"
        elif (month == 9 and day >= 18) or (month == 10 and day <= 13):
            return "Kapat (IV)", "Mata air mulai basah, hujan pertama (labuh). Persiapan persemaian.", " Labuh (Hujan Awal)"
        elif (month == 10 and day >= 14) or (month == 11 and day <= 8):
            return "Kalima (V)", "Hujan mulai sering, selokan air mengalir. Waktu Tanam Padi Utama.", " Hujan Mulai Stabil"
        elif (month == 11 and day >= 9) or (month == 12 and day <= 21):
            return "Kanem (VI)", "Musim buah-buahan. Hujan lebat. Tanam padi terus berlangsung.", " Hujan Lebat"
        elif (month == 12 and day >= 22) or (month == 2 and day <= 2):
            return "Kapitu (VII)", "Banjir, angin ribut. Puncak musim hujan. Perawatan tanaman.", " Puncak Hujan"
        elif (month == 2 and day >= 3) or (month == 2 and day <= 28): # Simplified Feb
            return "Kawolu (VIII)", "Padi bunting, ulat banyak. Mulai sedikit panas.", " Hujan Berkurang"
        elif (month == 3 and day >= 1) or (month == 3 and day <= 25):
            return "Kasanga (IX)", "Bunyi garengpung. Padi mulai tua. Menjelang panen.", " Pancaroba Akhir"
        elif (month == 3 and day >= 26) or (month == 4 and day <= 18):
            return "Kadasa (X)", "Padi menguning, banyak burung. Panen Raya.", " Mareng (Kering Awal)"
        elif (month == 4 and day >= 19) or (month == 5 and day <= 11):
            return "Desta (XI)", "Suhu dingin di malam hari. Panen palawija.", " Kering"
        else: # (month == 5 and day >= 12) or (month == 6 and day <= 21)
            return "Sada (XII)", "Suhu dingin siang hari. Jemur gabah.", " Kering Dingin"

    today = datetime.now()
    mangsa_name, mangsa_desc, mangsa_weather = get_pranata_mangsa(today)
    
    # --- PRIMBON LOGIC (Simplified Javanese Market Day) ---
    # Epoch: 1 Jan 2024 was Monday Pahing
    # Pasaran: Legi, Pahing, Pon, Wage, Kliwon (5 day cycle)
    known_date = datetime(2024, 1, 1)
    delta_days = (today - known_date).days
    pasaran_list = ["Pahing", "Pon", "Wage", "Kliwon", "Legi"] # Cycle starting from known date
    today_pasaran = pasaran_list[delta_days % 5]
    
    recommendation_primbon = ""
    if today_pasaran == "Legi": recommendation_primbon = " Baik untuk Tanam (Manis/Subur)"
    elif today_pasaran == "Wage": recommendation_primbon = " Kurang Baik (Kering/Gagal)"
    else: recommendation_primbon = " Netral"

    # Display Kearifan Lokal
    st.markdown("###  Kearifan Lokal (Pranata Mangsa & Primbon)")
    col_k1, col_k2 = st.columns(2)
    with col_k1:
        st.info(f"**Mangsa Saat Ini:** {mangsa_name}")
        st.caption(f"{mangsa_desc} ({mangsa_weather})")
    with col_k2:
        st.success(f"**Hari Ini:** {today.strftime('%A')}, {today_pasaran}")
        st.caption(f"Status Primbon Tanam: **{recommendation_primbon}**")

    st.markdown("---")
    
    if "Teknis" in irrigation:
        st.success(" **Irigasi Teknis:** Dapat tanam 2-3x per tahun")
        
        calendar_df = pd.DataFrame({
            'Musim Tanam': ['MT I (Musim Hujan)', 'MT II (Pancaroba)', 'MT III (Kemarau)'],
            'Bulan Tanam': ['Oktober - November', 'Februari - Maret', 'Juni - Juli'],
            'Bulan Panen': ['Februari - Maret', 'Juni - Juli', 'Oktober - November'],
            'Produktivitas': ['Tinggi (6-8 ton/ha)', 'Sedang (5-7 ton/ha)', 'Sedang (5-6 ton/ha)'],
            'Risiko': ['Rendah', 'Sedang (Hama)', 'Tinggi (Air)']
        })
    
    elif "Sederhana" in irrigation:
        st.warning(" **Irigasi Sederhana:** Dapat tanam 2x per tahun")
        
        calendar_df = pd.DataFrame({
            'Musim Tanam': ['MT I (Musim Hujan)', 'MT II (Pancaroba)'],
            'Bulan Tanam': ['Oktober - November', 'Februari - Maret'],
            'Bulan Panen': ['Februari - Maret', 'Juni - Juli'],
            'Produktivitas': ['Tinggi (6-7 ton/ha)', 'Sedang (5-6 ton/ha)'],
            'Risiko': ['Rendah', 'Sedang']
        })
    
    else:  # Tadah Hujan
        st.info(" **Tadah Hujan:** Hanya 1x per tahun (musim hujan)")
        
        calendar_df = pd.DataFrame({
            'Musim Tanam': ['MT I (Musim Hujan)'],
            'Bulan Tanam': ['Oktober - November'],
            'Bulan Panen': ['Februari - Maret'],
            'Produktivitas': ['Sedang (4-6 ton/ha)'],
            'Risiko': ['Tinggi (Kekeringan)']
        })
    
    st.dataframe(calendar_df, use_container_width=True, hide_index=True)
    
    # Timeline visualization
    st.subheader(" Timeline Tanam-Panen")
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
    
    if "Teknis" in irrigation:
        timeline_data = pd.DataFrame({
            'Bulan': months * 3,
            'Musim': ['MT I']*12 + ['MT II']*12 + ['MT III']*12,
            'Status': [
                '', '', 'Panen', '', '', '', '', '', '', 'Tanam', 'Tanam', '',  # MT I
                'Tanam', 'Tanam', '', '', '', 'Panen', 'Panen', '', '', '', '', '',  # MT II
                '', '', '', '', '', '', 'Tanam', '', '', 'Panen', 'Panen', ''  # MT III
            ]
        })
    else:
        timeline_data = pd.DataFrame({
            'Bulan': months * 2,
            'Musim': ['MT I']*12 + ['MT II']*12,
            'Status': [
                '', '', 'Panen', '', '', '', '', '', '', 'Tanam', 'Tanam', '',  # MT I
                'Tanam', 'Tanam', '', '', '', 'Panen', 'Panen', '', '', '', '', ''  # MT II
            ]
        })
    
    # Filter only planting and harvest
    timeline_display = timeline_data[timeline_data['Status'] != '']
    
    if not timeline_display.empty:
        chart = alt.Chart(timeline_display).mark_bar().encode(
            x=alt.X('Bulan:N', title='Bulan', sort=months),
            y=alt.Y('Musim:N', title='Musim Tanam'),
            color=alt.Color('Status:N', scale=alt.Scale(domain=['Tanam', 'Panen'], range=['#4CAF50', '#FFC107'])),
            tooltip=['Bulan', 'Musim', 'Status']
        ).properties(
            title='Timeline Tanam-Panen Sepanjang Tahun',
            height=300
        )
        
        st.altair_chart(chart, use_container_width=True)

with tab2:
    st.header(" Pola Musim Indonesia")
    
    st.markdown("""
    ### Karakteristik Musim
    
    **Musim Hujan (Oktober - Maret):**
    - Curah hujan tinggi (200-400 mm/bulan)
    - Cocok untuk tanam padi sawah
    - Risiko banjir di dataran rendah
    - Hama/penyakit lebih aktif
    
    **Musim Kemarau (April - September):**
    - Curah hujan rendah (<100 mm/bulan)
    - Perlu irigasi memadai
    - Risiko kekeringan
    - Hama tikus meningkat
    
    **Pancaroba (Maret-April, September-Oktober):**
    - Peralihan musim
    - Curah hujan tidak menentu
    - Perlu monitoring cuaca
    """)
    
    # Rainfall pattern
    rainfall_df = pd.DataFrame({
        'Bulan': months,
        'Curah Hujan (mm)': [350, 300, 250, 150, 100, 80, 60, 50, 80, 150, 250, 350]
    })
    
    rainfall_chart = alt.Chart(rainfall_df).mark_area(
        line={'color': '#1976D2'},
        color=alt.Gradient(
            gradient='linear',
            stops=[alt.GradientStop(color='white', offset=0),
                   alt.GradientStop(color='#1976D2', offset=1)],
            x1=0, x2=0, y1=1, y2=0
        )
    ).encode(
        x=alt.X('Bulan:N', title='Bulan', sort=months),
        y=alt.Y('Curah Hujan (mm):Q', title='Curah Hujan (mm)'),
        tooltip=['Bulan', 'Curah Hujan (mm)']
    ).properties(
        title='Pola Curah Hujan Rata-rata',
        height=300
    )
    
    st.altair_chart(rainfall_chart, use_container_width=True)

with tab3:
    st.header(" Rekomendasi Tanam")
    
    st.subheader(" Waktu Tanam Terbaik")
    
    col_rec1, col_rec2 = st.columns(2)
    
    with col_rec1:
        st.markdown("""
        ### MT I (Oktober-November)
        **Keunggulan:**
        - Air melimpah dari hujan
        - Produktivitas tertinggi
        - Biaya irigasi rendah
        
        **Risiko:**
        - Banjir (dataran rendah)
        - Hama/penyakit aktif
        - Harga jual rendah (panen massal)
        
        **Rekomendasi:**
         Sangat direkomendasikan untuk semua jenis irigasi
        """)
    
    with col_rec2:
        st.markdown("""
        ### MT II (Februari-Maret)
        **Keunggulan:**
        - Cuaca masih mendukung
        - Harga jual lebih baik
        - Hama lebih terkendali
        
        **Risiko:**
        - Perlu irigasi tambahan
        - Produktivitas sedikit turun
        
        **Rekomendasi:**
         Direkomendasikan untuk irigasi teknis/sederhana
        """)
    
    st.markdown("---")
    
    st.subheader(" Tips Pemilihan Waktu Tanam")
    
    tips = [
        "**Tanam serentak** dalam satu hamparan untuk kendalikan hama",
        "**Perhatikan prakiraan cuaca** sebelum tanam",
        "**Hindari tanam** saat puncak musim kemarau (Juli-Agustus)",
        "**Koordinasi dengan kelompok tani** untuk jadwal tanam bersama",
        "**Pilih varietas** sesuai umur tanam dan musim",
        "**Siapkan cadangan air** untuk musim kemarau"
    ]
    
    for tip in tips:
        st.info(tip)

st.markdown("---")
st.success(" **Kesimpulan:** Waktu tanam optimal adalah Oktober-November (MT I) untuk semua jenis irigasi")
