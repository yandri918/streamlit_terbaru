import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.medicinal_plants_service import (
    MedicinalPlantsService,
    CULTIVATION_DATABASE,
    MARKET_PRICES,
    INVESTMENT_COSTS
)

st.set_page_config(
    page_title="Tanaman Obat & Herbal",
    page_icon="🌿",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .hero-header {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        margin: 10px 0;
    }
    .info-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .cultivation-box {
        background: #f0fdf4;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero-header">
    <h1>🌿 Tanaman Obat & Herbal</h1>
    <p>High-Value Medicinal Plants with Export Potential</p>
    <p><strong>Margin Profit: 200-400% | Pasar Ekspor: Jepang, Eropa, Timur Tengah</strong></p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📊 Market Intelligence",
    "🌱 Rimpang (Rhizome)",
    "🍃 Daun & Herba",
    "🌿 Akar Premium",
    "✅ GAP & Sertifikasi",
    "💰 Kalkulator Bisnis",
    "📅 Panen & Pasca Panen",
    "🔬 Database Khasiat"
])

# ===== TAB 1: MARKET INTELLIGENCE =====
with tab1:
    st.markdown("## 📊 Market Intelligence - Tanaman Obat Indonesia")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>$2.5 B</h3><p>Pasar Global 2024</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>200-400%</h3><p>Margin Profit</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>15%/tahun</h3><p>Pertumbuhan Pasar</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>Top 5</h3><p>Eksportir Dunia</p></div>', unsafe_allow_html=True)
    
    st.markdown("### 🌍 Target Pasar Ekspor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="info-card">
        <h4>🇯🇵 Jepang (Kampo Medicine)</h4>
        <ul>
        <li><strong>Demand Tinggi:</strong> Jahe Merah, Kunyit, Temulawak</li>
        <li><strong>Standar:</strong> Organic JAS, Residue-free</li>
        <li><strong>Harga Premium:</strong> 3-5x harga lokal</li>
        <li><strong>Volume Import:</strong> 50,000 ton/tahun</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
        <h4>🇪🇺 Eropa (Herbal Medicine)</h4>
        <ul>
        <li><strong>Demand Tinggi:</strong> Sambiloto, Pegagan, Ginseng Jawa</li>
        <li><strong>Standar:</strong> EU Organic, GACP</li>
        <li><strong>Harga Premium:</strong> 4-6x harga lokal</li>
        <li><strong>Trend:</strong> Natural immunity boosters</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
        <h4>🕌 Timur Tengah (Halal Medicine)</h4>
        <ul>
        <li><strong>Demand Tinggi:</strong> Jahe, Kencur, Pasak Bumi</li>
        <li><strong>Standar:</strong> Halal MUI, Organic</li>
        <li><strong>Harga Premium:</strong> 2-4x harga lokal</li>
        <li><strong>Keunggulan:</strong> Sertifikasi Halal Indonesia diakui</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-card">
        <h4>🇨🇳 China (TCM - Traditional Chinese Medicine)</h4>
        <ul>
        <li><strong>Demand Tinggi:</strong> Temulawak, Sambiloto</li>
        <li><strong>Standar:</strong> GAP-TCM</li>
        <li><strong>Volume:</strong> Pasar terbesar dunia</li>
        <li><strong>Kompetisi:</strong> Tinggi, fokus pada kualitas premium</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📈 Tren Harga & Margin")
    
    # Price comparison chart
    price_data = []
    for species, prices in MARKET_PRICES.items():
        price_data.append({
            "Komoditas": species,
            "Lokal (Segar)": prices["fresh_local"],
            "Lokal (Kering)": prices["dry_local"],
            "Ekspor (Kering)": prices["dry_export"],
            "Premium Grade A": prices["grade_a_premium"]
        })
    
    df_prices = pd.DataFrame(price_data)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Lokal (Segar)', x=df_prices['Komoditas'], y=df_prices['Lokal (Segar)']))
    fig.add_trace(go.Bar(name='Lokal (Kering)', x=df_prices['Komoditas'], y=df_prices['Lokal (Kering)']))
    fig.add_trace(go.Bar(name='Ekspor (Kering)', x=df_prices['Komoditas'], y=df_prices['Ekspor (Kering)']))
    fig.add_trace(go.Bar(name='Premium Grade A', x=df_prices['Komoditas'], y=df_prices['Premium Grade A']))
    
    fig.update_layout(
        title="Perbandingan Harga Tanaman Obat (IDR/kg)",
        xaxis_title="Komoditas",
        yaxis_title="Harga (IDR/kg)",
        barmode='group',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.success("""
    **💡 Key Insights:**
    - Harga ekspor 2-5x lebih tinggi dari harga lokal
    - Grade A Premium bisa mencapai 10-15x harga segar lokal
    - Sertifikasi organik menambah premium 20-30%
    - Sertifikasi halal menambah premium 10-20%
    """)

# ===== TAB 2: RHIZOME CROPS =====
with tab2:
    st.markdown("## 🌱 Tanaman Rimpang (Rhizome Crops)")
    
    rhizome_species = ["Jahe Merah", "Kunyit", "Temulawak", "Kencur"]
    
    selected_rhizome = st.selectbox(
        "Pilih Komoditas Rimpang:",
        rhizome_species,
        key="rhizome_select"
    )
    
    cultivation = CULTIVATION_DATABASE[selected_rhizome]
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["cycle_months"]} bulan</h3><p>Siklus Tanam</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["yield_dry"]}</h3><p>Ton/Ha (Kering)</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["planting_density"]}</h3><p>Populasi/Ha</p></div>', unsafe_allow_html=True)
    with col4:
        price = MARKET_PRICES[selected_rhizome]["dry_export"]
        st.markdown(f'<div class="metric-card"><h3>Rp {price:,}</h3><p>Harga Ekspor/kg</p></div>', unsafe_allow_html=True)
    
    # Cultivation details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Spesifikasi Teknis")
        with st.expander("Detail Spesifikasi", expanded=True):
            st.markdown(f"""
            - **Nama Latin**: *{cultivation["latin_name"]}*
            - **Jarak Tanam**: {cultivation["spacing"]}
            - **Ketinggian**: {cultivation["altitude"]}
            - **Curah Hujan**: {cultivation["rainfall"]}
            - **pH Tanah**: {cultivation["soil_ph"]}
            - **Jenis Tanah**: {cultivation["soil_type"]}
            - **Hasil Segar**: {cultivation["yield_fresh"]}
            - **Hasil Kering**: {cultivation["yield_dry"]}
            - **Rasio Pengeringan**: {cultivation["drying_ratio"]*100}%
            """)
        
        st.markdown("### 🧪 Kandungan Aktif")
        with st.expander("Senyawa Bioaktif", expanded=False):
            for compound in cultivation["active_compounds"]:
                st.markdown(f"- **{compound}**")
    
    with col2:
        st.markdown("### 🌾 Jadwal Pemupukan")
        with st.expander("Detail Pemupukan", expanded=True):
            fert = cultivation["fertilizer"]
            st.markdown(f"""
            **Pupuk Organik (Dasar)**:
            - {fert["organic"]}
            
            **Pupuk Kimia**:
            - Urea: {fert["urea"]}
            - SP-36: {fert["sp36"]}
            - KCl: {fert["kcl"]}
            
            **Aplikasi**:
            - Pupuk dasar: 2 minggu sebelum tanam
            - Susulan 1: 1 bulan setelah tanam (1/3 dosis)
            - Susulan 2: 2 bulan setelah tanam (1/3 dosis)
            - Susulan 3: 3 bulan setelah tanam (1/3 dosis)
            """)
        
        st.markdown("### 🐛 Hama & Penyakit")
        with st.expander("Pengendalian IPM", expanded=False):
            st.markdown("**Hama Utama:**")
            for pest in cultivation["pests"]:
                st.markdown(f"- {pest}")
            
            st.markdown("\n**Penyakit Utama:**")
            for disease in cultivation["diseases"]:
                st.markdown(f"- {disease}")
            
            st.info("""
            **Strategi IPM:**
            - Rotasi tanaman dengan legum
            - Sanitasi lahan (buang sisa tanaman)
            - Mulsa jerami untuk kontrol gulma
            - Pestisida nabati (PGPR, Trichoderma)
            - Monitoring rutin setiap minggu
            """)
    
    st.markdown("### ✅ Indikator Panen")
    st.success(f"**{cultivation['harvest_indicator']}**")
    
    st.markdown("### 💊 Manfaat Kesehatan")
    cols = st.columns(2)
    for idx, benefit in enumerate(cultivation["health_benefits"]):
        with cols[idx % 2]:
            st.markdown(f"✅ {benefit}")

