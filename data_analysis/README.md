# AgriSensa Seasonal Prediction Data Pipeline

## 📊 Overview
Pipeline untuk mengumpulkan dan menganalisis data curah hujan & harga komoditi 3 tahun terakhir (2022-2024) untuk membangun model prediksi musiman.

## 🎯 Tujuan
1. **Seasonal Pest & Disease Risk Model**: Prediksi outbreak hama/penyakit berdasarkan pola musim
2. **Price Prediction Model**: Prediksi harga komoditi berdasarkan musim + supply-demand
3. **Optimal Planting Calendar**: Rekomendasi kapan tanam untuk maximize profit & minimize risk

## 📁 Struktur File

```
data_analysis/
├── README.md                          # File ini
├── scripts/
│   ├── 1_fetch_bapanas_historical.py  # Pull data harga BAPANAS 2022-2024
│   ├── 2_merge_weather_price.py       # Gabungkan curah hujan + harga
│   └── 3_exploratory_analysis.py      # EDA & visualisasi pola
├── data/
│   ├── raw/
│   │   ├── curah_hujan_2022_2024.csv  # Data BMKG (manual download)
│   │   └── harga_bapanas_raw/         # Data BAPANAS per komoditas
│   ├── processed/
│   │   └── dataset_training.csv       # Dataset gabungan siap ML
│   └── models/
│       └── seasonal_risk_model.pkl    # Model trained
└── notebooks/
    └── seasonal_analysis.ipynb        # Jupyter notebook untuk EDA
```

## 🚀 Quick Start

### Step 1: Download Data Curah Hujan (Manual)
1. Buka: https://dataonline.bmkg.go.id/home
2. Register akun (gratis)
3. Pilih stasiun: **Cilacap** atau **Purwokerto** (terdekat dengan Banyumas)
4. Download: Curah Hujan Bulanan **2022-2024**
5. Save ke: `data/raw/curah_hujan_2022_2024.csv`

### Step 2: Fetch Data Harga BAPANAS (Otomatis)
```bash
cd data_analysis/scripts
python 1_fetch_bapanas_historical.py
```

### Step 3: Merge Data
```bash
python 2_merge_weather_price.py
```

### Step 4: Exploratory Analysis
```bash
python 3_exploratory_analysis.py
```

## 📊 Output yang Dihasilkan

1. **Dataset Training** (`data/processed/dataset_training.csv`):
   - Kolom: Bulan, Tahun, Curah Hujan, Suhu, Harga Cabai, Harga Bawang, dll
   - Siap untuk training ML model

2. **Visualisasi Pola**:
   - Grafik curah hujan vs harga per bulan
   - Heatmap korelasi
   - Seasonal decomposition

3. **Insight Report**:
   - Pola musim kemarau vs hujan
   - Identifikasi bulan "double trouble" (hama + jamur)
   - Analisis faktor Nataru

## 🔧 Dependencies

```bash
pip install pandas numpy matplotlib seaborn plotly requests
```

## 📝 Notes

- Data BMKG harus download manual (tidak ada public API untuk historical data)
- Data BAPANAS bisa otomatis via API yang sudah ada di AgriSensa
- Untuk data outbreak hama, perlu request ke Dinas Pertanian Banyumas

## 👤 Author
Yandri - AgriSensa Platform
