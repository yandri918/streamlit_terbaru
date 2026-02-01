"""
🌴 Budidaya Buah Tropis Luar Musim (Off-Season)
Panduan lengkap teknik induksi pembungaan untuk harga premium

Features:
- 5 Buah Premium (Durian, Manggis, Rambutan, Kelengkeng, Mangga)
- Water Stress Protocol
- PBZ Application Guide
- Fertilization Program
- Economic ROI Calculator
- Scientific References
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.offseason_fruit_service import OffSeasonFruitService

# Page config
st.set_page_config(
    page_title="Budidaya Buah Tropis Off-Season",
    page_icon="🌴",
    layout="wide"
)

# Initialize service
@st.cache_resource
def get_service():
    return OffSeasonFruitService()

service = get_service()

# Header
st.title("🌴 Budidaya Buah Tropis Luar Musim")
st.markdown("""
**Teknik Induksi Pembungaan untuk Harga Premium 2-3x Lipat!**

Modul ini memberikan panduan lengkap budidaya buah tropis di luar musim normal menggunakan teknik ilmiah terbukti:
- 🌊 **Water Stress Protocol** - Manipulasi air terkontrol
- 💊 **PBZ Application** - Regulasi hormon pertumbuhan
- 🌱 **Fertilization Program** - Pemupukan strategis
- 💰 **Economic Analysis** - Analisis ROI & profitabilitas
""")

# Sidebar - Fruit Selection
st.sidebar.header("🍇 Pilih Buah")
fruits = service.get_available_fruits()

fruit_options = {f"{f['icon']} {f['name']} ({f['nickname']})": f['key'] for f in fruits}
selected_fruit_display = st.sidebar.selectbox(
    "Pilih Komoditas:",
    options=list(fruit_options.keys())
)
selected_fruit = fruit_options[selected_fruit_display]

# Get fruit data
fruit_data = service.get_fruit_info(selected_fruit)

# Display fruit info
col1, col2, col3 = st.columns([1, 2, 2])

with col1:
    st.markdown(f"## {fruit_data['icon']}")
    st.markdown(f"### {fruit_data['name_id']}")
    st.caption(f"*{fruit_data['scientific']}*")
    st.info(f"**{fruit_data['nickname']}**")

with col2:
    st.markdown("#### 📊 Info Pasar")
    market = fruit_data['market_info']
    st.metric("Harga Normal", f"Rp {market['price_normal']:,}/kg")
    st.metric("Harga Off-Season", f"Rp {market['price_offseason']:,}/kg", 
              delta=f"+{int((market['price_multiplier']-1)*100)}%")
    
with col3:
    st.markdown("#### 🌍 Potensi Ekspor")
    st.success(market['export_potential'])
    st.markdown("#### 📅 Musim")
    st.write(f"**Normal:** {market['normal_season']}")
    st.write(f"**Target Off-Season:** {market['off_season_target']}")

st.divider()

# Main tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🌊 Water Stress",
    "💊 PBZ Application", 
    "🌱 Fertilization",
    "💰 Economic Analysis",
    "📅 Calendar",
    "📚 Scientific References"
])

# Tab 1: Water Stress Protocol
with tab1:
    st.header("🌊 Protokol Stres Air (Water Stress)")
    
    st.info(f"""
    **Prinsip:** Manipulasi ketersediaan air untuk memicu pembungaan
    
    **Durasi:** {fruit_data['cultivation_params']['water_stress_duration']}  
    **Success Rate:** {fruit_data['cultivation_params']['success_rate']}
    """)
    
    # Generate schedule
    st.subheader("📋 Jadwal Stres Air")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Tanggal Mulai Stres Air:",
            value=datetime.now()
        )
    
    if st.button("Generate Jadwal", type="primary"):
        schedule_data = service.generate_water_stress_schedule(
            selected_fruit,
            start_date.strftime("%Y-%m-%d")
        )
        
        # Display schedule
        st.success(f"✅ Jadwal berhasil dibuat!")
        st.write(f"**Total Durasi:** {schedule_data['total_duration_weeks']} minggu")
        st.write(f"**Perkiraan Pembungaan:** {schedule_data['expected_flowering']}")
        st.write(f"**Perkiraan Panen:** {schedule_data['expected_harvest']}")
        
        # Schedule table
        df_schedule = pd.DataFrame(schedule_data['schedule'])
        st.dataframe(df_schedule, use_container_width=True, hide_index=True)
        
        # Timeline visualization
        fig = go.Figure()
        
        for idx, phase in enumerate(schedule_data['schedule']):
            fig.add_trace(go.Scatter(
                x=[phase['start_date'], phase['end_date']],
                y=[idx, idx],
                mode='lines+markers',
                name=phase['phase'],
                line=dict(width=20),
                marker=dict(size=12)
            ))
        
        fig.update_layout(
            title="Timeline Stres Air",
            xaxis_title="Tanggal",
            yaxis_title="Fase",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed protocol
    st.subheader("📖 Detail Protokol per Fase")
    
    protocol = fruit_data['water_stress_protocol']
    for phase_key in ['phase_1', 'phase_2', 'phase_3']:
        phase = protocol[phase_key]
        with st.expander(f"**{phase['name']}** - {phase['duration']}"):
            st.write(f"**Tindakan:** {phase['action']}")
            st.write(f"**Indikator:** {phase['indicator']}")

# Tab 2: PBZ Application
with tab2:
    st.header("💊 Aplikasi Paclobutrazol (PBZ)")
    
    st.warning("""
    ⚠️ **PERHATIAN:**
    - PBZ adalah growth retardant yang menghambat pertumbuhan vegetatif
    - Overdosis bisa menyebabkan hambatan pertumbuhan permanen
    - Gunakan dosis yang tepat sesuai ukuran pohon
    - Konsultasikan dengan ahli jika ragu
    """)
    
    st.subheader("🧮 Kalkulator Dosis PBZ")
    
    col1, col2 = st.columns(2)
    
    with col1:
        tree_age = st.number_input(
            "Umur Pohon (tahun):",
            min_value=3,
            max_value=30,
            value=10
        )
        
    with col2:
        tree_circumference = st.number_input(
            "Lingkar Batang (cm):",
            min_value=20,
            max_value=200,
            value=75
        )
    
    if st.button("Hitung Dosis PBZ", type="primary"):
        pbz_data = service.calculate_pbz_dosage(
            selected_fruit,
            tree_age,
            tree_circumference
        )
        
        st.success(f"✅ Dosis PBZ untuk pohon Anda:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dosis", f"{pbz_data['dosage_grams']} gram/pohon")
        with col2:
            st.metric("Range Normal", pbz_data['dosage_range'])
        with col3:
            st.info(pbz_data['application_method'])
        
        st.write(f"**Waktu Aplikasi:** {pbz_data['timing']}")
        st.write(f"**Cara Pengenceran:** {pbz_data['dilution']}")
        st.warning(pbz_data['safety_note'])
    
    # PBZ Info
    st.subheader("📖 Informasi PBZ")
    
    with st.expander("Cara Kerja PBZ"):
        st.write("""
        **Paclobutrazol (PBZ)** bekerja dengan cara:
        1. Menghambat sintesis Gibberellin (GA) - hormon pertumbuhan vegetatif
        2. Meningkatkan Abscisic Acid (ABA) - hormon stres
        3. Mengalihkan energi dari pertumbuhan vegetatif ke generatif (bunga)
        4. Meningkatkan akumulasi karbohidrat di cabang produktif
        
        **Hasil:** Pembentukan primordia bunga meningkat 2-3x lipat
        """)
    
    with st.expander("Metode Aplikasi"):
        st.write("""
        **1. Soil Drench (Siram Tanah):**
        - Larutkan PBZ dalam air (5-10 liter)
        - Siram melingkar di sekitar tajuk (drip line)
        - Lebih aman, efek bertahap
        
        **2. Trunk Injection (Injeksi Batang):**
        - Bor lubang kecil di batang (45° ke bawah)
        - Masukkan larutan PBZ
        - Tutup lubang dengan lilin
        - Lebih cepat, tapi berisiko infeksi
        
        **Rekomendasi:** Soil drench untuk pemula
        """)

# Tab 3: Fertilization
with tab3:
    st.header("🌱 Program Pemupukan")
    
    st.info("""
    **Strategi Pemupukan Off-Season:**
    - **Pre-Stress:** NPK seimbang untuk recovery
    - **Pre-Flowering:** Tinggi P-K untuk inisiasi bunga
    - **Flowering & Fruiting:** Balanced + mikronutrien
    """)
    
    st.subheader("📅 Jadwal Pemupukan")
    
    fert_start_date = st.date_input(
        "Tanggal Mulai Program:",
        value=datetime.now(),
        key="fert_date"
    )
    
    if st.button("Generate Jadwal Pemupukan", type="primary"):
        fert_schedule = service.generate_fertilization_schedule(
            selected_fruit,
            fert_start_date.strftime("%Y-%m-%d")
        )
        
        df_fert = pd.DataFrame(fert_schedule)
        st.dataframe(df_fert, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df_fert.to_csv(index=False)
        st.download_button(
            label="📥 Download Jadwal (CSV)",
            data=csv,
            file_name=f"jadwal_pemupukan_{selected_fruit}.csv",
            mime="text/csv"
        )
    
    # Fertilization details
    st.subheader("📖 Detail Program Pemupukan")
    
    fert_program = fruit_data['fertilization_program']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        with st.expander("**Pre-Stress (Vegetatif)**"):
            st.write(f"**NPK:** {fert_program['pre_stress']['npk_ratio']}")
            st.write(f"**Dosis:** {fert_program['pre_stress']['dosage']}")
            st.write(f"**Frekuensi:** {fert_program['pre_stress']['frequency']}")
            st.write(f"**Organik:** {fert_program['pre_stress']['organic']}")
    
    with col2:
        with st.expander("**Pre-Flowering**"):
            st.write(f"**NPK:** {fert_program['pre_flowering']['npk_ratio']}")
            st.write(f"**Dosis:** {fert_program['pre_flowering']['dosage']}")
            st.write(f"**Timing:** {fert_program['pre_flowering']['timing']}")
            st.write(f"**Mikro:** {fert_program['pre_flowering']['micronutrients']}")
    
    with col3:
        with st.expander("**Flowering & Fruiting**"):
            st.write(f"**NPK:** {fert_program['flowering_fruiting']['npk_ratio']}")
            st.write(f"**Dosis:** {fert_program['flowering_fruiting']['dosage']}")
            st.write(f"**Boron:** {fert_program['flowering_fruiting']['boron']}")
            st.write(f"**Calcium:** {fert_program['flowering_fruiting']['calcium']}")

# Tab 4: Economic Analysis
with tab4:
    st.header("💰 Analisis Ekonomi")
    
    st.subheader("🧮 Kalkulator ROI")
    
    col1, col2 = st.columns(2)
    
    with col1:
        num_trees = st.number_input(
            "Jumlah Pohon:",
            min_value=1,
            max_value=10000,
            value=100,
            step=10
        )
    
    if st.button("Hitung ROI", type="primary"):
        roi_data = service.calculate_roi(selected_fruit, num_trees)
        
        # Summary metrics
        st.subheader("📊 Ringkasan Finansial")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Revenue Normal",
                f"Rp {roi_data['normal']['revenue']:,.0f}"
            )
        
        with col2:
            st.metric(
                "Revenue Off-Season",
                f"Rp {roi_data['offseason']['revenue']:,.0f}",
                delta=f"+{int((roi_data['offseason']['revenue']/roi_data['normal']['revenue']-1)*100)}%"
            )
        
        with col3:
            st.metric(
                "Extra Cost",
                f"Rp {roi_data['offseason']['cost']:,.0f}"
            )
        
        with col4:
            st.metric(
                "ROI",
                f"{roi_data['comparison']['roi_percentage']:.0f}%",
                delta="Profit Increase"
            )
        
        # Comparison table
        st.subheader("📋 Perbandingan Detail")
        
        comparison_df = pd.DataFrame({
            "Metrik": ["Revenue Total", "Biaya Tambahan", "Profit Bersih", "Revenue per Pohon"],
            "Normal Season": [
                f"Rp {roi_data['normal']['revenue']:,.0f}",
                f"Rp {roi_data['normal']['cost']:,.0f}",
                f"Rp {roi_data['normal']['profit']:,.0f}",
                f"Rp {roi_data['normal']['per_tree']:,.0f}"
            ],
            "Off-Season": [
                f"Rp {roi_data['offseason']['revenue']:,.0f}",
                f"Rp {roi_data['offseason']['cost']:,.0f}",
                f"Rp {roi_data['offseason']['profit']:,.0f}",
                f"Rp {roi_data['offseason']['per_tree']:,.0f}"
            ],
            "Selisih": [
                f"+Rp {roi_data['offseason']['revenue'] - roi_data['normal']['revenue']:,.0f}",
                f"+Rp {roi_data['offseason']['cost']:,.0f}",
                f"+Rp {roi_data['comparison']['profit_increase']:,.0f}",
                f"+Rp {roi_data['offseason']['per_tree'] - roi_data['normal']['per_tree']:,.0f}"
            ]
        })
        
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Visualization
        fig = go.Figure(data=[
            go.Bar(name='Normal Season', x=['Revenue', 'Cost', 'Profit'], 
                   y=[roi_data['normal']['revenue'], roi_data['normal']['cost'], roi_data['normal']['profit']]),
            go.Bar(name='Off-Season', x=['Revenue', 'Cost', 'Profit'], 
                   y=[roi_data['offseason']['revenue'], roi_data['offseason']['cost'], roi_data['offseason']['profit']])
        ])
        
        fig.update_layout(
            title="Perbandingan Finansial",
            barmode='group',
            yaxis_title="Rupiah (Rp)",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        st.success(f"""
        **💡 Kesimpulan:**
        - Dengan {num_trees} pohon, Anda bisa mendapat tambahan profit **Rp {roi_data['comparison']['profit_increase']:,.0f}**
        - ROI: **{roi_data['comparison']['roi_percentage']:.0f}%** dari biaya tambahan
        - Harga off-season **{roi_data['comparison']['revenue_multiplier']}x** lebih tinggi
        - **Sangat menguntungkan** untuk dicoba!
        """)

# Tab 5: Calendar
with tab5:
    st.header("📅 Kalender Budidaya")
    
    st.info("""
    Gunakan kalender ini untuk merencanakan timing yang tepat agar panen di luar musim normal.
    """)
    
    current_month = datetime.now().month
    timing_rec = service.get_market_timing_recommendation(selected_fruit, current_month)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Info Musim")
        st.write(f"**Musim Normal:** {timing_rec['normal_season']}")
        st.write(f"**Harga Normal:** {timing_rec['normal_price']}")
        st.write(f"**Target Off-Season:** {timing_rec['off_season_target']}")
        st.write(f"**Harga Off-Season:** {timing_rec['off_season_price']}")
    
    with col2:
        st.subheader("💡 Rekomendasi")
        st.info(timing_rec['recommendation'])
        st.write(f"**Multiplier:** {timing_rec['price_multiplier']}")
        st.write(f"**Ekspor:** {timing_rec['export_potential']}")

# Tab 6: Scientific References
with tab6:
    st.header("📚 Referensi Ilmiah")
    
    st.info("""
    Semua teknik dalam modul ini berbasis penelitian ilmiah peer-reviewed dari institusi terpercaya.
    """)
    
    references = service.get_scientific_references(selected_fruit)
    
    if references:
        for idx, ref in enumerate(references, 1):
            with st.expander(f"**[{idx}] {ref['title']}**"):
                st.write(f"**Authors:** {ref['authors']}")
                st.write(f"**Journal:** {ref['journal']}")
                st.write(f"**Year:** {ref['year']}")
                if 'doi' in ref:
                    st.write(f"**DOI:** {ref['doi']}")
    
    st.subheader("🏛️ Institusi Penelitian")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("""
        **Thailand:**
        - Kasetsart University
        - TISTR (Thailand Institute of Scientific Research)
        
        **Malaysia:**
        - MARDI (Malaysian Agricultural Research Institute)
        - Universiti Putra Malaysia
        """)
    
    with col2:
        st.write("""
        **Indonesia:**
        - Institut Pertanian Bogor (IPB)
        - Balai Penelitian Tanaman Buah Tropika
        
        **International:**
        - ISHS (International Society for Horticultural Science)
        """)

# Footer
st.divider()
st.caption("""
**🌴 Budidaya Buah Tropis Off-Season** | AgriSensa Platform  
Data berbasis penelitian ilmiah dari Kasetsart University, MARDI, IPB, dan jurnal peer-reviewed.  
⚠️ Konsultasikan dengan ahli pertanian lokal untuk hasil optimal.
""")
