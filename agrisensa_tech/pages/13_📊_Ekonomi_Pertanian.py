# Ekonomi Pertanian & Analisis Produksi
# Advanced agricultural economics module with production functions, elasticity analysis, and optimization tools
# Version: 1.0.0

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from scipy.optimize import minimize

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Ekonomi Pertanian", page_icon="📊", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

st.title("📊 Ekonomi Pertanian & Analisis Produksi")
st.markdown("**Platform Analisis Ekonomi Pertanian: Production Functions, Elasticity, Cost-Benefit, dan Optimasi Input**")

# Main tabs
tab_prod, tab_elast, tab_cost, tab_optimal = st.tabs([
    "🏭 Production Function",
    "📈 Elasticity Analysis", 
    "💰 Cost & Profit Analysis",
    "🎯 Optimal Input Calculator"
])

# ==========================================
# TAB 1: PRODUCTION FUNCTION ANALYSIS
# ==========================================
with tab_prod:
    st.header("🏭 Cobb-Douglas Production Function Analysis")
    
    st.markdown("""
    ### Apa itu Fungsi Produksi Cobb-Douglas?
    
    **Fungsi Produksi Cobb-Douglas** adalah model yang menggambarkan hubungan antara input produksi dengan output:
    
    $$Y = A \\cdot K^{\\alpha} \\cdot L^{\\beta}$$
    
    Dimana:
    - **Y** = Output (hasil produksi)
    - **A** = Total Factor Productivity (TFP) - teknologi/efisiensi
    - **K** = Capital (modal: lahan, mesin, pupuk, dll)
    - **L** = Labor (tenaga kerja)
    - **α** = Elastisitas output terhadap capital
    - **β** = Elastisitas output terhadap labor
    
    ---
    
    ### Bentuk Linear (untuk Regresi OLS)
    
    Dengan transformasi logaritma natural:
    
    $$\\ln(Y) = \\ln(A) + \\alpha \\ln(K) + \\beta \\ln(L)$$
    
    Atau:
    
    $$\\ln(Y) = \\beta_0 + \\beta_1 \\ln(K) + \\beta_2 \\ln(L) + u$$
    
    Dimana:
    - **β₀ = ln(A)** → A = e^β₀
    - **β₁ = α** → Elastisitas capital
    - **β₂ = β** → Elastisitas labor
    
    ---
    
    ### Returns to Scale (Skala Hasil)
    
    **RTS = α + β**
    
    - **RTS = 1** → Constant Returns to Scale (CRS)
      - Jika input naik 10%, output naik 10%
    
    - **RTS > 1** → Increasing Returns to Scale (IRS)
      - Jika input naik 10%, output naik >10%
      - Economies of scale
    
    - **RTS < 1** → Decreasing Returns to Scale (DRS)
      - Jika input naik 10%, output naik <10%
      - Diseconomies of scale
    
    ---
    
    ### Interpretasi Koefisien
    
    **Elastisitas (α, β):**
    - α = 0.6 → Jika capital naik 1%, output naik 0.6%
    - β = 0.3 → Jika labor naik 1%, output naik 0.3%
    
    **Marginal Product:**
    - MP_K = ∂Y/∂K = α × (Y/K)
    - MP_L = ∂Y/∂L = β × (Y/L)
    
    **Average Product:**
    - AP_K = Y/K
    - AP_L = Y/L
    """)
    
    st.divider()
    st.subheader("🧮 Interactive Cobb-Douglas Estimator")
    
    # File upload or sample data
    prod_data_source = st.radio("Data Source:", ["Sample Data (Rice Production)", "Upload CSV"], horizontal=True)
    
    if prod_data_source == "Sample Data (Rice Production)":
        # Generate realistic rice production data
        np.random.seed(42)
        n_farms = 100
        
        # Simulate data
        land_area = np.random.uniform(0.5, 5, n_farms)  # hectares
        labor_days = np.random.uniform(20, 100, n_farms)  # person-days
        fertilizer = np.random.uniform(100, 500, n_farms)  # kg
        
        # True parameters: Y = 2 * Land^0.5 * Labor^0.3 * Fertilizer^0.15
        A_true = 2
        alpha_land = 0.5
        alpha_labor = 0.3
        alpha_fert = 0.15
        
        yield_rice = A_true * (land_area ** alpha_land) * (labor_days ** alpha_labor) * (fertilizer ** alpha_fert) * np.exp(np.random.normal(0, 0.1, n_farms))
        
        df_prod = pd.DataFrame({
            'Farm_ID': range(1, n_farms+1),
            'Yield_ton': yield_rice,
            'Land_ha': land_area,
            'Labor_days': labor_days,
            'Fertilizer_kg': fertilizer
        })
        
        st.success("✅ Sample data loaded: 100 rice farms")
        
    else:
        uploaded_prod = st.file_uploader("Upload CSV (columns: Output, Input1, Input2, ...)", type='csv', key='prod_upload')
        if uploaded_prod:
            df_prod = pd.read_csv(uploaded_prod)
            st.success(f"✅ Data loaded: {len(df_prod)} observations")
        else:
            df_prod = None
    
    if df_prod is not None:
        st.write("**Data Preview:**")
        st.dataframe(df_prod.head(10), use_container_width=True)
        
        # Variable selection
        st.divider()
        st.subheader("📊 Model Specification")
        
        col_spec1, col_spec2 = st.columns(2)
        
        with col_spec1:
            output_var = st.selectbox("Output Variable (Y):", df_prod.columns, index=1 if len(df_prod.columns) > 1 else 0)
        
        with col_spec2:
            input_vars = st.multiselect("Input Variables (K, L, ...):", 
                                       [c for c in df_prod.columns if c != output_var],
                                       default=[c for c in df_prod.columns if c != output_var][:3])
        
        if len(input_vars) >= 1 and st.button("🚀 Estimate Production Function", type="primary"):
            # Prepare data
            df_clean = df_prod[[output_var] + input_vars].dropna()
            
            # Check if all selected columns are numeric
            non_numeric = [col for col in [output_var] + input_vars if not pd.api.types.is_numeric_dtype(df_clean[col])]
            if non_numeric:
                st.error(f"⚠️ The following columns must be numeric: {', '.join(non_numeric)}")
            else:
                # Remove non-positive values
                mask = (df_clean[output_var] > 0)
                for var in input_vars:
                    mask &= (df_clean[var] > 0)
                df_clean = df_clean[mask]
                
                if len(df_clean) < 10:
                    st.error("⚠️ Insufficient data after cleaning. Need at least 10 observations with positive values.")
                else:
                    # Log transformation
                    df_log = np.log(df_clean)
                    df_log.columns = ['ln_' + c for c in df_log.columns]
                    
                    # OLS Regression
                    X = df_log[[f'ln_{v}' for v in input_vars]].values
                    y = df_log[f'ln_{output_var}'].values
                    
                    model = LinearRegression()
                    model.fit(X, y)
                    
                    # Results
                    beta_0 = model.intercept_
                    betas = model.coef_
                    r2 = model.score(X, y)
                    
                    # Calculate A (TFP)
                    A_estimated = np.exp(beta_0)
                    
                    # Returns to Scale
                    RTS = sum(betas)
                    
                    # Display Results
                    st.divider()
                    st.subheader("📊 Estimation Results")
                    
                    # Metrics
                    col_m1, col_m2, col_m3 = st.columns(3)
                    
                    with col_m1:
                        st.metric("R² (Goodness of Fit)", f"{r2:.4f}")
                    
                    with col_m2:
                        st.metric("TFP (A)", f"{A_estimated:.4f}")
                    
                    with col_m3:
                        rts_label = "CRS" if abs(RTS - 1) < 0.05 else ("IRS" if RTS > 1 else "DRS")
                        st.metric("Returns to Scale", f"{RTS:.4f}", delta=rts_label)
                    
                    # Estimated Function
                    st.markdown("### 📐 Estimated Production Function")
                    
                    # Build equation string
                    eq_parts = [f"{A_estimated:.4f}"]
                    for i, var in enumerate(input_vars):
                        eq_parts.append(f"{var}^{{{betas[i]:.4f}}}")
                    
                    eq_str = " \\cdot ".join(eq_parts)
                    st.latex(f"\\hat{{Y}} = {eq_str}")
                    
                    # Coefficient Table
                    st.markdown("### 📋 Coefficient Estimates (Elasticities)")
                    
                    coef_df = pd.DataFrame({
                        'Input': input_vars,
                        'Elasticity (β)': betas,
                        'Interpretation': [f"1% ↑ in {v} → {b*100:.2f}% ↑ in output" for v, b in zip(input_vars, betas)]
                    })
                    
                    st.dataframe(coef_df, use_container_width=True)
                    
                    # Returns to Scale Interpretation
                    st.markdown("### 🎯 Returns to Scale Analysis")
                    
                    if abs(RTS - 1) < 0.05:
                        st.success(f"""
                        **Constant Returns to Scale (RTS = {RTS:.4f})**
                        
                        - Jika semua input naik 10%, output akan naik ~10%
                        - Skala produksi optimal bisa besar atau kecil
                        - Tidak ada economies/diseconomies of scale
                        """)
                    elif RTS > 1:
                        st.info(f"""
                        **Increasing Returns to Scale (RTS = {RTS:.4f})**
                        
                        - Jika semua input naik 10%, output akan naik {(RTS-1)*100:.1f}% lebih banyak
                        - **Economies of scale** - lebih efisien di skala besar
                        - **Rekomendasi:** Pertimbangkan ekspansi produksi
                        """)
                    else:
                        st.warning(f"""
                        **Decreasing Returns to Scale (RTS = {RTS:.4f})**
                        
                        - Jika semua input naik 10%, output hanya naik {RTS*10:.1f}%
                        - **Diseconomies of scale** - kurang efisien di skala besar
                        - **Rekomendasi:** Fokus pada efisiensi, bukan ekspansi
                        """)
                    
                    # Marginal Product Calculation
                    st.markdown("### 📊 Marginal Product Analysis")
                    
                    st.info("""
                    **Marginal Product (MP)** = Tambahan output dari 1 unit tambahan input
                    
                    Formula: MP_i = β_i × (Y / X_i)
                    """)
                    
                    # Calculate average values
                    avg_output = df_clean[output_var].mean()
                    
                    mp_data = []
                    for i, var in enumerate(input_vars):
                        avg_input = df_clean[var].mean()
                        mp = betas[i] * (avg_output / avg_input)
                        ap = avg_output / avg_input
                        
                        mp_data.append({
                            'Input': var,
                            'Average Value': f"{avg_input:.2f}",
                            'Marginal Product': f"{mp:.4f}",
                            'Average Product': f"{ap:.4f}",
                            'MP/AP Ratio': f"{mp/ap:.4f}"
                        })
                    
                    mp_df = pd.DataFrame(mp_data)
                    st.dataframe(mp_df, use_container_width=True)
                    
                    # Visualization
                    st.markdown("### 📈 Visualizations")
                    
                    # 1. Actual vs Predicted
                    y_pred = model.predict(X)
                    y_pred_original = np.exp(y_pred)
                    y_actual_original = df_clean[output_var].values
                    
                    fig1 = go.Figure()
                    fig1.add_trace(go.Scatter(
                        x=y_actual_original,
                        y=y_pred_original,
                        mode='markers',
                        name='Observations',
                        marker=dict(size=8, color='blue', opacity=0.6)
                    ))
                    fig1.add_trace(go.Scatter(
                        x=[y_actual_original.min(), y_actual_original.max()],
                        y=[y_actual_original.min(), y_actual_original.max()],
                        mode='lines',
                        name='Perfect Fit',
                        line=dict(color='red', dash='dash')
                    ))
                    fig1.update_layout(
                        title='Actual vs Predicted Output',
                        xaxis_title='Actual Output',
                        yaxis_title='Predicted Output',
                        height=400
                    )
                    st.plotly_chart(fig1, use_container_width=True)
                    
                    # 2. Elasticity Comparison
                    fig2 = px.bar(
                        coef_df,
                        x='Input',
                        y='Elasticity (β)',
                        title='Input Elasticities Comparison',
                        color='Elasticity (β)',
                        color_continuous_scale='Viridis'
                    )
                    fig2.add_hline(y=0, line_dash="dash", line_color="gray")
                    st.plotly_chart(fig2, use_container_width=True)
                    
                    # Policy Recommendations
                    st.divider()
                    st.markdown("### 💡 Policy Recommendations")
                    
                    # Find most elastic input
                    max_elastic_idx = np.argmax(betas)
                    max_elastic_var = input_vars[max_elastic_idx]
                    max_elastic_val = betas[max_elastic_idx]
                    
                    st.success(f"""
                    **Key Findings:**
                    
                    1. **Most Important Input:** {max_elastic_var} (elasticity = {max_elastic_val:.4f})
                       - Fokus pada optimasi input ini untuk hasil maksimal
                       
                    2. **Production Efficiency:** R² = {r2:.4f}
                       - Model menjelaskan {r2*100:.1f}% variasi output
                       
                    3. **Scale Efficiency:** {rts_label}
                       - {"Skala produksi sudah optimal" if abs(RTS-1) < 0.05 else ("Pertimbangkan ekspansi" if RTS > 1 else "Fokus pada efisiensi")}
                    
                    **Actionable Steps:**
                    - Prioritaskan investasi pada {max_elastic_var}
                    - Monitor produktivitas dengan ratio MP/AP
                    - {"Eksplorasi peluang skala ekonomi" if RTS > 1 else "Tingkatkan efisiensi teknis"}
                    """)


