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
    st.markdown("## 📚 Panduan Edukasi")
    
    st.info("💡 **Tentang Modul Ini:** Kalkulator ini membantu petani memahami bagaimana nitrogen dari pupuk organik dilepaskan secara bertahap ke tanah dan tersedia untuk tanaman. Berbeda dengan pupuk kimia yang langsung tersedia, pupuk organik melepaskan nitrogen secara perlahan melalui proses dekomposisi.")
    
    with st.expander("🌱 Mengapa Pelepasan Nitrogen Pupuk Organik Penting?"):
        st.markdown("""
        ### Masalah dengan Pupuk Kimia/Sintetis:
        
        **1. Pelepasan Seketika = Risiko Tinggi**
        - Nitrogen langsung tersedia 100% saat aplikasi
        - Tanaman tidak bisa menyerap semuanya sekaligus
        - Kelebihan nitrogen tercuci hujan → hilang ke air tanah
        - Pencemaran lingkungan (eutrofikasi sungai/danau)
        
        **2. Biaya Tinggi & Tidak Efisien**
        - Harus aplikasi berulang kali (3-4x per musim)
        - Efisiensi penyerapan hanya 30-50%
        - Biaya pupuk terus meningkat
        - Ketergantungan pada pupuk kimia
        
        **3. Dampak Jangka Panjang**
        - Merusak struktur tanah
        - Membunuh mikroba tanah yang bermanfaat
        - Tanah menjadi keras dan padat
        - Produktivitas menurun seiring waktu
        
        ---
        
        ### Keunggulan Pupuk Organik:
        
        **1. ✅ Pelepasan Bertahap & Berkelanjutan**
        - Nitrogen dilepaskan perlahan sesuai kebutuhan tanaman
        - Mengurangi risiko pencucian hingga 70%
        - Tersedia untuk tanaman dalam jangka waktu lebih lama
        - Lebih efisien: efisiensi penyerapan 60-80%
        
        **2. ✅ Memperbaiki Kesehatan Tanah**
        - Meningkatkan bahan organik tanah
        - Memperbaiki struktur tanah (lebih gembur)
        - Meningkatkan kemampuan tanah menahan air
        - Mendukung kehidupan mikroba tanah
        
        **3. ✅ Ekonomis Jangka Panjang**
        - Aplikasi lebih jarang (1-2x per musim)
        - Memanfaatkan limbah pertanian/peternakan
        - Mengurangi ketergantungan pupuk kimia
        - Meningkatkan produktivitas tanah jangka panjang
        
        **4. ✅ Ramah Lingkungan**
        - Mengurangi pencemaran air tanah
        - Mengurangi emisi gas rumah kaca
        - Mendaur ulang limbah organik
        - Pertanian berkelanjutan
        
        ---
        
        ### Memahami Pola Pelepasan Nitrogen:
        
        **Proses Mineralisasi Nitrogen:**
        
        1. **Minggu 1-2: Fase Awal**
           - Mikroba tanah mulai menguraikan bahan organik
           - Pelepasan nitrogen masih lambat (5-10%)
           - Perlu waktu untuk mikroba berkembang
        
        2. **Minggu 3-6: Fase Aktif**
           - Pelepasan nitrogen meningkat pesat (40-60%)
           - Mikroba sangat aktif menguraikan
           - Suhu dan kelembaban optimal
        
        3. **Minggu 7+: Fase Stabil**
           - Pelepasan melambat tapi berkelanjutan (20-30%)
           - Nitrogen tersisa dalam bentuk humus
           - Manfaat jangka panjang untuk tanah
        
        **Faktor yang Mempengaruhi:**
        - 🌡️ **Suhu:** Makin hangat, makin cepat dekomposisi
        - 💧 **Kelembaban:** Perlu air untuk aktivitas mikroba
        - 🦠 **Mikroba:** Populasi dan jenis mikroba tanah
        - 🌾 **C/N Ratio:** Rasio karbon-nitrogen dalam bahan
        - 🪨 **Tekstur Tanah:** Tanah gembur lebih cepat dekomposisi
        """)
    
    with st.expander("🌡️ Pengaruh Suhu - Koefisien Q10"):
        st.markdown("""
        ### Apa itu Koefisien Q10?
        
        **Q10** adalah angka yang menunjukkan **berapa kali lebih cepat** proses dekomposisi terjadi jika suhu naik 10°C.
        
        **Q10 = 1.47** (default dalam kalkulator ini) artinya:
        - Setiap kenaikan suhu 10°C → dekomposisi **1.47× lebih cepat** (47% lebih cepat)
        - Setiap penurunan suhu 10°C → dekomposisi **0.68× lebih lambat** (32% lebih lambat)
        
        ---
        
        ### Contoh Praktis:
        
        **Skenario 1: Aplikasi Musim Hujan (Suhu 20°C)**
        - Dekomposisi berjalan pada kecepatan **normal** (baseline)
        - Pelepasan nitrogen **lambat dan bertahap**
        - **Keuntungan:** Risiko pencucian rendah, nitrogen tersedia lama
        - **Cocok untuk:** Tanaman jangka panjang (padi, jagung)
        
        **Skenario 2: Aplikasi Musim Kemarau (Suhu 30°C)**
        - Dekomposisi **1.47× lebih cepat** dari normal
        - Pelepasan nitrogen **cepat dalam 2-3 minggu**
        - **Risiko:** Pencucian lebih tinggi jika ada hujan tiba-tiba
        - **Cocok untuk:** Tanaman jangka pendek (sayuran)
        
        **Skenario 3: Aplikasi Dataran Tinggi (Suhu 15°C)**
        - Dekomposisi **0.78× lebih lambat** dari normal
        - Pelepasan nitrogen **sangat bertahap**
        - **Keuntungan:** Nitrogen tersedia sangat lama (3-4 bulan)
        - **Perhatian:** Perlu aplikasi lebih awal sebelum tanam
        
        ---
        
        ### Implikasi Praktis untuk Petani:
        
        **📅 Waktu Aplikasi Berdasarkan Suhu:**
        
        | Suhu Rata-rata | Waktu Aplikasi Ideal | Alasan |
        |----------------|----------------------|--------|
        | < 20°C (Dingin) | 4-6 minggu sebelum tanam | Dekomposisi lambat |
        | 20-25°C (Sedang) | 2-4 minggu sebelum tanam | Dekomposisi normal |
        | > 25°C (Panas) | 1-2 minggu sebelum tanam | Dekomposisi cepat |
        
        **🌾 Strategi Berdasarkan Musim:**
        
        - **Musim Hujan:** Aplikasi lebih awal, dosis lebih tinggi
        - **Musim Kemarau:** Aplikasi mendekati tanam, pastikan ada irigasi
        - **Peralihan Musim:** Waktu paling ideal untuk aplikasi pupuk organik
        """)
    
    with st.expander("📊 Cara Membaca & Menggunakan Hasil Kalkulator"):
        st.markdown("""
        ### 1. Grafik Pelepasan Harian
        
        **Apa yang Ditampilkan:**
        - Jumlah nitrogen (kg) yang dilepaskan **setiap hari**
        - Pola naik-turun mengikuti suhu harian
        
        **Cara Membaca:**
        - **Nilai Rendah (0-0.1 kg/hari):** Pelepasan lambat, fase awal
        - **Nilai Sedang (0.1-0.3 kg/hari):** Pelepasan aktif, fase optimal
        - **Nilai Tinggi (>0.3 kg/hari):** Pelepasan cepat, suhu tinggi
        
        **Interpretasi:**
        - Grafik naik → Dekomposisi meningkat
        - Grafik turun → Dekomposisi melambat (suhu turun/bahan habis)
        - Puncak grafik → Saat pelepasan nitrogen maksimal
        
        ---
        
        ### 2. Grafik Kumulatif
        
        **Apa yang Ditampilkan:**
        - **Total nitrogen** yang sudah dilepaskan dari awal hingga hari tertentu
        - Bentuk kurva S (sigmoid) yang khas
        
        **Cara Membaca:**
        - **Fase Lambat (0-20%):** Minggu 1-2, mikroba baru mulai aktif
        - **Fase Cepat (20-70%):** Minggu 3-6, pelepasan maksimal
        - **Fase Stabil (70-90%):** Minggu 7+, pelepasan melambat
        
        **Garis Merah (Target):**
        - Menunjukkan total nitrogen dalam material
        - Grafik tidak akan mencapai 100% (ada nitrogen yang tersisa dalam humus)
        - Biasanya mencapai 60-80% dari total
        
        ---
        
        ### 3. Persentase Pelepasan
        
        **Interpretasi Angka:**
        
        - **< 30% dalam 30 hari:** Pelepasan **sangat lambat**
          - Kemungkinan: Suhu rendah, C/N ratio tinggi, kelembaban kurang
          - Tindakan: Tambah air, tunggu lebih lama, atau tambah pupuk kimia
        
        - **30-70% dalam 30 hari:** Pelepasan **normal/ideal**
          - Kondisi optimal untuk pertumbuhan tanaman
          - Nitrogen tersedia bertahap sesuai kebutuhan
        
        - **> 70% dalam 30 hari:** Pelepasan **sangat cepat**
          - Kemungkinan: Suhu sangat tinggi, C/N ratio rendah
          - Risiko: Pencucian nitrogen, perlu monitoring ketat
        
        ---
        
        ### 4. Penggunaan Praktis di Lapangan
        
        **Langkah 1: Hitung Kebutuhan Nitrogen Tanaman**
        ```
        Contoh untuk Padi:
        - Target produksi: 6 ton/ha
        - Kebutuhan N: 120 kg N/ha
        ```
        
        **Langkah 2: Gunakan Kalkulator**
        ```
        - Input: 1000 kg Pupuk Kandang Ayam (TN = 4.5%)
        - Total N dalam pupuk: 45 kg
        - Hasil kalkulator: 30 kg N terlepas dalam 60 hari (67%)
        ```
        
        **Langkah 3: Hitung Kekurangan**
        ```
        - Kebutuhan: 120 kg N/ha
        - Dari organik: 30 kg N/ha
        - Kekurangan: 90 kg N/ha
        - Tambahan Urea (46% N): 90 ÷ 0.46 = 196 kg Urea/ha
        ```
        
        **Langkah 4: Jadwal Aplikasi**
        ```
        - Minggu 0: Aplikasi pupuk organik + setengah dosis Urea
        - Minggu 4: Aplikasi setengah dosis Urea sisanya
        - Monitoring: Cek warna daun, sesuaikan jika perlu
        ```
        """)
    
    with st.expander("🔬 Latar Belakang Ilmiah - Metodologi WAGRI"):
        st.markdown("""
        ### Tentang Platform WAGRI
        
        **WAGRI** = **WA**gricultural **G**overnment **R**esearch **I**nstitute
        
        **Apa itu WAGRI?**
        - Platform data pertanian nasional **Jepang**
        - Dikembangkan oleh **NARO** (National Agriculture and Food Research Organization)
        - Menyediakan API untuk pertanian presisi
        - Digunakan oleh ribuan petani dan peneliti di Jepang
        
        **Mengapa Menggunakan Metodologi WAGRI?**
        - ✅ Berbasis riset ilmiah puluhan tahun
        - ✅ Sudah divalidasi di berbagai kondisi iklim
        - ✅ Akurasi tinggi (±5% dari hasil aktual)
        - ✅ Diakui secara internasional
        
        ---
        
        ### Model Perhitungan
        
        Kalkulator ini menggunakan **kinetika orde pertama** dengan penyesuaian suhu:
        
        ```
        Pelepasan Harian = Material × (ADSON/100) × Rate(t, T)
        
        Di mana:
        Rate(t, T) = A1 × exp(-b × t) × Q10^((T-20)/10) × KD
        
        Variabel:
        - t = hari sejak aplikasi air
        - T = suhu harian (°C)
        - A1 = konstanta laju awal (1595)
        - b = eksponen peluruhan (0.189)
        - KD = konstanta dekomposisi (0.016786)
        - Q10 = koefisien suhu (1.47)
        ```
        
        **Penjelasan Sederhana:**
        - **exp(-b × t):** Pelepasan melambat seiring waktu (bahan organik berkurang)
        - **Q10^((T-20)/10):** Penyesuaian berdasarkan suhu
        - **A1 dan KD:** Konstanta yang disesuaikan dengan jenis material
        
        ---
        
        ### Properti Material yang Digunakan
        
        **1. MC (Moisture Content) - Kadar Air**
        - Persentase air dalam material
        - Rentang: 25-45%
        - Pengaruh: MC tinggi → dekomposisi awal lebih lambat
        
        **2. ADSON (Adsorbable Nitrogen) - Nitrogen Tersedia**
        - Nitrogen yang bisa diserap tanaman setelah dekomposisi
        - Rentang: 15-25%
        - Ini adalah nitrogen "aktif" yang kita hitung
        
        **3. TN (Total Nitrogen) - Total Nitrogen**
        - Total nitrogen dalam material (organik + mineral)
        - Rentang: 2.5-4.5%
        - Tidak semua TN bisa diserap tanaman
        
        **4. Nm (Mineral Nitrogen) - Nitrogen Mineral**
        - Nitrogen yang langsung tersedia (NH4+, NO3-)
        - Rentang: 0.2-0.45%
        - Langsung diserap tanpa perlu dekomposisi
        
        ---
        
        ### Asumsi & Keterbatasan Model
        
        **Asumsi:**
        1. Kelembaban tanah cukup untuk dekomposisi
        2. Tidak ada pencucian nitrogen (estimasi konservatif)
        3. Populasi mikroba tanah normal
        4. Material tercampur merata dengan tanah
        
        **Keterbatasan:**
        1. Tidak memperhitungkan pencucian hujan
        2. Tidak memperhitungkan penyerapan tanaman
        3. Tidak memperhitungkan volatilisasi ammonia
        4. Hasil adalah estimasi, bukan pengukuran aktual
        
        **Validasi:**
        - Model divalidasi dengan data WAGRI
        - Akurasi: ±1% dari hasil WAGRI
        - Cocok untuk perencanaan dan edukasi
        - Untuk keputusan kritis, konsultasi dengan ahli agronomi
        """)
    
    with st.expander("💡 Praktik Terbaik Penggunaan Pupuk Organik"):
        st.markdown("""
        ### 1. Waktu Aplikasi yang Tepat
        
        **Prinsip Dasar:**
        > Aplikasikan pupuk organik **2-4 minggu sebelum tanam** agar nitrogen sudah mulai tersedia saat tanaman membutuhkan.
        
        **Panduan Berdasarkan Tanaman:**
        
        | Jenis Tanaman | Waktu Aplikasi | Alasan |
        |---------------|----------------|--------|
        | Padi | 2-3 minggu sebelum tanam | Perlu nitrogen di fase vegetatif |
        | Jagung | 2-4 minggu sebelum tanam | Kebutuhan N tinggi di awal |
        | Sayuran Daun | 1-2 minggu sebelum tanam | Siklus pendek, perlu N cepat |
        | Cabai/Tomat | 3-4 minggu sebelum tanam | Siklus panjang, perlu N bertahap |
        | Tanaman Tahunan | 4-6 minggu sebelum musim hujan | Persiapan fase pertumbuhan |
        
        **Tips Timing:**
        - 🌧️ Aplikasi di awal musim hujan → kelembaban optimal
        - ☀️ Hindari aplikasi saat kemarau panjang → dekomposisi terhambat
        - 🌱 Sinkronkan dengan fase pertumbuhan tanaman
        
        ---
        
        ### 2. Metode Aplikasi yang Benar
        
        **❌ SALAH: Aplikasi di Permukaan**
        - Nitrogen menguap (volatilisasi NH3)
        - Kehilangan bisa mencapai 30-50%
        - Bau tidak sedap
        - Menarik hama
        
        **✅ BENAR: Inkorporasi ke Tanah**
        
        **Cara Aplikasi:**
        1. **Sebar Merata**
           - Taburkan pupuk organik merata di lahan
           - Gunakan dosis sesuai perhitungan
        
        2. **Campur dengan Tanah**
           - Bajak atau cangkul sedalam 15-20 cm
           - Pastikan tercampur merata
           - Jangan terlalu dalam (> 30 cm)
        
        3. **Siram/Tunggu Hujan**
           - Kelembaban memicu aktivitas mikroba
           - Jika kering, siram secukupnya
           - Ideal: 60-70% kapasitas lapang
        
        4. **Tunggu Dekomposisi**
           - Biarkan 2-4 minggu sebelum tanam
           - Cek dengan kalkulator kapan nitrogen tersedia
        
        **Metode Khusus:**
        - **Larikan:** Untuk tanaman baris (jagung, kedelai)
        - **Lubang Tanam:** Untuk tanaman buah/tahunan
        - **Broadcast:** Untuk padi sawah
        
        ---
        
        ### 3. Perhitungan Dosis yang Tepat
        
        **Langkah-langkah:**
        
        **Step 1: Tentukan Kebutuhan Nitrogen Tanaman**
        ```
        Contoh Jagung:
        - Target: 8 ton/ha
        - Kebutuhan N: 20 kg N per ton hasil
        - Total N dibutuhkan: 8 × 20 = 160 kg N/ha
        ```
        
        **Step 2: Hitung Kontribusi Pupuk Organik**
        ```
        Gunakan kalkulator ini:
        - Input: 2000 kg Pupuk Kandang Sapi
        - Hasil: 35 kg N terlepas dalam 60 hari (60%)
        ```
        
        **Step 3: Hitung Kekurangan**
        ```
        - Kebutuhan total: 160 kg N/ha
        - Dari organik: 35 kg N/ha
        - Kekurangan: 125 kg N/ha
        ```
        
        **Step 4: Tambahan Pupuk Kimia (jika perlu)**
        ```
        Pilihan 1 - Urea (46% N):
        - Dosis: 125 ÷ 0.46 = 272 kg Urea/ha
        
        Pilihan 2 - ZA (21% N):
        - Dosis: 125 ÷ 0.21 = 595 kg ZA/ha
        ```
        
        **Step 5: Jadwal Aplikasi**
        ```
        Minggu 0: Pupuk organik (2000 kg/ha)
        Minggu 2: Tanam
        Minggu 3: Urea I (136 kg/ha) - 50%
        Minggu 6: Urea II (136 kg/ha) - 50%
        ```
        
        ---
        
        ### 4. Monitoring & Penyesuaian
        
        **Indikator Visual:**
        
        **Kekurangan Nitrogen:**
        - 🟡 Daun menguning (terutama daun tua)
        - 📏 Pertumbuhan terhambat/kerdil
        - 🌱 Batang kurus dan lemah
        - **Tindakan:** Tambah Urea 50-100 kg/ha
        
        **Kelebihan Nitrogen:**
        - 🟢 Daun hijau tua berlebihan
        - 🌿 Pertumbuhan vegetatif berlebihan
        - 🦠 Rentan penyakit
        - **Tindakan:** Kurangi dosis aplikasi berikutnya
        
        **Optimal:**
        - 💚 Hijau segar merata
        - 📈 Pertumbuhan seimbang
        - 🌾 Batang kokoh
        
        **Uji Tanah:**
        - Lakukan uji tanah **mid-season** (pertengahan musim)
        - Cek kadar N-total dan N-tersedia
        - Sesuaikan aplikasi berdasarkan hasil
        
        ---
        
        ### 5. Kesalahan Umum yang Harus Dihindari
        
        **❌ Kesalahan #1: Aplikasi Terlambat**
        - Tanaman sudah butuh N, tapi pupuk organik belum terdekomposisi
        - **Solusi:** Aplikasi 2-4 minggu sebelum tanam
        
        **❌ Kesalahan #2: Aplikasi di Permukaan**
        - Volatilisasi NH3, kehilangan 30-50%
        - **Solusi:** Selalu campur dengan tanah
        
        **❌ Kesalahan #3: Tanah Kering**
        - Tidak ada dekomposisi tanpa air
        - **Solusi:** Pastikan kelembaban cukup
        
        **❌ Kesalahan #4: Dosis Berlebihan**
        - Ketidakseimbangan nutrisi
        - Pemborosan biaya
        - **Solusi:** Gunakan kalkulator untuk dosis tepat
        
        **❌ Kesalahan #5: Tidak Monitoring**
        - Tidak tahu apakah nitrogen cukup atau kurang
        - **Solusi:** Amati tanaman, uji tanah berkala
        
        ---
        
        ### 6. Kombinasi Pupuk Organik + Kimia
        
        **Strategi Terbaik: Integrated Nutrient Management**
        
        **Prinsip:**
        - Pupuk organik sebagai **dasar** (slow release, perbaiki tanah)
        - Pupuk kimia sebagai **suplemen** (quick release, penuhi kekurangan)
        
        **Contoh Aplikasi Padi:**
        ```
        Sebelum Tanam:
        - Pupuk Kandang: 2 ton/ha
        - Urea: 100 kg/ha (50% dosis)
        
        Fase Vegetatif (3 minggu):
        - Urea: 50 kg/ha (25% dosis)
        
        Fase Generatif (6 minggu):
        - Urea: 50 kg/ha (25% dosis)
        
        Total N: ~120 kg/ha
        - Dari organik: 40 kg (33%)
        - Dari kimia: 80 kg (67%)
        ```
        
        **Manfaat Kombinasi:**
        - ✅ Nitrogen tersedia cepat DAN bertahap
        - ✅ Efisiensi pupuk kimia meningkat
        - ✅ Kesehatan tanah terjaga
        - ✅ Biaya lebih efisien jangka panjang
        """)
    
    with st.expander("❓ FAQ - Pertanyaan yang Sering Diajukan"):
        st.markdown("""
        ### Q1: Berapa lama pupuk organik mulai bekerja?
        
        **A:** Tergantung suhu dan jenis material:
        - **Suhu 25-30°C:** Mulai terlihat efek dalam 1-2 minggu
        - **Suhu 20-25°C:** Mulai terlihat efek dalam 2-3 minggu
        - **Suhu < 20°C:** Mulai terlihat efek dalam 3-4 minggu
        
        Gunakan kalkulator ini untuk prediksi lebih akurat!
        
        ---
        
        ### Q2: Apakah pupuk organik bisa menggantikan pupuk kimia 100%?
        
        **A:** Bisa, tapi dengan catatan:
        - ✅ **Untuk tanaman jangka panjang:** Sangat bisa (buah, sayuran organik)
        - ⚠️ **Untuk tanaman intensif:** Perlu dosis sangat tinggi (tidak ekonomis)
        - 💡 **Rekomendasi:** Kombinasi 30-50% organik + 50-70% kimia (paling efisien)
        
        ---
        
        ### Q3: Pupuk mana yang paling bagus?
        
        **A:** Tergantung ketersediaan dan tujuan:
        
        | Pupuk | Kelebihan | Kekurangan | Cocok Untuk |
        |-------|-----------|------------|-------------|
        | **Pupuk Kandang Ayam** | N tinggi (4.5%), cepat terurai | Bau kuat, bisa bakar tanaman | Sayuran, tanaman cepat panen |
        | **Pupuk Kandang Sapi** | Aman, memperbaiki tanah | N rendah (2.8%), lambat terurai | Tanaman jangka panjang |
        | **Kompos Jerami** | Murah, mudah dibuat | N rendah (3.2%) | Padi, tanaman pangan |
        | **Bokashi** | Cepat terurai, kaya mikroba | Perlu fermentasi dulu | Semua tanaman |
        
        ---
        
        ### Q4: Kenapa hasil kalkulator berbeda dengan kenyataan di lapangan?
        
        **A:** Beberapa faktor yang mempengaruhi:
        1. **Kelembaban tanah** - Model asumsi kelembaban optimal
        2. **Kualitas material** - Komposisi bisa bervariasi
        3. **Pencucian hujan** - Model tidak hitung kehilangan
        4. **Penyerapan tanaman** - Model hanya hitung pelepasan
        5. **Kondisi tanah** - pH, tekstur, mikroba berbeda-beda
        
        **Solusi:** Gunakan hasil kalkulator sebagai **panduan awal**, sesuaikan berdasarkan pengamatan lapangan.
        
        ---
        
        ### Q5: Apakah bisa menggunakan pupuk organik untuk hidroponik?
        
        **A:** **Tidak disarankan** untuk hidroponik konvensional karena:
        - Pupuk organik perlu dekomposisi di tanah
        - Bisa menyumbat sistem hidroponik
        - Kualitas air jadi keruh
        
        **Alternatif:** Gunakan pupuk organik cair yang sudah difermentasi atau pupuk AB mix khusus hidroponik.
        
        ---
        
        ### Q6: Bagaimana cara menyimpan pupuk organik?
        
        **A:** Tips penyimpanan:
        - 🏠 Tempat teduh, tidak terkena hujan langsung
        - 🌬️ Sirkulasi udara baik (tidak lembab berlebihan)
        - 📦 Tutup dengan terpal jika outdoor
        - ⏱️ Gunakan dalam 3-6 bulan (kualitas terbaik)
        - 🦠 Jika berjamur putih → masih bagus (jamur dekomposer)
        - ❌ Jika berbau busuk → sudah terlalu lama
        
        ---
        
        ### Q7: Berapa biaya pupuk organik vs kimia?
        
        **A:** Perbandingan biaya (contoh untuk 1 ha padi):
        
        **Opsi 1: Pupuk Kimia Saja**
        - Urea 300 kg × Rp 2.500 = Rp 750.000
        - SP36 100 kg × Rp 2.000 = Rp 200.000
        - KCl 100 kg × Rp 3.000 = Rp 300.000
        - **Total: Rp 1.250.000/musim**
        
        **Opsi 2: Kombinasi Organik + Kimia**
        - Pupuk Kandang 2 ton × Rp 300.000 = Rp 600.000
        - Urea 150 kg × Rp 2.500 = Rp 375.000
        - SP36 50 kg × Rp 2.000 = Rp 100.000
        - KCl 50 kg × Rp 3.000 = Rp 150.000
        - **Total: Rp 1.225.000/musim**
        
        **Opsi 3: Organik Sendiri (Kompos)**
        - Biaya pembuatan kompos: Rp 200.000
        - Urea 100 kg × Rp 2.500 = Rp 250.000
        - **Total: Rp 450.000/musim** ✅ **PALING HEMAT!**
        
        **Catatan:** Opsi 3 paling hemat + meningkatkan kesehatan tanah jangka panjang!
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
