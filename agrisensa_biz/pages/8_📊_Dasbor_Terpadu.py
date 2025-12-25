# 📊 AgriSensa Command Center (Dasbor Terpadu)
# Executive Dashboard for Farm Management incorporating Financial, Agronomic, and Operational Health.

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="AgriSensa Command Center", page_icon="📡", layout="wide")

# ===== AUTH & CONFIG =====
user = require_auth()
show_user_info_sidebar()

# Custom CSS for Modern Cards
st.markdown("""
<style>
    .kpi-card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 20px;
        border-left: 5px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .kpi-title { font-size: 14px; color: #64748b; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 0.05em; }
    .kpi-value { font-size: 28px; font-weight: 700; color: #1e293b; }
    .kpi-trend { font-size: 14px; margin-top: 5px; }
    .trend-up { color: #10b981; }
    .trend-down { color: #ef4444; }
    .stProgress > div > div > div > div { background-color: #3b82f6; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 📥 DATA INGESTION LAYERS
# ==========================================

def load_data_source(filename):
    """Generic JSON loader with safety"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        # Silent fail or log
        pass
    return []

# Load all relevant data sources
harvest_data = load_data_source("data/harvest_data_streamlit.json")
soil_data = load_data_source("data/npk_analysis_records.json")
market_data = [] # Placeholder for future expansion
tasks_data = [] # Placeholder

# ==========================================
# 🧠 INTELLIGENCE ENGINE (Scoring Logic)
# ==========================================

def calculate_farm_kpis(harvest, soil):
    """
    Advanced Scoring Logic:
    Returns a unified score (0-100) and breakdown by dimension.
    """
    scores = {
        "Financial": 0,    # Revenue, Margin
        "Agronomic": 0,    # Soil Health
        "Operational": 0,  # Data Velocity
        "Resilience": 0    # Diversity, Sustainability (Mock)
    }
    
    metrics = {
        "total_revenue": 0,
        "avg_margin": 0,
        "harvest_count": 0,
        "soil_n_status": "Unknown",
        "soil_ph": 7.0
    }
    
    # 1. Financial Dimension
    if harvest:
        df = pd.DataFrame(harvest)
        metrics['total_revenue'] = df['total_value'].sum() if 'total_value' in df.columns else 0
        metrics['avg_margin'] = df['profit_margin'].mean() if 'profit_margin' in df.columns else 0
        metrics['harvest_count'] = len(df)
        
        # Score Logic: Margin > 30% is ideal (100 pts)
        margin_score = min(100, max(0, metrics['avg_margin'] / 30 * 100))
        # Activity Score: At least 3 harvests for full points
        activity_score = min(100, len(df) * 33) 
        
        scores['Financial'] = (margin_score * 0.7) + (activity_score * 0.3)
    
    # 2. Agronomic Dimension
    if soil:
        latest = soil[-1]
        metrics['soil_n_status'] = latest['analysis'].get('n_status', 'Unknown')
        metrics['soil_ph'] = latest.get('ph', 7.0)
        
        # Score Logic
        n_score = 100 if metrics['soil_n_status'] in ['Sedang', 'Optimal'] else 50
        ph_dev = abs(metrics['soil_ph'] - 6.5) # Deviation from ideal 6.5
        ph_score = max(0, 100 - (ph_dev * 20)) # -20 pts per 1.0 pH deviation
        
        scores['Agronomic'] = (n_score * 0.5) + (ph_score * 0.5)
        
    # 3. Operational Dimension (Data Completeness)
    data_points = 0
    if harvest: data_points += 50
    if soil: data_points += 50
    scores['Operational'] = data_points
    
    # 4. Resilience (Mock / Placeholder)
    # Assumes diversified crops = higher resilience
    if harvest:
        unique_crops = len(set(x.get('commodity', 'Unknown') for x in harvest))
        scores['Resilience'] = min(100, unique_crops * 50) # 2 crops = 100%
    else:
        scores['Resilience'] = 20 # Baseline
        
    # Composite Score (Weighted)
    final_score = (
        scores['Financial'] * 0.4 + 
        scores['Agronomic'] * 0.3 + 
        scores['Operational'] * 0.2 + 
        scores['Resilience'] * 0.1
    )
    
    return final_score, scores, metrics

# Calculate Analysis
overall_score, dim_scores, kpi_metrics = calculate_farm_kpis(harvest_data, soil_data)

# ==========================================
# 🖥️ UI / VISUALIZATION
# ==========================================

st.title("📡 AgriSensa Command Center")
st.caption(f"Last Updated: {datetime.now().strftime('%d %B %Y %H:%M')}")

# --- HERO SECTION: FARM HEALTH PULSE ---
col_pulse, col_radar = st.columns([1, 2])

with col_pulse:
    st.markdown("### ❤️ Farm Health Pulse")
    
    # Dynamic Color Logic
    color = "#10b981" # Green
    status_msg = "Excellent"
    if overall_score < 75: 
        color = "#f59e0b" # Orange
        status_msg = "Good"
    if overall_score < 50: 
        color = "#ef4444" # Red
        status_msg = "Critical"
        
    # Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = overall_score,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': status_msg, 'font': {'size': 24, 'color': color}},
        gauge = {
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 50], 'color': '#fef2f2'},
                {'range': [50, 75], 'color': '#fffbeb'},
                {'range': [75, 100], 'color': '#ecfdf5'}],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': overall_score}}))
    
    fig_gauge.update_layout(height=300, margin=dict(l=20,r=20,t=50,b=20))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_radar:
    st.markdown("### 🕸️ Holistic Assessment (360° View)")
    
    # Radar Data
    df_radar = pd.DataFrame(dict(
        r=[dim_scores['Financial'], dim_scores['Agronomic'], dim_scores['Operational'], dim_scores['Resilience']],
        theta=['Financial<br>(Profit)', 'Agronomic<br>(Soil/Plant)', 'Operational<br>(Data)', 'Resilience<br>(Risk)']
    ))
    
    fig_radar = px.line_polar(df_radar, r='r', theta='theta', line_close=True)
    fig_radar.update_traces(fill='toself', line_color=color)
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        height=300,
        margin=dict(l=40,r=40,t=20,b=20)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# --- KPI CARDS ROW ---
