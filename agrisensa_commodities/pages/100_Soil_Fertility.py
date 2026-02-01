import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.soil_fertility_service import SoilFertilityService

# Page config
st.set_page_config(
    page_title="Soil Fertility & Nutrient Management",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .nutrient-card {
        background: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
        border-radius: 5px;
    }
    .warning-card {
        background: #fff3cd;
        padding: 15px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌱 Soil Fertility & Nutrient Management Calculator")
st.markdown("""
<div class='info-box'>
    <h3>🔬 Science-Based Soil Analysis</h3>
    <p>Comprehensive fertility assessment using:</p>
    <ul>
        <li>✅ <strong>Albrecht's Base Saturation Method</strong> - Optimal cation balance</li>
        <li>✅ <strong>Troug's pH-Nutrient Availability</strong> - pH impact on nutrients</li>
        <li>✅ <strong>Liebig's Law of Minimum</strong> - Identify limiting factors</li>
        <li>✅ <strong>CEC Analysis</strong> - Soil nutrient holding capacity</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Create tabs
tabs = st.tabs([
    "📊 Soil Analysis",
    "🎯 Base Saturation",
    "📈 pH & Availability",
    "🔍 Limiting Nutrients",
    "💊 Fertilizer Recommendations",
    "📚 Educational Guide"
])

# TAB 1: SOIL ANALYSIS INPUT
with tabs[0]:
    st.markdown("## 📊 Enter Your Soil Test Results")
    
    st.info("💡 **Get a soil test from a certified lab for accurate results.** This calculator uses standard soil test parameters.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧪 Basic Parameters")
        
        ph = st.number_input(
            "pH (Soil Acidity)",
            min_value=3.0,
            max_value=9.0,
            value=6.5,
            step=0.1,
            help="Optimal range: 6.0-7.0 for most crops"
        )
        
        cec = st.number_input(
            "CEC - Cation Exchange Capacity (meq/100g)",
            min_value=1.0,
            max_value=50.0,
            value=15.0,
            step=0.5,
            help="Soil's ability to hold nutrients. Higher is better. Sandy: 5-15, Loam: 10-25, Clay: 20-40"
        )
        
        st.markdown("### 🔬 Macronutrients (ppm or mg/kg)")
        
        n = st.number_input("Nitrogen (N)", min_value=0.0, max_value=200.0, value=45.0, step=5.0)
        p = st.number_input("Phosphorus (P)", min_value=0.0, max_value=150.0, value=25.0, step=5.0)
        k = st.number_input("Potassium (K)", min_value=0.0, max_value=800.0, value=250.0, step=10.0)
    
    with col2:
        st.markdown("### ⚡ Secondary Nutrients (ppm)")
        
        ca = st.number_input("Calcium (Ca)", min_value=0.0, max_value=6000.0, value=1800.0, step=100.0)
        mg = st.number_input("Magnesium (Mg)", min_value=0.0, max_value=800.0, value=280.0, step=20.0)
        s = st.number_input("Sulfur (S)", min_value=0.0, max_value=100.0, value=30.0, step=5.0)
        
        st.markdown("### 🔹 Micronutrients (ppm)")
        
        col_micro1, col_micro2 = st.columns(2)
        
        with col_micro1:
            fe = st.number_input("Iron (Fe)", min_value=0.0, max_value=50.0, value=8.0, step=0.5)
            mn = st.number_input("Manganese (Mn)", min_value=0.0, max_value=100.0, value=12.0, step=1.0)
            zn = st.number_input("Zinc (Zn)", min_value=0.0, max_value=20.0, value=2.5, step=0.5)
        
        with col_micro2:
            cu = st.number_input("Copper (Cu)", min_value=0.0, max_value=10.0, value=1.2, step=0.1)
            b = st.number_input("Boron (B)", min_value=0.0, max_value=5.0, value=0.8, step=0.1)
            mo = st.number_input("Molybdenum (Mo)", min_value=0.0, max_value=2.0, value=0.2, step=0.05)
    
    st.markdown("---")
    
    # Nutrient status summary
    st.markdown("### 📋 Nutrient Status Summary")
    
    soil_data = {
        'N': n, 'P': p, 'K': k, 'Ca': ca, 'Mg': mg, 'S': s,
        'Fe': fe, 'Mn': mn, 'Zn': zn, 'Cu': cu, 'B': b, 'Mo': mo
    }
    
    # Create status table
    status_data = []
    for nutrient, value in soil_data.items():
        is_micro = nutrient in ['Fe', 'Mn', 'Zn', 'Cu', 'B', 'Mo']
        level = SoilFertilityService.classify_nutrient_level(nutrient, value, is_micro)
        
        # Color coding
        if 'Very Low' in level or 'Deficient' in level:
            color = "🔴"
        elif 'Low' in level:
            color = "🟡"
        elif 'Medium' in level or 'Sufficient' in level:
            color = "🟢"
        else:
            color = "🔵"
        
        status_data.append({
            'Nutrient': nutrient,
            'Value': f"{value} ppm",
            'Status': f"{color} {level}"
        })
    
    df_status = pd.DataFrame(status_data)
    st.dataframe(df_status, use_container_width=True, hide_index=True)

# TAB 2: BASE SATURATION
with tabs[1]:
    st.markdown("## 🎯 Base Saturation Analysis (Albrecht Method)")
    
    st.markdown("""
    <div class='nutrient-card'>
        <h4>📖 What is Base Saturation?</h4>
        <p>Base saturation refers to the percentage of CEC occupied by basic cations (Ca, Mg, K, Na). 
        Dr. William Albrecht's research showed that optimal plant growth occurs when these cations are in specific ratios:</p>
        <ul>
            <li><strong>Calcium (Ca):</strong> 65% - Structural integrity, cell walls</li>
            <li><strong>Magnesium (Mg):</strong> 10% - Chlorophyll, photosynthesis</li>
            <li><strong>Potassium (K):</strong> 5% - Water regulation, disease resistance</li>
            <li><strong>Sodium (Na):</strong> 0.5% - Minor role</li>
            <li><strong>Hydrogen (H):</strong> 10% - Soil acidity</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Convert ppm to meq/100g (simplified conversion)
    ca_meq = ca / 200  # Ca: 200 ppm ≈ 1 meq/100g
    mg_meq = mg / 120  # Mg: 120 ppm ≈ 1 meq/100g
    k_meq = k / 390    # K: 390 ppm ≈ 1 meq/100g
    na_meq = 0.1       # Assume low sodium
    
    base_sat = SoilFertilityService.calculate_base_saturation(ca_meq, mg_meq, k_meq, na_meq, cec)
    
    if 'error' not in base_sat:
        col_bs1, col_bs2 = st.columns(2)
        
        with col_bs1:
            st.markdown("### 📊 Actual vs Ideal Base Saturation")
            
            # Create comparison chart
            categories = ['Ca', 'Mg', 'K', 'Na', 'H']
            actual_values = [base_sat['actual'][cat] for cat in categories]
            ideal_values = [base_sat['ideal'][cat] for cat in categories]
            
            fig_bs = go.Figure(data=[
                go.Bar(name='Actual', x=categories, y=actual_values, marker_color='#ff6b6b'),
                go.Bar(name='Ideal (Albrecht)', x=categories, y=ideal_values, marker_color='#4ecdc4')
            ])
            fig_bs.update_layout(
                title="Base Saturation Comparison (%)",
                barmode='group',
                yaxis_title="Percentage (%)",
                xaxis_title="Cation"
            )
            st.plotly_chart(fig_bs, use_container_width=True)
        
        with col_bs2:
            st.markdown("### ⚖️ Cation Ratios")
            
            ratios_df = pd.DataFrame({
                'Ratio': ['Ca:Mg', 'Ca:K', 'Mg:K'],
                'Actual': [base_sat['ratios']['Ca:Mg'], base_sat['ratios']['Ca:K'], base_sat['ratios']['Mg:K']],
                'Ideal': [base_sat['ideal_ratios']['Ca:Mg'], base_sat['ideal_ratios']['Ca:K'], base_sat['ideal_ratios']['Mg:K']]
            })
            
            st.dataframe(ratios_df, use_container_width=True, hide_index=True)
            
            st.markdown(f"""
            **Total Base Saturation:** {base_sat['total_base_saturation']:.1f}%
            
            **Interpretation:**
            - Ca:Mg ratio of 6-7:1 is ideal
            - Ca:K ratio of 12-15:1 is ideal
            - Mg:K ratio of 2-3:1 is ideal
            """)
            
            # Recommendations
            if base_sat['actual']['Ca'] < 60:
                st.warning("⚠️ **Low Calcium**: Consider applying lime (calcitic or dolomitic)")
            if base_sat['actual']['Mg'] < 8:
                st.warning("⚠️ **Low Magnesium**: Consider applying dolomitic lime or Epsom salt")
            if base_sat['actual']['K'] < 3:
                st.warning("⚠️ **Low Potassium**: Consider applying potassium sulfate or KCl")

# TAB 3: pH & NUTRIENT AVAILABILITY
with tabs[2]:
    st.markdown("## 📈 pH and Nutrient Availability (Troug Diagram)")
    
    st.markdown("""
    <div class='nutrient-card'>
        <h4>📖 Why pH Matters</h4>
        <p>Soil pH dramatically affects nutrient availability. Even if nutrients are present in soil, 
        they may be "locked up" and unavailable to plants if pH is too high or too low.</p>
        <p><strong>Dr. Emil Troug (1946)</strong> created the famous diagram showing how each nutrient's 
        availability changes with pH. Most nutrients are optimally available at pH 6.0-7.0.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get availability at current pH
    availability = SoilFertilityService.get_nutrient_availability_by_ph(ph)
    
    col_ph1, col_ph2 = st.columns([2, 1])
    
    with col_ph1:
        st.markdown("### 📊 Nutrient Availability Curves")
        
        # Create pH range for curves
        ph_range = np.linspace(4.0, 8.5, 100)
        
        # Calculate availability for each pH
        curves_data = {nutrient: [] for nutrient in availability.keys()}
        for ph_val in ph_range:
            avail = SoilFertilityService.get_nutrient_availability_by_ph(ph_val)
            for nutrient, value in avail.items():
                curves_data[nutrient].append(value)
        
        # Create figure
        fig_ph = go.Figure()
        
        # Macronutrients
        for nutrient in ['N', 'P', 'K']:
            fig_ph.add_trace(go.Scatter(
                x=ph_range,
                y=curves_data[nutrient],
                name=nutrient,
                line=dict(width=3)
            ))
        
        # Add current pH line
        fig_ph.add_vline(x=ph, line_dash="dash", line_color="red", 
                         annotation_text=f"Your pH: {ph}")
        
        fig_ph.update_layout(
            title="Macronutrient Availability vs pH",
            xaxis_title="Soil pH",
            yaxis_title="Relative Availability (%)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_ph, use_container_width=True)
        
        # Micronutrients chart
        fig_micro = go.Figure()
        
        for nutrient in ['Fe', 'Mn', 'Zn', 'Cu', 'B', 'Mo']:
            fig_micro.add_trace(go.Scatter(
                x=ph_range,
                y=curves_data[nutrient],
                name=nutrient,
                line=dict(width=2)
            ))
        
        fig_micro.add_vline(x=ph, line_dash="dash", line_color="red")
        
        fig_micro.update_layout(
            title="Micronutrient Availability vs pH",
            xaxis_title="Soil pH",
            yaxis_title="Relative Availability (%)",
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_micro, use_container_width=True)
    
    with col_ph2:
        st.markdown(f"### 🎯 Availability at pH {ph}")
        
        avail_df = pd.DataFrame({
            'Nutrient': list(availability.keys()),
            'Availability (%)': list(availability.values())
        })
        avail_df = avail_df.sort_values('Availability (%)', ascending=False)
        
        # Color code
        def color_availability(val):
            if val >= 80:
                return '🟢 Excellent'
            elif val >= 60:
                return '🟡 Good'
            elif val >= 40:
                return '🟠 Fair'
            else:
                return '🔴 Poor'
        
        avail_df['Status'] = avail_df['Availability (%)'].apply(color_availability)
        
        st.dataframe(avail_df, use_container_width=True, hide_index=True)
        
        # pH recommendation
        if ph < 6.0:
            st.warning(f"""
            ⚠️ **Acidic Soil (pH {ph})**
            
            **Issues:**
            - Reduced P, Ca, Mg availability
            - Increased Al, Mn toxicity risk
            - Poor microbial activity
            
            **Solution:** Apply lime to raise pH to 6.0-6.5
            """)
        elif ph > 7.5:
            st.warning(f"""
            ⚠️ **Alkaline Soil (pH {ph})**
            
            **Issues:**
            - Reduced Fe, Mn, Zn availability
            - Phosphorus fixation
            - Micronutrient deficiencies
            
            **Solution:** Apply sulfur or acidifying fertilizers
            """)
        else:
            st.success(f"✅ **Optimal pH Range (pH {ph})**\n\nMost nutrients are readily available!")

# TAB 4: LIMITING NUTRIENTS
with tabs[3]:
    st.markdown("## 🔍 Limiting Nutrient Analysis (Liebig's Law)")
    
    st.markdown("""
    <div class='nutrient-card'>
        <h4>📖 Liebig's Law of the Minimum</h4>
        <p>Developed by Carl Sprengel (1828) and popularized by Justus von Liebig (1840), this law states:</p>
        <blockquote>"Plant growth is determined not by total resources available, but by the scarcest resource (limiting factor)."</blockquote>
        <p>Think of it like a barrel with staves of different heights - water (yield) can only rise to the height of the shortest stave (most limiting nutrient).</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Analyze limiting nutrients
    limiting_analysis = SoilFertilityService.identify_limiting_nutrient(soil_data)
    
    if 'error' not in limiting_analysis:
        col_lim1, col_lim2 = st.columns([1, 1])
        
        with col_lim1:
            st.markdown("### 📊 Nutrient Sufficiency Index")
            
            # Create radar chart
            nutrients = list(limiting_analysis['all_sufficiency'].keys())
            sufficiency_values = list(limiting_analysis['all_sufficiency'].values())
            
            fig_radar = go.Figure()
            
            fig_radar.add_trace(go.Scatterpolar(
                r=sufficiency_values,
                theta=nutrients,
                fill='toself',
                name='Current Sufficiency'
            ))
            
            fig_radar.add_trace(go.Scatterpolar(
                r=[100] * len(nutrients),
                theta=nutrients,
                fill='toself',
                name='Optimal (100%)',
                line=dict(dash='dash')
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=True,
                title="Nutrient Balance Radar"
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)
        
        with col_lim2:
            st.markdown("### 🎯 Limiting Factor Identified")
            
            limiting_nutrient = limiting_analysis['limiting_nutrient']
            sufficiency_index = limiting_analysis['sufficiency_index']
            
            st.markdown(f"""
            <div class='warning-card'>
                <h3>⚠️ {limiting_nutrient} is Your Limiting Nutrient</h3>
                <p><strong>Sufficiency Index:</strong> {sufficiency_index}%</p>
                <p>{limiting_analysis['interpretation']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Show all sufficiency levels
            st.markdown("### 📋 All Nutrient Sufficiency Levels")
            
            suff_df = pd.DataFrame({
                'Nutrient': nutrients,
                'Sufficiency (%)': sufficiency_values
            }).sort_values('Sufficiency (%)')
            
            st.dataframe(suff_df, use_container_width=True, hide_index=True)
            
            st.info("""
            **💡 Priority Action:**
            Address the limiting nutrient first for maximum yield improvement. 
            Adding other nutrients won't significantly increase yield until the limiting factor is corrected.
            """)

# TAB 5: FERTILIZER RECOMMENDATIONS
with tabs[4]:
    st.markdown("## 💊 Fertilizer Recommendations")
    
    st.info("💡 **Enter your target yield to get customized fertilizer recommendations**")
    
    col_fert1, col_fert2 = st.columns(2)
    
    with col_fert1:
        target_yield = st.number_input(
            "Target Yield (ton/ha)",
            min_value=1.0,
            max_value=50.0,
            value=5.0,
            step=0.5,
            help="Expected crop yield per hectare"
        )
        
        crop_type = st.selectbox(
            "Crop Type",
            ["General", "Rice", "Corn", "Vegetables", "Fruits"],
            help="Different crops have different nutrient requirements"
        )
    
    with col_fert2:
        farm_area = st.number_input(
            "Farm Area (hectare)",
            min_value=0.1,
            max_value=1000.0,
            value=1.0,
            step=0.1
        )
    
    if st.button("🔄 Calculate Fertilizer Needs", type="primary"):
        recommendations = SoilFertilityService.calculate_fertilizer_recommendation(
            soil_data, target_yield, crop_type.lower()
        )
        
        st.markdown("---")
        st.markdown("### 📊 Nutrient Requirements vs Available")
        
        col_req1, col_req2, col_req3 = st.columns(3)
        
        with col_req1:
            st.metric(
                "Nitrogen (N) Needed",
                f"{recommendations['needed']['N'] * farm_area:.1f} kg",
                delta=f"-{recommendations['available']['N'] * farm_area:.1f} kg available"
            )
        
        with col_req2:
            st.metric(
                "Phosphorus (P2O5) Needed",
                f"{recommendations['needed']['P2O5'] * farm_area:.1f} kg",
                delta=f"-{recommendations['available']['P2O5'] * farm_area:.1f} kg available"
            )
        
        with col_req3:
            st.metric(
                "Potassium (K2O) Needed",
                f"{recommendations['needed']['K2O'] * farm_area:.1f} kg",
                delta=f"-{recommendations['available']['K2O'] * farm_area:.1f} kg available"
            )
        
        st.markdown("---")
        st.markdown("### 🛒 Recommended Fertilizer Products")
        
        for product in recommendations['products']:
            st.markdown(f"""
            <div class='nutrient-card'>
                <h4>📦 {product['product']}</h4>
                <p><strong>Formula:</strong> {product['formula']}</p>
                <p><strong>Amount Needed:</strong> {product['amount_kg'] * farm_area:.1f} kg for {farm_area} ha</p>
                <p><strong>Provides:</strong> {product['provides']}</p>
                {f"<p><em>{product.get('note', '')}</em></p>" if 'note' in product else ""}
            </div>
            """, unsafe_allow_html=True)

# TAB 6: EDUCATIONAL GUIDE
with tabs[5]:
    st.markdown("## 📚 Educational Guide")
    
    with st.expander("🔬 Understanding CEC (Cation Exchange Capacity)"):
        st.markdown("""
        **What is CEC?**
        
        CEC is the soil's ability to hold and exchange positively charged ions (cations) like Ca²⁺, Mg²⁺, K⁺, and NH₄⁺.
        
        **Why it matters:**
        - Higher CEC = Better nutrient retention
        - Lower CEC = More frequent fertilization needed
        - Affects fertilizer efficiency and leaching risk
        
        **Typical CEC values:**
        - Sandy soils: 5-15 meq/100g
        - Loam soils: 10-25 meq/100g
        - Clay soils: 20-40 meq/100g
        - Organic soils: 50-100 meq/100g
        
        **How to improve CEC:**
        - Add organic matter (compost, manure)
        - Increase clay content
        - Maintain optimal pH
        """)
    
    with st.expander("⚖️ Albrecht's Base Saturation Method"):
        st.markdown("""
        **Dr. William Albrecht's Research (1930s-1970s)**
        
        Albrecht discovered that optimal plant growth occurs when soil cations are in specific ratios:
        
        - **Calcium: 65%** - Cell wall structure, root growth
        - **Magnesium: 10%** - Chlorophyll, photosynthesis
        - **Potassium: 5%** - Water regulation, disease resistance
        - **Sodium: 0.5%** - Minor role
        - **Hydrogen: 10%** - Soil acidity reserve
        
        **Key Ratios:**
        - Ca:Mg = 6.5:1 (ideal for most crops)
        - Ca:K = 13:1
        - Mg:K = 2:1
        
        **Benefits of balanced base saturation:**
        - Improved soil structure
        - Better water infiltration
        - Enhanced nutrient uptake
        - Increased disease resistance
        - Higher crop quality
        """)
    
    with st.expander("📈 Troug's pH-Nutrient Availability Diagram"):
        st.markdown("""
        **Dr. Emil Troug (1946)**
        
        Troug's famous diagram shows how soil pH affects nutrient availability:
        
        **Optimal pH ranges:**
        - Most nutrients: pH 6.0-7.0
        - Nitrogen: pH 6.0-8.0 (wide range)
        - Phosphorus: pH 6.0-7.0 (narrow range)
        - Iron, Manganese, Zinc: pH 5.0-6.5 (acidic)
        - Molybdenum: pH 6.5-8.0 (alkaline)
        
        **pH problems:**
        - **Too acidic (< 5.5):** Al and Mn toxicity, reduced P availability
        - **Too alkaline (> 7.5):** Fe, Mn, Zn deficiency, P fixation
        
        **Solutions:**
        - Acidic soil: Apply lime (CaCO₃)
        - Alkaline soil: Apply sulfur or acidifying fertilizers
        """)
    
    with st.expander("🪣 Liebig's Law of the Minimum"):
        st.markdown("""
        **Justus von Liebig (1840)**
        
        "Growth is controlled not by the total amount of resources available, but by the scarcest resource."
        
        **The Barrel Analogy:**
        
        Imagine a barrel made of staves of different heights:
        - Each stave represents a nutrient
        - Water level (yield) can only rise to the shortest stave
        - Adding more of abundant nutrients won't help
        - Only fixing the limiting factor increases yield
        
        **Practical Application:**
        1. Identify the limiting nutrient (lowest sufficiency)
        2. Address that nutrient first
        3. Monitor and adjust other nutrients
        4. Retest soil regularly
        
        **Modern Extension:**
        - Multiple limiting factors can exist
        - Interactions between nutrients matter
        - Environmental factors also limit growth
        """)
    
    with st.expander("🧪 How to Take a Soil Sample"):
        st.markdown("""
        **Proper Soil Sampling Procedure:**
        
        1. **When to sample:**
           - Before planting season
           - Same time each year for consistency
           - Avoid recently fertilized areas
        
        2. **Sampling pattern:**
           - Divide field into uniform areas
           - Take 10-15 sub-samples per area
           - Sample to plow depth (0-20 cm)
        
        3. **Avoid:**
           - Old fertilizer bands
           - Compost piles
           - Near roads or buildings
           - Wet or waterlogged areas
        
        4. **Mix and send:**
           - Combine all sub-samples
           - Mix thoroughly
           - Send 500g to certified lab
           - Label with field ID and date
        
        5. **Frequency:**
           - Annual for intensive crops
           - Every 2-3 years for perennials
           - After major amendments
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌱 <strong>AgriSensa Soil Fertility Calculator</strong></p>
    <p>Based on peer-reviewed research: Albrecht (1975), Troug (1946), Liebig (1840)</p>
    <p>For best results, use certified laboratory soil test data</p>
</div>
""", unsafe_allow_html=True)
