import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Fisiologi Tumbuhan - AgriSensa",
    page_icon="🌱",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Header
st.title("🌱 Fisiologi Tumbuhan & Hormon Pertumbuhan")
st.markdown("**Memahami Proses Fisiologis Tanaman untuk Optimasi Produksi**")

# Main tabs
tab_hormone, tab_growth, tab_photosynthesis, tab_stress, tab_practice, tab_brix = st.tabs([
    "🧪 Hormon Tumbuhan",
    "📈 Pertumbuhan & Perkembangan", 
    "☀️ Fotosintesis & Respirasi",
    "⚠️ Stress & Adaptasi",
    "🛠️ Aplikasi Praktis",
    "🍇 Analisis Brix"
])

# ===== TAB 1: HORMON TUMBUHAN =====
with tab_hormone:
    st.header("🧪 Hormon Tumbuhan (Plant Hormones)")
    
    # Sub-tabs for different hormones
    subtab_overview, subtab_auxin, subtab_gibberellin, subtab_cytokinin, subtab_ethylene, subtab_aba, subtab_natural = st.tabs([
        "📚 Overview",
        "🌿 Auksin (Auxin)",
        "🌾 Giberelin (Gibberellin)",
        "🌱 Sitokinin (Cytokinin)",
        "🍎 Etilen (Ethylene)",
        "💧 ABA",
        "🍇 Sumber Alami"
    ])
    
    # Overview
    with subtab_overview:
        st.subheader("Pengantar Hormon Tumbuhan")
        
        st.markdown("""
        ## 🧪 APA ITU HORMON TUMBUHAN?
        
        **Hormon tumbuhan (fitohormon)** adalah senyawa organik yang diproduksi tanaman dalam jumlah kecil 
        dan berfungsi sebagai **sinyal kimia** untuk mengatur pertumbuhan, perkembangan, dan respons terhadap lingkungan.
        
        ### Karakteristik Hormon Tumbuhan:
        
        - ✅ Diproduksi dalam **jumlah sangat kecil** (ppm atau ppb)
        - ✅ Bekerja pada **lokasi berbeda** dari tempat produksi (transportasi)
        - ✅ Mengatur **proses fisiologis** spesifik
        - ✅ Bekerja secara **sinergis atau antagonis** dengan hormon lain
        - ✅ Responsif terhadap **kondisi lingkungan**
        
        ---
        
        ## 🌟 5 HORMON UTAMA TUMBUHAN
        
        ### 1. **Auksin (Auxin)** 🌿
        - **Fungsi Utama:** Pemanjangan sel, dominansi apikal, pembentukan akar
        - **Contoh:** IAA (Indole-3-Acetic Acid)
        - **Aplikasi:** Rooting hormone, parthenocarpy
        
        ### 2. **Giberelin (Gibberellin)** 🌾
        - **Fungsi Utama:** Pemanjangan batang, perkecambahan, pembungaan
        - **Contoh:** GA3, GA7
        - **Aplikasi:** Pembesaran buah (anggur), breaking dormancy
        
        ### 3. **Sitokinin (Cytokinin)** 🌱
        - **Fungsi Utama:** Pembelahan sel, penundaan senescence
        - **Contoh:** Zeatin, Kinetin
        - **Aplikasi:** Kultur jaringan, memperpanjang kesegaran
        
        ### 4. **Etilen (Ethylene)** 🍎
        - **Fungsi Utama:** Pematangan buah, abscission, senescence
        - **Contoh:** C₂H₄ (gas)
        - **Aplikasi:** Ripening control, degreening
        
        ### 5. **Asam Absisat (ABA)** 💧
        - **Fungsi Utama:** Dormansi, penutupan stomata, stress response
        - **Contoh:** ABA
        - **Aplikasi:** Drought tolerance, storage
        
        ---
        
        ## 📊 PERBANDINGAN HORMON
        
        | Hormon | Produksi | Transportasi | Fungsi Utama | Aplikasi Praktis |
        |--------|----------|--------------|--------------|------------------|
        | **Auksin** | Meristem apikal | Basipetal (atas→bawah) | Pemanjangan sel | Stek, parthenocarpy |
        | **Giberelin** | Biji, daun muda | Xylem & phloem | Pemanjangan batang | Anggur seedless |
        | **Sitokinin** | Akar | Xylem (bawah→atas) | Pembelahan sel | Kultur jaringan |
        | **Etilen** | Buah matang | Difusi (gas) | Pematangan | Ripening pisang |
        | **ABA** | Daun, akar | Xylem & phloem | Stress response | Drought tolerance |
        
        ---
        
        ## 🔄 INTERAKSI HORMON
        
        Hormon tumbuhan **TIDAK bekerja sendiri** - mereka berinteraksi!
        
        **Contoh Interaksi:**
        
        **1. Auksin + Sitokinin = Organogenesis**
        ```
        Ratio Tinggi Auksin : Rendah Sitokinin → Pembentukan AKAR
        Ratio Rendah Auksin : Tinggi Sitokinin → Pembentukan TUNAS
        Ratio Seimbang → Pembentukan KALUS
        ```
        
        **2. Giberelin + ABA = Perkecambahan**
        ```
        Giberelin ↑ + ABA ↓ → PERKECAMBAHAN
        Giberelin ↓ + ABA ↑ → DORMANSI
        ```
        
        **3. Auksin + Etilen = Abscission**
        ```
        Auksin ↑ + Etilen ↓ → Buah/Daun TETAP
        Auksin ↓ + Etilen ↑ → Buah/Daun GUGUR
        ```
        
        ---
        
        ## 💡 APLIKASI PRAKTIS
        
        **Untuk Petani:**
        
        1. **Meningkatkan Hasil Panen**
           - Gibberellin untuk pembesaran buah
           - Auksin untuk fruit set
        
        2. **Mempercepat Perkecambahan**
           - Gibberellin untuk breaking dormancy
        
        3. **Kontrol Pematangan**
           - Etilen untuk ripening
           - 1-MCP untuk menunda pematangan
        
        4. **Perbanyakan Tanaman**
           - Auksin untuk rooting
           - Sitokinin untuk kultur jaringan
        
        5. **Manajemen Stress**
           - ABA untuk drought tolerance
        
        """)
    
    # Auxin
    with subtab_auxin:
        st.subheader("🌿 Auksin (Auxin)")
        
        st.markdown("""
        ### Apa itu Auksin?
        
        **Auksin** adalah hormon tumbuhan pertama yang ditemukan (1928) dan paling banyak dipelajari.
        Nama "auxin" berasal dari bahasa Yunani **"auxein"** = tumbuh.
        
        **Jenis Auksin:**
        - **IAA (Indole-3-Acetic Acid)** - Auksin alami utama
        - **IBA (Indole-3-Butyric Acid)** - Sintetik, lebih stabil
        - **NAA (Naphthalene Acetic Acid)** - Sintetik
        - **2,4-D** - Sintetik, herbisida selektif
        
        ---
        
        ## 📍 TEMPAT PRODUKSI
        
        **Diproduksi di:**
        - ✅ Meristem apikal (ujung tunas)
        - ✅ Daun muda
        - ✅ Biji yang berkembang
        - ✅ Buah muda
        
        **Transportasi:**
        - **Basipetal** (dari atas ke bawah)
        - **Polar transport** (satu arah)
        - Melalui **parenchyma cells**
        
        ---
        
        ## 🎯 FUNGSI AUKSIN
        
        ### 1. **Pemanjangan Sel (Cell Elongation)**
        
        **Mekanisme:**
        ```
        Auksin → Aktivasi H⁺-ATPase → Pengasaman dinding sel
        → Pelonggaran dinding sel → Pemanjangan sel
        ```
        
        **Aplikasi:**
        - Pemanjangan batang
        - Pertumbuhan akar
        
        ### 2. **Dominansi Apikal (Apical Dominance)**
        
        **Prinsip:**
        - Tunas apikal (pucuk) **menghambat** pertumbuhan tunas lateral (cabang)
        - Auksin dari apex → Menghambat tunas samping
        
        **Praktis:**
        ```
        Potong pucuk (topping) → Auksin ↓ → Tunas samping tumbuh
        → Tanaman lebih lebat/bercabang
        ```
        
        ### 3. **Pembentukan Akar (Root Initiation)**
        
        **Aplikasi Penting:**
        - **Rooting hormone** untuk stek
        - Konsentrasi: 1000-5000 ppm IBA
        
        **Cara Pakai:**
        ```
        1. Celupkan ujung stek ke rooting hormone
        2. Tanam di media
        3. Akar muncul 7-14 hari
        ```
        
        ### 4. **Parthenocarpy (Buah Tanpa Biji)**
        
        **Prinsip:**
        - Auksin → Stimulasi pembentukan buah tanpa fertilisasi
        
        **Contoh:**
        - Tomat seedless
        - Timun parthenocarpic
        
        ### 5. **Phototropism & Gravitropism**
        
        **Phototropism (Respon terhadap cahaya):**
        ```
        Cahaya dari samping → Auksin terakumulasi di sisi gelap
        → Sisi gelap tumbuh lebih cepat → Batang membengkok ke cahaya
        ```
        
        **Gravitropism (Respon terhadap gravitasi):**
        ```
        Akar: Auksin ke bawah → Menghambat pertumbuhan → Akar tumbuh ke bawah
        Batang: Auksin ke bawah → Menstimulasi pertumbuhan → Batang tumbuh ke atas
        ```
        
        ---
        
        ## 💊 KONSENTRASI & EFEK
        
        **Auksin bersifat DOSE-DEPENDENT:**
        
        | Konsentrasi | Efek pada Batang | Efek pada Akar |
        |-------------|------------------|----------------|
        | **Sangat Rendah** (< 10⁻⁸ M) | Tidak ada efek | Tidak ada efek |
        | **Rendah** (10⁻⁸ - 10⁻⁶ M) | Stimulasi | Stimulasi |
        | **Optimal** (10⁻⁶ - 10⁻⁵ M) | Maksimal | Maksimal |
        | **Tinggi** (10⁻⁵ - 10⁻⁴ M) | Inhibisi | Inhibisi |
        | **Sangat Tinggi** (> 10⁻⁴ M) | Kematian sel | Kematian sel |
        
        **PENTING:**
        - Akar **lebih sensitif** dari batang (10-100x)
        - Konsentrasi optimal untuk batang = Toksik untuk akar!
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### 1. **Rooting Hormone (Hormon Perakaran)**
        
        **Produk Komersial:**
        - Rootone (IBA 0.1%)
        - Hormodin (IBA 0.1-0.8%)
        
        **Cara Aplikasi:**
        ```
        Stek batang:
        1. Potong batang 10-15 cm
        2. Celupkan ujung 2-3 cm ke rooting powder
        3. Tanam di media (pasir/cocopeat)
        4. Jaga kelembaban
        5. Akar muncul 1-3 minggu
        ```
        
        ### 2. **Fruit Set (Pembentukan Buah)**
        
        **Aplikasi:**
        - Semprot bunga dengan NAA 10-20 ppm
        - Meningkatkan fruit set 20-40%
        
        **Tanaman:**
        - Tomat, cabai, terong
        - Strawberry
        
        ### 3. **Thinning (Penjarangan Buah)**
        
        **Aplikasi:**
        - NAA 10-15 ppm saat buah kecil
        - Buah berlebih gugur → Buah tersisa lebih besar
        
        **Tanaman:**
        - Apel, pir
        - Anggur
        
        ### 4. **Herbisida Selektif**
        
        **2,4-D (Synthetic Auxin):**
        - Membunuh dikotil (broad-leaf weeds)
        - Aman untuk monokotil (padi, jagung)
        
        ---
        
        ## ⚠️ PERINGATAN
        
        1. **Konsentrasi Tepat:**
           - Terlalu rendah → Tidak efektif
           - Terlalu tinggi → Toksik
        
        2. **Waktu Aplikasi:**
           - Pagi/sore (suhu rendah)
           - Hindari siang (degradasi cepat)
        
        3. **Kombinasi:**
           - Auksin + Sitokinin untuk kultur jaringan
           - Auksin + Giberelin untuk fruit set
        
        4. **Storage:**
           - Simpan di tempat gelap, sejuk
           - Hindari panas & cahaya langsung
        
        """)
    
    # Gibberellin
    with subtab_gibberellin:
        st.subheader("🌾 Giberelin (Gibberellin)")
        
        st.markdown("""
        ### Apa itu Giberelin?
        
        **Giberelin** adalah kelompok hormon tumbuhan yang ditemukan dari jamur *Gibberella fujikuroi* (1926) 
        yang menyebabkan penyakit "bakanae" pada padi (tanaman tumbuh sangat tinggi lalu roboh).
        
        **Jenis Giberelin:**
        - Lebih dari **130 jenis** giberelin (GA1, GA2, ... GA130+)
        - Yang paling aktif: **GA3 (Gibberellic Acid)**
        - **GA7** juga sangat efektif
        
        ---
        
        ## 📍 TEMPAT PRODUKSI
        
        **Diproduksi di:**
        - ✅ Biji yang berkembang
        - ✅ Daun muda
        - ✅ Ujung akar
        - ✅ Buah muda
        
        **Transportasi:**
        - Melalui **xylem** dan **phloem** (dua arah)
        - **Non-polar** (berbeda dengan auksin)
        
        ---
        
        ## 🎯 FUNGSI GIBERELIN
        
        ### 1. **Pemanjangan Batang (Stem Elongation)**
        
        **Mekanisme:**
        ```
        GA → Aktivasi enzim → Pemanjangan sel + Pembelahan sel
        → Batang memanjang
        ```
        
        **Contoh:**
        - Tanaman dwarf (kerdil) + GA → Tumbuh normal
        - Tanaman rosette + GA → Bolting (pemanjangan batang)
        
        **Aplikasi:**
        ```
        Tanaman hias pendek → Semprot GA3 50-100 ppm
        → Batang memanjang → Lebih menarik
        ```
        
        ### 2. **Perkecambahan Biji (Seed Germination)**
        
        **Mekanisme:**
        ```
        Imbibisi air → Produksi GA → Aktivasi α-amylase
        → Hidrolisis pati → Glukosa → Energi untuk perkecambahan
        ```
        
        **Aplikasi:**
        ```
        Biji dorman → Rendam GA3 100-500 ppm (24 jam)
        → Breaking dormancy → Perkecambahan seragam
        ```
        
        **Tanaman:**
        - Lettuce, celery (light-requiring seeds)
        - Barley, wheat (cereal grains)
        
        ### 3. **Pembungaan (Flowering)**
        
        **Prinsip:**
        - GA → Substitute untuk cold requirement (vernalisasi)
        - GA → Substitute untuk long-day requirement
        
        **Aplikasi:**
        ```
        Tanaman long-day di short-day → Semprot GA3
        → Pembungaan tanpa perlu long-day
        ```
        
        **Contoh:**
        - Strawberry, lettuce
        
        ### 4. **Pembesaran Buah (Fruit Enlargement)**
        
        **Aplikasi PALING TERKENAL:**
        
        **ANGGUR SEEDLESS:**
        ```
        Anggur Thompson Seedless:
        1. Semprot GA3 20-50 ppm saat bunga mekar
        2. Semprot lagi GA3 50-100 ppm saat buah kecil
        
        Hasil:
        - Buah 2-3x lebih besar
        - Tandan lebih panjang
        - Nilai jual 3-5x lebih tinggi!
        ```
        
        **Tanaman Lain:**
        - Apel, pir (pembesaran)
        - Tomat (parthenocarpy)
        - Mandarin (seedless)
        
        ### 5. **Parthenocarpy (Buah Tanpa Biji)**
        
        **Mekanisme:**
        - GA → Stimulasi pertumbuhan ovary tanpa fertilisasi
        
        **Contoh:**
        - Anggur seedless
        - Tomat parthenocarpic
        - Mandarin seedless
        
        ---
        
        ## 💊 KONSENTRASI & APLIKASI
        
        ### Dosis GA3 untuk Berbagai Tanaman:
        
        | Tanaman | Tujuan | Konsentrasi | Waktu Aplikasi |
        |---------|--------|-------------|----------------|
        | **Anggur** | Pembesaran buah | 20-100 ppm | Bunga + Buah kecil |
        | **Padi** | Pemanjangan batang | 50-100 ppm | Fase vegetatif |
        | **Lettuce** | Perkecambahan | 100-500 ppm | Rendam biji 24 jam |
        | **Strawberry** | Pembungaan | 10-50 ppm | Sebelum bunga |
        | **Tomat** | Fruit set | 10-20 ppm | Saat bunga |
        | **Apel** | Pembesaran | 10-30 ppm | Buah kecil |
        | **Mandarin** | Seedless | 10-20 ppm | Bunga |
        
        ---
        
        ## 🍇 SUMBER ALAMI GIBERELIN
        
        ### **ANGGUR HIJAU (Green Grapes)**
        
        **Kenapa Anggur Hijau?**
        - Anggur muda mengandung **GA3 dan GA7** tinggi
        - Konsentrasi tertinggi saat buah **2-4 minggu setelah fruit set**
        - Lebih murah dari GA sintetik!
        
        **Cara Membuat Ekstrak GA Alami:**
        
        ```
        BAHAN:
        - 1 kg anggur hijau muda (2-4 minggu setelah fruit set)
        - 2 liter air
        - Blender
        - Kain saring
        
        CARA:
        1. Cuci bersih anggur hijau
        2. Blender dengan 1 liter air (5-10 menit)
        3. Saring dengan kain halus
        4. Tambahkan air hingga 2 liter
        5. Aduk rata
        
        PENGGUNAAN:
        - Semprot langsung (konsentrasi ~50-100 ppm GA equivalent)
        - Atau encerkan 1:1 dengan air (25-50 ppm)
        - Aplikasi pagi/sore hari
        - Ulangi setiap 7-10 hari
        
        PENYIMPANAN:
        - Simpan di kulkas (tahan 3-5 hari)
        - Atau keringkan menjadi powder (tahan lebih lama)
        ```
        
        **Efektivitas:**
        - **70-80%** efektif dibanding GA3 sintetik
        - **Lebih aman** (organik)
        - **Lebih murah** (bisa buat sendiri)
        
        ### **SUMBER ALAMI LAIN:**
        
        **1. Kecambah (Sprouts)**
        - Kecambah kacang hijau, kedelai
        - Tinggi GA saat perkecambahan
        
        **Cara:**
        ```
        1. Rendam kacang 8-12 jam
        2. Kecambahkan 3-5 hari
        3. Blender kecambah dengan air (1:2)
        4. Saring dan aplikasikan
        ```
        
        **2. Rumput Laut (Seaweed)**
        - Mengandung GA alami + sitokinin
        - Produk komersial: Seaweed extract
        
        **3. Kompos Jamur**
        - Jamur produksi GA
        - Kompos jamur → GA residual
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### **Kasus 1: Anggur Seedless**
        
        **Problem:** Anggur seedless ukuran kecil, nilai jual rendah
        
        **Solusi:**
        ```
        Aplikasi GA3:
        1. Saat bunga mekar (bloom): 20-30 ppm
        2. Saat buah kecil (berry set): 50-100 ppm
        3. 2 minggu kemudian: 50-100 ppm (optional)
        
        Atau Ekstrak Anggur Hijau:
        1. Saat bunga mekar: Ekstrak 100% (undiluted)
        2. Saat buah kecil: Ekstrak 100%
        3. Ulangi 7-10 hari kemudian
        
        Hasil:
        - Buah 2-3x lebih besar
        - Tandan lebih panjang
        - Nilai jual naik 200-300%!
        ```
        
        ### **Kasus 2: Breaking Dormancy Biji**
        
        **Problem:** Biji lettuce tidak berkecambah di suhu tinggi
        
        **Solusi:**
        ```
        1. Rendam biji di GA3 100-200 ppm (24 jam)
        2. Atau rendam di ekstrak kecambah (24 jam)
        3. Keringkan sedikit
        4. Tanam normal
        
        Hasil:
        - Perkecambahan 80-90% (vs 20-30% tanpa GA)
        - Lebih seragam
        ```
        
        ### **Kasus 3: Pembesaran Buah Tomat**
        
        **Problem:** Fruit set rendah, buah kecil
        
        **Solusi:**
        ```
        1. Semprot GA3 10-20 ppm saat bunga mekar
        2. Atau semprot ekstrak anggur hijau (encerkan 1:1)
        3. Ulangi setiap minggu selama pembungaan
        
        Hasil:
        - Fruit set naik 30-50%
        - Buah lebih besar
        - Panen lebih awal 5-7 hari
        ```
        
        ---
        
        ## ⚠️ PERINGATAN
        
        ### **1. Dosis Berlebihan:**
        ```
        Gejala:
        - Batang terlalu panjang (lodging)
        - Daun pucat (chlorosis)
        - Buah pecah (cracking)
        
        Solusi:
        - Kurangi dosis 50%
        - Perpanjang interval aplikasi
        ```
        
        ### **2. Waktu Aplikasi:**
        ```
        BENAR:
        - Pagi (6-9 AM) atau Sore (4-6 PM)
        - Suhu sejuk, tidak hujan
        
        SALAH:
        - Siang hari (degradasi cepat)
        - Saat hujan (tercuci)
        ```
        
        ### **3. Kombinasi:**
        ```
        BAIK:
        - GA + Auksin (fruit set)
        - GA + Sitokinin (kultur jaringan)
        
        HINDARI:
        - GA + ABA (antagonis!)
        - GA + Retardant (berlawanan)
        ```
        
        ### **4. Tanaman Sensitif:**
        ```
        HATI-HATI:
        - Padi (bisa lodging)
        - Wheat (batang lemah)
        
        AMAN:
        - Anggur, tomat, lettuce
        - Strawberry, apel
        ```
        
        ---
        
        ## 💡 TIPS SUKSES
        
        **1. Mulai Rendah:**
        - Coba dosis terendah dulu
        - Naikkan bertahap jika perlu
        
        **2. Konsistensi:**
        - Aplikasi teratur (7-10 hari)
        - Jangan skip
        
        **3. Monitoring:**
        - Catat respons tanaman
        - Adjust dosis sesuai hasil
        
        **4. Ekonomis:**
        - Buat ekstrak sendiri (anggur hijau, kecambah)
        - Lebih murah, tetap efektif
        
        **5. Dokumentasi:**
        - Foto before-after
        - Ukur pertumbuhan
        - Hitung ROI
        
        """)
    
    # Cytokinin
    with subtab_cytokinin:
        st.subheader("🌱 Sitokinin (Cytokinin)")
        
        st.markdown("""
        ### Apa itu Sitokinin?
        
        **Sitokinin** adalah hormon tumbuhan yang merangsang **pembelahan sel (cytokinesis)** dan **penundaan penuaan (anti-senescence)**.
        Nama "cytokinin" berasal dari "cytokinesis" = pembelahan sel.
        
        **Jenis Sitokinin:**
        - **Zeatin** - Sitokinin alami utama (dari jagung)
        - **Kinetin** - Sintetik pertama (dari DNA)
        - **BAP (6-Benzylaminopurine)** - Sintetik, paling umum
        - **TDZ (Thidiazuron)** - Sintetik, sangat kuat
        
        **Sumber:**
        - Taub, D. R., & Goldberg, R. (1996). Plant Physiology, 110(4), 1103-1109
        - Mok, D. W., & Mok, M. C. (2001). Annual Review of Plant Biology, 52, 89-118
        
        ---
        
        ## 📍 TEMPAT PRODUKSI
        
        **Diproduksi di:**
        - ✅ **Akar** (terutama ujung akar)
        - ✅ Biji yang berkembang
        - ✅ Buah muda
        - ✅ Jaringan meristematik
        
        **Transportasi:**
        - Melalui **xylem** (dari akar ke atas)
        - **Acropetal** (dari bawah ke atas)
        - Berlawanan dengan auksin!
        
        **Referensi:**
        - Sakakibara, H. (2006). Annual Review of Plant Biology, 57, 431-449
        
        ---
        
        ## 🎯 FUNGSI SITOKININ
        
        ### 1. **Pembelahan Sel (Cell Division)**
        
        **Mekanisme:**
        ```
        Sitokinin → Aktivasi cyclin-dependent kinases (CDKs)
        → Progresi siklus sel → Pembelahan sel
        ```
        
        **Aplikasi:**
        - Kultur jaringan (kalus formation)
        - Organogenesis (tunas formation)
        - Meristem activation
        
        **Referensi:**
        - Riou-Khamlichi, C., et al. (1999). Science, 283(5407), 1541-1544
        
        ### 2. **Penundaan Senescence (Anti-Aging)**
        
        **Prinsip:**
        - Sitokinin **menunda** penuaan daun
        - Mempertahankan klorofil
        - Mencegah degradasi protein
        
        **Mekanisme:**
        ```
        Sitokinin → Inhibisi degradasi klorofil
        → Daun tetap hijau lebih lama
        → Fotosintesis lebih lama
        ```
        
        **Aplikasi Praktis:**
        ```
        Sayuran potong (lettuce, spinach):
        - Semprot sitokinin 10-50 ppm sebelum panen
        - Kesegaran bertahan 2-3x lebih lama
        - Nilai jual lebih tinggi
        ```
        
        **Referensi:**
        - Gan, S., & Amasino, R. M. (1995). Science, 270(5244), 1986-1988
        
        ### 3. **Pelepasan Dormansi Tunas Lateral**
        
        **Prinsip:**
        - Sitokinin **melawan** dominansi apikal (auksin)
        - Merangsang pertumbuhan tunas samping
        
        **Ratio Auksin:Sitokinin:**
        ```
        Auksin tinggi : Sitokinin rendah → Dominansi apikal
        Auksin rendah : Sitokinin tinggi → Tunas lateral tumbuh
        ```
        
        **Aplikasi:**
        ```
        Tanaman hias (krisan, mawar):
        - Semprot BAP 50-100 ppm
        - Tunas samping tumbuh
        - Tanaman lebih lebat/bushy
        ```
        
        ### 4. **Mobilisasi Nutrisi (Nutrient Sink)**
        
        **Prinsip:**
        - Sitokinin → Jaringan menjadi "sink" (penarik nutrisi)
        - Nutrisi dialihkan ke area dengan sitokinin tinggi
        
        **Contoh:**
        ```
        Buah/biji → Sitokinin tinggi → Nutrisi tertarik ke buah
        Daun tua → Sitokinin rendah → Nutrisi keluar (senescence)
        ```
        
        **Referensi:**
        - Roitsch, T., & Ehneß, R. (2000). Plant Biology, 2(02), 129-138
        
        ### 5. **Pembentukan Kloroplas**
        
        **Mekanisme:**
        - Sitokinin → Diferensiasi kloroplas
        - Meningkatkan kandungan klorofil
        - Daun lebih hijau
        
        ---
        
        ## 💊 KONSENTRASI & APLIKASI
        
        ### Dosis Sitokinin untuk Berbagai Aplikasi:
        
        | Aplikasi | Konsentrasi | Metode | Hasil |
        |----------|-------------|--------|-------|
        | **Kultur Jaringan** | 0.5-5 mg/L BAP | Media | Tunas formation |
        | **Anti-Senescence** | 10-50 ppm | Foliar spray | Kesegaran 2-3x |
        | **Tunas Lateral** | 50-100 ppm BAP | Foliar spray | Branching |
        | **Pembesaran Buah** | 5-20 ppm | Spray | Ukuran +20-30% |
        | **Kesegaran Bunga** | 10-30 ppm | Spray/dip | Vase life +50% |
        
        **Referensi:**
        - Skoog, F., & Miller, C. O. (1957). Symposia of the Society for Experimental Biology, 11, 118-130
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### 1. **Kultur Jaringan (Tissue Culture)**
        
        **Formula MS Medium + Sitokinin:**
        ```
        Media Dasar: MS (Murashige & Skoog)
        Auksin (NAA): 0.1-1 mg/L
        Sitokinin (BAP): 0.5-5 mg/L
        
        Ratio:
        - Auksin > Sitokinin → Akar
        - Auksin < Sitokinin → Tunas
        - Auksin = Sitokinin → Kalus
        ```
        
        **Aplikasi:**
        - Perbanyakan tanaman (micropropagation)
        - Konservasi germplasm
        - Produksi tanaman bebas virus
        
        **Referensi:**
        - Murashige, T., & Skoog, F. (1962). Physiologia Plantarum, 15(3), 473-497
        
        ### 2. **Memperpanjang Kesegaran Sayuran**
        
        **Produk Komersial:**
        - ProFresh (BAP 10 ppm)
        - ReTain (AVG + Cytokinin)
        
        **DIY Formula:**
        ```
        BAHAN:
        - Air kelapa 100 mL (sitokinin alami)
        - Air 900 mL
        - Gula 1 sendok teh (spreader)
        
        APLIKASI:
        - Semprot sayuran 1-2 hari sebelum panen
        - Atau celup setelah panen (30 detik)
        - Kesegaran +2-3 hari
        ```
        
        ### 3. **Meningkatkan Branching (Percabangan)**
        
        **Tanaman Hias:**
        ```
        Krisan, Mawar, Poinsettia:
        - Semprot BAP 50-100 ppm
        - Aplikasi 2-3x (interval 7 hari)
        - Tunas lateral +50-100%
        - Tanaman lebih penuh/bushy
        ```
        
        ### 4. **Pembesaran Buah**
        
        **Aplikasi:**
        ```
        Anggur, Apel, Kiwi:
        - Semprot sitokinin 5-20 ppm saat fruit set
        - Kombinasi dengan GA untuk efek maksimal
        - Ukuran buah +20-30%
        - Cell division meningkat
        ```
        
        **Referensi:**
        - Zhang, C., & Whiting, M. D. (2011). HortScience, 46(6), 865-870
        
        ### 5. **Memperpanjang Vase Life Bunga Potong**
        
        **Formula:**
        ```
        Preservative Solution:
        - Sucrose: 2-4%
        - Citric acid: 200 ppm
        - BAP: 10-30 ppm
        - Silver thiosulfate: 0.2 mM (optional)
        
        Hasil:
        - Vase life +50-100%
        - Daun tetap hijau
        - Bunga segar lebih lama
        ```
        
        **Referensi:**
        - van Doorn, W. G., & Woltering, E. J. (2008). Postharvest Biology and Technology, 50(2-3), 89-99
        
        ---
        
        ## 🥥 SUMBER ALAMI SITOKININ
        
        ### **1. AIR KELAPA (Coconut Water)**
        
        **Kandungan:**
        - **Zeatin:** 10-50 ppm (TINGGI!)
        - **Zeatin riboside:** 5-20 ppm
        - Plus: Gula, mineral, vitamin
        
        **Aplikasi:**
        ```
        Kultur Jaringan:
        - 10-20% air kelapa dalam media MS
        - Meningkatkan shoot formation
        - Lebih ekonomis dari BAP sintetik
        
        Foliar Spray:
        - Encerkan 1:1 dengan air
        - Semprot setiap 7-10 hari
        - Anti-senescence, kesegaran daun
        ```
        
        **Referensi:**
        - Yong, J. W., et al. (2009). Molecules, 14(12), 5144-5164
        
        ### **2. EKSTRAK RUMPUT LAUT (Seaweed Extract)**
        
        **Kandungan:**
        - Sitokinin: 10-50 ppm
        - Betaine, mineral, growth factors
        
        **Produk Komersial:**
        - Maxicrop, Seasol, Kelpak
        
        **DIY:**
        ```
        1 kg rumput laut segar → Rendam 5L air (2-3 minggu)
        → Saring → Encerkan 1:10 untuk aplikasi
        ```
        
        ### **3. EKSTRAK KECAMBAH**
        
        **Kandungan:**
        - Sitokinin: 10-30 ppm
        - Plus GA, auksin
        
        **Cara:**
        ```
        Kecambah alfalfa/kacang hijau (3-5 hari)
        → Blender dengan air (1:2)
        → Saring → Aplikasikan
        ```
        
        ---
        
        ## ⚠️ PERINGATAN
        
        ### 1. **Dosis Berlebihan:**
        ```
        Gejala:
        - Daun kecil-kecil (abnormal)
        - Tunas terlalu banyak (kompetisi)
        - Pertumbuhan terhambat
        
        Solusi:
        - Kurangi dosis 50%
        - Perpanjang interval
        ```
        
        ### 2. **Interaksi dengan Auksin:**
        ```
        PENTING:
        - Ratio Auksin:Sitokinin sangat penting!
        - Terlalu banyak sitokinin → Tunas berlebihan
        - Terlalu sedikit → Tidak ada efek
        
        Optimal:
        - Kultur jaringan: 1:1 sampai 1:10 (Auksin:Sitokinin)
        - Foliar spray: Sitokinin saja (atau + GA)
        ```
        
        ### 3. **Waktu Aplikasi:**
        ```
        BENAR:
        - Pagi/sore (suhu sejuk)
        - Fase vegetatif aktif
        - Sebelum stress (panas, kekeringan)
        
        SALAH:
        - Siang hari (degradasi)
        - Saat tanaman stress
        - Terlalu sering (waste)
        ```
        
        ---
        
        ## 💡 TIPS PRAKTIS
        
        **1. Untuk Kultur Jaringan:**
        - Start dengan BAP 1 mg/L
        - Adjust berdasarkan respons
        - Combine dengan auksin untuk organogenesis
        
        **2. Untuk Anti-Senescence:**
        - Aplikasi 1-2 hari sebelum panen
        - Atau gunakan air kelapa (ekonomis)
        - Efektif untuk sayuran daun
        
        **3. Untuk Branching:**
        - Aplikasi saat tanaman muda
        - 2-3x aplikasi (interval 7 hari)
        - Combine dengan topping untuk efek maksimal
        
        **4. Ekonomis:**
        - Gunakan air kelapa (alami, murah)
        - Atau seaweed extract
        - Efektivitas 60-80% vs sintetik
        
        **5. Storage:**
        - Sitokinin stabil di suhu rendah
        - Simpan stock solution di freezer
        - Working solution di kulkas (1-2 minggu)
        
        ---
        
        ## 📚 REFERENSI ILMIAH
        
        1. **Mok, D. W., & Mok, M. C. (2001).** Cytokinin metabolism and action. Annual Review of Plant Biology, 52, 89-118.
        
        2. **Sakakibara, H. (2006).** Cytokinins: activity, biosynthesis, and translocation. Annual Review of Plant Biology, 57, 431-449.
        
        3. **Gan, S., & Amasino, R. M. (1995).** Inhibition of leaf senescence by autoregulated production of cytokinin. Science, 270(5244), 1986-1988.
        
        4. **Murashige, T., & Skoog, F. (1962).** A revised medium for rapid growth and bio assays with tobacco tissue cultures. Physiologia Plantarum, 15(3), 473-497.
        
        5. **Yong, J. W., et al. (2009).** The chemical composition and biological properties of coconut (Cocos nucifera L.) water. Molecules, 14(12), 5144-5164.
        
        """)
    
    # Ethylene
    with subtab_ethylene:
        st.subheader("🍎 Etilen (Ethylene)")
        
        st.markdown("""
        ### Apa itu Etilen?
        
        **Etilen (C₂H₄)** adalah hormon tumbuhan berbentuk **GAS** yang mengatur pematangan buah, penuaan, dan abscission.
        Etilen adalah molekul organik paling sederhana yang berfungsi sebagai hormon.
        
        **Karakteristik Unik:**
        - ✅ Satu-satunya hormon berbentuk **gas**
        - ✅ Dapat berdifusi melalui udara
        - ✅ Sangat potent (aktif pada konsentrasi ppb!)
        - ✅ Diproduksi oleh semua bagian tanaman
        
        **Sumber:**
        - Abeles, F. B., et al. (1992). Ethylene in Plant Biology. Academic Press.
        - Bleecker, A. B., & Kende, H. (2000). Annual Review of Cell and Developmental Biology, 16, 1-18
        
        ---
        
        ## 📍 PRODUKSI & BIOSINTESIS
        
        **Jalur Biosintesis:**
        ```
        Methionine → SAM (S-Adenosyl Methionine)
        → ACC (1-Aminocyclopropane-1-Carboxylic Acid)
        → Ethylene (C₂H₄)
        ```
        
        **Enzim Kunci:**
        - **ACS (ACC Synthase)** - Rate-limiting step
        - **ACO (ACC Oxidase)** - Konversi ACC → Ethylene
        
        **Diproduksi di:**
        - ✅ Buah matang (TINGGI!)
        - ✅ Bunga yang layu
        - ✅ Daun yang menua
        - ✅ Jaringan yang terluka
        - ✅ Akar (saat stress)
        
        **Referensi:**
        - Yang, S. F., & Hoffman, N. E. (1984). Annual Review of Plant Physiology, 35, 155-189
        
        ---
        
        ## 🎯 FUNGSI ETILEN
        
        ### 1. **Pematangan Buah (Fruit Ripening)**
        
        **Mekanisme:**
        ```
        Etilen → Aktivasi enzim:
        - Pectinase → Pelunakan dinding sel
        - Amylase → Konversi pati → gula
        - Chlorophyllase → Degradasi klorofil
        - Carotenoid synthesis → Warna (merah, kuning)
        
        Hasil: Buah matang (lunak, manis, berwarna)
        ```
        
        **Buah Klimakterik vs Non-Klimakterik:**
        
        | Klimakterik | Non-Klimakterik |
        |-------------|-----------------|
        | Produksi etilen ↑↑ saat matang | Produksi etilen rendah |
        | Bisa matang setelah panen | Harus matang di pohon |
        | Contoh: Pisang, tomat, apel, mangga | Contoh: Anggur, jeruk, strawberry |
        
        **Referensi:**
        - Giovannoni, J. J. (2004). Annual Review of Plant Biology, 55, 521-551
        
        ### 2. **Abscission (Gugur Daun/Buah)**
        
        **Mekanisme:**
        ```
        Etilen ↑ + Auksin ↓ → Aktivasi cellulase & polygalacturonase
        → Degradasi dinding sel di abscission zone
        → Daun/buah gugur
        ```
        
        **Aplikasi:**
        - Defoliation (gugurkan daun sebelum panen)
        - Fruit thinning (penjarangan buah)
        
        **Referensi:**
        - Patterson, S. E. (2001). Plant Molecular Biology, 46(1), 1-19
        
        ### 3. **Senescence (Penuaan)**
        
        **Prinsip:**
        - Etilen → Mempercepat penuaan
        - Degradasi klorofil, protein, membran
        - "The death hormone"
        
        **Contoh:**
        - Bunga potong → Etilen tinggi → Cepat layu
        - Sayuran → Etilen → Menguning
        
        ### 4. **Triple Response (Respon Gelap)**
        
        **Pada seedling di gelap + etilen:**
        ```
        1. Inhibisi pemanjangan batang
        2. Penebalan batang
        3. Pertumbuhan horizontal (epinasty)
        
        Fungsi: Membantu seedling menembus tanah
        ```
        
        ### 5. **Sex Expression (Ekspresi Kelamin)**
        
        **Pada tanaman monoecious (timun, melon):**
        ```
        Etilen ↑ → Bunga betina ↑
        Etilen ↓ → Bunga jantan ↑
        
        Aplikasi:
        - Ethephon → Meningkatkan bunga betina
        - Hasil panen lebih tinggi
        ```
        
        **Referensi:**
        - Yamasaki, S., et al. (2003). Plant and Cell Physiology, 44(12), 1350-1358
        
        ---
        
        ## 💊 KONSENTRASI & APLIKASI
        
        ### Etilen dalam Berbagai Aplikasi:
        
        | Aplikasi | Konsentrasi | Metode | Hasil |
        |----------|-------------|--------|-------|
        | **Ripening Pisang** | 100-150 ppm | Gas chamber | Matang 3-5 hari |
        | **Degreening Jeruk** | 1-5 ppm | Gas chamber | Warna kuning |
        | **Defoliation Kapas** | Ethephon 500-1000 ppm | Spray | Gugur daun |
        | **Bunga Betina (Timun)** | Ethephon 100-250 ppm | Spray | Bunga betina +50% |
        | **Inhibisi (1-MCP)** | 0.5-1 ppm | Gas chamber | Tunda matang 2-4x |
        
        **Referensi:**
        - Saltveit, M. E. (1999). Postharvest Biology and Technology, 15(3), 279-292
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### 1. **Ripening Buah (Pematangan)**
        
        **Metode Tradisional:**
        ```
        PISANG MATANG CEPAT:
        1. Masukkan pisang hijau dalam kardus/plastik tertutup
        2. Tambahkan 1-2 buah apel/pisang matang (sumber etilen)
        3. Tutup rapat
        4. Suhu 20-25°C
        5. Matang dalam 2-3 hari
        
        Prinsip: Apel/pisang matang → Etilen → Pisang hijau matang
        ```
        
        **Metode Komersial:**
        ```
        RIPENING ROOM:
        1. Suhu: 18-20°C
        2. Humidity: 90-95%
        3. Etilen gas: 100-150 ppm
        4. Ventilasi: Sirkulasi udara
        5. Durasi: 24-48 jam
        
        Hasil: Matang seragam, kualitas baik
        ```
        
        **Ethephon (Ethrel) - Etilen Cair:**
        ```
        Aplikasi:
        - Ethephon 500-1000 ppm
        - Spray buah hijau
        - Ethephon → Release etilen
        - Matang 3-5 hari
        
        Tanaman: Tomat, pisang, mangga
        ```
        
        ### 2. **Menunda Pematangan (Anti-Ethylene)**
        
        **1-MCP (1-Methylcyclopropene):**
        ```
        Mekanisme:
        - 1-MCP → Blok reseptor etilen
        - Etilen tidak bisa bekerja
        - Pematangan tertunda
        
        Aplikasi:
        - Konsentrasi: 0.5-1 ppm (gas)
        - Durasi: 12-24 jam (sealed chamber)
        - Hasil: Shelf-life +2-4x
        
        Produk Komersial: SmartFresh, RipeLock
        ```
        
        **Referensi:**
        - Watkins, C. B. (2006). Biotechnology Advances, 24(4), 389-409
        
        **Absorber Etilen:**
        ```
        Potassium Permanganate (KMnO₄):
        - Absorb etilen dari udara
        - Sachet dalam packaging
        - Perpanjang kesegaran
        
        Aplikasi: Buah, sayur, bunga potong
        ```
        
        ### 3. **Degreening (Penghijauan → Kuning)**
        
        **Jeruk, Lemon:**
        ```
        Problem: Buah matang tapi masih hijau (suhu tinggi)
        
        Solusi:
        1. Etilen 1-5 ppm (gas chamber)
        2. Suhu: 20-25°C
        3. Humidity: 90-95%
        4. Durasi: 2-5 hari
        
        Hasil:
        - Klorofil degradasi
        - Warna kuning/orange muncul
        - Rasa tidak berubah (sudah matang)
        ```
        
        **Referensi:**
        - Goldschmidt, E. E. (1988). HortScience, 23(1), 42-44
        
        ### 4. **Defoliation (Gugurkan Daun)**
        
        **Kapas:**
        ```
        Tujuan: Gugurkan daun sebelum panen (mekanis)
        
        Aplikasi:
        - Ethephon 500-1000 ppm
        - Spray 7-14 hari sebelum panen
        - Daun gugur 90-100%
        - Panen lebih mudah, bersih
        ```
        
        ### 5. **Meningkatkan Bunga Betina**
        
        **Timun, Melon:**
        ```
        Aplikasi:
        - Ethephon 100-250 ppm
        - Spray saat 2-4 daun sejati
        - Bunga betina +50-100%
        - Hasil panen lebih tinggi
        ```
        
        **Referensi:**
        - Rudich, J., et al. (1972). Plant Physiology, 50(5), 585-590
        
        ---
        
        ## 🍎 SUMBER ETILEN ALAMI
        
        ### **Buah Klimakterik (Penghasil Etilen Tinggi):**
        
        | Buah | Produksi Etilen | Sensitivitas | Aplikasi |
        |------|-----------------|--------------|----------|
        | **Apel** | Tinggi (10-100 ppm) | Tinggi | Ripening agent |
        | **Pisang** | Sangat Tinggi (100-200 ppm) | Sangat Tinggi | Ripening agent |
        | **Tomat** | Tinggi (10-50 ppm) | Tinggi | Ripening |
        | **Alpukat** | Tinggi (50-100 ppm) | Tinggi | Ripening |
        | **Mangga** | Tinggi (20-80 ppm) | Tinggi | Ripening |
        
        **Cara Pakai:**
        ```
        Matangkan buah lain:
        1. Letakkan buah klimakterik matang (apel/pisang)
        2. Bersama buah yang ingin dimatangkan
        3. Dalam wadah tertutup
        4. Suhu ruang (20-25°C)
        5. Cek setiap hari
        ```
        
        ### **Hindari Kombinasi:**
        ```
        JANGAN SIMPAN BERSAMA:
        - Apel + Wortel → Wortel pahit
        - Pisang + Kentang → Kentang cepat berkecambah
        - Tomat + Lettuce → Lettuce cepat busuk
        
        Prinsip: Etilen dari buah klimakterik → Rusak sayuran
        ```
        
        ---
        
        ## ⚠️ PERINGATAN
        
        ### 1. **Etilen Berlebihan:**
        ```
        Gejala:
        - Buah terlalu cepat matang → Busuk
        - Daun menguning, gugur
        - Bunga layu prematur
        - Sayuran rusak
        
        Solusi:
        - Ventilasi baik (buang etilen)
        - Pisahkan buah klimakterik
        - Gunakan absorber etilen
        - Suhu rendah (slow down production)
        ```
        
        ### 2. **Storage & Transport:**
        ```
        PENTING:
        - Jangan campur buah klimakterik dengan non-klimakterik
        - Ventilasi baik (buang etilen)
        - Suhu rendah (reduce production)
        - Gunakan 1-MCP untuk long-distance transport
        ```
        
        ### 3. **Timing Aplikasi:**
        ```
        Ethephon:
        - Jangan terlalu dini (buah belum siap)
        - Jangan terlalu lambat (sudah matang)
        - Optimal: Physiological maturity (matang fisiologis)
        ```
        
        ---
        
        ## 💡 TIPS PRAKTIS
        
        **1. Ripening di Rumah:**
        - Gunakan apel/pisang matang sebagai sumber etilen
        - Kardus/plastik tertutup (konsentrasi etilen tinggi)
        - Suhu ruang, cek setiap hari
        
        **2. Perpanjang Kesegaran:**
        - Pisahkan buah klimakterik dari sayuran
        - Ventilasi baik di kulkas
        - Gunakan absorber etilen (DIY: arang aktif)
        
        **3. Bunga Potong:**
        - Hindari etilen (jauhkan dari buah)
        - Gunakan STS (Silver Thiosulfate) - blok etilen
        - Suhu rendah (slow down senescence)
        
        **4. Komersial:**
        - Invest in ripening room (kontrol presisi)
        - Gunakan 1-MCP untuk transport jarak jauh
        - Monitor etilen level (sensor)
        
        ---
        
        ## 📚 REFERENSI ILMIAH
        
        1. **Abeles, F. B., et al. (1992).** Ethylene in Plant Biology. Academic Press.
        
        2. **Bleecker, A. B., & Kende, H. (2000).** Ethylene: a gaseous signal molecule in plants. Annual Review of Cell and Developmental Biology, 16, 1-18.
        
        3. **Giovannoni, J. J. (2004).** Genetic regulation of fruit development and ripening. The Plant Cell, 16, S170-S180.
        
        4. **Saltveit, M. E. (1999).** Effect of ethylene on quality of fresh fruits and vegetables. Postharvest Biology and Technology, 15(3), 279-292.
        
        5. **Watkins, C. B. (2006).** The use of 1-methylcyclopropene (1-MCP) on fruits and vegetables. Biotechnology Advances, 24(4), 389-409.
        
        """)
    
    # ABA
    with subtab_aba:
        st.subheader("💧 Asam Absisat (ABA)")
        
        st.markdown("""
        ### Apa itu ABA?
        
        **ABA (Abscisic Acid)** adalah hormon "stress" yang membantu tanaman bertahan dalam kondisi tidak menguntungkan.
        Awalnya dikira mengatur abscission (gugur), tapi ternyata fungsi utamanya adalah **stress response**.
        
        **Karakteristik:**
        - ✅ "Stress hormone" atau "Growth inhibitor"
        - ✅ Antagonis dari gibberellin & sitokinin
        - ✅ Krusial untuk survival tanaman
        - ✅ Meningkat drastis saat stress
        
        **Sumber:**
        - Finkelstein, R. (2013). Annual Review of Plant Biology, 64, 429-450
        - Cutler, S. R., et al. (2010). Annual Review of Plant Biology, 61, 651-679
        
        ---
        
        ## 📍 PRODUKSI & BIOSINTESIS
        
        **Jalur Biosintesis:**
        ```
        Carotenoids (Zeaxanthin) → Violaxanthin
        → Neoxanthin → Xanthoxin → ABA
        ```
        
        **Diproduksi di:**
        - ✅ **Daun** (saat kekeringan)
        - ✅ **Akar** (saat stress air)
        - ✅ **Biji** (dormansi)
        - ✅ **Buah** (pematangan)
        
        **Transportasi:**
        - Xylem & phloem (dua arah)
        - Signal dari akar → daun (water stress)
        
        **Referensi:**
        - Nambara, E., & Marion-Poll, A. (2005). Annual Review of Plant Biology, 56, 165-185
        
        ---
        
        ## 🎯 FUNGSI ABA
        
        ### 1. **Penutupan Stomata (Drought Response)**
        
        **Mekanisme:**
        ```
        Kekeringan → ABA ↑ di akar
        → ABA transport ke daun
        → Aktivasi ion channels di guard cells
        → K⁺ dan Cl⁻ keluar dari guard cells
        → Air keluar → Guard cells mengempis
        → Stomata MENUTUP
        → Transpirasi ↓ → Konservasi air
        ```
        
        **Kecepatan:**
        - Stomata menutup dalam **10-15 menit** setelah ABA
        - Sangat cepat dan efektif!
        
        **Referensi:**
        - Schroeder, J. I., et al. (2001). Annual Review of Plant Physiology and Plant Molecular Biology, 52, 627-658
        
        ### 2. **Dormansi Biji (Seed Dormancy)**
        
        **Prinsip:**
        ```
        ABA tinggi → Biji dorman (tidak berkecambah)
        ABA rendah → Biji berkecambah
        
        Balance:
        ABA (inhibitor) vs GA (promoter)
        ```
        
        **Fungsi:**
        - Mencegah perkecambahan prematur (di buah)
        - Survival saat kondisi tidak optimal
        - Perkecambahan saat kondisi baik
        
        **Aplikasi:**
        ```
        Breaking Dormancy:
        - Stratifikasi dingin → ABA ↓
        - Gibberellin → Antagonis ABA
        - Perkecambahan seragam
        ```
        
        **Referensi:**
        - Finkelstein, R., et al. (2008). The Plant Cell, 20(12), 2981-2992
        
        ### 3. **Inhibisi Pertumbuhan (Growth Inhibition)**
        
        **Mekanisme:**
        - ABA → Inhibisi pemanjangan sel
        - Antagonis gibberellin
        - "Pause" pertumbuhan saat stress
        
        **Contoh:**
        ```
        Kekeringan → ABA ↑
        → Pertumbuhan berhenti
        → Energi dialihkan untuk survival
        → Setelah hujan → ABA ↓ → Pertumbuhan lanjut
        ```
        
        ### 4. **Toleransi Stress Abiotik**
        
        **Jenis Stress:**
        - **Drought** (kekeringan)
        - **Salinity** (salinitas)
        - **Cold** (dingin)
        - **Heat** (panas)
        
        **Mekanisme:**
        ```
        Stress → ABA ↑
        → Ekspresi stress-responsive genes
        → Produksi:
          - Osmoprotectants (proline, betaine)
          - Antioxidants (SOD, CAT)
          - Heat shock proteins (HSPs)
          - LEA proteins
        → Toleransi meningkat
        ```
        
        **Referensi:**
        - Zhu, J. K. (2002). Annual Review of Plant Biology, 53, 247-273
        
        ### 5. **Senescence & Abscission**
        
        **Prinsip:**
        - ABA → Mempercepat penuaan daun
        - ABA → Promosi abscission (dengan etilen)
        
        **Contoh:**
        - Daun tua → ABA tinggi → Menguning, gugur
        - Stress → ABA tinggi → Premature senescence
        
        ---
        
        ## 💊 KONSENTRASI & APLIKASI
        
        ### ABA dalam Berbagai Aplikasi:
        
        | Aplikasi | Konsentrasi | Metode | Hasil |
        |----------|-------------|--------|-------|
        | **Drought Tolerance** | 10-100 μM | Foliar spray | Stomata closure |
        | **Seed Priming** | 1-10 μM | Seed soak | Stress tolerance |
        | **Storage** | 50-100 ppm | Spray | Dormansi, shelf-life |
        | **Transplant** | 10-50 μM | Root dip | Survival rate ↑ |
        | **Fruit Storage** | 100-500 ppm | Spray | Delay ripening |
        
        **Referensi:**
        - Travaglia, C., et al. (2007). Plant Growth Regulation, 53(1), 1-9
        
        ---
        
        ## 🛠️ APLIKASI PRAKTIS
        
        ### 1. **Meningkatkan Drought Tolerance**
        
        **Priming Benih:**
        ```
        CARA:
        1. Rendam benih di ABA 1-10 μM (24 jam)
        2. Keringkan
        3. Tanam normal
        
        HASIL:
        - Toleransi kekeringan +30-50%
        - Survival rate lebih tinggi
        - Yield lebih stabil saat kekeringan
        ```
        
        **Foliar Application:**
        ```
        CARA:
        1. Semprot ABA 10-50 μM
        2. 1-2 hari sebelum stress (kekeringan, transplant)
        3. Atau saat stress ringan
        
        HASIL:
        - Stomata menutup → Transpirasi ↓
        - Water use efficiency ↑
        - Survival saat kekeringan
        ```
        
        **Referensi:**
        - Travaglia, C., et al. (2007). Plant Growth Regulation, 53(1), 1-9
        
        ### 2. **Meningkatkan Transplant Success**
        
        **Aplikasi:**
        ```
        SEEDLING TRANSPLANT:
        1. Rendam akar di ABA 10-50 μM (30 menit)
        2. Atau spray ABA 1 hari sebelum transplant
        3. Transplant
        
        HASIL:
        - Transplant shock ↓
        - Survival rate +20-40%
        - Recovery lebih cepat
        
        Mekanisme:
        - ABA → Stomata menutup
        - Transpirasi ↓ saat akar belum optimal
        - Survival lebih tinggi
        ```
        
        ### 3. **Perpanjang Storage Life**
        
        **Aplikasi:**
        ```
        BUAH & SAYURAN:
        1. Spray ABA 100-500 ppm sebelum panen
        2. Atau celup setelah panen
        
        HASIL:
        - Dormansi meningkat
        - Pematangan tertunda
        - Shelf-life +20-30%
        - Senescence tertunda
        ```
        
        ### 4. **Seed Storage**
        
        **Aplikasi:**
        ```
        BENIH:
        1. Spray ABA 50-100 ppm sebelum panen
        2. Keringkan
        3. Simpan
        
        HASIL:
        - Dormansi terjaga
        - Viabilitas lebih lama
        - Perkecambahan prematur ↓
        ```
        
        ### 5. **Salinity Tolerance**
        
        **Aplikasi:**
        ```
        TANAMAN DI TANAH SALIN:
        1. Seed priming dengan ABA 1-10 μM
        2. Atau foliar spray ABA 10-50 μM
        
        HASIL:
        - Osmotic adjustment
        - Ion homeostasis
        - Toleransi salinitas +30-50%
        ```
        
        **Referensi:**
        - Zhu, J. K. (2002). Annual Review of Plant Biology, 53, 247-273
        
        ---
        
        ## 🌿 SUMBER ABA ALAMI
        
        ### **1. Ekstrak Daun Tua/Stress**
        
        **Prinsip:**
        - Daun tua/stress → ABA tinggi
        - Ekstrak → Aplikasi ke tanaman lain
        
        **Cara:**
        ```
        1. Kumpulkan daun tua/menguning (ABA tinggi)
        2. Blender dengan air (1:2)
        3. Saring
        4. Aplikasikan (spray/siram)
        
        Efektivitas: 30-50% vs ABA sintetik
        ```
        
        ### **2. Stress-Induced ABA**
        
        **Cara:**
        ```
        1. Stress tanaman donor (kekeringan ringan 2-3 hari)
        2. ABA meningkat di daun
        3. Panen daun
        4. Ekstrak
        5. Aplikasi ke tanaman target
        ```
        
        ### **3. Produk Komersial**
        
        **ABA Sintetik:**
        - S-ABA (Active form)
        - ProTone (ABA untuk anggur)
        
        **Harga:**
        - Mahal (Rp 500K-2juta/100g)
        - Tapi sangat potent (μM level)
        
        ---
        
        ## ⚠️ PERINGATAN
        
        ### 1. **Dosis Berlebihan:**
        ```
        Gejala:
        - Pertumbuhan terhambat parah
        - Daun kecil, klorosis
        - Yield menurun
        
        Solusi:
        - Gunakan dosis rendah (μM level)
        - Aplikasi targeted (saat perlu)
        - Jangan aplikasi rutin
        ```
        
        ### 2. **Timing:**
        ```
        BENAR:
        - Sebelum stress (priming)
        - Saat stress ringan (protective)
        - Sebelum transplant
        
        SALAH:
        - Saat pertumbuhan aktif (inhibisi)
        - Terlalu sering (growth retardation)
        ```
        
        ### 3. **Interaksi:**
        ```
        ANTAGONIS:
        - ABA vs GA (berlawanan!)
        - ABA vs Sitokinin
        
        JANGAN KOMBINASI:
        - ABA + GA (cancel out)
        - Gunakan terpisah sesuai tujuan
        ```
        
        ---
        
        ## 💡 TIPS PRAKTIS
        
        **1. Untuk Drought Tolerance:**
        - Seed priming (1-10 μM, 24 jam)
        - Atau foliar spray sebelum kekeringan
        - Efektif untuk tanaman annual
        
        **2. Untuk Transplant:**
        - Root dip atau foliar spray 1 hari sebelum
        - Konsentrasi rendah (10-50 μM)
        - Kombinasi dengan good watering practice
        
        **3. Untuk Storage:**
        - Aplikasi sebelum panen
        - Konsentrasi tinggi (100-500 ppm)
        - Combine dengan suhu rendah
        
        **4. Ekonomis:**
        - ABA mahal → Gunakan hanya saat perlu
        - Seed priming paling cost-effective
        - Atau gunakan ekstrak alami (daun stress)
        
        **5. Research:**
        - ABA masih area penelitian aktif
        - Banyak aplikasi potensial (climate change)
        - Stay updated dengan literatur terbaru
        
        ---
        
        ## 📚 REFERENSI ILMIAH
        
        1. **Finkelstein, R. (2013).** Abscisic acid synthesis and response. The Arabidopsis Book, 11, e0166.
        
        2. **Cutler, S. R., et al. (2010).** Abscisic acid: emergence of a core signaling network. Annual Review of Plant Biology, 61, 651-679.
        
        3. **Schroeder, J. I., et al. (2001).** Guard cell signal transduction. Annual Review of Plant Physiology and Plant Molecular Biology, 52, 627-658.
        
        4. **Zhu, J. K. (2002).** Salt and drought stress signal transduction in plants. Annual Review of Plant Biology, 53, 247-273.
        
        5. **Travaglia, C., et al. (2007).** Exogenous ABA increases yield in field-grown wheat with moderate water restriction. Journal of Plant Growth Regulation, 53(1), 1-9.
        
        """)
    
    # Natural Sources
    with subtab_natural:
        st.subheader("🍇 Sumber Hormon Alami")
        
        st.markdown("""
        ### Mengapa Gunakan Sumber Alami?
        
        **Keuntungan:**
        - ✅ **Lebih murah** (bisa buat sendiri)
        - ✅ **Organik** (ramah lingkungan)
        - ✅ **Aman** (tidak toksik)
        - ✅ **Multi-hormon** (kombinasi alami)
        - ✅ **Mudah didapat** (bahan lokal)
        
        **Kekurangan:**
        - ⚠️ Konsentrasi tidak presisi
        - ⚠️ Variasi antar batch
        - ⚠️ Shelf-life pendek
        
        ---
        
        ## 🍇 1. ANGGUR HIJAU (Green Grapes)
        
        ### **Kandungan Hormon:**
        - **GA3 (Gibberellic Acid):** 50-200 ppm
        - **GA7:** 20-80 ppm
        - **Auksin (IAA):** 10-30 ppm
        - **Sitokinin:** 5-15 ppm
        
        ### **Waktu Panen Optimal:**
        - **2-4 minggu setelah fruit set**
        - Buah masih hijau, keras
        - Ukuran kecil (diameter 5-10 mm)
        
        ### **RESEP LENGKAP:**
        
        #### **A. Ekstrak Cair (Liquid Extract)**
        
        ```
        BAHAN:
        - 1 kg anggur hijau muda
        - 2 liter air bersih
        - 1 sendok makan gula (optional, sebagai spreader)
        
        ALAT:
        - Blender
        - Kain saring/saringan halus
        - Botol spray
        
        CARA MEMBUAT:
        1. Cuci bersih anggur (buang kotoran, pestisida)
        2. Potong-potong kecil (termasuk biji)
        3. Blender dengan 1 liter air (5-10 menit)
        4. Diamkan 30 menit (ekstraksi)
        5. Saring dengan kain halus (peras)
        6. Tambahkan air hingga 2 liter
        7. Tambahkan gula, aduk rata
        8. Siap digunakan!
        
        KONSENTRASI:
        - Undiluted (100%): ~100-150 ppm GA equivalent
        - Diluted 1:1: ~50-75 ppm
        - Diluted 1:2: ~30-50 ppm
        
        APLIKASI:
        - Semprot pagi/sore
        - Basahi seluruh tanaman
        - Ulangi 7-10 hari
        
        PENYIMPANAN:
        - Kulkas: 3-5 hari
        - Freezer: 1-2 bulan
        ```
        
        #### **B. Powder (Bubuk Kering)**
        
        ```
        CARA MEMBUAT:
        1. Blender anggur hijau (tanpa air)
        2. Sebar tipis di nampan
        3. Keringkan di oven 50-60°C (12-24 jam)
           Atau jemur di bawah sinar matahari (2-3 hari)
        4. Blender kering jadi powder
        5. Simpan di wadah kedap udara
        
        CARA PAKAI:
        - 10-20 gram powder per liter air
        - Rendam 2-4 jam, aduk sesekali
        - Saring, siap semprot
        
        PENYIMPANAN:
        - Tempat gelap, kering
        - Tahan 6-12 bulan
        ```
        
        ### **Target Tanaman:**
        - ✅ Anggur (pembesaran buah)
        - ✅ Tomat (fruit set, pembesaran)
        - ✅ Cabai (fruit set)
        - ✅ Strawberry (pembungaan)
        - ✅ Lettuce (perkecambahan)
        
        ---
        
        ## 🌱 2. KECAMBAH (SPROUTS)
        
        ### **Kandungan Hormon:**
        - **Giberelin (GA):** 100-300 ppm (TINGGI!)
        - **Auksin (IAA):** 20-50 ppm
        - **Sitokinin:** 10-30 ppm
        
        ### **Jenis Kecambah Terbaik:**
        1. **Kacang Hijau** (Mung Bean) - GA tertinggi
        2. **Kedelai** (Soybean) - Balanced hormones
        3. **Alfalfa** - Sitokinin tinggi
        
        ### **RESEP:**
        
        ```
        BAHAN:
        - 500 gram kacang hijau/kedelai
        - 2 liter air
        
        CARA MEMBUAT:
        1. Rendam kacang 8-12 jam
        2. Tiriskan, letakkan di wadah gelap
        3. Siram 2-3x sehari (jaga lembab)
        4. Kecambahkan 3-5 hari (panjang 3-5 cm)
        5. Blender kecambah + 1 liter air
        6. Saring, tambahkan air hingga 2 liter
        7. Siap pakai!
        
        KONSENTRASI:
        - Undiluted: ~150-250 ppm GA
        - Diluted 1:1: ~75-125 ppm
        
        APLIKASI:
        - Breaking dormancy biji
        - Pemanjangan batang
        - Perkecambahan seragam
        
        PENYIMPANAN:
        - Kulkas: 2-3 hari
        - Buat fresh lebih baik
        ```
        
        ---
        
        ## 🥥 3. AIR KELAPA (COCONUT WATER)
        
        ### **Kandungan Hormon:**
        - **Sitokinin (Zeatin):** 10-50 ppm (TINGGI!)
        - **Auksin (IAA):** 5-15 ppm
        - **Giberelin:** 2-10 ppm
        - Plus: Gula, mineral, vitamin
        
        ### **Waktu Panen Optimal:**
        - Kelapa muda (6-8 bulan)
        - Air masih manis, jernih
        
        ### **RESEP:**
        
        ```
        CARA PAKAI LANGSUNG:
        - Air kelapa murni (100%)
        - Atau encerkan 1:1 dengan air
        - Semprot atau siram
        
        APLIKASI:
        1. Kultur Jaringan:
           - 10-20% air kelapa dalam media
           - Stimulasi pembelahan sel
        
        2. Rooting:
           - Rendam stek di air kelapa (24 jam)
           - Atau semprot setelah tanam
        
        3. Foliar Spray:
           - Encerkan 1:2 (1 air kelapa : 2 air)
           - Semprot daun 7-10 hari sekali
        
        TARGET:
        - Kultur jaringan (sitokinin tinggi)
        - Stek (rooting + anti-senescence)
        - Tanaman hias (kesegaran daun)
        ```
        
        ---
        
        ## 🌿 4. EKSTRAK BAWANG (ONION EXTRACT)
        
        ### **Kandungan:**
        - **Auksin:** Tinggi
        - **Antibakteri:** Allicin
        - **Stimulan akar**
        
        ### **RESEP:**
        
        ```
        BAHAN:
        - 3-5 siung bawang merah/putih
        - 1 liter air
        
        CARA:
        1. Kupas dan potong halus bawang
        2. Rendam di air (24 jam)
        3. Saring
        4. Siap pakai
        
        APLIKASI:
        - Rooting hormone alami
        - Rendam stek 2-4 jam
        - Atau siram setelah tanam
        
        EFEKTIVITAS:
        - 60-70% vs rooting hormone sintetik
        - Plus efek antibakteri
        ```
        
        ---
        
        ## 🍌 5. KULIT PISANG (BANANA PEEL)
        
        ### **Kandungan:**
        - **Sitokinin:** Sedang
        - **Auksin:** Rendah
        - **Kalium:** TINGGI (K)
        - **Fosfor:** Sedang (P)
        
        ### **RESEP:**
        
        ```
        A. EKSTRAK CAIR:
        1. Potong kulit pisang 5-10 buah
        2. Rendam di 2 liter air (3-5 hari)
        3. Saring
        4. Encerkan 1:5 dengan air
        5. Siram tanaman
        
        B. KOMPOS:
        1. Potong kecil-kecil
        2. Tanam di sekitar tanaman
        3. Dekomposisi → Release nutrisi
        
        MANFAAT:
        - Nutrisi K tinggi (pembungaan, buah)
        - Hormon sitokinin (anti-aging)
        ```
        
        ---
        
        ## 🌊 6. RUMPUT LAUT (SEAWEED)
        
        ### **Kandungan:**
        - **Sitokinin:** Tinggi
        - **Auksin:** Sedang
        - **Giberelin:** Rendah
        - **Betaine:** Growth stimulant
        - **Mineral:** Lengkap
        
        ### **PRODUK KOMERSIAL:**
        - Maxicrop
        - Seasol
        - Kelpak
        
        ### **DIY EXTRACT:**
        
        ```
        BAHAN:
        - 1 kg rumput laut segar (atau 200g kering)
        - 5 liter air
        
        CARA:
        1. Cuci bersih rumput laut
        2. Potong kecil-kecil
        3. Rendam di air (2-3 minggu)
        4. Aduk setiap 2-3 hari
        5. Saring
        6. Encerkan 1:10 untuk aplikasi
        
        APLIKASI:
        - Foliar spray: 1:20
        - Soil drench: 1:10
        - Frekuensi: 2-4 minggu sekali
        ```
        
        ---
        
        ## 📊 PERBANDINGAN EFEKTIVITAS
        
        | Sumber | GA | Auksin | Sitokinin | Biaya | Efektivitas |
        |--------|----|----|-----------|-------|-------------|
        | **Anggur Hijau** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ | Rendah | 70-80% |
        | **Kecambah** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | Sangat Rendah | 60-70% |
        | **Air Kelapa** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐⭐ | Rendah | 50-60% |
        | **Bawang** | ⭐ | ⭐⭐⭐⭐ | ⭐ | Sangat Rendah | 60-70% |
        | **Pisang** | ⭐ | ⭐ | ⭐⭐⭐ | Sangat Rendah | 40-50% |
        | **Rumput Laut** | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ | Sedang | 60-70% |
        | **Sintetik** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | Tinggi | 100% |
        
        ---
        
        ## 💡 TIPS KOMBINASI
        
        ### **Formula 1: Rooting Super (Perakaran)**
        ```
        - 50% Air kelapa
        - 30% Ekstrak bawang
        - 20% Air
        
        Rendam stek 4-6 jam → Tanam
        Efektivitas: 80-90%
        ```
        
        ### **Formula 2: Growth Booster (Pertumbuhan)**
        ```
        - 40% Ekstrak kecambah (GA tinggi)
        - 30% Air kelapa (Sitokinin)
        - 30% Air
        
        Semprot 7-10 hari sekali
        Hasil: Pertumbuhan 30-50% lebih cepat
        ```
        
        ### **Formula 3: Fruit Set (Pembentukan Buah)**
        ```
        - 60% Ekstrak anggur hijau (GA)
        - 20% Air kelapa (Sitokinin)
        - 20% Air
        
        Semprot saat bunga mekar
        Hasil: Fruit set naik 40-60%
        ```
        
        ---
        
        ## ⚠️ PERINGATAN & TIPS
        
        **1. Hygiene:**
        - Cuci bersih semua bahan
        - Gunakan air bersih
        - Sterilkan alat (jika untuk kultur jaringan)
        
        **2. Penyimpanan:**
        - Ekstrak cair: Kulkas (3-5 hari)
        - Powder: Tempat gelap, kering (6-12 bulan)
        - Buat fresh lebih baik!
        
        **3. Aplikasi:**
        - Pagi/sore (suhu sejuk)
        - Jangan saat hujan
        - Basahi seluruh tanaman
        
        **4. Dosis:**
        - Mulai rendah (encerkan lebih banyak)
        - Naikkan bertahap
        - Monitor respons tanaman
        
        **5. Konsistensi:**
        - Aplikasi teratur (7-14 hari)
        - Catat hasil
        - Adjust formula sesuai kebutuhan
        
        ---
        
        ## 🎯 KESIMPULAN
        
        **Hormon alami adalah alternatif:**
        - ✅ **Ekonomis** (hemat 70-90% biaya)
        - ✅ **Organik** (ramah lingkungan)
        - ✅ **Efektif** (60-80% vs sintetik)
        - ✅ **Mudah** (bahan lokal, cara simple)
        
        **Terbaik untuk:**
        - Petani organik
        - Skala kecil-menengah
        - Budget terbatas
        - Eksperimen/trial
        
        **Gunakan sintetik jika:**
        - Butuh presisi tinggi
        - Skala komersial besar
        - Hasil harus konsisten
        - Budget memadai
        
        **ATAU KOMBINASI KEDUANYA!** 🌟
        
        """)

