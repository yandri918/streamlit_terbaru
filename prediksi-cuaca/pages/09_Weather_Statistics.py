"""
Advanced Weather Statistics & Correlations
Statistical analysis with UV Index, Heat Index, and Weather Comfort
"""
import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from scipy import stats

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_historical_weather

# Page configuration
st.set_page_config(
    page_title="Weather Statistics",
    page_icon="📈",
    layout="wide"
)

# Utility functions
def calculate_heat_index(temp_c, humidity):
    """Calculate heat index (feels like temperature in hot conditions)"""
    temp_f = temp_c * 9/5 + 32
    hi = -42.379 + 2.04901523*temp_f + 10.14333127*humidity - 0.22475541*temp_f*humidity
    hi -= 0.00683783*temp_f*temp_f - 0.05481717*humidity*humidity
    hi += 0.00122874*temp_f*temp_f*humidity + 0.00085282*temp_f*humidity*humidity
    hi -= 0.00000199*temp_f*temp_f*humidity*humidity
    return (hi - 32) * 5/9  # Convert back to Celsius

def get_uv_category(uv_index):
    """Get UV index category and color"""
    if pd.isna(uv_index):
        return "Unknown", "#718096", "❓"
    if uv_index < 3:
        return "Low", "#48bb78", "😊"
    elif uv_index < 6:
        return "Moderate", "#ed8936", "😐"
    elif uv_index < 8:
        return "High", "#dd6b20", "😰"
    elif uv_index < 11:
        return "Very High", "#c53030", "😱"
    else:
        return "Extreme", "#742a2a", "☠️"

def get_uv_protection_advice(uv_index):
    """Get UV protection recommendations"""
    if pd.isna(uv_index):
        return "UV data not available for this period."
    if uv_index < 3:
        return "Minimal protection needed. Safe to be outside."
    elif uv_index < 6:
        return "Wear sunscreen SPF 30+. Seek shade during midday."
    elif uv_index < 8:
        return "Protection essential. Sunscreen SPF 30+, hat, sunglasses."
    elif uv_index < 11:
        return "Extra protection required. Avoid sun 10am-4pm."
    else:
        return "Take all precautions. Avoid sun exposure if possible."

