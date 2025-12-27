import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page config
# from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Peternakan & Perikanan - AgriSensa",
    page_icon="🐄",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






# Import health monitoring service
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.livestock_health_service import (
    BCS_STANDARDS, DISEASE_DATABASE, VACCINATION_SCHEDULES, DEWORMING_PROTOCOLS,
    calculate_calving_interval, calculate_conception_rate, calculate_service_per_conception,
    analyze_milk_production, calculate_scc_status, diagnose_by_symptoms, get_bcs_recommendation
)

# Header
st.title("🐄 Manajemen Peternakan & Perikanan")
st.markdown("**Solusi Presisi untuk Ruminansia, Unggas, dan Budidaya Perikanan**")
st.info("💡 Modul ini menyediakan alat bantu hitung teknis (Ransum, FCR, Bioflok) dan asisten kesehatan hewan.")

# Main tabs - Added Health Monitoring tab
tab_ruminant, tab_poultry, tab_fish, tab_feed, tab_health, tab_vet = st.tabs([
    "🐄 Ruminansia (Sapi/Kambing)",
    "🐓 Unggas (Ayam/Bebek)",
    "🐟 Perikanan (Bioflok/RAS)",
    "🧮 Kalkulator Ransum",
    "🩺 Health Monitoring",
    "🤖 Dokter Hewan AI"
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

# ===== TAB 5: HEALTH MONITORING (NEW) =====
with tab_health:
    st.header("🩺 Sistem Monitoring Kesehatan Ternak")
    st.markdown("**Precision Livestock Health Management** - Scientifically Grounded Tools")
    
    # Sub-tabs for different health aspects
    health_tab_bcs, health_tab_disease, health_tab_vacc, health_tab_repro, health_tab_milk = st.tabs([
        "📊 Body Condition Score",
        "🦠 Disease Diagnosis",
        "💉 Vaccination & Deworming",
        "🐄 Reproductive Performance",
        "🥛 Milk Recording"
    ])
    
    # ========== SUB-TAB 1: BCS CALCULATOR ==========
    with health_tab_bcs:
        st.subheader("📊 Body Condition Score (BCS) Calculator")
        st.markdown("**Evaluasi kondisi tubuh ternak untuk optimasi produksi dan reproduksi**")
        
        col_bcs1, col_bcs2 = st.columns([1, 1])
        
        with col_bcs1:
            st.markdown("### 🐄 Input Data")
            
            bcs_species = st.selectbox(
                "Jenis Ternak",
                ["Sapi Potong", "Sapi Perah", "Kambing/Domba"],
                key="bcs_species"
            )
            
            if bcs_species == "Sapi Perah":
                bcs_score = st.slider("BCS Score (1-9)", 1.0, 9.0, 5.0, 0.5, key="bcs_score_dairy")
                production_stage = st.selectbox(
                    "Tahap Produksi",
                    ["Laktasi Awal (0-100 hari)", "Laktasi Tengah (100-200 hari)", 
                     "Laktasi Akhir (>200 hari)", "Kering Kandang"],
                    key="prod_stage"
                )
            else:
                bcs_score = st.slider("BCS Score (1-5)", 1.0, 5.0, 3.0, 0.5, key="bcs_score_beef")
                production_stage = st.selectbox(
                    "Status",
                    ["Pertumbuhan", "Bunting", "Laktasi", "Penggemukan"],
                    key="prod_stage_beef"
                )
            
            if st.button("🔍 Analisis BCS", type="primary", use_container_width=True):
                result = get_bcs_recommendation(bcs_species, bcs_score, production_stage)
                
                st.session_state['bcs_result'] = result
        
        with col_bcs2:
            st.markdown("### 📋 Hasil Analisis")
            
            if 'bcs_result' in st.session_state:
                result = st.session_state['bcs_result']
                
                # Display BCS category with color coding
                bcs_cat = result['bcs_category']
                if bcs_cat in [1, 2]:
                    color = "red"
                    icon = "🔴"
                elif bcs_cat in [3, 4, 5] if bcs_species != "Sapi Perah" else bcs_cat in [3, 4, 5, 6]:
                    color = "green"
                    icon = "🟢"
                else:
                    color = "orange"
                    icon = "🟡"
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                            padding: 20px; border-radius: 15px; border-left: 6px solid {color}; margin-bottom: 20px;">
                    <h3 style="margin:0; color: {color};">{icon} {result['description']}</h3>
                    <p style="margin: 10px 0 0 0; font-size: 0.9em; color: #495057;">
                        <strong>BCS:</strong> {result['bcs_score']} | <strong>Kategori:</strong> {result['bcs_category']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                st.info(f"**Visual Guide:** {result['visual_guide']}")
                
                st.success(f"**✅ Rekomendasi:** {result['recommendation']}")
                
                if result.get('risk_level'):
                    st.warning(f"**⚠️ Risk Level:** {result['risk_level']}")
            else:
                st.info("Masukkan data BCS dan klik tombol Analisis untuk melihat hasil.")
        
        # BCS Reference Guide
        st.divider()
        st.markdown("### 📚 Panduan Referensi BCS")
        
        with st.expander("📖 Lihat Standar BCS Lengkap"):
            selected_species = st.selectbox("Pilih Jenis Ternak", list(BCS_STANDARDS.keys()), key="ref_species")
            
            ref_data = []
            for score, data in BCS_STANDARDS[selected_species].items():
                ref_data.append({
                    "Score": score,
                    "Deskripsi": data.get("description", ""),
                    "Rekomendasi": data.get("recommendation", "")
                })
            
            ref_df = pd.DataFrame(ref_data)
            st.dataframe(ref_df, use_container_width=True, hide_index=True)
    
    # ========== SUB-TAB 2: DISEASE DIAGNOSIS ==========
    with health_tab_disease:
        st.subheader("🦠 Disease Expert System")
        st.markdown("**Sistem diagnosis berbasis gejala klinis**")
        
        col_diag1, col_diag2 = st.columns([1, 1])
        
        with col_diag1:
            st.markdown("### 🔍 Input Gejala")
            
            diag_species = st.selectbox(
                "Jenis Ternak",
                ["Sapi", "Kambing", "Domba"],
                key="diag_species"
            )
            
            # Collect all possible symptoms from database
            all_symptoms = set()
            for disease_data in DISEASE_DATABASE.values():
                if diag_species in disease_data.get("species", []) or "Sapi" in disease_data.get("species", []):
                    all_symptoms.update(disease_data["symptoms"])
            
            selected_symptoms = st.multiselect(
                "Pilih Gejala yang Terlihat",
                sorted(list(all_symptoms)),
                key="symptoms"
            )
            
            if st.button("🔬 Diagnosa", type="primary", use_container_width=True):
                if selected_symptoms:
                    results = diagnose_by_symptoms(selected_symptoms, diag_species)
                    st.session_state['diagnosis_results'] = results
                else:
                    st.warning("Pilih minimal 1 gejala untuk diagnosa")
        
        with col_diag2:
            st.markdown("### 📊 Hasil Diagnosis")
            
            if 'diagnosis_results' in st.session_state and st.session_state['diagnosis_results']:
                results = st.session_state['diagnosis_results']
                
                for i, result in enumerate(results[:3]):  # Show top 3 matches
                    match_pct = result['match_percentage']
                    
                    if match_pct >= 70:
                        color = "#dc3545"  # Red - high probability
                    elif match_pct >= 50:
                        color = "#ffc107"  # Yellow - medium
                    else:
                        color = "#6c757d"  # Gray - low
                    
                    st.markdown(f"""
                    <div style="background: white; padding: 15px; border-radius: 10px; 
                                border-left: 5px solid {color}; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h4 style="margin:0; color: {color};">#{i+1} {result['disease']} ({match_pct}% match)</h4>
                        <p style="margin: 5px 0; font-size: 0.85em;">
                            <strong>Kategori:</strong> {result['category']} | 
                            <strong>Severity:</strong> {result['severity']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"📋 Detail {result['disease']}"):
                        disease_data = result['data']
                        
                        st.markdown("**🔴 Gejala Lengkap:**")
                        for symptom in disease_data['symptoms']:
                            st.markdown(f"- {symptom}")
                        
                        st.markdown("**🧬 Penyebab:**")
                        for cause in disease_data['causes']:
                            st.markdown(f"- {cause}")
                        
                        st.markdown("**💊 Pengobatan:**")
                        for treatment in disease_data['treatment']:
                            st.markdown(f"- {treatment}")
                        
                        st.markdown("**🛡️ Pencegahan:**")
                        for prevention in disease_data['prevention']:
                            st.markdown(f"- {prevention}")
                        
                        st.error(f"**⚠️ Dampak Ekonomi:** {disease_data['economic_impact']}")
            else:
                st.info("Pilih gejala dan klik Diagnosa untuk melihat kemungkinan penyakit.")
        
        # Disease Database Reference
        st.divider()
        st.markdown("### 📚 Database Penyakit")
        
        with st.expander("📖 Lihat Semua Penyakit"):
            disease_list = []
            for name, data in DISEASE_DATABASE.items():
                disease_list.append({
                    "Penyakit": name,
                    "Kategori": data['category'],
                    "Spesies": ", ".join(data['species']),
                    "Severity": data['severity']
                })
            
            disease_df = pd.DataFrame(disease_list)
            st.dataframe(disease_df, use_container_width=True, hide_index=True)
    
    # ========== SUB-TAB 3: VACCINATION & DEWORMING ==========
    with health_tab_vacc:
        st.subheader("💉 Vaccination & Deworming Tracker")
        st.markdown("**Jadwal vaksinasi dan deworming berdasarkan standar nasional**")
        
        col_vacc1, col_vacc2 = st.columns([1, 1])
        
        with col_vacc1:
            st.markdown("### 📅 Jadwal Vaksinasi")
            
            vacc_species = st.selectbox(
                "Jenis Ternak",
                list(VACCINATION_SCHEDULES.keys()),
                key="vacc_species"
            )
            
            animal_age_months = st.number_input(
                "Umur Ternak (bulan)",
                min_value=0,
                max_value=60,
                value=6,
                key="animal_age"
            )
            
            st.markdown("#### 🗓️ Jadwal Vaksinasi Rekomendasi")
            
            schedule = VACCINATION_SCHEDULES[vacc_species]
            upcoming_vaccines = []
            
            for vacc in schedule:
                age_req = vacc['age_months']
                if isinstance(age_req, int):
                    if age_req >= animal_age_months:
                        upcoming_vaccines.append(vacc)
            
            if upcoming_vaccines:
                for vacc in upcoming_vaccines[:5]:  # Show next 5 vaccines
                    st.success(f"""
                    **{vacc['vaccine']}**
                    - Umur: {vacc['age_months']} bulan
                    - Dosis: {vacc['dose']}
                    - Booster: {vacc['frequency']}
                    """)
            else:
                st.info("Semua vaksinasi dasar sudah seharusnya dilakukan. Lanjutkan dengan booster rutin.")
            
            # Full schedule table
            with st.expander("📋 Lihat Jadwal Lengkap"):
                vacc_data = []
                for vacc in schedule:
                    vacc_data.append({
                        "Umur (bulan)": vacc['age_months'],
                        "Vaksin": vacc['vaccine'],
                        "Dosis": vacc['dose'],
                        "Frekuensi": vacc['frequency']
                    })
                
                vacc_df = pd.DataFrame(vacc_data)
                st.dataframe(vacc_df, use_container_width=True, hide_index=True)
        
        with col_vacc2:
            st.markdown("### 🐛 Protokol Deworming")
            
            deworm_species = st.selectbox(
                "Jenis Ternak",
                list(DEWORMING_PROTOCOLS.keys()),
                key="deworm_species"
            )
            
            protocol = DEWORMING_PROTOCOLS[deworm_species]
            
            st.info(f"**Frekuensi:** {protocol['frequency']}")
            
            st.markdown("#### 💊 Produk Rekomendasi")
            for product in protocol['products']:
                st.success(f"""
                **{product['name']}**
                - Dosis: {product['dose']}
                - Rute: {product['route']}
                """)
            
            st.markdown("#### ⏰ Waktu Kritis Deworming")
            for time in protocol['critical_times']:
                st.warning(f"🔔 {time}")
    
    # ========== SUB-TAB 4: REPRODUCTIVE PERFORMANCE ==========
    with health_tab_repro:
        st.subheader("🐄 Reproductive Performance Analytics")
        st.markdown("**Monitor dan optimasi performa reproduksi ternak**")
        
        repro_tab_ci, repro_tab_cr, repro_tab_sc = st.tabs([
            "📅 Calving Interval",
            "🎯 Conception Rate",
            "📊 Service/Conception"
        ])
        
        with repro_tab_ci:
            st.markdown("### 📅 Calving Interval Calculator")
            st.caption("Target optimal: 12-13 bulan (365-395 hari)")
            
            num_calvings = st.number_input("Jumlah Data Calving", min_value=2, max_value=10, value=3, key="num_calv")
            
            calving_dates = []
            for i in range(num_calvings):
                date = st.date_input(f"Tanggal Calving #{i+1}", key=f"calv_date_{i}")
                calving_dates.append(date.strftime("%Y-%m-%d"))
            
            if st.button("📊 Hitung Calving Interval", key="calc_ci"):
                result = calculate_calving_interval(calving_dates)
                
                if 'error' not in result:
                    col_ci1, col_ci2, col_ci3 = st.columns(3)
                    
                    with col_ci1:
                        st.metric("Rata-rata Interval", f"{result['average_interval_days']:.0f} hari")
                    
                    with col_ci2:
                        st.metric("Dalam Bulan", f"{result['average_interval_months']:.1f} bulan")
                    
                    with col_ci3:
                        status_color = "🟢" if result['status'] == "Optimal" else "🔴"
                        st.metric("Status", f"{status_color} {result['status']}")
                    
                    st.info(f"**💡 Rekomendasi:** {result['recommendation']}")
                    
                    # Visualize intervals
                    if len(result['intervals']) > 1:
                        fig_ci = px.line(
                            x=list(range(1, len(result['intervals'])+1)),
                            y=result['intervals'],
                            markers=True,
                            title="Trend Calving Interval",
                            labels={"x": "Interval ke-", "y": "Hari"}
                        )
                        fig_ci.add_hline(y=365, line_dash="dash", line_color="green", annotation_text="Target Min (365)")
                        fig_ci.add_hline(y=395, line_dash="dash", line_color="red", annotation_text="Target Max (395)")
                        st.plotly_chart(fig_ci, use_container_width=True)
                else:
                    st.error(result['error'])
        
        with repro_tab_cr:
            st.markdown("### 🎯 Conception Rate Calculator")
            st.caption("Target: >50% untuk first service, >70% overall")
            
            col_cr1, col_cr2 = st.columns(2)
            
            with col_cr1:
                cr_services = st.number_input("Jumlah Service/IB", min_value=1, value=20, key="cr_serv")
            
            with col_cr2:
                cr_pregnancies = st.number_input("Jumlah Bunting", min_value=0, value=12, key="cr_preg")
            
            if st.button("📊 Hitung Conception Rate", key="calc_cr"):
                result = calculate_conception_rate(cr_services, cr_pregnancies)
                
                if 'error' not in result:
                    col_cr_r1, col_cr_r2 = st.columns(2)
                    
                    with col_cr_r1:
                        cr_value = result['conception_rate']
                        status_color = "green" if cr_value >= 50 else ("orange" if cr_value >= 40 else "red")
                        
                        import plotly.graph_objects as go
                        fig_cr = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=cr_value,
                            title={'text': "Conception Rate (%)"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': status_color},
                                'steps': [
                                    {'range': [0, 40], 'color': "#fee2e2"},
                                    {'range': [40, 50], 'color': "#fef3c7"},
                                    {'range': [50, 100], 'color': "#d1fae5"}
                                ],
                                'threshold': {'line': {'color': "green", 'width': 4}, 'thickness': 0.75, 'value': 50}
                            }
                        ))
                        fig_cr.update_layout(height=250)
                        st.plotly_chart(fig_cr, use_container_width=True)
                    
                    with col_cr_r2:
                        st.metric("Conception Rate", f"{cr_value:.1f}%")
                        st.metric("Status", f"{'🟢' if result['status'] == 'Baik' else '🔴'} {result['status']}")
                        st.info(f"**💡 Rekomendasi:** {result['recommendation']}")
                else:
                    st.error(result['error'])
        
        with repro_tab_sc:
            st.markdown("### 📊 Service per Conception (S/C)")
            st.caption("Target: <1.8 (ideal <1.5)")
            
            col_sc1, col_sc2 = st.columns(2)
            
            with col_sc1:
                sc_total_services = st.number_input("Total Service", min_value=1, value=30, key="sc_serv")
            
            with col_sc2:
                sc_total_preg = st.number_input("Total Kebuntingan", min_value=1, value=18, key="sc_preg")
            
            if st.button("📊 Hitung S/C", key="calc_sc"):
                result = calculate_service_per_conception(sc_total_services, sc_total_preg)
                
                if 'error' not in result:
                    sc_value = result['service_per_conception']
                    
                    col_sc_r1, col_sc_r2 = st.columns(2)
                    
                    with col_sc_r1:
                        st.metric("Service/Conception", f"{sc_value:.2f}")
                        st.metric("Status", f"{'🟢' if result['status'] == 'Baik' else '🔴'} {result['status']}")
                    
                    with col_sc_r2:
                        st.info(f"**💡 Rekomendasi:** {result['recommendation']}")
                        
                        # Efficiency indicator
                        efficiency = (1 / sc_value) * 100
                        st.success(f"**Efisiensi Reproduksi:** {efficiency:.1f}%")
                else:
                    st.error(result['error'])
    
    # ========== SUB-TAB 5: MILK RECORDING ==========
    with health_tab_milk:
        st.subheader("🥛 Milk Recording System")
        st.markdown("**Sistem pencatatan dan analisis produksi susu**")
        
        milk_tab_prod, milk_tab_quality = st.tabs([
            "📊 Production Analysis",
            "🔬 Quality Assessment"
        ])
        
        with milk_tab_prod:
            st.markdown("### 📊 Analisis Produksi Susu")
            
            st.info("💡 Input data produksi harian untuk analisis trend dan performa laktasi")
            
            # Simple data input
            num_days = st.number_input("Jumlah Hari Data", min_value=1, max_value=30, value=7, key="milk_days")
            
            milk_records = []
            
            with st.form("milk_input_form"):
                st.markdown("#### 📝 Input Produksi Harian")
                
                for i in range(num_days):
                    col_m1, col_m2, col_m3 = st.columns(3)
                    
                    with col_m1:
                        date = st.date_input(f"Tanggal #{i+1}", key=f"milk_date_{i}")
                    
                    with col_m2:
                        morning = st.number_input(f"Pagi (L)", min_value=0.0, value=10.0, step=0.5, key=f"milk_morn_{i}")
                    
                    with col_m3:
                        evening = st.number_input(f"Sore (L)", min_value=0.0, value=8.0, step=0.5, key=f"milk_eve_{i}")
                    
                    milk_records.append({
                        "date": date.strftime("%Y-%m-%d"),
                        "morning": morning,
                        "evening": evening
                    })
                
                submit_milk = st.form_submit_button("📊 Analisis Produksi", type="primary", use_container_width=True)
            
            if submit_milk and milk_records:
                result = analyze_milk_production(milk_records)
                
                if 'error' not in result:
                    # KPI Cards
                    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
                    
                    with col_kpi1:
                        st.metric("Rata-rata Harian", f"{result['average_daily_production']:.2f} L")
                    
                    with col_kpi2:
                        st.metric("Produksi Puncak", f"{result['peak_production']:.2f} L")
                    
                    with col_kpi3:
                        st.metric("Produksi Terkini", f"{result['current_production']:.2f} L")
                    
                    with col_kpi4:
                        trend_icon = "📈" if result['trend'] == "Naik" else ("📉" if result['trend'] == "Turun" else "➡️")
                        st.metric("Trend", f"{trend_icon} {result['trend']}")
                    
                    # Production chart
                    df_milk = pd.DataFrame(milk_records)
                    df_milk['total'] = df_milk['morning'] + df_milk['evening']
                    
                    fig_milk = px.line(
                        df_milk,
                        x='date',
                        y='total',
                        markers=True,
                        title="Trend Produksi Susu Harian",
                        labels={"date": "Tanggal", "total": "Produksi (L)"}
                    )
                    fig_milk.add_hline(
                        y=result['average_daily_production'],
                        line_dash="dash",
                        line_color="green",
                        annotation_text=f"Rata-rata: {result['average_daily_production']:.2f}L"
                    )
                    st.plotly_chart(fig_milk, use_container_width=True)
                    
                    st.success(f"**Total Produksi {result['total_days']} Hari:** {result['total_production']:.2f} L")
                else:
                    st.error(result['error'])
        
        with milk_tab_quality:
            st.markdown("### 🔬 Milk Quality Assessment")
            
            col_qual1, col_qual2 = st.columns(2)
            
            with col_qual1:
                st.markdown("#### 🧪 Somatic Cell Count (SCC)")
                
                scc_value = st.number_input(
                    "SCC (cells/ml)",
                    min_value=0,
                    max_value=2000000,
                    value=150000,
                    step=10000,
                    key="scc_input"
                )
                
                if st.button("🔬 Evaluasi SCC", key="eval_scc"):
                    result = calculate_scc_status(scc_value)
                    
                    # Color coding
                    if result['risk_level'] == "Rendah":
                        color = "green"
                        icon = "🟢"
                    elif result['risk_level'] == "Sedang":
                        color = "orange"
                        icon = "🟡"
                    else:
                        color = "red"
                        icon = "🔴"
                    
                    st.markdown(f"""
                    <div style="background: white; padding: 20px; border-radius: 15px; 
                                border-left: 6px solid {color}; margin: 20px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <h3 style="margin:0; color: {color};">{icon} {result['status']}</h3>
                        <p style="margin: 10px 0 0 0;">
                            <strong>SCC:</strong> {result['scc_value']:,} cells/ml<br>
                            <strong>Risk Level:</strong> {result['risk_level']}<br>
                            <strong>Kualitas:</strong> {result['quality_impact']}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.warning(f"**⚠️ Tindakan:** {result['action']}")
            
            with col_qual2:
                st.markdown("#### 📊 Milk Composition")
                
                fat_pct = st.slider("Fat %", 0.0, 10.0, 3.5, 0.1, key="fat")
                protein_pct = st.slider("Protein %", 0.0, 6.0, 3.2, 0.1, key="protein")
                snf_pct = st.slider("SNF (Solid Non-Fat) %", 0.0, 12.0, 8.5, 0.1, key="snf")
                
                # Quality assessment
                quality_score = 0
                issues = []
                
                if 3.0 <= fat_pct <= 4.5:
                    quality_score += 33
                else:
                    issues.append(f"Fat {'rendah' if fat_pct < 3.0 else 'tinggi'}")
                
                if 3.0 <= protein_pct <= 3.8:
                    quality_score += 33
                else:
                    issues.append(f"Protein {'rendah' if protein_pct < 3.0 else 'tinggi'}")
                
                if 8.0 <= snf_pct <= 9.0:
                    quality_score += 34
                else:
                    issues.append(f"SNF {'rendah' if snf_pct < 8.0 else 'tinggi'}")
                
                st.metric("Quality Score", f"{quality_score}/100")
                
                if quality_score >= 90:
                    st.success("🟢 Kualitas Susu Excellent")
                elif quality_score >= 70:
                    st.info("🟡 Kualitas Susu Baik")
                else:
                    st.warning(f"🔴 Kualitas Susu Perlu Perbaikan: {', '.join(issues)}")
                
                # Composition chart
                fig_comp = px.pie(
                    names=['Fat', 'Protein', 'SNF', 'Water'],
                    values=[fat_pct, protein_pct, snf_pct, 100 - (fat_pct + protein_pct + snf_pct)],
                    title="Komposisi Susu"
                )
                st.plotly_chart(fig_comp, use_container_width=True)

# ===== TAB 6: DOKTER HEWAN AI =====
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
