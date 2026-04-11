# 🌤️ Analisis Cuaca & Lingkungan
# Dashboard cuaca khusus pertanian untuk perencanaan budidaya krisan

import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Analisis Cuaca", page_icon="🌤️", layout="wide")

# CSS Custom
st.markdown("""
<style>
    .weather-card-current {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        text-align: center;
    }
    .weather-card-forecast {
        background-color: white;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .metric-main { font-size: 2.5rem; font-weight: bold; }
    .metric-sub { font-size: 1rem; opacity: 0.9; }
    
    .alert-card {
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        border-left: 5px solid;
    }
    .alert-high-temp { background-color: #fef2f2; border-color: #ef4444; color: #991b1b; }
    .alert-humidity { background-color: #eff6ff; border-color: #3b82f6; color: #1e3a8a; }
    .alert-ideal { background-color: #f0fdf4; border-color: #22c55e; color: #166534; }
</style>
""", unsafe_allow_html=True)

st.title("🌤️ Analisis Cuaca & Lingkungan")
st.info("Perencanaan budidaya berbasis data cuaca real-time dan prakiraan 7 hari.")

# --- SIDEBAR LOCATION ---
with st.sidebar:
    st.header("📍 Pilih Lokasi Kebun")
    
    # Initialize lat/lon in session state if not exist
    if 'map_lat' not in st.session_state:
        st.session_state.map_lat = -6.80
    if 'map_lon' not in st.session_state:
        st.session_state.map_lon = 107.60
        
    # --- 1. INTERACTIVE MAP (Render First) ---
    st.caption("Klik pada peta untuk pilih lokasi:")
    with st.expander("🗺️ Peta Lokasi", expanded=True):
        m = folium.Map(location=[st.session_state.map_lat, st.session_state.map_lon], zoom_start=13)
        m.add_child(folium.LatLngPopup()) 
        
        folium.Marker(
            [st.session_state.map_lat, st.session_state.map_lon], 
            popup="Lokasi Kebun", 
            tooltip="Kebun Krisan",
            icon=folium.Icon(color="blue", icon="cloud")
        ).add_to(m)
        
        map_data = st_folium(m, height=200, width=280)

    # Map Click Logic
    if map_data and map_data.get("last_clicked"):
        clicked_lat = map_data["last_clicked"]["lat"]
        clicked_lon = map_data["last_clicked"]["lng"]
        
        # If click detected, update state and RERUN immediately
        if abs(clicked_lat - st.session_state.map_lat) > 0.0001 or abs(clicked_lon - st.session_state.map_lon) > 0.0001:
            st.session_state.map_lat = clicked_lat
            st.session_state.map_lon = clicked_lon
            st.rerun()

    # --- 2. INPUT WIDGETS (Render Second) ---
    # NOTE: We remove 'key' argument to avoid Streamlit Mutation Exception. 
    # The widget value will init from session_state.map_lat each rerun.
    lat = st.number_input("Latitude", value=st.session_state.map_lat, format="%.4f")
    lon = st.number_input("Longitude", value=st.session_state.map_lon, format="%.4f")
    
    # Sync manual input changes back to main state
    # If user types manually, 'lat' will differ from 'st.session_state.map_lat'
    if lat != st.session_state.map_lat or lon != st.session_state.map_lon:
        st.session_state.map_lat = lat
        st.session_state.map_lon = lon
        st.rerun()

# --- WEATHER API FUNCTIONS ---
def get_current_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain,surface_pressure,wind_speed_10m&timezone=auto"
        response = requests.get(url)
        return response.json()['current']
    except Exception: return None

def get_forecast_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max,temperature_2m_min,rain_sum,precipitation_probability_max,wind_speed_10m_max&timezone=auto"
        response = requests.get(url)
        return response.json()['daily']
    except Exception: return None

# --- MAIN CONTENT ---

# 1. Fetch Data
with st.spinner("Mengambil data cuaca..."):
    current = get_current_weather(st.session_state.map_lat, st.session_state.map_lon)
    forecast = get_forecast_weather(st.session_state.map_lat, st.session_state.map_lon)

