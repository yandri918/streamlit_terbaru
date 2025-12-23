import streamlit as st
import os

st.set_page_config(page_title="AgriSensa Biz", page_icon="📈", layout="wide")

st.markdown("""
<style>
    .hero { background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); padding: 3rem; border-radius: 1rem; color: white; text-align: center; }
    .card { background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 1rem; border: 1px solid #e5e7eb; }
    .card h3 { color: #7c3aed; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>📈 AgriSensa Biz</h1><p>Keuangan, Rantai Pasok, dan Manajemen Agribisnis</p></div>', unsafe_allow_html=True)

st.markdown("### 💰 Analisis Keuangan")
c1, c2, c3 = st.columns(3)
with c1:
    st.page_link("pages/28_Analisis_Usaha_Tani.py", label="Analisis Usaha Tani", icon="💰", use_container_width=True)
with c2:
    st.page_link("pages/6_📈_Analisis_Tren_Harga.py", label="Analisis Tren Harga", icon="📈", use_container_width=True)
with c3:
    st.page_link("pages/8_📊_Dasbor_Terpadu.py", label="Dasbor Terpadu", icon="📊", use_container_width=True)

st.markdown("### 🚚 Rantai Pasok & Produk")
c4, c5 = st.columns(2)
with c4:
    st.page_link("pages/48_🚚_Rantai_Pasok_Live.py", label="Rantai Pasok Live", icon="🚚", use_container_width=True)
    st.page_link("pages/49_🏷️_Traceability_Produk.py", label="Traceability Produk", icon="🏷️", use_container_width=True)
with c5:
    st.page_link("pages/1_🌾_Database_Panen.py", label="Database Panen (Lengkap)", icon="🌾", use_container_width=True)
    st.page_link("pages/7_🎯_Prediksi_Hasil_Panen.py", label="Prediksi Hasil Panen", icon="🎯", use_container_width=True)

st.markdown("### 👥 Manajemen & SDM")
c6, c7 = st.columns(2)
with c6:
    st.page_link("pages/45_📢_Ruang_Kerja_PPL_Final.py", label="Ruang Kerja PPL", icon="📢", use_container_width=True)
    st.page_link("pages/50_📋_Manajemen_Proyek_Pertanian.py", label="Manajemen Proyek (Baru)", icon="📋", use_container_width=True)
with c7:
    st.page_link("pages/53_🎓_Kurikulum_Pelatihan.py", label="Kurikulum Pelatihan", icon="🎓", use_container_width=True)

# Footer
st.markdown("---")
# Debugging Section (Visible only to Admin/Dev)
with st.expander("🔧 Debug Page Paths (System Info)"):
    st.write("Current File:", __file__)
    st.write("CWD:", os.getcwd())
    
    try:
        from streamlit.source_util import get_pages
        pages = get_pages("Home.py")
        st.write("Registered Pages in Streamlit:", pages)
        
        st.write("Files in 'pages' directory:")
        if os.path.exists("pages"):
            st.write(sorted(os.listdir("pages")))
        else:
            st.error("'pages' directory not found!")
            
    except Exception as e:
        st.error(f"Error reading pages: {e}")
