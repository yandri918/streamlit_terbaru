# 📊 Data Analyst Portfolio

Portfolio website profesional untuk menampilkan proyek-proyek analisis data menggunakan Streamlit dan Altair.

## 🎯 Featured Projects

### 1. 📈 Stock Price Analysis
Analisis mendalam terhadap data harga saham dengan visualisasi interaktif:
- Candlestick charts (OHLC)
- Moving averages (7-day & 30-day)
- Volume analysis
- Volatility tracking
- Returns distribution
- Statistical insights

### 2. 🔍 Credit Card Fraud Detection
Analisis pola fraud pada transaksi kartu kredit:
- Class imbalance analysis
- Transaction amount patterns
- Time-based fraud patterns
- PCA feature visualization
- Feature correlation analysis
- ML insights and metrics

## 🛠️ Tech Stack

- **Framework:** Streamlit
- **Visualization:** Altair
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Language:** Python 3.8+

## 📦 Installation

1. Clone repository:
```bash
git clone https://github.com/yandri918/data_analyst.git
cd data_analyst
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run Home.py
```

## 📁 Project Structure

```
data_analyst/
├── Home.py                          # Landing page
├── pages/
│   ├── 01_📈_Stock_Price_Analysis.py
│   └── 02_🔍_Credit_Card_Fraud.py
├── utils/
│   ├── data_loader.py              # Data loading utilities
│   ├── chart_builder.py            # Altair chart templates
│   └── metrics.py                  # Statistical calculations
├── data/
│   ├── stock_price.csv
│   └── creditcard.csv
├── .streamlit/
│   └── config.toml                 # Streamlit configuration
└── requirements.txt
```

## 📊 Datasets

### Stock Price Data
- **Source:** Historical stock market data
- **Records:** 1,500+ data points
- **Features:** Date, Open, High, Low, Close, Volume

### Credit Card Fraud Data
- **Source:** Credit card transactions
- **Records:** 284,000+ transactions
- **Features:** PCA-transformed features (V1-V28), Amount, Time, Class

## 🚀 Features

- **Interactive Visualizations:** All charts are interactive using Altair
- **Real-time Filtering:** Dynamic data filtering and exploration
- **Statistical Analysis:** Comprehensive statistical metrics
- **Responsive Design:** Works on desktop and mobile
- **Professional UI:** Modern, clean interface with custom styling

## 📈 Key Insights

### Stock Analysis
- Moving average crossover signals
- Volatility patterns
- Volume-price relationships
- Daily returns distribution

### Fraud Detection
- Class imbalance handling
- Fraud pattern identification
- Feature importance analysis
- Time-based fraud trends

## 🎨 Design Philosophy

- **Clean & Modern:** Professional design with gradient accents
- **Interactive:** All visualizations support zooming, panning, and tooltips
- **Informative:** Clear metrics and insights throughout
- **User-Friendly:** Intuitive navigation and filtering

## 📝 License

This project is licensed under the MIT License.

## 👤 Author

**Yandri**
- GitHub: [@yandri918](https://github.com/yandri918)
- Portfolio: [Data Analyst Portfolio](https://github.com/yandri918/data_analyst)

## 🙏 Acknowledgments

- Streamlit for the amazing framework
- Altair for powerful declarative visualizations
- The data science community for inspiration

---

Built with ❤️ using Streamlit & Altair
