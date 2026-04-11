"""
Annual Rainfall Analysis
Analyze yearly precipitation patterns and trends
"""
import streamlit as st
import sys
import os
import pandas as pd
import altair as alt
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_historical_weather

# Page configuration
st.set_page_config(
    page_title="Annual Rainfall",
    page_icon="🌧️",
    layout="wide"
)

# Header
st.title("🌧️ Annual Rainfall Analysis")
st.markdown("**Comprehensive yearly precipitation patterns and statistics**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Sidebar - Year selection
st.sidebar.markdown("### 📅 Select Analysis Period")

current_year = datetime.now().year
analysis_type = st.sidebar.selectbox(
    "Analysis Type",
    ["Current Year", "Last 12 Months", "Custom Year"]
)

if analysis_type == "Current Year":
    start_date = datetime(current_year, 1, 1)
    end_date = datetime.now() - timedelta(days=1)
    year_label = f"{current_year} (Year to Date)"
elif analysis_type == "Last 12 Months":
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=365)
    year_label = "Last 12 Months"
else:
    selected_year = st.sidebar.selectbox(
        "Select Year",
        range(current_year - 5, current_year)
    )
    start_date = datetime(selected_year, 1, 1)
    end_date = datetime(selected_year, 12, 31)
    year_label = str(selected_year)

