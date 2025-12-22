# Rekomendasi Pupuk Terpadu
# Unified fertilizer recommendation with 4 methods: Basic, AI Advanced, BWD Leaf Analysis, and Decision Theory

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image
import cv2
from datetime import datetime

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Rekomendasi Pupuk Terpadu", page_icon="🎯", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== HELPER FUNCTIONS ==========

def calculate_basic_fertilizer(crop, area_ha):
    """Basic fertilizer calculation"""
    requirements = {
        "Padi": {"N": 120, "P": 60, "K": 60},
        "Jagung": {"N": 200, "P": 90, "K": 60},
        "Cabai Merah": {"N": 180, "P": 120, "K": 150},
        "Tomat": {"N": 150, "P": 100, "K": 120},
    }
    
    req = requirements.get(crop, {"N": 120, "P": 60, "K": 60})
    
    return {
        'N': req['N'] * area_ha,
        'P': req['P'] * area_ha,
        'K': req['K'] * area_ha
    }

def ai_advanced_recommendation(crop, n_ppm, p_ppm, k_ppm, ph, area_ha):
    """AI-based advanced recommendation"""
    # Optimal NPK levels
    optimal = {
        "Padi": {"N": 3500, "P": 20, "K": 3000},
        "Jagung": {"N": 4000, "P": 25, "K": 3500},
        "Cabai Merah": {"N": 4500, "P": 30, "K": 4000},
        "Tomat": {"N": 4000, "P": 25, "K": 3500},
    }
    
    opt = optimal.get(crop, {"N": 3500, "P": 20, "K": 3000})
    
    # Calculate deficiency (convert ppm to kg/ha, rough approximation)
    n_deficit = max(0, (opt['N'] - n_ppm) * 2 / 1000) * area_ha
    p_deficit = max(0, (opt['P'] - p_ppm) * 2 / 1000) * area_ha
    k_deficit = max(0, (opt['K'] - k_ppm) * 2 / 1000) * area_ha
    
    # pH adjustment factor
    if 6.0 <= ph <= 7.0:
        ph_factor = 1.0
    elif 5.5 <= ph < 6.0 or 7.0 < ph <= 7.5:
        ph_factor = 1.2
    else:
        ph_factor = 1.5
    
    # Adjust for pH
    n_needed = n_deficit * ph_factor
    p_needed = p_deficit * ph_factor
    k_needed = k_deficit * ph_factor
    
    # Calculate fertilizer amounts
    urea = (n_needed / 0.46)  # Urea 46% N
    sp36 = (p_needed / 0.36)  # SP-36 36% P
    kcl = (k_needed / 0.60)   # KCl 60% K
    
    return {
        'npk_needed': {'N': n_needed, 'P': p_needed, 'K': k_needed},
        'fertilizers': {'Urea': urea, 'SP-36': sp36, 'KCl': kcl},
        'soil_status': {
            'N': 'Cukup' if n_ppm >= opt['N'] * 0.8 else 'Kurang',
            'P': 'Cukup' if p_ppm >= opt['P'] * 0.8 else 'Kurang',
            'K': 'Cukup' if k_ppm >= opt['K'] * 0.8 else 'Kurang',
            'pH': 'Optimal' if 6.0 <= ph <= 7.0 else 'Perlu Penyesuaian'
        }
    }

