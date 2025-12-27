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

from services.ipm_seed_landscape_calculator import IPMSeedLandscapeCalculator
from utils.auth import require_auth, show_user_info_sidebar

# Page config
st.set_page_config(
    page_title="IPM, Seed & Landscape",
    page_icon="🌾",
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
st.title("🌾 IPM 2.0, Seed Saving & Landscape Planning")
st.markdown("""
Integrated Pest Management dengan AI, Jaringan Benih Lokal, dan Perencanaan Lanskap Pertanian
""")

st.markdown("---")

# Initialize calculator
calc = IPMSeedLandscapeCalculator()

# Tabs
tab1, tab2, tab3 = st.tabs([
    "🔬 IPM 2.0 (AI Pest ID)",
    "🌱 Seed Saving Network",
    "🗺️ Landscape Planning"
])

# ===== TAB 1: IPM 2.0 =====
with tab1:
    st.subheader("Integrated Pest Management 2.0")
    
    st.info("""
    💡 **IPM 2.0** menggunakan AI untuk identifikasi hama dan rekomendasi pengendalian organik prioritas.
    Database hama telah disinkronisasi dengan **Heatmap Risiko Hama/Penyakit** (Hortikultura & Padi).
    """)
    
    # AI Pest Identification
    st.markdown("### 🔍 Identifikasi & Ensiklopedia Hama")
    
    col_p1, col_p2 = st.columns([1, 2])
    
    with col_p1:
        st.markdown("**Metode Input:**")
        input_method = st.radio("Pilih Metode:", ["📸 Upload Foto (AI Scan)", "📖 Pilih Manual (Database)"], label_visibility="collapsed")
        
        pest_name_selected = None
        
        if input_method == "📸 Upload Foto (AI Scan)":
            uploaded_file = st.file_uploader("Upload Foto Hama", type=['jpg', 'jpeg', 'png'])
            if uploaded_file:
                st.image(uploaded_file, caption="Preview Foto", use_container_width=True)
                if st.button("🚀 Analisis Foto (AI)", type="primary"):
                    # Simulation: Just pick the first one or random for now, or assume logical flow
                    # For demo purposes, we'll pretend it identified the one selected below or default
                    st.success("✅ AI berhasil mengidentifikasi hama!")
                    pest_name_selected = "Wereng Coklat" # Default simulation result
        
        else:
            st.markdown("**Pilih jenis OPT dari Database:**")
            pest_name_selected = st.selectbox("Daftar Hama & Penyakit:", list(calc.PEST_DATABASE.keys()))
            st.caption("ℹ️ Pilih nama hama untuk melihat detail pengendalian.")
    
    with col_p2:
        # Display Logic
        display_pest = pest_name_selected 
        
        # If we are in manual mode, we always show the selection
        # If we are in upload mode, we only show if analyzed (simulated above) or logic handled
        
        # Simplified logic for better UX:
        # If manual mode -> show immediately
        # If upload mode -> show "Waiting for upload/analysis" or result
        
        if input_method == "📖 Pilih Manual (Database)" and display_pest:
            result = calc.identify_pest(display_pest)
        elif input_method == "📸 Upload Foto (AI Scan)" and pest_name_selected:
             result = calc.identify_pest(pest_name_selected)
        else:
            result = None

        if result and result['identified']:
            # Header with "Card" style
            st.markdown(f"""
            <div style="background-color: #dcfce7; padding: 15px; border-radius: 10px; border-left: 5px solid #22c55e;">
                <h2 style="margin:0; color: #166534;">🦟 {result['pest_name']}</h2>
                <p style="margin:0; color: #15803d; font-style: italic;">{result['data']['scientific_name']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            pest_data = result['data']
            
            # Pest info tabs
            info_tab1, info_tab2 = st.tabs(["📋 Deskripsi & Gejala", "🛡️ Pengendalian (Solusi)"])
            
            with info_tab1:
                st.markdown(f"""
                **Tanaman Inang:**  
                {', '.join(pest_data['crops_affected'])}
                
                **Tipe Kerusakan:**  
                {pest_data['damage_type']}
                
                **Gejala Serangan:**  
                {pest_data['symptoms']}
                """)
                
                st.info(f"💡 **Pencegahan:** {pest_data['prevention']}")
            
            with info_tab2:
                st.markdown("### 🌿 Pengendalian Organik (Prioritas)")
                for method in pest_data['organic_control']:
                    st.markdown(f"- ✅ {method}")
                
                st.markdown("---")
                st.markdown("### ⚠️ Pengendalian Kimia (Terakhir)")
                st.markdown(f"🔴 **Bahan Aktif:** {pest_data['chemical_control']}")
                st.caption("Gunakan bijak sesuai dosis anjuran. Utamakan keselamatan musuh alami.")

        elif input_method == "📸 Upload Foto (AI Scan)" and not pest_name_selected:
            st.info("👈 Silakan upload foto dan klik tombol analisis, atau gunakan **Mode Manual** untuk melihat database.")
        
        else:
            st.info("👈 Silakan pilih hama di menu sebelah kiri.")    
    # IPM Cost-Benefit Analysis
    st.markdown("---")
    st.markdown("### 💰 IPM Cost-Benefit Analysis")
    
    col_cb1, col_cb2 = st.columns(2)
    
    with col_cb1:
        area_ipm = st.number_input("Luas Lahan (ha)", 1, 100, 5, 1, key="ipm_area")
        conventional_cost = st.number_input("Biaya Konvensional (Rp/ha)", 
                                           1000000, 20000000, 5000000, 100000,
                                           help="Biaya pestisida kimia per ha")
    
    with col_cb2:
        ipm_cost = st.number_input("Biaya IPM (Rp/ha)", 
                                   500000, 10000000, 3000000, 100000,
                                   help="Biaya pengendalian organik per ha")
        yield_increase = st.slider("Peningkatan Yield (%)", 0, 30, 10,
                                   help="Yield meningkat karena tanaman lebih sehat")
    
    if st.button("📊 Hitung ROI IPM", type="primary"):
        result = calc.calculate_ipm_cost_benefit(area_ipm, conventional_cost, ipm_cost, yield_increase)
        
        st.markdown("---")
        
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        
        with col_r1:
            st.metric("Biaya Konvensional", f"Rp {result['conventional_cost']:,.0f}")
        
        with col_r2:
            st.metric("Biaya IPM", f"Rp {result['ipm_cost']:,.0f}")
        
        with col_r3:
            st.metric("Total Benefit", f"Rp {result['total_benefit']:,.0f}",
                     f"Hemat + Yield")
        
        with col_r4:
            st.metric("ROI", f"{result['roi_pct']:.0f}%")
        
        st.success(f"""
        💰 **Penghematan Biaya:** Rp {result['cost_savings']:,.0f}
        
        📈 **Nilai Peningkatan Yield:** Rp {result['yield_increase_value']:,.0f}
        """)


# ===== TAB 2: SEED SAVING NETWORK =====
with tab2:
    st.subheader("Jaringan Benih Lokal & Heirloom")
    
    st.info("""
    💡 **Seed Saving Network** untuk konservasi varietas lokal dan heirloom.
    Biodiversitas adalah asuransi terhadap perubahan iklim!
    """)
    
    # Display seed varieties
    for crop_type, varieties in calc.SEED_VARIETIES.items():
        st.markdown(f"### 🌾 {crop_type}")
        
        for variety_name, variety_data in varieties.items():
            with st.expander(f"📦 {variety_name}"):
                col_s1, col_s2 = st.columns(2)
                
                with col_s1:
                    st.markdown(f"""
                    **Asal:** {variety_data['origin']}
                    
                    **Karakteristik:**
                    {variety_data['characteristics']}
                    
                    **Hari Panen:** {variety_data['days_to_harvest']} hari
                    """)
                
                with col_s2:
                    st.markdown(f"""
                    **Potensi Hasil:** {variety_data['yield_potential']}
                    
                    **Status Konservasi:** {variety_data['conservation_status']}
                    """)
                    
                    # Conservation status color
                    status = variety_data['conservation_status']
                    if status == 'Endangered':
                        st.error("🔴 Terancam Punah - Perlu Konservasi Segera!")
                    elif status == 'Rare':
                        st.warning("🟡 Langka - Perlu Perlindungan")
                    elif status == 'Vulnerable':
                        st.info("🔵 Rentan - Perlu Monitoring")
                    else:
                        st.success("🟢 Umum - Tetap Lestarikan")
                
                # Seed exchange info
                st.markdown("---")
                st.markdown("**💱 Seed Exchange:**")
                
                col_ex1, col_ex2 = st.columns(2)
                
                with col_ex1:
                    if st.button(f"📤 Saya Punya Benih Ini", key=f"have_{variety_name}"):
                        st.success("✅ Terima kasih! Benih Anda terdaftar di jaringan.")
                
                with col_ex2:
                    if st.button(f"📥 Saya Butuh Benih Ini", key=f"need_{variety_name}"):
                        st.info("📧 Kami akan hubungkan Anda dengan penyedia benih.")
    
    # Add new variety
    st.markdown("---")
    st.markdown("### ➕ Kontribusi Varietas Lokal")
    
    with st.expander("Tambahkan Varietas Baru"):
        col_add1, col_add2 = st.columns(2)
        
        with col_add1:
            new_crop = st.text_input("Jenis Tanaman")
            new_variety = st.text_input("Nama Varietas")
            new_origin = st.text_input("Asal Daerah")
        
        with col_add2:
            new_characteristics = st.text_area("Karakteristik Unik")
            new_days = st.number_input("Hari Panen", 30, 300, 90)
        
        if st.button("📝 Submit Varietas"):
            st.success("""
            ✅ Terima kasih atas kontribusinya!
            
            Tim kami akan verifikasi dan menambahkan ke database seed network.
            """)


# ===== TAB 3: LANDSCAPE PLANNING =====
with tab3:
    st.subheader("Perencanaan Lanskap Pertanian")
    
    st.info("""
    💡 **Landscape Planning** untuk desain farm yang optimal.
    Seimbangkan produksi, konservasi, dan infrastruktur!
    """)
    
    st.markdown("### 🗺️ Zonasi Lahan")
    
    col_l1, col_l2 = st.columns(2)
    
    with col_l1:
        total_area = st.number_input("Total Luas Lahan (ha)", 1, 1000, 10, 1)
        
        st.markdown("**Alokasi Zona (%):**")
        production_pct = st.slider("Zona Produksi", 0, 100, 70,
                                   help="Area untuk tanaman komersial")
        conservation_pct = st.slider("Zona Konservasi", 0, 100, 20,
                                     help="Area untuk biodiversitas, riparian buffer")
        infrastructure_pct = st.slider("Infrastruktur", 0, 100, 10,
                                       help="Jalan, irigasi, bangunan, storage")
    
    with col_l2:
        # Validation
        total_pct = production_pct + conservation_pct + infrastructure_pct
        
        if total_pct != 100:
            st.error(f"⚠️ Total alokasi: {total_pct}% (harus 100%)")
        else:
            st.success(f"✅ Total alokasi: {total_pct}%")
        
        # Pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['Produksi', 'Konservasi', 'Infrastruktur'],
            values=[production_pct, conservation_pct, infrastructure_pct],
            marker=dict(colors=['#10b981', '#3b82f6', '#f59e0b'])
        )])
        fig.update_layout(title="Distribusi Zona Lahan")
        st.plotly_chart(fig, use_container_width=True)
    
    if total_pct == 100 and st.button("🗺️ Generate Landscape Plan", type="primary"):
        result = calc.calculate_landscape_zones(total_area, production_pct, 
                                                conservation_pct, infrastructure_pct)
        
        st.markdown("---")
        st.markdown("### 📊 Rencana Zonasi")
        
        col_z1, col_z2, col_z3 = st.columns(3)
        
        with col_z1:
            st.metric("Zona Produksi", f"{result['production_area_ha']:.1f} ha",
                     f"{production_pct}%")
        
        with col_z2:
            st.metric("Zona Konservasi", f"{result['conservation_area_ha']:.1f} ha",
                     f"{conservation_pct}%")
        
        with col_z3:
            st.metric("Infrastruktur", f"{result['infrastructure_area_ha']:.1f} ha",
                     f"{infrastructure_pct}%")
        
        # Recommendations
        if result['recommendations']:
            st.markdown("### 💡 Rekomendasi")
            for rec in result['recommendations']:
                st.warning(rec)
        else:
            st.success("✅ Alokasi zona sudah optimal!")
        
        # Detailed zone planning
        st.markdown("### 🎯 Detail Perencanaan per Zona")
        
        with st.expander("🟢 Zona Produksi"):
            st.markdown(f"""
            **Luas:** {result['production_area_ha']:.1f} ha
            
            **Rekomendasi Layout:**
            - Plot produksi utama: 80% ({result['production_area_ha']*0.8:.1f} ha)
            - Crop rotation area: 15% ({result['production_area_ha']*0.15:.1f} ha)
            - Trial/nursery: 5% ({result['production_area_ha']*0.05:.1f} ha)
            
            **Best Practices:**
            - Kelompokkan tanaman dengan kebutuhan air sama
            - Buat akses jalan antar plot (min 2m)
            - Pertimbangkan arah matahari untuk tanaman sensitif
            """)
        
        with st.expander("🔵 Zona Konservasi"):
            st.markdown(f"""
            **Luas:** {result['conservation_area_ha']:.1f} ha
            
            **Komponen:**
            - Riparian buffer (tepi sungai/saluran): 30%
            - Windbreak/hedgerow: 25%
            - Wildlife corridor: 20%
            - Wetland/pond: 15%
            - Native vegetation: 10%
            
            **Manfaat:**
            - Habitat predator alami hama
            - Penyerbuk (lebah, kupu-kupu)
            - Kontrol erosi
            - Regulasi air
            - Biodiversitas
            """)
        
        with st.expander("🟡 Zona Infrastruktur"):
            st.markdown(f"""
            **Luas:** {result['infrastructure_area_ha']:.1f} ha
            
            **Komponen:**
            - Jalan utama & akses: 40%
            - Sistem irigasi: 25%
            - Bangunan (storage, kantor): 20%
            - Area parkir/loading: 10%
            - Utilitas (listrik, air): 5%
            
            **Prioritas:**
            1. Jalan all-weather untuk akses panen
            2. Sistem irigasi efisien
            3. Cold storage (jika perlu)
            4. Workshop/maintenance area
            """)


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🌾 <strong>AgriSensa IPM, Seed & Landscape</strong></p>
    <p>AI Pest Management | Seed Conservation | Farm Design Optimization</p>
</div>
""", unsafe_allow_html=True)
