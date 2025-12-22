import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Peternakan & Perikanan - AgriSensa",
    page_icon="🐄",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================






# Header
st.title("🐄 Manajemen Peternakan & Perikanan")
st.markdown("**Solusi Presisi untuk Ruminansia, Unggas, dan Budidaya Perikanan**")
st.info("💡 Modul ini menyediakan alat bantu hitung teknis (Ransum, FCR, Bioflok) dan asisten kesehatan hewan.")

# Main tabs
tab_ruminant, tab_poultry, tab_fish, tab_feed, tab_vet = st.tabs([
    "🐄 Ruminansia (Sapi/Kambing)",
    "🐓 Unggas (Ayam/Bebek)",
    "🐟 Perikanan (Bioflok/RAS)",
    "🧮 Kalkulator Ransum",
    "🩺 Dokter Hewan AI"
])

# ===== TAB 1: RUMINANSIA =====
with tab_ruminant:
    st.header("🐄 Manajemen Ruminansia")
    
    col_r1, col_r2 = st.columns(2)
    
    with col_r1:
        st.subheader("📊 Kalkulator ADG (PBBH)")
        st.markdown("*Average Daily Gain / Pertambahan Bobot Badan Harian*")
        
        awal = st.number_input("Bobot Awal (kg)", value=250.0, step=0.1)
        akhir = st.number_input("Bobot Akhir (kg)", value=300.0, step=0.1)
        hari = st.number_input("Jangka Waktu (hari)", value=30, step=1)
        
        if st.button("Hitung ADG"):
            if hari > 0:
                adg = (akhir - awal) / hari
                st.metric("ADG (kg/hari)", f"{adg:.2f} kg")
                
                if adg > 1.0:
                    st.success("✅ Pertumbuhan Sangat Baik (Sapi Potong)")
                elif adg > 0.6:
                    st.info("ℹ️ Pertumbuhan Cukup Baik")
                else:
                    st.warning("⚠️ Pertumbuhan Lambat. Evaluasi pakan & kesehatan.")
            else:
                st.error("Hari harus > 0")
                
    with col_r2:
        st.subheader("🍼 Estimasi Kebutuhan Pakan")
        st.markdown("Basis: Bahan Kering (Dry Matter) = 3% Bobot Badan")
        
        bb_sapi = st.number_input("Bobot Sapi Saat Ini (kg)", value=300)
        bk_pct = 3.0 # Persen bahan kering kebutuhan
        
        bk_total = bb_sapi * (bk_pct / 100)
        
        # Asumsi Hijauan punya BK 20%, Konsentrat BK 85%
        # Rasio Hijauan:Konsentrat = 60:40
        ratio_h = 60
        ratio_k = 40
        
        bk_hijauan = bk_total * (ratio_h/100)
        bk_konsentrat = bk_total * (ratio_k/100)
        
        # Konversi ke As Fed (Segar)
        segar_hijauan = bk_hijauan / 0.20
        segar_konsentrat = bk_konsentrat / 0.85
        
        st.write(f"**Total Kebutuhan Bahan Kering:** {bk_total:.2f} kg/hari")
        st.info(f"""
        **Rekomendasi Pemberian (As Fed/Segar):**
        *   🌾 **Hijauan (Rumput):** ± {segar_hijauan:.1f} kg
        *   📦 **Konsentrat:** ± {segar_konsentrat:.1f} kg
        *(Asumsi rasio 60:40)*
        """)

