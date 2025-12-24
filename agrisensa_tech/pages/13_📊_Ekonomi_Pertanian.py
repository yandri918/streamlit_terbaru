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
    st.info("🚧 Under Development - Coming in next update!")
    
    st.markdown("""
    ### Planned Features:
    
    - **Cost Function Estimation**
      - Total Cost (TC), Average Cost (AC), Marginal Cost (MC)
      - Short-run vs Long-run cost curves
      - Economies of scale analysis
    
    - **Profit Maximization**
      - Revenue function
      - Break-even analysis
      - Optimal pricing
    
    - **Cost-Benefit Analysis**
      - NPV, IRR, Payback period
      - Sensitivity analysis
      - Risk assessment
    """)

# ==========================================
# TAB 4: OPTIMAL INPUT CALCULATOR
# ==========================================
with tab_optimal:
    st.header("🎯 Optimal Input Calculator")
    st.info("🚧 Under Development - Coming in next update!")
    
    st.markdown("""
    ### Planned Features:
    
    - **Optimal Input Allocation**
      - Given budget constraint
      - Given target output
      - Minimize cost for target output
    
    - **Marginal Analysis**
      - Equi-marginal principle
      - Marginal value product
      - Input substitution
    
    - **Scenario Analysis**
      - What-if analysis
      - Sensitivity to price changes
      - Risk-adjusted optimization
    """)
