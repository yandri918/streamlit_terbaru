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

from services.precision_sop_service import PrecisionSopService
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="SOP Presisi Multi-Komoditas",
    page_icon="🎯",
    layout="wide"
)

# user = require_auth()
# show_user_info_sidebar()

service = PrecisionSopService()

st.title("🎯 SOP Presisi Komoditas Unggulan")
st.markdown("""
**Platform Manajemen Agronomi Terpadu** | Standar MHI & Presisi Tinggi (Melon, Cabai, Padi).
""")

# --- SIDEBAR: KONFIGURASI ---
st.sidebar.header("⚙️ Parameter Kebun")

# 1. Pilih Komoditas
crop_type = st.sidebar.selectbox("Pilih Komoditas:", list(service.CROP_CONFIG.keys()))
config = service.CROP_CONFIG[crop_type]

# 2. Input Luas
n_ha = st.sidebar.number_input("Luas Lahan (Hektar)", 0.1, 1000.0, 25.0, step=0.1)
n_plants = int(n_ha * config['pop_per_ha'])

st.sidebar.info(f"""
**Statistik Kebun:**
- Luas: {n_ha} Ha
- Populasi: {n_plants:,.0f} Tanaman
- Target: {config['target_yield_ton_ha']} Ton/Ha
""")

start_date = st.sidebar.date_input("Tanggal Tanam")

# --- MAIN: SLIDER HST ---
max_days = config['cycle_days']
st.markdown(f"### 📅 Fase Tanaman ({crop_type})")
hst = st.slider("Hari Setelah Tanam (HST):", 0, max_days + 10, 30)

# Get Data
phase_name, data = service.get_crop_data(crop_type, hst)

# --- DISPLAY ---
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.info(f"📍 **Status Fase:** {phase_name}")
with col_h2:
    yield_est = service.calculate_yield_potential(crop_type, n_ha)
    st.metric("Potensi Omzet (Est)", f"Rp {yield_est['revenue']/1e9:,.1f} Milyar", f"Total {yield_est['total_yield_ton']:,.0f} Ton")

# --- TABS DETAIL ---
tab1, tab2 = st.tabs(["💧 Nutrisi & Agronomi", "📋 Tugas Mandor (Logbook)"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 🧪 Target Nutrisi (PPM / Kg)")
        
        # Data Nutrisi
        nutrients = {
            'Unsur': ['Nitrogen (N)', 'Phosphat (P)', 'Kalium (K)', 'Kalsium (Ca)'],
            'Target': [data.get('n',0), data.get('p',0), data.get('k',0), data.get('ca',0)]
        }
        df_nut = pd.DataFrame(nutrients)
        st.dataframe(df_nut, hide_index=True, use_container_width=True)
        
        if crop_type == "Padi Sawah (Modern)":
            st.caption("*Untuk Padi: Konversi ke Kg Urea/SP36/KCL per Ha sesuai rekomendasi setempat.")
            
    with c2:
        st.markdown("#### 🌊 Manajemen Air")
        if data.get('ec') > 0:
            st.metric("Target EC (Kepekatan)", f"{data.get('ec')} mS/cm")
        
        water_val = data.get('water', 0)
        if crop_type == 'Padi Sawah (Modern)':
             st.metric("Tinggi Genangan Air", f"{water_val} cm", "Intermittent / Macak-macak")
        else:
             st.metric("Volume Air Siram", f"{water_val} Liter/tanaman", f"Total: {water_val*n_plants/1000:,.0f} m³/hari")

    st.warning(f"💡 **FOKUS UTAMA FASE INI:** {data.get('focus', '-')}")

with tab2:
    st.markdown("#### ✅ Checklist Pekerjaan (Mandor)")
    
    tasks = data.get('tasks', [])
    for t in tasks:
        st.checkbox(f"{t}", key=t)
        
    st.markdown("---")
    st.caption("Pastikan checklist ini diisi setiap hari oleh petugas lapangan.")

# --- FOOTER ---
st.markdown("---")
st.success(f"🚀 **Target Produktivitas:** {config['target_yield_ton_ha']} Ton/Ha ({crop_type})")
