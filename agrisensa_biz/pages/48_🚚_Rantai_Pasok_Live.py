import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import uuid
import hashlib

from utils.auth import require_auth, show_user_info_sidebar

st.set_page_config(
    page_title="Supply Chain Visibility - AgriSensa",
    page_icon="🚚",
    layout="wide"
)

# ===== AUTHENTICATION CHECK =====
user = require_auth()
show_user_info_sidebar()
# ================================

# ==========================================
# INITIALIZE SESSION STATE
# ==========================================

if 'shipments' not in st.session_state:
    st.session_state.shipments = []

if 'routes' not in st.session_state:
    st.session_state.routes = []

if 'market_prices' not in st.session_state:
    st.session_state.market_prices = []

# ==========================================
# DATA REFERENCES
# ==========================================

LOCATIONS = {
    "Farm": ["Farm Banyumas", "Farm Cianjur", "Farm Bandung", "Farm Garut", "Farm Lembang"],
    "Pasar Induk": ["PI Kramat Jati", "PI Tanah Tinggi", "PI Cibitung", "PI Caringin"],
    "Retail": ["Superindo", "Alfamart", "Indomaret", "Pasar Tradisional", "Restoran"]
}

VEHICLES = {
    "Pick Up (L300)": {"capacity_kg": 1000, "cost_per_km": 3500},
    "Truck Engkel": {"capacity_kg": 2200, "cost_per_km": 5000},
    "Colt Diesel": {"capacity_kg": 4500, "cost_per_km": 7500},
    "Fuso": {"capacity_kg": 12000, "cost_per_km": 12000}
}

