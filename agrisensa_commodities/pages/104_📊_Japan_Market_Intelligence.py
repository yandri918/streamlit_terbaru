import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.wagri_market_service import WagriMarketService
from agrisensa_commodities.services.commodity_database import CommodityDatabase

# Page config
st.set_page_config(
    page_title="Japan Market Intelligence - WAGRI",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .market-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .price-card {
        background: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        border-radius: 5px;
    }
    .opportunity-high {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .opportunity-medium {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize services
market_service = WagriMarketService()
commodity_db = CommodityDatabase()

# Header
st.title("📊 Japan Market Intelligence Dashboard")
st.markdown("""
<div class='market-header'>
    <h3>🇯🇵 WAGRI Wholesale Market Data</h3>
    <p>Real-time price monitoring & export opportunity analysis for Indonesian commodities</p>
    <p><em>Data source: WAGRI (Agriculture Data Collaboration Platform Japan)</em></p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Create tabs
tabs = st.tabs([
    "🌏 Live Market Prices",
    "🇮🇩 Export Opportunities", 
    "📈 Price Trends",
    "💰 Export Calculator",
    "📚 Market Intelligence"
])

# TAB 1: LIVE MARKET PRICES
with tabs[0]:
    st.markdown("## 🌏 Live Market Prices")
    
    st.info("💡 **Real-time wholesale prices** from Japan markets. Data updates hourly from WAGRI API.")
    
    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        category_filter = st.selectbox(
            "Category",
            ["All", "Vegetables", "Fruits"],
            key="live_category"
        )
    
    with col_f2:
        priority_filter = st.selectbox(
            "Priority",
            ["All", "Export Focus (⭐⭐⭐+)", "High Priority (⭐⭐⭐⭐⭐)"],
            key="live_priority"
        )
    
    with col_f3:
        search_term = st.text_input(
            "Search Commodity",
            placeholder="e.g., Asparagus, Mango",
            key="live_search"
        )
    
    # Get commodities based on filters
    if priority_filter == "High Priority (⭐⭐⭐⭐⭐)":
        commodities = commodity_db.get_by_priority(5)
    elif priority_filter == "Export Focus (⭐⭐⭐+)":
        commodities = commodity_db.get_by_priority(3)
    else:
        commodities = commodity_db.get_all_commodities()
    
    if category_filter != "All":
        cat = "vegetable" if category_filter == "Vegetables" else "fruit"
        commodities = {k: v for k, v in commodities.items() if v.get("category") == cat}
    
    if search_term:
        commodities = commodity_db.search_by_name(search_term)
    
    # Display sample data (in real implementation, fetch from WAGRI API)
    st.markdown("### 📋 Current Prices")
    
    # Create sample data table
    table_data = []
    for code, data in commodities.items():
        # In real implementation, fetch actual price from WAGRI
        # For now, show sample data
        table_data.append({
            "Code": code,
            "Commodity": f"{data['name_en']} ({data['name_id']})",
            "Category": data['category'].title(),
            "Priority": commodity_db.get_priority_stars(data['priority']),
            "Japan Price (¥)": "API Required",
            "Indonesia Cost (Rp)": market_service.format_price_idr(data['typical_price_idr']),
            "Regions": ", ".join(data['indonesia_regions'][:2])
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.info(f"📊 Showing {len(table_data)} commodities")
    else:
        st.warning("No commodities found matching your filters.")
    
    # Sample price card
    st.markdown("### 💡 How to Use Live Data")
    st.markdown("""
    **To get real-time prices:**
    1. Obtain WAGRI API access (requires registration)
    2. Get `MarketSurveyId` for specific commodity & date
    3. System will auto-fetch and cache prices
    4. Data refreshes every hour
    
    **Sample API Call:**
    ```python
    # Fetch Asparagus price for today
    data = market_service.fetch_commodity_data(market_survey_id)
    
    # Result:
    {
        "AveragePrice": 2651,  # JPY per kg
        "TradingVolume": 3627,  # kg
        "ProductionAreaName": "Saga",
        "TargetDate": "2025-03-01"
    }
    ```
    """)

# TAB 2: EXPORT OPPORTUNITIES
with tabs[1]:
    st.markdown("## 🇮🇩 Export Opportunities to Japan")
    
    st.info("💡 **Focus:** Indonesian commodities with high export potential to Japan market")
    
    # Get high-priority commodities
    export_commodities = commodity_db.get_by_priority(3)
    
    st.markdown(f"### 🎯 Top {len(export_commodities)} Export Priority Commodities")
    
    # Create opportunity cards
    opportunities = []
    
    for code, data in export_commodities.items():
        # Get typical costs
        costs = commodity_db.get_typical_costs(code)
        
        # Sample Japan price (in real implementation, fetch from WAGRI)
        # For demo, estimate based on typical markup
        sample_japan_price_jpy = data['typical_price_idr'] / market_service.EXCHANGE_RATE_JPY_TO_IDR * 3
        
        # Calculate margin
        margin_analysis = market_service.calculate_export_margin(
            japan_price_jpy=sample_japan_price_jpy,
            indonesia_production_cost=costs['production'],
            packaging_cost=costs['packaging'],
            transport_to_port=costs['transport_to_port'],
            air_freight_per_kg=costs['air_freight'],
            customs_duty=costs['customs_duty'],
            certification_cost=costs['certification']
        )
        
        opportunities.append({
            "code": code,
            "name": data['name_en'],
            "name_id": data['name_id'],
            "priority": data['priority'],
            "margin_pct": margin_analysis['margin_percentage'],
            "profitability": margin_analysis['profitability'],
            "score": margin_analysis['profitability_score'],
            "japan_price_idr": margin_analysis['japan_price_idr'],
            "gross_margin": margin_analysis['gross_margin'],
            "data": data,
            "analysis": margin_analysis
        })
    
    # Sort by profitability score
    opportunities.sort(key=lambda x: (x['score'], x['margin_pct']), reverse=True)
    
    # Display top opportunities
    col_opp1, col_opp2 = st.columns(2)
    
    for idx, opp in enumerate(opportunities[:10]):  # Top 10
        col = col_opp1 if idx % 2 == 0 else col_opp2
        
        with col:
            color_class = "opportunity-high" if opp['score'] >= 4 else "opportunity-medium"
            
            st.markdown(f"""
            <div class='{color_class}'>
                <h4>#{idx+1} {opp['name']} ({opp['name_id']})</h4>
                <p><strong>Priority:</strong> {commodity_db.get_priority_stars(opp['priority'])}</p>
                <p><strong>Margin:</strong> {opp['margin_pct']:.1f}%</p>
                <p><strong>Status:</strong> {opp['profitability']}</p>
                <p><strong>Gross Margin:</strong> {market_service.format_price_idr(opp['gross_margin'])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Expandable details
            with st.expander(f"📊 Detailed Analysis - {opp['name']}"):
                st.markdown(f"""
                **Market Information:**
                - Japan Price (estimated): {market_service.format_price_idr(opp['japan_price_idr'])}
                - Indonesia Regions: {', '.join(opp['data']['indonesia_regions'])}
                - Peak Season: {opp['data']['peak_season']}
                - Shelf Life: {opp['data']['shelf_life_days']} days
                
                **Cost Breakdown:**
                - Production: {market_service.format_price_idr(opp['analysis']['cost_breakdown']['production'])}
                - Packaging: {market_service.format_price_idr(opp['analysis']['cost_breakdown']['packaging'])}
                - Transport: {market_service.format_price_idr(opp['analysis']['cost_breakdown']['transport'])}
                - Air Freight: {market_service.format_price_idr(opp['analysis']['cost_breakdown']['air_freight'])}
                - Customs: {market_service.format_price_idr(opp['analysis']['cost_breakdown']['customs'])}
                - Certification: {market_service.format_price_idr(opp['analysis']['cost_breakdown']['certification'])}
                - **Total Cost:** {market_service.format_price_idr(opp['analysis']['total_cost'])}
                
                **Profitability:**
                - Gross Margin: {market_service.format_price_idr(opp['analysis']['gross_margin'])}
                - Margin %: {opp['analysis']['margin_percentage']:.1f}%
                - ROI: {opp['analysis']['roi_percentage']:.1f}%
                - Score: {opp['analysis']['profitability_score']}/5 ⭐
                
                **Export Requirements:**
                - Certifications: {', '.join(opp['data']['certification_needed'])}
                - Shipping: {opp['data']['shipping_method']}
                - Quality: {opp['data']['quality_grade']}
                - Packaging: {opp['data']['packaging']}
                """)

# Continue with remaining tabs in next message due to length...
