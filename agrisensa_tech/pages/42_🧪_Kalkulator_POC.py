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

def delete_recipe(recipe_name):
    """Delete a recipe"""
    recipes = load_recipes()
    if recipe_name in recipes:
        del recipes[recipe_name]
        with open(RECIPE_FILE, 'w') as f:
            json.dump(recipes, f, indent=2)

# Helper function to calculate NPK from formula
def calculate_npk_from_formula(inputs, target_volume=100):
    """Calculate NPK content from material inputs without UI"""
    total_N = 0
    total_P = 0
    total_K = 0
    total_C = 0
    total_liquid = 0
    total_cost = 0
    
    for material, qty in inputs.items():
        # Find material in database
        found = False
        for category, materials in MATERIALS.items():
            if material in materials:
                props = materials[material]
                
                # Calculate nutrients
                total_N += (props['N'] / 100) * qty
                total_P += (props['P'] / 100) * qty
                total_K += (props['K'] / 100) * qty
                total_C += (props['C'] / 100) * qty
                
                # Calculate liquid volume
                if props['unit'] == 'liter':
                    total_liquid += qty
                
                # Calculate cost
                total_cost += props['price'] * qty
                
                found = True
                break
    
    # Calculate percentages
    n_pct = (total_N / target_volume) * 100 if target_volume > 0 else 0
    p_pct = (total_P / target_volume) * 100 if target_volume > 0 else 0
    k_pct = (total_K / target_volume) * 100 if target_volume > 0 else 0
    c_pct = (total_C / target_volume) * 100 if target_volume > 0 else 0
    
    return {
        'N': n_pct,
        'P': p_pct,
        'K': k_pct,
        'C': c_pct,
        'total_cost': total_cost,
        'total_liquid': total_liquid
    }

