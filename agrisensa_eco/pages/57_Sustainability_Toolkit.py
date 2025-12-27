import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.regenerative_ag_calculator import RegenerativeAgCalculator
from services.climate_adaptation_calculator import ClimateAdaptationCalculator
from services.circular_economy_calculator import CircularEconomyCalculator
from utils.auth import require_auth, show_user_info_sidebar

# Page config
st.set_page_config(
    page_title="Sustainability Toolkit",
    page_icon="🌱",
    layout="wide"
)

# Authentication
user = require_auth()
show_user_info_sidebar()

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0fdf4;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌱 Sustainability Toolkit")
st.markdown("""
Toolkit lengkap untuk pertanian berkelanjutan: Regenerative Agriculture, Climate Adaptation, dan Circular Economy
""")

st.markdown("---")

# Initialize calculators
regen_calc = RegenerativeAgCalculator()
climate_calc = ClimateAdaptationCalculator()
circular_calc = CircularEconomyCalculator()

# Tabs
tab1, tab2, tab3 = st.tabs([
    "🌾 Regenerative Agriculture",
    "🌡️ Climate Adaptation",
    "♻️ Circular Economy"
])

# ===== TAB 1: REGENERATIVE AGRICULTURE =====
with tab1:
    st.subheader("Pertanian Regeneratif")
    
    subtab1, subtab2, subtab3 = st.tabs([
        "Soil Health Scorecard",
        "Cover Crop Selector",
        "Crop Rotation Planner"
    ])
    
    with subtab1:
        st.markdown("### 🌱 Soil Health Scorecard")
        
        col1, col2 = st.columns(2)
        
        with col1:
            c_organic = st.number_input("C-Organik (%)", 0.1, 10.0, 2.0, 0.1)
            ph = st.number_input("pH Tanah", 4.0, 9.0, 6.5, 0.1)
            n_total = st.number_input("N-Total (%)", 0.01, 1.0, 0.15, 0.01)
        
        with col2:
            p_available = st.number_input("P-Tersedia (ppm)", 1, 200, 20, 1)
            k_available = st.number_input("K-Tersedia (ppm)", 10, 500, 150, 10)
        
        if st.button("📊 Hitung Skor Kesehatan Tanah", type="primary"):
            result = regen_calc.calculate_soil_health_score(
                c_organic, ph, n_total, p_available, k_available
            )
            
            st.markdown("---")
            
            col_m1, col_m2, col_m3 = st.columns(3)
            
            with col_m1:
                score_color = "🟢" if result['overall_score'] >= 70 else "🟡" if result['overall_score'] >= 55 else "🔴"
                st.metric("Overall Score", f"{result['overall_score']}/100", result['rating'])
            
            with col_m2:
                st.metric("C-Organik Score", f"{result['individual_scores']['c_organic']}/100")
            
            with col_m3:
                st.metric("pH Score", f"{result['individual_scores']['ph']}/100")
            
            st.markdown("### 💡 Rekomendasi")
            for rec in result['recommendations']:
                st.success(f"✅ {rec}")
    
    with subtab2:
        st.markdown("### 🌿 Cover Crop Selector")
        
        col_s1, col_s2 = st.columns(2)
        
        with col_s1:
            season = st.selectbox("Musim", ["Hujan", "Kemarau", "Sepanjang tahun"])
        
        with col_s2:
            goal = st.selectbox("Tujuan Utama", [
                "Fiksasi N",
                "Biomassa",
                "Tekan gulma",
                "Pakan ternak",
                "Biofumigasi"
            ])
        
        if st.button("🔍 Cari Cover Crop", type="primary"):
            recs = regen_calc.recommend_cover_crop(season, goal)
            
            if recs:
                st.markdown("### Rekomendasi Cover Crop")
                for rec in recs:
                    st.info(f"""
                    **{rec['name']}** ({rec['category']})
                    - Musim: {rec['season']}
                    - Manfaat: {rec['benefit']}
                    - Durasi: {rec['duration']} hari
                    """)
            else:
                st.warning("Tidak ada rekomendasi yang cocok")
    
    with subtab3:
        st.markdown("### 🔄 Crop Rotation Planner")
        
        rotation_years = st.slider("Durasi Rotasi (tahun)", 2, 5, 3)
        
        if st.button("📊 Hitung Manfaat Rotasi", type="primary"):
            benefits = regen_calc.calculate_crop_rotation_benefit(rotation_years)
            
            st.markdown("### Manfaat Crop Rotation")
            
            col_b1, col_b2 = st.columns(2)
            
            with col_b1:
                st.metric("Pengurangan Hama", f"{benefits['pest_reduction_pct']}%")
                st.metric("Peningkatan Yield", f"{benefits['yield_increase_pct']}%")
            
            with col_b2:
                st.metric("Perbaikan Tanah", f"{benefits['soil_health_improvement_pct']}%")
                st.metric("Hemat Pupuk", f"{benefits['fertilizer_savings_pct']}%")


