import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Feed Formulation Pro - AgriSensa", page_icon="🧮", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

# Import services
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.feed_database_service import (
    FEED_DATABASE, get_feed_by_category, search_feeds, 
    get_all_categories, compare_feeds
)
from services.formulation_methods import (
    pearson_square, least_cost_formulation, calculate_tdn,
    calculate_de, calculate_me_ruminant, calculate_me_poultry,
    full_energy_analysis
)
from services.nrc_standards import (
    get_beef_cattle_requirements, get_dairy_cattle_requirements,
    get_broiler_requirements, get_layer_requirements,
    get_goat_requirements, get_sheep_requirements,
    check_amino_acid_balance, IDEAL_PROTEIN_RATIOS
)

# ==========================================
# HEADER
# ==========================================
st.title("🧮 Advanced Feed Formulation System")
st.markdown("**Professional-Grade Ration Formulation with NRC Standards**")
st.info("💡 Sistem formulasi ransum berbasis ilmiah dengan database 40+ bahan pakan, 3 metode formulasi, dan standar NRC")

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("🎯 Formulation Settings")

# Animal Type Selection
animal_type = st.sidebar.selectbox(
    "Select Animal Type",
    [
        "🐄 Beef Cattle (Sapi Potong)",
        "🥛 Dairy Cattle (Sapi Perah)",
        "🐓 Broiler (Ayam Pedaging)",
        "🥚 Layer (Ayam Petelur)",
        "🐐 Goat (Kambing)",
        "🐑 Sheep (Domba)"
    ]
)

# Formulation Method Selection
formulation_method = st.sidebar.selectbox(
    "Formulation Method",
    [
        "📐 Pearson Square (2 ingredients)",
        "🎯 Linear Programming (Least-Cost)",
        "🧮 Trial & Error (Manual)",
        "📊 Feed Database Browser"
    ]
)

st.sidebar.divider()

# ==========================================
# MAIN CONTENT AREA
# ==========================================

# ========== FEED DATABASE BROWSER ==========
if formulation_method == "📊 Feed Database Browser":
    st.header("📊 Feed Database Browser")
    st.markdown(f"**Total Ingredients:** {len(FEED_DATABASE)} bahan pakan")
    
    # Search and Filter
    col_search, col_filter = st.columns([2, 1])
    
    with col_search:
        search_query = st.text_input("🔍 Search by name", placeholder="e.g., Jagung, Kedelai...")
    
    with col_filter:
        categories = ["All Categories"] + get_all_categories()
        selected_category = st.selectbox("Filter by Category", categories)
    
    # Get feeds
    if search_query:
        feeds_to_show = search_feeds(search_query)
    elif selected_category != "All Categories":
        feeds_to_show = get_feed_by_category(selected_category)
    else:
        feeds_to_show = FEED_DATABASE
    
    st.markdown(f"**Showing {len(feeds_to_show)} ingredients**")
    
    # Display as table
    if feeds_to_show:
        feed_data = []
        for name, data in feeds_to_show.items():
            feed_data.append({
                "Ingredient": name,
                "Category": data['category'],
                "CP (%)": data['crude_protein'],
                "CF (%)": data['crude_fiber'],
                "TDN (%)": data['tdn'],
                "ME Ruminant (Mcal/kg)": data['me_ruminant'],
                "Ca (%)": data['calcium'],
                "P (%)": data['phosphorus'],
                "Price (Rp/kg)": data['price_per_kg']
            })
        
        df_feeds = pd.DataFrame(feed_data)
        st.dataframe(df_feeds, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df_feeds.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download as CSV",
            csv,
            "feed_database.csv",
            "text/csv",
            key='download-csv'
        )
        
        # Detailed view
        st.divider()
        st.markdown("### 🔬 Detailed Nutrient Profile")
        
        selected_feed = st.selectbox("Select ingredient for detailed view", list(feeds_to_show.keys()))
        
        if selected_feed:
            feed_detail = FEED_DATABASE[selected_feed]
            
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                st.markdown("**📊 Proximate Analysis**")
                st.metric("Dry Matter", f"{feed_detail['dry_matter']}%")
                st.metric("Crude Protein", f"{feed_detail['crude_protein']}%")
                st.metric("Crude Fiber", f"{feed_detail['crude_fiber']}%")
                st.metric("Ether Extract", f"{feed_detail['ether_extract']}%")
                st.metric("Ash", f"{feed_detail['ash']}%")
                st.metric("NFE", f"{feed_detail['nfe']}%")
            
            with col_d2:
                st.markdown("**⚡ Energy Values**")
                st.metric("TDN", f"{feed_detail['tdn']}%")
                st.metric("DE (Ruminant)", f"{feed_detail['de_ruminant']} Mcal/kg")
                st.metric("ME (Ruminant)", f"{feed_detail['me_ruminant']} Mcal/kg")
                st.metric("NE Lactation", f"{feed_detail['ne_lactation']} Mcal/kg")
                st.metric("ME (Poultry)", f"{feed_detail['me_poultry']} Mcal/kg")
            
            with col_d3:
                st.markdown("**🧬 Amino Acids & Minerals**")
                st.metric("Lysine", f"{feed_detail['lysine']}%")
                st.metric("Methionine", f"{feed_detail['methionine']}%")
                st.metric("Calcium", f"{feed_detail['calcium']}%")
                st.metric("Phosphorus", f"{feed_detail['phosphorus']}%")
                st.metric("Price", f"Rp {feed_detail['price_per_kg']:,}/kg")

