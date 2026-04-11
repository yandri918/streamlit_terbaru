import os
import csv
import json
import uuid
from datetime import datetime
import pandas as pd

# Directory for audit logs
AUDIT_DIR = "audit_logs"
AUDIT_FILE = os.path.join(AUDIT_DIR, "tax_calculations.csv")

# Ensure audit directory exists
os.makedirs(AUDIT_DIR, exist_ok=True)

def save_audit_log(calc_type, user_name, company_name, input_data, output_data):
    """
    Save audit log for tax calculation
    
    Args:
        calc_type (str): Type of calculation (PPh 21, PBB, etc)
        user_name (str): Name of user performing calculation
        company_name (str): Company name
        input_data (dict): Input parameters
        output_data (dict): Calculation results
    """
    try:
        # Generate session ID
        session_id = str(uuid.uuid4())[:8]
        
        # Get current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare log entry
        log_entry = {
            'timestamp': timestamp,
            'session_id': session_id,
            'user_name': user_name,
            'company_name': company_name,
            'calculation_type': calc_type,
            'input_data': json.dumps(input_data, ensure_ascii=False),
            'output_data': json.dumps(output_data, ensure_ascii=False)
        }
        
        # Check if file exists
        file_exists = os.path.isfile(AUDIT_FILE)
        
        # Write to CSV
        with open(AUDIT_FILE, 'a', newline='', encoding='utf-8') as f:
            fieldnames = ['timestamp', 'session_id', 'user_name', 'company_name', 
                         'calculation_type', 'input_data', 'output_data']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
            
            writer.writerow(log_entry)
        
        return True, session_id
    
    except Exception as e:
        print(f"Error saving audit log: {e}")
        return False, None

def load_audit_logs(limit=None):
    """
    Load audit logs from CSV file
    
    Args:
        limit (int): Maximum number of records to load (most recent)
    
    Returns:
        pandas.DataFrame: Audit logs
    """
    try:
        if not os.path.isfile(AUDIT_FILE):
            return pd.DataFrame()
        
        df = pd.read_csv(AUDIT_FILE, encoding='utf-8')
        
        # Sort by timestamp descending (most recent first)
        df = df.sort_values('timestamp', ascending=False)
        
        if limit:
            df = df.head(limit)
        
        return df
    
    except Exception as e:
        print(f"Error loading audit logs: {e}")
        return pd.DataFrame()

def export_audit_logs(start_date=None, end_date=None, calc_type=None, user_name=None):
    """
    Export filtered audit logs
    
    Args:
        start_date (str): Start date filter (YYYY-MM-DD)
        end_date (str): End date filter (YYYY-MM-DD)
        calc_type (str): Calculation type filter
        user_name (str): User name filter
    
    Returns:
        pandas.DataFrame: Filtered audit logs
    """
    try:
        df = load_audit_logs()
        
        if df.empty:
            return df
        
        # Apply filters
        if start_date:
            df = df[df['timestamp'] >= start_date]
        
        if end_date:
            df = df[df['timestamp'] <= end_date + ' 23:59:59']
        
        if calc_type and calc_type != "Semua":
            df = df[df['calculation_type'] == calc_type]
        
        if user_name:
            df = df[df['user_name'].str.contains(user_name, case=False, na=False)]
        
        return df
    
    except Exception as e:
        print(f"Error exporting audit logs: {e}")
        return pd.DataFrame()

def get_audit_summary():
    """
    Get summary statistics of audit logs
    
    Returns:
        dict: Summary statistics
    """
    try:
        df = load_audit_logs()
        
        if df.empty:
            return {
                'total_calculations': 0,
                'unique_users': 0,
                'unique_companies': 0,
                'calculations_by_type': {},
                'recent_activity': []
            }
        
        summary = {
            'total_calculations': len(df),
            'unique_users': df['user_name'].nunique(),
            'unique_companies': df['company_name'].nunique(),
            'calculations_by_type': df['calculation_type'].value_counts().to_dict(),
            'recent_activity': df.head(5)[['timestamp', 'user_name', 'calculation_type']].to_dict('records')
        }
        
        return summary
    
    except Exception as e:
        print(f"Error getting audit summary: {e}")
        return {
            'total_calculations': 0,
            'unique_users': 0,
            'unique_companies': 0,
            'calculations_by_type': {},
            'recent_activity': []
        }

def get_calculation_details(session_id):
    """
    Get detailed information for a specific calculation
    
    Args:
        session_id (str): Session ID of the calculation
    
    Returns:
        dict: Calculation details
    """
    try:
        df = load_audit_logs()
        
        if df.empty:
            return None
        
        record = df[df['session_id'] == session_id]
        
        if record.empty:
            return None
        
        record = record.iloc[0]
        
        return {
            'timestamp': record['timestamp'],
            'session_id': record['session_id'],
            'user_name': record['user_name'],
            'company_name': record['company_name'],
            'calculation_type': record['calculation_type'],
            'input_data': json.loads(record['input_data']),
            'output_data': json.loads(record['output_data'])
        }
    
    except Exception as e:
        print(f"Error getting calculation details: {e}")
        return None