# ===== TAB 2: CLIMATE ADAPTATION =====
with tab2:
    st.subheader("Adaptasi Perubahan Iklim")
    
    subtab1, subtab2, subtab3 = st.tabs([
        "Climate Risk Assessment",
        "Climate-Smart Crops",
        "Insurance Calculator"
    ])
    
    with subtab1:
        st.markdown("### 🌍 Climate Risk Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            region_type = st.selectbox("Tipe Wilayah", [
                "coastal", "lowland", "highland", "dryland"
            ], format_func=lambda x: {
                "coastal": "Pesisir",
                "lowland": "Dataran Rendah",
                "highland": "Dataran Tinggi",
                "dryland": "Lahan Kering"
            }[x])
            
            rainfall_mm = st.number_input("Curah Hujan Tahunan (mm)", 500, 5000, 2000, 100)
        
        with col2:
            temp_avg = st.number_input("Suhu Rata-rata (°C)", 20, 35, 27, 1)
            elevation = st.number_input("Ketinggian (mdpl)", 0, 3000, 100, 50)
        
        if st.button("⚠️ Assess Climate Risk", type="primary"):
            result = climate_calc.assess_climate_risk(region_type, rainfall_mm, temp_avg, elevation)
            
            st.markdown("---")
            
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                risk_color = "🔴" if result['overall_risk_pct'] >= 60 else "🟡" if result['overall_risk_pct'] >= 40 else "🟢"
                st.metric("Overall Risk", f"{result['overall_risk_pct']}%", result['risk_level'])
                
                st.markdown("### Primary Threats")
                for threat in result['primary_threats']:
                    st.warning(f"⚠️ {threat.replace('_', ' ').title()}")
            
            with col_r2:
                st.markdown("### Adaptation Strategies")
                for strategy in result['adaptation_strategies']:
                    st.success(f"✅ {strategy}")
    
    with subtab2:
        st.markdown("### 🌾 Climate-Smart Crop Selector")
        
        primary_risk = st.selectbox("Risiko Utama", [
            "Drought (Kekeringan)",
            "Flood (Banjir)",
            "Heat Stress (Panas Ekstrem)"
        ])
        
        if st.button("🔍 Cari Tanaman", type="primary"):
            crops = climate_calc.recommend_climate_smart_crop(primary_risk)
            
            st.markdown("### Rekomendasi Tanaman")
            
            for crop_name, crop_info in crops.items():
                st.info(f"""
                **{crop_name}**
                - {', '.join([f"{k}: {v}" for k, v in crop_info.items()])}
                """)
    
    with subtab3:
        st.markdown("### 💰 Insurance Premium Calculator")
        
        col_i1, col_i2 = st.columns(2)
        
        with col_i1:
            crop_value = st.number_input("Nilai Tanaman (Rp)", 1000000, 1000000000, 50000000, 1000000)
        
        with col_i2:
            risk_level = st.selectbox("Risk Level", [
                "Very Low", "Low", "Medium", "High", "Very High"
            ])
        
        if st.button("💵 Hitung Premi", type="primary"):
            result = climate_calc.calculate_insurance_premium(crop_value, risk_level)
            
            col_p1, col_p2, col_p3 = st.columns(3)
            
            with col_p1:
                st.metric("Premi Tahunan", f"Rp {result['premium']:,.0f}")
            
            with col_p2:
                st.metric("Rate", f"{result['rate_pct']}%")
            
            with col_p3:
                st.metric("Nilai Tanaman", f"Rp {result['crop_value']:,.0f}")