def analyze_bwd_leaf(image):
    """
    BWD (Brown-White-Disease) Leaf Analysis
    Analyzes leaf image for brown spots, white spots, and overall health
    """
    # Convert PIL to CV2
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
    
    # Define color ranges
    # Brown spots (disease)
    brown_lower = np.array([10, 50, 20])
    brown_upper = np.array([30, 255, 200])
    brown_mask = cv2.inRange(hsv, brown_lower, brown_upper)
    
    # White spots (fungal/bacterial)
    white_lower = np.array([0, 0, 200])
    white_upper = np.array([180, 30, 255])
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    
    # Green (healthy)
    green_lower = np.array([35, 40, 40])
    green_upper = np.array([85, 255, 255])
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    
    # Calculate percentages
    total_pixels = img_cv.shape[0] * img_cv.shape[1]
    brown_percent = (cv2.countNonZero(brown_mask) / total_pixels) * 100
    white_percent = (cv2.countNonZero(white_mask) / total_pixels) * 100
    green_percent = (cv2.countNonZero(green_mask) / total_pixels) * 100
    
    # Calculate BWD score (0-100, higher is healthier)
    bwd_score = max(0, 100 - (brown_percent * 3) - (white_percent * 2))
    
    # Determine health status
    if bwd_score >= 80:
        health_status = "Sehat"
        severity = "None"
    elif bwd_score >= 60:
        health_status = "Sedikit Terinfeksi"
        severity = "Low"
    elif bwd_score >= 40:
        health_status = "Terinfeksi Sedang"
        severity = "Medium"
    else:
        health_status = "Terinfeksi Parah"
        severity = "High"
    
    # Detect disease type
    disease_detected = []
    if brown_percent > 5:
        disease_detected.append("Bercak Coklat (Brown Spot)")
    if white_percent > 3:
        disease_detected.append("Hawar Daun (Leaf Blight)")
    if green_percent < 30:
        disease_detected.append("Defisiensi Nutrisi")
    
    return {
        'bwd_score': bwd_score,
        'health_status': health_status,
        'severity': severity,
        'brown_percent': brown_percent,
        'white_percent': white_percent,
        'green_percent': green_percent,
        'diseases': disease_detected if disease_detected else ["Tidak ada penyakit terdeteksi"],
        'recommendation': get_bwd_recommendation(bwd_score, brown_percent, white_percent)
    }

def get_bwd_recommendation(score, brown, white):
    """Get fertilizer recommendation based on BWD analysis"""
    recommendations = {
        'fertilizer_adjustment': [],
        'treatment': [],
        'prevention': []
    }
    
    if score < 60:
        # Stressed plant needs recovery
        recommendations['fertilizer_adjustment'] = [
            "Kurangi dosis nitrogen 20-30%",
            "Tingkatkan kalium untuk ketahanan",
            "Tambahkan pupuk organik untuk recovery"
        ]
    
    if brown > 5:
        recommendations['treatment'] = [
            "Aplikasi fungisida berbahan Mancozeb",
            "Semprot setiap 7 hari",
            "Buang daun terinfeksi parah"
        ]
    
    if white > 3:
        recommendations['treatment'].append(
            "Aplikasi bakterisida berbahan tembaga"
        )
    
    recommendations['prevention'] = [
        "Perbaiki drainase",
        "Jarak tanam teratur",
        "Pemupukan berimbang"
    ]
    
    return recommendations

