"""
 Panduan Budidaya Padi - Complete Rice Cultivation Guide
Step-by-step guide for successful rice farming
"""

import streamlit as st
import pandas as pd
import altair as alt

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

# Page config
st.set_page_config(
    page_title="Panduan Budidaya Padi",
    page_icon="",
    layout="wide"
)

# Apply Design System
apply_design_system()

# Header
st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('book-open', size='lg')} Panduan Budidaya</h1>", unsafe_allow_html=True)
st.markdown("**Panduan lengkap budidaya padi dari persiapan hingga panen**")
st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    " Persiapan", " Penanaman", " Pemeliharaan", " Panen", " Timeline"
])

with tab1:
    st.header(" Persiapan Lahan & Bibit")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Persiapan Lahan")
        st.markdown("""
        **Langkah-langkah:**
        1. **Pembersihan Lahan**
           - Bersihkan gulma dan sisa tanaman
           - Ratakan permukaan tanah
           - Perbaiki pematang sawah
        
        2. **Pengolahan Tanah**
           - Bajak tanah 2-3 kali
           - Garu hingga lumpur merata
           - Genangan air 5-10 cm
        
        3. **Pemupukan Dasar**
           - Pupuk organik: 2-3 ton/ha
           - Aplikasi 1-2 minggu sebelum tanam
           - Ratakan dengan tanah
        """)
        
        st.info(" **Tips:** Pengolahan tanah yang baik menentukan 50% keberhasilan budidaya!")
    
    with col2:
        st.subheader("2. Persiapan Bibit")
        st.markdown("""
        **Persemaian:**
        1. **Lokasi Persemaian**
           - Dekat sumber air
           - Tanah subur dan gembur
           - Terlindung dari hama
        
        2. **Penyemaian**
           - Benih: 25-30 kg/ha
           - Rendam benih 24 jam
           - Peram 48 jam hingga berkecambah
           - Sebar di bedengan
        
        3. **Perawatan Semai**
           - Jaga kelembaban
           - Siram pagi dan sore
           - Siap tanam umur 18-25 hari
        """)
        
        st.success(" Bibit siap tanam: tinggi 20-25 cm, 4-5 daun")

