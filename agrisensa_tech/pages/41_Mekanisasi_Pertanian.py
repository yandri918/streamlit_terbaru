import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Mekanisasi Pertanian - AgriSensa",
    page_icon="🚜",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Header
st.title("🚜 Mekanisasi Pertanian")
st.markdown("**Panduan Lengkap Modernisasi dan Efisiensi Alat Mesin Pertanian (Alsintan)**")
st.info("💡 Modul ini membantu Anda memilih teknologi yang tepat, mulai dari metode tradisional hingga presisi tinggi untuk skala industri.")

# Main tabs
# ... (Tab list update)
tab_land, tab_plant, tab_nursery_mech, tab_maintenance, tab_harvest, tab_greenhouse, tab_recommendation, tab_safety = st.tabs([
    "🌱 Pengolahan Lahan",
    "🚜 Penanaman",
    "🧩 Mekanisasi Nursery",
    "🛡️ Pemeliharaan",
    "🌾 Pemanenan",
    "🏠 Greenhouse & Hidroponik",
    "💡 Rekomendasi Pintar",
    "⚙️ Perawatan & K3"
])
# ... (Content for Tab 1 and 2 remains same)

# ===== TAB: NURSERY MECHANIZATION (NEW) =====
with tab_nursery_mech:
    st.header("🧩 Mekanisasi Pembibitan (Modern Nursery)")
    st.markdown("Automasi dalam produksi bibit memastikan keseragaman, efisiensi waktu, dan kualitas vigor tanaman yang tinggi.")
    
    n1, n2 = st.columns(2)
    
    with n1:
        st.subheader("1. Persiapan Media (Soil Preparation)")
        st.markdown("""
        *   **Soil Mixer:** Mesin pengaduk media tanam (tanah + cocopeat + pupuk) agar homogen. Kapasitas: 500-1000 kg/jam.
        *   **Tray Filler:** Mesin pengisi tray semai otomatis. Memastikan kepadatan media seragam di setiap lubang tray.
        """)
        
        st.image("https://sc04.alicdn.com/kf/H75475155f97341079366037060370600q.jpg", caption="Ilustrasi: Automatic Tray Filler Line", use_column_width=True)

    with n2:
        st.subheader("2. Penaburan Benih (Seeding)")
        st.markdown("""
        *   **Vacuum Seeder:** Menggunakan jarum hisap udara untuk mengambil 1 biji per lubang secara presisi. Kecepatan: 200 tray/jam.
        *   **Drum Seeder:** Untuk biji bulat (pelleted seeds). Lebih cepat dari vacuum, sistem putar.
        """)
        st.info("💡 **Efisiensi:** 1 Mesin Seeder setara dengan kecepatan kerja 20 orang tenaga kerja manual.")
    
    st.divider()
    
    st.subheader("3. Teknologi Penyiraman & Grafting")
    
    ng1, ng2 = st.columns(2)
    
    with ng1:
        st.markdown("#### 🌧️ Boom Irrigation")
        st.write("Lengan penyiram otomatis yang bergerak di atas rel (rail) sepanjang rumah semai. Menghasilkan butiran air sangat halus (mist) yang tidak merusak bibit muda.")
    
    with ng2:
        st.markdown("#### ✂️ Grafting Robot")
        st.write("Robot penyambung batang otomatis. Menggunakan kamera untuk mendeteksi diameter batang scion dan rootstock, lalu memotong dan menjepitnya dengan klip khusus. Tingkat keberhasilan >95%.")


