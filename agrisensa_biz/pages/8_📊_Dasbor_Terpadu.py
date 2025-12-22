# Dasbor Rekomendasi Terpadu
# Integrated dashboard with holistic recommendations

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import os

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Dasbor Terpadu", page_icon="📊", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== DATA LOADING ==========
def load_harvest_data():
    """Load harvest data if exists"""
    file_path = "data/harvest_data_streamlit.json"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def load_npk_data():
    """Load NPK analysis data if exists"""
    file_path = "data/npk_analysis_records.json"
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# ========== ANALYSIS FUNCTIONS ==========
def analyze_farm_health(harvest_data, npk_data):
    """Analyze overall farm health"""
    health_score = 0
    factors = {}
    
    # Harvest performance (40 points)
    if harvest_data:
        df = pd.DataFrame(harvest_data)
        avg_margin = df['profit_margin'].mean() if 'profit_margin' in df.columns else 0
        
        if avg_margin > 30:
            harvest_score = 40
        elif avg_margin > 20:
            harvest_score = 30
        elif avg_margin > 10:
            harvest_score = 20
        else:
            harvest_score = 10
        
        health_score += harvest_score
        factors['harvest'] = harvest_score
    else:
        factors['harvest'] = 0
    
    # Soil health (40 points)
    if npk_data:
        latest_npk = npk_data[-1]
        n_status = latest_npk['analysis']['n_status']
        p_status = latest_npk['analysis']['p_status']
        k_status = latest_npk['analysis']['k_status']
        
        status_scores = {'Tinggi': 15, 'Sedang': 10, 'Rendah': 5}
        soil_score = (status_scores.get(n_status, 0) + 
                     status_scores.get(p_status, 0) + 
                     status_scores.get(k_status, 0))
        
        # pH bonus
        ph = latest_npk.get('ph', 7)
        if 6.0 <= ph <= 7.0:
            soil_score += 10
        
        health_score += min(40, soil_score)
        factors['soil'] = min(40, soil_score)
    else:
        factors['soil'] = 0
    
    # Data completeness (20 points)
    data_score = 0
    if harvest_data:
        data_score += 10
    if npk_data:
        data_score += 10
    
    health_score += data_score
    factors['data'] = data_score
    
    return health_score, factors

def get_priority_recommendations(harvest_data, npk_data):
    """Get prioritized recommendations"""
    recommendations = []
    
    # NPK recommendations
    if npk_data:
        latest = npk_data[-1]
        if latest['analysis']['n_status'] == 'Rendah':
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Nutrisi',
                'title': 'Nitrogen Rendah',
                'description': 'Kandungan Nitrogen tanah rendah, segera tambahkan pupuk Urea',
                'action': 'Aplikasikan 200-300 kg Urea per hektar',
                'impact': 'Meningkatkan hasil panen 20-30%'
            })
        
        if latest['analysis']['p_status'] == 'Rendah':
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Nutrisi',
                'title': 'Fosfor Rendah',
                'description': 'Kandungan Fosfor tanah rendah, tambahkan pupuk SP-36',
                'action': 'Aplikasikan 150-200 kg SP-36 per hektar',
                'impact': 'Meningkatkan kualitas hasil 15-25%'
            })
    
    # Harvest recommendations
    if harvest_data:
        df = pd.DataFrame(harvest_data)
        if 'profit_margin' in df.columns:
            avg_margin = df['profit_margin'].mean()
            
            if avg_margin < 15:
                recommendations.append({
                    'priority': 'MEDIUM',
                    'category': 'Profitabilitas',
                    'title': 'Margin Keuntungan Rendah',
                    'description': f'Rata-rata margin hanya {avg_margin:.1f}%, perlu optimasi',
                    'action': 'Review biaya produksi dan strategi penjualan',
                    'impact': 'Potensi peningkatan margin 10-15%'
                })
    
    # General recommendations
    if not npk_data:
        recommendations.append({
            'priority': 'HIGH',
            'category': 'Data',
            'title': 'Belum Ada Data NPK',
            'description': 'Lakukan uji tanah untuk mendapatkan rekomendasi yang akurat',
            'action': 'Ambil sampel tanah dan uji di laboratorium',
            'impact': 'Dasar untuk pemupukan yang tepat'
        })
    
    if not harvest_data:
        recommendations.append({
            'priority': 'MEDIUM',
            'category': 'Data',
            'title': 'Belum Ada Data Panen',
            'description': 'Mulai catat data hasil panen untuk analisis profitabilitas',
            'action': 'Gunakan modul Database Panen untuk tracking',
            'impact': 'Monitoring performa dan trend'
        })
    
    # Sort by priority
    priority_order = {'HIGH': 0, 'MEDIUM': 1, 'LOW': 2}
    recommendations.sort(key=lambda x: priority_order[x['priority']])
    
    return recommendations