# ===== TAB 3: LEAF & HERB CROPS =====
with tab3:
    st.markdown("## 🍃 Tanaman Daun & Herba")
    
    leaf_species = ["Sambiloto", "Pegagan"]
    
    selected_leaf = st.selectbox(
        "Pilih Komoditas Daun/Herba:",
        leaf_species,
        key="leaf_select"
    )
    
    cultivation = CULTIVATION_DATABASE[selected_leaf]
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["cycle_months"]} bulan</h3><p>Siklus Tanam</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["yield_dry"]}</h3><p>Ton/Ha (Kering)</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["planting_density"]}</h3><p>Populasi/Ha</p></div>', unsafe_allow_html=True)
    with col4:
        price = MARKET_PRICES[selected_leaf]["dry_export"]
        st.markdown(f'<div class="metric-card"><h3>Rp {price:,}</h3><p>Harga Ekspor/kg</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Panduan Budidaya")
        with st.expander("Detail Teknis", expanded=True):
            st.markdown(f"""
            - **Nama Latin**: *{cultivation["latin_name"]}*
            - **Jarak Tanam**: {cultivation["spacing"]}
            - **Ketinggian**: {cultivation["altitude"]}
            - **Curah Hujan**: {cultivation["rainfall"]}
            - **pH Tanah**: {cultivation["soil_ph"]}
            - **Jenis Tanah**: {cultivation["soil_type"]}
            - **Hasil Segar**: {cultivation["yield_fresh"]}
            - **Hasil Kering**: {cultivation["yield_dry"]}
            """)
        
        if selected_leaf == "Pegagan":
            st.info("""
            **Keunggulan Pegagan:**
            - Panen setiap 2 bulan (6x/tahun)
            - Cocok untuk lahan naungan (di bawah pohon)
            - Permintaan ekspor tinggi (brain tonic)
            - Mudah diperbanyak (stolon)
            """)
    
    with col2:
        st.markdown("### 🌾 Pemupukan & Perawatan")
        with st.expander("Detail Pemupukan", expanded=True):
            fert = cultivation["fertilizer"]
            st.markdown(f"""
            **Pupuk Organik**:
            - {fert["organic"]}
            
            **Pupuk Kimia**:
            - Urea: {fert["urea"]}
            - SP-36: {fert["sp36"]}
            - KCl: {fert["kcl"]}
            """)
        
        st.markdown("### 💊 Kandungan & Khasiat")
        with st.expander("Senyawa Aktif", expanded=True):
            st.markdown("**Kandungan Aktif:**")
            for compound in cultivation["active_compounds"]:
                st.markdown(f"- {compound}")
            
            st.markdown("\n**Manfaat Kesehatan:**")
            for benefit in cultivation["health_benefits"]:
                st.markdown(f"✅ {benefit}")
    
    st.markdown("### 📅 Jadwal Panen")
    st.success(f"**{cultivation['harvest_indicator']}**")
    
    if selected_leaf == "Sambiloto":
        st.warning("""
        **⚠️ Penting untuk Sambiloto:**
        - Panen SEBELUM berbunga (kadar andrographolide tertinggi)
        - Potong 10 cm dari permukaan tanah
        - Bisa panen 2-3x dari 1 tanaman (ratoon)
        - Keringkan segera (max 24 jam setelah panen)
        """)

# ===== TAB 4: PREMIUM ROOT CROPS =====
with tab4:
    st.markdown("## 🌿 Tanaman Akar Premium")
    
    root_species = ["Ginseng Jawa", "Pasak Bumi"]
    
    selected_root = st.selectbox(
        "Pilih Komoditas Akar:",
        root_species,
        key="root_select"
    )
    
    cultivation = CULTIVATION_DATABASE[selected_root]
    
    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["cycle_months"]} bulan</h3><p>Siklus Tanam</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["yield_dry"]}</h3><p>Ton/Ha (Kering)</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{cultivation["planting_density"]}</h3><p>Populasi/Ha</p></div>', unsafe_allow_html=True)
    with col4:
        price = MARKET_PRICES[selected_root]["grade_a_premium"]
        st.markdown(f'<div class="metric-card"><h3>Rp {price:,}</h3><p>Premium/kg</p></div>', unsafe_allow_html=True)
    
    if selected_root == "Pasak Bumi":
        st.warning("""
        **⚠️ Investasi Jangka Panjang:**
        - Siklus tanam: **5 tahun** (60 bulan)
        - Investasi tinggi: Rp 169 juta/ha
        - ROI sangat tinggi: 500-800%
        - Cocok untuk investor jangka panjang
        - Bisa dikombinasi dengan tanaman semusim (intercropping)
        """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Spesifikasi Budidaya")
        with st.expander("Detail Teknis", expanded=True):
            st.markdown(f"""
            - **Nama Latin**: *{cultivation["latin_name"]}*
            - **Jarak Tanam**: {cultivation["spacing"]}
            - **Ketinggian**: {cultivation["altitude"]}
            - **Curah Hujan**: {cultivation["rainfall"]}
            - **pH Tanah**: {cultivation["soil_ph"]}
            - **Jenis Tanah**: {cultivation["soil_type"]}
            - **Hasil Kering**: {cultivation["yield_dry"]}
            """)
        
        st.markdown("### 💰 Analisis Ekonomi")
        roi_data = MedicinalPlantsService.calculate_roi(selected_root, 1.0, "grade_a_premium")
        
        if roi_data:
            st.metric("Investasi", f"Rp {roi_data['investment']:,.0f}")
            st.metric("Revenue", f"Rp {roi_data['revenue']:,.0f}")
            st.metric("Profit", f"Rp {roi_data['profit']:,.0f}")
            st.metric("ROI", f"{roi_data['roi_percent']:.1f}%")
    
    with col2:
        st.markdown("### 🌾 Pemupukan")
        with st.expander("Detail Pemupukan", expanded=True):
            fert = cultivation["fertilizer"]
            for key, value in fert.items():
                st.markdown(f"- **{key.replace('_', ' ').title()}**: {value}")
        
        st.markdown("### 💊 Kandungan & Khasiat")
        with st.expander("Senyawa Aktif", expanded=True):
            st.markdown("**Kandungan Aktif:**")
            for compound in cultivation["active_compounds"]:
                st.markdown(f"- {compound}")
            
            st.markdown("\n**Manfaat Kesehatan:**")
            for benefit in cultivation["health_benefits"]:
                st.markdown(f"✅ {benefit}")
    
    st.markdown("### ✅ Indikator Panen")
    st.success(f"**{cultivation['harvest_indicator']}**")
    
    if selected_root == "Pasak Bumi":
        st.info("""
        **💡 Strategi Bisnis Pasak Bumi:**
        1. **Tahun 1-3**: Intercropping dengan jahe/kunyit (cashflow)
        2. **Tahun 4**: Mulai panen parsial (akar samping)
        3. **Tahun 5**: Panen total (harga premium)
        4. **Diversifikasi**: Jual bibit (Rp 5,000-10,000/bibit)
        5. **Value-added**: Ekstrak/kapsul (margin 10x)
        """)

# ===== TAB 5: GAP & CERTIFICATION =====
with tab5:
    st.markdown("## ✅ GAP Protocol & Sertifikasi")
    
    st.markdown("""
    <div class="info-card">
    <h3>🎯 Mengapa Sertifikasi Penting?</h3>
    <ul>
    <li><strong>Akses Pasar Ekspor:</strong> Wajib untuk ekspor ke Jepang, Eropa, Timur Tengah</li>
    <li><strong>Premium Price:</strong> 20-50% lebih tinggi dari produk non-sertifikat</li>
    <li><strong>Kepercayaan Konsumen:</strong> Jaminan kualitas dan keamanan</li>
    <li><strong>Traceability:</strong> Pelacakan dari farm to table</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    cert_type = st.selectbox(
        "Pilih Jenis Sertifikasi:",
        ["GAP", "Organic", "Halal"]
    )
    
    checklist = MedicinalPlantsService.get_certification_checklist(cert_type)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### ✅ Checklist {cert_type}")
        
        for idx, item in enumerate(checklist, 1):
            st.checkbox(item, key=f"cert_{cert_type}_{idx}")
    
    with col2:
        if cert_type == "GAP":
            st.markdown("""
            <div class="cultivation-box">
            <h4>📋 GAP (Good Agricultural Practices)</h4>
            <p><strong>Standar:</strong> SNI 8244:2016</p>
            <p><strong>Biaya:</strong> Rp 5-10 juta</p>
            <p><strong>Masa Berlaku:</strong> 3 tahun</p>
            <p><strong>Lembaga:</strong> LSO terakreditasi KAN</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif cert_type == "Organic":
            st.markdown("""
            <div class="cultivation-box">
            <h4>🌱 Organic Certification</h4>
            <p><strong>Standar:</strong> SNI 6729, EU Organic, USDA</p>
            <p><strong>Biaya:</strong> Rp 15-25 juta/tahun</p>
            <p><strong>Konversi:</strong> 2 tahun</p>
            <p><strong>Lembaga:</strong> Inofice, Biocert, Control Union</p>
            </div>
            """, unsafe_allow_html=True)
        
        else:  # Halal
            st.markdown("""
            <div class="cultivation-box">
            <h4>🕌 Halal Certification</h4>
            <p><strong>Standar:</strong> HAS 23000</p>
            <p><strong>Biaya:</strong> Rp 3-10 juta</p>
            <p><strong>Masa Berlaku:</strong> 2 tahun</p>
            <p><strong>Lembaga:</strong> LPPOM MUI</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("### 📊 Perbandingan Sertifikasi")
    
    cert_comparison = pd.DataFrame({
        "Sertifikasi": ["GAP", "Organic", "Halal"],
        "Biaya (Rp Juta)": [7.5, 20, 6.5],
        "Masa Berlaku (Tahun)": [3, 1, 2],
        "Premium Price (%)": [15, 30, 20],
        "Target Pasar": ["Jepang, China", "Eropa, USA", "Timur Tengah, Malaysia"]
    })
    
    st.dataframe(cert_comparison, use_container_width=True, hide_index=True)
    
    st.success("""
    **💡 Rekomendasi:**
    - **Pemula**: Mulai dengan GAP (biaya rendah, akses pasar luas)
    - **Ekspor Eropa**: Wajib Organic (premium tertinggi)
    - **Ekspor Timur Tengah**: Kombinasi GAP + Halal (nilai tambah signifikan)
    - **Strategi Optimal**: Triple certification (GAP + Organic + Halal) untuk akses pasar maksimal
    """)

# ===== TAB 6: BUSINESS CALCULATOR =====
with tab6:
    st.markdown("## 💰 Kalkulator Bisnis Tanaman Obat")
    
    calc_species = st.selectbox(
        "Pilih Komoditas:",
        list(CULTIVATION_DATABASE.keys()),
        key="calc_species"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        area_ha = st.number_input(
            "Luas Lahan (Ha):",
            min_value=0.1,
            max_value=100.0,
            value=1.0,
            step=0.1
        )
    
    with col2:
        market_type = st.selectbox(
            "Target Pasar:",
            ["fresh_local", "dry_local", "dry_export", "grade_a_premium"],
            format_func=lambda x: {
                "fresh_local": "Lokal (Segar)",
                "dry_local": "Lokal (Kering)",
                "dry_export": "Ekspor (Kering)",
                "grade_a_premium": "Premium Grade A"
            }[x]
        )
    
    # Calculate ROI
    roi_data = MedicinalPlantsService.calculate_roi(calc_species, area_ha, market_type)
    
    if roi_data:
        st.markdown("### 📊 Hasil Analisis")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Investasi", f"Rp {roi_data['investment']:,.0f}")
        with col2:
            st.metric("Revenue", f"Rp {roi_data['revenue']:,.0f}")
        with col3:
            st.metric("Profit", f"Rp {roi_data['profit']:,.0f}")
        with col4:
            st.metric("ROI", f"{roi_data['roi_percent']:.1f}%")
        
        # Detailed breakdown
        st.markdown("### 💵 Rincian Biaya Investasi")
        
        costs = INVESTMENT_COSTS[calc_species]
        cost_items = []
        for key, value in costs.items():
            if key != "total":
                cost_items.append({
                    "Komponen": key.replace("_", " ").title(),
                    "Biaya (Rp)": value * area_ha,
                    "Persentase": f"{(value/costs['total']*100):.1f}%"
                })
        
        df_costs = pd.DataFrame(cost_items)
        st.dataframe(df_costs, use_container_width=True, hide_index=True)
        
        # Pie chart
        fig = px.pie(
            df_costs,
            values='Biaya (Rp)',
            names='Komponen',
            title='Distribusi Biaya Investasi'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Revenue breakdown
        st.markdown("### 💰 Proyeksi Revenue")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            - **Hasil Panen (Kering)**: {roi_data['yield_kg']:,.0f} kg
            - **Harga Jual**: Rp {roi_data['price_per_kg']:,.0f}/kg
            - **Total Revenue**: Rp {roi_data['revenue']:,.0f}
            - **Siklus**: {roi_data['cycle_months']} bulan
            """)
        
        with col2:
            st.markdown(f"""
            - **Total Profit**: Rp {roi_data['profit']:,.0f}
            - **Margin**: {roi_data['margin_percent']:.1f}%
            - **ROI**: {roi_data['roi_percent']:.1f}%
            - **Payback Period**: {roi_data['payback_months']} bulan
            """)
        
        # Scaling scenarios
        st.markdown("### 📈 Skenario Skala Usaha")
        
        scales = [0.1, 0.5, 1.0, 2.0, 5.0]
        scale_data = []
        
        for scale in scales:
            scale_roi = MedicinalPlantsService.calculate_roi(calc_species, scale, market_type)
            if scale_roi:
                scale_data.append({
                    "Skala (Ha)": scale,
                    "Investasi (Juta)": scale_roi['investment'] / 1000000,
                    "Revenue (Juta)": scale_roi['revenue'] / 1000000,
                    "Profit (Juta)": scale_roi['profit'] / 1000000,
                    "ROI (%)": scale_roi['roi_percent']
                })
        
        df_scale = pd.DataFrame(scale_data)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_scale['Skala (Ha)'], y=df_scale['Investasi (Juta)'], 
                                 mode='lines+markers', name='Investasi'))
        fig.add_trace(go.Scatter(x=df_scale['Skala (Ha)'], y=df_scale['Revenue (Juta)'], 
                                 mode='lines+markers', name='Revenue'))
        fig.add_trace(go.Scatter(x=df_scale['Skala (Ha)'], y=df_scale['Profit (Juta)'], 
                                 mode='lines+markers', name='Profit'))
        
        fig.update_layout(
            title='Proyeksi Bisnis Berdasarkan Skala',
            xaxis_title='Luas Lahan (Ha)',
            yaxis_title='Nilai (Juta Rupiah)',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Margin comparison
    st.markdown("### 📊 Perbandingan Margin Antar Komoditas")
    
    comparison = MedicinalPlantsService.compare_margins(1.0, market_type)
    
    df_comparison = pd.DataFrame(comparison)
    df_comparison['Investasi (Juta)'] = df_comparison['investment'] / 1000000
    df_comparison['Revenue (Juta)'] = df_comparison['revenue'] / 1000000
    df_comparison['Profit (Juta)'] = df_comparison['profit'] / 1000000
    
    fig = px.bar(
        df_comparison,
        x='species',
        y='roi_percent',
        color='margin_percent',
        title='Perbandingan ROI Antar Komoditas (%)',
        labels={'species': 'Komoditas', 'roi_percent': 'ROI (%)', 'margin_percent': 'Margin (%)'},
        color_continuous_scale='Greens'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(
        df_comparison[['species', 'Investasi (Juta)', 'Revenue (Juta)', 'Profit (Juta)', 'roi_percent', 'margin_percent', 'cycle_months']],
        use_container_width=True,
        hide_index=True
    )

# ===== TAB 7: HARVEST & POST-HARVEST =====
with tab7:
    st.markdown("## 📅 Manajemen Panen & Pasca Panen")
    
    st.markdown("""
    <div class="info-card">
    <h3>🎯 Pentingnya Pasca Panen yang Benar</h3>
    <ul>
    <li><strong>Kualitas:</strong> 60% kualitas ditentukan saat pasca panen</li>
    <li><strong>Harga:</strong> Perbedaan harga Grade A vs C bisa 3-5x</li>
    <li><strong>Losses:</strong> Pasca panen buruk = losses 30-50%</li>
    <li><strong>Shelf Life:</strong> Pengeringan optimal = shelf life 2-3 tahun</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⏰ Waktu Panen Optimal")
    
    harvest_data = []
    for species, data in CULTIVATION_DATABASE.items():
        harvest_data.append({
            "Komoditas": species,
            "Siklus (Bulan)": data["cycle_months"],
            "Indikator Panen": data["harvest_indicator"],
            "Rasio Kering": f"{data['drying_ratio']*100}%"
        })
    
    df_harvest = pd.DataFrame(harvest_data)
    st.dataframe(df_harvest, use_container_width=True, hide_index=True)
    
    st.markdown("### 🌡️ Metode Pengeringan")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="cultivation-box">
        <h4>☀️ Sun Drying (Tradisional)</h4>
        <p><strong>Waktu:</strong> 5-7 hari</p>
        <p><strong>Suhu:</strong> 30-35°C (alami)</p>
        <p><strong>Biaya:</strong> Rendah</p>
        <p><strong>Kualitas:</strong> Sedang</p>
        <p><strong>Cocok untuk:</strong> Skala kecil, cuaca cerah</p>
        <p><strong>Risiko:</strong> Hujan, kontaminasi</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="cultivation-box">
        <h4>🔥 Oven Drying (Terkontrol)</h4>
        <p><strong>Waktu:</strong> 12-24 jam</p>
        <p><strong>Suhu:</strong> 40-50°C</p>
        <p><strong>Biaya:</strong> Sedang</p>
        <p><strong>Kualitas:</strong> Baik</p>
        <p><strong>Cocok untuk:</strong> Skala menengah</p>
        <p><strong>Keunggulan:</strong> Konsisten, cepat</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="cultivation-box">
        <h4>❄️ Freeze Drying (Premium)</h4>
        <p><strong>Waktu:</strong> 24-48 jam</p>
        <p><strong>Suhu:</strong> -40°C (vakum)</p>
        <p><strong>Biaya:</strong> Tinggi</p>
        <p><strong>Kualitas:</strong> Excellent</p>
        <p><strong>Cocok untuk:</strong> Ekspor premium</p>
        <p><strong>Keunggulan:</strong> Kandungan aktif terjaga</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### 📦 Grading & Packaging")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🏆 Standar Grading:**
        
        **Grade A (Premium Export)**:
        - Kadar air: 10-12%
        - Warna: Cerah, seragam
        - Aroma: Kuat, khas
        - Kontaminan: 0%
        - Ukuran: Seragam
        - Harga: 100% (baseline)
        
        **Grade B (Standard)**:
        - Kadar air: 12-14%
        - Warna: Agak kusam
        - Aroma: Normal
        - Kontaminan: <2%
        - Ukuran: Bervariasi
        - Harga: 70-80% dari Grade A
        
        **Grade C (Lokal)**:
        - Kadar air: 14-16%
        - Warna: Kusam
        - Kontaminan: <5%
        - Harga: 40-50% dari Grade A
        """)
    
    with col2:
        st.markdown("""
        **📦 Packaging untuk Ekspor:**
        
        **Material:**
        - Plastik food-grade (PE/PP)
        - Aluminium foil (barrier oksigen)
        - Karton berlapis (outer packaging)
        
        **Ukuran Standar:**
        - 1 kg (retail)
        - 5 kg (semi-wholesale)
        - 25 kg (wholesale/industri)
        
        **Labeling (Wajib):**
        - Nama produk (Latin + lokal)
        - Berat bersih
        - Tanggal produksi & expired
        - Nomor batch
        - Sertifikasi (Organic/Halal/GAP)
        - Negara asal
        - Barcode
        
        **Storage:**
        - Suhu: 15-25°C
        - Humidity: <60%
        - Cahaya: Gelap/tertutup
        - Shelf life: 24-36 bulan
        """)
    
    st.success("""
    **💡 Tips Pasca Panen:**
    - Panen pagi hari (06:00-09:00) saat kadar air rendah
    - Cuci dengan air bersih (jika perlu)
    - Tiriskan sempurna sebelum pengeringan
    - Jangan tumpuk terlalu tebal saat penjemuran
    - Balik setiap 2-3 jam untuk pengeringan merata
    - Simpan di tempat kering, sejuk, gelap
    - Gunakan silica gel untuk kontrol humidity
    """)

# ===== TAB 8: MEDICINAL PROPERTIES DATABASE =====
with tab8:
    st.markdown("## 🔬 Database Khasiat & Kandungan Ilmiah")
    
    db_species = st.selectbox(
        "Pilih Komoditas:",
        list(CULTIVATION_DATABASE.keys()),
        key="db_species"
    )
    
    cultivation = CULTIVATION_DATABASE[db_species]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🧪 Kandungan Senyawa Aktif")
        
        st.markdown(f"""
        <div class="cultivation-box">
        <h4>{db_species}</h4>
        <p><em>{cultivation["latin_name"]}</em></p>
        </div>
        """, unsafe_allow_html=True)
        
        for compound in cultivation["active_compounds"]:
            st.markdown(f"- **{compound}**")
        
        # Specific details for popular species
        if db_species == "Jahe Merah":
            st.info("""
            **Gingerol (6-gingerol):**
            - Konsentrasi: 2-3% (berat kering)
            - Fungsi: Anti-inflamasi, antioksidan
            - Mekanisme: Inhibisi COX-2 dan LOX
            - Penelitian: 200+ studi klinis
            
            **Shogaol:**
            - Terbentuk saat pengeringan/pemanasan
            - 10x lebih poten dari gingerol
            - Anti-kanker (in-vitro studies)
            """)
        
        elif db_species == "Kunyit":
            st.info("""
            **Curcumin:**
            - Konsentrasi: 3-5% (berat kering)
            - Bioavailabilitas rendah (perlu piperine)
            - Anti-inflamasi setara ibuprofen
            - 3000+ publikasi ilmiah
            
            **Demethoxycurcumin & Bisdemethoxycurcumin:**
            - Curcuminoid minor (1-2%)
            - Sinergis dengan curcumin
            - Antioksidan kuat
            """)
        
        elif db_species == "Sambiloto":
            st.info("""
            **Andrographolide:**
            - Konsentrasi: 2-4% (daun kering)
            - Imunomodulator (meningkatkan CD4+)
            - Anti-virus (influenza, herpes)
            - Hepatoprotektor
            
            **Deoxyandrographolide:**
            - Konsentrasi: 0.5-1%
            - Anti-diabetes (↓ glukosa darah)
            - Penelitian klinis di Thailand
            """)
    
    with col2:
        st.markdown("### 💊 Manfaat Kesehatan (Evidence-Based)")
        
        for benefit in cultivation["health_benefits"]:
            st.markdown(f"✅ {benefit}")
        
        st.markdown("### 📚 Referensi Ilmiah")
        
        # Add scientific references based on species
        if db_species == "Jahe Merah":
            st.markdown("""
            1. **Grzanna et al. (2005)**. *J Med Food*. "Ginger—An Herbal Medicinal Product with Broad Anti-Inflammatory Actions"
            
            2. **Mashhadi et al. (2013)**. *Int J Prev Med*. "Anti-Oxidative and Anti-Inflammatory Effects of Ginger"
            
            3. **Palatty et al. (2013)**. *Phytother Res*. "Ginger in the prevention of nausea and vomiting"
            
            4. **Mozaffari-Khosravi et al. (2012)**. *Diabetes Res Clin Pract*. "Effects of ginger on fasting blood sugar"
            """)
        
        elif db_species == "Kunyit":
            st.markdown("""
            1. **Hewlings & Kalman (2017)**. *Foods*. "Curcumin: A Review of Its Effects on Human Health"
            
            2. **Gupta et al. (2013)**. *Biochim Biophys Acta*. "Therapeutic Roles of Curcumin"
            
            3. **Chainani-Wu (2003)**. *J Altern Complement Med*. "Safety and anti-inflammatory activity of curcumin"
            
            4. **Aggarwal & Harikumar (2009)**. *Int J Biochem Cell Biol*. "Potential therapeutic effects of curcumin"
            """)
        
        elif db_species == "Sambiloto":
            st.markdown("""
            1. **Saxena et al. (2010)**. *J Ethnopharmacol*. "Andrographis paniculata: A review of pharmacological activities"
            
            2. **Poolsup et al. (2004)**. *J Clin Pharm Ther*. "Andrographis paniculata in symptomatic treatment of uncomplicated upper respiratory tract infection"
            
            3. **Jayakumar et al. (2013)**. *Phytother Res*. "Experimental and clinical pharmacology of Andrographis paniculata"
            
            4. **Akbar (2011)**. *J Ethnopharmacol*. "Andrographis paniculata: A review of pharmacological activities and clinical effects"
            """)
        
        elif db_species == "Pegagan":
            st.markdown("""
            1. **Gohil et al. (2010)**. *Pharmacogn Rev*. "Pharmacological Review on Centella asiatica: A Potential Herbal Cure-all"
            
            2. **Wattanathorn et al. (2008)**. *J Ethnopharmacol*. "Positive modulation of cognition and mood in healthy elderly volunteers"
            
            3. **Brinkhaus et al. (2000)**. *Phytomedicine*. "Chemical, pharmacological and clinical profile of Centella asiatica"
            
            4. **Shinomol et al. (2011)**. *Neurotox Res*. "Exploring the role of Centella asiatica in improving age-related neurological antioxidant status"
            """)
        
        st.markdown("### ⚠️ Keamanan & Kontraindikasi")
        
        st.warning("""
        **Perhatian Umum:**
        - Konsultasi dokter untuk ibu hamil/menyusui
        - Hati-hati pada pasien dengan gangguan pembekuan darah
        - Interaksi dengan obat-obatan tertentu
        - Dosis berlebihan dapat menyebabkan efek samping
        
        **Dosis Aman (Dewasa):**
        - Jahe: 1-4 gram/hari
        - Kunyit: 1.5-3 gram/hari
        - Sambiloto: 400-1200 mg ekstrak/hari
        - Pegagan: 600-2000 mg ekstrak/hari
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p><strong>🌿 AgriSensa - Tanaman Obat & Herbal</strong></p>
    <p>Platform Panduan Budidaya Tanaman Obat Berorientasi Ekspor</p>
    <p><small>Data harga & standar diperbarui: Desember 2024</small></p>
</div>
""", unsafe_allow_html=True)
