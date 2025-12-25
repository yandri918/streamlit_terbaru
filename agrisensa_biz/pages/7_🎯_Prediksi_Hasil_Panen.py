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

FERT_PRODUCTS = {
    # Macros
    "Urea": {"n": 0.46, "p": 0, "k": 0, "price": 4000, "type": "Solid"},
    "ZA": {"n": 0.21, "p": 0, "k": 0, "s": 0.24, "price": 2500, "type": "Solid"},
    "SP-36": {"n": 0, "p": 0.36, "k": 0, "s": 0.05, "price": 3500, "type": "Solid"},
    "KCl": {"n": 0, "p": 0, "k": 0.60, "price": 12000, "type": "Solid"},
    "NPK 16-16-16": {"n": 0.16, "p": 0.16, "k": 0.16, "price": 15000, "type": "Solid"},
    
    # Secondary & Micro
    "Dolomit": {"ca": 0.30, "mg": 0.18, "price": 500, "type": "Solid"},
    "Kieserite": {"mg": 0.27, "s": 0.20, "price": 4000, "type": "Solid"},
    "Mikro Majemuk": {"fe":0.1, "zn":0.05, "b":0.02, "price": 80000, "type": "Soluble"}, # Simplified
    
    # Organics
    "Kompos": {"price": 1000, "type": "Solid"},
    "POC": {"price": 35000, "type": "Liquid"},
    
    # Hormones
    "ZPT Auksin": {"price": 45000, "type": "Small"},
    "ZPT Sitokinin": {"price": 50000, "type": "Small"},
    "ZPT Giberelin": {"price": 60000, "type": "Small"},
    "Kalium Booster": {"price": 40000, "type": "Soluble"}
}

# ... (Previous simulation code remains unchanged) ...

