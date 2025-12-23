import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(page_title="Manajemen Proyek Pertanian - AgriSensa", page_icon="📋", layout="wide")

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================

if 'projects' not in st.session_state:
    st.session_state.projects = []

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'team_members' not in st.session_state:
    st.session_state.team_members = []

if 'expenses' not in st.session_state:
    st.session_state.expenses = []

if 'activities' not in st.session_state:
    st.session_state.activities = []

if 'active_project_id' not in st.session_state:
    st.session_state.active_project_id = None

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def create_project(name, crop_type, area_hectare, start_date, end_date, budget_total):
    """Create new project"""
    project = {
        "id": str(uuid.uuid4()),
        "name": name,
        "crop_type": crop_type,
        "area_hectare": area_hectare,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d"),
        "status": "active",
        "budget_total": budget_total,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.projects.append(project)
    st.session_state.active_project_id = project["id"]
    return project

def get_active_project():
    """Get currently active project"""
    if st.session_state.active_project_id:
        for project in st.session_state.projects:
            if project["id"] == st.session_state.active_project_id:
                return project
    return None

def get_project_tasks(project_id):
    """Get all tasks for a project"""
    return [task for task in st.session_state.tasks if task["project_id"] == project_id]

def get_project_expenses(project_id):
    """Get all expenses for a project"""
    return [expense for expense in st.session_state.expenses if expense["project_id"] == project_id]

def calculate_project_stats(project_id):
    """Calculate project statistics"""
    tasks = get_project_tasks(project_id)
    expenses = get_project_expenses(project_id)
    
    total_tasks = len(tasks)
    completed_tasks = len([t for t in tasks if t["status"] == "done"])
    in_progress_tasks = len([t for t in tasks if t["status"] == "in_progress"])
    
    total_expenses = sum([e["amount"] for e in expenses])
    
    project = get_active_project()
    budget_remaining = project["budget_total"] - total_expenses if project else 0
    
    progress_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "in_progress_tasks": in_progress_tasks,
        "progress_pct": progress_pct,
        "total_expenses": total_expenses,
        "budget_remaining": budget_remaining
    }

# ==========================================
# HEADER
# ==========================================

st.title("📋 Manajemen Proyek Pertanian")
st.markdown("**Kelola proyek pertanian Anda secara profesional**")
st.info("💡 Sistem manajemen proyek berbasis pengalaman nyata mengelola proyek cabai 2 hektar dan proyek komersial lainnya")

# ==========================================
# SIDEBAR - PROJECT SELECTOR
# ==========================================

st.sidebar.title("🎯 Proyek Aktif")

if st.session_state.projects:
    project_names = [f"{p['name']} ({p['crop_type']})" for p in st.session_state.projects]
    selected_idx = st.sidebar.selectbox(
        "Pilih Proyek",
        range(len(st.session_state.projects)),
        format_func=lambda x: project_names[x]
    )
    st.session_state.active_project_id = st.session_state.projects[selected_idx]["id"]
else:
    st.sidebar.info("Belum ada proyek. Buat proyek baru di bawah!")

st.sidebar.divider()

# Quick stats in sidebar
active_project = get_active_project()
if active_project:
    stats = calculate_project_stats(active_project["id"])
    st.sidebar.metric("Progress", f"{stats['progress_pct']:.0f}%")
    st.sidebar.metric("Tasks Selesai", f"{stats['completed_tasks']}/{stats['total_tasks']}")
    st.sidebar.metric("Budget Tersisa", f"Rp {stats['budget_remaining']:,.0f}")

# ==========================================
# MAIN CONTENT
# ==========================================

