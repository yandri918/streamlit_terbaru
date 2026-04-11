"""
Weather Prediction Portfolio
Professional weather forecasting application using Open-Meteo API and Folium maps
"""
import streamlit as st
import sys
import os

# Add utils to path
sys.path.append(os.path.dirname(__file__))

# Page configuration
st.set_page_config(
    page_title="Weather Prediction Portfolio | Professional Forecasting",
    page_icon="🌤️",
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
        --primary-gradient: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
        --secondary-gradient: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        --success-gradient: linear-gradient(135deg, #10b981 0%, #059669 100%);
        --warning-gradient: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
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
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%);
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
        background: linear-gradient(to right, #ffffff, #e0f2fe);
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
    
    /* Icon Styling */
    .fas, .far, .fab {
        margin-right: 0.5rem;
    }
    
    .hero-icon {
        font-size: 4rem;
        color: #fbbf24;
        margin-bottom: 1rem;
        animation: bounce 2s ease-in-out infinite;
    }
    
    /* Glassmorphic Feature Cards */
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
        color: #1e40af;
        font-size: 1.5rem;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .glass-card h3 i {
        font-size: 1.75rem;
        color: #3b82f6;
    }
    
    .glass-card p {
        color: #334155;
        line-height: 1.6;
        margin: 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(135deg, rgba(59, 130, 246, 0.9) 0%, rgba(30, 64, 175, 0.9) 100%);
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
    
    /* How to Use Section */
    .steps-container {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 2rem;
        border-radius: 16px;
        border-left: 4px solid #3b82f6;
        margin: 2rem 0;
        box-shadow: var(--shadow-sm);
    }
    
    .steps-container ol {
        margin: 1rem 0;
        padding-left: 1.5rem;
    }
    
    .steps-container li {
        margin: 0.75rem 0;
        color: #1e293b;
        font-weight: 500;
    }
    
    /* Tech Stack Cards */
    .tech-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: var(--shadow-sm);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .tech-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-md);
        border-color: #3b82f6;
    }
    
    .tech-card h4 {
        color: #1e40af;
        margin-bottom: 1rem;
        font-size: 1.25rem;
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
        <div class="hero-icon"><i class="fas fa-cloud-sun"></i></div>
        <h1 class="hero-title">Weather Prediction Portfolio</h1>
        <p class="hero-subtitle">
            Professional Weather Forecasting with Interactive Maps & Real-time Data
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
<div class="section-header">
    <h2 class="section-title"><i class="fas fa-info-circle"></i> Welcome</h2>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
This portfolio showcases advanced weather prediction capabilities using:
- **Open-Meteo API** for accurate, real-time weather data
- **Folium Maps** for interactive location selection
- **Advanced Visualizations** with Altair and Plotly
- **Comprehensive Forecasts** from hourly to weekly predictions
""")

st.markdown("---")

# Features Overview
st.markdown("""
<div class="section-header">
    <h2 class="section-title"><i class="fas fa-star"></i> Features</h2>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-map-marked-alt"></i> Interactive Maps</h3>
        <p>Click anywhere on the map to get instant weather data. Search cities or select from popular locations.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-cloud-sun"></i> Real-time Weather</h3>
        <p>Current conditions including temperature, humidity, wind, pressure, and more.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-calendar-alt"></i> Forecasts</h3>
        <p>7-day daily forecasts and 48-hour hourly predictions with detailed metrics.</p>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-chart-line"></i> Analysis</h3>
        <p>Historical weather data analysis with trends and patterns visualization.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-globe-americas"></i> Multi-City</h3>
        <p>Compare weather across multiple cities simultaneously.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <h3><i class="fas fa-chart-area"></i> Visualizations</h3>
        <p>Beautiful charts and graphs for temperature, precipitation, and wind data.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick Stats
st.markdown("""
<div class="section-header">
    <h2 class="section-title"><i class="fas fa-tachometer-alt"></i> Quick Stats</h2>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">100%</div>
        <div class="metric-label">Free API</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">16 Days</div>
        <div class="metric-label">Forecast Range</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">Global</div>
        <div class="metric-label">Coverage</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-value">Real-time</div>
        <div class="metric-label">Updates</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# How to Use
st.markdown("""
<div class="section-header">
    <h2 class="section-title"><i class="fas fa-rocket"></i> How to Use</h2>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="steps-container">
    <ol>
        <li><strong>Navigate</strong> to any page using the sidebar</li>
        <li><strong>Select Location</strong> on the Interactive Map page</li>
        <li><strong>View Weather</strong> data and forecasts</li>
        <li><strong>Analyze</strong> historical trends</li>
        <li><strong>Compare</strong> multiple cities</li>
    </ol>
    <p style="margin-top: 1.5rem; font-weight: 600; color: #1e40af;">
        <i class="fas fa-arrow-left"></i> Start by selecting a page from the sidebar!
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Technology Stack
st.markdown("""
<div class="section-header">
    <h2 class="section-title"><i class="fas fa-tools"></i> Technology Stack</h2>
    <div class="section-divider"></div>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="tech-card">
        <h4><i class="fas fa-database"></i> Data & APIs</h4>
        <ul>
            <li>Open-Meteo API (Weather Data)</li>
            <li>Geocoding API (Location Search)</li>
            <li>Pandas (Data Processing)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tech-card">
        <h4><i class="fas fa-chart-pie"></i> Visualization</h4>
        <ul>
            <li>Folium (Interactive Maps)</li>
            <li>Altair (Statistical Charts)</li>
            <li>Plotly (Interactive Graphs)</li>
            <li>Streamlit (Web Framework)</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Footer
st.markdown("""
<div class="custom-footer">
    <p style="margin: 0; font-weight: 600;">
        Built with <i class="fas fa-heart" style="color: #ef4444;"></i> using Streamlit, Folium, and Open-Meteo API
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem;">
        © 2026 Weather Prediction Portfolio | All Rights Reserved
    </p>
</div>
""", unsafe_allow_html=True)