with tab_whatif:
    st.header("🧪 Lab Simulasi Interaktif Power-Up")
    st.write("Eksperimen dengan **Teknologi Input Lanjutan** untuk melihat potensi maksimal panen.")
    
    # Layout with cols
    col_input, col_kalkulator = st.columns([1, 1.2]) # Adjusted layout
    
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

        with st.expander("5️⃣ Hormon ZPT & Booster", expanded=True):
            w_auxin = st.slider("🧬 Auksin (ppm)", 0, 100, 0, help="Perakaran & Vegetatif. Optimal ~30ppm.")
            w_cyto = st.slider("🦠 Sitokinin (ppm)", 0, 100, 0, help="Pembelahan Sel & Pengisian Buah.")
            w_ga3 = st.slider("🎋 Giberelin (ppm)", 0, 200, 0, help="Ukuran Buah & Pemanjangan.")
            st.divider()
            w_boost = st.slider("💊 Kalium Booster (kg)", 0, 50, 0, help="Pupuk khusus fase generatif.")

    with col_kalkulator:
        st.subheader("💰 Kalkulator Belanja Pupuk")
        st.info("Otomatis mengkonversi kebutuhan nutrisi di samping menjadi kebutuhan produk pupuk komersial.")
        
        with st.expander("⚙️ Edit Harga Pupuk (Rp/kg atau Rp/L)", expanded=False):
            c_p1, c_p2 = st.columns(2)
            p_urea = c_p1.number_input("Harga Urea", 0, 50000, FERT_PRODUCTS["Urea"]["price"])
            p_sp36 = c_p2.number_input("Harga SP-36", 0, 50000, FERT_PRODUCTS["SP-36"]["price"])
            p_kcl  = c_p1.number_input("Harga KCl", 0, 50000, FERT_PRODUCTS["KCl"]["price"])
            p_dolomit = c_p2.number_input("Harga Dolomit", 0, 10000, FERT_PRODUCTS["Dolomit"]["price"])
            p_kompos = c_p1.number_input("Harga Kompos", 0, 5000, FERT_PRODUCTS["Kompos"]["price"])
            p_poc = c_p2.number_input("Harga POC (Liter)", 0, 200000, FERT_PRODUCTS["POC"]["price"])
            p_booster = c_p1.number_input("Harga K-Booster", 0, 200000, FERT_PRODUCTS["Kalium Booster"]["price"])
        
        # Calculation Logic
        req_list = []
        total_costs = 0
        
        # 1. Nitrogen -> Urea (Default)
        if w_n > 0:
            qty_urea = w_n / 0.46
            cost_urea = qty_urea * p_urea
            req_list.append({"Item": "Urea (46% N)", "Kebutuhan": f"{qty_urea:.1f} kg", "Estimasi Biaya": cost_urea})
            total_costs += cost_urea
            
        # 2. Fosfor -> SP-36
        if w_p > 0:
            qty_sp36 = w_p / 0.36
            cost_sp36 = qty_sp36 * p_sp36
            req_list.append({"Item": "SP-36 (36% P)", "Kebutuhan": f"{qty_sp36:.1f} kg", "Estimasi Biaya": cost_sp36})
            total_costs += cost_sp36

        # 3. Kalium -> KCl
        if w_k > 0:
            qty_kcl = w_k / 0.60
            cost_kcl = qty_kcl * p_kcl
            req_list.append({"Item": "KCl (60% K)", "Kebutuhan": f"{qty_kcl:.1f} kg", "Estimasi Biaya": cost_kcl})
            total_costs += cost_kcl
            
        # 4. Secondary (Example: Ca -> Dolomit)
        # Ca ppm to kg/ha approx: ppm * 2 (Assuming depth 20cmBD 1.0) -> roughly
        # Simplified: 1 ppm Ca ~ 2 kg Ca/ha needed in soil app? No, ppm is conc.
        # Let's assume the slider is "Target increase in ppm".
        # Soil mass/ha ~ 2,000,000 kg (20cm). 1 ppm = 2 kg element.
        if w_ca > 0:
            ca_kg_needed = w_ca * 2 # 2kg Ca per ppm
            dolomit_needed = ca_kg_needed / 0.30 # 30% Ca
            cost_dol = dolomit_needed * p_dolomit
            req_list.append({"Item": "Dolomit (30% Ca)", "Kebutuhan": f"{dolomit_needed:.1f} kg", "Estimasi Biaya": cost_dol})
            total_costs += cost_dol

        # Organics
        if w_org_solid > 0:
            cost_org = w_org_solid * p_kompos
            req_list.append({"Item": "Kompos/Organik", "Kebutuhan": f"{w_org_solid:,.0f} kg", "Estimasi Biaya": cost_org})
            total_costs += cost_org
            
        if w_org_liq > 0:
            cost_poc = w_org_liq * p_poc
            req_list.append({"Item": "POC (Cair)", "Kebutuhan": f"{w_org_liq:,.0f} L", "Estimasi Biaya": cost_poc})
            total_costs += cost_poc
            
        # Booster
        if w_boost > 0:
            cost_boost = w_boost * p_booster
            req_list.append({"Item": "Kalium Booster", "Kebutuhan": f"{w_boost:.1f} kg", "Estimasi Biaya": cost_boost})
            total_costs += cost_boost

        # Display Table
        if req_list:
            df_cost = pd.DataFrame(req_list)
            st.dataframe(
                df_cost, 
                column_config={
                    "Estimasi Biaya": st.column_config.NumberColumn(format="Rp %d")
                },
                use_container_width=True,
                hide_index=True
            )
            st.metric("Total Estimasi Biaya", f"Rp {total_costs:,.0f}", delta_color="off")
        else:
            st.info("Geser slider di menu kiri untuk melihat kebutuhan pupuk.")
            
        # Re-run logic for simulator (Simplified for brevity in view)
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
        
        net_profit_delta = delta_rev - total_costs # Use calculated total_costs

        st.subheader("📊 Hasil Prediksi Real-Time")
        
        met1, met2, met3 = st.columns(3)
        met1.metric("Hasil Panen Baru", f"{sim_res['yield_kg']:,.0f} kg", f"{delta_kg:+,.0f} kg")
        met2.metric("Nilai Tambah (Gross)", f"Rp {delta_rev:+,.0f}", help="Belum dikurangi biaya input simulasi")
        met3.metric("Net Profit Tambahan", f"Rp {net_profit_delta:,.0f}", delta_color="normal" if net_profit_delta >= 0 else "inverse")
        
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


