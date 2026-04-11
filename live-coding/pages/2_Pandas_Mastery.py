import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Pandas Mastery", page_icon="🐼", layout="wide")

st.markdown("# 🐼 Pandas Mastery")
st.markdown("### Tantangan Manipulasi & Pembersihan Data")
st.markdown("Modul ini dirancang untuk mengasah kemampuan manipulasi data Anda dari level dasar hingga mahir, dengan penjelasan dalam **Bahasa Indonesia**.")

with st.sidebar:
    st.header("📚 Referensi Belajar")
    st.markdown("""
    **Dokumentasi & Artikel:**
    - [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html) - Kitab suci Pandas.
    - [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) - Ringkasan cepat.
    
    **Video Tutorial (YouTube):**
    - [Keith Galli - Complete Pandas Tutorial (Pro!!)](https://www.youtube.com/watch?v=vmEHCJofslg)
    - [Data School - Pandas Tips](https://www.youtube.com/watch?v=hl-TJI4rmks)
    """)

# Helper to compare dataframes
def check_dataframe(user_df, expected_df):
    try:
        pd.testing.assert_frame_equal(user_df, expected_df)
        st.success("✅ Benar! DataFrame sesuai dengan jawaban yang diharapkan.")
        st.balloons()
    except AssertionError as e:
        st.error(f"❌ Belum tepat. Perbedaan: {e}")
    except Exception as e:
        st.error(f"⚠️ Error Eksekusi: {e}")

tab1, tab2, tab3 = st.tabs(["🟢 Beginner (Pemula)", "🟡 Intermediate (Menengah)", "🔴 Advanced (Mahir)"])

# --- BEGINNER SECTION ---
with tab1:
    st.header("🟢 Level Pemula: Filtering & Seleksi")
    
    st.markdown("""
    ### 📚 Materi Singkat
    Di pandas, menyeleksi data adalah kuncinya. Ada beberapa cara utama:
    1.  **Seleksi Kolom**: `df['nama_kolom']`
    2.  **Boolean Indexing** (Filtering): `df[df['umur'] > 25]`
    3.  **Kombinasi Kondisi**:
        -   `&` untuk **DAN** (AND)
        -   `|` untuk **ATAU** (OR)
        -   Jangan lupa kurung `()`: `df[(df['a'] > 1) & (df['b'] < 5)]`
    """)
    
    st.markdown("---")
    
    # Problem 1: Employee Filtering
    st.subheader("📝 Soal 1: Filter Karyawan")
    
    # Sample Data
    data = {
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eva'],
        'age': [25, 30, 35, 40, 28],
        'city': ['New York', 'Los Angeles', 'New York', 'Chicago', 'New York'],
        'salary': [70000, 80000, 120000, 90000, 110000]
    }
    df = pd.DataFrame(data)
    
    st.markdown("""
    **Tugas**:
    Diberikan dataframe `df`, lakukan filter untuk mendapatkan karyawan yang:
    1.  Tinggal di **'New York'**
    2.  **DAN** memiliki gaji (`salary`) lebih besar dari **100,000**.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Current DataFrame:")
        st.dataframe(df)
    
    user_code = st.text_area("Tulis kode Anda (hasilkan variabel `result`):", value="result = df[...]", height=100)
    
    if st.button("Jalankan Kode", key="pd_beg_1"):
        try:
            # Safe exec env
            local_vars = {'df': df.copy(), 'pd': pd}
            exec(user_code, {}, local_vars)
            result = local_vars.get('result')
            
            # Expected
            expected = df[(df['city'] == 'New York') & (df['salary'] > 100000)]
            
            if result is not None:
                st.write("Hasil Anda:")
                st.dataframe(result)
                check_dataframe(result, expected)
            else:
                st.error("Variabel 'result' tidak ditemukan. Pastikan Anda menugaskan hasil ke `result`.")
        except Exception as e:
            st.error(f"Execution Error: {e}")

    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Jawaban**:
        ```python
        result = df[(df['city'] == 'New York') & (df['salary'] > 100000)]
        ```
        **Penjelasan**:
        -   Kita menggunakan dua kondisi.
        -   Kondisi 1: `df['city'] == 'New York'` mengecek kota.
        -   Kondisi 2: `df['salary'] > 100000` mengecek gaji.
        -   Operator `&` menggabungkan keduanya (harus benar dua-duanya).
        -   Tanda kurung `()` **wajib** ada di setiap kondisi agar urutan operasinya benar.
        """)

    st.markdown("---")
    
    # Problem 2: Handling Missing Values
    st.subheader("📝 Soal 2: Menangani Data Kosong (Null)")
    
    data_missing = {
        'product': ['A', 'B', 'C', 'D'],
        'price': [100, np.nan, 150, 200],
        'stock': [10, 5, np.nan, 20]
    }
    df_missing = pd.DataFrame(data_missing)
    
    st.markdown("""
    **Tugas**:
    -   Isi nilai kosong pada kolom `substitute` (misal harga) dengan **0**.
    """)
    st.info("Catatan: Dalam soal ini, variabel `df_missing` tersedia. Simpan haslnya ke `result`.")
    st.dataframe(df_missing)
    
    user_code_2 = st.text_area("Solusi Anda:", value="result = df_missing.fillna(...)", height=100, key="code_beg_2")
    
    if st.button("Jalankan Kode", key="btn_beg_2"):
        expected_2 = df_missing.fillna(0)
        try:
            local_vars = {'df_missing': df_missing.copy(), 'pd': pd, 'np': np}
            exec(user_code_2, {}, local_vars)
            result_2 = local_vars.get('result')
            if result_2 is not None:
                st.write("Hasil:")
                st.dataframe(result_2)
                check_dataframe(result_2, expected_2)
            else: 
                st.error("Variable 'result' not found.")
        except Exception as e:
            st.error(str(e))
            
    with st.expander("💡 Lihat Penjelasan"):
        st.markdown("""
        **Jawaban**:
        ```python
        result = df_missing.fillna(0)
        ```
        **Penjelasan**:
        -   Fungsi `.fillna(nilai)` digunakan untuk mengganti `NaN` (Not a Number) dengan nilai tertentu.
        -   Ini sangat penting dalam data cleaning sebelum masuk ke model machine learning.
        """)

