import streamlit as st
import numpy as np
import pandas as pd
from scipy import stats
import plotly.graph_objects as go

st.set_page_config(page_title="A/B Testing & Stats", page_icon="📊", layout="wide")

st.markdown("# 📊 A/B Testing & Statistics")
st.markdown("### Experimentation Rigor (Bahasa Indonesia)")
st.markdown("Modul ini mencakup fondasi statistik yang diperlukan untuk merancang dan menganalisis eksperimen (A/B Test) secara valid.")

# Sidebar Resources
with st.sidebar:
    st.header("📚 Referensi Belajar")
    st.markdown("""
    **Tools & Kalkulator:**
    - [Evan Miller Sample Size](https://www.evanmiller.org/ab-testing/sample-size.html) - Standar industri.
    - [GPower](https://www.psychologie.hhu.de/arbeitsgruppen/allgemeine-psychologie-und-arbeitspsychologie/gpower) - Software power analysis.
    
    **Materi & Video:**
    - [Udacity - A/B Testing Course](https://www.udacity.com/course/ab-testing--ud257) - Materi Google.
    - [Data Science Dojo - What is A/B Testing](https://www.youtube.com/watch?v=8H6QIsoQ17g)
    - [A/B Testing Guide (Harvard)](https://hbr.org/2017/06/a-refresher-on-ab-testing)
    """)

tab1, tab2 = st.tabs(["🟢 Hypothesis Testing", "🔴 Sample Size Calculator"])

# --- HYPOTHESIS TESTING ---
with tab1:
    st.header("🟢 Uji Hipotesis (Hypothesis Testing)")
    
    st.markdown("""
    ### 📚 Materi Singkat
    1.  **Null Hypothesis ($H_0$)**: Tidak ada perbedaan efek (misal: Obat A = Obat B).
    2.  **Alternative Hypothesis ($H_1$)**: Ada perbedaan efek.
    3.  **P-Value**: Probabilitas melihat data seperti ini (atau lebih ekstrim) JIKA $H_0$ benar.
        -   Jika P-Value < $\\alpha$ (biasanya 0.05), kita tolak $H_0$.
    """)
    
    st.subheader("🧪 T-Test Simulator")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Grup Kontrol (A)**")
        mean_a = st.number_input("Rata-rata (Mean) A", value=10.0)
        std_a = st.number_input("Standar Deviasi A", value=2.0)
        n_a = st.number_input("Jumlah Sampel A", value=100, step=10)
    
    with col2:
        st.markdown("**Grup Perlakuan (B)**")
        mean_b = st.number_input("Rata-rata (Mean) B", value=10.5)
        std_b = st.number_input("Standar Deviasi B", value=2.0)
        n_b = st.number_input("Jumlah Sampel B", value=100, step=10)
    
    alpha = st.slider("Significance Level ($\\alpha$)", 0.01, 0.10, 0.05, 0.01)
    
    if st.button("Jalankan T-Test"):
        # Generate dummy data for simulation visualization
        np.random.seed(42)
        data_a = np.random.normal(mean_a, std_a, n_a)
        data_b = np.random.normal(mean_b, std_b, n_b)
        
        # Calculate T-Stat and P-Value
        t_stat, p_val = stats.ttest_ind(data_a, data_b)
        
        st.write("---")
        st.write(f"**T-Statistic**: {t_stat:.4f}")
        st.write(f"**P-Value**: {p_val:.4f}")
        
        if p_val < alpha:
            st.success(f"✅ **Hasil Signifikan!** (P-Value < {alpha}) \n\nKita menolak $H_0$. Ada perbedaan statistik yang signifikan antara Grup A dan B.")
        else:
            st.warning(f"⚠️ **Tidak Signifikan** (P-Value >= {alpha}) \n\nKita gagal menolak $H_0$. Tidak cukup bukti untuk mengatakan ada perbedaan.")
            
        # Visualization
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=data_a, name='Kontrol (A)', opacity=0.75))
        fig.add_trace(go.Histogram(x=data_b, name='Perlakuan (B)', opacity=0.75))
        fig.update_layout(barmode='overlay', title="Distribusi Sampling (Simulasi)")
        st.plotly_chart(fig)

# --- SAMPLE SIZE CALCULATOR ---
with tab2:
    st.header("🔴 Sample Size Calculator")
    
    st.markdown("""
    ### 📚 Materi Singkat
    Menghitung ukuran sampel SEBELUM eksperimen sangat krusial untuk menghindari **Underpowered Tests** (gagal mendeteksi efek yang sebenarnya ada).
    
    Faktor yang mempengaruhi ukuran sampel:
    1.  **Baseline Conversion Rate**: Konversi saat ini.
    2.  **Minimum Detectable Effect (MDE)**: Peningkatan minimum yang ingin dideteksi (misal: naik 2%).
    3.  **Power ($1 - \\beta$)**: Probabilitas mendeteksi efek JIKA efek itu ada (biasanya 80%).
    4.  **Significance Level ($\\alpha$)**: Probabilitas False Positive (biasanya 5%).
    """)
    
    st.subheader("🧮 Kalkulator Ukuran Sampel (Formula Evan Miller)")
    
    baseline_cr = st.number_input("Baseline Conversion Rate (%)", value=20.0, step=1.0) / 100
    mde = st.number_input("Minimum Detectable Effect / Lift (%) relative", value=10.0, step=1.0) / 100
    power = st.slider("Power (%)", 70, 99, 80) / 100
    sig_level = st.slider("Significance Level (%)", 1, 10, 5) / 100
    
    if st.button("Hitung Ukuran Sampel"):
        # Calculate standardized effect size (Cohen's h equivalent approximation for proportions)
        # Using simple standard normal approximation for two proportions
        
        p1 = baseline_cr
        p2 = baseline_cr * (1 + mde)
        
        # Pooled probability
        p_pool = (p1 + p2) / 2
        
        # Z-scores
        z_alpha = stats.norm.ppf(1 - sig_level / 2)
        z_beta = stats.norm.ppf(power)
        
        # Formula: n = (Z_alpha*sqrt(2*p_pool*(1-p_pool)) + Z_beta*sqrt(p1*(1-p1) + p2*(1-p2)))^2 / (p2 - p1)^2
        # Adapted for streamlit display
        
        sd1 = np.sqrt(2 * p_pool * (1 - p_pool))
        sd2 = np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
        
        n_per_variant = ((z_alpha * sd1 + z_beta * sd2)**2) / ((p2 - p1)**2)
        n_per_variant = int(np.ceil(n_per_variant))
        
        st.info(f"Untuk mendeteksi kenaikan dari **{p1:.1%}** ke **{p2:.1%}**:")
        st.markdown(f"### Anda butuh **{n_per_variant:,}** visitor per varian.")
        st.markdown(f"Total traffic yang dibutuhkan: **{n_per_variant * 2:,}** visitor.")
        
        st.warning("**Catatan**: Ini menggunakan pendekatan aproksimasi normal standar (serupa dengan Evan Miller Chi-Sq approximation).")
