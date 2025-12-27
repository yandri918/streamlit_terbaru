# Rekomendasi Tanaman Cerdas
# ML-based crop recommendation with deep land analysis

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Rekomendasi Tanaman", page_icon="🌱", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== CROP DATABASE ==========
CROP_DATABASE = {
    "Padi": {
        "optimal_conditions": {
            "n_ppm": (2500, 4000), "p_ppm": (15, 25), "k_ppm": (2000, 3500),
            "ph": (5.5, 7.0), "rainfall_mm": (1500, 2000), "temp_c": (24, 30),
            "water_need": "Tinggi"
        },
        "yield_potential": "5-7 ton/ha",
        "market_demand": "Sangat Tinggi",
        "difficulty": "Sedang",
        "season": "Sepanjang tahun (dengan irigasi)",
        "investment": "Sedang",
        "roi_potential": "15-25%",
        "description": "Tanaman pangan utama dengan permintaan stabil"
    },
    "Jagung": {
        "optimal_conditions": {
            "n_ppm": (3000, 5000), "p_ppm": (20, 30), "k_ppm": (2500, 4000),
            "ph": (5.8, 7.0), "rainfall_mm": (1200, 1800), "temp_c": (21, 30),
            "water_need": "Sedang"
        },
        "yield_potential": "6-9 ton/ha",
        "market_demand": "Tinggi",
        "difficulty": "Mudah",
        "season": "Musim kemarau",
        "investment": "Sedang",
        "roi_potential": "20-30%",
        "description": "Tanaman serbaguna untuk pangan dan pakan ternak"
    },
    "Kedelai": {
        "optimal_conditions": {
            "n_ppm": (1500, 3000), "p_ppm": (25, 40), "k_ppm": (2000, 3000),
            "ph": (6.0, 7.0), "rainfall_mm": (1000, 1500), "temp_c": (23, 30),
            "water_need": "Rendah"
        },
        "yield_potential": "2-3 ton/ha",
        "market_demand": "Tinggi",
        "difficulty": "Mudah",
        "season": "Musim kemarau",
        "investment": "Rendah",
        "roi_potential": "25-35%",
        "description": "Tanaman protein nabati dengan permintaan industri tinggi"
    },
    "Cabai Merah": {
        "optimal_conditions": {
            "n_ppm": (3500, 5000), "p_ppm": (25, 35), "k_ppm": (3000, 4500),
            "ph": (6.0, 7.0), "rainfall_mm": (1500, 2500), "temp_c": (24, 28),
            "water_need": "Sedang-Tinggi"
        },
        "yield_potential": "15-20 ton/ha",
        "market_demand": "Sangat Tinggi",
        "difficulty": "Sulit",
        "season": "Sepanjang tahun",
        "investment": "Tinggi",
        "roi_potential": "40-60%",
        "description": "Komoditas bernilai tinggi dengan fluktuasi harga besar"
    },
    "Tomat": {
        "optimal_conditions": {
            "n_ppm": (3000, 4500), "p_ppm": (20, 30), "k_ppm": (2500, 4000),
            "ph": (6.0, 6.8), "rainfall_mm": (1200, 2000), "temp_c": (20, 27),
            "water_need": "Sedang"
        },
        "yield_potential": "25-35 ton/ha",
        "market_demand": "Tinggi",
        "difficulty": "Sedang",
        "season": "Sepanjang tahun",
        "investment": "Tinggi",
        "roi_potential": "35-50%",
        "description": "Sayuran dengan permintaan konsisten dan nilai jual baik"
    },
    "Kentang": {
        "optimal_conditions": {
            "n_ppm": (3500, 5000), "p_ppm": (25, 35), "k_ppm": (3500, 5000),
            "ph": (5.0, 6.5), "rainfall_mm": (1500, 2000), "temp_c": (15, 20),
            "water_need": "Sedang"
        },
        "yield_potential": "20-30 ton/ha",
        "market_demand": "Tinggi",
        "difficulty": "Sedang",
        "season": "Dataran tinggi",
        "investment": "Tinggi",
        "roi_potential": "30-45%",
        "description": "Cocok untuk dataran tinggi dengan suhu sejuk"
    },
    "Bawang Merah": {
        "optimal_conditions": {
            "n_ppm": (2500, 4000), "p_ppm": (20, 30), "k_ppm": (2500, 3500),
            "ph": (6.0, 7.0), "rainfall_mm": (800, 1500), "temp_c": (25, 32),
            "water_need": "Rendah-Sedang"
        },
        "yield_potential": "10-15 ton/ha",
        "market_demand": "Sangat Tinggi",
        "difficulty": "Sedang-Sulit",
        "season": "Musim kemarau",
        "investment": "Tinggi",
        "roi_potential": "50-80%",
        "description": "Komoditas strategis dengan harga fluktuatif tinggi"
    },
    "Singkong": {
        "optimal_conditions": {
            "n_ppm": (1500, 3000), "p_ppm": (10, 20), "k_ppm": (2000, 3000),
            "ph": (5.5, 7.0), "rainfall_mm": (1000, 1500), "temp_c": (25, 30),
            "water_need": "Rendah"
        },
        "yield_potential": "25-35 ton/ha",
        "market_demand": "Sedang",
        "difficulty": "Mudah",
        "season": "Sepanjang tahun",
        "investment": "Rendah",
        "roi_potential": "15-25%",
        "description": "Tanaman tahan kering dengan perawatan minimal"
    }
}

