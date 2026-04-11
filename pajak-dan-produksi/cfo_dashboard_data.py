# CFO Dashboard - Data Generation and Helper Functions

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sqlite3

# ============================================================================
# OPTION 1: Load from Audit Trail
# ============================================================================

def load_from_audit_trail():
    """Load real data from audit trail CSV"""
    audit_file = "audit_logs/tax_calculations.csv"
    
    if not os.path.exists(audit_file):
        return None
    
    try:
        df = pd.read_csv(audit_file)
        
        # Parse timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Extract month
        df['month'] = df['timestamp'].dt.to_period('M').dt.to_timestamp()
        
        # Parse output_data JSON to extract tax amounts
        import json
        
        tax_data = []
        for _, row in df.iterrows():
            try:
                output = json.loads(row['output_data'])
                
                # Determine tax amount based on tax_type
                amount = 0
                if row['tax_type'] == 'PPh 21':
                    amount = output.get('pajak_bulanan', 0)
                elif row['tax_type'] == 'PPh 23':
                    amount = output.get('pph23', 0)
                elif row['tax_type'] == 'PPN':
                    amount = output.get('ppn', 0)
                elif row['tax_type'] == 'PPh Badan':
                    amount = output.get('pph_badan', 0)
                elif row['tax_type'] == 'PBB':
                    amount = output.get('pbb', 0)
                elif row['tax_type'] == 'PKB':
                    amount = output.get('total', 0)
                elif row['tax_type'] == 'BPHTB':
                    amount = output.get('bphtb', 0)
                
                tax_data.append({
                    'month': row['month'],
                    'tax_type': row['tax_type'],
                    'amount': amount
                })
            except:
                continue
        
        if not tax_data:
            return None
        
        return pd.DataFrame(tax_data)
    
    except Exception as e:
        print(f"Error loading audit trail: {e}")
        return None

# ============================================================================
# OPTION 2: Load from Database
# ============================================================================

def load_from_database(db_path="tax_data.db"):
    """Load real data from SQLite database"""
    
    if not os.path.exists(db_path):
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        
        # Query tax calculations
        query = """
        SELECT 
            datetime(timestamp) as timestamp,
            tax_type,
            amount
        FROM tax_calculations
        ORDER BY timestamp DESC
        """
        
        df = pd.read_sql_query(query, conn)
        conn.close()
        
        # Parse timestamp
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['month'] = df['timestamp'].dt.to_period('M').dt.to_timestamp()
        
        return df
    
    except Exception as e:
        print(f"Error loading from database: {e}")
        return None

# ============================================================================
# OPTION 3: Load from Uploaded File
# ============================================================================

def load_from_uploaded_file(uploaded_file):
    """Load data from uploaded Excel or CSV file"""
    
    if uploaded_file is None:
        return None
    
    try:
        # Determine file type
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:
            return None
        
        # Validate required columns
        required_columns = ['month', 'tax_type', 'amount']
        if not all(col in df.columns for col in required_columns):
            return None
        
        # Parse month
        df['month'] = pd.to_datetime(df['month'])
        
        return df
    
    except Exception as e:
        print(f"Error loading uploaded file: {e}")
        return None

# ============================================================================
# Data Processing Functions
# ============================================================================

def process_tax_data_for_dashboard(df):
    """Process raw tax data for dashboard visualizations"""
    
    if df is None or df.empty:
        return None
    
    # Aggregate by month and tax type
    aggregated = df.groupby(['month', 'tax_type'])['amount'].sum().reset_index()
    
    return aggregated

def calculate_pph21_trend(df):
    """Calculate PPh 21 trend with moving average"""
    
    if df is None or df.empty:
        return None
    
    # Filter PPh 21 data
    pph21_data = df[df['tax_type'] == 'PPh 21'].copy()
    
    if pph21_data.empty:
        return None
    
    # Aggregate by month
    monthly = pph21_data.groupby('month')['amount'].sum().reset_index()
    monthly.columns = ['month', 'pph21']
    
    # Sort by month
    monthly = monthly.sort_values('month')
    
    # Calculate moving average
    monthly['moving_avg'] = monthly['pph21'].rolling(window=3, min_periods=1).mean()
    
    return monthly

