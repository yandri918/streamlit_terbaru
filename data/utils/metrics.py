"""
Statistical and analytical metrics calculations
"""
import pandas as pd
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

def calculate_stock_metrics(df):
    """Calculate key stock market metrics"""
    if df is None or len(df) == 0:
        return {}
    
    metrics = {
        'current_price': df['last_value'].iloc[-1],
        'price_change': df['last_value'].iloc[-1] - df['last_value'].iloc[0],
        'price_change_pct': ((df['last_value'].iloc[-1] - df['last_value'].iloc[0]) / 
                            df['last_value'].iloc[0] * 100),
        'highest_price': df['high_value'].max(),
        'lowest_price': df['low_value'].min(),
        'avg_volume': df['turnover'].mean(),
        'avg_daily_return': df['daily_return'].mean() * 100 if 'daily_return' in df.columns else 0,
        'volatility': df['daily_return'].std() * 100 if 'daily_return' in df.columns else 0,
        'total_trading_days': len(df)
    }
    
    return metrics

def calculate_moving_average(series, window):
    """Calculate simple moving average"""
    return series.rolling(window=window).mean()

def calculate_ema(series, span):
    """Calculate exponential moving average"""
    return series.ewm(span=span, adjust=False).mean()

def calculate_rsi(series, period=14):
    """Calculate Relative Strength Index"""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def calculate_bollinger_bands(series, window=20, num_std=2):
    """Calculate Bollinger Bands"""
    sma = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()
    
    upper_band = sma + (std * num_std)
    lower_band = sma - (std * num_std)
    
    return sma, upper_band, lower_band

def calculate_fraud_metrics(df, class_column='Class'):
    """Calculate fraud detection metrics"""
    if df is None or len(df) == 0:
        return {}
    
    total_transactions = len(df)
    fraud_count = df[class_column].sum()
    legitimate_count = total_transactions - fraud_count
    
    metrics = {
        'total_transactions': total_transactions,
        'fraud_count': int(fraud_count),
        'legitimate_count': int(legitimate_count),
        'fraud_percentage': (fraud_count / total_transactions * 100),
        'avg_fraud_amount': df[df[class_column] == 1]['Amount'].mean() if fraud_count > 0 else 0,
        'avg_legitimate_amount': df[df[class_column] == 0]['Amount'].mean(),
        'max_fraud_amount': df[df[class_column] == 1]['Amount'].max() if fraud_count > 0 else 0,
        'class_imbalance_ratio': legitimate_count / fraud_count if fraud_count > 0 else 0
    }
    
    return metrics

def calculate_correlation_matrix(df, columns=None):
    """Calculate correlation matrix for specified columns"""
    if columns is None:
        # Use all numeric columns
        numeric_df = df.select_dtypes(include=[np.number])
    else:
        numeric_df = df[columns]
    
    corr_matrix = numeric_df.corr()
    
    return corr_matrix

def get_summary_statistics(df, column):
    """Get summary statistics for a column"""
    if column not in df.columns:
        return {}
    
    stats = {
        'count': len(df[column]),
        'mean': df[column].mean(),
        'median': df[column].median(),
        'std': df[column].std(),
        'min': df[column].min(),
        'max': df[column].max(),
        'q25': df[column].quantile(0.25),
        'q75': df[column].quantile(0.75),
        'skewness': df[column].skew(),
        'kurtosis': df[column].kurtosis()
    }
    
    return stats

def detect_outliers_iqr(df, column, multiplier=1.5):
    """Detect outliers using IQR method"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - multiplier * IQR
    upper_bound = Q3 + multiplier * IQR
    
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    
    return outliers, lower_bound, upper_bound