def optimize_budget(budget, params, crop, var, texture_key, fert_prices):
    """
    Greedy Hill-Climbing Algorithm:
    Allocates budget to the most limiting factor iteratively.
    """
    current_params = params.copy()
    remaining_budget = budget
    purchased_items = {} # Item: Qty
    
    # Cost definitions per unit step (Simplified Estimates for algorithm)
    # Unit sizes chosen for granular increments
    actions = {
        "Nitrogen": {"key": "n", "amount": 2, "cost": (2/0.46) * fert_prices["Urea"], "product": "Urea", "p_unit": "kg"},
        "Fosfor": {"key": "p", "amount": 2, "cost": (2/0.36) * fert_prices["SP-36"], "product": "SP-36", "p_unit": "kg"},
        "Kalium": {"key": "k", "amount": 2, "cost": (2/0.60) * fert_prices["KCl"], "product": "KCl", "p_unit": "kg"},
        "pH Tanah": {"key": "ph", "amount": 0.1, "cost": (200 * fert_prices["Dolomit"]), "product": "Dolomit/Kapur", "p_unit": "kg (est 200kg)"}, # Assumes 200kg to raise pH 0.1 (crude)
        "Nutrisi Mikro": {"key": "micro_pct", "amount": 5, "cost": 0.1 * fert_prices["Mikro Majemuk"], "product": "Mikro Majemuk", "p_unit": "kg"},
        "Mikro (Avg)": {"key": "micro_pct", "amount": 5, "cost": 0.1 * fert_prices["Mikro Majemuk"], "product": "Mikro Majemuk", "p_unit": "kg"},
        # Secondary
        "Kalsium (Ca)": {"key": "ca_ppm", "amount": 10, "cost": (20 * fert_prices["Dolomit"]), "product": "Dolomit", "p_unit": "kg"},
        "Magnesium (Mg)": {"key": "mg_ppm", "amount": 5, "cost": (5 * fert_prices["Kieserite"]), "product": "Kieserite", "p_unit": "kg"},
        "Sulfur (S)": {"key": "s_ppm", "amount": 5, "cost": (5 * fert_prices["ZA"]), "product": "ZA/Sulfur", "p_unit": "kg"},
        # Logic: If nothing else is strict limiting, dump into Organics/Boosters
        "General_Boost": {"key": "booster_kg", "amount": 1, "cost": 1 * fert_prices["Kalium Booster"], "product": "Kalium Booster", "p_unit": "kg"}
    }
    
    steps_log = []
    
    # Safety breakout
    for _ in range(100): 
        if remaining_budget <= 5000: break # Minimum transaction
        
        # 1. Run Sim to find Limiting Factor
        res = run_simulation(crop, var, texture_key, current_params)
        limit = res['limiting_factor']
        
        # 2. Determine Action
        action = actions.get(limit)
        
        # If limiting factor is Air/Temp (Unfixable by budget) -> Switch to Booster or Organic
        if not action or limit in ['Air', 'Suhu']:
             # Try Organic first if low, else Booster
             if current_params['org_solid'] < 5000:
                 action = {"key": "org_solid", "amount": 500, "cost": 500 * fert_prices["Kompos"], "product": "Kompos", "p_unit": "kg"}
             elif current_params['zpt_ppm'] < 50:
                  action = {"key": "auxin_ppm", "amount": 5, "cost": 5000, "product": "ZPT Mix", "p_unit": "ppm"} # Simplified ZPT cost
             else:
                 action = actions["General_Boost"]
        
        # 3. Check Affordability
        if remaining_budget >= action['cost']:
            # execute buy
            remaining_budget -= action['cost']
            
            # Update Param
            current_params[action['key']] = current_params.get(action['key'], 0) + action['amount']
            
            # Log purchase
            item_name = action['product']
            purchased_items[item_name] = purchased_items.get(item_name, 0) + (action['cost'] / fert_prices.get(item_name.split("/")[0], 1000)) # Approx qty back calc if complex, or just track cost
            
            # Better Qty tracking:
            # We defined 'amount' as nutrient amount, need to map back to product qty for display optimization?
            # actually action['cost'] is accurate.
            # Let's just store the 'cost spent' on each item efficiently? 
            # Or simplified: The user wants "Breakdown apa saja yang ditambahkan"
            
            # Simple Text Log for debug or display
            # steps_log.append(f"Fixed {limit} with {action['product']}")
            
        else:
            break # Can't afford the fix for the bottleneck
            
    final_res = run_simulation(crop, var, texture_key, current_params)
    return current_params, final_res, remaining_budget