with tab2:
    st.header(" Penanaman")
    
    # Planting methods comparison
    st.subheader(" Perbandingan Metode Tanam")
    
    methods_df = pd.DataFrame({
        'Metode': ['Transplanting', 'Direct Seeding', 'SRI', 'Jajar Legowo'],
        'Bibit (kg/ha)': [25, 60, 10, 25],
        'Tenaga Kerja': ['Tinggi', 'Rendah', 'Sedang', 'Tinggi'],
        'Produktivitas': ['Sedang', 'Rendah', 'Tinggi', 'Sangat Tinggi'],
        'Biaya': ['Tinggi', 'Rendah', 'Sedang', 'Tinggi']
    })
    
    st.dataframe(methods_df, use_container_width=True, hide_index=True)
    
    col_method1, col_method2, col_method3, col_method4 = st.columns(4)
    
    with col_method1:
        st.markdown("""
        ** Transplanting**
        - Jarak: 25x25 cm
        - 2-3 bibit/lubang
        - Umur: 18-25 hari
        
         Paling umum
        """)
    
    with col_method2:
        st.markdown("""
        ** Direct Seeding**
        - Benih langsung
        - Tanpa persemaian
        - Hemat tenaga
        
         Lahan luas
        """)
    
    with col_method3:
        st.markdown("""
        ** SRI**
        - Bibit muda 8-12 hari
        - 1 bibit/lubang
        - Jarak: 30x30 cm
        
         Hemat air
        """)
    
    with col_method4:
        st.markdown("""
        ** Jajar Legowo**
        - Sistem baris
        - Populasi tinggi
        - Produktivitas ++
        
         Hasil maksimal
        """)
    
    st.markdown("---")
    
    # Jajar Legowo Calculator
    st.subheader(" Kalkulator Jajar Legowo")
    
    col_jl1, col_jl2 = st.columns(2)
    
    with col_jl1:
        st.markdown("**Pilih Sistem Jajar Legowo:**")
        jl_system = st.selectbox(
            "Sistem",
            ["Legowo 2:1 (25x12.5x50)", "Legowo 3:1 (25x12.5x50)", "Legowo 4:1 (25x12.5x50)", "Legowo 2:1 (20x10x40)"],
            help="Format: jarak dalam baris x jarak antar rumpun x jarak antar kelompok"
        )
        
        luas_lahan_jl = st.number_input("Luas Lahan (ha)", 0.1, 100.0, 1.0, 0.1, key="jl_luas")
        bibit_per_lubang = st.number_input("Bibit per Lubang", 1, 5, 2, 1, key="jl_bibit")
        anakan_produktif = st.number_input(
            "Anakan Produktif per Rumpun", 
            5, 50, 20, 1, 
            key="jl_anakan",
            help="Jumlah anakan produktif yang menghasilkan malai per rumpun (rata-rata 15-25)"
        )
    
    with col_jl2:
        st.markdown("**Parameter Hasil:**")
        panjang_malai = st.number_input("Panjang Malai (cm)", 15.0, 35.0, 25.0, 0.5, help="Rata-rata panjang malai")
        bulir_per_malai = st.number_input("Bulir per Malai", 80, 200, 120, 5, help="Jumlah bulir per malai")
        berat_1000_bulir = st.number_input("Berat 1000 Bulir (gram)", 20.0, 35.0, 27.0, 0.5, help="Berat 1000 butir gabah")
    
    if st.button(" Hitung Populasi & Potensi Hasil", type="primary", key="calc_jl"):
        # Parse system
        if "2:1" in jl_system and "25x12.5" in jl_system:
            jarak_dalam = 25  # cm
            jarak_antar = 12.5  # cm
            jarak_lorong = 50  # cm
            ratio = 2
        elif "3:1" in jl_system:
            jarak_dalam = 25
            jarak_antar = 12.5
            jarak_lorong = 50
            ratio = 3
        elif "4:1" in jl_system:
            jarak_dalam = 25
            jarak_antar = 12.5
            jarak_lorong = 50
            ratio = 4
        else:  # 2:1 (20x10x40)
            jarak_dalam = 20
            jarak_antar = 10
            jarak_lorong = 40
            ratio = 2
        
        # Calculate population
        # Legowo pattern: ratio rows + 1 lorong
        lebar_unit = (ratio * jarak_dalam) + jarak_lorong  # cm
        
        # Rumpun per meter persegi
        # Dalam 1 meter: jumlah baris dalam 1 unit legowo
        # Contoh Legowo 2:1: 2 baris dalam (25+25=50cm) + 1 lorong (50cm) = 100cm total
        # Jarak antar rumpun dalam baris = 12.5 cm
        
        # Jumlah rumpun per meter baris
        rumpun_per_meter_baris = 100 / jarak_antar  # rumpun per meter
        
        # Jumlah baris per meter lebar
        baris_per_meter = (100 / lebar_unit) * ratio * 2  # 2 baris per sisi
        
        # Total rumpun per m2
        rumpun_per_m2 = (rumpun_per_meter_baris * baris_per_meter) / ratio
        
        # Total per ha (10,000 m2)
        populasi_per_ha = rumpun_per_m2 * 10000
        total_populasi = populasi_per_ha * luas_lahan_jl
        
        # Yield calculation
        # Potensi hasil = populasi × anakan produktif × bulir/malai × berat bulir
        total_anakan = total_populasi * anakan_produktif
        total_bulir = total_anakan * bulir_per_malai
        total_berat_gram = total_bulir * (berat_1000_bulir / 1000)
        total_berat_kg = total_berat_gram / 1000
        total_berat_ton = total_berat_kg / 1000
        
        # Per hectare
        hasil_per_ha = total_berat_ton / luas_lahan_jl
        
        st.success(" Perhitungan Selesai!")
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.metric("Populasi Rumpun/ha", f"{populasi_per_ha:,.0f}")
            st.metric("Total Rumpun", f"{total_populasi:,.0f}")
        
        with col_res2:
            st.metric("Total Anakan Produktif", f"{total_anakan:,.0f}")
            st.metric("Total Malai", f"{total_anakan:,.0f}")
        
        with col_res3:
            st.metric("Potensi Hasil/ha", f"{hasil_per_ha:.2f} ton")
            st.metric("Total Hasil", f"{total_berat_ton:.2f} ton")
        
        # Detailed breakdown
        st.markdown("---")
        st.subheader(" Rincian Perhitungan")
        
        breakdown = pd.DataFrame({
            'Parameter': [
                'Sistem Tanam',
                'Luas Lahan',
                'Populasi Rumpun/ha',
                'Bibit per Lubang',
                'Anakan Produktif/Rumpun',
                'Total Anakan Produktif',
                'Panjang Malai Rata-rata',
                'Bulir per Malai',
                'Total Bulir',
                'Berat 1000 Bulir',
                'Potensi Hasil per ha',
                'Total Potensi Hasil'
            ],
            'Nilai': [
                jl_system,
                f"{luas_lahan_jl} ha",
                f"{populasi_per_ha:,.0f} rumpun",
                f"{bibit_per_lubang} bibit",
                f"{anakan_produktif} anakan",
                f"{total_anakan:,.0f} anakan",
                f"{panjang_malai} cm",
                f"{bulir_per_malai} bulir",
                f"{total_bulir:,.0f} bulir",
                f"{berat_1000_bulir} gram",
                f"{hasil_per_ha:.2f} ton",
                f"{total_berat_ton:.2f} ton"
            ]
        })
        
        st.dataframe(breakdown, use_container_width=True, hide_index=True)
        
        st.info(f"""
         **Keunggulan Jajar Legowo {jl_system.split()[1]}:**
        - Populasi {((populasi_per_ha / 160000) * 100):.0f}% dari sistem konvensional (25x25 cm)
        - Tanaman pinggir lebih banyak (efek tepi)
        - Sirkulasi udara lebih baik
        - Memudahkan pemeliharaan
        - Potensi hasil +15-20% dari konvensional
        """)