# ==========================================
# TAB 2: ELASTICITY ANALYSIS
# ==========================================
with tab_elast:
    st.header("📈 Price Elasticity Analysis")
    
    st.markdown("""
    ### Apa itu Elastisitas?
    
    **Elastisitas** mengukur **sensitivitas** (responsiveness) satu variabel terhadap perubahan variabel lain.
    
    ---
    
    ### 1. Price Elasticity of Demand (PED)
    
    **Definisi:** Persentase perubahan quantity demanded akibat 1% perubahan harga
    
    $$E_d = \\frac{\\% \\Delta Q_d}{\\% \\Delta P} = \\frac{\\partial Q_d}{\\partial P} \\times \\frac{P}{Q_d}$$
    
    **Interpretasi:**
    - **|Ed| > 1** → Elastic (sensitif terhadap harga)
    - **|Ed| = 1** → Unit elastic
    - **|Ed| < 1** → Inelastic (tidak sensitif terhadap harga)
    - **Ed < 0** → Normal (hukum permintaan)
    
    **Contoh Pertanian:**
    - Beras: Ed ≈ -0.3 (inelastic - kebutuhan pokok)
    - Buah premium: Ed ≈ -1.5 (elastic - barang mewah)
    
    ---
    
    ### 2. Price Elasticity of Supply (PES)
    
    **Definisi:** Persentase perubahan quantity supplied akibat 1% perubahan harga
    
    $$E_s = \\frac{\\% \\Delta Q_s}{\\% \\Delta P} = \\frac{\\partial Q_s}{\\partial P} \\times \\frac{P}{Q_s}$$
    
    **Interpretasi:**
    - **Es > 1** → Elastic (mudah menambah produksi)
    - **Es = 1** → Unit elastic
    - **Es < 1** → Inelastic (sulit menambah produksi)
    - **Es > 0** → Normal (hukum penawaran)
    
    **Contoh Pertanian:**
    - Sayuran (short-run): Es ≈ 0.2 (inelastic - musim tanam tetap)
    - Sayuran (long-run): Es ≈ 1.5 (elastic - bisa adjust lahan)
    
    ---
    
    ### 3. Income Elasticity of Demand (YED)
    
    **Definisi:** Persentase perubahan quantity demanded akibat 1% perubahan pendapatan
    
    $$E_y = \\frac{\\% \\Delta Q_d}{\\% \\Delta Y} = \\frac{\\partial Q_d}{\\partial Y} \\times \\frac{Y}{Q_d}$$
    
    **Interpretasi:**
    - **Ey > 1** → Luxury good (barang mewah)
    - **0 < Ey < 1** → Normal good (barang normal)
    - **Ey < 0** → Inferior good (barang inferior)
    
    **Contoh Pertanian:**
    - Beras premium: Ey ≈ 1.2 (luxury)
    - Sayuran: Ey ≈ 0.5 (normal)
    - Singkong: Ey ≈ -0.3 (inferior)
    
    ---
    
    ### 4. Cross-Price Elasticity (CPE)
    
    **Definisi:** Persentase perubahan quantity demanded barang A akibat 1% perubahan harga barang B
    
    $$E_{AB} = \\frac{\\% \\Delta Q_A}{\\% \\Delta P_B} = \\frac{\\partial Q_A}{\\partial P_B} \\times \\frac{P_B}{Q_A}$$
    
    **Interpretasi:**
    - **E_AB > 0** → Substitutes (barang pengganti)
    - **E_AB < 0** → Complements (barang pelengkap)
    - **E_AB = 0** → Independent (tidak berhubungan)
    
    **Contoh Pertanian:**
    - Beras vs Jagung: E ≈ +0.4 (substitutes)
    - Kopi vs Gula: E ≈ -0.2 (complements)
    """)
    
    st.divider()
    st.subheader("🧮 Interactive Elasticity Calculator")
    
    elasticity_type = st.selectbox(
        "Pilih Jenis Elastisitas:",
        ["Price Elasticity of Demand (PED)",
         "Price Elasticity of Supply (PES)",
         "Income Elasticity of Demand (YED)",
         "Cross-Price Elasticity (CPE)"]
    )
    
    # Method selection
    calc_method = st.radio(
        "Metode Kalkulasi:",
        ["Point Elasticity (dari regresi)", "Arc Elasticity (dari 2 titik)"],
        horizontal=True
    )
    
    if calc_method == "Point Elasticity (dari regresi)":
        st.markdown("""
        **Point Elasticity** dihitung dari koefisien regresi:
        
        Untuk model log-log: $\\ln(Q) = \\beta_0 + \\beta_1 \\ln(P) + u$
        
        → Elastisitas = β₁ (langsung!)
        """)
        
        # File upload
        elast_file = st.file_uploader("Upload CSV (columns: Quantity, Price, Income, etc.)", type='csv', key='elast_upload')
        
        if elast_file:
            df_elast = pd.read_csv(elast_file)
            st.write("**Data Preview:**")
            st.dataframe(df_elast.head(), use_container_width=True)
            
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                q_var = st.selectbox("Quantity Variable:", df_elast.columns)
            
            with col_e2:
                if "Demand" in elasticity_type or "Income" in elasticity_type:
                    p_var = st.selectbox("Price/Income Variable:", [c for c in df_elast.columns if c != q_var])
                else:
                    p_var = st.selectbox("Price Variable:", [c for c in df_elast.columns if c != q_var])
            
            if st.button("Calculate Elasticity"):
                # Prepare data
                df_clean = df_elast[[q_var, p_var]].dropna()
                
                # Check if columns are numeric
                if not pd.api.types.is_numeric_dtype(df_clean[q_var]) or not pd.api.types.is_numeric_dtype(df_clean[p_var]):
                    st.error(f"⚠️ Both {q_var} and {p_var} must be numeric columns!")
                else:
                    # Remove non-positive values
                    df_clean = df_clean[(df_clean[q_var] > 0) & (df_clean[p_var] > 0)]
                    
                    if len(df_clean) < 10:
                        st.error("⚠️ Insufficient data. Need at least 10 observations with positive values.")
                    else:
                        ln_q = np.log(df_clean[q_var])
                        ln_p = np.log(df_clean[p_var])
                        
                        # OLS
                        model = LinearRegression()
                        model.fit(ln_p.values.reshape(-1, 1), ln_q.values)
                        
                        elasticity = model.coef_[0]
                        r2 = model.score(ln_p.values.reshape(-1, 1), ln_q.values)
                    
                    # Display result
                    st.success(f"### Estimated Elasticity: **{elasticity:.4f}**")
                    st.metric("R² (Model Fit)", f"{r2:.4f}")
                    
                    # Interpretation
                    if "Demand" in elasticity_type:
                        if abs(elasticity) > 1:
                            st.info(f"**Elastic Demand** (|E| = {abs(elasticity):.2f} > 1): Sangat sensitif terhadap harga")
                        elif abs(elasticity) < 1:
                            st.warning(f"**Inelastic Demand** (|E| = {abs(elasticity):.2f} < 1): Tidak sensitif terhadap harga")
                        else:
                            st.success("**Unit Elastic** (|E| ≈ 1)")
                        
                        st.markdown(f"""
                        **Interpretasi:**
                        - Jika harga naik 1%, quantity demanded akan {"turun" if elasticity < 0 else "naik"} {abs(elasticity):.2f}%
                        - Jika harga naik 10%, quantity demanded akan {"turun" if elasticity < 0 else "naik"} {abs(elasticity)*10:.1f}%
                        """)
                    
                    elif "Supply" in elasticity_type:
                        if elasticity > 1:
                            st.info(f"**Elastic Supply** (E = {elasticity:.2f} > 1): Mudah menambah produksi")
                        elif elasticity < 1:
                            st.warning(f"**Inelastic Supply** (E = {elasticity:.2f} < 1): Sulit menambah produksi")
                        
                        st.markdown(f"""
                        **Interpretasi:**
                        - Jika harga naik 1%, quantity supplied akan naik {elasticity:.2f}%
                        - Jika harga naik 10%, quantity supplied akan naik {elasticity*10:.1f}%
                        """)
                    
                    # Visualization
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=df_clean[p_var],
                        y=df_clean[q_var],
                        mode='markers',
                        name='Data',
                        marker=dict(size=8, opacity=0.6)
                    ))
                    
                    # Add fitted curve
                    p_range = np.linspace(df_clean[p_var].min(), df_clean[p_var].max(), 100)
                    q_fitted = np.exp(model.predict(np.log(p_range).reshape(-1, 1)))
                    
                    fig.add_trace(go.Scatter(
                        x=p_range,
                        y=q_fitted,
                        mode='lines',
                        name=f'Fitted (E={elasticity:.2f})',
                        line=dict(color='red', width=2)
                    ))
                    
                    fig.update_layout(
                        title=f'{elasticity_type} Analysis',
                        xaxis_title=p_var,
                        yaxis_title=q_var,
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    else:  # Arc Elasticity
        st.markdown("""
        **Arc Elasticity** dihitung dari 2 titik data:
        
        $$E = \\frac{Q_2 - Q_1}{P_2 - P_1} \\times \\frac{P_1 + P_2}{Q_1 + Q_2}$$
        
        (Midpoint formula)
        """)
        
        col_arc1, col_arc2 = st.columns(2)
        
        with col_arc1:
            st.markdown("**Point 1 (Before):**")
            q1 = st.number_input("Quantity 1:", value=100.0, step=1.0)
            p1 = st.number_input("Price 1:", value=10.0, step=0.1)
        
        with col_arc2:
            st.markdown("**Point 2 (After):**")
            q2 = st.number_input("Quantity 2:", value=80.0, step=1.0)
            p2 = st.number_input("Price 2:", value=12.0, step=0.1)
        
        if st.button("Calculate Arc Elasticity"):
            # Arc elasticity formula
            if (p2 - p1) == 0:
                st.error("⚠️ Price change cannot be zero!")
            else:
                arc_elast = ((q2 - q1) / (p2 - p1)) * ((p1 + p2) / (q1 + q2))
                
                pct_change_q = ((q2 - q1) / q1) * 100
                pct_change_p = ((p2 - p1) / p1) * 100
                
                st.success(f"### Arc Elasticity: **{arc_elast:.4f}**")
                
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    st.metric("% Change in Quantity", f"{pct_change_q:.2f}%")
                with col_r2:
                    st.metric("% Change in Price", f"{pct_change_p:.2f}%")
                
                # Interpretation
                if abs(arc_elast) > 1:
                    st.info("**Elastic** - Sensitif terhadap perubahan harga")
                elif abs(arc_elast) < 1:
                    st.warning("**Inelastic** - Tidak sensitif terhadap perubahan harga")
                else:
                    st.success("**Unit Elastic**")

# ==========================================
# TAB 3: COST & PROFIT ANALYSIS
# ==========================================
with tab_cost:
    st.header("💰 Cost & Profit Analysis")
    
    st.markdown("""
    ### Analisis Biaya & Keuntungan Usaha Tani
    
    Tool ini membantu Anda menganalisis struktur biaya, menghitung break-even point, dan memaksimalkan profit.
    """)
    
    analysis_type = st.radio(
        "Pilih Jenis Analisis:",
        ["📊 Break-Even Analysis", "💹 Profit Maximization", "📈 Cost Function Analysis"],
        horizontal=True
    )
    
    # ===== BREAK-EVEN ANALYSIS =====
    if analysis_type == "📊 Break-Even Analysis":
        st.divider()
        st.subheader("📊 Break-Even Point Calculator")
        
        st.markdown("""
        ### Apa itu Break-Even Point (BEP)?
        
        **Break-Even Point** adalah titik dimana **Total Revenue = Total Cost** (tidak untung, tidak rugi).
        
        **Formula:**
        
        $$BEP_{unit} = \\frac{Fixed\\ Cost}{Price - Variable\\ Cost\\ per\\ Unit}$$
        
        $$BEP_{rupiah} = BEP_{unit} \\times Price$$
        
        **Margin of Safety:**
        
        $$MOS = \\frac{Actual\\ Sales - BEP\\ Sales}{Actual\\ Sales} \\times 100\\%$$
        """)
        
        st.divider()
        
        # Check if data from Module 28 exists
        if 'economics_data' in st.session_state:
            econ_data = st.session_state['economics_data']
            st.success(f"""
            ✅ **Data Imported from {econ_data.get('source', 'External Source')}**
            
            - Crop: {econ_data.get('crop', 'N/A')}
            - Land Area: {econ_data.get('land_area_ha', 0):.2f} Ha
            - Estimated Yield: {econ_data.get('estimated_yield_kg', 0):,.0f} kg
            - Total Cost: Rp {econ_data.get('total_cost', 0):,.0f}
            """)
            
            if st.button("🔄 Use Imported Data", type="primary"):
                # Auto-populate fields
                fixed_cost_default = econ_data.get('fixed_cost', 10000000.0)
                var_cost_default = econ_data.get('variable_cost_per_unit', 5000.0)
                price_default = econ_data.get('selling_price', 12000.0)
                actual_sales_default = econ_data.get('estimated_yield_kg', 2000.0)
                
                st.session_state['use_imported'] = True
                st.session_state['imported_fc'] = fixed_cost_default
                st.session_state['imported_vc'] = var_cost_default
                st.session_state['imported_price'] = price_default
                st.session_state['imported_sales'] = actual_sales_default
                st.rerun()
            
            if st.button("🗑️ Clear Imported Data"):
                del st.session_state['economics_data']
                if 'use_imported' in st.session_state:
                    del st.session_state['use_imported']
                st.rerun()
            
            st.divider()
        
        # Get default values
        use_imported = st.session_state.get('use_imported', False)
        fc_default = st.session_state.get('imported_fc', 10000000.0) if use_imported else 10000000.0
        vc_default = st.session_state.get('imported_vc', 5000.0) if use_imported else 5000.0
        price_default = st.session_state.get('imported_price', 12000.0) if use_imported else 12000.0
        sales_default = st.session_state.get('imported_sales', 2000.0) if use_imported else 2000.0
        
        col_bep1, col_bep2 = st.columns(2)
        
        with col_bep1:
            st.markdown("**📥 Input Data:**")
            fixed_cost = st.number_input("Fixed Cost (Biaya Tetap) - Rp:", value=fc_default, step=100000.0, format="%.0f")
            st.caption("Contoh: Sewa lahan, penyusutan alat, gaji tetap")
            
            var_cost_per_unit = st.number_input("Variable Cost per Unit - Rp:", value=vc_default, step=100.0, format="%.0f")
            st.caption("Contoh: Bibit, pupuk, pestisida per kg")
            
            selling_price = st.number_input("Selling Price per Unit - Rp:", value=price_default, step=100.0, format="%.0f")
            st.caption("Harga jual per kg/unit")
        
        with col_bep2:
            st.markdown("**📊 Optional - Actual Sales:**")
            actual_sales_units = st.number_input("Actual Sales (units):", value=sales_default, step=10.0, format="%.0f")
            st.caption("Untuk menghitung Margin of Safety")
        
        if st.button("🔍 Calculate Break-Even", type="primary"):
            if selling_price <= var_cost_per_unit:
                st.error("⚠️ Selling price must be greater than variable cost per unit!")
            else:
                # Calculate BEP
                contribution_margin = selling_price - var_cost_per_unit
                bep_units = fixed_cost / contribution_margin
                bep_rupiah = bep_units * selling_price
                
                # Margin of Safety
                actual_sales_rupiah = actual_sales_units * selling_price
                mos_rupiah = actual_sales_rupiah - bep_rupiah
                mos_percentage = (mos_rupiah / actual_sales_rupiah) * 100 if actual_sales_rupiah > 0 else 0
                
                # Profit at actual sales
                total_cost_actual = fixed_cost + (var_cost_per_unit * actual_sales_units)
                total_revenue_actual = selling_price * actual_sales_units
                profit_actual = total_revenue_actual - total_cost_actual
                
                # Display Results
                st.divider()
                st.subheader("📊 Break-Even Analysis Results")
                
                col_r1, col_r2, col_r3 = st.columns(3)
                
                with col_r1:
                    st.metric("BEP (Units)", f"{bep_units:,.0f} units")
                    st.caption("Harus jual minimal ini untuk BEP")
                
                with col_r2:
                    st.metric("BEP (Rupiah)", f"Rp {bep_rupiah:,.0f}")
                    st.caption("Revenue minimal untuk BEP")
                
                with col_r3:
                    st.metric("Contribution Margin", f"Rp {contribution_margin:,.0f}")
                    st.caption("Per unit contribution")
                
                # Margin of Safety
                st.markdown("### 🛡️ Margin of Safety")
                
                col_mos1, col_mos2, col_mos3 = st.columns(3)
                
                with col_mos1:
                    st.metric("MOS (Rupiah)", f"Rp {mos_rupiah:,.0f}")
                
                with col_mos2:
                    st.metric("MOS (%)", f"{mos_percentage:.1f}%")
                
                with col_mos3:
                    profit_color = "normal" if profit_actual >= 0 else "inverse"
                    st.metric("Profit at Actual Sales", f"Rp {profit_actual:,.0f}", delta=profit_color)
                
                # Interpretation
                if mos_percentage > 30:
                    st.success(f"""
                    **✅ Margin of Safety Sangat Baik ({mos_percentage:.1f}%)**
                    
                    - Bisnis Anda memiliki cushion yang besar
                    - Dapat menahan penurunan penjualan hingga {mos_percentage:.1f}% sebelum rugi
                    - Risiko rendah
                    """)
                elif mos_percentage > 15:
                    st.info(f"""
                    **⚠️ Margin of Safety Cukup ({mos_percentage:.1f}%)**
                    
                    - Bisnis cukup aman tapi perlu monitoring
                    - Fokus pada efisiensi biaya
                    """)
                else:
                    st.warning(f"""
                    **⚠️ Margin of Safety Rendah ({mos_percentage:.1f}%)**
                    
                    - Risiko tinggi - dekat dengan BEP
                    - Perlu strategi untuk meningkatkan penjualan atau menurunkan biaya
                    """)
                
                # Visualization
                st.markdown("### 📈 Break-Even Chart")
                
                # Generate data for chart
                units_range = np.linspace(0, bep_units * 2, 100)
                total_cost = fixed_cost + (var_cost_per_unit * units_range)
                total_revenue = selling_price * units_range
                
                fig = go.Figure()
                
                # Total Cost line
                fig.add_trace(go.Scatter(
                    x=units_range,
                    y=total_cost,
                    mode='lines',
                    name='Total Cost',
                    line=dict(color='red', width=2)
                ))
                
                # Total Revenue line
                fig.add_trace(go.Scatter(
                    x=units_range,
                    y=total_revenue,
                    mode='lines',
                    name='Total Revenue',
                    line=dict(color='green', width=2)
                ))
                
                # BEP point
                fig.add_trace(go.Scatter(
                    x=[bep_units],
                    y=[bep_rupiah],
                    mode='markers',
                    name='Break-Even Point',
                    marker=dict(size=15, color='blue', symbol='star')
                ))
                
                # Actual sales point
                if actual_sales_units > 0:
                    fig.add_trace(go.Scatter(
                        x=[actual_sales_units],
                        y=[actual_sales_rupiah],
                        mode='markers',
                        name='Actual Sales',
                        marker=dict(size=12, color='orange', symbol='diamond')
                    ))
                
                fig.update_layout(
                    title='Break-Even Analysis Chart',
                    xaxis_title='Units Sold',
                    yaxis_title='Rupiah',
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Sensitivity Analysis
                st.markdown("### 🔍 Sensitivity Analysis")
                
                st.info("Bagaimana BEP berubah jika ada perubahan harga atau biaya?")
                
                # Price sensitivity
                price_changes = np.array([-20, -10, 0, 10, 20])
                new_prices = selling_price * (1 + price_changes/100)
                bep_price_sensitivity = [fixed_cost / (p - var_cost_per_unit) if p > var_cost_per_unit else np.nan 
                                        for p in new_prices]
                
                # Cost sensitivity
                cost_changes = np.array([-20, -10, 0, 10, 20])
                new_var_costs = var_cost_per_unit * (1 + cost_changes/100)
                bep_cost_sensitivity = [fixed_cost / (selling_price - vc) if selling_price > vc else np.nan 
                                       for vc in new_var_costs]
                
                col_sens1, col_sens2 = st.columns(2)
                
                with col_sens1:
                    st.markdown("**Price Sensitivity:**")
                    sens_price_df = pd.DataFrame({
                        'Price Change (%)': price_changes,
                        'New Price': new_prices,
                        'BEP (units)': bep_price_sensitivity
                    })
                    st.dataframe(sens_price_df.style.format({
                        'New Price': 'Rp {:,.0f}',
                        'BEP (units)': '{:,.0f}'
                    }), use_container_width=True)
                
                with col_sens2:
                    st.markdown("**Variable Cost Sensitivity:**")
                    sens_cost_df = pd.DataFrame({
                        'Cost Change (%)': cost_changes,
                        'New Var Cost': new_var_costs,
                        'BEP (units)': bep_cost_sensitivity
                    })
                    st.dataframe(sens_cost_df.style.format({
                        'New Var Cost': 'Rp {:,.0f}',
                        'BEP (units)': '{:,.0f}'
                    }), use_container_width=True)
    
    # ===== PROFIT MAXIMIZATION =====
    elif analysis_type == "💹 Profit Maximization":
        st.divider()
        st.subheader("💹 Profit Maximization Calculator")
        
        st.markdown("""
        ### Kondisi Profit Maksimum
        
        **Profit maksimum** tercapai ketika:
        
        $$Marginal\\ Revenue (MR) = Marginal\\ Cost (MC)$$
        
        **Untuk pasar kompetitif:**
        - MR = Price (constant)
        - Optimal quantity: dimana P = MC
        
        **Profit:**
        
        $$\\pi = Total\\ Revenue - Total\\ Cost$$
        $$\\pi = (P \\times Q) - (FC + VC \\times Q)$$
        """)
        
        st.divider()
        
        st.markdown("**📥 Input Parameters:**")
        
        col_pm1, col_pm2 = st.columns(2)
        
        with col_pm1:
            market_price = st.number_input("Market Price (Rp/unit):", value=15000.0, step=100.0, format="%.0f")
            fixed_cost_pm = st.number_input("Fixed Cost (Rp):", value=5000000.0, step=100000.0, format="%.0f")
        
        with col_pm2:
            var_cost_pm = st.number_input("Variable Cost per Unit (Rp):", value=8000.0, step=100.0, format="%.0f")
            max_capacity = st.number_input("Maximum Capacity (units):", value=5000.0, step=100.0, format="%.0f")
        
        if st.button("📊 Calculate Optimal Profit", type="primary"):
            if market_price <= var_cost_pm:
                st.error("⚠️ Market price must be greater than variable cost! Otherwise, don't produce.")
            else:
                # For linear cost function, optimal is at maximum capacity (if P > VC)
                # Because contribution margin is constant
                
                contribution_margin_pm = market_price - var_cost_pm
                
                # Calculate profit at different quantities
                quantities = np.linspace(0, max_capacity, 100)
                revenues = market_price * quantities
                total_costs = fixed_cost_pm + (var_cost_pm * quantities)
                profits = revenues - total_costs
                
                # Optimal quantity (at max capacity for linear case)
                optimal_qty = max_capacity
                optimal_revenue = market_price * optimal_qty
                optimal_cost = fixed_cost_pm + (var_cost_pm * optimal_qty)
                optimal_profit = optimal_revenue - optimal_cost
                
                # Display Results
                st.divider()
                st.subheader("📊 Profit Maximization Results")
                
                col_opt1, col_opt2, col_opt3, col_opt4 = st.columns(4)
                
                with col_opt1:
                    st.metric("Optimal Quantity", f"{optimal_qty:,.0f} units")
                
                with col_opt2:
                    st.metric("Total Revenue", f"Rp {optimal_revenue:,.0f}")
                
                with col_opt3:
                    st.metric("Total Cost", f"Rp {optimal_cost:,.0f}")
                
                with col_opt4:
                    st.metric("Maximum Profit", f"Rp {optimal_profit:,.0f}", 
                             delta="optimal" if optimal_profit > 0 else "loss")
                
                # Additional metrics
                st.markdown("### 📊 Profitability Metrics")
                
                col_met1, col_met2, col_met3 = st.columns(3)
                
                with col_met1:
                    profit_margin = (optimal_profit / optimal_revenue * 100) if optimal_revenue > 0 else 0
                    st.metric("Profit Margin", f"{profit_margin:.1f}%")
                
                with col_met2:
                    roi = (optimal_profit / optimal_cost * 100) if optimal_cost > 0 else 0
                    st.metric("ROI", f"{roi:.1f}%")
                
                with col_met3:
                    st.metric("Contribution Margin", f"Rp {contribution_margin_pm:,.0f}")
                
                # Visualization
                st.markdown("### 📈 Profit Curve")
                
                fig_profit = go.Figure()
                
                # Revenue line
                fig_profit.add_trace(go.Scatter(
                    x=quantities,
                    y=revenues,
                    mode='lines',
                    name='Total Revenue',
                    line=dict(color='green', width=2)
                ))
                
                # Cost line
                fig_profit.add_trace(go.Scatter(
                    x=quantities,
                    y=total_costs,
                    mode='lines',
                    name='Total Cost',
                    line=dict(color='red', width=2)
                ))
                
                # Profit line
                fig_profit.add_trace(go.Scatter(
                    x=quantities,
                    y=profits,
                    mode='lines',
                    name='Profit',
                    line=dict(color='blue', width=3, dash='dash')
                ))
                
                # Optimal point
                fig_profit.add_trace(go.Scatter(
                    x=[optimal_qty],
                    y=[optimal_profit],
                    mode='markers',
                    name='Maximum Profit',
                    marker=dict(size=15, color='gold', symbol='star')
                ))
                
                fig_profit.update_layout(
                    title='Revenue, Cost, and Profit Analysis',
                    xaxis_title='Quantity (units)',
                    yaxis_title='Rupiah',
                    height=500,
                    hovermode='x unified'
                )
                
                st.plotly_chart(fig_profit, use_container_width=True)
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                
                if optimal_profit > 0:
                    st.success(f"""
                    **✅ Profitable Operation**
                    
                    - Produksi pada kapasitas maksimum ({optimal_qty:,.0f} units)
                    - Expected profit: Rp {optimal_profit:,.0f}
                    - Profit margin: {profit_margin:.1f}%
                    
                    **Strategy:**
                    - Maintain atau tingkatkan kapasitas produksi
                    - Focus on quality control
                    - Explore market expansion
                    """)
                else:
                    st.error(f"""
                    **❌ Unprofitable Operation**
                    
                    - Current price (Rp {market_price:,.0f}) terlalu rendah
                    - Atau cost terlalu tinggi
                    
                    **Options:**
                    1. Negotiate higher selling price
                    2. Reduce variable costs
                    3. Consider not producing
                    """)
    
    # ===== COST FUNCTION ANALYSIS =====
    else:
        st.divider()
        st.subheader("📈 Cost Function Analysis")
        
        st.markdown("""
        ### Analisis Fungsi Biaya
        
        **Cost Functions:**
        
        - **Total Cost (TC)** = FC + VC
        - **Average Cost (AC)** = TC / Q
        - **Marginal Cost (MC)** = ΔTC / ΔQ
        
        **Economies of Scale:**
        - AC menurun → Economies of scale
        - AC konstan → Constant returns
        - AC naik → Diseconomies of scale
        """)
        
        st.info("🚧 Upload your cost data (CSV with columns: Quantity, Total_Cost) untuk analisis mendalam!")
        
        cost_file = st.file_uploader("Upload Cost Data CSV:", type='csv', key='cost_upload')
        
        if cost_file:
            df_cost = pd.read_csv(cost_file)
            st.write("**Data Preview:**")
            st.dataframe(df_cost.head(), use_container_width=True)
            
            if 'Quantity' in df_cost.columns and 'Total_Cost' in df_cost.columns:
                # Calculate AC and MC
                df_cost = df_cost.sort_values('Quantity')
                df_cost['Average_Cost'] = df_cost['Total_Cost'] / df_cost['Quantity']
                df_cost['Marginal_Cost'] = df_cost['Total_Cost'].diff() / df_cost['Quantity'].diff()
                
                st.markdown("### 📊 Cost Analysis Results")
                st.dataframe(df_cost, use_container_width=True)
                
                # Visualization
                fig_cost = go.Figure()
                
                fig_cost.add_trace(go.Scatter(
                    x=df_cost['Quantity'],
                    y=df_cost['Total_Cost'],
                    mode='lines+markers',
                    name='Total Cost'
                ))
                
                fig_cost.add_trace(go.Scatter(
                    x=df_cost['Quantity'],
                    y=df_cost['Average_Cost'],
                    mode='lines+markers',
                    name='Average Cost'
                ))
                
                fig_cost.add_trace(go.Scatter(
                    x=df_cost['Quantity'],
                    y=df_cost['Marginal_Cost'],
                    mode='lines+markers',
                    name='Marginal Cost'
                ))
                
                fig_cost.update_layout(
                    title='Cost Function Analysis',
                    xaxis_title='Quantity',
                    yaxis_title='Cost (Rp)',
                    height=500
                )
                
                st.plotly_chart(fig_cost, use_container_width=True)
            else:
                st.error("⚠️ CSV must have 'Quantity' and 'Total_Cost' columns!")


# ==========================================
# TAB 4: OPTIMAL INPUT CALCULATOR
# ==========================================
with tab_optimal:
    st.header("🎯 Optimal Input Calculator")
    
    st.markdown("""
    ### Optimasi Alokasi Input Produksi
    
    Tool ini membantu menentukan kombinasi input optimal untuk:
    1. **Maximize Output** dengan budget constraint
    2. **Minimize Cost** untuk target output tertentu
    """)
    
    opt_mode = st.radio(
        "Pilih Mode Optimasi:",
        ["📈 Maximize Output (Budget Constraint)", "💰 Minimize Cost (Target Output)"],
        horizontal=True
    )
    
    # ===== MAXIMIZE OUTPUT =====
    if opt_mode == "📈 Maximize Output (Budget Constraint)":
        st.divider()
        st.subheader("📈 Maximize Output with Budget Constraint")
        
        st.markdown("""
        ### Problem Formulation
        
        **Objective:** Maximize output Y
        
        **Subject to:** Budget constraint
        
        $$P_K \\times K + P_L \\times L \\leq Budget$$
        
        **Given:** Production function (Cobb-Douglas)
        
        $$Y = A \\times K^{\\alpha} \\times L^{\\beta}$$
        
        **Solution:** Equi-marginal principle
        
        $$\\frac{MP_K}{P_K} = \\frac{MP_L}{P_L}$$
        """)
        
        st.divider()
        
        col_max1, col_max2 = st.columns(2)
        
        with col_max1:
            st.markdown("**📥 Production Function Parameters:**")
            A_max = st.number_input("TFP (A):", value=2.0, step=0.1, format="%.2f", key='a_max')
            alpha_max = st.number_input("Capital Elasticity (α):", value=0.5, step=0.05, format="%.2f", key='alpha_max')
            beta_max = st.number_input("Labor Elasticity (β):", value=0.3, step=0.05, format="%.2f", key='beta_max')
        
        with col_max2:
            st.markdown("**💰 Budget & Prices:**")
            budget = st.number_input("Total Budget (Rp):", value=50000000.0, step=1000000.0, format="%.0f")
            price_K = st.number_input("Price of Capital (Rp/unit):", value=10000.0, step=100.0, format="%.0f")
            price_L = st.number_input("Price of Labor (Rp/unit):", value=5000.0, step=100.0, format="%.0f")
        
        if st.button("🎯 Find Optimal Allocation", type="primary"):
            # Optimal allocation using Lagrangian
            # For Cobb-Douglas: K* = (α/(α+β)) × (Budget/P_K)
            #                   L* = (β/(α+β)) × (Budget/P_L)
            
            total_elasticity = alpha_max + beta_max
            
            optimal_K = (alpha_max / total_elasticity) * (budget / price_K)
            optimal_L = (beta_max / total_elasticity) * (budget / price_L)
            
            # Calculate optimal output
            optimal_Y = A_max * (optimal_K ** alpha_max) * (optimal_L ** beta_max)
            
            # Cost check
            total_cost = (price_K * optimal_K) + (price_L * optimal_L)
            
            # Marginal products
            MP_K = alpha_max * (optimal_Y / optimal_K) if optimal_K > 0 else 0
            MP_L = beta_max * (optimal_Y / optimal_L) if optimal_L > 0 else 0
            
            # Marginal product per rupiah
            MPR_K = MP_K / price_K if price_K > 0 else 0
            MPR_L = MP_L / price_L if price_L > 0 else 0
            
            # Display Results
            st.divider()
            st.subheader("📊 Optimal Allocation Results")
            
            col_opt1, col_opt2, col_opt3 = st.columns(3)
            
            with col_opt1:
                st.metric("Optimal Capital (K)", f"{optimal_K:,.2f} units")
                st.caption(f"Cost: Rp {price_K * optimal_K:,.0f}")
            
            with col_opt2:
                st.metric("Optimal Labor (L)", f"{optimal_L:,.2f} units")
                st.caption(f"Cost: Rp {price_L * optimal_L:,.0f}")
            
            with col_opt3:
                st.metric("Maximum Output (Y)", f"{optimal_Y:,.2f} units")
                st.caption(f"Total Cost: Rp {total_cost:,.0f}")
            
            # Marginal Analysis
            st.markdown("### 📊 Marginal Analysis")
            
            col_mp1, col_mp2 = st.columns(2)
            
            with col_mp1:
                st.markdown("**Capital:**")
                st.metric("Marginal Product (MP_K)", f"{MP_K:.4f}")
                st.metric("MP per Rupiah", f"{MPR_K:.6f}")
            
            with col_mp2:
                st.markdown("**Labor:**")
                st.metric("Marginal Product (MP_L)", f"{MP_L:.4f}")
                st.metric("MP per Rupiah", f"{MPR_L:.6f}")
            
            # Check optimality
            if abs(MPR_K - MPR_L) < 0.0001:
                st.success("""
                ✅ **Optimal Allocation Achieved!**
                
                MP/Price ratio sama untuk semua input → Equi-marginal principle terpenuhi
                """)
            else:
                st.info(f"""
                **Equi-marginal Check:**
                - MP_K/P_K = {MPR_K:.6f}
                - MP_L/P_L = {MPR_L:.6f}
                - Difference: {abs(MPR_K - MPR_L):.6f}
                """)
            
            # Visualization - Isoquant and Budget Line
            st.markdown("### 📈 Isoquant & Budget Line")
            
            # Budget line: K = (Budget - P_L×L) / P_K
            L_range = np.linspace(0, budget/price_L, 100)
            K_budget = (budget - price_L * L_range) / price_K
            
            # Isoquant: K = (Y/A)^(1/α) × L^(-β/α)
            L_iso = np.linspace(optimal_L * 0.5, optimal_L * 1.5, 100)
            K_iso = ((optimal_Y / A_max) ** (1/alpha_max)) * (L_iso ** (-beta_max/alpha_max))
            
            fig_iso = go.Figure()
            
            # Budget line
            fig_iso.add_trace(go.Scatter(
                x=L_range,
                y=K_budget,
                mode='lines',
                name='Budget Constraint',
                line=dict(color='red', width=2)
            ))
            
            # Isoquant
            fig_iso.add_trace(go.Scatter(
                x=L_iso,
                y=K_iso,
                mode='lines',
                name=f'Isoquant (Y={optimal_Y:.0f})',
                line=dict(color='blue', width=2)
            ))
            
            # Optimal point
            fig_iso.add_trace(go.Scatter(
                x=[optimal_L],
                y=[optimal_K],
                mode='markers',
                name='Optimal Point',
                marker=dict(size=15, color='gold', symbol='star')
            ))
            
            fig_iso.update_layout(
                title='Isoquant-Isocost Analysis',
                xaxis_title='Labor (L)',
                yaxis_title='Capital (K)',
                height=500
            )
            
            st.plotly_chart(fig_iso, use_container_width=True)
            
            # Recommendations
            st.markdown("### 💡 Recommendations")
            
            st.success(f"""
            **Optimal Input Mix:**
            
            1. **Capital (K):** {optimal_K:,.2f} units @ Rp {price_K:,.0f}/unit
               - Total: Rp {price_K * optimal_K:,.0f}
               - Share: {(price_K * optimal_K / budget * 100):.1f}% of budget
            
            2. **Labor (L):** {optimal_L:,.2f} units @ Rp {price_L:,.0f}/unit
               - Total: Rp {price_L * optimal_L:,.0f}
               - Share: {(price_L * optimal_L / budget * 100):.1f}% of budget
            
            3. **Expected Output:** {optimal_Y:,.2f} units
            
            **Key Insights:**
            - Alokasi ini memaksimalkan output dengan budget yang tersedia
            - Ratio MP/Price sama untuk semua input (efficient allocation)
            - Returns to Scale: {total_elasticity:.2f} {"(IRS)" if total_elasticity > 1 else "(CRS)" if abs(total_elasticity-1) < 0.05 else "(DRS)"}
            """)
    
    # ===== MINIMIZE COST =====
    else:
        st.divider()
        st.subheader("💰 Minimize Cost for Target Output")
        
        st.markdown("""
        ### Problem Formulation
        
        **Objective:** Minimize total cost
        
        $$Min: C = P_K \\times K + P_L \\times L$$
        
        **Subject to:** Output constraint
        
        $$Y_{target} = A \\times K^{\\alpha} \\times L^{\\beta}$$
        
        **Solution:** Same equi-marginal principle
        
        $$\\frac{MP_K}{P_K} = \\frac{MP_L}{P_L}$$
        """)
        
        st.divider()
        
        col_min1, col_min2 = st.columns(2)
        
        with col_min1:
            st.markdown("**📥 Production Function Parameters:**")
            A_min = st.number_input("TFP (A):", value=2.0, step=0.1, format="%.2f", key='a_min')
            alpha_min = st.number_input("Capital Elasticity (α):", value=0.5, step=0.05, format="%.2f", key='alpha_min')
            beta_min = st.number_input("Labor Elasticity (β):", value=0.3, step=0.05, format="%.2f", key='beta_min')
        
        with col_min2:
            st.markdown("**🎯 Target & Prices:**")
            target_output = st.number_input("Target Output (Y):", value=1000.0, step=10.0, format="%.0f")
            price_K_min = st.number_input("Price of Capital (Rp/unit):", value=10000.0, step=100.0, format="%.0f", key='pk_min')
            price_L_min = st.number_input("Price of Labor (Rp/unit):", value=5000.0, step=100.0, format="%.0f", key='pl_min')
        
        if st.button("💰 Find Cost-Minimizing Allocation", type="primary"):
            # For Cobb-Douglas with cost minimization:
            # K/L = (α/β) × (P_L/P_K)
            # Substitute into production function to solve
            
            # Optimal ratio
            kl_ratio = (alpha_min / beta_min) * (price_L_min / price_K_min)
            
            # Solve for L: Y = A × (kl_ratio × L)^α × L^β
            #              Y = A × (kl_ratio)^α × L^(α+β)
            #              L = (Y / (A × kl_ratio^α))^(1/(α+β))
            
            total_elast = alpha_min + beta_min
            optimal_L_min = (target_output / (A_min * (kl_ratio ** alpha_min))) ** (1 / total_elast)
            optimal_K_min = kl_ratio * optimal_L_min
            
            # Verify output
            actual_output = A_min * (optimal_K_min ** alpha_min) * (optimal_L_min ** beta_min)
            
            # Calculate minimum cost
            min_cost = (price_K_min * optimal_K_min) + (price_L_min * optimal_L_min)
            
            # Marginal products
            MP_K_min = alpha_min * (actual_output / optimal_K_min) if optimal_K_min > 0 else 0
            MP_L_min = beta_min * (actual_output / optimal_L_min) if optimal_L_min > 0 else 0
            
            # Display Results
            st.divider()
            st.subheader("📊 Cost-Minimizing Allocation Results")
            
            col_res1, col_res2, col_res3 = st.columns(3)
            
            with col_res1:
                st.metric("Optimal Capital (K)", f"{optimal_K_min:,.2f} units")
                st.caption(f"Cost: Rp {price_K_min * optimal_K_min:,.0f}")
            
            with col_res2:
                st.metric("Optimal Labor (L)", f"{optimal_L_min:,.2f} units")
                st.caption(f"Cost: Rp {price_L_min * optimal_L_min:,.0f}")
            
            with col_res3:
                st.metric("Minimum Total Cost", f"Rp {min_cost:,.0f}")
                st.caption(f"Output: {actual_output:,.2f}")
            
            # Cost breakdown
            st.markdown("### 💰 Cost Breakdown")
            
            cost_data = pd.DataFrame({
                'Input': ['Capital (K)', 'Labor (L)', 'Total'],
                'Quantity': [optimal_K_min, optimal_L_min, '-'],
                'Price': [f"Rp {price_K_min:,.0f}", f"Rp {price_L_min:,.0f}", '-'],
                'Total Cost': [
                    f"Rp {price_K_min * optimal_K_min:,.0f}",
                    f"Rp {price_L_min * optimal_L_min:,.0f}",
                    f"Rp {min_cost:,.0f}"
                ],
                'Share (%)': [
                    f"{(price_K_min * optimal_K_min / min_cost * 100):.1f}%",
                    f"{(price_L_min * optimal_L_min / min_cost * 100):.1f}%",
                    "100.0%"
                ]
            })
            
            st.dataframe(cost_data, use_container_width=True)
            
            # Visualization - Cost breakdown pie chart
            st.markdown("### 📊 Cost Allocation")
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Capital', 'Labor'],
                values=[price_K_min * optimal_K_min, price_L_min * optimal_L_min],
                hole=.3
            )])
            
            fig_pie.update_layout(
                title='Cost Distribution',
                height=400
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Recommendations
            st.markdown("### 💡 Recommendations")
            
            st.success(f"""
            **Cost-Minimizing Strategy:**
            
            1. **Untuk mencapai output {target_output:,.0f} units:**
               - Gunakan {optimal_K_min:,.2f} units Capital
               - Gunakan {optimal_L_min:,.2f} units Labor
            
            2. **Minimum Cost:** Rp {min_cost:,.0f}
               - Capital cost: Rp {price_K_min * optimal_K_min:,.0f} ({(price_K_min * optimal_K_min / min_cost * 100):.1f}%)
               - Labor cost: Rp {price_L_min * optimal_L_min:,.0f} ({(price_L_min * optimal_L_min / min_cost * 100):.1f}%)
            
            3. **Cost per Unit Output:** Rp {min_cost / actual_output:,.2f}
            
            **Key Insights:**
            - Ini adalah kombinasi input paling efisien untuk target output
            - Tidak ada cara lain yang lebih murah untuk mencapai output ini
            - K/L ratio optimal: {kl_ratio:.4f}
            """)
