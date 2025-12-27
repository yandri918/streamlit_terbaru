import streamlit as st

# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Pembuatan Pupuk Organik - AgriSensa",
    page_icon="🧴",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






st.title("🧴 Laboratorium Pupuk Organik")
st.markdown("**pusat Panduan Pembuatan Pupuk, Bioaktivator, dan Ramuan Organik Tanaman**")

# Tabs
tab_bio, tab_poc, tab_padat, tab_mol, tab_herb, tab_zpt, tab_sawit, tab_kalkulator = st.tabs([
    "🧪 Bioaktivator & Decomposer",
    "💧 Pupuk Cair (POC)",
    "🍂 Pupuk Padat (Kompos)",
    "🦠 MOL (Mikro Organisme Lokal)",
    "🌿 Herbisida Alami",
    "🚀 ZPT Alami",
    "🌴 Spesial Sawit",
    "🧮 Kalkulator Organik"
])

# ===== TAB 1: BIOAKTIVATOR =====
with tab_bio:
    st.subheader("🧪 Bioaktivator & Decomposer")
    st.info("Bioaktivator berfungsi mempercepat proses pengomposan dan meningkatkan kesuburan tanah dengan mikroorganisme menguntungkan.")
    
    with st.expander("🐮 ROTAN (Ramuan Organik Tanaman) - Cairan Rumen Sapi", expanded=True):
        st.markdown("""
        **Bioaktivator Super (Probiotik Sempurna)** yang kaya akan mikroorganisme selulolitik dan penambat N. Sangat efektif untuk decomposer maupun pupuk dasar.
        """)
        
        col_bahan, col_cara = st.columns([1, 1.2])
        
        with col_bahan:
            st.markdown("#### 🥦 Bahan-Bahan")
            st.warning("**Bahan Utama:**")
            st.markdown("""
            1.  **Cairan Rumen Sapi** (Isi usus halus/perasan isi usus besar) = **2 Liter**
            2.  **Molase** (Tetes Tebu/Air Gula/Air Tebu) = **2 Liter**
            3.  **Air Rebusan Dedak/Katul** = **4 Liter**
            """)
            
            st.success("**Bahan Tambahan:**")
            st.markdown("""
            1.  **Ragi Tape** = 2-3 butir
            2.  **Terasi** = ½ - 1 ons
            3.  **Buah Nanas** = 1 buah
            4.  **Urine Ternak** (Sapi/Kambing/kelinci) yg sudah diendapkan 1 minggu = **4 Liter**
            """)
            
        with col_cara:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1.  **Siapkan Air Dedak:** Campur 1 kg dedak dengan 5 liter air. Rebus hingga mendidih, dinginkan, lalu saring. Ambil airnya sebanyak **4 liter**.
            2.  **Campur Utama:** Masukkan **2 liter Cairan Rumen** dan **2 liter Molase** ke dalam wadah. Aduk rata.
            3.  **Campur Dedak:** Masukkan air rebusan dedak (4 liter) ke dalam campuran rumen dan molase tadi.
            4.  **Haluskan Tambahan:** Parut/blender **1 buah nanas** dan encerkan **Terasi** dengan sedikit air. Masukkan ke dalam wadah.
            5.  **Ragi:** Hancurkan **2-3 butir ragi tape**, masukkan.
            6.  **Urine:** Tambahkan **4 liter Urine ternak**.
            7.  **Fermentasi:** Masukkan semua larutan ke dalam jerigen/tong plastik. Tutup rapat (anaerob).
            8.  **Waktu:** Simpan selama **2 Minggu**.
            9.  **Finishing:** Jika sudah jadi, bioaktivator ini siap digunakan atau dicampur dengan ROTAN lain.
            """)
            
        st.markdown("---")
        
        c1, c2 = st.columns(2)
        with c1:
            st.success("✅ **Ciri-Ciri Berhasil:**")
            st.markdown("""
            *   Berbau khas fermentasi (harum/asam segar).
            *   Berwarna kuning kecoklatan.
            *   Tidak keruh.
            *   Tidak ada jamur hitam/abu-abu (jamur putih/krem boleh).
            """)
            
        with c2:
            st.error("❌ **Ciri-Ciri Gagal:**")
            st.markdown("""
            *   Berbau busuk (seperti got/bangkai).
            *   Berwarna coklat kehitaman/keruh.
            *   Terdapat banyak jamur berwarna coklat/hitam/abu-abu.
            """)
            
        with st.chat_message("assistant"):
            st.markdown("""
            **🧬 Kandungan Mikroba Super:**
            *   **Selulolitik (Pengurai Serat):** *Bacteriodes succinogenes, Cillobacterium cellulosolvens, Lactobacillus sp.*
            *   **Hemiselulolitik:** *Butyrivibrio fibriosolven, Bacteriodes ruminicola*
            *   **Amilolitik:** *Bacteriodes amylophilus, Streptococcus bovis*
            *   **Penambat N (Penyubur N):** *Azotobacter, Azospirillum, Nitrosococcus, Nitrosomonas*
            *   **Pelarut P (Phosphate):** *Aspergillus niger, Bacillus subtilis, Bacillus polymixa, Bacillus megatherium*
            *   **ZPT (Hormon Tumbuh):** *Acetobacter sp, Actinomycetes sp*
            *   **Pembenah Tanah:** *Bacillus mojavensis* (meningkatkan kemampuan memegang air).
            
            *InsyaAllah menjadi Probiotik "SEMPURNA" untuk POC, POP, dan Decomposer.*
            """)
            
    st.markdown("---")
    
    with st.expander("🍄 Trichoderma sp. (Jamur Keberuntungan)", expanded=False):
        st.info("Cara memancing dan memperbanyak jamur Trichoderma sp. dari alam (Hutan Bambu). Trichoderma adalah fungisida alami yang ampuh.")
        
        col_t1, col_t2 = st.columns(2)
        
        with col_t1:
            st.markdown("#### 🍚 Bahan-Bahan")
            st.markdown("""
            1.  **Nasi Basi:** 1 Mangkuk (Minimal sudah 1 hari 1 malam).
            2.  **Bambu:** 3 Ruas (Baru ditebang lebih bagus).
            3.  **Pengikat:** Tali atau Karet ban.
            """)
            
        with col_t2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1.  **Siapkan Bambu:** Potong bambu 3 ruas. Belah dua. Gunakan bagian ruas tengah saja (beri jarak 10cm dari batas ruas kiri-kanan).
            2.  **Lubangi:** Buat lubang seukuran kelingking di batas ruas kiri dan kanan.
            3.  **Cuci Bersih:** Cuci ruas bambu dengan **Air Mengalir** (Sungai/Kran air sumur). **JANGAN** pakai Air PDAM (Kaporit mematikan jamur).
            4.  **Isi Nasi:** Masukkan nasi basi ke dalam belahan ruas bagian tengah.
            5.  **Tutup:** Satukan kembali belahan bambu, ikat erat dengan tali/karet.
            """)
            
        st.markdown("#### 🚜 Cara Pemeraman (Inkubasi)")
        st.markdown("""
        1.  **Lokasi:** Cari hutan bambu atau dapuran pohon bambu yang tanahnya subur/berhumus.
        2.  **Kubur:** Tanam bambu berisi nasi tadi sedalam **7-10 cm**.
        3.  **Tandai:** Beri tanda agar tidak lupa lokasi penguburan.
        4.  **Biarkan:** Tunggu selama **7-10 Hari**.
        5.  **Panen:** Buka bambu. Jika terdapat **Jamur Putih seperti Kapas** (Trichoderma sp.), selamat Anda berhasil!
        """)
        st.success("✅ **Hasil:** Nasi yang ditumbuhi jamur putih ini adalah biang Trichoderma yang siap diperbanyak.")