def calculate_pph_badan_quarterly(df):
    """Calculate PPh Badan quarterly data"""
    
    if df is None or df.empty:
        return None
    
    # Filter PPh Badan data
    pph_badan_data = df[df['tax_type'] == 'PPh Badan'].copy()
    
    if pph_badan_data.empty:
        return None
    
    # Extract quarter
    pph_badan_data['quarter'] = pph_badan_data['month'].dt.to_period('Q').astype(str)
    
    # Aggregate by quarter
    quarterly = pph_badan_data.groupby('quarter')['amount'].sum().reset_index()
    quarterly.columns = ['quarter', 'pph_badan']
    quarterly['scenario'] = 'Actual'
    
    return quarterly

# ============================================================================
# Sample Data Generation (Fallback)
# ============================================================================

def generate_sample_tax_data():
    """Generate sample tax data for the last 12 months"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    months = pd.date_range(start=start_date, end=end_date, freq='M')
    
    data = []
    for month in months:
        # PPh 21
        data.append({
            'month': month,
            'tax_type': 'PPh 21',
            'amount': np.random.randint(50000000, 100000000)
        })
        # PPh Badan
        data.append({
            'month': month,
            'tax_type': 'PPh Badan',
            'amount': np.random.randint(100000000, 200000000)
        })
        # PPN
        data.append({
            'month': month,
            'tax_type': 'PPN',
            'amount': np.random.randint(80000000, 150000000)
        })
        # Others
        data.append({
            'month': month,
            'tax_type': 'Lainnya',
            'amount': np.random.randint(20000000, 50000000)
        })
    
    return pd.DataFrame(data)

def generate_pph21_trend_data():
    """Generate PPh 21 trend data with moving average"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    months = pd.date_range(start=start_date, end=end_date, freq='M')
    
    base = 70000000
    data = []
    
    for i, month in enumerate(months):
        # Add trend and seasonality
        trend = base + (i * 2000000)
        seasonal = 10000000 * np.sin(i * np.pi / 6)
        noise = np.random.randint(-5000000, 5000000)
        amount = trend + seasonal + noise
        
        data.append({
            'month': month,
            'pph21': amount
        })
    
    df = pd.DataFrame(data)
    # Calculate moving average
    df['moving_avg'] = df['pph21'].rolling(window=3, min_periods=1).mean()
    
    return df

def generate_pph_badan_quarterly():
    """Generate PPh Badan quarterly data"""
    quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024']
    
    data = []
    for quarter in quarters:
        # UMKM
        data.append({
            'quarter': quarter,
            'scenario': 'UMKM (0.5%)',
            'pph_badan': np.random.randint(20000000, 40000000)
        })
        # Non-UMKM
        data.append({
            'quarter': quarter,
            'scenario': 'Non-UMKM (22%)',
            'pph_badan': np.random.randint(150000000, 250000000)
        })
    
    return pd.DataFrame(data)

def generate_5year_projection():
    """Generate 5-year tax projection with multiple scenarios"""
    years = list(range(2024, 2030))
    scenarios = ['Conservative', 'Moderate', 'Aggressive']
    growth_rates = {'Conservative': 0.05, 'Moderate': 0.10, 'Aggressive': 0.15}
    
    base_tax = 1200000000  # 1.2 Billion (current year)
    
    data = []
    for year in years:
        for scenario in scenarios:
            growth = growth_rates[scenario]
            years_from_base = year - 2024
            projected = base_tax * ((1 + growth) ** years_from_base)
            
            # Add some randomness
            if year > 2024:
                projected += np.random.randint(-50000000, 50000000)
            
            data.append({
                'year': str(year),
                'scenario': scenario,
                'projected_tax': projected,
                'type': 'Historical' if year == 2024 else 'Forecast'
            })
    
    return pd.DataFrame(data)

def generate_production_cost_data():
    """Generate production cost breakdown and trend data"""
    # Breakdown
    breakdown_data = [
        {'category': 'Bahan Baku', 'amount': 500000000, 'percentage': 50},
        {'category': 'Tenaga Kerja', 'amount': 300000000, 'percentage': 30},
        {'category': 'Overhead', 'amount': 150000000, 'percentage': 15},
        {'category': 'Lainnya', 'amount': 50000000, 'percentage': 5}
    ]
    
    # Trend
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    months = pd.date_range(start=start_date, end=end_date, freq='M')
    
    trend_data = []
    for month in months:
        for cat_data in breakdown_data:
            # Add some variation
            variation = np.random.uniform(0.9, 1.1)
            cost = cat_data['amount'] * variation / 12  # Monthly cost
            
            trend_data.append({
                'month': month,
                'category': cat_data['category'],
                'cost': cost
            })
    
    return pd.DataFrame(breakdown_data), pd.DataFrame(trend_data)
