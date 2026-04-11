import streamlit as st
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
# Note: In a real app we might import metrics to check answers, but we implement from scratch here.

st.set_page_config(page_title="Machine Learning Eng", page_icon="🤖", layout="wide")

st.markdown("# 🤖 Machine Learning Engineering")
st.markdown("### From Scratch Implementation & Pipelines")
st.markdown("Modul ini fokus pada implementasi *low-level* komponen ML yang sering ditanyakan di interview Big Tech (misal: membangun Transformer sendiri atau metrik evaluasi dari nol).")

# Sidebar Resources
with st.sidebar:
    st.header("📚 Referensi Belajar")
    st.markdown("""
    **Dokumentasi:**
    - [Sklearn Developer Guide](https://scikit-learn.org/stable/developers/index.html) - Cara buat custom estimator.
    - [ML System Design Interview](https://github.com/chiphuyen/ml-system-design-book) - Chip Huyen.
    
    **Video Tutorial:**
    - [Krish Naik - Creating Pipelines Using Sklearn](https://www.youtube.com/watch?v=w9auF4BMrlk)
    - [StatQuest - Logistic Regression](https://www.youtube.com/watch?v=yIYKR4sgzI8)
    
    **Dokumentasi Resmi:**
    - [Sklearn Pipelines Guide](https://scikit-learn.org/stable/modules/compose.html)
    """)

tab1, tab2, tab3 = st.tabs(["🟢 Custom Transformers", "🟡 Pipelines (Intermediate)", "🔴 Metrics from Scratch"])

# --- BEGINNER: CUSTOM TRANSFORMERS ---
with tab1:
    st.header("🟢 Level Pemula: Custom Transformers")
    
    st.markdown("""
    ### 📚 Materi Singkat
    Untuk membuat transformer yang kompatibel dengan Scikit-Learn (bisa masuk Pipeline), kita perlu:
    1.  Mewarisi `BaseEstimator` dan `TransformerMixin`.
    2.  Implementasi method `fit(self, X, y=None)`: Mempelajari parameter (misal: mean, std).
    3.  Implementasi method `transform(self, X)`: Mengubah data.
    """)
    
    st.subheader("📝 Soal: Outlier Remover")
    st.markdown("""
    **Tugas**:
    Buat class `OutlierRemover` yang menghapus baris dimana nilai pada kolom tertentu **lebih besar dari** `mean + 3 * std`.
    
    *Catatan: Di Scikit-Learn asli, menghapus baris di transformer agak tricky untuk pipeline (karena X dan y jadi tidak sinkron), tapi ini soal logika pemrograman yang umum.*
    """)
    
    # Example Data
    data = {
        'A': [10, 12, 12, 13, 12, 100, 12, 11],  # 100 is outlier
        'B': [1, 1, 1, 1, 1, 1, 1, 1]
    }
    df = pd.DataFrame(data)
    st.write("Data Awal:")
    st.dataframe(df.T)
    
    code_beg = st.text_area("Tulis Implementasi Class:", height=250, key="code_beg", value="""class OutlierRemover(BaseEstimator, TransformerMixin):
    def __init__(self, factor=3):
        self.factor = factor
        
    def fit(self, X, y=None):
        return self
        
    def transform(self, X):
        # Tulis logika di sini
        return X
""")
    
    if st.button("Jalankan Kode", key="btn_beg"):
        try:
             # Prepare context
             local_vars = {
                 'BaseEstimator': BaseEstimator, 
                 'TransformerMixin': TransformerMixin, 
                 'pd': pd, 
                 'np': np,
                 'X': df.copy()
             }
             exec(code_beg, {}, local_vars)
             
             # Instantiate and run
             OutlierRemover = local_vars['OutlierRemover']
             remover = OutlierRemover(factor=3)
             X_filtered = remover.fit_transform(df)
             
             st.write("Hasil Transformasi:")
             st.dataframe(X_filtered)
             
             if len(X_filtered) < len(df) and 100 not in X_filtered['A'].values:
                 st.success("✅ Sukses! Outlier 100 berhasil dihapus.")
                 st.balloons()
             else:
                 st.warning("⚠️ Outlier belum terhapus atau logika masih kurang tepat.")
                 
        except Exception as e:
            st.error(f"Error: {e}")

    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Jawaban**:
        ```python
        class OutlierRemover(BaseEstimator, TransformerMixin):
            def __init__(self, factor=3):
                self.factor = factor
                
            def fit(self, X, y=None):
                # Kita tidak perlu mempelajari apa-apa di fit untuk logika ini, 
                # tapi kita bisa hitung mean/std di sini jika ingin fixed threshold.
                # Untuk soal ini, kita hitung dinamis di transform (per batch) atau di fit.
                # Versi robust: hitung mean/std di fit.
                self.mean_ = X.mean()
                self.std_ = X.std()
                return self
                
            def transform(self, X):
                X_new = X.copy()
                # Anggap kita filter hanya kolom numerik atau spesifik
                for col in X_new.select_dtypes(include=np.number).columns:
                    upper_bound = self.mean_[col] + (self.factor * self.std_[col])
                    X_new = X_new[X_new[col] <= upper_bound]
                return X_new
        ```
        **Penting**:
        -   `BaseEstimator`: Memberi fitur `get_params` dan `set_params`.
        -   `TransformerMixin`: Memberi fitur `fit_transform` gratis.
        """)

# --- INTERMEDIATE: PIPELINES ---
with tab2:
    st.header("🟡 Level Menengah: ML Pipelines")
    
    st.markdown("""
    ### 📚 Materi Singkat
    **Pipeline** merangkai beberapa langkah proses (preprocessing -> model) menjadi satu objek.
    Ini mencegah *data leakage* (kebocoran data) karena transformasi `fit` hanya dilakukan pada data latih.
    """)
    
    st.subheader("📝 Soal: Rangkai Pipeline")
    st.markdown("""
    **Tugas**:
    Buat pipeline sederhana (variabel `my_pipeline`) yang melakukan:
    1.  Imputasi nilai kosong dengan 0 (gunakan `fillna` manual atau bayangkan `SimpleImputer`).
    2.  Scaling standar (`StandardScaler`).
    *Catatan: Kita simulasi saja kodenya.*
    """)
    
    code_int = st.text_area("Tulis Kode Pipeline:", height=150, key="code_int", value="""from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# my_pipeline = ...
