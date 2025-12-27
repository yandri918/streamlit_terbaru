import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
from PIL import Image

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.greenhouse_biosecurity_service import GreenhouseBiosecurityService
# from utils.auth import require_auth, show_user_info_sidebar

# Page Config
st.set_page_config(
    page_title="Biosecurity & IPM Design",
    page_icon="🛡️",
    layout="wide"
)

# Authentication
# user = require_auth()
# show_user_info_sidebar()

# Initialize Service
service = GreenhouseBiosecurityService()

# --- HEADER ---
st.title("🛡️ Smart Biosecurity & Greenhouse Infrastructure")
st.markdown("""
**SOP Melon GH MHI Standard** | Implementasi sistem Double Door, Hygiene Lock, dan IPM Fisik untuk perlindungan tanaman maksimal.
""")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🏗️ Desain & Layout", "💰 Kalkulator RAB Anteroom", "📄 Generator SOP"])

with tab1:
    st.subheader("Blueprint Biosecurity (Double Door System)")
    
    # Load Image
    try:
        # Try relative path first
        img_path = os.path.join(parent_dir, "assets", "biosecurity_layout.jpg")
        image = Image.open(img_path)
        st.image(image, caption="Blueprint Biosecurity & IPM Infra Greenhouse Melon (MHI Standard)", use_container_width=True)
    except Exception as e:
        st.warning(f"Gambar blueprint tidak ditemukan: {e}")
        st.info("Fitur tetap berjalan meski gambar preview tidak muncul.")
    
    col_desc1, col_desc2 = st.columns(2)
    with col_desc1:
        st.markdown("""
        ### 🎯 Fitur Utama Desain
        1. **Anteroom / Double Door Hygiene Lock**:
           - Zona transisi antara dunia luar (kotor) dan GH (bersih).
           - Mekanisme: Pintu luar harus tertutup sebelum pintu dalam dibuka.
        2. **Zona Sterilisasi Lengkap**:
           - **Footbath**: Bak celup sepatu dengan desinfektan.
           - **Hand Wash**: Wastafel cuci tangan wajib.
           - **Rak APD**: Tempat ganti sepatu kerja (Boots) & Jas Lab.
        """)
    with col_desc2:
        st.markdown("""
        ### 🦗 Integrasi IPM Fisik
        1. **Sticky Trap di Anteroom**:
           - Menangkap hama yang 'bonceng' masuk saat pintu luar dibuka.
        2. **Insect Screen**:
           - Filter pertama di ventilasi untuk mencegah Thrips/Kutu Kebul.
        3. **Alur Zonasi**:
           - Jalur pekerja diatur searah untuk meminimalisir kontaminasi silang.
        """)

with tab2:
    st.subheader("Kalkulator Biaya Pembuatan Anteroom")
    st.info("Hitung estimasi budget untuk upgrade biosecurity greenhouse Anda.")
    
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        gh_width = st.number_input("Lebar Ruang Anteroom (m)", 2.0, 5.0, 3.0)
        gh_length = st.number_input("Panjang Ruang Anteroom (m)", 2.0, 10.0, 4.0)
    with col_input2:
        gh_height = st.number_input("Tinggi Dinding (m)", 2.0, 5.0, 3.0)
        n_doors = st.number_input("Jumlah Pintu (Unit)", 1, 4, 2)
        
    if st.button("🧮 Hitung Estimasi Biaya"):
        rab = service.calculate_anteroom_cost(gh_width, gh_length, gh_height, n_doors)
        
        # Display RAB Cards
        st.markdown("### 📋 Rincian Anggaran Biaya (Estimasi)")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Struktur & Frame", f"Rp {rab['frame_structure']['cost']:,.0f}", f"{rab['frame_structure']['qty']:.1f} m")
        with c2:
            st.metric("Dinding/Atap (Polycarb)", f"Rp {rab['polycarbonate_or_plastic']['cost']:,.0f}", f"{rab['polycarbonate_or_plastic']['qty']:.1f} m²")
        with c3:
            st.metric("Pintu (Alumunium/Kaca)", f"Rp {rab['doors']['cost']:,.0f}", f"{rab['doors']['qty']} Unit")
            
        total_rab = rab['infrastructure_total']
        st.success(f"### Total Estimasi Fisik: Rp {total_rab:,.0f}")
        
        # Additional Equipments
        st.markdown("#### 🛠️ Perlengkapan Wajib (Hygiene Station)")
        eq_data = [
            {"Item": "Wastafel Cuci Tangan", "Harga Satuan": 750000, "Qty": 1, "Total": 750000},
            {"Item": "Footbath (Bak Desinfektan)", "Harga Satuan": 150000, "Qty": 1, "Total": 150000},
            {"Item": "Rak APD & Sepatu", "Harga Satuan": 500000, "Qty": 1, "Total": 500000},
            {"Item": "APD Set (Boots, Jas, Masker)", "Harga Satuan": 350000, "Qty": 2, "Total": 700000},
            {"Item": "Sticky Trap (Pack)", "Harga Satuan": 50000, "Qty": 2, "Total": 100000},
        ]
        df_eq = pd.DataFrame(eq_data)
        st.dataframe(df_eq, use_container_width=True)
        
        grand_total = total_rab + df_eq['Total'].sum()
        st.markdown(f"### 💰 GRAND TOTAL (Fisik + Alat): Rp {grand_total:,.0f}")

with tab3:
    st.subheader("Generator SOP Biosecurity")
    
    col_sop1, col_sop2 = st.columns(2)
    with col_sop1:
        gh_name = st.text_input("Nama Greenhouse/Blok", "GH-Melon-01")
    with col_sop2:
        manager = st.text_input("Nama Penanggung Jawab", user.get('name', 'Manager Farm'))
        
    if st.button("📄 Generate Dokumen SOP"):
        sop_content = service.generate_sop_checklist(gh_name, manager)
        
        st.markdown("---")
        st.markdown(sop_content)
        st.markdown("---")
        
        # Download Button
        st.download_button(
            label="⬇️ Download SOP (Markdown/Text)",
            data=sop_content,
            file_name=f"SOP_Biosecurity_{gh_name}.md",
            mime="text/markdown"
        )
        
    st.warning("""
    **Catatan Implementasi:**
    SOP ini harus dicetak dan ditempel di dinding Anteroom tepat di atas Rak APD atau di Pintu Luar agar terbaca oleh setiap orang yang masuk.
    """)
