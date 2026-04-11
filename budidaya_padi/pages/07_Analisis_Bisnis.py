"""
 Analisis Bisnis - Business Analysis for Rice Farming
Profitability, ROI, and financial analysis
"""

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

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

st.set_page_config(page_title="Analisis Bisnis", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('chart-line', size='lg')} Analisis Bisnis</h1>", unsafe_allow_html=True)
st.markdown("**Analisis kelayakan usaha dan profitabilitas**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([" Input", " Analisis", " Proyeksi"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Investasi & Biaya")
        investasi_awal = st.number_input("Investasi Awal (Rp)", 0, 100000000, 10000000, 1000000)
        biaya_produksi = st.number_input("Biaya Produksi/ha (Rp)", 0, 100000000, 15000000, 500000)
        luas_lahan = st.number_input("Luas Lahan (ha)", 0.1, 100.0, 1.0, 0.1)
    
    with col2:
        st.subheader("Pendapatan")
        produktivitas = st.number_input("Produktivitas (ton/ha)", 1.0, 15.0, 6.0, 0.5)
        harga_jual = st.number_input("Harga Jual (Rp/kg)", 3000, 10000, 5500, 100)
        siklus_per_tahun = st.number_input("Siklus/Tahun", 1, 3, 2, 1)
    
    if st.button(" Analisis", type="primary"):
        # Calculations
        total_biaya = biaya_produksi * luas_lahan
        total_produksi = produktivitas * luas_lahan * 1000
        total_pendapatan = total_produksi * harga_jual
        keuntungan = total_pendapatan - total_biaya
        roi = (keuntungan / total_biaya * 100) if total_biaya > 0 else 0
        
        # Annual
        keuntungan_tahunan = keuntungan * siklus_per_tahun
        payback = investasi_awal / keuntungan_tahunan if keuntungan_tahunan > 0 else 0
        
        st.session_state.business_data = {
            'investasi': investasi_awal,
            'biaya': total_biaya,
            'pendapatan': total_pendapatan,
            'keuntungan': keuntungan,
            'roi': roi,
            'keuntungan_tahunan': keuntungan_tahunan,
            'payback': payback,
            'siklus': siklus_per_tahun
        }
        st.success(" Analisis selesai!")

with tab2:
    st.header(" Hasil Analisis")
    
    if 'business_data' in st.session_state:
        data = st.session_state.business_data
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Biaya", f"Rp {data['biaya']:,.0f}")
        col2.metric("Pendapatan", f"Rp {data['pendapatan']:,.0f}")
        col3.metric("Keuntungan", f"Rp {data['keuntungan']:,.0f}")
        col4.metric("ROI", f"{data['roi']:.1f}%")
        
        st.markdown("---")
        
        # Profitability
        st.subheader(" Analisis Profitabilitas")
        
        if data['roi'] > 50:
            st.success(f" Sangat Menguntungkan - ROI {data['roi']:.1f}%")
        elif data['roi'] > 30:
            st.success(f" Menguntungkan - ROI {data['roi']:.1f}%")
        elif data['roi'] > 10:
            st.warning(f" Cukup Menguntungkan - ROI {data['roi']:.1f}%")
        else:
            st.error(f" Kurang Menguntungkan - ROI {data['roi']:.1f}%")
        
        col_pay1, col_pay2 = st.columns(2)
        col_pay1.metric("Keuntungan/Tahun", f"Rp {data['keuntungan_tahunan']:,.0f}")
        col_pay2.metric("Payback Period", f"{data['payback']:.1f} tahun")
        
        # Chart
        comparison_df = pd.DataFrame({
            'Kategori': ['Biaya', 'Pendapatan', 'Keuntungan'],
            'Nilai': [data['biaya'], data['pendapatan'], data['keuntungan']]
        })
        
        chart = alt.Chart(comparison_df).mark_bar().encode(
            x='Kategori:N',
            y='Nilai:Q',
            color='Kategori:N',
            tooltip=['Kategori', 'Nilai']
        ).properties(height=300)
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Input data di tab pertama")

with tab3:
    st.header(" Proyeksi 5 Tahun")
    
    if 'business_data' in st.session_state:
        data = st.session_state.business_data
        
        # Projection
        years = list(range(1, 6))
        cumulative = []
        running_total = -data['investasi']
        
        for year in years:
            running_total += data['keuntungan_tahunan']
            cumulative.append(running_total)
        
        proj_df = pd.DataFrame({
            'Tahun': years,
            'Keuntungan Kumulatif': cumulative
        })
        
        chart = alt.Chart(proj_df).mark_line(point=True).encode(
            x='Tahun:O',
            y='Keuntungan Kumulatif:Q',
            tooltip=['Tahun', 'Keuntungan Kumulatif']
        ).properties(title='Proyeksi Keuntungan Kumulatif', height=300)
        
        st.altair_chart(chart, use_container_width=True)
        
        st.dataframe(proj_df.style.format({'Keuntungan Kumulatif': 'Rp {:,.0f}'}), 
                    use_container_width=True, hide_index=True)
    else:
        st.info("Input data di tab pertama")

st.markdown("---")
st.info(" Analisis ini bersifat estimasi. Hasil aktual dapat bervariasi tergantung kondisi lapangan.")
