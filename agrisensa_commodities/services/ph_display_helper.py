"""
pH Display Helper Functions
Provides UI components for pH status and recommendations
"""

import streamlit as st
from .soil_adjustment_service import calculate_lime_requirement


def display_ph_section(crop_name, soil_ph, estimated_area, target_ph=None):
    """
    Display pH status and recommendations section
    
    Parameters:
    - crop_name: Name of the crop
    - soil_ph: Current soil pH
    - estimated_area: Farm area in hectares
    - target_ph: Target pH (optional, will be calculated if not provided)
    
    Returns:
    - None (displays Streamlit components)
    """
    
    st.markdown("---")
    st.subheader("🧪 Status & Rekomendasi pH Tanah")
    
    # Determine target pH if not provided
    if target_ph is None:
        target_ph = 6.5 if crop_name not in ["Kelapa Sawit", "Karet", "Kakao", "Kopi Arabika", "Kopi Robusta"] else 6.0
    
    # Always show pH status
    col1, col2 = st.columns(2)
    with col1:
        if soil_ph >= 3.0:
            # Visual indicator
            if abs(soil_ph - target_ph) <= 0.5:
                ph_status_color = "🟢"
                ph_status_text = "Ideal"
            elif soil_ph < target_ph:
                ph_status_color = "🟡"
                ph_status_text = "Perlu Pengapuran"
            else:
                ph_status_color = "🔵"
                ph_status_text = "Terlalu Basa"
            
            st.metric("pH Tanah Saat Ini", f"{ph_status_color} {soil_ph:.1f}", 
                     delta=f"Target: {target_ph:.1f}",
                     help=ph_status_text)
        else:
            st.metric("pH Tanah", "Belum diinput", help="Input pH di sidebar untuk rekomendasi")
    
    with col2:
        st.metric("pH Optimal", f"{target_ph:.1f}", 
                 delta=f"untuk {crop_name}",
                 help="pH ideal untuk pertumbuhan optimal")
    
    # Show recommendations based on pH
    if soil_ph >= 3.0:
        if soil_ph < target_ph:
            # Need liming
            st.warning(f"⚠️ pH terlalu rendah ({soil_ph:.1f}). Perlu pengapuran!")
            
            lime_req = calculate_lime_requirement(soil_ph, target_ph, estimated_area, 'medium')
            
            if lime_req['needed']:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Kebutuhan Dolomite", f"{lime_req['dolomite_total_ton']:.2f} ton",
                             help=f"{lime_req['dolomite_ton_per_ha']:.2f} ton/ha")
                with col2:
                    st.metric("Biaya Estimasi", f"Rp {lime_req['dolomite_cost']:,.0f}",
                             help="Harga Dolomite ~Rp 450K/ton")
                
                with st.expander("📋 Detail Rekomendasi Pengapuran", expanded=True):
                    st.markdown(f"""
                    **🎯 Target Kenaikan pH:** {lime_req['ph_increase']:.1f} unit ({soil_ph:.1f} → {target_ph:.1f})
                    
                    **💎 Pilihan Kapur:**
                    
                    **Opsi 1: Dolomite (CaMg(CO3)2)** ⭐ **Recommended**
                    - Dosis: {lime_req['dolomite_ton_per_ha']:.2f} ton/ha
                    - Total: {lime_req['dolomite_total_ton']:.2f} ton untuk {lime_req['area_ha']:.2f} ha
                    - Biaya: Rp {lime_req['dolomite_cost']:,.0f}
                    - Keunggulan: Mengandung Mg (baik untuk tanaman)
                    
                    **Opsi 2: CaCO3 (Kalsit)**
                    - Dosis: {lime_req['caco3_ton_per_ha']:.2f} ton/ha
                    - Total: {lime_req['caco3_total_ton']:.2f} ton
                    - Biaya: Rp {lime_req['caco3_cost']:,.0f}
                    
                    **📅 Waktu Aplikasi:**
                    - {lime_req['timing']}
                    - Metode: {lime_req['application_method']}
                    
                    **⚠️ Catatan Penting:**
                    - Aplikasikan 2-8 minggu SEBELUM pemupukan
                    - Campur merata dengan tanah (bajak/cangkul)
                    - JANGAN dicampur dengan Urea (akan menguap)
                    - Monitor pH setelah 2-3 bulan
                    - Pengapuran ulang setiap 2-3 tahun jika perlu
                    """)
        
        elif soil_ph <= target_ph + 0.5:
            # pH ideal
            st.success(f"✅ pH Ideal! ({soil_ph:.1f}) - Tidak perlu pengapuran")
            st.info("💡 Pertahankan pH dengan pemupukan berimbang dan monitoring rutin setiap 6 bulan")
        
        else:
            # pH too high
            st.warning(f"⚠️ pH terlalu tinggi ({soil_ph:.1f}). Perlu penurunan pH!")
            st.markdown("""
            **Cara Menurunkan pH:**
            - Gunakan pupuk yang bersifat asam (Urea, ZA, KCl)
            - Aplikasikan sulfur elemental (50-100 kg/ha)
            - Tambahkan bahan organik (kompos, pupuk kandang)
            - Hindari pengapuran
            """)
    else:
        st.info("💡 **Input pH tanah di sidebar** untuk mendapatkan rekomendasi pengapuran yang akurat!")
