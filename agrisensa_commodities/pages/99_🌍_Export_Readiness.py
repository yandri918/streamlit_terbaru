import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from services.export_readiness_service import (
    CERTIFICATIONS,
    EXPORT_DOCUMENTS,
    PHYTOSANITARY_PROCESS,
    PACKAGING_STANDARDS,
    BUYERS_DIRECTORY,
    COLD_CHAIN_GUIDE,
    HORTICULTURE_EXPORT,
    ExportReadinessService
)

# Page config
st.set_page_config(
    page_title="Export Readiness & Certification",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .cert-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .buyer-card {
        background: #f8f9fa;
        padding: 15px;
        border-left: 4px solid #007bff;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🌍 Export Readiness & Certification")
st.markdown("""
<div style='background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%); padding: 20px; border-radius: 10px; color: white;'>
    <h3>🚀 Akses Pasar Internasional dengan Sertifikasi Premium</h3>
    <p>✅ Premium price 2-3x lipat | ✅ Akses 50+ negara | ✅ Standarisasi kualitas global</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Create tabs
tabs = st.tabs([
    "📋 Overview",
    "📜 Certifications",
    "📄 Documentation",
    "🌱 Phytosanitary",
    "📦 Packaging",
    "🤝 Buyer Matching",
    "🚚 Logistics",
    "🥬 Horticulture Export",
    "✅ Readiness Assessment"
])

# TAB 1: OVERVIEW
with tabs[0]:
    st.markdown("## 🎯 Mengapa Ekspor?")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Premium Price", "2-3x", delta="vs domestic")
    with col2:
        st.metric("Market Size", "USD 2T+", delta="Global agri trade")
    with col3:
        st.metric("Countries", "50+", delta="Export destinations")
    with col4:
        st.metric("Certifications", "6+", delta="Available")
    
    st.markdown("---")
    
    st.markdown("### 💰 Benefits of Export")
    
    col_ben1, col_ben2 = st.columns(2)
    
    with col_ben1:
        st.markdown("""
        **Financial Benefits:**
        - 💵 Premium pricing (2-3x domestic)
        - 📈 Stable long-term contracts
        - 💰 Foreign currency earnings
        - 🌍 Diversified revenue streams
        - 📊 Economies of scale
        """)
    
    with col_ben2:
        st.markdown("""
        **Strategic Benefits:**
        - 🏆 Quality standardization
        - 🔒 Buyer confidence & trust
        - 🌟 Brand reputation
        - 📚 Knowledge transfer
        - 🤝 International partnerships
        """)
    
    st.markdown("---")
    
    st.markdown("### 📊 Export Success Stories")
    
    success_data = pd.DataFrame({
        "Komoditas": ["VCO", "Kopi Arabica", "Kakao", "Kelapa Sawit", "Udang"],
        "Harga Domestik (Rp/kg)": [150000, 80000, 35000, 12000, 120000],
        "Harga Export (Rp/kg)": [400000, 200000, 85000, 25000, 300000],
        "Premium (%)": [167, 150, 143, 108, 150]
    })
    
    fig_success = px.bar(
        success_data,
        x="Komoditas",
        y=["Harga Domestik (Rp/kg)", "Harga Export (Rp/kg)"],
        title="Perbandingan Harga Domestik vs Export",
        barmode="group",
        color_discrete_sequence=["#ff6b6b", "#4ecdc4"]
    )
    st.plotly_chart(fig_success, use_container_width=True)

# TAB 2: CERTIFICATIONS
with tabs[1]:
    st.markdown("## 📜 Sertifikasi Ekspor")
    
    st.info("💡 **Pilih sertifikasi yang sesuai dengan komoditas dan target pasar Anda**")
    
    # Certification comparison table
    cert_comparison = []
    for cert_name, cert_data in CERTIFICATIONS.items():
        cert_comparison.append({
            "Sertifikasi": cert_name,
            "Biaya/Tahun": cert_data['cost'],
            "Validity": cert_data['validity'],
            "Applicable To": ", ".join(cert_data['applicable_to'][:2]) + "...",
            "Benefits": cert_data['benefits'][:50] + "..."
        })
    
    df_cert = pd.DataFrame(cert_comparison)
    st.dataframe(df_cert, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Detailed certification info
    st.markdown("### 📋 Detail Sertifikasi")
    
    selected_cert = st.selectbox(
        "Pilih Sertifikasi untuk Detail:",
        list(CERTIFICATIONS.keys())
    )
    
    cert_detail = CERTIFICATIONS[selected_cert]
    
    col_cert1, col_cert2 = st.columns(2)
    
    with col_cert1:
        st.markdown(f"""
        <div class="cert-card">
            <h4>{selected_cert}</h4>
            <p><strong>💰 Biaya:</strong> {cert_detail['cost']}</p>
            <p><strong>⏱️ Validity:</strong> {cert_detail['validity']}</p>
            <p><strong>⏳ Process Time:</strong> {cert_detail['process_time']}</p>
            <p><strong>🏢 Certification Body:</strong> {cert_detail['certification_body']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_cert2:
        st.markdown("**📋 Requirements:**")
        for req in cert_detail['requirements']:
            st.markdown(f"- ✅ {req}")
        
        st.markdown(f"""
        **✨ Benefits:**
        {cert_detail['benefits']}
        
        **🔄 Renewal:**
        {cert_detail['renewal']}
        """)
    
    st.markdown("---")
    
    # Certification cost calculator
    st.markdown("### 🧮 Certification Cost Calculator")
    
    selected_certs = st.multiselect(
        "Pilih Sertifikasi yang Ingin Anda Dapatkan:",
        list(CERTIFICATIONS.keys())
    )
    
    if selected_certs:
        cost_result = ExportReadinessService.calculate_certification_cost(selected_certs)
        
        col_cost1, col_cost2 = st.columns(2)
        
        with col_cost1:
            st.metric("Total Investment", f"Rp {cost_result['total_cost']:,.0f}")
            st.caption("First year cost")
        
        with col_cost2:
            st.metric("Annual Cost", f"Rp {cost_result['annual_cost']:,.0f}")
            st.caption("Recurring yearly")
        
        # Breakdown
        st.markdown("**💼 Cost Breakdown:**")
        for detail in cost_result['details']:
            st.markdown(f"- **{detail['certification']}:** Rp {detail['cost']:,.0f} ({detail['validity']})")

# TAB 3: DOCUMENTATION
with tabs[2]:
    st.markdown("## 📄 Export Documentation")
    
    st.info("💡 **Checklist lengkap dokumen yang diperlukan untuk ekspor**")
    
    # Pre-Export Registration
    st.markdown("### 1️⃣ Pre-Export Registration")
    
    for doc_name, doc_desc in EXPORT_DOCUMENTS["Pre-Export Registration"].items():
        checked = st.checkbox(f"**{doc_name.replace('_', ' ')}:** {doc_desc}", key=f"pre_{doc_name}")
    
    st.markdown("---")
    
    # Shipping Documents
    st.markdown("### 2️⃣ Shipping Documents")
    
    for doc_name, doc_desc in EXPORT_DOCUMENTS["Shipping Documents"].items():
        checked = st.checkbox(f"**{doc_name.replace('_', ' ')}:** {doc_desc}", key=f"ship_{doc_name}")
    
    st.markdown("---")
    
    # Payment Documents
    st.markdown("### 3️⃣ Payment Documents")
    
    for doc_name, doc_desc in EXPORT_DOCUMENTS["Payment Documents"].items():
        checked = st.checkbox(f"**{doc_name.replace('_', ' ')}:** {doc_desc}", key=f"pay_{doc_name}")
    
    st.markdown("---")
    
    # Export timeline
    st.markdown("### 📅 Export Timeline")
    
    timeline_data = pd.DataFrame({
        "Week": [1, 2, 3, 4, 5, 6, 7, 8],
        "Activity": [
            "Registration & Licensing",
            "Product Certification",
            "Find Buyer",
            "Negotiate Contract",
            "Prepare Documentation",
            "Quality Inspection",
            "Shipping Arrangement",
            "Export & Delivery"
        ]
    })
    
    fig_timeline = px.timeline(
        timeline_data,
        x_start=[f"2024-01-{i:02d}" for i in range(1, 9)],
        x_end=[f"2024-01-{i+7:02d}" for i in range(1, 9)],
        y="Activity",
        title="Typical Export Timeline (8 weeks)"
    )
    st.plotly_chart(fig_timeline, use_container_width=True)

# TAB 4: PHYTOSANITARY
with tabs[3]:
    st.markdown("## 🌱 Phytosanitary Certificate")
    
    st.markdown(f"""
    **Definition:**
    {PHYTOSANITARY_PROCESS['definition']}
    
    **Validity:** {PHYTOSANITARY_PROCESS['validity']}
    
    **Issuing Authority:** {PHYTOSANITARY_PROCESS['issuing_authority']}
    """)
    
    st.markdown("---")
    
    col_phyto1, col_phyto2 = st.columns(2)
    
    with col_phyto1:
        st.markdown("### 📋 Requirements")
        for req in PHYTOSANITARY_PROCESS['requirements']:
            st.markdown(f"- ✅ {req}")
    
    with col_phyto2:
        st.markdown("### 📝 Process Steps")
        for step in PHYTOSANITARY_PROCESS['process_steps']:
            st.markdown(f"{step}")
    
    st.markdown("---")
    
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        st.metric("Cost", PHYTOSANITARY_PROCESS['cost'])
    
    with col_info2:
        st.metric("Processing Time", PHYTOSANITARY_PROCESS['processing_time'])
    
    st.success("🔗 **Apply Online:** https://karantina.pertanian.go.id (IQFAST system)")

# TAB 5: PACKAGING
with tabs[4]:
    st.markdown("## 📦 Packaging & Labeling Standards")
    
    st.info("💡 **Standar internasional untuk packaging dan labeling produk ekspor**")
    
    # International Requirements
    st.markdown("### 🌍 International Label Requirements")
    
    col_pack1, col_pack2 = st.columns(2)
    
    with col_pack1:
        for key, value in list(PACKAGING_STANDARDS["International_Requirements"].items())[:5]:
            st.markdown(f"**{key.replace('_', ' ')}:** {value}")
    
    with col_pack2:
        for key, value in list(PACKAGING_STANDARDS["International_Requirements"].items())[5:]:
            st.markdown(f"**{key.replace('_', ' ')}:** {value}")
    
    st.markdown("---")
    
    # Material Standards
    st.markdown("### 🏭 Material Standards")
    
    for key, value in PACKAGING_STANDARDS["Material_Standards"].items():
        st.markdown(f"- ✅ **{key.replace('_', ' ')}:** {value}")
    
    st.markdown("---")
    
    # Label Design
    st.markdown("### 🎨 Label Design Guidelines")
    
    for key, value in PACKAGING_STANDARDS["Label_Design"].items():
        st.markdown(f"- 📝 **{key.replace('_', ' ')}:** {value}")

# TAB 6: BUYER MATCHING
with tabs[5]:
    st.markdown("## 🤝 International Buyer Directory")
    
    st.info("💡 **Connect with 20+ verified international buyers**")
    
    # Market selection
    selected_market = st.selectbox(
        "Select Target Market:",
        list(BUYERS_DIRECTORY.keys())
    )
    
    buyers = BUYERS_DIRECTORY[selected_market]
    
    st.markdown(f"### 🏪 Buyers in {selected_market} ({len(buyers)} companies)")
    
    for buyer in buyers:
        st.markdown(f"""
        <div class="buyer-card">
            <h4>{buyer['name']}</h4>
            <p><strong>Products:</strong> {', '.join(buyer['products'])}</p>
            <p><strong>Contact:</strong> {buyer['contact']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📅 Upcoming Trade Shows")
    
    trade_shows = pd.DataFrame({
        "Event": ["Biofach (Organic)", "SIAL Paris", "Anuga", "Gulfood"],
        "Location": ["Nuremberg, Germany", "Paris, France", "Cologne, Germany", "Dubai, UAE"],
        "Date": ["Feb 2024", "Oct 2024", "Oct 2025", "Feb 2024"],
        "Focus": ["Organic products", "Food & beverage", "Food & beverage", "Middle East market"]
    })
    
    st.dataframe(trade_shows, use_container_width=True, hide_index=True)

# TAB 7: LOGISTICS
with tabs[6]:
    st.markdown("## 🚚 Logistics & Cold Chain")
    
    # Temperature requirements
    st.markdown("### 🌡️ Temperature Requirements")
    
    temp_data = []
    for product_type, temp in COLD_CHAIN_GUIDE["Temperature_Requirements"].items():
        temp_data.append({
            "Product Type": product_type.replace("_", " "),
            "Temperature": temp
        })
    
    df_temp = pd.DataFrame(temp_data)
    st.dataframe(df_temp, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Cold chain components
    st.markdown("### ❄️ Cold Chain Components")
    
    for component in COLD_CHAIN_GUIDE["Cold_Chain_Components"]:
        st.markdown(f"- ✅ {component}")
    
    st.markdown("---")
    
    # Logistics partners
    st.markdown("### 🤝 Logistics Partners")
    
    col_log1, col_log2 = st.columns(2)
    
    with col_log1:
        st.markdown("**Freight Forwarders:**")
        for partner in COLD_CHAIN_GUIDE["Logistics_Partners"]["Freight_Forwarders"]:
            st.markdown(f"- 📦 {partner}")
        
        st.markdown("**Shipping Lines:**")
        for partner in COLD_CHAIN_GUIDE["Logistics_Partners"]["Shipping_Lines"]:
            st.markdown(f"- 🚢 {partner}")
    
    with col_log2:
        st.markdown("**Cold Storage:**")
        for partner in COLD_CHAIN_GUIDE["Logistics_Partners"]["Cold_Storage"]:
            st.markdown(f"- ❄️ {partner}")
        
        st.markdown("**Customs Brokers:**")
        for partner in COLD_CHAIN_GUIDE["Logistics_Partners"]["Customs_Brokers"]:
            st.markdown(f"- 🛃 {partner}")
    
    st.markdown("---")
    
    # Shipping routes
    st.markdown("### 🗺️ Shipping Routes & Time")
    
    for destination, route in COLD_CHAIN_GUIDE["Shipping_Routes"].items():
        st.markdown(f"**{destination}:** {route}")

# TAB 8: HORTICULTURE EXPORT
with tabs[7]:
    st.markdown("## 🥬 Horticulture Export Calculator")
    
    st.info("💡 **Kalkulator khusus untuk ekspor produk hortikultura dengan breakdown biaya lengkap**")
    
    # Product selection
    col_hort1, col_hort2 = st.columns(2)
    
    with col_hort1:
        product_name = st.selectbox(
            "Pilih Produk Hortikultura:",
            list(HORTICULTURE_EXPORT.keys())
        )
    
    with col_hort2:
        volume_kg = st.number_input(
            "Volume Ekspor (kg):",
            min_value=100,
            max_value=50000,
            value=1000,
            step=100
        )
    
    if st.button("💰 Hitung Profitabilitas Ekspor", type="primary"):
        result = ExportReadinessService.calculate_horticulture_export(product_name, volume_kg)
        
        # Product info
        st.markdown("### 📋 Informasi Produk")
        
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.markdown(f"""
            **Export Grade:**
            {result['export_grade']}
            
            **Shelf Life:**
            {result['shelf_life']}
            """)
        
        with col_info2:
            st.markdown(f"""
            **Cold Chain:**
            {result['cold_chain']}
            
            **Rejection Rate:**
            {result['rejection_rate']}
            """)
        
        with col_info3:
            st.markdown(f"""
            **Main Markets:**
            {', '.join(result['main_markets'])}
            
            **Certifications:**
            {', '.join(result['certifications_required'])}
            """)
        
        st.markdown("---")
        
        # Price comparison
        st.markdown("### 💵 Price Comparison")
        
        col_price1, col_price2, col_price3 = st.columns(3)
        
        with col_price1:
            st.metric("Harga Domestik", f"Rp {result['price_domestic']:,}/kg")
        
        with col_price2:
            st.metric("Harga Export", f"Rp {result['price_export']:,}/kg")
        
        with col_price3:
            st.metric("Premium", result['premium'], delta="vs domestic")
        
        st.markdown("---")
        
        # Cost breakdown
        st.markdown("### 💰 Cost Breakdown")
        
        # Initialize session state for editable costs if not exists
        if 'custom_costs' not in st.session_state:
            st.session_state.custom_costs = {}
        if 'show_cost_editor' not in st.session_state:
            st.session_state.show_cost_editor = False
        
        costs = result['cost_breakdown']
        
        # Button to toggle edit mode (using session state to avoid refresh)
        col_btn1, col_btn2, col_btn3 = st.columns([2, 1, 2])
        with col_btn2:
            if not st.session_state.show_cost_editor:
                if st.button("✏️ Edit Costs", type="secondary", use_container_width=True, key=f"show_editor_{product_name}_{volume_kg}"):
                    st.session_state.show_cost_editor = True
                    st.rerun()
            else:
                if st.button("❌ Close Editor", type="secondary", use_container_width=True, key=f"hide_editor_{product_name}_{volume_kg}"):
                    st.session_state.show_cost_editor = False
                    st.rerun()
        
        # Create editable cost inputs
        if st.session_state.show_cost_editor:
            st.markdown("---")
            st.markdown("#### 📝 Editable Cost Components (Rp per kg)")
            
            # Use form to prevent auto-refresh on every input change
            with st.form(key=f"cost_form_{product_name}_{volume_kg}"):
                st.info("💡 Edit the costs below and click 'Recalculate' - no page refresh while editing!")
                
                # Initialize or get custom values
                key_prefix = f"{product_name}_{volume_kg}"
                
                # Use columns for better layout
                col_cost1, col_cost2 = st.columns(2)
                
                with col_cost1:
                    custom_product_cost = st.number_input(
                        "🌾 Product Cost (Farm Gate) - Rp/kg",
                        min_value=0,
                        value=int(result['price_domestic']),
                        step=1000,
                        key=f"form_product_cost_{key_prefix}",
                        help="Farm gate price per kg"
                    )
                    
                    custom_sorting = st.number_input(
                        "🔍 Sorting & Grading - Rp/kg",
                        min_value=0,
                        value=int(costs['sorting_grading'] / volume_kg),
                        step=100,
                        key=f"form_sorting_{key_prefix}",
                        help="Cost for sorting and grading per kg"
                    )
                    
                    custom_packaging = st.number_input(
                        "📦 Packaging - Rp/kg",
                        min_value=0,
                        value=int(costs['packaging'] / volume_kg),
                        step=100,
                        key=f"form_packaging_{key_prefix}",
                        help="Packaging materials and labor per kg"
                    )
                    
                    custom_cold_storage = st.number_input(
                        "❄️ Cold Storage - Rp/kg",
                        min_value=0,
                        value=int(costs['cold_storage'] / volume_kg),
                        step=100,
                        key=f"form_cold_storage_{key_prefix}",
                        help="Cold storage fees per kg"
                    )
                
                with col_cost2:
                    custom_phytosanitary = st.number_input(
                        "🌱 Phytosanitary Certificate - Rp/kg",
                        min_value=0,
                        value=int(costs['phytosanitary'] / volume_kg),
                        step=50,
                        key=f"form_phyto_{key_prefix}",
                        help="Phytosanitary certification cost per kg"
                    )
                    
                    custom_shipping = st.number_input(
                        "🚢 Shipping - Rp/kg",
                        min_value=0,
                        value=int(costs['shipping'] / volume_kg),
                        step=100,
                        key=f"form_shipping_{key_prefix}",
                        help="International shipping cost per kg"
                    )
                    
                    custom_insurance = st.number_input(
                        "🛡️ Insurance - Rp/kg",
                        min_value=0,
                        value=int(costs['insurance'] / volume_kg),
                        step=50,
                        key=f"form_insurance_{key_prefix}",
                        help="Cargo insurance per kg"
                    )
                    
                    custom_documentation = st.number_input(
                        "📄 Documentation - Rp/kg",
                        min_value=0,
                        value=int(costs['documentation'] / volume_kg),
                        step=50,
                        key=f"form_documentation_{key_prefix}",
                        help="Export documentation fees per kg"
                    )
                
                # Submit button
                submitted = st.form_submit_button("🔄 Recalculate Profitability", type="primary", use_container_width=True)
            
            # Only recalculate if form is submitted
            if submitted:
                # Recalculate with custom costs
                costs['product_cost'] = custom_product_cost * volume_kg
                costs['sorting_grading'] = custom_sorting * volume_kg
                costs['packaging'] = custom_packaging * volume_kg
                costs['cold_storage'] = custom_cold_storage * volume_kg
                costs['phytosanitary'] = custom_phytosanitary * volume_kg
                costs['shipping'] = custom_shipping * volume_kg
                costs['insurance'] = custom_insurance * volume_kg
                costs['documentation'] = custom_documentation * volume_kg
                
                costs['total_export_costs'] = (costs['sorting_grading'] + costs['packaging'] + 
                                              costs['cold_storage'] + costs['phytosanitary'] + 
                                              costs['shipping'] + costs['insurance'] + costs['documentation'])
                costs['total_cost'] = costs['product_cost'] + costs['total_export_costs']
                
                # Recalculate profit with custom costs
                result['revenue'] = result['saleable_volume'] * result['price_export']
                result['profit'] = result['revenue'] - costs['total_cost']
                result['profit_margin'] = round((result['profit'] / result['revenue'] * 100), 1) if result['revenue'] > 0 else 0
                result['roi'] = round((result['profit'] / costs['total_cost'] * 100), 1) if costs['total_cost'] > 0 else 0
                
                st.success("✅ Calculations updated with your custom costs!")
            
            st.markdown("---")
        
        # Display cost breakdown table
        cost_data = pd.DataFrame({
            "Cost Component": [
                "Product Cost (Farm Gate)",
                "Sorting & Grading",
                "Packaging",
                "Cold Storage",
                "Phytosanitary Certificate",
                "Shipping",
                "Insurance",
                "Documentation"
            ],
            "Amount (Rp)": [
                costs['product_cost'],
                costs['sorting_grading'],
                costs['packaging'],
                costs['cold_storage'],
                costs['phytosanitary'],
                costs['shipping'],
                costs['insurance'],
                costs['documentation']
            ],
            "Per Kg (Rp)": [
                costs['product_cost'] / volume_kg,
                costs['sorting_grading'] / volume_kg,
                costs['packaging'] / volume_kg,
                costs['cold_storage'] / volume_kg,
                costs['phytosanitary'] / volume_kg,
                costs['shipping'] / volume_kg,
                costs['insurance'] / volume_kg,
                costs['documentation'] / volume_kg
            ]
        })
        
        st.dataframe(cost_data, use_container_width=True, hide_index=True)
        
        # Cost composition pie chart
        fig_cost = px.pie(
            values=[
                costs['product_cost'],
                costs['sorting_grading'],
                costs['packaging'],
                costs['cold_storage'],
                costs['phytosanitary'],
                costs['shipping'],
                costs['insurance'],
                costs['documentation']
            ],
            names=[
                "Product Cost",
                "Sorting & Grading",
                "Packaging",
                "Cold Storage",
                "Phytosanitary",
                "Shipping",
                "Insurance",
                "Documentation"
            ],
            title="Cost Composition"
        )
        st.plotly_chart(fig_cost, use_container_width=True)
        
        st.markdown("---")
        
        # Profitability analysis
        st.markdown("### 📊 Profitability Analysis")
        
        col_prof1, col_prof2, col_prof3, col_prof4 = st.columns(4)
        
        with col_prof1:
            st.metric("Volume Input", f"{volume_kg:,} kg")
            st.caption("Harvest volume")
        
        with col_prof2:
            st.metric("Saleable Volume", f"{result['saleable_volume']:,.0f} kg")
            st.caption(f"After {result['rejection_rate']} rejection")
        
        with col_prof3:
            st.metric("Total Cost", f"Rp {costs['total_cost']:,.0f}")
            st.caption(f"Rp {costs['total_cost']/volume_kg:,.0f}/kg")
        
        with col_prof4:
            st.metric("Revenue", f"Rp {result['revenue']:,.0f}")
            st.caption(f"Rp {result['revenue']/result['saleable_volume']:,.0f}/kg")
        
        # Profit metrics
        col_profit1, col_profit2, col_profit3 = st.columns(3)
        
        with col_profit1:
            st.metric("Profit", f"Rp {result['profit']:,.0f}", delta=f"{result['profit_margin']}% margin")
        
        with col_profit2:
            st.metric("ROI", f"{result['roi']}%")
        
        with col_profit3:
            profit_per_kg = result['profit'] / volume_kg
            st.metric("Profit per kg", f"Rp {profit_per_kg:,.0f}")
        
        # Profit visualization
        fig_profit = go.Figure(data=[
            go.Bar(name='Total Cost', x=['Financial Summary'], y=[costs['total_cost']], marker_color='#ff6b6b'),
            go.Bar(name='Revenue', x=['Financial Summary'], y=[result['revenue']], marker_color='#4ecdc4'),
            go.Bar(name='Profit', x=['Financial Summary'], y=[result['profit']], marker_color='#95e1d3')
        ])
        fig_profit.update_layout(title="Cost vs Revenue vs Profit", barmode='group')
        st.plotly_chart(fig_profit, use_container_width=True)
        
        # Recommendations
        st.markdown("---")
        st.markdown("### 💡 Export Recommendations")
        
        if result['profit_margin'] >= 20:
            st.success(f"""
            ✅ **PROFITABLE!** Margin {result['profit_margin']}% sangat baik untuk ekspor.
            
            **Next Steps:**
            1. Dapatkan sertifikasi: {', '.join(result['certifications_required'])}
            2. Setup cold chain {result['cold_chain']}
            3. Contact buyers di: {', '.join(result['main_markets'])}
            4. Prepare phytosanitary certificate
            """)
        elif result['profit_margin'] >= 10:
            st.warning(f"""
            ⚠️ **MARGINAL** Margin {result['profit_margin']}% cukup, tapi bisa ditingkatkan.
            
            **Optimization Tips:**
            1. Kurangi rejection rate dengan quality control lebih ketat
            2. Negosiasi harga shipping untuk volume lebih besar
            3. Target pasar premium dengan sertifikasi organic
            4. Improve packaging efficiency
            """)
        else:
            st.error(f"""
            ❌ **NOT PROFITABLE** Margin {result['profit_margin']}% terlalu rendah.
            
            **Perbaikan Diperlukan:**
            1. Tingkatkan harga jual atau kurangi biaya produksi
            2. Fokus ke pasar domestik dulu
            3. Improve quality untuk reduce rejection rate
            4. Consider value-added processing
            """)

# TAB 9: READINESS ASSESSMENT
with tabs[8]:
    st.markdown("## ✅ Export Readiness Assessment")
    
    st.info("💡 **Evaluate your export readiness and get personalized recommendations**")
    
    # Assessment form
    st.markdown("### 📝 Self-Assessment")
    
    commodity = st.selectbox(
        "Komoditas Anda:",
        ["Hortikultura", "Buah", "Sayuran", "Tanaman Pangan", "Perkebunan", "Livestock"]
    )
    
    col_assess1, col_assess2 = st.columns(2)
    
    with col_assess1:
        has_gap = st.checkbox("✅ Saya memiliki sertifikasi GAP")
        has_organic = st.checkbox("✅ Saya memiliki sertifikasi Organic")
        has_haccp = st.checkbox("✅ Saya memiliki sertifikasi HACCP")
    
    with col_assess2:
        has_documentation = st.checkbox("✅ Saya memiliki dokumen ekspor lengkap (NIB, API, SKA)")
        has_buyer = st.checkbox("✅ Saya sudah memiliki buyer potensial")
        has_capacity = st.checkbox("✅ Saya mampu produksi konsisten (volume & kualitas)")
    
    if st.button("🎯 Assess My Readiness", type="primary"):
        result = ExportReadinessService.assess_readiness(
            commodity, has_gap, has_organic, has_haccp, has_documentation
        )
        
        # Display score
        st.markdown("### 📊 Your Export Readiness Score")
        
        col_score1, col_score2, col_score3 = st.columns(3)
        
        with col_score1:
            st.metric("Score", f"{result['score']}/100")
        
        with col_score2:
            st.metric("Level", result['level'])
        
        with col_score3:
            if result['level'] == "READY":
                st.success(result['message'])
            elif result['level'] == "ALMOST READY":
                st.warning(result['message'])
            else:
                st.error(result['message'])
        
        # Progress bar
        fig_progress = go.Figure(go.Indicator(
            mode="gauge+number",
            value=result['score'],
            title={'text': "Readiness Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 80
                }
            }
        ))
        st.plotly_chart(fig_progress, use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 Recommendations")
        
        for rec in result['recommendations']:
            st.markdown(rec)
        
        # Next steps
        st.markdown("### 🚀 Next Steps")
        
        if result['score'] >= 80:
            st.success("""
            **Anda siap untuk ekspor! Langkah selanjutnya:**
            1. 🔍 Cari buyer di tab "Buyer Matching"
            2. 📄 Lengkapi dokumen di tab "Documentation"
            3. 🚚 Arrange logistics di tab "Logistics"
            4. 📧 Contact us untuk export assistance
            """)
        else:
            st.warning("""
            **Perlu persiapan lebih lanjut:**
            1. 📜 Dapatkan sertifikasi yang diperlukan
            2. 📋 Lengkapi dokumentasi
            3. 🏭 Tingkatkan kapasitas produksi
            4. 📚 Ikuti training export readiness
            """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌍 <strong>AgriSensa Export Readiness Module</strong></p>
    <p>For export assistance, contact: export@agrisensa.com | WhatsApp: +62-xxx-xxxx-xxxx</p>
</div>
""", unsafe_allow_html=True)
