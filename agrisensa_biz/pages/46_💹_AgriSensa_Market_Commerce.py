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

# HELPER: Initialize Inventory DB
if 'inventory_db' not in st.session_state:
    st.session_state.inventory_db = pd.DataFrame([
        {"ID": "P001", "Nama": "NPK Mutiara 16-16-16", "Kategori": "Pupuk", "Stok": 50, "Satuan": "Zak (50kg)", "Modal": 850000, "Jual": 950000},
        {"ID": "B001", "Nama": "Benih Cabai Merah (Pilar)", "Kategori": "Benih", "Stok": 200, "Satuan": "Sachet", "Modal": 125000, "Jual": 150000},
        {"ID": "A001", "Nama": "Sprayer Elektrik 16L", "Kategori": "Alat", "Stok": 10, "Satuan": "Unit", "Modal": 450000, "Jual": 650000},
        {"ID": "O001", "Nama": "Fungisida Amistartop", "Kategori": "Pestisida", "Stok": 100, "Satuan": "Botol 100ml", "Modal": 85000, "Jual": 110000},
    ])

# TABS
tab_pos, tab_inventory, tab_orders, tab_forecast, tab_pricing = st.tabs([
    "🛒 Kasir (POS)",
    "📦 Gudang & Stok",
    "🚚 Riwayat Pesanan",
    "📈 Demand Forecasting",
    "🏷️ Cek Harga & Margin"
])

# ===== TAB 1: KASIR (POS) =====
with tab_pos:
    st.header("🛒 Point of Sales (Kasir Toko)")
    
    pos_col1, pos_col2 = st.columns([2, 1])
    
    with pos_col1:
        st.subheader("Input Transaksi")
        
        df_inv = st.session_state.inventory_db
        product_list = df_inv['Nama'].tolist()
        
        with st.form("pos_form"):
            col_in_1, col_in_2 = st.columns(2)
            
            with col_in_1:
                selected_product_name = st.selectbox("Pilih Produk", product_list)
                qty_buy = st.number_input("Jumlah Beli", 1, 1000, 1)
            
            with col_in_2:
                # Find product details
                selected_row = df_inv[df_inv['Nama'] == selected_product_name].iloc[0]
                price_unit = selected_row['Jual']
                st.metric("Harga Satuan", f"Rp {price_unit:,.0f}")
                st.metric("Subtotal", f"Rp {price_unit * qty_buy:,.0f}")
            
            customer_name = st.text_input("Nama Pelanggan (Opsional)", "Umum")
            payment_method = st.selectbox("Metode Bayar", ["Tunai", "QRIS", "Transfer", "Bon/Hutang"])
            
            submitted = st.form_submit_button("💰 PROSES PEMBAYARAN", type="primary")
            
            if submitted:
                # 1. Update Inventory
                current_stock = df_inv.loc[df_inv['Nama'] == selected_product_name, 'Stok'].values[0]
                
                if current_stock >= qty_buy:
                    # Deduct Stock
                    df_inv.loc[df_inv['Nama'] == selected_product_name, 'Stok'] -= qty_buy
                    st.session_state.inventory_db = df_inv # Save back
                    
                    # 2. Add to Transaction Log
                    # Initialize orders if not exists (migrating from old dummy logic)
                    if 'order_db' not in st.session_state: st.session_state.order_db = pd.DataFrame()
                    
                    new_trx = {
                        "Order ID": f"TRX-{datetime.datetime.now().strftime('%d%H%M%S')}",
                        "Date": datetime.date.today(),
                        "Customer": customer_name,
                        "Channel": "Offline Store (POS)",
                        "Commodity": selected_product_name,
                        "Qty (kg)": qty_buy, # Using general column name
                        "Price/kg": price_unit,
                        "Total Value": price_unit * qty_buy,
                        "Status": "Completed",
                        "Payment": payment_method
                    }
                    
                    st.session_state.order_db = pd.concat([pd.DataFrame([new_trx]), st.session_state.order_db], ignore_index=True)
                    st.success(f"✅ Transaksi Berhasil! Sisa stok: {current_stock - qty_buy}")
                    
                else:
                    st.error(f"❌ Stok tidak cukup! Sisa hanya {current_stock}.")
    
    with pos_col2:
        st.subheader("Stok Menipis ⚠️")
        low_stock = df_inv[df_inv['Stok'] < 20]
        if not low_stock.empty:
            for idx, row in low_stock.iterrows():
                st.warning(f"**{row['Nama']}**: Tinggal {row['Stok']} {row['Satuan']}")
        else:
            st.success("Semua stok aman.")

