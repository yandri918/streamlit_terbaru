import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Visualisasi Data Altair", page_icon="📊", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 1rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        color: white;
        margin: 1rem 0;
    }
    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>📊 Visualisasi Data Altair</h1>
    <p>Contoh Penggunaan Library Altair untuk Analisis Data Pertanian</p>
</div>
""", unsafe_allow_html=True)

# Introduction
st.markdown("""
### 🎯 Tentang Modul Ini

Modul ini mendemonstrasikan berbagai kemampuan **Altair** - library visualisasi data deklaratif yang powerful untuk Python.
Altair menggunakan grammar of graphics dan menghasilkan visualisasi interaktif yang indah dengan kode yang minimal.

**Keunggulan Altair:**
- 🎨 Sintaks yang bersih dan intuitif
- 🔄 Interaktivitas built-in (zoom, pan, tooltips)
- 📱 Responsive dan modern
- 🔗 Mudah di-embed di Streamlit
- 📊 Mendukung berbagai jenis chart
""")

# Tabs for different chart types
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📈 Line Chart", 
    "📊 Bar Chart", 
    "🔵 Scatter Plot", 
    "📉 Area Chart", 
    "🔥 Heatmap",
    "🎯 Multi-View Dashboard",
    "📚 Tutorial"
])

# ============================================================================
# TAB 1: LINE CHART - Trend Hasil Panen
# ============================================================================
with tab1:
    st.markdown("### 📈 Line Chart: Trend Hasil Panen Bulanan")
    
    st.markdown("""
    **Use Case:** Memvisualisasikan tren hasil panen dari waktu ke waktu untuk berbagai komoditas.
    
    **Fitur Interaktif:**
    - Hover untuk melihat detail data
    - Zoom dengan scroll
    - Pan dengan drag
    """)
    
    # Generate sample data
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2025-12-31', freq='M')
    
    data_line = pd.DataFrame({
        'Bulan': dates,
        'Cabai': 2000 + np.cumsum(np.random.randn(len(dates)) * 100),
        'Tomat': 1500 + np.cumsum(np.random.randn(len(dates)) * 80),
        'Terong': 1200 + np.cumsum(np.random.randn(len(dates)) * 60),
    })
    
    # Melt data for Altair
    data_line_melted = data_line.melt('Bulan', var_name='Komoditas', value_name='Hasil Panen (kg)')
    
    # Create interactive line chart
    line_chart = alt.Chart(data_line_melted).mark_line(point=True).encode(
        x=alt.X('Bulan:T', title='Bulan', axis=alt.Axis(format='%b %Y')),
        y=alt.Y('Hasil Panen (kg):Q', title='Hasil Panen (kg)', scale=alt.Scale(zero=False)),
        color=alt.Color('Komoditas:N', 
                       scale=alt.Scale(scheme='category10'),
                       legend=alt.Legend(title='Komoditas')),
        tooltip=[
            alt.Tooltip('Bulan:T', title='Bulan', format='%B %Y'),
            alt.Tooltip('Komoditas:N', title='Komoditas'),
            alt.Tooltip('Hasil Panen (kg):Q', title='Hasil Panen', format=',.0f')
        ]
    ).properties(
        width=800,
        height=400,
        title='Trend Hasil Panen Bulanan (2023-2025)'
    ).interactive()
    
    st.altair_chart(line_chart, use_container_width=True)
    
    # Show code
    with st.expander("📝 Lihat Kode"):
        st.code("""
# Create interactive line chart
line_chart = alt.Chart(data).mark_line(point=True).encode(
    x=alt.X('Bulan:T', title='Bulan'),
    y=alt.Y('Hasil Panen (kg):Q', title='Hasil Panen (kg)'),
    color=alt.Color('Komoditas:N', scale=alt.Scale(scheme='category10')),
    tooltip=['Bulan:T', 'Komoditas:N', 'Hasil Panen (kg):Q']
).properties(
    width=800,
    height=400,
    title='Trend Hasil Panen Bulanan'
).interactive()

