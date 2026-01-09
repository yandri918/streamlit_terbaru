---
title: AgriSensa API
emoji: 🌾
colorFrom: green
colorTo: yellow
sdk: docker
pinned: false
app_port: 7860
---

<div align="center">

# 🌾 AgriSensa

### AI-Powered Smart Agriculture Platform for Indonesian Farmers

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Streamlit Cloud](https://img.shields.io/badge/Streamlit-Cloud-orange)](https://mirai39.streamlit.app/)

[Live Demo](https://mirai39.streamlit.app/) • [Documentation](#documentation) • [Features](#key-features) • [Installation](#installation)

</div>

---

## 📖 About AgriSensa

AgriSensa is an intelligent agriculture platform that leverages **Artificial Intelligence (AI)**, **Machine Learning**, and **Computer Vision** technologies to help Indonesian farmers improve productivity and farming sustainability. The platform provides 25+ advanced modules covering soil analysis, crop recommendations, disease detection, market price prediction, and much more.

### 🎯 Vision & Mission

**Vision:** To become the leading digital agriculture platform that empowers Indonesian farmers with AI technology.

**Mission:**
- Increase agricultural productivity through data-driven recommendations
- Reduce losses from pests and diseases with early detection
- Provide transparent and real-time market information access
- Deliver easily accessible agricultural education

---

## ✨ Key Features

### 🤖 AI & Machine Learning
- **AgriBot** - Intelligent farming assistant powered by Google Gemini AI
- **Smart Crop Recommendation** - NPK, pH, and climate analysis for optimal recommendations
- **Harvest Prediction** - Tonnage estimation based on field conditions
- **Price Trend Analysis** - Commodity price prediction using Linear Regression
- **Predictive Intelligence (XAI)** - Transparent predictions with explanations

### 🔬 Analysis & Diagnostics
- **AI Plant Doctor** - Plant disease detection with Roboflow AI
- **BWD Analysis** - Rice disease detection with Computer Vision
- **Smart Symptom Diagnostic** - Pest & disease identification via questionnaire
- **Manual NPK Analysis** - Soil fertility input and analysis
- **Success Risk Analyst** - Farming success potential evaluation

### 🧮 Calculators & Tools
- **Holistic Fertilizer Calculator** - Precision fertilizer calculation with staged scheduling
- **Fertilizer Conversion Calculator** - Dose conversion between fertilizer types
- **Fertilizer Recommendation** - Fertilization advice based on soil conditions
- **Smart Spraying Strategy** - Spraying schedule and dosage optimization

### 💰 Market Intelligence
- **Market Price Intelligence** - Real-time commodity price monitoring
- **Price Trend Analysis** - Price trend visualization and prediction
- **Fertilizer Catalog** - Complete reference of fertilizer prices and specifications

### 📚 Knowledge Base
- **Cultivation Knowledge Base** - Best practices and SOPs (20+ commodities)
- **Commodity Encyclopedia** - In-depth information on various commodities
- **Fruit Guide** - Encyclopedia of tropical fruit cultivation
- **Pest & Disease Guide** - Complete database of pests and control methods
- **Pesticide Info** - Directory of active ingredients, mechanisms, and safety
- **Agricultural Knowledge Center** - NPK fertilizer, biological agents, plant hormones info
- **Soil pH Info** - Soil acidity management guide

### 🗺️ Advanced Features
- **AgriMap AI** - Location-based crop recommendations (Geospatial)
- **AI Harvest Planner** - AI-powered harvest target planning
- **Integrated Recommendation Dashboard** - Centralized integrated recommendations
- **Document Library** - Agricultural regulations and official documents

---

## 🏗️ Technology Architecture

### Tech Stack

**Backend & Framework:**
- Python 3.12
- Streamlit 1.32+ (Web Framework)
- pandas (Data Processing)
- plotly (Interactive Visualizations)
- numpy (Numerical Computing)

**Machine Learning & AI:**
- scikit-learn (ML Models)
- Google Generative AI (Gemini API)
- Roboflow (Computer Vision)
- SHAP (Explainable AI)

**Data Processing:**
- pandas (Data Manipulation)
- numpy (Numerical Computing)
- Pillow (Image Processing)
- openpyxl (Excel Processing)

**Visualization:**
- plotly (Interactive Charts)
- matplotlib (Static Charts)
- seaborn (Statistical Plots)

**Deployment:**
- Streamlit Cloud (Hosting)
- Git (Version Control)
- GitHub (Repository)

### Directory Structure

```
streamlit_terbaru/
├── agrisensa_main.py        # Main hub application
├── agrisensa_tech/          # Technology modules
│   ├── pages/              # Streamlit pages
│   │   ├── 11_📊_Analisis_Risiko.py
│   │   ├── 15_📸_Estimasi_Panen_AI.py
│   │   ├── 17_🌦️_Kalender_Tanam_Cerdas.py
│   │   └── ...
├── agrisensa_commodities/   # Commodity guides
│   └── pages/
├── agrisensa_biz/          # Business intelligence
│   └── pages/
├── agrisensa_eco/          # Ecosystem modules
│   └── pages/
├── agrisensa_livestock/    # Livestock modules
│   └── pages/
├── data_analysis/          # Data & datasets
├── services/               # Shared services
│   ├── gemini_service.py  # Gemini AI integration
│   ├── roboflow_service.py# Computer vision
│   └── ...
├── utils/                  # Utility functions
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

## 🚀 Installation

### Prerequisites

- Python 3.12+
- pip (Python package manager)
- Git
- (Optional) Docker

### Local Development

1. **Clone Repository**
```bash
git clone https://github.com/yandri918/streamlit_terbaru.git
cd streamlit_terbaru
```

2. **Create Virtual Environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Set Environment Variables**

Create a `.env` file:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///agrisensa.db
GEMINI_API_KEY=your-gemini-api-key
```

5. **Run Streamlit App**
```bash
streamlit run agrisensa_main.py
```

Server will run at `http://localhost:8501`

### Streamlit Cloud Deployment

1. Push repository to GitHub
2. Login to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect GitHub repository
4. Set main file: `agrisensa_main.py`
5. Add secrets in Settings (GEMINI_API_KEY, etc.)
6. Deploy!

---

## 📱 Progressive Web App (PWA)

AgriSensa supports installation as an Android/iOS app via PWA:

**How to Install on Android:**
1. Open AgriSensa in Chrome
2. Tap menu (⋮) → "Install App" or "Add to Home Screen"
3. App will appear in your phone menu

**PWA Features:**
- ✅ Offline capability
- ✅ App-like experience
- ✅ Fast loading
- ✅ Push notifications (coming soon)

---

## 🔌 API Documentation

### Base URL
```
Production: https://mirai39.streamlit.app/
Local: http://localhost:8501
```

### Streamlit Pages
AgriSensa uses multi-page Streamlit architecture with 6 satellite applications:

1. **Main Hub** - Main dashboard and navigation
2. **AgriSensa Tech** - Technology modules (AI, ML, Computer Vision)
3. **AgriSensa Commodities** - Commodity cultivation guides
4. **AgriSensa Biz** - Business intelligence & market analysis
5. **AgriSensa Eco** - Sustainable agriculture ecosystem
6. **AgriSensa Livestock** - Livestock & aquaculture

### Key Endpoints

#### Crop Recommendation
```http
POST /recommend-crop
Content-Type: application/json

{
  "n_value": 80,
  "p_value": 40,
  "k_value": 50,
  "ph": 6.5,
  "temperature": 28,
  "humidity": 75,
  "rainfall": 150
}
```

#### Fertilizer Recommendation
```http
POST /recommend-fertilizer
Content-Type: application/json

{
  "commodity": "rice",
  "area_sqm": 1000,
  "ph": 6.5
}
```

#### Yield Prediction (XAI)
```http
POST /predict-yield-advanced
Content-Type: application/json

{
  "n": 80,
  "p": 40,
  "k": 50,
  "temperature": 28,
  "humidity": 75,
  "ph": 6.5,
  "rainfall": 150
}
```

#### Chatbot
```http
POST /chat
Content-Type: application/json

{
  "message": "What's the best way to grow rice?"
}
```

#### Market Prices
```http
GET /get-ticker-prices
```

#### Price Trend Prediction
```http
POST /predict-price-trend
Content-Type: application/json

{
  "commodity": "chili",
  "days": 7
}
```

Complete documentation available in the "Methodology & Validation" page within the application.

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_ml_service.py
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

### Coding Standards
- Follow PEP 8 for Python code
- Write docstrings for all functions
- Add unit tests for new features
- Update documentation as needed

---

## 📊 Database Schema

### Users
- `id` (Primary Key)
- `username`
- `email`
- `password_hash`
- `role` (admin/user)
- `created_at`

### NPK Readings
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `n_value`, `p_value`, `k_value`
- `ph`, `temperature`, `humidity`, `rainfall`
- `location`
- `timestamp`

### Recommendations
- `id` (Primary Key)
- `user_id` (Foreign Key)
- `type` (crop/fertilizer)
- `input_data` (JSON)
- `recommendation` (JSON)
- `timestamp`

---

## 🔐 Security

- JWT-based authentication
- Password hashing with Werkzeug
- CORS protection
- Rate limiting (100 requests/hour)
- Input validation & sanitization
- SQL injection prevention via ORM

---

## 📈 Performance

- Response time: < 200ms (average)
- Uptime: 99.5%
- Concurrent users: 100+
- Database: SQLite (dev), PostgreSQL (prod recommended)

---

## 🌍 Roadmap

### Q1 2025
- [ ] Mobile app (React Native)
- [ ] Real-time IoT sensor integration
- [ ] Multi-language support (English, Javanese)
- [ ] Advanced weather forecasting

### Q2 2025
- [ ] Blockchain-based supply chain tracking
- [ ] Drone imagery analysis
- [ ] Community forum
- [ ] Marketplace integration

### Q3 2025
- [ ] AI-powered crop insurance
- [ ] Precision agriculture tools
- [ ] Farmer networking platform

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Team

**Developer:** Andriyanto  
**Email:** [yandri918@gmail.com](mailto:yandri918@gmail.com)  
**GitHub:** [@yandri918](https://github.com/yandri918)  
**LinkedIn:** [Andriyanto NA](https://www.linkedin.com/in/andriyanto-na-147492157)  
**Website:** [mirai39.streamlit.app](https://mirai39.streamlit.app/)

---

## 🙏 Acknowledgments

- Google Gemini AI for chatbot capabilities
- Roboflow for computer vision models
- Hugging Face for hosting platform
- Indonesian Ministry of Agriculture for data sources
- Open source community

---

## 📞 Support

Need help? Contact us:

- 📧 Email: yandri918@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/yandri918/streamlit_terbaru/issues)
- 💼 LinkedIn: [Andriyanto NA](https://www.linkedin.com/in/andriyanto-na-147492157)

---

## 📸 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### Crop Recommendation
![Crop Recommendation](docs/screenshots/crop-recommendation.png)

### AgriBot
![AgriBot](docs/screenshots/agribot.png)

### Market Intelligence
![Market Intelligence](docs/screenshots/market-intelligence.png)

---

<div align="center">

**Built with ❤️ for Indonesian Farmers**

⭐ Star this repository if you find it useful!

[Website](https://mirai39.streamlit.app/) • [GitHub](https://github.com/yandri918) • [LinkedIn](https://www.linkedin.com/in/andriyanto-na-147492157)

</div>