# ===== TAB 2: PERTUMBUHAN & PERKEMBANGAN =====
with tab_growth:
    st.header("📈 Pertumbuhan & Perkembangan Tanaman")
    
    st.markdown("""
    ### Perbedaan Pertumbuhan vs Perkembangan
    
    **PERTUMBUHAN (Growth):**
    - Peningkatan **ukuran** dan **massa** yang **irreversible**
    - Dapat diukur (tinggi, berat, volume)
    - Hasil dari pembelahan dan pemanjangan sel
    
    **PERKEMBANGAN (Development):**
    - Perubahan **bentuk** dan **fungsi** sepanjang siklus hidup
    - Diferensiasi sel → jaringan → organ
    - Termasuk: Perkecambahan, pembungaan, pematangan buah
    
    **Referensi:**
    - Taiz, L., & Zeiger, E. (2010). Plant Physiology, 5th Edition
    
    ---
    
    ## 🌱 FASE PERTUMBUHAN TANAMAN
    
    ### **1. Fase Perkecambahan (Germination)**
    
    **Tahapan:**
    ```
    Biji kering → Imbibisi air → Aktivasi enzim
    → Mobilisasi cadangan makanan → Pertumbuhan embrio
    → Munculnya radikula (akar) → Munculnya plumula (tunas)
    ```
    
    **Faktor yang Mempengaruhi:**
    - **Air:** Imbibisi (penyerapan air)
    - **Oksigen:** Respirasi aerobik
    - **Suhu:** Optimal 20-30°C (tergantung spesies)
    - **Cahaya:** Beberapa biji memerlukan cahaya (lettuce)
    
    **Hormon Terlibat:**
    - **Giberelin ↑** → Aktivasi α-amylase → Hidrolisis pati
    - **ABA ↓** → Pelepasan dormansi
    
    **Aplikasi Praktis:**
    ```
    Mempercepat Perkecambahan:
    1. Rendam biji di air 12-24 jam (imbibisi)
    2. Atau rendam di GA3 100-200 ppm (breaking dormancy)
    3. Suhu optimal 25-30°C
    4. Kelembaban tinggi (90-95%)
    
    Hasil: Perkecambahan lebih cepat 2-3 hari
    ```
    
    ---
    
    ### **2. Fase Vegetatif (Vegetative Growth)**
    
    **Karakteristik:**
    - Pertumbuhan **daun, batang, dan akar**
    - Fotosintesis aktif
    - Akumulasi biomassa
    - Belum ada organ reproduktif
    
    **Sub-fase:**
    
    **A. Seedling Stage (Bibit):**
    - 2-4 minggu setelah perkecambahan
    - Daun sejati pertama muncul
    - Sistem akar berkembang
    
    **B. Rapid Vegetative Growth:**
    - Pertumbuhan cepat daun dan batang
    - Fotosintesis maksimal
    - Akumulasi nutrisi
    
    **Hormon Dominan:**
    - **Auksin** → Pemanjangan sel, dominansi apikal
    - **Giberelin** → Pemanjangan batang
    - **Sitokinin** → Pembelahan sel, tunas lateral
    
    **Manajemen:**
    ```
    Untuk Pertumbuhan Vegetatif Optimal:
    - Nitrogen tinggi (N > P, K)
    - Cahaya cukup (6-8 jam/hari minimum)
    - Air teratur
    - Suhu 20-30°C
    - Topping (jika ingin lebat/bushy)
    ```
    
    ---
    
    ### **3. Fase Reproduktif (Reproductive Growth)**
    
    **Transisi Vegetatif → Reproduktif:**
    
    **Faktor Pemicu:**
    - **Photoperiod** (panjang hari)
      - Short-day plants: Bunga saat hari pendek (< 12 jam)
      - Long-day plants: Bunga saat hari panjang (> 12 jam)
      - Day-neutral: Tidak terpengaruh photoperiod
    
    - **Vernalisasi** (cold treatment)
      - Beberapa tanaman perlu paparan dingin (0-10°C)
      - Contoh: Wheat, cabbage
    
    - **Umur tanaman** (maturity)
    - **Stress** (kekeringan ringan dapat memicu pembungaan)
    
    **Tahapan Reproduktif:**
    
    **A. Inisiasi Bunga (Flower Initiation):**
    ```
    Meristem vegetatif → Meristem reproduktif
    → Pembentukan primordial bunga
    ```
    
    **B. Pembungaan (Flowering):**
    - Bunga mekar
    - Penyerbukan (pollination)
    - Fertilisasi
    
    **C. Pembentukan Buah & Biji:**
    - Ovary berkembang → Buah
    - Ovule berkembang → Biji
    - Akumulasi cadangan makanan
    
    **Hormon Terlibat:**
    - **Giberelin** → Induksi pembungaan (substitute vernalisasi/photoperiod)
    - **Florigen** → "Flowering hormone" (signal dari daun)
    - **Auksin + GA** → Fruit set & development
    - **Etilen** → Pematangan buah
    
    **Aplikasi Praktis:**
    ```
    Induksi Pembungaan:
    1. Manipulasi photoperiod (lampu/shading)
    2. Aplikasi GA3 10-50 ppm (substitute cold/long-day)
    3. Stress ringan (kurangi air sedikit)
    4. Nutrisi: Tinggi P & K, rendah N
    
    Hasil: Pembungaan lebih cepat 1-2 minggu
    ```
    
    ---
    
    ### **4. Fase Pematangan (Maturation)**
    
    **Buah Klimakterik:**
    ```
    Mature green → Breaker → Turning → Pink → Red ripe
    
    Proses:
    - Etilen ↑↑ (autocatalytic)
    - Respirasi ↑ (climacteric rise)
    - Pelunakan (pectinase)
    - Manis (amylase → gula)
    - Warna (chlorophyll ↓, carotenoid ↑)
    ```
    
    **Biji:**
    ```
    Akumulasi cadangan makanan:
    - Pati (cereals)
    - Protein (legumes)
    - Lipid (oilseeds)
    
    Desiccation (pengeringan):
    - Kadar air ↓ (10-15%)
    - ABA ↑ (dormansi)
    - Metabolisme ↓
    ```
    
    ---
    
    ### **5. Fase Senescence (Penuaan)**
    
    **Karakteristik:**
    - Degradasi klorofil (daun menguning)
    - Degradasi protein
    - Mobilisasi nutrisi ke organ penyimpanan
    - Akhirnya kematian
    
    **Hormon:**
    - **Etilen ↑** → Mempercepat senescence
    - **ABA ↑** → Stress-induced senescence
    - **Sitokinin ↓** → Hilangnya anti-aging effect
    
    **Jenis Senescence:**
    
    **1. Whole Plant Senescence:**
    - Annual plants setelah reproduksi
    - Monocarpic plants (sekali berbuah, mati)
    
    **2. Organ Senescence:**
    - Daun tua gugur (normal)
    - Bunga layu setelah fertilisasi
    
    **Aplikasi:**
    ```
    Menunda Senescence:
    - Aplikasi sitokinin (BAP 10-50 ppm)
    - Hindari stress (air, nutrisi cukup)
    - Suhu optimal
    
    Mempercepat Senescence (jika perlu):
    - Ethephon 500-1000 ppm (defoliation)
    - Stress kekeringan
    ```
    
    ---
    
    ## 📊 POLA PERTUMBUHAN
    
    ### **Kurva Pertumbuhan Sigmoid:**
    
    ```
    Tinggi/Berat
        ↑
        |     ┌─────────  Fase Stasioner
        |    ╱
        |   ╱   Fase Eksponensial
        |  ╱
        | ╱  Fase Lag
        |╱
        └──────────────────→ Waktu
    ```
    
    **Fase Lag:**
    - Pertumbuhan lambat
    - Adaptasi, pembentukan sistem akar
    
    **Fase Eksponensial:**
    - Pertumbuhan cepat
    - Fotosintesis maksimal
    - Pembelahan sel aktif
    
    **Fase Stasioner:**
    - Pertumbuhan melambat
    - Mencapai ukuran maksimal
    - Mulai reproduksi
    
    ---
    
    ## 🌡️ FAKTOR LINGKUNGAN
    
    ### **1. Cahaya**
    
    **Intensitas:**
    - Low light: Etiolasi (batang panjang, lemah, pucat)
    - Optimal: Pertumbuhan normal
    - High light: Tanaman pendek, kokoh, hijau tua
    
    **Photoperiod:**
    - Mengatur pembungaan
    - Mengatur dormansi
    
    **Kualitas (Spektrum):**
    - Red light (660 nm): Pemanjangan batang
    - Blue light (450 nm): Pembukaan stomata, phototropism
    - Far-red (730 nm): Shade avoidance
    
    ---
    
    ### **2. Suhu**
    
    **Cardinal Temperatures:**
    - **Minimum:** Di bawah ini, pertumbuhan berhenti
    - **Optimum:** Pertumbuhan maksimal
    - **Maximum:** Di atas ini, kerusakan/kematian
    
    **Contoh (Tomat):**
    - Minimum: 10°C
    - Optimum: 20-30°C
    - Maximum: 35°C
    
    **Efek Suhu:**
    - **Rendah:** Pertumbuhan lambat, dormansi
    - **Optimal:** Pertumbuhan normal
    - **Tinggi:** Stress, respirasi ↑, fotosintesis ↓
    
    ---
    
    ### **3. Air**
    
    **Fungsi:**
    - Turgor (tegangan sel)
    - Transport nutrisi
    - Fotosintesis (substrat)
    - Pendinginan (transpirasi)
    
    **Defisit Air:**
    - Wilting (layu)
    - Stomata menutup
    - Pertumbuhan terhambat
    - ABA ↑
    
    ---
    
    ### **4. Nutrisi**
    
    **Makronutrien:**
    - **N:** Pertumbuhan vegetatif, klorofil
    - **P:** Energi (ATP), akar, bunga
    - **K:** Osmoregulasi, enzim, kualitas buah
    
    **Mikronutrien:**
    - Fe, Mn, Zn, Cu, B, Mo, Cl
    
    **Defisiensi:**
    - Pertumbuhan terhambat
    - Gejala spesifik (klorosis, nekrosis)
    
    ---
    
    ## 💡 APLIKASI PRAKTIS
    
    **1. Manipulasi Pertumbuhan Vegetatif:**
    ```
    Untuk Tanaman Lebih Tinggi:
    - GA3 50-100 ppm
    - Nitrogen tinggi
    - Cahaya cukup tapi tidak berlebihan
    
    Untuk Tanaman Lebih Pendek/Kokoh:
    - Retardant (Paclobutrazol, CCC)
    - Cahaya tinggi
    - Nitrogen sedang
    ```
    
    **2. Induksi Pembungaan:**
    ```
    - Manipulasi photoperiod
    - GA3 10-50 ppm (substitute vernalisasi)
    - Stress ringan
    - Nutrisi P & K tinggi
    ```
    
    **3. Sinkronisasi Panen:**
    ```
    - Tanam serentak
    - Kondisi seragam
    - Aplikasi hormon serentak
    - Panen seragam → Efisien
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Taiz, L., & Zeiger, E. (2010).** Plant Physiology, 5th Edition. Sinauer Associates.
    
    2. **Salisbury, F. B., & Ross, C. W. (1992).** Plant Physiology, 4th Edition. Wadsworth Publishing.
    
    3. **Hopkins, W. G., & Hüner, N. P. A. (2008).** Introduction to Plant Physiology, 4th Edition. Wiley.
    
    """)

