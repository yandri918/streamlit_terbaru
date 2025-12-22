# Peta Data Tanah - Streamlit Version
# Interactive soil map with polygon drawing, NPK data, and weather integration

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import json
import os
import uuid
from datetime import datetime
import requests

# ========== CONFIGURATION ==========
st.set_page_config(
    page_title="Peta Data Tanah - AgriSensa",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== DATA STORAGE ==========
POLYGONS_FILE = "soil_map_polygons.json"
NPK_DATA_FILE = "soil_map_npk_data.json"
MARKERS_FILE = "soil_map_markers.json"

def load_json(filename, default=[]):
    """Load JSON file"""
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return default

def save_json(filename, data):
    """Save JSON file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ========== WEATHER SERVICE ==========
def get_weather_data(lat, lon):
    """Get weather data from Open-Meteo API (free, no API key needed)"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'current': 'temperature_2m,relative_humidity_2m,precipitation,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum',
            'timezone': 'Asia/Jakarta'
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def get_soil_data(lat, lon):
    """Get soil data from Open-Meteo Soil API"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': lat,
            'longitude': lon,
            'hourly': 'soil_temperature_0cm,soil_moisture_0_to_1cm',
            'timezone': 'Asia/Jakarta'
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            # Get latest values
            if 'hourly' in data:
                return {
                    'soil_temperature': data['hourly']['soil_temperature_0cm'][0] if data['hourly']['soil_temperature_0cm'] else None,
                    'soil_moisture': data['hourly']['soil_moisture_0_to_1cm'][0] if data['hourly']['soil_moisture_0_to_1cm'] else None
                }
    except:
        pass
    return None

# ========== NPK ANALYSIS ==========
def analyze_npk(n, p, k):
    """Analyze NPK values (all in ppm)"""
    def classify_value(value, low, high):
        if value < low:
            return "Rendah", "🔴"
        elif value <= high:
            return "Sedang", "🟡"
        else:
            return "Tinggi", "🟢"
    
    # Thresholds in ppm
    # N: 2000-5000 ppm (0.2-0.5%)
    # P: 10-25 ppm
    # K: 2000-4000 ppm (0.2-0.4%)
    n_status, n_icon = classify_value(n, 2000, 5000)
    p_status, p_icon = classify_value(p, 10, 25)
    k_status, k_icon = classify_value(k, 2000, 4000)
    
    return {
        'n': {'value': n, 'status': n_status, 'icon': n_icon, 'unit': 'ppm'},
        'p': {'value': p, 'status': p_status, 'icon': p_icon, 'unit': 'ppm'},
        'k': {'value': k, 'status': k_status, 'icon': k_icon, 'unit': 'ppm'}
    }

def get_fertilizer_recommendation(n, p, k):
    """Get fertilizer recommendations based on NPK (all in ppm)"""
    recommendations = []
    
    if n < 2000:
        recommendations.append("🔹 Tambahkan pupuk Urea (45-0-0) untuk meningkatkan Nitrogen")
    if p < 10:
        recommendations.append("🔹 Tambahkan pupuk SP-36 (0-36-0) untuk meningkatkan Fosfor")
    if k < 2000:
        recommendations.append("🔹 Tambahkan pupuk KCl (0-0-60) untuk meningkatkan Kalium")
    
    if not recommendations:
        recommendations.append("✅ Kandungan NPK sudah baik, lakukan pemeliharaan rutin")
    
    return recommendations

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #059669;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #10b981;
        text-align: center;
    }
    .info-box {
        background: #dbeafe;
        border: 2px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .npk-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 2px solid #e5e7eb;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP ==========
def main():
    # Header
    st.markdown('<h1 class="main-header">🗺️ Peta Data Tanah AgriSensa</h1>', unsafe_allow_html=True)
    st.markdown("**Pemetaan Lahan, Analisis NPK, dan Data Cuaca Terintegrasi**")
    
    # Sidebar
    st.sidebar.title("🗺️ Menu")
    menu = st.sidebar.radio(
        "Pilih Fitur:",
        ["🗺️ Peta Interaktif", "📊 Data NPK", "🌤️ Cuaca & Iklim", "📈 Statistik"]
    )
    
    # Load data
    polygons = load_json(POLYGONS_FILE)
    npk_data = load_json(NPK_DATA_FILE)
    markers = load_json(MARKERS_FILE)
    
    # ========== PAGE: INTERACTIVE MAP ==========
    if menu == "🗺️ Peta Interaktif":
        st.header("🗺️ Peta Interaktif Lahan")
        
        # Instructions
        with st.expander("📖 Cara Menggunakan Peta", expanded=False):
            st.markdown("""
            **Fitur Peta:**
            - 🖱️ **Klik & Drag** untuk menggeser peta
            - 🔍 **Zoom In/Out** dengan scroll atau tombol +/-
            - 📍 **Klik pada peta** untuk menandai lokasi
            - 🗺️ **Draw Tools** untuk menggambar polygon (area lahan)
            
            **Tips:**
            - Gunakan layer control (kanan atas) untuk mengubah tampilan peta
            - Klik marker untuk melihat informasi detail
            - Simpan polygon untuk tracking area lahan Anda
            """)
        
        # Map center (default: Indonesia)
        col1, col2 = st.columns(2)
        with col1:
            center_lat = st.number_input("Latitude Pusat", value=-6.2088, format="%.6f")
        with col2:
            center_lon = st.number_input("Longitude Pusat", value=106.8456, format="%.6f")
        
        # Create map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles=None
        )
        
        # Add tile layers
        folium.TileLayer('OpenStreetMap', name='Street Map').add_to(m)
        folium.TileLayer('Esri.WorldImagery', name='Satellite').add_to(m)
        folium.TileLayer('CartoDB positron', name='Light Map').add_to(m)
        
        # Add existing polygons
        for polygon in polygons:
            coords = polygon.get('coordinates', [])
            if coords:
                # Convert coordinates format if needed
                if isinstance(coords[0], dict):
                    coords = [[c['lat'], c['lng']] for c in coords]
                
                folium.Polygon(
                    locations=coords,
                    popup=f"<b>{polygon['name']}</b><br>Area: {polygon.get('area_sqm', 0):.2f} m²<br>pH: {polygon.get('ph', '-')}",
                    tooltip=polygon['name'],
                    color='#059669',
                    fill=True,
                    fillColor='#10b981',
                    fillOpacity=0.3
                ).add_to(m)
        
        # Add NPK markers
        for npk in npk_data:
            lat = npk.get('latitude')
            lon = npk.get('longitude')
            if lat and lon:
                popup_html = f"""
                <div style="width:200px">
                    <h4>📊 Data NPK</h4>
                    <p><b>N:</b> {npk.get('n_value', '-')} ppm</p>
                    <p><b>P:</b> {npk.get('p_value', '-')} ppm</p>
                    <p><b>K:</b> {npk.get('k_value', '-')} ppm</p>
                    <p><b>pH:</b> {npk.get('ph', '-')}</p>
                </div>
                """
                folium.Marker(
                    location=[lat, lon],
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip="Data NPK",
                    icon=folium.Icon(color='green', icon='leaf', prefix='fa')
                ).add_to(m)
        
        # Add custom markers
        for marker in markers:
            lat = marker.get('latitude')
            lon = marker.get('longitude')
            if lat and lon:
                icon_map = {
                    'water': ('blue', 'tint'),
                    'building': ('red', 'home'),
                    'tree': ('green', 'tree'),
                    'warning': ('orange', 'exclamation-triangle')
                }
                color, icon = icon_map.get(marker.get('type', 'info'), ('blue', 'info'))
                
                folium.Marker(
                    location=[lat, lon],
                    popup=f"<b>{marker['title']}</b><br>{marker.get('description', '')}",
                    tooltip=marker['title'],
                    icon=folium.Icon(color=color, icon=icon, prefix='fa')
                ).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        # Add draw plugin
        from folium.plugins import Draw
        Draw(
            export=True,
            position='topleft',
            draw_options={
                'polyline': False,
                'rectangle': True,
                'polygon': True,
                'circle': False,
                'marker': True,
                'circlemarker': False
            }
        ).add_to(m)
        
        # Display map
        map_data = st_folium(m, width=None, height=600)
        
        # Handle map interactions
        if map_data and map_data.get('last_clicked'):
            clicked = map_data['last_clicked']
            st.success(f"📍 Lokasi diklik: Lat {clicked['lat']:.6f}, Lon {clicked['lng']:.6f}")
            
            # Quick actions
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("🌤️ Lihat Cuaca"):
                    weather = get_weather_data(clicked['lat'], clicked['lng'])
                    if weather and 'current' in weather:
                        st.write(f"🌡️ Suhu: {weather['current']['temperature_2m']}°C")
                        st.write(f"💧 Kelembaban: {weather['current']['relative_humidity_2m']}%")
            
            with col2:
                if st.button("🌱 Tambah Data NPK"):
                    st.session_state['add_npk_lat'] = clicked['lat']
                    st.session_state['add_npk_lon'] = clicked['lng']
                    st.info("Scroll ke bawah untuk input data NPK")
            
            with col3:
                if st.button("📍 Tambah Marker"):
                    st.session_state['add_marker_lat'] = clicked['lat']
                    st.session_state['add_marker_lon'] = clicked['lng']
                    st.info("Scroll ke bawah untuk input marker")
        
        # Add NPK Data Form
        if 'add_npk_lat' in st.session_state:
            st.markdown("---")
            st.subheader("📊 Tambah Data NPK")
            
            with st.form("npk_form"):
                st.info("💡 **Semua nilai NPK dalam satuan ppm (mg/kg)** - sesuai dengan alat ukur standar")
                col1, col2 = st.columns(2)
                with col1:
                    n_value = st.number_input("Nitrogen (ppm)", min_value=0.0, max_value=10000.0, step=10.0, 
                                             help="Range normal: 2000-5000 ppm")
                    p_value = st.number_input("Fosfor (ppm)", min_value=0.0, max_value=100.0, step=1.0,
                                             help="Range normal: 10-25 ppm")
                    k_value = st.number_input("Kalium (ppm)", min_value=0.0, max_value=10000.0, step=10.0,
                                             help="Range normal: 2000-4000 ppm")
                with col2:
                    ph = st.number_input("pH Tanah", min_value=0.0, max_value=14.0, value=7.0, step=0.1,
                                        help="Range ideal: 6.0-7.0")
                    soil_type = st.selectbox("Jenis Tanah", ["Lempung", "Pasir", "Liat", "Humus", "Gambut"])
                    notes = st.text_area("Catatan", placeholder="Contoh: Hasil uji lab tanggal 4 Des 2024")
                
                submitted = st.form_submit_button("💾 Simpan Data NPK")
                
                if submitted:
                    npk_record = {
                        'id': str(uuid.uuid4()),
                        'latitude': st.session_state['add_npk_lat'],
                        'longitude': st.session_state['add_npk_lon'],
                        'n_value': n_value,
                        'p_value': p_value,
                        'k_value': k_value,
                        'ph': ph,
                        'soil_type': soil_type,
                        'notes': notes,
                        'created_at': datetime.now().isoformat()
                    }
                    npk_data.append(npk_record)
                    save_json(NPK_DATA_FILE, npk_data)
                    st.success("✅ Data NPK berhasil disimpan!")
                    del st.session_state['add_npk_lat']
                    del st.session_state['add_npk_lon']
                    st.rerun()
    
    # ========== PAGE: NPK DATA ==========
    elif menu == "📊 Data NPK":
        st.header("📊 Data NPK Tanah")
        
        if not npk_data:
            st.info("Belum ada data NPK. Gunakan peta interaktif untuk menambah data.")
        else:
            # Statistics
            df = pd.DataFrame(npk_data)
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Data", len(npk_data))
            with col2:
                st.metric("Rata-rata N", f"{df['n_value'].mean():.0f} ppm")
            with col3:
                st.metric("Rata-rata P", f"{df['p_value'].mean():.1f} ppm")
            with col4:
                st.metric("Rata-rata K", f"{df['k_value'].mean():.0f} ppm")
            
            st.markdown("---")
            
            # Display data
            for npk in npk_data:
                with st.expander(f"📍 NPK Data - {npk.get('soil_type', 'Unknown')} ({npk['created_at'][:10]})"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Lokasi:** {npk['latitude']:.6f}, {npk['longitude']:.6f}")
                        st.write(f"**Jenis Tanah:** {npk.get('soil_type', '-')}")
                        st.write(f"**pH:** {npk.get('ph', '-')}")
                        if npk.get('notes'):
                            st.write(f"**Catatan:** {npk['notes']}")
                        
                        # NPK Analysis
                        analysis = analyze_npk(npk['n_value'], npk['p_value'], npk['k_value'])
                        st.markdown("**Analisis NPK:**")
                        st.write(f"{analysis['n']['icon']} Nitrogen: {analysis['n']['value']:.0f} ppm ({analysis['n']['status']})")
                        st.write(f"{analysis['p']['icon']} Fosfor: {analysis['p']['value']:.1f} ppm ({analysis['p']['status']})")
                        st.write(f"{analysis['k']['icon']} Kalium: {analysis['k']['value']:.0f} ppm ({analysis['k']['status']})")
                    
                    with col2:
                        # Recommendations
                        st.markdown("**Rekomendasi:**")
                        recs = get_fertilizer_recommendation(npk['n_value'], npk['p_value'], npk['k_value'])
                        for rec in recs:
                            st.write(rec)
                    
                    # Delete button
                    if st.button(f"🗑️ Hapus", key=f"del_npk_{npk['id']}"):
                        npk_data = [n for n in npk_data if n['id'] != npk['id']]
                        save_json(NPK_DATA_FILE, npk_data)
                        st.success("Data dihapus!")
                        st.rerun()
    
    # ========== PAGE: WEATHER ==========
    elif menu == "🌤️ Cuaca & Iklim":
        st.header("🌤️ Data Cuaca & Iklim")
        
        col1, col2 = st.columns(2)
        with col1:
            weather_lat = st.number_input("Latitude", value=-6.2088, format="%.6f", key="weather_lat")
        with col2:
            weather_lon = st.number_input("Longitude", value=106.8456, format="%.6f", key="weather_lon")
        
        if st.button("🔍 Ambil Data Cuaca"):
            with st.spinner("Mengambil data cuaca..."):
                weather = get_weather_data(weather_lat, weather_lon)
                soil = get_soil_data(weather_lat, weather_lon)
                
                if weather and 'current' in weather:
                    st.success("✅ Data cuaca berhasil diambil!")
                    
                    # Current weather
                    st.subheader("🌤️ Cuaca Saat Ini")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("🌡️ Suhu", f"{weather['current']['temperature_2m']}°C")
                    with col2:
                        st.metric("💧 Kelembaban", f"{weather['current']['relative_humidity_2m']}%")
                    with col3:
                        st.metric("🌧️ Curah Hujan", f"{weather['current']['precipitation']} mm")
                    
                    # Soil data
                    if soil:
                        st.subheader("🌱 Data Tanah")
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("🌡️ Suhu Tanah", f"{soil.get('soil_temperature', '-')}°C")
                        with col2:
                            st.metric("💧 Kelembaban Tanah", f"{soil.get('soil_moisture', '-')}%")
                    
                    # Forecast
                    if 'daily' in weather:
                        st.subheader("📅 Prakiraan 7 Hari")
                        forecast_df = pd.DataFrame({
                            'Tanggal': weather['daily']['time'],
                            'Suhu Max (°C)': weather['daily']['temperature_2m_max'],
                            'Suhu Min (°C)': weather['daily']['temperature_2m_min'],
                            'Curah Hujan (mm)': weather['daily']['precipitation_sum']
                        })
                        st.dataframe(forecast_df, use_container_width=True)
                else:
                    st.error("❌ Gagal mengambil data cuaca. Periksa koneksi internet.")
    
    # ========== PAGE: STATISTICS ==========
    elif menu == "📈 Statistik":
        st.header("📈 Statistik Pemetaan")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:2rem;font-weight:700;color:#059669">{len(polygons)}</div>
                <div style="color:#6b7280;font-size:0.9rem;margin-top:0.5rem">Area Lahan</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:2rem;font-weight:700;color:#059669">{len(npk_data)}</div>
                <div style="color:#6b7280;font-size:0.9rem;margin-top:0.5rem">Data NPK</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div style="font-size:2rem;font-weight:700;color:#059669">{len(markers)}</div>
                <div style="color:#6b7280;font-size:0.9rem;margin-top:0.5rem">Marker</div>
            </div>
            """, unsafe_allow_html=True)
        
        if npk_data:
            st.markdown("---")
            st.subheader("📊 Distribusi NPK")
            
            df = pd.DataFrame(npk_data)
            
            # NPK distribution
            col1, col2 = st.columns(2)
            with col1:
                st.bar_chart(df[['n_value', 'p_value', 'k_value']].mean())
            with col2:
                st.line_chart(df[['n_value', 'p_value', 'k_value']])

if __name__ == "__main__":
    main()
