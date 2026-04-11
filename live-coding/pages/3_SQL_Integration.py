import streamlit as st
import duckdb
import pandas as pd

st.set_page_config(page_title="SQL Integration", page_icon="💾", layout="wide")

st.markdown("# 💾 SQL Integration with DuckDB")
st.markdown("### Eksekusi Query SQL Langsung (Bahasa Indonesia)")
st.markdown("Modul ini menggunakan **DuckDB** (database OLAP cepat) untuk melatih kemampuan SQL Anda dari dasar hingga Window Functions.")

with st.sidebar:
    st.header("📚 Referensi Belajar")
    st.markdown("""
    **Dokumentasi:**
    - [DuckDB SQL Introduction](https://duckdb.org/docs/sql/introduction)
    - [PostgreSQL Tutorial (Mode Analytics)](https://mode.com/sql-tutorial/)
    
    **Video Tutorial (YouTube):**
    - [Alex The Analyst - SQL Portfolio](https://www.youtube.com/watch?v=7PWEgYx9xqM)
    - [Advanced SQL Window Functions](https://www.youtube.com/watch?v=Ww71knvhQ-s)
    """)

# Setup Sandbox Database
@st.cache_resource
def get_connection():
    con = duckdb.connect(database=':memory:')
    # Create sample tables
    con.execute("CREATE TABLE employees (id INTEGER, name VARCHAR, department VARCHAR, salary INTEGER)")
    con.execute("INSERT INTO employees VALUES (1, 'Alice', 'HR', 60000), (2, 'Bob', 'Engineering', 120000), (3, 'Charlie', 'Engineering', 130000), (4, 'David', 'HR', 65000), (5, 'Eve', 'Marketing', 90000), (6, 'Frank', 'Marketing', 85000)")
    
    con.execute("CREATE TABLE sales (id INTEGER, employee_id INTEGER, amount INTEGER, date DATE)")
    con.execute("INSERT INTO sales VALUES (1, 2, 500, '2023-01-01'), (2, 2, 700, '2023-01-02'), (3, 3, 200, '2023-01-01'), (4, 5, 1000, '2023-01-05'), (5, 5, 500, '2023-01-06')")
    return con

con = get_connection()

# Sidebar Schema
st.sidebar.markdown("### 🗄️ Skema Database")
st.sidebar.markdown("**Tabel `employees`**")
st.sidebar.text("- id (INT)\n- name (VARCHAR)\n- department (VARCHAR)\n- salary (INT)")
st.sidebar.markdown("---")
st.sidebar.markdown("**Tabel `sales`**")
st.sidebar.text("- id (INT)\n- employee_id (INT)\n- amount (INT)\n- date (DATE)")

tab1, tab2, tab3 = st.tabs(["🟢 Basic Selects", "🟡 Joins & Aggregates", "🔴 Advanced Window Functions"])

# --- BEGINNER ---
with tab1:
    st.header("🟢 Level Pemula: Select & Filtering")
    
    st.markdown("""
    ### 📚 Materi Singkat
    Perintah dasar SQL meliputi:
    1.  `SELECT`: Memilih kolom.
    2.  `FROM`: Memilih tabel.
    3.  `WHERE`: Memfilter baris berdasarkan kondisi.
    4.  `ORDER BY`: Mengurutkan hasil.
    """)
    
    st.subheader("📝 Soal: Gaji Tinggi di Engineering")
    st.markdown("""
    **Tugas**:
    Tampilkan semua data karyawan yang bekerja di departemen **'Engineering'** DAN memiliki gaji diatas **125,000**.
    """)
    
    query_beg = st.text_area("Tulis Query SQL Anda:", "SELECT * FROM employees WHERE ...", key="sql_beg")
    
    if st.button("Jalankan Query", key="btn_beg"):
        try:
            result = con.execute(query_beg).df()
            st.write("Hasil Query:")
            st.dataframe(result)
            
            # Simple validation idea: check consistency
            if len(result) == 1 and result.iloc[0]['name'] == 'Charlie':
                st.success("✅ Benar! Hanya Charlie yang memenuhi kriteria.")
                st.balloons()
            else:
                st.warning("⚠️ Hasil belum tepat. Coba cek kondisi WHERE Anda.")
        except Exception as e:
            st.error(f"SQL Error: {e}")
            
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Jawaban**:
        ```sql
        SELECT * 
        FROM employees 
        WHERE department = 'Engineering' 
          AND salary > 125000;
        ```
        **Penjelasan**:
        -   `department = 'Engineering'`: Memilih hanya anak teknik.
        -   `AND`: Kedua syarat harus terpenuhi.
        -   `salary > 125000`: Batas gaji.
        """)
        
# --- INTERMEDIATE ---
with tab2:
    st.header("🟡 Level Menengah: Joins & Aggregates")
    
    st.markdown("""
    ### 📚 Materi Singkat
    1.  **JOIN**: Menggabungkan dua tabel berdasarkan kolom kunci (Key).
        -   `INNER JOIN`: Hanya baris yang cocok di kedua tabel.
        -   `LEFT JOIN`: Semua baris dari tabel kiri, dan yang cocok dari kanan.
    2.  **GROUP BY**: Mengelompokkan data untuk fungsi agregasi (`SUM`, `COUNT`, `AVG`).
    """)
    
    st.subheader("📝 Soal: Total Penjualan per Karyawan")
    st.markdown("""
    **Tugas**:
    Hitung **total penjualan** (`SUM(amount)`) untuk setiap karyawan yang memiliki penjualan. Tampilkan nama karyawan dan total penjualannya.
    """)
    
    query_int = st.text_area("Tulis Query SQL Anda:", """
