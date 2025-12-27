import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Konservasi Lahan & Tanah - AgriSensa",
    page_icon="🏞️",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






# Header
st.title("🏞️ Pengelolaan Lahan & Konservasi Tanah")
st.markdown("**Soil Conservation: Menjaga Aset Paling Berharga Petani**")

# Main tabs
tab_diagnosa, tab_mekanis, tab_vegetatif, tab_organik, tab_usle = st.tabs([
    "🔍 Diagnosa & Erosi",
    "🧱 Konservasi Mekanis",
    "🌿 Konservasi Vegetatif",
    "🍂 Manajemen Bahan Organik",
    "🧮 Kalkulator Erosi (USLE)"
])

# ===== TAB 1: DIAGNOSA & EROSI =====
with tab_diagnosa:
    st.header("🔍 Diagnosa Erosi & Degradasi Lahan")
    
    st.markdown("""
    ### Mengapa Konservasi Tanah Penting? (Hubungan Sebab-Akibat)
    
    Tanah adalah **aset non-renewable** dalam skala waktu manusia. Pembentukan tanah 1 cm butuh 100-400 tahun, tapi bisa hilang dalam 1 jam hujan lebat jika tidak dilindungi.
    
    **Rantai Sebab-Akibat (Causal Chain):**
    
    1.  **SEBAB: Hujan Lebat pada Tanah Terbuka**
        *   Energi kinetik butiran hujan memukul agregat tanah.
        *   **AKIBAT:** Agregat pecah (detachment), pori-pori tanah tersumbat.
    
    2.  **SEBAB: Pori-pori Tanah Tersumbat**
        *   Infiltrasi air menurun drastis.
        *   **AKIBAT:** Air mengalir di permukaan (Run-off) meningkat.
    
    3.  **SEBAB: Run-off Meningkat**
        *   Air mengalir membawa partikel tanah (topsoil) yang kaya hara.
        *   **AKIBAT:** Erosi lapisan atas (subur) hilang.
    
    4.  **DAMPAK FINAL (Petani Merugi):**
        *   📉 **Produktivitas turun** (hara hilang).
        *   💸 **Biaya pupuk naik** (harus ganti hara yang hanyut).
        *   🏜️ **Kekeringan** (tanah tidak bisa simpan air).
    
    ---
    
    ### Jenis-Jenis Erosi
    
    1.  **Erosi Percik (Splash Erosion):**
        *   Akibat pukulan air hujan langsung.
        *   *Ciri:* Butiran tanah terlempar, kotoran menempel di batang tanaman bawah.
    
    2.  **Erosi Lembar (Sheet Erosion):**
        *   Pengikisan merata di seluruh permukaan.
        *   *Ciri:* Akar tanaman terlihat, warna tanah memucat (humus hilang).
        *   *Bahaya:* Sering tidak disadari ("Invisible Enemy").
    
    3.  **Erosi Alur (Rill Erosion):**
        *   Terbentuk alur-alur kecil (<30 cm).
        *   *Ciri:* Ada selokan-selokan kecil searah lereng.
        *   *Solusi:* Masih bisa dihilangkan dengan pengolahan tanah biasa.
    
    4.  **Erosi Parit (Gully Erosion):**
        *   Alur membesar menjadi parit dalam (>30 cm).
        *   *Ciri:* Parit besar berbentuk V atau U.
        *   *Bahaya:* Lahan terbelah, tidak bisa diolah lagi.
    
    ---
    
    ### Indikator Lahan Kritis
    
    *   **Fisik:** Solum tanah dangkal, batuan induk muncul, warna merah/kuning (subsoil terekspos).
    *   **Kimia:** pH rendah (masam), miskin hara, C-organik rendah (<1%).
    *   **Biologi:** Tidak ada cacing tanah, vegetasi kerdil/kuning.
    """)

