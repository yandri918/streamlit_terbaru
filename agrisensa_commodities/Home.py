import streamlit as st

st.set_page_config(page_title="AgriSensa Commodities", page_icon="🌾", layout="wide")

st.markdown("""
<style>
    /* Modern Gradient Background */
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 50%, #bbf7d0 100%);
    }
    
    /* Premium Hero Section */
    .hero { 
        background: linear-gradient(135deg, #10b981 0%, #059669 50%, #047857 100%);
        padding: 3.5rem 2rem;
        border-radius: 1.5rem;
        color: white;
        text-align: center;
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.3);
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 15s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        position: relative;
        z-index: 1;
    }
    
    .hero p {
        font-size: 1.2rem;
        opacity: 0.95;
        position: relative;
        z-index: 1;
    }
    
    /* Section Header */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #047857;
        margin: 2rem 0 1.5rem 0;
        padding-left: 1rem;
        border-left: 5px solid #10b981;
    }
    
    /* Modern Glassmorphism Cards */
    .modern-card {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 1.2rem;
        padding: 2rem 1.5rem;
        margin-bottom: 1.5rem;
        border: 2px solid rgba(16, 185, 129, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        height: 100%;
        min-height: 180px;
    }
    
    .modern-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #10b981, #059669, #047857);
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.4s ease;
    }
    
    .modern-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(16, 185, 129, 0.25);
        border-color: rgba(16, 185, 129, 0.5);
    }
    
    .modern-card:hover::before {
        transform: scaleX(1);
    }
    
    .modern-card .icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.1));
    }
    
    .modern-card h3 {
        color: #047857;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        line-height: 1.3;
    }
    
    .modern-card p {
        color: #4b5563;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 0;
    }
    
    /* Compact Modern Cards for page_link modules */
    .compact-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 1rem;
        padding: 1.5rem;
        border: 2px solid rgba(16, 185, 129, 0.15);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
        height: 100%;
        min-height: 160px;
    }
    
    .compact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 32px rgba(16, 185, 129, 0.2);
        border-color: rgba(16, 185, 129, 0.4);
    }
    
    .compact-card .icon {
        font-size: 2.5rem;
        margin-bottom: 0.8rem;
        display: block;
    }
    
    .compact-card h4 {
        color: #047857;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .compact-card p {
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.5;
    }
    
    /* Hide default Streamlit elements */
    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 0.75rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4);
        transform: translateY(-2px);
    }
    
    /* Footer styling */
    .stAlert {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 1rem;
        border-left: 4px solid #10b981;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🌾 AgriSensa Commodities</h1><p>Panduan Spesifik Komoditas: Sayur, Buah, Padi, Sawit, & Jamur</p></div>', unsafe_allow_html=True)

st.markdown('<div class="section-header">📚 Modul Budidaya</div>', unsafe_allow_html=True)

# Row 1: Core 3 modules with modern cards
cols = st.columns(3)
with cols[0]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🥬</span>
        <h3>Sayuran</h3>
        <p>Panduan lengkap budidaya sayuran dataran rendah & tinggi dengan teknik modern.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Sayur", key="btn_sayur"): 
        st.switch_page("pages/21_Panduan_Budidaya_Sayuran.py")

with cols[1]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🍎</span>
        <h3>Buah-buahan</h3>
        <p>Teknik budidaya buah tropis dan subtropis untuk hasil maksimal.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Buah", key="btn_buah"): 
        st.switch_page("pages/23_Panduan_Budidaya_Buah.py")

with cols[2]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🌾</span>
        <h3>Padi</h3>
        <p>Kalkulator potensi panen padi dan teknik budidaya berbasis data.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Padi", key="btn_padi"): 
        st.switch_page("pages/25_Kalkulator_Potensi_Panen_Padi.py")

# Row 2: 4 modules with modern cards
cols2 = st.columns(4)
with cols2[0]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🌴</span>
        <h3>Kelapa Sawit</h3>
        <p>Manajemen perkebunan kelapa sawit live dengan monitoring real-time.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Sawit", key="btn_sawit"): 
        st.switch_page("pages/47_Manajemen_Sawit_Live.py")
    
with cols2[1]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🍄</span>
        <h3>Jamur</h3>
        <p>Budidaya jamur tiram dan kuping profesional dengan kontrol lingkungan.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Jamur", key="btn_jamur"): 
        st.switch_page("pages/51_Budidaya_Jamur_Profesional.py")

with cols2[2]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🦠</span>
        <h3>Mikroba & Biofertilizer</h3>
        <p>Produksi pupuk hayati & biocontrol untuk pertanian berkelanjutan.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Mikroba", key="btn_mikroba"): 
        st.switch_page("pages/52_Mikroba_Biofertilizer_Production.py")

with cols2[3]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🌿</span>
        <h3>Tanaman Obat & Herbal</h3>
        <p>High-value medicinal plants untuk pasar ekspor premium.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Herbal", key="btn_herbal"): 
        st.switch_page("pages/64_Tanaman_Obat_Herbal.py")

# Row 3: Additional modules
cols3 = st.columns(3)
with cols3[0]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🍵</span>
        <h3>Kalkulator Jamu Saintifik</h3>
        <p>Evidence-based traditional herbal medicine calculator berbasis riset.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Kalkulator Jamu", key="btn_jamu"): 
        st.switch_page("pages/65_Kalkulator_Jamu_Saintifik.py")

with cols3[1]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🥥</span>
        <h3>Kelapa & Produk Turunan</h3>
        <p>VCO, Gula Kelapa, Fiber, Peat, Charcoal - Diversifikasi produk kelapa.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Kelapa", key="btn_kelapa"): 
        st.switch_page("pages/67_Kelapa_Produk_Turunan.py")

with cols3[2]:
    st.markdown('''
    <div class="modern-card">
        <span class="icon">🌴</span>
        <h3>Budidaya Buah Luar Musim</h3>
        <p>Premium tropical fruits dengan teknik off-season cultivation.</p>
    </div>
    ''', unsafe_allow_html=True)
    if st.button("▶️ Buka Modul Buah Premium", key="btn_offseason"): 
        st.switch_page("pages/24_🌴_Budidaya_Buah_Luar_Musim.py")

st.markdown("---")
st.info("💡 Aplikasi ini adalah bagian dari ekosistem AgriSensa.")
