"""
ML Weather Forecasting
Compare ARIMA, Prophet, LSTM, and XGBoost models
"""
import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.weather_api import get_historical_weather, get_daily_forecast
from utils.ml_forecasting import (
    train_arima, train_prophet, train_lstm, train_xgboost,
    calculate_metrics, ensemble_forecast
)

# Page configuration
st.set_page_config(
    page_title="ML Forecasting",
    page_icon="🤖",
    layout="wide"
)

# Header
st.title("🤖 ML Weather Forecasting")
st.markdown("**Compare machine learning models with API forecasts**")

# Check if location is selected
if 'selected_lat' not in st.session_state:
    st.warning("⚠️ No location selected. Please select a location from the Interactive Map page first.")
    if st.button("🗺️ Go to Interactive Map"):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
    st.stop()

st.markdown(f"**📍 Location:** {st.session_state.get('selected_location', 'Unknown')}")
st.markdown("---")

# Sidebar - Model Configuration
st.sidebar.markdown("### ⚙️ Model Configuration")

# Select models to train
st.sidebar.markdown("**Select Models:**")
use_arima = st.sidebar.checkbox("ARIMA (Time Series)", value=True)
use_prophet = st.sidebar.checkbox("Prophet (Facebook)", value=True)
use_lstm = st.sidebar.checkbox("LSTM (Deep Learning)", value=True)
use_xgboost = st.sidebar.checkbox("XGBoost (Gradient Boosting)", value=True)

# Forecast settings
forecast_days = st.sidebar.slider("Forecast Days", 3, 14, 7)
historical_days = st.sidebar.slider("Historical Data (days)", 60, 365, 90)

# Training button
train_button = st.sidebar.button("🚀 Train Models", type="primary", use_container_width=True)