# ===== TAB 1: PENGOLAHAN LAHAN =====
with tab_land:
    st.header("🌱 Teknologi Pengolahan Lahan")
    
    st.markdown("""
    Pengolahan lahan adalah fondasi keberhasilan pertanian. Pilihan metode sangat bergantung pada skala lahan, topografi, dan anggaran.
    """)

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Metode Tradisional (Tenaga Hewan)")
        st.markdown("""
        Menggunakan tenaga kerbau atau sapi untuk menarik bajak singkal dan garu.
        
        **Kelebihan:**
        *   ✅ **Ramah Lingkungan:** Tidak ada emisi gas buang.
        *   ✅ **Struktur Tanah Terjaga:** Pemadatan tanah minimal dibanding traktor berat.
        *   ✅ **Pupuk Alami:** Kotoran hewan menjadi pupuk organik langsung.
        *   ✅ **Akses Medan Sulit:** Bisa menjangkau lahan terasering sempit yang sulit dilalui mesin.
        
        **Kekurangan:**
        *   ❌ **Lambat:** Kapasitas kerja rendah (lama penyelesaian).
        *   ❌ **Butuh Istirahat:** Hewan butuh istirahat, tidak bisa kerja nonstop.
        *   ❌ **Biaya Pemeliharaan Harian:** Pakan dan kandang harus tersedia sepanjang tahun.
        """)

    with col2:
        st.subheader("2. Metode Modern (Traktor)")
        st.markdown("""
        Menggunakan mesin, baik Traktor Roda 2 (TR2) maupun Traktor Roda 4 (TR4).
        
        **Kelebihan:**
        *   ✅ **Cepat & Efisien:** Kapasitas kerja tinggi, menyelesaikan lahan luas dalam waktu singkat.
        *   ✅ **Waktu Tepat:** Memungkinkan penanaman serentak (penting untuk pengendalian hama).
        *   ✅ **Kualitas Olahan:** Hasil balikan tanah lebih dalam dan gembur (terutama TR4).
        *   ✅ **Fleksibel:** Bisa kerja malam hari jika mendesak.
        
        **Kekurangan:**
        *   ❌ **Investasi Tinggi:** Harga beli mesin mahal.
        *   ❌ **Pemadatan Tanah:** Risiko *hardpan* jika penggunaan TR4 berlebih pada lahan basah.
        *   ❌ **Butuh Operator Terlatih.**
        """)
    
    st.divider()
    
    st.subheader("⚔️ PERBANDINGAN: Kerbau vs Traktor")
    
    # Data Comparison
    comparison_data = {
        "Parameter": ["Kecepatan Kerja (Ha/hari)", "Biaya Operasional (Rp/Ha)", "Tenaga Kerja", "Kedalaman Olah (cm)", "Dampak Tanah"],
        "🐃 Kerbau (Tradisional)": ["0.04 - 0.05 Ha", "Rp 1.5jt - 2jt (sewa + pawang)", "1 Pawang", "10 - 15 cm", "Pemadatan minim, lestari"],
        "🚜 Traktor Roda 2 (Modern)": ["0.3 - 0.5 Ha", "Rp 800rb - 1.2jt", "1 Operator", "15 - 20 cm", "Sedang"],
        "🚜 Traktor Roda 4 (Industri)": ["3.0 - 5.0 Ha", "Rp 1.5jt++ (Cepat)", "1 Operator", "25 - 30 cm", "Pemadatan tinggi (risiko hardpan)"]
    }
    df_compare = pd.DataFrame(comparison_data)
    st.table(df_compare)
    
    st.markdown("""
    > **Kesimpulan:** Untuk **lahan sempit (<0.5 Ha) dan berteras**, kerbau masih sangat relevan dan efisien. Namun untuk **target swasembada dan lahan hamparan**, mekanisasi mutlak diperlukan untuk mengejar musim tanam.
    """)
    
    st.markdown("### 🚜 Jenis Traktor")
    
    t1, t2 = st.tabs(["Traktor Roda 2 (Hand Tractor)", "Traktor Roda 4"])
    
    with t1:
        st.info("**Cocok untuk:** Petani skala kecil-menengah, lahan sawah, lahan kering datar.")
        st.markdown("""
        *   **Bajak Singkal (Moldboard Plow):** Membalik tanah, membenamkan gulma.
        *   **Bajak Rotary:** Mencacah tanah menjadi butiran halus (siap tanam).
        *   **Garu (Harrow):** Meratakan tanah setelah dibajak (lumpur).
        """)
        
    with t2:
        st.info("**Cocok untuk:** Perusahaan, UPJA, lahan kering luas (tebu, jagung, sawit), sawah bukaan baru.")
        st.markdown("""
        *   **Disc Plow (Bajak Piringan):** Untuk tanah keras, berbatu, atau akar banyak.
        *   **Rotavator:** Pengolahan tanah sekali jalan (one-pass tillage) untuk efisiensi.
        *   **Subsoiler:** Memecah lapisan keras (hardpan) di kedalaman 40-50 cm.
        """)

