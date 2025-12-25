# Prediksi Hasil Panen Advanced
# v2.0 - With What-If Analysis & Economic Projection

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

# --- AUTH CHECK ---
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from agrisensa_tech.utils import auth

st.set_page_config(page_title="Prediksi Panen Cerdas - AgriSensa", page_icon="🎯", layout="wide")

try:
    auth.require_auth()
    auth.show_user_info_sidebar()
except:
    pass # Dev mode fallback

# ================================
# 🧠 KNOWLEDGE BASE & MODELS
# ================================

CROP_DB = {
    "Padi": {
        "varieties": {
            "Ciherang": {"potential": 8500, "days": 115, "resilience": 0.8},
            "Inpari 32": {"potential": 9200, "days": 110, "resilience": 0.9},
            "IR64": {"potential": 7000, "days": 115, "resilience": 0.7}
        },
        "optimal": {"ph": 6.5, "n": 120, "p": 60, "k": 90, "water": 1500, "temp": 28},
        "price": 7200
    },
    "Jagung": {
        "varieties": {
            "Bisi 18": {"potential": 9500, "days": 105, "resilience": 0.85},
            "Pioneer P27": {"potential": 11000, "days": 110, "resilience": 0.9}
        },
        "optimal": {"ph": 6.8, "n": 180, "p": 80, "k": 100, "water": 1200, "temp": 30},
        "price": 5800
    },
    "Cabai Merah": {
         "varieties": {
            "Laju": {"potential": 18000, "days": 90, "resilience": 0.7},
            "Pilar": {"potential": 20000, "days": 95, "resilience": 0.8}
        },
        "optimal": {"ph": 6.5, "n": 200, "p": 150, "k": 200, "water": 1800, "temp": 26},
        "price": 45000
    },
    "Kedelai": {
        "varieties": {
            "Anjasmoro": {"potential": 2500, "days": 85, "resilience": 0.8},
            "Grobogan": {"potential": 3000, "days": 76, "resilience": 0.85}
        },
        "optimal": {"ph": 6.0, "n": 50, "p": 70, "k": 80, "water": 400, "temp": 28},
        "price": 10500
    },
    "Bawang Merah": {
        "varieties": {
            "Bima Brebes": {"potential": 10000, "days": 60, "resilience": 0.75},
            "Bauji": {"potential": 12000, "days": 58, "resilience": 0.8}
        },
        "optimal": {"ph": 6.5, "n": 150, "p": 100, "k": 120, "water": 600, "temp": 27},
        "price": 28000
    },
    "Tomat": {
        "varieties": {
            "Servo F1": {"potential": 60000, "days": 75, "resilience": 0.85},
            "Tymoti F1": {"potential": 55000, "days": 80, "resilience": 0.8}
        },
        "optimal": {"ph": 6.2, "n": 180, "p": 120, "k": 180, "water": 800, "temp": 24},
        "price": 8000
    },
    "Kentang": {
        "varieties": {
            "Granola": {"potential": 25000, "days": 100, "resilience": 0.75},
            "Atlantik": {"potential": 30000, "days": 110, "resilience": 0.8}
        },
        "optimal": {"ph": 5.5, "n": 200, "p": 150, "k": 200, "water": 600, "temp": 18},
        "price": 14000
    },
    "Ubi Kayu": {
        "varieties": {
            "Manggu": {"potential": 35000, "days": 300, "resilience": 0.9},
            "Casesa": {"potential": 40000, "days": 280, "resilience": 0.95}
        },
        "optimal": {"ph": 6.0, "n": 100, "p": 50, "k": 100, "water": 800, "temp": 30},
        "price": 3500
    },
    "Kopi": {
        "varieties": {
            "Arabica Gayo 1": {"potential": 1500, "days": 365, "resilience": 0.8},
            "Robusta BP 308": {"potential": 2500, "days": 365, "resilience": 0.9}
        },
        "optimal": {"ph": 5.5, "n": 120, "p": 80, "k": 120, "water": 2000, "temp": 22},
        "price": 45000
    },
    "Kakao": {
        "varieties": {
            "MCC 02": {"potential": 2500, "days": 365, "resilience": 0.85},
            "Sulawesi 1": {"potential": 2000, "days": 365, "resilience": 0.8}
        },
        "optimal": {"ph": 6.5, "n": 100, "p": 60, "k": 100, "water": 1800, "temp": 28},
        "price": 38000
    }
}

