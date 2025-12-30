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

from agrisensa_commodities.services.phosphorus_release_service import PhosphorusReleaseService

# Page config
st.set_page_config(
    page_title="Kalkulator Pelepasan Fosfor Pupuk Organik",
    page_icon="🔶",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-box {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #f5576c;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🔶 Kalkulator Pelepasan Fosfor (P) Pupuk Organik")
st.markdown("""
<div class='info-box'>
    <h3>🔬 Kalkulator Ilmiah Berbasis WAGRI</h3>
    <p>Pahami ketersediaan Fosfor (P) dari pupuk organik untuk tanaman!</p>
    <ul>
        <li>✅ <strong>Langsung Tersedia</strong> - P tidak perlu dekomposisi seperti N</li>
        <li>✅ <strong>Nilai Konstan</strong> - Tidak dipengaruhi suhu atau waktu</li>
        <li>✅ <strong>6 Preset Pupuk</strong> - Pupuk kandang & kompos Indonesia</li>
        <li>✅ <strong>Perbandingan dengan Kimia</strong> - SP-36, TSP, DSP</li>
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
            value=datetime(2024, 5, 1),
            help="Tanggal mulai pengamatan"
        )
        
        end_date = st.date_input(
            "Tanggal Akhir",
            value=datetime(2024, 7, 31),
            help="Tanggal akhir pengamatan (P tersedia konstan)"
        )
        
        total_days_preview = (end_date - start_date).days + 1
        st.info(f"📝 Periode: {total_days_preview} hari")
    
    with col2:
        st.markdown("### 🌾 Material Selection")
        
        material_presets = PhosphorusReleaseService.list_material_presets()
        material_presets.append("Custom")
        
        selected_material = st.selectbox(
            "Pilih Material Organik",
            material_presets,
            help="Pilih jenis pupuk organik atau Custom untuk input manual"
        )
        
        if selected_material != "Custom":
            preset = PhosphorusReleaseService.get_material_preset(selected_material)
            st.info(f"ℹ️ {preset['description']}")
            
            MC = preset["MC"]
            TP = preset["TP"]
            
            # Show preset values
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.metric("Kadar Air (MC)", f"{MC}%")
            with col_p2:
                st.metric("Total Fosfor (TP)", f"{TP}%")
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
            
            with col_c2:
                TP = st.number_input(
                    "Total Phosphorus (TP) %",
                    min_value=0.0,
                    max_value=10.0,
                    value=2.0,
                    step=0.1,
                    help="Total fosfor dalam material"
                )
        
        st.markdown("### 📦 Jumlah Aplikasi")
        
        material_amount = st.number_input(
            "Jumlah Material (kg)",
            min_value=1.0,
            max_value=10000.0,
            value=100.0,
            step=10.0,
            help="Jumlah pupuk organik yang diaplikasikan"
        )
        
        # Advanced settings
        with st.expander("⚙️ Koefisien Lanjutan"):
            st.markdown("**Koefisien Efisiensi** (nilai default dari WAGRI)")
            
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                FE_P = st.number_input(
                    "FE_P (Fertilizer Efficiency) %",
                    min_value=0.0,
                    max_value=100.0,
                    value=70.0,
                    step=1.0,
                    help="Efisiensi pupuk P (% yang bisa diserap tanaman)"
                )
            
            with col_a2:
                Region_PK = st.number_input(
                    "Region_PK (Regional Coefficient)",
                    min_value=0.0,
                    max_value=2.0,
                    value=1.0,
                    step=0.1,
                    help="Koefisien regional (Indonesia = 1.0)"
                )
    
    st.markdown("---")
    
    # Calculate button
    if st.button("🔄 Hitung Ketersediaan Fosfor", type="primary", use_container_width=True):
        # Prepare inputs
        material_props = {
            "MC": MC,
            "TP": TP
        }
        
        coefficients = {
            "FE_P": FE_P,
            "Region_PK": Region_PK
        }
        
        # Validate
        is_valid, error_msg = PhosphorusReleaseService.validate_inputs(
            start_date.strftime("%Y%m%d"),
            end_date.strftime("%Y%m%d"),
            material_amount,
            material_props
        )
        
        if not is_valid:
            st.error(f"❌ Validation Error: {error_msg}")
        else:
            # Calculate
            with st.spinner("🔄 Menghitung ketersediaan fosfor..."):
                result = PhosphorusReleaseService.calculate_p_release(
                    start_date=start_date.strftime("%Y%m%d"),
                    end_date=end_date.strftime("%Y%m%d"),
                    material_amount=material_amount,
                    material_type=1,
                    material_props=material_props,
                    coefficients=coefficients
                )
            
            if "error" in result:
                st.error(f"❌ Calculation Error: {result['error']}")
            else:
                # Store in session state
                st.session_state['p_release_result'] = result
                st.session_state['selected_material_p'] = selected_material
                
                st.success("✅ Perhitungan selesai! Buka tab 'Hasil & Visualisasi' untuk melihat hasilnya.")
                
                # Show quick summary
                p2o5_available = PhosphorusReleaseService.convert_p_to_p2o5(result['available_p'])
                
                st.markdown(f"""
                <div class='success-box'>
                    <h4>📊 Ringkasan Cepat</h4>
                    <p><strong>Total P dalam Material:</strong> {result['total_p_in_material']:.2f} kg</p>
                    <p><strong>P Tersedia untuk Tanaman:</strong> {result['available_p']:.2f} kg ({result['availability_percentage']:.1f}%)</p>
                    <p><strong>Setara P2O5:</strong> {p2o5_available:.2f} kg</p>
                    <p><strong>Periode:</strong> {result['total_days']} hari (nilai konstan)</p>
                    <p><strong>Material:</strong> {material_amount} kg {selected_material}</p>
                </div>
                """, unsafe_allow_html=True)

# TAB 2: RESULTS & VISUALIZATION
with tabs[1]:
    st.markdown("## 📈 Hasil & Visualisasi")
    
    if 'p_release_result' not in st.session_state:
        st.info("ℹ️ Silakan jalankan kalkulator terlebih dahulu di tab 'Kalkulator'.")
    else:
        result = st.session_state['p_release_result']
        material_name = st.session_state.get('selected_material_p', 'Unknown')
        
        # Summary metrics
        st.markdown("### 📊 Metrik Ringkasan")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        
        with col_m1:
            st.metric(
                "Total P dalam Material",
                f"{result['total_p_in_material']:.2f} kg"
            )
        
        with col_m2:
            st.metric(
                "P Tersedia",
                f"{result['available_p']:.2f} kg",
                delta=f"{result['availability_percentage']:.1f}% dari total"
            )
        
        with col_m3:
            p2o5 = PhosphorusReleaseService.convert_p_to_p2o5(result['available_p'])
            st.metric(
                "Setara P2O5",
                f"{p2o5:.2f} kg"
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
        
        # Chart 1: Constant Availability
        st.markdown("### 📊 Ketersediaan Fosfor (Konstan)")
        
        st.info("💡 **Catatan Penting:** Berbeda dengan Nitrogen, Fosfor langsung tersedia dan tidak berubah seiring waktu. Nilai tetap konstan dari awal hingga akhir periode.")
        
        fig_const = go.Figure()
        
        fig_const.add_trace(go.Scatter(
            x=date_strings,
            y=result['cum_list'],
            mode='lines',
            name='P Tersedia',
            line=dict(color='#f5576c', width=3),
            fill='tozeroy',
            fillcolor='rgba(245, 87, 108, 0.2)'
        ))
        
        fig_const.update_layout(
            title=f"Ketersediaan Fosfor dari {material_name} (Konstan)",
            xaxis_title="Tanggal",
            yaxis_title="Fosfor Tersedia (kg)",
            hovermode='x unified',
            height=400
        )
        
        st.plotly_chart(fig_const, use_container_width=True)
        
        # Chart 2: Comparison with Synthetic
        st.markdown("### ⚖️ Perbandingan dengan Pupuk Kimia")
        
        col_syn1, col_syn2 = st.columns(2)
        
        with col_syn1:
            synthetic_type = st.selectbox(
                "Pilih Jenis Pupuk Kimia",
                ["SP-36", "TSP", "DSP", "MKP", "NPK 15-15-15", "UltraDAP"],
                help="Pilih pupuk kimia untuk perbandingan"
            )
        
        comparison = PhosphorusReleaseService.compare_with_synthetic(
            organic_p=result['available_p'],
            synthetic_type=synthetic_type
        )
        
        with col_syn2:
            st.metric(
                f"Setara {synthetic_type}",
                f"{comparison['synthetic_needed_kg']:.2f} kg"
            )
        
        # Comparison bar chart
        fig_compare = go.Figure()
        
        fig_compare.add_trace(go.Bar(
            name='Pupuk Organik',
            x=['P2O5 Tersedia'],
            y=[comparison['organic_p2o5']],
            marker_color='#f5576c',
            text=[f"{comparison['organic_p2o5']:.2f} kg"],
            textposition='auto'
        ))
        
        fig_compare.add_trace(go.Bar(
            name=f'{synthetic_type} (setara)',
            x=['P2O5 Tersedia'],
            y=[comparison['organic_p2o5']],
            marker_color='#4ecdc4',
            text=[f"{comparison['synthetic_needed_kg']:.2f} kg {synthetic_type}"],
            textposition='auto'
        ))
        
        fig_compare.update_layout(
            title=f"Perbandingan Pupuk Organik vs {synthetic_type}",
            yaxis_title="P2O5 (kg)",
            barmode='group',
            height=350
        )
        
        st.plotly_chart(fig_compare, use_container_width=True)
        
        # Show fertilizer info
        st.info(f"ℹ️ **{synthetic_type}:** {comparison['fertilizer_info']}")
        
        st.success(f"✅ {comparison['advantage']}")
        
        # Data table
        st.markdown("### 📋 Tabel Data Detail")
        
        df_results = pd.DataFrame({
            'Tanggal': date_strings,
            'P Tersedia (kg)': result['cum_list'],
            'P2O5 Setara (kg)': [PhosphorusReleaseService.convert_p_to_p2o5(p) for p in result['cum_list']]
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
                file_name=f"phosphorus_availability_{material_name}_{result['start_date']}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_e2:
            # Create summary report
            report = f"""
LAPORAN KETERSEDIAAN FOSFOR (P)
=====================================

Material: {material_name}
Jumlah Aplikasi: {result['material_amount_kg']} kg
Periode: {result['start_date']} sampai {result['end_date']} ({result['total_days']} hari)

PROPERTI MATERIAL:
- Kadar Air (MC): {result['material_props']['MC']}%
- Total Fosfor (TP): {result['material_props']['TP']}%

KOEFISIEN:
- FE_P (Efisiensi Pupuk): {result['coefficients']['FE_P']}%
- Region_PK: {result['coefficients']['Region_PK']}

HASIL:
- Total P dalam Material: {result['total_p_in_material']:.2f} kg
- P Tersedia untuk Tanaman: {result['available_p']:.2f} kg
- Persentase Ketersediaan: {result['availability_percentage']:.1f}%
- Setara P2O5: {PhosphorusReleaseService.convert_p_to_p2o5(result['available_p']):.2f} kg

CATATAN PENTING:
- Fosfor langsung tersedia (tidak perlu dekomposisi seperti Nitrogen)
- Nilai konstan sepanjang periode (tidak dipengaruhi suhu)
- Aplikasikan dekat akar karena P tidak mobile di tanah

Dibuat oleh AgriSensa - Kalkulator Pelepasan Fosfor Pupuk Organik
Berdasarkan metodologi WAGRI (Platform Data Pertanian Jepang)
"""
            
            st.download_button(
                label="📄 Unduh Laporan (TXT)",
                data=report,
                file_name=f"laporan_phosphorus_{result['start_date']}.txt",
                mime="text/plain",
                use_container_width=True
            )

# TAB 3: MATERIAL PROPERTIES
with tabs[2]:
    st.markdown("## 🔬 Properti Material Database")
    
    st.info("ℹ️ Properti tipikal pupuk organik yang umum digunakan di Indonesia")
    
    # Create comparison table
    presets = PhosphorusReleaseService.MATERIAL_PRESETS
    
    materials_data = []
    for name, props in presets.items():
        materials_data.append({
            'Material': name,
            'MC (%)': props['MC'],
            'TP (%)': props['TP'],
            'Deskripsi': props['description']
        })
    
    df_materials = pd.DataFrame(materials_data)
    
    st.dataframe(df_materials, use_container_width=True, hide_index=True)
    
    # Comparison chart
    st.markdown("### 📊 Perbandingan Kandungan Fosfor")
    
    fig_compare_mat = go.Figure()
    
    materials = list(presets.keys())
    tp_values = [presets[m]['TP'] for m in materials]
    
    fig_compare_mat.add_trace(go.Bar(
        x=materials,
        y=tp_values,
        marker_color='#f5576c',
        text=[f"{tp}%" for tp in tp_values],
        textposition='auto'
    ))
    
    fig_compare_mat.update_layout(
        title="Kandungan Total Fosfor (TP) per Material",
        xaxis_title="Jenis Material",
        yaxis_title="Total Fosfor (%)",
        height=500
    )
    
    st.plotly_chart(fig_compare_mat, use_container_width=True)
    
    # Educational content
    with st.expander("📖 Memahami Properti Material"):
        st.markdown("""
        **Moisture Content (MC) - Kadar Air:**
        - Persentase air dalam material
        - Rentang tipikal: 25-45%
        - MC tinggi = material lebih basah
        - Tidak mempengaruhi ketersediaan P (berbeda dengan N)
        
        **Total Phosphorus (TP) - Total Fosfor:**
        - Total kandungan fosfor dalam material
        - Rentang tipikal: 0.8-3.5%
        - TP tinggi = lebih banyak P tersedia
        - Pupuk kandang ayam memiliki TP tertinggi (3.5%)
        
        **Perbedaan dengan Nitrogen:**
        - P tidak perlu dekomposisi (langsung tersedia)
        - P tidak dipengaruhi suhu atau waktu
        - P tidak mobile di tanah (tidak tercuci hujan)
        - P lebih stabil dalam jangka panjang
        """)

# Continue in next message due to length...