def calculate_decision_matrix(crop, area_ha, user_weights=None):
    """
    Multi-Attribute Utility Theory (MAUT) for fertilization strategy selection
    Criteria: Cost, Effectiveness, Risk, Environmental Impact
    """
    # Default weights (can be adjusted by user)
    if user_weights is None:
        weights = {
            'cost': 0.30,
            'effectiveness': 0.35,
            'risk': 0.20,
            'environmental': 0.15
        }
    else:
        weights = user_weights
    
    # Define strategies with their attributes
    strategies = {
        "Kimia Penuh": {
            "cost_per_ha": 3500000,
            "effectiveness": 95,
            "risk": 75,
            "environmental_impact": 80,
            "description": "Pupuk kimia 100% (Urea, SP-36, KCl) dengan dosis optimal",
            "pros": ["Hasil maksimal", "Respons cepat", "Mudah diaplikasikan"],
            "cons": ["Biaya tinggi", "Risiko over-fertilization", "Dampak lingkungan"]
        },
        "Kombinasi Seimbang": {
            "cost_per_ha": 2800000,
            "effectiveness": 85,
            "risk": 45,
            "environmental_impact": 50,
            "description": "60% kimia + 40% organik untuk keseimbangan",
            "pros": ["Biaya moderat", "Risiko rendah", "Ramah lingkungan"],
            "cons": ["Hasil sedikit lebih rendah", "Perlu 2 jenis pupuk"]
        },
        "Organik Prioritas": {
            "cost_per_ha": 3200000,
            "effectiveness": 75,
            "risk": 25,
            "environmental_impact": 20,
            "description": "80% organik + 20% kimia untuk sustainability",
            "pros": ["Sangat ramah lingkungan", "Perbaiki struktur tanah", "Risiko minimal"],
            "cons": ["Hasil lebih rendah", "Respons lebih lambat", "Biaya cukup tinggi"]
        },
        "Slow-Release": {
            "cost_per_ha": 4200000,
            "effectiveness": 90,
            "risk": 30,
            "environmental_impact": 35,
            "description": "Pupuk lepas lambat untuk efisiensi jangka panjang",
            "pros": ["Efisiensi tinggi", "Aplikasi lebih jarang", "Risiko rendah"],
            "cons": ["Biaya awal tinggi", "Ketersediaan terbatas"]
        }
    }
    
    # Calculate total cost for the area
    for strategy in strategies.values():
        strategy['total_cost'] = strategy['cost_per_ha'] * area_ha
    
    # Normalize attributes (0-100 scale)
    costs = [s['cost_per_ha'] for s in strategies.values()]
    min_cost, max_cost = min(costs), max(costs)
    
    results = {}
    for name, strategy in strategies.items():
        # Normalize cost (lower is better, so invert)
        norm_cost = 100 - ((strategy['cost_per_ha'] - min_cost) / (max_cost - min_cost) * 100) if max_cost > min_cost else 100
        
        # Normalize effectiveness (higher is better)
        norm_effectiveness = strategy['effectiveness']
        
        # Normalize risk (lower is better, so invert)
        norm_risk = 100 - strategy['risk']
        
        # Normalize environmental impact (lower is better, so invert)
        norm_environmental = 100 - strategy['environmental_impact']
        
        # Calculate weighted utility score
        utility_score = (
            norm_cost * weights['cost'] +
            norm_effectiveness * weights['effectiveness'] +
            norm_risk * weights['risk'] +
            norm_environmental * weights['environmental']
        )
        
        results[name] = {
            **strategy,
            'normalized_scores': {
                'cost': round(norm_cost, 1),
                'effectiveness': round(norm_effectiveness, 1),
                'risk': round(norm_risk, 1),
                'environmental': round(norm_environmental, 1)
            },
            'utility_score': round(utility_score, 1)
        }
    
    # Sort by utility score
    sorted_results = dict(sorted(results.items(), key=lambda x: x[1]['utility_score'], reverse=True))
    
    return sorted_results, weights

# ========== MAIN APP ==========
st.title("🎯 Rekomendasi Pupuk Terpadu")
st.markdown("**Pilih metode rekomendasi yang sesuai dengan kebutuhan Anda**")

# Method Selection
st.subheader("📋 Pilih Metode Rekomendasi")

method = st.radio(
    "Pilih metode:",
    [
        "Kalkulator Dosis (Basic)",
        "Rekomendasi Cerdas (Advanced AI)",
        "Analisis Kesehatan Daun (BWD)",
        "Strategi Keputusan (Decision Theory)"
    ],
    help="Pilih metode sesuai data yang Anda miliki"
)

st.markdown("---")

