"""
AgriSensa Tech - Kalender Tanam Cerdas
=======================================
Seasonal Planting Calendar with Pest Risk & Price Prediction

Author: Yandri
Date: 2024-12-26
Version: 1.0 (Rule-Based Expert System)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Authentication
from utils.auth import require_auth, show_user_info_sidebar
user = require_auth()
show_user_info_sidebar()

# Page config
st.set_page_config(page_title="Kalender Tanam Cerdas", page_icon="🌦️", layout="wide")

# ==========================================
# KNOWLEDGE BASE: Seasonal Patterns
# ==========================================

# Base Indonesia Seasonal Pattern (Opsi 1)
INDONESIA_SEASONAL_PATTERN = {
    1: {"season": "Hujan", "rainfall_mm": 300, "temp_c": 26, "humidity": 85},
    2: {"season": "Hujan", "rainfall_mm": 280, "temp_c": 26, "humidity": 85},
    3: {"season": "Hujan", "rainfall_mm": 250, "temp_c": 27, "humidity": 80},
    4: {"season": "Transisi_Kemarau", "rainfall_mm": 150, "temp_c": 28, "humidity": 75},
    5: {"season": "Transisi_Kemarau", "rainfall_mm": 120, "temp_c": 29, "humidity": 70},
    6: {"season": "Kemarau", "rainfall_mm": 60, "temp_c": 30, "humidity": 65},
    7: {"season": "Kemarau", "rainfall_mm": 40, "temp_c": 31, "humidity": 60},
    8: {"season": "Kemarau", "rainfall_mm": 50, "temp_c": 31, "humidity": 60},
    9: {"season": "Transisi_Hujan", "rainfall_mm": 100, "temp_c": 30, "humidity": 70},
    10: {"season": "Transisi_Hujan", "rainfall_mm": 150, "temp_c": 29, "humidity": 75},
    11: {"season": "Hujan", "rainfall_mm": 220, "temp_c": 27, "humidity": 80},
    12: {"season": "Hujan", "rainfall_mm": 320, "temp_c": 26, "humidity": 85},
}

# Banyumas Local Adjustment (Opsi 4 - dari pengalaman Pak Yandri)
BANYUMAS_PEST_PATTERN = {
    # Musim Kemarau (Jun-Agu): Hama tinggi
    6: {"thrips": 70, "kutu_kebul": 65, "jamur": 15, "patek": 10, "layu_bakteri": 15},
    7: {"thrips": 85, "kutu_kebul": 80, "jamur": 10, "patek": 10, "layu_bakteri": 10},
    8: {"thrips": 80, "kutu_kebul": 75, "jamur": 15, "patek": 15, "layu_bakteri": 15},
    
    # Transisi ke Hujan (Sep-Okt): DOUBLE TROUBLE!
    9: {"thrips": 65, "kutu_kebul": 60, "jamur": 70, "patek": 75, "layu_bakteri": 70},
    10: {"thrips": 50, "kutu_kebul": 45, "jamur": 80, "patek": 85, "layu_bakteri": 80},
    
    # Musim Hujan (Nov-Mar): Jamur tinggi
    11: {"thrips": 30, "kutu_kebul": 25, "jamur": 85, "patek": 80, "layu_bakteri": 85},
    12: {"thrips": 25, "kutu_kebul": 20, "jamur": 80, "patek": 75, "layu_bakteri": 80},
    1: {"thrips": 20, "kutu_kebul": 20, "jamur": 85, "patek": 80, "layu_bakteri": 85},
    2: {"thrips": 25, "kutu_kebul": 25, "jamur": 80, "patek": 75, "layu_bakteri": 80},
    3: {"thrips": 30, "kutu_kebul": 30, "jamur": 75, "patek": 70, "layu_bakteri": 75},
    
    # Transisi ke Kemarau (Apr-Mei)
    4: {"thrips": 45, "kutu_kebul": 40, "jamur": 50, "patek": 45, "layu_bakteri": 50},
    5: {"thrips": 60, "kutu_kebul": 55, "jamur": 35, "patek": 30, "layu_bakteri": 35},
}

# Price Pattern (dari mock data analysis)
CABAI_PRICE_PATTERN = {
    1: {"base_price": 75000, "multiplier": 1.2, "volatility": 0.15},  # Nataru
    2: {"base_price": 75000, "multiplier": 0.9, "volatility": 0.12},
    3: {"base_price": 75000, "multiplier": 0.85, "volatility": 0.10},
    4: {"base_price": 75000, "multiplier": 0.95, "volatility": 0.12},
    5: {"base_price": 75000, "multiplier": 1.1, "volatility": 0.15},
    6: {"base_price": 75000, "multiplier": 1.3, "volatility": 0.18},
    7: {"base_price": 75000, "multiplier": 1.5, "volatility": 0.20},  # Kemarau puncak
    8: {"base_price": 75000, "multiplier": 1.4, "volatility": 0.18},
    9: {"base_price": 75000, "multiplier": 1.6, "volatility": 0.22},  # Transisi (tertinggi!)
    10: {"base_price": 75000, "multiplier": 1.5, "volatility": 0.20},
    11: {"base_price": 75000, "multiplier": 1.1, "volatility": 0.15},
    12: {"base_price": 75000, "multiplier": 1.3, "volatility": 0.18},  # Nataru
}

# Crop growing days
CROP_GROWING_DAYS = {
    "Cabai Merah": 120,
    "Cabai Rawit": 100,
    "Tomat": 90,
    "Terong": 80,
    "Bawang Merah": 70,
}


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def calculate_harvest_month(plant_month, growing_days):
    """Calculate harvest month from planting month"""
    harvest_month = (plant_month + (growing_days // 30)) % 12
    if harvest_month == 0:
        harvest_month = 12
    return harvest_month


def get_risk_score(month):
    """Get total pest risk score for a month"""
    pests = BANYUMAS_PEST_PATTERN[month]
    # Weighted average (jamur & patek lebih berbahaya)
    total = (pests['thrips'] * 0.15 + 
             pests['kutu_kebul'] * 0.15 + 
             pests['jamur'] * 0.25 + 
             pests['patek'] * 0.25 + 
             pests['layu_bakteri'] * 0.20)
    return round(total, 1)


def get_risk_level(score):
    """Convert risk score to level"""
    if score >= 75:
        return "🔴 Sangat Tinggi", "red"
    elif score >= 60:
        return "🟠 Tinggi", "orange"
    elif score >= 40:
        return "🟡 Sedang", "yellow"
    else:
        return "🟢 Rendah", "green"


def get_price_prediction(month):
    """Get price prediction for harvest month"""
    pattern = CABAI_PRICE_PATTERN[month]
    predicted_price = pattern['base_price'] * pattern['multiplier']
    min_price = predicted_price * (1 - pattern['volatility'])
    max_price = predicted_price * (1 + pattern['volatility'])
    
    return {
        'predicted': round(predicted_price, 0),
        'min': round(min_price, 0),
        'max': round(max_price, 0)
    }


def get_recommendation(risk_score, predicted_price):
    """Get planting recommendation"""
    # Risk-Return Matrix
    if risk_score < 50 and predicted_price > 85000:
        return "✅ SANGAT DIREKOMENDASIKAN", "Risiko rendah, harga tinggi - kondisi ideal!"
    elif risk_score < 60 and predicted_price > 75000:
        return "✅ DIREKOMENDASIKAN", "Risk-reward balance bagus"
    elif risk_score > 75:
        return "❌ TIDAK DIREKOMENDASIKAN", "Risiko gagal panen sangat tinggi"
    elif predicted_price < 60000:
        return "⚠️ KURANG MENGUNTUNGKAN", "Harga rendah, pertimbangkan komoditas lain"
    else:
        return "⚠️ HATI-HATI", "Pertimbangkan mitigasi risiko"


# ==========================================
# MAIN APP
# ==========================================

st.title("🌦️ Kalender Tanam Cerdas")
st.markdown("**Prediksi Risiko Hama & Harga Berdasarkan Pola Musim**")
st.caption("💡 Berbasis pengalaman lapangan & pola musim Indonesia")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Rekomendasi Tanam",
    "📊 Pola Musim & Risiko",
    "💰 Prediksi Harga",
    "📚 Panduan Penggunaan"
])

# ========== TAB 1: REKOMENDASI TANAM ==========
with tab1:
    st.subheader("🎯 Cari Waktu Tanam Optimal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop = st.selectbox(
            "Pilih Komoditas",
            list(CROP_GROWING_DAYS.keys()),
            help="Pilih tanaman yang ingin ditanam"
        )
        
        growing_days = CROP_GROWING_DAYS[crop]
        st.info(f"⏱️ Masa tanam: **{growing_days} hari** (~{growing_days//30} bulan)")
    
    with col2:
        plant_month = st.selectbox(
            "Bulan Tanam",
            range(1, 13),
            format_func=lambda x: datetime(2024, x, 1).strftime('%B'),
            help="Kapan Anda berencana menanam?"
        )
    
    # Calculate harvest month
    harvest_month = calculate_harvest_month(plant_month, growing_days)
    
    st.markdown("---")
    
    # Analysis
    st.subheader(f"📈 Analisis: Tanam {datetime(2024, plant_month, 1).strftime('%B')} → Panen {datetime(2024, harvest_month, 1).strftime('%B')}")
    
    # Get data
    risk_score = get_risk_score(harvest_month)
    risk_level, risk_color = get_risk_level(risk_score)
    price = get_price_prediction(harvest_month)
    recommendation, reason = get_recommendation(risk_score, price['predicted'])
    
    # Display metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.metric(
            "Risiko Hama/Penyakit",
            f"{risk_score}%",
            risk_level
        )
    
    with col_m2:
        st.metric(
            "Prediksi Harga",
            f"Rp {price['predicted']:,.0f}/kg",
            f"±{((price['max']-price['min'])/2):,.0f}"
        )
    
    with col_m3:
        season = INDONESIA_SEASONAL_PATTERN[harvest_month]['season']
        st.metric(
            "Musim Panen",
            season.replace("_", " "),
            f"{INDONESIA_SEASONAL_PATTERN[harvest_month]['rainfall_mm']} mm"
        )
    
    # Recommendation box
    st.markdown("---")
    if "SANGAT DIREKOMENDASIKAN" in recommendation:
        st.success(f"### {recommendation}\n{reason}")
    elif "DIREKOMENDASIKAN" in recommendation:
        st.success(f"### {recommendation}\n{reason}")
    elif "TIDAK DIREKOMENDASIKAN" in recommendation:
        st.error(f"### {recommendation}\n{reason}")
    else:
        st.warning(f"### {recommendation}\n{reason}")
    
    # Detailed breakdown
    with st.expander("🔍 Detail Risiko Hama/Penyakit"):
        pests = BANYUMAS_PEST_PATTERN[harvest_month]
        
        st.markdown("**Tingkat Risiko per Jenis OPT:**")
        
        pest_df = pd.DataFrame({
            'OPT': ['Thrips', 'Kutu Kebul', 'Jamur', 'Patek', 'Layu Bakteri'],
            'Risiko (%)': [pests['thrips'], pests['kutu_kebul'], pests['jamur'], pests['patek'], pests['layu_bakteri']]
        })
        
        fig_pest = px.bar(pest_df, x='OPT', y='Risiko (%)', 
                         title=f"Risiko OPT Bulan {datetime(2024, harvest_month, 1).strftime('%B')}",
                         color='Risiko (%)', color_continuous_scale='Reds')
        st.plotly_chart(fig_pest, use_container_width=True)
        
        # Mitigation advice
        st.markdown("**💡 Saran Mitigasi:**")
        if pests['thrips'] > 60 or pests['kutu_kebul'] > 60:
            st.warning("- **Hama tinggi**: Siapkan insektisida (Imidakloprid, Abamektin)")
        if pests['jamur'] > 60 or pests['patek'] > 60:
            st.warning("- **Jamur tinggi**: Siapkan fungisida (Metalaxyl, Mankozeb)")
        if harvest_month in [9, 10]:
            st.error("- **DOUBLE TROUBLE**: Perlu monitoring ekstra ketat!")


# ========== TAB 2: POLA MUSIM & RISIKO ==========
with tab2:
    st.subheader("📊 Pola Musim & Risiko Sepanjang Tahun")
    
    # Create annual pattern dataframe
    months = list(range(1, 13))
    month_names = [datetime(2024, m, 1).strftime('%b') for m in months]
    
    annual_data = {
        'month': months,
        'month_name': month_names,
        'season': [INDONESIA_SEASONAL_PATTERN[m]['season'] for m in months],
        'rainfall': [INDONESIA_SEASONAL_PATTERN[m]['rainfall_mm'] for m in months],
        'risk_score': [get_risk_score(m) for m in months],
        'price': [get_price_prediction(m)['predicted'] for m in months]
    }
    
    df_annual = pd.DataFrame(annual_data)
    
    # Plot 1: Rainfall pattern
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=df_annual['month_name'],
        y=df_annual['rainfall'],
        name='Curah Hujan',
        marker_color='lightblue'
    ))
    fig1.update_layout(
        title="Pola Curah Hujan Sepanjang Tahun",
        xaxis_title="Bulan",
        yaxis_title="Curah Hujan (mm)",
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Plot 2: Risk heatmap
    st.markdown("### 🔥 Heatmap Risiko Hama/Penyakit")
    
    risk_matrix = []
    for m in months:
        pests = BANYUMAS_PEST_PATTERN[m]
        risk_matrix.append([
            pests['thrips'],
            pests['kutu_kebul'],
            pests['jamur'],
            pests['patek'],
            pests['layu_bakteri']
        ])
    
    fig2 = go.Figure(data=go.Heatmap(
        z=np.array(risk_matrix).T,
        x=month_names,
        y=['Thrips', 'Kutu Kebul', 'Jamur', 'Patek', 'Layu Bakteri'],
        colorscale='Reds',
        text=np.array(risk_matrix).T,
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Risiko (%)")
    ))
    fig2.update_layout(
        title="Pola Risiko OPT Sepanjang Tahun (Banyumas)",
        xaxis_title="Bulan",
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Key insights
    st.info("""
    **💡 Insight Pola Musim:**
    - **Juni-Agustus (Kemarau)**: Risiko hama tinggi (Thrips, Kutu Kebul)
    - **September-Oktober (Transisi)**: **DOUBLE TROUBLE** - Hama + Jamur tinggi!
    - **November-Maret (Hujan)**: Risiko jamur tinggi (Patek, Layu Bakteri)
    """)


# ========== TAB 3: PREDIKSI HARGA ==========
with tab3:
    st.subheader("💰 Prediksi Harga Cabai Merah Sepanjang Tahun")
    
    # Price trend
    fig3 = go.Figure()
    
    fig3.add_trace(go.Scatter(
        x=df_annual['month_name'],
        y=df_annual['price'],
        mode='lines+markers',
        name='Harga Prediksi',
        line=dict(color='green', width=3),
        marker=dict(size=10)
    ))
    
    # Add price range (min-max)
    price_min = [get_price_prediction(m)['min'] for m in months]
    price_max = [get_price_prediction(m)['max'] for m in months]
    
    fig3.add_trace(go.Scatter(
        x=df_annual['month_name'] + df_annual['month_name'][::-1],
        y=price_max + price_min[::-1],
        fill='toself',
        fillcolor='rgba(0,255,0,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Range Harga',
        showlegend=True
    ))
    
    fig3.update_layout(
        title="Tren Harga Cabai Merah (Prediksi)",
        xaxis_title="Bulan Panen",
        yaxis_title="Harga (Rp/kg)",
        height=500
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Price table
    st.markdown("### 📋 Tabel Prediksi Harga")
    
    price_table = []
    for m in months:
        price = get_price_prediction(m)
        price_table.append({
            'Bulan': datetime(2024, m, 1).strftime('%B'),
            'Harga Prediksi': f"Rp {price['predicted']:,.0f}",
            'Min': f"Rp {price['min']:,.0f}",
            'Max': f"Rp {price['max']:,.0f}",
            'Musim': INDONESIA_SEASONAL_PATTERN[m]['season'].replace('_', ' ')
        })
    
    st.dataframe(pd.DataFrame(price_table), use_container_width=True, hide_index=True)
    
    st.success("""
    **💡 Strategi Harga:**
    - **Harga Tertinggi**: September (Rp 120,000/kg) - Transisi, produksi turun
    - **Harga Terendah**: Maret (Rp 64,000/kg) - Hujan, banyak yang tanam
    - **Nataru Bonus**: Desember-Januari (+20-30%)
    """)


# ========== TAB 4: PANDUAN ==========
with tab4:
    st.subheader("📚 Panduan Penggunaan Kalender Tanam Cerdas")
    
    st.markdown("""
    ### 🎯 Cara Menggunakan
    
    1. **Pilih Komoditas** yang ingin ditanam
    2. **Pilih Bulan Tanam** yang direncanakan
    3. **Lihat Analisis**:
       - Risiko hama/penyakit saat panen
       - Prediksi harga saat panen
       - Rekomendasi (GO / HINDARI / HATI-HATI)
    
    ### 🧠 Basis Pengetahuan
    
    Model ini menggunakan **Rule-Based Expert System** yang menggabungkan:
    
    1. **Pola Musim Indonesia** (Opsi 1)
       - Musim Kemarau: Juni-Agustus
       - Musim Hujan: November-Maret
       - Transisi: April-Mei, September-Oktober
    
    2. **Pengalaman Lapangan Banyumas** (Opsi 4)
       - Pola hama/penyakit spesifik lokal
       - Observasi dari praktisi (8000 baglog jamur, 2 ha cabai, dll)
       - Validasi dengan kondisi riil
    
    3. **Analisis Harga Historis**
       - Pola harga dari data BAPANAS
       - Faktor Nataru (Desember-Januari)
       - Supply-demand musiman
    
    ### ⚠️ Disclaimer
    
    - Model ini adalah **alat bantu keputusan**, bukan jaminan
    - Hasil bersifat **estimatif** berdasarkan pola umum
    - Kondisi aktual bisa berbeda (perubahan iklim, outbreak lokal, dll)
    - Selalu lakukan **validasi lapangan** dan **monitoring rutin**
    
    ### 📞 Feedback
    
    Model ini akan terus di-update berdasarkan:
    - Data riil dari user AgriSensa
    - Feedback petani
    - Update pola iklim BMKG
    
    Jika ada saran atau koreksi, silakan hubungi tim AgriSensa!
    """)

# Footer
st.markdown("---")
st.caption("""
💡 **Tips**: Gunakan tab "Pola Musim & Risiko" untuk melihat gambaran tahunan, 
lalu gunakan tab "Rekomendasi Tanam" untuk analisis spesifik rencana tanam Anda.
""")
