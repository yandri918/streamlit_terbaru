"""
 Monitoring & Logbook - Farm Digital Journal
Track daily activities, expenses, and plant growth progress
"""

import streamlit as st
import pandas as pd
import altair as alt
from datetime import datetime
import random

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
    from design_system import apply_design_system, icon, COLORS

st.set_page_config(page_title="Monitoring & Logbook", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('book', size='lg')} Monitoring Logbook</h1>", unsafe_allow_html=True)
st.markdown("**Catatan digital aktivitas kebun, keuangan, dan progres pertumbuhan tanaman**")
st.markdown("---")

# Initialize session state for data persistence (mock database)
if 'logbook_data' not in st.session_state:
    st.session_state.logbook_data = []

if 'growth_data' not in st.session_state:
    # Dummy initial data for visualization
    st.session_state.growth_data = [
        {"umur": 7, "tinggi": 15, "anakan": 1, "daun": 2},
        {"umur": 14, "tinggi": 25, "anakan": 3, "daun": 4},
        {"umur": 21, "tinggi": 35, "anakan": 8, "daun": 6},
    ]

tab1, tab2, tab3 = st.tabs([" Catatan Harian", " Grafik Pertumbuhan", " Rekap Keuangan"])

with tab1:
    st.header("Input Jurnal Harian")
    
    with st.form("entry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            tanggal = st.date_input("Tanggal", datetime.now())
            kategori = st.selectbox("Kategori Kegiatan", [
                "Pemupukan", 
                "Penyemprotan Hama/Penyakit", 
                "Pengairan", 
                "Penyiangan Gulma",
                "Panen",
                "Lain-lain"
            ])
            deskripsi = st.text_area("Deskripsi Kegiatan", placeholder="Contoh: Aplikasi Urea 50kg dan Ponska 100kg")
        
        with col2:
            biaya = st.number_input("Biaya (Rp)", min_value=0, step=1000)
            foto = st.file_uploader("Upload Foto Dokumentasi", type=['jpg', 'png'])
            catatan_khusus = st.text_input("Catatan Tambahan", placeholder="Cuaca, kondisi tanaman, dll")
            
        submit = st.form_submit_button(" Simpan Catatan")
        
        if submit:
            entry = {
                "Tanggal": tanggal,
                "Kategori": kategori,
                "Deskripsi": deskripsi,
                "Biaya": biaya,
                "Catatan": catatan_khusus
            }
            st.session_state.logbook_data.append(entry)
            st.success(" Catatan berhasil disimpan!")

    st.markdown("---")
    st.subheader(" Riwayat Aktivitas")
    
    if st.session_state.logbook_data:
        df_log = pd.DataFrame(st.session_state.logbook_data)
        # Sort by date descending
        df_log['Tanggal'] = pd.to_datetime(df_log['Tanggal'])
        df_log = df_log.sort_values(by='Tanggal', ascending=False)
        
        st.dataframe(
            df_log, 
            column_config={
                "Biaya": st.column_config.NumberColumn(format="Rp %d")
            },
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("Belum ada catatan aktivitas. Silakan input kegiatan pertama Anda.")

with tab2:
    st.header(" Monitoring Pertumbuhan")
    
    with st.form("growth_form"):
        col_g1, col_g2, col_g3, col_g4 = st.columns(4)
        with col_g1:
            g_umur = st.number_input("Umur Tanaman (HST)", min_value=0, step=1)
        with col_g2:
            g_tinggi = st.number_input("Tinggi Tanaman (cm)", min_value=0.0, step=0.1)
        with col_g3:
            g_anakan = st.number_input("Jumlah Anakan", min_value=0, step=1)
        with col_g4:
            g_daun = st.number_input("Warna Daun (Skala BWD 2-5)", min_value=2.0, max_value=5.0, step=0.1)
            
        submit_growth = st.form_submit_button(" Tambah Data Pertumbuhan")
        
        if submit_growth:
            st.session_state.growth_data.append({
                "umur": g_umur,
                "tinggi": g_tinggi,
                "anakan": g_anakan,
                "daun": g_daun
            })
            st.success("Data pertumbuhan ditambahkan!")

    st.markdown("---")
    
    if st.session_state.growth_data:
        df_growth = pd.DataFrame(st.session_state.growth_data).sort_values('umur')
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Chart Tinggi Tanaman
            chart_tinggi = alt.Chart(df_growth).mark_line(point=True, color='#4CAF50').encode(
                x=alt.X('umur', title='Umur Tanaman (HST)'),
                y=alt.Y('tinggi', title='Tinggi Tanaman (cm)'),
                tooltip=['umur', 'tinggi']
            ).properties(title="Grafik Tinggi Tanaman")
            st.altair_chart(chart_tinggi, use_container_width=True)
            
        with col_chart2:
            # Chart Jumlah Anakan
            chart_anakan = alt.Chart(df_growth).mark_line(point=True, color='#2196F3').encode(
                x=alt.X('umur', title='Umur Tanaman (HST)'),
                y=alt.Y('anakan', title='Jumlah Anakan'),
                tooltip=['umur', 'anakan']
            ).properties(title="Grafik Perkembangan Anakan")
            st.altair_chart(chart_anakan, use_container_width=True)
            
        st.subheader("Data Tabular")
        st.dataframe(df_growth, use_container_width=True, hide_index=True)

with tab3:
    st.header(" Rekapitulasi Keuangan")
    
    if st.session_state.logbook_data:
        df_finance = pd.DataFrame(st.session_state.logbook_data)
        
        total_biaya = df_finance['Biaya'].sum()
        
        # Metrics
        col_fin1, col_fin2, col_fin3 = st.columns(3)
        col_fin1.metric("Total Pengeluaran", f"Rp {total_biaya:,.0f}")
        col_fin2.metric("Jumlah Transaksi", len(df_finance))
        col_fin3.metric("Rata-rata per Kegiatan", f"Rp {total_biaya/len(df_finance):,.0f}")
        
        st.markdown("---")
        
        # Cost breakdown by category
        cost_by_cat = df_finance.groupby('Kategori')['Biaya'].sum().reset_index()
        
        chart_pie = alt.Chart(cost_by_cat).mark_arc(innerRadius=50).encode(
            theta=alt.Theta(field="Biaya", type="quantitative"),
            color=alt.Color(field="Kategori", type="nominal"),
            tooltip=['Kategori', alt.Tooltip('Biaya', format=',.0f')]
        ).properties(title="Proporsi Biaya per Kategori")
        
        st.altair_chart(chart_pie, use_container_width=True)
        
    else:
        st.warning("Belum ada data keuangan. Masukkan data di tab Catatan Harian.")

st.markdown("---")
st.caption(" **Tips:** Lakukan pencatatan rutin setiap hari atau minimal seminggu sekali untuk hasil monitoring yang akurat.")
