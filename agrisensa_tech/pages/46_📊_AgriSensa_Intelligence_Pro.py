
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from scipy import stats
import datetime

# Page Config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="AgriSensa Intelligence Pro",
    page_icon="🤖",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# HELPER FUNCTIONS
@st.cache_data
def load_data(file):
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file)
    except Exception as e:
        st.error(f"Gagal memuat file: {e}")
        return None

def detect_date_columns(df):
    date_cols = []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            date_cols.append(col)
        elif df[col].astype(str).str.match(r'^\d{4}-\d{2}-\d{2}').all(): # Simple check YYYY-MM-DD
            try:
                df[col] = pd.to_datetime(df[col])
                date_cols.append(col)
            except:
                pass
    return date_cols

# CUSTOM CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e5e7eb;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .kpi-val { font-size: 2rem; font-weight: bold; color: #6366f1; }
    .kpi-lbl { color: #6b7280; font-size: 0.9rem; }
    h1, h2, h3 { color: #4338ca; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown('<div class="main-header"><h1>🤖 AgriSensa Intelligence (Pro)</h1><p>Platform Analisis Data Pertanian Mandiri (Self-Service BI)</p></div>', unsafe_allow_html=True)

# SIDEBAR CONFIG
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload File Laporan (Excel/CSV)", type=["xlsx", "xls", "csv"])

# MAIN LOGIC
if uploaded_file is not None:
    # 1. LOAD DATA
    df = load_data(uploaded_file)
    
    if df is not None:
        # DATA PREVIEW (EXPANDER)
        with st.expander("🔍 Preview Data Mentah", expanded=False):
            st.dataframe(df, use_container_width=True)
            
        # TABS NAVIGATION
        tab1, tab2, tab3 = st.tabs(["📊 Visualisasi Data", "🔮 Auto-Forecasting", "⚠️ Deteksi Anomali"])
        
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # --- TAB 1: VISUALISASI ---
        with tab1:
            st.markdown("### 📈 Ringkasan Data (Profiling)")
            c1, c2, c3, c4 = st.columns(4)
            
            c1.markdown(f'<div class="kpi-card"><div class="kpi-val">{df.shape[0]:,}</div><div class="kpi-lbl">Total Baris</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="kpi-card"><div class="kpi-val">{df.shape[1]}</div><div class="kpi-lbl">Total Kolom</div></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="kpi-card"><div class="kpi-val">{len(num_cols)}</div><div class="kpi-lbl">Kolom Angka</div></div>', unsafe_allow_html=True)
            c4.markdown(f'<div class="kpi-card"><div class="kpi-val">{len(cat_cols)}</div><div class="kpi-lbl">Kolom Kategori</div></div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # CHART BUILDER INTERFACE
            col_settings, col_chart = st.columns([1, 3])
            
            with col_settings:
                st.markdown("### 🛠️ Chart Builder")
                chart_type = st.selectbox("Jenis Grafik", ["Bar Chart", "Line Chart", "Pie Chart", "Scatter Plot", "Area Chart", "Histogram"])
                x_axis = st.selectbox("Sumbu X (Kategori/Waktu)", options=df.columns)
                y_axis = st.selectbox("Sumbu Y (Nilai)", options=num_cols)
                color_dim = st.selectbox("Warna/Group (Opsional)", options=["None"] + cat_cols)
                if color_dim == "None": color_dim = None
                st.markdown("---")
                agg_func = st.selectbox("Agregasi Data", ["Sum (Total)", "Average (Rata-rata)", "Count (Jumlah Data)", "Raw (Tanpa Agregasi)"])

            # PLOTTING LOGIC
            with col_chart:
                st.markdown(f"### 🖼️ Visualisasi: {chart_type}")
                if agg_func != "Raw (Tanpa Agregasi)":
                    try:
                        group_cols = [x_axis]
                        if color_dim: group_cols.append(color_dim)
                        
                        if agg_func == "Sum (Total)": plot_df = df.groupby(group_cols)[y_axis].sum().reset_index()
                        elif agg_func == "Average (Rata-rata)": plot_df = df.groupby(group_cols)[y_axis].mean().reset_index()
                        elif agg_func == "Count (Jumlah Data)": plot_df = df.groupby(group_cols)[y_axis].count().reset_index()
                        
                        # Formatting title column if date
                        if pd.api.types.is_datetime64_any_dtype(plot_df[x_axis]):
                            plot_df = plot_df.sort_values(x_axis)
                    except:
                        plot_df = df
                else:
                    plot_df = df
                
                try:
                    if chart_type == "Bar Chart": fig = px.bar(plot_df, x=x_axis, y=y_axis, color=color_dim, barmode='group')
                    elif chart_type == "Line Chart": fig = px.line(plot_df, x=x_axis, y=y_axis, color=color_dim, markers=True)
                    elif chart_type == "Area Chart": fig = px.area(plot_df, x=x_axis, y=y_axis, color=color_dim)
                    elif chart_type == "Scatter Plot": fig = px.scatter(plot_df, x=x_axis, y=y_axis, color=color_dim, size=y_axis)
                    elif chart_type == "Pie Chart": fig = px.pie(plot_df, names=x_axis, values=y_axis, color=color_dim, hole=0.4)
                    elif chart_type == "Histogram": fig = px.histogram(df, x=x_axis, color=color_dim)
                    fig.update_layout(height=450, template="plotly_white")
                    st.plotly_chart(fig, use_container_width=True)
                except Exception as e:
                    st.error(f"Error: {e}")

        # --- TAB 2: FORECASTING ---
        with tab2:
            st.markdown("### 🔮 Peramal Masa Depan (Auto-Forecasting)")
            st.info("Otomatis mendeteksi tren waktu dan memprediksi 3-6 periode ke depan.")
            
            # Detect Date Column
            date_cols = detect_date_columns(df)
            
            if not date_cols:
                st.warning("⚠️ Tidak ditemukan kolom Tanggal/Waktu yang valid di file ini. Pastikan format YYYY-MM-DD.")
            elif not num_cols:
                st.warning("⚠️ Tidak ada kolom angka untuk diprediksi.")
            else:
                col_f1, col_f2 = st.columns(2)
                with col_f1:
                    date_col = st.selectbox("Pilih Kolom Waktu:", date_cols)
                with col_f2:
                    target_col = st.selectbox("Pilih Target Prediksi:", num_cols)
                    
                periods = st.slider("Jumlah Periode Prediksi:", 3, 12, 6)
                
                if st.button("🚀 Ramal Sekarang"):
                    # Process Data
                    df_fc = df.copy()
                    df_fc[date_col] = pd.to_datetime(df_fc[date_col])
                    # Aggregate by month/period logic - Simplified to ordinal sorting
                    df_fc = df_fc.groupby(date_col)[target_col].sum().reset_index().sort_values(date_col)
                    
                    df_fc['ordinal_date'] = df_fc[date_col].map(datetime.datetime.toordinal)
                    
                    X = df_fc[['ordinal_date']]
                    y = df_fc[target_col]
                    
                    model = LinearRegression()
                    model.fit(X, y)
                    r2 = model.score(X, y)
                    
                    # Future Dates
                    last_date = df_fc[date_col].max()
                    # Determine avg freq roughly
                    if len(df_fc) > 1:
                        avg_diff = (df_fc[date_col].iloc[-1] - df_fc[date_col].iloc[0]).days / len(df_fc)
                    else:
                        avg_diff = 30 # Default monthly
                    
                    future_dates = [last_date + datetime.timedelta(days=int(avg_diff)*i) for i in range(1, periods+1)]
                    future_ordinals = [[d.toordinal()] for d in future_dates]
                    
                    predictions = model.predict(future_ordinals)
                    
                    # Plot
                    fig_fc = px.line(df_fc, x=date_col, y=target_col, markers=True, title=f"Prediksi {target_col} (R²: {r2:.2f})")
                    fig_fc.add_scatter(x=future_dates, y=predictions, mode='lines+markers', name='Prediksi AI', line=dict(dash='dash', color='red'))
                    
                    st.plotly_chart(fig_fc, use_container_width=True)
                    st.success(f"Model berhasil memprediksi tren dengan akurasi arah trend: {r2*100:.1f}%.")
                    
                    if avg_diff < 40:
                        st.caption("ℹ️ Frekuensi data terdeteksi: Bulanan/Harian")
                    else:
                        st.caption("ℹ️ Frekuensi data terdeteksi: Jarang/Acak")

        # --- TAB 3: ANOMALY ---
        with tab3:
            st.markdown("### ⚠️ Detektif Anomali (Z-Score)")
            st.info("Mendeteksi data 'aneh' (Outlier) yang menyimpang jauh dari rata-rata statistik.")
            
            anom_target = st.selectbox("Pilih Kolom untuk Audit:", num_cols, key="anom_target")
            threshold = st.slider("Sensitivitas (Standar Deviasi)", 1.5, 3.5, 2.0, help="Semakin kecil angka, semakin sensitif mendeteksi anomali.")
            
            if st.button("🔍 Scan Anomali"):
                # Z-Score Logic
                df_anom = df.copy()
                col_data = df_anom[anom_target]
                z_scores = np.abs(stats.zscore(col_data))
                
                df_anom['Is_Anomaly'] = z_scores > threshold
                anomalies = df_anom[df_anom['Is_Anomaly'] == True]
                
                cnt = len(anomalies)
                pct = (cnt / len(df)) * 100
                
                col_a1, col_a2 = st.columns([3, 1])
                
                with col_a1:
                    # Scatter Plot with Color Highlight
                    x_axis_anom = df_anom.columns[0] # Default to first col (ID/Date usually)
                    fig_anom = px.scatter(df_anom, x=x_axis_anom, y=anom_target, color='Is_Anomaly', 
                                          title=f"Sebaran Data: {cnt} Anomali Terdeteksi",
                                          color_discrete_map={False: "blue", True: "red"})
                    st.plotly_chart(fig_anom, use_container_width=True)
                    
                with col_a2:
                    st.metric("Total Anomali", f"{cnt} Baris", f"{pct:.1f}% dari data")
                    if cnt > 0:
                        st.error("Ditemukan data mencurigakan!")
                    else:
                        st.success("Data bersih. Tidak ada penyimpangan ekstrem.")
                
                if cnt > 0:
                    st.write("#### 📝 Daftar Data Aneh:")
                    st.dataframe(anomalies.style.applymap(lambda x: 'background-color: #fca5a5', subset=[anom_target]))

else:
    # EMPTY STATE
    st.info("👋 **Selamat Datang di AgriSensa Intelligence Pro!**")
    st.markdown("""
    Silakan upload file **Excel (.xlsx)** atau **CSV** di sidebar.
    
    **Fitur Versi Pro:**
    - 📊 **Visualisasi**: Buat grafik instan.
    - 🔮 **Forecasting**: Prediksi panen/harga masa depan.
    - ⚠️ **Anomaly**: Audit data yang tidak wajar.
    """)
    
    # Generate Dummy Data
    if st.button("🔽 Gunakan Data Dummy Lengkap"):
        dates = pd.date_range(start="2023-01-01", periods=24, freq='M')
        # Create trending data with some noise and an anomaly
        base_val = np.linspace(10, 25, 24)
        noise = np.random.normal(0, 2, 24)
        values = base_val + noise
        values[10] = 50 # Anomaly outlier!
        
        df_dummy = pd.DataFrame({
            "Tanggal": dates,
            "Hasil_Panen_Ton": values,
            "Biaya_Operasional": np.random.randint(5, 15, 24) * 1000000,
            "Lokasi": ["Blok A"]*12 + ["Blok B"]*12
        })
        csv = df_dummy.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV Dummy", csv, "dummy_data_pro.csv", "text/csv")

# Footer
st.markdown("---")
st.caption("AgriSensa Intelligence v2.0 Pro - AI Powered Analytics")
