"""
Gold Price Analysis
Real-time gold price tracking and analysis
"""
import streamlit as st
import pandas as pd
import requests
import altair as alt
from datetime import datetime
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.chart_builder import COLOR_SCHEME

# Page configuration
st.set_page_config(
    page_title="Gold Price Analysis",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .gold-metric {
        background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: #2d3748;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        font-weight: 600;
    }
    
    .info-box {
        background: #fff5f5;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #f6d365;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💰 Gold Price Analysis")
st.markdown("**Analisis harga emas real-time dari berbagai mata uang**")

# Fetch gold price data
@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_gold_price():
    """Fetch gold price from multiple API sources with fallback"""
    
    # Try primary API (metals-api.com - free tier)
    try:
        st.info("🔄 Fetching live gold prices from Metals API...")
        # Using metals-api.com free tier
        response = requests.get(
            "https://api.metals.dev/v1/latest?api_key=DEMO&currency=USD&unit=toz",
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            
            # Parse metals-api response
            if 'metals' in data and 'gold' in data['metals']:
                gold_price_usd = data['metals']['gold']
                
                # Get USD/IDR exchange rate (approximate)
                usd_to_idr = 15712  # Approximate rate
                
                # Calculate prices
                oz_usd = gold_price_usd
                gr_usd = gold_price_usd / 31.1035  # 1 oz = 31.1035 grams
                kg_usd = gr_usd * 1000
                
                oz_idr = oz_usd * usd_to_idr
                gr_idr = gr_usd * usd_to_idr
                kg_idr = kg_usd * usd_to_idr
                
                return {
                    "usd": {
                        "oz": f"{oz_usd:,.2f}",
                        "gr": f"{gr_usd:,.2f}",
                        "kg": f"{kg_usd:,.2f}"
                    },
                    "kurs_bi": {
                        "oz": f"{usd_to_idr:,.2f}",
                        "gr": f"{usd_to_idr:,.2f}",
                        "kg": f"{usd_to_idr:,.2f}"
                    },
                    "idr": {
                        "oz": f"{oz_idr:,.0f}",
                        "gr": f"{gr_idr:,.0f}",
                        "kg": f"{kg_idr:,.0f}"
                    },
                    "update_gold_price": datetime.now().strftime("%d %B %Y %H:%M"),
                    "update_kurs_bi": datetime.now().strftime("%d %B %Y %H:%M"),
                    "source": "https://metals.dev (Live Data)"
                }, True
    except Exception as e:
        st.warning(f"⚠️ Primary API unavailable: {str(e)[:80]}")
    
    # Try alternative API (goldapi.io - free tier)
    try:
        st.info("🔄 Trying alternative source (GoldAPI)...")
        response = requests.get(
            "https://www.goldapi.io/api/XAU/USD",
            headers={"x-access-token": "goldapi-demo"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            
            if 'price' in data:
                oz_usd = data['price']
                gr_usd = oz_usd / 31.1035
                kg_usd = gr_usd * 1000
                
                usd_to_idr = 15712
                
                oz_idr = oz_usd * usd_to_idr
                gr_idr = gr_usd * usd_to_idr
                kg_idr = kg_usd * usd_to_idr
                
                return {
                    "usd": {
                        "oz": f"{oz_usd:,.2f}",
                        "gr": f"{gr_usd:,.2f}",
                        "kg": f"{kg_usd:,.2f}"
                    },
                    "kurs_bi": {
                        "oz": f"{usd_to_idr:,.2f}",
                        "gr": f"{usd_to_idr:,.2f}",
                        "kg": f"{usd_to_idr:,.2f}"
                    },
                    "idr": {
                        "oz": f"{oz_idr:,.0f}",
                        "gr": f"{gr_idr:,.0f}",
                        "kg": f"{kg_idr:,.0f}"
                    },
                    "update_gold_price": datetime.now().strftime("%d %B %Y %H:%M"),
                    "update_kurs_bi": datetime.now().strftime("%d %B %Y %H:%M"),
                    "source": "https://goldapi.io (Live Data)"
                }, True
    except Exception as e:
        st.warning(f"⚠️ Alternative API unavailable: {str(e)[:80]}")
    
    # Fallback to sample data
    st.info("📊 All APIs unavailable - Displaying sample data for demonstration")
    return {
        "usd": {
            "oz": "2,171.35",
            "gr": "69.81",
            "kg": "69,810.52"
        },
        "kurs_bi": {
            "oz": "15,712.00",
            "gr": "505.00",
            "kg": "505,000.00"
        },
        "idr": {
            "oz": "34,116,251",
            "gr": "1,096,863",
            "kg": "1,096,862,947"
        },
        "update_gold_price": "Sample Data - All APIs Unavailable",
        "update_kurs_bi": "Sample Data - All APIs Unavailable",
        "source": "Sample Data (APIs Unavailable)"
    }, False

# Load data
with st.spinner("Fetching latest gold prices..."):
    data, is_live = fetch_gold_price()

if data:
    # Display live/sample indicator
    if is_live:
        st.success("🟢 **Live Data** - Real-time prices from API")
    else:
        st.info("📊 **Sample Data** - API temporarily unavailable, showing example data")
    
    # Parse data
    usd_data = data.get('usd', {})
    kurs_bi_data = data.get('kurs_bi', {})
    idr_data = data.get('idr', {})
    update_gold = data.get('update_gold_price', 'N/A')
    update_kurs = data.get('update_kurs_bi', 'N/A')
    source = data.get('source', 'N/A')
    
    # Display update info
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"🕐 **Gold Price Updated:** {update_gold}")
    with col2:
        st.info(f"🕐 **Kurs BI Updated:** {update_kurs}")
    
    st.markdown("---")
    
    # Key Metrics Dashboard
    st.markdown("## 📊 Current Gold Prices")
    
    # USD Prices
    st.markdown("### 💵 USD Prices")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Ounce (oz)</div>
            <div class="metric-value">${usd_data.get('oz', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Gram (gr)</div>
            <div class="metric-value">${usd_data.get('gr', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Kilogram (kg)</div>
            <div class="metric-value">${usd_data.get('kg', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # IDR Prices
    st.markdown("### 🇮🇩 IDR Prices")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Ounce (oz)</div>
            <div class="metric-value">Rp {idr_data.get('oz', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Gram (gr)</div>
            <div class="metric-value">Rp {idr_data.get('gr', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Kilogram (kg)</div>
            <div class="metric-value">Rp {idr_data.get('kg', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Kurs BI
    st.markdown("### 🏦 Kurs BI")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Ounce (oz)</div>
            <div class="metric-value">{kurs_bi_data.get('oz', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Gram (gr)</div>
            <div class="metric-value">{kurs_bi_data.get('gr', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="gold-metric">
            <div class="metric-label">Per Kilogram (kg)</div>
            <div class="metric-value">{kurs_bi_data.get('kg', 'N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Price Comparison
    st.markdown("## 📈 Price Comparison")
    
    # Create comparison dataframe
    comparison_data = []
    
    # Parse numeric values (remove commas and parentheses)
    def parse_price(price_str):
        if not price_str or price_str == 'N/A':
            return 0
        # Remove everything except digits, dots, and minus
        cleaned = ''.join(c for c in price_str.split('(')[0] if c.isdigit() or c in '.,')
        cleaned = cleaned.replace(',', '').replace('.', '')
        try:
            return float(cleaned) / 100  # Adjust for decimal
        except:
            return 0
    
    units = ['oz', 'gr', 'kg']
    unit_labels = ['Per Ounce', 'Per Gram', 'Per Kilogram']
    
    for unit, label in zip(units, unit_labels):
        comparison_data.append({
            'Unit': label,
            'USD': parse_price(usd_data.get(unit, '0')),
            'Currency': 'USD'
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    
    if len(comparison_df) > 0 and comparison_df['USD'].sum() > 0:
        # Bar chart
        chart = alt.Chart(comparison_df).mark_bar().encode(
            x=alt.X('Unit:N', title='Unit'),
            y=alt.Y('USD:Q', title='Price (USD)'),
            color=alt.value(COLOR_SCHEME['warning']),
            tooltip=['Unit', 'USD']
        ).properties(
            width=700,
            height=400,
            title='Gold Price Comparison by Unit (USD)'
        )
        
        st.altair_chart(chart, use_container_width=True)
    
    # Investment Calculator
    st.markdown("---")
    st.markdown("## 🧮 Investment Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        investment_amount = st.number_input(
            "Investment Amount (USD)",
            min_value=0.0,
            max_value=1000000.0,
            value=1000.0,
            step=100.0
        )
        
        unit_type = st.selectbox(
            "Purchase Unit",
            ["Gram", "Ounce", "Kilogram"]
        )
    
    with col2:
        # Calculate how much gold can be bought
        if unit_type == "Gram":
            price_per_unit = parse_price(usd_data.get('gr', '0'))
            unit_symbol = "gr"
        elif unit_type == "Ounce":
            price_per_unit = parse_price(usd_data.get('oz', '0'))
            unit_symbol = "oz"
        else:
            price_per_unit = parse_price(usd_data.get('kg', '0'))
            unit_symbol = "kg"
        
        if price_per_unit > 0:
            gold_amount = investment_amount / price_per_unit
            
            st.markdown(f"""
            <div class="info-box">
                <h3>💰 Investment Summary</h3>
                <p><strong>Investment:</strong> ${investment_amount:,.2f} USD</p>
                <p><strong>Gold Amount:</strong> {gold_amount:,.4f} {unit_symbol}</p>
                <p><strong>Price per {unit_type}:</strong> ${price_per_unit:,.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Price data not available for calculation")
    
    # Data source
    st.markdown("---")
    st.markdown(f"**📊 Data Source:** [{source}]({source})")
    
    # Refresh button
    if st.button("🔄 Refresh Prices"):
        st.cache_data.clear()
        st.rerun()

else:
    st.error("❌ Failed to load gold price data. Please try again later.")
    st.info("💡 Make sure you have internet connection and the API is accessible.")