if current and forecast:
    
    # --- DASHBOARD SUMMARY ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="weather-card-current">
            <div>🌡️ Suhu Saat Ini</div>
            <div class="metric-main">{current['temperature_2m']}°C</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="weather-card-current" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">
            <div>💧 Kelembaban</div>
            <div class="metric-main">{current['relative_humidity_2m']}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        rain_val = current['rain']
        bg_color = "#f59e0b" if rain_val > 0 else "#64748b" # Orange if raining
        st.markdown(f"""
        <div class="weather-card-current" style="background: {bg_color};">
            <div>🌧️ Hujan (Jam Ini)</div>
            <div class="metric-main">{rain_val} mm</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown(f"""
        <div class="weather-card-current" style="background: #6366f1;">
            <div>💨 Kecepatan Angin</div>
            <div class="metric-main">{current['wind_speed_10m']} km/h</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # --- TABS ---
    tab1, tab2, tab3 = st.tabs(["🚦 Rekomendasi & Analisis", "📅 Prakiraan 7 Hari", "📊 Grafik Mikroklimat"])
    
    # TAB 1: REKOMENDASI & ALERTS
    with tab1:
        st.subheader("🤖 Analisis Agroklimat Krisan")
        
        c_alert1, c_alert2 = st.columns(2)
        
        with c_alert1:
            st.markdown("#### 🔥 Stress Panas & Suhu")
            temp = current['temperature_2m']
            
            if temp > 28:
                st.markdown("""
                <div class="alert-card alert-high-temp">
                    <strong>⚠️ PERINGATAN PANAS EKTREM!</strong><br>
                    Suhu di atas 28°C dapat menyebabkan bunga pudar dan batang pendek.<br>
                    <strong>Tindakan:</strong>
                    <ul>
                    <li>Nyalakan sprinkler/kabut (misting) segera.</li>
                    <li>Buka ventilasi samping greenhouse lebar-lebar.</li>
                    <li>Cek kelayuan pada daun muda.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif temp < 15:
                st.markdown("""
                <div class="alert-card alert-humidity">
                     <strong>❄️ SUHU DINGIN</strong><br>
                    Pertumbuhan vegetatif akan melambat.<br>
                    <strong>Tindakan:</strong> Tutup screen/tirai plastik saat malam.
                </div>
                """, unsafe_allow_html=True)
            else:
                 st.markdown("""
                <div class="alert-card alert-ideal">
                    <strong>✅ SUHU IDEAL</strong><br>
                    Kondisi optimal untuk fotosintesis krisan.
                </div>
                """, unsafe_allow_html=True)
                
        with c_alert2:
            st.markdown("#### 🍄 Risiko Jamur (Kelembaban)")
            hum = current['relative_humidity_2m']
            
            if hum > 90:
                st.markdown("""
                <div class="alert-card alert-humidity">
                    <strong>⚠️ RISIKO TINGGI KARAT PUTIH!</strong><br>
                    Kelembaban > 90% memicu spora jamur <i>Puccinia horiana</i>.<br>
                    <strong>Tindakan:</strong>
                    <ul>
                    <li>Kurangi penyiraman (jaga daun tetap kering).</li>
                    <li>Semprot fungisida protektif jika belum terjadwal.</li>
                    <li>Pasang kipas sirkulasi jika ada.</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            elif hum < 50:
                 st.markdown("""
                <div class="alert-card alert-high-temp">
                    <strong>⚠️ UDARA KERING</strong><br>
                    Risiko populasi Tungau (Mites) meledak.<br>
                    <strong>Tindakan:</strong> Basahi lantai greenhouse (tembok/tanah) untuk menaikkan RH.
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="alert-card alert-ideal">
                    <strong>✅ KELEMBABAN OPTIMAL</strong><br>
                    Range 60-80% ideal untuk transpirasi tanaman.
                </div>
                """, unsafe_allow_html=True)
                
        st.markdown("### 🚜 Rencana Kerja Hari Ini (Work Plan)")
        
        rain_prob_today = forecast['precipitation_probability_max'][0]
        wind_max_today = forecast['wind_speed_10m_max'][0]
        
        col_rec1, col_rec2, col_rec3 = st.columns(3)
        
        with col_rec1:
            st.markdown("**🛡️ Penyemprotan (Spraying)**")
            if rain_prob_today > 60:
                st.error(f"⛔ TUNDA. Peluang hujan tinggi ({rain_prob_today}%). Pestisida akan luntur.")
            elif wind_max_today > 15:
                st.warning(f"⚠️ HATI-HATI. Angin kencang ({wind_max_today} km/h). Drift pestisida tinggi.")
            else:
                st.success("✅ DISARANKAN. Cuaca kondusif untuk aplikasi pestisida/pupuk daun.")
                
        with col_rec2:
            st.markdown("**💧 Penyiraman (Irrigation)**")
            if current['rain'] > 5:
                st.info("🌧️ HUJAN. Kurangi volume penyiraman, tanah sudah basah.")
            elif current['temperature_2m'] > 28:
                st.warning("☀️ PANAS. Tambah volume penyiraman +10% atau extra shot siang hari.")
            else:
                st.success("✅ NORMAL. Lakukan jadwal irigasi standar.")
                
        with col_rec3:
            st.markdown("**🌬️ Ventilasi**")
            if current['relative_humidity_2m'] > 85:
                st.warning("⚠️ BUKA PENUH. Turunkan kelembaban untuk cegah jamur.")
            elif current['temperature_2m'] < 18:
                st.info("❄️ TUTUP SEBAGIAN. Jaga kehangatan greenhouse.")
            else:
                st.success("✅ BUKA NORMAL. Sirkulasi udara standar.")

    # TAB 2: PRAKIRAAN 7 HARI
    with tab2:
        st.subheader("📅 Prakiraan Cuaca 7 Hari ke Depan")
        
        daily_data = []
        for i in range(7):
            date_obj = datetime.now() + timedelta(days=i)
            daily_data.append({
                "Tanggal": date_obj.strftime("%d %b"),
                "Suhu Max": forecast['temperature_2m_max'][i],
                "Suhu Min": forecast['temperature_2m_min'][i],
                "Hujan (mm)": forecast['rain_sum'][i],
                "Peluang Hujan (%)": forecast['precipitation_probability_max'][i],
                "Angin (km/h)": forecast['wind_speed_10m_max'][i]
            })
            
        df_daily = pd.DataFrame(daily_data)
        
        # Display as styled dataframe
        st.dataframe(
            df_daily,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Peluang Hujan (%)": st.column_config.ProgressColumn(
                    "Peluang Hujan",
                    format="%d%%",
                    min_value=0,
                    max_value=100,
                ),
                "Suhu Max": st.column_config.NumberColumn(
                    "Suhu Max",
                    format="%.1f°C",
                ),
                "Hujan (mm)": st.column_config.NumberColumn(
                    "Hujan",
                    format="%.1f mm",
                )
            }
        )
        
        # Chart Forecast
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Bar(
            x=df_daily['Tanggal'], y=df_daily['Hujan (mm)'],
            name='Hujan (mm)', marker_color='#3b82f6', yaxis='y2', opacity=0.3
        ))
        fig_forecast.add_trace(go.Scatter(
            x=df_daily['Tanggal'], y=df_daily['Suhu Max'],
            name='Suhu Max', line=dict(color='#ef4444')
        ))
        fig_forecast.add_trace(go.Scatter(
            x=df_daily['Tanggal'], y=df_daily['Suhu Min'],
            name='Suhu Min', line=dict(color='#0ea5e9')
        ))
        
        fig_forecast.update_layout(
            title="Tren Suhu & Hujan Mingguan",
            yaxis=dict(title="Suhu (°C)", side="left"),
            yaxis2=dict(title="Hujan (mm)", side="right", overlaying="y", showgrid=False),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig_forecast, use_container_width=True)

    # TAB 3: MIKROKLIMAT
    with tab3:
        st.subheader("📊 Analisis Kondisi Mikro")
        st.caption("Membandingkan kondisi saat ini dengan range ideal budidaya Krisan.")
        
        c_g1, c_g2 = st.columns(2)
        
        # Gauge Charts using Plotly
        
        # Temp Gauge
        fig_temp = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current['temperature_2m'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Suhu (°C)"},
            delta = {'reference': 24.0, 'increasing': {'color': "red"}, 'decreasing': {'color': "blue"}},
            gauge = {
                'axis': {'range': [0, 50], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 15], 'color': '#93c5fd'},
                    {'range': [15, 28], 'color': '#86efac'}, # Ideal range (Green)
                    {'range': [28, 50], 'color': '#fca5a5'}],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 28}}))
        
        with c_g1:
            st.plotly_chart(fig_temp, use_container_width=True)
            st.info("✅ Ideal: 15-28°C")

        # Humidity Gauge
        fig_hum = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current['relative_humidity_2m'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Kelembaban (%)"},
            delta = {'reference': 75, 'increasing': {'color': "blue"}, 'decreasing': {'color': "orange"}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': '#fca5a5'},
                    {'range': [50, 90], 'color': '#86efac'}, # Ideal range
                    {'range': [90, 100], 'color': '#93c5fd'}], # Too wet
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90}}))

        with c_g2:
            st.plotly_chart(fig_hum, use_container_width=True)
            st.info("✅ Ideal: 50-90%")

else:
    st.error("Gagal mengambil data cuaca. Periksa koneksi internet atau coba lagi nanti.")
