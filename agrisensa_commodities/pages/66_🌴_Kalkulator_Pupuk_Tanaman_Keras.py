# -*- coding: utf-8 -*-
"""
Kalkulator Pupuk Tanaman Keras & Buah
Advanced fertilizer calculator for hard crops and fruit trees
Based on scientific research from IOPRI, TNAU, Haifa, Yara
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

# Add parent directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.fertilizer_database import (
    get_crop_data,
    get_all_crops,
    get_crop_category,
    FERTILIZER_CONTENT,
    HARD_CROPS,
    FRUIT_TREES
)

from services.fertilizer_calculator import (
    get_current_phase,
    calculate_phase_requirements,
    calculate_single_fertilizer_mix,
    calculate_compound_fertilizer,
    calculate_tugal_application,
    calculate_kocor_solution,
    calculate_semprot_solution,
    calculate_organic_chemical_mix
)

# Page config
st.set_page_config(
    page_title="Kalkulator Pupuk Tanaman Keras & Buah",
    page_icon="🌴",
    layout="wide"
)

# ========== SESSION STATE INITIALIZATION ==========

# Initialize session state for storing calculation results
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False
if 'phase_req' not in st.session_state:
    st.session_state.phase_req = None
if 'crop_name' not in st.session_state:
    st.session_state.crop_name = None
if 'num_trees' not in st.session_state:
    st.session_state.num_trees = 100
if 'tree_age' not in st.session_state:
    st.session_state.tree_age = 3.0
if 'estimated_area' not in st.session_state:
    st.session_state.estimated_area = 0.67

# ========== HEADER ==========

st.title("🌴 Kalkulator Pupuk Tanaman Keras & Buah")
st.markdown("""
<div style="background: linear-gradient(135deg, #2E7D32 0%, #1B5E20 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 25px;">
    <h3 style="margin: 0; color: white;">📊 Kalkulator Ilmiah Berbasis Fase Pertumbuhan</h3>
    <p style="margin: 5px 0 0 0; opacity: 0.9;">
        Hitung kebutuhan pupuk berdasarkan fase pertumbuhan (TBM/TM) dengan 3 metode aplikasi: 
        <b>Tugal (Padat)</b>, <b>Kocor (Larutan Siram)</b>, dan <b>Semprot (Foliar Spray)</b>
    </p>
    <p style="margin: 5px 0 0 0; font-size: 0.9em; opacity: 0.8;">
        🔬 Data ilmiah dari: IOPRI, TNAU, IPB, Haifa Group, Yara Fertilizer
    </p>