# Fetch historical data
with st.spinner(f"Fetching rainfall data for {year_label}..."):
    rainfall_df = get_historical_weather(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

if rainfall_df is not None and len(rainfall_df) > 0:
    # Process data
    rainfall_df['date'] = pd.to_datetime(rainfall_df['time'])
    rainfall_df['month'] = rainfall_df['date'].dt.month
    rainfall_df['month_name'] = rainfall_df['date'].dt.strftime('%B')
    rainfall_df['week'] = rainfall_df['date'].dt.isocalendar().week
    
    # Annual Statistics
    st.markdown("## 📊 Annual Statistics")
    
    total_rainfall = rainfall_df['precipitation_sum'].sum()
    rainy_days = len(rainfall_df[rainfall_df['precipitation_sum'] > 0])
    total_days = len(rainfall_df)
    avg_daily_rainfall = rainfall_df['precipitation_sum'].mean()
    max_daily_rainfall = rainfall_df['precipitation_sum'].max()
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Rainfall",
            f"{total_rainfall:.1f} mm",
            delta=None
        )
    
    with col2:
        st.metric(
            "Rainy Days",
            f"{rainy_days} days",
            delta=f"{rainy_days/total_days*100:.1f}%"
        )
    
    with col3:
        st.metric(
            "Average Daily",
            f"{avg_daily_rainfall:.2f} mm",
            delta=None
        )
    
    with col4:
        st.metric(
            "Max Daily",
            f"{max_daily_rainfall:.1f} mm",
            delta=None
        )
    
    with col5:
        avg_rainy_day = rainfall_df[rainfall_df['precipitation_sum'] > 0]['precipitation_sum'].mean()
        st.metric(
            "Avg per Rainy Day",
            f"{avg_rainy_day:.1f} mm",
            delta=None
        )
    
    st.markdown("---")
    
    # Monthly Rainfall Distribution
    st.markdown("### 📅 Monthly Rainfall Distribution")
    
    monthly_data = rainfall_df.groupby('month').agg({
        'precipitation_sum': ['sum', 'mean', 'max'],
        'date': 'count'
    }).reset_index()
    
    monthly_data.columns = ['month', 'total', 'average', 'max_daily', 'days']
    monthly_data['month_name'] = pd.to_datetime(monthly_data['month'], format='%m').dt.strftime('%B')
    monthly_data['rainy_days'] = rainfall_df[rainfall_df['precipitation_sum'] > 0].groupby('month').size().reindex(monthly_data['month'], fill_value=0).values
    
    # Monthly bar chart
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_chart = alt.Chart(monthly_data).mark_bar().encode(
            x=alt.X('month_name:N', title='Month', sort=list(monthly_data['month_name'])),
            y=alt.Y('total:Q', title='Total Rainfall (mm)'),
            color=alt.Color('total:Q', scale=alt.Scale(scheme='blues'), legend=None),
            tooltip=['month_name', 'total', 'rainy_days', 'average']
        ).properties(
            height=400,
            title='Total Monthly Rainfall'
        )
        
        st.altair_chart(monthly_chart, use_container_width=True)
    
    with col2:
        # Rainy days per month
        rainy_days_chart = alt.Chart(monthly_data).mark_bar().encode(
            x=alt.X('month_name:N', title='Month', sort=list(monthly_data['month_name'])),
            y=alt.Y('rainy_days:Q', title='Number of Rainy Days'),
            color=alt.Color('rainy_days:Q', scale=alt.Scale(scheme='teals'), legend=None),
            tooltip=['month_name', 'rainy_days', 'total']
        ).properties(
            height=400,
            title='Rainy Days per Month'
        )
        
        st.altair_chart(rainy_days_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Daily Rainfall Pattern
    st.markdown("### 📈 Daily Rainfall Pattern")
    
    # Create daily rainfall chart
    daily_chart = alt.Chart(rainfall_df).mark_area(
        line={'color': '#4299e1'},
        color=alt.Gradient(
            gradient='linear',
            stops=[
                alt.GradientStop(color='white', offset=0),
                alt.GradientStop(color='#4299e1', offset=1)
            ],
            x1=1, x2=1, y1=1, y2=0
        )
    ).encode(
        x=alt.X('date:T', title='Date'),
        y=alt.Y('precipitation_sum:Q', title='Rainfall (mm)'),
        tooltip=['date:T', 'precipitation_sum:Q']
    ).properties(
        height=400
    )
    
    st.altair_chart(daily_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Rainfall Intensity Distribution
    st.markdown("### 💧 Rainfall Intensity Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Categorize rainfall intensity
        def categorize_rainfall(mm):
            if mm == 0:
                return "No Rain"
            elif mm < 5:
                return "Light (0-5mm)"
            elif mm < 20:
                return "Moderate (5-20mm)"
            elif mm < 50:
                return "Heavy (20-50mm)"
            else:
                return "Very Heavy (>50mm)"
        
        rainfall_df['intensity'] = rainfall_df['precipitation_sum'].apply(categorize_rainfall)
        intensity_counts = rainfall_df['intensity'].value_counts()
        
        # Create pie chart
        fig = go.Figure(data=[go.Pie(
            labels=intensity_counts.index,
            values=intensity_counts.values,
            hole=0.4,
            marker=dict(colors=['#e2e8f0', '#90cdf4', '#4299e1', '#2b6cb0', '#1a365d'])
        )])
        
        fig.update_layout(
            title='Rainfall Intensity Distribution',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Rainfall Categories:**")
        st.markdown(f"""
        - **No Rain:** {intensity_counts.get('No Rain', 0)} days
        - **Light (0-5mm):** {intensity_counts.get('Light (0-5mm)', 0)} days
        - **Moderate (5-20mm):** {intensity_counts.get('Moderate (5-20mm)', 0)} days
        - **Heavy (20-50mm):** {intensity_counts.get('Heavy (20-50mm)', 0)} days
        - **Very Heavy (>50mm):** {intensity_counts.get('Very Heavy (>50mm)', 0)} days
        
        **Wettest Month:** {monthly_data.loc[monthly_data['total'].idxmax(), 'month_name']} ({monthly_data['total'].max():.1f} mm)
        
        **Driest Month:** {monthly_data.loc[monthly_data['total'].idxmin(), 'month_name']} ({monthly_data['total'].min():.1f} mm)
        
        **Wettest Day:** {rainfall_df.loc[rainfall_df['precipitation_sum'].idxmax(), 'date'].strftime('%B %d, %Y')} ({max_daily_rainfall:.1f} mm)
        """)
    
    st.markdown("---")
    
    # Monthly Statistics Table
    st.markdown("### 📋 Monthly Statistics Table")
    
    display_monthly = monthly_data.copy()
    display_monthly['Month'] = display_monthly['month_name']
    display_monthly['Total (mm)'] = display_monthly['total'].apply(lambda x: f"{x:.1f}")
    display_monthly['Average (mm)'] = display_monthly['average'].apply(lambda x: f"{x:.2f}")
    display_monthly['Max Daily (mm)'] = display_monthly['max_daily'].apply(lambda x: f"{x:.1f}")
    display_monthly['Rainy Days'] = display_monthly['rainy_days']
    display_monthly['Rain %'] = (display_monthly['rainy_days'] / display_monthly['days'] * 100).apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(
        display_monthly[['Month', 'Total (mm)', 'Average (mm)', 'Max Daily (mm)', 'Rainy Days', 'Rain %']],
        use_container_width=True,
        hide_index=True
    )
    
    # Download button
    csv = display_monthly[['Month', 'Total (mm)', 'Average (mm)', 'Max Daily (mm)', 'Rainy Days', 'Rain %']].to_csv(index=False)
    st.download_button(
        label="📥 Download Monthly Statistics",
        data=csv,
        file_name=f"rainfall_statistics_{year_label.replace(' ', '_')}.csv",
        mime="text/csv"
    )
    
    st.markdown("---")
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Historical Analysis", use_container_width=True):
            st.switch_page("pages/05_📊_Historical_Analysis.py")
    
    with col2:
        if st.button("🌤️ Current Weather", use_container_width=True):
            st.switch_page("pages/02_🌤️_Current_Weather.py")
    
    with col3:
        if st.button("🗺️ Change Location", use_container_width=True):
            st.switch_page("pages/01_🗺️_Interactive_Map.py")

else:
    st.error("❌ Unable to fetch rainfall data. Please try again or select a different period.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
