import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

# Page config
from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Kalkulator POC - AgriSensa",
    page_icon="🧪",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

# Header
st.title("🧪 Kalkulator Pupuk Organik Cair (POC)")
st.markdown("""
<div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 25px;">
    <h3 style="margin:0; color: white;">POC Formulator Pro</h3>
    <p style="margin:0; opacity: 0.9;">Hitung kandungan hara (N, P, K, C-Organik) dari berbagai bahan organik untuk 100 Liter POC</p>
</div>
""", unsafe_allow_html=True)

# Material Database with Nutrient Content
MATERIALS = {
    "Urine": {
        "Urine Sapi": {"N": 0.5, "P": 0.1, "K": 0.4, "C": 0.2, "unit": "liter", "price": 0},
        "Urine Kambing": {"N": 1.5, "P": 0.3, "K": 2.0, "C": 0.3, "unit": "liter", "price": 0},
        "Urine Kelinci": {"N": 2.5, "P": 0.5, "K": 1.2, "C": 0.4, "unit": "liter", "price": 0},
    },
    "Bahan Fermentasi": {
        "Sabut Kelapa (fermentasi)": {"N": 0.8, "P": 0.2, "K": 1.5, "C": 45, "unit": "kg", "price": 2000},
        "Debog Pisang (cacahan)": {"N": 0.3, "P": 0.1, "K": 3.5, "C": 35, "unit": "kg", "price": 1000},
        "Kulit Pisang (cacahan)": {"N": 0.5, "P": 0.2, "K": 4.0, "C": 40, "unit": "kg", "price": 1500},
        "Bonggol Pisang": {"N": 0.4, "P": 0.15, "K": 5.0, "C": 38, "unit": "kg", "price": 1000},
        "Daun Kelor": {"N": 2.5, "P": 0.4, "K": 1.5, "C": 42, "unit": "kg", "price": 3000},
    },
    "Tambahan": {
        "Molase (Tetes Tebu)": {"N": 0.1, "P": 0.05, "K": 3.0, "C": 55, "unit": "liter", "price": 15000},
        "Dekomposer (EM4/MOL)": {"N": 0, "P": 0, "K": 0, "C": 0, "unit": "liter", "price": 25000},
    }
}

# Recipe Templates
TEMPLATES = {
    "Custom (Manual)": {},
    "High N (Vegetatif)": {
        "Urine Kelinci": 20,
        "Daun Kelor": 5,
        "Molase (Tetes Tebu)": 1.5,
        "Dekomposer (EM4/MOL)": 0.5
    },
    "High K (Generatif)": {
        "Bonggol Pisang": 8,
        "Kulit Pisang (cacahan)": 5,
        "Urine Kambing": 15,
        "Molase (Tetes Tebu)": 2,
        "Dekomposer (EM4/MOL)": 0.5
    },
    "Balanced NPK": {
        "Urine Sapi": 20,
        "Sabut Kelapa (fermentasi)": 5,
        "Debog Pisang (cacahan)": 5,
        "Daun Kelor": 3,
        "Molase (Tetes Tebu)": 1.5,
        "Dekomposer (EM4/MOL)": 0.75
    }
}

# Sidebar - Recipe Selection & Inputs
with st.sidebar:
    st.header("⚙️ Konfigurasi Resep")
    
    # Template selection
    template = st.selectbox("Pilih Template Resep", list(TEMPLATES.keys()))
    
    st.divider()
    st.subheader("📊 Target Volume")
    target_volume = st.number_input("Volume POC (Liter)", value=100, min_value=10, max_value=1000, step=10)
    
    # Water price input
    water_price = st.number_input("Harga Air Bersih (Rp/Liter)", value=0, min_value=0, step=10, 
                                   help="Opsional: Input biaya air bersih jika ada")
    
    st.divider()
    st.subheader("🧪 Komposisi Bahan")
    
    # Initialize inputs and prices
    inputs = {}
    custom_prices = {}
    
    # Load template if selected
    if template != "Custom (Manual)":
        st.info(f"📋 Template: **{template}**")
        for material, qty in TEMPLATES[template].items():
            inputs[material] = qty
    
    # Input for each category
    for category, materials in MATERIALS.items():
        with st.expander(f"**{category}**", expanded=(template == "Custom (Manual)")):
            for material, props in materials.items():
                # Get default value from template or 0
                default_val = inputs.get(material, 0.0)
                
                # Create two columns for quantity and price
                col_qty, col_price = st.columns([2, 1])
                
                with col_qty:
                    qty = st.number_input(
                        f"{material} ({props['unit']})",
                        value=float(default_val),
                        min_value=0.0,
                        step=0.5,
                        key=f"qty_{material}"
                    )
                
                with col_price:
                    price = st.number_input(
                        f"Harga/{props['unit']}",
                        value=props['price'],
                        min_value=0,
                        step=100,
                        key=f"price_{material}",
                        help=f"Default: Rp {props['price']:,}"
                    )
                
                if qty > 0:
                    inputs[material] = qty
                    custom_prices[material] = price

