
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime
import uuid

# Page Config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Rantai Pasok & Logistik",
    page_icon="🚚",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ea580c 0%, #c2410c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .metric-card {
        background: #fff7ed;
        border-left: 5px solid #ea580c;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    h1, h2, h3 { color: #9a3412; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1>🚚 Rantai Pasok Pangan</h1><p>Manajemen Logistik, Margin, & Timing Pasar Induk</p></div>', unsafe_allow_html=True)

# DATA REFERENCES
PASAR_INDUK = {
    "PI Kramat Jati (Jakarta)": {"peak_start": 23, "peak_end": 4, "lat": -6.27, "lon": 106.87},
    "PI Tanah Tinggi (Tangerang)": {"peak_start": 22, "peak_end": 3, "lat": -6.17, "lon": 106.66},
    "PI Cibitung (Bekasi)": {"peak_start": 21, "peak_end": 2, "lat": -6.24, "lon": 107.08},
    "PI Caringin (Bandung)": {"peak_start": 20, "peak_end": 1, "lat": -6.94, "lon": 107.57}
}

VEHICLES = {
    "Pick Up (L300)": {"kapasitas": 1000, "km_per_liter": 9, "sewa": 350000},
    "Engkel (4 Roda)": {"kapasitas": 2200, "km_per_liter": 7, "sewa": 600000},
    "Colt Diesel (6 Roda)": {"kapasitas": 4500, "km_per_liter": 5, "sewa": 900000},
    "Fuso (10 Roda)": {"kapasitas": 12000, "km_per_liter": 3, "sewa": 1500000},
}

# TABS
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🚛 Kalkulator Logistik", 
    "💰 Analisis Margin (Tata Niaga)", 
    "⏱️ Radar Pasar Induk",
    "🔗 Blockchain Ledger (Simulasi)",
    "📦 Shipment Tracking (NEW)"
])

