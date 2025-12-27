import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.advanced_sustainability_calculator import AdvancedSustainabilityCalculator
from utils.auth import require_auth, show_user_info_sidebar

# Page config
st.set_page_config(
    page_title="Advanced Sustainability",
    page_icon="🌍",
    layout="wide"
)

# Authentication
user = require_auth()
show_user_info_sidebar()

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f9ff;
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
st.title("🌍 Advanced Sustainability Features")
st.markdown("""
Fitur lanjutan untuk valuasi ekosistem, precision conservation, kearifan lokal, dan ESG reporting
""")

st.markdown("---")

# Initialize calculator
calc = AdvancedSustainabilityCalculator()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌳 Ecosystem Services",
    "🔬 Precision Conservation",
    "🌿 Indigenous Knowledge",
    "📊 ESG Reporting"
])

# ===== TAB 1: ECOSYSTEM SERVICES VALUATION =====
with tab1:
    st.subheader("Valuasi Jasa Ekosistem")
    
    st.info("""
    💡 **Jasa Ekosistem** adalah manfaat yang diberikan ekosistem kepada manusia.
    Valuasi ekonomi membantu menunjukkan nilai riil dari konservasi alam.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        land_type = st.selectbox("Tipe Lahan", [
            "forest",
            "agroforestry",
            "cropland",
            "terraced_cropland",
            "grassland",
            "wetland",
            "diverse_agroforestry",
            "organic_farm",
            "conventional_farm"
        ], format_func=lambda x: {
            "forest": "Hutan",
            "agroforestry": "Agroforestri",
            "cropland": "Lahan Pertanian",
            "terraced_cropland": "Lahan Teras",
            "grassland": "Padang Rumput",
            "wetland": "Lahan Basah",
            "diverse_agroforestry": "Agroforestri Beragam",
            "organic_farm": "Pertanian Organik",
            "conventional_farm": "Pertanian Konvensional"
        }[x])
        
        area_ha = st.number_input("Luas Lahan (ha)", 1, 1000, 10, 1)
    
    with col2:
        services = st.multiselect("Pilih Jasa Ekosistem", [
            "carbon_sequestration",
            "water_regulation",
            "soil_conservation",
            "pollination",
            "biodiversity_habitat"
        ], default=["carbon_sequestration", "water_regulation"],
        format_func=lambda x: {
            "carbon_sequestration": "Penyerapan Karbon",
            "water_regulation": "Regulasi Air",
            "soil_conservation": "Konservasi Tanah",
            "pollination": "Penyerbukan",
            "biodiversity_habitat": "Habitat Biodiversitas"
        }[x])
    
    if st.button("💰 Hitung Nilai Ekosistem", type="primary"):
        result = calc.calculate_ecosystem_services_value(land_type, area_ha, services)
        
        st.markdown("---")
        st.markdown("### 📊 Hasil Valuasi")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric("Nilai Total/Tahun", f"Rp {result['total_annual_value']:,.0f}")
        
        with col_m2:
            st.metric("Nilai per Hektar", f"Rp {result['value_per_ha']:,.0f}/ha")
        
        with col_m3:
            st.metric("Luas Lahan", f"{result['area_ha']} ha")
        
        # Breakdown
        st.markdown("### 🔢 Breakdown per Jasa")
        
        for service, data in result['breakdown'].items():
            service_name = {
                "carbon_sequestration": "🌳 Penyerapan Karbon",
                "water_regulation": "💧 Regulasi Air",
                "soil_conservation": "🌾 Konservasi Tanah",
                "pollination": "🐝 Penyerbukan",
                "biodiversity_habitat": "🦋 Habitat Biodiversitas"
            }.get(service, service)
            
            st.success(f"""
            **{service_name}**
            - Nilai per ha: Rp {data['value_per_ha']:,.0f}/ha/tahun
            - Total nilai: Rp {data['total_value']:,.0f}/tahun
            """)
        
        # Visualization
        st.markdown("### 📈 Visualisasi Nilai")
        
        labels = [s.replace('_', ' ').title() for s in result['breakdown'].keys()]
        values = [d['total_value'] for d in result['breakdown'].values()]
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.3)])
        fig.update_layout(title="Distribusi Nilai Jasa Ekosistem")
        st.plotly_chart(fig, use_container_width=True)


# ===== TAB 2: PRECISION CONSERVATION =====
with tab2:
    st.subheader("Precision Conservation Agriculture")
    
    st.info("""
    💡 **Precision Conservation** menggunakan teknologi untuk aplikasi input yang lebih tepat,
    mengurangi pemborosan dan meningkatkan efisiensi.
    """)
    
    st.markdown("### 🎯 Variable Rate Application (VRA) Calculator")
    
    col_p1, col_p2 = st.columns(2)
    
    with col_p1:
        area_vra = st.number_input("Luas Lahan (ha)", 1, 1000, 10, 1, key="vra_area")
        current_rate = st.number_input("Aplikasi Saat Ini (kg/ha)", 50, 500, 200, 10,
                                      help="Dosis pupuk/pestisida saat ini")
    
    with col_p2:
        optimal_rate = st.number_input("Aplikasi Optimal (kg/ha)", 50, 500, 150, 10,
                                       help="Dosis optimal berdasarkan soil test/mapping")
        input_price = st.number_input("Harga Input (Rp/kg)", 1000, 50000, 5000, 500)
    
    if st.button("📊 Hitung Penghematan VRA", type="primary"):
        result = calc.calculate_precision_conservation_savings(
            area_vra, current_rate, optimal_rate, input_price
        )
        
        st.markdown("---")
        st.markdown("### 💰 Hasil Analisis")
        
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        
        with col_r1:
            st.metric("Input Saat Ini", f"{result['current_total_kg']:,.0f} kg")
        
        with col_r2:
            st.metric("Input Optimal", f"{result['optimal_total_kg']:,.0f} kg")
        
        with col_r3:
            st.metric("Penghematan", f"{result['input_saved_kg']:,.0f} kg",
                     f"{result['savings_pct']:.1f}%")
        
        with col_r4:
            st.metric("Nilai Penghematan", f"Rp {result['cost_saved']:,.0f}")
        
        st.success(f"🌾 Bonus: Peningkatan yield ~{result['yield_improvement_pct']}% dari aplikasi yang lebih tepat")
        
        # Breakdown
        st.markdown("### 🔢 Breakdown Perhitungan")
        st.code(f"""
Luas Lahan:          {area_vra} ha
Aplikasi Saat Ini:   {current_rate} kg/ha
Input Total:         {area_vra} ha × {current_rate} kg/ha = {result['current_total_kg']:,.0f} kg

Aplikasi Optimal:    {optimal_rate} kg/ha  
Input Optimal:       {area_vra} ha × {optimal_rate} kg/ha = {result['optimal_total_kg']:,.0f} kg

Penghematan:         {result['current_total_kg']:,.0f} - {result['optimal_total_kg']:,.0f} = {result['input_saved_kg']:,.0f} kg
Nilai:               {result['input_saved_kg']:,.0f} kg × Rp {input_price:,.0f} = Rp {result['cost_saved']:,.0f}
        """)
        
        st.markdown("### 💡 Implementasi VRA")
        st.info("""
        **Langkah-langkah:**
        1. **Soil Sampling**: Grid sampling (1 sample per 0.5-1 ha)
        2. **Mapping**: Buat peta kesuburan tanah
        3. **Prescription Map**: Tentukan dosis per zona
        4. **VRA Equipment**: GPS-guided spreader/sprayer
        5. **Monitoring**: Track hasil dan adjust
        
        **ROI**: Biasanya 1-2 tahun untuk investasi VRA equipment
        """)


# ===== TAB 3: INDIGENOUS KNOWLEDGE =====
with tab3:
    st.subheader("Database Kearifan Lokal Pertanian")
    
    st.info("""
    💡 **Kearifan Lokal** adalah pengetahuan tradisional yang telah terbukti berkelanjutan selama berabad-abad.
    Digitalisasi membantu preservasi dan aplikasi modern.
    """)
    
    # Display practices
    for practice_name, practice_data in calc.INDIGENOUS_PRACTICES.items():
        with st.expander(f"📚 {practice_name}"):
            col_k1, col_k2 = st.columns(2)
            
            with col_k1:
                st.markdown(f"""
                **Deskripsi:**  
                {practice_data['description']}
                
                **Aplikasi:**  
                {practice_data['application']}
                """)
            
            with col_k2:
                st.markdown(f"""
                **Relevansi Modern:**  
                {practice_data['relevance']}
                
                **Wilayah:**  
                {practice_data['region']}
                """)
    
    # Add new practice form
    st.markdown("---")
    st.markdown("### ➕ Kontribusi Kearifan Lokal")
    
    with st.expander("Tambahkan Praktik Tradisional"):
        practice_name_new = st.text_input("Nama Praktik")
        description_new = st.text_area("Deskripsi")
        application_new = st.text_area("Cara Aplikasi")
        region_new = st.text_input("Wilayah Asal")
        
        if st.button("📝 Submit Kontribusi"):
            st.success("""
            ✅ Terima kasih atas kontribusinya!
            
            Tim kami akan review dan menambahkan ke database jika sesuai kriteria.
            """)


# ===== TAB 4: ESG REPORTING =====
with tab4:
    st.subheader("ESG Reporting Dashboard")
    
    st.info("""
    💡 **ESG (Environmental, Social, Governance)** adalah framework untuk mengukur keberlanjutan bisnis.
    Penting untuk akses green finance dan premium market.
    """)
    
    st.markdown("### 📋 Input Metrics")
    
    # Environmental Metrics
    st.markdown("#### 🌍 Environmental (40%)")
    col_e1, col_e2 = st.columns(2)
    
    with col_e1:
        carbon_reduction = st.slider("Carbon Footprint Reduction (%)", 0, 100, 50,
                                     help="Pengurangan emisi CO₂ vs baseline")
        water_efficiency = st.slider("Water Use Efficiency (%)", 0, 100, 60,
                                    help="Efisiensi penggunaan air")
    
    with col_e2:
        biodiversity = st.slider("Biodiversity Index", 0, 100, 70,
                                help="Shannon/Simpson index atau species count")
        waste_reduction = st.slider("Waste Reduction (%)", 0, 100, 55,
                                   help="Pengurangan limbah vs baseline")
    
    # Social Metrics
    st.markdown("#### 👥 Social (30%)")
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        fair_labor = st.slider("Fair Labor Practices", 0, 100, 75,
                              help="Upah layak, kondisi kerja, no child labor")
        community = st.slider("Community Engagement", 0, 100, 65,
                             help="Program CSR, local hiring, training")
    
    with col_s2:
        food_security = st.slider("Food Security Contribution", 0, 100, 70,
                                 help="Kontribusi ke ketahanan pangan lokal")
    
    # Governance Metrics
    st.markdown("#### 📜 Governance (30%)")
    col_g1, col_g2 = st.columns(2)
    
    with col_g1:
        certification = st.slider("Certification Compliance", 0, 100, 60,
                                 help="Sertifikasi (Organic, GAP, Fair Trade, dll)")
        traceability = st.slider("Traceability Score", 0, 100, 55,
                                help="Kemampuan tracking produk")
    
    with col_g2:
        transparency = st.slider("Transparency Index", 0, 100, 65,
                                help="Keterbukaan data dan reporting")
    
    if st.button("📊 Generate ESG Report", type="primary"):
        # Prepare metrics
        env_metrics = {
            'carbon_footprint_reduction': carbon_reduction,
            'water_efficiency': water_efficiency,
            'biodiversity_index': biodiversity,
            'waste_reduction': waste_reduction
        }
        
        soc_metrics = {
            'fair_labor': fair_labor,
            'community_engagement': community,
            'food_security': food_security
        }
        
        gov_metrics = {
            'certification_compliance': certification,
            'traceability': traceability,
            'transparency': transparency
        }
        
        result = calc.calculate_esg_score(env_metrics, soc_metrics, gov_metrics)
        
        st.markdown("---")
        st.markdown("### 🏆 ESG Scorecard")
        
        # Overall score
        col_o1, col_o2, col_o3, col_o4 = st.columns(4)
        
        with col_o1:
            st.metric("Overall ESG Score", f"{result['overall_score']}/100", result['rating'])
        
        with col_o2:
            st.metric("Environmental", f"{result['environmental_score']}/100", "40% weight")
        
        with col_o3:
            st.metric("Social", f"{result['social_score']}/100", "30% weight")
        
        with col_o4:
            st.metric("Governance", f"{result['governance_score']}/100", "30% weight")
        
        # Radar chart
        st.markdown("### 📈 ESG Profile")
        
        categories = ['Environmental', 'Social', 'Governance']
        values = [result['environmental_score'], result['social_score'], result['governance_score']]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Your Score'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 Rekomendasi Perbaikan")
        
        if result['environmental_score'] < 70:
            st.warning("🌍 **Environmental**: Tingkatkan praktik ramah lingkungan (carbon reduction, water efficiency)")
        
        if result['social_score'] < 70:
            st.warning("👥 **Social**: Perkuat program kesejahteraan pekerja dan community engagement")
        
        if result['governance_score'] < 70:
            st.warning("📜 **Governance**: Dapatkan sertifikasi dan tingkatkan traceability")
        
        if result['overall_score'] >= 75:
            st.success("""
            ✅ **Excellent ESG Performance!**
            
            Anda eligible untuk:
            - Green financing dengan bunga rendah
            - Premium market access (organic, fair trade)
            - ESG investment funds
            - Corporate partnerships (CSR)
            """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🌍 <strong>AgriSensa Advanced Sustainability</strong></p>
    <p>Ecosystem Services | Precision Conservation | Indigenous Knowledge | ESG Reporting</p>
</div>
""", unsafe_allow_html=True)