st.altair_chart(line_chart, use_container_width=True)
        """, language='python')

# ============================================================================
# TAB 2: BAR CHART - Perbandingan Produksi
# ============================================================================
with tab2:
    st.markdown("### 📊 Bar Chart: Perbandingan Produksi Antar Wilayah")
    
    st.markdown("""
    **Use Case:** Membandingkan produksi pertanian antar wilayah atau periode.
    
    **Fitur:**
    - Grouped bar chart untuk perbandingan multi-kategori
    - Color encoding untuk kategori
    - Interactive tooltips
    """)
    
    # Sample data
    data_bar = pd.DataFrame({
        'Wilayah': ['Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Sumatra Utara', 'Sulawesi Selatan'] * 3,
        'Komoditas': ['Padi'] * 5 + ['Jagung'] * 5 + ['Kedelai'] * 5,
        'Produksi (ton)': [
            12000, 11500, 13000, 9500, 8000,  # Padi
            8000, 7500, 9000, 6500, 5500,      # Jagung
            3000, 3500, 4000, 2500, 2000       # Kedelai
        ]
    })
    
    # Create grouped bar chart
    bar_chart = alt.Chart(data_bar).mark_bar().encode(
        x=alt.X('Wilayah:N', title='Wilayah', axis=alt.Axis(labelAngle=-45)),
        y=alt.Y('Produksi (ton):Q', title='Produksi (ton)'),
        color=alt.Color('Komoditas:N', 
                       scale=alt.Scale(scheme='tableau10'),
                       legend=alt.Legend(title='Komoditas')),
        xOffset='Komoditas:N',
        tooltip=[
            alt.Tooltip('Wilayah:N', title='Wilayah'),
            alt.Tooltip('Komoditas:N', title='Komoditas'),
            alt.Tooltip('Produksi (ton):Q', title='Produksi', format=',.0f')
        ]
    ).properties(
        width=800,
        height=400,
        title='Perbandingan Produksi Antar Wilayah'
    )
    
    st.altair_chart(bar_chart, use_container_width=True)
    
    # Show statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Produksi", f"{data_bar['Produksi (ton)'].sum():,.0f} ton")
    with col2:
        top_region = data_bar.groupby('Wilayah')['Produksi (ton)'].sum().idxmax()
        st.metric("Wilayah Tertinggi", top_region)
    with col3:
        avg_production = data_bar['Produksi (ton)'].mean()
        st.metric("Rata-rata Produksi", f"{avg_production:,.0f} ton")
    
    with st.expander("📝 Lihat Kode"):
        st.code("""
