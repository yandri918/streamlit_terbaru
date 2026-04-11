# 💰 Analisis Usaha Krisan
# Business analysis, ROI, dan break-even

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Analisis Usaha", page_icon="💰", layout="wide")

st.markdown("## 💰 Analisis Usaha Budidaya Krisan Spray")
st.info("Perhitungan investasi, ROI, break-even point, dan proyeksi bisnis lengkap.")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏗️ Investasi Awal", 
    "📊 Analisis Operasional", 
    "💰 Break-Even Analysis",
    "📈 ROI & Payback", 
    "🎯 Skenario Bisnis"
])

# TAB 1: Investasi Awal
with tab1:
    st.subheader("🏗️ Kalkulasi Investasi Awal")
    
    st.markdown("Masukkan parameter untuk menghitung kebutuhan modal awal:")
    
    col_in, col_out = st.columns([1, 1.5])
    
    with col_in:
        greenhouse_area = st.number_input("📐 Luas Greenhouse (m²)", 200, 5000, 1000, step=100)
        
        with st.expander("🏗️ Detail Biaya Konstruksi", expanded=True):
            cost_greenhouse_per_m2 = st.number_input("Biaya Greenhouse (Rp/m²)", 100000, 500000, 250000, step=10000)
            cost_irrigation = st.number_input("Sistem Irigasi (Rp total)", 5000000, 50000000, 15000000, step=1000000)
            cost_lighting = st.number_input("Instalasi Lampu (Rp total)", 5000000, 30000000, 10000000, step=1000000)
            cost_shading = st.number_input("Plastik Hitam/Shading (Rp total)", 2000000, 20000000, 5000000, step=500000)
            cost_equipment = st.number_input("Peralatan Lain (Rp)", 2000000, 20000000, 8000000, step=1000000)
        
        working_capital = st.number_input("💵 Modal Kerja Awal (3 bulan)", 10000000, 100000000, 30000000, step=5000000)
    
    with col_out:
        # Calculate totals
        cost_greenhouse_total = greenhouse_area * cost_greenhouse_per_m2
        total_fixed_investment = cost_greenhouse_total + cost_irrigation + cost_lighting + cost_shading + cost_equipment
        total_investment = total_fixed_investment + working_capital
        
        st.markdown("### 📊 Ringkasan Investasi")
        
        investment_data = pd.DataFrame({
            "Komponen": ["Konstruksi Greenhouse", "Sistem Irigasi", "Instalasi Lampu", 
                        "Plastik Hitam/Shading", "Peralatan Lain", "Modal Kerja"],
            "Biaya (Rp)": [cost_greenhouse_total, cost_irrigation, cost_lighting, 
                          cost_shading, cost_equipment, working_capital]
        })
        
        st.dataframe(investment_data, use_container_width=True, hide_index=True)
        
        st.metric("**TOTAL INVESTASI**", f"Rp {total_investment:,.0f}")
        st.metric("Investasi per m²", f"Rp {total_investment/greenhouse_area:,.0f}/m²")
        
        # Pie chart
        fig = go.Figure(data=[go.Pie(
            labels=investment_data["Komponen"],
            values=investment_data["Biaya (Rp)"],
            hole=0.4,
            marker_colors=['#ec4899', '#f472b6', '#f9a8d4', '#fbcfe8', '#fce7f3', '#10b981']
        )])
        fig.update_layout(title="Distribusi Investasi", height=350)
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: Analisis Operasional
with tab2:
    st.subheader("📊 Analisis Biaya & Pendapatan Operasional")
    
    # Sync with house_database and krisan_data
    if 'house_database' in st.session_state and st.session_state.house_database:
        house_db = st.session_state.house_database
        num_houses = len(house_db)
        total_beds = sum(h.get('beds', 12) for h in house_db.values())
        total_plants_synced = sum(h.get('total_plants', 0) for h in house_db.values())
        
        st.success(f"📊 Data tersinkronisasi: **{num_houses} house**, **{total_beds} bedengan**, **{total_plants_synced:,} tanaman/siklus**")
        use_synced = True
    else:
        use_synced = False
        total_plants_synced = 0
        st.info("💡 Sinkronkan data dari Kalkulator Produksi untuk hasil akurat")
    
    # Get data from Kalkulator Produksi (Tab 3)
    krisan_data = st.session_state.get('krisan_data', {})
    
    # DEBUG: Check if data is coming through
    with st.expander("🐛 Debug Data Session"):
        st.write("Raw keys in krisan_data:", list(krisan_data.keys()))
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.write("Old Costs:")
            st.write(f"Bibit: {krisan_data.get('rab_bibit', 'Not Found')}")
            st.write(f"Pupuk: {krisan_data.get('rab_pupuk', 'Not Found')}")
        with col_d2:
            st.write("New Costs:")
            st.write(f"Media: {krisan_data.get('rab_media', 'Not Found')}")
            st.write(f"Mulsa: {krisan_data.get('rab_mulsa', 'Not Found')}")
            st.write(f"Packaging: {krisan_data.get('rab_packaging', 'Not Found')}")
    
    # Use synced data or defaults
    if use_synced and total_plants_synced > 0:
        total_plants = total_plants_synced
        survival_rate = krisan_data.get('survival_rate', 85) / 100
        stems_per_plant = krisan_data.get('stems_per_plant', 3.5)
        cycles_per_year = 3  # Default
        avg_selling_price = 12000  # Default, user can override
        
        # Calculate from synced data
        surviving_plants = int(total_plants * survival_rate)
        total_stems = int(surviving_plants * stems_per_plant)
        
        # Get RAB data if available
        cost_cutting = krisan_data.get('rab_bibit', total_plants * 400)
        cost_fertilizer = krisan_data.get('rab_pupuk', total_beds * 50000)
        cost_pesticide = krisan_data.get('rab_pestisida', total_beds * 30000)
        cost_electricity = krisan_data.get('rab_listrik', 500000 * 4)
        cost_labor = krisan_data.get('rab_tenaga_kerja', 80000 * 90)
        cost_other = krisan_data.get('rab_lainnya', 2000000)
        
        # New cost components from Tab 3
        cost_media = krisan_data.get('rab_media', 0)
        cost_mulsa = krisan_data.get('rab_mulsa', 0)
        cost_consumables = krisan_data.get('rab_consumables', 0)
        cost_water = krisan_data.get('rab_water', 0)
        cost_maintenance = krisan_data.get('rab_maintenance', 0)
        cost_grading = krisan_data.get('rab_grading', 0)
        cost_packaging = krisan_data.get('rab_packaging', 0)
        cost_transport = krisan_data.get('rab_transport', 0)
    else:
        # Fallback to manual input
        st.warning("⚠️ Data belum tersinkronisasi. Gunakan input manual atau isi Kalkulator Produksi terlebih dahulu.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📝 Parameter Produksi")
            density = st.slider("Densitas (tanaman/m²)", 40, 80, 64)
            total_plants = greenhouse_area * density if 'greenhouse_area' in dir() else 76800
            
            survival_rate = st.slider("✅ Survival Rate (%)", 70, 95, 85) / 100
            stems_per_plant = st.slider("🌸 Tangkai per Tanaman", 1.0, 5.0, 3.5, 0.5)
            cycles_per_year = st.slider("📅 Siklus per Tahun", 2, 4, 3)
            
            st.markdown("### 💰 Parameter Harga")
            avg_selling_price = st.number_input("💵 Harga Jual Rata-rata (Rp/tangkai)", 500, 25000, 12000, 500)
        
        with col2:
            st.markdown("### 📋 Biaya Operasional per Siklus")
            
            surviving_plants = int(total_plants * survival_rate)
            total_stems = int(surviving_plants * stems_per_plant)
            
            # Manual cost inputs
            cost_cutting = total_plants * 400
            cost_fertilizer = st.number_input("Pupuk (Rp)", 0, 50000000, 2500000, 100000)
            cost_pesticide = st.number_input("Pestisida (Rp)", 0, 20000000, 1500000, 100000)
            cost_electricity = st.number_input("Listrik (Rp)", 0, 5000000, 2000000, 100000)
            cost_labor = st.number_input("Tenaga Kerja (Rp)", 0, 20000000, 7200000, 100000)
            cost_other = st.number_input("Lain-lain (Rp)", 0, 10000000, 2000000, 100000)
            
            # Default 0 for new components in manual mode to keep it simple
            cost_media = 0
            cost_mulsa = 0
            cost_consumables = 0
            cost_water = 0
            cost_maintenance = 0
            cost_grading = 0
            cost_packaging = 0
            cost_transport = 0
    
    # Calculate totals (including all NEW components)
    total_cost_cycle = (
        cost_cutting + cost_fertilizer + cost_pesticide + cost_electricity + cost_labor + cost_other +
        cost_media + cost_mulsa + cost_consumables + cost_water + cost_maintenance + 
        cost_grading + cost_packaging + cost_transport
    )
    
    # Allow user to override selling price and cycles
    st.markdown("---")
    st.markdown("### 💰 Parameter Penjualan")
    
    price_col, cycle_col = st.columns(2)
    with price_col:
        avg_selling_price = st.number_input("💵 Harga Jual (Rp/tangkai)", 500, 25000, avg_selling_price, 500)
    with cycle_col:
        cycles_per_year = st.slider("📅 Siklus per Tahun", 2, 4, cycles_per_year if 'cycles_per_year' in dir() else 3, key="cycles_override")
    
    # Revenue calculations
    revenue_cycle = total_stems * avg_selling_price
    revenue_year = revenue_cycle * cycles_per_year
    
    total_cost_year = total_cost_cycle * cycles_per_year
    
    profit_cycle = revenue_cycle - total_cost_cycle
    profit_year = profit_cycle * cycles_per_year
    
    # Display summary
    st.markdown("---")
    st.markdown("### 📊 Ringkasan per Siklus")
    
    col_summary = st.columns(4)
    with col_summary[0]:
        st.metric("🌸 Produksi", f"{total_stems:,} tangkai")
    with col_summary[1]:
        st.metric("💵 Pendapatan", f"Rp {revenue_cycle:,.0f}")
    with col_summary[2]:
        st.metric("💸 Biaya", f"Rp {total_cost_cycle:,.0f}")
    with col_summary[3]:
        margin_pct = (profit_cycle/revenue_cycle*100) if revenue_cycle > 0 else 0
        st.metric("📈 **PROFIT**", f"Rp {profit_cycle:,.0f}", 
                  delta=f"Margin {margin_pct:.1f}%")
    
    st.markdown("---")
    
    # Annual summary
    st.markdown("### 📅 Ringkasan Tahunan")
    
    annual_cols = st.columns(4)
    
    with annual_cols[0]:
        st.metric("Produksi/Tahun", f"{total_stems * cycles_per_year:,} tangkai")
    with annual_cols[1]:
        st.metric("Pendapatan/Tahun", f"Rp {revenue_year:,.0f}")
    with annual_cols[2]:
        st.metric("Biaya/Tahun", f"Rp {total_cost_year:,.0f}")
    with annual_cols[3]:
        st.metric("**PROFIT/Tahun**", f"Rp {profit_year:,.0f}")