# ===== TAB 2: PENANAMAN =====
with tab_plant:
    st.header("🚜 Teknologi Penanaman (Planting)")
    st.markdown("Presisi dalam jarak tanam dan jumlah benih sangat menentukan potensi hasil panen.")

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌾 Padi (Rice Transplanter)")
        st.markdown("""
        Mesin tanam pindah bibit padi.
        *   **Walk-behind Transplanter:** Operator berjalan di belakang. (4 baris). Cocok untuk sawah petakan.
        *   **Riding Transplanter:** Operator menaiki mesin. (6-8 baris). Kecepatan tinggi, presisi tinggi.
        
        **Manfaat:**
        *   Jarak tanam presisi (misal: Jajar Legowo).
        *   Populasi tanaman optimal.
        *   Hemat benih dibanding tabur benih langsung.
        """)
        
    with col2:
        st.subheader("🌽 Palawija (Seeder)")
        st.markdown("""
        Alat tanam biji-bijian (Jagung, Kedelai, Kacang Hijau).
        *   **Pneumatic Seeder:** Menggunakan angin hisap untuk mengambil benih satu per satu (sangat presisi).
        *   **Dosing Roller:** Mekanis, murah, namun kadang *double seed*.
        *   **Potato Planter:** Otomatis membuat guludan, menanam umbi, dan menutup tanah sekaligus.
        """)

# ===== TAB 3: PEMELIHARAAN =====
with tab_maintenance:
    st.header("🛡️ Pemeliharaan & Proteksi Tanaman")
    
    st.subheader("1. Penyemprotan (Spraying)")
    
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        st.markdown("**1. Knapsack Sprayer (Gendong)**")
        st.markdown("Manual atau Elektrik. Paling umum digunakan petani kecil.")
    
    with col_s2:
        st.markdown("**2. Power Sprayer / Boom Sprayer**")
        st.markdown("Menggunakan mesin pompa tekanan tinggi. Boom sprayer memiliki bentangan nozzle lebar (efisien untuk bawang/sayuran).")
        
    with col_s3:
        st.markdown("**3. Drone Pertanian (UAV)**")
        st.markdown("""
        Teknologi 4.0.
        *   ✅ **Cepat:** 1 Ha selesai dalam 10-15 menit.
        *   ✅ **Hemat Air:** Volume semprot rendah (Ultra Low Volume).
        *   ✅ **Safety:** Operator tidak terpapar pestisida.
        """)

# ===== TAB 4: PEMANENAN =====
with tab_harvest:
    st.header("🌾 Teknologi Pemanenan (Harvesting)")
    st.warning("Kehilangan hasil (losses) terbesar sering terjadi saat panen manual yang tidak tepat.")
    
    st.subheader("Mesin Panen Padi (Combine Harvester)")
    
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### 1. Mini Combine")
        st.markdown("""
        *   **Lebar potong:** 1.0 - 1.2 m
        *   **Karung:** Manual (gabah masuk karung)
        *   **Cocok:** Lahan terasering, petakan kecil.
        """)
        
    with c2:
        st.markdown("#### 2. Medium Combine")
        st.markdown("""
        *   **Lebar potong:** 1.5 - 2.0 m
        *   **Tanki:** Penampung gabah (grain tank)
        *   **Cocok:** Lahan datar hamparan menengah.
        """)
        
    with c3:
        st.markdown("#### 3. Large Combine")
        st.markdown("""
        *   **Lebar potong:** > 2.5 m
        *   **Kabin:** AC (nyaman untuk operator)
        *   **Efisien:** Kehilangan hasil < 2%.
        *   **Cocok:** Food estate, perusahaan.
        """)
        
    st.divider()
    st.subheader("🌽 Mesin Lainnya")
    st.markdown("""
    *   **Corn Combine:** Memanen jagung sekaligus memipil.
    *   **Potato Digger:** Mengangkat umbi kentang ke permukaan tanah (mengurangi luka cangkul).
    *   **Cane Harvester:** Mesin panen tebu otomatis (chopper).
    """)