bar_chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('Wilayah:N', title='Wilayah'),
    y=alt.Y('Produksi (ton):Q', title='Produksi (ton)'),
    color=alt.Color('Komoditas:N', scale=alt.Scale(scheme='tableau10')),
    xOffset='Komoditas:N',  # Untuk grouped bar
    tooltip=['Wilayah:N', 'Komoditas:N', 'Produksi (ton):Q']
).properties(
    width=800,
    height=400,
    title='Perbandingan Produksi Antar Wilayah'
)
        """, language='python')

# ============================================================================
# TAB 3: SCATTER PLOT - Analisis Korelasi
# ============================================================================
with tab3:
    st.markdown("### 🔵 Scatter Plot: Analisis Korelasi Pupuk vs Hasil Panen")
    
    st.markdown("""
    **Use Case:** Menganalisis hubungan antara input (pupuk) dan output (hasil panen).
    
    **Fitur:**
    - Scatter plot dengan regression line
    - Size encoding untuk variabel ketiga
    - Color encoding untuk kategori
    """)
    
    # Generate sample data
    np.random.seed(123)
    n_samples = 100
    
    data_scatter = pd.DataFrame({
        'Pupuk NPK (kg/ha)': np.random.uniform(100, 400, n_samples),
        'Hasil Panen (ton/ha)': np.random.uniform(3, 8, n_samples),
        'Luas Lahan (ha)': np.random.uniform(0.5, 5, n_samples),
        'Jenis Tanah': np.random.choice(['Aluvial', 'Latosol', 'Andosol'], n_samples)
    })
    
    # Add correlation
    data_scatter['Hasil Panen (ton/ha)'] = (
        2 + 0.015 * data_scatter['Pupuk NPK (kg/ha)'] + 
        np.random.randn(n_samples) * 0.5
    )
    
    # Create scatter plot with regression
    scatter_base = alt.Chart(data_scatter).mark_circle().encode(
        x=alt.X('Pupuk NPK (kg/ha):Q', title='Pupuk NPK (kg/ha)', scale=alt.Scale(zero=False)),
        y=alt.Y('Hasil Panen (ton/ha):Q', title='Hasil Panen (ton/ha)', scale=alt.Scale(zero=False)),
        size=alt.Size('Luas Lahan (ha):Q', 
                     scale=alt.Scale(range=[50, 500]),
                     legend=alt.Legend(title='Luas Lahan (ha)')),
        color=alt.Color('Jenis Tanah:N', 
                       scale=alt.Scale(scheme='set2'),
                       legend=alt.Legend(title='Jenis Tanah')),
        tooltip=[
            alt.Tooltip('Pupuk NPK (kg/ha):Q', title='Pupuk NPK', format='.1f'),
            alt.Tooltip('Hasil Panen (ton/ha):Q', title='Hasil Panen', format='.2f'),
            alt.Tooltip('Luas Lahan (ha):Q', title='Luas Lahan', format='.2f'),
            alt.Tooltip('Jenis Tanah:N', title='Jenis Tanah')
        ]
    ).properties(
        width=800,
        height=400,
        title='Korelasi Pupuk NPK vs Hasil Panen'
    )
    
    # Add regression line
    regression = scatter_base.transform_regression(
        'Pupuk NPK (kg/ha)', 'Hasil Panen (ton/ha)'
    ).mark_line(color='red', strokeDash=[5, 5])
    
    scatter_chart = (scatter_base + regression).interactive()
    
    st.altair_chart(scatter_chart, use_container_width=True)
    
    # Calculate correlation
    correlation = data_scatter['Pupuk NPK (kg/ha)'].corr(data_scatter['Hasil Panen (ton/ha)'])
    
    st.info(f"📊 **Korelasi Pearson:** {correlation:.3f} - Menunjukkan korelasi {'positif kuat' if correlation > 0.7 else 'positif sedang' if correlation > 0.4 else 'lemah'} antara pupuk NPK dan hasil panen.")
    
    with st.expander("📝 Lihat Kode"):
        st.code("""
# Scatter plot
scatter_base = alt.Chart(data).mark_circle().encode(
    x=alt.X('Pupuk NPK (kg/ha):Q'),
    y=alt.Y('Hasil Panen (ton/ha):Q'),
    size=alt.Size('Luas Lahan (ha):Q'),
    color=alt.Color('Jenis Tanah:N'),
    tooltip=['Pupuk NPK (kg/ha):Q', 'Hasil Panen (ton/ha):Q', 'Jenis Tanah:N']
)

# Regression line
regression = scatter_base.transform_regression(
    'Pupuk NPK (kg/ha)', 'Hasil Panen (ton/ha)'
).mark_line(color='red', strokeDash=[5, 5])

