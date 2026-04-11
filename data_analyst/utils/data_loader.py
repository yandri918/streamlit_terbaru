"""
Data loading utilities for the data analyst portfolio
"""
import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_stock_data():
    """Load stock price data with caching"""
    try:
        # Try to load from data_analyst/data folder first
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'stock_price.csv')
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
        else:
            # Fallback to parent directory
            parent_path = os.path.join(os.path.dirname(__file__), '..', '..', 'stock_price.csv')
            if os.path.exists(parent_path):
                df = pd.read_csv(parent_path)
            else:
                # Generate sample data for demonstration
                st.info("📊 **Using Sample Stock Data**")
                st.caption("The actual CSV file is not included in the repository. Displaying generated sample data for demonstration purposes.")
                
                import numpy as np
                from datetime import datetime, timedelta
                
                # Generate 500 days of sample stock data
                num_days = 500
                start_date = datetime(2023, 1, 1)
                dates = [start_date + timedelta(days=i) for i in range(num_days)]
                
                # Generate realistic stock prices with trend and volatility
                np.random.seed(42)
                base_price = 100
                trend = np.linspace(0, 20, num_days)  # Upward trend
                volatility = np.random.randn(num_days) * 2
                prices = base_price + trend + np.cumsum(volatility)
                
                # Generate OHLC data
                df = pd.DataFrame({
                    'date': dates,
                    'symbol': ['SAMPLE'] * num_days,
                    'mic': ['XNAS'] * num_days,
                    'open_value': prices + np.random.randn(num_days) * 0.5,
                    'high_value': prices + abs(np.random.randn(num_days)) * 1.5,
                    'low_value': prices - abs(np.random.randn(num_days)) * 1.5,
                    'last_value': prices,
                    'turnover': np.random.randint(1000000, 10000000, num_days)
                })
                
                # Ensure high >= open, close, low and low <= open, close, high
                df['high_value'] = df[['open_value', 'high_value', 'last_value']].max(axis=1)
                df['low_value'] = df[['open_value', 'low_value', 'last_value']].min(axis=1)
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        df = df.sort_values('date')
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading stock data: {e}")
        st.info("💡 Check that the CSV file exists and is properly formatted.")
        return None

@st.cache_data
def load_credit_card_data(sample_size=50000):
    """
    Load credit card fraud data with sampling for performance
    
    Args:
        sample_size: Number of rows to sample (default 50000)
    """
    try:
        # Try to load from data_analyst/data folder first
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'creditcard.csv')
        if os.path.exists(data_path):
            # For large files, use chunksize and sample
            df = pd.read_csv(data_path, nrows=sample_size)
        else:
            # Fallback to parent directory
            parent_path = os.path.join(os.path.dirname(__file__), '..', '..', 'creditcard.csv')
            if os.path.exists(parent_path):
                df = pd.read_csv(parent_path, nrows=sample_size)
            else:
                # Generate sample fraud data for demonstration
                st.info("📊 **Using Sample Credit Card Fraud Data**")
                st.caption("The actual CSV file (143.84 MB) is not included in the repository. Displaying generated sample data for demonstration purposes.")
                
                import numpy as np
                
                # Generate sample data with realistic fraud patterns
                np.random.seed(42)
                n_samples = min(sample_size, 10000)  # Limit for performance
                
                # Generate PCA features (V1-V28)
                pca_features = {}
                for i in range(1, 29):
                    pca_features[f'V{i}'] = np.random.randn(n_samples)
                
                # Generate Time (seconds elapsed)
                time_values = np.sort(np.random.randint(0, 172800, n_samples))  # 48 hours
                
                # Generate Amount with realistic distribution
                # Most transactions are small, few are large
                amounts = np.random.lognormal(3, 1.5, n_samples)
                amounts = np.clip(amounts, 0, 5000)  # Cap at $5000
                
                # Generate Class (0 = legitimate, 1 = fraud)
                # Create imbalanced dataset (~0.17% fraud rate)
                fraud_rate = 0.0017
                n_fraud = int(n_samples * fraud_rate)
                classes = np.array([0] * (n_samples - n_fraud) + [1] * n_fraud)
                np.random.shuffle(classes)
                
                # Make fraud transactions have different patterns
                fraud_mask = classes == 1
                
                # Fraud transactions tend to have:
                # - Higher amounts on average
                amounts[fraud_mask] = amounts[fraud_mask] * 1.5
                
                # - Different PCA patterns (modify some V features)
                for i in [1, 3, 4, 10, 12, 14, 17]:
                    pca_features[f'V{i}'][fraud_mask] += np.random.randn(fraud_mask.sum()) * 2
                
                # Create DataFrame
                df = pd.DataFrame({
                    'Time': time_values,
                    **pca_features,
                    'Amount': amounts,
                    'Class': classes
                })
        
        return df
    except Exception as e:
        st.error(f"❌ Error loading credit card data: {e}")
        st.info("💡 Check that the CSV file exists and has the correct format.")
        return None

def get_data_info(df):
    """Get basic information about the dataset"""
    if df is None:
        return None
    
    info = {
        'rows': len(df),
        'columns': len(df.columns),
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2,  # MB
        'missing_values': df.isnull().sum().sum(),
        'dtypes': df.dtypes.value_counts().to_dict()
    }
    
    return info

def preprocess_stock_data(df):
    """Preprocess stock data for analysis"""
    if df is None:
        return None
    
    # Calculate additional metrics
    df['daily_return'] = df['last_value'].pct_change()
    df['price_range'] = df['high_value'] - df['low_value']
    df['price_change'] = df['last_value'] - df['open_value']
    
    # Calculate moving averages
    df['ma_7'] = df['last_value'].rolling(window=7).mean()
    df['ma_30'] = df['last_value'].rolling(window=30).mean()
    
    # Calculate volatility (rolling standard deviation)
    df['volatility'] = df['daily_return'].rolling(window=30).std()
    
    return df

def preprocess_fraud_data(df):
    """Preprocess credit card fraud data"""
    if df is None:
        return None
    
    # Add hour of day from Time column
    df['Hour'] = (df['Time'] / 3600) % 24
    
    # Create bins for amount
    df['Amount_Bin'] = pd.cut(df['Amount'], 
                               bins=[0, 10, 50, 100, 500, float('inf')],
                               labels=['0-10', '10-50', '50-100', '100-500', '500+'])
    
    return df
