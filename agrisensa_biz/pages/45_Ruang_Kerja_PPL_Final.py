
import streamlit as st
import pandas as pd
import json
import os
import random
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date, timedelta
from io import BytesIO

# Page Config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Ruang Kerja PPL",
    page_icon="📢",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

# ========== DATA PERSISTENCE ==========
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "ppl")
TASKS_FILE = os.path.join(DATA_DIR, "ppl_tasks.json")
VISITS_FILE = os.path.join(DATA_DIR, "ppl_visits.json")
POKTAN_FILE = os.path.join(DATA_DIR, "ppl_poktan.json")

def ensure_data_dir():
    """Create data directory if not exists"""
    os.makedirs(DATA_DIR, exist_ok=True)

def load_tasks():
    """Load tasks from JSON file"""
    ensure_data_dir()
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks to JSON file"""
    ensure_data_dir()
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2, default=str)

def load_visits():
    """Load visit logs from JSON file"""
    ensure_data_dir()
    if os.path.exists(VISITS_FILE):
        with open(VISITS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_visits(visits):
    """Save visits to JSON file"""
    ensure_data_dir()
    with open(VISITS_FILE, 'w', encoding='utf-8') as f:
        json.dump(visits, f, ensure_ascii=False, indent=2, default=str)

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(30, 58, 138, 0.3);
    }
    .main-header h1 { color: white !important; margin: 0; }
    .main-header p { color: #bfdbfe; margin: 0.5rem 0 0 0; }
    
    .stat-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid #cbd5e1;
        transition: all 0.3s ease;
    }
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e3a8a;
        line-height: 1;
    }
    .stat-label {
        font-size: 0.85rem;
        color: #64748b;
        margin-top: 0.5rem;
    }
    
    .task-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    .task-card.high { border-left-color: #ef4444; }
    .task-card.medium { border-left-color: #f59e0b; }
    .task-card.low { border-left-color: #10b981; }
    .task-card.done { opacity: 0.6; background: #f1f5f9; }
    
    .priority-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .priority-high { background: #fef2f2; color: #dc2626; }
    .priority-medium { background: #fffbeb; color: #d97706; }
    .priority-low { background: #ecfdf5; color: #059669; }
    
    .status-badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    .status-pending { background: #fef3c7; color: #92400e; }
    .status-in_progress { background: #dbeafe; color: #1e40af; }
    .status-done { background: #d1fae5; color: #065f46; }
    
    .visit-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        border: 1px solid #a7f3d0;
    }
    
    h1, h2, h3 { color: #1e3a8a; }
</style>
""", unsafe_allow_html=True)

# ========== HEADER ==========
st.markdown('''
<div class="main-header">
    <h1>📢 Ruang Kerja PPL</h1>
    <p>Sistem Pendukung Keputusan Petugas Penyuluh Lapangan</p>
</div>
''', unsafe_allow_html=True)

# ========== TABS ==========
tab_dashboard, tab_tasks, tab_reports, tab_ubinan, tab_rdkk, tab_materi = st.tabs([
    "📊 Dashboard",
    "📋 Manajemen Tugas",
    "📝 Pelaporan",
    "🌾 Kalkulator Ubinan",
    "📋 Simulator e-RDKK",
    "📢 Generator Materi"
])

