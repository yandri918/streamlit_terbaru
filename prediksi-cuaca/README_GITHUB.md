# 🌤️ Weather Prediction & Forecasting System

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **Advanced weather forecasting platform** dengan interactive dashboard, machine learning predictions, dan RESTful API deployment.

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Machine Learning Models](#-machine-learning-models)
- [Deployment](#-deployment)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

Weather Prediction System adalah platform forecasting cuaca yang comprehensive dengan:

- **Interactive Dashboard**: 11 halaman Streamlit dengan visualisasi interaktif
- **Machine Learning**: 4 model ML (ARIMA, Prophet, LSTM, XGBoost) untuk prediksi
- **RESTful API**: FastAPI endpoints untuk integrasi dengan aplikasi lain
- **Real-time Data**: Integrasi dengan Open-Meteo API untuk data cuaca real-time
- **Advanced Analytics**: UV index, heat stress, weather comfort analysis
- **Production Ready**: Docker deployment dengan CI/CD pipeline

---

## ✨ Features

### 🎯 Core Features

#### 1. **Interactive Map** 🗺️
- Pilih lokasi dengan klik pada peta
- Marker interaktif dengan popup
- Koordinat latitude/longitude
- Session state management

#### 2. **Current Weather Dashboard** 🌤️
- **Hero Display**: Temperature besar dengan gradient background
- **Comfort Indicators**: 
  - Tingkat kenyamanan (heat index calculation)
  - Risiko UV (time-based estimation)
  - Kualitas udara (AQI estimate)
- **Atmospheric Gauges**: Interactive Plotly gauges untuk humidity & pressure
- **Wind Analysis**: 
  - Wind rose compass (polar chart)
  - 8 arah mata angin
  - Skala Beaufort
- **Hourly Mini-Forecast**: 12 jam ke depan
- **Astronomical Data**: Sunrise, sunset, sunshine duration, moon phase
- **Smart Alerts**: Temperature, wind, humidity, UV warnings

#### 3. **7-Day Forecast** 📅
- Daily forecast cards dengan emoji
- Temperature range (min/max)
- Precipitation probability
- Wind speed & direction
- Sunrise/sunset times
- Interactive charts

#### 4. **Hourly Forecast** ⏰
- 48-hour detailed forecast
- Temperature trends
- Precipitation probability
- Wind speed analysis
- Cloud cover visualization
- Interactive time-series charts

#### 5. **Weather Comparison** 🔄
- Compare 2 locations side-by-side
- Temperature comparison
- Precipitation comparison
- Wind speed comparison
- Humidity & pressure comparison
- Dual-location maps

#### 6. **Historical Analysis** 📊
- 30-day historical data
- Temperature trends
- Precipitation patterns
- Statistical analysis
- Correlation matrices

#### 7. **Weather Alerts** ⚠️
- Extreme temperature alerts
- Heavy rain warnings
- Strong wind alerts
- Custom threshold settings
- Alert history

#### 8. **Moon Phase Calendar** 🌙
- Current moon phase
- Illumination percentage
- Phase emoji & description
- Astronomical calculations

#### 9. **Weather Statistics** 📈
- **UV Index Analysis**:
  - UV trend charts
  - Category distribution
  - Health recommendations
  - Protection advice
- **Heat Stress Analysis**:
  - Heat index calculation
  - Comfort zones
  - Health warnings
- **Advanced Correlations**:
  - Temperature vs Humidity
  - Pressure vs Weather
  - Wind patterns
- **Extreme Events**:
  - Hottest/coldest days
  - Wettest days
  - Windiest days
- **Statistical Summaries**:
  - Percentiles
  - Distributions
  - Trends

#### 10. **Weather Radar** 📡
- **Realistic Precipitation Radar**:
  - 100x100 high-resolution grid
  - Gaussian precipitation cells
  - 8-level color scale
  - Geographic overlay
- **48-Hour Forecast Timeline**:
  - Intensity & probability charts
  - Zone annotations (ringan/sedang/lebat)
- **Intensity Scale Legend**:
  - Gerimis → Hujan Ekstrem
  - Color-coded dengan emoji
- **Atmospheric Conditions**:
  - Cloud cover timeline
  - Visibility forecast
- **Current Statistics**:
  - 24h total precipitation
  - Max intensity
  - Rain likelihood

#### 11. **ML Forecasting** 🤖
- **4 Machine Learning Models**:
  - **ARIMA**: Auto parameter selection (p,d,q)
  - **Prophet**: Facebook's forecasting tool
  - **LSTM**: Deep learning RNN
  - **XGBoost**: Gradient boosting
- **Model Comparison**:
  - Side-by-side forecasts
  - Performance metrics (MAE, RMSE, MAPE)
  - Training time comparison
- **Ensemble Methods**:
  - Weighted average
  - Combines all models
- **Feature Importance**:
  - XGBoost feature analysis
  - Top 10 features
- **Export Capabilities**:
  - Download forecasts as CSV
  - Includes confidence intervals

### 🔌 API Features

- **RESTful Endpoints**: 6 production-ready endpoints
- **Auto Documentation**: Swagger UI & ReDoc
- **Request Validation**: Pydantic models
- **Error Handling**: Comprehensive error responses
- **CORS Support**: Cross-origin requests enabled
- **Health Checks**: Monitoring endpoint

### 🐳 Deployment Features

- **Docker Support**: Multi-stage Dockerfile
- **Docker Compose**: Orchestration dengan Nginx
- **CI/CD Pipeline**: GitHub Actions automation
- **Testing**: Unit tests dengan pytest
- **Code Quality**: Linting dengan flake8 & black

---

## 🛠️ Tech Stack

### Frontend
- **Streamlit** 1.28+ - Interactive web framework
- **Plotly** 5.17+ - Interactive visualizations
- **Folium** 0.14+ - Interactive maps

### Backend
- **FastAPI** 0.104+ - Modern API framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

### Data & ML
- **Pandas** 2.0+ - Data manipulation
- **NumPy** 1.24+ - Numerical computing
- **SciPy** 1.11+ - Scientific computing
- **Statsmodels** 0.14+ - Statistical models (ARIMA)
- **Prophet** 1.1+ - Facebook forecasting
- **TensorFlow** 2.15+ - Deep learning (LSTM)
- **XGBoost** 2.0+ - Gradient boosting
- **Scikit-learn** 1.3+ - ML utilities

### Data Source
- **Open-Meteo API** - Free weather API
  - Current weather
  - Hourly forecast (168 hours)
  - Daily forecast (16 days)
  - Historical data

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **GitHub Actions** - CI/CD automation
- **Nginx** - Reverse proxy

---

## 📦 Installation

### Prerequisites

- Python 3.11 or higher
- pip package manager
- Git
- Docker (optional, for containerized deployment)

### Local Development Setup

1. **Clone the repository:**
```bash
git clone https://github.com/yandri918/prediksi-cuaca.git
cd prediksi-cuaca
```

2. **Create virtual environment:**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies:**
```bash
# Streamlit app dependencies
pip install -r requirements.txt

# API dependencies (optional)
pip install -r requirements-api.txt
```

4. **Run the Streamlit app:**
```bash
streamlit run app.py
```

5. **Access the application:**
- Streamlit Dashboard: http://localhost:8501
- API (if running): http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🚀 Usage

### Streamlit Dashboard

1. **Select Location**:
   - Navigate to "Interactive Map" page
   - Click on the map to select location
   - Or enter coordinates manually

2. **View Current Weather**:
   - Go to "Current Weather Dashboard"
   - See real-time conditions
   - Check comfort indicators
   - View hourly mini-forecast

3. **Check Forecasts**:
   - **7-Day Forecast**: Daily overview
   - **Hourly Forecast**: 48-hour detailed
   - **Weather Radar**: Precipitation visualization

4. **Analyze Data**:
   - **Weather Statistics**: UV, heat stress, correlations
   - **Historical Analysis**: 30-day trends
   - **Comparison**: Compare 2 locations

5. **ML Predictions**:
   - Go to "ML Forecasting"
   - Select models to train
   - Configure forecast horizon
   - View predictions & metrics
   - Download results

### FastAPI

1. **Start the API server:**
```bash
python api.py
```

2. **Access API documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

3. **Make API requests:**

**Get current weather:**
```bash
curl "http://localhost:8000/api/v1/weather/current?latitude=-6.2&longitude=106.8"
```

**Get hourly forecast:**
```bash
curl "http://localhost:8000/api/v1/weather/hourly?latitude=-6.2&longitude=106.8&hours=24"
```

**Get daily forecast:**
```bash
curl "http://localhost:8000/api/v1/weather/daily?latitude=-6.2&longitude=106.8&days=7"
```

---

## 📖 API Documentation

### Endpoints

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-31T12:00:00",
  "version": "1.0.0"
}
```

#### Current Weather
```http
GET /api/v1/weather/current?latitude={lat}&longitude={lon}
```

**Parameters:**
- `latitude` (float): -90 to 90
- `longitude` (float): -180 to 180

**Response:**
```json
{
  "location": {"latitude": -6.2, "longitude": 106.8},
  "timestamp": "2024-01-31T12:00:00",
  "temperature": 28.5,
  "feels_like": 32.1,
  "humidity": 75,
  "pressure": 1013.2,
  "wind_speed": 12.5,
  "wind_direction": 180,
  "cloud_cover": 50,
  "weather_code": 3,
  "description": "Berawan",
  "timezone": "Asia/Jakarta"
}
```

#### Hourly Forecast
```http
GET /api/v1/weather/hourly?latitude={lat}&longitude={lon}&hours={hours}
```

**Parameters:**
- `latitude` (float): -90 to 90
- `longitude` (float): -180 to 180
- `hours` (int): 1-168 (default: 24)

#### Daily Forecast
```http
GET /api/v1/weather/daily?latitude={lat}&longitude={lon}&days={days}
```

**Parameters:**
- `latitude` (float): -90 to 90
- `longitude` (float): -180 to 180
- `days` (int): 1-16 (default: 7)

#### Weather Statistics
```http
GET /api/v1/weather/statistics?latitude={lat}&longitude={lon}&days={days}
```

For complete API documentation, visit `/docs` when running the API server.

---

## 🤖 Machine Learning Models

### 1. ARIMA (AutoRegressive Integrated Moving Average)

**Description**: Statistical model untuk time series forecasting

**Features**:
- Auto parameter selection menggunakan `pmdarima`
- Optimal (p, d, q) parameters
- Confidence intervals
- Best for: Short-term univariate forecasts

**Training Time**: ~5-10 seconds

### 2. Prophet (Facebook)

**Description**: Forecasting tool dari Facebook

**Features**:
- Automatic seasonality detection
- Handles missing data
- Interpretable components (trend, weekly, yearly)
- Robust to outliers

**Training Time**: ~10-20 seconds

### 3. LSTM (Long Short-Term Memory)

**Description**: Deep learning RNN architecture

**Features**:
- 50-unit LSTM layers
- Dropout regularization
- Captures complex non-linear patterns
- Sequence-to-sequence learning

**Training Time**: ~30-60 seconds (50 epochs)

### 4. XGBoost (Extreme Gradient Boosting)

**Description**: Gradient boosting for time series

**Features**:
- Feature engineering (lag, rolling, time features)
- Feature importance analysis
- Handles non-linear relationships
- Fast training

**Training Time**: ~10-15 seconds

### Ensemble Method

Combines all 4 models using weighted average for improved accuracy.

---

## 🐳 Deployment

### Docker Deployment

1. **Build the image:**
```bash
docker build -t weather-api .
```

2. **Run the container:**
```bash
docker run -d -p 8000:8000 --name weather-api weather-api
```

### Docker Compose

1. **Start all services:**
```bash
docker-compose up -d
```

2. **View logs:**
```bash
docker-compose logs -f
```

3. **Stop services:**
```bash
docker-compose down
```

### Production Deployment

See [API_DEPLOYMENT.md](API_DEPLOYMENT.md) for detailed deployment instructions including:
- VPS/Cloud Server deployment
- Heroku deployment
- Railway deployment
- Render deployment
- CI/CD setup

---

## 📸 Screenshots

### Interactive Map
![Interactive Map](screenshots/interactive-map.png)

### Current Weather Dashboard
![Current Weather](screenshots/current-weather.png)

### Weather Radar
![Weather Radar](screenshots/weather-radar.png)

### ML Forecasting
![ML Forecasting](screenshots/ml-forecasting.png)

### API Documentation
![API Docs](screenshots/api-docs.png)

---

## 📊 Project Structure

```
prediksi-cuaca/
├── app.py                      # Main Streamlit application
├── api.py                      # FastAPI application
├── requirements.txt            # Streamlit dependencies
├── requirements-api.txt        # API dependencies
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose configuration
├── nginx.conf                  # Nginx configuration
├── .dockerignore              # Docker ignore file
├── API_DEPLOYMENT.md          # Deployment guide
├── README.md                  # This file
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml          # GitHub Actions CI/CD
│
├── pages/                     # Streamlit pages
│   ├── 01_🗺️_Interactive_Map.py
│   ├── 02_🌤️_Current_Weather.py
│   ├── 03_📅_7-Day_Forecast.py
│   ├── 04_⏰_Hourly_Forecast.py
│   ├── 05_🔄_Weather_Comparison.py
│   ├── 06_📊_Historical_Analysis.py
│   ├── 07_⚠️_Weather_Alerts.py
│   ├── 08_🌙_Moon_Phase.py
│   ├── 09_📈_Weather_Statistics.py
│   ├── 10_📡_Weather_Radar.py
│   └── 11_🤖_ML_Forecasting.py
│
├── utils/                     # Utility modules
│   ├── weather_api.py         # Weather API integration
│   ├── moon_phase.py          # Moon phase calculations
│   └── ml_forecasting.py      # ML models
│
└── tests/                     # Unit tests
    └── test_api.py            # API tests
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add unit tests for new features
- Update documentation
- Run tests before submitting PR

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Yandri**
- GitHub: [@yandri918](https://github.com/yandri918)
- Portfolio: [AgriSensa Portfolio](https://github.com/yandri918/agrisensa-api)

---

## 🙏 Acknowledgments

- [Open-Meteo](https://open-meteo.com/) - Free weather API
- [Streamlit](https://streamlit.io/) - Interactive web framework
- [FastAPI](https://fastapi.tiangolo.com/) - Modern API framework
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Facebook Prophet](https://facebook.github.io/prophet/) - Forecasting tool

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/yandri918/prediksi-cuaca/issues)
- Email: yandri918@example.com

---

## 🗺️ Roadmap

- [ ] Add more ML models (Random Forest, Neural Prophet)
- [ ] Implement caching for API responses
- [ ] Add user authentication
- [ ] Create mobile app version
- [ ] Add more weather parameters (air quality, pollen)
- [ ] Implement real-time notifications
- [ ] Add historical data download
- [ ] Create custom alert rules

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yandri918/prediksi-cuaca&type=Date)](https://star-history.com/#yandri918/prediksi-cuaca&Date)

---

<div align="center">

**Made with ❤️ by Yandri**

If you find this project useful, please consider giving it a ⭐!

</div>
