import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import requests
import folium
from streamlit_folium import st_folium

# Import AI modules
import sys
sys.path.append('.')
from utils.ai_growth_models import GrowthPredictor, AnomalyDetector, GrowthRateAnalyzer, HarvestPredictor
from utils.health_scoring import HealthScorer, HealthDiagnostics

st.set_page_config(page_title="Pantau Pertumbuhan & AI", page_icon="📈", layout="wide")

# CSS Custom
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .growth-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 2px solid #86efac;
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.1);
    }
    
    .health-gauge {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .status-badge-ok {
        background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
        color: #166534;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-badge-warning {
        background: linear-gradient(135deg, #fef9c3 0%, #fde047 100%);
        color: #854d0e;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-badge-danger {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .weather-widget {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
    }
    
    .recommendation-card {
        background: white;
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .recommendation-card.high {
        border-left-color: #ef4444;
    }
    
    .recommendation-card.medium {
        border-left-color: #f59e0b;
    }
    
    .recommendation-card.low {
        border-left-color: #3b82f6;
    }
    
    .anomaly-alert {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 2px solid #fca5a5;
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .ai-badge {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        display: inline-block;
        margin-left: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Title with AI badge
st.markdown("""
<h1 style="display: inline-block;">📈 Pantau Pertumbuhan</h1>
<span class="ai-badge">🤖 AI-POWERED</span>
""", unsafe_allow_html=True)

st.info("🧠 **AI Analysis Engine** - Monitor perkembangan tanaman dengan machine learning, prediksi pertumbuhan, deteksi anomali, dan rekomendasi cerdas.")

# Initialize session state
if 'growth_data' not in st.session_state:
    st.session_state.growth_data = []

# Standards for Chrysanthemum
STANDARDS = {
    1: {'h': 5, 'l': 4}, 2: {'h': 10, 'l': 6}, 3: {'h': 18, 'l': 9}, 
    4: {'h': 28, 'l': 12}, 5: {'h': 40, 'l': 16}, 6: {'h': 55, 'l': 20},
    7: {'h': 70, 'l': 24}, 8: {'h': 85, 'l': 28}, 9: {'h': 95, 'l': 30},
    10: {'h': 100, 'l': 32}, 11: {'h': 105, 'l': 34}, 12: {'h': 105, 'l': 34}
}

# Weather function
def get_open_meteo_weather(lat, lon):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,rain,surface_pressure,wind_speed_10m&timezone=auto"
        response = requests.get(url, timeout=5)
        data = response.json()
        return data['current']
    except:
        return None

# ==================== SIDEBAR: DATA INPUT ====================
with st.sidebar:
    st.header("📝 Input Data Pemantauan")
    
    # House selection
    if 'house_database' in st.session_state and st.session_state.house_database:
        house_options = [h['name'] for h in st.session_state.house_database.values()]
    else:
        house_options = ["House 1", "House 2", "House 3"]
    
    input_house = st.selectbox("🏠 Pilih House", house_options)
    
    # Tabs for different input methods
    input_tabs = st.tabs(["📊 Single Entry", "📸 Photo Upload", "📝 Batch Entry"])
    
    with input_tabs[0]:
        st.markdown("#### Basic Measurements")
        input_date = st.date_input("📅 Tanggal Cek", datetime.now())
        input_week = st.number_input("📅 Minggu ke- (HST)", 1, 16, 4, help="Hari Setelah Tanam")
        
        col1, col2 = st.columns(2)
        with col1:
            in_height = st.number_input("Tinggi (cm)", 0.0, 150.0, 25.0, step=0.5)
            in_leaves = st.number_input("Jumlah Daun", 0, 50, 12)
        with col2:
            in_diameter = st.number_input("Diameter Batang (mm)", 0.0, 10.0, 4.5, step=0.1)
            in_branches = st.number_input("Jumlah Cabang", 0, 10, 3)
        
        st.markdown("#### Environmental Data")
        
        # Location
        if 'map_lat' not in st.session_state:
            st.session_state.map_lat = -6.80
        if 'map_lon' not in st.session_state:
            st.session_state.map_lon = 107.60
        
        lat = st.number_input("Latitude", value=st.session_state.map_lat, format="%.4f")
        lon = st.number_input("Longitude", value=st.session_state.map_lon, format="%.4f")
        
        st.session_state.map_lat = lat
        st.session_state.map_lon = lon
        
        if st.button("📡 Ambil Data Cuaca"):
            weather = get_open_meteo_weather(lat, lon)
            if weather:
                st.session_state.weather_cache = weather
                st.success("✅ Data cuaca berhasil diambil!")
        
        default_temp = 24.5
        default_humid = 75
        
        if 'weather_cache' in st.session_state:
            w = st.session_state.weather_cache
            default_temp = float(w.get('temperature_2m', 24.5))
            default_humid = int(w.get('relative_humidity_2m', 75))
        
        in_temp = st.number_input("Suhu (°C)", 10.0, 40.0, default_temp, step=0.1)
        in_humidity = st.number_input("Kelembaban (%)", 0, 100, default_humid)
        
        if st.button("💾 Simpan Data", type="primary", use_container_width=True):
            new_record = {
                "house": input_house,
                "date": input_date.strftime("%Y-%m-%d"),
                "week": input_week,
                "height": in_height,
                "leaves": in_leaves,
                "diameter": in_diameter,
                "branches": in_branches,
                "temp": in_temp,
                "humidity": in_humidity
            }
            st.session_state.growth_data.append(new_record)
            st.success("✅ Data berhasil disimpan!")
            st.rerun()
    
    with input_tabs[1]:
        st.markdown("#### Photo Analysis")
        uploaded_file = st.file_uploader("Upload Foto Tanaman", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_file:
            st.image(uploaded_file, caption="Foto Tanaman", use_container_width=True)
            st.info("💡 Fitur analisis foto akan segera tersedia dengan computer vision untuk deteksi kesehatan daun dan penyakit.")
    
    with input_tabs[2]:
        st.markdown("#### Batch Data Entry")
        st.info("📝 Upload CSV dengan kolom: week, height, leaves, diameter, temp, humidity")
        
        batch_file = st.file_uploader("Upload CSV", type=['csv'])
        if batch_file:
            try:
                df_batch = pd.read_csv(batch_file)
                st.dataframe(df_batch.head())
                
                if st.button("Import Batch Data"):
                    for _, row in df_batch.iterrows():
                        new_record = {
                            "house": input_house,
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "week": int(row['week']),
                            "height": float(row['height']),
                            "leaves": int(row['leaves']),
                            "diameter": float(row['diameter']),
                            "branches": row.get('branches', 3),
                            "temp": float(row.get('temp', 24)),
                            "humidity": int(row.get('humidity', 70))
                        }
                        st.session_state.growth_data.append(new_record)
                    st.success(f"✅ {len(df_batch)} records imported!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

# ==================== MAIN CONTENT ====================

# Filter data for selected house
house_data = [d for d in st.session_state.growth_data if d['house'] == input_house]

if not house_data:
    st.warning(f"⚠️ Belum ada data untuk {input_house}. Silakan input data di sidebar.")
    
    # Show example ideal curve
    st.markdown("### 📊 Kurva Pertumbuhan Ideal")
    weeks = list(range(1, 13))
    ideal_heights = [STANDARDS[w]['h'] for w in weeks]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=weeks, y=ideal_heights,
        mode='lines+markers',
        name='Standar Ideal',
        line=dict(color='#94a3b8', width=3),
        marker=dict(size=8)
    ))
    fig.update_layout(
        title="Tinggi Tanaman Ideal (cm)",
        xaxis_title="Minggu ke-",
        yaxis_title="Tinggi (cm)",
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    st.stop()

# Convert to DataFrame
df_house = pd.DataFrame(house_data).sort_values('week')

# ==================== AI ANALYSIS ====================

st.markdown("---")

# Create tabs for different views
main_tabs = st.tabs(["📊 Growth Analysis", "🤖 AI Predictions", "🏥 Health Score", "💡 Recommendations", "📈 Comparative Analytics"])

with main_tabs[0]:
    st.subheader(f"📊 Analisis Pertumbuhan - {input_house}")
    
    # Weather widget
    if 'weather_cache' in st.session_state:
        w = st.session_state.weather_cache
        st.markdown(f"""
        <div class="weather-widget">
            <div style="font-weight:600; font-size:1.1rem; margin-bottom:8px;">🌤️ Cuaca Real-time (Open-Meteo)</div>
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <span style="font-size:2.5rem; font-weight:700;">{w.get('temperature_2m')}°C</span><br>
                    <span style="font-size:0.9rem;">Kelembaban: {w.get('relative_humidity_2m')}%</span>
                </div>
                <div style="text-align:right;">
                    <span>💧 Hujan: {w.get('rain')} mm</span><br>
                    <span>💨 Angin: {w.get('wind_speed_10m')} km/h</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Key metrics
    latest = df_house.iloc[-1]
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📏 Tinggi Terkini", f"{latest['height']:.1f} cm", 
                 delta=f"{latest['height'] - STANDARDS[latest['week']]['h']:.1f} cm vs ideal")
    with col2:
        st.metric("🍃 Jumlah Daun", f"{latest['leaves']}", 
                 delta=f"{latest['leaves'] - STANDARDS[latest['week']]['l']} vs ideal")
    with col3:
        st.metric("📊 Diameter Batang", f"{latest['diameter']:.1f} mm")
    with col4:
        growth_rate = GrowthRateAnalyzer.calculate_growth_rate(df_house)
        avg_rate = np.mean(growth_rate[-2:]) if len(growth_rate) >= 2 else 0
        st.metric("📈 Growth Rate", f"{avg_rate:.1f} cm/week")
    
    # Growth chart with actual vs ideal
    st.markdown("### 📈 Kurva Pertumbuhan")
    
    weeks = list(range(1, 13))
    ideal_heights = [STANDARDS[w]['h'] for w in weeks]
    
    fig_growth = go.Figure()
    
    # Ideal curve
    fig_growth.add_trace(go.Scatter(
        x=weeks, y=ideal_heights,
        mode='lines',
        name='Standar Ideal',
        line=dict(color='#cbd5e1', width=2, dash='dash')
    ))
    
    # Actual data
    fig_growth.add_trace(go.Scatter(
        x=df_house['week'], y=df_house['height'],
        mode='lines+markers',
        name='Aktual',
        line=dict(color='#10b981', width=4),
        marker=dict(size=10, line=dict(width=2, color='white'))
    ))
    
    fig_growth.update_layout(
        title="Tinggi Tanaman vs Standar Ideal",
        xaxis_title="Minggu ke-",
        yaxis_title="Tinggi (cm)",
        height=450,
        hovermode='x unified',
        legend=dict(orientation="h", y=1.1)
    )
    
    st.plotly_chart(fig_growth, use_container_width=True)
    
    # Additional charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Leaves comparison
        fig_leaves = go.Figure()
        ideal_leaves = [STANDARDS[w]['l'] for w in weeks]
        
        fig_leaves.add_trace(go.Bar(
            x=weeks, y=ideal_leaves,
            name='Ideal', marker_color='#e2e8f0'
        ))
        
        actual_leaves_map = dict(zip(df_house['week'], df_house['leaves']))
        actual_leaves = [actual_leaves_map.get(w, 0) for w in weeks]
        
        fig_leaves.add_trace(go.Bar(
            x=weeks, y=actual_leaves,
            name='Aktual', marker_color='#22c55e'
        ))
        
        fig_leaves.update_layout(
            title="Jumlah Daun",
            xaxis_title="Minggu",
            yaxis_title="Helai",
            height=300,
            barmode='group'
        )
        st.plotly_chart(fig_leaves, use_container_width=True)
    
    with col2:
        # Environmental conditions - using separate charts to avoid compatibility issues
        st.markdown("**Kondisi Lingkungan**")
        
        # Temperature chart
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(
            x=df_house['week'], 
            y=df_house['temp'],
            mode='lines+markers',
            name='Suhu',
            line=dict(color='#ef4444', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(239, 68, 68, 0.1)'
        ))
        fig_temp.update_layout(
            yaxis_title="Suhu (°C)",
            xaxis_title="Minggu",
            height=140,
            margin=dict(t=10, b=30, l=50, r=10),
            showlegend=False
        )
        st.plotly_chart(fig_temp, use_container_width=True, key="temp_chart")
        
        # Humidity chart
        fig_humid = go.Figure()
        fig_humid.add_trace(go.Scatter(
            x=df_house['week'], 
            y=df_house['humidity'],
            mode='lines+markers',
            name='Kelembaban',
            line=dict(color='#3b82f6', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(59, 130, 246, 0.1)'
        ))
        fig_humid.update_layout(
            yaxis_title="Kelembaban (%)",
            xaxis_title="Minggu",
            height=140,
            margin=dict(t=10, b=30, l=50, r=10),
            showlegend=False
        )
        st.plotly_chart(fig_humid, use_container_width=True, key="humid_chart")

with main_tabs[1]:
    st.subheader("🤖 AI Growth Prediction")
    
    if len(df_house) >= 3:
        # ML-based prediction
        predictor = GrowthPredictor(degree=3)
        predictor.fit(df_house['week'].values, df_house['height'].values)
        
        current_week = int(df_house['week'].max())
        weeks_ahead = st.slider("Prediksi untuk berapa minggu ke depan?", 1, 8, 4)
        
        prediction_result = predictor.predict(weeks_ahead=weeks_ahead, current_week=current_week)
        
        # Visualization
        fig_pred = go.Figure()
        
        # Historical data
        fig_pred.add_trace(go.Scatter(
            x=df_house['week'], y=df_house['height'],
            mode='markers+lines',
            name='Data Aktual',
            marker=dict(size=10, color='#10b981'),
            line=dict(width=3, color='#10b981')
        ))
        
        # Fitted curve
        fitted_weeks = list(range(1, current_week + 1))
        fitted_heights = predictor.get_fitted_curve(fitted_weeks)
        
        fig_pred.add_trace(go.Scatter(
            x=fitted_weeks, y=fitted_heights,
            mode='lines',
            name='Model Fit',
            line=dict(width=2, color='#059669', dash='dot')
        ))
        
        # Prediction
        pred_weeks = prediction_result['weeks']
        pred_heights = prediction_result['predictions']
        upper_bound = prediction_result['upper_bound']
        lower_bound = prediction_result['lower_bound']
        
        fig_pred.add_trace(go.Scatter(
            x=pred_weeks, y=pred_heights,
            mode='lines+markers',
            name='Prediksi AI',
            line=dict(width=4, color='#8b5cf6', dash='dash'),
            marker=dict(size=12, symbol='diamond')
        ))
        
        # Confidence interval
        fig_pred.add_trace(go.Scatter(
            x=pred_weeks + pred_weeks[::-1],
            y=upper_bound + lower_bound[::-1],
            fill='toself',
            fillcolor='rgba(139, 92, 246, 0.2)',
            line=dict(color='rgba(139, 92, 246, 0)'),
            name='95% Confidence Interval',
            showlegend=True
        ))
        
        # Ideal curve for reference
        all_weeks = list(range(1, max(pred_weeks) + 1))
        ideal_curve = [STANDARDS.get(w, {'h': 105})['h'] for w in all_weeks]
        
        fig_pred.add_trace(go.Scatter(
            x=all_weeks, y=ideal_curve,
            mode='lines',
            name='Standar Ideal',
            line=dict(width=2, color='#cbd5e1', dash='dash')
        ))
        
        fig_pred.update_layout(
            title="🔮 Prediksi Pertumbuhan dengan Machine Learning",
            xaxis_title="Minggu ke-",
            yaxis_title="Tinggi (cm)",
            height=500,
            hovermode='x unified',
            legend=dict(orientation="h", y=-0.15)
        )
        
        st.plotly_chart(fig_pred, use_container_width=True)
        
        # Prediction summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            final_pred = pred_heights[-1]
            st.metric("Prediksi Tinggi Akhir", f"{final_pred:.1f} cm", 
                     delta=f"Week {pred_weeks[-1]}")
        
        with col2:
            # Harvest prediction
            harvest_pred = HarvestPredictor.predict_harvest_date(df_house, target_height=100)
            if harvest_pred['status'] == 'predicted':
                st.metric("Estimasi Panen", f"Minggu {harvest_pred['harvest_week']}", 
                         delta=f"{harvest_pred['confidence']} confidence")
            else:
                st.metric("Estimasi Panen", "Calculating...")
        
        with col3:
            confidence = prediction_result['confidence_interval']
            st.metric("Confidence Interval", f"±{confidence:.1f} cm", 
                     delta="95% CI")
        
        # Growth rate analysis
        st.markdown("### 📊 Analisis Growth Rate")
        
        slowdown = GrowthRateAnalyzer.detect_growth_slowdown(df_house, threshold=3.0)
        
        if slowdown['slowdown']:
            st.warning(f"⚠️ {slowdown['message']}")
            st.markdown("**Rekomendasi:**")
            for rec in slowdown['recommendations']:
                st.markdown(f"- {rec}")
        else:
            st.success(f"✅ {slowdown['message']}")
        
    else:
        st.info("📊 Minimal 3 data point diperlukan untuk prediksi AI. Silakan tambahkan lebih banyak data.")

with main_tabs[2]:
    st.subheader("🏥 Health Score & Diagnostics")
    
    if len(df_house) >= 1:
        # Initialize health scorer
        scorer = HealthScorer(STANDARDS)
        
        latest_data = df_house.iloc[-1].to_dict()
        current_week = int(latest_data['week'])
        
        # Calculate health score
        health_result = scorer.calculate_total_score(
            plant_data=latest_data,
            week=current_week,
            growth_history=df_house.to_dict('records')
        )
        
        # Display health gauge
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Circular gauge
            total_score = health_result['total_score']
            grade = health_result['grade']
            status = health_result['status']
            color = health_result['color']
            
            st.markdown(f"""
            <div class="health-gauge">
                <div class="metric-label">HEALTH SCORE</div>
                <div style="font-size: 4rem; font-weight: 800; color: {color}; margin: 1rem 0;">
                    {total_score}
                </div>
                <div style="font-size: 1.5rem; font-weight: 600; color: {color};">
                    Grade {grade}
                </div>
                <div style="font-size: 1rem; color: #64748b; margin-top: 0.5rem;">
                    {status}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Breakdown bar chart
            breakdown = health_result['breakdown']
            weights = health_result['weights']
            
            categories = list(breakdown.keys())
            scores = list(breakdown.values())
            weight_pct = [weights[k] * 100 for k in categories]
            
            fig_breakdown = go.Figure()
            
            fig_breakdown.add_trace(go.Bar(
                y=[c.capitalize() for c in categories],
                x=scores,
                orientation='h',
                marker=dict(
                    color=scores,
                    colorscale='RdYlGn',
                    cmin=0,
                    cmax=100,
                    showscale=True,
                    colorbar=dict(title="Score")
                ),
                text=[f"{s:.1f} ({w:.0f}%)" for s, w in zip(scores, weight_pct)],
                textposition='auto'
            ))
            
            fig_breakdown.update_layout(
                title="Health Score Breakdown",
                xaxis_title="Score (0-100)",
                yaxis_title="",
                height=300,
                margin=dict(l=0, r=0, t=40, b=0)
            )
            
            st.plotly_chart(fig_breakdown, use_container_width=True)
        
        # Diagnostics
        st.markdown("### 🔬 Diagnostic Analysis")
        
        nutrient_warnings = HealthDiagnostics.diagnose_nutrient_deficiency(
            latest_data, current_week, STANDARDS
        )
        
        env_warnings = HealthDiagnostics.diagnose_environmental_stress(latest_data)
        
        if nutrient_warnings or env_warnings:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🧪 Nutrient Analysis")
                if nutrient_warnings:
                    for warning in nutrient_warnings:
                        severity_color = '#ef4444' if warning['severity'] == 'HIGH' else '#f59e0b'
                        st.markdown(f"""
                        <div style="background: #fef2f2; border-left: 4px solid {severity_color}; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                            <strong style="color: {severity_color};">{warning['nutrient']} Deficiency</strong><br>
                            <small>{warning['symptoms']}</small><br>
                            <strong>Action:</strong> {warning['recommendation']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ No nutrient deficiencies detected")
            
            with col2:
                st.markdown("#### 🌡️ Environmental Stress")
                if env_warnings:
                    for warning in env_warnings:
                        severity_color = '#ef4444' if warning['severity'] == 'HIGH' else '#f59e0b'
                        st.markdown(f"""
                        <div style="background: #fef2f2; border-left: 4px solid {severity_color}; padding: 1rem; border-radius: 8px; margin: 0.5rem 0;">
                            <strong style="color: {severity_color};">{warning['stress_type']}</strong><br>
                            <small>{warning['symptoms']}</small><br>
                            <strong>Action:</strong> {warning['immediate_action']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("✅ No environmental stress detected")
        else:
            st.success("✅ Plant is healthy with no detected issues!")

with main_tabs[3]:
    st.subheader("💡 Smart Recommendations")
    
    if len(df_house) >= 1:
        latest_data = df_house.iloc[-1].to_dict()
        current_week = int(latest_data['week'])
        
        # Get health score
        scorer = HealthScorer(STANDARDS)
        health_result = scorer.calculate_total_score(
            plant_data=latest_data,
            week=current_week,
            growth_history=df_house.to_dict('records')
        )
        
        # Get diagnostics
        nutrient_warnings = HealthDiagnostics.diagnose_nutrient_deficiency(
            latest_data, current_week, STANDARDS
        )
        env_warnings = HealthDiagnostics.diagnose_environmental_stress(latest_data)
        
        diagnostics = {
            'nutrient_warnings': nutrient_warnings,
            'environmental_warnings': env_warnings
        }
        
        # Generate recommendations
        recommendations = HealthDiagnostics.get_health_recommendations(
            health_result, diagnostics
        )
        
        if recommendations:
            for rec in recommendations:
                priority = rec['priority']
                
                if priority == 'CRITICAL':
                    card_class = 'high'
                    priority_badge = '🚨 CRITICAL'
                    badge_color = '#ef4444'
                elif priority == 'HIGH':
                    card_class = 'high'
                    priority_badge = '⚠️ HIGH'
                    badge_color = '#f59e0b'
                elif priority == 'MEDIUM':
                    card_class = 'medium'
                    priority_badge = '📌 MEDIUM'
                    badge_color = '#3b82f6'
                else:
                    card_class = 'low'
                    priority_badge = 'ℹ️ INFO'
                    badge_color = '#10b981'
                
                st.markdown(f"""
                <div class="recommendation-card {card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.5rem;">{rec['icon']}</span>
                        <span style="background: {badge_color}; color: white; padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;">
                            {priority_badge}
                        </span>
                    </div>
                    <div style="font-weight: 600; font-size: 1.1rem; margin-bottom: 0.5rem;">
                        {rec['action']}
                    </div>
                    <div style="color: #64748b; font-size: 0.9rem;">
                        {rec['details']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ No immediate actions needed. Plant is performing well!")
        
        # Harvest timing recommendation
        st.markdown("### 🌾 Harvest Planning")
        
        harvest_window = HarvestPredictor.estimate_harvest_window(df_house, variety='spray')
        
        status = harvest_window['status']
        
        if status == 'READY':
            st.success(f"✅ {harvest_window['message']}")
            st.info(f"📊 Current: Week {harvest_window['current_week']}, Height {harvest_window['current_height']:.1f}cm")
        elif status == 'GROWING':
            st.info(f"🌱 {harvest_window['message']}")
            st.metric("Weeks to Harvest Window", harvest_window['weeks_remaining'])
        else:
            st.warning(f"⚠️ {harvest_window['message']}")

with main_tabs[4]:
    st.subheader("📈 Comparative Analytics")
    
    if len(df_house) >= 3:
        # Anomaly detection
        st.markdown("### 🔍 Anomaly Detection")
        
        detector = AnomalyDetector(contamination=0.15)
        anomaly_result = detector.detect(df_house, STANDARDS)
        
        if anomaly_result['total_anomalies'] > 0:
            st.markdown(f"""
            <div class="anomaly-alert">
                <strong style="color: #991b1b;">⚠️ {anomaly_result['total_anomalies']} Anomalies Detected</strong><br>
                <small>Data points yang menunjukkan pola pertumbuhan tidak normal</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Show anomaly details
            for anomaly in anomaly_result['anomalies']:
                st.warning(f"Week {anomaly['week']}: Height {anomaly['height']:.1f}cm - Severity: {anomaly['severity']}")
            
            # Visualization with anomalies highlighted
            fig_anomaly = go.Figure()
            
            # Normal points
            normal_indices = [i for i in range(len(df_house)) if i not in anomaly_result['anomaly_indices']]
            
            if normal_indices:
                fig_anomaly.add_trace(go.Scatter(
                    x=df_house.iloc[normal_indices]['week'],
                    y=df_house.iloc[normal_indices]['height'],
                    mode='markers+lines',
                    name='Normal',
                    marker=dict(size=10, color='#10b981'),
                    line=dict(width=3, color='#10b981')
                ))
            
            # Anomalous points
            if anomaly_result['anomaly_indices']:
                fig_anomaly.add_trace(go.Scatter(
                    x=df_house.iloc[anomaly_result['anomaly_indices']]['week'],
                    y=df_house.iloc[anomaly_result['anomaly_indices']]['height'],
                    mode='markers',
                    name='Anomaly',
                    marker=dict(size=15, color='#ef4444', symbol='x', line=dict(width=2, color='white'))
                ))
            
            fig_anomaly.update_layout(
                title="Growth Data with Anomaly Detection",
                xaxis_title="Week",
                yaxis_title="Height (cm)",
                height=400
            )
            
            st.plotly_chart(fig_anomaly, use_container_width=True)
        else:
            st.success("✅ No anomalies detected. Growth pattern is consistent.")
        
        # Consistency analysis
        st.markdown("### 📊 Growth Consistency")
        
        consistency_score = GrowthRateAnalyzer.calculate_consistency_score(df_house)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.metric("Consistency Score", f"{consistency_score:.1f}/100")
            
            if consistency_score >= 80:
                st.success("✅ Very consistent growth")
            elif consistency_score >= 60:
                st.info("📊 Moderately consistent")
            else:
                st.warning("⚠️ Inconsistent growth pattern")
        
        with col2:
            # Growth rate over time
            growth_rates = GrowthRateAnalyzer.calculate_growth_rate(df_house)
            
            if growth_rates:
                fig_rate = go.Figure()
                
                rate_weeks = list(range(2, len(growth_rates) + 2))
                
                fig_rate.add_trace(go.Bar(
                    x=rate_weeks,
                    y=growth_rates,
                    marker=dict(
                        color=growth_rates,
                        colorscale='RdYlGn',
                        cmin=0,
                        cmax=max(growth_rates) if growth_rates else 10
                    ),
                    name='Growth Rate'
                ))
                
                # Add average line
                avg_rate = np.mean(growth_rates)
                fig_rate.add_hline(y=avg_rate, line_dash="dash", line_color="blue", 
                                  annotation_text=f"Avg: {avg_rate:.1f} cm/week")
                
                fig_rate.update_layout(
                    title="Week-over-Week Growth Rate",
                    xaxis_title="Week",
                    yaxis_title="Growth Rate (cm/week)",
                    height=300
                )
                
                st.plotly_chart(fig_rate, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.85rem; padding: 1rem;">
    🌸 <strong>Budidaya Krisan Pro</strong> | AI-Powered Growth Monitoring<br>
    <small>Powered by Machine Learning • Real-time Analysis • Smart Recommendations</small>
</div>
""", unsafe_allow_html=True)
