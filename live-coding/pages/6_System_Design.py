import streamlit as st

st.set_page_config(page_title="ML System Design", page_icon="🏗️", layout="wide")

st.markdown("# 🏗️ Machine Learning System Design")
st.markdown("### Designing Scalable ML Applications (Bahasa Indonesia)")
st.markdown("Modul ini membahas arsitektur sistem ML skala besar. Fokus pada **Trade-off**, **Scalability**, dan **Reliability**.")

# Sidebar Resources
with st.sidebar:
    st.header("📚 Referensi Belajar")
    st.markdown("""
    **Buku & Panduan:**
    - [Grokking the ML Interview](https://www.educative.io/courses/grokking-the-machine-learning-interview) - courses (wajib).
    - [CS329s: ML Systems Design](https://stanford-cs329s.github.io/) - Stanford Course.
    - [ByteByteGo](https://bytebytego.com/) - General System Design.
    
    **Video Tutorial:**
    - [System Design Primer](https://github.com/donnemartin/system-design-primer)
    - [Fraud Detection System Design](https://www.youtube.com/watch?v=5p8wJv_zdf8)
    """)

tab1, tab2 = st.tabs(["🟢 Design Pattern: Recommendation", "🔴 Design Pattern: Real-time Fraud"])

# --- RECOMMENDATION SYSTEM ---
with tab1:
    st.header("🟢 Recommendation System (Sistem Rekomendasi)")
    
    st.markdown("""
    ### 🎯 Studi Kasus: Video Recommendation (e.g., YouTube/TikTok)
    
    #### 1. Arsitektur Umum (Funnel Approach)
    Sistem rekomendasi skala besar biasanya membagi proses menjadi dua tahap utama karena jumlah konten (items) terlalu banyak (jutaan/miliaran) untuk diranking satu per satu.
    
    1.  **Candidate Generation (Retrieval)**:
        -   **Tujuan**: Menyaring jutaan item menjadi ratusan kandidat relevan dengan cepat.
        -   **Metode**: Collaborative Filtering (Matrix Factorization), Two-Tower Neural Networks, Graph-based.
        -   **Optimasi**: Kecepatan tinggi, Recall tinggi (jangan sampai ada item bagus terlewat).
        
    2.  **Ranking (Scoring)**:
        -   **Tujuan**: Mengurutkan ratusan kandidat untuk mendapatkan top-k item terbaik bagi user.
        -   **Metode**: Deep Neural Networks (DNN) dengan banyak fitur (user history, context, item metadata).
        -   **Optimasi**: Presisi tinggi (Precision), memaksimalkan engagement (Watch time, Click).
    
    #### 2. Kunci Desain (Design Implementation)
    """)
    
    st.info("""
    **Pertanyaan Interview**:
    "Bagaimana cara menangani **Cold Start Problem** (User baru atau Item baru)?"
    """)
    
    with st.expander("💡 Lihat Jawaban & Strategi"):
        st.markdown("""
        **Strategi Cold Start:**
        1.  **Untuk User Baru**:
            -   **Heuristic**: Tampilkan item populer/trending secara global.
            -   **Demografis**: Gunakan lokasi, umur, gender (jika ada saat sign-up) untuk personalisasi kasar.
            -   **Contextual**: Rekomendasi berdasarkan waktu, device, atau referer source.
        2.  **Untuk Item Baru**:
            -   **Content-Based**: Gunakan metadata item (kategori, tag, deskripsi) untuk mencari kemiripan dengan item yang disukai user lain.
            -   **Exploration (Bandits)**: Berikan 'boost' sementara pada item baru (exploration) untuk mengumpulkan data interaksi, sebelum dievaluasi murni berdasarkan performa (exploitation).
        """)
        
    st.markdown("#### 3. Metrics Evaluasi")
    st.markdown("""
    -   **Offline**: Precision@k, Recall@k, NDCG (Normalized Discounted Cumulative Gain).
    -   **Online**: Click-Through Rate (CTR), Watch Time, Conversion Rate.
    """)

# --- FRAUD DETECTION ---
with tab2:
    st.header("🔴 Real-time Fraud Detection (Deteksi Penipuan)")
    
    st.markdown("""
    ### 🎯 Studi Kasus: Credit Card Transaction Fraud
    
    #### 1. Tantangan Utama
    -   **Latency**: Keputusan (Allow/Block) harus dibuat dalam milidetik (< 200ms).
    -   **Imbalanced Data**: Transaksi fraud sangat sedikit (< 0.1%) dibanding transaksi legit.
    -   **Concept Drift**: Pola serangan penipu berubah dengan sangat cepat.
    
    #### 2. Arsitektur Real-time
    Sistem ini membutuhkan pemrosesan data streaming dan fitur instan.
    
    -   **Data Ingestion**: Kafka / Kinesis (Menangani ribuan transaksi per detik).
    -   **Stream Processing**: Flink / Spark Streaming (Menghitung fitur real-time seperti "jumlah transaksi dalam 5 menit terakhir").
    -   **Feature Store**: Redis / Cassandra (Menyimpan fitur user profile dan aggregasi real-time untuk akses low-latency).
    -   **Model Serving**: API Model (ONNX/TFLite) untuk prediksi cepat.
    """)
    
    st.code("""
    [User Swipe Card] -> [Payment Gateway] -> [Kafka Topic]
                                              |
                                              v
                                      [Stream Processor (Flink)] <--- [Feature Store (Redis)]
                                              | (Get Feature: Count last 10m)
                                              v
                                        [Model Inference]
                                              |
                                     (Score > 0.9? BLOCK : ALLOW)
    """, language="text")
    
    st.info("""
    **Pertanyaan Interview**:
    "Bagaimana menangani **Imbalanced Data** yang ekstrim pada fase training?"
    """)
    
    with st.expander("💡 Lihat Jawaban & Strategi"):
        st.markdown("""
        **Strategi Imbalanced Data:**
        1.  **Resampling**:
            -   **Undersampling** mayoritas (legit transaction) - Hati-hati kehilangan info.
            -   **Oversampling** minoritas (fraud) misal dengan **SMOTE** (Synthetic Minority Over-sampling Technique).
        2.  **Algorithmic**:
            -   Gunakan **Class Weights** (memberi penalti lebih besar jika salah prediksi fraud) pada Loss Function (misal: `scale_pos_weight` di XGBoost).
            -   Gunakan algoritma berbasis ensemble (Random Forest, XGBoost) yang umumnya lebih robust.
        3.  **Metric**:
            -   JANGAN gunakan Accuracy.
            -   Gunakan **Precision-Recall Curve (PR-AUC)**, F1-Score, atau Recall (jika prioritas menangkap semua fraud, siap menerima False Alarm).
        """)