# TAB 3: BREAK-EVEN ANALYSIS
with tab3:
    st.subheader("💰 Break-Even Point Analysis")
    
    st.markdown("""
    ### Apa itu Break-Even Point?
    
    **BEP** adalah titik dimana **Total Revenue = Total Cost** (tidak untung, tidak rugi).
    
    **Formula:**
    
    $$BEP_{tangkai} = \\frac{Biaya\\ Tetap}{Harga\\ Jual - Biaya\\ Variabel\\ per\\ Tangkai}$$
    """)
    
    # Get data from previous tabs or recalculate
    if 'total_stems' not in dir() or 'avg_selling_price' not in dir():
        # Recalculate with defaults
        if 'house_database' in st.session_state and st.session_state.house_database:
            house_db = st.session_state.house_database
            total_plants_calc = sum(h.get('total_plants', 0) for h in house_db.values())
            total_beds_calc = sum(h.get('beds', 12) for h in house_db.values())
        else:
            total_plants_calc = greenhouse_area * 64
            total_beds_calc = greenhouse_area / 10
        
        survival_rate_calc = 0.9
        stems_per_plant_calc = 1.0
        cycles_per_year_calc = 3
        avg_selling_price_calc = 1000
        
        harvested_calc = int(total_plants_calc * survival_rate_calc)
        total_stems_calc = int(harvested_calc * stems_per_plant_calc)
        
        # Costs
        cost_cutting_calc = total_plants_calc * 400
        cost_fertilizer_calc = total_beds_calc * 50000
        cost_pesticide_calc = total_beds_calc * 30000
        cost_electricity_calc = 500000 * 4
        cost_labor_calc = 80000 * 90
        cost_other_calc = 2000000
        
        total_cost_cycle_calc = cost_cutting_calc + cost_fertilizer_calc + cost_pesticide_calc + cost_electricity_calc + cost_labor_calc + cost_other_calc
    else:
        total_stems_calc = total_stems
        avg_selling_price_calc = avg_selling_price
        total_cost_cycle_calc = total_cost_cycle
        cycles_per_year_calc = cycles_per_year if 'cycles_per_year' in dir() else 3
    
    # Fixed vs Variable costs
    # Fixed costs per cycle (depreciation, etc.)
    if 'total_investment' in dir():
        # Depreciation calculation
        # Assume 5 year lifespan for greenhouse, 70% depreciable
        depreciation_per_year = (total_investment * 0.7) / 5
        depreciation_per_cycle = depreciation_per_year / cycles_per_year_calc
    else:
        # Default depreciation based on typical investment
        # Typical: Rp 200M for 4 houses, 3 cycles/year
        # = Rp 200M * 0.7 / 5 / 3 = Rp 9.3M per cycle
        depreciation_per_cycle = 10000000  # Default Rp 10M per cycle
    
    # Add overhead costs (admin, marketing, packaging, etc.)
    # Typically 15-20% of operational costs
    overhead_percentage = 0.15
    overhead_per_cycle = total_cost_cycle_calc * overhead_percentage
    
    # Fixed costs per cycle (depreciation only)
    biaya_tetap_cycle = depreciation_per_cycle
    
    # Variable costs (operational costs from RAB)
    biaya_variabel_cycle = total_cost_cycle_calc
    
    # Total costs = Operational + Depreciation + Overhead
    total_biaya_cycle = biaya_variabel_cycle + depreciation_per_cycle + overhead_per_cycle
    
    # Cost per stem (more realistic now)
    biaya_per_tangkai = total_biaya_cycle / total_stems_calc if total_stems_calc > 0 else 0
    biaya_variabel_per_tangkai = biaya_variabel_cycle / total_stems_calc if total_stems_calc > 0 else 0
    
    # Display cost breakdown
    st.info(f"""
    **💰 Breakdown Biaya per Siklus:**
    - Biaya Operasional: Rp {biaya_variabel_cycle:,.0f}
    - Depreciation: Rp {depreciation_per_cycle:,.0f}
    - Overhead (15%): Rp {overhead_per_cycle:,.0f}
    - **Total Biaya**: Rp {total_biaya_cycle:,.0f}
    - **Cost per Tangkai**: Rp {biaya_per_tangkai:,.0f}
    """)
    
    # Create sub-tabs
    subtab_bep, subtab_sens, subtab_profit = st.tabs([
        "📈 Break-Even Point",
        "🔍 Sensitivity Analysis",
        "💹 Profit Scenarios"
    ])
    
    # SUBTAB 1: BEP
    with subtab_bep:
        st.markdown("### 📊 Break-Even Point Calculation")
        
        # Calculate BEP
        if avg_selling_price_calc > biaya_variabel_per_tangkai:
            contribution_margin = avg_selling_price_calc - biaya_variabel_per_tangkai
            
            if biaya_tetap_cycle > 0:
                bep_tangkai = biaya_tetap_cycle / contribution_margin
                bep_rupiah = bep_tangkai * avg_selling_price_calc
            else:
                bep_tangkai = 0
                bep_rupiah = 0
                st.warning("""
                ⚠️ **Tidak Ada Biaya Tetap Terdeteksi**
                
                BEP = 0 (setiap penjualan langsung profit)
                """)
            
            # Margin of Safety
            actual_sales_rupiah = total_stems_calc * avg_selling_price_calc
            mos_rupiah = actual_sales_rupiah - bep_rupiah
            mos_percentage = (mos_rupiah / actual_sales_rupiah) * 100 if actual_sales_rupiah > 0 else 0
            
            # Display Results
            col_bep1, col_bep2, col_bep3 = st.columns(3)
            
            with col_bep1:
                st.metric("BEP (tangkai)", f"{bep_tangkai:,.0f} tangkai")
                st.caption("Minimal penjualan untuk BEP")
            
            with col_bep2:
                st.metric("BEP (Rupiah)", f"Rp {bep_rupiah:,.0f}")
                st.caption("Revenue minimal untuk BEP")
            
            with col_bep3:
                st.metric("Contribution Margin", f"Rp {contribution_margin:,.0f}")
                st.caption("Per tangkai contribution")
            
            # Margin of Safety
            st.markdown("### 🛡️ Margin of Safety (MOS)")
            
            col_mos1, col_mos2, col_mos3 = st.columns(3)
            
            with col_mos1:
                st.metric("MOS (Rupiah)", f"Rp {mos_rupiah:,.0f}")
            
            with col_mos2:
                st.metric("MOS (%)", f"{mos_percentage:.1f}%")
            
            with col_mos3:
                actual_profit = actual_sales_rupiah - total_biaya_cycle
                st.metric("Actual Profit", f"Rp {actual_profit:,.0f}")
            
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
            tangkai_range = np.linspace(0, bep_tangkai * 2, 100)
            total_cost_line = biaya_tetap_cycle + (biaya_variabel_per_tangkai * tangkai_range)
            total_revenue_line = avg_selling_price_calc * tangkai_range
            
            fig_bep = go.Figure()
            
            # Total Cost line
            fig_bep.add_trace(go.Scatter(
                x=tangkai_range,
                y=total_cost_line,
                mode='lines',
                name='Total Cost',
                line=dict(color='red', width=2)
            ))
            
            # Total Revenue line
            fig_bep.add_trace(go.Scatter(
                x=tangkai_range,
                y=total_revenue_line,
                mode='lines',
                name='Total Revenue',
                line=dict(color='green', width=2)
            ))
            
            # BEP point
            fig_bep.add_trace(go.Scatter(
                x=[bep_tangkai],
                y=[bep_rupiah],
                mode='markers',
                name='Break-Even Point',
                marker=dict(size=15, color='blue', symbol='star')
            ))
            
            # Actual sales point
            fig_bep.add_trace(go.Scatter(
                x=[total_stems_calc],
                y=[actual_sales_rupiah],
                mode='markers',
                name='Target Sales',
                marker=dict(size=12, color='orange', symbol='diamond')
            ))
            
            fig_bep.update_layout(
                title='Break-Even Analysis - Krisan Spray',
                xaxis_title='Quantity (tangkai)',
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
                    values=[biaya_tetap_cycle, biaya_variabel_cycle],
                    hole=.3,
                    marker_colors=['#ec4899', '#f472b6']
                )])
                fig_pie.update_layout(title='Cost Distribution', height=300)
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col_cost2:
                st.markdown("**Cost Breakdown:**")
                cost_breakdown = pd.DataFrame({
                    'Type': ['Biaya Operasional', 'Depreciation', 'Overhead (15%)', 'Total', 'Cost per Tangkai'],
                    'Amount': [
                        f"Rp {biaya_variabel_cycle:,.0f}",
                        f"Rp {depreciation_per_cycle:,.0f}",
                        f"Rp {overhead_per_cycle:,.0f}",
                        f"Rp {total_biaya_cycle:,.0f}",
                        f"Rp {biaya_per_tangkai:,.0f}/tangkai"
                    ],
                    'Share (%)': [
                        f"{(biaya_variabel_cycle/total_biaya_cycle*100):.1f}%" if total_biaya_cycle > 0 else "0%",
                        f"{(depreciation_per_cycle/total_biaya_cycle*100):.1f}%" if total_biaya_cycle > 0 else "0%",
                        f"{(overhead_per_cycle/total_biaya_cycle*100):.1f}%" if total_biaya_cycle > 0 else "0%",
                        "100.0%",
                        "-"
                    ]
                })
                st.dataframe(cost_breakdown, use_container_width=True, hide_index=True)
                
                st.caption(f"""
                💡 **Cost per Tangkai** = Total Biaya / Total Produksi
                
                = Rp {total_biaya_cycle:,.0f} / {total_stems_calc:,.0f} tangkai
                = **Rp {biaya_per_tangkai:,.0f}** per tangkai
                
                ✅ Sudah termasuk depreciation dan overhead
                """)
        
        else:
            st.error(f"""
            ⚠️ **Tidak Bisa Hitung BEP!**
            
            Harga jual (Rp {avg_selling_price_calc:,.0f}) harus lebih besar dari biaya variabel per tangkai (Rp {biaya_variabel_per_tangkai:,.0f})
            
            **Solusi:**
            - Naikkan harga jual, atau
            - Turunkan biaya variabel
            """)
    
    # SUBTAB 2: SENSITIVITY ANALYSIS
    with subtab_sens:
        st.subheader("🔍 Sensitivity Analysis")
        
        st.markdown("""
        ### Analisis Sensitivitas
        
        Bagaimana profit berubah jika ada perubahan pada:
        - Harga jual
        - Volume penjualan (yield)
        """)
        
        # Price Sensitivity
        st.markdown("#### 📊 Price Sensitivity")
        
        price_changes = np.array([-20, -10, 0, 10, 20])
        new_prices = avg_selling_price_calc * (1 + price_changes/100)
        
        price_sens_data = []
        for i, change in enumerate(price_changes):
            new_price = new_prices[i]
            new_revenue = total_stems_calc * new_price
            new_profit = new_revenue - total_biaya_cycle
            new_roi = (new_profit / total_biaya_cycle * 100) if total_biaya_cycle > 0 else 0
            
            price_sens_data.append({
                'Price Change (%)': f"{change:+.0f}%",
                'New Price': f"Rp {new_price:,.0f}",
                'Revenue': f"Rp {new_revenue:,.0f}",
                'Profit': f"Rp {new_profit:,.0f}",
                'ROI (%)': f"{new_roi:.1f}%"
            })
        
        price_sens_df = pd.DataFrame(price_sens_data)
        st.dataframe(price_sens_df, use_container_width=True, hide_index=True)
        
        # Yield Sensitivity
        st.markdown("#### 🌸 Yield Sensitivity")
        
        yield_changes = np.array([-20, -10, 0, 10, 20])
        new_yields = total_stems_calc * (1 + yield_changes/100)
        
        yield_sens_data = []
        for i, change in enumerate(yield_changes):
            new_yield = new_yields[i]
            new_revenue = new_yield * avg_selling_price_calc
            new_profit = new_revenue - total_biaya_cycle
            new_roi = (new_profit / total_biaya_cycle * 100) if total_biaya_cycle > 0 else 0
            
            yield_sens_data.append({
                'Yield Change (%)': f"{change:+.0f}%",
                'New Yield': f"{new_yield:,.0f} tangkai",
                'Revenue': f"Rp {new_revenue:,.0f}",
                'Profit': f"Rp {new_profit:,.0f}",
                'ROI (%)': f"{new_roi:.1f}%"
            })
        
        yield_sens_df = pd.DataFrame(yield_sens_data)
        st.dataframe(yield_sens_df, use_container_width=True, hide_index=True)
        
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
            line=dict(color='#ec4899', width=2),
            marker=dict(size=8)
        ))
        
        # Yield sensitivity line
        yield_profits = [float(row['Profit'].replace('Rp ', '').replace(',', '')) for row in yield_sens_data]
        fig_sens.add_trace(go.Scatter(
            x=yield_changes,
            y=yield_profits,
            mode='lines+markers',
            name='Yield Sensitivity',
            line=dict(color='#10b981', width=2),
            marker=dict(size=8)
        ))
        
        fig_sens.update_layout(
            title='Profit Sensitivity to Price & Yield Changes',
            xaxis_title='Change (%)',
            yaxis_title='Profit (Rp)',
            height=400
        )
        
        st.plotly_chart(fig_sens, use_container_width=True)
    
    # SUBTAB 3: PROFIT SCENARIOS
    with subtab_profit:
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
            scenario_price = avg_selling_price_calc * multipliers['price_mult']
            scenario_yield = total_stems_calc * multipliers['yield_mult']
            scenario_cost = total_biaya_cycle * multipliers['cost_mult']
            scenario_revenue = scenario_price * scenario_yield
            scenario_profit = scenario_revenue - scenario_cost
            scenario_roi = (scenario_profit / scenario_cost * 100) if scenario_cost > 0 else 0
            
            # Calculate BEP for scenario
            scenario_var_cost_per_unit = (biaya_variabel_cycle * multipliers['cost_mult']) / scenario_yield if scenario_yield > 0 else 0
            scenario_contribution = scenario_price - scenario_var_cost_per_unit
            scenario_bep = (biaya_tetap_cycle * multipliers['cost_mult']) / scenario_contribution if scenario_contribution > 0 else 0
            
            scenario_results.append({
                'Scenario': scenario_name,
                'Price': f"Rp {scenario_price:,.0f}",
                'Yield': f"{scenario_yield:,.0f} tangkai",
                'Cost': f"Rp {scenario_cost:,.0f}",
                'Revenue': f"Rp {scenario_revenue:,.0f}",
                'Profit': f"Rp {scenario_profit:,.0f}",
                'ROI (%)': f"{scenario_roi:.1f}%",
                'BEP (tangkai)': f"{scenario_bep:,.0f}"
            })
        
        scenario_df = pd.DataFrame(scenario_results)
        st.dataframe(scenario_df, use_container_width=True, hide_index=True)
        
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
                marker_color=['#ef4444', '#fbbf24', '#10b981']
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
        
        1. **Break-Even Point:** {bep_tangkai:,.0f} tangkai @ Rp {bep_rupiah:,.0f}
        2. **Current Target:** {total_stems_calc:,.0f} tangkai ({(total_stems_calc/bep_tangkai*100):.0f}% of BEP)
        3. **Margin of Safety:** {mos_percentage:.1f}%
        
        **Action Items:**
        - Monitor harga pasar secara berkala
        - Fokus pada kualitas untuk maintain harga premium
        - Diversifikasi warna untuk mitigasi risiko
        - Target minimal: {bep_tangkai:,.0f} tangkai per siklus untuk avoid loss
        """)

# TAB 4: ROI & Payback (previously tab3)
with tab4:
    st.subheader("📈 Return on Investment & Payback Period")
    
    # Use values from previous tabs (simplified recalculation)
    if 'total_investment' not in dir():
        total_investment = 200000000  # Default
    if 'profit_year' not in dir():
        profit_year = 50000000  # Default
    
    # ROI
    roi = (profit_year / total_investment) * 100 if total_investment > 0 else 0
    
    # Payback period
    payback_months = (total_investment / profit_year * 12) if profit_year > 0 else 999
    payback_years = payback_months / 12
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Investasi", f"Rp {total_investment:,.0f}")
    with col2:
        st.metric("Profit Tahunan", f"Rp {profit_year:,.0f}")
    with col3:
        st.metric("ROI", f"{roi:.1f}%/tahun")
    
    st.markdown("---")
    
    st.markdown("### ⏱️ Payback Period")
    
    if payback_years <= 3:
        color = "🟢"
        status = "SANGAT BAIK"
    elif payback_years <= 5:
        color = "🟡"
        status = "BAIK"
    else:
        color = "🔴"
        status = "PERLU EVALUASI"
    
    st.markdown(f"""
    ### {color} {payback_years:.1f} Tahun ({payback_months:.0f} bulan)
    
    **Status:** {status}
    """)
    
    # Cumulative cash flow chart
    st.markdown("### 📊 Proyeksi Arus Kas Kumulatif")
    
    years = list(range(0, 6))
    cash_flow = [-total_investment]
    for y in range(1, 6):
        cash_flow.append(cash_flow[-1] + profit_year)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=cash_flow,
        mode='lines+markers',
        name='Kumulatif Cash Flow',
        line=dict(color='#ec4899', width=3),
        marker=dict(size=10)
    ))
    
    fig.add_hline(y=0, line_dash="dash", line_color="gray",
                  annotation_text="Break Even Point")
    
    fig.update_layout(
        xaxis_title="Tahun",
        yaxis_title="Cash Flow Kumulatif (Rp)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# TAB 5: Skenario Bisnis (previously tab4)
with tab5:
    st.subheader("🎯 Simulasi Skenario Bisnis")
    
    st.markdown("Bandingkan berbagai skenario untuk pengambilan keputusan:")
    
    scenarios = {
        "Konservatif": {"price": 10000, "survival": 0.80, "stems": 3.0, "cycles": 2},
        "Moderat": {"price": 12000, "survival": 0.85, "stems": 3.5, "cycles": 3},
        "Optimis": {"price": 15000, "survival": 0.90, "stems": 4.0, "cycles": 3},
    }
    
    scenario_results = []
    
    for name, params in scenarios.items():
        plants = greenhouse_area * 64
        harvested = plants * params["survival"]
        stems = harvested * params["stems"]
        revenue = stems * params["price"]
        cost = plants * 400 + greenhouse_area * 4500 + 80000 * 90 + 2500000
        profit = (revenue - cost) * params["cycles"]
        
        scenario_results.append({
            "Skenario": name,
            "Harga Jual": f"Rp {params['price']:,}",
            "Survival": f"{params['survival']*100:.0f}%",
            "Tangkai/Tanaman": params["stems"],
            "Siklus/Tahun": params["cycles"],
            "Profit Tahunan": f"Rp {profit:,.0f}",
            "ROI": f"{(profit/total_investment)*100:.1f}%"
        })
    
    df_scenarios = pd.DataFrame(scenario_results)
    st.dataframe(df_scenarios, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # Risk factors
    st.markdown("### ⚠️ Faktor Risiko")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Risiko Produksi:**
        - 🔴 Serangan hama/penyakit (terutama white rust)
        - 🟠 Gagal photoperiod → bunga tidak keluar
        - 🟡 Cuaca ekstrem → kualitas turun
        - 🟡 Bibit berkualitas rendah
        """)
    
    with col2:
        st.markdown("""
        **Risiko Pasar:**
        - 🔴 Fluktuasi harga musiman
        - 🟠 Kompetisi dengan impor
        - 🟡 Penurunan permintaan (resesi)
        - 🟢 Diversifikasi warna = mitigasi
        """)
    
    st.success("""
    **💡 Rekomendasi Mitigasi:**
    1. Asuransi pertanian (jika tersedia)
    2. Kontrak dengan buyer (florist, hotel)
    3. Diversifikasi 3 warna untuk spread risiko
    4. Emergency fund 2-3 bulan operasional
    """)

# Footer
st.markdown("---")
st.caption("🌸 Budidaya Krisan Pro - Analisis Usaha")
