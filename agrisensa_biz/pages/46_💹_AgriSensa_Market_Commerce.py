import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Page Configuration
st.set_page_config(
    page_title="Market Intelligence & Commerce - AgriSensa",
    page_icon="💹",
    layout="wide"
)

# HELPER: Generate Dummy Orders
def generate_orders():
    # Simulate "Omnichannel" data
    channels = ["WhatsApp (Manual)", "Tokopedia", "Shopee", "Pasar Induk Contract", "TikTok Shop"]
    statuses = ["New", "Packed", "Shipped", "Completed", "Cancelled"]
    commodities = ["Cabai Merah Keriting", "Tomat Beef", "Letus Romaine", "Pakcoy", "Bawang Merah"]
    
    data = []
    for i in range(50):
        date_offset = np.random.randint(0, 30)
        order_date = datetime.date.today() - datetime.timedelta(days=date_offset)
        
        qty = np.random.randint(5, 100)
        price_base = 15000 if "Cabai" in commodities[i%5] else 5000
        price = price_base + np.random.randint(-1000, 2000)
        
        data.append({
            "Order ID": f"ORD-{2024}-{i:03d}",
            "Date": order_date,
            "Customer": f"Cust_{i}",
            "Channel": np.random.choice(channels),
            "Commodity": np.random.choice(commodities),
            "Qty (kg)": qty,
            "Price/kg": price,
            "Total Value": qty * price,
            "Status": np.random.choice(statuses, p=[0.1, 0.2, 0.2, 0.45, 0.05]),
            "Payment": np.random.choice(["Paid", "Unpaid"], p=[0.8, 0.2])
        })
    return pd.DataFrame(data)

# MAIN LAYOUT
st.title("💹 Smart Commerce Center")
st.markdown("""
**Pusat Komando Penjualan & Market Intelligence**
*Omnichannel Order Management | AI Demand Forecasting | Dynamic Pricing Strategy*
""")

# TABS
tab_orders, tab_forecast, tab_pricing = st.tabs([
    "📦 Omnichannel Orders",
    "📈 Demand Forecasting (AI)",
    "🏷️ Dynamic Pricing Engine"
])

# ===== TAB 1: OMNICHANNEL ORDERS =====
with tab_orders:
    st.header("📦 Centralized Order Management")
    st.caption("Satu dashboard untuk mengelola pesanan dari WhatsApp, Marketplace, dan Kontrak B2B.")

    # Load Data (Simulation)
    if 'order_db' not in st.session_state:
        st.session_state.order_db = generate_orders()
    
    df_orders = st.session_state.order_db

    # METRICS
    m1, m2, m3, m4 = st.columns(4)
    daily_sales = df_orders[df_orders['Date'] == datetime.date.today()]['Total Value'].sum()
    total_revenue = df_orders['Total Value'].sum()
    pending_orders = len(df_orders[df_orders['Status'] == 'New'])
    top_channel = df_orders.groupby('Channel')['Total Value'].sum().idxmax()
    
    m1.metric("Omset Hari Ini", f"Rp {daily_sales:,.0f}")
    m2.metric("Total Revenue (30 Hari)", f"Rp {total_revenue:,.0f}")
    m3.metric("Pesanan Baru (Perlu Diproses)", f"{pending_orders}", delta_color="inverse")
    m4.metric("Top Channel", top_channel)

    st.divider()

    # FILTERS & TABLE
    c_filter, c_table = st.columns([1, 3])
    
    with c_filter:
        st.subheader("🔍 Filter")
        f_channel = st.multiselect("Sales Channel", df_orders['Channel'].unique(), default=df_orders['Channel'].unique())
        f_status = st.multiselect("Status Pesanan", df_orders['Status'].unique(), default=["New", "Packed", "Shipped"])
        
    with c_table:
        # Apply filters
        df_view = df_orders[
            (df_orders['Channel'].isin(f_channel)) & 
            (df_orders['Status'].isin(f_status))
        ]
        
        st.dataframe(
            df_view.sort_values(by="Date", ascending=False),
            column_config={
                "Total Value": st.column_config.NumberColumn(format="Rp %d"),
                "Price/kg": st.column_config.NumberColumn(format="Rp %d"),
                "Status": st.column_config.SelectboxColumn(
                    "Status",
                    help="Update status pesanan",
                    width="medium",
                    options=["New", "Packed", "Shipped", "Completed", "Cancelled"],
                    required=True,
                )
            },
            use_container_width=True,
            hide_index=True
        )
        st.caption("*Tips: Anda bisa mengedit 'Status' langsung di tabel (jika terhubung database real).*")

