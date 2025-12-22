import streamlit as st
import datetime
import pandas as pd

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
        "Strengths": "Teknologi presisi, Akses pasar modern, Traceability Blockchain.",
        "Weaknesses": "Ketergantungan cuaca ekstrim, Biaya awal infrastruktur.",
        "Opportunities": "Pasar ekspor sayuran premium, Pola makan sehat konsumen.",
        "Threats": "Fluktuasi harga pupuk global, Serangan hama bermutasi."
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
    proj_name = st.text_input("Nama Proyek", "Pusat Agribisnis Melon Premium 3K")
    company_name = st.text_input("Instansi / Perusahaan", "PT. AgriSensa Solusi Madani")
    owner_name = st.text_input("Penanggung Jawab / CEO", "Bpk. Yandri")
    report_date = st.date_input("Tanggal Terbit", datetime.date.today())
    
    st.divider()
    st.subheader("Sumber Data")
    source_rab = st.radio("Sektor Finansial (RAB)", ["Template Standar", "Sinkron Modul 28"], index=0)
    source_3k = st.radio("Sektor Operasional (3K)", ["Template Standar", "Sinkron Modul 33"], index=0)
    source_trace = st.radio("Sektor Keamanan", ["Template Standar", "Sinkron Modul 48"], index=0)

    st.divider()
    if st.button("Generate & Print (Buku Putih)", type="primary", use_container_width=True):
        st.info("Tekan Ctrl+P (Windows) atau Cmd+P (Mac) untuk mencetak")
        st.components.v1.html("<script>window.print();</script>", height=0)

# --- HEADER ---
st.title("Strategic Project Dossier V3")
st.markdown("Sistem Manajemen Laporan Strategis Terpadu")

# --- FETCH DATA ---
rab_raw = st.session_state.get('global_rab_summary', {}) if source_rab == "Sinkron Modul 28" else {}
sim_raw = st.session_state.get('global_3k_sim', {}) if source_3k == "Sinkron Modul 33" else {}
ledger_raw = st.session_state.get('ledger_db', []) if source_trace == "Sinkron Modul 48" else []

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["Step 1: Editor", "Step 2: Dashboard", "Step 3: Laporan"])

# TAB 1: EDITOR
with tab1:
    st.subheader("Penyusunan Konten Strategis")
    
    st.markdown("**1. Matriks SWOT**")
    cols = st.columns(2)
    with cols[0]:
        st.session_state['swot_data']['Strengths'] = st.text_area("Kekuatan (Strengths)", st.session_state['swot_data']['Strengths'])
        st.session_state['swot_data']['Opportunities'] = st.text_area("Peluang (Opportunities)", st.session_state['swot_data']['Opportunities'])
    with cols[1]:
        st.session_state['swot_data']['Weaknesses'] = st.text_area("Kelemahan (Weaknesses)", st.session_state['swot_data']['Weaknesses'])
        st.session_state['swot_data']['Threats'] = st.text_area("Ancaman (Threats)", st.session_state['swot_data']['Threats'])
    
    st.divider()
    
    st.markdown("**2. Project Timeline**")
    df_timeline = pd.DataFrame(st.session_state['timeline_data'])
    edited_df = st.data_editor(df_timeline, num_rows="dynamic", use_container_width=True)
    st.session_state['timeline_data'] = edited_df.to_dict('records')

# TAB 2: DASHBOARD
with tab2:
    st.subheader("Monitoring & Analisa Terintegrasi")
    
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Investment", f"Rp {rab_raw.get('total_biaya', 850000000):,.0f}")
    with m2:
        st.metric("ROI", f"{rab_raw.get('roi_percent', 0):.1f}%" if rab_raw else "24-28 Bulan")
    with m3:
        st.metric("Blockchain", f"{len(ledger_raw)} Blocks")
    with m4:
        st.metric("Kapasitas", f"{sim_raw.get('kapasitas_mingguan', 200)} kg/minggu")

# TAB 3: LAPORAN
with tab3:
    st.subheader("Laporan Strategis - Buku Putih")
    
    st.success(f"Proyek: {proj_name}")
    st.write(f"Perusahaan: {company_name}")
    st.write(f"Tanggal: {report_date}")
    
    st.divider()
    
    st.markdown("**Analisis SWOT**")
    swot = st.session_state.get('swot_data', {})
    c1, c2 = st.columns(2)
    with c1:
        st.success(f"**Strengths**\n\n{swot.get('Strengths', '')}")
        st.info(f"**Opportunities**\n\n{swot.get('Opportunities', '')}")
    with c2:
        st.warning(f"**Weaknesses**\n\n{swot.get('Weaknesses', '')}")
        st.error(f"**Threats**\n\n{swot.get('Threats', '')}")
    
    st.divider()
    
    st.markdown("**Kelayakan Ekonomi**")
    df_ekonomi = pd.DataFrame({
        "Parameter": ["Total Investasi", "Estimasi ROI", "Kapasitas", "Blockchain"],
        "Nilai": [
            f"Rp {rab_raw.get('total_biaya', 850000000):,.0f}",
            f"{rab_raw.get('roi_percent', 0):.1f}%" if rab_raw else "24-28 Bulan",
            f"{sim_raw.get('kapasitas_mingguan', 200)} kg/minggu",
            f"{len(ledger_raw)} Transaksi"
        ]
    })
    st.table(df_ekonomi)
    
    st.divider()
    
    st.markdown("**Timeline Implementasi**")
    df_timeline_display = pd.DataFrame(st.session_state['timeline_data'])
    st.table(df_timeline_display)
    
    st.divider()
    
    st.caption("Seluruh data dihasilkan dari sistem AgriSensa Intelligence")
    
    sig1, sig2 = st.columns(2)
    with sig1:
        st.markdown(f"**Strategic Analyst**\n\nAgriSensa AI System")
    with sig2:
        st.markdown(f"**Project Director**\n\n{owner_name}\n\n{company_name}")
