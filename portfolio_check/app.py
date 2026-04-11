import streamlit as st

# Page Config
st.set_page_config(
    page_title="Andriyanto - AgriTech Developer",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Hero Section */
    .hero-container {
        text-align: center;
        padding: 60px 20px;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(59, 130, 246, 0.1) 100%);
        border-radius: 30px;
        margin-bottom: 40px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #10b981 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: #94a3b8;
        margin-bottom: 20px;
    }
    
    .hero-tagline {
        font-size: 1.1rem;
        color: #64748b;
        max-width: 700px;
        margin: 0 auto 30px;
        line-height: 1.8;
    }
    
    /* Stat Card */
    .stat-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(16, 185, 129, 0.2);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #10b981;
    }
    
    .stat-label {
        color: #94a3b8;
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* Skill Badge */
    .skill-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(59, 130, 246, 0.2) 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10b981;
        padding: 8px 20px;
        border-radius: 25px;
        margin: 5px;
        font-weight: 500;
    }
    
    /* Project Card */
    .project-card {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(6, 78, 59, 0.2) 100%);
        border: 2px solid #10b981;
        border-radius: 25px;
        padding: 40px;
        margin: 20px 0;
    }
    
    .project-title {
        font-size: 2rem;
        font-weight: 700;
        color: #10b981;
        margin-bottom: 15px;
    }
    
    .project-desc {
        color: #cbd5e1;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    
    /* Partner Card */
    .partner-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        height: 100%;
    }
    
    .partner-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .partner-name {
        color: #e2e8f0;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .partner-role {
        color: #64748b;
        font-size: 0.85rem;
    }
    
    /* Section Title */
    .section-title {
        font-size: 2rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .section-subtitle {
        color: #64748b;
        text-align: center;
        margin-bottom: 40px;
    }
    
    /* CTA Button */
    .cta-button {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important;
        padding: 15px 40px;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
        margin: 10px;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    
    .cta-button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 30px rgba(16, 185, 129, 0.4);
    }
    
    .cta-secondary {
        background: transparent;
        border: 2px solid #10b981;
        color: #10b981 !important;
    }
    
    /* Contact Card */
    .contact-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
    }
    
    .contact-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    
    .contact-label {
        color: #64748b;
        font-size: 0.85rem;
    }
    
    .contact-value {
        color: #10b981;
        font-weight: 600;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 40px;
        color: #64748b;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin-top: 60px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ============================================
# HERO SECTION
# ============================================
st.markdown("""
<div class="hero-container">
    <div style="font-size: 5rem; margin-bottom: 20px;">🌾</div>
    <h1 class="hero-title">Andriyanto</h1>
    <p class="hero-subtitle">AgriTech Developer & Agronomist</p>
    <p class="hero-tagline">
        Membangun masa depan pertanian Indonesia melalui teknologi. 
        Menggabungkan keahlian agronomi dengan full-stack development 
        untuk menciptakan solusi precision agriculture yang berdampak nyata.
    </p>
    <div style="margin-top: 30px;">
        <a href="https://agrisensa-app.streamlit.app/" target="_blank" class="cta-button">🚀 Lihat AgriSensa</a>
        <a href="https://github.com/yandri918" target="_blank" class="cta-button cta-secondary">💻 GitHub</a>
        <a href="https://www.linkedin.com/in/andriyanto-na-147492157" target="_blank" class="cta-button cta-secondary">🔗 LinkedIn</a>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# STATS
# ============================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">50+</div>
        <div class="stat-label">Modul AgriSensa</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">4+</div>
        <div class="stat-label">Partner Kolaborasi</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">5+</div>
        <div class="stat-label">Tahun Experience</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="stat-card">
        <div class="stat-number">🇯🇵</div>
        <div class="stat-label">Japan Experience</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================
# ABOUT ME
# ============================================
st.markdown("""
<h2 class="section-title">🧑‍💻 Tentang Saya</h2>
<p class="section-subtitle">Intersection of Agriculture & Technology</p>
""", unsafe_allow_html=True)

about_col1, about_col2 = st.columns([1, 1])

with about_col1:
    st.markdown("""
    ### 🌱 Background
    
    Saya adalah seorang **Agronomist** dengan latar belakang teknis yang kuat. 
    Pengalaman bekerja di **Jepang** memberikan perspektif unik tentang bagaimana 
    teknologi dan disiplin dapat mentransformasi sektor pertanian.
    
    ### 🎯 Misi
    
    Membangun **ekosistem digital pertanian Indonesia** yang terintegrasi - 
    dari sensor di lapangan hingga QR code di kemasan konsumen. AgriSensa 
    adalah manifestasi visi ini.
    """)

with about_col2:
    st.markdown("""
    ### 💡 Approach
    
    Saya percaya bahwa **teknologi harus melayani pengguna**, bukan sebaliknya. 
    Setiap modul di AgriSensa dibangun berdasarkan kebutuhan nyata petani Indonesia.
    
    ### 🌍 Vision
    
    Menjadikan pertanian Indonesia lebih **produktif**, **sustainable**, dan 
    **traceable** melalui digitalisasi end-to-end yang accessible untuk semua skala usaha.
    """)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================
# SKILLS
# ============================================
st.markdown("""
<h2 class="section-title">⚡ Tech Stack & Skills</h2>
<p class="section-subtitle">Kombinasi unik antara domain expertise dan technical capability</p>
""", unsafe_allow_html=True)

skill_col1, skill_col2, skill_col3 = st.columns(3)

with skill_col1:
    st.markdown("""
    ### 💻 Development
    <span class="skill-badge">Python</span>
    <span class="skill-badge">Flask</span>
    <span class="skill-badge">Streamlit</span>
    <span class="skill-badge">JavaScript</span>
    <span class="skill-badge">HTML/CSS</span>
    <span class="skill-badge">SQLAlchemy</span>
    <span class="skill-badge">Git</span>
    """, unsafe_allow_html=True)

with skill_col2:
    st.markdown("""
    ### 📊 Data & Analytics
    <span class="skill-badge">Pandas</span>
    <span class="skill-badge">Plotly</span>
    <span class="skill-badge">Data Visualization</span>
    <span class="skill-badge">GIS Mapping</span>
    <span class="skill-badge">IoT Integration</span>
    <span class="skill-badge">AI/ML Basics</span>
    """, unsafe_allow_html=True)

with skill_col3:
    st.markdown("""
    ### 🌾 Agriculture
    <span class="skill-badge">Agronomi</span>
    <span class="skill-badge">Nutrisi Tanaman</span>
    <span class="skill-badge">Hidroponik</span>
    <span class="skill-badge">Waste Management</span>
    <span class="skill-badge">Supply Chain</span>
    <span class="skill-badge">Quality Control</span>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================
# FEATURED PROJECT - AGRISENSA
# ============================================
st.markdown("""
<h2 class="section-title">🚀 Featured Project</h2>
<p class="section-subtitle">Flagship project yang mendemonstrasikan kemampuan end-to-end</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="project-card">
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <span style="font-size: 3rem; margin-right: 20px;">🌾</span>
        <div>
            <h2 class="project-title" style="margin: 0;">AgriSensa</h2>
            <p style="color: #94a3b8; margin: 0;">Precision Agriculture Platform</p>
        </div>
    </div>
    <p class="project-desc">
        Platform pertanian terintegrasi dengan <strong>50+ modul</strong> yang mencakup seluruh 
        siklus pertanian - dari perencanaan, budidaya, monitoring, hingga traceability produk. 
        Dibangun dengan pendekatan <strong>full-stack</strong> menggunakan Python, Flask, dan Streamlit.
    </p>
</div>
""", unsafe_allow_html=True)

# AgriSensa Features
feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)

with feat_col1:
    st.markdown("""
    #### 📊 Dashboard & Analytics
    - Real-time KPI monitoring
    - Interactive visualizations
    - Predictive analytics
    """)

with feat_col2:
    st.markdown("""
    #### 🌱 Smart Farming
    - Rekomendasi tanaman AI
    - Kalkulator pupuk presisi
    - Monitoring pertumbuhan
    """)

with feat_col3:
    st.markdown("""
    #### ♻️ Waste-to-Value
    - Pengolahan sampah organik
    - Sistem grading pupuk
    - Carbon offset tracking
    """)

with feat_col4:
    st.markdown("""
    #### 📱 Traceability
    - QR Code product passport
    - Supply chain tracking
    - Consumer verification
    """)

st.markdown("<br>", unsafe_allow_html=True)

# CTA to AgriSensa
st.markdown("""
<div style="text-align: center; margin: 20px 0;">
    <a href="https://agrisensa-app.streamlit.app/" target="_blank" class="cta-button">
        🌐 Explore AgriSensa Live Demo
    </a>
</div>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================
# PARTNERS & COLLABORATIONS
# ============================================
st.markdown("""
<h2 class="section-title">🤝 Partners & Collaborations</h2>
<p class="section-subtitle">Kolaborasi nyata dengan berbagai stakeholder pertanian</p>
""", unsafe_allow_html=True)

partner_col1, partner_col2, partner_col3, partner_col4 = st.columns(4)

with partner_col1:
    st.markdown("""
    <div class="partner-card">
        <div class="partner-icon">♻️</div>
        <div class="partner-name">Bank Sampah</div>
        <div class="partner-role">Waste-to-Value Partner</div>
    </div>
    """, unsafe_allow_html=True)

with partner_col2:
    st.markdown("""
    <div class="partner-card">
        <div class="partner-icon">👨‍🌾</div>
        <div class="partner-name">Kelompok Tani Wonogiri</div>
        <div class="partner-role">Farming Community</div>
    </div>
    """, unsafe_allow_html=True)

with partner_col3:
    st.markdown("""
    <div class="partner-card">
        <div class="partner-icon">🌳</div>
        <div class="partner-name">Perhutani</div>
        <div class="partner-role">Forestry Collaboration</div>
    </div>
    """, unsafe_allow_html=True)

with partner_col4:
    st.markdown("""
    <div class="partner-card">
        <div class="partner-icon">🌾</div>
        <div class="partner-name">Teman Petani</div>
        <div class="partner-role">Upcoming Partner</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# ============================================
# CONTACT
# ============================================
st.markdown("""
<h2 class="section-title">📬 Get In Touch</h2>
<p class="section-subtitle">Tertarik berkolaborasi? Mari berdiskusi!</p>
""", unsafe_allow_html=True)

contact_col1, contact_col2, contact_col3 = st.columns(3)

with contact_col1:
    st.markdown("""
    <div class="contact-card">
        <div class="contact-icon">📧</div>
        <div class="contact-label">Email</div>
        <div class="contact-value">yandri918@gmail.com</div>
    </div>
    """, unsafe_allow_html=True)

with contact_col2:
    st.markdown("""
    <div class="contact-card">
        <div class="contact-icon">🔗</div>
        <div class="contact-label">LinkedIn</div>
        <div class="contact-value">andriyanto-na</div>
    </div>
    """, unsafe_allow_html=True)

with contact_col3:
    st.markdown("""
    <div class="contact-card">
        <div class="contact-icon">💻</div>
        <div class="contact-label">GitHub</div>
        <div class="contact-value">yandri918</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown("""
<div class="footer">
    <p>© 2024 Andriyanto. Built with ❤️ and 🌾</p>
    <p style="font-size: 0.85rem;">Powered by Streamlit | Deployed on Vercel</p>
</div>
""", unsafe_allow_html=True)