chart = (scatter_base + regression).interactive()
        """, language='python')

# ============================================================================
# TAB 4: AREA CHART - Pola Musiman
# ============================================================================
with tab4:
    st.markdown("### 📉 Area Chart: Pola Musiman Curah Hujan & Produksi")
    
    st.markdown("""
    **Use Case:** Menampilkan pola musiman dan tren kumulatif.
    
    **Fitur:**
    - Stacked area chart
    - Normalized area chart
    - Time series analysis
    """)
    
    # Generate seasonal data
    months = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    
    data_area = pd.DataFrame({
        'Bulan': months,
        'Curah Hujan (mm)': [250, 280, 200, 150, 100, 80, 60, 50, 70, 120, 180, 230],
        'Produksi Padi (ton)': [800, 850, 900, 950, 1000, 1050, 1100, 1150, 1100, 1000, 900, 850],
        'Produksi Jagung (ton)': [400, 450, 500, 550, 600, 650, 700, 750, 700, 600, 500, 450],
    })
    
    # Melt for stacked area
    data_area_melted = data_area.melt('Bulan', 
                                      value_vars=['Produksi Padi (ton)', 'Produksi Jagung (ton)'],
                                      var_name='Komoditas', 
                                      value_name='Produksi (ton)')
    
    # Create stacked area chart
    area_chart = alt.Chart(data_area_melted).mark_area(opacity=0.7).encode(
        x=alt.X('Bulan:T', title='Bulan', axis=alt.Axis(format='%b')),
        y=alt.Y('Produksi (ton):Q', title='Produksi (ton)', stack='zero'),
        color=alt.Color('Komoditas:N', 
                       scale=alt.Scale(scheme='tableau10'),
                       legend=alt.Legend(title='Komoditas')),
        tooltip=[
            alt.Tooltip('Bulan:T', title='Bulan', format='%B %Y'),
            alt.Tooltip('Komoditas:N', title='Komoditas'),
            alt.Tooltip('Produksi (ton):Q', title='Produksi', format=',.0f')
        ]
    ).properties(
        width=800,
        height=300,
        title='Produksi Bulanan (Stacked Area)'
    )
    
    # Create rainfall line overlay
    rainfall_line = alt.Chart(data_area).mark_line(
        color='#3b82f6',
        strokeWidth=3,
        point=alt.OverlayMarkDef(filled=False, fill='white', size=100)
    ).encode(
        x=alt.X('Bulan:T'),
        y=alt.Y('Curah Hujan (mm):Q', 
               title='Curah Hujan (mm)',
               axis=alt.Axis(titleColor='#3b82f6')),
        tooltip=[
            alt.Tooltip('Bulan:T', title='Bulan', format='%B'),
            alt.Tooltip('Curah Hujan (mm):Q', title='Curah Hujan', format='.0f')
        ]
    ).properties(
        width=800,
        height=300,
        title='Curah Hujan Bulanan'
    )
    
    st.altair_chart(area_chart, use_container_width=True)
    st.altair_chart(rainfall_line.interactive(), use_container_width=True)
    
    with st.expander("📝 Lihat Kode"):
        st.code("""
# Stacked area chart
area_chart = alt.Chart(data).mark_area(opacity=0.7).encode(
    x=alt.X('Bulan:T', title='Bulan'),
    y=alt.Y('Produksi (ton):Q', stack='zero'),  # stack='zero' untuk stacked
    color=alt.Color('Komoditas:N'),
    tooltip=['Bulan:T', 'Komoditas:N', 'Produksi (ton):Q']
).properties(
    title='Produksi Bulanan (Stacked Area)'
)

