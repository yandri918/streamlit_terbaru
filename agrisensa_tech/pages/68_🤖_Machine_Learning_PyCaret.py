import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Machine Learning PyCaret", page_icon="🤖", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        color: white;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🤖 Machine Learning dengan PyCaret</h1>
    <p>AutoML untuk Prediksi & Analisis Data Pertanian</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
### 🎯 Tentang PyCaret

**PyCaret** adalah library AutoML (Automated Machine Learning) yang mempermudah proses machine learning dari data preparation hingga deployment.

**Keunggulan PyCaret:**
- 🚀 AutoML - Otomatis compare puluhan model
- 📊 Built-in visualizations
- 🔧 Hyperparameter tuning otomatis
- 📦 Model deployment ready
- 🎓 Low-code, mudah dipelajari
- 🔄 Support regression, classification, clustering, time series

> **Note:** Modul ini menggunakan simulasi PyCaret untuk demonstrasi. Untuk production, install PyCaret dengan `pip install pycaret`.
""")

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Regression", 
    "🎯 Classification", 
    "🔵 Clustering",
    "📉 Time Series",
    "📚 Tutorial"
])

# ============================================================================
# TAB 1: REGRESSION - Prediksi Hasil Panen
# ============================================================================
with tab1:
    st.markdown("### 📈 Regression: Prediksi Hasil Panen")
    
    st.markdown("""
    **Use Case:** Memprediksi hasil panen (ton/ha) berdasarkan input pertanian.
    
    **Features:**
    - Pupuk N, P, K (kg/ha)
    - Curah hujan (mm)
    - Suhu rata-rata (°C)
    - pH tanah
    - Luas lahan (ha)
    """)
    
    # Generate sample data
    np.random.seed(42)
    n_samples = 200
    
    data_reg = pd.DataFrame({
        'Pupuk_N': np.random.uniform(50, 200, n_samples),
        'Pupuk_P': np.random.uniform(30, 120, n_samples),
        'Pupuk_K': np.random.uniform(40, 150, n_samples),
        'Curah_Hujan': np.random.uniform(1000, 2500, n_samples),
        'Suhu': np.random.uniform(25, 32, n_samples),
        'pH': np.random.uniform(5.5, 7.5, n_samples),
        'Luas_Lahan': np.random.uniform(0.5, 5, n_samples),
    })
    
    # Create target with realistic relationship
    data_reg['Hasil_Panen'] = (
        2.5 + 
        0.015 * data_reg['Pupuk_N'] +
        0.012 * data_reg['Pupuk_P'] +
        0.010 * data_reg['Pupuk_K'] +
        0.002 * data_reg['Curah_Hujan'] +
        0.15 * data_reg['pH'] -
        0.08 * data_reg['Suhu'] +
        np.random.randn(n_samples) * 0.5
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Dataset Preview")
        st.dataframe(data_reg.head(10), use_container_width=True)
        
        st.markdown("#### 📈 Statistik Deskriptif")
        st.dataframe(data_reg.describe().round(2), use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Workflow PyCaret Regression")
        
        st.code("""
# 1. Setup environment
from pycaret.regression import *

setup(data=data_reg, 
      target='Hasil_Panen',
      session_id=123,
      normalize=True,
      transformation=True,
      remove_outliers=True,
      train_size=0.8)

# 2. Compare models
best_models = compare_models(n_select=5)

# 3. Tune best model
tuned_model = tune_model(best_models[0])

# 4. Evaluate
evaluate_model(tuned_model)

# 5. Predict
predictions = predict_model(tuned_model, data=new_data)

