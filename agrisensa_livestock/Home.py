import streamlit as st

st.set_page_config(page_title="AgriSensa Livestock", page_icon="🐟", layout="wide")

st.markdown("""
<style>
    .hero { background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%); padding: 3rem; border-radius: 1rem; color: white; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🐟 AgriSensa Livestock</h1><p>Peternakan dan Perikanan Terintegrasi</p></div>', unsafe_allow_html=True)

st.info("Modul ini sedang dikembangkan lebih lanjut. Saat ini tersedia modul Peternakan & Perikanan dasar.")

if st.button("🐄 Buka Modul Peternakan & Perikanan"):
    st.switch_page("pages/42_🐄_Peternakan_Perikanan.py")