# If no projects, show create project form
if not st.session_state.projects or st.sidebar.button("➕ Buat Proyek Baru", use_container_width=True):
    st.header("🌱 Buat Proyek Baru")
    
    with st.form("create_project_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Nama Proyek", placeholder="e.g., Cabai Merah Musim 1")
            crop_type = st.selectbox("Jenis Tanaman", [
                "Cabai", "Tomat", "Terong", "Bawang Merah", "Bawang Putih",
                "Kentang", "Wortel", "Jagung", "Padi", "Kedelai", "Lainnya"
            ])
            area_hectare = st.number_input("Luas Lahan (hektar)", min_value=0.1, max_value=1000.0, value=1.0, step=0.1)
        
        with col2:
            start_date = st.date_input("Tanggal Mulai", datetime.now())
            end_date = st.date_input("Tanggal Target Selesai", datetime.now() + timedelta(days=120))
            budget_total = st.number_input("Total Budget (Rp)", min_value=0, value=10000000, step=1000000)
        
        submitted = st.form_submit_button("🚀 Buat Proyek", use_container_width=True, type="primary")
        
        if submitted:
            if project_name:
                create_project(project_name, crop_type, area_hectare, start_date, end_date, budget_total)
                st.success(f"✅ Proyek '{project_name}' berhasil dibuat!")
                st.rerun()
            else:
                st.error("Nama proyek harus diisi!")

