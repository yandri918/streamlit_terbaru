# Kalkulator Potensi Panen Padi
# Module 24 - Comprehensive Rice Yield Calculator
# Version: 1.0.0

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Kalkulator Potensi Panen Padi", page_icon="🌾", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ========== DATA & CONSTANTS ==========

PLANTING_PATTERNS = {
    "Jajar Legowo 2:1": {
        "spacing_row": 25,
        "spacing_plant": 12.5,
        "spacing_legowo": 50,
        "description": "2 baris tanam, 1 baris kosong",
        "population_factor": 1.33,
        "yield_increase": "15-20%"
    },
    "Jajar Legowo 4:1": {
        "spacing_row": 25,
        "spacing_plant": 12.5,
        "spacing_legowo": 50,
        "description": "4 baris tanam, 1 baris kosong",
        "population_factor": 1.6,
        "yield_increase": "20-25%"
    },
    "Tegel 25×25": {
        "spacing_row": 25,
        "spacing_plant": 25,
        "description": "Pola persegi standar",
        "population_factor": 1.0,
        "yield_increase": "Baseline"
    },
    "Tegel 20×20": {
        "spacing_row": 20,
        "spacing_plant": 20,
        "description": "Pola persegi rapat",
        "population_factor": 1.0,
        "yield_increase": "Baseline"
    },
    "Custom": {
        "spacing_row": 25,
        "spacing_plant": 25,
        "description": "Atur jarak tanam sendiri",
        "population_factor": 1.0,
        "yield_increase": "Tergantung input"
    }
}

OPTIMAL_RANGES = {
    "plants_per_hill": (2, 3, "Bibit per rumpun yang ideal"),
    "tillers": (15, 25, "Anakan produktif optimal"),
    "grains_per_panicle": (100, 200, "Bulir per malai untuk varietas unggul"),
    "grain_weight_1000": (25, 30, "Berat 1000 bulir untuk hasil maksimal"),
    "loss_percentage": (10, 20, "Target kehilangan realistis")
}

RICE_VARIETIES = {
    "IR64": {"tillers": 18, "grains": 130, "weight": 26, "description": "Varietas populer, tahan rebah"},
    "Ciherang": {"tillers": 20, "grains": 150, "weight": 27, "description": "Varietas unggul nasional"},
    "Inpari 32": {"tillers": 22, "grains": 160, "weight": 28, "description": "Varietas genjah, tahan wereng"},
    "Mekongga": {"tillers": 19, "grains": 140, "weight": 28, "description": "Cocok lahan kering"},
    "Ciliwung": {"tillers": 21, "grains": 155, "weight": 27, "description": "Tahan hama, hasil tinggi"}
}

# ========== CALCULATION FUNCTIONS ==========

def calculate_population(spacing_row, spacing_plant, pattern_factor=1.0):
    """Calculate plants per hectare"""
    area_per_plant = (spacing_row / 100) * (spacing_plant / 100)  # m²
    population = (10000 / area_per_plant) * pattern_factor
    return int(population)

def calculate_yield(population, plants_per_hill, tillers, grains, weight_1000, loss_pct):
    """Calculate potential yield with detailed breakdown"""
    # Total hills
    total_hills = population
    
    # Total productive tillers
    total_tillers = total_hills * tillers
    
    # Total grains
    total_grains = total_tillers * grains
    
    # GKP Net (Gabah Kering Panen Bersih)
    gkp_gross_kg = (total_grains * weight_1000) / 1_000_000
    gkp_net_kg = gkp_gross_kg * (1 - loss_pct / 100)
    
    # GKG (Gabah Kering Giling) - Standar BPS: Konversi GKP ke GKG sekitar 86.02%
    gkg_kg = gkp_net_kg * 0.8602
    
    # Beras - Standar BPS: Rendemen Giling GKG ke Beras sekitar 62.74% - 64.02%
    # Kita gunakan angka optimis moderat 64%
    rice_kg = gkg_kg * 0.64
    
    return {
        "population": total_hills,
        "tillers_total": total_tillers,
        "grains_total": total_grains,
        "gkp_gross_ton": gkp_gross_kg / 1000,
        "gkp_net_ton": gkp_net_kg / 1000,
        "gkg_ton": gkg_kg / 1000,
        "rice_ton": rice_kg / 1000,
        "loss_kg": (gkp_gross_kg - gkp_net_kg),
        "revenue_estimate": gkp_net_kg * 6000  # Update harga GKP Rp 6000/kg (Trend 2024/2025)
    }

