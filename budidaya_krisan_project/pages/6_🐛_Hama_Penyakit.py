# 🐛 Hama & Penyakit Krisan
# Panduan IPM (Integrated Pest Management)

import streamlit as st
import pandas as pd

st.set_page_config(page_title="Hama & Penyakit", page_icon="🐛", layout="wide")

# CSS
st.markdown("""
<style>
    .pest-card {
        background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
        border: 1px solid #fca5a5;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .disease-card {
        background: linear-gradient(135deg, #fefce8 0%, #ffffff 100%);
        border: 1px solid #fde047;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    .solution-box {
        background: #ecfdf5;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 🐛 Hama & Penyakit Krisan Spray")
st.info("Panduan identifikasi dan pengendalian terpadu (IPM) untuk budidaya krisan.")

tab1, tab2, tab3 = st.tabs(["🪲 Hama Utama", "🦠 Penyakit Utama", "🛡️ Program IPM"])

# TAB 1: Hama
with tab1:
    st.subheader("🪲 Hama Utama pada Krisan")
    
    # THRIPS
    st.markdown("""
    <div class="pest-card">
        <h3>🔴 1. Thrips (Frankliniella occidentalis)</h3>
        <p><strong>Tingkat Bahaya:</strong> ⭐⭐⭐⭐⭐ (Sangat Tinggi)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gejala Serangan:**
        - Bercak putih keperakan pada daun
        - Daun menggulung dan keriting
        - Bunga cacat, tidak membuka sempurna
        - Terlihat serangga kecil (1-2mm) pada kuncup bunga
        
        **Siklus Hidup:** 14-21 hari (sangat cepat!)
        """)
    with col2:
        st.markdown("""
        <div class="solution-box">
        <strong>🛡️ Pengendalian:</strong><br>
        • Pasang sticky trap kuning (10-20/1000m²)<br>
        • Semprot Spinosad 0.5 ml/L<br>
        • Aplikasi Abamectin 0.5 ml/L<br>
        • Rotasi insektisida (hindari resistensi)<br>
        • Buang bunga/bagian terinfeksi berat
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # APHIDS
    st.markdown("""
    <div class="pest-card">
        <h3>🟠 2. Kutu Daun / Aphids (Aphis gossypii)</h3>
        <p><strong>Tingkat Bahaya:</strong> ⭐⭐⭐⭐ (Tinggi)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gejala Serangan:**
        - Koloni kutu di pucuk dan tunas muda
        - Daun keriting dan tumbuh abnormal
        - Embun madu → jamur jelaga hitam
        - Tanaman kerdil, bunga kecil
        
        **Vektor virus:** Cucumber Mosaic Virus (CMV)
        """)
    with col2:
        st.markdown("""
        <div class="solution-box">
        <strong>🛡️ Pengendalian:</strong><br>
        • Semprot Imidacloprid 0.25 ml/L<br>
        • Aplikasi sabun insektisida<br>
        • Predator alami: Coccinellid (kumbang koksi)<br>
        • Hindari pemupukan N berlebihan<br>
        • Buang bagian terinfeksi
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # LEAF MINER
    st.markdown("""
    <div class="pest-card">
        <h3>🟡 3. Leaf Miner (Liriomyza spp.)</h3>
        <p><strong>Tingkat Bahaya:</strong> ⭐⭐⭐ (Sedang)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gejala Serangan:**
        - Liang/terowongan berliku di daun
        - Daun menguning dan kering
        - Kualitas tanaman menurun
        - Lalat kecil beterbangan
        """)
    with col2:
        st.markdown("""
        <div class="solution-box">
        <strong>🛡️ Pengendalian:</strong><br>
        • Yellow sticky trap<br>
        • Cyromazine (regulator pertumbuhan)<br>
        • Abamectin 0.5 ml/L<br>
        • Buang daun terinfeksi berat
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # SPIDER MITES
    st.markdown("""
    <div class="pest-card">
        <h3>🔵 4. Tungau / Spider Mites (Tetranychus urticae)</h3>
        <p><strong>Tingkat Bahaya:</strong> ⭐⭐⭐⭐ (Tinggi, terutama musim kering)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gejala Serangan:**
        - Bintik kuning/perunggu pada daun
        - Daun mengering dari bawah ke atas
        - Jaring halus di permukaan bawah daun
        - Populasi meledak saat kering & panas
        """)
    with col2:
        st.markdown("""
        <div class="solution-box">
        <strong>🛡️ Pengendalian:</strong><br>
        • Jaga kelembaban >60%<br>
        • Akarisida: Abamectin, Spiromesifen<br>
        • Predator: Phytoseiulus persimilis<br>
        • Semprot bawah daun (tempat hidup tungau)
        </div>
        """, unsafe_allow_html=True)

# TAB 2: Penyakit
with tab2:
    st.subheader("🦠 Penyakit Utama pada Krisan")
    
    # WHITE RUST
    st.markdown("""
    <div class="disease-card">
        <h3>⚪ 1. White Rust / Karat Putih (Puccinia horiana)</h3>
        <p><strong>Tingkat Bahaya:</strong> ⭐⭐⭐⭐⭐ (SANGAT BERBAHAYA - Karantina!)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gejala:**
        - Bercak kuning pucat di permukaan atas daun
        - Pustul putih/krem di bawah daun
        - Daun melenting dan rontok
        - Menyebar sangat cepat!
        
        **⚠️ WASPADA:** Penyakit karantina di banyak negara!
        """)
    with col2:
        st.markdown("""
        <div class="solution-box">
        <strong>🛡️ Pengendalian:</strong><br>
        • <strong>Pencegahan utama!</strong> Gunakan bibit bersertifikat<br>
        • Fungisida: Mancozeb, Chlorothalonil preventif<br>
        • Trifloxystrobin/Azoxystrobin kuratif<br>
        • Bakar tanaman terinfeksi (JANGAN kompos!)<br>
        • Karantina area terinfeksi
        </div>
        """, unsafe_allow_html=True)
    
    st.error("🚨 **PENTING:** Jika menemukan white rust, SEGERA isolasi dan musnahkan tanaman. Laporkan ke dinas pertanian setempat!")
    
    st.markdown("---")
    
    # FUSARIUM
    st.markdown("""
    <div class="disease-card">
        <h3>🟤 2. Layu Fusarium (Fusarium oxysporum)</h3>
        <p><strong>Tingkat Bahaya:</strong> ⭐⭐⭐⭐ (Tinggi)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gejala:**
        - Daun menguning dari bawah
        - Layu meski tanah lembab
        - Pembuluh batang coklat (belah batang)
        - Tanaman mati perlahan
        """)
    with col2:
        st.markdown("""
        <div class="solution-box">
        <strong>🛡️ Pengendalian:</strong><br>
        • Sterilisasi media tanam (fumigasi/solarisasi)<br>
        • Gunakan antagonis Trichoderma<br>
        • Rotasi tanaman<br>
        • Jaga pH tanah 6.5-7.0<br>
        • Cabut dan bakar tanaman sakit
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # PYTHIUM
    st.markdown("""
    <div class="disease-card">
        <h3>🟢 3. Busuk Akar Pythium (Pythium spp.)</h3>
        <p><strong>Tingkat Bahaya:</strong> ⭐⭐⭐ (Sedang-Tinggi)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gejala:**
        - Stek gagal berakar
        - Akar coklat, lembek, busuk
        - Tanaman layu mendadak
        - Terjadi saat overwatering
        """)
    with col2:
        st.markdown("""
        <div class="solution-box">
        <strong>🛡️ Pengendalian:</strong><br>
        • Jangan overwatering!<br>
        • Drainase yang baik<br>
        • Fungisida: Metalaxyl, Fosetyl-Al<br>
        • Antagonis: Trichoderma
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # BOTRYTIS
    st.markdown("""
    <div class="disease-card">
        <h3>🔘 4. Busuk Bunga Botrytis (Botrytis cinerea)</h3>
        <p><strong>Tingkat Bahaya:</strong> ⭐⭐⭐⭐ (Tinggi saat hujan)</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Gejala:**
        - Bercak coklat pada kelopak bunga
        - Lapisan kapang abu-abu
        - Bunga busuk dan rontok
        - Parah saat kelembaban >85%
        """)
    with col2:
        st.markdown("""
        <div class="solution-box">
        <strong>🛡️ Pengendalian:</strong><br>
        • Ventilasi yang baik!<br>
        • Jaga kelembaban <80%<br>
        • Fungisida: Iprodione, Boscalid<br>
        • Buang bunga terinfeksi
        </div>
        """, unsafe_allow_html=True)

# TAB 3: Program IPM
with tab3:
    st.subheader("🛡️ Program Pengendalian Hama Terpadu (IPM)")
    
    st.success("""
    **Prinsip IPM:**
    1. **Pencegahan** → lebih baik dari pengobatan
    2. **Monitoring** → deteksi dini = kerugian minimal
    3. **Pengendalian Terpadu** → kombinasi metode
    4. **Pestisida Terakhir** → bila perlu saja, rotasi!
    """)
    
    st.markdown("### 📋 Jadwal Monitoring Rutin")
    
    monitoring_data = pd.DataFrame({
        "Waktu": ["Harian", "Mingguan", "2 Minggu Sekali", "Bulanan"],
        "Aktivitas": [
            "Cek sticky trap, amati gejala visual di pucuk/tunas muda",
            "Hitung populasi hama di 10 tanaman sampel, cek bawah daun untuk tungau",
            "Evaluasi efektivitas pengendalian, rotasi pestisida jika perlu",
            "Review data, laporkan ke konsultan, update strategi"
        ],
        "Target Pengamatan": [
            "Thrips, aphids, lalat leaf miner",
            "Populasi per tanaman, persentase serangan",
            "Trend naik/turun, resistensi",
            "Analisis musiman, prediksi outbreak"
        ]
    })
    
    st.dataframe(monitoring_data, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### 🧪 Contoh Program Pestisida Rotasi")
    
    st.warning("⚠️ Rotasi pestisida WAJIB untuk mencegah resistensi! Ganti golongan bahan aktif setiap 2-3 aplikasi.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Minggu 1-2: Golongan A**
        - Spinosad (Spinosyns)
        - Target: Thrips, leaf miner
        
        **Minggu 3-4: Golongan B**
        - Imidacloprid (Neonicotinoid)
        - Target: Aphids, whitefly
        """)
    
    with col2:
        st.markdown("""
        **Minggu 5-6: Golongan C**
        - Abamectin (Avermectin)
        - Target: Tungau, thrips
        
        **Minggu 7-8: Kembali ke A**
        - Atau gunakan golongan baru
        """)
    
    st.markdown("---")
    
    st.markdown("### 🌿 Pengendalian Hayati (Agen Biologi)")
    
    biocontrol = pd.DataFrame({
        "Agen Hayati": ["Amblyseius swirskii", "Phytoseiulus persimilis", "Aphidius colemani", 
                        "Orius insidiosus", "Trichoderma harzianum"],
        "Target": ["Thrips, whitefly", "Spider mites", "Aphids", "Thrips, aphids", "Fusarium, Pythium"],
        "Aplikasi": ["Release 50-100/m²", "Release 10-20/m²", "Release 2-5/m²", 
                    "Release 1-2/m²", "Kocor 5g/L"]
    })
    
    st.dataframe(biocontrol, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Panduan Hama & Penyakit")
