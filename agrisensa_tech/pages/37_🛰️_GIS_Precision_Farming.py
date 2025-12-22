import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="GIS & Precision Farming - AgriSensa",
    page_icon="🛰️",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Header
st.title("🛰️ AgriSensa GIS & Precision Farming")
st.markdown("""
**Transformasi Digital Pertanian Skala Luas**
*Hardware Integration Required | Big Data Analytics | Spatial Management*
""")

# Main tabs
tab_intro, tab_vra, tab_ndvi, tab_iot, tab_drone = st.tabs([
    "🗺️ Konsep GIS",
    "🚜 VRA (Variable Rate)",
    "📡 Remote Sensing (NDVI)",
    "📶 IoT Sensor Dashboard",
    "✈️ Drone Flight Plan"
])

# ===== TAB 1: KONSEP GIS =====
with tab_intro:
    st.header("🗺️ Geographic Information System (GIS) dalam Pertanian")
    
    st.markdown("""
    ### Apa itu Precision Farming?
    Pertanian Presisi adalah manajemen pertanian berdasarkan **informasi dan teknologi** untuk mengidentifikasi, menganalisis, dan mengelola **variabilitas spasial dan temporal** di dalam lahan untuk keuntungan optimal, keberlanjutan, dan perlindungan lingkungan.
    
    **Konsep "The Right 4":**
    1.  **Right Source:** Sumber input yang tepat.
    2.  **Right Rate:** Dosis yang tepat (sesuai kebutuhan spesifik titik tersebut).
    3.  **Right Time:** Waktu yang tepat.
    4.  **Right Place:** Tempat yang tepat.
    
    ---
    
    ### Komponen Utama:
    *   **GPS/GNSS:** Sistem penentu lokasi global untuk navigasi traktor dan pemetaan.
    *   **GIS Software:** Mengolah data spasial (peta tanah, peta hasil panen, topografi).
    *   **Remote Sensing:** Satelit & Drone untuk pantau kesehatan tanaman (NDVI).
    *   **Vra (Variable Rate Technology):** Mesin yang bisa mengubah dosis aplikasi secara otomatis saat berjalan.
    *   **IoT Sensors:** Sensor tanah/cuaca real-time.
    """)
    
    # Simulasi Peta (Static for now to avoid dependencies issues)
    st.write("### 📍 Simulasi Peta Lahan (Grid Sampling)")
    
    # Create dummy grid data
    cols = list("ABCDE")
    rows = list(range(1, 6))
    
    data_grid = []
    for r in rows:
        for c in cols:
            # Simulasi variabilitas pH tanah (4.5 - 7.5)
            ph = np.random.uniform(4.5, 7.5)
            # Simulasi variabilitas N (ppm)
            n_val = np.random.uniform(10, 50)
            data_grid.append({'Grid': f"{c}{r}", 'Row': r, 'Col': c, 'pH': ph, 'N_ppm': n_val})
            
    df_grid = pd.DataFrame(data_grid)
    
    # Pivot for heatmap
    pivot_ph = df_grid.pivot(index='Row', columns='Col', values='pH')
    
    fig = px.imshow(pivot_ph, 
                    labels=dict(x="Kolom Grid", y="Baris Grid", color="pH Tanah"),
                    x=cols, y=rows,
                    color_continuous_scale='RdYlGn',
                    title="Peta Variabilitas pH Tanah (Simulasi Grid 1 Ha)")
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Peta ini menunjukkan bahwa tanah **TIDAK SERAGAM**. Ada yang masam (merah) dan netral (hijau). Pertanian konvensional memberi kapur rata, Pertanian Presisi memberi kapur **HANYA** di zona merah.")

