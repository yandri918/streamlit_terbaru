import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Genetika & Pemuliaan Tanaman - AgriSensa",
    page_icon="🧬",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Header
st.title("🧬 Genetika & Pemuliaan Tanaman")
st.markdown("**Prinsip Genetika, Seleksi Varietas, dan Teknologi Pemuliaan Modern**")

# Main tabs
tab_principles, tab_selection, tab_hybrid, tab_biotech, tab_propagation, tab_tools = st.tabs([
    "📚 Prinsip Pemuliaan",
    "🌱 Seleksi Varietas",
    "🌾 Hybrid vs Open-Pollinated",
    "🔬 GMO & Bioteknologi",
    "🌿 Perbanyakan Tanaman",
    "🛠️ Tools & Database"
])

# ===== TAB 1: PRINSIP PEMULIAAN =====
with tab_principles:
    st.header("📚 Prinsip Dasar Pemuliaan Tanaman")
    
    st.markdown("""
    ### Definisi Pemuliaan Tanaman
    
    **Pemuliaan tanaman** adalah **seni dan ilmu** untuk **meningkatkan sifat genetik** tanaman agar lebih **produktif, berkualitas, dan adaptif**.
    
    **Tujuan:**
    - ✅ Meningkatkan hasil (yield)
    - ✅ Meningkatkan kualitas (rasa, nutrisi, penampilan)
    - ✅ Ketahanan terhadap hama & penyakit
    - ✅ Toleransi stress (kekeringan, salinitas, suhu ekstrem)
    - ✅ Adaptasi lingkungan spesifik
    
    **Referensi:**
    - Allard, R. W. (1999). Principles of Plant Breeding, 2nd Edition. John Wiley & Sons.
    
    ---
    
    ## 🧬 DASAR GENETIKA
    
    ### **Hukum Mendel**
    
    **Gregor Mendel (1866)** - Bapak Genetika
    
    **Hukum I: Segregasi (Pemisahan)**
    ```
    Setiap individu memiliki 2 alel untuk setiap sifat
    → Saat pembentukan gamet, alel berpisah
    → Setiap gamet hanya membawa 1 alel
    
    Contoh:
    Tinggi (T) dominan terhadap pendek (t)
    
    P: TT (tinggi) × tt (pendek)
    F1: Tt (semua tinggi - 100%)
    
    F1 × F1: Tt × Tt
    F2: TT : Tt : Tt : tt
        1  :  2 :  2 :  1
        
    Fenotip: 3 tinggi : 1 pendek (ratio 3:1)
    Genotip: 1 TT : 2 Tt : 1 tt (ratio 1:2:1)
    ```
    
    **Hukum II: Asortasi Bebas (Independent Assortment)**
    ```
    Gen-gen yang berbeda diwariskan secara independen
    (jika tidak linked)
    
    Contoh:
    Tinggi (T) vs Pendek (t)
    Bulat (R) vs Keriput (r)
    
    P: TTRR × ttrr
    F1: TtRr (semua tinggi bulat)
    
    F1 × F1: TtRr × TtRr
    F2: 9 tinggi bulat : 3 tinggi keriput : 3 pendek bulat : 1 pendek keriput
        (ratio 9:3:3:1)
    ```
    
    **Referensi:**
    - Mendel, G. (1866). Experiments in Plant Hybridization.
    
    ---
    
    ### **Konsep Genetika Modern**
    
    **1. DNA & Gen:**
    ```
    DNA (Deoxyribonucleic Acid)
    → Double helix (Watson & Crick, 1953)
    → Kode genetik (A, T, G, C)
    
    Gen = Segmen DNA yang mengkode protein/sifat tertentu
    
    Genom = Seluruh DNA dalam satu organisme
    ```
    
    **2. Kromosom:**
    ```
    DNA dikemas dalam kromosom
    
    Manusia: 46 kromosom (23 pasang)
    Padi: 24 kromosom (12 pasang)
    Tomat: 24 kromosom (12 pasang)
    Jagung: 20 kromosom (10 pasang)
    
    Diploid (2n): Sel somatik (2 set kromosom)
    Haploid (n): Gamet (1 set kromosom)
    ```
    
    **3. Alel:**
    ```
    Alel = Bentuk alternatif dari gen yang sama
    
    Contoh:
    Gen untuk warna bunga:
    - Alel R (merah) - dominan
    - Alel r (putih) - resesif
    
    Genotip:
    - RR: Homozigot dominan (merah)
    - Rr: Heterozigot (merah)
    - rr: Homozigot resesif (putih)
    ```
    
    **4. Dominansi:**
    ```
    Dominan penuh:
    - Alel dominan menutupi alel resesif
    - Contoh: Tinggi (T) > pendek (t)
    
    Dominansi tidak penuh (Incomplete):
    - Heterozigot intermediate
    - Contoh: Merah (RR) × Putih (rr) → Pink (Rr)
    
    Kodominansi:
    - Kedua alel terekspresi
    - Contoh: Golongan darah AB
    ```
    
    ---
    
    ## 🌱 VARIASI GENETIK
    
    ### **Sumber Variasi:**
    
    **1. Mutasi:**
    ```
    Perubahan urutan DNA
    
    Jenis:
    - Point mutation (1 nukleotida)
    - Insertion/deletion
    - Chromosomal rearrangement
    
    Penyebab:
    - Spontan (error replikasi)
    - Induksi (radiasi, kimia)
    
    Frekuensi: Rendah (10⁻⁶ - 10⁻⁹ per gen per generasi)
    ```
    
    **2. Rekombinasi:**
    ```
    Pertukaran materi genetik saat meiosis
    
    Crossing over:
    - Kromosom homolog bertukar segmen
    - Menghasilkan kombinasi gen baru
    
    Independent assortment:
    - Kromosom berbeda diwariskan independen
    - 2ⁿ kombinasi gamet (n = jumlah pasangan kromosom)
    ```
    
    **3. Hibridisasi:**
    ```
    Persilangan antar individu berbeda
    
    Intraspecific: Dalam spesies sama
    Interspecific: Antar spesies berbeda
    
    Menghasilkan kombinasi gen baru
    ```
    
    ---
    
    ## 🎯 METODE PEMULIAAN
    
    ### **1. SELEKSI (Selection)**
    
    **Prinsip:**
    ```
    Pilih individu terbaik → Perbanyak
    → Generasi berikutnya lebih baik
    ```
    
    **Jenis Seleksi:**
    
    **A. Seleksi Massa (Mass Selection):**
    ```
    Metode:
    1. Tanam populasi besar
    2. Pilih individu terbaik (visual)
    3. Panen benih dari individu terpilih
    4. Tanam generasi berikutnya
    5. Ulangi
    
    Keuntungan:
    ✅ Mudah
    ✅ Murah
    ✅ Cepat
    
    Kekurangan:
    ❌ Tidak akurat (pengaruh lingkungan)
    ❌ Lambat (progress kecil per generasi)
    
    Cocok untuk: Sifat heritabilitas tinggi (warna, tinggi)
    ```
    
    **B. Seleksi Galur Murni (Pure Line Selection):**
    ```
    Metode:
    1. Pilih individu terbaik
    2. Tanam benih dari SATU individu (progeny row)
    3. Evaluasi progeny (keturunan)
    4. Pilih galur terbaik
    5. Perbanyak
    
    Keuntungan:
    ✅ Lebih akurat (evaluasi progeny)
    ✅ Homozigot (seragam)
    
    Kekurangan:
    ❌ Lebih lama
    ❌ Lebih mahal
    
    Cocok untuk: Tanaman self-pollinated (padi, gandum, kedelai)
    ```
    
    **C. Seleksi Progeny (Progeny Test):**
    ```
    Metode:
    1. Pilih individu
    2. Uji keturunannya (progeny test)
    3. Pilih berdasarkan performa progeny
    
    Keuntungan:
    ✅ Sangat akurat
    ✅ Bisa deteksi gen resesif
    
    Kekurangan:
    ❌ Sangat lama (butuh 1-2 generasi)
    ❌ Mahal
    
    Cocok untuk: Tanaman cross-pollinated, perennial
    ```
    
    ---
    
    ### **2. HIBRIDISASI (Hybridization)**
    
    **Prinsip:**
    ```
    Silangkan 2 tetua berbeda (P1 × P2)
    → Kombinasi gen baru
    → Pilih yang terbaik
    ```
    
    **Tahapan:**
    
    **1. Pemilihan Tetua (Parent Selection):**
    ```
    Kriteria:
    - Komplementer (saling melengkapi)
    - Contoh: P1 (hasil tinggi, rentan penyakit)
              P2 (hasil rendah, tahan penyakit)
    - Target: F1 (hasil tinggi + tahan penyakit)
    ```
    
    **2. Persilangan (Crossing):**
    ```
    Teknik:
    - Emaskulasi (buang benang sari)
    - Isolasi (cegah penyerbukan lain)
    - Polinasi (serbuk sari P2 ke putik P1)
    - Label (catat silangan)
    ```
    
    **3. Evaluasi Generasi:**
    
    **F1 (First Filial):**
    ```
    - Semua heterozigot
    - Seragam
    - Sering menunjukkan heterosis (hybrid vigor)
    ```
    
    **F2 (Second Filial):**
    ```
    - Segregasi (bervariasi)
    - Ratio Mendel (3:1, 9:3:3:1, dll)
    - Pilih individu terbaik
    ```
    
    **F3 - F6:**
    ```
    - Lanjutkan seleksi
    - Inbreeding (self-pollination)
    - Menuju homozigot (seragam)
    ```
    
    **F7+:**
    ```
    - Sudah homozigot (>98%)
    - Uji multilokasi
    - Uji adaptasi
    - Release sebagai varietas baru
    ```
    
    **Waktu:**
    ```
    Total: 8-12 tahun (dari crossing sampai release)
    ```
    
    ---
    
    ### **3. BACKCROSS (Silang Balik)**
    
    **Prinsip:**
    ```
    Transfer 1-2 gen spesifik ke varietas unggul
    Tanpa mengubah sifat lain
    ```
    
    **Metode:**
    ```
    P1 (Recurrent parent): Varietas unggul (tapi rentan penyakit)
    P2 (Donor parent): Varietas biasa (tapi tahan penyakit)
    
    F1 = P1 × P2
    BC1 = F1 × P1 (silang balik ke P1)
    BC2 = BC1 × P1
    BC3 = BC2 × P1
    ...
    BC5-BC6 = Sudah 98-99% seperti P1, tapi dengan gen tahan penyakit
    
    Waktu: 5-7 tahun
    ```
    
    **Keuntungan:**
    ```
    ✅ Pertahankan sifat unggul P1
    ✅ Tambahkan 1-2 sifat baru
    ✅ Lebih cepat dari hibridisasi biasa
    ```
    
    **Cocok untuk:**
    - Transfer resistensi penyakit
    - Transfer toleransi stress
    - Perbaikan sifat spesifik
    
    ---
    
    ### **4. MUTASI (Mutation Breeding)**
    
    **Prinsip:**
    ```
    Induksi mutasi → Variasi baru → Seleksi
    ```
    
    **Mutagen:**
    
    **A. Fisik:**
    ```
    - Sinar gamma (Co-60)
    - Sinar X
    - Neutron cepat
    
    Dosis: 100-500 Gy (tergantung spesies)
    ```
    
    **B. Kimia:**
    ```
    - EMS (Ethyl Methanesulfonate)
    - MMS (Methyl Methanesulfonate)
    - Colchicine (untuk polyploidy)
    ```
    
    **Metode:**
    ```
    1. Iradiasi benih/pollen/tunas
    2. Tanam M1 (generasi pertama)
    3. Panen M1 (banyak mutan chimera)
    4. Tanam M2 (segregasi mutan)
    5. Seleksi mutan terbaik
    6. Uji stabilitas (M3-M5)
    7. Release varietas mutan
    
    Waktu: 5-8 tahun
    ```
    
    **Keberhasilan:**
    ```
    Varietas mutan yang dirilis: >3000 worldwide
    
    Contoh:
    - Padi: IR8 (semi-dwarf)
    - Gandum: Durum wheat (pasta)
    - Barley: Golden Promise (malting)
    ```
    
    **Referensi:**
    - FAO/IAEA Mutant Variety Database
    
    ---
    
    ## 📊 HERITABILITAS
    
    ### **Konsep:**
    
    ```
    Heritabilitas (h²) = Proporsi variasi fenotip yang disebabkan oleh genetik
    
    Vp (Variasi Fenotip) = Vg (Variasi Genetik) + Ve (Variasi Lingkungan)
    
    h² = Vg / Vp
    
    Range: 0 - 1 (atau 0% - 100%)
    ```
    
    **Interpretasi:**
    
    ```
    h² tinggi (>0.5):
    - Sifat sangat dipengaruhi genetik
    - Seleksi efektif
    - Contoh: Tinggi tanaman, warna bunga
    
    h² sedang (0.2-0.5):
    - Sifat dipengaruhi genetik + lingkungan
    - Seleksi cukup efektif
    - Contoh: Hasil panen, ukuran buah
    
    h² rendah (<0.2):
    - Sifat sangat dipengaruhi lingkungan
    - Seleksi kurang efektif
    - Contoh: Jumlah anakan (tillering)
    ```
    
    **Implikasi:**
    ```
    Sifat h² tinggi → Seleksi massa efektif
    Sifat h² rendah → Perlu progeny test, uji multilokasi
    ```
    
    ---
    
    ## 🎯 STRATEGI PEMULIAAN
    
    ### **Berdasarkan Sistem Reproduksi:**
    
    **1. Self-Pollinated (Menyerbuk Sendiri):**
    ```
    Contoh: Padi, gandum, kedelai, tomat
    
    Karakteristik:
    - Outcrossing <5%
    - Cepat homozigot
    - Varietas: Galur murni (pure line)
    
    Metode:
    - Pure line selection
    - Pedigree method
    - Bulk method
    - Single seed descent (SSD)
    ```
    
    **2. Cross-Pollinated (Menyerbuk Silang):**
    ```
    Contoh: Jagung, bunga matahari, bawang
    
    Karakteristik:
    - Outcrossing >50%
    - Heterozigot
    - Varietas: Hybrid, open-pollinated
    
    Metode:
    - Recurrent selection
    - Hybrid breeding
    - Population improvement
    ```
    
    **3. Vegetatif (Asexual):**
    ```
    Contoh: Kentang, ubi kayu, pisang, strawberry
    
    Karakteristik:
    - Perbanyakan klonal
    - Heterozigot dipertahankan
    - Varietas: Klon
    
    Metode:
    - Clonal selection
    - Somaclonal variation
    - Tissue culture
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Allard, R. W. (1999).** Principles of Plant Breeding, 2nd Edition. John Wiley & Sons.
    
    2. **Falconer, D. S., & Mackay, T. F. C. (1996).** Introduction to Quantitative Genetics, 4th Edition. Longman.
    
    3. **Acquaah, G. (2012).** Principles of Plant Genetics and Breeding, 2nd Edition. Wiley-Blackwell.
    
    4. **Mendel, G. (1866).** Experiments in Plant Hybridization. Verhandlungen des naturforschenden Vereines in Brünn.
    
    """)