# Line chart overlay
line = alt.Chart(data).mark_line().encode(
    x='Bulan:T',
    y='Curah Hujan (mm):Q'
)
        """, language='python')

# ============================================================================
# TAB 5: HEATMAP - Analisis Nutrisi Tanah
# ============================================================================
with tab5:
    st.markdown("### 🔥 Heatmap: Analisis Nutrisi Tanah Per Zona")
    
    st.markdown("""
    **Use Case:** Visualisasi distribusi nutrisi tanah di berbagai zona lahan.
    
    **Fitur:**
    - Color gradient untuk nilai
    - Grid layout
    - Interactive tooltips
    """)
    
    # Generate heatmap data
    zones = [f'Zona {i}' for i in range(1, 11)]
    nutrients = ['N (ppm)', 'P (ppm)', 'K (ppm)', 'pH', 'C-Organik (%)']
    
    data_heatmap = []
    for zone in zones:
        for nutrient in nutrients:
            if nutrient == 'pH':
                value = np.random.uniform(5.5, 7.5)
            elif nutrient == 'C-Organik (%)':
                value = np.random.uniform(1.5, 4.5)
            else:
                value = np.random.uniform(20, 100)
            
            data_heatmap.append({
                'Zona': zone,
                'Nutrisi': nutrient,
                'Nilai': value
            })
    
    data_heatmap = pd.DataFrame(data_heatmap)
    
    # Create heatmap
    heatmap = alt.Chart(data_heatmap).mark_rect().encode(
        x=alt.X('Zona:N', title='Zona Lahan'),
        y=alt.Y('Nutrisi:N', title='Parameter'),
        color=alt.Color('Nilai:Q', 
                       scale=alt.Scale(scheme='viridis'),
                       legend=alt.Legend(title='Nilai')),
        tooltip=[
            alt.Tooltip('Zona:N', title='Zona'),
            alt.Tooltip('Nutrisi:N', title='Parameter'),
            alt.Tooltip('Nilai:Q', title='Nilai', format='.2f')
        ]
    ).properties(
        width=800,
        height=300,
        title='Heatmap Nutrisi Tanah Per Zona'
    )
    
    st.altair_chart(heatmap, use_container_width=True)
    
    # Summary statistics
    st.markdown("#### 📊 Statistik Ringkasan")
    col1, col2 = st.columns(2)
    
    with col1:
        summary_stats = data_heatmap.groupby('Nutrisi')['Nilai'].agg(['mean', 'min', 'max']).round(2)
        st.dataframe(summary_stats, use_container_width=True)
    
    with col2:
        # Bar chart of averages
        avg_chart = alt.Chart(data_heatmap).mark_bar().encode(
            x=alt.X('mean(Nilai):Q', title='Rata-rata Nilai'),
            y=alt.Y('Nutrisi:N', title='Parameter'),
            color=alt.Color('Nutrisi:N', legend=None),
            tooltip=[
                alt.Tooltip('Nutrisi:N', title='Parameter'),
                alt.Tooltip('mean(Nilai):Q', title='Rata-rata', format='.2f')
            ]
        ).properties(
            height=250,
            title='Rata-rata Nilai Per Parameter'
        )
        st.altair_chart(avg_chart, use_container_width=True)
    
    with st.expander("📝 Lihat Kode"):
        st.code("""