COMMODITIES = [
    "Cabai Merah", "Cabai Rawit", "Tomat", "Bawang Merah", "Bawang Putih",
    "Kentang", "Wortel", "Sawi", "Kangkung", "Bayam", "Selada"
]

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def create_shipment(data):
    """Create new shipment record"""
    shipment = {
        "id": str(uuid.uuid4()),
        "shipment_number": f"SHP-{datetime.now().strftime('%Y%m%d')}-{len(st.session_state.shipments)+1:03d}",
        **data,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.shipments.append(shipment)
    return shipment

def get_active_shipments():
    """Get shipments that are not completed"""
    return [s for s in st.session_state.shipments if s['status'] != 'delivered']

def calculate_logistics_cost(distance_km, vehicle_type, quantity_kg):
    """Calculate total logistics cost"""
    vehicle = VEHICLES[vehicle_type]
    transport_cost = distance_km * vehicle['cost_per_km']
    cost_per_kg = transport_cost / quantity_kg if quantity_kg > 0 else 0
    return {
        "transport_cost": transport_cost,
        "cost_per_kg": cost_per_kg,
        "total_cost": transport_cost
    }

# ==========================================
# HEADER
# ==========================================

st.title("🚚 Supply Chain Visibility & Logistics Optimization")
st.markdown("**End-to-end tracking dari Farm → Pasar Induk → Retail dengan cost optimization**")
st.info("💡 Sistem berbasis pengalaman nyata di seluruh value chain: produksi, pasar induk, retail, dan e-commerce")

# ==========================================
# MAIN TABS
# ==========================================

tab_dashboard, tab_shipments, tab_optimizer, tab_analytics, tab_legacy = st.tabs([
    "📊 Dashboard",
    "🚛 Shipment Tracking",
    "⚡ Logistics Optimizer",
    "📈 Analytics & Reports",
    "🔧 Legacy Tools"
])

# ========== TAB: DASHBOARD ==========
with tab_dashboard:
    st.header("📊 Real-Time Supply Chain Dashboard")
    
    # KPI Cards
    active_shipments = get_active_shipments()
    total_shipments = len(st.session_state.shipments)
    
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    
    with col_kpi1:
        st.metric("Total Shipments", total_shipments)
    
    with col_kpi2:
        st.metric("Active Shipments", len(active_shipments))
    
    with col_kpi3:
        completed = len([s for s in st.session_state.shipments if s['status'] == 'delivered'])
        on_time_rate = (completed / total_shipments * 100) if total_shipments > 0 else 0
        st.metric("On-Time Delivery", f"{on_time_rate:.0f}%")
    
    with col_kpi4:
        if st.session_state.shipments:
            avg_cost = sum([s.get('total_cost', 0) for s in st.session_state.shipments]) / total_shipments
            st.metric("Avg Cost/Shipment", f"Rp {avg_cost:,.0f}")
        else:
            st.metric("Avg Cost/Shipment", "Rp 0")
    
    st.divider()
    
    # Active Shipments Overview
    if active_shipments:
        st.subheader("🚛 Active Shipments")
        
        for shipment in active_shipments:
            with st.container():
                col_s1, col_s2, col_s3, col_s4 = st.columns([2, 2, 1, 1])
                
                with col_s1:
                    st.markdown(f"**{shipment['shipment_number']}**")
                    st.caption(f"{shipment['commodity']} - {shipment['quantity_kg']} kg")
                
                with col_s2:
                    st.markdown(f"📍 {shipment['origin']} → {shipment['destination']}")
                
                with col_s3:
                    status_emoji = {
                        "packing": "📦",
                        "in_transit": "🚛",
                        "arrived": "✅",
                        "delivered": "🎯"
                    }
                    st.markdown(f"{status_emoji.get(shipment['status'], '❓')} {shipment['status'].replace('_', ' ').title()}")
                
                with col_s4:
                    if st.button("View", key=f"view_{shipment['id']}", use_container_width=True):
                        st.session_state.selected_shipment = shipment['id']
                
                st.divider()
    else:
        st.info("Tidak ada shipment aktif. Buat shipment baru di tab 'Shipment Tracking'")
    
    # Status Distribution
    if st.session_state.shipments:
        st.subheader("📊 Shipment Status Distribution")
        
        status_counts = {}
        for s in st.session_state.shipments:
            status = s['status']
            status_counts[status] = status_counts.get(status, 0) + 1
        
        fig_status = px.pie(
            values=list(status_counts.values()),
            names=list(status_counts.keys()),
            title="Status Distribution",
            hole=0.4
        )
        st.plotly_chart(fig_status, use_container_width=True)

# ========== TAB: SHIPMENT TRACKING ==========
with tab_shipments:
    st.header("🚛 Shipment Management & Tracking")
    
    # Create New Shipment
    with st.expander("➕ Create New Shipment", expanded=not st.session_state.shipments):
        with st.form("create_shipment_form"):
            col_ship1, col_ship2 = st.columns(2)
            
            with col_ship1:
                st.subheader("Shipment Details")
                commodity = st.selectbox("Commodity", COMMODITIES)
                quantity_kg = st.number_input("Quantity (kg)", min_value=10, max_value=50000, value=500, step=10)
                
                origin_type = st.selectbox("Origin Type", ["Farm", "Pasar Induk"])
                origin = st.selectbox("Origin Location", LOCATIONS[origin_type])
                
                dest_type = st.selectbox("Destination Type", ["Pasar Induk", "Retail"])
                destination = st.selectbox("Destination Location", LOCATIONS[dest_type])
            
            with col_ship2:
                st.subheader("Logistics Details")
                vehicle_type = st.selectbox("Vehicle Type", list(VEHICLES.keys()))
                driver_name = st.text_input("Driver Name", "")
                distance_km = st.number_input("Distance (km)", min_value=1, max_value=1000, value=100, step=10)
                
                departure_date = st.date_input("Departure Date", datetime.now())
                departure_time = st.time_input("Departure Time", datetime.now().time())
                
                estimated_hours = st.number_input("Estimated Travel Time (hours)", min_value=1, max_value=24, value=6)
            
            if st.form_submit_button("🚀 Create Shipment", type="primary", use_container_width=True):
                departure_datetime = datetime.combine(departure_date, departure_time)
                estimated_arrival = departure_datetime + timedelta(hours=estimated_hours)
                
                # Calculate costs
                costs = calculate_logistics_cost(distance_km, vehicle_type, quantity_kg)
                
                shipment_data = {
                    "commodity": commodity,
                    "quantity_kg": quantity_kg,
                    "origin": origin,
                    "destination": destination,
                    "vehicle_type": vehicle_type,
                    "driver_name": driver_name,
                    "distance_km": distance_km,
                    "departure_time": departure_datetime.strftime("%Y-%m-%d %H:%M"),
                    "estimated_arrival": estimated_arrival.strftime("%Y-%m-%d %H:%M"),
                    "actual_arrival": None,
                    "status": "packing",
                    "checkpoints": [],
                    "transport_cost": costs['transport_cost'],
                    "cost_per_kg": costs['cost_per_kg'],
                    "total_cost": costs['total_cost']
                }
                
                new_shipment = create_shipment(shipment_data)
                st.success(f"✅ Shipment {new_shipment['shipment_number']} created successfully!")
                st.rerun()
    
    st.divider()
    
    # Shipment List
    if st.session_state.shipments:
        st.subheader("📋 All Shipments")
        
        # Filters
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            filter_status = st.multiselect("Filter by Status", 
                                          ["packing", "in_transit", "arrived", "delivered"],
                                          default=["packing", "in_transit", "arrived"])
        
        with col_f2:
            filter_commodity = st.multiselect("Filter by Commodity", COMMODITIES)
        
        with col_f3:
            sort_by = st.selectbox("Sort by", ["Newest First", "Oldest First", "Cost (High-Low)", "Cost (Low-High)"])
        
        # Apply filters
        filtered_shipments = st.session_state.shipments
        
        if filter_status:
            filtered_shipments = [s for s in filtered_shipments if s['status'] in filter_status]
        
        if filter_commodity:
            filtered_shipments = [s for s in filtered_shipments if s['commodity'] in filter_commodity]
        
        # Apply sorting
        if sort_by == "Newest First":
            filtered_shipments = sorted(filtered_shipments, key=lambda x: x['created_at'], reverse=True)
        elif sort_by == "Oldest First":
            filtered_shipments = sorted(filtered_shipments, key=lambda x: x['created_at'])
        elif sort_by == "Cost (High-Low)":
            filtered_shipments = sorted(filtered_shipments, key=lambda x: x.get('total_cost', 0), reverse=True)
        elif sort_by == "Cost (Low-High)":
            filtered_shipments = sorted(filtered_shipments, key=lambda x: x.get('total_cost', 0))
        
        # Display shipments
        for shipment in filtered_shipments:
            with st.expander(f"🚛 {shipment['shipment_number']} - {shipment['commodity']} ({shipment['status'].replace('_', ' ').title()})"):
                col_d1, col_d2 = st.columns(2)
                
                with col_d1:
                    st.markdown("**Shipment Info:**")
                    st.write(f"- Commodity: {shipment['commodity']}")
                    st.write(f"- Quantity: {shipment['quantity_kg']} kg")
                    st.write(f"- Route: {shipment['origin']} → {shipment['destination']}")
                    st.write(f"- Distance: {shipment['distance_km']} km")
                    st.write(f"- Vehicle: {shipment['vehicle_type']}")
                    st.write(f"- Driver: {shipment['driver_name']}")
                
                with col_d2:
                    st.markdown("**Timeline & Costs:**")
                    st.write(f"- Departure: {shipment['departure_time']}")
                    st.write(f"- Est. Arrival: {shipment['estimated_arrival']}")
                    if shipment['actual_arrival']:
                        st.write(f"- Actual Arrival: {shipment['actual_arrival']}")
                    st.write(f"- Transport Cost: Rp {shipment['transport_cost']:,.0f}")
                    st.write(f"- Cost per kg: Rp {shipment['cost_per_kg']:,.0f}")
                
                # Status Update
                st.markdown("**Update Status:**")
                col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
                
                with col_btn1:
                    if shipment['status'] == 'packing' and st.button("🚛 Start Transit", key=f"transit_{shipment['id']}"):
                        shipment['status'] = 'in_transit'
                        st.rerun()
                
                with col_btn2:
                    if shipment['status'] == 'in_transit' and st.button("✅ Mark Arrived", key=f"arrived_{shipment['id']}"):
                        shipment['status'] = 'arrived'
                        shipment['actual_arrival'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                        st.rerun()
                
                with col_btn3:
                    if shipment['status'] == 'arrived' and st.button("🎯 Delivered", key=f"delivered_{shipment['id']}"):
                        shipment['status'] = 'delivered'
                        st.rerun()
                
                with col_btn4:
                    if st.button("🗑️ Delete", key=f"delete_{shipment['id']}"):
                        st.session_state.shipments.remove(shipment)
                        st.rerun()
    else:
        st.info("Belum ada shipment. Buat shipment baru di atas!")

# ========== TAB: LOGISTICS OPTIMIZER ==========
with tab_optimizer:
    st.header("⚡ Logistics Cost Optimizer")
    
    st.subheader("📊 Route Comparison Tool")
    
    col_opt1, col_opt2 = st.columns(2)
    
    with col_opt1:
        st.markdown("**Route A**")
        route_a_origin = st.selectbox("Origin A", LOCATIONS["Farm"], key="route_a_origin")
        route_a_dest = st.selectbox("Destination A", LOCATIONS["Pasar Induk"], key="route_a_dest")
        route_a_dist = st.number_input("Distance A (km)", 1, 1000, 150, key="route_a_dist")
        route_a_vehicle = st.selectbox("Vehicle A", list(VEHICLES.keys()), key="route_a_vehicle")
        route_a_qty = st.number_input("Quantity A (kg)", 10, 50000, 1000, key="route_a_qty")
    
    with col_opt2:
        st.markdown("**Route B**")
        route_b_origin = st.selectbox("Origin B", LOCATIONS["Farm"], key="route_b_origin")
        route_b_dest = st.selectbox("Destination B", LOCATIONS["Pasar Induk"], key="route_b_dest")
        route_b_dist = st.number_input("Distance B (km)", 1, 1000, 200, key="route_b_dist")
        route_b_vehicle = st.selectbox("Vehicle B", list(VEHICLES.keys()), key="route_b_vehicle")
        route_b_qty = st.number_input("Quantity B (kg)", 10, 50000, 1000, key="route_b_qty")
    
    if st.button("🔍 Compare Routes", type="primary", use_container_width=True):
        cost_a = calculate_logistics_cost(route_a_dist, route_a_vehicle, route_a_qty)
        cost_b = calculate_logistics_cost(route_b_dist, route_b_vehicle, route_b_qty)
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.markdown("### Route A Results")
            st.metric("Total Cost", f"Rp {cost_a['total_cost']:,.0f}")
            st.metric("Cost per kg", f"Rp {cost_a['cost_per_kg']:,.0f}")
        
        with col_res2:
            st.markdown("### Route B Results")
            st.metric("Total Cost", f"Rp {cost_b['total_cost']:,.0f}")
            st.metric("Cost per kg", f"Rp {cost_b['cost_per_kg']:,.0f}")
        
        # Recommendation
        if cost_a['cost_per_kg'] < cost_b['cost_per_kg']:
            savings = cost_b['cost_per_kg'] - cost_a['cost_per_kg']
            st.success(f"✅ **Recommendation: Route A** - Save Rp {savings:,.0f} per kg!")
        elif cost_b['cost_per_kg'] < cost_a['cost_per_kg']:
            savings = cost_a['cost_per_kg'] - cost_b['cost_per_kg']
            st.success(f"✅ **Recommendation: Route B** - Save Rp {savings:,.0f} per kg!")
        else:
            st.info("Both routes have similar costs")
        
        # Comparison Chart
        comparison_data = pd.DataFrame({
            "Route": ["Route A", "Route B"],
            "Total Cost": [cost_a['total_cost'], cost_b['total_cost']],
            "Cost per kg": [cost_a['cost_per_kg'], cost_b['cost_per_kg']]
        })
        
        fig_compare = px.bar(comparison_data, x="Route", y=["Total Cost", "Cost per kg"], 
                            title="Cost Comparison", barmode="group")
        st.plotly_chart(fig_compare, use_container_width=True)

# ========== TAB: ANALYTICS ==========
with tab_analytics:
    st.header("📈 Performance Analytics & Reports")
    
    if st.session_state.shipments:
        # Performance Metrics
        col_a1, col_a2 = st.columns(2)
        
        with col_a1:
            st.subheader("📊 Delivery Performance")
            
            total = len(st.session_state.shipments)
            delivered = len([s for s in st.session_state.shipments if s['status'] == 'delivered'])
            in_transit = len([s for s in st.session_state.shipments if s['status'] == 'in_transit'])
            
            perf_data = pd.DataFrame({
                "Status": ["Delivered", "In Transit", "Others"],
                "Count": [delivered, in_transit, total - delivered - in_transit]
            })
            
            fig_perf = px.pie(perf_data, values="Count", names="Status", 
                             title="Shipment Status Distribution", hole=0.4)
            st.plotly_chart(fig_perf, use_container_width=True)
        
        with col_a2:
            st.subheader("💰 Cost Analysis")
            
            # Cost by commodity
            cost_by_commodity = {}
            for s in st.session_state.shipments:
                comm = s['commodity']
                cost = s.get('cost_per_kg', 0)
                if comm in cost_by_commodity:
                    cost_by_commodity[comm].append(cost)
                else:
                    cost_by_commodity[comm] = [cost]
            
            avg_costs = {k: sum(v)/len(v) for k, v in cost_by_commodity.items()}
            
            cost_df = pd.DataFrame({
                "Commodity": list(avg_costs.keys()),
                "Avg Cost per kg": list(avg_costs.values())
            })
            
            fig_cost = px.bar(cost_df, x="Commodity", y="Avg Cost per kg",
                             title="Average Cost per kg by Commodity")
            st.plotly_chart(fig_cost, use_container_width=True)
        
        # Export
        st.subheader("📥 Export Data")
        
        if st.button("📥 Download Shipment Data (CSV)", use_container_width=True):
            df_export = pd.DataFrame(st.session_state.shipments)
            csv = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Download CSV",
                csv,
                "shipments_data.csv",
                "text/csv"
            )
    else:
        st.info("Tidak ada data untuk dianalisis. Buat shipment terlebih dahulu!")

# ========== TAB: LEGACY TOOLS ==========
with tab_legacy:
    st.header("🔧 Legacy Logistics Tools")
    st.info("Tools lama yang masih berguna untuk perhitungan cepat")
    
    # Simple Cost Calculator
    st.subheader("💰 Quick Cost Calculator")
    
    col_leg1, col_leg2 = st.columns(2)
    
    with col_leg1:
        quick_dist = st.number_input("Distance (km)", 1, 1000, 100, key="quick_dist")
        quick_vehicle = st.selectbox("Vehicle", list(VEHICLES.keys()), key="quick_vehicle")
    
    with col_leg2:
        quick_qty = st.number_input("Quantity (kg)", 10, 50000, 500, key="quick_qty")
        
        if st.button("Calculate", use_container_width=True):
            quick_cost = calculate_logistics_cost(quick_dist, quick_vehicle, quick_qty)
            st.success(f"**Total Cost:** Rp {quick_cost['total_cost']:,.0f}")
            st.info(f"**Cost per kg:** Rp {quick_cost['cost_per_kg']:,.0f}")

# ==========================================
# FOOTER
# ==========================================

st.divider()
st.caption("💡 Supply Chain Visibility - Based on real-world experience across entire agricultural value chain")