# ===== TAB 2: SELEKSI VARIETAS =====
with tab_selection:
    st.header("🌱 Seleksi Varietas & Kriteria Pemilihan")
    
    st.markdown("""
    ### Pentingnya Pemilihan Varietas
    
    **Varietas yang tepat** = **50% keberhasilan budidaya**!
    
    **Faktor yang Dipengaruhi:**
    - ✅ Hasil panen (yield)
    - ✅ Kualitas produk
    - ✅ Ketahanan hama & penyakit
    - ✅ Adaptasi lingkungan
    - ✅ Profitabilitas
    
    ---
    
    ## 📋 KRITERIA PEMILIHAN VARIETAS
    
    ### **1. HASIL (Yield)**
    
    **Potensi Hasil:**
    ```
    Tinggi: >8 ton/ha (padi), >10 ton/ha (jagung)
    Sedang: 5-8 ton/ha (padi), 7-10 ton/ha (jagung)
    Rendah: <5 ton/ha (padi), <7 ton/ha (jagung)
    ```
    
    **Stabilitas Hasil:**
    ```
    Penting!
    - Varietas dengan hasil stabil lebih baik
    - Daripada hasil tinggi tapi tidak stabil
    
    Uji: Multilokasi, multitahun
    ```
    
    ---
    
    ### **2. KUALITAS**
    
    **Padi:**
    ```
    - Beras kepala: >60% (baik)
    - Kadar amilosa: 20-25% (pulen)
    - Aroma: Ada/tidak (sesuai pasar)
    - Warna: Putih bersih
    ```
    
    **Jagung:**
    ```
    - Kadar protein: >9% (pakan)
    - Kadar pati: >70% (industri)
    - Warna: Kuning/putih (sesuai pasar)
    ```
    
    **Tomat:**
    ```
    - Ukuran: Seragam, besar (>150g)
    - Warna: Merah cerah
    - Kekerasan: Firm (tahan transport)
    - Rasa: Manis (Brix >4%)
    ```
    
    ---
    
    ### **3. KETAHANAN HAMA & PENYAKIT**
    
    **Tingkat Ketahanan:**
    
    ```
    Immune (Imun):
    - Tidak pernah terserang
    - Sangat jarang
    
    Resistant (Tahan):
    - Terserang ringan
    - Tidak perlu pestisida
    - IDEAL!
    
    Moderately Resistant (Agak Tahan):
    - Terserang sedang
    - Perlu pestisida minimal
    
    Susceptible (Rentan):
    - Terserang berat
    - Perlu pestisida intensif
    - HINDARI!
    ```
    
    **Penyakit Penting:**
    
    **Padi:**
    ```
    - Blast (Pyricularia oryzae)
    - Bacterial leaf blight (Xanthomonas)
    - Tungro virus
    ```
    
    **Tomat:**
    ```
    - Late blight (Phytophthora)
    - Fusarium wilt
    - Tomato yellow leaf curl virus (TYLCV)
    ```
    
    **Jagung:**
    ```
    - Downy mildew (Peronosclerospora)
    - Leaf blight (Helminthosporium)
    - Corn borer (Ostrinia)
    ```
    
    ---
    
    ### **4. TOLERANSI STRESS ABIOTIK**
    
    **Kekeringan:**
    ```
    Penting untuk:
    - Lahan tadah hujan
    - Musim kemarau
    - Irigasi terbatas
    
    Indikator:
    - Akar dalam
    - Stomata efisien
    - Osmotic adjustment
    ```
    
    **Salinitas:**
    ```
    Penting untuk:
    - Lahan pesisir
    - Lahan bekas tambak
    
    Indikator:
    - Na+ exclusion
    - K+/Na+ ratio tinggi
    ```
    
    **Genangan:**
    ```
    Penting untuk:
    - Lahan rawa
    - Daerah banjir
    
    Indikator:
    - Elongation ability
    - Aerenchyma tissue
    ```
    
    **Suhu Ekstrem:**
    ```
    Panas (>35°C):
    - Pollen viability
    - Heat shock proteins
    
    Dingin (<15°C):
    - Cold tolerance
    - Antifreeze proteins
    ```
    
    ---
    
    ### **5. UMUR TANAMAN**
    
    **Klasifikasi:**
    
    **Genjah (Early):**
    ```
    - Umur: <100 hari (padi), <90 hari (jagung)
    - Keuntungan:
      ✅ Cepat panen
      ✅ 3x tanam/tahun
      ✅ Hindari puncak hama
    - Kekurangan:
      ❌ Hasil lebih rendah
      ❌ Ukuran lebih kecil
    ```
    
    **Sedang (Medium):**
    ```
    - Umur: 100-120 hari (padi), 90-110 hari (jagung)
    - Keuntungan:
      ✅ Hasil sedang-tinggi
      ✅ 2-3x tanam/tahun
    - Paling umum digunakan
    ```
    
    **Dalam (Late):**
    ```
    - Umur: >120 hari (padi), >110 hari (jagung)
    - Keuntungan:
      ✅ Hasil sangat tinggi
      ✅ Ukuran besar
    - Kekurangan:
      ❌ Lama panen
      ❌ 2x tanam/tahun
      ❌ Risiko hama tinggi
    ```
    
    ---
    
    ### **6. ADAPTASI LINGKUNGAN**
    
    **Ketinggian:**
    ```
    Dataran rendah (0-700 mdpl):
    - Suhu tinggi
    - Kelembaban tinggi
    - Contoh: IR64, Ciherang (padi)
    
    Dataran sedang (700-1000 mdpl):
    - Suhu sedang
    - Contoh: Situ Bagendit (padi)
    
    Dataran tinggi (>1000 mdpl):
    - Suhu rendah
    - Intensitas cahaya tinggi
    - Contoh: Pandan Wangi (padi)
    ```
    
    **Musim:**
    ```
    Musim hujan:
    - Tahan penyakit (kelembaban tinggi)
    - Tahan rebah
    
    Musim kemarau:
    - Toleran kekeringan
    - Efisien air
    ```
    
    **Jenis Tanah:**
    ```
    Sawah:
    - Toleran genangan
    - Contoh: Padi sawah
    
    Tadah hujan:
    - Toleran kekeringan
    - Contoh: Padi gogo
    
    Lahan kering:
    - Sistem akar kuat
    - Contoh: Jagung, kedelai
    ```
    
    ---
    
    ## 🔍 CARA MENGENAL VARIETAS
    
    ### **1. Deskripsi Varietas**
    
    **Informasi Penting:**
    ```
    - Nama varietas
    - Tahun pelepasan
    - Pemulia/institusi
    - Potensi hasil
    - Umur tanaman
    - Ketahanan hama/penyakit
    - Kualitas
    - Anjuran tanam (lokasi, musim)
    ```
    
    **Sumber:**
    - Katalog varietas (Kementan)
    - Brosur produsen benih
    - Website resmi (BPTP, Balitbangtan)
    
    ---
    
    ### **2. Uji Adaptasi (On-Farm Trial)**
    
    **Protokol:**
    ```
    1. Pilih 3-5 varietas kandidat
    2. Tanam di lahan sendiri (plot kecil)
    3. Bandingkan dengan varietas lokal (kontrol)
    4. Evaluasi:
       - Pertumbuhan
       - Ketahanan hama/penyakit
       - Hasil
       - Kualitas
    5. Pilih yang terbaik
    6. Tanam skala besar musim berikutnya
    
    Waktu: 1-2 musim tanam
    ```
    
    **Keuntungan:**
    ```
    ✅ Tahu performa di lahan sendiri
    ✅ Minimal risiko (plot kecil)
    ✅ Belajar budidaya varietas baru
    ```
    
    ---
    
    ## 📊 PERBANDINGAN VARIETAS
    
    ### **Contoh: Varietas Padi**
    
    | Varietas | Umur (hari) | Hasil (ton/ha) | Ketahanan | Kualitas Beras | Anjuran |
    |----------|-------------|----------------|-----------|----------------|---------|
    | **IR64** | 115-125 | 5-6 | Blast (T), BLB (R) | Pulen, kepala 60% | Dataran rendah, sawah |
    | **Ciherang** | 116-125 | 6-7 | Blast (T), BLB (T), Wereng (T) | Pulen, kepala 65% | Dataran rendah-sedang |
    | **Inpari 32** | 115-120 | 7-8 | Blast (T), BLB (T), Hawar (T) | Pulen, kepala 70% | Dataran rendah, sawah |
    | **Situ Bagendit** | 125-135 | 6-7 | Blast (T), BLB (T) | Pulen, kepala 65% | Dataran sedang |
    | **Pandan Wangi** | 140-150 | 4-5 | Blast (R) | Wangi, pulen, premium | Dataran tinggi |
    
    **Keterangan:**
    - T = Tahan
    - R = Rentan
    - BLB = Bacterial Leaf Blight
    
    ---
    
    ### **Contoh: Varietas Jagung**
    
    | Varietas | Tipe | Umur (hari) | Hasil (ton/ha) | Ketahanan | Kegunaan |
    |----------|------|-------------|----------------|-----------|----------|
    | **Bisi 18** | Hybrid | 95-100 | 10-12 | DM (T), Borer (T) | Pakan, pangan |
    | **Pioneer 21** | Hybrid | 100-105 | 11-13 | DM (T), Blight (T) | Pakan, industri |
    | **NK 212** | Hybrid | 95-100 | 10-11 | DM (T) | Pakan |
    | **Bisma** | OP | 95-100 | 6-7 | DM (AT) | Pangan |
    | **Pulut** | OP | 100-110 | 4-5 | DM (R) | Pangan (ketan) |
    
    **Keterangan:**
    - DM = Downy Mildew
    - AT = Agak Tahan
    - OP = Open-Pollinated
    
    ---
    
    ## 💡 TIPS PEMILIHAN VARIETAS
    
    **1. Sesuaikan dengan Tujuan:**
    ```
    Konsumsi sendiri:
    - Prioritas: Kualitas, rasa
    - Contoh: Pandan Wangi (padi), Pulut (jagung)
    
    Komersial:
    - Prioritas: Hasil, harga jual
    - Contoh: Ciherang (padi), Bisi 18 (jagung)
    
    Industri:
    - Prioritas: Kualitas spesifik (pati, protein)
    - Contoh: Pioneer 21 (jagung)
    ```
    
    **2. Sesuaikan dengan Kondisi Lahan:**
    ```
    Sawah irigasi teknis:
    - Varietas hasil tinggi
    - Contoh: Inpari 32
    
    Tadah hujan:
    - Varietas toleran kekeringan
    - Contoh: Situ Bagendit
    
    Dataran tinggi:
    - Varietas adaptasi suhu rendah
    - Contoh: Pandan Wangi
    ```
    
    **3. Pertimbangkan Pasar:**
    ```
    Cek harga:
    - Varietas premium → Harga tinggi
    - Varietas biasa → Harga standar
    
    Cek permintaan:
    - Varietas populer → Mudah jual
    - Varietas langka → Susah jual (kecuali niche market)
    ```
    
    **4. Gunakan Benih Bersertifikat:**
    ```
    ✅ Kemurnian terjamin (>98%)
    ✅ Daya tumbuh tinggi (>80%)
    ✅ Bebas penyakit
    ✅ Performa sesuai deskripsi
    
    Label:
    - Benih Penjenis (Breeder Seed) - Putih
    - Benih Dasar (Foundation Seed) - Putih bergaris ungu
    - Benih Pokok (Stock Seed) - Ungu
    - Benih Sebar (Extension Seed) - Biru
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Kementerian Pertanian RI.** Katalog Varietas Unggul Tanaman Pangan.
    
    2. **IRRI (International Rice Research Institute).** Rice Knowledge Bank.
    
    3. **CIMMYT (International Maize and Wheat Improvement Center).** Maize Varieties Database.
    
    """)

