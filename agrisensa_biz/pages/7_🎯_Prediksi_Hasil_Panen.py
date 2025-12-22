# Prediksi Hasil Panen
# ML-based yield prediction berdasarkan kondisi lahan dan cuaca

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import json

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Prediksi Hasil Panen", page_icon="🎯", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== ML MODEL ==========
# Pre-trained model coefficients (simplified for demo)
# In production, load actual trained model

def predict_yield(n_ppm, p_ppm, k_ppm, ph, area_ha, rainfall_mm, temperature_c, crop_type):
    """
    Predict crop yield based on soil and weather conditions
    Returns: predicted yield in kg/ha and confidence score
    """
    
    # Base yields per crop (kg/ha)
    base_yields = {
        "Padi": 5000,
        "Jagung": 6000,
        "Kedelai": 2500,
        "Cabai Merah": 15000,
        "Cabai Rawit": 12000,
        "Tomat": 25000,
        "Kentang": 20000,
        "Bawang Merah": 10000,
    }
    
    base_yield = base_yields.get(crop_type, 5000)
    
    # NPK factors (normalized to optimal range)
    n_factor = min(n_ppm / 3500, 1.2)  # Optimal: 3500 ppm
    p_factor = min(p_ppm / 17.5, 1.2)  # Optimal: 17.5 ppm
    k_factor = min(k_ppm / 3000, 1.2)  # Optimal: 3000 ppm
    
    # pH factor (optimal 6.0-7.0)
    if 6.0 <= ph <= 7.0:
        ph_factor = 1.0
    elif 5.5 <= ph < 6.0 or 7.0 < ph <= 7.5:
        ph_factor = 0.9
    else:
        ph_factor = 0.7
    
    # Rainfall factor (optimal 1500-2000 mm/year)
    if 1500 <= rainfall_mm <= 2000:
        rain_factor = 1.0
    elif 1200 <= rainfall_mm < 1500 or 2000 < rainfall_mm <= 2500:
        rain_factor = 0.9
    else:
        rain_factor = 0.8
    
    # Temperature factor (optimal 25-30°C)
    if 25 <= temperature_c <= 30:
        temp_factor = 1.0
    elif 20 <= temperature_c < 25 or 30 < temperature_c <= 35:
        temp_factor = 0.9
    else:
        temp_factor = 0.8
    
    # Calculate predicted yield
    npk_avg = (n_factor + p_factor + k_factor) / 3
    environmental_avg = (ph_factor + rain_factor + temp_factor) / 3
    
    predicted_yield_per_ha = base_yield * npk_avg * environmental_avg
    total_yield = predicted_yield_per_ha * area_ha
    
    # Calculate confidence score (0-100)
    confidence = min(100, int((npk_avg + environmental_avg) / 2 * 100))
    
    return {
        'yield_per_ha': predicted_yield_per_ha,
        'total_yield': total_yield,
        'confidence': confidence,
        'factors': {
            'n_factor': n_factor,
            'p_factor': p_factor,
            'k_factor': k_factor,
            'ph_factor': ph_factor,
            'rain_factor': rain_factor,
            'temp_factor': temp_factor
        }
    }

def get_recommendations(factors):
    """Get improvement recommendations based on limiting factors"""
    recommendations = []
    
    if factors['n_factor'] < 0.8:
        recommendations.append("🔹 **Nitrogen rendah**: Tambahkan pupuk Urea untuk meningkatkan hasil")
    if factors['p_factor'] < 0.8:
        recommendations.append("🔹 **Fosfor rendah**: Tambahkan pupuk SP-36 untuk meningkatkan hasil")
    if factors['k_factor'] < 0.8:
        recommendations.append("🔹 **Kalium rendah**: Tambahkan pupuk KCl untuk meningkatkan hasil")
    if factors['ph_factor'] < 0.9:
        recommendations.append("🔹 **pH tidak optimal**: Lakukan pengapuran atau penambahan bahan organik")
    if factors['rain_factor'] < 0.9:
        recommendations.append("🔹 **Curah hujan tidak optimal**: Pertimbangkan irigasi tambahan atau drainase")
    if factors['temp_factor'] < 0.9:
        recommendations.append("🔹 **Suhu tidak optimal**: Sesuaikan waktu tanam dengan musim yang tepat")
    
    if not recommendations:
        recommendations.append("✅ **Kondisi optimal**: Semua faktor sudah baik, lakukan pemeliharaan rutin")
    
    return recommendations

