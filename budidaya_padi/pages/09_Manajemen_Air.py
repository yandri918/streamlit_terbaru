"""
 Manajemen Air Padi - Water Management
Calculator for Intermittent Irrigation (AWD - Alternate Wetting and Drying)
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

st.set_page_config(page_title="Manajemen Air", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('tint', size='lg')} Manajemen Air</h1>", unsafe_allow_html=True)
st.markdown("**Pengelolaan air irigasi padi sawah (System of Rice Intensification / AWD)**")
st.markdown("---")

# Information Section
with st.expander(" Apa itu Pengairan Berselang (Intermittent Irrigation)?", expanded=True):
    st.markdown("""
    **Pengairan Berselang (Alternate Wetting and Drying / AWD)** adalah teknik pengaturan air sawah 
    dimana lahan dikeringkan dan digenangi secara bergantian.
    
    **Manfaat:**
    1.  Hemat air irigasi hingga 30%
    2.  Akar mendapatkan oksigen lebih baik (aerasi)
    3.  Batang lebih kokoh, mengurangi risiko rebah
    4.  Mengurangi populasi hama (wereng keong mas)
    5.  Mengurangi emisi gas metana
    """)

# Calculator Section
st.header(" Kalkulator Kebutuhan Air")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Lahan")
    luas_lahan = st.number_input("Luas Lahan (m²)", min_value=100, value=1000, step=100)
    umur_tanaman = st.slider("Umur Tanaman (HST - Hari Setelah Tanam)", 0, 120, 30)
    jenis_tanah = st.selectbox("Jenis Tanah", [
        "Lempung Berpasir (Poros, butuh banyak air)",
        "Lempung (Sedang)",
        "Lempung Berliat (Tahan air)"
    ])
    musim = st.selectbox("Musim", ["Hujan", "Kemarau"])

with col2:
    st.subheader("Rekomendasi Tinggi Air")
    
    status_air = ""
    rekomendasi_cm = 0
    fase = ""
    tips = ""
    
    # Logic for water recommendation based on stage
    if umur_tanaman <= 10:
        fase = "Fase Pemulihan & Perakaran (0-10 HST)"
        status_air = "Basah / Macak-macak"
        rekomendasi_cm = 2  # 2-3 cm
        tips = "Jaga tanah tetap basah tapi tidak tergenang dalam agar akar cepat pulih. Waspada keong mas."
        
    elif 10 < umur_tanaman <= 40:
        fase = "Fase Pembentukan Anakan (10-40 HST)"
        status_air = "Intermittent / Berselang"
        rekomendasi_cm = 0  # 0-5 cm intermittent
        tips = "Lakukan pengeringan berkala (5 hari genang, 2 hari kering) untuk merangsang anakan. Keringkan saat pemupukan."
        
    elif 40 < umur_tanaman <= 60:
        fase = "Fase Bunting / Primordia (40-60 HST)"
        status_air = "Tergenang"
        rekomendasi_cm = 5  # 5-7 cm
        tips = "Tanaman butuh banyak air untuk pembentukan malai. JANGAN SAMPAI KERING! Stress air fase ini akan menurunkan hasil drastis."
        
    elif 60 < umur_tanaman <= 90:
        fase = "Fase Pembungaan & Pengisian (60-90 HST)"
        status_air = "Tergenang Dangkal"
        rekomendasi_cm = 3  # 3-5 cm
        tips = "Pertahankan air mencukupi. Kekurangan air menyebabkan gabah hampa."
        
    elif 90 < umur_tanaman <= 105:
        fase = "Fase Pemasakan (90-105 HST)"
        status_air = "Macak-macak"
        rekomendasi_cm = 1  # 0-1 cm
        tips = "Kurangi air perlahan untuk mempercepat pematangan gabah."
        
    else:  # > 105
        fase = "Fase Panen (>105 HST)"
        status_air = "Kering Total"
        rekomendasi_cm = 0
        tips = "Keringkan total 10-14 hari sebelum panen untuk memudahkan panen dan meningkatkan kualitas gabah."

    # Display Result
    st.info(f"**Fase:** {fase}")
    st.metric("Target Tinggi Air", f"{rekomendasi_cm} cm", f"{status_air}")
    st.warning(f" **Tips:** {tips}")

# Visualization
st.markdown("---")
st.header(" Jadwal Pengairan Satu Musim")

# Generate Data for Chart
schedule_data = []
for d in range(0, 121, 5):
    h = 0
    s_fase = ""
    if d <= 10: h=2; s_fase="Awal"
    elif d <= 40: h=3; s_fase="Anakan (Intermittent)" # Average for chart
    elif d <= 60: h=7; s_fase="Bunting (Max)"
    elif d <= 90: h=5; s_fase="Pengisian"
    elif d <= 100: h=1; s_fase="Pemasakan"
    else: h=0; s_fase="Panen"
    
    schedule_data.append({"HST": d, "Tinggi Air (cm)": h, "Fase": s_fase})

df_schedule = pd.DataFrame(schedule_data)

# Altair Chart
chart = alt.Chart(df_schedule).mark_area(
    line={'color': '#2196F3'},
    color=alt.Gradient(
        gradient='linear',
        stops=[alt.GradientStop(color='white', offset=0),
               alt.GradientStop(color='#2196F3', offset=1)],
        x1=1, x2=1, y1=1, y2=0
    )
).encode(
    x=alt.X('HST', title='Umur Tanaman (Hari)'),
    y=alt.Y('Tinggi Air (cm)', title='Rekomendasi Tinggi Air (cm)'),
    tooltip=['HST', 'Tinggi Air (cm)', 'Fase']
).properties(
    title='Profil Ketinggian Air Ideal Sepanjang Musim',
    height=300
)

st.altair_chart(chart, use_container_width=True)

# Volume Calculator
st.markdown("---")
st.subheader(" Estimasi Volume Air Irigasi")

vol_m3 = (luas_lahan * (rekomendasi_cm / 100))
# Add factor for soil absorption/evaporation
factor = 1.5 if "Berpasir" in jenis_tanah else 1.2
if musim == "Kemarau": factor += 0.3

vol_total = vol_m3 * factor

st.write(f"Untuk mencapai genangan **{rekomendasi_cm} cm** di lahan **{luas_lahan} m²** ({jenis_tanah}, {musim}):")
col_vol1, col_vol2 = st.columns(2)
with col_vol1:
    st.metric("Volume Air Netto", f"{vol_m3:.1f} m³", "Air di permukaan")
with col_vol2:
    st.metric("Volume Air Bruto (Estimasi)", f"{vol_total:.1f} m³", "+ Serapan tanah & evaporasi")

st.caption("*Perhitungan bruto adalah estimasi kasar, tergantung kondisi drainase dan cuaca real-time.*")