# ========== MAIN APP ==========
st.title("📊 Dasbor Rekomendasi Terpadu")
st.markdown("**Dashboard komprehensif dengan rekomendasi holistik untuk optimasi pertanian**")

# Load data
harvest_data = load_harvest_data()
npk_data = load_npk_data()

# Calculate health score
health_score, health_factors = analyze_farm_health(harvest_data, npk_data)

# Health score display
st.markdown("---")
st.subheader("🏥 Skor Kesehatan Pertanian")

col1, col2, col3, col4 = st.columns(4)

with col1:
    # Overall health
    health_color = "🟢" if health_score >= 80 else "🟡" if health_score >= 60 else "🔴"
    health_status = "Excellent" if health_score >= 80 else "Good" if health_score >= 60 else "Needs Improvement"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%); 
                padding: 2rem; border-radius: 12px; border: 2px solid #10b981; text-align: center;">
        <div style="font-size: 3rem;">{health_color}</div>
        <h2 style="color: #059669; margin: 0.5rem 0;">{health_score}/100</h2>
        <p style="color: #6b7280; margin: 0;">{health_status}</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    harvest_pct = (health_factors['harvest'] / 40) * 100
    st.metric("Performa Panen", f"{harvest_pct:.0f}%", 
             delta="40 poin max", help="Berdasarkan profitabilitas panen")

with col3:
    soil_pct = (health_factors['soil'] / 40) * 100
    st.metric("Kesehatan Tanah", f"{soil_pct:.0f}%",
             delta="40 poin max", help="Berdasarkan status NPK & pH")

with col4:
    data_pct = (health_factors['data'] / 20) * 100
    st.metric("Kelengkapan Data", f"{data_pct:.0f}%",
             delta="20 poin max", help="Kelengkapan data untuk analisis")

# Health breakdown chart
st.markdown("---")
st.subheader("📈 Breakdown Skor Kesehatan")

fig = go.Figure(go.Bar(
    x=['Performa Panen<br>(40 poin)', 'Kesehatan Tanah<br>(40 poin)', 'Kelengkapan Data<br>(20 poin)'],
    y=[health_factors['harvest'], health_factors['soil'], health_factors['data']],
    marker_color=['#3b82f6', '#10b981', '#f59e0b'],
    text=[f"{health_factors['harvest']}", f"{health_factors['soil']}", f"{health_factors['data']}"],
    textposition='auto',
))

fig.add_hline(y=40, line_dash="dash", line_color="green", annotation_text="Max (Panen & Tanah)")
fig.add_hline(y=20, line_dash="dash", line_color="orange", annotation_text="Max (Data)")

