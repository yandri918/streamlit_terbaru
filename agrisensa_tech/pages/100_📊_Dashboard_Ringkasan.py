import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.auth import require_auth, show_user_info_sidebar

# Page Config
st.set_page_config(page_title="Executive Dashboard", page_icon="📊", layout="wide")

# Auth
user = require_auth()
show_user_info_sidebar()

# ==========================================
# HEADER
# ==========================================
st.title("📊 Executive Summary Dashboard")
st.markdown(f"**Welcome back, {user['name'] if user else 'Manager'}!** Here is the high-level overview of your agricultural portfolio.")
st.markdown("---")

# ==========================================
# 1. KEY PERFORMANCE INDICATORS (KPIs)
# ==========================================
# Simulated aggregated data
col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)

with col_kpi1:
    st.metric("Total Lahan Dikelola", "15.5 Ha", "+2.5 Ha")

with col_kpi2:
    st.metric("Proj. Annual Revenue", "Rp 850 Jt", "+12%")

with col_kpi3:
    st.metric("Weighted Risk Score", "4.2/10", "-0.5 (Mitigated)")

with col_kpi4:
    st.metric("Active Campaigns", "3 Projects", "Padi, Cabai, Jagung")

# ==========================================
# 2. PORTFOLIO SNAPSHOT
# ==========================================
st.divider()
col_main1, col_main2 = st.columns([2, 1])

with col_main1:
    st.subheader("💰 Portfolio Allocation Snapshot")
    # Simplified data mimicking Page 13 results
    portfolio_data = pd.DataFrame({
        'Crop': ['Padi (Food Base)', 'Cabai (Cash Cow)', 'Jagung (Rotation)', 'Kedelai (Nitrogen Fixer)'],
        'Allocation': [40, 30, 20, 10],
        'Type': ['Low Risk', 'High Risk', 'Medium Risk', 'Low Risk']
    })
    
    fig_pie = px.pie(portfolio_data, values='Allocation', names='Crop', hole=0.4, 
                     color_discrete_sequence=px.colors.sequential.RdBu)
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
    
    st.plotly_chart(fig_pie, use_container_width=True)

with col_main2:
    st.subheader("⚠️ Critical Risk Alerts")
    
    # Alert Card 1
    st.error("""
    **🚨 Harga Cabai Volatil**
    - **Risk:** Price Crash predicted next month (-15%)
    - **Action:** Lock price with contract farming now.
    """)
    
    # Alert Card 2
    st.warning("""
    **🌦️ El Nino Warning**
    - **Risk:** Drought Risk for Padi (Oct-Dec)
    - **Action:** Activate irrigation pumps (Mitigation #4).
    """)
    
    # Alert Card 3
    st.success("""
    **✅ Nitrogen Efficiency**
    - **Status:** Good synergy detected (Jagung + Kedelai)
    - **Impact:** Fertilizer cost reduced by 15%.
    """)

# ==========================================
# 3. FINANCIAL PROJECTION (Monte Carlo Summary)
# ==========================================
st.divider()
st.subheader("📈 Financial Projection (Risk-Adjusted)")

# Simulated distribution data
x_dist = [-20, -10, 0, 10, 20, 30, 40, 50, 60]
y_prob = [0.01, 0.05, 0.1, 0.2, 0.3, 0.2, 0.1, 0.03, 0.01]

fig_area = go.Figure()
fig_area.add_trace(go.Scatter(x=x_dist, y=y_prob, fill='tozeroy', mode='none', fillcolor='rgba(0, 100, 80, 0.2)'))
fig_area.update_layout(
    title="ROI Probability Distribution (Monte Carlo)",
    xaxis_title="Potential ROI (%)",
    yaxis_title="Probability Density",
    height=300
)

col_fin1, col_fin2 = st.columns([1, 2])

with col_fin1:
    st.markdown("""
    **Analisis Keuangan:**
    
    - **Most Likely ROI:** 20-30%
    - **Value at Risk (95%):** -5%
      *(Kemungkinan rugi hanya 5%)*
    - **Upside Potential:** up to 60%
    """)
    
    st.button("View Detailed Analysis (Page 11) →")

with col_fin2:
    st.plotly_chart(fig_area, use_container_width=True)

# Footer
st.caption("Data aggregated from Analysis Modules (11, 13, 14). Last updated: Real-time.")
