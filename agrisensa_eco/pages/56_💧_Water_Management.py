import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.water_calculator import WaterCalculator
from utils.auth import require_auth, show_user_info_sidebar

# Page config
st.set_page_config(
    page_title="Smart Water Management",
    page_icon="💧",
    layout="wide"
)

# Authentication
user = require_auth()
show_user_info_sidebar()

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f0f9ff;
    }
    .stMetric {
        background: rgba(255, 255, 255, 0.9);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .water-card {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(14, 165, 233, 0.3);
        margin: 20px 0;
    }
    .irrigation-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #0ea5e9;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .alert-irrigate {
        background: #fef3c7;
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .alert-no-irrigate {
        background: #d1fae5;
        border-left: 5px solid #10b981;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("💧 Smart Water Management")
st.markdown("""
Optimasi penggunaan air untuk pertanian berkelanjutan. Hemat air, tingkatkan hasil panen! 🌾
""")

st.markdown("---")

# Initialize calculator
calc = WaterCalculator()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "💧 Water Footprint",
    "📅 Irrigation Scheduler",
    "🏗️ Drip Irrigation ROI",
    "📚 Panduan"
])

# ===== TAB 1: WATER FOOTPRINT =====
with tab1:
    st.subheader("Kalkulator Water Footprint")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Input Data")
        
        crop = st.selectbox(
            "Komoditas",
            options=list(calc.CROP_WATER_REQUIREMENTS.keys()),
            help="Pilih jenis tanaman"
        )
        
        area_ha = st.number_input(
            "Luas Lahan (ha)",
            min_value=0.1,
            max_value=100.0,
            value=2.5,
            step=0.5
        )
        
        yield_kg = st.number_input(
            "Hasil Panen (kg)",
            min_value=100,
            max_value=1000000,
            value=12000,
            step=100,
            help="Total hasil panen dalam kg"
        )
        
        soil_type = st.selectbox(
            "Jenis Tanah",
            options=["sandy", "loam", "clay"],
            index=1,
            format_func=lambda x: {"sandy": "Berpasir", "loam": "Lempung (Loam)", "clay": "Liat (Clay)"}[x]
        )
    
    with col2:
        st.markdown("### 💡 Info Komoditas")
        
        req = calc.CROP_WATER_REQUIREMENTS.get(crop)
        
        st.info(f"""
        **{crop}**
        
        - **Kebutuhan Air**: {req['total_mm']} mm/musim
        - **Durasi**: {req['duration_days']} hari
        - **Kebutuhan Harian**: {req['total_mm']/req['duration_days']:.1f} mm/hari
        
        💧 **Kategori**: {'Tinggi' if req['total_mm'] > 800 else 'Sedang' if req['total_mm'] > 500 else 'Rendah'}
        """)
    
    if st.button("💧 Hitung Water Footprint", type="primary", use_container_width=True):
        result = calc.calculate_water_footprint(crop, area_ha, yield_kg)
        
        st.markdown("---")
        st.markdown("### 📊 Hasil Analisis")
        
        col_m1, col_m2, col_m3 = st.columns(3)
        
        with col_m1:
            st.metric(
                "Total Air Digunakan",
                f"{result['total_water_m3']:,.0f} m³",
                f"{result['duration_days']} hari"
            )
        
        with col_m2:
            st.metric(
                "Water Footprint",
                f"{result['water_footprint_l_per_kg']:,.0f} L/kg",
                "per kilogram produk"
            )
        
        with col_m3:
            # Benchmark (simplified)
            benchmarks = {
                'Padi': 2500,
                'Jagung': 900,
                'Cabai Merah': 1000,
                'Tomat': 400
            }
            benchmark = benchmarks.get(crop, 1000)
            diff = result['water_footprint_l_per_kg'] - benchmark
            
            st.metric(
                "vs Benchmark",
                f"{benchmark:,.0f} L/kg",
                f"{diff:+.0f} L/kg",
                delta_color="inverse"
            )
        
        # Recommendations
        st.markdown("### 💡 Rekomendasi Penghematan Air")
        
        col_r1, col_r2, col_r3 = st.columns(3)
        
        with col_r1:
            st.success("""
            **🚿 Irigasi Tetes**
            - Hemat: 40-60%
            - ROI: 2-3 tahun
            - Yield: +15-25%
            """)
        
        with col_r2:
            st.success("""
            **🌾 Mulching**
            - Hemat: 25-35%
            - Evaporasi ↓
            - Gulma ↓
            """)
        
        with col_r3:
            st.success("""
            **🌱 Varietas Hemat Air**
            - Hemat: 15-20%
            - Drought-tolerant
            - Adaptif iklim
            """)


