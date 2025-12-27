import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium
import requests

# Page Config
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Budidaya Jamur Profesional",
    page_icon="🍄",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






# ========== HELPER FUNCTIONS ==========
def get_elevation(lat, lon):
    """Get elevation using Open-Meteo API"""
    try:
        url = f"https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={lon}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('elevation', [0])[0]
    except:
        return 0
    return 0

def get_weather_snapshot(lat, lon):
    """Get current weather snapshot"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m&timezone=Asia%2FJakarta"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            return resp.json().get('current', {})
    except:
        return {}
    return {}

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .mushroom-card {
        background: linear-gradient(135deg, rgba(236, 253, 245, 0.8) 0%, rgba(255, 255, 255, 0.4) 100%);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(16, 185, 129, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .param-optimal {
        background: #d1fae5;
        color: #065f46;
        padding: 0.5rem;
        border-radius: 8px;
        font-weight: bold;
    }
    .param-warning {
        background: #fef3c7;
        color: #92400e;
        padding: 0.5rem;
        border-radius: 8px;
        font-weight: bold;
    }
    .param-critical {
        background: #fee2e2;
        color: #991b1b;
        padding: 0.5rem;
        border-radius: 8px;
        font-weight: bold;
    }
    h1, h2, h3 { color: #7c3aed; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1>🍄 AgriSensa Mushroom Cultivation Pro</h1><p>Panduan Budidaya 5 Jenis Jamur Komersial Berbasis Riset Ilmiah</p></div>', unsafe_allow_html=True)

# MUSHROOM DATABASE
MUSHROOM_DATA = {
    "Jamur Tiram (Pleurotus)": {
        "emoji": "🍄",
        "latin": "Pleurotus ostreatus / P. florida",
        "difficulty": "⭐⭐☆☆☆",
        "difficulty_text": "Mudah - Cocok Pemula",
        "temp_mycelium": (25, 30, 28),
        "temp_fruiting": (15, 28, 22),
        "humidity_mycelium": (70, 75),
        "humidity_fruiting": (85, 95),
        "light_lux": (500, 1000),
        "light_hours": (8, 12),
        "co2_ppm": 1000,
        "timeline_days": (45, 60),
        "be_percent": (80, 120),
        "price_min": 25000,
        "price_max": 35000,
        "substrate": "Serbuk gergaji + bekatul (20:1) + kapur 2%",
        "special_req": "Tidak ada - paling mudah",
        "description": "Jamur paling populer untuk pemula. Tumbuh cepat, toleran terhadap variasi suhu, dan mudah dipasarkan."
    },
    "Jamur Kuping (Auricularia)": {
        "emoji": "🍂",
        "latin": "Auricularia auricula-judae / A. polytricha",
        "difficulty": "⭐⭐☆☆☆",
        "difficulty_text": "Mudah - Tahan Panas",
        "temp_mycelium": (22, 30, 25),
        "temp_fruiting": (15, 28, 22),
        "humidity_mycelium": (80, 90),
        "humidity_fruiting": (85, 95),
        "light_lux": (20, 50),
        "light_hours": (8, 10),
        "co2_ppm": 1000,
        "timeline_days": (60, 90),
        "be_percent": (60, 100),
        "price_min": 30000,
        "price_max": 40000,
        "substrate": "Serbuk gergaji + bekatul (C/N 20:1 miselium, 30-40:1 fruiting)",
        "special_req": "pH substrat 5.0-7.0",
        "description": "Cocok untuk dataran rendah dan daerah panas. Tekstur kenyal, populer untuk masakan Asia."
    },
    "Jamur Shiitake (Lentinus)": {
        "emoji": "🍄",
        "latin": "Lentinus edodes",
        "difficulty": "⭐⭐⭐☆☆",
        "difficulty_text": "Menengah - Premium Quality",
        "temp_mycelium": (20, 25, 22),
        "temp_fruiting": (10, 18, 14),
        "humidity_mycelium": (70, 80),
        "humidity_fruiting": (85, 95),
        "light_lux": (200, 500),
        "light_hours": (10, 12),
        "co2_ppm": 1000,
        "timeline_days": (90, 180),
        "be_percent": (50, 80),
        "price_min": 80000,
        "price_max": 150000,
        "substrate": "Kayu keras (oak/beech) atau serbuk gergaji + suplemen",
        "special_req": "BUTUH COLD SHOCK (48-72 jam dari 25°C ke 10°C)",
        "description": "Jamur premium dengan harga tinggi. Butuh kesabaran dan kontrol suhu ketat, tapi sangat menguntungkan."
    },
    "Jamur Kancing (Agaricus)": {
        "emoji": "🔘",
        "latin": "Agaricus bisporus",
        "difficulty": "⭐⭐⭐⭐☆",
        "difficulty_text": "Sulit - Butuh Casing Layer",
        "temp_mycelium": (22, 28, 24),
        "temp_fruiting": (12, 20, 16),
        "humidity_mycelium": (80, 90),
        "humidity_fruiting": (85, 95),
        "light_lux": (0, 50),
        "light_hours": (0, 0),
        "co2_ppm": 2000,
        "timeline_days": (60, 90),
        "be_percent": (60, 100),
        "price_min": 40000,
        "price_max": 60000,
        "substrate": "Kompos khusus (manure + jerami) + CASING LAYER (tanah steril 3-4cm)",
        "special_req": "WAJIB casing layer, kompos khusus, pasteurisasi",
        "description": "Teknis dan rumit. Butuh kompos khusus dan casing layer. Cocok untuk yang sudah berpengalaman."
    },
    "Jamur Enoki (Flammulina)": {
        "emoji": "🍜",
        "latin": "Flammulina velutipes",
        "difficulty": "⭐⭐⭐⭐⭐",
        "difficulty_text": "Sangat Sulit - Butuh Cold Room",
        "temp_mycelium": (22, 26, 24),
        "temp_fruiting": (3, 16, 10),
        "humidity_mycelium": (85, 95),
        "humidity_fruiting": (85, 95),
        "light_lux": (0, 20),
        "light_hours": (0, 2),
        "co2_ppm": 5000,
        "timeline_days": (45, 70),
        "be_percent": (70, 100),
        "price_min": 50000,
        "price_max": 80000,
        "substrate": "Serbuk gergaji + bekatul + suplemen",
        "special_req": "WAJIB COLD ROOM (3-16°C), CO2 tinggi untuk batang panjang",
        "description": "Paling sulit! Butuh investasi cold room/AC 24/7. Batang putih panjang hanya muncul di suhu sangat dingin."
    }
}

# TABS
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab_extra, tab_commercial = st.tabs([
    "🍄 Jamur Tiram", 
    "🍂 Jamur Kuping", 
    "🍄‍🟫 Jamur Shiitake",
    "🔘 Jamur Kancing",
    "🍜 Jamur Enoki",
    "🌡️ Monitor Lingkungan",
    "📍 Rekomendasi Lokasi",
    "📊 Kalkulator Produksi",
    "🔧 Troubleshooting",
    "📚 Info & Tools",
    "🍳 Pasca Panen & Olahan"
])

# Helper function for mushroom guide tabs
def render_mushroom_guide(mushroom_name):
    data = MUSHROOM_DATA[mushroom_name]
    
    st.markdown(f"## {data['emoji']} {mushroom_name}")
    st.markdown(f"**Nama Latin:** *{data['latin']}*")
    
    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric("Tingkat Kesulitan", data['difficulty'])
        st.caption(data['difficulty_text'])
    with col2:
        st.info(data['description'])
    
    st.markdown("---")
    st.subheader("📊 Parameter Lingkungan Optimal")
    
    col_param1, col_param2 = st.columns(2)
    
    with col_param1:
        st.markdown("### 🌡️ Suhu")
        st.markdown(f"""
        **Fase Miselium:**
        - Range: {data['temp_mycelium'][0]}-{data['temp_mycelium'][1]}°C
        - Optimal: **{data['temp_mycelium'][2]}°C**
        
        **Fase Fruiting:**
        - Range: {data['temp_fruiting'][0]}-{data['temp_fruiting'][1]}°C
        - Optimal: **{data['temp_fruiting'][2]}°C**
        """)
        
        st.markdown("### 💧 Kelembaban")
        st.markdown(f"""
        **Fase Miselium:** {data['humidity_mycelium'][0]}-{data['humidity_mycelium'][1]}%
        
        **Fase Fruiting:** {data['humidity_fruiting'][0]}-{data['humidity_fruiting'][1]}%
        """)
    
    with col_param2:
        st.markdown("### 💡 Cahaya")
        st.markdown(f"""
        - Intensitas: {data['light_lux'][0]}-{data['light_lux'][1]} lux
        - Durasi: {data['light_hours'][0]}-{data['light_hours'][1]} jam/hari
        """)
        
        st.markdown("### 🌬️ CO2")
        st.markdown(f"- Maksimal: **<{data['co2_ppm']} ppm**")
        st.caption("Ventilasi yang baik sangat penting!")
    
    st.markdown("---")
    st.subheader("🌾 Substrat & Komposisi")
    st.markdown(f"**Formula:** {data['substrate']}")
    
    if data['special_req'] != "Tidak ada - paling mudah":
        st.warning(f"⚠️ **Kebutuhan Khusus:** {data['special_req']}")
    else:
        st.success(f"✅ {data['special_req']}")
    
    st.markdown("---")
    st.subheader("📅 Timeline Produksi")
    
    timeline_col1, timeline_col2, timeline_col3 = st.columns(3)
    with timeline_col1:
        st.metric("Inokulasi → Panen", f"{data['timeline_days'][0]}-{data['timeline_days'][1]} hari")
    with timeline_col2:
        st.metric("Biological Efficiency", f"{data['be_percent'][0]}-{data['be_percent'][1]}%")
    with timeline_col3:
        st.metric("Harga Pasar", f"Rp {data['price_min']:,}-{data['price_max']:,}/kg")
    
    st.markdown("---")
    st.subheader("📋 Tahapan Budidaya")
    
    st.markdown("""
    **1. Persiapan Substrat (Hari 0-3)**
    - Campur bahan sesuai formula
    - Atur kadar air 60-65%
    - Sterilisasi 121°C selama 2 jam
    
    **2. Inokulasi (Hari 4-5)**
    - Dinginkan substrat hingga <30°C
    - Inokulasi dengan bibit F3 (3-5%)
    - Tutup rapat, simpan di ruang inkubasi
    
    **3. Inkubasi/Spawn Run (Hari 6-30)**
    - Suhu dijaga sesuai parameter miselium
    - Kelembaban 70-80%
    - Ruangan gelap
    - Tunggu miselium memutih sempurna
    
    **4. Inisiasi Fruiting (Hari 31-35)**
    - Buka baglog, beri lubang
    - Turunkan suhu ke range fruiting
    - Naikkan kelembaban ke 85-95%
    - Beri cahaya sesuai kebutuhan
    
    **5. Pemanenan (Hari 36-60)**
    - Panen saat tubuh buah optimal
    - Jangan tunggu terlalu tua
    - Panen dengan memutar, jangan tarik
    - Bisa 2-4 flush (gelombang panen)
    """)

# TAB 1-5: Individual Mushroom Guides
with tab1:
    render_mushroom_guide("Jamur Tiram (Pleurotus)")

with tab2:
    render_mushroom_guide("Jamur Kuping (Auricularia)")
    
    st.markdown("---")
    st.subheader("🍂 Analisa Bisnis: Jual Basah vs Kering")
    st.caption("Jamur kuping adalah satu-satunya jenis yang nilainya bisa naik drastis jika dikeringkan.")
    
    with st.expander("🧮 Buka Kalkulator Basah vs Kering", expanded=True):
        col_dry1, col_dry2 = st.columns(2)
        
        with col_dry1:
            price_fresh_ear = st.number_input("Harga Jual Basah (Rp/kg)", 5000, 50000, 10000, step=500, key="p_fresh_ear")
            price_dry_ear = st.number_input("Harga Jual Kering (Rp/kg)", 50000, 500000, 120000, step=5000, key="p_dry_ear")
            shrinkage = 10 # 10kg fresh = 1kg dry
            
        with col_dry2:
            st.info(f"""
            **Rasio Penyusutan (Shrinkage):**
            Rata-rata **10 kg Basah** menjadi **1 kg Kering** (Kadar air 12-14%).
            
            *Proses pengeringan biaya murah (jemur matahari) namun butuh waktu 2-3 hari.*
            """)
            
        # Calculation for 100kg Fresh Batch
        batch_fresh_kg = 100 # Basis perhitungan
        batch_revenue_fresh = batch_fresh_kg * price_fresh_ear
        
        batch_dry_kg = batch_fresh_kg / shrinkage
        batch_revenue_dry = batch_dry_kg * price_dry_ear
        
        profit_diff = batch_revenue_dry - batch_revenue_fresh
        
        st.write(f"**Simulasi untuk {batch_fresh_kg} kg Hasil Panen:**")
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        
        with metric_col1:
            st.metric("Total Jual Basah", f"Rp {batch_revenue_fresh:,.0f}")
        with metric_col2:
            st.metric("Total Jual Kering", f"Rp {batch_revenue_dry:,.0f}", f"{batch_dry_kg} kg Output")
        with metric_col3:
            st.metric("Selisih (Profit Tambahan)", f"Rp {profit_diff:,.0f}", delta_color="normal" if profit_diff > 0 else "inverse")
            
        if profit_diff > 0:
            st.success(f"✅ **Rekomendasi:** Lebih untung dijual **KERING**. Anda mendapat tambahan Rp {profit_diff:,.0f} per 100kg panen.")
        else:
            st.warning(f"⚠️ **Rekomendasi:** Lebih untung dijual **BASAH**. Harga kering saat ini belum menutupi penyusutan bobot.")

with tab3:
    render_mushroom_guide("Jamur Shiitake (Lentinus)")

with tab4:
    render_mushroom_guide("Jamur Kancing (Agaricus)")

with tab5:
    render_mushroom_guide("Jamur Enoki (Flammulina)")

# TAB 6: Environmental Monitor
with tab6:
    st.subheader("🌡️ Monitor & Analisis Parameter Lingkungan")
    
    col_input1, col_input2 = st.columns(2)
    
    with col_input1:
        selected_mushroom = st.selectbox(
            "Pilih Jenis Jamur",
            list(MUSHROOM_DATA.keys())
        )
        
        growth_phase = st.radio(
            "Fase Pertumbuhan",
            ["Miselium (Inkubasi)", "Fruiting (Berbuah)"]
        )
        
        current_temp = st.number_input(
            "Suhu Aktual (°C)",
            min_value=0.0,
            max_value=50.0,
            value=25.0,
            step=0.5
        )
        
        current_humidity = st.number_input(
            "Kelembaban Aktual (%)",
            min_value=0,
            max_value=100,
            value=80,
            step=1
        )
    
    with col_input2:
        altitude = st.number_input(
            "Ketinggian Lokasi (mdpl)",
            min_value=0,
            max_value=3000,
            value=500,
            step=50
        )
        
        st.markdown("### 📊 Status Parameter")
        
        # Get optimal parameters
        data = MUSHROOM_DATA[selected_mushroom]
        
        if growth_phase == "Miselium (Inkubasi)":
            temp_min, temp_max, temp_opt = data['temp_mycelium']
            hum_min, hum_max = data['humidity_mycelium']
        else:
            temp_min, temp_max, temp_opt = data['temp_fruiting']
            hum_min, hum_max = data['humidity_fruiting']
        
        # Temperature analysis
        if temp_min <= current_temp <= temp_max:
            if abs(current_temp - temp_opt) <= 2:
                st.markdown('<div class="param-optimal">🌡️ Suhu: OPTIMAL ✅</div>', unsafe_allow_html=True)
                temp_status = "optimal"
            else:
                st.markdown('<div class="param-warning">🌡️ Suhu: ACCEPTABLE ⚠️</div>', unsafe_allow_html=True)
                temp_status = "warning"
        else:
            st.markdown('<div class="param-critical">🌡️ Suhu: CRITICAL ❌</div>', unsafe_allow_html=True)
            temp_status = "critical"
        
        # Humidity analysis
        if hum_min <= current_humidity <= hum_max:
            st.markdown('<div class="param-optimal">💧 Kelembaban: OPTIMAL ✅</div>', unsafe_allow_html=True)
            hum_status = "optimal"
        elif abs(current_humidity - hum_min) <= 5 or abs(current_humidity - hum_max) <= 5:
            st.markdown('<div class="param-warning">💧 Kelembaban: ACCEPTABLE ⚠️</div>', unsafe_allow_html=True)
            hum_status = "warning"
        else:
            st.markdown('<div class="param-critical">💧 Kelembaban: CRITICAL ❌</div>', unsafe_allow_html=True)
            hum_status = "critical"
    
    st.markdown("---")
    st.subheader("💡 Rekomendasi Penyesuaian")
    
    recommendations = []
    
    # Temperature recommendations
    if temp_status == "critical":
        if current_temp < temp_min:
            recommendations.append(f"🔥 **SUHU TERLALU RENDAH!** Naikkan suhu ke {temp_min}-{temp_max}°C. Gunakan heater atau pindahkan ke ruangan lebih hangat.")
        else:
            recommendations.append(f"❄️ **SUHU TERLALU TINGGI!** Turunkan suhu ke {temp_min}-{temp_max}°C. Gunakan AC, exhaust fan, atau pindahkan ke ruangan lebih dingin.")
    elif temp_status == "warning":
        recommendations.append(f"⚠️ Suhu bisa lebih optimal di **{temp_opt}°C** untuk hasil maksimal.")
    
    # Humidity recommendations
    if hum_status == "critical":
        if current_humidity < hum_min:
            recommendations.append(f"💧 **KELEMBABAN TERLALU RENDAH!** Naikkan ke {hum_min}-{hum_max}%. Semprot air lebih sering, gunakan humidifier, atau tutup ventilasi.")
        else:
            recommendations.append(f"🌊 **KELEMBABAN TERLALU TINGGI!** Turunkan ke {hum_min}-{hum_max}%. Buka ventilasi, kurangi penyemprotan, gunakan dehumidifier.")
    elif hum_status == "warning":
        recommendations.append(f"⚠️ Kelembaban bisa lebih stabil di {hum_min}-{hum_max}%.")
    
    # Altitude-based recommendations
    if altitude > 1500:
        recommendations.append(f"🏔️ **Lokasi dataran tinggi** - Suhu alami lebih dingin, cocok untuk {data['emoji']} {selected_mushroom}!" if selected_mushroom in ["Jamur Shiitake (Lentinus)", "Jamur Enoki (Flammulina)"] else f"🏔️ **Lokasi dataran tinggi** - Mungkin perlu heating untuk fase miselium.")
    elif altitude < 700:
        recommendations.append(f"🌴 **Lokasi dataran rendah** - Suhu lebih hangat, cocok untuk {data['emoji']} {selected_mushroom}!" if selected_mushroom in ["Jamur Tiram (Pleurotus)", "Jamur Kuping (Auricularia)"] else f"🌴 **Lokasi dataran rendah** - Perlu cooling system untuk fase fruiting.")
    
    if recommendations:
        for rec in recommendations:
            st.warning(rec)
    else:
        st.success("✅ **Semua parameter OPTIMAL!** Pertahankan kondisi ini untuk hasil terbaik.")
    
    # Visualization
    st.markdown("---")
    st.subheader("📈 Visualisasi Parameter")
    
    fig = go.Figure()
    
    # Temperature gauge
    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = current_temp,
        domain = {'x': [0, 0.48], 'y': [0, 1]},
        title = {'text': "Suhu (°C)"},
        delta = {'reference': temp_opt},
        gauge = {
            'axis': {'range': [None, 50]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, temp_min], 'color': "lightgray"},
                {'range': [temp_min, temp_max], 'color': "lightgreen"},
                {'range': [temp_max, 50], 'color': "lightgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': temp_opt
            }
        }
    ))
    
    # Humidity gauge
    fig.add_trace(go.Indicator(
        mode = "gauge+number+delta",
        value = current_humidity,
        domain = {'x': [0.52, 1], 'y': [0, 1]},
        title = {'text': "Kelembaban (%)"},
        delta = {'reference': (hum_min + hum_max) / 2},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, hum_min], 'color': "lightgray"},
                {'range': [hum_min, hum_max], 'color': "lightblue"},
                {'range': [hum_max, 100], 'color': "lightgray"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': (hum_min + hum_max) / 2
            }
        }
    ))
    
    fig.update_layout(height=300)
    st.plotly_chart(fig, use_container_width=True)

# TAB 7: Location-Based Advisor
with tab7:
    st.subheader("📍 Rekomendasi Berdasarkan Lokasi (Auto-Detect)")
    
    col_map, col_res = st.columns([1.5, 1])
    
    with col_map:
        st.markdown("### 🗺️ Pilih Lokasi Lahan")
        st.info("Klik pada peta untuk mendapatkan data ketinggian dan cuaca otomatis.")
        
        # Default: Central Java (Agricultural Hub)
        default_lat, default_lon = -7.3, 110.0
        
        m = folium.Map(location=[default_lat, default_lon], zoom_start=9)
        m.add_child(folium.LatLngPopup())
        
        # Display Map
        map_output = st_folium(m, height=400, use_container_width=True)
        
        # Check interaction
        if map_output and map_output.get("last_clicked"):
            lat = map_output["last_clicked"]["lat"]
            lon = map_output["last_clicked"]["lng"]
            st.success(f"📍 Koordinat: {lat:.4f}, {lon:.4f}")
            
            # Fetch Data
            with st.spinner("Mengambil data topografi & cuaca..."):
                elevation = get_elevation(lat, lon)
                weather = get_weather_snapshot(lat, lon)
                
                # Update Session State for interactivity
                st.session_state['loc_elevation'] = elevation
                st.session_state['loc_temp'] = weather.get('temperature_2m', 26.0)
                st.session_state['loc_hum'] = weather.get('relative_humidity_2m', 80)
        else:
            st.warning("👆 Silakan klik peta untuk analisis otomatis")
            # Defaults if no click
            if 'loc_elevation' not in st.session_state:
                st.session_state['loc_elevation'] = 0.0
                st.session_state['loc_temp'] = 28.0
                st.session_state['loc_hum'] = 80

    with col_res:
        st.markdown("### 📊 Data Lingkungan Real-time")
        
        elev = st.session_state.get('loc_elevation', 0)
        temp_val = st.session_state.get('loc_temp', 0)
        hum_val = st.session_state.get('loc_hum', 0)
        
        met1, met2, met3 = st.columns(3)
        met1.metric("Ketinggian", f"{elev:.0f} mdpl")
        met2.metric("Suhu Alami", f"{temp_val}°C")
        met3.metric("Kelembaban", f"{hum_val}%")
        
        st.markdown("---")
        
        # LOGIC: Recommendation based on Auto Data
        user_altitude = elev
        altitude_category = ""
        
        if user_altitude < 700:
            altitude_category = "Dataran Rendah"
            recommended = ["Jamur Tiram (Pleurotus)", "Jamur Kuping (Auricularia)"]
            possible = ["Jamur Kancing (Agaricus)"]
            difficult = ["Jamur Shiitake (Lentinus)", "Jamur Enoki (Flammulina)"]
            advise = "Suhu cenderung panas. Perlu humidifier atau kabut buatan untuk menjaga kelembaban."
        elif user_altitude < 1500:
            altitude_category = "Dataran Menengah"
            recommended = ["Jamur Tiram (Pleurotus)", "Jamur Shiitake (Lentinus)"]
            possible = ["Jamur Kuping (Auricularia)", "Jamur Kancing (Agaricus)"]
            difficult = ["Jamur Enoki (Flammulina)"]
            advise = "Lokasi ideal! Suhu alami sejuk. Ventilasi yang baik sudah cukup memadai."
        else:
            altitude_category = "Dataran Tinggi"
            recommended = ["Jamur Shiitake (Lentinus)", "Jamur Enoki (Flammulina)"]
            possible = ["Jamur Kancing (Agaricus)"]
            difficult = ["Jamur Tiram (Pleurotus)", "Jamur Kuping (Auricularia)"]
            advise = "Suhu sangat dingin. Sangat bagus untuk jamur premium (Shiitake/Enoki). Tiram mungkin tumbuh lambat."
            
        st.metric("Kategori", altitude_category)
        
        st.success("**✅ SANGAT COCOK:**")
        for r in recommended:
            st.markdown(f"- {r}")
            
        if difficult:
            st.error("**❌ BUTUH PERALATAN KHUSUS (AC/Heater):**")
            for d in difficult:
                st.markdown(f"- {d}")
                
        st.info(f"💡 **Saran:** {advise}")

    st.markdown("---")
    st.subheader("💰 Estimasi Investasi di Lokasi Ini")
    
    investment_data = {
        "Dataran Rendah": {
            "basic": "Rp 5-10 juta (Fokus: Pendinginan & Kelembaban)",
            "advanced": "Rp 20-50 juta (AC + Humidifier otomatis)"
        },
        "Dataran Menengah": {
            "basic": "Rp 3-8 juta (Konstruksi kumbung standar)",
            "advanced": "Rp 15-30 juta (Otomatisasi ventilasi)"
        },
        "Dataran Tinggi": {
            "basic": "Rp 5-10 juta (Isolasi panas/Heater)",
            "advanced": "Rp 20-40 juta (Climate control system)"
        }
    }
    
    inv = investment_data.get(altitude_category, investment_data["Dataran Rendah"])
    
    c_inv1, c_inv2 = st.columns(2)
    with c_inv1:
        st.markdown(f"**Investasi Awal (Pemula):**\n{inv['basic']}")
    with c_inv2:
        st.markdown(f"**Investasi Skala Bisnis:**\n{inv['advanced']}")

# TAB 8: Production Calculator
with tab8:
    st.subheader("📊 Kalkulator Produksi & Estimasi Profit")
    
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        calc_mushroom = st.selectbox(
            "Pilih Jenis Jamur",
            list(MUSHROOM_DATA.keys()),
            key="calc_mushroom"
        )
        
        num_baglogs = st.number_input(
            "Jumlah Baglog",
            min_value=10,
            max_value=10000,
            value=100,
            step=10
        )
        
        start_date_input = st.date_input(
            "📅 Tanggal Mulai Inokulasi (Suntik Bibit)",
            value=datetime.now()
        )
        # Convert to datetime for calculations
        start_date = datetime.combine(start_date_input, datetime.min.time())
        
        substrate_weight = st.number_input(
            "Berat Substrat per Baglog (kg)",
            min_value=0.5,
            max_value=5.0,
            value=1.0,
            step=0.1
        )
        

        selling_price = st.number_input(
            "Harga Jual (Rp/kg)",
            min_value=10000,
            max_value=200000,
            value=MUSHROOM_DATA[calc_mushroom]['price_min'],
            step=1000
        )
        
        cost_per_baglog = st.number_input(
            "Biaya Produksi per Baglog (Rp)",
            min_value=1000,
            max_value=20000,
            value=3500 if calc_mushroom != "Jamur Enoki (Flammulina)" else 5000,
            step=100,
            help="Termasuk bibit, media, plastik, & tenaga kerja per log"
        )
    
    with calc_col2:
        data_calc = MUSHROOM_DATA[calc_mushroom]
        
        # Calculate yields
        total_substrate = num_baglogs * substrate_weight
        be_low = data_calc['be_percent'][0] / 100
        be_high = data_calc['be_percent'][1] / 100
        
        yield_low = total_substrate * be_low
        yield_high = total_substrate * be_high
        yield_avg = (yield_low + yield_high) / 2
        
        revenue_low = yield_low * selling_price
        revenue_high = yield_high * selling_price
        revenue_avg = (revenue_low + revenue_high) / 2
        
        # Production costs (USER INPUT)
        total_cost = num_baglogs * cost_per_baglog
        
        profit_low = revenue_low - total_cost
        profit_high = revenue_high - total_cost
        profit_avg = (profit_low + profit_high) / 2
        
        st.markdown("### 📈 Estimasi Hasil Total")
        
        st.metric("Total Substrat", f"{total_substrate:.1f} kg")
        st.metric("Total Panen (Semua Flush)", 
                 f"{yield_avg:.1f} kg", 
                 delta=f"{yield_low:.1f} - {yield_high:.1f} kg")
        
        st.markdown("### 💰 Estimasi Finansial")
        
        st.metric("Pendapatan Kotor", f"Rp {revenue_avg:,.0f}", 
                 delta=f"Rp {revenue_low:,.0f} - Rp {revenue_high:,.0f}")
        st.metric("Biaya Produksi", f"Rp {total_cost:,.0f}")
        st.metric("Profit Bersih", f"Rp {profit_avg:,.0f}", 
                 delta=f"Rp {profit_low:,.0f} - Rp {profit_high:,.0f}")
    
    st.markdown("---")
    st.subheader("🗓️ Jadwal Panen Harian (Untuk Market)")
    st.info("Simulasi ini menghitung potensi panen per hari berdasarkan pola 'Flush' (gelombang panen) alami jamur.")
    
    # Harvest Simulation Logic
    timeline_days = data_calc['timeline_days']
    first_harvest_day = timeline_days[0]
    
    # Define Flush Patterns (Percentage of total yield per flush)
    # Day offset from first harvest day
    flush_patterns = {
        "Jamur Tiram (Pleurotus)": [(0, 0.40), (15, 0.35), (30, 0.25)], # 3 Flushes: 40%, 35%, 25% interval 15 days
        "Jamur Kuping (Auricularia)": [(0, 0.50), (20, 0.30), (40, 0.20)],
        "Jamur Shiitake (Lentinus)": [(0, 0.30), (30, 0.30), (60, 0.20), (90, 0.20)], # Slow, many flushes
        "Jamur Kancing (Agaricus)": [(0, 0.45), (10, 0.35), (20, 0.20)],
        "Jamur Enoki (Flammulina)": [(0, 1.0)] # Usually one big harvest then discard
    }
    
    pattern = flush_patterns.get(calc_mushroom, [(0, 1.0)])
    
    # Generate daily harvest data
    daily_harvest = {} # Day: Kg
    harvest_window = 5 # Each flush spreads over 5 days
    
    for start_offset, harvest_pct in pattern:
        flush_yield = yield_avg * harvest_pct
        start_day_idx = first_harvest_day + start_offset
        
        # Distribute flush yield over harvest window (Gaussian-ish)
        # Day 1: 10%, Day 2: 20%, Day 3: 40%, Day 4: 20%, Day 5: 10%
        daily_distribution = [0.10, 0.20, 0.40, 0.20, 0.10]
        
        for i, daily_pct in enumerate(daily_distribution):
            day = start_day_idx + i
            kg_today = flush_yield * daily_pct
            daily_harvest[day] = daily_harvest.get(day, 0) + kg_today

    # Create DataFrame
    if daily_harvest:
        days = sorted(daily_harvest.keys())
        # start_date is already defined above from user input
        
        harvest_list = []
        for d in range(min(days), max(days) + 1):
            kg = daily_harvest.get(d, 0)
            if kg > 0.1: # Only show significant days
                date_str = (start_date + timedelta(days=d)).strftime("%d %b %Y")
                harvest_list.append({
                    "Hari Ke-": d,
                    "Tanggal": date_str,
                    "Estimasi Panen (kg)": round(kg, 1),
                    "Status": "Panen Raya 🌟" if kg > (yield_avg * 0.05) else "Panen Biasa"
                })
        
        df_harvest = pd.DataFrame(harvest_list)
        
        # 1. Visualization
        fig_harvest = px.bar(
            df_harvest, 
            x="Tanggal", 
            y="Estimasi Panen (kg)",
            color="Estimasi Panen (kg)",
            color_continuous_scale="Greens",
            title=f"📅 Potensi Panen Harian ({calc_mushroom})",
            labels={"Estimasi Panen (kg)": "Kg per Hari"}
        )
        st.plotly_chart(fig_harvest, use_container_width=True)
        
        # 2. Table
        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            st.dataframe(df_harvest, use_container_width=True, hide_index=True)
        with col_t2:
            max_day = df_harvest.loc[df_harvest["Estimasi Panen (kg)"].idxmax()]
            st.success(f"""
            **🎯 Puncak Panen:**
            
            Tanggal: **{max_day['Tanggal']}**
            Jumlah: **{max_day['Estimasi Panen (kg)']} kg**
            
            *Siapkan pasar/pembeli pada tanggal ini!*
            """)
    
    st.markdown("---")
    st.subheader("📝 Timeline Aktivitas Lengkap")
    
    timeline_events = [
        (0, "Persiapan Substrat", "Mixing, sterilisasi"),
        (4, "Inokulasi", "Tanam bibit F3"),
        (5, "Inkubasi Mulai", "Ruang gelap, suhu miselium"),
        (timeline_days[0] // 2, "Miselium 50%", "Cek kontaminasi"),
        (timeline_days[0] - 5, "Miselium 100%", "Siap fruiting"),
        (timeline_days[0], "Inisiasi Fruiting", "Buka baglog, turunkan suhu"),
    ]
    
    # Add Harvest Events to timeline
    for i, (offset, pct) in enumerate(pattern):
        day = first_harvest_day + offset
        timeline_events.append((day, f"Mulai Panen Flush {i+1}", f"Estimasi {pct*100:.0f}% dari total hasil"))

    timeline_events.append((timeline_days[1], "Selesai", "Buang baglog / Kompos"))
    
    timeline_df = pd.DataFrame([
        {
            "Hari Ke-": day,
            "Tanggal": (start_date + timedelta(days=day)).strftime("%d %b %Y"),
            "Aktivitas": activity,
            "Keterangan": note
        }
        for day, activity, note in sorted(timeline_events)
    ])
    
    st.dataframe(timeline_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.info(f"""
    💡 **Tips Maksimalkan Profit:**
    - Jaga kebersihan untuk minimalisir kontaminasi
    - Monitor suhu & kelembaban setiap hari
    - Panen di waktu yang tepat (jangan terlalu tua)
    - Pasarkan langsung ke konsumen untuk margin lebih besar
    - Pertimbangkan diversifikasi (2-3 jenis jamur)
    """)

    st.markdown("---")
    st.subheader("🔄 Kalkulator Siklus Berkelanjutan (Continuous Harvest)")
    st.caption("Hitung kebutuhan infrastruktur untuk menjamin panen SETIAP HARI tanpa putus.")

    with st.expander("🛠️ Buka Kalkulator Siklus & Rotasi Kumbung", expanded=True):
        col_sus1, col_sus2 = st.columns(2)
        
        with col_sus1:
            kumbung_cap = st.number_input("Kapasitas per Kumbung (Log)", 1000, 50000, 6000, step=500)
            target_harvest_interval = st.selectbox(
                "Target Frekuensi Tanam Baru",
                ["2 Minggu Sekali", "1 Bulan Sekali", "2 Bulan Sekali"],
                index=1
            )
            
            interval_days = 30
            if target_harvest_interval == "2 Minggu Sekali":
                interval_days = 14
            elif target_harvest_interval == "2 Bulan Sekali":
                interval_days = 60
                
            cleaning_gap = st.number_input("Jeda Sterilisasi Kumbung (Hari)", 1, 14, 7, help="Waktu untuk bersih-bersih setelah afkir sebelum isi baru")
            
        with col_sus2:
            # Calculation
            cycle_duration = timeline_days[1] # Max days (e.g., 60 for Oyster)
            total_occupancy = cycle_duration + cleaning_gap
            
            # Formula: Houses needed = Total Occupancy / Planting Interval
            # Example: 67 days / 14 days = 4.7 -> 5 Houses
            import math
            kumbung_needed = math.ceil(total_occupancy / interval_days)
            
            total_logs_system = kumbung_needed * kumbung_cap
            
            # Estimasi Yield Stabil
            # If we plant 'kumbung_cap' every 'interval_days'
            # Average daily yield = (Total Yield per Batch / Interval Days)
            # Total Yield per Batch = kumbung_cap * substrate_weight * be_avg
            # Wait, yield_avg is for 'num_baglogs' which is user input above. We need to recalc for 'kumbung_cap'
            
            batch_substrate = kumbung_cap * substrate_weight # kg
            batch_yield = batch_substrate * ((be_low + be_high)/2) # kg
            
            stable_daily_yield = batch_yield / interval_days
            
            st.metric("🏠 Jumlah Kumbung Dibutuhkan", f"{kumbung_needed} Unit")
            st.metric("📦 Total Populasi Sistem", f"{total_logs_system:,} Baglog")
            st.metric("⚖️ Estimasi Panen Stabil", f"±{stable_daily_yield:.1f} kg / hari", help="Rata-rata panen harian saat sistem sudah berjalan penuh")
            
        st.markdown("### 🗓️ Jadwal Rotasi Tanam (Sistem Berjalan)")
        
        rotation_data = []
        current_date = datetime.now()
        
        for k in range(1, kumbung_needed + 1):
            plant_date = current_date + timedelta(days=(k-1)*interval_days)
            harvest_start = plant_date + timedelta(days=first_harvest_day)
            end_date = plant_date + timedelta(days=cycle_duration)
            next_fill = end_date + timedelta(days=cleaning_gap)
            
            rotation_data.append({
                "Kumbung": f"Unit {k}",
                "Tanam (Start)": plant_date.strftime("%d %b %Y"),
                "Mulai Panen": harvest_start.strftime("%d %b %Y"),
                "Afkir (Selesai)": end_date.strftime("%d %b %Y"),
                "Siap Isi Ulang": next_fill.strftime("%d %b %Y")
            })
            
        st.dataframe(pd.DataFrame(rotation_data), use_container_width=True, hide_index=True)
        
        st.success(f"**Kesimpulan:** Dengan membangun **{kumbung_needed} kumbung** kapacitas {kumbung_cap} log dan menanam setiap **{target_harvest_interval}**, Anda akan mendapatkan panen stabil **{stable_daily_yield:.0f} kg/hari** sepanjang tahun.")

    st.markdown("---")
    st.subheader("♻️ Manajemen Limbah (Zero Waste Income)")
    st.caption("Ubah sampah baglog menjadi Rupiah! Jangan buang limbah sembarangan.")
    
    with st.expander("💰 Hitung Potensi Uang dari Limbah Baglog", expanded=False):
        col_waste1, col_waste2 = st.columns(2)
        
        with col_waste1:
            waste_log_count = st.number_input("Jumlah Baglog Afkir", 10, 50000, num_baglogs, step=100, help="Default mengambil dari input di atas, tapi bisa diubah")
            waste_price_curah = st.number_input("Harga Jual Limbah Curah (Rp/karung)", 0, 50000, 2000, step=500, help="Dijual mentah ke petani sayur/tanaman hias")
            waste_price_premium = st.number_input("Harga Jual Kompos Premium (Rp/kg)", 0, 50000, 5000, step=500, help="Setelah difermentasi + dikemas rapi")
            avg_log_residue = 0.6 # kg (asumsi penyusutan bobot 40% setelah panen habis)
            
        with col_waste2:
            st.info("""
            **Opsi Pengolahan:**
            1. **Jual Curah:** Langsung jual karungan ke petani sayur/cabe (Cepat, duit kecil).
            2. **Kompos:** Fermentasi dengan kotoran hewan + EM4 selama 1 bulan (Lama, duit besar).
            """)
            
        # Calculation
        total_waste_logs = waste_log_count # From new input
        total_waste_weight = total_waste_logs * substrate_weight * avg_log_residue # kg
        
        # Scenario 1: Curah (per sack ~20kg)
        sacks_count = total_waste_weight / 20
        revenue_curah = sacks_count * waste_price_curah
        
        # Scenario 2: Premium (per kg)
        # Asumsi rendemen kompos 80% dari limbah basah
        compost_yield = total_waste_weight * 0.8
        revenue_premium = compost_yield * waste_price_premium
        
        st.markdown("### 💸 Potensi Pendapatan Tambahan")
        c_res1, c_res2 = st.columns(2)
        
        with c_res1:
            st.metric("Opsi 1: Jual Curah", f"Rp {revenue_curah:,.0f}", f"{int(sacks_count)} karung")
            
        with c_res2:
            st.metric("Opsi 2: Olah Kompos", f"Rp {revenue_premium:,.0f}", f"{int(compost_yield)} kg (Siap Pakai)")
            
        st.info(f"""
        **ℹ️ Simulasi Perhitungan untuk {waste_log_count} Baglog:**
        1. **Total Bobot Awal:** {waste_log_count} baglog × {substrate_weight} kg = **{waste_log_count * substrate_weight:,.0f} kg**
        2. **Est. Berat Limbah (60%):** {waste_log_count * substrate_weight:,.0f} kg × 0.6 = **{total_waste_weight:,.0f} kg** (Limbah Basah)
        3. **Est. Kompos Jadi (80%):** {total_waste_weight:,.0f} kg × 0.8 = **{compost_yield:,.0f} kg** (Siap Jual)
        """)
        
        st.success("**Saran:** Gunakan limbah untuk membiayai operasional listrik & air. Ini adalah 'hidden profit'!")

    st.markdown("---")
    st.subheader("📄 Export Laporan Bisnis")
    st.caption("Download semua perhitungan di atas sebagai Proposal Bisnis / Laporan Bank.")
    
    # Prepare Data for Export
    import io
    
    # 1. Summary Data
    summary_data = {
        "Parameter": [
            "Jenis Jamur", "Jumlah Baglog Saat Ini", "Estimasi Total Panen (kg)", 
            "Pendapatan Kotor", "Biaya Operasional", "Profit Bersih",
            "Kebutuhan Kumbung (Kontinyu)", "Potensi Uang Limbah (Kompos)"
        ],
        "Nilai": [
            calc_mushroom, num_baglogs, f"{yield_avg:.1f}",
            f"Rp {revenue_avg:,.0f}", f"Rp {total_cost:,.0f}", f"Rp {profit_avg:,.0f}",
            f"{kumbung_needed} Unit (@{kumbung_cap} log)", f"Rp {revenue_premium:,.0f}"
        ]
    }
    df_summary = pd.DataFrame(summary_data)
    
    # 2. Daily Harvest Schedule (already in df_harvest)
    # 3. Rotation Schedule (already in pd.DataFrame(rotation_data))
    df_rotation = pd.DataFrame(rotation_data)
    
    # Buffer
    buffer = io.BytesIO()
    
    # Create Excel Writer
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_summary.to_excel(writer, sheet_name='Ringkasan Bisnis', index=False)
        if 'df_harvest' in locals() and not df_harvest.empty:
            df_harvest.to_excel(writer, sheet_name='Jadwal Panen', index=False)
        df_rotation.to_excel(writer, sheet_name='Rotasi Kumbung', index=False)
        
        # Add metadata sheet
        pd.DataFrame({
            "Generated By": ["AgriSensa App"],
            "Date": [datetime.now().strftime("%Y-%m-%d %H:%M")]
        }).to_excel(writer, sheet_name='Metadata', index=False)
        
    # Download Button
    st.download_button(
        label="📥 Download Laporan Lengkap (.xlsx)",
        data=buffer.getvalue(),
        file_name=f"Laporan_Bisnis_{calc_mushroom.split()[0]}_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.ms-excel",
        help="Laporan ini berisi: Ringkasan Finansial, Jadwal Panen Harian, Rencana Rotasi Kumbung, & Potensi Limbah."
    )

# TAB 9: Troubleshooting
with tab9:
    st.subheader("🔧 Panduan Troubleshooting")
    
    problem_category = st.selectbox(
        "Pilih Kategori Masalah",
        ["Kontaminasi", "Pertumbuhan Lambat", "Tubuh Buah Abnormal", "Masalah Lingkungan", "Masalah Khusus per Jenis"]
    )
    
    if problem_category == "Kontaminasi":
        st.markdown("""
        ### 🦠 Kontaminasi (Jamur Hijau, Bakteri, dll)
        """)
        
        # VISUAL DOCTOR
        st.info("📸 **Visual Doctor:** Mencocokkan Gejala")
        col_img1, col_img2 = st.columns([1, 2])
        with col_img1:
            try:
                st.image("assets/img/trichoderma.png", caption="Kontaminasi Trichoderma (Jamur Hijau)", use_column_width=True)
            except:
                st.caption("📷 (Gambar tidak tersedia server)")
        with col_img2:
            st.markdown("""
            **Gejala Utama:**
            - **Warna Hijau Melingkar:** Khas Trichoderma. Awalnya putih, lalu hijau spora.
            - **Bau Apek/Tanah:** Berbeda dengan bau segar miselium jamur tiram.
            - **Tekstur Kasar**: Seperti beludru kasar.
            """)
        
        st.markdown("""
        **Penyebab:**
        - Sterilisasi tidak sempurna (kurang panas/lama)
        - Inokulasi tidak steril (tangan/alat kotor)
        - Ruangan terlalu lembab (>95%) tanpa sirkulasi
        
        **Solusi:**
        1. **Isolasi & Buang:** Jangan buka log hijau di dalam kumbung! Spora akan menyebar.
        2. **Sterilisasi Ulang:** Bersihkan rak dengan alkohol 70% atau pemutih (bleach) 5%.
        3. **Cek Bibit:** Pastikan bibit F3 tidak membawa spora hijau sejak awal.
        """)
    
    elif problem_category == "Pertumbuhan Lambat":
        st.markdown("""
        ### 🐌 Pertumbuhan Miselium Lambat
        
        **Gejala:**
        - Miselium tumbuh <1cm per hari
        - Tidak merata
        - Warna kekuningan
        
        **Penyebab:**
        - Suhu terlalu rendah/tinggi
        - Kadar air substrat tidak tepat
        - Bibit kurang bagus
        - Nutrisi substrat kurang
        
        **Solusi:**
        1. Cek suhu ruangan (harus sesuai parameter miselium)
        2. Cek kadar air substrat (60-65% optimal)
        3. Ganti supplier bibit jika perlu
        4. Tambahkan suplemen (bekatul, dedak)
        5. Pastikan pH substrat 6-7
        
        **Preventif:**
        - Gunakan thermometer/hygrometer digital
        - Tes kadar air sebelum sterilisasi
        - Beli bibit dari produsen terpercaya
        """)
    
    elif problem_category == "Tubuh Buah Abnormal":
        st.markdown("""
        ### 🍄 Tubuh Buah Kecil, Kering, atau Deformasi
        
        **Gejala:**
        - Jamur kecil-kecil
        - Batang panjang, tudung kecil
        - Kering/pecah-pecah
        - Warna pucat
        
        **Penyebab:**
        - Kelembaban terlalu rendah
        - Ventilasi buruk (CO2 tinggi)
        - Cahaya tidak cukup/terlalu banyak
        - Penyiraman tidak teratur
        
        **Solusi:**
        1. **Kelembaban rendah:** Semprot lebih sering, gunakan humidifier
        2. **CO2 tinggi:** Buka ventilasi, gunakan exhaust fan
        3. **Cahaya:** Sesuaikan dengan kebutuhan jenis jamur
        4. **Penyiraman:** 2-3x/hari saat fruiting
        
        **Preventif:**
        - Pasang hygrometer untuk monitor kelembaban
        - Buat jadwal penyiraman teratur
        - Ventilasi 4-6x/hari selama 15 menit
        """)
    
    elif problem_category == "Masalah Lingkungan":
        st.markdown("""
        ### 🌡️ Masalah Suhu & Kelembaban
        
        **Suhu Tidak Stabil:**
        - **Terlalu Panas:** Gunakan AC, exhaust fan, atau pindah ke ruangan lebih dingin
        - **Terlalu Dingin:** Gunakan heater, lampu pijar, atau insulasi ruangan
        - **Fluktuasi:** Gunakan thermostat otomatis
        
        **Kelembaban Tidak Stabil:**
        - **Terlalu Kering:** Humidifier, semprot lebih sering, tutup ventilasi sebagian
        - **Terlalu Lembab:** Dehumidifier, buka ventilasi, kurangi penyemprotan
        - **Fluktuasi:** Gunakan humidistat otomatis
        
        **Ventilasi Buruk:**
        - Pasang exhaust fan
        - Buat lubang ventilasi di kumbung
        - Buka pintu 4-6x/hari
        """)
    
    else:  # Masalah Khusus
        st.markdown("""
        ### 🎯 Masalah Khusus per Jenis Jamur
        
        **🍄 Jamur Tiram:**
        - **Pinhead tidak muncul:** Turunkan suhu 5°C, naikkan kelembaban ke 90%
        - **Tudung terlalu kecil:** Kurangi CO2, tambah cahaya
        
        **🍂 Jamur Kuping:**
        - **Tekstur keras:** Kelembaban kurang, semprot lebih sering
        - **Warna gelap:** Normal, tapi jika terlalu gelap berarti terlalu tua
        
        **🍄‍🟫 Jamur Shiitake:**
        - **Tidak fruiting setelah inkubasi:** BUTUH COLD SHOCK! Turunkan suhu dari 25°C ke 10°C selama 48-72 jam
        - **Tudung tidak membuka:** Kelembaban kurang, naikkan ke 90%
        
        **🔘 Jamur Kancing:**
        - **Tidak keluar dari casing:** Casing terlalu tebal/padat, atau pH tidak tepat (harus 7-7.5)
        - **Warna coklat:** Normal untuk cremini/portobello
        
            - **Tidak fruiting:** Suhu harus SANGAT DINGIN (3-13°C), cek AC/cold room
            """)
            
    st.markdown("---")
    st.subheader("� Apotek Alami: Solusi Hama Tanpa Kimia")
    st.caption("Resep pestisida nabati berdasarkan referensi ilmiah untuk budidaya organik.")
    
    with st.expander("🧪 Buka Resep Apotek Alami", expanded=True):
        remedy_cols = st.columns(2)
        
        with remedy_cols[0]:
            st.markdown("### 🌸 1. Lavender & Serai Wangi (Repellent)")
            st.markdown("""
            **Target:** Lalat Buah (Phorid/Sciarid), Nyamuk Jamur.
            **Fungsi:** Mengacaukan navigasi lalat sehingga tidak bertelur di baglog.
            
            **Bahan:**
            - Bunga Lavender kering / Minyak Serai Wangi (Citronella)
            - Air bersih 1 Liter
            - Sabun cair (perekat) sedikittt
            
            **Cara:**
            1. Rebus lavender/serai hingga mendidih (ekstraksi).
            2. Dinginkan, saring ampasnya.
            3. Tambahkan 1-2 tetes sabun cair.
            4. **Semprotkan ke UDARA dan Dinding Kumbung** (JANGAN langsung ke jamur muda, bisa gosong).
            """)
            
            st.markdown("### 🍂 2. Minyak Mimba (Neem Oil)")
            st.markdown("""
            **Target:** Larva Lalat, Tungau (Mites).
            **Fungsi:** *Antifeedant* (bikin hama tidak mau makan) & Gangguan Hormon ganti kulit (IGR).
            
            **Dosis:** 3-5 ml per Liter air.
            **Aplikasi:** Semprot pada rak/lantai saat steril ruangan.
            """)
            
        with remedy_cols[1]:
            st.markdown("### 🥯 3. Baking Soda (Anti-Jamur Liar)")
            st.markdown("""
            **Target:** Jamur liar permukaan, spora trichoderma di udara.
            **Fungsi:** Mengubah pH menjadi basa yang menghambat pertumbuhan jamur kontaminan.
            
            **Dosis:** 1 sendok teh per Liter air.
            **Aplikasi:** Semprot ke dinding/lantai yang berlumut.
            """)
            
            st.markdown("### 🧄 4. Bawang Putih & Cabai")
            st.markdown("""
            **Target:** Serangga umum, kutu.
            **Fungsi:** Pembasmi kontak (panas).
            
            **Cara:** Blender 1 bonggol bawang + 5 cabai + 500ml air. Endapkan semalam. Saring.
            **Aplikasi:** Semprot ke area bawah rak (Hati-hati, bau menyengat bisa mempengaruhi aroma jamur jika terlalu dekat).
            """)

# TAB 10: Extra Tools & Info (Consolidated)
with tab_extra:
    st.header("📚 Informasi Tambahan & Tools Ekstra")
    subtab1, subtab2, subtab3, subtab4 = st.tabs(["📊 Perbandingan", "📚 Referensi Ilmiah", "🧪 Kalkulator Nutrisi", "🚀 Booster ZPT"])

    # SUBTAB 1: Comparison Table
    with subtab1:
        st.subheader("📊 Perbandingan 5 Jenis Jamur")
        
        try:
            comparison_data = []
            for name, data in MUSHROOM_DATA.items():
                comparison_data.append({
                    "Jamur": f"{data['emoji']} {name}",
                    "Kesulitan": data['difficulty'],
                    "Waktu Panen": f"{data['timeline_days'][0]}-{data['timeline_days'][1]} hari",
                    "BE (%)": f"{data['be_percent'][0]}-{data['be_percent'][1]}%",
                    "Harga (Rp/kg)": f"{data['price_min']:,}-{data['price_max']:,}",
                    "Suhu Fruiting": f"{data['temp_fruiting'][0]}-{data['temp_fruiting'][1]}°C",
                    "Kebutuhan Khusus": data['special_req']
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.subheader("🎯 Rekomendasi Berdasarkan Kriteria")
            
            criteria = st.selectbox(
                "Pilih Kriteria Utama Anda",
                ["Pemula (Mudah)", "Profit Maksimal", "Waktu Tercepat", "Lokasi Panas", "Lokasi Dingin"]
            )
            
            if criteria == "Pemula (Mudah)":
                st.success("**Rekomendasi: 🍄 Jamur Tiram**")
                st.markdown("""
                **Alasan:**
                - Paling mudah dan toleran
                - Tidak butuh peralatan khusus
                - Waktu panen relatif cepat (45-60 hari)
                - Harga jual stabil
                - Banyak tutorial dan komunitas
                """)
            
            elif criteria == "Profit Maksimal":
                st.success("**Rekomendasi: 🍄‍🟫 Jamur Shiitake**")
                st.markdown("""
                **Alasan:**
                - Harga tertinggi (Rp 80,000-150,000/kg)
                - Permintaan pasar premium tinggi
                - Margin profit besar meski investasi lebih tinggi
                - Cocok untuk pasar ekspor
                
                **Catatan:** Butuh kesabaran (90-180 hari) dan kontrol suhu ketat
                """)
            
            elif criteria == "Waktu Tercepat":
                st.success("**Rekomendasi: 🍄 Jamur Tiram atau 🍜 Jamur Enoki**")
                st.markdown("""
                **Jamur Tiram:** 45-60 hari (MUDAH)
                
                **Jamur Enoki:** 45-70 hari (SULIT - butuh cold room)
                
                Pilih Tiram jika pemula, Enoki jika sudah punya cold room.
                """)
            
            elif criteria == "Lokasi Panas":
                st.success("**Rekomendasi: 🍂 Jamur Kuping**")
                st.markdown("""
                **Alasan:**
                - Paling toleran terhadap suhu tinggi
                - Cocok untuk dataran rendah (0-700 mdpl)
                - Tidak butuh AC untuk fruiting
                - Harga jual bagus (Rp 30,000-40,000/kg)
                """)
            
            else:  # Lokasi Dingin
                st.success("**Rekomendasi: 🍄‍🟫 Jamur Shiitake atau 🍜 Jamur Enoki**")
                st.markdown("""
                **Dataran Tinggi (>1500 mdpl):**
                - Suhu alami sudah dingin (15-22°C)
                - Cocok untuk shiitake dan enoki
                - Hemat biaya cooling
                - Kualitas jamur lebih bagus
                
                **Shiitake:** Lebih mudah, harga tinggi
                
                **Enoki:** Sangat sulit, butuh 3-13°C
                """)
                
        except Exception as e:
            st.error(f"Gagal memuat Tab Perbandingan: {str(e)}")

    # SUBTAB 2: Scientific References
    with subtab2:
        st.subheader("📚 Referensi Jurnal Ilmiah")
        
        try:
            st.markdown("""
            Modul ini disusun berdasarkan penelitian ilmiah peer-reviewed dari berbagai sumber terpercaya:
            
            ### 🍄 Jamur Tiram (Pleurotus)
            
            1. **Temperature and Humidity Requirements for Oyster Mushroom Cultivation**
            - Source: International Journal of Research and Review (IJRRR)
            - Key Finding: Optimal mycelial growth at 25-30°C, fruiting at 20-28°C
            - [Link](https://www.ijrrr.com)
            
            2. **Effect of Environmental Factors on Pleurotus Species**
            - Source: NIH (National Institutes of Health)
            - DOI: Available at PubMed Central
            - Key Finding: RH 85-95% critical for fruiting body development
            
            3. **Optimization of Oyster Mushroom Production**
            - Source: ResearchGate
            - Key Finding: BE 80-120% achievable with proper substrate formulation
            
            ---
            
            ### � Jamur Kuping (Auricularia)
            
            4. **Auricularia auricula-judae Cultivation Parameters**
            - Source: Mushroom Farm Supplies Australia
            - Key Finding: Optimal fruiting at 15-20°C, humidity 85-95%
            
            5. **Effect of C/N Ratio on Auricularia Growth**
            - Source: MDPI (Multidisciplinary Digital Publishing Institute)
            - Key Finding: C/N 20:1 for mycelium, 30-40:1 for fruiting
            
            6. **Wood Ear Mushroom Environmental Conditions**
            - Source: Korean Science Database
            - Key Finding: pH 5.0-7.0 optimal for substrate
            
            ---
            
            ### 🍄‍🟫 Jamur Shiitake (Lentinus edodes)
            
            7. **Temperature Management in Shiitake Cultivation**
            - Source: Carbon Active Research
            - Key Finding: Cold shock (48-72h from 25°C to 10°C) triggers fruiting
            
            8. **Humidity Control for Premium Shiitake**
            - Source: Gorilla Grow Tent Scientific Studies
            - Key Finding: 85-95% RH during fruiting prevents cap cracking
            
            9. **Shiitake Substrate Optimization**
            - Source: Satrise Agricultural Research
            - Key Finding: Hardwood sawdust + supplements yields best results
            
            ---
            
            ### 🔘 Jamur Kancing (Agaricus bisporus)
            
            10. **Button Mushroom Casing Layer Requirements**
                - Source: National Horticultural Board (NHB), India
                - Key Finding: Casing layer pH 7-7.5, thickness 3-4cm critical
            
            11. **Environmental Conditions for Agaricus Cultivation**
                - Source: ResearchGate
                - Key Finding: Mycelial growth 22-28°C, fruiting 12-20°C
            
            12. **CO2 Management in Button Mushroom Production**
                - Source: OMICS International
                - Key Finding: CO2 <1000-2000 ppm during fruiting
            
            ---
            
            ### 🍜 Jamur Enoki (Flammulina velutipes)
            
            13. **Temperature Requirements for Enoki Mushroom**
                - Source: The Spore Depot
                - Key Finding: Primordia formation at 7-13°C, fruiting 10-16°C
            
            14. **Light and CO2 Effects on Enoki Morphology**
                - Source: CABI Digital Library
                - Key Finding: Low light + high CO2 produces long white stems
            
            15. **Enoki Cultivation in Controlled Environment**
                - Source: Mycoboutique Research
                - Key Finding: 3-5°C produces hardest, best-shaped mushrooms
            """)
        except Exception as e:
            st.error(f"Gagal memuat Tab Referensi: {str(e)}")

    # SUBTAB 3: Premium Baglog Calculator
    with subtab3:
        st.subheader("🧪 Kalkulator Nutrisi Baglog (Premium Formulation)")
        st.info("Gunakan kalkulator ini untuk meracik substrat dengan komposisi nutrisi TERBAIK agar panen maksimal (Biological Efficiency >90%).")
        
        try:
            col_form1, col_form2 = st.columns([1, 1.5])
            
            with col_form1:
                st.markdown("### ⚙️ Input Produksi")
                
                target_basis = st.radio(
                    "Basis Perhitungan",
                    ["Total Berat Adukan (kg)", "Jumlah Baglog (pcs)"]
                )
                
                if target_basis == "Total Berat Adukan (kg)":
                    total_mix_weight = st.number_input("Total Berat Adukan Basah (kg)", 10, 5000, 100, step=10)
                    baglog_size = 1.2
                    est_log_count = int(total_mix_weight / baglog_size)
                    st.caption(f"Estimasi jadi ±{est_log_count} baglog (@1.2kg)")
                else:
                    target_log_count = st.number_input("Target Jumlah Baglog", 10, 5000, 100, step=10)
                    baglog_size = st.number_input("Berat per Baglog (kg)", 0.8, 2.0, 1.2, step=0.1)
                    total_mix_weight = target_log_count * baglog_size
                    st.caption(f"Total adukan dibutuhkan: {total_mix_weight:.1f} kg")

                formula_type = st.selectbox(
                    "Pilih Jenis Formulasi",
                    ["Standard (Ekonomis)", "Super Yield (Premium) 🚀", "Khusus Shiitake (Hardwood)"]
                )
                
                st.markdown("---")
                st.markdown("### 📝 Hasil Perhitungan")
                
                recipe = {}
                tips = ""
                cn_ratio = 50
                
                if formula_type == "Standard (Ekonomis)":
                    dry_mass = total_mix_weight * 0.40
                    water_mass = total_mix_weight * 0.60
                    
                    recipe = {
                        "Serbuk Gergaji": dry_mass * 0.85,
                        "Bekatul": dry_mass * 0.13,
                        "Kapur (CaCO3)": dry_mass * 0.02,
                        "Air Bersih": water_mass
                    }
                    cn_ratio = 50
                    tips = "Cocok untuk Jamur Tiram & Kuping. Murah dan mudah didapat."
                    
                elif formula_type == "Super Yield (Premium) 🚀":
                    dry_mass = total_mix_weight * 0.40
                    water_mass = total_mix_weight * 0.60
                    
                    recipe = {
                        "Serbuk Gergaji": dry_mass * 0.80,
                        "Bekatul": dry_mass * 0.15,
                        "Tepung Jagung": dry_mass * 0.02,
                        "Kapur (CaCO3)": dry_mass * 0.015,
                        "Gypsum": dry_mass * 0.015,
                        "Air Bersih + Molase": water_mass
                    }
                    cn_ratio = 35
                    tips = "Menghasilkan tubuh buah lebih tebal. Gunakan molase 1% dalam air."

                elif formula_type == "Khusus Shiitake (Hardwood)":
                    dry_mass = total_mix_weight * 0.45
                    water_mass = total_mix_weight * 0.55
                    
                    recipe = {
                        "Serbuk Kayu Keras": dry_mass * 0.78,
                        "Bekatul/Gandum": dry_mass * 0.20,
                        "Gypsum": dry_mass * 0.01,
                        "Gula Pasir": dry_mass * 0.01,
                        "Air Bersih": water_mass
                    }
                    cn_ratio = 25
                    tips = "Wajib gunakan serbuk kayu keras! Fermentasi minimal 1-2 hari."

                for item, weight in recipe.items():
                    unit = "Liter" if "Air" in item else "kg"
                    st.metric(item, f"{weight:.2f} {unit}")
                    
                # Seed Calculation
                st.markdown("### 🌱 Estimasi Kebutuhan Bibit (F3)")
                avg_seeds_per_log = 15 # grams
                bottle_weight = 220 # grams (standard glass bottle)
                
                total_seeds_needed_kg = (num_baglogs * avg_seeds_per_log) / 1000
                bottles_needed = (num_baglogs * avg_seeds_per_log) / bottle_weight
                
                col_seed1, col_seed2 = st.columns(2)
                with col_seed1:
                    st.metric("Total Bibit F3", f"{total_seeds_needed_kg:.1f} kg")
                with col_seed2:
                    st.metric("Estimasi Botol", f"{int(bottles_needed)+1} botol", help="Asumsi 1 botol = 220g miselium padat")

            with col_form2:
                st.markdown(f"## 🥣 Panduan Racikan: {formula_type}")
                st.success(f"💡 **Keunggulan:** {tips}")
                st.markdown(f"**Estimasi C/N Ratio: {cn_ratio}:1**")
                
                st.markdown("### 🪵 Rekomendasi Jenis Kayu (Serbuk Gergaji)")
                st.markdown("""
                Kualitas serbuk gergaji menentukan 80% keberhasilan nutrisi:
                
                ✅ **Sangat Disarankan (Hardwood Ringan):**
                - **Sengon (Albasia):** Paling umum, mudah didapat, tekstur pas.
                - **Karet (Rubberwood):** Kandungan nutrisi tinggi, hasil jamur tebal.
                - **Jabon:** Tekstur lunak, miselium cepat merambat.
                
                ⚠️ **Bisa Digunakan (Dicampur):**
                - **Mahoni/Jati:** Keras, sebaiknya dicampur Sengon (1:1). Fermentasi harus matang.
                - **Glugu (Kelapa):** Serat kasar, wajib digiling ulang.
                
                ⛔ **Hindari/Perlakuan Khusus:**
                - **Pinus/Cemara:** Mengandung resin/getah fungisida alami. WAJIB fermentasi >1 bulan atau dikukus lama.
                """)
                
                st.markdown("### 🛠️ Langkah-Langkah Pembuatan:")
                
                steps_text = """
1. **Pengayakan Serbuk:** Ayak serbuk gergaji untuk memisahkan potongan tajam.

2. **Pencampuran Kering:** Campur semua bahan kering secara merata (minimal 3x aduk).

3. **Pemberian Air:** Siram air perlahan sambil diaduk.

4. **Tes Kepal:** Genggam adukan. Tidak boleh menetes (terlalu basah) dan tidak boleh buyar (terlalu kering).

5. **Pembungkusan:** Masukkan ke plastik PP tahan panas, padatkan.

6. **Sterilisasi:** Kukus 95-100°C selama 8 jam atau Autoclave 121°C selama 2 jam.
"""
                st.markdown(steps_text)
                
                st.warning("⛔ **Pantangan:** Jangan pakai serbuk kayu bergetah (pinus) tanpa fermentasi lama.")

            st.markdown("---")
            st.info("💡 **Tips:** Bergabunglah dengan komunitas petani jamur untuk belajar lebih lanjut.")
            
        except Exception as e:
            st.error(f"Gagal memuat Kalkulator Baglog: {str(e)}")

# TAB 11: Pasca Panen & Olahan
with tab_commercial:
    st.header("🍳 Dapur Bisnis: Olahan & Nilai Tambah")
    st.caption("Jangan jual mentah semua! Olah sebagian hasil panen untuk keuntungan berlipat ganda dan daya tahan lebih lama.")
    
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 1])
    
    with res_col1:
        st.subheader("🥣 3 Resep Produk Terlaris")
        
        with st.expander("🍟 1. Keripik Jamur Crispy (Tahan 3-6 Bulan)", expanded=True):
            st.markdown("""
            **Ide Bisnis:** Camilan sehat, oleh-oleh.
            **Nilai Jual:** Rp 60.000 - Rp 100.000 / kg (setara).
            
            **Resep Rahasia:**
            - **Bahan:** Jamur Tiram (suwir, peras kering max), Tepung Beras (70%) + Maizena (30%), Telur (1 butir/kg), Bawang Putih, Ketumbar.
            - **Cara:**
              1. Cuci jamur, **PERAS** sampai benar-benar kering (kunci kerenyahan).
              2. Marinasi dengan bumbu halus 15 menit.
              3. Balur tepung kering (jangan adonan basah).
              4. Goreng *Deep Fry* minyak panas api sedang sampai kuning keemasan.
              5. **Spinner:** Wajib di-spinner untuk buang minyak (agar awet).
            """)
            
        with st.expander("uggets 2. Nugget Jamur Sehat (Frozen Food)", expanded=False):
            st.markdown("""
            **Ide Bisnis:** Bekal anak sekolah, vegetarian.
            **Keunggulan:** Tekstur mirip ayam, sehat.
            
            **Resep:**
            - **Bahan:** Jamur Tiram (kukus, cincang halus), Tahu Putih (hancurkan), Telur, Bawang Bombay, Tepung Panir.
            - **Cara:**
              1. Campur jamur, tahu, telur, bumbu.
              2. Kukus adonan dalam loyang (30 menit).
              3. Dinginkan, potong-potong.
              4. Celup putih telur -> gulingkan tepung panir.
              5. Bekukan di freezer. Siap jual.
            """)
            
        with st.expander("🍲 3. Kaldu Jamur Bubuk (Zero Waste)", expanded=False):
            st.markdown("""
            **Ide Bisnis:** Pengganti MSG, bumbu masak premium.
            **Bahan Baku:** Batang jamur bawah/jamur afkir bentuk (tapi masih segar).
            
            **Cara:**
            1. Iris tipis-tipis semua bagian jamur.
            2. Sangrai (tanpa minyak) atau Oven suhu rendah sampai BENAR-BENAR kering keriuk.
            3. Blender halus jadi bubuk.
            4. Campur: Gula, Garam, Bawang Putih Bubuk, Maizena sangrai (dikit).
            5. Kemas botolan.
            """)

    with res_col2:
        st.subheader("💰 Kalkulator Nilai Tambah (Value Added)")
        st.info("Bandingkan keuntungan jual segar vs jual olahan.")
        
        va_prod = st.selectbox("Pilih Produk Olahan", ["Keripik Jamur", "Nugget Jamur", "Kaldu Bubuk"])
        
        fresh_price_input = st.number_input("Harga Jamur Segar (Rp/kg)", 5000, 50000, 15000, step=1000)
        
        if va_prod == "Keripik Jamur":
            # Rendemen 25% (1kg basah jadi 250g keripik)
            rendemen = 0.25
            pack_size = 100 # gram
            default_sell = 15000 # per pack
        elif va_prod == "Nugget Jamur":
            # Rendemen 120% (karena tambah tepung/tahu)
            rendemen = 1.2
            pack_size = 250 # gram
            default_sell = 25000
        else:
            # Kaldu
            rendemen = 0.1 # 1kg jadi 100g bubuk
            pack_size = 50 # gram
            default_sell = 20000
            
        sell_price_pack = st.number_input(f"Harga Jual per Pack ({pack_size}g) (Rp)", 1000, 100000, default_sell, step=500)
        
        # Calculate
        output_weight = 1000 * rendemen # grams output from 1kg fresh
        num_packs = output_weight / pack_size
        total_revenue = num_packs * sell_price_pack
        
        # Simple COGS assumption (bumbu, minyak, packaging)
        # Assuming processing cost is roughly 30% of revenue (standard F&B)
        proc_cost = total_revenue * 0.3 
        profit_processed = total_revenue - fresh_price_input - proc_cost
        
        profit_fresh = fresh_price_input - 5000 # Asumsi HPP jamur 5000 (dari tab kalkulator)
        
        st.markdown("### 📊 Analisa per 1 Kg Jamur Segar")
        
        col_va1, col_va2 = st.columns(2)
        with col_va1:
            st.metric("Jual Segar (Profit)", f"Rp {profit_fresh:,.0f}", "Margin Tipis")
            st.caption("Resiko: Busuk dalam 24 jam")
            
        with col_va2:
            st.metric(f"Jual {va_prod} (Profit)", f"Rp {profit_processed:,.0f}", f"{profit_processed/fresh_price_input*100:.0f}% Uplift!")
            st.caption(f"Output: {num_packs:.1f} pack @{pack_size}g")
            
        if profit_processed > profit_fresh:
            st.success(f"**Insight:** Mengolah jamur menjadi **{va_prod}** meningkatkan keuntungan **{profit_processed/profit_fresh:.1f}x lipat** dibanding jual segar!")
        else:
            st.warning("Harga jual olahan terlalu rendah atau biaya terlalu tinggi.")
            
    with subtab4:
        st.subheader("🚀 Booster Pertumbuhan & ZPT Alami")
        st.caption("Optimalkan bobot dan kecepatan tumbuh jamur dengan hormon organik (Biostimulant).")
        
        st.markdown("""
        ### 🌿 Formula "Digrow" Alami (Ekstrak Rumput Laut)
        Rumput laut kaya akan **Auxin, Cytokinin, dan Gibberellin** alami serta unsur mikro (Ca, Mg, Fe) yang memacu pembelahan sel jamur.
        
        **Manfaat:**
        - Miselium merambat 20-30% lebih cepat.
        - Tudung jamur lebih tebal & berat (bobot naik).
        - Daya simpan panen lebih lama (karena mineral cukup).
        
        #### 🥣 Resep DIY (Biang ZPT):
        1. **Bahan:**
           - 1 kg Rumput Laut Basah (Sargassum sp. / Gracilaria) - *Cuci bersih garamnya!*
           - 5 Liter Air Kelapa Tua (Sumber Cytokinin + Kalium).
           - 200 ml EM4 Pertanian (Bakteri Pengurai).
           - 500 gram Gula Merah/Molase (Makanan Bakteri).
           
        2. **Cara Buat:**
           - Blender rumput laut dengan 1 liter air kelapa sampai halus (bubur).
           - Masukkan ke wadah tertutup (jrigen/baskom).
           - Tambahkan sisa air kelapa, gula, dan EM4. Aduk rata.
           - **Fermentasi Anaerob (Tutup Rapat):** Selama 14-21 hari.
           - Buka tutup sebentar setiap pagi untuk buang gas.
           - Saring ampasnya. Cairan coklat pekat adalah **BIANG ZPT PREMIUN**.
           
        #### 🚿 Dosis & Aplikasi:
        - **Dosis:** 5 - 10 ml Biang per 1 Liter Air (Jangan berlebih!).
        - **Waktu Semprot:**
           - **Fase Miselium (Inkubasi):** Semprot kabut (mist) ke mulut baglog sekali sebelum kapas ditaruh (hati-hati kontam).
           - **Fase Primordia (Pinhead):** Semprot kabut ke udara kumbung (BUKAN langsung ke jamur) untuk memacu kelembaban bernutrisi.
           - **Habis Panen:** Semprot ke permukaan baglog yang baru dipanen untuk memacu *Flush* berikutnya.
        """)
        
        st.info("💡 **Tips:** Ampas sisa saringan fermentasi bisa dicampur ke media kompos batang jamur (Tab Kalkulator) untuk menambah nutrisi!")


# Footer
st.markdown("---")
st.caption("(c) 2025 AgriSensa Intelligence - Modul Budidaya Jamur Profesional | Data berdasarkan riset ilmiah peer-reviewed")
