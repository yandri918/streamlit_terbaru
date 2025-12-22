import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="AgriSensa Academy - Kurikulum Pelatihan",
    page_icon="🎓",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Custom Glassmorphic CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }
    .course-title {
        color: #065f46;
        font-weight: 800;
        font-size: 1.5rem;
        margin-bottom: 10px;
    }
    .price-tag {
        background-color: #10b981;
        color: white;
        padding: 5px 15px;
        border-radius: 50px;
        font-weight: 700;
        font-size: 0.9rem;
    }
    .level-badge {
        font-size: 0.8rem;
        padding: 3px 10px;
        border-radius: 5px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .silver { background: #e5e7eb; color: #4b5563; }
    .gold { background: #fef3c7; color: #92400e; }
    .platinum { background: #dbeafe; color: #1e40af; }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div style="text-align: center; padding: 40px 0;">
    <h1 style="font-size: 3rem; font-weight: 900; color: #065f46; margin-bottom: 0;">🎓 AgriSensa Academy</h1>
    <p style="font-size: 1.2rem; color: #047857; font-weight: 500;">Mastering High-Value Agriculture through Precision & Experience Economy</p>
</div>
""", unsafe_allow_html=True)

# Navigation Tabs
tabs = st.tabs(["📚 Kurikulum Utama", "💰 Strategi Komersialisasi", "📽️ Video Course Map", "🏫 Workshop Offline"])

# --- TAB 1: KURIKULUM UTAMA ---
with tabs[0]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🎯 Learning Tracks & Roadmaps")
    st.write("Kurikulum berbasis kompetensi yang dirancang untuk menghasilkan praktisi pertanian bernilai tinggi.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="border-left: 5px solid #10b981; padding-left: 15px; margin-bottom: 20px;">
            <h3 class="course-title">1. Precision Agrotechnology</h3>
            <p>Fokus pada optimalisasi fisiologi tanaman dan efisiensi input saintifik.</p>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Lihat Detail Modul"):
            st.markdown("""
            - **Level Silver:** Dasar Fisiologi, Nutrisi 101, Pengenalan HPT.
            - **Level Gold:** Fertigasi Presisi (EC/pH Control), Analisis Tanah Digital.
            - **Level Platinum:** Desain Nutrisi Spesifik Varietas, Manajemen Defisiensi Lanjut.
            """)

    with col2:
        st.markdown("""
        <div style="border-left: 5px solid #3b82f6; padding-left: 15px; margin-bottom: 20px;">
            <h3 class="course-title">2. Agrowisata & Experience</h3>
            <p>Fokus pada transformasi lahan menjadi destinasi wisata ber-ROI tinggi.</p>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Lihat Detail Modul"):
            st.markdown("""
            - **Level Silver:** Konsep Experience Economy, Zonasi Lahan Dasar.
            - **Level Gold:** Desain Masterplan Estetik, Manajemen Alur Pengunjung.
            - **Level Platinum:** Strategi Branding Premium, ROI Agrowisata & Exit Strategy.
            """)

    with col3:
        st.markdown("""
        <div style="border-left: 5px solid #f59e0b; padding-left: 15px; margin-bottom: 20px;">
            <h3 class="course-title">3. Smart Farm IoT</h3>
            <p>Fokus pada otomasi dan data-driven farming menggunakan teknologi AgriSensa.</p>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("Lihat Detail Modul"):
            st.markdown("""
            - **Level Silver:** Pengenalan Sensor IoT, Dashboard Monitoring.
            - **Level Gold:** Otomasi Pengairan & Nutrisi, Pemeliharaan Sensor.
            - **Level Platinum:** Implementasi Digital Twin Lahan, Integrasi AI Prediktif.
            """)
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: STRATEGI KOMERSIALISASI ---
with tabs[1]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("💰 Monetization & Pricing Strategy")
    st.write("Bagaimana mengubah kurikulum ini menjadi mesin pendapatan yang sustain.")
    
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        st.subheader("🌐 Online Stream (Low Touch, High Scalability)")
        st.markdown("""
        - **Video Tutorial Series:** Dijual per modul via Website/Platform Edukasi.
        - **Membership Access:** Langganan bulanan untuk akses dashboard presisi AgriSensa.
        - **E-Book & Panduan Digital:** Dokumen teknis SOP industri.
        """)
        
        # Pricing Table
        pricing_data = {
            "Product Type": ["Video Course Basic", "Video Course Masterclass", "Digital SOP Bundle", "Monthly Membership"],
            "Target Price (Rp)": ["250.000 - 500.000", "1.500.000 - 3.000.000", "350.000", "150.000 / bln"]
        }
        st.table(pd.DataFrame(pricing_data))

    with m_col2:
        st.subheader("🏛️ Offline Stream (High Touch, High Ticket)")
        st.markdown("""
        - **Intensive Bootcamps:** Pelatihan 3 hari langsung di kebun (Farm-Stay).
        - **Corporate Training:** Untuk staff perusahaan agribisnis atau developer properti.
        - **Konsultasi Pendampingan:** Setup agrowisata dari nol sampai operasional.
        """)
        
        services_data = {
            "Service Type": ["3-Day Workshop", "Private Farm Mentoring", "Agrowisata Design Consult", "Certified Professional Course"],
            "Target Price (Rp)": ["3.5M - 7.5M / org", "25M - 50M", "15M - 35M", "10M - 15M"]
        }
        st.table(pd.DataFrame(services_data))
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 3: VIDEO COURSE MAP ---
with tabs[2]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("📽️ Content Production Roadmap")
    st.write("Struktur modul untuk produksi video tutorial berstandar premium.")
    
    video_modules = {
        "Modul 1: The New Era of Farming": "Mindset industri, potensi market, dan pengenalan AgriSensa.",
        "Modul 2: Scientific Foundation": "Cara membaca data pH, EC, dan Fisiologi secara pro.",
        "Modul 3: Designing Your Dream Farm": "Teknis zonasi agrowisata dan estetika lorong buah.",
        "Modul 4: Digital Operation": "Step-by-step menggunakan dashboard IoT dan AI AgriSensa.",
        "Modul 5: Harvest & Marketing": "Teknik panen petik langsung dan strategi jualan via sosmed."
    }
    
    for mod, desc in video_modules.items():
        st.markdown(f"**{mod}**")
        st.caption(desc)
        st.progress(0.0) # Placeholder for production progress
        st.write("---")
    st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 4: WORKSHOP OFFLINE ---
with tabs[3]:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.header("🏫 3-Day Intensive Workshop Syllabus")
    st.info("Workshop offline dirancang untuk memberikan 'Hands-on Experience' yang tak terlupakan.")
    
    day_cols = st.columns(3)
    
    with day_cols[0]:
        st.markdown("### 🌅 Hari 1: Foundation")
        st.write("""
        - **AM:** Teori Fisiologi & Nutrisi.
        - **PM:** Praktik Tes Tanaman & Media.
        - **Night:** Networking Dinner & Case Study.
        """)
        
    with day_cols[1]:
        st.markdown("### ☀️ Hari 2: Action")
        st.write("""
        - **AM:** Teknik Pruning & Fertigasi IoT.
        - **PM:** Desain Agrowisata di Lapangan.
        - **Night:** Simulasi RAB Lahan Peserta.
        """)
        
    with day_cols[2]:
        st.markdown("### 🏆 Hari 3: Master")
        st.write("""
        - **AM:** Marketing & Branding Strategi.
        - **PM:** Ujian Kompetensi & Sertifikasi.
        - **Closing:** Graduation Ceremony.
        """)
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.success("💡 **Tip:** Gunakan fasilitas di 'Modul 28: Analisis Usaha Tani' untuk mendemonstrasikan perhitungan laba rugi real-time saat workshop.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280;">
    <p><b>AgriSensa Education System v1.0</b></p>
    <p>Kurikulum ini dirancang untuk menciptakan standar kualitas baru di industri pertanian Indonesia.</p>
</div>
""", unsafe_allow_html=True)
