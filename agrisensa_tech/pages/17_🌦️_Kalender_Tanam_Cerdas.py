"""
AgriSensa Tech - Kalender Tanam Cerdas
=======================================
Seasonal Planting Calendar with Pest Risk & Price Prediction

Author: Yandri
Date: 2024-12-26
Version: 1.0 (Rule-Based Expert System)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Authentication
from utils.auth import require_auth, show_user_info_sidebar
user = require_auth()
show_user_info_sidebar()

# Page config
st.set_page_config(page_title="Kalender Tanam Cerdas", page_icon="🌦️", layout="wide")

# ==========================================
# KNOWLEDGE BASE: Seasonal Patterns
# ==========================================

# Base Indonesia Seasonal Pattern (Opsi 1)
INDONESIA_SEASONAL_PATTERN = {
    1: {"season": "Hujan", "rainfall_mm": 300, "temp_c": 26, "humidity": 85},
    2: {"season": "Hujan", "rainfall_mm": 280, "temp_c": 26, "humidity": 85},
    3: {"season": "Hujan", "rainfall_mm": 250, "temp_c": 27, "humidity": 80},
    4: {"season": "Transisi_Kemarau", "rainfall_mm": 150, "temp_c": 28, "humidity": 75},
    5: {"season": "Transisi_Kemarau", "rainfall_mm": 120, "temp_c": 29, "humidity": 70},
    6: {"season": "Kemarau", "rainfall_mm": 60, "temp_c": 30, "humidity": 65},
    7: {"season": "Kemarau", "rainfall_mm": 40, "temp_c": 31, "humidity": 60},
    8: {"season": "Kemarau", "rainfall_mm": 50, "temp_c": 31, "humidity": 60},
    9: {"season": "Transisi_Hujan", "rainfall_mm": 100, "temp_c": 30, "humidity": 70},
    10: {"season": "Transisi_Hujan", "rainfall_mm": 150, "temp_c": 29, "humidity": 75},
    11: {"season": "Hujan", "rainfall_mm": 220, "temp_c": 27, "humidity": 80},
    12: {"season": "Hujan", "rainfall_mm": 320, "temp_c": 26, "humidity": 85},
}

# Banyumas Local Adjustment (Opsi 4 - dari pengalaman Pak Yandri)
BANYUMAS_PEST_PATTERN = {
    # Musim Kemarau (Jun-Agu): Hama tinggi
    6: {"thrips": 70, "kutu_kebul": 65, "jamur": 15, "patek": 10, "layu_bakteri": 15},
    7: {"thrips": 85, "kutu_kebul": 80, "jamur": 10, "patek": 10, "layu_bakteri": 10},
    8: {"thrips": 80, "kutu_kebul": 75, "jamur": 15, "patek": 15, "layu_bakteri": 15},
    
    # Transisi ke Hujan (Sep-Okt): DOUBLE TROUBLE!
    9: {"thrips": 65, "kutu_kebul": 60, "jamur": 70, "patek": 75, "layu_bakteri": 70},
    10: {"thrips": 50, "kutu_kebul": 45, "jamur": 80, "patek": 85, "layu_bakteri": 80},
    
    # Musim Hujan (Nov-Mar): Jamur tinggi
    11: {"thrips": 30, "kutu_kebul": 25, "jamur": 85, "patek": 80, "layu_bakteri": 85},
    12: {"thrips": 25, "kutu_kebul": 20, "jamur": 80, "patek": 75, "layu_bakteri": 80},
    1: {"thrips": 20, "kutu_kebul": 20, "jamur": 85, "patek": 80, "layu_bakteri": 85},
    2: {"thrips": 25, "kutu_kebul": 25, "jamur": 80, "patek": 75, "layu_bakteri": 80},
    3: {"thrips": 30, "kutu_kebul": 30, "jamur": 75, "patek": 70, "layu_bakteri": 75},
    
    # Transisi ke Kemarau (Apr-Mei)
    4: {"thrips": 45, "kutu_kebul": 40, "jamur": 50, "patek": 45, "layu_bakteri": 50},
    5: {"thrips": 60, "kutu_kebul": 55, "jamur": 35, "patek": 30, "layu_bakteri": 35},
}

# Price Pattern (dari CROP_DATABASE Page 11 + seasonal adjustment)
# Base price Cabai Merah: Rp 35,000/kg (dari Page 11)
# Volatility: 50% (highly volatile)
CABAI_PRICE_PATTERN = {
    1: {"base_price": 35000, "multiplier": 1.3, "volatility": 0.50},  # Nataru (+30%)
    2: {"base_price": 35000, "multiplier": 0.9, "volatility": 0.45},  # Hujan puncak (-10%)
    3: {"base_price": 35000, "multiplier": 0.85, "volatility": 0.40},  # Hujan (-15%)
    4: {"base_price": 35000, "multiplier": 0.95, "volatility": 0.45},  # Transisi (-5%)
    5: {"base_price": 35000, "multiplier": 1.1, "volatility": 0.50},  # Mulai kemarau (+10%)
    6: {"base_price": 35000, "multiplier": 1.4, "volatility": 0.55},  # Kemarau (+40%)
    7: {"base_price": 35000, "multiplier": 1.6, "volatility": 0.60},  # Kemarau puncak (+60%)
    8: {"base_price": 35000, "multiplier": 1.5, "volatility": 0.55},  # Kemarau (+50%)
    9: {"base_price": 35000, "multiplier": 1.8, "volatility": 0.65},  # Transisi - TERTINGGI! (+80%)
    10: {"base_price": 35000, "multiplier": 1.7, "volatility": 0.60},  # Transisi (+70%)
    11: {"base_price": 35000, "multiplier": 1.2, "volatility": 0.50},  # Mulai hujan (+20%)
    12: {"base_price": 35000, "multiplier": 1.4, "volatility": 0.55},  # Nataru (+40%)
}

# Crop growing days
CROP_GROWING_DAYS = {
    "Cabai Merah": 120,
    "Cabai Rawit": 100,
    "Tomat": 90,
    "Terong": 80,
    "Bawang Merah": 70,
}


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def calculate_harvest_month(plant_month, growing_days):
    """Calculate harvest month from planting month"""
    harvest_month = (plant_month + (growing_days // 30)) % 12
    if harvest_month == 0:
        harvest_month = 12
    return harvest_month


def get_risk_score(month):
    """Get total pest risk score for a month"""
    pests = BANYUMAS_PEST_PATTERN[month]
    # Weighted average (jamur & patek lebih berbahaya)
    total = (pests['thrips'] * 0.15 + 
             pests['kutu_kebul'] * 0.15 + 
             pests['jamur'] * 0.25 + 
             pests['patek'] * 0.25 + 
             pests['layu_bakteri'] * 0.20)
    return round(total, 1)


def get_risk_level(score):
    """Convert risk score to level"""
    if score >= 75:
        return "🔴 Sangat Tinggi", "red"
    elif score >= 60:
        return "🟠 Tinggi", "orange"
    elif score >= 40:
        return "🟡 Sedang", "yellow"
    else:
        return "🟢 Rendah", "green"


def get_price_prediction(month):
    """Get price prediction for harvest month"""
    pattern = CABAI_PRICE_PATTERN[month]
    predicted_price = pattern['base_price'] * pattern['multiplier']
    min_price = predicted_price * (1 - pattern['volatility'])
    max_price = predicted_price * (1 + pattern['volatility'])
    
    return {
        'predicted': round(predicted_price, 0),
        'min': round(min_price, 0),
        'max': round(max_price, 0)
    }


def get_recommendation(risk_score, predicted_price):
    """Get planting recommendation"""
    # Risk-Return Matrix (adjusted for base price Rp 35,000)
    if risk_score < 50 and predicted_price > 50000:  # >Rp 50k = very high
        return "✅ SANGAT DIREKOMENDASIKAN", "Risiko rendah, harga tinggi - kondisi ideal!"
    elif risk_score < 60 and predicted_price > 40000:  # >Rp 40k = high
        return "✅ DIREKOMENDASIKAN", "Risk-reward balance bagus"
    elif risk_score > 75:
        return "❌ TIDAK DIREKOMENDASIKAN", "Risiko gagal panen sangat tinggi"
    elif predicted_price < 30000:  # <Rp 30k = very low
        return "⚠️ KURANG MENGUNTUNGKAN", "Harga rendah, pertimbangkan komoditas lain"
    else:
        return "⚠️ HATI-HATI", "Pertimbangkan mitigasi risiko"


def calculate_planting_score(risk_score, predicted_price, harvest_month):
    """
    Calculate optimal planting score (0-100)
    Factors: Risk, Price, Season, Supply Glut
    """
    # Base score from risk (inverse - lower risk = higher score)
    risk_component = (100 - risk_score) * 0.4  # 40% weight
    
    # Price component (normalized to base price 35k)
    price_ratio = predicted_price / 35000
    price_component = min(price_ratio * 50, 50)  # 50% weight, max 50 points
    
    # Season bonus (avoid extreme months)
    if harvest_month in [9, 10]:  # Double trouble
        season_penalty = -10
    elif harvest_month in [1, 12]:  # Nataru bonus
        season_bonus = 10
    else:
        season_bonus = 0
    
    # Supply glut penalty (tanam serentak)
    if harvest_month in [2, 3]:  # Panen serentak musim hujan
        supply_penalty = -15
    elif harvest_month in [7, 8]:  # Panen serentak kemarau
        supply_penalty = -10
    else:
        supply_penalty = 0
    
    total_score = risk_component + price_component + season_bonus + supply_penalty
    return max(0, min(100, round(total_score, 1)))


def get_supply_glut_warning(harvest_month):
    """Check if harvest month has supply glut risk"""
    # Months when many farmers harvest simultaneously
    glut_months = {
        2: {"severity": "HIGH", "reason": "Panen serentak MT-I (musim hujan), banyak petani tanam Nov-Des"},
        3: {"severity": "HIGH", "reason": "Puncak panen MT-I, supply melimpah"},
        7: {"severity": "MEDIUM", "reason": "Panen MT-II, kompetisi dengan sentra produksi lain"},
        8: {"severity": "MEDIUM", "reason": "Akhir panen MT-II"},
    }
    
    if harvest_month in glut_months:
        return glut_months[harvest_month]
    return None


def calculate_roi(area_ha, predicted_price, harvest_month):
    """
    Calculate ROI for cabai merah
    Data from CROP_DATABASE Page 11
    """
    # Constants from Page 11
    CAPITAL_PER_HA = 45000000  # Rp 45 juta/ha
    YIELD_POTENTIAL = 12000  # kg/ha
    
    # Adjust yield based on risk
    risk_score = get_risk_score(harvest_month)
    yield_factor = 1 - (risk_score / 200)  # High risk = lower yield
    actual_yield = YIELD_POTENTIAL * yield_factor * area_ha
    
    # Revenue
    revenue = actual_yield * predicted_price
    
    # Costs
    total_cost = CAPITAL_PER_HA * area_ha
    
    # Profit & ROI
    profit = revenue - total_cost
    roi_pct = (profit / total_cost) * 100
    
    return {
        'area_ha': area_ha,
        'yield_kg': round(actual_yield, 0),
        'price_per_kg': predicted_price,
        'revenue': round(revenue, 0),
        'cost': round(total_cost, 0),
        'profit': round(profit, 0),
        'roi_pct': round(roi_pct, 1),
        'payback_months': round((total_cost / (profit / 4)) if profit > 0 else 999, 1)  # Assuming 4 months cycle
    }


def get_contract_farming_recommendation(predicted_price, harvest_month):
    """
    Recommend contract farming if price risk is high
    """
    glut = get_supply_glut_warning(harvest_month)
    
    if glut and glut['severity'] == 'HIGH':
        return {
            'recommended': True,
            'reason': f"⚠️ Risiko harga jatuh tinggi: {glut['reason']}",
            'partners': [
                "🏭 **Indofood** (Cabai untuk sambal/bumbu)",
                "🏭 **ABC** (Sambal botol)",
                "🏭 **Dua Belibis** (Sambal sachet)",
                "🏪 **Supermarket** (Lotte Mart, Transmart, Hypermart)"
            ],
            'benefits': [
                "✅ Harga terjamin (tidak terpengaruh fluktuasi pasar)",
                "✅ Pembayaran pasti",
                "✅ Standar kualitas jelas",
                "✅ Bisa akses kredit/modal kerja"
            ]
        }
    elif predicted_price < 35000:  # Below base price
        return {
            'recommended': True,
            'reason': "⚠️ Prediksi harga rendah, kontrak farming bisa jadi safety net",
            'partners': [
                "🏭 **Indofood** (Harga kontrak biasanya Rp 30-35k/kg)",
                "🏪 **Supermarket** (Pre-order untuk supply reguler)"
            ],
            'benefits': [
                "✅ Harga minimum terjamin",
                "✅ Mengurangi risiko kerugian"
            ]
        }
    else:
        return {
            'recommended': False,
            'reason': "✅ Kondisi pasar cukup baik, jual spot market lebih menguntungkan",
            'note': "Tetap monitor harga menjelang panen"
        }



# ==========================================
# MAIN APP
# ==========================================

st.title("🌦️ Kalender Tanam Cerdas")
st.markdown("**Prediksi Risiko Hama & Harga Berdasarkan Pola Musim**")
st.caption("💡 Berbasis pengalaman lapangan & pola musim Indonesia")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🎯 Rekomendasi Tanam",
    "📊 Pola Musim & Risiko",
    "💰 Prediksi Harga",
    "📚 Panduan Penggunaan"
])

# ========== TAB 1: REKOMENDASI TANAM ==========
with tab1:
    st.subheader("🎯 Cari Waktu Tanam Optimal")
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop = st.selectbox(
            "Pilih Komoditas",
            list(CROP_GROWING_DAYS.keys()),
            help="Pilih tanaman yang ingin ditanam"
        )
        
        growing_days = CROP_GROWING_DAYS[crop]
        st.info(f"⏱️ Masa tanam: **{growing_days} hari** (~{growing_days//30} bulan)")
    
    with col2:
        plant_month = st.selectbox(
            "Bulan Tanam",
            range(1, 13),
            format_func=lambda x: datetime(2024, x, 1).strftime('%B'),
            help="Kapan Anda berencana menanam?"
        )
    
    # Calculate harvest month
    harvest_month = calculate_harvest_month(plant_month, growing_days)
    
    st.markdown("---")
    
    # Analysis
    st.subheader(f"📈 Analisis: Tanam {datetime(2024, plant_month, 1).strftime('%B')} → Panen {datetime(2024, harvest_month, 1).strftime('%B')}")
    
    # Get data
    risk_score = get_risk_score(harvest_month)
    risk_level, risk_color = get_risk_level(risk_score)
    price = get_price_prediction(harvest_month)
    recommendation, reason = get_recommendation(risk_score, price['predicted'])
    
    # Display metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.metric(
            "Risiko Hama/Penyakit",
            f"{risk_score}%",
            risk_level
        )
    
    with col_m2:
        st.metric(
            "Prediksi Harga",
            f"Rp {price['predicted']:,.0f}/kg",
            f"±{((price['max']-price['min'])/2):,.0f}"
        )
    
    with col_m3:
        season = INDONESIA_SEASONAL_PATTERN[harvest_month]['season']
        st.metric(
            "Musim Panen",
            season.replace("_", " "),
            f"{INDONESIA_SEASONAL_PATTERN[harvest_month]['rainfall_mm']} mm"
        )
    
    # Recommendation box
    st.markdown("---")
    if "SANGAT DIREKOMENDASIKAN" in recommendation:
        st.success(f"### {recommendation}\n{reason}")
    elif "DIREKOMENDASIKAN" in recommendation:
        st.success(f"### {recommendation}\n{reason}")
    elif "TIDAK DIREKOMENDASIKAN" in recommendation:
        st.error(f"### {recommendation}\n{reason}")
    else:
        st.warning(f"### {recommendation}\n{reason}")
    
    # NEW FEATURE 1: Optimal Planting Score
    st.markdown("---")
    planting_score = calculate_planting_score(risk_score, price['predicted'], harvest_month)
    
    col_score1, col_score2 = st.columns([1, 2])
    
    with col_score1:
        # Score gauge
        if planting_score >= 80:
            score_color = "🟢"
            score_label = "EXCELLENT"
        elif planting_score >= 65:
            score_color = "🟡"
            score_label = "GOOD"
        elif planting_score >= 50:
            score_color = "🟠"
            score_label = "FAIR"
        else:
            score_color = "🔴"
            score_label = "POOR"
        
        st.metric("Optimal Planting Score", f"{planting_score}/100", score_color + " " + score_label)
    
    with col_score2:
        st.info(f"""
        **Komponen Score:**
        - Risiko Hama/Penyakit: {(100-risk_score)*0.4:.1f} pts
        - Prediksi Harga: {min((price['predicted']/35000)*50, 50):.1f} pts
        - Faktor Musim & Supply: {planting_score - (100-risk_score)*0.4 - min((price['predicted']/35000)*50, 50):.1f} pts
        """)
    
    # Supply Glut Warning
    glut_warning = get_supply_glut_warning(harvest_month)
    if glut_warning:
        severity_color = "🔴" if glut_warning['severity'] == 'HIGH' else "🟠"
        st.warning(f"""
        {severity_color} **PERINGATAN: Risiko Supply Glut ({glut_warning['severity']})**
        
        {glut_warning['reason']}
        
        **Dampak:** Harga bisa jatuh 20-40% karena oversupply di pasar.
        """)
    
    # NEW FEATURE 2: ROI Calculator
    with st.expander("💰 Kalkulator ROI & Kelayakan Usaha", expanded=False):
        st.markdown("**Hitung estimasi keuntungan berdasarkan luas lahan Anda**")
        
        area_input = st.number_input(
            "Luas Lahan (hektar)",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1,
            help="Masukkan luas lahan yang akan ditanami cabai"
        )
        
        roi_data = calculate_roi(area_input, price['predicted'], harvest_month)
        
        st.markdown("### 📊 Analisis Finansial")
        
        col_roi1, col_roi2, col_roi3 = st.columns(3)
        
        with col_roi1:
            st.metric("Total Biaya", f"Rp {roi_data['cost']/1e6:.1f} Jt")
            st.caption(f"Rp 45 jt/ha × {area_input} ha")
        
        with col_roi2:
            st.metric("Estimasi Revenue", f"Rp {roi_data['revenue']/1e6:.1f} Jt")
            st.caption(f"{roi_data['yield_kg']:,.0f} kg × Rp {roi_data['price_per_kg']:,.0f}/kg")
        
        with col_roi3:
            profit_color = "normal" if roi_data['profit'] > 0 else "inverse"
            st.metric("Profit", f"Rp {roi_data['profit']/1e6:.1f} Jt", 
                     f"ROI: {roi_data['roi_pct']:.1f}%",
                     delta_color=profit_color)
        
        # Detailed breakdown
        st.markdown("---")
        st.markdown("**Detail Perhitungan:**")
        
        breakdown_df = pd.DataFrame({
            'Item': [
                'Luas Lahan',
                'Potensi Yield',
                'Yield Adjusted (Risk)',
                'Harga Jual',
                'Total Revenue',
                'Total Biaya Modal',
                'Profit Bersih',
                'ROI',
                'Payback Period'
            ],
            'Nilai': [
                f"{roi_data['area_ha']} ha",
                f"12,000 kg/ha",
                f"{roi_data['yield_kg']:,.0f} kg",
                f"Rp {roi_data['price_per_kg']:,.0f}/kg",
                f"Rp {roi_data['revenue']:,.0f}",
                f"Rp {roi_data['cost']:,.0f}",
                f"Rp {roi_data['profit']:,.0f}",
                f"{roi_data['roi_pct']:.1f}%",
                f"{roi_data['payback_months']:.1f} bulan" if roi_data['payback_months'] < 999 else "N/A"
            ]
        })
        
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
        
        # Profitability assessment
        if roi_data['roi_pct'] > 50:
            st.success("✅ **Sangat Menguntungkan** - ROI >50%, layak untuk dijalankan!")
        elif roi_data['roi_pct'] > 20:
            st.info("✅ **Menguntungkan** - ROI >20%, cukup baik untuk usaha pertanian")
        elif roi_data['roi_pct'] > 0:
            st.warning("⚠️ **Profit Tipis** - ROI rendah, pertimbangkan efisiensi biaya")
        else:
            st.error("❌ **Tidak Menguntungkan** - Prediksi rugi, pertimbangkan bulan tanam lain")
    
    # NEW FEATURE 3: Contract Farming Recommendation
    contract_rec = get_contract_farming_recommendation(price['predicted'], harvest_month)
    
    if contract_rec['recommended']:
        with st.expander("🤝 Rekomendasi: Contract Farming", expanded=glut_warning is not None):
            st.markdown(f"### {contract_rec['reason']}")
            
            st.markdown("**Mitra Potensial:**")
            for partner in contract_rec['partners']:
                st.markdown(f"- {partner}")
            
            st.markdown("\n**Keuntungan Contract Farming:**")
            for benefit in contract_rec['benefits']:
                st.markdown(f"- {benefit}")
            
            st.info("""
            💡 **Tips Negosiasi Kontrak:**
            1. Minta harga minimum guarantee (floor price)
            2. Pastikan standar kualitas jelas (grade A, B, C)
            3. Tanyakan skema pembayaran (cash, tempo berapa hari)
            4. Cek apakah ada bantuan input (bibit, pupuk, pestisida)
            5. Minta kontrak tertulis yang jelas
            """)
    else:
        with st.expander("📈 Strategi Penjualan: Spot Market"):
            st.success(contract_rec['reason'])
            st.markdown(f"**Catatan:** {contract_rec.get('note', '')}")
            
            st.markdown("""
            **Tips Maksimalkan Profit di Spot Market:**
            1. Monitor harga harian via BAPANAS/pasar lokal
            2. Jual bertahap (jangan sekaligus) untuk dapat harga terbaik
            3. Sortir kualitas (grade A harga premium)
            4. Jaga kualitas panen (petik pagi hari, handling hati-hati)
            5. Diversifikasi buyer (pedagang, pasar, supermarket)
            """)

    
    # Detailed breakdown
    with st.expander("🔍 Detail Risiko Hama/Penyakit"):
        pests = BANYUMAS_PEST_PATTERN[harvest_month]
        
        st.markdown("**Tingkat Risiko per Jenis OPT:**")
        
        pest_df = pd.DataFrame({
            'OPT': ['Thrips', 'Kutu Kebul', 'Jamur', 'Patek', 'Layu Bakteri'],
            'Risiko (%)': [pests['thrips'], pests['kutu_kebul'], pests['jamur'], pests['patek'], pests['layu_bakteri']]
        })
        
        fig_pest = px.bar(pest_df, x='OPT', y='Risiko (%)', 
                         title=f"Risiko OPT Bulan {datetime(2024, harvest_month, 1).strftime('%B')}",
                         color='Risiko (%)', color_continuous_scale='Reds')
        st.plotly_chart(fig_pest, use_container_width=True)
        
        # Mitigation advice
        st.markdown("**💡 Saran Mitigasi:**")
        if pests['thrips'] > 60 or pests['kutu_kebul'] > 60:
            st.warning("- **Hama tinggi**: Siapkan insektisida (Imidakloprid, Abamektin)")
        if pests['jamur'] > 60 or pests['patek'] > 60:
            st.warning("- **Jamur tinggi**: Siapkan fungisida (Metalaxyl, Mankozeb)")
        if harvest_month in [9, 10]:
            st.error("- **DOUBLE TROUBLE**: Perlu monitoring ekstra ketat!")
    
    # Kementan Validation
    with st.expander("✅ Validasi dengan Kalender Tanam Kementan"):
        st.markdown("""
        **Rekomendasi Resmi Kementan untuk Indonesia:**
        
        ### 📅 Musim Tanam Nasional
        
        **Musim Tanam I (MT-I):**
        - **Periode**: Oktober - Maret (Musim Hujan)
        - **Komoditas Utama**: Padi, Jagung, Kedelai
        - **Waktu Tanam Optimal**: November - Desember
        - **Karakteristik**: Curah hujan tinggi, risiko banjir di dataran rendah
        
        **Musim Tanam II (MT-II):**
        - **Periode**: April - September (Musim Kemarau)
        - **Komoditas Utama**: Padi (dengan irigasi), Palawija, Hortikultura
        - **Waktu Tanam Optimal**: April - Mei
        - **Karakteristik**: Curah hujan rendah, perlu irigasi memadai
        
        ### 🐛 Risiko OPT Musiman (Kementan)
        
        **Musim Hujan (Nov-Mar):**
        - Penyakit: Blast, Hawar Daun Bakteri, Busuk Batang
        - Hama: Keong Mas, Tikus (awal musim)
        
        **Musim Kemarau (Jun-Sep):**
        - Hama: Wereng Coklat, Penggerek Batang, Walang Sangit
        - Penyakit: Kresek (jika irigasi tidak lancar)
        
        ### 💡 Rekomendasi Kementan
        
        - **Padi**: Tanam MT-I (Nov-Des) untuk hasil optimal
        - **Jagung**: Tanam MT-I (Okt-Nov) atau MT-II (Apr-Mei)
        - **Cabai**: Tanam Apr-Mei (panen Jul-Agu, harga tinggi)
        - **Bawang Merah**: Tanam Jun-Jul (musim kemarau, kualitas baik)
        
        ---
        
        **Sumber:** [SI KATAM Terpadu Kementan](http://katam.info)
        
        📝 **Catatan:** 
        - Data ini adalah pola umum nasional
        - Untuk rekomendasi spesifik wilayah Anda, kunjungi website KATAM
        - KATAM menyediakan data per kecamatan yang di-update 3x/tahun
        - Akses via: Website, App Android, atau SMS ke 082123456500
        """)
    
    # Pranata Mangsa
    with st.expander("🌾 Kearifan Lokal: Pranata Mangsa Jawa"):
        st.markdown("""
        **Kalender Pertanian Tradisional Jawa**
        
        Pranata Mangsa adalah sistem penanggalan tradisional Jawa yang ditetapkan oleh 
        **Sunan Pakubuwono VII (1855)** untuk Kasunanan Surakarta sebagai pedoman pertanian.
        
        ### 📅 12 Mangsa (Musim) dalam Setahun
        """)
        
        # Create Pranata Mangsa table
        mangsa_data = [
            {"No": 1, "Mangsa": "Kasa", "Periode": "22 Jun - 1 Agu", "Hari": 41, "Musim": "Kemarau", "Aktivitas": "Bakar jerami, tanam palawija (jagung, kacang, ubi)"},
            {"No": 2, "Mangsa": "Karo", "Periode": "2 - 24 Agu", "Hari": 23, "Musim": "Kemarau (Paceklik)", "Aktivitas": "Palawija tumbuh, randu & mangga bersemi"},
            {"No": 3, "Mangsa": "Katelu", "Periode": "25 Agu - 17 Sep", "Hari": 24, "Musim": "Kemarau Puncak", "Aktivitas": "Panen palawija awal"},
            {"No": 4, "Mangsa": "Kapat", "Periode": "18 Sep - 12 Okt", "Hari": 24, "Musim": "Transisi", "Aktivitas": "Cek saluran irigasi, hujan kecil mulai"},
            {"No": 5, "Mangsa": "Kalima", "Periode": "13 Okt - 8 Nov", "Hari": 27, "Musim": "Awal Hujan", "Aktivitas": "⭐ SEMAI BENIH PADI"},
            {"No": 6, "Mangsa": "Kanem", "Periode": "9 Nov - 21 Des", "Hari": 43, "Musim": "Hujan", "Aktivitas": "⭐ BAJAK SAWAH, TANAM PADI"},
            {"No": 7, "Mangsa": "Kapitu", "Periode": "22 Des - 2 Feb", "Hari": 43, "Musim": "Hujan Lebat", "Aktivitas": "Padi tumbuh, waspadai banjir"},
            {"No": 8, "Mangsa": "Kawolu", "Periode": "3 - 28 Feb", "Hari": 26, "Musim": "Hujan", "Aktivitas": "Padi berbunga"},
            {"No": 9, "Mangsa": "Kasanga", "Periode": "2 - 26 Mar", "Hari": 25, "Musim": "Hujan + Kilat", "Aktivitas": "Pasang orang-orangan sawah"},
            {"No": 10, "Mangsa": "Kadasa", "Periode": "26 Mar - 18 Apr", "Hari": 24, "Musim": "Pancaroba", "Aktivitas": "⭐ PANEN PADI RAYA"},
            {"No": 11, "Mangsa": "Dhesta", "Periode": "19 Apr - 11 Mei", "Hari": 23, "Musim": "Kemarau Awal", "Aktivitas": "⭐ PANEN RAYA, potong padi"},
            {"No": 12, "Mangsa": "Saddha", "Periode": "12 Mei - 21 Jun", "Hari": 41, "Musim": "Kemarau", "Aktivitas": "Panen selesai, istirahat lahan"},
        ]
        
        df_mangsa = pd.DataFrame(mangsa_data)
        st.dataframe(df_mangsa, use_container_width=True, hide_index=True)
        
        st.markdown("""
        ### 🌦️ 4 Musim Utama Pranata Mangsa
        
        1. **Katiga (Kering)**: Mangsa Kasa - Katelu (Jun-Sep)
           - Karakteristik: Kemarau, tanah kering, paceklik
           - Komoditas: Palawija (jagung, kacang, ubi)
        
        2. **Labuh (Awal Hujan)**: Mangsa Kapat - Kalima (Sep-Nov)
           - Karakteristik: Hujan mulai turun, persiapan tanam
           - Komoditas: Semai padi, persiapan sawah
        
        3. **Rendheng (Hujan Puncak)**: Mangsa Kanem - Kasanga (Nov-Mar)
           - Karakteristik: Hujan lebat, banjir, petir
           - Komoditas: Padi (tanam & tumbuh)
        
        4. **Mareng (Transisi)**: Mangsa Kadasa - Dhesta (Mar-Mei)
           - Karakteristik: Hujan berkurang, panas
           - Komoditas: Panen padi raya
        
        ### 💡 Korelasi dengan Rekomendasi AgriSensa
        
        **Untuk Cabai (Hortikultura):**
        - **Tanam Optimal**: Mangsa Dhesta - Saddha (Apr-Jun)
          - Panen di Mangsa Katelu - Kapat (Agu-Okt)
          - Sesuai rekomendasi AgriSensa: Tanam Apr → Panen Jul-Agu (harga tinggi!)
        
        - **Hindari**: Mangsa Kanem - Kapitu (Nov-Feb)
          - Hujan lebat, risiko jamur/patek sangat tinggi
          - Sesuai data AgriSensa: Risiko jamur 80-85% di periode ini
        
        **Untuk Padi:**
        - **Tanam Optimal**: Mangsa Kanem (Nov-Des) - MT I
        - **Panen**: Mangsa Kadasa - Dhesta (Mar-Mei)
        
        ### 📜 Kearifan Lokal
        
        Pranata Mangsa menggunakan **tanda alam** sebagai indikator:
        - 🌳 Pohon asam bertunas → Mangsa Kalima (mulai hujan)
        - 🐍 Ular keluar → Mangsa Kalima (awal hujan)
        - 🦗 Jangkrik & tonggeret → Mangsa Kawolu (padi berbunga)
        - ✨ Kunang-kunang beterbangan → Mangsa Saddha (panen selesai)
        
        ---
        
        **Sumber:** Kasunanan Surakarta Hadiningrat (1855)
        
        📝 **Catatan:** 
        - Pranata Mangsa masih relevan untuk Jawa Tengah (termasuk Banyumas)
        - Kombinasikan dengan data cuaca modern (BMKG) untuk akurasi lebih tinggi
        - Sistem ini sudah digunakan petani Jawa selama **170+ tahun**!
        """)



# ========== TAB 2: POLA MUSIM & RISIKO ==========
with tab2:
    st.subheader("📊 Pola Musim & Risiko Sepanjang Tahun")
    
    # Create annual pattern dataframe
    months = list(range(1, 13))
    month_names = [datetime(2024, m, 1).strftime('%b') for m in months]
    
    annual_data = {
        'month': months,
        'month_name': month_names,
        'season': [INDONESIA_SEASONAL_PATTERN[m]['season'] for m in months],
        'rainfall': [INDONESIA_SEASONAL_PATTERN[m]['rainfall_mm'] for m in months],
        'risk_score': [get_risk_score(m) for m in months],
        'price': [get_price_prediction(m)['predicted'] for m in months]
    }
    
    df_annual = pd.DataFrame(annual_data)
    
    # Plot 1: Rainfall pattern
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=df_annual['month_name'],
        y=df_annual['rainfall'],
        name='Curah Hujan',
        marker_color='lightblue'
    ))
    fig1.update_layout(
        title="Pola Curah Hujan Sepanjang Tahun",
        xaxis_title="Bulan",
        yaxis_title="Curah Hujan (mm)",
        height=400
    )
    st.plotly_chart(fig1, use_container_width=True)
    
    # Plot 2: Risk heatmap
    st.markdown("### 🔥 Heatmap Risiko Hama/Penyakit")
    
    risk_matrix = []
    for m in months:
        pests = BANYUMAS_PEST_PATTERN[m]
        risk_matrix.append([
            pests['thrips'],
            pests['kutu_kebul'],
            pests['jamur'],
            pests['patek'],
            pests['layu_bakteri']
        ])
    
    fig2 = go.Figure(data=go.Heatmap(
        z=np.array(risk_matrix).T,
        x=month_names,
        y=['Thrips', 'Kutu Kebul', 'Jamur', 'Patek', 'Layu Bakteri'],
        colorscale='Reds',
        text=np.array(risk_matrix).T,
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Risiko (%)")
    ))
    fig2.update_layout(
        title="Pola Risiko OPT Sepanjang Tahun (Banyumas)",
        xaxis_title="Bulan",
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Key insights
    st.info("""
    **💡 Insight Pola Musim:**
    - **Juni-Agustus (Kemarau)**: Risiko hama tinggi (Thrips, Kutu Kebul)
    - **September-Oktober (Transisi)**: **DOUBLE TROUBLE** - Hama + Jamur tinggi!
    - **November-Maret (Hujan)**: Risiko jamur tinggi (Patek, Layu Bakteri)
    """)


# ========== TAB 3: PREDIKSI HARGA ==========
with tab3:
    st.subheader("💰 Prediksi Harga Cabai Merah Sepanjang Tahun")
    
    # Price trend
    fig3 = go.Figure()
    
    fig3.add_trace(go.Scatter(
        x=df_annual['month_name'],
        y=df_annual['price'],
        mode='lines+markers',
        name='Harga Prediksi',
        line=dict(color='green', width=3),
        marker=dict(size=10)
    ))
    
    # Add price range (min-max)
    price_min = [get_price_prediction(m)['min'] for m in months]
    price_max = [get_price_prediction(m)['max'] for m in months]
    
    fig3.add_trace(go.Scatter(
        x=df_annual['month_name'] + df_annual['month_name'][::-1],
        y=price_max + price_min[::-1],
        fill='toself',
        fillcolor='rgba(0,255,0,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Range Harga',
        showlegend=True
    ))
    
    fig3.update_layout(
        title="Tren Harga Cabai Merah (Prediksi)",
        xaxis_title="Bulan Panen",
        yaxis_title="Harga (Rp/kg)",
        height=500
    )
    
    st.plotly_chart(fig3, use_container_width=True)
    
    # Price table
    st.markdown("### 📋 Tabel Prediksi Harga")
    
    price_table = []
    for m in months:
        price = get_price_prediction(m)
        price_table.append({
            'Bulan': datetime(2024, m, 1).strftime('%B'),
            'Harga Prediksi': f"Rp {price['predicted']:,.0f}",
            'Min': f"Rp {price['min']:,.0f}",
            'Max': f"Rp {price['max']:,.0f}",
            'Musim': INDONESIA_SEASONAL_PATTERN[m]['season'].replace('_', ' ')
        })
    
    st.dataframe(pd.DataFrame(price_table), use_container_width=True, hide_index=True)
    
    st.success("""
    **💡 Strategi Harga:**
    - **Harga Tertinggi**: September (Rp 63,000/kg) - Transisi, produksi turun drastis
    - **Harga Terendah**: Maret (Rp 30,000/kg) - Hujan, banyak yang tanam
    - **Nataru Bonus**: Desember-Januari (+30-40% dari base)
    - **Base Price**: Rp 35,000/kg (dari database Page 11)
    """)


# ========== TAB 4: PANDUAN ==========
with tab4:
    st.subheader("📚 Panduan Penggunaan Kalender Tanam Cerdas")
    
    st.markdown("""
    ### 🎯 Cara Menggunakan
    
    1. **Pilih Komoditas** yang ingin ditanam
    2. **Pilih Bulan Tanam** yang direncanakan
    3. **Lihat Analisis**:
       - Risiko hama/penyakit saat panen
       - Prediksi harga saat panen
       - Rekomendasi (GO / HINDARI / HATI-HATI)
    
    ### 🧠 Basis Pengetahuan
    
    Model ini menggunakan **Rule-Based Expert System** yang menggabungkan:
    
    1. **Pola Musim Indonesia** (Opsi 1)
       - Musim Kemarau: Juni-Agustus
       - Musim Hujan: November-Maret
       - Transisi: April-Mei, September-Oktober
    
    2. **Pengalaman Lapangan Banyumas** (Opsi 4)
       - Pola hama/penyakit spesifik lokal
       - Observasi dari praktisi (8000 baglog jamur, 2 ha cabai, dll)
       - Validasi dengan kondisi riil
    
    3. **Analisis Harga Historis**
       - Pola harga dari data BAPANAS
       - Faktor Nataru (Desember-Januari)
       - Supply-demand musiman
    
    ### ⚠️ Disclaimer
    
    - Model ini adalah **alat bantu keputusan**, bukan jaminan
    - Hasil bersifat **estimatif** berdasarkan pola umum
    - Kondisi aktual bisa berbeda (perubahan iklim, outbreak lokal, dll)
    - Selalu lakukan **validasi lapangan** dan **monitoring rutin**
    
    ### 📞 Feedback
    
    Model ini akan terus di-update berdasarkan:
    - Data riil dari user AgriSensa
    - Feedback petani
    - Update pola iklim BMKG
    
    Jika ada saran atau koreksi, silakan hubungi tim AgriSensa!
    """)

# Footer
st.markdown("---")
st.caption("""
💡 **Tips**: Gunakan tab "Pola Musim & Risiko" untuk melihat gambaran tahunan, 
lalu gunakan tab "Rekomendasi Tanam" untuk analisis spesifik rencana tanam Anda.
""")