st.markdown("### 📊 Key Performance Indicators")
k1, k2, k3, k4 = st.columns(4)

def kpi_card(col, title, value, subtext, trend="neutral"):
    trend_color = "#64748b"
    if trend == "up": trend_color = "#10b981"
    if trend == "down": trend_color = "#ef4444"
    
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-title">{title}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-trend" style="color: {trend_color};">{subtext}</div>
    </div>
    """, unsafe_allow_html=True)

kpi_card(k1, "Total Revenue", f"Rp {kpi_metrics['total_revenue']/1e6:.1f} M", f"{kpi_metrics['harvest_count']} siklus panen", "up")
kpi_card(k2, "Avg Profit Margin", f"{kpi_metrics['avg_margin']:.1f}%", "Target: >30%", "up" if kpi_metrics['avg_margin']>20 else "down")
kpi_card(k3, "Soil Health (pH)", f"{kpi_metrics['soil_ph']}", "Ideal: 6.0 - 7.0", "neutral")
kpi_card(k4, "Active Modules", "5", "Integrated System", "neutral")

# --- INTELLIGENT INSIGHTS (ACTION ITEMS) ---
st.markdown("---")
st.subheader("🤖 AI Strategic Insights")

col_left, col_right = st.columns([2, 1])

with col_left:  
    # Dynamic Recommendations based on Logic
    if dim_scores['Agronomic'] < 60:
        st.error("🚨 **Critical Issue: Soil Health Degrading**")
        st.write("Analisis menunjukkan penurunan kualitas tanah (pH atau NPK). Segera lakukan uji lab ulang atau aplikasi pembenah tanah (Dolomit/Organik).")
        st.button("Buka Modul Rekomendasi Pupuk", type="primary")
        
    if dim_scores['Financial'] < 50 and kpi_metrics['harvest_count'] > 0:
        st.warning("⚠️ **Profitability Warning**")
        st.write("Margin keuntungan rata-rata di bawah target 20%. Pertimbangkan efisiensi biaya input atau pivot ke varietas bernilai tinggi.")
        
    if dim_scores['Operational'] < 50:
        st.info("ℹ️ **Data Gap Detected**")
        st.write("Sistem kekurangan data historis untuk membuat prediksi akurat. Mulai catat setiap aktivitas harian.")
        
    if overall_score > 80:
        st.success("✅ **Operations Optimization**")
        st.write("Performa pertanian sangat baik! Saatnya memikirkan ekspansi lahan atau investasi teknologi IoT/Drone.")

with col_right:
    # Quick Actions
    st.markdown("**⚡ Quick Actions**")
    with st.expander("Update Data Harian"):
        st.markdown("[📝 Catat Panen Baru](Database_Panen)")
        st.markdown("[🧪 Input Hasil Lab](Peta_Data_Tanah)")
        st.markdown("[💰 Transaksi Keuangan](Analisis_Usaha_Tani)")
        
    with st.expander("Tools Kalkulator"):
        st.markdown("[🧮 Kalkulator Pupuk](Rekomendasi_Terpadu)")
        st.markdown("[💵 Simulasi Kredit](Analisis_Kelayakan_Bisnis)")
        st.markdown("[🔬 Cek Penyakit (BWD)](Rekomendasi_Terpadu)")

# --- FOOTER ---
st.markdown("---")
st.caption("AgriSensa Enterprise v2.0 - Powered by Decision Support System (DSS) Core")
