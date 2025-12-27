
import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import time
import random

# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(layout="wide", page_title="AgriDrone Command Center", page_icon="🛰️")

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================


# --- CUSTOM CSS ---
st.markdown("""
<style>
    .big-font { font-size: 24px !important; font-weight: bold; color: #0f766e; }
    .sensor-box {
        background-color: #f0fdfa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ccfbf1;
        margin-bottom: 10px;
        text-align: center;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        background-color: #0f766e;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([3, 1])
with c1:
    st.title("🛰️ AgriDrone Command Center")
    st.caption("Pusat Kendali Pertanian Presisi & Monitoring IoT Real-time")
with c2:
    status_drone = st.empty()
    status_drone.success("✅ Drone Ready: DJI Agras T30")

# --- SIDEBAR: MISSION CONTROL ---
with st.sidebar:
    st.header("🎮 Mission Control")
    
    # 1. Flight Plan
    st.subheader("1. Flight Plan")
    region_select = st.selectbox("Area Target", ["Blok A (Padi)", "Blok B (Jagung)", "Blok C (Hutan Rakyat)"])
    altitude = st.slider("Ketinggian Terbang (m)", 10, 100, 50)
    speed = st.slider("Kecepatan (m/s)", 1, 15, 5)
    
    if st.button("🛫 TAKE OFF MISSION"):
        with st.status("🚀 Misi Dimulai...", expanded=True) as status:
            st.write("Checking GPS...")
            time.sleep(1)
            st.write("Arming Motors...")
            time.sleep(1)
            st.write("Ascending to altitude...")
            time.sleep(1)
            st.write("Scanning Area...")
            time.sleep(2)
            status.update(label="✅ Misi Selesai! Data NDVI Terupdate.", state="complete", expanded=False)
            st.toast("Data Scan Baru Diterima!", icon="⬇️")

    
    # 2. Location Selector
    st.divider()
    st.subheader("2. Pilih Lokasi Kebun")
    
    preset_locations = {
        "Banyumas, Jawa Tengah": [-7.45, 109.28],
        "Yogyakarta": [-7.80, 110.36],
        "Bandung, Jawa Barat": [-6.90, 107.62],
        "Malang, Jawa Timur": [-7.98, 112.63],
        "Lampung": [-5.45, 105.27],
        "Custom (Manual Input)": None
    }
    
    location_choice = st.selectbox("Preset Lokasi", list(preset_locations.keys()))
    
    if location_choice == "Custom (Manual Input)":
        col_lat, col_lon = st.columns(2)
        with col_lat:
            custom_lat = st.number_input("Latitude", value=-7.45, format="%.6f")
        with col_lon:
            custom_lon = st.number_input("Longitude", value=109.28, format="%.6f")
        center = [custom_lat, custom_lon]
    else:
        center = preset_locations[location_choice]
    
    # 3. IoT Config
    st.divider()
    st.subheader("3. IoT Sensors")
    st.info("Terhubung ke 12 Titik Sensor")


# --- MAIN LAYOUT ---
col_map, col_iot = st.columns([2.5, 1])

with col_map:
    st.subheader(f"🗺️ Peta Kesehatan Tanaman (NDVI) - {region_select}")
    
    
    # --- FOLIUM MAP SETUP ---
    # Center is now dynamic from sidebar selection
    
    m = folium.Map(location=center, zoom_start=16, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri')
    
    # Simulate NDVI Grid Overlay
    # Create 5x5 grid slightly offset from center
    lat_start = center[0] - 0.002
    lon_start = center[1] - 0.002
    step = 0.001
    
    for i in range(5):
        for j in range(5):
            # Random health logic
            health = random.random() # 0.0 - 1.0
            
            # Color logic
            if health > 0.7:
                color = "#4ade80" # Green (Healthy)
                status = "Sehat"
            elif health > 0.4:
                color = "#facc15" # Yellow (Stress)
                status = "Kurang Air"
            else:
                color = "#ef4444" # Red (Danger)
                status = "Hama/Mati"
            
            # Draw Rectangle
            bounds = [[lat_start + i*step, lon_start + j*step], 
                      [lat_start + (i+1)*step, lon_start + (j+1)*step]]
            
            folium.Rectangle(
                bounds=bounds,
                color=color,
                fill=True,
                fill_opacity=0.5,
                weight=1,
                popup=f"Sektor {i}-{j}: {status} (NDVI: {health:.2f})"
            ).add_to(m)

    # Render Map
    st_folium(m, width="100%", height=500)
    
    st.markdown("""
    **Legenda NDVI:**
    <span style='color:#4ade80'>■</span> Sehat (Nitrogen Cukup) &nbsp;
    <span style='color:#facc15'>■</span> Stres Ringan (Butuh Air) &nbsp;
    <span style='color:#ef4444'>■</span> Kritis (Hama/Penyakit)
    """, unsafe_allow_html=True)

with col_iot:
    st.subheader("📡 Live IoT Dashboard")
    
    # Simulated Real-time Data
    # Random fluctuation
    moist = random.randint(30, 80)
    temp = random.uniform(25, 32)
    ph = random.uniform(5.5, 7.5)
    npk_n = random.randint(100, 300)
    
    # SOIL MOISTURE
    st.markdown(f"""
    <div class="sensor-box">
        <div style='font-size:14px; color:gray;'>💧 Kelembaban Tanah</div>
        <div class="big-font">{moist}%</div>
        <div style='font-size:12px;'>Ideal: 60-80%</div>
    </div>
    """, unsafe_allow_html=True)
    if moist < 40: st.error("⚠️ Tanah Kering! Nyalakan Irigasi.")
    
    # TEMP
    st.markdown(f"""
    <div class="sensor-box">
        <div style='font-size:14px; color:gray;'>🌡️ Suhu Udara</div>
        <div class="big-font">{temp:.1f}°C</div>
    </div>
    """, unsafe_allow_html=True)
    
    # pH
    st.markdown(f"""
    <div class="sensor-box">
        <div style='font-size:14px; color:gray;'>🌍 pH Tanah</div>
        <div class="big-font">{ph:.1f}</div>
        <div style='font-size:12px;'>Netral: 6.5-7.0</div>
    </div>
    """, unsafe_allow_html=True)
    if ph < 6.0: st.warning("⚠️ Tanah Asam! Butuh Kapur.")
    
    # NPK Sensor
    with st.expander("🧪 Detail Nutrisi (NPK)"):
        st.progress(npk_n/400, text=f"Nitrogen: {npk_n} ppm")
        st.progress(random.randint(20, 100)/150, text="Fosfor (P)")
        st.progress(random.randint(100, 300)/500, text="Kalium (K)")

# --- ACTION PANEL ---
st.divider()
c_act1, c_act2, c_act3 = st.columns(3)
with c_act1:
    st.info("💡 **AI Recommendation:** Sektor 3-2 terdeteksi kering. Sistem merekomendasikan irigasi tetes aktif selama 45 menit.")
with c_act2:
    if st.button("🚿 Aktifkan Smart Irrigation"):
        st.success("Perintah Terkirim ke Valve V-03. Irigasi Aktif!")
with c_act3:
    if st.button("🚁 Kirim Drone Penyemprot"):
        st.warning("Otorisasi Diperlukan. Masukkan Kode Pilot.")