# ===== TAB 2: IRRIGATION SCHEDULER =====
with tab2:
    st.subheader("📅 Jadwal Irigasi Cerdas (7 Hari)")
    
    st.success("""
    ✅ **Terintegrasi dengan Open-Meteo API** - Prediksi cuaca real-time untuk optimasi irigasi!
    
    Jadwal irigasi disesuaikan otomatis berdasarkan forecast hujan 7 hari ke depan.
    """)
    
    col_s1, col_s2, col_s3 = st.columns(3)
    
    with col_s1:
        crop_schedule = st.selectbox(
            "Pilih Tanaman",
            options=list(calc.CROP_WATER_REQUIREMENTS.keys()),
            key="schedule_crop"
        )
    
    with col_s2:
        crop_age = st.number_input(
            "Umur Tanaman (hari)",
            min_value=1,
            max_value=200,
            value=45,
            help="Berapa hari sejak tanam"
        )
    
    with col_s3:
        # Location selector for weather
        location_presets = {
            "Jakarta": (-6.2088, 106.8456),
            "Bandung": (-6.9175, 107.6191),
            "Surabaya": (-7.2575, 112.7521),
            "Yogyakarta": (-7.7956, 110.3695),
            "Bogor": (-6.5971, 106.8060)
        }
        location = st.selectbox("Lokasi Kebun", list(location_presets.keys()))
        lat, lon = location_presets[location]
    
    # Get real weather data
    try:
        # Import weather service from agrisensa_tech
        import sys
        tech_services_path = str(Path(__file__).parent.parent.parent / "agrisensa_tech" / "services")
        if tech_services_path not in sys.path:
            sys.path.insert(0, tech_services_path)
        
        from weather_service import WeatherService
        
        weather_service = WeatherService()
        weather_data = weather_service.get_weather_forecast(lat, lon)
        
        if weather_data:
            forecast_7day = weather_service.get_7day_forecast(weather_data)
            
            st.markdown("### 🌤️ Jadwal 7 Hari Ke Depan (Real-Time)")
            
            req = calc.CROP_WATER_REQUIREMENTS.get(crop_schedule)
            daily_need = req['total_mm'] / req['duration_days']
            
            for day_forecast in forecast_7day:
                date_obj = datetime.strptime(day_forecast['date'], '%Y-%m-%d')
                day_name = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'][date_obj.weekday()]
                
                rain_mm = day_forecast['rain_mm']
                temp_max = day_forecast['temp_max']
                temp_min = day_forecast['temp_min']
                
                # Determine weather icon
                if rain_mm > 10:
                    weather_icon = "🌧️ Hujan Lebat"
                elif rain_mm > 5:
                    weather_icon = "🌦️ Hujan Sedang"
                elif rain_mm > 0:
                    weather_icon = "🌤️ Hujan Ringan"
                else:
                    weather_icon = "☀️ Cerah"
                
                need_irrigation = rain_mm < daily_need
                irrigation_amount = max(0, daily_need - rain_mm)
                
                if need_irrigation:
                    st.markdown(f"""
                    <div class="alert-irrigate">
                        <h4>{day_name}, {date_obj.strftime('%d %b %Y')}</h4>
                        <p>{weather_icon} | Hujan: {rain_mm:.1f}mm | Suhu: {temp_min:.0f}-{temp_max:.0f}°C</p>
                        <p>💧 Kebutuhan: {daily_need:.1f}mm/hari</p>
                        <p><strong>⚠️ PERLU IRIGASI: {irrigation_amount:.1f}mm</strong></p>
                        <p><small>Alasan: Hujan tidak cukup ({rain_mm:.1f}mm < {daily_need:.1f}mm)</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="alert-no-irrigate">
                        <h4>{day_name}, {date_obj.strftime('%d %b %Y')}</h4>
                        <p>{weather_icon} | Hujan: {rain_mm:.1f}mm | Suhu: {temp_min:.0f}-{temp_max:.0f}°C</p>
                        <p>💧 Kebutuhan: {daily_need:.1f}mm/hari</p>
                        <p><strong>✅ TIDAK PERLU IRIGASI</strong></p>
                        <p><small>Alasan: Hujan cukup ({rain_mm:.1f}mm ≥ {daily_need:.1f}mm)</small></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("❌ Gagal mengambil data cuaca. Menampilkan simulasi...")
            # Fallback to simulated data (original code)
            st.markdown("### 🌤️ Jadwal 7 Hari Ke Depan (Simulasi)")
            
            req = calc.CROP_WATER_REQUIREMENTS.get(crop_schedule)
            daily_need = req['total_mm'] / req['duration_days']
            
            today = datetime.now()
            weather_sim = [
                {'rain': 2, 'weather': '🌤️ Berawan'},
                {'rain': 15, 'weather': '🌧️ Hujan Lebat'},
                {'rain': 0, 'weather': '☀️ Cerah'},
                {'rain': 5, 'weather': '🌦️ Hujan Ringan'},
                {'rain': 0, 'weather': '☀️ Cerah'},
                {'rain': 8, 'weather': '🌧️ Hujan Sedang'},
                {'rain': 3, 'weather': '🌤️ Berawan'}
            ]
            
            for i, weather in enumerate(weather_sim):
                date = today + timedelta(days=i)
                day_name = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu'][date.weekday()]
                
                rain_mm = weather['rain']
                need_irrigation = rain_mm < daily_need
                irrigation_amount = max(0, daily_need - rain_mm)
                
                if need_irrigation:
                    st.markdown(f"""
                    <div class="alert-irrigate">
                        <h4>{day_name}, {date.strftime('%d %b %Y')}</h4>
                        <p>{weather['weather']} | Hujan: {rain_mm}mm</p>
                        <p>💧 Kebutuhan: {daily_need:.1f}mm/hari</p>
                        <p><strong>⚠️ PERLU IRIGASI: {irrigation_amount:.1f}mm</strong></p>
                        <p><small>Alasan: Hujan tidak cukup ({rain_mm}mm < {daily_need:.1f}mm)</small></p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="alert-no-irrigate">
                        <h4>{day_name}, {date.strftime('%d %b %Y')}</h4>
                        <p>{weather['weather']} | Hujan: {rain_mm}mm</p>
                        <p>💧 Kebutuhan: {daily_need:.1f}mm/hari</p>
                        <p><strong>✅ TIDAK PERLU IRIGASI</strong></p>
                        <p><small>Alasan: Hujan cukup ({rain_mm}mm ≥ {daily_need:.1f}mm)</small></p>
                    </div>
                    """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error mengambil data cuaca: {str(e)}")
        st.info("Menampilkan simulasi jadwal irigasi...")
    
    st.markdown("### 💡 Tips Irigasi")
    st.info("""
    - ⏰ **Waktu Terbaik**: Pagi (6-8 AM) atau Sore (4-6 PM)
    - 🌡️ **Hindari**: Siang hari (evaporasi tinggi)
    - 💧 **Metode**: Irigasi tetes lebih efisien dari sprinkler
    - 📊 **Monitor**: Cek kelembaban tanah sebelum irigasi
    """)


# ===== TAB 3: DRIP IRRIGATION ROI =====
with tab3:
    st.subheader("🏗️ Simulasi Investasi Irigasi Tetes")
    
    col_d1, col_d2 = st.columns(2)
    
    with col_d1:
        st.markdown("### 📋 Input Investasi")
        
        area_drip = st.number_input(
            "Luas Lahan (ha)",
            min_value=0.1,
            max_value=50.0,
            value=1.0,
            step=0.5,
            key="drip_area"
        )
        
        investment_per_ha = st.number_input(
            "Biaya per Hektar (Rp)",
            min_value=5000000,
            max_value=30000000,
            value=15000000,
            step=1000000,
            help="Biaya instalasi irigasi tetes per hektar"
        )
        
        water_saved_pct = st.slider(
            "Penghematan Air (%)",
            min_value=20,
            max_value=70,
            value=40,
            help="Estimasi penghematan air dengan irigasi tetes"
        )
    
    with col_d2:
        st.markdown("### 💡 Info Irigasi Tetes")
        
        st.info("""
        **Keuntungan Irigasi Tetes:**
        
        ✅ Hemat air 40-60%
        ✅ Hemat pupuk 30-50%
        ✅ Yield meningkat 15-25%
        ✅ Gulma berkurang
        ✅ Penyakit tanah ↓
        
        **Cocok untuk:**
        - Cabai, Tomat, Terong
        - Melon, Semangka
        - Strawberry, Paprika
        - Tanaman greenhouse
        """)
    
    if st.button("💰 Hitung ROI", type="primary", use_container_width=True):
        result_roi = calc.calculate_drip_irrigation_roi(area_drip, water_saved_pct, investment_per_ha)
        
        st.markdown("---")
        st.markdown("### 📊 Analisis ROI")
        
        col_roi1, col_roi2, col_roi3, col_roi4 = st.columns(4)
        
        with col_roi1:
            st.metric(
                "Total Investasi",
                f"Rp {result_roi['investment']:,.0f}",
                f"{area_drip} ha"
            )
        
        with col_roi2:
            st.metric(
                "Penghematan/Tahun",
                f"Rp {result_roi['annual_cost_savings']:,.0f}",
                f"{result_roi['annual_water_saved_m3']:,.0f} m³"
            )
        
        with col_roi3:
            st.metric(
                "Payback Period",
                f"{result_roi['payback_years']:.1f} tahun",
                "Break-even point"
            )
        
        with col_roi4:
            st.metric(
                "ROI (5 Tahun)",
                f"{result_roi['roi_5_years_pct']:.0f}%",
                "Return on Investment"
            )
        
        # Additional benefits
        st.markdown("### 💰 Manfaat Tambahan")
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            st.success(f"""
            **📈 Peningkatan Yield**
            - Estimasi: +{result_roi['yield_increase_pct']}%
            - Kualitas produk lebih baik
            - Ukuran lebih seragam
            """)
        
        with col_b2:
            st.success("""
            **🌱 Manfaat Lain**
            - Hemat tenaga kerja
            - Pupuk lebih efisien (fertigation)
            - Penyakit tanah berkurang
            - Umur sistem: 5-10 tahun
            """)


# ===== TAB 4: PANDUAN =====
with tab4:
    st.subheader("📚 Panduan Water Management")
    
    with st.expander("💧 Apa itu Water Footprint?"):
        st.markdown("""
        **Water Footprint** adalah total volume air yang digunakan untuk memproduksi barang atau jasa.
        
        Untuk pertanian, water footprint dihitung dari:
        - **Blue Water**: Air irigasi (dari sungai, sumur)
        - **Green Water**: Air hujan yang diserap tanaman
        - **Grey Water**: Air yang tercemar (pupuk, pestisida)
        
        **Contoh:**
        - 1 kg Padi = 2,500 L air
        - 1 kg Jagung = 900 L air
        - 1 kg Tomat = 400 L air
        
        **Mengapa Penting?**
        - Krisis air global
        - Efisiensi produksi
        - Sertifikasi (Water Stewardship)
        """)
    
    with st.expander("🚿 Jenis-Jenis Irigasi"):
        st.markdown("""
        **1. Irigasi Permukaan (Surface)**
        - Genangan/banjir (padi sawah)
        - Efisiensi: 40-60%
        - Biaya: Rendah
        
        **2. Irigasi Sprinkler**
        - Penyiraman seperti hujan
        - Efisiensi: 60-75%
        - Biaya: Sedang
        
        **3. Irigasi Tetes (Drip)**
        - Air langsung ke akar
        - Efisiensi: 85-95%
        - Biaya: Tinggi (ROI bagus)
        
        **4. Irigasi Bawah Permukaan (Subsurface)**
        - Pipa di bawah tanah
        - Efisiensi: 90-95%
        - Biaya: Sangat tinggi
        """)
    
    with st.expander("📊 Cara Menghemat Air"):
        st.markdown("""
        **Teknik Penghematan Air:**
        
        1. **Mulching** (Penutup Tanah)
           - Kurangi evaporasi 25-35%
           - Bahan: Jerami, plastik, kompos
        
        2. **Irigasi Tetes**
           - Hemat 40-60%
           - Tepat sasaran ke akar
        
        3. **Jadwal Irigasi Tepat**
           - Pagi/sore (evaporasi rendah)
           - Sesuai kebutuhan tanaman
        
        4. **Varietas Hemat Air**
           - Drought-tolerant varieties
           - Sistem perakaran dalam
        
        5. **Rainwater Harvesting**
           - Tampung air hujan
           - Gunakan saat kemarau
        
        6. **Soil Improvement**
           - Tambah bahan organik
           - Retensi air lebih baik
        """)
    
    with st.expander("🌧️ Rainwater Harvesting"):
        st.markdown("""
        **Sistem Penampungan Air Hujan:**
        
        **Komponen:**
        1. Catchment area (atap, lahan)
        2. Gutter (talang)
        3. First flush (pembuangan air awal)
        4. Storage tank (tangki)
        5. Distribution system
        
        **Perhitungan Kapasitas:**
        - Luas atap 100 m²
        - Curah hujan 2000 mm/tahun
        - Potensi: 100 × 2 × 0.8 = 160 m³/tahun
        
        **Biaya:**
        - Tangki 5 m³: Rp 7-10 juta
        - Tangki 10 m³: Rp 12-15 juta
        - ROI: 3-5 tahun
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p>💧 <strong>AgriSensa Smart Water Management</strong></p>
    <p>Hemat Air, Tingkatkan Hasil</p>
    <p><small>Powered by FAO Crop Water Requirements | Weather Data: BMKG/OpenWeatherMap</small></p>
</div>
""", unsafe_allow_html=True)
