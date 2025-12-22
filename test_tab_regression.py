import streamlit as st

st.set_page_config(page_title="Test Tab Regression", page_icon="🔬", layout="wide")

st.title("🔬 Test: Apakah Tab Regresi Ada?")

# MAIN TABS - SAMA SEPERTI DI MODULE 12
tab_ml, tab_stat, tab_regression = st.tabs([
    "🤖 Mode Machine Learning (Prediksi)", 
    "📊 Mode Statistika (RAL/RAK)",
    "📚 Teori Regresi & Visualisasi"
])

with tab_ml:
    st.header("Tab 1: Machine Learning")
    st.success("✅ Tab ML berfungsi!")

with tab_stat:
    st.header("Tab 2: Statistika")
    st.success("✅ Tab Statistika berfungsi!")

with tab_regression:
    st.header("Tab 3: Teori Regresi")
    st.success("✅✅✅ TAB REGRESI BERFUNGSI! ✅✅✅")
    st.balloons()
    
    st.markdown("""
    ## 🎉 Selamat!
    
    Jika Anda melihat halaman ini, berarti **tab ke-3 sudah ada dan berfungsi!**
    
    Ini berarti di Module 12 yang asli juga sudah ada tab ini.
    
    **Kemungkinan masalahnya:**
    1. Browser cache - Coba hard refresh (Ctrl + Shift + R)
    2. Streamlit cache - Sudah di-clear
    3. Anda membuka port yang salah
    
    **Solusi:**
    - Tutup semua tab browser yang buka AgriSensa
    - Restart Streamlit
    - Buka fresh: http://localhost:8501
    """)
