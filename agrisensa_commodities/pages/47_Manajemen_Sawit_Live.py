
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

# Page Config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Manajemen Sawit Pro",
    page_icon="🌴",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #14532d 0%, #166534 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.15);
    }
    .metric-card {
        background: #f0fdf4;
        border-left: 5px solid #15803d;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .warning-card {
        background: #fef2f2;
        border-left: 5px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
        color: #991b1b;
    }
    h1, h2, h3 { color: #14532d; }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header"><h1>🌴 Manajemen Sawit Pro</h1><p>Agronomy Intelligence System: Yield, Nutrisi, & Kualitas</p></div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["📊 Potensi Yield (S-Curve)", "🧪 Nutrisi & LSU (Daun)", "🏭 Grading Pabrik (OER)"])

# --- TAB 1: YIELD PREDICTION ---
with tab1:
    st.markdown("### 📊 Prediksi Produksi (Standard Yield Curve)")
    st.info("Simulasi potensi produksi TBS berdasarkan kurva pertumbuhan standar varietas unggul (Ref: PPKS/Socfindo Benchmark).")
    
    col_y1, col_y2 = st.columns([1, 2])
    
    with col_y1:
        thn_tanam = st.number_input("Tahun Tanam:", min_value=1990, max_value=datetime.datetime.now().year, value=2015)
        luas_ha = st.number_input("Luas Lahan (Ha):", value=10.0, step=0.5)
        sph = st.number_input("SPH (Pokok/Ha):", value=136, help="Standar: 128-143 pokok/ha. Kerapatan tinggi = kompetisi sinar.")
        
        umur = datetime.datetime.now().year - thn_tanam
        st.write(f"**Umur Tanaman:** {umur} Tahun")
        
        # Status Tananman
        if umur < 3: status_tm = "TBM (Belum Menghasilkan)"
        elif umur < 8: status_tm = "TM Muda (Young Mature)"
        elif umur < 18: status_tm = "TM Remaja (Prime Mature)"
        else: status_tm = "TM Tua (Old Mature)"
        
        st.caption(f"Status: **{status_tm}**")

    with col_y2:
        # LOGIC: SIMPLE S-CURVE MODEL for Yield (Ton/Ha)
        # 3 th: 5, 4 th: 10, 5 th: 14, 6 th: 18, 7 th: 22, 8-15 th: 26-30 (Peak), >20 decline
        
        def get_std_yield(age):
            if age < 3: return 0
            if age == 3: return 6.0
            if age == 4: return 12.0
            if age == 5: return 16.0
            if age == 6: return 20.0
            if age == 7: return 23.0
            if age == 8: return 25.0
            if 9 <= age <= 18: return 28.0 # Peak genetic potential
            if age > 18: return max(28.0 - ((age-18)*0.5), 15.0) # Decline
            return 0
            
        std_yield_ha = get_std_yield(umur)
        
        # LOGIC: Yield adjustments based on SPH (Intra-stand competition)
        # Standard SPH reference = 136 pokok/ha
        # If SPH goes up, yield/tree goes down due to canopy competition.
        
        base_yield_per_tree = std_yield_ha / 136.0 # Ton/tree
        
        competition_factor = 1.0
        if sph > 136:
            # Overcrowding penalty: Yield per tree drops 0.6% for every 1 extra tree
            competition_factor = 1.0 - ((sph - 136) * 0.006) 
        elif sph < 136:
            # Lower density bonus: Yield per tree increases 0.2% (more light) but capped
            competition_factor = 1.0 + ((136 - sph) * 0.002)
            
        final_yield_per_tree = base_yield_per_tree * competition_factor
        final_yield_ha = final_yield_per_tree * sph
        total_tbs = final_yield_ha * luas_ha
        bjr_est = 3.5 + (umur * 0.5) if umur < 10 else 10.0 + ((umur-10)*0.2) # Estimasi Berat Janjang
        if bjr_est > 25: bjr_est = 25 # Cap max BJR
        
        # Display Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Target Yield (Ton/Ha)", f"{final_yield_ha:.1f}", delta=f"{'Peak' if 9<=umur<=18 else 'Growing/Decline'}")
        m2.metric("Total Produksi (Ton/Thn)", f"{total_tbs:,.0f}")
        m3.metric("Estimasi BJR (kg)", f"{bjr_est:.1f}")
        
        def get_competition_factor(s):
            if s > 136: return 1.0 - ((s - 136) * 0.006)
            elif s < 136: return 1.0 + ((136 - s) * 0.002)
            return 1.0
            
        # Plotting the Curve
        ages = list(range(3, 26))
        # Use current SPH (constant) for the forecast line
        current_comp_factor = get_competition_factor(sph)
        yields = [get_std_yield(a) * current_comp_factor for a in ages]
        
        df_chart = pd.DataFrame({"Umur": ages, "Yield (Ton/Ha)": yields})
        df_chart['Status'] = ["Current" if a == umur else "Forecast" for a in ages]
        
        fig = px.line(df_chart, x="Umur", y="Yield (Ton/Ha)", title="Kurva Siklus Hidup Produktivitas (Life Cycle)", markers=True)
        # Add point for current age
        fig.add_trace(go.Scatter(x=[umur], y=[final_yield_ha], mode='markers', marker=dict(color='red', size=12), name='Saat Ini'))
        
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: NUTRISI & LSU ---
with tab2:
    st.markdown("### 🧪 Analisa Hara & Rekomendasi Pemupukan")
    st.info("Gunakan data Leaf Sampling Unit (LSU) dari Pelepah ke-17 untuk diagnosa presisi.")
    
    col_n1, col_n2 = st.columns([1, 1])
    
    with col_n1:
        st.subheader("🍃 Input Laboratorium Daun (LSU)")
        st.caption("Masukan % berat kering (Dry Matter Basis) dari hasil lab.")
        
        n_val = st.number_input("Nitrogen (% N)", 2.00, 3.50, 2.45, step=0.01)
        p_val = st.number_input("Fosfor (% P)", 0.10, 0.30, 0.150, step=0.001, format="%.3f")
        k_val = st.number_input("Kalium (% K)", 0.50, 2.00, 0.95, step=0.01)
        mg_val = st.number_input("Magnesium (% Mg)", 0.10, 0.50, 0.22, step=0.01)
        b_val = st.number_input("Boron (ppm B)", 5.0, 50.0, 15.0, step=1.0)
        
    with col_n2:
        st.subheader("🩺 Diagnosa Dokter Sawit")
        
        # CRITICAL LEVELS (Simplified from Fairhurst & Hardter, 2003)
        def check_status(name, val, crit_low, crit_high, opt_low, opt_high):
            if val < crit_low: return "🔴 Deficiency (Kritis)", f"Genjot pupuk {name} segera!"
            if val < opt_low: return "🟡 Low (Rendah)", f"Tambah dosis {name}."
            if val > crit_high: return "🔴 Excess (Beracun)", f"Stop pupuk {name}, boros/racun."
            if val > opt_high: return "🔵 High (Tinggi)", f"Kurangi dosis {name}."
            return "✅ Optimum", "Pertahankan dosis."

        # N Check (Optimum 2.50 - 2.80)
        s_n, r_n = check_status("Nitrogen", n_val, 2.30, 3.2, 2.50, 2.90)
        # P Check (Optimum 0.15 - 0.18)
        s_p, r_p = check_status("Fosfor", p_val, 0.13, 0.25, 0.15, 0.19)
        # K Check (Optimum 1.00 - 1.25)
        s_k, r_k = check_status("Kalium", k_val, 0.80, 1.6, 1.00, 1.30)
        # Mg Check (Optimum 0.24 - 0.30)
        s_mg, r_mg = check_status("Magnesium", mg_val, 0.20, 0.40, 0.24, 0.30)
        
        st.markdown(f"**Nitrogen (Urea):** {s_n} -> *{r_n}*")
        st.markdown(f"**Fosfor (TSP/RP):** {s_p} -> *{r_p}*")
        st.markdown(f"**Kalium (MOP):** {s_k} -> *{r_k}*")
        st.markdown(f"**Magnesium (Kieserite):** {s_mg} -> *{r_mg}*")
        
        # N/K Ratio Logic (Balance)
        nk_ratio = n_val / k_val
        st.markdown("---")
        st.markdown(f"**Rasio N/K:** {nk_ratio:.2f}")
        if nk_ratio > 3.0:
            st.warning("⚠️ Rasio N/K terlalu tinggi (>3.0). Tanaman rentan penyakit & Yield turun (Buah kecil). Tambah K!")
        elif nk_ratio < 2.0:
            st.warning("⚠️ Rasio N/K terlalu rendah (<2.0). Efisiensi N rendah. Tambah N!")
        else:
            st.success("✅ Keseimbangan Hara Bagus (2.0 - 3.0).")

# --- TAB 3: MILL GRADING ---
with tab3:
    st.markdown("### 🏭 Simulasi Grading PKS (Rendemen)")
    st.info("Menghitung potensi OER (Oil Extraction Rate) dan Penalti harga.")
    
    col_m1, col_m2 = st.columns(2)
    
    with col_m1:
        st.write("#### 🚛 Kualitas Buah Masuk")
        berat_kirim = st.number_input("Berat Kirim (Ton)", 5.0, 20.0, 8.0)
        
        f0_mentah = st.slider("% Buah Mentah (Unripe - Hitam)", 0, 50, 5)
        f1_mengkal = st.slider("% Buah Mengkal (Underripe)", 0, 50, 10)
        f23_matang = st.slider("% Buah Matang (Ripe - Merah)", 0, 100, 80)
        f_tangkai = st.slider("% Tangkai Panjang (>2.5cm)", 0, 20, 2)
        
        # Normalization check
        total_p = f0_mentah + f1_mengkal + f23_matang
        if total_p != 100 and total_p > 0:
            st.warning(f"Total Fraksi Biologis: {total_p}% (Idealnya 100%). Sisa dianggap sampah/rusak.")
            
    with col_m2:
        st.write("#### 📉 Hasil Analisa & Potongan")
        
        # REF OER POTENTIAL
        # Mentah: 14% OER, Mengkal: 18% OER, Matang: 23% OER
        oer_potential = ((f0_mentah * 0.14) + (f1_mengkal * 0.18) + (f23_matang * 0.235)) 
        
        # FFA Prediction (Mentah = High Water, Lewat Matang = High FFA)
        # Simplified logic
        ffa_base = 2.5
        if f0_mentah > 10: ffa_base += 1.0 # Sulit lepas, wounding process lama -> FFA naik
        
        # PENALTY LOGIC (Common PKS Rules)
        # Mentah > 0% -> Potong 50% dari berat janjang mentah (Extreme rule) or just grading deduction
        # Here we use simplified deduction %
        deduction_pct = 0
        if f0_mentah > 0: deduction_pct += (f0_mentah * 0.5) # PKS kejam, mentah dipotong setengah
        if f_tangkai > 1: deduction_pct += (f_tangkai * 1.0) # Tangkai panjang sampah
        
        berat_bersih = berat_kirim * (1 - (deduction_pct/100))
        loss_ton = berat_kirim - berat_bersih
        
        st.markdown(f"""
        <div class="metric-card">
            <h3>🛢️ Potensi Rendemen (OER): {oer_potential:.2f}%</h3>
            <p>Target Industri: >23.0%</p>
        </div>
        """, unsafe_allow_html=True)
        
        if oer_potential < 21.0:
            st.markdown('<div class="warning-card">⚠️ <b>OER RENDAH!</b> Banyak buah mentah. Pabrik rugi.</div>', unsafe_allow_html=True)
            
        st.markdown("---")
        st.metric("Potongan Grading (Sortasi)", f"{deduction_pct:.1f} %", delta_color="inverse", delta=f"{loss_ton:.2f} Ton Hilang")
        st.caption("Alasan Potongan: Buah Mentah (Unripe) & Tangkai Panjang.")

# Footer
st.markdown("---")
st.caption("Referensi: PPKS (Pusat Penelitian Kelapa Sawit) & Jurnal Agronomi Industri (Fairhurst & Hardter, 2003)")