# ========== PEARSON SQUARE METHOD ==========
elif formulation_method == "📐 Pearson Square (2 ingredients)":
    st.header("📐 Pearson Square Method")
    st.markdown("**Simple 2-ingredient formulation for meeting a single nutrient target**")
    
    col_ps1, col_ps2 = st.columns(2)
    
    with col_ps1:
        st.subheader("🔧 Input Parameters")
        
        target_nutrient = st.number_input(
            "Target Nutrient Level (%)",
            min_value=0.0,
            max_value=100.0,
            value=18.0,
            step=0.5,
            help="e.g., 18% Crude Protein"
        )
        
        nutrient_type = st.selectbox(
            "Nutrient Type",
            ["Crude Protein", "TDN", "Crude Fiber"]
        )
        
        st.divider()
        
        # Ingredient 1
        st.markdown("**Ingredient 1 (High in nutrient)**")
        ing1_name = st.selectbox("Select Ingredient 1", list(FEED_DATABASE.keys()), key="ps_ing1")
        
        if nutrient_type == "Crude Protein":
            ing1_nutrient = FEED_DATABASE[ing1_name]['crude_protein']
        elif nutrient_type == "TDN":
            ing1_nutrient = FEED_DATABASE[ing1_name]['tdn']
        else:
            ing1_nutrient = FEED_DATABASE[ing1_name]['crude_fiber']
        
        st.info(f"{nutrient_type}: {ing1_nutrient}%")
        
        # Ingredient 2
        st.markdown("**Ingredient 2 (Low in nutrient)**")
        ing2_name = st.selectbox("Select Ingredient 2", list(FEED_DATABASE.keys()), key="ps_ing2")
        
        if nutrient_type == "Crude Protein":
            ing2_nutrient = FEED_DATABASE[ing2_name]['crude_protein']
        elif nutrient_type == "TDN":
            ing2_nutrient = FEED_DATABASE[ing2_name]['tdn']
        else:
            ing2_nutrient = FEED_DATABASE[ing2_name]['crude_fiber']
        
        st.info(f"{nutrient_type}: {ing2_nutrient}%")
        
        if st.button("🔬 Calculate Pearson Square", type="primary", use_container_width=True):
            result = pearson_square(target_nutrient, ing1_name, ing1_nutrient, ing2_name, ing2_nutrient)
            st.session_state['ps_result'] = result
    
    with col_ps2:
        st.subheader("📊 Results")
        
        if 'ps_result' in st.session_state:
            result = st.session_state['ps_result']
            
            if 'error' in result:
                st.error(f"❌ {result['error']}")
            else:
                # Visual representation
                st.success(f"✅ Target: {result['target_nutrient']}% | Calculated: {result['calculated_nutrient']}%")
                
                # Proportions
                col_r1, col_r2 = st.columns(2)
                
                with col_r1:
                    st.metric(
                        result['ingredient1'],
                        f"{result['ingredient1_percentage']}%",
                        f"{result['ingredient1_parts']} parts"
                    )
                
                with col_r2:
                    st.metric(
                        result['ingredient2'],
                        f"{result['ingredient2_percentage']}%",
                        f"{result['ingredient2_parts']} parts"
                    )
                
                # Pie chart
                fig_ps = px.pie(
                    names=[result['ingredient1'], result['ingredient2']],
                    values=[result['ingredient1_percentage'], result['ingredient2_percentage']],
                    title="Formulation Composition"
                )
                st.plotly_chart(fig_ps, use_container_width=True)
                
                # For 100 kg
                st.divider()
                st.markdown("### 📦 For 100 kg Total Feed")
                
                ing1_kg = result['ingredient1_percentage']
                ing2_kg = result['ingredient2_percentage']
                
                ing1_cost = ing1_kg * FEED_DATABASE[result['ingredient1']]['price_per_kg']
                ing2_cost = ing2_kg * FEED_DATABASE[result['ingredient2']]['price_per_kg']
                total_cost = ing1_cost + ing2_cost
                
                cost_data = pd.DataFrame({
                    "Ingredient": [result['ingredient1'], result['ingredient2'], "TOTAL"],
                    "Weight (kg)": [ing1_kg, ing2_kg, 100],
                    "Cost (Rp)": [ing1_cost, ing2_cost, total_cost]
                })
                
                st.dataframe(cost_data, use_container_width=True, hide_index=True)
                st.success(f"**Total Cost:** Rp {total_cost:,.0f} (Rp {total_cost/100:,.0f}/kg)")
        else:
            st.info("Enter parameters and click Calculate to see results")

