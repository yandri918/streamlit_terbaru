# Panduan Download Dataset Harian untuk AgriSensa
## Data Curah Hujan (BMKG) & Harga Pangan (BAPANAS)

---

## 📊 BAGIAN 1: DATA CURAH HUJAN HARIAN (BMKG)

### **Sumber:** `https://dataonline.bmkg.go.id`

### **Langkah-langkah Download:**

#### 1. **Registrasi Akun (Gratis)**
- Buka: https://dataonline.bmkg.go.id
- Klik "**Daftar Sekarang**"
- Isi form registrasi (nama, email, institusi, dll)
- Verifikasi email
- Login dengan akun yang sudah dibuat

#### 2. **Pilih Data Iklim Harian**
- Setelah login, pilih menu "**Data Iklim**"
- Pilih "**Data Iklim Harian**" (bukan bulanan)
- Pilih jenis stasiun: **UPT (Unit Pelaksana Teknis)**

#### 3. **Pilih Lokasi Stasiun**
Untuk area **Banyumas/Purwokerto**, pilih stasiun terdekat:
- **Stasiun Cilacap** (paling dekat dengan Banyumas)
- Atau **Stasiun Purwokerto** (jika tersedia)
- Atau **Stasiun Semarang** (alternatif)

**Cara memilih:**
- Klik peta atau dropdown "Provinsi" → Pilih **Jawa Tengah**
- Pilih stasiun dari daftar
- Centang parameter yang dibutuhkan:
  - ✅ **Curah Hujan (RR)**
  - ✅ **Hari Hujan**
  - ✅ **Suhu Rata-rata (Tavg)**
  - ✅ **Kelembaban (RH_avg)**

#### 4. **Pilih Periode Waktu**
⚠️ **PENTING**: BMKG hanya bisa download **per bulan**, jadi harus diulang 36 kali untuk 3 tahun!

**Contoh untuk Januari 2022:**
- Tanggal Mulai: `01/01/2022`
- Tanggal Akhir: `31/01/2022`
- Klik "**Proses**" atau "**Kirim**"

#### 5. **Download File**
- Setelah proses selesai, klik "**Download**"
- File akan terdownload dalam format **Excel (.xlsx)**
- Isi kuesioner singkat (jika diminta)
- Simpan file dengan nama: `curah_hujan_2022_01.xlsx`

#### 6. **Ulangi untuk Semua Bulan**
Ulangi langkah 4-5 untuk:
- **2022**: Januari - Desember (12 file)
- **2023**: Januari - Desember (12 file)
- **2024**: Januari - Desember (12 file)
- **Total**: 36 file Excel

#### 7. **Gabungkan Semua File**
Setelah download semua, gabungkan menjadi 1 file CSV:

**Cara Manual (Excel):**
1. Buka semua file Excel
2. Copy-paste semua data ke 1 sheet
3. Save As → CSV (Comma delimited)
4. Simpan sebagai: `curah_hujan_2022_2024.csv`

**Cara Otomatis (Python):**
Saya sudah buatkan script di bawah untuk merge otomatis!

---

## 💰 BAGIAN 2: DATA HARGA PANGAN HARIAN (BAPANAS)

### **Sumber:** `https://panelharga.badanpangan.go.id` atau `https://data.badanpangan.go.id`

### **Langkah-langkah Download:**

#### **Opsi A: Via Panel Harga Pangan (Lebih Mudah)**

1. **Buka Panel Harga**
   - URL: https://panelharga.badanpangan.go.id
   - Tidak perlu login!

2. **Pilih Komoditas**
   - Pilih komoditas: **Cabai Merah Keriting** (atau yang lain)
   - Pilih tingkat: **Konsumen** (harga eceran)

3. **Pilih Periode**
   - Tahun Awal: **2022**
   - Tahun Akhir: **2024**
   - Periode Tanggal: Pilih rentang (misal: 01/01/2022 - 31/12/2024)

4. **Download Data**
   - Cari tombol "**Download**" atau "**Export CSV**"
   - Jika tidak ada tombol download, gunakan **Opsi B** di bawah

#### **Opsi B: Via Portal Data BAPANAS (Lebih Lengkap)**

1. **Buka Portal Data**
   - URL: https://data.badanpangan.go.id
   - Cari bagian "**Dataset Publikasi**"

2. **Cari Dataset Harga Harian**
   - Cari dataset dengan nama seperti:
     - "Harga Pangan Harian 2022"
     - "Harga Pangan Harian 2023"
     - "Harga Pangan Harian 2024"

3. **Download CSV**
   - Klik dataset yang diinginkan
   - Pilih format: **CSV** (bukan JSON atau XLSX)
   - Klik "**Download**"

4. **Gabungkan File**
   - Jika download terpisah per tahun, gabungkan menjadi 1 file
   - Simpan sebagai: `harga_bapanas_2022_2024.csv`

