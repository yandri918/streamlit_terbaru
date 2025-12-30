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

# TAB 4: EDUCATIONAL GUIDE
with tabs[3]:
    st.markdown("## 📚 Panduan Edukasi")
    
    st.info("💡 **Tentang Modul Ini:** Kalkulator ini membantu petani memahami ketersediaan Fosfor (P) dari pupuk organik. Berbeda dengan Nitrogen yang perlu dekomposisi, Fosfor langsung tersedia untuk tanaman sejak aplikasi.")
    
    with st.expander("🔶 Mengapa Fosfor (P) Penting untuk Tanaman?"):
        st.markdown("""
        ### Peran Kritis Fosfor dalam Pertumbuhan Tanaman
        
        **1. 🌱 Pembentukan Akar**
        - P sangat penting untuk pertumbuhan akar
        - Tanaman kekurangan P = akar pendek dan lemah
        - Akar kuat = penyerapan air & nutrisi lebih baik
        - **Fase kritis:** 2-4 minggu pertama setelah tanam
        
        **2. 🌸 Pembungaan & Pembuahan**
        - P memicu pembentukan bunga
        - Meningkatkan jumlah bunga dan buah
        - Mempercepat waktu berbunga
        - **Tanpa P cukup:** Bunga sedikit, buah kecil
        
        **3. ⚡ Transfer Energi (ATP)**
        - P adalah komponen ATP (Adenosine Triphosphate)
        - ATP = "baterai" sel tanaman
        - Semua proses metabolisme butuh ATP
        - **P kurang = energi tanaman rendah**
        
        **4. 🧬 Pembentukan DNA & RNA**
        - P adalah bagian dari DNA dan RNA
        - Penting untuk pembelahan sel
        - Pertumbuhan tanaman terhambat tanpa P
        
        **5. 🌾 Kualitas Hasil Panen**
        - Meningkatkan kadar protein biji-bijian
        - Memperbaiki kualitas buah
        - Meningkatkan daya simpan hasil panen
        
        ---
        
        ### Gejala Defisiensi Fosfor:
        
        **Visual (Mudah Dilihat):**
        - 🟣 **Daun tua berwarna ungu/kemerahan** (tanda khas!)
        - 🌱 **Pertumbuhan terhambat** (tanaman kerdil)
        - 🍂 **Daun kecil dan gelap**
        - 🌸 **Pembungaan terlambat atau tidak berbunga**
        
        **Non-Visual (Perlu Pengamatan):**
        - Akar pendek dan sedikit
        - Batang kurus dan lemah
        - Buah/biji sedikit dan kecil
        - Tanaman mudah rebah
        
        **Fase Kritis:**
        - Minggu 1-4: Pembentukan akar
        - Minggu 4-8: Pertumbuhan vegetatif
        - Minggu 8+: Pembungaan & pembuahan
        
        **Tindakan Jika Defisiensi:**
        1. Aplikasi pupuk P organik (pupuk kandang ayam)
        2. Tambah pupuk kimia (SP-36) untuk hasil cepat
        3. Perbaiki pH tanah (P tersedia optimal di pH 6-7)
        """)
    
    with st.expander("⚖️ Perbedaan Fosfor (P) vs Nitrogen (N)"):
        st.markdown("""
        ### Perbandingan Lengkap P vs N
        
        | Aspek | Nitrogen (N) 🌿 | Fosfor (P) 🔶 |
        |-------|------------------|----------------|
        | **Pelepasan** | Bertahap (1-3 bulan) | **Langsung tersedia** |
        | **Dekomposisi** | Perlu dekomposisi mikroba | **Tidak perlu dekomposisi** |
        | **Pengaruh Suhu** | Sangat berpengaruh (Q10) | **Tidak berpengaruh** |
        | **Mobilitas di Tanah** | Tinggi (mudah tercuci) | **Rendah (tidak tercuci)** |
        | **Waktu Aplikasi** | 2-4 minggu sebelum tanam | **Saat/sebelum tanam** |
        | **Metode Aplikasi** | Campur merata dengan tanah | **Dekat akar (tidak mobile)** |
        | **Fungsi Utama** | Pertumbuhan vegetatif (daun) | **Akar, bunga, buah** |
        | **Fase Kritis** | Sepanjang pertumbuhan | **Awal pertumbuhan** |
        | **Gejala Defisiensi** | Daun menguning | **Daun keunguan** |
        | **Kehilangan** | Pencucian hujan (30-50%) | **Fiksasi tanah (10-20%)** |
        
        ---
        
        ### Implikasi Praktis:
        
        **Untuk Nitrogen:**
        - ✅ Aplikasi bertahap (2-3 kali)
        - ✅ Perhatikan suhu & kelembaban
        - ✅ Hindari aplikasi sebelum hujan lebat
        - ✅ Monitor warna daun secara berkala
        
        **Untuk Fosfor:**
        - ✅ Aplikasi sekali di awal (langsung tersedia)
        - ✅ Tidak perlu khawatir suhu
        - ✅ Tidak tercuci hujan (aman)
        - ✅ Aplikasikan dekat akar (P tidak mobile)
        
        **Kombinasi Ideal:**
        ```
        Sebelum Tanam:
        - Pupuk Organik (N + P + K)
        - Fokus P di lubang tanam
        
        Minggu 2-4:
        - Tambah N (Urea) jika perlu
        - P sudah cukup dari awal
        
        Minggu 6-8:
        - Tambah N lagi
        - P masih tersedia dari awal
        ```
        
        💡 **Link ke Kalkulator N:** Gunakan halaman **102_🌿_Organic_Fertilizer_N_Release** untuk menghitung pelepasan Nitrogen
        """)
    
    with st.expander("🌾 Cara Aplikasi Pupuk P Organik yang Benar"):
        st.markdown("""
        ### Strategi Aplikasi Fosfor
        
        **Prinsip Dasar:**
        > Fosfor **tidak mobile** di tanah, jadi harus ditempatkan **dekat akar** tanaman!
        
        ---
        
        ### Metode Aplikasi Berdasarkan Tanaman:
        
        **1. Tanaman Baris (Jagung, Kedelai, Cabai)**
        
        **Metode Larikan:**
        ```
        1. Buat larikan sedalam 10-15 cm
        2. Taburkan pupuk organik di larikan
        3. Tutup dengan tanah tipis
        4. Tanam benih/bibit di atas larikan
        5. Akar langsung kontak dengan P
        ```
        
        **Dosis:** 2-3 ton/ha pupuk kandang
        
        ---
        
        **2. Tanaman Buah/Tahunan (Mangga, Jeruk, Durian)**
        
        **Metode Lubang Tanam:**
        ```
        1. Gali lubang 60×60×60 cm
        2. Campur tanah galian dengan:
           - 20-30 kg pupuk kandang
           - 500 g SP-36 (optional)
        3. Isi kembali lubang
        4. Biarkan 2 minggu
        5. Tanam bibit
        ```
        
        **Pemupukan Lanjutan:**
        - Buat parit melingkar (jarak 50 cm dari batang)
        - Isi dengan pupuk organik
        - Tutup kembali
        
        ---
        
        **3. Padi Sawah**
        
        **Metode Broadcast:**
        ```
        1. Setelah bajak, sebelum tanam
        2. Sebar pupuk organik merata
        3. Dosis: 2-3 ton/ha
        4. Rendam sawah
        5. Tanam padi 1-2 minggu kemudian
        ```
        
        **Catatan:** P tidak tercuci air, aman untuk sawah
        
        ---
        
        **4. Sayuran Daun (Kangkung, Bayam, Selada)**
        
        **Metode Bedengan:**
        ```
        1. Buat bedengan tinggi 20-30 cm
        2. Campur pupuk organik dengan tanah bedengan
        3. Dosis: 10-15 kg per 10 m² bedengan
        4. Ratakan dan siram
        5. Tanam 3-5 hari kemudian
        ```
        
        ---
        
        ### Tips Penting:
        
        **✅ DO (Lakukan):**
        - Campur pupuk organik dengan tanah
        - Aplikasikan dekat zona perakaran
        - Aplikasi sebelum/saat tanam
        - Kombinasi dengan pupuk kimia untuk hasil optimal
        
        **❌ DON'T (Jangan):**
        - Aplikasi di permukaan saja (P tidak turun)
        - Aplikasi terlalu jauh dari akar
        - Aplikasi terlalu dalam (>30 cm)
        - Mengandalkan P organik saja untuk tanaman intensif
        """)
    
    with st.expander("💰 Analisis Biaya: Organik vs Kimia"):
        st.markdown("""
        ### Perbandingan Biaya Pupuk P
        
        **Contoh Kasus: 1 Hektar Jagung**
        - Kebutuhan P: 60 kg P2O5/ha
        
        ---
        
        **Opsi 1: Pupuk Kimia Saja (SP-36)**
        
        ```
        Kebutuhan: 60 kg P2O5
        SP-36 (36% P2O5): 60 ÷ 0.36 = 167 kg
        
        Biaya:
        - SP-36: 167 kg × Rp 3.500 = Rp 584.500
        
        Total: Rp 584.500
        
        Keuntungan:
        ✅ Langsung tersedia
        ✅ Dosis pasti
        
        Kekurangan:
        ❌ Tidak memperbaiki tanah
        ❌ Biaya tinggi jangka panjang
        ```
        
        ---
        
        **Opsi 2: Kombinasi Organik + Kimia (Recommended ✅)**
        
        ```
        Pupuk Kandang Ayam (TP 3.5%):
        - Aplikasi: 2 ton/ha
        - P tersedia: 2000 × 0.035 × 0.53 = 37 kg P
        - P2O5 setara: 37 × 2.29 = 85 kg P2O5
        
        Kekurangan P2O5: 60 - 85 = -25 kg (SURPLUS!)
        
        Biaya:
        - Pupuk Kandang: 2 ton × Rp 400.000 = Rp 800.000
        - SP-36: TIDAK PERLU!
        
        Total: Rp 800.000
        
        Keuntungan:
        ✅ P cukup + surplus
        ✅ Bonus N dan K
        ✅ Memperbaiki struktur tanah
        ✅ Meningkatkan bahan organik
        
        Kekurangan:
        ⚠️ Biaya awal lebih tinggi
        ```
        
        ---
        
        **Opsi 3: Organik Sendiri (Kompos) + Kimia**
        
        ```
        Kompos Sendiri (TP 1.2%):
        - Aplikasi: 3 ton/ha
        - P tersedia: 3000 × 0.012 × 0.53 = 19 kg P
        - P2O5 setara: 19 × 2.29 = 44 kg P2O5
        
        Kekurangan: 60 - 44 = 16 kg P2O5
        SP-36 tambahan: 16 ÷ 0.36 = 44 kg
        
        Biaya:
        - Kompos (biaya buat): Rp 300.000
        - SP-36: 44 kg × Rp 3.500 = Rp 154.000
        
        Total: Rp 454.000 ✅ PALING HEMAT!
        
        Keuntungan:
        ✅ Biaya paling rendah
        ✅ Memperbaiki tanah
        ✅ Berkelanjutan
        
        Kekurangan:
        ⚠️ Perlu waktu buat kompos
        ```
        
        ---
        
        ### Kesimpulan Analisis Biaya:
        
        | Opsi | Biaya | Manfaat Tanah | Rekomendasi |
        |------|-------|---------------|-------------|
        | Kimia Saja | Rp 584.500 | ❌ Tidak ada | Untuk hasil cepat |
        | Organik + Kimia | Rp 800.000 | ✅✅✅ Sangat baik | **Terbaik jangka panjang** |
        | Kompos + Kimia | Rp 454.000 | ✅✅ Baik | **Paling hemat** |
        
        **Rekomendasi AgriSensa:**
        - **Tahun 1-2:** Opsi 2 (Organik + Kimia) untuk perbaiki tanah
        - **Tahun 3+:** Opsi 3 (Kompos sendiri) karena tanah sudah baik
        """)
    
    with st.expander("❓ FAQ - Pertanyaan Seputar Fosfor"):
        st.markdown("""
        ### Q1: Kenapa hasil kalkulator P konstan, tidak berubah seperti N?
        
        **A:** Karena **Fosfor tidak perlu dekomposisi**!
        
        - **Nitrogen (N):** Dalam bentuk organik, perlu diuraikan mikroba → butuh waktu → nilai berubah setiap hari
        - **Fosfor (P):** Sudah dalam bentuk tersedia (orthophosphate) → langsung bisa diserap → nilai konstan
        
        Ini bukan bug, ini memang karakteristik P! 😊
        
        ---
        
        ### Q2: Apakah P organik bisa menggantikan SP-36 100%?
        
        **A:** Bisa, tapi dengan catatan:
        
        ✅ **Untuk tanaman jangka panjang:** Sangat bisa (buah, sayuran organik)
        - Contoh: 2 ton pupuk kandang ayam = 85 kg P2O5 (cukup untuk jagung!)
        
        ⚠️ **Untuk tanaman intensif:** Perlu dosis sangat tinggi
        - Contoh: Untuk 100 kg P2O5 perlu 2.5 ton pupuk kandang ayam
        - Tidak ekonomis untuk lahan kecil
        
        💡 **Rekomendasi:** Kombinasi 50-70% organik + 30-50% kimia (paling efisien)
        
        ---
        
        ### Q3: Kenapa P tidak tercuci hujan seperti N?
        
        **A:** Karena P **tidak mobile** di tanah!
        
        **Nitrogen (N):**
        - Bentuk: NO3- (nitrat) = ion negatif
        - Sifat: Larut air, mudah bergerak
        - Hasil: Tercuci hujan (kehilangan 30-50%)
        
        **Fosfor (P):**
        - Bentuk: H2PO4- atau HPO4²- (phosphate)
        - Sifat: Terikat kuat dengan tanah (fiksasi)
        - Hasil: Tidak tercuci (kehilangan <5%)
        
        **Keuntungan:**
        - Aplikasi P sekali cukup untuk satu musim
        - Tidak perlu khawatir hujan lebat
        - P tersisa bisa dimanfaatkan musim berikutnya
        
        **Kekurangan:**
        - Harus aplikasi dekat akar (tidak bergerak ke akar)
        
        ---
        
        ### Q4: Apa itu P2O5? Kenapa tidak langsung P saja?
        
        **A:** P2O5 adalah **notasi standar pupuk**, bukan bentuk sebenarnya!
        
        **Sejarah:**
        - Dulu, analisis pupuk mengukur P sebagai P2O5 (fosfor pentoksida)
        - Notasi ini jadi standar internasional
        - Semua pupuk P ditulis dalam P2O5
        
        **Konversi:**
        - P2O5 = P × 2.29
        - P = P2O5 ÷ 2.29
        
        **Contoh:**
        - SP-36 = 36% P2O5 = 15.7% P
        - 10 kg P = 22.9 kg P2O5
        
        **Praktis:**
        - Gunakan P2O5 untuk bandingkan dengan pupuk kimia
        - Gunakan P untuk perhitungan ilmiah
        
        ---
        
        ### Q5: Kapan waktu terbaik aplikasi P organik?
        
        **A:** **Sebelum atau saat tanam** (berbeda dengan N!)
        
        **Alasan:**
        1. P langsung tersedia (tidak perlu tunggu dekomposisi)
        2. P tidak mobile (harus ada di zona akar sejak awal)
        3. Tanaman butuh P paling banyak di fase awal (pembentukan akar)
        
        **Timeline Aplikasi:**
        ```
        Minggu -2: Aplikasi P organik + olah tanah
        Minggu -1: Biarkan tanah settle
        Minggu 0: TANAM
        Minggu 2: Tambah N jika perlu
        Minggu 4: Tambah N lagi
        Minggu 6+: P masih tersedia dari awal
        ```
        
        **Catatan:** Jika terlambat aplikasi P, tanaman sudah stress → hasil turun
        
        ---
        
        ### Q6: Bagaimana cara tahu tanaman kekurangan P?
        
        **A:** Lihat **warna daun tua**!
        
        **Gejala Khas Defisiensi P:**
        - 🟣 **Daun tua berwarna ungu/kemerahan** (tanda paling jelas!)
        - 🌱 Tanaman kerdil (pertumbuhan lambat)
        - 🍂 Daun kecil dan gelap
        - 🌸 Tidak berbunga atau bunga sedikit
        
        **Bedakan dengan Defisiensi Lain:**
        - **N kurang:** Daun menguning (bukan ungu)
        - **K kurang:** Tepi daun terbakar
        - **Fe kurang:** Daun muda menguning (bukan tua)
        
        **Tindakan Cepat:**
        1. Aplikasi SP-36 (100-200 kg/ha) untuk hasil cepat
        2. Tambah pupuk kandang untuk jangka panjang
        3. Cek pH tanah (P tersedia optimal di pH 6-7)
        
        ---
        
        ### Q7: Apakah bisa aplikasi P organik untuk hidroponik?
        
        **A:** **Tidak disarankan** untuk hidroponik!
        
        **Alasan:**
        - Pupuk organik mengandung partikel padat
        - Bisa menyumbat sistem hidroponik
        - Kualitas air jadi keruh
        - Sulit kontrol konsentrasi P
        
        **Alternatif untuk Hidroponik:**
        - Gunakan pupuk AB mix (larut sempurna)
        - Atau pupuk organik cair yang sudah difilter
        - Atau ekstrak P dari pupuk organik (advanced)
        
        **Untuk Tanah:** Pupuk organik P sangat bagus! ✅
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🔶 <strong>AgriSensa Kalkulator Pelepasan Fosfor Pupuk Organik</strong></p>
    <p>Berdasarkan metodologi WAGRI (Platform Data Pertanian Jepang)</p>
    <p>Dikembangkan oleh NARO (National Agriculture and Food Research Organization)</p>
    <p><em>Untuk tujuan edukasi dan perencanaan. Konsultasi dengan ahli agronomi untuk rekomendasi spesifik.</em></p>
</div>
""", unsafe_allow_html=True)