# ===== TAB 2: POC =====
with tab_poc:
    st.header("💧 Pupuk Organik Cair (POC)")
    st.markdown("Kumpulan resep POC kualitas tinggi (Premium)")
    
    with st.expander("🥣 POC ROTAN (Premium Quality)", expanded=True):
        st.info("POC ini memiliki kandungan mikroba lengkap: *Azotobacter sp., Azospirillium sp., Pseudomonas sp., Lactobacillus sp., Rhizobium sp., dan Streptomyces sp.*")
        
        tab_buat, tab_banyak, tab_upgrade, tab_dosis = st.tabs(["🥣 Cara Buat", "📈 Cara Memperbanyak", "🚀 Upgrade ZPT", "💉 Dosis Aplikasi"])
        
        with tab_buat:
            col_b, col_c = st.columns([1, 1.2])
            
            with col_b:
                st.markdown("#### 🥦 Bahan-Bahan")
                st.markdown("""
                1.  **Buah Pisang:** 5 buah
                2.  **Buah Pepaya:** 1 buah
                3.  **Buah Nanas:** 1 buah
                4.  **Buah Mangga:** 2 buah
                5.  **Buah Melon/Semangka:** 1 buah
                6.  **Kangkung Air:** 3 ikat
                7.  **Kacang Panjang:** 3 ikat
                8.  **Jagung Muda:** 2 buah
                9.  **Ragi:** 3 butir
                10. **Air Kelapa:** 5 Liter
                11. **Air Leri (Cucian Beras):** 3 Liter
                12. **Gula Kelapa:** 1 kg
                13. **Usus Ikan:** 2 ons
                """)
                
            with col_c:
                st.markdown("#### 🥣 Cara Pembuatan")
                st.markdown("""
                1.  **Blender Halus:** Blender bahan no 1 sampai 8 (Buah-buahan, sayuran, jagung) sampai seperti jus.
                2.  **Rebus Gula:** Didihkan gula kelapa dengan 1 liter air, biarkan sampai **benar-benar dingin**.
                3.  **Pencampuran:** Campurkan semua bahan (Jus, Gula cair dingin, Air kelapa, Air leri, Usus ikan, Ragi) menjadi satu. Aduk sampai benar-benar merata.
                4.  **Wadah:** Simpan dalam wadah **Tembikar** atau **Plastik**.
                5.  **PENTING:** Jangan gunakan wadah LOGAM.
                6.  **Fermentasi:** Tutup rapat, fermentasi selama **10-14 Hari**.
                7.  **Perawatan:** Setiap **2 hari sekali**, buka tutup dan aduk selama 5 menit, lalu tutup kembali rapat-rapat.
                """)
                
            st.markdown("---")
            c1, c2 = st.columns(2)
            with c1:
                st.success("✅ **Ciri-Ciri Berhasil:**")
                st.markdown("* Campuran berbau **Asam** dan **Harum Tape**.")
                st.markdown("* Fermentasi selesai jika **sudah tidak ada gas**.")
            with c2:
                st.warning("⚠️ **Tips:**")
                st.markdown("* Saring hasil fermentasi.")
                st.markdown("* **Ampas jangan dibuang!** Masih mengandung semua mikroba super di atas.")

        with tab_banyak:
            st.subheader("📈 Cara Memperbanyak (Perbanyakan Masal)")
            st.markdown("Anda bisa membuat 100 Liter POC ROTAN dengan kualitas SAMA dari 1 Liter biang POC ROTAN.")
            
            st.markdown("#### Bahan:")
            st.markdown("""
            1.  **Air Jernih** (Sumur/Mata air): 100 Liter
            2.  **Dedak:** 10 kg
            3.  **Gula Kelapa:** 5 kg
            4.  **Air Kelapa:** 10 liter
            5.  **Biang POC ROTAN:** 1 Liter
            """)
            
            st.markdown("#### Cara Buat:")
            st.markdown("""
            1.  Panaskan/Rebus bahan **Air Jernih (sebagian), Dedak, dan Gula Kelapa**.
            2.  Setelah larut dan matang, biarkan sampai **Benar-benar Dingin**.
            3.  Campurkan dengan sisa Air Jernih, Air Kelapa, dan **1 Liter POC ROTAN**.
            4.  Masukkan ke dalam drum plastik, tutup rapat (anaerob).
            5.  Diamkan selama **7 Hari**.
            6.  **Selesai!** Anda punya 100 Liter POC ROTAN kualitas super.
            """)
            
        with tab_upgrade:
            st.subheader("🚀 Upgrade Kualitas Nomor Wahid (Plus ZPT)")
            st.markdown("Tambahkan ZPT (Zat Pengatur Tumbuh) ke dalam **100 Liter** POC ROTAN tadi sesuai fase tanaman.")
            
            col_veg, col_gen = st.columns(2)
            
            with col_veg:
                st.success("🌱 **Fase Vegetatif (Pertumbuhan)**")
                st.markdown("""
                Tambahkan:
                *   **ZPT Auxin:** 1 Liter
                *   **ZPT Sitokinin:** 1 Liter
                """)
                
            with col_gen:
                st.warning("🌺 **Fase Generatif (Pembuahan)**")
                st.markdown("""
                Tambahkan:
                *   **ZPT Sitokinin:** ½ Liter
                *   **ZPT Giberelin:** 1.5 Liter
                """)
                
        with tab_dosis:
            st.subheader("💉 Dosis Aplikasi")
            
            col_d1, col_d2 = st.columns(2)
            
            with col_d1:
                st.info("🌾 **Tanaman Padi**")
                st.markdown("""
                *   **Dosis:** 250 ml per 14 Liter air (per tangki).
                *   **Interval:** 1 Minggu sekali.
                """)
                
            with col_d2:
                st.info("🌽 **Palawija / Sayuran**")
                st.markdown("""
                *   **Dosis:** 100 ml per 14 Liter air.
                *   **Interval:** 1 Minggu sekali.
                """)
                
    st.markdown("---")
    
    with st.expander("🐐 POC Rumen Kambing (By Ayah Manjel)", expanded=False):
        st.info("Resep alternatif memanfaatkan limbah rumen/usus kambing. Proses cepat (3-7 hari).")
        
        col_pk1, col_pk2 = st.columns(2)
        
        with col_pk1:
            st.markdown("#### 🥬 Bahan-Bahan")
            st.markdown("""
            1.  **Air Bersih:** 5 Liter
            2.  **Gula Kelapa:** 1 kg
            3.  **Kecambah (Tauge):** 1 kg
            4.  **Dedak:** 2 kg
            5.  **Susu Murni:** 1 Liter
            6.  **Rumen/Usus Kambing:** Bagian usus dekat perut besar (kira-kira 12 jari)
            """)
            
        with col_pk2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1.  **Sterilisasi:** Cuci wadah (ember/jerigen) dengan air panas.
            2.  **Larutan Gula & Dedak:** Seduh Gula dan Dedak dengan **Air Panas**, aduk rata, saring, dan masukkan airnya ke jerigen.
            3.  **Larutan Susu:** Haluskan/blender Kecambah, campur dengan Susu Murni, saring, dan masukkan ke jerigen.
            4.  **Rumen:** Cincang Rumen/Usus sampai halus, masukkan ke jerigen.
            5.  **Fermentasi:** Tutup rapat (anaerob).
            6.  **Perawatan:** Aduk setiap **Pagi & Sore** (buka sebentar).
            7.  **Waktu:** Cek hari ke-3. Jika harum = JADI. Biarkan maksimal **7 Hari** untuk pematangan.
            """)
            
        st.success("💉 **Dosis Aplikasi:** 250 cc per 14 Liter Air (1 Tangki).")

        st.caption("Aplikasi Pagi (06.00-09.00) atau Sore (15.00-17.00).")

    st.markdown("---")
    
    # === POC 3: EMPON-EMPON (IMUN BOOSTER) ===
    with st.expander("🛡️ POC Empon-Empon Plus (Imun Booster & Bio-Pestisida)", expanded=False):
        st.markdown("""
        **Fungsi Ganda (2-in-1):** Selain sebagai pupuk (Nutrisi), ramuan ini berfungsi sebagai **"Vaksin Tanaman"** untuk meningkatkan kekebalan terhadap jamur dan bakteri.
        
        **🔬 Konsep Modern:**
        *   **Analgesik & Antibiotik Alami:** Kandungan Kurkumin & Minyak Atsiri dari empon-empon (Jahe, Kunyit, Temulawak) menghambat pertumbuhan patogen.
        *   **Pasteurisasi Media:** Teknik perebusan (elemen listrik) digunakan untuk mensterilkan media dari telur lalat/hama sebelum difermentasi dengan mikroba baik (EM4).
        """)
        
        col_emp1, col_emp2 = st.columns(2)
        
        with col_emp1:
            st.markdown("#### 🥦 Bahan-Bahan (Skala Besar)")
            st.warning("💡 **Tips:** Bahan banyak! Ajak 3 orang teman untuk patungan modal & tenaga.")
            st.markdown("""
            | Bahan | Jumlah (Kg) | Fungsi Utama |
            | :--- | :--- | :--- |
            | **Jahe** | 1 Kg | Hangat, Antijamur |
            | **Lengkuas** | 1 Kg | Antibakteri |
            | **Kunyit** | 1 Kg | Kurkumin (Imun) |
            | **Temulawak** | 1 Kg | Nafsu makan (Serap nutrisi) |
            | **Temu Ireng** | 1 Kg | Anti-helminth (Cacing) |
            | **Puyang** | 1 Kg | Pestisida Nabati |
            | **Kencur** | 1 Kg | Aroma Repellent |
            | **Batang Pisang** | 1 Kg | Kalium & Fosfor |
            | **Nanas** | 1 Kg | Enzim Bromelain (Dekomposer) |
            | **Tauge (Kecambah)** | 1 Kg | Hormon Auksin (Tumbuh) |
            | **Buah Maja** | 2-5 Buah | Hormon & Gula Alami |
            | **Ampas Jus Buah** | 10 Liter | Media Glukosa |
            | **Urine Sapi** | 125-150 L | Nitrogen (Vegetatif) |
            | **Decomposer** | EM4 / ROTAN | Bakteri Starter |
            """)
            
        with col_emp2:
            st.markdown("#### ⚙️ Cara Pembuatan Modern")
            st.markdown("""
            1.  **Penggilingan:** Giling halus semua bahan padat (1-10) di penggilingan tepung/bumbu.
            2.  **Pencampuran:** Masukkan semua bahan gilingan + ampas jus + urine sapi ke dalam drum besar.
            3.  **Pasteurisasi (PENTING):**
                *   Didihkan campuran menggunakan **Elemen Pemanas Listrik** (Immersion Heater).
                *   *Tujuan:* Membunuh telur lalat/larva jahat agar tidak jadi belatung liar.
            4.  **Pendinginan:** Tutup rapat dan biarkan dingin alami (Suhu ruang).
            5.  **Inokulasi:** Setelah dingin, masukkan **Decomposer (EM4/ROTAN)**. Aduk rata.
            6.  **Fermentasi Anaerob:** Tutup drum rapat-rapat (udara tidak boleh masuk).
            7.  **Indikator Panen:**
                *   Tunggu sampai bau **"Pesing"** (Amonia) hilang.
                *   Berubah menjadi bau **"Jamu Segar/Tape"**.
            """)
            
        st.info("""
        **🧬 Dosis & Aplikasi:**
        *   **Fase Vegetatif (0 - 30 HST):** 1 Minggu sekali.
        *   **Fase Generatif (50 HST - Pengisian Bulir):** 1 Minggu sekali.
        *   **Cara:** Semprot kabut pada daun (Pagi/Sore).
        """)

    st.markdown("---")

    # === POC 4: URINE KELINCI (LIQUID GOLD) ===
    with st.expander("🐇 POC Urine Kelinci (Liquid Gold)", expanded=False):
        st.markdown("""
        **Kenapa Urine Kelinci?**
        Urine kelinci memiliki kandungan **N (Nitrogen) tertinggi** dibandingkan ternak lain (Sapi/Kambing). Dijuluki *"Liquid Gold"* karena efeknya yang instan menghijaukan daun.
        """)
        
        col_uk1, col_uk2 = st.columns(2)
        
        with col_uk1:
            st.markdown("#### 🧪 Bahan-Bahan")
            st.markdown("""
            1.  **Urine Kelinci Murni:** 10 Liter
            2.  **Starter (EM4/MOL):** 2 Tutup Botol / 200 ml
            3.  **Molase/Gula Merah:** 200 ml (Makanan Bakteri)
            4.  **Air Kelapa (Opsional):** 1 Liter (Untuk ZPT tambahan)
            5.  **Rempah (Opsional):** Jahe/Lengkuas (Untuk pestisida nabati)
            """)
            
        with col_uk2:
            st.markdown("#### ⚙️ Cara Fermentasi")
            st.markdown("""
            1.  Masukkan Urine Kelinci ke dalam jerigen.
            2.  Larutkan Gula + Starter, lalu masukkan ke jerigen.
            3.  Tutup rapat (Anaerob).
            4.  **Gas:** Buka tutup setiap pagi untuk buang gas.
            5.  **Panen:** Siap pakai setelah **7-14 Hari**.
            6.  *Ciri:* Bau menyengat hilang, wangi fermentasi.
            """)
            
        st.success("💉 **Dosis:** 1 Bagian Urine : 10 Bagian Air (Kocor) atau 1:20 (Semprot Daun).")

# ===== TAB 3: PADAT =====
with tab_padat:
    st.header("🍂 Pupuk Organik Padat (Kompos/Bokashi)")
    
    with st.expander("💩 Bokashi Padat ROTAN (1 Hektar)", expanded=True):
        st.info("Resep ini mencukupi kebutuhan 16 Unsur Hara Makro & Mikro untuk lahan 1 Hektar.")
        
        col_pb, col_pc = st.columns(2)
        
        with col_pb:
            st.markdown("#### 🧱 Bahan-Bahan")
            st.markdown("""
            1.  **Kohe Domba/Kambing:** 1 Ton
            2.  **Dolomit (Kapur Pertanian):** 100 kg
            3.  **Dedak/Katul:** 50 kg
            4.  **Sekam Padi:** 300 kg
            5.  **Jerami Padi:** 1 Ton
            6.  **Bioaktivator ROTAN:** 4 Liter
            7.  **Air Kelapa:** Secukupnya (untuk kelembaban)
            """)
            
        with col_pc:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1.  **Pencampuran:** Campur semua bahan padat (Kohe, Dolomit, Dedak, Sekam, Jerami (cacah)) hingga merata.
            2.  **Larutan:** Campurkan 4 Liter Bioaktivator ROTAN dengan Air Kelapa secukupnya.
            3.  **Penyiraman:** Siramkan larutan ke tumpukan bahan padat sambil diaduk.
            4.  **Kelembaban:** Pastikan kelembaban sekitar **30-40%** (Mamel: Bila digenggam menggumpal, bila disentuh hancur, tidak meneteskan air).
            5.  **Fermentasi:** Tutup tumpukan dengan terpal.
            6.  **Waktu:** Fermentasi selama **5 - 7 Hari**.
            7.  **Panen:** Pupuk siap digunakan jika suhu sudah turun/dingin dan berbau harum fermentasi.
            """)

    st.divider()

    # === KOMPOS SPESIFIK: AYAM, PUYUH, GUANO, SAPI ===
    with st.expander("🐔🦇🐄 Panduan Bokashi Spesifik (Ayam, Puyuh, Guano, Sapi)", expanded=False):
        st.info("Setiap kotoran ternak memiliki 'Karakter' unik. Sesuaikan resep untuk hasil maksimal.")
        
        tab_ayam, tab_puyuh, tab_guano, tab_sapi = st.tabs([
            "🐔 Ayam (Broiler/Petelur)", 
            "🐦 Burung Puyuh",
            "🦇 Guano (Kelelawar)",
            "🐄 Sapi/Kerbau"
        ])
        
        with tab_ayam:
            st.markdown("### 🐔 Bokashi Kotoran Ayam (Manure)")
            st.warning("**Karakter:** Panas tinggi, Amonia tinggi, C/N Ratio rendah (butuh banyak karbon).")
            col_a1, col_a2 = st.columns(2)
            with col_a1: 
                st.markdown("**Resep Khusus:**")
                st.markdown("""
                *   **Kohe Ayam:** 1 Ton
                *   **Sekam Mentah/Gergaji Kayu:** 500 Kg (Wajib Tinggi! Untuk serap amonia).
                *   **Dolomit:** 100 Kg (Netralkan asam).
                """)
            with col_a2:
                st.success("**Cocok Untuk:** Sayuran Daun (Bayam, Kangkung) karena **Nitrogen Tinggi**.")
                
        with tab_puyuh:
            st.markdown("### 🐦 Bokashi Kotoran Puyuh")
            st.warning("**Karakter:** Nutrisi sangat pekat (Lebih tinggi dari ayam), mudah 'membakar' tanaman jika belum matang.")
            st.markdown("""
            *   **Tips Fermentasi:** Wajib fermentasi minimal **21-30 Hari** (lebih lama dari sapi).
            *   **Campuran:** Perbanyak Dedak (Nutrisi Mikroba) agar penguraian sempurna.
            *   **Penggunaan:** Sangat irit! Gunakan separuh dosis pupuk kandang biasa.
            """)
            
        with tab_guano:
            st.markdown("### 🦇 Bokashi Guano (Kelelawar)")
            st.info("**Karakter:** Emas Hitam! Kaya **Fosfor (P)** dan Nitrogen.")
            st.markdown("""
            *   **Spesialis:** Pembuahan (Generatif).
            *   **Mix:** Sangat bagus dicampur dengan **Arang Sekam**.
            *   **Tanaman:** Durian, Kelengkeng, Cabai (Fase Bunga).
            """)
            
        with tab_sapi:
            st.markdown("### 🐄 Bokashi Sapi/Kerbau")
            st.success("**Karakter:** Pupuk Dingin, Serat Tinggi, Memperbaiki Struktur Tanah.")
            st.markdown("""
            *   **Fungsi Utama:** *Soil Conditioner* (Pembenah Tanah) untuk tanah keras/liat.
            *   **Fermentasi:** Lebih lambat karena serat kasar. Bakteri butuh waktu.
            *   **Rekomendasi:** Tambahkan **Trichoderma** saat proses pematangan untuk anti-jamur akar.
            """)