# ===== TAB 5: GREENHOUSE & HIDROPONIK =====
with tab_greenhouse:
    st.header("🏠 Mekanisasi Greenhouse & Hidroponik")
    st.markdown("Modernisasi pertanian presisi di lingkungan terkendali (Controlled Environment Agriculture).")
    
    col_gh1, col_gh2 = st.columns(2)
    
    with col_gh1:
        st.subheader("1. Pengendalian Iklim (Climate Control)")
        st.markdown("""
        Menjaga suhu dan kelembaban optimal di dalam greenhouse.
        *   **Exhaust Fan:** Kipas besar (biasanya 50 inch) untuk membuang udara panas.
        *   **Cooling Pad (Cellideck):** Bantalan basah di sisi berseberangan dengan kipas untuk menurunkan suhu (Evaporative Cooling).
        *   **Mist Maker / Fogging:** Pengabut untuk meningkatkan kelembaban (RH) secara instan.
        *   **Shading Net Otomatis:** Jaring peneduh yang bisa buka-tutup dengan motor elektrik sesuai intensitas matahari.
        """)
        
    with col_gh2:
        st.subheader("2. Fertigasi Otomatis (Fertigation)")
        st.markdown("""
        Pemberian air dan nutrisi (pupuk) secara bersamaan dan presisi.
        *   **Venturi Injector:** Alat sederhana hisap pupuk dengan prinsip perbedaan tekanan air. Murah & efektif.
        *   **Dosing Pump (Dosatron):** Pompa khusus yang mencampur nutrisi dengan rasio sangat akurat tanpa listrik (tenaga air).
        *   **Drip Irrigation (Tetes):** Tetesan air langsung ke akar. Hemat air hingga 70%.
        *   **NFT/DFT System:** Untuk selada/sayur daun, pompa sirkulasi 24 jam.
        """)
    
    st.divider()
    
    st.subheader("🤖 IoT & Automation")
    st.info("Level tertinggi mekanisasi greenhouse adalah otomatisasi penuh berbasis sensor.")
    
    col_iot1, col_iot2, col_iot3 = st.columns(3)
    
    with col_iot1:
        st.markdown("#### 🌡️ Sensor")
        st.markdown("- Suhu & Kelembaban (DHT/SHT)\n- Intensitas Cahaya (Lux)\n- pH & EC Air (Nutrisi)")
    
    with col_iot2:
        st.markdown("#### 🧠 Controller")
        st.markdown("- Mikrokontroler (ESP32/Arduino)\n- PLC (Industrial Grade)\n- Mengambil keputusan (e.g., *Jika suhu > 30°C, nyalakan kipas*)")
        
    with col_iot3:
        st.markdown("#### 📱 Monitoring")
        st.markdown("- Dashboard di HP/Laptop\n- Notifikasi via WA/Telegram jika air habis atau listrik mati.")

