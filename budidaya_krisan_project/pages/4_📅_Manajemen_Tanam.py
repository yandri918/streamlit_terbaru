import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Manajemen Tanam", page_icon="📅", layout="wide")

# Custom CSS
st.markdown("""
<style>
.status-tanam { background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; text-align: center; }
.status-vegetatif { background: linear-gradient(135deg, #84cc16, #65a30d); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; text-align: center; }
.status-generatif { background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; text-align: center; }
.status-panen { background: linear-gradient(135deg, #ef4444, #dc2626); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; text-align: center; }
.status-jeda { background: linear-gradient(135deg, #6b7280, #4b5563); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; text-align: center; }
.sync-badge { background: linear-gradient(135deg, #1e3a5f, #2d5a87); color: white; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; }
.timeline-card { background: white; border: 1px solid #e5e7eb; border-radius: 0.5rem; padding: 1rem; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📅 Manajemen Tanam & Panen Mingguan")
st.info("Sistem rotasi tanam mingguan dengan panen bertahap dan persiapan lahan terjadwal")

# Initialize session state
if 'planting_schedule' not in st.session_state:
    st.session_state.planting_schedule = []

if 'harvest_sessions' not in st.session_state:
    st.session_state.harvest_sessions = []

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📅 Jadwal Tanam",
    "🌾 Jadwal Panen", 
    "🚜 Persiapan Lahan",
    "📊 Overview",
    "🧮 Kalkulator House"
])

# ==================== TAB 1: JADWAL TANAM ====================
with tab1:
    st.subheader("📅 Penjadwalan Tanam Mingguan")
    
    col_setup, col_timeline = st.columns([1, 1.5])
    
    with col_setup:
        st.markdown("### ⚙️ Konfigurasi Siklus")
        
        # Get house list - priority: house_database > house_list > default
        if 'house_database' in st.session_state and st.session_state.house_database:
            house_options = [data['name'] for key, data in st.session_state.house_database.items()]
        elif 'house_list' in st.session_state:
            house_options = st.session_state.house_list
        else:
            # Initialize house_list if not exists
            st.session_state.house_list = ["House 1", "House 2", "House 3", "House 4"]
            house_options = st.session_state.house_list
        
        house_name = st.selectbox(
            "🏠 Pilih House",
            house_options,
            key="plant_house"
        )
        
        # Option to add new house
        with st.expander("➕ Tambah House Baru"):
            new_house = st.text_input("Nama House Baru", key="add_house_mgt")
            if st.button("Tambah House", key="btn_add_house_mgt"):
                if new_house:
                    if 'house_list' not in st.session_state:
                        st.session_state.house_list = list(house_options)
                    if new_house not in st.session_state.house_list:
                        st.session_state.house_list.append(new_house)
                        st.success(f"✅ {new_house} ditambahkan!")
                        st.rerun()
        
        num_beds_group = st.number_input(
            "📦 Jumlah Bedengan dalam House",
            min_value=1, max_value=20, value=12,
            help="Jumlah bedengan dalam satu house (ditanam bersamaan)"
        )
        
        st.markdown("#### ⏱️ Durasi Fase (hari)")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            days_vegetatif = st.number_input("🌱 Vegetatif", 21, 42, 35, help="~5 minggu")
            days_generatif = st.number_input("🌸 Generatif", 42, 70, 56, help="~8 minggu")
        with col_d2:
            days_harvest = st.number_input("🌾 Periode Panen", 7, 14, 10)
            days_jeda = st.number_input("🚜 Jeda Lahan", 10, 21, 14, help="~2 minggu")
        
        total_cycle = days_vegetatif + days_generatif + days_harvest + days_jeda
        st.metric("📊 Total Siklus", f"{total_cycle} hari", f"~{total_cycle/30:.1f} bulan")
        
        st.markdown("---")
        
        st.markdown("### 📆 Tambah Jadwal Tanam")
        
        planting_date = st.date_input("📅 Tanggal Tanam", value=datetime.now().date())
        bed_ids = st.text_input(
            "📝 ID Bedengan (pisah koma)",
            placeholder="B1, B2, B3",
            help="Contoh: B1, B2, B3"
        )
        
        if st.button("✅ Tambah ke Jadwal", type="primary", use_container_width=True):
            if bed_ids:
                beds = [b.strip() for b in bed_ids.split(",")]
                
                for bed in beds:
                    # Calculate dates
                    harvest_start = planting_date + timedelta(days=days_vegetatif + days_generatif)
                    harvest_end = harvest_start + timedelta(days=days_harvest)
                    clearing_start = harvest_end + timedelta(days=1)
                    next_planting = clearing_start + timedelta(days=days_jeda)
                    
                    schedule_entry = {
                        "house": house_name,
                        "bed_id": f"{house_name[:2]}-{bed}",
                        "planting_date": planting_date.strftime("%Y-%m-%d"),
                        "harvest_start": harvest_start.strftime("%Y-%m-%d"),
                        "harvest_end": harvest_end.strftime("%Y-%m-%d"),
                        "clearing_start": clearing_start.strftime("%Y-%m-%d"),
                        "next_planting": next_planting.strftime("%Y-%m-%d"),
                        "days_vegetatif": days_vegetatif,
                        "days_generatif": days_generatif,
                        "days_harvest": days_harvest,
                        "days_jeda": days_jeda,
                        "status": "vegetatif"
                    }
                    st.session_state.planting_schedule.append(schedule_entry)
                
                st.success(f"✅ {len(beds)} bedengan ditambahkan ke jadwal!")
                st.rerun()
    
    with col_timeline:
        st.markdown("### 📋 Jadwal Aktif")
        
        if st.session_state.planting_schedule:
            # Update status based on current date
            today = datetime.now().date()
            
            for entry in st.session_state.planting_schedule:
                plant_date = datetime.strptime(entry['planting_date'], "%Y-%m-%d").date()
                harvest_start = datetime.strptime(entry['harvest_start'], "%Y-%m-%d").date()
                harvest_end = datetime.strptime(entry['harvest_end'], "%Y-%m-%d").date()
                clearing_start = datetime.strptime(entry['clearing_start'], "%Y-%m-%d").date()
                next_planting = datetime.strptime(entry['next_planting'], "%Y-%m-%d").date()
                
                veg_end = plant_date + timedelta(days=entry['days_vegetatif'])
                
                if today < plant_date:
                    entry['status'] = "belum tanam"
                elif today < veg_end:
                    entry['status'] = "vegetatif"
                elif today < harvest_start:
                    entry['status'] = "generatif"
                elif today <= harvest_end:
                    entry['status'] = "panen"
                elif today < next_planting:
                    entry['status'] = "jeda"
                else:
                    entry['status'] = "selesai"
            
            df_schedule = pd.DataFrame(st.session_state.planting_schedule)
            
            # Filter by house
            filter_house = st.selectbox("Filter House:", ["Semua"] + list(df_schedule['house'].unique()))
            
            if filter_house != "Semua":
                df_schedule = df_schedule[df_schedule['house'] == filter_house]
            
            # Display table
            display_df = df_schedule[['house', 'bed_id', 'planting_date', 'harvest_start', 'harvest_end', 'status']].copy()
            display_df.columns = ['House', 'Bedengan', 'Tanam', 'Panen Mulai', 'Panen Selesai', 'Status']
            
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            # Status summary
            st.markdown("#### 📊 Status Summary")
            status_counts = df_schedule['status'].value_counts()
            
            status_cols = st.columns(5)
            status_colors = {
                'vegetatif': '🌱',
                'generatif': '🌸',
                'panen': '🌾',
                'jeda': '🚜',
                'selesai': '✅'
            }
            
            for i, (status, count) in enumerate(status_counts.items()):
                if i < 5:
                    with status_cols[i]:
                        emoji = status_colors.get(status, '📋')
                        st.metric(f"{emoji} {status.title()}", count)
            
            # Clear button
            if st.button("🗑️ Hapus Semua Jadwal"):
                st.session_state.planting_schedule = []
                st.rerun()
        else:
            st.info("📝 Belum ada jadwal tanam. Tambahkan di panel kiri.")

# ==================== TAB 2: JADWAL PANEN ====================
with tab2:
    st.subheader("🌾 Jadwal Panen Bertahap")
    
    if st.session_state.planting_schedule:
        today = datetime.now().date()
        
        # Filter beds ready for harvest or in harvest period
        harvest_beds = []
        for entry in st.session_state.planting_schedule:
            harvest_start = datetime.strptime(entry['harvest_start'], "%Y-%m-%d").date()
            harvest_end = datetime.strptime(entry['harvest_end'], "%Y-%m-%d").date()
            
            if harvest_start <= today <= harvest_end:
                days_left = (harvest_end - today).days
                harvest_beds.append({**entry, 'days_left': days_left})
            elif today < harvest_start:
                days_until = (harvest_start - today).days
                if days_until <= 7:
                    harvest_beds.append({**entry, 'days_until': days_until, 'status': 'siap panen'})
        
        if harvest_beds:
            st.markdown("### 🌾 Bedengan dalam Periode Panen")
            
            col_harv1, col_harv2 = st.columns([2, 1])
            
            with col_harv1:
                df_harvest = pd.DataFrame(harvest_beds)
                st.dataframe(df_harvest[['house', 'bed_id', 'harvest_start', 'harvest_end', 'status']], 
                            use_container_width=True, hide_index=True)
            
            with col_harv2:
                st.markdown("#### ⚙️ Pengaturan Panen")
                
                harvest_freq = st.radio(
                    "Frekuensi Panen:",
                    ["Setiap Hari", "2 Hari Sekali"],
                    horizontal=True
                )
                
                stems_per_session = st.number_input(
                    "Est. Batang per Sesi",
                    min_value=100, max_value=5000, value=500, step=100
                )
                
                st.markdown("---")
                st.markdown("#### 📅 Jadwal Panen Hari Ini")
                
                if st.button("📝 Catat Sesi Panen", type="primary"):
                    session = {
                        "date": today.strftime("%Y-%m-%d"),
                        "beds": [b['bed_id'] for b in harvest_beds if b.get('status') == 'panen'],
                        "stems": stems_per_session,
                        "time": datetime.now().strftime("%H:%M")
                    }
                    st.session_state.harvest_sessions.append(session)
                    st.success("✅ Sesi panen dicatat!")
        else:
            # Show upcoming harvests
            st.info("📅 Tidak ada bedengan dalam periode panen saat ini.")
            
            upcoming = []
            for entry in st.session_state.planting_schedule:
                harvest_start = datetime.strptime(entry['harvest_start'], "%Y-%m-%d").date()
                if harvest_start > today:
                    days_until = (harvest_start - today).days
                    upcoming.append({**entry, 'days_until': days_until})
            
            if upcoming:
                upcoming_sorted = sorted(upcoming, key=lambda x: x['days_until'])[:5]
                st.markdown("### 📆 Panen Mendatang")
                
                for u in upcoming_sorted:
                    st.markdown(f"- **{u['bed_id']}** ({u['house']}): {u['days_until']} hari lagi ({u['harvest_start']})")
        
        # Harvest history
        st.markdown("---")
        st.markdown("### 📋 Riwayat Panen")
        
        if st.session_state.harvest_sessions:
            df_sessions = pd.DataFrame(st.session_state.harvest_sessions)
            st.dataframe(df_sessions, use_container_width=True, hide_index=True)
            
            total_harvested = sum(s['stems'] for s in st.session_state.harvest_sessions)
            st.metric("🌸 Total Panen", f"{total_harvested:,} batang")
        else:
            st.info("📝 Belum ada riwayat panen.")
    else:
        st.info("📝 Tambahkan jadwal tanam terlebih dahulu di Tab Jadwal Tanam.")

# ==================== TAB 3: PERSIAPAN LAHAN ====================
with tab3:
    st.subheader("🚜 Persiapan Lahan & Rotasi")
    
    if st.session_state.planting_schedule:
        today = datetime.now().date()
        
        # Find beds in jeda period
        jeda_beds = []
        for entry in st.session_state.planting_schedule:
            clearing_start = datetime.strptime(entry['clearing_start'], "%Y-%m-%d").date()
            next_planting = datetime.strptime(entry['next_planting'], "%Y-%m-%d").date()
            
            if clearing_start <= today < next_planting:
                days_in_jeda = (today - clearing_start).days
                days_left = (next_planting - today).days
                jeda_beds.append({
                    **entry, 
                    'days_in_jeda': days_in_jeda,
                    'days_left': days_left,
                    'progress': min(100, (days_in_jeda / entry['days_jeda']) * 100)
                })
        
        if jeda_beds:
            st.markdown("### 🔄 Bedengan dalam Periode Jeda")
            
            for bed in jeda_beds:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{bed['bed_id']}** ({bed['house']})")
                    
                    # Timeline progress
                    progress = bed['progress']
                    
                    # Determine current phase
                    if bed['days_in_jeda'] <= 3:
                        phase = "🔨 Bongkar & Bajak"
                    elif bed['days_in_jeda'] <= 10:
                        phase = "🧪 Fermentasi & Disinfektansi"
                    else:
                        phase = "📐 Pembuatan Bedengan"
                    
                    st.progress(progress / 100)
                    st.caption(f"Fase: {phase} | {bed['days_left']} hari menuju tanam")
                
                with col2:
                    st.metric("Tanam Ulang", bed['next_planting'])
                
                st.markdown("---")
        
        # Timeline explanation
        st.markdown("### 📋 Timeline Persiapan Lahan (Default 14 Hari)")
        
        timeline_data = pd.DataFrame({
            "Fase": ["🔨 Bongkar & Bajak", "🧪 Fermentasi", "📐 Bedengan Baru"],
            "Hari ke": ["1-3", "4-10", "11-14"],
            "Durasi": ["3 hari", "7 hari", "4 hari"],
            "Keterangan": ["Cabut tanaman, bajak tanah", "Pupuk kandang, disinfektansi", "Buat bedengan, siap tanam"]
        })
        
        st.dataframe(timeline_data, use_container_width=True, hide_index=True)
    else:
        st.info("📝 Tambahkan jadwal tanam terlebih dahulu.")

# ==================== TAB 4: OVERVIEW DASHBOARD ====================
with tab4:
    st.subheader("📊 Overview Dashboard")
    
    if st.session_state.planting_schedule:
        # Gantt chart
        st.markdown("### 📊 Timeline Gantt Chart")
        
        gantt_data = []
        
        for entry in st.session_state.planting_schedule:
            plant_date = datetime.strptime(entry['planting_date'], "%Y-%m-%d")
            veg_end = plant_date + timedelta(days=entry['days_vegetatif'])
            gen_end = veg_end + timedelta(days=entry['days_generatif'])
            harvest_start = datetime.strptime(entry['harvest_start'], "%Y-%m-%d")
            harvest_end = datetime.strptime(entry['harvest_end'], "%Y-%m-%d")
            next_planting = datetime.strptime(entry['next_planting'], "%Y-%m-%d")
            
            # Vegetatif
            gantt_data.append({
                "Bedengan": entry['bed_id'],
                "Fase": "Vegetatif",
                "Start": plant_date,
                "Finish": veg_end
            })
            
            # Generatif
            gantt_data.append({
                "Bedengan": entry['bed_id'],
                "Fase": "Generatif",
                "Start": veg_end,
                "Finish": gen_end
            })
            
            # Panen
            gantt_data.append({
                "Bedengan": entry['bed_id'],
                "Fase": "Panen",
                "Start": harvest_start,
                "Finish": harvest_end
            })
            
            # Jeda
            gantt_data.append({
                "Bedengan": entry['bed_id'],
                "Fase": "Jeda Lahan",
                "Start": harvest_end,
                "Finish": next_planting
            })
        
        df_gantt = pd.DataFrame(gantt_data)
        
        color_map = {
            "Vegetatif": "#84cc16",
            "Generatif": "#f59e0b",
            "Panen": "#ef4444",
            "Jeda Lahan": "#6b7280"
        }
        
        fig = px.timeline(
            df_gantt, 
            x_start="Start", 
            x_end="Finish", 
            y="Bedengan",
            color="Fase",
            color_discrete_map=color_map,
            title="Timeline Bedengan"
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Monthly calendar summary
        st.markdown("### 📅 Ringkasan per House")
        
        df_schedule = pd.DataFrame(st.session_state.planting_schedule)
        
        for house in df_schedule['house'].unique():
            house_data = df_schedule[df_schedule['house'] == house]
            
            with st.expander(f"🏠 {house} ({len(house_data)} bedengan)"):
                status_summary = house_data['status'].value_counts()
                
                cols = st.columns(len(status_summary))
                for i, (status, count) in enumerate(status_summary.items()):
                    with cols[i]:
                        st.metric(status.title(), count)
        
        # Statistics
        st.markdown("### 📊 Statistik")
        
        stat1, stat2, stat3, stat4 = st.columns(4)
        
        with stat1:
            st.metric("📦 Total Bedengan", len(st.session_state.planting_schedule))
        
        with stat2:
            panen_count = len([e for e in st.session_state.planting_schedule if e['status'] == 'panen'])
            st.metric("🌾 Sedang Panen", panen_count)
        
        with stat3:
            jeda_count = len([e for e in st.session_state.planting_schedule if e['status'] == 'jeda'])
            st.metric("🚜 Dalam Jeda", jeda_count)
        
        with stat4:
            total_harvested = sum(s['stems'] for s in st.session_state.harvest_sessions)
            st.metric("🌸 Total Panen", f"{total_harvested:,}")
    else:
        st.info("📝 Tambahkan jadwal tanam untuk melihat overview.")
        
        # Demo button
        if st.button("📋 Load Demo Data"):
            demo_beds = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06']
            base_date = datetime.now().date() - timedelta(days=60)
            
            for i, bed in enumerate(demo_beds):
                plant_date = base_date + timedelta(weeks=i)
                
                entry = {
                    "house": "House 1",
                    "bed_id": f"H1-{bed}",
                    "planting_date": plant_date.strftime("%Y-%m-%d"),
                    "harvest_start": (plant_date + timedelta(days=91)).strftime("%Y-%m-%d"),
                    "harvest_end": (plant_date + timedelta(days=101)).strftime("%Y-%m-%d"),
                    "clearing_start": (plant_date + timedelta(days=102)).strftime("%Y-%m-%d"),
                    "next_planting": (plant_date + timedelta(days=116)).strftime("%Y-%m-%d"),
                    "days_vegetatif": 35,
                    "days_generatif": 56,
                    "days_harvest": 10,
                    "days_jeda": 14,
                    "status": "vegetatif"
                }
                st.session_state.planting_schedule.append(entry)
            
            st.rerun()

# ==================== TAB 5: KALKULATOR HOUSE ====================
with tab5:
    st.subheader("🧮 Kalkulator Kebutuhan House")
    
    # Check if house config exists
    if 'house_database' in st.session_state and st.session_state.house_database:
        existing_houses = len(st.session_state.house_database)
        existing_beds = sum(h.get('beds', 12) for h in st.session_state.house_database.values())
        st.success(f"📊 Konfigurasi saat ini: **{existing_houses} house** dengan **{existing_beds} bedengan**")
    else:
        existing_houses = 0
        existing_beds = 0
        st.info("Hitung berapa house untuk **tanam tiap minggu di house berbeda** secara berurutan")
    
    col_calc1, col_calc2 = st.columns([1, 1.5])
    
    with col_calc1:
        st.markdown("### ⚙️ Parameter Siklus")
        
        calc_veg = st.number_input("🌱 Fase Vegetatif (hari)", 21, 50, 30, key="calc_veg", help="~4 minggu")
        calc_gen = st.number_input("🌸 Fase Generatif (hari)", 35, 70, 42, key="calc_gen", help="~6 minggu")
        calc_harvest = st.number_input("🌾 Periode Panen (hari)", 5, 14, 7, key="calc_harv")
        calc_jeda = st.number_input("🚜 Jeda Lahan (hari)", 10, 21, 12, key="calc_jeda")
        
        st.markdown("---")
        
        planting_interval = st.number_input(
            "📅 Interval Tanam antar House (hari)",
            min_value=5, max_value=14, value=7,
            help="Jarak waktu antar penanaman house berbeda"
        )
        
        # Get default from house_database or use 12
        default_beds = 12
        if 'house_database' in st.session_state and st.session_state.house_database:
            first_house = list(st.session_state.house_database.values())[0]
            default_beds = first_house.get('beds', 12)
        
        beds_per_house = st.number_input(
            "📦 Bedengan per House",
            min_value=4, max_value=50, value=default_beds,
            help="Jumlah bedengan dalam 1 greenhouse"
        )
    
    with col_calc2:
        st.markdown("### 📊 Hasil Kalkulasi")
        
        # Calculate
        total_cycle = calc_veg + calc_gen + calc_harvest + calc_jeda
        days_until_harvest = calc_veg + calc_gen
        
        import math
        required_houses = math.ceil(total_cycle / planting_interval)
        
        st.metric("📊 Total Siklus per House", f"{total_cycle} hari", f"~{total_cycle/30:.1f} bulan")
        st.metric("⏳ Hari Sampai Panen Pertama", f"{days_until_harvest} hari")
        
        st.markdown("---")
        
        st.metric("🏠 **JUMLAH HOUSE DIBUTUHKAN**", f"{required_houses} house")
        
        total_beds = required_houses * beds_per_house
        st.metric("📦 Total Bedengan", f"{total_beds}", f"@ {beds_per_house}/house")
        
        st.markdown("---")
        
        st.markdown(f"""
        <div class="sync-badge">
            <strong>Sistem Tanam Bergilir per House:</strong><br><br>
            📅 Minggu 1 → Tanam <strong>House 1</strong><br>
            📅 Minggu 2 → Tanam <strong>House 2</strong><br>
            ... sampai ...<br>
            📅 Minggu {required_houses} → Tanam <strong>House {required_houses}</strong><br><br>
            🔄 Minggu {required_houses + 1} → House 1 selesai jeda, siap tanam lagi!
        </div>
        """, unsafe_allow_html=True)
        
        # Timeline table
        st.markdown("#### 📋 Jadwal Rotasi House")
        
        rotation_data = []
        today = datetime.now().date()
        
        for i in range(min(required_houses, 10)):
            plant_date = today + timedelta(days=i * planting_interval)
            harvest_start = plant_date + timedelta(days=days_until_harvest)
            harvest_end = harvest_start + timedelta(days=calc_harvest)
            
            rotation_data.append({
                "House": f"House {i+1}",
                "Tanam": plant_date.strftime("%d %b"),
                "Panen Mulai": harvest_start.strftime("%d %b"),
                "Panen Selesai": harvest_end.strftime("%d %b")
            })
        
        st.dataframe(pd.DataFrame(rotation_data), use_container_width=True, hide_index=True)
        
        st.success(f"""
        💡 **Kesimpulan:**
        - Siklus **{total_cycle} hari**, tanam tiap **{planting_interval} hari**
        - Butuh **{required_houses} house** untuk rotasi kontinu
        - Total **{total_beds} bedengan**
        - Panen tiap minggu setelah {math.ceil(days_until_harvest/7)} minggu pertama!
        """)
        
        # Comparison with existing config
        if existing_houses > 0:
            st.markdown("### 📊 Perbandingan dengan Konfigurasi Saat Ini")
            
            comp_cols = st.columns(3)
            with comp_cols[0]:
                diff_houses = existing_houses - required_houses
                delta_text = f"+{diff_houses}" if diff_houses >= 0 else str(diff_houses)
                st.metric("🏠 House Tersedia", f"{existing_houses}", delta_text)
            
            with comp_cols[1]:
                diff_beds = existing_beds - total_beds
                delta_beds = f"+{diff_beds}" if diff_beds >= 0 else str(diff_beds)
                st.metric("📦 Bedengan Tersedia", f"{existing_beds}", delta_beds)
            
            with comp_cols[2]:
                if existing_houses >= required_houses:
                    st.success("✅ CUKUP untuk rotasi mingguan!")
                else:
                    st.warning(f"⚠️ Kurang {required_houses - existing_houses} house")