# ========== LINEAR PROGRAMMING ==========
elif formulation_method == "🎯 Linear Programming (Least-Cost)":
    st.header("🎯 Linear Programming - Least-Cost Formulation")
    st.markdown("**Optimize feed cost while meeting all nutritional requirements**")
    
    # Get NRC requirements based on animal type
    st.sidebar.markdown("### 📋 Animal Parameters")
    
    if "Beef Cattle" in animal_type:
        body_weight = st.sidebar.number_input("Body Weight (kg)", 200, 800, 400)
        adg = st.sidebar.number_input("Target ADG (kg/day)", 0.3, 2.0, 0.8, 0.1)
        sex = st.sidebar.selectbox("Sex", ["steer", "heifer", "bull"])
        
        nrc_req = get_beef_cattle_requirements(body_weight, adg, sex)
        
    elif "Dairy Cattle" in animal_type:
        body_weight = st.sidebar.number_input("Body Weight (kg)", 400, 800, 600)
        milk_prod = st.sidebar.number_input("Milk Production (kg/day)", 5, 50, 20)
        milk_fat = st.sidebar.number_input("Milk Fat (%)", 2.5, 5.0, 3.5, 0.1)
        
        nrc_req = get_dairy_cattle_requirements(body_weight, milk_prod, milk_fat)
        
    elif "Broiler" in animal_type:
        age_days = st.sidebar.number_input("Age (days)", 1, 45, 21)
        
        nrc_req = get_broiler_requirements(age_days)
        
    elif "Layer" in animal_type:
        age_weeks = st.sidebar.number_input("Age (weeks)", 1, 100, 30)
        prod_rate = st.sidebar.number_input("Production Rate (%)", 50, 95, 85)
        
        nrc_req = get_layer_requirements(age_weeks, prod_rate)
        
    elif "Goat" in animal_type:
        body_weight = st.sidebar.number_input("Body Weight (kg)", 10, 100, 30)
        adg = st.sidebar.number_input("Target ADG (kg/day)", 0.05, 0.3, 0.15, 0.01)
        prod_type = st.sidebar.selectbox("Production Type", ["meat", "dairy", "maintenance"])
        
        nrc_req = get_goat_requirements(body_weight, adg, prod_type)
        
    else:  # Sheep
        body_weight = st.sidebar.number_input("Body Weight (kg)", 10, 100, 40)
        adg = st.sidebar.number_input("Target ADG (kg/day)", 0.05, 0.4, 0.20, 0.01)
        prod_type = st.sidebar.selectbox("Production Type", ["meat", "wool", "maintenance"])
        
        nrc_req = get_sheep_requirements(body_weight, adg, prod_type)
    
    # Display NRC requirements
    st.subheader("📋 NRC Nutritional Requirements")
    
    col_nrc1, col_nrc2, col_nrc3, col_nrc4 = st.columns(4)
    
    with col_nrc1:
        st.metric("DMI", f"{nrc_req.get('dmi_kg_day', 0):.2f} kg/day")
    
    with col_nrc2:
        cp_key = 'crude_protein_percent'
        st.metric("Crude Protein", f"{nrc_req.get(cp_key, 0):.1f}%")
    
    with col_nrc3:
        if 'total_ne_mcal' in nrc_req:
            st.metric("Total NE", f"{nrc_req['total_ne_mcal']:.2f} Mcal")
        elif 'total_me_mcal' in nrc_req:
            st.metric("Total ME", f"{nrc_req['total_me_mcal']:.2f} Mcal")
        else:
            st.metric("ME", f"{nrc_req.get('me_kcal_kg', 0)} kcal/kg")
    
    with col_nrc4:
        st.metric("Calcium", f"{nrc_req.get('calcium_percent', 0):.2f}%")
    
    st.divider()
    
    # Ingredient selection for LP
    st.subheader("🔧 Select Available Ingredients")
    
    # Multi-select for ingredients
    available_ingredients = st.multiselect(
        "Choose ingredients to include in formulation",
        list(FEED_DATABASE.keys()),
        default=["Jagung Kuning", "Bungkil Kedelai", "Dedak Padi", "Kapur (CaCO3)", "DCP (Dicalcium Phosphate)"]
    )
    
    if len(available_ingredients) < 3:
        st.warning("⚠️ Select at least 3 ingredients for meaningful optimization")
    else:
        # Prepare ingredients dict
        ingredients_for_lp = {name: FEED_DATABASE[name] for name in available_ingredients}
        
        # Define constraints based on NRC
        requirements = {
            'crude_protein': (nrc_req.get('crude_protein_percent', 10) * 0.95, 
                            nrc_req.get('crude_protein_percent', 10) * 1.05),
            'calcium': (nrc_req.get('calcium_percent', 0.5) * 0.9,
                       nrc_req.get('calcium_percent', 0.5) * 1.1),
            'phosphorus': (nrc_req.get('phosphorus_percent', 0.3) * 0.9 if 'phosphorus_percent' in nrc_req else (0.3, 0.5),
                          nrc_req.get('phosphorus_percent', 0.3) * 1.1 if 'phosphorus_percent' in nrc_req else (0.3, 0.5))
        }
        
        # Add fiber constraints for ruminants
        if "Cattle" in animal_type or "Goat" in animal_type or "Sheep" in animal_type:
            requirements['crude_fiber'] = (nrc_req.get('crude_fiber_min_percent', 15),
                                          nrc_req.get('crude_fiber_max_percent', 30))
        
        total_weight = st.number_input("Total Formulation Weight (kg)", 10, 1000, 100, 10)
        
        if st.button("🚀 Run Linear Programming Optimization", type="primary", use_container_width=True):
            with st.spinner("Optimizing formulation..."):
                result = least_cost_formulation(
                    ingredients_for_lp,
                    requirements,
                    total_weight,
                    "cattle" if "Cattle" in animal_type else "poultry"
                )
                
                st.session_state['lp_result'] = result
        
        # Display results
        if 'lp_result' in st.session_state:
            result = st.session_state['lp_result']
            
            if 'error' in result:
                st.error(f"❌ {result['error']}")
                st.info("💡 Try: Relax constraints, add more ingredients, or check if requirements are feasible")
            else:
                st.success("✅ Optimal Solution Found!")
                
                col_res1, col_res2 = st.columns(2)
                
                with col_res1:
                    st.metric("Total Cost", f"Rp {result['total_cost']:,.0f}")
                    st.metric("Cost per kg", f"Rp {result['cost_per_kg']:,.0f}")
                
                with col_res2:
                    # Formulation table
                    form_data = []
                    for ing_name, data in result['formulation'].items():
                        form_data.append({
                            "Ingredient": ing_name,
                            "Weight (kg)": data['weight_kg'],
                            "Percentage": f"{data['percentage']:.1f}%",
                            "Cost (Rp)": f"{data['cost_idr']:,.0f}"
                        })
                    
                    df_form = pd.DataFrame(form_data)
                    st.dataframe(df_form, use_container_width=True, hide_index=True)
                
                # Nutritional analysis
                st.divider()
                st.markdown("### 📊 Nutritional Analysis")
                
                nutr_analysis = result['nutritional_analysis']
                
                col_n1, col_n2, col_n3, col_n4 = st.columns(4)
                
                with col_n1:
                    st.metric("Crude Protein", f"{nutr_analysis['crude_protein']:.2f}%")
                
                with col_n2:
                    st.metric("Crude Fiber", f"{nutr_analysis['crude_fiber']:.2f}%")
                
                with col_n3:
                    st.metric("Calcium", f"{nutr_analysis['calcium']:.2f}%")
                
                with col_n4:
                    st.metric("Phosphorus", f"{nutr_analysis['phosphorus']:.2f}%")
                
                # Constraints check
                st.markdown("### ✅ Constraint Satisfaction")
                
                constraints_check = result['constraints_met']
                
                check_data = []
                for nutrient, data in constraints_check.items():
                    check_data.append({
                        "Nutrient": nutrient.replace('_', ' ').title(),
                        "Actual": f"{data['actual']:.2f}",
                        "Required": data['required'],
                        "Status": data['status']
                    })
                
                df_check = pd.DataFrame(check_data)
                st.dataframe(df_check, use_container_width=True, hide_index=True)