# 6. Save model
save_model(tuned_model, 'yield_prediction_model')
        """, language='python')
    
    st.markdown("---")
    st.markdown("#### 🔬 Simulasi Model Comparison")
    
    # Simulate model comparison results
    model_results = pd.DataFrame({
        'Model': ['Random Forest', 'XGBoost', 'LightGBM', 'Extra Trees', 'Gradient Boosting', 
                 'Linear Regression', 'Ridge', 'Lasso', 'ElasticNet', 'KNN'],
        'MAE': [0.45, 0.48, 0.47, 0.46, 0.50, 0.65, 0.64, 0.66, 0.65, 0.72],
        'MSE': [0.32, 0.35, 0.34, 0.33, 0.38, 0.58, 0.57, 0.59, 0.58, 0.68],
        'RMSE': [0.57, 0.59, 0.58, 0.57, 0.62, 0.76, 0.75, 0.77, 0.76, 0.82],
        'R²': [0.89, 0.88, 0.88, 0.89, 0.87, 0.78, 0.79, 0.77, 0.78, 0.72],
        'Training Time (s)': [2.3, 3.1, 2.8, 2.5, 3.5, 0.1, 0.1, 0.1, 0.1, 0.2]
    }).sort_values('R²', ascending=False)
    
    st.dataframe(model_results.style.highlight_max(subset=['R²'], color='lightgreen')
                                   .highlight_min(subset=['MAE', 'MSE', 'RMSE'], color='lightgreen'),
                use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig_r2 = px.bar(model_results, x='Model', y='R²', 
                       title='Model Performance (R² Score)',
                       color='R²', color_continuous_scale='Viridis')
        fig_r2.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig_r2, use_container_width=True)
    
    with col2:
        fig_time = px.scatter(model_results, x='Training Time (s)', y='R²', 
                             text='Model', size='R²',
                             title='Training Time vs Performance',
                             color='R²', color_continuous_scale='RdYlGn')
        fig_time.update_traces(textposition='top center')
        fig_time.update_layout(height=400)
        st.plotly_chart(fig_time, use_container_width=True)
    
    st.markdown("#### 🎯 Feature Importance (Random Forest)")
    
    feature_importance = pd.DataFrame({
        'Feature': ['Pupuk_N', 'Curah_Hujan', 'Pupuk_P', 'pH', 'Pupuk_K', 'Suhu', 'Luas_Lahan'],
        'Importance': [0.28, 0.22, 0.18, 0.14, 0.10, 0.05, 0.03]
    }).sort_values('Importance', ascending=True)
    
    
    fig_importance = px.bar(feature_importance, x='Importance', y='Feature',
                            title='Feature Importance',
                            color='Importance', color_continuous_scale='Blues',
                            orientation='h')
    fig_importance.update_layout(height=350)
    st.plotly_chart(fig_importance, use_container_width=True)
    
    st.markdown("#### 🔮 Prediction Interface")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        n_input = st.number_input("Pupuk N (kg/ha)", 50, 200, 120, key='reg_n')
        p_input = st.number_input("Pupuk P (kg/ha)", 30, 120, 70, key='reg_p')
        k_input = st.number_input("Pupuk K (kg/ha)", 40, 150, 90, key='reg_k')
    
    with col2:
        rain_input = st.number_input("Curah Hujan (mm)", 1000, 2500, 1800, key='reg_rain')
        temp_input = st.number_input("Suhu (°C)", 25.0, 32.0, 28.5, key='reg_temp')
    
    with col3:
        ph_input = st.number_input("pH Tanah", 5.5, 7.5, 6.5, key='reg_ph')
        area_input = st.number_input("Luas Lahan (ha)", 0.5, 5.0, 2.0, key='reg_area')
    
    if st.button("🔮 Prediksi Hasil Panen", key='predict_reg'):
        # Simulate prediction
        predicted_yield = (
            2.5 + 
            0.015 * n_input +
            0.012 * p_input +
            0.010 * k_input +
            0.002 * rain_input +
            0.15 * ph_input -
            0.08 * temp_input
        )
        
        st.success(f"### 🎯 Prediksi Hasil Panen: **{predicted_yield:.2f} ton/ha**")
        
        # Confidence interval
        lower = predicted_yield - 0.5
        upper = predicted_yield + 0.5
        st.info(f"📊 **Confidence Interval (95%):** {lower:.2f} - {upper:.2f} ton/ha")

# ============================================================================
# TAB 2: CLASSIFICATION - Deteksi Penyakit
# ============================================================================
with tab2:
    st.markdown("### 🎯 Classification: Deteksi Penyakit Tanaman")
    
    st.markdown("""
    **Use Case:** Klasifikasi penyakit tanaman berdasarkan gejala dan kondisi lingkungan.
    
    **Classes:**
    - Sehat
    - Bercak Daun
    - Layu Bakteri
    - Virus Mosaik
    """)
    
    # Generate sample data
    np.random.seed(123)
    n_samples = 300
    
    diseases = ['Sehat', 'Bercak Daun', 'Layu Bakteri', 'Virus Mosaik']
    
    data_class = pd.DataFrame({
        'Bercak_Kuning': np.random.randint(0, 100, n_samples),
        'Bercak_Coklat': np.random.randint(0, 100, n_samples),
        'Daun_Layu': np.random.randint(0, 100, n_samples),
        'Pertumbuhan_Terhambat': np.random.randint(0, 100, n_samples),
        'Kelembaban': np.random.uniform(60, 95, n_samples),
        'Suhu': np.random.uniform(20, 35, n_samples),
        'Penyakit': np.random.choice(diseases, n_samples)
    })
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Dataset Preview")
        st.dataframe(data_class.head(10), use_container_width=True)
        
        # Class distribution
        class_dist = data_class['Penyakit'].value_counts()
        fig_dist = px.pie(values=class_dist.values, names=class_dist.index,
                         title='Distribusi Kelas Penyakit',
                         color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Workflow PyCaret Classification")
        
        st.code("""
