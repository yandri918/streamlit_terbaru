"""
Machine Learning Forecasting Module
Implements ARIMA, Prophet, LSTM, and XGBoost for weather forecasting
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Evaluation metrics
from sklearn.metrics import mean_absolute_error, mean_squared_error

def calculate_mape(y_true, y_pred):
    """Calculate Mean Absolute Percentage Error"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / (y_true + 1e-10))) * 100

def calculate_metrics(y_true, y_pred):
    """Calculate MAE, RMSE, MAPE"""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = calculate_mape(y_true, y_pred)
    return {'MAE': mae, 'RMSE': rmse, 'MAPE': mape}

# Feature Engineering
def create_time_features(df):
    """Create time-based features"""
    df = df.copy()
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_of_month'] = df['date'].dt.day
    df['month'] = df['date'].dt.month
    df['quarter'] = df['date'].dt.quarter
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    return df

def create_lag_features(df, target_col, lags=[1, 2, 3, 7]):
    """Create lag features"""
    df = df.copy()
    for lag in lags:
        df[f'{target_col}_lag_{lag}'] = df[target_col].shift(lag)
    return df

def create_rolling_features(df, target_col, windows=[7, 14, 30]):
    """Create rolling statistics"""
    df = df.copy()
    for window in windows:
        df[f'{target_col}_rolling_mean_{window}'] = df[target_col].rolling(window=window).mean()
        df[f'{target_col}_rolling_std_{window}'] = df[target_col].rolling(window=window).std()
    return df

# ARIMA Model
def train_arima(data, forecast_days=7):
    """Train ARIMA model"""
    try:
        from statsmodels.tsa.arima.model import ARIMA
        from pmdarima import auto_arima
        
        # Auto ARIMA to find best parameters
        auto_model = auto_arima(
            data, 
            seasonal=False, 
            stepwise=True,
            suppress_warnings=True,
            error_action='ignore',
            max_p=5, max_q=5, max_d=2,
            trace=False
        )
        
        # Get best parameters
        order = auto_model.order
        
        # Train final model
        model = ARIMA(data, order=order)
        fitted_model = model.fit()
        
        # Forecast
        forecast = fitted_model.forecast(steps=forecast_days)
        
        # Get confidence intervals
        forecast_df = fitted_model.get_forecast(steps=forecast_days)
        conf_int = forecast_df.conf_int()
        
        return {
            'forecast': forecast.values,
            'lower_bound': conf_int.iloc[:, 0].values,
            'upper_bound': conf_int.iloc[:, 1].values,
            'params': order,
            'model': fitted_model
        }
    except Exception as e:
        print(f"ARIMA Error: {e}")
        return None

# Prophet Model
def train_prophet(df, forecast_days=7):
    """Train Prophet model"""
    try:
        from prophet import Prophet
        
        # Prepare data for Prophet
        prophet_df = df[['date', 'temperature_2m_mean']].copy()
        prophet_df.columns = ['ds', 'y']
        
        # Initialize and train model
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            yearly_seasonality=True,
            changepoint_prior_scale=0.05
        )
        model.fit(prophet_df)
        
        # Create future dataframe
        future = model.make_future_dataframe(periods=forecast_days)
        forecast = model.predict(future)
        
        # Get forecast values
        forecast_values = forecast.tail(forecast_days)
        
        return {
            'forecast': forecast_values['yhat'].values,
            'lower_bound': forecast_values['yhat_lower'].values,
            'upper_bound': forecast_values['yhat_upper'].values,
            'model': model,
            'full_forecast': forecast
        }
    except Exception as e:
        print(f"Prophet Error: {e}")
        return None