# ===== TAB 6: REKOMENDASI =====
with tab_recommendation:
    st.header("💡 Rekomendasi Pintar Alsintan")
    st.markdown("Dapatkan rekomendasi paket mekanisasi sesuai kondisi Anda.")
    
    with st.form("alsintan_form"):
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            lahan = st.number_input("Luas Lahan (Ha)", min_value=0.1, value=1.0, step=0.1)
            komoditas = st.selectbox("Komoditas Utama", ["Padi Sawah", "Jagung", "Hortikultura (Sayur/Buah)", "Tebu/Sawit"])
        with col_f2:
            budget = st.select_slider("Tingkat Investasi / Anggaran", options=["Hemat (Low)", "Menengah (Medium)", "Profesional (High)"])
            topografi = st.selectbox("Kondisi Lahan", ["Datar Hamparan Luas", "Berteras/Petakan Kecil", "Lahan Kering/Berbukit"])
            
        submit = st.form_submit_button("🔍 Cari Rekomendasi")
        
    if submit:
        st.divider()
        st.subheader("📦 Paket Rekomendasi Anda")
        
        # Simple Logic for Recommendation
        rec_olah = ""
        rec_tanam = ""
        rec_rawat = ""
        rec_panen = ""
        
        # PADI
        if komoditas == "Padi Sawah":
            if budget == "Hemat (Low)":
                rec_olah = "Sewa Traktor Roda 2 (Bajak Singkal) atau Kerbau (jika lahan dalam)"
                rec_tanam = "Tanam Manual (Taju) / Caplak Legowo"
                rec_rawat = "Knapsack Sprayer Manual"
                rec_panen = "Sabit Bergerigi + Power Thresher (Perontok)"
            elif budget == "Menengah (Medium)":
                rec_olah = "Miliki Traktor Roda 2 (Rotary)"
                rec_tanam = "Walk-behind Transplanter (Sewa/Beli)"
                rec_rawat = "Electric Knapsack Sprayer"
                rec_panen = "Mini Combine Harvester"
            else: # High
                rec_olah = "Traktor Roda 4 (Rotavator) - Efisiensi tinggi"
                rec_tanam = "Riding Transplanter (Cepat & Nyaman)"
                rec_rawat = "Drone Spraying (Presisi)"
                rec_panen = "Large Combine Harvester (Losses minimum)"
        
        elif komoditas == "Jagung":
            if budget == "Hemat (Low)":
                rec_olah = "Traktor Roda 2"
                rec_tanam = "Alat Tanam Dorong (Manual Seeder)"
                rec_rawat = "Knapsack Sprayer"
                rec_panen = "Manual + Corn Sheller (Pemipil)"
            else:
                rec_olah = "Traktor Roda 4 (Disc Plow)"
                rec_tanam = "Pneumatic Planter (4 rows)"
                rec_rawat = "Boom Sprayer"
                rec_panen = "Corn Combine Harvester"
                
        else:
            rec_olah = "Cultivator (untuk bedengan)"
            rec_tanam = "Manual / Semi-mekanis"
            rec_rawat = "Power Sprayer (Irigasi kabut)"
            rec_panen = "Manual"

        # Tampilkan Hasil
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        with col_r1:
            st.info("🌱 Pengolahan")
            st.markdown(f"**{rec_olah}**")
        with col_r2:
            st.success("🚜 Penanaman")
            st.markdown(f"**{rec_tanam}**")
        with col_r3:
            st.warning("🛡️ Perawatan")
            st.markdown(f"**{rec_rawat}**")
        with col_r4:
            st.error("🌾 Panen")
            st.markdown(f"**{rec_panen}**")
            
        st.caption(f"Rekomendasi disesuaikan untuk: {komoditas} pada lahan {lahan} Ha dengan topografi {topografi}.")

# ===== TAB 6: PERAWATAN & K3 =====
with tab_safety:
    st.header("⚙️ Perawatan Mesin & Keselamatan Kerja")
    
    st.subheader("Jadwal Perawatan Dasar")
    st.markdown("""
    1.  **Harian (Sebelum Operasi):**
        *   Cek air radiator.
        *   Cek level oli mesin.
        *   Cek bahan bakar.
        *   Kencangkan baut-baut kendor (akibat getaran).
    2.  **Mingguan (50 Jam Kerja):**
        *   Bersihkan filter udara.
        *   Cek ketegangan V-belt.
        *   Lumasi grease nipple (gemuk).
    3.  **Bulanan (200 Jam Kerja):**
        *   Ganti oli mesin.
        *   Ganti filter oli.
        *   Cek oli transmisi/gardan.
    """)
    
    st.error("""
    ### ⚠️ KESELAMATAN KERJA (K3)
    *   **Jangan memakai baju longgar** yang bisa tersangkut di putaran mesin (V-belt/PTO).
    *   **Matikan mesin** saat melakukan perbaikan atau pembersihan pisau.
    *   Gunakan **sepatu boots** dan masker saat menyemprot pestisida.
    *   Hati-hati saat memutar traktor di lahan miring (risiko terbalik).
    """)