# ===== TAB 2: VRA (VARIABLE RATE APPLICATION) =====
with tab_vra:
    st.header("🚜 Variable Rate Application (VRA)")
    st.markdown("Teknologi aplikasi input (pupuk/kapur) dengan dosis yang berbeda-beda di setiap titik lahan sesuai kebutuhan.")
    
    st.subheader("Simulasi Resep Pemupukan Presisi")
    
    col1, col2 = st.columns(2)
    with col1:
        target_ph = st.number_input("Target pH Tanah", 6.0, 7.5, 6.5)
        kebutuhan_kapur_per_delta = st.number_input("Kebutuhan Kapur (ton) per kenaikan 1 pH", 1.0, 5.0, 2.0, help="Jumlah kapur (dolomit) untuk menaikkan pH sebesar 1 poin per hektar.")
    
    with col2:
        luas_grid = st.number_input("Luas per Grid (m2)", 100, 10000, 400) # 20x20m default
        
    st.write("---")
    
    # Generate random grid data if not exists (using previous df_grid logic simulation)
    # Re-using df_grid from Tab 1 context isn't clean in Streamlit without session state, so we regen brief logic
    cols = list("ABCDE")
    rows = list(range(1, 6))
    vra_data = []
    
    total_area_ha = (len(cols) * len(rows) * luas_grid) / 10000
    total_lime_needed = 0
    total_lime_uniform = 0
    
    # Calculate Uniform Rate (Konvensional) - asumsikan rata-rata pH 5.5
    avg_ph_assumed = 5.5
    delta_uniform = max(0, target_ph - avg_ph_assumed)
    rate_uniform = delta_uniform * kebutuhan_kapur_per_delta # ton/ha
    total_lime_uniform = rate_uniform * total_area_ha
    
    st.write(f"**Analisis Grid & Resep Dosis:**")
    
    # Display table logic
    for r in rows:
        for c in cols:
            # Random pH again for demo (consistent seed ideally)
            np.random.seed(ord(c) + r) 
            current_ph = np.random.uniform(4.8, 7.2)
            
            # Logic VRA
            delta_ph = max(0, target_ph - current_ph)
            dose_ton_ha = delta_ph * kebutuhan_kapur_per_delta
            dose_kg_grid = (dose_ton_ha * 1000) * (luas_grid / 10000)
            
            total_lime_needed += dose_kg_grid
            
            vra_data.append({
                "Grid ID": f"{c}{r}",
                "pH Aktual": round(current_ph, 2),
                "pH Target": target_ph,
                "Delta": round(delta_ph, 2),
                "Dosis (ton/ha)": round(dose_ton_ha, 2),
                "Kebutuhan Grid (kg)": round(dose_kg_grid, 1)
            })
            
    df_vra = pd.DataFrame(vra_data)
    st.dataframe(df_vra, height=250)
    
    # Summary
    st.subheader("💡 Perbandingan Ekonomi")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        st.metric("Total Luas Lahan", f"{total_area_ha} Ha")
        
    with col_b:
        total_ton_vra = total_lime_needed / 1000
        st.metric("Kebutuhan Kapur (Metode VRA)", f"{total_ton_vra:.2f} Ton")
        
    with col_c:
        st.metric("Kebutuhan Kapur (Metode Konvensional)", f"{total_lime_uniform:.2f} Ton", help="Asumsi dosis rata untuk seluruh lahan")
        
    saving = total_lime_uniform - total_ton_vra
    if saving > 0:
        st.success(f"✅ **EFISIENSI:** Anda menghemat **{saving:.2f} Ton** pupuk dengan metode presisi!")
    else:
        st.warning("Data menunjukkan variabilitas rendah, VRA mungkin belum ekonomis.")

# ===== TAB 3: REMOTE SENSING (NDVI) =====
with tab_ndvi:
    st.header("📡 Remote Sensing & Analisis Citra (NDVI)")
    
    st.markdown("""
    **NDVI (Normalized Difference Vegetation Index)** adalah indeks 'kehijauan' daun yang diukur dari pantulan cahaya.
    
    $$NDVI = \\frac{(NIR - Red)}{(NIR + Red)}$$
    
    *   **NIR (Near Infrared):** Dipantulkan kuat oleh sel daun sehat.
    *   **Red:** Diserap kuat oleh klorofil untuk fotosintesis.
    *   **Nilai:** -1 (Air) sampai +1 (Hutan Lebat). Tanaman sehat biasanya 0.3 - 0.8.
    """)
    
    st.subheader("📈 Simulasi Profil Kesehatan Tanaman")
    
    # Time series simulation
    weeks = list(range(1, 13)) # 12 minggu masa tanam jagung
    
    # Healthy curve (S-curve logic)
    ndvi_healthy = [0.2, 0.3, 0.45, 0.6, 0.75, 0.82, 0.85, 0.83, 0.75, 0.6, 0.4, 0.3]
    # Stressed curve (Drop in middle)
    ndvi_stressed = [0.2, 0.28, 0.4, 0.5, 0.55, 0.5, 0.48, 0.52, 0.5, 0.4, 0.3, 0.2]
    
    df_ndvi = pd.DataFrame({
        "Minggu Ke": weeks,
        "Zona A (Sehat)": ndvi_healthy,
        "Zona B (Stress/Hama)": ndvi_stressed
    })
    
    fig_ndvi = px.line(df_ndvi, x="Minggu Ke", y=["Zona A (Sehat)", "Zona B (Stress/Hama)"],
                       title="Monitoring Kesehatan Tanaman via Satelit",
                       labels={"value": "Nilai NDVI", "variable": "Zona Lahan"})
    
    st.plotly_chart(fig_ndvi, use_container_width=True)
    
    st.warning("⚠️ **Deteksi Dini:** Zona B mengalami penurunan NDVI pada Minggu ke-6. Ini indikasi serangan hama atau kekurangan air sebelum terlihat mata telanjang!")

