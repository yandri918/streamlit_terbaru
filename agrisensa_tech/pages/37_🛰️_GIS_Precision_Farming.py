import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pydeck as pdk
from streamlit_folium import st_folium
import folium
from scipy.interpolate import Rbf

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Soil Command Center v2.0 - AgriSensa",
    page_icon="🛰️",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

# Header
st.title("🛰️ Soil Command Center v2.0")
st.markdown("""
**Advanced Geospatial Intelligence System**
*3D Chemical Mapping | Satellite Analysis | IoT Digital Twin*
""")

# Main tabs
tab_map, tab_3d, tab_analysis, tab_assets = st.tabs([
    "🗺️ Satellite & Zoning",
    "🧊 3D Soil Chemistry",
    "📈 Interpolation Heatmap",
    "🚜 Digital Twin (IoT & Assets)"
])

# UTILS: Generate Geo-Referenced Data
@st.cache_data
def generate_geo_data(lat, lon, points=100, radius_m=200):
    # Generate points around a center lat/lon
    # 1 deg lat ~ 111km
    deg_radius = radius_m / 111000
    
    data = []
    for i in range(points):
        d_lat = np.random.uniform(-deg_radius, deg_radius)
        d_lon = np.random.uniform(-deg_radius, deg_radius)
        
        # Simualte spatial correlation (simple logic)
        dist = np.sqrt(d_lat**2 + d_lon**2)
        norm_dist = dist / deg_radius
        
        # pH pattern (higher in center)
        ph = 5.0 + (2.0 * (1 - norm_dist)) + np.random.normal(0, 0.2)
        ph = np.clip(ph, 4.0, 7.5)
        
        # N pattern (random patches)
        n_ppm = np.random.uniform(20, 100)
        if d_lat > 0: n_ppm += 50 # North side richer
        
        data.append({
            "lat": lat + d_lat,
            "lon": lon + d_lon,
            "ph": ph,
            "n_ppm": n_ppm,
            "k_ppm": np.random.uniform(50, 200),
            "moisture": np.random.uniform(20, 80)
        })
    return pd.DataFrame(data)

# Default Center (Kebun Percobaan IPB / or Generic Farm)
# Lat/Lon for generic Indo farm
CENTER_LAT = -6.5567
CENTER_LON = 106.7303

# DATA LOADER ENGINE
with st.sidebar:
    st.header("📂 Data Source")
    data_source = st.radio("Pilih Sumber Data:", ["Simulasi (Random)", "Upload CSV (Data Asli)"])
    
    df_geo = None
    
    if data_source == "Upload CSV (Data Asli)":
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], help="Format: lat, lon, ph, n_ppm, k_ppm, moisture")
        
        # Download Template Button
        template_csv = "lat,lon,ph,n_ppm,k_ppm,moisture\n-6.5567,106.7303,6.5,120,80,60\n-6.5570,106.7310,5.5,90,70,45"
        st.download_button("⬇️ Download Template CSV", template_csv, "template_gis.csv", "text/csv")
        
        if uploaded_file:
            try:
                df_geo = pd.read_csv(uploaded_file)
                # Validation
                req_cols = ['lat', 'lon', 'ph']
                if not all(col in df_geo.columns for col in req_cols):
                    st.error(f"CSV Error: Wajib memiliki kolom {req_cols}")
                    df_geo = None
                else:
                    st.success(f"✅ Loaded {len(df_geo)} points!")
                    # Update Center
                    CENTER_LAT = df_geo['lat'].mean()
                    CENTER_LON = df_geo['lon'].mean()
                    
                    # Fill missing cols with default
                    if 'n_ppm' not in df_geo.columns: df_geo['n_ppm'] = 50
                    if 'k_ppm' not in df_geo.columns: df_geo['k_ppm'] = 50
                    if 'moisture' not in df_geo.columns: df_geo['moisture'] = 50
                    
            except Exception as e:
                st.error(f"Error reading CSV: {e}")
                
    if df_geo is None:
        # Fallback to simulation
        if data_source == "Upload CSV (Data Asli)":
            st.warning("Menggunakan data simulasi sementara menunggu upload.")
        df_geo = generate_geo_data(CENTER_LAT, CENTER_LON)


