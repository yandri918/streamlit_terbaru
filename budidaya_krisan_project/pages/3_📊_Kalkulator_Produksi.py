# 📊 Kalkulator Budidaya Krisan Spray
# Populasi, Irigasi, RAB, dan AI Optimasi

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os

# --- PERSISTENCE LOGIC ---
CONFIG_FILE = "data/krisan_house_config.json"

def load_house_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            return {}
    return {}

def save_house_config(config):
    os.makedirs("data", exist_ok=True)
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f)

st.set_page_config(page_title="Kalkulator Budidaya", page_icon="📊", layout="wide")

# CSS Styling
st.markdown("""
<style>
    .calc-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #ffffff 100%);
        border: 1px solid #a7f3d0;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .sync-badge {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border: 1px solid #93c5fd;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .result-box {
        background: #f0fdf4;
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("## 📊 Kalkulator Budidaya Krisan Spray")
st.info("Perhitungan lengkap: Populasi, Irigasi, RAB, dan Rekomendasi AI Optimasi")

# ========== DEFAULT CONFIGURATION ==========
# Default values for consistent calculation across all modules
DEFAULT_CONFIG = {
    'beds_per_house': 12,
    'bed_length': 50,       # meter
    'bed_width': 100,       # cm
    'rows_per_bed': 6,
    'plant_spacing': 12.5,  # cm
}

# Calculate default plants per bed: (length_cm / spacing) * rows
DEFAULT_PLANTS_PER_BED = int((DEFAULT_CONFIG['bed_length'] * 100) / DEFAULT_CONFIG['plant_spacing']) * DEFAULT_CONFIG['rows_per_bed']

# ========== INITIALIZE SESSION STATE ==========
if 'krisan_data' not in st.session_state:
    st.session_state.krisan_data = {
        'total_plants': 0,
        'total_bed_area': 0,
        'num_beds': DEFAULT_CONFIG['beds_per_house'],
        'total_stems': 0,
        'nozzle_count': 0,
        'irrigation_cost': 0,
        'bed_length': DEFAULT_CONFIG['bed_length'],
        'rows_per_bed': DEFAULT_CONFIG['rows_per_bed'],
        'plant_spacing': DEFAULT_CONFIG['plant_spacing'],
        'plants_per_bed': DEFAULT_PLANTS_PER_BED,
    }

# ========== TABS ==========
# ========== TABS ==========

# Initialize house database in session state
if 'house_database' not in st.session_state:
    st.session_state.house_database = {}

# AUTO-LOAD: Check if we have saved config and load it if session is empty
# Place this BEFORE tabs so it's ready globally
if not st.session_state.house_database:
    saved_config = load_house_config()
    if saved_config:
        st.session_state.house_database = saved_config
        st.toast(f"📂 Konfigurasi {len(saved_config)} House dimuat!", icon="✅")

# Determine default number of houses from saved data
default_num_houses = len(st.session_state.house_database) if st.session_state.house_database else 4

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌱 Populasi", 
    "💧 Irigasi & Teknis", 
    "💰 RAB & Profit",
    "🤖 AI Optimasi",
    "📈 Analisis Tahunan"
])

# ==================== TAB 1: POPULASI ====================
with tab1:
    st.subheader("🌱 Perhitungan Populasi Tanaman")
    
    # ========== KONFIGURASI HOUSE ==========
    st.markdown("### 🏠 Konfigurasi House/Greenhouse")
    
    house_config_cols = st.columns([1, 1, 1])
    
    with house_config_cols[0]:
        num_houses = st.number_input(
            "🏠 Jumlah House",
            min_value=1, max_value=20, value=default_num_houses,
            help="Total greenhouse yang akan dikelola"
        )
    
    with house_config_cols[1]:
        beds_per_house_config = st.number_input(
            "📦 Bedengan per House",
            min_value=4, max_value=50, value=12,
            help="Jumlah bedengan dalam satu greenhouse"
        )
    
    with house_config_cols[2]:
        st.metric("📊 Total Bedengan (default)", f"{num_houses * beds_per_house_config}")
    
    # House naming and configuration
    with st.expander("✏️ Konfigurasi Detail per House", expanded=True):
        st.info("Atur nama, bedengan, parameter tanam, dan proporsi varietas tiap house")
        
        house_configs = {}
        
        for i in range(num_houses):
            st.markdown(f"##### 🏠 House {i+1}")
            
            # Get existing config or defaults
            existing = st.session_state.house_database.get(f"house_{i+1}", {})
            
            # Row 1: Nama, Bedengan, Panjang, Baris, Jarak Tanam
            row1 = st.columns([1.5, 0.8, 0.8, 0.8, 0.8])
            
            with row1[0]:
                h_name = st.text_input(
                    "Nama",
                    value=existing.get('name', f"House {i+1}"),
                    key=f"h_name_{i+1}"
                )
            
            with row1[1]:
                h_beds = st.number_input(
                    "Bedengan",
                    min_value=1, max_value=50,
                    value=existing.get('beds', beds_per_house_config),
                    key=f"h_beds_{i+1}"
                )
            
            with row1[2]:
                h_length = st.number_input(
                    "Panjang (m)",
                    min_value=5, max_value=100,
                    value=existing.get('bed_length', 50),
                    key=f"h_length_{i+1}"
                )
            
            with row1[3]:
                h_rows = st.number_input(
                    "Baris/bed",
                    min_value=4, max_value=12,
                    value=existing.get('rows_per_bed', 6),
                    key=f"h_rows_{i+1}"
                )
            
            with row1[4]:
                h_spacing = st.selectbox(
                    "Jarak (cm)",
                    [10, 12.5, 15],
                    index=[10, 12.5, 15].index(existing.get('plant_spacing', 12.5)),
                    key=f"h_spacing_{i+1}"
                )
            
            # Row 2: Varietas proportion
            row2 = st.columns([1, 1, 1, 1.5])
            
            with row2[0]:
                h_putih = st.number_input(
                    "🤍 Putih",
                    min_value=0, max_value=h_beds,
                    value=min(existing.get('beds_putih', h_beds // 3), h_beds),
                    key=f"h_putih_{i+1}"
                )
            
            with row2[1]:
                h_pink = st.number_input(
                    "💗 Pink",
                    min_value=0, max_value=h_beds,
                    value=min(existing.get('beds_pink', h_beds // 3), h_beds),
                    key=f"h_pink_{i+1}"
                )
            
            with row2[2]:
                h_kuning = st.number_input(
                    "💛 Kuning",
                    min_value=0, max_value=h_beds,
                    value=min(existing.get('beds_kuning', h_beds - (h_beds // 3) * 2), h_beds),
                    key=f"h_kuning_{i+1}"
                )
            
            # Calculate plants
            plants_per_row = int((h_length * 100) / h_spacing)
            plants_per_bed = plants_per_row * h_rows
            total_plants_house = plants_per_bed * h_beds
            
            with row2[3]:
                st.metric("🌱 Total Tanaman", f"{total_plants_house:,}")
            
            # Validate total
            total_var = h_putih + h_pink + h_kuning
            if total_var != h_beds:
                st.warning(f"⚠️ Total varietas ({total_var}) ≠ bedengan ({h_beds})")
            
            house_configs[f"house_{i+1}"] = {
                'name': h_name,
                'beds': h_beds,
                'bed_length': h_length,
                'rows_per_bed': h_rows,
                'plant_spacing': h_spacing,
                'plants_per_bed': plants_per_bed,
                'total_plants': total_plants_house,
                'beds_putih': h_putih,
                'beds_pink': h_pink,
                'beds_kuning': h_kuning,
                'id': i + 1
            }
            
            st.markdown("---")
        
        if st.button("💾 Simpan Semua Konfigurasi House", type="primary"):
            st.session_state.house_database = house_configs
            st.session_state.krisan_data['num_houses'] = num_houses
            
            # Calculate totals
            total_beds_all = sum(c['beds'] for c in house_configs.values())
            total_plants_all = sum(c['total_plants'] for c in house_configs.values())
            st.session_state.krisan_data['total_beds_all_houses'] = total_beds_all
            st.session_state.krisan_data['total_plants_all_houses'] = total_plants_all
            
            # PERSISTENCE: Save to JSON file
            try:
                save_house_config(house_configs)
                st.success(f"✅ {num_houses} house tersimpan PERMANEN! Total {total_beds_all} bedengan, {total_plants_all:,} tanaman")
            except Exception as e:
                st.error(f"❌ Gagal menyimpan ke file: {e}")
                
            st.rerun()
    
    # Show saved houses summary
    if st.session_state.house_database:
        st.markdown("#### 📋 Ringkasan Konfigurasi House")
        house_list = []
        total_beds = 0
        total_plants = 0
        for key, data in st.session_state.house_database.items():
            beds_count = data.get('beds', 12)
            plants_count = data.get('total_plants', 0)
            total_beds += beds_count
            total_plants += plants_count
            house_list.append({
                "ID": data.get('id', 0),
                "Nama": data.get('name', key),
                "Bed": beds_count,
                "Pjg(m)": data.get('bed_length', 25),
                "Baris": data.get('rows_per_bed', 8),
                "Jarak": f"{data.get('plant_spacing', 12.5)}cm",
                "🌱Tanaman": f"{plants_count:,}",
                "🤍": data.get('beds_putih', 0),
                "💗": data.get('beds_pink', 0),
                "💛": data.get('beds_kuning', 0)
            })
        if house_list:
            st.dataframe(pd.DataFrame(house_list), use_container_width=True, hide_index=True)
            
            m1, m2 = st.columns(2)
            with m1:
                st.metric("📦 Total Bedengan", f"{total_beds}")
            with m2:
                st.metric("🌱 Total Tanaman", f"{total_plants:,}")
    
    st.markdown("---")
    
    col_bed, col_result = st.columns([1.2, 1])
    
    with col_bed:
        st.markdown("### 📐 Konfigurasi Bedengan")
        
        bed_length = st.number_input(
            "📏 Panjang Bedengan (meter)", 
            min_value=5, max_value=100, value=25, step=1,
            help="Panjang satu bedengan dalam meter"
        )
        
        bed_width = st.number_input(
            "📐 Lebar Bedengan (cm)", 
            min_value=80, max_value=150, value=100, step=10,
            help="Lebar standar bedengan krisan: 100-120 cm"
        )
        
        calculated_beds = num_houses * beds_per_house_config
        num_beds = st.number_input(
            "🔢 Jumlah Bedengan Total", 
            min_value=1, max_value=500, value=min(calculated_beds, 500), step=1,
            help="Total bedengan dalam greenhouse"
        )
        
        # ========== PROPORSI BEDENGAN PER VARIETAS ==========
        st.markdown("### 🌸 Proporsi Bedengan per Varietas")
        st.caption("Tentukan pembagian bedengan untuk setiap warna krisan")
        
        var_cols = st.columns(3)
        
        with var_cols[0]:
            beds_putih = st.number_input("🤍 Bedengan Putih", 0, num_beds, 4, key="calc_beds_putih")
        with var_cols[1]:
            beds_pink = st.number_input("💗 Bedengan Pink", 0, num_beds, 4, key="calc_beds_pink")
        with var_cols[2]:
            beds_kuning = st.number_input("💛 Bedengan Kuning", 0, num_beds, 4, key="calc_beds_kuning")
        
        total_assigned = beds_putih + beds_pink + beds_kuning
        
        if total_assigned != num_beds:
            st.warning(f"⚠️ Total bedengan varietas ({total_assigned}) tidak sama dengan total bedengan ({num_beds})")
        else:
            st.success(f"✅ Semua {num_beds} bedengan sudah dialokasikan")
        
        st.markdown("### 🌿 Konfigurasi Tanam")
        
        rows_per_bed = st.selectbox(
            "📊 Jumlah Baris per Bedengan",
            options=[6, 7, 8, 9, 10],
            index=2,
            help="Standar: 8 baris untuk lebar 100cm"
        )
        
        plant_spacing = st.selectbox(
            "↔️ Jarak Tanam dalam Baris (cm)",
            options=[10.0, 12.5, 15.0],
            index=1,
            format_func=lambda x: f"{x} cm"
        )
        
        survival_rate = st.slider("📊 Survival Rate (%)", 70, 98, 85)
        stems_per_plant = st.slider("🌸 Tangkai/Tanaman", 2.0, 5.0, 3.5, 0.5)
    
    with col_result:
        st.markdown("### 📊 Hasil Perhitungan")
        
        # CALCULATIONS
        plants_per_row = int((bed_length * 100) / plant_spacing)
        plants_per_bed = plants_per_row * rows_per_bed
        total_plants = plants_per_bed * num_beds
        bed_area_m2 = (bed_length * (bed_width / 100))
        total_bed_area = bed_area_m2 * num_beds
        actual_density = total_plants / total_bed_area if total_bed_area > 0 else 0
        surviving_plants = int(total_plants * (survival_rate / 100))
        total_stems = int(surviving_plants * stems_per_plant)
        
        # Update session state
        st.session_state.krisan_data['total_plants'] = total_plants
        st.session_state.krisan_data['total_bed_area'] = total_bed_area
        st.session_state.krisan_data['num_beds'] = num_beds
        st.session_state.krisan_data['total_stems'] = total_stems
        st.session_state.krisan_data['surviving_plants'] = surviving_plants
        st.session_state.krisan_data['bed_length'] = bed_length
        st.session_state.krisan_data['plants_per_bed'] = plants_per_bed
        st.session_state.krisan_data['actual_density'] = actual_density
        st.session_state.krisan_data['survival_rate'] = survival_rate
        st.session_state.krisan_data['stems_per_plant'] = stems_per_plant
        
        # Variety data for sync with Pasca Panen
        st.session_state.krisan_data['beds_putih'] = beds_putih
        st.session_state.krisan_data['beds_pink'] = beds_pink
        st.session_state.krisan_data['beds_kuning'] = beds_kuning
        st.session_state.krisan_data['plants_putih'] = beds_putih * plants_per_bed
        st.session_state.krisan_data['plants_pink'] = beds_pink * plants_per_bed
        st.session_state.krisan_data['plants_kuning'] = beds_kuning * plants_per_bed
        
        # Display
        st.metric("🌱 Tanaman per Baris", f"{plants_per_row:,}")
        st.metric("📦 Tanaman per Bedengan", f"{plants_per_bed:,}")
        st.metric("🌿 **TOTAL TANAMAN**", f"{total_plants:,}")
        
        st.markdown("---")
        
        st.metric("✅ Tanaman Hidup", f"{surviving_plants:,}", f"Survival {survival_rate}%")
        st.metric("🌸 **TOTAL TANGKAI**", f"{total_stems:,}", f"{stems_per_plant} tangkai/tanaman")
        
        st.markdown("---")
        
        st.metric("📐 Luas Bedengan Total", f"{total_bed_area:.1f} m²")
        st.metric("📊 Densitas", f"{actual_density:.1f} tanaman/m²")

# ==================== TAB 2: NOZZLE & IRIGASI ====================
with tab2:
    st.subheader("💧 Perhitungan Nozzle & Sistem Irigasi")
    
    # Sync badge
    data = st.session_state.krisan_data
    st.markdown(f"""
    <div class="sync-badge">
        📊 <strong>Data Tersinkronisasi:</strong> 
        🌱 Populasi: <strong>{data.get('total_plants', 0):,}</strong> tanaman | 
        📐 Luas: <strong>{data.get('total_bed_area', 0):.1f}</strong> m² |
        📦 Bedengan: <strong>{data.get('num_beds', 0)}</strong> unit
    </div>
    """, unsafe_allow_html=True)
    
    col_irr, col_res = st.columns([1, 1])
    
    with col_irr:
        st.markdown("### ⚙️ Konfigurasi Sistem Irigasi")
        
        irrigation_type = st.selectbox(
            "💧 Jenis Irigasi",
            ["Drip Irrigation", "Sprinkler/Misting", "Manual Selang"]
        )
        
        if irrigation_type == "Drip Irrigation":
            nozzle_spacing = st.selectbox(
                "↔️ Jarak Antar Dripper (cm)",
                [15, 20, 25, 30],
                index=1,
                help="Jarak dripper dalam selang PE"
            )
            lines_per_bed = st.selectbox(
                "📏 Jumlah Lateral per Bedengan",
                [2, 3, 4],
                index=1,
                help="Jumlah selang PE per bedengan"
            )
        elif irrigation_type == "Sprinkler/Misting":
            nozzle_spacing = st.selectbox(
                "↔️ Jarak Antar Nozzle (meter)",
                [1, 1.5, 2, 2.5, 3],
                index=2
            )
            lines_per_bed = 1
        else:
            nozzle_spacing = 100
            lines_per_bed = 1
        
        st.markdown("### 💰 Biaya Komponen")
        
        price_per_nozzle = st.number_input(
            "💧 Harga per Nozzle/Dripper (Rp)",
            500, 10000, 2500, 100
        )
        
        price_pe_pipe = st.number_input(
            "🔧 Harga Pipa PE per meter (Rp)",
            2000, 20000, 5000, 500
        )
        
        price_mainpipe = st.number_input(
            "🔧 Harga Pipa Utama PVC per meter (Rp)",
            10000, 50000, 25000, 1000
        )
        
        mainpipe_length = st.number_input(
            "📏 Panjang Pipa Utama (meter)",
            10, 200, 50, 5
        )
        
        price_pump = st.number_input(
            "⚙️ Harga Pompa (Rp)",
            500000, 5000000, 1500000, 100000
        )
        
        price_filter = st.number_input(
            "🔧 Harga Filter & Fitting (Rp)",
            200000, 2000000, 500000, 50000
        )
    
    with col_res:
        st.markdown("### 📊 Hasil Perhitungan Irigasi")
        
        # Get data from session
        num_beds = data.get('num_beds', 12)
        bed_length = data.get('bed_length', 25)
        total_bed_area = data.get('total_bed_area', 300)
        
        # Calculate nozzles
        if irrigation_type == "Drip Irrigation":
            nozzles_per_line = int((bed_length * 100) / nozzle_spacing)
            nozzles_per_bed = nozzles_per_line * lines_per_bed
            total_nozzles = nozzles_per_bed * num_beds
            pe_length_per_bed = bed_length * lines_per_bed
            total_pe_length = pe_length_per_bed * num_beds
        elif irrigation_type == "Sprinkler/Misting":
            nozzles_per_bed = int(bed_length / nozzle_spacing) + 1
            total_nozzles = nozzles_per_bed * num_beds
            total_pe_length = bed_length * num_beds
        else:
            total_nozzles = 0
            total_pe_length = 0
        
        # Costs
        cost_nozzles = total_nozzles * price_per_nozzle
        cost_pe = total_pe_length * price_pe_pipe
        cost_mainpipe = mainpipe_length * price_mainpipe
        total_irrigation_cost = cost_nozzles + cost_pe + cost_mainpipe + price_pump + price_filter
        
        # Update session state
        st.session_state.krisan_data['nozzle_count'] = total_nozzles
        st.session_state.krisan_data['irrigation_cost'] = total_irrigation_cost
        
        # Display
        st.metric("💧 Total Nozzle/Dripper", f"{total_nozzles:,}")
        st.metric("📏 Total Pipa PE", f"{total_pe_length:.0f} meter")
        
        st.markdown("---")
        
        st.markdown("**💰 Rincian Biaya Irigasi:**")
        
        irr_breakdown = pd.DataFrame({
            "Komponen": ["Nozzle/Dripper", "Pipa PE", "Pipa Utama PVC", "Pompa", "Filter & Fitting"],
            "Biaya": [cost_nozzles, cost_pe, cost_mainpipe, price_pump, price_filter]
        })
        
        for _, row in irr_breakdown.iterrows():
            st.markdown(f"- {row['Komponen']}: **Rp {row['Biaya']:,.0f}**")
        
        st.markdown("---")
        st.metric("💰 **TOTAL BIAYA IRIGASI**", f"Rp {total_irrigation_cost:,.0f}")
        
        cost_per_m2 = total_irrigation_cost / total_bed_area if total_bed_area > 0 else 0
        st.caption(f"Biaya per m²: Rp {cost_per_m2:,.0f}")

# ==================== TAB 3: RAB LENGKAP ====================
with tab3:
    st.subheader("💰 Rencana Anggaran Biaya (RAB) Lengkap")
    
    # Sync badge
    data = st.session_state.krisan_data
    st.markdown(f"""
    <div class="sync-badge">
        📊 <strong>Data Tersinkronisasi dari Tab Lain:</strong><br>
        🌱 Populasi: <strong>{data.get('total_plants', 0):,}</strong> tanaman | 
        Luas: <strong>{data.get('total_bed_area', 0):.1f}</strong> m²<br>
        💧 Irigasi: <strong>{data.get('nozzle_count', 0):,}</strong> nozzle | 
        Biaya Instalasi: <strong>Rp {data.get('irrigation_cost', 0):,.0f}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    col_rab1, col_rab2 = st.columns([1, 1])
    
    with col_rab1:
        st.markdown("### 🏗️ A. Investasi Awal (Modal Tetap)")
        
        # Get number of houses for scaling logic (reused from Part B logic for consistency)
        house_db = st.session_state.get('house_database', {})
        num_houses = len(house_db) if house_db else 1
        
        # Cost input mode for Investment - reusing the concept or adding a specific one
        # To keep it clean, let's auto-detect or ask. 
        # Since Part B has a toggle, Part A should likely have one too or share it. 
        # But Part A is at the top. Let's add a toggle here specifically for Investment scaling.
        
        inv_input_mode = st.radio(
            "Mode Input Investasi:",
            ["Input Total (Semua House)", "Input Per House (Otomatis dikali Jml House)"],
            index=1,
            key="inv_mode",
            help=f"Jika Mode 'Per House' dipilih, investasi akan dikalikan dengan {num_houses} house."
        )
        inv_multiplier = num_houses if "Per House" in inv_input_mode else 1
        
        if inv_multiplier > 1:
            st.info(f"💡 Investasi Greenhouse, Lampu, dll akan dikalikan **{inv_multiplier} house**")

        with st.expander("📐 Konstruksi Greenhouse", expanded=True):
            greenhouse_area = st.number_input("Luas Greenhouse per House (m²)", 100, 5000, 400, 50)
            cost_gh_per_m2 = st.number_input("Biaya per m² (Rp)", 100000, 500000, 250000, 10000)
            cost_greenhouse = greenhouse_area * cost_gh_per_m2 * inv_multiplier
            st.metric("Subtotal Greenhouse", f"Rp {cost_greenhouse:,.0f}", f"x {inv_multiplier} house" if inv_multiplier > 1 else "")
        
        with st.expander("💧 Sistem Irigasi (dari Tab 2)"):
            # Irrigation cost from Tab 2 is usually total if configured per house logic there.
            # But let's check. Default 7.5M is likely per house.
            base_irrigation = data.get('irrigation_cost', 7500000)
            # If data comes from Tab 2, it might already be total if tab 2 handles multiple houses.
            # But usually Tab 2 calculates for "Current Configuration". 
            # If house_db exists, Tab 2 might be just one instance. 
            # Safest is to apply multiplier if it looks small, but user chose "Per House".
            # Let's trust the Multiplier logic for Consistency.
            irrigation_cost = base_irrigation * inv_multiplier
            st.metric("Subtotal Irigasi", f"Rp {irrigation_cost:,.0f}", f"x {inv_multiplier} house" if inv_multiplier > 1 else "")
        
        with st.expander("💡 Sistem Lampu (Photoperiod)"):
            num_lamps = st.number_input("Jumlah Lampu per House", 10, 200, 50, 5)
            cost_per_lamp = st.number_input("Harga per Lampu (Rp)", 50000, 500000, 150000, 10000)
            cost_installation = st.number_input("Biaya Instalasi Listrik per House (Rp)", 500000, 5000000, 2000000, 100000)
            cost_lighting = ((num_lamps * cost_per_lamp) + cost_installation) * inv_multiplier
            st.metric("Subtotal Lampu", f"Rp {cost_lighting:,.0f}", f"x {inv_multiplier} house" if inv_multiplier > 1 else "")
        
        with st.expander("🌑 Plastik Hitam (Shading)"):
            shading_area = st.number_input("Luas Shading per House (m²)", 100, 5000, int(data.get('total_bed_area', 300)), 50)
            cost_shading_per_m2 = st.number_input("Harga Plastik per m² (Rp)", 5000, 30000, 15000, 1000)
            cost_shading = shading_area * cost_shading_per_m2 * inv_multiplier
            st.metric("Subtotal Shading", f"Rp {cost_shading:,.0f}", f"x {inv_multiplier} house" if inv_multiplier > 1 else "")
        
        with st.expander("🔧 Peralatan Lain"):
            cost_tools = st.number_input("Peralatan per House (Rp)", 1000000, 10000000, 3000000, 500000)
            cost_tools = cost_tools * inv_multiplier
            st.metric("Subtotal Peralatan", f"Rp {cost_tools:,.0f}", f"x {inv_multiplier} house" if inv_multiplier > 1 else "")
        
        total_investment = cost_greenhouse + irrigation_cost + cost_lighting + cost_shading + cost_tools
        
        st.markdown("---")
        st.metric("💼 **TOTAL INVESTASI AWAL**", f"Rp {total_investment:,.0f}")
        
        # Save total investment to session state
        st.session_state.krisan_data['total_investment'] = total_investment
    
    with col_rab2:
        st.markdown("### 💵 B. Biaya Operasional (per Siklus)")
        
        total_plants = data.get('total_plants', 20000)
        total_bed_area = data.get('total_bed_area', 300)
        
        # Get number of houses for scaling logic
        house_db = st.session_state.get('house_database', {})
        num_houses = len(house_db) if house_db else 1
        
        st.markdown("### ⚙️ Mode Input Biaya Periodik")
        cost_input_mode = st.radio(
            "Untuk Tenaga Kerja, Listrik, Air, dll:",
            ["Input Total (Semua House)", "Input Per House (Otomatis dikali Jml House)"],
            index=1,
            help=f"Jika Mode 'Per House' dipilih, biaya akan dikalikan dengan {num_houses} house."
        )
        
        cost_multiplier = num_houses if "Per House" in cost_input_mode else 1
        
        if cost_multiplier > 1:
            st.info(f"💡 Biaya Tenaga Kerja, Listrik, Air, dll akan dikalikan **{cost_multiplier} house**")
        
        # Variable Costs (Already scaled by area/quantity)
        with st.expander("🌱 Bibit/Stek", expanded=True):
            cost_cutting = st.number_input("Harga per Stek (Rp)", 200, 1000, 400, 50)
            cost_cuttings_total = total_plants * cost_cutting
            st.metric("Subtotal Bibit", f"Rp {cost_cuttings_total:,.0f}", f"{total_plants:,} stek")
        
        with st.expander("🧪 Pupuk"):
            cost_fertilizer_m2 = st.number_input("Biaya Pupuk per m² (Rp)", 1000, 10000, 3000, 200)
            cost_fertilizer = total_bed_area * cost_fertilizer_m2
            st.metric("Subtotal Pupuk", f"Rp {cost_fertilizer:,.0f}")
        
        with st.expander("🛡️ Pestisida"):
            cost_pesticide_m2 = st.number_input("Biaya Pestisida per m² (Rp)", 500, 5000, 2000, 200)
            cost_pesticide = total_bed_area * cost_pesticide_m2
            st.metric("Subtotal Pestisida", f"Rp {cost_pesticide:,.0f}")
        
        # Fixed/Periodic Costs (Need scaling)
        with st.expander("👷 Tenaga Kerja"):
            labor_daily = st.number_input("Upah Harian (Rp)", 50000, 150000, 80000, 5000)
            labor_days = st.number_input("Hari Kerja per Siklus (per House)", 60, 120, 90, 5)
            # Apply multiplier
            cost_labor = labor_daily * labor_days * cost_multiplier
            st.metric("Subtotal Tenaga Kerja", f"Rp {cost_labor:,.0f}", f"x {cost_multiplier} house" if cost_multiplier > 1 else "")
        
        with st.expander("⚡ Listrik"):
            cost_electricity = st.number_input("Biaya Listrik per Bulan (Rp/House)", 200000, 2000000, 600000, 50000)
            months_per_cycle = 4
            # Apply multiplier
            cost_electricity_total = cost_electricity * months_per_cycle * cost_multiplier
            st.metric("Subtotal Listrik", f"Rp {cost_electricity_total:,.0f}", f"{months_per_cycle} bulan x {cost_multiplier} house")
        
        with st.expander("📦 Lain-lain"):
            cost_other = st.number_input("Biaya Lain-lain (Rp/House)", 0, 5000000, 500000, 100000)
            # Apply multiplier
            cost_other = cost_other * cost_multiplier
            st.metric("Subtotal Lainnya", f"Rp {cost_other:,.0f}", f"x {cost_multiplier} house" if cost_multiplier > 1 else "")
        
        # NEW COST COMPONENTS (Already Added previously, checking if scaling needed)
        with st.expander("🌱 Media Tanam"):
            media_cost_per_m2 = st.number_input("Biaya Media per m² (Rp)", 1000, 10000, 3000, 500, key="media_cost")
            media_cost = total_bed_area * media_cost_per_m2
            st.metric("Subtotal Media Tanam", f"Rp {media_cost:,.0f}")
            st.caption("Sekam bakar, cocopeat, kompos")
        
        with st.expander("🛡️ Plastik Mulsa"):
            mulsa_cost_per_m2 = st.number_input("Biaya Mulsa per m² (Rp)", 5000, 30000, 15000, 1000, key="mulsa_cost")
            mulsa_lifespan = st.selectbox("Umur Pakai (siklus)", [1, 2, 3], index=1, key="mulsa_life")
            mulsa_cost = (total_bed_area * mulsa_cost_per_m2) / mulsa_lifespan
            st.metric("Subtotal Plastik Mulsa", f"Rp {mulsa_cost:,.0f}")
            st.caption(f"Amortisasi {mulsa_lifespan} siklus")
        
        with st.expander("📦 Bahan Habis Pakai"):
            # Variable cost, scales with plants (already total)
            consumable_per_plant = st.number_input("Biaya per Tanaman (Rp)", 20, 200, 50, 10, key="consumable")
            consumable_cost = total_plants * consumable_per_plant
            st.metric("Subtotal Bahan Habis Pakai", f"Rp {consumable_cost:,.0f}")
            st.caption("Tali rafia, ajir, label, karet")
        
        with st.expander("💧 Air"):
            water_cost_monthly = st.number_input("Biaya Air per Bulan (Rp/House)", 100000, 2000000, 500000, 50000, key="water")
            # Apply multiplier
            water_cost = water_cost_monthly * 4 * cost_multiplier
            st.metric("Subtotal Air", f"Rp {water_cost:,.0f}", f"4 bulan x {cost_multiplier} house")
        
        with st.expander("🔧 Pemeliharaan & Perbaikan"):
            maintenance_pct = st.slider("% dari Investasi/tahun", 1, 10, 5, key="maintenance_pct")
            # Using estimated investment if total_investment variable not available in this scope easily, 
            # OR better to use total_investment if computed above, but let's use logic consistent with previous step
            estimated_investment = 200000000 * num_houses # Scale investment estimate by number of houses
            cycles_per_year_est = 3
            maintenance_cost = (estimated_investment * maintenance_pct / 100) / cycles_per_year_est
            st.metric("Subtotal Pemeliharaan", f"Rp {maintenance_cost:,.0f}")
            st.caption("Service pompa, perbaikan greenhouse")
        
        with st.expander("✂️ Grading & Sortir"):
            # Calculate total stems for grading
            total_stems_rab = int(total_plants * 0.85 * 3.5)  # Default survival 85%, stems 3.5
            grading_per_stem = st.number_input("Biaya per Tangkai (Rp)", 20, 200, 75, 5, key="grading")
            grading_cost = total_stems_rab * grading_per_stem
            st.metric("Subtotal Grading", f"Rp {grading_cost:,.0f}")
            st.caption(f"Untuk {total_stems_rab:,} tangkai")
        
        with st.expander("📦 Packaging"):
            packaging_per_stem = st.number_input("Biaya per Tangkai (Rp)", 50, 300, 150, 10, key="packaging")
            packaging_cost = total_stems_rab * packaging_per_stem
            st.metric("Subtotal Packaging", f"Rp {packaging_cost:,.0f}")
            st.caption("Kardus, plastik wrap, label")
        
        with st.expander("🚚 Transportasi"):
            transport_cost = st.number_input("Biaya Transport per Siklus (Rp)", 500000, 10000000, 2000000, 100000, key="transport")
            st.metric("Subtotal Transportasi", f"Rp {transport_cost:,.0f}")
            st.caption("Angkut input & distribusi output")
        
        total_operational = (
            cost_cuttings_total + 
            cost_fertilizer + 
            cost_pesticide + 
            cost_labor + 
            cost_electricity_total + 
            cost_other +
            media_cost +
            mulsa_cost +
            consumable_cost +
            water_cost +
            maintenance_cost +
            grading_cost +
            packaging_cost +
            transport_cost
        )
        
        # Save RAB estimates to session state for sync with Jurnal Harian
        st.session_state.krisan_data['rab_bibit'] = cost_cuttings_total
        st.session_state.krisan_data['rab_pupuk'] = cost_fertilizer
        st.session_state.krisan_data['rab_pestisida'] = cost_pesticide
        st.session_state.krisan_data['rab_tenaga_kerja'] = cost_labor
        st.session_state.krisan_data['rab_listrik'] = cost_electricity_total
        st.session_state.krisan_data['rab_lainnya'] = cost_other
        # New cost components
        st.session_state.krisan_data['rab_media'] = media_cost
        st.session_state.krisan_data['rab_mulsa'] = mulsa_cost
        st.session_state.krisan_data['rab_consumables'] = consumable_cost
        st.session_state.krisan_data['rab_water'] = water_cost
        st.session_state.krisan_data['rab_maintenance'] = maintenance_cost
        st.session_state.krisan_data['rab_grading'] = grading_cost
        st.session_state.krisan_data['rab_packaging'] = packaging_cost
        st.session_state.krisan_data['rab_transport'] = transport_cost
        st.session_state.krisan_data['rab_total_operational'] = total_operational
        
        st.markdown("---")
        st.metric("💵 **TOTAL OPERASIONAL/SIKLUS**", f"Rp {total_operational:,.0f}")
    
    # SUMMARY
    st.markdown("---")
    st.subheader("📊 Ringkasan RAB & Proyeksi Keuntungan")
    
    col_sum1, col_sum2, col_sum3 = st.columns(3)
    
    # Calculate total_stems properly from population data
    total_plants = data.get('total_plants', 0)
    survival_rate = data.get('survival_rate', 85) / 100  # Convert to decimal
    stems_per_plant = data.get('stems_per_plant', 3.5)
    
    # If total_plants is 0, try to get from house_database
    if total_plants == 0 and 'house_database' in st.session_state and st.session_state.house_database:
        total_plants = sum(h.get('total_plants', 0) for h in st.session_state.house_database.values())
    
    # Calculate total stems
    surviving_plants = int(total_plants * survival_rate)
    total_stems = int(surviving_plants * stems_per_plant)
    
    # Update session state with calculated value
    st.session_state.krisan_data['total_stems'] = total_stems
    
    with col_sum1:
        st.markdown("**📥 Pendapatan & Optimisasi**")
        # Fix min value 5000 -> 100 to allow simulation of low prices
        selling_price = st.number_input("Harga Jual (Rp/tangkai)", 100, 25000, 12000, 100, help="Ubah untuk simulasi profit")
        cycles_per_year = st.selectbox(
            "Siklus/Tahun", 
            [2, 3, 4], 
            index=1,
            help="Estimasi: 1 siklus krisan = 3.5 - 4 bulan. \n- 3 Siklus = Standar (ada jeda istirahat lahan)\n- 4 Siklus = Intensif (manajemen jeda sangat singkat)"
        )
        
        revenue_cycle = total_stems * selling_price
        revenue_year = revenue_cycle * cycles_per_year
        
        st.metric("Pendapatan/Siklus", f"Rp {revenue_cycle:,.0f}")
        st.metric("Pendapatan/Tahun", f"Rp {revenue_year:,.0f}")
        
        st.markdown("📉 **Batas Aman (Break-Even):**")
        # Safety Limits / BEP Analysis
        # 1. Min Price (Cost per Stem) to break even
        cost_per_stem_limit = total_operational / total_stems if total_stems > 0 else 0
        st.metric("Harga Jual Minimum", f"Rp {cost_per_stem_limit:,.0f}", help="Jika harga jual di bawah ini, Anda rugi (Operational only)")
        
        # 2. Min Production (Stems) to break even at current price
        # BEP Units = Total Cost / Price
        min_stems_limit = int(total_operational / selling_price) if selling_price > 0 else 0
        st.metric("Produksi Minimum", f"{min_stems_limit:,} tangkai", help="Jika produksi di bawah ini, Anda rugi")
    
    with col_sum2:
        st.markdown("**📤 Total Biaya**")
        operational_year = total_operational * cycles_per_year
        
        st.metric("Operasional/Siklus", f"Rp {total_operational:,.0f}")
        st.metric("Operasional/Tahun", f"Rp {operational_year:,.0f}")
        st.metric("Investasi Awal", f"Rp {total_investment:,.0f}")
    
    with col_sum3:
        st.markdown("**💰 Profit & ROI**")
        profit_cycle = revenue_cycle - total_operational
        profit_year = profit_cycle * cycles_per_year
        roi = (profit_year / total_investment * 100) if total_investment > 0 else 0
        payback = (total_investment / profit_year) if profit_year > 0 else 999
        
        st.metric("Profit/Siklus", f"Rp {profit_cycle:,.0f}",
                  delta_color="normal" if profit_cycle > 0 else "inverse")
        st.metric("Profit/Tahun", f"Rp {profit_year:,.0f}",
                  delta_color="normal" if profit_year > 0 else "inverse")
        st.metric("ROI", f"{roi:.1f}%/tahun")
        st.metric("Payback Period", f"{payback:.1f} tahun")

# ==================== TAB 4: AI OPTIMASI ====================
with tab4:
    st.subheader("🤖 AI Optimasi & Rekomendasi")
    
    data = st.session_state.krisan_data
    
    st.markdown(f"""
    <div class="sync-badge">
        📊 <strong>Analisis berdasarkan data Anda:</strong><br>
        🌱 {data.get('total_plants', 0):,} tanaman | 
        🌸 {data.get('total_stems', 0):,} tangkai | 
        📐 {data.get('total_bed_area', 0):.1f} m²
    </div>
    """, unsafe_allow_html=True)
    
    # AI Analysis
    total_plants = data.get('total_plants', 20000)
    total_stems = data.get('total_stems', 50000)
    total_bed_area = data.get('total_bed_area', 300)
    nozzle_count = data.get('nozzle_count', 1000)
    
    density = total_plants / total_bed_area if total_bed_area > 0 else 0
    
    st.markdown("### 🎯 Analisis & Rekomendasi")
    
    recommendations = []
    
    # Density analysis
    if density < 50:
        recommendations.append({
            "type": "warning",
            "title": "📊 Densitas Rendah",
            "desc": f"Densitas {density:.1f}/m² di bawah optimal (64/m²). Pertimbangkan mengurangi jarak tanam untuk meningkatkan produktivitas."
        })
    elif density > 80:
        recommendations.append({
            "type": "warning", 
            "title": "📊 Densitas Terlalu Tinggi",
            "desc": f"Densitas {density:.1f}/m² terlalu padat. Risiko: sirkulasi udara buruk, penyakit mudah menyebar. Kurangi baris atau tambah jarak tanam."
        })
    else:
        recommendations.append({
            "type": "success",
            "title": "✅ Densitas Optimal",
            "desc": f"Densitas {density:.1f}/m² sudah dalam range optimal (50-80/m²)."
        })
    
    # Irrigation analysis
    plants_per_nozzle = total_plants / nozzle_count if nozzle_count > 0 else 0
    if plants_per_nozzle > 25:
        recommendations.append({
            "type": "warning",
            "title": "💧 Nozzle Kurang",
            "desc": f"Ratio {plants_per_nozzle:.0f} tanaman/nozzle terlalu tinggi. Tambahkan nozzle untuk distribusi air merata."
        })
    elif nozzle_count > 0:
        recommendations.append({
            "type": "success",
            "title": "✅ Irigasi Memadai",
            "desc": f"Ratio {plants_per_nozzle:.0f} tanaman/nozzle sudah baik."
        })
    
    # Production optimization
    recommendations.append({
        "type": "info",
        "title": "💡 Tips Meningkatkan Produksi",
        "desc": """
        - Pinching yang tepat bisa meningkatkan tangkai/tanaman dari 3.5 ke 4-5
        - Photoperiod ketat (14 jam gelap) untuk pembungaan optimal
        - Suhu malam 15-18°C untuk warna bunga lebih intens
        """
    })
    
    # Market timing
    recommendations.append({
        "type": "info",
        "title": "📅 Timing Pasar",
        "desc": """
        **Peak Demand:** Valentine (Feb), Imlek (Jan-Feb), Mother's Day (Mei)
        **Strategi:** Tanam mundur 105 hari dari peak untuk panen tepat waktu.
        """
    })
    
    # Display recommendations
    for rec in recommendations:
        if rec["type"] == "success":
            st.success(f"**{rec['title']}**\n\n{rec['desc']}")
        elif rec["type"] == "warning":
            st.warning(f"**{rec['title']}**\n\n{rec['desc']}")
        else:
            st.info(f"**{rec['title']}**\n\n{rec['desc']}")
    
    # Profit optimization scenarios
    st.markdown("---")
    st.markdown("### 📈 Skenario Optimasi Profit")
    
    scenarios = pd.DataFrame({
        "Skenario": ["Kondisi Saat Ini", "Optimasi Densitas", "Tingkatkan Survival", "Premium Market"],
        "Tanaman": [total_plants, int(total_plants * 1.2), total_plants, total_plants],
        "Survival": [85, 85, 92, 85],
        "Harga": [12000, 12000, 12000, 18000],
        "Tangkai/Tanaman": [3.5, 3.5, 3.5, 3.5]
    })
    
    scenarios["Tangkai"] = (scenarios["Tanaman"] * scenarios["Survival"] / 100 * scenarios["Tangkai/Tanaman"]).astype(int)
    scenarios["Pendapatan"] = scenarios["Tangkai"] * scenarios["Harga"]
    scenarios["Pendapatan (Rp)"] = scenarios["Pendapatan"].apply(lambda x: f"Rp {x:,.0f}")
    
    # Calculate potential increase
    base_revenue = scenarios.iloc[0]["Pendapatan"]
    scenarios["Peningkatan"] = ((scenarios["Pendapatan"] - base_revenue) / base_revenue * 100).apply(lambda x: f"+{x:.1f}%" if x > 0 else "-")
    
    st.dataframe(
        scenarios[["Skenario", "Tanaman", "Survival", "Harga", "Tangkai", "Pendapatan (Rp)", "Peningkatan"]],
        use_container_width=True,
        hide_index=True
    )

# ==================== TAB 5: ANALISIS TAHUNAN ====================
with tab5:
    st.subheader("📈 Analisis Usaha Tahunan - Semua House")
    st.info("Proyeksi produksi dan pendapatan 1 tahun berdasarkan konfigurasi house")
    
    # Get house data from database or use defaults
    if 'house_database' in st.session_state and st.session_state.house_database:
        houses = st.session_state.house_database
        num_houses = len(houses)
        st.success(f"📊 Data dari {num_houses} house tersinkronisasi")
    else:
        # Use defaults
        num_houses = 4
        houses = {}
        for i in range(num_houses):
            houses[f"house_{i+1}"] = {
                'name': f"House {i+1}",
                'beds': DEFAULT_CONFIG['beds_per_house'],
                'bed_length': DEFAULT_CONFIG['bed_length'],
                'rows_per_bed': DEFAULT_CONFIG['rows_per_bed'],
                'plant_spacing': DEFAULT_CONFIG['plant_spacing'],
                'total_plants': DEFAULT_PLANTS_PER_BED * DEFAULT_CONFIG['beds_per_house'],
                'beds_putih': 4, 'beds_pink': 4, 'beds_kuning': 4
            }
        st.warning("⚠️ Menggunakan default. Simpan konfigurasi di Tab Populasi untuk data akurat.")
    
    st.markdown("---")
    
    # Annual Parameters
    st.markdown("### ⚙️ Parameter Analisis Tahunan")
    
    param_cols = st.columns([1, 1, 1, 1])
    
    with param_cols[0]:
        cycle_days = st.number_input("⏱️ Siklus (hari)", 90, 150, 115, help="Veg + Gen + Panen + Jeda")
    
    with param_cols[1]:
        cycles_per_year = 365 // cycle_days
        st.metric("📊 Siklus/Tahun", f"{cycles_per_year} siklus")
    
    with param_cols[2]:
        stems_per_plant = st.number_input("🌸 Tangkai/Tanaman", 1.0, 3.0, 1.0, step=0.5, help="1 tanaman = 1 tangkai bunga")
    
    with param_cols[3]:
        survival_rate = st.number_input("✅ Survival Rate (%)", 70, 100, 90) / 100
    
    st.markdown("### 💰 Parameter Harga & Biaya")
    
    price_cols = st.columns([1, 1, 1])
    
    with price_cols[0]:
        avg_price = st.number_input("💵 Harga Jual Rata-rata (Rp/btg)", 500, 2000, 1000, step=50)
    
    with price_cols[1]:
        cost_per_plant = st.number_input("💸 Biaya per Tanaman (Rp)", 200, 1000, 450, step=50)
    
    with price_cols[2]:
        overhead_monthly = st.number_input("🏢 Overhead/Bulan (Rp)", 1000000, 20000000, 5000000, step=500000)
    
    st.markdown("---")
    
    # Calculate totals
    st.markdown("### 📊 Ringkasan Produksi Tahunan")
    
    # Per-house calculations
    annual_data = []
    total_plants_all = 0
    total_stems_all = 0
    total_revenue_all = 0
    total_cost_all = 0
    
    for key, house in houses.items():
        plants_per_cycle = house.get('total_plants', DEFAULT_PLANTS_PER_BED * 12)
        surviving_plants = int(plants_per_cycle * survival_rate)
        stems_per_cycle = int(surviving_plants * stems_per_plant)
        
        annual_plants = plants_per_cycle * cycles_per_year
        annual_stems = stems_per_cycle * cycles_per_year
        annual_revenue = annual_stems * avg_price
        annual_cost = (plants_per_cycle * cost_per_plant * cycles_per_year)
        annual_profit = annual_revenue - annual_cost
        
        total_plants_all += annual_plants
        total_stems_all += annual_stems
        total_revenue_all += annual_revenue
        total_cost_all += annual_cost
        
        annual_data.append({
            "House": house.get('name', key),
            "Bedengan": house.get('beds', 12),
            "Tanaman/Siklus": f"{plants_per_cycle:,}",
            "Tangkai/Tahun": f"{annual_stems:,}",
            "Pendapatan": f"Rp {annual_revenue:,.0f}",
            "Biaya": f"Rp {annual_cost:,.0f}",
            "Profit": f"Rp {annual_profit:,.0f}"
        })
    
    # Add overhead
    total_overhead = overhead_monthly * 12
    total_cost_with_overhead = total_cost_all + total_overhead
    total_profit = total_revenue_all - total_cost_with_overhead
    
    st.dataframe(pd.DataFrame(annual_data), use_container_width=True, hide_index=True)
    
    # Summary metrics
    st.markdown("### 💰 Ringkasan Keuangan Tahunan")
    
    sum_cols = st.columns(4)
    
    with sum_cols[0]:
        st.metric("🌱 Total Tanaman/Tahun", f"{total_plants_all:,}")
    with sum_cols[1]:
        st.metric("🌸 Total Tangkai/Tahun", f"{total_stems_all:,}")
    with sum_cols[2]:
        st.metric("💵 Total Pendapatan", f"Rp {total_revenue_all:,.0f}")
    with sum_cols[3]:
        st.metric("💸 Total Biaya Produksi", f"Rp {total_cost_all:,.0f}")
    
    st.markdown("---")
    
    fin_cols = st.columns(3)
    
    with fin_cols[0]:
        st.metric("🏢 Overhead Tahunan", f"Rp {total_overhead:,.0f}", f"Rp {overhead_monthly:,}/bulan")
    
    with fin_cols[1]:
        st.metric("💸 Total Biaya (+ Overhead)", f"Rp {total_cost_with_overhead:,.0f}")
    
    with fin_cols[2]:
        profit_color = "normal" if total_profit > 0 else "inverse"
        margin = (total_profit / total_revenue_all * 100) if total_revenue_all > 0 else 0
        st.metric("📈 **NET PROFIT TAHUNAN**", f"Rp {total_profit:,.0f}", f"Margin: {margin:.1f}%", delta_color=profit_color)
    
    # Monthly breakdown
    st.markdown("### 📅 Proyeksi Bulanan")
    
    monthly_revenue = total_revenue_all / 12
    monthly_cost = total_cost_with_overhead / 12
    monthly_profit = total_profit / 12
    
    m_cols = st.columns(3)
    with m_cols[0]:
        st.metric("💵 Pendapatan/Bulan", f"Rp {monthly_revenue:,.0f}")
    with m_cols[1]:
        st.metric("💸 Biaya/Bulan", f"Rp {monthly_cost:,.0f}")
    with m_cols[2]:
        st.metric("📈 Profit/Bulan", f"Rp {monthly_profit:,.0f}")
    
    # ROI calculation
    st.markdown("### 📊 Analisis ROI")
    
    roi_cols = st.columns([1, 1, 1.5])
    
    with roi_cols[0]:
        initial_investment = st.number_input("💰 Modal Awal (Rp)", 50000000, 500000000, 150000000, step=10000000)
    
    with roi_cols[1]:
        if total_profit > 0:
            roi_pct = (total_profit / initial_investment) * 100
            bep_months = initial_investment / monthly_profit if monthly_profit > 0 else 0
            st.metric("📈 ROI/Tahun", f"{roi_pct:.1f}%")
        else:
            st.metric("📈 ROI/Tahun", "N/A", "Rugi")
    
    with roi_cols[2]:
        if total_profit > 0 and monthly_profit > 0:
            st.metric("⏱️ Break Even Point", f"{bep_months:.1f} bulan")
        else:
            st.metric("⏱️ Break Even Point", "N/A")
    
    # Summary box
    st.markdown("---")
    st.markdown(f"""
    <div class="sync-badge">
        <strong>📈 RINGKASAN ANALISIS TAHUNAN ({num_houses} House)</strong><br><br>
        📦 Total Bedengan: <strong>{sum(h.get('beds', 12) for h in houses.values())}</strong> |
        🌱 Tanaman/Tahun: <strong>{total_plants_all:,}</strong> |
        🌸 Tangkai/Tahun: <strong>{total_stems_all:,}</strong><br><br>
        💵 Pendapatan: <strong>Rp {total_revenue_all:,.0f}</strong> |
        💸 Biaya: <strong>Rp {total_cost_with_overhead:,.0f}</strong> |
        📈 Profit: <strong>Rp {total_profit:,.0f}</strong><br><br>
        📊 Margin: <strong>{margin:.1f}%</strong> |
        📈 ROI: <strong>{roi_pct:.1f}%</strong> |
        ⏱️ BEP: <strong>{bep_months:.1f} bulan</strong>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Kalkulator Lengkap dengan Sinkronisasi Data")