# Header
st.title("🧪 Kalkulator Pupuk Organik Cair (POC)")
st.markdown("""
<div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 25px;">
    <h3 style="margin:0; color: white;">POC Formulator Pro</h3>
    <p style="margin:0; opacity: 0.9;">Hitung kandungan hara (N, P, K, C-Organik) dari berbagai bahan organik untuk 100 Liter POC</p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["🧪 Kalkulator POC", "💼 Business Model"])

with tab1:
    # Detect mode: Business Model AI or Manual Input
    is_business_mode = st.session_state.get('ai_formula') is not None
    
    if is_business_mode:
        # Business Mode Header
        st.success("🤖 **Mode: Business Model AI** - Formula otomatis dari rekomendasi bisnis")
        col_mode1, col_mode2 = st.columns([3, 1])
        with col_mode1:
            formula_name = st.session_state.get('ai_formula_name', 'AI Formula')
            st.info(f"📋 Formula: **{formula_name}**")
        with col_mode2:
            if st.button("🔄 Reset ke Mode Manual", use_container_width=True):
                if 'ai_formula' in st.session_state:
                    del st.session_state['ai_formula']
                if 'ai_formula_name' in st.session_state:
                    del st.session_state['ai_formula_name']
                st.rerun()
    else:
        # Personal Mode Header
        st.info("✋ **Mode: Input Manual** - Kontrol penuh untuk eksperimen formula")

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
    
    # Check mode
    is_business_mode = st.session_state.get('ai_formula') is not None
    
    if is_business_mode:
        # Business Mode: Locked sidebar
        st.warning("🔒 **Mode: Business Model AI**")
        st.caption("Formula dikontrol dari tab Business Model")
        st.caption("Volume dan bahan otomatis ter-scale")
        st.divider()
        st.info("💡 Untuk ubah formula, gunakan tab **Business Model** atau klik **Reset ke Mode Manual**")
    else:
        # Personal Mode: Full controls
        st.info("💡 **AI Optimizer** ada di tab **Business Model** untuk rekomendasi lengkap")
    
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
    
    # Check if there's a drum capacity from Business Model
    business_drums = st.session_state.get('ai_drums', 0)
    if business_drums > 0:
        use_drum_capacity = st.checkbox(
            f"🏭 Gunakan Kapasitas Drum ({business_drums} × 1000L = {business_drums * 1000}L)",
            value=False,
            help="Sinkronkan dengan setup produksi di Business Model"
        )
        if use_drum_capacity:
            target_volume = business_drums * 1000
            st.info(f"✅ Volume disesuaikan dengan kapasitas drum: **{target_volume:,} L**")
        else:
            target_volume = st.number_input("Volume POC (Liter)", value=100, min_value=10, max_value=10000, step=10)
    else:
        target_volume = st.number_input("Volume POC (Liter)", value=100, min_value=10, max_value=10000, step=10)
    
    # Water price input
    water_price = st.number_input("Harga Air Bersih (Rp/Liter)", value=0, min_value=0, step=10, 
                                   help="Opsional: Input biaya air bersih jika ada")
    
    st.divider()
    st.subheader("🧪 Komposisi Bahan")
    
    # Initialize inputs and prices
    inputs = {}
    custom_prices = {}
    
    # Check if AI formula was recommended
    if st.session_state.get('ai_formula'):
        formula_data = st.session_state['ai_formula']
        formula_name = st.session_state.get('ai_formula_name', 'AI Recommendation')
        st.success(f"🤖 Formula AI: **{formula_name}**")
        
        # Scale formula based on target volume (formula is for 100L base)
        scale_factor = target_volume / 100
        inputs = {material: qty * scale_factor for material, qty in formula_data.items()}
        
        if scale_factor != 1:
            st.info(f"📐 Formula di-scale {scale_factor}x untuk volume {target_volume}L")
        
        # DON'T delete AI formula - keep it for Business Model tab
        # It will be cleared when user clicks Reset button
    # Check if recipe was loaded
    elif st.session_state.get('loaded_recipe'):
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
    
    # Application Schedule Generator
    st.markdown("---")
    st.subheader("📱 Jadwal Aplikasi POC")
    
    col_sch1, col_sch2 = st.columns([1, 2])
    
    with col_sch1:
        st.markdown("**⚙️ Konfigurasi Jadwal:**")
        planting_date = st.date_input("Tanggal Tanam", value=datetime.now())
        crop_cycle_days = st.number_input("Siklus Tanaman (hari)", value=90, min_value=30, max_value=365, step=10)
        application_frequency = st.selectbox("Frekuensi Aplikasi", 
                                             ["Setiap 7 hari", "Setiap 10 hari", "Setiap 14 hari", "Custom"])
        
        if application_frequency == "Custom":
            custom_freq = st.number_input("Interval (hari)", value=7, min_value=3, max_value=30)
            freq_days = custom_freq
        else:
            freq_days = int(application_frequency.split()[1])
        
        num_applications = crop_cycle_days // freq_days
        total_poc_needed = (total_solution / ratio_value) * num_applications  # POC concentrate needed
    
    with col_sch2:
        st.markdown("**📅 Kalender Aplikasi:**")
        
        schedule_data = []
        current_date = planting_date
        
        for i in range(num_applications):
            app_date = current_date + timedelta(days=i * freq_days)
            day_after_planting = i * freq_days
            
            # Determine phase
            if day_after_planting < crop_cycle_days * 0.4:
                phase = "🌱 Vegetatif"
                recommended_ratio = "1:10"
            elif day_after_planting < crop_cycle_days * 0.8:
                phase = "🌸 Generatif"
                recommended_ratio = "1:8"
            else:
                phase = "🌾 Pemeliharaan"
                recommended_ratio = "1:15"
            
            schedule_data.append({
                "Aplikasi": f"#{i+1}",
                "Tanggal": app_date.strftime("%d %b %Y"),
                "HST": day_after_planting,
                "Fase": phase,
                "Rasio": recommended_ratio,
                "POC": f"{poc_volume_available:.1f}L"
            })
        
        df_schedule = pd.DataFrame(schedule_data)
        st.dataframe(df_schedule, use_container_width=True, hide_index=True, height=300)
        
        st.info(f"""
        **📊 Ringkasan:**
        - Total Aplikasi: {num_applications}x
        - POC Dibutuhkan: {total_poc_needed:.1f} L
        - Harvest: {(planting_date + timedelta(days=crop_cycle_days)).strftime('%d %b %Y')}
        """)
    
    # Cost Comparison Chart
    st.markdown("---")
    st.subheader("📊 Perbandingan Biaya vs Pupuk Komersial")
    
    col_cost1, col_cost2, col_cost3 = st.columns(3)
    
    with col_cost1:
        st.markdown("**💰 Harga Pupuk Komersial:**")
        commercial_npk_price = st.number_input("NPK Pabrikan (Rp/kg)", value=12000, min_value=0, step=1000)
        commercial_poc_price = st.number_input("POC Komersial (Rp/L)", value=50000, min_value=0, step=5000)
    
    with col_cost2:
        st.markdown("**🧪 POC Anda:**")
        poc_cost_per_liter = total_cost_with_water / target_volume
        st.metric("Biaya POC/Liter", f"Rp {poc_cost_per_liter:,.0f}")
        
        # Calculate NPK equivalent
        npk_equivalent_kg = (n_pct + p_pct + k_pct) / 45 * target_volume  # Rough estimate
        st.metric("Setara NPK", f"{npk_equivalent_kg:.1f} kg")
    
    with col_cost3:
        st.markdown("**💵 Penghematan:**")
        
        # Compare with commercial POC
        savings_vs_commercial_poc = (commercial_poc_price - poc_cost_per_liter) * target_volume
        savings_pct_poc = (savings_vs_commercial_poc / (commercial_poc_price * target_volume)) * 100 if commercial_poc_price > 0 else 0
        
        st.metric("vs POC Komersial", 
                 f"Rp {savings_vs_commercial_poc:,.0f}", 
                 delta=f"{savings_pct_poc:.0f}% lebih murah" if savings_vs_commercial_poc > 0 else f"{abs(savings_pct_poc):.0f}% lebih mahal")
        
        # Compare with NPK
        commercial_npk_cost = npk_equivalent_kg * commercial_npk_price
        savings_vs_npk = commercial_npk_cost - total_cost_with_water
        savings_pct_npk = (savings_vs_npk / commercial_npk_cost) * 100 if commercial_npk_cost > 0 else 0
        
        st.metric("vs NPK Pabrikan", 
                 f"Rp {savings_vs_npk:,.0f}", 
                 delta=f"{savings_pct_npk:.0f}% lebih murah" if savings_vs_npk > 0 else f"{abs(savings_pct_npk):.0f}% lebih mahal")
    
    # Visualize cost comparison
    comparison_chart_data = {
        "Jenis": ["POC Anda", "POC Komersial", "NPK Pabrikan"],
        "Biaya": [total_cost_with_water, commercial_poc_price * target_volume, commercial_npk_cost]
    }
    df_cost_comp = pd.DataFrame(comparison_chart_data)
    
    fig_cost = px.bar(df_cost_comp, x="Jenis", y="Biaya", 
                      title="Perbandingan Biaya Total",
                      color="Jenis",
                      color_discrete_map={"POC Anda": "#10b981", "POC Komersial": "#f59e0b", "NPK Pabrikan": "#ef4444"})
    fig_cost.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig_cost, use_container_width=True)
    
    # Batch Production Planner
    st.markdown("---")
    st.subheader("📅 Perencanaan Produksi Batch")
    
    col_batch1, col_batch2 = st.columns([1, 2])
    
    with col_batch1:
        st.markdown("**⚙️ Konfigurasi Produksi:**")
        batches_per_month = st.number_input("Batch per Bulan", value=4, min_value=1, max_value=12, step=1)
        fermentation_days = st.number_input("Lama Fermentasi (hari)", value=14, min_value=7, max_value=30, step=1)
        
        # Calculate staggered schedule
        days_between_batches = 30 / batches_per_month
    
    with col_batch2:
        st.markdown("**📅 Jadwal Produksi Bulanan:**")
        
        batch_schedule = []
        start_date = datetime.now()
        
        for batch_num in range(batches_per_month):
            batch_start = start_date + timedelta(days=batch_num * days_between_batches)
            batch_ready = batch_start + timedelta(days=fermentation_days)
            
            batch_schedule.append({
                "Batch": f"#{batch_num + 1}",
                "Mulai": batch_start.strftime("%d %b"),
                "Siap": batch_ready.strftime("%d %b"),
                "Volume": f"{target_volume}L",
                "Status": "🟢 Aktif" if batch_num == 0 else "⏳ Terjadwal"
            })
        
        df_batch = pd.DataFrame(batch_schedule)
        st.dataframe(df_batch, use_container_width=True, hide_index=True)
        
        # Monthly summary
        monthly_poc_production = target_volume * batches_per_month
        monthly_cost = total_cost_with_water * batches_per_month
        monthly_materials_needed = {mat: qty * batches_per_month for mat, qty in inputs.items()}
        
        st.success(f"""
        **📊 Ringkasan Bulanan:**
        - Total Produksi: {monthly_poc_production:.0f} L/bulan
        - Total Biaya: Rp {monthly_cost:,.0f}/bulan
        - Biaya per Liter: Rp {monthly_cost/monthly_poc_production:,.0f}
        """)
        
        # Show material needs
        with st.expander("📦 Kebutuhan Bahan Bulanan"):
            for material, total_qty in monthly_materials_needed.items():
                # Find unit
                unit = "unit"
                for cat_materials in MATERIALS.values():
                    if material in cat_materials:
                        unit = cat_materials[material]['unit']
                        break
                st.write(f"- {material}: {total_qty:.1f} {unit}")
    
    # Nutrient Trend Tracker
    st.markdown("---")
    st.subheader("📈 Pelacak Tren Nutrisi")
    
    # Initialize trend data in session state
    if 'nutrient_history' not in st.session_state:
        st.session_state['nutrient_history'] = []
    
    col_trend1, col_trend2 = st.columns([1, 2])
    
    with col_trend1:
        st.markdown("**💾 Simpan Data Batch:**")
        
        if st.button("📊 Simpan Batch Ini ke History", type="primary", use_container_width=True):
            batch_data = {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'batch_name': f"Batch {len(st.session_state['nutrient_history']) + 1}",
                'N': n_pct,
                'P': p_pct,
                'K': k_pct,
                'C': c_pct,
                'cost': total_cost_with_water,
                'volume': target_volume
            }
            st.session_state['nutrient_history'].append(batch_data)
            st.success(f"✅ Batch #{len(st.session_state['nutrient_history'])} tersimpan!")
            st.rerun()
        
        if st.session_state['nutrient_history']:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state['nutrient_history'] = []
                st.rerun()
            
            st.info(f"📊 Total Batch: {len(st.session_state['nutrient_history'])}")
    
    with col_trend2:
        if st.session_state['nutrient_history']:
            st.markdown("**📈 Tren NPK dari Waktu ke Waktu:**")
            
            # Create trend dataframe
            trend_df = pd.DataFrame(st.session_state['nutrient_history'])
            
            # Plot NPK trends
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(x=trend_df['batch_name'], y=trend_df['N'], 
                                          mode='lines+markers', name='N (%)', line=dict(color='#10b981')))
            fig_trend.add_trace(go.Scatter(x=trend_df['batch_name'], y=trend_df['P'], 
                                          mode='lines+markers', name='P (%)', line=dict(color='#f59e0b')))
            fig_trend.add_trace(go.Scatter(x=trend_df['batch_name'], y=trend_df['K'], 
                                          mode='lines+markers', name='K (%)', line=dict(color='#3b82f6')))
            
            fig_trend.update_layout(
                title="Tren Kandungan NPK",
                xaxis_title="Batch",
                yaxis_title="Konsentrasi (%)",
                height=300,
                hovermode='x unified'
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Analysis
            if len(trend_df) >= 2:
                latest_n = trend_df.iloc[-1]['N']
                prev_n = trend_df.iloc[-2]['N']
                n_change = ((latest_n - prev_n) / prev_n * 100) if prev_n > 0 else 0
                
                st.markdown("**📊 Analisis Perubahan:**")
                if abs(n_change) < 5:
                    st.success(f"✅ Formula konsisten (N: {n_change:+.1f}%)")
                elif n_change > 0:
                    st.info(f"📈 N meningkat {n_change:.1f}% dari batch sebelumnya")
                else:
                    st.warning(f"📉 N menurun {abs(n_change):.1f}% dari batch sebelumnya")
        else:
            st.info("💡 Simpan batch pertama untuk mulai tracking tren nutrisi")

else:
    st.info("""
    👈 **Cara Mendapatkan Analisis POC:**
    
    **Opsi 1: Gunakan AI Optimizer (Recommended)**
    1. Buka tab **"💼 Business Model"**
    2. Input skala produksi, target, dan produk
    3. Klik **"🚀 GENERATE REKOMENDASI LENGKAP"**
    4. Formula otomatis ter-load di sini dengan analisis lengkap!
    
    **Opsi 2: Manual**
    - Pilih template resep di sidebar, atau
    - Input bahan manual di sidebar
    """)

# Business Model Tab
with tab2:
    st.markdown("### 💼 Model Bisnis Produksi POC Komersial")
    st.info("🏭 **Kapasitas Pabrikan:** Drum 1000 Liter | 3 Varian Produk | Analisis Kelayakan Bisnis Lengkap")
    
    # AI Optimizer for Production Setup
    st.markdown("---")
    st.subheader("🤖 AI Optimizer - Rekomendasi Setup Produksi")
    
    col_ai1, col_ai2 = st.columns([1, 2])
    
    with col_ai1:
        st.markdown("**⚙️ Pilih Skala Produksi:**")
        production_scale = st.radio(
            "Tipe Produksi",
            ["🏠 Pemakaian Pribadi", "🏭 Industri/Komersial"],
            help="AI akan memberikan rekomendasi berbeda untuk setiap skala"
        )
        
        # Save to session state for cross-tab sync
        st.session_state['biz_production_scale'] = production_scale
        
        if production_scale == "🏠 Pemakaian Pribadi":
            target_monthly = st.slider("Target Produksi (L/bulan)", 50, 500, 200, 50, key="ai_target_personal")
        else:
            target_monthly = st.slider("Target Produksi (L/bulan)", 500, 10000, 2000, 500, key="ai_target_industrial")
        
        preferred_product = st.selectbox(
            "Produk Utama",
            ["Vegetatif (High N)", "Generatif (High K)", "Balanced", "Mix (Semua)"],
            key="ai_product"
        )
        
        # Save to session state for cross-tab sync
        st.session_state['biz_preferred_product'] = preferred_product
        
        # Additional inputs for comprehensive optimization
        st.markdown("**💰 Target Bisnis:**")
        target_price_1l = st.number_input("Target Harga Jual 1L (Rp)", value=30000, min_value=1000, step=1000, key="ai_target_price")
        target_margin = st.slider("Target Margin (%)", 30, 200, 100, 10, key="ai_target_margin")
    
    with col_ai2:
        st.markdown("**💡 Preview Rekomendasi:**")
        
        # Show preview based on selections
        if production_scale == "🏠 Pemakaian Pribadi":
            if target_monthly <= 100:
                st.info(f"""
                **Skala: Pribadi Kecil**
                - Produksi: {target_monthly}L/bulan
                - Produk: {preferred_product}
                - Investasi: ~Rp 3 juta
                - Cocok untuk: Lahan sendiri
                """)
            elif target_monthly <= 300:
                st.info(f"""
                **Skala: Pribadi Menengah**
                - Produksi: {target_monthly}L/bulan
                - Produk: {preferred_product}
                - Investasi: ~Rp 6 juta
                - Cocok untuk: 1-2 hektar
                """)
            else:
                st.info(f"""
                **Skala: Semi-Komersial**
                - Produksi: {target_monthly}L/bulan
                - Produk: {preferred_product}
                - Investasi: ~Rp 9 juta
                - Cocok untuk: >2 hektar + jual surplus
                """)
        else:
            if target_monthly <= 2000:
                st.info(f"""
                **Skala: Industri Startup**
                - Produksi: {target_monthly:,}L/bulan
                - Produk: {preferred_product}
                - Investasi: ~Rp 17 juta
                - Target: Toko tani lokal
                """)
            elif target_monthly <= 5000:
                st.info(f"""
                **Skala: Industri Menengah**
                - Produksi: {target_monthly:,}L/bulan
                - Produk: {preferred_product}
                - Investasi: ~Rp 33 juta
                - Target: Distributor regional
                """)
            else:
                st.info(f"""
                **Skala: Industri Besar**
                - Produksi: {target_monthly:,}L/bulan
                - Produk: {preferred_product}
                - Investasi: ~Rp 75 juta+
                - Target: Nasional
                """)
        
        st.markdown("---")
        st.markdown("**🎯 Klik tombol di bawah untuk generate:**")
        st.caption("✅ Setup Produksi Optimal")
        st.caption("✅ Formula POC Ter-scale")
        st.caption("✅ Analisis Biaya Lengkap")
        st.caption("✅ Proyeksi Profit & ROI")
        
        if st.button("🚀 GENERATE REKOMENDASI LENGKAP", type="primary", use_container_width=True, key="ai_generate_all"):
            # Calculate optimal setup
            if production_scale == "🏠 Pemakaian Pribadi":
                if target_monthly <= 100:
                    drums_rec, cycles_rec = 1, 1
                elif target_monthly <= 300:
                    drums_rec, cycles_rec = 2, 2
                else:
                    drums_rec, cycles_rec = 3, 2
            else:
                if target_monthly <= 2000:
                    drums_rec, cycles_rec = 4, 2
                elif target_monthly <= 5000:
                    drums_rec, cycles_rec = 8, 2
                else:
                    drums_rec, cycles_rec = 12, 3
            
            util_rec = (target_monthly / (drums_rec * 1000 * cycles_rec)) * 100
            
            # Save production setup
            st.session_state['ai_drums'] = drums_rec
            st.session_state['ai_cycles'] = cycles_rec
            st.session_state['ai_util'] = min(util_rec, 100)
            
            # Generate formula based on product
            if preferred_product == "Vegetatif (High N)":
                st.session_state['ai_formula'] = {
                    'Urine Kelinci': 15,
                    'Daun Kelor': 5,
                    'Molase': 2,
                    'Dekomposer (EM4/MOL)': 0.5,
                    'Urea': 0.5 if production_scale == "🏭 Industri/Komersial" else 0
                }
                st.session_state['ai_formula_name'] = "POC Vegetatif (High N)"
            elif preferred_product == "Generatif (High K)":
                st.session_state['ai_formula'] = {
                    'Bonggol Pisang': 10,
                    'Kulit Pisang': 5,
                    'KCl': 0.3,
                    'Molase': 2,
                    'Dekomposer (EM4/MOL)': 0.5
                }
                st.session_state['ai_formula_name'] = "POC Generatif (High K)"
            elif preferred_product == "Balanced":
                st.session_state['ai_formula'] = {
                    'Urine Sapi': 10,
                    'Sabut Kelapa': 3,
                    'NPK Phonska (15-15-15)': 0.5,
                    'Molase': 2,
                    'Dekomposer (EM4/MOL)': 0.5
                }
                st.session_state['ai_formula_name'] = "POC Balanced"
            else:
                st.session_state['ai_formula'] = {
                    'Urine Kambing': 8,
                    'Bonggol Pisang': 5,
                    'Daun Kelor': 3,
                    'Molase': 2,
                    'Dekomposer (EM4/MOL)': 0.5
                }
                st.session_state['ai_formula_name'] = "POC Mix (All Purpose)"
            
            st.success(f"""
            ✅ **REKOMENDASI LENGKAP BERHASIL DI-GENERATE!**
            
            **📦 Setup Produksi:**
            - {drums_rec} drum × 1000L
            - {cycles_rec} siklus/bulan
            - {min(util_rec, 100):.0f}% utilisasi
            - Kapasitas: {target_monthly:,}L/bulan
            
            **🧪 Formula POC:**
            - {st.session_state['ai_formula_name']}
            - Ter-scale untuk {drums_rec * 1000}L per batch
            
            **💰 Target Bisnis:**
            - Harga jual: Rp {target_price_1l:,}/L
            - Margin: {target_margin}%
            
            **📊 Lihat hasil lengkap di bawah:**
            - Scroll ke "Setup Produksi" untuk detail equipment
            - Scroll ke "Proyeksi Pendapatan" untuk profit
            - Buka tab "🧪 Kalkulator POC" untuk analisis NPK
            """)
            st.rerun()
            # Personal use recommendations
            if target_monthly <= 100:
                drums_rec = 1
                cycles_rec = 1
                util_rec = target_monthly / 1000 * 100
                st.success(f"""
                **Setup untuk Pemakaian Pribadi (Skala Kecil)**
                
                📦 **Rekomendasi Equipment:**
                - Drum: {drums_rec} unit (1000L)
                - Siklus: {cycles_rec}x per bulan
                - Utilisasi: {util_rec:.0f}%
                - Produksi: {target_monthly} L/bulan
                
                💰 **Estimasi Investasi:**
                - Drum 1000L: Rp 2,500,000
                - Mixer sederhana: Rp 500,000
                - Total: ~Rp 3,000,000
                
                🎯 **Fokus Produk:**
                - {preferred_product}
                - Untuk kebutuhan lahan sendiri
                - Surplus bisa dijual ke tetangga
                
                ✅ **Keuntungan:**
                - Hemat biaya pupuk (vs beli POC komersial)
                - Kontrol kualitas sendiri
                - Ramah lingkungan
                """)
            elif target_monthly <= 300:
                drums_rec = 2
                cycles_rec = 2
                util_rec = target_monthly / (2 * 1000 * 2) * 100
                st.success(f"""
                **Setup untuk Pemakaian Pribadi (Skala Menengah)**
                
                📦 **Rekomendasi Equipment:**
                - Drum: {drums_rec} unit (1000L)
                - Siklus: {cycles_rec}x per bulan
                - Utilisasi: {util_rec:.0f}%
                - Produksi: {target_monthly} L/bulan
                
                💰 **Estimasi Investasi:**
                - Drum 1000L: Rp 5,000,000 (2 unit)
                - Mixer: Rp 1,000,000
                - Total: ~Rp 6,000,000
                
                🎯 **Fokus Produk:**
                - {preferred_product}
                - Untuk lahan 1-2 hektar
                - Bisa jual surplus ke kelompok tani
                
                ✅ **Keuntungan:**
                - ROI < 6 bulan (vs beli POC)
                - Bisa mulai bisnis kecil-kecilan
                - Stok selalu tersedia
                """)
            else:
                drums_rec = 3
                cycles_rec = 2
                util_rec = target_monthly / (3 * 1000 * 2) * 100
                st.info(f"""
                **Setup Semi-Komersial**
                
                📦 **Rekomendasi Equipment:**
                - Drum: {drums_rec} unit (1000L)
                - Siklus: {cycles_rec}x per bulan
                - Utilisasi: {util_rec:.0f}%
                - Produksi: {target_monthly} L/bulan
                
                💰 **Estimasi Investasi:**
                - Drum 1000L: Rp 7,500,000 (3 unit)
                - Mixer profesional: Rp 1,500,000
                - Total: ~Rp 9,000,000
                
                🎯 **Fokus Produk:**
                - {preferred_product}
                - Untuk lahan >2 hektar
                - **Mulai pertimbangkan bisnis POC**
                
                💡 **Saran:**
                - Pertimbangkan izin PIRT
                - Mulai branding & packaging
                - Target: Kelompok tani lokal
                """)
        
        else:
            # Industrial recommendations
            if target_monthly <= 2000:
                drums_rec = 4
                cycles_rec = 2
                util_rec = target_monthly / (4 * 1000 * 2) * 100
                st.success(f"""
                **Setup Industri Kecil (Startup)**
                
                📦 **Rekomendasi Equipment:**
                - Drum: {drums_rec} unit (1000L)
                - Siklus: {cycles_rec}x per bulan
                - Utilisasi: {util_rec:.0f}%
                - Produksi: {target_monthly:,} L/bulan
                
                💰 **Estimasi Investasi:**
                - Drum 1000L: Rp 10,000,000 (4 unit)
                - Mixer industrial: Rp 2,000,000
                - Packaging equipment: Rp 3,000,000
                - Izin & sertifikasi: Rp 2,000,000
                - Total: ~Rp 17,000,000
                
                🎯 **Strategi Produk:**
                - Mix produk: 30% Veg, 40% Gen, 30% Bal
                - Packaging: 60% kemasan 5L, 40% kemasan 1L
                - Target: Toko tani & distributor lokal
                
                👥 **SDM:**
                - 1 operator produksi
                - 1 admin/marketing
                
                📈 **Target Pasar:**
                - Radius 50 km
                - 20-30 pelanggan tetap
                - Omzet: Rp 50-100 juta/bulan
                """)
            elif target_monthly <= 5000:
                drums_rec = 8
                cycles_rec = 2
                util_rec = target_monthly / (8 * 1000 * 2) * 100
                st.success(f"""
                **Setup Industri Menengah**
                
                📦 **Rekomendasi Equipment:**
                - Drum: {drums_rec} unit (1000L)
                - Siklus: {cycles_rec}x per bulan
                - Utilisasi: {util_rec:.0f}%
                - Produksi: {target_monthly:,} L/bulan
                
                💰 **Estimasi Investasi:**
                - Drum 1000L: Rp 20,000,000 (8 unit)
                - Mixer industrial: Rp 3,000,000
                - Packaging line: Rp 5,000,000
                - QC equipment: Rp 2,000,000
                - Izin lengkap: Rp 3,000,000
                - Total: ~Rp 33,000,000
                
                🎯 **Strategi Produk:**
                - 3 varian lengkap + custom formula
                - Packaging: 50% bulk (20L), 30% jerigen (5L), 20% botol (1L)
                - Target: Distributor regional & koperasi
                
                👥 **SDM:**
                - 2 operator produksi
                - 1 QC specialist
                - 1 admin
                - 1 sales/marketing
                
                📈 **Target Pasar:**
                - Radius 100 km
                - 50-100 pelanggan
                - Omzet: Rp 150-300 juta/bulan
                """)
            else:
                drums_rec = 12
                cycles_rec = 3
                util_rec = target_monthly / (12 * 1000 * 3) * 100
                st.warning(f"""
                **Setup Industri Besar (Enterprise)**
                
                📦 **Rekomendasi Equipment:**
                - Drum: {drums_rec}+ unit (1000L)
                - Siklus: {cycles_rec}x per bulan
                - Utilisasi: {util_rec:.0f}%
                - Produksi: {target_monthly:,} L/bulan
                
                💰 **Estimasi Investasi:**
                - Drum 1000L: Rp 30,000,000+ (12+ unit)
                - Automated mixing system: Rp 10,000,000
                - Packaging automation: Rp 15,000,000
                - Lab QC lengkap: Rp 5,000,000
                - Izin & sertifikasi: Rp 5,000,000
                - Warehouse & logistics: Rp 10,000,000
                - Total: ~Rp 75,000,000+
                
                🎯 **Strategi Produk:**
                - Full product line (5+ varian)
                - Custom formulation service
                - White label untuk brand lain
                - Packaging: Semua ukuran (1L, 5L, 20L, 200L)
                
                👥 **SDM:**
                - 4-6 operator produksi (shift)
                - 2 QC specialist
                - 2 admin
                - 3-5 sales team
                - 1 supervisor/manager
                
                📈 **Target Pasar:**
                - Nasional (multi-provinsi)
                - 200+ pelanggan
                - Omzet: Rp 500 juta - 1 miliar/bulan
                
                ⚠️ **Catatan:**
                - Pertimbangkan PT/CV
                - Perlu business plan detail
                - Funding/investor mungkin diperlukan
                """)
        
        if st.button("✅ Terapkan Rekomendasi AI", type="primary", use_container_width=True):
            st.session_state['ai_drums'] = drums_rec
            st.session_state['ai_cycles'] = cycles_rec
            st.session_state['ai_util'] = min(util_rec, 100)
            
            # Also recommend POC formula based on preferred product
            if preferred_product == "Vegetatif (High N)":
                # High N formula
                st.session_state['ai_formula'] = {
                    'Urine Kelinci': 15,
                    'Daun Kelor': 5,
                    'Molase': 2,
                    'Dekomposer (EM4/MOL)': 0.5,
                    'Urea': 0.5 if production_scale == "🏭 Industri/Komersial" else 0
                }
                st.session_state['ai_formula_name'] = "POC Vegetatif (High N)"
            elif preferred_product == "Generatif (High K)":
                # High K formula
                st.session_state['ai_formula'] = {
                    'Bonggol Pisang': 10,
                    'Kulit Pisang': 5,
                    'KCl': 0.3,
                    'Molase': 2,
                    'Dekomposer (EM4/MOL)': 0.5
                }
                st.session_state['ai_formula_name'] = "POC Generatif (High K)"
            elif preferred_product == "Balanced":
                # Balanced formula
                st.session_state['ai_formula'] = {
                    'Urine Sapi': 10,
                    'Sabut Kelapa': 3,
                    'NPK Phonska (15-15-15)': 0.5,
                    'Molase': 2,
                    'Dekomposer (EM4/MOL)': 0.5
                }
                st.session_state['ai_formula_name'] = "POC Balanced"
            else:  # Mix
                # Mixed formula
                st.session_state['ai_formula'] = {
                    'Urine Kambing': 8,
                    'Bonggol Pisang': 5,
                    'Daun Kelor': 3,
                    'Molase': 2,
                    'Dekomposer (EM4/MOL)': 0.5
                }
                st.session_state['ai_formula_name'] = "POC Mix (All Purpose)"
            
            # Calculate NPK preview from generated formula
            volume_per_drum = drums_rec * 1000
            npk_preview = calculate_npk_from_formula(st.session_state['ai_formula'], volume_per_drum)
            
            st.success(f"""
            ✅ **REKOMENDASI LENGKAP BERHASIL DI-GENERATE!**
            
            **📦 Setup Produksi:**
            - {drums_rec} drum × 1000L = {volume_per_drum:,}L per batch
            - {cycles_rec} siklus/bulan
            - {min(util_rec, 100):.0f}% utilisasi
            - Kapasitas: {target_monthly:,}L/bulan
            
            **🧪 Formula POC:**
            - {st.session_state['ai_formula_name']}
            - Ter-scale untuk {volume_per_drum:,}L per batch
            """)
            
            # Show NPK Preview
            st.markdown("---")
            st.subheader("📊 Preview Analisis POC")
            
            col_npk1, col_npk2, col_npk3, col_npk4 = st.columns(4)
            with col_npk1:
                st.metric("Nitrogen (N)", f"{npk_preview['N']:.2f}%")
            with col_npk2:
                st.metric("Fosfor (P)", f"{npk_preview['P']:.2f}%")
            with col_npk3:
                st.metric("Kalium (K)", f"{npk_preview['K']:.2f}%")
            with col_npk4:
                st.metric("C-Organik", f"{npk_preview['C']:.2f}%")
            
            st.info(f"""
            💰 **Estimasi Biaya per Batch ({volume_per_drum:,}L):**
            - Bahan Baku: Rp {npk_preview['total_cost']:,.0f}
            - Biaya per Liter: Rp {(npk_preview['total_cost']/volume_per_drum):,.0f}/L
            
            📊 **Lihat analisis lengkap** (charts, recommendations, dll) di tab **"🧪 Kalkulator POC"**
            """)
            
            st.rerun()
    
    # Production Setup
    st.markdown("---")
    st.subheader("🏭 Setup Produksi")
    
    col_prod1, col_prod2, col_prod3 = st.columns(3)
    
    with col_prod1:
        default_drums = st.session_state.get('ai_drums', 4)
        num_drums = st.number_input("Jumlah Drum (1000L)", value=default_drums, min_value=1, max_value=20, step=1, key="biz_num_drums")
        fermentation_days = st.number_input("Lama Fermentasi (hari)", value=14, min_value=7, max_value=30, step=1, key="biz_fermentation_days")
    
    with col_prod2:
        default_cycles = st.session_state.get('ai_cycles', 2)
        default_util = st.session_state.get('ai_util', 70)
        cycles_per_month = st.number_input("Siklus per Bulan", value=default_cycles, min_value=1, max_value=4, step=1, key="biz_cycles")
        capacity_utilization = st.slider("Utilisasi Kapasitas (%)", 30, 100, int(default_util), 5, key="biz_capacity")
    
    with col_prod3:
        monthly_capacity = num_drums * 1000 * cycles_per_month * (capacity_utilization / 100)
        annual_capacity = monthly_capacity * 12
        st.metric("Kapasitas Bulanan", f"{monthly_capacity:,.0f} L")
        st.metric("Kapasitas Tahunan", f"{annual_capacity:,.0f} L")
    
    # Product Variants
    st.markdown("---")
    st.subheader("📦 Varian Produk & Sales Mix")
    
    st.info("💡 **NPK dan biaya produksi dihitung otomatis dari formula bahan**")
    
    # Calculate NPK and cost from formula templates
    veg_formula = {'Urine Kelinci': 15, 'Daun Kelor': 5, 'Molase': 2, 'Dekomposer (EM4/MOL)': 0.5}
    gen_formula = {'Bonggol Pisang': 10, 'Kulit Pisang': 5, 'KCl': 0.3, 'Molase': 2, 'Dekomposer (EM4/MOL)': 0.5}
    bal_formula = {'Urine Sapi': 10, 'Sabut Kelapa': 3, 'NPK Phonska (15-15-15)': 0.5, 'Molase': 2, 'Dekomposer (EM4/MOL)': 0.5}
    
    veg_data = calculate_npk_from_formula(veg_formula, 100)
    gen_data = calculate_npk_from_formula(gen_formula, 100)
    bal_data = calculate_npk_from_formula(bal_formula, 100)
    
    col_var1, col_var2, col_var3 = st.columns(3)
    
    with col_var1:
        st.markdown("**🌱 POC Vegetatif (High N)**")
        st.caption(f"NPK: N={veg_data['N']:.2f}%, P={veg_data['P']:.2f}%, K={veg_data['K']:.2f}%")
        st.caption(f"Biaya: Rp {veg_data['total_cost']:,.0f}/100L")
        veg_mix = st.slider("Sales Mix Vegetatif (%)", 0, 100, 30, 5, key="veg_mix")
        veg_cost_per_liter = veg_data['total_cost'] / 100  # Auto-calculated
    
    with col_var2:
        st.markdown("**🌸 POC Generatif (High K)**")
        st.caption(f"NPK: N={gen_data['N']:.2f}%, P={gen_data['P']:.2f}%, K={gen_data['K']:.2f}%")
        st.caption(f"Biaya: Rp {gen_data['total_cost']:,.0f}/100L")
        gen_mix = st.slider("Sales Mix Generatif (%)", 0, 100, 40, 5, key="gen_mix")
        gen_cost_per_liter = gen_data['total_cost'] / 100  # Auto-calculated
    
    with col_var3:
        st.markdown("**⚖️ POC Balanced**")
        st.caption(f"NPK: N={bal_data['N']:.2f}%, P={bal_data['P']:.2f}%, K={bal_data['K']:.2f}%")
        st.caption(f"Biaya: Rp {bal_data['total_cost']:,.0f}/100L")
        bal_mix = 100 - veg_mix - gen_mix
        st.metric("Sales Mix Balanced", f"{bal_mix}%")
        bal_cost_per_liter = bal_data['total_cost'] / 100  # Auto-calculated
    
    # Weighted average cost
    avg_cost_per_liter = (veg_cost_per_liter * veg_mix + gen_cost_per_liter * gen_mix + bal_cost_per_liter * bal_mix) / 100
    
    # POC Analysis & Material Breakdown - FROM AI GENERATED FORMULA
    st.markdown("---")
    st.subheader("🧪 Analisis POC dari Formula AI")
    
    # Check if AI formula exists
    if st.session_state.get('ai_formula'):
        ai_formula = st.session_state.get('ai_formula')
        ai_formula_name = st.session_state.get('ai_formula_name', 'AI Formula')
        ai_drums = st.session_state.get('ai_drums', 4)
        volume_per_batch = ai_drums * 1000
        
        st.success(f"📋 **Formula Aktif:** {ai_formula_name} | **Volume:** {volume_per_batch:,}L per batch")
        
        # Calculate NPK from AI formula at actual volume
        ai_npk = calculate_npk_from_formula(ai_formula, volume_per_batch)
        
        # Display NPK metrics
        col_ai1, col_ai2, col_ai3, col_ai4 = st.columns(4)
        with col_ai1:
            st.metric("Nitrogen (N)", f"{ai_npk['N']:.2f}%")
        with col_ai2:
            st.metric("Fosfor (P)", f"{ai_npk['P']:.2f}%")
        with col_ai3:
            st.metric("Kalium (K)", f"{ai_npk['K']:.2f}%")
        with col_ai4:
            st.metric("C-Organik", f"{ai_npk['C']:.2f}%")
        
        # Build material breakdown table
        st.markdown(f"**📋 Rincian Bahan (per {volume_per_batch:,}L):**")
        ai_material_list = []
        for material, qty_base in ai_formula.items():
            # Scale quantity to actual volume
            qty_scaled = qty_base * (volume_per_batch / 100)
            
            # Find material in database
            for cat_name, cat_materials in MATERIALS.items():
                if material in cat_materials:
                    props = cat_materials[material]
                    n_contrib = (qty_scaled * props['N']) / 100
                    p_contrib = (qty_scaled * props['P']) / 100
                    k_contrib = (qty_scaled * props['K']) / 100
                    unit = props['unit']
                    price = props['price']
                    cost = qty_scaled * price
                    
                    ai_material_list.append({
                        "Bahan": material,
                        "Jumlah": f"{qty_scaled:.1f} {unit}",
                        "Kontribusi N": f"{n_contrib:.3f} kg",
                        "Kontribusi P": f"{p_contrib:.3f} kg",
                        "Kontribusi K": f"{k_contrib:.3f} kg",
                        "Biaya": f"Rp {cost:,.0f}"
                    })
                    break
        
        ai_materials_df = pd.DataFrame(ai_material_list)
        st.dataframe(ai_materials_df, use_container_width=True, hide_index=True)
        
        # Cost summary
        col_cost1, col_cost2, col_cost3 = st.columns(3)
        with col_cost1:
            st.metric("Total Biaya Bahan", f"Rp {ai_npk['total_cost']:,.0f}")
        with col_cost2:
            st.metric("Biaya per Liter", f"Rp {(ai_npk['total_cost']/volume_per_batch):,.0f}/L")
        with col_cost3:
            st.metric("Biaya per 100L", f"Rp {(ai_npk['total_cost']/volume_per_batch*100):,.0f}")
        
        st.info(f"""
        **🎯 Rekomendasi Penggunaan:**
        - Formula ini di-generate khusus untuk **{ai_formula_name}**
        - Cocok untuk skala produksi **{volume_per_batch:,}L per batch**
        - Total investasi bahan baku: **Rp {ai_npk['total_cost']:,.0f}** per batch
        
        **📊 Lihat analisis teknis lengkap** di tab **"🧪 Kalkulator POC"**
        """)
        
    else:
        st.warning("""
        ⚠️ **Belum ada formula AI yang di-generate**
        
        Untuk melihat analisis POC:
        1. Scroll ke atas ke section **"🤖 AI Optimizer"**
        2. Input preferensi (skala, target, produk)
        3. Klik **"🚀 GENERATE REKOMENDASI LENGKAP"**
        4. Analisis akan muncul di sini secara otomatis
        """)
        
        # Show template analysis as reference
        st.markdown("---")
        st.caption("📚 **Referensi: Analisis Template Formula** (untuk perbandingan)")
        
        ref_tab1, ref_tab2, ref_tab3 = st.tabs(["🌱 Vegetatif", "🌸 Generatif", "⚖️ Balanced"])
        
        with ref_tab1:
            st.caption(f"NPK: N={veg_data['N']:.2f}%, P={veg_data['P']:.2f}%, K={veg_data['K']:.2f}%")
            st.caption(f"Biaya: Rp {veg_data['total_cost']:,.0f}/100L")
        
        with ref_tab2:
            st.caption(f"NPK: N={gen_data['N']:.2f}%, P={gen_data['P']:.2f}%, K={gen_data['K']:.2f}%")
            st.caption(f"Biaya: Rp {gen_data['total_cost']:,.0f}/100L")
        
        with ref_tab3:
            st.caption(f"NPK: N={bal_data['N']:.2f}%, P={bal_data['P']:.2f}%, K={bal_data['K']:.2f}%")
            st.caption(f"Biaya: Rp {bal_data['total_cost']:,.0f}/100L")
    
    
    
    # Cost Structure
    st.markdown("---")
    st.subheader("💰 Struktur Biaya")
    
    col_cost1, col_cost2 = st.columns(2)
    
    with col_cost1:
        st.markdown("**🔧 Biaya Tetap (Fixed Costs)**")
        
        # Equipment
        drum_price = st.number_input("Harga Drum 1000L", value=2500000, step=100000, key="biz_drum_price")
        mixer_price = st.number_input("Mixer/Aerator", value=1500000, step=100000, key="biz_mixer_price")
        equipment_other = st.number_input("Peralatan Lain", value=2000000, step=100000, key="biz_equipment_other")
        
        total_equipment = (drum_price * num_drums) + mixer_price + equipment_other
        
        # Facility
        monthly_rent = st.number_input("Sewa Tempat/Bulan", value=2000000, step=100000, key="biz_rent")
        
        # Licensing
        licensing = st.number_input("Izin & Sertifikasi", value=2000000, step=100000, key="biz_licensing")
        
        total_fixed_initial = total_equipment + licensing
        monthly_fixed = monthly_rent + (total_equipment / 60)  # Depreciation 5 years
        
        st.success(f"""
        **Total Investasi Awal:** Rp {total_fixed_initial:,.0f}
        **Biaya Tetap Bulanan:** Rp {monthly_fixed:,.0f}
        """)
    
    with col_cost2:
        st.markdown("**⚙️ Biaya Operasional Bulanan**")
        
        # Raw materials (already calculated per liter)
        raw_material_cost = avg_cost_per_liter * monthly_capacity
        
        # Packaging
        packaging_1l = st.number_input("Kemasan 1L (Rp/unit)", value=2000, step=100, key="biz_pack_1l")
        packaging_5l = st.number_input("Kemasan 5L (Rp/unit)", value=8000, step=500, key="biz_pack_5l")
        
        # Labor
        labor_cost = st.number_input("Gaji Karyawan Total", value=7500000, step=500000, key="biz_labor")
        
        # Utilities
        utilities = st.number_input("Listrik + Air + Gas", value=1000000, step=100000, key="biz_utilities")
        
        # Marketing
        marketing_pct = st.slider("Marketing Budget (% Revenue)", 5, 20, 10, 1, key="biz_marketing_pct")
        
        total_operational_base = raw_material_cost + labor_cost + utilities
        
        st.success(f"""
        **Bahan Baku:** Rp {raw_material_cost:,.0f}
        **Total Operasional:** Rp {total_operational_base:,.0f}/bulan
        """)
    
    # Pricing Strategy
    st.markdown("---")
    st.subheader("💵 Strategi Harga & Packaging")
    
    col_price1, col_price2, col_price3 = st.columns(3)
    
    with col_price1:
        st.markdown("**📊 Harga Jual (Manual)**")
        
        # Manual price input
        price_1l = st.number_input("Harga Jual 1L (Rp)", value=30000, min_value=1000, step=1000, key="biz_price_1l",
                                    help="Tentukan harga jual per botol 1L")
        price_5l = st.number_input("Harga Jual 5L (Rp)", value=135000, min_value=5000, step=5000, key="biz_price_5l",
                                    help="Tentukan harga jual per jerigen 5L")
        
        # Calculate actual margin
        price_5l_per_liter = price_5l / 5
        actual_margin_1l = ((price_1l - avg_cost_per_liter) / avg_cost_per_liter * 100) if avg_cost_per_liter > 0 else 0
        actual_margin_5l = ((price_5l_per_liter - avg_cost_per_liter) / avg_cost_per_liter * 100) if avg_cost_per_liter > 0 else 0
        
        st.caption(f"Margin 1L: {actual_margin_1l:.0f}%")
        st.caption(f"Margin 5L: {actual_margin_5l:.0f}% (Rp {price_5l_per_liter:,.0f}/L)")
    
    with col_price2:
        st.markdown("**📦 Packaging Mix**")
        packaging_1l_pct = st.slider("Kemasan 1L (%)", 0, 100, 40, 5, key="biz_pack_1l_pct")
        packaging_5l_pct = 100 - packaging_1l_pct
        
        st.info(f"""
        - 1L: {packaging_1l_pct}%
        - 5L: {packaging_5l_pct}%
        """)
    
    with col_price3:
        st.markdown("**💼 Benchmark Pasar**")
        commercial_poc_price = st.number_input("POC Komersial (Rp/L)", value=50000, step=5000, key="biz_commercial_price")
        
        price_vs_market = ((price_1l - commercial_poc_price) / commercial_poc_price) * 100
        
        if price_vs_market < -20:
            st.success(f"✅ {abs(price_vs_market):.0f}% lebih murah dari pasar")
        elif price_vs_market < 0:
            st.info(f"👍 {abs(price_vs_market):.0f}% lebih murah dari pasar")
        else:
            st.warning(f"⚠️ {price_vs_market:.0f}% lebih mahal dari pasar")
    
    # Revenue Projections
    st.markdown("---")
    st.subheader("📈 Proyeksi Pendapatan & Profit")
    
    # Calculate revenue
    volume_1l = monthly_capacity * (packaging_1l_pct / 100)
    volume_5l_units = (monthly_capacity * (packaging_5l_pct / 100)) / 5
    
    revenue_1l = volume_1l * price_1l
    revenue_5l = volume_5l_units * price_5l
    total_revenue = revenue_1l + revenue_5l
    
    # Packaging costs
    packaging_cost = (volume_1l * packaging_1l) + (volume_5l_units * packaging_5l)
    
    # Marketing cost
    marketing_cost = total_revenue * (marketing_pct / 100)
    
    # Total costs
    total_monthly_cost = monthly_fixed + total_operational_base + packaging_cost + marketing_cost
    
    # Profit
    monthly_profit = total_revenue - total_monthly_cost
    annual_profit = monthly_profit * 12
    
    # Metrics
    col_rev1, col_rev2, col_rev3, col_rev4 = st.columns(4)
    
    with col_rev1:
        st.metric("Revenue Bulanan", f"Rp {total_revenue:,.0f}")
        st.caption(f"1L: Rp {revenue_1l:,.0f}")
        st.caption(f"5L: Rp {revenue_5l:,.0f}")
    
    with col_rev2:
        st.metric("Total Biaya", f"Rp {total_monthly_cost:,.0f}")
        st.caption(f"Fixed: Rp {monthly_fixed:,.0f}")
        st.caption(f"Variable: Rp {(total_monthly_cost - monthly_fixed):,.0f}")
    
    with col_rev3:
        st.metric("Profit Bulanan", f"Rp {monthly_profit:,.0f}", 
                 delta=f"{(monthly_profit/total_revenue*100):.1f}% margin")
        st.caption(f"Tahunan: Rp {annual_profit:,.0f}")
    
    with col_rev4:
        roi_annual = (annual_profit / total_fixed_initial) * 100
        payback_months = total_fixed_initial / monthly_profit if monthly_profit > 0 else 999
        st.metric("ROI Tahunan", f"{roi_annual:.0f}%")
        st.caption(f"Payback: {payback_months:.1f} bulan")
    
    # Break-Even Analysis
    st.markdown("---")
    st.subheader("⚖️ Analisis Break-Even")
    
    col_be1, col_be2 = st.columns(2)
    
    with col_be1:
        # Calculate break-even
        contribution_margin_per_liter = ((price_1l * packaging_1l_pct + price_5l_per_liter * packaging_5l_pct) / 100) - avg_cost_per_liter
        
        if contribution_margin_per_liter > 0:
            breakeven_liters = monthly_fixed / contribution_margin_per_liter
            breakeven_pct = (breakeven_liters / monthly_capacity) * 100 if monthly_capacity > 0 else 0
            
            st.success(f"""
            **Break-Even Point:**
            - Volume: {breakeven_liters:,.0f} Liter/bulan
            - Utilisasi: {breakeven_pct:.1f}% kapasitas
            - Revenue: Rp {(breakeven_liters * ((price_1l * packaging_1l_pct + price_5l_per_liter * packaging_5l_pct) / 100)):,.0f}
            """)
        else:
            st.error("⚠️ Margin negatif - harga jual terlalu rendah!")
    
    with col_be2:
        # Profitability chart
        scenarios = ["Worst (30%)", "Base (70%)", "Best (90%)"]
        scenario_utils = [30, 70, 90]
        scenario_profits = []
        
        for util in scenario_utils:
            scenario_capacity = num_drums * 1000 * cycles_per_month * (util / 100)
            scenario_revenue = scenario_capacity * ((price_1l * packaging_1l_pct + price_5l_per_liter * packaging_5l_pct) / 100)
            scenario_var_cost = scenario_capacity * avg_cost_per_liter + (scenario_revenue * marketing_pct / 100)
            scenario_profit = scenario_revenue - monthly_fixed - scenario_var_cost
            scenario_profits.append(scenario_profit)
        
        fig_scenario = go.Figure(data=[
            go.Bar(x=scenarios, y=scenario_profits, 
                   marker_color=['#ef4444', '#3b82f6', '#10b981'],
                   text=[f"Rp {p:,.0f}" for p in scenario_profits],
                   textposition='outside')
        ])
        fig_scenario.update_layout(
            title="Profit per Skenario Utilisasi",
            yaxis_title="Profit (Rp)",
            height=300,
            showlegend=False
        )
        st.plotly_chart(fig_scenario, use_container_width=True)
    
    # Business Summary
    st.markdown("---")
    st.subheader("📊 Ringkasan Kelayakan Bisnis")
    
    # Determine feasibility
    is_feasible = monthly_profit > 0 and payback_months < 24 and roi_annual > 50
    
    if is_feasible:
        st.success(f"""
        ### ✅ BISNIS LAYAK!
        
        **Highlights:**
        - 💰 Profit: Rp {monthly_profit:,.0f}/bulan (Rp {annual_profit:,.0f}/tahun)
        - 📈 ROI: {roi_annual:.0f}% per tahun
        - ⏱️ Payback Period: {payback_months:.1f} bulan
        - 🎯 Break-Even: {breakeven_pct:.1f}% kapasitas
        - 💵 Margin: {(monthly_profit/total_revenue*100):.1f}%
        
        **Rekomendasi:**
        - Mulai dengan {num_drums} drum untuk test market
        - Focus pada produk Generatif (margin lebih tinggi)
        - Target utilisasi minimal {breakeven_pct:.0f}% untuk BEP
        - Investasi marketing {marketing_pct}% dari revenue
        """)
    else:
        st.warning(f"""
        ### ⚠️ PERLU OPTIMASI
        
        **Issues:**
        - Profit: Rp {monthly_profit:,.0f}/bulan
        - ROI: {roi_annual:.0f}% (target >50%)
        - Payback: {payback_months:.1f} bulan (target <24)
        
        **Saran Perbaikan:**
        - Tingkatkan margin jual (sekarang {margin_pct}%)
        - Kurangi biaya operasional
        - Tingkatkan utilisasi kapasitas
        - Review pricing strategy
        """)

# Footer
st.markdown("---")
st.caption("💡 **Tips:** POC terbaik menggunakan kombinasi bahan dengan rasio C/N optimal (25-30) dan NPK seimbang sesuai kebutuhan tanaman.")
