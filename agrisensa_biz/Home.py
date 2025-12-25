import streamlit as st
import os

st.set_page_config(
    page_title="AgriSensa Biz", 
    page_icon="📈", 
    layout="wide"
)

# Header
st.title("📈 AgriSensa Biz")
st.caption("Platform Manajemen Keuangan, Rantai Pasok, dan Agribisnis Terpadu")
st.markdown("---")

# Main Content
st.subheader("💰 Analisis Keuangan")
st.caption("Tools untuk analisis biaya, proyeksi laba, dan perencanaan finansial")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 💰 Analisis Usaha Tani")
    st.caption("Hitung RAB, proyeksi laba, break-even analysis, dan unit economics untuk berbagai komoditas pertanian.")
    st.page_link("pages/28_Analisis_Usaha_Tani.py", label="Buka Module", icon="💰", use_container_width=True)

with col2:
    st.markdown("#### 📈 Analisis Tren Harga")
    st.caption("Pantau tren harga komoditas, analisis volatilitas, dan prediksi harga untuk keputusan jual-beli optimal.")
    st.page_link("pages/6_📈_Analisis_Tren_Harga.py", label="Buka Module", icon="📈", use_container_width=True)

with col3:
    st.markdown("#### 📊 Dasbor Terpadu")
    st.caption("Dashboard komprehensif dengan visualisasi real-time untuk monitoring performa bisnis pertanian Anda.")
    st.page_link("pages/8_📊_Dasbor_Terpadu.py", label="Buka Module", icon="📊", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("🚚 Rantai Pasok & Produk")
st.caption("Manajemen supply chain dan traceability produk")

col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("#### 🚚 Rantai Pasok Live")
    st.caption("Tracking real-time pergerakan produk dari farm to table dengan blockchain simulation dan carbon footprint.")
    st.page_link("pages/48_🚚_Rantai_Pasok_Live.py", label="Buka Module", icon="🚚", use_container_width=True)

with col5:
    st.markdown("#### 🏷️ Traceability Produk")
    st.caption("Generate QR code product passport, hash verification, dan consumer feedback loop untuk transparansi produk.")
    st.page_link("pages/49_🏷️_Traceability_Produk.py", label="Buka Module", icon="🏷️", use_container_width=True)

with col6:
    st.markdown("#### 🌾 Database Panen")
    st.caption("Database lengkap hasil panen dengan analisis produktivitas, kualitas, dan historical data.")
    st.page_link("pages/1_🌾_Database_Panen.py", label="Buka Module", icon="🌾", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

st.subheader("👥 Manajemen & SDM")
st.caption("Tools untuk manajemen tim dan pengembangan SDM")

col7, col8, col9 = st.columns(3)

with col7:
    st.markdown("#### 📢 Ruang Kerja PPL")
    st.caption("Workspace khusus untuk Penyuluh Pertanian Lapangan dengan tools perencanaan dan monitoring kegiatan.")
    st.page_link("pages/45_📢_Ruang_Kerja_PPL_Final.py", label="Buka Module", icon="📢", use_container_width=True)

with col8:
    st.markdown("#### 📋 Manajemen Proyek")
    st.caption("Project management tools untuk koordinasi tim, task tracking, dan timeline monitoring.")
    st.page_link("pages/50_📋_Manajemen_Proyek_Pertanian.py", label="Buka Module", icon="📋", use_container_width=True)

with col9:
    st.markdown("#### 🎓 Kurikulum Pelatihan")
    st.caption("Program pelatihan terstruktur untuk pengembangan kapasitas petani dan tim agribisnis.")
    st.page_link("pages/53_🎓_Kurikulum_Pelatihan.py", label="Buka Module", icon="🎓", use_container_width=True)

# Footer
st.markdown("---")
st.caption("💡 **Tip:** Gunakan sidebar untuk navigasi cepat antar module")

