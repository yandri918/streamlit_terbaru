import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.melon_sop_service import MelonSopService
from utils.auth import require_auth, show_user_info_sidebar

# Page Config
st.set_page_config(
    page_title="Melon Precision SOP",
    page_icon="🍈",
    layout="wide"
)

# Authentication
user = require_auth()
show_user_info_sidebar()

service = MelonSopService()

st.title("🍈 SOP Presisi Melon (Standard 25 Ton/Ha)")
st.markdown("""
**Sistem Manajemen Kebun Digital berbasis MHI** | Nutrisi Terukur, Irigasi Tepat, Kerja Terjadwal.
""")

# --- SIDEBAR CONFIG ---
st.sidebar.header("⚙️ Konfigurasi Kebun")
n_plants = st.sidebar.number_input("Jumlah Tanaman", 100, 50000, 1000, step=100)
var_name = st.sidebar.text_input("Varietas Melon", "Golden Aroma / Stella")
start_date = st.sidebar.date_input("Tanggal Tanam (HST 0)")

# --- MAIN DASHBOARD: HST CONTROL ---
st.markdown("### 📅 Hari Setelah Tanam (HST)")
hst = st.slider("Geser untuk melihat instruksi harian:", 0, 75, 15, help="Pilih umur tanaman saat ini")

# Get Data for selected HST
current_status = service.get_schedule_by_hst(hst)
phase = current_status['phase']
data = current_status['data']

# --- DISPLAY CARDS ---
st.info(f"📍 **Status Saat Ini:** {phase}")

col1, col2, col3 = st.columns([1.5, 1.5, 1])

with col1:
    st.markdown("#### 💧 Nutrisi & Irigasi (Fertigation)")
    
    # Gauge Chart for EC
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = data.get('target_ec', 0),
        title = {'text': "Target EC (mS/cm)"},
        gauge = {'axis': {'range': [0, 4]}, 'bar': {'color': "#10b981"}}
    ))
    fig.update_layout(height=200, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("##### 🧪 Resep Pupuk (PPM):")
    ppm_df = pd.DataFrame({
        'Unsur': ['Nitrogen (N)', 'Phosphat (P)', 'Kalium (K)', 'Kalsium (Ca)'],
        'Target PPM': [data.get('ppm_n'), data.get('ppm_p'), data.get('ppm_k'), data.get('ppm_ca')]
    })
    st.dataframe(ppm_df, hide_index=True, use_container_width=True)
    
    st.warning(f"⚠️ **Fokus Fase Ini:** {data.get('focus')}")

with col2:
    st.markdown("#### 📋 Mandor Logbook (To-Do List)")
    
    # Find relevant work tasks
    # Simple logic to find list in range
    tasks = []
    for period, task_list in service.WORK_SCHEDULE.items():
        if "HST" in period:
            try:
                # Handle numeric range parsing "HST 0-14"
                parts = period.replace("HST ", "").split("-")
                if len(parts) == 2:
                    start, end = int(parts[0]), int(parts[1]) if parts[1] != 'Panen' else 100
                    if start <= hst <= end:
                        tasks = task_list
                        break
            except:
                pass
        elif period == 'Pra-Tanam' and hst == 0:
             tasks = service.WORK_SCHEDULE['Pra-Tanam']
             
    for task in tasks:
        st.markdown(f"☐ {task}")
        
    st.markdown("---")
    water_plant = data.get('water_l_plant_day', 0)
    total_water = water_plant * n_plants
    
    st.metric("💦 Kebutuhan Air Harian", f"{total_water:,.0f} Liter", f"{water_plant} L/tanaman")
    st.caption("Pecah menjadi 5-8x interval siram (Pulse Irrigation) untuk efisiensi.")

with col3:
    st.markdown("#### 💰 Estimasi Panen")
    est = service.calculate_needs(n_plants)
    
    st.metric("Target Yield (Ton)", f"{est['est_yield_ton']:.1f} Ton", "Standard MHI")
    st.metric("Potensi Omzet", f"Rp {est['est_gross_revenue']:,.0f}", "Asumsi Grade A 80%")
    
    st.markdown("### 🛡️ PHT Checklist")
    st.checkbox("Cek Kuning Daun (Virus/Mg/N)")
    st.checkbox("Cek Balik Daun (Kutu)")
    st.checkbox("Cek Leher Akar (Gummy Stem)")
    
# --- FOOTER SOP DOWNLOAD ---
st.markdown("---")
with st.expander("📥 Download SOP Lengkap (PDF/Excel)"):
    st.info("Fitur export dokumen PDF lengkap akan tersedia pada update berikutnya.")
    st.markdown("""
    **Isi Dokumen:**
    1. Tabel Jadwal Pemupukan Harian (H-7 s.d H+70)
    2. Logbook Mandor Kosong
    3. Standar Grade Panen
    """)

st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>🍈 <strong>AgriSensa Melon Precision System</strong></p>
    <p>Mengawal Kualitas dari Benih hingga Meja Makan</p>
</div>
""", unsafe_allow_html=True)
