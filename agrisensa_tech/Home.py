import streamlit as st
import sys
import os

# Direct Ticker Implementation (Fixes Import Issues)
def price_ticker():
    # Mock Data (Simulated Bapanas Feed)
    prices = [
        {"name": "🌶️ Cabai Merah", "price": "Rp 45.000", "trend": "up"},
        {"name": "🧅 Bawang Merah", "price": "Rp 28.500", "trend": "down"},
        {"name": "🍚 Beras Premium", "price": "Rp 14.200", "trend": "stable"},
        {"name": "🐔 Daging Ayam", "price": "Rp 35.000", "trend": "up"},
        {"name": "🌽 Jagung Pipil", "price": "Rp 5.800", "trend": "stable"},
    ]
    
    ticker_html = ""
    for p in prices:
        color = "#10b981" if p['trend'] == "up" else ("#ef4444" if p['trend'] == "down" else "#fbbf24")
        icon = "&uarr;" if p['trend'] == "up" else ("&darr;" if p['trend'] == "down" else "&bull;")
        
        # Simple HTML Span
        ticker_html += f"""
        <span style="margin-right: 40px; font-weight: 500;">
            <span style="color: #94a3b8;">{p["name"]}</span> 
            <span style="color: white; font-weight: bold;">{p["price"]}</span> 
            <span style="color: {color}; font-weight: bold;">{icon}</span>
        </span>
        """
    
    # Use Standard Marquee Tag (Foolproof)
    st.markdown(f"""
    <div style="background-color: #0f172a; padding: 10px; border-bottom: 2px solid #334155; margin-bottom: 20px; border-radius: 5px;">
        <marquee scrollamount="10" style="color: white; font-family: sans-serif; font-size: 1.1rem;">
            {ticker_html}
        </marquee>
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
with c6:
    if st.button("🏠 Greenhouse & Hidroponik"): st.switch_page("pages/33_🏠_Greenhouse_Hidroponik.py")
    if st.button("💧 Irigasi & Drainase"): st.switch_page("pages/32_💧_Irigasi_Drainase.py")

st.markdown("---")
if st.button("🚜 Mekanisasi Pertanian"): st.switch_page("pages/41_🚜_Mekanisasi_Pertanian.py")
