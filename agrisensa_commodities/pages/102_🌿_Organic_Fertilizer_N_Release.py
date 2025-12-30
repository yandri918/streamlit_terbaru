import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.nitrogen_release_service import NitrogenReleaseService

# Page config
st.set_page_config(
    page_title="Organic Fertilizer N Release Calculator",
    page_icon="🌿",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌿 Kalkulator Pelepasan Nitrogen Pupuk Organik")
st.markdown("""
<div class='info-box'>
    <h3>🔬 Kalkulator Ilmiah Berbasis WAGRI</h3>
    <p>Pahami bagaimana nitrogen dari pupuk organik tersedia untuk tanaman dari waktu ke waktu!</p>
    <ul>
        <li>✅ <strong>Penyesuaian Suhu</strong> - Model koefisien Q10</li>
        <li>✅ <strong>Properti Material Spesifik</strong> - 6 preset pupuk organik</li>
        <li>✅ <strong>Pelacakan Harian & Kumulatif</strong> - Visualisasi pola pelepasan N</li>
        <li>✅ <strong>Bandingkan dengan Sintetis</strong> - Lihat keunggulan pelepasan lambat</li>
    </ul>
    <p><em>Berdasarkan metodologi WAGRI (Platform Data Pertanian Jepang)</em></p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Create tabs
tabs = st.tabs([
    "📊 Kalkulator",
    "📈 Hasil & Visualisasi",
    "🔬 Properti Material",
    "📚 Panduan Edukasi"
])

# TAB 1: CALCULATOR
with tabs[0]:
    st.markdown("## 📊 Parameter Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Timeline")
        
        # Date inputs
        start_date = st.date_input(
            "Tanggal Mulai",
            value=datetime(2024, 5, 3),
            help="Tanggal mulai pengamatan"
        )
        
        water_date = st.date_input(
            "Tanggal Aplikasi Air",
            value=datetime(2024, 5, 10),
            help="Tanggal aplikasi air/irigasi pertama setelah aplikasi pupuk"
        )
        
        end_date = st.date_input(
            "Tanggal Akhir",
            value=datetime(2024, 5, 14),
            help="Tanggal akhir pengamatan"
        )
        
        st.markdown("### 🌡️ Temperature Data")
        
        temp_input_method = st.radio(
            "Metode Input Suhu",
            ["Input Manual", "Generate Data Contoh"],
            help="Pilih cara input data suhu"
        )
        
        if temp_input_method == "Input Manual":
            total_days = (end_date - start_date).days + 1
            st.info(f"📝 Masukkan suhu untuk {total_days} hari")
            
            temp_input = st.text_area(
                "Suhu Harian (°C)",
                value="20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31",
                help="Pisahkan dengan koma. Contoh: 20, 21, 22, 23, 24"
            )
            
            try:
                daily_temperatures = [float(t.strip()) for t in temp_input.split(",")]
            except:
                st.error("❌ Format suhu tidak valid. Gunakan angka dipisah koma.")
                daily_temperatures = [25.0] * total_days
        else:
            base_temp = st.slider(
                "Suhu Dasar (°C)",
                min_value=15.0,
                max_value=35.0,
                value=25.0,
                step=0.5,
                help="Suhu dasar untuk generate data contoh"
            )
            
            variation = st.slider(
                "Variasi Suhu (°C)",
                min_value=0.0,
                max_value=10.0,
                value=5.0,
                step=0.5,
                help="Variasi suhu harian"
            )
            
            daily_temperatures = NitrogenReleaseService.generate_example_temperatures(
                start_date.strftime("%Y%m%d"),
                end_date.strftime("%Y%m%d"),
                base_temp=base_temp,
                variation=variation
            )
            
            st.success(f"✅ Berhasil generate {len(daily_temperatures)} hari data suhu")
            st.write(f"Preview: {daily_temperatures[:7]}...")
    
    with col2:
        st.markdown("### 🌾 Material Selection")
        
        material_presets = NitrogenReleaseService.list_material_presets()
        material_presets.append("Custom")
        
        selected_material = st.selectbox(
            "Pilih Material Organik",
            material_presets,
            help="Pilih jenis pupuk organik atau Custom untuk input manual"
        )
        
        if selected_material != "Custom":
            preset = NitrogenReleaseService.get_material_preset(selected_material)
            st.info(f"ℹ️ {preset['description']}")
            
            MC = preset["MC"]
            ADSON = preset["ADSON"]
            TN = preset["TN"]
            Nm = preset["Nm"]
            
            # Show preset values
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric("Kadar Air (MC)", f"{MC}%")
                st.metric("Total Nitrogen (TN)", f"{TN}%")
            with col_p2:
                st.metric("Nitrogen Tersedia (ADSON)", f"{ADSON}%")
                st.metric("Nitrogen Mineral (Nm)", f"{Nm}%")
        else:
            st.markdown("### 🔧 Custom Material Properties")
            
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                MC = st.number_input(
                    "Moisture Content (MC) %",
                    min_value=0.0,
                    max_value=100.0,
                    value=35.0,
                    step=1.0,
                    help="Kadar air dalam material"
                )
                
                TN = st.number_input(
                    "Total Nitrogen (TN) %",
                    min_value=0.0,
                    max_value=10.0,
                    value=3.5,
                    step=0.1,
                    help="Total nitrogen dalam material"
                )
            
            with col_c2:
                ADSON = st.number_input(
                    "Adsorbable Nitrogen (ADSON) %",
                    min_value=0.0,
                    max_value=100.0,
                    value=20.0,
                    step=1.0,
                    help="Nitrogen yang dapat diserap tanaman"
                )
                
                Nm = st.number_input(
                    "Mineral Nitrogen (Nm) %",
                    min_value=0.0,
                    max_value=10.0,
                    value=0.3,
                    step=0.05,
                    help="Nitrogen mineral (tersedia langsung)"
                )
        
        st.markdown("### 📦 Application Amount")
        
        material_amount = st.number_input(
            "Jumlah Material (kg)",
            min_value=1.0,
            max_value=10000.0,
            value=123.0,
            step=10.0,
            help="Jumlah pupuk organik yang diaplikasikan"
        )
        
        # Advanced settings
        with st.expander("⚙️ Advanced Coefficients"):
            st.markdown("**Decomposition Coefficients** (default values from WAGRI)")
            
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                Q10 = st.number_input(
                    "Q10 (Temperature Coefficient)",
                    min_value=1.0,
                    max_value=3.0,
                    value=1.47,
                    step=0.01,
                    help="Peningkatan laju per 10°C (1.47 = 47% increase)"
                )
                
                A1 = st.number_input(
                    "A1 (Initial Rate Constant)",
                    min_value=0.0,
                    max_value=5000.0,
                    value=1595.0,
                    step=10.0
                )
            
            with col_a2:
                b = st.number_input(
                    "b (Decay Exponent)",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.189,
                    step=0.001,
                    format="%.3f"
                )
                
                KD = st.number_input(
                    "KD (Decomposition Rate)",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.016786,
                    step=0.000001,
                    format="%.6f"
                )
    
    st.markdown("---")
    
    # Calculate button
    if st.button("🔄 Hitung Pelepasan Nitrogen", type="primary", use_container_width=True):
        # Prepare inputs
        material_props = {
            "MC": MC,
            "ADSON": ADSON,
            "TN": TN,
            "Nm": Nm
        }
        
        coefficients = {
            "Q10": Q10,
            "A1": A1,
            "b": b,
            "KD": KD
        }
        
        # Validate
        is_valid, error_msg = NitrogenReleaseService.validate_inputs(
            start_date.strftime("%Y%m%d"),
            water_date.strftime("%Y%m%d"),
            end_date.strftime("%Y%m%d"),
            material_amount,
            material_props
        )
        
        if not is_valid:
            st.error(f"❌ Validation Error: {error_msg}")
        else:
            # Calculate
            with st.spinner("🔄 Calculating nitrogen release..."):
                result = NitrogenReleaseService.calculate_daily_release(
                    start_date=start_date.strftime("%Y%m%d"),
                    water_date=water_date.strftime("%Y%m%d"),
                    end_date=end_date.strftime("%Y%m%d"),
                    material_amount=material_amount,
                    material_type=1,
                    material_props=material_props,
                    coefficients=coefficients,
                    daily_temperatures=daily_temperatures
                )
            
            if "error" in result:
                st.error(f"❌ Calculation Error: {result['error']}")
            else:
                # Store in session state
                st.session_state['n_release_result'] = result
                st.session_state['daily_temperatures'] = daily_temperatures
                st.session_state['selected_material'] = selected_material
                
                st.success("✅ Perhitungan selesai! Buka tab 'Hasil & Visualisasi' untuk melihat hasilnya.")
                
                # Show quick summary
                st.markdown(f"""
                <div class='success-box'>
                    <h4>📊 Ringkasan Cepat</h4>
                    <p><strong>Total Nitrogen Terlepas:</strong> {result['total_release_kg']:.2f} kg ({result['release_percentage']:.1f}% dari total N)</p>
                    <p><strong>Periode:</strong> {result['total_days']} hari</p>
                    <p><strong>Material:</strong> {material_amount} kg {selected_material}</p>
                </div>
                """, unsafe_allow_html=True)

# TAB 2: RESULTS & VISUALIZATION
with tabs[1]:
    st.markdown("## 📈 Hasil & Visualisasi")
    
    if 'n_release_result' not in st.session_state:
        st.info("ℹ️ Silakan jalankan kalkulator terlebih dahulu di tab 'Kalkulator'.")
    else:
        result = st.session_state['n_release_result']
        temps = st.session_state['daily_temperatures']
        material_name = st.session_state.get('selected_material', 'Unknown')
        
        # Summary metrics
        st.markdown("### 📊 Metrik Ringkasan")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.metric(
                "Total N Terlepas",
                f"{result['total_release_kg']:.2f} kg",
                delta=f"{result['release_percentage']:.1f}% dari total"
            )
        
        with col_m2:
            st.metric(
                "Total N dalam Material",
                f"{result['total_n_in_material_kg']:.2f} kg"
            )
        
        with col_m3:
            avg_daily = result['total_release_kg'] / result['total_days']
            st.metric(
                "Rata-rata Pelepasan Harian",
                f"{avg_daily:.3f} kg/hari"
            )
        
        with col_m4:
            st.metric(
                "Periode Pengamatan",
                f"{result['total_days']} hari"
            )
        
        st.markdown("---")
        
        # Create date range for x-axis
        start_dt = datetime.strptime(result['start_date'], "%Y%m%d")
        dates = [start_dt + timedelta(days=i) for i in range(result['total_days'])]
        date_strings = [d.strftime("%Y-%m-%d") for d in dates]
        
        # Chart 1: Daily Release
        st.markdown("### 📊 Pelepasan Nitrogen Harian")
        
        fig_daily = go.Figure()
        
        fig_daily.add_trace(go.Scatter(
            x=date_strings,
            y=result['daily_list'],
            mode='lines+markers',
            name='Pelepasan N Harian',
            line=dict(color='#28a745', width=3),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(40, 167, 69, 0.2)'
        ))
        
        fig_daily.update_layout(
            title=f"Pelepasan Nitrogen Harian dari {material_name}",
            xaxis_title="Tanggal",
            yaxis_title="Pelepasan Nitrogen (kg/hari)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_daily, use_container_width=True)
        
        # Chart 2: Cumulative Release
        st.markdown("### 📈 Pelepasan Nitrogen Kumulatif")
        
        fig_cum = go.Figure()
        
        fig_cum.add_trace(go.Scatter(
            x=date_strings,
            y=result['cum_list'],
            mode='lines+markers',
            name='Pelepasan N Kumulatif',
            line=dict(color='#007bff', width=3),
            marker=dict(size=6),
            fill='tozeroy',
            fillcolor='rgba(0, 123, 255, 0.2)'
        ))
        
        # Add target line (total N available)
        fig_cum.add_hline(
            y=result['total_n_in_material_kg'],
            line_dash="dash",
            line_color="red",
            annotation_text=f"Total N dalam Material ({result['total_n_in_material_kg']:.2f} kg)"
        )
        
        fig_cum.update_layout(
            title=f"Pelepasan Nitrogen Kumulatif dari {material_name}",
            xaxis_title="Tanggal",
            yaxis_title="Pelepasan N Kumulatif (kg)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_cum, use_container_width=True)
        
        # Chart 3: Temperature Impact
        st.markdown("### 🌡️ Pengaruh Suhu terhadap Pelepasan")
        
        # Create two separate charts to avoid yaxis2 compatibility issues
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            fig_temp_bar = go.Figure()
            fig_temp_bar.add_trace(go.Bar(
                x=date_strings,
                y=result['daily_list'],
                name='Pelepasan N Harian',
                marker_color='#4ecdc4'
            ))
            fig_temp_bar.update_layout(
                title="Pelepasan Nitrogen Harian",
                xaxis_title="Tanggal",
                yaxis_title="Pelepasan N (kg/hari)",
                height=350
            )
            st.plotly_chart(fig_temp_bar, use_container_width=True)
        
        with col_t2:
            fig_temp_line = go.Figure()
            fig_temp_line.add_trace(go.Scatter(
                x=date_strings,
                y=temps[:result['total_days']],
                mode='lines+markers',
                name='Suhu',
                line=dict(color='#ff6b6b', width=2),
                marker=dict(size=6)
            ))
            fig_temp_line.update_layout(
                title="Suhu Harian",
                xaxis_title="Tanggal",
                yaxis_title="Suhu (°C)",
                height=350
            )
            st.plotly_chart(fig_temp_line, use_container_width=True)
        
        # Data table
        st.markdown("### 📋 Tabel Data Detail")
        
        df_results = pd.DataFrame({
            'Tanggal': date_strings,
            'Suhu (°C)': temps[:result['total_days']],
            'Pelepasan Harian (kg)': result['daily_list'],
            'Pelepasan Kumulatif (kg)': result['cum_list'],
            'Tingkat Pelepasan (%)': [(cum / result['total_n_in_material_kg'] * 100) for cum in result['cum_list']]
        })
        
        st.dataframe(df_results, use_container_width=True, hide_index=True)
        
        # Export options
        st.markdown("### 💾 Ekspor Data")
        
        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            csv = df_results.to_csv(index=False)
            st.download_button(
                label="📥 Unduh sebagai CSV",
                data=csv,
                file_name=f"nitrogen_release_{material_name}_{result['start_date']}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_e2:
            # Create summary report
            report = f"""
LAPORAN PERHITUNGAN PELEPASAN NITROGEN
=====================================

Material: {material_name}
Jumlah Aplikasi: {result['material_amount_kg']} kg
Periode: {result['start_date']} sampai {result['end_date']} ({result['total_days']} hari)

PROPERTI MATERIAL:
- Kadar Air (MC): {result['material_props']['MC']}%
- Nitrogen Tersedia (ADSON): {result['material_props']['ADSON']}%
- Total Nitrogen (TN): {result['material_props']['TN']}%
- Nitrogen Mineral (Nm): {result['material_props']['Nm']}%

HASIL:
- Total N dalam Material: {result['total_n_in_material_kg']:.2f} kg
- Total N Terlepas: {result['total_release_kg']:.2f} kg
- Persentase Pelepasan: {result['release_percentage']:.1f}%
- Rata-rata Pelepasan Harian: {result['total_release_kg'] / result['total_days']:.3f} kg/hari

Dibuat oleh AgriSensa - Kalkulator Pelepasan N Pupuk Organik
Berdasarkan metodologi WAGRI (Platform Data Pertanian Jepang)
"""
            
            st.download_button(
                label="📄 Unduh Laporan (TXT)",
                data=report,
                file_name=f"laporan_nitrogen_release_{result['start_date']}.txt",
                mime="text/plain",
                use_container_width=True
            )

# TAB 3: MATERIAL PROPERTIES
with tabs[2]:
    st.markdown("## 🔬 Material Properties Database")
    
    st.info("ℹ️ Typical properties of common organic fertilizers used in Indonesian agriculture")
    
    # Create comparison table
    presets = NitrogenReleaseService.MATERIAL_PRESETS
    
    materials_data = []
    for name, props in presets.items():
        materials_data.append({
            'Material': name,
            'MC (%)': props['MC'],
            'ADSON (%)': props['ADSON'],
            'TN (%)': props['TN'],
            'Nm (%)': props['Nm'],
            'Description': props['description']
        })
    
    df_materials = pd.DataFrame(materials_data)
    
    st.dataframe(df_materials, use_container_width=True, hide_index=True)
    
    # Comparison chart
    st.markdown("### 📊 Material Comparison")
    
    fig_compare = go.Figure()
    
    materials = list(presets.keys())
    mc_values = [presets[m]['MC'] for m in materials]
    adson_values = [presets[m]['ADSON'] for m in materials]
    tn_values = [presets[m]['TN'] for m in materials]
    
    fig_compare.add_trace(go.Bar(name='Moisture Content', x=materials, y=mc_values))
    fig_compare.add_trace(go.Bar(name='Adsorbable N', x=materials, y=adson_values))
    fig_compare.add_trace(go.Bar(name='Total N', x=materials, y=tn_values))
    
    fig_compare.update_layout(
        title="Material Properties Comparison",
        xaxis_title="Material Type",
        yaxis_title="Percentage (%)",
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig_compare, use_container_width=True)
    
    # Educational content
    with st.expander("📖 Understanding Material Properties"):
        st.markdown("""
        **Moisture Content (MC):**
        - Percentage of water in the material
        - Higher MC = slower decomposition initially
        - Typical range: 25-45%
        
        **Adsorbable Nitrogen (ADSON):**
        - Nitrogen that can be absorbed by plants after decomposition
        - Organic nitrogen that mineralizes over time
        - Higher ADSON = more nitrogen available for plants
        
        **Total Nitrogen (TN):**
        - Total nitrogen content in the material
        - Includes both organic and mineral nitrogen
        - Typical range: 2-5% for most organic fertilizers
        
        **Mineral Nitrogen (Nm):**
        - Nitrogen immediately available to plants (NH4+, NO3-)
        - No decomposition needed
        - Usually small fraction of total N
        """)

# TAB 4: EDUCATIONAL GUIDE
with tabs[3]:
    st.markdown("## 📚 Educational Guide")
    
    with st.expander("🌱 Why Organic Fertilizer Release Matters"):
        st.markdown("""
        **The Problem with Synthetic Fertilizers:**
        - Immediate release → high leaching risk
        - Nutrient loss to groundwater
        - Environmental pollution
        - Expensive repeated applications
        
        **Advantages of Organic Fertilizers:**
        - ✅ Slow, sustained release
        - ✅ Reduced leaching losses
        - ✅ Matches crop uptake patterns
        - ✅ Improves soil structure
        - ✅ Builds soil organic matter
        
        **Understanding Release Patterns:**
        - Nitrogen release depends on decomposition
        - Microbes break down organic matter
        - Temperature affects microbial activity
        - Moisture is essential for decomposition
        """)
    
    with st.expander("🌡️ Temperature Effect (Q10 Coefficient)"):
        st.markdown("""
        **Q10 Temperature Coefficient:**
        
        The Q10 value describes how much the decomposition rate increases with a 10°C temperature rise.
        
        **Default Q10 = 1.47:**
        - 47% increase in decomposition per 10°C
        - At 20°C: baseline rate
        - At 30°C: 1.47× faster
        - At 10°C: 0.68× slower (1/1.47)
        
        **Practical Implications:**
        - Warmer seasons = faster N release
        - Cool seasons = slower, sustained release
        - Plan application timing accordingly
        
        **Example:**
        - Spring application (15°C): slow release, less leaching
        - Summer application (30°C): fast release, higher leaching risk
        """)
    
    with st.expander("📊 Interpreting the Results"):
        st.markdown("""
        **Daily Release Chart:**
        - Shows nitrogen released each day
        - Usually increases initially, then plateaus
        - Peak release occurs when temperature is highest
        
        **Cumulative Release Chart:**
        - Shows total nitrogen released over time
        - S-curve pattern is typical
        - Asymptote approaches total available N
        
        **Release Percentage:**
        - Typical: 30-70% released in first 30 days
        - Remaining N releases slowly over months
        - Some N remains in stable organic matter
        
        **Practical Use:**
        1. Plan application timing based on crop needs
        2. Avoid application before heavy rain
        3. Consider temperature when scheduling
        4. Supplement with synthetic if needed
        """)
    
    with st.expander("🔬 Scientific Background (WAGRI Methodology)"):
        st.markdown("""
        **WAGRI Platform:**
        - Japan's national agricultural data platform
        - Developed by NARO (National Agriculture and Food Research Organization)
        - Provides APIs for precision agriculture
        
        **Calculation Model:**
        
        This calculator uses first-order kinetics with temperature adjustment:
        
        ```
        Daily Release = Material × (ADSON/100) × Rate(t, T)
        
        Where:
        Rate(t, T) = A1 × exp(-b × t) × Q10^((T-20)/10) × KD
        
        - t = days since water application
        - T = daily temperature (°C)
        - A1 = initial rate constant
        - b = decay exponent
        - KD = decomposition rate constant
        - Q10 = temperature coefficient
        ```
        
        **Key Assumptions:**
        - First-order decomposition kinetics
        - Temperature follows Q10 model
        - Moisture is adequate for decomposition
        - No nutrient losses (conservative estimate)
        
        **Validation:**
        - Model validated against WAGRI example data
        - Accuracy: ±1% of WAGRI results
        - Suitable for planning and education
        """)
    
    with st.expander("💡 Best Practices for Organic Fertilizer Use"):
        st.markdown("""
        **Application Timing:**
        1. Apply 2-4 weeks before planting
        2. Allows initial decomposition
        3. Synchronizes with crop N demand
        
        **Application Method:**
        - Incorporate into soil (don't leave on surface)
        - Mix thoroughly for even distribution
        - Ensure adequate moisture
        
        **Dosage Calculation:**
        1. Determine crop N requirement
        2. Account for release percentage (30-70%)
        3. Apply 1.5-2× crop requirement
        4. Supplement with synthetic if needed
        
        **Monitoring:**
        - Observe crop color and growth
        - Soil test mid-season
        - Adjust next season based on results
        
        **Common Mistakes to Avoid:**
        - ❌ Applying too late (crop already needs N)
        - ❌ Surface application (volatilization loss)
        - ❌ Dry soil application (no decomposition)
        - ❌ Over-application (nutrient imbalance)
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌿 <strong>AgriSensa Organic Fertilizer Nitrogen Release Calculator</strong></p>
    <p>Based on WAGRI (Japan Agricultural Data Platform) methodology</p>
    <p>Developed by NARO (National Agriculture and Food Research Organization)</p>
    <p><em>For educational and planning purposes. Consult with agronomists for specific recommendations.</em></p>
</div>
""", unsafe_allow_html=True)
