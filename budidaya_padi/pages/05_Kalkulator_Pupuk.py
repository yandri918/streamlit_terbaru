"""
 Kalkulator Pupuk - Rice Fertilizer Calculator
Calculate optimal fertilizer requirements for rice cultivation
"""

import streamlit as st
import pandas as pd
import altair as alt

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
    from design_system import apply_design_system, icon, COLORS

st.set_page_config(page_title="Kalkulator Pupuk", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('flask', size='lg')} Kalkulator Pupuk</h1>", unsafe_allow_html=True)
st.markdown("**Hitung kebutuhan pupuk optimal untuk budidaya padi**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([" Input Data", " Hasil", " Rekomendasi"])

with tab1:
    st.header(" Input Data Lahan & Target")
    
    col1, col2 = st.columns(2)
    
    with col1:
        luas_lahan = st.number_input("Luas Lahan (ha)", 0.1, 100.0, 1.0, 0.1)
        target_hasil = st.number_input("Target Hasil (ton/ha)", 1.0, 15.0, 6.0, 0.5)
        varietas = st.selectbox("Varietas", ["IR64", "Ciherang", "Inpari 32", "Inpari 42"])
    
    with col2:
        jenis_tanah = st.selectbox("Jenis Tanah", ["Aluvial", "Latosol", "Podsolik", "Regosol"])
        status_hara = st.selectbox("Status Hara Tanah", ["Rendah", "Sedang", "Tinggi"])
        umur_tanam = st.number_input("Umur Varietas (hari)", 100, 150, 115, 5)
    
    if st.button(" Hitung Kebutuhan Pupuk", type="primary"):
        # Calculation logic
        base_n = 150 if status_hara == "Rendah" else 120 if status_hara == "Sedang" else 100
        base_p = 60 if status_hara == "Rendah" else 50 if status_hara == "Sedang" else 40
        base_k = 80 if status_hara == "Rendah" else 60 if status_hara == "Sedang" else 50
        
        # Adjust for target
        n_need = base_n * (target_hasil / 6.0)
        p_need = base_p * (target_hasil / 6.0)
        k_need = base_k * (target_hasil / 6.0)
        
        # Convert to fertilizer
        urea = n_need / 0.46  # Urea 46% N
        sp36 = p_need / 0.36  # SP-36 36% P2O5
        kcl = k_need / 0.60   # KCl 60% K2O
        npk = 200  # Base NPK Phonska
        
        st.session_state.fertilizer_data = {
            'luas': luas_lahan,
            'target': target_hasil,
            'urea': urea * luas_lahan,
            'sp36': sp36 * luas_lahan,
            'kcl': kcl * luas_lahan,
            'npk': npk * luas_lahan,
            'n_need': n_need,
            'p_need': p_need,
            'k_need': k_need
        }
        st.success(" Perhitungan selesai! Lihat hasil di tab 'Hasil'")

with tab2:
    st.header(" Kebutuhan Pupuk")
    
    if 'fertilizer_data' in st.session_state:
        data = st.session_state.fertilizer_data
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Urea", f"{data['urea']:.0f} kg")
        col2.metric("SP-36", f"{data['sp36']:.0f} kg")
        col3.metric("KCl", f"{data['kcl']:.0f} kg")
        col4.metric("NPK Phonska", f"{data['npk']:.0f} kg")
        
        # Chart
        fert_df = pd.DataFrame({
            'Pupuk': ['Urea', 'SP-36', 'KCl', 'NPK'],
            'Jumlah': [data['urea'], data['sp36'], data['kcl'], data['npk']]
        })
        
        chart = alt.Chart(fert_df).mark_bar().encode(
            x='Pupuk:N',
            y='Jumlah:Q',
            color='Pupuk:N',
            tooltip=['Pupuk', 'Jumlah']
        ).properties(height=300)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Schedule
        st.subheader(" Jadwal Aplikasi")
        schedule = pd.DataFrame({
            'Waktu': ['0 HST', '10-15 HST', '30-35 HST', '50-55 HST'],
            'Urea (kg)': [0, data['urea']*0.4, data['urea']*0.4, data['urea']*0.2],
            'NPK (kg)': [data['npk'], 0, 0, 0],
            'SP-36 (kg)': [data['sp36'], 0, 0, 0]
        })
        st.dataframe(schedule, use_container_width=True, hide_index=True)
    else:
        st.info("Input data di tab pertama")

with tab3:
    st.header(" Rekomendasi Pemupukan")
    st.markdown("""
    ###  Tips Pemupukan Efektif:
    
    1. **Waktu Aplikasi**
       - Pagi hari (7-9 pagi) atau sore (15-17)
       - Hindari saat hujan atau panas terik
    
    2. **Cara Aplikasi**
       - Tabur merata di permukaan air
       - Jarak 5-7 cm dari batang
       - Genangan air 3-5 cm
    
    3. **Pupuk Organik**
       - Tambahkan 2-3 ton/ha kompos
       - Aplikasi saat olah tanah
       - Tingkatkan kesuburan tanah
    
    4. **Monitoring**
       - Amati warna daun
       - Hijau tua = cukup N
       - Kuning = kurang N
    """)
