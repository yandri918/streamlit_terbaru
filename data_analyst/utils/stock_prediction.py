"""
Stock price prediction using LSTM and Prophet
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error

# LSTM imports
try:
    from tensorflow import keras
    from keras.models import Sequential
    from keras.layers import LSTM, Dense, Dropout
    from keras.callbacks import EarlyStopping
    LSTM_AVAILABLE = True
except ImportError:
    LSTM_AVAILABLE = False

# Prophet imports
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False

@st.cache_resource
def train_lstm_model(data, sequence_length=30, lstm_units=50, epochs=50, 
                     batch_size=32, num_layers=2):
    """
    Train LSTM model for stock price prediction
    
    Args:
        data: Price data (pandas Series or array)
        sequence_length: Number of days to look back
        lstm_units: Number of LSTM units per layer
        epochs: Training epochs
        batch_size: Batch size
        num_layers: Number of LSTM layers
    
    Returns:
        model, scaler, training_history
    """
    if not LSTM_AVAILABLE:
        st.error("TensorFlow/Keras not available. Please install tensorflow.")
        return None, None, None
    
    # Prepare data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data.values.reshape(-1, 1))
    
    # Create sequences
    X, y = [], []
    for i in range(sequence_length, len(scaled_data)):
        X.append(scaled_data[i-sequence_length:i, 0])
        y.append(scaled_data[i, 0])
    
    X, y = np.array(X), np.array(y)
    X = X.reshape((X.shape[0], X.shape[1], 1))
    
    # Split data
    split = int(0.8 * len(X))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    
    # Build model
    model = Sequential()
    
    # First LSTM layer
    model.add(LSTM(units=lstm_units, return_sequences=(num_layers > 1), 
                   input_shape=(X_train.shape[1], 1)))
    model.add(Dropout(0.2))
    
    # Additional LSTM layers
    for i in range(1, num_layers):
        return_seq = (i < num_layers - 1)
        model.add(LSTM(units=lstm_units, return_sequences=return_seq))
        model.add(Dropout(0.2))
    
    # Output layer
    model.add(Dense(units=1))
    
    # Compile
    model.compile(optimizer='adam', loss='mean_squared_error')
    
    # Train
    early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    
    history = model.fit(
        X_train, y_train,
        epochs=epochs,
        batch_size=batch_size,
        validation_data=(X_test, y_test),
        callbacks=[early_stop],
        verbose=0
    )
    
    return model, scaler, history, X_test, y_test

@st.cache_resource
def train_prophet_model(df, forecast_days=30, seasonality_mode='additive',
                       changepoint_prior_scale=0.05):
    """
    Train Prophet model for stock price prediction
    
    Args:
        df: DataFrame with 'date' and 'price' columns
        forecast_days: Number of days to forecast
        seasonality_mode: 'additive' or 'multiplicative'
        changepoint_prior_scale: Flexibility of trend changes
    
    Returns:
        model, forecast
    """
    if not PROPHET_AVAILABLE:
        st.error("Prophet not available. Please install prophet.")
        return None, None
    
    # Prepare data for Prophet
    prophet_df = df[['date', 'last_value']].copy()
    prophet_df.columns = ['ds', 'y']
    
    # Initialize and train model
    model = Prophet(
        seasonality_mode=seasonality_mode,
        changepoint_prior_scale=changepoint_prior_scale,
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=True
    )
    
    model.fit(prophet_df)
    
    # Make future dataframe
    future = model.make_future_dataframe(periods=forecast_days)
    forecast = model.predict(future)
    
    return model, forecast

def predict_lstm(model, scaler, last_sequence, days_ahead=7):
    """
    Make future predictions with LSTM
    
    Args:
        model: Trained LSTM model
        scaler: Fitted scaler
        last_sequence: Last n days of data
        days_ahead: Number of days to predict
    
    Returns:
        predictions array
    """
    predictions = []
    current_sequence = last_sequence.copy()
    
    for _ in range(days_ahead):
        # Reshape for prediction
        current_input = current_sequence.reshape((1, len(current_sequence), 1))
        
        # Predict next value
        next_pred = model.predict(current_input, verbose=0)[0, 0]
        predictions.append(next_pred)
        
        # Update sequence
        current_sequence = np.append(current_sequence[1:], next_pred)
    
    # Inverse transform
    predictions = scaler.inverse_transform(np.array(predictions).reshape(-1, 1))
    
    return predictions.flatten()

def calculate_metrics(y_true, y_pred):
    """
    Calculate prediction metrics
    
    Returns:
        Dictionary with RMSE, MAE, MAPE
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    
    return {
        'RMSE': rmse,
        'MAE': mae,
        'MAPE': mape
    }

def plot_predictions(actual, predicted, title="Actual vs Predicted"):
    """
    Plot actual vs predicted prices
    """
    fig = go.Figure()
    
    # Actual prices
    fig.add_trace(go.Scatter(
        x=list(range(len(actual))),
        y=actual,
        mode='lines',
        name='Actual',
        line=dict(color='#667eea', width=2)
    ))
    
    # Predicted prices
    fig.add_trace(go.Scatter(
        x=list(range(len(predicted))),
        y=predicted,
        mode='lines',
        name='Predicted',
        line=dict(color='#f56565', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title='Time',
        yaxis_title='Price',
        width=800,
        height=400,
        showlegend=True
    )
    
    return fig

def plot_forecast(df, forecast, model_name="Prophet"):
    """
    Plot forecast with confidence intervals
    """
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['last_value'],
        mode='lines',
        name='Historical',
        line=dict(color='#667eea', width=2)
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'],
        mode='lines',
        name='Forecast',
        line=dict(color='#48bb78', width=2)
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=forecast['ds'].tolist() + forecast['ds'].tolist()[::-1],
        y=forecast['yhat_upper'].tolist() + forecast['yhat_lower'].tolist()[::-1],
        fill='toself',
        fillcolor='rgba(72, 187, 120, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='Confidence Interval',
        showlegend=True
    ))
    
    fig.update_layout(
        title=f'{model_name} Stock Price Forecast',
        xaxis_title='Date',
        yaxis_title='Price',
        width=900,
        height=500,
        showlegend=True
    )
    
    return fig

def plot_training_history(history):
    """
    Plot LSTM training history
    """
    fig = go.Figure()
    
    # Training loss
    fig.add_trace(go.Scatter(
        y=history.history['loss'],
        mode='lines',
        name='Training Loss',
        line=dict(color='#667eea', width=2)
    ))
    
    # Validation loss
    fig.add_trace(go.Scatter(
        y=history.history['val_loss'],
        mode='lines',
        name='Validation Loss',
        line=dict(color='#f56565', width=2)
    ))
    
    fig.update_layout(
        title='Model Training History',
        xaxis_title='Epoch',
        yaxis_title='Loss (MSE)',
        width=700,
        height=400,
        showlegend=True
    )
    
    return fig

def plot_residuals(y_true, y_pred):
    """
    Plot residuals (prediction errors)
    """
    residuals = y_true - y_pred
    
    fig = go.Figure()
    
    # Residuals scatter
    fig.add_trace(go.Scatter(
        x=list(range(len(residuals))),
        y=residuals,
        mode='markers',
        name='Residuals',
        marker=dict(color='#667eea', size=6)
    ))
    
    # Zero line
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    
    fig.update_layout(
        title='Residual Plot',
        xaxis_title='Sample',
        yaxis_title='Residual (Actual - Predicted)',
        width=700,
        height=400
    )
    
    return fig
