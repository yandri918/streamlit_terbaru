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

from services.crop_planning_calculator import CropPlanningCalculator
# from utils.auth import require_auth, show_user_info_sidebar

# Page config
st.set_page_config(
    page_title="Crop Planning Optimizer",
    page_icon="🥗",
    layout="wide"
)

# Authentication
# user = require_auth()
# show_user_info_sidebar()

# Initialize calculator
calc = CropPlanningCalculator()

# Header
st.title("🥗 Crop Planning Optimizer")
st.markdown("""
Rencanakan komposisi tanaman sayuran Anda secara optimal berdasarkan **Sistem Tanam** dan **Tujuan** (Pribadi/Pasar).
""")
st.markdown("---")

# --- SIDEBAR INPUT ---
st.sidebar.header("📝 Parameter Perencanaan")

# 1. Tujuan
goal_display = {
    'personal': '🏠 Konsumsi Pribadi (Nutrisi Keluarga)',
    'market': '💰 Bisnis (Profit & Fast Turning)'
}
goal_key = st.sidebar.selectbox("Tujuan Tanam", options=['personal', 'market'], format_func=lambda x: goal_display[x])

# 2. Sistem
system_display = {
    'hydroponic': '💧 Hidroponik (NFT/DFT/Rakit Apung)',
    'soil': '🌱 Lahan Terbuka/Tanah (Konvensional)',
    'mixed': '🔄 Campuran (Hybrid)'
}
system_key = st.sidebar.selectbox("Sistem Pertanian", options=['hydroponic', 'soil', 'mixed'], format_func=lambda x: system_display[x])

# 3. Luasan
area_input = st.sidebar.number_input("Luas Lahan Efektif (m²)", min_value=1.0, value=20.0, step=1.0, help="Area bersih yang bisa ditanami")

# 4. Pilihan Tanaman
available_crops = list(calc.VEGETABLE_DB.keys())
# Ensure defaults exist in available_crops to prevent StreamlitAPIException
default_personal = [c for c in ['Pakcoy', 'Selada (Lettuce)', 'Kangkung'] if c in available_crops]
default_market = [c for c in ['Selada (Lettuce)', 'Pakcoy', 'Kale'] if c in available_crops]

default_selection = default_personal if goal_key == 'personal' else default_market
selected_crops = st.sidebar.multiselect("Pilih Jenis Tanaman (Min. 2)", options=available_crops, default=default_selection)

if st.sidebar.button("🚀 Buat Rencana Tanam", type="primary"):
    if not selected_crops:
        st.error("Mohon pilih minimal satu jenis tanaman.")
    else:
        # Run Calculation
        inputs = {
            'area_m2': area_input,
            'system': system_key,
            'goal': goal_key,
            'selected_crops': selected_crops
        }
        result = calc.calculate_plan(inputs)
        
        # --- RESULTS DISPLAY ---
        
        # 1. Summary Metrics
        st.subheader("📊 Ringkasan Rencana")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Luas", f"{result['total_area']} m²")
        with col2:
            st.metric("Estimasi Total Panen", f"{result['total_yield_kg']:.1f} kg", "per siklus")
        with col3:
            st.metric("Variasi Tanaman", f"{len(result['plan'])} Jenis")
            
        # 2. Visualization (Pie Chart)
        labels = list(result['plan'].keys())
        values = [d['allocation_pct'] for d in result['plan'].values()]
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4)])
        fig.update_layout(title="Proporsi Alokasi Lahan (%)")
        st.plotly_chart(fig, use_container_width=True)
        
        # 3. Detailed Plan
        st.subheader("📝 Detail & Jadwal Tanam")
        
        for crop, data in result['plan'].items():
            with st.expander(f"🥬 {crop} ({data['allocation_pct']}%)", expanded=True):
                c1, c2, c3, c4 = st.columns(4)
                with c1:
                    st.markdown(f"**Alokasi Area:**\n{data['area_alloc_m2']:.1f} m²")
                with c2:
                    st.markdown(f"**Jumlah Tanaman:**\n~{data['plant_count']} lubang/btg")
                with c3:
                    st.markdown(f"**Estimasi Panen:**\n{data['yield_est_kg']:.1f} kg")
                with c4:
                    st.markdown(f"**Slus Panen:**\n{data['harvest_days']} Hari")
                    
                if goal_key == 'personal':
                     st.caption(f"💡 Cukup untuk konsumsi sayur keluarga selama {(data['yield_est_kg']/0.5):.0f} kali makan (asumsi 0.5kg/masak).")
                else:
                     st.caption(f"💡 Perputaran {365/data['harvest_days']:.0f}x setahun. Fokus kualitas visual daun.")

        # 4. Recommendation Note
        st.info("""
        **💡 Tips Implementasi:**
        - **Semaian:** Lakukan penyemaian (seeding) 10-14 hari sebelum panen siklus sebelumnya agar lahan tidak kosong (continuous farming).
        - **Rotasi:** Pertimbangkan rotasi jenis tanaman antar blok untuk memutus siklus hama (terutama di lahan tanah).
        - **Nutrisi (Hidroponik):** Pastikan kepekatan nutrisi (PPM) disesuaikan. Sayur daun (Leafy) biasanya butuh 800-1200 PPM, sayur buah butuh lebih tinggi.
        """)
else:
    st.info("👈 Mulai dengan mengatur parameter di Sidebar kiri.")
    
    # Static Guide
    st.markdown("### Panduan Pemilihan Sistem & Tujuan")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Hidroponik**")
        st.markdown("- ✅ Bersih, pertumbuhan cepat, bebas gulma.")
        st.markdown("- ❌ Investasi awal tinggi, butuh listrik.")
    with c2:
        st.markdown("**Lahan Tanah (Konvensional)**")
        st.markdown("- ✅ Rasa lebih 'rich', investasi rendah.")
        st.markdown("- ❌ Butuh olah tanah, risiko hama tanah.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🥗 <strong>AgriSensa Crop Optimizer</strong></p>
    <p>Smart Allocation for Maximum Yield & Satisfaction</p>
</div>
""", unsafe_allow_html=True)