# Header
st.title("📈 Advanced Weather Statistics")
st.markdown("**Statistical analysis with UV Index, Heat Index, and Weather Comfort**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Sidebar - Analysis period
st.sidebar.markdown("### 📅 Analysis Period")
days_back = st.sidebar.slider("Days of Historical Data", 30, 365, 90)

end_date = datetime.now() - timedelta(days=1)
start_date = end_date - timedelta(days=days_back)

# Fetch data
with st.spinner(f"Analyzing {days_back} days of weather data..."):
    weather_df = get_historical_weather(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        start_date.strftime('%Y-%m-%d'),
        end_date.strftime('%Y-%m-%d')
    )

if weather_df is not None and len(weather_df) > 0:
    # Process data
    weather_df['date'] = pd.to_datetime(weather_df['time'])
    
    # Calculate additional metrics
    if 'apparent_temperature_max' in weather_df.columns and 'temperature_2m_max' in weather_df.columns:
        weather_df['heat_stress'] = weather_df['apparent_temperature_max'] - weather_df['temperature_2m_max']
    
    # Statistical Summary
    st.markdown("## 📊 Comprehensive Statistical Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 🌡️ Temperature")
        temp_mean = weather_df['temperature_2m_mean'].mean()
        temp_std = weather_df['temperature_2m_mean'].std()
        temp_median = weather_df['temperature_2m_mean'].median()
        
        st.metric("Mean", f"{temp_mean:.1f}°C")
        st.metric("Std Dev", f"{temp_std:.2f}°C")
        st.metric("Median", f"{temp_median:.1f}°C")
    
    with col2:
        st.markdown("### 💧 Precipitation")
        precip_total = weather_df['precipitation_sum'].sum()
        precip_mean = weather_df['precipitation_sum'].mean()
        precip_max = weather_df['precipitation_sum'].max()
        
        st.metric("Total", f"{precip_total:.1f} mm")
        st.metric("Daily Avg", f"{precip_mean:.2f} mm")
        st.metric("Max Daily", f"{precip_max:.1f} mm")
    
    with col3:
        st.markdown("### 🌬️ Wind Speed")
        wind_mean = weather_df['wind_speed_10m_max'].mean()
        wind_std = weather_df['wind_speed_10m_max'].std()
        wind_max = weather_df['wind_speed_10m_max'].max()
        
        st.metric("Mean", f"{wind_mean:.1f} km/h")
        st.metric("Std Dev", f"{wind_std:.2f} km/h")
        st.metric("Max", f"{wind_max:.1f} km/h")
    
    with col4:
        if 'uv_index_max' in weather_df.columns:
            st.markdown("### ☀️ UV Index")
            # Drop NaN values for statistics
            uv_data = weather_df['uv_index_max'].dropna()
            
            if len(uv_data) > 0:
                uv_mean = uv_data.mean()
                uv_max = uv_data.max()
                uv_category, uv_color, uv_emoji = get_uv_category(uv_mean)
                
                st.metric("Avg Max", f"{uv_mean:.1f}")
                st.metric("Highest", f"{uv_max:.1f}")
                st.markdown(f"**Category:** {uv_emoji} {uv_category}")
            else:
                st.markdown("*No UV data available*")
    
    st.markdown("---")
    
    # UV Index Analysis
    if 'uv_index_max' in weather_df.columns:
        st.markdown("## ☀️ UV Index Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # UV Index trend
            fig_uv = go.Figure()
            
            fig_uv.add_trace(go.Scatter(
                x=weather_df['date'],
                y=weather_df['uv_index_max'],
                name='UV Index',
                fill='tozeroy',
                line=dict(color='#ed8936', width=2)
            ))
            
            # Add category thresholds
            fig_uv.add_hline(y=3, line_dash="dash", line_color="green", annotation_text="Low/Moderate")
            fig_uv.add_hline(y=6, line_dash="dash", line_color="orange", annotation_text="Moderate/High")
            fig_uv.add_hline(y=8, line_dash="dash", line_color="red", annotation_text="High/Very High")
            fig_uv.add_hline(y=11, line_dash="dash", line_color="darkred", annotation_text="Very High/Extreme")
            
            fig_uv.update_layout(
                title='UV Index Trend',
                xaxis_title='Date',
                yaxis_title='UV Index',
                height=400,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig_uv, use_container_width=True)
        
        with col2:
            # UV Index distribution
            uv_categories = weather_df['uv_index_max'].apply(lambda x: get_uv_category(x)[0])
            uv_counts = uv_categories.value_counts()
            
            fig_uv_pie = go.Figure(data=[go.Pie(
                labels=uv_counts.index,
                values=uv_counts.values,
                marker=dict(colors=['#48bb78', '#ed8936', '#dd6b20', '#c53030', '#742a2a'])
            )])
            
            fig_uv_pie.update_layout(
                title='UV Index Distribution',
                height=400
            )
            
            st.plotly_chart(fig_uv_pie, use_container_width=True)
        
        # UV Protection Advice
        uv_data_for_advice = weather_df['uv_index_max'].dropna()
        if len(uv_data_for_advice) > 0:
            uv_mean_advice = uv_data_for_advice.mean()
            st.info(f"**☀️ UV Protection Advice:** {get_uv_protection_advice(uv_mean_advice)}")
        else:
            st.info("**☀️ UV Protection Advice:** UV data not available for this period.")
        
        st.markdown("---")
    
    # Heat Stress Analysis
    if 'heat_stress' in weather_df.columns:
        st.markdown("## 🌡️ Heat Stress & Comfort Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Heat stress trend
            fig_heat = go.Figure()
            
            fig_heat.add_trace(go.Scatter(
                x=weather_df['date'],
                y=weather_df['heat_stress'],
                name='Heat Stress',
                fill='tozeroy',
                line=dict(color='#e53e3e', width=2)
            ))
            
            fig_heat.update_layout(
                title='Heat Stress (Apparent - Actual Temperature)',
                xaxis_title='Date',
                yaxis_title='Temperature Difference (°C)',
                height=400
            )
            
            st.plotly_chart(fig_heat, use_container_width=True)
        
        with col2:
            # Comfort scatter
            fig_comfort = go.Figure()
            
            fig_comfort.add_trace(go.Scatter(
                x=weather_df['temperature_2m_mean'],
                y=weather_df['apparent_temperature_max'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=weather_df['heat_stress'],
                    colorscale='RdYlBu_r',
                    showscale=True,
                    colorbar=dict(title="Heat<br>Stress")
                ),
                text=weather_df['date'].dt.strftime('%Y-%m-%d'),
                hovertemplate='<b>%{text}</b><br>Actual: %{x:.1f}°C<br>Feels: %{y:.1f}°C<extra></extra>'
            ))
            
            # Add diagonal line (feels = actual)
            min_temp = weather_df['temperature_2m_mean'].min()
            max_temp = weather_df['temperature_2m_mean'].max()
            fig_comfort.add_trace(go.Scatter(
                x=[min_temp, max_temp],
                y=[min_temp, max_temp],
                mode='lines',
                line=dict(color='gray', dash='dash'),
                name='Feels = Actual',
                showlegend=True
            ))
            
            fig_comfort.update_layout(
                title='Temperature vs Feels Like',
                xaxis_title='Actual Temperature (°C)',
                yaxis_title='Feels Like (°C)',
                height=400
            )
            
            st.plotly_chart(fig_comfort, use_container_width=True)
        
        st.markdown("---")
    
    # Enhanced Correlation Analysis
    st.markdown("## 🔗 Advanced Correlation Analysis")
    
    # Select available columns for correlation
    corr_columns = ['temperature_2m_mean', 'precipitation_sum', 'wind_speed_10m_max']
    if 'uv_index_max' in weather_df.columns:
        corr_columns.append('uv_index_max')
    if 'apparent_temperature_max' in weather_df.columns:
        corr_columns.append('apparent_temperature_max')
    if 'wind_gusts_10m_max' in weather_df.columns:
        corr_columns.append('wind_gusts_10m_max')
    
    corr_data = weather_df[corr_columns].corr()
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Correlation heatmap
        fig_corr = go.Figure(data=go.Heatmap(
            z=corr_data.values,
            x=[col.replace('_', ' ').title() for col in corr_data.columns],
            y=[col.replace('_', ' ').title() for col in corr_data.columns],
            colorscale='RdBu',
            zmid=0,
            text=corr_data.values.round(3),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Correlation")
        ))
        
        fig_corr.update_layout(
            title='Weather Variables Correlation Matrix',
            height=500
        )
        
        st.plotly_chart(fig_corr, use_container_width=True)
    
    with col2:
        # Temperature vs UV Index (if available)
        if 'uv_index_max' in weather_df.columns:
            scatter_fig = go.Figure()
            
            scatter_fig.add_trace(go.Scatter(
                x=weather_df['temperature_2m_max'],
                y=weather_df['uv_index_max'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=weather_df['precipitation_sum'],
                    colorscale='Blues',
                    showscale=True,
                    colorbar=dict(title="Precip<br>(mm)")
                ),
                text=weather_df['date'].dt.strftime('%Y-%m-%d'),
                hovertemplate='<b>%{text}</b><br>Temp: %{x:.1f}°C<br>UV: %{y:.1f}<extra></extra>'
            ))
            
            scatter_fig.update_layout(
                title='Temperature vs UV Index',
                xaxis_title='Max Temperature (°C)',
                yaxis_title='UV Index',
                height=500
            )
            
            st.plotly_chart(scatter_fig, use_container_width=True)
        else:
            # Fallback to temp vs precipitation
            scatter_fig = go.Figure()
            
            scatter_fig.add_trace(go.Scatter(
                x=weather_df['temperature_2m_mean'],
                y=weather_df['precipitation_sum'],
                mode='markers',
                marker=dict(
                    size=8,
                    color=weather_df['wind_speed_10m_max'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Wind<br>(km/h)")
                ),
                text=weather_df['date'].dt.strftime('%Y-%m-%d'),
                hovertemplate='<b>%{text}</b><br>Temp: %{x:.1f}°C<br>Precip: %{y:.1f}mm<extra></extra>'
            ))
            
            scatter_fig.update_layout(
                title='Temperature vs Precipitation',
                xaxis_title='Temperature (°C)',
                yaxis_title='Precipitation (mm)',
                height=500
            )
            
            st.plotly_chart(scatter_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Time Series Decomposition
    st.markdown("## 📉 Temperature Trend Analysis")
    
    # Calculate moving averages
    weather_df['temp_ma7'] = weather_df['temperature_2m_mean'].rolling(window=7, center=True).mean()
    weather_df['temp_ma30'] = weather_df['temperature_2m_mean'].rolling(window=30, center=True).mean()
    
    # Create trend chart
    trend_fig = go.Figure()
    
    trend_fig.add_trace(go.Scatter(
        x=weather_df['date'],
        y=weather_df['temperature_2m_mean'],
        name='Daily Temperature',
        line=dict(color='lightgray', width=1),
        opacity=0.5
    ))
    
    trend_fig.add_trace(go.Scatter(
        x=weather_df['date'],
        y=weather_df['temp_ma7'],
        name='7-Day Moving Average',
        line=dict(color='#4299e1', width=2)
    ))
    
    trend_fig.add_trace(go.Scatter(
        x=weather_df['date'],
        y=weather_df['temp_ma30'],
        name='30-Day Moving Average',
        line=dict(color='#e53e3e', width=2)
    ))
    
    trend_fig.update_layout(
        title='Temperature Trends with Moving Averages',
        xaxis_title='Date',
        yaxis_title='Temperature (°C)',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(trend_fig, use_container_width=True)
    
    st.markdown("---")
    
    # Distribution Analysis
    st.markdown("## 📊 Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Temperature distribution
        temp_hist = go.Figure()
        
        temp_hist.add_trace(go.Histogram(
            x=weather_df['temperature_2m_mean'],
            nbinsx=30,
            name='Temperature',
            marker_color='#4299e1',
            opacity=0.7
        ))
        
        # Add normal distribution overlay
        mu = weather_df['temperature_2m_mean'].mean()
        sigma = weather_df['temperature_2m_mean'].std()
        x_range = np.linspace(weather_df['temperature_2m_mean'].min(), 
                             weather_df['temperature_2m_mean'].max(), 100)
        y_normal = stats.norm.pdf(x_range, mu, sigma) * len(weather_df) * \
                   (weather_df['temperature_2m_mean'].max() - weather_df['temperature_2m_mean'].min()) / 30
        
        temp_hist.add_trace(go.Scatter(
            x=x_range,
            y=y_normal,
            name='Normal Distribution',
            line=dict(color='red', width=2)
        ))
        
        temp_hist.update_layout(
            title='Temperature Distribution',
            xaxis_title='Temperature (°C)',
            yaxis_title='Frequency',
            height=350
        )
        
        st.plotly_chart(temp_hist, use_container_width=True)
    
    with col2:
        # UV Index distribution (if available)
        if 'uv_index_max' in weather_df.columns:
            uv_hist = go.Figure()
            
            uv_hist.add_trace(go.Histogram(
                x=weather_df['uv_index_max'],
                nbinsx=20,
                name='UV Index',
                marker_color='#ed8936',
                opacity=0.7
            ))
            
            uv_hist.update_layout(
                title='UV Index Distribution',
                xaxis_title='UV Index',
                yaxis_title='Frequency',
                height=350
            )
            
            st.plotly_chart(uv_hist, use_container_width=True)
        else:
            # Precipitation distribution
            precip_data = weather_df[weather_df['precipitation_sum'] > 0]['precipitation_sum']
            
            precip_hist = go.Figure()
            
            precip_hist.add_trace(go.Histogram(
                x=precip_data,
                nbinsx=30,
                name='Precipitation',
                marker_color='#48bb78',
                opacity=0.7
            ))
            
            precip_hist.update_layout(
                title='Precipitation Distribution (Rainy Days Only)',
                xaxis_title='Precipitation (mm)',
                yaxis_title='Frequency',
                height=350
            )
            
            st.plotly_chart(precip_hist, use_container_width=True)
    
    st.markdown("---")
    
    # Percentile Analysis
    st.markdown("## 📏 Percentile Analysis")
    
    cols = st.columns(4)
    percentiles = [10, 25, 50, 75, 90, 95, 99]
    
    with cols[0]:
        st.markdown("### Temperature")
        temp_percentiles = np.percentile(weather_df['temperature_2m_mean'], percentiles)
        for p, val in zip(percentiles, temp_percentiles):
            st.markdown(f"**{p}th:** {val:.1f}°C")
    
    with cols[1]:
        st.markdown("### Precipitation")
        precip_percentiles = np.percentile(weather_df['precipitation_sum'], percentiles)
        for p, val in zip(percentiles, precip_percentiles):
            st.markdown(f"**{p}th:** {val:.1f} mm")
    
    with cols[2]:
        st.markdown("### Wind Speed")
        wind_percentiles = np.percentile(weather_df['wind_speed_10m_max'], percentiles)
        for p, val in zip(percentiles, wind_percentiles):
            st.markdown(f"**{p}th:** {val:.1f} km/h")
    
    with cols[3]:
        if 'uv_index_max' in weather_df.columns:
            st.markdown("### UV Index")
            # Drop NaN values before calculating percentiles
            uv_data = weather_df['uv_index_max'].dropna()
            if len(uv_data) > 0:
                uv_percentiles = np.percentile(uv_data, percentiles)
                for p, val in zip(percentiles, uv_percentiles):
                    st.markdown(f"**{p}th:** {val:.1f}")
            else:
                st.markdown("*No UV data available*")
    
    st.markdown("---")
    
    # Extreme Events
    st.markdown("## ⚡ Extreme Weather Events")
    
    # Define thresholds
    temp_high_threshold = np.percentile(weather_df['temperature_2m_max'], 95)
    temp_low_threshold = np.percentile(weather_df['temperature_2m_min'], 5)
    precip_threshold = np.percentile(weather_df['precipitation_sum'], 95)
    wind_threshold = np.percentile(weather_df['wind_speed_10m_max'], 95)
    
    # Find extreme events
    hot_days = weather_df[weather_df['temperature_2m_max'] > temp_high_threshold]
    cold_days = weather_df[weather_df['temperature_2m_min'] < temp_low_threshold]
    heavy_rain = weather_df[weather_df['precipitation_sum'] > precip_threshold]
    windy_days = weather_df[weather_df['wind_speed_10m_max'] > wind_threshold]
    
    cols = st.columns(4)
    
    with cols[0]:
        st.metric(
            "🔥 Hot Days",
            len(hot_days),
            delta=f">{temp_high_threshold:.1f}°C"
        )
    
    with cols[1]:
        st.metric(
            "❄️ Cold Days",
            len(cold_days),
            delta=f"<{temp_low_threshold:.1f}°C"
        )
    
    with cols[2]:
        st.metric(
            "🌧️ Heavy Rain Days",
            len(heavy_rain),
            delta=f">{precip_threshold:.1f}mm"
        )
    
    with cols[3]:
        st.metric(
            "💨 Windy Days",
            len(windy_days),
            delta=f">{wind_threshold:.1f}km/h"
        )
    
    # High UV days
    if 'uv_index_max' in weather_df.columns:
        # Filter out NaN values
        high_uv_days = weather_df[weather_df['uv_index_max'].notna() & (weather_df['uv_index_max'] >= 8)]
        total_days_with_uv = len(weather_df[weather_df['uv_index_max'].notna()])
        
        if total_days_with_uv > 0:
            st.metric(
                "☀️ High UV Days (≥8)",
                len(high_uv_days),
                delta=f"{(len(high_uv_days)/total_days_with_uv*100):.1f}% of days with UV data"
            )
        else:
            st.info("UV data not available for this period")
    
    st.markdown("---")
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Historical Analysis", use_container_width=True):
            st.switch_page("pages/05_📊_Historical_Analysis.py")
    
    with col2:
        if st.button("🌧️ Annual Rainfall", use_container_width=True):
            st.switch_page("pages/08_🌧️_Annual_Rainfall.py")
    
    with col3:
        if st.button("🗺️ Change Location", use_container_width=True):
            st.switch_page("pages/01_🗺️_Interactive_Map.py")

else:
    st.error("❌ Unable to fetch weather data. Please try again.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