</div>
""", unsafe_allow_html=True)

# ========== SIDEBAR INPUT ==========

with st.sidebar:
    st.header("⚙️ Input Data")
    
    # Crop selection
    all_crops = get_all_crops()
    crop_name = st.selectbox(
        "🌱 Pilih Tanaman",
        options=all_crops,
        help="Pilih jenis tanaman keras atau buah",
        key="crop_select"
    )
    
    # Get crop data
    crop_data = get_crop_data(crop_name)
    
    if crop_data:
        st.info(f"**{crop_data['latin_name']}**\n\n{crop_data['category']}")
        
        # Tree age
        tree_age = st.number_input(
            "🎂 Umur Tanaman (Tahun)",
            min_value=0.5,
            max_value=50.0,
            value=st.session_state.tree_age,
            step=0.5,
            help="Umur tanaman dalam tahun",
            key="tree_age_input"
        )
        
        # Number of trees
        num_trees = st.number_input(
            "🌳 Jumlah Pohon",
            min_value=1,
            max_value=10000,
            value=st.session_state.num_trees,
            step=10,
            help="Total jumlah pohon yang akan dipupuk",
            key="num_trees_input"
        )
        
        # Area calculation (optional)
        if 'spacing' in crop_data:
            st.caption(f"📏 Jarak tanam: {crop_data['spacing']}")
            # Extract population from spacing info
            if "pohon/ha" in crop_data['spacing']:
                try:
                    pop_str = crop_data['spacing'].split("Populasi")[1].split("pohon/ha")[0].strip()
                    # Handle range like "100-156"
                    if "-" in pop_str:
                        pop_avg = sum([int(x) for x in pop_str.split("-")]) / 2
                    else:
                        pop_avg = int(pop_str)
                    estimated_area = num_trees / pop_avg
                    st.caption(f"📐 Estimasi luas: ~{estimated_area:.2f} ha")
                except:
                    estimated_area = num_trees / 150  # default
                    st.caption(f"📐 Estimasi luas: ~{estimated_area:.2f} ha")
            else:
                estimated_area = num_trees / 150
        else:
            estimated_area = num_trees / 150
        
        st.divider()
        
        # Calculate button - updates session state
        if st.button("🔍 Hitung Kebutuhan Pupuk", type="primary", use_container_width=True):
            # Store inputs in session state
            st.session_state.crop_name = crop_name
            st.session_state.tree_age = tree_age
            st.session_state.num_trees = num_trees
            st.session_state.estimated_area = estimated_area
            
            # Calculate and store results
            phase_req = calculate_phase_requirements(crop_name, tree_age, num_trees)
            if phase_req:
                st.session_state.phase_req = phase_req
                st.session_state.calculation_done = True
            else:
                st.error("❌ Tidak dapat menghitung kebutuhan pupuk untuk umur tanaman ini.")
                st.session_state.calculation_done = False

# ========== MAIN CONTENT ==========

# Display results if calculation has been done
if st.session_state.calculation_done and st.session_state.phase_req:
    
    # Get data from session state
    phase_req = st.session_state.phase_req
    crop_name = st.session_state.crop_name
    num_trees = st.session_state.num_trees
    tree_age = st.session_state.tree_age
    estimated_area = st.session_state.estimated_area
    crop_data = get_crop_data(crop_name)
    
    # ========== TAB 1: REKOMENDASI DASAR ==========
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📋 Rekomendasi Dasar",
        "🔸 Metode Tugal (Padat)",
        "💧 Metode Kocor (Larutan)",
        "💨 Metode Semprot (Foliar)",
        "🌿 Organik + Kimia",
        "📊 Jadwal & Biaya"
    ])
    
    with tab1:
        st.header("📋 Kebutuhan Pupuk Per Pohon")
        
        # Emphasize current phase
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #4CAF50 0%, #2E7D32 100%); padding: 20px; border-radius: 10px; color: white; margin-bottom: 20px;">
            <h3 style="margin: 0; color: white;">🌱 {phase_req['phase_name']}</h3>
            <p style="margin: 5px 0 0 0; font-size: 1.1em;">
                Umur: {phase_req['age_range']} | Frekuensi: {phase_req['application_frequency']}x per tahun
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Core Logic: Per Tree Requirements
        st.subheader("🎯 Kebutuhan Per Pohon Per Tahun")
        
        npk_per_tree = phase_req['npk_per_tree']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Nitrogen (N)",
                f"{npk_per_tree.get('N', 0):.0f} gram",
                help="Untuk pertumbuhan daun dan batang"
            )
        
        with col2:
            st.metric(
                "Fosfor (P)",
                f"{npk_per_tree.get('P', 0):.0f} gram",
                help="Untuk akar, bunga, dan buah"
            )
        
        with col3:
            st.metric(
                "Kalium (K)",
                f"{npk_per_tree.get('K', 0):.0f} gram",
                help="Untuk kualitas buah dan ketahanan"
            )
        
        if 'Mg' in npk_per_tree:
            st.info(f"➕ **Magnesium (Mg):** {npk_per_tree.get('Mg', 0):.0f} gram/pohon/tahun")
        
        st.markdown("---")
        
        # Per Application Breakdown
        st.subheader("📅 Kebutuhan Per Aplikasi")
        
        freq = phase_req['application_frequency']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            **Per Pohon Per Aplikasi:**
            - **Nitrogen (N):** {npk_per_tree.get('N', 0) / freq:.1f} gram
            - **Fosfor (P):** {npk_per_tree.get('P', 0) / freq:.1f} gram
            - **Kalium (K):** {npk_per_tree.get('K', 0) / freq:.1f} gram
            """)
            if 'Mg' in npk_per_tree:
                st.markdown(f"- **Magnesium (Mg):** {npk_per_tree.get('Mg', 0) / freq:.1f} gram")
        
        with col2:
            st.markdown(f"""
            **Jadwal Aplikasi:**
            - **Frekuensi:** {freq}x per tahun
            - **Interval:** Setiap {12/freq:.1f} bulan
            - **Bulan:** {', '.join([str(int(i * 12/freq) + 1) for i in range(freq)])}
            """)
        
        st.markdown("---")
        
        # Total for all trees
        st.subheader(f"📊 Total Kebutuhan ({num_trees} Pohon)")
        
        npk_total = phase_req['npk_total']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total N", f"{npk_total.get('N', 0):.2f} kg")
        
        with col2:
            st.metric("Total P", f"{npk_total.get('P', 0):.2f} kg")
        
        with col3:
            st.metric("Total K", f"{npk_total.get('K', 0):.2f} kg")
        
        # Visualization: Timeline
        st.markdown("---")
        st.subheader("📈 Timeline Pemupukan Tahunan")
        
        # Create timeline data
        timeline_data = []
        for i in range(freq):
            month = int(i * 12/freq) + 1
            timeline_data.append({
                'Bulan': month,
                'N (gram/pohon)': npk_per_tree.get('N', 0) / freq,
                'P (gram/pohon)': npk_per_tree.get('P', 0) / freq,
                'K (gram/pohon)': npk_per_tree.get('K', 0) / freq
            })
        
        timeline_df = pd.DataFrame(timeline_data)
        
        # Create line chart
        fig_timeline = go.Figure()
        
        fig_timeline.add_trace(go.Scatter(
            x=timeline_df['Bulan'],
            y=timeline_df['N (gram/pohon)'],
            mode='lines+markers',
            name='Nitrogen (N)',
            line=dict(color='#4CAF50', width=3),
            marker=dict(size=10)
        ))
        
        fig_timeline.add_trace(go.Scatter(
            x=timeline_df['Bulan'],
            y=timeline_df['P (gram/pohon)'],
            mode='lines+markers',
            name='Fosfor (P)',
            line=dict(color='#2196F3', width=3),
            marker=dict(size=10)
        ))
        
        fig_timeline.add_trace(go.Scatter(
            x=timeline_df['Bulan'],
            y=timeline_df['K (gram/pohon)'],
            mode='lines+markers',
            name='Kalium (K)',
            line=dict(color='#FF9800', width=3),
            marker=dict(size=10)
        ))
        
        fig_timeline.update_layout(
            title=f'Jadwal Pemupukan - {phase_req["phase_name"]}',
            xaxis_title='Bulan',
            yaxis_title='Gram per Pohon',
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_timeline, use_container_width=True)
        
        # Show all phases for reference
        st.markdown("---")
        st.subheader("📚 Semua Fase Pertumbuhan")
        
        with st.expander("Lihat Kebutuhan Semua Fase", expanded=False):
            crop_data_full = get_crop_data(crop_name)
            
            phases_data = []
            for phase in crop_data_full['phases']:
                phases_data.append({
                    'Fase': phase['phase_name'],
                    'Rentang Umur': phase['age_range'],
                    'N (g/pohon/tahun)': phase['npk_per_tree_per_year'].get('N', 0),
                    'P (g/pohon/tahun)': phase['npk_per_tree_per_year'].get('P', 0),
                    'K (g/pohon/tahun)': phase['npk_per_tree_per_year'].get('K', 0),
                    'Frekuensi': f"{phase['application_frequency']}x/tahun"
                })
            
            phases_df = pd.DataFrame(phases_data)
            st.dataframe(phases_df, use_container_width=True, hide_index=True)
            
            st.caption(f"📚 Sumber: {phase_req['source']}")
        
        # Notes
        st.info(f"💡 **Catatan Fase Ini:** {phase_req['notes']}")
        
        # Application methods available
        st.markdown("---")
        st.subheader("✅ Metode Aplikasi yang Tersedia")
        
        methods = phase_req['application_methods']
        method_icons = {
            'tugal': '🔸',
            'kocor': '💧',
            'semprot': '💨'
        }
        method_names = {
            'tugal': 'Tugal (Padat)',
            'kocor': 'Kocor (Larutan Siram)',
            'semprot': 'Semprot (Foliar Spray)'
        }
        
        cols = st.columns(len(methods))
        for idx, method in enumerate(methods):
            with cols[idx]:
                st.success(f"{method_icons.get(method, '✓')} **{method_names.get(method, method.title())}**")
        
        # Climate and weather information
        st.markdown("---")
        st.subheader("🌤️ Informasi Iklim & Cuaca Ideal")
        
        # Get climate info from crop data
        climate_info = {}
        
        # Extract climate data based on crop type
        if crop_name in ["Kelapa Sawit", "Kakao", "Kopi Robusta", "Karet", "Kelapa"]:
            # Hard crops have specific climate requirements
            if crop_name == "Kelapa Sawit":
                climate_info = {
                    "Curah Hujan": "1500-2500 mm/tahun",
                    "Suhu Optimal": "24-32°C",
                    "Ketinggian": "0-400 mdpl (dataran rendah)",
                    "Kelembaban": "80-90%",
                    "Musim Kering": "Tidak tahan kekeringan panjang",
                    "Catatan": "Butuh distribusi hujan merata sepanjang tahun"
                }
            elif crop_name == "Kakao":
                climate_info = {
                    "Curah Hujan": "1500-2500 mm/tahun",
                    "Suhu Optimal": "25-28°C",
                    "Ketinggian": "0-600 mdpl",
                    "Kelembaban": "70-80%",
                    "Naungan": "Wajib ada naungan saat muda (2-3 tahun pertama)",
                    "Catatan": "Tidak tahan angin kencang"
                }
            elif crop_name == "Kopi Robusta":
                climate_info = {
                    "Curah Hujan": "2000-3000 mm/tahun",
                    "Suhu Optimal": "24-30°C",
                    "Ketinggian": "0-800 mdpl (dataran rendah-menengah)",
                    "Kelembaban": "70-80%",
                    "Musim Kering": "2-3 bulan untuk induksi bunga",
                    "Catatan": "Lebih tahan panas dibanding Arabika"
                }
            elif crop_name == "Kopi Arabika":
                climate_info = {
                    "Curah Hujan": "1500-2500 mm/tahun",
                    "Suhu Optimal": "16-20°C (sejuk)",
                    "Ketinggian": "800-2000 mdpl (dataran tinggi WAJIB)",
                    "Kelembaban": "70-80%",
                    "Musim Kering": "2-3 bulan untuk induksi bunga",
                    "Catatan": "Tidak tahan suhu >30°C, butuh naungan"
                }
            elif crop_name == "Karet":
                climate_info = {
                    "Curah Hujan": "2000-4000 mm/tahun",
                    "Suhu Optimal": "24-28°C",
                    "Ketinggian": "0-600 mdpl",
                    "Kelembaban": "80-90%",
                    "Musim Kering": "Maksimal 2 bulan",
                    "Catatan": "Butuh hujan merata, tidak tahan kekeringan"
                }
            elif crop_name == "Kelapa":
                climate_info = {
                    "Curah Hujan": "1500-2500 mm/tahun",
                    "Suhu Optimal": "27-30°C",
                    "Ketinggian": "0-450 mdpl (dataran rendah)",
                    "Kelembaban": "70-80%",
                    "Angin": "Tahan angin pantai",
                    "Catatan": "Cocok untuk daerah pesisir"
                }
        
        elif crop_name in ["Mangga", "Durian", "Jeruk", "Rambutan", "Alpukat"]:
            # Fruit trees
            if crop_name == "Mangga":
                climate_info = {
                    "Curah Hujan": "750-2500 mm/tahun",
                    "Suhu Optimal": "24-30°C",
                    "Ketinggian": "0-500 mdpl (dataran rendah)",
                    "Kelembaban": "50-80%",
                    "Musim Kering": "WAJIB 3-4 bulan kering untuk pembungaan",
                    "Catatan": "Musim kering sangat penting untuk bunga!"
                }
            elif crop_name == "Durian":
                climate_info = {
                    "Curah Hujan": "1500-2500 mm/tahun",
                    "Suhu Optimal": "23-30°C",
                    "Ketinggian": "100-800 mdpl (optimal 400-600 mdpl)",
                    "Kelembaban": "75-85%",
                    "Musim Kering": "1-3 bulan untuk induksi bunga",
                    "Catatan": "Perbedaan suhu siang-malam membantu pembungaan"
                }
            elif crop_name == "Jeruk":
                climate_info = {
                    "Curah Hujan": "1000-2000 mm/tahun",
                    "Suhu Optimal": "25-30°C (Siam), 20-25°C (Keprok)",
                    "Ketinggian": "0-1200 mdpl (Siam rendah, Keprok tinggi)",
                    "Kelembaban": "70-80%",
                    "Musim Kering": "Tidak terlalu kritis",
                    "Catatan": "Perbedaan suhu siang-malam untuk warna kulit cerah"
                }
            elif crop_name == "Rambutan":
                climate_info = {
                    "Curah Hujan": "2000-3000 mm/tahun",
                    "Suhu Optimal": "25-30°C",
                    "Ketinggian": "0-500 mdpl (dataran rendah)",
                    "Kelembaban": "75-85%",
                    "Musim Kering": "Jelas untuk induksi bunga",
                    "Catatan": "Butuh distribusi hujan merata"
                }
            elif crop_name == "Alpukat":
                climate_info = {
                    "Curah Hujan": "1000-2000 mm/tahun",
                    "Suhu Optimal": "20-28°C (sejuk lebih baik)",
                    "Ketinggian": "200-1000 mdpl (dataran menengah-tinggi)",
                    "Kelembaban": "60-80%",
                    "Drainase": "WAJIB sempurna - tidak tahan genangan!",
                    "Catatan": "Angin kencang dapat merusak cabang"
                }
        
        # Display climate information
        if climate_info:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**📊 Kondisi Iklim Optimal:**")
                for key, value in list(climate_info.items())[:3]:
                    st.markdown(f"- **{key}:** {value}")
            
            with col2:
                st.markdown("**🌡️ Kondisi Lingkungan:**")
                for key, value in list(climate_info.items())[3:]:
                    st.markdown(f"- **{key}:** {value}")
            
            # Weather recommendations
            st.info("""
            💡 **Tips Pemupukan Berdasarkan Cuaca:**
            - ☀️ **Musim Kemarau:** Tingkatkan frekuensi penyiraman saat aplikasi pupuk
            - 🌧️ **Musim Hujan:** Hindari pemupukan saat hujan deras (pupuk tercuci)
            - 🌤️ **Waktu Terbaik:** Pagi hari (07:00-09:00) atau sore (16:00-18:00)
            - ⚠️ **Hindari:** Pemupukan saat tanah terlalu kering atau tergenang air
            """)
        else:
            st.warning("Informasi iklim untuk tanaman ini sedang dikembangkan.")
    
    
    # ========== TAB 2: METODE TUGAL ==========
    
    with tab2:
        st.header("🔸 Metode Tugal (Aplikasi Padat)")
        
        st.info("""
        **Metode Tugal** adalah aplikasi pupuk padat langsung ke tanah di sekitar pohon.
        Pupuk ditaburkan melingkar di bawah tajuk (radius 1-2 meter dari batang).
        """)
        
        # Editable prices section
        with st.expander("⚙️ Edit Harga Pupuk (Opsional)", expanded=False):
            st.markdown("**Sesuaikan harga pupuk sesuai harga lokal Anda:**")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                urea_price = st.number_input(
                    "Harga Urea (Rp/kg)",
                    min_value=1000,
                    max_value=10000,
                    value=FERTILIZER_CONTENT['Urea']['price_per_kg'],
                    step=100,
                    key="urea_price_tugal"
                )
            
            with col2:
                sp36_price = st.number_input(
                    "Harga SP-36 (Rp/kg)",
                    min_value=1000,
                    max_value=10000,
                    value=FERTILIZER_CONTENT['SP-36']['price_per_kg'],
                    step=100,
                    key="sp36_price_tugal"
                )
            
            with col3:
                kcl_price = st.number_input(
                    "Harga KCl (Rp/kg)",
                    min_value=1000,
                    max_value=10000,
                    value=FERTILIZER_CONTENT['KCl']['price_per_kg'],
                    step=100,
                    key="kcl_price_tugal"
                )
        
        # Calculate for single fertilizer mix with custom prices
        single_mix = calculate_single_fertilizer_mix(phase_req['npk_total'])
        
        # Recalculate costs with custom prices
        urea_cost_custom = single_mix['urea_kg'] * urea_price
        sp36_cost_custom = single_mix['sp36_kg'] * sp36_price
        kcl_cost_custom = single_mix['kcl_kg'] * kcl_price
        total_cost_custom = urea_cost_custom + sp36_cost_custom + kcl_cost_custom
        
        st.subheader("💊 Rekomendasi Pupuk Tunggal (Ekonomis)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            ### Urea (46% N)
            - **Total/Tahun:** {single_mix['urea_kg']:.2f} kg
            - **Karung (50kg):** {single_mix['urea_kg']/50:.1f} karung
            - **Harga:** Rp {urea_price:,.0f}/kg
            - **Biaya:** Rp {urea_cost_custom:,.0f}
            """)
        
        with col2:
            st.markdown(f"""
            ### SP-36 (36% P)
            - **Total/Tahun:** {single_mix['sp36_kg']:.2f} kg
            - **Karung (50kg):** {single_mix['sp36_kg']/50:.1f} karung
            - **Harga:** Rp {sp36_price:,.0f}/kg
            - **Biaya:** Rp {sp36_cost_custom:,.0f}
            """)
        
        with col3:
            st.markdown(f"""
            ### KCl (60% K)
            - **Total/Tahun:** {single_mix['kcl_kg']:.2f} kg
            - **Karung (50kg):** {single_mix['kcl_kg']/50:.1f} karung
            - **Harga:** Rp {kcl_price:,.0f}/kg
            - **Biaya:** Rp {kcl_cost_custom:,.0f}
            """)
        
        st.success(f"💰 **Total Biaya Pupuk Tunggal:** Rp {total_cost_custom:,.0f}")
        
        st.markdown("---")
        
        # Application schedule
        tugal_app = calculate_tugal_application(
            single_mix['total_kg'],
            num_trees,
            phase_req['application_frequency']
        )
        
        st.subheader("📅 Jadwal Aplikasi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Per Pohon Per Aplikasi", f"{tugal_app['per_tree_per_app_g']:.0f} gram")
            st.metric("Per Pohon Per Tahun", f"{tugal_app['per_tree_per_year_g']:.0f} gram")
        
        with col2:
            st.metric("Total Per Aplikasi", f"{tugal_app['total_per_app_kg']:.2f} kg")
            st.metric("Frekuensi Per Tahun", f"{tugal_app['applications_per_year']}x")
        
        st.info(f"📝 **Cara Aplikasi:** {tugal_app['instructions']}")
        
        # Compound fertilizer option
        st.markdown("---")
        st.subheader("💊 Alternatif: Pupuk Majemuk (Praktis)")
        
        compound_options = ["NPK 15-15-15", "NPK 16-16-16", "NPK 12-12-17+2MgO"]
        
        compound_results = []
        for compound in compound_options:
            result = calculate_compound_fertilizer(phase_req['npk_total'], compound)
            if result:
                compound_results.append(result)
        
        cols = st.columns(len(compound_results))
        for idx, result in enumerate(compound_results):
            with cols[idx]:
                st.markdown(f"""
                ### {result['fertilizer_type']}
                - **Total:** {result['total_kg']:.2f} kg
                - **Karung:** {result['total_kg']/50:.1f} karung
                - **Biaya:** Rp {result['total_cost']:,.0f}
                """)
        
        st.caption("💡 Pupuk majemuk lebih praktis tapi biasanya lebih mahal. Pilih sesuai budget dan kemudahan aplikasi.")
        
        st.markdown("---")
        
        # Additional fertilizer options with editable prices
        st.subheader("💊 Input Pupuk Kimia Lengkap (Editable)")
        
        with st.expander("⚙️ Pilih & Edit Pupuk Sesuai Kebutuhan", expanded=False):
            st.markdown("**Sesuaikan jenis dan harga pupuk berdasarkan ketersediaan lokal:**")
            
            # Get NPK requirements
            npk_needed = phase_req['npk_total']
            
            # Fertilizer selection
            st.markdown("### 1️⃣ Pilih Pupuk untuk Nitrogen (N)")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                n_fertilizer = st.selectbox(
                    "Pupuk N",
                    options=["Urea", "ZA (Amonium Sulfat)", "KNO3 (Kalium Nitrat)"],
                    key="n_fert_tugal"
                )
            
            with col2:
                n_content = FERTILIZER_CONTENT[n_fertilizer]['N']
                st.metric("Kandungan N", f"{n_content}%")
            
            with col3:
                n_price = st.number_input(
                    f"Harga {n_fertilizer} (Rp/kg)",
                    min_value=1000,
                    max_value=50000,
                    value=FERTILIZER_CONTENT[n_fertilizer]['price_per_kg'],
                    step=100,
                    key="n_price_tugal"
                )
            
            # Calculate N fertilizer needed
            n_needed_kg = npk_needed.get('N', 0) / (n_content / 100)
            n_cost = n_needed_kg * n_price
            
            st.success(f"✅ Kebutuhan {n_fertilizer}: **{n_needed_kg:.2f} kg** (Rp {n_cost:,.0f})")
            
            st.markdown("---")
            
            st.markdown("### 2️⃣ Pilih Pupuk untuk Fosfor (P)")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                p_fertilizer = st.selectbox(
                    "Pupuk P",
                    options=["SP-36", "MKP (Mono Kalium Fosfat)"],
                    key="p_fert_tugal"
                )
            
            with col2:
                p_content = FERTILIZER_CONTENT[p_fertilizer]['P']
                st.metric("Kandungan P", f"{p_content}%")
            
            with col3:
                p_price = st.number_input(
                    f"Harga {p_fertilizer} (Rp/kg)",
                    min_value=1000,
                    max_value=50000,
                    value=FERTILIZER_CONTENT[p_fertilizer]['price_per_kg'],
                    step=100,
                    key="p_price_tugal"
                )
            
            # Calculate P fertilizer needed
            p_needed_kg = npk_needed.get('P', 0) / (p_content / 100)
            p_cost = p_needed_kg * p_price
            
            st.success(f"✅ Kebutuhan {p_fertilizer}: **{p_needed_kg:.2f} kg** (Rp {p_cost:,.0f})")
            
            st.markdown("---")
            
            st.markdown("### 3️⃣ Pilih Pupuk untuk Kalium (K)")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                k_fertilizer = st.selectbox(
                    "Pupuk K",
                    options=["KCl", "KNO3 (Kalium Nitrat)", "MKP (Mono Kalium Fosfat)"],
                    key="k_fert_tugal"
                )
            
            with col2:
                k_content = FERTILIZER_CONTENT[k_fertilizer]['K']
                st.metric("Kandungan K", f"{k_content}%")
            
            with col3:
                k_price = st.number_input(
                    f"Harga {k_fertilizer} (Rp/kg)",
                    min_value=1000,
                    max_value=50000,
                    value=FERTILIZER_CONTENT[k_fertilizer]['price_per_kg'],
                    step=100,
                    key="k_price_tugal"
                )
            
            # Calculate K fertilizer needed
            k_needed_kg = npk_needed.get('K', 0) / (k_content / 100)
            k_cost = k_needed_kg * k_price
            
            st.success(f"✅ Kebutuhan {k_fertilizer}: **{k_needed_kg:.2f} kg** (Rp {k_cost:,.0f})")
            
            st.markdown("---")
            
            # Total custom mix
            st.markdown("### 💰 Total Biaya Pupuk Custom")
            
            total_custom_kg = n_needed_kg + p_needed_kg + k_needed_kg
            total_custom_cost = n_cost + p_cost + k_cost
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Pupuk", f"{total_custom_kg:.2f} kg")
            
            with col2:
                st.metric("Total Biaya", f"Rp {total_custom_cost:,.0f}")
            
            with col3:
                st.metric("Biaya per Pohon", f"Rp {total_custom_cost/num_trees:,.0f}")
            
            # Comparison with standard mix
            st.info(f"""
            📊 **Perbandingan:**
            - **Pupuk Tunggal Standard:** Rp {total_cost_custom:,.0f}
            - **Pupuk Custom Pilihan Anda:** Rp {total_custom_cost:,.0f}
            - **Selisih:** Rp {abs(total_custom_cost - total_cost_custom):,.0f} ({'+' if total_custom_cost > total_cost_custom else '-'}{abs((total_custom_cost - total_cost_custom)/total_cost_custom*100):.1f}%)
            """)
        
        st.markdown("---")
        
        # Combination: Compound + Single fertilizers
        st.subheader("🔄 Kombinasi Pupuk Majemuk + Tunggal")
        
        with st.expander("⚙️ Gunakan NPK Majemuk + Pupuk Tunggal untuk Kekurangan", expanded=False):
            st.markdown("""
            **Strategi Kombinasi:**
            Gunakan pupuk majemuk (NPK) sebagai base, lalu tambahkan pupuk tunggal untuk nutrisi yang masih kurang.
            Ini lebih praktis daripada full pupuk tunggal, tapi lebih ekonomis daripada full majemuk.
            """)
            
            # Get NPK requirements
            npk_needed = phase_req['npk_total']
            
            # Step 1: Choose compound fertilizer
            st.markdown("### 1️⃣ Pilih Pupuk Majemuk (Base)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                compound_type = st.selectbox(
                    "Jenis NPK Majemuk",
                    options=["NPK 15-15-15", "NPK 16-16-16", "NPK 12-12-17+2MgO"],
                    key="compound_combo"
                )
            
            with col2:
                compound_price = st.number_input(
                    f"Harga {compound_type} (Rp/kg)",
                    min_value=1000,
                    max_value=20000,
                    value=FERTILIZER_CONTENT[compound_type]['price_per_kg'],
                    step=100,
                    key="compound_price_combo"
                )
            
            # Show NPK content
            compound_npk = FERTILIZER_CONTENT[compound_type]
            st.info(f"📊 Kandungan: N={compound_npk['N']}%, P={compound_npk['P']}%, K={compound_npk['K']}%")
            
            # Calculate compound fertilizer amount (based on limiting nutrient)
            n_from_compound = npk_needed.get('N', 0) / (compound_npk['N'] / 100)
            p_from_compound = npk_needed.get('P', 0) / (compound_npk['P'] / 100)
            k_from_compound = npk_needed.get('K', 0) / (compound_npk['K'] / 100)
            
            # Use the maximum (limiting nutrient)
            compound_kg = max(n_from_compound, p_from_compound, k_from_compound)
            
            # Calculate NPK provided by compound
            n_provided = compound_kg * (compound_npk['N'] / 100)
            p_provided = compound_kg * (compound_npk['P'] / 100)
            k_provided = compound_kg * (compound_npk['K'] / 100)
            
            # Calculate remaining needs
            n_remaining = max(0, npk_needed.get('N', 0) - n_provided)
            p_remaining = max(0, npk_needed.get('P', 0) - p_provided)
            k_remaining = max(0, npk_needed.get('K', 0) - k_provided)
            
            compound_cost = compound_kg * compound_price
            
            st.success(f"✅ Kebutuhan {compound_type}: **{compound_kg:.2f} kg** (Rp {compound_cost:,.0f})")
            
            # Show what's provided and what's remaining
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "N dari NPK",
                    f"{n_provided:.2f} kg",
                    delta=f"{n_remaining:.2f} kg kurang" if n_remaining > 0 else "✓ Cukup",
                    delta_color="inverse" if n_remaining > 0 else "normal"
                )
            
            with col2:
                st.metric(
                    "P dari NPK",
                    f"{p_provided:.2f} kg",
                    delta=f"{p_remaining:.2f} kg kurang" if p_remaining > 0 else "✓ Cukup",
                    delta_color="inverse" if p_remaining > 0 else "normal"
                )
            
            with col3:
                st.metric(
                    "K dari NPK",
                    f"{k_provided:.2f} kg",
                    delta=f"{k_remaining:.2f} kg kurang" if k_remaining > 0 else "✓ Cukup",
                    delta_color="inverse" if k_remaining > 0 else "normal"
                )
            
            st.markdown("---")
            
            # Step 2: Add single fertilizers for remaining needs
            st.markdown("### 2️⃣ Tambahkan Pupuk Tunggal untuk Kekurangan")
            
            total_single_cost = 0
            
            # N supplement
            if n_remaining > 0:
                st.markdown(f"**Tambahan Nitrogen:** {n_remaining:.2f} kg")
                col1, col2 = st.columns(2)
                
                with col1:
                    n_supp_type = st.selectbox(
                        "Pupuk N Tambahan",
                        options=["Urea", "ZA (Amonium Sulfat)"],
                        key="n_supp_combo"
                    )
                
                with col2:
                    n_supp_price = st.number_input(
                        f"Harga {n_supp_type} (Rp/kg)",
                        min_value=1000,
                        max_value=20000,
                        value=FERTILIZER_CONTENT[n_supp_type]['price_per_kg'],
                        step=100,
                        key="n_supp_price_combo"
                    )
                
                n_supp_kg = n_remaining / (FERTILIZER_CONTENT[n_supp_type]['N'] / 100)
                n_supp_cost = n_supp_kg * n_supp_price
                total_single_cost += n_supp_cost
                
                st.success(f"✅ Tambah {n_supp_type}: **{n_supp_kg:.2f} kg** (Rp {n_supp_cost:,.0f})")
            else:
                st.info("✓ Nitrogen sudah cukup dari NPK majemuk")
            
            # P supplement
            if p_remaining > 0:
                st.markdown(f"**Tambahan Fosfor:** {p_remaining:.2f} kg")
                col1, col2 = st.columns(2)
                
                with col1:
                    p_supp_type = st.selectbox(
                        "Pupuk P Tambahan",
                        options=["SP-36"],
                        key="p_supp_combo"
                    )
                
                with col2:
                    p_supp_price = st.number_input(
                        f"Harga {p_supp_type} (Rp/kg)",
                        min_value=1000,
                        max_value=20000,
                        value=FERTILIZER_CONTENT[p_supp_type]['price_per_kg'],
                        step=100,
                        key="p_supp_price_combo"
                    )
                
                p_supp_kg = p_remaining / (FERTILIZER_CONTENT[p_supp_type]['P'] / 100)
                p_supp_cost = p_supp_kg * p_supp_price
                total_single_cost += p_supp_cost
                
                st.success(f"✅ Tambah {p_supp_type}: **{p_supp_kg:.2f} kg** (Rp {p_supp_cost:,.0f})")
            else:
                st.info("✓ Fosfor sudah cukup dari NPK majemuk")
            
            # K supplement
            if k_remaining > 0:
                st.markdown(f"**Tambahan Kalium:** {k_remaining:.2f} kg")
                col1, col2 = st.columns(2)
                
                with col1:
                    k_supp_type = st.selectbox(
                        "Pupuk K Tambahan",
                        options=["KCl", "KNO3 (Kalium Nitrat)"],
                        key="k_supp_combo"
                    )
                
                with col2:
                    k_supp_price = st.number_input(
                        f"Harga {k_supp_type} (Rp/kg)",
                        min_value=1000,
                        max_value=50000,
                        value=FERTILIZER_CONTENT[k_supp_type]['price_per_kg'],
                        step=100,
                        key="k_supp_price_combo"
                    )
                
                k_supp_kg = k_remaining / (FERTILIZER_CONTENT[k_supp_type]['K'] / 100)
                k_supp_cost = k_supp_kg * k_supp_price
                total_single_cost += k_supp_cost
                
                st.success(f"✅ Tambah {k_supp_type}: **{k_supp_kg:.2f} kg** (Rp {k_supp_cost:,.0f})")
            else:
                st.info("✓ Kalium sudah cukup dari NPK majemuk")
            
            st.markdown("---")
            
            # Total combination cost
            st.markdown("### 💰 Total Biaya Kombinasi")
            
            total_combo_cost = compound_cost + total_single_cost
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Biaya NPK Majemuk", f"Rp {compound_cost:,.0f}")
            
            with col2:
                st.metric("Biaya Pupuk Tunggal", f"Rp {total_single_cost:,.0f}")
            
            with col3:
                st.metric("Total Kombinasi", f"Rp {total_combo_cost:,.0f}")
            
            # Comparison with other strategies
            st.info(f"""
            📊 **Perbandingan Semua Strategi:**
            - **Pupuk Tunggal Saja:** Rp {total_cost_custom:,.0f}
            - **Kombinasi NPK + Tunggal:** Rp {total_combo_cost:,.0f} ({'Lebih murah' if total_combo_cost < total_cost_custom else 'Lebih mahal'} Rp {abs(total_combo_cost - total_cost_custom):,.0f})
            - **Biaya per Pohon:** Rp {total_combo_cost/num_trees:,.0f}
            
            💡 **Rekomendasi:** {'Kombinasi lebih ekonomis!' if total_combo_cost < total_cost_custom else 'Pupuk tunggal lebih ekonomis!'}
            """)
    
    
    # ========== TAB 3: METODE KOCOR ==========
    
    with tab3:
        st.header("💧 Metode Kocor (Larutan Siram)")
        
        st.info("""
        **Metode Kocor** adalah aplikasi pupuk dalam bentuk larutan yang disiramkan ke tanah.
        Konsentrasi aman: **0.5-1.5%** untuk mencegah root burn.
        """)
        
        st.markdown("### 📊 Perhitungan untuk Semua Opsi Pupuk")
        st.caption("Menggunakan data dari Tab Tugal - Volume default: 2L per pohon")
        
        # Use default parameters
        liters_per_tree = 2  # Standard 2L per tree
        
        # Calculate for all 3 options from Tab 2
        # 1. Single fertilizer mix
        single_mix = calculate_single_fertilizer_mix(phase_req['npk_total'])
        
        # 2. Compound fertilizer
        compound_npk = calculate_compound_fertilizer(phase_req['npk_total'], "NPK 15-15-15")
        
        # Create tabs for each option
        kocor_tab1, kocor_tab2, kocor_tab3 = st.tabs([
            "💊 Pupuk Tunggal",
            "🔷 Pupuk Majemuk", 
            "🔄 Kombinasi"
        ])
        
        # ===== OPTION 1: Single Fertilizer =====
        with kocor_tab1:
            st.subheader("Larutan Pupuk Tunggal (Urea + SP-36 + KCl)")
            
            # Calculate kocor for total single mix
            kocor_single = calculate_kocor_solution(
                single_mix['total_kg'],
                num_trees,
                phase_req['application_frequency'],
                liters_per_tree,
                "Urea"  # Use Urea as reference for safety
            )
            
            # Safety check
            if kocor_single['is_safe']:
                st.success(f"✅ Konsentrasi: {kocor_single['concentration_percent']:.2f}% (AMAN)")
            else:
                st.error(f"⚠️ Konsentrasi: {kocor_single['concentration_percent']:.2f}% (TERLALU TINGGI!)")
                
                # Calculate safe volume
                fertilizer_per_app_g = kocor_single['fertilizer_per_app_g']
                safe_conc = 1.0  # Safe for mixed fertilizers
                min_water_liters = fertilizer_per_app_g / (safe_conc * 10)
                recommended_per_tree = min_water_liters / num_trees
                
                st.warning(f"""
                **💡 Rekomendasi Aman:**
                - Minimum **{min_water_liters:.0f} liter air** total
                - **{recommended_per_tree:.1f} liter per pohon**
                """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pupuk per Aplikasi", f"{kocor_single['fertilizer_per_app_g']:.0f} g")
            with col2:
                st.metric("Total Larutan", f"{kocor_single['total_solution_per_app_L']:.0f} L")
            with col3:
                st.metric("Tangki 16L", f"{kocor_single['tanks_16L_needed']:.1f}")
            
            st.info(f"""
            **📝 Cara Mencampur (Per Tangki 16L):**
            1. Campur: Urea {single_mix['urea_kg']/phase_req['application_frequency']/kocor_single['tanks_16L_needed']:.0f}g + 
               SP-36 {single_mix['sp36_kg']/phase_req['application_frequency']/kocor_single['tanks_16L_needed']:.0f}g + 
               KCl {single_mix['kcl_kg']/phase_req['application_frequency']/kocor_single['tanks_16L_needed']:.0f}g
            2. Larutkan dalam 16L air
            3. Siram {liters_per_tree}L per pohon
            4. Aplikasi {phase_req['application_frequency']}x per tahun
            """)
        
        # ===== OPTION 2: Compound Fertilizer =====
        with kocor_tab2:
            st.subheader("Larutan Pupuk Majemuk")
            
            # User can choose compound type
            compound_choice = st.selectbox(
                "Pilih Jenis NPK",
                ["NPK 15-15-15", "NPK 16-16-16", "NPK 12-12-17+2MgO"],
                key="kocor_compound_choice"
            )
            
            compound_data = calculate_compound_fertilizer(phase_req['npk_total'], compound_choice)
            
            kocor_compound = calculate_kocor_solution(
                compound_data['total_kg'],
                num_trees,
                phase_req['application_frequency'],
                liters_per_tree,
                compound_choice
            )
            
            # Safety check
            if kocor_compound['is_safe']:
                st.success(f"✅ Konsentrasi: {kocor_compound['concentration_percent']:.2f}% (AMAN)")
            else:
                st.error(f"⚠️ Konsentrasi: {kocor_compound['concentration_percent']:.2f}% (TERLALU TINGGI!)")
                
                fertilizer_per_app_g = kocor_compound['fertilizer_per_app_g']
                safe_conc = kocor_compound['safe_concentration']
                min_water_liters = fertilizer_per_app_g / (safe_conc * 10)
                recommended_per_tree = min_water_liters / num_trees
                
                st.warning(f"""
                **💡 Rekomendasi Aman:**
                - Minimum **{min_water_liters:.0f} liter air** total
                - **{recommended_per_tree:.1f} liter per pohon**
                """)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pupuk per Aplikasi", f"{kocor_compound['fertilizer_per_app_g']:.0f} g")
            with col2:
                st.metric("Total Larutan", f"{kocor_compound['total_solution_per_app_L']:.0f} L")
            with col3:
                st.metric("Tangki 16L", f"{kocor_compound['tanks_16L_needed']:.1f}")
            
            st.info(f"""
            **📝 Cara Mencampur (Per Tangki 16L):**
            1. Siapkan **{kocor_compound['fertilizer_per_tank_g']:.0f} gram {compound_choice}**
            2. Larutkan dalam 16L air
            3. Siram {liters_per_tree}L per pohon
            4. Aplikasi {phase_req['application_frequency']}x per tahun
            
            💰 **Biaya:** Rp {compound_data['total_cost']:,.0f}/tahun
            """)
        
        # ===== OPTION 3: Combination =====
        with kocor_tab3:
            st.subheader("Larutan Kombinasi (NPK + Tunggal)")
            
            st.info("""
            **Strategi:** Gunakan NPK majemuk sebagai base, tambah pupuk tunggal untuk kekurangan.
            Untuk kocor, bisa dicampur dalam satu larutan atau diaplikasikan terpisah.
            """)
            
            # Use NPK 15-15-15 as base
            npk_base = calculate_compound_fertilizer(phase_req['npk_total'], "NPK 15-15-15")
            
            # Calculate total fertilizer for combination
            # This is simplified - in practice would calculate based on actual combination from Tab 2
            total_combo_kg = npk_base['total_kg'] * 0.7  # Assume 70% of full NPK + supplements
            
            kocor_combo = calculate_kocor_solution(
                total_combo_kg,
                num_trees,
                phase_req['application_frequency'],
                liters_per_tree,
                "NPK 15-15-15"
            )
            
            # Safety check
            if kocor_combo['is_safe']:
                st.success(f"✅ Konsentrasi: {kocor_combo['concentration_percent']:.2f}% (AMAN)")
            else:
                st.error(f"⚠️ Konsentrasi: {kocor_combo['concentration_percent']:.2f}% (TERLALU TINGGI!)")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Pupuk per Aplikasi", f"{kocor_combo['fertilizer_per_app_g']:.0f} g")
            with col2:
                st.metric("Total Larutan", f"{kocor_combo['total_solution_per_app_L']:.0f} L")
            with col3:
                st.metric("Tangki 16L", f"{kocor_combo['tanks_16L_needed']:.1f}")
            
            st.info("""
            **📝 Cara Aplikasi:**
            
            **Opsi A - Campur Jadi Satu:**
            1. Larutkan NPK majemuk + pupuk tunggal dalam satu tangki
            2. Siram 2L per pohon
            
            **Opsi B - Aplikasi Terpisah (Lebih Aman):**
            1. Hari 1: Kocor dengan NPK majemuk
            2. Hari 3-5: Kocor dengan pupuk tunggal (jika ada kekurangan)
            
            💡 Opsi B lebih aman untuk mencegah reaksi kimia antar pupuk
            """)

    
    # ========== TAB 4: METODE SEMPROT ==========
    
    with tab4:
        st.header("💨 Metode Semprot (Foliar Spray)")
        
        st.warning("""
        ⚠️ **PENTING:** Konsentrasi semprot HARUS LEBIH RENDAH dari kocor!
        
        Konsentrasi aman foliar: **0.5-2.0%** (lebih rendah untuk mencegah leaf burn)
        """)
        
        # Use default parameters from phase data - no additional user input
        spray_volume_ha = 400  # Standard 400L/ha
        fertilizer_for_semprot = "KNO3 (Kalium Nitrat)"  # Best for foliar
        
        st.info(f"💨 **Parameter Default:** Volume {spray_volume_ha}L/ha, Pupuk {fertilizer_for_semprot}")
        
        # Calculate semprot solution
        if fertilizer_for_semprot == "KNO3 (Kalium Nitrat)":
            fert_amount = phase_req['npk_total']['K'] / 0.46
        elif fertilizer_for_semprot == "MKP (Mono Kalium Fosfat)":
            fert_amount = max(
                phase_req['npk_total']['P'] / 0.52,
                phase_req['npk_total']['K'] / 0.34
            )
        elif fertilizer_for_semprot == "Urea":
            fert_amount = phase_req['npk_total']['N'] / 0.46
        else:  # NPK 15-15-15
            fert_amount = calculate_compound_fertilizer(phase_req['npk_total'], "NPK 15-15-15")['total_kg']
        
        # Reduce amount for foliar (typically 20-30% of soil application)
        fert_amount_foliar = fert_amount * 0.25  # 25% of soil dose
        
        semprot_solution = calculate_semprot_solution(
            fert_amount_foliar,
            estimated_area,
            phase_req['application_frequency'],
            spray_volume_ha,
            fertilizer_for_semprot
        )
        
        # Display results
        st.subheader("🧪 Perhitungan Larutan Semprot")
        
        # Safety indicator with recommendation
        if semprot_solution['is_safe']:
            st.success(f"✅ Konsentrasi AMAN: {semprot_solution['recommended_concentration']:.2f}% (Batas: {semprot_solution['safe_concentration']}%)")
        else:
            st.error(f"⚠️ BAHAYA LEAF BURN! Konsentrasi diturunkan ke {semprot_solution['recommended_concentration']:.2f}%")
            st.warning(semprot_solution['warning'])
            
            # Calculate safe volume recommendation
            # Note: For semprot, we already auto-adjust to safe concentration
            # But show what the original calculation would need
            original_fert_g = (semprot_solution['concentration_percent'] * semprot_solution['total_spray_volume_L'] * 10)
            safe_conc = semprot_solution['safe_concentration']
            
            # Minimum spray volume needed for original fertilizer amount at safe concentration
            min_spray_volume = original_fert_g / (safe_conc * 10)
            min_volume_per_ha = min_spray_volume / estimated_area
            
            st.info(f"""
            **💡 Rekomendasi Aman:**
            
            Sistem otomatis menurunkan dosis pupuk untuk keamanan daun.
            
            **Alternatif - Jika ingin gunakan dosis penuh:**
            - **Minimum {min_spray_volume:.0f} liter** volume semprot total
            - **{min_volume_per_ha:.0f} liter per hektar** (saat ini: {spray_volume_ha}L/ha)
            
            **Rekomendasi Terbaik:**
            ✅ Gunakan dosis yang sudah disesuaikan ({semprot_solution['fertilizer_needed_g']:.0f}g)
            ✅ Volume semprot tetap {spray_volume_ha}L/ha
            ✅ Konsentrasi aman {safe_conc}% - tidak akan bakar daun!
            """)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Konsentrasi Aman", f"{semprot_solution['recommended_concentration']:.2f}%")
            st.metric("Volume per Ha", f"{semprot_solution['spray_volume_per_ha_L']} L")
        
        with col2:
            st.metric("Pupuk Dibutuhkan", f"{semprot_solution['fertilizer_needed_g']:.0f} g")
            st.metric("Total Volume", f"{semprot_solution['total_spray_volume_L']:.0f} L")
        
        with col3:
            st.metric("Tangki 16L Dibutuhkan", f"{semprot_solution['tanks_16L_needed']:.1f}")
            st.metric("Frekuensi/Tahun", f"{semprot_solution['applications_per_year']}x")
        
        st.markdown("---")
        
        # Mixing instructions
        st.subheader("📝 Cara Mencampur Larutan Semprot")
        
        st.success(f"""
        **Per Tangki 16 Liter:**
        1. Isi tangki dengan {semprot_solution['water_per_tank_L']} liter air bersih
        2. Tambahkan **{semprot_solution['fertilizer_per_tank_g']:.0f} gram {fertilizer_for_semprot}**
        3. Aduk hingga larut sempurna
        4. Semprot merata pada daun (atas dan bawah)
        5. Aplikasi **{semprot_solution['applications_per_year']}x per tahun**
        
        ⚠️ **WAJIB:**
        - Semprot pagi hari (06:00-09:00) atau sore (16:00-18:00)
        - JANGAN semprot saat terik matahari (leaf burn!)
        - JANGAN semprot saat hujan atau akan hujan
        - Gunakan nozzle halus untuk coverage maksimal
        """)
    
    # ========== TAB 5: ORGANIK + KIMIA ==========
    
    with tab5:
        st.header("🌿 Kombinasi Pupuk Organik + Kimia")
        
        st.info("""
        **Kombinasi Organik + Kimia** memberikan manfaat jangka panjang:
        - Organik: Memperbaiki struktur tanah, meningkatkan mikroba
        - Kimia: Nutrisi cepat tersedia untuk tanaman
        
        Rasio rekomendasi: **30% Organik + 70% Kimia**
        """)
        
        # Use standard 30% organic ratio - no user input
        organic_ratio = 0.30  # Standard 30% organic + 70% chemical
        
        st.info(f"🌿 **Rasio Standard:** {organic_ratio*100:.0f}% Organik + {(1-organic_ratio)*100:.0f}% Kimia")
        
        # Calculate mix
        org_chem_mix = calculate_organic_chemical_mix(phase_req['npk_total'], organic_ratio)
        
        st.subheader("📊 Perhitungan Kombinasi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌿 Pupuk Organik")
            st.markdown(f"""
            **Pupuk Kandang Sapi**
            - Rasio: **{org_chem_mix['organic_ratio']:.0f}%**
            - Jumlah: **{org_chem_mix['organic_kg']:.2f} kg**
            - Biaya: **Rp {org_chem_mix['organic_cost']:,.0f}**
            
            💡 Aplikasi: Taburkan melingkar di bawah tajuk, 2x per tahun
            """)
        
        with col2:
            st.markdown("### 💊 Pupuk Kimia")
            st.markdown(f"""
            **Kombinasi Tunggal**
            - Rasio: **{org_chem_mix['chemical_ratio']:.0f}%**
            - Urea: **{org_chem_mix['chemical_urea_kg']:.2f} kg**
            - SP-36: **{org_chem_mix['chemical_sp36_kg']:.2f} kg**
            - KCl: **{org_chem_mix['chemical_kcl_kg']:.2f} kg**
            - Biaya: **Rp {org_chem_mix['chemical_cost']:,.0f}**
            """)
        
        st.success(f"💰 **Total Biaya Kombinasi:** Rp {org_chem_mix['total_cost']:,.0f}")
        
        st.markdown("---")
        
        # Benefits
        st.subheader("✅ Manfaat Kombinasi Organik + Kimia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Jangka Pendek:**
            - ✓ Nutrisi cepat tersedia (dari kimia)
            - ✓ Pertumbuhan optimal
            - ✓ Hasil panen meningkat
            """)
        
        with col2:
            st.markdown("""
            **Jangka Panjang:**
            - ✓ Struktur tanah membaik
            - ✓ Aktivitas mikroba meningkat
            - ✓ Kesuburan tanah berkelanjutan
            - ✓ Ketahanan terhadap stress
            """)
        
        st.info(org_chem_mix['benefits'])
    
    # ========== TAB 6: JADWAL & BIAYA ==========
    
    with tab6:
        st.header("📊 Jadwal Pemupukan & Analisis Biaya")
        
        # Annual schedule
        st.subheader("📅 Jadwal Pemupukan Tahunan")
        
        # Create schedule dataframe
        freq = phase_req['application_frequency']
        months_interval = 12 / freq
        
        schedule_data = []
        for i in range(freq):
            month = int(i * months_interval) + 1
            schedule_data.append({
                "Aplikasi Ke-": i + 1,
                "Bulan": month,
                "Fase": phase_req['phase_name'],
                "Metode": ", ".join([m.title() for m in phase_req['application_methods']])
            })
        
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Cost comparison
        st.subheader("💰 Perbandingan Biaya Metode Pemupukan")
        
        # Calculate costs for different strategies
        cost_data = []
        
        # 1. Single fertilizer mix
        cost_data.append({
            "Strategi": "Pupuk Tunggal (Urea+SP36+KCl)",
            "Total Biaya (Rp)": single_mix['total_cost'],
            "Biaya per Pohon (Rp)": single_mix['total_cost'] / num_trees,
            "Keterangan": "Paling ekonomis"
        })
        
        # 2. Compound fertilizer
        npk_compound = calculate_compound_fertilizer(phase_req['npk_total'], "NPK 15-15-15")
        cost_data.append({
            "Strategi": "Pupuk Majemuk (NPK 15-15-15)",
            "Total Biaya (Rp)": npk_compound['total_cost'],
            "Biaya per Pohon (Rp)": npk_compound['total_cost'] / num_trees,
            "Keterangan": "Paling praktis"
        })
        
        # 3. Organic + Chemical
        cost_data.append({
            "Strategi": "Organik 30% + Kimia 70%",
            "Total Biaya (Rp)": org_chem_mix['total_cost'],
            "Biaya per Pohon (Rp)": org_chem_mix['total_cost'] / num_trees,
            "Keterangan": "Terbaik jangka panjang"
        })
        
        cost_df = pd.DataFrame(cost_data)
        st.dataframe(cost_df, use_container_width=True, hide_index=True)
        
        # Visualization
        fig_cost = px.bar(
            cost_df,
            x='Strategi',
            y='Total Biaya (Rp)',
            title='Perbandingan Total Biaya Pemupukan',
            color='Strategi',
            text='Total Biaya (Rp)'
        )
        fig_cost.update_traces(texttemplate='Rp %{text:,.0f}', textposition='outside')
        st.plotly_chart(fig_cost, use_container_width=True)
        
        st.markdown("---")
        
        # ROI Calculator
        st.subheader("💵 Kalkulator ROI (Return on Investment)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            yield_per_tree = st.number_input(
                "Estimasi Hasil per Pohon (kg/tahun)",
                min_value=1.0,
                max_value=1000.0,
                value=50.0,
                step=5.0
            )
        
        with col2:
            price_per_kg = st.number_input(
                "Harga Jual per Kg (Rp)",
                min_value=1000,
                max_value=100000,
                value=15000,
                step=1000
            )
        
        # Calculate ROI
        total_yield = yield_per_tree * num_trees
        total_revenue = total_yield * price_per_kg
        
        # Use cheapest fertilizer cost
        fertilizer_cost = min([c['Total Biaya (Rp)'] for c in cost_data])
        
        net_profit = total_revenue - fertilizer_cost
        roi = (net_profit / fertilizer_cost) * 100 if fertilizer_cost > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Hasil", f"{total_yield:,.0f} kg")
        
        with col2:
            st.metric("Pendapatan", f"Rp {total_revenue:,.0f}")
        
        with col3:
            st.metric("Biaya Pupuk", f"Rp {fertilizer_cost:,.0f}")
        
        with col4:
            st.metric("ROI", f"{roi:,.0f}%")
        
        if roi > 100:
            st.success(f"✅ ROI sangat baik! Setiap Rp 1 biaya pupuk menghasilkan Rp {roi/100:.2f} keuntungan.")
        elif roi > 50:
            st.info(f"💡 ROI cukup baik. Optimasi pemupukan dapat meningkatkan hasil.")
        else:
            st.warning(f"⚠️ ROI rendah. Pertimbangkan efisiensi pemupukan atau peningkatan harga jual.")

