# 📦 Pasca Panen Krisan
# Panduan panen, grading input, dan perpanjangan vase life

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import sys
import os

# Ensure project root is in path for utils import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_manager import init_db, save_harvest_record, get_harvest_summary, get_harvest_details, clear_database

st.set_page_config(page_title="Pasca Panen", page_icon="📦", layout="wide")

# Initialize DB and Load Data
init_db()
# Load latest data from DB to ensure session state is in sync
st.session_state.harvest_history = get_harvest_summary()
st.session_state.harvest_details = get_harvest_details()

# CSS
st.markdown("""
<style>
    .grade-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
        border: 1px solid #a7f3d0;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .grade-bs {
        background: linear-gradient(135deg, #fef3c7 0%, #ffffff 100%);
        border: 1px solid #fcd34d;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    .progress-bar {
        background: #e5e7eb;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    .progress-fill {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    .summary-box {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid #93c5fd;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📦 Teknologi Pasca Panen Krisan Spray")
st.info("Panduan pemanenan, grading input aktual, handling, dan perpanjangan vase life.")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "✂️ Teknik Panen", 
    "📊 Input Grading", 
    "📔 Jurnal Biaya",
    "📋 Standar Grade",
    "💧 Vase Life", 
    "📦 Packing",
    "📤 Export & Riwayat"
])

# TAB 1: Teknik Panen
with tab1:
    st.subheader("✂️ Teknik Pemanenan Krisan Spray")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### ⏰ Waktu Panen Optimal
        
        **Waktu Terbaik:**
        - Pagi hari: 06.00 - 09.00 WIB
        - Sore hari: 15.00 - 17.00 WIB
        - **HINDARI:** Tengah hari saat terik!
        
        **Kondisi Bunga:**
        - 2-3 kuntum sudah mekar penuh (untuk spray)
        - Kuntum lain masih kuncup berwarna
        - Hindari panen saat bunga basah
        """)
    
    with col2:
        st.markdown("""
        ### 🔧 Peralatan & Teknik
        
        **Peralatan:**
        - Pisau/gunting tajam & steril
        - Ember berisi air + preservative
        - Keranjang pengangkut
        
        **Cara Potong:**
        - Potong miring 45°
        - Sisakan 2 ruas daun di tanaman
        - Langsung masukkan ke air!
        """)
    
    st.warning("⚠️ **PENTING:** Jangan biarkan tangkai terkena udara >30 detik! Air embolism akan mengurangi vase life.")

