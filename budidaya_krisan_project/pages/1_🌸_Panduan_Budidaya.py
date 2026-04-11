# 🌸 Panduan Budidaya Krisan Spray Jepang
# SOP Lengkap dari Hulu hingga Hilir

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Panduan Budidaya Krisan",
    page_icon="🌸",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #ec4899 0%, #f472b6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sop-card {
        background: linear-gradient(135deg, rgba(252, 231, 243, 0.8) 0%, rgba(255, 255, 255, 0.9) 100%);
        border: 1px solid rgba(236, 72, 153, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .phase-title {
        color: #be185d;
        font-weight: 700;
        font-size: 1.2rem;
        border-bottom: 2px solid #f9a8d4;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .timeline-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        background: #fce7f3;
        border-radius: 20px;
        font-size: 0.8rem;
        color: #be185d;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🌸 Panduan Budidaya Krisan Spray Jepang</h1>
    <p>SOP Lengkap dari Hulu hingga Hilir | Berbasis Riset & Praktik Petani</p>
</div>
""", unsafe_allow_html=True)

# ========== DATABASE VARIETAS ==========
KRISAN_VARIETIES = {
    "Krisan Spray Putih": {
        "emoji": "🤍",
        "color_code": "#ffffff",
        "market_price_min": 8000,
        "market_price_max": 15000,
        "demand": "Tinggi - Wedding, duka cita, formal",
        "vase_life": "10-14 hari",
        "characteristics": "Bunga spray dengan banyak kuntum, diameter 4-6 cm per kuntum",
        "best_season": "Sepanjang tahun, peak Desember-Februari"
    },
    "Krisan Spray Pink": {
        "emoji": "💗",
        "color_code": "#ec4899",
        "market_price_min": 10000,
        "market_price_max": 18000,
        "demand": "Sangat Tinggi - Valentine, ulang tahun, romantis",
        "vase_life": "12-16 hari",
        "characteristics": "Warna cerah, favorit florist, multi-kuntum",
        "best_season": "Peak Februari (Valentine), Mei (Mother's Day)"
    },
    "Krisan Spray Kuning": {
        "emoji": "💛",
        "color_code": "#fbbf24",
        "market_price_min": 8000,
        "market_price_max": 14000,
        "demand": "Tinggi - Imlek, dekorasi, cheerful occasion",
        "vase_life": "10-14 hari",
        "characteristics": "Warna cheerful, cocok rangkaian tropikal",
        "best_season": "Peak Januari-Februari (Imlek)"
    }
}

# ========== TABS ==========
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
    "📋 Database Varietas",
    "🌱 Persiapan & Stek",
    "🌿 Fase Vegetatif",
    "🌸 Fase Generatif",
    "💡 Pengaturan Cahaya",
    "🧪 Pemupukan",
    "📅 Timeline Lengkap",
    "🔥 Manajemen Suhu Musim Dingin"
])

# TAB 1: Database Varietas
with tab1:
    st.subheader("📋 Database Varietas Krisan Spray Jepang")
    st.info("Krisan Spray Jepang terkenal dengan kualitas bunga yang tahan lama dan banyak kuntum per tangkai.")
    
    for name, data in KRISAN_VARIETIES.items():
        with st.expander(f"{data['emoji']} {name}", expanded=True):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="background: {data['color_code']}; 
                            width: 100px; height: 100px; 
                            border-radius: 50%; 
                            border: 3px solid #e5e7eb;
                            margin: 0 auto;"></div>
                """, unsafe_allow_html=True)
                st.metric("Harga Pasar", f"Rp {data['market_price_min']:,}-{data['market_price_max']:,}/tangkai")
            
            with col2:
                st.markdown(f"**Karakteristik:** {data['characteristics']}")
                st.markdown(f"**Permintaan:** {data['demand']}")
                st.markdown(f"**Vase Life:** {data['vase_life']}")
                st.markdown(f"**Musim Peak:** {data['best_season']}")

# TAB 2: Persiapan & Stek
with tab2:
    st.subheader("🌱 Fase 1: Persiapan Lahan & Stek")
    st.markdown('<span class="timeline-badge">📅 Hari 0 - 21</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">🏗️ A. Persiapan Greenhouse & Bedengan</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Syarat Lokasi:**
        - Ketinggian: **800 - 1.500 mdpl** (ideal 1.000-1.200 mdpl)
        - Suhu: 18-24°C siang, 15-18°C malam
        - Intensitas cahaya: 40.000-60.000 lux
        - Tersedia sumber air bersih
        
        **2. Konstruksi Greenhouse:**
        - Tipe: Tunnel atau multispan
        - Tinggi: minimal 4 meter
        - Material: Plastik UV 14% atau paranet
        - Ventilasi samping yang bisa dibuka-tutup
        """)
    
    with col2:
        st.markdown("""
        **3. Persiapan Bedengan:**
        - Lebar: 100-120 cm
        - Tinggi: 20-30 cm
        - Jarak antar bedengan: 40-50 cm
        - Sterilisasi tanah: fumigasi atau solarisasi 2-3 minggu
        
        **4. Media Tanam:**
        - Tanah : Sekam bakar : Pupuk kandang = 2:1:1
        - pH optimal: 6.0 - 6.5
        - EC: 1.5 - 2.5 mS/cm
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">✂️ B. Persiapan Stek (Cutting)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    | Parameter | Standar |
    |-----------|---------|
    | Sumber stek | Tanaman induk sehat, bebas virus |
    | Panjang stek | 5-7 cm dengan 3-4 daun |
    | Diameter batang | 3-5 mm |
    | Pemotongan | Gunakan pisau tajam, steril |
    | Hormon akar | IBA 1000-2000 ppm (celup 5 detik) |
    | Media rooting | Pasir steril atau rockwool |
    | Waktu rooting | 14-21 hari |
    | Kelembaban | 85-95% (gunakan misting) |
    """)
    
    st.success("✅ **Target:** Stek berakar dengan akar 3-5 cm, siap dipindah ke bedengan produksi.")

# TAB 3: Fase Vegetatif
with tab3:
    st.subheader("🌿 Fase 2: Pertumbuhan Vegetatif")
    st.markdown('<span class="timeline-badge">📅 Hari 21 - 49 (4 minggu)</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">🌱 Transplanting & Pemeliharaan Vegetatif</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Pindah Tanam (Transplanting):**
        - Waktu: Sore hari (hindari terik)
        - Jarak tanam: 12.5 x 12.5 cm (64 tanaman/m²)
        - Kedalaman: 2-3 cm
        - Siram segera setelah tanam
        
        **2. Pencahayaan Fase Vegetatif:**
        - **PENTING:** Berikan hari panjang (Long Day)
        - Durasi: **16-18 jam cahaya/hari**
        - Gunakan lampu TL/LED 100-150 lux
        - Penyinaran malam: 22.00 - 02.00 WIB
        """)
    
    with col2:
        st.markdown("""
        **3. Pemeliharaan:**
        - Penyiraman: 2x sehari (pagi & sore)
        - EC nutrisi: 1.5-2.0 mS/cm
        - Pinching (potong pucuk): Minggu ke-2 setelah tanam
        - Jumlah cabang dipertahankan: 3-4 cabang/tanaman
        
        **4. Target Vegetatif:**
        - Tinggi tanaman: 25-30 cm
        - Jumlah daun: 15-20 helai
        - Batang kokoh, hijau tua
        """)
    
    st.warning("⚠️ **Kritis:** Fase vegetatif menentukan jumlah cabang produktif. Pinching yang tepat menghasilkan banyak kuntum bunga!")
    
    # Visualization: Pinching diagram
    st.markdown("### 📐 Teknik Pinching")
    st.image("https://via.placeholder.com/600x200/fce7f3/be185d?text=Diagram+Pinching+Krisan", 
             caption="Ilustrasi: Potong pucuk utama untuk merangsang cabang lateral", 
             use_container_width=True) if False else st.info("💡 Potong pucuk utama menyisakan 4-5 ruas untuk menghasilkan 3-4 cabang produktif.")

# TAB 4: Fase Generatif
with tab4:
    st.subheader("🌸 Fase 3: Pembungaan (Generatif)")
    st.markdown('<span class="timeline-badge">📅 Hari 49 - 105 (8 minggu)</span>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">💡 Induksi Pembungaan dengan Hari Pendek</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.error("🔴 **KRITIS:** Krisan adalah tanaman **short day plant**. Pembungaan HANYA terjadi jika hari pendek (<12 jam cahaya)!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Induksi Hari Pendek (Short Day):**
        - Durasi cahaya: **10-11 jam/hari MAKSIMAL**
        - Metode: Penutupan dengan plastik hitam
        - Waktu tutup: 17.00 - 07.00 WIB (14 jam gelap)
        - Lakukan KONSISTEN selama 8 minggu
        
        **2. Timeline Pembungaan:**
        - Minggu 1-2: Inisiasi tunas bunga
        - Minggu 3-4: Kuncup mulai terlihat
        - Minggu 5-6: Kuncup membesar
        - Minggu 7-8: Bunga mulai mekar
        """)
    
    with col2:
        st.markdown("""
        **3. Parameter Lingkungan:**
        - Suhu siang: 20-24°C
        - Suhu malam: 15-18°C (PENTING untuk warna)
        - Kelembaban: 60-70%
        - EC nutrisi: 2.0-2.5 mS/cm
        
        **4. Peningkatan Kualitas Bunga:**
        - Kurangi N, tingkatkan K di minggu ke-6
        - Suhu malam rendah → warna lebih intens
        - Jaga konsistensi tutup plastik hitam
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">🎯 Disbudding (Pembuangan Kuncup Samping)</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    Untuk krisan **spray**, TIDAK perlu disbudding karena kita ingin banyak kuntum per tangkai.
    
    Tetapi untuk krisan **standard** (satu bunga besar), lakukan disbudding:
    - Buang semua kuncup samping, sisakan hanya kuncup terminal
    - Lakukan saat kuncup masih kecil (<5mm)
    """)

# TAB 5: Pengaturan Cahaya
with tab5:
    st.subheader("💡 Pengaturan Photoperiod (Hari Panjang vs Pendek)")
    
    st.info("""
    **Konsep Dasar:**
    - Krisan adalah **Short Day Plant** (SDP)
    - Vegetatif membutuhkan **hari panjang** (>14 jam cahaya)
    - Pembungaan membutuhkan **hari pendek** (<12 jam cahaya)
    - Di Indonesia (dekat ekuator), hari alami ~12 jam → perlu manipulasi!
    """)
    
    # Timeline visualization
    st.markdown("### 📊 Jadwal Photoperiod")
    
    schedule_data = {
        "Minggu": list(range(1, 16)),
        "Fase": ["Rooting"]*3 + ["Vegetatif"]*4 + ["Generatif"]*8,
        "Jam Cahaya": [16]*3 + [16]*4 + [10]*8,
        "Perlakuan": ["Lampu malam"]*3 + ["Lampu malam"]*4 + ["Tutup plastik hitam"]*8
    }
    
    df = pd.DataFrame(schedule_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df["Minggu"],
        y=df["Jam Cahaya"],
        marker_color=['#86efac' if x >= 14 else '#f472b6' for x in df["Jam Cahaya"]],
        text=df["Jam Cahaya"].astype(str) + " jam",
        textposition='outside'
    ))
    
    fig.update_layout(
        title="Durasi Cahaya per Minggu",
        xaxis_title="Minggu ke-",
        yaxis_title="Jam Cahaya/Hari",
        yaxis_range=[0, 20],
        height=400,
        showlegend=False
    )
    
    fig.add_hline(y=12, line_dash="dash", line_color="red", 
                  annotation_text="Batas Kritis (12 jam)")
    
    st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🌙 Teknik Perpanjangan Hari (Long Day)
        **Tujuan:** Memperpanjang fase vegetatif
        
        **Metode:**
        1. Pasang lampu di atas bedengan (tinggi 2m)
        2. Jenis lampu: LED putih atau TL 40W
        3. Intensitas: 100-150 lux
        4. Jadwal: 22.00 - 02.00 WIB (4 jam tambahan)
        5. Jarak lampu: setiap 2-3 meter
        """)
    
    with col2:
        st.markdown("""
        ### 🌑 Teknik Hari Pendek (Short Day)
        **Tujuan:** Memicu pembungaan
        
        **Metode:**
        1. Gunakan plastik hitam 0.3-0.5 mm
        2. Konstruksi: Rangka besi/bambu + plastik
        3. Tutup: 17.00 WIB (sebelum matahari terbenam)
        4. Buka: 07.00 WIB (setelah matahari terbit)
        5. Wajib konsisten setiap hari!
        """)

# TAB 6: Pemupukan
with tab6:
    st.subheader("🧪 Program Pemupukan Krisan Spray")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">📊 Kebutuhan Nutrisi per Fase</div>
    </div>
    """, unsafe_allow_html=True)
    
    fertilizer_program = pd.DataFrame({
        "Fase": ["Rooting (0-3 minggu)", "Vegetatif Awal (3-5 minggu)", 
                 "Vegetatif Akhir (5-7 minggu)", "Generatif Awal (7-11 minggu)",
                 "Generatif Akhir (11-15 minggu)"],
        "N-P-K Ratio": ["10-52-10", "20-10-20", "15-10-30", "10-10-30", "5-10-40"],
        "EC (mS/cm)": ["0.8-1.0", "1.5-1.8", "1.8-2.0", "2.0-2.2", "2.0-2.5"],
        "Frekuensi": ["1x/minggu", "2x/minggu", "2x/minggu", "3x/minggu", "3x/minggu"],
        "Catatan": [
            "Fokus akar, P tinggi",
            "Dorong pertumbuhan vegetatif",
            "Transisi ke K tinggi",
            "Pembentukan bunga",
            "Kualitas & warna bunga"
        ]
    })
    
    st.dataframe(fertilizer_program, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### 🧪 Contoh Formulasi Pupuk")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Fase Vegetatif:**
        - NPK 20-10-20: 2 g/L
        - Kalsium Nitrat: 1 g/L
        - MgSO4: 0.5 g/L
        - Mikro: sesuai label
        """)
    
    with col2:
        st.markdown("""
        **Fase Generatif:**
        - NPK 10-10-30: 2 g/L
        - KNO3: 1 g/L
        - MgSO4: 0.5 g/L
        - Boron: 0.1 g/L
        """)
    
    with col3:
        st.markdown("""
        **Finishing:**
        - KCl / K2SO4: 2 g/L
        - Kalsium: 0.5 g/L
        - Kurangi N drastis
        - Fokus warna & kekerasan
        """)
    
    st.warning("⚠️ **Penting:** Selalu cek pH larutan (6.0-6.5) dan EC sebelum aplikasi!")