# Main content
if train_button:
    # Fetch historical data
    with st.spinner(f"Fetching {historical_days} days of historical data..."):
        end_date = datetime.now() - timedelta(days=1)
        start_date = end_date - timedelta(days=historical_days)
        
        historical_df = get_historical_weather(
            st.session_state['selected_lat'],
            st.session_state['selected_lon'],
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )
        
        # Get API forecast for comparison
        api_forecast = get_daily_forecast(
            st.session_state['selected_lat'],
            st.session_state['selected_lon'],
            days=forecast_days
        )
    
    if historical_df is not None and len(historical_df) > 30:
        historical_df['date'] = pd.to_datetime(historical_df['time'])
        temperature_data = historical_df['temperature_2m_mean'].values
        
        st.success(f"✅ Loaded {len(historical_df)} days of historical data")
        
        # Results storage
        results = {}
        training_times = {}
        
        # Progress tracking
        st.markdown("## 🔄 Training Models")
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        models_to_train = []
        if use_arima: models_to_train.append('ARIMA')
        if use_prophet: models_to_train.append('Prophet')
        if use_lstm: models_to_train.append('LSTM')
        if use_xgboost: models_to_train.append('XGBoost')
        
        total_models = len(models_to_train)
        
        for idx, model_name in enumerate(models_to_train):
            status_text.markdown(f"**Training {model_name}...**")
            start_time = time.time()
            
            try:
                if model_name == 'ARIMA':
                    result = train_arima(temperature_data, forecast_days)
                elif model_name == 'Prophet':
                    result = train_prophet(historical_df, forecast_days)
                elif model_name == 'LSTM':
                    result = train_lstm(temperature_data, forecast_days)
                elif model_name == 'XGBoost':
                    result = train_xgboost(historical_df, forecast_days)
                
                if result:
                    results[model_name] = result
                    training_times[model_name] = time.time() - start_time
                    status_text.markdown(f"✅ **{model_name} trained** ({training_times[model_name]:.1f}s)")
                else:
                    status_text.markdown(f"❌ **{model_name} failed**")
            
            except Exception as e:
                st.error(f"Error training {model_name}: {str(e)}")
            
            progress_bar.progress((idx + 1) / total_models)
            time.sleep(0.5)
        
        status_text.markdown("✅ **All models trained successfully!**")
        
        st.markdown("---")
        
        # Forecast Visualization
        st.markdown("## 📈 Forecast Comparison")
        
        # Create forecast dates
        last_date = historical_df['date'].max()
        forecast_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]
        
        # Create comparison chart
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=historical_df['date'].tail(30),
            y=historical_df['temperature_2m_mean'].tail(30),
            name='Historical',
            line=dict(color='gray', width=2),
            mode='lines'
        ))
        
        # ML Model forecasts
        colors = {
            'ARIMA': '#4299e1',
            'Prophet': '#48bb78',
            'LSTM': '#9f7aea',
            'XGBoost': '#ed8936'
        }
        
        for model_name, result in results.items():
            # Main forecast line
            fig.add_trace(go.Scatter(
                x=forecast_dates,
                y=result['forecast'],
                name=model_name,
                line=dict(color=colors.get(model_name, '#000'), width=2),
                mode='lines+markers'
            ))
            
            # Confidence interval
            fig.add_trace(go.Scatter(
                x=forecast_dates + forecast_dates[::-1],
                y=list(result['upper_bound']) + list(result['lower_bound'][::-1]),
                fill='toself',
                fillcolor=colors.get(model_name, '#000').replace('1', '0.2'),
                line=dict(color='rgba(255,255,255,0)'),
                showlegend=False,
                name=f'{model_name} CI'
            ))
        
        # API Forecast
        if api_forecast is not None and len(api_forecast) > 0:
            api_dates = pd.to_datetime(api_forecast['time']).tolist()[:forecast_days]
            
            # Try different column names for temperature
            if 'temperature_2m_mean' in api_forecast.columns:
                api_temps = api_forecast['temperature_2m_mean'].tolist()[:forecast_days]
            elif 'temperature_2m_max' in api_forecast.columns and 'temperature_2m_min' in api_forecast.columns:
                # Calculate mean from max and min
                api_temps = ((api_forecast['temperature_2m_max'] + api_forecast['temperature_2m_min']) / 2).tolist()[:forecast_days]
            else:
                # Fallback to first temperature column found
                temp_cols = [col for col in api_forecast.columns if 'temperature' in col.lower()]
                if temp_cols:
                    api_temps = api_forecast[temp_cols[0]].tolist()[:forecast_days]
                else:
                    api_temps = None
            
            if api_temps:
                fig.add_trace(go.Scatter(
                    x=api_dates,
                    y=api_temps,
                    name='API Forecast',
                    line=dict(color='#e53e3e', width=3, dash='dash'),
                    mode='lines+markers'
                ))
        
        fig.update_layout(
            title='Temperature Forecast Comparison',
            xaxis_title='Date',
            yaxis_title='Temperature (°C)',
            height=500,
            hovermode='x unified',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        
        # Model Performance
        st.markdown("## 📊 Model Performance")
        
        # Calculate metrics against API forecast (as baseline)
        if api_forecast is not None and len(api_forecast) > 0:
            # Get API temperatures with proper column handling
            if 'temperature_2m_mean' in api_forecast.columns:
                api_temps_list = api_forecast['temperature_2m_mean'].tolist()[:forecast_days]
            elif 'temperature_2m_max' in api_forecast.columns and 'temperature_2m_min' in api_forecast.columns:
                api_temps_list = ((api_forecast['temperature_2m_max'] + api_forecast['temperature_2m_min']) / 2).tolist()[:forecast_days]
            else:
                temp_cols = [col for col in api_forecast.columns if 'temperature' in col.lower()]
                if temp_cols:
                    api_temps_list = api_forecast[temp_cols[0]].tolist()[:forecast_days]
                else:
                    api_temps_list = None
            
            if api_temps_list:
                api_temps_array = np.array(api_temps_list)
                
                metrics_data = []
                for model_name, result in results.items():
                    model_forecast = result['forecast'][:len(api_temps_array)]
                    metrics = calculate_metrics(api_temps_array, model_forecast)
                    metrics_data.append({
                        'Model': model_name,
                        'MAE (°C)': f"{metrics['MAE']:.2f}",
                        'RMSE (°C)': f"{metrics['RMSE']:.2f}",
                        'MAPE (%)': f"{metrics['MAPE']:.2f}",
                        'Training Time (s)': f"{training_times[model_name]:.1f}"
                    })
                
                metrics_df = pd.DataFrame(metrics_data)
                st.dataframe(metrics_df, use_container_width=True, hide_index=True)
                
                st.info("📌 **Note:** Metrics calculated by comparing ML forecasts with API forecast (baseline)")
            else:
                st.warning("⚠️ Unable to calculate metrics - API forecast temperature data not available")
        else:
            st.warning("⚠️ API forecast not available for comparison")
        
        st.markdown("---")
        
        # Ensemble Forecast
        st.markdown("## 🎯 Ensemble Forecast")
        
        if len(results) > 1:
            # Calculate ensemble
            forecasts_list = [result['forecast'] for result in results.values()]
            ensemble = ensemble_forecast(forecasts_list)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Ensemble chart
                fig_ensemble = go.Figure()
                
                # Historical
                fig_ensemble.add_trace(go.Scatter(
                    x=historical_df['date'].tail(30),
                    y=historical_df['temperature_2m_mean'].tail(30),
                    name='Historical',
                    line=dict(color='gray', width=2)
                ))
                
                # Ensemble
                fig_ensemble.add_trace(go.Scatter(
                    x=forecast_dates,
                    y=ensemble,
                    name='Ensemble',
                    line=dict(color='#f6ad55', width=3),
                    mode='lines+markers',
                    marker=dict(size=8)
                ))
                
                # API
                if api_forecast is not None and len(api_forecast) > 0:
                    # Get API temps with proper column handling
                    if 'temperature_2m_mean' in api_forecast.columns:
                        api_temps_for_chart = api_forecast['temperature_2m_mean'].tolist()[:forecast_days]
                    elif 'temperature_2m_max' in api_forecast.columns and 'temperature_2m_min' in api_forecast.columns:
                        api_temps_for_chart = ((api_forecast['temperature_2m_max'] + api_forecast['temperature_2m_min']) / 2).tolist()[:forecast_days]
                    else:
                        temp_cols = [col for col in api_forecast.columns if 'temperature' in col.lower()]
                        api_temps_for_chart = api_forecast[temp_cols[0]].tolist()[:forecast_days] if temp_cols else None
                    
                    if api_temps_for_chart:
                        fig_ensemble.add_trace(go.Scatter(
                            x=api_dates,
                            y=api_temps_for_chart,
                            name='API',
                            line=dict(color='#e53e3e', width=2, dash='dash')
                        ))
                
                fig_ensemble.update_layout(
                    title='Ensemble vs API Forecast',
                    xaxis_title='Date',
                    yaxis_title='Temperature (°C)',
                    height=400
                )
                
                st.plotly_chart(fig_ensemble, use_container_width=True)
            
            with col2:
                st.markdown("**Ensemble Method:**")
                st.markdown("- Equal weight average")
                st.markdown(f"- {len(results)} models combined")
                
                if api_forecast is not None and len(api_forecast) > 0 and api_temps_list:
                    ensemble_metrics = calculate_metrics(api_temps_array, ensemble[:len(api_temps_array)])
                    st.markdown("**Performance:**")
                    st.metric("MAE", f"{ensemble_metrics['MAE']:.2f}°C")
                    st.metric("RMSE", f"{ensemble_metrics['RMSE']:.2f}°C")
                    st.metric("MAPE", f"{ensemble_metrics['MAPE']:.2f}%")
        
        st.markdown("---")
        
        # Feature Importance (XGBoost)
        if 'XGBoost' in results and 'feature_importance' in results['XGBoost']:
            st.markdown("## 🔍 Feature Importance (XGBoost)")
            
            importance = results['XGBoost']['feature_importance']
            importance_df = pd.DataFrame(
                list(importance.items()),
                columns=['Feature', 'Importance']
            ).sort_values('Importance', ascending=False).head(10)
            
            fig_importance = go.Figure(go.Bar(
                x=importance_df['Importance'],
                y=importance_df['Feature'],
                orientation='h',
                marker=dict(color='#ed8936')
            ))
            
            fig_importance.update_layout(
                title='Top 10 Most Important Features',
                xaxis_title='Importance',
                yaxis_title='Feature',
                height=400
            )
            
            st.plotly_chart(fig_importance, use_container_width=True)
        
        st.markdown("---")
        
        # Export Results
        st.markdown("## 💾 Export Forecasts")
        
        # Prepare export data
        export_data = {'Date': [d.strftime('%Y-%m-%d') for d in forecast_dates]}
        
        for model_name, result in results.items():
            export_data[f'{model_name}_Forecast'] = result['forecast']
            export_data[f'{model_name}_Lower'] = result['lower_bound']
            export_data[f'{model_name}_Upper'] = result['upper_bound']
        
        if api_forecast is not None and len(api_forecast) > 0:
            # Get API temps with proper column handling
            if 'temperature_2m_mean' in api_forecast.columns:
                export_data['API_Forecast'] = api_forecast['temperature_2m_mean'].tolist()[:forecast_days]
            elif 'temperature_2m_max' in api_forecast.columns and 'temperature_2m_min' in api_forecast.columns:
                export_data['API_Forecast'] = ((api_forecast['temperature_2m_max'] + api_forecast['temperature_2m_min']) / 2).tolist()[:forecast_days]
            else:
                temp_cols = [col for col in api_forecast.columns if 'temperature' in col.lower()]
                if temp_cols:
                    export_data['API_Forecast'] = api_forecast[temp_cols[0]].tolist()[:forecast_days]
        
        if len(results) > 1:
            export_data['Ensemble_Forecast'] = ensemble
        
        export_df = pd.DataFrame(export_data)
        csv = export_df.to_csv(index=False)
        
        st.download_button(
            label="📥 Download Forecasts (CSV)",
            data=csv,
            file_name=f"ml_forecasts_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
        
    else:
        st.error("❌ Insufficient historical data. Please try a different location or time period.")

else:
    # Initial state - show instructions
    st.info("👈 **Configure models in the sidebar and click 'Train Models' to start**")
    
    st.markdown("## 🤖 Available Models")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 📊 ARIMA
        - **Type:** Statistical time series
        - **Best for:** Short-term forecasts
        - **Speed:** Fast (~5-10s)
        - **Pros:** Interpretable, reliable
        - **Cons:** Univariate only
        """)
        
        st.markdown("""
        ### 🧠 LSTM
        - **Type:** Deep learning (RNN)
        - **Best for:** Complex patterns
        - **Speed:** Slow (~30-60s)
        - **Pros:** Captures non-linearity
        - **Cons:** Requires more data
        """)
    
    with col2:
        st.markdown("""
        ### 📈 Prophet
        - **Type:** Additive model
        - **Best for:** Seasonality
        - **Speed:** Medium (~10-20s)
        - **Pros:** Handles missing data
        - **Cons:** Less flexible
        """)
        
        st.markdown("""
        ### 🚀 XGBoost
        - **Type:** Gradient boosting
        - **Best for:** Feature-rich data
        - **Speed:** Medium (~10-15s)
        - **Pros:** Feature importance
        - **Cons:** Requires engineering
        """)

st.markdown("---")

# Quick navigation
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📊 Historical Analysis", use_container_width=True):
        st.switch_page("pages/05_📊_Historical_Analysis.py")

with col2:
    if st.button("📈 Weather Statistics", use_container_width=True):
        st.switch_page("pages/09_📈_Weather_Statistics.py")

with col3:
    if st.button("🗺️ Change Location", use_container_width=True):
        st.switch_page("pages/01_🗺️_Interactive_Map.py")
