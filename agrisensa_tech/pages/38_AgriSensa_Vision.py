import streamlit as st
import cv2
import numpy as np
import plotly.express as px
from PIL import Image

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="AgriSensa Vision", page_icon="🛸", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================


# ==========================================
# 🧠 IMAGE PROCESSING ENGINE
# ==========================================

# ==========================================
# 🧠 IMAGE PROCESSING ENGINES
# ==========================================

def calculate_vari(image_array):
    """VARI Algorithm for Aerial View"""
    img = image_array.astype(float) / 255.0
    R, G, B = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    numerator = G - R
    denominator = G + R - B + 0.00001
    return numerator / denominator

def detect_plants(image_array, sensitivity, min_area):
    """Plant Counting for Aerial View"""
    hsv = cv2.cvtColor(image_array, cv2.COLOR_RGB2HSV)
    lower_green = np.array([30 - (sensitivity/5), 40, 40])
    upper_green = np.array([90 + (sensitivity/5), 255, 255])
    mask = cv2.inRange(hsv, lower_green, upper_green)
    kernel = np.ones((3,3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    valid_contours = []
    output_img = image_array.copy()
    for c in contours:
        if cv2.contourArea(c) > min_area:
            valid_contours.append(c)
            cv2.drawContours(output_img, [c], -1, (255, 0, 0), 2)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cv2.circle(output_img, (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"])), 5, (255, 255, 0), -1)
    return len(valid_contours), output_img, mask

def analyze_bwd(image_array, crop_type="Padi"):
    """
    BWD / LCC (Leaf Color Chart) Analysis for Nitrogen Estimation.
    Supports Padi (Standard IRRI), Jagung, and General Horticulture (Cabai).
    """
    # 1. Focus on Center Area (Region of Interest)
    h, w, _ = image_array.shape
    center_img = image_array[int(h*0.3):int(h*0.7), int(w*0.3):int(w*0.7)]
    
    # 2. Average Greenness Calculation
    avg_color_per_row = np.average(center_img, axis=0)
    avg_color = np.average(avg_color_per_row, axis=0)
    R, G, B = avg_color
    
    lcc_score = 0
    status = ""
    recommendation = ""
    
    # 3. LOGIC BY CROP TYPE
    
    if crop_type == "Padi (Rice)":
        # Standard IRRI LCC Logic
        if G < 60:
            lcc_score = 1; status = "BWD 1 (Kuning/Kering)"
            recommendation = "Kritis. Segera pupuk Urea 100 kg/ha."
        elif G < 100:
            lcc_score = 2; status = "BWD 2 (Hijau Kekuningan)"
            recommendation = "Defisiensi. Tambahkan Urea 75 kg/ha."
        elif G < 140:
            lcc_score = 3; status = "BWD 3 (Hijau Muda)"
            recommendation = "Perlu Urea 50 kg/ha (Fase Aktif)."
        elif G < 180:
            lcc_score = 4; status = "BWD 4 (Hijau Mantap)"
            recommendation = "Optimal. TIDAK PERLU pupuk."
        else:
            lcc_score = 5; status = "BWD 5 (Hijau Gelap)"
            recommendation = "Berlebih. Stop pemupukan."
            
    elif crop_type == "Jagung (Maize)":
        # CIMMYT LCC Logic (Slightly darker needs)
        if G < 80:
            status = "Kritis (Kuning)"
            recommendation = "Kekurangan N parah. Kocor Urea+ZA segera."
        elif G < 130:
            status = "Kurang (Hijau Muda)"
            recommendation = "Berikan NPK da Urea susulan."
        elif G < 170:
            status = "Optimal (Hijau)"
            recommendation = "Pertahankan kondisi."
        else:
            status = "Excess (Hijau Kebiruan)"
            recommendation = "Kurangi dosis N periode berikutnya."
            
    elif crop_type == "Cabai & Sayuran":
        # Horticulture Logic (General N-Index)
        # Cabai is sensitive to excess N (leaves become curly/dark)
        if G < 90:
            status = "Defisiensi Berat (Kuning)"
            recommendation = "Tanaman kerdil/klorosis. Kocor NPK Seimbang + Magnesium (Epsom)."
        elif G < 130:
            status = "Defisiensi Ringan (Hijau Pucat)"
            recommendation = "Tambahkan Pupuk Daun (Foliar) atau KNO3 Merah."
        elif G < 160:
            status = "Optimal (Hijau Segar)"
            recommendation = "Lanjutkan pemupukan rutin mingguan."
        else:
            status = "Kelebihan N (Hijau Gelap/Hitam)"
            recommendation = "Bahaya! Rentan serangan Thrips/Tungau. Stop pupuk N, ganti MKP/Kalium."
        
    return status, recommendation, center_img

# ==========================================
# 🖥️ UI LAYOUT
# ==========================================

st.title("🛸 AgriSensa Vision")
st.markdown("**Platform Analisis Citra Pertanian Cerdas**")

# MODE SELECTION
mode = st.radio("Pilih Mode Analisis:", ["📸 Analisis Daun (BWD/LCC/Visual)", "🚁 Analisis Drone (Aerial)"], horizontal=True)

if mode == "🚁 Analisis Drone (Aerial)":
    # ... (Aerial Logic remains same) ...
    st.info("Upload foto udara/drone untuk menghitung populasi dan cek kesehatan lahan (VARI).")
    
    # SIDEBAR CONFIG AERIAL
    with st.sidebar:
        st.header("⚙️ Konfigurasi Drone")
        sens = st.slider("Sensitivitas Warna Hijau", 0, 100, 50)
        min_area = st.number_input("Min. Area (px)", 10, 5000, 100)
        heatmap_opacity = st.slider("Opasitas Heatmap", 0.1, 1.0, 0.6)

    uploaded_file = st.file_uploader("Upload Foto Udara (JPG/PNG)", type=['jpg', 'jpeg', 'png'], key="drone")

    if uploaded_file:
        with Image.open(uploaded_file) as src_img:
            image = src_img.convert("RGB")
            img_array = np.array(image)
        
        with st.spinner("Menganalisa lahan..."):
            count, contour_img, mask_img = detect_plants(img_array, sens, min_area)
            vari_map = calculate_vari(img_array)
            
        st.success("Selesai!")
        tab1, tab2 = st.tabs(["📊 Counting", "🌡️ Health Heatmap"])
        with tab1:
            st.image(contour_img, caption=f"Terdeteksi: {count} Tanaman", use_column_width=True)
        with tab2:
            fig = px.imshow(vari_map, color_continuous_scale='RdYlGn')
            fig.update_traces(opacity=heatmap_opacity)
            st.plotly_chart(fig, use_container_width=True)

elif mode == "📸 Analisis Daun (BWD/LCC/Visual)":
    st.info("Diagnosa visual status Nitrogen berdasarkan warna daun.")
    
    crop_type = st.selectbox("Pilih Jenis Tanaman:", ["Padi (Rice)", "Jagung (Maize)", "Cabai & Sayuran"])
    
    input_method = st.radio("Sumber Citra:", ["📂 Upload Galeri", "📸 Kamera Langsung"], horizontal=True)
    
    uploaded_leaf = None
    if input_method == "📂 Upload Galeri":
        uploaded_leaf = st.file_uploader("Upload Foto Daun (Close Up)", type=['jpg', 'jpeg', 'png'], key="leaf_upload")
    else:
        uploaded_leaf = st.camera_input("Ambil Foto Presisi (Pastikan Cahaya Cukup)")
    
    if uploaded_leaf:
        with Image.open(uploaded_leaf) as src_img:
            image = src_img.convert("RGB")
            img_array = np.array(image)
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.image(img_array, caption="Foto Asli", use_column_width=True)
            
        with st.spinner("Menganalisa warna daun..."):
            status, rec, roi_img = analyze_bwd(img_array, crop_type)
            
        with col_res2:
            st.image(roi_img, caption="Area Analisis (ROI)", width=150)
            st.subheader(status)
            
            if "Kritis" in status or "Defisiensi" in status:
                st.warning(f"💡 **Rekomendasi:** {rec}")
            elif "Kelebihan" in status or "Excess" in status:
                st.error(f"⚠️ **Peringatan:** {rec}")
            else:
                st.success(f"✅ **Rekomendasi:** {rec}")
                
            st.markdown("---")
            if crop_type == "Padi (Rice)":
                st.caption("Referensi: IRRI Leaf Color Chart Standard (Skala 1-5)")
            else:
                st.caption("Catatan: Analisis ini adalah estimasi visual (Digital Diagnosis). Untuk hasil presisi tinggi, gunakan uji laboratorium jaringan.")