# ... (Previous code) ...

    with col_kalkulator:
        st.subheader("💰 Kalkulator Belanja Pupuk")
        # ... (Previous calculator code) ...
        # ... Ensure user inputs like p_urea are captured in a dictionary for the optimizer ...
        current_prices = {
            "Urea": p_urea, "SP-36": p_sp36, "KCl": p_kcl, 
            "Dolomit": p_dolomit, "Kompos": p_kompos, "POC": p_poc,
            "Kalium Booster": p_booster, "Kieserite": 4000, "ZA": 2500, "Mikro Majemuk": 80000 
            # Add implicit pricing for others if not in UI yet, or add them to UI
        }
        
        # ... (Existing Calculation Logic for Cost Table) ...
        
        st.divider()
        st.subheader("🤖 Smart Budget Allocator (Reverse)")
        st.info("Punya modal terbatas? Biarkan AI menentukan prioritas belanja pupuk paling efisien (Hukum Minimum Liebig).")
        
        budget_input = st.number_input("Masukkan Modal Tambahan (Rp)", 0, 100000000, 1000000, step=100000, help="Anggaran yang tersedia untuk optimalisasi.")
        
        if st.button("✨ Optimalkan Modal Saya"):
            # Run Optimizer
            # Start from 'current actual' params (without the manual sliders from columns?)
            # Usually optimization starts from the 'base' condition (i_n, i_p, etc from Sidebar) 
            # OR from the current slider state? Let's assume from Sidebar/Base condition to be safe "Add to existing"
            
            base_params_for_opt = {
                "area_ha": s_area, "ph": i_ph, "temp": i_temp, "rain": i_rain,
                "n": i_n, "p": i_p, "k": i_k,
                "org_solid": 0, "org_liquid": 0, 
                "ca_ppm": 100, "mg_ppm": 30, "s_ppm": 20,
                "fe_ppm": 2, "mn_ppm": 2, "zn_ppm": 1, "b_ppm": 0.5, "cu_ppm": 0.2, "mo_ppm": 0.05,
                "auxin_ppm": 0, "cyto_ppm": 0, "ga3_ppm": 0, "booster_kg": 0
            }
            
            opt_params, opt_res, left_budget = optimize_budget(budget_input, base_params_for_opt, s_crop, s_var, s_grad, current_prices)
            
            # Display Results
            opt_delta_kg = opt_res['yield_kg'] - res['yield_kg'] # Res is base run
            opt_delta_rev = opt_delta_kg * price_est
            spent_budget = budget_input - left_budget
            opt_roi = ((opt_delta_rev - spent_budget) / spent_budget * 100) if spent_budget > 0 else 0
            
            st.success(f"✅ Optimasi Selesai! Anggaran terpakai: Rp {spent_budget:,.0f}")
            
            # Metrics
            c_o1, c_o2, c_o3 = st.columns(3)
            c_o1.metric("Kenaikan Hasil", f"+{opt_delta_kg:,.0f} kg", f"{opt_res['yield_pct']:.1f}% Potensi")
            c_o2.metric("Revenue Tambahan", f"Rp {opt_delta_rev:,.0f}")
            c_o3.metric("ROI Optimasi", f"{opt_roi:.1f}%", help="Return on Investment dari modal tambahan ini")
            
            # Visualization: What did we buy?
            # Compare opt_params vs base_params_for_opt
            shopping_list = []
            
            # NPK Breakdown logic similar to previous table but diff source types
            # Simplified for display speed
            if opt_params['n'] > base_params_for_opt['n']:
                added = opt_params['n'] - base_params_for_opt['n']
                product_kg = added / 0.46
                shopping_list.append({"Item": "Urea", "Qty": f"+{product_kg:.1f} kg", "Alasan": "Fix Defisiensi Nitrogen"})
            
            if opt_params['p'] > base_params_for_opt['p']:
                added = opt_params['p'] - base_params_for_opt['p']
                product_kg = added / 0.36
                shopping_list.append({"Item": "SP-36", "Qty": f"+{product_kg:.1f} kg", "Alasan": "Fix Defisiensi Fosfor"})
                
            if opt_params['k'] > base_params_for_opt['k']:
                added = opt_params['k'] - base_params_for_opt['k']
                product_kg = added / 0.60
                shopping_list.append({"Item": "KCl", "Qty": f"+{product_kg:.1f} kg", "Alasan": "Fix Defisiensi Kalium"})

            if opt_params['ph'] > base_params_for_opt['ph']:
                # Crude calc
                shopping_list.append({"Item": "Dolomit/Kapur", "Qty": "Sesuai dosis", "Alasan": "Netralisasi pH Masam"})
            
            # Check ZPT/Boosters
            if opt_params['booster_kg'] > base_params_for_opt['booster_kg']:
                 shopping_list.append({"Item": "Kalium Booster", "Qty": f"+{opt_params['booster_kg']:.1f} kg", "Alasan": "Maksimalkan fase generatif"})
                 
            st.write("**Rekomendasi Belanja Prioritas:**")
            st.table(shopping_list)



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