# Main Content
if inputs:
    # Calculate total nutrients
    total_N = 0
    total_P = 0
    total_K = 0
    total_C = 0
    total_cost = 0
    total_solid = 0
    total_liquid = 0
    
    material_breakdown = []
    
    for material, qty in inputs.items():
        # Find material props
        props = None
        for cat_materials in MATERIALS.values():
            if material in cat_materials:
                props = cat_materials[material]
                break
        
        if props:
            # Calculate nutrients
            n_contrib = (qty * props['N']) / 100
            p_contrib = (qty * props['P']) / 100
            k_contrib = (qty * props['K']) / 100
            c_contrib = (qty * props['C']) / 100
            
            # Use custom price if available, otherwise use default
            material_price = custom_prices.get(material, props['price'])
            cost = qty * material_price
            
            total_N += n_contrib
            total_P += p_contrib
            total_K += k_contrib
            total_C += c_contrib
            total_cost += cost
            
            if props['unit'] == 'kg':
                total_solid += qty
            else:
                total_liquid += qty
            
            material_breakdown.append({
                "Bahan": material,
                "Jumlah": f"{qty} {props['unit']}",
                "Harga Satuan": f"Rp {material_price:,.0f}",
                "N (%)": f"{props['N']}",
                "P (%)": f"{props['P']}",
                "K (%)": f"{props['K']}",
                "Kontribusi N": f"{n_contrib:.2f} unit",
                "Kontribusi P": f"{p_contrib:.2f} unit",
                "Kontribusi K": f"{k_contrib:.2f} unit",
                "Biaya": f"Rp {cost:,.0f}"
            })
    
    # Calculate concentrations per 100L
    n_pct = (total_N / target_volume) * 100
    p_pct = (total_P / target_volume) * 100
    k_pct = (total_K / target_volume) * 100
    c_pct = (total_C / target_volume) * 100
    
    # Calculate C/N ratio
    cn_ratio = (total_C / total_N) if total_N > 0 else 0
    
    # Water needed and cost
    water_needed = target_volume - total_liquid
    water_cost = water_needed * water_price
    total_cost_with_water = total_cost + water_cost
    
    # Display Results
    st.markdown("## 📊 Hasil Analisis POC")
    
    # Summary Metrics - Row 1: NPK + C-Organic
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Nitrogen (N)", f"{n_pct:.2f}%", help="Kandungan Nitrogen total")
    
    with col2:
        st.metric("Fosfor (P)", f"{p_pct:.2f}%", help="Kandungan Fosfor total")
    
    with col3:
        st.metric("Kalium (K)", f"{k_pct:.2f}%", help="Kandungan Kalium total")
    
    with col4:
        st.metric("C-Organik", f"{c_pct:.1f}%", help="Kandungan Karbon Organik")
    
    # Summary Metrics - Row 2: Water + Cost
    st.markdown("---")
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.metric("Air Bersih Dibutuhkan", f"{water_needed:.1f} L", 
                 help=f"Air untuk mencapai volume {target_volume} L")
    
    with col6:
        st.metric("Biaya Air", f"Rp {water_cost:,.0f}", 
                 help=f"{water_needed:.1f} L x Rp {water_price:,.0f}/L")
    
    with col7:
        st.metric("Biaya Bahan", f"Rp {total_cost:,.0f}", 
                 help="Total biaya semua bahan organik")
    
    with col8:
        st.metric("Total Biaya POC", f"Rp {total_cost_with_water:,.0f}", 
                 delta=f"Rp {total_cost_with_water/target_volume:.0f}/L",
                 help="Biaya bahan + air per liter POC")
    
    # NPK Ratio & C/N Ratio
    st.markdown("---")
    col_r1, col_r2, col_r3 = st.columns(3)
    
    with col_r1:
        # Calculate NPK ratio
        if total_N > 0 and total_P > 0 and total_K > 0:
            min_val = min(total_N, total_P, total_K)
            ratio_n = total_N / min_val
            ratio_p = total_P / min_val
            ratio_k = total_K / min_val
            st.metric("Rasio NPK", f"{ratio_n:.1f} : {ratio_p:.1f} : {ratio_k:.1f}")
        else:
            st.metric("Rasio NPK", "N/A")
    
    with col_r2:
        st.metric("Rasio C/N", f"{cn_ratio:.1f}", 
                 delta="Optimal" if 25 <= cn_ratio <= 30 else "Perlu Penyesuaian",
                 help="Rasio C/N optimal: 25-30")
    
    with col_r3:
        st.metric("Total Biaya", f"Rp {total_cost:,.0f}")
    
    # Visualizations
    st.markdown("---")
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        st.subheader("📈 Kandungan Hara (NPK)")
        fig_npk = go.Figure(data=[
            go.Bar(name='N', x=['Nitrogen'], y=[n_pct], marker_color='#10b981'),
            go.Bar(name='P', x=['Fosfor'], y=[p_pct], marker_color='#f59e0b'),
            go.Bar(name='K', x=['Kalium'], y=[k_pct], marker_color='#3b82f6')
        ])
        fig_npk.update_layout(height=300, showlegend=True, yaxis_title="Konsentrasi (%)")
        st.plotly_chart(fig_npk, use_container_width=True)
    
    with col_v2:
        st.subheader("🥧 Komposisi Bahan")
        # Pie chart of material quantities
        materials_for_pie = []
        quantities_for_pie = []
        for material, qty in inputs.items():
            materials_for_pie.append(material[:20])  # Truncate long names
            quantities_for_pie.append(qty)
        
        fig_pie = go.Figure(data=[go.Pie(labels=materials_for_pie, values=quantities_for_pie)])
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Material Breakdown Table
    st.markdown("---")
    st.subheader("📋 Rincian Bahan & Kontribusi Hara")
    df_breakdown = pd.DataFrame(material_breakdown)
    st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
    
    # Mixing Instructions
    st.markdown("---")
    st.subheader("🔬 Instruksi Pembuatan POC")
    
    col_i1, col_i2 = st.columns(2)
    
    with col_i1:
        st.markdown("**📝 Langkah-langkah:**")
        st.markdown(f"""
        1. **Siapkan wadah** berkapasitas minimal {target_volume + 20} liter
        2. **Masukkan bahan padat** ({total_solid:.1f} kg) yang sudah dicacah halus
        3. **Tambahkan urine** ({total_liquid:.1f} liter) jika ada
        4. **Tambahkan molase** untuk sumber energi mikroba
        5. **Masukkan dekomposer** (EM4/MOL) sebagai starter
        6. **Tambahkan air bersih** sebanyak {water_needed:.1f} liter
        7. **Aduk rata** dan tutup rapat (beri lubang udara kecil)
        8. **Fermentasi** selama 14-21 hari
        9. **Aduk setiap 3 hari** untuk aerasi
        10. **POC siap** saat bau tidak menyengat dan berwarna coklat kehitaman
        """)
    
    with col_i2:
        st.markdown("**⏱️ Timeline Fermentasi:**")
        
        # Fermentation timeline
        today = datetime.now()
        timeline_data = [
            {"Hari": "0", "Aktivitas": "Pencampuran bahan", "Tanggal": today.strftime("%d %b")},
            {"Hari": "3", "Aktivitas": "Pengadukan pertama", "Tanggal": (today + timedelta(days=3)).strftime("%d %b")},
            {"Hari": "7", "Aktivitas": "Pengadukan kedua", "Tanggal": (today + timedelta(days=7)).strftime("%d %b")},
            {"Hari": "14", "Aktivitas": "Cek kematangan (minimal)", "Tanggal": (today + timedelta(days=14)).strftime("%d %b")},
            {"Hari": "21", "Aktivitas": "POC siap panen (optimal)", "Tanggal": (today + timedelta(days=21)).strftime("%d %b")},
        ]
        df_timeline = pd.DataFrame(timeline_data)
        st.dataframe(df_timeline, use_container_width=True, hide_index=True)
        
        st.markdown(f"""
        **🌡️ Kondisi Optimal:**
        - Suhu: 25-35°C
        - pH target: 6.5-7.5
        - Kelembaban: 60-70%
        """)
    
    # Application Guide
    st.markdown("---")
    st.subheader("💧 Panduan Aplikasi")
    
    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        st.markdown("**🌱 Fase Vegetatif:**")
        st.info(f"""
        - Pengenceran: 1 : 10 (POC : Air)
        - Dosis: 500 ml POC + 5 L air
        - Frekuensi: 1x per minggu
        - Aplikasi: Siram ke tanah/semprot daun
        """)
    
    with col_a2:
        st.markdown("**🌸 Fase Generatif:**")
        st.info(f"""
        - Pengenceran: 1 : 8 (POC : Air)
        - Dosis: 500 ml POC + 4 L air
        - Frekuensi: 2x per minggu
        - Aplikasi: Siram ke tanah
        """)
    
    with col_a3:
        st.markdown("**🌾 Fase Pemeliharaan:**")
        st.info(f"""
        - Pengenceran: 1 : 15 (POC : Air)
        - Dosis: 500 ml POC + 7.5 L air
        - Frekuensi: 1x per 2 minggu
        - Aplikasi: Siram ke tanah
        """)
    
    # Quality Indicators
    st.markdown("---")
    st.subheader("✅ Indikator Kualitas POC")
    
    quality_score = 0
    quality_notes = []
    
    # Check C/N ratio
    if 25 <= cn_ratio <= 30:
        quality_score += 25
        quality_notes.append("✅ Rasio C/N optimal (25-30)")
    else:
        quality_notes.append(f"⚠️ Rasio C/N {cn_ratio:.1f} (optimal: 25-30)")
    
    # Check NPK balance
    if 0.5 <= ratio_n <= 3 and 0.5 <= ratio_p <= 2 and 0.5 <= ratio_k <= 4:
        quality_score += 25
        quality_notes.append("✅ Rasio NPK seimbang")
    else:
        quality_notes.append("⚠️ Rasio NPK perlu penyesuaian")
    
    # Check total nutrients
    total_npk = n_pct + p_pct + k_pct
    if total_npk >= 2:
        quality_score += 25
        quality_notes.append(f"✅ Total NPK mencukupi ({total_npk:.2f}%)")
    else:
        quality_notes.append(f"⚠️ Total NPK rendah ({total_npk:.2f}%)")
    
    # Check C-Organic
    if c_pct >= 10:
        quality_score += 25
        quality_notes.append(f"✅ C-Organik tinggi ({c_pct:.1f}%)")
    else:
        quality_notes.append(f"⚠️ C-Organik rendah ({c_pct:.1f}%)")
    
    col_q1, col_q2 = st.columns([1, 2])
    
    with col_q1:
        st.metric("Skor Kualitas", f"{quality_score}/100", 
                 delta="Excellent" if quality_score >= 75 else "Good" if quality_score >= 50 else "Needs Improvement")
    
    with col_q2:
        for note in quality_notes:
            st.markdown(note)

else:
    st.info("👈 Silakan pilih template atau input bahan di sidebar untuk mulai menghitung POC")

# Footer
st.markdown("---")
st.caption("💡 **Tips:** POC terbaik menggunakan kombinasi bahan dengan rasio C/N optimal (25-30) dan NPK seimbang sesuai kebutuhan tanaman.")
