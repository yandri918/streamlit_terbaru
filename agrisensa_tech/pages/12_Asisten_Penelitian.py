# Asisten Penelitian Agronomi
# Advanced research assistant with multiple ML models and statistical analysis (ANOVA/RAK/RAL)
# Version: 2.1.0 (Fixed RAK Kelompok Selection - 2024-12-06)

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ML Imports
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

# Stats Imports
from scipy import stats

# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Asisten Penelitian v2.1", page_icon="🔬", layout="wide")

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================


# ==========================================
# 📐 STATISTICAL ENGINE (ANOVA & POST-HOC)
# ==========================================
def calculate_anova_ral(df, col_perlakuan, col_hasil):
    """
    Hitung ANOVA Rancangan Acak Lengkap (CRD)
    Sumber Keragaman: Perlakuan, Galat, Total
    """
    # 1. Prepare Data
    groups = df.groupby(col_perlakuan)[col_hasil]
    grand_mean = df[col_hasil].mean()
    n_total = len(df)
    n_treatments = df[col_perlakuan].nunique()
    
    # 2. Sum of Squares (JK)
    # FK (Faktor Koreksi)
    fk = (df[col_hasil].sum()**2) / n_total
    
    # JK Total
    jk_total = (df[col_hasil]**2).sum() - fk
    
    # JK Perlakuan
    jk_perlakuan = (groups.sum()**2 / groups.count()).sum() - fk
    
    # JK Galat
    jk_galat = jk_total - jk_perlakuan
    
    # 3. Degrees of Freedom (DB)
    db_perlakuan = n_treatments - 1
    db_total = n_total - 1
    db_galat = db_total - db_perlakuan
    
    # 4. Mean Square (KT)
    kt_perlakuan = jk_perlakuan / db_perlakuan
    kt_galat = jk_galat / db_galat
    
    # 5. F-Hitung
    f_hitung = kt_perlakuan / kt_galat
    
    # 6. P-Value (1 - CDF)
    p_value = 1 - stats.f.cdf(f_hitung, db_perlakuan, db_galat)
    
    # 7. CV (Koefisien Keragaman)
    cv = (np.sqrt(kt_galat) / grand_mean) * 100
    
    summary = {
        "SK": ["Perlakuan", "Galat", "Total"],
        "DB": [db_perlakuan, db_galat, db_total],
        "JK": [jk_perlakuan, jk_galat, jk_total],
        "KT": [kt_perlakuan, kt_galat, np.nan],
        "F-Hitung": [f_hitung, np.nan, np.nan],
        "P-Value": [p_value, np.nan, np.nan],
        "Signifikan": [p_value < 0.05, np.nan, np.nan]
    }
    
    return pd.DataFrame(summary), kt_galat, db_galat, cv

def calculate_anova_rak(df, col_perlakuan, col_kelompok, col_hasil):
    """
    Hitung ANOVA Rancangan Acak Kelompok (RCBD)
    Sumber Keragaman: Kelompok, Perlakuan, Galat, Total
    """
    # 1. Prereq
    n_total = len(df)
    n_kelompok = df[col_kelompok].nunique()
    n_perlakuan = df[col_perlakuan].nunique()
    grand_mean = df[col_hasil].mean()
    
    # FK
    fk = (df[col_hasil].sum()**2) / n_total
    
    # JK Total
    jk_total = (df[col_hasil]**2).sum() - fk
    
    # JK Kelompok
    jk_kelompok = (df.groupby(col_kelompok)[col_hasil].sum()**2 / n_perlakuan).sum() - fk
    
    # JK Perlakuan
    jk_perlakuan = (df.groupby(col_perlakuan)[col_hasil].sum()**2 / n_kelompok).sum() - fk
    
    # JK Galat
    jk_galat = jk_total - jk_kelompok - jk_perlakuan
    
    # DB
    db_kelompok = n_kelompok - 1
    db_perlakuan = n_perlakuan - 1
    db_total = n_total - 1
    db_galat = db_total - db_kelompok - db_perlakuan
    
    # KT
    kt_kelompok = jk_kelompok / db_kelompok
    kt_perlakuan = jk_perlakuan / db_perlakuan
    kt_galat = jk_galat / db_galat
    
    # F-Hitung
    f_kelompok = kt_kelompok / kt_galat
    f_perlakuan = kt_perlakuan / kt_galat
    
    # P-Value
    p_kelompok = 1 - stats.f.cdf(f_kelompok, db_kelompok, db_galat)
    p_perlakuan = 1 - stats.f.cdf(f_perlakuan, db_perlakuan, db_galat)
    
    # CV
    cv = (np.sqrt(kt_galat) / grand_mean) * 100
    
    summary = {
        "SK": ["Kelompok", "Perlakuan", "Galat", "Total"],
        "DB": [db_kelompok, db_perlakuan, db_galat, db_total],
        "JK": [jk_kelompok, jk_perlakuan, jk_galat, jk_total],
        "KT": [kt_kelompok, kt_perlakuan, kt_galat, np.nan],
        "F-Hitung": [f_kelompok, f_perlakuan, np.nan, np.nan],
        "P-Value": [p_kelompok, p_perlakuan, np.nan, np.nan],
        "Signifikan": [p_kelompok < 0.05, p_perlakuan < 0.05, np.nan, np.nan]
    }
    
    return pd.DataFrame(summary), kt_galat, db_galat, cv

def calculate_bnt(df, col_perlakuan, col_hasil, kt_galat, db_galat, alpha=0.05):
    """
    Uji Beda Nyata Terkecil (LSD/BNT)
    """
    mean_perlakuan = df.groupby(col_perlakuan)[col_hasil].mean().sort_values(ascending=False)
    n_ulangan = len(df) / df[col_perlakuan].nunique() # Asumsi ulangan sama (seimbang)
    
    # T-Table value
    t_val = stats.t.ppf(1 - alpha/2, db_galat)
    
    # BNT Value
    bnt_val = t_val * np.sqrt((2 * kt_galat) / n_ulangan)
    
    # Notasi Huruf logic
    means = mean_perlakuan.values
    labels = mean_perlakuan.index
    notasi = [''] * len(means)
    
    # Simple algorithm for notation (Greedy approach)
    # Note: Full recursive algorithm is complex, using simplified "significant diff check"
    
    # Init with 'a' for highest
    curr_char = 97 # 'a'
    
    # This is a simplified logic placeholder. 
    # Real BNJ grouping requires matrix overlap check.
    # For MVP: Just comparing each to the best.
    
    # Let's do a Pairwise Comparison Matrix instead, simpler and more informative
    matrix = []
    for i in range(len(means)):
        row = []
        for j in range(len(means)):
            diff = abs(means[i] - means[j])
            sig = "*" if diff > bnt_val else "ns"
            row.append(sig)
        matrix.append(row)
            
    df_matrix = pd.DataFrame(matrix, index=labels, columns=labels)
    
    return mean_perlakuan, bnt_val, df_matrix

# ==========================================
# 🤖 ML ENGINE (EXISTING)
# ==========================================
AVAILABLE_MODELS = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=1.0),
    "Lasso Regression": Lasso(alpha=1.0),
    "Polynomial Regression (deg=2)": "polynomial",
    "Decision Tree": DecisionTreeRegressor(max_depth=5, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, max_depth=3, random_state=42)
}

def train_and_evaluate_models(X, y, model_names):
    results = []
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    for model_name in model_names:
        if model_name == "Polynomial Regression (deg=2)":
            poly = PolynomialFeatures(degree=2)
            X_poly = poly.fit_transform(X)
            model = LinearRegression()
            model.fit(X_poly, y)
            y_pred = model.predict(X_poly)
            cv_scores = cross_val_score(model, X_poly, y, cv=5, scoring='r2')
        else:
            model = AVAILABLE_MODELS[model_name]
            model.fit(X_scaled, y)
            y_pred = model.predict(X_scaled)
            cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')
        
        results.append({
            'Model': model_name,
            'R² Score': r2_score(y, y_pred),
            'RMSE': np.sqrt(mean_squared_error(y, y_pred)),
            'CV Mean R²': cv_scores.mean()
        })
    return pd.DataFrame(results)

# ==========================================
# 🏗️ UI LAYOUT
# ==========================================
st.title("🔬 Asisten Penelitian Agronomi")
st.markdown("**Platform Analisis Data Pertanian Terpadu: Machine Learning & Statistika**")

# MAIN TABS
tab_ml, tab_stat, tab_regression = st.tabs([
    "🤖 Mode Machine Learning (Prediksi)", 
    "📊 Mode Statistika (RAL/RAK)",
    "📚 Teori Regresi & Visualisasi"
])

# -----------------
# TAB 1: MACHINE LEARNING
# -----------------
with tab_ml:
    st.header("Prediksi & Pemodelan (ML)")
    st.info("Gunakan mode ini untuk memprediksi hasil panen berdasarkan variabel input (NPK, Cuaca, dll).")
    
    ml_data_source = st.radio("Sumber Data ML:", ["Sample (Yield vs NPK)", "Upload CSV"], horizontal=True)
    
    if ml_data_source == "Sample (Yield vs NPK)":
        # Generate dummy
        np.random.seed(42)
        N = np.random.uniform(50, 200, 100)
        P = np.random.uniform(20, 100, 100)
        K = np.random.uniform(30, 150, 100)
        yield_val = 2000 + 15*N + 10*P + 8*K + np.random.normal(0, 300, 100)
        df_ml = pd.DataFrame({'N': N, 'P': P, 'K': K, 'Yield': yield_val})
    else:
        uploaded = st.file_uploader("Upload CSV (ML)", type='csv', key='ml_upload')
        if uploaded:
            df_ml = pd.read_csv(uploaded)
        else:
            df_ml = None
            
    if df_ml is not None:
        st.dataframe(df_ml.head(5), use_container_width=True)
        col1, col2 = st.columns(2)
        target = col1.selectbox("Target (Y)", df_ml.columns)
        feats = col2.multiselect("Features (X)", [c for c in df_ml.columns if c!=target], default=[c for c in df_ml.columns if c!=target])
        
        if st.button("Jalankan Model ML"):
            with st.spinner("Training models..."):
                res = train_and_evaluate_models(df_ml[feats].values, df_ml[target].values, AVAILABLE_MODELS.keys())
                res_sorted = res.sort_values('R² Score', ascending=False)
                
                # Best model info
                best_model = res_sorted.iloc[0]
                best_r2 = best_model['R² Score']
                best_name = best_model['Model']
                
                # Display results
                st.subheader("📊 Hasil Analisis ML")
                
                col_res1, col_res2 = st.columns([2, 1])
                
                with col_res1:
                    st.dataframe(res_sorted, use_container_width=True)
                    
                with col_res2:
                    st.metric("Model Terbaik", best_name)
                    st.metric("Akurasi (R²)", f"{best_r2:.3f}")
                    
                    # Interpretation
                    if best_r2 >= 0.9:
                        st.success("🎯 Excellent! Model sangat akurat")
                    elif best_r2 >= 0.7:
                        st.info("✅ Good! Model cukup reliable")
                    elif best_r2 >= 0.5:
                        st.warning("⚠️ Fair. Perlu improvement")
                    else:
                        st.error("❌ Poor. Data mungkin tidak linear")
                
                # Chart
                fig = px.bar(res_sorted, x='Model', y='R² Score', title="Perbandingan Akurasi Model", 
                            color='R² Score', color_continuous_scale='Viridis')
                st.plotly_chart(fig, use_container_width=True)
                
                # 💡 INSIGHTS SECTION
                st.divider()
                st.subheader("💡 Insight & Rekomendasi")
                
                # Feature Importance (for tree-based models)
                if "Random Forest" in res_sorted['Model'].values:
                    from sklearn.ensemble import RandomForestRegressor
                    rf = RandomForestRegressor(n_estimators=100, random_state=42)
                    rf.fit(df_ml[feats].values, df_ml[target].values)
                    
                    importance_df = pd.DataFrame({
                        'Feature': feats,
                        'Importance': rf.feature_importances_
                    }).sort_values('Importance', ascending=False)
                    
                    col_ins1, col_ins2 = st.columns(2)
                    
                    with col_ins1:
                        st.markdown("**🔍 Faktor Paling Berpengaruh:**")
                        fig_imp = px.bar(importance_df, x='Importance', y='Feature', orientation='h',
                                        title="Feature Importance (Random Forest)", color='Importance')
                        st.plotly_chart(fig_imp, use_container_width=True)
                        
                    with col_ins2:
                        st.markdown("**📈 Interpretasi:**")
                        top_feature = importance_df.iloc[0]['Feature']
                        top_importance = importance_df.iloc[0]['Importance']
                        
                        st.write(f"• **{top_feature}** adalah faktor paling dominan ({top_importance*100:.1f}%)")
                        
                        if len(importance_df) > 1:
                            second_feature = importance_df.iloc[1]['Feature']
                            st.write(f"• **{second_feature}** juga berpengaruh signifikan")
                        
                        # Recommendations
                        st.markdown("**🎯 Rekomendasi:**")
                        st.write(f"1. Fokus optimasi pada **{top_feature}**")
                        st.write(f"2. Monitor perubahan **{top_feature}** secara berkala")
                        if best_r2 < 0.8:
                            st.write("3. Pertimbangkan tambah data atau fitur baru")
                
                # Model Selection Advice
                st.divider()
                st.markdown("**🤖 Pemilihan Model:**")
                
                if best_name in ["Random Forest", "Gradient Boosting"]:
                    st.info("✅ Model ensemble (RF/GB) cocok untuk data kompleks dengan interaksi non-linear")
                elif best_name in ["Linear Regression", "Ridge", "Lasso"]:
                    st.info("✅ Model linear cocok untuk hubungan sederhana dan interpretasi mudah")
                elif best_name == "Polynomial Regression (deg=2)":
                    st.info("✅ Polynomial cocok untuk hubungan kuadratik (parabola)")
                
                # Data Quality Check
                st.markdown("**📊 Kualitas Data:**")
                col_qual1, col_qual2, col_qual3 = st.columns(3)
                
                with col_qual1:
                    n_samples = len(df_ml)
                    st.metric("Jumlah Data", n_samples)
                    if n_samples < 50:
                        st.caption("⚠️ Data terlalu sedikit")
                    else:
                        st.caption("✅ Cukup untuk training")
                        
                with col_qual2:
                    n_features = len(feats)
                    st.metric("Jumlah Features", n_features)
                    if n_features > n_samples / 10:
                        st.caption("⚠️ Terlalu banyak fitur")
                    else:
                        st.caption("✅ Rasio baik")
                        
                with col_qual3:
                    cv_std = res_sorted.iloc[0].get('CV Std R²', 0)
                    if cv_std > 0.1:
                        st.metric("Konsistensi", "Low", delta="Perlu validasi")
                    else:
                        st.metric("Konsistensi", "High", delta="Model stabil")

# -----------------
# TAB 2: STATISTIKA
# -----------------
with tab_stat:
    st.header("Rancangan Percobaan (Experimental Design)")
    st.info("Gunakan mode ini untuk analisis ANOVA (Sidik Ragam) pada eksperimen RAL atau RAK.")
    
    stat_source = st.radio("Sumber Data Statistik:", ["Sample RAL (Sederhana)", "Sample RAK (Kompleks Multi-Var)", "Upload CSV"], horizontal=True, key='stat_src')
    
    if stat_source == "Sample RAL (Sederhana)":
        data_stat = {
            'Perlakuan': ['P0', 'P0', 'P0', 'P1', 'P1', 'P1', 'P2', 'P2', 'P2', 'P3', 'P3', 'P3'],
            'Ulangan': [1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3],
            'Hasil_Tan': [12.5, 13.0, 12.8, 15.2, 15.5, 15.0, 18.5, 18.2, 18.8, 16.0, 16.2, 16.5]
        }
        df_stat = pd.DataFrame(data_stat)
        default_target = ['Hasil_Tan']
        
    elif stat_source == "Sample RAK (Kompleks Multi-Var)":
        # Generate Complex Dataset: Uji Efektivitas NPK pada Cabai
        # 5 Perlakuan, 4 Kelompok
        treatments = ['K0 (Kontrol)', 'K1 (NPK A)', 'K2 (NPK B)', 'K3 (NPK C)', 'K4 (NPK Premium)']
        blocks = [1, 2, 3, 4]
        
        rows = []
        np.random.seed(42)
        
        for t_idx, treat in enumerate(treatments):
            # Base effect for treatment (increasing logic)
            base_effect = t_idx * 2 
            
            for bird in blocks:
                # Block effect (soil fertility gradient)
                block_effect = bird * 0.5
                noise = np.random.normal(0, 1)
                
                rows.append({
                    'Perlakuan': treat,
                    'Kelompok': bird,
                    # Variable 1: Vegetative (Height) - Sig
                    'Tinggi_Tanaman_cm': 40 + (base_effect * 3) + block_effect + np.random.normal(0, 2),
                    # Variable 2: Generative (Fruit Count) - Sig
                    'Jml_Buah_per_Tan': 15 + (base_effect * 1.5) + np.random.normal(0, 3),
                    # Variable 3: Weight (Yield) - Very Sig
                    'Bobot_Buah_g': 10 + (base_effect * 0.8) + block_effect + np.random.normal(0, 1),
                    # Variable 4: Quality (Brix) - Not Sig (Treatment doesn't affect sweetness much)
                    'Kadar_Gula_Brix': 5 + np.random.normal(0, 0.5), # Flat base
                    # Variable 5: Disease Index - Sig (Negative correlation)
                    'Intensitas_Penyakit_%': max(0, 20 - (base_effect * 2) + np.random.normal(0, 2))
                })
        
        df_stat = pd.DataFrame(rows)
        default_target = ['Tinggi_Tanaman_cm', 'Bobot_Buah_g', 'Kadar_Gula_Brix']
        
    else:
        uploaded_stat = st.file_uploader("Upload CSV (Format: Perlakuan, Kelompok/Ulangan, Hasil)", type='csv', key='stat_upload')
        if uploaded_stat:
            df_stat = pd.read_csv(uploaded_stat)
            default_target = []
        else:
            df_stat = None
            default_target = []
            
    if df_stat is not None:
        st.write("Preview Data:")
        st.dataframe(df_stat.head(), use_container_width=True)
        
        # Config
        st.subheader("⚙️ Konfigurasi Desain")
        col_design1, col_design2 = st.columns(2)
        
        design_type = col_design1.selectbox("Tipe Rancangan", ["RAL (Rancangan Acak Lengkap)", "RAK (Rancangan Acak Kelompok)"])
        
        c_perlakuan = col_design1.selectbox("Kolom Perlakuan", df_stat.columns)
        
        if design_type == "RAK (Rancangan Acak Kelompok)":
            kelompok_options = [c for c in df_stat.columns if c != c_perlakuan]
            c_kelompok = col_design1.selectbox("Kolom Kelompok/Blok", kelompok_options, index=0 if kelompok_options else None)
        else:
            c_kelompok = None
            
        # MULTI-SELECT TARGET
        available_targets = [c for c in df_stat.columns if c not in [c_perlakuan, c_kelompok]]
        # Filter default_target to only include columns that exist in available_targets
        valid_defaults = [t for t in default_target if t in available_targets] if default_target else []
        
        c_hasil_list = col_design2.multiselect(
            "Pilih Variabel Target (Y) - Bisa Lebih dari 1:",
            available_targets,
            default=valid_defaults if valid_defaults else None
        )
            
        if st.button("📊 Hitung Batch Analysis (Semua Variabel)", type="primary"):
            if not c_hasil_list:
                st.error("Pilih setidaknya satu variabel target.")
                st.stop()
            
            # Validation for RAK design
            if design_type == "RAK (Rancangan Acak Kelompok)" and c_kelompok is None:
                st.error("⚠️ Untuk desain RAK, Anda harus memilih Kolom Kelompok/Blok!")
                st.stop()
                
            st.divider()
            
            # DEBUG OUTPUT
            with st.expander("🔧 Debug: Configuration Values", expanded=False):
                st.write(f"**Design Type:** {design_type}")
                st.write(f"**c_perlakuan:** {c_perlakuan}")
                st.write(f"**c_kelompok:** {c_kelompok}")
                st.write(f"**c_hasil_list:** {c_hasil_list}")
                st.write(f"**Available columns:** {list(df_stat.columns)}")
            
            summary_results = []
            
            # 🔄 LOOP OVER TARGETS
            for idx, c_hasil in enumerate(c_hasil_list):
                st.markdown(f"### 📌 Analisis Variabel {idx+1}: {c_hasil}")
                
                with st.expander(f"Detail Hasil: {c_hasil}", expanded=(idx==0)):
                    try:
                        # 1. ANOVA Analysis
                        if design_type == "RAL":
                            df_anova, kt_galat, db_galat, cv = calculate_anova_ral(df_stat, c_perlakuan, c_hasil)
                            p_val = df_anova.loc[0, 'P-Value']
                        else:
                            df_anova, kt_galat, db_galat, cv = calculate_anova_rak(df_stat, c_perlakuan, c_kelompok, c_hasil)
                            p_val = df_anova.loc[1, 'P-Value']
                        
                        is_sig = p_val < 0.05
                        sig_label = "SIGNIFIKAN (Nyata)" if is_sig else "NON-SIGNIFIKAN (Tidak Nyata)"
                        
                        # Add to summary list
                        summary_results.append({
                            "Variabel": c_hasil,
                            "F-Hitung": df_anova.loc[0 if design_type=="RAL" else 1, 'F-Hitung'],
                            "P-Value": p_val,
                            "Kesimpulan": sig_label,
                            "CV (%)": cv
                        })
                        
                        col_a1, col_a2 = st.columns([2, 1])
                        with col_a1:
                            st.write("**Tabel ANOVA:**")
                            st.dataframe(df_anova.style.highlight_between(subset='P-Value', left=0, right=0.05, color='#d4edda'), use_container_width=True)
                        with col_a2:
                            st.metric("Status Hipotesis", sig_label, delta="Tolak H0" if is_sig else "Terima H0", delta_color="normal" if is_sig else "off")
                            st.caption(f"CV: {cv:.2f}%")

                        # 2. Post-Hoc (If Sig) or Just Plot
                        col_viz1, col_viz2 = st.columns(2)
                        
                        # Barplot mean
                        mean_df = df_stat.groupby(c_perlakuan)[c_hasil].agg(['mean', 'std']).reset_index()
                        fig_bar = px.bar(mean_df, x=c_perlakuan, y='mean', error_y='std', title=f"Rata-rata {c_hasil}", color=c_perlakuan)
                        col_viz1.plotly_chart(fig_bar, use_container_width=True)
                        
                        if is_sig:
                            col_viz2.success("✅ Uji Lanjut BNT 5% (Post-Hoc)")
                            means, bnt_val, matrix = calculate_bnt(df_stat, c_perlakuan, c_hasil, kt_galat, db_galat)
                            col_viz2.write(f"**Nilai Beda Nyata (BNT): {bnt_val:.3f}**")
                            col_viz2.dataframe(means.to_frame(name="Rata-rata").style.background_gradient(cmap="Greens"), use_container_width=True)
                        else:
                            col_viz2.info("ℹ️ Tidak ada uji lanjut karena P-Value > 0.05")
                            
                    except Exception as e:
                        import traceback
                        error_detail = str(e) if str(e) else traceback.format_exc()
                        st.error(f"Error pada variabel {c_hasil}: {error_detail}")
                        with st.expander("Debug Info"):
                            st.code(traceback.format_exc())

            # 🏁 FINAL SUMMARY TABLE
            st.divider()
            st.subheader("📝 Ringkasan Eksekutif (Batch Report)")
            df_sums = pd.DataFrame(summary_results)
            
            if not df_sums.empty:
                st.dataframe(
                    df_sums.style.applymap(lambda v: 'color: green; font-weight: bold' if v == 'SIGNIFIKAN (Nyata)' else 'color: gray', subset=['Kesimpulan']),
                    use_container_width=True
                )
            else:
                st.warning("⚠️ Tidak ada hasil analisis yang berhasil dihitung. Periksa visualisasi error di atas.")

