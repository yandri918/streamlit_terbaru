
import streamlit as st
import pandas as pd
import datetime
import qrcode
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import streamlit.components.v1 as components

# Page Config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Traceability & QR Passport",
    page_icon="🏷️",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Custom CSS with Print Styles
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #0f766e 0%, #115e59 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .label-preview {
        border: 2px dashed #cbd5e1;
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    h1, h2, h3 { color: #134e4a; }
    
    /* Print Styles */
    @media print {
        .stApp > header, .main-header, .stTabs, button, .stDownloadButton {
            display: none !important;
        }
        .printable-label {
            page-break-after: always;
            margin: 0;
            padding: 0;
        }
    }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1>🏷️ AgriPass (Traceability)</h1><p>Paspor Digital Produk Premium & Generator QR Code</p></div>', unsafe_allow_html=True)

# SESSION STATE Init
if 'batch_data' not in st.session_state:
    st.session_state['batch_data'] = {}

# ===== HELPER FUNCTIONS =====

def generate_printable_label(data, size="medium", qr_img=None):
    """
    Generate print-ready label image with MODERN PREMIUM layout
    Args:
        data: batch data dictionary
        size: "small" (5x5cm), "medium" (10x10cm), "large" (15x10cm)
        qr_img: PIL Image of QR code
    Returns:
        PIL Image object
    """
    # Size mapping at 300 DPI for print quality
    # Format: (width, height)
    sizes = {
        # Square/Portrait formats
        "small": (590, 590),          # 5x5 cm
        "medium": (1181, 1181),       # 10x10 cm
        "large": (1772, 1181),        # 15x10 cm
        
        # Landscape formats (RECOMMENDED for products)
        "small_landscape": (1181, 590),      # 10x5 cm - compact
        "medium_landscape": (1772, 1181),    # 15x10 cm - standard
        "large_landscape": (2362, 1181),     # 20x10 cm - premium
    }
    
    width, height = sizes[size]
    is_landscape = "landscape" in size
    is_small = size == "small"  # Special handling for 5x5 cm
    
    # Create blank canvas with gradient background
    label = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(label)
    
    # === MODERN GRADIENT BACKGROUND ===
    # Create subtle gradient from light teal to white
    for i in range(height):
        # Gradient from top (light teal) to bottom (white)
        ratio = i / height
        r = int(240 + (255 - 240) * ratio)
        g = int(253 + (255 - 253) * ratio)
        b = int(250 + (255 - 250) * ratio)
        draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
    
    # === ADAPTIVE FONT SIZES based on label size ===
    try:
        if is_small:
            # Smaller, more compact fonts for 5x5 cm
            font_brand = ImageFont.truetype("arialbd.ttf", 22)      # Brand/header
            font_title = ImageFont.truetype("arialbd.ttf", 48)      # Product name (bold)
            font_subtitle = ImageFont.truetype("arialbd.ttf", 32)   # Varietas (bold for emphasis)
            font_body = ImageFont.truetype("arial.ttf", 26)         # Body text
            font_small = ImageFont.truetype("arial.ttf", 22)        # Small text
            font_tiny = ImageFont.truetype("arial.ttf", 18)         # Tiny text
        else:
            # Standard fonts for larger labels
            font_brand = ImageFont.truetype("arialbd.ttf", 45)      # Brand/header
            font_title = ImageFont.truetype("arialbd.ttf", 70)      # Product name (bold)
            font_subtitle = ImageFont.truetype("arial.ttf", 42)     # Varietas
            font_body = ImageFont.truetype("arial.ttf", 38)         # Body text
            font_small = ImageFont.truetype("arial.ttf", 32)        # Small text
            font_tiny = ImageFont.truetype("arial.ttf", 28)         # Tiny text
    except:
        font_brand = ImageFont.load_default()
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
        font_small = ImageFont.load_default()
        font_tiny = ImageFont.load_default()
    
    # === MODERN COLOR PALETTE ===
    color_primary = (16, 185, 129)      # Emerald-500
    color_primary_dark = (5, 150, 105)  # Emerald-600
    color_accent = (251, 191, 36)       # Amber-400
    color_text = (31, 41, 55)           # Gray-800
    color_text_light = (107, 114, 128)  # Gray-500
    color_white = (255, 255, 255)
    color_badge_organic = (34, 197, 94)     # Green-500
    color_badge_halal = (59, 130, 246)      # Blue-500
    color_badge_premium = (168, 85, 247)    # Purple-500
    
    # Adaptive margins and spacing
    margin = 25 if is_small else 50
    
    # === HEADER CARD (Top Banner) ===
    header_height = 50 if is_small else 100
    # Draw header with gradient
    for i in range(header_height):
        ratio = i / header_height
        r = int(16 + (5 - 16) * ratio)
        g = int(185 + (150 - 185) * ratio)
        b = int(129 + (105 - 129) * ratio)
        draw.rectangle([(0, i), (width, i+1)], fill=(r, g, b))
    
    # AgriSensa branding in header
    header_text_y = 15 if is_small else 30
    draw.text((margin, header_text_y), "🌾 AgriSensa", fill=color_white, font=font_brand)
    
    # === MAIN CONTENT CARD ===
    card_top = header_height + (10 if is_small else 20)
    card_margin = 15 if is_small else 30
    
    # White card with shadow effect (multiple rectangles for shadow)
    shadow_offset = 4 if is_small else 8
    for i in range(shadow_offset, 0, -1):
        alpha = int(20 * (shadow_offset - i) / shadow_offset)
        shadow_color = (200 - alpha, 200 - alpha, 200 - alpha)
        draw.rounded_rectangle(
            [(card_margin + i, card_top + i), (width - card_margin + i, height - (15 if is_small else 30) + i)],
            radius=15 if is_small else 25,
            fill=shadow_color
        )
    
    # Main white card
    draw.rounded_rectangle(
        [(card_margin, card_top), (width - card_margin, height - (15 if is_small else 30))],
        radius=15 if is_small else 25,
        fill=color_white,
        outline=color_primary,
        width=2 if is_small else 3
    )
    
    # === LAYOUT: QR CODE + INFO ===
    content_x = card_margin + (20 if is_small else 40)
    content_y = card_top + (20 if is_small else 40)
    
    if qr_img:
        # QR Code with rounded corners effect
        # Adjust QR size based on label size and orientation
        if is_small:
            qr_size = 180  # Smaller QR for 5x5 cm
        elif is_landscape:
            qr_size = min(280, height - card_top - 100)  # Fit within height
        else:
            qr_size = 280 if "large" in size else 240
        
        qr_resized = qr_img.resize((qr_size, qr_size))
        
        # QR background card
        qr_bg_padding = 8 if is_small else 15
        draw.rounded_rectangle(
            [(content_x - qr_bg_padding, content_y - qr_bg_padding),
             (content_x + qr_size + qr_bg_padding, content_y + qr_size + qr_bg_padding)],
            radius=12 if is_small else 20,
            fill=(248, 250, 252),  # Light gray background
            outline=color_primary,
            width=2
        )
        
        label.paste(qr_resized, (content_x, content_y))
        
        # "Scan Me" text below QR (skip for very small labels)
        if not is_small:
            scan_text_y = content_y + qr_size + 10
            draw.text((content_x + qr_size//2 - 50, scan_text_y), "📱 Scan Me", 
                     fill=color_primary_dark, font=font_small)
        else:
            scan_text_y = content_y + qr_size + 5
        
        # For landscape: always put text to the right of QR
        # For square/portrait: text below QR
        if is_landscape:
            text_x = content_x + qr_size + 50
            text_y = content_y
        else:
            # Original logic for square labels
            if "large" in size and not is_landscape:
                text_x = content_x + qr_size + 50
                text_y = content_y
            else:
                text_x = content_x
                text_y = scan_text_y + (30 if is_small else 60)
    else:
        text_x = content_x
        text_y = content_y
    
    # === PRODUCT INFO (ADAPTIVE CONTENT) ===
    # Product Name (Bold, Large)
    product_name = data['produk'][:20] if is_small else (data['produk'][:28] if len(data['produk']) > 28 else data['produk'])
    draw.text((text_x, text_y), product_name, fill=color_text, font=font_title)
    text_y += 55 if is_small else 85
    
    # Varietas with accent color
    varietas_text = data['varietas'][:22] if is_small else data['varietas'][:32]
    draw.text((text_x, text_y), varietas_text, fill=color_primary_dark, font=font_subtitle)
    text_y += 38 if is_small else 55
    
    # Divider line
    divider_width = 180 if is_small else 300
    draw.rectangle([(text_x, text_y), (text_x + divider_width, text_y + 2)], fill=color_primary)
    text_y += 12 if is_small else 20
    
    # === CONDITIONAL CONTENT based on size ===
    if is_small:
        # For 5x5 cm: Show only ESSENTIAL info with larger spacing
        
        # Price (PRIORITY for small labels)
        if data.get('harga'):
            price_card_y = text_y
            draw.rounded_rectangle(
                [(text_x, price_card_y), (text_x + 200, price_card_y + 42)],
                radius=10,
                fill=color_accent,
                outline=None
            )
            draw.text((text_x + 10, price_card_y + 8), f"💰 Rp {data['harga']:,}/kg", 
                     fill=color_text, font=font_subtitle)
            text_y += 50
        
        # Date (compact)
        draw.text((text_x, text_y), f"📅 {data['tgl']}", fill=color_text_light, font=font_small)
        text_y += 28
        
        # Location only (skip farmer name to save space)
        location_short = data['lokasi'][:18] if len(data['lokasi']) > 18 else data['lokasi']
        draw.text((text_x, text_y), f"📍 {location_short}", fill=color_text, font=font_small)
        text_y += 35
        
        # Quality badges (compact, max 2)
        if data.get('klaim'):
            badge_colors = {
                'Organik': color_badge_organic,
                'Halal': color_badge_halal,
                'Premium': color_badge_premium
            }
            
            badge_x = text_x
            for badge in data['klaim'][:2]:  # Max 2 badges for small labels
                badge_color = badge_colors.get(badge, color_primary)
                badge_width = 90
                
                # Compact badge
                draw.rounded_rectangle(
                    [(badge_x, text_y), (badge_x + badge_width, text_y + 28)],
                    radius=14,
                    fill=badge_color,
                    outline=None
                )
                draw.text((badge_x + 10, text_y + 5), f"✓ {badge[:3]}", fill=color_white, font=font_tiny)
                badge_x += badge_width + 8
    else:
        # For larger labels: Show ALL information
        
        # Date with icon
        draw.text((text_x, text_y), f"📅 {data['tgl']}", fill=color_text_light, font=font_body)
        text_y += 50
        
        # Farmer info
        draw.text((text_x, text_y), f"👨‍🌾 {data['petani'][:28]}", fill=color_text, font=font_body)
        text_y += 45
        
        # Location
        draw.text((text_x, text_y), f"📍 {data['lokasi'][:30]}", fill=color_text, font=font_body)
        text_y += 55
        
        # Price (if available) - HIGHLIGHTED
        if data.get('harga'):
            # Price card
            price_card_y = text_y
            draw.rounded_rectangle(
                [(text_x, price_card_y), (text_x + 350, price_card_y + 55)],
                radius=12,
                fill=color_accent,
                outline=None
            )
            draw.text((text_x + 15, price_card_y + 12), f"💰 Rp {data['harga']:,}/kg", 
                     fill=color_text, font=font_subtitle)
            text_y += 70
        
        # Contact (if available)
        if data.get('kontak'):
            draw.text((text_x, text_y), f"📞 {data['kontak']}", fill=color_text, font=font_body)
            text_y += 55
        
        # === QUALITY BADGES (Modern Pills) ===
        if data.get('klaim'):
            text_y += 10
            badge_colors = {
                'Organik': color_badge_organic,
                'Halal': color_badge_halal,
                'Premium': color_badge_premium
            }
            
            badge_x = text_x
            for badge in data['klaim']:
                badge_color = badge_colors.get(badge, color_primary)
                badge_width = 160
                
                # Modern pill-shaped badge with shadow
                draw.rounded_rectangle(
                    [(badge_x + 2, text_y + 2), (badge_x + badge_width + 2, text_y + 47)],
                    radius=25,
                    fill=(200, 200, 200)  # Shadow
                )
                draw.rounded_rectangle(
                    [(badge_x, text_y), (badge_x + badge_width, text_y + 45)],
                    radius=25,
                    fill=badge_color,
                    outline=None
                )
                draw.text((badge_x + 20, text_y + 10), f"✓ {badge}", fill=color_white, font=font_small)
                badge_x += badge_width + 15
    
    # === FOOTER: Batch ID ===
    footer_y = height - (30 if is_small else 60)
    footer_id_text = f"ID: {data['id'][-8:]}" if is_small else f"Batch ID: {data['id']}"
    draw.text((margin + (10 if is_small else 20), footer_y), footer_id_text, 
             fill=color_text_light, font=font_tiny)
    
    # Verification badge (skip for very small labels)
    if not is_small:
        verify_text = "✓ Verified Product"
        draw.text((width - margin - 250, footer_y), verify_text, 
                 fill=color_primary, font=font_tiny)
    
    return label

def generate_qr_only(data, qr_img, size="medium"):
    """
    Generate QR code only with minimal branding
    Args:
        data: batch data dictionary
        qr_img: PIL Image of QR code
        size: "small" (5x5cm), "medium" (8x8cm), "large" (10x10cm)
    Returns:
        PIL Image object
    """
    # Size mapping for QR-only prints
    sizes = {
        "small": (590, 590),      # 5x5 cm
        "medium": (945, 945),     # 8x8 cm
        "large": (1181, 1181),    # 10x10 cm
    }
    
    width, height = sizes[size]
    
    # Create white canvas
    label = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(label)
    
    # Colors
    color_primary = (16, 185, 129)
    color_text = (31, 41, 55)
    color_white = (255, 255, 255)
    
    # Fonts
    try:
        if size == "small":
            font_brand = ImageFont.truetype("arialbd.ttf", 28)
            font_small = ImageFont.truetype("arial.ttf", 22)
        elif size == "medium":
            font_brand = ImageFont.truetype("arialbd.ttf", 36)
            font_small = ImageFont.truetype("arial.ttf", 28)
        else:
            font_brand = ImageFont.truetype("arialbd.ttf", 42)
            font_small = ImageFont.truetype("arial.ttf", 32)
    except:
        font_brand = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Calculate QR size (80% of canvas)
    qr_size = int(width * 0.7)
    qr_resized = qr_img.resize((qr_size, qr_size))
    
    # Center QR code
    qr_x = (width - qr_size) // 2
    qr_y = (height - qr_size) // 2 - 30
    
    # Draw subtle border
    border_padding = 20
    draw.rounded_rectangle(
        [(qr_x - border_padding, qr_y - border_padding),
         (qr_x + qr_size + border_padding, qr_y + qr_size + border_padding)],
        radius=15,
        outline=color_primary,
        width=3
    )
    
    # Paste QR
    label.paste(qr_resized, (qr_x, qr_y))
    
    # Top branding
    brand_text = "🌾 AgriSensa"
    bbox = draw.textbbox((0, 0), brand_text, font=font_brand)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, 30), brand_text, fill=color_primary, font=font_brand)
    
    # Bottom text
    scan_text = "Scan untuk info produk"
    bbox = draw.textbbox((0, 0), scan_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, qr_y + qr_size + 35), scan_text, fill=color_text, font=font_small)
    
    # Batch ID at bottom
    id_text = f"ID: {data['id']}"
    bbox = draw.textbbox((0, 0), id_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    draw.text(((width - text_width) // 2, height - 50), id_text, fill=color_text, font=font_small)
    
    return label

def pil_to_pdf_bytes(pil_image):
    """Convert PIL Image to PDF bytes"""
    pdf_buffer = io.BytesIO()
    pil_image.save(pdf_buffer, format='PDF', resolution=300.0)
    pdf_buffer.seek(0)
    return pdf_buffer.getvalue()

# TABS
tab1, tab2, tab3 = st.tabs(["📝 Input Data Batch (Produksi)", "🖨️ Cetak Label", "📱 Simulasi Scan Konsumen"])

# --- TAB 1: INPUT BATCH ---
with tab1:
    col_in1, col_in2 = st.columns([1, 1])
    
    with col_in1:
        st.subheader("1. Identitas Produk")
        
        # Extended Commodity Options
        opsi_komoditas = [
            "Beras (Pandan Wangi/Rojolele)", "Beras Merah/Hitam", 
            "Kopi Arabika", "Kopi Robusta", "Kakao (Cokelat)",
            "Cabai Rawit", "Cabai Merah", "Bawang Merah", "Bawang Putih",
            "Sayuran Daun (Bayam/Kangkung)", "Selada Hidroponik", "Tomat Cherry",
            "Melon Premium", "Semangka", "Mangga", "Durian", "Alpukat",
            "Telur Ayam Kampung", "Madu Murni", "Ikan Nila", "Ikan Lele",
            "Lainnya (Ketik Manual)..."
        ]
        
        pilihan_awal = st.selectbox("Pilih Komoditas", opsi_komoditas)
        
        if pilihan_awal == "Lainnya (Ketik Manual)...":
            jenis_produk = st.text_input("✍️ Masukkan Nama Komoditas", placeholder="Contoh: Vanili Eksport")
            if not jenis_produk:
                jenis_produk = "Produk Tanpa Nama"
        else:
            jenis_produk = pilihan_awal
        varietas = st.text_input("Varietas / Grade", "Cianjur Pandan Wangi (Grade A)")
        tgl_panen = st.date_input("Tanggal Panen", datetime.date.today())
        
        st.subheader("2. Asal Usul (Origin)")
        nama_petani = st.text_input("Nama Petani / Kelompok", "Gapoktan Sejahtera")
        lokasi_kebun = st.text_input("Lokasi Kebun", "Banyumas, Jawa Tengah")
        
        # Photo Upload
        foto_produk = st.file_uploader("Foto Petani / Kebun (Opsional)", type=['jpg', 'jpeg', 'png'])
        
    with col_in2:
        st.subheader("3. Informasi Komersial")
        
        # Price Input
        harga_produk = st.number_input(
            "💰 Harga per Kg/Unit (Rp)", 
            min_value=0, 
            value=50000, 
            step=1000,
            help="Harga jual produk yang akan ditampilkan di label"
        )
        
        # Contact Input
        kontak_petani = st.text_input(
            "📞 Nomor Kontak (WhatsApp/Telp)",
            placeholder="Contoh: 0812-3456-7890",
            help="Nomor yang bisa dihubungi pembeli"
        )
        
        st.subheader("4. Klaim Kualitas")
        is_organik = st.checkbox("✅ Bebas Pestisida / Organik")
        is_halal = st.checkbox("✅ Halal Certified")
        is_premium = st.checkbox("✅ Kualitas Ekspor (Sortir Ketat)")
        
        st.subheader("5. Riwayat Budidaya & Milestones (Advanced)")
        riwayat_log = st.text_area("📝 Catatan Budidaya", "Pupuk Organik Cair (Minggu 2), Kompos (Minggu 4).")
        
        # --- NEW: ADVANCED FEATURES ---
        # --- NEW: ADVANCED FEATURES (MANUAL INPUT) ---
        with st.expander("🌍 Climate Proof & Digital Journey (Input Manual)", expanded=True):
            st.info("Masukkan data iklim dan jam panen secara manual (Mode Standalone).")
            
            # 1. Climate Inputs
            st.markdown("**1. Data Iklim Mikro (Rata-rata)**")
            c_clim1, c_clim2, c_clim3 = st.columns(3)
            with c_clim1:
                avg_temp = st.number_input("Suhu (°C)", value=24.5, step=0.1, format="%.1f")
            with c_clim2:
                avg_hum = st.number_input("Kelembaban (%)", value=75, step=1)
            with c_clim3:
                sun_hours = st.number_input("Penyinaran (Jam)", value=11.5, step=0.5)

            climate_proof = {
                "avg_temp": avg_temp, 
                "avg_hum": avg_hum,
                "sun_hours": sun_hours,
                "rainfall": 1200 # Static for now or add input if needed
            }
            
            st.divider()
            
            # 2. Key Milestones Inputs
            st.markdown("**2. Waktu Milestone Utama**")
            c_mil1, c_mil2, c_mil3 = st.columns(3)
            with c_mil1:
                t_harvest = st.time_input("Jam Panen", datetime.time(8, 30))
            with c_mil2:
                t_qc = st.time_input("Jam Sortir/QC", datetime.time(10, 15))
            with c_mil3:
                t_pack = st.time_input("Jam Packing", datetime.time(13, 00))
            
            # Construct Milestones from Inputs
            date_str = tgl_panen.strftime("%Y-%m-%d")
            milestones = [
                {"date": date_str, "time": t_harvest.strftime("%H:%M"), "event": "Panen (Harvesting)", "loc": lokasi_kebun, "icon": "🌾"},
                {"date": date_str, "time": t_qc.strftime("%H:%M"), "event": "Sortir & Grading (QC 1)", "loc": "Gudang Sortir", "icon": "🔍"},
                {"date": date_str, "time": t_pack.strftime("%H:%M"), "event": "Packaging & Labeling", "loc": "Processing House", "icon": "📦"}
            ]
            st.caption("✅ Milestone akan otomatis digenerate berdasarkan jam di atas.")

        # Generator ID & Blockchain Fake Hash
        import hashlib
        import json
        batch_id = f"AGRI-{tgl_panen.strftime('%Y%m%d')}-{hash(jenis_produk)%1000:03d}"
        
        # Hash includes advanced data now
        data_string = f"{batch_id}{json.dumps(climate_proof)}{json.dumps(milestones)}{nama_petani}"
        blockchain_hash = hashlib.sha256(data_string.encode()).hexdigest()
        
        st.markdown("---")
        if st.button("💾 Simpan & Generate Passport 2.0", type="primary", use_container_width=True):
            st.session_state['batch_data'] = {
                "id": batch_id,
                "hash": blockchain_hash,
                "produk": jenis_produk,
                "varietas": varietas,
                "tgl": tgl_panen,
                "petani": nama_petani,
                "lokasi": lokasi_kebun,
                "foto": foto_produk,
                "harga": harga_produk if harga_produk > 0 else None,
                "kontak": kontak_petani if kontak_petani else None,
                "riwayat": riwayat_log,
                "climate": climate_proof,
                "milestones": milestones,
                "klaim": [k for k, v in [("Organik", is_organik), ("Halal", is_halal), ("Premium", is_premium)] if v]
            }
            st.success(f"✅ Batch {batch_id} berhasil dibuat dengan Advanced Traceability!")
            st.info("📌 Silakan ke tab **'📱 Simulasi Scan Konsumen'** untuk melihat Journey Timeline!")

# --- TAB 2: PRINT LABEL ---
with tab2:
    st.subheader("🖨️ Generator Label Siap Cetak")
    
    if st.session_state['batch_data']:
        data = st.session_state['batch_data']
        
        # Print Type Selection
        st.markdown("### 1️⃣ Pilih Jenis Cetakan")
        col_type1, col_type2 = st.columns(2)
        
        with col_type1:
            print_type = st.radio(
                "Jenis Cetakan:",
                ["label_lengkap", "qr_only"],
                format_func=lambda x: {
                    "label_lengkap": "📋 Label Lengkap (dengan info produk)",
                    "qr_only": "📱 QR Code Saja (minimalis)"
                }[x],
                help="Pilih apakah ingin mencetak label lengkap atau hanya QR code"
            )
        
        with col_type2:
            if print_type == "label_lengkap":
                st.info("💡 **Label Lengkap** cocok untuk kemasan produk retail yang membutuhkan info detail")
            else:
                st.success("✅ **QR Only** cocok untuk produk yang sudah punya kemasan, tinggal tempel QR")
        
        st.markdown("---")
        st.markdown("### 2️⃣ Pilih Ukuran")
        
        # Size Selection (different options based on print type)
        col_size, col_opt = st.columns([1, 2])
        
        with col_size:
            if print_type == "label_lengkap":
                label_size = st.selectbox(
                    "Ukuran & Orientasi Label",
                    ["medium_landscape", "large_landscape", "small_landscape", "medium", "large", "small"],
                    index=0,  # Default to medium landscape
                    format_func=lambda x: {
                        # Landscape (RECOMMENDED)
                        "small_landscape": "🏞️ Landscape Kecil (10x5 cm) ⭐ Compact",
                        "medium_landscape": "🏞️ Landscape Sedang (15x10 cm) ⭐ RECOMMENDED",
                        "large_landscape": "🏞️ Landscape Besar (20x10 cm) ⭐ Premium",
                        # Square/Portrait
                        "small": "⬜ Square Kecil (5x5 cm)",
                        "medium": "⬜ Square Sedang (10x10 cm)",
                        "large": "⬜ Wide (15x10 cm)"
                    }[x]
                )
            else:
                # QR Only sizes
                qr_size = st.selectbox(
                    "Ukuran QR Code",
                    ["medium", "large", "small"],
                    index=0,
                    format_func=lambda x: {
                        "small": "📱 Kecil (5x5 cm)",
                        "medium": "📱 Sedang (8x8 cm) ⭐ RECOMMENDED",
                        "large": "📱 Besar (10x10 cm)"
                    }[x]
                )
        
        with col_opt:
            if print_type == "label_lengkap":
                if "landscape" in label_size:
                    st.success("✅ **Landscape** - Format horizontal lebih cocok untuk kemasan produk!")
                else:
                    st.info("💡 **Tip:** Coba format Landscape untuk hasil lebih profesional!")
            else:
                st.info("💡 QR Code akan dicetak dengan branding minimal AgriSensa")
        
        # Generate QR Code - NOW USES VERCEL URL!
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        
        # Build Vercel Product Passport URL
        # Build Vercel Product Passport URL
        import urllib.parse
        import json
        
        base_url = "https://vercel-scan2.vercel.app/product"
        # Payload construction for Base64 (Minified for compact QR)
        payload = {
            'id': data['id'],
            'n': data['produk'],                 # name
            'v': data['varietas'],               # variety
            'f': data['petani'],                 # farmer
            'l': data['lokasi'],                 # location
            'd': str(data['tgl']),               # date
            'w': f"{data.get('berat', 1)} kg",   # weight
            'e': '🌾',                           # emoji
            'p': str(data['harga']) if data.get('harga') else None, # price
            # Climate: t=temp, h=hum, s=sun
            'c': {
                't': str(data.get('climate', {}).get('avg_temp', '')),
                'h': str(data.get('climate', {}).get('avg_hum', '')),
                's': str(data.get('climate', {}).get('sun_hours', ''))
            },
            # Milestones: m
            'm': data.get('milestones', [])
        }
        
        # Encode to URL-Safe Base64 (Strip Padding for Cleaner URL)
        import base64
        json_str = json.dumps(payload, separators=(',', ':'))
        b64_str = base64.urlsafe_b64encode(json_str.encode()).decode().rstrip("=")
        
        # Final Robust URL
        qr_url = f"{base_url}/{b64_str}"
        
        # DEBUG: Show URL to User
        st.caption("🔗 **Debug Link:** " + qr_url)
        
        # Generate QR Code
        qr = qrcode.QRCode(
            version=None, 
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10, 
            border=4
        )
        qr.add_data(qr_url)
        qr.make(fit=True)
        img_qr = qr.make_image(fill_color="black", back_color="white")

        
        # Generate Image based on print type
        if print_type == "label_lengkap":
            label_image = generate_printable_label(data, label_size, img_qr)
            filename_prefix = f"Label_{data['id']}_{label_size}"
        else:
            label_image = generate_qr_only(data, img_qr, qr_size)
            filename_prefix = f"QR_{data['id']}_{qr_size}"
        
        # Convert to bytes for display and download
        label_buffer = io.BytesIO()
        label_image.save(label_buffer, format='PNG', dpi=(300, 300))
        label_bytes = label_buffer.getvalue()
        
        # Preview
        st.markdown("---")
        st.markdown("### 3️⃣ Preview")
        st.caption(f"🔍 Preview {print_type.replace('_', ' ').title()}:")
        
        col_prev1, col_prev2, col_prev3 = st.columns([1, 2, 1])
        with col_prev2:
            st.image(label_bytes, use_container_width=True)
        
        # Action Buttons
        st.markdown("---")
        st.markdown("### 4️⃣ Download / Print")
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            st.download_button(
                "⬇️ Download PNG",
                label_bytes,
                f"{filename_prefix}.png",
                "image/png",
                use_container_width=True
            )
        
        with col_btn2:
            # Generate PDF
            pdf_bytes = pil_to_pdf_bytes(label_image)
            st.download_button(
                "📄 Download PDF",
                pdf_bytes,
                f"{filename_prefix}.pdf",
                "application/pdf",
                use_container_width=True
            )
        
        with col_btn3:
            # Print button with JavaScript
            if st.button("🖨️ Print Langsung", use_container_width=True):
                # Encode image to base64 for embedding
                img_base64 = base64.b64encode(label_bytes).decode()
                
                # JavaScript to open print dialog
                print_js = f"""
                <script>
                    function printLabel() {{
                        var printWindow = window.open('', '', 'height=800,width=800');
                        printWindow.document.write('<html><head><title>Print Label</title>');
                        printWindow.document.write('<style>@media print {{ @page {{ margin: 0; }} body {{ margin: 0; }} }}</style>');
                        printWindow.document.write('</head><body>');
                        printWindow.document.write('<img src="data:image/png;base64,{img_base64}" style="width:100%; height:auto;">');
                        printWindow.document.write('</body></html>');
                        printWindow.document.close();
                        printWindow.focus();
                        setTimeout(function() {{ printWindow.print(); }}, 250);
                    }}
                    printLabel();
                </script>
                """
                st.components.v1.html(print_js, height=0)
                st.success("✅ Dialog print akan muncul. Pastikan printer Anda sudah siap!")
        
        st.markdown("---")
        st.success("✅ **Label siap cetak!** Gunakan kertas stiker atau print di kertas biasa lalu tempel dengan lem.")
        
    else:
        st.warning("⚠️ Belum ada data batch. Silakan input data di **Tab 1** terlebih dahulu.")

# --- TAB 3: CONSUMER VIEW ---
with tab3:
    st.markdown("### 📱 Tampilan di HP Konsumen")
    st.info("Ini yang dilihat pembeli saat men-scan QR Code Anda.")
    
    if st.session_state['batch_data']:
        data = st.session_state['batch_data']
        
        # Simulation of Mobile View (Narrow container)
        c_mob1, c_mob2, c_mob3 = st.columns([1.5, 2, 1.5])
        
        with c_mob2:
            # Build HTML content
            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; background-color: #f8fafc; }}
    </style>
</head>
<body>
<div style='max-width: 400px; margin: 0 auto; background-color: white; min-height: 100vh; box-shadow: 0 0 20px rgba(0,0,0,0.1); overflow: hidden;'>
    
    <!-- HEADER -->
    <div style='background-color: #0f766e; color: white; padding: 20px 20px 40px 20px; border-bottom-left-radius: 30px; border-bottom-right-radius: 30px; text-align: center;'>
        <div style='font-size: 0.8em; opacity: 0.9;'>✅ TERVERIFIKASI BLOCKCHAIN</div>
        <h1 style='margin: 10px 0 5px 0; font-size: 1.8em;'>{data['produk']}</h1>
        <div style='font-size: 1.1em; opacity: 0.9;'>{data['varietas']}</div>
    </div>
    
    <div style='padding: 20px; margin-top: -30px;'>
"""
            
            # PHOTO
            if data.get('foto'):
                foto_base64 = base64.b64encode(data['foto'].getvalue()).decode()
                html_content += f"""
        <div style='background: white; padding: 5px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 20px;'>
            <img src='data:image/png;base64,{foto_base64}' style='width:100%; border-radius:10px; display: block;'>
        </div>
"""
            
            # MAIN INFO CARD
            html_content += f"""
        <div style='background: white; border-radius: 15px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e2e8f0;'>
            <h3 style='margin: 0 0 15px 0; color: #0f766e; border-bottom: 2px solid #f0fdf4; padding-bottom: 10px;'>📦 Informasi Produk</h3>
            
            <div style='margin-bottom: 12px;'>
                <div style='font-size: 0.8em; color: #64748b;'>🗓️ Tanggal Panen</div>
                <div style='font-weight: 600; color: #334155;'>{str(data['tgl'])}</div>
            </div>
            
            <div style='margin-bottom: 12px;'>
                <div style='font-size: 0.8em; color: #64748b;'>📍 Lokasi Kebun</div>
                <div style='font-weight: 600; color: #334155;'>{data['lokasi']}</div>
            </div>
            
            <div style='margin-bottom: 12px;'>
                <div style='font-size: 0.8em; color: #64748b;'>👨‍🌾 Petani</div>
                <div style='font-weight: 600; color: #334155;'>{data['petani']}</div>
            </div>
"""
            if data.get('harga'):
                html_content += f"""
            <div style='margin-top: 15px; padding-top: 15px; border-top: 1px dashed #cbd5e1;'>
                <div style='font-size: 0.8em; color: #64748b;'>💰 Harga Referensi</div>
                <div style='font-weight: bold; color: #059669; font-size: 1.2em;'>Rp {data['harga']:,} <span style='font-size:0.7em; color:#64748b;'>/kg</span></div>
            </div>
"""
            html_content += "</div>" # Close Info Card

            # CLIMATE PROOF
            if data.get('climate'):
                clim = data['climate']
                html_content += f"""
        <div style='background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border-radius: 15px; padding: 20px; margin-bottom: 15px; border: 1px solid #fcd34d;'>
            <h3 style='margin: 0 0 15px 0; color: #92400e; font-size: 1.1em;'>🌍 Climate Proof (Bukti Iklim)</h3>
            <div style='display:flex; justify-content:space-between; text-align: center;'>
                <div style='background: rgba(255,255,255,0.5); padding: 8px; border-radius: 10px; width: 30%;'>
                    <div style='font-size: 1.5em;'>🌡️</div>
                    <div style='font-weight: bold; color: #92400e;'>{clim['avg_temp']}°C</div>
                    <div style='font-size: 0.7em; color: #b45309;'>Avg Temp</div>
                </div>
                <div style='background: rgba(255,255,255,0.5); padding: 8px; border-radius: 10px; width: 30%;'>
                    <div style='font-size: 1.5em;'>💧</div>
                    <div style='font-weight: bold; color: #92400e;'>{clim['avg_hum']}%</div>
                    <div style='font-size: 0.7em; color: #b45309;'>Humidity</div>
                </div>
                <div style='background: rgba(255,255,255,0.5); padding: 8px; border-radius: 10px; width: 30%;'>
                    <div style='font-size: 1.5em;'>☀️</div>
                    <div style='font-weight: bold; color: #92400e;'>{clim['sun_hours']}h</div>
                    <div style='font-size: 0.7em; color: #b45309;'>Sun/Day</div>
                </div>
            </div>
        </div>
"""

            # JOURNEY TIMELINE
            if data.get('milestones'):
                html_content += f"""
        <div style='background: white; border-radius: 15px; padding: 20px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 15px; border: 1px solid #e2e8f0;'>
            <h3 style='margin: 0 0 20px 0; color: #0f766e;'>🚚 Perjalanan Produk</h3>
            <div style='position: relative; padding-left: 20px; border-left: 2px solid #e2e8f0; margin-left: 10px;'>
"""
                for m in data['milestones']:
                    html_content += f"""
                <div style='margin-bottom: 25px; position: relative;'>
                    <div style='position: absolute; left: -27px; top: 0; background: #10b981; color: white; width: 12px; height: 12px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 0 2px #10b981;'></div>
                    <div style='font-weight: bold; color: #334155; font-size: 0.95em;'>{m['event']} {m['icon']}</div>
                    <div style='font-size: 0.8em; color: #64748b; margin-top: 2px;'>{m['date']} • {m['time']}</div>
                    <div style='font-size: 0.8em; color: #64748b;'>📍 {m['loc']}</div>
                </div>
"""
                html_content += """
            </div>
        </div>
"""

            # STORY & HISTORY
            html_content += f"""
        <div style='background: #f8fafc; border-radius: 15px; padding: 15px; border: 1px dashed #cbd5e1; margin-bottom: 20px;'>
            <div style='font-weight: bold; color: #475569; margin-bottom: 5px;'>📝 Catatan Budidaya:</div>
            <div style='font-style: italic; color: #64748b; font-size: 0.9em;'>"{data.get('riwayat', '-')}"</div>
        </div>
        
        <div style='text-align: center; margin-top: 30px; margin-bottom: 20px;'>
            <div style='font-size: 0.7em; color: #94a3b8; margin-bottom: 5px;'>ID BATCH: {data['id']}</div>
            <div style='font-size: 0.7em; color: #94a3b8;'>Hash: {data.get('hash', '')[:16]}...</div>
            <div style='margin-top: 10px; font-weight: bold; color: #cbd5e1;'>POWERED BY AGRISENSA</div>
        </div>

    </div> <!-- End Padding -->
</div> <!-- End Container -->
</body>
</html>
"""
            
            components.html(html_content, height=800, scrolling=True)

    else:
        st.warning("⚠️ Belum ada data batch. Silakan input data di **Tab 1** terlebih dahulu.")