# ===== TAB 2: KONSERVASI MEKANIS =====
with tab_mekanis:
    st.header("🧱 Metode Konservasi Mekanis (Sipil Teknis)")
    
    st.markdown("""
    Teknik mekanis bertujuan untuk:
    1.  **Memperpendek** panjang lereng (LS factor).
    2.  **Memperkecil** kemiringan lereng.
    3.  **Menampung** dan menyalurkan aliran permukaan (run-off) agar tidak merusak.
    
    ---
    
    ### 1. Terasering (Sengkedan)
    
    **Konsep:** Mengubah lereng miring menjadi serangkaian bidang datar bertingkat.
    
    #### A. Teras Bangku (Bench Terrace)
    *   **Cocok untuk:** Lereng 10-40%, tanah tebal (>50 cm).
    *   **Konstruksi:**
        *   **Bidang Olah:** Datar/sedikit miring ke dalam (reverse slope 1%) agar air masuk tanah.
        *   **Tampingan (Riser):** Ditanami rumput penguat (Vetiver, Rumput Gajah) agar tidak longsor.
        *   **Bibir Teras:** Ditinggikan 10-20 cm untuk menahan air.
    *   **Kelemahan:** Biaya tenaga kerja tinggi, tidak cocok untuk tanah dangkal (badrock).
    
    #### B. Teras Gulud (Ridge Terrace)
    *   **Cocok untuk:** Lereng landai (3-10%), tanah agak dangkal.
    *   **Konstruksi:** Membuat guludan tanah memotong lereng (sejajar kontur). Di belakang guludan dibuat saluran air.
    *   **Sebab-Akibat:** Guludan menahan laju air → air meresap di saluran → erosi berkurang.
    
    #### C. Teras Individu (Individual Terrace)
    *   **Cocok untuk:** Tanaman perkebunan (Kelapa, Durian, Sawit) di lereng curam.
    *   **Konstruksi:** Teras hanya dibuat di sekeliling piringan pohon (diameter 1-2 m).
    *   **Manfaat:** Hemat biaya, tidak memotong akar tanaman yang sudah ada.
    
    ---
    
    ### 2. Rorak (Silt Pit / Lubang Angin)
    
    **Definisi:** Lubang buntu yang dibuat di bidang olah atau saluran teras.
    
    **Dimensi Ideal:**
    *   Panjang: 1 - 2 meter
    *   Lebar: 40 - 50 cm
    *   Kedalaman: 40 - 60 cm
    
    **Fungsi (Sebab-Akibat):**
    1.  **Jebakan Sediment:** Lumpur hasil erosi tertampung di rorak → tidak hanyut ke sungai → dikembalikan ke bidang olah (topsoil recycle).
    2.  **Water Harvesting:** Menampung run-off saat hujan → air meresap perlahan → cadangan air tanah saat kemarau.
    
    ---
    
    ### 3. Check Dam (Pengendali Jurang)
    
    **Fungsi:** Bendungan kecil di alur erosi parit untuk menahan sedimen dan mengurangi kecepatan air.
    *   **Material:** Batu, bambu, atau kayu.
    *   **Prinsip:** Air boleh lewat, lumpur harus tertahan. Lama-kelamaan parit akan tertimbun sedimen dan menjadi landai kembali.
    """)

# ===== TAB 3: KONSERVASI VEGETATIF =====
with tab_vegetatif:
    st.header("🌿 Metode Konservasi Vegetatif")
    
    st.markdown("""
    Teknik ini menggunakan tanaman untuk melindungi tanah. Lebih murah dan lestari dibanding teknik mekanis.
    
    **Sebab-Akibat:**
    *   **SEBAB:** Daun menutupi tanah (Intersepsi).
    *   **AKIBAT:** Pukulan hujan tidak langsung ke tanah → Agregat tanah tetap utuh → Infiltrasi tetap tinggi.
    *   **SEBAB:** Akar tanaman mencengkeram tanah.
    *   **AKIBAT:** Stabilitas tanah meningkat → Lawan longsor.
    
    ---
    
    ### 1. Pertanaman Lorong (Alley Cropping)
    
    **Sistem:** Menanam tanaman pangan di lorong antara barisan tanaman pagar (hedgerows).
    *   **Tanaman Pagar:** Legum (Lamtoro, Gamal, Kaliandra).
    *   **Manfaat Ganda:**
        1.  **Konservasi:** Barisan pagar menahan erosi.
        2.  **Pemupukan:** Pangkasan daun legum (biomassa) dijadikan mulsa/pupuk hijau (kaya Nitrogen).
    
    ### 2. Tanaman Penutup Tanah (Cover Crop)
    
    Biasanya Legume Cover Crop (LCC) seperti *Mucuna bracteata*, *Calopogonium*, *Centrosema*.
    *   **Aplikasi:** Di perkebunan Sawit/Karet/Buah.
    *   **Fungsi:** Menjaga kelembaban, menekan gulma, menambah N tanah.
    
    ### 3. Strip Rumput (Grass Strips)
    
    Menanam rumput penguat teras searah kontur.
    *   **Jenis:** Rumput Gajah, Setaria, Raja.
    *   **Manfaat:** Barrier erosi + Pakan ternak (Integrasi Crop-Livestock).
    
    ### 4. Sistem Akar Wangi (Vetiver System)
    
    **"The Bio-Engineering Solution"**
    
    Vetiver (*Chrysopogon zizanioides*) punya karakteristik ajaib:
    *   **Akar:** Tumbuh vertikal ke bawah hingga 3-4 meter (bukan menyebar), kekuatan tarik setara 1/6 baja lunak. **Sebab-Akibat:** Seperti "paku bumi" hidup yang menjahit tanah agar tidak longsor.
    *   **Daun:** Kaku dan tegak, tumbuh rapat membentuk pagar. **Akibat:** Menahan sedimen tapi meloloskan air pelan-pelan.
    *   **Toleransi:** Tahan pH ekstrem (3-10), logam berat, kersang, terendam.
    """)