# ===== TAB 3: HYBRID VS OPEN-POLLINATED =====
with tab_hybrid:
    st.header("🌾 Hybrid vs Open-Pollinated")
    
    st.markdown("""
    ### Perbedaan Fundamental
    
    **Hybrid (F1 Hybrid):**
    ```
    Hasil persilangan 2 tetua berbeda (inbred lines)
    → F1 heterozigot
    → Menunjukkan heterosis (hybrid vigor)
    → Tidak bisa ditanam ulang (F2 segregasi)
    ```
    
    **Open-Pollinated (OP):**
    ```
    Populasi heterogen
    → Penyerbukan bebas dalam populasi
    → Bisa ditanam ulang
    → Performa stabil antar generasi
    ```
    
    ---
    
    ## 💪 HETEROSIS (Hybrid Vigor)
    
    ### **Konsep:**
    
    ```
    Heterosis = F1 hybrid lebih unggul dari kedua tetuanya
    
    Contoh:
    P1 (Inbred A): Hasil 5 ton/ha
    P2 (Inbred B): Hasil 5 ton/ha
    F1 (A × B): Hasil 10 ton/ha (100% heterosis!)
    ```
    
    **Teori:**
    
    **1. Dominance Theory:**
    ```
    Alel dominan menguntungkan dari kedua tetua berkumpul di F1
    → Menutupi alel resesif merugikan
    → Performa superior
    ```
    
    **2. Overdominance Theory:**
    ```
    Heterozigot (Aa) lebih baik dari homozigot (AA atau aa)
    → Interaksi alel menguntungkan
    ```
    
    **Referensi:**
    - Shull, G. H. (1908). The Composition of a Field of Maize. American Breeders Association Reports.
    
    ---
    
    ## 🌽 PRODUKSI HYBRID (Hybrid Seed Production)
    
    ### **Tahapan:**
    
    **1. Pembuatan Inbred Lines:**
    ```
    Tujuan: Homozigot murni
    
    Metode:
    - Self-pollination berulang (6-8 generasi)
    - Seleksi setiap generasi
    
    S0 (awal) → S1 → S2 → S3 → S4 → S5 → S6 (inbred)
    
    Waktu: 6-8 tahun
    
    Karakteristik inbred:
    - Homozigot (>98%)
    - Vigor rendah (inbreeding depression)
    - Seragam
    ```
    
    **2. Uji Combining Ability:**
    ```
    Tujuan: Cari kombinasi inbred terbaik
    
    Metode:
    - Silangkan semua kombinasi inbred
    - Uji performa F1
    - Pilih kombinasi dengan heterosis tertinggi
    
    Contoh:
    Inbred A × Inbred B → F1 (AB) - Hasil 10 ton/ha ✅
    Inbred A × Inbred C → F1 (AC) - Hasil 8 ton/ha
    Inbred B × Inbred C → F1 (BC) - Hasil 9 ton/ha
    
    Pilih: A × B (terbaik)
    ```
    
    **3. Produksi Benih Hybrid:**
    
    **Metode Detasseling (Jagung):**
    ```
    Lahan produksi benih:
    - Tanam Inbred A (female) : Inbred B (male) = 6 : 2 (ratio)
    - Buang bunga jantan (tassel) dari Inbred A
    - Serbuk sari dari Inbred B menyerbuki Inbred A
    - Panen benih dari Inbred A saja
    → Benih F1 hybrid
    
    Tenaga kerja: Intensif (detasseling manual)
    ```
    
    **Metode Male Sterility (Berbagai tanaman):**
    ```
    Gunakan Inbred A dengan male sterility (CMS - Cytoplasmic Male Sterility)
    → Tidak perlu detasseling
    → Otomatis cross-pollination
    
    Lebih efisien!
    ```
    
    ---
    
    ## 📊 PERBANDINGAN HYBRID VS OPEN-POLLINATED
    
    | Aspek | Hybrid (F1) | Open-Pollinated (OP) |
    |-------|-------------|----------------------|
    | **Hasil** | Sangat tinggi (heterosis) | Sedang |
    | **Keseragaman** | Sangat seragam | Bervariasi |
    | **Vigor** | Sangat kuat | Sedang |
    | **Harga Benih** | Mahal (Rp 50-150K/kg) | Murah (Rp 10-30K/kg) |
    | **Bisa Ditanam Ulang?** | ❌ TIDAK (F2 segregasi) | ✅ YA (stabil) |
    | **Investasi Awal** | Tinggi | Rendah |
    | **ROI** | Tinggi (jika dikelola baik) | Sedang |
    | **Ketergantungan** | Tinggi (harus beli benih) | Rendah (bisa simpan benih) |
    | **Cocok untuk** | Komersial, intensif | Subsisten, organik |
    
    ---
    
    ## 💰 ANALISIS EKONOMI
    
    ### **Contoh: Jagung Hybrid vs OP**
    
    **HYBRID (Bisi 18):**
    ```
    Biaya Benih: Rp 100,000/kg (20 kg/ha) = Rp 2,000,000
    Hasil: 10 ton/ha
    Harga jual: Rp 4,000/kg
    Pendapatan: 10,000 kg × Rp 4,000 = Rp 40,000,000
    
    Biaya lain (pupuk, pestisida, tenaga): Rp 15,000,000
    Total biaya: Rp 17,000,000
    
    PROFIT: Rp 23,000,000/ha
    ```
    
    **OPEN-POLLINATED (Bisma):**
    ```
    Biaya Benih: Rp 20,000/kg (20 kg/ha) = Rp 400,000
    (Atau GRATIS jika simpan benih sendiri)
    
    Hasil: 6 ton/ha
    Harga jual: Rp 4,000/kg
    Pendapatan: 6,000 kg × Rp 4,000 = Rp 24,000,000
    
    Biaya lain: Rp 12,000,000
    Total biaya: Rp 12,400,000
    
    PROFIT: Rp 11,600,000/ha
    ```
    
    **KESIMPULAN:**
    ```
    Hybrid: Profit 2x lebih tinggi!
    Tapi: Investasi awal lebih besar
    
    Pilihan:
    - Modal cukup + Intensif → HYBRID
    - Modal terbatas + Subsisten → OP
    ```
    
    ---
    
    ## ⚠️ MASALAH HYBRID
    
    **1. F2 Segregasi:**
    ```
    F1 (Hybrid): Seragam, hasil tinggi
    F2 (Turunan F1): Segregasi (bervariasi), hasil turun 30-50%
    
    JANGAN tanam benih dari hybrid!
    Harus beli benih baru setiap musim
    ```
    
    **2. Ketergantungan:**
    ```
    Petani tergantung pada perusahaan benih
    → Harga benih bisa naik
    → Ketersediaan benih bisa terbatas
    ```
    
    **3. Biaya Tinggi:**
    ```
    Benih mahal
    → Risiko gagal panen lebih besar (kerugian besar)
    ```
    
    ---
    
    ## 💡 REKOMENDASI
    
    **Gunakan HYBRID jika:**
    ```
    ✅ Modal cukup
    ✅ Lahan subur + irigasi baik
    ✅ Manajemen intensif
    ✅ Akses pasar baik
    ✅ Target: Profit maksimal
    
    Contoh: Jagung komersial, tomat greenhouse
    ```
    
    **Gunakan OPEN-POLLINATED jika:**
    ```
    ✅ Modal terbatas
    ✅ Lahan marginal
    ✅ Manajemen sederhana
    ✅ Ingin simpan benih sendiri
    ✅ Target: Swasembada, organik
    
    Contoh: Padi subsisten, jagung lokal
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Shull, G. H. (1908).** The Composition of a Field of Maize. American Breeders Association Reports, 4, 296-301.
    
    2. **Duvick, D. N. (2001).** Biotechnology in the 1930s: the development of hybrid maize. Nature Reviews Genetics, 2(1), 69-74.
    
    3. **Hallauer, A. R., et al. (2010).** Quantitative Genetics in Maize Breeding. Springer.
    
    """)