# ========== ML SCORING FUNCTION ==========
def calculate_suitability_score(crop_name, n, p, k, ph, rainfall, temp, water_availability):
    """Calculate suitability score (0-100) for a crop"""
    crop = CROP_DATABASE[crop_name]
    optimal = crop["optimal_conditions"]
    
    def score_parameter(value, optimal_range):
        """Score a parameter based on how close it is to optimal range"""
        min_val, max_val = optimal_range
        optimal_mid = (min_val + max_val) / 2
        optimal_width = max_val - min_val
        
        if min_val <= value <= max_val:
            # Inside optimal range
            distance_from_mid = abs(value - optimal_mid)
            score = 100 - (distance_from_mid / (optimal_width / 2)) * 20
            return max(80, score)
        else:
            # Outside optimal range
            if value < min_val:
                distance = min_val - value
                penalty = min(distance / min_val * 100, 80)
            else:
                distance = value - max_val
                penalty = min(distance / max_val * 100, 80)
            return max(0, 80 - penalty)
    
    # Score each parameter
    n_score = score_parameter(n, optimal["n_ppm"])
    p_score = score_parameter(p, optimal["p_ppm"])
    k_score = score_parameter(k, optimal["k_ppm"])
    ph_score = score_parameter(ph, optimal["ph"])
    rain_score = score_parameter(rainfall, optimal["rainfall_mm"])
    temp_score = score_parameter(temp, optimal["temp_c"])
    
    # Water availability score
    water_needs = {"Rendah": 1, "Rendah-Sedang": 1.5, "Sedang": 2, "Sedang-Tinggi": 2.5, "Tinggi": 3}
    crop_water_need = water_needs[optimal["water_need"]]
    
    water_scores = {"Rendah": 1, "Sedang": 2, "Tinggi": 3}
    available_water = water_scores[water_availability]
    
    if available_water >= crop_water_need:
        water_score = 100
    else:
        water_score = (available_water / crop_water_need) * 100
    
    # Weighted average
    total_score = (
        n_score * 0.20 +
        p_score * 0.15 +
        k_score * 0.15 +
        ph_score * 0.15 +
        rain_score * 0.15 +
        temp_score * 0.10 +
        water_score * 0.10
    )
    
    return {
        'total': round(total_score, 1),
        'breakdown': {
            'Nitrogen': round(n_score, 1),
            'Fosfor': round(p_score, 1),
            'Kalium': round(k_score, 1),
            'pH': round(ph_score, 1),
            'Curah Hujan': round(rain_score, 1),
            'Suhu': round(temp_score, 1),
            'Ketersediaan Air': round(water_score, 1)
        }
    }

# ========== MAIN APP ==========
st.title("🌱 Rekomendasi Tanaman Cerdas")
st.markdown("**Analisis mendalam kondisi lahan untuk rekomendasi tanaman yang optimal**")

# Instructions
with st.expander("📖 Cara Menggunakan", expanded=False):
    st.markdown("""
    **Fitur:**
    - 🤖 Analisis ML untuk 8+ jenis tanaman
    - 📊 Skor kesesuaian (0-100) untuk setiap tanaman
    - 💡 Rekomendasi top 3 tanaman terbaik
    - 📈 Breakdown faktor-faktor penentu
    - 💰 Estimasi ROI dan investasi
    
    **Input yang Diperlukan:**
    1. Data NPK tanah (N, P, K dalam ppm)
    2. pH tanah
    3. Data iklim (curah hujan, suhu)
    4. Ketersediaan air (irigasi)
    
    **Output:**
    - Ranking tanaman berdasarkan kesesuaian
    - Skor detail untuk setiap parameter
    - Rekomendasi improvement
    - Estimasi hasil dan ROI
    """)