# ===== TAB 2: UNGGAS (ENHANCED) =====
with tab_poultry:
    st.header("🐓 Manajemen Unggas (Broiler/Layer)")
    st.info("💡 Modul komprehensif dengan KPI industri, standar performa, analisis biaya, dan integrasi circular economy (olahan kotoran).")
    
    # Sub-tabs for Poultry
    stab_dashboard, stab_broiler, stab_layer, stab_produksi, stab_biaya, stab_pasca = st.tabs([
        "📊 Dashboard KPI",
        "🐔 Broiler (Pedaging)",
        "🥚 Layer (Petelur)",
        "📈 Analisis Produksi",
        "💰 Analisis Biaya",
        "♻️ Pasca Panen"
    ])
    
    # ========== SUB-TAB 1: DASHBOARD KPI ==========
    with stab_dashboard:
        st.subheader("📊 Dashboard KPI Unggas")
        st.markdown("**Real-time Performance Indicators** dengan benchmark industri.")
        
        # Input Section
        col_input1, col_input2 = st.columns(2)
        
        with col_input1:
            st.markdown("##### 📝 Data Periode")
            kpi_populasi = st.number_input("Populasi Awal (DOC)", value=5000, step=100, key="kpi_pop")
            kpi_mati = st.number_input("Total Kematian (ekor)", value=150, step=10, key="kpi_mati")
            kpi_umur = st.number_input("Umur Panen (hari)", value=35, step=1, key="kpi_umur")
        
        with col_input2:
            st.markdown("##### 📦 Data Pakan & Hasil")
            kpi_pakan = st.number_input("Total Pakan (kg)", value=15000.0, step=100.0, key="kpi_pakan")
            kpi_bobot_avg = st.number_input("Bobot Rata-rata (kg)", value=2.0, step=0.1, key="kpi_bb")
            kpi_bobot_doc = st.number_input("Bobot DOC (gram)", value=40, step=5, key="kpi_doc")
        
        st.divider()
        
        # Calculate KPIs
        kpi_hidup = kpi_populasi - kpi_mati
        kpi_deplesi = (kpi_mati / kpi_populasi) * 100 if kpi_populasi > 0 else 0
        kpi_livability = 100 - kpi_deplesi
        kpi_total_bobot = kpi_hidup * kpi_bobot_avg
        kpi_fcr = kpi_pakan / kpi_total_bobot if kpi_total_bobot > 0 else 0
        kpi_adg = ((kpi_bobot_avg * 1000) - kpi_bobot_doc) / kpi_umur if kpi_umur > 0 else 0
        kpi_ip = ((kpi_livability * kpi_bobot_avg) / (kpi_fcr * kpi_umur)) * 100 if (kpi_fcr > 0 and kpi_umur > 0) else 0
        
        # Display KPI Cards
        st.markdown("### 🎯 Indikator Kinerja Utama")
        
        kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)
        
        with kpi_c1:
            fcr_delta = kpi_fcr - 1.6
            fcr_status = "🟢" if kpi_fcr < 1.6 else ("🟡" if kpi_fcr < 1.8 else "🔴")
            st.metric("FCR " + fcr_status, f"{kpi_fcr:.3f}", f"{fcr_delta:+.3f} vs target 1.6")
            st.caption("Target: < 1.6")
        
        with kpi_c2:
            ip_status = "🟢" if kpi_ip > 350 else ("🟡" if kpi_ip > 300 else "🔴")
            st.metric("Indeks Performa " + ip_status, f"{kpi_ip:.0f}", f"Target: >350")
            st.caption("🌟 >400 = Istimewa")
        
        with kpi_c3:
            depl_status = "🟢" if kpi_deplesi < 5 else ("🟡" if kpi_deplesi < 8 else "🔴")
            st.metric("Deplesi " + depl_status, f"{kpi_deplesi:.2f}%", f"Target: <5%")
            st.caption(f"Hidup: {kpi_hidup:,} ekor")
        
        with kpi_c4:
            adg_status = "🟢" if kpi_adg > 55 else ("🟡" if kpi_adg > 50 else "🔴")
            st.metric("ADG " + adg_status, f"{kpi_adg:.1f} g/hari", f"Target: >55")
            st.caption("Average Daily Gain")
        
        # Gauge Charts
        st.divider()
        st.markdown("### 📈 Visualisasi Performa")
        
        import plotly.graph_objects as go
        
        gauge_c1, gauge_c2 = st.columns(2)
        
        with gauge_c1:
            fig_fcr = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=kpi_fcr,
                title={'text': "Feed Conversion Ratio (FCR)"},
                delta={'reference': 1.6, 'increasing': {'color': "red"}, 'decreasing': {'color': "green"}},
                gauge={
                    'axis': {'range': [1.0, 2.5]},
                    'bar': {'color': "#3b82f6"},
                    'steps': [
                        {'range': [1.0, 1.6], 'color': "#d1fae5"},
                        {'range': [1.6, 1.8], 'color': "#fef3c7"},
                        {'range': [1.8, 2.5], 'color': "#fee2e2"}
                    ],
                    'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 1.6}
                }
            ))
            fig_fcr.update_layout(height=250)
            st.plotly_chart(fig_fcr, use_container_width=True)
        
        with gauge_c2:
            fig_ip = go.Figure(go.Indicator(
                mode="gauge+number",
                value=kpi_ip,
                title={'text': "Indeks Performa (IP)"},
                gauge={
                    'axis': {'range': [0, 500]},
                    'bar': {'color': "#10b981"},
                    'steps': [
                        {'range': [0, 300], 'color': "#fee2e2"},
                        {'range': [300, 350], 'color': "#fef3c7"},
                        {'range': [350, 400], 'color': "#d1fae5"},
                        {'range': [400, 500], 'color': "#a7f3d0"}
                    ],
                    'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 350}
                }
            ))
            fig_ip.update_layout(height=250)
            st.plotly_chart(fig_ip, use_container_width=True)
        
        # Summary Table
        st.markdown("### 📋 Ringkasan Periode")
        summary_data = {
            "Parameter": ["Populasi Awal", "Populasi Panen", "Deplesi", "Total Pakan", "Total Bobot Panen", "FCR", "IP", "ADG"],
            "Nilai": [f"{kpi_populasi:,}", f"{kpi_hidup:,}", f"{kpi_deplesi:.2f}%", f"{kpi_pakan:,.0f} kg", 
                     f"{kpi_total_bobot:,.0f} kg", f"{kpi_fcr:.3f}", f"{kpi_ip:.0f}", f"{kpi_adg:.1f} g/hari"],
            "Benchmark": ["DOC", ">95%", "<5%", "-", "-", "<1.6", ">350", ">55 g"]
        }
        st.table(pd.DataFrame(summary_data))
    
    # ========== SUB-TAB 2: BROILER ==========
    with stab_broiler:
        st.subheader("🐔 Manajemen Broiler (Ayam Pedaging)")
        
        # Standard Performance Table
        st.markdown("### 📊 Standar Performa Broiler (Cobb 500)")
        
        standard_data = {
            "Umur (Hari)": [7, 14, 21, 28, 35, 42],
            "BB Standar (g)": [180, 470, 900, 1420, 2000, 2700],
            "Konsumsi Kumulatif (g)": [153, 493, 1098, 1960, 3100, 4644],
            "FCR Target": [0.85, 1.05, 1.22, 1.38, 1.55, 1.72],
            "ADG (g/hari)": [20, 31, 40, 49, 56, 63]
        }
        df_standard = pd.DataFrame(standard_data)
        st.dataframe(df_standard, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Period Simulator
        st.markdown("### 🎯 Simulator Periode Pemeliharaan")
        
        sim_c1, sim_c2 = st.columns(2)
        
        with sim_c1:
            sim_doc = st.number_input("Jumlah DOC (ekor)", value=5000, step=500, key="sim_doc")
            sim_harga_doc = st.number_input("Harga DOC (Rp/ekor)", value=5500, step=100, key="sim_harga_doc")
            sim_target_bb = st.number_input("Target BB Panen (kg)", value=2.0, step=0.1, key="sim_bb")
            sim_umur_target = st.number_input("Target Umur Panen (hari)", value=35, step=1, key="sim_umur")
        
        with sim_c2:
            sim_deplesi_est = st.slider("Estimasi Deplesi (%)", 1.0, 15.0, 5.0, key="sim_depl")
            sim_fcr_est = st.slider("Estimasi FCR", 1.4, 2.0, 1.55, 0.01, key="sim_fcr")
            sim_harga_pakan = st.number_input("Harga Pakan (Rp/kg)", value=8500, step=100, key="sim_hpakan")
            sim_harga_jual = st.number_input("Harga Jual (Rp/kg hidup)", value=19000, step=500, key="sim_hjual")
        
        # Calculations
        sim_hidup = sim_doc * (1 - sim_deplesi_est/100)
        sim_total_bb = sim_hidup * sim_target_bb
        sim_total_pakan = sim_total_bb * sim_fcr_est
        
        # Costs & Revenue
        sim_cost_doc = sim_doc * sim_harga_doc
        sim_cost_pakan = sim_total_pakan * sim_harga_pakan
        sim_cost_lain = sim_cost_doc * 0.15  # 15% for medication, labor, etc.
        sim_total_cost = sim_cost_doc + sim_cost_pakan + sim_cost_lain
        sim_revenue = sim_total_bb * sim_harga_jual
        sim_profit = sim_revenue - sim_total_cost
        sim_margin = (sim_profit / sim_revenue) * 100 if sim_revenue > 0 else 0
        
        st.divider()
        st.markdown("### 💰 Proyeksi Finansial")
        
        fin_c1, fin_c2, fin_c3, fin_c4 = st.columns(4)
        fin_c1.metric("Total Biaya", f"Rp {sim_total_cost/1e6:.1f} Jt")
        fin_c2.metric("Revenue", f"Rp {sim_revenue/1e6:.1f} Jt")
        fin_c3.metric("Profit", f"Rp {sim_profit/1e6:.1f} Jt", f"{sim_margin:.1f}%")
        fin_c4.metric("BEP/kg", f"Rp {sim_total_cost/sim_total_bb:,.0f}")
        
        # Growth Chart
        st.markdown("### 📈 Kurva Pertumbuhan Standar")
        
        df_growth = pd.DataFrame({
            "Umur (Hari)": [0, 7, 14, 21, 28, 35, 42],
            "Standar (g)": [40, 180, 470, 900, 1420, 2000, 2700]
        })
        
        fig_growth = px.line(df_growth, x="Umur (Hari)", y="Standar (g)", 
                            title="Standar Pertumbuhan Broiler (Cobb 500)",
                            markers=True)
        fig_growth.update_traces(line_color='#10b981', line_width=3)
        fig_growth.add_hline(y=sim_target_bb*1000, line_dash="dash", line_color="red",
                            annotation_text=f"Target: {sim_target_bb}kg")
        st.plotly_chart(fig_growth, use_container_width=True)
    
    # ========== SUB-TAB 3: LAYER ==========
    with stab_layer:
        st.subheader("🥚 Manajemen Layer (Ayam Petelur)")
        
        # Standard Performance Table
        st.markdown("### 📊 Standar Produksi Layer (Lohmann Brown)")
        
        layer_data = {
            "Umur (Minggu)": [20, 24, 28, 32, 40, 52, 60, 72],
            "HDEP (%)": [10, 85, 95, 93, 90, 85, 80, 75],
            "Egg Mass (g/hari)": [5.5, 51, 60, 59, 58, 55, 52, 48],
            "Konsumsi (g/hari)": [95, 115, 122, 120, 125, 122, 120, 118],
            "BB (kg)": [1.5, 1.8, 2.0, 2.0, 2.1, 2.1, 2.1, 2.1]
        }
        st.dataframe(pd.DataFrame(layer_data), use_container_width=True, hide_index=True)
        
        st.divider()
        
        # HDEP Calculator
        st.markdown("### 🔢 Kalkulator HDEP (Hen Day Egg Production)")
        
        hdep_c1, hdep_c2 = st.columns(2)
        
        with hdep_c1:
            hdep_populasi = st.number_input("Populasi Ayam (ekor)", value=1000, step=100, key="hdep_pop")
            hdep_telur = st.number_input("Produksi Telur Hari Ini (butir)", value=850, step=10, key="hdep_telur")
        
        with hdep_c2:
            hdep_bobot_telur = st.number_input("Bobot Telur Rata-rata (gram)", value=62, step=1, key="hdep_bt")
            hdep_pakan = st.number_input("Konsumsi Pakan Hari Ini (kg)", value=120.0, step=1.0, key="hdep_pakan")
        
        # Calculate
        hdep_pct = (hdep_telur / hdep_populasi) * 100 if hdep_populasi > 0 else 0
        egg_mass = (hdep_telur * hdep_bobot_telur) / 1000  # kg
        eem = egg_mass / hdep_pakan if hdep_pakan > 0 else 0  # Egg Efficiency Mass
        
        st.divider()
        
        hdep_m1, hdep_m2, hdep_m3 = st.columns(3)
        
        hdep_status = "🟢" if hdep_pct > 80 else ("🟡" if hdep_pct > 70 else "🔴")
        hdep_m1.metric("HDEP " + hdep_status, f"{hdep_pct:.1f}%", "Target: >80%")
        hdep_m2.metric("Egg Mass", f"{egg_mass:.2f} kg/hari")
        hdep_m3.metric("EEM", f"{eem:.3f}", "Target: >0.5")
        
        # Production Curve
        st.markdown("### 📈 Kurva Produksi Layer")
        
        production_curve = pd.DataFrame({
            "Umur (Minggu)": list(range(18, 76, 4)),
            "HDEP (%)": [5, 50, 90, 95, 93, 90, 87, 84, 81, 78, 75, 72, 69, 66, 63]
        })
        
        fig_prod = px.area(production_curve, x="Umur (Minggu)", y="HDEP (%)",
                          title="Kurva Produksi Telur (Typical Layer)")
        fig_prod.update_traces(fill='tozeroy', line_color='#f59e0b')
        fig_prod.add_hline(y=80, line_dash="dash", line_color="green",
                          annotation_text="Target HDEP: 80%")
        st.plotly_chart(fig_prod, use_container_width=True)
        
        # Egg Grading
        st.markdown("### 🥚 Distribusi Grading Telur")
        grade_c1, grade_c2 = st.columns([1, 2])
        
        with grade_c1:
            grade_xl = st.number_input("XL (>65g)", value=10, key="g_xl")
            grade_l = st.number_input("L (60-65g)", value=45, key="g_l")
            grade_m = st.number_input("M (55-60g)", value=35, key="g_m")
            grade_s = st.number_input("S (<55g)", value=8, key="g_s")
            grade_reject = st.number_input("Reject", value=2, key="g_rej")
        
        with grade_c2:
            fig_grade = px.pie(
                names=["XL", "L", "M", "S", "Reject"],
                values=[grade_xl, grade_l, grade_m, grade_s, grade_reject],
                title="Distribusi Grade Telur (%)",
                color_discrete_sequence=px.colors.sequential.Greens_r
            )
            st.plotly_chart(fig_grade, use_container_width=True)
    
    # ========== SUB-TAB 4: ANALISIS PRODUKSI ==========
    with stab_produksi:
        st.subheader("📈 Analisis Produksi")
        st.info("Tracking performa mingguan dan perbandingan antar batch.")
        
        # Weekly Input
        st.markdown("### 📅 Input Data Mingguan")
        
        week_c1, week_c2, week_c3, week_c4 = st.columns(4)
        with week_c1:
            week_no = st.selectbox("Minggu ke-", list(range(1, 7)), key="w_no")
        with week_c2:
            week_mati = st.number_input("Kematian Minggu Ini", value=20, key="w_mati")
        with week_c3:
            week_pakan = st.number_input("Pakan Minggu (kg)", value=2500.0, key="w_pakan")
        with week_c4:
            week_bb = st.number_input("BB Sampling (g)", value=1000, key="w_bb")
        
        # Simulated Weekly Data
        weekly_data = {
            "Minggu": [1, 2, 3, 4, 5],
            "Kematian": [50, 30, 25, 20, 15],
            "Pakan (kg)": [500, 1200, 2000, 2800, 3500],
            "BB Sampling (g)": [180, 450, 850, 1350, 1900],
            "FCR Mingguan": [0.85, 1.05, 1.22, 1.35, 1.50],
            "Deplesi Kum (%)": [1.0, 1.6, 2.1, 2.5, 2.8]
        }
        df_weekly = pd.DataFrame(weekly_data)
        
        st.markdown("### 📊 Tabel Performa Mingguan")
        st.dataframe(df_weekly, use_container_width=True, hide_index=True)
        
        # Charts
        chart_c1, chart_c2 = st.columns(2)
        
        with chart_c1:
            fig_bb = px.line(df_weekly, x="Minggu", y="BB Sampling (g)", 
                            title="Kurva Pertumbuhan", markers=True)
            fig_bb.update_traces(line_color='#10b981')
            st.plotly_chart(fig_bb, use_container_width=True)
        
        with chart_c2:
            fig_fcr = px.bar(df_weekly, x="Minggu", y="FCR Mingguan",
                            title="FCR per Minggu", color="FCR Mingguan",
                            color_continuous_scale="RdYlGn_r")
            st.plotly_chart(fig_fcr, use_container_width=True)
    
    # ========== SUB-TAB 5: ANALISIS BIAYA ==========
    with stab_biaya:
        st.subheader("💰 Analisis Biaya & Profitabilitas")
        
        st.markdown("### 📝 Input Komponen Biaya")
        
        cost_c1, cost_c2 = st.columns(2)
        
        with cost_c1:
            cost_doc = st.number_input("Biaya DOC (Rp)", value=27500000, step=500000, key="c_doc")
            cost_pakan = st.number_input("Biaya Pakan (Rp)", value=127500000, step=1000000, key="c_pakan")
            cost_obat = st.number_input("Obat & Vaksin (Rp)", value=7500000, step=500000, key="c_obat")
        
        with cost_c2:
            cost_tenaga = st.number_input("Tenaga Kerja (Rp)", value=6000000, step=500000, key="c_tenaga")
            cost_listrik = st.number_input("Listrik & Air (Rp)", value=3000000, step=250000, key="c_listrik")
            cost_lain = st.number_input("Lain-lain (Rp)", value=2000000, step=250000, key="c_lain")
        
        total_cost = cost_doc + cost_pakan + cost_obat + cost_tenaga + cost_listrik + cost_lain
        
        st.divider()
        
        # Cost Breakdown Chart
        st.markdown("### 📊 Breakdown Biaya")
        
        cost_breakdown = pd.DataFrame({
            "Komponen": ["DOC", "Pakan", "Obat/Vaksin", "Tenaga Kerja", "Listrik/Air", "Lain-lain"],
            "Nilai": [cost_doc, cost_pakan, cost_obat, cost_tenaga, cost_listrik, cost_lain]
        })
        
        fig_cost = px.pie(cost_breakdown, values="Nilai", names="Komponen",
                         title=f"Total Biaya: Rp {total_cost/1e6:.1f} Juta",
                         color_discrete_sequence=px.colors.sequential.Blues_r)
        st.plotly_chart(fig_cost, use_container_width=True)
        
        # Break-even Calculator
        st.markdown("### 🎯 Break-even Analysis")
        
        be_c1, be_c2 = st.columns(2)
        
        with be_c1:
            be_bobot_total = st.number_input("Total Bobot Panen (kg)", value=9500.0, key="be_bb")
            be_harga_jual = st.number_input("Harga Jual (Rp/kg)", value=19000, key="be_hj")
        
        with be_c2:
            be_revenue = be_bobot_total * be_harga_jual
            be_profit = be_revenue - total_cost
            be_margin = (be_profit / be_revenue) * 100 if be_revenue > 0 else 0
            be_bep_kg = total_cost / be_bobot_total if be_bobot_total > 0 else 0
            
            st.metric("BEP per kg", f"Rp {be_bep_kg:,.0f}")
            st.metric("Revenue", f"Rp {be_revenue/1e6:.1f} Juta")
            st.metric("Profit/Loss", f"Rp {be_profit/1e6:.1f} Juta", f"{be_margin:.1f}%")
    
    # ========== SUB-TAB 6: PASCA PANEN (MANURE PROCESSING) ==========
    with stab_pasca:
        st.subheader("♻️ Pasca Panen - Olahan Kotoran Ayam")
        st.success("🌱 **Circular Economy**: Ubah limbah menjadi pendapatan tambahan!")
        
        st.markdown("### 🧮 Kalkulator Produksi Kotoran")
        
        man_c1, man_c2 = st.columns(2)
        
        with man_c1:
            man_populasi = st.number_input("Populasi Ayam (ekor)", value=5000, step=500, key="man_pop")
            man_umur = st.number_input("Lama Pemeliharaan (hari)", value=35, step=1, key="man_umur")
            man_rate = st.number_input("Produksi Kotoran (g/ekor/hari)", value=150, step=10, key="man_rate",
                                       help="Broiler: ~150g, Layer: ~120g")
        
        # Calculate manure production
        man_total_kg = (man_populasi * man_rate * man_umur) / 1000
        man_total_ton = man_total_kg / 1000
        
        with man_c2:
            st.markdown("##### 📦 Hasil Estimasi")
            st.metric("Total Kotoran Basah", f"{man_total_kg:,.0f} kg", f"= {man_total_ton:.2f} ton")
            st.caption("*Asumsi kadar air 70-80%*")
        
        st.divider()
        
        # Product Value Table
        st.markdown("### 💰 Nilai Ekonomi Olahan")
        
        product_data = {
            "Produk": ["🔹 Kotoran Mentah", "🔹 Pupuk Kandang Kering", "🔹 Pupuk Fermentasi (EM4)", 
                      "🔹 Granul Organik", "🔹 Vermikompos"],
            "Proses": ["Kumpul langsung", "Penjemuran 3-5 hari", "+ EM4, 21 hari fermentasi",
                      "Mesin granulator", "+ Cacing Tanah"],
            "Rendemen (%)": [100, 50, 45, 40, 35],
            "Harga Min (Rp/kg)": [500, 1500, 3000, 5000, 8000],
            "Harga Max (Rp/kg)": [800, 2000, 5000, 8000, 15000]
        }
        df_product = pd.DataFrame(product_data)
        st.dataframe(df_product, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Revenue Calculator
        st.markdown("### 💵 Kalkulator Pendapatan Tambahan")
        
        rev_c1, rev_c2 = st.columns(2)
        
        with rev_c1:
            selected_product = st.selectbox("Pilih Produk Output:", 
                                           ["Kotoran Mentah", "Pupuk Kandang Kering", 
                                            "Pupuk Fermentasi (EM4)", "Granul Organik", "Vermikompos"],
                                           key="sel_prod")
            
            # Get values based on selection
            rendemen_map = {"Kotoran Mentah": 1.0, "Pupuk Kandang Kering": 0.5, 
                           "Pupuk Fermentasi (EM4)": 0.45, "Granul Organik": 0.4, "Vermikompos": 0.35}
            harga_map = {"Kotoran Mentah": (500, 800), "Pupuk Kandang Kering": (1500, 2000), 
                        "Pupuk Fermentasi (EM4)": (3000, 5000), "Granul Organik": (5000, 8000), 
                        "Vermikompos": (8000, 15000)}
            
            rendemen = rendemen_map.get(selected_product, 1.0)
            harga_range = harga_map.get(selected_product, (500, 800))
            
            man_harga_jual = st.slider("Harga Jual (Rp/kg)", harga_range[0], harga_range[1], 
                                       int((harga_range[0] + harga_range[1])/2), key="man_hj")
        
        with rev_c2:
            man_output = man_total_kg * rendemen
            man_revenue = man_output * man_harga_jual
            
            st.markdown("##### 📊 Proyeksi Pendapatan")
            st.metric("Output Produk", f"{man_output:,.0f} kg")
            st.metric("Pendapatan Tambahan", f"Rp {man_revenue/1e6:.2f} Juta", "Per Periode")
        
        # Tips
        st.divider()
        st.markdown("### 💡 Tips Pengolahan")
        
        with st.expander("📚 Panduan Fermentasi Cepat", expanded=False):
            st.markdown("""
            **Bahan:**
            - Kotoran ayam: 100 kg
            - Dedak/Sekam: 10 kg
            - EM4/MOL: 100 ml
            - Gula/Molase: 100 ml
            - Air secukupnya
            
            **Cara:**
            1. Campurkan semua bahan hingga rata
            2. Kelembaban target: 50-60% (seperti tanah basah)
            3. Tutup dengan terpal, beri lubang aerasi
            4. Balik setiap 3 hari
            5. Siap pakai dalam 14-21 hari (tidak berbau, warna gelap)
            
            **C/N Ratio:** Target 20-25 (tambah sekam jika terlalu basau)
            """)
        
        with st.expander("🔗 Integrasi dengan Modul Lain"):
            st.markdown("""
            - 📗 **Modul 54 (Pengolahan Sampah)**: Detail proses fermentasi & upcycling
            - 📗 **Modul 3 (Pupuk Organik)**: Panduan aplikasi ke tanaman
            - 📗 **Modul 6 (Analisis Pasar)**: Harga jual pupuk organik
            """)

# ===== TAB 3: PERIKANAN =====
with tab_fish:
    st.header("🐟 Perikanan (Komoditas & Pakan)")
    st.markdown("Panduan teknis budidaya, pakan alternatif berbasis jurnal, dan manajemen kualitas air.")
    
    # --- SUB TABS PERIKANAN ---
    stab_lele, stab_nila, stab_gurame, stab_unagi, stab_bioflok, stab_pakan = st.tabs([
        "🐟 Lele (Catfish)",
        "🐠 Nila (Tilapia)",
        "🐡 Gurame (Gourami)",
        "🐍 Sidat (Unagi)",
        "🧪 Bioflok & Air",
        "🦗 Database Pakan Alami"
    ])

    # === 1. LELE ===
    with stab_lele:
        st.subheader("😺 Budidaya Lele Intensif")
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.info("**Kunci Sukses:** Manajemen pakan dan grading (penyortiran) rutin.")
            jumlah_ikan = st.number_input("Jumlah Tebar (ekor)", value=1000, step=100)
            bobot_rata = st.number_input("Bobot Rata-rata per Ekor (gram)", value=50.0, step=1.0)
            fr_pct = st.number_input("Feeding Rate (%)", value=3.0, step=0.1, help="3-5% dari bobot biomasa")
            
        with col_l2:
            st.markdown("""
            **Rekomendasi Feeding Rate (FR):**
            *   Bibit (<10g): **5-7%** (Cepat tumbuh)
            *   Pembesaran (10-100g): **3-5%**
            *   Konsumsi (>100g): **2-3%** (Maintenance)
            """)
            
        biomasa_kg = (jumlah_ikan * bobot_rata) / 1000
        pakan_harian = biomasa_kg * (fr_pct / 100)
        
        st.success(f"📦 **Kebutuhan Pakan Harian:** {pakan_harian:.2f} kg (Biomasa: {biomasa_kg:.1f} kg)")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Pagi (08:00)", f"{pakan_harian*0.3:.2f} kg")
        c2.metric("Sore (16:00)", f"{pakan_harian*0.4:.2f} kg")
        c3.metric("Malam (21:00)", f"{pakan_harian*0.3:.2f} kg")
        
    # === 2. NILA ===
    with stab_nila:
        st.subheader("🐠 Budidaya Nila (Tilapia)")
        st.info("Nila adalah raja Bioflok. Tahan banting, omnivora, dan tumbuh cepat.")
        
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            st.markdown("#### 🌟 Sistem Monosex Jantan")
            st.markdown("""
            **Kenapa Monosex?**
            *   Nila jantan tumbuh **40% lebih cepat** dari betina.
            *   Mencegah perkimpoian liar di kolam yang membuat populasi over (ikan kerdil).
            *   **Teknik:** Gunakan hormon *17α-methyltestosterone* pada larva usia dini (Panduan khusus).
            """)
        with col_n2:
            st.markdown("#### 🌊 Parameter Kritis")
            st.markdown("""
            *   **Oksigen (DO):** Wajib > 3 mg/L (Gunakan Aerator/Kincir).
            *   **pH Air:** 6.5 - 8.5.
            *   **Suhu:** 25 - 30°C (Nila mogok makan di bawah 20°C).
            """)
            
    # === 3. GURAME ===
    with stab_gurame:
        st.subheader("🐡 Budidaya Gurame (Si Santai)")
        st.warning("⚠️ **Karakter:** Tumbuh lambat, rentan jamur, tapi harga jual tinggi & stabil.")
        
        tab_g1, tab_g2 = st.tabs(["🍃 Pakan & Nutrisi", "🏥 Kesehatan"])
        
        with tab_g1:
            st.markdown("#### Strategi Pakan Hemat (Herbivora)")
            st.markdown("""
            Gurame dewasa punya usus panjang yang mampu mencerna serat kasar. **Manfaatkan pakan alami!**
            1.  **Daun Sente (Lompong):** Pakan favorit, tinggi serat.
            2.  **Daun Pepaya:** Mengandung papain (bantu pencernaan) & antimikroba alami.
            3.  **Daun Mengkudu:** Meningkatkan kekebalan tubuh.
            """)
            
        with tab_g2:
            st.success("✅ **Probiotik Wajib:** Gunakan probiotik (Lactobacillus) pada pakan untuk mencegah kembung.")
            st.error("❌ **Musuh Utama:** Jamur Saprolegnia (Bercak Putih). Jaga suhu stabil, berikan garam krosok 500g/m³ saat hujan.")

    # === 4. UNAGI (SIDAT) ===
    with stab_unagi:
        st.subheader("🐍 Budidaya Sidat (Unagi) - Emas Berlendir")
        st.info("Komoditas ekspor premium (Jepang). Membutuhkan air jernih dan protein tinggi.")
        
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            st.markdown("#### 🍣 Pakan Pasta (Dough Feed)")
            st.markdown("""
            Sidat tidak suka pelet keras. Pakan harus berbentuk **Pasta**.
            *   **Resep:** Pelet powder (Tepung) + Air + Minyak Ikan + Vitamin Mix.
            *   **Protein Target:**
                *   Glass Eel: **50 - 55%**
                *   Elver: **45 - 50%**
                *   Market Size: **40 - 45%**
            """)
        with col_u2:
            st.markdown("#### 🏠 Habitat Gelap")
            st.markdown("""
            *   **Sifat:** Nokturnal & Fotofobik (Takut Cahaya).
            *   **Setting Kolam:** Wajib diberi naungan/shelter (paralon/gelap).
            *   **Salinitas:** Glass eel butuh adaptasi dari air payau ke tawar (Aklimatisasi perlahan).
            """)

    # === 5. BIOFLOK & AIR (Calculator preserved) ===
    with stab_bioflok:
        st.subheader("🧪 Kalkulator C/N Ratio (Bioflok)")
        st.markdown("**Target C/N Ratio ideal: 15:1 s/d 20:1**")

    # --- SHARED DATA: DATABASE PAKAN ALAMI ---
    # Defined here to be accessible by both "Database Tab" and "Calculator Tab"
    pakan_alami_db = [
        {"Nama": "Tepung Ikan (Lokal)", "Protein": 50.0, "Lemak": 8.0, "Fungsi": "Sumber Protein Utama", "Ket": "Mahal, hati-hati pemalsuan"},
        {"Nama": "Maggot BSF (Kering)", "Protein": 42.0, "Lemak": 20.0, "Fungsi": "Substitusi Tepung Ikan", "Ket": "High Fat, Antimikroba"},
        {"Nama": "Maggot BSF (Segar)", "Protein": 15.0, "Lemak": 6.0, "Fungsi": "Pakan Tambahan", "Ket": "Kadar air ~70% (Konversi 4:1)"},
        {"Nama": "Cacing Sutera (Tubifex)", "Protein": 57.0, "Lemak": 13.0, "Fungsi": "Pakan Larva (Benih)", "Ket": "Terbaik untuk burayak"},
        {"Nama": "Cacing Tanah (Lumbricus)", "Protein": 65.0, "Lemak": 9.0, "Fungsi": "Atraktan & Protein", "Ket": "Basis BK (Kering)"},
        {"Nama": "Azolla microphylla", "Protein": 25.0, "Lemak": 3.0, "Fungsi": "Sumber Protein Nabati", "Ket": "Hemat, mudah kultur"},
        {"Nama": "Lemna sp. (Duckweed)", "Protein": 30.0, "Lemak": 4.0, "Fungsi": "Pakan Nila/Gurame", "Ket": "Menyerap amonia air"},
        {"Nama": "Tepung Keong Mas", "Protein": 52.0, "Lemak": 6.0, "Fungsi": "Sumber Protein Hewani", "Ket": "Hama sawit jadi pakan"},
        {"Nama": "Bungkil Kedelai (SBM)", "Protein": 44.0, "Lemak": 1.5, "Fungsi": "Protein Nabati Utama", "Ket": "Asam amino lengkap"},
        {"Nama": "Dedak Padi (Halus)", "Protein": 12.0, "Lemak": 10.0, "Fungsi": "Sumber Energi (Karbo)", "Ket": "Perekat pelet"},
        {"Nama": "Tepung Jagung", "Protein": 9.0, "Lemak": 4.0, "Fungsi": "Sumber Energi", "Ket": "Karbohidrat tinggi"},
        {"Nama": "Tepung Tapioka", "Protein": 2.0, "Lemak": 0.5, "Fungsi": "Binder (Perekat)", "Ket": "Gunakan 5-10%"}
    ]
    # Helper for dropdown
    pakan_dict = {item["Nama"]: item["Protein"] for item in pakan_alami_db}

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        pakan_ikan_bf = st.number_input("Jumlah Pakan per Hari (kg)", value=10.0, key="bf_pakan")
        protein_pakan_bf = st.number_input("Kandungan Protein Pakan (%)", value=30.0, key="bf_prot")

    with col_f2:
        if st.button("Hitung Kebutuhan Molase"):
            n_content = pakan_ikan_bf * (protein_pakan_bf/100) * 0.16 
            tan_excreted = n_content * 0.5 
            target_cn = 15
            needed_c = tan_excreted * target_cn
            molase_needed = needed_c / 0.5 
            
            st.success(f"🍯 **Tambahkan Molase:** ± {molase_needed:.2f} kg / hari")
            st.caption(f"Basis: TAN terbuang {tan_excreted:.3f} kg. Dibutuhkan Carbon {needed_c:.3f} kg.")

    # === 6. DATABASE PAKAN ALAMI ===
    with stab_pakan:
        st.subheader("🦗 Database Nutrisi Pakan Alternatif (Jurnal Ilmiah)")
        st.info("Referensi nutrisi untuk formulasi pakan mandiri.")
        
        # Display DataFrame from Shared Data
        df_pakan = pd.DataFrame(pakan_alami_db)
        # Format displayed float columns for readability if needed, or just show as is
        st.dataframe(df_pakan)
        
        st.markdown("### 💡 Tips Formulasi:")
        st.markdown("""
        *   **Keseimbangan:** Jangan andalkan 1 jenis saja. Campur protein hewani (Ikan/Maggot) dan nabati (Kedelai/Azolla).
        *   **Lemak:** Hati-hati penggunaan Maggot Penuh > 30% karena lemak tinggi bisa bikin ikan berlemak (gajih).
        *   **Binder:** Gunakan Tepung Tapioka/Terigu (5-10%) agar pelet tidak mudah hancur di air.
        """)

# ===== TAB 4: RANSUM =====
# ===== TAB 4: RANSUM =====
with tab_feed:
    st.header("🧮 Kalkulator Formulasi Ransum Mandiri")
    st.markdown("Buat pakan ikan/ternak sendiri dengan formulasi multi-bahan untuk mencapai target protein.")
    
    # Init Session State untuk Pakan
    if "feed_ingredients" not in st.session_state:
        st.session_state.feed_ingredients = [
            {"nama": "Tepung Ikan", "pk": 50.0, "porsi": 30.0},
            {"nama": "Dedak Padi", "pk": 11.0, "porsi": 30.0},
            {"nama": "Bungkil Kedelai", "pk": 44.0, "porsi": 40.0}
        ]
        
    col_fc1, col_fc2 = st.columns([1, 1.5])
    
    with col_fc1:
        st.subheader("🛠️ Atur Komposisi")
        target_pk = st.number_input("Target Protein Kasar (%)", value=30.0, step=1.0)
        total_pakan = st.number_input("Rencana Total Pakan (kg)", value=100.0, step=10.0)
        
        st.divider()
        st.write("**Daftar Bahan:**")
        
        # Editor Bahan
        updated_ingredients = []
        total_porsi = 0.0
        
        # Use pakan_dict for dropdown options
        db_options = ["-- Pilih dari Database --"] + list(pakan_dict.keys())
        
        for i, item in enumerate(st.session_state.feed_ingredients):
            c_nama, c_pk, c_pct = st.columns([2, 1, 1])
            with c_nama:
                # Logic: Show text input if "Custom" or if existing value is not in DB (or manual edit)
                # But to keep it simple, we use a selectbox helper. 
                # Improving UI: Selectbox to pick ingredient, it auto-updates name & pk.
                
                # We need a key mechanism. 
                sel_key = f"sel_{i}"
                
                # Check if current item name matches DB, if so set index
                current_name = item['nama']
                try:
                    idx = db_options.index(current_name)
                except ValueError:
                    idx = 0 # Default to "-- Pilih --"
                
                selected_opt = st.selectbox(f"Bahan {i+1}", db_options, index=idx, key=sel_key, label_visibility="collapsed")
                
                # If selection changes from default/previous, update the item values
                final_name = current_name
                final_pk = item['pk']
                
                if selected_opt != "-- Pilih dari Database --":
                    final_name = selected_opt
                    final_pk = pakan_dict.get(selected_opt, 0.0)
                
                # Also allow manual override via text input? 
                # For simplicity in this iteration, allow the Selectbox to be the primary 'Chooser'.
                # But what if custom? -> "Custom" Not implemented yet in DB list. 
                # Let's add text input BELOW it for manual name override if needed? No, too cluttered.
                # Approach: Just use selectbox for now to solve user's "Source" question.
            
            with c_pk:
                # If we just selected from DB, the number input should default to that.
                # But st.number_input is stateful. We rely on the re-run cycle or 'value' param if key changed?
                # Simpler: Just display the PK input. If user selected something new, we might need to force update state.
                # In Streamlit, updating state mid-loop is tricky.
                # Better Pattern: Input is driven by state. State is updated by callback or logic before rendering.
                
                # Quick Fix: If the dropdown selection (selected_opt) is different from stored item['nama'], update it immediately?
                # Yes, logic above: final_pk = pakan_dict.get...
                
                pk = st.number_input(f"PK", value=float(final_pk), key=f"p_{i}", label_visibility="collapsed")
            with c_pct:
                porsi = st.number_input(f"%", value=item['porsi'], key=f"r_{i}", label_visibility="collapsed")
            
            updated_ingredients.append({"nama": final_name, "pk": pk, "porsi": porsi})
            total_porsi += porsi
            
        st.session_state.feed_ingredients = updated_ingredients
        
        # Tools Add/Remove
        b_add, b_reset = st.columns(2)
        if b_add.button("➕ Tambah Bahan"):
            st.session_state.feed_ingredients.append({"nama": "Bahan Baru", "pk": 0.0, "porsi": 0.0})
            st.rerun()
            
        if b_reset.button("🔄 Reset Default"):
            st.session_state.feed_ingredients = [
                {"nama": "Tepung Ikan", "pk": 50.0, "porsi": 30.0},
                {"nama": "Dedak Padi", "pk": 11.0, "porsi": 30.0},
                {"nama": "Bungkil Kedelai", "pk": 44.0, "porsi": 40.0}
            ]
            st.rerun()
            
    with col_fc2:
        st.subheader("📊 Analisis Nutrisi")
        
        # Real-time Calculation
        calc_pk = 0.0
        details = []
        
        for item in st.session_state.feed_ingredients:
            # Contribution PK = (Porsi / Total Porsi) * PK Bahan
            if total_porsi > 0:
                real_pct = (item['porsi'] / total_porsi) * 100
                contrib_pk = (real_pct / 100) * item['pk']
                real_kg = (real_pct / 100) * total_pakan
                
                calc_pk += contrib_pk
                details.append({
                    "Bahan": item['nama'],
                    "PK Bahan (%)": item['pk'],
                    "Proporsi (%)": f"{real_pct:.1f}%",
                    "Berat (kg)": f"{real_kg:.2f}",
                    "Sumbangan PK (%)": f"{contrib_pk:.2f}"
                })
        
        # Display Gauge
        delta_pk = calc_pk - target_pk
        st.metric("Total Protein Kasar (Calculated)", f"{calc_pk:.2f} %", f"{delta_pk:.2f} % dari Target")
        
        # Logic Check
        if abs(total_porsi - 100.0) > 0.1:
            st.error(f"⚠️ Total Proporsi belum 100% (Saat ini: {total_porsi:.1f}%). Harap sesuaikan porsi bahan.")
        else:
            if calc_pk >= target_pk - 1.0 and calc_pk <= target_pk + 1.0:
                st.success("✅ **Formulasi Ideal!** Sesuai dengan target protein.")
            elif calc_pk < target_pk:
                st.warning("⚠️ **Protein Kurang.** Tambahkan porsi bahan protein tinggi (Tepung Ikan/Kedelai).")
            else:
                st.info("ℹ️ **Protein Tinggi.** Bisa dikurangi untuk hemat biaya.")
                
            st.table(pd.DataFrame(details))
            
            # Recommendation Chart
            fig_feed = px.pie(
                names=[d['Bahan'] for d in details],
                values=[float(d['Berat (kg)']) for d in details],
                title=f"Komposisi untuk {total_pakan} kg Pakan"
            )
            st.plotly_chart(fig_feed, use_container_width=True)
            
            st.info("""
            **Tips Formulasi:**
            *   Gunakan **Metode Trial & Error** dengan mengubah angka 'Porsi%' di sebelah kiri sampai Total Proporsi 100% dan Target Protein tercapai.
            *   PK = Protein Kasar (Crude Protein).
            """)

# ===== TAB 5: DOKTER HEWAN AI =====
with tab_vet:
    st.header("🩺 Asisten Kesehatan Hewan AI")
    st.markdown("Diskusikan gejala penyakit pada ternak atau ikan Anda.")
    
    # Initialize chat history
    if "vet_messages" not in st.session_state:
        st.session_state.vet_messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.vet_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Contoh: Sapi saya keluar air liur berbusa dan kuku luka..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.vet_messages.append({"role": "user", "content": prompt})

        # Placeholder response Logic
        # In real app, connect to LLM API here.
        # For now, we use a simple static response or "simulated" analysis.
        
        response = f"""
        **Analisis Sementara (Simulasi AI):**
        
        Berdasarkan keluhan "{prompt}", ini membutuhkan diagnosa lebih lanjut.
        
        Namun, jika gejala melibatkan mulut berbusa dan luka kuku pada ruminansia, **Waspadai PMK (Penyakit Mulut dan Kuku)**.
        
        **Saran Awal:**
        1. Pisahkan ternak sakit (Karantina).
        2. Berikan cairan elektrolit/vitamin support.
        3. Segera hubungi Dokter Hewan setempat untuk konfirmasi.
        
        *Catatan: Sistem ini masih dalam pengembangan (Dummy Response).*
        """
        
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.vet_messages.append({"role": "assistant", "content": response})