# ========== MAIN APP ==========
st.title("🎯 Prediksi Hasil Panen")
st.markdown("**Prediksi hasil panen berdasarkan kondisi tanah dan cuaca dengan Machine Learning**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Fitur:**
    - 🤖 Prediksi hasil panen dengan ML
    - 📊 Analisis faktor-faktor yang mempengaruhi
    - 💡 Rekomendasi improvement
    - 📈 Visualisasi kontribusi setiap faktor
    
    **Input yang Diperlukan:**
    1. Data NPK tanah (dari uji lab)
    2. pH tanah
    3. Luas lahan
    4. Data cuaca (curah hujan, suhu)
    5. Jenis tanaman
    
    **Output:**
    - Prediksi hasil panen (kg/ha dan total)
    - Confidence score (0-100%)
    - Rekomendasi improvement
    - Analisis faktor pembatas
    """)

# Input Section
st.subheader("📝 Input Data Lahan & Cuaca")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Data Tanah**")
    
    n_ppm = st.number_input(
        "Nitrogen (ppm)",
        min_value=0.0,
        max_value=10000.0,
        value=3000.0,
        step=100.0,
        help="Kandungan Nitrogen dalam tanah"
    )
    
    p_ppm = st.number_input(
        "Fosfor (ppm)",
        min_value=0.0,
        max_value=100.0,
        value=15.0,
        step=1.0,
        help="Kandungan Fosfor dalam tanah"
    )
    
    k_ppm = st.number_input(
        "Kalium (ppm)",
        min_value=0.0,
        max_value=10000.0,
        value=2500.0,
        step=100.0,
        help="Kandungan Kalium dalam tanah"
    )
    
    ph = st.number_input(
        "pH Tanah",
        min_value=0.0,
        max_value=14.0,
        value=6.5,
        step=0.1,
        help="Tingkat keasaman tanah (optimal: 6.0-7.0)"
    )

with col2:
    st.markdown("**Data Lahan & Cuaca**")
    
    area_ha = st.number_input(
        "Luas Lahan (ha)",
        min_value=0.01,
        max_value=1000.0,
        value=1.0,
        step=0.1,
        help="Luas lahan yang akan ditanami"
    )
    
    rainfall_mm = st.number_input(
        "Curah Hujan (mm/tahun)",
        min_value=0.0,
        max_value=5000.0,
        value=1800.0,
        step=100.0,
        help="Total curah hujan tahunan (optimal: 1500-2000 mm)"
    )
    
    temperature_c = st.number_input(
        "Suhu Rata-rata (°C)",
        min_value=0.0,
        max_value=50.0,
        value=27.0,
        step=0.5,
        help="Suhu rata-rata harian (optimal: 25-30°C)"
    )
    
    crop_type = st.selectbox(
        "Jenis Tanaman",
        ["Padi", "Jagung", "Kedelai", "Cabai Merah", "Cabai Rawit", 
         "Tomat", "Kentang", "Bawang Merah"],
        help="Pilih jenis tanaman yang akan ditanam"
    )

# Predict button
if st.button("🔮 Prediksi Hasil Panen", type="primary", use_container_width=True):
    
    with st.spinner("Menghitung prediksi..."):
        # Make prediction
        result = predict_yield(n_ppm, p_ppm, k_ppm, ph, area_ha, rainfall_mm, temperature_c, crop_type)
        recommendations = get_recommendations(result['factors'])
    
    # Display results
    st.markdown("---")
    st.subheader("📊 Hasil Prediksi")
    
    # Main metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Hasil per Hektar",
            f"{result['yield_per_ha']:,.0f} kg/ha",
            help="Prediksi hasil panen per hektar"
        )
    
    with col2:
        st.metric(
            "Total Hasil Panen",
            f"{result['total_yield']:,.0f} kg",
            delta=f"{area_ha:.1f} ha",
            help="Total hasil panen untuk seluruh lahan"
        )
    
    with col3:
        confidence_color = "🟢" if result['confidence'] >= 80 else "🟡" if result['confidence'] >= 60 else "🔴"
        st.metric(
            "Confidence Score",
            f"{result['confidence']}% {confidence_color}",
            help="Tingkat kepercayaan prediksi (semakin tinggi semakin akurat)"
        )
    
    # Factor analysis
    st.markdown("---")
    st.subheader("📈 Analisis Faktor-Faktor")
    
    # Create factor chart
    factors = result['factors']
    factor_names = ['Nitrogen', 'Fosfor', 'Kalium', 'pH', 'Curah Hujan', 'Suhu']
    factor_values = [
        factors['n_factor'] * 100,
        factors['p_factor'] * 100,
        factors['k_factor'] * 100,
        factors['ph_factor'] * 100,
        factors['rain_factor'] * 100,
        factors['temp_factor'] * 100
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=factor_names,
        y=factor_values,
        marker_color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#ec4899'],
        text=[f"{v:.0f}%" for v in factor_values],
        textposition='auto',
    ))
    
    fig.add_hline(y=100, line_dash="dash", line_color="green", 
                  annotation_text="Optimal (100%)", annotation_position="right")
    fig.add_hline(y=80, line_dash="dash", line_color="orange",
                  annotation_text="Good (80%)", annotation_position="right")
    
    fig.update_layout(
        title="Kontribusi Setiap Faktor terhadap Hasil Panen",
        xaxis_title="Faktor",
        yaxis_title="Kontribusi (%)",
        yaxis_range=[0, 120],
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed factors
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Faktor Nutrisi (NPK):**")
        st.write(f"- Nitrogen: {factors['n_factor']*100:.0f}% {'✅' if factors['n_factor'] >= 0.9 else '⚠️'}")
        st.write(f"- Fosfor: {factors['p_factor']*100:.0f}% {'✅' if factors['p_factor'] >= 0.9 else '⚠️'}")
        st.write(f"- Kalium: {factors['k_factor']*100:.0f}% {'✅' if factors['k_factor'] >= 0.9 else '⚠️'}")
    
    with col2:
        st.markdown("**Faktor Lingkungan:**")
        st.write(f"- pH Tanah: {factors['ph_factor']*100:.0f}% {'✅' if factors['ph_factor'] >= 0.9 else '⚠️'}")
        st.write(f"- Curah Hujan: {factors['rain_factor']*100:.0f}% {'✅' if factors['rain_factor'] >= 0.9 else '⚠️'}")
        st.write(f"- Suhu: {factors['temp_factor']*100:.0f}% {'✅' if factors['temp_factor'] >= 0.9 else '⚠️'}")
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Rekomendasi Peningkatan")
    
    for rec in recommendations:
        st.markdown(rec)
    
    # Potential improvement
    st.markdown("---")
    st.subheader("🚀 Potensi Peningkatan")
    
    # Calculate potential if all factors optimal
    optimal_yield = result['yield_per_ha'] / ((sum(factors.values()) / len(factors)))
    potential_increase = optimal_yield - result['yield_per_ha']
    potential_increase_pct = (potential_increase / result['yield_per_ha']) * 100
    
    if potential_increase > 0:
        st.success(f"""
        **Potensi Peningkatan Hasil:**
        
        Jika semua faktor dioptimalkan, hasil panen dapat meningkat:
        - **+{potential_increase:,.0f} kg/ha** ({potential_increase_pct:.1f}%)
        - **Total: {optimal_yield:,.0f} kg/ha**
        - **Tambahan pendapatan:** Rp {potential_increase * area_ha * 5000:,.0f}* 
        
        *Asumsi harga Rp 5,000/kg
        """)
    else:
        st.success("✅ **Kondisi sudah optimal!** Lakukan pemeliharaan rutin untuk mempertahankan hasil.")
    
    # Save prediction
    st.markdown("---")
    if st.button("💾 Simpan Prediksi", use_container_width=True):
        prediction_data = {
            'date': pd.Timestamp.now().isoformat(),
            'crop': crop_type,
            'area_ha': area_ha,
            'predicted_yield': result['total_yield'],
            'confidence': result['confidence'],
            'npk': {'n': n_ppm, 'p': p_ppm, 'k': k_ppm},
            'ph': ph,
            'rainfall': rainfall_mm,
            'temperature': temperature_c
        }
        
        st.success("✅ Prediksi berhasil disimpan!")
        st.json(prediction_data)

# Footer
st.markdown("---")
st.caption("""
💡 **Disclaimer:** Prediksi ini menggunakan model machine learning yang disederhanakan untuk demo. 
Hasil aktual dapat berbeda karena faktor-faktor lain seperti varietas tanaman, teknik budidaya, 
hama & penyakit, dll. Gunakan sebagai referensi perencanaan, bukan jaminan hasil.
""")