# ===== TAB 3: FOTOSINTESIS & RESPIRASI =====
with tab_photosynthesis:
    st.header("☀️ Fotosintesis & Respirasi")
    
    st.markdown("""
    ### Hubungan Fotosintesis & Respirasi
    
    **FOTOSINTESIS:**
    ```
    6 CO₂ + 6 H₂O + Cahaya → C₆H₁₂O₆ + 6 O₂
    (Karbon dioksida + Air + Energi cahaya → Glukosa + Oksigen)
    ```
    
    **RESPIRASI:**
    ```
    C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + ATP
    (Glukosa + Oksigen → Karbon dioksida + Air + Energi)
    ```
    
    **Hubungan:** Proses **berlawanan** tapi **saling melengkapi**!
    
    ---
    
    ## 🌿 FOTOSINTESIS
    
    ### **Lokasi:** Kloroplas (daun)
    
    **Struktur Kloroplas:**
    - **Thylakoid:** Membran tempat reaksi terang
    - **Stroma:** Cairan tempat reaksi gelap (Calvin cycle)
    - **Grana:** Tumpukan thylakoid
    
    ---
    
    ### **TAHAP 1: REAKSI TERANG (Light Reactions)**
    
    **Lokasi:** Thylakoid membrane
    
    **Proses:**
    ```
    Cahaya → Fotosistem II → Fotolisis air
    → O₂ + H⁺ + elektron
    → Fotosistem I → NADPH
    → ATP synthase → ATP
    
    Hasil:
    - ATP (energi)
    - NADPH (reducing power)
    - O₂ (byproduct)
    ```
    
    **Fotosistem:**
    - **PS II:** Absorb 680 nm (P680)
    - **PS I:** Absorb 700 nm (P700)
    
    **Fotolisis Air:**
    ```
    2 H₂O → 4 H⁺ + 4 e⁻ + O₂
    (Sumber elektron untuk PS II)
    ```
    
    ---
    
    ### **TAHAP 2: REAKSI GELAP (Calvin Cycle)**
    
    **Lokasi:** Stroma
    
    **Tidak perlu cahaya** (tapi perlu ATP & NADPH dari reaksi terang)
    
    **Tahapan:**
    
    **1. Fiksasi Karbon:**
    ```
    CO₂ + RuBP (5C) → 2 x 3-PGA (3C)
    Enzim: RuBisCO (Ribulose-1,5-bisphosphate carboxylase/oxygenase)
    ```
    
    **2. Reduksi:**
    ```
    3-PGA + ATP + NADPH → G3P (Glyceraldehyde-3-phosphate)
    ```
    
    **3. Regenerasi RuBP:**
    ```
    G3P → RuBP (menggunakan ATP)
    Cycle continues...
    ```
    
    **Hasil Bersih:**
    ```
    3 CO₂ + 9 ATP + 6 NADPH → 1 G3P (3C)
    → 2 G3P → 1 Glukosa (6C)
    ```
    
    ---
    
    ### **JALUR FOTOSINTESIS ALTERNATIF**
    
    ### **1. C3 Plants (Mayoritas tanaman)**
    
    **Karakteristik:**
    - Produk pertama: 3-PGA (3 karbon)
    - Fiksasi CO₂ hanya di mesophyll
    - Enzim: RuBisCO
    
    **Contoh:** Padi, gandum, kedelai, tomat
    
    **Kelemahan:**
    - **Photorespiration** (RuBisCO bind O₂ instead of CO₂)
    - Efisiensi rendah saat panas & kering
    
    ---
    
    ### **2. C4 Plants (Adaptasi iklim panas)**
    
    **Karakteristik:**
    - Produk pertama: Oxaloacetate (4 karbon)
    - Fiksasi CO₂ di mesophyll → Transport ke bundle sheath
    - Enzim: PEP carboxylase (tidak bind O₂!)
    
    **Anatomi Khusus:** Kranz anatomy
    
    **Proses:**
    ```
    Mesophyll:
    CO₂ + PEP → Oxaloacetate (4C) → Malate (4C)
    
    Bundle Sheath:
    Malate → CO₂ (concentrated!) + Pyruvate
    → Calvin cycle (RuBisCO dengan CO₂ tinggi)
    ```
    
    **Keuntungan:**
    - **Tidak ada photorespiration**
    - Efisien di suhu tinggi (30-40°C)
    - Efisien penggunaan air (WUE tinggi)
    
    **Contoh:** Jagung, tebu, sorghum, rumput
    
    **Referensi:**
    - Hatch, M. D. (1987). Biochemistry of Plants, 10, 207-281
    
    ---
    
    ### **3. CAM Plants (Adaptasi kekeringan)**
    
    **CAM = Crassulacean Acid Metabolism**
    
    **Karakteristik:**
    - **Temporal separation** (waktu berbeda)
    - Stomata buka **MALAM** (CO₂ uptake)
    - Stomata tutup **SIANG** (conserve water)
    
    **Proses:**
    ```
    MALAM:
    Stomata buka → CO₂ masuk
    → PEP carboxylase → Malate (stored in vacuole)
    
    SIANG:
    Stomata tutup (conserve water)
    → Malate release CO₂
    → Calvin cycle (RuBisCO)
    ```
    
    **Keuntungan:**
    - **Extreme water efficiency**
    - Survive di gurun/kering
    
    **Kelemahan:**
    - Pertumbuhan lambat
    
    **Contoh:** Kaktus, lidah buaya, nanas, agave
    
    **Referensi:**
    - Winter, K., & Smith, J. A. C. (1996). Ecological Studies, 114
    
    ---
    
    ### **PERBANDINGAN C3, C4, CAM:**
    
    | Karakteristik | C3 | C4 | CAM |
    |---------------|----|----|-----|
    | **Produk 1st** | 3-PGA (3C) | Oxaloacetate (4C) | Malate (4C) |
    | **Enzim** | RuBisCO | PEP carboxylase + RuBisCO | PEP carboxylase + RuBisCO |
    | **Photorespiration** | Ya (tinggi) | Tidak | Tidak |
    | **Suhu Optimal** | 15-25°C | 30-40°C | 35-55°C |
    | **Water Use Efficiency** | Rendah | Sedang | Sangat Tinggi |
    | **Growth Rate** | Sedang | Tinggi | Rendah |
    | **Contoh** | Padi, gandum | Jagung, tebu | Kaktus, nanas |
    
    ---
    
    ## 🫁 RESPIRASI
    
    ### **Fungsi:** Menghasilkan **ATP** (energi) dari glukosa
    
    **Lokasi:** Mitokondria (sebagian besar)
    
    ---
    
    ### **TAHAP RESPIRASI:**
    
    ### **1. Glikolisis**
    
    **Lokasi:** Sitoplasma
    
    **Proses:**
    ```
    Glukosa (6C) → 2 Pyruvate (3C)
    
    Hasil:
    - 2 ATP (net)
    - 2 NADH
    ```
    
    **Tidak perlu O₂** (anaerobic)
    
    ---
    
    ### **2. Siklus Krebs (Citric Acid Cycle)**
    
    **Lokasi:** Mitokondria matrix
    
    **Proses:**
    ```
    Pyruvate → Acetyl-CoA (2C)
    → Masuk siklus Krebs
    → CO₂ + NADH + FADH₂ + ATP
    ```
    
    **Hasil (per glukosa):**
    - 2 ATP
    - 6 NADH
    - 2 FADH₂
    - 4 CO₂
    
    ---
    
    ### **3. Rantai Transport Elektron (ETC)**
    
    **Lokasi:** Inner mitochondrial membrane
    
    **Proses:**
    ```
    NADH & FADH₂ → Donate elektron
    → Electron transport chain
    → Proton gradient (H⁺)
    → ATP synthase → ATP
    → O₂ (final electron acceptor) → H₂O
    ```
    
    **Hasil:**
    - ~28-32 ATP (dari NADH & FADH₂)
    
    **Total ATP per Glukosa: ~30-32 ATP**
    
    ---
    
    ### **RESPIRASI ANAEROB (Fermentasi)**
    
    **Saat O₂ terbatas** (akar tergenang, biji berkecambah)
    
    **Jenis:**
    
    **1. Fermentasi Alkohol:**
    ```
    Pyruvate → Ethanol + CO₂
    (Ragi, akar tergenang)
    
    Hasil: 2 ATP only (dari glikolisis)
    ```
    
    **2. Fermentasi Asam Laktat:**
    ```
    Pyruvate → Lactate
    (Otot saat exercise intense)
    
    Hasil: 2 ATP only
    ```
    
    **Efisiensi:** Sangat rendah (2 ATP vs 30-32 ATP aerobic)
    
    ---
    
    ## ⚖️ RESPIRASI vs FOTOSINTESIS
    
    ### **Balance Harian:**
    
    **SIANG (Cahaya):**
    ```
    Fotosintesis > Respirasi
    → Net CO₂ uptake
    → Net O₂ release
    → Akumulasi biomassa
    ```
    
    **MALAM (Gelap):**
    ```
    Fotosintesis = 0
    Respirasi continues
    → Net CO₂ release
    → Net O₂ uptake
    → Konsumsi cadangan makanan
    ```
    
    **Net Productivity:**
    ```
    Gross Photosynthesis - Total Respiration = Net Productivity
    
    Untuk pertumbuhan, harus POSITIF!
    ```
    
    ---
    
    ## 💡 APLIKASI PRAKTIS
    
    ### **1. Optimasi Fotosintesis:**
    
    ```
    Faktor yang Bisa Dikontrol:
    
    A. Cahaya:
       - Intensitas: 400-800 μmol/m²/s (optimal untuk kebanyakan tanaman)
       - Durasi: 12-16 jam/hari
       - LED grow lights (red + blue spectrum)
    
    B. CO₂:
       - Ambient: 400 ppm
       - Enrichment: 800-1200 ppm (greenhouse)
       - Hasil: Fotosintesis +30-50%
    
    C. Suhu:
       - C3 plants: 20-25°C
       - C4 plants: 30-35°C
       - Avoid > 35°C (enzyme denaturation)
    
    D. Air & Nutrisi:
       - Cukup tapi tidak berlebihan
       - N untuk klorofil
       - Mg untuk klorofil (pusat molekul)
    ```
    
    ---
    
    ### **2. Mengurangi Respirasi (Postharvest):**
    
    ```
    Tujuan: Perpanjang shelf-life
    
    Metode:
    A. Suhu Rendah:
       - 0-5°C (sayuran)
       - Respirasi ↓ 50-70%
    
    B. Atmosfer Terkontrol:
       - O₂ ↓ (3-5%)
       - CO₂ ↑ (5-10%)
       - Respirasi ↓
    
    C. Coating:
       - Wax coating
       - Edible films
       - Reduce O₂ diffusion
    
    Hasil: Shelf-life +2-4x
    ```
    
    ---
    
    ### **3. Greenhouse Management:**
    
    ```
    Optimasi Fotosintesis:
    
    Pagi (6-9 AM):
    - Buka ventilasi (CO₂ fresh)
    - Cahaya mulai masuk
    
    Siang (9 AM - 3 PM):
    - CO₂ enrichment (800-1200 ppm)
    - Suhu kontrol (< 30°C)
    - Shading jika terlalu panas
    
    Sore (3-6 PM):
    - Kurangi CO₂ enrichment
    - Ventilasi
    
    Malam:
    - Tutup (conserve heat)
    - Respirasi only (konsumsi O₂)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Taiz, L., & Zeiger, E. (2010).** Plant Physiology, 5th Edition. Chapter 8 (Photosynthesis) & Chapter 11 (Respiration).
    
    2. **Hatch, M. D. (1987).** C4 photosynthesis: a unique blend of modified biochemistry, anatomy and ultrastructure. Biochemistry of Plants, 10, 207-281.
    
    3. **Winter, K., & Smith, J. A. C. (1996).** Crassulacean Acid Metabolism. Ecological Studies, 114.
    
    4. **Nobel, P. S. (2009).** Physicochemical and Environmental Plant Physiology, 4th Edition.
    
    """)

