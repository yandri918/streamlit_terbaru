# Monte Carlo Educational Content
# To be inserted into Page 11

MONTE_CARLO_EDUCATION = """
# ========== TAB 7: EDUKASI MONTE CARLO ==========
with tab_edukasi:
    st.header("📚 Memahami Monte Carlo Simulation")
    st.caption("Panduan Lengkap untuk Memahami Metode Simulasi yang Digunakan dalam Analisis Risiko")
    
    # Section 1: Theory
    with st.expander("📖 **1. Apa itu Monte Carlo Simulation?**", expanded=True):
        st.markdown(\"\"\"
        ### Definisi
        **Monte Carlo Simulation** adalah metode komputasi yang menggunakan **sampling acak berulang** 
        untuk memperoleh hasil numerik dari masalah yang kompleks atau tidak pasti.
        
        ### Sejarah Singkat
        - **Nama**: Diambil dari kasino Monte Carlo di Monaco (karena unsur keacakan/probabilitas)
        - **Penemu**: Stanislaw Ulam & John von Neumann (1940-an) untuk proyek Manhattan
        - **Aplikasi Modern**: Keuangan, fisika, teknik, kedokteran, dan **pertanian**
        
        ### Prinsip Dasar
        Bayangkan Anda ingin tahu rata-rata hasil panen dalam kondisi cuaca yang tidak pasti:
        
        **Pendekatan Tradisional (Deterministik):**
        - Asum cuaca "normal" → Hitung 1 hasil
        - Masalah: Realitas tidak pernah "normal" sempurna
        
        **Pendekatan Monte Carlo (Probabilistik):**
        - Simulasikan 1000 skenario cuaca berbeda (hujan lebat, kering, ideal, dll)
        - Hitung hasil untuk setiap skenario
        - Lihat distribusi: Berapa persen untung? Berapa persen rugi?
        
        ### Kapan Menggunakan Monte Carlo?
        ✅ **Cocok untuk:**
        - Masalah dengan banyak variabel acak (cuaca, harga, hama)
        - Ketika Anda ingin tahu **rentang kemungkinan**, bukan satu angka pasti
        - Analisis risiko & pengambilan keputusan
        
        ❌ **Tidak cocok untuk:**
        - Masalah sederhana yang bisa dihitung langsung
        - Ketika data historis sangat terbatas
        \"\"\")
    
    # Section 2: Interactive Demo
    with st.expander("🎲 **2. Demonstrasi Interaktif: Lempar Dadu**"):
        st.markdown(\"\"\"
        Mari kita lihat Monte Carlo bekerja dengan contoh sederhana: **Melempar 2 dadu**.
        
        **Pertanyaan:** Berapa probabilitas mendapat total 7?
        
        **Cara Analitis (Matematika):**
        - Ada 6 kombinasi yang menghasilkan 7: (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
        - Total kemungkinan: 6 × 6 = 36
        - Probabilitas = 6/36 = **16.67%**
        
        **Cara Monte Carlo (Simulasi):**
        Kita lempar dadu ribuan kali dan hitung berapa kali muncul angka 7.
        \"\"\")
        
        # Interactive Simulator
        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            n_rolls = st.slider("Jumlah Lemparan", 100, 10000, 1000, step=100)
        
        if st.button("🎲 Jalankan Simulasi Dadu"):
            import random
            results = []
            count_seven = 0
            
            for i in range(n_rolls):
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)
                total = dice1 + dice2
                results.append(total)
                if total == 7:
                    count_seven += 1
            
            prob_seven = (count_seven / n_rolls) * 100
            
            with col_sim2:
                st.metric("Probabilitas Total = 7", f"{prob_seven:.2f}%", 
                         f"Error: {abs(prob_seven - 16.67):.2f}%")
            
            # Histogram
            import plotly.express as px
            fig_dice = px.histogram(x=results, nbins=11, 
                                   title=f"Distribusi Hasil {n_rolls} Lemparan Dadu",
                                   labels={'x': 'Total Dadu', 'y': 'Frekuensi'})
            fig_dice.add_vline(x=7, line_dash="dash", line_color="red", 
                              annotation_text="Target: 7")
            st.plotly_chart(fig_dice, use_container_width=True)
            
            st.success(f\"\"\"
            ✅ **Hasil Simulasi:**
            - Teori: 16.67%
            - Simulasi ({n_rolls}x): {prob_seven:.2f}%
            - **Kesimpulan:** Semakin banyak iterasi, semakin akurat hasilnya!
            \"\"\")
    
    # Section 3: Agricultural Application
    with st.expander("🌾 **3. Aplikasi di Pertanian: Prediksi Hasil Panen**"):
        st.markdown(\"\"\"
        ### Skenario Nyata
        Seorang petani cabai ingin tahu: **"Berapa kemungkinan saya untung minimal 30%?"**
        
        **Faktor Tidak Pasti:**
        1. **Cuaca**: Bisa kering (yield -20%), normal (0%), atau basah (-10%)
        2. **Hama**: Ringan (0%), sedang (-15%), berat (-30%)
        3. **Harga Jual**: Bisa Rp 40.000/kg (rendah), Rp 60.000/kg (normal), Rp 80.000/kg (tinggi)
        4. **Biaya Input**: Pupuk bisa naik 0-20% dari rencana
        
        ### Simulasi Monte Carlo (1000 Skenario)
        \"\"\")
        
        # Simple Agricultural Monte Carlo
        if st.button("🌶️ Simulasikan Usaha Tani Cabai"):
            np.random.seed(42)
            n_sim = 1000
            
            # Base assumptions
            base_yield = 5000  # kg/ha
            base_price = 60000  # Rp/kg
            base_cost = 150000000  # Rp/ha
            
            roi_results = []
            
            for _ in range(n_sim):
                # Random factors
                weather_impact = np.random.choice([0.8, 1.0, 0.9], p=[0.2, 0.6, 0.2])  # Drought, Normal, Flood
                pest_impact = np.random.choice([1.0, 0.85, 0.7], p=[0.5, 0.3, 0.2])  # Light, Medium, Heavy
                price = np.random.normal(60000, 15000)  # Mean 60k, StdDev 15k
                cost_multiplier = np.random.uniform(1.0, 1.2)  # Cost can increase 0-20%
                
                # Calculate scenario
                actual_yield = base_yield * weather_impact * pest_impact
                revenue = actual_yield * max(price, 20000)  # Floor price 20k
                cost = base_cost * cost_multiplier
                profit = revenue - cost
                roi = (profit / cost) * 100
                
                roi_results.append(roi)
            
            # Analysis
            mean_roi = np.mean(roi_results)
            prob_profit = (np.array(roi_results) > 0).sum() / n_sim * 100
            prob_30pct = (np.array(roi_results) > 30).sum() / n_sim * 100
            var_95 = np.percentile(roi_results, 5)  # Worst 5% case
            
            # Display Results
            col_r1, col_r2, col_r3 = st.columns(3)
            col_r1.metric("ROI Rata-rata", f"{mean_roi:.1f}%")
            col_r2.metric("Prob. Untung (ROI > 0%)", f"{prob_profit:.1f}%")
            col_r3.metric("Prob. Untung > 30%", f"{prob_30pct:.1f}%")
            
            # Histogram
            fig_agri = go.Figure()
            fig_agri.add_trace(go.Histogram(x=roi_results, nbinsx=40, name='ROI Distribution'))
            fig_agri.add_vline(x=0, line_color="black", annotation_text="BEP")
            fig_agri.add_vline(x=30, line_dash="dash", line_color="green", annotation_text="Target 30%")
            fig_agri.add_vline(x=var_95, line_dash="dot", line_color="red", annotation_text=f"VaR 95%: {var_95:.0f}%")
            fig_agri.update_layout(title="Distribusi ROI Usaha Tani Cabai (1000 Simulasi)",
                                  xaxis_title="ROI (%)", yaxis_title="Frekuensi")
            st.plotly_chart(fig_agri, use_container_width=True)
            
            st.info(f\"\"\"
            **📊 Interpretasi Hasil:**
            - **Rata-rata ROI**: {mean_roi:.1f}% (ekspektasi keuntungan)
            - **Probabilitas Untung**: {prob_profit:.1f}% (kemungkinan tidak rugi)
            - **Probabilitas Target (>30%)**: {prob_30pct:.1f}%
            - **Value at Risk (VaR 95%)**: {var_95:.1f}% (skenario terburuk 5%)
            
            **💡 Keputusan Bisnis:**
            - Jika prob. untung < 70% → **Risiko Tinggi**, pertimbangkan mitigasi
            - Jika VaR < -20% → Ada risiko rugi besar, siapkan dana cadangan
            \"\"\")
    
    # Section 4: Code Walkthrough
    with st.expander("💻 **4. Cara Kerja Kode Simulasi**"):
        st.markdown(\"\"\"
        ### Pseudocode Monte Carlo untuk Pertanian
        \"\"\")
        
        st.code(\"\"\"
# Langkah 1: Setup Parameter
n_simulations = 1000  # Jumlah skenario
base_yield = 5000     # Hasil panen dasar (kg/ha)
base_price = 60000    # Harga jual dasar (Rp/kg)

# Langkah 2: Loop Simulasi
results = []
for i in range(n_simulations):
    # Generate random factors
    weather_factor = random.choice([0.8, 1.0, 0.9])  # Kering, Normal, Basah
    pest_factor = random.choice([1.0, 0.85, 0.7])    # Ringan, Sedang, Berat
    price = random.normal(60000, 15000)              # Harga fluktuatif
    
    # Hitung hasil skenario ini
    actual_yield = base_yield * weather_factor * pest_factor
    revenue = actual_yield * price
    roi = (revenue - cost) / cost * 100
    
    results.append(roi)

# Langkah 3: Analisis Distribusi
mean_roi = np.mean(results)
probability_profit = (results > 0).sum() / n_simulations
worst_case_5pct = np.percentile(results, 5)

# Langkah 4: Visualisasi
plot_histogram(results)
        \"\"\", language='python')
        
        st.markdown(\"\"\"
        ### Parameter yang Bisa Diubah User
        Di aplikasi ini, Anda bisa mengatur:
        - **Jumlah Simulasi**: Lebih banyak = lebih akurat (tapi lebih lambat)
        - **Distribusi Probabilitas**: Misalnya, jika Anda tahu El Nino datang, 
          ubah probabilitas kekeringan dari 20% jadi 60%
        - **Range Harga**: Sesuaikan dengan data historis pasar lokal Anda
        \"\"\")
    
    # Section 5: References
    with st.expander("📚 **5. Referensi & Sumber Belajar**"):
        st.markdown(\"\"\"
        ### Paper Ilmiah (Pertanian)
        1. **Ramirez-Villegas et al. (2013)**: "Implications of regional improvement in global climate models for agricultural impact research"
           - Menggunakan Monte Carlo untuk model perubahan iklim di pertanian
        
        2. **Asseng et al. (2013)**: "Uncertainty in simulating wheat yields under climate change"
           - Monte Carlo untuk prediksi hasil gandum dengan ketidakpastian iklim
        
        3. **Challinor et al. (2009)**: "Crops and climate change: progress, trends, and challenges in simulating impacts and informing adaptation"
           - Review komprehensif simulasi Monte Carlo di agrikultur
        
        ### Buku Rekomendasi
        - **"Monte Carlo Methods in Financial Engineering"** - Paul Glasserman (2003)
          *(Meskipun fokus keuangan, prinsipnya sama untuk pertanian)*
        
        - **"Simulation Modeling and Analysis"** - Averill Law (2015)
          *(Textbook klasik tentang simulasi, termasuk Monte Carlo)*
        
        ### Online Resources
        - **Khan Academy**: Probability & Statistics (gratis)
        - **Coursera**: "Monte Carlo Methods in Finance" (University of Washington)
        - **YouTube**: "StatQuest with Josh Starmer" - Penjelasan visual tentang distribusi probabilitas
        
        ### Tools Lanjutan
        - **@RISK (Excel Add-in)**: Software komersial untuk Monte Carlo di Excel
        - **Python Libraries**: `numpy.random`, `scipy.stats`, `pymc3` (Bayesian Monte Carlo)
        - **R Packages**: `mc2d`, `sensitivity`
        
        ### Kontak Expert
        Jika Anda tertarik mendalami Monte Carlo untuk riset pertanian:
        - **CGIAR**: Consultative Group for International Agricultural Research
        - **IRRI**: International Rice Research Institute (punya divisi modeling)
        \"\"\")
    
    # Final Summary
    st.markdown("---")
    st.success(\"\"\"
    ### 🎯 Kesimpulan
    
    **Monte Carlo Simulation** adalah alat yang sangat powerful untuk:
    - Menghadapi ketidakpastian (cuaca, harga, hama)
    - Membuat keputusan berbasis data probabilistik
    - Memahami **rentang risiko**, bukan hanya satu angka prediksi
    
    **Kunci Sukses Menggunakan Monte Carlo:**
    1. **Garbage In, Garbage Out**: Kualitas input (asumsi probabilitas) menentukan kualitas output
    2. **Iterasi Cukup**: Minimal 1000 simulasi untuk hasil stabil
    3. **Interpretasi Bijak**: Hasil adalah **estimasi**, bukan kepastian
    
    **Next Steps:**
    - Coba tab "🎲 Monte Carlo" di atas dengan data riil Anda
    - Bandingkan hasil simulasi dengan realitas panen Anda
    - Gunakan untuk perencanaan musim tanam berikutnya
    \"\"\")
"""
