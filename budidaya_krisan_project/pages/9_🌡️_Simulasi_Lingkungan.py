# 🌡️ Monitor Lingkungan Krisan
# Parameter checker untuk budidaya optimal

import streamlit as st
import plotly.graph_objects as go
import requests

st.set_page_config(page_title="Monitor Lingkungan", page_icon="🌡️", layout="wide")

# CSS
st.markdown("""
<style>
    .param-optimal { background: #d1fae5; color: #065f46; padding: 1rem; border-radius: 12px; text-align: center; }
    .param-warning { background: #fef3c7; color: #92400e; padding: 1rem; border-radius: 12px; text-align: center; }
    .param-critical { background: #fee2e2; color: #991b1b; padding: 1rem; border-radius: 12px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🌡️ Monitor & Analisis Parameter Lingkungan")
st.info("Masukkan kondisi lingkungan Anda untuk mendapatkan rekomendasi penyesuaian.")

# OPTIMAL PARAMETERS untuk Krisan Spray
KRISAN_PARAMS = {
    "vegetatif": {
        "temp_min": 18, "temp_max": 26, "temp_opt": 22,
        "hum_min": 60, "hum_max": 80,
        "light_hours": 16,
        "phase_name": "Vegetatif (Hari Panjang)"
    },
    "generatif": {
        "temp_min": 15, "temp_max": 24, "temp_opt": 20,
        "hum_min": 60, "hum_max": 70,
        "light_hours": 10,
        "phase_name": "Generatif (Hari Pendek)"
    }
}

# Input Section
col_input, col_result = st.columns([1, 1.5])

with col_input:
    st.subheader("📝 Input Parameter")
    
    phase = st.radio(
        "Fase Pertumbuhan",
        ["vegetatif", "generatif"],
        format_func=lambda x: KRISAN_PARAMS[x]["phase_name"]
    )
    
    current_temp = st.slider("🌡️ Suhu Aktual (°C)", 10, 40, 24)
    current_humidity = st.slider("💧 Kelembaban Aktual (%)", 30, 100, 70)
    current_altitude = st.number_input("🏔️ Ketinggian Lokasi (mdpl)", 0, 3000, 1000, step=100)
    has_greenhouse = st.checkbox("🏠 Menggunakan Greenhouse", value=True)

with col_result:
    st.subheader("📊 Analisis Parameter")
    
    params = KRISAN_PARAMS[phase]
    
    # Temperature Check
    if params["temp_min"] <= current_temp <= params["temp_max"]:
        if abs(current_temp - params["temp_opt"]) <= 2:
            temp_status = "optimal"
            temp_class = "param-optimal"
            temp_icon = "✅"
        else:
            temp_status = "acceptable"
            temp_class = "param-warning"
            temp_icon = "⚠️"
    else:
        temp_status = "critical"
        temp_class = "param-critical"
        temp_icon = "❌"
    
    # Humidity Check
    if params["hum_min"] <= current_humidity <= params["hum_max"]:
        hum_status = "optimal"
        hum_class = "param-optimal"
        hum_icon = "✅"
    elif abs(current_humidity - params["hum_min"]) <= 10 or abs(current_humidity - params["hum_max"]) <= 10:
        hum_status = "acceptable"
        hum_class = "param-warning"
        hum_icon = "⚠️"
    else:
        hum_status = "critical"
        hum_class = "param-critical"
        hum_icon = "❌"
    
    # Altitude Check
    if 800 <= current_altitude <= 1500:
        alt_status = "optimal"
        alt_class = "param-optimal"
        alt_icon = "✅"
    elif 500 <= current_altitude <= 2000:
        alt_status = "acceptable"
        alt_class = "param-warning"
        alt_icon = "⚠️"
    else:
        alt_status = "critical"
        alt_class = "param-critical"
        alt_icon = "❌"
    
    # Display Results
    r1, r2, r3 = st.columns(3)
    
    with r1:
        st.markdown(f"""
        <div class="{temp_class}">
            <div style="font-size: 2rem;">{temp_icon}</div>
            <strong>Suhu</strong><br>
            {current_temp}°C<br>
            <small>Optimal: {params['temp_opt']}°C</small>
        </div>
        """, unsafe_allow_html=True)
    
    with r2:
        st.markdown(f"""
        <div class="{hum_class}">
            <div style="font-size: 2rem;">{hum_icon}</div>
            <strong>Kelembaban</strong><br>
            {current_humidity}%<br>
            <small>Optimal: {params['hum_min']}-{params['hum_max']}%</small>
        </div>
        """, unsafe_allow_html=True)
    
    with r3:
        st.markdown(f"""
        <div class="{alt_class}">
            <div style="font-size: 2rem;">{alt_icon}</div>
            <strong>Ketinggian</strong><br>
            {current_altitude} mdpl<br>
            <small>Optimal: 800-1500 mdpl</small>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# Recommendations
st.subheader("💡 Rekomendasi Penyesuaian")

recommendations = []

# Temperature recommendations
if temp_status == "critical":
    if current_temp < params["temp_min"]:
        recommendations.append(f"🔥 **Suhu terlalu rendah!** Gunakan heater atau tutup ventilasi greenhouse. Target: {params['temp_min']}-{params['temp_max']}°C")
    else:
        recommendations.append(f"❄️ **Suhu terlalu tinggi!** Tingkatkan ventilasi, gunakan shade net 40%, atau exhaust fan. Target: {params['temp_min']}-{params['temp_max']}°C")
elif temp_status == "acceptable":
    recommendations.append(f"⚠️ Suhu bisa lebih optimal di **{params['temp_opt']}°C** untuk pertumbuhan maksimal.")

# Humidity recommendations
if hum_status == "critical":
    if current_humidity < params["hum_min"]:
        recommendations.append(f"💧 **Kelembaban terlalu rendah!** Gunakan misting system atau siram lantai greenhouse.")
    else:
        recommendations.append(f"🌊 **Kelembaban terlalu tinggi!** Buka ventilasi, kurangi penyiraman, waspadai penyakit jamur!")

# Altitude recommendations
if alt_status != "optimal":
    if current_altitude < 800:
        recommendations.append(f"🏔️ **Lokasi terlalu rendah.** Perlu investasi cooling system (AC/cooler) untuk budidaya krisan berkualitas tinggi.")
    elif current_altitude > 1500:
        recommendations.append(f"⛰️ **Lokasi sangat tinggi.** Bagus untuk kualitas, tapi pertumbuhan mungkin lambat. Tambahkan heating di malam hari.")

# Greenhouse recommendation
if not has_greenhouse:
    recommendations.append("🏠 **Sangat disarankan menggunakan greenhouse** untuk kontrol hari pendek (plastik hitam) dan perlindungan dari hujan.")

if recommendations:
    for rec in recommendations:
        st.warning(rec)
else:
    st.success("✅ **Semua parameter sudah OPTIMAL!** Pertahankan kondisi ini untuk hasil terbaik.")

# Gauge Visualization
st.markdown("---")
st.subheader("📈 Visualisasi Parameter")

fig = go.Figure()

# Temperature Gauge
fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=current_temp,
    domain={'x': [0, 0.45], 'y': [0, 1]},
    title={'text': "Suhu (°C)"},
    delta={'reference': params['temp_opt']},
    gauge={
        'axis': {'range': [10, 40]},
        'bar': {'color': "#ec4899"},
        'steps': [
            {'range': [10, params['temp_min']], 'color': "#fecdd3"},
            {'range': [params['temp_min'], params['temp_max']], 'color': "#86efac"},
            {'range': [params['temp_max'], 40], 'color': "#fecdd3"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': params['temp_opt']
        }
    }
))

# Humidity Gauge
fig.add_trace(go.Indicator(
    mode="gauge+number+delta",
    value=current_humidity,
    domain={'x': [0.55, 1], 'y': [0, 1]},
    title={'text': "Kelembaban (%)"},
    delta={'reference': (params['hum_min'] + params['hum_max']) / 2},
    gauge={
        'axis': {'range': [30, 100]},
        'bar': {'color': "#3b82f6"},
        'steps': [
            {'range': [30, params['hum_min']], 'color': "#bfdbfe"},
            {'range': [params['hum_min'], params['hum_max']], 'color': "#86efac"},
            {'range': [params['hum_max'], 100], 'color': "#bfdbfe"}
        ]
    }
))

fig.update_layout(height=300)
st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Monitor Lingkungan")