# 1. Setup environment
from pycaret.classification import *

setup(data=data_class, 
      target='Penyakit',
      session_id=123,
      normalize=True,
      remove_outliers=True,
      fix_imbalance=True,
      train_size=0.8)

# 2. Compare models
best_models = compare_models(n_select=3)

# 3. Tune best model
tuned_model = tune_model(best_models[0])

# 4. Evaluate
evaluate_model(tuned_model)

# 5. Predict
predictions = predict_model(tuned_model, data=new_data)

# 6. Save model
save_model(tuned_model, 'disease_detection_model')
        """, language='python')
    
    st.markdown("---")
    st.markdown("#### 🔬 Simulasi Model Comparison")
    
    # Simulate classification results
    class_results = pd.DataFrame({
        'Model': ['Random Forest', 'XGBoost', 'LightGBM', 'Extra Trees', 'Gradient Boosting',
                 'Logistic Regression', 'SVM', 'KNN', 'Naive Bayes', 'Decision Tree'],
        'Accuracy': [0.94, 0.93, 0.93, 0.92, 0.91, 0.85, 0.88, 0.86, 0.82, 0.89],
        'Precision': [0.93, 0.92, 0.92, 0.91, 0.90, 0.84, 0.87, 0.85, 0.81, 0.88],
        'Recall': [0.94, 0.93, 0.93, 0.92, 0.91, 0.85, 0.88, 0.86, 0.82, 0.89],
        'F1-Score': [0.93, 0.92, 0.92, 0.91, 0.90, 0.84, 0.87, 0.85, 0.81, 0.88],
        'AUC': [0.98, 0.97, 0.97, 0.96, 0.96, 0.91, 0.93, 0.92, 0.88, 0.94],
        'Training Time (s)': [2.8, 3.5, 3.2, 2.9, 4.1, 0.2, 1.5, 0.3, 0.1, 0.5]
    }).sort_values('Accuracy', ascending=False)
    
    st.dataframe(class_results.style.highlight_max(subset=['Accuracy', 'Precision', 'Recall', 'F1-Score', 'AUC'], color='lightgreen'),
                use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig_acc = px.bar(class_results, x='Model', y='Accuracy',
                        title='Model Accuracy Comparison',
                        color='Accuracy', color_continuous_scale='Greens')
        fig_acc.update_layout(xaxis_tickangle=-45, height=400)
        st.plotly_chart(fig_acc, use_container_width=True)
    
    with col2:
        # Confusion Matrix (simulated for best model)
        conf_matrix = np.array([
            [45, 2, 1, 0],
            [1, 42, 2, 1],
            [0, 3, 44, 1],
            [1, 0, 2, 43]
        ])
        
        fig_cm = px.imshow(conf_matrix, 
                          labels=dict(x="Predicted", y="Actual", color="Count"),
                          x=diseases, y=diseases,
                          title='Confusion Matrix (Random Forest)',
                          color_continuous_scale='Blues',
                          text_auto=True)
        fig_cm.update_layout(height=400)
        st.plotly_chart(fig_cm, use_container_width=True)
    
    st.markdown("#### 🔮 Prediction Interface")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        bercak_kuning = st.slider("Bercak Kuning (%)", 0, 100, 30, key='class_bk')
        bercak_coklat = st.slider("Bercak Coklat (%)", 0, 100, 20, key='class_bc')
    
    with col2:
        daun_layu = st.slider("Daun Layu (%)", 0, 100, 15, key='class_dl')
        pertumbuhan = st.slider("Pertumbuhan Terhambat (%)", 0, 100, 10, key='class_pt')
    
    with col3:
        kelembaban = st.slider("Kelembaban (%)", 60, 95, 80, key='class_hum')
        suhu_class = st.slider("Suhu (°C)", 20, 35, 28, key='class_temp')
    
    if st.button("🔮 Deteksi Penyakit", key='predict_class'):
        # Simple rule-based prediction for demo
        if bercak_kuning > 50 or bercak_coklat > 50:
            prediction = "Bercak Daun"
            confidence = 0.87
        elif daun_layu > 50:
            prediction = "Layu Bakteri"
            confidence = 0.91
        elif pertumbuhan > 50:
            prediction = "Virus Mosaik"
            confidence = 0.84
        else:
            prediction = "Sehat"
            confidence = 0.95
        
        st.success(f"### 🎯 Prediksi: **{prediction}**")
        st.info(f"📊 **Confidence:** {confidence*100:.1f}%")
        
        # Show probabilities
        probs = {
            'Sehat': np.random.uniform(0.05, 0.15) if prediction != 'Sehat' else confidence,
            'Bercak Daun': np.random.uniform(0.05, 0.15) if prediction != 'Bercak Daun' else confidence,
            'Layu Bakteri': np.random.uniform(0.05, 0.15) if prediction != 'Layu Bakteri' else confidence,
            'Virus Mosaik': np.random.uniform(0.05, 0.15) if prediction != 'Virus Mosaik' else confidence,
        }
        # Normalize
        total = sum(probs.values())
        probs = {k: v/total for k, v in probs.items()}
        
        fig_probs = px.bar(x=list(probs.keys()), y=list(probs.values()),
                          title='Probability Distribution',
                          labels={'x': 'Penyakit', 'y': 'Probability'},
                          color=list(probs.values()),
                          color_continuous_scale='RdYlGn')
        st.plotly_chart(fig_probs, use_container_width=True)

# ============================================================================
# TAB 3: CLUSTERING - Segmentasi Petani
# ============================================================================
with tab3:
    st.markdown("### 🔵 Clustering: Segmentasi Profil Petani")
    
    st.markdown("""
    **Use Case:** Mengelompokkan petani berdasarkan karakteristik untuk program yang targeted.
    
    **Features:**
    - Luas lahan
    - Produksi tahunan
    - Penggunaan teknologi
    - Modal kerja
    - Pengalaman bertani
    """)
    
    # Generate sample data
    np.random.seed(456)
    n_farmers = 150
    
    data_cluster = pd.DataFrame({
        'Luas_Lahan': np.random.uniform(0.5, 10, n_farmers),
        'Produksi_Tahunan': np.random.uniform(2, 50, n_farmers),
        'Skor_Teknologi': np.random.randint(1, 10, n_farmers),
        'Modal_Kerja': np.random.uniform(5, 100, n_farmers),
        'Pengalaman': np.random.randint(1, 40, n_farmers)
    })
    
    # Simulate clustering (3 clusters)
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data_cluster)
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    data_cluster['Cluster'] = kmeans.fit_predict(data_scaled)
    data_cluster['Cluster'] = data_cluster['Cluster'].map({0: 'Petani Kecil', 1: 'Petani Menengah', 2: 'Petani Besar'})
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Dataset Preview")
        st.dataframe(data_cluster.head(10), use_container_width=True)
        
        # Cluster distribution
        cluster_dist = data_cluster['Cluster'].value_counts()
        fig_cluster_dist = px.pie(values=cluster_dist.values, names=cluster_dist.index,
                                  title='Distribusi Cluster',
                                  color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_cluster_dist, use_container_width=True)
    
    with col2:
        st.markdown("#### 🎯 Workflow PyCaret Clustering")
        
        st.code("""
