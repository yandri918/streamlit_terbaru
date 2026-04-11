import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from audit_logger import save_audit_log, load_audit_logs, export_audit_logs, get_audit_summary
from pdf_generator import generate_tax_report_pdf
from ai_tax_advisor import get_ai_response, get_suggested_questions
import altair as alt
import numpy as np
from cfo_dashboard_data import (
    generate_sample_tax_data, generate_pph21_trend_data,
    generate_pph_badan_quarterly, generate_5year_projection,
    generate_production_cost_data,
    load_from_audit_trail, load_from_database, load_from_uploaded_file,
    process_tax_data_for_dashboard, calculate_pph21_trend, calculate_pph_badan_quarterly
)

# Page Configuration
st.set_page_config(
    page_title="TaxPro Indonesia - Kalkulator Pajak & Biaya Produksi",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main Container */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 1.5rem;
    }
    
    /* Header Styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        font-size: 1.2rem;
        opacity: 0.95;
    }
    
    /* Feature Cards */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #6366f1;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e5e7eb;
        padding: 0.75rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem 2rem;
        color: white;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #6366f1 !important;
    }
    
    /* Success/Info Boxes */
    .stSuccess, .stInfo, .stWarning {
        border-radius: 10px;
        padding: 1rem;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Result Cards */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .result-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    
    .result-value {
        font-size: 2rem;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Navigation
with st.sidebar:
    st.markdown("### 💼 TaxPro Indonesia")
    st.markdown("---")
    
    # User Info for Audit Trail
    st.markdown("### 👤 **Info Pengguna**")
    st.markdown("**Untuk keperluan Audit Trail**")
    
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    if 'company_name' not in st.session_state:
        st.session_state.company_name = ""
    
    st.session_state.user_name = st.text_input(
        "**Nama Pengguna** 👤",
        value=st.session_state.user_name,
        placeholder="Masukkan nama Anda",
        help="Nama ini akan tercatat di audit trail"
    )
    
    st.session_state.company_name = st.text_input(
        "**Nama Perusahaan** 🏢",
        value=st.session_state.company_name,
        placeholder="Masukkan nama perusahaan",
        help="Nama perusahaan untuk audit trail"
    )
    
    st.markdown("---")
    
    page = st.radio(
        "Navigasi",
        ["🏠 Beranda", "📊 CFO Dashboard", "💰 Kalkulator Pajak", "🏭 Biaya Produksi", "🤖 AI Tax Advisor", "📋 Audit Trail", "📞 Kontak"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Info Cepat")
    st.info("**Tarif PPN:** 11%")
    st.info("**PPh Badan:** 22%")
    st.info("**PBB:** 0.5%")
    st.info("**PKB:** 1.5%-2%")
    st.info("**BPHTB:** 5%")
    st.info("**Update:** UU HPP 2021")
    
    st.markdown("---")
    st.markdown("### 🔗 Link Penting")
    st.markdown("[DJP Online](https://www.pajak.go.id)")
    st.markdown("[Peraturan Pajak](https://www.pajak.go.id/id/peraturan)")

# Main Content
if page == "🏠 Beranda":
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💼 TaxPro Indonesia</h1>
        <p>Konsultan Digital Pajak & Manajemen Biaya Produksi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📊</div>
            <h3>Kalkulator Pajak Lengkap</h3>
            <p>PPh 21, PPh 23, PPN, PPh Badan, PBB, PKB, BPHTB sesuai regulasi terbaru</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🏭</div>
            <h3>Analisis Biaya Produksi</h3>
            <p>Break-even point, margin keuntungan, dan harga jual optimal</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🛡️</div>
            <h3>Sesuai Regulasi DJP</h3>
            <p>Update UU HPP 2021 dan peraturan perpajakan Indonesia</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Welcome Section
    st.markdown("""
    <div class="glass-card">
        <h2>Selamat Datang di TaxPro Indonesia</h2>
        <p style="font-size: 1.1rem; line-height: 1.8;">
            Platform digital terpercaya untuk perhitungan pajak dan manajemen biaya produksi perusahaan Anda.
            Kami menyediakan kalkulator pajak yang akurat sesuai dengan peraturan perpajakan Indonesia terbaru,
            serta tools analisis biaya produksi untuk membantu Anda menentukan harga jual yang optimal.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Services
    st.markdown("<div class='glass-card'><h2>Layanan Kami</h2></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 📄 Pelaporan SPT")
        st.write("Bantuan pelaporan SPT Tahunan dan Masa")
        
        st.markdown("#### ⚖️ Tax Planning")
        st.write("Perencanaan pajak yang efisien")
    
    with col2:
        st.markdown("#### 🔍 Tax Review")
        st.write("Review dan audit internal perpajakan")
        
        st.markdown("#### 🎓 Pelatihan Pajak")
        st.write("Workshop untuk tim finance")
    
    with col3:
        st.markdown("#### 🤝 Pendampingan Pemeriksaan")
        st.write("Pendampingan saat pemeriksaan DJP")
        
        st.markdown("#### 📊 Pembukuan & Akuntansi")
        st.write("Jasa pembukuan dan laporan keuangan")

elif page == "📊 CFO Dashboard":
    st.markdown("""
    <div class="main-header">
        <h1>📊 CFO Dashboard</h1>
        <p>Executive Tax & Production Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Data Source Selector
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📂 Sumber Data")
    
    data_source = st.radio(
        "Pilih sumber data untuk dashboard:",
        ["📊 Sample Data (Demo)", "📋 Audit Trail", "💾 Database", "📤 Upload File"],
        horizontal=True
    )
    
    # Initialize data variables
    raw_data = None
    data_source_info = ""
    
    # Load data based on selection
    if data_source == "📋 Audit Trail":
        with st.spinner("Loading data from audit trail..."):
            raw_data = load_from_audit_trail()
            if raw_data is not None and not raw_data.empty:
                data_source_info = f"✅ Loaded {len(raw_data)} records from audit trail"
                st.success(data_source_info)
            else:
                st.warning("⚠️ No audit trail data found. Using sample data instead.")
                raw_data = None
    
    elif data_source == "💾 Database":
        db_path = st.text_input("Database Path:", value="tax_data.db")
        if st.button("Load from Database"):
            with st.spinner("Loading data from database..."):
                raw_data = load_from_database(db_path)
                if raw_data is not None and not raw_data.empty:
                    data_source_info = f"✅ Loaded {len(raw_data)} records from database"
                    st.success(data_source_info)
                else:
                    st.error("❌ Database not found or empty. Using sample data instead.")
                    raw_data = None
    
    elif data_source == "📤 Upload File":
        st.info("📝 **Format File:** Excel/CSV dengan kolom: `month`, `tax_type`, `amount`")
        uploaded_file = st.file_uploader(
            "Upload file Excel atau CSV",
            type=['xlsx', 'xls', 'csv'],
            help="File harus memiliki kolom: month (tanggal), tax_type (jenis pajak), amount (jumlah)"
        )
        
        if uploaded_file is not None:
            with st.spinner("Processing uploaded file..."):
                raw_data = load_from_uploaded_file(uploaded_file)
                if raw_data is not None and not raw_data.empty:
                    data_source_info = f"✅ Loaded {len(raw_data)} records from {uploaded_file.name}"
                    st.success(data_source_info)
                    
                    # Show preview
                    with st.expander("Preview Data"):
                        st.dataframe(raw_data.head(10), use_container_width=True)
                else:
                    st.error("❌ Invalid file format. Please check column names. Using sample data instead.")
                    raw_data = None
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Process data or use sample data
    if raw_data is not None and not raw_data.empty:
        # Use real data
        tax_data = process_tax_data_for_dashboard(raw_data)
        pph21_trend = calculate_pph21_trend(raw_data)
        pph_badan_quarterly = calculate_pph_badan_quarterly(raw_data)
        
        # For projections and production costs, still use generated data
        # (since these require historical patterns not available in raw data)
        projection_data = generate_5year_projection()
        cost_breakdown, cost_trend = generate_production_cost_data()
        
        # Fallback to sample if processing failed
        if tax_data is None or tax_data.empty:
            st.warning("⚠️ Data processing failed. Using sample data.")
            tax_data = generate_sample_tax_data()
            pph21_trend = generate_pph21_trend_data()
            pph_badan_quarterly = generate_pph_badan_quarterly()
    else:
        # Use sample data (default)
        tax_data = generate_sample_tax_data()
        pph21_trend = generate_pph21_trend_data()
        pph_badan_quarterly = generate_pph_badan_quarterly()
        projection_data = generate_5year_projection()
        cost_breakdown, cost_trend = generate_production_cost_data()
        
        if data_source == "📊 Sample Data (Demo)":
            st.info("ℹ️ Menampilkan data demo untuk ilustrasi dashboard")
    
    # KPI Summary Cards
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📈 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_tax = tax_data['amount'].sum()
    pph21_ytd = tax_data[tax_data['tax_type'] == 'PPh 21']['amount'].sum()
    pph_badan_ytd = tax_data[tax_data['tax_type'] == 'PPh Badan']['amount'].sum()
    prod_cost_total = cost_breakdown['amount'].sum()
    tax_efficiency = 85.5  # Sample efficiency ratio
    
    with col1:
        st.metric("Total Pajak YTD", f"Rp {total_tax/1e9:.2f}B", delta="12.5%")
    
    with col2:
        st.metric("PPh 21 YTD", f"Rp {pph21_ytd/1e6:.0f}M", delta="8.2%")
    
    with col3:
        st.metric("PPh Badan YTD", f"Rp {pph_badan_ytd/1e9:.2f}B", delta="15.3%")
    
    with col4:
        st.metric("Biaya Produksi", f"Rp {prod_cost_total/1e9:.2f}B", delta="-3.1%")
    
    with col5:
        st.metric("Tax Efficiency", f"{tax_efficiency}%", delta="2.3%")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Pajak Tahunan - Stacked Bar Chart
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📊 Pajak Tahunan per Bulan")
    
    # Prepare data for Altair
    tax_data['month_str'] = tax_data['month'].dt.strftime('%b %Y')
    
    chart_annual = alt.Chart(tax_data).mark_bar().encode(
        x=alt.X('month_str:N', title='Bulan', sort=None),
        y=alt.Y('amount:Q', title='Pajak (Rp)', axis=alt.Axis(format='~s')),
        color=alt.Color('tax_type:N', 
            title='Jenis Pajak',
            scale=alt.Scale(
                domain=['PPh 21', 'PPh Badan', 'PPN', 'Lainnya'],
                range=['#667eea', '#764ba2', '#f093fb', '#feca57']
            )
        ),
        tooltip=[
            alt.Tooltip('month_str:N', title='Bulan'),
            alt.Tooltip('tax_type:N', title='Jenis Pajak'),
            alt.Tooltip('amount:Q', title='Jumlah', format=',.0f')
        ]
    ).properties(
        width='container',
        height=400
    ).configure_axis(
        labelAngle=45
    )
    
    st.altair_chart(chart_annual, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Tren PPh 21 & PPh Badan
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 Tren PPh 21")
        
        pph21_trend['month_str'] = pph21_trend['month'].dt.strftime('%b %Y')
        
        # Create base chart
        base = alt.Chart(pph21_trend).encode(
            x=alt.X('month_str:N', title='Bulan', sort=None)
        )
        
        # Actual line
        line = base.mark_line(color='#667eea', strokeWidth=3).encode(
            y=alt.Y('pph21:Q', title='PPh 21 (Rp)', axis=alt.Axis(format='~s')),
            tooltip=[
                alt.Tooltip('month_str:N', title='Bulan'),
                alt.Tooltip('pph21:Q', title='PPh 21', format=',.0f')
            ]
        )
        
        # Moving average
        ma_line = base.mark_line(color='#f093fb', strokeDash=[5,5], strokeWidth=2).encode(
            y=alt.Y('moving_avg:Q'),
            tooltip=[
                alt.Tooltip('month_str:N', title='Bulan'),
                alt.Tooltip('moving_avg:Q', title='MA (3 bulan)', format=',.0f')
            ]
        )
        
        chart_pph21 = (line + ma_line).properties(
            width='container',
            height=300
        ).configure_axis(
            labelAngle=45
        )
        
        st.altair_chart(chart_pph21, use_container_width=True)
        st.caption("Garis putus-putus: Moving Average 3 bulan")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_right:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Tren PPh Badan (Quarterly)")
        
        chart_pph_badan = alt.Chart(pph_badan_quarterly).mark_line(point=True).encode(
            x=alt.X('quarter:N', title='Quarter'),
            y=alt.Y('pph_badan:Q', title='PPh Badan (Rp)', axis=alt.Axis(format='~s')),
            color=alt.Color('scenario:N', 
                title='Skenario',
                scale=alt.Scale(
                    domain=['UMKM (0.5%)', 'Non-UMKM (22%)'],
                    range=['#51cf66', '#667eea']
                )
            ),
            strokeDash=alt.StrokeDash('scenario:N',
                scale=alt.Scale(
                    domain=['UMKM (0.5%)', 'Non-UMKM (22%)'],
                    range=[[1,0], [5,5]]
                )
            ),
            tooltip=[
                alt.Tooltip('quarter:N', title='Quarter'),
                alt.Tooltip('scenario:N', title='Skenario'),
                alt.Tooltip('pph_badan:Q', title='PPh Badan', format=',.0f')
            ]
        ).properties(
            width='container',
            height=300
        )
        
        st.altair_chart(chart_pph_badan, use_container_width=True)
        st.caption("Perbandingan UMKM vs Non-UMKM")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Proyeksi 5 Tahun
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔮 Proyeksi Pajak 5 Tahun")
    
    chart_projection = alt.Chart(projection_data).mark_line(point=True, strokeWidth=3).encode(
        x=alt.X('year:N', title='Tahun'),
        y=alt.Y('projected_tax:Q', title='Proyeksi Pajak (Rp)', axis=alt.Axis(format='~s')),
        color=alt.Color('scenario:N',
            title='Skenario',
            scale=alt.Scale(
                domain=['Conservative', 'Moderate', 'Aggressive'],
                range=['#ff6b6b', '#667eea', '#51cf66']
            )
        ),
        strokeDash=alt.StrokeDash('type:N',
            title='Tipe',
            scale=alt.Scale(
                domain=['Historical', 'Forecast'],
                range=[[1,0], [5,5]]
            )
        ),
        tooltip=[
            alt.Tooltip('year:N', title='Tahun'),
            alt.Tooltip('scenario:N', title='Skenario'),
            alt.Tooltip('projected_tax:Q', title='Proyeksi', format=',.0f'),
            alt.Tooltip('type:N', title='Tipe')
        ]
    ).properties(
        width='container',
        height=400
    )
    
    st.altair_chart(chart_projection, use_container_width=True)
    
    # Scenario explanation
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("**🔴 Conservative (5% growth)**")
        st.caption("Pertumbuhan minimal, fokus efisiensi")
    with col_s2:
        st.markdown("**🔵 Moderate (10% growth)**")
        st.caption("Pertumbuhan stabil, balanced approach")
    with col_s3:
        st.markdown("**🟢 Aggressive (15% growth)**")
        st.caption("Ekspansi cepat, investasi tinggi")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Biaya Produksi Analysis
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🏭 Analisis Biaya Produksi")
    
    col_cost1, col_cost2 = st.columns([1, 2])
    
    with col_cost1:
        st.markdown("**Breakdown Biaya**")
        
        # Pie chart using Altair
        chart_pie = alt.Chart(cost_breakdown).mark_arc(innerRadius=50).encode(
            theta=alt.Theta('amount:Q'),
            color=alt.Color('category:N',
                scale=alt.Scale(
                    domain=['Bahan Baku', 'Tenaga Kerja', 'Overhead', 'Lainnya'],
                    range=['#667eea', '#764ba2', '#f093fb', '#feca57']
                ),
                legend=alt.Legend(title='Kategori')
            ),
            tooltip=[
                alt.Tooltip('category:N', title='Kategori'),
                alt.Tooltip('amount:Q', title='Jumlah', format=',.0f'),
                alt.Tooltip('percentage:Q', title='Persentase', format='.1f')
            ]
        ).properties(
            width=300,
            height=300
        )
        
        st.altair_chart(chart_pie, use_container_width=True)
        
        # Breakdown table
        st.dataframe(
            cost_breakdown[['category', 'percentage']].rename(columns={'category': 'Kategori', 'percentage': '%'}),
            use_container_width=True,
            hide_index=True
        )
    
    with col_cost2:
        st.markdown("**Tren Biaya per Kategori**")
        
        cost_trend['month_str'] = cost_trend['month'].dt.strftime('%b %Y')
        
        chart_cost_trend = alt.Chart(cost_trend).mark_area().encode(
            x=alt.X('month_str:N', title='Bulan', sort=None),
            y=alt.Y('cost:Q', title='Biaya (Rp)', axis=alt.Axis(format='~s')),
            color=alt.Color('category:N',
                title='Kategori',
                scale=alt.Scale(
                    domain=['Bahan Baku', 'Tenaga Kerja', 'Overhead', 'Lainnya'],
                    range=['#667eea', '#764ba2', '#f093fb', '#feca57']
                )
            ),
            tooltip=[
                alt.Tooltip('month_str:N', title='Bulan'),
                alt.Tooltip('category:N', title='Kategori'),
                alt.Tooltip('cost:Q', title='Biaya', format=',.0f')
            ]
        ).properties(
            width='container',
            height=350
        ).configure_axis(
            labelAngle=45
        )
        
        st.altair_chart(chart_cost_trend, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Export Dashboard
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📥 Export Dashboard")
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.info("Feature coming soon!")
    
    with col_exp2:
        if st.button("📄 Export to PDF", use_container_width=True):
            st.info("Feature coming soon!")
    
    with col_exp3:
        st.metric("Last Updated", datetime.now().strftime('%d %b %Y'))
    
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "💰 Kalkulator Pajak":
    st.markdown("""
    <div class="main-header">
        <h1>💰 Kalkulator Pajak</h1>
        <p>Hitung pajak Anda dengan akurat sesuai peraturan perpajakan Indonesia</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tax Type Tabs
    tax_tab = st.tabs(["PPh 21", "PPh 23", "PPN", "PPh Badan", "PBB", "PKB", "BPHTB"])
    
    # PPh 21 Calculator
    with tax_tab[0]:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Kalkulator PPh 21 - Pajak Penghasilan Karyawan")
        st.caption("Hitung pajak penghasilan karyawan berdasarkan UU HPP 2021")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Input Data Karyawan")
            
            gaji_bruto = st.number_input(
                "Gaji Bruto per Bulan (Rp)",
                min_value=0,
                value=10000000,
                step=100000,
                format="%d"
            )
            
            status = st.selectbox(
                "Status Pernikahan",
                ["TK/0 - Tidak Kawin, Tanpa Tanggungan",
                 "TK/1 - Tidak Kawin, 1 Tanggungan",
                 "TK/2 - Tidak Kawin, 2 Tanggungan",
                 "TK/3 - Tidak Kawin, 3 Tanggungan",
                 "K/0 - Kawin, Tanpa Tanggungan",
                 "K/1 - Kawin, 1 Tanggungan",
                 "K/2 - Kawin, 2 Tanggungan",
                 "K/3 - Kawin, 3 Tanggungan"]
            )
            
            bonus = st.number_input(
                "Bonus/THR Tahunan (Rp)",
                min_value=0,
                value=0,
                step=100000,
                format="%d"
            )
            
            potongan = st.number_input(
                "Potongan (BPJS, Pensiun) per Bulan (Rp)",
                min_value=0,
                value=0,
                step=10000,
                format="%d"
            )
            
            if st.button("🧮 Hitung PPh 21", use_container_width=True):
                # PTKP Calculation
                ptkp_map = {
                    "TK/0": 54000000,
                    "TK/1": 58500000,
                    "TK/2": 63000000,
                    "TK/3": 67500000,
                    "K/0": 58500000,
                    "K/1": 63000000,
                    "K/2": 67500000,
                    "K/3": 72000000
                }
                
                status_code = status.split(" - ")[0]
                ptkp = ptkp_map[status_code]
                
                # Annual Calculation
                gaji_tahunan = (gaji_bruto - potongan) * 12
                penghasilan_bruto = gaji_tahunan + bonus
                penghasilan_netto = penghasilan_bruto
                pkp = max(0, penghasilan_netto - ptkp)
                
                # Progressive Tax Calculation (UU HPP 2021)
                pajak = 0
                if pkp > 0:
                    if pkp <= 60000000:
                        pajak = pkp * 0.05
                    elif pkp <= 250000000:
                        pajak = 60000000 * 0.05 + (pkp - 60000000) * 0.15
                    elif pkp <= 500000000:
                        pajak = 60000000 * 0.05 + 190000000 * 0.15 + (pkp - 250000000) * 0.25
                    elif pkp <= 5000000000:
                        pajak = 60000000 * 0.05 + 190000000 * 0.15 + 250000000 * 0.25 + (pkp - 500000000) * 0.30
                    else:
                        pajak = 60000000 * 0.05 + 190000000 * 0.15 + 250000000 * 0.25 + 4500000000 * 0.30 + (pkp - 5000000000) * 0.35
                
                pajak_bulanan = pajak / 12
                gaji_netto_bulanan = gaji_bruto - pajak_bulanan
                
                # Store in session state
                st.session_state.pph21_result = {
                    'gaji_bruto': gaji_bruto,
                    'potongan': potongan,
                    'gaji_tahunan': gaji_tahunan,
                    'bonus': bonus,
                    'penghasilan_bruto': penghasilan_bruto,
                    'ptkp': ptkp,
                    'pkp': pkp,
                    'pajak_tahunan': pajak,
                    'pajak_bulanan': pajak_bulanan,
                    'gaji_netto': gaji_netto_bulanan
                }
                
                # Save audit log
                save_audit_log(
                    calc_type="PPh 21",
                    user_name=st.session_state.get('user_name', 'Anonymous'),
                    company_name=st.session_state.get('company_name', 'N/A'),
                    input_data={'gaji_bruto': gaji_bruto, 'status': status, 'bonus': bonus, 'potongan': potongan},
                    output_data={'pajak_bulanan': pajak_bulanan, 'pajak_tahunan': pajak, 'gaji_netto': gaji_netto_bulanan}
                )
        
        with col2:
            st.markdown("#### Hasil Perhitungan")
            
            if 'pph21_result' in st.session_state:
                result = st.session_state.pph21_result
                
                # Display Results
                st.metric("Gaji Bruto/Bulan", f"Rp {result['gaji_bruto']:,.0f}")
                st.metric("PPh 21/Bulan", f"Rp {result['pajak_bulanan']:,.0f}", 
                         delta=f"{(result['pajak_bulanan']/result['gaji_bruto']*100):.2f}%")
                st.metric("Gaji Netto/Bulan", f"Rp {result['gaji_netto']:,.0f}")
                
                st.markdown("---")
                st.markdown("##### Detail Perhitungan Tahunan")
                
                detail_df = pd.DataFrame({
                    'Keterangan': [
                        'Penghasilan Bruto',
                        'PTKP',
                        'Penghasilan Kena Pajak (PKP)',
                        'PPh 21 Tahunan'
                    ],
                    'Jumlah (Rp)': [
                        f"{result['penghasilan_bruto']:,.0f}",
                        f"{result['ptkp']:,.0f}",
                        f"{result['pkp']:,.0f}",
                        f"{result['pajak_tahunan']:,.0f}"
                    ]
                })
                
                st.dataframe(detail_df, use_container_width=True, hide_index=True)
                
                # Download Buttons
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        "📥 Download CSV",
                        detail_df.to_csv(index=False).encode('utf-8'),
                        "hasil_pph21.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col_dl2:
                    pdf_bytes = generate_tax_report_pdf(
                        calc_type="PPh 21",
                        user_name=st.session_state.get('user_name', 'Anonymous'),
                        company_name=st.session_state.get('company_name', 'N/A'),
                        input_data={'gaji_bruto': gaji_bruto, 'status': status, 'bonus': bonus, 'potongan': potongan},
                        output_data=result
                    )
                    st.download_button(
                        "📄 Download PDF Report",
                        pdf_bytes,
                        f"Tax_Report_PPh21_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        "application/pdf",
                        use_container_width=True
                    )
            else:
                st.info("👈 Masukkan data dan klik tombol Hitung untuk melihat hasil")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # PPh 23 Calculator
    with tax_tab[1]:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Kalkulator PPh 23 - Pajak Potong Pungut")
        st.caption("Hitung pajak potong pungut untuk jasa dan dividen")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Input Data")
            
            jenis_penghasilan = st.selectbox(
                "Jenis Penghasilan",
                ["Jasa Teknik, Manajemen, Konsultan (2%)",
                 "Sewa Selain Tanah/Bangunan (2%)",
                 "Dividen (15%)",
                 "Royalti (15%)",
                 "Bunga (15%)",
                 "Hadiah & Penghargaan (15%)"]
            )
            
            jumlah_bruto = st.number_input(
                "Jumlah Bruto (Rp)",
                min_value=0,
                value=10000000,
                step=100000,
                format="%d"
            )
            
            punya_npwp = st.checkbox("Penerima Memiliki NPWP", value=True)
            st.caption("⚠️ Tanpa NPWP, tarif dinaikkan 100%")
            
            if st.button("🧮 Hitung PPh 23", use_container_width=True):
                # Determine rate
                if "2%" in jenis_penghasilan:
                    tarif_dasar = 0.02
                else:
                    tarif_dasar = 0.15
                
                # Adjust for NPWP
                tarif_final = tarif_dasar if punya_npwp else tarif_dasar * 2
                
                # Calculate tax
                pph23 = jumlah_bruto * tarif_final
                jumlah_netto = jumlah_bruto - pph23
                
                st.session_state.pph23_result = {
                    'jenis': jenis_penghasilan,
                    'bruto': jumlah_bruto,
                    'tarif': tarif_final * 100,
                    'pph23': pph23,
                    'netto': jumlah_netto,
                    'npwp': punya_npwp
                }
                
                # Save audit log
                save_audit_log(
                    calc_type="PPh 23",
                    user_name=st.session_state.get('user_name', 'Anonymous'),
                    company_name=st.session_state.get('company_name', 'N/A'),
                    input_data={'jenis': jenis_penghasilan, 'bruto': jumlah_bruto, 'npwp': punya_npwp},
                    output_data={'pph23': pph23, 'tarif': tarif_final * 100, 'netto': jumlah_netto}
                )
        
        with col2:
            st.markdown("#### Hasil Perhitungan")
            
            if 'pph23_result' in st.session_state:
                result = st.session_state.pph23_result
                
                st.metric("Jumlah Bruto", f"Rp {result['bruto']:,.0f}")
                st.metric("Tarif PPh 23", f"{result['tarif']:.1f}%")
                st.metric("PPh 23", f"Rp {result['pph23']:,.0f}")
                st.metric("Jumlah Netto", f"Rp {result['netto']:,.0f}")
                
                if not result['npwp']:
                    st.warning("⚠️ Tarif dinaikkan 100% karena tidak memiliki NPWP")
                
                st.markdown("---")
                
                detail_df = pd.DataFrame({
                    'Keterangan': ['Jenis Penghasilan', 'Jumlah Bruto', 'Tarif', 'PPh 23', 'Jumlah Netto'],
                    'Nilai': [
                        result['jenis'],
                        f"Rp {result['bruto']:,.0f}",
                        f"{result['tarif']:.1f}%",
                        f"Rp {result['pph23']:,.0f}",
                        f"Rp {result['netto']:,.0f}"
                    ]
                })
                
                st.dataframe(detail_df, use_container_width=True, hide_index=True)
                
                # Download Buttons
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        "📥 Download CSV",
                        detail_df.to_csv(index=False).encode('utf-8'),
                        "hasil_pph23.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col_dl2:
                    pdf_bytes = generate_tax_report_pdf(
                        calc_type="PPh 23",
                        user_name=st.session_state.get('user_name', 'Anonymous'),
                        company_name=st.session_state.get('company_name', 'N/A'),
                        input_data={'jenis': jenis_penghasilan, 'bruto': jumlah_bruto, 'npwp': punya_npwp},
                        output_data=result
                    )
                    st.download_button(
                        "📄 Download PDF Report",
                        pdf_bytes,
                        f"Tax_Report_PPh23_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        "application/pdf",
                        use_container_width=True
                    )
            else:
                st.info("👈 Masukkan data dan klik tombol Hitung untuk melihat hasil")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # PPN Calculator
    with tax_tab[2]:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Kalkulator PPN - Pajak Pertambahan Nilai")
        st.caption("Hitung Pajak Pertambahan Nilai 11%")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Input Data")
            
            jenis_hitung = st.radio(
                "Jenis Perhitungan",
                ["Harga Belum Termasuk PPN", "Harga Sudah Termasuk PPN"]
            )
            
            jumlah = st.number_input(
                "Jumlah (Rp)",
                min_value=0,
                value=10000000,
                step=100000,
                format="%d"
            )
            
            tarif_ppn = st.selectbox(
                "Tarif PPN",
                ["11% (Tarif Standar 2022-sekarang)", "12% (Rencana 2025)"]
            )
            
            if st.button("🧮 Hitung PPN", use_container_width=True):
                tarif = 0.11 if "11%" in tarif_ppn else 0.12
                
                if jenis_hitung == "Harga Belum Termasuk PPN":
                    dpp = jumlah
                    ppn = dpp * tarif
                    harga_total = dpp + ppn
                else:
                    harga_total = jumlah
                    dpp = harga_total / (1 + tarif)
                    ppn = harga_total - dpp
                
                st.session_state.ppn_result = {
                    'jenis': jenis_hitung,
                    'tarif': tarif * 100,
                    'dpp': dpp,
                    'ppn': ppn,
                    'total': harga_total
                }
                
                # Save audit log
                save_audit_log(
                    calc_type="PPN",
                    user_name=st.session_state.get('user_name', 'Anonymous'),
                    company_name=st.session_state.get('company_name', 'N/A'),
                    input_data={'jenis': jenis_hitung, 'jumlah': jumlah, 'tarif': tarif * 100},
                    output_data={'dpp': dpp, 'ppn': ppn, 'total': harga_total}
                )
        
        with col2:
            st.markdown("#### Hasil Perhitungan")
            
            if 'ppn_result' in st.session_state:
                result = st.session_state.ppn_result
                
                st.metric("DPP (Dasar Pengenaan Pajak)", f"Rp {result['dpp']:,.0f}")
                st.metric("PPN", f"Rp {result['ppn']:,.0f}", delta=f"{result['tarif']:.0f}%")
                st.metric("Harga Total", f"Rp {result['total']:,.0f}")
                
                # Visualization
                fig = go.Figure(data=[go.Pie(
                    labels=['DPP', 'PPN'],
                    values=[result['dpp'], result['ppn']],
                    hole=.4,
                    marker_colors=['#667eea', '#764ba2']
                )])
                
                fig.update_layout(
                    title="Komposisi Harga",
                    height=300,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Download Buttons
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    detail_df = pd.DataFrame({
                        'Keterangan': ['Jenis', 'Tarif', 'DPP', 'PPN', 'Total'],
                        'Nilai': [
                            result['jenis'],
                            f"{result['tarif']:.0f}%",
                            f"Rp {result['dpp']:,.0f}",
                            f"Rp {result['ppn']:,.0f}",
                            f"Rp {result['total']:,.0f}"
                        ]
                    })
                    st.download_button(
                        "📥 Download CSV",
                        detail_df.to_csv(index=False).encode('utf-8'),
                        "hasil_ppn.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col_dl2:
                    pdf_bytes = generate_tax_report_pdf(
                        calc_type="PPN",
                        user_name=st.session_state.get('user_name', 'Anonymous'),
                        company_name=st.session_state.get('company_name', 'N/A'),
                        input_data={'jenis': jenis_hitung, 'jumlah': jumlah, 'tarif': result['tarif']},
                        output_data=result
                    )
                    st.download_button(
                        "📄 Download PDF Report",
                        pdf_bytes,
                        f"Tax_Report_PPN_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        "application/pdf",
                        use_container_width=True
                    )
            else:
                st.info("👈 Masukkan data dan klik tombol Hitung untuk melihat hasil")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # PPh Badan Calculator - ADVANCED
    with tax_tab[3]:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Kalkulator PPh Badan Advanced - Pajak Perusahaan")
        st.caption("Perhitungan pajak perusahaan dengan fitur advanced: PPh 25, proyeksi, dan tax planning")
        
        # Sub-tabs for advanced features
        pph_badan_tabs = st.tabs(["💼 Perhitungan Dasar", "📅 PPh 25 (Angsuran)", "📈 Proyeksi Multi-Tahun", "⚖️ Perbandingan Skenario", "💡 Tax Planning"])
        
        # Tab 1: Basic Calculation
        with pph_badan_tabs[0]:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("#### Input Data Keuangan")
                
                omzet = st.number_input(
                    "Omzet/Peredaran Bruto Tahunan (Rp)",
                    min_value=0,
                    value=1000000000,
                    step=10000000,
                    format="%d",
                    key="omzet_basic"
                )
                
                biaya = st.number_input(
                    "Biaya Operasional (Rp)",
                    min_value=0,
                    value=500000000,
                    step=10000000,
                    format="%d",
                    key="biaya_basic"
                )
                
                penghasilan_lain = st.number_input(
                    "Penghasilan Lain (Rp)",
                    min_value=0,
                    value=0,
                    step=1000000,
                    format="%d",
                    key="penghasilan_lain_basic"
                )
                
                st.markdown("##### Koreksi Fiskal")
                
                biaya_tidak_deductible = st.number_input(
                    "Biaya Tidak Dapat Dikurangkan (Rp)",
                    min_value=0,
                    value=0,
                    step=1000000,
                    format="%d",
                    help="Contoh: sumbangan, sanksi pajak, natura"
                )
                
                penghasilan_final = st.number_input(
                    "Penghasilan Kena Pajak Final (Rp)",
                    min_value=0,
                    value=0,
                    step=1000000,
                    format="%d",
                    help="Penghasilan yang sudah dipotong PPh Final"
                )
                
                koreksi_lainnya = st.number_input(
                    "Koreksi Fiskal Lainnya (Rp)",
                    value=0,
                    step=1000000,
                    format="%d",
                    help="Positif untuk menambah, negatif untuk mengurangi"
                )
                
                is_umkm = st.checkbox("UMKM (Omzet < 4.8 Miliar)", value=False, key="umkm_basic")
                
                st.markdown("##### Kredit Pajak")
                
                pph_pasal_22 = st.number_input(
                    "PPh Pasal 22 yang Dipungut (Rp)",
                    min_value=0,
                    value=0,
                    step=100000,
                    format="%d"
                )
                
                pph_pasal_23 = st.number_input(
                    "PPh Pasal 23 yang Dipotong (Rp)",
                    min_value=0,
                    value=0,
                    step=100000,
                    format="%d"
                )
                
                if st.button("🧮 Hitung PPh Badan", use_container_width=True, key="calc_basic"):
                    # Calculate taxable income
                    laba_kotor = omzet - biaya + penghasilan_lain
                    
                    # Fiscal corrections
                    koreksi_fiskal_total = biaya_tidak_deductible - penghasilan_final + koreksi_lainnya
                    laba_fiskal = laba_kotor + koreksi_fiskal_total
                    
                    # Calculate tax
                    if is_umkm and omzet <= 4800000000:
                        # UMKM gets special rate
                        if laba_fiskal <= 500000000:
                            pph_badan_terutang = laba_fiskal * 0.11
                            tarif_efektif = 11
                        else:
                            pph_badan_terutang = 500000000 * 0.11 + (laba_fiskal - 500000000) * 0.22
                            tarif_efektif = (pph_badan_terutang / laba_fiskal * 100) if laba_fiskal > 0 else 0
                    else:
                        pph_badan_terutang = laba_fiskal * 0.22
                        tarif_efektif = 22
                    
                    # Tax credits
                    total_kredit_pajak = pph_pasal_22 + pph_pasal_23
                    pph_kurang_bayar = pph_badan_terutang - total_kredit_pajak
                    
                    laba_netto = laba_fiskal - pph_badan_terutang
                    
                    st.session_state.pph_badan_result = {
                        'omzet': omzet,
                        'biaya': biaya,
                        'penghasilan_lain': penghasilan_lain,
                        'laba_kotor': laba_kotor,
                        'koreksi_fiskal': koreksi_fiskal_total,
                        'laba_fiskal': laba_fiskal,
                        'pph_badan': pph_badan_terutang,
                        'tarif_efektif': tarif_efektif,
                        'kredit_pajak': total_kredit_pajak,
                        'pph_kurang_bayar': pph_kurang_bayar,
                        'laba_netto': laba_netto,
                        'is_umkm': is_umkm
                    }
                    
                    # Save audit log
                    save_audit_log(
                        calc_type="PPh Badan",
                        user_name=st.session_state.get('user_name', 'Anonymous'),
                        company_name=st.session_state.get('company_name', 'N/A'),
                        input_data={'omzet': omzet, 'biaya': biaya, 'is_umkm': is_umkm},
                        output_data={'laba_fiskal': laba_fiskal, 'pph_badan': pph_badan_terutang, 'pph_kurang_bayar': pph_kurang_bayar}
                    )
            
            with col2:
                st.markdown("#### Hasil Perhitungan")
                
                if 'pph_badan_result' in st.session_state:
                    result = st.session_state.pph_badan_result
                    
                    # Key Metrics
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Laba Kotor", f"Rp {result['laba_kotor']:,.0f}")
                        st.metric("Laba Fiskal (PKP)", f"Rp {result['laba_fiskal']:,.0f}")
                    
                    with col_b:
                        st.metric("PPh Badan Terutang", f"Rp {result['pph_badan']:,.0f}",
                                 delta=f"{result['tarif_efektif']:.2f}%")
                        st.metric("PPh Kurang/(Lebih) Bayar", f"Rp {result['pph_kurang_bayar']:,.0f}")
                    
                    if result['is_umkm']:
                        st.success("✅ Mendapat fasilitas tarif UMKM")
                    
                    st.markdown("---")
                    
                    # Detailed Breakdown
                    st.markdown("##### Rincian Perhitungan")
                    detail_df = pd.DataFrame({
                        'Keterangan': [
                            'Omzet',
                            'Biaya Operasional',
                            'Penghasilan Lain',
                            'Laba Kotor',
                            'Koreksi Fiskal',
                            'Laba Fiskal (PKP)',
                            'PPh Badan Terutang',
                            'Kredit Pajak',
                            'PPh Kurang Bayar',
                            'Laba Netto'
                        ],
                        'Jumlah (Rp)': [
                            f"{result['omzet']:,.0f}",
                            f"({result['biaya']:,.0f})",
                            f"{result['penghasilan_lain']:,.0f}",
                            f"{result['laba_kotor']:,.0f}",
                            f"{result['koreksi_fiskal']:,.0f}",
                            f"{result['laba_fiskal']:,.0f}",
                            f"({result['pph_badan']:,.0f})",
                            f"{result['kredit_pajak']:,.0f}",
                            f"({result['pph_kurang_bayar']:,.0f})",
                            f"{result['laba_netto']:,.0f}"
                        ]
                    })
                    
                    st.dataframe(detail_df, use_container_width=True, hide_index=True)
                    
                    # Download Buttons
                    col_dl1, col_dl2 = st.columns(2)
                    with col_dl1:
                        st.download_button(
                            "📥 Download CSV",
                            detail_df.to_csv(index=False).encode('utf-8'),
                            "hasil_pph_badan.csv",
                            "text/csv",
                            use_container_width=True
                        )
                    
                    with col_dl2:
                        # Assuming generate_tax_report_pdf and datetime are imported
                        from datetime import datetime
                        pdf_bytes = generate_tax_report_pdf(
                            calc_type="PPh Badan",
                            user_name=st.session_state.get('user_name', 'Anonymous'),
                            company_name=st.session_state.get('company_name', 'N/A'),
                            input_data={
                                'omzet': result['omzet'],
                                'biaya': result['biaya'],
                                'penghasilan_lain': result['penghasilan_lain'],
                                'biaya_tidak_deductible': biaya_tidak_deductible, # Need to pass original inputs
                                'penghasilan_final': penghasilan_final,
                                'koreksi_lainnya': koreksi_lainnya,
                                'is_umkm': result['is_umkm'],
                                'pph_pasal_22': pph_pasal_22,
                                'pph_pasal_23': pph_pasal_23
                            },
                            output_data=result
                        )
                        st.download_button(
                            "📄 Download PDF Report",
                            pdf_bytes,
                            f"Tax_Report_PPhBadan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            "application/pdf",
                            use_container_width=True
                        )
                else:
                    st.info("👈 Masukkan data dan klik tombol Hitung untuk melihat hasil")
        
        # Tab 2: PPh 25 (Installments)
        with pph_badan_tabs[1]:
            st.markdown("#### Perhitungan Angsuran PPh Pasal 25")
            st.caption("Hitung angsuran pajak bulanan berdasarkan pajak tahun sebelumnya")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                pph_tahun_lalu = st.number_input(
                    "PPh Badan Tahun Lalu (Rp)",
                    min_value=0,
                    value=50000000,
                    step=1000000,
                    format="%d",
                    help="PPh Badan terutang tahun pajak sebelumnya"
                )
                
                kredit_pajak_tahun_lalu = st.number_input(
                    "Kredit Pajak Tahun Lalu (Rp)",
                    min_value=0,
                    value=0,
                    step=100000,
                    format="%d",
                    help="PPh 22, PPh 23 tahun lalu"
                )
                
                bulan_berjalan = st.slider(
                    "Bulan Berjalan",
                    min_value=1,
                    max_value=12,
                    value=6,
                    help="Untuk menghitung total angsuran yang sudah dibayar"
                )
                
                if st.button("🧮 Hitung PPh 25", use_container_width=True):
                    # PPh 25 calculation
                    pph_netto_tahun_lalu = pph_tahun_lalu - kredit_pajak_tahun_lalu
                    pph_25_bulanan = pph_netto_tahun_lalu / 12
                    total_angsuran_dibayar = pph_25_bulanan * bulan_berjalan
                    sisa_angsuran = pph_25_bulanan * (12 - bulan_berjalan)
                    
                    st.session_state.pph25_result = {
                        'pph_tahun_lalu': pph_tahun_lalu,
                        'kredit_pajak': kredit_pajak_tahun_lalu,
                        'pph_netto': pph_netto_tahun_lalu,
                        'pph25_bulanan': pph_25_bulanan,
                        'bulan_berjalan': bulan_berjalan,
                        'total_dibayar': total_angsuran_dibayar,
                        'sisa_angsuran': sisa_angsuran
                    }
            
            with col2:
                if 'pph25_result' in st.session_state:
                    result = st.session_state.pph25_result
                    
                    st.metric("PPh 25 per Bulan", f"Rp {result['pph25_bulanan']:,.0f}")
                    st.metric("Total Angsuran s.d. Bulan Ini", f"Rp {result['total_dibayar']:,.0f}")
                    st.metric("Sisa Angsuran", f"Rp {result['sisa_angsuran']:,.0f}")
                    
                    st.markdown("---")
                    st.markdown("##### Jadwal Angsuran PPh 25")
                    
                    # Create monthly schedule
                    bulan_names = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
                    schedule_data = []
                    
                    for i in range(12):
                        status = "✅ Dibayar" if i < result['bulan_berjalan'] else "⏳ Belum Bayar"
                        schedule_data.append({
                            'Bulan': bulan_names[i],
                            'Angsuran (Rp)': f"{result['pph25_bulanan']:,.0f}",
                            'Status': status
                        })
                    
                    schedule_df = pd.DataFrame(schedule_data)
                    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
                else:
                    st.info("👈 Masukkan data untuk menghitung PPh 25")
        
        # Tab 3: Multi-Year Projection
        with pph_badan_tabs[2]:
            st.markdown("#### Proyeksi Pajak Multi-Tahun")
            st.caption("Proyeksikan pajak perusahaan untuk 3-5 tahun ke depan")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                omzet_awal = st.number_input(
                    "Omzet Tahun Ini (Rp)",
                    min_value=0,
                    value=1000000000,
                    step=10000000,
                    format="%d",
                    key="omzet_proj"
                )
                
                pertumbuhan_omzet = st.slider(
                    "Proyeksi Pertumbuhan Omzet (%/tahun)",
                    min_value=0,
                    max_value=50,
                    value=15,
                    step=1
                )
                
                margin_laba = st.slider(
                    "Margin Laba Kotor (%)",
                    min_value=0,
                    max_value=100,
                    value=50,
                    step=1
                )
                
                tahun_proyeksi = st.selectbox(
                    "Periode Proyeksi",
                    [3, 4, 5],
                    index=0
                )
                
                is_umkm_proj = st.checkbox("UMKM", value=False, key="umkm_proj")
                
                if st.button("📈 Buat Proyeksi", use_container_width=True):
                    proyeksi_data = []
                    
                    for tahun in range(tahun_proyeksi):
                        omzet_tahun = omzet_awal * ((1 + pertumbuhan_omzet/100) ** tahun)
                        laba_kotor = omzet_tahun * (margin_laba / 100)
                        
                        # Calculate tax
                        if is_umkm_proj and omzet_tahun <= 4800000000:
                            if laba_kotor <= 500000000:
                                pajak = laba_kotor * 0.11
                            else:
                                pajak = 500000000 * 0.11 + (laba_kotor - 500000000) * 0.22
                        else:
                            pajak = laba_kotor * 0.22
                        
                        laba_netto = laba_kotor - pajak
                        
                        proyeksi_data.append({
                            'Tahun': f"Tahun {tahun + 1}",
                            'Omzet': omzet_tahun,
                            'Laba Kotor': laba_kotor,
                            'PPh Badan': pajak,
                            'Laba Netto': laba_netto
                        })
                    
                    st.session_state.proyeksi_result = proyeksi_data
            
            with col2:
                if 'proyeksi_result' in st.session_state:
                    data = st.session_state.proyeksi_result
                    
                    # Display table
                    display_df = pd.DataFrame(data)
                    display_df['Omzet'] = display_df['Omzet'].apply(lambda x: f"Rp {x:,.0f}")
                    display_df['Laba Kotor'] = display_df['Laba Kotor'].apply(lambda x: f"Rp {x:,.0f}")
                    display_df['PPh Badan'] = display_df['PPh Badan'].apply(lambda x: f"Rp {x:,.0f}")
                    display_df['Laba Netto'] = display_df['Laba Netto'].apply(lambda x: f"Rp {x:,.0f}")
                    
                    st.dataframe(display_df, use_container_width=True, hide_index=True)
                    
                    # Chart
                    st.markdown("##### Grafik Proyeksi")
                    
                    chart_data = pd.DataFrame(data)
                    
                    fig = go.Figure()
                    fig.add_trace(go.Bar(
                        name='Omzet',
                        x=chart_data['Tahun'],
                        y=chart_data['Omzet'],
                        marker_color='#667eea'
                    ))
                    fig.add_trace(go.Bar(
                        name='Laba Netto',
                        x=chart_data['Tahun'],
                        y=chart_data['Laba Netto'],
                        marker_color='#764ba2'
                    ))
                    fig.add_trace(go.Bar(
                        name='PPh Badan',
                        x=chart_data['Tahun'],
                        y=chart_data['PPh Badan'],
                        marker_color='#f093fb'
                    ))
                    
                    fig.update_layout(
                        barmode='group',
                        height=400,
                        xaxis_title="Tahun",
                        yaxis_title="Jumlah (Rp)",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("👈 Masukkan parameter proyeksi")
        
        # Tab 4: Scenario Comparison
        with pph_badan_tabs[3]:
            st.markdown("#### Perbandingan Skenario UMKM vs Non-UMKM")
            st.caption("Bandingkan beban pajak dengan status UMKM dan Non-UMKM")
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                omzet_skenario = st.number_input(
                    "Omzet Tahunan (Rp)",
                    min_value=0,
                    value=3000000000,
                    step=100000000,
                    format="%d",
                    key="omzet_skenario"
                )
                
                margin_skenario = st.slider(
                    "Margin Laba (%)",
                    min_value=0,
                    max_value=100,
                    value=40,
                    step=1,
                    key="margin_skenario"
                )
                
                if st.button("⚖️ Bandingkan Skenario", use_container_width=True):
                    laba_kotor = omzet_skenario * (margin_skenario / 100)
                    
                    # Scenario 1: UMKM
                    if omzet_skenario <= 4800000000:
                        if laba_kotor <= 500000000:
                            pajak_umkm = laba_kotor * 0.11
                        else:
                            pajak_umkm = 500000000 * 0.11 + (laba_kotor - 500000000) * 0.22
                    else:
                        pajak_umkm = laba_kotor * 0.22  # Tidak eligible UMKM
                    
                    # Scenario 2: Non-UMKM
                    pajak_non_umkm = laba_kotor * 0.22
                    
                    # Calculate savings
                    penghematan = pajak_non_umkm - pajak_umkm
                    persentase_hemat = (penghematan / pajak_non_umkm * 100) if pajak_non_umkm > 0 else 0
                    
                    st.session_state.skenario_result = {
                        'omzet': omzet_skenario,
                        'laba_kotor': laba_kotor,
                        'pajak_umkm': pajak_umkm,
                        'pajak_non_umkm': pajak_non_umkm,
                        'penghematan': penghematan,
                        'persentase_hemat': persentase_hemat,
                        'eligible_umkm': omzet_skenario <= 4800000000
                    }
            
            with col2:
                if 'skenario_result' in st.session_state:
                    result = st.session_state.skenario_result
                    
                    if result['eligible_umkm']:
                        st.success("✅ Eligible untuk fasilitas UMKM")
                    else:
                        st.warning("⚠️ Omzet melebihi batas UMKM (4.8 Miliar)")
                    
                    st.markdown("##### Perbandingan Pajak")
                    
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("PPh Badan (UMKM)", f"Rp {result['pajak_umkm']:,.0f}")
                    with col_b:
                        st.metric("PPh Badan (Non-UMKM)", f"Rp {result['pajak_non_umkm']:,.0f}")
                    
                    if result['penghematan'] > 0:
                        st.success(f"💰 Penghematan dengan UMKM: **Rp {result['penghematan']:,.0f}** ({result['persentase_hemat']:.2f}%)")
                    
                    # Comparison chart
                    fig = go.Figure(data=[
                        go.Bar(
                            name='UMKM',
                            x=['PPh Badan'],
                            y=[result['pajak_umkm']],
                            marker_color='#667eea',
                            text=[f"Rp {result['pajak_umkm']:,.0f}"],
                            textposition='auto'
                        ),
                        go.Bar(
                            name='Non-UMKM',
                            x=['PPh Badan'],
                            y=[result['pajak_non_umkm']],
                            marker_color='#f093fb',
                            text=[f"Rp {result['pajak_non_umkm']:,.0f}"],
                            textposition='auto'
                        )
                    ])
                    
                    fig.update_layout(
                        barmode='group',
                        height=300,
                        yaxis_title="Pajak (Rp)",
                        showlegend=True
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("👈 Masukkan data untuk perbandingan")
        
        # Tab 5: Tax Planning Recommendations
        with pph_badan_tabs[4]:
            st.markdown("#### Rekomendasi Tax Planning")
            st.caption("Strategi optimasi pajak yang legal dan sesuai regulasi")
            
            st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 10px; color: white; margin-bottom: 1rem;'>
                <h4>💡 Strategi Pengurangan Beban Pajak</h4>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 1. Manfaatkan Fasilitas UMKM")
                st.write("""
                - Tarif 11% untuk PKP ≤ 500 juta (vs 22%)
                - Syarat: Omzet ≤ 4.8 miliar/tahun
                - Penghematan signifikan untuk perusahaan kecil
                """)
                
                st.markdown("##### 2. Optimalkan Biaya Deductible")
                st.write("""
                - Biaya R&D dan pelatihan karyawan
                - Biaya promosi dan iklan
                - Biaya CSR (sesuai ketentuan)
                - Penyusutan aset tetap
                """)
                
                st.markdown("##### 3. Manfaatkan Kredit Pajak")
                st.write("""
                - PPh Pasal 22 (impor/pembelian)
                - PPh Pasal 23 (jasa/dividen)
                - PPh Pasal 24 (luar negeri)
                """)
            
            with col2:
                st.markdown("##### 4. Perencanaan Investasi")
                st.write("""
                - Tax holiday untuk industri tertentu
                - Tax allowance untuk investasi besar
                - Super deduction untuk vokasi & R&D
                """)
                
                st.markdown("##### 5. Timing Strategy")
                st.write("""
                - Percepat biaya di akhir tahun
                - Tunda penghasilan ke tahun berikutnya
                - Optimalkan PPh 25 (angsuran)
                """)
                
                st.markdown("##### 6. Restrukturisasi Bisnis")
                st.write("""
                - Pisahkan unit bisnis jika perlu
                - Pertimbangkan holding company
                - Evaluasi struktur kepemilikan
                """)
            
            st.markdown("---")
            
            st.warning("""
            ⚠️ **Disclaimer**: Semua strategi tax planning harus dilakukan sesuai dengan peraturan perpajakan yang berlaku. 
            Konsultasikan dengan konsultan pajak profesional sebelum mengimplementasikan strategi apapun.
            """)
            
            st.info("""
            📞 **Butuh Konsultasi?**  
            Hubungi tim TaxPro Indonesia untuk konsultasi tax planning yang disesuaikan dengan kondisi perusahaan Anda.
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # PBB Calculator (Pajak Bumi dan Bangunan)
    with tax_tab[4]:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Kalkulator PBB - Pajak Bumi dan Bangunan")
        st.caption("Hitung pajak properti tahunan berdasarkan NJOP")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Input Data Properti")
            
            st.markdown("##### 🏞️ Data Tanah")
            luas_tanah = st.number_input(
                "Luas Tanah (m²)",
                min_value=0,
                value=100,
                step=1,
                format="%d"
            )
            
            njop_tanah_per_m2 = st.number_input(
                "NJOP Tanah per m² (Rp)",
                min_value=0,
                value=1000000,
                step=10000,
                format="%d",
                help="Nilai Jual Objek Pajak tanah per meter persegi"
            )
            
            st.markdown("##### 🏠 Data Bangunan")
            luas_bangunan = st.number_input(
                "Luas Bangunan (m²)",
                min_value=0,
                value=80,
                step=1,
                format="%d"
            )
            
            njop_bangunan_per_m2 = st.number_input(
                "NJOP Bangunan per m² (Rp)",
                min_value=0,
                value=1500000,
                step=10000,
                format="%d",
                help="Nilai Jual Objek Pajak bangunan per meter persegi"
            )
            
            st.markdown("##### ⚙️ Pengaturan")
            njoptkp = st.number_input(
                "NJOPTKP - Nilai Tidak Kena Pajak (Rp)",
                min_value=0,
                value=10000000,
                step=1000000,
                format="%d",
                help="Bervariasi per daerah, umumnya Rp 10-15 juta"
            )
            
            tarif_pbb = st.selectbox(
                "Tarif PBB",
                ["0.5% (Standar)", "0.3% (NJOP < 1 Miliar)", "0.2% (Khusus)"]
            )
            
            if st.button("🧮 Hitung PBB", use_container_width=True):
                # Calculate NJOP
                njop_tanah = luas_tanah * njop_tanah_per_m2
                njop_bangunan = luas_bangunan * njop_bangunan_per_m2
                njop_total = njop_tanah + njop_bangunan
                
                # Calculate taxable NJOP
                njop_kena_pajak = max(0, njop_total - njoptkp)
                
                # Determine tax rate
                if "0.3%" in tarif_pbb:
                    rate = 0.003
                elif "0.2%" in tarif_pbb:
                    rate = 0.002
                else:
                    rate = 0.005
                
                # Calculate PBB
                pbb_terutang = njop_kena_pajak * rate
                
                st.session_state.pbb_result = {
                    'luas_tanah': luas_tanah,
                    'njop_tanah_per_m2': njop_tanah_per_m2,
                    'njop_tanah': njop_tanah,
                    'luas_bangunan': luas_bangunan,
                    'njop_bangunan_per_m2': njop_bangunan_per_m2,
                    'njop_bangunan': njop_bangunan,
                    'njop_total': njop_total,
                    'njoptkp': njoptkp,
                    'njop_kena_pajak': njop_kena_pajak,
                    'tarif': rate * 100,
                    'pbb': pbb_terutang
                }
                
                # Save audit log
                save_audit_log(
                    calc_type="PBB",
                    user_name=st.session_state.get('user_name', 'Anonymous'),
                    company_name=st.session_state.get('company_name', 'N/A'),
                    input_data={'luas_tanah': luas_tanah, 'njop_tanah_per_m2': njop_tanah_per_m2, 'luas_bangunan': luas_bangunan, 'njop_bangunan_per_m2': njop_bangunan_per_m2},
                    output_data={'njop_total': njop_total, 'njop_kena_pajak': njop_kena_pajak, 'pbb': pbb_terutang}
                )
        
        with col2:
            st.markdown("#### Hasil Perhitungan")
            
            if 'pbb_result' in st.session_state:
                result = st.session_state.pbb_result
                
                # Key Metrics
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("NJOP Total", f"Rp {result['njop_total']:,.0f}")
                    st.metric("NJOP Kena Pajak", f"Rp {result['njop_kena_pajak']:,.0f}")
                
                with col_b:
                    st.metric("Tarif PBB", f"{result['tarif']:.2f}%")
                    st.metric("PBB Terutang/Tahun", f"Rp {result['pbb']:,.0f}")
                
                st.markdown("---")
                
                # Visualization
                st.markdown("##### Komposisi NJOP")
                fig = go.Figure(data=[go.Pie(
                    labels=['NJOP Tanah', 'NJOP Bangunan'],
                    values=[result['njop_tanah'], result['njop_bangunan']],
                    hole=.4,
                    marker_colors=['#667eea', '#764ba2']
                )])
                
                fig.update_layout(
                    height=250,
                    showlegend=True,
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed Breakdown
                st.markdown("##### Rincian Perhitungan")
                detail_df = pd.DataFrame({
                    'Keterangan': [
                        f'Tanah ({result["luas_tanah"]:,.0f} m²)',
                        f'Bangunan ({result["luas_bangunan"]:,.0f} m²)',
                        'NJOP Total',
                        'NJOPTKP',
                        'NJOP Kena Pajak',
                        'PBB Terutang'
                    ],
                    'Nilai (Rp)': [
                        f"{result['njop_tanah']:,.0f}",
                        f"{result['njop_bangunan']:,.0f}",
                        f"{result['njop_total']:,.0f}",
                        f"({result['njoptkp']:,.0f})",
                        f"{result['njop_kena_pajak']:,.0f}",
                        f"{result['pbb']:,.0f}"
                    ]
                })
                
                st.dataframe(detail_df, use_container_width=True, hide_index=True)
                
                # Download Buttons
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        "📥 Download CSV",
                        detail_df.to_csv(index=False).encode('utf-8'),
                        "hasil_pbb.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col_dl2:
                    pdf_bytes = generate_tax_report_pdf(
                        calc_type="PBB",
                        user_name=st.session_state.get('user_name', 'Anonymous'),
                        company_name=st.session_state.get('company_name', 'N/A'),
                        input_data={'luas_tanah': luas_tanah, 'njop_tanah_per_m2': njop_tanah_per_m2, 'luas_bangunan': luas_bangunan, 'njop_bangunan_per_m2': njop_bangunan_per_m2},
                        output_data=result
                    )
                    st.download_button(
                        "📄 Download PDF Report",
                        pdf_bytes,
                        f"Tax_Report_PBB_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        "application/pdf",
                        use_container_width=True
                    )
            else:
                st.info("👈 Masukkan data properti dan klik tombol Hitung untuk melihat hasil")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # PKB Calculator (Pajak Kendaraan Bermotor)
    with tax_tab[5]:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Kalkulator PKB - Pajak Kendaraan Bermotor")
        st.caption("Hitung pajak kendaraan tahunan")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Input Data Kendaraan")
            
            jenis_kendaraan = st.selectbox(
                "Jenis Kendaraan",
                ["Motor", "Mobil Pribadi", "Mobil Komersial", "Truk", "Bus"]
            )
            
            nilai_jual = st.number_input(
                "Nilai Jual Kendaraan (Rp)",
                min_value=0,
                value=20000000,
                step=1000000,
                format="%d",
                help="Sesuai dengan NJKB (Nilai Jual Kendaraan Bermotor)"
            )
            
            provinsi = st.selectbox(
                "Provinsi",
                ["DKI Jakarta (2%)", "Jawa Barat (1.75%)", "Jawa Tengah (1.5%)", 
                 "Jawa Timur (1.5%)", "Bali (1.5%)", "Lainnya (1.5%)"]
            )
            
            tahun_kendaraan = st.number_input(
                "Tahun Kendaraan",
                min_value=1980,
                max_value=datetime.now().year,
                value=2020,
                step=1
            )
            
            bobot_koefisien = st.slider(
                "Bobot/Koefisien",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Untuk kendaraan komersial atau berdasarkan fungsi"
            )
            
            if st.button("🧮 Hitung PKB", use_container_width=True):
                # Determine provincial rate
                if "2%" in provinsi:
                    tarif_provinsi = 0.02
                elif "1.75%" in provinsi:
                    tarif_provinsi = 0.0175
                else:
                    tarif_provinsi = 0.015
                
                # Calculate PKB
                pkb = nilai_jual * tarif_provinsi * bobot_koefisien
                
                # SWDKLLJ (fixed amount based on vehicle type)
                if jenis_kendaraan == "Motor":
                    swdkllj = 35000
                elif jenis_kendaraan == "Mobil Pribadi":
                    swdkllj = 143000
                elif jenis_kendaraan in ["Mobil Komersial", "Truk"]:
                    swdkllj = 163000
                else:  # Bus
                    swdkllj = 166000
                
                # Administrative fee
                biaya_admin = 50000
                
                total_pajak = pkb + swdkllj + biaya_admin
                
                # Calculate depreciation factor
                umur_kendaraan = datetime.now().year - tahun_kendaraan
                
                st.session_state.pkb_result = {
                    'jenis': jenis_kendaraan,
                    'nilai_jual': nilai_jual,
                    'provinsi': provinsi,
                    'tarif': tarif_provinsi * 100,
                    'bobot': bobot_koefisien,
                    'pkb': pkb,
                    'swdkllj': swdkllj,
                    'admin': biaya_admin,
                    'total': total_pajak,
                    'umur': umur_kendaraan
                }
                
                # Save audit log
                save_audit_log(
                    calc_type="PKB",
                    user_name=st.session_state.get('user_name', 'Anonymous'),
                    company_name=st.session_state.get('company_name', 'N/A'),
                    input_data={'jenis': jenis_kendaraan, 'nilai_jual': nilai_jual, 'provinsi': provinsi, 'tahun': tahun_kendaraan},
                    output_data={'pkb': pkb, 'swdkllj': swdkllj, 'total': total_pajak}
                )
        
        with col2:
            st.markdown("#### Hasil Perhitungan")
            
            if 'pkb_result' in st.session_state:
                result = st.session_state.pkb_result
                
                # Key Metrics
                st.metric("PKB (Pajak Kendaraan)", f"Rp {result['pkb']:,.0f}")
                st.metric("SWDKLLJ", f"Rp {result['swdkllj']:,.0f}")
                st.metric("Total yang Harus Dibayar", f"Rp {result['total']:,.0f}")
                
                st.markdown("---")
                
                # Breakdown Chart
                st.markdown("##### Breakdown Biaya")
                fig = go.Figure(data=[go.Bar(
                    x=['PKB', 'SWDKLLJ', 'Admin'],
                    y=[result['pkb'], result['swdkllj'], result['admin']],
                    marker_color=['#667eea', '#764ba2', '#f093fb'],
                    text=[f"Rp {result['pkb']:,.0f}", 
                          f"Rp {result['swdkllj']:,.0f}", 
                          f"Rp {result['admin']:,.0f}"],
                    textposition='auto'
                )])
                
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    yaxis_title="Jumlah (Rp)",
                    margin=dict(t=20, b=0, l=0, r=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed Table
                st.markdown("##### Rincian Pembayaran")
                detail_df = pd.DataFrame({
                    'Komponen': [
                        'Jenis Kendaraan',
                        'Nilai Jual Kendaraan',
                        'Provinsi',
                        'Tarif',
                        'Bobot/Koefisien',
                        'PKB',
                        'SWDKLLJ',
                        'Biaya Admin',
                        'Total Pajak'
                    ],
                    'Keterangan': [
                        result['jenis'],
                        f"Rp {result['nilai_jual']:,.0f}",
                        result['provinsi'],
                        f"{result['tarif']:.2f}%",
                        f"{result['bobot']:.1f}",
                        f"Rp {result['pkb']:,.0f}",
                        f"Rp {result['swdkllj']:,.0f}",
                        f"Rp {result['admin']:,.0f}",
                        f"Rp {result['total']:,.0f}"
                    ]
                })
                
                st.dataframe(detail_df, use_container_width=True, hide_index=True)
                
                if result['umur'] > 10:
                    st.warning(f"⚠️ Kendaraan berusia {result['umur']} tahun. Pertimbangkan biaya tambahan untuk uji emisi.")
                
                # Download Buttons
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        "📥 Download CSV",
                        detail_df.to_csv(index=False).encode('utf-8'),
                        "hasil_pkb.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col_dl2:
                    pdf_bytes = generate_tax_report_pdf(
                        calc_type="PKB",
                        user_name=st.session_state.get('user_name', 'Anonymous'),
                        company_name=st.session_state.get('company_name', 'N/A'),
                        input_data={'jenis': jenis_kendaraan, 'nilai_jual': nilai_jual, 'provinsi': provinsi, 'tahun': tahun_kendaraan},
                        output_data=result
                    )
                    st.download_button(
                        "📄 Download PDF Report",
                        pdf_bytes,
                        f"Tax_Report_PKB_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        "application/pdf",
                        use_container_width=True
                    )
            else:
                st.info("👈 Masukkan data kendaraan dan klik tombol Hitung untuk melihat hasil")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # BPHTB Calculator (Bea Perolehan Hak atas Tanah dan Bangunan)
    with tax_tab[6]:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📊 Kalkulator BPHTB - Bea Perolehan Hak atas Tanah dan Bangunan")
        st.caption("Hitung pajak pembelian/transfer properti")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Input Data Transaksi")
            
            jenis_perolehan = st.selectbox(
                "Jenis Perolehan",
                ["Jual Beli", "Hibah", "Waris", "Tukar Menukar", "Lelang"]
            )
            
            harga_transaksi = st.number_input(
                "Harga Transaksi/NPOP (Rp)",
                min_value=0,
                value=500000000,
                step=10000000,
                format="%d",
                help="Nilai Perolehan Objek Pajak sesuai akta"
            )
            
            st.markdown("##### Data NJOP")
            njop_tanah_bphtb = st.number_input(
                "NJOP Tanah (Rp)",
                min_value=0,
                value=200000000,
                step=10000000,
                format="%d",
                key="njop_tanah_bphtb"
            )
            
            njop_bangunan_bphtb = st.number_input(
                "NJOP Bangunan (Rp)",
                min_value=0,
                value=300000000,
                step=10000000,
                format="%d",
                key="njop_bangunan_bphtb"
            )
            
            st.markdown("##### Pengaturan")
            
            # NPOPTKP varies by transaction type
            if jenis_perolehan == "Waris":
                default_npoptkp = 300000000
                help_text = "Untuk waris, NPOPTKP umumnya Rp 300 juta"
            elif jenis_perolehan == "Hibah":
                default_npoptkp = 60000000
                help_text = "Untuk hibah, NPOPTKP umumnya Rp 60 juta"
            else:
                default_npoptkp = 80000000
                help_text = "Untuk jual beli, NPOPTKP umumnya Rp 60-80 juta (bervariasi per daerah)"
            
            npoptkp = st.number_input(
                "NPOPTKP - Nilai Tidak Kena Pajak (Rp)",
                min_value=0,
                value=default_npoptkp,
                step=10000000,
                format="%d",
                help=help_text
            )
            
            tarif_bphtb = st.selectbox(
                "Tarif BPHTB",
                ["5% (Standar)", "2.5% (Khusus Waris/Hibah Keluarga)"]
            )
            
            if st.button("🧮 Hitung BPHTB", use_container_width=True):
                # Calculate NJOP total
                njop_total_bphtb = njop_tanah_bphtb + njop_bangunan_bphtb
                
                # Dasar pengenaan is the higher of transaction price or NJOP
                dasar_pengenaan = max(harga_transaksi, njop_total_bphtb)
                
                # Calculate taxable amount
                npop_kena_pajak = max(0, dasar_pengenaan - npoptkp)
                
                # Determine rate
                if "2.5%" in tarif_bphtb:
                    rate = 0.025
                else:
                    rate = 0.05
                
                # Calculate BPHTB
                bphtb_terutang = npop_kena_pajak * rate
                
                # Total cost including notary and other fees (estimated)
                biaya_notaris = harga_transaksi * 0.01  # ~1% of transaction
                biaya_lainnya = 5000000  # Administrative fees
                total_biaya_transaksi = harga_transaksi + bphtb_terutang + biaya_notaris + biaya_lainnya
                
                st.session_state.bphtb_result = {
                    'jenis': jenis_perolehan,
                    'harga_transaksi': harga_transaksi,
                    'njop_tanah': njop_tanah_bphtb,
                    'njop_bangunan': njop_bangunan_bphtb,
                    'njop_total': njop_total_bphtb,
                    'dasar_pengenaan': dasar_pengenaan,
                    'npoptkp': npoptkp,
                    'npop_kena_pajak': npop_kena_pajak,
                    'tarif': rate * 100,
                    'bphtb': bphtb_terutang,
                    'biaya_notaris': biaya_notaris,
                    'biaya_lainnya': biaya_lainnya,
                    'total_biaya': total_biaya_transaksi
                }
                
                # Save audit log
                save_audit_log(
                    calc_type="BPHTB",
                    user_name=st.session_state.get('user_name', 'Anonymous'),
                    company_name=st.session_state.get('company_name', 'N/A'),
                    input_data={'jenis': jenis_perolehan, 'harga_transaksi': harga_transaksi, 'njop_total': njop_total_bphtb},
                    output_data={'dasar_pengenaan': dasar_pengenaan, 'bphtb': bphtb_terutang, 'total_biaya': total_biaya_transaksi}
                )
        
        with col2:
            st.markdown("#### Hasil Perhitungan")
            
            if 'bphtb_result' in st.session_state:
                result = st.session_state.bphtb_result
                
                # Key Metrics
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Dasar Pengenaan", f"Rp {result['dasar_pengenaan']:,.0f}")
                    st.metric("NPOP Kena Pajak", f"Rp {result['npop_kena_pajak']:,.0f}")
                
                with col_b:
                    st.metric("BPHTB Terutang", f"Rp {result['bphtb']:,.0f}", 
                             delta=f"{result['tarif']:.1f}%")
                    st.metric("Total Biaya Transaksi", f"Rp {result['total_biaya']:,.0f}")
                
                st.markdown("---")
                
                # Cost Breakdown
                st.markdown("##### Breakdown Biaya Transaksi")
                fig = go.Figure(data=[go.Pie(
                    labels=['Harga Properti', 'BPHTB', 'Notaris', 'Lainnya'],
                    values=[result['harga_transaksi'], result['bphtb'], 
                           result['biaya_notaris'], result['biaya_lainnya']],
                    hole=.4,
                    marker_colors=['#667eea', '#764ba2', '#f093fb', '#a8edea']
                )])
                
                fig.update_layout(
                    height=250,
                    showlegend=True,
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Detailed Breakdown
                st.markdown("##### Rincian Perhitungan")
                detail_df = pd.DataFrame({
                    'Keterangan': [
                        'Jenis Perolehan',
                        'Harga Transaksi',
                        'NJOP Total',
                        'Dasar Pengenaan',
                        'NPOPTKP',
                        'NPOP Kena Pajak',
                        'Tarif BPHTB',
                        'BPHTB Terutang',
                        'Biaya Notaris (est.)',
                        'Biaya Lainnya (est.)',
                        'Total Biaya Transaksi'
                    ],
                    'Nilai': [
                        result['jenis'],
                        f"Rp {result['harga_transaksi']:,.0f}",
                        f"Rp {result['njop_total']:,.0f}",
                        f"Rp {result['dasar_pengenaan']:,.0f}",
                        f"(Rp {result['npoptkp']:,.0f})",
                        f"Rp {result['npop_kena_pajak']:,.0f}",
                        f"{result['tarif']:.1f}%",
                        f"Rp {result['bphtb']:,.0f}",
                        f"Rp {result['biaya_notaris']:,.0f}",
                        f"Rp {result['biaya_lainnya']:,.0f}",
                        f"Rp {result['total_biaya']:,.0f}"
                    ]
                })
                
                st.dataframe(detail_df, use_container_width=True, hide_index=True)
                
                # Important Notes
                if result['dasar_pengenaan'] > result['harga_transaksi']:
                    st.warning("⚠️ NJOP lebih tinggi dari harga transaksi. Dasar pengenaan menggunakan NJOP.")
                
                st.info("💡 **Catatan:** Biaya notaris dan biaya lainnya adalah estimasi. Konsultasikan dengan notaris untuk biaya aktual.")
                
                # Download Buttons
                col_dl1, col_dl2 = st.columns(2)
                with col_dl1:
                    st.download_button(
                        "📥 Download CSV",
                        detail_df.to_csv(index=False).encode('utf-8'),
                        "hasil_bphtb.csv",
                        "text/csv",
                        use_container_width=True
                    )
                
                with col_dl2:
                    pdf_bytes = generate_tax_report_pdf(
                        calc_type="BPHTB",
                        user_name=st.session_state.get('user_name', 'Anonymous'),
                        company_name=st.session_state.get('company_name', 'N/A'),
                        input_data={'jenis': jenis_perolehan, 'harga_transaksi': harga_transaksi, 'njop_total': njop_total_bphtb},
                        output_data=result
                    )
                    st.download_button(
                        "📄 Download PDF Report",
                        pdf_bytes,
                        f"Tax_Report_BPHTB_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        "application/pdf",
                        use_container_width=True
                    )
            else:
                st.info("👈 Masukkan data transaksi dan klik tombol Hitung untuk melihat hasil")
        
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "🏭 Biaya Produksi":
    st.markdown("""
    <div class="main-header">
        <h1>🏭 Manajemen Biaya Produksi</h1>
        <p>Analisis biaya produksi dan tentukan harga jual yang optimal</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Input Biaya Produksi")
        
        st.markdown("#### 📦 Biaya Bahan Baku Langsung")
        bahan_baku = st.number_input("Bahan Baku (Rp)", min_value=0, value=0, step=1000)
        kemasan = st.number_input("Kemasan (Rp)", min_value=0, value=0, step=1000)
        
        st.markdown("#### 👷 Biaya Tenaga Kerja Langsung")
        upah = st.number_input("Upah Tenaga Kerja (Rp)", min_value=0, value=0, step=1000)
        
        st.markdown("#### ⚙️ Biaya Overhead Pabrik")
        listrik = st.number_input("Listrik & Air (Rp)", min_value=0, value=0, step=1000)
        sewa = st.number_input("Sewa Pabrik (Rp)", min_value=0, value=0, step=1000)
        pemeliharaan = st.number_input("Pemeliharaan Mesin (Rp)", min_value=0, value=0, step=1000)
        depresiasi = st.number_input("Depresiasi (Rp)", min_value=0, value=0, step=1000)
        
        st.markdown("#### 📊 Target & Volume")
        volume = st.number_input("Volume Produksi (Unit)", min_value=1, value=100, step=1)
        target_margin = st.number_input("Target Margin Keuntungan (%)", min_value=0, max_value=100, value=30, step=1)
        
        if st.button("🧮 Hitung Biaya Produksi", use_container_width=True):
            # Calculate costs
            total_bahan_baku = bahan_baku + kemasan
            total_tenaga_kerja = upah
            total_overhead = listrik + sewa + pemeliharaan + depresiasi
            
            total_biaya = total_bahan_baku + total_tenaga_kerja + total_overhead
            biaya_per_unit = total_biaya / volume if volume > 0 else 0
            
            harga_jual = biaya_per_unit * (1 + target_margin/100)
            keuntungan_per_unit = harga_jual - biaya_per_unit
            keuntungan_total = keuntungan_per_unit * volume
            
            st.session_state.production_result = {
                'bahan_baku': total_bahan_baku,
                'tenaga_kerja': total_tenaga_kerja,
                'overhead': total_overhead,
                'total_biaya': total_biaya,
                'volume': volume,
                'biaya_per_unit': biaya_per_unit,
                'margin': target_margin,
                'harga_jual': harga_jual,
                'keuntungan_per_unit': keuntungan_per_unit,
                'keuntungan_total': keuntungan_total
            }
    
    with col2:
        st.markdown("### 📊 Hasil Analisis")
        
        if 'production_result' in st.session_state:
            result = st.session_state.production_result
            
            # Key Metrics
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Total Biaya Produksi", f"Rp {result['total_biaya']:,.0f}")
                st.metric("Biaya per Unit", f"Rp {result['biaya_per_unit']:,.0f}")
            
            with col_b:
                st.metric("Harga Jual Optimal", f"Rp {result['harga_jual']:,.0f}")
                st.metric("Keuntungan Total", f"Rp {result['keuntungan_total']:,.0f}")
            
            st.markdown("---")
            
            # Cost Breakdown Chart
            st.markdown("#### Breakdown Biaya")
            
            fig = go.Figure(data=[go.Pie(
                labels=['Bahan Baku', 'Tenaga Kerja', 'Overhead'],
                values=[result['bahan_baku'], result['tenaga_kerja'], result['overhead']],
                hole=.4,
                marker_colors=['#667eea', '#764ba2', '#f093fb']
            )])
            
            fig.update_layout(
                height=300,
                showlegend=True,
                margin=dict(t=0, b=0, l=0, r=0)
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Detailed Table
            st.markdown("#### Detail Biaya")
            detail_df = pd.DataFrame({
                'Kategori': ['Bahan Baku', 'Tenaga Kerja', 'Overhead', 'Total Biaya', 'Biaya/Unit', 'Harga Jual', 'Keuntungan/Unit'],
                'Jumlah (Rp)': [
                    f"{result['bahan_baku']:,.0f}",
                    f"{result['tenaga_kerja']:,.0f}",
                    f"{result['overhead']:,.0f}",
                    f"{result['total_biaya']:,.0f}",
                    f"{result['biaya_per_unit']:,.0f}",
                    f"{result['harga_jual']:,.0f}",
                    f"{result['keuntungan_per_unit']:,.0f}"
                ]
            })
            
            st.dataframe(detail_df, use_container_width=True, hide_index=True)
            
            # Download
            st.download_button(
                "📥 Download Analisis (CSV)",
                detail_df.to_csv(index=False).encode('utf-8'),
                "analisis_biaya_produksi.csv",
                "text/csv",
                use_container_width=True
            )
        else:
            st.info("👈 Masukkan data biaya dan klik tombol Hitung untuk melihat analisis")
    
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "🤖 AI Tax Advisor":
    st.markdown("""
    <div class="main-header">
        <h1>🤖 AI Tax Advisor</h1>
        <p>Konsultan Pajak Virtual Anda 24/7</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Suggested Questions
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("💡 Pertanyaan Populer")
    st.caption("Klik untuk bertanya langsung")
    
    suggested = get_suggested_questions()
    
    for category_data in suggested:
        st.markdown(f"**{category_data['category']}**")
        cols = st.columns(len(category_data['questions']))
        for idx, question in enumerate(category_data['questions']):
            with cols[idx]:
                if st.button(question, key=f"suggested_{category_data['category']}_{idx}", use_container_width=True):
                    # Add to chat history
                    user_context = {}
                    if 'pph_badan_result' in st.session_state:
                        user_context['omzet'] = st.session_state.pph_badan_result.get('omzet', 0)
                    if 'production_result' in st.session_state:
                        user_context['biaya_produksi'] = st.session_state.production_result.get('total_biaya', 0)
                    
                    response = get_ai_response(question, user_context)
                    st.session_state.chat_history.append({
                        'user': question,
                        'ai': response,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                    st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Chat Interface
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("💬 Chat dengan AI Tax Advisor")
    
    # Display chat history
    if st.session_state.chat_history:
        for chat in st.session_state.chat_history:
            # User message
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 15px; border-radius: 10px; margin: 10px 0;">
                <strong>👤 Anda ({chat['timestamp']}):</strong><br>
                {chat['user']}
            </div>
            """, unsafe_allow_html=True)
            
            # AI response
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); 
                        padding: 15px; border-radius: 10px; margin: 10px 0; 
                        border-left: 4px solid #667eea;">
                <strong>🤖 AI Tax Advisor:</strong>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(chat['ai'])
            st.markdown("---")
    else:
        st.info("💡 Mulai percakapan dengan mengetik pertanyaan atau klik salah satu pertanyaan yang disarankan di atas!")
    
    # Input area
    col1, col2 = st.columns([5, 1])
    with col1:
        user_question = st.text_input(
            "Tanyakan sesuatu...",
            placeholder="Contoh: Bagaimana cara menurunkan PPh Badan 2025?",
            label_visibility="collapsed",
            key="user_input"
        )
    
    with col2:
        send_button = st.button("📤 Send", use_container_width=True)
    
    if send_button and user_question:
        # Get user context
        user_context = {}
        if 'pph_badan_result' in st.session_state:
            user_context['omzet'] = st.session_state.pph_badan_result.get('omzet', 0)
        if 'production_result' in st.session_state:
            user_context['biaya_produksi'] = st.session_state.production_result.get('total_biaya', 0)
        
        # Get AI response
        response = get_ai_response(user_question, user_context)
        
        # Add to chat history
        st.session_state.chat_history.append({
            'user': user_question,
            'ai': response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        st.rerun()
    
    # Action buttons
    if st.session_state.chat_history:
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        with col_b:
            # Export chat history
            chat_text = "AI TAX ADVISOR - CHAT HISTORY\n"
            chat_text += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            chat_text += "="*50 + "\n\n"
            
            for chat in st.session_state.chat_history:
                chat_text += f"[{chat['timestamp']}]\n"
                chat_text += f"USER: {chat['user']}\n\n"
                chat_text += f"AI: {chat['ai']}\n\n"
                chat_text += "-"*50 + "\n\n"
            
            st.download_button(
                "📥 Export Chat",
                chat_text.encode('utf-8'),
                f"ai_tax_advisor_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "text/plain",
                use_container_width=True
            )
        
        with col_c:
            st.metric("Total Pertanyaan", len(st.session_state.chat_history))
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Info & Disclaimer
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### ℹ️ Tentang AI Tax Advisor")
    st.markdown("""
    AI Tax Advisor adalah asisten virtual yang dapat membantu Anda dengan:
    - ✅ Pertanyaan umum perpajakan
    - ✅ Strategi tax planning
    - ✅ Analisis eligibilitas UMKM
    - ✅ Optimasi biaya produksi
    - ✅ Rekomendasi berdasarkan data Anda
    
    **⚠️ Disclaimer:** AI Tax Advisor memberikan informasi umum dan rekomendasi berdasarkan regulasi perpajakan Indonesia. 
    Untuk kasus spesifik dan kompleks, konsultasikan dengan konsultan pajak profesional.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📋 Audit Trail":
    st.markdown("""
    <div class="main-header">
        <h1>📋 Audit Trail</h1>
        <p>Riwayat Perhitungan Pajak untuk Audit & Compliance</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Summary Statistics
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📊 Ringkasan Audit")
    
    summary = get_audit_summary()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Perhitungan", f"{summary['total_calculations']:,}")
    with col2:
        st.metric("Total Pengguna", summary['unique_users'])
    with col3:
        st.metric("Total Perusahaan", summary['unique_companies'])
    with col4:
        most_used = max(summary['calculations_by_type'].items(), key=lambda x: x[1])[0] if summary['calculations_by_type'] else "N/A"
        st.metric("Paling Sering", most_used)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Calculations by Type Chart
    if summary['calculations_by_type']:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 Distribusi Perhitungan per Jenis Pajak")
        
        fig = go.Figure(data=[go.Bar(
            x=list(summary['calculations_by_type'].keys()),
            y=list(summary['calculations_by_type'].values()),
            marker_color='#667eea',
            text=list(summary['calculations_by_type'].values()),
            textposition='auto'
        )])
        
        fig.update_layout(
            height=300,
            xaxis_title="Jenis Pajak",
            yaxis_title="Jumlah Perhitungan",
            showlegend=False,
            margin=dict(t=20, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Filters
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("🔍 Filter & Pencarian")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        start_date = st.date_input(
            "Tanggal Mulai",
            value=None,
            help="Filter berdasarkan tanggal mulai"
        )
    
    with col2:
        end_date = st.date_input(
            "Tanggal Akhir",
            value=None,
            help="Filter berdasarkan tanggal akhir"
        )
    
    with col3:
        calc_types = ["Semua", "PPh 21", "PPh 23", "PPN", "PPh Badan", "PBB", "PKB", "BPHTB"]
        selected_calc_type = st.selectbox(
            "Jenis Pajak",
            calc_types
        )
    
    search_user = st.text_input(
        "Cari Nama Pengguna",
        placeholder="Ketik nama pengguna untuk mencari..."
    )
    
    if st.button("🔍 Terapkan Filter", use_container_width=True):
        st.session_state.filter_applied = True
        st.session_state.filter_params = {
            'start_date': str(start_date) if start_date else None,
            'end_date': str(end_date) if end_date else None,
            'calc_type': selected_calc_type,
            'user_name': search_user
        }
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Audit Logs Table
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.subheader("📋 Riwayat Perhitungan")
    
    # Load logs with filters
    if 'filter_applied' in st.session_state and st.session_state.filter_applied:
        params = st.session_state.filter_params
        df_logs = export_audit_logs(
            start_date=params['start_date'],
            end_date=params['end_date'],
            calc_type=params['calc_type'],
            user_name=params['user_name']
        )
    else:
        df_logs = load_audit_logs(limit=100)  # Load last 100 records
    
    if not df_logs.empty:
        st.info(f"📊 Menampilkan {len(df_logs)} record")
        
        # Display table (without JSON columns for readability)
        display_df = df_logs[['timestamp', 'session_id', 'user_name', 'company_name', 'calculation_type']].copy()
        display_df.columns = ['Waktu', 'Session ID', 'Pengguna', 'Perusahaan', 'Jenis Pajak']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Export Options
        st.markdown("---")
        st.markdown("### 📥 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Export filtered data
            csv_data = df_logs.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Download Audit Log (CSV)",
                csv_data,
                f"audit_trail_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            # Export summary report
            if st.button("📊 Generate Summary Report", use_container_width=True):
                summary_text = f"""
AUDIT TRAIL SUMMARY REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Total Calculations: {len(df_logs)}
Date Range: {df_logs['timestamp'].min()} to {df_logs['timestamp'].max()}

Calculations by Type:
{df_logs['calculation_type'].value_counts().to_string()}

Unique Users: {df_logs['user_name'].nunique()}
Unique Companies: {df_logs['company_name'].nunique()}
                """
                
                st.download_button(
                    "📥 Download Summary Report (TXT)",
                    summary_text.encode('utf-8'),
                    f"audit_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    "text/plain",
                    use_container_width=True
                )
        
        # Detail View
        st.markdown("---")
        st.markdown("### 🔍 Detail Perhitungan")
        
        session_ids = df_logs['session_id'].tolist()
        selected_session = st.selectbox(
            "Pilih Session ID untuk melihat detail",
            ["Pilih..."] + session_ids
        )
        
        if selected_session and selected_session != "Pilih...":
            from audit_logger import get_calculation_details
            import json
            
            details = get_calculation_details(selected_session)
            
            if details:
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("#### 📥 Input Data")
                    st.json(details['input_data'])
                
                with col_b:
                    st.markdown("#### 📊 Output Data")
                    st.json(details['output_data'])
                
                st.info(f"**Waktu:** {details['timestamp']} | **User:** {details['user_name']} | **Perusahaan:** {details['company_name']}")
    else:
        st.warning("📭 Belum ada data audit trail. Lakukan perhitungan pajak untuk mulai mencatat audit log.")
        st.info("💡 **Tip:** Isi nama pengguna dan perusahaan di sidebar sebelum melakukan perhitungan untuk audit trail yang lebih lengkap.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Important Notes
    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("### ⚠️ Catatan Penting")
    st.markdown("""
    - **Audit trail** mencatat semua perhitungan pajak untuk keperluan audit dan compliance
    - Data disimpan secara lokal di file `audit_logs/tax_calculations.csv`
    - Pastikan untuk **backup** file audit log secara berkala
    - Untuk keamanan data, jangan bagikan file audit log kepada pihak yang tidak berwenang
    - Session ID unik untuk setiap perhitungan memudahkan tracking
    """)
    st.markdown("</div>", unsafe_allow_html=True)

elif page == "📞 Kontak":
    st.markdown("""
    <div class="main-header">
        <h1>📞 Hubungi Kami</h1>
        <p>Konsultasi gratis untuk kebutuhan perpajakan Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### 📍 Informasi Kontak")
        
        st.markdown("""
        **📞 Telepon**  
        +62 812-3456-7890
        
        **📧 Email**  
        konsultasi@taxpro.id
        
        **📍 Alamat**  
        Jakarta, Indonesia
        
        **🕐 Jam Operasional**  
        Senin - Jumat: 09.00 - 17.00 WIB
        """)
        
        st.markdown("### 🔗 Media Sosial")
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.markdown("[![WhatsApp](https://img.shields.io/badge/WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/6281234567890)")
        with col_b:
            st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com)")
        with col_c:
            st.markdown("[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://instagram.com)")
        with col_d:
            st.markdown("[![Facebook](https://img.shields.io/badge/Facebook-1877F2?style=for-the-badge&logo=facebook&logoColor=white)](https://facebook.com)")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.markdown("### ✉️ Kirim Pesan")
        
        with st.form("contact_form"):
            nama = st.text_input("Nama Lengkap")
            email = st.text_input("Email")
            telepon = st.text_input("Nomor Telepon")
            subjek = st.selectbox("Subjek", ["Konsultasi Pajak", "Pelaporan SPT", "Pembukuan", "Lainnya"])
            pesan = st.text_area("Pesan", height=150)
            
            submitted = st.form_submit_button("📤 Kirim Pesan", use_container_width=True)
            
            if submitted:
                if nama and email and telepon and pesan:
                    st.success("✅ Pesan Anda telah terkirim! Kami akan menghubungi Anda segera.")
                else:
                    st.error("❌ Mohon lengkapi semua field")
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; color: white;'>
    <p style='font-size: 0.9rem; opacity: 0.8;'>
        © 2026 TaxPro Indonesia. All rights reserved.<br>
        <small>Disclaimer: Kalkulator ini adalah alat bantu estimasi. Untuk perhitungan resmi, silakan konsultasikan dengan konsultan pajak profesional.</small>
    </p>
</div>
""", unsafe_allow_html=True)
