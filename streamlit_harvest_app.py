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
st.set_page_config(
    page_title="Database Panen - AgriSensa",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

# ========== CUSTOM CSS ==========
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #059669;
        text-align: center;
        margin-bottom: 1rem;
    }
    .stat-card {
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 2px solid #10b981;
        text-align: center;
    }
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        color: #059669;
    }
    .stat-label {
        color: #6b7280;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    .record-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .success-box {
        background: #d1fae5;
        border: 2px solid #10b981;
        border-radius: 8px;
        padding: 1rem;
        color: #065f46;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fef3c7;
        border: 2px solid #f59e0b;
        border-radius: 8px;
        padding: 1rem;
        color: #92400e;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ========== MAIN APP ==========
def main():
    # Header
    st.markdown('<h1 class="main-header">🌾 Database Panen AgriSensa</h1>', unsafe_allow_html=True)
    st.markdown("**Catat, Analisis, dan Visualisasikan Data Hasil Panen Anda**")
    
    # Sidebar Navigation
    st.sidebar.title("📋 Menu")
    menu = st.sidebar.radio(
        "Pilih Halaman:",
        ["📊 Dashboard", "➕ Tambah Data Panen", "📝 Lihat & Edit Data", "📈 Analisis & Visualisasi", "💾 Export Data"]
    )
    
    # Load data
    data = load_data()
    
    # ========== PAGE: DASHBOARD ==========
    if menu == "📊 Dashboard":
        st.header("📊 Dashboard Ringkasan")
        
        if not data:
            st.info("👋 Belum ada data panen. Mulai dengan menambahkan data panen pertama Anda!")
        else:
            # Calculate statistics
            total_records = len(data)
            total_quantity = sum(r.get('total_quantity', 0) for r in data)
            total_value = sum(r.get('total_value', 0) for r in data)
            total_profit = sum(r.get('profit', 0) for r in data)
            
            # Display stats
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{total_records}</div>
                    <div class="stat-label">Total Catatan Panen</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">{total_quantity:,.0f} kg</div>
                    <div class="stat-label">Total Hasil Panen</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">Rp {total_value:,.0f}</div>
                    <div class="stat-label">Total Pendapatan</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-value">Rp {total_profit:,.0f}</div>
                    <div class="stat-label">Total Keuntungan</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Recent harvests
            st.subheader("🕒 5 Panen Terakhir")
            recent = sorted(data, key=lambda x: x.get('harvest_date', ''), reverse=True)[:5]
            
            for record in recent:
                with st.expander(f"🌾 {record['commodity']} - {record['harvest_date']} ({record['farmer_name']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Lokasi:** {record['location']}")
                        st.write(f"**Total Hasil:** {record.get('total_quantity', 0):.2f} kg")
                        st.write(f"**Pendapatan:** Rp {record.get('total_value', 0):,.0f}")
                    with col2:
                        st.write(f"**Biaya:** Rp {record.get('total_cost', 0):,.0f}")
                        st.write(f"**Keuntungan:** Rp {record.get('profit', 0):,.0f}")
                        st.write(f"**Margin:** {record.get('profit_margin', 0):.2f}%")
    
    # ========== PAGE: ADD RECORD ==========
    elif menu == "➕ Tambah Data Panen":
        st.header("➕ Tambah Data Panen Baru")
        
        # Number of criteria OUTSIDE form for reactivity
        st.subheader("📊 Kriteria Hasil Panen")
        st.info("Tambahkan minimal 1 kriteria (ukuran/grade) hasil panen")
        num_criteria = st.number_input("Jumlah Kriteria", min_value=1, max_value=5, value=1, 
                                       help="Ubah angka ini untuk menambah/mengurangi jumlah kriteria")
        
        with st.form("add_harvest_form"):
            st.subheader("📝 Informasi Petani")
            col1, col2 = st.columns(2)
            with col1:
                farmer_name = st.text_input("Nama Petani *", placeholder="Contoh: Budi Santoso")
                farmer_phone = st.text_input("No. Telepon *", placeholder="08123456789")
            with col2:
                commodity = st.selectbox("Komoditas *", [
                    "Padi", "Jagung", "Kedelai", "Cabai Merah", "Cabai Rawit",
                    "Tomat", "Kentang", "Bawang Merah", "Bawang Putih"
                ])
                location = st.text_input("Lokasi Lahan *", placeholder="Contoh: Desa Sukamaju, Kec. Cianjur")
            
            harvest_date = st.date_input("Tanggal Panen *", value=date.today())
            harvest_sequence = st.number_input("Panen Ke-", min_value=1, value=1, step=1)
            
            st.markdown("---")
            st.markdown(f"### Input Data untuk {num_criteria} Kriteria")
            criteria = []
            
            for i in range(num_criteria):
                st.markdown(f"**Kriteria {i+1}**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    size = st.text_input(f"Ukuran/Grade {i+1}", key=f"size_{i}", placeholder="Contoh: Besar, Sedang, Kecil")
                with col2:
                    quantity = st.number_input(f"Jumlah (kg) {i+1}", min_value=0.0, key=f"qty_{i}", step=0.1)
                with col3:
                    price = st.number_input(f"Harga/kg (Rp) {i+1}", min_value=0.0, key=f"price_{i}", step=100.0)
                
                if size and quantity > 0 and price > 0:
                    criteria.append({
                        'size': size,
                        'quantity_kg': quantity,
                        'price_per_kg': price,
                        'total': quantity * price
                    })
            
            st.subheader("💰 Biaya Produksi (Opsional)")
            col1, col2 = st.columns(2)
            with col1:
                cost_seed = st.number_input("Bibit/Benih (Rp)", min_value=0.0, step=1000.0)
                cost_fertilizer = st.number_input("Pupuk (Rp)", min_value=0.0, step=1000.0)
                cost_pesticide = st.number_input("Pestisida (Rp)", min_value=0.0, step=1000.0)
            with col2:
                cost_labor = st.number_input("Tenaga Kerja (Rp)", min_value=0.0, step=1000.0)
                cost_equipment = st.number_input("Peralatan (Rp)", min_value=0.0, step=1000.0)
                cost_other = st.number_input("Lain-lain (Rp)", min_value=0.0, step=1000.0)
            
            costs = {
                'bibit': cost_seed,
                'pupuk': cost_fertilizer,
                'pestisida': cost_pesticide,
                'tenaga_kerja': cost_labor,
                'peralatan': cost_equipment,
                'lainnya': cost_other
            }
            
            st.subheader("📝 Informasi Tambahan")
            weather = st.selectbox("Cuaca Saat Panen", ["Cerah", "Berawan", "Hujan Ringan", "Hujan Lebat"])
            notes = st.text_area("Catatan", placeholder="Tambahkan catatan penting tentang panen ini...")
            
            submitted = st.form_submit_button("💾 Simpan Data Panen", use_container_width=True)
            
            if submitted:
                if not farmer_name or not farmer_phone or not commodity or not location:
                    st.error("❌ Mohon lengkapi semua field yang wajib diisi (*)")
                elif len(criteria) == 0:
                    st.error("❌ Tambahkan minimal 1 kriteria hasil panen")
                else:
                    # Calculate totals
                    total_quantity, total_value = calculate_totals(criteria)
                    profitability = calculate_profitability(total_value, costs)
                    
                    # Create record
                    record = {
                        'farmer_name': farmer_name,
                        'farmer_phone': farmer_phone,
                        'commodity': commodity,
                        'location': location,
                        'harvest_date': harvest_date.isoformat(),
                        'harvest_sequence': harvest_sequence,
                        'criteria': criteria,
                        'total_quantity': total_quantity,
                        'total_value': total_value,
                        'costs': costs,
                        **profitability,
                        'weather': weather,
                        'notes': notes
                    }
                    
                    add_record(record)
                    st.success("✅ Data panen berhasil disimpan!")
                    st.balloons()
                    
                    # Show summary
                    st.markdown(f"""
                    <div class="success-box">
                        <h4>📊 Ringkasan Panen</h4>
                        <p><strong>Total Hasil:</strong> {total_quantity:.2f} kg</p>
                        <p><strong>Pendapatan:</strong> Rp {total_value:,.0f}</p>
                        <p><strong>Biaya:</strong> Rp {profitability['total_cost']:,.0f}</p>
                        <p><strong>Keuntungan:</strong> Rp {profitability['profit']:,.0f}</p>
                        <p><strong>Margin:</strong> {profitability['profit_margin']:.2f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ========== PAGE: VIEW & EDIT ==========
    elif menu == "📝 Lihat & Edit Data":
        st.header("📝 Lihat & Edit Data Panen")
        
        if not data:
            st.info("Belum ada data panen yang tersimpan.")
        else:
            # Filters
            st.subheader("🔍 Filter Data")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                commodities = list(set(r['commodity'] for r in data))
                filter_commodity = st.selectbox("Filter Komoditas", ["Semua"] + commodities)
            
            with col2:
                farmers = list(set(r['farmer_name'] for r in data))
                filter_farmer = st.selectbox("Filter Petani", ["Semua"] + farmers)
            
            with col3:
                sort_by = st.selectbox("Urutkan Berdasarkan", ["Tanggal (Terbaru)", "Tanggal (Terlama)", "Pendapatan (Tertinggi)", "Keuntungan (Tertinggi)"])
            
            # Apply filters
            filtered_data = data.copy()
            if filter_commodity != "Semua":
                filtered_data = [r for r in filtered_data if r['commodity'] == filter_commodity]
            if filter_farmer != "Semua":
                filtered_data = [r for r in filtered_data if r['farmer_name'] == filter_farmer]
            
            # Apply sorting
            if sort_by == "Tanggal (Terbaru)":
                filtered_data.sort(key=lambda x: x.get('harvest_date', ''), reverse=True)
            elif sort_by == "Tanggal (Terlama)":
                filtered_data.sort(key=lambda x: x.get('harvest_date', ''))
            elif sort_by == "Pendapatan (Tertinggi)":
                filtered_data.sort(key=lambda x: x.get('total_value', 0), reverse=True)
            elif sort_by == "Keuntungan (Tertinggi)":
                filtered_data.sort(key=lambda x: x.get('profit', 0), reverse=True)
            
            st.write(f"**Menampilkan {len(filtered_data)} dari {len(data)} catatan**")
            
            # Display records
            for record in filtered_data:
                with st.expander(f"🌾 {record['commodity']} - {record['harvest_date']} - {record['farmer_name']}"):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**Petani:** {record['farmer_name']} ({record['farmer_phone']})")
                        st.write(f"**Lokasi:** {record['location']}")
                        st.write(f"**Panen Ke-:** {record.get('harvest_sequence', 1)}")
                        st.write(f"**Cuaca:** {record.get('weather', '-')}")
                        
                        if record.get('notes'):
                            st.write(f"**Catatan:** {record['notes']}")
                        
                        st.markdown("**Kriteria Hasil:**")
                        for i, c in enumerate(record.get('criteria', []), 1):
                            st.write(f"{i}. {c['size']}: {c['quantity_kg']} kg × Rp {c['price_per_kg']:,.0f} = Rp {c['total']:,.0f}")
                    
                    with col2:
                        st.metric("Total Hasil", f"{record.get('total_quantity', 0):.2f} kg")
                        st.metric("Pendapatan", f"Rp {record.get('total_value', 0):,.0f}")
                        st.metric("Biaya", f"Rp {record.get('total_cost', 0):,.0f}")
                        st.metric("Keuntungan", f"Rp {record.get('profit', 0):,.0f}", 
                                 delta=f"{record.get('profit_margin', 0):.1f}%")
                    
                    # Delete button
                    if st.button(f"🗑️ Hapus Data", key=f"del_{record['id']}"):
                        delete_record(record['id'])
                        st.success("Data berhasil dihapus!")
                        st.rerun()
    
    # ========== PAGE: ANALYTICS ==========
    elif menu == "📈 Analisis & Visualisasi":
        st.header("📈 Analisis & Visualisasi Data")
        
        if not data:
            st.info("Belum ada data untuk divisualisasikan.")
        else:
            # Convert to DataFrame
            df = pd.DataFrame(data)
            
            # Commodity Distribution
            st.subheader("📊 Distribusi Komoditas")
            commodity_counts = df['commodity'].value_counts()
            fig_commodity = px.pie(
                values=commodity_counts.values,
                names=commodity_counts.index,
                title="Distribusi Jumlah Panen per Komoditas",
                color_discrete_sequence=px.colors.sequential.Greens
            )
            st.plotly_chart(fig_commodity, use_container_width=True)
            
            # Revenue by Commodity
            st.subheader("💰 Pendapatan per Komoditas")
            revenue_by_commodity = df.groupby('commodity')['total_value'].sum().sort_values(ascending=False)
            fig_revenue = px.bar(
                x=revenue_by_commodity.index,
                y=revenue_by_commodity.values,
                labels={'x': 'Komoditas', 'y': 'Total Pendapatan (Rp)'},
                title="Total Pendapatan per Komoditas",
                color=revenue_by_commodity.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig_revenue, use_container_width=True)
            
            # Monthly Trend
            st.subheader("📅 Tren Bulanan")
            df['month'] = pd.to_datetime(df['harvest_date']).dt.to_period('M').astype(str)
            monthly_data = df.groupby('month').agg({
                'total_quantity': 'sum',
                'total_value': 'sum',
                'profit': 'sum'
            }).reset_index()
            
            fig_trend = go.Figure()
            fig_trend.add_trace(go.Scatter(
                x=monthly_data['month'],
                y=monthly_data['total_quantity'],
                name='Total Hasil (kg)',
                mode='lines+markers',
                line=dict(color='#10b981', width=3)
            ))
            fig_trend.update_layout(
                title="Tren Hasil Panen Bulanan",
                xaxis_title="Bulan",
                yaxis_title="Total Hasil (kg)",
                hovermode='x unified'
            )
            st.plotly_chart(fig_trend, use_container_width=True)
            
            # Profitability Analysis
            st.subheader("💹 Analisis Profitabilitas")
            col1, col2 = st.columns(2)
            
            with col1:
                avg_margin = df['profit_margin'].mean()
                st.metric("Rata-rata Margin Keuntungan", f"{avg_margin:.2f}%")
                
                top_profitable = df.nlargest(5, 'profit')[['commodity', 'harvest_date', 'profit']]
                st.write("**Top 5 Panen Paling Menguntungkan:**")
                for idx, row in top_profitable.iterrows():
                    st.write(f"• {row['commodity']} ({row['harvest_date']}): Rp {row['profit']:,.0f}")
            
            with col2:
                avg_roi = df['roi'].mean()
                st.metric("Rata-rata ROI", f"{avg_roi:.2f}%")
                
                profitable_commodities = df.groupby('commodity')['profit'].mean().sort_values(ascending=False)
                st.write("**Komoditas Paling Menguntungkan (Rata-rata):**")
                for commodity, profit in profitable_commodities.head(5).items():
                    st.write(f"• {commodity}: Rp {profit:,.0f}")
    
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
