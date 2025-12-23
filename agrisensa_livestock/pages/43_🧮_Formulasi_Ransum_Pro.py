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
        "🤖 AI Auto-Formulation (Recommended)",
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

# ========== AI AUTO-FORMULATION (NEW - RECOMMENDED) ==========
if formulation_method == "🤖 AI Auto-Formulation (Recommended)":
    st.header("🤖 AI-Powered Automatic Feed Formulation")
    st.markdown("**Formulasi otomatis berdasarkan kebutuhan ternak Anda**")
    st.success("💡 Cukup masukkan data ternak, AI akan menghitung formulasi optimal secara otomatis!")
    
    # Get animal parameters from sidebar
    st.sidebar.markdown("### 📋 Data Ternak")
    
    # Determine animal type and get parameters
    if "Beef Cattle" in animal_type:
        body_weight = st.sidebar.number_input("Bobot Badan (kg)", 200, 800, 400, 10)
        adg = st.sidebar.number_input("Target Pertambahan BB (kg/hari)", 0.3, 2.0, 0.8, 0.1)
        sex = st.sidebar.selectbox("Jenis Kelamin", ["steer", "heifer", "bull"])
        
        nrc_req = get_beef_cattle_requirements(body_weight, adg, sex)
        animal_category = "ruminant"
        
    elif "Dairy Cattle" in animal_type:
        body_weight = st.sidebar.number_input("Bobot Badan (kg)", 400, 800, 600, 10)
        milk_prod = st.sidebar.number_input("Produksi Susu (kg/hari)", 5, 50, 20, 1)
        milk_fat = st.sidebar.number_input("Kadar Lemak Susu (%)", 2.5, 5.0, 3.5, 0.1)
        
        nrc_req = get_dairy_cattle_requirements(body_weight, milk_prod, milk_fat)
        animal_category = "ruminant"
        
    elif "Broiler" in animal_type:
        age_days = st.sidebar.number_input("Umur (hari)", 1, 45, 21, 1)
        
        nrc_req = get_broiler_requirements(age_days)
        animal_category = "poultry"
        
    elif "Layer" in animal_type:
        age_weeks = st.sidebar.number_input("Umur (minggu)", 1, 100, 30, 1)
        prod_rate = st.sidebar.number_input("Produksi Telur (%)", 50, 95, 85, 1)
        
        nrc_req = get_layer_requirements(age_weeks, prod_rate)
        animal_category = "poultry"
        
    elif "Goat" in animal_type:
        body_weight = st.sidebar.number_input("Bobot Badan (kg)", 10, 100, 30, 5)
        adg = st.sidebar.number_input("Target Pertambahan BB (kg/hari)", 0.05, 0.3, 0.15, 0.01)
        prod_type = st.sidebar.selectbox("Tipe Produksi", ["meat", "dairy", "maintenance"])
        
        nrc_req = get_goat_requirements(body_weight, adg, prod_type)
        animal_category = "ruminant"
        
    else:  # Sheep
        body_weight = st.sidebar.number_input("Bobot Badan (kg)", 10, 100, 40, 5)
        adg = st.sidebar.number_input("Target Pertambahan BB (kg/hari)", 0.05, 0.4, 0.20, 0.01)
        prod_type = st.sidebar.selectbox("Tipe Produksi", ["meat", "wool", "maintenance"])
        
        nrc_req = get_sheep_requirements(body_weight, adg, prod_type)
        animal_category = "ruminant"
    
    # Display NRC requirements
    st.subheader("📋 Kebutuhan Nutrisi (Standar NRC)")
    
    col_req1, col_req2, col_req3, col_req4 = st.columns(4)
    
    with col_req1:
        st.metric("Konsumsi Pakan", f"{nrc_req.get('dmi_kg_day', nrc_req.get('me_kcal_kg', 0)/1000):.1f} kg/hari" if 'dmi_kg_day' in nrc_req else "N/A")
    
    with col_req2:
        cp_key = 'crude_protein_percent'
        st.metric("Protein Kasar", f"{nrc_req.get(cp_key, 0):.1f}%")
    
    with col_req3:
        if 'total_ne_mcal' in nrc_req:
            st.metric("Total Energi", f"{nrc_req['total_ne_mcal']:.1f} Mcal NE")
        elif 'total_me_mcal' in nrc_req:
            st.metric("Total Energi", f"{nrc_req['total_me_mcal']:.1f} Mcal ME")
        else:
            st.metric("Energi", f"{nrc_req.get('me_kcal_kg', 0)} kcal/kg")
    
    with col_req4:
        st.metric("Kalsium", f"{nrc_req.get('calcium_percent', 0):.2f}%")
    
    st.divider()
    
    # Auto-select appropriate ingredients based on animal type
    st.subheader("🎯 Formulasi Otomatis")
    
    if animal_category == "ruminant":
        # Ruminant default ingredients
        default_ingredients = [
            "Jagung Kuning", "Bungkil Kedelai", "Dedak Padi", 
            "Rumput Gajah", "Hay Alfalfa",
            "Kapur (CaCO3)", "DCP (Dicalcium Phosphate)", "Garam (NaCl)"
        ]
        st.info("🐄 Bahan pakan untuk ruminansia: Jagung, Bungkil Kedelai, Dedak, Hijauan, Mineral")
    else:
        # Poultry default ingredients
        default_ingredients = [
            "Jagung Kuning", "Bungkil Kedelai", "Tepung Ikan",
            "Dedak Padi", "Minyak Kelapa Sawit",
            "Kapur (CaCO3)", "DCP (Dicalcium Phosphate)", "Garam (NaCl)",
            "DL-Methionine", "L-Lysine HCl"
        ]
        st.info("🐓 Bahan pakan untuk unggas: Jagung, Bungkil Kedelai, Tepung Ikan, Minyak, Mineral, Asam Amino")
    
    # Option to customize ingredients
    with st.expander("🔧 Sesuaikan Bahan Pakan (Opsional)"):
        selected_ingredients = st.multiselect(
            "Pilih bahan pakan yang tersedia",
            list(FEED_DATABASE.keys()),
            default=default_ingredients
        )
    
    if 'selected_ingredients' not in locals() or not selected_ingredients:
        selected_ingredients = default_ingredients
    
    # Formulation weight
    total_weight = st.number_input(
        "Total Pakan yang Diinginkan (kg)",
        min_value=10,
        max_value=10000,
        value=100,
        step=10,
        help="Jumlah total pakan yang akan diformulasikan"
    )
    
    # Auto-formulate button
    if st.button("🚀 Buat Formulasi Otomatis", type="primary", use_container_width=True, key="auto_formulate"):
        with st.spinner("🤖 AI sedang menghitung formulasi optimal..."):
            # Prepare ingredients
            ingredients_for_lp = {name: FEED_DATABASE[name] for name in selected_ingredients if name in FEED_DATABASE}
            
            # Define constraints based on NRC
            # Relax constraints to ±10% for better feasibility
            requirements = {
                'crude_protein': (
                    nrc_req.get('crude_protein_percent', 10) * 0.90,  # 90% of target
                    nrc_req.get('crude_protein_percent', 10) * 1.10   # 110% of target
                ),
                'calcium': (
                    nrc_req.get('calcium_percent', 0.5) * 0.85,  # More relaxed
                    nrc_req.get('calcium_percent', 0.5) * 1.15
                )
            }
            
            # Add phosphorus if available
            if 'phosphorus_percent' in nrc_req:
                requirements['phosphorus'] = (
                    nrc_req['phosphorus_percent'] * 0.85,
                    nrc_req['phosphorus_percent'] * 1.15
                )
            elif 'phosphorus_available_percent' in nrc_req:
                requirements['phosphorus'] = (
                    nrc_req['phosphorus_available_percent'] * 0.85,
                    nrc_req['phosphorus_available_percent'] * 1.15
                )
            
            # Add fiber constraints for ruminants (more relaxed)
            if animal_category == "ruminant":
                cf_min = nrc_req.get('crude_fiber_min_percent', 15)
                cf_max = nrc_req.get('crude_fiber_max_percent', 30)
                requirements['crude_fiber'] = (
                    max(10, cf_min * 0.8),  # At least 10%, or 80% of target
                    min(40, cf_max * 1.2)   # At most 40%, or 120% of target
                )
            
            # Run optimization
            result = least_cost_formulation(
                ingredients_for_lp,
                requirements,
                total_weight,
                animal_category
            )
            
            st.session_state['auto_result'] = result
    
    # Display results
    if 'auto_result' in st.session_state:
        result = st.session_state['auto_result']
        
        if 'error' in result:
            st.error(f"❌ {result['error']}")
            
            # Show debug information
            with st.expander("🔍 Debug Information"):
                st.markdown("**NRC Requirements:**")
                for key, val in nrc_req.items():
                    if isinstance(val, (int, float)):
                        st.write(f"- {key}: {val}")
                
                st.markdown("**Constraints Applied:**")
                for nutrient, (min_val, max_val) in requirements.items():
                    st.write(f"- {nutrient}: {min_val:.2f} - {max_val:.2f}")
                
                st.markdown("**Selected Ingredients:**")
                for ing in selected_ingredients:
                    if ing in FEED_DATABASE:
                        data = FEED_DATABASE[ing]
                        st.write(f"- {ing}: CP={data['crude_protein']}%, CF={data['crude_fiber']}%, Ca={data['calcium']}%, P={data['phosphorus']}%")
                
                if 'message' in result:
                    st.code(result['message'])
            
            st.warning("💡 **Saran:**")
            st.markdown("""
            - Coba tambah lebih banyak bahan pakan (terutama sumber protein & mineral)
            - Periksa apakah bahan pakan yang dipilih bisa memenuhi kebutuhan
            - Untuk ruminansia, pastikan ada hijauan (rumput/hay) untuk serat
            - Untuk unggas, pastikan ada sumber protein tinggi (tepung ikan/bungkil kedelai)
            - Constraints sudah direlaksasi ±10-15% dari target NRC
            """)
        else:
            st.success("✅ **Formulasi Optimal Berhasil Dibuat!**")
            
            # Cost summary
            col_cost1, col_cost2, col_cost3 = st.columns(3)
            
            with col_cost1:
                st.metric("💰 Total Biaya", f"Rp {result['total_cost']:,.0f}")
            
            with col_cost2:
                st.metric("📊 Biaya per kg", f"Rp {result['cost_per_kg']:,.0f}")
            
            with col_cost3:
                # Calculate daily cost
                daily_cost = result['cost_per_kg'] * nrc_req.get('dmi_kg_day', 1)
                st.metric("💵 Biaya Harian", f"Rp {daily_cost:,.0f}")
            
            st.divider()
            
            # Formulation table
            st.subheader("📋 Komposisi Ransum")
            
            form_data = []
            for ing_name, data in result['formulation'].items():
                form_data.append({
                    "Bahan Pakan": ing_name,
                    "Berat (kg)": f"{data['weight_kg']:.2f}",
                    "Persentase": f"{data['percentage']:.1f}%",
                    "Biaya (Rp)": f"{data['cost_idr']:,.0f}"
                })
            
            df_form = pd.DataFrame(form_data)
            st.dataframe(df_form, use_container_width=True, hide_index=True)
            
            # Pie chart
            fig_pie = px.pie(
                df_form,
                names='Bahan Pakan',
                values=[float(x.replace('%', '')) for x in df_form['Persentase']],
                title="Komposisi Ransum (%)"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Nutritional analysis
            st.divider()
            st.subheader("🔬 Analisis Nutrisi")
            
            nutr = result['nutritional_analysis']
            
            col_n1, col_n2, col_n3, col_n4, col_n5 = st.columns(5)
            
            with col_n1:
                st.metric("Protein Kasar", f"{nutr['crude_protein']:.2f}%")
            
            with col_n2:
                st.metric("Serat Kasar", f"{nutr['crude_fiber']:.2f}%")
            
            with col_n3:
                st.metric("TDN", f"{nutr['tdn']:.1f}%")
            
            with col_n4:
                st.metric("Kalsium", f"{nutr['calcium']:.2f}%")
            
            with col_n5:
                st.metric("Fosfor", f"{nutr['phosphorus']:.2f}%")
            
            # Energy analysis
            if animal_category == "ruminant":
                col_e1, col_e2, col_e3 = st.columns(3)
                
                with col_e1:
                    st.metric("DE", f"{nutr['de_ruminant']:.2f} Mcal/kg")
                
                with col_e2:
                    st.metric("ME", f"{nutr['me_ruminant']:.2f} Mcal/kg")
                
                with col_e3:
                    # Calculate if meets requirement
                    if 'total_me_mcal' in nrc_req:
                        daily_me = nutr['me_ruminant'] * nrc_req.get('dmi_kg_day', 1)
                        st.metric("ME Harian", f"{daily_me:.1f} Mcal")
            
            # Constraint check
            st.divider()
            st.subheader("✅ Pemenuhan Standar NRC")
            
            constraints = result['constraints_met']
            
            check_data = []
            for nutrient, data in constraints.items():
                nutrient_name = nutrient.replace('_', ' ').title()
                check_data.append({
                    "Nutrisi": nutrient_name,
                    "Aktual": f"{data['actual']:.2f}",
                    "Target": data['required'],
                    "Status": data['status']
                })
            
            df_check = pd.DataFrame(check_data)
            st.dataframe(df_check, use_container_width=True, hide_index=True)
            
            # Download button
            st.divider()
            
            # Prepare download data
            download_data = {
                "Animal Type": [animal_type],
                "Total Weight (kg)": [total_weight],
                "Total Cost (Rp)": [result['total_cost']],
                "Cost per kg (Rp)": [result['cost_per_kg']]
            }
            
            # Add formulation
            for ing_name, data in result['formulation'].items():
                download_data[f"{ing_name} (kg)"] = [data['weight_kg']]
            
            df_download = pd.DataFrame(download_data)
            csv = df_download.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                "📥 Download Formulasi (CSV)",
                csv,
                f"formulasi_{animal_type.replace(' ', '_')}.csv",
                "text/csv",
                key='download-formulation'
            )

# ========== FEED DATABASE BROWSER ==========
elif formulation_method == "📊 Feed Database Browser":
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