# ===== TAB 4: MANAJEMEN BAHAN ORGANIK =====
with tab_organik:
    st.header("🍂 Manajemen Bahan Organik Tanah (SOM)")
    
    st.markdown("""
    Bahan Organik Tanah (Soil Organic Matter) adalah **kunci** dari segala kunci konservasi tanah.
    
    ### Hubungan Bahan Organik & Erosi (Causal Loop)
    
    1.  **Struktur Tanah (Aggregate Stability):**
        *   Bahan organik menghasilkan "lem" perekat partikel tanah (gums, polysaccharides).
        *   **Akibat:** Tanah membentuk remah (crumb) yang stabil, tidak mudah hancur dipukul hujan.
    
    2.  **Porositas & Infiltrasi:**
        *   Bahan organik membuat tanah gembur (porous).
        *   **Akibat:** Daya serap air meningkat drastis. Run-off berkurang → Erosi berkurang.
    
    3.  **Daya Simpan Air (Water Holding Capacity):**
        *   Bahan organik bisa menyerap air 20x beratnya (seperti spons).
        *   **Akibat:** Tanaman tahan kekeringan.
    
    ---
    
    ### Teknik Aplikasi
    
    #### 1. Mulsa (Mulching)
    Menutup permukaan tanah dengan sisa tanaman (jerami, serasah).
    *   **Fungsi Fisik:** Melindungi dari pukulan hujan langsung.
    *   **Fungsi Biologis:** Makanan cacing tanah & mikroba.
    *   **Fungsi Kimia:** Menambah hara saat lapuk.
    
    #### 2. Biochar (Arang Hayati)
    Arang dari limbah pertanian (sekam, tongkol jagung) yang dibakar tidak sempurna (pirolisis).
    *   **Keunggulan:** Tahan lama di tanah (recalcitrant) hingga ratusan tahun. Rumah bagi mikroba ("Apartemen Mikroba").
    
    #### 3. Pupuk Kandang & Kompos
    Mengembalikan siklus hara dari ternak ke lahan.
    """)

