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

from agrisensa_commodities.services.soil_texture_service import SoilTextureService

# Page config
st.set_page_config(
    page_title="Soil Texture & Structure",
    page_icon="🏔️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .texture-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .property-card {
        background: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
        border-radius: 5px;
    }
    .warning-box {
        background: #fff3cd;
        padding: 15px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏔️ Soil Texture & Structure Calculator")
st.markdown("""
<div class='texture-card'>
    <h3>📐 USDA Soil Texture Triangle & Physical Properties</h3>
    <p>Comprehensive analysis of soil physical properties:</p>
    <ul>
        <li>✅ <strong>USDA Texture Triangle</strong> - Interactive classification</li>
        <li>✅ <strong>Bulk Density & Porosity</strong> - Compaction analysis</li>
        <li>✅ <strong>Water Holding Capacity</strong> - Saxton & Rawls equations</li>
        <li>✅ <strong>Infiltration Rate</strong> - Drainage assessment</li>
    </ul>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Create tabs
tabs = st.tabs([
    "📐 Texture Triangle",
    "⚖️ Bulk Density",
    "💧 Water Holding Capacity",
    "🌊 Infiltration Rate",
    "📚 Educational Guide"
])

# TAB 1: TEXTURE TRIANGLE
with tabs[0]:
    st.markdown("## 📐 USDA Soil Texture Triangle")
    
    st.markdown("""
    <div class='property-card'>
        <h4>📖 What is Soil Texture?</h4>
        <p>Soil texture refers to the relative proportions of <strong>sand</strong>, <strong>silt</strong>, and <strong>clay</strong> particles:</p>
        <ul>
            <li><strong>Sand:</strong> 0.05-2.0 mm (gritty, drains fast)</li>
            <li><strong>Silt:</strong> 0.002-0.05 mm (smooth, holds water)</li>
            <li><strong>Clay:</strong> <0.002 mm (sticky, holds nutrients)</li>
        </ul>
        <p>The USDA Texture Triangle classifies soil into 12 texture classes based on these percentages.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_input, col_triangle = st.columns([1, 2])
    
    with col_input:
        st.markdown("### 🔢 Enter Particle Size Distribution")
        
        st.info("💡 **Tip:** Get a lab analysis for accurate results, or estimate using the 'feel method'")
        
        sand = st.slider(
            "🟤 Sand (%)",
            min_value=0,
            max_value=100,
            value=40,
            step=1,
            help="Coarse particles (0.05-2.0 mm)"
        )
        
        silt = st.slider(
            "🟡 Silt (%)",
            min_value=0,
            max_value=100,
            value=40,
            step=1,
            help="Medium particles (0.002-0.05 mm)"
        )
        
        clay = st.slider(
            "🔴 Clay (%)",
            min_value=0,
            max_value=100,
            value=20,
            step=1,
            help="Fine particles (<0.002 mm)"
        )
        
        total = sand + silt + clay
        
        if total != 100:
            st.warning(f"⚠️ Total must equal 100% (current: {total}%)")
            # Auto-adjust
            if st.button("🔄 Auto-Adjust to 100%"):
                factor = 100 / total
                sand = int(sand * factor)
                silt = int(silt * factor)
                clay = 100 - sand - silt
                st.rerun()
        else:
            st.success(f"✅ Total: {total}%")
            
            # Classify texture
            texture_result = SoilTextureService.classify_texture(sand, silt, clay)
            
            if 'error' not in texture_result:
                st.markdown(f"""
                <div class='texture-card'>
                    <h3>🎯 Your Soil Texture Class</h3>
                    <h2>{texture_result['class']}</h2>
                    <p>{texture_result['properties']['description']}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Properties
                st.markdown("### 📋 Texture Properties")
                
                props = texture_result['properties']
                
                st.markdown(f"""
                **Best Crops:** {props.get('crops', 'N/A')}
                
                **Management Tips:** {props.get('management', 'N/A')}
                """)
    
    with col_triangle:
        st.markdown("### 🔺 Interactive USDA Texture Triangle")
        
        if total == 100:
            # Create ternary plot
            fig = go.Figure()
            
            # Add texture class boundaries (simplified)
            # In production, you'd add all 12 class boundaries
            
            # Add user's point
            fig.add_trace(go.Scatterternary(
                a=[sand],
                b=[clay],
                c=[silt],
                mode='markers+text',
                marker=dict(
                    size=20,
                    color='red',
                    symbol='star',
                    line=dict(color='white', width=2)
                ),
                text=[texture_result['class']],
                textposition='top center',
                textfont=dict(size=14, color='red', family='Arial Black'),
                name='Your Soil',
                hovertemplate='<b>%{text}</b><br>' +
                             'Sand: %{a}%<br>' +
                             'Clay: %{b}%<br>' +
                             'Silt: %{c}%<br>' +
                             '<extra></extra>'
            ))
            
            # Add reference points for common textures
            reference_textures = {
                'Sand': (90, 5, 5),
                'Loam': (40, 20, 40),
                'Clay': (20, 60, 20),
                'Silt Loam': (20, 15, 65),
                'Sandy Loam': (65, 10, 25),
                'Clay Loam': (32, 34, 34)
            }
            
            ref_sand, ref_clay, ref_silt = [], [], []
            ref_names = []
            
            for name, (s, c, si) in reference_textures.items():
                ref_sand.append(s)
                ref_clay.append(c)
                ref_silt.append(si)
                ref_names.append(name)
            
            fig.add_trace(go.Scatterternary(
                a=ref_sand,
                b=ref_clay,
                c=ref_silt,
                mode='markers+text',
                marker=dict(
                    size=8,
                    color='lightblue',
                    symbol='circle',
                    line=dict(color='darkblue', width=1)
                ),
                text=ref_names,
                textposition='bottom center',
                textfont=dict(size=9, color='darkblue'),
                name='Reference Textures',
                hovertemplate='<b>%{text}</b><br>' +
                             'Sand: %{a}%<br>' +
                             'Clay: %{b}%<br>' +
                             'Silt: %{c}%<br>' +
                             '<extra></extra>'
            ))
            
            fig.update_layout(
                title={
                    'text': 'USDA Soil Texture Triangle',
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 20, 'color': '#333', 'family': 'Arial Black'}
                },
                ternary=dict(
                    sum=100,
                    aaxis=dict(title='Sand (%)', min=0, linewidth=2, ticks='outside'),
                    baxis=dict(title='Clay (%)', min=0, linewidth=2, ticks='outside'),
                    caxis=dict(title='Silt (%)', min=0, linewidth=2, ticks='outside'),
                    bgcolor='#f0f0f0'
                ),
                showlegend=True,
                height=600,
                paper_bgcolor='white',
                plot_bgcolor='white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.info("""
            💡 **How to read the triangle:**
            - Each corner represents 100% of that particle size
            - Your red star shows your soil's position
            - Blue dots show common texture classes
            - Hover over points for details
            """)

# TAB 2: BULK DENSITY
with tabs[1]:
    st.markdown("## ⚖️ Bulk Density & Porosity Analysis")
    
    st.markdown("""
    <div class='property-card'>
        <h4>📖 What is Bulk Density?</h4>
        <p><strong>Bulk Density (BD)</strong> is the mass of dry soil per unit volume, including pore spaces.</p>
        <p><strong>Formula:</strong> BD = Dry Soil Mass / Total Volume (g/cm³)</p>
        <p><strong>Why it matters:</strong></p>
        <ul>
            <li>Indicates soil compaction</li>
            <li>Affects root penetration</li>
            <li>Influences water infiltration</li>
            <li>Determines aeration</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col_bd1, col_bd2 = st.columns(2)
    
    with col_bd1:
        st.markdown("### 📊 Enter Bulk Density")
        
        bulk_density = st.number_input(
            "Bulk Density (g/cm³)",
            min_value=0.5,
            max_value=2.5,
            value=1.4,
            step=0.05,
            help="Typical range: 1.0-1.8 g/cm³"
        )
        
        particle_density = st.number_input(
            "Particle Density (g/cm³)",
            min_value=2.0,
            max_value=3.0,
            value=2.65,
            step=0.05,
            help="Default 2.65 for mineral soils"
        )
        
        # Calculate properties
        bd_props = SoilTextureService.calculate_bulk_density_properties(bulk_density, particle_density)
        
        st.markdown("---")
        
        # Display results
        col_metric1, col_metric2 = st.columns(2)
        
        with col_metric1:
            st.metric(
                "Total Porosity",
                f"{bd_props['total_porosity']}%",
                help="Percentage of soil volume that is pore space"
            )
        
        with col_metric2:
            status_colors = {
                'excellent': '🟢',
                'good': '🟡',
                'moderate': '🟠',
                'poor': '🔴',
                'critical': '🔴'
            }
            color = status_colors.get(bd_props['status_level'], '⚪')
            
            st.metric(
                "Compaction Status",
                f"{color} {bd_props['compaction_status']}"
            )
        
        st.markdown(f"""
        <div class='property-card'>
            <h4>📋 Interpretation</h4>
            <p>{bd_props['interpretation']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_bd2:
        st.markdown("### 📊 Bulk Density Ranges by Texture")
        
        # Create comparison chart
        texture_types = ['Sandy', 'Loamy', 'Clayey']
        ideal_min = [1.4, 1.1, 1.0]
        ideal_max = [1.6, 1.4, 1.3]
        
        fig_bd = go.Figure()
        
        # Add ideal ranges
        for i, texture in enumerate(texture_types):
            fig_bd.add_trace(go.Bar(
                name=texture,
                x=[texture],
                y=[ideal_max[i]],
                marker_color=['#F4A460', '#8B4513', '#654321'][i],
                text=[f"{ideal_min[i]}-{ideal_max[i]}"],
                textposition='inside',
                hovertemplate=f'<b>{texture} Soils</b><br>' +
                             f'Ideal Range: {ideal_min[i]}-{ideal_max[i]} g/cm³<br>' +
                             '<extra></extra>'
            ))
        
        # Add user's value line
        fig_bd.add_hline(
            y=bulk_density,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Your BD: {bulk_density} g/cm³",
            annotation_position="right"
        )
        
        fig_bd.update_layout(
            title="Ideal Bulk Density Ranges",
            yaxis_title="Bulk Density (g/cm³)",
            showlegend=False,
            height=400
        )
        
        st.plotly_chart(fig_bd, use_container_width=True)
        
        # Porosity visualization
        st.markdown("### 🕳️ Porosity Visualization")
        
        # Create gauge chart for porosity
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=bd_props['total_porosity'],
            title={'text': "Total Porosity (%)"},
            delta={'reference': 50, 'suffix': '% vs ideal'},
            gauge={
                'axis': {'range': [None, 70]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 30], 'color': "lightgray"},
                    {'range': [30, 50], 'color': "yellow"},
                    {'range': [50, 70], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 40
                }
            }
        ))
        
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)

# TAB 3: WATER HOLDING CAPACITY
with tabs[2]:
    st.markdown("## 💧 Water Holding Capacity (Saxton & Rawls Method)")
    
    st.markdown("""
    <div class='property-card'>
        <h4>📖 Water Holding Capacity</h4>
        <p>The amount of water soil can hold for plant use, measured between:</p>
        <ul>
            <li><strong>Field Capacity (FC):</strong> Water held after drainage (-33 kPa)</li>
            <li><strong>Wilting Point (WP):</strong> Water unavailable to plants (-1500 kPa)</li>
            <li><strong>Available Water Capacity (AWC):</strong> FC - WP</li>
        </ul>
        <p>Based on <strong>Saxton & Rawls (2006)</strong> soil water characteristic equations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col_whc1, col_whc2 = st.columns([1, 1])
    
    with col_whc1:
        st.markdown("### 🔢 Input Parameters")
        
        # Use texture from Tab 1 or allow manual input
        use_texture_tab1 = st.checkbox("Use texture from Tab 1", value=True)
        
        if use_texture_tab1 and total == 100:
            whc_sand = sand
            whc_clay = clay
            st.info(f"Using: Sand {sand}%, Clay {clay}%")
        else:
            whc_sand = st.slider("Sand (%)", 0, 100, 40)
            whc_clay = st.slider("Clay (%)", 0, 100, 20)
        
        organic_matter = st.slider(
            "Organic Matter (%)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.5,
            help="Typical range: 1-5% for mineral soils"
        )
        
        # Calculate WHC
        whc_result = SoilTextureService.calculate_water_holding_capacity(
            whc_sand, whc_clay, organic_matter
        )
        
        st.markdown("---")
        st.markdown("### 📊 Results")
        
        col_whc_m1, col_whc_m2, col_whc_m3 = st.columns(3)
        
        with col_whc_m1:
            st.metric(
                "Field Capacity",
                f"{whc_result['field_capacity']} mm/m",
                help="Water held after drainage"
            )
        
        with col_whc_m2:
            st.metric(
                "Wilting Point",
                f"{whc_result['wilting_point']} mm/m",
                help="Water unavailable to plants"
            )
        
        with col_whc_m3:
            st.metric(
                "Available Water",
                f"{whc_result['available_water_capacity']} mm/m",
                help="Plant-available water"
            )
        
        st.markdown(f"""
        <div class='property-card'>
            <h4>💧 {whc_result['awc_classification']}</h4>
            <p>{whc_result['interpretation']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_whc2:
        st.markdown("### 📊 Water Retention Visualization")
        
        # Create water retention bar chart
        fig_whc = go.Figure()
        
        fig_whc.add_trace(go.Bar(
            name='Field Capacity',
            x=['Water Content'],
            y=[whc_result['field_capacity']],
            marker_color='#4ecdc4',
            text=[f"{whc_result['field_capacity']:.0f} mm/m"],
            textposition='inside'
        ))
        
        fig_whc.add_trace(go.Bar(
            name='Wilting Point',
            x=['Water Content'],
            y=[whc_result['wilting_point']],
            marker_color='#ff6b6b',
            text=[f"{whc_result['wilting_point']:.0f} mm/m"],
            textposition='inside'
        ))
        
        fig_whc.add_trace(go.Bar(
            name='Available Water',
            x=['Water Content'],
            y=[whc_result['available_water_capacity']],
            marker_color='#95e1d3',
            text=[f"{whc_result['available_water_capacity']:.0f} mm/m"],
            textposition='inside'
        ))
        
        fig_whc.update_layout(
            title="Water Holding Capacity Components",
            yaxis_title="Water Content (mm/m)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig_whc, use_container_width=True)
        
        # Irrigation scheduling helper
        st.markdown("### 💦 Irrigation Scheduling Helper")
        
        root_depth = st.slider(
            "Root Depth (m)",
            min_value=0.1,
            max_value=2.0,
            value=0.5,
            step=0.1
        )
        
        total_awc = whc_result['available_water_capacity'] * root_depth
        
        st.info(f"""
        **Total Available Water in Root Zone:** {total_awc:.0f} mm
        
        **Irrigation Trigger (50% depletion):** {total_awc * 0.5:.0f} mm
        
        **Irrigation Amount:** {total_awc * 0.7:.0f} mm (to refill to 70% capacity)
        """)

# TAB 4: INFILTRATION RATE
with tabs[3]:
    st.markdown("## 🌊 Infiltration Rate & Drainage")
    
    st.markdown("""
    <div class='property-card'>
        <h4>📖 What is Infiltration Rate?</h4>
        <p><strong>Infiltration rate</strong> is the speed at which water enters the soil surface.</p>
        <p><strong>Why it matters:</strong></p>
        <ul>
            <li>Determines runoff and erosion risk</li>
            <li>Affects irrigation efficiency</li>
            <li>Influences drainage needs</li>
            <li>Impacts crop selection</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    col_inf1, col_inf2 = st.columns([1, 1])
    
    with col_inf1:
        st.markdown("### 🔢 Input Parameters")
        
        # Use texture from Tab 1
        if total == 100:
            inf_texture = texture_result['class']
            st.info(f"Using texture class: **{inf_texture}**")
        else:
            inf_texture = st.selectbox(
                "Select Texture Class",
                list(SoilTextureService.TEXTURE_CLASSES.keys())
            )
        
        soil_structure = st.select_slider(
            "Soil Structure Quality",
            options=['Poor', 'Moderate', 'Good'],
            value='Moderate',
            help="Poor = compacted, Moderate = average, Good = well-aggregated"
        )
        
        # Calculate infiltration
        inf_result = SoilTextureService.estimate_infiltration_rate(
            inf_texture, soil_structure
        )
        
        st.markdown("---")
        
        # Display results
        st.metric(
            "Infiltration Rate",
            f"{inf_result['infiltration_rate']} mm/hr",
            help="Speed of water entry into soil"
        )
        
        st.markdown(f"""
        <div class='property-card'>
            <h4>📊 Classification</h4>
            <p><strong>{inf_result['classification']}</strong></p>
            <p><strong>Runoff Risk:</strong> {inf_result['runoff_risk']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💡 Management Recommendations")
        
        for i, rec in enumerate(inf_result['recommendations'], 1):
            st.markdown(f"{i}. {rec}")
    
    with col_inf2:
        st.markdown("### 📊 Infiltration Rate Comparison")
        
        # Create comparison chart for different textures
        all_textures = list(SoilTextureService.TEXTURE_CLASSES.keys())
        inf_rates = []
        
        for texture in all_textures:
            result = SoilTextureService.estimate_infiltration_rate(texture, 'moderate')
            inf_rates.append(result['infiltration_rate'])
        
        fig_inf = go.Figure(data=[
            go.Bar(
                x=all_textures,
                y=inf_rates,
                marker_color=['#FF6B6B' if t == inf_texture else '#4ECDC4' for t in all_textures],
                text=[f"{r:.1f}" for r in inf_rates],
                textposition='outside'
            )
        ])
        
        fig_inf.update_layout(
            title="Infiltration Rates by Texture Class",
            xaxis_title="Texture Class",
            yaxis_title="Infiltration Rate (mm/hr)",
            xaxis={'tickangle': -45},
            height=500
        )
        
        st.plotly_chart(fig_inf, use_container_width=True)
        
        st.info(f"Your soil ({inf_texture}) is highlighted in red")

# TAB 5: EDUCATIONAL GUIDE
with tabs[4]:
    st.markdown("## 📚 Educational Guide")
    
    with st.expander("📐 Understanding the USDA Texture Triangle"):
        st.markdown("""
        **How to Use the Triangle:**
        
        1. **Find your sand percentage** on the bottom axis
        2. **Follow the line** going up and to the left
        3. **Find your clay percentage** on the left axis
        4. **Follow the line** going across to the right
        5. **Where the lines intersect** is your texture class
        
        **The 12 Texture Classes:**
        
        1. **Sand** - Very coarse, drains rapidly
        2. **Loamy Sand** - Slightly better retention
        3. **Sandy Loam** - Good drainage, moderate retention
        4. **Loam** - IDEAL! Balanced properties
        5. **Silt Loam** - Smooth, good retention
        6. **Silt** - Very smooth, can crust
        7. **Sandy Clay Loam** - Moderate retention
        8. **Clay Loam** - Good nutrients, heavy
        9. **Silty Clay Loam** - High retention, slow drainage
        10. **Sandy Clay** - Difficult to work
        11. **Silty Clay** - Very fine, poor drainage
        12. **Clay** - Excellent nutrients, very heavy
        
        **Why Texture Matters:**
        - Determines water holding capacity
        - Affects nutrient retention
        - Influences workability
        - Determines drainage needs
        - Affects crop suitability
        """)
    
    with st.expander("⚖️ Bulk Density & Compaction"):
        st.markdown("""
        **What Causes Compaction?**
        
        - Heavy machinery traffic
        - Working soil when wet
        - Livestock trampling
        - Natural settling
        - Loss of organic matter
        
        **Effects of Compaction:**
        
        - Reduced root growth
        - Poor water infiltration
        - Decreased aeration
        - Lower crop yields
        - Increased runoff
        
        **How to Prevent Compaction:**
        
        1. Avoid working wet soil
        2. Use controlled traffic patterns
        3. Add organic matter regularly
        4. Use cover crops
        5. Minimize tillage
        
        **How to Fix Compaction:**
        
        1. **Deep tillage/subsoiling** - Break hardpan
        2. **Organic matter** - Improve structure
        3. **Gypsum** - For clay soils
        4. **Deep-rooted crops** - Natural tillage
        5. **Reduce traffic** - Prevent recurrence
        
        **Ideal Bulk Density Ranges:**
        
        - Sandy soils: 1.4-1.6 g/cm³
        - Loamy soils: 1.1-1.4 g/cm³
        - Clay soils: 1.0-1.3 g/cm³
        - Organic soils: 0.5-1.0 g/cm³
        """)
    
    with st.expander("💧 Water Holding Capacity (Saxton & Rawls)"):
        st.markdown("""
        **Saxton & Rawls (2006) Equations:**
        
        These equations predict soil water retention based on:
        - Sand percentage
        - Clay percentage
        - Organic matter content
        
        **Key Concepts:**
        
        **Field Capacity (FC):**
        - Water held after gravity drainage (2-3 days)
        - Soil is "full" but not saturated
        - Optimal for plant growth
        - Measured at -33 kPa tension
        
        **Wilting Point (WP):**
        - Water so tightly held plants can't extract it
        - Plants permanently wilt
        - Measured at -1500 kPa tension
        
        **Available Water Capacity (AWC):**
        - AWC = FC - WP
        - Water actually available to plants
        - Varies by texture:
          - Sand: 50-100 mm/m
          - Loam: 150-200 mm/m
          - Clay: 150-250 mm/m
        
        **Irrigation Management:**
        
        1. **Determine root depth** (e.g., 0.5 m for vegetables)
        2. **Calculate total AWC** (AWC × root depth)
        3. **Set trigger point** (usually 50% depletion)
        4. **Apply irrigation** (refill to 70-80% capacity)
        
        **Example:**
        - Loam soil: AWC = 180 mm/m
        - Root depth: 0.6 m
        - Total AWC: 108 mm
        - Trigger: 54 mm (50% depletion)
        - Irrigation amount: 76 mm (to 70% capacity)
        """)
    
    with st.expander("🌊 Infiltration & Drainage"):
        st.markdown("""
        **Infiltration Rate Factors:**
        
        1. **Texture** - Coarse = fast, fine = slow
        2. **Structure** - Well-aggregated = fast
        3. **Organic matter** - More = faster
        4. **Compaction** - Compacted = slower
        5. **Surface sealing** - Crusting = slower
        
        **Infiltration Rate Classes:**
        
        - **Very Slow:** <1 mm/hr (Clay, compacted)
        - **Slow:** 1-5 mm/hr (Clay loam, silt)
        - **Moderate:** 5-15 mm/hr (Loam, silt loam)
        - **Rapid:** 15-50 mm/hr (Sandy loam)
        - **Very Rapid:** >50 mm/hr (Sand)
        
        **Drainage Problems:**
        
        **Poor Drainage (slow infiltration):**
        - Waterlogging
        - Root diseases
        - Nutrient deficiencies
        - Delayed planting
        
        **Solutions:**
        - Install drainage tiles
        - Use raised beds
        - Add organic matter
        - Improve structure with gypsum
        
        **Excessive Drainage (fast infiltration):**
        - Drought stress
        - Nutrient leaching
        - Frequent irrigation needed
        
        **Solutions:**
        - Add organic matter
        - Use mulch
        - Drip irrigation
        - Drought-tolerant crops
        """)
    
    with st.expander("🧪 How to Determine Your Soil Texture"):
        st.markdown("""
        **Method 1: Laboratory Analysis (Most Accurate)**
        
        1. Send soil sample to certified lab
        2. Request particle size analysis
        3. Receive exact sand-silt-clay percentages
        4. Use this calculator with lab results
        
        **Method 2: Feel Method (Field Estimate)**
        
        1. **Take a handful of moist soil**
        2. **Squeeze it into a ball**
        3. **Try to form a ribbon**
        
        **Interpretation:**
        
        - **Won't form ball:** Sand
        - **Forms ball, no ribbon:** Loamy sand
        - **Forms ball, ribbon <2.5 cm:** Sandy loam or loam
        - **Ribbon 2.5-5 cm, gritty:** Sandy clay loam
        - **Ribbon 2.5-5 cm, smooth:** Silt loam
        - **Ribbon >5 cm, gritty:** Sandy clay
        - **Ribbon >5 cm, smooth:** Silty clay or clay
        
        **Method 3: Jar Test (Home Method)**
        
        1. Fill jar 1/3 with soil
        2. Add water to 2/3 full
        3. Add 1 tsp dish soap
        4. Shake vigorously for 5 minutes
        5. Let settle for 24 hours
        
        **Reading the Jar:**
        - Bottom layer (settles in 1 min): Sand
        - Middle layer (settles in 2 hrs): Silt
        - Top layer (settles in 24 hrs): Clay
        - Measure each layer, calculate percentages
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏔️ <strong>AgriSensa Soil Texture & Structure Calculator</strong></p>
    <p>Based on USDA Soil Texture Triangle & Saxton-Rawls (2006) equations</p>
    <p>For best results, use laboratory particle size analysis</p>
</div>
""", unsafe_allow_html=True)
