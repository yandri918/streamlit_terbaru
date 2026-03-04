import streamlit as st
import datetime
import pandas as pd
import plotly.express as px
import textwrap

# Page Config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="AgriSensa Strategic Dossier",
    page_icon="📄",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================



# --- SESSION STATE INITIALIZATION ---
if 'swot_data' not in st.session_state:
    st.session_state['swot_data'] = {
        "Strengths": "Teknologi presisi AI, Akses pasar modern, Traceability Blockchain, dan Praktik ESG kuat.",
        "Weaknesses": "Ketergantungan cuaca ekstrem, Biaya setup awal infrastruktur (IoT/Greenhouse) tinggi.",
        "Opportunities": "Permintaan tinggi atas sayuran/buah premium, Ekspor agrobisnis, Kesadaran pola makan sehat.",
        "Threats": "Fluktuasi harga sarana produksi (pupuk global), Disrupsi rantai pasok, Mutasi serangan hama."
    }

if 'timeline_data' not in st.session_state:
    st.session_state['timeline_data'] = [
        {"Fase": "Persiapan Lahan & Konstruksi", "Durasi": "Bulan 1-2"},
        {"Fase": "Instalasi IoT & Smart Irrigation", "Durasi": "Bulan 3"},
        {"Fase": "Trial Tanam & QC Setup", "Durasi": "Bulan 4"},
        {"Fase": "Operasional Penuh & Harvest", "Durasi": "Bulan 5+"}
    ]

# --- SIDEBAR: GLOBAL CONFIG ---
with st.sidebar:
    st.header("Konfigurasi Proyek")
    proj_name = st.text_input("Nama Proyek", "Pusat Agribisnis Premium Terpadu")
    company_name = st.text_input("Instansi / Perusahaan", "PT. AgriSensa Solusi Madani")
    owner_name = st.text_input("Penanggung Jawab / CEO", "Bpk. Andriyanto")
    report_date = st.date_input("Tanggal Terbit", datetime.date.today())
    
    st.divider()
    st.subheader("Sumber Data")
    source_rab = st.radio("Sektor Finansial (RAB)", ["Template Standar (Dummy)", "Sinkron Modul 28 (Live)"], index=0)
    source_3k = st.radio("Sektor Operasional (3K)", ["Template Standar (Dummy)", "Sinkron Modul 33 (Live)"], index=0)
    source_trace = st.radio("Sektor Keamanan", ["Template Standar (Dummy)", "Sinkron Modul 48 (Live)"], index=0)




# --- DATA FETCHING & FALLBACK (Mencegah Error) ---
# Penanganan aman apabila session kosong atau format tidak sesuai
default_rab = {
    'total_biaya': 850000000, 
    'roi_percent': 24.5, 
    'npv_value': 1250000000, 
    'payback_period': 2.5
}
default_3k = {
    'kapasitas_mingguan': 250,
    'efisiensi_panen': 92.5
}
default_ledger = [
    {"hash": "0x1A2B...", "timestamp": "2026-03-01"},
    {"hash": "0x8F4C...", "timestamp": "2026-03-02"},
    {"hash": "0x992E...", "timestamp": "2026-03-03"}
]

if source_rab == "Sinkron Modul 28 (Live)":
    rab_raw = st.session_state.get('global_rab_summary')
    if not rab_raw:
        st.sidebar.warning("⚠️ Warning: Data Modul 28 kosong. Menggunakan data Fallback.")
        rab_raw = default_rab
else:
    rab_raw = default_rab

if source_3k == "Sinkron Modul 33 (Live)":
    sim_raw = st.session_state.get('global_3k_sim')
    if not sim_raw:
        st.sidebar.warning("⚠️ Warning: Data Modul 33 kosong. Menggunakan data Fallback.")
        sim_raw = default_3k
else:
    sim_raw = default_3k

if source_trace == "Sinkron Modul 48 (Live)":
    ledger_raw = st.session_state.get('ledger_db')
    if not ledger_raw:
        st.sidebar.warning("⚠️ Warning: Data Modul 48 kosong. Menggunakan data Fallback.")
        ledger_raw = default_ledger
else:
    ledger_raw = default_ledger


# --- HEADER ---
st.markdown("""
<div style='background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 2rem; border-radius: 12px; color: white; margin-bottom: 2rem;'>
    <h1 style='margin:0; font-size: 2.2rem; color: #f8fafc;'>📄 Strategic Project Dossier V3</h1>
    <p style='margin: 0.5rem 0 0 0; font-size: 1.1rem; color: #94a3b8;'>Sistem Manajemen Laporan Strategis Terpadu Ekosistem AgriSensa</p>
</div>
""", unsafe_allow_html=True)