# ===== TAB 4: STRESS & ADAPTASI =====
with tab_stress:
    st.header("⚠️ Stress & Adaptasi Tanaman")
    
    st.markdown("""
    ### Apa itu Stress pada Tanaman?
    
    **STRESS:** Kondisi lingkungan yang **tidak optimal** yang menyebabkan **penurunan pertumbuhan, produktivitas, atau survival**.
    
    **Jenis Stress:**
    1. **Abiotik:** Faktor non-biologis (kekeringan, salinitas, suhu ekstrem)
    2. **Biotik:** Faktor biologis (hama, penyakit, kompetisi)
    
    ---
    
    ## 💧 STRESS KEKERINGAN (Drought Stress)
    
    ### **Penyebab:**
    - Kurang air di tanah
    - Evapotranspirasi tinggi
    - Sistem akar tidak efisien
    
    ### **Efek pada Tanaman:**
    
    **1. Efek Langsung:**
    ```
    Kurang air → Turgor ↓
    → Wilting (layu)
    → Stomata menutup
    → Fotosintesis ↓
    → Pertumbuhan terhambat
    ```
    
    **2. Efek Fisiologis:**
    - **ABA ↑** (signal dari akar ke daun)
    - **Stomata closure** (conserve water)
    - **Osmotic adjustment** (akumulasi solutes)
    - **Protein stress** (LEA proteins, HSPs)
    
    **3. Efek Jangka Panjang:**
    - Daun mengecil
    - Akar lebih dalam
    - Senescence prematur
    - Yield ↓
    
    ---
    
    ### **MEKANISME TOLERANSI KEKERINGAN:**
    
    **1. Drought Avoidance (Menghindari):**
    ```
    Strategi:
    - Akar dalam (akses air lebih dalam)
    - Stomata menutup cepat (conserve water)
    - Daun menggulung (reduce surface area)
    - Wax layer tebal (reduce evaporation)
    
    Contoh: Kaktus, agave
    ```
    
    **2. Drought Tolerance (Bertahan):**
    ```
    Strategi:
    - Osmotic adjustment (proline, betaine)
    - Antioxidants (SOD, CAT, APX)
    - LEA proteins (protect cellular structures)
    - Maintain turgor at low water potential
    
    Contoh: Sorghum, millet
    ```
    
    **Referensi:**
    - Zhu, J. K. (2002). Annual Review of Plant Biology, 53, 247-273
    
    ---
    
    ### **APLIKASI PRAKTIS:**
    
    ```
    Meningkatkan Drought Tolerance:
    
    1. SEED PRIMING:
       - Rendam benih di ABA 1-10 μM (24 jam)
       - Atau PEG (Polyethylene Glycol) 10-20%
       - Hasil: Toleransi +30-50%
    
    2. FOLIAR APPLICATION:
       - ABA 10-50 μM (1-2 hari sebelum stress)
       - Proline 10-50 mM
       - Glycine betaine 50-100 mM
    
    3. CULTURAL PRACTICES:
       - Mulching (reduce evaporation)
       - Drip irrigation (efficient)
       - Drought-tolerant varieties
    
    4. TIMING:
       - Irrigate saat critical stages (flowering, fruit set)
       - Deficit irrigation (controlled stress)
    ```
    
    ---
    
    ## 🧂 STRESS SALINITAS (Salinity Stress)
    
    ### **Penyebab:**
    - Tanah salin (NaCl tinggi)
    - Irigasi dengan air salin
    - Intrusi air laut
    
    ### **Efek pada Tanaman:**
    
    **1. Osmotic Stress:**
    ```
    Salt ↑ di tanah → Water potential ↓
    → Tanaman sulit absorb air
    → "Physiological drought"
    ```
    
    **2. Ion Toxicity:**
    ```
    Na⁺ & Cl⁻ excessive → Toxic
    → Mengganggu enzim
    → Kompetisi dengan K⁺, Ca²⁺
    → Nutrient imbalance
    ```
    
    **3. Oxidative Stress:**
    ```
    Salt stress → ROS (Reactive Oxygen Species) ↑
    → Lipid peroxidation
    → Protein damage
    → DNA damage
    ```
    
    ---
    
    ### **MEKANISME TOLERANSI SALINITAS:**
    
    **1. Ion Exclusion:**
    ```
    - Mencegah Na⁺ masuk ke akar
    - Selektif uptake K⁺ over Na⁺
    - Maintain high K⁺/Na⁺ ratio
    ```
    
    **2. Ion Compartmentalization:**
    ```
    - Sequester Na⁺ di vacuole
    - Keep cytoplasm Na⁺ low
    - Enzim: NHX (Na⁺/H⁺ antiporter)
    ```
    
    **3. Osmotic Adjustment:**
    ```
    - Akumulasi compatible solutes:
      - Proline
      - Glycine betaine
      - Sugars (sucrose, trehalose)
    - Maintain turgor
    ```
    
    **4. Antioxidant Defense:**
    ```
    - Enzim: SOD, CAT, APX, GPX
    - Non-enzymatic: Ascorbate, glutathione
    - Scavenge ROS
    ```
    
    **Referensi:**
    - Munns, R., & Tester, M. (2008). Annual Review of Plant Biology, 59, 651-681
    
    ---
    
    ### **APLIKASI PRAKTIS:**
    
    ```
    Meningkatkan Salt Tolerance:
    
    1. SEED PRIMING:
       - NaCl priming (50-100 mM, 24 jam)
       - Hardening effect
    
    2. FOLIAR APPLICATION:
       - Glycine betaine 50-100 mM
       - Proline 10-50 mM
       - Calcium (Ca²⁺) 10-20 mM
    
    3. SOIL MANAGEMENT:
       - Leaching (flush salt)
       - Gypsum application (Ca²⁺ replace Na⁺)
       - Organic matter (improve structure)
    
    4. VARIETAL SELECTION:
       - Salt-tolerant varieties
       - Halophytes (extreme tolerance)
    ```
    
    ---
    
    ## 🌡️ STRESS SUHU (Temperature Stress)
    
    ### **A. HEAT STRESS (Panas)**
    
    **Efek:**
    ```
    Suhu > 35°C:
    - Protein denaturation
    - Membrane fluidity ↑
    - Photosynthesis ↓ (RuBisCO inactivation)
    - Respiration ↑
    - Pollen sterility
    ```
    
    **Mekanisme Toleransi:**
    ```
    1. Heat Shock Proteins (HSPs):
       - Chaperones (protect proteins)
       - Refold denatured proteins
    
    2. Membrane Adjustment:
       - Increase saturated fatty acids
       - Maintain membrane integrity
    
    3. Antioxidants:
       - Scavenge ROS
    ```
    
    **Aplikasi:**
    ```
    - Shading (reduce temperature)
    - Evaporative cooling (misting)
    - Heat-tolerant varieties
    - Foliar spray: Salicylic acid, proline
    ```
    
    ---
    
    ### **B. COLD STRESS (Dingin)**
    
    **Efek:**
    ```
    Suhu < 10°C (chilling):
    - Membrane rigidity
    - Enzyme activity ↓
    - Photosynthesis ↓
    
    Suhu < 0°C (freezing):
    - Ice crystal formation
    - Cell rupture
    - Death
    ```
    
    **Mekanisme Toleransi:**
    ```
    1. Cold Acclimation:
       - Gradual exposure to cold
       - Induce cold-responsive genes
    
    2. Membrane Adjustment:
       - Increase unsaturated fatty acids
       - Maintain fluidity
    
    3. Cryoprotectants:
       - Sugars (sucrose, raffinose)
       - Proline
       - Antifreeze proteins (AFPs)
    
    4. Supercooling:
       - Prevent ice nucleation
       - Water stays liquid below 0°C
    ```
    
    **Aplikasi:**
    ```
    - Cold-hardy varieties
    - Frost protection (covers, heaters)
    - Hardening (gradual cold exposure)
    - Avoid fertilization before winter
    ```
    
    ---
    
    ## ☀️ STRESS CAHAYA
    
    ### **A. LOW LIGHT (Shade)**
    
    **Efek:**
    ```
    - Etiolation (batang panjang, lemah)
    - Daun tipis, pucat
    - Fotosintesis ↓
    - Yield ↓
    ```
    
    **Adaptasi:**
    ```
    - Klorofil ↑ (capture more light)
    - Daun lebih lebar
    - Shade tolerance (understory plants)
    ```
    
    ---
    
    ### **B. HIGH LIGHT (Photoinhibition)**
    
    **Efek:**
    ```
    Light > photosynthetic capacity:
    - Photosystem damage (especially PS II)
    - ROS production
    - Photooxidation
    ```
    
    **Mekanisme Proteksi:**
    ```
    1. Non-Photochemical Quenching (NPQ):
       - Dissipate excess energy as heat
       - Xanthophyll cycle
    
    2. Photorespiration:
       - Alternative electron sink
       - Protect from photoinhibition
    
    3. Antioxidants:
       - Scavenge ROS
    ```
    
    ---
    
    ## 🔬 STRESS OKSIDATIF (Oxidative Stress)
    
    **Penyebab:** Semua stress → ROS ↑
    
    **ROS (Reactive Oxygen Species):**
    - Superoxide (O₂⁻)
    - Hydrogen peroxide (H₂O₂)
    - Hydroxyl radical (•OH)
    
    **Damage:**
    - Lipid peroxidation (membrane damage)
    - Protein oxidation
    - DNA damage
    
    **Antioxidant Defense:**
    
    **Enzymatic:**
    ```
    - SOD (Superoxide Dismutase): O₂⁻ → H₂O₂
    - CAT (Catalase): H₂O₂ → H₂O + O₂
    - APX (Ascorbate Peroxidase): H₂O₂ → H₂O
    - GPX (Glutathione Peroxidase)
    ```
    
    **Non-Enzymatic:**
    ```
    - Ascorbate (Vitamin C)
    - Glutathione
    - Tocopherol (Vitamin E)
    - Carotenoids
    - Flavonoids
    ```
    
    **Referensi:**
    - Mittler, R. (2002). Trends in Plant Science, 7(9), 405-410
    
    ---
    
    ## 💡 APLIKASI PRAKTIS TERPADU
    
    ### **Strategi Multi-Stress Tolerance:**
    
    ```
    1. VARIETAL SELECTION:
       - Pilih varietas toleran multi-stress
       - Local varieties often more adapted
    
    2. SEED PRIMING:
       - ABA (drought + salt tolerance)
       - PEG (drought tolerance)
       - NaCl (salt tolerance)
    
    3. FOLIAR APPLICATION:
       - Proline (multi-stress)
       - Glycine betaine (salt + drought)
       - Salicylic acid (heat + disease)
       - Antioxidants (oxidative stress)
    
    4. CULTURAL PRACTICES:
       - Mulching (temperature + moisture)
       - Proper irrigation (avoid stress)
       - Balanced nutrition (resilience)
       - Crop rotation (soil health)
    
    5. TIMING:
       - Avoid stress during critical stages
       - Flowering & fruit set most sensitive
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Zhu, J. K. (2002).** Salt and drought stress signal transduction in plants. Annual Review of Plant Biology, 53, 247-273.
    
    2. **Munns, R., & Tester, M. (2008).** Mechanisms of salinity tolerance. Annual Review of Plant Biology, 59, 651-681.
    
    3. **Mittler, R. (2002).** Oxidative stress, antioxidants and stress tolerance. Trends in Plant Science, 7(9), 405-410.
    
    4. **Hasanuzzaman, M., et al. (2013).** Physiological, biochemical, and molecular mechanisms of heat stress tolerance in plants. International Journal of Molecular Sciences, 14(5), 9643-9684.
    
    """)