# ===== TAB 1: SATELLITE & ZONING (FOLIUM) =====
with tab_map:
    st.header("🗺️ Satellite Ops View")
    
    col_ctrl, col_map = st.columns([1, 3])
    
    with col_ctrl:
        st.subheader("Layer Control")
        map_style = st.selectbox("Base Map", ["Satellite (Esri)", "OpenStreetMap", "Terrain"])
        show_points = st.checkbox("Show Sampling Points", value=True)
        show_heatmap = st.checkbox("Show pH Heatmap Layer", value=False)
        
        st.info("💡 **Tip:** Gunakan Polygon Tool (pojok kiri peta) untuk mengukur luas area tanam baru.")
        
        st.metric("Total Sampling Points", len(df_geo))
        avg_ph = df_geo['ph'].mean()
        st.metric("Avg Soil pH", f"{avg_ph:.1f}", delta=f"{avg_ph-6.0:.1f} vs Ideal")

    with col_map:
        # Initialize Folium Map
        tiles = "OpenStreetMap"
        attr = "OpenStreetMap"
        
        if map_style == "Satellite (Esri)":
            tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            attr = "Esri"
        elif map_style == "Terrain":
            tiles = "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png"
            attr = "OpenTopoMap"
            
        m = folium.Map(location=[CENTER_LAT, CENTER_LON], zoom_start=17, tiles=None)
        folium.TileLayer(tiles=tiles, attr=attr, name=map_style).add_to(m)
        
        # Add Points
        if show_points:
            for idx, row in df_geo.iterrows():
                # Color logic
                color = "green" if row['ph'] >= 6.0 and row['ph'] <= 7.0 else "red"
                folium.CircleMarker(
                    location=[row['lat'], row['lon']],
                    radius=5,
                    color=color,
                    fill=True,
                    fill_opacity=0.7,
                    popup=f"pH: {row['ph']:.1f} | N: {row['n_ppm']:.0f}"
                ).add_to(m)
                
        # Heatmap Layer (Simple)
        if show_heatmap:
            from folium.plugins import HeatMap
            heat_data = [[row['lat'], row['lon'], row['ph']] for index, row in df_geo.iterrows()]
            HeatMap(heat_data, radius=15, blur=10).add_to(m)

        # Draw Control
        from folium.plugins import Draw
        Draw(export=True).add_to(m)
        
        st_folium(m, height=500, use_container_width=True)


# ===== TAB 2: 3D SOIL CHEMISTRY (PYDECK) =====
with tab_3d:
    st.header("🧊 3D Soil Chemical Analysis")
    st.markdown("Visualisasi 3D untuk memetakan konsentrasi nutrisi. **Tinggi Bar = Konsentrasi Nutrisi**, **Warna = Status Kesehatan**.")
    
    param_view = st.selectbox("Pilih Parameter Visualisasi", ["Nitrogen (ppm)", "pH Tanah", "Kelembaban (%)"])
    
    # Map selection to col params
    if param_view == "Nitrogen (ppm)":
        target_col = "n_ppm"
        elevation_scale = 2
        color_exp = "n_ppm > 100 ? [0, 255, 0, 150] : [255, 0, 0, 150]"
    elif param_view == "pH Tanah":
        target_col = "ph"
        elevation_scale = 50
        color_exp = "ph >= 6.0 && ph <= 7.0 ? [0, 255, 0, 150] : [255, 0, 0, 150]"
    else:
        target_col = "moisture"
        elevation_scale = 5
        color_exp = "moisture > 40 ? [0, 0, 255, 150] : [255, 165, 0, 150]"

    # PyDeck Layer
    layer = pdk.Layer(
        "ColumnLayer",
        data=df_geo,
        get_position=["lon", "lat"],
        get_elevation=target_col,
        elevation_scale=elevation_scale,
        radius=10,
        get_fill_color=color_exp,
        pickable=True,
        auto_highlight=True,
    )
    
    # Tooltip
    tooltip = {
        "html": "<b>Lon:</b> {lon}<br/><b>Lat:</b> {lat}<br/><b>Value:</b> {"+target_col+"}",
        "style": {"backgroundColor": "steelblue", "color": "white"}
    }

    # Render Deck
    view_state = pdk.ViewState(
        latitude=CENTER_LAT,
        longitude=CENTER_LON,
        zoom=17,
        pitch=60,
    )
    
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
        map_style="mapbox://styles/mapbox/satellite-v9"
    )
    
    st.pydeck_chart(r)
    
    st.caption("ℹ️ Gunakan **Shift + Drag** untuk memutar sudut pandang peta 3D.")


