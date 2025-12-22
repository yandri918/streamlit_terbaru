
# 🎯 AgriSensa AI Harvest Planner (Global Standard Edition)
# Advanced Decision Support System for Precision Agriculture
# Features: Yield/Profit Optimization, Sustainability Scoring, Risk Analysis, Deep Integration (Modul 6, 18, 25, 26, 27)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
import requests
import sys
import os

# Add updated path logic
from utils.auth import require_auth, show_user_info_sidebar

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_farm_service import get_ai_model, optimize_solution
from services.crop_service import CropService
from services.bapanas_service import BapanasService 
from services.weather_service import WeatherService
from utils.bapanas_constants import PROVINCE_MAPPING # for location mapping

st.set_page_config(page_title="AI Harvest Planner Pro", page_icon="🎯", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# Initialize Services
bapanas_service = BapanasService()
weather_service = WeatherService()

# ==========================================
# 🌳 DATA DICTIONARY (CROP DATABASE)
# ==========================================

# Helper: Categorize crops
all_crops = CropService.get_all_crops()

CROP_DATABASE = {
    "Tanaman Pangan": [
        "Padi (Inpari 32)", "Padi (Ciherang)", "Padi (IR64)", "Padi (Sidenuk)",
        "Jagung Hibrida", "Jagung Manis", "Jagung Pakan",
        "Kedelai (Grobogan)", "Kedelai (Anjasmoro)",
        "Kacang Tanah", "Kacang Hijau", "Ubi Kayu (Singkong)", "Ubi Jalar"
    ],
    "Hortikultura (Sayur)": [
        "Cabai Merah Besar", "Cabai Rawit", "Cabai Keriting",
        "Tomat", "Kentang", "Bawang Merah", "Bawang Putih",
        "Kubis/Kol", "Wortel", "Sawi/Caisim", "Bayam", "Kangkung",
        "Terong", "Timun", "Kacang Panjang", "Brokoli"
    ] + [c for c in all_crops if "Sayur" in c or "Cabai" in c or "Tomat" in c or "Bawang" in c], 
    "Buah-buahan": [
        "Semangka", "Melon", "Pepaya", "Nanas", "Pisang",
        "Jeruk Siam", "Mangga", "Durian", "Alpukat", "Manggis"
    ] + [c for c in all_crops if "Melon" in c],
    "Perkebunan": [
        "Kelapa Sawit", "Kopi Arabika", "Kopi Robusta", 
        "Kakao (Cokelat)", "Tebu", "Karet", "Lada", "Cengkeh", "Jambu Mete"
    ]
}

# De-duplicate lists
for cat in CROP_DATABASE:
    CROP_DATABASE[cat] = sorted(list(set(CROP_DATABASE[cat])))

SOIL_TEXTURES = {
    "Lempung Berpasir (Sandy Loam)": 0.4, 
    "Lempung (Loam)": 0.7, 
    "Lempung Berliat (Clay Loam)": 0.9, 
    "Liat (Clay)": 0.8 
}

# Mapping: Modul 16 Variety Name -> Bapanas Commodity Name Substring
# Crucial for valid price fetching
CROP_TO_BAPANAS_MAP = {
    # Padi / Beras
    "Padi (Inpari 32)": "Beras Premium", 
    "Padi (Ciherang)": "Beras Medium",
    "Padi (IR64)": "Beras Medium", 
    "Padi (Sidenuk)": "Beras Medium",
    
    # Jagung
    "Jagung Hibrida": "Jagung",
    "Jagung Manis": "Jagung",
    "Jagung Pakan": "Jagung",
    
    # Edisi Khusus / Sayur
    "Cabai Merah Besar": "Cabai Merah Keriting", # Approximation
    "Cabai Rawit": "Cabai Rawit Merah",
    "Cabai Keriting": "Cabai Merah Keriting",
    "Bawang Merah": "Bawang Merah",
    "Bawang Putih": "Bawang Putih",
    
    # Kedelai
    "Kedelai (Grobogan)": "Kedelai",
    "Kedelai (Anjasmoro)": "Kedelai",
    
    # Others (Fallback or Manual Estimations if not in Bapanas)
    "Daging Sapi": "Daging Sapi",
    "Telur Ayam": "Telur Ayam",
    "Gula": "Gula Pasir",
    "Minyak": "Minyak Goreng" 
}

PEST_STRATEGIES = {
    "Organic (Nabati)": {"cost_factor": 1.0, "risk_reduction": 0.3, "tox_score": 0, "desc": "Ramah lingkungan, risiko hama moderat"},
    "IPM (Terpadu)": {"cost_factor": 1.5, "risk_reduction": 0.6, "tox_score": 20, "desc": "Seimbang, kimia hanya jika perlu"},
    "Konvensional": {"cost_factor": 2.5, "risk_reduction": 0.8, "tox_score": 60, "desc": "Preventif terjadwal, biaya tinggi"},
    "Agresif (Intensif)": {"cost_factor": 4.0, "risk_reduction": 0.95, "tox_score": 100, "desc": "Sangat mahal, risiko hama minimal, bahaya residu"}
}

# ==========================================
# 🧠 AI ENGINE & LOGIC LAYER
# ==========================================

def calculate_sustainability_score(n_input, p_input, k_input, org_input, yield_produced, pest_strategy):
    """Calculate Sustainability Score (0-100)."""
    # 1. Carbon Logic
    cf_n = 5.0
    cf_p = 2.0
    cf_k = 1.0
    total_carbon = (n_input * cf_n) + (p_input * cf_p) + (k_input * cf_k)
    efficiency_score = min(40, (yield_produced / max(total_carbon, 1)) * 1.5) # Max 40 points
    
    # 2. Pesticide Toxicity Logic
    tox_penalty = PEST_STRATEGIES[pest_strategy]['tox_score'] * 0.4 # Max 40 points penalty
    
    # 3. Organic Bonus Logic
    organic_bonus = min(20, org_input * 2) # Max 20 points
    
    # Final Calculation
    base_score = efficiency_score + organic_bonus + 40 # Base 40
    final_score = base_score - tox_penalty
    
    return int(np.clip(final_score, 0, 100)), total_carbon

def run_monte_carlo_simulation(model, conditions, pest_strategy, n_simulations=500):
    """Simulate yield risks with Monte Carlo."""
    base_rain = conditions[4]
    base_temp = conditions[5]
    
    risk_reduction = PEST_STRATEGIES[pest_strategy]['risk_reduction']
    
    final_predictions = []
    
    for _ in range(n_simulations):
        # Weather randomization
        rain_sim = np.random.normal(base_rain, base_rain * 0.2)
        temp_sim = np.random.normal(base_temp, 2.0)
        
        # Pest Event
        pest_event = np.random.random() < 0.3 
        pest_damage = 0
        if pest_event:
             damage_potential = np.random.uniform(0.2, 0.6) 
             actual_damage = damage_potential * (1 - risk_reduction)
             pest_damage = actual_damage
             
        sim_input = conditions.copy()
        sim_input[4] = rain_sim
        sim_input[5] = temp_sim
        
        pred = model.predict(sim_input.reshape(1, -1))[0]
        final_yield = pred * (1 - pest_damage)
        final_predictions.append(final_yield)

    final_predictions = np.array(final_predictions)
    
    p10 = np.percentile(final_predictions, 10)
    p50 = np.percentile(final_predictions, 50)
    p90 = np.percentile(final_predictions, 90)
    
    return p10, p50, p90, final_predictions

def generate_strategic_insight(weather_data, price_trend, price_val):
    """Combines Price and Weather data for high-level advice"""
    rain_risk = weather_data.get('rain_risk_3d', 'Rendah')
    is_high_price = price_trend == "Naik 📈"
    
    advice = "Netral"
    action = "Lanjutkan SOP standar."
    color = "blue"
    
    if is_high_price and rain_risk == "Rendah":
        advice = "🚀 PELUANG EMAS (Golden Opportunity)"
        action = "Cuaca mendukung dan harga sedang naik. Genjot produksi maksimal!"
        color = "green"
    elif is_high_price and rain_risk == "Tinggi":
        advice = "⚠️ HIGH RISK HIGH REWARD"
        action = "Harga bagus tapi cuaca berisiko. Gunakan varietas tahan air atau perlindungan ekstra."
        color = "orange"
    elif not is_high_price and rain_risk == "Tinggi":
        advice = "⛔ SITUASI TIDAK MENGUNTUNGKAN"
        action = "Harga turun & cuaca buruk. Pertimbangkan menunda tanam untuk efisiensi biaya."
        color = "red"
    elif not is_high_price and rain_risk == "Rendah":
        advice = "🛡️ STRATEGI DEFENSIF"
        action = "Cuaca aman, tapi harga kurang menarik. Fokus pada efisiensi biaya input (pupuk/pestisida)."
        color = "blue"
        
    return advice, action, color

# ==========================================
# 🎨 UI PRESENTATION LAYER
# ==========================================

with st.sidebar:
    st.header("⚙️ Konfigurasi Lahan")
    
    # CROP SELECTION
    category = st.selectbox("Kategori Tanaman", list(CROP_DATABASE.keys()))
    selected_crop = st.selectbox("Komoditas", CROP_DATABASE[category])
    
    # LOCATION (Synced with Modul 27 Logic)
    # Mapping simple province selection for Price API
    province_name = st.selectbox("Provinsi (Untuk Harga)", list(PROVINCE_MAPPING.keys()), index=0)
    province_id = PROVINCE_MAPPING[province_name]
    
    # 1. FETCH PRICE (BAPANAS API)
    with st.spinner("Mengambil harga Bapanas..."):
        # Try to find commodity in fetched data
        price_df = bapanas_service.get_latest_prices(province_id=province_id)
        
        market_price = 0
        market_trend = "Stabil ➖"
        
        if price_df is not None and not price_df.empty:
            # 1. TRY EXACT MAPPING FIRST (Priority)
            bapanas_name = CROP_TO_BAPANAS_MAP.get(selected_crop, "")
            match_row = pd.DataFrame()
            
            if bapanas_name:
                # Filter strictly by the mapped name (substring check)
                match_row = price_df[price_df['commodity'].str.contains(bapanas_name, case=False, na=False)]
            
            # 2. IF NO MAP OR NO MATCH, TRY FUZZY SEARCH (Fallback)
            if match_row.empty:
                match_row = price_df[price_df['commodity'].apply(
                    lambda x: x.lower() in selected_crop.lower() or selected_crop.lower() in x.lower()
                )]
            
            if not match_row.empty:
                market_price = int(match_row.iloc[0]['price'])
                # Simple trend if previous data exists (simulated for now if single point)
                market_trend = "Naik 📈" # Placeholder/Simulated as API V2 gives snapshots
            else:
                 # Fallback if specific commodity not found in Bapanas List (e.g. Durian)
                 market_price = 15000 
                 st.caption(f"ℹ️ Item '{selected_crop}' (Map: {bapanas_name}) tidak ada di Bapanas. Estimasi manual.")
        else:
             market_price = 15000 # Fallback connection error
        
    st.metric("Harga Pasar (Bapanas)", f"Rp {market_price:,} /kg", market_trend)
    
    st.divider()
    
    # 2. FETCH WEATHER (OPEN-METEO VIA SERVICE)
    st.subheader("🌦️ Kondisi Iklim (Real-time)")
    
    # Use Session State location if avail (from Modul 27) or Default
    lat = st.session_state.get('data_lat', -6.2088)
    lon = st.session_state.get('data_lon', 106.8456)
    
    with st.spinner("Mengambil data cuaca..."):
        weather_insight = weather_service.get_weather_forecast(lat, lon)
        
    if weather_insight:
        rain_est = weather_insight['seasonal_rain_est']
        temp = weather_insight['current_temp']
        st.success(f"Lokasi: {lat:.2f}, {lon:.2f}")
        st.info(f"Hujan: {rain_est} mm/musim | Suhu: {temp}°C")
    else:
        rain_est = 2000
        temp = 27.0
        st.error("Gagal ambil cuaca, pakai data default.")
        
    st.divider()
    
    # FARM PARAMETERS
    st.subheader("🧪 Parameter Input")
    target_yield_input = st.number_input("Target (kg/ha)", 4000, 30000, 8000, step=500)
    land_area = st.number_input("Luas (Ha)", 0.1, 100.0, 1.0, step=0.1)
    
    soil_texture_name = st.selectbox("Tekstur Tanah", list(SOIL_TEXTURES.keys()), index=1)
    
    use_organic = st.checkbox("Pupuk Organik", value=True)
    organic_dose = st.slider("Dosis Organik (Ton/ha)", 0.0, 20.0, 5.0, step=0.5) if use_organic else 0.0
    
    pest_strategy = st.select_slider("Strategi Hama", options=list(PEST_STRATEGIES.keys()), value="IPM (Terpadu)")
    
    optimization_strategy = st.radio("Strategi AI:", ["Max Yield", "Max Profit"])
    
    if st.button("🚀 Jalankan Analisis Lengkap", type="primary", use_container_width=True):
        st.session_state['run_analysis_v4'] = True

# MAIN CONTENT
st.title("🎯 AI Harvest Planner: Command Center")
st.markdown(f"**Komoditas:** {selected_crop} | **Lokasi:** {province_name}")

# STRATEGIC INSIGHT BLOCK (NEW)
if weather_insight and market_price > 0:
    st.markdown("### 🧠 AgriSensa Strategic Insight")
    adv_title, adv_desc, adv_color = generate_strategic_insight(weather_insight, market_trend, market_price)
    
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border-left: 6px solid {adv_color}; padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h3 style="margin-top:0; color: {adv_color};">{adv_title}</h3>
        <p style="font-size: 1.1em;">{adv_desc}</p>
        <hr>
        <small>💡 Analisis gabungan: <b>Harga Bapanas</b> (Market Demand) + <b>Open-Meteo</b> (Production Risk)</small>
    </div>
    """, unsafe_allow_html=True)

if 'run_analysis_v4' not in st.session_state:
     st.info("👈 Silakan atur parameter lahan dan klik tombol Jalankan Analisis.")
else:
    with st.spinner("AI mensimulasikan pertumbuhan, pasar, & risiko..."):
        model = get_ai_model()
        
        fixed_params = {
            'texture': SOIL_TEXTURES[soil_texture_name],
            'fixed_org': organic_dose,
            'pest_strategy': pest_strategy,
            'rain': rain_est, # Integrated Data
            'temp': temp      # Integrated Data
        }
        
        mode_str = "Yield" if "Yield" in optimization_strategy else "Profit"
        
        # Optimize
        opt_result = optimize_solution(model, target_yield_input, mode_str, fixed_params, price_per_kg=market_price)
        
        # Reconstruct Condition
        opt_cond = np.array([
            opt_result['n_kg'], 
            opt_result['p_kg'], 
            opt_result['k_kg'], 
            6.5,                     
            fixed_params['rain'],    
            fixed_params['temp'],    
            opt_result['organic_ton'],
            fixed_params['texture'], 
            0.8                      
        ])
        pred_yield = opt_result['predicted_yield']
        pest_cost = opt_result['pest_cost']
        
        sus_score, co2 = calculate_sustainability_score(opt_cond[0], opt_cond[1], opt_cond[2], opt_cond[6], pred_yield, pest_strategy)
        p10, p50, p90, risk_dist = run_monte_carlo_simulation(model, opt_cond, pest_strategy)
        
    # DASHBOARD
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Prediksi Hasil", f"{pred_yield:.0f} kg/ha", f"{(pred_yield/target_yield_input)*100:.0f}% Target")
    k2.metric("Sustainability Score", f"{sus_score}/100", f"{'🌱 Eco-Friendly' if sus_score>70 else '⚠️ Chemical Heavy'}")
    
    # Profit calculation with DYNAMIC Price
    profit_val = (pred_yield * market_price) - ((opt_cond[0]*15000) + (opt_cond[1]*20000) + (opt_cond[2]*18000) + (opt_cond[6]*1000*1000) + pest_cost)
    k3.metric("Est. Profit", f"Rp {profit_val/1e6:.1f} Jt", f"Harga: {market_price}/kg")
    
    k4.metric("Keamanan Hasil (P10)", f"{p10:.0f} kg", "Worst Case Scenario")
    
    st.markdown("---")
    
    t1, t2, t3, t4 = st.tabs(["📋 Resep & Belanja", "🎮 Skenario", "🌍 Sustainability", "⚖️ Neraca Biaya"])
    
    with t1:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("### 💊 Resep Input")
            res_df = pd.DataFrame({
                "Parameter": ["Nitrogen", "Fosfor", "Kalium", "Organik", "Pestisida"],
                "Nilai": [f"{opt_cond[0]:.1f} kg", f"{opt_cond[1]:.1f} kg", f"{opt_cond[2]:.1f} kg", f"{opt_cond[6]:.1f} Ton", pest_strategy],
                "Kategori": ["Kimia", "Kimia", "Kimia", "Alami", "Proteksi"]
            })
            st.dataframe(res_df, hide_index=True, use_container_width=True)
            
            st.divider()
            st.markdown("#### 🛍️ Tindakan Lanjut (Integrasi)")
            
            if st.button("🛒 Beli Pupuk (Katalog Modul 25)", use_container_width=True):
                st.switch_page("pages/25_🧪_Katalog_Pupuk_Harga.py")
            
            if "Organic" in pest_strategy:
                if st.button("🌿 Lihat Resep Nabati (Modul 18)", use_container_width=True):
                    st.switch_page("pages/18_🌿_Pestisida_Nabati.py")
            else:
                if st.button("🔬 Cek Bahan Aktif Aman (Modul 26)", use_container_width=True):
                    st.switch_page("pages/26_🔬_Direktori_Bahan_Aktif.py")
            
        with c2:
            radar_data = pd.DataFrame({
                'r': [
                    opt_cond[0]/350*100, 
                    opt_cond[1]/130*100, 
                    opt_cond[2]/250*100, 
                    PEST_STRATEGIES[pest_strategy]['cost_factor']*25, 
                    opt_cond[6]/20*100 if opt_cond[6] > 0 else 5
                ],
                'theta': ['N', 'P', 'K', 'Proteksi Hama', 'Bahan Organik']
            })
            fig_rad = px.line_polar(radar_data, r='r', theta='theta', line_close=True, range_r=[0,100], title="Profil Input Agronomi")
            fig_rad.update_traces(fill='toself', line_color='#10b981')
            st.plotly_chart(fig_rad, use_container_width=True)

    with t2:
        st.subheader("🎲 Analisis Risiko (Monte Carlo)")
        st.info(f"Strategi **{pest_strategy}** memberikan perlindungan risiko sebesar **{PEST_STRATEGIES[pest_strategy]['risk_reduction']*100:.0f}%** terhadap gagal panen.")
        
        hist_fig = px.histogram(risk_dist, nbins=40, title=f"Distribusi Peluang Hasil (N=500 Simulasi)", 
                               color_discrete_sequence=['#3b82f6'])
        hist_fig.add_vline(x=p10, line_dash="dash", line_color="red", annotation_text="Gagal (P10)")
        hist_fig.add_vline(x=p50, line_dash="solid", line_color="green", annotation_text="Ekspektasi")
        st.plotly_chart(hist_fig, use_container_width=True)

    with t3:
        st.subheader("🌍 Dampak Lingkungan")
        col_env1, col_env2 = st.columns(2)
        with col_env1:
            st.metric("Total Emisi CO2e", f"{co2:.1f} kg/ha")
            st.metric("Toksisitas Pestisida", f"{PEST_STRATEGIES[pest_strategy]['tox_score']}/100", "Indeks Bahaya")
        with col_env2:
            st.warning("Strategi Agresif meningkatkan risiko residu kimia pada produk dan membunuh musuh alami. Di rekomendasikan menggunakan IPM.")
            
    with t4:
        st.subheader("💰 Struktur Biaya")
        costs = {
            "Pupuk Kimia": (opt_cond[0]*15000) + (opt_cond[1]*20000) + (opt_cond[2]*18000),
            "Pupuk Organik": (opt_cond[6]*1000*1000),
            "Pestisida & Hama": pest_cost
        }
        fig_pie = px.pie(values=list(costs.values()), names=list(costs.keys()), title="Breakdown Biaya Operasional")
        st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")
st.caption("© 2025 AgriSensa Intelligence Systems | v3.3 Integrated Price Mapping & Weather")