# ===== TAB 4: GMO & BIOTEKNOLOGI =====
with tab_biotech:
    st.header("🔬 GMO & Bioteknologi")
    
    st.markdown("""
    ### Definisi
    
    **GMO (Genetically Modified Organism):**
    ```
    Organisme yang DNA-nya dimodifikasi menggunakan teknologi rekayasa genetika
    → Tambah/hapus/ubah gen tertentu
    → Sifat baru yang tidak ada di alam
    ```
    
    **Bioteknologi:**
    ```
    Penggunaan organisme hidup atau komponennya untuk menghasilkan produk
    
    Klasik: Fermentasi, seleksi tradisional
    Modern: Rekayasa genetika, kultur jaringan
    ```
    
    ---
    
    ## 🧬 REKAYASA GENETIKA (Genetic Engineering)
    
    ### **Prinsip:**
    
    ```
    1. Identifikasi gen target (contoh: gen Bt untuk tahan hama)
    2. Isolasi gen dari organisme donor
    3. Insert gen ke DNA tanaman target
    4. Regenerasi tanaman transgenik
    5. Uji & seleksi
    6. Release sebagai varietas GMO
    ```
    
    ---
    
    ### **Metode Transfer Gen:**
    
    **1. Agrobacterium-mediated Transformation:**
    ```
    Prinsip:
    - Agrobacterium tumefaciens = bakteri tanah
    - Secara alami bisa transfer DNA (T-DNA) ke tanaman
    - Manfaatkan untuk transfer gen target
    
    Tahapan:
    1. Insert gen target ke plasmid Agrobacterium
    2. Infeksi sel tanaman dengan Agrobacterium
    3. T-DNA (dengan gen target) masuk ke genom tanaman
    4. Kultur jaringan → Regenerasi tanaman transgenik
    5. Seleksi (marker gene, contoh: resistensi antibiotik)
    
    Keuntungan:
    ✅ Efisien
    ✅ Single copy insertion (stabil)
    ✅ Murah
    
    Kekurangan:
    ❌ Tidak semua tanaman susceptible (monocot sulit)
    
    Cocok untuk: Dicot (tomat, kentang, kedelai)
    ```
    
    **2. Gene Gun (Biolistic):**
    ```
    Prinsip:
    - "Tembak" DNA dengan partikel emas/tungsten
    - Masuk ke sel tanaman secara fisik
    
    Tahapan:
    1. Coat partikel emas dengan DNA (gen target)
    2. Tembak ke sel tanaman dengan gene gun
    3. DNA masuk ke genom
    4. Kultur jaringan → Regenerasi
    5. Seleksi
    
    Keuntungan:
    ✅ Bisa untuk semua tanaman (termasuk monocot)
    ✅ Tidak tergantung Agrobacterium
    
    Kekurangan:
    ❌ Multiple copy insertion (kurang stabil)
    ❌ Mahal
    
    Cocok untuk: Monocot (padi, jagung, gandum)
    ```
    
    **3. Electroporation:**
    ```
    Prinsip:
    - Kejut listrik → Pori di membran sel
    - DNA masuk melalui pori
    
    Cocok untuk: Protoplas (sel tanpa dinding sel)
    ```
    
    ---
    
    ## 🌾 CONTOH TANAMAN GMO
    
    ### **1. Bt Crops (Bacillus thuringiensis)**
    
    **Gen:** Cry gene dari bakteri Bt
    
    **Fungsi:**
    ```
    Produksi protein Bt (Cry toxin)
    → Racun untuk serangga hama (lepidoptera, coleoptera)
    → Tapi aman untuk manusia & hewan
    ```
    
    **Tanaman:**
    ```
    - Bt Cotton (kapas)
    - Bt Corn (jagung)
    - Bt Eggplant (terong)
    ```
    
    **Keuntungan:**
    ```
    ✅ Kurangi pestisida 50-80%
    ✅ Hasil ↑ 10-30%
    ✅ Biaya ↓
    ✅ Lingkungan lebih baik
    ```
    
    **Adopsi:**
    ```
    Global: >100 juta ha (2020)
    Negara: USA, Brazil, Argentina, India, China
    ```
    
    ---
    
    ### **2. Herbicide-Tolerant Crops**
    
    **Gen:** EPSPS gene (dari Agrobacterium)
    
    **Fungsi:**
    ```
    Toleran terhadap herbisida glyphosate (Roundup)
    → Bisa semprot herbisida tanpa bunuh tanaman
    → Kontrol gulma efektif
    ```
    
    **Tanaman:**
    ```
    - Roundup Ready Soybean (kedelai)
    - Roundup Ready Corn (jagung)
    - Roundup Ready Cotton (kapas)
    ```
    
    **Keuntungan:**
    ```
    ✅ Kontrol gulma mudah
    ✅ No-till farming (konservasi tanah)
    ✅ Hemat tenaga kerja
    ```
    
    **Kontroversi:**
    ```
    ⚠️ Gulma resisten (superweeds)
    ⚠️ Ketergantungan herbisida
    ```
    
    ---
    
    ### **3. Golden Rice**
    
    **Gen:** Beta-carotene biosynthesis genes
    
    **Fungsi:**
    ```
    Produksi beta-carotene (provitamin A) di beras
    → Warna kuning keemasan
    → Atasi defisiensi vitamin A
    ```
    
    **Target:**
    ```
    Negara berkembang dengan defisiensi vitamin A
    → Kebutaan, kematian anak
    ```
    
    **Status:**
    ```
    Approved: Filipina, Bangladesh, USA
    Kontroversi: Greenpeace menentang
    ```
    
    **Referensi:**
    - Ye, X., et al. (2000). Engineering the provitamin A (β-carotene) biosynthetic pathway into (carotenoid-free) rice endosperm. Science, 287(5451), 303-305.
    
    ---
    
    ## ✂️ CRISPR-Cas9 (Gene Editing)
    
    ### **Prinsip:**
    
    ```
    CRISPR = Clustered Regularly Interspaced Short Palindromic Repeats
    Cas9 = Protein "gunting" DNA
    
    Fungsi:
    - Potong DNA di lokasi spesifik
    - Edit/hapus/tambah gen
    - Presisi tinggi!
    ```
    
    **Cara Kerja:**
    ```
    1. Design guide RNA (gRNA) → Target gen spesifik
    2. gRNA + Cas9 → Kompleks
    3. Kompleks cari & potong DNA target
    4. Sel repair DNA:
       - Non-Homologous End Joining (NHEJ) → Knockout gen
       - Homology-Directed Repair (HDR) → Insert gen baru
    5. Gen ter-edit!
    ```
    
    **Keuntungan vs GMO Konvensional:**
    ```
    ✅ Lebih presisi (target spesifik)
    ✅ Lebih cepat (1-2 tahun vs 5-10 tahun)
    ✅ Tidak insert DNA asing (bisa non-transgenic)
    ✅ Regulasi lebih mudah (beberapa negara)
    ```
    
    **Contoh Aplikasi:**
    ```
    - Tomat tahan penyakit (powdery mildew)
    - Gandum low-gluten (celiac disease)
    - Jamur tidak browning
    - Padi tahan kekeringan
    ```
    
    **Referensi:**
    - Doudna, J. A., & Charpentier, E. (2014). The new frontier of genome engineering with CRISPR-Cas9. Science, 346(6213).
    
    ---
    
    ## ⚖️ PRO & KONTRA GMO
    
    ### **PRO (Keuntungan):**
    
    ```
    ✅ Hasil lebih tinggi
    ✅ Kurangi pestisida (Bt crops)
    ✅ Toleran stress (kekeringan, salinitas)
    ✅ Nutrisi lebih baik (Golden Rice)
    ✅ Shelf-life lebih panjang (Flavr Savr tomato)
    ✅ Biofuel (algae GMO)
    ✅ Farmasi (insulin dari bakteri GMO)
    ```
    
    ### **KONTRA (Kekhawatiran):**
    
    ```
    ⚠️ Keamanan pangan (alergi, toksisitas)
       → Tapi: Belum ada bukti ilmiah bahaya
    
    ⚠️ Lingkungan:
       - Gene flow ke tanaman liar
       - Superweeds (gulma resisten)
       - Dampak biodiversitas
    
    ⚠️ Sosial-ekonomi:
       - Monopoli perusahaan benih (Monsanto, dll)
       - Ketergantungan petani
       - Hak paten
    
    ⚠️ Etika:
       - "Main Tuhan"?
       - Hak konsumen untuk tahu (labeling)
    ```
    
    ---
    
    ## 📋 REGULASI GMO
    
    ### **Global:**
    
    **Permisif (Pro-GMO):**
    ```
    - USA: Approved banyak GMO (jagung, kedelai, kapas, dll)
    - Brazil, Argentina: Adopsi luas
    - Filipina: Golden Rice approved
    ```
    
    **Ketat (Anti-GMO):**
    ```
    - EU: Regulasi sangat ketat, sedikit GMO approved
    - Rusia: Ban GMO
    - Banyak negara Afrika: Ban/ketat
    ```
    
    **Indonesia:**
    ```
    Status: Ketat, tapi beberapa GMO approved untuk pakan (jagung, kedelai)
    
    Regulasi:
    - PP No. 21/2005: Keamanan Hayati Produk Rekayasa Genetik
    - Perlu uji keamanan pangan, lingkungan
    - Labeling wajib
    
    GMO Approved:
    - Jagung Bt (untuk pakan ternak)
    - Kedelai Roundup Ready (impor untuk pakan)
    
    GMO untuk Konsumsi Manusia: Belum approved
    ```
    
    ---
    
    ## 🔬 BIOTEKNOLOGI LAIN
    
    ### **1. Kultur Jaringan (Tissue Culture):**
    
    ```
    Prinsip: Regenerasi tanaman dari sel/jaringan
    
    Aplikasi:
    - Perbanyakan massal (pisang, anggrek)
    - Bebas penyakit (meristem culture)
    - Konservasi germplasm
    - Produksi secondary metabolites
    
    Keuntungan:
    ✅ Cepat (ribuan tanaman dari 1 eksplan)
    ✅ Seragam (klonal)
    ✅ Bebas penyakit
    ```
    
    ---
    
    ### **2. Marker-Assisted Selection (MAS):**
    
    ```
    Prinsip: Gunakan DNA marker untuk seleksi
    
    Tahapan:
    1. Identifikasi marker linked dengan gen target
    2. Skrining DNA seedling (PCR)
    3. Pilih seedling dengan marker positif
    4. Buang yang negatif (sebelum tanam!)
    
    Keuntungan:
    ✅ Seleksi lebih awal (seedling stage)
    ✅ Lebih akurat
    ✅ Hemat waktu & biaya
    
    Aplikasi:
    - Seleksi resistensi penyakit
    - Seleksi kualitas (amilosa, protein)
    - Backcross breeding (percepat)
    ```
    
    ---
    
    ### **3. Genomic Selection:**
    
    ```
    Prinsip: Gunakan seluruh genom untuk prediksi
    
    Metode:
    - Genotyping (SNP array, sequencing)
    - Phenotyping (uji lapangan)
    - Model statistik → Prediksi breeding value
    - Seleksi berdasarkan prediksi
    
    Keuntungan:
    ✅ Akurasi tinggi
    ✅ Percepat breeding cycle
    
    Aplikasi:
    - Breeding tanaman perennial (kelapa sawit)
    - Sifat kompleks (yield, stress tolerance)
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Ye, X., et al. (2000).** Engineering the provitamin A (β-carotene) biosynthetic pathway into rice endosperm. Science, 287(5451), 303-305.
    
    2. **Doudna, J. A., & Charpentier, E. (2014).** The new frontier of genome engineering with CRISPR-Cas9. Science, 346(6213).
    
    3. **James, C. (2019).** Global Status of Commercialized Biotech/GM Crops. ISAAA Brief No. 55.
    
    4. **Collard, B. C. Y., & Mackill, D. J. (2008).** Marker-assisted selection: an approach for precision plant breeding in the twenty-first century. Philosophical Transactions of the Royal Society B, 363(1491), 557-572.
    
    """)