# ===== TAB 4: M O L =====
with tab_mol:
    st.header("🦠 MOL (Mikro Organisme Lokal)")
    st.info("Kumpulan resep MOL sederhana menggunakan bahan-bahan lokal.")
    
    mol_choice = st.selectbox("Pilih Jenis MOL:", [
        "MOL Sayuran",
        "MOL Buah",
        "MOL Rebung Bambu",
        "MOL Keong Mas / Bekicot",
        "MOL Bonggol Pisang",
        "MOL Sabut Kelapa",
        "MOL Gedebok / Pelepah Pisang"
    ])
    
    if mol_choice == "MOL Sayuran":
        with st.expander("🥦 MOL Sayuran (Vegetatif)", expanded=True):
            st.markdown("**Fungsi:** Pupuk masa Vegetatif.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Sayur-sayuran (beragam, jangan busuk): 3 kg
                *   Gula Merah: 0.5 kg
                *   Garam: 150 gram
                *   Air Leri (Beras): 3 Liter
                *   Air Kelapa: 2 Liter
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Cincang halus/blender sayuran.
                2.  Campur semua bahan, kocok/aduk 3-5 menit.
                3.  Simpan dalam wadah tertutup di tempat teduh.
                4.  Fermentasi: **14 Hari**.
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 10 Liter Air (10%). Aplikasi 2 minggu sekali.")

    elif mol_choice == "MOL Buah":
        with st.expander("🍎 MOL Buah (Generatif)", expanded=True):
            st.markdown("**Fungsi:** Pupuk masa Generatif (Pembuahan) & BOoster Manis.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Buah matang (Pepaya, Mangga, Pisang, Tomat, Nanas, dll): 2 kg
                *   Gula Merah: 0.5 kg
                *   Air Kelapa: 5 Liter
                *   Penyedap Rasa (Opsional): 1 sdt
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Cincang halus/blender buah-buahan.
                2.  Campur semua bahan, kocok/aduk 3-5 menit.
                3.  Simpan wadah tertutup, tempat teduh.
                4.  Fermentasi: **14 Hari**.
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 10 Liter Air (10%). Aplikasi 2 minggu sekali.")
            st.markdown("*Tips: Tambahkan kocokan telur bebek/ayam saat aplikasi agar buah makin manis.*")

    elif mol_choice == "MOL Rebung Bambu":
        with st.expander("🎍 MOL Rebung Bambu (ZPT Gibberellin)", expanded=True):
            st.markdown("**Fungsi:** Perangsang Tumbuh (Gibberellin) & Pengurai Kompos.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Rebung Bambu: 1 kg
                *   Air Leri (Beras): 5 Liter
                *   Gula Merah: 0.5 kg
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Iris tipis atau tumbuk rebung bambu.
                2.  Masukkan ke jerigen bersama Gula Merah dan Air Leri.
                3.  Kocok hingga tercampur.
                4.  Buka tutup sebentar setiap pagi (buang gas).
                5.  Siap pakai setelah **15 Hari**.
                """)
            st.info("""
            **Dosis:**
            *   **Pengomposan:** 1 MOL : 5 Air. Siramkan ke bahan kompos.
            *   **Tanaman:** 1 MOL : 15 Air. Semprot/Kocor.
            """)

    elif mol_choice == "MOL Keong Mas / Bekicot":
        with st.expander("🐌 MOL Keong Mas (Asam Amino Plus)", expanded=True):
            st.markdown("**Fungsi:** Sumber Asam Amino & Dekomposer.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Keong Mas/Bekicot Hidup: 1 kg
                *   Buah Maja (atau Gula Merah 0.5 kg): 1/2 buah
                *   Air Kelapa: 5 Liter
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Tumbuk halus Keong Mas (cangkang + daging).
                2.  Tumbuk halus Buah Maja / Gula Merah.
                3.  Campur semua dengan Air Kelapa dalam jerigen.
                4.  Kocok rata. Buka tutup sebentar setiap pagi.
                5.  Siap pakai setelah **15 Hari**.
                """)
            st.info("""
            **Dosis:**
            *   **Pengomposan:** 1 MOL : 5 Air (Plus 1 ons Gula Merah).
            *   **Tanaman:** 1 Liter per Tangki. Semprot pagi/sore.
            """)

    elif mol_choice == "MOL Bonggol Pisang":
        with st.expander("🍌 MOL Bonggol Pisang (ZPT Sitokinin)", expanded=True):
            st.markdown("**Fungsi:** Perangsang akar & tunas (Sitokinin).")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Bonggol Pisang: 1 kg
                *   Gula Merah: 0.5 ons
                *   Air Leri (Beras): 5 Liter
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Potong kecil/tumbuk bonggol pisang.
                2.  Larutkan gula merah dengan air leri.
                3.  Campur semua dalam jerigen, tutup rapat.
                4.  Buka tutup setiap 2 hari (buang gas).
                5.  Fermentasi: **14 Hari**.
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 10 Liter Air (10%). Aplikasi Vegetatif (2 minggu sekali).")

    elif mol_choice == "MOL Sabut Kelapa":
        with st.expander("🥥 MOL Sabut Kelapa (Kalium Tinggi)", expanded=True):
            st.markdown("**Fungsi:** Pupuk K (Kalium) untuk pembuahan.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Sabut Kelapa
                *   Air Bersih
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Masukkan sabut kelapa ke drum (jangan penuh).
                2.  Isi air sampai semua terendam.
                3.  Tutup rapat drum.
                4.  **Biarkan 2 Minggu**.
                5.  Air berwarna coklat hitam siap dipakai.
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 10 Liter Air (10%). Aplikasi 2 minggu sekali.")

    elif mol_choice == "MOL Gedebok / Pelepah Pisang":
        with st.expander("🌿 MOL Gedebok Pisang (Fosfat)", expanded=True):
            st.markdown("**Fungsi:** Sumber Fosfat & Penguat batang.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Bahan:")
                st.markdown("""
                *   Batang Pisang: 2 kg
                *   Air Nira (atau Gula Jawa 0.5 kg): 1 Liter
                """)
            with c2:
                st.markdown("#### Cara Buat:")
                st.markdown("""
                1.  Potong-potong batang pisang (jangan ditumbuk).
                2.  Campur dengan 3/4 Air Nira/Gula.
                3.  Masukkan baskom, padatkan.
                4.  Siram sisa nira di atasnya.
                5.  Tutup rapat, biarkan **2 Minggu**.
                6.  Peras airnya (MOL).
                """)
            st.success("💉 **Dosis:** 1 Liter MOL : 100 Liter Air (1:100). Semprot pagi/sore.")

# ===== TAB 5: HERBISIDA =====
with tab_herb:
    st.header("🌿 Herbisida Alami (Pembasmi Gulma)")
    st.info("Resep herbisida kontak ramah lingkungan untuk membasmi gulma/rumput liar.")
    
    with st.expander("🔥 Herbisida Garam + Cuka + Belerang", expanded=True):
        st.warning("⚠️ **Perhatian:** Herbisida ini bersifat **Kontak** (mematikan bagian yang terkena) dan **Non-Selektif** (mematikan semua tumbuhan hijau). Jangan semprotkan ke tanaman budidaya!")
        
        col_h1, col_h2 = st.columns(2)
        
        with col_h1:
            st.markdown("#### 🧪 Bahan-Bahan")
            st.markdown("""
            1.  **Garam:** 1 kg
            2.  **Cuka (80%):** 1 Botol
            3.  **Belerang / Sulfur:** 1.5 Ons
            4.  **Air:** 2 Liter
            """)
            
        with col_h2:
            st.markdown("#### 🥣 Cara Pembuatan")
            st.markdown("""
            1.  **Rebus Air:** Didihkan 2 liter air bersama **Garam** sampai larut.
            2.  **Tumbuk Halus:** Tumbuk belerang sampai benar-benar halus.
            3.  **Pencampuran:** Campurkan air garam panas dengan Cuka dan Belerang halus.
            4.  **Wadah:** Masukkan dalam jerigen/wadah tertutup.
            5.  **Kocok:** Kocok sampai tercampur rata.
            6.  **Diamkan:** Simpan selama **3 Hari** sebelum digunakan.
            """)
            
        st.markdown("---")
        st.markdown("#### 🚜 Cara Aplikasi")
        
        c_dose, c_time = st.columns(2)
        with c_dose:
            st.success("💉 **Dosis:**")
            st.markdown("""
            *   Campur **1 Liter Herbisida** dengan **1 Liter Air** (1:1).
            *   Atau 5 Liter campuran untuk areal luas (sesuaikan konsentrasi).
            """)
        with c_time:
            st.info("⏳ **Waktu Aplikasi:**")
            st.markdown("""
            *   Semprotkan ke lahan **minimal 2 Minggu** sebelum ditanami.
            *   Semprot saat cuaca cerah (panas terik) agar reaksi cepat.
            """)

# ===== TAB 6: ZPT =====
with tab_zpt:
    st.header("🚀 Zat Pengatur Tumbuh (ZPT) Alami")
    st.info("Kumpulan sumber fitohormon alami untuk memacu pertumbuhan dan hasil panen.")
    
    with st.expander("🍃 Ekstrak Daun Kelor (Sumber Sitokinin Alami)", expanded=True):
        col_sci, col_pr = st.columns([1, 1])
        
        with col_sci:
            st.success("🔬 **Fakta Ilmiah (Science Fact):**")
            st.markdown("""
            Ekstrak **Daun Kelor** (*Moringa oleifera*) kaya akan hormon **Zeatin** (salah satu jenis *Cytokinin* paling aktif). 
            
            **Manfaat Sitokinin (Cytokinin):**
            *   **Cell Division:** Memacu pembelahan sel tanaman muda secara cepat.
            *   **Delay Senescence:** Menunda penuaan daun (daun tetap hijau dan fotosintesis lebih lama).
            *   **Yield Booster:** Meningkatkan hasil panen 20-35%.
            *   **Immunity:** Tanaman lebih vigor dan tahan penyakit.
            
            *Referensi: Makkar and Becker (1996)*
            """)
            
        with col_pr:
            st.warning("🧪 **Metode Ekstraksi Laboratorium:**")
            st.caption("*Metode ini direkomendasikan untuk hasil ekstraksi hormon maksimal.*")
            st.markdown("""
            1.  **Bahan:** 20 gram Daun Kelor Segar.
            2.  **Pelarut:** 675 ml Etanol 80% (Alkohol).
            3.  **Alat:** Blender (Ultra-turrax) atau Tumbuk.
            4.  **Proses:** Haluskan daun bersama pelarut, saring ekstraknya.
            """)
            
        st.markdown("---")
        st.subheader("🥣 Cara Pembuatan (Versi Petani)")
        st.markdown("Jika Etanol sulit didapat, gunakan metode fermentasi air kelapa yang juga efektif menarik hormon.")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("#### Bahan:")
            st.markdown("""
            *   **Daun Kelor Segar:** 1 kg (Pilih pucuk/daun muda).
            *   **Air Kelapa:** 1 Liter (Sumber Cytokinin juga).
            *   **Gula Merah:** 1 Ons.
            """)
        with col_m2:
            st.markdown("#### Cara Buat:")
            st.markdown("""
            1.  Blender daun kelor bersama air kelapa sampai halus.
            2.  Campurkan gula merah cair.
            3.  Fermentasi selama **24 Jam - 3 Hari** (Jangan terlalu lama untuk ZPT segar).
            4.  Saring dan ambil airnya.
            """)
            
        st.success("💉 **Aplikasi:** Semprot daun (Foliar Spray) pagi hari. Dosis 1:10 (1 Bagian Ekstrak : 10 Bagian Air).")

    st.markdown("---")
    
    with st.expander("📚 Panduan Lengkap Ilmu Hormon (ZPT) - Oleh Edhi Sandra", expanded=False):
        st.markdown("""
        **Penting:** Hormon bukanlah nutrisi/makanan. Hormon adalah *"Provokator"* yang memerintah tanaman untuk tumbuh. 
        Tanpa nutrisi (pupuk) yang cukup, hormon tidak akan bekerja efektif.
        """)
        
        tab_konsep, tab_sumber, tab_tips = st.tabs(["🧠 Konsep Dasar", "🌿 Sumber Alami", "⚠️ Aturan Pakai"])
        
        with tab_konsep:
            st.markdown("#### 1. Tiga Raja Hormon")
            col_k1, col_k2, col_k3 = st.columns(3)
            with col_k1:
                st.info("🌱 **AUKSIN (Akar)**")
                st.markdown("""
                *   **Fungsi:** Memacu pertumbuhan **AKAR**.
                *   **Sifat:** Menghambat tunas & bunga.
                *   **Lokasi:** Diproduksi di pucuk, turun ke akar.
                """)
            with col_k2:
                st.success("🌿 **SITOKININ (Tunas)**")
                st.markdown("""
                *   **Fungsi:** Memacu pertumbuhan **TUNAS/DAUN**.
                *   **Sifat:** Menghambat akar & penuaan.
                *   **Lokasi:** Diproduksi di ujung akar, naik ke tunas.
                """)
            with col_k3:
                st.warning("🌺 **GIBERELIN (Bunga)**")
                st.markdown("""
                *   **Fungsi:** Memacu **BUNGA & BUAH**.
                *   **Sifat:** Memperbesar sel, memecah dormansi biji.
                *   **Lokasi:** Di daun dan buah.
                """)
                
            st.markdown("#### 2. Hukum Konsentrasi")
            st.markdown("""
            *   **Dosis Tepat:** Memacu pertumbuhan.
            *   **Dosis Berlebih:** Menghambat pertumbuhan (Kerdil).
            *   **Dosis Tinggi Sekali:** Mematikan (Herbisida).
            *   *Kunci: Lebih baik dosis rendah tapi rutin, daripada dosis tinggi sekali semprot.*
            """)

        with tab_sumber:
            st.markdown("#### 🧬 Sumber Hormon Organik di Sekitar Kita")
            st.markdown("""
            | Sumber Bahan | Kandungan Dominan |
            | :--- | :--- |
            | **Air Kelapa** | Auksin, Sitokinin, Giberelin (Lengkap) |
            | **Urine Ternak** | Auksin (Tinggi) |
            | **Kecambah (Tauge)** | Auksin |
            | **Bawang Merah** | Auksin |
            | **Rebung Bambu** | Giberelin (untuk pertumbuhan cepat) |
            | **Bonggol Pisang** | Sitokinin |
            | **Jagung Muda** | Sitokinin (Zeatin) |
            | **Eceng Gondok** | Giberelin |
            | **Daun Kelor** | Sitokinin (Zeatin) |
            | **Air Cucian Beras** | Vitamin B1 & Hormon pertumbuhan |
            """)
            
        with tab_tips:
            st.error("⛔ **Jangan Lakukan (Pantangan):**")
            st.markdown("""
            1.  **Salah Fase:** Jangan semprot Hormon Akar (Auksin) saat tanaman sedang berbunga/berbuah -> **Bunga bisa rontok!**
            2.  **Duplikasi:** Jika ingin memacu tunas (Sitokinin), jangan campur dengan hormon akar (Auksin) dosis tinggi, karena akan saling meniadakan.
            3.  **Tanpa Makan:** Jangan beri hormon jika tanaman kurus/kurang pupuk. Beri makan (pupuk) dulu, baru provokasi (hormon).
            """)
            
            st.success("✅ **Tips Aplikasi:**")
            st.markdown("""
            *   **Target Semprot:** Semprotkan hormon sesuai target. Hormon akar siram ke tanah/akar. Hormon tunas semprot ke daun bawah permukaan.
            *   **Waktu:** Pagi hari (stomata terbuka) atau sore hari.
            *   **Campuran:** Boleh dicampur dengan pupuk daun/POC, gula/molase, dan perekat organik.
            """)

# ===== TAB 7: SAWIT SPESIAL =====
with tab_sawit:
    st.header("🌴 Solusi Spesial Kelapa Sawit (By Ayah Manjel)")
    st.info("Kumpulan trik lapangan teruji untuk mengatasi masalah spesifik pada kebun Sawit.")
    
    with st.expander("♂️ Mengatasi Sawit Jantan Dominan (Sex Ratio Balance)", expanded=True):
        st.markdown("""
        **Masalah:** Tanaman sawit dominan bunga jantan, sedikit/tidak ada bunga betina.
        **Ilmiahnya:** Tanaman mengalami stres energi atau ketidakseimbangan nutrisi (biasanya C/N ratio rendah atau defisit air), sehingga "mencari jalan aman" dengan hanya memproduksi bunga jantan yang murah energi.
        """)
        
        st.warning("⚠️ **Solusi Lapangan (Ayah Manjel):** Memperbaiki nutrisi vegetatif & generatif secara kejut.")
        
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("#### 🧪 Ramuan Kocor (Akar)")
            st.markdown("""
            **Dosis per 10 Liter Air (Untuk 1 Pohon):**
            1.  **MOL Daun Hijau:** 1 Liter (Sumber Nitrogen/Vegetatif - Pakai Mol Gamal/Rumput Teki/Gajah).
            2.  **ROTAN Generatif (POC):** 200 cc (2 Gelas Aqua).
            3.  **Air:** 10 Liter.
            
            **Cara Aplikasi:**
            *   Siramkan (Kocor) di sekeliling piringan.
            *   Jarak 0.5 - 1 meter dari pangkal batang.
            """)
            
        with col_s2:
            st.markdown("#### 🚿 Ramuan Semprot (Daun)")
            st.markdown("""
            **Dosis per Tangki (15 Liter):**
            1.  **ROTAN Generatif (POC):** 250 cc (1 Gelas Aqua Besar).
            2.  **Air:** 15 Liter.
            
            **Cara Aplikasi:**
            *   Semprot basah merata ke: **Bunga Jantan, Batang, dan Pelepah Daun**.
            """)
            
        st.success("""
        ✅ **Hasil yang Diharapkan:**
        *   **15 Hari:** Bunga jantan rontok/mudah dicabut.
        *   **Berikutnya:** Muncul bunga betina pada pelepah baru.
        *   *Catatan:* Untuk pohon tinggi, gunakan sistem **TUGAL** (Lubang 30cm) untuk aplikasi kocor.
        """)
        
    st.markdown("---")
    
    with st.expander("💎 Meningkatkan Kualitas Buah (Berat & Mengkilap)", expanded=False):
        st.info("Trik meningkatkan Berat Tandan (BJR) dan Rendemen Minyak.")
        
        col_q1, col_q2 = st.columns([1, 2])
        
        with col_q1:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Elaeis_guineensis_fruit.jpg/320px-Elaeis_guineensis_fruit.jpg", caption="Buah Sawit Berkualitas")
            
        with col_q2:
            st.markdown("#### 🚜 Teknik Aplikasi")
            st.markdown("""
            1.  **Ramuan:** ROTAN Generatif (POC) **250 cc** + Air **15 Liter** (1 Tangki).
            2.  **Target:** Semprotkan langsung ke **Tandan Buah Sawit** secara merata.
            3.  **Waktu:** Lakukan **30 Hari sebelum panen**.
            """)
            
            st.success("""
            **Manfaat:**
            *   📈 **Berat Naik:** Kenaikan berat 30% - 50%.
            *   ✨ **Visual:** Buah lebih mengkilap dan besar.
            """)

# ===== TAB 8: KALKULATOR ORGANIK =====
with tab_kalkulator:
    st.header("🧮 Kalkulator Estimasi NPK Pupuk Organik")
    st.info("Hitung estimasi kandungan NPK dari campuran bahan organik Anda berdasarkan referensi ilmiah.")
    
    # --- Database Kandungan Hara (Scientific References - Range Average) ---
    # Values are approximate percentages of Dry Weight
    # Source refs: FAO, Dept. Pertanian, Jurnal Ilmu Tanah
    bahan_organik = {
        "Kotoran Ayam (Murni)": {"N": 3.0, "P": 2.5, "K": 1.5, "C_N": 10, "Desc": "Panas, Cepat Terurai, Kaya N & P"},
        "Kotoran Kambing/Domba": {"N": 1.5, "P": 1.0, "K": 1.5, "C_N": 25, "Desc": "Seimbang, Bagus untuk Buah"},
        "Kotoran Sapi": {"N": 1.0, "P": 0.5, "K": 1.0, "C_N": 18, "Desc": "Dingin, Pembenah Tanah"},
        "Kotoran Kelinci (Padat)": {"N": 2.0, "P": 1.4, "K": 0.6, "C_N": 12, "Desc": "Kualitas Tinggi"},
        "Guano (Kelelawar)": {"N": 1.0, "P": 10.0, "K": 1.0, "C_N": 10, "Desc": "Sangat Kaya Fosfor (P)"},
        "Urine Sapi": {"N": 1.0, "P": 0.1, "K": 1.0, "C_N": 0.8, "Desc": "Cepat Serap"},
        "Urine Kelinci": {"N": 2.5, "P": 0.2, "K": 1.5, "C_N": 0.8, "Desc": "High Nitrogen Liquid"},
        "Dedak Padi (Halus)": {"N": 2.0, "P": 1.0, "K": 1.0, "C_N": 20, "Desc": "Sumber Makanan Mikroba (Karb)"},
        "Sekam Padi (Mentah)": {"N": 0.5, "P": 0.2, "K": 0.5, "C_N": 80, "Desc": "Prositias Tinggi, Lambat Terurai"},
        "Arang Sekam": {"N": 0.3, "P": 0.2, "K": 1.0, "C_N": 100, "Desc": "Media Tanam, Sumber K, Hama"},
        "Jerami Padi": {"N": 0.6, "P": 0.2, "K": 1.4, "C_N": 60, "Desc": "Sumber Kalium (K) Tinggi"},
        "Hijauan (Leguminosa/Kacangan)": {"N": 3.5, "P": 0.5, "K": 2.0, "C_N": 15, "Desc": "Sumber Nitrogen Hijau"},
        "Dolomit (Kapur)": {"N": 0.0, "P": 0.0, "K": 0.0, "Mg": 18.0, "Ca": 30.0, "C_N": 0, "Desc": "Netralisir pH, Sumber Ca & Mg"},
        "Abu Dapur (Kayu)": {"N": 0.0, "P": 1.5, "K": 7.0, "C_N": 0, "Desc": "Sangat Kaya Kalium (K)"},
        "Cangkang Telur": {"N": 0.5, "P": 0.1, "K": 0.1, "Ca": 90.0, "C_N": 0, "Desc": "Sumber Kalsium (Ca)"}
    }

    # --- UI Input ---
    col_k1, col_k2 = st.columns([1, 2])
    
    with col_k1:
        st.markdown("### 📝 Pilih Bahan")
        options = list(bahan_organik.keys())
        selected_materials = st.multiselect("Tambahkan bahan ke resep:", options, default=["Kotoran Sapi", "Dedak Padi (Halus)"])
        
        inputs = {}
        st.markdown("---")
        for mat in selected_materials:
            inputs[mat] = st.number_input(f"Berat {mat} (kg/L):", min_value=0.1, value=10.0, step=1.0, key=mat)

    # --- Calculation Engine ---
    total_weight = 0
    total_n_kg = 0
    total_p_kg = 0
    total_k_kg = 0
    
    mix_details = []

    for mat, weight in inputs.items():
        data = bahan_organik[mat]
        n_content = data.get("N", 0)
        p_content = data.get("P", 0)
        k_content = data.get("K", 0)
        
        n_mass = weight * (n_content / 100)
        p_mass = weight * (p_content / 100)
        k_mass = weight * (k_content / 100)
        
        total_weight += weight
        total_n_kg += n_mass
        total_p_kg += p_mass
        total_k_kg += k_mass
        
        mix_details.append({
            "Bahan": mat,
            "Berat (kg)": weight,
            "N (%)": n_content,
            "P (%)": p_content,
            "K (%)": k_content,
            "Fungsi": data.get("Desc", "-")
        })

    # --- Results Display ---
    with col_k2:
        st.markdown("### 📊 Hasil Analisis Campuran")
        
        if total_weight > 0:
            final_n_percent = (total_n_kg / total_weight) * 100
            final_p_percent = (total_p_kg / total_weight) * 100
            final_k_percent = (total_k_kg / total_weight) * 100
            
            # Display Metrics
            m1, m2, m3, m4 = st.columns(4)
            m1.metric("Total Berat", f"{total_weight:.1f} kg")
            m2.metric("Nitrogen (N)", f"{final_n_percent:.2f} %", f"{total_n_kg:.2f} kg Real")
            m3.metric("Fosfor (P)", f"{final_p_percent:.2f} %", f"{total_p_kg:.2f} kg Real")
            m4.metric("Kalium (K)", f"{final_k_percent:.2f} %", f"{total_k_kg:.2f} kg Real")
            
            # Analysis
            st.success(f"**Estimasi NPK Mix:** {final_n_percent:.1f} - {final_p_percent:.1f} - {final_k_percent:.1f}")
            
            # Interpretation logic
            note = []
            if final_n_percent > 2.0: note.append("✅ **Tinggi Nitrogen:** Bagus untuk pertumbuhan Daun/Vegetatif.")
            if final_p_percent > 2.0: note.append("✅ **Tinggi Fosfor:** Bagus untuk Akar & Bunga.")
            if final_k_percent > 2.0: note.append("✅ **Tinggi Kalium:** Bagus untuk Kualitas Buah & Kekebalan.")
            if final_n_percent < 1.0 and final_p_percent < 1.0 and final_k_percent < 1.0:
                note.append("⚠️ **Kandungan Rendah:** Ini tipikal Kompos 'Pembenah Tanah', bukan pupuk utama. Berfungsi memperbaiki fisik tanah.")
            
            for n in note:
                st.info(n)

            # Disclaimer
            st.caption("""
            **Catatan Ilmiah:** 
            Angka ini adalah *estimasi matematis* berdasarkan rata-rata literatur. 
            Proses fermentasi dapat **meningkatkan** ketersediaan nutrisi (N-Fixing Bacteria) atau **menurunkan** (penguapan Amonia jika terlalu panas). 
            Selalu jaga C/N rasio dan suhu fermentasi.
            """)
            
            # Show Table detail
            with st.expander("🔍 Lihat Detail Kontribusi Bahan"):
                st.dataframe(mix_details)
        else:
            st.warning("Masukkan berat bahan untuk melihat hasil.")