# 1. Setup environment
from pycaret.clustering import *

setup(data=data_cluster,
      session_id=123,
      normalize=True,
      pca=True,
      pca_components=3)

# 2. Create models
kmeans = create_model('kmeans', num_clusters=3)
dbscan = create_model('dbscan')
hclust = create_model('hclust', num_clusters=3)

# 3. Assign clusters
data_with_clusters = assign_model(kmeans)

# 4. Plot clusters
plot_model(kmeans, plot='cluster')
plot_model(kmeans, plot='distribution')
plot_model(kmeans, plot='elbow')

# 5. Save model
save_model(kmeans, 'farmer_segmentation_model')
        """, language='python')
    
    st.markdown("---")
    st.markdown("#### 📊 Cluster Visualization")
    
    # 2D scatter plot
    fig_scatter = px.scatter(data_cluster, x='Luas_Lahan', y='Produksi_Tahunan',
                            color='Cluster', size='Modal_Kerja',
                            hover_data=['Skor_Teknologi', 'Pengalaman'],
                            title='Cluster Visualization: Luas Lahan vs Produksi',
                            color_discrete_sequence=px.colors.qualitative.Set2)
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("#### 📈 Cluster Characteristics")
    
    # Cluster statistics
    cluster_stats = data_cluster.groupby('Cluster').agg({
        'Luas_Lahan': 'mean',
        'Produksi_Tahunan': 'mean',
        'Skor_Teknologi': 'mean',
        'Modal_Kerja': 'mean',
        'Pengalaman': 'mean'
    }).round(2)
    
    st.dataframe(cluster_stats, use_container_width=True)
    
    # Radar chart for cluster profiles
    categories = ['Luas Lahan', 'Produksi', 'Teknologi', 'Modal', 'Pengalaman']
    
    fig_radar = go.Figure()
    
    for cluster in data_cluster['Cluster'].unique():
        cluster_data = data_cluster[data_cluster['Cluster'] == cluster]
        values = [
            cluster_data['Luas_Lahan'].mean() / 10 * 10,
            cluster_data['Produksi_Tahunan'].mean() / 50 * 10,
            cluster_data['Skor_Teknologi'].mean(),
            cluster_data['Modal_Kerja'].mean() / 100 * 10,
            cluster_data['Pengalaman'].mean() / 40 * 10
        ]
        
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=cluster
        ))
    
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        title='Cluster Profile Comparison',
        height=500
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    
    st.markdown("#### 💡 Actionable Insights")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🌱 Petani Kecil**
        - Lahan < 3 ha
        - Teknologi rendah
        - **Rekomendasi:**
          - Subsidi pupuk
          - Pelatihan teknologi
          - Akses kredit mikro
        """)
    
    with col2:
        st.markdown("""
        **🌾 Petani Menengah**
        - Lahan 3-7 ha
        - Teknologi sedang
        - **Rekomendasi:**
          - Mekanisasi pertanian
          - Kemitraan korporasi
          - Diversifikasi produk
        """)
    
    with col3:
        st.markdown("""
        **🚜 Petani Besar**
        - Lahan > 7 ha
        - Teknologi tinggi
        - **Rekomendasi:**
          - IoT & precision farming
          - Export market access
          - R&D collaboration
        """)

