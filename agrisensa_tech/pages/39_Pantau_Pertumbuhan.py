import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

from scipy.optimize import curve_fit

# Page config
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Pantau Pertumbuhan Tanaman - AgriSensa",
    page_icon="📏",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






# Constants & Setup
DATA_FILE = "data/growth_journal.csv"

import folium
from streamlit_folium import st_folium

# Add updated path logic for services
import sys

# Add parent directory to path for imports (required for Streamlit Cloud)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.weather_service import WeatherService
weather_service = WeatherService()

# Ensure Data Directory and File Exist
if not os.path.exists('data'):
    os.makedirs('data')

def init_data():
    if not os.path.exists(DATA_FILE):
        # Migrating to include more columns if needed, but keeping core
        df = pd.DataFrame(columns=['tanggal', 'komoditas', 'usia_hst', 'tinggi_cm', 'jumlah_daun', 'gdd_cumulative'])
        df.to_csv(DATA_FILE, index=False)

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            if 'gdd_cumulative' not in df.columns:
                df['gdd_cumulative'] = 0.0
            return df
        except:
            return pd.DataFrame(columns=['tanggal', 'komoditas', 'usia_hst', 'tinggi_cm', 'jumlah_daun', 'gdd_cumulative'])
    return pd.DataFrame(columns=['tanggal', 'komoditas', 'usia_hst', 'tinggi_cm', 'jumlah_daun', 'gdd_cumulative'])

def save_data(tgl, komoditas, hst, tinggi, daun, gdd=0.0):
    df = load_data()
    new_data = pd.DataFrame({
        'tanggal': [tgl],
        'komoditas': [komoditas],
        'usia_hst': [hst],
        'tinggi_cm': [tinggi],
        'jumlah_daun': [daun],
        'gdd_cumulative': [gdd]
    })
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

init_data()

# Header
st.title("📏 Pantau Pertumbuhan Tanaman (Advanced)")
st.markdown("""
<div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 25px;">
    <h3 style="margin:0; color: #4ade80;">Scientific Growth Engine v2.1</h3>
    <p style="margin:0; opacity: 0.8;">Integrated with Biological Logistic Models (Verhulst) and <strong>Automatic Map-Based GDD Tracking</strong>.</p>
</div>
""", unsafe_allow_html=True)

# Profile Data (Standard Scientific Profiles)
# Base Temp (Tb) and Target GDD are sourced from agricultural literature
profiles = {
    # Cereals
    "Padi Inpari": {"max_h": 110, "panen_hst": 115, "growth_rate": 0.07, "Tb": 10, "target_gdd": 1200},
    "Jagung Hibrida": {"max_h": 220, "panen_hst": 105, "growth_rate": 0.08, "Tb": 10, "target_gdd": 1400},
    
    # Vegetables (Leafy & Fruit)
    "Cabai Rawit": {"max_h": 80, "panen_hst": 90, "growth_rate": 0.05, "Tb": 15, "target_gdd": 1800},
    "Tomat": {"max_h": 150, "panen_hst": 85, "growth_rate": 0.08, "Tb": 10, "target_gdd": 1500},
    "Terong": {"max_h": 100, "panen_hst": 90, "growth_rate": 0.06, "Tb": 12, "target_gdd": 1700},
    "Timun": {"max_h": 200, "panen_hst": 60, "growth_rate": 0.10, "Tb": 12, "target_gdd": 900},
    "Sawi": {"max_h": 30, "panen_hst": 35, "growth_rate": 0.15, "Tb": 7, "target_gdd": 600},
    "Kangkung": {"max_h": 35, "panen_hst": 25, "growth_rate": 0.18, "Tb": 10, "target_gdd": 500},
    "Bayam": {"max_h": 30, "panen_hst": 25, "growth_rate": 0.18, "Tb": 10, "target_gdd": 500},
    "Kubis": {"max_h": 40, "panen_hst": 90, "growth_rate": 0.05, "Tb": 7, "target_gdd": 1400},
    "Kacang Panjang": {"max_h": 250, "panen_hst": 60, "growth_rate": 0.09, "Tb": 12, "target_gdd": 1000},
    
    # Tubers & Bulbs
    "Bawang Merah": {"max_h": 45, "panen_hst": 65, "growth_rate": 0.06, "Tb": 10, "target_gdd": 1000},
    "Kentang": {"max_h": 60, "panen_hst": 100, "growth_rate": 0.05, "Tb": 7, "target_gdd": 1500},
    "Ubi Jalar": {"max_h": 40, "panen_hst": 120, "growth_rate": 0.04, "Tb": 12, "target_gdd": 2200},
    
    # Legumes
    "Kedelai": {"max_h": 70, "panen_hst": 85, "growth_rate": 0.07, "Tb": 10, "target_gdd": 1800},
    "Kacang Tanah": {"max_h": 50, "panen_hst": 100, "growth_rate": 0.06, "Tb": 10, "target_gdd": 2000},
    
    # Fruits
    "Melon": {"max_h": 200, "panen_hst": 70, "growth_rate": 0.12, "Tb": 12, "target_gdd": 1100},
    "Semangka": {"max_h": 200, "panen_hst": 80, "growth_rate": 0.10, "Tb": 12, "target_gdd": 1300}
}