heatmap = alt.Chart(data).mark_rect().encode(
    x=alt.X('Zona:N', title='Zona Lahan'),
    y=alt.Y('Nutrisi:N', title='Parameter'),
    color=alt.Color('Nilai:Q', 
                   scale=alt.Scale(scheme='viridis'),
                   legend=alt.Legend(title='Nilai')),
    tooltip=['Zona:N', 'Nutrisi:N', 'Nilai:Q']
).properties(
    width=800,
    height=300,
    title='Heatmap Nutrisi Tanah Per Zona'
)
        """, language='python')

# ============================================================================
# TAB 6: MULTI-VIEW DASHBOARD
# ============================================================================
with tab6:
    st.markdown("### 🎯 Multi-View Dashboard: Analisis Komprehensif")
    
    st.markdown("""
    **Use Case:** Dashboard interaktif dengan multiple linked views.
    
    **Fitur:**
    - Linked selection across charts
    - Brushing and linking
    - Coordinated views
    """)
    
    # Generate comprehensive data
    np.random.seed(456)
    n = 200
    
    data_dashboard = pd.DataFrame({
        'Tanggal': pd.date_range(start='2024-01-01', periods=n, freq='D'),
        'Suhu (°C)': np.random.uniform(25, 35, n),
        'Kelembaban (%)': np.random.uniform(60, 90, n),
        'Hasil Panen (kg)': np.random.uniform(100, 300, n),
        'Wilayah': np.random.choice(['Utara', 'Selatan', 'Timur', 'Barat'], n),
        'Komoditas': np.random.choice(['Cabai', 'Tomat', 'Terong'], n)
    })
    
    # Create selection
    brush = alt.selection_interval(encodings=['x'])
    
    # Chart 1: Time series with brush
    time_series = alt.Chart(data_dashboard).mark_line(point=True).encode(
        x=alt.X('Tanggal:T', title='Tanggal'),
        y=alt.Y('Hasil Panen (kg):Q', title='Hasil Panen (kg)'),
        color=alt.condition(brush, 'Komoditas:N', alt.value('lightgray')),
        tooltip=['Tanggal:T', 'Hasil Panen (kg):Q', 'Komoditas:N']
    ).properties(
        width=800,
        height=200,
        title='Hasil Panen Harian (Pilih area untuk filter)'
    ).add_params(brush)
    
    # Chart 2: Histogram filtered by brush
    histogram = alt.Chart(data_dashboard).mark_bar().encode(
        x=alt.X('Hasil Panen (kg):Q', bin=alt.Bin(maxbins=30), title='Hasil Panen (kg)'),
        y=alt.Y('count():Q', title='Frekuensi'),
        color=alt.Color('Komoditas:N', legend=alt.Legend(title='Komoditas'))
    ).transform_filter(
        brush
    ).properties(
        width=380,
        height=250,
        title='Distribusi Hasil Panen (Filtered)'
    )
    
    # Chart 3: Scatter plot filtered by brush
    scatter = alt.Chart(data_dashboard).mark_circle(size=60).encode(
        x=alt.X('Suhu (°C):Q', title='Suhu (°C)', scale=alt.Scale(zero=False)),
        y=alt.Y('Kelembaban (%):Q', title='Kelembaban (%)', scale=alt.Scale(zero=False)),
        color=alt.Color('Komoditas:N', legend=alt.Legend(title='Komoditas')),
        tooltip=['Suhu (°C):Q', 'Kelembaban (%):Q', 'Hasil Panen (kg):Q', 'Komoditas:N']
    ).transform_filter(
        brush
    ).properties(
        width=380,
        height=250,
        title='Suhu vs Kelembaban (Filtered)'
    )
    
    # Combine charts
    dashboard = alt.vconcat(
        time_series,
        alt.hconcat(histogram, scatter)
    )
    
    st.altair_chart(dashboard, use_container_width=True)
    
    st.info("💡 **Tip:** Klik dan drag pada chart atas untuk memilih periode waktu. Chart di bawah akan otomatis ter-filter!")
    
    with st.expander("📝 Lihat Kode"):
        st.code("""
# Create interactive selection
brush = alt.selection_interval(encodings=['x'])

# Main chart with brush
main_chart = alt.Chart(data).mark_line().encode(
    x='Tanggal:T',
    y='Hasil Panen (kg):Q',
    color=alt.condition(brush, 'Komoditas:N', alt.value('lightgray'))
).add_params(brush)

# Filtered chart
filtered_chart = alt.Chart(data).mark_bar().encode(
    x=alt.X('Hasil Panen (kg):Q', bin=True),
    y='count():Q'
).transform_filter(brush)  # Filter berdasarkan brush

# Combine
dashboard = alt.vconcat(main_chart, filtered_chart)
        """, language='python')

# ============================================================================
# TAB 7: TUTORIAL
# ============================================================================
with tab7:
    st.markdown("### 📚 Tutorial Altair untuk Pemula")
    
    st.markdown("""
    ## 🎓 Pengenalan Altair
    
    **Altair** adalah library visualisasi data Python yang menggunakan **Vega-Lite** grammar of graphics.
    
    ### 📦 Instalasi
    ```bash
    pip install altair
    ```
    
    ### 🔰 Konsep Dasar
    
    Altair menggunakan pendekatan **deklaratif** - Anda mendeskripsikan **apa** yang ingin divisualisasikan,
    bukan **bagaimana** cara membuatnya.
    
    #### Struktur Dasar:
    """)
    
    st.code("""
import altair as alt
import pandas as pd

# 1. Siapkan data
data = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 6, 8, 10]
})

# 2. Buat chart
chart = alt.Chart(data).mark_point().encode(
    x='x:Q',  # Q = Quantitative (numerik)
    y='y:Q'
)

