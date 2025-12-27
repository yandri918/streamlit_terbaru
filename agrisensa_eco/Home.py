import streamlit as st

st.set_page_config(page_title="AgriSensa Eco", page_icon="♻️", layout="wide")

st.markdown("""
<style>
    .hero { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); padding: 3rem; border-radius: 1rem; color: white; text-align: center; }
    .card { background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 1rem; border: 1px solid #e5e7eb; }
    .card h3 { color: #d97706; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>♻️ AgriSensa Eco</h1><p>Keberlanjutan, Lingkungan, dan Konservasi</p></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.markdown("### 🌳 Konservasi & Agroforestri")
    if st.button("🌳 Pertanian Terpadu"): st.switch_page("pages/34_🌳_Pertanian_Terpadu.py")
    if st.button("🏞️ Konservasi Lahan"): st.switch_page("pages/35_🏞️_Konservasi_Lahan.py")
    if st.button("🌲 Agroforestri"): st.switch_page("pages/44_🌲_Agroforestri_V3.py")

with c2:
    st.markdown("### ♻️ Sampah & Organik")
    if st.button("♻️ Pengolahan Sampah"): st.switch_page("pages/54_♻️_Pengolahan_Sampah_Terpadu.py")
    if st.button("🧴 Pembuatan Pupuk Organik"): st.switch_page("pages/43_🧴_Pembuatan_Pupuk_Organik.py")

st.markdown("### 💰 Keberlanjutan & Sumber Daya")
c3, c4 = st.columns(2)
with c3:
    if st.button("💰 Carbon Credit Marketplace"): st.switch_page("pages/55_💰_Carbon_Credit.py")
with c4:
    if st.button("💧 Smart Water Management"): st.switch_page("pages/56_💧_Water_Management.py")

st.markdown("### 🌱 Toolkit Keberlanjutan")
if st.button("🌱 Sustainability Toolkit", use_container_width=True): 
    st.switch_page("pages/57_🌱_Sustainability_Toolkit.py")
st.caption("Regenerative Agriculture | Climate Adaptation | Circular Economy")

st.markdown("### 🌍 Advanced Sustainability")
if st.button("🌍 Advanced Sustainability Features", use_container_width=True):
    st.switch_page("pages/58_🌍_Advanced_Sustainability.py")
st.caption("Ecosystem Services | Precision Conservation | Indigenous Knowledge | ESG Reporting")

st.markdown("### 🌾 IPM, Seed & Landscape")
if st.button("🌾 IPM 2.0, Seed Saving & Landscape Planning", use_container_width=True):
    st.switch_page("pages/59_🌾_IPM_Seed_Landscape.py")
st.caption("AI Pest Identification | Seed Network | Farm Design")

st.markdown("### 🔄 Integrated Farming System")
if st.button("🔄 Sistem Pertanian Terpadu (Zero Waste)", use_container_width=True):
    st.switch_page("pages/60_🔄_Integrated_Farming_System.py")
st.caption("Simulator Maggot, Cacing, Kompos & Integrasi Ternak-Tani")

st.markdown("### 🥗 Crop Planning Optimizer")
if st.button("🥗 Rekomendasi Proporsi Tanaman", use_container_width=True):
    st.switch_page("pages/61_🥗_Crop_Planning_Optimizer.py")
st.caption("Optimasi Tanam Sayur: Hidroponik vs Tanah | Pribadi vs Pasar")

st.markdown("### 🍓 Agrowisata & Rekomendasi")
c5, c6 = st.columns(2)
with c5:
    if st.button("🍓 Agrowisata Petik"): st.switch_page("pages/52_🍓_Agrowisata_Petik_Langsung.py")
with c6:
    if st.button("🌱 Rekomendasi Tanaman"): st.switch_page("pages/9_🌱_Rekomendasi_Tanaman.py")