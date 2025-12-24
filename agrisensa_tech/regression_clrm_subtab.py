# ===== NEW SUB-TAB: CLRM ASSUMPTIONS & GAUSS-MARKOV =====
# Insert this as the FIRST sub-tab in tab_regression (before subtab_simple)

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
    
    **Matematically:**
    
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
            else:
                st.info("Select at least 2 variables for VIF calculation")
        else:
            st.warning("Need at least 2 numeric variables for VIF calculation")