# ===== TAB 4: IOT SENSOR DASHBOARD =====
with tab_iot:
    st.header("📶 Smart Farming IoT Dashboard")
    st.caption("Simulasi Live Data dari Sensor Lapangan")
    
    if st.button("🔄 Refresh Data Sensor"):
        st.toast("Connecting to IoT Gateway...")
        st.toast("Data updated!")
        
    # Generate dummy live data
    temp = np.random.uniform(28, 34)
    humidity = np.random.uniform(60, 90)
    soil_moist_1 = np.random.uniform(20, 80)
    soil_moist_2 = np.random.uniform(20, 80)
    npk_n = np.random.randint(100, 300)
    
    # Dashboard Layout
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌡️ Suhu Udara", f"{temp:.1f} °C", f"{temp-30:.1f} °C")
    with col2:
        st.metric("💧 Kelembaban", f"{humidity:.1f} %", f"{humidity-75:.1f} %")
    with col3:
        st.metric("🌱 Soil Moisture A", f"{soil_moist_1:.1f} %", help="Sensor Kedalaman 20cm")
    with col4:
        st.metric("🌱 Soil Moisture B", f"{soil_moist_2:.1f} %", help="Sensor Kedalaman 40cm")
        
    st.write("---")
    
    # Gauge Charts (Visual indicators)
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_soil = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = soil_moist_1,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Kelembaban Tanah (Blok Utama)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "red"},
                    {'range': [40, 70], 'color': "lightgreen"},
                    {'range': [70, 100], 'color': "blue"}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 40}}))
        st.plotly_chart(fig_soil, use_container_width=True)
        
        if soil_moist_1 < 40:
            st.error("🚨 **ALERT:** Tanah KERING! Sistem irigasi otomatis akan aktif dalam 5 menit.")
        else:
            st.success("✅ Kondisi Tanah Optimal.")

    with col_chart2:
        st.markdown("### 📝 Log Aktivitas Otomatis")
        st.code("""
        [08:00] Sensor Read: Stabil
        [09:00] Sensor Read: Suhu naik > 32°C
        [09:15] Action: Mist Sprayer ON (Cooling)
        [09:30] Sensor Read: Suhu turun 30°C
        [09:30] Action: Mist Sprayer OFF
        """, language="bash")

# ===== TAB 5: DRONE FLIGHT PLAN =====
with tab_drone:
    st.header("✈️ Kalkulator Misi Terbang Drone (Mapping)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Parameter Kamera & Misi")
        sensor_width = st.number_input("Sensor Width (mm)", value=13.2) # DJI Phantom 4 Pro default
        focal_length = st.number_input("Focal Length (mm)", value=8.8)
        image_width_px = st.number_input("Image Width (pixel)", value=5472)
        
        altitude = st.slider("Ketinggian Terbang (m)", 30, 120, 100)
        overlap = st.slider("Front Overlap (%)", 60, 90, 75)
        
    with col2:
        st.subheader("Hasil Perhitungan GSD")
        # GSD Formula: (Sensor Width * Altitude * 100) / (Focal Length * Image Width)
        gsd = (sensor_width * altitude * 100) / (focal_length * image_width_px)
        
        st.metric("GSD (Ground Sampling Distance)", f"{gsd:.2f} cm/pixel")
        st.caption("*GSD semakin kecil = Peta semakin tajam/detail.*")
        
        if gsd > 5:
            st.warning("GSD > 5 cm. Kurang detail untuk hitung jumlah tanaman, tapi cukup untuk kontur.")
        else:
            st.success("GSD sangat detail! Bisa untuk survei tanaman individual.")
        
        st.info(f"Pada ketinggian {altitude}m, estimasi waktu terbang untuk 10 Ha: ~15-20 menit.")
