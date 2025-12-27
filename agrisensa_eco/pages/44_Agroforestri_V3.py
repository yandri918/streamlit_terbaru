import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium

# Page Config
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Sistem Agroforestri",
    page_icon="🌲",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






# Custom CSS for aesthetics
st.markdown("""
<style>
    .stHeader {
        background-color: #2E7D32;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .card {
        background-color: #f0f8ff;
        border-left: 5px solid #2E7D32;
        padding: 1rem;
        border-radius: 5px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .badge-high {
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .badge-low {
        background-color: #fff3e0;
        color: #e65100;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        padding: 1rem;
        border-radius: 8px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="stHeader">
    <h1>🌲 Sistem Agroforestri Terpadu</h1>
    <p>Panduan Optimalisasi Lahan Di Bawah Tegakan (LMDH / Perhutanan Sosial)</p>
</div>
""", unsafe_allow_html=True)

# Introduction
with st.expander("ℹ️ Tentang Modul Ini & Potensi Agroforestri", expanded=False):
    st.markdown("""
    **Agroforestri** (Wanatani) adalah solusi strategis untuk meningkatkan kesejahteraan petani hutan sekaligus menjaga kelestarian lingkungan.
    Modul ini dirancang khusus untuk mendukung petani mitra **Perhutani** dan pengelola **Perhutanan Sosial**.
    """)

# Main Content Layout - EXPANDED to 8 Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "🌳 Karakteristik", 
    "🌽 Tanaman Sela", 
    "💡 Rekomendasi",
    "💰 Bisnis",
    "🌍 Karbon",
    "🐄 Silvopastura",
    "💧 Getah & HHBK",
    "🔥 Info Kebakaran"
])