with tab3:
    st.header(" Pemeliharaan Tanaman")
    
    st.subheader(" Pengairan")
    st.markdown("""
    **Fase Vegetatif (0-60 HST):**
    - Genangan 3-5 cm
    - Jaga kelembaban tanah
    
    **Fase Generatif (60-90 HST):**
    - Genangan 5-10 cm
    - Penting saat pembungaan
    
    **Fase Pemasakan (90-120 HST):**
    - Kurangi air bertahap
    - Keringkan 2 minggu sebelum panen
    
     **AWD (Alternate Wetting & Drying):** Hemat air 30% tanpa kurangi hasil!
    """)
    
    st.markdown("---")
    
    st.subheader(" Pemupukan")
    
    fertilizer_schedule = pd.DataFrame({
        'Waktu': ['0 HST (Dasar)', '10-15 HST', '30-35 HST', '50-55 HST'],
        'Urea (kg/ha)': [0, 100, 100, 50],
        'NPK (kg/ha)': [200, 0, 100, 0],
        'SP-36 (kg/ha)': [100, 0, 0, 0],
        'Tujuan': ['Persiapan', 'Anakan', 'Malai', 'Pengisian']
    })
    
    st.dataframe(fertilizer_schedule, use_container_width=True, hide_index=True)
    
    # Altair chart for fertilizer schedule
    chart_data = pd.DataFrame({
        'HST': [0, 10, 30, 50, 0, 10, 30, 50],
        'Pupuk': ['Urea', 'Urea', 'Urea', 'Urea', 'NPK', 'NPK', 'NPK', 'NPK'],
        'Dosis': [0, 100, 100, 50, 200, 0, 100, 0]
    })
    
    chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x=alt.X('HST:Q', title='Hari Setelah Tanam (HST)'),
        y=alt.Y('Dosis:Q', title='Dosis (kg/ha)'),
        color='Pupuk:N',
        tooltip=['HST', 'Pupuk', 'Dosis']
    ).properties(
        title='Jadwal Pemupukan',
        height=300
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
    st.markdown("---")
    
    st.subheader(" Pengendalian Hama & Penyakit")
    
    col_pest1, col_pest2 = st.columns(2)
    
    with col_pest1:
        st.markdown("""
        **Hama Utama:**
        1. **Wereng Coklat**
           - Gejala: Hopperburn
           - Pengendalian: Varietas tahan, insektisida
        
        2. **Penggerek Batang**
           - Gejala: Sundep, beluk
           - Pengendalian: Sanitasi, perangkap
        
        3. **Walang Sangit**
           - Gejala: Gabah hampa
           - Pengendalian: Hand picking, insektisida
        """)
    
    with col_pest2:
        st.markdown("""
        **Penyakit Utama:**
        1. **Blast (Blas)**
           - Gejala: Bercak daun
           - Pengendalian: Fungisida, varietas tahan
        
        2. **Hawar Daun Bakteri**
           - Gejala: Daun menguning
           - Pengendalian: Varietas tahan, sanitasi
        
        3. **Tungro**
           - Gejala: Daun kuning-oranye
           - Pengendalian: Kendalikan wereng
        """)

with tab4:
    st.header(" Panen & Pasca Panen")
    
    col_harvest1, col_harvest2 = st.columns(2)
    
    with col_harvest1:
        st.subheader(" Panen")
        st.markdown("""
        **Waktu Panen yang Tepat:**
        - Umur: 110-150 hari (tergantung varietas)
        - Gabah menguning 90-95%
        - Kadar air: 22-26%
        - Pagi hari (7-10 pagi)
        
        **Cara Panen:**
        1. Potong batang 15-20 cm dari pangkal
        2. Ikat dalam bundel
        3. Perontokan segera (max 24 jam)
        4. Hindari kehilangan hasil
        
         **Jangan terlambat panen:** Gabah rontok, kualitas turun!
        """)
    
    with col_harvest2:
        st.subheader(" Pasca Panen")
        st.markdown("""
        **Pengeringan:**
        - Target kadar air: 14%
        - Jemur 2-3 hari
        - Bolak-balik teratur
        - Hindari hujan
        
        **Penyimpanan:**
        - Tempat kering & bersih
        - Ventilasi baik
        - Fumigasi jika perlu
        - Cek berkala
        
        **Penggilingan:**
        - Rendemen: 60-65%
        - Gabah → Beras
        - Sortasi kualitas
        """)
    
    # Yield calculation
    st.subheader(" Estimasi Hasil")
    
    col_yield1, col_yield2, col_yield3 = st.columns(3)
    
    with col_yield1:
        lahan_panen = st.number_input("Luas Lahan (ha)", value=1.0, step=0.1, key="harvest_area")
    
    with col_yield2:
        produktivitas = st.number_input("Produktivitas (ton/ha)", value=6.0, step=0.5, key="productivity")
    
    with col_yield3:
        rendemen = st.slider("Rendemen (%)", 55, 70, 63, key="rendemen")
    
    gabah_total = lahan_panen * produktivitas * 1000  # kg
    beras_total = gabah_total * (rendemen / 100)
    
    col_result1, col_result2 = st.columns(2)
    
    with col_result1:
        st.metric("Total Gabah Kering Giling (GKG)", f"{gabah_total:,.0f} kg")
    
    with col_result2:
        st.metric("Total Beras", f"{beras_total:,.0f} kg")

with tab5:
    st.header(" Timeline Budidaya Padi")
    
    # Create timeline data
    timeline_data = pd.DataFrame({
        'Fase': ['Persiapan Lahan', 'Persemaian', 'Tanam', 'Vegetatif', 
                'Generatif', 'Pemasakan', 'Panen'],
        'Mulai': [0, 0, 20, 25, 60, 90, 115],
        'Selesai': [20, 20, 25, 60, 90, 115, 120],
        'Durasi': [20, 20, 5, 35, 30, 25, 5]
    })
    
    # Altair Gantt chart
    gantt = alt.Chart(timeline_data).mark_bar().encode(
        x=alt.X('Mulai:Q', title='Hari Setelah Tanam (HST)'),
        x2='Selesai:Q',
        y=alt.Y('Fase:N', title='Fase Budidaya'),
        color=alt.Color('Fase:N', legend=None),
        tooltip=['Fase', 'Mulai', 'Selesai', 'Durasi']
    ).properties(
        title='Timeline Budidaya Padi (120 hari)',
        height=400
    )
    
    st.altair_chart(gantt, use_container_width=True)
    
    # Detailed schedule
    st.subheader(" Jadwal Detail per Fase")
    
    schedule_detail = pd.DataFrame({
        'Fase': ['Persiapan Lahan', 'Persemaian', 'Tanam', 'Vegetatif', 
                'Generatif', 'Pemasakan', 'Panen'],
        'Durasi': ['0-20 HST', '0-20 HST', '20-25 HST', '25-60 HST', 
                  '60-90 HST', '90-115 HST', '115-120 HST'],
        'Kegiatan Utama': [
            'Olah tanah, pupuk dasar',
            'Semai benih, rawat bibit',
            'Pindah tanam ke sawah',
            'Pemupukan, penyiangan, pengairan',
            'Pemupukan susulan, pengendalian hama',
            'Kurangi air, monitoring',
            'Panen, perontokan, pengeringan'
        ]
    })
    
    st.dataframe(schedule_detail, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.success("""
 **Tips Sukses Budidaya Padi:**
1. Pilih varietas sesuai kondisi lahan
2. Persiapan lahan yang baik
3. Pemupukan berimbang
4. Pengairan teratur
5. Pengendalian hama/penyakit tepat waktu
6. Panen pada waktu yang tepat
""")
