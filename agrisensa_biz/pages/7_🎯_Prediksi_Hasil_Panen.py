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

def sigmoid_curve(val, max_boost=1.1, midpoint=50):
    """S-curve for organic/bio boosters (diminishing returns)"""
    return 1 + (max_boost - 1) / (1 + np.exp(-0.1 * (val - midpoint)))

def run_simulation(crop, variety, texture_key, params):
    # Get base potential
    crop_data = CROP_DB[crop]
    var_data = crop_data['varieties'][variety]
    opt = crop_data['optimal']
    
    potential = var_data['potential'] * params['area_ha']
    
    # Soil Texture Impact
    texture = SOIL_TEXTURES[texture_key]
    
    # --- ORGANIC & BIO AMENDMENTS IMPACT ---
    # Organic Solid improves Texture (Water retention & Nutrient Holding)
    org_solid_factor = 1.0 + (params.get('org_solid', 0) / 10000) * 0.2 # Max 20% improvement at 10ton/ha
    
    current_water_retention = min(1.0, texture['water_retention'] * org_solid_factor)
    current_nutrient_holding = min(1.2, texture['nutrient_holding'] * org_solid_factor)
    
    # Organic Liquid/POC acts as immediate nutrient efficiency booster
    poc_eff_boost = 1.0 + (params.get('org_liquid', 0) / 100) * 0.15 # Max 15% efficiency boost at 100L/ha

    # 1. Nutrient Factors (Saturation Curve)
    # Effective N = Input N * Soil Holding Cap * POC Boost
    eff_n = params['n'] * current_nutrient_holding * poc_eff_boost
    score_n = saturation_curve(eff_n, opt['n'])
    
    eff_p = params['p'] * current_nutrient_holding * poc_eff_boost
    score_p = saturation_curve(eff_p, opt['p'])
    
    eff_k = params['k'] * current_nutrient_holding * poc_eff_boost
    score_k = saturation_curve(eff_k, opt['k'])
    
    # Secondary Macros (Ca, Mg, S) - Critical for quality/enzyme function
    # Modeled as sufficiency score (0.0 - 1.0) based on input ppm/kg
    # Simplified thresholds for simulator
    score_ca = saturation_curve(params.get('ca_ppm', 0), 200) # Need ~200ppm
    score_mg = saturation_curve(params.get('mg_ppm', 0), 50)  # Need ~50ppm
    score_s  = saturation_curve(params.get('s_ppm', 0), 30)   # Need ~30ppm
    
    # Micro Nutrients (Fe, Mn, Zn, B, Cu, Mo) - Trace but vital
    # Modeled as individual sufficiency
    score_fe = saturation_curve(params.get('fe_ppm', 0), 5)   # Iron
    score_mn = saturation_curve(params.get('mn_ppm', 0), 5)   # Manganese
    score_zn = saturation_curve(params.get('zn_ppm', 0), 2)   # Zinc
    score_b  = saturation_curve(params.get('b_ppm', 0), 1)    # Boron
    score_cu = saturation_curve(params.get('cu_ppm', 0), 0.5) # Copper
    score_mo = saturation_curve(params.get('mo_ppm', 0), 0.1) # Molybdenum
    
    # Aggregate Micro Score (Geometric Mean for average health, but Min for Liebig)
    # Using geometric mean for the "Micro Group" score to avoid one zero killing everything unduly in the display,
    # but strictly, Liebig says Min.
    micro_scores = [score_fe, score_mn, score_zn, score_b, score_cu, score_mo]
    avg_micro_score = np.mean(micro_scores)
    
    # 2. Environmental Factors (Gaussian)
    score_ph = gaussian_curve(params['ph'], opt['ph'])
    score_temp = gaussian_curve(params['temp'], opt['temp'])
    
    # 3. Water (Linear with penalty)
    eff_water = params['rain'] * current_water_retention
    if eff_water < opt['water'] * 0.5:
        score_water = 0.4 + (eff_water / opt['water']) * 0.6
    elif eff_water > opt['water'] * 1.5:
        score_water = 0.8 # Flood stress
    else:
        score_water = 1.0
        
    # LIEBIG'S LAW OF THE MINIMUM (Expanded)
    factors = {
        "Nitrogen": score_n, "Fosfor": score_p, "Kalium": score_k,
        "Kalsium (Ca)": score_ca, "Magnesium (Mg)": score_mg, "Sulfur (S)": score_s,
        "Mikro (Avg)": avg_micro_score, # For radar chart simplicity
        "pH Tanah": score_ph, "Air": score_water, "Suhu": score_temp
    }
    
    # Check strict limiting factor including specific micros
    all_scores_dict = factors.copy()
    all_scores_dict.update({
        "Besi (Fe)": score_fe, "Mangan (Mn)": score_mn, "Seng (Zn)": score_zn,
        "Boron (B)": score_b, "Tembaga (Cu)": score_cu, "Molibdenum (Mo)": score_mo
    })
    
    limiting_factor_val = min(all_scores_dict.values())
    limiting_factor_name = min(all_scores_dict, key=all_scores_dict.get)
    
    # Average of major groups
    avg_factor_val = sum(factors.values()) / len(factors)
    
    # Hybrid model
    final_yield_pct = (limiting_factor_val * 0.6) + (avg_factor_val * 0.4)
    
    # --- BOOSTERS & HORMONES (Multipliers) ---
    # Hormones (ZPT) Split: Auksin, Sitokinin, Giberelin
    
    # Auksin: Rooting & Nutrient Uptake Efficiency (Gaussian)
    # Optimal ~20-40 ppm. 
    auxin_ppm = params.get('auxin_ppm', 0)
    mu_auxin = 30
    if auxin_ppm > 0:
        auxin_mult = 1.0 + (0.12 * np.exp(-0.5 * ((auxin_ppm - mu_auxin) / 15)**2))
        # High overdose penalty
        if auxin_ppm > 80: auxin_mult -= ((auxin_ppm - 80) * 0.005) 
    else:
        auxin_mult = 1.0

    # Sitokinin: Cell Division & Filling (Sigmoid -> Plateau)
    # Good for grain filling / vegetable leafiness. Harder to overdose than Auxin.
    cyto_ppm = params.get('cyto_ppm', 0)
    if cyto_ppm > 0:
        cyto_mult = 1.0 + (0.10 * (1 - np.exp(-0.05 * cyto_ppm)))    
    else:
        cyto_mult = 1.0
        
    # Giberelin (GA3): Size & Elongation (Gaussian broad)
    # Powerful but risky (bolting). Optimal ~50-80 ppm.
    ga3_ppm = params.get('ga3_ppm', 0)
    mu_ga3 = 60
    if ga3_ppm > 0:
        ga3_mult = 1.0 + (0.15 * np.exp(-0.5 * ((ga3_ppm - mu_ga3) / 25)**2))
        if ga3_ppm > 150: ga3_mult -= ((ga3_ppm - 150) * 0.003)
    else:
        ga3_mult = 1.0

    # Combined ZPT Effect (Multiplicative with damping)
    zpt_total_mult = auxin_mult * cyto_mult * ga3_mult
        
    # Booster (e.g. Kalium Booster for fruit phase)
    # Modeled as Sigmoid - steady increase
    booster_kg = params.get('booster_kg', 0)
    booster_multiplier = 1.0 + (0.1 * (1 - np.exp(-0.1 * booster_kg))) # Max 10% boost
    
    final_yield_pct = final_yield_pct * zpt_total_mult * booster_multiplier
    
    # Variety resilience bonus
    final_yield_pct = final_yield_pct * (0.9 + (var_data['resilience'] * 0.1))
    
    # Cap at 130% of standard potential (genetic breakdown limit)
    final_yield_pct = min(1.3, final_yield_pct)
    
    predicted_kg = potential * final_yield_pct
    
    return {
        "yield_kg": predicted_kg,
        "yield_pct": final_yield_pct * 100,
        "factors": factors,
        "limiting_factor": limiting_factor_name,
        "potential_kg": potential,
        "multipliers": {
            "auxin": auxin_mult,
            "cyto": cyto_mult,
            "ga3": ga3_mult,
            "zpt_total": zpt_total_mult,
            "booster": booster_multiplier,
            "organic_solid": org_solid_factor,
            "organic_liquid": poc_eff_boost
        },
        "micros": {
            "fe": score_fe, "mn": score_mn, "zn": score_zn, 
            "b": score_b, "cu": score_cu, "mo": score_mo
        },
        "macros_sec": {
            "ca": score_ca, "mg": score_mg, "s": score_s
        }
    }