SELECT e.name, ...
FROM employees e
JOIN sales s ON ...
...
    """, key="sql_int", height=150)
    
    if st.button("Jalankan Query", key="btn_int"):
        try:
            result = con.execute(query_int).df()
            st.write("Hasil Query:")
            st.dataframe(result)
            
            if 'total_sales' in result.columns or 'sum(amount)' in [c.lower() for c in result.columns]:
                st.success("✅ Query berhasil dijalankan.")
            else:
                st.warning("Pastikan Anda menghitung jumlah penjualan.")
        except Exception as e:
             st.error(f"SQL Error: {e}")

    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Jawaban**:
        ```sql
        SELECT 
            e.name, 
            SUM(s.amount) as total_sales
        FROM employees e
        JOIN sales s ON e.id = s.employee_id
        GROUP BY e.name;
        ```
        **Penjelasan**:
        -   `JOIN`: Menghubungkan karyawan dengan penjualan mereka lewat `e.id = s.employee_id`.
        -   `GROUP BY e.name`: Wajib dilakukan karena kita menggunakan fungsi agregasi `SUM()`. Kita ingin satu baris per nama.
        """)

# --- ADVANCED ---
with tab3:
    st.header("🔴 Level Mahir: Window Functions")
    
    st.markdown("""
    ### 📚 Materi Singkat
    **Window Functions** melakukan perhitungan pada sekumpulan baris yang terkait dengan baris saat ini.
    -   Sintaks: `FUNGSI() OVER (PARTITION BY ... ORDER BY ...)`
    -   `RANK()`: Ranking dengan loncat (1, 2, 2, 4).
    -   `DENSE_RANK()`: Ranking tanpa loncat (1, 2, 2, 3).
    -   `ROW_NUMBER()`: Nomor unik baris (1, 2, 3, 4).
    """)
    
    st.subheader("📝 Soal: Ranking Gaji per Departemen")
    st.markdown("""
    **Tugas**:
    Berikan ranking gaji untuk setiap karyawan **di dalam departemennya masing-masing**. Gaji tertinggi dapat ranking 1.
    Gunakan `DENSE_RANK()`.
    """)
    
    query_adv = st.text_area("Tulis Query SQL Anda:", """
SELECT 
    name, 
    department, 
    salary,
    ... OVER (...) as raking_gaji
FROM employees
    """, key="sql_adv", height=150)
    
    if st.button("Jalankan Query", key="btn_adv"):
        try:
            result = con.execute(query_adv).df()
            st.write("Hasil Query:")
            st.dataframe(result)
        except Exception as e:
            st.error(f"SQL Error: {e}")
            
    with st.expander("💡 Lihat Penjelasan & Jawaban"):
        st.markdown("""
        **Jawaban**:
        ```sql
        SELECT 
            name, 
            department, 
            salary,
            DENSE_RANK() OVER (
                PARTITION BY department 
                ORDER BY salary DESC
            ) as ranking_gaji
        FROM employees;
        ```
        **Penjelasan**:
        -   `PARTITION BY department`: Ranking direset untuk setiap departemen (HR sendiri, Engineering sendiri).
        -   `ORDER BY salary DESC`: Gaji tertinggi di atas (Rank 1).
        -   `DENSE_RANK()`: Jika ada gaji sama, rankingnya sama, dan ranking berikutnya tidak loncat angka.
        """)