def get_recommendation(pattern, tillers, grains, weight, loss):
    """Generate recommendations based on inputs"""
    recommendations = []
    warnings = []
    
    # Check pattern
    if "Jajar Legowo" in pattern:
        recommendations.append("✅ Pola Jajar Legowo sangat baik untuk hasil maksimal")
    else:
        recommendations.append("💡 Pertimbangkan Jajar Legowo untuk hasil +15-25%")
    
    # Check tillers
    if tillers < OPTIMAL_RANGES["tillers"][0]:
        warnings.append(f"⚠️ Anakan produktif rendah (<{OPTIMAL_RANGES['tillers'][0]}). Tingkatkan pemupukan N")
    elif tillers > OPTIMAL_RANGES["tillers"][1]:
        warnings.append(f"⚠️ Anakan terlalu banyak (>{OPTIMAL_RANGES['tillers'][1]}). Risiko rebah tinggi")
    else:
        recommendations.append("✅ Jumlah anakan produktif optimal")
    
    # Check grains
    if grains < OPTIMAL_RANGES["grains_per_panicle"][0]:
        warnings.append("⚠️ Bulir per malai rendah. Periksa pemupukan P dan K")
    else:
        recommendations.append("✅ Jumlah bulir per malai baik")
    
    # Check grain weight
    if weight < OPTIMAL_RANGES["grain_weight_1000"][0]:
        warnings.append("⚠️ Berat bulir rendah. Pastikan pengisian bulir optimal")
    else:
        recommendations.append("✅ Berat bulir baik")
    
    # Check loss
    if loss > OPTIMAL_RANGES["loss_percentage"][1]:
        warnings.append(f"⚠️ Kehilangan tinggi (>{OPTIMAL_RANGES['loss_percentage'][1]}%). Perbaiki teknik panen")
    else:
        recommendations.append("✅ Persentase kehilangan terkendali")
    
    return recommendations, warnings

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
    .metric-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #10b981;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #059669;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #6b7280;
        margin-top: 0.5rem;
    }
    .recommendation-box {
        background: #f0fdf4;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #10b981;
        margin-bottom: 0.5rem;
    }
    .warning-box {
        background: #fef3c7;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #f59e0b;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown('<h1 class="main-header">🌾 Kalkulator Potensi Panen Padi</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #6b7280; margin-bottom: 2rem;">Hitung potensi hasil panen dengan akurat berdasarkan pola tanam dan parameter budidaya</p>', unsafe_allow_html=True)

# ========== TABS ==========
tab1, tab2, tab3, tab4 = st.tabs(["🧮 Kalkulator", "💡 Rekomendasi", "📊 Perbandingan Skenario", "📚 Panduan"])

# ========== TAB 1: KALKULATOR ==========
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input Parameter")
        
        # Pola Tanam
        pattern = st.selectbox(
            "Pola Tanam",
            options=list(PLANTING_PATTERNS.keys()),
            help="Pilih pola tanam yang akan digunakan"
        )
        
        pattern_data = PLANTING_PATTERNS[pattern]
        st.info(f"**{pattern_data['description']}** - Peningkatan hasil: {pattern_data['yield_increase']}")
        
        # Jarak Tanam
        if pattern == "Custom":
            spacing_row = st.number_input("Jarak Antar Baris (cm)", min_value=15, max_value=40, value=25, step=1)
            spacing_plant = st.number_input("Jarak Dalam Baris (cm)", min_value=10, max_value=40, value=25, step=1)
        else:
            spacing_row = pattern_data["spacing_row"]
            spacing_plant = pattern_data["spacing_plant"]
            st.text_input("Jarak Tanam", value=f"{spacing_row} × {spacing_plant} cm", disabled=True)
        
        # Luas Lahan
        area_ha = st.number_input("Luas Lahan (hektar)", min_value=0.1, max_value=100.0, value=1.0, step=0.1)
        
        # Quick Fill dari Varietas
        st.markdown("---")
        st.markdown("**🌾 Quick Fill dari Varietas:**")
        variety = st.selectbox("Pilih Varietas (opsional)", ["Manual Input"] + list(RICE_VARIETIES.keys()))
        
        if variety != "Manual Input":
            var_data = RICE_VARIETIES[variety]
            st.info(f"📌 {var_data['description']}")
            default_tillers = var_data["tillers"]
            default_grains = var_data["grains"]
            default_weight = var_data["weight"]
        else:
            default_tillers = 20
            default_grains = 150
            default_weight = 27
        
        st.markdown("---")
        
        # Parameter Tanaman
        plants_per_hill = st.slider(
            "Bibit per Rumpun",
            min_value=1, max_value=5, value=2,
            help="Jumlah bibit yang ditanam per rumpun"
        )
        
        tillers = st.slider(
            "Anakan Produktif per Rumpun",
            min_value=10, max_value=30, value=default_tillers,
            help="Jumlah anakan yang menghasilkan malai"
        )
        
        grains = st.slider(
            "Bulir per Malai",
            min_value=80, max_value=250, value=default_grains,
            help="Jumlah bulir padi per malai"
        )
        
        weight_1000 = st.slider(
            "Berat 1000 Bulir (gram)",
            min_value=20, max_value=35, value=default_weight,
            help="Berat 1000 bulir padi kering"
        )
        
        # Kehilangan
        st.markdown("---")
        st.markdown("**📉 Persentase Kehilangan:**")
        
        loss_method = st.radio("Metode Input", ["Total", "Detail"])
        
        if loss_method == "Total":
            loss_total = st.slider("Total Kehilangan (%)", min_value=0, max_value=40, value=15)
        else:
            loss_hampa = st.slider("Gabah Hampa (%)", min_value=0, max_value=20, value=8)
            loss_panen = st.slider("Kehilangan Panen (%)", min_value=0, max_value=10, value=3)
            loss_pasca = st.slider("Kehilangan Pasca Panen (%)", min_value=0, max_value=10, value=4)
            loss_total = loss_hampa + loss_panen + loss_pasca
            st.info(f"**Total Kehilangan: {loss_total}%**")
    
    with col2:
        st.markdown("### 📊 Hasil Perhitungan")
        
        # Calculate
        population = calculate_population(spacing_row, spacing_plant, pattern_data["population_factor"])
        results = calculate_yield(population, plants_per_hill, tillers, grains, weight_1000, loss_total)
        
        # Scale by area
        results_scaled = {k: v * area_ha for k, v in results.items()}
        
        # Display Metrics
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{results["population"]:,}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Rumpun per Hektar</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{results["tillers_total"]:,}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Total Malai per Hektar</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_b:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{results["grains_total"]:,}</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Total Bulir per Hektar</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-value">{results["loss_kg"]:,.0f} kg</div>', unsafe_allow_html=True)
            st.markdown('<div class="metric-label">Kehilangan Hasil</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Potensi Hasil")
        
        # Main Results
        st.metric("GKP Kotor (Gabah Kering Panen)", f"{results_scaled['gkp_gross_ton']:.2f} ton", 
                 help="Hasil panen sebelum dikurangi kehilangan")
        st.metric("GKP Bersih", f"{results_scaled['gkp_net_ton']:.2f} ton", 
                 delta=f"-{loss_total}% kehilangan",
                 help="Hasil panen setelah dikurangi kehilangan")
        st.metric("GKG (Gabah Kering Giling)", f"{results_scaled['gkg_ton']:.2f} ton",
                 help="Hasil setelah pengeringan (rendemen 85%)")
        st.metric("Beras", f"{results_scaled['rice_ton']:.2f} ton",
                 help="Hasil akhir beras (rendemen 65%)")
        
        st.markdown("---")
        st.markdown("### 💰 Estimasi Pendapatan")
        st.success(f"**Rp {results_scaled['revenue_estimate']:,.0f}**")
        st.caption("*Asumsi harga GKP Rp 5.000/kg")
        
        # Visualization
        st.markdown("---")
        st.markdown("### 📈 Visualisasi Hasil")
        
        # Pie chart for yield breakdown
        fig_pie = go.Figure(data=[go.Pie(
            labels=['GKP Bersih', 'Kehilangan'],
            values=[results['gkp_net_ton'], results['loss_kg']/1000],
            marker=dict(colors=['#10b981', '#ef4444']),
            hole=0.4
        )])
        fig_pie.update_layout(
            title="Breakdown Hasil vs Kehilangan",
            height=300
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# ========== TAB 2: REKOMENDASI ==========
with tab2:
    st.markdown("### 💡 Rekomendasi & Analisis")
    
    recommendations, warnings = get_recommendation(pattern, tillers, grains, weight_1000, loss_total)
    
    if recommendations:
        st.markdown("#### ✅ Rekomendasi")
        for rec in recommendations:
            st.markdown(f'<div class="recommendation-box">{rec}</div>', unsafe_allow_html=True)
    
    if warnings:
        st.markdown("#### ⚠️ Peringatan")
        for warn in warnings:
            st.markdown(f'<div class="warning-box">{warn}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 🎯 Tips Optimasi Hasil")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Meningkatkan Anakan Produktif:**
        - Pemupukan N yang cukup saat fase vegetatif
        - Pengairan yang baik (macak-macak)
        - Jarak tanam optimal
        - Varietas unggul
        
        **Meningkatkan Bulir per Malai:**
        - Pemupukan P dan K yang cukup
        - Pengairan saat fase generatif
        - Pengendalian hama (walang sangit)
        """)
    
    with col2:
        st.markdown("""
        **Meningkatkan Berat Bulir:**
        - Pemupukan K saat pengisian bulir
        - Pengairan optimal saat pengisian
        - Panen tepat waktu
        
        **Mengurangi Kehilangan:**
        - Panen saat kadar air 22-25%
        - Gunakan alat panen yang tepat
        - Pengeringan segera setelah panen
        - Penyimpanan yang baik
        """)

# ========== TAB 3: PERBANDINGAN SKENARIO ==========
with tab3:
    st.markdown("### 📊 Perbandingan Skenario")
    
    # Compare different patterns
    st.markdown("#### Perbandingan Pola Tanam")
    
    comparison_data = []
    for patt_name, patt_data in PLANTING_PATTERNS.items():
        if patt_name == "Custom":
            continue
        pop = calculate_population(patt_data["spacing_row"], patt_data["spacing_plant"], patt_data["population_factor"])
        res = calculate_yield(pop, plants_per_hill, tillers, grains, weight_1000, loss_total)
        comparison_data.append({
            "Pola Tanam": patt_name,
            "Populasi": f"{pop:,}",
            "GKP Bersih (ton/ha)": f"{res['gkp_net_ton']:.2f}",
            "GKG (ton/ha)": f"{res['gkg_ton']:.2f}",
            "Peningkatan": patt_data["yield_increase"]
        })
    
    df_comparison = pd.DataFrame(comparison_data)
    st.dataframe(df_comparison, use_container_width=True)
    
    # Bar chart comparison
    yields = [float(row["GKP Bersih (ton/ha)"]) for row in comparison_data]
    patterns = [row["Pola Tanam"] for row in comparison_data]
    
    fig_bar = go.Figure(data=[
        go.Bar(x=patterns, y=yields, marker_color='#10b981')
    ])
    fig_bar.update_layout(
        title="Perbandingan Hasil Berbagai Pola Tanam",
        xaxis_title="Pola Tanam",
        yaxis_title="GKP Bersih (ton/ha)",
        height=400
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    st.markdown("#### Analisis Sensitivitas")
    
    # Sensitivity analysis for loss percentage
    loss_range = range(5, 31, 5)
    sensitivity_data = []
    
    for loss in loss_range:
        res = calculate_yield(population, plants_per_hill, tillers, grains, weight_1000, loss)
        sensitivity_data.append({
            "Kehilangan (%)": loss,
            "GKP Bersih (ton/ha)": res['gkp_net_ton']
        })
    
    df_sensitivity = pd.DataFrame(sensitivity_data)
    
    fig_line = px.line(df_sensitivity, x="Kehilangan (%)", y="GKP Bersih (ton/ha)",
                      markers=True, title="Dampak Kehilangan terhadap Hasil")
    fig_line.update_traces(line_color='#10b981', line_width=3)
    st.plotly_chart(fig_line, use_container_width=True)

# ========== TAB 4: PANDUAN ==========
with tab4:
    st.markdown("### 📚 Panduan Penggunaan")
    
    st.markdown("""
    #### Cara Menggunakan Kalkulator
    
    1. **Pilih Pola Tanam**
       - Jajar Legowo 2:1 atau 4:1 untuk hasil maksimal
       - Tegel untuk kemudahan penerapan
       - Custom untuk jarak tanam khusus
    
    2. **Atur Parameter Tanaman**
       - Gunakan Quick Fill dari varietas untuk nilai default
       - Atau atur manual sesuai kondisi lahan
    
    3. **Tentukan Persentase Kehilangan**
       - Pilih "Total" untuk input cepat
       - Pilih "Detail" untuk breakdown lengkap
    
    4. **Lihat Hasil**
       - GKP Bersih: Hasil yang bisa dijual
       - GKG: Hasil setelah pengeringan
       - Beras: Hasil akhir konsumsi
    
    #### Parameter Optimal
    """)
    
    optimal_df = pd.DataFrame([
        {"Parameter": "Bibit per Rumpun", "Range Optimal": "2-3 batang", "Keterangan": "Lebih banyak = kompetisi"},
        {"Parameter": "Anakan Produktif", "Range Optimal": "15-25 anakan", "Keterangan": "Tergantung varietas & pemupukan"},
        {"Parameter": "Bulir per Malai", "Range Optimal": "100-200 bulir", "Keterangan": "Varietas unggul: 150-200"},
        {"Parameter": "Berat 1000 Bulir", "Range Optimal": "25-30 gram", "Keterangan": "Varietas premium: 28-30g"},
        {"Parameter": "Kehilangan", "Range Optimal": "10-20%", "Keterangan": "Target: <15%"}
    ])
    
    st.dataframe(optimal_df, use_container_width=True)
    
    st.markdown("""
    #### Breakdown Kehilangan
    
    - **Gabah Hampa (5-10%)**: Penyerbukan tidak sempurna, serangan hama
    - **Kehilangan Panen (2-5%)**: Rontok saat panen, tertinggal di sawah
    - **Kehilangan Pasca Panen (3-5%)**: Pengeringan, penyimpanan, penggilingan
    
    **Target Total:** 10-15% untuk hasil optimal
    
    #### Referensi Varietas
    """)
    
    variety_df = pd.DataFrame([
        {"Varietas": name, 
         "Anakan": data["tillers"], 
         "Bulir/Malai": data["grains"],
         "Berat 1000": f"{data['weight']}g",
         "Keterangan": data["description"]}
        for name, data in RICE_VARIETIES.items()
    ])
    
    st.dataframe(variety_df, use_container_width=True)

# ========== FOOTER ==========
st.markdown("---")
st.caption("""
🌾 **Kalkulator Potensi Panen Padi v1.0**

💡 **Catatan**: Hasil perhitungan adalah estimasi berdasarkan parameter input. 
Hasil aktual di lapangan dapat bervariasi tergantung kondisi tanah, iklim, dan manajemen budidaya.

📊 **Sumber**: Balai Penelitian Tanaman Padi, Kementerian Pertanian RI
""")