# Styling tambahan sembunyikan UI saat Mode Print (di dalam aplikasi)
st.markdown("""
<style>
@media print {
    /* Menyembunyikan elemen Streamlit yang tidak perlu */
    header, .stSidebar, .stTabs > div:first-child, .stButton, div[data-testid="stToolbar"] { display: none !important; }
    
    /* Memastikan halaman tidak terpotong (overflow visible pada parent container) */
    body, html, .stApp, .main, .block-container {
        height: auto !important;
        overflow: visible !important;
    }

    .book-white { display: block !important; padding: 0 !important; border: none !important; box-shadow: none !important;}
}
</style>
""", unsafe_allow_html=True)


# --- TABS ---
tab1, tab2, tab3 = st.tabs(["✍️ Step 1: Editor Konten", "📊 Step 2: Dashboard Eksekutif", "📑 Step 3: Cetak Laporan (Buku Putih)"])

# TAB 1: EDITOR
with tab1:
    st.subheader("Penyusunan Konten Strategis & Analisa")
    st.markdown("Edit ringkasan eksekutif sebelum di-_generate_ ke dalam Laporan Buku Putih.")
    
    st.markdown("##### 🔍 1. Matriks Analisis SWOT")
    cols = st.columns(2)
    with cols[0]:
        st.session_state['swot_data']['Strengths'] = st.text_area("🌟 Kekuatan (Strengths)", st.session_state['swot_data']['Strengths'], height=120)
        st.session_state['swot_data']['Opportunities'] = st.text_area("🎯 Peluang (Opportunities)", st.session_state['swot_data']['Opportunities'], height=120)
    with cols[1]:
        st.session_state['swot_data']['Weaknesses'] = st.text_area("⚠️ Kelemahan (Weaknesses)", st.session_state['swot_data']['Weaknesses'], height=120)
        st.session_state['swot_data']['Threats'] = st.text_area("💣 Ancaman (Threats)", st.session_state['swot_data']['Threats'], height=120)
    
    st.divider()
    
    st.markdown("##### 📅 2. Project Execution Timeline")
    df_timeline = pd.DataFrame(st.session_state['timeline_data'])
    edited_df = st.data_editor(df_timeline, num_rows="dynamic", use_container_width=True, hide_index=True)
    st.session_state['timeline_data'] = edited_df.to_dict('records')


# TAB 2: DASHBOARD
with tab2:
    st.subheader("Monitoring & Analisa Kelayakan Komprehensif")
    
    # METRICS ROW
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.info("💰 Total Investment")
        st.markdown(f"<h3 style='margin:0; color:#334155;'>Rp {rab_raw.get('total_biaya', 0):,.0f}</h3>", unsafe_allow_html=True)
    with m2:
        st.success("📈 Proyeksi ROI")
        st.markdown(f"<h3 style='margin:0; color:#10b981;'>{rab_raw.get('roi_percent', 0):.1f}%</h3>", unsafe_allow_html=True)
    with m3:
        st.warning("⏱️ Payback Period")
        st.markdown(f"<h3 style='margin:0; color:#f59e0b;'>{rab_raw.get('payback_period', 2.5)} Tahun</h3>", unsafe_allow_html=True)
    with m4:
        st.error("🛡️ Keamanan Sistem (Ledger)")
        st.markdown(f"<h3 style='margin:0; color:#ef4444;'>{len(ledger_raw)} Blocks Secured</h3>", unsafe_allow_html=True)

    st.divider()

    # CHARTS ROW
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Perbandingan Estimasi Penganggaran (Dummy Ratio)**")
        # Visualisasi Dummy CAPEX vs OPEX berdasarkan total investasi
        total_inv = float(rab_raw.get('total_biaya', 850000000))
        df_budget = pd.DataFrame({
            "Kategori": ["CAPEX (Infrastruktur)", "OPEX (Operasional YoY)", "Cadangan Darurat"],
            "Alokasi": [total_inv * 0.65, total_inv * 0.25, total_inv * 0.10]
        })
        fig = px.pie(df_budget, values="Alokasi", names="Kategori", hole=0.5, 
                     color_discrete_sequence=['#0ea5e9', '#10b981', '#f59e0b'])
        fig.update_layout(margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.markdown("**Indikator Skala Proyek & Operasional**")
        df_ind = pd.DataFrame({
            "Metrik": ["Kapasitas Produksi (Mingguan)", "Proyeksi NPV (Rp Miliar)", "Efisiensi"],
            "Nilai": [
                float(sim_raw.get('kapasitas_mingguan', 0)),
                float(rab_raw.get('npv_value', 0)) / 1000000000, # to Bio
                float(sim_raw.get('efisiensi_panen', 90))
            ]
        })
        fig2 = px.bar(df_ind, x="Nilai", y="Metrik", orientation='h', 
                      color="Metrik", color_discrete_sequence=['#6366f1', '#14b8a6', '#8b5cf6'])
        fig2.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)


