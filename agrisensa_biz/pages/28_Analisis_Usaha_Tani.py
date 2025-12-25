import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import sys
import os
import io
import datetime

# Add updated path logic if needed, but for same-repo deployment:
from utils.auth import require_auth, show_user_info_sidebar


# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

# Add parent directory to path for imports (required for Streamlit Cloud)
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.ai_farm_service import get_ai_model, optimize_solution

# ==========================================
# 📊 DATABASE STANDARD OPERATIONAL (RAB)
# ==========================================
# ==========================================
# 📊 DATABASE STANDARD OPERATIONAL (RAB)
# ==========================================
# Harga asumsi nasional (bisa diedit user)
# HOK = Hari Orang Kerja (standar 8 jam kerja)

import sys
import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.crop_service import CropService
from services.project_service import ProjectManager

# 1. Initialize with Legacy/Non-standard Crops
CROP_TEMPLATES = {
    "Jagung Hibrida": {
        "params": {"populasi_ha": 66000, "total_panen_kg": 9000, "harga_jual": 5000, "lama_tanam_bulan": 4},
        "items": [
            {"kategori": "Biaya Tetap", "item": "Sewa Lahan", "satuan": "Musim", "volume": 1, "harga": 3000000, "wajib": True},
            {"kategori": "Benih", "item": "Benih Hibrida (Exp: NK/Bisi)", "satuan": "Kg", "volume": 20, "harga": 110000, "wajib": True},
            {"kategori": "Pupuk", "item": "Urea", "satuan": "Kg", "volume": 350, "harga": 6000, "wajib": True},
            {"kategori": "Pupuk", "item": "NPK", "satuan": "Kg", "volume": 300, "harga": 15000, "wajib": True},
             {"kategori": "Pestisida", "item": "Herbisida Selektif Jagung", "satuan": "Liter", "volume": 3, "harga": 180000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Olah Tanah", "satuan": "Borongan/Ha", "volume": 1, "harga": 2000000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Tanam", "satuan": "HOK", "volume": 15, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Pemupukan I & II", "satuan": "HOK", "volume": 12, "harga": 90000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Panen & Pipil", "satuan": "Borongan", "volume": 1, "harga": 3500000, "wajib": True},
        ]
    },
     "Kentang (Dieng/Granola)": {
         "params": {"populasi_ha": 25000, "total_panen_kg": 20000, "harga_jual": 12000, "lama_tanam_bulan": 4},
         "items": [
             {"kategori": "Biaya Tetap", "item": "Sewa Lahan Bukit", "satuan": "Musim", "volume": 1, "harga": 8000000, "wajib": True},
             {"kategori": "Benih", "item": "Bibit Knol (G1/G2)", "satuan": "Kg", "volume": 1200, "harga": 25000, "wajib": True},
             {"kategori": "Pupuk", "item": "Pupuk Kandang (Ayam/Sapi)", "satuan": "Ton", "volume": 15, "harga": 800000, "wajib": True},
             {"kategori": "Pestisida", "item": "Fungisida (Phytophthora)", "satuan": "Paket", "volume": 1, "harga": 10000000, "wajib": True, "catatan": "Sangat tinggi di musim hujan"},
             {"kategori": "Tenaga Kerja", "item": "Garpu/Bedengan Tinggi", "satuan": "HOK", "volume": 80, "harga": 100000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Panen & Angkut", "satuan": "Borongan", "volume": 1, "harga": 5000000, "wajib": True},
         ]
    },
    "Kubis / Kol": {
        "params": {"populasi_ha": 30000, "total_panen_kg": 50000, "harga_jual": 2000, "lama_tanam_bulan": 3},
        "items": [
            {"kategori": "Benih", "item": "Benih Hibrida", "satuan": "Sachet", "volume": 15, "harga": 80000, "wajib": True},
            {"kategori": "Pupuk", "item": "Pupuk Kandang & Urea", "satuan": "Paket", "volume": 1, "harga": 5000000, "wajib": True},
            {"kategori": "Pestisida", "item": "Insektisida (Ulat Krop)", "satuan": "Paket", "volume": 1, "harga": 3000000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Perawatan Intensif", "satuan": "HOK", "volume": 40, "harga": 90000, "wajib": True},
        ]
    },
    "Wortel": {
         "params": {"populasi_ha": 250000, "total_panen_kg": 25000, "harga_jual": 3000, "lama_tanam_bulan": 3.5},
         "items": [
             {"kategori": "Benih", "item": "Benih Unggul", "satuan": "Kaleng", "volume": 8, "harga": 300000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Olah Tanah (Gembur)", "satuan": "HOK", "volume": 50, "harga": 100000, "wajib": True, "catatan": "Tanah harus sangat gembur"},
             {"kategori": "Tenaga Kerja", "item": "Panen (Cabut & Cuci)", "satuan": "HOK", "volume": 80, "harga": 80000, "wajib": True},
         ]
    },
    "Semangka (Non-Biji)": {
         "params": {"populasi_ha": 4000, "total_panen_kg": 25000, "harga_jual": 4500, "lama_tanam_bulan": 3},
         "items": [
            {"kategori": "Benih", "item": "Benih Non-Biji + Serbuk Sari", "satuan": "Paket", "volume": 1, "harga": 3000000, "wajib": True},
            {"kategori": "Penunjang", "item": "Mulsa", "satuan": "Roll", "volume": 5, "harga": 650000, "wajib": True},
            {"kategori": "Pupuk", "item": "Pupuk Kandang & NPK", "satuan": "Paket", "volume": 1, "harga": 5000000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Olah Tanah", "satuan": "Borongan", "volume": 1, "harga": 2500000, "wajib": True},
         ]
    },
     "Buah Naga (Investasi Tahun 1)": {
        "params": {"populasi_ha": 2000, "total_panen_kg": 0, "harga_jual": 12000, "lama_tanam_bulan": 12}, 
        # Note: Yield Year 1 is usually 0 or low. We set 0 for konservatif, or allow small harvest.
        "items": [
            {"kategori": "Investasi Awal", "item": "Tiang Panjat (Beton/Kayu)", "satuan": "Batang", "volume": 500, "harga": 150000, "wajib": True, "catatan": "Jarak 2.5 x 2.5m (populasi 4 tan/tiang)"},
            {"kategori": "Investasi Awal", "item": "Ban Bekas / Penyangga", "satuan": "Buah", "volume": 500, "harga": 10000, "wajib": True},
            {"kategori": "Benih", "item": "Stek Batang (Bibit)", "satuan": "Batang", "volume": 2000, "harga": 5000, "wajib": True},
            {"kategori": "Pupuk", "item": "Pupuk Kandang (Awal)", "satuan": "Truk", "volume": 5, "harga": 1500000, "wajib": True},
            {"kategori": "Tenaga Kerja", "item": "Lubang Tanam & Pasang Tiang", "satuan": "Borongan", "volume": 1, "harga": 6000000, "wajib": True},
        ]
    },
    "Cabai Merah (Greenhouse Hydroponic)": {
        "params": {"populasi_ha": 30000, "total_panen_kg": 25000, "harga_jual": 30000, "lama_tanam_bulan": 6},
        "items": [
            {"kategori": "Biaya Tetap", "item": "Amortisasi Green house (Sewa/Penyusutan)", "satuan": "Musim", "volume": 1, "harga": 75000000, "wajib": True, "catatan": "Asumsi GH 1 Ha @1.5M, umur 10 thn"},
            {"kategori": "Biaya Tetap", "item": "Listrik & Air (Pompa)", "satuan": "Bulan", "volume": 6, "harga": 500000, "wajib": True},
            {"kategori": "Nutrisi (AB Mix)", "item": "Paket AB Mix Cabai (Pekat)", "satuan": "Paket (5L)", "volume": 100, "harga": 85000, "wajib": True, "catatan": "Kebutuhan Fertigasi Harian"},
            {"kategori": "Media Tanam", "item": "Cocopeat & Polybag", "satuan": "Paket", "volume": 1, "harga": 15000000, "wajib": True, "catatan": "Dipakai 2-3 musim"},
            {"kategori": "Benih", "item": "Benih F1 Import", "satuan": "Sachet", "volume": 20, "harga": 180000, "wajib": True},
            {"kategori": "Pestisida", "item": "Bio-Pesticide (Preventif)", "satuan": "Paket", "volume": 1, "harga": 1500000, "wajib": True, "catatan": "Hanya 30% dibanding Open Field"},
            {"kategori": "Tenaga Kerja", "item": "Operator Fertigasi & Pruning", "satuan": "HOK", "volume": 120, "harga": 100000, "wajib": True, "catatan": "Manajemen Intensif"},
             {"kategori": "Tenaga Kerja", "item": "Panen (Sortir Grade A)", "satuan": "HOK", "volume": 150, "harga": 90000, "wajib": True},
        ]
    },
    "Melon (Greenhouse Premium)": {
        "params": {"populasi_ha": 22000, "total_panen_kg": 35000, "harga_jual": 25000, "lama_tanam_bulan": 3},
        "items": [
             {"kategori": "Biaya Tetap", "item": "Amortisasi Green house", "satuan": "Musim", "volume": 1, "harga": 75000000, "wajib": True},
             {"kategori": "Biaya Tetap", "item": "Talianjir & Klip Gantung", "satuan": "Paket", "volume": 1, "harga": 5000000, "wajib": True},
            {"kategori": "Benih", "item": "Benih Melon Premium (Intanon/Fujisawa)", "satuan": "Biji", "volume": 22000, "harga": 2500, "wajib": True, "catatan": "Harga per biji!"},
             {"kategori": "Nutrisi (AB Mix)", "item": "Nutrisi Buah Premium", "satuan": "Paket", "volume": 150, "harga": 90000, "wajib": True},
             {"kategori": "Pestisida", "item": "Fungisida Powdery Mildew", "satuan": "Paket", "volume": 1, "harga": 1000000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Polinasi & Gantung Buah", "satuan": "HOK", "volume": 80, "harga": 100000, "wajib": True, "catatan": "Kritis & Rumit"},
             {"kategori": "Tenaga Kerja", "item": "Panen & Packaging", "satuan": "HOK", "volume": 60, "harga": 90000, "wajib": True},
        ]
    },
    "Krisan / Bunga Potong (Greenhouse)": {
        "params": {"populasi_ha": 400000, "total_panen_kg": 350000, "harga_jual": 2500, "lama_tanam_bulan": 3.5, "unit": "Batang"},
        "items": [
             {"kategori": "Biaya Tetap", "item": "Amortisasi Green house (Standard)", "satuan": "Musim", "volume": 1, "harga": 50000000, "wajib": True, "catatan": "Bambu/Besi Sederhana, umur 5 th"},
             {"kategori": "Biaya Tetap", "item": "Listrik Night Break (Lampu)", "satuan": "Bulan", "volume": 2, "harga": 1500000, "wajib": True, "catatan": "Fase Vegetatif (4-5 Jam/malam)"},
             {"kategori": "Persiapan Lahan", "item": "Amandemen (Kapur/Sekam)", "satuan": "Paket", "volume": 1, "harga": 5000000, "wajib": True},
             {"kategori": "Persiapan Lahan", "item": "Jaring Penegak (Netting)", "satuan": "Roll", "volume": 20, "harga": 350000, "wajib": True, "catatan": "Dipakai berulang 3-4x"},
             {"kategori": "Benih", "item": "Bibit Siap Tanam (Stek Pucuk)", "satuan": "Batang", "volume": 400000, "harga": 300, "wajib": True, "catatan": "Kerapatan 60-80 tan/m2"},
             {"kategori": "Pupuk", "item": "Pupuk Dasar & Kocor", "satuan": "Paket", "volume": 1, "harga": 12000000, "wajib": True},
             {"kategori": "Pestisida", "item": "Pestisida (Karat Putih/Trips)", "satuan": "Paket", "volume": 1, "harga": 8000000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Tanam/Pinch/Disbudding", "satuan": "HOK", "volume": 200, "harga": 90000, "wajib": True},
             {"kategori": "Tenaga Kerja", "item": "Panen & Ikat", "satuan": "HOK", "volume": 150, "harga": 90000, "wajib": True},
        ]
    },
}

# 2. Merge with Standardized Crops from Service
for crop_name in CropService.get_all_crops():
    data = CropService.get_rab_template(crop_name)
    if data:
        CROP_TEMPLATES[crop_name] = data
# ==========================================
# 🧠 LOGIC & UI
# ==========================================

st.title("💰 RAB Usaha Tani Presisi")
st.markdown("Buat Rencana Anggaran Biaya (RAB) dengan kalkulasi amandemen lahan, populasi, dan mulsa yang akurat.")

# ==========================================
# 📂 PROJECT MANAGEMENT SIDEBAR
# ==========================================
with st.sidebar:
    st.header("📂 Manajemen Proyek")
    
    # Initialize Session State for Params if not exist
    if 'rab_params' not in st.session_state:
        st.session_state.rab_params = {}
    
    # Load/Save Logic
    project_list = ProjectManager.get_all_projects_list()
    selected_project_load = st.selectbox("Pilih Proyek Tersimpan", ["-- Buat Baru --"] + project_list)
    
    col_proj1, col_proj2 = st.columns(2)
    if col_proj1.button("📂 Muat"):
        if selected_project_load != "-- Buat Baru --":
            data = ProjectManager.load_project(selected_project_load)
            if data:
                st.session_state.rab_params = data
                st.session_state['active_project_name'] = selected_project_load
                st.success(f"Proyek '{selected_project_load}' dimuat!")
                st.rerun()
                
    if col_proj2.button("🗑️ Hapus"):
         if selected_project_load != "-- Buat Baru --":
            ProjectManager.delete_project(selected_project_load)
            st.warning(f"Proyek dihapus.")
            st.rerun()

    st.divider()

# 1. SMART CALCULATOR & CONFIGURATION
with st.sidebar:
    st.header("⚙️ Kalkulator Agronomi")
    
    # Helper to get value from state or default
    def get_param(key, default):
        return st.session_state.rab_params.get(key, default)

    # A. Land & Crop
    # Note: selectbox requires index matching, so we find index of saved value
    saved_crop = get_param('crop', list(CROP_TEMPLATES.keys())[0])
    try:
        crop_idx = list(CROP_TEMPLATES.keys()).index(saved_crop)
    except:
        crop_idx = 0
        
    selected_crop = st.selectbox("Komoditas", list(CROP_TEMPLATES.keys()), index=crop_idx)
    
    # Unit Selector (Auto-detect preference)
    is_mikro = "Hidroponik" in selected_crop or "Greenhouse" in selected_crop
    
    saved_unit_idx = 1 if is_mikro else 0
    if 'satuan_luas' in st.session_state.rab_params:
         try:
             saved_unit_idx = ["Hektar (Ha)", "Meter Persegi (m²)"].index(st.session_state.rab_params['satuan_luas'])
         except: pass
         
    col_u1, col_u2 = st.columns([1, 2])
    with col_u1:
        satuan_luas = st.selectbox("Satuan", ["Hektar (Ha)", "Meter Persegi (m²)"], index=saved_unit_idx)
    
    with col_u2:
        if satuan_luas == "Hektar (Ha)":
            def_val = get_param('input_luas', 1.0)
            input_luas = st.number_input("Luas Lahan", 0.01, 100.0, float(def_val), step=0.1)
            luas_lahan_ha = input_luas
            luas_lahan_m2 = input_luas * 10000
        else:
            def_m2 = 500.0 if "Sayuran" in selected_crop else 1000.0
            def_val = get_param('input_luas', def_m2)
            # Prevent crash if switching from Ha (e.g. 1.0) to m2 (min 10.0)
            if def_val < 10.0: 
                def_val = def_m2
            input_luas = st.number_input("Luas Lahan", 10.0, 50000.0, float(def_val), step=100.0)
            luas_lahan_m2 = input_luas
            luas_lahan_ha = input_luas / 10000
            
    st.caption(f"Konversi: {luas_lahan_ha:.4f} Ha | {luas_lahan_m2:,.0f} m²")
    
    # Save params to state
    st.session_state.rab_params.update({
        'crop': selected_crop,
        'satuan_luas': satuan_luas,
        'input_luas': input_luas
    })
    
    st.divider()
    
    # B. Standar & Asumsi (New Config)
    st.subheader("⚙️ Standar & Asumsi")
    
    # 1. Labor Wage (HOK)
    def_wage = get_param('std_hok', 100000.0)
    std_hok = st.number_input("Standar Upah (Rp/HOK)", 50000.0, 500000.0, float(def_wage), step=10000.0, help="Upah harian rata-rata")
    
    # 2. Pesticide Cost
    def_pest = get_param('std_pest', 15000.0)
    std_pest = st.number_input("Biaya Racikan (Rp/Tangki)", 0.0, 200000.0, float(def_pest), step=1000.0, help="Rata-rata biaya per tangki", key="std_pest_cfg")
    
    st.session_state.rab_params.update({
        'std_hok': std_hok,
        'std_pest': std_pest
    })
    
    biaya_per_tangki = std_pest # Alias for backward compatibility if used globally
    
    st.divider()
    
    # B. Jarak Tanam (Bedengan vs Rak)
    st.subheader("📐 Jarak Tanam & Bedengan")
    
    # Defaults based on crop
    is_hydroponic = "Hidroponik" in selected_crop
    
    if "Bawang" in selected_crop:
        def_jarak = 15; def_bedengan = 120
    elif "Melon" in selected_crop:
        def_jarak = 40; def_bedengan = 100
    elif "Cabai" in selected_crop:
        def_jarak = 50; def_bedengan = 100
    elif "Sayuran Daun" in selected_crop: # Hydroponic default
        def_jarak = 20; def_bedengan = 200 # Meja lebar 2m
    elif "Krisan" in selected_crop:
        def_jarak = 12; def_bedengan = 100 # Jarak 12.5 x 12.5 cm -> 64 tanaman/m2 bedeng
    elif "Padi" in selected_crop:
        def_jarak = 25; def_bedengan = 0 # Not used for Padi
    else:
        def_jarak = 25; def_bedengan = 100
        
    def_parit = 50
    
    # Get params
    val_jarak = get_param('jarak_tanam', def_jarak)
    val_bedengan = get_param('lebar_bedengan', def_bedengan)
    val_parit = get_param('lebar_parit', def_parit)
    
    # --- PADI MODE: Pola Tanam ---
    padi_mode = "Padi" in selected_crop
    populasi_padi_override = 0
    
    if padi_mode:
        st.subheader("🌾 Pola Tanam Padi")
        pola_tanam = st.selectbox("Sistem Tanam", ["Sistem Tegel (25x25)", "Jajar Legowo 2:1", "Jajar Legowo 4:1", "Custom"])
        
        if pola_tanam == "Sistem Tegel (25x25)":
            jarak_padi = st.number_input("Jarak Tanam (cm)", 20, 30, 25)
            populasi_padi_override = (10000 / ((jarak_padi/100)**2)) * luas_lahan_ha
            st.caption(f"Populasi Tegel: {populasi_padi_override:,.0f} rumpun/ha")
            
        elif "Jajar Legowo" in pola_tanam:
            # Asumsi standar Legowo: Jarak antar baris 20-25cm, Legowo gap 40-50cm
            # Rumus Praktis: Peningkatan populasi vs Tegel
            # Legowo 2:1 -> +30% s.d +33% dari Tegel
            # Legowo 4:1 -> +20% s.d +25% dari Tegel
            basis_tegel = 160000 # 25x25
            
            if "2:1" in pola_tanam:
                factor = 1.33  # 213.300
                st.caption("ℹ️ Legowo 2:1 meningkatkan populasi ~33% dibanding Tegel.")
            else:
                factor = 1.25 # 200.000 (4:1)
                st.caption("ℹ️ Legowo 4:1 meningkatkan populasi ~25% dibanding Tegel.")
                
            populasi_padi_override = basis_tegel * factor * luas_lahan_ha
            
        elif pola_tanam == "Custom":
            c_p1, c_p2 = st.columns(2)
            with c_p1:
                j_baris = st.number_input("Jarak Antar Baris (cm)", 10, 100, 25)
            with c_p2:
                j_dalam = st.number_input("Jarak Dalam Baris (cm)", 10, 100, 25)
            
            populasi_padi_override = (10000 / ((j_baris/100) * (j_dalam/100))) * luas_lahan_ha
            
        # Fix NameError: Padi doesn't use Bedengan/Parit logic, but downstream calc needs it.
        # Set dummy to 100% efficiency.
        lebar_bedengan = 100 
        lebar_parit = 0

    
    elif is_hydroponic:

        st.subheader("🏗️ Instalasi Hidroponik")
        # Override Concept: Bedengan -> Meja/Gully, Parit -> Jalan Antar Meja
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            jarak_tanam = st.number_input("Jarak Lubang Tanam (cm)", 10, 50, int(val_jarak), step=5)
            lebar_bedengan = st.number_input("Lebar Meja/Rak (cm)", 50, 400, int(val_bedengan), step=10)
        with col_p2:
            lebar_parit = st.number_input("Jalan Antar Meja (cm)", 30, 150, int(val_parit), step=10)
            # Baris per meja usually derived or fixed, let's allow override
            val_baris = get_param('baris_per_bedeng', int(def_bedengan/20))
            baris_per_bedeng = st.number_input("Baris per Meja", 1, 20, int(val_baris), step=1, help="Lebar meja dibagi jarak tanam")
    else:
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            jarak_tanam = st.number_input("Jarak Tanam (cm)", 10, 100, int(val_jarak), step=5)
            lebar_bedengan = st.number_input("Lebar Bedengan (cm)", 50, 200, int(val_bedengan), step=10)
        with col_p2:
            lebar_parit = st.number_input("Lebar Parit (cm)", 30, 100, int(val_parit), step=10)
            
            saved_model_idx = 0
            if 'baris_per_bedeng' in st.session_state.rab_params:
                saved_model_idx = 0 if st.session_state.rab_params['baris_per_bedeng'] == 1 else 1
            
            if "Krisan" in selected_crop:
                 def_baris = 8
                 baris_per_bedeng = st.number_input("Baris per Bedengan", 2, 20, int(def_baris), step=1, help="Krisan butuh kerapatan tinggi")
            else:
                 baris_per_bedeng = st.selectbox("Model Tanam", [1, 2], index=saved_model_idx, format_func=lambda x: f"{x} Baris (Zigzag)" if x==2 else "1 Baris (Single)")
    
    # C. Mulch Specs
    st.divider()
    # C. Mulch Specs (Dynamic Check)
    template_items = CROP_TEMPLATES[selected_crop]['items']
    needs_mulsa = any("Mulsa" in i['item'] for i in template_items)
    
    st.divider()
    if needs_mulsa:
        st.subheader("⚫ Spesifikasi Mulsa")
        panjang_roll = st.number_input("Panjang per Roll (m)", 100, 1000, 250, step=50, help="Biasanya 250m atau 500m")
    else:
        panjang_roll = None

    # --- KHUSUS KRISAN: Input Panjang & Jumlah Bedengan ---
    krisan_mode = "Krisan" in selected_crop
    total_panjang_bedengan_override = 0
    
    if krisan_mode:
        st.divider()
        st.subheader("🌸 Dimensi Bedengan (Krisan)")
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            panjang_bedengan_m = st.number_input("Panjang Bedengan (m)", 1, 100, 50)
        with col_k2:
            jumlah_bedengan = st.number_input("Jumlah Bedengan", 1, 1000, 20)
            
        # Override Total Panjang Bedengan
        total_panjang_bedengan_override = panjang_bedengan_m * jumlah_bedengan
        
        # Override Luas Lahan Display (Estimasi)
        lebar_total_cm = lebar_bedengan + lebar_parit
        estimasi_luas_m2 = (lebar_total_cm / 100) * total_panjang_bedengan_override
        st.caption(f"ℹ️ Total Bedengan: {total_panjang_bedengan_override:,.0f} m | Est. Luas: {estimasi_luas_m2:,.0f} m²")
        
        # Sync to metric variables
        luas_lahan_m2 = estimasi_luas_m2
        luas_lahan_ha = luas_lahan_m2 / 10000


    # --- CALCULATION ENGINE ---
    # 1. Efficiency Metric
    total_lebar_segmen = (lebar_bedengan + lebar_parit) / 100 # meter
    # More accurate: Effective Bed Area = Area * (Bed / (Bed + Ditch))
    efisiensi_lahan = lebar_bedengan / (lebar_bedengan + lebar_parit)
    luas_bedengan_netto = luas_lahan_m2 * efisiensi_lahan
    
    # 2. Mulch Needs
    if krisan_mode:
        # Use explicit override
        total_panjang_bedengan = total_panjang_bedengan_override
    else:
        # Standard Formula
        # Total Length of Beds = Net Bed Area / Bed Width (in meters)
        total_panjang_bedengan = luas_bedengan_netto / (lebar_bedengan / 100)
    
    if panjang_roll and not is_hydroponic:
        kebutuhan_mulsa_roll = total_panjang_bedengan / panjang_roll
        # Round up safely e.g. 10% safety margin for cutting
        kebutuhan_mulsa_roll = np.ceil(kebutuhan_mulsa_roll * 1.05) 
    else:
        kebutuhan_mulsa_roll = 0
        
    # 3. Population Needs (Seeds)
    if padi_mode:
        populasi_tanaman = int(populasi_padi_override)
    else:
        # Standard Formula (Applies to Krisan, Chili, etc)
        # Pop = (Total Bed Length / Plant Spacing) * Rows per Bed
        # Ensure non-zero divisor
        j_tanam_m = max(jarak_tanam / 100, 0.05) 
        populasi_tanaman = (total_panjang_bedengan / j_tanam_m) * baris_per_bedeng
    
    # Safety margin 10% for 'sulam' if not Padi (Padi seeds usually by weight not clumps, but we track clumps for yield)
    if not padi_mode:
        populasi_tanaman = int(populasi_tanaman * 1.10)
    
    # Display Calc Results in Sidebar
    # Display Calc Results in Sidebar
    info_mulsa = f"- Kebutuhan Mulsa: **{kebutuhan_mulsa_roll:.0f}** Roll" if not is_hydroponic else ""
    st.info(f"""
    **🔍 Hasil Kalkulasi:**
    - Populasi: **{populasi_tanaman:,.0f}** Tanaman
    - Tot. Panjang Bedengan/Rak: **{total_panjang_bedengan:,.0f}** m
    {info_mulsa}
    """)
    
    # D. Metode Bibit (Restored)
    pilih_metode_bibit = "semai"
    pakai_booster = False
    
    if "Cabai" in selected_crop or "Tomat" in selected_crop or "Padi" in selected_crop:
        st.divider()
        st.subheader("🌱 Metode Bibit")
        if "Padi" in selected_crop:
             metode_bibit_ui = st.radio("Sumber Benih:", ["Beli Benih Label", "Benih Sendiri"], index=0)
             # Reuse helper
             pilih_metode_bibit = "semai" # Default logic
        else:
             metode_bibit_ui = st.radio("Sumber Bibit:", ["Semai Sendiri", "Beli Bibit Jadi"], index=0)
             pilih_metode_bibit = "semai" if "Semai" in metode_bibit_ui else "bibit"
        
        st.caption("💎 **Opsi Pupuk**")
        pakai_booster = st.checkbox("Pakai Booster (KNO3/Kalsium)?", value=True, help="Centang untuk hasil panen premium (Perpaduan Terbaik)")

    st.divider()

    # F. Pesticide Calculator (New Request)
    st.subheader("🚿 Kalkulator Penyemprotan")
    
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        cap_tangki = st.number_input("Kapasitas Tangki (Liter)", 10, 20, 16, help="Standar Knapsack Sprayer 16L")
        luas_per_tangki = st.number_input("Luas Semprot per Tangki (m²)", 100, 5000, 500, step=50, help="Satu tangki habis untuk berapa meter persegi?")
    
    with c_p2:
        def_freq = 24 if "Cabai" in selected_crop else 10 # Cabai intensif
        freq_semprot = st.number_input("Frekuensi Semprot (kali/musim)", 1, 100, def_freq, step=1)
        # Restore editable input with default from sidebar
        biaya_per_tangki = st.number_input("Biaya Racikan (Rp/Tangki)", 0, 100000, int(std_pest), step=1000, help="Default diambil dari Sidebar, tapi bisa diubah khusus di sini")

    # Calc Pesticide Needs
    jumlah_tangki_per_aplikasi = np.ceil(luas_lahan_m2 / luas_per_tangki)
    total_tangki_musim = jumlah_tangki_per_aplikasi * freq_semprot
    estimasi_biaya_pestisida = total_tangki_musim * biaya_per_tangki
    
    st.info(f"""
    **🔍 Data Penyemprotan:**
    - Kebutuhan: **{jumlah_tangki_per_aplikasi:.0f}** Tangki / aplikasi
    - Total: **{total_tangki_musim:.0f}** Tangki / musim
    - Est. Biaya: **Rp {estimasi_biaya_pestisida:,.0f}**
    """)
    if estimasi_biaya_pestisida > 100000000:
        st.error("⚠️ Biaya Pestisida > 100 Juta! Cek input 'Luas per Tangki' atau 'Harga per Tangki'.")

    # G. AI Integration (ENTERPRISE FEATURE)
    st.divider()
    st.markdown("### 🔮 Integrasi AI Smart Farming")
    
    # Check for Integration Context (from Map or NPK Module)
    ctx = st.session_state.get('rab_context', {})
    
    # Auto-enable AI if context exists
    default_ai_check = True if ctx else False
    use_ai_opt = st.checkbox("Optimasi Hasil dengan AI", value=default_ai_check)
    
    if ctx and use_ai_opt:
        with st.container():
            st.info(f"📋 **Inisiasi Data dari: {ctx.get('source')}**")
            k1, k2, k3, k4 = st.columns(4)
            k1.metric("pH Tanah", f"{ctx.get('ph')}", delta="Aktual")
            k2.metric("Tekstur", ctx.get('texture', '-'))
            k3.metric("N-P-K (ppm)", f"{int(ctx.get('n_ppm',0))}-{int(ctx.get('p_ppm',0))}-{int(ctx.get('k_ppm',0))}")
            
            if st.button("🔄 Reset Data Integrasi"):
                del st.session_state['rab_context']
                st.rerun()
        st.divider()

    ai_suggestion = None
        
    if use_ai_opt:
        st.markdown("##### 🧪 Input Data Tanah (Real-Time)")
        col_ai1, col_ai2 = st.columns(2)
        with col_ai1:
            # Auto-fill from Context if available
            def_ph = ctx.get('ph', 6.0)
            real_ph = st.number_input("pH Tanah Aktual", 3.0, 8.0, float(def_ph), step=0.1, help="Dari hasil tes tanah / Modul Peta Data Tanah")
            
            # Map Texture Strings
            def_tex_idx = 0
            if ctx.get('texture'):
                tex_str = ctx.get('texture').lower()
                if "pasir" in tex_str: def_tex_idx = 1
                elif "liat" in tex_str: def_tex_idx = 2
                
            real_texture = st.selectbox("Tekstur Tanah", ["Lempung (Ideal)", "Pasir (Boros Air)", "Liat (Padat)"], index=def_tex_idx)
            
        # Map Texture to Float (0-1 Index for AI)
        tex_map = {"Lempung (Ideal)": 0.7, "Pasir (Boros Air)": 0.2, "Liat (Padat)": 0.5}
        
        with st.spinner("AI sedang menghitung SOP optimal berdasarkan kondisi tanah..."):
            model = get_ai_model()
            # Advanced assumption mappings
            ai_params = {
                'rain': 2000, 
                'temp': 27,
                'texture': tex_map[real_texture],
                'pest_strategy': "IPM (Terpadu)"
            }
            # Optimize for Yield
            ai_suggestion = optimize_solution(model, 10000, "Yield", ai_params, price_per_kg=6000)
            
            st.success(f"✅ AI menyesuaikan resep dengan tanah {real_texture} & pH {real_ph}!")
            
            # Simple Dolomite Logic override based on pH Gap
            kebutuhan_kapur = 0
            if real_ph < 6.0:
                kebutuhan_kapur = (6.5 - real_ph) * 2000 # Rule of thumb: 1 ton per 0.5 pH delta? Simplified: 2 ton/ha per 1.0 delta
                kebutuhan_kapur = max(kebutuhan_kapur, 500) # Min 500kg if acidic
                
            st.markdown(f"""
            **Saran AI (Disesuaikan Kondisi Lapangan):**
            - Urea (N): {ai_suggestion['n_kg']:.0f} kg/ha
            - SP-36 (P): {ai_suggestion['p_kg']:.0f} kg/ha
            - KCl (K): {ai_suggestion['k_kg']:.0f} kg/ha
            - Kapur (Dolomit): {kebutuhan_kapur:.0f} kg/ha (utk netralisir pH {real_ph})
            """)

    # H. Market Assumptions
    st.subheader("💵 Asumsi Pasar")
    crop_data = CROP_TEMPLATES[selected_crop]['params']
    unit_hasil = crop_data.get('unit', 'kg') # Default kg
    
    if ai_suggestion:
        def_target_panen = float(ai_suggestion['predicted_yield'])
        st.caption("✨ Target hasil otomatis diisi oleh AI")
    else:
        def_target_panen = float(crop_data.get('estimasi_panen_kg', 10000))
        
    target_harga = st.number_input(f"Harga Jual (Rp/{unit_hasil})", 0, 200000, crop_data.get('harga_jual', 10000), step=100)
    target_panen = st.number_input(f"Target Hasil ({unit_hasil}/ha)", 0, 1000000, int(def_target_panen), step=500)

# 2. GENERATE DATA FRAME (DYNAMICALLY)
template_items = CROP_TEMPLATES[selected_crop]['items']
rab_data = []

for item in template_items:
    # Filter based on options
    if 'opsi' in item:
        if item['opsi'] in ['semai', 'bibit'] and item['opsi'] != pilih_metode_bibit:
            continue
        if item['opsi'] == 'premium' and not pakai_booster:
            continue
            
    # --- DYNAMIC VOLUME ASSIGNMENT ---
    vol = 0
    price_override = None
    item_name_override = None
    
    # Apply Standard HOK Price if unit is HOK
    if item['satuan'] == 'HOK':
        price_override = std_hok
    elif item['satuan'] == 'Tangki':
         price_override = biaya_per_tangki

    # AI OVERRIDES (If Active)
    ai_override_active = False
    
    if ai_suggestion:
        # Map AI outputs to RAB Items
        if "Urea" in item['item'] and "Pupuk" in item['kategori']:
            vol = ai_suggestion['n_kg'] * luas_lahan_ha
            item_name_override = f"{item['item']} (Saran AI: {ai_suggestion['n_kg']:.0f} kg/ha)"
            ai_override_active = True
        elif "SP-36" in item['item'] or ("kocor" in item['item'].lower() and "kompleks" not in item['item'].lower()):
             pass
        elif "Kapur" in item['item'] or "Dolomit" in item['item']:
            vol = kebutuhan_kapur # From pH logic
            item_name_override = f"{item['item']} (pH {real_ph} -> Butuh {kebutuhan_kapur:.0f} kg)"
            ai_override_active = True
    
    if not ai_override_active:
        # Case 1: Benih/Bibit (Use Calculated Population)
        if "Bibit Siap Tanam" in item['item']:
            vol = populasi_tanaman
        elif "Benih Biji" in item['item']:
            vol = np.ceil(populasi_tanaman / 1750)
        elif "Benih" in item['item'] and "Kg" in item['satuan']: 
             vol = item['volume'] * luas_lahan_ha
             
        # Case 2: Mulsa (Use Calculated Rolls)
        elif "Mulsa" in item['item']:
            vol = kebutuhan_mulsa_roll
            
        # Case 3: Ajir (Matches Population)
        elif "Ajir" in item['item'] and item['satuan'] in ['Batang', 'Buah', 'Pcs']:
            vol = populasi_tanaman 
            
        # Case 3b: KPemasangan Ajir
        elif "Pasang" in item['item'] and "Ajir" in item['item']:
             vol = np.ceil(populasi_tanaman / 750)

        # Case 3c: Benih Padi (Scale by Population Density)
        elif "Benih Padi" in item['item'] and padi_mode:
             # Standard 30kg is for Tegel (160k pop). Scale if density changes.
             # Only scale if we are calculating population (some modes might be area only)
             if populasi_tanaman > 0:
                 std_pop_per_ha = 160000
                 current_pop_per_ha = populasi_tanaman / luas_lahan_ha
                 scale_factor = current_pop_per_ha / std_pop_per_ha
                 # Apply scale but keep reasonable bounds (e.g. 0.8 to 1.5)
                 vol = item['volume'] * luas_lahan_ha * scale_factor
                 
                 if abs(scale_factor - 1.0) > 0.1:
                      item_name_override = f"{item['item']} (Kepadatan {scale_factor:.1f}x)"
             else:
                 vol = item['volume'] * luas_lahan_ha

        # Case 4: Pesticide (New Logic using Config)
        elif "Insektisida & Fungisida" in item['item'] or "Pestisida" in item['kategori']:
            if item['satuan'] == 'Paket' and not is_mikro: # Change legacy Paket to Tank model if open field
                 # Only convert if it looks like generic pesticide
                 vol = total_tangki_musim
                 item['satuan'] = "Tangki" # Override unit
                 price_override = biaya_per_tangki
                 item_name_override = f"Pestisida ({freq_semprot}x Aplikasi, @{biaya_per_tangki/1000:.0f}k/tangki)"
            elif item['satuan'] == 'Paket':
                 # Greenhouse fixed packets, usually per area
                 vol = item['volume'] * luas_lahan_ha
            else:
                 vol = item['volume'] * luas_lahan_ha # Default fallback
            
        # Case 5: Default Scaling by Area
            # Case 5: Default Scaling by Area
        else:
            if "Rockwool" in item['item']:
                # 1 Slab = 200 cubes approx
                vol = np.ceil(populasi_tanaman / 250) 
            elif "Benih" in item['item'] and "Kaleng" in item['satuan'] and "Sayur" in item['item']:
                 # 1 Kaleng 20ml = ~2000-3000 seeds? Let's assume high density
                 # Assume 1 kaleng covers 5000 plants
                 vol = np.ceil(populasi_tanaman / 5000)
            elif "AB Mix" in item['item']:
                 # 1 Paket 5L pekat = 1000L larutan siap pakai (EC 2.0).
                 # 1 Tanaman sayur butuh ~1-2 Liter nutrisi selama hidup (30 hari x 50ml/hari)
                 # Total Liter = Populasi * 1.5 Liter
                 total_larutan = populasi_tanaman * 1.5
                 vol = np.ceil(total_larutan / 1000)
                 item_name_override = f"{item['item']} (Butuh ~{total_larutan:,.0f} L Larutan)"
            elif item['item'] == "Pupuk Kandang/Organik":
                vol = item['volume'] * luas_lahan_ha
            else:
                vol = item['volume'] * luas_lahan_ha

    # Merge with User Edits (Persist manual changes)
    unique_key = item_name_override if item_name_override else item['item']
    
    # Final Append
    rab_data.append({
        "Kategori": item['kategori'],
        "Uraian": unique_key,
        "Satuan": item['satuan'],
        "Volume": float(vol),
        "Harga Satuan (Rp)": int(price_override if price_override is not None else item['harga']),
        "Total (Rp)": int(vol * (price_override if price_override is not None else item['harga'])),
        "Catatan": item.get('catatan', '-')
    })

# --- INJECT EXTRA ITEMS FOR KRISAN (IRRIGATION) ---
if krisan_mode:
    # 1. Nozzle (Tip 30 cm)
    # Jarak nozzle 30 cm -> 0.3 m
    jml_nozzle = np.ceil(total_panjang_bedengan_override / 0.3)
    harga_nozzle = 2500 # Asumsi harga satuan nozzle
    
    rab_data.append({
        "Kategori": "Irigasi (Drip/Sprinkler)",
        "Uraian": "Nozzle Sprayer (Jarak 30cm)",
        "Satuan": "Pcs",
        "Volume": float(jml_nozzle),
        "Harga Satuan (Rp)": harga_nozzle,
        "Total (Rp)": int(jml_nozzle * harga_nozzle),
        "Catatan": "Tengah bedengan"
    })
    
    # 2. Pipa (Sepanjang bedengan)
    panjang_pipa = np.ceil(total_panjang_bedengan_override)
    harga_pipa_per_m = 5000 # Asumsi PE 16mm/20mm
    
    rab_data.append({
        "Kategori": "Irigasi (Drip/Sprinkler)",
        "Uraian": "Pipa Irigasi (PE/PVC)",
        "Satuan": "Meter",
        "Volume": float(panjang_pipa),
        "Harga Satuan (Rp)": harga_pipa_per_m,
        "Total (Rp)": int(panjang_pipa * harga_pipa_per_m),
        "Catatan": "Sepanjang bedengan"
    })


# --- FIX: PERSIST EDITS AND RECALC TOTALS ---
if "rab_editor" in st.session_state:
    # Verify if it's the same crop context to avoid garbage mapping
    pass

df_rab = pd.DataFrame(rab_data)

cols_config = {
    "Kategori": st.column_config.TextColumn("Kategori", disabled=False),
    "Uraian": st.column_config.TextColumn("Uraian Pekerjaan/Barang", width="large"),
    "Satuan": st.column_config.TextColumn("Satuan", width="small"),
    "Volume": st.column_config.NumberColumn("Volume", format="%.1f"),
    "Harga Satuan (Rp)": st.column_config.NumberColumn("Harga Satuan", format="Rp %d"),
    "Total (Rp)": st.column_config.NumberColumn("Total Biaya", format="Rp %d", disabled=True),
}

# 3. MAIN TABLE EDITOR
st.subheader(f"📝 Tabel RAB: {selected_crop} ({luas_lahan_ha} Ha)")
st.info("💡 Klik sel untuk ubah data. Anda bisa mengetik manual di kolom 'Kategori' untuk menambah item baru (misal: 'Lainnya').")

# Session State for Dataframe to support "Reactive" updates
if 'df_rab_current' not in st.session_state or st.session_state.get('last_crop') != selected_crop:
    st.session_state['df_rab_current'] = df_rab
    st.session_state['last_crop'] = selected_crop
    # If we just switched crops, we disregard old edits
else:
    # If we are in same crop, we want to respect the LATEST edits from the user
    # But we also want to respect the "defaults" if param changed? 
    # Complexity: balancing "Auto-calc" vs "User Edit".
    # User said: "Perkalian tidak berubah". 
    # Best fix: Always use the *output* of the previous run as the *input* of the next, 
    # BUT re-run the multiplication logic on it.
    
    # Check if there's an edited DF from the widget
    pass

# We use a callback pattern effectively by just processing the previous `edited_df` if it exists in the variable scope from the last run? 
# No, streamlit reruns the whole script. 
# We just need to capture the `data_editor` return value, recalculate Total, and use THAT as the input for the NEXT render?
# No, that creates a lag.

# CORRECT PATTERN:
# 1. Create base `df_rab` from template (fresh).
# 2. Render data_editor with `df_rab`.
# 3. Capture `edited_df`.
# 4. Display `edited_df` metrics. 
# PROBLEM: The Table Widget itself shows (1), not (3).
# SOLUTION: We must use `st.data_editor` on a state-backed dataframe.

# Composite Context Key to detect upstream changes
current_input_context = f"{selected_crop}_{luas_lahan_ha}_{target_panen}_{target_harga}_{use_ai_opt}_{ai_override_active}_{std_hok}_{std_pest}_{freq_semprot}_{luas_per_tangki}_{biaya_per_tangki}_{pilih_metode_bibit}_{pakai_booster}"

if "rab_state_df" not in st.session_state:
    st.session_state.rab_state_df = df_rab
    st.session_state.last_input_context = current_input_context
elif st.session_state.get("last_input_context") != current_input_context:
    # Inputs changed! Reset the dataframe to reflect new params (Area scaling, etc)
    st.session_state.rab_state_df = df_rab
    st.session_state.last_input_context = current_input_context

# 4. DATA EDITOR DISPLAY
edited_df = st.data_editor(
    st.session_state.rab_state_df, 
    use_container_width=True, 
    num_rows="dynamic",
    column_config=cols_config,
    key="rab_editor"
)

# 5. RECALCULATE TOTALS (Reactive Mode)
# We need to recalc the 'Total (Rp)' column because user might have changed Volume or Price
edited_df['Total (Rp)'] = edited_df['Volume'] * edited_df['Harga Satuan (Rp)']

# 6. SUMMARY METRICS
total_biaya = edited_df['Total (Rp)'].sum()
estimasi_omzet = target_panen * luas_lahan_ha * target_harga
estimasi_laba = estimasi_omzet - total_biaya
roi_percent = (estimasi_laba / total_biaya * 100) if total_biaya > 0 else 0

st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Total Biaya (RAB)", f"Rp {total_biaya:,.0f}", help="Total CAPEX + OPEX")
m2.metric("Est. Omzet Panen", f"Rp {estimasi_omzet:,.0f}", f"{target_panen:,.0f} {unit_hasil} x Rp {target_harga}")
m3.metric("Potensi Laba", f"Rp {estimasi_laba:,.0f}", f"ROI: {roi_percent:.1f}%")

# Unit Economics Row
st.markdown("##### 📊 Unit Economics")
u1, u2, u3, u4 = st.columns(4)

# Calculate cost per plant
biaya_per_batang = total_biaya / populasi_tanaman if populasi_tanaman > 0 else 0
biaya_per_kg = total_biaya / (target_panen * luas_lahan_ha) if (target_panen * luas_lahan_ha) > 0 else 0

u1.metric("Biaya per Batang", f"Rp {biaya_per_batang:,.0f}", help=f"Total Biaya / {populasi_tanaman:,.0f} tanaman")
u2.metric(f"Biaya per {unit_hasil}", f"Rp {biaya_per_kg:,.0f}", help="Total Biaya / Total Hasil Panen")
u3.metric("Populasi Tanaman", f"{populasi_tanaman:,.0f} btg", help="Jumlah total tanaman")
u4.metric("Target Panen", f"{target_panen * luas_lahan_ha:,.0f} {unit_hasil}", help=f"{target_panen:,.0f} {unit_hasil}/ha x {luas_lahan_ha} ha")

# ==========================================
# 🔄 GLOBAL SYNC (For Strategic Report)
# ==========================================
st.session_state['global_rab_summary'] = {
    "komoditas": selected_crop,
    "luas_lahan": luas_lahan_ha,
    "total_biaya": total_biaya,
    "estimasi_omzet": estimasi_omzet,
    "estimasi_laba": estimasi_laba,
    "roi_percent": roi_percent,
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
}

if roi_percent < 0:
    st.error("⚠️ Proyeksi Rugi! Coba kurangi biaya tetangga atau naikkan target panen.")
elif roi_percent > 100:
    st.success("🚀 Potensi ROI Sangat Tinggi (High Risk High Return)")

# ==========================================
# 📊 BREAK-EVEN & ECONOMIC ANALYSIS
# ==========================================
st.divider()
st.header("📊 Analisis Ekonomi & Break-Even")

# Get parameters from template or session state
template_params = CROP_TEMPLATES[selected_crop]['params']
target_panen = template_params.get('estimasi_panen_kg', 10000)  # kg/ha
target_harga = template_params.get('harga_jual', 10000)  # Rp/kg
unit_hasil = template_params.get('unit', 'kg')
harga_jual = target_harga  # Alias for consistency
lama_tanam_bulan = template_params.get('lama_tanam_bulan', 4)  # months

# Calculate fixed and variable costs
biaya_tetap = sum([row['Total (Rp)'] for row in edited_df.to_dict('records') if row['Kategori'] == 'Biaya Tetap'])
biaya_variabel = total_biaya - biaya_tetap
total_panen_kg = target_panen * luas_lahan_ha  # Total yield in kg

# Calculate cost per unit (Total RAB / Total Yield)
biaya_per_unit = total_biaya / total_panen_kg if total_panen_kg > 0 else 0
biaya_variabel_per_unit = biaya_variabel / total_panen_kg if total_panen_kg > 0 else 0

# Create tabs for different analyses
tab_bep, tab_sensitivity, tab_profit = st.tabs([
    "📈 Break-Even Analysis",
    "🔍 Sensitivity Analysis", 
    "💹 Profit Scenarios"
])

# ===== TAB 1: BREAK-EVEN ANALYSIS =====
with tab_bep:
    st.subheader("📈 Break-Even Point (BEP)")
    
    st.markdown("""
    ### Apa itu Break-Even Point?
    
    **BEP** adalah titik dimana **Total Revenue = Total Cost** (tidak untung, tidak rugi).
    
    **Formula:**
    
    $$BEP_{unit} = \\frac{Biaya\\ Tetap}{Harga\\ Jual - Biaya\\ Variabel\\ per\\ Unit}$$
    """)
    
    # Calculate BEP
    if harga_jual > biaya_variabel_per_unit:
        contribution_margin = harga_jual - biaya_variabel_per_unit
        
        # Check if there are fixed costs
        if biaya_tetap > 0:
            bep_units = biaya_tetap / contribution_margin
            bep_rupiah = bep_units * harga_jual
        else:
            # No fixed costs - special case
            bep_units = 0
            bep_rupiah = 0
            
            st.warning("""
            ⚠️ **Tidak Ada Biaya Tetap Terdeteksi**
            
            Template komoditas ini tidak memiliki item dengan kategori "Biaya Tetap".
            
            **Implikasi:**
            - BEP = 0 (setiap penjualan langsung profit)
            - Contribution Margin per unit: Rp {:,.0f}
            - Profit = Quantity × Contribution Margin
            
            **Rekomendasi:**
            - Jika ada biaya tetap (sewa lahan, penyusutan, dll), tambahkan manual di tabel RAB
            - Atau gunakan analisis Profit Scenarios di tab berikutnya
            """.format(contribution_margin))
        
        # Margin of Safety
        actual_sales_rupiah = total_panen_kg * harga_jual
        mos_rupiah = actual_sales_rupiah - bep_rupiah
        mos_percentage = (mos_rupiah / actual_sales_rupiah) * 100 if actual_sales_rupiah > 0 else 0
        
        # Display Results
        col_bep1, col_bep2, col_bep3 = st.columns(3)
        
        with col_bep1:
            st.metric("BEP (kg/unit)", f"{bep_units:,.0f} {unit_hasil}")
            st.caption("Minimal penjualan untuk BEP")
        
        with col_bep2:
            st.metric("BEP (Rupiah)", f"Rp {bep_rupiah:,.0f}")
            st.caption("Revenue minimal untuk BEP")
        
        with col_bep3:
            st.metric("Contribution Margin", f"Rp {contribution_margin:,.0f}")
            st.caption("Per unit contribution")
        
        # Margin of Safety
        st.markdown("### 🛡️ Margin of Safety (MOS)")
        
        col_mos1, col_mos2, col_mos3 = st.columns(3)
        
        with col_mos1:
            st.metric("MOS (Rupiah)", f"Rp {mos_rupiah:,.0f}")
        
        with col_mos2:
            st.metric("MOS (%)", f"{mos_percentage:.1f}%")
        
        with col_mos3:
            st.metric("Actual Profit", f"Rp {estimasi_laba:,.0f}")
        
        # Interpretation
        if mos_percentage > 30:
            st.success(f"""
            **✅ Margin of Safety Sangat Baik ({mos_percentage:.1f}%)**
            
            - Bisnis memiliki cushion yang besar
            - Dapat menahan penurunan penjualan hingga {mos_percentage:.1f}% sebelum rugi
            - Risiko rendah
            """)
        elif mos_percentage > 15:
            st.info(f"""
            **⚠️ Margin of Safety Cukup ({mos_percentage:.1f}%)**
            
            - Bisnis cukup aman tapi perlu monitoring
            - Fokus pada efisiensi biaya
            """)
        else:
            st.warning(f"""
            **⚠️ Margin of Safety Rendah ({mos_percentage:.1f}%)**
            
            - Risiko tinggi - dekat dengan BEP
            - Perlu strategi untuk meningkatkan penjualan atau menurunkan biaya
            """)
        
        # Visualization
        st.markdown("### 📈 Break-Even Chart")
        
        # Generate data for chart
        units_range = np.linspace(0, bep_units * 2, 100)
        total_cost_line = biaya_tetap + (biaya_variabel_per_unit * units_range)
        total_revenue_line = harga_jual * units_range
        
        fig_bep = go.Figure()
        
        # Total Cost line
        fig_bep.add_trace(go.Scatter(
            x=units_range,
            y=total_cost_line,
            mode='lines',
            name='Total Cost',
            line=dict(color='red', width=2)
        ))
        
        # Total Revenue line
        fig_bep.add_trace(go.Scatter(
            x=units_range,
            y=total_revenue_line,
            mode='lines',
            name='Total Revenue',
            line=dict(color='green', width=2)
        ))
        
        # BEP point
        fig_bep.add_trace(go.Scatter(
            x=[bep_units],
            y=[bep_rupiah],
            mode='markers',
            name='Break-Even Point',
            marker=dict(size=15, color='blue', symbol='star')
        ))
        
        # Actual sales point
        fig_bep.add_trace(go.Scatter(
            x=[total_panen_kg],
            y=[actual_sales_rupiah],
            mode='markers',
            name='Target Sales',
            marker=dict(size=12, color='orange', symbol='diamond')
        ))
        
        fig_bep.update_layout(
            title=f'Break-Even Analysis - {selected_crop}',
            xaxis_title=f'Quantity ({unit_hasil})',
            yaxis_title='Rupiah',
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_bep, use_container_width=True)
        
        # Cost Breakdown
        st.markdown("### 💰 Cost Structure")
        
        col_cost1, col_cost2 = st.columns(2)
        
        with col_cost1:
            # Pie chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Biaya Tetap', 'Biaya Variabel'],
                values=[biaya_tetap, biaya_variabel],
                hole=.3
            )])
            fig_pie.update_layout(title='Cost Distribution', height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_cost2:
            st.markdown("**Cost Breakdown:**")
            cost_breakdown = pd.DataFrame({
                'Type': ['Biaya Tetap', 'Biaya Variabel', 'Total', 'Cost per Unit'],
                'Amount': [
                    f"Rp {biaya_tetap:,.0f}",
                    f"Rp {biaya_variabel:,.0f}",
                    f"Rp {total_biaya:,.0f}",
                    f"Rp {biaya_per_unit:,.0f}/{unit_hasil}"
                ],
                'Share (%)': [
                    f"{(biaya_tetap/total_biaya*100):.1f}%" if total_biaya > 0 else "0%",
                    f"{(biaya_variabel/total_biaya*100):.1f}%" if total_biaya > 0 else "0%",
                    "100.0%",
                    "-"
                ]
            })
            st.dataframe(cost_breakdown, use_container_width=True)
            
            # Add explanation
            st.caption(f"""
            💡 **Cost per Unit** = Total RAB / Total Yield
            
            = Rp {total_biaya:,.0f} / {total_panen_kg:,.0f} {unit_hasil}
            = Rp {biaya_per_unit:,.0f} per {unit_hasil}
            
            Ini adalah biaya produksi per unit hasil panen.
            """)
    
    else:
        st.error(f"""
        ⚠️ **Tidak Bisa Hitung BEP!**
        
        Harga jual (Rp {harga_jual:,.0f}) harus lebih besar dari biaya variabel per unit (Rp {biaya_variabel_per_unit:,.0f})
        
        **Solusi:**
        - Naikkan harga jual, atau
        - Turunkan biaya variabel
        """)

# ===== TAB 2: SENSITIVITY ANALYSIS =====
with tab_sensitivity:
    st.subheader("🔍 Sensitivity Analysis")
    
    st.markdown("""
    ### Analisis Sensitivitas
    
    Bagaimana profit berubah jika ada perubahan pada:
    - Harga jual
    - Biaya produksi
    - Volume penjualan
    """)
    
    # Price Sensitivity
    st.markdown("#### 📊 Price Sensitivity")
    
    price_changes = np.array([-20, -10, 0, 10, 20])
    new_prices = harga_jual * (1 + price_changes/100)
    
    price_sens_data = []
    for i, change in enumerate(price_changes):
        new_price = new_prices[i]
        new_revenue = total_panen_kg * new_price
        new_profit = new_revenue - total_biaya
        new_roi = (new_profit / total_biaya * 100) if total_biaya > 0 else 0
        
        price_sens_data.append({
            'Price Change (%)': f"{change:+.0f}%",
            'New Price': f"Rp {new_price:,.0f}",
            'Revenue': f"Rp {new_revenue:,.0f}",
            'Profit': f"Rp {new_profit:,.0f}",
            'ROI (%)': f"{new_roi:.1f}%"
        })
    
    price_sens_df = pd.DataFrame(price_sens_data)
    st.dataframe(price_sens_df, use_container_width=True)
    
    # Yield Sensitivity
    st.markdown("#### 🌾 Yield Sensitivity")
    
    yield_changes = np.array([-20, -10, 0, 10, 20])
    new_yields = total_panen_kg * (1 + yield_changes/100)
    
    yield_sens_data = []
    for i, change in enumerate(yield_changes):
        new_yield = new_yields[i]
        new_revenue = new_yield * harga_jual
        new_profit = new_revenue - total_biaya
        new_roi = (new_profit / total_biaya * 100) if total_biaya > 0 else 0
        
        yield_sens_data.append({
            'Yield Change (%)': f"{change:+.0f}%",
            'New Yield': f"{new_yield:,.0f} {unit_hasil}",
            'Revenue': f"Rp {new_revenue:,.0f}",
            'Profit': f"Rp {new_profit:,.0f}",
            'ROI (%)': f"{new_roi:.1f}%"
        })
    
    yield_sens_df = pd.DataFrame(yield_sens_data)
    st.dataframe(yield_sens_df, use_container_width=True)
    
    # Visualization
    st.markdown("#### 📈 Sensitivity Chart")
    
    fig_sens = go.Figure()
    
    # Price sensitivity line
    price_profits = [float(row['Profit'].replace('Rp ', '').replace(',', '')) for row in price_sens_data]
    fig_sens.add_trace(go.Scatter(
        x=price_changes,
        y=price_profits,
        mode='lines+markers',
        name='Price Sensitivity',
        line=dict(color='blue', width=2)
    ))
    
    # Yield sensitivity line
    yield_profits = [float(row['Profit'].replace('Rp ', '').replace(',', '')) for row in yield_sens_data]
    fig_sens.add_trace(go.Scatter(
        x=yield_changes,
        y=yield_profits,
        mode='lines+markers',
        name='Yield Sensitivity',
        line=dict(color='green', width=2)
    ))
    
    fig_sens.update_layout(
        title='Profit Sensitivity to Price & Yield Changes',
        xaxis_title='Change (%)',
        yaxis_title='Profit (Rp)',
        height=400
    )
    
    st.plotly_chart(fig_sens, use_container_width=True)

# ===== TAB 3: PROFIT SCENARIOS =====
with tab_profit:
    st.subheader("💹 Profit Scenarios")
    
    st.markdown("""
    ### Skenario Optimis vs Pesimis
    
    Bandingkan profit dalam berbagai kondisi pasar.
    """)
    
    # Define scenarios
    scenarios = {
        'Pesimis': {'price_mult': 0.8, 'yield_mult': 0.8, 'cost_mult': 1.2},
        'Realistis': {'price_mult': 1.0, 'yield_mult': 1.0, 'cost_mult': 1.0},
        'Optimis': {'price_mult': 1.2, 'yield_mult': 1.2, 'cost_mult': 0.9}
    }
    
    scenario_results = []
    
    for scenario_name, multipliers in scenarios.items():
        scenario_price = harga_jual * multipliers['price_mult']
        scenario_yield = total_panen_kg * multipliers['yield_mult']
        scenario_cost = total_biaya * multipliers['cost_mult']
        scenario_revenue = scenario_price * scenario_yield
        scenario_profit = scenario_revenue - scenario_cost
        scenario_roi = (scenario_profit / scenario_cost * 100) if scenario_cost > 0 else 0
        
        scenario_results.append({
            'Scenario': scenario_name,
            'Price': f"Rp {scenario_price:,.0f}",
            'Yield': f"{scenario_yield:,.0f} {unit_hasil}",
            'Cost': f"Rp {scenario_cost:,.0f}",
            'Revenue': f"Rp {scenario_revenue:,.0f}",
            'Profit': f"Rp {scenario_profit:,.0f}",
            'ROI (%)': f"{scenario_roi:.1f}%"
        })
    
    scenario_df = pd.DataFrame(scenario_results)
    st.dataframe(scenario_df, use_container_width=True)
    
    # Visualization
    st.markdown("#### 📊 Scenario Comparison")
    
    scenario_names = [s['Scenario'] for s in scenario_results]
    scenario_profits = [float(s['Profit'].replace('Rp ', '').replace(',', '')) for s in scenario_results]
    
    fig_scenario = go.Figure(data=[
        go.Bar(
            x=scenario_names,
            y=scenario_profits,
            text=[f"Rp {p:,.0f}" for p in scenario_profits],
            textposition='auto',
            marker_color=['red', 'yellow', 'green']
        )
    ])
    
    fig_scenario.update_layout(
        title='Profit by Scenario',
        xaxis_title='Scenario',
        yaxis_title='Profit (Rp)',
        height=400
    )
    
    st.plotly_chart(fig_scenario, use_container_width=True)
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    
    st.info(f"""
    **Based on Analysis:**
    
    1. **Break-Even Point:** {bep_units:,.0f} {unit_hasil} @ Rp {bep_rupiah:,.0f}
    2. **Current Target:** {total_panen_kg:,.0f} {unit_hasil} ({(total_panen_kg/bep_units*100):.0f}% of BEP)
    3. **Margin of Safety:** {mos_percentage:.1f}%
    
    **Action Items:**
    - Monitor harga pasar secara berkala
    - Fokus pada efisiensi untuk turunkan biaya variabel
    - Diversifikasi untuk mitigasi risiko
    - Target minimal: {bep_units:,.0f} {unit_hasil} untuk avoid loss
    """)


# 7. EXPORT & ACTIONS
st.subheader("📤 Export & Simpan")
c_ex1, c_ex2 = st.columns(2)

# save logic
with c_ex1:
    save_name = st.text_input("Nama Proyek", value=st.session_state.get('active_project_name', f"RAB {selected_crop}"))
    if st.button("💾 Simpan Proyek"):
        project_data = st.session_state.rab_params.copy()
        ProjectManager.save_project(save_name, project_data)
        st.success(f"Proyek '{save_name}' berhasil disimpan!")

# Download Logic

with c_ex2:
    st.write("Download Data")
    
    # --- EXCEL EXPORT (Using pandas) ---
    buffer_excel = io.BytesIO()
    with pd.ExcelWriter(buffer_excel, engine='xlsxwriter') as writer:
        edited_df.to_excel(writer, sheet_name='RAB Detail', index=False)
        # Add Summary Sheet
        summary_data = pd.DataFrame([{
            "Parameter": "Komoditas", "Nilai": selected_crop
        }, {
            "Parameter": "Luas Lahan", "Nilai": f"{luas_lahan_ha} Ha"
        }, {
            "Parameter": "Total Biaya", "Nilai": total_biaya
        }, {
            "Parameter": "Estimasi Omzet", "Nilai": estimasi_omzet
        }, {
            "Parameter": "Estimasi Laba", "Nilai": estimasi_laba
        }])
        summary_data.to_excel(writer, sheet_name='Ringkasan', index=False)
        
    st.download_button(
        label="📥 Download Excel (.xlsx)",
        data=buffer_excel.getvalue(),
        file_name=f"RAB_{selected_crop}_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.ms-excel"
    )

    # --- CSV EXPORT ---
    csv = edited_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "📄 Download CSV",
        csv,
        f"RAB_{selected_crop}.csv",
        "text/csv",
        key='download-csv'
    )

# 8. ADVANCED ECONOMIC ANALYSIS
st.divider()
st.subheader("📊 Analisis Ekonomi Lanjutan")

st.info("""
**💡 Tip:** Gunakan data RAB ini untuk analisis ekonomi mendalam di Module Ekonomi Pertanian!

Analisis yang tersedia:
- **Break-Even Analysis** - Hitung titik impas dan margin of safety
- **Profit Maximization** - Optimasi keuntungan
- **Optimal Input Allocation** - Alokasi input yang paling efisien
""")

if st.button("📊 Analyze in Economics Module", type="primary", use_container_width=True):
    # Prepare data for economics module
    st.session_state['economics_data'] = {
        'source': 'Analisis Usaha Tani',
        'crop': selected_crop,
        'land_area_ha': luas_lahan_ha,
        'population': populasi_tanaman,
        'estimated_yield_kg': total_panen_kg,
        'selling_price': harga_jual,
        'total_cost': total_biaya,
        'total_revenue': estimasi_omzet,
        'profit': estimasi_laba,
        'roi_percent': roi_percent,
        'production_period_months': lama_tanam_bulan,
        
        # Break-even data
        'fixed_cost': sum([row['Total (Rp)'] for row in edited_df.to_dict('records') if row['Kategori'] == 'Biaya Tetap']),
        'variable_cost': total_biaya - sum([row['Total (Rp)'] for row in edited_df.to_dict('records') if row['Kategori'] == 'Biaya Tetap']),
        'variable_cost_per_unit': (total_biaya - sum([row['Total (Rp)'] for row in edited_df.to_dict('records') if row['Kategori'] == 'Biaya Tetap'])) / total_panen_kg if total_panen_kg > 0 else 0,
        
        # Cost breakdown
        'cost_by_category': edited_df.groupby('Kategori')['Total (Rp)'].sum().to_dict(),
        'detailed_costs': edited_df.to_dict('records'),
        
        # Timestamp
        'exported_at': datetime.datetime.now().isoformat()
    }
    
    st.success("✅ Data berhasil disiapkan untuk analisis ekonomi!")
    st.info("""
    **Next Steps:**
    1. Buka **Module 13: 📊 Ekonomi Pertanian** dari sidebar
    2. Pilih tab yang sesuai:
       - Tab 3: Cost & Profit Analysis → Break-Even
       - Tab 4: Optimal Input Calculator
    3. Data akan otomatis ter-load!
    
    Atau klik tombol di bawah untuk langsung ke module:
    """)
    
    # Note: st.switch_page only works in same app, so we provide instructions
    st.markdown("""
    **📍 Lokasi Module:**
    - **AgriSensa Tech** → **13_📊_Ekonomi_Pertanian**
    
    Data sudah tersimpan di session dan siap digunakan!
    """)
