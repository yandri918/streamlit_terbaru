import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Data Analyst Portfolio | Professional Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with Glassmorphism, Animations, and Premium Design
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@600;700;800&display=swap');
    
    /* Import Font Awesome */
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css');
    
    /* CSS Variables for Theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --glass-border: rgba(255, 255, 255, 0.2);
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
        --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
        --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.15);
        --shadow-xl: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Global Styles */
    .main {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Premium Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 4rem 2rem;
        border-radius: 24px;
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
        box-shadow: var(--shadow-xl);
        animation: fadeInUp 0.8s ease-out;
    }
    
    .hero-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 20s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    .hero-content {
        position: relative;
        z-index: 1;
        text-align: center;
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(to right, #ffffff, #e0e7ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: slideInDown 0.8s ease-out;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        color: rgba(255, 255, 255, 0.95);
        margin-top: 1rem;
        font-weight: 500;
        animation: fadeIn 1s ease-out 0.3s both;
    }
    
    .hero-icon {
        font-size: 4rem;
        color: #fbbf24;
        margin-bottom: 1rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    /* Icon Styling */
    .fas, .far, .fab {
        margin-right: 0.5rem;
    }
    
    /* Skill Badges */
    .skill-badge {
        display: inline-block;
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.25rem;
        font-weight: 600;
        font-size: 0.9rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }
    
    .skill-badge:hover {
        transform: translateY(-2px);
        background: rgba(255, 255, 255, 0.3);
    }
    
    /* Glassmorphic Project Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: var(--shadow-md);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 100%;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--primary-gradient);
        transform: scaleX(0);
        transition: transform 0.3s ease;
        border-radius: 20px 20px 0 0;
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 48px rgba(0, 0, 0, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    .glass-card:hover::before {
        transform: scaleX(1);
    }
    
    .glass-card h3 {
        color: #667eea;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .glass-card h3 i {
        font-size: 1.75rem;
    }
    
    .glass-card p {
        color: #334155;
        line-height: 1.6;
        margin: 0.75rem 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9) 0%, rgba(118, 75, 162, 0.9) 100%);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: var(--shadow-md);
        transition: all 0.3s ease;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: var(--shadow-lg);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* Section Headers */
    .section-header {
        text-align: center;
        margin: 3rem 0 2rem 0;
        position: relative;
    }
    
    .section-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .section-title i {
        margin-right: 0.75rem;
    }
    
    .section-divider {
        width: 80px;
        height: 4px;
        background: var(--primary-gradient);
        margin: 1rem auto;
        border-radius: 2px;
        animation: expandWidth 0.8s ease-out;
    }
    
    @keyframes expandWidth {
        from { width: 0; }
        to { width: 80px; }
    }
    
    /* Contact Cards */
    .contact-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow-sm);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        text-align: center;
    }
    
    .contact-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
        border-color: #667eea;
    }
    
    .contact-card i {
        font-size: 2rem;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    /* Footer */
    .custom-footer {
        text-align: center;
        padding: 2rem 0;
        margin-top: 4rem;
        border-top: 2px solid transparent;
        border-image: var(--primary-gradient) 1;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
        }
        
        .section-title {
            font-size: 1.8rem;
        }
        
        .glass-card {
            padding: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-content">
        <div class="hero-icon"><i class="fas fa-chart-line"></i></div>
        <h1 class="hero-title">Data Analyst Portfolio</h1>
        <p class="hero-subtitle">
            Transforming Data into Actionable Insights
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Introduction Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title"><i class="fas fa-user-circle"></i> Selamat Datang</h2>
        <div class="section-divider"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Saya adalah seorang **Data Analyst** yang berfokus pada analisis data, visualisasi, 
    dan pengembangan insights berbasis data untuk mendukung pengambilan keputusan bisnis.
    
    Portfolio ini menampilkan beberapa proyek analisis data yang telah saya kerjakan, 
    menggunakan berbagai teknik analisis statistik, machine learning, dan visualisasi data interaktif.
    """)
    
    st.markdown("### <i class='fas fa-star'></i> Keahlian Utama", unsafe_allow_html=True)
    st.markdown("""
    <div>
        <span class="skill-badge">Python</span>
        <span class="skill-badge">Pandas</span>
        <span class="skill-badge">NumPy</span>
        <span class="skill-badge">Scikit-learn</span>
        <span class="skill-badge">Altair</span>
        <span class="skill-badge">Streamlit</span>
        <span class="skill-badge">SQL</span>
        <span class="skill-badge">Statistical Analysis</span>
        <span class="skill-badge">Machine Learning</span>
        <span class="skill-badge">Data Visualization</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <p class="metric-value">4</p>
        <p class="metric-label">Featured Projects</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="metric-card" style="margin-top: 1rem;">
        <p class="metric-value">5+</p>
        <p class="metric-label">Technologies Used</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Projects Overview
st.markdown("""
<div class="section-header">
    <h2 class="section-title"><i class="fas fa-briefcase"></i> Featured Projects</h2>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-chart-line" style="color: #10b981;"></i> Stock Price Analysis</h3>
        <p>Analisis mendalam terhadap data harga saham dengan visualisasi interaktif, 
        termasuk candlestick charts, moving averages, dan analisis volatilitas.</p>
        <p><strong><i class="fas fa-tools"></i> Teknologi:</strong> Python, Pandas, Altair, Statistical Analysis</p>
        <p><strong><i class="fas fa-database"></i> Dataset:</strong> 1,500+ data points</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-shield-alt" style="color: #ef4444;"></i> Credit Card Fraud</h3>
        <p>Analisis pola fraud pada transaksi kartu kredit menggunakan teknik machine learning 
        dan visualisasi untuk mengidentifikasi anomali.</p>
        <p><strong><i class="fas fa-tools"></i> Teknologi:</strong> Python, Scikit-learn, PCA, Altair</p>
        <p><strong><i class="fas fa-database"></i> Dataset:</strong> 284,000+ transactions</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-coins" style="color: #f59e0b;"></i> Gold Price Analysis</h3>
        <p>Analisis tren harga emas dengan prediksi dan visualisasi pola historis untuk 
        mendukung keputusan investasi.</p>
        <p><strong><i class="fas fa-tools"></i> Teknologi:</strong> Python, Pandas, Time Series Analysis</p>
        <p><strong><i class="fas fa-database"></i> Dataset:</strong> Historical gold prices</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-vote-yea" style="color: #667eea;"></i> Survey Sampling & Election Polling</h3>
        <p>Kalkulator profesional untuk survey sampling, termasuk sample size calculation, 
        margin of error, confidence intervals, dan statistical significance testing untuk polling pemilu.</p>
        <p><strong><i class="fas fa-tools"></i> Teknologi:</strong> Python, SciPy, Plotly, Statistical Inference</p>
        <p><strong><i class="fas fa-calculator"></i> Features:</strong> Sample size, MoE, CI, significance tests</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Contact Section
st.markdown("""
<div class="section-header">
    <h2 class="section-title"><i class="fas fa-envelope"></i> Kontak & Informasi</h2>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="contact-card">
        <i class="fab fa-github"></i>
        <p><strong>GitHub</strong></p>
        <p><a href="https://github.com/yandri918/data" target="_blank">github.com/yandri918/data</a></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="contact-card">
        <i class="fas fa-envelope"></i>
        <p><strong>Email</strong></p>
        <p>Contact via GitHub</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="contact-card">
        <i class="fab fa-linkedin"></i>
        <p><strong>LinkedIn</strong></p>
        <p>Connect on LinkedIn</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
<div class="custom-footer">
    <p style="margin: 0; font-weight: 600;">
        Built with <i class="fas fa-heart" style="color: #ef4444;"></i> using Streamlit & Altair
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem;">
        © 2026 Data Analyst Portfolio | All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### <i class='fas fa-compass'></i> Navigation", unsafe_allow_html=True)
    st.info("👈 Pilih halaman di atas untuk melihat proyek analisis data")
    
    st.markdown("---")
    
    st.markdown("### <i class='fas fa-tachometer-alt'></i> Quick Stats", unsafe_allow_html=True)
    st.metric("Total Projects", "4")
    st.metric("Total Data Points", "285K+")
    st.metric("Visualization Types", "20+")
    
    st.markdown("---")
    
    st.markdown("### <i class='fas fa-tools'></i> Tech Stack", unsafe_allow_html=True)
    st.markdown("""
    - **Languages:** Python
    - **Libraries:** Pandas, NumPy, Scikit-learn
    - **Visualization:** Altair, Streamlit
    - **Analysis:** Statistical Methods, ML
    """)
