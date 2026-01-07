import streamlit as st
import sys
import os

# Import BAPANAS Service
try:
    from services.bapanas_service import BapanasService
except ImportError:
    # Fallback if import fails
    BapanasService = None

# Real-Time BAPANAS Ticker
def price_ticker():
    """Display real-time commodity prices from BAPANAS"""
    
    # Try to fetch real data
    if BapanasService:
        try:
            service = BapanasService()
            df = service.get_latest_prices(province_id=0)  # National average
            
            if df is not None and not df.empty:
                # Get today's prices only
                latest_df = df[df['date'] == df['date'].max()].copy()
                
                # Display ALL commodities from BAPANAS (instead of just top 5)
                ticker_parts = []
                for _, row in latest_df.iterrows():
                    commodity = row['commodity']
                    price = row['price']
                    
                    # Format price
                    price_str = f"Rp {price:,.0f}"
                    
                    # Simple trend indicator (can be enhanced with yesterday comparison)
                    ticker_parts.append(f"{commodity} **{price_str}**")
                
                ticker_text = "   •   ".join(ticker_parts)
                
                # Display with BAPANAS branding
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); 
                            padding: 12px 20px; 
                            border-radius: 8px; 
                            border-left: 4px solid #10b981;
                            margin-bottom: 20px;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <p style="color: #e2e8f0; margin: 0; font-size: 0.95rem; font-weight: 500;">
                        📊 <strong>Harga Pangan Hari Ini (BAPANAS - LIVE):</strong> {ticker_text}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                return
            else:
                # API returned empty data
                st.warning("⚠️ API BAPANAS mengembalikan data kosong. Menggunakan fallback.")
        except Exception as e:
            # Show error for debugging
            st.error(f"❌ Error saat mengambil data BAPANAS: {str(e)}")
            import traceback
            st.code(traceback.format_exc())
    
    # Fallback: Show static message if API fails
    st.markdown("""
    <div style="background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%); 
                padding: 12px 20px; 
                border-radius: 8px; 
                border-left: 4px solid #fbbf24;
                margin-bottom: 20px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
        <p style="color: #e2e8f0; margin: 0; font-size: 0.95rem; font-weight: 500;">
            📊 <strong>Harga Pangan:</strong> Klik menu "Analisis Tren Harga" untuk data real-time BAPANAS
        </p>
    </div>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="AgriSensa Tech", page_icon="🛰️", layout="wide")

# Validasi Auth (Optional check if needed)
# from utils.auth import require_auth
# require_auth()

# --- RUNNING TEXT TICKER ---
price_ticker()

st.markdown("""
<style>
    .hero { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%); padding: 3rem; border-radius: 1rem; color: white; text-align: center; }
    .card { background: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); margin-bottom: 1rem; border: 1px solid #e5e7eb; }
    .card h3 { color: #2563eb; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="hero"><h1>🛰️ AgriSensa Tech</h1><p>Presisi, IoT, Drone, dan Bioteknologi Pertanian</p></div>', unsafe_allow_html=True)

st.markdown("### 🔬 Laboratorium & Riset")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🔬 Asisten Penelitian"): st.switch_page("pages/12_🔬_Asisten_Penelitian.py")
    if st.button("🧬 Genetika Pemuliaan"): st.switch_page("pages/31_🧬_Genetika_Pemuliaan.py")
with c2:
    if st.button("🌱 Fisiologi Tumbuhan"): st.switch_page("pages/29_🌱_Fisiologi_Tumbuhan.py")
    if st.button("📏 Pantau Pertumbuhan"): st.switch_page("pages/39_📏_Pantau_Pertumbuhan.py")
with c3:
    if st.button("📦 Teknologi Pasca Panen"): st.switch_page("pages/30_📦_Teknologi_Pasca_Panen.py")

st.markdown("### 🛸 Smart Farming & IoT")
c4, c5, c6 = st.columns(3)
with c4:
    if st.button("🛰️ GIS Precision Farming"): st.switch_page("pages/37_🛰️_GIS_Precision_Farming.py")
    if st.button("🛸 AgriSensa Vision"): st.switch_page("pages/38_🛸_AgriSensa_Vision.py")
with c5:
    if st.button("🛰️ Drone Command Center"): st.switch_page("pages/50_🛰️_AgriDrone_Command_Center.py")
    if st.button("📊 AI Intelligence Pro"): st.switch_page("pages/46_📊_AgriSensa_Intelligence_Pro.py")
    if st.button("🌦️ Weather Intelligence"): st.switch_page("pages/62_Weather_Intelligence.py")
with c6:
    if st.button("🏠 Greenhouse & Hidroponik"): st.switch_page("pages/33_Greenhouse_Hidroponik.py")
    if st.button("🌱 Premium Hidroponik AI"): st.switch_page("pages/66_Hidroponik_Premium_Advanced.py")
    st.caption("AI-Powered | IoT Ready | 10x Advanced")
    if st.button("🎯 SOP Presisi Komoditas"): st.switch_page("pages/54_SOP_Presisi_Komoditas.py")
    if st.button("📚 SOP Documentation Center"): st.switch_page("pages/63_SOP_Documentation_Center.py")
    if st.button("📊 Visualisasi Data Altair"): st.switch_page("pages/67_📊_Visualisasi_Data_Altair.py")
    st.caption("Interactive Charts & Analytics")
    if st.button("🤖 Machine Learning PyCaret"): st.switch_page("pages/68_🤖_Machine_Learning_PyCaret.py")
    st.caption("AutoML & Predictive Analytics")

st.markdown("---")
st.markdown("### 🚜 Manajemen Aset & Infrastruktur")

c_m1, c_m2, c_m3 = st.columns(3)
with c_m1:
    if st.button("🚜 Manajemen Alsintan"): st.switch_page("pages/41_🚜_Mekanisasi_Pertanian.py")
with c_m2:
    if st.button("🛡️ Desain Biosecurity"): st.switch_page("pages/60_🛡️_Biosecurity_Design.py")
    st.caption("RAB Anteroom & SOP")
with c_m3:
    if st.button("📦 Packhouse & QC"): st.switch_page("pages/61_📦_Packhouse_Design.py")
    st.caption("Grading & Labeling Layout")
