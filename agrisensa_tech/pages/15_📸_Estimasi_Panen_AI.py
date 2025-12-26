
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
def detect_objects_by_color(image_bytes, hsv_lower, hsv_upper, min_area=50):
    """
    Detect objects based on HSV color range.
    Returns: processed_image, count, contours
    """
    # Convert bytes to numpy array
    file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Resize for consistency (optional, but good for speed)
    # height, width = image.shape[:2]
    # if width > 1000:
    #     scale = 1000 / width
    #     image = cv2.resize(image, (int(width*scale), int(height*scale)))
    
    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Create Mask
    lower_bound = np.array(hsv_lower)
    upper_bound = np.array(hsv_upper)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Morphological operations to clean noise
    kernel = np.ones((5,5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Find Contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter by Area
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    count = len(valid_contours)
    
    # Draw Results
    result_img = image.copy()
    cv2.drawContours(result_img, valid_contours, -1, (0, 255, 0), 2)
    
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
        
        result_image, count = detect_objects_by_color(uploaded_file, hsv_lower, hsv_upper, min_area=min_area_val)
        
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
        avg_fruit_per_tree = count / sample_rate # Asumsi foto mewakili X sampel
        est_yield_kg = (avg_fruit_per_tree * avg_weight * plant_pop) / 1000
        
        st.metric("Potensi Tonase Panen (Estimasi)", f"{est_yield_kg:,.1f} Kg")
        st.caption(f"Asumsi: {avg_fruit_per_tree:.1f} buah/pohon x {avg_weight}gr x {plant_pop} pohon.")
        
    except Exception as e:
        st.error(f"Error Processing Image: {e}")
        st.error("Tip: Pastikan format gambar JPG/PNG standard.")

else:
    with col_out:
        st.info("👈 Upload foto dulu untuk melihat hasil.")
        
st.markdown("---")
st.caption("🔒 **Privacy Safe**: Foto diproses di memori sementara (RAM) dan tidak disimpan selamanya.")