# ========================================
# TAB 1: DASHBOARD
# ========================================
with tab_dashboard:
    st.markdown("### 📊 Dashboard PPL")
    
    # Load data
    tasks = load_tasks()
    visits = load_visits()
    
    # Calculate stats
    total_tasks = len(tasks)
    pending_tasks = len([t for t in tasks if t.get('status') == 'pending'])
    in_progress = len([t for t in tasks if t.get('status') == 'in_progress'])
    done_tasks = len([t for t in tasks if t.get('status') == 'done'])
    
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    visits_this_week = len([v for v in visits if v.get('date', '') >= str(week_start)])
    
    # Quick Stats
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number">{total_tasks}</div>
            <div class="stat-label">Total Tugas</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number" style="color: #f59e0b;">{pending_tasks}</div>
            <div class="stat-label">Menunggu</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number" style="color: #3b82f6;">{in_progress}</div>
            <div class="stat-label">Dikerjakan</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number" style="color: #10b981;">{done_tasks}</div>
            <div class="stat-label">Selesai</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col5:
        st.markdown(f'''
        <div class="stat-card">
            <div class="stat-number" style="color: #8b5cf6;">{visits_this_week}</div>
            <div class="stat-label">Kunjungan Minggu Ini</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Performance & Upcoming
    col_perf, col_upcoming = st.columns(2)
    
    with col_perf:
        st.subheader("📈 Performa Bulan Ini")
        
        if total_tasks > 0:
            completion_rate = (done_tasks / total_tasks) * 100
        else:
            completion_rate = 0
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = completion_rate,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Tingkat Penyelesaian Tugas"},
            delta = {'reference': 80, 'increasing': {'color': "#10b981"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#3b82f6"},
                'steps': [
                    {'range': [0, 50], 'color': "#fef3c7"},
                    {'range': [50, 80], 'color': "#dbeafe"},
                    {'range': [80, 100], 'color': "#d1fae5"}
                ],
                'threshold': {
                    'line': {'color': "#ef4444", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_upcoming:
        st.subheader("🗓️ Tugas Mendatang")
        
        # Get upcoming tasks (pending/in_progress, sorted by due date)
        upcoming = [t for t in tasks if t.get('status') in ['pending', 'in_progress']]
        upcoming = sorted(upcoming, key=lambda x: x.get('due_date', '9999-12-31'))[:5]
        
        if upcoming:
            for task in upcoming:
                priority_class = f"priority-{task.get('priority', 'medium')}"
                st.markdown(f'''
                <div class="task-card {task.get('priority', 'medium')}">
                    <strong>{task.get('title', 'Untitled')}</strong><br>
                    <span style="color: #64748b; font-size: 0.85rem;">
                        📍 {task.get('poktan', '-')} • 📅 {task.get('due_date', '-')}
                    </span>
                    <span class="priority-badge {priority_class}">{task.get('priority', 'medium')}</span>
                </div>
                ''', unsafe_allow_html=True)
        else:
            st.info("🎉 Tidak ada tugas mendatang. Kerja bagus!")
    
    # Recent Visits
    st.markdown("---")
    st.subheader("📝 Kunjungan Terakhir")
    
    recent_visits = sorted(visits, key=lambda x: x.get('date', ''), reverse=True)[:5]
    
    if recent_visits:
        for visit in recent_visits:
            st.markdown(f'''
            <div class="visit-card">
                <strong>📍 {visit.get('poktan', '-')}</strong> - {visit.get('desa', '-')}<br>
                <span style="color: #065f46; font-size: 0.85rem;">
                    📅 {visit.get('date', '-')} • 👥 {visit.get('jumlah_hadir', 0)} peserta
                </span><br>
                <span style="color: #059669; font-size: 0.8rem;">{visit.get('kegiatan', '-')}</span>
            </div>
            ''', unsafe_allow_html=True)
    else:
        st.info("Belum ada data kunjungan. Mulai catat kunjungan di tab Pelaporan.")

# ========================================
# TAB 2: MANAJEMEN TUGAS
# ========================================
with tab_tasks:
    st.markdown("### 📋 Manajemen Tugas")
    
    # Initialize session state
    if 'task_edit_id' not in st.session_state:
        st.session_state.task_edit_id = None
    
    tasks = load_tasks()
    
    # Subtabs
    subtab_list, subtab_create = st.tabs(["📋 Daftar Tugas", "➕ Buat Tugas Baru"])
    
    # ---- CREATE TASK ----
    with subtab_create:
        st.subheader("➕ Buat Tugas Baru")
        
        with st.form("create_task_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                task_title = st.text_input("📝 Judul Tugas *", placeholder="Kunjungan rutin Poktan Maju Bersama")
                task_poktan = st.text_input("👥 Kelompok Tani", placeholder="Sukamaju I")
                task_desa = st.text_input("📍 Desa/Kelurahan", placeholder="Sukamakmur")
            
            with col2:
                task_due = st.date_input("📅 Tenggat Waktu", value=date.today() + timedelta(days=7))
                task_priority = st.selectbox("🚦 Prioritas", ["high", "medium", "low"], index=1,
                                            format_func=lambda x: {"high": "🔴 Tinggi", "medium": "🟡 Sedang", "low": "🟢 Rendah"}[x])
                task_status = st.selectbox("📊 Status", ["pending", "in_progress", "done"], index=0,
                                          format_func=lambda x: {"pending": "⏳ Menunggu", "in_progress": "🔄 Dikerjakan", "done": "✅ Selesai"}[x])
            
            task_desc = st.text_area("📄 Deskripsi", placeholder="Detail tugas yang harus dikerjakan...")
            
            submitted = st.form_submit_button("💾 Simpan Tugas", use_container_width=True, type="primary")
            
            if submitted:
                if task_title:
                    new_task = {
                        "id": str(datetime.now().timestamp()),
                        "title": task_title,
                        "description": task_desc,
                        "poktan": task_poktan,
                        "desa": task_desa,
                        "due_date": str(task_due),
                        "priority": task_priority,
                        "status": task_status,
                        "created_date": str(date.today())
                    }
                    tasks.append(new_task)
                    save_tasks(tasks)
                    st.success("✅ Tugas berhasil disimpan!")
                    st.rerun()
                else:
                    st.error("❌ Judul tugas wajib diisi!")
    
    # ---- TASK LIST ----
    with subtab_list:
        # Filters
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        with col_filter1:
            filter_status = st.selectbox("Filter Status", ["all", "pending", "in_progress", "done"],
                                        format_func=lambda x: {"all": "📋 Semua", "pending": "⏳ Menunggu", 
                                                               "in_progress": "🔄 Dikerjakan", "done": "✅ Selesai"}[x])
        with col_filter2:
            filter_priority = st.selectbox("Filter Prioritas", ["all", "high", "medium", "low"],
                                          format_func=lambda x: {"all": "🚦 Semua", "high": "🔴 Tinggi", 
                                                                 "medium": "🟡 Sedang", "low": "🟢 Rendah"}[x])
        with col_filter3:
            sort_by = st.selectbox("Urutkan", ["due_date", "created_date", "priority"],
                                  format_func=lambda x: {"due_date": "📅 Tenggat", "created_date": "🕐 Dibuat", 
                                                         "priority": "🚦 Prioritas"}[x])
        
        # Filter tasks
        filtered_tasks = tasks.copy()
        if filter_status != "all":
            filtered_tasks = [t for t in filtered_tasks if t.get('status') == filter_status]
        if filter_priority != "all":
            filtered_tasks = [t for t in filtered_tasks if t.get('priority') == filter_priority]
        
        # Sort
        priority_order = {"high": 0, "medium": 1, "low": 2}
        if sort_by == "priority":
            filtered_tasks = sorted(filtered_tasks, key=lambda x: priority_order.get(x.get('priority', 'medium'), 1))
        else:
            filtered_tasks = sorted(filtered_tasks, key=lambda x: x.get(sort_by, ''), reverse=(sort_by == 'created_date'))
        
        st.markdown(f"**{len(filtered_tasks)} tugas ditemukan**")
        st.markdown("---")
        
        # Display tasks
        if filtered_tasks:
            for idx, task in enumerate(filtered_tasks):
                task_class = f"task-card {task.get('priority', 'medium')}"
                if task.get('status') == 'done':
                    task_class += " done"
                
                priority_class = f"priority-{task.get('priority', 'medium')}"
                status_class = f"status-{task.get('status', 'pending')}"
                status_label = {"pending": "⏳ Menunggu", "in_progress": "🔄 Dikerjakan", "done": "✅ Selesai"}
                
                col_task, col_actions = st.columns([4, 1])
                
                with col_task:
                    st.markdown(f'''
                    <div class="{task_class}">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div>
                                <strong style="font-size: 1.1rem;">{task.get('title', 'Untitled')}</strong>
                                <span class="priority-badge {priority_class}">{task.get('priority', 'medium').upper()}</span>
                                <span class="status-badge {status_class}">{status_label.get(task.get('status'), 'Pending')}</span>
                            </div>
                        </div>
                        <div style="color: #64748b; font-size: 0.85rem; margin-top: 0.5rem;">
                            📍 {task.get('poktan', '-')} • {task.get('desa', '-')} | 📅 Tenggat: {task.get('due_date', '-')}
                        </div>
                        <div style="color: #475569; font-size: 0.9rem; margin-top: 0.3rem;">
                            {task.get('description', '')[:100]}{'...' if len(task.get('description', '')) > 100 else ''}
                        </div>
                    </div>
                    ''', unsafe_allow_html=True)
                
                with col_actions:
                    # Quick status update
                    new_status = st.selectbox(
                        "Status",
                        ["pending", "in_progress", "done"],
                        index=["pending", "in_progress", "done"].index(task.get('status', 'pending')),
                        key=f"status_{task.get('id')}",
                        label_visibility="collapsed"
                    )
                    
                    if new_status != task.get('status'):
                        # Update task status
                        for t in tasks:
                            if t.get('id') == task.get('id'):
                                t['status'] = new_status
                                break
                        save_tasks(tasks)
                        st.rerun()
                    
                    if st.button("🗑️", key=f"del_{task.get('id')}", help="Hapus tugas"):
                        tasks = [t for t in tasks if t.get('id') != task.get('id')]
                        save_tasks(tasks)
                        st.rerun()
        else:
            st.info("📭 Tidak ada tugas yang ditemukan.")

# ========================================
# TAB 3: PELAPORAN
# ========================================
with tab_reports:
    st.markdown("### 📝 Sistem Pelaporan")
    
    visits = load_visits()
    
    subtab_log, subtab_weekly, subtab_monthly, subtab_history = st.tabs([
        "📝 Catat Kunjungan", "📊 Laporan Mingguan", "📈 Rekapitulasi Bulanan", "📋 Riwayat"
    ])
    
    # ---- LOG VISIT ----
    with subtab_log:
        st.subheader("📝 Catat Kunjungan Lapangan")
        
        with st.form("visit_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                visit_date = st.date_input("📅 Tanggal Kunjungan", value=date.today())
                visit_poktan = st.text_input("👥 Kelompok Tani *", placeholder="Sukamaju I")
                visit_desa = st.text_input("📍 Desa/Kelurahan", placeholder="Sukamakmur")
                visit_kec = st.text_input("🏘️ Kecamatan", placeholder="Caringin")
            
            with col2:
                visit_kegiatan = st.selectbox("📋 Jenis Kegiatan", [
                    "Penyuluhan Kelompok",
                    "Kunjungan Lapangan",
                    "Monitoring Tanaman",
                    "Pengambilan Ubinan",
                    "Verifikasi e-RDKK",
                    "Rapat Koordinasi",
                    "Pelatihan/Demo",
                    "Lainnya"
                ])
                visit_hadir = st.number_input("👥 Jumlah Peserta", min_value=0, value=15)
                visit_laki = st.number_input("👨 Peserta Laki-laki", min_value=0, value=10)
                visit_perempuan = st.number_input("👩 Peserta Perempuan", min_value=0, value=5)
            
            visit_catatan = st.text_area("📝 Catatan/Hasil Kunjungan", 
                                        placeholder="Ringkasan kegiatan dan hasil diskusi...")
            visit_tindak = st.text_area("🎯 Rencana Tindak Lanjut", 
                                       placeholder="Langkah selanjutnya yang akan dilakukan...")
            
            submitted_visit = st.form_submit_button("💾 Simpan Laporan Kunjungan", 
                                                   use_container_width=True, type="primary")
            
            if submitted_visit:
                if visit_poktan:
                    new_visit = {
                        "id": str(datetime.now().timestamp()),
                        "date": str(visit_date),
                        "poktan": visit_poktan,
                        "desa": visit_desa,
                        "kecamatan": visit_kec,
                        "kegiatan": visit_kegiatan,
                        "jumlah_hadir": visit_hadir,
                        "laki_laki": visit_laki,
                        "perempuan": visit_perempuan,
                        "catatan": visit_catatan,
                        "tindak_lanjut": visit_tindak,
                        "created_at": str(datetime.now())
                    }
                    visits.append(new_visit)
                    save_visits(visits)
                    st.success("✅ Laporan kunjungan berhasil disimpan!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Nama Kelompok Tani wajib diisi!")
    
    # ---- WEEKLY REPORT ----
    with subtab_weekly:
        st.subheader("📊 Generator Laporan Mingguan")
        
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            week_start = st.date_input("Mulai Minggu", value=date.today() - timedelta(days=date.today().weekday()))
        with col_w2:
            week_end = st.date_input("Akhir Minggu", value=week_start + timedelta(days=6))
        
        ppl_name = st.text_input("Nama PPL", value=user.get('name', 'PPL'))
        wilayah = st.text_input("Wilayah Binaan", placeholder="Kec. Caringin, Kab. Bogor")
        
        if st.button("📄 Generate Laporan Mingguan", type="primary"):
            # Filter visits for the week
            week_visits = [v for v in visits if str(week_start) <= v.get('date', '') <= str(week_end)]
            
            total_visits = len(week_visits)
            total_peserta = sum(v.get('jumlah_hadir', 0) for v in week_visits)
            total_poktan = len(set(v.get('poktan', '') for v in week_visits))
            
            report_text = f"""
╔══════════════════════════════════════════════════════════════╗
║          LAPORAN MINGGUAN PETUGAS PENYULUH LAPANGAN          ║
╚══════════════════════════════════════════════════════════════╝

📅 Periode       : {week_start.strftime('%d %B %Y')} - {week_end.strftime('%d %B %Y')}
👤 Nama PPL      : {ppl_name}
🗺️ Wilayah Binaan: {wilayah}

════════════════════════════════════════════════════════════════
                        RINGKASAN KEGIATAN
════════════════════════════════════════════════════════════════

📊 STATISTIK MINGGU INI:
   • Total Kunjungan    : {total_visits} kali
   • Poktan Dikunjungi  : {total_poktan} kelompok
   • Total Peserta      : {total_peserta} orang

📋 RINCIAN KEGIATAN:
"""
            for i, v in enumerate(week_visits, 1):
                report_text += f"""
   {i}. {v.get('date', '')} - {v.get('poktan', '')} ({v.get('desa', '')})
      Kegiatan : {v.get('kegiatan', '')}
      Peserta  : {v.get('jumlah_hadir', 0)} orang (L: {v.get('laki_laki', 0)}, P: {v.get('perempuan', 0)})
      Catatan  : {v.get('catatan', '-')[:80]}...
"""
            
            report_text += f"""
════════════════════════════════════════════════════════════════

Demikian laporan mingguan ini dibuat dengan sebenarnya.

                                        {date.today().strftime('%d %B %Y')}
                                        Petugas Penyuluh Lapangan,

                                        {ppl_name}
"""
            
            st.text_area("📄 Laporan Mingguan", value=report_text, height=500)
            
            # Download button
            st.download_button(
                label="📥 Download Laporan (TXT)",
                data=report_text,
                file_name=f"Laporan_Mingguan_PPL_{week_start}_{week_end}.txt",
                mime="text/plain"
            )
    
    # ---- MONTHLY SUMMARY ----
    with subtab_monthly:
        st.subheader("📈 Rekapitulasi Bulanan")
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            month_year = st.date_input("Pilih Bulan", value=date.today().replace(day=1))
        
        # Filter for the selected month
        month_start = month_year.replace(day=1)
        if month_year.month == 12:
            month_end = month_year.replace(year=month_year.year + 1, month=1, day=1)
        else:
            month_end = month_year.replace(month=month_year.month + 1, day=1)
        
        month_visits = [v for v in visits if str(month_start) <= v.get('date', '') < str(month_end)]
        
        # Stats
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        col_s1.metric("Total Kunjungan", len(month_visits))
        col_s2.metric("Total Peserta", sum(v.get('jumlah_hadir', 0) for v in month_visits))
        col_s3.metric("Poktan Terjangkau", len(set(v.get('poktan', '') for v in month_visits)))
        col_s4.metric("Peserta/Kunjungan", 
                     f"{sum(v.get('jumlah_hadir', 0) for v in month_visits) / max(len(month_visits), 1):.1f}")
        
        st.markdown("---")
        
        # Chart by activity type
        if month_visits:
            df_kegiatan = pd.DataFrame(month_visits)
            kegiatan_counts = df_kegiatan['kegiatan'].value_counts().reset_index()
            kegiatan_counts.columns = ['Jenis Kegiatan', 'Jumlah']
            
            fig = px.pie(kegiatan_counts, values='Jumlah', names='Jenis Kegiatan',
                        title="Distribusi Jenis Kegiatan",
                        color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig, use_container_width=True)
            
            # Gender distribution
            total_l = sum(v.get('laki_laki', 0) for v in month_visits)
            total_p = sum(v.get('perempuan', 0) for v in month_visits)
            
            fig2 = px.pie(
                values=[total_l, total_p],
                names=['Laki-laki', 'Perempuan'],
                title="Distribusi Gender Peserta",
                color_discrete_sequence=['#3b82f6', '#ec4899']
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Belum ada data kunjungan untuk bulan ini.")
    
    # ---- HISTORY ----
    with subtab_history:
        st.subheader("📋 Riwayat Kunjungan")
        
        if visits:
            df_visits = pd.DataFrame(visits)
            df_visits = df_visits.sort_values('date', ascending=False)
            
            # Display columns
            display_cols = ['date', 'poktan', 'desa', 'kegiatan', 'jumlah_hadir']
            rename_cols = {
                'date': 'Tanggal',
                'poktan': 'Kelompok Tani',
                'desa': 'Desa',
                'kegiatan': 'Kegiatan',
                'jumlah_hadir': 'Peserta'
            }
            
            df_display = df_visits[display_cols].rename(columns=rename_cols)
            st.dataframe(df_display, use_container_width=True, hide_index=True)
            
            # Export to Excel
            buffer = BytesIO()
            df_visits.to_excel(buffer, index=False, sheet_name='Kunjungan')
            buffer.seek(0)
            
            st.download_button(
                label="📥 Export ke Excel",
                data=buffer,
                file_name=f"Riwayat_Kunjungan_PPL_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.info("Belum ada riwayat kunjungan.")

# ========================================
# TAB 4: KALKULATOR UBINAN (EXISTING)
# ========================================
with tab_ubinan:
    st.markdown("### 🌾 Kalkulator Ubinan Digital")
    st.info("Alat bantu hitung cepat estimasi produktivitas panen di lapangan.")
    
    col_u1, col_u2 = st.columns(2)
    
    with col_u1:
        st.subheader("📝 Input Lapangan")
        panjang = st.number_input("Panjang Ubinan (m)", value=2.5, step=0.1, key="ub_panjang")
        lebar = st.number_input("Lebar Ubinan (m)", value=2.5, step=0.1, key="ub_lebar")
        berat_ubin = st.number_input("Berat Gabah (GKP) per Ubinan (Kg)", value=6.0, step=0.1, 
                                     help="Berat bersih setelah dikurangi tarra.", key="ub_berat")
        jml_rumpun = st.number_input("Jumlah Rumpun dalam Ubinan", value=120, step=10, 
                                     help="Untuk menghitung populasi per Ha.", key="ub_rumpun")
        
    with col_u2:
        st.subheader("📊 Hasil Analisa")
        
        luas_ubin = panjang * lebar
        faktor_konversi = 10000 / luas_ubin
        hasil_gkp_ha = (berat_ubin * faktor_konversi) / 1000
        hasil_gkg = hasil_gkp_ha * 0.8602
        hasil_beras = hasil_gkg * 0.6402
        populasi_ha = jml_rumpun * faktor_konversi
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Estimasi GKP", f"{hasil_gkp_ha:.2f} Ton/Ha")
        col_m2.metric("Estimasi Beras", f"{hasil_beras:.2f} Ton/Ha")
        
        st.info(f"""
        **Detail Teknis:**
        - Faktor Konversi: {faktor_konversi:,.0f}x
        - Populasi: {populasi_ha:,.0f} rumpun/Ha
        - GKG (Giling): {hasil_gkg:.2f} Ton/Ha
        """)

    # Berita Acara
    st.markdown("---")
    with st.expander("📄 Buat Berita Acara (Siap Cetak)", expanded=False):
        c_ba1, c_ba2 = st.columns(2)
        with c_ba1:
            ba_poktan = st.text_input("Nama Kelompok Tani", "Sukamaju I", key="ba_poktan")
            ba_desa = st.text_input("Desa/Kelurahan", "Sukamakmur", key="ba_desa")
            ba_var = st.text_input("Varietas Padi", "Ciherang", key="ba_var")
        with c_ba2:
            ba_kec = st.text_input("Kecamatan", "Caringin", key="ba_kec")
            ba_tanggal = st.date_input("Tanggal Ubinan", date.today(), key="ba_tanggal")
            ba_ka = st.number_input("Kadar Air Saat Panen (%)", 20.0, key="ba_ka")

        ba_text = f"""BERITA ACARA PENGAMBILAN UBINAN
-----------------------------------------
Pada hari ini {ba_tanggal.strftime('%A, %d %B %Y')}, telah dilakukan pengambilan ubinan padi sawah di:

📍 LOKASI
Kelompok Tani : {ba_poktan}
Desa/Kel.     : {ba_desa}
Kecamatan     : {ba_kec}

🌾 DATA TEKNIS
Varietas      : {ba_var}
Luas Petak    : {panjang} m x {lebar} m ({luas_ubin} m²)
Jumlah Rumpun : {jml_rumpun} rumpun (Sampel)

⚖️ HASIL UBINAN
Berat Ubinan  : {berat_ubin} kg
Kadar Air     : {ba_ka} %
-----------------------------------------
✅ KONVERSI HASIL (ESTIMASI)
Produktivitas : {hasil_gkp_ha:.2f} Ton/Ha (GKP)
Populasi      : {populasi_ha:,.0f} Rumpun/Ha

Demikian berita acara ini dibuat untuk dipergunakan sebagaimana mestinya.

Mengetahui,
Penyuluh Pertanian (PPL)             Ketua Kelompok Tani

( .................... )             ( .................... )
"""
        st.text_area("Salin Teks Ini:", value=ba_text, height=350, key="ba_text")
        st.download_button("📥 Download Berita Acara", data=ba_text, 
                          file_name=f"Berita_Acara_Ubinan_{ba_tanggal}.txt")

# ========================================
# TAB 5: E-RDKK (EXISTING)
# ========================================
with tab_rdkk:
    st.markdown("### 📋 Cek Kuota Pupuk Subsidi (Simulasi)")
    st.info("Berdasarkan aturan Permentan (Maksimal 2 Ha per NIK).")
    
    col_r1, col_r2 = st.columns([1, 2])
    
    with col_r1:
        luas_lahan = st.number_input("Luas Lahan (Ha)", value=1.0, max_value=10.0, step=0.1, key="rdkk_luas")
        komoditas = st.selectbox("Komoditas Prioritas", 
                                 ["Padi", "Jagung", "Kedelai", "Cabai", "Bawang Merah", "Bawang Putih", 
                                  "Tebu Rakyat", "Kopi", "Kakao"], key="rdkk_komoditas")
        mt = st.selectbox("Musim Tanam", ["MT 1", "MT 2", "MT 3"], key="rdkk_mt")
        
    with col_r2:
        quota_ref = {
            "Padi": {"urea": 200, "npk": 250},
            "Jagung": {"urea": 250, "npk": 300},
            "Kedelai": {"urea": 50, "npk": 150},
            "Cabai": {"urea": 200, "npk": 200},
        }
        ref = quota_ref.get(komoditas, {"urea": 150, "npk": 150})
        
        luas_valid = min(luas_lahan, 2.0)
        is_capped = luas_lahan > 2.0
        
        quota_urea = ref['urea'] * luas_valid
        quota_npk = ref['npk'] * luas_valid
        
        if is_capped:
            st.warning(f"⚠️ Input {luas_lahan} Ha melebihi batas subsidi. Perhitungan dibatasi max 2.0 Ha.")
        
        st.success(f"✅ **Alokasi Subsidi untuk {komoditas} ({mt}):**")
        
        q1, q2 = st.columns(2)
        q1.metric("UREA (Subsidi)", f"{quota_urea:,.0f} Kg")
        q2.metric("NPK FORMULA (Subsidi)", f"{quota_npk:,.0f} Kg")
        
        st.caption("*Simulasi sesuai rekomendasi teknis umum. Realisasi tergantung e-Alokasi daerah.*")

        # Chart
        need_urea_ideal = 250 * luas_lahan if komoditas in ["Padi", "Jagung"] else 150 * luas_lahan
        subsidi_pct = (quota_urea / need_urea_ideal) * 100 if need_urea_ideal > 0 else 0
        mandiri_pct = 100 - subsidi_pct
        
        df_chart = pd.DataFrame({
            "Jenis": ["Subsidi (Jatah)", "Mandiri (Kekurangan)"],
            "Jumlah": [subsidi_pct, mandiri_pct]
        })
        
        fig = px.pie(df_chart, values='Jumlah', names='Jenis', 
                     title=f"Cakupan Subsidi vs Kebutuhan ({komoditas})",
                     color='Jenis',
                     color_discrete_map={'Subsidi (Jatah)':'#10b981', 'Mandiri (Kekurangan)':'#f59e0b'})
        st.plotly_chart(fig, use_container_width=True)

# ========================================
# TAB 6: GENERATOR MATERI (EXISTING - Enhanced)
# ========================================
with tab_materi:
    st.markdown("### 📢 Generator Materi Penyuluhan")
    st.markdown("Buat outline materi penyuluhan dalam hitungan detik untuk pertemuan poktan.")
    
    topik = st.text_input("Topik Penyuluhan:", placeholder="Contoh: Pengendalian Hama Wereng Batang Coklat",
                         key="materi_topik")
    audiens = st.selectbox("Target Audiens:", 
                          ["Kelompok Tani Pemula", "Kelompok Tani Lanjut/Madya", "Petani Milenial"],
                          key="materi_audiens")
    durasi = st.selectbox("Durasi Penyuluhan:", ["30 menit", "1 jam", "2 jam"], key="materi_durasi")
    
    if st.button("🤖 Buat Materi", key="btn_materi"):
        if topik:
            st.markdown("---")
            st.markdown(f"#### 🎙️ Modul Penyuluhan: {topik}")
            st.caption(f"Audiens: {audiens} | Durasi: {durasi}")
            
            intro_style = "Santai & Motivasi" if "Pemula" in audiens else "Teknis & Data"
            waktu_isi = "15 menit" if durasi == "30 menit" else ("30 menit" if durasi == "1 jam" else "1 jam")
            
            materi_text = f"""
═══════════════════════════════════════════════════
       MODUL PENYULUHAN: {topik.upper()}
═══════════════════════════════════════════════════
📋 Audiens    : {audiens}
⏱️ Durasi     : {durasi}
🎨 Gaya       : {intro_style}

═══════════════════════════════════════════════════
              STRUKTUR MATERI
═══════════════════════════════════════════════════

📍 1. PEMBUKAAN ({intro_style}) - 5-10 menit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✦ Salam & Apersepsi
     "Assalamualaikum, selamat pagi Bapak/Ibu..."
     Tanyakan kabar lahan dan tanaman.
   
   ✦ Ice Breaking
     "Siapa yang minggu ini sudah ke sawah?"
     
   ✦ Pengantar Topik
     "Hari ini kita bahas {topik} yang sedang hangat."

📍 2. ISI MATERI (Poin Kunci) - {waktu_isi}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   A. IDENTIFIKASI MASALAH
      • Ciri-ciri serangan/kendala di lapangan
      • Foto/gambar contoh gejala
      • Pengalaman petani setempat
   
   B. SOLUSI PRAKTIS
      • Langkah 1: [Sesuaikan dengan topik]
      • Langkah 2: [Sesuaikan dengan topik]
      • Langkah 3: [Sesuaikan dengan topik]
      
   C. ANALISA BIAYA
      • Perbandingan biaya solusi
      • Efisiensi vs hasil
      • Contoh perhitungan sederhana

📍 3. SESI DISKUSI - 10-15 menit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✦ Pertanyaan Pemancing:
     "Siapa yang lahannya sudah mengalami [masalah]?"
     "Apa yang sudah dicoba untuk mengatasinya?"
   
   ✦ Tips: Beri hadiah kecil untuk penanya aktif
   
   ✦ Catat pertanyaan untuk follow-up

📍 4. KESIMPULAN & RTL - 5 menit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✦ Rangkuman 3 poin utama
   ✦ Jadwal praktek lapangan: [tentukan bersama]
   ✦ Salam penutup & yel-yel pertanian

═══════════════════════════════════════════════════
💡 TIPS PPL:
   • Gunakan bahasa daerah setempat
   • Bawa contoh nyata (foto smartphone/sampel)
   • Libatkan ketua poktan dalam penyampaian
   • Dokumentasikan dengan foto untuk laporan
═══════════════════════════════════════════════════
"""
            
            st.text_area("📋 Materi Penyuluhan", value=materi_text, height=600, key="materi_output")
            
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                st.download_button("📥 Download Materi (TXT)", data=materi_text,
                                  file_name=f"Materi_Penyuluhan_{topik.replace(' ', '_')}.txt")
        else:
            st.error("Mohon isi topik penyuluhan terlebih dulu.")

# ========== FOOTER ==========
st.markdown("---")
st.caption("🌾 AgriSensa PPL Tools v2.0 - Sistem Pendukung Keputusan untuk Pahlawan Pangan Indonesia 🇮🇩")
