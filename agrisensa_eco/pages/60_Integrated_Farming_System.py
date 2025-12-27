import streamlit as st
import sys
import os
from pathlib import Path
import plotly.graph_objects as go
import pandas as pd

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.integrated_farming_calculator import IntegratedFarmingCalculator
from utils.auth import require_auth, show_user_info_sidebar

# Page config
st.set_page_config(
    page_title="Integrated Farming System",
    page_icon="🔄",
    layout="wide"
)

# Authentication
user = require_auth()
show_user_info_sidebar()

# Custom CSS
st.markdown("""
<style>
    .stMetric {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        padding: 15px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid #bbf7d0;
    }
    .main-header {
        text-align: center; 
        color: #166534;
        margin-bottom: 30px;
    }
    .highlight-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #166534;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.image("https://img.freepik.com/free-vector/isometric-farm-composition-with-view-farm-field-barn-house-windmill-vector-illustration_1284-80735.jpg?w=1380", use_column_width=True, caption="Ilustrasi Integrated Farming System")
st.markdown("<h1 class='main-header'>🔄 Sistem Pertanian Terpadu (Zero Waste)</h1>", unsafe_allow_html=True)

st.info("""
**Selamat Datang di Generator Sistem Terintegrasi!**
Masukkan komponen peternakan, pertanian, dan perikanan yang Anda miliki. 
Sistem akan menghitung potensi **Ekonomi Sirkular** menggunakan teknologi **Maggot BSF**, **Cacing (Vermicompost)**, dan **Kompos**.
""")

# --- INPUT SECTION (SIDEBAR) ---
st.sidebar.header("📝 Input Komponen Pertanian")

with st.sidebar.expander("🐄 1. Peternakan (Sumber Limbah)", expanded=True):
    n_sapi = st.number_input("Jumlah Sapi", 0, 100, 2, help="Penghasil limbah terbesar")
    n_kambing = st.number_input("Jumlah Kambing/Domba", 0, 200, 5)
    n_ayam = st.number_input("Jumlah Ayam (Ekor)", 0, 10000, 50)
    n_bebek = st.number_input("Jumlah Bebek (Ekor)", 0, 5000, 0)

with st.sidebar.expander("🌾 2. Pertanian (Lahan)", expanded=True):
    ha_padi = st.number_input("Luas Padi (Ha)", 0.0, 10.0, 0.5, step=0.1)
    ha_jagung = st.number_input("Luas Jagung (Ha)", 0.0, 10.0, 0.0, step=0.1)
    ha_sayur = st.number_input("Luas Sayuran (Ha)", 0.0, 5.0, 0.1, step=0.1)

with st.sidebar.expander("🐟 3. Perikanan (Konsumen Pakan)", expanded=True):
    n_lele = st.number_input("Jumlah Lele (Ekor)", 0, 50000, 1000)
    n_nila = st.number_input("Jumlah Nila (Ekor)", 0, 20000, 0)

# Build Input Dictionary
inputs = {
    'livestock': {'sapi': n_sapi, 'kambing': n_kambing, 'ayam_petelur': n_ayam, 'bebek': n_bebek},
    'land': {'padi': ha_padi, 'jagung': ha_jagung, 'sayuran': ha_sayur},
    'fisheries': {'lele': n_lele, 'nila': n_nila}
}

# --- CALCULATION ---
if st.sidebar.button("🚀 Analisis Potensi Integrasi", type="primary"):
    calc = IntegratedFarmingCalculator()
    results = calc.calculate_flow(inputs)
    sankey_data = calc.get_sankey_data(results)
    
    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["📊 Diagram Alir (Sankey)", "💰 Analisis Ekonomi & Detail", "💡 Rekomendasi Teknologi"])
    
    # TAB 1: SANKEY DIAGRAM
    with tab1:
        st.subheader("Peta Aliran Energi & Materi (Mass Balance)")
        st.caption("Visualisasi bagaimana limbah dikonversi menjadi produk bernilai tinggi.")
        
        # Create Sankey
        fig = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(color = "black", width = 0.5),
              label = sankey_data['label'],
              color = ["#ef4444", "#f97316", "#84cc16", "#06b6d4", "#8b5cf6", "#10b981", "#facc15", "#16a34a", "#4ade80"]
            ),
            link = dict(
              source = sankey_data['source'],
              target = sankey_data['target'],
              value = sankey_data['value']
            ))])

        fig.update_layout(title_text="Aliran Limbah ke Produk (Harian)", font_size=12, height=500)
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"""
        <div class="highlight-card">
            <h3>🔢 Neraca Massa Harian</h3>
            <ul>
                <li><strong>Total Limbah Ternak Masuk:</strong> {results['daily_waste_kg']:.1f} kg/hari</li>
                <li><strong>Output Maggot Segar:</strong> {results['potential_maggot_kg']:.1f} kg/hari (Protein Tinggi)</li>
                <li><strong>Output Pupuk Organik Total:</strong> {(results['potential_kasgot_kg'] + results['potential_kascing_kg'] + results['potential_compost_kg']):.1f} kg/hari</li>
                <li><strong>Potensi Biogas:</strong> {results['potential_biogas_m3']:.2f} m³/hari (Setara {results['potential_biogas_m3']*0.4:.1f} kg LPG)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # TAB 2: ECONOMIC ANALYSIS
    with tab2:
        st.subheader("Potensi Ekonomi & Penghematan")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Penghematan Pakan (Maggot)", f"Rp {results['feed_substitution_value']:,.0f}", "/hari")
        with col2:
            st.metric("Produksi Pupuk Mandiri", f"Rp {results['fertilizer_substitution_value']:,.0f}", "/hari")
        with col3:
            total_benefit = results['feed_substitution_value'] + results['fertilizer_substitution_value']
            st.metric("Total Nilai Tambah", f"Rp {total_benefit:,.0f}", "/hari")
            
        st.markdown("---")
        st.subheader("Rincian Produksi")
        
        # DataFrame for details
        data_produksi = {
            "Komponen": ["Maggot BSF (Black Soldier Fly)", "Kasgot (Pupuk Maggot)", "Kascing (Vermicompost)", "Kompos Konvensional", "Urine Ternak (POC)"],
            "Jumlah Harian": [
                f"{results['potential_maggot_kg']:.1f} kg",
                f"{results['potential_kasgot_kg']:.1f} kg",
                f"{results['potential_kascing_kg']:.1f} kg",
                f"{results['potential_compost_kg']:.1f} kg",
                f"{results['daily_urine_liter']:.1f} Liter"
            ],
            "Kegunaan Utama": [
                "Pakan Ikan/Unggas (Protein 40%)",
                "Pupuk Organik Padat (Kaya N)",
                "Pupuk Premium (Hormon Tumbuh)",
                "Pembenah Tanah (Soil Conditioner)",
                "Pupuk Organik Cair / Pestisida Nabati"
            ]
        }
        st.table(pd.DataFrame(data_produksi))
        
    # TAB 3: TECHNOLOGY RECOMMENDATIONS
    with tab3:
        st.subheader("Panduan Implementasi Teknologi")
        
        with st.expander("🪰 Budidaya Maggot BSF", expanded=True):
            st.markdown("""
            **Konsep:** Lalat BSF tidak membawa penyakit. Larvanya sangat rakus memakan limbah organik.
            
            **Cara Implementasi:**
            1. **Kandang Lalat (Insectarium):** Untuk perkawinan lalat dewasa.
            2. **Biopond (Tempat Larva):** Kotak kayu/beton tempat larva memakan sampah.
            3. **Panen:** Umur 14-18 hari. Maggot 'Pre-pupa' akan mencari tempat kering sendiri (self-harvesting).
            4. **Pemberian Pakan:** Langsung tebar ke kolam lele/nila (dapat menggantikan 30-50% pelet).
            """)
            
        with st.expander("🪱 Vermicomposting (Cacing Lumbricus)", expanded=False):
            st.markdown("""
            **Konsep:** Cacing memakan limbah yang sudah agak membusuk (fermentasi). Outputnya adalah Kascing (Terra Preta).
            
            **Cara Implementasi:**
            1. **Media:** Campuran kotoran sapi + serbuk gergaji/jerami.
            2. **Pakan:** Limbah sayur/buah (jangan terlalu asam/pedas).
            3. **Panen:** 1 bulan sekali. Ayak media untuk memisahkan cacing dan kascing.
            """)
            
        with st.expander("🍃 Kompos & Biogas", expanded=False):
            st.markdown("""
            **Biogas:**
            - Gunakan kotoran sapi segar + air (1:1).
            - Output gas metana untuk memasak.
            - Output ampas (slurry) sangat bagus untuk pupuk cair.
            
            **Kompos Jerami:**
            - Jangan dibakar! Gunakan dekomposer (EM4/Trichoderma).
            - Tumpuk berlapis dengan kotoran ternak.
            """)

else:
    st.info("👈 Silakan masukkan data ternak dan lahan Anda di Sidebar, lalu klik tombol 'Analisis'.")
    
    # Default landing visuals
    st.markdown("### Mengapa Integrated Farming?")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("### 💰 Profit Berganda")
        st.caption("Pendapatan tidak hanya dari daging/telur, tapi juga pupuk, maggot, dan penghematan biaya pakan.")
    with col_b:
        st.markdown("### 🛡️ Tahan Krisis")
        st.caption("Jika harga pakan pabrik naik, Anda punya pakan alternatif (Maggot/Azolla).")
    with col_c:
        st.markdown("### ♻️ Lingkungan Lestari")
        st.caption("Zero waste. Kotoran jadi emas hitam (pupuk), bukan masalah pencemaran.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🔄 <strong>AgriSensa Integrated System</strong></p>
    <p>Connecting Nature's Loops for Sustainable Agriculture</p>
</div>
""", unsafe_allow_html=True)
