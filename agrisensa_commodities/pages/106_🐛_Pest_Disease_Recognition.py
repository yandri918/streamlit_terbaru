import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
parent_dir = str(Path(__file__).parent.parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from agrisensa_commodities.services.pest_disease_service import PestDiseaseService

# Page config
st.set_page_config(
    page_title="Pest & Disease Recognition - WAGRI",
    page_icon="🐛",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .pest-card {
        background: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
        border-radius: 5px;
    }
    .disease-card {
        background: #fff3cd;
        padding: 15px;
        border-left: 4px solid #ffc107;
        margin: 10px 0;
        border-radius: 5px;
    }
    .ipm-card {
        background: #d1ecf1;
        padding: 15px;
        border-left: 4px solid #17a2b8;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize service
pest_service = PestDiseaseService()

# Header
st.title("🐛 Sistem Identifikasi Hama & Penyakit Tanaman")
st.markdown("""
<div class='main-header'>
    <h3>📊 Berbasis Metodologi WAGRI & IPM</h3>
    <p>Identifikasi hama dan penyakit tanaman dengan database lengkap 24+ entries</p>
    <p><em>Integrated Pest Management untuk pertanian berkelanjutan</em></p>
</div>
""", unsafe_allow_html=True)

st.info("💡 **Database Lokal Lengkap:** 5 tanaman (Padi, Jagung, Tomat, Cabai, Kedelai) dengan 13 hama + 11 penyakit. Siap integrasi WAGRI API!")

st.markdown("---")

# Create tabs
tabs = st.tabs([
    "🔍 Identifikasi Visual",
    "📚 Database Lengkap",
    "🌾 Rekomendasi IPM",
    "📖 Panduan Edukasi"
])

# TAB 1: VISUAL IDENTIFICATION
with tabs[0]:
    st.markdown("## 🔍 Identifikasi Visual Hama & Penyakit")
    
    st.info("💡 **Cara Menggunakan:** Pilih tanaman dan kategori, lalu browse galeri untuk identifikasi visual")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### 🌱 Filter")
        
        # Get available crops
        crops = pest_service.get_available_crops()
        
        crop_options = {crop["key"]: f"{crop['name_id']} ({crop['pest_count']} hama, {crop['disease_count']} penyakit)" 
                       for crop in crops}
        
        selected_crop = st.selectbox(
            "Pilih Tanaman",
            options=list(crop_options.keys()),
            format_func=lambda x: crop_options[x],
            key="visual_crop"
        )
        
        pest_type = st.radio(
            "Kategori",
            options=["all", "pest", "disease"],
            format_func=lambda x: {
                "all": "Semua",
                "pest": "Hama",
                "disease": "Penyakit"
            }[x],
            key="visual_type"
        )
        
        # Get pests/diseases for selected crop
        items = pest_service.get_all_pests_by_crop(selected_crop, pest_type)
        
        st.metric("Total Ditemukan", len(items))
    
    with col2:
        st.markdown("### 📸 Galeri Identifikasi")
        
        if not items:
            st.warning("Tidak ada data untuk tanaman dan kategori yang dipilih")
        else:
            # Display in grid
            cols_per_row = 3
            for i in range(0, len(items), cols_per_row):
                cols = st.columns(cols_per_row)
                for j, col in enumerate(cols):
                    if i + j < len(items):
                        item = items[i + j]
                        with col:
                            # Card style based on type
                            card_class = "pest-card" if item["type"] == "pest" else "disease-card"
                            
                            st.markdown(f"""
                            <div class='{card_class}'>
                                <h4>{item['name_id']}</h4>
                                <p><em>{item['scientific']}</em></p>
                                <p><strong>Severity:</strong> {item['severity'].upper()}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Placeholder for image (will use WAGRI API when token available)
                            st.image("https://via.placeholder.com/300x200?text=Image+Placeholder", 
                                   caption=f"{item['name_id']}")
                            
                            # Expandable details
                            with st.expander("📋 Detail"):
                                st.markdown(f"**Nama Inggris:** {item['name_en']}")
                                st.markdown(f"**Nama Ilmiah:** *{item['scientific']}*")
                                st.markdown(f"**Tingkat Bahaya:** {item['severity']}")
                                
                                st.markdown("**Gejala:**")
                                for symptom in item['symptoms']:
                                    st.markdown(f"- {symptom}")
                                
                                st.markdown(f"**Fase Kerusakan:** {', '.join(item['damage_stage'])}")
                                
                                if st.button(f"Lihat Rekomendasi IPM", key=f"ipm_{item['id']}"):
                                    st.session_state['selected_pest'] = item
                                    st.session_state['selected_crop'] = selected_crop
                                    st.info("✅ Silakan buka tab **Rekomendasi IPM** untuk melihat detail")

# TAB 2: DATABASE BROWSER
with tabs[1]:
    st.markdown("## 📚 Database Lengkap Hama & Penyakit")
    
    st.success("✅ **Database Lokal:** 24+ entries siap digunakan tanpa koneksi internet!")
    
    # Filters
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        filter_crop = st.selectbox(
            "Filter Tanaman",
            options=["all"] + [crop["key"] for crop in crops],
            format_func=lambda x: "Semua Tanaman" if x == "all" else next(
                (c["name_id"] for c in crops if c["key"] == x), x
            ),
            key="db_crop"
        )
    
    with col_f2:
        filter_type = st.selectbox(
            "Filter Kategori",
            options=["all", "pest", "disease"],
            format_func=lambda x: {
                "all": "Semua",
                "pest": "Hama",
                "disease": "Penyakit"
            }[x],
            key="db_type"
        )
    
    with col_f3:
        search_query = st.text_input(
            "🔍 Cari",
            placeholder="Nama hama/penyakit...",
            key="db_search"
        )
    
    # Get all data
    all_data = []
    crops_to_search = [filter_crop] if filter_crop != "all" else [crop["key"] for crop in crops]
    
    for crop_key in crops_to_search:
        crop_name = next((c["name_id"] for c in crops if c["key"] == crop_key), crop_key)
        items = pest_service.get_all_pests_by_crop(crop_key, filter_type)
        
        for item in items:
            # Apply search filter
            if search_query:
                if (search_query.lower() not in item["name_id"].lower() and
                    search_query.lower() not in item["name_en"].lower() and
                    search_query.lower() not in item["scientific"].lower()):
                    continue
            
            all_data.append({
                "Tanaman": crop_name,
                "Nama": item["name_id"],
                "Nama Inggris": item["name_en"],
                "Nama Ilmiah": item["scientific"],
                "Kategori": "Hama" if item["type"] == "pest" else "Penyakit",
                "Severity": item["severity"],
                "ID": item["id"],
                "Crop Key": crop_key
            })
    
    if not all_data:
        st.warning("Tidak ada data yang sesuai dengan filter")
    else:
        df = pd.DataFrame(all_data)
        
        st.markdown(f"### 📊 Ditemukan: {len(df)} entries")
        
        # Display table
        st.dataframe(
            df[["Tanaman", "Nama", "Nama Inggris", "Kategori", "Severity"]],
            use_container_width=True,
            hide_index=True
        )
        
        # Statistics
        st.markdown("### 📈 Statistik Database")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        
        with col_s1:
            # Pie chart by category
            fig_cat = px.pie(
                df,
                names="Kategori",
                title="Distribusi Hama vs Penyakit",
                color="Kategori",
                color_discrete_map={"Hama": "#667eea", "Penyakit": "#ffc107"}
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        
        with col_s2:
            # Bar chart by crop
            crop_counts = df["Tanaman"].value_counts()
            fig_crop = px.bar(
                x=crop_counts.index,
                y=crop_counts.values,
                title="Jumlah per Tanaman",
                labels={"x": "Tanaman", "y": "Jumlah"},
                color=crop_counts.values,
                color_continuous_scale="Viridis"
            )
            st.plotly_chart(fig_crop, use_container_width=True)
        
        with col_s3:
            # Severity distribution
            severity_counts = df["Severity"].value_counts()
            fig_sev = px.bar(
                x=severity_counts.index,
                y=severity_counts.values,
                title="Distribusi Tingkat Bahaya",
                labels={"x": "Severity", "y": "Jumlah"},
                color=severity_counts.index,
                color_discrete_map={"high": "#dc3545", "medium": "#ffc107", "low": "#28a745"}
            )
            st.plotly_chart(fig_sev, use_container_width=True)
        
        # Export options
        st.markdown("### 💾 Export Data")
        
        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            csv_data = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"pest_disease_database_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col_e2:
            # Create detailed text export
            txt_data = "PEST & DISEASE DATABASE\n"
            txt_data += "=" * 60 + "\n\n"
            
            for _, row in df.iterrows():
                txt_data += f"{row['Nama']} ({row['Nama Ilmiah']})\n"
                txt_data += f"Tanaman: {row['Tanaman']}\n"
                txt_data += f"Kategori: {row['Kategori']}\n"
                txt_data += f"Severity: {row['Severity']}\n"
                txt_data += "-" * 60 + "\n\n"
            
            st.download_button(
                label="📥 Download TXT",
                data=txt_data,
                file_name=f"pest_disease_database_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

# Continue with Tab 3 and 4 in next part...