# --- TAB 1: LOGISTICS CALCULATOR ---
with tab1:
    st.markdown("### 🚛 Estimasi Biaya Kirim & Susut Bobot")
    st.info("Menghitung HPP Transportasi per Kg agar tidak boncos di jalan.")
    
    col_l1, col_l2 = st.columns(2)
    
    # Calculate Distance via Coordinates (Haversine)
    def haversine(lat1, lon1, lat2, lon2):
        import math
        R = 6371 # Earth radius in km
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c
        
    with col_l1:
        st.subheader("1. Data Pengiriman")
        
        # Auto Distance Feature
        with st.expander("📍 Hitung Jarak Otomatis (Koordinat)", expanded=False):
            st.caption("Masukkan Lat/Lon Kebun (Copy dari Google Maps).")
            kebun_lat = st.number_input("Latitude Kebun", -11.0, 6.0, -6.59, format="%.5f")
            kebun_lon = st.number_input("Longitude Kebun", 95.0, 141.0, 106.79, format="%.5f")
            
            dest_pasar = st.selectbox("Tujuan Otomatis", list(PASAR_INDUK.keys()), key="dest_auto")
            
            if st.button("📏 Hitung Jarak"):
                p_data = PASAR_INDUK[dest_pasar]
                air_dist = haversine(kebun_lat, kebun_lon, p_data['lat'], p_data['lon'])
                road_dist = air_dist * 1.4 # Road factor
                st.session_state['calc_dist'] = int(road_dist)
                st.success(f"Jarak Udara: {air_dist:.1f} km. Estimasi Jalan Raya (Faktor 1.4x): {road_dist:.1f} km.")

        # Main Distance Input (manual or auto-filled)
        def_dist = st.session_state.get('calc_dist', 150)
        jarak = st.number_input("Jarak Tempuh (km)", 10, 1000, def_dist)
        jenis_truk = st.selectbox("Jenis Armada", list(VEHICLES.keys()))
        muatan_kg = st.number_input(f"Total Muatan (kg) - Max {VEHICLES[jenis_truk]['kapasitas']}kg", 100, VEHICLES[jenis_truk]['kapasitas'], int(VEHICLES[jenis_truk]['kapasitas']*0.9))
        
        st.subheader("2. Biaya Operasional")
        harga_bbm = st.number_input("Harga Solar/BBM (Rp/liter)", 5000, 20000, 6800)
        biaya_sopir = st.number_input("Upah Sopir + Kernet (Rp)", 0, 2000000, 250000)
        biaya_tol = st.number_input("Biaya Tol/Parkir/Pungli (Rp)", 0, 2000000, 150000)
        
    with col_l2:
        st.subheader("3. Risiko Susut (Shrinkage)")
        jenis_muatan = st.selectbox("Jenis Komoditas", [
            "Sayur Daun (Bayam)", 
            "Sayur Daun (Sawi/Caisim)", 
            "Sayur Daun (Kangkung)", 
            "Sayur Daun (Selada)",
            "Sayur Buah (Cabe/Tomat)", 
            "Umbi-umbian (Kentang/Bawang)", 
            "Buah Keras (Semangka/Melon)",
            "Lainnya (Input Manual)"
        ])
        
        # Manual Input for Shrinkage
        manual_factor = 0.0
        if jenis_muatan == "Lainnya (Input Manual)":
            manual_factor = st.number_input("Input Susut Manual (% per 100km)", 0.0, 10.0, 1.0, step=0.1)

        
        # Shrinkage Logic per 100km/Time
        susut_factor = 0.0 # % per 100km roughly
        if "Sayur Daun" in jenis_muatan: 
            susut_factor = 2.5
        elif "Sayur Buah" in jenis_muatan: 
            susut_factor = 1.2
        elif "Umbi" in jenis_muatan: 
            susut_factor = 0.5
        elif "Keras" in jenis_muatan: 
            susut_factor = 0.3
        elif jenis_muatan == "Lainnya (Input Manual)":
            susut_factor = manual_factor
        
        est_susut_pct = (jarak / 100) * susut_factor
        berat_susut = muatan_kg * (est_susut_pct / 100)
        berat_jual = muatan_kg - berat_susut
        
        # Cost Calc
        veh_data = VEHICLES[jenis_truk]
        liter_bbm = jarak / veh_data['km_per_liter']
        total_bbm = liter_bbm * harga_bbm
        # Sewa is usually daily, assuming 1 trip fits in rental
        # Note: If own car, sewa = maintenance depreciation.
        
        total_biaya = total_bbm + biaya_sopir + biaya_tol + veh_data['sewa']
        hpp_per_kg_awal = total_biaya / muatan_kg
        hpp_per_kg_akhir = total_biaya / berat_jual # Real logistic cost based on sellable weight
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>💰 Biaya Total: Rp {total_biaya:,.0f}</h3>
            <p>HPP Logistik (Awal): <b>Rp {hpp_per_kg_awal:,.0f} /kg</b></p>
            <p>HPP Logistik (Real): <b>Rp {hpp_per_kg_akhir:,.0f} /kg</b> (Setelah Susut)</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.warning(f"⚠️ **Estimasi Susut:** {est_susut_pct:.1f}% ({berat_susut:.0f} kg hilang diperjalanan). \nBerat siap jual: {berat_jual:.0f} kg.")

        # --- CARBON FOOTPRINT CALCULATOR ---
        st.markdown("---")
        st.subheader("🌍 Jejak Karbon (Carbon Footprint)")
        # Emission factors: Diesel avg 2.68 kg CO2/liter
        total_co2 = liter_bbm * 2.68
        co2_per_kg = total_co2 / muatan_kg
        
        c_c1, c_c2 = st.columns(2)
        c_c1.metric("Total Emisi CO2", f"{total_co2:.1f} kg")
        c_c2.metric("Emisi per kg Produk", f"{co2_per_kg*1000:.1f} gram")
        
        st.caption("Fokus pada Green Logistics untuk akses pasar ekspor & premium.")

        # Breakdown Chart
        cost_data = pd.DataFrame({
            "Komponen": ["Sewa Truk", "BBM", "Sopir", "Tol/Lainnya", "Kerugian Susut (Valuasi)"],
            "Nilai": [veh_data['sewa'], total_bbm, biaya_sopir, biaya_tol, 0] # Susut not cash cost but opportunity cost
        })
        fig_pie = px.pie(cost_data.iloc[:-1], values='Nilai', names='Komponen', title="Komposisi Biaya Distribusi", hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 2: MARGIN ANALYSIS ---
with tab2:
    st.markdown("### 💰 Analisis & Distribusi Margin")
    st.info("Bandingkan struktur harga (Siapa makan untung?) antara Pasar Tradisional vs Modern.")
    
    col_t1, col_t2 = st.columns([1, 2])
    
    with col_t1:
        st.subheader("Data Harga (Simulasi)")
        harga_petani = st.number_input("Harga di Petani (Farm Gate)", 1000, 100000, 5000, step=500)
        
        st.markdown("**Jalur Tradisional:**")
        margin_pengepul = st.slider("Margin Pengepul Desa (%)", 5, 30, 15)
        margin_bandar = st.slider("Margin Bandar Besar (%)", 5, 30, 10)
        margin_pedagang = st.slider("Margin Pengecer Pasar (%)", 10, 50, 25)
        cost_logistik_trad = st.number_input("Biaya Logistik Total (Rp/kg)", 500, 5000, 1500)
        
        st.markdown("---")
        st.markdown("**Jalur Modern (Supermarket):**")
        margin_supplier = st.slider("Margin Supplier/Aggregator (%)", 10, 40, 20)
        margin_retail = st.slider("Margin Supermarket (%)", 15, 60, 35)
        cost_logistik_mod = st.number_input("Biaya Packing & Logistik (Rp/kg)", 1000, 10000, 2500)
        
    with col_t2:
        # Waterfall Logic Traditional
        p1 = harga_petani
        c_p1 = p1 * (margin_pengepul/100)
        p2 = p1 + c_p1 # Pengepul
        c_trs = cost_logistik_trad # Logistik
        p3 = p2 + c_trs # Landed Cost Pasar Induk
        c_p3 = p3 * (margin_bandar/100) # Bandar Margin
        p4 = p3 + c_p3 # Harga Jual Bandar
        c_p4 = p4 * (margin_pedagang/100) # Pengecer Margin
        p_final_trad = p4 + c_p4
        
        # Waterfall Logic Modern
        m1 = harga_petani
        c_ops = cost_logistik_mod # Packing + Sorting + Kirim DC
        m2 = m1 + c_ops
        c_m2 = m2 * (margin_supplier/100)
        m3 = m2 + c_m2 # Harga Masuk DC (Buying Price)
        c_m3 = m3 * (margin_retail/100)
        p_final_mod = m3 + c_m3
        
        mode_view = st.radio("Pilih View:", ["Jalur Tradisional", "Jalur Modern"], horizontal=True)
        
        if mode_view == "Jalur Tradisional":
            fig_wf = go.Figure(go.Waterfall(
                name = "Struktur Harga", orientation = "v",
                measure = ["relative", "relative", "relative", "relative", "relative", "total"],
                x = ["Harga Petani", "Margin Pengepul", "Ongkos Kirim", "Margin Bandar", "Margin Pengecer", "Harga Konsumen"],
                y = [p1, c_p1, c_trs, c_p3, c_p4, p_final_trad],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
            final_p = p_final_trad
            
        else:
             fig_wf = go.Figure(go.Waterfall(
                name = "Struktur Harga", orientation = "v",
                measure = ["relative", "relative", "relative", "relative", "total"],
                x = ["Harga Petani", "Biaya Ops (Sortir/Pack/Kirim)", "Margin Supplier", "Margin Supermarket", "Harga Konsumen"],
                y = [m1, c_ops, c_m2, c_m3, p_final_mod],
                connector = {"line":{"color":"rgb(63, 63, 63)"}},
            ))
             final_p = p_final_mod

        fig_wf.update_layout(title=f"Pembentukan Harga Akhir: Rp {final_p:,.0f}", waterfallgap = 0.3)
        st.plotly_chart(fig_wf, use_container_width=True)
        
        share_petani = (harga_petani / final_p) * 100
        st.info(f"💡 **Farmer's Share:** Petani hanya menikmati **{share_petani:.1f}%** dari harga yang dibayar konsumen akhir.")

# --- TAB 3: MARKET TIMING ---
with tab3:
    # Updated Market Operational Hours (Real World Data)
    PASAR_INDUK = {
        "PI Kramat Jati (Jakarta)": {"ops_start": 19, "peak_start": 21, "peak_end": 23, "ops_end": 24},
        "PI Tanah Tinggi (Tangerang)": {"ops_start": 18, "peak_start": 20, "peak_end": 22, "ops_end": 23},
        # Others keep standard relative trend
        "PI Cibitung (Bekasi)": {"ops_start": 18, "peak_start": 20, "peak_end": 23, "ops_end": 24},
    }

    st.markdown("### ⏱️ Radar Pasar Induk (Real-Time Price Trend)")
    st.info("Analisis Jam Operasional (19.00 - 24.00) & Posisi Lapak.")
    
    col_tm1, col_tm2 = st.columns(2)
    
    with col_tm1:
        target_pasar = st.selectbox("Pilih Pasar Induk Tujuan", list(PASAR_INDUK.keys()))
        data_pasar = PASAR_INDUK[target_pasar]
        
        jam_est_tempuh = st.slider("Estimasi Lama Perjalanan (Jam)", 1, 24, 6)
        posisi_lapak = st.selectbox("Posisi Lapak / Bongkar", ["Depan (Strategis)", "Tengah", "Belakang / Pojok"])
        
        # Logic: Price impact based on stall location
        lapak_premium = 0
        if posisi_lapak == "Depan (Strategis)": lapak_premium = 500 # Rp/kg higher
        elif posisi_lapak == "Belakang / Pojok": lapak_premium = -300 # Discounted
        
        st.write("#### 📊 Profil Harga Pasar:")
        st.write(f"- **Buka Lapak:** {data_pasar['ops_start']}:00 WIB")
        st.write(f"- **Harga Puncak (Golden Hour):** {data_pasar['peak_start']}:00 - {data_pasar['peak_end']}:00 WIB")
        st.write(f"- **Harga Turun (Cuci Gudang):** > {data_pasar['ops_end']}:00 WIB")
        
    with col_tm2:
        st.subheader("🕑 Strategi Keberangkatan")
        
        # Calculate departure to arrive at start of PEAK (21:00)
        arrival_target = data_pasar['peak_start']
        dep_hour = arrival_target - jam_est_tempuh
        
        day_offset = "Hari yang Sama"
        if dep_hour < 0:
            dep_hour += 24
            day_offset = "Hari Sebelumnya"
            
        st.markdown(f"""
        <div style='text-align: center; border: 2px solid #ea580c; background-color: #fff7ed; padding: 15px; border-radius: 10px;'>
            <p>Target Tiba: <b>{arrival_target}:00 WIB</b> (Awal Harga Naik)</p>
            <h3>Truk Berangkat Pukul:</h3>
            <h1 style='color: #ea580c; margin: 0;'>{int(dep_hour):02d}:00 WIB</h1>
            <small>({day_offset})</small>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        # Impact Analysis
        st.markdown(f"**💰 Estimasi Dampak Harga:**")
        st.markdown(f"- Timing Tepat: **Harga Optimal**")
        if lapak_premium > 0:
            st.success(f"- Posisi {posisi_lapak}: Potensi Harga **+Rp {lapak_premium}/kg**")
        elif lapak_premium < 0:
            st.error(f"- Posisi {posisi_lapak}: Potensi Harga **{lapak_premium} Rp/kg** (Susah laku)")
        else:
            st.info(f"- Posisi {posisi_lapak}: Harga Standar")

# --- TAB 4: BLOCKCHAIN LEDGER ---
with tab4:
    st.markdown("### 🔗 Blockchain Supply Chain Ledger (Simulation)")
    st.info("Catatan transaksi yang tidak dapat diubah (Immutable) untuk menjamin transparansi.")
    
    import hashlib
    import qrcode
    from io import BytesIO
    
    def generate_hash(text):
        return hashlib.sha256(text.encode()).hexdigest()

    # SECTION 1: FORM HANDOVER
    st.subheader("📝 Form Serah Terima (Proof of Handover)")
    with st.form("handover_form"):
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            farmer_id = st.text_input("ID Petani / Sertifikat", "PET-2025-001")
            komoditas_name = st.text_input("Nama Komoditas", "Cabai Red Beauty")
            berat_kg = st.number_input("Berat Serah Terima (kg)", 1.0, 10000.0, 200.0)
        with col_h2:
            grade_produk = st.selectbox("Grade", ["Grade A (Premium)", "Grade B", "Grade C", "BS"])
            lokasi_serah = st.text_input("Lokasi Serah Terima", "Gudang Pengepul Cianjur")
            catatan_qc = st.text_area("Catatan QC / Kebersihan", "Lulus sortir, residu minimal.")
        
        submit_handover = st.form_submit_button("✅ Konfirmasi Serah Terima (Simpan ke Ledger)")

    # Simulated Ledger Storage in Session State
    if 'ledger_db' not in st.session_state:
        st.session_state['ledger_db'] = [
            {"actor": "🚜 Petani (Pemanenan)", "timestamp": "2025-12-18 06:00", "action": "Validasi Panen: 500kg Cabai Red Beauty"},
            {"actor": "🚛 Pengepul (Sortir)", "timestamp": "2025-12-18 10:00", "action": "Quality Control: Lulus Seleksi Grade A"}
        ]

    if submit_handover:
        new_entry = {
            "actor": f"🚛 Handover: {farmer_id}",
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
            "action": f"Serah Terima: {berat_kg}kg {komoditas_name} ({grade_produk}) di {lokasi_serah}"
        }
        st.session_state['ledger_db'].append(new_entry)
        st.success(f"Transaksi untuk {farmer_id} berhasil dicatat ke dalam Ledger!")

        # GENERATE QR PASSPORT
        st.markdown("### 🎫 QR Passport (Digital Certificate)")
        qr_data = f"AgriSensa Traceability\nID: {farmer_id}\nItem: {komoditas_name}\nBerat: {berat_kg}kg\nGrade: {grade_produk}\nHash: {generate_hash(str(new_entry))[:16]}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")
        
        buf = BytesIO()
        img_qr.save(buf, format="PNG")
        
        c_qr1, c_qr2 = st.columns([1, 2])
        with c_qr1:
            st.image(buf.getvalue(), caption=f"QR Passport - {farmer_id}")
        with c_qr2:
            st.markdown(f"""
            <div style='background: #f8fafc; padding: 15px; border-radius: 10px; border: 1px solid #cbd5e1;'>
                <h4 style='margin:0;'>🎫 AgriPass Verified</h4>
                <p style='margin:5px 0; font-size: 0.9em;'>Produk ini telah melalui verifikasi serah terima digital.</p>
                <hr/>
                <p style='margin:5px 0;'><b>Komoditas:</b> {komoditas_name}</p>
                <p style='margin:5px 0;'><b>Berat:</b> {berat_kg} kg</p>
                <p style='margin:5px 0;'><b>Grade:</b> {grade_produk}</p>
                <p style='margin:5px 0; font-size: 0.7em; color: gray;'>Immutable Hash: {generate_hash(str(new_entry))}</p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 📜 Riwayat Ledger (Blockchain Timeline)")
    
    prev_hash = "00000000000000000000000000000000"
    
    for i, item in enumerate(st.session_state['ledger_db']):
        curr_text = f"{item['actor']}{item['timestamp']}{item['action']}{prev_hash}"
        curr_hash = generate_hash(curr_text)
        
        with st.container():
            st.markdown(f"""
            <div style='border-left: 5px solid #10b981; padding: 10px; background: #f0fdf4; margin-bottom: 10px;'>
                <p style='margin:0; font-weight:bold; color:#065f46;'>{item['actor']}</p>
                <p style='margin:0; font-size:0.8em; color:gray;'>{item['timestamp']}</p>
                <p style='margin:5px 0;'>{item['action']}</p>
                <code style='font-size:0.7em;'>Hash: {curr_hash[:32]}...</code>
            </div>
            """, unsafe_allow_html=True)
            prev_hash = curr_hash

    # Logic for manual simulated transactions removed in favor of the form

# --- TAB 5: SHIPMENT TRACKING (NEW) ---
with tab5:
    st.markdown("### 📦 Advanced Shipment Tracking & Management")
    st.info("💡 Track pengiriman dari Farm → Pasar Induk → Retail dengan real-time monitoring")
    
    # Initialize session state for shipments
    if 'shipments' not in st.session_state:
        st.session_state.shipments = []
    
    # Quick Stats
    active_shipments = [s for s in st.session_state.shipments if s['status'] != 'delivered']
    
    col_st1, col_st2, col_st3, col_st4 = st.columns(4)
    
    with col_st1:
        st.metric("Total Shipments", len(st.session_state.shipments))
    
    with col_st2:
        st.metric("Active", len(active_shipments))
    
    with col_st3:
        delivered = len([s for s in st.session_state.shipments if s['status'] == 'delivered'])
        st.metric("Delivered", delivered)
    
    with col_st4:
        if st.session_state.shipments:
            avg_cost = sum([s.get('cost_per_kg', 0) for s in st.session_state.shipments]) / len(st.session_state.shipments)
            st.metric("Avg Cost/kg", f"Rp {avg_cost:,.0f}")
        else:
            st.metric("Avg Cost/kg", "Rp 0")
    
    st.divider()
    
    # Create Shipment
    with st.expander("➕ Buat Shipment Baru", expanded=not st.session_state.shipments):
        
        # --- INTEGRATION: LOAD PENDING ORDERS ---
        pending_orders = []
        if 'order_db' in st.session_state:
            df_orders = st.session_state.order_db
            # Filter for New/Packed orders not yet shipped
            pending_orders = df_orders[df_orders['Status'].isin(['New', 'Packed'])].to_dict('records')
        
        selected_order_ids = []
        fulfillment_mode = st.checkbox("🔗 Ambil dari Daftar Pesanan (Fulfillment Mode)")
        
        # Auto-fill variables
        af_commodity = "Cabai Merah"
        af_qty = 500
        af_dest = "PI Kramat Jati"
        
        if fulfillment_mode and pending_orders:
            st.info(f"Ditemukan {len(pending_orders)} pesanan menunggu pengiriman.")
            
            # Multi-select for orders
            order_options = {f"{o['Order ID']} - {o['Customer']} ({o['Qty (kg)']}kg)": o for o in pending_orders}
            selected_labels = st.multiselect("Pilih Pesanan untuk Diangkut:", list(order_options.keys()))
            
            if selected_labels:
                selected_orders = [order_options[l] for l in selected_labels]
                selected_order_ids = [o['Order ID'] for o in selected_orders]
                
                # Auto-calculate totals
                total_q = sum([o['Qty (kg)'] for o in selected_orders])
                commodities = list(set([o['Commodity'] for o in selected_orders]))
                destinations = list(set([o['Channel'] for o in selected_orders])) # Proxy destination
                
                af_commodity = ", ".join(commodities)
                af_qty = total_q
                af_dest = f"Multi-Drop: {', '.join(destinations)}"
                
                st.success(f"📦 Total Muatan: {af_qty} kg | Tujuan: {af_dest}")
        elif fulfillment_mode and not pending_orders:
            st.warning("Tidak ada pesanan status 'New' atau 'Packed' di Modul Commerce.")
        
        # --- END INTEGRATION ---

        with st.form("new_shipment_form"):
            col_ns1, col_ns2 = st.columns(2)
            
            with col_ns1:
                ship_commodity = st.text_input("Komoditas", af_commodity, disabled=fulfillment_mode)
                ship_qty = st.number_input("Quantity (kg)", 10, 50000, int(af_qty), step=10, disabled=fulfillment_mode)
                ship_origin = st.text_input("Origin (Farm/Gudang)", "Farm Banyumas")
                ship_dest = st.text_input("Destination", af_dest)
            
            with col_ns2:
                ship_vehicle = st.selectbox("Kendaraan", list(VEHICLES.keys()))
                ship_driver = st.text_input("Nama Sopir", "")
                ship_dist = st.number_input("Jarak (km)", 1, 1000, 150, step=10)
                ship_date = st.date_input("Tanggal Kirim", datetime.datetime.now())
            
            if st.form_submit_button("🚀 Buat Shipment", type="primary", use_container_width=True):
                # Calculate cost
                veh_data = VEHICLES[ship_vehicle]
                liter_bbm = ship_dist / veh_data['km_per_liter']
                total_bbm = liter_bbm * 6800  # Assume Rp 6800/liter
                total_cost = total_bbm + veh_data['sewa'] + 250000 + 150000  # BBM + Sewa + Sopir + Tol
                cost_per_kg = total_cost / ship_qty
                
                new_ship = {
                    "id": str(uuid.uuid4())[:8],
                    "number": f"SHP-{datetime.datetime.now().strftime('%Y%m%d')}-{len(st.session_state.shipments)+1:03d}",
                    "commodity": ship_commodity,
                    "quantity_kg": ship_qty,
                    "origin": ship_origin,
                    "destination": ship_dest,
                    "vehicle": ship_vehicle,
                    "driver": ship_driver,
                    "distance_km": ship_dist,
                    "date": ship_date.strftime("%Y-%m-%d"),
                    "status": "in_transit" if fulfillment_mode else "packing", # Auto-move if fulfilling
                    "total_cost": total_cost,
                    "cost_per_kg": cost_per_kg,
                    "linked_orders": selected_order_ids, # Linked IDs
                    "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                st.session_state.shipments.append(new_ship)
                
                # --- SYNC STATUS BACK TO COMMERCE ---
                if selected_order_ids and 'order_db' in st.session_state:
                    # Update status in dataframe
                    st.session_state.order_db.loc[
                        st.session_state.order_db['Order ID'].isin(selected_order_ids), 
                        'Status'
                    ] = 'Shipped'
                    st.toast(f"✅ Status {len(selected_order_ids)} pesanan diupdate jadi 'Shipped'!")
                # ------------------------------------
                
                st.success(f"✅ Shipment {new_ship['number']} berhasil dibuat!")
                st.rerun()
    
    st.divider()
    
    # Shipment List
    if st.session_state.shipments:
        st.subheader("📋 Daftar Shipment")
        
        # Filter
        filter_status = st.multiselect("Filter Status", 
                                       ["packing", "in_transit", "arrived", "delivered"],
                                       default=["packing", "in_transit", "arrived"])
        
        filtered = [s for s in st.session_state.shipments if s['status'] in filter_status]
        
        for ship in sorted(filtered, key=lambda x: x['created_at'], reverse=True):
            with st.expander(f"🚛 {ship['number']} - {ship['commodity']} ({ship['status'].replace('_', ' ').title()})"):
                col_sd1, col_sd2 = st.columns(2)
                
                with col_sd1:
                    st.markdown("**Detail Shipment:**")
                    st.write(f"- Komoditas: {ship['commodity']}")
                    st.write(f"- Quantity: {ship['quantity_kg']} kg")
                    st.write(f"- Rute: {ship['origin']} → {ship['destination']}")
                    st.write(f"- Jarak: {ship['distance_km']} km")
                    st.write(f"- Kendaraan: {ship['vehicle']}")
                    st.write(f"- Sopir: {ship['driver']}")
                
                with col_sd2:
                    st.markdown("**Biaya & Status:**")
                    st.write(f"- Tanggal: {ship['date']}")
                    st.write(f"- Total Biaya: Rp {ship['total_cost']:,.0f}")
                    st.write(f"- Biaya per kg: Rp {ship['cost_per_kg']:,.0f}")
                    st.write(f"- Status: **{ship['status'].replace('_', ' ').title()}**")
                
                # --- ACTION BUTTONS & FORMS ---
                st.markdown("---")
                
                # 1. Edit Info (For Packing/Transit)
                if ship['status'] in ['packing', 'in_transit']:
                    with st.expander("✏️ Edit Info Pengiriman"):
                        with st.form(f"edit_{ship['id']}"):
                            ed_driver = st.text_input("Update Nama Sopir", ship.get('driver', ''))
                            ed_note = st.text_area("Catatan Tambahan", ship.get('notes', ''))
                            if st.form_submit_button("Simpan Perubahan"):
                                ship['driver'] = ed_driver
                                ship['notes'] = ed_note
                                st.success("Info updated!")
                                st.rerun()

                # 2. Status Actions
                col_act1, col_act2 = st.columns(2)
                
                with col_act1:
                    # START TRIP
                    if ship['status'] == 'packing':
                        if st.button("🚛 Mulai Jalan (Depart)", key=f"start_{ship['id']}", use_container_width=True):
                            ship['status'] = 'in_transit'
                            st.rerun()
                            
                    # ARRIVAL FORM (The "Check-in" Process)
                    elif ship['status'] == 'in_transit':
                        st.markdown("#### 🏁 Verifikasi Kedatangan")
                        with st.form(f"arrival_{ship['id']}"):
                            act_weight = st.number_input("Berat Aktual Tiba (kg)", 0.0, float(ship['quantity_kg']), float(ship['quantity_kg']), step=0.1)
                            act_condition = st.selectbox("Kondisi Barang", ["Bagus (Fresh)", "Layu Sedikit", "Rusak/Busuk", "Pecah/Rusak Fisik"])
                            act_note = st.text_area("Catatan Penerimaan", "")
                            
                            if st.form_submit_button("✅ Konfirmasi Tiba"):
                                # Calc Shrinkage
                                shrinkage_kg = ship['quantity_kg'] - act_weight
                                shrinkage_pct = (shrinkage_kg / ship['quantity_kg']) * 100
                                
                                ship['actual_arrival'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                                ship['actual_weight'] = act_weight
                                ship['shrinkage_kg'] = shrinkage_kg
                                ship['shrinkage_pct'] = shrinkage_pct
                                ship['arrival_condition'] = act_condition
                                ship['arrival_notes'] = act_note
                                ship['status'] = 'arrived'
                                st.success(f"Tiba! Susut: {shrinkage_kg:.1f} kg ({shrinkage_pct:.1f}%)")
                                st.rerun()

                with col_act2:
                    # FINALIZE (Settlement)
                    if ship['status'] == 'arrived':
                        st.info(f"🏁 Tiba: {ship.get('actual_arrival','-')}")
                        st.write(f"📉 Susut: **{ship.get('shrinkage_kg',0):.1f} kg**")
                        st.write(f"📝 Kondisi: {ship.get('arrival_condition','-')}")
                        
                        if st.button("💰 Selesaikan & Bayar (Complete)", key=f"done_{ship['id']}", use_container_width=True):
                            ship['status'] = 'delivered'
                            
                            # Update Commerce (Complete)
                            if 'linked_orders' in ship and 'order_db' in st.session_state:
                                st.session_state.order_db.loc[
                                    st.session_state.order_db['Order ID'].isin(ship['linked_orders']), 
                                    'Status'
                                ] = 'Completed'
                                
                            st.rerun()
                    
                    # DELETE (Only if not delivered)
                    if ship['status'] != 'delivered':
                         if st.button("🗑️ Batalkan/Hapus", key=f"del_{ship['id']}"):
                            st.session_state.shipments.remove(ship)
                            st.rerun()

    else:
        st.info("Belum ada shipment. Buat shipment baru di atas!")

# Footer
st.markdown("---")
st.caption("AgriSensa Logistics - Mengamankan Profit & Transparansi dari Kebun ke Kota.")
