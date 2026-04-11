import sqlite3
import pandas as pd
from datetime import datetime
import streamlit as st

DB_PATH = 'krisan.db'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Table Harvest Summary
    c.execute('''
        CREATE TABLE IF NOT EXISTS harvest_summary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT,
            house TEXT,
            tangkai INTEGER,
            grade_a_pct REAL,
            pendapatan INTEGER,
            putih INTEGER,
            pink INTEGER,
            kuning INTEGER
        )
    ''')
    
    # Table Harvest Details
    c.execute('''
        CREATE TABLE IF NOT EXISTS harvest_details (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary_id INTEGER,
            tanggal TEXT,
            house TEXT,
            varietas TEXT,
            grade TEXT,
            tipe TEXT,
            ukuran TEXT,
            jml_ikat INTEGER,
            isi_per_ikat INTEGER,
            total_batang INTEGER,
            harga_per_ikat INTEGER,
            harga_per_batang REAL,
            total_pendapatan INTEGER,
            FOREIGN KEY (summary_id) REFERENCES harvest_summary(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def save_harvest_record(summary_data, details_df):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        # 1. Insert Summary
        c.execute('''
            INSERT INTO harvest_summary (tanggal, house, tangkai, grade_a_pct, pendapatan, putih, pink, kuning)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            summary_data['Tanggal'],
            summary_data['House'],
            summary_data['Tangkai'],
            summary_data['Grade A %'],
            summary_data['Pendapatan'],
            summary_data['Putih'],
            summary_data['Pink'],
            summary_data['Kuning']
        ))
        
        summary_id = c.lastrowid
        
        # 2. Insert Details
        if not details_df.empty:
            # Add summary_id to details
            details_records = details_df.to_dict('records')
            for record in details_records:
                c.execute('''
                    INSERT INTO harvest_details (
                        summary_id, tanggal, house, varietas, grade, tipe, ukuran, 
                        jml_ikat, isi_per_ikat, total_batang, harga_per_ikat, 
                        harga_per_batang, total_pendapatan
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    summary_id,
                    record['Tanggal'],
                    record['House'],
                    record['Varietas'],
                    record['Grade'],
                    record['Tipe'],
                    record['Ukuran'],
                    record['Jml_Ikat'],
                    record['Isi_per_Ikat'],
                    record['Total_Batang'],
                    record['Harga_per_Ikat'],
                    record['Harga_per_Batang'],
                    record['Total_Pendapatan']
                ))
        
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Database Error: {e}")
        return False
    finally:
        conn.close()

def get_harvest_summary():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM harvest_summary ORDER BY tanggal DESC, id DESC", conn)
        return df.to_dict('records') # Convert to list of dicts to match session_state format
    except:
        return []
    finally:
        conn.close()

def get_harvest_details():
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM harvest_details ORDER BY tanggal DESC", conn)
        # Drop summary_id and id for display cleanliness if needed, or keep them
        return df.to_dict('records')
    except:
        return []
    finally:
        conn.close()

def clear_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM harvest_details")
    c.execute("DELETE FROM harvest_summary")
    conn.commit()
    conn.close()