# If project exists, show project management interface
elif active_project:
    
    # Project Header
    col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
    
    with col_h1:
        st.header(f"🌾 {active_project['name']}")
        st.caption(f"{active_project['crop_type']} | {active_project['area_hectare']} ha | {active_project['start_date']} - {active_project['end_date']}")
    
    with col_h2:
        if st.button("⚙️ Edit Proyek", use_container_width=True):
            st.session_state.show_edit_project = True
    
    with col_h3:
        if st.button("🗑️ Hapus Proyek", type="secondary", use_container_width=True):
            st.session_state.show_delete_confirm = True
    
    # Edit Project Dialog
    if st.session_state.get('show_edit_project', False):
        st.divider()
        st.subheader("⚙️ Edit Proyek")
        
        with st.form("edit_project_form"):
            col_e1, col_e2 = st.columns(2)
            
            with col_e1:
                edit_name = st.text_input("Nama Proyek", value=active_project['name'])
                edit_crop = st.selectbox("Jenis Tanaman", 
                    ["Cabai", "Tomat", "Terong", "Bawang Merah", "Bawang Putih",
                     "Kentang", "Wortel", "Jagung", "Padi", "Kedelai", "Lainnya"],
                    index=["Cabai", "Tomat", "Terong", "Bawang Merah", "Bawang Putih",
                           "Kentang", "Wortel", "Jagung", "Padi", "Kedelai", "Lainnya"].index(active_project['crop_type']) 
                           if active_project['crop_type'] in ["Cabai", "Tomat", "Terong", "Bawang Merah", "Bawang Putih",
                                                               "Kentang", "Wortel", "Jagung", "Padi", "Kedelai", "Lainnya"] else 0
                )
                edit_area = st.number_input("Luas Lahan (hektar)", min_value=0.1, max_value=1000.0, 
                                           value=float(active_project['area_hectare']), step=0.1)
            
            with col_e2:
                edit_start = st.date_input("Tanggal Mulai", 
                                          value=datetime.strptime(active_project['start_date'], "%Y-%m-%d"))
                edit_end = st.date_input("Tanggal Target Selesai",
                                        value=datetime.strptime(active_project['end_date'], "%Y-%m-%d"))
                edit_budget = st.number_input("Total Budget (Rp)", min_value=0, 
                                             value=int(active_project['budget_total']), step=1000000)
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.form_submit_button("💾 Simpan Perubahan", type="primary", use_container_width=True):
                    # Update project
                    active_project['name'] = edit_name
                    active_project['crop_type'] = edit_crop
                    active_project['area_hectare'] = edit_area
                    active_project['start_date'] = edit_start.strftime("%Y-%m-%d")
                    active_project['end_date'] = edit_end.strftime("%Y-%m-%d")
                    active_project['budget_total'] = edit_budget
                    
                    st.session_state.show_edit_project = False
                    st.success("✅ Proyek berhasil diupdate!")
                    st.rerun()
            
            with col_btn2:
                if st.form_submit_button("❌ Batal", use_container_width=True):
                    st.session_state.show_edit_project = False
                    st.rerun()
        
        st.divider()
    
    # Delete Confirmation Dialog
    if st.session_state.get('show_delete_confirm', False):
        st.divider()
        st.warning(f"⚠️ **Konfirmasi Hapus Proyek**")
        st.markdown(f"Apakah Anda yakin ingin menghapus proyek **{active_project['name']}**?")
        st.error("⚠️ Semua data tasks, expenses, dan activities akan ikut terhapus!")
        
        col_del1, col_del2 = st.columns(2)
        
        with col_del1:
            if st.button("🗑️ Ya, Hapus Proyek", type="primary", use_container_width=True):
                project_id = active_project['id']
                
                # Remove project
                st.session_state.projects = [p for p in st.session_state.projects if p['id'] != project_id]
                
                # Remove related tasks
                st.session_state.tasks = [t for t in st.session_state.tasks if t['project_id'] != project_id]
                
                # Remove related expenses
                st.session_state.expenses = [e for e in st.session_state.expenses if e['project_id'] != project_id]
                
                # Remove related activities
                st.session_state.activities = [a for a in st.session_state.activities if a['project_id'] != project_id]
                
                # Reset active project
                st.session_state.active_project_id = None
                st.session_state.show_delete_confirm = False
                
                st.success("✅ Proyek berhasil dihapus!")
                st.rerun()
        
        with col_del2:
            if st.button("❌ Batal", use_container_width=True):
                st.session_state.show_delete_confirm = False
                st.rerun()
        
        st.divider()
    
    st.divider()
    
    # KPI Dashboard
    stats = calculate_project_stats(active_project["id"])
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        st.metric("📊 Progress", f"{stats['progress_pct']:.0f}%", 
                 delta=f"{stats['completed_tasks']} dari {stats['total_tasks']} tasks")
    
    with col_kpi2:
        st.metric("✅ Tasks Selesai", stats['completed_tasks'])
    
    with col_kpi3:
        budget_used_pct = (stats['total_expenses'] / active_project['budget_total'] * 100) if active_project['budget_total'] > 0 else 0
        st.metric("💰 Budget Terpakai", f"{budget_used_pct:.0f}%",
                 delta=f"Rp {stats['total_expenses']:,.0f}")
    
    with col_kpi4:
        st.metric("💵 Budget Tersisa", f"Rp {stats['budget_remaining']:,.0f}")
    
    st.divider()
    
    # Tabs for different sections
    tab_tasks, tab_team, tab_budget, tab_timeline, tab_reports = st.tabs([
        "✅ Tasks & Kanban",
        "👥 Tim",
        "💰 Budget & Biaya",
        "📅 Timeline",
        "📊 Laporan"
    ])
    
    # ========== TAB: TASKS & KANBAN ==========
    with tab_tasks:
        st.subheader("📋 Manajemen Tasks")
        
        # Add new task
        with st.expander("➕ Tambah Task Baru"):
            with st.form("add_task_form"):
                col_t1, col_t2 = st.columns(2)
                
                with col_t1:
                    task_title = st.text_input("Judul Task", placeholder="e.g., Persiapan Lahan")
                    task_desc = st.text_area("Deskripsi", placeholder="Detail pekerjaan...")
                    task_assignee = st.selectbox("Assign ke", 
                                                ["Belum ditentukan"] + [tm["name"] for tm in st.session_state.team_members])
                
                with col_t2:
                    task_priority = st.selectbox("Prioritas", ["Low", "Medium", "High"])
                    task_due_date = st.date_input("Deadline", datetime.now() + timedelta(days=7))
                    task_status = st.selectbox("Status", ["to_do", "in_progress", "done"])
                
                if st.form_submit_button("➕ Tambah Task", type="primary"):
                    if task_title:
                        new_task = {
                            "id": str(uuid.uuid4()),
                            "project_id": active_project["id"],
                            "title": task_title,
                            "description": task_desc,
                            "assignee": task_assignee if task_assignee != "Belum ditentukan" else None,
                            "status": task_status,
                            "priority": task_priority,
                            "due_date": task_due_date.strftime("%Y-%m-%d"),
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "completed_at": None
                        }
                        st.session_state.tasks.append(new_task)
                        st.success("✅ Task berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("Judul task harus diisi!")
        
        st.divider()
        
        # Kanban Board
        st.markdown("### 📊 Kanban Board")
        
        project_tasks = get_project_tasks(active_project["id"])
        
        col_todo, col_progress, col_done = st.columns(3)
        
        with col_todo:
            st.markdown("#### 📝 To Do")
            todo_tasks = [t for t in project_tasks if t["status"] == "to_do"]
            
            if todo_tasks:
                for task in todo_tasks:
                    with st.container():
                        st.markdown(f"**{task['title']}**")
                        st.caption(f"🎯 {task['priority']} | 📅 {task['due_date']}")
                        if task['assignee']:
                            st.caption(f"👤 {task['assignee']}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("▶️ Start", key=f"start_{task['id']}", use_container_width=True):
                                task['status'] = "in_progress"
                                st.rerun()
                        with col_btn2:
                            if st.button("🗑️", key=f"del_{task['id']}", use_container_width=True):
                                st.session_state.tasks.remove(task)
                                st.rerun()
                        st.divider()
            else:
                st.info("Tidak ada task")
        
        with col_progress:
            st.markdown("#### 🔄 In Progress")
            progress_tasks = [t for t in project_tasks if t["status"] == "in_progress"]
            
            if progress_tasks:
                for task in progress_tasks:
                    with st.container():
                        st.markdown(f"**{task['title']}**")
                        st.caption(f"🎯 {task['priority']} | 📅 {task['due_date']}")
                        if task['assignee']:
                            st.caption(f"👤 {task['assignee']}")
                        
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("✅ Done", key=f"done_{task['id']}", use_container_width=True):
                                task['status'] = "done"
                                task['completed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                st.rerun()
                        with col_btn2:
                            if st.button("⏸️ Pause", key=f"pause_{task['id']}", use_container_width=True):
                                task['status'] = "to_do"
                                st.rerun()
                        st.divider()
            else:
                st.info("Tidak ada task")
        
        with col_done:
            st.markdown("#### ✅ Done")
            done_tasks = [t for t in project_tasks if t["status"] == "done"]
            
            if done_tasks:
                for task in done_tasks:
                    with st.container():
                        st.markdown(f"**{task['title']}**")
                        st.caption(f"✅ Selesai: {task.get('completed_at', 'N/A')}")
                        if task['assignee']:
                            st.caption(f"👤 {task['assignee']}")
                        st.divider()
            else:
                st.info("Tidak ada task")
    
    # ========== TAB: TEAM ==========
    with tab_team:
        st.subheader("👥 Manajemen Tim")
        
        # Add team member
        with st.expander("➕ Tambah Anggota Tim"):
            with st.form("add_team_form"):
                col_tm1, col_tm2 = st.columns(2)
                
                with col_tm1:
                    member_name = st.text_input("Nama")
                    member_role = st.selectbox("Role", ["Manager", "Supervisor", "Worker", "Specialist"])
                
                with col_tm2:
                    member_contact = st.text_input("Kontak (HP/Email)")
                
                if st.form_submit_button("➕ Tambah Anggota", type="primary"):
                    if member_name:
                        new_member = {
                            "id": str(uuid.uuid4()),
                            "name": member_name,
                            "role": member_role,
                            "contact": member_contact,
                            "joined_at": datetime.now().strftime("%Y-%m-%d")
                        }
                        st.session_state.team_members.append(new_member)
                        st.success(f"✅ {member_name} berhasil ditambahkan!")
                        st.rerun()
                    else:
                        st.error("Nama harus diisi!")
        
        st.divider()
        
        # Team list
        if st.session_state.team_members:
            team_data = []
            for member in st.session_state.team_members:
                # Count tasks assigned
                member_tasks = [t for t in get_project_tasks(active_project["id"]) if t.get("assignee") == member["name"]]
                tasks_assigned = len(member_tasks)
                tasks_completed = len([t for t in member_tasks if t["status"] == "done"])
                
                team_data.append({
                    "Nama": member["name"],
                    "Role": member["role"],
                    "Kontak": member["contact"],
                    "Tasks Assigned": tasks_assigned,
                    "Tasks Completed": tasks_completed,
                    "Completion Rate": f"{(tasks_completed/tasks_assigned*100):.0f}%" if tasks_assigned > 0 else "0%"
                })
            
            df_team = pd.DataFrame(team_data)
            st.dataframe(df_team, use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada anggota tim. Tambahkan anggota tim di atas!")
    
    # ========== TAB: BUDGET ==========
    with tab_budget:
        st.subheader("💰 Budget & Pengeluaran")
        
        col_b1, col_b2 = st.columns([1, 1])
        
        with col_b1:
            st.markdown("#### 📊 Ringkasan Budget")
            st.metric("Total Budget", f"Rp {active_project['budget_total']:,.0f}")
            st.metric("Total Pengeluaran", f"Rp {stats['total_expenses']:,.0f}")
            st.metric("Sisa Budget", f"Rp {stats['budget_remaining']:,.0f}")
            
            # Budget usage chart
            if stats['total_expenses'] > 0:
                fig_budget = go.Figure(data=[go.Pie(
                    labels=['Terpakai', 'Tersisa'],
                    values=[stats['total_expenses'], stats['budget_remaining']],
                    hole=0.4
                )])
                fig_budget.update_layout(title="Penggunaan Budget")
                st.plotly_chart(fig_budget, use_container_width=True)
        
        with col_b2:
            st.markdown("#### ➕ Catat Pengeluaran")
            
            with st.form("add_expense_form"):
                expense_category = st.selectbox("Kategori", [
                    "Benih/Bibit", "Pupuk", "Pestisida", "Tenaga Kerja",
                    "Sewa Alat", "Transportasi", "Lain-lain"
                ])
                expense_desc = st.text_input("Deskripsi", placeholder="e.g., NPK 15-15-15 50kg")
                expense_amount = st.number_input("Jumlah (Rp)", min_value=0, value=0, step=10000)
                expense_date = st.date_input("Tanggal", datetime.now())
                
                if st.form_submit_button("💰 Catat Pengeluaran", type="primary"):
                    if expense_amount > 0:
                        new_expense = {
                            "id": str(uuid.uuid4()),
                            "project_id": active_project["id"],
                            "category": expense_category,
                            "description": expense_desc,
                            "amount": expense_amount,
                            "date": expense_date.strftime("%Y-%m-%d"),
                            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        st.session_state.expenses.append(new_expense)
                        st.success("✅ Pengeluaran berhasil dicatat!")
                        st.rerun()
                    else:
                        st.error("Jumlah harus lebih dari 0!")
        
        st.divider()
        
        # Expense list
        st.markdown("#### 📋 Riwayat Pengeluaran")
        
        project_expenses = get_project_expenses(active_project["id"])
        
        if project_expenses:
            expense_data = [{
                "Tanggal": e["date"],
                "Kategori": e["category"],
                "Deskripsi": e["description"],
                "Jumlah (Rp)": f"{e['amount']:,.0f}"
            } for e in sorted(project_expenses, key=lambda x: x["date"], reverse=True)]
            
            df_expenses = pd.DataFrame(expense_data)
            st.dataframe(df_expenses, use_container_width=True, hide_index=True)
            
            # Expense by category chart
            expense_by_cat = {}
            for e in project_expenses:
                expense_by_cat[e["category"]] = expense_by_cat.get(e["category"], 0) + e["amount"]
            
            fig_cat = px.bar(
                x=list(expense_by_cat.keys()),
                y=list(expense_by_cat.values()),
                title="Pengeluaran per Kategori",
                labels={"x": "Kategori", "y": "Jumlah (Rp)"}
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("Belum ada pengeluaran tercatat")
    
    # ========== TAB: TIMELINE ==========
    with tab_timeline:
        st.subheader("📅 Timeline Proyek")
        
        st.info("🚧 Timeline visualization (Gantt chart) akan ditambahkan di fase berikutnya")
        
        # Show project duration
        start = datetime.strptime(active_project["start_date"], "%Y-%m-%d")
        end = datetime.strptime(active_project["end_date"], "%Y-%m-%d")
        duration_days = (end - start).days
        days_elapsed = (datetime.now() - start).days
        days_remaining = (end - datetime.now()).days
        
        col_tl1, col_tl2, col_tl3 = st.columns(3)
        
        with col_tl1:
            st.metric("Durasi Total", f"{duration_days} hari")
        
        with col_tl2:
            st.metric("Hari Berjalan", f"{days_elapsed} hari")
        
        with col_tl3:
            st.metric("Sisa Waktu", f"{days_remaining} hari")
        
        # Progress bar
        time_progress = (days_elapsed / duration_days * 100) if duration_days > 0 else 0
        st.progress(min(time_progress / 100, 1.0))
        st.caption(f"Progress waktu: {time_progress:.0f}%")
    
    # ========== TAB: REPORTS ==========
    with tab_reports:
        st.subheader("📊 Laporan & Analisis")
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.markdown("#### 📈 Ringkasan Proyek")
            
            summary_data = {
                "Metrik": [
                    "Nama Proyek",
                    "Jenis Tanaman",
                    "Luas Lahan",
                    "Periode",
                    "Total Budget",
                    "Total Pengeluaran",
                    "Sisa Budget",
                    "Total Tasks",
                    "Tasks Selesai",
                    "Progress"
                ],
                "Nilai": [
                    active_project["name"],
                    active_project["crop_type"],
                    f"{active_project['area_hectare']} ha",
                    f"{active_project['start_date']} s/d {active_project['end_date']}",
                    f"Rp {active_project['budget_total']:,.0f}",
                    f"Rp {stats['total_expenses']:,.0f}",
                    f"Rp {stats['budget_remaining']:,.0f}",
                    stats['total_tasks'],
                    stats['completed_tasks'],
                    f"{stats['progress_pct']:.0f}%"
                ]
            }
            
            df_summary = pd.DataFrame(summary_data)
            st.dataframe(df_summary, use_container_width=True, hide_index=True)
        
        with col_r2:
            st.markdown("#### 📥 Export Data")
            
            st.info("Export ke PDF/Excel akan ditambahkan di fase berikutnya")
            
            # Simple CSV export for now
            if st.button("📥 Download Tasks (CSV)", use_container_width=True):
                tasks_df = pd.DataFrame(get_project_tasks(active_project["id"]))
                csv = tasks_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download CSV",
                    csv,
                    f"tasks_{active_project['name']}.csv",
                    "text/csv"
                )
            
            if st.button("📥 Download Expenses (CSV)", use_container_width=True):
                expenses_df = pd.DataFrame(get_project_expenses(active_project["id"]))
                csv = expenses_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "Download CSV",
                    csv,
                    f"expenses_{active_project['name']}.csv",
                    "text/csv"
                )

# ==========================================
# FOOTER
# ==========================================

st.divider()
st.caption("💡 Farm Project Management - Based on real-world experience managing 2-hectare chili project and commercial farming operations")
