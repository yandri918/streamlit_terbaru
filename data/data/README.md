# Data Files

## ⚠️ Important Note

The CSV data files are **NOT included** in this repository due to GitHub's 100 MB file size limit.

## 📥 How to Get the Data Files

### For Local Development

1. Download or copy the following files to this `data/` folder:
   - `stock_price.csv` - Stock market historical data
   - `creditcard.csv` - Credit card fraud detection dataset

2. Place them in this directory:
   ```
   data_analyst/data/
   ├── stock_price.csv
   └── creditcard.csv
   ```

### For Streamlit Cloud Deployment

Since the data files are too large for GitHub, you have several options:

#### Option 1: Use External Data Source (Recommended)
Upload your CSV files to a cloud storage service and load them via URL:
- Google Drive (with public link)
- Dropbox
- AWS S3
- GitHub Releases (supports larger files)

Then modify `utils/data_loader.py` to load from URL:
```python
df = pd.read_csv('https://your-storage-url/stock_price.csv')
```

#### Option 2: Use Sample Data
Create smaller sample datasets (< 100 MB) for demonstration purposes.

#### Option 3: Git LFS (Git Large File Storage)
If you need to include large files in Git:
```bash
git lfs install
git lfs track "*.csv"
git add .gitattributes
git add data/*.csv
git commit -m "Add large data files with LFS"
git push
```

Note: Git LFS has storage limits on free tier.

## 📊 Dataset Information

### stock_price.csv
- **Size:** ~2 MB
- **Records:** 1,500+ rows
- **Columns:** date, symbol, open_value, high_value, low_value, last_value, turnover

### creditcard.csv
- **Size:** ~143 MB
- **Records:** 284,807 rows
- **Columns:** Time, V1-V28 (PCA features), Amount, Class

## 🔗 Alternative: Public Datasets

You can also use publicly available datasets:
- **Stock Data:** Yahoo Finance, Alpha Vantage API
- **Credit Card Fraud:** [Kaggle Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)

---

**For questions, see the main [README.md](../README.md)**