#### **Opsi C: Via API BAPANAS (Paling Canggih)**

Gunakan script Python yang sudah saya buat di `1_fetch_bapanas_historical.py`!

**Keuntungan:**
- ✅ Otomatis
- ✅ Selalu update
- ✅ Bisa dijadwalkan (cron job)

**Kekurangan:**
- ⚠️ API hanya return data terbaru (bukan historical 3 tahun)
- ⚠️ Perlu setup daily scraping untuk build historical data

---

## 🔧 SCRIPT OTOMATIS: MERGE FILE BMKG

Simpan script ini sebagai `merge_bmkg_files.py`:

```python
import pandas as pd
import glob
import os

# Path ke folder yang berisi file Excel BMKG
bmkg_folder = "data/raw/bmkg_downloads/"

# Cari semua file Excel
excel_files = glob.glob(os.path.join(bmkg_folder, "*.xlsx"))

print(f"Found {len(excel_files)} Excel files")

# List untuk menyimpan semua dataframe
all_data = []

for file in excel_files:
    print(f"Processing: {file}")
    try:
        df = pd.read_excel(file)
        all_data.append(df)
    except Exception as e:
        print(f"Error reading {file}: {e}")

# Gabungkan semua dataframe
merged_df = pd.concat(all_data, ignore_index=True)

# Rename kolom (sesuaikan dengan nama kolom di file BMKG)
# Contoh kolom BMKG: Tanggal, RR (curah hujan), Tavg (suhu), RH_avg (kelembaban)
merged_df = merged_df.rename(columns={
    'Tanggal': 'date',
    'RR': 'curah_hujan_mm',
    'Tavg': 'suhu_rata_c',
    'RH_avg': 'kelembaban_persen'
})

# Convert tanggal ke datetime
merged_df['date'] = pd.to_datetime(merged_df['date'])

# Extract year dan month
merged_df['year'] = merged_df['date'].dt.year
merged_df['month'] = merged_df['date'].dt.month

# Sort by date
merged_df = merged_df.sort_values('date')

# Save to CSV
output_file = "data/raw/curah_hujan_2022_2024.csv"
merged_df.to_csv(output_file, index=False)

print(f"\n✅ Merged {len(merged_df)} records")
print(f"💾 Saved to: {output_file}")
print(f"📅 Date range: {merged_df['date'].min()} to {merged_df['date'].max()}")
```

**Cara pakai:**
```bash
# 1. Letakkan semua file Excel BMKG di folder: data/raw/bmkg_downloads/
# 2. Jalankan script:
python merge_bmkg_files.py
```

---

## 📝 CHECKLIST DOWNLOAD

### **Data BMKG (Curah Hujan)**
- [ ] Registrasi akun di dataonline.bmkg.go.id
- [ ] Download data Januari 2022
- [ ] Download data Februari 2022
- [ ] ... (ulangi untuk 36 bulan)
- [ ] Gabungkan semua file menjadi `curah_hujan_2022_2024.csv`
- [ ] Simpan di: `data/raw/curah_hujan_2022_2024.csv`

### **Data BAPANAS (Harga Pangan)**
- [ ] Buka panelharga.badanpangan.go.id atau data.badanpangan.go.id
- [ ] Download data harga 2022-2024 (CSV)
- [ ] Simpan di: `data/raw/harga_bapanas_2022_2024.csv`

### **Jalankan Pipeline**
- [ ] Run: `python data_analysis/scripts/2_merge_weather_price.py`
- [ ] Run: `python data_analysis/scripts/3_exploratory_analysis.py`
- [ ] Review visualizations di: `data/processed/visualizations/`

---

## 🚨 TROUBLESHOOTING

### **Problem: BMKG download terlalu lama (36 file!)**
**Solusi:**
- Download hanya 1 tahun dulu (2024) untuk testing
- Atau gunakan sample data yang sudah saya generate

### **Problem: BAPANAS tidak ada tombol download**
**Solusi:**
- Gunakan API yang sudah ada di AgriSensa (`BapanasService`)
- Atau screenshot data dan manual input (tidak recommended)

### **Problem: Format file BMKG berbeda**
**Solusi:**
- Cek nama kolom di file Excel
- Update script `merge_bmkg_files.py` sesuai nama kolom yang benar

---

## 💡 TIPS

1. **Mulai dari yang kecil**: Download 1 bulan dulu untuk testing
2. **Gunakan script otomatis**: Jangan manual copy-paste 36 file!
3. **Backup data**: Simpan file original sebelum merge
4. **Validasi data**: Cek apakah ada missing values atau outliers

---

## 📞 KONTAK SUPPORT

**BMKG Data Online:**
- Email: dataonline@bmkg.go.id
- Telp: (021) 196, (021) 4246703

**BAPANAS:**
- Website: badanpangan.go.id
- Email: (cek di website)

---

**Good luck, Pak! Kalau ada kendala, kabari saya!** 🚀
