# Database Panen - Streamlit Version
# Aplikasi standalone untuk mencatat dan memvisualisasikan data hasil panen

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import json
import os
import uuid

# ========== CONFIGURATION ==========
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Database Panen - AgriSensa",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================







# ========== DATA STORAGE ==========
DATA_FILE = "harvest_data_streamlit.json"

def load_data():
    """Load harvest data from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_data(data):
    """Save harvest data to JSON file"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_record(record):
    """Add new harvest record"""
    data = load_data()
    record['id'] = str(uuid.uuid4())
    record['created_at'] = datetime.now().isoformat()
    record['updated_at'] = datetime.now().isoformat()
    data.append(record)
    save_data(data)
    return record

def update_record(record_id, updates):
    """Update existing record"""
    data = load_data()
    for i, record in enumerate(data):
        if record['id'] == record_id:
            data[i].update(updates)
            data[i]['updated_at'] = datetime.now().isoformat()
            save_data(data)
            return True
    return False

def delete_record(record_id):
    """Delete record"""
    data = load_data()
    data = [r for r in data if r['id'] != record_id]
    save_data(data)

# ========== CALCULATIONS ==========
def calculate_totals(criteria):
    """Calculate total quantity and value from criteria"""
    total_quantity = sum(c['quantity_kg'] for c in criteria)
    total_value = sum(c['quantity_kg'] * c['price_per_kg'] for c in criteria)
    return total_quantity, total_value

def calculate_profitability(total_value, costs):
    """Calculate profit metrics"""
    total_cost = sum(costs.values())
    profit = total_value - total_cost
    profit_margin = (profit / total_value * 100) if total_value > 0 else 0
    roi = (profit / total_cost * 100) if total_cost > 0 else 0
    return {
        'total_cost': total_cost,
        'profit': profit,
        'profit_margin': round(profit_margin, 2),
        'roi': round(roi, 2)
    }