# ===== TAB 2: DEMAND FORECASTING =====
with tab_forecast:
    st.header("📈 Smart Demand Forecasting")
    st.markdown("Prediksi kebutuhan pasar minggu depan berdasarkan tren historis & musiman. **Tanam sesuai permintaan (Market Pull), bukan asal tanam (Production Push).**")

    col_f1, col_f2 = st.columns([1, 2])
    
    with col_f1:
        st.subheader("⚙️ Parameter Prediksi")
        target_com = st.selectbox("Pilih Komoditas", df_orders['Commodity'].unique())
        horizon = st.slider("Horizon Prediksi (Minggu)", 1, 12, 4)
        growth_scen = st.select_slider("Skenario Pertumbuhan Pasar", options=["Konservatif (-10%)", "Normal", "Agresif (+20%)"], value="Normal")
        
        st.info("💡 **Insight:** Permintaan 'Cabai Merah' diprediksi NAIK 15% bulan depan karena menjelang Hari Raya.")

    with col_f2:
        # Generate Forecast Data
        dates = pd.date_range(start=datetime.date.today(), periods=horizon*7)
        # Base demand roughly based on history avg
        avg_qty = df_orders[df_orders['Commodity'] == target_com]['Qty (kg)'].mean()
        if pd.isna(avg_qty): avg_qty = 50
        
        # Add trend & noise
        trend = np.linspace(0, 10, len(dates)) # Increasing trend
        if growth_scen == "Konservatif (-10%)": trend = trend * -0.5
        elif growth_scen == "Agresif (+20%)": trend = trend * 2.5
        
        seasonality = 10 * np.sin(np.linspace(0, 3.14 * horizon, len(dates)))
        
        forecast_vals = avg_qty + trend + seasonality + np.random.normal(0, 5, len(dates))
        forecast_vals = np.maximum(forecast_vals, 0) # No negative demand
        
        df_forecast = pd.DataFrame({"Date": dates, "Predicted Demand (kg)": forecast_vals})
        
        fig_fc = px.line(df_forecast, x='Date', y='Predicted Demand (kg)', title=f"Prediksi Permintaan: {target_com}")
        fig_fc.add_annotation(x=dates[-1], y=forecast_vals[-1], text=f"Target: {int(forecast_vals.sum())} kg total", showarrow=True, arrowhead=1)
        st.plotly_chart(fig_fc, use_container_width=True)
        
        st.success(f"🎯 **Rekomendasi Tanam:** Untuk memenuhi permintaan {horizon} minggu ke depan, Anda perlu menyiapkan lahan seluas **{(forecast_vals.sum()/1000):.1f} Ha** (Asumsi produktivitas 10 ton/ha).")


# ===== TAB 3: DYNAMIC PRICING =====
with tab_pricing:
    st.header("🏷️ Dynamic Pricing Engine")
    st.markdown("Kalkulator harga jual cerdas untuk memaksimalkan margin saat harga pasar fluktuatif.")
    
    c_p1, c_p2, c_p3 = st.columns(3)
    
    with c_p1:
        st.subheader("1. Struktur Biaya (HPP)")
        hpp_prod = st.number_input("HPP Produksi (Rp/kg)", 0, 50000, 8500, help="Biaya benih, pupuk, tenaga kerja")
        hpp_logistics = st.number_input("Biaya Logistik & Packing (Rp/kg)", 0, 10000, 1500)
        total_hpp = hpp_prod + hpp_logistics
        st.metric("Total HPP (Break Even)", f"Rp {total_hpp:,.0f}")
        
    with c_p2:
        st.subheader("2. Kondisi Pasar")
        competitor_price = st.number_input("Harga Pasar Induk Hari Ini (Rp/kg)", 0, 100000, 15000)
        market_trend = st.radio("Tren Pasar:", ["🔥 Naik (Langka)", "➡️ Stabil", "📉 Turun (Banjir)"], horizontal=True)
        
    with c_p3:
        st.subheader("3. Strategi Margin")
        target_margin_pct = st.slider("Target Margin (%)", 0, 100, 30)
        
        # Calculation Logic
        ideal_price = total_hpp * (1 + target_margin_pct/100)
        
        # Dynamic Adjustment logic
        adjusted_price = ideal_price
        color = "green"
        reco_text = "HARGA IDEAL (Sesuai Target)"
        
        if market_trend == "🔥 Naik (Langka)":
            # Opportunity to increase price but stay competitive
            if ideal_price < competitor_price:
                adjusted_price = (ideal_price + competitor_price) / 2 # Take extra profit
                color = "blue"
                reco_text = "MAXIMIZE PROFIT (Pasar Sedang Bagus)"
        elif market_trend == "📉 Turun (Banjir)":
            # Force to lower price to clear stock
            if ideal_price > competitor_price:
                adjusted_price = max(total_hpp * 1.05, competitor_price) # Min 5% margin or market price
                color = "red"
                reco_text = "CLEARANCE SALE (Hindari Rugi)"
                
        st.metric("🎯 Rekomendasi Harga Jual", f"Rp {adjusted_price:,.0f}", delta=f"Margin: {((adjusted_price-total_hpp)/adjusted_price)*100:.1f}%")
        st.caption(f"Status: **{reco_text}**")
        
    st.divider()
    
    # Simulation Table
    st.write("#### 📊 Tabel Sensitivitas Laba")
    
    sens_data = []
    for p in range(int(total_hpp*0.8), int(total_hpp*2.0), 500):
        margin_rp = p - total_hpp
        margin_p = (margin_rp / p) * 100 if p > 0 else 0
        status = "RUGI" if margin_rp < 0 else "UNTUNG"
        sens_data.append({"Harga Jual (Rp)": p, "Profit/kg (Rp)": margin_rp, "Margin (%)": round(margin_p, 1), "Status": status})
        
    df_sens = pd.DataFrame(sens_data)
    
    # Highlight recommended row logic (simplified for viz)
    st.dataframe(df_sens.style.applymap(lambda v: 'color: red;' if v == 'RUGI' else 'color: green;', subset=['Status']), use_container_width=True)

