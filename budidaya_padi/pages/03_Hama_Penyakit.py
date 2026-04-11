"""
 Hama & Penyakit Padi - Rice Pest and Disease Database
Comprehensive guide for pest and disease management
Database from AgriSensa Commodities
"""

import streamlit as st
import pandas as pd
import altair as alt
import sys
from pathlib import Path

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from data.pest_disease_data import get_all_pests, get_all_diseases, search_by_symptom

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

st.set_page_config(page_title="Hama & Penyakit", page_icon="", layout="wide")

# Apply Design System
apply_design_system()

st.markdown(f"<h1 style='margin-bottom: 0;'>{icon('bug', size='lg')} Hama & Penyakit</h1>", unsafe_allow_html=True)
st.markdown("**Database lengkap hama dan penyakit padi dengan cara pengendalian**")
st.markdown("---")

# Load data
PESTS = get_all_pests()
DISEASES = get_all_diseases()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([" Hama", " Penyakit", " Cari Gejala", " Perbandingan"])

with tab1:
    st.header(" Database Hama Padi")
    st.markdown(f"**Total: {len(PESTS)} Hama Utama**")
    
    for pest in PESTS:
        severity_color = "" if pest['severity'] == 'high' else "🟡" if pest['severity'] == 'medium' else "🟢"
        
        with st.expander(f"{severity_color} {pest['name_id']} ({pest['scientific']})", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("###  Informasi")
                st.write(f"**Nama Ilmiah:** *{pest['scientific']}*")
                st.write(f"**Tingkat Bahaya:** {pest['severity'].upper()}")
                st.write(f"**Fase Kerusakan:** {', '.join(pest['damage_stage'])}")
                
                st.markdown("###  Gejala")
                for symptom in pest['symptoms']:
                    st.write(f"• {symptom}")
                
                st.warning(f" **Ambang Ekonomi:** {pest['economic_threshold']}")
                st.info(f" **Puncak Serangan:** {pest['peak_season']}")
            
            with col2:
                st.markdown("###  Pengendalian")
                
                st.markdown("** Kultur Teknis:**")
                for control in pest['control']['cultural']:
                    st.write(f"• {control}")
                
                st.markdown("** Hayati (Biological):**")
                for control in pest['control']['biological']:
                    st.write(f"• {control}")
                
                st.markdown("** Kimia (Chemical):**")
                for control in pest['control']['chemical']:
                    st.write(f"• {control}")

with tab2:
    st.header(" Database Penyakit Padi")
    st.markdown(f"**Total: {len(DISEASES)} Penyakit Utama**")
    
    for disease in DISEASES:
        severity_color = "" if disease['severity'] == 'high' else "🟡" if disease['severity'] == 'medium' else "🟢"
        
        with st.expander(f"{severity_color} {disease['name_id']} ({disease['scientific']})", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("###  Informasi")
                st.write(f"**Patogen:** *{disease['scientific']}*")
                st.write(f"**Tingkat Bahaya:** {disease['severity'].upper()}")
                st.write(f"**Fase Kerusakan:** {', '.join(disease['damage_stage'])}")
                
                st.markdown("###  Gejala")
                for symptom in disease['symptoms']:
                    st.write(f"• {symptom}")
                
                st.warning(f" **Kondisi Menguntungkan:** {disease['favorable_conditions']}")
                st.info(f" **Puncak Serangan:** {disease['peak_season']}")
            
            with col2:
                st.markdown("###  Pengendalian")
                
                st.markdown("** Kultur Teknis:**")
                for control in disease['control']['cultural']:
                    st.write(f"• {control}")
                
                st.markdown("** Hayati (Biological):**")
                for control in disease['control']['biological']:
                    st.write(f"• {control}")
                
                st.markdown("** Kimia (Chemical):**")
                for control in disease['control']['chemical']:
                    st.write(f"• {control}")

with tab3:
    st.header(" Cari Berdasarkan Gejala")
    
    st.markdown("Masukkan gejala yang Anda lihat di tanaman padi:")
    
    search_query = st.text_input("Cari gejala (contoh: daun kuning, gabah hampa, busuk)", "")
    
    if search_query:
        results = search_by_symptom(search_query)
        
        if results:
            st.success(f" Ditemukan {len(results)} hasil:")
            
            for item in results:
                item_type = " Hama" if 'economic_threshold' in item else " Penyakit"
                severity_color = "" if item['severity'] == 'high' else "🟡" if item['severity'] == 'medium' else "🟢"
                
                with st.expander(f"{severity_color} {item_type}: {item['name_id']}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.write(f"**Nama Ilmiah:** *{item['scientific']}*")
                        st.markdown("**Gejala:**")
                        for symptom in item['symptoms']:
                            st.write(f"• {symptom}")
                    
                    with col2:
                        st.markdown("**Pengendalian Utama:**")
                        st.write(" **Kultur Teknis:**")
                        for i, control in enumerate(item['control']['cultural'][:3], 1):
                            st.write(f"{i}. {control}")
        else:
            st.warning(" Tidak ditemukan hasil. Coba kata kunci lain.")
    else:
        st.info(" Ketik gejala yang Anda amati untuk mencari hama/penyakit yang cocok")

with tab4:
    st.header(" Perbandingan Hama & Penyakit")
    
    # Create comparison dataframe
    all_items = []
    
    for pest in PESTS:
        all_items.append({
            'Nama': pest['name_id'],
            'Jenis': 'Hama',
            'Tingkat Bahaya': pest['severity'].upper(),
            'Fase': ', '.join(pest['damage_stage'])
        })
    
    for disease in DISEASES:
        all_items.append({
            'Nama': disease['name_id'],
            'Jenis': 'Penyakit',
            'Tingkat Bahaya': disease['severity'].upper(),
            'Fase': ', '.join(disease['damage_stage'])
        })
    
    comparison_df = pd.DataFrame(all_items)
    
    st.subheader(" Tabel Lengkap")
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # Distribution by type
        type_chart = alt.Chart(comparison_df).mark_bar().encode(
            x=alt.X('Jenis:N', title='Jenis'),
            y=alt.Y('count():Q', title='Jumlah'),
            color=alt.Color('Jenis:N', scale=alt.Scale(domain=['Hama', 'Penyakit'], range=['#FF6B6B', '#4ECDC4'])),
            tooltip=['Jenis', 'count()']
        ).properties(
            title='Distribusi Hama vs Penyakit',
            height=300
        )
        
        st.altair_chart(type_chart, use_container_width=True)
    
    with col_chart2:
        # Distribution by severity
        severity_chart = alt.Chart(comparison_df).mark_bar().encode(
            x=alt.X('Tingkat Bahaya:N', title='Tingkat Bahaya', sort=['HIGH', 'MEDIUM', 'LOW']),
            y=alt.Y('count():Q', title='Jumlah'),
            color=alt.Color('Tingkat Bahaya:N', 
                          scale=alt.Scale(domain=['HIGH', 'MEDIUM', 'LOW'], 
                                        range=['#FF4444', '#FFA500', '#4CAF50'])),
            tooltip=['Tingkat Bahaya', 'count()']
        ).properties(
            title='Distribusi Tingkat Bahaya',
            height=300
        )
        
        st.altair_chart(severity_chart, use_container_width=True)
    
    # PHT Schedule
    st.markdown("---")
    st.subheader(" Jadwal Pengendalian Hama Terpadu (PHT)")
    
    st.markdown("""
    ### Strategi PHT
    
    **Prinsip:**
    1. Pencegahan lebih baik dari pengobatan
    2. Gunakan musuh alami
    3. Pestisida sebagai pilihan terakhir
    4. Monitoring rutin 2x/minggu
    """)
    
    schedule_df = pd.DataFrame({
        'Periode (HST)': ['0-20', '20-40', '40-60', '60-80', '80-100', '100-120'],
        'Target Utama': [
            'Tikus, Keong, Lalat Bibit',
            'Penggerek batang, Tungro, Wereng Hijau',
            'Wereng Coklat, Blast, Kepik Bergaris',
            'Blast, Hawar daun, Busuk Pelepah',
            'Walang sangit, Hampa Palsu',
            'Tikus, Burung, Bercak Coklat'
        ],
        'Tindakan': [
            'Gropyokan, sanitasi, monitoring',
            'Perangkap, eradikasi tanaman sakit',
            'Monitoring, fungisida/insektisida jika perlu',
            'Fungisida, bakterisida, drainase',
            'Hand picking, insektisida spot',
            'Pengusiran, jaring, panen tepat waktu'
        ]
    })
    
    st.dataframe(schedule_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.success("""
 **Tips Pengendalian Efektif:**
- Monitoring rutin 2x seminggu
- Catat populasi hama/intensitas penyakit
- Aplikasi pestisida sesuai ambang ekonomi
- Rotasi pestisida untuk hindari resistensi
- Gunakan APD saat aplikasi
- Prioritaskan pengendalian kultur teknis dan hayati
""")

st.caption(" **Penting:** Selalu ikuti dosis dan cara aplikasi pestisida sesuai label. Database ini dari AgriSensa Commodities.")
