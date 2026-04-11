"""
 Mekanisasi & Alsintan - Agricultural Machinery
Calculator for machine capacity, cost analysis (Buy vs Rent), and maintenance guide
"""

import streamlit as st
import pandas as pd
import altair as alt

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
    from design_system import apply_design_system, icon, COLORS

st.set_page_config(page_title="Mekanisasi", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('tractor', size='lg')} Mekanisasi</h1>", unsafe_allow_html=True)
st.markdown("**Manajemen Alat Mesin Pertanian (Traktor, Transplanter, Combine Harvester)**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs(["⏱ Kalkulator Kapasitas", " Analisis Sewa vs Beli", " Perawatan Mesin"])

with tab1:
    st.header("⏱ Kalkulator Kapasitas Kerja")
    st.write("Hitung berapa lama waktu yang dibutuhkan untuk mengolah lahan.")
    
    col_cap1, col_cap2 = st.columns(2)
    
    with col_cap1:
        jenis_alsintan = st.selectbox("Jenis Alsintan", [
            "Traktor Roda 2 (Hand Tractor)",
            "Traktor Roda 4",
            "Rice Transplanter (Tanam)",
            "Combine Harvester (Panen Besar)",
            "Mini Combine (Panen Kecil)"
        ])
        
        luas_lahan_ha = st.number_input("Luas Lahan (Hektar)", min_value=0.1, value=1.0, step=0.1)
        
        # Default speeds based on machine type
        defaults = {
            "Traktor Roda 2 (Hand Tractor)": {"w": 0.6, "v": 2.5, "eff": 70}, # 60cm width, 2.5 km/h
            "Traktor Roda 4": {"w": 2.0, "v": 4.0, "eff": 80},
            "Rice Transplanter (Tanam)": {"w": 1.2, "v": 2.0, "eff": 60}, # 4 rows x 30cm
            "Combine Harvester (Panen Besar)": {"w": 2.5, "v": 3.5, "eff": 75},
            "Mini Combine (Panen Kecil)": {"w": 1.2, "v": 2.5, "eff": 70}
        }
        
        machine = defaults[jenis_alsintan]
        
        lebar_kerja = st.number_input("Lebar Kerja (meter)", value=machine["w"], step=0.1)
        kecepatan = st.number_input("Kecepatan Maju (km/jam)", value=machine["v"], step=0.5)
        efisiensi = st.slider("Efisiensi Lapangan (%)", 50, 100, machine["eff"])
        
    with col_cap2:
        # Theoretical Capacity (Kt) = 0.1 * W * V
        kt = 0.1 * lebar_kerja * kecepatan # Ha/Jam
        
        # Effective Capacity (Ke) = Kt * eff/100
        ke = kt * (efisiensi / 100)
        
        # Total Hours
        total_jam = luas_lahan_ha / ke if ke > 0 else 0
        
        st.subheader("Hasil Perhitungan:")
        st.metric("Kapasitas Kerja Efektif", f"{ke:.2f} Ha/Jam")
        
        if total_jam < 8:
            durasi_str = f"{total_jam:.1f} Jam ({total_jam*60:.0f} Menit)"
            st.success(f"⏱ Estimasi Waktu: **{durasi_str}** (Selesai dalam 1 hari)")
        else:
            hari_kerja = total_jam / 8
            st.warning(f"⏱ Estimasi Waktu: **{total_jam:.1f} Jam** (Sekitar {hari_kerja:.1f} hari kerja)")

        # Solar Consumption
        konsumsi_per_jam = 1.5 if "Roda 2" in jenis_alsintan or "Mini" in jenis_alsintan else 5.0
        konsumsi_per_jam = st.number_input("Konsumsi BBM (Liter/Jam)", value=konsumsi_per_jam)
        total_bbm = total_jam * konsumsi_per_jam
        
        st.info(f" Estimasi BBM: **{total_bbm:.1f} Liter**")

with tab2:
    st.header(" Analisis: Beli Sendiri atau Sewa?")
    st.markdown("Analisis Titik Impas (Break Even Point) kepemilikan alsintan.")
    
    col_buy1, col_buy2 = st.columns(2)
    
    with col_buy1:
        harga_mesin = st.number_input("Harga Beli Mesin (Rp)", min_value=10000000, value=30000000, step=1000000, format="%d")
        umur_ekonomis = st.number_input("Umur Ekonomis (Tahun)", value=5)
        biaya_perawatan_thn = st.number_input("Biaya Perawatan/Tahun (Rp)", value=2000000)
        
    with col_buy2:
        harga_sewa = st.number_input("Harga Sewa UPJA per Ha (Rp)", value=1500000)
        biaya_ops_sendiri = st.number_input("Biaya Operasional Sendiri per Ha (Rp)", value=800000, help="BBM + Operator")
        
    # Calculation
    # Fixed Cost / Year = Depreciation + Interest (simplified to Depreciation + Maintenance)
    penyusutan = harga_mesin / umur_ekonomis
    biaya_tetap_thn = penyusutan + biaya_perawatan_thn
    
    # Margin per Ha (Saving)
    margin_per_ha = harga_sewa - biaya_ops_sendiri
    
    # BEP (Luas)
    if margin_per_ha > 0:
        bep_luas = biaya_tetap_thn / margin_per_ha
        
        st.markdown("###  Hasil Analisis")
        st.metric("Minimum Luas Garapan per Tahun", f"{bep_luas:.1f} Hektar")
        
        st.info(f"""
        Agar untung membeli mesin ini, Anda harus menggarap minimal **{bep_luas:.1f} Hektar** per tahun. 
        (Bisa lahan sendiri atau membuka jasa sewa ke tetangga).
        """)
        
        # Scenario
        luas_rencana = st.slider("Rencana Luas Garapan Tahunan (Ha)", 1, 50, int(bep_luas)+5)
        
        keuntungan = (margin_per_ha * luas_rencana) - biaya_tetap_thn
        
        if keuntungan > 0:
            st.success(f" Untung Bersih: **Rp {keuntungan:,.0f} / tahun**")
        else:
            st.error(f" Rugi: **Rp {abs(keuntungan):,.0f} / tahun** (Sebaiknya sewa saja)")
    else:
        st.error("Biaya operasional sendiri lebih mahal dari harga sewa. Tidak layak beli!")

with tab3:
    st.header(" checklist Perawatan Berkala")
    st.write("Pilih jenis mesin untuk melihat jadwal maintenance.")
    
    tipe_mesin = st.selectbox("Pilih Mesin", ["Traktor Roda 2", "Traktor Roda 4", "Combine Harvester"])
    
    maintenance_data = {
        "Harian (Sebelum Start)": [
            "Cek level oli mesin",
            "Cek air radiator (coolant)",
            "Cek bahan bakar",
            "Cek kekencangan baut roda/track",
            "Bersihkan saringan udara (Air Filter)"
        ],
        "50 Jam Kerja": [
            "Ganti oli mesin (Periode Inreyen)",
            "Bersihkan filter bahan bakar",
            "Cek ketegangan V-belt",
            "Lumasi grease nipple (gemuk)"
        ],
        "200 Jam Kerja": [
            "Ganti oli mesin rutin",
            "Ganti filter oli",
            "Ganti filter bahan bakar",
            "Ganti oli transmisi/gardan"
        ],
        "600 Jam Kerja / 1 Musim": [
            "Kuras tangki solar",
            "Ganti air radiator (flushing)",
            "Cek nozzle injektor",
            "Servis dinamo starter & ampere"
        ]
    }
    
    for periode, items in maintenance_data.items():
        with st.expander(f" {periode}"):
            for item in items:
                st.checkbox(item, key=f"{tipe_mesin}_{periode}_{item}")

st.markdown("---")
st.caption(" **Tip:** Mesin yang terawat akan memiliki harga jual kembali (Resale Value) yang tinggi.")