# TAB 3: LAPORAN (BUKU PUTIH / PRINT VIEW)
with tab3:
    col_print, _ = st.columns([1, 4])
    with col_print:
        if st.button("🖨️ Cetak Buku Putih", type="primary", use_container_width=True):
            st.info("📌 Jendela cetakan disiapkan. (Tekan Ctrl+P)")
            st.components.v1.html("<script>setTimeout(function() { window.parent.print(); }, 1000);</script>", height=0)
    
    st.divider()
    
    # Membangun struktur HTML untuk tampilan laporannya 
    # Tampilan ini akan di-target oleh @media print 
    
    # Bangun Timeline HTML
    tl_html = ""
    for idx, row in enumerate(st.session_state['timeline_data']):
        tl_html += f"<tr><td style='padding: 8px; border-bottom: 1px solid #e2e8f0;'>Milestone {idx+1}</td><td style='padding: 8px; border-bottom: 1px solid #e2e8f0;'><strong>{row.get('Fase','-')}</strong></td><td style='padding: 8px; text-align:right; border-bottom: 1px solid #e2e8f0;'>{row.get('Durasi','-')}</td></tr>"
    
    # Rendering Dokumen Premium
    print_html = f"""<div class="book-white" style="font-family: 'Times New Roman', serif; color: #000; max-width: 800px; margin: 0 auto; padding: 40px; background: white; border: 1px solid #cbd5e1; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
<!-- HEADER KOP SURAT -->
<table style="width: 100%; border-bottom: 3px solid #1e293b; margin-bottom: 25px; padding-bottom: 15px;">
    <tr>
        <td style="width: 25%;"><h1 style="color: #16a34a; margin:0;">🌾 AgriSensa</h1><p style="margin:0; font-size: 11px; color:#64748b;">Ecosystem Intelligence</p></td>
        <td style="text-align: center;"><h2 style="margin:0; color:#1e293b; text-transform: uppercase;">STRATEGIC PROJECT DOSSIER / BUKU PUTIH</h2><p style="margin: 5px 0 0 0; font-size: 14px;">Nomor Dokumen: AS/PRJ/{datetime.date.today().strftime('%Y%m%d')}/01</p></td>
        <td style="width: 25%; text-align: right;"><span style="color: #64748b; font-size: 12px;">Tanggal Terbit:</span><br/><strong>{report_date.strftime('%d %B %Y')}</strong></td>
    </tr>
</table>

<!-- BAGIAN 1: PROFIL PROYEK -->
<h3 style="color: #1e293b; border-bottom: 1px solid #94a3b8; padding-bottom: 5px;">A. RINGKASAN EKSEKUTIF PROFIL PROYEK</h3>
<table style="width: 100%; margin-bottom: 25px; font-size: 14px; line-height: 1.6;">
    <tr><td style="width: 30%; font-weight: bold;">Nama Kegiatan / Proyek</td><td>: {proj_name}</td></tr>
    <tr><td style="font-weight: bold;">Instansi Pengusul</td><td>: {company_name}</td></tr>
    <tr><td style="font-weight: bold;">Penanggung Jawab / CEO</td><td>: {owner_name}</td></tr>
</table>

<!-- BAGIAN 2: ANALISIS SWOT -->
<h3 style="color: #1e293b; border-bottom: 1px solid #94a3b8; padding-bottom: 5px;">B. MATRIKS STRATEGI (SWOT ASSESSMENT)</h3>
<table style="width: 100%; border-collapse: collapse; margin-bottom: 25px; font-size: 13px;">
    <tr>
        <td style="width: 50%; padding: 15px; border: 1px solid #94a3b8; vertical-align: top; background-color: #f8fafc;">
            <h4 style="margin-top:0; color: #16a34a;">☑️ STRENGTHS (Kekuatan)</h4>
            <p style="margin:0;">{st.session_state['swot_data']['Strengths']}</p>
        </td>
        <td style="width: 50%; padding: 15px; border: 1px solid #94a3b8; vertical-align: top; background-color: #f8fafc;">
            <h4 style="margin-top:0; color: #b45309;">⚠️ WEAKNESSES (Kelemahan)</h4>
            <p style="margin:0;">{st.session_state['swot_data']['Weaknesses']}</p>
        </td>
    </tr>
    <tr>
        <td style="padding: 15px; border: 1px solid #94a3b8; vertical-align: top; background-color: #f8fafc;">
            <h4 style="margin-top:0; color: #2563eb;">🎯 OPPORTUNITIES (Peluang)</h4>
            <p style="margin:0;">{st.session_state['swot_data']['Opportunities']}</p>
        </td>
        <td style="padding: 15px; border: 1px solid #94a3b8; vertical-align: top; background-color: #f8fafc;">
            <h4 style="margin-top:0; color: #dc2626;">💣 THREATS (Ancaman)</h4>
            <p style="margin:0;">{st.session_state['swot_data']['Threats']}</p>
        </td>
    </tr>
</table>

<!-- BAGIAN 3: KELAYAKAN EKONOMI -->
<h3 style="color: #1e293b; border-bottom: 1px solid #94a3b8; padding-bottom: 5px;">C. PROYEKSI KELAYAKAN FINANSIAL & OPERASIONAL</h3>
<table style="width: 100%; border-collapse: collapse; margin-bottom: 25px; font-size: 14px;">
    <tr style="background:#f1f5f9;"><th style="padding:10px; border: 1px solid #cbd5e1; text-align: left;">Indikator Utama</th><th style="padding:10px; border: 1px solid #cbd5e1; text-align: right;">Estimasi Penilaian (Validasi Modul AgriSensa)</th></tr>
    <tr><td style="padding:10px; border: 1px solid #cbd5e1;">Pagu Investasi / Total Pengeluaran Modal (CAPEX+OPEX)</td><td style="padding:10px; border: 1px solid #cbd5e1; text-align: right; font-weight: bold;">Rp {rab_raw.get('total_biaya'):,.0f}</td></tr>
    <tr><td style="padding:10px; border: 1px solid #cbd5e1;">Return on Investment (ROI) Proyeksi</td><td style="padding:10px; border: 1px solid #cbd5e1; text-align: right; font-weight: bold; color: #16a34a;">{rab_raw.get('roi_percent'):.1f} %</td></tr>
    <tr><td style="padding:10px; border: 1px solid #cbd5e1;">Kapasitas Yield Operasional</td><td style="padding:10px; border: 1px solid #cbd5e1; text-align: right; font-weight: bold;">{sim_raw.get('kapasitas_mingguan')} kg/minggu</td></tr>
    <tr><td style="padding:10px; border: 1px solid #cbd5e1;">Arsitektur Pengamanan Catu Daya Rantai Pasok</td><td style="padding:10px; border: 1px solid #cbd5e1; text-align: right; font-weight: bold; color: #2563eb;">Traceability Blockchain ({len(ledger_raw)} node tersimpan)</td></tr>
</table>

<!-- BAGIAN 4: TIMELINE -->
<h3 style="color: #1e293b; border-bottom: 1px solid #94a3b8; padding-bottom: 5px;">D. TIMELINE EKSEKUSI PROYEK</h3>
<table style="width: 100%; border-collapse: collapse; margin-bottom: 40px; font-size: 14px;">
    <tr style="background:#1e293b; color: white;"><th style="padding:8px; text-align: left;">Tahapan</th><th style="padding:8px; text-align: left;">Fase Implementasi Operasional</th><th style="padding:8px; text-align: right;">Sasaran Jangka Waktu</th></tr>
    {tl_html}
</table>

<!-- BAGIAN 5: SIGNATURES -->
<p style="font-size: 12px; font-style: italic; color: #64748b; margin-bottom: 20px;">*Dossier ini di-generate secara otomatis via AgriSensa Artificial Intelligence System. Validasi dokumen memuat komparasi algoritma dan skenario pada data pipeline terpusat.</p>
<table style="width: 100%; text-align: center; margin-top: 30px;">
    <tr>
        <td style="width: 50%; padding-bottom: 80px;">Menyetujui & Memvalidasi,<br/><strong>Strategic Analyst (Sistem Terpadu)</strong></td>
        <td style="width: 50%; padding-bottom: 80px;">Ditetapkan oleh,<br/><strong>Project Director</strong></td>
    </tr>
    <tr>
        <td><strong>AgriSensa AI Engine</strong></td>
        <td><strong style="text-decoration: underline;">{owner_name}</strong><br/>{company_name}</td>
    </tr>
</table>
</div>"""
    
    st.markdown(print_html, unsafe_allow_html=True)