with tab1:
    st.subheader("Karakteristik Tegakan Hutan")
    
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("### 🌲 Pinus (*Pinus merkusii*)")
        st.markdown("""
        <div class="card">
        <ul>
            <li><b>Habitat Ideal:</b> <span class="badge-high">Dataran Tinggi (> 700 mdpl)</span></li>
            <li><b>Karakter Naungan:</b> Daun jarum, naungan moderat.</li>
            <li><b>Kondisi Tanah:</b> Cenderung <b>ASAM</b> (pH rendah).</li>
            <li><b>Tanaman Cocok:</b> Kopi Arabika, Wortel, Kapulaga.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🌳 Jati (*Tectona grandis*)")
        st.markdown("""
        <div class="card">
        <ul>
            <li><b>Habitat Ideal:</b> <span class="badge-low">Dataran Rendah - Menengah (< 700 mdpl)</span></li>
            <li><b>Karakter Naungan:</b> Gugur daun saat kemarau.</li>
            <li><b>Kondisi Tanah:</b> Butuh Kalsium (Ca) tinggi, tidak tahan asam kuat.</li>
            <li><b>Tanaman Cocok:</b> Jagung, Padi Gogo, Kunyit, Porang.</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_t2:
        st.markdown("### 🌿 Kayu Putih (*Melaleuca cajuputi*)")
        st.markdown("""
        <div class="card">
        <ul>
            <li><b>Habitat Ideal:</b> <span class="badge-low">Dataran Rendah & Panas</span></li>
            <li><b>Karakter Naungan:</b> Terbuka karena rutin dipangkas.</li>
            <li><b>Tanaman Cocok:</b> Jagung, Kacang-kacangan (Sistem Lorong).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🌲 Damar (*Agathis dammara*)")
        st.markdown("""
        <div class="card">
        <ul>
            <li><b>Habitat Ideal:</b> <span class="badge-high">Dataran Menengah - Tinggi</span></li>
            <li><b>Karakter Naungan:</b> Sangat Teduh / Gelap.</li>
            <li><b>Tanaman Cocok:</b> Tanaman shade-loving (Kapulaga, Vanili).</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.subheader("Panduan Budidaya Tanaman Sela")
    
    crop = st.selectbox("Pilih Komoditas untuk Panduan Detail:", 
                        ["Jagung", "Padi Gogo", "Rempah (Jahe/Kunyit/Kapulaga)", "Porang & Umbi-umbian", "Kopi (Arabika/Robusta)"])
    
    if crop == "Jagung":
        st.markdown("""
        ### 🌽 Jagung
        <span class="badge-low">Cocok: Dataran Rendah - Menengah</span>
        
        *   **Kesesuaian:** Sangat baik di sela **Jati Muda** atau **Kayu Putih**.
        *   **Syarat:** Butuh cahaya matahari > 75%. Jangan tanam di bawah tegakan rapat/tua.
        *   **Tips:** Di dataran tinggi (>800 mdpl), umur panen jagung akan jauh lebih lama.
        """, unsafe_allow_html=True)

    elif crop == "Padi Gogo":
        st.markdown("""
        ### 🌾 Padi Gogo
        <span class="badge-low">Cocok: Dataran Rendah - Menengah (< 700 mdpl)</span>
        
        *   **Varietas:** Gunakan Inpago (Inbrida Padi Gogo).
        *   **Suhu:** Tidak tahan suhu dingin (pertumbuhan melambat drastis di >800 mdpl).
        """, unsafe_allow_html=True)

    elif crop == "Rempah (Jahe/Kunyit/Kapulaga)":
        st.markdown("""
        ### 🍛 Rempah & Empon-empon
        | Jenis | Elevasi Ideal | Keterangan |
        | :--- | :--- | :--- |
        | **Kapulaga** | <span class="badge-high">Menengah - Tinggi (400-1000m)</span> | Emas hijau di bawah **Pinus/Damar**. Butuh lembab. |
        | **Jahe Gajah** | <span class="badge-high">Menengah - Tinggi</span> | Nilai ekonomi tinggi, butuh tanah gembur. |
        | **Jahe Merah** | <span class="badge-low">Rendah - Menengah</span> | Lebih tahan panas & kering. |
        | **Kunyit** | <span class="badge-low">Rendah - Menengah</span> | Sangat adaptif di bawah **Jati**. |
        """, unsafe_allow_html=True)

    elif crop == "Porang & Umbi-umbian":
        st.markdown("""
        ### 🥔 Porang
        <span class="badge-low">Optimal: 100 - 600 mdpl</span>
        
        *   **Ketinggian:** Di atas 700 mdpl pertumbuhan umbi melambat.
        *   **Naungan:** Butuh naungan 40-60%. Ideal di bawah **Jati tua** atau **Sono**.
        """, unsafe_allow_html=True)

    elif "Kopi" in crop:
        st.markdown("""
        ### ☕ Kopi
        Tanaman konservasi terbaik.
        
        *   **Robusta:** <span class="badge-low">Dataran Rendah (0 - 800 mdpl)</span>. Cocok di bawah Lamtoro/Sengon.
        *   **Arabika:** <span class="badge-high">Dataran Tinggi (> 800 mdpl)</span>. Wajib di bawah **Pinus/Eucalyptus** untuk citarasa terbaik.
        """, unsafe_allow_html=True)

with tab3:
    st.subheader("💡 Rekomendasi Cerdas Pola Tanam")
    
    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        altitude = st.select_slider("Ketinggian Tempat (mdpl):", 
                                    options=["Dataran Rendah (<400m)", "Menengah (400-700m)", "Dataran Tinggi (>700m)"])
    with col_in2:
        tree_type = st.selectbox("Jenis Pohon Utama (Tegakan):", ["Jati", "Pinus", "Kayu Putih", "Damar/Sengon"])
    with col_in3:
        tree_age = st.selectbox("Umur / Kondisi Tegakan:", 
                                ["Muda / Terbuka (Cahaya >75%)", 
                                 "Remaja / Sedang (Cahaya 50-75%)", 
                                 "Tua / Rimbun (Cahaya <50%)"])

    st.markdown("---")
    st.markdown(f"### 🌱 Hasil Rekomendasi untuk: **{tree_type}** di **{altitude}**")
    
    rec_text = ""
    rec_type = "info" # success, warning, info, error
    
    # Logic Blocks
    if "Dataran Tinggi" in altitude and tree_type in ["Jati", "Kayu Putih"]:
         st.warning(f"⚠️ **Perhatian:** {tree_type} biasanya kurang optimal di dataran tinggi. Pertumbuhan mungkin lambat.")
    elif "Dataran Rendah" in altitude and tree_type in ["Pinus", "Damar"]:
         st.warning(f"⚠️ **Perhatian:** {tree_type} di dataran rendah rentan hama.")
         
    if "Dataran Rendah" in altitude:
        if tree_type == "Jati":
            if "Muda" in tree_age:
                rec_text = "✅ **Jagung, Padi Gogo, Kacang Tanah, Kedelai.**\n\nOptimal untuk tumpangsari pangan (Palawija)."
                rec_type = "success"
            elif "Remaja" in tree_age:
                rec_text = "✅ **Kunyit, Temulawak, Garut.**\n\nCahaya berkurang, beralih ke rimpang-rimpangan."
                rec_type = "warning"
            else:
                rec_text = "✅ **Porang, Empon-empon (Kunyit/Temu).**\n\nNaungan rapat cocok untuk Porang."
                rec_type = "info"
        elif tree_type == "Kayu Putih":
             rec_text = "✅ **Jagung, Kacang Hijau (Sistem Lorong).**\n\nKayu putih pangkas pendek, cahaya aman untuk jagung."
             rec_type = "success"
        else: 
             rec_text = "✅ **Kopi Robusta.**\n\nJika dipaksakan, Kopi Robusta lebih tahan panas dibanding Arabika."
             rec_type = "warning"

    elif "Menengah" in altitude:
        if "Muda" in tree_age:
            rec_text = "✅ **Jagung, Cabai, Sayuran.**"
            rec_type = "success"
        else: 
            if tree_type == "Pinus" or "Damar" in tree_type:
                rec_text = "✅ **Kapulaga, Jahe Gajah, Kopi Robusta.**\n\nZona transisi sangat bagus untuk rempah."
                rec_type = "success"
            else: 
                rec_text = "✅ **Porang, Vanili, Lada.**"
                rec_type = "success"

    elif "Dataran Tinggi" in altitude:
        if tree_type in ["Pinus", "Damar", "Sengon"]:
            if "Muda" in tree_age:
                rec_text = "✅ **Wortel, Kubis (Kol), Kentang, Bawang Daun.**\n\nSayuran dataran tinggi sangat cocok di sela pinus muda."
                rec_type = "success"
            else:
                rec_text = "⭐ **Kopi Arabika (Premium), Kapulaga.**\n\nKombinasi Pinus + Kopi Arabika adalah standar emas konservasi."
                rec_type = "success"
        else:
            rec_text = "✅ **Sayuran (Jika cahaya cukup), Kopi Arabika.**"
            rec_type = "info"

    if rec_type == "success":
        st.success(rec_text)
    elif rec_type == "warning":
        st.warning(rec_text)
    elif rec_type == "info":
        st.info(rec_text)

with tab4:
    st.subheader("💰 Simulasi Usaha Tani (Tanaman Sela)")
    
    col_biz1, col_biz2 = st.columns(2)
    with col_biz1:
        biz_crop = st.selectbox("Komoditas:", ["Jagung Hibrida", "Porang (Umbi)", "Padi Gogo"])
        biz_area = st.number_input("Luas Lahan Efektif (Ha):", value=0.5, step=0.1)
    
    with col_biz2:
        if biz_crop == "Jagung Hibrida":
            biz_yield = st.number_input("Target Hasil Panen (Ton/Ha):", value=6.0)
            biz_price = st.number_input("Harga Jual (Rp/Kg):", value=4500)
            biz_cost = st.number_input("Biaya Produksi Total (Rp):", value=8000000)
        elif biz_crop == "Porang (Umbi)":
            biz_yield = st.number_input("Target Hasil Panen (Ton/Ha):", value=15.0)
            biz_price = st.number_input("Harga Jual (Rp/Kg):", value=3500)
            biz_cost = st.number_input("Biaya Produksi Total (Rp):", value=15000000)
        else: 
            biz_yield = st.number_input("Target Hasil Panen (Ton/Ha):", value=4.0)
            biz_price = st.number_input("Harga Jual (Rp/Kg):", value=5500)
            biz_cost = st.number_input("Biaya Produksi Total (Rp):", value=6000000)

    # Calculation
    total_revenue = biz_yield * biz_price * 1000 * biz_area 
    total_cost = biz_cost * biz_area
    profit = total_revenue - total_cost
    roi = (profit / total_cost) * 100 if total_cost > 0 else 0
    
    st.markdown("---")
    c_res1, c_res2, c_res3 = st.columns(3)
    c_res1.metric("Omzet", f"Rp {total_revenue:,.0f}")
    c_res2.metric("Biaya", f"Rp {total_cost:,.0f}")
    c_res3.metric("Profit", f"Rp {profit:,.0f}", delta=f"{roi:.1f}% ROI")

with tab5:
    st.subheader("🌍 Kalkulator Karbon")
    
    col_carb1, col_carb2 = st.columns(2)
    with col_carb1:
        c_tree = st.selectbox("Jenis Pohon:", ["Jati", "Pinus", "Mahoni", "Sengon"])
        c_age = st.slider("Umur Rata-rata (Thn):", 5, 40, 10)
    with col_carb2:
        c_dens = st.number_input("Jumlah Pohon:", value=100)
        
    biomass_per_tree = 0
    if c_tree == "Jati":
        biomass_per_tree = 0.15 * (c_age ** 2.3) * 10 
    elif c_tree == "Pinus":
        biomass_per_tree = 0.10 * (c_age ** 2.4) * 8
    elif c_tree == "Mahoni":
        biomass_per_tree = 0.12 * (c_age ** 2.3) * 9
    else: 
        biomass_per_tree = 0.08 * (c_age ** 2.5) * 6
        
    total_biomass_ton = (biomass_per_tree * c_dens) / 1000
    carbon_stock_ton = total_biomass_ton * 0.47
    co2_equivalent = carbon_stock_ton * 3.67
    
    mc1, mc2, mc3 = st.columns(3)
    mc1.metric("Biomassa", f"{total_biomass_ton:,.1f} Ton")
    mc2.metric("Stok C", f"{carbon_stock_ton:,.1f} Ton")
    mc3.metric("Serapan CO2", f"{co2_equivalent:,.1f} Ton", delta="Green")

# === NEW FEATURES ===

with tab6:
    st.subheader("🐄 Silvopastura (Ternak di Hutan)")
    st.markdown("**Integrasi Hutan & Ternak (Agrosilvopastura)**. Hitung daya dukung lahan untuk pakan ternak.")
    
    with st.expander("ℹ️ Konsep HPT (Hutan Pakan Ternak)", expanded=True):
        st.info("""
        Menanam rumput unggul (Gajah/Odot) di bawah tegakan hutan (Jati/Pinus) untuk pakan sapi tanpa merusak pohon utama.
        """)
        
    col_sp1, col_sp2 = st.columns(2)
    with col_sp1:
        luas_hpt = st.number_input("Luas Lahan Hutan (Ha) untuk Rumput:", value=1.0)
        prod_rumput = st.number_input("Produksi Rumput per Ha/Tahun (Ton):", value=40.0, help="Rumput Gajah: 150-200 ton (intensif), di hutan asumsi 30-50 ton.")
        
    with col_sp2:
        bobot_ternak = st.number_input("Bobot Rata-rata Sapi (kg):", value=300.0)
        konsumsi_harian = 0.1 * bobot_ternak # 10% BB (Segar)
        st.write(f"Konsumsi Pakan: **{konsumsi_harian} kg/ekor/hari**")
        
    # Calculation
    total_pakan_tahun = prod_rumput * 1000 # kg
    kebutuhan_sapi_tahun = konsumsi_harian * 365
    kapasitas_tampung = total_pakan_tahun / kebutuhan_sapi_tahun
    
    st.markdown("### 📊 Hasil Analisis Daya Dukung")
    st.metric("Kapasitas Ternak (Carrying Capacity)", f"{kapasitas_tampung:.1f} Ekor Sapi / Ha")
    
    if kapasitas_tampung > 5:
        st.success("✅ **Sangat Potensial.** Lahan ini bisa menjadi lumbung pakan ternak.")
    else:
        st.warning("⚠️ **Terbatas.** Pertimbangkan memilih rumput varietas unggul (Odot/Zanzibar) tahan naungan.")

with tab7:
    st.subheader("💧 Kalkulator Getah & HHBK (Pinus / Karet)")
    st.markdown("Estimasi produksi hasil sadapan (Oleoresin & Lateks).")
    
    # Selector Komoditas
    komoditas_hhbk = st.radio("Pilih Komoditas:", ["🌲 Pinus (Gondorukem)", "🌳 Karet (Lateks/Lump)"], horizontal=True)
    
    if "Pinus" in komoditas_hhbk:
        st.write("#### 🌲 Prediksi Panen Getah Pinus")
        col_g1, col_g2 = st.columns(2)
        
        with col_g1:
            jml_pohon_sadap = st.number_input("Jumlah Pohon Siap Sadap:", value=500, step=50)
            jml_koarekan = st.slider("Jumlah Koarekan (Luka) per Pohon:", 1, 4, 2)
            
        with col_g2:
            yield_per_harvest = st.number_input("Estimasi Getah per Koarekan (gram/panen):", value=20.0, help="Rata-rata 15-25 gram per pembaharuan luka.")
            freq_panen = st.selectbox("Frekuensi Panen:", ["3 Hari Sekali (10x sebulan)", "Seminggu Sekali (4x sebulan)"], key="freq_pinus")
            
        freq_num = 10 if "3 Hari" in freq_panen else 4
        
        # Calc Pinus
        total_gram_per_panen = jml_pohon_sadap * jml_koarekan * yield_per_harvest
        total_kg_bulan = (total_gram_per_panen * freq_num) / 1000
        default_price = 4000
        
    else: # KARET
        st.write("#### 🌳 Prediksi Panen Karet (Lump Mangkok)")
        col_k1, col_k2 = st.columns(2)
        
        with col_k1:
            jml_pohon_sadap = st.number_input("Jumlah Pohon Karet:", value=500, step=50, key="jml_karet")
            # Karet biasanya 1 irisan sadap spiral
            st.info("Asumsi: Sistem sadap 1/2 Spiral (S/2).")
            
        with col_k2:
            yield_per_harvest = st.number_input("Yield per Pohon (gram Basah/sadap):", value=35.0, help="Lump mangkok basah rata-rata 30-50 gram per sadap.")
            freq_panen = st.selectbox("Frekuensi Sadap:", ["2 Hari Sekali (d2) - 15x/bln", "3 Hari Sekali (d3) - 10x/bln"], key="freq_karet")
        
        freq_num = 15 if "2 Hari" in freq_panen else 10
        
        # Calc Karet
        total_gram_per_panen = jml_pohon_sadap * yield_per_harvest
        total_kg_bulan = (total_gram_per_panen * freq_num) / 1000
        default_price = 9000 # Harga lump karet basah variatif, misal 7rb - 10rb
        
    # Output Section (Shared Logic)
    harga_getah = st.number_input(f"Harga Jual ({'Gondorukem' if 'Pinus' in komoditas_hhbk else 'Lump Karet'}) (Rp/Kg):", value=default_price, step=100)
    omzet_getah = total_kg_bulan * harga_getah
    
    st.markdown("---")
    cmg1, cmg2 = st.columns(2)
    cmg1.metric("Potensi Produksi (Bulan)", f"{total_kg_bulan:,.1f} Kg")
    cmg2.metric("Estimasi Pendapatan Kotor", f"Rp {omzet_getah:,.0f}", help=f"Asumsi harga Rp {harga_getah:,.0f}/kg")
    
    if "Pinus" in komoditas_hhbk:
        st.caption("**Tips:** Gunakan stimulan (ETHEPHON) secara bijak untuk meningkatkan getah tanpa merusak pohon.")
    else:
        st.caption("**Tips:** Jaga kebersihan mangkok sadap untuk kualitas DRC (Kadar Karet Kering) terbaik.")

with tab8:
    st.subheader("🔥 Sistem Peringatan Dini Kebakaran (FDRS Advanced)")
    st.markdown("Model: **Fire Warning System** berbasis cuaca mikro dan kondisi bahan bakar.")
    st.error("🛑 **STOP MEMBAKAR!** Cuaca ekstrem + kelalaian = Bencana.")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    
    # Init Session State for FDRS
    if "f_temp" not in st.session_state: st.session_state["f_temp"] = 33
    if "f_hum" not in st.session_state: st.session_state["f_hum"] = 50
    if "f_wind" not in st.session_state: st.session_state["f_wind"] = 20

    with col_f1:
        st.markdown("#### 1. Cuaca")
        
        # Weather Integration
        with st.expander("📍 Ambil Data Satelit (Peta & Real-time)", expanded=False):
            st.caption("Klik di peta untuk memilih lokasi hutan:")
            
            # Map Logic
            default_lat, default_lon = -7.15, 110.14
            m = folium.Map(location=[default_lat, default_lon], zoom_start=9)
            m.add_child(folium.LatLngPopup())
            
            map_data = st_folium(m, height=300, width=400)
            
            # Coord Logic
            if map_data and map_data.get("last_clicked"):
                sel_lat = map_data["last_clicked"]["lat"]
                sel_lon = map_data["last_clicked"]["lng"]
            else:
                sel_lat, sel_lon = default_lat, default_lon
                
            col_coord1, col_coord2 = st.columns(2)
            lat_in = col_coord1.number_input("Lat:", value=sel_lat, format="%.4f")
            lon_in = col_coord2.number_input("Lon:", value=sel_lon, format="%.4f")
            
            if st.button("📡 Tarik Data Live"):
                try:
                    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat_in}&longitude={lon_in}&current=temperature_2m,relative_humidity_2m,wind_speed_10m&wind_speed_unit=kmh"
                    res = requests.get(url, timeout=5).json()
                    curr = res['current']
                    
                    st.session_state["f_temp"] = int(curr['temperature_2m'])
                    st.session_state["f_hum"] = int(curr['relative_humidity_2m'])
                    st.session_state["f_wind"] = int(curr['wind_speed_10m'])
                    st.success(f"Data: {st.session_state['f_temp']}°C, {st.session_state['f_hum']}%, {st.session_state['f_wind']}km/h")
                    st.rerun()
                except Exception as e:
                    st.error(f"Gagal koneksi: {e}")

        f_temp = st.slider("Suhu (°C)", 20, 45, st.session_state["f_temp"], key="slider_temp")
        f_hum = st.slider("Kelembaban (%)", 10, 100, st.session_state["f_hum"], key="slider_hum")
        f_wind = st.slider("Kecepatan Angin (km/jam)", 0, 100, st.session_state["f_wind"], help="Angin kencang mempercepat sebaran api.", key="slider_wind")

        
    with col_f2:
        st.markdown("#### 2. Bahan Bakar")
        f_hth = st.number_input("Hari Tanpa Hujan (HTH)", 0, 60, 5, help="Jumlah hari berturut-turut tidak hujan.")
        f_fuel = st.selectbox("Jenis Bahan Bakar (Serasah)", 
                              ["Daun Lebar (Jati/Mahoni)", "Semak Belukar", "Serasah Pinus (Mudah Terbakar)"])
        
    # --- LOGIC HITUNG (FDRS Simplified Model) ---
    # Skor Dasar Cuaca (0-100 Scale concept mapped to simplified points)
    
    score_temp = 0
    if f_temp > 35: score_temp = 30
    elif f_temp > 30: score_temp = 20
    elif f_temp > 25: score_temp = 10
    
    score_hum = 0
    if f_hum < 40: score_hum = 30
    elif f_hum < 60: score_hum = 20
    elif f_hum < 80: score_hum = 10
    
    score_wind = 0
    if f_wind > 30: score_wind = 30   # Badai
    elif f_wind > 15: score_wind = 20 # Kencang
    elif f_wind > 5: score_wind = 10
    
    score_hth = 0
    if f_hth > 14: score_hth = 30     # Kering Kerontang
    elif f_hth > 7: score_hth = 20    # Kering
    elif f_hth > 3: score_hth = 10
    
    base_index = score_temp + score_hum + score_wind + score_hth
    
    # Fuel Factor Multiplier
    fuel_factor = 1.0
    if "Semak" in f_fuel: fuel_factor = 1.2
    elif "Pinus" in f_fuel: fuel_factor = 1.5 # Resin = Flammable
    
    final_fdrs = base_index * fuel_factor
    
    # --- OUTPUT ---
    with col_f3:
        st.markdown("#### 3. Status Bahaya")
        
        # Color coding & Level
        level_text = ""
        level_color = ""
        action_msg = ""
        
        if final_fdrs >= 100:
            level_text = "EXTREME (SANGAT EKSTREM)"
            level_color = "#000000" # Black
            action_msg = "⛔ AKTIVITAS HUTAN DITUTUP TOTAL."
            st.markdown(f"<h1 style='color:red; text-align:center;'>🔥 {final_fdrs:.0f}</h1>", unsafe_allow_html=True)
        elif final_fdrs >= 70:
            level_text = "VERY HIGH (SANGAT TINGGI)"
            level_color = "#d32f2f" # Red
            action_msg = "🚫 Dilarang menyalakan api. Siaga 1."
            st.markdown(f"<h1 style='color:#d32f2f; text-align:center;'>{final_fdrs:.0f}</h1>", unsafe_allow_html=True)
        elif final_fdrs >= 40:
            level_text = "HIGH (TINGGI)"
            level_color = "#f57c00" # Orange
            action_msg = "⚠️ Waspada puntung rokok & loncatan api."
            st.markdown(f"<h1 style='color:#f57c00; text-align:center;'>{final_fdrs:.0f}</h1>", unsafe_allow_html=True)
        elif final_fdrs >= 20:
            level_text = "MODERATE (SEDANG)"
            level_color = "#fbc02d" # Yellow
            action_msg = "✅ Patroli rutin."
            st.markdown(f"<h1 style='color:#fbc02d; text-align:center;'>{final_fdrs:.0f}</h1>", unsafe_allow_html=True)
        else:
            level_text = "LOW (RENDAH)"
            level_color = "#388e3c" # Green
            action_msg = "✅ Kondisi Aman."
            st.markdown(f"<h1 style='color:#388e3c; text-align:center;'>{final_fdrs:.0f}</h1>", unsafe_allow_html=True)
            
        st.markdown(f"<div style='background-color:{level_color}; color:white; padding:10px; text-align:center; border-radius:5px;'><b>{level_text}</b></div>", unsafe_allow_html=True)
        st.info(f"💡 **SOP:** {action_msg}")

    st.markdown("---")
    st.caption("**Parameter Kunci:** Kecepatan Angin & Serasah Pinus adalah faktor pengali risiko terbesar.")

# Footer
st.markdown("---")
st.caption("Dikembangkan untuk Petani Indonesia & Mitra Perhutani | AgriSensa © 2025")