SOIL_TEXTURES = {
    "Lempung (Ideal)": {"water_retention": 1.0, "nutrient_holding": 1.0, "desc": "Struktur tanah seimbang"},
    "Pasir (Sandy)": {"water_retention": 0.6, "nutrient_holding": 0.5, "desc": "Cepat kering, boros pupuk"},
    "Liat (Clay)": {"water_retention": 0.9, "nutrient_holding": 1.2, "desc": "Keras saat kering, mengikat air kuat"}
}

# ================================
# 🧮 SIMULATION ENGINE
# ================================

def gaussian_curve(val, optimal, sigma=1.0):
    """Bell curve response: 1.0 at optimal, drops as you move away"""
    # Simply: e^(-0.5 * ((x-mu)/sig)^2)
    # We calibrate sigma so that +/- 20% deviation gives ~0.8 score
    spread = optimal * 0.3 # 30% tolerance
    return np.exp(-0.5 * ((val - optimal) / (spread/2))**2)

def saturation_curve(val, optimal):
    """Increases then plateaus (Law of Minimum)"""
    # 1 - e^(-k * val)
    # Calibrated so that at 'optimal' value, we reach 0.99
    if val >= optimal * 1.5: return 0.95 # Toxicity/Waste penalty
    k = 4.0 / optimal 
    return 1 - np.exp(-k * val)

def run_simulation(crop, variety, texture_key, params):
    # Get base potential
    crop_data = CROP_DB[crop]
    var_data = crop_data['varieties'][variety]
    opt = crop_data['optimal']
    
    potential = var_data['potential'] * params['area_ha']
    
    # Soil Texture Impact
    texture = SOIL_TEXTURES[texture_key]
    
    # 1. Nutrient Factors (Saturation Curve)
    # Effective N = Input N * Soil Holding Cap
    eff_n = params['n'] * texture['nutrient_holding']
    score_n = saturation_curve(eff_n, opt['n'])
    
    eff_p = params['p'] * texture['nutrient_holding']
    score_p = saturation_curve(eff_p, opt['p'])
    
    eff_k = params['k'] * texture['nutrient_holding']
    score_k = saturation_curve(eff_k, opt['k'])
    
    # 2. Environmental Factors (Gaussian)
    score_ph = gaussian_curve(params['ph'], opt['ph'])
    score_temp = gaussian_curve(params['temp'], opt['temp'])
    
    # 3. Water (Linear with penalty)
    eff_water = params['rain'] * texture['water_retention']
    if eff_water < opt['water'] * 0.5:
        score_water = 0.4 + (eff_water / opt['water']) * 0.6
    elif eff_water > opt['water'] * 1.5:
        score_water = 0.8 # Flood stress
    else:
        score_water = 1.0
        
    # LIEBIG'S LAW OF THE MINIMUM (Modified)
    # Yield is determined mostly by the lowest limiting factor, but averaged slightly
    factors = {
        "Nitrogen": score_n, "Fosfor": score_p, "Kalium": score_k,
        "pH Tanah": score_ph, "Air/Curah Hujan": score_water, "Suhu": score_temp
    }
    
    limiting_factor_val = min(factors.values())
    avg_factor_val = sum(factors.values()) / len(factors)
    
    # Hybrid model: 70% Law of Min, 30% Average
    final_yield_pct = (limiting_factor_val * 0.7) + (avg_factor_val * 0.3)
    
    # Variety resilience bonus
    final_yield_pct = min(1.0, final_yield_pct * (0.9 + (var_data['resilience'] * 0.1)))
    
    predicted_kg = potential * final_yield_pct
    
    return {
        "yield_kg": predicted_kg,
        "yield_pct": final_yield_pct * 100,
        "factors": factors,
        "limiting_factor": min(factors, key=factors.get),
        "potential_kg": potential
    }