# ===== TAB 5: KALKULATOR EROSI (USLE) =====
with tab_usle:
    st.header("🧮 Kalkulator Prediksi Erosi (Metode USLE)")
    
    st.markdown("""
    **Universal Soil Loss Equation (USLE)**
    Rumus empiris untuk memprediksi rata-rata erosi tanah jangka panjang.
    
    $$A = R \\times K \\times LS \\times C \\times P$$
    
    Dimana:
    *   **A**: Prediksi Erosi (ton/ha/tahun)
    *   **R**: Faktor Curah Hujan (Erosivitas)
    *   **K**: Faktor Erodibilitas Tanah (Kepekaan tanah)
    *   **LS**: Faktor Panjang & Kemiringan Lereng
    *   **C**: Faktor Tanaman (Cover crop management)
    *   **P**: Faktor Tindakan Konservasi
    """)
    
    st.write("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("1. Input Data Lingkungan")
        
        # Faktor R
        r_input = st.number_input("R - Indeks Erosivitas Hujan", min_value=100.0, max_value=5000.0, value=1500.0, 
                                 help="Di Indonesia rata-rata tinggi (1000-4000). Jawa Barat ~2000-2500.")
        
        # Faktor K
        k_option = st.selectbox("K - Jenis Tanah (Kepekaan)", 
                               options=["Latosol (Tahan) - 0.10", "Andosol (Sedang) - 0.20", "Regosol/Podsolik (Peka) - 0.30", "Tanah Liat/Debu (Sangat Peka) - 0.40"])
        k_value = float(k_option.split(" - ")[-1])
        
        # Faktor LS
        slope = st.slider("Kemiringan Lereng (%)", 0, 100, 15)
        length = st.slider("Panjang Lereng (m)", 10, 200, 50)
        
        # Rumus sederhana LS (Wischmeier & Smith) - simplified approximation
        # LS = (L/22.1)^m * (0.065 + 0.045s + 0.0065s^2)
        # s = slope in %, L in meters
        ls_value = (length/22.1)**0.5 * (0.065 + 0.045*slope + 0.0065*slope**2)
        st.caption(f"Calculated LS Factor: {ls_value:.2f}")

    with col2:
        st.subheader("2. Input Manajemen")
        
        # Faktor C
        c_option = st.selectbox("C - Vegetasi/Tanaman", 
                               options=[
                                   "Hutan Alam Lebat - 0.001",
                                   "Semak Belukar/Kebun Campur - 0.1",
                                   "Padi/Jagung Monokultur - 0.5",
                                   "Tanah Terbuka (Tanpa Tanaman) - 1.0"
                               ])
        c_value = float(c_option.split(" - ")[-1])
        
        # Faktor P
        p_option = st.selectbox("P - Tindakan Konservasi",
                               options=[
                                   "Teras Bangku Sempurna - 0.04",
                                   "Teras Gulud / Kontur - 0.15",
                                   "Pertanaman Lorong (Alley) - 0.30",
                                   "Tanpa Tindakan Konservasi - 1.0"
                               ])
        p_value = float(p_option.split(" - ")[-1])
        
        st.write("---")
        
        # PREDIKSI USLE
        erosion_rate = r_input * k_value * ls_value * c_value * p_value
        
        st.metric(label="Prediksi Laju Erosi", value=f"{erosion_rate:.2f} ton/ha/thn")
        
        # Toleransi Erosi (T) - asumsikan rata-rata 10-12 ton/ha/thn
        t_value = 12.0
        
        if erosion_rate <= t_value:
            st.success("✅ **AMAN:** Erosi di bawah ambang batas toleransi (12 ton/ha/thn). Lanjutkan praktik ini.")
        elif erosion_rate <= 50:
             st.warning("⚠️ **WASPADA:** Erosi sedang. Pertimbangkan menambah tanaman penutup atau memperbaiki teras.")
        else:
            st.error("🚨 **BAHAYA:** Erosi sangat tinggi! Tanah akan habis dalam waktu singkat. WAJIB terasering + reboisasi segera!")
            
    # Simulasi Skenario
    st.write("---")
    st.subheader("📉 Simulasi: Dampak Intervensi")
    st.write("Lihat bagaimana mengubah pengelolaan (C) dan konservasi (P) menurunkan erosi secara drastis:")
    
    # Compare current scenario vs 'Do Nothing' (C=1, P=1)
    erosion_do_nothing = r_input * k_value * ls_value * 1.0 * 1.0
    
    data_comparison = pd.DataFrame({
        "Skenario": ["Tanpa Konservasi (Do Nothing)", "Kondisi Anda Sekarang"],
        "Erosi (ton/ha/thn)": [erosion_do_nothing, erosion_rate]
    })
    
    fig = px.bar(data_comparison, x="Skenario", y="Erosi (ton/ha/thn)", color="Skenario", 
                 color_discrete_sequence=["red", "green"],
                 title="Perbandingan Erosi: Tanpa vs Dengan Konservasi")
    st.plotly_chart(fig, use_container_width=True)

    st.info("💡 **Tips:** Mengubah **P** (misal membuat teras) dan **C** (menanam pohon) adalah cara paling efektif menurunkan erosi karena faktor R (hujan), K (tanah), dan LS (lereng) sulit diubah oleh manusia.")