# ===== TAB 5: PERBANYAKAN TANAMAN =====
with tab_propagation:
    st.header("🌿 Metode Perbanyakan Tanaman")
    
    st.markdown("""
    ### Definisi
    
    **Perbanyakan tanaman** adalah proses **memproduksi tanaman baru** dari tanaman induk untuk **mempertahankan sifat unggul** dan **meningkatkan populasi**.
    
    **Jenis Perbanyakan:**
    - 🌱 **Generatif (Sexual):** Melalui biji
    - 🌿 **Vegetatif (Asexual):** Tanpa biji (stek, cangkok, okulasi, dll)
    
    ---
    
    ## 🌱 PERBANYAKAN GENERATIF (BIJI)
    
    ### **Karakteristik:**
    
    ```
    Keuntungan:
    ✅ Mudah (tanam biji)
    ✅ Murah
    ✅ Jumlah banyak
    ✅ Bebas penyakit (biasanya)
    ✅ Variasi genetik (breeding)
    
    Kekurangan:
    ❌ Tidak identik dengan induk (kecuali self-pollinated)
    ❌ Lama berbuah (3-10 tahun untuk pohon)
    ❌ Kualitas tidak terjamin (segregasi)
    ```
    
    **Cocok untuk:**
    - Tanaman self-pollinated (padi, gandum, kedelai)
    - Tanaman semusim (sayuran)
    - Breeding program
    
    **TIDAK cocok untuk:**
    - Hybrid (F2 segregasi)
    - Tanaman cross-pollinated (variasi tinggi)
    - Tanaman yang sulit berbunga/biji
    
    ---
    
    ## 🌿 PERBANYAKAN VEGETATIF
    
    ### **Karakteristik:**
    
    ```
    Keuntungan:
    ✅ Identik dengan induk (klonal)
    ✅ Cepat berbuah (1-3 tahun)
    ✅ Kualitas terjamin
    ✅ Pertahankan sifat unggul
    
    Kekurangan:
    ❌ Lebih sulit
    ❌ Lebih mahal
    ❌ Jumlah terbatas
    ❌ Risiko penyakit (jika induk sakit)
    ```
    
    ---
    
    ## ✂️ STEK (Cutting)
    
    ### **Prinsip:**
    ```
    Potong bagian tanaman → Tanam → Tumbuh akar & tunas baru
    → Tanaman baru identik dengan induk
    ```
    
    ### **Jenis Stek:**
    
    **1. STEK BATANG (Stem Cutting):**
    
    **A. Stek Pucuk (Tip Cutting):**
    ```
    Bagian: Ujung batang muda (10-15 cm)
    
    Cocok untuk:
    - Tanaman hias (Gelombang Cinta, Sirih Gading)
    - Sayuran (Kangkung, Bayam)
    - Buah (Anggur, Markisa)
    
    Protokol:
    1. Pilih pucuk sehat, tidak terlalu muda/tua
    2. Potong 10-15 cm (3-4 ruas)
    3. Buang daun bawah, sisakan 2-3 daun atas
    4. Potong daun atas 1/2 (kurangi transpirasi)
    5. Celup pangkal ke rootone (hormon akar)
    6. Tanam di media (pasir/sekam/cocopeat)
    7. Jaga kelembaban (sungkup plastik)
    8. Akar tumbuh 2-4 minggu
    9. Pindah ke pot/lahan
    
    Keberhasilan: 70-90%
    ```
    
    **B. Stek Batang (Stem Cutting):**
    ```
    Bagian: Batang tengah (15-30 cm)
    
    Cocok untuk:
    - Singkong
    - Tebu
    - Ubi jalar
    
    Protokol:
    1. Pilih batang sehat, diameter 1-2 cm
    2. Potong 20-30 cm (3-5 ruas)
    3. Tanam miring (45°) atau horizontal
    4. Kubur 2/3 bagian
    5. Siram rutin
    6. Tunas muncul 1-2 minggu
    
    Keberhasilan: 80-95%
    ```
    
    **C. Stek Akar (Root Cutting):**
    ```
    Bagian: Akar
    
    Cocok untuk:
    - Sukun
    - Raspberry
    - Horseradish
    
    Protokol:
    1. Gali akar lateral (diameter 0.5-1 cm)
    2. Potong 5-10 cm
    3. Tanam horizontal, kedalaman 2-3 cm
    4. Tunas muncul dari akar
    
    Keberhasilan: 50-70%
    ```
    
    ---
    
    **2. STEK DAUN (Leaf Cutting):**
    
    ```
    Bagian: Daun
    
    Cocok untuk:
    - Begonia
    - Sansevieria (lidah mertua)
    - African Violet
    - Succulent
    
    Protokol:
    1. Pilih daun sehat, dewasa
    2. Potong dengan tangkai (jika ada)
    3. Tanam tangkai di media
    4. Atau: Potong daun jadi beberapa bagian
    5. Tancapkan di media
    6. Akar & tunas muncul dari pangkal daun
    
    Waktu: 4-8 minggu
    Keberhasilan: 60-80%
    ```
    
    ---
    
    ### **Tips Sukses Stek:**
    
    ```
    1. WAKTU:
       - Pagi hari (turgor tinggi)
       - Musim hujan (kelembaban tinggi)
    
    2. ALAT:
       - Pisau/gunting tajam (clean cut)
       - Steril (alkohol/api)
    
    3. HORMON PERANGSANG AKAR:
       - Rootone (IBA/NAA)
       - Atau: Air kelapa muda
       - Celup pangkal stek 5-10 detik
    
    4. MEDIA:
       - Steril, porous, drainase baik
       - Campuran: Pasir + Sekam + Cocopeat (1:1:1)
    
    5. KELEMBABAN:
       - Tinggi (80-90%)
       - Sungkup plastik/greenhouse
       - Semprot air 2-3x/hari
    
    6. CAHAYA:
       - Terang tapi tidak langsung
       - Hindari sinar matahari penuh (layu)
    
    7. SUHU:
       - Optimal: 25-30°C
    ```
    
    ---
    
    ## 🌳 CANGKOK (Air Layering)
    
    ### **Prinsip:**
    ```
    Luka batang → Tutup media lembab → Akar tumbuh
    → Potong & tanam → Tanaman baru
    ```
    
    ### **Protokol:**
    
    ```
    1. PILIH CABANG:
       - Sehat, diameter 1-2 cm
       - Umur 1-2 tahun
       - Tidak terlalu muda/tua
    
    2. KELUPAS KULIT:
       - Sayat melingkar (2 sayatan, jarak 3-5 cm)
       - Kelupas kulit & kambium
       - Bersihkan getah (jika ada)
    
    3. APLIKASI HORMON (Optional):
       - Oleskan rootone di bagian atas luka
    
    4. TUTUP MEDIA:
       - Bungkus dengan media lembab:
         * Tanah + Kompos + Sekam (1:1:1)
         * Atau: Cocopeat + Kompos
       - Bungkus dengan plastik (transparan)
       - Ikat atas & bawah (kedap air)
    
    5. PERAWATAN:
       - Cek kelembaban (seminggu sekali)
       - Semprot air jika kering
       - Jangan terlalu basah (busuk)
    
    6. AKAR TUMBUH:
       - Waktu: 1-3 bulan (tergantung spesies)
       - Akar terlihat di plastik
    
    7. POTONG & TANAM:
       - Potong di bawah akar
       - Buka plastik hati-hati
       - Tanam di pot/lahan
       - Pangkas daun 50% (kurangi transpirasi)
       - Naungi 1-2 minggu
    
    Keberhasilan: 80-95%
    ```
    
    **Cocok untuk:**
    - Mangga
    - Jambu
    - Rambutan
    - Lengkeng
    - Leci
    - Tanaman hias (Kamboja, Bougenville)
    
    **Keuntungan:**
    ```
    ✅ Keberhasilan tinggi (akar tumbuh sebelum dipotong)
    ✅ Tanaman besar langsung
    ✅ Cepat berbuah (1-2 tahun)
    ```
    
    **Kekurangan:**
    ```
    ❌ Lambat (1-3 bulan)
    ❌ Jumlah terbatas (1 cangkok/cabang)
    ❌ Merusak pohon induk
    ```
    
    ---
    
    ## 🌱 OKULASI & SAMBUNG (Grafting & Budding)
    
    ### **Prinsip:**
    ```
    Gabungkan 2 tanaman berbeda:
    - Batang bawah (rootstock): Akar kuat, tahan penyakit
    - Batang atas (scion/entres): Varietas unggul
    
    → Tumbuh jadi 1 tanaman dengan sifat gabungan
    ```
    
    ### **Jenis:**
    
    **1. OKULASI (Budding):**
    
    **A. Okulasi Mata Tidur (T-Budding):**
    ```
    Bagian: Mata tunas (bud)
    
    Protokol:
    1. BATANG BAWAH:
       - Diameter 0.5-1 cm
       - Umur 6-12 bulan
       - Sayat bentuk T (2-3 cm vertikal, 1 cm horizontal)
       - Buka kulit
    
    2. MATA TUNAS:
       - Pilih dari cabang sehat
       - Potong perisai (shield) 2-3 cm
       - Sisipkan ke sayatan T
    
    3. IKAT:
       - Plastik okulasi (atas-bawah)
       - Mata tunas terbuka
    
    4. PERAWATAN:
       - Cek 2-3 minggu (mata hijau = berhasil)
       - Buka ikatan setelah 1 bulan
       - Potong batang bawah di atas mata (setelah tunas tumbuh)
    
    Waktu: Tunas tumbuh 3-4 minggu
    Keberhasilan: 70-90%
    
    Cocok untuk: Jeruk, Mangga, Jambu, Mawar
    ```
    
    **B. Okulasi Chip (Chip Budding):**
    ```
    Mirip T-budding, tapi:
    - Sayatan bentuk chip (potongan kecil)
    - Bisa untuk batang lebih besar
    
    Cocok untuk: Apel, Pir, Cherry
    ```
    
    ---
    
    **2. SAMBUNG (Grafting):**
    
    **A. Sambung Pucuk (Cleft Grafting):**
    ```
    Protokol:
    1. BATANG BAWAH:
       - Diameter 2-5 cm
       - Potong horizontal
       - Belah tengah (2-3 cm)
    
    2. ENTRES (Scion):
       - Pucuk sehat, diameter 0.5-1 cm
       - Panjang 10-15 cm (3-4 mata)
       - Runcing kedua sisi (bentuk V)
    
    3. SAMBUNG:
       - Sisipkan entres ke belahan batang bawah
       - Kambium bertemu kambium (PENTING!)
    
    4. IKAT & TUTUP:
       - Ikat dengan tali rafia
       - Tutup dengan lilin/plastik (cegah kering)
    
    5. PERAWATAN:
       - Tunas tumbuh 2-4 minggu
       - Buka ikatan setelah 2-3 bulan
    
    Keberhasilan: 60-80%
    
    Cocok untuk: Mangga, Durian, Alpukat
    ```
    
    **B. Sambung Sisip (Side Grafting):**
    ```
    - Entres disisipkan di sisi batang bawah
    - Tidak perlu potong batang bawah
    - Cocok untuk: Kaktus, tanaman hias
    ```
    
    ---
    
    ### **Keuntungan Okulasi/Sambung:**
    
    ```
    ✅ Gabungkan sifat unggul:
       - Akar kuat + Buah berkualitas
       - Tahan penyakit + Produktif
    
    ✅ Cepat berbuah (2-3 tahun vs 5-10 tahun dari biji)
    
    ✅ Kualitas terjamin (identik dengan induk)
    
    ✅ Adaptasi:
       - Batang bawah lokal (adaptasi tanah/iklim)
       - Batang atas varietas unggul
    
    ✅ Rejuvenasi pohon tua (top working)
    ```
    
    **Aplikasi:**
    - Buah: Jeruk, Mangga, Durian, Apel
    - Hias: Mawar, Kaktus, Adenium
    
    ---
    
    ## 🌿 MERUNDUK (Layering)
    
    ### **Prinsip:**
    ```
    Cabang dibengkokkan ke tanah → Kubur sebagian
    → Akar tumbuh → Potong dari induk → Tanaman baru
    ```
    
    ### **Jenis:**
    
    **1. Simple Layering:**
    ```
    Protokol:
    1. Pilih cabang fleksibel (dekat tanah)
    2. Bengkokkan ke tanah
    3. Luka bagian bawah (sayat/kelupas sedikit)
    4. Kubur 5-10 cm
    5. Timbun tanah, beri pemberat
    6. Ujung cabang tetap di atas tanah
    7. Akar tumbuh 2-6 bulan
    8. Potong dari induk, pindahkan
    
    Cocok untuk: Anggur, Melati, Mawar
    ```
    
    **2. Air Layering (Cangkok):**
    ```
    Sudah dijelaskan di atas
    ```
    
    **3. Mound Layering:**
    ```
    - Timbun pangkal tanaman dengan tanah
    - Banyak cabang berakar
    - Cocok untuk: Apel, Gooseberry
    ```
    
    ---
    
    ## 🌱 PEMISAHAN (Division)
    
    ### **Prinsip:**
    ```
    Pisahkan anakan/rumpun dari induk
    → Tanam terpisah → Tanaman baru
    ```
    
    ### **Jenis:**
    
    **1. Pemisahan Anakan:**
    ```
    Cocok untuk:
    - Pisang (bonggol)
    - Nanas (crown, sucker)
    - Strawberry (runner)
    - Bambu (rumpun)
    
    Protokol:
    1. Pilih anakan sehat (1/3-1/2 ukuran induk)
    2. Gali hati-hati
    3. Potong dari induk (pisau tajam)
    4. Tanam di lahan baru
    5. Siram rutin
    
    Keberhasilan: 90-95%
    ```
    
    **2. Pemisahan Umbi:**
    ```
    Cocok untuk:
    - Kentang (umbi batang)
    - Ubi jalar (umbi akar)
    - Bawang (umbi lapis)
    - Jahe (rimpang)
    
    Protokol:
    1. Pilih umbi sehat, ada mata tunas
    2. Potong (1 umbi jadi 2-4 bagian)
    3. Setiap bagian minimal 1 mata tunas
    4. Keringkan luka (1-2 hari)
    5. Tanam
    
    Keberhasilan: 85-95%
    ```
    
    ---
    
    ## 🧬 KULTUR JARINGAN (Tissue Culture)
    
    ### **Prinsip:**
    ```
    Ambil jaringan kecil (eksplan) → Kultur in vitro
    → Regenerasi → Ribuan tanaman identik
    ```
    
    ### **Tahapan:**
    
    ```
    1. INISIASI:
       - Ambil eksplan (pucuk, mata tunas, daun)
       - Sterilisasi (alkohol, klorox)
       - Kultur di media MS + hormon
    
    2. MULTIPLIKASI:
       - Tunas berkembang
       - Sub-kultur (pindah media baru)
       - Tunas berlipat ganda
       - Ulangi 3-5x → Ribuan tunas
    
    3. PERAKARAN:
       - Pindah ke media perakaran
       - Hormon auxin (IBA, NAA)
       - Akar tumbuh
    
    4. AKLIMATISASI:
       - Pindah ke pot (ex vitro)
       - Naungi, jaga kelembaban
       - Adaptasi bertahap
       - Siap tanam
    
    Waktu: 3-6 bulan (dari eksplan ke tanaman)
    ```
    
    **Keuntungan:**
    ```
    ✅ Jumlah sangat banyak (ribuan dari 1 eksplan)
    ✅ Cepat
    ✅ Bebas penyakit
    ✅ Seragam (klonal)
    ✅ Bisa sepanjang tahun (tidak tergantung musim)
    ```
    
    **Kekurangan:**
    ```
    ❌ Investasi tinggi (lab steril)
    ❌ Skill tinggi
    ❌ Biaya per tanaman tinggi (untuk skala kecil)
    ```
    
    **Aplikasi:**
    ```
    - Tanaman hias: Anggrek, Anthurium
    - Buah: Pisang, Strawberry, Nanas
    - Kehutanan: Jati, Mahoni
    - Konservasi: Tanaman langka
    ```
    
    ---
    
    ## 📊 PERBANDINGAN METODE
    
    | Metode | Waktu | Keberhasilan | Jumlah | Biaya | Skill | Cocok untuk |
    |--------|-------|--------------|--------|-------|-------|-------------|
    | **Biji** | 3-10 tahun | 80-95% | Banyak | Murah | Mudah | Semusim, breeding |
    | **Stek** | 2-4 minggu | 70-90% | Sedang | Murah | Mudah | Hias, sayuran |
    | **Cangkok** | 1-3 bulan | 80-95% | Sedikit | Murah | Sedang | Buah, hias |
    | **Okulasi** | 3-4 minggu | 70-90% | Sedang | Murah | Tinggi | Buah, mawar |
    | **Sambung** | 2-4 minggu | 60-80% | Sedang | Murah | Tinggi | Buah besar |
    | **Merunduk** | 2-6 bulan | 80-90% | Sedikit | Murah | Mudah | Anggur, melati |
    | **Pemisahan** | Langsung | 90-95% | Sedang | Murah | Mudah | Pisang, nanas |
    | **Kultur Jaringan** | 3-6 bulan | 85-95% | Sangat banyak | Mahal | Sangat tinggi | Anggrek, pisang |
    
    ---
    
    ## 💡 TIPS PEMILIHAN METODE
    
    **Pilih BIJI jika:**
    ```
    ✅ Tanaman self-pollinated (padi, kedelai)
    ✅ Breeding program (butuh variasi)
    ✅ Skala besar, murah
    ✅ Tidak terburu-buru
    ```
    
    **Pilih STEK jika:**
    ```
    ✅ Tanaman mudah berakar (kangkung, singkong)
    ✅ Butuh banyak, cepat
    ✅ Murah, mudah
    ```
    
    **Pilih CANGKOK jika:**
    ```
    ✅ Tanaman sulit stek (mangga, jambu)
    ✅ Ingin tanaman besar langsung
    ✅ Cepat berbuah (1-2 tahun)
    ✅ Keberhasilan tinggi penting
    ```
    
    **Pilih OKULASI/SAMBUNG jika:**
    ```
    ✅ Ingin gabungkan sifat (akar kuat + buah unggul)
    ✅ Buah berkualitas (jeruk, mangga)
    ✅ Cepat berbuah
    ✅ Punya skill
    ```
    
    **Pilih KULTUR JARINGAN jika:**
    ```
    ✅ Butuh jumlah sangat banyak (ribuan)
    ✅ Bebas penyakit penting (pisang, anggrek)
    ✅ Tanaman langka/sulit perbanyak
    ✅ Punya akses lab/modal
    ```
    
    ---
    
    ## 📚 REFERENSI
    
    1. **Hartmann, H. T., et al. (2011).** Hartmann & Kester's Plant Propagation: Principles and Practices, 8th Edition. Prentice Hall.
    
    2. **Dirr, M. A., & Heuser, C. W. (2006).** The Reference Manual of Woody Plant Propagation. Timber Press.
    
    3. **George, E. F., et al. (2008).** Plant Propagation by Tissue Culture, 3rd Edition. Springer.
    
    """)