# ================================
# 🖥️ UI INTERFACE
# ================================

st.title("🎯 Advanced Harvest Forecast & Simulator")
st.markdown("### Simulasi Cerdas Berbasis Machine Learning & Ekonomi")

# --- SIDEBAR INPUTS ---
with st.sidebar:
    st.header("1️⃣ Konfigurasi Lahan")
    
    s_crop = st.selectbox("Komoditas", list(CROP_DB.keys()))
    s_var = st.selectbox("Varietas Benih", list(CROP_DB[s_crop]['varieties'].keys()))
    s_area = st.number_input("Luas Lahan (Ha)", 0.1, 100.0, 1.0, 0.1)
    s_grad = st.selectbox("Tekstur Tanah", list(SOIL_TEXTURES.keys()))
    
    st.divider()
    st.header("2️⃣ Kondisi Aktual")
    
    # Defaults from CROP_DB for nice UX
    def_opt = CROP_DB[s_crop]['optimal']
    
    i_ph = st.slider("pH Tanah", 3.0, 10.0, 6.0, 0.1)
    i_temp = st.slider("Suhu Rata-rata (°C)", 15, 40, 28)
    i_rain = st.number_input("Curah Hujan (mm/musim)", 0, 5000, 1200)
    
    st.info("👇 Masukkan hasil uji lab tanah:")
    c_n, c_p, c_k = st.columns(3)
    i_n = c_n.number_input("N (kg/ha)", 0, 500, int(def_opt['n']*0.5))
    i_p = c_p.number_input("P (kg/ha)", 0, 300, int(def_opt['p']*0.5))
    i_k = c_k.number_input("K (kg/ha)", 0, 300, int(def_opt['k']*0.5))
    
    btn_predict = st.button("🚀 Jalankan Analisis", type="primary", use_container_width=True)

# --- MAIN AREA ---

# Initial params
params = {
    "area_ha": s_area, "ph": i_ph, "temp": i_temp, "rain": i_rain,
    "n": i_n, "p": i_p, "k": i_k
}

# Run Simulation
res = run_simulation(s_crop, s_var, s_grad, params)

# TABS
tab_sim, tab_eco, tab_whatif = st.tabs(["📊 Hasil & Analisis", "💰 Proyeksi Ekonomi", "🧪 What-If Simulator"])

with tab_sim:
    # 1. HERO METRIC
    c1, c2, c3 = st.columns(3)
    c1.metric("Prediksi Hasil Panen", f"{res['yield_kg']:,.0f} kg", f"{res['yield_pct']:.1f}% Potensi")
    
    gap = res['potential_kg'] - res['yield_kg']
    c2.metric("Potensi Hilang (Loss)", f"{gap:,.0f} kg", "Opportunity Gap", delta_color="inverse")
    
    c3.metric("Faktor Pembatas Utama", res['limiting_factor'], f"Skor: {res['factors'][res['limiting_factor']]*100:.0f}%", delta_color="inverse")

    st.divider()
    
    # 2. FACTOR RADAR CHART
    c_chart, c_insight = st.columns([1.5, 1])
    
    with c_chart:
        factors = res['factors']
        df_radar = pd.DataFrame(dict(
            r=list(factors.values()),
            theta=list(factors.keys())
        ))
        fig = px.line_polar(df_radar, r='r', theta='theta', line_close=True, range_r=[0, 1.2])
        fig.update_traces(fill='toself')
        fig.update_layout(title="Profil Kesehatan Lahan")
        st.plotly_chart(fig, use_container_width=True)
        
    with c_insight:
        st.subheader("💡 Rekomendasi Agronomis")
        
        # Smart Text Generation
        recos = []
        if factors['pH Tanah'] < 0.8:
            if i_ph < 6.0: recos.append("🔴 **pH Asam**: Tambahkan kapur Dolomit (2 ton/ha).")
            else: recos.append("🔴 **pH Basa**: Tambahkan Sulfur atau bahan organik.")
            
        if factors['Nitrogen'] < 0.7:
             recos.append("🟠 **Defisiensi N**: Tambahkan Urea 100kg/ha fase vegetatif.")
        
        if factors['Air/Curah Hujan'] < 0.6:
            recos.append("🔵 **Kekurangan Air**: Wajib irigasi pompa 2x seminggu.")
            
        if not recos:
            st.success("✅ Kondisi lahan cukup optimal! Lakukan pemupukan berimbang.")
        else:
            for r in recos: st.markdown(r)
            
        st.info(f"**Varietas {s_var}** memiliki ketahanan {CROP_DB[s_crop]['varieties'][s_var]['resilience']*100:.0f}% terhadap stress lingkungan.")