# TAB 7: Timeline Lengkap
with tab7:
    st.subheader("📅 Timeline Lengkap Budidaya Krisan Spray")
    
    st.info("Total durasi: **105-120 hari** dari stek hingga panen")
    
    # Interactive timeline
    timeline_data = [
        {"Minggu": "0-3", "Hari": "0-21", "Fase": "Rooting", "Aktivitas": "Persiapan stek, pembentukan akar", "Warna": "#86efac"},
        {"Minggu": "3-4", "Hari": "21-28", "Fase": "Transplanting", "Aktivitas": "Pindah tanam ke bedengan produksi", "Warna": "#4ade80"},
        {"Minggu": "4-5", "Hari": "28-35", "Fase": "Vegetatif 1", "Aktivitas": "Pinching, pembentukan cabang", "Warna": "#22c55e"},
        {"Minggu": "5-7", "Hari": "35-49", "Fase": "Vegetatif 2", "Aktivitas": "Pertumbuhan cabang, lampu malam ON", "Warna": "#16a34a"},
        {"Minggu": "7-9", "Hari": "49-63", "Fase": "Inisiasi Bunga", "Aktivitas": "Mulai tutup plastik hitam, tunas bunga", "Warna": "#f9a8d4"},
        {"Minggu": "9-11", "Hari": "63-77", "Fase": "Kuncup Terlihat", "Aktivitas": "Kuncup membesar, naikkan K", "Warna": "#f472b6"},
        {"Minggu": "11-13", "Hari": "77-91", "Fase": "Pematangan", "Aktivitas": "Bunga mulai berwarna, finishing", "Warna": "#ec4899"},
        {"Minggu": "13-15", "Hari": "91-105", "Fase": "Panen", "Aktivitas": "Panen saat 2-3 kuntum mekar/tangkai", "Warna": "#be185d"},
    ]
    
    for item in timeline_data:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin: 0.5rem 0; padding: 1rem; 
                    background: {item['Warna']}20; border-left: 4px solid {item['Warna']}; 
                    border-radius: 8px;">
            <div style="min-width: 100px; font-weight: bold; color: {item['Warna']};">
                Minggu {item['Minggu']}<br>
                <small style="color: #6b7280;">Hari {item['Hari']}</small>
            </div>
            <div style="margin-left: 1rem;">
                <strong>{item['Fase']}</strong><br>
                <span style="color: #4b5563;">{item['Aktivitas']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Harvest date calculator
    st.markdown("### 🧮 Kalkulator Tanggal Panen")
    
    start_date = st.date_input("Tanggal mulai stek:", datetime.now())
    
    if start_date:
        harvest_start = start_date + timedelta(days=98)
        harvest_end = start_date + timedelta(days=112)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Mulai Tutup Plastik", (start_date + timedelta(days=49)).strftime('%d %B %Y'))
        with col2:
            st.metric("Estimasi Panen Awal", harvest_start.strftime('%d %B %Y'))
        with col3:
            st.metric("Estimasi Panen Akhir", harvest_end.strftime('%d %B %Y'))
        
        st.success(f"🌸 Bunga siap panen antara **{harvest_start.strftime('%d %B')}** hingga **{harvest_end.strftime('%d %B %Y')}**")

# TAB 8: Manajemen Suhu Musim Dingin
with tab8:
    st.subheader("🔥 Manajemen Suhu Musim Dingin & Mesin Dambo")
    
    st.info("""
    **Mengapa Penting?**
    - Krisan membutuhkan suhu optimal 18-24°C
    - Di musim dingin (Desember-Februari), suhu bisa turun hingga 10-15°C di dataran tinggi
    - Suhu rendah menghambat pertumbuhan dan kualitas bunga
    - Mesin dambo (heater) adalah solusi efektif untuk menjaga suhu greenhouse
    """)
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">🌡️ A. Kalkulator Kebutuhan Pemanas (Dambo)</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📐 Input Data Greenhouse")
        gh_length = st.number_input("Panjang Greenhouse (m)", min_value=1.0, max_value=100.0, value=20.0, step=1.0)
        gh_width = st.number_input("Lebar Greenhouse (m)", min_value=1.0, max_value=50.0, value=8.0, step=1.0)
        gh_height = st.number_input("Tinggi Greenhouse (m)", min_value=1.0, max_value=10.0, value=4.0, step=0.5)
        
        outside_temp = st.slider("Suhu Luar Minimum (°C)", min_value=5, max_value=20, value=12)
        target_temp = st.slider("Suhu Target Greenhouse (°C)", min_value=15, max_value=28, value=20)
    
    with col2:
        st.markdown("#### 🔥 Hasil Perhitungan")
        
        # Calculate volume
        volume = gh_length * gh_width * gh_height
        st.metric("Volume Greenhouse", f"{volume:.1f} m³")
        
        # Calculate temperature difference
        temp_diff = target_temp - outside_temp
        st.metric("Selisih Suhu yang Harus Dinaikkan", f"{temp_diff}°C")
        
        # Calculate required heating capacity (simplified formula)
        # BTU/hr = Volume (m³) × Temp Diff (°C) × 3.41 × Heat Loss Factor
        heat_loss_factor = 1.5  # For greenhouse with plastic cover
        btu_required = volume * temp_diff * 3.41 * heat_loss_factor
        kw_required = btu_required / 3412.14  # Convert to kW
        
        st.metric("Kapasitas Pemanas Dibutuhkan", f"{btu_required:,.0f} BTU/hr")
        st.metric("Setara dengan", f"{kw_required:.1f} kW")
        
        # Recommend number of dambo units
        # Assume 1 dambo unit = 50,000 BTU/hr
        dambo_capacity = 50000
        num_dambo = int(btu_required / dambo_capacity) + 1
        
        st.success(f"💡 **Rekomendasi:** {num_dambo} unit mesin dambo (@ 50,000 BTU/hr)")
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">⛽ B. Estimator Konsumsi Bahan Bakar</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fuel_type = st.selectbox("Jenis Bahan Bakar", ["Minyak Tanah", "Solar", "LPG"])
        hours_per_day = st.slider("Jam Operasi/Hari", min_value=1, max_value=24, value=12)
        days_per_month = st.slider("Hari Operasi/Bulan", min_value=1, max_value=31, value=30)
    
    # Fuel consumption calculation
    # Assume 1 dambo consumes ~1.5 L/hour for kerosene
    consumption_rates = {
        "Minyak Tanah": 1.5,  # L/hour per unit
        "Solar": 1.2,
        "LPG": 0.8  # kg/hour per unit
    }
    
    fuel_prices = {
        "Minyak Tanah": 12500,  # Rp/L
        "Solar": 6800,
        "LPG": 15000  # Rp/kg
    }
    
    consumption_per_hour = consumption_rates[fuel_type] * num_dambo
    daily_consumption = consumption_per_hour * hours_per_day
    monthly_consumption = daily_consumption * days_per_month
    
    daily_cost = daily_consumption * fuel_prices[fuel_type]
    monthly_cost = monthly_consumption * fuel_prices[fuel_type]
    
    with col2:
        st.markdown("#### 📊 Konsumsi Bahan Bakar")
        unit = "L" if fuel_type != "LPG" else "kg"
        st.metric(f"Per Hari", f"{daily_consumption:.1f} {unit}")
        st.metric(f"Per Bulan", f"{monthly_consumption:.1f} {unit}")
        st.metric(f"Per Siklus (3.5 bulan)", f"{monthly_consumption * 3.5:.1f} {unit}")
    
    with col3:
        st.markdown("#### 💰 Biaya Operasional")
        st.metric("Per Hari", f"Rp {daily_cost:,.0f}")
        st.metric("Per Bulan", f"Rp {monthly_cost:,.0f}")
        st.metric("Per Siklus (3.5 bulan)", f"Rp {monthly_cost * 3.5:,.0f}")
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">💡 C. Tips Efisiensi Energi</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **1. Insulasi Greenhouse:**
        - Gunakan plastik UV double layer (gap 10-15 cm)
        - Pasang thermal screen di malam hari
        - Tutup ventilasi samping saat malam
        - Seal semua celah dengan lakban
        
        **2. Strategi Pemanasan:**
        - Operasikan dambo hanya saat suhu \u003c 15°C
        - Gunakan thermostat otomatis
        - Zona heating: fokus di area tanaman
        - Waktu optimal: 18.00 - 06.00 WIB
        """)
    
    with col2:
        st.markdown("""
        **3. Alternatif Pemanas:**
        - **Electric Heater:** Lebih bersih, tapi biaya listrik tinggi
        - **Thermal Blanket:** Pasif, cocok untuk suhu tidak terlalu rendah
        - **Kompos Panas:** Organik, tapi kurang konsisten
        
        **4. Monitoring:**
        - Pasang termometer digital dengan alarm
        - Catat suhu setiap 2 jam
        - Adjust berdasarkan fase tanaman
        - Suhu malam 15-18°C cukup untuk krisan
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">📈 D. Analisis Cost-Benefit</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Investment calculation
    dambo_price = 3500000  # Rp per unit
    installation_cost = 500000 * num_dambo
    total_investment = (dambo_price * num_dambo) + installation_cost
    
    # Benefit calculation
    # Assume without heating: 30% yield loss in winter
    # With heating: maintain 90% yield
    plants_per_cycle = int(volume * 50)  # Rough estimate: 50 plants/m³
    yield_without_heating = plants_per_cycle * 0.6  # 60% survival in cold
    yield_with_heating = plants_per_cycle * 0.9  # 90% survival with heating
    additional_yield = yield_with_heating - yield_without_heating
    
    price_per_stem = 12000  # Average Rp/stem
    additional_revenue = additional_yield * price_per_stem
    
    # ROI calculation
    operating_cost_per_cycle = monthly_cost * 3.5
    net_benefit_per_cycle = additional_revenue - operating_cost_per_cycle
    
    if net_benefit_per_cycle > 0:
        payback_cycles = total_investment / net_benefit_per_cycle
        payback_months = payback_cycles * 3.5
    else:
        payback_months = float('inf')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Investasi Awal", f"Rp {total_investment/1_000_000:.1f} jt")
    with col2:
        st.metric("Biaya Operasi/Siklus", f"Rp {operating_cost_per_cycle/1_000_000:.1f} jt")
    with col3:
        st.metric("Tambahan Hasil/Siklus", f"{additional_yield:,.0f} tangkai")
    with col4:
        st.metric("Net Benefit/Siklus", f"Rp {net_benefit_per_cycle/1_000_000:.1f} jt")
    
    if payback_months < 24:
        st.success(f"✅ **Layak!** Payback period: **{payback_months:.1f} bulan** (~{payback_cycles:.1f} siklus)")
    elif payback_months < 48:
        st.warning(f"⚠️ **Cukup Layak.** Payback period: **{payback_months:.1f} bulan** (~{payback_cycles:.1f} siklus)")
    else:
        st.error("❌ **Kurang Layak.** Pertimbangkan alternatif lain atau perbaiki efisiensi.")
    
    st.markdown("---")
    
    st.markdown("""
    <div class="sop-card">
        <div class="phase-title">🎯 E. Rekomendasi Praktis</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    **Untuk Greenhouse Anda ({gh_length}m × {gh_width}m × {gh_height}m):**
    
    1. **Peralatan:**
       - {num_dambo} unit mesin dambo @ Rp {dambo_price/1_000_000:.1f} jt = Rp {(dambo_price * num_dambo)/1_000_000:.1f} jt
       - Thermostat digital: Rp 500,000
       - Instalasi pipa \u0026 ducting: Rp {installation_cost/1_000_000:.1f} jt
       - **Total: Rp {total_investment/1_000_000:.1f} jt**
    
    2. **Penempatan Dambo:**
       - Letakkan di tengah greenhouse untuk distribusi merata
       - Tinggi 50-100 cm dari tanah
       - Arahkan output panas ke atas (bukan langsung ke tanaman)
       - Jarak antar unit: {gh_length/num_dambo:.1f} meter
    
    3. **Jadwal Operasi Optimal:**
       - Mulai operasi saat suhu \u003c 16°C
       - Peak hours: 22.00 - 06.00 WIB
       - Matikan saat suhu \u003e 20°C
       - Estimasi: {hours_per_day} jam/hari di musim dingin
    
    4. **Budget Bulanan:**
       - Bahan bakar ({fuel_type}): Rp {monthly_cost/1_000_000:.1f} jt
       - Maintenance: Rp 200,000
       - **Total: Rp {(monthly_cost + 200000)/1_000_000:.1f} jt/bulan**
    """)
    
    st.info("""
    💡 **Pro Tips:**
    - Kombinasikan dengan thermal screen untuk efisiensi maksimal
    - Monitor suhu dengan sensor IoT untuk otomasi
    - Lakukan maintenance rutin setiap 2 minggu
    - Simpan bahan bakar di tempat aman, jauh dari sumber api
    - Pastikan ventilasi cukup untuk menghindari akumulasi CO₂
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #9ca3af; font-size: 0.8rem;">
    🌸 Budidaya Krisan Pro | Panduan berbasis riset dan praktik petani Indonesia
</div>
""", unsafe_allow_html=True)
