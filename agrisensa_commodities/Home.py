import streamlit as st

st.set_page_config(page_title="AgriSensa Commodities", page_icon="🌾", layout="wide")

st.markdown("""
<style>
    .hero { background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 3rem; border-radius: 1rem; color: white; text-align: center; }
    .card { background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 1rem; border: 1px solid #e5e7eb; }
    .card h3 { color: #059669; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🌾 AgriSensa Commodities</h1><p>Panduan Spesifik Komoditas: Sayur, Buah, Padi, Sawit, & Jamur</p></div>', unsafe_allow_html=True)

st.markdown("### 📚 Modul Budidaya")

cols = st.columns(3)
with cols[0]:
    st.markdown('<div class="card"><h3>🥬 Sayuran</h3><p>Panduan lengkap budidaya sayuran dataran rendah & tinggi.</p></div>', unsafe_allow_html=True)
    if st.button("Buka Modul Sayur"): st.switch_page("pages/21_🥬_Panduan_Budidaya_Sayuran.py")

with cols[1]:
    st.markdown('<div class="card"><h3>🍎 Buah-buahan</h3><p>Teknik budidaya buah tropis dan subtropis.</p></div>', unsafe_allow_html=True)
    if st.button("Buka Modul Buah"): st.switch_page("pages/23_🍎_Panduan_Budidaya_Buah.py")

with cols[2]:
    st.markdown('<div class="card"><h3>🌾 Padi</h3><p>Kalkulator potensi panen padi dan teknik budidaya.</p></div>', unsafe_allow_html=True)
    if st.button("Buka Modul Padi"): st.switch_page("pages/24_🌾_Kalkulator_Potensi_Panen_Padi.py")

cols2 = st.columns(3)
with cols2[0]:
    st.markdown('<div class="card"><h3>🌴 Kelapa Sawit</h3><p>Manajemen perkebunan kelapa sawit live.</p></div>', unsafe_allow_html=True)
    if st.button("Buka Modul Sawit"): st.switch_page("pages/47_🌴_Manajemen_Sawit_Live.py")
    
with cols2[1]:
    st.markdown('<div class="card"><h3>🍄 Jamur</h3><p>Budidaya jamur tiram dan kuping profesional.</p></div>', unsafe_allow_html=True)
    if st.button("Buka Modul Jamur"): st.switch_page("pages/51_Budidaya_Jamur_Profesional.py")

with cols2[2]: # Updated content for Mikroba & Biofertilizer
    with st.container():
        st.markdown("**🦠 Mikroba & Biofertilizer**")
        st.caption("Produksi pupuk hayati & biocontrol")
        st.page_link("pages/52_Mikroba_Biofertilizer_Production.py", label="Buka Module", icon="▶️", use_container_width=True)

with cols2[3]: # New module for Tanaman Obat & Herbal
    with st.container():
        st.markdown("**🌿 Tanaman Obat & Herbal**")
        st.caption("High-value medicinal plants - Export market")
        st.page_link("pages/64_Tanaman_Obat_Herbal.py", label="Buka Module", icon="▶️", use_container_width=True)

# Row 3: New modules
cols3 = st.columns(3)
with cols3[0]:
    with st.container():
        st.markdown("**🍵 Kalkulator Jamu Saintifik**")
        st.caption("Evidence-based traditional herbal medicine calculator")
        st.page_link("pages/65_Kalkulator_Jamu_Saintifik.py", label="Buka Module", icon="▶️", use_container_width=True)

st.markdown("---")
st.info("💡 Aplikasi ini adalah bagian dari ekosistem AgriSensa.")
