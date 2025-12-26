
import streamlit as st
import cv2
import numpy as np
import io
from PIL import Image
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Estimasi Panen AI", page_icon="📸", layout="wide")

# Auth
user = require_auth()
show_user_info_sidebar()

# ==========================================
# 🧠 COMPUTER VISION LOGIC (OpenCV)
# ==========================================
def detect_objects_by_color(image_bytes, hsv_lower, hsv_upper, min_area=50, min_circularity=0.3, erosion_size=1):
    """
    Detect objects based on HSV color range & Shape.
    Returns: processed_image, count, contours
    """
    # Convert bytes to numpy array
    file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create Mask
    lower_bound = np.array(hsv_lower)
    upper_bound = np.array(hsv_upper)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Morphological operations to clean noise AND remove stems
    # 1. Open (Erosion then Dilation) to remove thin lines (stems)
    kernel_erode = np.ones((erosion_size, erosion_size), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel_erode, iterations=1)
    
    # 2. Close (Dilation then Erosion) to fill gaps in fruits
    kernel_close = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel_close)
    
    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by Area & Shape (Circularity)
    valid_contours = []
    rejected_contours = []
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
            
        # Circularity Check
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0: continue
        circularity = (4 * np.pi * area) / (perimeter ** 2)
        
        if circularity > min_circularity: 
             valid_contours.append(cnt)
        else:
             rejected_contours.append(cnt)

    count = len(valid_contours)
    
    # Draw Results
    result_img = image.copy()
    # Draw Valid in GREEN
    cv2.drawContours(result_img, valid_contours, -1, (0, 255, 0), 2)
    # Draw Rejected (Stems/Noise) in RED so user sees what is ignored
    cv2.drawContours(result_img, rejected_contours, -1, (0, 0, 255), 1)
    
    # Add count label
    cv2.putText(result_img, f"Count: {count}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    
    # Convert back to RGB for Streamlit
    result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
    
    return result_img, count

# ==========================================
# UI
# ==========================================
st.title("📸 Estimasi Panen Visual Cepat (V1)")
st.markdown("**Prototipe Penghitung Buah Otomatis berbasis Warna (Color Thresholding)**")

st.info("""
ℹ️ **Cara Kerja:** Upload foto tanaman atau gunakan kamera. Sistem akan menghitung buah berdasarkan warna (Merah/Oranye/Hijau).
Gunakan **Slider Kalibrasi** di sebelah kiri untuk menyesuaikan deteksi dengan pencahayaan foto Anda.
""")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("⚙️ Kalibrasi Deteksi")

detect_mode = st.sidebar.selectbox("Target Deteksi:", ["🌶️ Cabai Merah (Red)", "🍅 Tomat (Orange/Red)", "🍋 Jeruk/Lemon (Yellow)", "🥬 Daun/Sayur (Green)"])

# Default HSV Ranges
if "Cabai" in detect_mode or "Tomat" in detect_mode:
    # Red has two ranges in HSV (0-10 and 170-180), simpler single range for now
    def_h_low, def_h_high = 0, 10 
    def_s_low, def_s_high = 100, 255
    def_v_low, def_v_high = 100, 255
elif "Jeruk" in detect_mode:
    def_h_low, def_h_high = 20, 35
    def_s_low, def_s_high = 100, 255
    def_v_low, def_v_high = 100, 255
else: # Green
    def_h_low, def_h_high = 35, 85
    def_s_low, def_s_high = 50, 255
    def_v_low, def_v_high = 50, 255

st.sidebar.subheader("🎚️ Fine Tuning HSV")
h_min = st.sidebar.slider("Hue Min", 0, 179, def_h_low)
h_max = st.sidebar.slider("Hue Max", 0, 179, def_h_high)
s_min = st.sidebar.slider("Saturation Min", 0, 255, def_s_low)
s_max = st.sidebar.slider("Saturation Max", 0, 255, def_s_high)
v_min = st.sidebar.slider("Value Min", 0, 255, def_v_low)
v_max = st.sidebar.slider("Value Max", 0, 255, def_v_high)

st.sidebar.divider()
min_area_val = st.sidebar.slider("Min Pixel Area (Size Filter)", 10, 500, 50, help="Abaikan bintik kecil (noise)")
min_circ_val = st.sidebar.slider("Min Circularity (Shape Filter)", 0.0, 1.0, 0.3, step=0.05, help="0.0=Semua, 1.0=Lingkaran Sempurna. Naikkan untuk membuang tangkai (garis).")
erosion_val = st.sidebar.slider("Stem Removal Strength (Erosion)", 1, 9, 3, step=2, help="Kekuatan penghapusan garis tipis. Ganjil (1,3,5...). Semakin besar, tangkai semakin hilang tapi buah kecil bisa ikut hilang.")

st.sidebar.divider()
st.sidebar.subheader("🌤️ Skenario Iklim")
climate_scenario = st.sidebar.selectbox(
    "Prakiraan Cuaca Musim Depan:",
    ["Normal / Ideal (Optimis)", "El Nino / Kekeringan (-20%)", "La Nina / Curah Hujan Tinggi (-15%)"],
    help="AI akan mengoreksi target panen berdasarkan stres lingkungan."
)

# --- MAIN AREA ---
col_in, col_out = st.columns(2)

uploaded_file = None
use_camera = st.checkbox("Gunakan Kamera Langsung?")

with col_in:
    st.subheader("1. Input Gambar")
    if use_camera:
        uploaded_file = st.camera_input("Ambil Foto Tanaman")
    else:
        uploaded_file = st.file_uploader("Upload Foto (JPG/PNG)", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # Process
    hsv_lower = [h_min, s_min, v_min]
    hsv_upper = [h_max, s_max, v_max]
    
    try:
        # We need to read the file, but Streamlit file object pointer moves. 
        # Reset pointer or read once.
        # detect_objects_by_color reads it.
        
        result_image, count = detect_objects_by_color(uploaded_file, hsv_lower, hsv_upper, min_area=min_area_val, min_circularity=min_circ_val, erosion_size=erosion_val)
        
        with col_out:
            st.subheader("2. Hasil Deteksi")
            st.image(result_image, caption=f"Terdeteksi: {count} Objek", use_column_width=True)
            
            if count == 0:
                st.warning("⚠️ Tidak ada objek terdeteksi. Coba atur slider HSV di sidebar.")
            else:
                st.success(f"✅ **Ditemukan {count} Buah!**")
        
        # --- YIELD CALCULATOR ---
        st.divider()
        st.subheader("💰 Kalkulator Estimasi Panen")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            avg_weight = st.number_input("Rata-rata Berat per Buah (gram):", 1, 1000, 15)
        with c2:
            plant_pop = st.number_input("Total Populasi Tanaman (Pohon):", 100, 100000, 1000)
        with c3:
            sample_rate = st.number_input("Jumlah Sampel Foto:", 1, 100, 1, help="Berapa pohon yang Anda foto?")
            
        # Calc
        # Calc Raw
        avg_fruit_per_tree = count / sample_rate # Asumsi foto mewakili X sampel
        raw_yield_kg = (avg_fruit_per_tree * avg_weight * plant_pop) / 1000
        
        # --- STAGE 3: CLIMATE CORRECTION ---
        # (Selector now in Sidebar)
        
        correction_factor = 0.0
        correction_desc = "Optimal"
        if "El Nino" in climate_scenario:
            correction_factor = -0.20
            correction_desc = "Stres Air (Buah Mengecil)"
        elif "La Nina" in climate_scenario:
            correction_factor = -0.15
            correction_desc = "Risiko Busuk/Jamur"
            
        final_yield_kg = raw_yield_kg * (1 + correction_factor)
        loss_kg = raw_yield_kg - final_yield_kg
        
        # Display
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.metric("Potensi Awal (Raw)", f"{raw_yield_kg:,.1f} Kg", help="Hitungan murni dari kamera x populasi.")
        with col_res2:
            delta_color = "off" if correction_factor == 0 else "inverse"
            st.metric("Prediksi Akhir (Climate Adjusted)", f"{final_yield_kg:,.1f} Kg", f"{correction_factor*100:.0f}% ({correction_desc})", delta_color=delta_color)
            
        if correction_factor != 0:
            st.warning(f"⚠️ Potensi kehilangan hasil: **{loss_kg:,.1f} Kg** akibat faktor cuaca.")
            
        st.caption(f"Asumsi: {avg_fruit_per_tree:.1f} buah/pohon x {avg_weight}gr x {plant_pop} pohon.")
        
    except Exception as e:
        st.error(f"Error Processing Image: {e}")
        st.error("Tip: Pastikan format gambar JPG/PNG standard.")

else:
    with col_out:
        st.info("👈 Upload foto dulu untuk melihat hasil.")
        
st.markdown("---")
st.caption("🔒 **Privacy Safe**: Foto diproses di memori sementara (RAM) dan tidak disimpan selamanya.")
