import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import hashlib
import io
import qrcode
from datetime import datetime, timedelta

# --- CONFIG & DATA PATHS ---
# from utils.auth import require_auth, show_user_info_sidebar

DATA_DIR = "data"
WASTE_LOG_FILE = os.path.join(DATA_DIR, "waste_log.csv")

def init_waste_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(WASTE_LOG_FILE):
        df = pd.DataFrame(columns=['tanggal', 'tipe', 'berat_kg', 'created_at'])
        df.to_csv(WASTE_LOG_FILE, index=False)

@st.cache_data(ttl=60)  # Cache for 60 seconds to improve performance
def load_waste_logs():
    if os.path.exists(WASTE_LOG_FILE):
        return pd.read_csv(WASTE_LOG_FILE)
    return pd.DataFrame(columns=['tanggal', 'tipe', 'berat_kg', 'created_at'])

def save_waste_entry(date, waste_type, weight):
    df = load_waste_logs()
    new_entry = {
        'tanggal': date,
        'tipe': waste_type,
        'berat_kg': weight,
        'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(WASTE_LOG_FILE, index=False)
    st.cache_data.clear()  # Clear cache after new entry

def reset_waste_logs():
    if os.path.exists(WASTE_LOG_FILE):
        df = pd.DataFrame(columns=['tanggal', 'tipe', 'berat_kg', 'created_at'])
        df.to_csv(WASTE_LOG_FILE, index=False)
    return df

# Page Config
st.set_page_config(
    page_title="AgriSensa Eco - Pengolahan Sampah Terpadu",
    page_icon="♻️",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
# user = require_auth()
# show_user_info_sidebar()
# ================================






# Import and inject Design System
try:
    from utils.styles import inject_styles, COLORS
    inject_styles()
except ImportError:
    pass  # Fallback if styles module not available

# Custom CSS for Premium UI
st.markdown("""
<style>
    .main {
        background-color: #f0fdf4;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .jap-sorting-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .jap-sorting-card:hover {
        transform: translateY(-5px);
    }
    /* Premium Gomi Cards */
    .gomi-card-premium {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        min-height: 380px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    .gomi-card-premium:hover {
        transform: scale(1.02);
        box-shadow: 0 15px 45px rgba(0,0,0,0.1);
        border-color: rgba(255,255,255,0.3);
    }
    .gomi-title {
        font-size: 1.4rem;
        font-weight: 800;
        margin-bottom: 5px;
        letter-spacing: 1px;
    }
    .gomi-subtitle {
        font-size: 0.85rem;
        opacity: 0.8;
        margin-bottom: 20px;
        font-style: italic;
    }
    .gomi-list {
        text-align: left;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 20px;
    }
    .gomi-icon-container {
        background: rgba(255,255,255,0.1);
        border-radius: 50%;
        width: 80px;
        height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    }
    
    /* PRINT OPTIMIZATION (STRICT) */
    @media print {
        /* Hide UI clutter */
        [data-testid="stSidebar"], 
        header, 
        footer, 
        .stButton, 
        .stDownloadButton, 
        [data-testid="stHeader"], 
        [data-testid="stToolbar"],
        [data-testid="stNotification"] {
            display: none !important;
        }
        
        /* Layout Fixes for Blank Page and Scrolling */
        .stApp, .main, .block-container, .stAppViewContainer {
            overflow: visible !important;
            height: auto !important;
            min-height: auto !important;
            padding-top: 0 !important;
            margin: 0 !important;
        }
        
        /* Card Printing Fixes */
        .jap-sorting-card, .transformation-card, .gomi-card-premium, .metric-card {
            break-inside: avoid;
            border: 1px solid #ddd !important;
            box-shadow: none !important;
            background: #fff !important;
            color: #000 !important;
            -webkit-print-color-adjust: exact;
        }
        
        /* Typography */
        h1, h2, h3, h4, p, span, div {
            color: #000 !important;
        }
    }
    
    .transformation-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #3b82f6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.07);
        margin-bottom: 20px;
    }
    .highlight-text {
        color: #059669;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.title("♻️ Pengolahan Sampah Terpadu (Circular Economy)")
st.markdown("""
**Transformasi Limbah Menjadi Emas Hijau & Bahan Baku Presisi.** 
Modul ini mengadopsi disiplin pengelolaan sampah ala Jepang untuk mendukung ekosistem AgriSensa.
""")

st.markdown("---")

# --- SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("⚙️ Konfigurasi Parameter")
    st.write("Sesuaikan angka pengali untuk kalkulasi dashboard.")
    
    with st.expander("🌍 Parameter Lingkungan", expanded=True):
        coef_carbon = st.number_input(
            "Koefisien CO2 (kg/kg sampah)", 
            value=0.53, 
            step=0.01,
            help="Jumlah emisi CO2 yang dikurangi per 1kg sampah yang dikelola."
        )
        target_monthly = st.number_input("Target Bulanan (kg)", value=5000, step=500)

    with st.expander("💰 Parameter Ekonomi", expanded=True):
        price_organic = st.number_input(
            "Harga Pupuk (Rp/kg)", 
            value=2500, 
            step=500,
            help="Asumsi nilai ekonomi hasil olahan organik."
        )
        price_filament = st.number_input(
            "Harga Filamen (Rp/kg)", 
            value=150000, 
            step=10000,
            help="Asumsi nilai ekonomi hasil upcycling plastik."
        )

    with st.expander("🏗️ Parameter Investasi (CAPEX)", expanded=False):
        c_shredder = st.number_input("Mesin Shredder (Rp)", 2000000, 50000000, 8000000)
        c_extruder = st.number_input("Mesin Extruder (Rp)", 5000000, 100000000, 12000000)
        c_compost = st.number_input("Instalasi Komposter (Rp)", 1000000, 20000000, 5000000)
        c_other = st.number_input("Peralatan Lainnya (Rp)", 0, 10000000, 2000000)
        total_capex = c_shredder + c_extruder + c_compost + c_other
        
    with st.expander("⚙️ Biaya Operasional (OPEX)", expanded=False):
        o_labor_base = st.number_input("Gaji per Orang (Rp/Bulan)", 1000000, 10000000, 3000000)
        o_maint = st.number_input("Maintenance & Listrik Dasar (Rp)", 100000, 5000000, 750000)
        total_opex_base = o_maint # Dynamic labor added later in simulator
        
    st.divider()
    
    with st.expander("🎯 Target & Efisiensi (Simulator API)", expanded=True):
        st.markdown("**💰 Target Omzet Bulanan**")
        s_target_ferti = st.slider("Target Omzet Pupuk (Juta Rp)", 1, 100, 18, help="Target pendapatan dari penjualan pupuk organik.") * 1e6
        s_target_filam = st.slider("Target Omzet Filamen (Juta Rp)", 10, 500, 225, help="Target pendapatan dari upcycling plastik.") * 1e6
        
        st.markdown("**⚙️ Efisiensi & Kapasitas**")
        s_yield_organic = st.slider("Efisiensi Rendemen Kompos (%)", 20, 60, 40) / 100
        s_machine_cap = st.slider("Kapasitas Mesin (kg/jam)", 1, 20, 5)
        s_waste_per_partner = st.slider("Sampah/Instansi (kg/hari)", 5, 100, 20)

    st.divider()
    
# Init Data
init_waste_data()
df_logs = load_waste_logs()

# --- KPI & BASICS (GLOBAL) ---
total_waste_collected = df_logs['berat_kg'].sum() if not df_logs.empty else 0
organic_processed = df_logs[df_logs['tipe'].str.contains("Organik", na=False)]['berat_kg'].sum() if not df_logs.empty else 0
plastic_recycled = df_logs[df_logs['tipe'].str.contains("Plastik", na=False)]['berat_kg'].sum() if not df_logs.empty else 0

sustainability_rate = ( (organic_processed + plastic_recycled) / total_waste_collected ) * 100 if total_waste_collected > 0 else 0
carbon_offset = total_waste_collected * coef_carbon
money_saved = (organic_processed * price_organic) + (plastic_recycled * price_filament)

# --- STRATEGIC AI & ESG ENGINE (GLOBAL SCOPE) ---
# Monthly required output
req_ferti_month = s_target_ferti / price_organic
req_filam_month = s_target_filam / price_filament

# Daily required weight (30 days)
daily_ferti = req_ferti_month / 30
daily_filam = req_filam_month / 30

# Raw waste required
raw_org_needed = daily_ferti / s_yield_organic
raw_pla_needed = daily_filam / 0.9 # Constant high yield for plastic
total_raw_daily = raw_org_needed + raw_pla_needed

# Infrastructure & Logistics
partners_needed = total_raw_daily / s_waste_per_partner
machine_hours_extrude = daily_filam / s_machine_cap

# Labor & Energy
shifts_needed = max(1, int(machine_hours_extrude / 8) + (1 if machine_hours_extrude % 8 > 0 else 0))
operators_needed = shifts_needed * 2
energy_kwh_daily = machine_hours_extrude * 3.5
energy_cost_daily = energy_kwh_daily * 1500

# Net Carbon
co2_saved_daily = total_raw_daily * coef_carbon
co2_emitted_ops = (energy_kwh_daily * 0.8) + (partners_needed * 0.2)
net_carbon_daily = co2_saved_daily - co2_emitted_ops

# ESG Dimensions
methane_avoided = (organic_processed * 0.5) 
landfill_m3_saved = total_waste_collected / 500
tree_equivalent = (total_waste_collected * coef_carbon) / 22
value_per_kg = ((organic_processed * price_organic) + (plastic_recycled * price_filament)) / (total_waste_collected or 1)
social_jobs = (total_waste_collected / 500) + (partners_needed / 10)
edu_reach = partners_needed * 50
trace_hash = hashlib.sha256(f"AgriSensa_{total_waste_collected}_{datetime.now().strftime('%Y%m%d')}".encode()).hexdigest()[:16].upper()

# Navigation Tabs
tabs = st.tabs([
    "📊 Dashboard & KPI",
    "🇯🇵 Sistem Pemilahan", 
    "🍃 Transformasi Organik", 
    "🧵 Upcycling Plastik", 
    "🤝 Kolaborasi & Matriks",
    "🎯 Blueprint Target AI",
    "🗓️ Roadmap 12 Minggu",
    "📁 Laporan Strategis",
    "🌍 Sustainability Command",
    "💼 Business Intelligence"
])

# --- TAB 0: DASHBOARD & KPI ---
with tabs[0]:
    st.header("📊 Dashboard Operasional & Real-time KPI")
    st.write("Ringkasan aktivitas harian dan performa ekosistem waste-to-value.")
    
    # KPI Metrics
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    kpi_col1.metric("Sustainability Rate", f"{sustainability_rate:.1f}%")
    kpi_col2.metric("Carbon Offset (CO2e)", f"{carbon_offset:,.1f} kg")
    kpi_col3.metric("Economic Value", f"Rp {money_saved/1000000:.2f}M")
    kpi_col4.metric("Instansi Mitra", f"{partners_needed:.0f}", "AI Est.")
    
    st.markdown("---")
    
    # Daily Log Simulation
    st.subheader("📝 Daily Collection Log")
    log_col1, log_col2 = st.columns([1, 2])
    
    with log_col1:
        log_date = st.date_input("Tanggal Transaksi", datetime.now())
        
        waste_categories = [
            "🍃 Organik (Sisa Makanan)", 
            "🍃 Organik (Ranting/Daun)",
            "🧵 Plastik PET (Botol)", 
            "🧵 Plastik HDPE/LDPE (Kemasan)",
            "📦 Kertas & Kardus",
            "🧴 Kaca & Keramik",
            "🥫 Logam & Kaleng",
            "🔌 Elektronik (E-Waste)",
            "🧤 Tekstil/Kain",
            "⚠️ Limbah B3 (Baterai/Lampu)",
            "➕ Lainnya (Input Manual)"
        ]
        
        selected_cat = st.selectbox("Tipe Sampah", waste_categories)
        
        # Manual Input Logic
        if selected_cat == "➕ Lainnya (Input Manual)":
            waste_type_final = st.text_input("Sebutkan Tipe Sampah", placeholder="Misal: Karet, Kayu Besar, dll")
        else:
            waste_type_final = selected_cat

        weight_in = st.number_input("Berat Masuk (kg)", 0.0, 500.0, 25.0)
        if st.button("Simpan Log Aktivitas"):
            if selected_cat == "➕ Lainnya (Input Manual)" and not waste_type_final:
                st.error("Silakan tulis tipe sampah manual Anda!")
            else:
                save_waste_entry(log_date.strftime("%Y-%m-%d"), waste_type_final, weight_in)
                st.success(f"Berhasil mencatat {weight_in}kg {waste_type_final} ke database!")
                st.rerun()
            
    with log_col2:
        # Mini Chart for Progress
        # (Target taken from sidebar)
        current_progress = total_waste_collected

        if not df_logs.empty:
            st.markdown("**📜 Log Terakhir**")
            st.dataframe(df_logs.tail(5), use_container_width=True)
            st.markdown("---")
        
        fig_progress = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = current_progress,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Progress Target Bulanan (kg)"},
            delta = {'reference': target_monthly},
            gauge = {
                'axis': {'range': [None, target_monthly]},
                'bar': {'color': "#0fb981"},
                'steps' : [
                    {'range': [0, 2500], 'color': "#ecfdf5"},
                    {'range': [2500, 5000], 'color': "#d1fae5"}]
            }
        ))
        fig_progress.update_layout(height=280, margin=dict(t=50, b=10))
        st.plotly_chart(fig_progress, use_container_width=True)

    # --- DATA MANAGEMENT (BOTTOM OF TAB 0) ---
    st.divider()
    with st.expander("🛠️ Pengaturan Data (Simulation Mode)", expanded=False):
        st.markdown("#### 🗑️ Hapus Data Log")
        
        # Selective Delete Options - Using selectbox to minimize reruns
        delete_mode = st.selectbox(
            "Pilih Mode Penghapusan:",
            ["🎯 Hapus Data Tertentu", "📅 Hapus Berdasarkan Tanggal", "🏷️ Hapus Berdasarkan Tipe", "⚠️ Hapus Seluruh Data"],
            key="waste_delete_mode"
        )
        
        if delete_mode == "🎯 Hapus Data Tertentu":
            if not df_logs.empty:
                st.markdown("**Pilih entri yang ingin dihapus:**")
                
                # Create selection dataframe with row index
                df_display = df_logs.copy()
                df_display['No'] = range(1, len(df_display) + 1)
                df_display = df_display[['No', 'tanggal', 'tipe', 'berat_kg']]
                
                # Multi-select for deletion
                options = [f"#{row['No']} - {row['tanggal']} | {row['tipe']} | {row['berat_kg']}kg" 
                          for _, row in df_display.iterrows()]
                selected_to_delete = st.multiselect("Pilih entri:", options)
                
                if selected_to_delete and st.button("🗑️ Hapus Entri Terpilih", type="secondary"):
                    # Get indices to delete
                    indices_to_delete = [int(s.split('#')[1].split(' ')[0]) - 1 for s in selected_to_delete]
                    df_logs = df_logs.drop(df_logs.index[indices_to_delete])
                    df_logs.to_csv(WASTE_LOG_FILE, index=False)
                    st.success(f"✅ {len(selected_to_delete)} entri berhasil dihapus!")
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.info("Tidak ada data untuk dihapus.")
        
        elif delete_mode == "📅 Hapus Berdasarkan Tanggal":
            if not df_logs.empty:
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    date_from = st.date_input("Dari Tanggal", value=datetime.now() - timedelta(days=30), key="del_from")
                with col_d2:
                    date_to = st.date_input("Sampai Tanggal", value=datetime.now(), key="del_to")
                
                # Count affected entries
                mask = (pd.to_datetime(df_logs['tanggal']) >= pd.to_datetime(date_from)) & \
                       (pd.to_datetime(df_logs['tanggal']) <= pd.to_datetime(date_to))
                affected_count = mask.sum()
                
                st.warning(f"⚠️ {affected_count} entri akan dihapus (periode {date_from} - {date_to})")
                
                if affected_count > 0 and st.button(f"🗑️ Hapus {affected_count} Entri", type="secondary"):
                    df_logs = df_logs[~mask]
                    df_logs.to_csv(WASTE_LOG_FILE, index=False)
                    st.success(f"✅ {affected_count} entri berhasil dihapus!")
                    st.cache_data.clear()
                    st.rerun()
            else:
                st.info("Tidak ada data untuk dihapus.")
        
        elif delete_mode == "🏷️ Hapus Berdasarkan Tipe":
            if not df_logs.empty:
                unique_types = df_logs['tipe'].unique().tolist()
                selected_types = st.multiselect("Pilih tipe sampah yang ingin dihapus:", unique_types)
                
                if selected_types:
                    affected_count = df_logs[df_logs['tipe'].isin(selected_types)].shape[0]
                    st.warning(f"⚠️ {affected_count} entri dengan tipe terpilih akan dihapus")
                    
                    if st.button(f"🗑️ Hapus {affected_count} Entri", type="secondary"):
                        df_logs = df_logs[~df_logs['tipe'].isin(selected_types)]
                        df_logs.to_csv(WASTE_LOG_FILE, index=False)
                        st.success(f"✅ {affected_count} entri berhasil dihapus!")
                        st.cache_data.clear()
                        st.rerun()
            else:
                st.info("Tidak ada data untuk dihapus.")
        
        else:  # Hapus Seluruh Data
            st.warning("⚠️ **Perhatian:** Menghapus SELURUH data akan menghilangkan semua log aktivitas secara permanen.")
            confirm_delete = st.checkbox("Saya yakin ingin menghapus seluruh data simulasi.")
            if st.button("🗑️ Hapus Seluruh Database Log", type="secondary", disabled=not confirm_delete):
                reset_waste_logs()
                st.success("Database berhasil dibersihkan! Me-refresh aplikasi...")
                st.cache_data.clear()
                st.rerun()

# --- TAB 1: SISTEM PEMILAHAN ---
with tabs[1]:
    st.header("🇯🇵 Pola Pemilahan Gaya Jepang (Gomi Hiroi)")
    st.info("Kunci keberhasilan pengolahan adalah pada **Disiplin Pemilahan di Sumber**.")
    
    # --- SECTION 1: VISUAL GOMI BOARD ---
    st.subheader("🗺️ Visual Gomi Board (Standardized Segregation)")
    g_col1, g_col2, g_col3, g_col4 = st.columns(4)
    
    with g_col1:
        st.markdown(f"""
        <div class="gomi-card-premium" style="background: linear-gradient(135deg, #fff5f5 0%, #fff 100%); border-top: 8px solid #ef4444;">
            <div class="gomi-title" style="color: #ef4444;">🔴 MOERU</div>
            <div class="gomi-subtitle">Combustible / Bakar</div>
            <div class="gomi-list">
                • Sisa Makanan<br>
                • Kertas Kotor/Tisu<br>
                • Daun/Ranting Kecil<br>
                • Popok Bayi
            </div>
            <div class="gomi-icon-container" style="background: #fee2e2;">
                <img src="https://img.icons8.com/isometric/100/Organic-Food.png" width="60">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with g_col2:
        st.markdown(f"""
        <div class="gomi-card-premium" style="background: linear-gradient(135deg, #eef2ff 0%, #fff 100%); border-top: 8px solid #3b82f6;">
            <div class="gomi-title" style="color: #3b82f6;">🔵 SHIGEN</div>
            <div class="gomi-subtitle">Recyclable / Daur Ulang</div>
            <div class="gomi-list">
                • Koran & Kardus<br>
                • Kaleng Logam<br>
                • Botol Kaca Bersih<br>
                • Plastik Campuran
            </div>
            <div class="gomi-icon-container" style="background: #e0e7ff;">
                <img src="https://img.icons8.com/isometric/100/Plastic-Bottle.png" width="60">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with g_col3:
        st.markdown(f"""
        <div class="gomi-card-premium" style="background: linear-gradient(135deg, #ecfdf5 0%, #fff 100%); border-top: 8px solid #10b981;">
            <div class="gomi-title" style="color: #10b981;">🟢 FILAMEN</div>
            <div class="gomi-subtitle">AgriSensa Gold Standard</div>
            <div class="gomi-list">
                • Botol PET Bening<br>
                • Tutup Botol HDPE<br>
                • Label Kemasan PP<br>
                • Gelas Plastik PET
            </div>
            <div class="gomi-icon-container" style="background: #d1fae5;">
                <img src="https://img.icons8.com/isometric/100/3D-Printer.png" width="60">
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with g_col4:
        st.markdown(f"""
        <div class="gomi-card-premium" style="background: linear-gradient(135deg, #f8fafc 0%, #fff 100%); border-top: 8px solid #64748b;">
            <div class="gomi-title" style="color: #64748b;">⚫ MOENAI</div>
            <div class="gomi-subtitle">Non-Combustible / B3</div>
            <div class="gomi-list">
                • Pecahan Kaca<br>
                • Baterai & Lampu<br>
                • Logam Tajam<br>
                • Limbah Kimia
            </div>
            <div class="gomi-icon-container" style="background: #f1f5f9;">
                <img src="https://img.icons8.com/isometric/100/Battery-Level.png" width="60">
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- SECTION 2: INTERACTIVE PERFECTION CHECKLIST ---
    st.subheader("✅ Japanese Perfection Checklist (Standard SOP)")
    st.write("Lakukan 3 langkah ini sebelum menaruh sampah di wadah koleksi:")
    
    chk_c1, chk_c2, chk_c3 = st.columns(3)
    with chk_c1:
        st.checkbox("🚿 **WASH & CLEAN**: Sudah dibilas dari sisa makanan/cairan?")
    with chk_c2:
        st.checkbox("🏷️ **DETACH**: Label dan Tutup sudah dipisahkan?")
    with chk_c3:
        st.checkbox("📉 **COMPRESS**: Kardus/Botol sudah digepengkan?")
    
    st.divider()

    # --- SECTION 3: CALENDAR & FLOW ---
    c_col1, c_col2 = st.columns([1, 1])
    
    with c_col1:
        st.subheader("📅 Jadwal Pengumpulan Kolektif")
        schedule = {
            "Hari": ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"],
            "Kategori": ["🔴 Organik", "🔵 Plastik (Filamen)", "🔴 Organik", "📦 Kertas/Kardus", "🔴 Organik", "⚠️ Spesial/B3"],
            "Tujuan": ["Unit Kompos", "Unit Shredding", "Unit Kompos", "Bank Sampah", "Unit Kompos", "Karantina B3"]
        }
        st.table(pd.DataFrame(schedule))
        
    with c_col2:
        st.subheader("🔗 Supply Chain Impact")
        st.write("Efisiensi pemilahan Anda berdampak langsung pada kualitas produk:")
        
        # Funnel Chart Simulation
        fig_funnel = go.Figure(go.Funnel(
            y=["Total Sampah Input", "Sampah Terpilah Disiplin", "Bahan Baku Berkualitas", "Produk Jadi (Pupuk/Filamen)"],
            x=[100, 85, 70, 60],
            marker = {"color": ["#d1d5db", "#94a3b8", "#3b82f6", "#10b981"]}
        ))
        fig_funnel.update_layout(height=300, margin=dict(t=20, b=20, l=100))
        st.plotly_chart(fig_funnel, use_container_width=True)
        st.caption("⚠️ **Catatan AI:** Pemilahan yang buruk (kontaminasi) menurunkan yield produksi sebesar 30-40%.")

# --- TAB 2: TRANSFORMASI ORGANIK ---
with tabs[2]:
    st.header("🍃 Transformasi Limbah ke Pupuk Organik Premium")
    st.write("Sistem pengolahan terkontrol untuk menghasilkan nutrisi berkualitas tinggi yang setara dengan pupuk industri.")
    
    col_t1, col_t2 = st.columns([1, 1])
    
    with col_t1:
        st.markdown('<div class="transformation-card">', unsafe_allow_html=True)
        st.subheader("🔬 4 Fase Dekomposisi Saintifik")
        st.markdown("""
        1. **Fase Mesofilik (Hari 1-3):** Pertumbuhan mikroba awal, suhu naik ke 40°C. pH mulai turun.
        2. **Fase Termofilik (Hari 4-15):** Suhu 55-70°C. Mematikan patogen & biji gulma. Degradasi selulosa.
        3. **Fase Pendinginan (Hari 16-25):** Aktivitas mikroba menurun, suhu kembali ke 40°C, muncul fungi dekomposer.
        4. **Fase Pematangan (Hari >30):** Stabilisasi C/N ratio (Target <20). Pembentukan asam humat & fulvat.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_t2:
        st.subheader("🧪 Quality Control (QC) Parameter")
        st.write("Pantau indikator fisik untuk menjamin kualitas output.")
        q1, q2 = st.columns(2)
        q1.metric("Target Kelembaban", "50-60%", "Kunci Aerob")
        q2.metric("Target pH Akhir", "6.5 - 7.5", "Netral")
        
        st.markdown("""
        - **Aroma:** Harus berbau tanah segar (bukan amonia/busuk).
        - **Warna:** Cokelat kegelapan hingga hitam (seperti tanah).
        - **Tekstur:** Remah, tidak menggumpal saat digenggam.
        """)

    st.divider()
    
    col_t3, col_t4 = st.columns([1, 1])
    
    with col_t3:
        st.subheader("🧫 Manajemen Biologi & Agen Hayati")
        st.write("Integrasi Bioaktivator dari **Laboratorium Pupuk Organik** untuk akselerasi dekomposisi.")
        st.table(pd.DataFrame({
            "Agen Hayati": ["🌱 ROTAN (Ramuan Organik)", "🍄 Trichoderma sp.", "🧪 Molase / Gula Baru", "🧪 Asam Humat"],
            "Fungsi Utama": ["Probiotik Sempurna (Selulolitik & Penambat N)", "Antifungi (Perlindungan Akar)", "Sumber Energi Mikroba (Karbon)", "Pembenah Tanah & Khelasi Nutrisi"],
            "Dosis": ["10-20ml / Liter air", "50gr / m3 sampah", "100ml / 10L air", "2gr / Liter kocor"]
        }))

    with col_t4:
        st.subheader("📊 Simulasi Output & Aplikasi Nursery")
        waste_input_t = st.number_input("Input Sampah Organik (kg/hari)", 10, 1000, 100, key="t_waste")
        
        # Calculation Logic
        reduction_rate = 0.4 # 40% yield
        fert_output = waste_input_t * reduction_rate
        
        st.metric("Estimasi Pupuk Matang", f"{fert_output:.1f} kg/hari")
        
        with st.expander("📝 Rekomendasi Dosis Aplikasi Nursery", expanded=True):
            st.markdown(f"""
            - **Media Semai:** Campur 1 bagian pupuk : 3 bagian tanah (Top Soil).
            - **Polybag (Bibit):** 50-100gr per pohon, frekuensi 2 minggu sekali.
            - **Pupuk Cair (POC):** Fermentasi 1kg hasil olahan + 10L air (Dosis 1:10 kocor).
            """)
            st.success(f"Output cukup untuk menyuplai nutrisi **{(fert_output/0.1):.0f} polybag bibit** rutin.")

    st.divider()
    st.subheader("📊 Analisis Kandungan Hara (NPK Lab Simulation)")
    st.write("Hasil simulasi uji laboratorium berdasarkan standarisasi **SNI 19-7030-2004** untuk kompos berkualitas.")
    
    # Advanced Nutrient Data
    nutrient_db = {
        "Grup": ["Primer", "Primer", "Primer", "Sekunder", "Sekunder", "Sekunder", "Mikro", "Mikro", "Mikro", "Lainnya"],
        "Parameter": ["Nitrogen (N)", "Phosphate (P)", "Kalium (K)", "Kalsium (Ca)", "Magnesium (Mg)", "Sulfur (S)", "Besi (Fe)", "Mangan (Mn)", "Seng (Zn)", "C/N Ratio"],
        "Hasil (%)": [2.65, 1.95, 2.30, 1.10, 0.45, 0.35, 0.05, 0.02, 0.015, 12.5],
        "SNI Min (%)": [2.00, 1.50, 1.50, 0.80, 0.30, 0.25, 0.03, 0.01, 0.010, 20.0],
        "Fungsi Saintifik": [
            "Pembentukan Klorofil & Vegetatif", 
            "Perkembangan Akar & Pembungaan", 
            "Transportasi Nutrisi & Imun",
            "Dinding Sel & Aktivasi Enzim",
            "Inti Klorofil (Fotosintesis)",
            "Sintesis Protein & Aroma",
            "Transfer Elektron dalam Sel",
            "Aktivator Metabolisme Nitrogen",
            "Sintesis Hormon Auksin (Tumbuh)",
            "Indikator Kematangan Kompos"
        ]
    }
    df_lab = pd.DataFrame(nutrient_db)
    
    l_col1, l_col2 = st.columns([2, 1])
    
    with l_col1:
        fig_lab = go.Figure()
        
        # Filter for charting percent assets only (not C/N Ratio)
        df_chart = df_lab[df_lab["Parameter"] != "C/N Ratio"]
        
        fig_lab.add_trace(go.Bar(
            x=df_chart["Parameter"], 
            y=df_chart["Hasil (%)"], 
            name="AgriSensa Eco Lab", 
            marker_color="#10b981",
            text=df_chart["Hasil (%)"],
            textposition='auto'
        ))
        
        fig_lab.add_trace(go.Bar(
            x=df_chart["Parameter"], 
            y=df_chart["SNI Min (%)"], 
            name="SNI Standard", 
            marker_color="#d1d5db"
        ))
        
        fig_lab.update_layout(
            barmode='group', 
            height=400, 
            margin=dict(t=20, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_lab, use_container_width=True)
        
    with l_col2:
        st.markdown("**🔬 Kesimpulan Lab**")
        cn_val = df_lab[df_lab["Parameter"] == "C/N Ratio"]["Hasil (%)"].values[0]
        if cn_val < 20:
            st.success(f"**C/N Ratio: {cn_val}**\n\nKompos sudah **MATANG SEMPURNA** dan aman untuk media tanam nursery.")
        else:
            st.warning(f"**C/N Ratio: {cn_val}**\n\nKompos masih perlu maturasi tambahan.")
            
        st.markdown("""
        > [!NOTE]
        > Kandungan **Nitrogen (2.65%)** di atas standar SNI menandakan bahan baku sisa dapur Anda kaya akan protein, sangat baik untuk fase vegetatif sayuran.
        """)

    st.markdown("**📄 Tabel Rincian Unsur Hara Lengkap**")
    st.table(df_lab)
    
    # ========================================================
    # 🔥 ADVANCED FERMENTATION MONITOR (NEW FEATURE)
    # ========================================================
    st.divider()
    st.markdown("---")
    st.header("🔥 Real-Time Fermentation Command Center")
    st.write("Monitor parameter kritis proses pengomposan secara real-time untuk menghasilkan pupuk grade premium.")
    
    # Sub-tabs for advanced features
    ferm_tabs = st.tabs([
        "🌡️ Live Monitor", 
        "📊 KPI Scorecard", 
        "📈 Production Analytics",
        "🏆 Quality Grading"
    ])
    
    # --- SUB-TAB 1: LIVE FERMENTATION MONITOR ---
    with ferm_tabs[0]:
        st.subheader("🌡️ Real-Time Process Parameters")
        
        # Initialize simulation day in session state if not exists
        if 'ferm_sim_day' not in st.session_state:
            st.session_state.ferm_sim_day = 10
        
        # Simulation controls
        sim_col1, sim_col2 = st.columns([3, 1])
        with sim_col2:
            sim_day = st.slider("📅 Simulasi Hari ke-", 1, 45, st.session_state.ferm_sim_day, key="ferm_day_slider")
            st.session_state.ferm_sim_day = sim_day
        
        # Dynamic values based on day (realistic fermentation curve)
        if sim_day <= 3:
            phase = "🟢 Mesofilik"
            temp = 28 + (sim_day * 4)
            ph = 6.5 - (sim_day * 0.15)
            moisture = 65 - (sim_day * 2)
            phase_color = "#22c55e"
        elif sim_day <= 15:
            phase = "🔴 Termofilik"
            temp = 55 + min(15, (sim_day - 3) * 1.5)
            ph = 6.0 + ((sim_day - 3) * 0.05)
            moisture = 55 - ((sim_day - 3) * 0.5)
            phase_color = "#ef4444"
        elif sim_day <= 25:
            phase = "🟡 Pendinginan"
            temp = 70 - ((sim_day - 15) * 3)
            ph = 6.6 + ((sim_day - 15) * 0.04)
            moisture = 50 + ((sim_day - 15) * 0.3)
            phase_color = "#f59e0b"
        else:
            phase = "✅ Pematangan"
            temp = 35 - min(10, (sim_day - 25) * 0.5)
            ph = 7.0 + min(0.3, (sim_day - 25) * 0.02)
            moisture = 52 + min(8, (sim_day - 25) * 0.3)
            phase_color = "#10b981"
        
        # C/N Ratio degradation simulation
        cn_ratio = 35 - (sim_day * 0.5)
        cn_ratio = max(12, cn_ratio)
        
        with sim_col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {phase_color}22 0%, white 100%); 
                        padding: 15px; border-radius: 10px; border-left: 5px solid {phase_color};
                        margin-bottom: 15px;">
                <h3 style="margin:0; color: {phase_color};">Fase Saat Ini: {phase}</h3>
                <p style="margin:5px 0 0 0; color: #6b7280;">Hari ke-{sim_day} dari proses pengomposan</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Gauge Charts Row
        g1, g2, g3, g4 = st.columns(4)
        
        # Temperature Gauge
        with g1:
            fig_temp = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=temp,
                title={'text': "🌡️ Suhu (°C)"},
                delta={'reference': 55, 'increasing': {'color': "red"}},
                gauge={
                    'axis': {'range': [20, 80]},
                    'bar': {'color': "#ef4444"},
                    'steps': [
                        {'range': [20, 40], 'color': "#d1fae5"},
                        {'range': [40, 55], 'color': "#fef3c7"},
                        {'range': [55, 70], 'color': "#fee2e2"},
                        {'range': [70, 80], 'color': "#fca5a5"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75, 'value': 70
                    }
                }
            ))
            fig_temp.update_layout(height=200, margin=dict(t=50, b=10, l=20, r=20))
            st.plotly_chart(fig_temp, use_container_width=True)
        
        # pH Gauge
        with g2:
            fig_ph = go.Figure(go.Indicator(
                mode="gauge+number",
                value=ph,
                title={'text': "⚗️ pH Level"},
                gauge={
                    'axis': {'range': [4, 9]},
                    'bar': {'color': "#3b82f6"},
                    'steps': [
                        {'range': [4, 5.5], 'color': "#fca5a5"},
                        {'range': [5.5, 6.5], 'color': "#fef3c7"},
                        {'range': [6.5, 7.5], 'color': "#d1fae5"},
                        {'range': [7.5, 8.5], 'color': "#fef3c7"},
                        {'range': [8.5, 9], 'color': "#fca5a5"}
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75, 'value': 7.0
                    }
                }
            ))
            fig_ph.update_layout(height=200, margin=dict(t=50, b=10, l=20, r=20))
            st.plotly_chart(fig_ph, use_container_width=True)
        
        # Moisture Gauge
        with g3:
            fig_moist = go.Figure(go.Indicator(
                mode="gauge+number",
                value=moisture,
                title={'text': "💧 Kelembaban (%)"},
                gauge={
                    'axis': {'range': [30, 80]},
                    'bar': {'color': "#06b6d4"},
                    'steps': [
                        {'range': [30, 45], 'color': "#fef3c7"},
                        {'range': [45, 60], 'color': "#d1fae5"},
                        {'range': [60, 80], 'color': "#fef3c7"}
                    ],
                    'threshold': {
                        'line': {'color': "blue", 'width': 4},
                        'thickness': 0.75, 'value': 55
                    }
                }
            ))
            fig_moist.update_layout(height=200, margin=dict(t=50, b=10, l=20, r=20))
            st.plotly_chart(fig_moist, use_container_width=True)
        
        # C/N Ratio Gauge
        with g4:
            fig_cn = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=cn_ratio,
                title={'text': "⚖️ C/N Ratio"},
                delta={'reference': 20, 'decreasing': {'color': "green"}},
                gauge={
                    'axis': {'range': [5, 40]},
                    'bar': {'color': "#8b5cf6"},
                    'steps': [
                        {'range': [5, 15], 'color': "#d1fae5"},
                        {'range': [15, 20], 'color': "#d1fae5"},
                        {'range': [20, 30], 'color': "#fef3c7"},
                        {'range': [30, 40], 'color': "#fee2e2"}
                    ],
                    'threshold': {
                        'line': {'color': "green", 'width': 4},
                        'thickness': 0.75, 'value': 20
                    }
                }
            ))
            fig_cn.update_layout(height=200, margin=dict(t=50, b=10, l=20, r=20))
            st.plotly_chart(fig_cn, use_container_width=True)
        
        # Trend Chart (30 Days)
        st.subheader("📈 Trend Parameter 30 Hari")
        days = list(range(1, 46))
        temp_trend = []
        ph_trend = []
        cn_trend = []
        
        for d in days:
            if d <= 3:
                temp_trend.append(28 + (d * 4))
                ph_trend.append(6.5 - (d * 0.15))
                cn_trend.append(35 - (d * 0.5))
            elif d <= 15:
                temp_trend.append(55 + min(15, (d - 3) * 1.5))
                ph_trend.append(6.0 + ((d - 3) * 0.05))
                cn_trend.append(35 - 1.5 - ((d - 3) * 0.8))
            elif d <= 25:
                temp_trend.append(70 - ((d - 15) * 3))
                ph_trend.append(6.6 + ((d - 15) * 0.04))
                cn_trend.append(25 - ((d - 15) * 0.6))
            else:
                temp_trend.append(35 - min(10, (d - 25) * 0.5))
                ph_trend.append(7.0 + min(0.3, (d - 25) * 0.02))
                cn_trend.append(max(12, 19 - ((d - 25) * 0.3)))
        
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(x=days, y=temp_trend, name="Suhu (°C)", line=dict(color="#ef4444", width=2)))
        fig_trend.add_trace(go.Scatter(x=days, y=[t*10 for t in ph_trend], name="pH (x10)", line=dict(color="#3b82f6", width=2)))
        fig_trend.add_trace(go.Scatter(x=days, y=cn_trend, name="C/N Ratio", line=dict(color="#8b5cf6", width=2)))
        
        # Add phase regions
        fig_trend.add_vrect(x0=1, x1=3, fillcolor="#22c55e", opacity=0.1, line_width=0)
        fig_trend.add_vrect(x0=3, x1=15, fillcolor="#ef4444", opacity=0.1, line_width=0)
        fig_trend.add_vrect(x0=15, x1=25, fillcolor="#f59e0b", opacity=0.1, line_width=0)
        fig_trend.add_vrect(x0=25, x1=45, fillcolor="#10b981", opacity=0.1, line_width=0)
        
        # Mark current day
        fig_trend.add_vline(x=sim_day, line=dict(color="black", dash="dash", width=2))
        fig_trend.add_annotation(x=sim_day, y=80, text=f"Hari ke-{sim_day}", showarrow=True, arrowhead=2)
        
        fig_trend.update_layout(
            height=350,
            margin=dict(t=20, b=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            xaxis_title="Hari",
            yaxis_title="Nilai Parameter"
        )
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Alert System
        alert_col1, alert_col2 = st.columns(2)
        with alert_col1:
            if temp > 70:
                st.error("🚨 **ALERT:** Suhu terlalu tinggi! Buka ventilasi atau siram dengan air.")
            elif temp < 35 and sim_day < 25:
                st.warning("⚠️ **WARNING:** Suhu rendah. Tambah bahan hijau (nitrogen) untuk meningkatkan aktivitas mikroba.")
            else:
                st.success("✅ Suhu dalam rentang optimal")
        
        with alert_col2:
            if cn_ratio < 15:
                st.success(f"✅ **C/N Ratio: {cn_ratio:.1f}** - Kompos MATANG SEMPURNA!")
            elif cn_ratio < 20:
                st.info(f"ℹ️ **C/N Ratio: {cn_ratio:.1f}** - Hampir matang, tunggu beberapa hari lagi.")
            else:
                st.warning(f"⚠️ **C/N Ratio: {cn_ratio:.1f}** - Belum matang, lanjutkan proses dekomposisi.")
    
    # --- SUB-TAB 2: KPI SCORECARD ---
    with ferm_tabs[1]:
        st.subheader("🎯 Balanced Scorecard - Pupuk Organik Premium")
        st.write("Key Performance Indicators untuk menjamin kualitas setara industri.")
        
        # Financial KPIs
        st.markdown("### 💰 Financial Perspective")
        
        # Calculate financial metrics
        revenue_actual = organic_processed * price_organic
        revenue_target = s_target_ferti  # From sidebar
        cost_per_kg = (total_opex_base / 30) / max(1, daily_ferti)
        margin_per_kg = price_organic - cost_per_kg
        roi_actual = ((revenue_actual - total_opex_base) / max(1, total_capex)) * 100
        roi_target = ((revenue_target - total_opex_base) / max(1, total_capex)) * 100
        achievement = (revenue_actual / max(1, revenue_target)) * 100
        
        # Row 1: Target vs Actual Revenue
        st.markdown("**📊 Revenue Comparison**")
        rev_col1, rev_col2, rev_col3 = st.columns(3)
        rev_col1.metric("📈 Revenue TARGET", f"Rp {revenue_target/1e6:.1f}M", "Dari Sidebar")
        rev_col2.metric("📉 Revenue AKTUAL", f"Rp {revenue_actual/1e6:.1f}M", f"{achievement:.0f}% tercapai")
        rev_col3.metric("🎯 Achievement", f"{achievement:.1f}%", "Target vs Aktual")
        
        st.markdown("---")
        
        # Row 2: Other financial metrics  
        fin_col1, fin_col2, fin_col3, fin_col4 = st.columns(4)
        fin_col1.metric("Biaya/kg", f"Rp {cost_per_kg:,.0f}", "-15%" if cost_per_kg < 2000 else None)
        fin_col2.metric("Margin/kg", f"Rp {margin_per_kg:,.0f}", "Profit")
        fin_col3.metric("ROI Target", f"{roi_target:.1f}%", "Proyeksi")
        fin_col4.metric("ROI Aktual", f"{roi_actual:.1f}%", "Investasi")
        
        # Process KPIs
        st.markdown("### ⚙️ Process Perspective")
        proc_col1, proc_col2, proc_col3, proc_col4 = st.columns(4)
        
        cycle_time = 30  # days
        throughput = daily_ferti
        yield_rate = s_yield_organic * 100
        capacity_util = (throughput / max(1, 100)) * 100
        
        proc_col1.metric("Cycle Time", f"{cycle_time} hari", "Standar")
        proc_col2.metric("Throughput", f"{throughput:.0f} kg/hari", "Output")
        proc_col3.metric("Rendemen", f"{yield_rate:.0f}%", "Efisiensi")
        proc_col4.metric("Utilitas Kapasitas", f"{min(100, capacity_util):.0f}%", "Mesin")
        
        # Quality KPIs
        st.markdown("### 🔬 Quality Perspective")
        qual_col1, qual_col2, qual_col3, qual_col4 = st.columns(4)
        
        npk_score = 95  # Simulated
        cn_target_met = "✅ Ya" if cn_ratio < 20 else "❌ Belum"
        sni_compliance = 100 if cn_ratio < 20 else 75
        defect_rate = 2.5
        
        qual_col1.metric("NPK Score", f"{npk_score}%", "vs Target")
        qual_col2.metric("C/N Target", cn_target_met, "<20")
        qual_col3.metric("SNI Compliance", f"{sni_compliance}%", "19-7030")
        qual_col4.metric("Defect Rate", f"{defect_rate}%", "-0.5%")
        
        # Environmental KPIs
        st.markdown("### 🌍 Environmental Perspective")
        env_col1, env_col2, env_col3, env_col4 = st.columns(4)
        
        env_col1.metric("Carbon Offset", f"{carbon_offset:,.0f} kg", "CO2e")
        env_col2.metric("Methane Avoided", f"{methane_avoided:,.0f} kg", "CH4")
        env_col3.metric("Landfill Saved", f"{landfill_m3_saved:.1f} m³", "Volume")
        env_col4.metric("Tree Equivalent", f"{tree_equivalent:.0f} pohon", "Tahunan")
        
        # Radar Chart Summary
        st.markdown("### 📊 Overall Performance Radar")
        perf_values = [
            min(100, roi_actual),
            min(100, yield_rate),
            npk_score,
            min(100, capacity_util),
            sni_compliance
        ]
        perf_labels = ["ROI", "Rendemen", "NPK Score", "Kapasitas", "SNI"]
        
        fig_perf = go.Figure()
        fig_perf.add_trace(go.Scatterpolar(
            r=perf_values,
            theta=perf_labels,
            fill='toself',
            name='Current Performance',
            line_color="#10b981"
        ))
        fig_perf.add_trace(go.Scatterpolar(
            r=[80, 80, 90, 85, 100],
            theta=perf_labels,
            fill='toself',
            name='Target',
            line_color="#3b82f6",
            opacity=0.5
        ))
        fig_perf.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=True,
            height=400,
            margin=dict(t=40, b=40)
        )
        st.plotly_chart(fig_perf, use_container_width=True)
    
    # --- SUB-TAB 3: PRODUCTION ANALYTICS ---
    with ferm_tabs[2]:
        st.subheader("📈 Production Analytics & Flow")
        
        # Get input from session state (set by Simulasi Output section)
        sankey_input = st.session_state.get('t_waste', 100)
        
        # Calculate flow values based on input (realistic composting losses)
        flow_pre = int(sankey_input * 0.95)      # 5% loss in pre-processing
        flow_ferm = int(sankey_input * 0.90)     # 10% total loss after fermentation
        flow_mat = int(sankey_input * 0.80)      # 20% total loss after maturation
        flow_grade_a = int(flow_mat * 0.50)      # 50% of mature = Grade A
        flow_grade_b = int(flow_mat * 0.30)      # 30% of mature = Grade B
        flow_grade_c = int(flow_mat * 0.12)      # 12% of mature = Grade C
        flow_reject = int(flow_mat * 0.08)       # 8% reject/recycle
        
        # Sankey Diagram
        st.markdown("### 🔄 Material Flow Diagram (Sankey)")
        st.caption(f"Visualisasi alur transformasi **{sankey_input} kg** sampah organik menjadi pupuk premium.")
        
        fig_sankey = go.Figure(data=[go.Sankey(
            arrangement='snap',
            node=dict(
                pad=30,
                thickness=25,
                line=dict(color="white", width=2),
                label=[
                    f"🗑️ Sampah Input ({sankey_input}kg)", 
                    f"⚙️ Pre-Processing ({flow_pre}kg)", 
                    f"🔥 Fermentasi ({flow_ferm}kg)",
                    f"✅ Pematangan ({flow_mat}kg)",
                    f"🥇 Grade A ({flow_grade_a}kg)",
                    f"🥈 Grade B ({flow_grade_b}kg)", 
                    f"🥉 Grade C ({flow_grade_c}kg)",
                    f"♻️ Reject ({flow_reject}kg)"
                ],
                color=[
                    "#475569",  # Input - slate
                    "#64748b",  # Pre-processing - gray
                    "#f97316",  # Fermentasi - orange
                    "#22c55e",  # Pematangan - green
                    "#eab308",  # Grade A - gold
                    "#3b82f6",  # Grade B - blue
                    "#a855f7",  # Grade C - purple
                    "#ef4444"   # Reject - red
                ],
                customdata=[sankey_input, flow_pre, flow_ferm, flow_mat, flow_grade_a, flow_grade_b, flow_grade_c, flow_reject],
                hovertemplate='<b>%{label}</b><br>Berat: %{customdata}kg<extra></extra>'
            ),
            link=dict(
                source=[0, 1, 2, 3, 3, 3, 3],
                target=[1, 2, 3, 4, 5, 6, 7],
                value=[sankey_input, flow_pre, flow_ferm, flow_grade_a, flow_grade_b, flow_grade_c, flow_reject],
                color=[
                    "rgba(71, 85, 105, 0.4)",   # Input → Pre
                    "rgba(100, 116, 139, 0.4)", # Pre → Ferm
                    "rgba(249, 115, 22, 0.4)",  # Ferm → Mat
                    "rgba(234, 179, 8, 0.5)",   # Mat → A
                    "rgba(59, 130, 246, 0.4)",  # Mat → B
                    "rgba(168, 85, 247, 0.4)",  # Mat → C
                    "rgba(239, 68, 68, 0.4)"    # Mat → Reject
                ],
                hovertemplate='%{source.label} → %{target.label}<br>Transfer: %{value}kg<extra></extra>'
            )
        )])
        
        fig_sankey.update_layout(
            font=dict(size=14, family="Arial, sans-serif", color="#000000"),
            height=500,
            margin=dict(t=30, b=30, l=30, r=30),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_sankey, use_container_width=True)
        
        # Summary metrics below sankey (dynamic)
        rendemen_pct = int((flow_mat / sankey_input) * 100)
        grade_a_pct = int((flow_grade_a / sankey_input) * 100)
        grade_b_pct = int((flow_grade_b / sankey_input) * 100)
        
        san_col1, san_col2, san_col3, san_col4 = st.columns(4)
        san_col1.metric("⬇️ Input", f"{sankey_input} kg", "Sampah Organik")
        san_col2.metric("🥇 Grade A", f"{flow_grade_a} kg", f"{grade_a_pct}% (Premium)")
        san_col3.metric("🥈 Grade B", f"{flow_grade_b} kg", f"{grade_b_pct}% (Standard)")
        san_col4.metric("♻️ Rendemen Total", f"{rendemen_pct}%", "Efisiensi")
        
        # Waterfall Chart - Cost Breakdown
        st.markdown("### 💵 Waterfall: Struktur Biaya Produksi")
        
        waterfall_data = {
            "Kategori": ["Input Bahan", "Pre-Processing", "Bioaktivator", "Tenaga Kerja", "Energi", "Packaging", "Overhead", "Total Biaya"],
            "Nilai": [200, 150, 100, 300, 120, 80, 50, None]
        }
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="Biaya",
            orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", "relative", "relative", "total"],
            x=waterfall_data["Kategori"],
            y=[200, 150, 100, 300, 120, 80, 50, 0],
            connector={"line": {"color": "#6b7280"}},
            increasing={"marker": {"color": "#ef4444"}},
            decreasing={"marker": {"color": "#22c55e"}},
            totals={"marker": {"color": "#3b82f6"}},
            text=["+Rp200", "+Rp150", "+Rp100", "+Rp300", "+Rp120", "+Rp80", "+Rp50", "Rp1.000/kg"]
        ))
        
        fig_waterfall.update_layout(
            title="Biaya per kg Pupuk Premium (Rp)",
            height=350,
            showlegend=False
        )
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
        # Heatmap - Correlation
        st.markdown("### 🔥 Heatmap: Korelasi Input-Output")
        
        import numpy as np
        corr_matrix = np.array([
            [1.0, 0.85, 0.72, 0.65],
            [0.85, 1.0, 0.78, 0.71],
            [0.72, 0.78, 1.0, 0.92],
            [0.65, 0.71, 0.92, 1.0]
        ])
        
        fig_heat = go.Figure(data=go.Heatmap(
            z=corr_matrix,
            x=["Input Organik", "Bioaktivator", "Suhu Optimal", "Output Grade A"],
            y=["Input Organik", "Bioaktivator", "Suhu Optimal", "Output Grade A"],
            colorscale="Greens",
            text=[[f"{v:.2f}" for v in row] for row in corr_matrix],
            texttemplate="%{text}",
            textfont={"size": 12}
        ))
        
        fig_heat.update_layout(
            title="Korelasi Faktor Produksi",
            height=350
        )
        st.plotly_chart(fig_heat, use_container_width=True)
    
    # --- SUB-TAB 4: QUALITY GRADING ---
    with ferm_tabs[3]:
        st.subheader("🏆 Sistem Grading Kualitas Pupuk")
        st.write("Standarisasi output berdasarkan parameter laboratorium untuk penetapan harga diferensial.")
        
        # Grade Cards
        grade_col1, grade_col2, grade_col3 = st.columns(3)
        
        with grade_col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%); 
                        padding: 20px; border-radius: 15px; border: 3px solid #f59e0b; text-align: center;">
                <h1 style="margin:0; font-size: 4rem;">🥇</h1>
                <h2 style="margin:10px 0; color: #b45309;">GRADE A - PREMIUM</h2>
                <p style="margin:5px 0;"><b>C/N Ratio:</b> < 15</p>
                <p style="margin:5px 0;"><b>NPK:</b> > 2.5% / 1.8% / 2.0%</p>
                <p style="margin:5px 0;"><b>pH:</b> 6.8 - 7.2</p>
                <hr style="border-color: #f59e0b;">
                <h3 style="color: #b45309;">Rp 5.000/kg</h3>
                <p style="font-size: 0.85rem; color: #78716c;">Untuk: Hidroponik, Nursery Premium, Ekspor</p>
            </div>
            """, unsafe_allow_html=True)
        
        with grade_col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #e0e7ff 0%, #eef2ff 100%); 
                        padding: 20px; border-radius: 15px; border: 3px solid #6366f1; text-align: center;">
                <h1 style="margin:0; font-size: 4rem;">🥈</h1>
                <h2 style="margin:10px 0; color: #4338ca;">GRADE B - STANDARD</h2>
                <p style="margin:5px 0;"><b>C/N Ratio:</b> 15 - 20</p>
                <p style="margin:5px 0;"><b>NPK:</b> > 2.0% / 1.5% / 1.5%</p>
                <p style="margin:5px 0;"><b>pH:</b> 6.5 - 7.5</p>
                <hr style="border-color: #6366f1;">
                <h3 style="color: #4338ca;">Rp 2.500/kg</h3>
                <p style="font-size: 0.85rem; color: #78716c;">Untuk: Kebun Sayur, Polybag, Campuran Media</p>
            </div>
            """, unsafe_allow_html=True)
        
        with grade_col3:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%); 
                        padding: 20px; border-radius: 15px; border: 3px solid #64748b; text-align: center;">
                <h1 style="margin:0; font-size: 4rem;">🥉</h1>
                <h2 style="margin:10px 0; color: #475569;">GRADE C - BULK</h2>
                <p style="margin:5px 0;"><b>C/N Ratio:</b> 20 - 25</p>
                <p style="margin:5px 0;"><b>NPK:</b> SNI Minimum</p>
                <p style="margin:5px 0;"><b>pH:</b> 6.0 - 8.0</p>
                <hr style="border-color: #64748b;">
                <h3 style="color: #475569;">Rp 1.200/kg</h3>
                <p style="font-size: 0.85rem; color: #78716c;">Untuk: Rehabilitasi Lahan, Mulsa, Reklamasi</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Grade Calculator
        st.markdown("### 🧮 Kalkulator Grading Otomatis")
        
        # Add explanation about grading basis
        with st.expander("📖 Dasar Penetapan Grade (SNI 19-7030-2004)", expanded=False):
            st.markdown("""
            **Sistem grading ini berdasarkan standar nasional Indonesia untuk pupuk organik:**
            
            | Parameter | Grade A (Premium) | Grade B (Standard) | Grade C (Bulk) |
            |-----------|-------------------|-------------------|----------------|
            | **C/N Ratio** | < 15 | 15 - 20 | 20 - 25 |
            | **Nitrogen (N)** | > 2.5% | ≥ 2.0% | SNI Min |
            | **Phosphate (P)** | > 1.8% | ≥ 1.5% | SNI Min |
            | **Kalium (K)** | > 2.0% | ≥ 1.5% | SNI Min |
            | **pH Level** | 6.8 - 7.2 | 6.5 - 7.5 | 6.0 - 8.0 |
            
            **Referensi:**
            - SNI 19-7030-2004: Spesifikasi Kompos dari Sampah Organik Domestik
            - Permentan No. 70/2011: Pupuk Organik, Pupuk Hayati, & Pembenah Tanah
            - Standar AgriSensa Eco Premium (Internal)
            
            > **Catatan:** C/N Ratio < 20 menandakan kompos sudah matang sempurna dan aman untuk tanaman.
            """)
        
        calc_col1, calc_col2 = st.columns([1, 1])
        
        with calc_col1:
            st.markdown("**📊 Masukkan Hasil Uji Laboratorium:**")
            input_cn = st.number_input("C/N Ratio", 5.0, 40.0, 14.5, 0.5, key="grade_cn_input")
            input_n = st.number_input("Nitrogen (N) %", 0.5, 5.0, 2.65, 0.05, key="grade_n_input")
            input_p = st.number_input("Phosphate (P) %", 0.5, 5.0, 1.95, 0.05, key="grade_p_input")
            input_k = st.number_input("Kalium (K) %", 0.5, 5.0, 2.30, 0.05, key="grade_k_input")
            input_ph = st.number_input("pH Level", 5.0, 9.0, 7.0, 0.1, key="grade_ph_input")
        
        with calc_col2:
            # Determine grade
            if input_cn < 15 and input_n > 2.5 and input_p > 1.8 and input_k > 2.0 and 6.8 <= input_ph <= 7.2:
                grade = "A"
                grade_color = "#f59e0b"
                price = 5000
                cert = "🏆 PREMIUM CERTIFIED"
            elif input_cn <= 20 and input_n >= 2.0 and input_p >= 1.5 and input_k >= 1.5 and 6.5 <= input_ph <= 7.5:
                grade = "B"
                grade_color = "#6366f1"
                price = 2500
                cert = "✅ SNI COMPLIANT"
            else:
                grade = "C"
                grade_color = "#64748b"
                price = 1200
                cert = "📋 BULK GRADE"
            
            st.markdown(f"""
            <div style="background: white; padding: 30px; border-radius: 15px; 
                        border: 4px solid {grade_color}; text-align: center; margin-top: 20px;">
                <h1 style="margin:0; font-size: 5rem; color: {grade_color};">GRADE {grade}</h1>
                <h3 style="margin:10px 0;">{cert}</h3>
                <hr>
                <h2 style="color: {grade_color};">Harga Jual: Rp {price:,}/kg</h2>
                <p style="color: #6b7280;">Berdasarkan parameter laboratorium yang Anda masukkan</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Digital Certificate Preview
            if grade == "A":
                st.success("🎖️ Produk ini berhak mendapat **Sertifikat Digital AgriSensa Premium** yang dapat di-scan konsumen!")
                
                # Generate QR Code for Premium Certificate
                st.divider()
                st.markdown("### 📱 Generate Sertifikat QR Code")
                
                cert_col1, cert_col2 = st.columns([1, 1])
                
                with cert_col1:
                    cert_product = st.text_input("Nama Produk Pupuk", "Pupuk Organik Premium AgriSensa", key="cert_prod")
                    cert_batch = st.text_input("Batch ID", f"FERT-{datetime.now().strftime('%Y%m%d')}-001", key="cert_batch")
                    cert_producer = st.text_input("Nama Produsen", "AgriSensa Eco System", key="cert_producer")
                    
                    # Store lab values in session for QR generation
                    if st.button("🔗 Generate QR Sertifikat", type="primary", use_container_width=True, key="gen_qr_btn"):
                        import urllib.parse
                        
                        # Build Vercel URL for certificate
                        base_url = "https://vercel-scan2.vercel.app/product"
                        params = {
                            'name': cert_product,
                            'variety': 'Grade A Premium',
                            'farmer': cert_producer,
                            'location': 'AgriSensa Lab Certified',
                            'harvest_date': datetime.now().strftime('%Y-%m-%d'),
                            'emoji': '🥇',
                            'cn_ratio': str(input_cn),
                            'ph_level': str(input_ph),
                            'nitrogen': str(input_n),
                            'phosphate': str(input_p),
                            'kalium': str(input_k),
                            'grade': 'A'
                        }
                        query_string = urllib.parse.urlencode(params)
                        cert_url = f"{base_url}/{cert_batch}?{query_string}"
                        
                        # Generate QR Code
                        qr = qrcode.QRCode(version=1, box_size=10, border=4)
                        qr.add_data(cert_url)
                        qr.make(fit=True)
                        qr_img = qr.make_image(fill_color="black", back_color="white")
                        
                        # Convert to bytes
                        buffer = io.BytesIO()
                        qr_img.save(buffer, format='PNG')
                        qr_bytes = buffer.getvalue()
                        
                        # Store in session state
                        st.session_state['cert_qr_bytes'] = qr_bytes
                        st.session_state['cert_qr_url'] = cert_url
                        st.session_state['cert_qr_batch'] = cert_batch
                
                with cert_col2:
                    # Display QR from session state (persistent)
                    if 'cert_qr_bytes' in st.session_state and st.session_state['cert_qr_bytes']:
                        st.image(st.session_state['cert_qr_bytes'], caption="Scan untuk verifikasi sertifikat", width=250)
                        
                        st.download_button(
                            "⬇️ Download QR Certificate",
                            st.session_state['cert_qr_bytes'],
                            f"Certificate_{st.session_state.get('cert_qr_batch', 'FERT')}.png",
                            "image/png",
                            use_container_width=True,
                            key="download_qr_btn"
                        )
                        
                        st.info(f"🔗 **URL:** `{st.session_state.get('cert_qr_url', '')[:60]}...`")
                        st.success("✅ QR Code siap! Scan dengan HP untuk melihat detail produk.")
                    else:
                        st.info("👈 Isi data di kiri, lalu klik **Generate QR Sertifikat**")


# --- TAB 3: UPCYCLING PLASTIK ---
with tabs[3]:
    st.header("🧵 Upcycling Plastik ke Filamen 3D (Pita 3D)")
    st.write("Sistem manufaktur presisi untuk mengubah limbah botol menjadi bahan baku teknologi.")
    
    col_p1, col_p2 = st.columns([1, 1])
    
    with col_p1:
        st.markdown('<div class="transformation-card" style="border-left-color: #3b82f6;">', unsafe_allow_html=True)
        st.subheader("� Database Karakteristik Material")
        st.write("Parameter teknis untuk pengaturan mesin ekstrusi (SOP Saintifik).")
        
        material_data = {
            "Tipe Plastik": ["PET (Botol Minum)", "HDPE (Tutup/Shampoo)", "LDPE (Kemasan Lentur)"],
            "Temp. Ekstrusi (°C)": ["240 - 260", "180 - 210", "160 - 190"],
            "Kekuatan Tarik": ["Sangat Tinggi", "Sedang", "Rendah-Lentur"],
            "Shrinkage (%)": ["0.2 - 0.5", "2.0 - 3.0", "1.5 - 2.0"]
        }
        st.table(pd.DataFrame(material_data))
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_p2:
        st.subheader("📐 Filament Yield Calculator (Proyeksi Output)")
        st.write("Estimasi hasil produksi berdasarkan jumlah sampah input.")
        
        calc_col1, calc_col2 = st.columns(2)
        with calc_col1:
            num_bottles = st.number_input("Jumlah Botol PET (600ml)", 1, 1000, 50)
            avg_weight = 0.025 # 25 grams per bottle
            total_input_gr = num_bottles * avg_weight * 1000
        
        with calc_col2:
            filament_dia = st.selectbox("Diameter Filamen (mm)", [1.75, 2.85])
            density_pet = 1.38 # g/cm3 standard PET
            
            # Volume = Mass / Density
            volume_cm3 = total_input_gr / density_pet
            # area = pi * r^2
            radius_cm = (filament_dia / 2) / 10 
            area_cm2 = 3.14159 * (radius_cm**2)
            
            length_cm = volume_cm3 / area_cm2
            length_meters = length_cm / 100
            
            # Spool estimation (1kg per spool)
            total_kg = total_input_gr / 1000
            num_spools = total_kg / 1.0 # 1kg spool
        
        # Displaying Results with Clearer Units
        res_y1, res_y2, res_y3 = st.columns(3)
        res_y1.metric("Total Berat", f"{total_kg:,.2f} Kg", "Material PET")
        res_y2.metric("Estimasi Panjang", f"{length_meters:,.1f} Meter", f"dia {filament_dia}mm")
        res_y3.metric("Output Produksi", f"{num_spools:,.1f} Roll", "Spool 1kg")
        
        st.caption(f"💡 **Catatan Teknis:** 1 Roll filamen PET 1.75mm standar memiliki panjang ±330 meter. Hasil {(total_kg*1000)/3.32:,.0f}m didasarkan pada densitas murni PET 1.38 g/cm³.")
        st.info(f"Produksi ini cukup untuk mencetak **{int(length_meters/15)} unit** label nursery standar.")

    st.divider()
    
    col_p3, col_p4 = st.columns([1, 1])
    
    with col_p3:
        st.subheader("📊 Quality Benchmarking (Upcycled vs Commercial)")
        st.write("Analisis perbandingan kekuatan dan stabilitas dimensi.")
        
        bench_data = {
            "Parameter": ["Kekuatan Tarik (MPa)", "Variasi Diameter (mm)", "Temperatur Cetak (°C)", "Tingkat Adhesi"],
            "Filamen AgriSensa": [55, 0.05, 250, "Sangat Baik"],
            "Commercial Grade": [62, 0.02, 245, "Sempurna"]
        }
        df_bench = pd.DataFrame(bench_data)
        
        fig_bench = go.Figure()
        fig_bench.add_trace(go.Scatterpolar(
            r=[55, 80, 95, 85], # Normalized scores
            theta=bench_data["Parameter"],
            fill='toself',
            name='AgriSensa Eco',
            line_color="#3b82f6"
        ))
        fig_bench.add_trace(go.Scatterpolar(
            r=[90, 95, 90, 100],
            theta=bench_data["Parameter"],
            fill='toself',
            name='Commercial',
            line_color="#94a3b8"
        ))
        fig_bench.update_layout(polar=dict(radialaxis=dict(visible=False, range=[0, 100])), showlegend=True, height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_bench, use_container_width=True)

    with col_p4:
        st.subheader("⚙️ Extrusion Process Control")
        st.write("Monitoring parameter kritis saat mesin beroperasi (Simulasi).")
        
        pc1, pc2 = st.columns(2)
        pc1.metric("Current Temp", "248.5 °C", "+1.2 °C")
        pc2.metric("Motor Speed", "15.0 RPM", "Stable")
        
        st.markdown("""
        **🔍 AI Analysis & Quality Log:**
        - **Status:** Filamen terdeteksi stabil pada 1.75mm.
        - **Kualitas Permukaan:** Glossy (Optimal).
        - **Rekomendasi:** Bersihkan nozzle setiap 50 jam operasional untuk menjaga kejernihan warna.
        """)
        
        if st.button("Generate Production Report (3D)"):
            st.toast("Menyiapkan dokumen teknis manufaktur...")
            st.success("Report siap diunduh di tab **Laporan Strategis** (Tab 7).")

    st.divider()
    st.subheader("📐 Penggunaan di Ekosistem AgriSensa")
    st.write("Hasil pita 3D digunakan untuk mencetak komponen operasional mandiri:")
    cols_app = st.columns(3)
    cols_app[0].image("https://img.icons8.com/isometric/100/3D-Printer.png", caption="Label Nursery")
    cols_app[1].image("https://img.icons8.com/isometric/100/Water-Pipe.png", caption="Konektor Irigasi")
    cols_app[2].image("https://img.icons8.com/isometric/100/Marker.png", caption="Patok Lahan")

# --- TAB 4: KOLABORASI & MATRIKS KEMITRAAN ---
with tabs[4]:
    st.header("🤝 Matriks Kolaborasi & Ekosistem Kemitraan")
    st.write("Membangun jaringan sirkular yang memberikan nilai tambah bagi seluruh stakeholder.")
    
    # --- SECTION 1: STAKEHOLDER STRATEGIC MAPPING ---
    st.subheader("🗺️ Stakeholder Strategic Mapping (Advanced)")
    m_data = {
        "Stakeholder": ["Sekolah/Kampus", "Perkantoran", "RT/RW Lingkungan", "UMKM Lokal", "Instansi Pemerintah"],
        "Peran Konkret": ["Suplier Organik Kantin & Edukasi", "Suplier Kertas & Plastik Premium", "Suplier Domestik Terpilah", "Pemanfaat Produk (Pupuk/Filamen)", "Regulator & Green Funding"],
        "KPI Utama": ["Tingkat Segregasi > 90%", "Volume PET > 50kg/bulan", "Zero Waste Compliance", "Efisiensi Biaya Produksi 30%", "Sertifikasi Carbon Offset"],
        "SLA Respon": ["4 Jam (Pickup)", "24 Jam (Pickup)", "Jadwal Mingguan", "On-Demand", "Laporan Bulanan"],
        "Insentif (Reward)": ["Sertifikat Green School", "Laporan ESG & Profit Sharing", "Poin Barter Bibit", "Diskon Bahan Baku 25%", "Data Dampak Kebijakan"]
    }
    st.table(pd.DataFrame(m_data))
    
    st.divider()
    
    # --- SECTION 2: PARTNERSHIP ONBOARDING WORKFLOW ---
    st.subheader("⚙️ Alur Kerja Sama (Onboarding Workflow)")
    w1, w2, w3, w4 = st.columns(4)
    
    with w1:
        st.markdown("""
        **1. Inisiasi & MOU**
        - Survey volume sampah.
        - Penandatanganan MOU.
        - Penetapan Target Bulanan.
        """)
    with w2:
        st.markdown("""
        **2. Edukasi & Infrastruktur**
        - Pelatihan pemilahan Jepang.
        - Penempatan Bin Segregasi.
        - Instalasi QR Log.
        """)
    with w3:
        st.markdown("""
        **3. Operasional & Logistik**
        - Penjadwalan angkutan.
        - QC sampah di lokasi.
        - Pencatatan di Aplikasi.
        """)
    with w4:
        st.markdown("""
        **4. Reporting & Reward**
        - Analisis dampak bulanan.
        - Pembagian insentif/poin.
        - Publikasi Green Branding.
        """)

    st.divider()

    # --- SECTION 3: INSTITUTIONAL INCENTIVE SYSTEM (TOKEN ECO) ---
    st.subheader("💎 Sistem Insentif & Token Ekonomi")
    st.write("Simulasi poin yang didapatkan instansi mitra berdasarkan kontribusi sampah.")
    
    col_ins1, col_ins2 = st.columns([1, 2])
    
    with col_ins1:
        st.markdown('<div class="transformation-card" style="border-left-color: #f59e0b;">', unsafe_allow_html=True)
        st.markdown("**💰 Kalkulator Poin Mitra**")
        p_org = st.number_input("Input Organik (kg)", 0, 1000, 100)
        p_pla = st.number_input("Input Plastik (kg)", 0, 1000, 50)
        
        # Poin calculation logic
        total_points = (p_org * 10) + (p_pla * 50)
        st.metric("Total AgriSensa Points", f"{total_points:,} Pts")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_ins2:
        st.markdown("**🎁 Katalog Barter Poin (Redemption)**")
        redem_data = {
            "Item Reward": ["Bibit Anggur Premum", "Pupuk Organik Matang (5kg)", "Komponen IRigasi 3D", "Modul Pelatihan Academy"],
            "Harga Poin": ["5.000 Pts", "1.500 Pts", "3.000 Pts", "10.000 Pts"],
            "Stok": ["Tersedia", "Melimpah", "Terbatas", "Akses Digital"]
        }
        st.dataframe(pd.DataFrame(redem_data), use_container_width=True)

    st.divider()
    
    # --- SECTION 4: IMPACT DASHBOARD FOR PARTNERS ---
    st.subheader("📈 Social & Environmental Impact Projection")
    st.write("Visualisasi dampak kolektif mitra dalam ekosistem AgriSensa.")
    
    imp_col1, imp_col2 = st.columns(2)
    
    with imp_col1:
        # Chart: Cumulative CO2 Offset by Stakeholder Type
        fig_impact = px.bar(
            x=["Sekolah", "Kantor", "RW 01", "RW 02", "Pasar"],
            y=[1200, 2500, 800, 1100, 4500],
            labels={'x':'Kategori Mitra', 'y':'CO2 Offset (kg)'},
            title="Kontribusi Carbon Offset per Kategori",
            color_discrete_sequence=["#059669"]
        )
        st.plotly_chart(fig_impact, use_container_width=True)
        
    with imp_col2:
        st.info("""
        **📢 Institutional Branding:**
        Partner yang mencapai target 'Platinum' (Offset > 5 Ton) berhak mendapatkan **Green Label Certification** dari AgriSensa yang dapat digunakan untuk laporan tahunan (ESG) atau publikasi media.
        """)
        st.progress(0.75, text="75% Kapasitas Kerja Sama Terpakai")

    # ROI Calculator (Kept and Integrated above earlier)
    # Note: ROI Calculator is already deep in previous turn.

    # ROI Calculator 

# --- TAB 5: BLUEPRINT TARGET AI (SIMULATOR) ---
with tabs[5]:
    st.header("🎯 AI Strategic Simulator (Dynamic Blueprint)")
    st.write("Target omzet dan beban operasional didasarkan pada parameter di Sidebar.")
    
    # --- DYNAMIC CALCULATIONS (NOW GLOBAL) ---

    st.divider()
    
    # --- RESULTS DASHBOARD (ADVANCED) ---
    st.subheader("🚀 High-Fidelity Operational Analysis")
    res_c1, res_c2, res_c3, res_c4 = st.columns(4)
    
    res_c1.metric("Total Raw Material", f"{total_raw_daily:,.0f} kg/day", "Input")
    res_c2.metric("Logistics Load", f"{partners_needed:,.0f} Partners", f"{shifts_needed} Pickups")
    res_c3.metric("Energy Load", f"{energy_kwh_daily:,.1f} kWh", "Daily Usage")
    res_c4.metric("Net Carbon Offset", f"{net_carbon_daily:,.1f} kg CO2e", "Pure Impact")
    
    st.markdown("---")
    
    # --- LABOR & SHIFT PLANNING ---
    st.subheader("👷 Penjadwalan Tenaga Kerja & Shift")
    sh_col1, sh_col2 = st.columns([2, 1])
    
    with sh_col1:
        st.write(f"Berdasarkan durasi mesin **{machine_hours_extrude:.1f} jam/hari**, dibutuhkan **{shifts_needed} Shift**.")
        shift_schedule = {
            "Shift": [f"Shift {i+1}" for i in range(shifts_needed)],
            "Waktu": ["08:00 - 16:00", "16:00 - 00:00", "00:00 - 08:00"][:shifts_needed],
            "Petugas": ["2 Operator + 1 Driver"] * shifts_needed,
            "Target Output": [f"{daily_filam/shifts_needed:.1f} kg Filamen"] * shifts_needed
        }
        st.table(pd.DataFrame(shift_schedule))
        
    with sh_col2:
        st.markdown('<div class="transformation-card" style="border-left-color: #ef4444;">', unsafe_allow_html=True)
        st.markdown("**🚨 Bottleneck Analysis**")
        if machine_hours_extrude > 16:
            st.error("MAINTENANCE RISK: Mesin bekerja >16 jam. Resiko downtime tinggi. Siapkan suku cadang cadangan.")
        if partners_needed > 25:
            st.warning("LOGISTICS RISK: Terlalu banyak titik jemput. Perlu rute zonasi yang kompleks.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    
    # --- SENSITIVITY ANALYSIS (PROFITABILITY) ---
    st.subheader("📈 Analisis Sensitivitas Keuntungan (AI Analysis)")
    st.write("Bagaimana perubahan efisiensi rendemen mempengaruhi Laba Bersih bulanan.")
    
    sensitivity_data = []
    for yield_var in [0.2, 0.3, 0.4, 0.5, 0.6]:
        temp_org_needed = daily_ferti / yield_var
        temp_rev = (req_ferti_month * price_organic) + (req_filam_month * price_filament)
        # Simplified opex for sensitivity
        status = "Optimal" if yield_var >= s_yield_organic else "Low Margin"
        sensitivity_data.append({
            "Rendemen (%)": f"{yield_var*100:.0f}%",
            "Target Sampah (kg/hr)": int(temp_org_needed + raw_pla_needed),
            "Status Efisiensi": status
        })
    st.table(pd.DataFrame(sensitivity_data))

    # --- VISUALIZATION (UNCHANGED BUT UPDATED DATA) ---
    col_v1, col_v2 = st.columns([2, 1])
    
    with col_v1:
        st.subheader("📈 Proyeksi Pertumbuhan Puncak Target")
        growth_index = [1, 2, 4, 8, 12] 
        months = ["Bulan 1", "Bulan 3", "Bulan 6", "Bulan 9", "Bulan 12"]
        
        fig_sim = go.Figure()
        fig_sim.add_trace(go.Bar(x=months, y=[(s_target_ferti + s_target_filam)*i/12 for i in growth_index], name="Total Omzet Proyeksi", marker_color="#10b981", opacity=0.7))
        fig_sim.add_trace(go.Scatter(x=months, y=[(s_target_ferti + s_target_filam)]*5, name="Target Puncak", line=dict(color="#ef4444", dash="dash")))
        fig_sim.update_layout(height=350, margin=dict(t=20))
        st.plotly_chart(fig_sim, use_container_width=True)
        
    with col_v2:
        st.subheader("🧩 Komposisi Pendapatan")
        fig_pie_sim = px.pie(
            names=["Pupuk Organic", "Filamen 3D"],
            values=[s_target_ferti, s_target_filam],
            color_discrete_sequence=["#10b981", "#3b82f6"],
            hole=0.4
        )
        fig_pie_sim.update_layout(height=350, margin=dict(t=20))
        st.plotly_chart(fig_pie_sim, use_container_width=True)

            
        st.success("🎯 **Goal Akhir:** Sistem mandiri (Self-Sustaining Eco-System) yang menghasilkan profit dari sampah.")

# --- TAB 6: ROADMAP ---
with tabs[6]:
    st.header("🗓️ Roadmap Implementasi (12 Minggu)")
    st.write("Langkah konkret transisi dari perencanaan ke operasional penuh.")
    
    r_col1, r_col2 = st.columns(2)
    
    with r_col1:
        with st.expander("🚀 Fase 1: Setup & Inisiasi (Minggu 1-4)", expanded=True):
            st.markdown("""
            - **W1:** Sosialisasi sistem pemilahan gaya Jepang ke calon mitra.
            - **W2:** Pengadaan bin sampah tersegregasi dan unit shredder plastik.
            - **W3:** Pelatihan SDM operasional (Teknik Composting & 3D Lab).
            - **W4:** Pilot project di 1 instansi (Sekolah/Kantor).
            """)
        
        with st.expander("⚙️ Fase 2: Optimasi Produksi (Minggu 5-8)"):
            st.markdown("""
            - **W5:** Uji lab pertama hasil pupuk organik (Parameter NPK).
            - **W6:** Kalibrasi mesin ekstrusi filamen untuk kualitas pita 3D.
            - **W7:** Peluncuran aplikasi log monitoring harian.
            - **W8:** Evaluasi sistem reward dan barter bibit.
            """)

    with r_col2:
        with st.expander("📈 Fase 3: Scale-up & Komersial (Minggu 9-12)"):
            st.markdown("""
            - **W9:** Ekspansi ke 5-10 instansi mitra baru.
            - **W10:** Integrasi penuh output pupuk ke unit Nursery AgriSensa.
            - **W11:** Penjualan perdana surplus filamen 3D ke komunitas maker.
            - **W12:** Audit dampak lingkungan (Carbon Offset Report).
            """)

# --- TAB 7: LAPORAN STRATEGIS ---
with tabs[7]:
    st.header("📁 Laporan Strategis Proyek (Waste-to-Value)")
    st.write("Dokumen komprehensif yang merangkum kelayakan teknis, finansial, dan dampak lingkungan.")
    
    # --- CROSS-MODULE DATA SYNC ---
    rab_remote = st.session_state.get('rab_state_df', None)
    ops_3k_remote = st.session_state.get('global_3k_sim', None)
    security_remote = st.session_state.get('ledger_db', None)
    
    st.markdown('<div class="jap-sorting-card" style="border-top-color: #10b981;">', unsafe_allow_html=True)
    st.subheader("📑 Executive Summary: AgriSensa Eco System")
    
    r_c1, r_c2 = st.columns(2)
    with r_c1:
        st.markdown(f"""
        **Sektor Ekonomi & ROI:**
        - **Proyeksi Omzet:** Rp {(s_target_ferti + s_target_filam):,.0f} / Bulan
        - **Total Investasi (CAPEX):** Rp {total_capex:,.0f}
        - **Beban Kerja (Operator):** {operators_needed} Orang
        - **Net Profit Target:** Rp {(s_target_ferti + s_target_filam - (operators_needed * o_labor_base + energy_cost_daily * 30 + o_maint)):,.0f} / Bulan
        """)
    
    with r_c2:
        st.markdown(f"""
        **Sektor Lingkungan & Sosial:**
        - **Net Carbon Offset:** {net_carbon_daily * 30:,.1f} kg CO2e / Bulan
        - **Mitra Strategis:** {partners_needed:,.0f} Instansi
        - **Status Keberlanjutan:** {trace_hash[:8].upper() if trace_hash else "GOLD"} Label
        """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.divider()
    
    # SECTOR SYNC DISPLAY
    s_col1, s_col2, s_col3 = st.columns(3)
    
    with s_col1:
        st.subheader("💰 Sektor Finansial")
        if rab_remote is not None:
            st.success("✅ Terintegrasi (Modul 28)")
            st.caption(f"Total Item: {len(rab_remote)} Baris")
            # Minimalist summary of external RAB
            st.markdown(f"**Total Modal:** Rp {rab_remote['Total (Rp)'].sum():,.0f}")
        else:
            st.warning("🔄 Template Standar (Modul 28)")
            st.markdown(f"**Est. Project CAPEX:** Rp {total_capex:,.0f}")
            st.caption("Kunjungi Modul 💰 28 untuk sinkronisasi RAB detail.")
            
    with s_col2:
        st.subheader("🚀 Sektor Operasional")
        if ops_3k_remote:
            st.success("✅ Terintegrasi (Modul 33)")
            st.markdown(f"**Komoditas:** {ops_3k_remote['komoditas']}")
            st.markdown(f"**Kapasitas:** {ops_3k_remote['kapasitas_mingguan']} kg/minggu")
        else:
            st.warning("🔄 Template Standar (Modul 33)")
            st.markdown(f"**Model:** Waste-to-Production Loop")
            st.markdown(f"**Ops Duration:** 24/7 Monitoring")
            st.caption("Kunjungi Modul 🏠 33 untuk sinkronisasi strategi 3K.")
            
    with s_col3:
        st.subheader("🛡️ Sektor Keamanan")
        if security_remote:
            st.success("✅ Terintegrasi (Modul 48)")
            st.markdown(f"**Blockchain Audit:** {len(security_remote)} Transaksi")
            st.markdown(f"**Last Sync:** {security_remote[-1]['timestamp']}")
        else:
            st.warning("🔄 Template Standar (Modul 48)")
            st.markdown("**Traceability ID:** Verified")
            st.markdown("**Security:** ISO/ESG Aligned")
            st.caption("Kunjungi Modul 🚚 48 untuk sinkronisasi Supply Chain.")

    st.divider()
    
    st.subheader("🛠️ Technical Dossier & Data Export")
    tab_exp1, tab_exp2 = st.tabs(["📊 Data Log Eksport", "🧪 Spesifikasi Produk"])
    
    with tab_exp1:
        st.write("Unduh row data aktivitas harian untuk audit internal.")
        csv_data = df_logs.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Waste Log (CSV)",
            data=csv_data,
            file_name=f"waste_log_agrisensa_{datetime.now().strftime('%Y%m%d')}.csv",
            mime='text/csv',
        )
        st.table(df_logs.tail(10))
        
    with tab_exp2:
        st.markdown(f"""
        - **Status Bioaktivator:** Menggunakan formula **ROTAN** (Modul 43).
        - **Standar Filamen:** 1.75mm (Variasi < 0.05mm).
        - **Standar Pupuk:** SNI 19-7030-2004 (Target C/N < 20).
        """)
        
    st.divider()
    
    # Final Action Button
    if st.button("⎙ Print Strategic Dossier (Full Data Sync)", type="primary"):
        st.components.v1.html("""
            <script>
                // Mempersiapkan layout cetak dengan memaksa window utama fokus
                window.parent.focus();
                
                // Menghilangkan overflow pada container utama untuk mencegah pemotongan halaman
                const root = window.parent.document.querySelector('.stApp');
                if(root) {
                    root.style.overflow = 'visible';
                    root.style.height = 'auto';
                }
                
                setTimeout(function() {
                    window.parent.print();
                }, 750);
            </script>
        """, height=0)
        st.toast("⚙️ Mengoptimalkan layout laporan (Sync Data)...")
        st.info("💡 **Solusi PDF:** Agar tidak kosong, pastikan Anda menggunakan **Google Chrome** atau **Edge**. Saat dialog print muncul, tunggu 2-3 detik hingga pratinjau muncul sempurna. Aktifkan **'Background Graphics'** agar warna kartu tercetak.")

    st.markdown("""
    > [!IMPORTANT]
    > **Catatan Analis:** Untuk menjaga stabilitas omzet Rp 243M, fokus 3 bulan pertama adalah **Stabilitas Supply Chain** (Bahan Baku). Jangan melakukan ekspansi mesin sebelum pasokan sampah harian mencapai 80% dari target simulator.
    """)

# --- TAB 8: SUSTAINABILITY COMMAND CENTER (ADVANCED ESG) ---
with tabs[8]:
    st.header("🌍 Advanced ESG Sustainability Command Center")
    st.write("Monitoring multi-dimensi dampak lingkungan, sosial, dan tata kelola berbasis standar internasional.")
    
    # --- ESG CORE CALCULATIONS (NOW GLOBAL) ---
    compliance_score = 94.5 # Fixed simulation for now
    
    # --- ESG TOP METRICS ---
    st.markdown("### 📊 High-Fidelity Impact Real-time")
    e_c1, e_c2, e_c3, e_c4 = st.columns(4)
    
    e_c1.metric("Methane Avoided", f"{methane_avoided:,.1f} kg CO2e", "Environmental")
    e_c2.metric("Landfill Saved", f"{landfill_m3_saved:,.2f} m³", "Spatial Impact")
    e_c3.metric("Jobs Created", f"{social_jobs:,.1f} FTE", "Social Economy")
    e_c4.metric("Tree Equivalence", f"{tree_equivalent:,.0f} Trees", "Annual Bio-Offset")
    
    st.divider()
    
    # --- ESG BALANCE & RATING ---
    r_col1, r_col2 = st.columns([1, 1])
    
    with r_col1:
        st.subheader("🎯 ESG Balance Radar")
        # Dynamic Radar Chart Data based on actual progress
        # If 0 data, all scores are 0
        if total_waste_collected > 0:
            esg_values = [
                min(100, (carbon_offset/1000)*100), # Norm 1 ton carbon
                sustainability_rate, 
                min(100, (partners_needed/20)*100), # Norm 20 partners
                min(100, (money_saved/1e7)*100),    # Norm 10jt economic
                95 # Governance fixed simulation
            ]
        else:
            esg_values = [0, 0, 0, 0, 0]
            
        esg_labels = ['Carbon Offset', 'Resource Circularity', 'Community Reach', 'Economic Value', 'Data Transparency']
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=esg_values,
            theta=esg_labels,
            fill='toself',
            name='Current ESG Profile',
            line_color="#10b981"
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=380,
            margin=dict(t=40, b=40, l=40, r=40)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    with r_col2:
        st.subheader("🏆 Sustainability Rating")
        st.markdown('<div class="jap-sorting-card" style="text-align: center; border-top-color: #f59e0b; background: #fffcf0;">', unsafe_allow_html=True)
        # Dynamic Rating based on progress
        if total_waste_collected > 5000: rating = "AAA"
        elif total_waste_collected > 1000: rating = "AA+"
        elif total_waste_collected > 500: rating = "A"
        elif total_waste_collected > 0: rating = "B"
        else: rating = "Pending"
        
        st.markdown(f"<h1 style='font-size: 5rem; color: #f59e0b; margin: 0;'>{rating}</h1>", unsafe_allow_html=True)
        st.markdown("**AgriSensa Strategic ESG Rating**")
        st.write(f"Status: *{'Market Leader' if rating != 'Pending' else 'Awaiting Initial Logs'}*")
        st.progress(sustainability_rate/100 if sustainability_rate > 0 else 0, text=f"{sustainability_rate:.0f}% Compliance to Strategy")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f"""
        **🔗 Governance Integrity (Immutable Traceability)**
        > `Batch_ID: AS-{trace_hash}`  
        > `Status: Verified on Simulated Ledger`
        """)
        
    st.divider()
    
    # --- DEEP ANALYTICS ---
    st.subheader("📋 Detailed ESG Breakdown")
    tab_e1, tab_e2, tab_e3 = st.tabs(["🌱 Environmental Depth", "👥 Social Value", "⚖️ Governance Audit"])
    
    with tab_e1:
        st.write("Analisis mendalam mengenai kontribusi terhadap mitigasi perubahan iklim.")
        ec1, ec2 = st.columns(2)
        with ec1:
            st.info(f"**Bio-Regeneration**: Mengonversi {organic_processed:,.0f}kg sampah menjadi nutrisi tanah, mencegah pelepasan gas metana yang 21x lebih berbahaya dari CO2.")
        with ec2:
            st.success(f"**Circular Loop**: {plastic_recycled:,.0f}kg plastik diolah menjadi produk high-value, mengurangi permintaan plastik virgin sebesar 1.1x berat input.")
            
    with tab_e2:
        st.write("Dampak nyata bagi kesejahteraan masyarakat dan inklusivitas.")
        sc1, sc2 = st.columns(2)
        sc1.write(f"- **Peluang Kerja:** Proyeksi penyerapan {social_jobs:.1f} tenaga kerja lokal.")
        sc1.write(f"- **Edukasi:** {edu_reach:,.0f} orang mendapatkan literasi pemilahan sampah.")
        sc2.image("https://img.icons8.com/isometric/100/Conference.png", width=80)
        
    with tab_e3:
        st.write("Transparansi data dan kepatuhan terhadap standar operasional.")
        gc1, gc2 = st.columns([2,1])
        with gc1:
            audit_data = {
                "Audit Parameter": ["Data Accuracy", "SOP Discipline", "Safety Compliance", "Traceability Index"],
                "Score (%)": [98, 92, 95, 100],
                "Status": ["Certified", "High", "Certified", "Impenetrable"]
            }
            st.table(pd.DataFrame(audit_data))
        with gc2:
            st.image("https://img.icons8.com/isometric/100/Checked-Identification_Card.png", width=80)

    # --- COMPLIANCE ROADMAP TO GOLD STANDARD ---
    st.divider()
    st.subheader("📜 Compliance Roadmap to Certification")
    st.write("Untuk mendapatkan sertifikat **AgriSensa Gold Standard**, proyek Anda harus memenuhi kriteria berikut:")
    
    # Define thresholds
    t_diversion = 80.0
    t_carbon = 100.0
    t_partners = 5
    t_circularity = 2500.0
    
    # Checks
    c_div = sustainability_rate >= t_diversion
    c_carb = carbon_offset >= t_carbon
    c_part = partners_needed >= t_partners
    c_circ = value_per_kg >= t_circularity
    c_gov = True # Hash exists
    
    comp_col1, comp_col2 = st.columns(2)
    
    with comp_col1:
        st.markdown(f"{'✅' if c_div else '❌'} **Waste Diversion Rate** ({sustainability_rate:.1f}% / {t_diversion}%)")
        st.markdown(f"{'✅' if c_carb else '❌'} **Carbon Impact Offset** ({carbon_offset:.1f} / {t_carbon} kg CO2e)")
        st.markdown(f"{'✅' if c_part else '❌'} **Institutional Partners** ({partners_needed:.0f} / {t_partners} Mitra)")
        
    with comp_col2:
        st.markdown(f"{'✅' if c_circ else '❌'} **Circularity Index** (Rp {value_per_kg:,.0f} / Rp {t_circularity:,.0f})")
        st.markdown(f"✅ **Governance Traceability** (Batch ID: {trace_hash})")
        st.markdown(f"✅ **Regulatory Alignment** (Standard ISO/ESG Ready)")

    # Final Certification Status
    gold_certified = all([c_div, c_carb, c_part, c_circ, c_gov])
    
    # Show Final Certificate Look
    st.markdown("---")
    if gold_certified:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #fffcf0 0%, #fff 100%); padding: 30px; border-radius: 20px; border: 3px solid #f59e0b; text-align: center; box-shadow: 0 10px 40px rgba(245, 158, 11, 0.15);">
            <img src="https://img.icons8.com/isometric/100/World-Peace.png" width="80" style="margin-bottom: 10px;">
            <h2 style="color: #b45309; margin: 0; letter-spacing: 2px;">CERTIFIED SUSTAINABLE ECOSYSTEM</h2>
            <p style="color: #d97706; font-weight: 600;">AgriSensa Gold Standard for Circular Economy</p>
            <hr style="border-color: rgba(245, 158, 11, 0.2);">
            <p style="color: #92400e; font-size: 0.9rem;">Proyek ini secara resmi diakui telah mencapai efisiensi daur ulang optimal dan dampak karbon terukur.</p>
            <p style="font-family: monospace; color: #b45309; font-weight: bold; font-size: 1.1rem;">Ref ID: AGR-2025-ESG-{trace_hash[:8]}</p>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 30px; border-radius: 20px; border: 2px dashed #cbd5e1; text-align: center;">
            <h4 style="color: #475569; margin-bottom: 5px;">STATUS: AUDIT PENDING</h4>
            <p style="color: #64748b; font-size: 0.9rem;">Selesaikan kriteria di atas untuk mengaktifkan Sertifikat Gold Standard.</p>
            <p style="font-family: monospace; color: #94a3b8;">Current Ref ID: PENDING-LOGS-{datetime.now().strftime('%Y%m')}</p>
        </div>
        """, unsafe_allow_html=True)