# LSTM Model
def train_lstm(data, forecast_days=7, lookback=30):
    """Train LSTM model"""
    try:
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import LSTM, Dense, Dropout
        from sklearn.preprocessing import MinMaxScaler
        
        # Scale data
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(data.reshape(-1, 1))
        
        # Create sequences
        X, y = [], []
        for i in range(lookback, len(scaled_data)):
            X.append(scaled_data[i-lookback:i, 0])
            y.append(scaled_data[i, 0])
        
        X, y = np.array(X), np.array(y)
        X = X.reshape((X.shape[0], X.shape[1], 1))
        
        # Build model
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(lookback, 1)),
            Dropout(0.2),
            LSTM(50, return_sequences=False),
            Dropout(0.2),
            Dense(25),
            Dense(1)
        ])
        
        model.compile(optimizer='adam', loss='mse')
        
        # Train model
        model.fit(X, y, epochs=50, batch_size=32, verbose=0)
        
        # Forecast
        last_sequence = scaled_data[-lookback:]
        forecasts = []
        
        for _ in range(forecast_days):
            pred = model.predict(last_sequence.reshape(1, lookback, 1), verbose=0)
            forecasts.append(pred[0, 0])
            last_sequence = np.append(last_sequence[1:], pred)
        
        # Inverse transform
        forecasts = scaler.inverse_transform(np.array(forecasts).reshape(-1, 1)).flatten()
        
        # Estimate confidence intervals (±1 std)
        std = np.std(data[-30:])
        
        return {
            'forecast': forecasts,
            'lower_bound': forecasts - std,
            'upper_bound': forecasts + std,
            'model': model,
            'scaler': scaler
        }
    except Exception as e:
        print(f"LSTM Error: {e}")
        return None

# XGBoost Model
def train_xgboost(df, forecast_days=7):
    """Train XGBoost model"""
    try:
        from xgboost import XGBRegressor
        from sklearn.preprocessing import StandardScaler
        
        # Feature engineering
        df = create_time_features(df)
        df = create_lag_features(df, 'temperature_2m_mean', lags=[1, 2, 3, 7])
        df = create_rolling_features(df, 'temperature_2m_mean', windows=[7, 14])
        
        # Drop NaN
        df = df.dropna()
        
        # Prepare features
        feature_cols = [col for col in df.columns if col not in ['date', 'temperature_2m_mean', 'time']]
        X = df[feature_cols]
        y = df['temperature_2m_mean']
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train model
        model = XGBRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        model.fit(X_scaled, y)
        
        # Create future features
        last_date = df['date'].max()
        future_dates = [last_date + timedelta(days=i+1) for i in range(forecast_days)]
        
        forecasts = []
        for future_date in future_dates:
            # Create features for future date
            future_row = {
                'day_of_week': future_date.dayofweek,
                'day_of_month': future_date.day,
                'month': future_date.month,
                'quarter': (future_date.month - 1) // 3 + 1,
                'is_weekend': 1 if future_date.dayofweek >= 5 else 0
            }
            
            # Add lag features (use last known values and predictions)
            recent_temps = list(df['temperature_2m_mean'].tail(7).values) + forecasts
            for lag in [1, 2, 3, 7]:
                if len(recent_temps) >= lag:
                    future_row[f'temperature_2m_mean_lag_{lag}'] = recent_temps[-lag]
                else:
                    future_row[f'temperature_2m_mean_lag_{lag}'] = df['temperature_2m_mean'].mean()
            
            # Add rolling features (approximate)
            for window in [7, 14]:
                future_row[f'temperature_2m_mean_rolling_mean_{window}'] = df['temperature_2m_mean'].tail(window).mean()
                future_row[f'temperature_2m_mean_rolling_std_{window}'] = df['temperature_2m_mean'].tail(window).std()
            
            # Predict
            X_future = pd.DataFrame([future_row])[feature_cols]
            X_future_scaled = scaler.transform(X_future)
            pred = model.predict(X_future_scaled)[0]
            forecasts.append(pred)
        
        # Estimate confidence intervals
        std = np.std(y[-30:])
        
        return {
            'forecast': np.array(forecasts),
            'lower_bound': np.array(forecasts) - std,
            'upper_bound': np.array(forecasts) + std,
            'model': model,
            'feature_importance': dict(zip(feature_cols, model.feature_importances_))
        }
    except Exception as e:
        print(f"XGBoost Error: {e}")
        return None

# Ensemble Forecasting
def ensemble_forecast(forecasts, weights=None):
    """Combine multiple forecasts using weighted average"""
    if weights is None:
        weights = [1/len(forecasts)] * len(forecasts)
    
    ensemble = np.zeros_like(forecasts[0])
    for forecast, weight in zip(forecasts, weights):
        ensemble += forecast * weight
    
    return ensemble