# Sidebar Input
with st.sidebar:
    st.header("⚙️ Konfigurasi")
    kom_choice = st.selectbox("Pilih Komoditas", list(profiles.keys()), index=0)
    prof = profiles[kom_choice]
    
    st.divider()
    st.header("📍 Lokasi Lahan (Peta Otomatis)")
    
    # Map for Location selection
    default_lat, default_lon = st.session_state.get('data_lat', -7.15), st.session_state.get('data_lon', 110.14)
    m = folium.Map(location=[default_lat, default_lon], zoom_start=13)
    m.add_child(folium.LatLngPopup())
    
    # Map in sidebar is a bit tight, but let's try
    map_data = st_folium(m, height=250, width=280)
    
    if map_data and map_data.get("last_clicked"):
        lat_sel = map_data["last_clicked"]["lat"]
        lon_sel = map_data["last_clicked"]["lng"]
        # Sync back to session state
        st.session_state['data_lat'] = lat_sel
        st.session_state['data_lon'] = lon_sel
        st.success(f"Lokasi: {lat_sel:.4f}, {lon_sel:.4f}")
    else:
        lat_sel, lon_sel = default_lat, default_lon
        st.info("Pilih lokasi lahan di peta.")

    st.divider()
    st.header("📝 Input Data Harian")
    tgl_catat = st.date_input("Tanggal Pencatatan", datetime.now())
    usia_hst = st.number_input("Usia Tanaman (HST)", min_value=1, value=1)
    tinggi_in = st.number_input("Tinggi Tanaman (cm)", min_value=0.0, value=0.0)
    daun_in = st.number_input("Jumlah Daun (helai)", min_value=0, value=0)
    
    # GDD Calculation helper with automated weather
    st.markdown("---")
    st.markdown("**🌡️ Auto-GDD (Weather Sync)**")
    
    with st.spinner("Mengambil cuaca real-time..."):
        w_data = weather_service.get_weather_forecast(lat_sel, lon_sel)
        if w_data and 'raw_daily' in w_data:
            t_max = w_data['raw_daily'].get('temperature_2m_max', [32.0])[0]
            t_min = w_data['raw_daily'].get('temperature_2m_min', [24.0])[0]
            gdd_today = max(0, (t_max + t_min)/2 - prof['Tb'])
            st.metric("Estimasi Panas (GDD)", f"{gdd_today:.1f} Units", delta=f"{t_max}°C / {t_min}°C")
        else:
            gdd_today = 10.0 # Fallback
            st.warning("Gagal fetch cuaca. Menggunakan estimasi default.")
    
    if st.button("💾 Simpan Data ke Jurnal", type="primary", use_container_width=True):
        # Calculate cumulative GDD from previous entries if exists
        df_temp = load_data()
        df_kom_temp = df_temp[df_temp['komoditas'] == kom_choice]
        prev_gdd = df_kom_temp['gdd_cumulative'].max() if not df_kom_temp.empty else 0.0
        
        save_data(tgl_catat.strftime("%Y-%m-%d"), kom_choice, usia_hst, tinggi_in, daun_in, prev_gdd + gdd_today)
        st.toast(f"Data {kom_choice} berhasil disimpan!", icon="🚀")
        st.rerun()

# Main Layout
st.markdown(f"### 📊 Dashboard Monitoring Scientifik: **{kom_choice}**")
col_main, col_side = st.columns([3, 1])

# --- DATA PROCESSING ---
df = load_data()
df_filtered = df[df['komoditas'] == kom_choice].sort_values(by='usia_hst')

# LOGISTIC FUNCTION FOR CURVE FITTING
def logistic_model(t, K, r, t0):
    return K / (1 + np.exp(-r * (t - t0)))

# Calculate Standard Curve
max_days = prof['panen_hst'] + 15
days_standard = np.arange(1, max_days)
K_std = prof['max_h']
r_std = prof['growth_rate']
t0_std = prof['panen_hst'] / 2
standard_curve = logistic_model(days_standard, K_std, r_std, t0_std)