# ===== TAB 3: INTERPOLATION HEATMAP =====
with tab_analysis:
    st.header("📈 Interpolated Nutrient Map")
    st.markdown("Mengubah data titik sampling diskrit menjadi peta kontur kontinu untuk analisis zona pemupukan (VRA).")
    
    try:
        # RBF Interpolation
        x = df_geo['lon']
        y = df_geo['lat']
        z = df_geo['ph']
        
        # Create grid
        xi = np.linspace(min(x), max(x), 100)
        yi = np.linspace(min(y), max(y), 100)
        xi, yi = np.meshgrid(xi, yi)
        
        # Interpolate
        rbf = Rbf(x, y, z, function='linear')
        zi = rbf(xi, yi)
        
        fig_interp = go.Figure(data=[go.Surface(z=zi, x=xi, y=yi, colorscale='Viridis')])
        fig_interp.update_layout(title='Model Elevasi Nutrisi (Interpolated)', autosize=False,
                          width=800, height=600,
                          scene = dict(aspectratio=dict(x=1, y=1, z=0.5)))
        
        st.plotly_chart(fig_interp, use_container_width=True)
        
        st.success("✅ Model interpolasi berhasil dibuat. Zona lembah menunjukan nilai rendah.")
        
    except Exception as e:
        st.error(f"Error interpolation: {e}")


# ===== TAB 4: DIGITAL TWIN =====
with tab_assets:
    st.header("🚜 Digital Twin & Asset Tracking")
    
    col_a1, col_a2 = st.columns([1, 1])
    
    with col_a1:
        st.subheader("📡 Live Sensor Readings")
        # Dummy Live Data
        st.metric("Node A1 (Soil)", "pH 6.2", "Active")
        st.metric("Node A2 (Weather)", "32°C / 60% RH", "Active")
        st.metric("Node B1 (Pump)", "OFF", "Standby")
        
    with col_a2:
        st.subheader("🚜 Machinery Status")
        st.dataframe(pd.DataFrame({
            "Asset": ["Tractor John Deere", "Drone DJI Agras", "Pump Station 1"],
            "Status": ["Field B - Plowing", "Gudang - Charging", "Idle"],
            "Operator": ["Pak Budi", "-", "-"]
        }))
    
    st.divider()
    st.subheader("🗺️ 3D Flight Path (Drone Mission)")
    
    # Simulate flight path
    path_data = []
    alt = 30
    for i in range(10):
        path_data.append([CENTER_LON + (i*0.0001), CENTER_LAT, alt])
        path_data.append([CENTER_LON + (i*0.0001), CENTER_LAT + 0.001, alt])
        
    df_path = pd.DataFrame({'path': [path_data]})
    
    layer_path = pdk.Layer(
        "PathLayer",
        df_path,
        get_path="path",
        get_color=[255, 255, 0],
        width_scale=20,
        width_min_pixels=2,
    )
    
    view_state_drone = pdk.ViewState(latitude=CENTER_LAT, longitude=CENTER_LON, zoom=16, pitch=45)
    
    st.pydeck_chart(pdk.Deck(layers=[layer_path], initial_view_state=view_state_drone))

st.sidebar.info("AgriSensa GIS v2.0 - Powered by PyDeck & Folium")