# -----------------
# TAB 3: TEORI REGRESI
# -----------------
with tab_regression:
    st.header("📚 Teori Regresi Linear & Aplikasi Ekonomi Pertanian")
    st.info("Tab ini menjelaskan konsep regresi linear, dari dasar hingga lanjutan, dengan visualisasi dan aplikasi praktis dalam ekonomi & bisnis pertanian.")
    
    # Sub-tabs for better organization (9 sub-tabs - Added CLRM)
    subtab_clrm, subtab_simple, subtab_multiple, subtab_inference, subtab_timeseries, subtab_chisquare, subtab_bayes, subtab_decision, subtab_viz = st.tabs([
        "🎓 CLRM & Gauss-Markov",
        "📖 Regresi Sederhana", 
        "🔢 Regresi Berganda",
        "📊 Inferensia OLS",
        "📈 Analisis Runtun Waktu",
        "🔲 Uji Chi-Square",
        "🎲 Teorema Bayes",
        "🎯 Teori Keputusan",
        "🎨 Visualisasi & Praktik"
    ])
    
    # ===== SUB-TAB 0: CLRM ASSUMPTIONS & GAUSS-MARKOV =====
    with subtab_clrm:
        st.subheader("🎓 Classical Linear Regression Model (CLRM)")
        
        st.markdown("""
        ## 📐 CLASSICAL LINEAR REGRESSION MODEL (CLRM)
        
        ### Apa itu CLRM?
        
        **CLRM** adalah fondasi teoritis dari analisis regresi linear. Model ini mendefinisikan **asumsi-asumsi** yang harus dipenuhi agar estimator OLS (Ordinary Least Squares) memiliki sifat-sifat optimal.
        
        ---
        
        ### 🎯 Asumsi-Asumsi CLRM
        
        #### **Asumsi 1: Linearity in Parameters**
        
        Model harus **linear dalam parameter** (β), bukan necessarily linear dalam variabel:
        
        $$Y_i = \\beta_0 + \\beta_1 X_{i1} + \\beta_2 X_{i2} + ... + \\beta_k X_{ik} + u_i$$
        
        **Contoh VALID:**
        - $Y = \\beta_0 + \\beta_1 X + \\beta_2 X^2 + u$ ✅ (Linear dalam β)
        - $Y = \\beta_0 + \\beta_1 \\ln(X) + u$ ✅ (Linear dalam β)
        
        **Contoh TIDAK VALID:**
        - $Y = \\beta_0 + X^{\\beta_1} + u$ ❌ (Non-linear dalam β)
        
        **Aplikasi Pertanian:**
        ```
        Yield = β₀ + β₁(NPK) + β₂(NPK²) + u
        ```
        Ini valid karena linear dalam β₁ dan β₂, meskipun ada NPK².
        
        ---
        
        #### **Asumsi 2: Random Sampling**
        
        Data harus merupakan **random sample** dari populasi:
        
        $$(Y_i, X_{i1}, X_{i2}, ..., X_{ik}) \\text{ untuk } i=1,2,...,n$$
        
        **Mengapa Penting:**
        - Menghindari selection bias
        - Memastikan sampel representatif
        - Validitas inferensi statistik
        
        **Contoh Pelanggaran:**
        - ❌ Hanya survey petani sukses (survivorship bias)
        - ❌ Hanya ambil data dari satu desa (tidak representatif)
        - ❌ Self-selection (hanya petani yang mau ikut survey)
        
        **Best Practice:**
        - ✅ Stratified random sampling
        - ✅ Cluster sampling dengan randomisasi
        - ✅ Systematic sampling dengan random start
        
        ---
        
        #### **Asumsi 3: No Perfect Multicollinearity**
        
        Tidak ada variabel independen yang **perfectly correlated**:
        
        $$\\text{rank}(X) = k+1$$
        
        **Multicollinearity Perfect (FATAL):**
        ```python
        # Contoh: Luas Lahan (ha) dan Luas Lahan (m²)
        X₁ = Luas_ha
        X₂ = Luas_m2 = 10000 × Luas_ha  # Perfect correlation!
        ```
        
        **Dampak:**
        - Koefisien tidak bisa dihitung (matrix singular)
        - Standard error → ∞
        - Model tidak estimable
        
        **Multicollinearity Tinggi (PROBLEM):**
        ```python
        # Contoh: Pupuk N dan Pupuk Urea
        Correlation(N, Urea) = 0.95  # Sangat tinggi
        ```
        
        **Deteksi: VIF (Variance Inflation Factor)**
        
        $$VIF_j = \\frac{1}{1 - R^2_j}$$
        
        **Interpretasi:**
        - VIF < 5: ✅ OK
        - 5 ≤ VIF < 10: ⚠️ Moderate
        - VIF ≥ 10: ❌ Severe
        
        **Solusi:**
        1. Drop salah satu variabel yang berkorelasi
        2. Combine variables (e.g., create NPK index)
        3. Ridge/Lasso regression
        4. Principal Component Analysis (PCA)
        
        ---
        
        #### **Asumsi 4: Zero Conditional Mean**
        
        **Expected value** dari error term adalah nol untuk semua nilai X:
        
        $$E(u_i | X_{i1}, X_{i2}, ..., X_{ik}) = 0$$
        
        **Implikasi:**
        - Error tidak sistematis
        - Tidak ada omitted variable bias
        - Tidak ada measurement error dalam X
        
        **Contoh Pelanggaran:**
        
        **Case 1: Omitted Variable**
        ```
        True Model: Yield = β₀ + β₁(NPK) + β₂(Rainfall) + u
        Estimated:  Yield = β₀ + β₁(NPK) + v
        
        Jika Rainfall berkorelasi dengan NPK:
        → E(v|NPK) ≠ 0
        → β̂₁ biased!
        ```
        
        **Case 2: Simultaneity**
        ```
        Demand: Q = α₀ + α₁P + u₁
        Supply: Q = β₀ + β₁P + u₂
        
        P dan u₁ berkorelasi (endogeneity)
        → E(u₁|P) ≠ 0
        → α̂₁ biased!
        ```
        
        **Solusi:**
        - Include all relevant variables
        - Use instrumental variables (IV)
        - Fixed effects / Random effects
        - Difference-in-differences
        
        ---
        
        #### **Asumsi 5: Homoscedasticity**
        
        **Variance** dari error term konstan untuk semua observasi:
        
        $$Var(u_i | X_{i1}, X_{i2}, ..., X_{ik}) = \\sigma^2$$
        
        **Visualisasi:**
        
        **Homoscedastic (✅):**
        ```
        Residuals
            |  ●  ●  ●  ●
            | ● ● ● ● ● ●
        ----+-------------
            | ● ● ● ● ● ●
            |  ●  ●  ●  ●
                Fitted Values
        ```
        
        **Heteroscedastic (❌):**
        ```
        Residuals
            |          ●  ●
            |       ●  ●  ●
        ----+-------------
            | ● ● ●
            |● ●
                Fitted Values
        ```
        
        **Contoh Pertanian:**
        ```
        Model: Profit = β₀ + β₁(Farm_Size) + u
        
        Problem: Variance profit lebih besar untuk farm besar
        → Heteroscedasticity!
        ```
        
        **Deteksi:**
        
        **1. Breusch-Pagan Test**
        ```
        H₀: Homoscedasticity
        H₁: Heteroscedasticity
        
        Test statistic: LM = n × R²
        Distribution: χ²(k)
        ```
        
        **2. White Test**
        ```
        More general (tidak assume functional form)
        ```
        
        **Dampak Heteroscedasticity:**
        - β̂ still unbiased ✅
        - β̂ NOT efficient ❌
        - Standard errors WRONG ❌
        - t-tests, F-tests INVALID ❌
        
        **Solusi:**
        1. **Weighted Least Squares (WLS)**
        2. **Robust Standard Errors** (Huber-White)
        3. **Transform variables** (log, sqrt)
        4. **Generalized Least Squares (GLS)**
        
        ---
        
        #### **Asumsi 6: No Autocorrelation**
        
        Error terms tidak berkorelasi satu sama lain:
        
        $$Cov(u_i, u_j | X) = 0 \\text{ untuk } i \\neq j$$
        
        **Relevan untuk:**
        - Time series data
        - Panel data
        - Spatial data
        
        **Contoh:**
        ```
        Model: Price_t = β₀ + β₁(Supply_t) + u_t
        
        Problem: u_t berkorelasi dengan u_{t-1}
        → Autocorrelation!
        ```
        
        **Deteksi: Durbin-Watson Test**
        
        $$DW = \\frac{\\sum_{t=2}^{n}(\\hat{u}_t - \\hat{u}_{t-1})^2}{\\sum_{t=1}^{n}\\hat{u}_t^2}$$
        
        **Interpretasi:**
        - DW ≈ 2: No autocorrelation ✅
        - DW < 2: Positive autocorrelation ❌
        - DW > 2: Negative autocorrelation ❌
        
        **Solusi:**
        1. Add lagged dependent variable
        2. Cochrane-Orcutt procedure
        3. Newey-West standard errors
        4. ARIMA models
        
        ---
        
        #### **Asumsi 7: Normality of Errors**
        
        Error term mengikuti **distribusi normal**:
        
        $$u_i \\sim N(0, \\sigma^2)$$
        
        **Catatan Penting:**
        - Asumsi ini **TIDAK** diperlukan untuk unbiasedness
        - Diperlukan untuk **exact inference** (t-test, F-test)
        - Dengan sampel besar (n > 30), CLT berlaku → asymptotic normality
        
        **Deteksi:**
        
        **1. Jarque-Bera Test**
        ```
        H₀: Errors normally distributed
        
        JB = n/6 × (S² + (K-3)²/4)
        
        S = Skewness
        K = Kurtosis
        ```
        
        **2. Q-Q Plot**
        ```
        Plot quantiles of residuals vs theoretical normal quantiles
        Should be straight line if normal
        ```
        
        **Dampak Non-Normality:**
        - β̂ still unbiased ✅
        - With large n, inference still valid (CLT) ✅
        - With small n, t-tests may be invalid ❌
        
        **Solusi:**
        1. Transform Y (log, Box-Cox)
        2. Use bootstrap for inference
        3. Robust regression methods
        4. Increase sample size
        
        ---
        
        ### 🏆 Gauss-Markov Theorem
        
        **Teorema:**
        
        Jika asumsi CLRM 1-5 terpenuhi, maka estimator OLS adalah **BLUE**:
        
        - **B**est
        - **L**inear
        - **U**nbiased
        - **E**stimator
        
        **Artinya:**
        
        1. **Unbiased**: $E(\\hat{\\beta}) = \\beta$
        2. **Linear**: $\\hat{\\beta}$ adalah linear combination dari Y
        3. **Best**: Memiliki variance terkecil di antara semua linear unbiased estimators
        
        **Mathematically:**
        
        $$Var(\\hat{\\beta}_{OLS}) \\leq Var(\\tilde{\\beta})$$
        
        untuk semua linear unbiased estimator $\\tilde{\\beta}$.
        
        **Implikasi Praktis:**
        
        ✅ OLS adalah metode terbaik (paling efisien) jika asumsi terpenuhi
        
        ❌ Jika asumsi dilanggar:
        - Heteroscedasticity → WLS lebih baik
        - Autocorrelation → GLS lebih baik
        - Non-normality → MLE bisa lebih baik
        
        ---
        
        ### 📊 Matrix Notation (Advanced)
        
        **Model dalam bentuk matrix:**
        
        $$\\mathbf{Y} = \\mathbf{X}\\boldsymbol{\\beta} + \\mathbf{u}$$
        
        Dimana:
        ```
        Y = [Y₁, Y₂, ..., Yₙ]ᵀ     (n × 1)
        
        X = [1  X₁₁  X₁₂  ...  X₁ₖ]
            [1  X₂₁  X₂₂  ...  X₂ₖ]
            [⋮   ⋮    ⋮   ⋱    ⋮ ]
            [1  Xₙ₁  Xₙ₂  ...  Xₙₖ]  (n × k+1)
        
        β = [β₀, β₁, β₂, ..., βₖ]ᵀ   (k+1 × 1)
        
        u = [u₁, u₂, ..., uₙ]ᵀ       (n × 1)
        ```
        
        **OLS Estimator:**
        
        $$\\hat{\\boldsymbol{\\beta}} = (\\mathbf{X}'\\mathbf{X})^{-1}\\mathbf{X}'\\mathbf{Y}$$
        
        **Variance-Covariance Matrix:**
        
        $$Var(\\hat{\\boldsymbol{\\beta}}) = \\sigma^2(\\mathbf{X}'\\mathbf{X})^{-1}$$
        
        **Estimator untuk σ²:**
        
        $$\\hat{\\sigma}^2 = \\frac{\\mathbf{u}'\\mathbf{u}}{n-k-1} = \\frac{SSE}{n-k-1}$$
        
        **Standard Errors:**
        
        $$SE(\\hat{\\beta}_j) = \\sqrt{\\hat{\\sigma}^2 \\times [(\\mathbf{X}'\\mathbf{X})^{-1}]_{jj}}$$
        
        ---
        
        ### 🎯 Checklist Asumsi CLRM
        
        Gunakan checklist ini untuk setiap analisis regresi:
        
        | Asumsi | Test | Action if Violated |
        |--------|------|-------------------|
        | 1. Linearity | Residual plot | Transform variables, add polynomial terms |
        | 2. Random Sampling | Research design | Cannot fix post-hoc, acknowledge limitation |
        | 3. No Multicollinearity | VIF | Drop variables, PCA, Ridge/Lasso |
        | 4. Zero Conditional Mean | Theory, IV test | Add variables, use IV, FE/RE |
        | 5. Homoscedasticity | BP test, White test | WLS, robust SE |
        | 6. No Autocorrelation | DW test | Add lags, Newey-West SE |
        | 7. Normality | JB test, Q-Q plot | Transform Y, bootstrap, robust methods |
        
        ---
        
        ### 💡 Practical Implications
        
        **Untuk Penelitian Pertanian:**
        
        1. **Production Function Analysis**
           - Check for diminishing returns (polynomial terms)
           - Test for heteroscedasticity (larger farms = larger variance)
           - Consider spatial autocorrelation
        
        2. **Price Analysis**
           - Time series → check autocorrelation
           - Seasonal patterns → add dummy variables
           - Volatility clustering → GARCH models
        
        3. **Adoption Studies**
           - Selection bias → use IV or propensity score matching
           - Omitted variables → include farm characteristics
           - Heterogeneous effects → interaction terms
        
        4. **Impact Evaluation**
           - Endogeneity → difference-in-differences, RDD
           - Spillover effects → spatial models
           - Panel data → fixed effects
        
        ---
        
        ### 📚 Further Reading
        
        **Classic Texts:**
        1. Wooldridge, J. M. (2020). *Introductory Econometrics: A Modern Approach*
        2. Greene, W. H. (2018). *Econometric Analysis*
        3. Stock, J. H., & Watson, M. W. (2020). *Introduction to Econometrics*
        
        **Agricultural Economics:**
        1. Debertin, D. L. (2012). *Agricultural Production Economics*
        2. Doll, J. P., & Orazem, F. (1984). *Production Economics: Theory with Applications*
        
        **Online Resources:**
        - [MIT OpenCourseWare: Econometrics](https://ocw.mit.edu)
        - [Econometrics Academy](https://sites.google.com/site/econometricsacademy/)
        """)
        
        # Interactive VIF Calculator
        st.divider()
        st.subheader("🧮 Interactive VIF Calculator")
        
        st.markdown("""
        Upload your data to calculate VIF for multicollinearity detection:
        """)
        
        vif_file = st.file_uploader("Upload CSV with independent variables", type='csv', key='vif_upload')
        
        if vif_file:
            df_vif = pd.read_csv(vif_file)
            st.write("**Data Preview:**")
            st.dataframe(df_vif.head(), use_container_width=True)
            
            numeric_cols = df_vif.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) >= 2:
                selected_vars = st.multiselect("Select variables for VIF calculation:", numeric_cols, default=numeric_cols[:min(5, len(numeric_cols))])
                
                if len(selected_vars) >= 2:
                    if st.button("Calculate VIF"):
                        try:
                            from statsmodels.stats.outliers_influence import variance_inflation_factor
                            
                            X_vif = df_vif[selected_vars].dropna()
                            
                            vif_data = pd.DataFrame()
                            vif_data["Variable"] = selected_vars
                            vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) for i in range(len(selected_vars))]
                            vif_data["Status"] = vif_data["VIF"].apply(
                                lambda x: "✅ OK" if x < 5 else ("⚠️ Moderate" if x < 10 else "❌ Severe")
                            )
                            
                            st.write("**VIF Results:**")
                            st.dataframe(
                                vif_data.style.applymap(
                                    lambda v: 'background-color: #d4edda' if '✅' in str(v) else 
                                             ('background-color: #fff3cd' if '⚠️' in str(v) else 
                                              ('background-color: #f8d7da' if '❌' in str(v) else '')),
                                    subset=['Status']
                                ),
                                use_container_width=True
                            )
                            
                            # Visualization
                            fig = px.bar(vif_data, x='Variable', y='VIF', 
                                        color='VIF',
                                        color_continuous_scale=['green', 'yellow', 'red'],
                                        title='Variance Inflation Factor by Variable')
                            fig.add_hline(y=5, line_dash="dash", line_color="orange", 
                                         annotation_text="Threshold: VIF=5")
                            fig.add_hline(y=10, line_dash="dash", line_color="red",
                                         annotation_text="Severe: VIF=10")
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Recommendations
                            severe_vars = vif_data[vif_data["VIF"] >= 10]["Variable"].tolist()
                            if severe_vars:
                                st.error(f"⚠️ **Severe Multicollinearity Detected:** {', '.join(severe_vars)}")
                                st.markdown("""
                                **Recommended Actions:**
                                1. Remove one of the highly correlated variables
                                2. Combine correlated variables into an index
                                3. Use Ridge or Lasso regression
                                4. Apply Principal Component Analysis (PCA)
                                """)
                        except ImportError:
                            st.error("statsmodels library not installed. Run: pip install statsmodels")
                        except Exception as e:
                            st.error(f"Error calculating VIF: {str(e)}")
                else:
                    st.info("Select at least 2 variables for VIF calculation")
            else:
                st.warning("Need at least 2 numeric variables for VIF calculation")
    

    # ===== SUB-TAB 1: REGRESI SEDERHANA =====
    with subtab_simple:
        st.subheader("📐 Konsep Regresi Linear")
        
        st.markdown("""
        ### Apa itu Analisis Regresi?
        
        **Analisis regresi** adalah metode statistik untuk memodelkan hubungan antara:
        - **Variabel Dependen (Y)**: Variabel yang ingin diprediksi/dijelaskan
        - **Variabel Independen (X)**: Variabel yang digunakan untuk memprediksi
        
        ### Model Regresi Linear Sederhana
        
        Persamaan matematisnya:
        
        $$Y = \\alpha + \\beta X + \\varepsilon$$
        
        Dimana:
        - **Y** = Variabel dependen (contoh: Hasil Panen)
        - **X** = Variabel independen (contoh: Dosis Pupuk N)
        - **α (alpha)** = Intercept (konstanta) - nilai Y ketika X = 0
        - **β (beta)** = Slope (kemiringan) - perubahan Y untuk setiap kenaikan 1 unit X
        - **ε (epsilon)** = Error term (residual) - perbedaan antara nilai aktual dan prediksi
        
        ---
        
        ### Metode Least Squares (Kuadrat Terkecil)
        
        Untuk menemukan garis regresi terbaik, kita menggunakan **metode kuadrat terkecil** yang meminimalkan:
        
        $$\\text{SSE} = \\sum_{i=1}^{n} (Y_i - \\hat{Y}_i)^2$$
        
        Dimana:
        - **SSE** = Sum of Squared Errors (Jumlah Kuadrat Galat)
        - **Y_i** = Nilai aktual observasi ke-i
        - **Ŷ_i** = Nilai prediksi observasi ke-i
        
        **Rumus untuk menghitung koefisien:**
        
        $$\\beta = \\frac{\\sum(X_i - \\bar{X})(Y_i - \\bar{Y})}{\\sum(X_i - \\bar{X})^2}$$
        
        $$\\alpha = \\bar{Y} - \\beta \\bar{X}$$
        
        ---
        
        ### Koefisien Determinasi (R²)
        
        **R²** mengukur seberapa baik model menjelaskan variasi dalam data:
        
        $$R^2 = 1 - \\frac{\\text{SSE}}{\\text{SST}} = 1 - \\frac{\\sum(Y_i - \\hat{Y}_i)^2}{\\sum(Y_i - \\bar{Y})^2}$$
        
        **Interpretasi:**
        - **R² = 0.90** → Model menjelaskan 90% variasi dalam Y
        - **R² = 0.50** → Model menjelaskan 50% variasi dalam Y
        - **R² = 0.10** → Model hanya menjelaskan 10% variasi (model lemah)
        
        ---
        
        ### Koefisien Korelasi (r) - Pearson Correlation
        
        **Koefisien korelasi (r)** mengukur **kekuatan dan arah** hubungan linear antara dua variabel:
        
        $$r = \\frac{\\sum(X_i - \\bar{X})(Y_i - \\bar{Y})}{\\sqrt{\\sum(X_i - \\bar{X})^2 \\sum(Y_i - \\bar{Y})^2}}$$
        
        Atau dalam bentuk lain:
        
        $$r = \\frac{\\text{Cov}(X,Y)}{\\sigma_X \\sigma_Y}$$
        
        **Rentang Nilai:**
        - **r = +1** → Korelasi positif sempurna (X naik, Y naik proporsional)
        - **r = 0** → Tidak ada korelasi linear
        - **r = -1** → Korelasi negatif sempurna (X naik, Y turun proporsional)
        
        **Interpretasi Kekuatan Korelasi:**
        - **|r| > 0.8** → Korelasi sangat kuat
        - **0.6 < |r| ≤ 0.8** → Korelasi kuat
        - **0.4 < |r| ≤ 0.6** → Korelasi sedang
        - **0.2 < |r| ≤ 0.4** → Korelasi lemah
        - **|r| ≤ 0.2** → Korelasi sangat lemah/tidak ada
        
        **Contoh Interpretasi:**
        - **r = 0.85** → Korelasi positif sangat kuat (X dan Y bergerak searah)
        - **r = -0.65** → Korelasi negatif kuat (X naik, Y cenderung turun)
        - **r = 0.25** → Korelasi positif lemah (hubungan tidak terlalu jelas)
        
        ---
        
        ### 🔗 Hubungan antara r dan R²
        
        **Untuk regresi linear sederhana (1 variabel X):**
        
        $$R^2 = r^2$$
        
        **Artinya:**
        - Jika **r = 0.9**, maka **R² = 0.81** (81% variasi dijelaskan)
        - Jika **r = -0.9**, maka **R² = 0.81** (sama! R² selalu positif)
        - Jika **r = 0.5**, maka **R² = 0.25** (hanya 25% variasi dijelaskan)
        
        **Perbedaan Penting:**
        
        | Aspek | Korelasi (r) | Determinasi (R²) |
        |-------|--------------|------------------|
        | **Rentang** | -1 hingga +1 | 0 hingga 1 |
        | **Arah** | Menunjukkan arah (+ atau -) | Tidak menunjukkan arah |
        | **Interpretasi** | Kekuatan & arah hubungan | Proporsi variasi yang dijelaskan |
        | **Regresi Berganda** | Tidak berlaku | Berlaku (R² multiple) |
        
        **Contoh Praktis:**
        
        Misalkan kita analisis hubungan **Dosis Pupuk N (X)** dengan **Hasil Panen (Y)**:
        
        - **r = 0.85** → Ada korelasi positif kuat (semakin banyak pupuk, hasil cenderung naik)
        - **R² = 0.72** → 72% variasi hasil panen dijelaskan oleh dosis pupuk
        - **Sisanya 28%** → Dijelaskan oleh faktor lain (cuaca, varietas, dll)
        
        ---
        
        ### 📊 Visualisasi Korelasi
        
        **Korelasi Positif Kuat (r ≈ 0.9):**
        ```
        Y |        ●
          |      ●
          |    ●
          |  ●
          |●___________X
        ```
        
        **Korelasi Negatif Kuat (r ≈ -0.9):**
        ```
        Y |●
          |  ●
          |    ●
          |      ●
          |        ●___X
        ```
        
        **Tidak Ada Korelasi (r ≈ 0):**
        ```
        Y |  ●   ●
          |●   ●   ●
          |  ●   ●
          |___________X
        ```
        
        ---
        
        ### ⚠️ Peringatan Penting
        
        1. **Korelasi ≠ Kausalitas**
           - r = 0.9 TIDAK berarti X menyebabkan Y
           - Bisa ada variabel ketiga yang mempengaruhi keduanya
           - Contoh: Es krim dan kasus tenggelam berkorelasi (keduanya naik di musim panas)
        
        2. **Korelasi hanya mengukur hubungan LINEAR**
           - Bisa ada hubungan non-linear yang kuat tapi r = 0
           - Contoh: Y = X² memiliki hubungan sempurna tapi r ≠ 1
        
        3. **Outlier sangat mempengaruhi r**
           - Satu data ekstrem bisa mengubah r secara signifikan
           - Selalu cek scatter plot, jangan hanya lihat angka r
        
        ---
        
        ### Asumsi Regresi Linear (BLUE - Best Linear Unbiased Estimator)
        
        Agar hasil regresi valid, harus memenuhi asumsi:
        
        1. **Linearitas**: Hubungan antara X dan Y harus linear
        2. **Independensi**: Observasi harus independen satu sama lain
        3. **Homoskedastisitas**: Varians error harus konstan (tidak heteroskedastik)
        4. **Normalitas**: Error harus terdistribusi normal
        5. **No Multicollinearity** (untuk regresi berganda): Variabel X tidak saling berkorelasi tinggi
        
        """)  # End of Simple Regression sub-tab
    
    # ===== SUB-TAB 2: REGRESI BERGANDA =====
    with subtab_multiple:
        st.subheader("🔢 Regresi Linear Berganda")
        
        st.markdown("""
        ## 🔢 REGRESI LINEAR BERGANDA (Multiple Linear Regression)
        
        ### Apa itu Regresi Berganda?
        
        **Regresi berganda** adalah perluasan dari regresi sederhana dimana kita menggunakan **lebih dari satu variabel independen** untuk memprediksi variabel dependen.
        
        **Contoh Aplikasi Pertanian:**
        - Hasil Panen = f(Pupuk N, Pupuk P, Pupuk K, Curah Hujan, Suhu)
        - Harga Komoditas = f(Produksi, Permintaan, Biaya Transportasi, Musim)
        - Produktivitas = f(Luas Lahan, Tenaga Kerja, Modal, Teknologi)
        
        ---
        
        ### Model Regresi Linear Berganda
        
        **Bentuk Umum:**
        
        $$Y = \\beta_0 + \\beta_1 X_1 + \\beta_2 X_2 + \\beta_3 X_3 + ... + \\beta_k X_k + \\varepsilon$$
        
        Dimana:
        - **Y** = Variabel dependen (yang diprediksi)
        - **X₁, X₂, ..., Xₖ** = Variabel independen (prediktor)
        - **β₀** = Intercept (konstanta)
        - **β₁, β₂, ..., βₖ** = Koefisien regresi parsial
        - **ε** = Error term
        - **k** = Jumlah variabel independen
        
        **Contoh Konkret (Hasil Panen Padi):**
        
        $$\\text{Yield} = \\beta_0 + \\beta_1 \\text{(Pupuk N)} + \\beta_2 \\text{(Pupuk P)} + \\beta_3 \\text{(Curah Hujan)} + \\varepsilon$$
        
        Misal hasil estimasi:
        
        $$\\text{Yield} = 2000 + 15N + 10P + 5R + \\varepsilon$$
        
        **Interpretasi:**
        - **Intercept (2000)**: Hasil panen dasar tanpa input apapun
        - **β₁ = 15**: Setiap kenaikan 1 kg/ha pupuk N → yield naik 15 kg/ha (ceteris paribus)
        - **β₂ = 10**: Setiap kenaikan 1 kg/ha pupuk P → yield naik 10 kg/ha (ceteris paribus)
        - **β₃ = 5**: Setiap kenaikan 1 mm curah hujan → yield naik 5 kg/ha (ceteris paribus)
        
        > **Ceteris paribus** = "hal lain tetap sama" - artinya efek satu variabel dihitung sambil menahan variabel lain konstan
        
        ---
        
        ### Notasi Matriks (Matrix Form)
        
        Untuk efisiensi komputasi, regresi berganda ditulis dalam bentuk matriks:
        
        $$\\mathbf{Y} = \\mathbf{X}\\boldsymbol{\\beta} + \\boldsymbol{\\varepsilon}$$
        
        Dimana:
        - **Y** = Vektor n×1 (n observasi)
        - **X** = Matriks n×(k+1) (design matrix)
        - **β** = Vektor (k+1)×1 (koefisien)
        - **ε** = Vektor n×1 (error)
        
        **Solusi Least Squares:**
        
        $$\\hat{\\boldsymbol{\\beta}} = (\\mathbf{X}^T\\mathbf{X})^{-1}\\mathbf{X}^T\\mathbf{Y}$$
        
        Ini adalah formula yang digunakan oleh software statistik (Python, R, SPSS, dll) untuk menghitung koefisien regresi.
        
        ---
        
        ### R² dan Adjusted R² (R² Adjusted)
        
        **R² (Coefficient of Determination):**
        
        $$R^2 = 1 - \\frac{\\text{SSE}}{\\text{SST}} = 1 - \\frac{\\sum(Y_i - \\hat{Y}_i)^2}{\\sum(Y_i - \\bar{Y})^2}$$
        
        **Masalah R² dalam Regresi Berganda:**
        - R² **selalu naik** ketika menambah variabel baru (bahkan variabel yang tidak relevan!)
        - Ini bisa menyesatkan - model dengan banyak variabel terlihat lebih baik padahal overfitting
        
        **Solusi: Adjusted R² (R̄²)**
        
        $$R^2_{adj} = 1 - \\frac{(1-R^2)(n-1)}{n-k-1}$$
        
        Dimana:
        - **n** = Jumlah observasi
        - **k** = Jumlah variabel independen
        
        **Perbedaan:**
        
        | Aspek | R² | Adjusted R² |
        |-------|-----|-------------|
        | **Nilai** | Selalu naik saat tambah variabel | Bisa turun jika variabel tidak berguna |
        | **Penalty** | Tidak ada | Ada penalty untuk kompleksitas |
        | **Interpretasi** | % variasi dijelaskan | % variasi dijelaskan (adjusted) |
        | **Untuk Perbandingan** | Tidak cocok | Cocok untuk compare model |
        
        **Contoh:**
        - Model 1: R² = 0.85, R²adj = 0.83 (3 variabel)
        - Model 2: R² = 0.87, R²adj = 0.82 (10 variabel)
        - **Pilih Model 1!** (R²adj lebih tinggi, lebih parsimonious)
        
        ---
        
        ### Multicollinearity (Multikolinearitas)
        
        **Definisi:**
        Multikolinearitas terjadi ketika **variabel independen saling berkorelasi tinggi**.
        
        **Contoh Masalah:**
        - Pupuk N dan Pupuk Urea (hampir sama, korelasi tinggi)
        - Luas Lahan dan Jumlah Tanaman (berkorelasi sempurna)
        - Suhu dan Musim (berkorelasi kuat)
        
        **Dampak Multikolinearitas:**
        1. **Koefisien tidak stabil** - berubah drastis dengan data sedikit berbeda
        2. **Standard error besar** - koefisien tidak signifikan padahal seharusnya signifikan
        3. **Interpretasi sulit** - susah memisahkan efek masing-masing variabel
        4. **Tanda koefisien aneh** - bisa berlawanan dengan teori
        
        **Deteksi Multikolinearitas: VIF (Variance Inflation Factor)**
        
        $$VIF_j = \\frac{1}{1 - R^2_j}$$
        
        Dimana R²ⱼ adalah R² dari regresi Xⱼ terhadap semua X lainnya.
        
        **Interpretasi VIF:**
        - **VIF = 1** → Tidak ada korelasi (ideal)
        - **VIF < 5** → Multikolinearitas rendah (acceptable)
        - **5 ≤ VIF < 10** → Multikolinearitas sedang (perlu perhatian)
        - **VIF ≥ 10** → Multikolinearitas tinggi (masalah serius!)
        
        **Solusi Multikolinearitas:**
        1. **Hapus salah satu variabel** yang berkorelasi tinggi
        2. **Kombinasikan variabel** (misal: buat indeks komposit)
        3. **Gunakan Ridge Regression** atau Lasso (regularization)
        4. **Tambah data** (jika memungkinkan)
        5. **Principal Component Analysis (PCA)**
        
        ---
        
        ### Interpretasi Koefisien Regresi Berganda
        
        **Koefisien Parsial (βⱼ):**
        
        Koefisien βⱼ menunjukkan **perubahan Y untuk setiap kenaikan 1 unit Xⱼ, dengan variabel lain tetap (ceteris paribus)**.
        
        **Contoh Praktis:**
        
        Model: **Harga Tomat = 5000 + 200×Kualitas - 50×Jarak + 100×Musim**
        
        Interpretasi:
        - **β₀ = 5000**: Harga dasar tomat (Rp 5,000/kg)
        - **β₁ = 200**: Setiap kenaikan 1 poin kualitas → harga naik Rp 200/kg (jarak & musim tetap)
        - **β₂ = -50**: Setiap kenaikan 1 km jarak → harga turun Rp 50/kg (kualitas & musim tetap)
        - **β₃ = 100**: Di musim panen → harga naik Rp 100/kg (kualitas & jarak tetap)
        
        **Standardized Coefficients (Beta Coefficients):**
        
        Untuk membandingkan **kekuatan relatif** masing-masing variabel:
        
        $$\\beta^*_j = \\beta_j \\times \\frac{\\sigma_{X_j}}{\\sigma_Y}$$
        
        **Contoh:**
        - β*₁ = 0.65 (Kualitas)
        - β*₂ = -0.30 (Jarak)
        - β*₃ = 0.15 (Musim)
        
        **Interpretasi:** Kualitas adalah faktor paling kuat (0.65), diikuti Jarak (-0.30), lalu Musim (0.15).
        
        ---
        
        ### Uji Signifikansi dalam Regresi Berganda
        
        **1. Uji F (Overall Significance)**
        
        **Hipotesis:**
        - H₀: β₁ = β₂ = ... = βₖ = 0 (semua variabel tidak berpengaruh)
        - H₁: Minimal ada satu βⱼ ≠ 0
        
        **Statistik F:**
        
        $$F = \\frac{R^2/k}{(1-R^2)/(n-k-1)}$$
        
        **Keputusan:**
        - Jika **p-value < 0.05** → Tolak H₀ → Model signifikan secara keseluruhan
        - Jika **p-value ≥ 0.05** → Terima H₀ → Model tidak berguna
        
        **2. Uji t (Individual Significance)**
        
        **Hipotesis (untuk setiap βⱼ):**
        - H₀: βⱼ = 0 (variabel Xⱼ tidak berpengaruh)
        - H₁: βⱼ ≠ 0 (variabel Xⱼ berpengaruh)
        
        **Statistik t:**
        
        $$t_j = \\frac{\\hat{\\beta}_j}{SE(\\hat{\\beta}_j)}$$
        
        **Keputusan:**
        - Jika **p-value < 0.05** → Variabel Xⱼ signifikan
        - Jika **p-value ≥ 0.05** → Variabel Xⱼ tidak signifikan (bisa dihapus)
        
        ---
        
        ### Contoh Analisis Lengkap (Hasil Panen Cabai)
        
        **Data:** 100 petani cabai dengan variabel:
        - Y = Hasil Panen (ton/ha)
        - X₁ = Pupuk NPK (kg/ha)
        - X₂ = Pestisida (liter/ha)
        - X₃ = Tenaga Kerja (HOK/ha)
        
        **Hasil Regresi:**
        
        ```
        Yield = 2.5 + 0.015×NPK + 0.8×Pestisida + 0.05×Tenaga_Kerja
        
        R² = 0.78
        R²adj = 0.77
        F-statistic = 112.5 (p < 0.001)
        
        Koefisien:
        - NPK: β = 0.015, t = 8.2, p < 0.001 ✅ Signifikan
        - Pestisida: β = 0.8, t = 5.1, p < 0.001 ✅ Signifikan
        - Tenaga Kerja: β = 0.05, t = 2.3, p = 0.024 ✅ Signifikan
        
        VIF:
        - NPK: 1.2 ✅ OK
        - Pestisida: 1.5 ✅ OK
        - Tenaga Kerja: 1.3 ✅ OK
        ```
        
        **Interpretasi:**
        
        1. **Model Valid:**
           - F-test signifikan (p < 0.001) → Model berguna
           - R²adj = 0.77 → 77% variasi yield dijelaskan
           - VIF < 5 → Tidak ada multikolinearitas
        
        2. **Efek Variabel:**
           - **NPK**: Setiap tambahan 1 kg/ha → yield naik 0.015 ton/ha (15 kg/ha)
           - **Pestisida**: Setiap tambahan 1 liter/ha → yield naik 0.8 ton/ha (800 kg/ha)
           - **Tenaga Kerja**: Setiap tambahan 1 HOK/ha → yield naik 0.05 ton/ha (50 kg/ha)
        
        3. **Rekomendasi:**
           - Semua variabel signifikan → pertahankan dalam model
           - Pestisida paling efektif (koefisien terbesar)
           - Untuk meningkatkan yield 1 ton/ha, bisa:
             - Tambah 67 kg NPK, ATAU
             - Tambah 1.25 liter pestisida, ATAU
             - Tambah 20 HOK tenaga kerja
        
        ---
        
        ### ⚠️ Peringatan Penting Regresi Berganda
        
        1. **Overfitting:**
           - Jangan tambah terlalu banyak variabel
           - Gunakan R²adj, bukan R²
           - Rule of thumb: n ≥ 10k (10 observasi per variabel)
        
        2. **Multikolinearitas:**
           - Selalu cek VIF
           - Jangan gunakan variabel yang sangat berkorelasi
        
        3. **Interpretasi Kausal:**
           - Regresi hanya menunjukkan **asosiasi**, bukan **kausalitas**
           - Perlu eksperimen atau teori kuat untuk klaim kausal
        
        4. **Extrapolation:**
           - Jangan prediksi di luar range data
           - Model hanya valid dalam range observasi
        
        5. **Asumsi:**
        """)  # End of Multiple Regression sub-tab
    
    # ===== SUB-TAB 3: INFERENSIA OLS =====
    with subtab_inference:
        st.subheader("📊 Inferensia Regresi OLS")
        
        st.markdown("""
        ## 📊 INFERENSIA REGRESI OLS (Statistical Inference)
        
        ### Apa itu Inferensia Statistik dalam Regresi?
        
        **Inferensia statistik** memungkinkan kita untuk:
        1. **Menguji hipotesis** tentang parameter populasi (β)
        2. **Membuat interval kepercayaan** untuk estimasi parameter
        3. **Memprediksi** nilai Y baru dengan tingkat kepercayaan tertentu
        4. **Menilai signifikansi** model secara keseluruhan
        
        Ingat: Data yang kita punya adalah **sampel** dari **populasi**. Inferensia membantu kita menarik kesimpulan tentang populasi berdasarkan sampel.
        
        ---
        
        ### A. PENGUJIAN PARAMETER REGRESI & INTERVAL KEPERCAYAAN
        
        #### 1. Uji Hipotesis untuk Koefisien Individual (Uji t)
        
        **Tujuan:** Menguji apakah variabel Xⱼ berpengaruh signifikan terhadap Y
        
        **Hipotesis:**
        - **H₀: βⱼ = 0** (variabel Xⱼ tidak berpengaruh)
        - **H₁: βⱼ ≠ 0** (variabel Xⱼ berpengaruh)
        
        **Statistik Uji:**
        
        $$t = \\frac{\\hat{\\beta}_j - 0}{SE(\\hat{\\beta}_j)}$$
        
        Dimana:
        - **β̂ⱼ** = Estimasi koefisien dari sampel
        - **SE(β̂ⱼ)** = Standard error dari β̂ⱼ
        
        **Standard Error:**
        
        $$SE(\\hat{\\beta}_j) = \\sqrt{\\frac{MSE}{\\sum(X_{ij} - \\bar{X}_j)^2}}$$
        
        Dimana MSE (Mean Squared Error) = SSE/(n-k-1)
        
        **Distribusi:** t mengikuti distribusi t-Student dengan df = n-k-1
        
        **Keputusan:**
        - Jika **|t| > t_critical** atau **p-value < α** → Tolak H₀ (signifikan)
        - Jika **|t| ≤ t_critical** atau **p-value ≥ α** → Terima H₀ (tidak signifikan)
        
        **Contoh Output:**
        ```
        Variabel: Pupuk_N
        Koefisien (β̂): 15.5
        Standard Error: 2.3
        t-statistic: 6.74
        p-value: 0.000
        
        Kesimpulan: Pupuk N berpengaruh signifikan (p < 0.05) ✅
        ```
        
        ---
        
        #### 2. Interval Kepercayaan untuk Koefisien (Confidence Interval)
        
        **Tujuan:** Estimasi range nilai β yang mungkin dengan tingkat kepercayaan tertentu (biasanya 95%)
        
        **Formula:**
        
        $$CI_{95\\%}(\\beta_j) = \\hat{\\beta}_j \\pm t_{\\alpha/2, df} \\times SE(\\hat{\\beta}_j)$$
        
        Dimana:
        - **t_{α/2, df}** = Nilai kritis t untuk α = 0.05 dan df = n-k-1
        - Untuk 95% CI: α = 0.05, α/2 = 0.025
        
        **Interpretasi:**
        
        "Kita 95% yakin bahwa nilai β yang sebenarnya berada dalam interval ini"
        
        **Contoh:**
        ```
        Pupuk N:
        β̂ = 15.5
        SE = 2.3
        t_critical (df=97, α=0.025) = 1.984
        
        CI_95% = 15.5 ± 1.984 × 2.3
               = 15.5 ± 4.56
               = [10.94, 20.06]
        
        Interpretasi:
        Kita 95% yakin bahwa setiap kenaikan 1 kg/ha pupuk N akan
        meningkatkan yield antara 10.94 hingga 20.06 kg/ha
        ```
        
        **Hubungan CI dengan Uji t:**
        - Jika **CI tidak mengandung 0** → Variabel signifikan
        - Jika **CI mengandung 0** → Variabel tidak signifikan
        
        ---
        
        #### 3. Uji Signifikansi Model Keseluruhan (Uji F)
        
        **Tujuan:** Menguji apakah model secara keseluruhan berguna
        
        **Hipotesis:**
        - **H₀: β₁ = β₂ = ... = βₖ = 0** (semua variabel tidak berpengaruh)
        - **H₁: Minimal ada satu βⱼ ≠ 0** (minimal satu variabel berpengaruh)
        
        **Statistik Uji:**
        
        $$F = \\frac{MSR}{MSE} = \\frac{SSR/k}{SSE/(n-k-1)} = \\frac{R^2/k}{(1-R^2)/(n-k-1)}$$
        
        Dimana:
        - **SSR** = Sum of Squares Regression (variasi dijelaskan model)
        - **SSE** = Sum of Squares Error (variasi tidak dijelaskan)
        - **MSR** = Mean Square Regression = SSR/k
        - **MSE** = Mean Square Error = SSE/(n-k-1)
        
        **Distribusi:** F mengikuti distribusi F dengan df₁ = k dan df₂ = n-k-1
        
        **Tabel ANOVA:**
        
        | Source | SS | df | MS | F | p-value |
        |--------|----|----|----|----|---------|
        | Regression | SSR | k | MSR | F | p |
        | Residual | SSE | n-k-1 | MSE | - | - |
        | Total | SST | n-1 | - | - | - |
        
        **Contoh:**
        ```
        ANOVA Table:
        Source      | SS      | df  | MS     | F      | p-value
        ------------|---------|-----|--------|--------|--------
        Regression  | 450.5   | 3   | 150.17 | 112.5  | <0.001
        Residual    | 128.3   | 96  | 1.34   |        |
        Total       | 578.8   | 99  |        |        |
        
        Kesimpulan: Model signifikan (F = 112.5, p < 0.001) ✅
        ```
        
        ---
        
        #### 4. Interval Prediksi (Prediction Interval)
        
        **Perbedaan CI vs PI:**
        
        | Aspek | Confidence Interval | Prediction Interval |
        |-------|---------------------|---------------------|
        | **Untuk** | Estimasi rata-rata E(Y) | Prediksi nilai individual Y |
        | **Lebar** | Lebih sempit | Lebih lebar |
        | **Interpretasi** | Rata-rata populasi | Nilai individual baru |
        
        **Formula Prediction Interval:**
        
        $$PI_{95\\%}(Y_{new}) = \\hat{Y}_{new} \\pm t_{\\alpha/2, df} \\times SE_{pred}$$
        
        Dimana:
        
        $$SE_{pred} = \\sqrt{MSE \\times (1 + \\frac{1}{n} + \\frac{(X_{new} - \\bar{X})^2}{\\sum(X_i - \\bar{X})^2})}$$
        
        **Contoh:**
        ```
        Prediksi yield untuk petani baru dengan Pupuk N = 150 kg/ha:
        
        Ŷ = 2000 + 15 × 150 = 4,250 kg/ha
        
        SE_pred = 85.3
        t_critical = 1.984
        
        PI_95% = 4,250 ± 1.984 × 85.3
               = 4,250 ± 169.2
               = [4,080.8, 4,419.2]
        
        Interpretasi:
        Kita 95% yakin bahwa petani baru dengan pupuk N = 150 kg/ha
        akan memiliki yield antara 4,081 hingga 4,419 kg/ha
        ```
        
        ---
        
        ### B. KOEFISIEN DETERMINASI BERGANDA & OUTPUT SPSS
        
        #### 1. R² dan Adjusted R² (Review)
        
        **R² (Coefficient of Multiple Determination):**
        
        $$R^2 = \\frac{SSR}{SST} = 1 - \\frac{SSE}{SST}$$
        
        **Interpretasi:** Proporsi variasi Y yang dijelaskan oleh semua variabel X secara bersama-sama
        
        **Adjusted R²:**
        
        $$R^2_{adj} = 1 - \\frac{(1-R^2)(n-1)}{n-k-1}$$
        
        **Kapan Gunakan:**
        - **R²**: Untuk menilai goodness of fit satu model
        - **R²adj**: Untuk membandingkan model dengan jumlah variabel berbeda
        
        ---
        
        #### 2. Interpretasi Output Regresi (SPSS-Style)
        
        **Contoh Output Lengkap:**
        
        ```
        ═══════════════════════════════════════════════════════════
        MODEL SUMMARY
        ═══════════════════════════════════════════════════════════
        R                    : 0.883
        R Square             : 0.780
        Adjusted R Square    : 0.773
        Std. Error of Est.   : 1.157
        
        ═══════════════════════════════════════════════════════════
        ANOVA
        ═══════════════════════════════════════════════════════════
        Source          | SS      | df  | MS     | F      | Sig.
        ----------------|---------|-----|--------|--------|-------
        Regression      | 450.5   | 3   | 150.17 | 112.5  | .000
        Residual        | 128.3   | 96  | 1.34   |        |
        Total           | 578.8   | 99  |        |        |
        
        ═══════════════════════════════════════════════════════════
        COEFFICIENTS
        ═══════════════════════════════════════════════════════════
        Variable    | B      | SE    | Beta  | t     | Sig.  | VIF
        ------------|--------|-------|-------|-------|-------|-----
        (Constant)  | 2.500  | 0.350 |       | 7.14  | .000  |
        Pupuk_NPK   | 0.015  | 0.002 | 0.520 | 8.20  | .000  | 1.2
        Pestisida   | 0.800  | 0.157 | 0.380 | 5.10  | .000  | 1.5
        Tenaga_Kerja| 0.050  | 0.022 | 0.160 | 2.30  | .024  | 1.3
        
        ═══════════════════════════════════════════════════════════
        ```
        
        **Cara Membaca Output:**
        
        **1. Model Summary:**
        - **R = 0.883**: Korelasi multiple (kekuatan hubungan)
        - **R² = 0.780**: 78% variasi yield dijelaskan oleh 3 variabel
        - **R²adj = 0.773**: Adjusted untuk kompleksitas model
        - **Std. Error = 1.157**: Rata-rata deviasi prediksi dari aktual
        
        **2. ANOVA:**
        - **F = 112.5, Sig. = .000**: Model signifikan (p < 0.001) ✅
        - Minimal ada satu variabel yang berpengaruh
        
        **3. Coefficients:**
        
        **Pupuk NPK:**
        - **B = 0.015**: Setiap +1 kg/ha NPK → yield +0.015 ton/ha (15 kg/ha)
        - **SE = 0.002**: Standard error estimasi
        - **Beta = 0.520**: Standardized coefficient (paling kuat!)
        - **t = 8.20, Sig. = .000**: Sangat signifikan ✅
        - **VIF = 1.2**: Tidak ada multikolinearitas ✅
        
        **Pestisida:**
        - **B = 0.800**: Setiap +1 liter/ha → yield +0.8 ton/ha
        - **Beta = 0.380**: Faktor kedua terkuat
        - **t = 5.10, Sig. = .000**: Signifikan ✅
        - **VIF = 1.5**: OK ✅
        
        **Tenaga Kerja:**
        - **B = 0.050**: Setiap +1 HOK/ha → yield +0.05 ton/ha
        - **Beta = 0.160**: Faktor terlemah (tapi tetap signifikan)
        - **t = 2.30, Sig. = .024**: Signifikan ✅
        - **VIF = 1.3**: OK ✅
        
        ---
        
        #### 3. Langkah-langkah Analisis Regresi (Praktis)
        
        **Step 1: Estimasi Model**
        - Jalankan regresi OLS
        - Dapatkan koefisien β̂
        
        **Step 2: Uji Signifikansi Model (F-test)**
        - Cek ANOVA table
        - Jika p < 0.05 → Lanjut
        - Jika p ≥ 0.05 → Model tidak berguna, STOP
        
        **Step 3: Uji Signifikansi Individual (t-test)**
        - Cek p-value setiap variabel
        - Hapus variabel dengan p ≥ 0.05 (tidak signifikan)
        - Re-run model tanpa variabel tersebut
        
        **Step 4: Cek Multikolinearitas (VIF)**
        - Jika VIF ≥ 10 → Ada masalah
        - Hapus salah satu variabel yang berkorelasi tinggi
        
        **Step 5: Cek Asumsi (Diagnostik)**
        - Residual plot → Cek linearitas & homoskedastisitas
        - Q-Q plot → Cek normalitas
        - Jika asumsi dilanggar → Transformasi atau model lain
        
        **Step 6: Interpretasi**
        - Interpretasi koefisien dalam konteks bisnis
        - Buat rekomendasi praktis
        
        **Step 7: Prediksi (Opsional)**
        - Gunakan model untuk prediksi nilai baru
        - Hitung prediction interval
        
        ---
        
        ### C. CONTOH LENGKAP: ANALISIS REGRESI STEP-BY-STEP
        
        **Kasus:** Prediksi Harga Tomat (Rp/kg) berdasarkan:
        - X₁ = Kualitas (1-10)
        - X₂ = Jarak ke Pasar (km)
        - X₃ = Musim (0=off-season, 1=peak)
        
        **Data:** 80 observasi
        
        **Hasil Regresi:**
        
        ```
        Harga = 5,200 + 350×Kualitas - 45×Jarak + 120×Musim
        
        R² = 0.72, R²adj = 0.71, F = 68.5 (p < 0.001)
        
        Koefisien:
        - Kualitas: β = 350, SE = 45, t = 7.8, p < 0.001 ✅
        - Jarak: β = -45, SE = 12, t = -3.75, p < 0.001 ✅
        - Musim: β = 120, SE = 85, t = 1.41, p = 0.163 ❌
        
        VIF: Kualitas = 1.1, Jarak = 1.2, Musim = 1.05 ✅
        ```
        
        **Interpretasi:**
        
        1. **Model Valid:**
           - F-test signifikan → Model berguna ✅
           - R²adj = 0.71 → 71% variasi harga dijelaskan
           - VIF < 5 → Tidak ada multikolinearitas ✅
        
        2. **Variabel Signifikan:**
           - **Kualitas** (p < 0.001): Setiap +1 poin → harga +Rp 350/kg
           - **Jarak** (p < 0.001): Setiap +1 km → harga -Rp 45/kg
           - **Musim** (p = 0.163): TIDAK signifikan ❌
        
        3. **Rekomendasi:**
           - Hapus variabel "Musim" (tidak signifikan)
           - Re-run model hanya dengan Kualitas dan Jarak
           - Fokus pada peningkatan kualitas (efek terbesar)
           - Minimalisir jarak transportasi
        
        4. **Prediksi:**
           ```
           Untuk tomat dengan Kualitas = 8, Jarak = 10 km:
           
           Harga = 5,200 + 350×8 - 45×10
                 = 5,200 + 2,800 - 450
                 = 7,550 Rp/kg
           
           PI_95% = [6,850, 8,250] Rp/kg
           ```
        
        ---
        
        ### ⚠️ Peringatan Penting Inferensia
        
        1. **Sample Size:**
           - Minimal n ≥ 30 untuk asumsi normalitas (CLT)
           - Minimal n ≥ 10k untuk regresi berganda
        
        2. **Outliers:**
           - Satu outlier bisa mengubah hasil drastis
           - Selalu cek scatter plot dan residual plot
        
        3. **P-value Bukan Segalanya:**
           - p < 0.05 tidak berarti efek besar atau penting
           - Lihat juga magnitude koefisien dan R²
        
        4. **Multiple Testing:**
           - Jika test banyak variabel, gunakan Bonferroni correction
           - α_adjusted = α / jumlah_test
        
        5. **Causation:**
           - Signifikansi statistik ≠ kausalitas
           - Perlu eksperimen atau teori kuat
        
        """)
        
        # Interactive Example
        st.divider()
        st.markdown("### 🧮 Kalkulator Regresi Interaktif")
        
        col_calc1, col_calc2 = st.columns(2)
        
        with col_calc1:
            st.markdown("**Input Parameter:**")
            intercept_demo = st.number_input("Intercept (α)", value=100.0, step=10.0, key='intercept_demo')
            slope_demo = st.number_input("Slope (β)", value=5.0, step=0.5, key='slope_demo')
            x_value = st.slider("Nilai X", 0, 100, 50, key='x_demo')
        
        with col_calc2:
            st.markdown("**Output Prediksi:**")
            y_pred_demo = intercept_demo + slope_demo * x_value
            st.metric("Prediksi Y", f"{y_pred_demo:.2f}")
            st.latex(f"Y = {intercept_demo} + {slope_demo} \\times {x_value} = {y_pred_demo:.2f}")
            
            st.caption(f"""
            **Interpretasi:**
            - Jika X = 0, maka Y = {intercept_demo}
            - Setiap kenaikan 1 unit X, Y naik {slope_demo} unit
            - Pada X = {x_value}, prediksi Y = {y_pred_demo:.2f}
            """)
        
        # Correlation Calculator
        st.divider()
        st.markdown("### 📊 Kalkulator Korelasi & R²")
        
        st.info("""
        **Demonstrasi Hubungan r dan R²**
        
        Kalkulator ini menunjukkan bagaimana koefisien korelasi (r) berhubungan dengan koefisien determinasi (R²).
        Anda bisa generate data dengan korelasi tertentu dan lihat hasilnya!
        """)
        
        col_corr1, col_corr2 = st.columns(2)
        
        with col_corr1:
            st.markdown("**Input Parameter:**")
            target_r = st.slider("Target Korelasi (r)", -1.0, 1.0, 0.8, 0.05, key='target_r')
            n_points = st.slider("Jumlah Data", 20, 100, 50, key='n_points_corr')
            noise_factor = st.slider("Noise Level", 0.0, 2.0, 0.3, 0.1, key='noise_corr')
        
        # Generate correlated data
        np.random.seed(42)
        X_corr = np.random.uniform(0, 100, n_points)
        
        # Generate Y with target correlation
        # Using Cholesky decomposition for exact correlation
        mean = [50, 50]
        cov = [[100, target_r * 100], [target_r * 100, 100]]
        data_corr = np.random.multivariate_normal(mean, cov, n_points)
        X_corr = data_corr[:, 0]
        Y_corr = data_corr[:, 1] + np.random.normal(0, noise_factor, n_points)
        
        # Calculate actual correlation and R²
        correlation = np.corrcoef(X_corr, Y_corr)[0, 1]
        r_squared = correlation ** 2
        
        # Fit regression for comparison
        from sklearn.linear_model import LinearRegression
        model_corr = LinearRegression()
        model_corr.fit(X_corr.reshape(-1, 1), Y_corr)
        r2_sklearn = model_corr.score(X_corr.reshape(-1, 1), Y_corr)
        
        with col_corr2:
            st.markdown("**Hasil Perhitungan:**")
            
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric("Korelasi (r)", f"{correlation:.4f}")
                if abs(correlation) > 0.8:
                    st.caption("✅ Korelasi sangat kuat")
                elif abs(correlation) > 0.6:
                    st.caption("✅ Korelasi kuat")
                elif abs(correlation) > 0.4:
                    st.caption("⚠️ Korelasi sedang")
                else:
                    st.caption("❌ Korelasi lemah")
            
            with col_metric2:
                st.metric("R² (dari r²)", f"{r_squared:.4f}")
                st.caption(f"R² (sklearn): {r2_sklearn:.4f}")
        
        # Verification
        st.success(f"""
        **✅ Verifikasi Hubungan r dan R²:**
        
        - r = {correlation:.4f}
        - r² = {correlation**2:.4f}
        - R² (sklearn) = {r2_sklearn:.4f}
        - **Selisih:** {abs(r_squared - r2_sklearn):.6f} (seharusnya ≈ 0)
        
        **Interpretasi:**
        - {abs(r_squared * 100):.1f}% variasi Y dijelaskan oleh X
        - {abs((1 - r_squared) * 100):.1f}% dijelaskan oleh faktor lain
        """)
        
        # Plot correlation
        fig_corr = go.Figure()
        
        fig_corr.add_trace(go.Scatter(
            x=X_corr, y=Y_corr,
            mode='markers',
            name='Data Points',
            marker=dict(size=8, color='#3b82f6', opacity=0.6)
        ))
        
        # Add regression line
        Y_pred_corr = model_corr.predict(X_corr.reshape(-1, 1))
        fig_corr.add_trace(go.Scatter(
            x=X_corr, y=Y_pred_corr,
            mode='lines',
            name='Regression Line',
            line=dict(color='#ef4444', width=2)
        ))
        
        fig_corr.update_layout(
            title=f"Scatter Plot: r = {correlation:.3f}, R² = {r_squared:.3f}",
            xaxis_title="X",
            yaxis_title="Y",
            height=400
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Interpretation guide
        st.markdown("""
        **💡 Panduan Interpretasi:**
        
        1. **Korelasi Positif (r > 0):**
           - Garis regresi naik dari kiri ke kanan
           - X naik → Y cenderung naik
           - Contoh: Dosis pupuk vs Hasil panen
        
        2. **Korelasi Negatif (r < 0):**
           - Garis regresi turun dari kiri ke kanan
           - X naik → Y cenderung turun
           - Contoh: Suhu vs Kualitas produk tertentu
        
        3. **Tidak Ada Korelasi (r ≈ 0):**
           - Garis regresi hampir horizontal
           - X tidak mempengaruhi Y
           - R² mendekati 0 (model tidak berguna)
        """)
        
        # ===== ASUMSI OLS & UJI ASUMSI KLASIK =====
        st.divider()
        st.subheader("🔍 Asumsi OLS & Uji Asumsi Klasik")
        
        st.markdown("""
        ## 🔍 ASUMSI YANG MENDASARI REGRESI OLS
        
        ### Mengapa Asumsi Penting?
        
        **Ordinary Least Squares (OLS)** memberikan estimator **BLUE** (Best Linear Unbiased Estimator) **HANYA JIKA** asumsi-asumsi tertentu terpenuhi.
        
        **Jika asumsi dilanggar:**
        - Estimator tidak lagi BLUE
        - Standard error bias → uji t dan F tidak valid
        - Interval kepercayaan salah
        - Prediksi tidak akurat
        
        ---
        
        ### Asumsi Klasik Regresi OLS (Gauss-Markov)
        
        #### 1. **LINEARITAS (Linearity)**
        
        **Asumsi:** Hubungan antara X dan Y adalah **linear** dalam parameter
        
        $$E(Y|X) = \\beta_0 + \\beta_1 X_1 + \\beta_2 X_2 + ... + \\beta_k X_k$$
        
        **Artinya:**
        - Model harus linear dalam β (bukan harus linear dalam X!)
        - Y = β₀ + β₁X + β₂X² ✅ Linear dalam β (polynomial)
        - Y = β₀X^β₁ ❌ Tidak linear dalam β
        
        **Konsekuensi Jika Dilanggar:**
        - Estimasi bias
        - Prediksi tidak akurat
        - R² menyesatkan
        
        **Uji Linearitas:**
        
        1. **Scatter Plot** (X vs Y)
           - Lihat pola: harus linear
           - Jika kurva → perlu transformasi
        
        2. **Residual Plot** (Fitted vs Residuals)
           - Pola acak = ✅ Linear
           - Pola kurva/U-shape = ❌ Non-linear
        
        3. **Ramsey RESET Test**
           - H₀: Model linear
           - H₁: Model non-linear
           - Jika p < 0.05 → Tolak H₀ (non-linear)
        
        **Remedial Measures:**
        - Transformasi variabel (log, sqrt, polynomial)
        - Tambah variabel kuadratik (X²)
        - Gunakan model non-linear
        
        ---
        
        #### 2. **NORMALITAS (Normality of Errors)**
        
        **Asumsi:** Error term (ε) terdistribusi **normal**
        
        $$\\varepsilon \\sim N(0, \\sigma^2)$$
        
        **Artinya:**
        - Residual harus mengikuti distribusi normal
        - Mean residual = 0
        - Variance konstan
        
        **Konsekuensi Jika Dilanggar:**
        - Uji t dan F tidak valid (untuk sampel kecil)
        - Interval kepercayaan bias
        - **TAPI:** Dengan n besar (n > 30), CLT berlaku → masih OK
        
        **Uji Normalitas:**
        
        1. **Histogram Residual**
           - Bentuk bell curve = ✅ Normal
           - Skewed/flat = ❌ Tidak normal
        
        2. **Q-Q Plot (Quantile-Quantile)**
           - Titik mengikuti garis diagonal = ✅ Normal
           - Titik menyimpang = ❌ Tidak normal
        
        3. **Kolmogorov-Smirnov Test**
           - H₀: Residual normal
           - H₁: Residual tidak normal
           - Jika p > 0.05 → Terima H₀ (normal)
        
        4. **Shapiro-Wilk Test** (lebih powerful)
           - H₀: Residual normal
           - Jika p > 0.05 → Normal ✅
        
        5. **Jarque-Bera Test**
           - Berdasarkan skewness dan kurtosis
           - Jika p > 0.05 → Normal ✅
        
        **Remedial Measures:**
        - Transformasi Y (log, sqrt, Box-Cox)
        - Hapus outliers (jika justified)
        - Gunakan robust regression
        - Dengan n besar, abaikan (CLT)
        
        ---
        
        #### 3. **HOMOSKEDASTISITAS (Constant Variance)**
        
        **Asumsi:** Variance error **konstan** untuk semua nilai X
        
        $$Var(\\varepsilon_i) = \\sigma^2 \\text{ untuk semua } i$$
        
        **Artinya:**
        - Spread residual harus sama di semua level X
        - Tidak ada pola corong (funnel shape)
        
        **Lawan:** **Heteroskedastisitas** (variance tidak konstan)
        
        **Konsekuensi Heteroskedastisitas:**
        - Estimator masih **unbiased** ✅
        - TAPI tidak lagi **efficient** (variance besar)
        - Standard error **bias** → uji t dan F tidak valid
        - Interval kepercayaan salah
        
        **Uji Homoskedastisitas:**
        
        1. **Residual Plot** (Fitted vs Residuals)
           - Spread konstan = ✅ Homoskedastik
           - Pola corong = ❌ Heteroskedastik
        
        2. **Breusch-Pagan Test**
           - H₀: Homoskedastik
           - H₁: Heteroskedastik
           - Jika p > 0.05 → Homoskedastik ✅
        
        3. **White Test**
           - Lebih general (tidak assume bentuk heteroskedastisitas)
           - Jika p > 0.05 → Homoskedastik ✅
        
        4. **Goldfeld-Quandt Test**
           - Membagi data jadi 2 grup
           - Compare variance kedua grup
        
        **Remedial Measures:**
        - **Weighted Least Squares (WLS)**
        - **Robust Standard Errors** (White's correction)
        - Transformasi Y (log, sqrt)
        - Tambah variabel yang hilang
        
        ---
        
        #### 4. **NO AUTOCORRELATION (Independence)**
        
        **Asumsi:** Error tidak **berkorelasi** satu sama lain
        
        $$Cov(\\varepsilon_i, \\varepsilon_j) = 0 \\text{ untuk } i \\neq j$$
        
        **Artinya:**
        - Residual observasi ke-i tidak tergantung pada residual observasi ke-j
        - Penting untuk **data time series**
        
        **Lawan:** **Autokorelasi** (serial correlation)
        
        **Konsekuensi Autokorelasi:**
        - Estimator masih unbiased
        - Standard error bias (biasanya underestimate)
        - Uji t dan F terlalu optimis
        - R² overestimate
        
        **Uji Autokorelasi:**
        
        1. **Durbin-Watson Test**
           - Statistik DW: 0 hingga 4
           - **DW ≈ 2** → Tidak ada autokorelasi ✅
           - **DW < 2** → Autokorelasi positif
           - **DW > 2** → Autokorelasi negatif
           - Rule: 1.5 < DW < 2.5 → OK
        
        2. **Breusch-Godfrey Test (LM Test)**
           - Lebih general dari DW
           - Bisa detect higher-order autocorrelation
           - Jika p > 0.05 → Tidak ada autokorelasi ✅
        
        3. **Ljung-Box Test**
           - Untuk time series
           - Jika p > 0.05 → Tidak ada autokorelasi ✅
        
        4. **ACF Plot (Autocorrelation Function)**
           - Visual inspection
           - Jika lag signifikan → Ada autokorelasi
        
        **Remedial Measures:**
        - Tambah lag variabel dependen (AR model)
        - **Cochrane-Orcutt procedure**
        - **Newey-West standard errors**
        - Gunakan ARIMA atau time series model
        
        ---
        
        #### 5. **NO MULTICOLLINEARITY**
        
        **Asumsi:** Variabel independen **tidak saling berkorelasi tinggi**
        
        **Artinya:**
        - Tidak ada hubungan linear sempurna antar X
        - Tidak ada X yang bisa diprediksi sempurna dari X lain
        
        **Konsekuensi Multikolinearitas:**
        - Estimator masih unbiased
        - Standard error **sangat besar**
        - Koefisien tidak signifikan (padahal seharusnya signifikan)
        - Koefisien tidak stabil (berubah drastis)
        - Tanda koefisien aneh (berlawanan teori)
        
        **Uji Multikolinearitas:**
        
        1. **Correlation Matrix**
           - Jika |r| > 0.8 antar X → Multikolinearitas
        
        2. **VIF (Variance Inflation Factor)**
           - **VIF < 5** → OK ✅
           - **5 ≤ VIF < 10** → Moderate
           - **VIF ≥ 10** → Serious problem ❌
        
        3. **Tolerance** (1/VIF)
           - **Tolerance > 0.2** → OK ✅
           - **Tolerance < 0.1** → Problem ❌
        
        4. **Condition Index**
           - **CI < 30** → OK ✅
           - **CI ≥ 30** → Multikolinearitas
        
        **Remedial Measures:**
        - Hapus salah satu variabel yang berkorelasi
        - Kombinasikan variabel (buat index)
        - **Ridge Regression** atau **Lasso**
        - **Principal Component Analysis (PCA)**
        - Tambah data (jika memungkinkan)
        
        ---
        
        ### 📊 PENGGUNAAN SPSS UNTUK UJI ASUMSI
        
        #### Langkah-langkah di SPSS:
        
        **1. Jalankan Regresi:**
        ```
        Analyze → Regression → Linear
        - Dependent: Y
        - Independent: X1, X2, X3
        - Statistics: Klik "Collinearity diagnostics" (untuk VIF)
        - Plots: 
          ✓ *ZPRED vs *ZRESID (untuk linearitas & homoskedastisitas)
          ✓ Histogram (untuk normalitas)
          ✓ Normal P-P Plot (untuk normalitas)
        - Save: Klik "Unstandardized residuals" (untuk uji lebih lanjut)
        - OK
        ```
        
        **2. Interpretasi Output:**
        
        **A. Coefficients Table:**
        ```
        Variable    | VIF   | Tolerance
        ------------|-------|----------
        X1          | 1.25  | 0.800  ✅ OK
        X2          | 8.50  | 0.118  ⚠️ Moderate
        X3          | 12.30 | 0.081  ❌ Problem!
        ```
        
        **B. Residual Plots:**
        
        **Scatter Plot (*ZPRED vs *ZRESID):**
        - **Pola acak** = ✅ Linearitas & Homoskedastisitas OK
        - **Pola kurva** = ❌ Non-linear
        - **Pola corong** = ❌ Heteroskedastisitas
        
        **Histogram:**
        - **Bell curve** = ✅ Normal
        - **Skewed** = ❌ Tidak normal
        
        **Normal P-P Plot:**
        - **Titik di garis diagonal** = ✅ Normal
        - **Titik menyimpang** = ❌ Tidak normal
        
        **3. Uji Tambahan (Manual):**
        
        **Durbin-Watson (Autokorelasi):**
        - Lihat di "Model Summary" table
        - **DW ≈ 2** → OK ✅
        - **DW < 1.5 atau > 2.5** → Problem ❌
        
        **Kolmogorov-Smirnov (Normalitas):**
        ```
        Analyze → Nonparametric Tests → Legacy Dialogs → 1-Sample K-S
        - Test Variable: RES_1 (saved residuals)
        - Test Distribution: Normal
        - OK
        
        Interpretasi:
        - p > 0.05 → Normal ✅
        - p < 0.05 → Tidak normal ❌
        ```
        
        **Breusch-Pagan (Heteroskedastisitas):**
        - SPSS tidak punya built-in
        - Gunakan syntax atau plugin
        - Atau gunakan White test
        
        ---
        
        ### 📋 Checklist Uji Asumsi (Praktis)
        
        **Sebelum Interpretasi Regresi, CEK:**
        
        - [ ] **Linearitas**
          - ✅ Scatter plot linear
          - ✅ Residual plot acak
        
        - [ ] **Normalitas**
          - ✅ Histogram bell curve
          - ✅ Q-Q plot di garis
          - ✅ K-S test p > 0.05
        
        - [ ] **Homoskedastisitas**
          - ✅ Residual plot spread konstan
          - ✅ Breusch-Pagan p > 0.05
        
        - [ ] **No Autokorelasi**
          - ✅ Durbin-Watson ≈ 2
          - ✅ (Untuk time series saja)
        
        - [ ] **No Multikolinearitas**
          - ✅ VIF < 5
          - ✅ Tolerance > 0.2
        
        **Jika SEMUA ✅ → Lanjut interpretasi!**
        
        **Jika ada ❌ → Lakukan remedial measures!**
        
        ---
        
        ### ⚠️ Prioritas Uji Asumsi
        
        **Paling Penting (HARUS dicek):**
        1. **Multikolinearitas** - Sangat mudah dicek (VIF)
        2. **Linearitas** - Fundamental assumption
        3. **Homoskedastisitas** - Mempengaruhi inferensia
        
        **Penting (Sebaiknya dicek):**
        4. **Normalitas** - Kurang penting jika n > 30 (CLT)
        
        **Opsional (Tergantung data):**
        5. **Autokorelasi** - Hanya untuk time series
        
        ---
        
        ### 💡 Tips Praktis
        
        1. **Jangan Panik Jika Ada Pelanggaran:**
           - Hampir semua data real-world melanggar asumsi
           - Yang penting: magnitude pelanggaran
        
        2. **Prioritaskan Remedial:**
           - Multikolinearitas → Paling mudah diatasi
           - Heteroskedastisitas → Gunakan robust SE
           - Non-linearitas → Transformasi
        
        3. **Dokumentasikan:**
           - Selalu report hasil uji asumsi
           - Jelaskan remedial measures yang diambil
        
        4. **Gunakan Robust Methods:**
           - Jika banyak pelanggaran → Robust regression
           - Bootstrap standard errors
           - Quantile regression
        
        5. **Sample Size Matters:**
           - n > 100 → Banyak asumsi lebih toleran
           - n < 30 → Harus strict dengan asumsi
        
        """)  # End of OLS Assumptions section
    
    
    # ===== SUB-TAB 4: ANALISIS RUNTUN WAKTU =====
    with subtab_timeseries:
        st.subheader("📈 Analisis Runtun Waktu (Time Series Analysis)")
        
        st.markdown("""
        ## 📈 ANALISIS RUNTUN WAKTU
        
        ### Apa itu Data Runtun Waktu?
        
        **Data runtun waktu (time series)** adalah data yang dikumpulkan **secara berurutan dalam waktu** dengan interval tertentu.
        
        **Karakteristik:**
        - Observasi diurutkan berdasarkan waktu (t)
        - Interval waktu konsisten (harian, mingguan, bulanan, tahunan)
        - Nilai saat ini dipengaruhi oleh nilai masa lalu
        
        **Contoh dalam Pertanian:**
        - Harga komoditas bulanan (2020-2024)
        - Produksi padi tahunan (1990-2023)
        - Curah hujan harian
        - Harga saham perusahaan agribisnis
        - Konsumsi pupuk per kuartal
        
        ---
        
        ### Komponen Data Runtun Waktu
        
        Data time series terdiri dari 4 komponen utama:
        
        #### 1. **Trend (T)** - Kecenderungan Jangka Panjang
        
        **Definisi:** Pola pergerakan jangka panjang (naik, turun, atau stabil)
        
        **Contoh:**
        - Produksi padi Indonesia cenderung **naik** dari tahun ke tahun
        - Luas lahan pertanian cenderung **turun** karena urbanisasi
        
        **Jenis Trend:**
        - **Linear:** Y = a + bt (garis lurus)
        - **Non-linear:** Eksponensial, kuadratik, logaritmik
        
        #### 2. **Seasonal (S)** - Pola Musiman
        
        **Definisi:** Pola yang **berulang** dalam periode tertentu (< 1 tahun)
        
        **Contoh:**
        - Harga cabai **naik** menjelang Ramadan & Natal
        - Produksi padi **tinggi** saat musim panen (Maret-April, Sept-Okt)
        - Curah hujan **tinggi** di musim hujan
        
        **Periode:**
        - Bulanan: 12 bulan
        - Kuartalan: 4 kuartal
        - Mingguan: 52 minggu
        
        #### 3. **Cyclical (C)** - Pola Siklis
        
        **Definisi:** Fluktuasi jangka panjang (> 1 tahun) yang tidak teratur
        
        **Contoh:**
        - Siklus bisnis (boom-recession)
        - Siklus harga komoditas global
        - El Niño / La Niña (3-7 tahun)
        
        **Perbedaan dengan Seasonal:**
        - Seasonal: Periode tetap (12 bulan)
        - Cyclical: Periode tidak tetap (bisa 3-10 tahun)
        
        #### 4. **Irregular (I)** - Komponen Acak
        
        **Definisi:** Fluktuasi acak yang tidak bisa diprediksi
        
        **Contoh:**
        - Bencana alam (banjir, kekeringan)
        - Wabah penyakit tanaman
        - Kebijakan mendadak (impor/ekspor)
        - Shock harga global
        
        ---
        
        ### Model Dekomposisi
        
        **Tujuan:** Memisahkan komponen T, S, C, I untuk analisis
        
        #### Model Aditif:
        
        $$Y_t = T_t + S_t + C_t + I_t$$
        
        **Kapan digunakan:**
        - Amplitudo seasonal **konstan** (tidak berubah seiring waktu)
        - Contoh: Curah hujan (variasi musiman relatif tetap)
        
        #### Model Multiplikatif:
        
        $$Y_t = T_t \\times S_t \\times C_t \\times I_t$$
        
        **Kapan digunakan:**
        - Amplitudo seasonal **meningkat** seiring trend
        - Contoh: Harga komoditas (variasi musiman membesar saat harga naik)
        
        **Transformasi ke Aditif:**
        
        $$\\log(Y_t) = \\log(T_t) + \\log(S_t) + \\log(C_t) + \\log(I_t)$$
        
        ---
        
        ## 📊 ANALISIS TREND
        
        ### A. TREND LINEAR
        
        **Model:**
        
        $$Y_t = \\alpha + \\beta t + \\varepsilon_t$$
        
        Dimana:
        - **Y_t** = Nilai pada waktu t
        - **t** = Waktu (1, 2, 3, ..., n)
        - **α** = Intercept (nilai awal)
        - **β** = Slope (perubahan per periode)
        - **ε_t** = Error
        
        **Interpretasi:**
        - **β > 0** → Trend naik (pertumbuhan)
        - **β < 0** → Trend turun (penurunan)
        - **β ≈ 0** → Tidak ada trend (stasioner)
        
        **Estimasi:** Gunakan OLS (sama seperti regresi biasa)
        
        **Contoh: Produksi Padi Indonesia**
        
        ```
        Data: 2010-2023 (14 tahun)
        
        Model: Produksi = α + β × Tahun
        
        Hasil:
        Produksi = 50,000 + 1,200 × t
        
        Interpretasi:
        - Produksi awal (2010): 50,000 ton
        - Pertumbuhan: 1,200 ton per tahun
        - Prediksi 2024 (t=15): 50,000 + 1,200×15 = 68,000 ton
        ```
        
        **Kelebihan:**
        - Sederhana
        - Mudah interpretasi
        - Cocok untuk trend yang relatif stabil
        
        **Kekurangan:**
        - Tidak bisa capture perubahan kecepatan pertumbuhan
        - Asumsi pertumbuhan konstan
        
        ---
        
        ### B. TREND NON-LINEAR
        
        #### 1. **Trend Kuadratik (Quadratic)**
        
        **Model:**
        
        $$Y_t = \\alpha + \\beta_1 t + \\beta_2 t^2 + \\varepsilon_t$$
        
        **Kapan digunakan:**
        - Trend berubah arah (naik lalu turun, atau sebaliknya)
        - Ada titik maksimum/minimum
        
        **Contoh:**
        - Produksi yang naik cepat lalu melambat (diminishing returns)
        - Harga yang turun lalu naik kembali
        
        **Interpretasi:**
        - **β₂ > 0** → Kurva cembung (U-shape)
        - **β₂ < 0** → Kurva cekung (inverted U)
        
        **Contoh: Adopsi Teknologi**
        
        ```
        Model: Adopsi = 5 + 10t - 0.5t²
        
        Interpretasi:
        - Awalnya adopsi naik cepat (β₁ = 10)
        - Lama-lama melambat (β₂ = -0.5)
        - Titik maksimum: t = -β₁/(2β₂) = -10/(2×-0.5) = 10
        ```
        
        #### 2. **Trend Eksponensial**
        
        **Model:**
        
        $$Y_t = \\alpha e^{\\beta t}$$
        
        Atau dalam bentuk log-linear:
        
        $$\\log(Y_t) = \\log(\\alpha) + \\beta t + \\varepsilon_t$$
        
        **Kapan digunakan:**
        - Pertumbuhan **proporsional** (compound growth)
        - Growth rate konstan
        
        **Contoh:**
        - Populasi (pertumbuhan eksponensial)
        - Harga dengan inflasi konstan
        - Penyebaran penyakit
        
        **Interpretasi β:**
        
        $$\\text{Growth rate} = (e^\\beta - 1) \\times 100\\%$$
        
        **Contoh: Harga Lahan**
        
        ```
        Model: log(Harga) = 10 + 0.05t
        
        Interpretasi:
        - β = 0.05
        - Growth rate = (e^0.05 - 1) × 100% = 5.13% per tahun
        - Harga naik 5.13% per tahun (compound)
        ```
        
        #### 3. **Trend Logaritmik**
        
        **Model:**
        
        $$Y_t = \\alpha + \\beta \\log(t) + \\varepsilon_t$$
        
        **Kapan digunakan:**
        - Pertumbuhan cepat awalnya, lalu melambat
        - Approaching saturation
        
        **Contoh:**
        - Hasil panen dengan pupuk (diminishing returns)
        - Adopsi teknologi (S-curve awal)
        
        #### 4. **Trend Logistik (S-Curve)**
        
        **Model:**
        
        $$Y_t = \\frac{K}{1 + e^{-r(t-t_0)}}$$
        
        Dimana:
        - **K** = Carrying capacity (nilai maksimum)
        - **r** = Growth rate
        - **t₀** = Titik infleksi
        
        **Kapan digunakan:**
        - Pertumbuhan dengan batas atas
        - Adopsi teknologi (S-curve penuh)
        - Penyebaran inovasi
        
        **Contoh:**
        - Adopsi varietas baru (0% → 100%)
        - Market share (ada batas maksimum)
        
        ---
        
        ### Pemilihan Model Trend
        
        **Langkah-langkah:**
        
        1. **Plot data** → Lihat pola visual
        2. **Coba beberapa model** (linear, kuadratik, eksponensial)
        3. **Bandingkan R²** → Pilih yang tertinggi
        4. **Cek residual** → Harus acak (tidak ada pola)
        5. **Interpretasi** → Pilih yang paling masuk akal
        
        **Kriteria Pemilihan:**
        
        | Pola Data | Model Terbaik |
        |-----------|---------------|
        | Garis lurus | Linear |
        | Kurva cembung/cekung | Kuadratik |
        | Naik cepat terus | Eksponensial |
        | Naik cepat lalu lambat | Logaritmik |
        | S-curve | Logistik |
        
        ---
        
        ## 🔄 METODE DEKOMPOSISI
        
        ### Tujuan Dekomposisi
        
        1. **Memahami** komponen-komponen time series
        2. **Menghilangkan** seasonal untuk lihat trend murni
        3. **Forecasting** yang lebih akurat
        4. **Deteksi** anomali (irregular component)
        
        ---
        
        ### Metode 1: MOVING AVERAGE (Rata-rata Bergerak)
        
        **Tujuan:** Smoothing data untuk lihat trend
        
        **Formula (MA sederhana):**
        
        $$MA_t = \\frac{Y_{t-k} + Y_{t-k+1} + ... + Y_t + ... + Y_{t+k}}{2k+1}$$
        
        **Contoh: MA(3) - Moving Average 3 periode**
        
        ```
        Data: 10, 12, 15, 14, 16, 18, 20
        
        MA₃(t=2) = (10 + 12 + 15) / 3 = 12.33
        MA₃(t=3) = (12 + 15 + 14) / 3 = 13.67
        MA₃(t=4) = (15 + 14 + 16) / 3 = 15.00
        ...
        ```
        
        **Pemilihan k:**
        - **k kecil** (3, 5) → Mengikuti data lebih dekat
        - **k besar** (12, 24) → Lebih smooth, hilangkan seasonal
        - **Seasonal data:** k = periode seasonal (12 untuk bulanan)
        
        **Kelebihan:**
        - Sederhana
        - Mudah dipahami
        - Efektif hilangkan noise
        
        **Kekurangan:**
        - Hilang data di awal dan akhir
        - Lag (tertinggal dari data aktual)
        
        ---
        
        ### Metode 2: CENTERED MOVING AVERAGE
        
        **Untuk seasonal adjustment:**
        
        **Langkah (untuk data bulanan):**
        
        1. **MA(12)** → Hilangkan seasonal
        2. **Center** → Rata-rata 2 MA berurutan
        3. **Deseasonalize** → Y / CMA (untuk multiplikatif)
        
        **Contoh:**
        
        ```
        Bulan | Y   | MA(12) | CMA   | Y/CMA
        ------|-----|--------|-------|------
        Jan   | 100 |   -    |   -   |  -
        ...   | ... |  ...   |  ...  | ...
        Jul   | 120 | 105.0  | 105.5 | 1.14  ← 14% di atas trend
        Aug   | 110 | 106.0  | 105.5 | 1.04
        ...
        ```
        
        ---
        
        ### Metode 3: CLASSICAL DECOMPOSITION
        
        **Langkah-langkah (Model Multiplikatif):**
        
        **Step 1: Estimasi Trend (T)**
        - Gunakan MA atau regresi
        
        **Step 2: Detrend**
        - Hitung: Y / T (untuk multiplikatif)
        - Atau: Y - T (untuk aditif)
        
        **Step 3: Estimasi Seasonal (S)**
        - Rata-rata untuk setiap periode (bulan/kuartal)
        - Normalisasi agar total = 12 (untuk multiplikatif)
        
        **Step 4: Deseasonalize**
        - Hitung: Y / S
        
        **Step 5: Estimasi Irregular (I)**
        - I = Y / (T × S)
        
        **Contoh Output:**
        
        ```
        Bulan | Y   | T    | S     | I     | Ŷ = T×S
        ------|-----|------|-------|-------|--------
        Jan   | 95  | 100  | 0.90  | 1.06  | 90
        Feb   | 88  | 101  | 0.85  | 1.03  | 86
        Mar   | 110 | 102  | 1.05  | 1.03  | 107
        Apr   | 125 | 103  | 1.20  | 1.01  | 124
        ...
        ```
        
        **Interpretasi:**
        - **S = 0.90** → Januari 10% di bawah rata-rata
        - **S = 1.20** → April 20% di atas rata-rata
        
        ---
        
        ### Metode 4: STL DECOMPOSITION
        
        **STL = Seasonal and Trend decomposition using Loess**
        
        **Kelebihan:**
        - Lebih robust terhadap outliers
        - Bisa handle seasonal yang berubah
        - Lebih fleksibel
        
        **Kapan digunakan:**
        - Data dengan outliers banyak
        - Seasonal pattern berubah seiring waktu
        - Perlu dekomposisi yang lebih akurat
        
        ---
        
        ## 📊 APLIKASI DALAM PERTANIAN
        
        ### Contoh 1: Analisis Harga Cabai
        
        **Data:** Harga cabai bulanan 2020-2023
        
        **Analisis:**
        
        1. **Trend:** Linear naik (inflasi)
           - Model: Harga = 25,000 + 500t
           - Harga naik Rp 500/kg per bulan
        
        2. **Seasonal:** Pola musiman jelas
           - Tinggi: Ramadan (bulan 4), Natal (bulan 12)
           - Rendah: Pasca panen (bulan 2-3, 8-9)
        
        3. **Dekomposisi:**
           - Seasonal index Ramadan: 1.35 (35% di atas trend)
           - Seasonal index Februari: 0.75 (25% di bawah trend)
        
        **Rekomendasi:**
        - **Petani:** Tanam agar panen sebelum Ramadan/Natal
        - **Pedagang:** Stok sebelum peak season
        - **Konsumen:** Beli saat off-season (lebih murah)
        
        ### Contoh 2: Forecasting Produksi Padi
        
        **Data:** Produksi padi tahunan 1990-2023
        
        **Analisis:**
        
        1. **Trend:** Kuadratik
           - Model: Produksi = 40,000 + 2,000t - 50t²
           - Pertumbuhan melambat (diminishing returns)
        
        2. **Forecast 2024-2026:**
           - 2024: 68,500 ton
           - 2025: 69,400 ton
           - 2026: 70,200 ton
        
        3. **Interpretasi:**
           - Pertumbuhan masih positif tapi melambat
           - Perlu inovasi untuk akselerasi
        
        ---
        
        ## ⚠️ PERINGATAN PENTING
        
        1. **Stationarity:**
           - Time series harus stasioner untuk analisis lanjutan (ARIMA)
           - Cek dengan Augmented Dickey-Fuller test
        
        2. **Autocorrelation:**
           - Residual time series sering berkorelasi
           - Gunakan Durbin-Watson test
           - Jika ada autokorelasi → Gunakan ARIMA, bukan OLS
        
        3. **Structural Breaks:**
           - Perubahan kebijakan, bencana → Trend berubah
           - Cek dengan Chow test
           - Jika ada break → Model terpisah untuk setiap periode
        
        4. **Extrapolation:**
           - Jangan forecast terlalu jauh (max 10-20% dari data)
           - Uncertainty meningkat eksponensial
        
        5. **Seasonal Adjustment:**
           - Gunakan data deseasonalized untuk analisis trend
           - Tapi gunakan data asli untuk forecast
        
        ---
        
        ## 💡 TIPS PRAKTIS
        
        1. **Selalu Plot Data Dulu:**
           - Visual inspection sangat penting
           - Lihat pola, outliers, breaks
        
        2. **Gunakan Multiple Models:**
           - Coba linear, kuadratik, eksponensial
           - Pilih yang paling fit (R² tinggi, residual acak)
        
        3. **Validasi Forecast:**
           - Hold-out sample (20% data terakhir)
           - Compare forecast vs actual
           - Hitung MAPE (Mean Absolute Percentage Error)
        
        4. **Dokumentasi:**
           - Catat asumsi yang digunakan
           - Jelaskan pemilihan model
           - Report uncertainty (confidence interval)
        
        5. **Update Berkala:**
           - Re-estimate model dengan data baru
           - Trend bisa berubah seiring waktu
        
        """)  # End of Time Series sub-tab
    
    # ===== SUB-TAB 5: UJI CHI-SQUARE =====
    with subtab_chisquare:
        st.subheader("🔲 Uji Chi-Square (χ²)")
        
        st.markdown("""
        ## 🔲 KONSEP CHI-SQUARE
        
        ### Apa itu Uji Chi-Square?
        
        **Uji Chi-Square (χ²)** adalah uji statistik **non-parametrik** untuk menguji hubungan antara **variabel kategorikal** (nominal atau ordinal).
        
        **Kapan Digunakan:**
        - Data **kategorikal** (bukan numerik)
        - Tidak asumsi distribusi normal
        - Ukuran sampel cukup besar (n ≥ 30)
        
        **Perbedaan dengan Uji Parametrik:**
        
        | Aspek | Uji Parametrik (t, F) | Uji Chi-Square |
        |-------|----------------------|----------------|
        | **Data** | Numerik (interval/rasio) | Kategorikal (nominal/ordinal) |
        | **Asumsi** | Normalitas, homoskedastisitas | Minimal (frekuensi ≥ 5) |
        | **Contoh** | Rata-rata hasil panen | Proporsi petani adopsi teknologi |
        
        ---
        
        ### Distribusi Chi-Square
        
        **Statistik Chi-Square:**
        
        $$\\chi^2 = \\sum \\frac{(O_i - E_i)^2}{E_i}$$
        
        Dimana:
        - **O_i** = Observed frequency (frekuensi observasi)
        - **E_i** = Expected frequency (frekuensi harapan)
        
        **Interpretasi:**
        - **χ² = 0** → Observed = Expected (perfect fit)
        - **χ² besar** → Perbedaan besar antara observed dan expected
        
        **Distribusi:**
        - Mengikuti distribusi chi-square dengan **degrees of freedom (df)**
        - Selalu **positif** (χ² ≥ 0)
        - **Skewed right** (tidak simetris)
        
        **Degrees of Freedom:**
        - Goodness of Fit: df = k - 1 (k = jumlah kategori)
        - Test of Independence: df = (r-1)(c-1) (r=baris, c=kolom)
        - Test of Homogeneity: df = (r-1)(c-1)
        
        ---
        
        ## A. UJI KEPATUTAN (GOODNESS OF FIT TEST)
        
        ### Tujuan
        
        Menguji apakah **distribusi observasi** sesuai dengan **distribusi teoritis** tertentu.
        
        **Pertanyaan yang Dijawab:**
        - Apakah data mengikuti distribusi uniform?
        - Apakah data mengikuti distribusi normal?
        - Apakah proporsi sesuai dengan yang diharapkan?
        
        ---
        
        ### Hipotesis
        
        - **H₀:** Data mengikuti distribusi yang diharapkan
        - **H₁:** Data TIDAK mengikuti distribusi yang diharapkan
        
        ---
        
        ### Formula
        
        $$\\chi^2 = \\sum_{i=1}^{k} \\frac{(O_i - E_i)^2}{E_i}$$
        
        **Degrees of Freedom:** df = k - 1 - p
        
        Dimana:
        - k = Jumlah kategori
        - p = Jumlah parameter yang diestimasi
        
        **Keputusan:**
        - Jika **χ² > χ²_critical** atau **p < 0.05** → Tolak H₀
        - Jika **χ² ≤ χ²_critical** atau **p ≥ 0.05** → Terima H₀
        
        ---
        
        ### Contoh 1: Uji Distribusi Uniform
        
        **Kasus:** Apakah petani memilih 4 varietas padi dengan proporsi yang sama?
        
        **Data:**
        
        | Varietas | Observed (O) | Expected (E) | (O-E)²/E |
        |----------|--------------|--------------|----------|
        | A        | 45           | 50           | 0.50     |
        | B        | 52           | 50           | 0.08     |
        | C        | 48           | 50           | 0.08     |
        | D        | 55           | 50           | 0.50     |
        | **Total**| **200**      | **200**      | **1.16** |
        
        **Perhitungan:**
        
        ```
        Expected (E) = Total / k = 200 / 4 = 50
        
        χ² = Σ(O-E)²/E = 1.16
        df = k - 1 = 4 - 1 = 3
        χ²_critical (α=0.05, df=3) = 7.815
        
        Keputusan: χ² (1.16) < χ²_critical (7.815)
        Kesimpulan: Terima H₀ → Distribusi uniform ✅
        ```
        
        **Interpretasi:**
        - Tidak ada perbedaan signifikan dalam preferensi varietas
        - Petani memilih keempat varietas dengan proporsi yang sama
        
        ---
        
        ### Contoh 2: Uji Proporsi Tertentu
        
        **Kasus:** Apakah proporsi adopsi teknologi sesuai target (60% adopsi, 40% non-adopsi)?
        
        **Data:**
        
        | Status | Observed (O) | Expected (E) | (O-E)²/E |
        |--------|--------------|--------------|----------|
        | Adopsi | 140          | 150 (60%)    | 0.67     |
        | Non-Adopsi | 110      | 100 (40%)    | 1.00     |
        | **Total** | **250**   | **250**      | **1.67** |
        
        **Perhitungan:**
        
        ```
        χ² = 1.67
        df = 2 - 1 = 1
        χ²_critical (α=0.05, df=1) = 3.841
        p-value = 0.196
        
        Keputusan: χ² (1.67) < χ²_critical (3.841)
        Kesimpulan: Terima H₀ → Proporsi sesuai target ✅
        ```
        
        ---
        
        ### Contoh 3: Uji Distribusi Normal (Binning)
        
        **Kasus:** Apakah hasil panen mengikuti distribusi normal?
        
        **Langkah:**
        
        1. **Bagi data ke dalam bins** (misal 5 kategori)
        2. **Hitung expected frequency** berdasarkan distribusi normal
        3. **Hitung χ²**
        
        **Data:**
        
        | Bin | Range | Observed | Expected (Normal) | (O-E)²/E |
        |-----|-------|----------|-------------------|----------|
        | 1   | < 40  | 12       | 15.9              | 0.96     |
        | 2   | 40-50 | 35       | 34.1              | 0.02     |
        | 3   | 50-60 | 48       | 50.0              | 0.08     |
        | 4   | 60-70 | 33       | 34.1              | 0.04     |
        | 5   | > 70  | 17       | 15.9              | 0.08     |
        | **Total** | | **145** | **150**          | **1.18** |
        
        ```
        χ² = 1.18
        df = 5 - 1 - 2 = 2  (2 parameter: mean, SD)
        χ²_critical (α=0.05, df=2) = 5.991
        
        Kesimpulan: Terima H₀ → Data normal ✅
        ```
        
        ---
        
        ## C. TES HOMOGENITAS (TEST OF HOMOGENEITY)
        
        ### Tujuan
        
        Menguji apakah **distribusi variabel kategorikal sama** di beberapa **populasi berbeda**.
        
        **Pertanyaan yang Dijawab:**
        - Apakah proporsi adopsi sama di berbagai daerah?
        - Apakah preferensi varietas sama di berbagai kelompok petani?
        - Apakah distribusi tingkat pendidikan sama di berbagai desa?
        
        **Perbedaan dengan Test of Independence:**
        
        | Aspek | Test of Homogeneity | Test of Independence |
        |-------|---------------------|----------------------|
        | **Tujuan** | Compare distribusi antar populasi | Test hubungan 2 variabel |
        | **Sampling** | Sampel terpisah per populasi | Satu sampel |
        | **Pertanyaan** | "Apakah distribusi sama?" | "Apakah ada hubungan?" |
        
        ---
        
        ### Hipotesis
        
        - **H₀:** Distribusi sama di semua populasi (homogen)
        - **H₁:** Distribusi berbeda di minimal satu populasi
        
        ---
        
        ### Formula
        
        $$\\chi^2 = \\sum_{i=1}^{r} \\sum_{j=1}^{c} \\frac{(O_{ij} - E_{ij})^2}{E_{ij}}$$
        
        **Expected Frequency:**
        
        $$E_{ij} = \\frac{(\\text{Row Total}_i) \\times (\\text{Column Total}_j)}{\\text{Grand Total}}$$
        
        **Degrees of Freedom:** df = (r - 1)(c - 1)
        
        Dimana:
        - r = Jumlah baris (populasi)
        - c = Jumlah kolom (kategori)
        
        ---
        
        ### Contoh: Adopsi Teknologi di 3 Daerah
        
        **Kasus:** Apakah proporsi adopsi teknologi sama di Daerah A, B, dan C?
        
        **Data Observasi:**
        
        | Daerah | Adopsi | Non-Adopsi | Total |
        |--------|--------|------------|-------|
        | A      | 60     | 40         | 100   |
        | B      | 45     | 55         | 100   |
        | C      | 75     | 25         | 100   |
        | **Total** | **180** | **120** | **300** |
        
        **Expected Frequency:**
        
        ```
        E(A, Adopsi) = (100 × 180) / 300 = 60
        E(A, Non-Adopsi) = (100 × 120) / 300 = 40
        E(B, Adopsi) = (100 × 180) / 300 = 60
        E(B, Non-Adopsi) = (100 × 120) / 300 = 40
        E(C, Adopsi) = (100 × 180) / 300 = 60
        E(C, Non-Adopsi) = (100 × 120) / 300 = 40
        ```
        
        **Tabel Expected:**
        
        | Daerah | Adopsi | Non-Adopsi |
        |--------|--------|------------|
        | A      | 60     | 40         |
        | B      | 60     | 40         |
        | C      | 60     | 40         |
        
        **Perhitungan χ²:**
        
        ```
        χ² = (60-60)²/60 + (40-40)²/40 +
             (45-60)²/60 + (55-40)²/40 +
             (75-60)²/60 + (25-40)²/40
           
           = 0 + 0 + 3.75 + 5.625 + 3.75 + 5.625
           = 18.75
        
        df = (3-1)(2-1) = 2
        χ²_critical (α=0.05, df=2) = 5.991
        p-value < 0.001
        
        Keputusan: χ² (18.75) > χ²_critical (5.991)
        Kesimpulan: Tolak H₀ → Distribusi BERBEDA ❌
        ```
        
        **Interpretasi:**
        - Proporsi adopsi **tidak sama** di ketiga daerah
        - Daerah C memiliki adopsi tertinggi (75%)
        - Daerah B memiliki adopsi terendah (45%)
        - **Rekomendasi:** Fokus program penyuluhan di Daerah B
        
        ---
        
        ### Contoh 2: Preferensi Varietas di 4 Kelompok Petani
        
        **Data:**
        
        | Kelompok | Varietas A | Varietas B | Varietas C | Total |
        |----------|------------|------------|------------|-------|
        | Muda     | 30         | 45         | 25         | 100   |
        | Menengah | 40         | 35         | 25         | 100   |
        | Tua      | 50         | 30         | 20         | 100   |
        | Wanita   | 35         | 40         | 25         | 100   |
        | **Total**| **155**    | **150**    | **95**     | **400**|
        
        **Hasil Analisis:**
        
        ```
        χ² = 8.92
        df = (4-1)(3-1) = 6
        χ²_critical (α=0.05, df=6) = 12.592
        p-value = 0.178
        
        Kesimpulan: Terima H₀ → Distribusi SAMA ✅
        ```
        
        **Interpretasi:**
        - Tidak ada perbedaan signifikan dalam preferensi varietas
        - Semua kelompok memiliki pola preferensi yang serupa
        
        ---
        
        ## 📊 ASUMSI UJI CHI-SQUARE
        
        ### 1. **Expected Frequency ≥ 5**
        
        **Aturan:**
        - Semua sel harus memiliki **E_i ≥ 5**
        - Jika ada sel dengan E < 5 → Gabungkan kategori
        
        **Contoh:**
        
        ```
        Kategori | Observed | Expected
        ---------|----------|----------
        A        | 10       | 8.5  ✅
        B        | 15       | 12.0 ✅
        C        | 3        | 2.5  ❌ (< 5)
        D        | 2        | 2.0  ❌ (< 5)
        
        Solusi: Gabungkan C dan D
        
        C+D      | 5        | 4.5  ⚠️ (borderline, tapi acceptable)
        ```
        
        ### 2. **Independence**
        
        - Observasi harus **independen**
        - Satu individu hanya masuk **satu kategori**
        - Tidak ada **repeated measures**
        
        ### 3. **Random Sampling**
        
        - Sampel harus **random**
        - Representatif dari populasi
        
        ---
        
        ## ⚠️ PERINGATAN PENTING
        
        ### 1. **Chi-Square vs Fisher's Exact Test**
        
        **Gunakan Fisher's Exact Test jika:**
        - Sampel kecil (n < 30)
        - Ada expected frequency < 5
        - Tabel 2×2
        
        ### 2. **Interpretasi p-value**
        
        - **p < 0.05** → Tolak H₀ (ada perbedaan/hubungan)
        - **p ≥ 0.05** → Terima H₀ (tidak ada perbedaan/hubungan)
        
        **TAPI:** p-value tidak memberitahu **seberapa besar** perbedaannya!
        
        ### 3. **Effect Size**
        
        **Cramér's V** (untuk mengukur kekuatan hubungan):
        
        $$V = \\sqrt{\\frac{\\chi^2}{n \\times \\min(r-1, c-1)}}$$
        
        **Interpretasi:**
        - **V < 0.1** → Efek sangat kecil
        - **0.1 ≤ V < 0.3** → Efek kecil
        - **0.3 ≤ V < 0.5** → Efek sedang
        - **V ≥ 0.5** → Efek besar
        
        ### 4. **Multiple Comparisons**
        
        Jika χ² signifikan dengan banyak kategori:
        - Lakukan **post-hoc tests**
        - Gunakan **Bonferroni correction**
        - α_adjusted = α / jumlah_perbandingan
        
        ---
        
        ## 💡 TIPS PRAKTIS
        
        ### 1. **Selalu Cek Asumsi**
        
        ```python
        # Cek expected frequency
        if any(expected < 5):
            print("Warning: Expected frequency < 5")
            print("Consider combining categories")
        ```
        
        ### 2. **Visualisasi**
        
        - Gunakan **bar chart** untuk compare observed vs expected
        - Gunakan **mosaic plot** untuk tabel kontingensi
        
        ### 3. **Interpretasi Kontekstual**
        
        - Jangan hanya lihat p-value
        - Lihat **magnitude** perbedaan
        - Pertimbangkan **practical significance**
        
        ### 4. **Report Lengkap**
        
        Selalu report:
        - χ² statistic
        - Degrees of freedom
        - p-value
        - Effect size (Cramér's V)
        - Interpretasi dalam konteks
        
        **Contoh:**
        ```
        χ²(2, N=300) = 18.75, p < 0.001, V = 0.25
        
        Interpretasi:
        Terdapat perbedaan signifikan dalam proporsi adopsi
        teknologi di ketiga daerah (χ² = 18.75, p < 0.001).
        Effect size sedang (V = 0.25) menunjukkan perbedaan
        yang cukup substansial secara praktis.
        ```
        
        ---
        
        ## 📚 APLIKASI DALAM PENELITIAN PERTANIAN
        
        ### 1. **Adopsi Teknologi**
        - Uji homogenitas adopsi di berbagai daerah
        - Uji kepatutan proporsi adopsi vs target
        
        ### 2. **Preferensi Varietas**
        - Uji apakah petani memilih varietas secara merata
        - Uji perbedaan preferensi antar kelompok
        
        ### 3. **Distribusi Penyakit**
        - Uji apakah distribusi penyakit sama di berbagai lokasi
        - Uji kepatutan dengan distribusi teoritis
        
        ### 4. **Kategori Hasil Panen**
        - Uji homogenitas distribusi kualitas (A, B, C) antar daerah
        - Uji kepatutan dengan standar industri
        
        ### 5. **Survei Petani**
        - Uji apakah distribusi jawaban sama antar kelompok
        - Uji kepatutan dengan expected response pattern
        
        """)  # End of Chi-Square sub-tab
    
    # ===== SUB-TAB 6: TEOREMA BAYES =====
    with subtab_bayes:
        st.subheader("🎲 Teorema Bayes & Probabilitas")
        
        st.markdown("""
        ## 🎲 PELUANG BERBAGAI KEJADIAN
        
        ### Konsep Dasar Probabilitas
        
        **Probabilitas (Peluang)** adalah ukuran kemungkinan suatu kejadian terjadi, dengan nilai antara 0 dan 1.
        
        $$0 \\leq P(A) \\leq 1$$
        
        **Interpretasi:**
        - **P(A) = 0** → Kejadian A tidak mungkin terjadi
        - **P(A) = 1** → Kejadian A pasti terjadi
        - **P(A) = 0.5** → Kejadian A memiliki peluang 50%
        
        **Contoh Pertanian:**
        - P(Hujan besok) = 0.7 → Peluang hujan 70%
        - P(Panen gagal) = 0.1 → Peluang gagal panen 10%
        - P(Harga naik) = 0.6 → Peluang harga naik 60%
        
        ---
        
        ### 1. Aturan Dasar Probabilitas
        
        #### A. Complement Rule (Aturan Komplemen)
        
        $$P(A^c) = 1 - P(A)$$
        
        Dimana A^c = kejadian A tidak terjadi
        
        **Contoh:**
        ```
        P(Hujan) = 0.7
        P(Tidak Hujan) = 1 - 0.7 = 0.3
        ```
        
        #### B. Addition Rule (Aturan Penjumlahan)
        
        **Untuk kejadian mutually exclusive (saling lepas):**
        
        $$P(A \\cup B) = P(A) + P(B)$$
        
        **Untuk kejadian umum:**
        
        $$P(A \\cup B) = P(A) + P(B) - P(A \\cap B)$$
        
        **Contoh:**
        ```
        P(Harga naik) = 0.4
        P(Harga turun) = 0.3
        P(Harga stabil) = 0.3
        
        P(Harga naik ATAU turun) = 0.4 + 0.3 = 0.7
        (karena mutually exclusive)
        ```
        
        #### C. Multiplication Rule (Aturan Perkalian)
        
        **Untuk kejadian independen:**
        
        $$P(A \\cap B) = P(A) \\times P(B)$$
        
        **Untuk kejadian dependen:**
        
        $$P(A \\cap B) = P(A) \\times P(B|A)$$
        
        **Contoh Independen:**
        ```
        P(Hujan di Lahan A) = 0.7
        P(Hujan di Lahan B) = 0.6
        
        P(Hujan di A DAN B) = 0.7 × 0.6 = 0.42
        (jika independen)
        ```
        
        ---
        
        ### 2. Probabilitas Bersyarat (Conditional Probability)
        
        **Definisi:**
        
        Probabilitas kejadian A terjadi **JIKA** kejadian B sudah terjadi.
        
        $$P(A|B) = \\frac{P(A \\cap B)}{P(B)}$$
        
        **Dibaca:** "Probabilitas A given B"
        
        **Contoh:**
        
        ```
        P(Panen Berhasil | Cuaca Baik) = ?
        
        P(Panen Berhasil ∩ Cuaca Baik) = 0.56
        P(Cuaca Baik) = 0.7
        
        P(Panen Berhasil | Cuaca Baik) = 0.56 / 0.7 = 0.8
        
        Interpretasi:
        Jika cuaca baik, peluang panen berhasil adalah 80%
        ```
        
        ---
        
        ### 3. Independensi vs Dependensi
        
        **Kejadian Independen:**
        
        A dan B independen jika:
        
        $$P(A|B) = P(A)$$
        
        Artinya: Kejadian B tidak mempengaruhi probabilitas A
        
        **Contoh Independen:**
        - Hasil lempar koin pertama vs kedua
        - Cuaca di Jakarta vs cuaca di Surabaya
        
        **Kejadian Dependen:**
        
        $$P(A|B) \\neq P(A)$$
        
        **Contoh Dependen:**
        - Cuaca vs Hasil Panen
        - Harga Pupuk vs Biaya Produksi
        - Adopsi Teknologi vs Produktivitas
        
        ---
        
        ### 4. Law of Total Probability
        
        Jika B₁, B₂, ..., Bₙ adalah partisi dari sample space:
        
        $$P(A) = \\sum_{i=1}^{n} P(A|B_i) \\times P(B_i)$$
        
        **Contoh:**
        
        ```
        Hitung P(Panen Berhasil) dengan 3 kondisi cuaca:
        
        P(Berhasil | Baik) = 0.9,  P(Baik) = 0.5
        P(Berhasil | Sedang) = 0.6,  P(Sedang) = 0.3
        P(Berhasil | Buruk) = 0.2,  P(Buruk) = 0.2
        
        P(Berhasil) = 0.9×0.5 + 0.6×0.3 + 0.2×0.2
                    = 0.45 + 0.18 + 0.04
                    = 0.67 (67%)
        ```
        
        ---
        
        ## 📊 TEOREMA BAYES
        
        ### Apa itu Teorema Bayes?
        
        **Teorema Bayes** adalah formula untuk **memperbarui** probabilitas berdasarkan **informasi baru**.
        
        **Formula:**
        
        $$P(A|B) = \\frac{P(B|A) \\times P(A)}{P(B)}$$
        
        Atau lebih lengkap:
        
        $$P(A|B) = \\frac{P(B|A) \\times P(A)}{P(B|A) \\times P(A) + P(B|A^c) \\times P(A^c)}$$
        
        **Komponen:**
        - **P(A|B)** = **Posterior** (probabilitas A setelah tahu B)
        - **P(B|A)** = **Likelihood** (probabilitas B jika A benar)
        - **P(A)** = **Prior** (probabilitas A sebelum tahu B)
        - **P(B)** = **Evidence** (probabilitas B total)
        
        ---
        
        ### Interpretasi Bayesian
        
        **Bayesian Thinking:**
        
        ```
        Prior Belief + New Evidence → Updated Belief (Posterior)
        ```
        
        **Contoh Sederhana:**
        
        ```
        Prior: "Saya pikir peluang hujan 30%"
        Evidence: "Langit mendung"
        Posterior: "Sekarang saya pikir peluang hujan 70%"
        ```
        
        Teorema Bayes memberikan cara **matematis** untuk update belief!
        
        ---
        
        ### Contoh 1: Diagnosis Penyakit Tanaman
        
        **Kasus:**
        
        Petani ingin tahu apakah tanamannya terkena penyakit layu berdasarkan gejala daun kuning.
        
        **Informasi:**
        - P(Penyakit Layu) = 0.05 (5% tanaman terkena)
        - P(Daun Kuning | Penyakit Layu) = 0.90 (90% tanaman sakit punya daun kuning)
        - P(Daun Kuning | Sehat) = 0.10 (10% tanaman sehat juga punya daun kuning)
        
        **Pertanyaan:**
        
        Jika tanaman punya daun kuning, berapa peluang terkena penyakit layu?
        
        **Solusi:**
        
        ```
        P(Layu | Kuning) = ?
        
        P(Kuning | Layu) = 0.90
        P(Layu) = 0.05
        P(Sehat) = 0.95
        P(Kuning | Sehat) = 0.10
        
        P(Kuning) = P(Kuning|Layu)×P(Layu) + P(Kuning|Sehat)×P(Sehat)
                  = 0.90×0.05 + 0.10×0.95
                  = 0.045 + 0.095
                  = 0.14
        
        P(Layu | Kuning) = (0.90 × 0.05) / 0.14
                         = 0.045 / 0.14
                         = 0.321 (32.1%)
        ```
        
        **Interpretasi:**
        
        - **Sebelum** lihat daun kuning: P(Layu) = 5%
        - **Setelah** lihat daun kuning: P(Layu|Kuning) = 32.1%
        - Informasi baru **meningkatkan** peluang dari 5% → 32.1%
        - Tapi masih **lebih mungkin sehat** (67.9%) daripada sakit
        
        **Rekomendasi:**
        - Lakukan tes lebih lanjut
        - Cek gejala lain
        - Jangan langsung semprot pestisida
        
        ---
        
        ### Contoh 2: Kualitas Benih
        
        **Kasus:**
        
        Petani beli benih dari 3 supplier berbeda. Ingin tahu dari supplier mana benih yang gagal tumbuh berasal.
        
        **Informasi:**
        
        | Supplier | % Pembelian | % Gagal Tumbuh |
        |----------|-------------|----------------|
        | A        | 50%         | 5%             |
        | B        | 30%         | 10%            |
        | C        | 20%         | 15%            |
        
        **Pertanyaan:**
        
        Jika ada benih yang gagal tumbuh, berapa peluang berasal dari Supplier A, B, atau C?
        
        **Solusi:**
        
        ```
        P(A) = 0.50,  P(Gagal|A) = 0.05
        P(B) = 0.30,  P(Gagal|B) = 0.10
        P(C) = 0.20,  P(Gagal|C) = 0.15
        
        P(Gagal) = 0.05×0.50 + 0.10×0.30 + 0.15×0.20
                 = 0.025 + 0.030 + 0.030
                 = 0.085 (8.5%)
        
        P(A|Gagal) = (0.05 × 0.50) / 0.085 = 0.294 (29.4%)
        P(B|Gagal) = (0.10 × 0.30) / 0.085 = 0.353 (35.3%)
        P(C|Gagal) = (0.15 × 0.20) / 0.085 = 0.353 (35.3%)
        ```
        
        **Interpretasi:**
        
        - Meskipun 50% benih dari A, hanya 29.4% benih gagal dari A
        - B dan C punya peluang sama (35.3%) sebagai sumber benih gagal
        - **Rekomendasi:** Kurangi pembelian dari B dan C
        
        ---
        
        ### Contoh 3: Prediksi Cuaca & Keputusan Tanam
        
        **Kasus:**
        
        Petani ingin tanam besok. Ramalan cuaca bilang 70% hujan. Tapi ramalan sering salah.
        
        **Informasi:**
        
        - P(Hujan) = 0.30 (30% hari dalam setahun hujan)
        - P(Ramalan Hujan | Hujan) = 0.80 (80% akurat jika memang hujan)
        - P(Ramalan Hujan | Tidak Hujan) = 0.20 (20% false alarm)
        
        **Pertanyaan:**
        
        Jika ramalan bilang hujan, berapa peluang **benar-benar** hujan?
        
        **Solusi:**
        
        ```
        P(Hujan | Ramalan Hujan) = ?
        
        P(Ramalan Hujan) = 0.80×0.30 + 0.20×0.70
                         = 0.24 + 0.14
                         = 0.38
        
        P(Hujan | Ramalan Hujan) = (0.80 × 0.30) / 0.38
                                  = 0.24 / 0.38
                                  = 0.632 (63.2%)
        ```
        
        **Interpretasi:**
        
        - Ramalan bilang 70% hujan
        - Tapi peluang **sebenarnya** hanya 63.2%
        - Masih ada 36.8% peluang tidak hujan
        
        **Keputusan:**
        - Jika tanaman tahan hujan → Tanam
        - Jika tanaman sensitif → Tunda 1 hari
        
        ---
        
        ## 📈 APLIKASI TEOREMA BAYES DALAM PERTANIAN
        
        ### 1. Diagnosis Penyakit & Hama
        
        **Update probabilitas penyakit berdasarkan gejala:**
        
        ```
        Prior: Prevalensi penyakit di daerah
        Evidence: Gejala yang diamati
        Posterior: Peluang penyakit setelah lihat gejala
        ```
        
        **Manfaat:**
        - Diagnosis lebih akurat
        - Hindari over-treatment
        - Hemat biaya pestisida
        
        ### 2. Kualitas Produk
        
        **Update probabilitas sumber masalah:**
        
        ```
        Prior: Distribusi supplier/batch
        Evidence: Produk defect
        Posterior: Peluang dari supplier tertentu
        ```
        
        **Manfaat:**
        - Identifikasi supplier bermasalah
        - Quality control lebih baik
        - Keputusan pembelian lebih informed
        
        ### 3. Prediksi Cuaca & Iklim
        
        **Update probabilitas cuaca berdasarkan ramalan:**
        
        ```
        Prior: Pola cuaca historis
        Evidence: Ramalan cuaca
        Posterior: Peluang cuaca adjusted
        ```
        
        **Manfaat:**
        - Keputusan tanam lebih baik
        - Manajemen risiko
        - Optimasi jadwal panen
        
        ### 4. Adopsi Teknologi
        
        **Update probabilitas sukses berdasarkan karakteristik petani:**
        
        ```
        Prior: Success rate teknologi
        Evidence: Profil petani (pendidikan, luas lahan, dll)
        Posterior: Peluang sukses untuk petani ini
        ```
        
        **Manfaat:**
        - Targeting program lebih tepat
        - Customized recommendations
        - Prediksi adopsi lebih akurat
        
        ### 5. Market Intelligence
        
        **Update probabilitas harga berdasarkan informasi:**
        
        ```
        Prior: Pola harga historis
        Evidence: Berita, kebijakan, produksi
        Posterior: Prediksi harga updated
        ```
        
        **Manfaat:**
        - Timing penjualan lebih baik
        - Hedging decisions
        - Inventory management
        
        ---
        
        ## 💡 BAYESIAN vs FREQUENTIST
        
        ### Perbedaan Filosofi
        
        | Aspek | Frequentist | Bayesian |
        |-------|-------------|----------|
        | **Probabilitas** | Frekuensi jangka panjang | Degree of belief |
        | **Parameter** | Fixed (unknown) | Random variable |
        | **Prior** | Tidak ada | Ada (subjective) |
        | **Update** | Tidak | Ya (dengan data baru) |
        | **Contoh** | t-test, ANOVA | Bayesian inference |
        
        ### Kapan Gunakan Bayesian?
        
        **Gunakan Bayesian jika:**
        - Ada **prior knowledge** yang kuat
        - Data **terbatas** (small sample)
        - Perlu **update** belief secara bertahap
        - Decision making **sequential**
        
        **Gunakan Frequentist jika:**
        - **Tidak ada** prior knowledge
        - Data **banyak** (large sample)
        - Perlu **objektif** (no subjectivity)
        - Analisis **one-time**
        
        ---
        
        ## ⚠️ PERINGATAN PENTING
        
        ### 1. Prior Sensitivity
        
        - Hasil Bayesian **sensitif** terhadap prior
        - Prior yang salah → Posterior yang salah
        - **Solusi:** Gunakan **non-informative prior** jika tidak yakin
        
        ### 2. Base Rate Fallacy
        
        **Jangan abaikan base rate (prior)!**
        
        **Contoh:**
        
        ```
        Tes penyakit 99% akurat
        Tapi prevalensi penyakit hanya 0.1%
        
        Jika tes positif:
        P(Sakit | Positif) ≈ 9% (BUKAN 99%!)
        ```
        
        ### 3. Conditional Probability Confusion
        
        **P(A|B) ≠ P(B|A)**
        
        **Contoh:**
        - P(Hujan | Mendung) ≠ P(Mendung | Hujan)
        - P(Penyakit | Gejala) ≠ P(Gejala | Penyakit)
        
        ### 4. Independence Assumption
        
        - Teorema Bayes assume **conditional independence**
        - Jika asumsi dilanggar → Hasil bias
        - **Solusi:** Gunakan **Bayesian Network** untuk dependensi kompleks
        
        ---
        
        ## 🎯 TIPS PRAKTIS
        
        ### 1. Visualisasi
        
        Gunakan **tree diagram** atau **probability tree** untuk visualisasi:
        
        ```
        Penyakit (5%)
            ├─ Kuning (90%)
            └─ Tidak Kuning (10%)
        
        Sehat (95%)
            ├─ Kuning (10%)
            └─ Tidak Kuning (90%)
        ```
        
        ### 2. Sensitivity Analysis
        
        - Coba berbagai **prior** yang reasonable
        - Lihat seberapa **robust** posterior
        - Jika posterior stabil → Hasil reliable
        
        ### 3. Update Iteratif
        
        - Posterior hari ini = Prior besok
        - Update terus dengan data baru
        - **Bayesian learning** = continuous improvement
        
        ### 4. Komunikasi
        
        Jelaskan dalam bahasa sederhana:
        
        ```
        "Sebelumnya saya pikir peluangnya 30%,
         tapi setelah lihat bukti baru,
         sekarang saya pikir peluangnya 60%"
        ```
        
        ### 5. Software
        
        - **Python:** `scipy.stats`, `pymc3`
        - **R:** `BayesFactor`, `rstan`
        - **Excel:** Bisa manual dengan formula
        
        ---
        
        ## 📚 KESIMPULAN
        
        **Teorema Bayes adalah tool powerful untuk:**
        
        1. **Update belief** dengan informasi baru
        2. **Decision making** under uncertainty
        3. **Diagnosis** dan troubleshooting
        4. **Prediction** yang lebih akurat
        5. **Learning** dari data secara bertahap
        
        **Key Takeaways:**
        
        - Probabilitas bisa **diupdate** dengan evidence
        - **Prior knowledge** penting (jangan diabaikan)
        - **Base rate** sangat berpengaruh
        - Bayesian thinking = **rational** way to update beliefs
        
        **Dalam Pertanian:**
        
        Teorema Bayes membantu petani membuat **keputusan lebih baik** dengan:
        - Menggabungkan **pengalaman** (prior) dan **data baru** (evidence)
        - Update **prediksi** secara real-time
        - **Quantify uncertainty** dalam decision making
        
        """)  # End of Bayes' Theorem sub-tab
    
    # ===== SUB-TAB 7: TEORI KEPUTUSAN =====
    with subtab_decision:
        st.subheader("🎯 Teori Keputusan (Decision Theory)")
        
        st.markdown("""
        ## 🎯 TEORI KEPUTUSAN
        
        ### Apa itu Teori Keputusan?
        
        **Teori Keputusan** adalah framework sistematis untuk membuat **keputusan optimal** dalam kondisi **ketidakpastian** atau **risiko**.
        
        **Komponen Keputusan:**
        
        1. **Decision Alternatives** (Alternatif keputusan)
        2. **States of Nature** (Kondisi alam/kejadian)
        3. **Payoffs** (Hasil/konsekuensi)
        4. **Decision Criteria** (Kriteria keputusan)
        
        **Contoh Pertanian:**
        
        ```
        Keputusan: Tanaman apa yang ditanam?
        Alternatif: Padi, Jagung, Kedelai
        States of Nature: Cuaca (Baik, Sedang, Buruk)
        Payoffs: Profit (juta rupiah)
        Kriteria: Maksimalkan profit
        ```
        
        ---
        
        ### Payoff Matrix (Matriks Hasil)
        
        **Format:**
        
        | Alternatif | State 1 | State 2 | State 3 |
        |------------|---------|---------|---------|
        | A1         | Payoff  | Payoff  | Payoff  |
        | A2         | Payoff  | Payoff  | Payoff  |
        | A3         | Payoff  | Payoff  | Payoff  |
        
        **Contoh:**
        
        | Tanaman | Cuaca Baik | Cuaca Sedang | Cuaca Buruk |
        |---------|------------|--------------|-------------|
        | Padi    | 50 juta    | 30 juta      | 10 juta     |
        | Jagung  | 60 juta    | 25 juta      | 5 juta      |
        | Kedelai | 40 juta    | 35 juta      | 20 juta     |
        
        ---
        
        ## A. PENGAMBILAN KEPUTUSAN PADA KONDISI TIDAK PASTI
        
        ### Karakteristik
        
        - **Tidak ada informasi** tentang probabilitas states of nature
        - **Pure uncertainty** (ketidakpastian murni)
        - Hanya tahu **kemungkinan** yang bisa terjadi
        - **Tidak bisa** hitung expected value
        
        **Kapan terjadi:**
        - Situasi baru (no historical data)
        - Perubahan drastis (paradigm shift)
        - Black swan events
        
        ---
        
        ### 1. MAXIMIN CRITERION (Pessimistic/Conservative)
        
        **Prinsip:** "Pilih alternatif dengan **worst-case terbaik**"
        
        **Langkah:**
        1. Untuk setiap alternatif, cari payoff **minimum**
        2. Pilih alternatif dengan **maksimum** dari minimum tersebut
        
        **Filosofi:** **Risk-averse** (hindari risiko)
        
        **Contoh:**
        
        | Tanaman | Cuaca Baik | Cuaca Sedang | Cuaca Buruk | **MIN** |
        |---------|------------|--------------|-------------|---------|
        | Padi    | 50         | 30           | 10          | **10**  |
        | Jagung  | 60         | 25           | 5           | **5**   |
        | Kedelai | 40         | 35           | 20          | **20** ✅|
        
        **Keputusan:** Tanam **Kedelai** (worst-case = 20 juta, paling tinggi)
        
        **Interpretasi:**
        - Jika cuaca buruk, Kedelai masih untung 20 juta
        - Padi worst-case 10 juta, Jagung hanya 5 juta
        - **Cocok untuk:** Petani risk-averse, modal terbatas
        
        ---
        
        ### 2. MAXIMAX CRITERION (Optimistic/Aggressive)
        
        **Prinsip:** "Pilih alternatif dengan **best-case terbaik**"
        
        **Langkah:**
        1. Untuk setiap alternatif, cari payoff **maksimum**
        2. Pilih alternatif dengan **maksimum** dari maksimum tersebut
        
        **Filosofi:** **Risk-seeking** (cari peluang maksimal)
        
        **Contoh:**
        
        | Tanaman | Cuaca Baik | Cuaca Sedang | Cuaca Buruk | **MAX** |
        |---------|------------|--------------|-------------|---------|
        | Padi    | 50         | 30           | 10          | **50**  |
        | Jagung  | 60         | 25           | 5           | **60** ✅|
        | Kedelai | 40         | 35           | 20          | **40**  |
        
        **Keputusan:** Tanam **Jagung** (best-case = 60 juta, paling tinggi)
        
        **Interpretasi:**
        - Jika cuaca baik, Jagung untung 60 juta (tertinggi)
        - Abaikan worst-case (optimis cuaca akan baik)
        - **Cocok untuk:** Petani risk-taker, modal besar
        
        ---
        
        ### 3. MINIMAX REGRET CRITERION
        
        **Prinsip:** "Minimalisir **penyesalan maksimum**"
        
        **Regret (Opportunity Loss):** Selisih antara payoff terbaik dengan payoff yang dipilih
        
        **Langkah:**
        
        1. **Buat Regret Matrix:**
           - Untuk setiap state, cari payoff maksimum
           - Regret = Max Payoff - Actual Payoff
        
        2. **Untuk setiap alternatif, cari regret maksimum**
        
        3. **Pilih alternatif dengan minimum regret maksimum**
        
        **Contoh:**
        
        **Payoff Matrix:**
        
        | Tanaman | Cuaca Baik | Cuaca Sedang | Cuaca Buruk |
        |---------|------------|--------------|-------------|
        | Padi    | 50         | 30           | 10          |
        | Jagung  | 60         | 25           | 5           |
        | Kedelai | 40         | 35           | 20          |
        | **MAX** | **60**     | **35**       | **20**      |
        
        **Regret Matrix:**
        
        | Tanaman | Cuaca Baik | Cuaca Sedang | Cuaca Buruk | **MAX Regret** |
        |---------|------------|--------------|-------------|----------------|
        | Padi    | 60-50=10   | 35-30=5      | 20-10=10    | **10** ✅      |
        | Jagung  | 60-60=0    | 35-25=10     | 20-5=15     | **15**         |
        | Kedelai | 60-40=20   | 35-35=0      | 20-20=0     | **20**         |
        
        **Keputusan:** Tanam **Padi** (max regret = 10 juta, paling kecil)
        
        **Interpretasi:**
        - Padi: Penyesalan maksimum hanya 10 juta
        - Jagung: Bisa menyesal 15 juta (jika cuaca buruk)
        - Kedelai: Bisa menyesal 20 juta (jika cuaca baik)
        - **Cocok untuk:** Petani yang tidak mau menyesal banyak
        
        ---
        
        ### 4. LAPLACE CRITERION (Equal Likelihood)
        
        **Prinsip:** "Semua states **equally likely**" (probabilitas sama)
        
        **Langkah:**
        1. Hitung rata-rata payoff untuk setiap alternatif
        2. Pilih alternatif dengan rata-rata tertinggi
        
        **Formula:**
        
        $$\\text{Average Payoff} = \\frac{\\sum \\text{Payoffs}}{n}$$
        
        **Contoh:**
        
        | Tanaman | Cuaca Baik | Cuaca Sedang | Cuaca Buruk | **Average** |
        |---------|------------|--------------|-------------|-------------|
        | Padi    | 50         | 30           | 10          | 30.0        |
        | Jagung  | 60         | 25           | 5           | 30.0        |
        | Kedelai | 40         | 35           | 20          | **31.7** ✅ |
        
        ```
        Padi: (50 + 30 + 10) / 3 = 30.0
        Jagung: (60 + 25 + 5) / 3 = 30.0
        Kedelai: (40 + 35 + 20) / 3 = 31.7
        ```
        
        **Keputusan:** Tanam **Kedelai** (rata-rata tertinggi)
        
        **Interpretasi:**
        - Kedelai paling **konsisten** di semua kondisi
        - Padi dan Jagung rata-rata sama tapi lebih **volatile**
        - **Cocok untuk:** Tidak ada informasi probabilitas
        
        ---
        
        ### 5. HURWICZ CRITERION (Realism)
        
        **Prinsip:** "Kombinasi **optimism** dan **pessimism**"
        
        **Formula:**
        
        $$H = \\alpha \\times \\text{MAX} + (1-\\alpha) \\times \\text{MIN}$$
        
        Dimana:
        - **α** = Coefficient of optimism (0 ≤ α ≤ 1)
        - **α = 1** → Maximax (sangat optimis)
        - **α = 0** → Maximin (sangat pesimis)
        - **α = 0.5** → Moderate (balanced)
        
        **Contoh (α = 0.6):**
        
        | Tanaman | MAX | MIN | **H (α=0.6)** |
        |---------|-----|-----|---------------|
        | Padi    | 50  | 10  | 0.6×50 + 0.4×10 = **34** |
        | Jagung  | 60  | 5   | 0.6×60 + 0.4×5 = **38** ✅|
        | Kedelai | 40  | 20  | 0.6×40 + 0.4×20 = **32** |
        
        **Keputusan:** Tanam **Jagung** (H = 38, tertinggi)
        
        **Interpretasi:**
        - Dengan α = 0.6 (cukup optimis), Jagung terbaik
        - Jika α = 0.3 (pesimis) → Kedelai menang
        - **Cocok untuk:** Adjust sesuai risk appetite
        
        ---
        
        ## B. PENGAMBILAN KEPUTUSAN PADA KONDISI BERESIKO
        
        ### Karakteristik
        
        - **Ada informasi probabilitas** states of nature
        - **Risk** (bukan pure uncertainty)
        - Bisa hitung **expected value**
        - Lebih **objektif** (data-driven)
        
        **Kapan terjadi:**
        - Ada historical data
        - Bisa estimasi probabilitas
        - Situasi berulang
        
        ---
        
        ### 1. EXPECTED MONETARY VALUE (EMV)
        
        **Prinsip:** "Pilih alternatif dengan **expected value tertinggi**"
        
        **Formula:**
        
        $$EMV = \\sum (\\text{Payoff}_i \\times P_i)$$
        
        **Langkah:**
        1. Tentukan probabilitas setiap state
        2. Hitung EMV untuk setiap alternatif
        3. Pilih alternatif dengan EMV maksimum
        
        **Contoh:**
        
        **Probabilitas:** P(Baik) = 0.5, P(Sedang) = 0.3, P(Buruk) = 0.2
        
        | Tanaman | Baik (0.5) | Sedang (0.3) | Buruk (0.2) | **EMV** |
        |---------|------------|--------------|-------------|---------|
        | Padi    | 50         | 30           | 10          | **37**  |
        | Jagung  | 60         | 25           | 5           | **39** ✅|
        | Kedelai | 40         | 35           | 20          | **34.5**|
        
        **Perhitungan:**
        ```
        EMV(Padi) = 50×0.5 + 30×0.3 + 10×0.2 = 25 + 9 + 2 = 37
        EMV(Jagung) = 60×0.5 + 25×0.3 + 5×0.2 = 30 + 7.5 + 1 = 38.5
        EMV(Kedelai) = 40×0.5 + 35×0.3 + 20×0.2 = 20 + 10.5 + 4 = 34.5
        ```
        
        **Keputusan:** Tanam **Jagung** (EMV = 38.5 juta)
        
        **Interpretasi:**
        - Dalam jangka panjang, Jagung rata-rata untung 38.5 juta
        - Lebih tinggi dari Padi (37) dan Kedelai (34.5)
        - **Cocok untuk:** Decision berulang, risk-neutral
        
        ---
        
        ### 2. EXPECTED OPPORTUNITY LOSS (EOL)
        
        **Prinsip:** "Minimalisir **expected regret**"
        
        **Langkah:**
        1. Buat regret matrix (seperti minimax regret)
        2. Hitung EOL = Σ(Regret × Probability)
        3. Pilih alternatif dengan EOL minimum
        
        **Regret Matrix:**
        
        | Tanaman | Baik (0.5) | Sedang (0.3) | Buruk (0.2) | **EOL** |
        |---------|------------|--------------|-------------|---------|
        | Padi    | 10         | 5            | 10          | **8.5** ✅|
        | Jagung  | 0          | 10           | 15          | **8.5** ✅|
        | Kedelai | 20         | 0            | 0           | **10**  |
        
        **Perhitungan:**
        ```
        EOL(Padi) = 10×0.5 + 5×0.3 + 10×0.2 = 5 + 1.5 + 2 = 8.5
        EOL(Jagung) = 0×0.5 + 10×0.3 + 15×0.2 = 0 + 3 + 3 = 6
        EOL(Kedelai) = 20×0.5 + 0×0.3 + 0×0.2 = 10 + 0 + 0 = 10
        ```
        
        **Keputusan:** Tanam **Jagung** (EOL = 6, terendah)
        
        **Note:** EMV dan EOL **selalu konsisten** (pilih alternatif sama)
        
        ---
        
        ### 3. EXPECTED VALUE OF PERFECT INFORMATION (EVPI)
        
        **Definisi:** Nilai maksimum yang layak dibayar untuk **informasi sempurna**
        
        **Formula:**
        
        $$EVPI = EV_{\\text{with PI}} - EV_{\\text{without PI}}$$
        
        Atau:
        
        $$EVPI = \\text{Best EMV} - \\text{EMV of best alternative}$$
        
        **Langkah:**
        
        1. **EV with Perfect Information:**
           - Untuk setiap state, pilih payoff terbaik
           - Hitung expected value
        
        2. **EV without Perfect Information:**
           - EMV dari alternatif terbaik
        
        3. **EVPI = Selisihnya**
        
        **Contoh:**
        
        **EV with Perfect Information:**
        
        | State | Best Payoff | Probability | Weighted |
        |-------|-------------|-------------|----------|
        | Baik  | 60 (Jagung) | 0.5         | 30       |
        | Sedang| 35 (Kedelai)| 0.3         | 10.5     |
        | Buruk | 20 (Kedelai)| 0.2         | 4        |
        | **Total** |         |             | **44.5** |
        
        **EV without Perfect Information:**
        - Best EMV = 38.5 (Jagung)
        
        **EVPI:**
        ```
        EVPI = 44.5 - 38.5 = 6 juta
        ```
        
        **Interpretasi:**
        - Maksimal bayar **6 juta** untuk informasi cuaca sempurna
        - Jika ramalan cuaca harga > 6 juta → Tidak worth it
        - Jika harga ≤ 6 juta → Beli informasi
        
        ---
        
        ### 4. DECISION TREE (Pohon Keputusan)
        
        **Komponen:**
        - **Decision Node** (□) - Keputusan yang kita kontrol
        - **Chance Node** (○) - Kejadian acak (states of nature)
        - **Branches** - Alternatif atau outcomes
        - **Payoffs** - Hasil akhir
        
        **Contoh Sederhana:**
        
        ```
        □ Pilih Tanaman
        ├─ Padi
        │  ├─ ○ Cuaca
        │  │  ├─ Baik (0.5) → 50
        │  │  ├─ Sedang (0.3) → 30
        │  │  └─ Buruk (0.2) → 10
        │  └─ EMV = 37
        │
        ├─ Jagung
        │  ├─ ○ Cuaca
        │  │  ├─ Baik (0.5) → 60
        │  │  ├─ Sedang (0.3) → 25
        │  │  └─ Buruk (0.2) → 5
        │  └─ EMV = 38.5 ✅
        │
        └─ Kedelai
           ├─ ○ Cuaca
           │  ├─ Baik (0.5) → 40
           │  ├─ Sedang (0.3) → 35
           │  └─ Buruk (0.2) → 20
           └─ EMV = 34.5
        ```
        
        **Analisis:** Pilih Jagung (EMV tertinggi)
        
        ---
        
        ## 📊 PERBANDINGAN KRITERIA
        
        ### Decision Under Uncertainty
        
        | Kriteria | Filosofi | Cocok Untuk | Hasil (Contoh) |
        |----------|----------|-------------|----------------|
        | **Maximin** | Pessimistic | Risk-averse | Kedelai |
        | **Maximax** | Optimistic | Risk-seeker | Jagung |
        | **Minimax Regret** | Minimize regret | Avoid regret | Padi |
        | **Laplace** | Equal probability | No info | Kedelai |
        | **Hurwicz** | Balanced | Flexible | Depends on α |
        
        ### Decision Under Risk
        
        | Kriteria | Formula | Interpretasi |
        |----------|---------|--------------|
        | **EMV** | Σ(Payoff × P) | Expected profit |
        | **EOL** | Σ(Regret × P) | Expected regret |
        | **EVPI** | Best - EMV | Value of info |
        
        ---
        
        ## 💡 APLIKASI DALAM AGRIBISNIS
        
        ### 1. Pemilihan Komoditas
        
        **Keputusan:** Tanaman apa yang ditanam musim ini?
        
        **Factors:**
        - Harga pasar (uncertain)
        - Cuaca (risky)
        - Hama/penyakit (uncertain)
        
        **Approach:**
        - Jika ada data historis → EMV
        - Jika no data → Maximin/Laplace
        
        ### 2. Investasi Teknologi
        
        **Keputusan:** Beli traktor atau tidak?
        
        **States:**
        - Luas lahan bertambah (opportunity)
        - Luas lahan tetap
        - Luas lahan berkurang (risk)
        
        **Approach:**
        - Hitung EMV dengan/tanpa traktor
        - Hitung EVPI (value of market research)
        
        ### 3. Timing Penjualan
        
        **Keputusan:** Jual sekarang atau tunggu?
        
        **States:**
        - Harga naik
        - Harga stabil
        - Harga turun
        
        **Approach:**
        - Decision tree multi-period
        - Sequential decision making
        
        ### 4. Asuransi Pertanian
        
        **Keputusan:** Beli asuransi atau tidak?
        
        **States:**
        - Gagal panen (low probability, high loss)
        - Panen normal
        
        **Approach:**
        - EMV dengan/tanpa asuransi
        - Risk premium calculation
        
        ### 5. Diversifikasi
        
        **Keputusan:** Monokultur atau diversifikasi?
        
        **Approach:**
        - Portfolio theory
        - Risk-return tradeoff
        - Correlation analysis
        
        ---
        
        ## ⚠️ PERINGATAN PENTING
        
        ### 1. EMV ≠ Actual Outcome
        
        - EMV adalah **rata-rata jangka panjang**
        - Actual outcome bisa jauh berbeda
        - **Jangan** gunakan EMV untuk one-time decision besar
        
        ### 2. Probability Estimation
        
        - Garbage in, garbage out
        - Probabilitas salah → Keputusan salah
        - **Solusi:** Sensitivity analysis
        
        ### 3. Risk Attitude Matters
        
        - EMV assume **risk-neutral**
        - Petani kecil biasanya **risk-averse**
        - **Solusi:** Gunakan utility theory
        
        ### 4. Non-Monetary Factors
        
        - Tidak semua bisa diukur dengan uang
        - Kesehatan, lingkungan, sosial
        - **Solusi:** Multi-criteria decision analysis
        
        ### 5. Dynamic Environment
        
        - Kondisi berubah seiring waktu
        - Decision tree bisa kompleks
        - **Solusi:** Adaptive decision making
        
        ---
        
        ## 🎯 TIPS PRAKTIS
        
        ### 1. Start Simple
        
        - Mulai dengan payoff matrix sederhana
        - Jangan terlalu banyak alternatif/states
        - 3-5 alternatif, 3-4 states cukup
        
        ### 2. Sensitivity Analysis
        
        **Test berbagai skenario:**
        - Bagaimana jika probabilitas berubah?
        - Bagaimana jika payoff berbeda?
        - Apakah keputusan tetap sama?
        
        ### 3. Combine Criteria
        
        Jangan hanya pakai satu kriteria:
        - Cek EMV (expected value)
        - Cek Maximin (worst-case)
        - Cek Minimax Regret (regret)
        - **Pilih yang konsisten** di beberapa kriteria
        
        ### 4. Use Decision Tree for Complex Decisions
        
        - Sequential decisions
        - Multiple stages
        - Learning opportunities
        
        ### 5. Document Assumptions
        
        Selalu catat:
        - Sumber probabilitas
        - Asumsi payoff
        - Risk attitude
        - Time horizon
        
        ---
        
        ## 📚 KESIMPULAN
        
        **Decision Theory membantu:**
        
        1. **Struktur** keputusan kompleks
        2. **Kuantifikasi** uncertainty dan risk
        3. **Objektif** dalam decision making
        4. **Konsisten** dengan goals
        5. **Defensible** (bisa dijelaskan)
        
        **Key Takeaways:**
        
        - **Uncertainty:** Gunakan Maximin (conservative) atau Laplace (balanced)
        - **Risk:** Gunakan EMV (jika risk-neutral) atau utility (jika risk-averse)
        - **EVPI:** Hitung value of information sebelum beli data
        - **Sensitivity:** Selalu test robustness keputusan
        
        **Dalam Agribisnis:**
        
        Decision theory sangat berguna untuk:
        - **Crop selection** (pilih tanaman)
        - **Investment decisions** (beli alat/teknologi)
        - **Marketing decisions** (timing penjualan)
        - **Risk management** (asuransi, hedging)
        - **Strategic planning** (diversifikasi, ekspansi)
        
        **Remember:**
        
        > "The best decision is not always the one with the highest expected value,
        > but the one that aligns with your risk tolerance and objectives."
        
        """)  # End of Decision Theory sub-tab
    
    # ===== SUB-TAB 8: VISUALISASI & PRAKTIK =====
    with subtab_viz:
        st.subheader("📊 Visualisasi Garis Regresi & Residual")
        
        st.markdown("""
        Visualisasi adalah kunci untuk memahami regresi. Di sini kita akan melihat:
        1. **Scatter Plot + Regression Line** - Garis regresi yang fit dengan data
        2. **Residual Plot** - Untuk cek asumsi homoskedastisitas
        3. **Q-Q Plot** - Untuk cek asumsi normalitas
        """)
        
        # Generate sample data
        st.markdown("---")
        st.markdown("### 🎲 Generate Data Sample")
        
        col_gen1, col_gen2, col_gen3 = st.columns(3)
        
        with col_gen1:
            n_samples = st.slider("Jumlah Data", 20, 200, 50, key='n_samples_reg')
        with col_gen2:
            noise_level = st.slider("Noise Level", 0.0, 50.0, 10.0, key='noise_reg')
        with col_gen3:
            true_slope = st.number_input("True Slope (β)", value=2.5, step=0.1, key='true_slope')
        
        # Generate data
        np.random.seed(42)
        X_demo = np.random.uniform(10, 100, n_samples)
        Y_demo = 50 + true_slope * X_demo + np.random.normal(0, noise_level, n_samples)
        
        # Fit regression
        from sklearn.linear_model import LinearRegression
        model_demo = LinearRegression()
        model_demo.fit(X_demo.reshape(-1, 1), Y_demo)
        
        Y_pred_demo = model_demo.predict(X_demo.reshape(-1, 1))
        residuals = Y_demo - Y_pred_demo
        
        r2_demo = r2_score(Y_demo, Y_pred_demo)
        rmse_demo = np.sqrt(mean_squared_error(Y_demo, Y_pred_demo))
        
        # Display equation
        st.success(f"""
        **Persamaan Regresi yang Ditemukan:**
        
        Y = {model_demo.intercept_:.2f} + {model_demo.coef_[0]:.2f} × X
        
        **Metrik Akurasi:**
        - R² = {r2_demo:.4f} ({r2_demo*100:.2f}% variasi dijelaskan)
        - RMSE = {rmse_demo:.2f}
        """)
        
        # Plot 1: Scatter + Regression Line
        st.markdown("#### 1️⃣ Scatter Plot + Garis Regresi")
        
        fig_scatter = go.Figure()
        
        # Scatter points
        fig_scatter.add_trace(go.Scatter(
            x=X_demo, y=Y_demo,
            mode='markers',
            name='Data Aktual',
            marker=dict(size=8, color='#3b82f6', opacity=0.6)
        ))
        
        # Regression line
        X_line = np.linspace(X_demo.min(), X_demo.max(), 100)
        Y_line = model_demo.intercept_ + model_demo.coef_[0] * X_line
        
        fig_scatter.add_trace(go.Scatter(
            x=X_line, y=Y_line,
            mode='lines',
            name='Garis Regresi',
            line=dict(color='#ef4444', width=3)
        ))
        
        # Add residual lines
        for i in range(min(10, len(X_demo))):  # Show first 10 residuals
            fig_scatter.add_trace(go.Scatter(
                x=[X_demo[i], X_demo[i]],
                y=[Y_demo[i], Y_pred_demo[i]],
                mode='lines',
                line=dict(color='gray', width=1, dash='dot'),
                showlegend=False,
                hoverinfo='skip'
            ))
        
        fig_scatter.update_layout(
            title=f"Regresi Linear: Y = {model_demo.intercept_:.2f} + {model_demo.coef_[0]:.2f}X (R² = {r2_demo:.3f})",
            xaxis_title="X (Variabel Independen)",
            yaxis_title="Y (Variabel Dependen)",
            height=450,
            hovermode='closest'
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        st.caption("""
        **Penjelasan:**
        - **Titik biru** = Data observasi aktual
        - **Garis merah** = Garis regresi (prediksi model)
        - **Garis putus-putus abu-abu** = Residual (jarak vertikal dari titik ke garis)
        """)
        
        # Plot 2: Residual Plot
        st.markdown("#### 2️⃣ Residual Plot (Cek Homoskedastisitas)")
        
        fig_resid = go.Figure()
        
        fig_resid.add_trace(go.Scatter(
            x=Y_pred_demo, y=residuals,
            mode='markers',
            marker=dict(size=8, color='#8b5cf6', opacity=0.6)
        ))
        
        # Add zero line
        fig_resid.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero Line")
        
        fig_resid.update_layout(
            title="Residual Plot - Cek Asumsi Homoskedastisitas",
            xaxis_title="Predicted Values (Ŷ)",
            yaxis_title="Residuals (Y - Ŷ)",
            height=400
        )
        
        st.plotly_chart(fig_resid, use_container_width=True)
        
        st.caption("""
        **Interpretasi:**
        - **Pola acak** di sekitar garis nol = ✅ Asumsi homoskedastisitas terpenuhi
        - **Pola corong/funnel** = ❌ Heteroskedastisitas (varians tidak konstan)
        - **Pola kurva** = ❌ Hubungan non-linear
        """)
        
        # Plot 3: Q-Q Plot
        st.markdown("#### 3️⃣ Q-Q Plot (Cek Normalitas Residual)")
        
        from scipy import stats as sp_stats
        
        # Calculate theoretical quantiles
        sorted_residuals = np.sort(residuals)
        theoretical_quantiles = sp_stats.norm.ppf(np.linspace(0.01, 0.99, len(sorted_residuals)))
        
        fig_qq = go.Figure()
        
        fig_qq.add_trace(go.Scatter(
            x=theoretical_quantiles,
            y=sorted_residuals,
            mode='markers',
            name='Residuals',
            marker=dict(size=8, color='#10b981', opacity=0.6)
        ))
        
        # Add diagonal line
        min_val = min(theoretical_quantiles.min(), sorted_residuals.min())
        max_val = max(theoretical_quantiles.max(), sorted_residuals.max())
        fig_qq.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Normal Line',
            line=dict(color='red', dash='dash')
        ))
        
        fig_qq.update_layout(
            title="Q-Q Plot - Cek Normalitas Residual",
            xaxis_title="Theoretical Quantiles",
            yaxis_title="Sample Quantiles (Residuals)",
            height=400
        )
        
        st.plotly_chart(fig_qq, use_container_width=True)
        
        st.caption("""
        **Interpretasi:**
        - **Titik mengikuti garis diagonal** = ✅ Residual terdistribusi normal
        - **Titik menyimpang dari garis** = ❌ Residual tidak normal (perlu transformasi)
        """)
        
        # ===== APLIKASI PERTANIAN (Merged into Visualization tab) =====
        st.divider()
        st.subheader("🌾 Aplikasi Regresi dalam Ekonomi & Bisnis Pertanian")
        
        st.markdown("""
        Regresi sangat berguna dalam analisis ekonomi pertanian untuk:
        1. **Prediksi Hasil Panen** berdasarkan input produksi
        2. **Analisis Harga** - hubungan harga dengan supply/demand
        3. **Fungsi Produksi** - hubungan input (pupuk, tenaga kerja) dengan output
        4. **Analisis Biaya** - hubungan volume produksi dengan biaya
        5. **Elastisitas** - sensitivitas permintaan terhadap harga
        """)
        
        st.divider()
        
        # Case Study Selector
        case_study = st.selectbox(
            "Pilih Studi Kasus:",
            [
                "📈 Regresi Harga vs Produksi (Supply Curve)",
                "🌾 Fungsi Produksi Padi (Yield vs Pupuk N)",
                "💰 Analisis Biaya (Cost Function)",
                "📊 Elastisitas Permintaan Harga"
            ]
        )
        
        if case_study == "📈 Regresi Harga vs Produksi (Supply Curve)":
            st.markdown("### Studi Kasus: Kurva Penawaran (Supply Curve)")
            
            st.info("""
            **Teori Ekonomi:**
            Hukum penawaran menyatakan bahwa ketika harga naik, produsen cenderung meningkatkan produksi.
            Kita akan menggunakan regresi untuk memodelkan hubungan ini.
            """)
            
            # Generate supply data
            np.random.seed(123)
            harga = np.array([5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000])
            produksi = 50 + 0.003 * harga + np.random.normal(0, 5, len(harga))
            
            # Fit model
            model_supply = LinearRegression()
            model_supply.fit(harga.reshape(-1, 1), produksi)
            produksi_pred = model_supply.predict(harga.reshape(-1, 1))
            
            r2_supply = r2_score(produksi, produksi_pred)
            
            # Display results
            col_supply1, col_supply2 = st.columns(2)
            
            with col_supply1:
                st.markdown("**📊 Data Observasi:**")
                df_supply = pd.DataFrame({
                    'Harga (Rp/kg)': harga,
                    'Produksi (ton)': produksi.round(1),
                    'Prediksi (ton)': produksi_pred.round(1)
                })
                st.dataframe(df_supply, use_container_width=True)
            
            with col_supply2:
                st.markdown("**📐 Hasil Regresi:**")
                st.success(f"""
                **Persamaan Supply:**
                
                Produksi = {model_supply.intercept_:.2f} + {model_supply.coef_[0]:.6f} × Harga
                
                **Metrik:**
                - R² = {r2_supply:.4f}
                - Slope (β) = {model_supply.coef_[0]:.6f}
                """)
                
                st.markdown(f"""
                **💡 Interpretasi Bisnis:**
                
                - **Intercept ({model_supply.intercept_:.2f})**: Produksi dasar ketika harga = 0 (secara teoritis)
                - **Slope ({model_supply.coef_[0]:.6f})**: Setiap kenaikan harga Rp 1.000/kg, produksi naik {model_supply.coef_[0]*1000:.2f} ton
                - **Elastisitas Penawaran**: Positif (sesuai hukum penawaran)
                
                **🎯 Rekomendasi:**
                - Jika target produksi 80 ton, harga optimal = Rp {((80 - model_supply.intercept_) / model_supply.coef_[0]):.0f}/kg
                """)
            
            # Plot
            fig_supply = go.Figure()
            
            fig_supply.add_trace(go.Scatter(
                x=harga, y=produksi,
                mode='markers',
                name='Data Aktual',
                marker=dict(size=10, color='#3b82f6')
            ))
            
            fig_supply.add_trace(go.Scatter(
                x=harga, y=produksi_pred,
                mode='lines',
                name='Supply Curve (Regresi)',
                line=dict(color='#ef4444', width=3)
            ))
            
            fig_supply.update_layout(
                title="Kurva Penawaran (Supply Curve) - Harga vs Produksi",
                xaxis_title="Harga (Rp/kg)",
                yaxis_title="Produksi (ton)",
                height=450
            )
            
            st.plotly_chart(fig_supply, use_container_width=True)
        
        elif case_study == "🌾 Fungsi Produksi Padi (Yield vs Pupuk N)":
            st.markdown("### Studi Kasus: Fungsi Produksi Padi")
            
            st.info("""
            **Teori Agronomi:**
            Hasil panen padi dipengaruhi oleh dosis pupuk Nitrogen (N). Kita akan mencari dosis optimal.
            """)
            
            # Generate production function data
            np.random.seed(456)
            dosis_n = np.array([0, 50, 100, 150, 200, 250, 300, 350, 400])
            # Quadratic relationship (diminishing returns)
            yield_padi = 2000 + 15*dosis_n - 0.025*dosis_n**2 + np.random.normal(0, 200, len(dosis_n))
            
            # Fit linear model (for comparison)
            model_linear = LinearRegression()
            model_linear.fit(dosis_n.reshape(-1, 1), yield_padi)
            yield_pred_linear = model_linear.predict(dosis_n.reshape(-1, 1))
            
            # Fit polynomial model (better fit)
            from sklearn.preprocessing import PolynomialFeatures
            poly = PolynomialFeatures(degree=2)
            dosis_n_poly = poly.fit_transform(dosis_n.reshape(-1, 1))
            model_poly = LinearRegression()
            model_poly.fit(dosis_n_poly, yield_padi)
            yield_pred_poly = model_poly.predict(dosis_n_poly)
            
            r2_linear = r2_score(yield_padi, yield_pred_linear)
            r2_poly = r2_score(yield_padi, yield_pred_poly)
            
            # Display
            col_prod1, col_prod2 = st.columns(2)
            
            with col_prod1:
                st.markdown("**📊 Data Eksperimen:**")
                df_prod = pd.DataFrame({
                    'Dosis N (kg/ha)': dosis_n,
                    'Yield Aktual (kg/ha)': yield_padi.round(0),
                    'Prediksi Linear': yield_pred_linear.round(0),
                    'Prediksi Polynomial': yield_pred_poly.round(0)
                })
                st.dataframe(df_prod, use_container_width=True)
            
            with col_prod2:
                st.markdown("**📐 Perbandingan Model:**")
                
                st.metric("R² Linear", f"{r2_linear:.4f}")
                st.metric("R² Polynomial (deg=2)", f"{r2_poly:.4f}", delta=f"+{(r2_poly-r2_linear):.4f}")
                
                st.success(f"""
                **Model Terbaik: Polynomial Regression**
                
                Yield = {model_poly.intercept_:.2f} + {model_poly.coef_[1]:.2f}×N + {model_poly.coef_[2]:.4f}×N²
                
                **💡 Interpretasi:**
                - Hubungan **non-linear** (diminishing returns)
                - Ada titik optimal dimana tambahan pupuk tidak efektif
                - Model polynomial lebih akurat (R² lebih tinggi)
                """)
            
            # Plot
            fig_prod = go.Figure()
            
            fig_prod.add_trace(go.Scatter(
                x=dosis_n, y=yield_padi,
                mode='markers',
                name='Data Aktual',
                marker=dict(size=12, color='#10b981')
            ))
            
            fig_prod.add_trace(go.Scatter(
                x=dosis_n, y=yield_pred_linear,
                mode='lines',
                name=f'Linear (R²={r2_linear:.3f})',
                line=dict(color='#3b82f6', dash='dash')
            ))
            
            fig_prod.add_trace(go.Scatter(
                x=dosis_n, y=yield_pred_poly,
                mode='lines',
                name=f'Polynomial (R²={r2_poly:.3f})',
                line=dict(color='#ef4444', width=3)
            ))
            
            fig_prod.update_layout(
                title="Fungsi Produksi Padi - Yield vs Dosis Pupuk N",
                xaxis_title="Dosis Pupuk N (kg/ha)",
                yaxis_title="Yield Padi (kg/ha)",
                height=450
            )
            
            st.plotly_chart(fig_prod, use_container_width=True)
            
            st.warning("""
            **⚠️ Pelajaran Penting:**
            - Tidak semua hubungan adalah linear!
            - Dalam agronomi, sering ada **diminishing returns** (hasil marginal menurun)
            - Polynomial regression lebih cocok untuk kasus seperti ini
            - Dosis optimal bisa dihitung dengan mencari titik maksimum kurva
            """)
        
        elif case_study == "💰 Analisis Biaya (Cost Function)":
            st.markdown("### Studi Kasus: Fungsi Biaya Produksi")
            
            st.info("""
            **Teori Ekonomi:**
            Total biaya produksi terdiri dari biaya tetap (fixed cost) dan biaya variabel (variable cost).
            Model: TC = FC + VC×Q
            """)
            
            # Generate cost data
            np.random.seed(789)
            quantity = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
            fixed_cost = 5000000  # Rp 5 juta
            variable_cost_per_unit = 50000  # Rp 50 ribu per unit
            total_cost = fixed_cost + variable_cost_per_unit * quantity + np.random.normal(0, 200000, len(quantity))
            
            # Fit model
            model_cost = LinearRegression()
            model_cost.fit(quantity.reshape(-1, 1), total_cost)
            cost_pred = model_cost.predict(quantity.reshape(-1, 1))
            
            r2_cost = r2_score(total_cost, cost_pred)
            
            # Calculate average cost
            avg_cost = total_cost / quantity
            avg_cost_pred = cost_pred / quantity
            
            # Display
            col_cost1, col_cost2 = st.columns(2)
            
            with col_cost1:
                st.markdown("**📊 Data Biaya:**")
                df_cost = pd.DataFrame({
                    'Quantity (unit)': quantity,
                    'Total Cost (Rp)': total_cost.round(0),
                    'Avg Cost (Rp/unit)': avg_cost.round(0)
                })
                st.dataframe(df_cost, use_container_width=True)
            
            with col_cost2:
                st.markdown("**📐 Hasil Analisis:**")
                st.success(f"""
                **Fungsi Biaya:**
                
                TC = {model_cost.intercept_:.0f} + {model_cost.coef_[0]:.0f} × Q
                
                **Interpretasi:**
                - **Fixed Cost (FC)** = Rp {model_cost.intercept_:,.0f}
                - **Variable Cost (VC)** = Rp {model_cost.coef_[0]:,.0f} per unit
                - **R²** = {r2_cost:.4f}
                
                **💡 Insight Bisnis:**
                - Break-even jika harga jual > Rp {model_cost.coef_[0]:,.0f}/unit
                - Economies of scale: Average cost turun seiring volume naik
                """)
            
            # Plot Total Cost
            fig_cost = go.Figure()
            
            fig_cost.add_trace(go.Scatter(
                x=quantity, y=total_cost,
                mode='markers',
                name='Total Cost Aktual',
                marker=dict(size=10, color='#f59e0b')
            ))
            
            fig_cost.add_trace(go.Scatter(
                x=quantity, y=cost_pred,
                mode='lines',
                name='Total Cost (Regresi)',
                line=dict(color='#ef4444', width=3)
            ))
            
            fig_cost.update_layout(
                title="Fungsi Biaya Total (Total Cost Function)",
                xaxis_title="Quantity (unit)",
                yaxis_title="Total Cost (Rp)",
                height=400
            )
            
            st.plotly_chart(fig_cost, use_container_width=True)
            
            # Plot Average Cost
            fig_avg = go.Figure()
            
            fig_avg.add_trace(go.Scatter(
                x=quantity, y=avg_cost,
                mode='markers+lines',
                name='Average Cost',
                marker=dict(size=8, color='#8b5cf6'),
                line=dict(color='#8b5cf6', dash='dash')
            ))
            
            fig_avg.update_layout(
                title="Average Cost (Economies of Scale)",
                xaxis_title="Quantity (unit)",
                yaxis_title="Average Cost (Rp/unit)",
                height=400
            )
            
            st.plotly_chart(fig_avg, use_container_width=True)
        
        else:  # Elastisitas
            st.markdown("### Studi Kasus: Elastisitas Permintaan Harga")
            
            st.info("""
            **Teori Ekonomi:**
            Elastisitas permintaan mengukur sensitivitas quantity demanded terhadap perubahan harga.
            
            Formula: **E = (ΔQ/Q) / (ΔP/P) = (dQ/dP) × (P/Q)**
            
            - **E > 1**: Elastis (permintaan sangat sensitif terhadap harga)
            - **E = 1**: Unit elastic
            - **E < 1**: Inelastis (permintaan tidak terlalu sensitif)
            """)
            
            # Generate demand data
            np.random.seed(999)
            price = np.array([15000, 14000, 13000, 12000, 11000, 10000, 9000, 8000, 7000, 6000])
            quantity_demanded = 100 - 0.005 * price + np.random.normal(0, 3, len(price))
            
            # Fit model
            model_demand = LinearRegression()
            model_demand.fit(price.reshape(-1, 1), quantity_demanded)
            qty_pred = model_demand.predict(price.reshape(-1, 1))
            
            r2_demand = r2_score(quantity_demanded, qty_pred)
            
            # Calculate elasticity at mean price
            mean_price = price.mean()
            mean_qty = quantity_demanded.mean()
            slope = model_demand.coef_[0]
            elasticity = slope * (mean_price / mean_qty)
            
            # Display
            col_elas1, col_elas2 = st.columns(2)
            
            with col_elas1:
                st.markdown("**📊 Data Permintaan:**")
                df_demand = pd.DataFrame({
                    'Harga (Rp/kg)': price,
                    'Qty Demanded (ton)': quantity_demanded.round(1),
                    'Prediksi (ton)': qty_pred.round(1)
                })
                st.dataframe(df_demand, use_container_width=True)
            
            with col_elas2:
                st.markdown("**📐 Hasil Analisis:**")
                st.success(f"""
                **Fungsi Permintaan:**
                
                Q = {model_demand.intercept_:.2f} + {model_demand.coef_[0]:.6f} × P
                
                **Elastisitas (pada harga rata-rata):**
                
                E = {elasticity:.3f}
                
                **Interpretasi:**
                - Slope negatif = Hukum permintaan terpenuhi ✅
                - |E| = {abs(elasticity):.3f} {'> 1 (Elastis)' if abs(elasticity) > 1 else '< 1 (Inelastis)'}
                - Kenaikan harga 1% → Penurunan qty {abs(elasticity):.2f}%
                """)
                
                if abs(elasticity) > 1:
                    st.warning("**Strategi:** Turunkan harga untuk meningkatkan revenue (permintaan elastis)")
                else:
                    st.info("**Strategi:** Naikkan harga untuk meningkatkan revenue (permintaan inelastis)")
            
            # Plot
            fig_demand = go.Figure()
            
            fig_demand.add_trace(go.Scatter(
                x=price, y=quantity_demanded,
                mode='markers',
                name='Data Aktual',
                marker=dict(size=10, color='#ec4899')
            ))
            
            fig_demand.add_trace(go.Scatter(
                x=price, y=qty_pred,
                mode='lines',
                name='Demand Curve (Regresi)',
                line=dict(color='#ef4444', width=3)
            ))
            
            fig_demand.update_layout(
                title="Kurva Permintaan (Demand Curve) - Harga vs Quantity",
                xaxis_title="Harga (Rp/kg)",
                yaxis_title="Quantity Demanded (ton)",
                height=450
            )
            
            st.plotly_chart(fig_demand, use_container_width=True)
            
            st.markdown(f"""
            **💡 Aplikasi Bisnis:**
            
            1. **Pricing Strategy**: 
               - Jika elastis (|E| > 1): Turunkan harga → Volume naik signifikan → Revenue naik
               - Jika inelastis (|E| < 1): Naikkan harga → Volume turun sedikit → Revenue naik
            
            2. **Revenue Maximization**:
               - Revenue = P × Q
               - Optimal price bisa dicari dengan turunan pertama = 0
            
            3. **Market Segmentation**:
               - Produk premium (inelastis) → Fokus pada kualitas, bisa harga tinggi
               - Produk komoditas (elastis) → Fokus pada efisiensi biaya, harga kompetitif
            """)
        
        st.divider()
        st.markdown("""
        ### 📚 Kesimpulan: Kekuatan Regresi dalam Agribisnis
        
        Analisis regresi adalah alat yang sangat powerful untuk:
        
        ✅ **Prediksi** - Memprediksi hasil, harga, biaya berdasarkan data historis
        
        ✅ **Optimasi** - Menemukan dosis pupuk optimal, harga optimal, dll
        
        ✅ **Decision Making** - Data-driven decisions untuk strategi bisnis
        
        ✅ **Risk Management** - Memahami sensitivitas dan volatilitas
        
        ✅ **Policy Analysis** - Evaluasi dampak kebijakan (subsidi, tarif, dll)
        
        **🎯 Next Steps:**
        - Kembali ke tab "Mode Machine Learning" untuk praktek langsung
        - Upload data Anda sendiri dan coba berbagai model regresi
        - Bandingkan Linear vs Polynomial vs Random Forest
        """)
