import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Kalkulator POC - AgriSensa",
    page_icon="🧪",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

# Recipe Management Functions
RECIPE_FILE = "data/poc_recipes.json"

def ensure_recipe_file():
    """Ensure recipe file and directory exist"""
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(RECIPE_FILE):
        with open(RECIPE_FILE, 'w') as f:
            json.dump({}, f)

def load_recipes():
    """Load all saved recipes"""
    ensure_recipe_file()
    try:
        with open(RECIPE_FILE, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_recipe(name, recipe_data):
    """Save a recipe"""
    recipes = load_recipes()
    recipes[name] = recipe_data
    with open(RECIPE_FILE, 'w') as f:
        json.dump(recipes, f, indent=2)

def delete_recipe(name):
    """Delete a recipe"""
    recipes = load_recipes()
    if name in recipes:
        del recipes[name]
        with open(RECIPE_FILE, 'w') as f:
            json.dump(recipes, f, indent=2)

# Header
st.title("🧪 Kalkulator Pupuk Organik Cair (POC)")
st.markdown("""
<div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 25px;">
    <h3 style="margin:0; color: white;">POC Formulator Pro</h3>
    <p style="margin:0; opacity: 0.9;">Hitung kandungan hara (N, P, K, C-Organik) dari berbagai bahan organik untuk 100 Liter POC</p>
</div>
""", unsafe_allow_html=True)

# Material Database with Nutrient Content
MATERIALS = {
    "Urine": {
        "Urine Sapi": {"N": 0.5, "P": 0.1, "K": 0.4, "C": 0.2, "unit": "liter", "price": 0},
        "Urine Kambing": {"N": 1.5, "P": 0.3, "K": 2.0, "C": 0.3, "unit": "liter", "price": 0},
        "Urine Kelinci": {"N": 2.5, "P": 0.5, "K": 1.2, "C": 0.4, "unit": "liter", "price": 0},
    },
    "Bahan Fermentasi": {
        "Sabut Kelapa (fermentasi)": {"N": 0.8, "P": 0.2, "K": 1.5, "C": 45, "unit": "kg", "price": 2000},
        "Debog Pisang (cacahan)": {"N": 0.3, "P": 0.1, "K": 3.5, "C": 35, "unit": "kg", "price": 1000},
        "Kulit Pisang (cacahan)": {"N": 0.5, "P": 0.2, "K": 4.0, "C": 40, "unit": "kg", "price": 1500},
        "Bonggol Pisang": {"N": 0.4, "P": 0.15, "K": 5.0, "C": 38, "unit": "kg", "price": 1000},
        "Daun Kelor": {"N": 2.5, "P": 0.4, "K": 1.5, "C": 42, "unit": "kg", "price": 3000},
    },
    "Pupuk Kimia (Fermentasi)": {
        "Urea (46-0-0)": {"N": 46, "P": 0, "K": 0, "C": 0, "unit": "kg", "price": 2500, "note": "Sumber N tinggi"},
        "ZA/Amonium Sulfat (21-0-0)": {"N": 21, "P": 0, "K": 0, "C": 0, "unit": "kg", "price": 1800, "note": "N + Sulfur"},
        "SP-36 (0-36-0)": {"N": 0, "P": 36, "K": 0, "C": 0, "unit": "kg", "price": 2300, "note": "Sumber P tinggi"},
        "TSP (0-46-0)": {"N": 0, "P": 46, "K": 0, "C": 0, "unit": "kg", "price": 2800, "note": "Triple Super Phosphate"},
        "KCl (0-0-60)": {"N": 0, "P": 0, "K": 60, "C": 0, "unit": "kg", "price": 3500, "note": "Sumber K tinggi"},
        "NPK Phonska (15-15-15)": {"N": 15, "P": 15, "K": 15, "C": 0, "unit": "kg", "price": 2400, "note": "NPK seimbang"},
        "NPK Mutiara (16-16-16)": {"N": 16, "P": 16, "K": 16, "C": 0, "unit": "kg", "price": 2600, "note": "NPK seimbang plus"},
        "NPK Pelangi (15-9-20)": {"N": 15, "P": 9, "K": 20, "C": 0, "unit": "kg", "price": 2500, "note": "Tinggi K untuk generatif"},
        "NPK Grower (27-7-7)": {"N": 27, "P": 7, "K": 7, "C": 0, "unit": "kg", "price": 2700, "note": "Tinggi N untuk vegetatif"},
        "KNO3/Kalium Nitrat (13-0-46)": {"N": 13, "P": 0, "K": 46, "C": 0, "unit": "kg", "price": 18000, "note": "Premium - larut sempurna"},
        "MKP/Mono Kalium Fosfat (0-52-34)": {"N": 0, "P": 52, "K": 34, "C": 0, "unit": "kg", "price": 25000, "note": "Premium - P+K tinggi"},
    },
    "Tambahan": {
        "Molase (Tetes Tebu)": {"N": 0.1, "P": 0.05, "K": 3.0, "C": 55, "unit": "liter", "price": 15000},
        "Dekomposer (EM4/MOL)": {"N": 0, "P": 0, "K": 0, "C": 0, "unit": "liter", "price": 25000},
    }
}

# Recipe Templates
TEMPLATES = {
    "Custom (Manual)": {},
    "High N (Vegetatif)": {
        "Urine Kelinci": 20,
        "Daun Kelor": 5,
        "Molase (Tetes Tebu)": 1.5,
        "Dekomposer (EM4/MOL)": 0.5
    },
    "High K (Generatif)": {
        "Bonggol Pisang": 8,
        "Kulit Pisang (cacahan)": 5,
        "Urine Kambing": 15,
        "Molase (Tetes Tebu)": 2,
        "Dekomposer (EM4/MOL)": 0.5
    },
    "Balanced NPK": {
        "Urine Sapi": 20,
        "Sabut Kelapa (fermentasi)": 5,
        "Debog Pisang (cacahan)": 5,
        "Daun Kelor": 3,
        "Molase (Tetes Tebu)": 1.5,
        "Dekomposer (EM4/MOL)": 0.75
    },
    "POC Kimia - Vegetatif (High N)": {
        "Urea (46-0-0)": 0.5,
        "NPK Phonska (15-15-15)": 1.0,
        "Molase (Tetes Tebu)": 2,
        "Dekomposer (EM4/MOL)": 0.5
    },
    "POC Kimia - Generatif (High K)": {
        "KCl (0-0-60)": 0.5,
        "NPK Pelangi (15-9-20)": 1.0,
        "Molase (Tetes Tebu)": 2,
        "Dekomposer (EM4/MOL)": 0.5
    },
    "POC Kimia - Premium": {
        "KNO3/Kalium Nitrat (13-0-46)": 0.3,
        "MKP/Mono Kalium Fosfat (0-52-34)": 0.2,
        "Molase (Tetes Tebu)": 1.5,
        "Dekomposer (EM4/MOL)": 0.5
    }
}

# Sidebar - Recipe Selection & Inputs
with st.sidebar:
    st.header("⚙️ Konfigurasi Resep")
    
    # AI Optimizer Toggle
    use_ai_optimizer = st.checkbox("🤖 Gunakan AI Optimizer", value=False, 
                                     help="AI akan merekomendasikan formula optimal berdasarkan target NPK dan budget")
    
    if use_ai_optimizer:
        st.divider()
        st.subheader("🎯 Target AI Optimizer")
        
        target_type = st.selectbox("Tipe Tanaman", 
                                    ["Vegetatif (Daun)", "Generatif (Bunga/Buah)", "Balanced"],
                                    help="AI akan optimize NPK sesuai fase tanaman")
        
        budget_limit = st.number_input("Budget Maksimal (Rp)", value=50000, min_value=0, step=5000,
                                        help="AI akan cari kombinasi paling efisien dalam budget")
        
        prefer_organic = st.slider("Preferensi Organik (%)", 0, 100, 50,
                                     help="0% = Full Kimia, 100% = Full Organik")
        
        if st.button("🚀 Generate Formula AI", type="primary", use_container_width=True):
            st.session_state['ai_generated'] = True
            st.session_state['target_type'] = target_type
            st.session_state['budget_limit'] = budget_limit
            st.session_state['prefer_organic'] = prefer_organic
            st.rerun()
    
    st.divider()
    st.subheader("💾 Resep Tersimpan")
    
    # Load saved recipes
    saved_recipes = load_recipes()
    
    # Load Recipe
    if saved_recipes:
        recipe_names = ["-- Pilih Resep --"] + list(saved_recipes.keys())
        selected_recipe = st.selectbox("Load Resep", recipe_names, key="load_recipe")
        
        col_load, col_del = st.columns(2)
        with col_load:
            if st.button("📂 Load", use_container_width=True, disabled=(selected_recipe == "-- Pilih Resep --")):
                if selected_recipe != "-- Pilih Resep --":
                    recipe_data = saved_recipes[selected_recipe]
                    st.session_state['loaded_recipe'] = recipe_data
                    st.success(f"✅ Loaded: {selected_recipe}")
                    st.rerun()
        
        with col_del:
            if st.button("🗑️ Hapus", use_container_width=True, disabled=(selected_recipe == "-- Pilih Resep --")):
                if selected_recipe != "-- Pilih Resep --":
                    delete_recipe(selected_recipe)
                    st.success(f"🗑️ Deleted: {selected_recipe}")
                    st.rerun()
    else:
        st.info("Belum ada resep tersimpan")
    
    # Save Current Recipe
    st.markdown("**Simpan Resep Saat Ini:**")
    recipe_name = st.text_input("Nama Resep", placeholder="Misal: POC Cabai Terbaik", key="recipe_name")
    if st.button("💾 Simpan Resep", type="primary", use_container_width=True, disabled=(not recipe_name)):
        # Will save after inputs are populated
        st.session_state['save_recipe_name'] = recipe_name
        st.session_state['save_recipe_flag'] = True
    
    st.divider()
    # Template selection
    template = st.selectbox("Pilih Template Resep", list(TEMPLATES.keys()))
    
    st.divider()
    st.subheader("📊 Target Volume")
    target_volume = st.number_input("Volume POC (Liter)", value=100, min_value=10, max_value=1000, step=10)
    
    # Water price input
    water_price = st.number_input("Harga Air Bersih (Rp/Liter)", value=0, min_value=0, step=10, 
                                   help="Opsional: Input biaya air bersih jika ada")
    
    st.divider()
    st.subheader("🧪 Komposisi Bahan")
    
    # Initialize inputs and prices
    inputs = {}
    custom_prices = {}
    
    # Check if recipe was loaded
    if st.session_state.get('loaded_recipe'):
        loaded_data = st.session_state['loaded_recipe']
        st.success(f"📂 Resep dimuat: {loaded_data.get('name', 'Unknown')}")
        inputs = loaded_data.get('materials', {})
        custom_prices = loaded_data.get('prices', {})
        target_volume = loaded_data.get('volume', 100)
        # Clear loaded flag
        del st.session_state['loaded_recipe']
    # Load template if selected
    elif template != "Custom (Manual)":
        st.info(f"📋 Template: **{template}**")
        for material, qty in TEMPLATES[template].items():
            inputs[material] = qty
    
    # Input for each category
    for category, materials in MATERIALS.items():
        with st.expander(f"**{category}**", expanded=(template == "Custom (Manual)")):
            for material, props in materials.items():
                # Get default value from template or 0
                default_val = inputs.get(material, 0.0)
                
                # Create two columns for quantity and price
                col_qty, col_price = st.columns([2, 1])
                
                with col_qty:
                    qty = st.number_input(
                        f"{material} ({props['unit']})",
                        value=float(default_val),
                        min_value=0.0,
                        step=0.5,
                        key=f"qty_{material}"
                    )
                
                with col_price:
                    price = st.number_input(
                        f"Harga/{props['unit']}",
                        value=props['price'],
                        min_value=0,
                        step=100,
                        key=f"price_{material}",
                        help=f"Default: Rp {props['price']:,}"
                    )
                
                if qty > 0:
                    inputs[material] = qty
                    custom_prices[material] = price

# Save Recipe Logic
if st.session_state.get('save_recipe_flag', False) and inputs:
    recipe_name = st.session_state.get('save_recipe_name', '')
    if recipe_name:
        recipe_data = {
            'name': recipe_name,
            'materials': inputs.copy(),
            'prices': custom_prices.copy(),
            'volume': target_volume,
            'saved_date': datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        save_recipe(recipe_name, recipe_data)
        st.success(f"💾 Resep '{recipe_name}' berhasil disimpan!")
        st.session_state['save_recipe_flag'] = False
        st.rerun()

# AI Optimizer Logic
if st.session_state.get('ai_generated', False):
    target_type = st.session_state.get('target_type', 'Balanced')
    budget = st.session_state.get('budget_limit', 50000)
    organic_pref = st.session_state.get('prefer_organic', 50)
    
    st.info(f"🤖 **AI Optimizer Aktif:** Target {target_type}, Budget Rp {budget:,}, Preferensi Organik {organic_pref}%")
    
    # AI Logic: Smart material selection based on target
    ai_inputs = {}
    ai_prices = {}
    
    # Base: Always add molase + dekomposer
    ai_inputs["Molase (Tetes Tebu)"] = 1.5
    ai_inputs["Dekomposer (EM4/MOL)"] = 0.5
    ai_prices["Molase (Tetes Tebu)"] = MATERIALS["Tambahan"]["Molase (Tetes Tebu)"]["price"]
    ai_prices["Dekomposer (EM4/MOL)"] = MATERIALS["Tambahan"]["Dekomposer (EM4/MOL)"]["price"]
    
    remaining_budget = budget - (ai_inputs["Molase (Tetes Tebu)"] * ai_prices["Molase (Tetes Tebu)"]) - (ai_inputs["Dekomposer (EM4/MOL)"] * ai_prices["Dekomposer (EM4/MOL)"])
    
    if organic_pref >= 70:  # High organic preference
        if target_type == "Vegetatif (Daun)":
            ai_inputs["Urine Kelinci"] = min(20, remaining_budget / 100)
            ai_inputs["Daun Kelor"] = min(5, (remaining_budget - 20*100) / 3000)
        elif target_type == "Generatif (Bunga/Buah)":
            ai_inputs["Bonggol Pisang"] = min(8, remaining_budget / 1000)
            ai_inputs["Kulit Pisang (cacahan)"] = min(5, (remaining_budget - 8000) / 1500)
        else:  # Balanced
            ai_inputs["Urine Sapi"] = min(15, remaining_budget / 100)
            ai_inputs["Sabut Kelapa (fermentasi)"] = min(5, (remaining_budget - 1500) / 2000)
    elif organic_pref <= 30:  # High chemical preference
        if target_type == "Vegetatif (Daun)":
            ai_inputs["Urea (46-0-0)"] = min(0.5, remaining_budget / 2500)
            ai_inputs["NPK Phonska (15-15-15)"] = min(1.0, (remaining_budget - 1250) / 2400)
        elif target_type == "Generatif (Bunga/Buah)":
            ai_inputs["KCl (0-0-60)"] = min(0.5, remaining_budget / 3500)
            ai_inputs["NPK Pelangi (15-9-20)"] = min(1.0, (remaining_budget - 1750) / 2500)
        else:  # Balanced
            ai_inputs["NPK Phonska (15-15-15)"] = min(1.5, remaining_budget / 2400)
    else:  # Mixed (50/50)
        if target_type == "Vegetatif (Daun)":
            ai_inputs["Urine Kelinci"] = min(10, remaining_budget * 0.3 / 100)
            ai_inputs["Daun Kelor"] = min(3, remaining_budget * 0.3 / 3000)
            ai_inputs["Urea (46-0-0)"] = min(0.3, remaining_budget * 0.4 / 2500)
        elif target_type == "Generatif (Bunga/Buah)":
            ai_inputs["Bonggol Pisang"] = min(5, remaining_budget * 0.3 / 1000)
            ai_inputs["KCl (0-0-60)"] = min(0.3, remaining_budget * 0.4 / 3500)
            ai_inputs["NPK Pelangi (15-9-20)"] = min(0.5, remaining_budget * 0.3 / 2500)
        else:  # Balanced
            ai_inputs["Urine Sapi"] = min(10, remaining_budget * 0.3 / 100)
            ai_inputs["NPK Phonska (15-15-15)"] = min(0.8, remaining_budget * 0.4 / 2400)
            ai_inputs["Sabut Kelapa (fermentasi)"] = min(3, remaining_budget * 0.3 / 2000)
    
    # Update inputs and prices with AI recommendations
    for material, qty in ai_inputs.items():
        if qty > 0:
            inputs[material] = qty
            # Find price
            for cat_materials in MATERIALS.values():
                if material in cat_materials:
                    custom_prices[material] = cat_materials[material]["price"]
                    break
    
    # Clear AI flag
    st.session_state['ai_generated'] = False

# Main Content
if inputs:
    # Calculate total nutrients - separated by source
    # Organic sources
    organic_N = organic_P = organic_K = organic_C = organic_cost = 0
    # Chemical sources  
    chemical_N = chemical_P = chemical_K = chemical_cost = 0
    # Combined totals
    total_N = total_P = total_K = total_C = total_cost = 0
    total_solid = total_liquid = 0
    
    material_breakdown = []
    
    for material, qty in inputs.items():
        # Find material props and category
        props = None
        category = None
        for cat_name, cat_materials in MATERIALS.items():
            if material in cat_materials:
                props = cat_materials[material]
                category = cat_name
                break
        
        if props:
            # Calculate nutrients
            n_contrib = (qty * props['N']) / 100
            p_contrib = (qty * props['P']) / 100
            k_contrib = (qty * props['K']) / 100
            c_contrib = (qty * props['C']) / 100
            
            # Use custom price if available, otherwise use default
            material_price = custom_prices.get(material, props['price'])
            cost = qty * material_price
            
            # Categorize as organic or chemical
            is_chemical = (category == "Pupuk Kimia (Fermentasi)")
            
            if is_chemical:
                chemical_N += n_contrib
                chemical_P += p_contrib
                chemical_K += k_contrib
                chemical_cost += cost
            else:
                organic_N += n_contrib
                organic_P += p_contrib
                organic_K += k_contrib
                organic_C += c_contrib
                organic_cost += cost
            
            # Add to totals
            total_N += n_contrib
            total_P += p_contrib
            total_K += k_contrib
            total_C += c_contrib
            total_cost += cost
            
            if props['unit'] == 'kg':
                total_solid += qty
            else:
                total_liquid += qty
            
            material_breakdown.append({
                "Kategori": "🧪 Kimia" if is_chemical else "🌿 Organik",
                "Bahan": material,
                "Jumlah": f"{qty} {props['unit']}",
                "Harga Satuan": f"Rp {material_price:,.0f}",
                "N (%)": f"{props['N']}",
                "P (%)": f"{props['P']}",
                "K (%)": f"{props['K']}",
                "Kontribusi N": f"{n_contrib:.2f} unit",
                "Kontribusi P": f"{p_contrib:.2f} unit",
                "Kontribusi K": f"{k_contrib:.2f} unit",
                "Biaya": f"Rp {cost:,.0f}"
            })
    
    # Calculate concentrations per 100L
    n_pct = (total_N / target_volume) * 100
    p_pct = (total_P / target_volume) * 100
    k_pct = (total_K / target_volume) * 100
    c_pct = (total_C / target_volume) * 100
    
    # Calculate C/N ratio
    cn_ratio = (total_C / total_N) if total_N > 0 else 0
    
    # Water needed and cost
    water_needed = target_volume - total_liquid
    water_cost = water_needed * water_price
    total_cost_with_water = total_cost + water_cost
    
    # Display Results
    st.markdown("## 📊 Hasil Analisis POC")
    
    # Summary Metrics - Row 1: NPK + C-Organic
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nitrogen (N)", f"{n_pct:.2f}%", help="Kandungan Nitrogen total")
    
    with col2:
        st.metric("Fosfor (P)", f"{p_pct:.2f}%", help="Kandungan Fosfor total")
    
    with col3:
        st.metric("Kalium (K)", f"{k_pct:.2f}%", help="Kandungan Kalium total")
    
    with col4:
        st.metric("C-Organik", f"{c_pct:.1f}%", help="Kandungan Karbon Organik")
    
    # Summary Metrics - Row 2: Water + Cost
    st.markdown("---")
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Air Bersih Dibutuhkan", f"{water_needed:.1f} L", 
                 help=f"Air untuk mencapai volume {target_volume} L")
    
    with col6:
        st.metric("Biaya Air", f"Rp {water_cost:,.0f}", 
                 help=f"{water_needed:.1f} L x Rp {water_price:,.0f}/L")
    
    with col7:
        st.metric("Biaya Bahan", f"Rp {total_cost:,.0f}", 
                 help="Total biaya semua bahan organik")
    
    with col8:
        st.metric("Total Biaya POC", f"Rp {total_cost_with_water:,.0f}", 
                 delta=f"Rp {total_cost_with_water/target_volume:.0f}/L",
                 help="Biaya bahan + air per liter POC")
    
    # 3-Way Comparison: Organic vs Chemical vs Combined
    st.markdown("---")
    st.subheader("📊 Perbandingan Kontribusi Hara")
    
    # Calculate percentages for each source
    organic_n_pct = (organic_N / target_volume) * 100
    organic_p_pct = (organic_P / target_volume) * 100
    organic_k_pct = (organic_K / target_volume) * 100
    
    chemical_n_pct = (chemical_N / target_volume) * 100
    chemical_p_pct = (chemical_P / target_volume) * 100
    chemical_k_pct = (chemical_K / target_volume) * 100
    
    # Create comparison dataframe
    comparison_data = {
        "Sumber": ["🌿 Organik", "🧪 Kimia", "🔄 Gabungan"],
        "N (%)": [f"{organic_n_pct:.2f}", f"{chemical_n_pct:.2f}", f"{n_pct:.2f}"],
        "P (%)": [f"{organic_p_pct:.2f}", f"{chemical_p_pct:.2f}", f"{p_pct:.2f}"],
        "K (%)": [f"{organic_k_pct:.2f}", f"{chemical_k_pct:.2f}", f"{k_pct:.2f}"],
        "C-Organik (%)": [f"{(organic_C/target_volume)*100:.1f}", "0.0", f"{c_pct:.1f}"],
        "Biaya": [f"Rp {organic_cost:,.0f}", f"Rp {chemical_cost:,.0f}", f"Rp {total_cost:,.0f}"]
    }
    df_comparison = pd.DataFrame(comparison_data)
    
    col_comp1, col_comp2 = st.columns([2, 1])
    
    with col_comp1:
        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
    
    with col_comp2:
        st.markdown("**💡 Insight:**")
        if chemical_N > 0 or chemical_P > 0 or chemical_K > 0:
            st.info(f"""
            - Organik: {(organic_cost/total_cost*100):.1f}% biaya
            - Kimia: {(chemical_cost/total_cost*100):.1f}% biaya
            - Kombinasi memberikan NPK lebih tinggi
            """)
        else:
            st.success("100% Organik - Ramah lingkungan!")
    
    # NPK Ratio & C/N Ratio
    st.markdown("---")
    col_r1, col_r2, col_r3 = st.columns(3)
    
    with col_r1:
        # Calculate NPK ratio
        if total_N > 0 and total_P > 0 and total_K > 0:
            min_val = min(total_N, total_P, total_K)
            ratio_n = total_N / min_val
            ratio_p = total_P / min_val
            ratio_k = total_K / min_val
            st.metric("Rasio NPK", f"{ratio_n:.1f} : {ratio_p:.1f} : {ratio_k:.1f}")
        else:
            st.metric("Rasio NPK", "N/A")
    
    with col_r2:
        st.metric("Rasio C/N", f"{cn_ratio:.1f}", 
                 delta="Optimal" if 25 <= cn_ratio <= 30 else "Perlu Penyesuaian",
                 help="Rasio C/N optimal: 25-30")
    
    with col_r3:
        st.metric("Total Biaya", f"Rp {total_cost:,.0f}")
    
    # Visualizations
    st.markdown("---")
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("📈 Kandungan Hara (NPK)")
        fig_npk = go.Figure(data=[
            go.Bar(name='N', x=['Nitrogen'], y=[n_pct], marker_color='#10b981'),
            go.Bar(name='P', x=['Fosfor'], y=[p_pct], marker_color='#f59e0b'),
            go.Bar(name='K', x=['Kalium'], y=[k_pct], marker_color='#3b82f6')
        ])
        fig_npk.update_layout(height=300, showlegend=True, yaxis_title="Konsentrasi (%)")
        st.plotly_chart(fig_npk, use_container_width=True)
    
    with col_v2:
        st.subheader("🥧 Komposisi Bahan")
        # Pie chart of material quantities
        materials_for_pie = []
        quantities_for_pie = []
        for material, qty in inputs.items():
            materials_for_pie.append(material[:20])  # Truncate long names
            quantities_for_pie.append(qty)
        
        fig_pie = go.Figure(data=[go.Pie(labels=materials_for_pie, values=quantities_for_pie)])
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Material Breakdown Table
    st.markdown("---")
    st.subheader("📋 Rincian Bahan & Kontribusi Hara")
    df_breakdown = pd.DataFrame(material_breakdown)
    st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
    
    # Mixing Instructions
    st.markdown("---")
    st.subheader("🔬 Instruksi Pembuatan POC")
    
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.markdown("**📝 Langkah-langkah:**")
        st.markdown(f"""
        1. **Siapkan wadah** berkapasitas minimal {target_volume + 20} liter
        2. **Masukkan bahan padat** ({total_solid:.1f} kg) yang sudah dicacah halus
        3. **Tambahkan urine** ({total_liquid:.1f} liter) jika ada
        4. **Tambahkan molase** untuk sumber energi mikroba
        5. **Masukkan dekomposer** (EM4/MOL) sebagai starter
        6. **Tambahkan air bersih** sebanyak {water_needed:.1f} liter
        7. **Aduk rata** dan tutup rapat (beri lubang udara kecil)
        8. **Fermentasi** selama 14-21 hari
        9. **Aduk setiap 3 hari** untuk aerasi
        10. **POC siap** saat bau tidak menyengat dan berwarna coklat kehitaman
        """)
    
    with col_i2:
        st.markdown("**⏱️ Timeline Fermentasi:**")
        
        # Fermentation timeline
        today = datetime.now()
        timeline_data = [
            {"Hari": "0", "Aktivitas": "Pencampuran bahan", "Tanggal": today.strftime("%d %b")},
            {"Hari": "3", "Aktivitas": "Pengadukan pertama", "Tanggal": (today + timedelta(days=3)).strftime("%d %b")},
            {"Hari": "7", "Aktivitas": "Pengadukan kedua", "Tanggal": (today + timedelta(days=7)).strftime("%d %b")},
            {"Hari": "14", "Aktivitas": "Cek kematangan (minimal)", "Tanggal": (today + timedelta(days=14)).strftime("%d %b")},
            {"Hari": "21", "Aktivitas": "POC siap panen (optimal)", "Tanggal": (today + timedelta(days=21)).strftime("%d %b")},
        ]
        df_timeline = pd.DataFrame(timeline_data)
        st.dataframe(df_timeline, use_container_width=True, hide_index=True)
        
        st.markdown(f"""
        **🌡️ Kondisi Optimal:**
        - Suhu: 25-35°C
        - pH target: 6.5-7.5
        - Kelembaban: 60-70%
        """)
    
    # Application Guide
    st.markdown("---")
    st.subheader("💧 Panduan Aplikasi")
    
    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        st.markdown("**🌱 Fase Vegetatif:**")
        st.info(f"""
        - Pengenceran: 1 : 10 (POC : Air)
        - Dosis: 500 ml POC + 5 L air
        - Frekuensi: 1x per minggu
        - Aplikasi: Siram ke tanah/semprot daun
        """)
    
    with col_a2:
        st.markdown("**🌸 Fase Generatif:**")
        st.info(f"""
        - Pengenceran: 1 : 8 (POC : Air)
        - Dosis: 500 ml POC + 4 L air
        - Frekuensi: 2x per minggu
        - Aplikasi: Siram ke tanah
        """)
    
    with col_a3:
        st.markdown("**🌾 Fase Pemeliharaan:**")
        st.info(f"""
        - Pengenceran: 1 : 15 (POC : Air)
        - Dosis: 500 ml POC + 7.5 L air
        - Frekuensi: 1x per 2 minggu
        - Aplikasi: Siram ke tanah
        """)
    
    # Quality Indicators
    st.markdown("---")
    st.subheader("✅ Indikator Kualitas POC")
    
    quality_score = 0
    quality_notes = []
    
    # Check C/N ratio
    if 25 <= cn_ratio <= 30:
        quality_score += 25
        quality_notes.append("✅ Rasio C/N optimal (25-30)")
    else:
        quality_notes.append(f"⚠️ Rasio C/N {cn_ratio:.1f} (optimal: 25-30)")
    
    # Check NPK balance
    if 0.5 <= ratio_n <= 3 and 0.5 <= ratio_p <= 2 and 0.5 <= ratio_k <= 4:
        quality_score += 25
        quality_notes.append("✅ Rasio NPK seimbang")
    else:
        quality_notes.append("⚠️ Rasio NPK perlu penyesuaian")
    
    # Check total nutrients
    total_npk = n_pct + p_pct + k_pct
    if total_npk >= 2:
        quality_score += 25
        quality_notes.append(f"✅ Total NPK mencukupi ({total_npk:.2f}%)")
    else:
        quality_notes.append(f"⚠️ Total NPK rendah ({total_npk:.2f}%)")
    
    # Check C-Organic
    if c_pct >= 10:
        quality_score += 25
        quality_notes.append(f"✅ C-Organik tinggi ({c_pct:.1f}%)")
    else:
        quality_notes.append(f"⚠️ C-Organik rendah ({c_pct:.1f}%)")
    
    col_q1, col_q2 = st.columns([1, 2])
    
    with col_q1:
        st.metric("Skor Kualitas", f"{quality_score}/100", 
                 delta="Excellent" if quality_score >= 75 else "Good" if quality_score >= 50 else "Needs Improvement")
    
    with col_q2:
        for note in quality_notes:
            st.markdown(note)
    
    # Dilution Calculator
    st.markdown("---")
    st.subheader("🧮 Kalkulator Pengenceran & Aplikasi")
    
    col_dil1, col_dil2 = st.columns(2)
    
    with col_dil1:
        st.markdown("**💧 Pengenceran POC:**")
        dilution_ratio = st.selectbox("Rasio Pengenceran", 
                                       ["1:5 (Sangat Pekat)", "1:10 (Vegetatif)", "1:15 (Pemeliharaan)", "1:20 (Ringan)", "Custom"],
                                       help="Pilih rasio sesuai fase tanaman")
        
        if dilution_ratio == "Custom":
            custom_ratio = st.number_input("POC : Air (1:X)", value=10, min_value=1, max_value=50)
            ratio_value = custom_ratio
        else:
            ratio_value = int(dilution_ratio.split(":")[1].split()[0])
        
        poc_volume_available = st.number_input("Volume POC Tersedia (Liter)", value=float(target_volume), min_value=0.1, step=0.5)
        
        # Calculate dilution
        water_for_dilution = poc_volume_available * ratio_value
        total_solution = poc_volume_available + water_for_dilution
        
        st.success(f"""
        **Hasil Pengenceran:**
        - POC: {poc_volume_available:.1f} L
        - Air: {water_for_dilution:.1f} L
        - Total Larutan: {total_solution:.1f} L
        """)
    
    with col_dil2:
        st.markdown("**🌾 Estimasi Aplikasi:**")
        application_method = st.radio("Metode Aplikasi", ["Siram ke Tanah", "Semprot Daun"])
        
        if application_method == "Siram ke Tanah":
            dose_per_plant = st.number_input("Dosis per Tanaman (ml)", value=500, min_value=100, max_value=2000, step=100)
            plants_covered = int((total_solution * 1000) / dose_per_plant)
            st.metric("Jumlah Tanaman", f"{plants_covered:,} pohon", 
                     help=f"{total_solution:.1f}L ÷ {dose_per_plant}ml/pohon")
        else:
            coverage_per_liter = st.number_input("Coverage per Liter (m²)", value=20, min_value=5, max_value=50, step=5)
            area_covered = total_solution * coverage_per_liter
            st.metric("Luas Area", f"{area_covered:,.0f} m²", 
                     help=f"{total_solution:.1f}L × {coverage_per_liter}m²/L")
        
        # Cost per application
        cost_per_liter_solution = total_cost_with_water / total_solution if total_solution > 0 else 0
        st.metric("Biaya per Liter Larutan", f"Rp {cost_per_liter_solution:,.0f}")
    
    # Crop-Specific Recommendations
    st.markdown("---")
    st.subheader("🎯 Rekomendasi Spesifik Tanaman")
    
    # Crop database with ideal NPK
    CROP_NPK = {
        "Cabai": {"N": 0.3, "P": 0.2, "K": 0.4, "phase": "Generatif", "note": "Tinggi K untuk buah"},
        "Tomat": {"N": 0.25, "P": 0.25, "K": 0.35, "phase": "Generatif", "note": "Balanced NPK"},
        "Padi": {"N": 0.4, "P": 0.15, "K": 0.2, "phase": "Vegetatif", "note": "Tinggi N untuk anakan"},
        "Jagung": {"N": 0.35, "P": 0.2, "K": 0.25, "phase": "Vegetatif", "note": "Tinggi N untuk batang"},
        "Sawi": {"N": 0.5, "P": 0.1, "K": 0.15, "phase": "Vegetatif", "note": "Sangat tinggi N untuk daun"},
        "Kangkung": {"N": 0.45, "P": 0.1, "K": 0.15, "phase": "Vegetatif", "note": "Tinggi N untuk daun"},
        "Terong": {"N": 0.3, "P": 0.2, "K": 0.35, "phase": "Generatif", "note": "Balanced untuk buah"},
        "Timun": {"N": 0.25, "P": 0.15, "K": 0.4, "phase": "Generatif", "note": "Tinggi K untuk buah"},
        "Bawang Merah": {"N": 0.2, "P": 0.25, "K": 0.45, "phase": "Generatif", "note": "Tinggi K untuk umbi"},
        "Kentang": {"N": 0.25, "P": 0.2, "K": 0.4, "phase": "Generatif", "note": "Tinggi K untuk umbi"},
    }
    
    selected_crop = st.selectbox("Pilih Tanaman Target", list(CROP_NPK.keys()))
    
    if selected_crop:
        crop_data = CROP_NPK[selected_crop]
        
        col_crop1, col_crop2, col_crop3 = st.columns(3)
        
        with col_crop1:
            st.markdown(f"**Target NPK untuk {selected_crop}:**")
            st.info(f"""
            - N: {crop_data['N']}%
            - P: {crop_data['P']}%
            - K: {crop_data['K']}%
            - Fase: {crop_data['phase']}
            """)
        
        with col_crop2:
            st.markdown("**NPK POC Anda:**")
            st.success(f"""
            - N: {n_pct:.2f}%
            - P: {p_pct:.2f}%
            - K: {k_pct:.2f}%
            """)
        
        with col_crop3:
            st.markdown("**Kesesuaian:**")
            n_match = abs(n_pct - crop_data['N']) < 0.1
            p_match = abs(p_pct - crop_data['P']) < 0.1
            k_match = abs(k_pct - crop_data['K']) < 0.1
            
            match_score = sum([n_match, p_match, k_match])
            
            if match_score == 3:
                st.success("✅ Sangat Sesuai!")
            elif match_score == 2:
                st.info("👍 Cukup Sesuai")
            else:
                st.warning("⚠️ Perlu Penyesuaian")
            
            st.caption(crop_data['note'])
        
        # Recommendations
        st.markdown("**💡 Saran Penyesuaian:**")
        suggestions = []
        
        if n_pct < crop_data['N'] - 0.1:
            suggestions.append(f"➕ Tambah sumber N (Urea/Urine Kelinci) untuk mencapai {crop_data['N']}%")
        elif n_pct > crop_data['N'] + 0.1:
            suggestions.append(f"➖ Kurangi sumber N, target {crop_data['N']}%")
        
        if p_pct < crop_data['P'] - 0.1:
            suggestions.append(f"➕ Tambah sumber P (SP-36/TSP) untuk mencapai {crop_data['P']}%")
        elif p_pct > crop_data['P'] + 0.1:
            suggestions.append(f"➖ Kurangi sumber P, target {crop_data['P']}%")
        
        if k_pct < crop_data['K'] - 0.1:
            suggestions.append(f"➕ Tambah sumber K (KCl/Bonggol Pisang) untuk mencapai {crop_data['K']}%")
        elif k_pct > crop_data['K'] + 0.1:
            suggestions.append(f"➖ Kurangi sumber K, target {crop_data['K']}%")
        
        if suggestions:
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
        else:
            st.success("✅ Formula POC sudah optimal untuk " + selected_crop + "!")

else:
    st.info("👈 Silakan pilih template atau input bahan di sidebar untuk mulai menghitung POC")

# Footer
st.markdown("---")
st.caption("💡 **Tips:** POC terbaik menggunakan kombinasi bahan dengan rasio C/N optimal (25-30) dan NPK seimbang sesuai kebutuhan tanaman.")