# ========== TRIAL & ERROR METHOD ==========
else:  # Trial & Error
    st.header("🧮 Trial & Error - Manual Formulation")
    st.markdown("**Manually adjust ingredient proportions to meet targets**")
    
    st.info("This is the existing trial & error method. You can enhance it with NRC standards integration.")
    
    # Initialize session state
    if 'manual_ingredients' not in st.session_state:
        st.session_state.manual_ingredients = [
            {"name": "Jagung Kuning", "proportion": 50.0},
            {"name": "Bungkil Kedelai", "proportion": 30.0},
            {"name": "Dedak Padi", "proportion": 20.0}
        ]
    
    col_man1, col_man2 = st.columns([1, 1])
    
    with col_man1:
        st.subheader("🔧 Ingredient Proportions")
        
        total_proportion = 0
        updated_ingredients = []
        
        for i, ing in enumerate(st.session_state.manual_ingredients):
            col_name, col_prop = st.columns([2, 1])
            
            with col_name:
                name = st.selectbox(f"Ingredient {i+1}", list(FEED_DATABASE.keys()), 
                                  index=list(FEED_DATABASE.keys()).index(ing['name']) if ing['name'] in FEED_DATABASE else 0,
                                  key=f"man_name_{i}")
            
            with col_prop:
                prop = st.number_input(f"%", 0.0, 100.0, ing['proportion'], 1.0, key=f"man_prop_{i}")
            
            updated_ingredients.append({"name": name, "proportion": prop})
            total_proportion += prop
        
        st.session_state.manual_ingredients = updated_ingredients
        
        # Add/Remove buttons
        col_add, col_remove = st.columns(2)
        
        with col_add:
            if st.button("➕ Add Ingredient"):
                st.session_state.manual_ingredients.append({"name": "Jagung Kuning", "proportion": 0.0})
                st.rerun()
        
        with col_remove:
            if len(st.session_state.manual_ingredients) > 1:
                if st.button("➖ Remove Last"):
                    st.session_state.manual_ingredients.pop()
                    st.rerun()
        
        # Total check
        if abs(total_proportion - 100.0) > 0.1:
            st.error(f"⚠️ Total proportion: {total_proportion:.1f}% (should be 100%)")
        else:
            st.success(f"✅ Total proportion: {total_proportion:.1f}%")
    
    with col_man2:
        st.subheader("📊 Nutritional Analysis")
        
        if abs(total_proportion - 100.0) < 0.1:
            # Calculate weighted average
            nutrients = {
                "crude_protein": 0,
                "crude_fiber": 0,
                "tdn": 0,
                "calcium": 0,
                "phosphorus": 0,
                "me_ruminant": 0
            }
            
            total_cost = 0
            
            for ing in st.session_state.manual_ingredients:
                prop = ing['proportion'] / 100
                feed_data = FEED_DATABASE[ing['name']]
                
                for nutrient in nutrients.keys():
                    nutrients[nutrient] += feed_data[nutrient] * prop
                
                total_cost += feed_data['price_per_kg'] * prop
            
            # Display metrics
            col_m1, col_m2 = st.columns(2)
            
            with col_m1:
                st.metric("Crude Protein", f"{nutrients['crude_protein']:.2f}%")
                st.metric("Crude Fiber", f"{nutrients['crude_fiber']:.2f}%")
                st.metric("TDN", f"{nutrients['tdn']:.2f}%")
            
            with col_m2:
                st.metric("Calcium", f"{nutrients['calcium']:.2f}%")
                st.metric("Phosphorus", f"{nutrients['phosphorus']:.2f}%")
                st.metric("ME (Ruminant)", f"{nutrients['me_ruminant']:.2f} Mcal/kg")
            
            st.divider()
            st.metric("Cost per kg", f"Rp {total_cost:,.0f}")
            
            # Composition pie chart
            fig_comp = px.pie(
                names=[ing['name'] for ing in st.session_state.manual_ingredients],
                values=[ing['proportion'] for ing in st.session_state.manual_ingredients],
                title="Formulation Composition"
            )
            st.plotly_chart(fig_comp, use_container_width=True)
