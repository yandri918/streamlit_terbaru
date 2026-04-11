"""
 Varietas Padi - Rice Varieties Database
Comprehensive database of Indonesian rice varieties with comparison tools
"""

import streamlit as st
import pandas as pd
import altair as alt
from data.rice_varieties import RICE_VARIETIES, get_all_varieties, get_varieties_by_region, compare_varieties

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

# Page config
st.set_page_config(
    page_title="Varietas Padi",
    page_icon="",
    layout="wide"
)

# Apply Design System
apply_design_system()

# Header
st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('seedling', size='lg')} Varietas Padi</h1>", unsafe_allow_html=True)
st.markdown("**Database lengkap varietas padi unggul untuk kondisi Indonesia**")
st.markdown("---")

# Tabs
tab1, tab2, tab3 = st.tabs([" Database Varietas", " Pencarian & Filter", " Perbandingan"])

# TAB 1: Database
with tab1:
    st.header(" Database Varietas Padi")
    
    # Display all varieties
    for variety_name, variety_data in RICE_VARIETIES.items():
        with st.expander(f" {variety_data['name']}", expanded=False):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("### Informasi Dasar")
                st.write(f"**Tipe:** {variety_data['type']}")
                st.write(f"**Umur:** {variety_data['duration']} hari")
                st.write(f"**Potensi Hasil:** {variety_data['yield_potential']} ton/ha")
                st.write(f"**Tipe Gabah:** {variety_data['grain_type']}")
                st.write(f"**Kualitas:** {variety_data['grain_quality']}")
            
            with col2:
                st.markdown("### Ketahanan")
                st.write(f"**Wereng Coklat:** {variety_data['resistance']['wereng_coklat']}")
                st.write(f"**Blast:** {variety_data['resistance']['blast']}")
                st.write(f"**Hawar Daun:** {variety_data['resistance']['hawar_daun']}")
                
                st.markdown("### Kebutuhan")
                st.write(f"**Air:** {variety_data['water_requirement']}")
                st.write(f"**Respon Pupuk:** {variety_data['fertilizer_response']}")
            
            with col3:
                st.markdown("### Adaptasi")
                st.write(f"**Region:** {', '.join(variety_data['suitable_regions'])}")
                st.write(f"**Musim:** {', '.join(variety_data['suitable_seasons'])}")
                
                st.markdown("### Harga Pasar")
                st.write(f"**Range:** Rp {variety_data['price_range'][0]:,} - Rp {variety_data['price_range'][1]:,}/kg")
            
            st.info(f"**Karakteristik:** {variety_data['characteristics']}")

# TAB 2: Search & Filter
with tab2:
    st.header(" Pencarian & Filter Varietas")
    
    col_filter1, col_filter2 = st.columns(2)
    
    with col_filter1:
        # Region filter
        st.subheader("Filter berdasarkan Region")
        regions = ['Semua', 'Jawa', 'Sumatera', 'Sulawesi', 'Bali', 'NTB', 'Papua', 'Maluku']
        selected_region = st.selectbox("Pilih Region", regions)
        
        if selected_region != 'Semua':
            filtered_varieties = get_varieties_by_region(selected_region)
            st.success(f"Ditemukan {len(filtered_varieties)} varietas untuk region {selected_region}")
            
            for name, data in filtered_varieties.items():
                st.markdown(f"""
                <div style='padding: 10px; background-color: #F1F8E9; border-left: 4px solid #2E7D32; margin: 5px 0;'>
                    <strong>{data['name']}</strong> - {data['duration']} hari, {data['yield_potential']} ton/ha
                </div>
                """, unsafe_allow_html=True)
    
    with col_filter2:
        # Duration filter
        st.subheader("Filter berdasarkan Umur Tanam")
        min_days = st.number_input("Minimal (hari)", min_value=100, max_value=130, value=110)
        max_days = st.number_input("Maksimal (hari)", min_value=100, max_value=130, value=125)
        
        filtered_by_duration = {
            name: data for name, data in RICE_VARIETIES.items()
            if min_days <= data['duration'] <= max_days
        }
        
        st.success(f"Ditemukan {len(filtered_by_duration)} varietas dengan umur {min_days}-{max_days} hari")
        
        for name, data in filtered_by_duration.items():
            st.markdown(f"""
            <div style='padding: 10px; background-color: #E8F5E9; border-left: 4px solid #558B2F; margin: 5px 0;'>
                <strong>{data['name']}</strong> - {data['duration']} hari
            </div>
            """, unsafe_allow_html=True)

