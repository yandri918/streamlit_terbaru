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
        
        if method and st.button("💰 Hitung Nilai", type="primary"):
            result = circular_calc.calculate_waste_valorization(waste_type, waste_amount, method)
            
            if 'error' not in result:
                st.markdown("---")
                
                col_v1, col_v2, col_v3 = st.columns(3)
                
                with col_v1:
                    if 'output_kg' in result:
                        st.metric("Output", f"{result['output_kg']:,.0f} kg")
                    elif 'output_m3' in result:
                        st.metric("Output", f"{result['output_m3']:,.0f} m³")
                
                with col_v2:
                    st.metric("Nilai Total", f"Rp {result['value']:,.0f}")
                
                with col_v3:
                    if 'value_per_kg_waste' in result:
                        st.metric("Nilai/kg Limbah", f"Rp {result['value_per_kg_waste']:,.0f}")
                    elif 'kwh_equivalent' in result:
                        st.metric("Energi", f"{result['kwh_equivalent']:,.0f} kWh")
    
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
        
        col_c1, col_c2 = st.columns(2)
        
        with col_c1:
            material = st.text_input("Jenis Material", "Campuran")
            cn_ratio = st.number_input("C:N Ratio", 10, 50, 28, 1)
        
        with col_c2:
            moisture = st.slider("Kelembaban (%)", 30, 80, 55)
            turning = st.selectbox("Frekuensi Pembalikan", [
                "daily", "every_2_days", "weekly", "biweekly", "monthly"
            ], format_func=lambda x: {
                "daily": "Harian",
                "every_2_days": "2 Hari Sekali",
                "weekly": "Mingguan",
                "biweekly": "2 Minggu Sekali",
                "monthly": "Bulanan"
            }[x])
        
        if st.button("⏱️ Estimasi Waktu", type="primary"):
            result = circular_calc.calculate_composting_time(material, cn_ratio, moisture, turning)
            
            st.markdown("---")
            
            col_t1, col_t2 = st.columns(2)
            
            with col_t1:
                st.metric("Estimasi Waktu", f"{result['estimated_days']} hari")
                st.metric("", f"({result['estimated_weeks']} minggu)")
            
            with col_t2:
                st.info(f"""
                **Kondisi Optimal:**
                - C:N Ratio: {result['optimal_cn_ratio']}
                - Kelembaban: {result['optimal_moisture']}
                """)
            
            st.markdown("### Rekomendasi")
            for rec in result['recommendations']:
                st.success(f"✅ {rec}")


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🌱 <strong>AgriSensa Sustainability Toolkit</strong></p>
    <p>Regenerative Agriculture | Climate Adaptation | Circular Economy</p>
</div>
""", unsafe_allow_html=True)
