import streamlit as st
import os
from utils.modern_ui import load_custom_css, dashboard_header, section_header

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
    with st.container():
        st.markdown("### 💰 Analisis Usaha Tani")
        st.caption("Hitung RAB, proyeksi laba, break-even analysis, dan unit economics untuk berbagai komoditas pertanian.")
        st.page_link("pages/28_Analisis_Usaha_Tani.py", label="Buka Module →", icon="💰", use_container_width=True)

with col2:
    with st.container():
        st.markdown("### 📈 Analisis Tren Harga")
        st.caption("Pantau tren harga komoditas, analisis volatilitas, dan prediksi harga untuk keputusan jual-beli optimal.")
        st.page_link("pages/6_📈_Analisis_Tren_Harga.py", label="Buka Module →", icon="📈", use_container_width=True)

with col3:
    with st.container():
        st.markdown("### 📊 Dasbor Terpadu")
        st.caption("Dashboard komprehensif dengan visualisasi real-time untuk monitoring performa bisnis pertanian Anda.")
        st.page_link("pages/8_📊_Dasbor_Terpadu.py", label="Buka Module →", icon="📊", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

section_header("🚚 Rantai Pasok & Produk", "Manajemen supply chain dan traceability produk")

col4, col5, col6 = st.columns(3)

with col4:
    with st.container():
        st.markdown("### 🚚 Rantai Pasok Live")
        st.caption("Tracking real-time pergerakan produk dari farm to table dengan blockchain simulation dan carbon footprint.")
        st.page_link("pages/48_🚚_Rantai_Pasok_Live.py", label="Buka Module →", icon="🚚", use_container_width=True)

with col5:
    with st.container():
        st.markdown("### 🏷️ Traceability Produk")
        st.caption("Generate QR code product passport, hash verification, dan consumer feedback loop untuk transparansi produk.")
        st.page_link("pages/49_🏷️_Traceability_Produk.py", label="Buka Module →", icon="🏷️", use_container_width=True)

with col6:
    with st.container():
        st.markdown("### 🌾 Database Panen")
        st.caption("Database lengkap hasil panen dengan analisis produktivitas, kualitas, dan historical data.")
        st.page_link("pages/1_🌾_Database_Panen.py", label="Buka Module →", icon="🌾", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

section_header("👥 Manajemen & SDM", "Tools untuk manajemen tim dan pengembangan SDM")

col7, col8, col9 = st.columns(3)

with col7:
    with st.container():
        st.markdown("### 📢 Ruang Kerja PPL")
        st.caption("Workspace khusus untuk Penyuluh Pertanian Lapangan dengan tools perencanaan dan monitoring kegiatan.")
        st.page_link("pages/45_📢_Ruang_Kerja_PPL_Final.py", label="Buka Module →", icon="📢", use_container_width=True)

with col8:
    with st.container():
        st.markdown("### 📋 Manajemen Proyek")
        st.caption("Project management tools untuk koordinasi tim, task tracking, dan timeline monitoring.")
        st.page_link("pages/50_📋_Manajemen_Proyek_Pertanian.py", label="Buka Module →", icon="📋", use_container_width=True)

with col9:
    with st.container():
        st.markdown("### 🎓 Kurikulum Pelatihan")
        st.caption("Program pelatihan terstruktur untuk pengembangan kapasitas petani dan tim agribisnis.")
        st.page_link("pages/53_🎓_Kurikulum_Pelatihan.py", label="Buka Module →", icon="🎓", use_container_width=True)

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


