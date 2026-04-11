"""
 Strategi Penyemprotan - Spraying Strategy
Technical guide for pesticide application, dose calculator, and resistance management
"""

import streamlit as st
import pandas as pd

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

st.set_page_config(page_title="Strategi Semprot", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('spray-can', size='lg')} Strategi Semprot</h1>", unsafe_allow_html=True)
st.markdown("**Panduan teknis aplikasi pestisida, kalkulator dosis, dan manajemen resistensi**")
st.markdown("---")

tab1, tab2, tab3 = st.tabs([" Strategi per Hama", " Kalkulator Dosis", " Rotasi Bahan Aktif"])

with tab1:
    st.header(" Taktik Penyemprotan per Target")
    st.info(" Beda hama, beda cara semprotnya. Jangan asal 'mandiin' tanaman!")
    
    pest_strategies = {
        "Wereng Coklat": {
            "target": "Pangkal Batang (Bawah)",
            "waktu": "Pagi (07.00-09.00) atau Sore",
            "nozzle": "Cone (Kabut Halus)",
            "taktik": "Singkap/buka tajuk tanaman agar semprotan menembus ke pangkal batang. Gunakan air volume tinggi (500L/ha).",
            "bahan_aktif": "Imidakloprid, Buprofezin, Pimetrozin"
        },
        "Penggerek Batang (Sundep/Beluk)": {
            "target": "Seluruh Daun & Batang",
            "waktu": "Fase vegetatif awal atau saat penerbangan ngengat",
            "nozzle": "Flat Fan (Kipas) atau Cone",
            "taktik": "Gunakan sistemik agar masuk jaringan. Semprot sebelum ulat masuk ke dalam batang.",
            "bahan_aktif": "Fipronil, Klorantraniliprol, Dimehipo"
        },
        "Walang Sangit": {
            "target": "Malai/Bulir Padi",
            "waktu": "Pagi sekali (sebelum jam 9) atau Sore (setelah jam 16)",
            "nozzle": "Cone (Kabut)",
            "taktik": "Semprot melambung di atas tanaman. Lakukan saat hama aktif makan di bulir.",
            "bahan_aktif": "Sipermetrin, Deltametrin, BPMC"
        },
        "Tikus": {
            "target": "Lubang Aktif / Jalur Jalan",
            "waktu": "Sore hari sebelum malam",
            "nozzle": "-",
            "taktik": "Bukan disemprot! Gunakan umpan racun di jalur aktif atau pengemposan (asap belerang) di lubang aktif.",
            "bahan_aktif": "Brodifakum (Umpan), Belerang (Empos)"
        },
        "Wereng Hijau": {
            "target": "Daun & Batang Bagian Atas",
            "waktu": "Pagi/Sore",
            "nozzle": "Cone",
            "taktik": "Kendalikan segera karena vektor Tungro. Semprot merata.",
            "bahan_aktif": "Imidakloprid, Tiametoksam"
        },
        "Lalat Bibit": {
            "target": "Persemaian / Tanaman Muda",
            "waktu": "Pagi hari",
            "nozzle": "Cone",
            "taktik": "Lindungi persemaian. Basahi daun merata.",
            "bahan_aktif": "Fipronil, Karbofuran (Tabur)"
        },
        "Kepik Bergaris (Hispa)": {
            "target": "Permukaan Daun",
            "waktu": "Pagi hari",
            "nozzle": "Flat Fan",
            "taktik": "Pastikan daun terbasahi sempurna. Hama ini memakan jaringan daun.",
            "bahan_aktif": "Klorpirifos, Sipermetrin"
        },
        "Ulat Kantong": {
            "target": "Daun & Permukaan Air",
            "waktu": "Sore hari",
            "nozzle": "Cone",
            "taktik": "Buang air sawah dahulu agar ulat tidak mengapung/lari, lalu semprot tanaman dan tanah.",
            "bahan_aktif": "Klorpirifos, Sipermetrin"
        }
    }
    
    selected_pest = st.selectbox("Pilih Target Hama:", list(pest_strategies.keys()))
    strategy = pest_strategies[selected_pest]
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.markdown(f"###  Target: {strategy['target']}")
        st.markdown(f"**⏰ Waktu Terbaik:** {strategy['waktu']}")
        st.markdown(f"** Jenis Nozzle:** {strategy['nozzle']}")
    
    with col_s2:
        st.success(f"** Taktik Jitu:** {strategy['taktik']}")
        st.warning(f"** Bahan Aktif Rekomendasi:** {strategy['bahan_aktif']}")

with tab2:
    st.header(" Kalkulator Dosis & Tangki")
    st.write("Hitung berapa sendok/tutup yang harus dimasukkan ke dalam tangki.")
    
    col_calc1, col_calc2 = st.columns(2)
    
    with col_calc1:
        # Input
        dosis_label = st.selectbox("Satuan Dosis di Kemasan", ["ml/liter (Cair)", "gram/liter (Tepung)"])
        dosis_per_liter = st.number_input(f"Dosis ({dosis_label})", min_value=0.1, value=1.0, step=0.1)
        volume_tangki = st.selectbox("Ukuran Tangki", [16, 14, 20, 10, "Custom"])
        
        if volume_tangki == "Custom":
            volume_tangki = st.number_input("Volume Tangki Sendiri (Liter)", min_value=1, value=16)
            
    with col_calc2:
        # Calculation
        kebutuhan_per_tangki = dosis_per_liter * volume_tangki
        
        unit = "ml" if "Cair" in dosis_label else "gram"
        alat_takar = "Tutup Botol (rata-rata 10-15ml)" if unit == "ml" else "Sendok Makan (rata-rata 10-15g)"
        
        st.subheader("Hasil Perhitungan:")
        st.metric(f"Dosis Per Tangki ({volume_tangki}L)", f"{kebutuhan_per_tangki:.1f} {unit}")
        
        st.info(f" Kira-kira setara dengan **{kebutuhan_per_tangki/15:.1f} - {kebutuhan_per_tangki/10:.1f} {alat_takar}**")
        st.caption("*Pastikan kalibrasi alat takar Anda sendiri untuk akurasi maksimal*")

with tab3:
    st.header(" Manajemen Resistensi (Rotasi Racun)")
    st.error(" **BAHAYA:** Jangan gunakan bahan aktif yang sama terus menerus! Hama akan kebal.")
    
    rotation_cols = st.columns(3)
    
    with rotation_cols[0]:
        st.markdown("### 🟢 Minggu 1-2")
        st.write("**Cara Kerja A (Saraf)**")
        st.write("- Piretroid (Sipermetrin)")
        st.write("- Karbamat (BPMC)")
        st.write("*Efek: Knockdown cepat*")
        
    with rotation_cols[1]:
        st.markdown("### 🟡 Minggu 3-4")
        st.write("**Cara Kerja B (Pertumbuhan)**")
        st.write("- IGR (Buprofezin)")
        st.write("- Penghambat Kitin")
        st.write("*Efek: Hama gagal ganti kulit*")
        
    with rotation_cols[2]:
        st.markdown("###  Minggu 5-6")
        st.write("**Cara Kerja C (Energi/Perut)**")
        st.write("- Fipronil")
        st.write("- Klorfenapir")
        st.write("*Efek: Hama lemas & mati perlahan*")
        
    st.markdown("---")
    st.write("**Tips:** Cek Kode MoA (Mode of Action) pada kemasan pestisida. Rotasi berdasarkan **KODE ANGKA**, bukan merek dagang!")

st.markdown("---")
st.warning(" **Safety First:** Selalu gunakan masker, sarung tangan, dan baju lengan panjang saat menyemprot.")
