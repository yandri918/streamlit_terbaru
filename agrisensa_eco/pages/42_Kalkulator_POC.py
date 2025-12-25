import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Kalkulator POC - AgriSensa",
    page_icon="🧪",
    layout="wide"
)

user = require_auth()
show_user_info_sidebar()

st.title("🧪 Kalkulator Pupuk Organik Cair (POC)")
st.markdown("""
<div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 20px; border-radius: 15px; color: white; margin-bottom: 25px;">
    <h3 style="margin:0; color: white;">POC Formulator Pro</h3>
    <p style="margin:0; opacity: 0.9;">Hitung kandungan hara (N, P, K, C-Organik) dari berbagai bahan organik untuk 100 Liter POC</p>
</div>
""", unsafe_allow_html=True)

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

with st.sidebar:
    st.header("⚙️ Konfigurasi Resep")
    template = st.selectbox("Pilih Template Resep", list(TEMPLATES.keys()))
    st.divider()
    st.subheader("📊 Target Volume")
    target_volume = st.number_input("Volume POC (Liter)", value=100, min_value=10, max_value=1000, step=10)
    st.divider()
    st.subheader("🧪 Komposisi Bahan")
    inputs = {}
    if template != "Custom (Manual)":
        st.info(f"📋 Template: **{template}**")
        for material, qty in TEMPLATES[template].items():
            inputs[material] = qty
    for category, materials in MATERIALS.items():
        with st.expander(f"**{category}**", expanded=(template == "Custom (Manual)")):
            for material, props in materials.items():
                default_val = inputs.get(material, 0.0)
                qty = st.number_input(
                    f"{material} ({props['unit']})",
                    value=float(default_val),
                    min_value=0.0,
                    step=0.5,
                    key=material
                )
                if qty > 0:
                    inputs[material] = qty

if inputs:
    total_N = total_P = total_K = total_C = total_cost = total_solid = total_liquid = 0
    material_breakdown = []
    for material, qty in inputs.items():
        props = None
        for cat_materials in MATERIALS.values():
            if material in cat_materials:
                props = cat_materials[material]
                break
        if props:
            n_contrib = (qty * props['N']) / 100
            p_contrib = (qty * props['P']) / 100
            k_contrib = (qty * props['K']) / 100
            c_contrib = (qty * props['C']) / 100
            cost = qty * props['price']
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
                "N (%)": f"{props['N']}",
                "P (%)": f"{props['P']}",
                "K (%)": f"{props['K']}",
                "Biaya": f"Rp {cost:,.0f}"
            })
    n_pct = (total_N / target_volume) * 100
    p_pct = (total_P / target_volume) * 100
    k_pct = (total_K / target_volume) * 100
    c_pct = (total_C / target_volume) * 100
    cn_ratio = (total_C / total_N) if total_N > 0 else 0
    water_needed = target_volume - total_liquid
    st.markdown("## 📊 Hasil Analisis POC")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Nitrogen (N)", f"{n_pct:.2f}%")
    with col2:
        st.metric("Fosfor (P)", f"{p_pct:.2f}%")
    with col3:
        st.metric("Kalium (K)", f"{k_pct:.2f}%")
    with col4:
        st.metric("C-Organik", f"{c_pct:.1f}%")
    st.markdown("---")
    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
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
                 delta="Optimal" if 25 <= cn_ratio <= 30 else "Perlu Penyesuaian")
    with col_r3:
        st.metric("Total Biaya", f"Rp {total_cost:,.0f}")
    st.markdown("---")
    st.subheader("📋 Rincian Bahan")
    df_breakdown = pd.DataFrame(material_breakdown)
    st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
    st.markdown("---")
    st.subheader("🔬 Instruksi Pembuatan POC")
    st.markdown(f"""
    1. Siapkan wadah berkapasitas minimal {target_volume + 20} liter
    2. Masukkan bahan padat ({total_solid:.1f} kg) yang sudah dicacah halus
    3. Tambahkan urine ({total_liquid:.1f} liter) jika ada
    4. Tambahkan molase untuk sumber energi mikroba
    5. Masukkan dekomposer (EM4/MOL) sebagai starter
    6. Tambahkan air bersih sebanyak {water_needed:.1f} liter
    7. Aduk rata dan tutup rapat (beri lubang udara kecil)
    8. Fermentasi selama 14-21 hari
    9. Aduk setiap 3 hari untuk aerasi
    10. POC siap saat bau tidak menyengat dan berwarna coklat kehitaman
    """)
else:
    st.info("👈 Silakan pilih template atau input bahan di sidebar untuk mulai menghitung POC")

st.markdown("---")
st.caption("💡 **Tips:** POC terbaik menggunakan kombinasi bahan dengan rasio C/N optimal (25-30) dan NPK seimbang sesuai kebutuhan tanaman.")