# TAB 3: Comparison
with tab3:
    st.header(" Perbandingan Varietas")
    
    # Select varieties to compare
    st.subheader("Pilih Varietas untuk Dibandingkan")
    all_varieties = get_all_varieties()
    selected_varieties = st.multiselect(
        "Pilih 2-5 varietas",
        all_varieties,
        default=all_varieties[:3]
    )
    
    if len(selected_varieties) >= 2:
        comparison_data = compare_varieties(selected_varieties)
        
        # Create comparison dataframe
        comparison_df = pd.DataFrame({
            'Varietas': [data['name'] for data in comparison_data.values()],
            'Umur (hari)': [data['duration'] for data in comparison_data.values()],
            'Potensi Hasil (ton/ha)': [data['yield_potential'] for data in comparison_data.values()],
            'Kualitas': [data['grain_quality'] for data in comparison_data.values()],
            'Harga Min (Rp/kg)': [data['price_range'][0] for data in comparison_data.values()],
            'Harga Max (Rp/kg)': [data['price_range'][1] for data in comparison_data.values()],
        })
        
        # Display table
        st.subheader("Tabel Perbandingan")
        st.dataframe(comparison_df, use_container_width=True, hide_index=True)
        
        # Altair charts
        st.subheader(" Visualisasi Perbandingan")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Yield comparison
            yield_chart = alt.Chart(comparison_df).mark_bar().encode(
                x=alt.X('Varietas:N', title='Varietas'),
                y=alt.Y('Potensi Hasil (ton/ha):Q', title='Potensi Hasil (ton/ha)'),
                color=alt.Color('Varietas:N', legend=None),
                tooltip=['Varietas', 'Potensi Hasil (ton/ha)', 'Umur (hari)']
            ).properties(
                title='Perbandingan Potensi Hasil',
                height=400
            ).interactive()
            
            st.altair_chart(yield_chart, use_container_width=True)
        
        with col_chart2:
            # Duration comparison
            duration_chart = alt.Chart(comparison_df).mark_bar().encode(
                x=alt.X('Varietas:N', title='Varietas'),
                y=alt.Y('Umur (hari):Q', title='Umur Tanam (hari)'),
                color=alt.Color('Varietas:N', legend=None),
                tooltip=['Varietas', 'Umur (hari)', 'Potensi Hasil (ton/ha)']
            ).properties(
                title='Perbandingan Umur Tanam',
                height=400
            ).interactive()
            
            st.altair_chart(duration_chart, use_container_width=True)
        
        # Price range chart
        st.subheader(" Perbandingan Harga Pasar")
        
        price_chart = alt.Chart(comparison_df).mark_bar().encode(
            x=alt.X('Varietas:N', title='Varietas'),
            y=alt.Y('Harga Min (Rp/kg):Q', title='Harga (Rp/kg)'),
            y2='Harga Max (Rp/kg):Q',
            color=alt.Color('Varietas:N', legend=None),
            tooltip=['Varietas', 'Harga Min (Rp/kg)', 'Harga Max (Rp/kg)']
        ).properties(
            title='Range Harga Pasar',
            height=400
        ).interactive()
        
        st.altair_chart(price_chart, use_container_width=True)
        
        # Detailed comparison
        st.subheader(" Perbandingan Detail")
        
        for variety_name in selected_varieties:
            variety_data = RICE_VARIETIES[variety_name]
            
            with st.expander(f" {variety_data['name']}", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Ketahanan Hama/Penyakit:**")
                    st.write(f"- Wereng Coklat: {variety_data['resistance']['wereng_coklat']}")
                    st.write(f"- Blast: {variety_data['resistance']['blast']}")
                    st.write(f"- Hawar Daun: {variety_data['resistance']['hawar_daun']}")
                
                with col2:
                    st.markdown("**Adaptasi:**")
                    st.write(f"- Region: {', '.join(variety_data['suitable_regions'])}")
                    st.write(f"- Kebutuhan Air: {variety_data['water_requirement']}")
                    st.write(f"- Respon Pupuk: {variety_data['fertilizer_response']}")
                
                st.info(f"**Karakteristik:** {variety_data['characteristics']}")
    
    else:
        st.warning("Pilih minimal 2 varietas untuk perbandingan")

# Footer
st.markdown("---")
st.info("""
 **Tips Memilih Varietas:**
1. Sesuaikan dengan kondisi lahan dan iklim regional
2. Pertimbangkan umur tanam untuk pola tanam yang diinginkan
3. Pilih varietas dengan ketahanan terhadap hama/penyakit lokal
4. Perhatikan preferensi pasar untuk kualitas gabah
5. Konsultasikan dengan penyuluh pertanian setempat
""")