# ===== TAB 2: INVENTORY MANAGER =====
with tab_inventory:
    st.header("📦 Manajemen Gudang")
    
    # Editable Table
    edited_df = st.data_editor(st.session_state.inventory_db, num_rows="dynamic", use_container_width=True)
    
    # Save mechanism (Streamlit data editor auto updates details but saving entire DF to session state)
    st.session_state.inventory_db = edited_df

# ===== TAB 3: RIWAYAT PESANAN (Previously Tab 1) =====
with tab_orders:
    st.header("📦 Centralized Order Management")
    st.caption("Satu dashboard untuk mengelola pesanan dari WhatsApp, Marketplace, dan Kontrak B2B.")

    # --- ACTION BAR (INPUT & UPLOAD) ---
    st.sidebar.markdown("### 📥 Input Data Penjualan")
    
    # 1. CSV Upload
    uploaded_sales = st.sidebar.file_uploader("Upload Laporan (CSV)", type="csv")
    if uploaded_sales:
        try:
            df_new = pd.read_csv(uploaded_sales)
            # Basic validation/mapping could go here
            if "Order ID" in df_new.columns:
                st.session_state.order_db = df_new
                st.sidebar.success(f"Loaded {len(df_new)} orders!")
        except Exception as e:
            st.sidebar.error(f"Error: {e}")

    # 2. Manual Input Form
    with st.expander("➕ Input Pesanan Baru (Manual)", expanded=False):
        with st.form("add_order_form"):
            c_in1, c_in2, c_in3 = st.columns(3)
            with c_in1:
                new_date = st.date_input("Tanggal", datetime.date.today())
                new_channel = st.selectbox("Channel", ["WhatsApp (Manual)", "Tokopedia", "Shopee", "TikTok Shop", "Contract B2B", "Offline Store"])
            with c_in2:
                new_cust = st.text_input("Nama Customer", "Walking Customer")
                new_item = st.text_input("Komoditas", "Cabai Merah")
            with c_in3:
                new_qty = st.number_input("Qty (kg)", 1, 1000, 10)
                new_price = st.number_input("Harga/kg (Rp)", 0, 100000, 15000)
            
            if st.form_submit_button("Simpan Pesanan"):
                new_entry = {
                    "Order ID": f"MAN-{datetime.datetime.now().strftime('%m%d%H%M')}",
                    "Date": new_date, # Keep as object for internal match
                    "Customer": new_cust,
                    "Channel": new_channel,
                    "Commodity": new_item,
                    "Qty (kg)": new_qty,
                    "Price/kg": new_price,
                    "Total Value": new_qty * new_price,
                    "Status": "New",
                    "Payment": "Unpaid"
                }
                # Check formatting consistency
                # Convert date strictly for display if needed but generated data uses datetime.date
                st.session_state.order_db = pd.concat([pd.DataFrame([new_entry]), st.session_state.order_db], ignore_index=True)
                st.success("✅ Pesanan berhasil dicatat!")
                st.rerun()

    # Load Data (Simulation OR Session)
    if 'order_db' not in st.session_state:
        st.session_state.order_db = generate_orders()
    
    df_orders = st.session_state.order_db
    # Ensure Date format consistency
    if not pd.api.types.is_datetime64_any_dtype(df_orders['Date']):
         df_orders['Date'] = pd.to_datetime(df_orders['Date']).dt.date


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

