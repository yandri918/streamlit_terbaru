import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
import math

st.set_page_config(page_title="Survey Sampling & Election Polling", page_icon="🗳️", layout="wide")

# Header
st.title("🗳️ Survey Sampling & Election Polling Calculator")
st.markdown("""
**Professional survey sampling tools** untuk menghitung ukuran sampel, margin of error, dan confidence intervals.
Cocok untuk polling pemilu, survei opini publik, dan riset pasar.
""")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Sample Size Calculator",
    "📈 Survey Results Analysis",
    "🎯 Margin of Error",
    "📚 Education & Guide"
])

# ========== TAB 1: SAMPLE SIZE CALCULATOR ==========
with tab1:
    st.header("📊 Sample Size Calculator")
    st.markdown("Hitung berapa banyak responden yang dibutuhkan untuk survei Anda.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Input Parameters")
        
        # Population size
        population = st.number_input(
            "Ukuran Populasi (N)",
            min_value=100,
            max_value=1000000000,
            value=200000000,  # Indonesia population
            step=1000,
            help="Total jumlah populasi yang ingin di-survey (misal: pemilih Indonesia ~200 juta)"
        )
        
        # Confidence level
        confidence_level = st.select_slider(
            "Confidence Level",
            options=[80, 85, 90, 95, 99],
            value=95,
            help="Tingkat kepercayaan. 95% adalah standar industri."
        )
        
        # Margin of error
        margin_of_error = st.slider(
            "Margin of Error (%)",
            min_value=1.0,
            max_value=10.0,
            value=3.0,
            step=0.5,
            help="Tingkat kesalahan yang dapat diterima. Semakin kecil, semakin banyak sampel yang dibutuhkan."
        )
        
        # Expected proportion (for worst case, use 0.5)
        proportion = st.slider(
            "Expected Proportion (p)",
            min_value=0.1,
            max_value=0.9,
            value=0.5,
            step=0.05,
            help="Proporsi yang diharapkan. 0.5 memberikan sampel maksimum (worst case scenario)."
        )
        
        # Calculate button
        if st.button("🔢 Calculate Sample Size", type="primary"):
            st.session_state['calculate_sample'] = True
    
    with col2:
        if st.session_state.get('calculate_sample', False):
            st.markdown("### Results")
            
            # Z-score for confidence level
            z_scores = {80: 1.28, 85: 1.44, 90: 1.645, 95: 1.96, 99: 2.576}
            z = z_scores[confidence_level]
            
            # Margin of error as decimal
            e = margin_of_error / 100
            
            # Sample size formula (infinite population)
            n_infinite = (z**2 * proportion * (1 - proportion)) / (e**2)
            
            # Sample size formula (finite population correction)
            n_finite = n_infinite / (1 + ((n_infinite - 1) / population))
            
            # Round up
            n_required = math.ceil(n_finite)
            
            # Display results
            st.success(f"### Sampel yang Dibutuhkan: **{n_required:,}** responden")
            
            st.info(f"""
            **Interpretasi:**
            - Dengan **{n_required:,}** responden
            - Confidence level: **{confidence_level}%**
            - Margin of error: **±{margin_of_error}%**
            
            Artinya: Jika survei menunjukkan kandidat A mendapat 45%, maka dengan 95% confidence, 
            dukungan sebenarnya ada di antara **{45-margin_of_error:.1f}% - {45+margin_of_error:.1f}%**
            """)
            
            # Comparison table
            st.markdown("### Comparison: Different Margin of Errors")
            
            comparison_data = []
            for moe in [1, 2, 3, 4, 5]:
                e_comp = moe / 100
                n_inf = (z**2 * proportion * (1 - proportion)) / (e_comp**2)
                n_fin = n_inf / (1 + ((n_inf - 1) / population))
                comparison_data.append({
                    'Margin of Error': f"±{moe}%",
                    'Sample Size': f"{math.ceil(n_fin):,}",
                    'Cost Factor': f"{math.ceil(n_fin) / n_required:.1f}x"
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)
            
            st.caption("💡 **Tip:** Margin of error yang lebih kecil membutuhkan sampel yang jauh lebih besar (dan biaya lebih tinggi).")

# ========== TAB 2: SURVEY RESULTS ANALYSIS ==========
with tab2:
    st.header("📈 Survey Results Analysis")
    st.markdown("Analisis hasil survei dengan confidence intervals dan statistical significance.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Survey Data")
        
        # Sample size
        sample_size = st.number_input(
            "Jumlah Responden (n)",
            min_value=100,
            max_value=100000,
            value=1200,
            step=100,
            help="Total responden yang berhasil di-survey"
        )
        
        # Confidence level
        conf_level = st.select_slider(
            "Confidence Level",
            options=[90, 95, 99],
            value=95,
            key="conf_level_tab2"
        )
        
        # Number of candidates/options
        num_candidates = st.number_input(
            "Jumlah Kandidat/Pilihan",
            min_value=2,
            max_value=10,
            value=3,
            step=1
        )
        
        st.markdown("### Input Survey Results (%)")
        
        # Input for each candidate
        results = []
        total_pct = 0
        
        for i in range(num_candidates):
            pct = st.number_input(
                f"Kandidat {chr(65+i)} (%)",
                min_value=0.0,
                max_value=100.0,
                value=30.0 if i == 0 else (25.0 if i == 1 else 20.0),
                step=0.1,
                key=f"cand_{i}"
            )
            results.append({'Candidate': chr(65+i), 'Percentage': pct})
            total_pct += pct
        
        # Undecided
        undecided = 100 - total_pct
        results.append({'Candidate': 'Undecided', 'Percentage': undecided})
        
        if abs(total_pct - 100) > 0.1 and total_pct > 100:
            st.warning(f"⚠️ Total percentage: {total_pct:.1f}% (should be ≤100%)")
        
        if st.button("📊 Analyze Results", type="primary"):
            st.session_state['analyze_results'] = True
            st.session_state['survey_data'] = results
            st.session_state['sample_size'] = sample_size
            st.session_state['conf_level'] = conf_level
    
    with col2:
        if st.session_state.get('analyze_results', False):
            st.markdown("### Analysis Results")
            
            results_df = pd.DataFrame(st.session_state['survey_data'])
            sample_size = st.session_state['sample_size']
            conf_level = st.session_state['conf_level']
            
            # Calculate confidence intervals
            z_scores = {90: 1.645, 95: 1.96, 99: 2.576}
            z = z_scores[conf_level]
            
            ci_data = []
            for idx, row in results_df.iterrows():
                p = row['Percentage'] / 100
                
                # Standard error
                se = math.sqrt((p * (1 - p)) / sample_size)
                
                # Margin of error
                moe = z * se * 100
                
                # Confidence interval
                ci_lower = max(0, p * 100 - moe)
                ci_upper = min(100, p * 100 + moe)
                
                ci_data.append({
                    'Candidate': row['Candidate'],
                    'Survey %': f"{row['Percentage']:.1f}%",
                    'Margin of Error': f"±{moe:.1f}%",
                    f'{conf_level}% CI': f"[{ci_lower:.1f}%, {ci_upper:.1f}%]",
                    'CI_Lower': ci_lower,
                    'CI_Upper': ci_upper,
                    'Percentage': row['Percentage']
                })
            
            ci_df = pd.DataFrame(ci_data)
            
            # Display table
            st.dataframe(ci_df[['Candidate', 'Survey %', 'Margin of Error', f'{conf_level}% CI']], 
                        use_container_width=True, hide_index=True)
            
            # Visualization
            st.markdown("### Confidence Interval Visualization")
            
            fig = go.Figure()
            
            # Filter out undecided for cleaner viz
            viz_df = ci_df[ci_df['Candidate'] != 'Undecided'].copy()
            
            # Sort by percentage
            viz_df = viz_df.sort_values('Percentage', ascending=True)
            
            # Error bars
            for idx, row in viz_df.iterrows():
                fig.add_trace(go.Scatter(
                    x=[row['CI_Lower'], row['Percentage'], row['CI_Upper']],
                    y=[row['Candidate']] * 3,
                    mode='lines+markers',
                    name=row['Candidate'],
                    line=dict(width=3),
                    marker=dict(size=[8, 12, 8]),
                    error_x=None
                ))
            
            fig.update_layout(
                title=f"Survey Results with {conf_level}% Confidence Intervals",
                xaxis_title="Percentage (%)",
                yaxis_title="Candidate",
                height=400,
                showlegend=False,
                hovermode='y unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistical significance test
            st.markdown("### Statistical Significance")
            
            # Check if top 2 candidates are statistically different
            top_2 = ci_df.nlargest(2, 'Percentage')
            
            if len(top_2) >= 2:
                cand1 = top_2.iloc[0]
                cand2 = top_2.iloc[1]
                
                # Check if CIs overlap
                overlap = not (cand1['CI_Lower'] > cand2['CI_Upper'] or cand2['CI_Lower'] > cand1['CI_Upper'])
                
                if overlap:
                    st.warning(f"""
                    ⚠️ **Tidak Ada Perbedaan Signifikan**
                    
                    Kandidat {cand1['Candidate']} ({cand1['Survey %']}) dan Kandidat {cand2['Candidate']} ({cand2['Survey %']}) 
                    memiliki confidence intervals yang **overlap**.
                    
                    Artinya: Perbedaan mereka **tidak signifikan secara statistik**. 
                    Kedua kandidat bisa saja memiliki dukungan yang sama di populasi sebenarnya.
                    """)
                else:
                    st.success(f"""
                    ✅ **Perbedaan Signifikan**
                    
                    Kandidat {cand1['Candidate']} ({cand1['Survey %']}) **secara statistik lebih unggul** 
                    dari Kandidat {cand2['Candidate']} ({cand2['Survey %']}).
                    
                    Confidence intervals mereka tidak overlap, menunjukkan perbedaan yang signifikan.
                    """)

# ========== TAB 3: MARGIN OF ERROR ==========
with tab3:
    st.header("🎯 Margin of Error Calculator")
    st.markdown("Hitung margin of error untuk survei yang sudah dilakukan.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Input")
        
        n_moe = st.number_input(
            "Sample Size (n)",
            min_value=100,
            max_value=100000,
            value=1000,
            step=100,
            key="n_moe"
        )
        
        conf_moe = st.select_slider(
            "Confidence Level",
            options=[90, 95, 99],
            value=95,
            key="conf_moe"
        )
        
        p_moe = st.slider(
            "Survey Result (%)",
            min_value=1.0,
            max_value=99.0,
            value=50.0,
            step=1.0,
            key="p_moe",
            help="Hasil survei untuk kandidat/pilihan tertentu. 50% memberikan MoE maksimum."
        )
        
        if st.button("Calculate MoE", type="primary"):
            st.session_state['calc_moe'] = True
    
    with col2:
        if st.session_state.get('calc_moe', False):
            st.markdown("### Results")
            
            # Calculate
            z_scores = {90: 1.645, 95: 1.96, 99: 2.576}
            z = z_scores[conf_moe]
            
            p = p_moe / 100
            se = math.sqrt((p * (1 - p)) / n_moe)
            moe = z * se * 100
            
            st.success(f"### Margin of Error: **±{moe:.2f}%**")
            
            st.info(f"""
            **Interpretasi:**
            - Hasil survei: **{p_moe:.1f}%**
            - Margin of error: **±{moe:.2f}%**
            - Confidence level: **{conf_moe}%**
            
            **Range sebenarnya:** {p_moe - moe:.1f}% - {p_moe + moe:.1f}%
            
            Dengan {conf_moe}% confidence, dukungan sebenarnya di populasi berada dalam range ini.
            """)
            
            # Visualization
            st.markdown("### MoE vs Sample Size")
            
            sample_sizes = np.arange(100, 5000, 100)
            moes = []
            
            for n in sample_sizes:
                se_temp = math.sqrt((p * (1 - p)) / n)
                moe_temp = z * se_temp * 100
                moes.append(moe_temp)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=sample_sizes,
                y=moes,
                mode='lines',
                name='Margin of Error',
                line=dict(color='blue', width=3)
            ))
            
            # Current point
            fig.add_trace(go.Scatter(
                x=[n_moe],
                y=[moe],
                mode='markers',
                name='Your Survey',
                marker=dict(size=15, color='red')
            ))
            
            fig.update_layout(
                title="How Sample Size Affects Margin of Error",
                xaxis_title="Sample Size (n)",
                yaxis_title="Margin of Error (%)",
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.caption("💡 **Insight:** Margin of error turun drastis saat sampel kecil, tapi improvement melambat setelah n>1000.")

# ========== TAB 4: EDUCATION & GUIDE ==========
with tab4:
    st.header("📚 Survey Sampling Guide")
    
    with st.expander("📖 **Apa itu Sample Size?**", expanded=True):
        st.markdown("""
        **Sample Size** adalah jumlah responden yang dibutuhkan untuk merepresentasikan populasi.
        
        **Mengapa penting?**
        - Sampel terlalu kecil → Hasil tidak akurat
        - Sampel terlalu besar → Buang biaya dan waktu
        
        **Formula:**
        ```
        n = (Z² × p × (1-p)) / E²
        
        Dimana:
        - Z = Z-score (1.96 untuk 95% confidence)
        - p = Expected proportion (0.5 untuk worst case)
        - E = Margin of error (misal: 0.03 untuk 3%)
        ```
        
        **Finite Population Correction:**
        Jika populasi terbatas (misal: 1000 orang), gunakan:
        ```
        n_adjusted = n / (1 + (n-1)/N)
        ```
        """)
    
    with st.expander("🎯 **Apa itu Margin of Error?**"):
        st.markdown("""
        **Margin of Error (MoE)** adalah range kesalahan yang mungkin terjadi dalam survei.
        
        **Contoh:**
        - Survei: Kandidat A = 45%
        - MoE: ±3%
        - **Artinya:** Dukungan sebenarnya antara 42% - 48%
        
        **Faktor yang mempengaruhi MoE:**
        1. **Sample size:** Semakin besar, MoE semakin kecil
        2. **Confidence level:** 99% confidence → MoE lebih besar
        3. **Variance:** Proporsi 50-50 → MoE maksimum
        
        **Rule of Thumb:**
        - MoE ±3%: Standar untuk polling nasional
        - MoE ±5%: Acceptable untuk survei regional
        - MoE ±10%: Terlalu besar, kurang reliable
        """)
    
    with st.expander("📊 **Confidence Level vs Confidence Interval**"):
        st.markdown("""
        ### Confidence Level
        **Tingkat kepercayaan** bahwa hasil survei mencerminkan populasi sebenarnya.
        
        - **90%:** 9 dari 10 survei akan akurat
        - **95%:** 19 dari 20 survei akan akurat (standar industri)
        - **99%:** 99 dari 100 survei akan akurat
        
        ### Confidence Interval
        **Range nilai** dimana parameter populasi sebenarnya berada.
        
        **Contoh:**
        - Survei: 45% ± 3% (95% CI)
        - **Artinya:** Kita 95% yakin dukungan sebenarnya antara 42%-48%
        
        ### Trade-off
        - Confidence level lebih tinggi → CI lebih lebar → Kurang presisi
        - Confidence level lebih rendah → CI lebih sempit → Lebih presisi tapi kurang yakin
        """)
    
    with st.expander("🔍 **Statistical Significance**"):
        st.markdown("""
        **Kapan perbedaan survei signifikan?**
        
        Dua kandidat **berbeda signifikan** jika confidence intervals mereka **tidak overlap**.
        
        ### Contoh 1: Tidak Signifikan
        ```
        Kandidat A: 45% [42% - 48%]
        Kandidat B: 43% [40% - 46%]
        
        → CIs overlap (42-46%)
        → Perbedaan TIDAK signifikan
        → Bisa saja tie di populasi sebenarnya
        ```
        
        ### Contoh 2: Signifikan
        ```
        Kandidat A: 50% [47% - 53%]
        Kandidat B: 40% [37% - 43%]
        
        → CIs tidak overlap
        → Perbedaan SIGNIFIKAN
        → A lebih unggul secara statistik
        ```
        
        ### Implikasi
        - Jika **tidak signifikan:** Terlalu dini menyebut pemenang
        - Jika **signifikan:** Bisa confident kandidat unggul
        """)
    
    with st.expander("💡 **Best Practices untuk Polling Pemilu**"):
        st.markdown("""
        ### 1. Sample Size
        - **Nasional:** Minimum 1,000-1,200 responden
        - **Regional:** Minimum 400-600 responden
        - **Lokal:** Minimum 300-400 responden
        
        ### 2. Sampling Method
        - **Random Sampling:** Setiap orang punya peluang sama
        - **Stratified Sampling:** Proporsi sesuai demografi (umur, gender, wilayah)
        - **Cluster Sampling:** Sampling per wilayah geografis
        
        ### 3. Timing
        - **Jarak dari pemilu:** Survei 1 minggu sebelum > 1 bulan sebelum
        - **Undecided voters:** Perhatikan tren undecided
        - **Multiple waves:** Lakukan beberapa kali untuk lihat tren
        
        ### 4. Reporting
        - **Selalu cantumkan:**
          - Sample size
          - Margin of error
          - Confidence level
          - Tanggal survei
          - Metodologi
        
        ### 5. Red Flags
        - ⚠️ Sample size < 300
        - ⚠️ MoE > 5%
        - ⚠️ Tidak ada metodologi yang jelas
        - ⚠️ Tidak ada informasi tentang non-response rate
        """)
    
    with st.expander("📈 **Real-World Examples**"):
        st.markdown("""
        ### Contoh 1: Polling Pilpres Indonesia 2024
        ```
        Sample Size: 1,200 responden
        Confidence Level: 95%
        Margin of Error: ±2.8%
        
        Hasil:
        - Kandidat A: 52% [49.2% - 54.8%]
        - Kandidat B: 35% [32.2% - 37.8%]
        - Undecided: 13%
        
        Kesimpulan: Kandidat A unggul signifikan
        ```
        
        ### Contoh 2: Quick Count Pemilu
        ```
        Sample Size: 2,000 TPS (dari 800,000 TPS)
        Stratified by province
        
        Hasil Real Count vs Quick Count:
        - Kandidat A: 58.6% vs 58.4% (selisih 0.2%)
        - Kandidat B: 41.4% vs 41.6% (selisih 0.2%)
        
        Akurasi: Sangat tinggi dengan stratified sampling
        ```
        
        ### Contoh 3: Exit Poll
        ```
        Sample Size: 50,000 voters
        Systematic sampling (setiap voter ke-10)
        
        Keuntungan:
        - Real voters (bukan intention)
        - Large sample → MoE sangat kecil
        - Hasil cepat (hari H)
        
        Kelemahan:
        - Mahal
        - Butuh banyak surveyor
        ```
        """)

# Footer
st.divider()

st.markdown("""
### 📚 References & Resources
- **Cochran, W.G.** (1977). *Sampling Techniques*. Wiley.
- **Lohr, S.L.** (2019). *Sampling: Design and Analysis*. CRC Press.
- **Pew Research Center** - [Survey Methodology](https://www.pewresearch.org/methods/)
- **AAPOR** - American Association for Public Opinion Research

### 🛠️ Technical Notes
- All calculations use **normal approximation** (valid for n > 30)
- Finite population correction applied when n/N > 0.05
- Confidence intervals calculated using **Wald method**
- For small samples or extreme proportions, consider **Wilson score interval**
""")

st.caption("🗳️ **Survey Sampling & Election Polling Calculator** | Built with Streamlit & Plotly")
