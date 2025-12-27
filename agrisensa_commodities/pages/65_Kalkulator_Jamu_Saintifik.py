import streamlit as st
import sys
import os
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Add parent directory to path
parent_dir = str(Path(__file__).parent.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.jamu_calculator_service import (
    JamuCalculatorService,
    JAMU_FORMULAS,
    INGREDIENT_DATABASE,
    RESEARCH_REFERENCES
)

st.set_page_config(
    page_title="Kalkulator Jamu Saintifik",
    page_icon="🍵",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .jamu-header {
        background: linear-gradient(135deg, #16a34a 0%, #15803d 100%);
        color: white;
        padding: 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .formula-card {
        background: white;
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #16a34a;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    .warning-box {
        background: #fef3c7;
        border-left: 4px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
    .evidence-box {
        background: #dbeafe;
        border-left: 4px solid #3b82f6;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="jamu-header">
    <h1>🍵 Kalkulator Jamu Saintifik</h1>
    <p>Evidence-Based Traditional Indonesian Herbal Medicine</p>
    <p><strong>Berdasarkan Penelitian B2P2TOOT & Program Saintifikasi Jamu</strong></p>
</div>
""", unsafe_allow_html=True)

# Medical Disclaimer
st.warning("""
**⚕️ DISCLAIMER MEDIS:**
- Kalkulator ini untuk tujuan edukasi dan suplementasi kesehatan
- BUKAN pengganti pengobatan medis atau konsultasi dokter
- Konsultasikan dengan dokter sebelum menggunakan jamu, terutama jika sedang mengonsumsi obat
- Hentikan penggunaan jika terjadi efek samping dan konsultasi dokter
""")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📖 Tentang Jamu Saintifik",
    "🏥 Pilih Kondisi Kesehatan",
    "🧮 Kalkulator Formulasi",
    "🧪 Database Bahan Aktif",
    "📚 Referensi Penelitian",
    "⚠️ Panduan Keamanan",
    "💰 Kalkulator Biaya"
])

# ===== TAB 1: TENTANG JAMU SAINTIFIK =====
with tab1:
    st.markdown("## 📖 Tentang Jamu Saintifik")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="formula-card">
        <h3>🔬 Program Saintifikasi Jamu</h3>
        <p><strong>Saintifikasi Jamu</strong> adalah program penelitian ilmiah pemanfaatan jamu melalui penelitian berbasis pelayanan kesehatan yang dilakukan oleh <strong>B2P2TOOT (Balai Besar Penelitian dan Pengembangan Tanaman Obat dan Obat Tradisional)</strong> di bawah Kementerian Kesehatan RI.</p>
        
        <h4>Tujuan Program:</h4>
        <ul>
        <li>Membuktikan khasiat dan keamanan jamu secara ilmiah</li>
        <li>Menyediakan bukti berbasis penelitian (evidence-based)</li>
        <li>Mengintegrasikan jamu ke dalam sistem pelayanan kesehatan</li>
        <li>Meningkatkan kepercayaan masyarakat terhadap jamu</li>
        </ul>
        
        <h4>Metode Penelitian:</h4>
        <ul>
        <li><strong>RCT (Randomized Controlled Trial)</strong>: Uji klinis acak terkontrol</li>
        <li><strong>Uji Fase I, II, III</strong>: Keamanan, efikasi, dan efektivitas</li>
        <li><strong>Publikasi Jurnal</strong>: Nasional dan internasional</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="evidence-box">
        <h4>📊 Hasil Program Saintifikasi Jamu:</h4>
        <ul>
        <li><strong>11 Formula Jamu</strong> telah divalidasi secara klinis</li>
        <li><strong>25,821 Formula</strong> terinventarisasi (Ristoja)</li>
        <li><strong>3,000 Spesies</strong> tanaman obat terdokumentasi</li>
        <li>Terbukti <strong>aman dan berkhasiat</strong> untuk Penyakit Tidak Menular (PTM)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="formula-card">
        <h3>📋 Klasifikasi Obat Tradisional (BPOM)</h3>
        
        <h4>1. Jamu</h4>
        <ul>
        <li>Berdasarkan resep turun-temurun</li>
        <li>Belum melalui uji klinis</li>
        <li>Aman berdasarkan pengalaman empiris</li>
        </ul>
        
        <h4>2. Obat Herbal Terstandar (OHT)</h4>
        <ul>
        <li>Telah melalui uji praklinis</li>
        <li>Bahan baku terstandar</li>
        <li>Khasiat terbukti secara ilmiah (in-vitro/in-vivo)</li>
        </ul>
        
        <h4>3. Fitofarmaka</h4>
        <ul>
        <li>Telah melalui <strong>uji klinis</strong> pada manusia</li>
        <li>Setara dengan obat modern</li>
        <li>Dapat diresepkan dokter</li>
        <li>Contoh: Stimuno, Tensigard</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="formula-card">
        <h3>✅ Keunggulan Jamu Saintifik</h3>
        <ul>
        <li>✅ <strong>Evidence-Based</strong>: Terbukti melalui penelitian klinis</li>
        <li>✅ <strong>Dosis Terstandar</strong>: Takaran pasti (gram), bukan "secukupnya"</li>
        <li>✅ <strong>Keamanan Terjamin</strong>: Telah melalui uji toksisitas</li>
        <li>✅ <strong>Efektivitas Terbukti</strong>: Setara atau mendekati obat modern</li>
        <li>✅ <strong>Minim Efek Samping</strong>: Jika digunakan sesuai dosis</li>
        <li>✅ <strong>Biaya Terjangkau</strong>: Lebih murah dari obat sintetis</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.info("""
    **💡 Catatan Penting:**
    Kalkulator ini menggunakan formula yang telah divalidasi melalui penelitian klinis (RCT) dan dipublikasikan dalam jurnal ilmiah. 
    Semua dosis dan komposisi berdasarkan protokol penelitian B2P2TOOT dan literatur ilmiah terpercaya.
    """)

# ===== TAB 2: PILIH KONDISI KESEHATAN =====
with tab2:
    st.markdown("## 🏥 Pilih Kondisi Kesehatan")
    
    st.info("Pilih kondisi kesehatan yang ingin Anda atasi dengan jamu. Setiap formula telah divalidasi melalui penelitian klinis.")
    
    # Get all conditions
    conditions = JamuCalculatorService.get_all_conditions()
    
    # Create cards for each condition
    cols = st.columns(2)
    
    for idx, condition in enumerate(conditions):
        with cols[idx % 2]:
            formula = JamuCalculatorService.get_formula_by_condition(condition)
            
            with st.expander(f"**{condition}**", expanded=False):
                st.markdown(f"**🔬 Bukti Klinis:**")
                st.success(formula["clinical_evidence"])
                
                st.markdown(f"**📝 Komposisi:**")
                for ingredient, amount in formula["ingredients"].items():
                    st.markdown(f"- {ingredient}: {amount} gram")
                
                st.markdown(f"**💊 Dosis:**")
                st.markdown(f"- {formula['dosage']}")
                
                st.markdown(f"**⏱️ Durasi:**")
                st.markdown(f"- {formula['duration']}")
                
                st.markdown(f"**⚠️ Kontraindikasi:**")
                for contra in formula["contraindications"]:
                    st.markdown(f"- {contra}")
                
                if st.button(f"Gunakan Formula Ini", key=f"select_{idx}"):
                    st.session_state['selected_condition'] = condition
                    st.success(f"✅ Formula **{condition}** dipilih! Lanjut ke tab **Kalkulator Formulasi**")

# ===== TAB 3: KALKULATOR FORMULASI =====
with tab3:
    st.markdown("## 🧮 Kalkulator Formulasi Jamu")
    
    # Condition selection
    selected_condition = st.selectbox(
        "Pilih Kondisi Kesehatan:",
        JamuCalculatorService.get_all_conditions(),
        index=0 if 'selected_condition' not in st.session_state else JamuCalculatorService.get_all_conditions().index(st.session_state.get('selected_condition'))
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        servings = st.number_input(
            "Jumlah Porsi (hari):",
            min_value=1,
            max_value=30,
            value=7,
            help="1 porsi = kebutuhan untuk 1 hari"
        )
    
    with col2:
        body_weight = st.number_input(
            "Berat Badan (kg):",
            min_value=30,
            max_value=150,
            value=60,
            help="Untuk penyesuaian dosis"
        )
    
    with col3:
        age_group = st.selectbox(
            "Kelompok Usia:",
            ["adult", "elderly"],
            format_func=lambda x: "Dewasa (18-60 tahun)" if x == "adult" else "Lansia (>60 tahun)"
        )
    
    # Calculate
    if st.button("🧮 Hitung Formulasi", type="primary"):
        calculation = JamuCalculatorService.calculate_ingredients(
            selected_condition, servings, body_weight, age_group
        )
        
        if calculation:
            st.success(f"✅ Formulasi untuk **{selected_condition}** berhasil dihitung!")
            
            # Display results
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("### 📋 Daftar Bahan")
                
                ingredients_data = []
                for ingredient, amount in calculation["ingredients"].items():
                    ingredients_data.append({
                        "Bahan": ingredient,
                        "Jumlah (gram)": amount,
                        "Untuk": f"{servings} hari"
                    })
                
                df_ingredients = pd.DataFrame(ingredients_data)
                st.dataframe(df_ingredients, use_container_width=True, hide_index=True)
                
                # Preparation method
                st.markdown("### 🔥 Cara Pembuatan")
                st.info(calculation["preparation"])
                
                # Dosage
                st.markdown("### 💊 Dosis & Aturan Pakai")
                st.success(f"**Dosis:** {calculation['dosage']}")
                st.success(f"**Durasi:** {calculation['duration']}")
            
            with col2:
                st.markdown("### 🔬 Bukti Klinis")
                st.markdown(f"""
                <div class="evidence-box">
                {calculation['clinical_evidence']}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("### ⚠️ Peringatan")
                st.markdown(f"""
                <div class="warning-box">
                <strong>Kontraindikasi:</strong><br>
                {"<br>".join(['• ' + c for c in calculation['contraindications']])}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="warning-box">
                <strong>Efek Samping:</strong><br>
                {calculation['side_effects']}
                </div>
                """, unsafe_allow_html=True)
            
            # Visual chart
            st.markdown("### 📊 Komposisi Bahan")
            
            fig = px.pie(
                df_ingredients,
                values='Jumlah (gram)',
                names='Bahan',
                title=f'Komposisi {selected_condition} ({servings} hari)'
            )
            st.plotly_chart(fig, use_container_width=True)

# ===== TAB 4: DATABASE BAHAN AKTIF =====
with tab4:
    st.markdown("## 🧪 Database Bahan Aktif & Fitokimia")
    
    st.info("Database lengkap kandungan senyawa aktif, mekanisme kerja, dan informasi keamanan setiap bahan jamu.")
    
    # Ingredient selector
    selected_ingredient = st.selectbox(
        "Pilih Bahan:",
        list(INGREDIENT_DATABASE.keys())
    )
    
    ingredient_info = JamuCalculatorService.get_ingredient_info(selected_ingredient)
    
    if ingredient_info:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown(f"### {selected_ingredient}")
            
            st.markdown("**🧪 Senyawa Aktif:**")
            for compound in ingredient_info["active_compounds"]:
                st.markdown(f"- {compound}")
            
            st.markdown("**💊 Manfaat Kesehatan:**")
            for benefit in ingredient_info["benefits"]:
                st.markdown(f"✅ {benefit}")
            
            st.markdown("**⚙️ Mekanisme Kerja:**")
            st.info(ingredient_info["mechanism"])
        
        with col2:
            st.markdown("**📏 Dosis Aman:**")
            st.success(ingredient_info["safe_dose"])
            
            st.markdown("**⚠️ Kontraindikasi:**")
            for contra in ingredient_info["contraindications"]:
                st.warning(f"• {contra}")
            
            st.markdown("**💊 Interaksi Obat:**")
            for interaction in ingredient_info["drug_interactions"]:
                st.error(f"• {interaction}")
    
    # Summary table
    st.markdown("### 📊 Ringkasan Database Bahan")
    
    summary_data = []
    for ingredient, info in INGREDIENT_DATABASE.items():
        summary_data.append({
            "Bahan": ingredient.split("(")[0].strip(),
            "Senyawa Utama": info["active_compounds"][0] if info["active_compounds"] else "-",
            "Manfaat Utama": info["benefits"][0] if info["benefits"] else "-",
            "Dosis Aman": info["safe_dose"]
        })
    
    df_summary = pd.DataFrame(summary_data)
    st.dataframe(df_summary, use_container_width=True, hide_index=True)

# ===== TAB 5: REFERENSI PENELITIAN =====
with tab5:
    st.markdown("## 📚 Referensi Penelitian Ilmiah")
    
    st.info("""
    Semua formula jamu dalam kalkulator ini berdasarkan penelitian ilmiah yang telah dipublikasikan. 
    Berikut adalah referensi utama dari uji klinis dan penelitian fitokimia.
    """)
    
    # Research by category
    for category, references in RESEARCH_REFERENCES.items():
        st.markdown(f"### 📖 {category}")
        
        for idx, ref in enumerate(references, 1):
            with st.expander(f"**[{idx}] {ref['title']}**", expanded=False):
                st.markdown(f"**Penulis:** {ref['authors']}")
                st.markdown(f"**Tahun:** {ref['year']}")
                
                if 'journal' in ref:
                    st.markdown(f"**Jurnal:** *{ref['journal']}*")
                
                if 'source' in ref:
                    st.markdown(f"**Sumber:** {ref['source']}")
                
                st.markdown(f"**Temuan:**")
                st.success(ref['finding'])
    
    # B2P2TOOT Information
    st.markdown("### 🏛️ Tentang B2P2TOOT")
    
    st.markdown("""
    <div class="formula-card">
    <h4>Balai Besar Penelitian dan Pengembangan Tanaman Obat dan Obat Tradisional</h4>
    
    <p><strong>B2P2TOOT</strong> adalah lembaga penelitian di bawah Badan Penelitian dan Pengembangan Kesehatan, 
    Kementerian Kesehatan RI yang fokus pada penelitian dan pengembangan tanaman obat serta saintifikasi jamu.</p>
    
    <h4>Program Utama:</h4>
    <ul>
    <li><strong>Saintifikasi Jamu</strong>: Penelitian berbasis pelayanan kesehatan</li>
    <li><strong>Ristoja</strong>: Riset Tumbuhan Obat dan Jamu</li>
    <li><strong>Rumah Riset Jamu (RRJ) Hortus Medicus</strong>: Fasilitas penelitian klinis</li>
    <li><strong>Standardisasi Tanaman Obat</strong>: Budidaya dan kadar senyawa aktif</li>
    </ul>
    
    <h4>Hasil Penelitian:</h4>
    <ul>
    <li>11 Formula Jamu Saintifik tervalidasi (RCT)</li>
    <li>25,821 Formula jamu terinventarisasi</li>
    <li>3,000 Spesies tanaman obat terdokumentasi</li>
    <li>Publikasi di jurnal nasional dan internasional</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# ===== TAB 6: PANDUAN KEAMANAN =====
with tab6:
    st.markdown("## ⚠️ Panduan Keamanan & Kontraindikasi")
    
    st.warning("""
    **⚕️ PENTING: Konsultasi Dokter Diperlukan Jika:**
    - Sedang hamil atau menyusui
    - Sedang mengonsumsi obat resep
    - Memiliki penyakit kronis (diabetes, hipertensi, gangguan hati/ginjal)
    - Akan menjalani operasi (hentikan jamu 7 hari sebelum operasi)
    - Mengalami efek samping setelah konsumsi jamu
    """)
    
    # Safety checker
    st.markdown("### 🔍 Cek Keamanan Personal")
    
    with st.form("safety_check"):
        st.markdown("**Profil Kesehatan Anda:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            pregnant = st.checkbox("Sedang hamil")
            breastfeeding = st.checkbox("Sedang menyusui")
            taking_medications = st.checkbox("Sedang mengonsumsi obat")
        
        with col2:
            conditions = st.multiselect(
                "Kondisi Kesehatan yang Dimiliki:",
                ["Diabetes", "Hipertensi", "Gangguan Hati", "Gangguan Ginjal", 
                 "Gangguan Pembekuan Darah", "Tukak Lambung", "Alergi"]
            )
        
        check_condition = st.selectbox(
            "Formula yang Ingin Dicek:",
            JamuCalculatorService.get_all_conditions()
        )
        
        submitted = st.form_submit_button("🔍 Cek Keamanan", type="primary")
        
        if submitted:
            user_profile = {
                'pregnant': pregnant,
                'breastfeeding': breastfeeding,
                'taking_medications': taking_medications,
                'conditions': conditions
            }
            
            warnings = JamuCalculatorService.check_contraindications(check_condition, user_profile)
            
            if warnings:
                st.error("**⚠️ PERINGATAN KEAMANAN:**")
                for warning in warnings:
                    st.error(warning)
                st.error("**Konsultasikan dengan dokter sebelum menggunakan jamu ini!**")
            else:
                st.success("✅ Tidak ada kontraindikasi yang terdeteksi berdasarkan profil Anda.")
                st.info("Namun tetap disarankan untuk berkonsultasi dengan dokter, terutama jika Anda sedang mengonsumsi obat.")
    
    # General safety guidelines
    st.markdown("### 📋 Panduan Umum Keamanan Jamu")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **✅ DO (Lakukan):**
        - ✅ Gunakan dosis sesuai rekomendasi
        - ✅ Konsumsi secara teratur sesuai durasi
        - ✅ Gunakan bahan berkualitas baik
        - ✅ Simpan di tempat sejuk dan kering
        - ✅ Konsultasi dokter jika ada kondisi khusus
        - ✅ Monitor efek samping
        - ✅ Beri jeda 2 jam antara jamu dan obat
        """)
    
    with col2:
        st.markdown("""
        **❌ DON'T (Jangan):**
        - ❌ Melebihi dosis yang dianjurkan
        - ❌ Menggunakan jika ada kontraindikasi
        - ❌ Menghentikan obat dokter tanpa konsultasi
        - ❌ Menggunakan bahan yang sudah rusak/berjamur
        - ❌ Menyimpan jamu >24 jam (untuk rebusan)
        - ❌ Mengabaikan efek samping
        - ❌ Menggunakan saat hamil tanpa konsultasi
        """)

# ===== TAB 7: KALKULATOR BIAYA =====
with tab7:
    st.markdown("## 💰 Kalkulator Biaya Jamu")
    
    st.info("Hitung estimasi biaya pembuatan jamu berdasarkan harga bahan di pasar.")
    
    # Condition and servings selection
    col1, col2 = st.columns(2)
    
    with col1:
        cost_condition = st.selectbox(
            "Pilih Formula Jamu:",
            JamuCalculatorService.get_all_conditions(),
            key="cost_condition"
        )
    
    with col2:
        cost_servings = st.number_input(
            "Jumlah Porsi (hari):",
            min_value=1,
            max_value=30,
            value=7,
            key="cost_servings"
        )
    
    # Get formula to know ingredients
    formula = JamuCalculatorService.get_formula_by_condition(cost_condition)
    calculation = JamuCalculatorService.calculate_ingredients(cost_condition, cost_servings)
    
    if calculation:
        st.markdown("### 💵 Edit Harga Bahan (Rp per 100 gram)")
        st.info("💡 **Sesuaikan harga sesuai pasar lokal Anda**")
        
        # Default prices
        default_prices = {
            "Daun Salam": 5000,
            "Sambiloto": 15000,
            "Kayu Manis": 25000,
            "Temulawak": 8000,
            "Kunyit": 6000,
            "Jahe Merah": 12000,
            "Jahe": 10000,
            "Kencur": 10000,
            "Seledri": 8000,
            "Bawang Putih": 15000,
            "Daun Sirsak": 10000,
            "Daun Jombang": 12000,
            "Beras": 3000,
            "Asam Jawa": 8000,
            "Gula Aren": 20000,
            "Madu": 50000,
            "Daun Mint": 15000,
            "Mengkudu": 5000,
            "Daun Sembung": 10000,
            "Jeruk Nipis": 10000,
            "Serai": 7000,
            "Daun Jati Belanda": 12000
        }
        
        # Create editable inputs for each ingredient
        custom_prices = {}
        
        # Get unique ingredients from calculation
        ingredients_list = list(calculation["ingredients"].keys())
        
        # Create columns for input fields
        num_cols = 3
        cols = st.columns(num_cols)
        
        for idx, ingredient in enumerate(ingredients_list):
            # Extract base ingredient name
            base_name = ingredient.split("(")[0].strip()
            
            # Find matching default price
            default_price = 10000  # fallback
            for price_key, price_value in default_prices.items():
                if price_key in base_name:
                    default_price = price_value
                    break
            
            # Create input in appropriate column
            with cols[idx % num_cols]:
                custom_prices[ingredient] = st.number_input(
                    f"{base_name}:",
                    min_value=0,
                    value=default_price,
                    step=1000,
                    key=f"price_{idx}",
                    help=f"Harga per 100 gram"
                )
        
        # Recalculate with custom prices
        total_cost = 0
        cost_breakdown = {}
        
        for ingredient, amount_grams in calculation["ingredients"].items():
            price_per_100g = custom_prices[ingredient]
            item_cost = (amount_grams / 100) * price_per_100g
            
            cost_breakdown[ingredient] = {
                "amount_grams": amount_grams,
                "price_per_100g": price_per_100g,
                "total_cost": item_cost
            }
            total_cost += item_cost
        
        cost_per_day = total_cost / cost_servings if cost_servings > 0 else 0
        
        # Display summary metrics
        st.markdown("### 📊 Hasil Perhitungan (Berdasarkan Harga Custom)")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Biaya", f"Rp {total_cost:,.0f}")
        with col2:
            st.metric("Biaya per Hari", f"Rp {cost_per_day:,.0f}")
        with col3:
            st.metric("Biaya per Bulan", f"Rp {cost_per_day * 30:,.0f}")
        with col4:
            commercial_price = cost_per_day * 5  # Estimate 5x markup
            st.metric("Harga Komersial (est.)", f"Rp {commercial_price:,.0f}/hari")
        
        # Detailed breakdown
        st.markdown("### 📋 Rincian Biaya per Bahan")
        
        breakdown_data = []
        for ingredient, details in cost_breakdown.items():
            breakdown_data.append({
                "Bahan": ingredient,
                "Jumlah (gram)": details['amount_grams'],
                "Harga/100g (Rp)": details['price_per_100g'],
                "Total (Rp)": details['total_cost']
            })
        
        df_breakdown = pd.DataFrame(breakdown_data)
        st.dataframe(df_breakdown, use_container_width=True, hide_index=True)
        
        # Pie chart
        fig = px.pie(
            df_breakdown,
            values='Total (Rp)',
            names='Bahan',
            title=f'Distribusi Biaya {cost_condition} (Custom Prices)'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Comparison with commercial products
        st.markdown("### 💵 Perbandingan: Homemade vs Komersial")
        
        comparison_data = pd.DataFrame({
            "Jenis": ["Jamu Homemade (Custom)", "Jamu Komersial (Sachet)", "Suplemen Herbal (Kapsul)"],
            "Biaya per Hari (Rp)": [
                cost_per_day,
                15000,  # Estimate
                25000   # Estimate
            ]
        })
        
        fig_comparison = px.bar(
            comparison_data,
            x='Jenis',
            y='Biaya per Hari (Rp)',
            title='Perbandingan Biaya per Hari',
            color='Jenis',
            color_discrete_sequence=['green', 'orange', 'red']
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
        
        savings = 15000 - cost_per_day
        if savings > 0:
            st.success(f"""
            **💡 Penghematan:**
            - Jamu homemade: **Rp {cost_per_day:,.0f}/hari**
            - Jamu komersial: **Rp 15,000/hari** (estimasi)
            - **Hemat: Rp {savings:,.0f}/hari** atau **Rp {savings * 30:,.0f}/bulan**
            """)
        else:
            st.info(f"""
            **💡 Informasi:**
            - Jamu homemade: **Rp {cost_per_day:,.0f}/hari**
            - Jamu komersial: **Rp 15,000/hari** (estimasi)
            - Dengan harga bahan premium, biaya homemade bisa lebih tinggi namun kualitas terjamin
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 20px;">
    <p><strong>🍵 AgriSensa - Kalkulator Jamu Saintifik</strong></p>
    <p>Evidence-Based Traditional Indonesian Herbal Medicine Calculator</p>
    <p><small>Berdasarkan Penelitian B2P2TOOT & Program Saintifikasi Jamu Kemenkes RI</small></p>
    <p><small>Data diperbarui: Desember 2024</small></p>
</div>
""", unsafe_allow_html=True)