# Input Section
st.subheader("📝 Input Kondisi Lahan")

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
        value=20.0,
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
        help="Tingkat keasaman tanah"
    )

with col2:
    st.markdown("**Data Iklim & Air**")
    
    rainfall_mm = st.number_input(
        "Curah Hujan (mm/tahun)",
        min_value=0.0,
        max_value=5000.0,
        value=1500.0,
        step=100.0,
        help="Total curah hujan tahunan"
    )
    
    temp_c = st.number_input(
        "Suhu Rata-rata (°C)",
        min_value=0.0,
        max_value=50.0,
        value=27.0,
        step=0.5,
        help="Suhu rata-rata harian"
    )
    
    water_availability = st.selectbox(
        "Ketersediaan Air/Irigasi",
        ["Rendah", "Sedang", "Tinggi"],
        index=1,
        help="Rendah: tadah hujan, Sedang: irigasi terbatas, Tinggi: irigasi penuh"
    )
    
    area_ha = st.number_input(
        "Luas Lahan (ha)",
        min_value=0.1,
        max_value=1000.0,
        value=1.0,
        step=0.1,
        help="Luas lahan yang tersedia"
    )

# Analyze button
if st.button("🔍 Analisis & Rekomendasikan", type="primary", use_container_width=True):
    
    with st.spinner("Menganalisis kondisi lahan..."):
        # Calculate suitability for all crops
        results = []
        for crop_name in CROP_DATABASE.keys():
            score_data = calculate_suitability_score(
                crop_name, n_ppm, p_ppm, k_ppm, ph, rainfall_mm, temp_c, water_availability
            )
            
            results.append({
                'crop': crop_name,
                'score': score_data['total'],
                'breakdown': score_data['breakdown'],
                'info': CROP_DATABASE[crop_name]
            })
        
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
    
    # Display results
    st.markdown("---")
    st.subheader("🏆 Top 3 Rekomendasi Tanaman")
    
    # Top 3 cards
    cols = st.columns(3)
    medals = ["🥇", "🥈", "🥉"]
    colors = ["#ffd700", "#c0c0c0", "#cd7f32"]
    
    for i, (col, result) in enumerate(zip(cols, results[:3])):
        with col:
            score = result['score']
            crop = result['crop']
            info = result['info']
            
            # Determine suitability level
            if score >= 80:
                suitability = "Sangat Cocok"
                bg_color = "#ecfdf5"
                border_color = "#10b981"
            elif score >= 60:
                suitability = "Cocok"
                bg_color = "#fef3c7"
                border_color = "#f59e0b"
            else:
                suitability = "Kurang Cocok"
                bg_color = "#fee2e2"
                border_color = "#ef4444"
            
            st.markdown(f"""
            <div style="background: {bg_color}; padding: 1.5rem; border-radius: 12px; 
                        border: 2px solid {border_color}; text-align: center;">
                <div style="font-size: 3rem;">{medals[i]}</div>
                <h3 style="margin: 0.5rem 0;">{crop}</h3>
                <div style="font-size: 2rem; font-weight: 700; color: {border_color};">
                    {score}/100
                </div>
                <p style="color: #6b7280; margin: 0.5rem 0;">{suitability}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            **Info Singkat:**
            - Hasil: {info['yield_potential']}
            - ROI: {info['roi_potential']}
            - Kesulitan: {info['difficulty']}
            - Permintaan: {info['market_demand']}
            """)
    
    # Detailed analysis for top recommendation
    st.markdown("---")
    st.subheader(f"📊 Analisis Detail: {results[0]['crop']}")
    
    top_crop = results[0]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Breakdown chart
        breakdown = top_crop['breakdown']
        
        fig = go.Figure(go.Bar(
            x=list(breakdown.keys()),
            y=list(breakdown.values()),
            marker_color=['#3b82f6', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#ec4899', '#14b8a6'],
            text=[f"{v:.1f}" for v in breakdown.values()],
            textposition='auto',
        ))
        
        fig.add_hline(y=80, line_dash="dash", line_color="green", 
                      annotation_text="Optimal (80+)")
        
        fig.update_layout(
            title=f"Breakdown Skor Kesesuaian - {top_crop['crop']}",
            xaxis_title="Parameter",
            yaxis_title="Skor",
            yaxis_range=[0, 105],
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Detail Tanaman:**")
        info = top_crop['info']
        st.write(f"📝 {info['description']}")
        st.write(f"🌾 **Hasil Potensial:** {info['yield_potential']}")
        st.write(f"💰 **ROI Potensial:** {info['roi_potential']}")
        st.write(f"📈 **Permintaan Pasar:** {info['market_demand']}")
        st.write(f"🎯 **Tingkat Kesulitan:** {info['difficulty']}")
        st.write(f"📅 **Musim Tanam:** {info['season']}")
        st.write(f"💵 **Investasi:** {info['investment']}")
    
    # All crops comparison
    st.markdown("---")
    st.subheader("📋 Perbandingan Semua Tanaman")
    
    # Create comparison dataframe
    comparison_data = []
    for result in results:
        comparison_data.append({
            'Tanaman': result['crop'],
            'Skor': f"{result['score']}/100",
            'Hasil Potensial': result['info']['yield_potential'],
            'ROI': result['info']['roi_potential'],
            'Permintaan': result['info']['market_demand'],
            'Kesulitan': result['info']['difficulty']
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True, hide_index=True)
    
    # Recommendations
    st.markdown("---")
    st.subheader("💡 Rekomendasi Aksi")
    
    top_score = results[0]['score']
    
    if top_score >= 80:
        st.success(f"""
        ✅ **Kondisi Sangat Baik untuk {results[0]['crop']}!**
        
        Lahan Anda sangat cocok untuk menanam {results[0]['crop']}. Berikut langkah selanjutnya:
        
        1. **Persiapan Lahan:** Lakukan pengolahan tanah sesuai standar
        2. **Pemupukan:** Gunakan Kalkulator Pupuk untuk dosis yang tepat
        3. **Bibit:** Pilih varietas unggul yang sesuai iklim
        4. **Perawatan:** Ikuti SOP budidaya untuk hasil optimal
        5. **Monitoring:** Catat perkembangan di Database Panen
        """)
    elif top_score >= 60:
        st.info(f"""
        🟡 **Kondisi Cukup Baik untuk {results[0]['crop']}**
        
        Lahan Anda cocok untuk {results[0]['crop']}, namun ada beberapa yang perlu dioptimalkan:
        
        **Parameter yang perlu ditingkatkan:**
        """)
        
        # Show parameters below 70
        for param, score in results[0]['breakdown'].items():
            if score < 70:
                st.write(f"- {param}: {score:.1f}/100 - Perlu improvement")
        
        st.write("""
        **Saran:**
        - Gunakan Analisis NPK untuk rekomendasi pemupukan
        - Pertimbangkan perbaikan drainase/irigasi
        - Konsultasi dengan ahli agronomi
        """)
    else:
        st.warning(f"""
        🔴 **Kondisi Kurang Optimal**
        
        Lahan Anda kurang cocok untuk {results[0]['crop']}. Pertimbangkan:
        
        1. **Pilih tanaman alternatif** dari rekomendasi top 3
        2. **Perbaiki kondisi tanah** terlebih dahulu
        3. **Konsultasi ahli** untuk improvement lahan
        """)
    
    # Financial projection
    st.markdown("---")
    st.subheader("💰 Proyeksi Finansial")
    
    # Simple financial calculation
    top_info = results[0]['info']
    
    # Extract yield range
    yield_range = top_info['yield_potential'].split('-')
    avg_yield = (float(yield_range[0]) + float(yield_range[1].split()[0])) / 2
    total_yield = avg_yield * area_ha
    
    # Estimated price (simplified)
    prices = {
        "Padi": 5000, "Jagung": 4500, "Kedelai": 8000, "Cabai Merah": 45000,
        "Tomat": 8000, "Kentang": 12000, "Bawang Merah": 35000, "Singkong": 2000
    }
    
    price_per_kg = prices.get(results[0]['crop'], 5000)
    revenue = total_yield * 1000 * price_per_kg  # Convert ton to kg
    
    # Extract ROI range
    roi_range = top_info['roi_potential'].split('-')
    avg_roi = (float(roi_range[0]) + float(roi_range[1].rstrip('%'))) / 2 / 100
    
    investment = revenue / (1 + avg_roi)
    profit = revenue - investment
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Hasil Panen", f"{total_yield:.1f} ton")
    with col2:
        st.metric("Pendapatan", f"Rp {revenue:,.0f}")
    with col3:
        st.metric("Keuntungan", f"Rp {profit:,.0f}")
    with col4:
        st.metric("ROI", f"{avg_roi*100:.0f}%")
    
    st.caption("*Proyeksi berdasarkan harga rata-rata dan asumsi kondisi optimal")

# Footer
st.markdown("---")
st.caption("""
🌱 **Rekomendasi Tanaman Cerdas** - Menggunakan machine learning untuk menganalisis kesesuaian 
tanaman berdasarkan kondisi lahan Anda. Untuk hasil terbaik, lakukan uji tanah di laboratorium 
dan konsultasikan dengan ahli agronomi setempat.
""")