""")
    
    if st.button("Jalankan Kode", key="btn_int"):
        st.success("✅ Konsep Pipeline benar! (Simulasi)")
        
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Jawaban**:
        ```python
        my_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
            ('scaler', StandardScaler())
        ])
        ```
        """)

# --- ADVANCED: METRICS FROM SCRATCH ---
with tab3:
    st.header("🔴 Level Mahir: Metrics from Scratch")
    
    st.markdown("""
    ### 📚 Materi Singkat
    Memahami matematika di balik metrik evaluasi.
    -   **Precision**: TP / (TP + FP) -> Seberapa akurat saat memprediksi Positif.
    -   **Recall**: TP / (TP + FN) -> Seberapa banyak Positif yang berhasil ditemukan.
    -   **F1-Score**: Harmonic Mean dari Precision dan Recall.
    """)
    
    st.subheader("📝 Soal: Implementasi F1 Score")
    st.markdown("""
    **Tugas**:
    Implementasikan fungsi `calculate_f1(y_true, y_pred)` menggunakan Numpy dasar. 
    Jangan gunakan `sklearn.metrics`.
    """)
    
    y_true = np.array([1, 1, 1, 0, 0, 1, 0])
    y_pred = np.array([1, 0, 1, 0, 1, 1, 0])
    # TP: 3 (idx 0, 2, 5)
    # FP: 1 (idx 4)
    # FN: 1 (idx 1)
    
    st.write("y_true:", y_true)
    st.write("y_pred:", y_pred)
    
    code_adv = st.text_area("Tulis Fungsi Anda:", height=200, key="code_adv", value="""def calculate_f1(y_true, y_pred):
    # Hitung TP, FP, FN
    # Return f1
    pass
""")
    
    if st.button("Jalankan Kode", key="btn_adv"):
        try:
             local_vars = {'np': np}
             exec(code_adv, {}, local_vars)
             calc_f1 = local_vars.get('calculate_f1')
             
             if calc_f1:
                 user_f1 = calc_f1(y_true, y_pred)
                 # Expected
                 tp = np.sum((y_true == 1) & (y_pred == 1))
                 fp = np.sum((y_true == 0) & (y_pred == 1))
                 fn = np.sum((y_true == 1) & (y_pred == 0))
                 precision = tp / (tp + fp)
                 recall = tp / (tp + fn)
                 expected_f1 = 2 * (precision * recall) / (precision + recall)
                 
                 st.write(f"F1 Score Anda: {user_f1:.4f}")
                 st.write(f"F1 Score Target: {expected_f1:.4f}")
                 
                 if np.isclose(user_f1, expected_f1):
                     st.success("✅ Sempurna! Implementasi F1 Score Anda benar.")
                     st.balloons()
                 else:
                     st.error("❌ Hasil belum tepat.")
        except Exception as e:
            st.error(f"Error: {e}")
            
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Jawaban**:
        ```python
        def calculate_f1(y_true, y_pred):
            # True Positive: Prediksi 1 dan Aktual 1
            tp = np.sum((y_true == 1) & (y_pred == 1))
            
            # False Positive: Prediksi 1 tapi Aktual 0
            fp = np.sum((y_true == 0) & (y_pred == 1))
            
            # False Negative: Prediksi 0 tapi Aktual 1
            fn = np.sum((y_true == 1) & (y_pred == 0))
            
            if (tp + fp) == 0: precision = 0
            else: precision = tp / (tp + fp)
            
            if (tp + fn) == 0: recall = 0
            else: recall = tp / (tp + fn)
            
            if (precision + recall) == 0: return 0
            
            f1 = 2 * (precision * recall) / (precision + recall)
            return f1
        ```
        """)
