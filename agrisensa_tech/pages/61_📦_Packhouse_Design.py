import streamlit as st
import sys
import os
from pathlib import Path
from PIL import Image
import pandas as pd
import random
import string

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.packhouse_service import PackhouseService
from utils.auth import require_auth, show_user_info_sidebar

# Page Config
st.set_page_config(
    page_title="Packhouse Design & QC",
    page_icon="📦",
    layout="wide"
)

# Authentication
user = require_auth()
show_user_info_sidebar()

service = PackhouseService()

# --- HEADER ---
st.title("📦 Packhouse & Post-Harvest Center")
st.markdown("""
**SOP Pasca Panen Melon Standard MHI** | Desain Zonasi, QC Grading Digital, dan Traceability System.
""")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["🏗️ Layout & Zonasi", "📱 Digital QC Grading", "🏷️ Label Generator"])

with tab1:
    st.subheader("Blueprint Packhouse (5 Zona Linier)")
    
    # Load Image
    try:
        img_path = os.path.join(parent_dir, "assets", "packhouse_layout.jpg")
        image = Image.open(img_path)
        st.image(image, caption="Blueprint Area Panen - Grading - Packing Melon (MHI Standard)", use_container_width=True)
    except Exception as e:
        st.warning("Gambar blueprint tidak ditemukan.")
    
    st.info("💡 **Konsep Utama:** Alur Satu Arah (One Way Flow) dari Kotor -> Bersih.")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        ### ✅ Zonasi Higienis
        - **Zona 1 (Penerimaan):** Area kotor, buah datang dari GH.
        - **Zona 2 (Pembersihan):** Inspeksi awal & pembersihan debu.
        - **Zona 3 (Sortasi/Grading):** Pemisahan Grade A, B, dan Reject.
        - **Zona 4 (Penimbangan):** Penimbangan presisi & labelling.
        - **Zona 5 (Packing):** Pengemasan akhir & siap kirim.
        """)
    with c2:
        st.markdown("""
        ### 🛡️ Kunci Keamanan Pangan
        - **No Cross-Movement:** Jalur masuk buah kotor berbeda dengan jalur keluar buah bersih.
        - **QC Point:** Pos QC ditempatkan strategis di tengah alur.
        - **Hygiene Station:** Wastafel & APD wajib bagi staf packing.
        """)

with tab2:
    st.subheader("📱 Digital QC Form (Meja Sortasi)")
    st.caption("Gunakan tablet di meja grading untuk input data real-time.")
    
    col_batch, col_src = st.columns(2)
    with col_batch:
        batch_id = st.text_input("Kode Batch Panen", f"B-{random.randint(1000,9999)}")
    with col_src:
        gh_source = st.selectbox("Asal Greenhouse", ["GH-Melon-01", "GH-Melon-02", "GH-Sayur-01"])
        
    st.markdown("### Input Hasil Grading")
    
    # Session state for temporary batch data
    if 'grading_data' not in st.session_state:
        st.session_state.grading_data = [] # List of dicts
        
    with st.form("grading_input"):
        c_g1, c_g2, c_g3 = st.columns(3)
        with c_g1:
            n_grade_a = st.number_input("Jumlah Grade A (Pcs)", 0, 1000, 0)
            avg_w_a = st.number_input("Avg Berat A (kg)", 0.0, 5.0, 1.8)
        with c_g2:
            n_grade_b = st.number_input("Jumlah Grade B (Pcs)", 0, 1000, 0)
            avg_w_b = st.number_input("Avg Berat B (kg)", 0.0, 5.0, 1.2)
        with c_g3:
            n_reject = st.number_input("Jumlah Reject (Pcs)", 0, 1000, 0)
            reason = st.text_input("Alasan Utama Reject", "Ukuran kecil / Cacat")
            
        btn_add = st.form_submit_button("➕ Submit Data Grading")
        
        if btn_add:
            # Generate dummy itemized data for stats calculation
            batch_items = []
            for _ in range(n_grade_a):
                batch_items.append({'grade': 'A', 'weight': avg_w_a})
            for _ in range(n_grade_b):
                batch_items.append({'grade': 'B', 'weight': avg_w_b})
            for _ in range(n_reject):
                batch_items.append({'grade': 'Reject', 'weight': 0.5}) # dummy weight for reject
            
            stats = service.calculate_grading_stats(batch_items)
            st.session_state.grading_results = stats
            st.success("Data berhasil diinput!")
            
    # Show Results
    if 'grading_results' in st.session_state:
        res = st.session_state.grading_results
        st.markdown("### 📊 Laporan Kualitas Batch Ini")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Buah", f"{res['total_pcs']} pcs")
        m2.metric("Grade A (Premium)", f"{res['grade_a_count']} pcs", f"{res['pct_a']:.1f}%")
        m3.metric("Grade B (Standard)", f"{res['grade_b_count']} pcs", f"{res['pct_b']:.1f}%")
        m4.metric("Reject", f"{res['reject_count']} pcs", f"-{res['pct_reject']:.1f}%", delta_color="inverse")
        
        if res['pct_a'] > 80:
            st.success("🌟 Kualitas Panen Sangat Baik! (>80% Grade A)")
        elif res['pct_reject'] > 20:
            st.error("⚠️ Perhatian: Tingkat Reject Tinggi (>20%). Cek hama/penyakit di GH.")

with tab3:
    st.subheader("🏷️ Label Generator (Traceability)")
    
    col_lab1, col_lab2 = st.columns(2)
    with col_lab1:
        lbl_grade = st.selectbox("Pilih Grade Label", ["Grade A (Premium)", "Grade B (Standard)"])
    with col_lab2:
        lbl_weight = st.number_input("Berat (kg - Kosongkan utk manual)", 0.0, 5.0, 0.0)
        
    if st.button("🖨️ Preview Label"):
        grade_code = "A" if "Grade A" in lbl_grade else "B"
        label_text = service.generate_label_text(batch_id, gh_source, "Melon Golden Aroma", grade_code, lbl_weight if lbl_weight > 0 else "____")
        
        st.code(label_text, language="text")
        st.caption("Siap dicetak di printer label thermal (Zebra/TSC).")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>📦 <strong>AgriSensa Packhouse System</strong></p>
    <p>Professional Post-Harvest Handling for Export Quality</p>
</div>
""", unsafe_allow_html=True)