# --- INTERMEDIATE SECTION ---
with tab2:
    st.header("🟡 Level Menengah: GroupBy & Aggregasi")
    
    st.markdown("""
    ### 📚 Materi Singkat
    Teknik **Split-Apply-Combine** sangat powerful:
    1.  **Split**: Memecah data berdasarkan grup (misal: per departemen).
    2.  **Apply**: Menerapkan fungsi (sum, mean, count) ke setiap grup.
    3.  **Combine**: Menyatukan kembali hasilnya.
    
    Sintaks dasar: `df.groupby('kolom_grup')['kolom_target'].agg(['mean', 'sum'])`
    """)
    
    # Soal Intermediat
    dates = pd.date_range('20230101', periods=6)
    df2 = pd.DataFrame({
        'Date': dates,
        'Category': ['Elektronik', 'Pakaian', 'Elektronik', 'Pakaian', 'Elektronik', 'Makanan'],
        'Sales': [1000, 500, 1200, 600, 1100, 300],
        'Profit': [200, 50, 300, 100, 250, 30]
    })
    
    st.subheader("📝 Soal: Analisis Kategori")
    st.dataframe(df2)
    st.markdown("**Tugas**: Hitung **rata-rata (mean)** dari kolom `Sales` untuk setiap `Category`. Simpan hasil (Series) ke variabel `result`.")
    
    user_code_int = st.text_area("Solusi Anda:", value="result = df2...", key="code_int")
    
    if st.button("Jalankan Kode", key="btn_int"):
        expected_int = df2.groupby('Category')['Sales'].mean()
        try:
             local_vars = {'df2': df2.copy(), 'pd': pd}
             exec(user_code_int, {}, local_vars)
             result_int = local_vars.get('result')
             if result_int is not None:
                 st.write("Hasil:")
                 st.dataframe(result_int)
                 # Series check
                 try:
                     pd.testing.assert_series_equal(result_int, expected_int)
                     st.success("✅ Benar!")
                     st.balloons()
                 except:
                     st.error("❌ Hasil tidak sesuai.")
        except Exception as e:
            st.error(str(e))
            
    with st.expander("💡 Lihat Penjelasan"):
         st.markdown("""
         **Jawaban**:
         ```python
         result = df2.groupby('Category')['Sales'].mean()
         ```
         **Penjelasan**:
         -   `df2.groupby('Category')`: Mengelompokkan baris berdasarkan nilai unik di kolom Category.
         -   `['Sales']`: Kita hanya tertarik pada kolom Sales untuk dihitung.
         -   `.mean()`: Fungsi agregasi rata-rata.
         """)

# --- ADVANCED SECTION ---
with tab3:
    st.header("🔴 Level Mahir: Window Functions & Apply")
    
    st.markdown("""
    ### 📚 Materi Singkat
    Untuk interview Big Tech, Anda harus menguasai:
    1.  **Rolling Windows**: Menghitung moving average (misal: rata-rata 3 hari terakhir).
        -   Syntax: `df.rolling(window=3).mean()`
    2.  **Apply**: Menerapkan fungsi custom yang kompleks ke baris/kolom.
        -   Syntax: `df.apply(lambda row: ..., axis=1)`
    """)
    
    st.subheader("📝 Soal: 3-Day Rolling Average")
    
    df3 = pd.DataFrame({
        'Date': pd.date_range('2023-01-01', periods=5),
        'Price': [100, 110, 120, 130, 140]
    })
    st.dataframe(df3)
    
    st.markdown("""
    **Tugas**:
    Buat kolom baru atau Series yang berisi **Rata-rata Bergerak 3 Hari (3-Day Rolling Mean)** dari kolom `Price`.
    Pastikan data terurut berdasarkan Tanggal (sudah terurut di sini). Simpan hasil ke `result`.
    """)
    
    user_code_adv = st.text_area("Solusi Anda:", value="result = ...", key="code_adv")
    
    if st.button("Jalankan Kode", key="btn_adv"):
        expected_adv = df3['Price'].rolling(window=3).mean()
        try:
             local_vars = {'df3': df3.copy(), 'pd': pd}
             exec(user_code_adv, {}, local_vars)
             result_adv = local_vars.get('result')
             if result_adv is not None:
                 st.write("Hasil:")
                 st.dataframe(result_adv)
                 pd.testing.assert_series_equal(result_adv, expected_adv)
                 st.success("✅ Luar Biasa! Pemahaman window function Anda bagus.")
                 st.balloons()
             else:
                st.error("Variable 'result' not found.")
        except Exception as e:
             st.error(str(e))
             
    with st.expander("💡 Lihat Penjelasan"):
        st.markdown("""
        **Jawaban**:
        ```python
        result = df3['Price'].rolling(window=3).mean()
        ```
        **Penjelasan**:
        -   `rolling(window=3)`: Membuat jendela selebar 3 baris (hari ini + 2 hari sebelumnya).
        -   `.mean()`: Menghitung rata-rata dalam jendela tersebut.
        -   Dua nilai pertama akan `NaN` karena belum cukup data (butuh 3 data).
        """)
