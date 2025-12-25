import streamlit as st
import os
from utils.modern_ui import load_custom_css, dashboard_header, feature_card, section_header

st.set_page_config(
    page_title="AgriSensa Biz", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS theme
load_custom_css()

# Dashboard Header
dashboard_header(
    "AgriSensa Biz",
    "Platform Manajemen Keuangan, Rantai Pasok, dan Agribisnis Terpadu",
    user_name=st.session_state.get('user', {}).get('full_name')
)

# Main Content
section_header("💰 Analisis Keuangan", "Tools untuk analisis biaya, proyeksi laba, dan perencanaan finansial")

col1, col2, col3 = st.columns(3)

with col1:
    feature_card(
        "Analisis Usaha Tani",
        "Hitung RAB, proyeksi laba, break-even analysis, dan unit economics untuk berbagai komoditas pertanian.",
        "💰",
        "pages/28_Analisis_Usaha_Tani.py"
    )

with col2:
    feature_card(
        "Analisis Tren Harga",
        "Pantau tren harga komoditas, analisis volatilitas, dan prediksi harga untuk keputusan jual-beli optimal.",
        "📈",
        "pages/6_📈_Analisis_Tren_Harga.py"
    )

with col3:
    feature_card(
        "Dasbor Terpadu",
        "Dashboard komprehensif dengan visualisasi real-time untuk monitoring performa bisnis pertanian Anda.",
        "📊",
        "pages/8_📊_Dasbor_Terpadu.py"
    )

st.markdown("<br>", unsafe_allow_html=True)

section_header("🚚 Rantai Pasok & Produk", "Manajemen supply chain dan traceability produk")

col4, col5, col6 = st.columns(3)

with col4:
    feature_card(
        "Rantai Pasok Live",
        "Tracking real-time pergerakan produk dari farm to table dengan blockchain simulation dan carbon footprint.",
        "🚚",
        "pages/48_🚚_Rantai_Pasok_Live.py"
    )

with col5:
    feature_card(
        "Traceability Produk",
        "Generate QR code product passport, hash verification, dan consumer feedback loop untuk transparansi produk.",
        "🏷️",
        "pages/49_🏷️_Traceability_Produk.py"
    )

with col6:
    feature_card(
        "Database Panen",
        "Database lengkap hasil panen dengan analisis produktivitas, kualitas, dan historical data.",
        "🌾",
        "pages/1_🌾_Database_Panen.py"
    )

st.markdown("<br>", unsafe_allow_html=True)

section_header("👥 Manajemen & SDM", "Tools untuk manajemen tim dan pengembangan SDM")

col7, col8, col9 = st.columns(3)

with col7:
    feature_card(
        "Ruang Kerja PPL",
        "Workspace khusus untuk Penyuluh Pertanian Lapangan dengan tools perencanaan dan monitoring kegiatan.",
        "📢",
        "pages/45_📢_Ruang_Kerja_PPL_Final.py"
    )

with col8:
    feature_card(
        "Manajemen Proyek",
        "Project management tools untuk koordinasi tim, task tracking, dan timeline monitoring.",
        "📋",
        "pages/50_📋_Manajemen_Proyek_Pertanian.py"
    )

with col9:
    feature_card(
        "Kurikulum Pelatihan",
        "Program pelatihan terstruktur untuk pengembangan kapasitas petani dan tim agribisnis.",
        "🎓",
        "pages/53_🎓_Kurikulum_Pelatihan.py"
    )

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

# Debug Section (Collapsible)
with st.expander("🔧 System Information"):
    st.caption("**Current File:**")
    st.code(__file__, language="text")
    st.caption("**Working Directory:**")
    st.code(os.getcwd(), language="text")
    
    try:
        from streamlit.source_util import get_pages
        pages = get_pages("Home.py")
        st.caption("**Registered Pages:**")
        st.json({k: v['page_name'] for k, v in pages.items()})
    except Exception as e:
        st.error(f"Error reading pages: {e}")