# 3. Tampilkan
chart.show()  # Atau st.altair_chart(chart) di Streamlit
    """, language='python')
    
    st.markdown("""
    ### 🎨 Jenis Mark (Tipe Visualisasi)
    
    | Mark | Fungsi | Use Case |
    |------|--------|----------|
    | `mark_point()` | Scatter plot | Korelasi, distribusi |
    | `mark_line()` | Line chart | Trend, time series |
    | `mark_bar()` | Bar chart | Perbandingan kategori |
    | `mark_area()` | Area chart | Kumulatif, komposisi |
    | `mark_rect()` | Heatmap | Matrix, grid data |
    | `mark_circle()` | Bubble chart | Multi-dimensi |
    
    ### 🔤 Tipe Data Encoding
    
    - **Q** (Quantitative): Data numerik kontinu (suhu, berat, harga)
    - **N** (Nominal): Kategori tanpa urutan (nama, jenis, warna)
    - **O** (Ordinal): Kategori dengan urutan (rendah-sedang-tinggi)
    - **T** (Temporal): Data waktu (tanggal, jam)
    
    ### 🎯 Channel Encoding
    
    Altair memetakan data ke visual channels:
    """)
    
    st.code("""
chart = alt.Chart(data).mark_circle().encode(
    x='variabel_x:Q',           # Posisi X
    y='variabel_y:Q',           # Posisi Y
    color='kategori:N',         # Warna
    size='ukuran:Q',            # Ukuran
    opacity='transparansi:Q',   # Transparansi
    shape='bentuk:N',           # Bentuk marker
    tooltip=['var1', 'var2']    # Tooltip interaktif
)
    """, language='python')
    
    st.markdown("""
    ### 🔄 Interaktivitas
    
    #### 1. Tooltip (Hover)
    """)
    
    st.code("""
chart = alt.Chart(data).mark_point().encode(
    x='x:Q',
    y='y:Q',
    tooltip=['x:Q', 'y:Q', 'kategori:N']  # Tampil saat hover
)
    """, language='python')
    
    st.markdown("""
    #### 2. Zoom & Pan
    """)
    
    st.code("""
chart = alt.Chart(data).mark_line().encode(
    x='x:Q',
    y='y:Q'
).interactive()  # Aktifkan zoom & pan
    """, language='python')
    
    st.markdown("""
    #### 3. Selection & Filtering
    """)
    
    st.code("""
# Buat selection
brush = alt.selection_interval()

# Chart dengan selection
chart1 = alt.Chart(data).mark_point().encode(
    x='x:Q',
    y='y:Q',
    color=alt.condition(brush, 'kategori:N', alt.value('gray'))
).add_params(brush)

# Chart yang ter-filter
chart2 = alt.Chart(data).mark_bar().encode(
    x='kategori:N',
    y='count():Q'
).transform_filter(brush)

# Gabungkan
combined = chart1 & chart2  # Vertikal
# atau
combined = chart1 | chart2  # Horizontal
    """, language='python')
    
    st.markdown("""
    ### 🎨 Customization
    
    #### Color Schemes
    """)
    
    st.code("""
# Built-in color schemes
chart = alt.Chart(data).mark_bar().encode(
    x='kategori:N',
    y='nilai:Q',
    color=alt.Color('kategori:N', 
                   scale=alt.Scale(scheme='tableau10'))
    # Schemes: tableau10, category10, viridis, plasma, etc.
)

# Custom colors
chart = alt.Chart(data).mark_bar().encode(
    x='kategori:N',
    y='nilai:Q',
    color=alt.Color('kategori:N',
                   scale=alt.Scale(domain=['A', 'B', 'C'],
                                 range=['#ff0000', '#00ff00', '#0000ff']))
)
    """, language='python')
    
    st.markdown("""
    #### Styling
    """)
    
    st.code("""