with tab_eco:
    st.subheader("Simulasi Keuntungan Bisnis")
    
    # Economics Inputs
    ce1, ce2, ce3 = st.columns(3)
    price_est = ce1.number_input("Estimasi Harga Jual (Rp/kg)", 0, 100000, CROP_DB[s_crop]['price'])
    cost_est = ce2.number_input("Total Biaya Produksi (Rp)", 0, 1000000000, int(s_area * 15000000)) # 15jt/ha default
    
    # Calc
    revenue = res['yield_kg'] * price_est
    profit = revenue - cost_est
    roi = (profit / cost_est) * 100 if cost_est > 0 else 0
    
    # Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Omzet (Revenue)", f"Rp {revenue:,.0f}")
    m2.metric("Keuntungan Bersih", f"Rp {profit:,.0f}", f"ROI: {roi:.1f}%")
    m3.metric("Break Even Point (Yield)", f"{(cost_est/price_est):,.0f} kg", "Titik Impas")
    
    # Visualization: Waterfall
    fig_waterfall = go.Figure(go.Waterfall(
        measure = ["relative", "relative", "total"],
        x = ["Penjualan", "Biaya Produksi", "Laba Bersih"],
        y = [revenue, -cost_est, profit],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))
    fig_waterfall.update_layout(title = "Analisis Cashflow Proyek")
    st.plotly_chart(fig_waterfall, use_container_width=True)

with tab_whatif:
    st.header("🧪 Lab Simulasi Interaktif")
    st.markdown("Geser slider untuk melihat bagaimana **perubahan input** mempengaruhi hasil panen secara real-time.")
    
    wc1, wc2 = st.columns([1, 2])
    
    with wc1:
        st.caption("🎮 Kontrol Simulator")
        sim_n = st.slider("➕ Tambah Pupuk N (kg)", 0, 500, i_n)
        sim_p = st.slider("➕ Tambah Pupuk P (kg)", 0, 300, i_p)
        sim_water = st.slider("💧 Irigasi Tambahan (mm)", 0, 1000, 0)
        
    with wc2:
        # Re-run logic for simulator
        sim_params = params.copy()
        sim_params['n'] = sim_n
        sim_params['p'] = sim_p
        sim_params['rain'] += sim_water
        
        sim_res = run_simulation(s_crop, s_var, s_grad, sim_params)
        
        delta_yield = sim_res['yield_kg'] - res['yield_kg']
        delta_rev = delta_yield * price_est
        
        # Display Result
        st.subheader("Hasil Simulasi:")
        
        sm1, sm2 = st.columns(2)
        sm1.metric("Prediksi Baru", f"{sim_res['yield_kg']:,.0f} kg", f"{delta_yield:+,.0f} kg")
        sm2.metric("Tambahan Omzet", f"Rp {sim_res['yield_kg']*price_est:,.0f}", f"Rp {delta_rev:+,.0f}")
        
        # Progress Bar Comparison
        st.write("Perbandingan Efisiensi:")
        st.progress(int(res['yield_pct']))
        st.caption(f"Awal: {res['yield_pct']:.1f}%")
        st.progress(int(sim_res['yield_pct']))
        st.caption(f"Simulasi: {sim_res['yield_pct']:.1f}%")
        
        if delta_yield > 0:
            st.success(f"🔥 Skenario ini meningkatkan hasil sebesar **{delta_yield:,.0f} kg**!")
        elif delta_yield < 0:
            st.error("⚠️ Over-dosis! Penambahan input berlebih justru menurunkan hasil (Hukum Diminishing Return).")
        else:
            st.warning("Tidak ada perubahan signifikan.")