# TAB 2: Input Grading Aktual
with tab2:
    st.subheader("📊 Input Hasil Grading Harian")
    
    # ========== HEADER LAPORAN HARIAN ==========
    st.markdown("### 📋 Informasi Laporan")
    
    report_cols = st.columns([1, 1, 1.5])
    
    with report_cols[0]:
        report_date = st.date_input(
            "📅 Tanggal",
            value=datetime.now().date(),
            help="Tanggal panen/grading"
        )
        
        # Day name in Indonesian
        day_names = {
            0: "Senin", 1: "Selasa", 2: "Rabu", 3: "Kamis", 
            4: "Jumat", 5: "Sabtu", 6: "Minggu"
        }
        day_name = day_names[report_date.weekday()]
        st.info(f"**Hari:** {day_name}")
    
    with report_cols[1]:
        # Get house list from database or use default
        if 'house_database' in st.session_state and st.session_state.house_database:
            house_options = [data['name'] for key, data in st.session_state.house_database.items()]
        elif 'house_list' in st.session_state:
            house_options = st.session_state.house_list
        else:
            st.session_state.house_list = ["House 1", "House 2", "House 3"]
            house_options = st.session_state.house_list
        
        house_name = st.selectbox(
            "🏠 Nama Greenhouse/House",
            house_options,
            help="Pilih greenhouse untuk grading"
        )
        
        # Option to add new house
        with st.expander("➕ Tambah House Baru"):
            new_house = st.text_input("Nama House Baru", key="add_house_grading")
            if st.button("Tambah", key="btn_add_grading"):
                if new_house:
                    if 'house_list' not in st.session_state:
                        st.session_state.house_list = list(house_options)
                    if new_house not in st.session_state.house_list:
                        st.session_state.house_list.append(new_house)
                        st.success(f"✅ {new_house} ditambahkan!")
                        st.rerun()
    
    with report_cols[2]:
        st.markdown(f"""
        <div class="summary-box">
            📊 <strong>Laporan Grading</strong><br>
            📅 {day_name}, {report_date.strftime('%d %B %Y')}<br>
            🏠 <strong>{house_name}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ========== SYNC DATA DARI HOUSE DATABASE ==========
    # Get selected house data from database
    selected_house_data = None
    if 'house_database' in st.session_state:
        for key, data in st.session_state.house_database.items():
            if data.get('name') == house_name:
                selected_house_data = data
                break
    
    if selected_house_data:
        st.markdown(f"""
        <div class="sync-badge">
            📊 <strong>Data House "{house_name}" dari Kalkulator Produksi:</strong><br>
            📦 Bedengan: <strong>{selected_house_data.get('beds', 0)}</strong> |
            📏 Panjang: <strong>{selected_house_data.get('bed_length', 25)}m</strong> |
            📊 Baris: <strong>{selected_house_data.get('rows_per_bed', 8)}</strong> |
            🌱 Total Tanaman: <strong>{selected_house_data.get('total_plants', 0):,}</strong><br>
            🤍 Putih: <strong>{selected_house_data.get('beds_putih', 0)}</strong> bed |
            💗 Pink: <strong>{selected_house_data.get('beds_pink', 0)}</strong> bed |
            💛 Kuning: <strong>{selected_house_data.get('beds_kuning', 0)}</strong> bed
        </div>
        """, unsafe_allow_html=True)
        
        use_synced = st.checkbox("✅ Gunakan data dari Kalkulator Produksi", value=True, key="use_synced_grading")
        
        if use_synced:
            beds_putih = selected_house_data.get('beds_putih', 4)
            beds_pink = selected_house_data.get('beds_pink', 4)
            beds_kuning = selected_house_data.get('beds_kuning', 4)
            plants_per_bed = selected_house_data.get('plants_per_bed', 1400)
        else:
            st.markdown("### 🌸 Input Manual Proporsi Bedengan")
            col_bed1, col_bed2, col_bed3 = st.columns(3)
            with col_bed1:
                beds_putih = st.number_input("🤍 Bedengan Putih", 0, 50, 4, key="manual_beds_putih")
            with col_bed2:
                beds_pink = st.number_input("💗 Bedengan Pink", 0, 50, 4, key="manual_beds_pink")
            with col_bed3:
                beds_kuning = st.number_input("💛 Bedengan Kuning", 0, 50, 4, key="manual_beds_kuning")
            plants_per_bed = st.number_input("🌱 Tanaman per Bedengan", 500, 3000, 1400, step=100)
    else:
        st.info("💡 Untuk sinkronisasi otomatis, isi data di **Kalkulator Produksi** → Tab Populasi Tanaman terlebih dahulu.")
        
        st.markdown("### 🌸 Proporsi Bedengan per Varietas")
        col_bed1, col_bed2, col_bed3 = st.columns(3)
        with col_bed1:
            beds_putih = st.number_input("🤍 Bedengan Putih", 0, 50, 4, key="beds_putih")
        with col_bed2:
            beds_pink = st.number_input("💗 Bedengan Pink", 0, 50, 4, key="beds_pink")
        with col_bed3:
            beds_kuning = st.number_input("💛 Bedengan Kuning", 0, 50, 4, key="beds_kuning")
        plants_per_bed = st.number_input("🌱 Tanaman per Bedengan", 500, 3000, 1400, step=100,
                                         help="Berdasarkan panjang × baris × jarak tanam")
    
    # Calculate plants per variety
    total_beds = beds_putih + beds_pink + beds_kuning
    plants_putih = beds_putih * plants_per_bed
    plants_pink = beds_pink * plants_per_bed
    plants_kuning = beds_kuning * plants_per_bed
    total_plants = plants_putih + plants_pink + plants_kuning
    
    # Display proportion
    st.markdown("### 📊 Proporsi Tanaman per Varietas")
    
    prop_cols = st.columns(4)
    
    with prop_cols[0]:
        pct_putih = (plants_putih / total_plants * 100) if total_plants > 0 else 0
        st.metric("🤍 Krisan Putih", f"{plants_putih:,}", f"{pct_putih:.1f}%")
    with prop_cols[1]:
        pct_pink = (plants_pink / total_plants * 100) if total_plants > 0 else 0
        st.metric("💗 Krisan Pink", f"{plants_pink:,}", f"{pct_pink:.1f}%")
    with prop_cols[2]:
        pct_kuning = (plants_kuning / total_plants * 100) if total_plants > 0 else 0
        st.metric("💛 Krisan Kuning", f"{plants_kuning:,}", f"{pct_kuning:.1f}%")
    with prop_cols[3]:
        st.metric("🌸 **TOTAL**", f"{total_plants:,}")
    
    st.markdown("---")
    
    # ========== PILIH VARIETAS UNTUK GRADING ==========
    st.markdown("### 📝 Input Grading per Varietas")
    
    selected_variety = st.radio(
        "Pilih Varietas untuk Input Grading:",
        ["🤍 Krisan Putih", "💗 Krisan Pink", "💛 Krisan Kuning"],
        horizontal=True
    )
    
    # Map variety to key
    variety_key = {
        "🤍 Krisan Putih": "putih",
        "💗 Krisan Pink": "pink", 
        "💛 Krisan Kuning": "kuning"
    }[selected_variety]
    
    variety_plants = {
        "putih": plants_putih,
        "pink": plants_pink,
        "kuning": plants_kuning
    }
    
    potential_harvest = variety_plants[variety_key]
    
    st.info(f"📊 Potensi panen {selected_variety}: **{potential_harvest:,}** batang ({beds_putih if variety_key == 'putih' else beds_pink if variety_key == 'pink' else beds_kuning} bedengan)")
    
    st.markdown("---")
    
    # Initialize session state for grades per variety
    if 'grading_data_variety' not in st.session_state:
        st.session_state.grading_data_variety = {
            'putih': {'g60': 0, 'g80': 0, 'g100': 0, 'g120': 0, 'g160': 0, 'r80': 0, 'r100': 0, 'r160': 0, 'r200': 0},
            'pink': {'g60': 0, 'g80': 0, 'g100': 0, 'g120': 0, 'g160': 0, 'r80': 0, 'r100': 0, 'r160': 0, 'r200': 0},
            'kuning': {'g60': 0, 'g80': 0, 'g100': 0, 'g120': 0, 'g160': 0, 'r80': 0, 'r100': 0, 'r160': 0, 'r200': 0},
        }
    
    # Use current variety data
    grading_data = st.session_state.grading_data_variety[variety_key]
    
    # GRADE NORMAL (Panjang 90 cm)
    st.markdown("### ✅ Grade Normal (Panjang 90 cm)")
    
    # Initialize price session state
    if 'grade_prices' not in st.session_state:
        st.session_state.grade_prices = {
            'g60': 1000, 'g80': 1000, 'g100': 1000, 'g120': 1000, 'g160': 1000,
            'r80': 500, 'r100': 500, 'r160': 400, 'r200': 350
        }
    
    normal_grades = [
        {"name": "Grade 60", "key": "g60", "qty": 60},
        {"name": "Grade 80", "key": "g80", "qty": 80},
        {"name": "Grade 100", "key": "g100", "qty": 100},
        {"name": "Grade 120", "key": "g120", "qty": 120},
        {"name": "Grade 160", "key": "g160", "qty": 160},
    ]
    
    cols_normal = st.columns(5)
    
    for i, grade in enumerate(normal_grades):
        with cols_normal[i]:
            st.markdown(f"""
            <div class="grade-card">
                <strong>{grade['name']}</strong><br>
                <small>{grade['qty']} btg/ikat</small>
            </div>
            """, unsafe_allow_html=True)
            
            grading_data[grade['key']] = st.number_input(
                "Jml Ikat",
                min_value=0, max_value=500, value=grading_data[grade['key']],
                key=f"input_{variety_key}_{grade['key']}",
                label_visibility="visible"
            )
            
            # Harga per batang (editable)
            st.session_state.grade_prices[grade['key']] = st.number_input(
                "Rp/btg",
                min_value=100, max_value=10000, 
                value=st.session_state.grade_prices[grade['key']],
                step=50,
                key=f"price_{variety_key}_{grade['key']}",
                label_visibility="visible"
            )
            
            # Hitung total
            total_stems_grade = grading_data[grade['key']] * grade['qty']
            price_per_stem = st.session_state.grade_prices[grade['key']]
            total_price_grade = total_stems_grade * price_per_stem
            
            if total_stems_grade > 0:
                st.markdown(f"<small>= {total_stems_grade:,} btg<br>**Rp {total_price_grade:,.0f}**</small>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # GRADE BS/RUSAK (Panjang 70-80 cm)
    st.markdown("### ⚠️ Grade Rusak/BS (Panjang 70-80 cm)")
    st.caption("Untuk bunga dengan batang lebih pendek dari standar")
    
    bs_grades = [
        {"name": "R-80", "key": "r80", "qty": 80, "length": 80},
        {"name": "R-100", "key": "r100", "qty": 100, "length": 80},
        {"name": "R-160", "key": "r160", "qty": 160, "length": 70},
        {"name": "R-200", "key": "r200", "qty": 200, "length": 70},
    ]
    
    cols_bs = st.columns(4)
    
    for i, grade in enumerate(bs_grades):
        with cols_bs[i]:
            st.markdown(f"""
            <div class="grade-bs">
                <strong>{grade['name']}</strong><br>
                <small>({grade['qty']} btg, {grade['length']}cm)</small>
            </div>
            """, unsafe_allow_html=True)
            
            grading_data[grade['key']] = st.number_input(
                "Jml Ikat",
                min_value=0, max_value=500, value=grading_data[grade['key']],
                key=f"input_{variety_key}_{grade['key']}",
                label_visibility="visible"
            )
            
            # Harga per batang (editable)
            st.session_state.grade_prices[grade['key']] = st.number_input(
                "Rp/btg",
                min_value=100, max_value=10000, 
                value=st.session_state.grade_prices[grade['key']],
                step=50,
                key=f"price_{variety_key}_{grade['key']}",
                label_visibility="visible"
            )
            
            # Hitung total
            total_stems_grade = grading_data[grade['key']] * grade['qty']
            price_per_stem = st.session_state.grade_prices[grade['key']]
            total_price_grade = total_stems_grade * price_per_stem
            
            if total_stems_grade > 0:
                st.markdown(f"<small>= {total_stems_grade:,} btg<br>**Rp {total_price_grade:,.0f}**</small>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # CALCULATE TOTALS (for current variety) - ikat × qty
    total_normal_stems = sum(
        grading_data[g['key']] * g['qty']
        for g in normal_grades
    )
    
    total_bs_stems = sum(
        grading_data[g['key']] * g['qty']
        for g in bs_grades
    )
    
    total_graded = total_normal_stems + total_bs_stems
    progress_pct = (total_graded / potential_harvest * 100) if potential_harvest > 0 else 0
    remaining = potential_harvest - total_graded
    
    # Revenue calculation - (ikat × qty) × price per stem from session state
    revenue_normal = sum(
        grading_data[g['key']] * g['qty'] * st.session_state.grade_prices[g['key']] 
        for g in normal_grades
    )
    
    revenue_bs = sum(
        grading_data[g['key']] * g['qty'] * st.session_state.grade_prices[g['key']] 
        for g in bs_grades
    )
    
    total_revenue = revenue_normal + revenue_bs
    
    # PROGRESS BAR
    st.markdown("### 📊 Progress Grading")
    
    progress_color = "#10b981" if progress_pct <= 100 else "#ef4444"
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {min(progress_pct, 100)}%; background: {progress_color};"></div>
    </div>
    <div style="text-align: center; margin-top: 0.5rem;">
        <strong>{total_graded:,}</strong> / {potential_harvest:,} batang 
        (<strong>{progress_pct:.1f}%</strong>)
        {f" — Sisa: {remaining:,} batang" if remaining > 0 else ""}
    </div>
    """, unsafe_allow_html=True)
    
    if progress_pct > 100:
        st.error(f"⚠️ Total grading ({total_graded:,}) melebihi potensi panen ({potential_harvest:,})!")
    
    st.markdown("---")
    
    # SUMMARY TABLE - Current Variety
    st.markdown(f"### 💰 Ringkasan Grading {selected_variety}")
    
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    
    with col_sum1:
        st.metric("🌸 Total Batang Normal", f"{total_normal_stems:,}")
        st.metric("💵 Pendapatan Normal", f"Rp {revenue_normal:,.0f}")
    
    with col_sum2:
        st.metric("⚠️ Total Batang BS", f"{total_bs_stems:,}")
        st.metric("💵 Pendapatan BS", f"Rp {revenue_bs:,.0f}")
    
    with col_sum3:
        st.metric("📦 **TOTAL BATANG**", f"{total_graded:,}")
        st.metric("💰 **TOTAL PENDAPATAN**", f"Rp {total_revenue:,.0f}")
    
    # ========== RINGKASAN SEMUA VARIETAS ==========
    st.markdown("---")
    st.markdown("### 🌈 Ringkasan Keseluruhan (Semua Varietas)")
    
    # Calculate totals for all varieties
    all_variety_data = st.session_state.grading_data_variety
    
    def calculate_variety_totals(var_key):
        var_data = all_variety_data[var_key]
        stems_normal = sum(var_data[g['key']] * g['qty'] for g in normal_grades)
        stems_bs = sum(var_data[g['key']] * g['qty'] for g in bs_grades)
        rev_normal = sum(var_data[g['key']] * g['qty'] * st.session_state.grade_prices[g['key']] for g in normal_grades)
        rev_bs = sum(var_data[g['key']] * g['qty'] * st.session_state.grade_prices[g['key']] for g in bs_grades)
        return {
            'stems': stems_normal + stems_bs,
            'normal': stems_normal,
            'bs': stems_bs,
            'revenue': rev_normal + rev_bs
        }
    
    totals_putih = calculate_variety_totals('putih')
    totals_pink = calculate_variety_totals('pink')
    totals_kuning = calculate_variety_totals('kuning')
    
    grand_total_stems = totals_putih['stems'] + totals_pink['stems'] + totals_kuning['stems']
    grand_total_revenue = totals_putih['revenue'] + totals_pink['revenue'] + totals_kuning['revenue']
    
    # Display per variety summary
    var_cols = st.columns(4)
    
    with var_cols[0]:
        pct_putih = (totals_putih['stems'] / grand_total_stems * 100) if grand_total_stems > 0 else 0
        st.markdown("**🤍 Putih**")
        st.metric("Batang", f"{totals_putih['stems']:,}", f"{pct_putih:.1f}%")
        st.metric("Pendapatan", f"Rp {totals_putih['revenue']:,.0f}")
    
    with var_cols[1]:
        pct_pink = (totals_pink['stems'] / grand_total_stems * 100) if grand_total_stems > 0 else 0
        st.markdown("**💗 Pink**")
        st.metric("Batang", f"{totals_pink['stems']:,}", f"{pct_pink:.1f}%")
        st.metric("Pendapatan", f"Rp {totals_pink['revenue']:,.0f}")
    
    with var_cols[2]:
        pct_kuning = (totals_kuning['stems'] / grand_total_stems * 100) if grand_total_stems > 0 else 0
        st.markdown("**💛 Kuning**")
        st.metric("Batang", f"{totals_kuning['stems']:,}", f"{pct_kuning:.1f}%")
        st.metric("Pendapatan", f"Rp {totals_kuning['revenue']:,.0f}")
    
    with var_cols[3]:
        st.markdown("**🌈 TOTAL**")
        st.metric("Batang", f"{grand_total_stems:,}")
        st.metric("Pendapatan", f"Rp {grand_total_revenue:,.0f}")
    
    # Proportion chart for all varieties
    if grand_total_stems > 0:
        st.markdown("#### 📊 Proporsi per Varietas")
        
        fig_var = go.Figure(data=[go.Pie(
            labels=['Putih', 'Pink', 'Kuning'],
            values=[totals_putih['stems'], totals_pink['stems'], totals_kuning['stems']],
            hole=0.4,
            marker_colors=['#f8fafc', '#f9a8d4', '#fcd34d'],
            textinfo='label+percent'
        )])
        fig_var.update_layout(title="Distribusi Batang per Varietas", height=300)
        st.plotly_chart(fig_var, use_container_width=True)
        
        # ========== SIMPAN GRADING KE RIWAYAT ==========
        st.markdown("---")
        st.markdown("### 💾 Simpan Laporan Grading")
        
        st.info(f"📊 Total: **{grand_total_stems:,}** tangkai | 💵 Pendapatan: **Rp {grand_total_revenue:,.0f}**")
        
        # Calculate Grade A percentage (normal grades proportion)
        grade_a_stems = totals_putih['normal'] + totals_pink['normal'] + totals_kuning['normal']
        grade_a_pct = (grade_a_stems / grand_total_stems * 100) if grand_total_stems > 0 else 0
        
        if st.button("💾 Simpan ke Riwayat Panen", type="primary", use_container_width=True, key="save_grading_to_history"):
            # Prepare Summary Data
            summary_entry = {
                "Tanggal": report_date.strftime("%Y-%m-%d"),
                "House": house_name,
                "Tangkai": int(grand_total_stems),
                "Grade A %": float(round(grade_a_pct, 1)),
                "Pendapatan": int(grand_total_revenue),
                "Putih": int(totals_putih['stems']),
                "Pink": int(totals_pink['stems']),
                "Kuning": int(totals_kuning['stems'])
            }
            
            # Prepare Details Data (Granular)
            current_date = report_date.strftime("%Y-%m-%d")
            details_rows = []
            
            # Helper to record item lines
            def record_variety_details(var_name, var_key, var_data):
                # Normal grades
                for g in normal_grades:
                    ikat = var_data.get(g['key'], 0)
                    if ikat > 0:
                        qty = ikat * g['qty']
                        price_per_ikat = st.session_state.grade_prices.get(g['key'], 0) * g['qty']
                        revenue = ikat * price_per_ikat
                        
                        details_rows.append({
                            "Tanggal": current_date,
                            "House": house_name,
                            "Varietas": var_name,
                            "Grade": g['label'], # Use label from dict
                            "Tipe": "Normal",
                            "Ukuran": f"{g['qty']} bt/ikat",
                            "Jml_Ikat": ikat,
                            "Isi_per_Ikat": g['qty'],
                            "Total_Batang": qty,
                            "Harga_per_Ikat": price_per_ikat,
                            "Harga_per_Batang": st.session_state.grade_prices.get(g['key'], 0),
                            "Total_Pendapatan": revenue
                        })

                # BS grades
                for b in bs_grades:
                    ikat = var_data.get(b['key'], 0)
                    if ikat > 0:
                        qty = ikat * b['qty']
                        price_per_ikat = st.session_state.grade_prices.get(b['key'], 0) * b['qty']
                        revenue = ikat * price_per_ikat
                        
                        details_rows.append({
                            "Tanggal": current_date,
                            "House": house_name,
                            "Varietas": var_name,
                            "Grade": b['label'], # Use label from dict (need to check if key exists in list above)
                            "Tipe": "BS/Reject",
                            "Ukuran": f"{b['qty']} bt/ikat",
                            "Jml_Ikat": ikat,
                            "Isi_per_Ikat": b['qty'],
                            "Total_Batang": qty,
                            "Harga_per_Ikat": price_per_ikat,
                            "Harga_per_Batang": st.session_state.grade_prices.get(b['key'], 0),
                            "Total_Pendapatan": revenue
                        })

            # Check if grade dicts have 'label' or need 'name'
            # Based on view_file, they have 'name'. Let's use 'name'.
            # Redefining helper properly inside the replacement.
            
            details_rows = []
            def record_variety_details_db(var_name, var_key, var_data):
                for g in normal_grades: # uses 'name'
                    ikat = var_data.get(g['key'], 0)
                    if ikat > 0:
                        details_rows.append({
                            "Tanggal": current_date,
                            "House": house_name,
                            "Varietas": var_name,
                            "Grade": g['name'],
                            "Tipe": "Normal",
                            "Ukuran": f"{g['qty']} bt/ikat",
                            "Jml_Ikat": ikat,
                            "Isi_per_Ikat": g['qty'],
                            "Total_Batang": ikat * g['qty'],
                            "Harga_per_Ikat": st.session_state.grade_prices.get(g['key'], 0) * g['qty'],
                            "Harga_per_Batang": st.session_state.grade_prices.get(g['key'], 0),
                            "Total_Pendapatan": ikat * g['qty'] * st.session_state.grade_prices.get(g['key'], 0)
                        })
                for b in bs_grades: # uses 'name'
                    ikat = var_data.get(b['key'], 0)
                    if ikat > 0:
                        details_rows.append({
                            "Tanggal": current_date,
                            "House": house_name,
                            "Varietas": var_name,
                            "Grade": b['name'],
                            "Tipe": "BS/Reject",
                            "Ukuran": f"{b['qty']} bt/ikat",
                            "Jml_Ikat": ikat,
                            "Isi_per_Ikat": b['qty'],
                            "Total_Batang": ikat * b['qty'],
                            "Harga_per_Ikat": st.session_state.grade_prices.get(b['key'], 0) * b['qty'],
                            "Harga_per_Batang": st.session_state.grade_prices.get(b['key'], 0),
                            "Total_Pendapatan": ikat * b['qty'] * st.session_state.grade_prices.get(b['key'], 0)
                        })

            record_variety_details_db("Putih", "putih", st.session_state.grading_data_variety['putih'])
            record_variety_details_db("Pink", "pink", st.session_state.grading_data_variety['pink'])
            record_variety_details_db("Kuning", "kuning", st.session_state.grading_data_variety['kuning'])
            
            df_details_save = pd.DataFrame(details_rows)
            
            # Save to Database
            if save_harvest_record(summary_entry, df_details_save):
                st.success("✅ Data berhasil disimpan ke Database!")
                # Refresh session state
                st.session_state.harvest_history = get_harvest_summary()
                st.session_state.harvest_details = get_harvest_details()
                st.balloons()
            else:
                st.error("❌ Gagal menyimpan data.")
            

    
    # Detailed breakdown table
    with st.expander("📋 Lihat Rincian per Grade", expanded=False):
        breakdown_data = []
        
        for g in normal_grades:
            ikat = grading_data[g['key']]
            if ikat > 0:
                price = st.session_state.grade_prices[g['key']]
                breakdown_data.append({
                    "Grade": g['name'],
                    "Tipe": "Normal",
                    "Ikat": ikat,
                    "Batang": ikat * g['qty'],
                    "Harga/Btg": f"Rp {price:,}",
                    "Subtotal": f"Rp {ikat * g['qty'] * price:,}"
                })
        
        for g in bs_grades:
            ikat = grading_data[g['key']]
            if ikat > 0:
                price = st.session_state.grade_prices[g['key']]
                breakdown_data.append({
                    "Grade": g['name'],
                    "Tipe": "BS/Rusak",
                    "Ikat": ikat,
                    "Batang": ikat * g['qty'],
                    "Harga/Btg": f"Rp {price:,}",
                    "Subtotal": f"Rp {ikat * g['qty'] * price:,}"
                })
        
        if breakdown_data:
            st.dataframe(pd.DataFrame(breakdown_data), use_container_width=True, hide_index=True)
        else:
            st.info("Belum ada data grading yang diinput.")
    
    # Pie chart - Distribusi Grade
    if total_graded > 0:
        st.markdown("### 📊 Distribusi Grade")
        
        labels = []
        values = []
        revenues = []
        
        for g in normal_grades:
            stems = grading_data[g['key']] * g['qty']
            if stems > 0:
                labels.append(g['name'])
                values.append(stems)
                revenues.append(stems * st.session_state.grade_prices[g['key']])
        
        for g in bs_grades:
            stems = grading_data[g['key']] * g['qty']
            if stems > 0:
                labels.append(g['name'])
                values.append(stems)
                revenues.append(stems * st.session_state.grade_prices[g['key']])
        
        # Two charts side by side
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig1 = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values, 
                hole=0.4,
                marker_colors=['#10b981', '#059669', '#047857', '#065f46', '#064e3b', 
                              '#fbbf24', '#f59e0b', '#d97706', '#b45309']
            )])
            fig1.update_layout(title="Distribusi Batang", height=350)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_chart2:
            fig2 = go.Figure(data=[go.Pie(
                labels=labels, 
                values=revenues, 
                hole=0.4,
                marker_colors=['#10b981', '#059669', '#047857', '#065f46', '#064e3b', 
                              '#fbbf24', '#f59e0b', '#d97706', '#b45309']
            )])
            fig2.update_layout(title="Distribusi Pendapatan", height=350)
            st.plotly_chart(fig2, use_container_width=True)
    
    # ========== ANALISIS HARGA PER BATANG ==========
    st.markdown("---")
    st.markdown("### 💵 Analisis Biaya & Pendapatan Operasional")
    
    # Sync production parameters
    if 'krisan_data' in st.session_state and st.session_state.krisan_data.get('total_plants', 0) > 0:
        kd = st.session_state.krisan_data
        st.markdown(f"""
        <div class="sync-badge">
            📊 <strong>Data Tersinkronisasi dari Kalkulator Produksi:</strong><br>
            🌱 Total Tanaman: <strong>{kd.get('total_plants', 0):,}</strong> |
            ✅ Tanaman Hidup: <strong>{kd.get('surviving_plants', 0):,}</strong> |
            🌸 Potensi Tangkai: <strong>{kd.get('total_stems', 0):,}</strong><br>
            📐 Luas: <strong>{kd.get('total_bed_area', 0):.1f}</strong> m² |
            📦 Bedengan: <strong>{kd.get('num_beds', 0)}</strong> unit |
            📊 Densitas: <strong>{kd.get('actual_density', 0):.1f}</strong> tanaman/m²
        </div>
        """, unsafe_allow_html=True)
    
    col_cost, col_expected = st.columns(2)
    
    with col_cost:
        st.markdown("**📊 Input Parameter Biaya Produksi**")
        
        operational_cost = st.number_input(
            "💵 Biaya Operasional (Rp/siklus)",
            min_value=1000000, max_value=300000000, value=25000000, step=1000000,
            help="Bibit, pupuk, pestisida, tenaga kerja, listrik, dll"
        )
        
        depreciation_cost = st.number_input(
            "🏠 Biaya Penyusutan House (Rp/siklus)",
            min_value=500000, max_value=50000000, value=5000000, step=500000,
            help="Penyusutan greenhouse, irigasi, lampu per siklus"
        )
        
        production_cost_total = operational_cost + depreciation_cost
        
        st.metric("💰 **TOTAL BIAYA PRODUKSI**", f"Rp {production_cost_total:,.0f}")
        st.caption(f"= Operasional Rp {operational_cost:,.0f} + Penyusutan Rp {depreciation_cost:,.0f}")
        
        # Cost per stem based on synced or graded data
        if grand_total_stems > 0:
            cost_per_stem = production_cost_total / grand_total_stems
            st.metric("📊 Biaya per Batang", f"Rp {cost_per_stem:,.0f}", help="Total Biaya / Total Batang Graded")
        
        st.markdown("---")
        
        expected_price_per_stem = st.number_input(
            "🎯 Harga Ekspektasi Awal (Rp/batang)",
            min_value=500, max_value=5000, value=1200, step=100,
            help="Harga jual per batang yang diharapkan sebelum grading"
        )
    
    with col_expected:
        st.markdown("**🎯 Ekspektasi Awal**")
        
        expected_revenue = potential_harvest * expected_price_per_stem
        expected_profit = expected_revenue - production_cost_total
        expected_margin = (expected_profit / expected_revenue * 100) if expected_revenue > 0 else 0
        
        st.metric("Pendapatan Ekspektasi", f"Rp {expected_revenue:,.0f}")
        st.metric("Profit Ekspektasi", f"Rp {expected_profit:,.0f}")
        st.metric("Margin Ekspektasi", f"{expected_margin:.1f}%")
    
    # PERBANDINGAN AKTUAL VS EKSPEKTASI
    st.markdown("---")
    st.markdown("### 📈 Perbandingan Aktual vs Ekspektasi")
    
    # Calculate actual per stem values
    if total_graded > 0:
        actual_price_per_stem = total_revenue / total_graded
        cost_per_stem = production_cost_total / total_graded
        profit_per_stem = actual_price_per_stem - cost_per_stem
        margin_per_stem = (profit_per_stem / actual_price_per_stem * 100) if actual_price_per_stem > 0 else 0
        
        actual_profit = total_revenue - production_cost_total
        actual_margin = (actual_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # Variance calculation
        price_variance = actual_price_per_stem - expected_price_per_stem
        price_variance_pct = (price_variance / expected_price_per_stem * 100) if expected_price_per_stem > 0 else 0
        revenue_variance = total_revenue - expected_revenue
        profit_variance = actual_profit - expected_profit
        
        # Display comparison table
        comparison_data = pd.DataFrame({
            "Parameter": [
                "Jumlah Batang",
                "Harga per Batang",
                "Total Pendapatan",
                "Biaya Produksi",
                "Total Profit",
                "Margin (%)"
            ],
            "Ekspektasi": [
                f"{potential_harvest:,}",
                f"Rp {expected_price_per_stem:,.0f}",
                f"Rp {expected_revenue:,.0f}",
                f"Rp {production_cost_total:,.0f}",
                f"Rp {expected_profit:,.0f}",
                f"{expected_margin:.1f}%"
            ],
            "Aktual": [
                f"{total_graded:,}",
                f"Rp {actual_price_per_stem:,.0f}",
                f"Rp {total_revenue:,.0f}",
                f"Rp {production_cost_total:,.0f}",
                f"Rp {actual_profit:,.0f}",
                f"{actual_margin:.1f}%"
            ],
            "Selisih": [
                f"{total_graded - potential_harvest:+,}",
                f"Rp {price_variance:+,.0f} ({price_variance_pct:+.1f}%)",
                f"Rp {revenue_variance:+,.0f}",
                "-",
                f"Rp {profit_variance:+,.0f}",
                f"{actual_margin - expected_margin:+.1f}%"
            ]
        })
        
        st.dataframe(comparison_data, use_container_width=True, hide_index=True)
        
        # Visual indicators
        st.markdown("---")
        st.markdown("### 📊 Analisis Per Batang")
        
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            st.metric(
                "Harga Jual/Batang", 
                f"Rp {actual_price_per_stem:,.0f}",
                delta=f"Rp {price_variance:+,.0f} vs ekspektasi",
                delta_color="normal" if price_variance >= 0 else "inverse"
            )
        
        with m2:
            st.metric("Biaya/Batang", f"Rp {cost_per_stem:,.0f}")
        
        with m3:
            st.metric(
                "Profit/Batang", 
                f"Rp {profit_per_stem:,.0f}",
                delta_color="normal" if profit_per_stem > 0 else "inverse"
            )
        
        with m4:
            st.metric(
                "Margin/Batang", 
                f"{margin_per_stem:.1f}%",
                delta_color="normal" if margin_per_stem > 20 else "inverse"
            )
        
        # Summary verdict
        st.markdown("---")
        
        if price_variance >= 0 and profit_variance >= 0:
            st.success(f"""
            ✅ **HASIL LEBIH BAIK DARI EKSPEKTASI!**
            
            - Harga aktual per batang **lebih tinggi** Rp {price_variance:,.0f} dari ekspektasi
            - Profit aktual **lebih besar** Rp {profit_variance:,.0f} dari target
            """)
        elif price_variance < 0 and profit_variance < 0:
            st.error(f"""
            ⚠️ **HASIL DI BAWAH EKSPEKTASI**
            
            - Harga aktual per batang **lebih rendah** Rp {abs(price_variance):,.0f} dari ekspektasi
            - Profit aktual **lebih kecil** Rp {abs(profit_variance):,.0f} dari target
            
            **Penyebab potensial:** Proporsi grade BS tinggi, harga pasar turun
            """)
        else:
            st.warning(f"""
            ⚡ **HASIL BERVARIASI**
            
            - Harga per batang: {'lebih tinggi' if price_variance >= 0 else 'lebih rendah'} dari ekspektasi
            - Total profit: {'tercapai' if profit_variance >= 0 else 'tidak tercapai'}
            """)
        
        # Grade price analysis
        st.markdown("---")
        st.markdown("### 📋 Harga per Batang tiap Grade")
        
        grade_price_data = []
        
        for g in normal_grades:
            ikat = grading_data.get(g['key'], 0)
            if ikat > 0:
                price_per_stem_actual = st.session_state.grade_prices.get(g['key'], 0)
                price_per_ikat = price_per_stem_actual * g['qty']
                
                grade_price_data.append({
                    "Grade": g['name'],
                    "Batang/Ikat": g['qty'],
                    "Harga/Ikat": f"Rp {price_per_ikat:,.0f}",
                    "Harga/Batang": f"Rp {price_per_stem_actual:,.0f}",
                    "vs Ekspektasi": f"Rp {price_per_stem_actual - expected_price_per_stem:+,.0f}",
                    "Status": "✅" if price_per_stem_actual >= expected_price_per_stem else "⚠️"
                })
        
        for g in bs_grades:
            ikat = grading_data.get(g['key'], 0)
            if ikat > 0:
                price_per_stem_actual = st.session_state.grade_prices.get(g['key'], 0)
                price_per_ikat = price_per_stem_actual * g['qty']
                
                grade_price_data.append({
                    "Grade": g['name'],
                    "Batang/Ikat": g['qty'],
                    "Harga/Ikat": f"Rp {price_per_ikat:,.0f}",
                    "Harga/Batang": f"Rp {price_per_stem_actual:,.0f}",
                    "vs Ekspektasi": f"Rp {price_per_stem_actual - expected_price_per_stem:+,.0f}",
                    "Status": "✅" if price_per_stem_actual >= expected_price_per_stem else "⚠️"
                })
        
        if grade_price_data:
            st.dataframe(pd.DataFrame(grade_price_data), use_container_width=True, hide_index=True)
    else:
        st.info("💡 Masukkan data grading di atas untuk melihat analisis perbandingan.")

# TAB 3: Jurnal Biaya Harian
with tab3:
    st.subheader("📔 Jurnal Biaya Harian")
    st.info("Catat biaya aktual harian untuk dibandingkan dengan estimasi RAB")
    
    # Initialize journal session state
    if 'cost_journal' not in st.session_state:
        st.session_state.cost_journal = []
    
    # Sync RAB data
    rab_data = st.session_state.get('krisan_data', {})
    has_rab = rab_data.get('rab_total_operational', 0) > 0
    
    if has_rab:
        st.markdown(f"""
        <div class="sync-badge">
            💰 <strong>Estimasi RAB dari Kalkulator Produksi:</strong><br>
            🌱 Bibit: <strong>Rp {rab_data.get('rab_bibit', 0):,.0f}</strong> |
            🧪 Pupuk: <strong>Rp {rab_data.get('rab_pupuk', 0):,.0f}</strong> |
            🛡️ Pestisida: <strong>Rp {rab_data.get('rab_pestisida', 0):,.0f}</strong><br>
            👷 TK: <strong>Rp {rab_data.get('rab_tenaga_kerja', 0):,.0f}</strong> |
            ⚡ Listrik: <strong>Rp {rab_data.get('rab_listrik', 0):,.0f}</strong> |
            📦 Lainnya: <strong>Rp {rab_data.get('rab_lainnya', 0):,.0f}</strong> |
            💰 Total: <strong>Rp {rab_data.get('rab_total_operational', 0):,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Isi data RAB di Kalkulator Produksi → Tab RAB untuk perbandingan")
    
    st.markdown("---")
    
    # Input form
    st.markdown("### ➕ Input Biaya Baru")
    
    col_inp1, col_inp2, col_inp3 = st.columns([1, 1.5, 1])
    
    with col_inp1:
        journal_date = st.date_input("📅 Tanggal", value=datetime.now().date(), key="journal_date")
        
        category_options = ["🌱 Bibit", "🧪 Pupuk", "🛡️ Pestisida", "👷 Tenaga Kerja", "⚡ Listrik", "📦 Lain-lain"]
        journal_category = st.selectbox("📂 Kategori", category_options, key="journal_cat")
    
    with col_inp2:
        journal_desc = st.text_input("📝 Deskripsi/Keterangan", placeholder="Contoh: Beli NPK 50kg", key="journal_desc")
        journal_amount = st.number_input("💰 Jumlah Biaya (Rp)", min_value=0, max_value=100000000, value=0, step=10000, key="journal_amt")
    
    with col_inp3:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✅ Simpan Entri", type="primary", use_container_width=True):
            if journal_amount > 0:
                entry = {
                    "date": journal_date.strftime("%Y-%m-%d"),
                    "day": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"][journal_date.weekday()],
                    "category": journal_category,
                    "description": journal_desc,
                    "amount": journal_amount
                }
                st.session_state.cost_journal.append(entry)
                st.success(f"✅ Biaya Rp {journal_amount:,} tersimpan!")
                st.rerun()
            else:
                st.error("⚠️ Jumlah biaya harus lebih dari 0")
    
    st.markdown("---")
    
    # Journal history
    st.markdown("### 📋 Riwayat Transaksi")
    
    if st.session_state.cost_journal:
        df_journal = pd.DataFrame(st.session_state.cost_journal)
        df_journal['amount_formatted'] = df_journal['amount'].apply(lambda x: f"Rp {x:,}")
        
        st.dataframe(
            df_journal[['date', 'day', 'category', 'description', 'amount_formatted']].rename(columns={
                'date': 'Tanggal', 'day': 'Hari', 'category': 'Kategori', 
                'description': 'Keterangan', 'amount_formatted': 'Jumlah'
            }),
            use_container_width=True, hide_index=True
        )
        
        # Summary by category
        st.markdown("### 📊 Ringkasan per Kategori")
        
        # Calculate actual totals per category
        actual_totals = {}
        for cat in category_options:
            actual_totals[cat] = sum(e['amount'] for e in st.session_state.cost_journal if e['category'] == cat)
        
        total_actual = sum(actual_totals.values())
        
        # RAB mapping
        rab_mapping = {
            "🌱 Bibit": rab_data.get('rab_bibit', 0),
            "🧪 Pupuk": rab_data.get('rab_pupuk', 0),
            "🛡️ Pestisida": rab_data.get('rab_pestisida', 0),
            "👷 Tenaga Kerja": rab_data.get('rab_tenaga_kerja', 0),
            "⚡ Listrik": rab_data.get('rab_listrik', 0),
            "📦 Lain-lain": rab_data.get('rab_lainnya', 0)
        }
        
        total_rab = rab_data.get('rab_total_operational', 0)
        
        # Comparison table
        comparison_rows = []
        for cat in category_options:
            actual = actual_totals.get(cat, 0)
            estimated = rab_mapping.get(cat, 0)
            diff = actual - estimated
            pct = (diff / estimated * 100) if estimated > 0 else 0
            status = "✅ Hemat" if diff < 0 else ("⚠️ Over" if diff > 0 else "➖ Sama")
            
            comparison_rows.append({
                "Kategori": cat,
                "Estimasi RAB": f"Rp {estimated:,}",
                "Aktual": f"Rp {actual:,}",
                "Selisih": f"Rp {diff:+,}",
                "Persentase": f"{pct:+.1f}%",
                "Status": status
            })
        
        # Total row
        total_diff = total_actual - total_rab
        total_pct = (total_diff / total_rab * 100) if total_rab > 0 else 0
        total_status = "✅ Hemat" if total_diff < 0 else ("⚠️ Over Budget" if total_diff > 0 else "➖ Tepat")
        
        comparison_rows.append({
            "Kategori": "💰 **TOTAL**",
            "Estimasi RAB": f"Rp {total_rab:,}",
            "Aktual": f"Rp {total_actual:,}",
            "Selisih": f"Rp {total_diff:+,}",
            "Persentase": f"{total_pct:+.1f}%",
            "Status": total_status
        })
        
        st.dataframe(pd.DataFrame(comparison_rows), use_container_width=True, hide_index=True)
        
        # Summary metrics
        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("💰 Total RAB", f"Rp {total_rab:,}")
        with col_m2:
            st.metric("💵 Total Aktual", f"Rp {total_actual:,}")
        with col_m3:
            delta_color = "inverse" if total_diff > 0 else "normal"
            st.metric("📊 Selisih", f"Rp {total_diff:+,}", delta=f"{total_pct:+.1f}%", delta_color=delta_color)
        
        # Clear button
        st.markdown("---")
        if st.button("🗑️ Hapus Semua Data Jurnal", type="secondary"):
            st.session_state.cost_journal = []
            st.rerun()
    else:
        st.info("📝 Belum ada data jurnal. Mulai input biaya di atas.")

# TAB 4: Standar Grading (was tab3)
with tab4:
    st.subheader("📋 Standar Grading Krisan Spray")
    
    grading_criteria = pd.DataFrame({
        "Kriteria": ["Panjang Tangkai", "Jumlah Kuntum", "Ukuran Kuntum", "Kesegaran", 
                     "Kerusakan/Cacat", "Keseragaman Warna", "Daun"],
        "Grade Super": ["80-90 cm", "7-10 kuntum", ">5 cm diameter", "Turgid, segar", 
                        "0%", "100% seragam", "Hijau segar, lengkap"],
        "Grade A": ["70-80 cm", "5-7 kuntum", "4-5 cm diameter", "Turgid", 
                    "<5%", ">95% seragam", "Hijau, sedikit bercak OK"],
        "Grade B": ["60-70 cm", "4-5 kuntum", "3-4 cm diameter", "Cukup segar", 
                    "<10%", ">90% seragam", "Minor yellowing OK"],
        "Reject": ["<60 cm", "<4 kuntum", "<3 cm", "Layu", 
                   ">10%", "Tidak seragam", "Rusak/kuning"]
    })
    
    st.dataframe(grading_criteria, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.markdown("### 💰 Harga per Grade")
    
    cols = st.columns(4)
    with cols[0]:
        st.metric("Super", "Rp 15.000-20.000", "/tangkai")
    with cols[1]:
        st.metric("Grade A", "Rp 10.000-15.000", "/tangkai")
    with cols[2]:
        st.metric("Grade B", "Rp 7.000-10.000", "/tangkai")
    with cols[3]:
        st.metric("Grade C", "Rp 4.000-7.000", "/tangkai")

# TAB 4: Vase Life
with tab4:
    st.subheader("💧 Teknik Perpanjangan Vase Life")
    
    st.success("**Target Vase Life Krisan Spray:** 10-16 hari")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🧪 Larutan Preservative
        
        **Formula Komersial:**
        - Chrysal, Floralife
        - Ikuti dosis pada kemasan
        - Ganti setiap 2-3 hari
        
        **Formula DIY (per 1 Liter):**
        - Gula: 20g
        - Cuka: 2ml
        - Bleach: 3-4 tetes
        """)
    
    with col2:
        st.markdown("""
        ### 🌡️ Cold Chain
        
        | Tahap | Suhu | Durasi |
        |-------|------|--------|
        | Hydration | 2-4°C | 2-4 jam |
        | Storage | 2-4°C | Maks 7 hari |
        | Display | 8-12°C | 3-5 hari |
        """)
    
    st.error("🚨 JANGAN simpan bersama buah yang menghasilkan etilen!")

# TAB 5: Packing
with tab5:
    st.subheader("📦 Packing & Distribusi")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📦 Jenis Kemasan
        
        **1. Bunch Wrapping** (10 tangkai/bunch)
        - Plastik OPP transparan
        - Cocok untuk florist
        
        **2. Box Kardus** (20-50 bunch)
        - Distribusi jarak jauh
        """)
    
    with col2:
        st.markdown("""
        ### 🚚 Distribusi
        
        | Jarak | Suhu | Durasi |
        |-------|------|--------|
        | <50 km | Ambient | 2-3 jam |
        | 50-200 km | 8-15°C | 4-6 jam |
        | >200 km | 2-4°C | 24-48 jam |
        """)

# TAB 7: Export & Riwayat
with tab7:
    st.subheader("📤 Export Data & Riwayat Panen")
    
    col_export, col_history = st.columns([1, 1.5])
    
    with col_export:
        st.markdown("### 📥 Export Laporan")
        
        # Initialize harvest history if not exists
        if 'harvest_history' not in st.session_state:
            st.session_state.harvest_history = []
        
        # Export grading data
        if 'grading_data' in st.session_state and st.session_state.grading_data:
            grading_df = pd.DataFrame(st.session_state.grading_data)
            
            csv_grading = grading_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📊 Download Grading Data (CSV)",
                data=csv_grading,
                file_name=f"grading_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Belum ada data grading untuk di-export")
        
        st.markdown("---")
        
        # Export journal data
        if 'cost_journal' in st.session_state and st.session_state.cost_journal:
            journal_df = pd.DataFrame(st.session_state.cost_journal)
            
            csv_journal = journal_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📔 Download Jurnal Biaya (CSV)",
                data=csv_journal,
                file_name=f"jurnal_biaya_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        else:
            st.info("Belum ada data jurnal biaya")
        
        st.markdown("---")
        
        # Export harvest history
        if st.session_state.harvest_history:
            history_df = pd.DataFrame(st.session_state.harvest_history)
            
            csv_history = history_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "🌾 Download Riwayat Panen (Summary CSV)",
                data=csv_history,
                file_name=f"riwayat_panen_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        # Export granular details
        if 'harvest_details' in st.session_state and st.session_state.harvest_details:
            details_df = pd.DataFrame(st.session_state.harvest_details)
            
            csv_details = details_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📈 Download Dataset Detail (Granular CSV)",
                data=csv_details,
                file_name=f"dataset_panen_lengkap_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                type="primary",
                help="Download data rinci: Tanggal, House, Varietas, Grade, Ukuran, Jumlah, Harga"
            )
    
    with col_history:
        st.markdown("### 🌾 Riwayat Panen")
        
        # Add new harvest entry
        with st.expander("➕ Tambah Data Panen Baru", expanded=False):
            h_date = st.date_input("📅 Tanggal Panen", datetime.now().date(), key="harvest_date")
            
            # Get house list
            if 'house_database' in st.session_state and st.session_state.house_database:
                house_options = [h['name'] for h in st.session_state.house_database.values()]
            else:
                house_options = ["House 1", "House 2", "House 3"]
            
            h_house = st.selectbox("🏠 House", house_options, key="harvest_house")
            
            h_cols = st.columns(3)
            with h_cols[0]:
                h_stems = st.number_input("🌸 Total Tangkai", 0, 100000, 1000, key="harvest_stems")
            with h_cols[1]:
                h_grade_a = st.number_input("✅ Grade A (%)", 0, 100, 60, key="harvest_grade_a")
            with h_cols[2]:
                h_revenue = st.number_input("💵 Pendapatan (Rp)", 0, 100000000, 0, step=100000, key="harvest_revenue")
            
            if st.button("💾 Simpan Panen", type="primary", key="save_harvest"):
                summary_entry = {
                    "Tanggal": h_date.strftime("%Y-%m-%d"),
                    "House": h_house,
                    "Tangkai": int(h_stems),
                    "Grade A %": float(h_grade_a),
                    "Pendapatan": int(h_revenue),
                    "Putih": 0, "Pink": 0, "Kuning": 0 # Default if unknown
                }
                
                # Save with empty details
                if save_harvest_record(summary_entry, pd.DataFrame()):
                    st.success("✅ Data panen tersimpan ke Database!")
                    st.session_state.harvest_history = get_harvest_summary()
                    st.rerun()
                else:
                    st.error("❌ Gagal menyimpan data.")
        
        # Show history
        if st.session_state.harvest_history:
            st.markdown("#### 📋 Data Panen")
            history_df = pd.DataFrame(st.session_state.harvest_history)
            st.dataframe(history_df, use_container_width=True, hide_index=True)
            
            # Summary metrics
            total_stems = history_df['Tangkai'].sum()
            total_revenue = history_df['Pendapatan'].sum()
            avg_grade = history_df['Grade A %'].mean()
            
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("🌸 Total Tangkai", f"{total_stems:,}")
            with m2:
                st.metric("💵 Total Pendapatan", f"Rp {total_revenue:,}")
            with m3:
                st.metric("📊 Rata-rata Grade A", f"{avg_grade:.1f}%")
            
            st.markdown("---")
            
            # Trend chart
            st.markdown("#### 📈 Grafik Tren Panen")
            
            import plotly.express as px
            
            fig = px.bar(
                history_df, 
                x='Tanggal', 
                y='Tangkai',
                color='House',
                title="Produksi per Tanggal",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Revenue trend
            if total_revenue > 0:
                fig2 = px.line(
                    history_df,
                    x='Tanggal',
                    y='Pendapatan',
                    markers=True,
                    title="Tren Pendapatan"
                )
                fig2.update_layout(height=250)
                st.plotly_chart(fig2, use_container_width=True)
            
            # Clear button
            if st.button("🗑️ Hapus Semua Riwayat", type="primary", key="clear_history"):
                clear_database()
                st.session_state.harvest_history = []
                st.session_state.harvest_details = []
                st.rerun()
        else:
            st.info("📊 Belum ada riwayat panen. Tambahkan data melalui form di atas.")

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Teknologi Pasca Panen & Grading")

