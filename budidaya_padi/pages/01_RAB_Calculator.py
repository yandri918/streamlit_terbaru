"""
RAB Calculator - Advanced Rice Cultivation Budget Planning
Comprehensive budget planning with scenario comparison, cash flow, and analytics
"""

import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
from datetime import datetime, timedelta

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from utils.design_system import apply_design_system, icon, COLORS
    from utils.rab_templates import get_all_templates, get_template, REGIONAL_BENCHMARKS, calculate_efficiency_score
except ImportError:
    # Fallback for different directory structures
    sys.path.insert(0, str(Path(__file__).parent.parent / "utils"))
    from design_system import apply_design_system, icon, COLORS
    from rab_templates import get_all_templates, get_template, REGIONAL_BENCHMARKS, calculate_efficiency_score

# Page config
st.set_page_config(
    page_title="RAB Calculator Advanced",
    page_icon="💰",
    layout="wide"
)

# Apply Design System
apply_design_system()

# Header
st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('calculator', size='lg')} RAB Calculator - Advanced</h1>", unsafe_allow_html=True)
st.markdown("**Perencanaan Anggaran Budidaya Padi dengan Analisis Komprehensif**")
st.markdown("---")

# Initialize session state
if 'scenarios' not in st.session_state:
    st.session_state.scenarios = {}
if 'active_scenario' not in st.session_state:
    st.session_state.active_scenario = "Skenario 1"

# Sidebar for scenario management
with st.sidebar:
    st.markdown(f"<h3>{icon('folder')} Manajemen Skenario</h3>", unsafe_allow_html=True)
    
    # Scenario selector
    # Include all existing scenarios plus the active one (in case it's new)
    all_scenario_names = list(st.session_state.scenarios.keys())
    if st.session_state.active_scenario not in all_scenario_names:
        all_scenario_names.append(st.session_state.active_scenario)
    if not all_scenario_names:
        all_scenario_names = ["Skenario 1"]
    
    selected_scenario = st.selectbox("Pilih Skenario", all_scenario_names, 
                                     index=all_scenario_names.index(st.session_state.active_scenario) if st.session_state.active_scenario in all_scenario_names else 0,
                                     key="scenario_selector")
    st.session_state.active_scenario = selected_scenario
    
    st.markdown("---")
    
    # Add new scenario section with better visibility
    st.markdown(f"<h4>{icon('plus-circle')} Buat Skenario Baru</h4>", unsafe_allow_html=True)
    
    # Auto-generate next scenario number as default
    existing_nums = []
    for name in st.session_state.scenarios.keys():
        if name.startswith("Skenario "):
            try:
                num = int(name.split(" ")[1])
                existing_nums.append(num)
            except:
                pass
    next_num = max(existing_nums) + 1 if existing_nums else 1
    
    # Input field for new scenario name
    new_scenario_name = st.text_input(
        "Nama Skenario Baru", 
        value=f"Skenario {next_num}",
        placeholder="Contoh: Organik MT1, Konvensional Lahan A",
        help="Masukkan nama untuk skenario baru, lalu klik tombol Buat",
        key="new_scenario_input"
    )
    
    # Create button
    if st.button("✅ Buat Skenario", use_container_width=True, type="primary", key="create_scenario_btn"):
        if not new_scenario_name or new_scenario_name.strip() == "":
            st.error("❌ Nama skenario tidak boleh kosong!")
        elif new_scenario_name in all_scenario_names:
            st.error(f"❌ Skenario '{new_scenario_name}' sudah ada!")
        else:
            st.session_state.active_scenario = new_scenario_name
            # Clear loaded template so new scenario starts fresh (unless user loads one)
            if 'loaded_template' in st.session_state:
                del st.session_state['loaded_template']
            
            st.success(f"✅ Skenario '{new_scenario_name}' berhasil dibuat!")
            st.rerun()
    
    st.markdown("---")
    
    # Delete scenario button
    if st.button("🗑️ Hapus Skenario Aktif", use_container_width=True, disabled=len(st.session_state.scenarios) <= 1):
        if st.session_state.active_scenario in st.session_state.scenarios:
            del st.session_state.scenarios[st.session_state.active_scenario]
            st.session_state.active_scenario = list(st.session_state.scenarios.keys())[0] if st.session_state.scenarios else "Skenario 1"
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"<h3>{icon('cog')} Mode Input</h3>", unsafe_allow_html=True)
    input_mode = st.radio("", ["Simple", "Detail"], horizontal=True)
    
    # Template loader
    st.markdown("---")
    st.markdown(f"<h3>{icon('bookmark')} Template</h3>", unsafe_allow_html=True)
    templates = get_all_templates()
    template_names = ["-- Pilih Template --"] + list(templates.keys())
    selected_template = st.selectbox("Load Template", template_names, key="template_selector")
    
    if selected_template != "-- Pilih Template --":
        if st.button("📥 Terapkan Template", use_container_width=True):
            tpl = templates[selected_template]
            act = st.session_state.active_scenario
            costs = tpl.get('costs_per_ha', {})
            
            # Direct injection into widget states
            # This forces the UI to update immediately
            st.session_state[f"prod_{act}"] = float(tpl.get('target_produksi', 6.0))
            st.session_state[f"met_{act}"] = tpl.get('metode_tanam', "Transplanting (Pindah Tanam)")
            
            # Cost mappings
            st.session_state[f"olah_{act}"] = int(costs.get('persiapan_lahan', 2000000))
            st.session_state[f"bibit_{act}"] = int(costs.get('bibit', 1500000))
            st.session_state[f"urea_{act}"] = int(costs.get('pupuk_subsidi', 2000000) * 0.4)
            st.session_state[f"npk_{act}"] = int(costs.get('pupuk_subsidi', 2000000) * 0.6)
            st.session_state[f"org_{act}"] = int(costs.get('pupuk_organik', 800000))
            st.session_state[f"pest_{act}"] = int(costs.get('pestisida', 1000000))
            st.session_state[f"herb_{act}"] = 500000 # Default
            st.session_state[f"tanam_{act}"] = int(costs.get('tenaga_kerja', 4000000) * 0.3)
            st.session_state[f"rawat_{act}"] = int(costs.get('tenaga_kerja', 4000000) * 0.3)
            st.session_state[f"panen_{act}"] = int(costs.get('panen_pasca', 3000000))
            st.session_state[f"sewa_{act}"] = int(costs.get('lainnya', 500000))
            st.session_state[f"lain_{act}"] = int(costs.get('lainnya', 500000))
            
            # Clear loaded_template flag if it exists to avoid confusion
            if 'loaded_template' in st.session_state:
                del st.session_state['loaded_template']

            st.success(f"✅ Template '{selected_template}' berhasil diterapkan!")
            st.rerun()


# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Input Data",
    "📊 Hasil RAB",
    "📈 Analisis",
    "💾 Export"
])

# ==================== TAB 1: INPUT DATA ====================
with tab1:
    st.markdown(f"<h3>{icon('seedling')} Skenario: {st.session_state.active_scenario}</h3>", unsafe_allow_html=True)
    
    # Get existing data if scenario already calculated
    existing_data = st.session_state.scenarios.get(st.session_state.active_scenario, {})
    
    if existing_data:
         st.success(f"✅ Data tersimpan (Update terakhir: {existing_data.get('calculated_at', 'N/A')})")
    else:
        st.info("📝 Skenario baru - Silakan isi form atau pilih Template di sidebar")

    # Helper function to get value safely from existing data or return default
    def get_val(key, default):
        if existing_data and key in existing_data:
            return existing_data[key]
        return default
    
    # Basic Information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**📍 Informasi Lahan**")
        luas_lahan = st.number_input("Luas Lahan (ha)", 
                                     min_value=0.1, max_value=100.0, 
                                     value=float(get_val('luas_lahan', 1.0)), 
                                     step=0.1, 
                                     key=f"luas_{st.session_state.active_scenario}")
        
        lokasi_options = ["Jawa Barat", "Jawa Tengah", "Jawa Timur", "Sulawesi Selatan", "Sumatera Utara"]
        default_loc = get_val('lokasi', "Jawa Barat")
        default_lokasi_idx = lokasi_options.index(default_loc) if default_loc in lokasi_options else 0
        lokasi = st.selectbox("Lokasi", lokasi_options, 
                             index=default_lokasi_idx,
                             key=f"lok_{st.session_state.active_scenario}")
    
    with col2:
        st.markdown("**🌾 Varietas & Metode**")
        varietas_options = ["IR64", "Ciherang", "Inpari 32", "Inpari 42", "Inpari 43", "Mekongga", "Memberamo"]
        varietas = st.selectbox("Varietas Padi", 
            varietas_options,
            key=f"var_{st.session_state.active_scenario}")
            # Note: Varietas not currently in template structure
            
        metode_options = [
            "Transplanting (Pindah Tanam)",
            "Direct Seeding (Tabela)",
            "SRI (System of Rice Intensification)",
            "Jajar Legowo 2:1",
            "Jajar Legowo 4:1"
        ]
        default_metode = get_val('metode_tanam', "Transplanting (Pindah Tanam)")
        default_metode_idx = metode_options.index(default_metode) if default_metode in metode_options else 0
        metode_tanam = st.selectbox("Metode Tanam", metode_options, 
                                   index=default_metode_idx,
                                   key=f"met_{st.session_state.active_scenario}")
    
    with col3:
        st.markdown("**🎯 Target & Harga**")
        target_produksi = st.number_input("Target Produksi (ton/ha)", min_value=1.0, max_value=15.0, 
                                          value=float(get_val('target_produksi', 6.0)), step=0.5, 
                                          key=f"prod_{st.session_state.active_scenario}")
        harga_jual = st.number_input("Harga Jual GKP (Rp/kg)", min_value=3000, max_value=10000, 
                                     value=int(get_val('harga_jual', 5500)), step=100, 
                                     key=f"harga_{st.session_state.active_scenario}")
        musim_tanam = st.selectbox("Musim Tanam", ["MT I (Okt-Feb)", "MT II (Mar-Jul)", "MT III (Agu-Nov)"], key=f"musim_{st.session_state.active_scenario}")
    
    st.markdown("---")
    
    # Cost Input - Simple or Detail mode
    if input_mode == "Simple":
        st.markdown(f"<h3>{icon('money')} Rincian Biaya (Mode Simple)</h3>", unsafe_allow_html=True)
        
        col_cost1, col_cost2 = st.columns(2)
        
        # Helper shortcut for current scenario key suffix
        k_suffix = st.session_state.active_scenario
        
        with col_cost1:
            st.markdown("**🌱 Persiapan Lahan & Bibit**")
            biaya_olah_tanah = st.number_input("Olah Tanah (Rp/ha)", value=int(get_val(f'olah_{k_suffix}', 2000000)), step=100000, key=f"olah_{k_suffix}")
            biaya_bibit = st.number_input("Bibit/Benih (Rp/ha)", value=int(get_val(f'bibit_{k_suffix}', 1500000)), step=100000, key=f"bibit_{k_suffix}")
            
            st.markdown("**🧪 Pupuk**")
            biaya_urea = st.number_input("Urea (Rp/ha)", value=int(get_val(f'urea_{k_suffix}', 1200000)), step=50000, key=f"urea_{k_suffix}")
            biaya_npk = st.number_input("NPK/Phonska (Rp/ha)", value=int(get_val(f'npk_{k_suffix}', 1500000)), step=50000, key=f"npk_{k_suffix}")
            biaya_organik = st.number_input("Pupuk Organik (Rp/ha)", value=int(get_val(f'org_{k_suffix}', 800000)), step=50000, key=f"org_{k_suffix}")
        
        with col_cost2:
            st.markdown("**💊 Pestisida & Herbisida**")
            biaya_pestisida = st.number_input("Pestisida (Rp/ha)", value=int(get_val(f'pest_{k_suffix}', 1000000)), step=50000, key=f"pest_{k_suffix}")
            biaya_herbisida = st.number_input("Herbisida (Rp/ha)", value=int(get_val(f'herb_{k_suffix}', 500000)), step=50000, key=f"herb_{k_suffix}")
            
            st.markdown("**👷 Tenaga Kerja**")
            biaya_tanam = st.number_input("Tanam (Rp/ha)", value=int(get_val(f'tanam_{k_suffix}', 2000000)), step=100000, key=f"tanam_{k_suffix}")
            biaya_rawat = st.number_input("Perawatan (Rp/ha)", value=int(get_val(f'rawat_{k_suffix}', 1500000)), step=100000, key=f"rawat_{k_suffix}")
            biaya_panen = st.number_input("Panen (Rp/ha)", value=int(get_val(f'panen_{k_suffix}', 3000000)), step=100000, key=f"panen_{k_suffix}")
            
            st.markdown("**💧 Irigasi & Lainnya**")
            biaya_sewa = st.number_input("Irigasi/Sewa Pompa (Rp/ha)", value=int(get_val(f'sewa_{k_suffix}', 500000)), step=50000, key=f"sewa_{k_suffix}")
            biaya_lain = st.number_input("Lain-lain (Rp/ha)", value=int(get_val(f'lain_{k_suffix}', 500000)), step=50000, key=f"lain_{k_suffix}")
        
        # Aggregate costs
        total_persiapan = biaya_olah_tanah + biaya_bibit
        total_pupuk = biaya_urea + biaya_npk + biaya_organik
        total_pestisida = biaya_pestisida + biaya_herbisida
        total_tenaga_kerja = biaya_tanam + biaya_rawat + biaya_panen
        total_lainnya = biaya_sewa + biaya_lain
        
    else:  # Detail mode
        st.markdown(f"<h3>{icon('list')} Rincian Biaya (Mode Detail)</h3>", unsafe_allow_html=True)
        
        with st.expander("🌱 Persiapan Lahan", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                biaya_bajak = st.number_input("Bajak (Rp/ha)", value=800000, step=50000, key=f"bajak_{st.session_state.active_scenario}")
                biaya_garu = st.number_input("Garu (Rp/ha)", value=600000, step=50000, key=f"garu_{st.session_state.active_scenario}")
            with col2:
                biaya_ratakan = st.number_input("Ratakan (Rp/ha)", value=400000, step=50000, key=f"rata_{st.session_state.active_scenario}")
                biaya_buat_pematang = st.number_input("Buat Pematang (Rp/ha)", value=200000, step=50000, key=f"pematang_{st.session_state.active_scenario}")
            total_persiapan = biaya_bajak + biaya_garu + biaya_ratakan + biaya_buat_pematang
        
        with st.expander("🌾 Bibit & Persemaian"):
            col1, col2 = st.columns(2)
            with col1:
                biaya_benih = st.number_input("Benih (Rp/ha)", value=800000, step=50000, key=f"benih_{st.session_state.active_scenario}")
                biaya_persemaian = st.number_input("Persemaian (Rp/ha)", value=400000, step=50000, key=f"semai_{st.session_state.active_scenario}")
            with col2:
                biaya_cabut_bibit = st.number_input("Cabut Bibit (Rp/ha)", value=300000, step=50000, key=f"cabut_{st.session_state.active_scenario}")
        
        with st.expander("🧪 Pupuk (Per Aplikasi)"):
            st.markdown("**Pemupukan Dasar**")
            col1, col2, col3 = st.columns(3)
            with col1:
                pupuk_dasar_urea = st.number_input("Urea Dasar (Rp/ha)", value=300000, step=50000, key=f"urea_d_{st.session_state.active_scenario}")
            with col2:
                pupuk_dasar_npk = st.number_input("NPK Dasar (Rp/ha)", value=500000, step=50000, key=f"npk_d_{st.session_state.active_scenario}")
            with col3:
                pupuk_dasar_organik = st.number_input("Organik Dasar (Rp/ha)", value=800000, step=50000, key=f"org_d_{st.session_state.active_scenario}")
            
            st.markdown("**Pemupukan Susulan**")
            col1, col2 = st.columns(2)
            with col1:
                pupuk_susulan1 = st.number_input("Susulan 1 (Rp/ha)", value=400000, step=50000, key=f"sus1_{st.session_state.active_scenario}")
                pupuk_susulan2 = st.number_input("Susulan 2 (Rp/ha)", value=400000, step=50000, key=f"sus2_{st.session_state.active_scenario}")
            with col2:
                pupuk_susulan3 = st.number_input("Susulan 3 (Rp/ha)", value=400000, step=50000, key=f"sus3_{st.session_state.active_scenario}")
            
            total_pupuk = pupuk_dasar_urea + pupuk_dasar_npk + pupuk_dasar_organik + pupuk_susulan1 + pupuk_susulan2 + pupuk_susulan3
        
        with st.expander("💊 Pestisida & Herbisida"):
            col1, col2 = st.columns(2)
            with col1:
                biaya_insektisida = st.number_input("Insektisida (Rp/ha)", value=600000, step=50000, key=f"insek_{st.session_state.active_scenario}")
                biaya_fungisida = st.number_input("Fungisida (Rp/ha)", value=400000, step=50000, key=f"fungi_{st.session_state.active_scenario}")
            with col2:
                biaya_herbisida_detail = st.number_input("Herbisida (Rp/ha)", value=500000, step=50000, key=f"herb_d_{st.session_state.active_scenario}")
            total_pestisida = biaya_insektisida + biaya_fungisida + biaya_herbisida_detail
        
        with st.expander("👷 Tenaga Kerja"):
            col1, col2 = st.columns(2)
            with col1:
                tk_tanam = st.number_input("Tanam (Rp/ha)", value=2000000, step=100000, key=f"tk_tanam_{st.session_state.active_scenario}")
                tk_penyiangan = st.number_input("Penyiangan (Rp/ha)", value=800000, step=50000, key=f"tk_siang_{st.session_state.active_scenario}")
                tk_pemupukan = st.number_input("Pemupukan (Rp/ha)", value=400000, step=50000, key=f"tk_pupuk_{st.session_state.active_scenario}")
            with col2:
                tk_penyemprotan = st.number_input("Penyemprotan (Rp/ha)", value=300000, step=50000, key=f"tk_semprot_{st.session_state.active_scenario}")
                tk_panen = st.number_input("Panen (Rp/ha)", value=2000000, step=100000, key=f"tk_panen_{st.session_state.active_scenario}")
                tk_pasca_panen = st.number_input("Pasca Panen (Rp/ha)", value=1000000, step=100000, key=f"tk_pasca_{st.session_state.active_scenario}")
            total_tenaga_kerja = tk_tanam + tk_penyiangan + tk_pemupukan + tk_penyemprotan + tk_panen + tk_pasca_panen
        
        with st.expander("💧 Irigasi & Lain-lain"):
            col1, col2 = st.columns(2)
            with col1:
                biaya_irigasi = st.number_input("Irigasi/Air (Rp/ha)", value=500000, step=50000, key=f"irigasi_{st.session_state.active_scenario}")
                biaya_sewa_alat = st.number_input("Sewa Alat (Rp/ha)", value=300000, step=50000, key=f"alat_{st.session_state.active_scenario}")
            with col2:
                biaya_transportasi = st.number_input("Transportasi (Rp/ha)", value=200000, step=50000, key=f"transport_{st.session_state.active_scenario}")
                biaya_lain_detail = st.number_input("Lain-lain (Rp/ha)", value=200000, step=50000, key=f"lain_d_{st.session_state.active_scenario}")
            total_lainnya = biaya_irigasi + biaya_sewa_alat + biaya_transportasi + biaya_lain_detail
    
    # Calculate button
    st.markdown("---")
    if st.button("🧮 Hitung RAB", type="primary", use_container_width=True):
        # Calculate totals
        total_biaya_per_ha = total_persiapan + total_pupuk + total_pestisida + total_tenaga_kerja + total_lainnya
        total_biaya = total_biaya_per_ha * luas_lahan
        
        # Revenue
        total_produksi_kg = target_produksi * luas_lahan * 1000
        total_pendapatan = total_produksi_kg * harga_jual
        
        # Profit
        keuntungan = total_pendapatan - total_biaya
        roi = (keuntungan / total_biaya * 100) if total_biaya > 0 else 0
        biaya_per_kg = total_biaya / total_produksi_kg if total_produksi_kg > 0 else 0
        margin_per_kg = keuntungan / total_produksi_kg if total_produksi_kg > 0 else 0
        
        # Cash flow projection (4 months cycle)
        cash_flow = {
            'Bulan 1': -total_persiapan * luas_lahan - (total_pupuk * 0.4 * luas_lahan),
            'Bulan 2': -(total_pupuk * 0.3 * luas_lahan) - (total_pestisida * 0.5 * luas_lahan) - (total_tenaga_kerja * 0.3 * luas_lahan),
            'Bulan 3': -(total_pupuk * 0.3 * luas_lahan) - (total_pestisida * 0.5 * luas_lahan) - (total_tenaga_kerja * 0.3 * luas_lahan),
            'Bulan 4': -(total_tenaga_kerja * 0.4 * luas_lahan) - total_lainnya * luas_lahan + total_pendapatan
        }
        
        cumulative_cash = []
        running_total = 0
        for month, amount in cash_flow.items():
            running_total += amount
            cumulative_cash.append(running_total)
        
        # Store in session state
        st.session_state.scenarios[st.session_state.active_scenario] = {
            # Basic info
            'luas_lahan': luas_lahan,
            'lokasi': lokasi,
            'varietas': varietas,
            'metode_tanam': metode_tanam,
            'target_produksi': target_produksi,
            'harga_jual': harga_jual,
            'musim_tanam': musim_tanam,
            
            # Costs
            'total_persiapan': total_persiapan * luas_lahan,
            'total_pupuk': total_pupuk * luas_lahan,
            'total_pestisida': total_pestisida * luas_lahan,
            'total_tenaga_kerja': total_tenaga_kerja * luas_lahan,
            'total_lainnya': total_lainnya * luas_lahan,
            'total_biaya': total_biaya,
            'biaya_per_ha': total_biaya_per_ha,
            
            # Revenue & Profit
            'total_produksi_kg': total_produksi_kg,
            'total_pendapatan': total_pendapatan,
            'keuntungan': keuntungan,
            'roi': roi,
            'biaya_per_kg': biaya_per_kg,
            'margin_per_kg': margin_per_kg,
            
            # Cash flow
            'cash_flow': cash_flow,
            'cumulative_cash': cumulative_cash,
            'peak_financing': min(cumulative_cash),
            
            # Timestamp
            'calculated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        st.success(f"✅ RAB untuk {st.session_state.active_scenario} berhasil dihitung!")
        st.balloons()

# ==================== TAB 2: HASIL RAB ====================
with tab2:
    if not st.session_state.scenarios:
        st.info("ℹ️ Silakan input data dan hitung RAB di tab 'Input Data' terlebih dahulu")
    else:
        data = st.session_state.scenarios.get(st.session_state.active_scenario)
        
        if not data:
            st.warning(f"Data untuk {st.session_state.active_scenario} belum dihitung")
        else:
            # Summary metrics
            st.markdown(f"<h3>{icon('chart-bar')} Ringkasan Keuangan - {st.session_state.active_scenario}</h3>", unsafe_allow_html=True)
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Biaya", f"Rp {data['total_biaya']:,.0f}", f"Rp {data['biaya_per_ha']:,.0f}/ha")
            col2.metric("Total Pendapatan", f"Rp {data['total_pendapatan']:,.0f}", f"{data['total_produksi_kg']/1000:.1f} ton")
            col3.metric("Keuntungan Bersih", f"Rp {data['keuntungan']:,.0f}", 
                       f"{data['roi']:.1f}% ROI",
                       delta_color="normal" if data['keuntungan'] > 0 else "inverse")
            col4.metric("Biaya Produksi", f"Rp {data['biaya_per_kg']:,.0f}/kg", 
                       f"Margin: Rp {data['margin_per_kg']:,.0f}/kg")
            
            st.markdown("---")
            
            # Cost breakdown
            col_chart, col_table = st.columns([1.5, 1])
            
            with col_chart:
                st.markdown(f"<h3>{icon('chart-pie')} Struktur Biaya</h3>", unsafe_allow_html=True)
                
                breakdown_df = pd.DataFrame({
                    'Kategori': ['Persiapan Lahan', 'Pupuk', 'Pestisida', 'Tenaga Kerja', 'Lainnya'],
                    'Biaya': [
                        data['total_persiapan'],
                        data['total_pupuk'],
                        data['total_pestisida'],
                        data['total_tenaga_kerja'],
                        data['total_lainnya']
                    ]
                })
                breakdown_df['Persentase'] = (breakdown_df['Biaya'] / data['total_biaya'] * 100).round(1)
                
                # Pie chart
                pie = alt.Chart(breakdown_df).mark_arc(innerRadius=50).encode(
                    theta=alt.Theta('Biaya:Q'),
                    color=alt.Color('Kategori:N', scale=alt.Scale(scheme='category10')),
                    tooltip=['Kategori', alt.Tooltip('Biaya:Q', format=',.0f'), alt.Tooltip('Persentase:Q', format='.1f')]
                ).properties(height=300)
                
                st.altair_chart(pie, use_container_width=True)
            
            with col_table:
                st.markdown(f"<h3>{icon('table')} Detail Biaya</h3>", unsafe_allow_html=True)
                st.dataframe(
                    breakdown_df.style.format({
                        'Biaya': 'Rp {:,.0f}',
                        'Persentase': '{:.1f}%'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
            
            # Cash Flow Projection
            st.markdown("---")
            st.markdown(f"<h3>{icon('chart-line')} Proyeksi Arus Kas</h3>", unsafe_allow_html=True)
            
            cash_flow_df = pd.DataFrame({
                'Bulan': list(data['cash_flow'].keys()),
                'Arus Kas': list(data['cash_flow'].values()),
                'Kumulatif': data['cumulative_cash']
            })
            
            col_cf1, col_cf2 = st.columns([2, 1])
            
            with col_cf1:
                # Cash flow chart
                base = alt.Chart(cash_flow_df).encode(x='Bulan:O')
                
                bars = base.mark_bar().encode(
                    y='Arus Kas:Q',
                    color=alt.condition(
                        alt.datum['Arus Kas'] > 0,
                        alt.value(COLORS['success']),
                        alt.value(COLORS['error'])
                    ),
                    tooltip=['Bulan', alt.Tooltip('Arus Kas:Q', format=',.0f')]
                )
                
                line = base.mark_line(point=True, color=COLORS['primary']).encode(
                    y='Kumulatif:Q',
                    tooltip=['Bulan', alt.Tooltip('Kumulatif:Q', format=',.0f')]
                )
                
                chart = (bars + line).properties(height=300)
                st.altair_chart(chart, use_container_width=True)
            
            with col_cf2:
                st.markdown("**Analisis Arus Kas:**")
                st.metric("Kebutuhan Modal Puncak", f"Rp {abs(data['peak_financing']):,.0f}")
                st.metric("Posisi Kas Akhir", f"Rp {data['cumulative_cash'][-1]:,.0f}")
                
                if data['peak_financing'] < 0:
                    st.warning(f"⚠️ Perlu pembiayaan maksimal Rp {abs(data['peak_financing']):,.0f}")
                else:
                    st.success("✅ Tidak perlu pembiayaan eksternal")

# ==================== TAB 3: ANALISIS ====================
with tab3:
    if len(st.session_state.scenarios) < 1:
        st.info("ℹ️ Buat minimal 1 skenario untuk melihat analisis")
    else:
        st.markdown(f"<h3>{icon('chart-line')} Analisis Komparatif</h3>", unsafe_allow_html=True)
        
        # Scenario comparison
        if len(st.session_state.scenarios) >= 2:
            st.markdown("#### Perbandingan Skenario")
            
            # Create comparison dataframe
            comparison_data = []
            for name, scenario in st.session_state.scenarios.items():
                comparison_data.append({
                    'Skenario': name,
                    'Varietas': scenario['varietas'],
                    'Luas (ha)': scenario['luas_lahan'],
                    'Biaya Total': scenario['total_biaya'],
                    'Pendapatan': scenario['total_pendapatan'],
                    'Keuntungan': scenario['keuntungan'],
                    'ROI (%)': scenario['roi'],
                    'Biaya/kg': scenario['biaya_per_kg']
                })
            
            comp_df = pd.DataFrame(comparison_data)
            
            # Display comparison table
            st.dataframe(
                comp_df.style.format({
                    'Luas (ha)': '{:.1f}',
                    'Biaya Total': 'Rp {:,.0f}',
                    'Pendapatan': 'Rp {:,.0f}',
                    'Keuntungan': 'Rp {:,.0f}',
                    'ROI (%)': '{:.1f}',
                    'Biaya/kg': 'Rp {:,.0f}'
                }).background_gradient(subset=['ROI (%)'], cmap='RdYlGn'),
                use_container_width=True,
                hide_index=True
            )
            
            # Comparison charts
            col1, col2 = st.columns(2)
            
            with col1:
                # ROI comparison
                roi_chart = alt.Chart(comp_df).mark_bar().encode(
                    x=alt.X('Skenario:N', title=''),
                    y=alt.Y('ROI (%):Q', title='ROI (%)'),
                    color=alt.Color('ROI (%):Q', scale=alt.Scale(scheme='redyellowgreen')),
                    tooltip=['Skenario', alt.Tooltip('ROI (%):Q', format='.1f')]
                ).properties(title='Perbandingan ROI', height=300)
                st.altair_chart(roi_chart, use_container_width=True)
            
            with col2:
                # Cost comparison
                cost_chart = alt.Chart(comp_df).mark_bar().encode(
                    x=alt.X('Skenario:N', title=''),
                    y=alt.Y('Biaya/kg:Q', title='Biaya per kg (Rp)'),
                    color=alt.value(COLORS['primary']),
                    tooltip=['Skenario', alt.Tooltip('Biaya/kg:Q', format=',.0f')]
                ).properties(title='Perbandingan Biaya Produksi', height=300)
                st.altair_chart(cost_chart, use_container_width=True)
            
            # Best scenario recommendation
            st.markdown("---")
            st.markdown("#### 🏆 Rekomendasi")
            
            best_roi = comp_df.loc[comp_df['ROI (%)'].idxmax()]
            lowest_cost = comp_df.loc[comp_df['Biaya/kg'].idxmin()]
            highest_profit = comp_df.loc[comp_df['Keuntungan'].idxmax()]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.success(f"**ROI Tertinggi**\n\n{best_roi['Skenario']}\n\n{best_roi['ROI (%)']:.1f}%")
            with col2:
                st.success(f"**Biaya Terendah**\n\n{lowest_cost['Skenario']}\n\nRp {lowest_cost['Biaya/kg']:,.0f}/kg")
            with col3:
                st.success(f"**Keuntungan Terbesar**\n\n{highest_profit['Skenario']}\n\nRp {highest_profit['Keuntungan']:,.0f}")
        
        else:
            st.info("Buat minimal 2 skenario untuk perbandingan")
        
        # Sensitivity Analysis (for active scenario)
        if st.session_state.active_scenario in st.session_state.scenarios:
            st.markdown("---")
            st.markdown(f"<h4>{icon('sliders')} Analisis Sensitivitas - {st.session_state.active_scenario}</h4>", unsafe_allow_html=True)
            
            data = st.session_state.scenarios[st.session_state.active_scenario]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Sensitivitas Harga Jual**")
                price_range = np.linspace(data['harga_jual'] * 0.7, data['harga_jual'] * 1.3, 7)
                profit_by_price = []
                
                for price in price_range:
                    new_revenue = data['total_produksi_kg'] * price
                    new_profit = new_revenue - data['total_biaya']
                    profit_by_price.append(new_profit)
                
                price_df = pd.DataFrame({
                    'Harga (Rp/kg)': price_range,
                    'Keuntungan': profit_by_price
                })
                
                price_chart = alt.Chart(price_df).mark_line(point=True, color=COLORS['primary']).encode(
                    x=alt.X('Harga (Rp/kg):Q', title='Harga Jual (Rp/kg)'),
                    y=alt.Y('Keuntungan:Q', title='Keuntungan (Rp)'),
                    tooltip=[alt.Tooltip('Harga (Rp/kg):Q', format=',.0f'), alt.Tooltip('Keuntungan:Q', format=',.0f')]
                ).properties(height=250)
                st.altair_chart(price_chart, use_container_width=True)
            
            with col2:
                st.markdown("**Sensitivitas Produktivitas**")
                prod_range = np.linspace(data['target_produksi'] * 0.7, data['target_produksi'] * 1.3, 7)
                profit_by_prod = []
                
                for prod in prod_range:
                    new_prod_kg = prod * data['luas_lahan'] * 1000
                    new_revenue = new_prod_kg * data['harga_jual']
                    new_profit = new_revenue - data['total_biaya']
                    profit_by_prod.append(new_profit)
                
                prod_df = pd.DataFrame({
                    'Produktivitas (ton/ha)': prod_range,
                    'Keuntungan': profit_by_prod
                })
                
                prod_chart = alt.Chart(prod_df).mark_line(point=True, color=COLORS['success']).encode(
                    x=alt.X('Produktivitas (ton/ha):Q', title='Produktivitas (ton/ha)'),
                    y=alt.Y('Keuntungan:Q', title='Keuntungan (Rp)'),
                    tooltip=[alt.Tooltip('Produktivitas (ton/ha):Q', format='.1f'), alt.Tooltip('Keuntungan:Q', format=',.0f')]
                ).properties(height=250)
                st.altair_chart(prod_chart, use_container_width=True)
        
        # Cost Structure Analysis
        if st.session_state.active_scenario in st.session_state.scenarios:
            st.markdown("---")
            st.markdown(f"<h4>{icon('chart-pie')} Analisis Struktur Biaya - {st.session_state.active_scenario}</h4>", unsafe_allow_html=True)
            
            data = st.session_state.scenarios[st.session_state.active_scenario]
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Klasifikasi Biaya**")
                
                # Fixed vs Variable costs estimation
                fixed_costs = data['total_persiapan'] + (data['total_lainnya'] * 0.5)
                variable_costs = data['total_pupuk'] + data['total_pestisida'] + data['total_tenaga_kerja'] + (data['total_lainnya'] * 0.5)
                
                cost_class_df = pd.DataFrame({
                    'Kategori': ['Biaya Tetap', 'Biaya Variabel'],
                    'Nilai': [fixed_costs, variable_costs],
                    'Persentase': [
                        fixed_costs / data['total_biaya'] * 100,
                        variable_costs / data['total_biaya'] * 100
                    ]
                })
                
                st.dataframe(
                    cost_class_df.style.format({
                        'Nilai': 'Rp {:,.0f}',
                        'Persentase': '{:.1f}%'
                    }),
                    use_container_width=True,
                    hide_index=True
                )
                
                st.metric("Rasio Biaya Tetap", f"{fixed_costs/data['total_biaya']*100:.1f}%")
                st.metric("Biaya Variabel per kg", f"Rp {variable_costs/data['total_produksi_kg']:,.0f}")
            
            with col2:
                st.markdown("**Efisiensi Biaya**")
                
                # Cost efficiency metrics
                metrics_df = pd.DataFrame({
                    'Metrik': [
                        'Biaya per Hektar',
                        'Biaya per Kilogram',
                        'Biaya per Ton',
                        'Produktivitas Modal'
                    ],
                    'Nilai': [
                        f"Rp {data['biaya_per_ha']:,.0f}",
                        f"Rp {data['biaya_per_kg']:,.0f}",
                        f"Rp {data['biaya_per_kg']*1000:,.0f}",
                        f"{data['total_produksi_kg']/data['total_biaya']*1000:.2f} kg/juta"
                    ]
                })
                
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)
                
                # Marginal analysis
                if data['luas_lahan'] > 0:
                    marginal_cost = data['total_biaya'] / data['luas_lahan']
                    marginal_revenue = data['total_pendapatan'] / data['luas_lahan']
                    st.metric("Margin Kontribusi per ha", f"Rp {marginal_revenue - marginal_cost:,.0f}")
        
        # Benchmark Comparison
        if st.session_state.active_scenario in st.session_state.scenarios:
            st.markdown("---")
            st.markdown(f"<h4>{icon('trophy')} Perbandingan dengan Benchmark Regional</h4>", unsafe_allow_html=True)
            
            data = st.session_state.scenarios[st.session_state.active_scenario]
            benchmark = REGIONAL_BENCHMARKS.get(data['lokasi'], REGIONAL_BENCHMARKS['Jawa Barat'])
            
            # Calculate efficiency scores
            scores = calculate_efficiency_score(data, benchmark)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                score_color = "🟢" if scores['cost_efficiency'] >= 70 else "🟡" if scores['cost_efficiency'] >= 50 else "🔴"
                st.metric("Efisiensi Biaya", f"{scores['cost_efficiency']:.0f}/100", score_color)
            
            with col2:
                score_color = "🟢" if scores['productivity_efficiency'] >= 70 else "🟡" if scores['productivity_efficiency'] >= 50 else "🔴"
                st.metric("Efisiensi Produktivitas", f"{scores['productivity_efficiency']:.0f}/100", score_color)
            
            with col3:
                score_color = "🟢" if scores['roi_efficiency'] >= 70 else "🟡" if scores['roi_efficiency'] >= 50 else "🔴"
                st.metric("Efisiensi ROI", f"{scores['roi_efficiency']:.0f}/100", score_color)
            
            with col4:
                score_color = "🟢" if scores['overall'] >= 70 else "🟡" if scores['overall'] >= 50 else "🔴"
                st.metric("Skor Keseluruhan", f"{scores['overall']:.0f}/100", score_color)
            
            # Comparison table
            st.markdown("**Perbandingan Detail**")
            comparison_df = pd.DataFrame({
                'Indikator': ['Biaya per ha', 'Produktivitas', 'Biaya per kg', 'ROI'],
                'Anda': [
                    f"Rp {data['biaya_per_ha']:,.0f}",
                    f"{data['target_produksi']:.1f} ton/ha",
                    f"Rp {data['biaya_per_kg']:,.0f}",
                    f"{data['roi']:.1f}%"
                ],
                'Rata-rata Regional': [
                    f"Rp {benchmark['avg_cost_per_ha']:,.0f}",
                    f"{benchmark['avg_productivity']:.1f} ton/ha",
                    f"Rp {benchmark['avg_cost_per_kg']:,.0f}",
                    f"{benchmark['avg_roi']:.0f}%"
                ],
                'Status': [
                    "✅ Lebih Rendah" if data['biaya_per_ha'] < benchmark['avg_cost_per_ha'] else "⚠️ Lebih Tinggi",
                    "✅ Lebih Tinggi" if data['target_produksi'] > benchmark['avg_productivity'] else "⚠️ Lebih Rendah",
                    "✅ Lebih Rendah" if data['biaya_per_kg'] < benchmark['avg_cost_per_kg'] else "⚠️ Lebih Tinggi",
                    "✅ Lebih Tinggi" if data['roi'] > benchmark['avg_roi'] else "⚠️ Lebih Rendah"
                ]
            })
            
            st.dataframe(comparison_df, use_container_width=True, hide_index=True)


# ==================== TAB 4: EXPORT ====================
with tab4:
    st.markdown(f"<h3>{icon('download')} Export & Laporan</h3>", unsafe_allow_html=True)
    
    if not st.session_state.scenarios:
        st.info("Belum ada data untuk di-export")
    else:
        # Select scenarios to export
        export_scenarios = st.multiselect(
            "Pilih Skenario untuk Export",
            list(st.session_state.scenarios.keys()),
            default=list(st.session_state.scenarios.keys())
        )
        
        if export_scenarios:
            # Create export dataframe
            export_data = []
            for name in export_scenarios:
                scenario = st.session_state.scenarios[name]
                export_data.append({
                    'Skenario': name,
                    'Lokasi': scenario['lokasi'],
                    'Varietas': scenario['varietas'],
                    'Metode Tanam': scenario['metode_tanam'],
                    'Luas Lahan (ha)': scenario['luas_lahan'],
                    'Target Produksi (ton/ha)': scenario['target_produksi'],
                    'Harga Jual (Rp/kg)': scenario['harga_jual'],
                    'Total Biaya (Rp)': scenario['total_biaya'],
                    'Total Pendapatan (Rp)': scenario['total_pendapatan'],
                    'Keuntungan (Rp)': scenario['keuntungan'],
                    'ROI (%)': scenario['roi'],
                    'Biaya per kg (Rp)': scenario['biaya_per_kg'],
                    'Margin per kg (Rp)': scenario['margin_per_kg']
                })
            
            export_df = pd.DataFrame(export_data)
            
            # Preview
            st.markdown("#### Preview Data Export")
            st.dataframe(export_df, use_container_width=True, hide_index=True)
            
            # Export buttons
            col1, col2, col3 = st.columns(3)
            
            with col1:
                csv = export_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📄 Download CSV",
                    data=csv,
                    file_name=f"RAB_Padi_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                # Excel export (requires openpyxl)
                try:
                    from io import BytesIO
                    buffer = BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                        export_df.to_excel(writer, sheet_name='RAB Summary', index=False)
                    
                    st.download_button(
                        label="📄 Download Excel",
                        data=buffer.getvalue(),
                        file_name=f"RAB_Padi_{datetime.now().strftime('%Y%m%d')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                except ImportError:
                    st.info("Install openpyxl untuk export Excel")
            
            with col3:
                st.button("🖨️ Print Preview", use_container_width=True, disabled=True)
                st.caption("Coming soon")

# Footer
st.markdown("---")
st.caption("ℹ️ **Tips:** Gunakan mode Detail untuk breakdown biaya yang lebih akurat. Bandingkan beberapa skenario untuk keputusan terbaik.")
