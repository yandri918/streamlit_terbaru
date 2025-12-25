import streamlit as st

st.set_page_config(page_title="AgriSensa Biz", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .hero { 
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); 
        padding: 3rem; 
        border-radius: 1rem; 
        color: white; 
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #7c3aed;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e5e7eb;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>📈 AgriSensa Biz</h1><p>Platform Manajemen Keuangan, Rantai Pasok, dan Agribisnis Terpadu</p></div>', unsafe_allow_html=True)

# Analisis Keuangan
st.markdown('<div class="section-header">💰 Analisis Keuangan</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    with st.container():
        st.markdown("**💰 Analisis Usaha Tani**")
        st.caption("Hitung RAB, proyeksi laba, dan break-even analysis")
        st.page_link("pages/28_Analisis_Usaha_Tani.py", label="Buka Module", icon="▶️", use_container_width=True)

with c2:
    with st.container():
        st.markdown("**📈 Analisis Tren Harga**")
        st.caption("Pantau tren harga dan volatilitas komoditas")
        st.page_link("pages/6_📈_Analisis_Tren_Harga.py", label="Buka Module", icon="▶️", use_container_width=True)

with c3:
    with st.container():
        st.markdown("**📊 Dasbor Terpadu**")
        st.caption("Dashboard monitoring performa bisnis real-time")
        st.page_link("pages/8_📊_Dasbor_Terpadu.py", label="Buka Module", icon="▶️", use_container_width=True)

# Rantai Pasok & Produk
st.markdown('<div class="section-header">🚚 Rantai Pasok & Produk</div>', unsafe_allow_html=True)
c4, c5, c6, c7 = st.columns(4)

with c4:
    with st.container():
        st.markdown("**🚚 Rantai Pasok Live**")
        st.caption("Tracking produk farm to table")
        st.page_link("pages/48_🚚_Rantai_Pasok_Live.py", label="Buka Module", icon="▶️", use_container_width=True)

with c5:
    with st.container():
        st.markdown("**🏷️ Traceability Produk**")
        st.caption("QR code & product passport")
        st.page_link("pages/49_🏷️_Traceability_Produk.py", label="Buka Module", icon="▶️", use_container_width=True)

with c6:
    with st.container():
        st.markdown("**🌾 Database Panen**")
        st.caption("Data hasil panen lengkap")
        st.page_link("pages/1_🌾_Database_Panen.py", label="Buka Module", icon="▶️", use_container_width=True)

with c7:
    with st.container():
        st.markdown("**🎯 Prediksi Hasil Panen**")
        st.caption("AI-powered yield prediction")
        st.page_link("pages/7_🎯_Prediksi_Hasil_Panen.py", label="Buka Module", icon="▶️", use_container_width=True)

# Manajemen & SDM
st.markdown('<div class="section-header">👥 Manajemen & SDM</div>', unsafe_allow_html=True)
c8, c9, c10 = st.columns(3)

with c8:
    with st.container():
        st.markdown("**📢 Ruang Kerja PPL**")
        st.caption("Workspace untuk Penyuluh Pertanian Lapangan")
        st.page_link("pages/45_📢_Ruang_Kerja_PPL_Final.py", label="Buka Module", icon="▶️", use_container_width=True)

with c9:
    with st.container():
        st.markdown("**📋 Manajemen Proyek**")
        st.caption("Project management & task tracking")
        st.page_link("pages/50_📋_Manajemen_Proyek_Pertanian.py", label="Buka Module", icon="▶️", use_container_width=True)

with c10:
    with st.container():
        st.markdown("**🎓 Kurikulum Pelatihan**")
        st.caption("Program pelatihan terstruktur")
        st.page_link("pages/53_🎓_Kurikulum_Pelatihan.py", label="Buka Module", icon="▶️", use_container_width=True)

# Footer
st.markdown("---")
st.caption("💡 **Tip:** Gunakan sidebar untuk navigasi cepat antar module")