fig.update_layout(
    title="Kontribusi Setiap Faktor ke Skor Kesehatan",
    yaxis_title="Poin",
    height=300,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# Priority recommendations
st.markdown("---")
st.subheader("🎯 Rekomendasi Prioritas")

recommendations = get_priority_recommendations(harvest_data, npk_data)

if recommendations:
    for i, rec in enumerate(recommendations[:5]):  # Show top 5
        priority_colors = {
            'HIGH': ('#fee2e2', '#dc2626', '🔴'),
            'MEDIUM': ('#fef3c7', '#f59e0b', '🟡'),
            'LOW': ('#dbeafe', '#3b82f6', '🔵')
        }
        
        bg_color, border_color, icon = priority_colors[rec['priority']]
        
        st.markdown(f"""
        <div style="background: {bg_color}; padding: 1.5rem; border-radius: 8px; 
                    border-left: 4px solid {border_color}; margin: 1rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h4 style="margin: 0; color: #1f2937;">
                        {icon} {rec['title']}
                        <span style="background: {border_color}; color: white; padding: 0.2rem 0.5rem; 
                                     border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem;">
                            {rec['priority']}
                        </span>
                    </h4>
                    <p style="color: #6b7280; margin: 0.5rem 0;">{rec['description']}</p>
                    <p style="margin: 0.5rem 0;"><strong>Aksi:</strong> {rec['action']}</p>
                    <p style="color: #059669; margin: 0;"><strong>Dampak:</strong> {rec['impact']}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.success("✅ Tidak ada rekomendasi prioritas. Semua aspek dalam kondisi baik!")

# Quick stats
st.markdown("---")
st.subheader("📊 Statistik Cepat")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**📦 Data Panen**")
    if harvest_data:
        df = pd.DataFrame(harvest_data)
        st.metric("Total Catatan", len(harvest_data))
        st.metric("Total Hasil", f"{df['total_quantity'].sum():,.0f} kg")
        st.metric("Total Pendapatan", f"Rp {df['total_value'].sum():,.0f}")
    else:
        st.info("Belum ada data panen")

with col2:
    st.markdown("**🌱 Data NPK**")
    if npk_data:
        latest = npk_data[-1]
        st.metric("Total Analisis", len(npk_data))
        st.metric("N (Latest)", f"{latest['n_value']:.0f} ppm")
        st.metric("P (Latest)", f"{latest['p_value']:.1f} ppm")
    else:
        st.info("Belum ada data NPK")

with col3:
    st.markdown("**📈 Tren**")
    if harvest_data and len(harvest_data) >= 2:
        df = pd.DataFrame(harvest_data)
        df = df.sort_values('created_at')
        
        # Calculate trend
        recent_margin = df['profit_margin'].iloc[-3:].mean() if len(df) >= 3 else df['profit_margin'].iloc[-1]
        older_margin = df['profit_margin'].iloc[:3].mean() if len(df) >= 6 else df['profit_margin'].iloc[0]
        
        trend = "📈 Naik" if recent_margin > older_margin else "📉 Turun"
        
        st.metric("Tren Margin", trend)
        st.metric("Margin Terbaru", f"{recent_margin:.1f}%")
        st.metric("Perubahan", f"{(recent_margin - older_margin):.1f}%")
    else:
        st.info("Perlu lebih banyak data")

# Action items
st.markdown("---")
st.subheader("✅ Action Items")

st.markdown("""
**Langkah-langkah yang bisa dilakukan:**

1. **Jika belum ada data NPK:**
   - Kunjungi modul **Peta Data Tanah** atau **Analisis NPK**
   - Input data hasil uji lab tanah
   - Dapatkan rekomendasi pupuk yang tepat

2. **Jika belum ada data panen:**
   - Kunjungi modul **Database Panen**
   - Catat hasil panen terakhir
   - Mulai tracking profitabilitas

3. **Untuk optimasi:**
   - Gunakan **Kalkulator Pupuk** untuk hitung kebutuhan
   - Cek **Analisis Tren Harga** untuk timing penjualan
   - Gunakan **Prediksi Hasil Panen** untuk planning

4. **Monitoring rutin:**
   - Update data NPK setiap 3-6 bulan
   - Catat setiap hasil panen
   - Review dashboard ini secara berkala
""")

# Module shortcuts
st.markdown("---")
st.subheader("🚀 Akses Cepat ke Modul")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    **📊 Analisis**
    - Analisis NPK
    - Analisis Tren Harga
    - Prediksi Hasil Panen
    """)

with col2:
    st.markdown("""
    **🧮 Kalkulator**
    - Kalkulator Pupuk
    - Konversi Pupuk
    """)

with col3:
    st.markdown("""
    **📦 Data**
    - Database Panen
    - Peta Data Tanah
    """)

with col4:
    st.markdown("""
    **📈 Visualisasi**
    - Charts & Graphs
    - Export Data
    """)

# Tips
st.markdown("---")
with st.expander("💡 Tips Menggunakan Dashboard"):
    st.markdown("""
    **Untuk Hasil Optimal:**
    
    1. **Lengkapi Data:**
       - Semakin lengkap data, semakin akurat rekomendasi
       - Update data secara berkala
    
    2. **Ikuti Rekomendasi Prioritas:**
       - Fokus pada rekomendasi HIGH priority dulu
       - Implementasikan secara bertahap
    
    3. **Monitor Tren:**
       - Perhatikan perubahan skor kesehatan
       - Identifikasi pola dari data historical
    
    4. **Integrasi Antar Modul:**
       - Data NPK → Kalkulator Pupuk
       - Prediksi Harga → Timing Penjualan
       - Prediksi Hasil → Planning Produksi
    
    5. **Review Berkala:**
       - Cek dashboard minimal 1x per bulan
       - Evaluasi progress implementasi rekomendasi
    """)

# Footer
st.markdown("---")
st.caption("""
📊 **Dashboard Terpadu AgriSensa** - Mengintegrasikan semua data dan analisis untuk memberikan 
rekomendasi holistik yang membantu optimasi pertanian Anda.
""")