# ===== TAB 6: TOOLS & DATABASE =====
with tab_tools:
    st.header("🛠️ Tools & Database Varietas")
    
    st.markdown("""
    ### Fitur yang Tersedia:
    - 🔍 Variety Comparison Tool
    - 📊 Breeding Program Planner
    - 🧬 Genetic Traits Database
    - 📈 Yield Prediction Calculator
    
    ---
    """)
    
    # VARIETY COMPARISON TOOL
    st.subheader("🔍 Variety Comparison Tool")
    
    # Sample variety database
    variety_db = {
        'Padi': {
            'IR64': {'Umur': 120, 'Hasil': 5.5, 'Blast': 'T', 'BLB': 'R', 'Kualitas': 60, 'Harga': 'Sedang'},
            'Ciherang': {'Umur': 120, 'Hasil': 6.5, 'Blast': 'T', 'BLB': 'T', 'Kualitas': 65, 'Harga': 'Sedang'},
            'Inpari 32': {'Umur': 118, 'Hasil': 7.5, 'Blast': 'T', 'BLB': 'T', 'Kualitas': 70, 'Harga': 'Tinggi'},
            'Situ Bagendit': {'Umur': 130, 'Hasil': 6.5, 'Blast': 'T', 'BLB': 'T', 'Kualitas': 65, 'Harga': 'Sedang'},
            'Pandan Wangi': {'Umur': 145, 'Hasil': 4.5, 'Blast': 'R', 'BLB': 'R', 'Kualitas': 90, 'Harga': 'Premium'},
        },
        'Jagung': {
            'Bisi 18': {'Umur': 98, 'Hasil': 11, 'DM': 'T', 'Borer': 'T', 'Tipe': 'Hybrid', 'Harga': 'Mahal'},
            'Pioneer 21': {'Umur': 103, 'Hasil': 12, 'DM': 'T', 'Borer': 'T', 'Tipe': 'Hybrid', 'Harga': 'Mahal'},
            'NK 212': {'Umur': 98, 'Hasil': 10.5, 'DM': 'T', 'Borer': 'AT', 'Tipe': 'Hybrid', 'Harga': 'Mahal'},
            'Bisma': {'Umur': 98, 'Hasil': 6.5, 'DM': 'AT', 'Borer': 'R', 'Tipe': 'OP', 'Harga': 'Murah'},
        },
        'Kedelai': {
            'Anjasmoro': {'Umur': 87, 'Hasil': 2.3, 'Karat': 'T', 'Ukuran': 'Besar', 'Tipe': 'OP'},
            'Grobogan': {'Umur': 76, 'Hasil': 3.4, 'Karat': 'AT', 'Ukuran': 'Sangat Besar', 'Tipe': 'OP'},
            'Dena 1': {'Umur': 78, 'Hasil': 2.9, 'Karat': 'T', 'Ukuran': 'Sedang', 'Tipe': 'OP (Tahan Naungan)'}
        },
        'Cabai Merah': {
            'Lado F1': {'Umur': 115, 'Hasil': 18, 'Layu': 'T', 'Pedas': 'Sedang', 'Tipe': 'Hybrid'},
            'PM 99': {'Umur': 105, 'Hasil': 25, 'Layu': 'T', 'Pedas': 'Pedas', 'Tipe': 'Hybrid'},
            'Laba': {'Umur': 95, 'Hasil': 16, 'Layu': 'AT', 'Pedas': 'Sangat Pedas', 'Tipe': 'OP'}
        },
        'Bawang Merah': {
            'Bima Brebes': {'Umur': 60, 'Hasil': 10, 'Hujan': 'R', 'Warna': 'Merah Tua', 'Tipe': 'Lokal'},
            'Bauji': {'Umur': 58, 'Hasil': 12, 'Hujan': 'T', 'Warna': 'Merah Pucat', 'Tipe': 'Lokal'},
            'Pikatan': {'Umur': 55, 'Hasil': 11, 'Hujan': 'AT', 'Warna': 'Merah', 'Tipe': 'Lokal'}
        }
    }
    
    col1, col2 = st.columns(2)
    
    with col1:
        crop_type = st.selectbox("Pilih Komoditas:", list(variety_db.keys()))
    
    with col2:
        varieties = list(variety_db[crop_type].keys())
        selected_vars = st.multiselect(
            "Pilih Varietas untuk Dibandingkan (max 4):",
            varieties,
            default=varieties[:3] if len(varieties) >= 3 else varieties
        )
    
    if selected_vars:
        # Create comparison dataframe
        comparison_data = []
        for var in selected_vars:
            data = variety_db[crop_type][var].copy()
            data['Varietas'] = var
            comparison_data.append(data)
        
        df_comparison = pd.DataFrame(comparison_data)
        # Reorder columns
        cols = ['Varietas'] + [c for c in df_comparison.columns if c != 'Varietas']
        df_comparison = df_comparison[cols]
        
        st.dataframe(df_comparison, use_container_width=True)
        
        # Visualization
        fig = go.Figure()
        
        # Generic Yield Bar (Almost all have 'Hasil')
        if 'Hasil' in variety_db[crop_type][selected_vars[0]]:
            fig.add_trace(go.Bar(
                name=f'Hasil (ton/ha)',
                x=selected_vars,
                y=[variety_db[crop_type][v]['Hasil'] for v in selected_vars],
                marker_color='#3b82f6'
            ))
            
        # Generic Duration Bar (Almost all have 'Umur')
        if 'Umur' in variety_db[crop_type][selected_vars[0]]:
            # Scale Factor for visualization if needed (e.g. days vs ton)
            # For Padi/Jagung (100 days vs 6 tons), scaling by 10 makes sense visually
            # For Chili (100 days vs 20 tons), scaling by 5 is better
            scale = 10
            if crop_type in ['Cabai Merah', 'Bawang Merah']: scale = 5
            
            fig.add_trace(go.Bar(
                name=f'Umur (hari/{scale})',
                x=selected_vars,
                y=[variety_db[crop_type][v]['Umur']/scale for v in selected_vars],
                marker_color='#10b981'
            ))
            
        fig.update_layout(
            title=f'Perbandingan Varietas {crop_type}',
            xaxis_title='Varietas',
            yaxis_title='Nilai Relatif',
            barmode='group',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # BREEDING PROGRAM PLANNER
    st.subheader("📊 Breeding Program Planner")
    
    st.markdown("""
    **Estimasi Waktu & Biaya Program Pemuliaan**
    
    Gunakan tool ini untuk merencanakan program pemuliaan Anda.
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        breeding_method = st.selectbox(
            "Metode Pemuliaan:",
            ['Hibridisasi (Pedigree)', 'Backcross', 'Mutasi', 'Hybrid Production']
        )
        
        crop_breeding = st.selectbox(
            "Tanaman:",
            ['Padi', 'Jagung', 'Kedelai', 'Tomat']
        )
    
    with col2:
        num_crosses = st.number_input("Jumlah Persilangan:", min_value=1, max_value=100, value=10)
        num_generations = st.number_input("Jumlah Generasi:", min_value=1, max_value=10, value=6)
    
    # Calculate estimates
    if breeding_method == 'Hibridisasi (Pedigree)':
        years = num_generations + 2  # +2 for testing
        cost_per_cross = 5000000  # Rp 5 juta per cross
        total_cost = num_crosses * cost_per_cross * num_generations * 0.5
    elif breeding_method == 'Backcross':
        years = num_generations + 1
        cost_per_cross = 3000000
        total_cost = num_crosses * cost_per_cross * num_generations * 0.3
    elif breeding_method == 'Mutasi':
        years = 5 + num_generations
        cost_per_cross = 10000000  # Irradiation cost
        total_cost = num_crosses * cost_per_cross
    else:  # Hybrid Production
        years = 8 + 2  # Inbred development + testing
        cost_per_cross = 20000000
        total_cost = num_crosses * cost_per_cross * 2
    
    st.success(f"""
    **Estimasi Program Pemuliaan:**
    
    - **Waktu:** {years} tahun
    - **Biaya Total:** Rp {total_cost:,.0f}
    - **Biaya per Tahun:** Rp {total_cost/years:,.0f}
    - **Jumlah Galur Akhir:** {int(num_crosses * 0.1)} galur (10% seleksi)
    """)
    
    st.markdown("---")
    
    # GENETIC TRAITS DATABASE
    st.subheader("🧬 Genetic Traits Database")
    
    st.markdown("""
    **Database Sifat Genetik Penting**
    
    Informasi tentang sifat-sifat genetik yang umum digunakan dalam pemuliaan.
    """)
    
    traits_db = {
        'Tinggi Tanaman': {
            'Heritabilitas': 'Tinggi (0.7-0.9)',
            'Tipe': 'Kuantitatif',
            'Gen Utama': 'sd1 (semi-dwarf)',
            'Aplikasi': 'Tahan rebah, efisiensi pupuk'
        },
        'Umur Tanaman': {
            'Heritabilitas': 'Tinggi (0.6-0.8)',
            'Tipe': 'Kuantitatif',
            'Gen Utama': 'Hd1, Hd3 (heading date)',
            'Aplikasi': 'Adaptasi musim, cropping pattern'
        },
        'Hasil Panen': {
            'Heritabilitas': 'Sedang (0.3-0.5)',
            'Tipe': 'Kuantitatif kompleks',
            'Gen Utama': 'Multiple QTLs',
            'Aplikasi': 'Produktivitas'
        },
        'Resistensi Blast': {
            'Heritabilitas': 'Tinggi (0.7-0.9)',
            'Tipe': 'Kualitatif/Kuantitatif',
            'Gen Utama': 'Pi genes (Pi1, Pi2, Pi9, dll)',
            'Aplikasi': 'Ketahanan penyakit'
        },
        'Kualitas Beras (Amilosa)': {
            'Heritabilitas': 'Tinggi (0.8-0.9)',
            'Tipe': 'Kuantitatif',
            'Gen Utama': 'Wx gene',
            'Aplikasi': 'Tekstur nasi (pulen/pera)'
        },
        'Toleransi Kekeringan': {
            'Heritabilitas': 'Rendah-Sedang (0.2-0.4)',
            'Tipe': 'Kuantitatif kompleks',
            'Gen Utama': 'Multiple QTLs',
            'Aplikasi': 'Adaptasi lahan kering'
        }
    }
    
    trait_selected = st.selectbox("Pilih Sifat Genetik:", list(traits_db.keys()))
    
    if trait_selected:
        trait_info = traits_db[trait_selected]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Heritabilitas", trait_info['Heritabilitas'])
            st.metric("Tipe Pewarisan", trait_info['Tipe'])
        
        with col2:
            st.info(f"**Gen Utama:** {trait_info['Gen Utama']}")
            st.success(f"**Aplikasi:** {trait_info['Aplikasi']}")
    
    st.markdown("---")
    
    # YIELD PREDICTION
    st.subheader("📈 Yield Prediction Calculator")
    
    st.markdown("""
    **Prediksi Hasil Berdasarkan Heritabilitas**
    
    Tool sederhana untuk memprediksi response to selection.
    """)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        parent_mean = st.number_input("Rata-rata Populasi (ton/ha):", min_value=1.0, max_value=20.0, value=5.0, step=0.5)
        selected_mean = st.number_input("Rata-rata Terseleksi (ton/ha):", min_value=1.0, max_value=20.0, value=7.0, step=0.5)
    
    with col2:
        heritability = st.slider("Heritabilitas (h²):", min_value=0.0, max_value=1.0, value=0.5, step=0.1)
    
    with col3:
        selection_differential = selected_mean - parent_mean
        response = heritability * selection_differential
        predicted_mean = parent_mean + response
        
        st.metric("Selection Differential (S)", f"{selection_differential:.2f} ton/ha")
        st.metric("Response to Selection (R)", f"{response:.2f} ton/ha")
        st.metric("Prediksi Generasi Berikutnya", f"{predicted_mean:.2f} ton/ha", delta=f"+{response:.2f}")
    
    st.info(f"""
    **Formula:** R = h² × S
    
    - **R** = Response to selection (gain per generasi)
    - **h²** = Heritabilitas ({heritability})
    - **S** = Selection differential ({selection_differential:.2f})
    
    **Interpretasi:** Dengan heritabilitas {heritability} dan seleksi {selection_differential:.2f} ton/ha,
    diharapkan peningkatan hasil sebesar {response:.2f} ton/ha pada generasi berikutnya.
    """)
    
    st.markdown("---")
    
    st.markdown("""
    ## 📚 SUMBER DATA
    
    Database varietas ini dikompilasi dari:
    - Katalog Varietas Unggul Kementerian Pertanian RI
    - IRRI Rice Knowledge Bank
    - CIMMYT Maize Varieties Database
    - Publikasi ilmiah peer-reviewed
    
    **Disclaimer:** Data bersifat indikatif. Performa aktual dapat bervariasi tergantung kondisi lingkungan dan manajemen.
    """)