# ========== FOOTER: SCIENTIFIC REFERENCES ==========

st.markdown("---")

with st.expander("📚 Referensi Ilmiah & Sumber Data"):
    st.markdown("""
    ### Sumber Data Ilmiah
    
    **Tanaman Keras:**
    - **Kelapa Sawit:** Indonesian Oil Palm Research Institute (IOPRI), Malaysian Palm Oil Board
    - **Kakao:** Indonesian Coffee and Cocoa Research Institute (ICCRI)
    - **Kopi:** ICCRI, TNAU (Tamil Nadu Agricultural University)
    - **Karet:** Rubber Research Institute
    - **Kelapa:** Coconut Research Institute, TNAU
    
    **Tanaman Buah:**
    - **Mangga:** TNAU, Mango.org, Haifa Group
    - **Durian:** Haifa Group, IPB (Institut Pertanian Bogor), Growplant.org
    - **Jeruk:** Yara Fertilizer, Citrus Australia, TNAU
    - **Rambutan, Alpukat:** IPB, Agriculture Institute
    
    **Fertilizer Research:**
    - Haifa Group - Nutrition Programs
    - Yara International - Crop Nutrition
    - Malaysian Palm Oil Board (MPOB)
    - Various peer-reviewed journals on tropical fruit cultivation
    
    ### Konsentrasi Aman Pupuk
    
    **Metode Kocor (Drench):**
    - Konsentrasi umum: 0.5-1.5%
    - Maksimum: 2% (untuk tanaman dewasa)
    
    **Metode Semprot (Foliar):**
    - Urea: 0.5-2%
    - KNO3: 0.5-1%
    - NPK Compound: 0.5-1.5%
    - Maksimum: 2% (risiko leaf burn!)
    
    ### Disclaimer
    
    Data dalam kalkulator ini berdasarkan penelitian ilmiah dan rekomendasi standar.
    Kebutuhan aktual dapat bervariasi tergantung:
    - Kondisi tanah lokal
    - Iklim dan cuaca
    - Varietas tanaman
    - Sistem budidaya
    
    **Rekomendasi:** Lakukan analisis tanah dan daun untuk rekomendasi yang lebih spesifik.
    """)

st.caption("🌴 Kalkulator Pupuk Tanaman Keras & Buah - AgriSensa Commodities © 2025")