# ===== TAB 5: APLIKASI PRAKTIS =====
with tab_practice:
    st.header("🛠️ Aplikasi Praktis Fisiologi Tumbuhan")
    
    st.markdown("""
    ### Integrasi Pengetahuan Fisiologi untuk Optimasi Produksi
    
    ---
    
    ## 🌾 KASUS 1: OPTIMASI PRODUKSI TOMAT
    
    ### **Fase 1: Perkecambahan & Seedling (0-4 minggu)**
    
    **Tujuan:** Perkecambahan cepat & seragam, seedling kuat
    
    **Aplikasi:**
    ```
    SEED TREATMENT:
    - Rendam biji di GA3 100 ppm (24 jam) → Breaking dormancy
    - Atau priming dengan PEG 10% (24 jam) → Stress tolerance
    
    KONDISI:
    - Suhu: 25-28°C (optimal germination)
    - Kelembaban: 90-95%
    - Cahaya: Tidak perlu sampai muncul kotiledon
    
    HASIL:
    - Perkecambahan 85-95% dalam 5-7 hari
    - Seedling seragam
    ```
    
    ---
    
    ### **Fase 2: Vegetatif (4-8 minggu)**
    
    **Tujuan:** Pertumbuhan vegetatif kuat, sistem akar baik
    
    **Aplikasi:**
    ```
    NUTRISI:
    - N tinggi (NPK 20-10-10)
    - Aplikasi setiap 7-10 hari
    
    HORMON (Optional):
    - Air kelapa 10% (sitokinin) → Anti-senescence
    - Atau seaweed extract 1:20 → Multi-hormone
    
    KONDISI:
    - Cahaya: 12-14 jam/hari, 400-600 μmol/m²/s
    - Suhu: 22-28°C (siang), 18-22°C (malam)
    - Air: Teratur, jangan sampai wilting
    
    HASIL:
    - Tanaman kokoh, daun hijau tua
    - Akar kuat
    ```
    
    ---
    
    ### **Fase 3: Pembungaan & Fruit Set (8-10 minggu)**
    
    **Tujuan:** Pembungaan seragam, fruit set tinggi
    
    **Aplikasi:**
    ```
    NUTRISI:
    - Switch ke NPK 10-20-20 (P & K tinggi)
    
    HORMON:
    - NAA 10-20 ppm atau GA3 10 ppm saat bunga mekar
    - Atau ekstrak anggur hijau (encerkan 1:1)
    - Semprot bunga setiap 3-5 hari
    
    KONDISI:
    - Suhu: 20-25°C (optimal pollination)
    - Hindari > 30°C (pollen sterility)
    - Kelembaban: 60-70% (optimal pollination)
    
    HASIL:
    - Fruit set 80-90%
    - Buah seragam
    ```
    
    ---
    
    ### **Fase 4: Pembesaran Buah (10-14 minggu)**
    
    **Tujuan:** Buah besar, kualitas baik
    
    **Aplikasi:**
    ```
    NUTRISI:
    - NPK 15-15-30 (K tinggi untuk kualitas)
    - Ca untuk mencegah blossom end rot
    
    HORMON (Optional):
    - GA3 + Sitokinin (5-10 ppm each) → Pembesaran
    - Aplikasi 1-2x saat buah kecil
    
    AIR:
    - Teratur, consistent (avoid cracking)
    - Deficit irrigation ringan → Meningkatkan gula
    
    HASIL:
    - Buah besar (150-200g)
    - Kualitas baik (Brix 4-6%)
    ```
    
    ---
    
    ### **Fase 5: Pematangan & Panen (14-16 minggu)**
    
    **Tujuan:** Pematangan seragam, kualitas optimal
    
    **Aplikasi:**
    ```
    PEMATANGAN:
    - Panen saat breaker stage (mulai berubah warna)
    - Atau mature green (untuk transport jauh)
    
    RIPENING (Post-harvest):
    - Ethylene 100 ppm, 20°C, 90% RH (24-48 jam)
    - Atau simpan dengan apel/pisang matang
    
    STORAGE:
    - 1-MCP treatment (delay ripening)
    - Suhu 12-15°C (avoid chilling injury)
    - Shelf-life: 7-14 hari
    
    HASIL:
    - Pematangan seragam
    - Kualitas konsisten
    - Shelf-life optimal
    ```
    
    ---
    
    ## 🌾 KASUS 2: MANAJEMEN STRESS KEKERINGAN PADA PADI
    
    ### **Situasi:** Musim kemarau, air terbatas
    
    **Strategi:**
    
    ```
    1. SEED PRIMING (Sebelum tanam):
       - Rendam benih di ABA 5 μM (24 jam)
       - Atau PEG 15% (24 jam)
       - Keringkan, tanam
       
       Hasil: Drought tolerance +30-40%
    
    2. VARIETAL SELECTION:
       - Pilih varietas drought-tolerant
       - Contoh: IR64, Situ Bagendit
    
    3. CULTURAL PRACTICES:
       - System of Rice Intensification (SRI)
       - Alternate Wetting & Drying (AWD)
       - Mulching (reduce evaporation)
    
    4. CRITICAL STAGE PROTECTION:
       - Pastikan air cukup saat:
         * Tillering (anakan)
         * Panicle initiation (inisiasi malai)
         * Flowering (pembungaan)
       - Deficit irrigation di fase lain (acceptable)
    
    5. FOLIAR APPLICATION (saat stress):
       - ABA 10-50 μM → Stomata closure
       - Proline 20 mM → Osmotic adjustment
       - Aplikasi pagi hari
    
    HASIL:
    - Water use efficiency +40-60%
    - Yield reduction minimal (< 15%)
    - Survival rate tinggi
    ```
    
    ---
    
    ## 🍇 KASUS 3: PEMBESARAN BUAH ANGGUR SEEDLESS
    
    ### **Tujuan:** Buah besar, nilai jual tinggi
    
    **Protokol Lengkap:**
    
    ```
    TAHAP 1: SAAT BUNGA MEKAR (Bloom)
    
    Aplikasi:
    - GA3 20-30 ppm (komersial)
    - Atau ekstrak anggur hijau 100% (DIY)
    - Semprot seluruh tandan
    
    Tujuan:
    - Fruit set tanpa biji (parthenocarpy)
    - Pemanjangan tandan
    
    ────────────────────────────────────
    
    TAHAP 2: SAAT BUAH KECIL (Berry Set, 7-10 hari setelah bloom)
    
    Aplikasi:
    - GA3 50-100 ppm
    - Atau ekstrak anggur hijau 100%
    - Celup tandan (lebih efektif dari spray)
    
    Tujuan:
    - Pembesaran buah (cell division & elongation)
    
    ────────────────────────────────────
    
    TAHAP 3: 2 MINGGU SETELAH TAHAP 2 (Optional)
    
    Aplikasi:
    - GA3 50 ppm
    - Atau ekstrak anggur hijau (encerkan 1:1)
    
    Tujuan:
    - Pembesaran lanjutan
    
    ────────────────────────────────────
    
    NUTRISI PENDUKUNG:
    - NPK 15-15-30 (K tinggi)
    - Ca & Mg (kualitas buah)
    - Boron (fruit set)
    
    HASIL:
    - Buah 2-3x lebih besar
    - Tandan lebih panjang
    - Nilai jual +200-300%!
    
    ROI:
    - Biaya GA3: Rp 50K-100K/pohon
    - Atau DIY (anggur hijau): Rp 10K-20K/pohon
    - Peningkatan nilai: Rp 500K-1juta/pohon
    - ROI: 500-2000%! 🚀
    ```
    
    ---
    
    ## 🥬 KASUS 4: PERPANJANG KESEGARAN SAYURAN DAUN
    
    ### **Tujuan:** Shelf-life lebih lama, nilai jual lebih tinggi
    
    **Protokol:**
    
    ```
    PRE-HARVEST (1-2 hari sebelum panen):
    
    Aplikasi:
    - Sitokinin (BAP) 10-30 ppm
    - Atau air kelapa (encerkan 1:1 dengan air)
    - Semprot pagi hari
    
    Tujuan:
    - Anti-senescence
    - Maintain klorofil
    
    ────────────────────────────────────
    
    HARVEST:
    - Panen pagi hari (suhu rendah, turgor tinggi)
    - Hindari kerusakan mekanis
    
    ────────────────────────────────────
    
    POST-HARVEST:
    
    1. COOLING:
       - Hydrocooling atau air cooling
       - Turunkan suhu ke 5-10°C (cepat!)
    
    2. DIP TREATMENT (Optional):
       - Celup di air kelapa 10% (30 detik)
       - Atau sitokinin 20 ppm
    
    3. PACKAGING:
       - Perforated plastic (breathable)
       - Atau modified atmosphere (MA)
    
    4. STORAGE:
       - Suhu: 5-10°C
       - Humidity: 90-95%
       - Avoid ethylene exposure (pisahkan dari buah)
    
    HASIL:
    - Shelf-life: 3-5 hari → 7-14 hari
    - Daun tetap hijau, segar
    - Nilai jual lebih tinggi
    - Waste reduction 50-70%
    ```
    
    ---
    
    ## 🌱 KASUS 5: KULTUR JARINGAN (Tissue Culture)
    
    ### **Tujuan:** Perbanyakan tanaman cepat & seragam
    
    **Protokol Umum:**
    
    ```
    TAHAP 1: INISIASI (Initiation)
    
    Media:
    - MS basal medium
    - Auksin (NAA): 0.5-1 mg/L
    - Sitokinin (BAP): 1-2 mg/L
    - Ratio: Auksin < Sitokinin → Tunas
    
    Hasil: Kalus + tunas adventif
    
    ────────────────────────────────────
    
    TAHAP 2: MULTIPLIKASI (Multiplication)
    
    Media:
    - MS medium
    - Sitokinin (BAP): 2-5 mg/L (tinggi!)
    - Auksin (NAA): 0.1-0.5 mg/L (rendah)
    
    Subculture: Setiap 3-4 minggu
    
    Hasil: Banyak tunas (multiplikasi 5-10x per cycle)
    
    ────────────────────────────────────
    
    TAHAP 3: ROOTING (Perakaran)
    
    Media:
    - MS medium (1/2 strength)
    - Auksin (IBA): 1-3 mg/L (tinggi!)
    - Sitokinin: 0 (tidak ada)
    - Ratio: Auksin > Sitokinin → Akar
    
    Hasil: Plantlet dengan akar kuat
    
    ────────────────────────────────────
    
    TAHAP 4: AKLIMATISASI (Acclimatization)
    
    Prosedur:
    1. Transfer plantlet ke pot kecil
    2. Media: Cocopeat + perlite (1:1)
    3. Humidity tinggi (90-95%) → Gradual turun
    4. Cahaya rendah → Gradual naik
    5. Suhu: 25-28°C
    
    Durasi: 2-4 minggu
    
    Survival rate: 80-95%
    
    ────────────────────────────────────
    
    TIPS SUKSES:
    - Sterilitas total (avoid contamination)
    - Kontrol hormon ratio (kunci organogenesis)
    - Subculture teratur (maintain vigor)
    - Aklimatisasi gradual (reduce shock)
    ```
    
    ---
    
    ## 💡 TIPS UMUM APLIKASI HORMON
    
    ### **DO's:**
    
    ```
    ✅ Mulai dengan dosis rendah, naikkan bertahap
    ✅ Aplikasi pagi/sore (suhu sejuk)
    ✅ Gunakan spreader/sticker (improve absorption)
    ✅ Konsisten (interval teratur)
    ✅ Monitor respons tanaman
    ✅ Catat hasil (dokumentasi)
    ✅ Kombinasi hormon (synergistic effect)
    ✅ Adjust berdasarkan kondisi
    ```
    
    ### **DON'Ts:**
    
    ```
    ❌ Dosis berlebihan (toxic!)
    ❌ Aplikasi saat panas (degradasi cepat)
    ❌ Aplikasi saat hujan (tercuci)
    ❌ Mix hormon antagonis (GA + ABA)
    ❌ Aplikasi terlalu sering (waste, stress)
    ❌ Ignore plant response (adjust!)
    ❌ Gunakan hormon expired
    ❌ Aplikasi tanpa tujuan jelas
    ```
    
    ---
    
    ## 📊 MONITORING & EVALUASI
    
    ### **Parameter yang Diukur:**
    
    ```
    PERTUMBUHAN:
    - Tinggi tanaman (cm)
    - Jumlah daun
    - Diameter batang (mm)
    - Berat segar & kering (g)
    
    REPRODUKSI:
    - Jumlah bunga
    - Fruit set (%)
    - Ukuran buah (diameter, berat)
    - Yield (kg/tanaman atau kg/ha)
    
    KUALITAS:
    - Warna (colorimeter)
    - Kekerasan (penetrometer)
    - Gula (refractometer, °Brix)
    - Kesegaran (visual)
    
    EKONOMI:
    - Biaya input (Rp)
    - Nilai output (Rp)
    - ROI (%)
    - Break-even point
    ```
    
    ---
    
    ## 🎯 KESIMPULAN
    
    **Fisiologi tumbuhan adalah FONDASI untuk:**
    
    1. ✅ **Optimasi produksi** (yield maksimal)
    2. ✅ **Efisiensi input** (hemat biaya)
    3. ✅ **Kualitas produk** (nilai jual tinggi)
    4. ✅ **Manajemen stress** (resilience)
    5. ✅ **Inovasi** (teknologi baru)
    
    **Dengan memahami fisiologi:**
    - Anda bisa **diagnosa** masalah dengan tepat
    - Anda bisa **intervensi** dengan efektif
    - Anda bisa **optimasi** setiap fase pertumbuhan
    - Anda bisa **inovasi** dengan percaya diri
    
    **KNOWLEDGE IS POWER!** 💪🌱
    
    ---
    
    ## 📚 REFERENSI LENGKAP
    
    **Textbooks:**
    1. Taiz, L., & Zeiger, E. (2010). Plant Physiology, 5th Edition.
    2. Salisbury, F. B., & Ross, C. W. (1992). Plant Physiology, 4th Edition.
    3. Hopkins, W. G., & Hüner, N. P. A. (2008). Introduction to Plant Physiology, 4th Edition.
    
    **Journals:**
    - Annual Review of Plant Biology
    - Plant Physiology
    - Journal of Experimental Botany
    - Plant, Cell & Environment
    
    **Semua konten di module ini berdasarkan literatur peer-reviewed!** ✅
    
    """)