chart = alt.Chart(data).mark_line(
    color='red',
    strokeWidth=3,
    strokeDash=[5, 5],  # Dashed line
    point=True          # Tambah points
).encode(
    x='x:Q',
    y='y:Q'
).properties(
    width=600,
    height=400,
    title='Judul Chart'
).configure_axis(
    labelFontSize=12,
    titleFontSize=14
).configure_title(
    fontSize=16,
    anchor='start'
)
    """, language='python')
    
    st.markdown("""
    ### 📊 Contoh Praktis: Analisis Pertanian
    """)
    
    # Example
    example_data = pd.DataFrame({
        'Bulan': pd.date_range('2024-01', periods=12, freq='M'),
        'Hasil Panen': [100, 120, 150, 180, 200, 220, 210, 190, 170, 160, 140, 130],
        'Target': [150] * 12
    })
    
    example_chart = alt.Chart(example_data).mark_line(point=True, color='#10b981').encode(
        x=alt.X('Bulan:T', title='Bulan', axis=alt.Axis(format='%b')),
        y=alt.Y('Hasil Panen:Q', title='Hasil Panen (ton)'),
        tooltip=[
            alt.Tooltip('Bulan:T', format='%B %Y'),
            alt.Tooltip('Hasil Panen:Q', format=',.0f')
        ]
    ).properties(
        width=700,
        height=300,
        title='Hasil Panen Bulanan 2024'
    )
    
    target_line = alt.Chart(example_data).mark_line(
        color='red',
        strokeDash=[5, 5]
    ).encode(
        x='Bulan:T',
        y='Target:Q'
    )
    
    st.altair_chart((example_chart + target_line).interactive(), use_container_width=True)
    
    with st.expander("📝 Lihat Kode Contoh"):
        st.code("""
import altair as alt
import pandas as pd

# Data
data = pd.DataFrame({
    'Bulan': pd.date_range('2024-01', periods=12, freq='M'),
    'Hasil Panen': [100, 120, 150, 180, 200, 220, 210, 190, 170, 160, 140, 130],
    'Target': [150] * 12
})

# Chart hasil panen
harvest_chart = alt.Chart(data).mark_line(point=True, color='#10b981').encode(
    x=alt.X('Bulan:T', title='Bulan'),
    y=alt.Y('Hasil Panen:Q', title='Hasil Panen (ton)'),
    tooltip=['Bulan:T', 'Hasil Panen:Q']
).properties(
    title='Hasil Panen Bulanan 2024'
)

# Target line
target_line = alt.Chart(data).mark_line(
    color='red',
    strokeDash=[5, 5]
).encode(
    x='Bulan:T',
    y='Target:Q'
)

# Gabungkan dan tampilkan
final_chart = (harvest_chart + target_line).interactive()
st.altair_chart(final_chart, use_container_width=True)
        """, language='python')
    
    st.markdown("""
    ### 🔗 Resources
    
    - 📖 [Altair Documentation](https://altair-viz.github.io/)
    - 🎨 [Vega-Lite Examples](https://vega.github.io/vega-lite/examples/)
    - 🎓 [Altair Tutorial](https://altair-viz.github.io/getting_started/overview.html)
    - 🌈 [Color Schemes](https://vega.github.io/vega/docs/schemes/)
    
    ### 💡 Tips & Best Practices
    
    1. **Pilih chart type yang tepat** - Line untuk trend, bar untuk perbandingan, scatter untuk korelasi
    2. **Gunakan color dengan bijak** - Jangan terlalu banyak warna, pilih palette yang konsisten
    3. **Tambahkan tooltips** - Membantu user memahami data detail
    4. **Buat interactive** - `.interactive()` untuk zoom/pan
    5. **Optimasi performa** - Untuk dataset besar (>5000 rows), pertimbangkan aggregasi
    6. **Responsive design** - Gunakan `use_container_width=True` di Streamlit
    
    ### ⚠️ Common Pitfalls
    
    - ❌ Lupa specify data type (`:Q`, `:N`, `:T`)
    - ❌ Data tidak dalam format tidy (long format)
    - ❌ Terlalu banyak data points tanpa aggregasi
    - ❌ Tidak memberikan title/label yang jelas
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>📊 <strong>AgriSensa Tech - Visualisasi Data Altair</strong></p>
    <p>Modul demonstrasi penggunaan Altair untuk analisis data pertanian</p>
    <p style='font-size: 0.9rem;'>💡 Tip: Explore setiap tab untuk melihat berbagai jenis visualisasi!</p>
</div>
""", unsafe_allow_html=True)