# --- TAB 9: BUSINESS INTELLIGENCE ---
with tabs[9]:
    st.header("💼 Business Intelligence Center")
    st.write("Analisis keuangan mendalam untuk pengambilan keputusan strategis.")
    
    bi_tab1, bi_tab2, bi_tab3 = st.tabs(["💹 Harga Pasar Real-Time", "🏦 Model Pendanaan", "📊 Break-Even Analysis"])
    
    # --- BI TAB 1: MARKET PRICE SIMULATION ---
    with bi_tab1:
        st.subheader("💹 Simulasi Harga Pasar (Market Price Feed)")
        st.info("💡 **Catatan:** Ini adalah simulasi. Data aktual dapat diintegrasikan dengan API e-commerce di masa depan.")
        
        mp_col1, mp_col2 = st.columns(2)
        
        with mp_col1:
            st.markdown("**🟢 Harga Jual Produk Anda**")
            sim_price_fertilizer = st.slider("Harga Pupuk Organik (Rp/kg)", 1000, 10000, price_organic, step=100, key="mp_fert")
            sim_price_filament = st.slider("Harga Filamen 3D (Rp/kg)", 50000, 500000, price_filament, step=5000, key="mp_fila")
            
            st.markdown("**🟡 Harga Beli Bahan Baku (Simulasi WasteBank)")
            sim_buy_organic = st.slider("Harga Beli Sampah Organik (Rp/kg)", 0, 1000, 200, step=50, key="mp_buyorg")
            sim_buy_plastic = st.slider("Harga Beli Sampah Plastik (Rp/kg)", 0, 5000, 1500, step=100, key="mp_buypla")
        
        with mp_col2:
            st.markdown("**📊 Margin Analisis**")
            
            margin_fertilizer = sim_price_fertilizer - (sim_buy_organic / s_yield_organic)
            margin_filament = sim_price_filament - (sim_buy_plastic / 0.9)
            
            st.metric("Gross Margin Pupuk", f"Rp {margin_fertilizer:,.0f}/kg", delta=f"{(margin_fertilizer/sim_price_fertilizer)*100:.1f}%")
            st.metric("Gross Margin Filamen", f"Rp {margin_filament:,.0f}/kg", delta=f"{(margin_filament/sim_price_filament)*100:.1f}%")
            
            # Chart: Price Comparison
            price_df = pd.DataFrame({
                "Produk": ["Pupuk", "Filamen"],
                "Harga Jual": [sim_price_fertilizer, sim_price_filament],
                "HPP (Bahan Baku)": [sim_buy_organic / s_yield_organic, sim_buy_plastic / 0.9]
            })
            fig_price = px.bar(price_df, x="Produk", y=["Harga Jual", "HPP (Bahan Baku)"], barmode="group", title="Perbandingan Harga Jual vs HPP")
            st.plotly_chart(fig_price, use_container_width=True)
    
    # --- BI TAB 2: FUNDING MODEL ---
    with bi_tab2:
        st.subheader("🏦 Simulasi Struktur Pendanaan Proyek")
        st.write("Tentukan komposisi sumber modal untuk proyek Waste-to-Value Anda.")
        
        fund_col1, fund_col2 = st.columns([1, 2])
        
        with fund_col1:
            st.markdown("**💰 Sumber Pendanaan (Rp Juta)**")
            fund_internal = st.number_input("Kas Internal / Swadaya", 0, 1000, 50, step=10) * 1e6
            fund_investor = st.number_input("Investor (Equity)", 0, 1000, 100, step=10) * 1e6
            fund_loan = st.number_input("Pinjaman Bank", 0, 1000, 50, step=10) * 1e6
            fund_csr = st.number_input("Hibah CSR / Donasi", 0, 500, 20, step=5) * 1e6
            fund_gov = st.number_input("Subsidi Pemerintah", 0, 500, 30, step=5) * 1e6
            
            total_funding = fund_internal + fund_investor + fund_loan + fund_csr + fund_gov
        
        with fund_col2:
            st.markdown("**📊 Visualisasi & Analisis Keuangan**")
            
            # Pie Chart
            funding_data = {
                "Sumber": ["Kas Internal", "Investor", "Pinjaman Bank", "Hibah CSR", "Subsidi Pemerintah"],
                "Nominal": [fund_internal, fund_investor, fund_loan, fund_csr, fund_gov]
            }
            fig_fund = px.pie(funding_data, values="Nominal", names="Sumber", title=f"Struktur Pendanaan (Total: Rp {total_funding/1e6:,.0f} Juta)", hole=0.4)
            st.plotly_chart(fig_fund, use_container_width=True)
            
            # Financial Ratios
            debt = fund_loan
            equity = fund_internal + fund_investor + fund_csr + fund_gov
            der = (debt / equity) * 100 if equity > 0 else 0
            
            ratio_col1, ratio_col2, ratio_col3 = st.columns(3)
            ratio_col1.metric("Total Modal", f"Rp {total_funding/1e6:,.0f}M")
            ratio_col2.metric("Debt-to-Equity Ratio", f"{der:.1f}%", delta="Sehat" if der < 100 else "Risiko Tinggi")
            ratio_col3.metric("Coverage CAPEX", f"{(total_funding/total_capex)*100:.0f}%" if total_capex > 0 else "N/A")
            
            if total_funding < total_capex:
                st.warning(f"⚠️ **Funding Gap:** Modal Anda masih kurang **Rp {(total_capex - total_funding)/1e6:,.0f} Juta** untuk menutup kebutuhan CAPEX.")
            else:
                st.success(f"✅ **Fully Funded:** Modal Anda cukup dengan surplus **Rp {(total_funding - total_capex)/1e6:,.0f} Juta** untuk modal kerja awal.")
    
    # --- BI TAB 3: BREAK-EVEN ANALYSIS ---
    with bi_tab3:
        st.subheader("📊 Break-Even Point (BEP) Analysis")
        st.write("Analisis titik impas untuk mengetahui kapan bisnis mulai menghasilkan profit.")
        
        bep_col1, bep_col2 = st.columns([1, 2])
        
        with bep_col1:
            st.markdown("**⚙️ Parameter BEP**")
            bep_fixed_cost = st.number_input("Biaya Tetap Bulanan (Rp Juta)", 1, 500, int((o_maint + (operators_needed * o_labor_base))/1e6), step=1) * 1e6
            bep_var_cost = st.number_input("Biaya Variabel per Kg (Rp)", 100, 50000, 500, step=100)
            bep_sell_price = st.number_input("Harga Jual Rata-rata per Kg (Rp)", 1000, 500000, int((price_organic + price_filament)/2), step=500)
            
            # BEP Calculation
            contribution_margin = bep_sell_price - bep_var_cost
            bep_units = bep_fixed_cost / contribution_margin if contribution_margin > 0 else 0
            bep_revenue = bep_units * bep_sell_price
        
        with bep_col2:
            st.markdown("**🎯 Hasil Analisis BEP**")
            
            bep_m1, bep_m2, bep_m3 = st.columns(3)
            bep_m1.metric("BEP Unit", f"{bep_units:,.0f} kg/bulan")
            bep_m2.metric("BEP Revenue", f"Rp {bep_revenue/1e6:,.1f} Juta")
            bep_m3.metric("Contribution Margin", f"Rp {contribution_margin:,.0f}/kg")
            
            # BEP Chart
            units_range = list(range(0, int(bep_units * 2.5) + 100, max(1, int(bep_units / 10))))
            bep_chart_data = pd.DataFrame({
                "Produksi (kg)": units_range,
                "Total Revenue": [u * bep_sell_price for u in units_range],
                "Total Cost": [bep_fixed_cost + (u * bep_var_cost) for u in units_range]
            })
            
            fig_bep = go.Figure()
            fig_bep.add_trace(go.Scatter(x=bep_chart_data["Produksi (kg)"], y=bep_chart_data["Total Revenue"], name="Revenue", line=dict(color="#10b981", width=3)))
            fig_bep.add_trace(go.Scatter(x=bep_chart_data["Produksi (kg)"], y=bep_chart_data["Total Cost"], name="Total Cost", line=dict(color="#ef4444", width=3)))
            fig_bep.add_vline(x=bep_units, line_dash="dash", line_color="#3b82f6", annotation_text=f"BEP: {bep_units:,.0f} kg")
            fig_bep.update_layout(title="Grafik Break-Even Point", xaxis_title="Produksi (kg)", yaxis_title="Nilai (Rp)", legend=dict(orientation="h"))
            st.plotly_chart(fig_bep, use_container_width=True)
            
            # Sensitivity Analysis
            st.markdown("**🔬 Analisis Sensitivitas (What-If)**")
            sens_price_change = st.slider("Jika Harga Jual Berubah (%)", -30, 30, 0, step=5)
            
            new_price = bep_sell_price * (1 + sens_price_change/100)
            new_cm = new_price - bep_var_cost
            new_bep = bep_fixed_cost / new_cm if new_cm > 0 else float('inf')
            
            if sens_price_change != 0:
                delta_bep = ((new_bep - bep_units) / bep_units) * 100 if bep_units > 0 else 0
                st.info(f"💡 Jika harga jual berubah **{sens_price_change:+d}%**, BEP menjadi **{new_bep:,.0f} kg** ({delta_bep:+.1f}% dari baseline).")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.9rem;">
    <p><b>AgriSensa Eco System v1.1</b> | Integrated Waste Management Model</p>
    <p>Kolaborasi Menghasilkan Keberlanjutan</p>
</div>
""", unsafe_allow_html=True)