# ===== TAB 6: ANALISIS BRIX =====
with tab_brix:
    st.header("🍇 Analisis Brix - Indikator Kualitas Tanaman")
    st.info("💡 Brix mengukur kadar gula (Total Soluble Solids) dalam tanaman - indikator penting kualitas, rasa, dan kesehatan tanaman.")
    
    # Sub-tabs for Brix
    brix_teori, brix_ukur, brix_organik, brix_kimia, brix_standar, brix_ai = st.tabs([
        "📚 Teori & Ilmiah",
        "🔬 Cara Pengukuran",
        "🌿 Optimalisasi Organik",
        "⚗️ Optimalisasi Kimia",
        "📊 Standar Komoditas",
        "🤖 AI Brix Predictor"
    ])
    
    # ========== SUB-TAB 1: TEORI & ILMIAH ==========
    with brix_teori:
        st.subheader("📚 Teori & Dasar Ilmiah Brix")
        
        st.markdown("""
        ## 🔬 APA ITU BRIX?
        
        **Brix (°Bx)** adalah skala untuk mengukur **Total Soluble Solids (TSS)** atau padatan terlarut total 
        dalam cairan tanaman, terutama gula (sukrosa, glukosa, fruktosa).
        
        **Definisi:**
        > **1° Brix = 1 gram sukrosa per 100 gram larutan**
        
        **Sejarah:**
        - Dikembangkan oleh **Adolf Ferdinand Wenzeslaus Brix** (1798-1870)
        - Awalnya untuk industri minuman dan gula
        - Sekarang standar industri pertanian untuk kualitas
        
        ---
        
        ## 🔗 HUBUNGAN BRIX DENGAN KUALITAS
        
        ### 1. **Rasa & Sweetness**
        ```
        Brix Tinggi → Gula Tinggi → Rasa Lebih Manis
        ```
        
        ### 2. **Nilai Nutrisi**
        ```
        Brix Tinggi → Mineral & Vitamin Tinggi
        (Korelasi dengan uptake nutrisi yang baik)
        ```
        
        ### 3. **Ketahanan Penyakit**
        ```
        Brix Tinggi → Membrana sel lebih kuat
        → Lebih tahan patogen & serangga
        ```
        
        ### 4. **Shelf Life**
        ```
        Brix Tinggi → Osmotic pressure tinggi
        → Tahan lebih lama (tidak mudah busuk)
        ```
        
        ### 5. **Indikator Kesehatan Tanah**
        ```
        Tanah sehat → Uptake nutrisi optimal
        → Fotosintesis maksimal → Brix tinggi
        ```
        
        ---
        
        ## 📖 TEORI CAREY REAMS
        
        **Dr. Carey Reams** adalah pionir High-Brix Farming:
        
        ### Prinsip Utama:
        1. **"The higher the Brix, the higher the quality"**
        2. **Soil Biology = Key** - Mikoriza & bakteri meningkatkan uptake
        3. **Mineral Balance** - Kelebihan N menurunkan Brix
        4. **Calcium:Phosphorus Ratio** - 7:1 ideal untuk high Brix
        
        ### Reams' Brix Chart:
        | Category | Brix Range | Deskripsi |
        |----------|------------|-----------|
        | **Poor** | <4° | Nutrisi rendah, mudah sakit |
        | **Average** | 4-8° | Standar pasar |
        | **Good** | 8-12° | Premium quality |
        | **Excellent** | 12-18° | Superior, organic grade |
        
        ---
        
        ## 📊 PRINSIP REFRAKTOMETRI
        
        **Cara Kerja Refraktometer:**
        
        ```
        Cahaya → Melewati sampel → PEMBIASAN (refraction)
        → Sudut pembiasan ∝ konsentrasi gula
        → Skala Brix
        ```
        
        **Indeks Refraksi (nD):**
        - Air murni: nD = 1.333 (0° Brix)
        - Sukrosa 20%: nD = 1.367 (20° Brix)
        
        ---
        
        ## 📚 REFERENSI ILMIAH
        
        1. **Reams, C. A.** (1976). *Choose Life or Death*. Holistic Agriculture Library.
        2. **Chandler, W.** (2015). *High Brix Growing*. Permaculture Research Institute.
        3. **Brix, A. F. W.** (1870). *Polarimetrische Zuckerbestimmung*. Braunschweig.
        4. **Kays, S. J.** (1991). *Postharvest Physiology of Perishable Plant Products*. Springer.
        
        """)
        
        # Comparison Table
        st.markdown("### 📊 Perbandingan Low vs High Brix")
        
        comparison_data = {
            "Aspek": ["Rasa", "Warna", "Aroma", "Tekstur", "Shelf Life", "Harga Jual", "Serangga", "Penyakit"],
            "Low Brix (<6°)": ["Hambar/Asam", "Pucat", "Lemah", "Lembek", "2-5 hari", "Standar", "Rentan", "Rentan"],
            "High Brix (>12°)": ["Manis, Kompleks", "Cerah, Intense", "Kuat, Aromatik", "Renyah/Padat", "7-14 hari", "Premium 2-3x", "Tahan", "Tahan"]
        }
        st.table(pd.DataFrame(comparison_data))
    
    # ========== SUB-TAB 2: CARA PENGUKURAN ==========
    with brix_ukur:
        st.subheader("🔬 Cara Mengukur Brix")
        
        st.markdown("""
        ## 🔧 JENIS REFRAKTOMETER
        
        ### 1. **Refraktometer Analog (Optik)**
        - Prinsip: Melihat skala melalui eyepiece
        - Harga: Rp 100.000 - 500.000
        - Akurasi: ± 0.2° Brix
        - **Keuntungan:** Murah, portable, tidak perlu baterai
        
        ### 2. **Refraktometer Digital**
        - Prinsip: Sensor optik + display digital
        - Harga: Rp 500.000 - 5.000.000
        - Akurasi: ± 0.1° Brix
        - **Keuntungan:** Lebih akurat, auto-temperature compensation (ATC)
        
        ---
        
        ## 📝 PROSEDUR PENGUKURAN
        
        ### Langkah-langkah:
        
        ```
        1. KALIBRASI
           - Bersihkan prisma dengan air suling
           - Teteskan air suling → Harus 0° Brix
           - Jika tidak, adjust dengan skrup kalibrasi
        
        2. SAMPLING
           - Pilih bagian tanaman yang representatif
           - Buah: Potong, peras/crush
           - Daun: Gunakan garlic press atau blender
           - Hindari kontaminasi
        
        3. PENGUKURAN
           - Teteskan 2-3 tetes sampel ke prisma
           - Tutup daylight plate
           - Arahkan ke cahaya
           - Baca skala pada garis batas terang-gelap
        
        4. PEMBERSIHAN
           - Bersihkan dengan tissue lembab
           - Jangan gores prisma
           - Simpan dalam case
        ```
        
        ---
        
        ## ⏰ WAKTU PENGUKURAN OPTIMAL
        
        | Waktu | Brix | Alasan |
        |-------|------|--------|
        | **Pagi (6-8 AM)** | Terendah | Respirasi malam menghabiskan gula |
        | **Siang (12-2 PM)** | Tinggi | Fotosintesis aktif |
        | **Sore (4-6 PM)** | **Tertinggi** | Akumulasi gula maksimal |
        
        **TIP:** Ukur konsisten di waktu yang sama (idealnya sore hari)
        
        ---
        
        ## ⚠️ FAKTOR YANG MEMPENGARUHI PEMBACAAN
        
        1. **Suhu:** Pembacaan berubah ±0.4° per 10°C
           - Gunakan refraktometer dengan ATC (Auto Temperature Compensation)
        
        2. **Kontaminasi:**
           - Kotoran/tanah → Pembacaan salah
           - Selalu cuci sampel
        
        3. **Bagian Tanaman:**
           - Buah matang > Buah muda
           - Daun muda > Daun tua
           - Batang < Daun < Buah
        
        4. **Waktu Harvest:**
           - Konsisten ukur di waktu sama
        
        """)
    
    # ========== SUB-TAB 3: OPTIMALISASI ORGANIK ==========
    with brix_organik:
        st.subheader("🌿 Optimalisasi Brix - Jalur Organik")
        
        st.markdown("""
        ## 🦠 BIOLOGI TANAH
        
        **Prinsip:** Tanah sehat = Tanaman sehat = High Brix
        
        ### 1. **Mikoriza (Mycorrhizal Fungi)**
        
        ```
        Mikoriza → Memperluas jangkauan akar 10-1000x
        → Uptake P, Zn, Cu meningkat
        → Fotosintesis lebih efisien
        → BRIX NAIK 2-4°
        ```
        
        **Aplikasi:**
        - Dosis: 5-10 gram/tanaman (inokulasi)
        - Waktu: Saat tanam atau transplanting
        - Produk: Glomus spp., Rhizophagus irregularis
        
        ### 2. **Bakteri Pelarut Fosfat**
        
        ```
        Bacillus, Pseudomonas → Melarutkan P terikat
        → P tersedia untuk tanaman
        → Energi (ATP) untuk fotosintesis
        → BRIX NAIK 1-2°
        ```
        
        ### 3. **Rhizobium (untuk Legume)**
        
        ```
        Rhizobium → Fiksasi N2 dari udara
        → N tersedia (tanpa pupuk)
        → Pertumbuhan optimal
        ```
        
        ---
        
        ## 🌱 BAHAN ORGANIK
        
        ### 1. **Kompos Berkualitas Tinggi**
        
        **Kriteria:**
        - C/N Ratio: 15-20 (sudah matang)
        - Warna: Cokelat gelap - hitam
        - Aroma: Tanah segar (tidak busuk)
        
        **Dosis:** 
        - Sayuran: 10-20 ton/ha
        - Buah: 5-10 kg/pohon/tahun
        
        ### 2. **Humic & Fulvic Acid**
        
        ```
        Humic Acid → Meningkatkan CEC tanah
        → Nutrisi tersedia lebih lama
        → Uptake lebih efisien
        → BRIX NAIK 2-3°
        ```
        
        **Aplikasi:**
        - Kocor: 2-5 ml/L, seminggu sekali
        - Foliar: 1-2 ml/L, seminggu sekali
        
        ### 3. **Biochar**
        
        ```
        Biochar → Habitat mikroba
        → Retensi nutrisi & air
        → Biologi tanah meningkat
        ```
        
        **Dosis:** 1-5 ton/ha (sekali saja)
        
        ---
        
        ## 🧪 FERMENTASI HAYATI
        
        ### 1. **EM4 (Effective Microorganisms)**
        - Dosis: 10-20 ml/L
        - Frekuensi: Seminggu sekali
        
        ### 2. **PGPR (Plant Growth Promoting Rhizobacteria)**
        - Dosis: 5-10 ml/L
        - Waktu: Fase vegetatif
        
        ### 3. **MOL (Mikroorganisme Lokal)**
        - Buat dari buah busuk + gula + air
        - Fermentasi 14-21 hari
        - Aplikasi: 10 ml/L
        
        """)
        
        # Organic Application Calculator
        st.divider()
        st.markdown("### 🧮 Kalkulator Aplikasi Organik")
        
        org_c1, org_c2 = st.columns(2)
        
        with org_c1:
            org_luas = st.number_input("Luas Lahan (m²)", value=1000, step=100, key="org_luas")
            org_type = st.selectbox("Jenis Bahan", ["Kompos", "Humic Acid", "EM4", "Mikoriza"], key="org_type")
        
        with org_c2:
            if org_type == "Kompos":
                dosis = 2  # kg/m²
                st.metric("Dosis Rekomendasi", f"{dosis} kg/m²")
                st.metric("Total Kebutuhan", f"{org_luas * dosis:,.0f} kg")
            elif org_type == "Humic Acid":
                dosis_ml = 3  # ml/L, 1L per m²
                st.metric("Dosis Rekomendasi", f"{dosis_ml} ml/L")
                st.metric("Total Kebutuhan", f"{org_luas * dosis_ml:,.0f} ml")
            elif org_type == "EM4":
                dosis_ml = 15  # ml/L
                st.metric("Dosis Rekomendasi", f"{dosis_ml} ml/L")
                st.metric("Total Kebutuhan", f"{org_luas * dosis_ml:,.0f} ml")
            else:
                dosis_g = 5  # gram per lubang tanam
                populasi = org_luas // 4  # asumsi jarak 2x2m
                st.metric("Dosis Rekomendasi", f"{dosis_g} g/tanaman")
                st.metric("Total Kebutuhan", f"{populasi * dosis_g:,.0f} gram")
    
    # ========== SUB-TAB 4: OPTIMALISASI KIMIA ==========
    with brix_kimia:
        st.subheader("⚗️ Optimalisasi Brix - Jalur Kimia")
        
        st.markdown("""
        ## 🔑 NUTRISI KUNCI UNTUK BRIX
        
        ### 1. **KALIUM (K)** - The Sugar Maker
        
        **Peran:**
        ```
        K → Aktivasi 60+ enzim
        → Termasuk enzim fotosintesis
        → Translokasi gula dari daun ke buah
        → BRIX NAIK 2-5°
        ```
        
        **Gejala Defisiensi:**
        - Tepi daun menguning/coklat (necrosis)
        - Buah kecil, rasa hambar
        - Brix rendah
        
        **Aplikasi:**
        | Sumber | K₂O (%) | Dosis | Waktu |
        |--------|---------|-------|-------|
        | KCl | 60% | 200-400 kg/ha | Tanam |
        | K₂SO₄ | 50% | 200-400 kg/ha | Tanam + Buah |
        | KNO₃ | 44% | Foliar 1-2% | Generatif |
        
        ---
        
        ### 2. **MAGNESIUM (Mg)** - The Chlorophyll Core
        
        **Peran:**
        ```
        Mg → INTI molekul klorofil
        → Fotosintesis efisien
        → Produksi gula maksimal
        → BRIX NAIK 1-2°
        ```
        
        **Gejala Defisiensi:**
        - Interveinal chlorosis (kuning antar tulang daun)
        - Daun tua lebih dulu
        
        **Aplikasi:**
        | Sumber | Mg (%) | Dosis |
        |--------|--------|-------|
        | MgSO₄ (Epsom Salt) | 10% | 50-100 kg/ha |
        | Dolomit | 5-15% | 1-2 ton/ha |
        | Foliar MgSO₄ | - | 1-2% |
        
        ---
        
        ### 3. **BORON (B)** - Sugar Transporter
        
        **Peran:**
        ```
        B → Integritas membran sel
        → Transportasi gula melalui phloem
        → Kekuatan dinding sel
        → BRIX NAIK 1-3°
        ```
        
        **Gejala Defisiensi:**
        - Growing point abnormal (dieback)
        - Buah pecah/retak
        - Fruit set rendah
        
        **Aplikasi:**
        | Sumber | B (%) | Dosis |
        |--------|-------|-------|
        | Borax | 11% | 10-20 kg/ha |
        | Boric Acid | 17% | Foliar 0.1-0.2% |
        | Solubor | 20% | 5-10 kg/ha |
        
        **⚠️ HATI-HATI:** B bersifat toksik di dosis tinggi! Jangan lebih dari 2 kg/ha
        
        ---
        
        ### 4. **SULFUR (S)** - Protein Builder
        
        **Peran:**
        ```
        S → Komponen asam amino esensial
        → Sintesis protein & enzim
        → Aroma & rasa kompleks
        ```
        
        **Aplikasi:**
        | Sumber | S (%) | Dosis |
        |--------|-------|-------|
        | ZA (Ammonium Sulfate) | 24% | 150-200 kg/ha |
        | Elemental S | 90% | 20-50 kg/ha |
        | Gypsum | 18% | 500-1000 kg/ha |
        
        ---
        
        ## ⏰ TIMING PEMUPUKAN
        
        | Fase | Fokus Nutrisi | Tujuan |
        |------|---------------|--------|
        | **Vegetatif** | N, P | Pertumbuhan daun & akar |
        | **Transisi** | K, Mg | Persiapan pembungaan |
        | **Generatif** | K, B | Fruit set & pembesaran |
        | **Pematangan** | K (tinggi), kurangi N | Akumulasi gula, BRIX maksimal |
        
        ### PRINSIP PENTING:
        
        > **KURANGI NITROGEN di fase pematangan!**
        > N tinggi → Pertumbuhan vegetatif terus → Gula untuk daun, bukan buah
        > → BRIX TURUN
        
        """)
        
        # Chemical Fertilizer Calculator
        st.divider()
        st.markdown("### 🧮 Kalkulator Pupuk untuk High Brix")
        
        chem_c1, chem_c2 = st.columns(2)
        
        with chem_c1:
            chem_luas = st.number_input("Luas Lahan (ha)", value=1.0, step=0.1, key="chem_luas")
            current_brix = st.number_input("Brix Saat Ini (°Bx)", value=6.0, step=0.5, key="curr_brix")
            target_brix = st.number_input("Target Brix (°Bx)", value=12.0, step=0.5, key="tgt_brix")
        
        with chem_c2:
            gap = target_brix - current_brix
            st.metric("Gap Brix", f"{gap:.1f}°", "perlu ditingkatkan")
            
            # Recommendations based on gap
            if gap > 0:
                k_need = gap * 50  # rough estimate: 50 kg KCl per 1° Brix
                mg_need = gap * 15
                b_need = gap * 1.5
                
                st.markdown("**Rekomendasi Pemupukan:**")
                st.markdown(f"- **K₂SO₄:** {k_need * chem_luas:.0f} kg ({k_need:.0f} kg/ha)")
                st.markdown(f"- **MgSO₄:** {mg_need * chem_luas:.0f} kg ({mg_need:.0f} kg/ha)")
                st.markdown(f"- **Borax:** {b_need * chem_luas:.1f} kg ({b_need:.1f} kg/ha)")
    
    # ========== SUB-TAB 5: STANDAR KOMODITAS ==========
    with brix_standar:
        st.subheader("📊 Standar Brix per Komoditas")
        
        # Brix Standards Database
        brix_db = {
            "Komoditas": [
                # Buah
                "🍇 Anggur", "🍓 Stroberi", "🍉 Semangka", "🍈 Melon", "🥭 Mangga",
                "🍑 Persik", "🍎 Apel", "🍊 Jeruk", "🍌 Pisang", "🍍 Nanas",
                # Sayuran
                "🍅 Tomat", "🌶️ Cabai", "🥕 Wortel", "🥬 Bayam", "🥗 Selada",
                "🥒 Timun", "🧅 Bawang Merah", "🥔 Kentang", "🌽 Jagung Manis", "🫑 Paprika"
            ],
            "Kategori": [
                "Buah", "Buah", "Buah", "Buah", "Buah",
                "Buah", "Buah", "Buah", "Buah", "Buah",
                "Sayuran", "Sayuran", "Sayuran", "Sayuran", "Sayuran",
                "Sayuran", "Sayuran", "Sayuran", "Sayuran", "Sayuran"
            ],
            "Poor": [12, 6, 8, 10, 10, 8, 8, 8, 16, 12, 4, 4, 4, 4, 2, 4, 6, 4, 10, 4],
            "Average": [16, 10, 10, 12, 12, 10, 10, 10, 18, 14, 6, 6, 8, 6, 4, 5, 8, 6, 14, 6],
            "Good": [20, 14, 12, 14, 14, 13, 12, 12, 20, 16, 8, 8, 12, 8, 6, 7, 10, 8, 18, 8],
            "Excellent": [26, 16, 14, 16, 18, 16, 14, 14, 22, 18, 12, 10, 18, 12, 10, 10, 12, 10, 22, 10]
        }
        
        df_brix = pd.DataFrame(brix_db)
        
        # Filter
        filter_cat = st.radio("Filter Kategori:", ["Semua", "Buah", "Sayuran"], horizontal=True, key="brix_filter")
        
        if filter_cat != "Semua":
            df_display = df_brix[df_brix["Kategori"] == filter_cat]
        else:
            df_display = df_brix
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        st.markdown("""
        ### 📖 Cara Membaca Tabel:
        
        | Kategori | Deskripsi |
        |----------|-----------|
        | **Poor** | Kualitas rendah, rasa hambar, nutrisi minimal |
        | **Average** | Standar pasar konvensional |
        | **Good** | Premium quality, layak organic premium |
        | **Excellent** | Superior, harga jual 2-3x lipat |
        
        ---
        
        ### 🍇 VISUAL BRIX METER
        """)
        
        # Visual Brix Meter
        meter_commodity = st.selectbox("Pilih Komoditas:", df_brix["Komoditas"].tolist(), key="meter_comm")
        meter_value = st.slider("Nilai Brix (°Bx)", 0.0, 30.0, 8.0, 0.5, key="meter_val")
        
        # Get commodity standards
        comm_data = df_brix[df_brix["Komoditas"] == meter_commodity].iloc[0]
        poor = comm_data["Poor"]
        avg = comm_data["Average"]
        good = comm_data["Good"]
        exc = comm_data["Excellent"]
        
        # Determine classification
        if meter_value < poor:
            classification = "🔴 POOR"
            color = "#ef4444"
        elif meter_value < avg:
            classification = "🟡 AVERAGE"
            color = "#f59e0b"
        elif meter_value < good:
            classification = "🟢 GOOD"
            color = "#22c55e"
        else:
            classification = "🌟 EXCELLENT"
            color = "#10b981"
        
        # Display gauge
        fig_brix = go.Figure(go.Indicator(
            mode="gauge+number",
            value=meter_value,
            title={'text': f"Brix {meter_commodity}"},
            gauge={
                'axis': {'range': [0, exc + 5]},
                'bar': {'color': color},
                'steps': [
                    {'range': [0, poor], 'color': "#fee2e2"},
                    {'range': [poor, avg], 'color': "#fef3c7"},
                    {'range': [avg, good], 'color': "#d1fae5"},
                    {'range': [good, exc + 5], 'color': "#a7f3d0"}
                ],
                'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': good}
            }
        ))
        fig_brix.update_layout(height=300)
        st.plotly_chart(fig_brix, use_container_width=True)
        
        st.markdown(f"### Klasifikasi: **{classification}**")
    
    # ========== SUB-TAB 6: AI BRIX PREDICTOR ==========
    with brix_ai:
        st.subheader("🤖 AI Brix Predictor & Optimizer")
        st.success("🧠 Model AI akan memprediksi Brix berdasarkan parameter input dan memberikan rekomendasi optimalisasi.")
        
        st.markdown("### 📝 Input Parameter")
        
        ai_c1, ai_c2, ai_c3 = st.columns(3)
        
        with ai_c1:
            st.markdown("##### 🌱 Tanaman")
            ai_commodity = st.selectbox("Komoditas", 
                ["Tomat", "Stroberi", "Anggur", "Melon", "Cabai", "Wortel", "Bayam", "Selada"],
                key="ai_comm")
            ai_age = st.number_input("Umur Tanaman (hari)", value=60, step=5, key="ai_age")
            ai_stage = st.selectbox("Fase Pertumbuhan", 
                ["Vegetatif Awal", "Vegetatif Akhir", "Generatif (Bunga)", "Pembesaran Buah", "Pematangan"],
                key="ai_stage")
        
        with ai_c2:
            st.markdown("##### 🌍 Tanah & Nutrisi")
            ai_ph = st.slider("pH Tanah", 4.0, 9.0, 6.5, 0.1, key="ai_ph")
            ai_om = st.slider("Bahan Organik (%)", 0.0, 10.0, 2.5, 0.5, key="ai_om")
            ai_k = st.slider("Konsentrasi K (ppm)", 50, 500, 200, 10, key="ai_k")
            ai_mg = st.slider("Konsentrasi Mg (ppm)", 20, 300, 100, 10, key="ai_mg")
        
        with ai_c3:
            st.markdown("##### ☀️ Lingkungan")
            ai_light = st.slider("Intensitas Cahaya (%)", 20, 100, 80, 5, key="ai_light")
            ai_temp = st.slider("Suhu Rata-rata (°C)", 15, 40, 28, 1, key="ai_temp")
            ai_water = st.select_slider("Kondisi Irigasi", 
                options=["Sangat Kering", "Kering", "Optimal", "Basah", "Sangat Basah"],
                value="Optimal", key="ai_water")
            ai_b = st.slider("Konsentrasi B (ppm)", 0.0, 5.0, 1.0, 0.1, key="ai_b")
        
        st.divider()
        
        if st.button("🚀 Prediksi Brix & Generate Rekomendasi", type="primary", key="ai_predict"):
            
            # AI Model (Simulation) - Weighted Factor Model
            # Base Brix by commodity
            base_brix = {
                "Tomat": 6, "Stroberi": 8, "Anggur": 14, "Melon": 10,
                "Cabai": 5, "Wortel": 6, "Bayam": 5, "Selada": 4
            }
            
            # Calculate factors (0-1 scale)
            ph_factor = 1 - abs(ai_ph - 6.5) / 3  # optimal at 6.5
            om_factor = min(ai_om / 5, 1)  # higher is better up to 5%
            k_factor = min(ai_k / 300, 1)  # optimal around 300 ppm
            mg_factor = min(ai_mg / 150, 1)
            b_factor = min(ai_b / 2, 1)  # optimal around 2 ppm
            light_factor = ai_light / 100
            temp_factor = 1 - abs(ai_temp - 25) / 15  # optimal at 25°C
            
            water_map = {"Sangat Kering": 0.4, "Kering": 0.7, "Optimal": 1.0, "Basah": 0.8, "Sangat Basah": 0.5}
            water_factor = water_map.get(ai_water, 1.0)
            
            stage_multiplier = {
                "Vegetatif Awal": 0.6, "Vegetatif Akhir": 0.75, 
                "Generatif (Bunga)": 0.85, "Pembesaran Buah": 0.95, "Pematangan": 1.1
            }
            stage_mult = stage_multiplier.get(ai_stage, 1.0)
            
            # Weighted calculation
            quality_score = (
                k_factor * 0.25 +
                om_factor * 0.20 +
                mg_factor * 0.12 +
                b_factor * 0.10 +
                ph_factor * 0.10 +
                light_factor * 0.10 +
                water_factor * 0.08 +
                temp_factor * 0.05
            )
            
            predicted_brix = base_brix.get(ai_commodity, 6) * quality_score * 1.5 * stage_mult
            predicted_brix = round(predicted_brix, 1)
            
            # Get commodity standards
            comm_standards = df_brix[df_brix["Komoditas"].str.contains(ai_commodity, case=False)]
            if not comm_standards.empty:
                target_brix = comm_standards.iloc[0]["Good"]
            else:
                target_brix = 10
            
            # Classification
            if predicted_brix < target_brix * 0.5:
                classification = "🔴 POOR"
            elif predicted_brix < target_brix * 0.75:
                classification = "🟡 AVERAGE"
            elif predicted_brix < target_brix:
                classification = "🟢 GOOD"
            else:
                classification = "🌟 EXCELLENT"
            
            # Display Results
            st.markdown("---")
            st.markdown("### 📊 Hasil Prediksi AI")
            
            res_c1, res_c2, res_c3 = st.columns(3)
            
            with res_c1:
                st.metric("Prediksi Brix", f"{predicted_brix}°Bx")
            with res_c2:
                st.metric("Klasifikasi", classification)
            with res_c3:
                gap = target_brix - predicted_brix
                st.metric("Gap vs Target", f"{gap:+.1f}°", f"Target: {target_brix}°Bx")
            
            # Optimization Recommendations
            st.markdown("### 🎯 Rekomendasi Optimalisasi AI")
            
            # Identify weak factors
            factors = {
                "Kalium (K)": (k_factor, "Tingkatkan pemupukan K₂SO₄ (200-400 kg/ha) terutama di fase generatif"),
                "Bahan Organik": (om_factor, "Tambahkan kompos 10-20 ton/ha dan humic acid 2ml/L"),
                "Magnesium (Mg)": (mg_factor, "Aplikasi MgSO₄ foliar 1-2% setiap minggu"),
                "Boron (B)": (b_factor, "Semprot Boric acid 0.1-0.2% saat pembungaan"),
                "pH Tanah": (ph_factor, f"Adjust pH ke 6.5 (saat ini {ai_ph})"),
                "Cahaya": (light_factor, "Tingkatkan paparan cahaya (pruning, spacing)"),
                "Irigasi": (water_factor, "Terapkan deficit irrigation di fase pematangan")
            }
            
            # Sort by lowest score
            sorted_factors = sorted(factors.items(), key=lambda x: x[1][0])
            
            st.markdown("**Top 3 Faktor yang Perlu Diperbaiki:**")
            
            for i, (factor_name, (score, recommendation)) in enumerate(sorted_factors[:3], 1):
                score_pct = score * 100
                if score_pct < 50:
                    status = "🔴 Kritis"
                elif score_pct < 75:
                    status = "🟡 Perlu Perhatian"
                else:
                    status = "🟢 Cukup Baik"
                
                with st.expander(f"**{i}. {factor_name}** - Score: {score_pct:.0f}% {status}"):
                    st.markdown(f"**Rekomendasi:** {recommendation}")
                    st.progress(score)
            
            # Expected Improvement
            st.markdown("### 📈 Proyeksi Perbaikan")
            
            potential_improvement = (1 - quality_score) * base_brix.get(ai_commodity, 6) * 0.5
            projected_brix = predicted_brix + potential_improvement
            
            improve_data = pd.DataFrame({
                "Status": ["Saat Ini", "Proyeksi (3 bulan)"],
                "Brix": [predicted_brix, round(projected_brix, 1)]
            })
            
            fig_improve = px.bar(improve_data, x="Status", y="Brix", 
                                title="Proyeksi Peningkatan Brix",
                                text="Brix", color="Status",
                                color_discrete_map={"Saat Ini": "#f59e0b", "Proyeksi (3 bulan)": "#10b981"})
            fig_improve.update_traces(textposition='outside')
            fig_improve.add_hline(y=target_brix, line_dash="dash", line_color="red",
                                 annotation_text=f"Target: {target_brix}°Bx")
            st.plotly_chart(fig_improve, use_container_width=True)
            
            st.success(f"✅ Dengan menerapkan rekomendasi di atas, Brix dapat meningkat dari **{predicted_brix}°Bx** ke **{round(projected_brix, 1)}°Bx** dalam 2-3 bulan!")