# ================================
# 🖥️ UI INTERFACE
# ================================

st.title("🎯 Advanced Harvest Forecast & Simulator")
st.markdown("### Simulasi Cerdas Berbasis Machine Learning & Ekonomi")
st.info("💡 **Tips:** Gunakan tab 'What-If Simulator' untuk bereksperimen dengan kombinasi pupuk lengkap (Makro, Mikro, ZPT).")

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
    i_temp = st.slider("Suhu Rata-rata (°C)", 15, 40, int(def_opt.get('temp', 28)))
    i_rain = st.number_input("Curah Hujan (mm/musim)", 0, 5000, 1200)
    
    st.markdown("---")
    st.markdown("**🧪 Input Nutrisi Dasar**")
    c_n, c_p, c_k = st.columns(3)
    i_n = c_n.number_input("Urea/N (kg)", 0, 1000, int(def_opt['n']*0.5))
    i_p = c_p.number_input("SP36/P (kg)", 0, 1000, int(def_opt['p']*0.5))
    i_k = c_k.number_input("KCl/K (kg)", 0, 1000, int(def_opt['k']*0.5))
    
    btn_predict = st.button("🚀 Jalankan Analisis", type="primary", use_container_width=True)

# --- MAIN AREA ---

# Initial params
params = {
    "area_ha": s_area, "ph": i_ph, "temp": i_temp, "rain": i_rain,
    "n": i_n, "p": i_p, "k": i_k,
    # Defaults for initial run
    "org_solid": 0, "org_liquid": 0, 
    "ca_ppm": 100, "mg_ppm": 30, "s_ppm": 20, # Moderate defaults
    "fe_ppm": 2, "mn_ppm": 2, "zn_ppm": 1, "b_ppm": 0.5, "cu_ppm": 0.2, "mo_ppm": 0.05, # Moderate defaults
    "auxin_ppm": 0, "cyto_ppm": 0, "ga3_ppm": 0, "booster_kg": 0
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
    
    c3.metric("Faktor Pembatas Utama", res['limiting_factor'], f"Optimasi Perlu Ditingkatkan", delta_color="inverse")

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
        fig.update_layout(title="Profil Kesehatan Lahan & Nutrisi")
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
        
        if factors['Mikro (Avg)'] < 0.8:
            recos.append("🟡 **Mikro Rendah**: Aplikasikan pupuk daun mikro lengkap (Fe, Zn, B).")
            
        if factors['Sulfur (S)'] < 0.7:
            recos.append("🟡 **Defisiensi Sulfur**: Gunakan ZA atau Gypsum.")

        if factors['Air'] < 0.6:
            recos.append("🔵 **Kekurangan Air**: Wajib irigasi pompa 2x seminggu.")
            
        if not recos:
            st.success("✅ Kondisi lahan cukup optimal! Lakukan pemupukan berimbang atau gunakan Booster.")
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
    st.header("🧪 Lab Simulasi Interaktif Power-Up")
    st.write("Eksperimen dengan **Teknologi Input Lanjutan** untuk melihat potensi maksimal panen.")
    
    # Layout with cols
    col_input, col_res = st.columns([1, 1.5])
    
    with col_input:
        with st.expander("1️⃣ Nutrisi Makro Primer (N, P, K)", expanded=True):
            w_n = st.slider("➕ Tambah N (kg)", 0, 300, 0, help="Tambahan Urea/ZA")
            w_p = st.slider("➕ Tambah P (kg)", 0, 200, 0, help="Tambahan SP36/DAP")
            w_k = st.slider("➕ Tambah K (kg)", 0, 200, 0, help="Tambahan KCl/ZK")
        
        with st.expander("2️⃣ Nutrisi Makro Sekunder (Ca, Mg, S)"):
            w_ca = st.slider("🥛 Kalsium (ppm)", 0, 500, 100, help="Dolomit/Kaptan. Penting untuk dinding sel.")
            w_mg = st.slider("🌿 Magnesium (ppm)", 0, 200, 30, help="Pusat klorofil daun.")
            w_s = st.slider("🟡 Sulfur (ppm)", 0, 100, 20, help="Penyusun protein & enzim.")

        with st.expander("3️⃣ Nutrisi Mikro Lengkap (Fe, Zn, dll)"):
            c_m1, c_m2 = st.columns(2)
            w_fe = c_m1.slider("Besi/Fe", 0.0, 20.0, 2.0)
            w_mn = c_m2.slider("Mangan/Mn", 0.0, 20.0, 2.0)
            w_zn = c_m1.slider("Seng/Zn", 0.0, 10.0, 1.0)
            w_b = c_m2.slider("Boron/B", 0.0, 5.0, 0.5)
            w_cu = c_m1.slider("Tembaga/Cu", 0.0, 2.0, 0.2)
            w_mo = c_m2.slider("Molibdenum", 0.0, 1.0, 0.05)
        
        with st.expander("4️⃣ Organik & Hayati"):
            w_org_solid = st.slider("🍂 Organik Padat (kg)", 0, 20000, 0, step=500, help="Kompos/Kohe. Memperbaiki tekstur tanah.")
            w_org_liq = st.slider("🧴 Organik Cair / POC (Liter)", 0, 500, 0, step=10, help="Booster efisiensi serapan hara.")

        with st.expander("5️⃣ Hormon ZPT (Tri-Hormon) & Booster", expanded=True):
            w_auxin = st.slider("🧬 Auksin (ppm)", 0, 100, 0, help="Perakaran & Vegetatif. Optimal ~30ppm.")
            w_cyto = st.slider("🦠 Sitokinin (ppm)", 0, 100, 0, help="Pembelahan Sel & Pengisian Buah.")
            w_ga3 = st.slider("🎋 Giberelin (ppm)", 0, 200, 0, help="Ukuran Buah & Pemanjangan. Hati-hati overdosis!")
            st.divider()
            w_boost = st.slider("💊 Kalium Booster (kg)", 0, 50, 0, help="Pupuk khusus fase generatif (e.g., MKP/KNO3).")

    with col_res:
        # Re-run logic for simulator
        sim_params = params.copy()
        
        # Additive updates to base params
        sim_params['n'] += w_n
        sim_params['p'] += w_p
        sim_params['k'] += w_k
        
        # New params override
        sim_params['ca_ppm'] = w_ca
        sim_params['mg_ppm'] = w_mg
        sim_params['s_ppm'] = w_s
        
        sim_params['fe_ppm'] = w_fe
        sim_params['mn_ppm'] = w_mn
        sim_params['zn_ppm'] = w_zn
        sim_params['b_ppm'] = w_b
        sim_params['cu_ppm'] = w_cu
        sim_params['mo_ppm'] = w_mo
        
        sim_params['org_solid'] = w_org_solid
        sim_params['org_liquid'] = w_org_liq
        
        sim_params['auxin_ppm'] = w_auxin
        sim_params['cyto_ppm'] = w_cyto
        sim_params['ga3_ppm'] = w_ga3
        sim_params['booster_kg'] = w_boost
        
        sim_res = run_simulation(s_crop, s_var, s_grad, sim_params)
        
        delta_kg = sim_res['yield_kg'] - res['yield_kg']
        delta_rev = delta_kg * price_est
        
        # Cost Estimator for Simulation Inputs (Rough estimates)
        cost_inputs = (w_n * 5000) + (w_p * 6000) + (w_k * 15000) + \
                      (w_org_solid * 1000) + (w_org_liq * 25000) + \
                      (w_auxin * 2000) + (w_cyto * 3000) + (w_ga3 * 3000) + \
                      (w_boost * 35000)
                      
        net_profit_delta = delta_rev - cost_inputs

        st.subheader("📊 Hasil Prediksi Real-Time")
        
        met1, met2, met3 = st.columns(3)
        met1.metric("Hasil Panen Baru", f"{sim_res['yield_kg']:,.0f} kg", f"{delta_kg:+,.0f} kg")
        met2.metric("Nilai Tambah (Gross)", f"Rp {delta_rev:+,.0f}", help="Belum dikurangi biaya input simulasi")
        met3.metric("Net Profit Tambahan", f"Rp {net_profit_delta:,.0f}", delta_color="normal" if net_profit_delta >= 0 else "inverse")
        
        st.caption(f"estimasi biaya input tambahan: Rp {cost_inputs:,.0f}")
        
        # Progress Bar Visualization
        st.write("---")
        st.write("**Perbandingan Performance (% Potensi Genetik):**")
        
        col_bar_lbl, col_bar_val = st.columns([1,3])
        with col_bar_lbl: st.write("Awal")
        with col_bar_val: st.progress(int(min(100, res['yield_pct'])))
        
        col_bar_lbl2, col_bar_val2 = st.columns([1,3])
        with col_bar_lbl2: st.write("Simulasi")
        with col_bar_val2: 
            p_val = int(min(100, sim_res['yield_pct']))
            st.progress(p_val)
            if sim_res['yield_pct'] > 100:
                st.caption(f"🚀 **SUPER-OPTIMAL!** ({sim_res['yield_pct']:.1f}%) - Efek ZPT & Booster Aktif.")
        
        # Diagnostics
        with st.expander("🔍 Analisis Dampak Input (Diagnostics)", expanded=True):
            mults = sim_res['multipliers']
            st.write(f"- **Efek Organik Padat:** +{(mults['organic_solid']-1)*100:.1f}%")
            st.write(f"- **Efek Organik Cair:** +{(mults['organic_liquid']-1)*100:.1f}%")
            
            # Detailed Hormone Breakdown
            c_z1, c_z2, c_z3 = st.columns(3)
            with c_z1:
                eff = (mults['auxin']-1)*100
                st.metric("Auksin (Root)", f"{eff:+.1f}%", delta_color="normal" if eff >= 0 else "inverse")
            with c_z2:
                eff = (mults['cyto']-1)*100
                st.metric("Sitokinin (Cell)", f"{eff:+.1f}%")
            with c_z3:
                eff = (mults['ga3']-1)*100
                st.metric("Giberelin (Size)", f"{eff:+.1f}%", delta_color="normal" if eff >= 0 else "inverse")

            st.markdown("---")
            st.markdown("**Status Nutrisi Mikro & Sekunder:**")
            micros = sim_res['micros']
            macros_sec = sim_res['macros_sec']
            
            c_d1, c_d2 = st.columns(2)
            with c_d1:
                st.write("**Makro Sekunder**")
                st.progress(macros_sec['ca'], text=f"Kalsium (Ca): {macros_sec['ca']*100:.0f}%")
                st.progress(macros_sec['mg'], text=f"Magnesium (Mg): {macros_sec['mg']*100:.0f}%")
                st.progress(macros_sec['s'], text=f"Sulfur (S): {macros_sec['s']*100:.0f}%")
            with c_d2:
                st.write("**Mikro Esensial**")
                st.progress(micros['fe'], text=f"Besi (Fe): {micros['fe']*100:.0f}%")
                st.progress(micros['zn'], text=f"Seng (Zn): {micros['zn']*100:.0f}%")
                st.progress(micros['b'], text=f"Boron (B): {micros['b']*100:.0f}%")

            st.write(f"- **Efek Booster Buah:** +{(mults['booster']-1)*100:.1f}%")