# ========== METHOD 1: BASIC CALCULATOR ==========
if method == "Kalkulator Dosis (Basic)":
    st.subheader("Kalkulator Dosis Pupuk (Basic)")
    st.info("Metode ini menggunakan rekomendasi standar berdasarkan jenis tanaman dan luas lahan")
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop = st.selectbox(
            "Jenis Tanaman",
            ["Padi", "Jagung", "Cabai Merah", "Tomat"]
        )
    
    with col2:
        area_ha = st.number_input(
            "Luas Lahan (ha)",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1
        )
    
    if st.button("Hitung Dosis", type="primary", use_container_width=True):
        result = calculate_basic_fertilizer(crop, area_ha)
        
        st.markdown("---")
        st.subheader("Hasil Perhitungan")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nitrogen (N)", f"{result['N']:.1f} kg")
        with col2:
            st.metric("Fosfor (P)", f"{result['P']:.1f} kg")
        with col3:
            st.metric("Kalium (K)", f"{result['K']:.1f} kg")
        
        # Fertilizer breakdown
        st.markdown("---")
        st.subheader("Kebutuhan Pupuk")
        
        urea = result['N'] / 0.46
        sp36 = result['P'] / 0.36
        kcl = result['K'] / 0.60
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **Urea (46% N)**
            - {urea:.1f} kg
            - {urea/50:.1f} karung (50kg)
            - Rp {urea * 2500:,.0f}
            """)
        
        with col2:
            st.markdown(f"""
            **SP-36 (36% P)**
            - {sp36:.1f} kg
            - {sp36/50:.1f} karung (50kg)
            - Rp {sp36 * 3000:,.0f}
            """)
        
        with col3:
            st.markdown(f"""
            **KCl (60% K)**
            - {kcl:.1f} kg
            - {kcl/50:.1f} karung (50kg)
            - Rp {kcl * 3500:,.0f}
            """)
        
        total_cost = (urea * 2500) + (sp36 * 3000) + (kcl * 3500)
        st.success(f"Total Biaya: Rp {total_cost:,.0f}")

# ========== METHOD 2: AI ADVANCED ==========
elif method == "Rekomendasi Cerdas (Advanced AI)":
    st.subheader("Rekomendasi Cerdas dengan AI")
    st.info("Analisis mendalam menggunakan AI berdasarkan kondisi tanah dan tanaman")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Data Tanaman & Lahan**")
        crop = st.selectbox(
            "Jenis Tanaman",
            ["Padi", "Jagung", "Cabai Merah", "Tomat"]
        )
        area_ha = st.number_input(
            "Luas Lahan (ha)",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1
        )
    
    with col2:
        st.markdown("**Data Tanah (Hasil Uji Lab)**")
        n_ppm = st.number_input("Nitrogen (ppm)", 0.0, 10000.0, 3000.0, 100.0)
        p_ppm = st.number_input("Fosfor (ppm)", 0.0, 100.0, 20.0, 1.0)
        k_ppm = st.number_input("Kalium (ppm)", 0.0, 10000.0, 2500.0, 100.0)
        ph = st.number_input("pH Tanah", 0.0, 14.0, 6.5, 0.1)
    
    if st.button("Analisis dengan AI", type="primary", use_container_width=True):
        result = ai_advanced_recommendation(crop, n_ppm, p_ppm, k_ppm, ph, area_ha)
        
        st.markdown("---")
        st.subheader("Hasil Analisis AI")
        
        # Soil status
        st.markdown("**Status Tanah:**")
        col1, col2, col3, col4 = st.columns(4)
        
        status_colors = {'Cukup': 'green', 'Kurang': 'red', 'Optimal': 'green', 'Perlu Penyesuaian': 'yellow'}
        
        with col1:
            st.metric("Nitrogen", result['soil_status']['N'])
        with col2:
            st.metric("Fosfor", result['soil_status']['P'])
        with col3:
            st.metric("Kalium", result['soil_status']['K'])
        with col4:
            st.metric("pH", result['soil_status']['pH'])
        
        # NPK needed
        st.markdown("---")
        st.subheader("Rekomendasi Pupuk AI")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            **Urea**
            - {result['fertilizers']['Urea']:.1f} kg
            - {result['fertilizers']['Urea']/50:.1f} karung
            - Rp {result['fertilizers']['Urea'] * 2500:,.0f}
            """)
        
        with col2:
            st.markdown(f"""
            **SP-36**
            - {result['fertilizers']['SP-36']:.1f} kg
            - {result['fertilizers']['SP-36']/50:.1f} karung
            - Rp {result['fertilizers']['SP-36'] * 3000:,.0f}
            """)
        
        with col3:
            st.markdown(f"""
            **KCl**
            - {result['fertilizers']['KCl']:.1f} kg
            - {result['fertilizers']['KCl']/50:.1f} karung
            - Rp {result['fertilizers']['KCl'] * 3500:,.0f}
            """)
        
        # Visualization
        fig = go.Figure(data=[
            go.Bar(name='N', x=['NPK'], y=[result['npk_needed']['N']], marker_color='#3b82f6'),
            go.Bar(name='P', x=['NPK'], y=[result['npk_needed']['P']], marker_color='#10b981'),
            go.Bar(name='K', x=['NPK'], y=[result['npk_needed']['K']], marker_color='#f59e0b')
        ])
        
        fig.update_layout(
            title="Kebutuhan NPK Berdasarkan Analisis AI",
            yaxis_title="Jumlah (kg)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

# ========== METHOD 3: BWD LEAF ANALYSIS ==========
elif method == "Analisis Kesehatan Daun (BWD)":
    st.subheader("Analisis Kesehatan Daun (BWD)")
    st.info("Upload foto daun untuk mendapatkan skor BWD otomatis dan deteksi penyakit")
    
    with st.expander("Tentang Analisis BWD"):
        st.markdown("""
        **BWD (Brown-White-Disease) Analysis:**
        - **Brown Spots:** Deteksi bercak coklat (penyakit jamur)
        - **White Spots:** Deteksi bercak putih (bakteri/jamur)
        - **Disease Detection:** Identifikasi jenis penyakit
        - **Health Score:** Skor kesehatan 0-100
        
        **Tips Foto:**
        - Ambil foto di siang hari
        - Fokus pada daun yang bergejala
        - Jarak 20-30 cm
        - Hindari bayangan
        """)
    
    uploaded_file = st.file_uploader(
        "Upload foto daun (JPG, PNG)",
        type=['jpg', 'jpeg', 'png']
    )
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.image(image, caption="Foto Original", use_container_width=True)
        
        if st.button("Analisis BWD", type="primary", use_container_width=True):
            with st.spinner("Menganalisis kesehatan daun..."):
                result = analyze_bwd_leaf(image)
            
            with col2:
                # BWD Score
                score_color = "#10b981" if result['bwd_score'] >= 80 else "#f59e0b" if result['bwd_score'] >= 60 else "#ef4444"
                
                st.markdown(f"""
                <div style="background: {score_color}20; padding: 2rem; border-radius: 12px; 
                            border: 2px solid {score_color}; text-align: center;">
                    <h2 style="color: {score_color}; margin: 0;">BWD Score</h2>
                    <h1 style="font-size: 3rem; margin: 0.5rem 0; color: {score_color};">
                        {result['bwd_score']:.1f}/100
                    </h1>
                    <p style="color: #6b7280; margin: 0;">{result['health_status']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Detailed Analysis
            st.markdown("---")
            st.subheader("Analisis Detail")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Bercak Coklat", f"{result['brown_percent']:.1f}%")
            with col2:
                st.metric("Bercak Putih", f"{result['white_percent']:.1f}%")
            with col3:
                st.metric("Area Hijau Sehat", f"{result['green_percent']:.1f}%")
            
            # Disease Detection
            st.markdown("---")
            st.subheader("Penyakit Terdeteksi")
            
            for disease in result['diseases']:
                if "Tidak ada" in disease:
                    st.success(f"{disease}")
                else:
                    st.error(f"{disease}")
            
            # Recommendations
            st.markdown("---")
            st.subheader("Rekomendasi")
            
            rec = result['recommendation']
            
            if rec['fertilizer_adjustment']:
                st.markdown("**Penyesuaian Pemupukan:**")
                for adj in rec['fertilizer_adjustment']:
                    st.write(f"- {adj}")
            
            if rec['treatment']:
                st.markdown("**Treatment:**")
                for treat in rec['treatment']:
                    st.write(f"- {treat}")
            
            if rec['prevention']:
                st.markdown("**Pencegahan:**")
                for prev in rec['prevention']:
                    st.write(f"- {prev}")

# ========== METHOD 4: DECISION THEORY ==========
else:
    st.subheader("Analisis Strategi Pemupukan (MAUT)")
    st.info("Gunakan Multi-Attribute Utility Theory untuk memilih strategi pemupukan terbaik berdasarkan biaya, efektivitas, risiko, dan dampak lingkungan")
    
    with st.expander("Tentang Decision Theory"):
        st.markdown("""
        **Multi-Attribute Utility Theory (MAUT):**
        
        Metode ini membantu Anda memilih strategi pemupukan terbaik dengan mempertimbangkan:
        - **Biaya (30%):** Total investasi pupuk
        - **Efektivitas (35%):** Potensi hasil panen
        - **Risiko (20%):** Risiko over-fertilization dan kegagalan
        - **Dampak Lingkungan (15%):** Sustainability dan kesehatan tanah
        
        **4 Strategi yang Dibandingkan:**
        1. **Kimia Penuh:** Maksimalkan hasil dengan pupuk kimia
        2. **Kombinasi Seimbang:** Balance antara kimia dan organik
        3. **Organik Prioritas:** Fokus sustainability
        4. **Slow-Release:** Efisiensi jangka panjang
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop_decision = st.selectbox(
            "Jenis Tanaman",
            ["Padi", "Jagung", "Cabai Merah", "Tomat"],
            key="crop_decision"
        )
    
    with col2:
        area_decision = st.number_input(
            "Luas Lahan (ha)",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1,
            key="area_decision"
        )
    
    # Sensitivity Analysis - Adjust Weights
    st.markdown("---")
    st.subheader("Sesuaikan Bobot Kriteria (Sensitivity Analysis)")
    
    # Initialize session state for weights
    if 'weight_cost' not in st.session_state:
        st.session_state.weight_cost = 30
    if 'weight_eff' not in st.session_state:
        st.session_state.weight_eff = 35
    if 'weight_risk' not in st.session_state:
        st.session_state.weight_risk = 20
    if 'weight_env' not in st.session_state:
        st.session_state.weight_env = 15
    if 'decision_results' not in st.session_state:
        st.session_state.decision_results = None
    if 'decision_crop' not in st.session_state:
        st.session_state.decision_crop = None
    if 'decision_area' not in st.session_state:
        st.session_state.decision_area = None
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        new_cost = st.slider("Biaya", 0, 100, st.session_state.weight_cost, 5, key="slider_cost")
        if new_cost != st.session_state.weight_cost:
            # Adjust other weights proportionally
            old_total = st.session_state.weight_eff + st.session_state.weight_risk + st.session_state.weight_env
            if old_total > 0:
                remaining = 100 - new_cost
                ratio = remaining / old_total
                st.session_state.weight_eff = int(st.session_state.weight_eff * ratio)
                st.session_state.weight_risk = int(st.session_state.weight_risk * ratio)
                st.session_state.weight_env = 100 - new_cost - st.session_state.weight_eff - st.session_state.weight_risk
            st.session_state.weight_cost = new_cost
            # Recalculate if results exist
            if st.session_state.decision_results is not None:
                temp_weights = {
                    'cost': st.session_state.weight_cost / 100,
                    'effectiveness': st.session_state.weight_eff / 100,
                    'risk': st.session_state.weight_risk / 100,
                    'environmental': st.session_state.weight_env / 100
                }
                st.session_state.decision_results, _ = calculate_decision_matrix(
                    st.session_state.decision_crop, 
                    st.session_state.decision_area, 
                    temp_weights
                )
            st.rerun()
    
    with col2:
        new_eff = st.slider("Efektivitas", 0, 100, st.session_state.weight_eff, 5, key="slider_eff")
        if new_eff != st.session_state.weight_eff:
            old_total = st.session_state.weight_cost + st.session_state.weight_risk + st.session_state.weight_env
            if old_total > 0:
                remaining = 100 - new_eff
                ratio = remaining / old_total
                st.session_state.weight_cost = int(st.session_state.weight_cost * ratio)
                st.session_state.weight_risk = int(st.session_state.weight_risk * ratio)
                st.session_state.weight_env = 100 - new_eff - st.session_state.weight_cost - st.session_state.weight_risk
            st.session_state.weight_eff = new_eff
            if st.session_state.decision_results is not None:
                temp_weights = {
                    'cost': st.session_state.weight_cost / 100,
                    'effectiveness': st.session_state.weight_eff / 100,
                    'risk': st.session_state.weight_risk / 100,
                    'environmental': st.session_state.weight_env / 100
                }
                st.session_state.decision_results, _ = calculate_decision_matrix(
                    st.session_state.decision_crop, 
                    st.session_state.decision_area, 
                    temp_weights
                )
            st.rerun()
    
    with col3:
        new_risk = st.slider("Risiko", 0, 100, st.session_state.weight_risk, 5, key="slider_risk")
        if new_risk != st.session_state.weight_risk:
            old_total = st.session_state.weight_cost + st.session_state.weight_eff + st.session_state.weight_env
            if old_total > 0:
                remaining = 100 - new_risk
                ratio = remaining / old_total
                st.session_state.weight_cost = int(st.session_state.weight_cost * ratio)
                st.session_state.weight_eff = int(st.session_state.weight_eff * ratio)
                st.session_state.weight_env = 100 - new_risk - st.session_state.weight_cost - st.session_state.weight_eff
            st.session_state.weight_risk = new_risk
            if st.session_state.decision_results is not None:
                temp_weights = {
                    'cost': st.session_state.weight_cost / 100,
                    'effectiveness': st.session_state.weight_eff / 100,
                    'risk': st.session_state.weight_risk / 100,
                    'environmental': st.session_state.weight_env / 100
                }
                st.session_state.decision_results, _ = calculate_decision_matrix(
                    st.session_state.decision_crop, 
                    st.session_state.decision_area, 
                    temp_weights
                )
            st.rerun()
    
    with col4:
        new_env = st.slider("Lingkungan", 0, 100, st.session_state.weight_env, 5, key="slider_env")
        if new_env != st.session_state.weight_env:
            old_total = st.session_state.weight_cost + st.session_state.weight_eff + st.session_state.weight_risk
            if old_total > 0:
                remaining = 100 - new_env
                ratio = remaining / old_total
                st.session_state.weight_cost = int(st.session_state.weight_cost * ratio)
                st.session_state.weight_eff = int(st.session_state.weight_eff * ratio)
                st.session_state.weight_risk = 100 - new_env - st.session_state.weight_cost - st.session_state.weight_eff
            st.session_state.weight_env = new_env
            if st.session_state.decision_results is not None:
                temp_weights = {
                    'cost': st.session_state.weight_cost / 100,
                    'effectiveness': st.session_state.weight_eff / 100,
                    'risk': st.session_state.weight_risk / 100,
                    'environmental': st.session_state.weight_env / 100
                }
                st.session_state.decision_results, _ = calculate_decision_matrix(
                    st.session_state.decision_crop, 
                    st.session_state.decision_area, 
                    temp_weights
                )
            st.rerun()
    
    # Use session state values
    weight_cost = st.session_state.weight_cost
    weight_eff = st.session_state.weight_eff
    weight_risk = st.session_state.weight_risk
    weight_env = st.session_state.weight_env
    
    total_weight = weight_cost + weight_eff + weight_risk + weight_env
    
    st.success(f"Total bobot: {total_weight}% (Biaya: {weight_cost}%, Efektivitas: {weight_eff}%, Risiko: {weight_risk}%, Lingkungan: {weight_env}%)")
    
    user_weights = {
        'cost': weight_cost / 100,
        'effectiveness': weight_eff / 100,
        'risk': weight_risk / 100,
        'environmental': weight_env / 100
    }
    
    if st.button("Analisis Strategi", type="primary", use_container_width=True):
        results, weights = calculate_decision_matrix(crop_decision, area_decision, user_weights)
        st.session_state.decision_results = results
        st.session_state.decision_crop = crop_decision
        st.session_state.decision_area = area_decision
    
    # Display results if they exist in session state
    if st.session_state.decision_results is not None:
        results = st.session_state.decision_results
        
        st.markdown("---")
        st.subheader("Decision Matrix")
        
        # Create decision matrix table
        matrix_data = []
        for strategy_name, data in results.items():
            matrix_data.append({
                'Strategi': strategy_name,
                'Biaya': f"Rp {data['total_cost']:,.0f}",
                'Efektivitas': f"{data['effectiveness']}/100",
                'Risiko': f"{100 - data['risk']}/100",
                'Lingkungan': f"{100 - data['environmental_impact']}/100",
                'Skor Utilitas': f"{data['utility_score']:.1f}/100"
            })
        
        df_matrix = pd.DataFrame(matrix_data)
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)
        
        # Top Recommendation
        st.markdown("---")
        top_strategy = list(results.keys())[0]
        top_data = results[top_strategy]
        
        st.success(f"Rekomendasi Terbaik: {top_strategy}")
        st.write(f"**Skor Utilitas:** {top_data['utility_score']:.1f}/100")
        st.write(f"**Deskripsi:** {top_data['description']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Keunggulan:**")
            for pro in top_data['pros']:
                st.write(f"- {pro}")
        
        with col2:
            st.markdown("**Pertimbangan:**")
            for con in top_data['cons']:
                st.write(f"- {con}")
        
        # Radar Chart Comparison
        st.markdown("---")
        st.subheader("Perbandingan Visual (Radar Chart)")
        
        # Prepare data for radar chart
        categories = ['Biaya', 'Efektivitas', 'Risiko (Rendah)', 'Lingkungan (Ramah)']
        
        fig = go.Figure()
        
        for strategy_name, data in results.items():
            scores = data['normalized_scores']
            fig.add_trace(go.Scatterpolar(
                r=[scores['cost'], scores['effectiveness'], scores['risk'], scores['environmental']],
                theta=categories,
                fill='toself',
                name=strategy_name
            ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Perbandingan Strategi Pemupukan",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Detailed Comparison
        st.markdown("---")
        st.subheader("Perbandingan Detail Semua Strategi")
        
        for rank, (strategy_name, data) in enumerate(results.items(), 1):
            with st.expander(f"#{rank} - {strategy_name} (Skor: {data['utility_score']:.1f})"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Biaya Total", f"Rp {data['total_cost']:,.0f}")
                    st.metric("Biaya/ha", f"Rp {data['cost_per_ha']:,.0f}")
                
                with col2:
                    st.metric("Efektivitas", f"{data['effectiveness']}/100")
                    st.metric("Risiko", f"{data['risk']}/100")
                
                with col3:
                    st.metric("Dampak Lingkungan", f"{data['environmental_impact']}/100")
                    st.metric("Skor Utilitas", f"{data['utility_score']:.1f}/100")
                
                st.markdown(f"**Deskripsi:** {data['description']}")
                
                col_pros, col_cons = st.columns(2)
                
                with col_pros:
                    st.markdown("**Keunggulan:**")
                    for pro in data['pros']:
                        st.write(f"- {pro}")
                
                with col_cons:
                    st.markdown("**Pertimbangan:**")
                    for con in data['cons']:
                        st.write(f"- {con}")

# Footer
st.markdown("---")
st.caption("""
Rekomendasi Pupuk Terpadu - Pilih metode sesuai kebutuhan: Basic untuk cepat, 
AI Advanced untuk presisi, BWD untuk diagnosis kesehatan daun, atau Decision Theory untuk analisis strategi.
""")
