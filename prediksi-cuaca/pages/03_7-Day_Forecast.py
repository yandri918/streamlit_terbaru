"""
7-Day Weather Forecast
Weekly weather predictions with detailed visualizations
"""
import streamlit as st
import sys
import os
import pandas as pd
import altair as alt

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_daily_forecast, get_weather_emoji, get_weather_description

# Page configuration
st.set_page_config(
    page_title="7-Day Forecast",
    page_icon="📅",
    layout="wide"
)

# Header
st.title("📅 7-Day Weather Forecast")
st.markdown("**Weekly weather predictions for your selected location**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Fetch forecast
with st.spinner("Fetching 7-day forecast..."):
    forecast_df = get_daily_forecast(
        st.session_state['selected_lat'],
        st.session_state['selected_lon'],
        days=7
    )

if forecast_df is not None and len(forecast_df) > 0:
    # Display forecast cards
    st.markdown("### 📊 Daily Forecast")
    
    cols = st.columns(7)
    
    for idx, row in forecast_df.iterrows():
        with cols[idx % 7]:
            emoji = get_weather_emoji(row['weather_code'])
            day_name = row['time'].strftime('%a')
            date = row['time'].strftime('%m/%d')
            
            st.markdown(f"""
            <div style="background: #f7fafc; padding: 1rem; border-radius: 8px; text-align: center; border: 2px solid #e2e8f0;">
                <h4 style="margin: 0;">{day_name}</h4>
                <p style="font-size: 0.8rem; color: #666; margin: 0.2rem 0;">{date}</p>
                <div style="font-size: 3rem; margin: 0.5rem 0;">{emoji}</div>
                <p style="font-size: 1.2rem; font-weight: 700; margin: 0.5rem 0; color: #e53e3e;">
                    {row['temperature_2m_max']:.1f}°
                </p>
                <p style="font-size: 1rem; color: #4299e1; margin: 0;">
                    {row['temperature_2m_min']:.1f}°
                </p>
                <p style="font-size: 0.8rem; color: #666; margin: 0.5rem 0;">
                    💧 {row['precipitation_probability_max']:.0f}%
                </p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Temperature chart
    st.markdown("### 🌡️ Temperature Trends")
    
    # Prepare data for chart
    chart_data = forecast_df.copy()
    chart_data['date'] = chart_data['time'].dt.strftime('%m/%d')
    
    # Create temperature line chart
    temp_chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x=alt.X('date:N', title='Date'),
        y=alt.Y('temperature_2m_max:Q', title='Temperature (°C)', scale=alt.Scale(zero=False)),
        color=alt.value('#e53e3e'),
        tooltip=['date', 'temperature_2m_max', 'temperature_2m_min']
    ).properties(
        height=300
    )
    
    temp_min_chart = alt.Chart(chart_data).mark_line(point=True).encode(
        x=alt.X('date:N', title='Date'),
        y=alt.Y('temperature_2m_min:Q', title='Temperature (°C)'),
        color=alt.value('#4299e1'),
        tooltip=['date', 'temperature_2m_max', 'temperature_2m_min']
    )
    
    st.altair_chart(temp_chart + temp_min_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Precipitation chart
    st.markdown("### 💧 Precipitation Probability")
    
    precip_chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('date:N', title='Date'),
        y=alt.Y('precipitation_probability_max:Q', title='Probability (%)', scale=alt.Scale(domain=[0, 100])),
        color=alt.Color('precipitation_probability_max:Q', scale=alt.Scale(scheme='blues'), legend=None),
        tooltip=['date', 'precipitation_probability_max', 'precipitation_sum']
    ).properties(
        height=300
    )
    
    st.altair_chart(precip_chart, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed table
    st.markdown("### 📋 Detailed Forecast Table")
    
    display_df = forecast_df.copy()
    display_df['Date'] = display_df['time'].dt.strftime('%Y-%m-%d (%A)')
    display_df['Weather'] = display_df['weather_code'].apply(lambda x: f"{get_weather_emoji(x)} {get_weather_description(x)}")
    display_df['High/Low'] = display_df.apply(lambda x: f"{x['temperature_2m_max']:.1f}° / {x['temperature_2m_min']:.1f}°", axis=1)
    display_df['Precipitation'] = display_df['precipitation_probability_max'].apply(lambda x: f"{x:.0f}%")
    display_df['Wind'] = display_df['wind_speed_10m_max'].apply(lambda x: f"{x:.1f} km/h")
    display_df['UV Index'] = display_df['uv_index_max'].apply(lambda x: f"{x:.1f}")
    
    st.dataframe(
        display_df[['Date', 'Weather', 'High/Low', 'Precipitation', 'Wind', 'UV Index']],
        use_container_width=True,
        hide_index=True
    )
    
    st.markdown("---")
    
    # Quick navigation
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🌤️ Current Weather", use_container_width=True):
            st.switch_page("pages/02_🌤️_Current_Weather.py")
    
    with col2:
        if st.button("⏰ Hourly Forecast", use_container_width=True):
            st.switch_page("pages/04_⏰_Hourly_Forecast.py")
    
    with col3:
        if st.button("🗺️ Change Location", use_container_width=True):
            st.switch_page("pages/01_🗺️_Interactive_Map.py")

else:
    st.error("❌ Unable to fetch forecast data. Please try again or select a different location.")
    if st.button("🗺️ Select Different Location"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