# ========== CUSTOM CSS (Premium Glassmorphism) ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
    
    * { font-family: 'Outfit', sans-serif; }

    .main {
        background-color: #f8fafc;
    }

    /* Header & Hero */
    .header-container {
        background: linear-gradient(135deg, #065f46 0%, #059669 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 25px -5px rgba(5, 150, 105, 0.3);
    }

    /* Command Center KPI Cards */
    .kpi-container {
        display: flex;
        gap: 20px;
        margin-bottom: 30px;
    }
    .kpi-card {
        flex: 1;
        background: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-5px);
        border-color: #10b981;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 5px;
    }
    .kpi-label {
        color: #64748b;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Feed Entry Cards */
    .harvest-card {
        background: white;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        padding: 0;
        margin-bottom: 20px;
        overflow: hidden;
        transition: all 0.3s ease;
    }
    .harvest-card:hover {
        box-shadow: 0 12px 20px -10px rgba(0,0,0,0.1);
    }
    .card-header {
        background: #f8fafc;
        padding: 15px 25px;
        border-bottom: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .card-body {
        padding: 25px;
    }
    .metric-pill {
        display: inline-flex;
        align-items: center;
        background: #f1f5f9;
        padding: 6px 12px;
        border-radius: 30px;
        font-size: 0.85rem;
        color: #475569;
        font-weight: 600;
        margin-right: 10px;
        margin-bottom: 10px;
        border: 1px solid #e2e8f0;
    }
    
    /* Scientific Colors */
    .color-yield { border-left: 5px solid #10b981; }
    .color-profit { border-left: 5px solid #8b5cf6; }
    .color-loss { border-left: 5px solid #ef4444; }

    /* Forms & Inputs */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

def icon_score(score):
    if score >= 85: return "⭐⭐⭐ Excellent"
    if score >= 70: return "⭐⭐ Good"
    return "⭐ Average"

# ========== MAIN APP ==========
def main():
    # Header Hero
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; color:white; font-size:2.8rem;">🌾 Database Panen AgriSensa</h1>
        <p style="margin:0; opacity:0.9; font-size:1.1rem; font-weight:300;">Command Center: Catat, Analisis, dan Visualisasikan Hasil Produksi Anda</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Navigation
    st.sidebar.title("🍱 Navigation")
    menu = st.sidebar.radio(
        "Pilih Halaman:",
        ["📊 Dashboard", "➕ Tambah Data Panen", "📝 Lihat & Edit Data", "📈 Analisis & Visualisasi", "💾 Export Data"]
    )
    
    # Load data
    data = load_data()
    
    # ========== PAGE: DASHBOARD ==========
    if menu == "📊 Dashboard":
        if not data:
            st.info("👋 Belum ada data panen. Mulai dengan menambahkan data panen pertama Anda!")
        else:
            # Calculate productivity metrics
            total_records = len(data)
            total_quantity = sum(r.get('total_quantity', 0) for r in data)
            total_value = sum(r.get('total_value', 0) for r in data)
            total_profit = sum(r.get('profit', 0) for r in data)
            avg_margin = sum(r.get('profit_margin', 0) for r in data) / total_records if total_records > 0 else 0
            
            # New Scientific Metric: Total Productivity (if area exists)
            total_ha = sum(r.get('land_size_ha', 0.1) for r in data if 'land_size_ha' in r)
            avg_yield_ha = (total_quantity / 1000) / total_ha if total_ha > 0 else 0

            # KPI Command Center
            st.markdown(f"""
            <div class="kpi-container">
                <div class="kpi-card">
                    <div class="kpi-value">{total_records}</div>
                    <div class="kpi-label">Total Panen</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{total_quantity/1000:,.1f} Ton</div>
                    <div class="kpi-label">Total Produksi</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value">{avg_yield_ha:,.2f}</div>
                    <div class="kpi-label">Ton / Hektar (Avg)</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-value" style="color:#16a34a;">Rp {total_profit/1000000:,.1f}M</div>
                    <div class="kpi-label">Estimasi Profit</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Recent harvests - Premium Feed Style
            st.subheader("🕒 Riwayat Panen Terakhir")
            recent = sorted(data, key=lambda x: x.get('harvest_date', ''), reverse=True)[:5]
            
            for record in recent:
                p_margin = record.get('profit_margin', 0)
                color_class = "color-profit" if p_margin > 0 else "color-loss"
                icon = "🟢" if p_margin > 20 else "🟡" if p_margin > 0 else "🔴"
                
                st.markdown(f"""
                <div class="harvest-card {color_class}">
                    <div class="card-header">
                        <span style="font-weight:700; color:#1e293b;">{icon} {record['commodity']} - {record['harvest_date']}</span>
                        <span style="color:#64748b; font-size:0.85rem;">Ref: {record['id'][:8]}</span>
                    </div>
                    <div class="card-body">
                        <div class="metric-pill">📍 {record['location']}</div>
                        <div class="metric-pill">🚜 {record['farmer_name']}</div>
                        <div class="metric-pill">⚖️ {record.get('total_quantity', 0):,.0f} kg</div>
                        <div class="metric-pill">💰 Rp {record.get('total_value', 0):,.0f}</div>
                        <div class="metric-pill" style="background:#f0fdf4; color:#16a34a;">📈 Profit: Rp {record.get('profit', 0):,.0f} ({p_margin:.1f}%)</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # ========== PAGE: ADD RECORD ==========
    elif menu == "➕ Tambah Data Panen":
        st.header("➕ Form Input Panen Presisi")
        
        # Number of criteria OUTSIDE form for reactivity
        st.subheader("📊 Konfigurasi & Identifikasi")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.info("Konfigurasi Lahan & Grade")
            num_criteria = st.number_input("Jumlah Kriteria/Grade", min_value=1, max_value=5, value=1)
            land_size_ha = st.number_input("Luas Lahan Panen (Hektar)", min_value=0.01, value=1.0, step=0.01)
        
        with col_c2:
            st.info("Pilih atau Ketik Komoditas")
            commodity_options = [
                "Padi Inpari", "Jagung Hibrida", "Kedelai", "Cabai Rawit", "Cabai Merah",
                "Tomat", "Kentang", "Bawang Merah", "Bawang Putih", "Melon", "Semangka",
                "Lainnya (Ketik Manual)"
            ]
            commodity_choice = st.selectbox("Komoditas Identifikasi *", commodity_options)
            if commodity_choice == "Lainnya (Ketik Manual)":
                commodity = st.text_input("Ketik Nama Komoditas *", placeholder="Misal: Vanili, Porang, dll")
            else:
                commodity = commodity_choice
        
        st.markdown("---")
        
        # Farmer & Location (Also outside for immediate feedback if needed, but safe inside too)
        # However, for a clean look, let's keep the core form as the "Data Entry" spot.
        # But we must ensure all mandatory fields are captured.

        with st.form("add_harvest_form_v2"):
            st.subheader("📝 Metadata Produksi")
            col1, col2 = st.columns(2)
            with col1:
                farmer_name = st.text_input("Nama Petani / Operator *", placeholder="Contoh: Kelompok Tani Makmur")
                farmer_phone = st.text_input("No. WhatsApp *", placeholder="08123456789")
            with col2:
                location = st.text_input("Blok / Nama Lahan *", placeholder="Contoh: Blok A - Sawah Barat")
                harvest_date = st.date_input("Tanggal Aktual Panen", value=date.today())
                harvest_sequence = st.number_input("Urutan Panen (Periode)", min_value=1, value=1)
            
            st.markdown("---")
            st.markdown(f"### ⚖️ Input Grade Produksi ({num_criteria} Grade)")
            criteria = []
            
            for i in range(num_criteria):
                st.markdown(f"**Grade {i+1}**")
                col_g1, col_g2, col_g3 = st.columns(3)
                with col_g1:
                    size = st.text_input(f"Nama Grade {i+1}", key=f"size_{i}", placeholder="Contoh: Super / Grade A")
                with col_g2:
                    quantity = st.number_input(f"Berat (kg) {i+1}", min_value=0.0, key=f"qty_{i}", step=0.1)
                with col_g3:
                    price = st.number_input(f"Harga Jual/kg (Rp) {i+1}", min_value=0.0, key=f"price_{i}", step=100.0)
                
                if size and quantity > 0:
                    criteria.append({
                        'size': size,
                        'quantity_kg': quantity,
                        'price_per_kg': price,
                        'total': quantity * price
                    })
            
            st.markdown("---")
            st.subheader("🧪 Parameter Kualitas (Scientific)")
            col_q1, col_q2, col_q3 = st.columns(3)
            with col_q1:
                moisture = st.slider("Kadar Air (%)", 5, 35, 14, help="Penting untuk standarisasi harga gabah/jagung")
            with col_q2:
                quality_score = st.slider("Indeks Kualitas Fisik", 0, 100, 85, help="Visual, keutuhan bulir, warna")
            with col_q3:
                soil_status = st.selectbox("Kondisi Tanah Akhir", ["Subur", "Menengah", "Kritis", "Sangat Kritis"])

            st.subheader("💰 Biaya Logistik & Produksi")
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                cost_seed = st.number_input("Total Biaya Bibit (Rp)", min_value=0.0, step=1000.0)
                cost_fertilizer = st.number_input("Total Biaya Pupuk (Rp)", min_value=0.0, step=1000.0)
                cost_pesticide = st.number_input("Total Biaya Pestisida (Rp)", min_value=0.0, step=1000.0)
            with col_b2:
                cost_labor = st.number_input("Biaya Tenaga Kerja (Rp)", min_value=0.0, step=1000.0)
                cost_transport = st.number_input("Biaya Transport/Logistik (Rp)", min_value=0.0, step=1000.0)
                cost_other = st.number_input("Biaya Lain-lain (Rp)", min_value=0.0, step=1000.0)
            
            costs = {
                'bibit': cost_seed,
                'pupuk': cost_fertilizer,
                'pestisida': cost_pesticide,
                'tenaga_kerja': cost_labor,
                'transport': cost_transport,
                'lainnya': cost_other
            }
            
            notes = st.text_area("Catatan Strategis", placeholder="Contoh: Serangan hama di akhir masa tanam, penggunaan varietas baru...")
            
            submitted = st.form_submit_button("🚀 SIMPAN DATA KE DATABASE", use_container_width=True)
            
            if submitted:
                if not farmer_name or not location:
                    st.error("❌ Nama Petani dan Lokasi wajib diisi.")
                elif not criteria:
                    st.error("❌ Masukkan minimal 1 data grade hasil panen.")
                else:
                    total_quantity, total_value = calculate_totals(criteria)
                    profitability = calculate_profitability(total_value, costs)
                    
                    # Ton/Ha Calculation
                    productivity_ton_ha = (total_quantity / 1000) / land_size_ha if land_size_ha > 0 else 0
                    
                    record = {
                        'farmer_name': farmer_name,
                        'farmer_phone': farmer_phone,
                        'commodity': commodity,
                        'location': location,
                        'land_size_ha': land_size_ha,
                        'harvest_date': harvest_date.isoformat(),
                        'harvest_sequence': harvest_sequence,
                        'criteria': criteria,
                        'total_quantity': total_quantity,
                        'total_value': total_value,
                        'productivity_ton_ha': productivity_ton_ha,
                        'quality_params': {
                            'moisture': moisture,
                            'quality_score': quality_score,
                            'soil_status': soil_status
                        },
                        'costs': costs,
                        **profitability,
                        'notes': notes
                    }
                    
                    add_record(record)
                    st.success("✅ Rekaman Panen Presisi Berhasil Disimpan!")
                    st.balloons()
                    
                    st.markdown(f"""
                    <div class="success-box">
                        <h4 style="margin-top:0;">📊 Resume Produksi: {commodity}</h4>
                        <p><strong>Produktivitas:</strong> {productivity_ton_ha:.2f} Ton/Ha</p>
                        <p><strong>Total Hasil:</strong> {total_quantity:,.0f} kg ({total_quantity/1000:.1f} Ton)</p>
                        <p><strong>Profit Bersih:</strong> Rp {profitability['profit']:,.0f}</p>
                        <p><strong>Kualitas:</strong> {icon_score(quality_score)} {quality_score}/100</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ========== PAGE: VIEW & EDIT ==========
    elif menu == "📝 Lihat & Edit Data":
        st.header("📝 Database Rekaman Panen")
        
        if not data:
            st.info("Belum ada data panen yang tersimpan.")
        else:
            # Filters
            with st.expander("🔍 Filter & Pengurutan Canggih"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    commodities = list(set(r['commodity'] for r in data))
                    filter_commodity = st.selectbox("Filter Komoditas", ["Semua"] + commodities)
                
                with col2:
                    farmers = list(set(r['farmer_name'] for r in data))
                    filter_farmer = st.selectbox("Filter Petani", ["Semua"] + farmers)
                
                with col3:
                    sort_by = st.selectbox("Urutkan Berdasarkan", ["Tanggal (Terbaru)", "Produktivitas (Tertinggi)", "Profit (Tertinggi)", "Kualitas (Terbaik)"])
            
            # Apply filters
            filtered_data = data.copy()
            if filter_commodity != "Semua":
                filtered_data = [r for r in filtered_data if r['commodity'] == filter_commodity]
            if filter_farmer != "Semua":
                filtered_data = [r for r in filtered_data if r['farmer_name'] == filter_farmer]
            
            # Apply sorting
            if sort_by == "Tanggal (Terbaru)":
                filtered_data.sort(key=lambda x: x.get('harvest_date', ''), reverse=True)
            elif sort_by == "Produktivitas (Tertinggi)":
                filtered_data.sort(key=lambda x: x.get('productivity_ton_ha', 0), reverse=True)
            elif sort_by == "Profit (Tertinggi)":
                filtered_data.sort(key=lambda x: x.get('profit', 0), reverse=True)
            elif sort_by == "Kualitas (Terbaik)":
                filtered_data.sort(key=lambda x: x.get('quality_params', {}).get('quality_score', 0), reverse=True)
            
            st.write(f"**Menampilkan {len(filtered_data)} catatan**")
            
            # Display records - Premium Feed Card
            for record in filtered_data:
                p_ton_ha = record.get('productivity_ton_ha', 0)
                q_score = record.get('quality_params', {}).get('quality_score', 0)
                
                st.markdown(f"""
                <div class="harvest-card color-yield" style="margin-bottom:10px;">
                    <div class="card-header">
                        <span style="font-weight:700;">{record['commodity']} - {record['harvest_date']}</span>
                        <span style="background:#dcfce7; color:#166534; padding:2px 8px; border-radius:10px; font-size:0.75rem;">{p_ton_ha:.2f} Ton/Ha</span>
                    </div>
                    <div class="card-body" style="padding:15px 25px;">
                        <span class="metric-pill">🚜 {record['farmer_name']}</span>
                        <span class="metric-pill">📍 {record['location']}</span>
                        <span class="metric-pill">🧪 Q: {q_score}/100</span>
                        <span class="metric-pill">💧 {record.get('quality_params', {}).get('moisture', 14)}% MC</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.expander("👁️ Detail & Analisis Biaya"):
                    col_d1, col_d2 = st.columns([2, 1])
                    with col_d1:
                        st.subheader("📊 Rincian Grade")
                        for i, c in enumerate(record.get('criteria', []), 1):
                            st.write(f"**{c.get('size', 'N/A')}**: {c['quantity_kg']} kg × Rp {c['price_per_kg']:,.0f} = Rp {c['total']:,.0f}")
                        
                        st.subheader("💰 Struktur Biaya")
                        cost_df = pd.DataFrame(list(record['costs'].items()), columns=['Kategori', 'Nilai (Rp)'])
                        st.table(cost_df)
                    
                    with col_d2:
                        st.metric("Total Hasil", f"{record['total_quantity']:,.0f} kg")
                        st.metric("Total Profit", f"Rp {record['profit']:,.0f}")
                        st.metric("ROI", f"{record.get('roi', 0):.1f}%")
                        
                        if st.button(f"🗑️ Hapus Rekaman", key=f"del_{record['id']}"):
                            delete_record(record['id'])
                            st.rerun()
                st.write("")
    
    # ========== PAGE: ANALYTICS ==========
    elif menu == "📈 Analisis & Visualisasi":
        st.header("📈 Analisis Sains & Performa")
        
        if not data:
            st.info("Belum ada data untuk divisualisasikan.")
        else:
            df = pd.DataFrame(data)
            df['harvest_date'] = pd.to_datetime(df['harvest_date'])
            
            # 1. Benchmark Produktivitas (Ton/Ha)
            st.subheader("🚀 Benchmark Produktivitas (Ton/Ha)")
            if 'productivity_ton_ha' in df.columns:
                prod_by_commodity = df.groupby('commodity')['productivity_ton_ha'].mean().sort_values(ascending=False)
                fig_prod = px.bar(
                    x=prod_by_commodity.index,
                    y=prod_by_commodity.values,
                    labels={'x': 'Komoditas', 'y': 'Ton / Hektar'},
                    color=prod_by_commodity.values,
                    color_continuous_scale='Emrld',
                    title="Rata-rata Hasil per Hektar"
                )
                st.plotly_chart(fig_prod, use_container_width=True)
            else:
                st.warning("Data Ton/Ha belum tersedia pada rekaman lama.")

            col_a1, col_a2 = st.columns(2)
            
            # 2. Profit vs Quality Correlation
            with col_a1:
                st.subheader("🎯 Korelasi Kualitas vs Profit")
                if 'quality_params' in df.columns:
                    # Flatten quality score for plotting
                    df['q_score'] = df['quality_params'].apply(lambda x: x.get('quality_score', 0) if isinstance(x, dict) else 0)
                    fig_corr = px.scatter(
                        df, x='q_score', y='profit',
                        color='commodity', size='total_quantity',
                        labels={'q_score': 'Indeks Kualitas', 'profit': 'Profit (Rp)'},
                        title="Kualitas vs Keuntungan",
                        template="plotly_white"
                    )
                    st.plotly_chart(fig_corr, use_container_width=True)
                else:
                    st.info("Tambahkan data panen baru untuk melihat korelasi kualitas.")

            # 3. Monthly Production Trend
            with col_a2:
                st.subheader("📅 Tren Produksi Bulanan")
                df['month'] = df['harvest_date'].dt.to_period('M').astype(str)
                monthly_qty = df.groupby('month')['total_quantity'].sum().reset_index()
                fig_trend = px.line(
                    monthly_qty, x='month', y='total_quantity',
                    markers=True,
                    labels={'total_quantity': 'Total Hasil (kg)'},
                    title="Volume Produksi per Bulan"
                )
                fig_trend.update_traces(line_color='#059669', line_width=3)
                st.plotly_chart(fig_trend, use_container_width=True)

            st.markdown("---")
            
            # 4. Financial Health Table
            st.subheader("💹 Struktur Keuntungan Komoditas")
            fin_summary = df.groupby('commodity').agg({
                'total_value': 'sum',
                'profit': 'sum',
                'profit_margin': 'mean',
                'roi': 'mean'
            }).reset_index()
            
            # Format numbers for better reading
            fin_summary['total_value'] = fin_summary['total_value'].apply(lambda x: f"Rp {x:,.0f}")
            fin_summary['profit'] = fin_summary['profit'].apply(lambda x: f"Rp {x:,.0f}")
            fin_summary['profit_margin'] = fin_summary['profit_margin'].apply(lambda x: f"{x:.1f}%")
            fin_summary['roi'] = fin_summary['roi'].apply(lambda x: f"{x:.1f}%")
            
            st.table(fin_summary.rename(columns={
                'commodity': 'Komoditas',
                'total_value': 'Total Omzet',
                'profit': 'Total Profit',
                'profit_margin': 'Margin (Avg)',
                'roi': 'ROI (Avg)'
            }))
    
    # ========== PAGE: EXPORT ==========
    elif menu == "💾 Export Data":
        st.header("💾 Export Data")
        
        if not data:
            st.info("Belum ada data untuk di-export.")
        else:
            st.write(f"**Total Data:** {len(data)} catatan panen")
            
            # Export to CSV
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False).encode('utf-8')
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"harvest_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_str = json.dumps(data, ensure_ascii=False, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"harvest_data_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
            
            # Preview data
            st.subheader("👀 Preview Data")
            st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()
