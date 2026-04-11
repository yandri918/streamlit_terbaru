"""
Stock Price Analysis Dashboard
Comprehensive analysis of stock market data with interactive visualizations
"""
import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import plotly.graph_objects as go
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.data_loader import load_stock_data, preprocess_stock_data
from utils.chart_builder import (create_line_chart, create_candlestick_chart, 
                                  create_histogram, create_area_chart, 
                                  create_multi_line_chart, COLOR_SCHEME)
from utils.metrics import calculate_stock_metrics, get_summary_statistics

# Page configuration
st.set_page_config(
    page_title="Stock Price Analysis",
    page_icon="📈",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .insight-box {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📈 Stock Price Analysis")
st.markdown("**Analisis mendalam terhadap pergerakan harga saham dengan visualisasi interaktif**")

# Load and preprocess data
with st.spinner("Loading stock data..."):
    df = load_stock_data()
    
if df is not None:
    df = preprocess_stock_data(df)
    
    # Sidebar filters
    st.sidebar.markdown("### 📊 Data Filters")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df[(df['date'].dt.date >= start_date) & 
                        (df['date'].dt.date <= end_date)]
    else:
        df_filtered = df
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Data Points:** {len(df_filtered):,}")
    st.sidebar.markdown(f"**Date Range:** {df_filtered['date'].min().date()} to {df_filtered['date'].max().date()}")
    
    # Calculate metrics
    metrics = calculate_stock_metrics(df_filtered)
    
    # Key Metrics Dashboard
    st.markdown("## 📊 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Current Price</div>
            <div class="metric-value">${metrics['current_price']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        change_color = "🟢" if metrics['price_change'] >= 0 else "🔴"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Price Change</div>
            <div class="metric-value">{change_color} {metrics['price_change_pct']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Volatility</div>
            <div class="metric-value">{metrics['volatility']:.2f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Daily Return</div>
            <div class="metric-value">{metrics['avg_daily_return']:.3f}%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main visualizations
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Price Trends", 
        "🕯️ Candlestick", 
        "📊 Volume Analysis",
        "📉 Returns & Volatility",
        "📋 Statistics",
        "🔮 Price Prediction"
    ])
    
    with tab1:
        st.markdown("### Price Trends with Moving Averages")
        
        # Multi-line chart with price and moving averages
        chart_data = df_filtered[['date', 'last_value', 'ma_7', 'ma_30']].dropna()
        
        if len(chart_data) > 0:
            chart = create_multi_line_chart(
                chart_data,
                x='date',
                y_columns=['last_value', 'ma_7', 'ma_30'],
                title="Stock Price with 7-day and 30-day Moving Averages",
                width=800,
                height=450
            )
            st.altair_chart(chart, use_container_width=True)
            
            st.markdown("""
            <div class="insight-box">
                <strong>💡 Insight:</strong> Moving averages help identify trends. 
                When the price is above the moving average, it indicates an uptrend, 
                and when below, it suggests a downtrend.
            </div>
            """, unsafe_allow_html=True)
        
        # Price range visualization
        st.markdown("### Daily Price Range")
        
        range_chart = alt.Chart(df_filtered).mark_bar(opacity=0.7).encode(
            x=alt.X('date:T', title='Date'),
            y=alt.Y('price_range:Q', title='Price Range (High - Low)'),
            color=alt.value(COLOR_SCHEME['warning']),
            tooltip=['date:T', 'price_range:Q', 'high_value:Q', 'low_value:Q']
        ).properties(
            width=800,
            height=300,
            title='Daily Price Range (High - Low)'
        ).interactive()
        
        st.altair_chart(range_chart, use_container_width=True)
    
    with tab2:
        st.markdown("### Candlestick Chart")
        st.markdown("Interactive candlestick chart showing OHLC (Open, High, Low, Close) data")
        
        # Sample data for better performance
        sample_size = min(200, len(df_filtered))
        df_sample = df_filtered.tail(sample_size)
        
        candlestick = create_candlestick_chart(
            df_sample,
            date_col='date',
            open_col='open_value',
            high_col='high_value',
            low_col='low_value',
            close_col='last_value',
            width=900,
            height=500
        )
        
        st.altair_chart(candlestick, use_container_width=True)
        
        st.markdown("""
        <div class="insight-box">
            <strong>💡 How to Read:</strong> 
            Green bars indicate the closing price was higher than opening (bullish), 
            while red bars show the closing price was lower (bearish). 
            The lines represent the high and low prices for the day.
        </div>
        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Trading Volume Analysis")
        
        # Volume over time
        volume_chart = create_area_chart(
            df_filtered,
            x='date:T',
            y='turnover:Q',
            title="Trading Volume Over Time",
            color=COLOR_SCHEME['info'],
            width=800,
            height=400
        )
        
        st.altair_chart(volume_chart, use_container_width=True)
        
        # Volume distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Volume Distribution")
            volume_hist = create_histogram(
                df_filtered,
                column='turnover',
                bins=40,
                title="Distribution of Trading Volume",
                width=400,
                height=350
            )
            st.altair_chart(volume_hist, use_container_width=True)
        
        with col2:
            st.markdown("#### Volume Statistics")
            volume_stats = get_summary_statistics(df_filtered, 'turnover')
            
            st.metric("Average Volume", f"${volume_stats['mean']:,.2f}")
            st.metric("Median Volume", f"${volume_stats['median']:,.2f}")
            st.metric("Max Volume", f"${volume_stats['max']:,.2f}")
            st.metric("Std Deviation", f"${volume_stats['std']:,.2f}")
    
    with tab4:
        st.markdown("### Returns and Volatility Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Daily Returns Distribution")
            returns_data = df_filtered[df_filtered['daily_return'].notna()]
            
            if len(returns_data) > 0:
                returns_hist = create_histogram(
                    returns_data,
                    column='daily_return',
                    bins=50,
                    title="Distribution of Daily Returns",
                    width=450,
                    height=350
                )
                st.altair_chart(returns_hist, use_container_width=True)
        
        with col2:
            st.markdown("#### Volatility Over Time")
            volatility_data = df_filtered[df_filtered['volatility'].notna()]
            
            if len(volatility_data) > 0:
                volatility_chart = create_line_chart(
                    volatility_data,
                    x='date:T',
                    y='volatility:Q',
                    title="30-Day Rolling Volatility",
                    color=COLOR_SCHEME['danger'],
                    width=450,
                    height=350
                )
                st.altair_chart(volatility_chart, use_container_width=True)
        
        # Returns statistics
        st.markdown("#### Returns Statistics")
        if 'daily_return' in df_filtered.columns:
            returns_stats = get_summary_statistics(df_filtered, 'daily_return')
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Mean Return", f"{returns_stats['mean']*100:.4f}%")
            col2.metric("Median Return", f"{returns_stats['median']*100:.4f}%")
            col3.metric("Std Dev", f"{returns_stats['std']*100:.4f}%")
            col4.metric("Skewness", f"{returns_stats['skewness']:.4f}")
    
    with tab5:
        st.markdown("### Detailed Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Price Statistics")
            price_stats = get_summary_statistics(df_filtered, 'last_value')
            
            stats_df = pd.DataFrame({
                'Metric': ['Count', 'Mean', 'Median', 'Std Dev', 'Min', 'Max', 'Q25', 'Q75'],
                'Value': [
                    f"{price_stats['count']:,}",
                    f"${price_stats['mean']:.2f}",
                    f"${price_stats['median']:.2f}",
                    f"${price_stats['std']:.2f}",
                    f"${price_stats['min']:.2f}",
                    f"${price_stats['max']:.2f}",
                    f"${price_stats['q25']:.2f}",
                    f"${price_stats['q75']:.2f}"
                ]
            })
            
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("#### Key Insights")
            
            st.markdown(f"""
            - **Total Trading Days:** {metrics['total_trading_days']}
            - **Price Range:** ${metrics['lowest_price']:.2f} - ${metrics['highest_price']:.2f}
            - **Average Volume:** ${metrics['avg_volume']:,.2f}
            - **Volatility:** {metrics['volatility']:.2f}%
            """)
            
            # Trend indicator
            if metrics['price_change_pct'] > 0:
                st.success(f"📈 **Uptrend:** Price increased by {metrics['price_change_pct']:.2f}%")
            else:
                st.error(f"📉 **Downtrend:** Price decreased by {abs(metrics['price_change_pct']):.2f}%")
        
        # Raw data preview
        st.markdown("#### Data Preview")
        st.dataframe(
            df_filtered[['date', 'open_value', 'high_value', 'low_value', 
                        'last_value', 'turnover']].tail(20),
            use_container_width=True
        )
    
    with tab6:
        st.markdown("### 🔮 Stock Price Prediction")
        
        st.markdown("""
        Predict future stock prices using advanced machine learning models.
        Choose between LSTM (deep learning) and Prophet (time series forecasting).
        """)
        
        # Import prediction utilities
        from utils.stock_prediction import (train_lstm_model, train_prophet_model,
                                           predict_lstm, calculate_metrics,
                                           plot_predictions, plot_forecast,
                                           plot_training_history, plot_residuals,
                                           LSTM_AVAILABLE, PROPHET_AVAILABLE)
        
        # Model selection
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🤖 Prediction Model")
        
        model_type = st.sidebar.selectbox(
            "Select Model",
            ["LSTM Neural Network", "Prophet Forecasting", "Compare Both"]
        )
        
        # LSTM Parameters
        if "LSTM" in model_type:
            st.sidebar.markdown("#### LSTM Parameters")
            sequence_length = st.sidebar.slider("Sequence Length (days)", 10, 60, 30, 5)
            lstm_units = st.sidebar.slider("LSTM Units", 32, 256, 50, 16)
            num_layers = st.sidebar.slider("Number of Layers", 1, 3, 2, 1)
            epochs = st.sidebar.slider("Training Epochs", 10, 100, 50, 10)
            batch_size = st.sidebar.selectbox("Batch Size", [16, 32, 64, 128], index=1)
        
        # Prophet Parameters
        if "Prophet" in model_type:
            st.sidebar.markdown("#### Prophet Parameters")
            forecast_days = st.sidebar.slider("Forecast Horizon (days)", 7, 90, 30, 7)
            seasonality_mode = st.sidebar.selectbox("Seasonality Mode", ["additive", "multiplicative"])
            changepoint_scale = st.sidebar.slider("Changepoint Prior Scale", 0.001, 0.5, 0.05, 0.01)
        
        # Train button
        if st.sidebar.button("🚀 Train & Predict", type="primary"):
            
            # LSTM Model
            if model_type in ["LSTM Neural Network", "Compare Both"]:
                if not LSTM_AVAILABLE:
                    st.error("❌ TensorFlow/Keras not available. Please install: `pip install tensorflow`")
                else:
                    with st.spinner("Training LSTM model... This may take a few minutes."):
                        # Prepare data
                        price_data = df_filtered['last_value']
                        
                        # Train model
                        model, scaler, history, X_test, y_test = train_lstm_model(
                            price_data,
                            sequence_length=sequence_length,
                            lstm_units=lstm_units,
                            epochs=epochs,
                            batch_size=batch_size,
                            num_layers=num_layers
                        )
                        
                        if model is not None:
                            # Store in session state
                            st.session_state['lstm_model'] = model
                            st.session_state['lstm_scaler'] = scaler
                            st.session_state['lstm_history'] = history
                            st.session_state['lstm_X_test'] = X_test
                            st.session_state['lstm_y_test'] = y_test
                            st.session_state['lstm_sequence_length'] = sequence_length
                            st.session_state['price_data'] = price_data
                            
                            st.success("✅ LSTM model trained successfully!")
            
            # Prophet Model
            if model_type in ["Prophet Forecasting", "Compare Both"]:
                if not PROPHET_AVAILABLE:
                    st.error("❌ Prophet not available. Please install: `pip install prophet`")
                else:
                    with st.spinner("Training Prophet model..."):
                        # Train model
                        prophet_model, forecast = train_prophet_model(
                            df_filtered,
                            forecast_days=forecast_days,
                            seasonality_mode=seasonality_mode,
                            changepoint_prior_scale=changepoint_scale
                        )
                        
                        if prophet_model is not None:
                            # Store in session state
                            st.session_state['prophet_model'] = prophet_model
                            st.session_state['prophet_forecast'] = forecast
                            st.session_state['forecast_days'] = forecast_days
                            
                            st.success("✅ Prophet model trained successfully!")
        
        # Display LSTM Results
        if 'lstm_model' in st.session_state and model_type in ["LSTM Neural Network", "Compare Both"]:
            st.markdown("---")
            st.markdown("#### 🧠 LSTM Model Results")
            
            model = st.session_state['lstm_model']
            scaler = st.session_state['lstm_scaler']
            history = st.session_state['lstm_history']
            X_test = st.session_state['lstm_X_test']
            y_test = st.session_state['lstm_y_test']
            sequence_length = st.session_state['lstm_sequence_length']
            price_data = st.session_state['price_data']
            
            # Make predictions on test set
            y_pred = model.predict(X_test, verbose=0)
            
            # Inverse transform
            y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1)).flatten()
            y_pred_inv = scaler.inverse_transform(y_pred).flatten()
            
            # Calculate metrics
            metrics = calculate_metrics(y_test_inv, y_pred_inv)
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            col1.metric("RMSE", f"${metrics['RMSE']:.2f}")
            col2.metric("MAE", f"${metrics['MAE']:.2f}")
            col3.metric("MAPE", f"{metrics['MAPE']:.2f}%")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### Training History")
                history_fig = plot_training_history(history)
                st.plotly_chart(history_fig, use_container_width=True)
            
            with col2:
                st.markdown("##### Actual vs Predicted")
                pred_fig = plot_predictions(y_test_inv, y_pred_inv, "LSTM: Actual vs Predicted")
                st.plotly_chart(pred_fig, use_container_width=True)
            
            # Residuals
            st.markdown("##### Residual Analysis")
            residual_fig = plot_residuals(y_test_inv, y_pred_inv)
            st.plotly_chart(residual_fig, use_container_width=True)
            
            # Future predictions
            st.markdown("##### Future Price Predictions")
            
            pred_days = st.slider("Days to Predict", 7, 30, 14, 7, key="lstm_pred_days")
            
            if st.button("🔮 Generate LSTM Forecast", key="lstm_forecast_btn"):
                # Get last sequence
                scaled_data = scaler.transform(price_data.values.reshape(-1, 1))
                last_sequence = scaled_data[-sequence_length:].flatten()
                
                # Predict
                future_predictions = predict_lstm(model, scaler, last_sequence, pred_days)
                
                # Create forecast dataframe
                last_date = df_filtered['date'].max()
                future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=pred_days)
                
                forecast_df = pd.DataFrame({
                    'date': future_dates,
                    'predicted_price': future_predictions
                })
                
                # Store in session state
                st.session_state['lstm_forecast_df'] = forecast_df
            
            # Display forecast if available
            if 'lstm_forecast_df' in st.session_state:
                forecast_df = st.session_state['lstm_forecast_df']
                
                # Combine historical and forecast
                historical_df = df_filtered[['date', 'last_value']].tail(60)
                
                fig = go.Figure()
                
                # Historical prices
                fig.add_trace(go.Scatter(
                    x=historical_df['date'],
                    y=historical_df['last_value'],
                    mode='lines',
                    name='Historical',
                    line=dict(color='#667eea', width=2)
                ))
                
                # Forecast
                fig.add_trace(go.Scatter(
                    x=forecast_df['date'],
                    y=forecast_df['predicted_price'],
                    mode='lines+markers',
                    name='LSTM Forecast',
                    line=dict(color='#48bb78', width=2, dash='dash')
                ))
                
                fig.update_layout(
                    title='LSTM Stock Price Forecast',
                    xaxis_title='Date',
                    yaxis_title='Price ($)',
                    width=900,
                    height=500
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Show forecast table
                st.markdown("##### Forecast Table")
                st.dataframe(forecast_df.style.format({'predicted_price': '${:.2f}'}), use_container_width=True)
        
        # Display Prophet Results
        if 'prophet_model' in st.session_state and model_type in ["Prophet Forecasting", "Compare Both"]:
            st.markdown("---")
            st.markdown("#### 📊 Prophet Model Results")
            
            prophet_model = st.session_state['prophet_model']
            forecast = st.session_state['prophet_forecast']
            forecast_days = st.session_state['forecast_days']
            
            # Plot forecast
            forecast_fig = plot_forecast(df_filtered, forecast, "Prophet")
            st.plotly_chart(forecast_fig, use_container_width=True)
            
            # Forecast table
            st.markdown("##### Forecast Details")
            future_forecast = forecast[forecast['ds'] > df_filtered['date'].max()][['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
            future_forecast.columns = ['Date', 'Predicted Price', 'Lower Bound', 'Upper Bound']
            
            st.dataframe(
                future_forecast.style.format({
                    'Predicted Price': '${:.2f}',
                    'Lower Bound': '${:.2f}',
                    'Upper Bound': '${:.2f}'
                }),
                use_container_width=True
            )
            
            # Components plot
            st.markdown("##### Forecast Components")
            st.markdown("Prophet decomposes the time series into trend, weekly, and yearly seasonality.")
            
            # Note: Prophet's plot_components requires matplotlib, so we'll show a simplified version
            st.info("💡 Prophet model captures trend and seasonality patterns automatically.")
        
        # If no model trained yet
        if 'lstm_model' not in st.session_state and 'prophet_model' not in st.session_state:
            st.info("👆 Configure parameters in the sidebar and click 'Train & Predict' to start.")
            
            # Model comparison info
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("""
                <div class="insight-box">
                    <strong>🧠 LSTM Neural Network</strong><br>
                    <ul>
                        <li>Deep learning approach</li>
                        <li>Captures complex patterns</li>
                        <li>Requires more training time</li>
                        <li>Good for short-term predictions</li>
                        <li>Sensitive to hyperparameters</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("""
                <div class="insight-box">
                    <strong>📊 Prophet Forecasting</strong><br>
                    <ul>
                        <li>Time series forecasting</li>
                        <li>Automatic seasonality detection</li>
                        <li>Fast training</li>
                        <li>Good for long-term predictions</li>
                        <li>Handles missing data well</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)

else:
    st.error("❌ Failed to load stock data. Please check the data file.")
    st.info("💡 Make sure 'stock_price.csv' is in the data folder or parent directory.")