with col_main:
    fig = go.Figure()
    
    # 1. Trace Standard
    fig.add_trace(go.Scatter(x=days_standard, y=standard_curve, mode='lines', name='Standar Varietas (Ideal)',
                             line=dict(color='rgba(150, 150, 150, 0.4)', dash='dot')))
    
    # 2. Trace Actual Data
    if not df_filtered.empty:
        fig.add_trace(go.Scatter(x=df_filtered['usia_hst'], y=df_filtered['tinggi_cm'], 
                                 mode='lines+markers', name='Data Aktual',
                                 line=dict(color='#22c55e', width=4),
                                 marker=dict(size=10, symbol='circle')))
        
        # 3. SCIENTIFIC PREDICTION (Logistic Fit)
        if len(df_filtered) >= 3:
            try:
                # Fit the model to actual data
                # P0: initial guess [K, r, t0]
                p0 = [prof['max_h'], prof['growth_rate'], prof['panen_hst']/2]
                popt, _ = curve_fit(logistic_model, df_filtered['usia_hst'], df_filtered['tinggi_cm'], p0=p0, bounds=(0, [500, 1, 200]))
                
                K_fit, r_fit, t0_fit = popt
                
                last_hst = df_filtered['usia_hst'].iloc[-1]
                future_days = np.arange(last_hst, prof['panen_hst'] + 10)
                predicted_growth = logistic_model(future_days, K_fit, r_fit, t0_fit)
                
                fig.add_trace(go.Scatter(x=future_days, y=predicted_growth, mode='lines', name='AI Logistic Prediction',
                                         line=dict(color='#f59e0b', width=3, dash='dash')))
            except Exception as e:
                st.warning("⚠️ Fit Matematika Gagal: Memerlukan sebaran data yang lebih representatif.")
                predicted_growth = []
                future_days = []
        else:
            predicted_growth = []
            future_days = []
    else:
        st.info("👋 Belum ada data. Silakan input data harian di sidebar untuk melihat grafik.")
        predicted_growth = []
        future_days = []

    fig.update_layout(title="Analisis Bio-Logistic (Verhulst Model)", 
                      xaxis_title="Hari Setelah Tanam (HST)", yaxis_title="Tinggi (cm)",
                      hovermode="x unified",
                      plot_bgcolor='rgba(0,0,0,0)',
                      paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

    # 4. GDD PROGRESS CHART
    st.subheader("🌡️ Akumulasi Energi Panas (GDD)")
    if not df_filtered.empty:
        fig_gdd = go.Figure()
        fig_gdd.add_trace(go.Scatter(x=df_filtered['usia_hst'], y=df_filtered['gdd_cumulative'],
                                     mode='lines+markers', name='Indeks GDD Aktual',
                                     line=dict(color='#ef4444', width=3)))
        
        # Target GDD line
        fig_gdd.add_hline(y=prof['target_gdd'], line_dash="dash", line_color="red", 
                          annotation_text=f"Target Panen ({prof['target_gdd']} GDD)")
        
        fig_gdd.update_layout(height=300, margin=dict(t=30, b=30), 
                              xaxis_title="HST", yaxis_title="Cumulative GDD")
        st.plotly_chart(fig_gdd, use_container_width=True)
    
    # 5. SCIENTIFIC ADVICE
    st.subheader("🧬 Analisis Fisiologis & Advice")
    if len(df_filtered) >= 2:
        last_p = df_filtered.iloc[-1]
        prev_p = df_filtered.iloc[-2]
        
        h2, t2 = last_p['tinggi_cm'], last_p['usia_hst']
        h1, t1 = prev_p['tinggi_cm'], prev_p['usia_hst']
        
        delta_t = t2 - t1
        if delta_t > 0 and h1 > 0:
            rgr = (np.log(h2) - np.log(h1)) / delta_t
            
            # NAR Proxy: Growth per leaf unit per day
            l2 = last_p['jumlah_daun']
            delta_h = h2 - h1
            nar = (delta_h / delta_t) / l2 if l2 > 0 else 0
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Relative Growth Rate (RGR)", f"{rgr:.4f}", delta=f"{(rgr - prof['growth_rate']):.4f} vs Std")
            c2.metric("Net Assimilation Rate (NAR)", f"{nar:.2f} cm/daun/hr", help="Proxy laju fotosintesis per unit daun.")
            
            # Health Score
            std_h_now = logistic_model(t2, prof['max_h'], prof['growth_rate'], prof['panen_hst']/2)
            health_idx = (h2 / std_h_now) * 100 if std_h_now > 0 else 100
            c3.metric("Indeks Kesehatan Vegetatif", f"{health_idx:.1f}%", delta="Normal" if 90 <= health_idx <= 110 else "Anomali")
            
            # Advice logic & Stages
            st.divider()
            adv_col, stage_col = st.columns([2, 1])
            with adv_col:
                st.markdown("**💡 Advice Scientifik (AI Analysis):**")
                if health_idx < 80:
                    st.error("🚨 **Laju Melambat**: Tanaman menunjukkan defisit biomass. Rekomendasi: Aplikasi KNO3 atau Urea (Vegetatif) untuk bootstrap klorofil.")
                elif health_idx > 120:
                    st.warning("⚠️ **Vigor Berlebih**: Potensi etiolasi atau rebah. Rekomendasi: Kurangi N, berikan P-K tinggi untuk penguatan jaringan.")
                else:
                    st.success("✅ **Pertumbuhan Efisien**: Keseimbangan asimilasi dan respirasi terjaga dengan baik.")
                    
            with stage_col:
                st.markdown("**🎯 Target Phenologi:**")
                current_gdd = last_p['gdd_cumulative']
                if current_gdd < prof['target_gdd'] * 0.3:
                    st.info("🌱 **Fase Vegetatif Awal**")
                elif current_gdd < prof['target_gdd'] * 0.6:
                    st.info("🌿 **Fase Vegetatif Aktif**")
                elif current_gdd < prof['target_gdd'] * 0.8:
                    st.warning("🌸 **Fase Primordia/Bunga**")
                else:
                    st.success("🌾 **Fase Pengisian/Masak**")
    else:
        st.info("Input minimal 2 data pengamatan untuk memunculkan analisis RGR, NAR, dan Indeks Kesehatan.")

    with st.expander("📂 Riwayat Log Data (Advanced)"):
        st.dataframe(df_filtered, use_container_width=True)

with col_side:
    st.subheader("🎯 Prediksi Panen AI")
    
    if not df_filtered.empty:
        current_gdd = df_filtered['gdd_cumulative'].iloc[-1]
        remaining_gdd = max(0, prof['target_gdd'] - current_gdd)
        
        # LOGIC REFINEMENT: Use today's GDD rate for projection (Scientific Engine v2.2)
        # If gdd_today is fetched successfully, use it. Otherwise, use a safe default of 12 GDD/day (Tropical avg)
        projected_rate = gdd_today if gdd_today > 5 else 12.0 
        
        est_days_gdd = int(remaining_gdd / projected_rate) if projected_rate > 0 else 0
        
        st.markdown(f"""
        <div style="text-align: center; padding: 25px; background: #f8fafc; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <p style="margin:0; color: #64748b; font-size: 0.8em; font-weight: bold; text-transform: uppercase;">Estimasi GDD Sisa</p>
            <h2 style="color: #ef4444; margin: 5px 0;">{remaining_gdd:.0f} Units</h2>
            <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 15px 0;">
            <p style="margin:0; color: #64748b; font-size: 0.8em; font-weight: bold; text-transform: uppercase;">Proyeksi Laju: {projected_rate:.1f} / hari</p>
            <h1 style="color: #16a34a; margin: 5px 0;">~{est_days_gdd} Hari</h1>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress Bar GDD
        progress = min(1.0, current_gdd / prof['target_gdd'])
        st.write("")
        st.write(f"Progres Termal: **{progress*100:.1f}%**")
        st.progress(progress)
        
        st.markdown("---")
        st.write("**🛡️ Status Keamanan**")
        # Logic: If current HST > planned but height is low
        # Note: health_idx is calculated in the main column
        try:
            h_idx = health_idx
        except:
            h_idx = 100
            
        if df_filtered['usia_hst'].iloc[-1] > prof['panen_hst'] * 0.8 and h_idx < 80:
            st.error("⚠️ Potensi Gagal Panen Tinggi.")
        else:
            st.success("🟢 Lokasi Aman.")

    else:
        st.info("Input data untuk menghitung kalkulasi GDD dan prediksi panen.")

# Link to Jurnal Harian
st.divider()
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.info("💡 **Tips Ilmiah**: Growing Degree Days (GDD) lebih akurat dari kalender biasa karena memperhitungkan akumulasi panas yang dibutuhkan tanaman untuk mencapai setiap fase phenologi.")
with col_f2:
    if st.button("📓 Buka Jurnal Harian Central"):
        st.switch_page("pages/40_📓_Jurnal_Harian.py")
