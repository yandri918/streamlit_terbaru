import streamlit as st

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
    if st.button("💰 Analisis Usaha Tani"): st.switch_page("pages/28_💰_Analisis_Usaha_Tani.py")
with c2:
    if st.button("📈 Analisis Tren Harga"): st.switch_page("pages/6_📈_Analisis_Tren_Harga.py")
with c3:
    if st.button("📊 Dasbor Terpadu"): st.switch_page("pages/8_📊_Dasbor_Terpadu.py")

st.markdown("### 🚚 Rantai Pasok & Produk")
c4, c5 = st.columns(2)
with c4:
    if st.button("🚚 Rantai Pasok Live"): st.switch_page("pages/48_🚚_Rantai_Pasok_Live.py")
    if st.button("🏷️ Traceability Produk"): st.switch_page("pages/49_🏷️_Traceability_Produk.py")
with c5:
    if st.button("🌾 Database Panen (Lengkap)"): st.switch_page("pages/1_🌾_Database_Panen.py")
    if st.button("🎯 Prediksi Hasil Panen"): st.switch_page("pages/7_🎯_Prediksi_Hasil_Panen.py")

st.markdown("### 👥 Manajemen & SDM")
c6, c7 = st.columns(2)
with c6:
    if st.button("📢 Ruang Kerja PPL"): st.switch_page("pages/45_📢_Ruang_Kerja_PPL_Final.py")
    if st.button("📋 Manajemen Proyek (Baru)"): st.switch_page("pages/50_📋_Manajemen_Proyek_Pertanian.py")
with c7:
    if st.button("🎓 Kurikulum Pelatihan"): st.switch_page("pages/53_🎓_Kurikulum_Pelatihan.py")