# ============================================================================
# TAB 4: TIME SERIES - Forecasting Harga
# ============================================================================
with tab4:
    st.markdown("### 📉 Time Series: Forecasting Harga Komoditas")
    
    st.markdown("""
    **Use Case:** Prediksi harga komoditas pertanian untuk planning produksi.
    
    **Features:**
    - Historical price data
    - Seasonality detection
    - Trend analysis
    - Confidence intervals
    """)
    
    # Generate time series data
    dates = pd.date_range(start='2022-01-01', end='2025-12-31', freq='D')
    n_days = len(dates)
    
    # Create realistic price pattern with trend and seasonality
    trend = np.linspace(8000, 12000, n_days)
    seasonality = 2000 * np.sin(2 * np.pi * np.arange(n_days) / 365)
    noise = np.random.randn(n_days) * 500
    
    prices = trend + seasonality + noise
    
    data_ts = pd.DataFrame({
        'Date': dates,
        'Price': prices
    })
    
    # Split into train and forecast
    split_date = '2025-07-01'
    train_data = data_ts[data_ts['Date'] < split_date]
    forecast_dates = data_ts[data_ts['Date'] >= split_date]
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("#### 📊 Historical Price Data")
        st.dataframe(train_data.tail(10), use_container_width=True)
        
        # Statistics
        st.markdown("#### 📈 Price Statistics")
        st.metric("Current Price", f"Rp {train_data['Price'].iloc[-1]:,.0f}")
        st.metric("Average Price", f"Rp {train_data['Price'].mean():,.0f}")
        st.metric("Price Volatility (Std)", f"Rp {train_data['Price'].std():,.0f}")
    
    with col2:
        st.markdown("#### 🎯 Workflow PyCaret Time Series")
        
        st.code("""
# 1. Setup environment
from pycaret.time_series import *

setup(data=data_ts,
      fh=180,  # Forecast horizon (days)
      fold=3,
      session_id=123)

# 2. Compare models
best_models = compare_models(n_select=3)

# 3. Tune best model
tuned_model = tune_model(best_models[0])

# 4. Finalize model
final_model = finalize_model(tuned_model)

# 5. Predict future
predictions = predict_model(final_model, fh=180)

# 6. Plot forecast
plot_model(final_model, plot='forecast')

# 7. Save model
save_model(final_model, 'price_forecast_model')
        """, language='python')
    
    st.markdown("---")
    st.markdown("#### 📊 Price Forecast Visualization")
    
    # Generate forecast
    forecast_trend = np.linspace(train_data['Price'].iloc[-1], 13000, len(forecast_dates))
    forecast_seasonality = 2000 * np.sin(2 * np.pi * np.arange(len(forecast_dates)) / 365)
    forecast_prices = forecast_trend + forecast_seasonality
    
    # Confidence intervals
    lower_bound = forecast_prices - 1000
    upper_bound = forecast_prices + 1000
    
    # Plot
    fig_ts = go.Figure()
    
    # Historical data
    fig_ts.add_trace(go.Scatter(
        x=train_data['Date'],
        y=train_data['Price'],
        mode='lines',
        name='Historical',
        line=dict(color='blue')
    ))
    
    # Forecast
    fig_ts.add_trace(go.Scatter(
        x=forecast_dates['Date'],
        y=forecast_prices,
        mode='lines',
        name='Forecast',
        line=dict(color='red', dash='dash')
    ))
    
    # Confidence interval
    fig_ts.add_trace(go.Scatter(
        x=forecast_dates['Date'].tolist() + forecast_dates['Date'].tolist()[::-1],
        y=upper_bound.tolist() + lower_bound.tolist()[::-1],
        fill='toself',
        fillcolor='rgba(255,0,0,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='95% Confidence Interval',
        showlegend=True
    ))
    
    fig_ts.update_layout(
        title='Price Forecast with Confidence Interval',
        xaxis_title='Date',
        yaxis_title='Price (Rp)',
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_ts, use_container_width=True)
    
    st.markdown("#### 📈 Forecast Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Current Price", f"Rp {train_data['Price'].iloc[-1]:,.0f}")
    
    with col2:
        st.metric("30-Day Forecast", f"Rp {forecast_prices[29]:,.0f}",
                 delta=f"{((forecast_prices[29] - train_data['Price'].iloc[-1]) / train_data['Price'].iloc[-1] * 100):.1f}%")
    
    with col3:
        st.metric("90-Day Forecast", f"Rp {forecast_prices[89]:,.0f}",
                 delta=f"{((forecast_prices[89] - train_data['Price'].iloc[-1]) / train_data['Price'].iloc[-1] * 100):.1f}%")
    
    with col4:
        st.metric("180-Day Forecast", f"Rp {forecast_prices[-1]:,.0f}",
                 delta=f"{((forecast_prices[-1] - train_data['Price'].iloc[-1]) / train_data['Price'].iloc[-1] * 100):.1f}%")
    
    # Seasonality decomposition
    st.markdown("#### 🔄 Seasonality Analysis")
    
    fig_decomp = go.Figure()
    
    # Trend
    fig_decomp.add_trace(go.Scatter(
        x=train_data['Date'][-365:],
        y=trend[-365:],
        mode='lines',
        name='Trend',
        line=dict(color='green')
    ))
    
    # Seasonality
    fig_decomp.add_trace(go.Scatter(
        x=train_data['Date'][-365:],
        y=seasonality[-365:],
        mode='lines',
        name='Seasonality',
        line=dict(color='orange'),
        yaxis='y2'
    ))
    
    fig_decomp.update_layout(
        title='Trend and Seasonality (Last 365 Days)',
        xaxis_title='Date',
        yaxis_title='Trend (Rp)',
        yaxis2=dict(title='Seasonality', overlaying='y', side='right'),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_decomp, use_container_width=True)

