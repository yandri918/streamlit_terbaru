"""
Demo Page: AI Nutrient Optimizer
Halaman demo untuk fitur AI Nutrient Optimizer
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.ai_nutrient_optimizer import AInutrientOptimizer

# Page config
st.set_page_config(
    page_title="AI Nutrient Optimizer - AgriSensa",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}
.success-box {
    background: #d4edda;
    border-left: 4px solid #28a745;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
.warning-box {
    background: #fff3cd;
    border-left: 4px solid #ffc107;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
.danger-box {
    background: #f8d7da;
    border-left: 4px solid #dc3545;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 AI Nutrient Optimizer</h1>
    <p>Sistem Optimasi Nutrisi Hidroponik Berbasis Kecerdasan Buatan</p>
    <p><strong>Rekomendasi Presisi | Analisis Real-time | Hemat Biaya</strong></p>
</div>
""", unsafe_allow_html=True)

# Initialize service
optimizer = AInutrientOptimizer()

# Tabs
tab1, tab2, tab3 = st.tabs([
    "🎯 Rekomendasi AI",
    "📊 Analisis Kondisi",
    "💰 Kalkulator Biaya"
])

with tab1:
    st.header("🎯 Rekomendasi Nutrisi AI")
    st.info("💡 **AI akan menganalisis** tanaman, fase pertumbuhan, dan kondisi saat ini untuk memberikan rekomendasi nutrisi yang optimal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Data Tanaman")
        
        tanaman = st.selectbox(
            "Pilih Tanaman",
            ["Selada", "Tomat", "Cabai", "Strawberry", "Timun", "Kangkung", "Pakcoy"],
            help="Pilih jenis tanaman yang Anda budidayakan"
        )
        
        # Get available phases for selected plant
        available_phases = list(optimizer.OPTIMAL_PARAMETERS.get(tanaman, {}).keys())
        fase = st.selectbox(
            "Fase Pertumbuhan",
            available_phases,
            help="Pilih fase pertumbuhan tanaman saat ini"
        )
        
        target_hasil = st.selectbox(
            "Target Hasil",
            ["Standard", "Tinggi", "Maksimal"],
            help="Standard = Normal, Tinggi = +10% nutrisi, Maksimal = +20% nutrisi"
        )
        
        volume = st.number_input(
            "Volume Larutan (Liter)",
            min_value=10,
            max_value=1000,
            value=100,
            step=10,
            help="Total volume larutan nutrisi dalam sistem Anda"
        )
    
    with col2:
        st.subheader("🔬 Kondisi Saat Ini")
        
        current_ec = st.number_input(
            "EC Saat Ini (mS/cm)",
            min_value=0.0,
            max_value=5.0,
            value=1.5,
            step=0.1,
            help="Electrical Conductivity - ukur dengan EC meter"
        )
        
        current_ph = st.number_input(
            "pH Saat Ini",
            min_value=4.0,
            max_value=8.0,
            value=6.0,
            step=0.1,
            help="Tingkat keasaman - ukur dengan pH meter"
        )
        
        st.info("""
        **📌 Cara Mengukur:**
        - **EC Meter**: Celupkan probe ke larutan, tunggu stabil
        - **pH Meter**: Kalibrasi dulu, lalu celupkan ke larutan
        - **Waktu Terbaik**: Pagi hari sebelum matahari terik
        """)
    
    # Generate recommendation button
    if st.button("🚀 Generate Rekomendasi AI", type="primary", use_container_width=True):
        with st.spinner("🤖 AI sedang menganalisis..."):
            # Get recommendation
            result = optimizer.generate_recommendation(
                tanaman=tanaman,
                fase=fase,
                current_ec=current_ec,
                current_ph=current_ph,
                target_hasil=target_hasil,
                volume=volume
            )
            
            # Display results
            st.success("✅ Analisis Selesai!")
            
            # Metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            
            with col_m1:
                st.metric(
                    "EC Optimal",
                    f"{result['optimal_ec']} mS/cm",
                    f"{result['optimal_ec'] - current_ec:+.1f}"
                )
            
            with col_m2:
                st.metric(
                    "pH Optimal",
                    f"{result['optimal_ph']}",
                    f"{result['optimal_ph'] - current_ph:+.1f}"
                )
            
            with col_m3:
                st.metric(
                    "Formula Type",
                    result['formula_type'].replace('_', ' ')
                )
            
            with col_m4:
                st.metric(
                    "Biaya Total",
                    f"Rp {result['biaya']['total_biaya']:,.0f}"
                )
            
            st.markdown("---")
            
            # Analysis
            st.subheader("📊 Analisis Kondisi")
            
            analysis = result['analisis']
            
            if analysis['tingkat_keparahan'] == 'Rendah':
                st.markdown(f"""
                <div class="success-box">
                    <h4>✅ {analysis['status']}</h4>
                    <p>{result['insight']}</p>
                </div>
                """, unsafe_allow_html=True)
            elif analysis['tingkat_keparahan'] == 'Sedang':
                st.markdown(f"""
                <div class="warning-box">
                    <h4>⚠️ {analysis['status']}</h4>
                    <p>{result['insight']}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="danger-box">
                    <h4>🚨 {analysis['status']}</h4>
                    <p>{result['insight']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Problems & Recommendations
            if analysis['masalah']:
                st.subheader("⚠️ Masalah Terdeteksi")
                for masalah in analysis['masalah']:
                    st.warning(f"• {masalah}")
            
            if analysis['rekomendasi']:
                st.subheader("💡 Rekomendasi Penyesuaian")
                for rek in analysis['rekomendasi']:
                    st.info(f"✓ {rek}")
            
            # Adjustment Guide
            st.markdown("---")
            st.subheader("🔧 Panduan Penyesuaian")
            
            adjustment = result['penyesuaian']
            
            col_adj1, col_adj2 = st.columns(2)
            
            with col_adj1:
                st.markdown(f"""
                **Aksi:** {adjustment['aksi']}
                
                **Cara:**
                {adjustment['cara']}
                """)
            
            with col_adj2:
                st.info(f"📝 **Catatan:**\n{adjustment['catatan']}")
            
            # Formula Details
            st.markdown("---")
            st.subheader("🧪 Formula Nutrisi Detail")
            st.caption(f"Formula untuk {volume} liter larutan")
            
            import pandas as pd
            
            formula_data = []
            for nutrient, amount in result['formula'].items():
                amount_for_volume = (amount / 100) * volume
                biaya_item = result['biaya']['breakdown'][nutrient]['biaya']
                
                formula_data.append({
                    'Nutrisi': nutrient,
                    'Jumlah (gram)': round(amount_for_volume, 2),
                    'Biaya (Rp)': f"Rp {biaya_item:,.0f}"
                })
            
            df_formula = pd.DataFrame(formula_data)
            st.dataframe(df_formula, use_container_width=True, hide_index=True)
            
            # Cost Summary
            st.markdown("---")
            st.subheader("💰 Ringkasan Biaya")
            
            col_cost1, col_cost2, col_cost3 = st.columns(3)
            
            with col_cost1:
                st.metric(
                    "Total Biaya",
                    f"Rp {result['biaya']['total_biaya']:,.0f}"
                )
            
            with col_cost2:
                st.metric(
                    "Biaya per Liter",
                    f"Rp {result['biaya']['biaya_per_liter']:,.0f}"
                )
            
            with col_cost3:
                # Calculate monthly cost (assume change every 2 weeks)
                monthly_cost = result['biaya']['total_biaya'] * 2
                st.metric(
                    "Biaya per Bulan",
                    f"Rp {monthly_cost:,.0f}",
                    help="Asumsi: Ganti nutrisi setiap 2 minggu"
                )

with tab2:
    st.header("📊 Analisis Kondisi Mendalam")
    st.info("Analisis defisiensi dan kelebihan nutrisi berdasarkan parameter saat ini")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.subheader("Parameter Saat Ini")
        current_ec_a = st.number_input("EC (mS/cm)", 0.0, 5.0, 1.5, 0.1, key="ec_analysis")
        current_ph_a = st.number_input("pH", 4.0, 8.0, 6.0, 0.1, key="ph_analysis")
    
    with col_a2:
        st.subheader("Parameter Target")
        optimal_ec_a = st.number_input("EC Optimal (mS/cm)", 0.0, 5.0, 1.8, 0.1)
        optimal_ph_a = st.number_input("pH Optimal", 4.0, 8.0, 5.8, 0.1)
    
    if st.button("🔍 Analisis", use_container_width=True):
        analysis = optimizer.analyze_deficiency(
            current_ec_a, current_ph_a,
            optimal_ec_a, optimal_ph_a
        )
        
        st.subheader("Hasil Analisis")
        
        # Status
        if analysis['tingkat_keparahan'] == 'Rendah':
            st.success(f"✅ **Status:** {analysis['status']}")
        elif analysis['tingkat_keparahan'] == 'Sedang':
            st.warning(f"⚠️ **Status:** {analysis['status']}")
        else:
            st.error(f"🚨 **Status:** {analysis['status']}")
        
        # Problems
        if analysis['masalah']:
            st.subheader("⚠️ Masalah")
            for masalah in analysis['masalah']:
                st.warning(masalah)
        
        # Recommendations
        if analysis['rekomendasi']:
            st.subheader("💡 Rekomendasi")
            for rek in analysis['rekomendasi']:
                st.info(rek)
        else:
            st.success("✅ Tidak ada penyesuaian yang diperlukan. Kondisi optimal!")

with tab3:
    st.header("💰 Kalkulator Biaya Nutrisi")
    st.info("Hitung biaya nutrisi untuk berbagai volume dan formula")
    
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        formula_type = st.selectbox(
            "Tipe Formula",
            ["Standard", "Tinggi_N", "Tinggi_K", "Tinggi_P"],
            help="Pilih formula sesuai kebutuhan tanaman"
        )
        
        volume_calc = st.number_input(
            "Volume (Liter)",
            10, 1000, 100, 10,
            key="volume_calc"
        )
    
    with col_c2:
        st.markdown("""
        **📌 Panduan Pilih Formula:**
        - **Standard**: Untuk semua fase
        - **Tinggi N**: Fase vegetatif (daun)
        - **Tinggi K**: Fase berbuah
        - **Tinggi P**: Fase berbunga
        """)
    
    if st.button("💵 Hitung Biaya", use_container_width=True):
        formula = optimizer.NUTRIENT_FORMULAS[formula_type]
        cost = optimizer.calculate_cost(formula, volume_calc)
        
        st.subheader("Rincian Biaya")
        
        # Summary metrics
        col_sum1, col_sum2, col_sum3 = st.columns(3)
        
        with col_sum1:
            st.metric("Total Biaya", f"Rp {cost['total_biaya']:,.0f}")
        
        with col_sum2:
            st.metric("Per Liter", f"Rp {cost['biaya_per_liter']:,.0f}")
        
        with col_sum3:
            monthly = cost['total_biaya'] * 2
            st.metric("Per Bulan", f"Rp {monthly:,.0f}")
        
        # Breakdown table
        st.subheader("Detail per Nutrisi")
        
        import pandas as pd
        
        breakdown_data = []
        for nutrient, data in cost['breakdown'].items():
            breakdown_data.append({
                'Nutrisi': nutrient,
                'Jumlah (g)': data['jumlah_gram'],
                'Biaya (Rp)': f"Rp {data['biaya']:,.0f}",
                '% dari Total': f"{(data['biaya']/cost['total_biaya']*100):.1f}%"
            })
        
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
        
        # Cost comparison
        st.markdown("---")
        st.subheader("📊 Perbandingan dengan Nutrisi Komersial")
        
        col_comp1, col_comp2 = st.columns(2)
        
        with col_comp1:
            st.markdown("""
            **DIY (Formula Anda):**
            - Biaya: Rp {biaya:,.0f}
            - Per liter: Rp {per_liter:,.0f}
            - Kualitas: Terkontrol
            - Fleksibilitas: Tinggi
            """.format(
                biaya=cost['total_biaya'],
                per_liter=cost['biaya_per_liter']
            ))
        
        with col_comp2:
            # Estimate commercial price (usually 3-5x more expensive)
            commercial_price = cost['total_biaya'] * 4
            st.markdown("""
            **Nutrisi Komersial (Est.):**
            - Biaya: Rp {biaya:,.0f}
            - Per liter: Rp {per_liter:,.0f}
            - Kualitas: Standar
            - Fleksibilitas: Rendah
            """.format(
                biaya=commercial_price,
                per_liter=commercial_price/volume_calc
            ))
        
        savings = commercial_price - cost['total_biaya']
        savings_pct = (savings / commercial_price) * 100
        
        st.success(f"""
        💰 **Penghematan:** Rp {savings:,.0f} ({savings_pct:.0f}%)
        
        Dengan membuat sendiri, Anda hemat {savings_pct:.0f}% dibanding beli jadi!
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    <p><strong>🤖 AI Nutrient Optimizer</strong> - Powered by AgriSensa</p>
    <p>Teknologi AI untuk Pertanian Modern Indonesia</p>
</div>
""", unsafe_allow_html=True)
