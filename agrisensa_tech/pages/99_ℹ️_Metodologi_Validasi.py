import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Metodologi & Validasi Sistem",
    page_icon="ℹ️",
    layout="wide"
)

st.title("ℹ️ Metodologi & Validasi Saintifik")
st.markdown("---")

st.markdown("""
### 🛡️ Pernyataan Pertanggungjawaban (Accountability Statement)
Sistem AgriSensa dibangun di atas prinsip **Transparansi Algoritmik** dan **Landasan Agronomi Modern**. 
Halaman ini mendokumentasikan logika, rumus matematika, dan sumber data yang digunakan di balik setiap rekomendasi yang dihasilkan sistem, untuk menjamin validitas dan akuntabilitas hasil.
""")

# --- TAB SETUP ---
tab1, tab2, tab3 = st.tabs(["🧪 Logika Hara (Agronomi)", "🧠 Kecerdasan Buatan (ML)", "⚖️ Sistem Keputusan (TOPSIS)"])

# === TAB 1: AGRONOMI ===
with tab1:
    st.header("1. Kalkulator Hara & Pupuk Presisi")
    st.info("**Digunakan pada:** Dasbor Rekomendasi Terpadu")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Konsep: Hukum Keseimbangan Massa")
        st.write("""
        Perhitungan dosis pupuk tidak dilakukan secara *rule of thumb* semata, melainkan menggunakan pendekatan **Scientific Nutrient Balance** yang mempertimbangkan:
        1.  **Target Yield**: Berapa ton hasil panen yang ingin dicapai.
        2.  **Soil Supply**: Berapa hara yang sudah tersedia di tanah (hasil uji lab).
        3.  **Efficiency Factor**: Seberapa efisien tanaman menyerap hara pada kondisi pH tertentu.
        """)
        
        st.markdown("#### Rumus Dasar (Core Formula)")
        st.latex(r'''
        \text{Kebutuhan Pupuk} = \frac{(\text{Kebutuhan Tanaman} - \text{Suplai Tanah}) \times \text{Faktor Koreksi}}{\text{Kandungan Hara Pupuk} \times \text{Efisiensi Penyerapan}}
        ''')
        
    with col2:
        st.subheader("Koreksi pH (Hukum Mitscherlich)")
        st.write("Ketersediaan hara sangat bergantung pada pH tanah. Kami menggunakan **Kurva Distribusi Normal** untuk memodelkan penurunan efisiensi penyerapan saat pH menyimpang dari optimal.")
        
        # Plotting the pH Curve logic used in code
        ph_range = np.linspace(4, 9, 100)
        opt_ph = 6.5
        efficiency = np.exp(-0.5 * ((ph_range - opt_ph) / 1.0)**2) * 100
        
        chart_data = pd.DataFrame({"pH Tanah": ph_range, "Efisiensi Penyerapan (%)": efficiency})
        st.line_chart(chart_data, x="pH Tanah", y="Efisiensi Penyerapan (%)")
        st.caption("Grafik: Model penurunan efisiensi hara yang digunakan sistem saat pH menjauhi 6.5")

    st.markdown("---")
    st.markdown("#### 📚 Sumber Data Referensi")
    st.markdown("""
    - **Standar Kebutuhan Hara**: FAO (Food and Agriculture Organization) & Puslitanak (Pusat Penelitian Tanah dan Agroklimat).
    - **Sifat Fisik Tanah**: Asumsi Berat Jenis Tanah (Bulk Density) = $1.2 \text{ g/cm}^3$ atau $2,000,000 \text{ kg/ha}$ (lapisan olah 20cm).
    """)

# === TAB 2: MACHINE LEARNING ===
with tab2:
    st.header("2. Prediksi Kecerdasan Buatan (AI)")
    st.info("**Digunakan pada:** Rekomendasi Dosis Cepat & Prediksi Tanaman Cocok")
    
    st.markdown("""
    Fitur ini menggunakan model **Machine Learning** tipe Klasifikasi dan Regresi untuk memberikan estimasi probabilistik berdasarkan data historis.
    """)
    
    c_ai1, c_ai2 = st.columns(2)
    
    with c_ai1:
        st.subheader("Arsitektur Model")
        st.markdown("""
        - **Algoritma**: Random Forest Classifier / Regressor.
        - **Sifat Hasil**: **Probabilistik** (Peluang/Estimasi Terbaik).
        - **Keunggulan**: Mampu menangkap pola non-linier yang kompleks antar variabel (misal: hubungan suhu, curah hujan, dan pH terhadap kesuburan).
        """)
        st.code("""
# Cuplikan Arsitektur Model (Python/Scikit-Learn)
model = RandomForestClassifier(
    n_estimators=100, 
    criterion='gini', 
    max_depth=None
)
        """, language="python")

    with c_ai2:
        st.subheader("Data Latih (Training Data)")
        st.warning("⚠️ Validitas AI bergantung penuh pada kualitas data latih.")
        st.write("""
        Dataset yang digunakan mencakup ribuan sampel data pertanian yang berisi variabel:
        - N, P, K, pH Tanah
        - Temperatur & Kelembaban
        - Curah Hujan
        - Label Tanaman / Dosis Optimal
        """)
        
    st.subheader("Mekanisme Keamanan (Fail-Safe)")
    st.success("""
    Jika prediksi AI dinilai aneh atau *outliers* (misal: dosis negatif atau terlalu ekstrem), sistem secara otomatis akan beralih ke **Logika Rule-Based Manual** untuk menjaga keamanan rekomendasi.
    """)

# === TAB 3: TOPSIS ===
with tab3:
    st.header("3. Sistem Pendukung Keputusan (SPK)")
    st.info("**Digunakan pada:** Pemilihan Strategi Pertanian (Ranking)")
    
    st.write("Kami menggunakan metode **TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution)**. Ini adalah metode matematika murni yang objektif, bukan tebakan AI.")
    
    st.markdown("#### Langkah Algoritma")
    st.markdown("""
    1.  **Matriks Keputusan**: Mengumpulkan semua opsi strategi (Kimia, Organik, Berimbang).
    2.  **Normalisasi**: Menyamakan satuan (misal: Rupiah vs Persen vs Skala 1-5).
    3.  **Pembobotan**: Mengalikan dengan bobot preferensi User (Efektivitas vs Biaya).
    4.  **Jarak Solusi Ideal**:
        - Menghitung jarak opsi ke **Solusi Ideal Positif** (Biaya termurah, Hasil tertinggi).
        - Menghitung jarak opsi ke **Solusi Ideal Negatif** (Biaya termahal, Hasil terendah).
    5.  **Perangkingan**: Opsi dengan rasio terbaik (paling dekat ke Positif dan paling jauh dari Negatif) menjadi Juara 1.
    """)
    
    st.latex(r'''
    \text{Skor TOPSIS} = \frac{D_i^-}{D_i^+ + D_i^-}
    ''')
    st.caption("Dimana $D_i^-$ adalah jarak ke solusi terburuk dan $D_i^+$ adalah jarak ke solusi terbaik. Semakin mendekati 1, semakin sempurna.")

st.markdown("---")
st.caption("© 2025 AgriSensa Artificial Intelligence System. Dokumen ini dibuat secara otomatis untuk menjamin auditabilitas sistem.")