# ===== TAB 3: CIRCULAR ECONOMY =====
with tab3:
    st.subheader("Ekonomi Sirkular")
    
    subtab1, subtab2, subtab3 = st.tabs([
        "Waste Valorization",
        "Biogas Calculator",
        "Composting Guide"
    ])
    
    with subtab1:
        st.markdown("### ♻️ Agricultural Waste Valorization")
        
        col1, col2 = st.columns(2)
        
        with col1:
            waste_type = st.selectbox("Jenis Limbah", [
                "Jerami Padi",
                "Tongkol Jagung",
                "Kulit Kopi",
                "Limbah Sawit",
                "Kotoran Ternak"
            ])
            
            waste_amount = st.number_input("Jumlah Limbah (kg)", 10, 10000, 1000, 10)
        
        with col2:
            # Get available methods for selected waste
            methods = list(circular_calc.WASTE_VALORIZATION.get(waste_type, {}).keys())
            if methods:
                method = st.selectbox("Metode Valorisasi", methods)
            else:
                method = None
        
        # Initialize variables with default values
        yield_pct = 80
        yield_m3 = 0.3
        price_per_kg = 2000
        price_per_m3 = 3000
        
        # Editable price section
        if method:
            st.markdown("### ⚙️ Parameter Harga (Editable)")
            
            # Get default values
            waste_options = circular_calc.WASTE_VALORIZATION.get(waste_type, {})
            method_data = waste_options.get(method, {})
            
            col_p1, col_p2 = st.columns(2)
            
            with col_p1:
                if 'yield_pct' in method_data:
                    yield_pct = st.number_input(
                        "Yield (%)", 
                        10, 100, 
                        method_data['yield_pct'], 
                        5,
                        help="Persentase output dari input limbah"
                    )
                elif 'yield_m3_per_kg' in method_data:
                    yield_m3 = st.number_input(
                        "Yield (m³/kg)", 
                        0.1, 1.0, 
                        method_data['yield_m3_per_kg'], 
                        0.05,
                        help="Volume biogas per kg limbah"
                    )
            
            with col_p2:
                if 'value_per_kg' in method_data:
                    price_per_kg = st.number_input(
                        "Harga Jual (Rp/kg)", 
                        100, 100000, 
                        method_data['value_per_kg'], 
                        100,
                        help="Harga jual produk per kilogram"
                    )
                elif 'value_per_m3' in method_data:
                    price_per_m3 = st.number_input(
                        "Harga Biogas (Rp/m³)", 
                        1000, 10000, 
                        method_data['value_per_m3'], 
                        500,
                        help="Harga biogas per meter kubik"
                    )
            
            # Show button inside the method block
            if st.button("💰 Hitung Nilai", type="primary"):
                # Manual calculation with editable values
                st.markdown("---")
                st.markdown("### 📊 Hasil Perhitungan")
                
                if 'yield_pct' in method_data:
                    # Calculate with editable values
                    output_kg = waste_amount * (yield_pct / 100)
                    value = output_kg * price_per_kg
                    value_per_kg_waste = value / waste_amount if waste_amount > 0 else 0
                    
                    # Show breakdown
                    st.markdown("### 🔢 Breakdown Perhitungan")
                    st.code(f"""
Input Limbah:        {waste_amount:,.0f} kg
Yield:               {yield_pct}%
Output Produk:       {waste_amount:,.0f} kg × {yield_pct}% = {output_kg:,.2f} kg

Harga Jual:          Rp {price_per_kg:,.0f}/kg
Nilai Total:         {output_kg:,.2f} kg × Rp {price_per_kg:,.0f} = Rp {value:,.0f}

Nilai per kg Limbah: Rp {value:,.0f} / {waste_amount:,.0f} kg = Rp {value_per_kg_waste:,.0f}/kg
                    """)
                    
                    # Metrics
                    col_v1, col_v2, col_v3 = st.columns(3)
                    
                    with col_v1:
                        st.metric("Output", f"{output_kg:,.0f} kg", f"{yield_pct}% dari input")
                    
                    with col_v2:
                        st.metric("Nilai Total", f"Rp {value:,.0f}", f"@ Rp {price_per_kg:,.0f}/kg")
                    
                    with col_v3:
                        st.metric("Nilai/kg Limbah", f"Rp {value_per_kg_waste:,.0f}", "Profit margin")
                    
                elif 'yield_m3_per_kg' in method_data:
                    # Biogas calculation
                    output_m3 = waste_amount * yield_m3
                    value = output_m3 * price_per_m3
                    kwh_equivalent = output_m3 * 2.5  # 1 m³ biogas ≈ 2.5 kWh
                    
                    # Show breakdown
                    st.markdown("### 🔢 Breakdown Perhitungan")
                    st.code(f"""
Input Limbah:        {waste_amount:,.0f} kg
Yield Biogas:        {yield_m3} m³/kg
Output Biogas:       {waste_amount:,.0f} kg × {yield_m3} m³/kg = {output_m3:,.2f} m³

Harga Biogas:        Rp {price_per_m3:,.0f}/m³
Nilai Total:         {output_m3:,.2f} m³ × Rp {price_per_m3:,.0f} = Rp {value:,.0f}

Energi Setara:       {output_m3:,.2f} m³ × 2.5 kWh/m³ = {kwh_equivalent:,.2f} kWh
                    """)
                    
                    # Metrics
                    col_v1, col_v2, col_v3 = st.columns(3)
                    
                    with col_v1:
                        st.metric("Output Biogas", f"{output_m3:,.0f} m³", f"{yield_m3} m³/kg")
                    
                    with col_v2:
                        st.metric("Nilai Total", f"Rp {value:,.0f}", f"@ Rp {price_per_m3:,.0f}/m³")
                    
                    with col_v3:
                        st.metric("Energi", f"{kwh_equivalent:,.0f} kWh", "Setara listrik")
                
                # Additional info
                st.markdown("### 💡 Tips Optimasi")
                st.info(f"""
                **Cara Meningkatkan Nilai:**
                - Tingkatkan yield dengan proses yang lebih baik
                - Cari pembeli dengan harga lebih tinggi
                - Diversifikasi produk dari limbah yang sama
                - Pertimbangkan value chain lebih panjang (processing lanjutan)
                """)
    
    with subtab2:
        st.markdown("### 🔥 Biogas Production Calculator")
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            feedstock = st.selectbox("Bahan Baku", list(circular_calc.BIOGAS_POTENTIAL.keys()))
            daily_input = st.number_input("Input Harian (kg)", 10, 1000, 100, 10)
        
        with col_b2:
            efficiency = st.slider("Efisiensi Digester (%)", 50, 90, 70) / 100
        
        if st.button("⚡ Hitung Produksi Biogas", type="primary"):
            result = circular_calc.calculate_biogas_potential(feedstock, daily_input, efficiency)
            
            st.markdown("---")
            st.markdown("### Produksi Biogas")
            
            col_bg1, col_bg2, col_bg3, col_bg4 = st.columns(4)
            
            with col_bg1:
                st.metric("Harian", f"{result['daily_biogas_m3']} m³")
            
            with col_bg2:
                st.metric("Bulanan", f"{result['monthly_biogas_m3']} m³")
            
            with col_bg3:
                st.metric("Tahunan", f"{result['annual_biogas_m3']} m³")
            
            with col_bg4:
                st.metric("Nilai/Tahun", f"Rp {result['annual_value']:,.0f}")
            
            st.success(f"🌍 Pengurangan CO₂: {result['co2_reduction_kg']:,.0f} kg/tahun")
    
    with subtab3:
        st.markdown("### 🍂 Composting Time Estimator")
        
        # Material database with C:N ratios
        COMPOST_MATERIALS = {
            'Bahan Hijau (Nitrogen Tinggi)': {
                'Rumput Segar': {'cn_ratio': 15, 'moisture': 80},
                'Sisa Sayuran': {'cn_ratio': 12, 'moisture': 85},
                'Kotoran Ayam': {'cn_ratio': 10, 'moisture': 75},
                'Kotoran Sapi': {'cn_ratio': 18, 'moisture': 80},
                'Ampas Kopi': {'cn_ratio': 20, 'moisture': 70}
            },
            'Bahan Coklat (Carbon Tinggi)': {
                'Jerami Padi': {'cn_ratio': 80, 'moisture': 15},
                'Daun Kering': {'cn_ratio': 60, 'moisture': 10},
                'Serbuk Gergaji': {'cn_ratio': 500, 'moisture': 20},
                'Sekam Padi': {'cn_ratio': 120, 'moisture': 12},
                'Kertas/Kardus': {'cn_ratio': 170, 'moisture': 5}
            }
        }
        
        st.markdown("### 📝 Input Komposisi Bahan")
        st.info("💡 Tip: Campuran ideal = 1 bagian bahan hijau : 2-3 bagian bahan coklat")
        
        # Initialize session state for materials
        if 'compost_materials' not in st.session_state:
            st.session_state.compost_materials = []
        
        # Add material form
        with st.expander("➕ Tambah Bahan Kompos", expanded=True):
            col_add1, col_add2, col_add3 = st.columns(3)
            
            with col_add1:
                category = st.selectbox("Kategori", list(COMPOST_MATERIALS.keys()), key="cat_select")
            
            with col_add2:
                material_name = st.selectbox("Nama Bahan", list(COMPOST_MATERIALS[category].keys()), key="mat_select")
            
            with col_add3:
                amount_kg = st.number_input("Jumlah (kg)", 1, 1000, 10, 1, key="amount_input")
            
            if st.button("➕ Tambahkan Bahan"):
                material_data = COMPOST_MATERIALS[category][material_name]
                st.session_state.compost_materials.append({
                    'name': material_name,
                    'category': category,
                    'amount_kg': amount_kg,
                    'cn_ratio': material_data['cn_ratio'],
                    'moisture': material_data['moisture']
                })
                st.success(f"✅ Ditambahkan: {amount_kg} kg {material_name}")
                st.rerun()
        
        # Display current materials
        if st.session_state.compost_materials:
            st.markdown("### 📋 Komposisi Campuran")
            
            # Create DataFrame
            import pandas as pd
            df = pd.DataFrame(st.session_state.compost_materials)
            
            # Calculate totals
            total_weight = df['amount_kg'].sum()
            df['proportion_%'] = (df['amount_kg'] / total_weight * 100).round(1)
            
            # Display table
            st.dataframe(
                df[['name', 'category', 'amount_kg', 'proportion_%', 'cn_ratio', 'moisture']],
                use_container_width=True,
                hide_index=True
            )
            
            # Clear button
            if st.button("🗑️ Hapus Semua Bahan"):
                st.session_state.compost_materials = []
                st.rerun()
            
            # Calculate weighted average C:N ratio
            weighted_cn = sum(m['cn_ratio'] * m['amount_kg'] for m in st.session_state.compost_materials) / total_weight
            weighted_moisture = sum(m['moisture'] * m['amount_kg'] for m in st.session_state.compost_materials) / total_weight
            
            st.markdown("---")
            st.markdown("### ⚙️ Parameter Komposting")
            
            col_p1, col_p2 = st.columns(2)
            
            with col_p1:
                st.metric("C:N Ratio Campuran", f"{weighted_cn:.1f}:1")
                st.metric("Kelembaban Rata-rata", f"{weighted_moisture:.0f}%")
            
            with col_p2:
                # Adjustable parameters
                moisture_adjust = st.slider(
                    "Kelembaban Target (%)", 
                    30, 80, 
                    int(weighted_moisture),
                    help="Sesuaikan dengan menambah/kurangi air"
                )
                
                turning = st.selectbox("Frekuensi Pembalikan", [
                    "daily", "every_2_days", "weekly", "biweekly", "monthly"
                ], format_func=lambda x: {
                    "daily": "Harian",
                    "every_2_days": "2 Hari Sekali",
                    "weekly": "Mingguan",
                    "biweekly": "2 Minggu Sekali",
                    "monthly": "Bulanan"
                }[x])
            
            # Calculate button
            if st.button("⏱️ Estimasi Waktu Komposting", type="primary"):
                result = circular_calc.calculate_composting_time(
                    "Campuran", 
                    weighted_cn, 
                    moisture_adjust, 
                    turning
                )
                
                st.markdown("---")
                st.markdown("### 📊 Hasil Estimasi")
                
                col_r1, col_r2, col_r3 = st.columns(3)
                
                with col_r1:
                    st.metric("Estimasi Waktu", f"{result['estimated_days']} hari")
                    st.caption(f"({result['estimated_weeks']} minggu)")
                
                with col_r2:
                    st.metric("Total Bahan", f"{total_weight} kg")
                    
                    # Estimate output (60-70% of input)
                    output_estimate = total_weight * 0.65
                    st.metric("Estimasi Output", f"{output_estimate:.0f} kg")
                
                with col_r3:
                    # C:N ratio status
                    if 25 <= weighted_cn <= 30:
                        cn_status = "🟢 Optimal"
                    elif 20 <= weighted_cn < 25 or 30 < weighted_cn <= 35:
                        cn_status = "🟡 Cukup Baik"
                    else:
                        cn_status = "🔴 Perlu Penyesuaian"
                    
                    st.metric("Status C:N Ratio", cn_status)
                    st.caption(f"Optimal: 25-30:1")
                
                # Breakdown by category
                st.markdown("### 📈 Komposisi Campuran")
                
                green_total = sum(m['amount_kg'] for m in st.session_state.compost_materials if 'Hijau' in m['category'])
                brown_total = sum(m['amount_kg'] for m in st.session_state.compost_materials if 'Coklat' in m['category'])
                
                col_b1, col_b2 = st.columns(2)
                
                with col_b1:
                    st.success(f"""
                    **🟢 Bahan Hijau (N-tinggi)**
                    - Total: {green_total} kg ({green_total/total_weight*100:.0f}%)
                    - Fungsi: Sumber nitrogen, mempercepat dekomposisi
                    """)
                
                with col_b2:
                    st.warning(f"""
                    **🟤 Bahan Coklat (C-tinggi)**
                    - Total: {brown_total} kg ({brown_total/total_weight*100:.0f}%)
                    - Fungsi: Sumber karbon, struktur aerasi
                    """)
                
                # Recommendations
                st.markdown("### 💡 Rekomendasi")
                
                for rec in result['recommendations']:
                    st.info(f"✅ {rec}")
                
                # Additional tips based on composition
                if green_total / total_weight > 0.4:
                    st.warning("⚠️ Terlalu banyak bahan hijau. Tambahkan bahan coklat untuk menghindari bau dan meningkatkan aerasi.")
                elif brown_total / total_weight > 0.8:
                    st.warning("⚠️ Terlalu banyak bahan coklat. Tambahkan bahan hijau untuk mempercepat dekomposisi.")
                else:
                    st.success("✅ Komposisi campuran sudah baik!")
        
        else:
            st.info("👆 Mulai dengan menambahkan bahan kompos di atas")
            
            # Show example composition
            with st.expander("📚 Contoh Komposisi Kompos"):
                st.markdown("""
                **Kompos Standar (100 kg):**
                - Rumput Segar: 20 kg
                - Sisa Sayuran: 10 kg
                - Kotoran Sapi: 20 kg
                - Jerami Padi: 30 kg
                - Daun Kering: 20 kg
                
                **Hasil:**
                - C:N Ratio: ~28:1 (Optimal)
                - Waktu: 45-60 hari
                - Output: ~65 kg kompos matang
                """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🌱 <strong>AgriSensa Sustainability Toolkit</strong></p>
    <p>Regenerative Agriculture | Climate Adaptation | Circular Economy</p>
</div>
""", unsafe_allow_html=True)