# ============================================================================
# TAB 5: TUTORIAL
# ============================================================================
with tab5:
    st.markdown("### 📚 Tutorial PyCaret untuk Pemula")
    
    st.markdown("""
    ## 🎓 Pengenalan PyCaret
    
    **PyCaret** adalah library AutoML open-source yang mempermudah machine learning workflow.
    
    ### 📦 Instalasi
    
    ```bash
    # Install PyCaret
    pip install pycaret
    
    # Untuk regression
    pip install pycaret[full]
    
    # Untuk specific module
    pip install pycaret[regression]
    pip install pycaret[classification]
    pip install pycaret[clustering]
    pip install pycaret[time_series]
    ```
    
    ### 🔰 Workflow Umum PyCaret
    
    Semua modul PyCaret mengikuti workflow yang konsisten:
    
    1. **Setup** - Initialize environment
    2. **Compare** - Compare multiple models
    3. **Create/Tune** - Create or tune specific model
    4. **Evaluate** - Evaluate model performance
    5. **Predict** - Make predictions
    6. **Save** - Save model for deployment
    
    ---
    
    ## 📈 1. Regression
    
    **Use Case:** Prediksi nilai kontinu (harga, yield, dll)
    
    ### Basic Example:
    """)
    
    st.code("""
from pycaret.regression import *
import pandas as pd

# Load data
data = pd.read_csv('crop_yield.csv')

# 1. Setup
reg = setup(data=data, 
           target='yield',
           session_id=123,
           normalize=True,
           transformation=True,
           remove_outliers=True,
           train_size=0.8,
           fold=5)

# 2. Compare models (auto-compare 15+ models)
best_models = compare_models(n_select=3, sort='R2')

# 3. Tune best model
tuned_rf = tune_model(best_models[0], optimize='R2')

# 4. Evaluate
evaluate_model(tuned_rf)

# 5. Predict on new data
predictions = predict_model(tuned_rf, data=new_data)

# 6. Save model
save_model(tuned_rf, 'yield_prediction_model')

# 7. Load model (for deployment)
loaded_model = load_model('yield_prediction_model')
    """, language='python')
    
    st.markdown("""
    ### Key Parameters:
    
    - `normalize=True` - Normalize features
    - `transformation=True` - Transform skewed features
    - `remove_outliers=True` - Remove outliers
    - `feature_selection=True` - Auto feature selection
    - `pca=True` - Apply PCA
    
    ---
    
    ## 🎯 2. Classification
    
    **Use Case:** Prediksi kategori (disease type, quality grade, dll)
    
    ### Basic Example:
    """)
    
    st.code("""
from pycaret.classification import *

# Load data
data = pd.read_csv('disease_data.csv')

# 1. Setup
clf = setup(data=data,
           target='disease_type',
           session_id=123,
           normalize=True,
           fix_imbalance=True,  # Handle imbalanced classes
           remove_outliers=True,
           train_size=0.8)

# 2. Compare models
best_models = compare_models(n_select=3, sort='Accuracy')

# 3. Create ensemble
ensemble = ensemble_model(best_models[0])

# 4. Tune
tuned_model = tune_model(ensemble)

# 5. Plot confusion matrix
plot_model(tuned_model, plot='confusion_matrix')

# 6. Plot feature importance
plot_model(tuned_model, plot='feature')

# 7. Predict
predictions = predict_model(tuned_model, data=new_data)

# 8. Save
save_model(tuned_model, 'disease_classifier')
    """, language='python')
    
    st.markdown("""
    ### Available Plots:
    
    - `confusion_matrix` - Confusion matrix
    - `auc` - ROC-AUC curve
    - `pr` - Precision-Recall curve
    - `feature` - Feature importance
    - `learning` - Learning curve
    - `calibration` - Calibration curve
    
    ---
    
    ## 🔵 3. Clustering
    
    **Use Case:** Segmentasi tanpa label (customer segmentation, farm grouping)
    
    ### Basic Example:
    """)
    
    st.code("""
from pycaret.clustering import *

# Load data
data = pd.read_csv('farmer_data.csv')

# 1. Setup
clu = setup(data=data,
           session_id=123,
           normalize=True,
           pca=True,
           pca_components=3)

# 2. Create K-Means model
kmeans = create_model('kmeans', num_clusters=4)

# 3. Assign clusters to data
data_with_clusters = assign_model(kmeans)

# 4. Plot clusters
plot_model(kmeans, plot='cluster')  # 2D cluster plot
plot_model(kmeans, plot='distribution')  # Distribution
plot_model(kmeans, plot='elbow')  # Elbow plot

# 5. Tune clusters
tuned_kmeans = tune_model(kmeans)

# 6. Save
save_model(kmeans, 'farmer_segmentation')
    """, language='python')
    
    st.markdown("""
    ### Available Algorithms:
    
    - `kmeans` - K-Means
    - `ap` - Affinity Propagation
    - `meanshift` - Mean Shift
    - `sc` - Spectral Clustering
    - `hclust` - Hierarchical Clustering
    - `dbscan` - DBSCAN
    
    ---
    
    ## 📉 4. Time Series
    
    **Use Case:** Forecasting (price, demand, production)
    
    ### Basic Example:
    """)
    
    st.code("""
from pycaret.time_series import *

# Load data
data = pd.read_csv('price_history.csv')

# 1. Setup
ts = setup(data=data,
          fh=30,  # Forecast horizon (30 days)
          fold=3,
          session_id=123)

# 2. Compare models
best_models = compare_models(n_select=3)

# 3. Create specific model
arima = create_model('arima')
prophet = create_model('prophet')

# 4. Tune
tuned_model = tune_model(best_models[0])

# 5. Finalize
final_model = finalize_model(tuned_model)

# 6. Predict future
predictions = predict_model(final_model, fh=30)

# 7. Plot forecast
plot_model(final_model, plot='forecast')
plot_model(final_model, plot='diagnostics')

# 8. Save
save_model(final_model, 'price_forecaster')
    """, language='python')
    
    st.markdown("""
    ### Available Models:
    
    - `naive` - Naive Forecaster
    - `arima` - ARIMA
    - `exp_smooth` - Exponential Smoothing
    - `prophet` - Facebook Prophet
    - `lr_cds_dt` - Linear Regression with Date Features
    
    ---
    
    ## 🎨 Advanced Features
    
    ### 1. Hyperparameter Tuning
    """)
    
    st.code("""
# Grid search
tuned = tune_model(model, 
                  optimize='R2',
                  n_iter=50,  # Number of iterations
                  search_library='scikit-learn',
                  search_algorithm='random')

# Custom grid
custom_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [5, 10, 15],
    'min_samples_split': [2, 5, 10]
}

tuned_custom = tune_model(model, custom_grid=custom_grid)
    """, language='python')
    
    st.markdown("""
    ### 2. Ensemble Methods
    """)
    
    st.code("""
# Bagging
bagged = ensemble_model(model, method='Bagging')

# Boosting
boosted = ensemble_model(model, method='Boosting')

# Voting (combine multiple models)
blended = blend_models([model1, model2, model3])

# Stacking
stacked = stack_models([model1, model2, model3], meta_model=model4)
    """, language='python')
    
    st.markdown("""
    ### 3. Model Interpretation
    """)
    
    st.code("""
# SHAP values
interpret_model(model)

# Feature importance
plot_model(model, plot='feature')

# Partial dependence
plot_model(model, plot='parameter')

# Learning curve
plot_model(model, plot='learning')
    """, language='python')
    
    st.markdown("""
    ### 4. Model Deployment
    """)
    
    st.code("""
# Save model
save_model(model, 'my_model')

# Load model
loaded_model = load_model('my_model')

# Deploy to AWS
deploy_model(model, 
            model_name='crop_predictor',
            platform='aws',
            authentication={'bucket': 'my-bucket'})

# Create API
from pycaret.utils import create_api
create_api(model, 'my_api')

# Create Docker
from pycaret.utils import create_docker
create_docker(model, 'my_docker_image')
    """, language='python')
    
    st.markdown("""
    ---
    
    ## 💡 Best Practices
    
    ### 1. Data Preparation
    - ✅ Clean missing values
    - ✅ Remove duplicates
    - ✅ Handle outliers
    - ✅ Encode categorical variables
    - ✅ Scale numerical features
    
    ### 2. Model Selection
    - ✅ Always use `compare_models()` first
    - ✅ Select top 3-5 models
    - ✅ Tune each model
    - ✅ Use ensemble methods
    - ✅ Cross-validate results
    
    ### 3. Evaluation
    - ✅ Use multiple metrics
    - ✅ Check for overfitting
    - ✅ Validate on holdout set
    - ✅ Interpret model predictions
    - ✅ Monitor model drift
    
    ### 4. Deployment
    - ✅ Save model artifacts
    - ✅ Version control models
    - ✅ Monitor performance
    - ✅ Retrain periodically
    - ✅ A/B test new models
    
    ---
    
    ## 🔗 Resources
    
    - 📖 [PyCaret Documentation](https://pycaret.gitbook.io/docs/)
    - 🎓 [PyCaret Tutorials](https://github.com/pycaret/pycaret/tree/master/tutorials)
    - 💬 [PyCaret Slack Community](https://pycaret.slack.com)
    - 🐙 [GitHub Repository](https://github.com/pycaret/pycaret)
    - 📺 [YouTube Channel](https://www.youtube.com/channel/UCxA1YTYJ9BEeo50lxyI_B3g)
    
    ---
    
    ## ⚠️ Common Issues
    
    ### Issue 1: Import Error
    ```python
    # Solution: Install specific module
    pip install pycaret[regression]
    ```
    
    ### Issue 2: Memory Error
    ```python
    # Solution: Reduce data size or use sampling
    setup(data=data.sample(frac=0.5), ...)
    ```
    
    ### Issue 3: Slow Training
    ```python
    # Solution: Reduce models or use turbo mode
    compare_models(turbo=True, n_select=3)
    ```
    
    ### Issue 4: Imbalanced Data
    ```python
    # Solution: Use fix_imbalance
    setup(data=data, fix_imbalance=True, ...)
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🤖 <strong>AgriSensa Tech - Machine Learning dengan PyCaret</strong></p>
    <p>AutoML untuk prediksi dan analisis data pertanian</p>
    <p style='font-size: 0.9rem;'>💡 Tip: Gunakan PyCaret untuk mempercepat development ML pipeline Anda!</p>
</div>
""", unsafe_allow_html=True)
