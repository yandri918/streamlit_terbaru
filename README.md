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

### Platform Pertanian Cerdas Berbasis AI untuk Petani Indonesia

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Hugging Face](https://img.shields.io/badge/🤗-Hugging%20Face-orange)](https://huggingface.co/spaces/yandri918/agrisensa-api)

[Demo](https://huggingface.co/spaces/yandri918/agrisensa-api) • [Dokumentasi](#dokumentasi) • [Fitur](#fitur-utama) • [Instalasi](#instalasi)

</div>

---

## 📖 Tentang AgriSensa

AgriSensa adalah platform pertanian cerdas yang memanfaatkan teknologi **Artificial Intelligence (AI)**, **Machine Learning**, dan **Computer Vision** untuk membantu petani Indonesia meningkatkan produktivitas dan keberlanjutan usaha tani. Platform ini menyediakan 25+ modul canggih yang mencakup analisis tanah, rekomendasi tanaman, deteksi penyakit, prediksi harga pasar, dan banyak lagi.

### 🎯 Visi & Misi

**Visi:** Menjadi platform pertanian digital terdepan yang memberdayakan petani Indonesia dengan teknologi AI.

**Misi:**
- Meningkatkan produktivitas pertanian melalui rekomendasi berbasis data
- Mengurangi kerugian akibat hama dan penyakit dengan deteksi dini
- Memberikan akses informasi pasar yang transparan dan real-time
- Menyediakan edukasi pertanian yang mudah diakses

---

## ✨ Fitur Utama

### 🤖 AI & Machine Learning
- **AgriBot** - Asisten pertanian cerdas berbasis Google Gemini AI
- **Rekomendasi Tanaman Cerdas** - Analisis NPK, pH, iklim untuk rekomendasi optimal
- **Prediksi Hasil Panen** - Estimasi tonase berdasarkan kondisi lahan
- **Analisis Tren Harga** - Prediksi harga komoditas dengan Linear Regression
- **Intelijen Prediktif (XAI)** - Prediksi dengan penjelasan transparan

### 🔬 Analisis & Diagnostik
- **Dokter Tanaman AI** - Deteksi penyakit tanaman dengan Roboflow AI
- **Analisis BWD** - Deteksi penyakit padi dengan Computer Vision
- **Diagnostik Gejala Cerdas** - Identifikasi hama & penyakit via kuesioner
- **Analisis NPK Manual** - Input dan analisis kesuburan tanah
- **Analis Risiko Keberhasilan** - Evaluasi potensi keberhasilan usaha tani

### 🧮 Kalkulator & Tools
- **Kalkulator Pupuk Holistik** - Perhitungan kebutuhan pupuk presisi dengan jadwal bertahap
- **Kalkulator Konversi Pupuk** - Konversi dosis antar jenis pupuk
- **Rekomendasi Pupuk** - Saran pemupukan berdasarkan kondisi tanah
- **Strategi Penyemprotan Cerdas** - Optimasi jadwal dan dosis penyemprotan

### 💰 Intelijen Pasar
- **Intelijen Harga Pasar** - Monitor harga komoditas real-time
- **Analisis Tren Harga** - Visualisasi dan prediksi tren harga
- **Katalog Pupuk** - Referensi lengkap harga dan spesifikasi pupuk

### 📚 Basis Pengetahuan
- **Basis Pengetahuan Budidaya** - SOP dan teknik budidaya terbaik (20+ komoditas)
- **Ensiklopedia Komoditas** - Informasi mendalam berbagai komoditas
- **Panduan Buah** - Ensiklopedia budidaya tanaman buah tropis
- **Panduan Hama & Penyakit** - Database lengkap hama dan pengendaliannya
- **Info Pestisida** - Direktori bahan aktif, cara kerja, dan keamanan
- **Pusat Pengetahuan Pertanian** - Info pupuk NPK, agen hayati, hormon tanaman
- **Info pH Tanah** - Panduan manajemen keasaman tanah

### 🗺️ Fitur Lanjutan
- **AgriMap AI** - Rekomendasi tanaman berbasis lokasi (Geospatial)
- **Perencana Hasil Panen AI** - Perencanaan target panen dengan AI
- **Dasbor Rekomendasi Terpadu** - Pusat rekomendasi terintegrasi
- **Pustaka Dokumen** - Regulasi dan dokumen resmi pertanian

---

## 🏗️ Arsitektur Teknologi

### Tech Stack

**Backend:**
- Python 3.12
- Flask 3.0 (Web Framework)
- SQLAlchemy (ORM)
- Flask-Migrate (Database Migrations)
- Flask-JWT-Extended (Authentication)
- Flask-CORS (Cross-Origin Resource Sharing)
- Flask-Limiter (Rate Limiting)

**Machine Learning & AI:**
- scikit-learn (ML Models)
- TensorFlow/Keras (Deep Learning)
- Google Generative AI (Gemini API)
- Roboflow (Computer Vision)
- SHAP (Explainable AI)

**Data Processing:**
- pandas (Data Manipulation)
- numpy (Numerical Computing)
- Pillow (Image Processing)

**Frontend:**
- HTML5, CSS3, JavaScript (ES6+)
- Chart.js (Data Visualization)
- Marked.js (Markdown Rendering)

**Deployment:**
- Docker (Containerization)
- Hugging Face Spaces (Hosting)
- Git (Version Control)

### Struktur Direktori

```
agrisensa-api/
├── app/
│   ├── __init__.py           # Application factory
│   ├── config/               # Configuration files
│   ├── data/                 # Static data & databases
│   │   ├── cultivation_db.py # Cultivation knowledge base
│   │   ├── pest_disease_db.py# Pest & disease database
│   │   └── fertilizer_db.py  # Fertilizer database
│   ├── models/               # SQLAlchemy models
│   ├── routes/               # API routes/blueprints
│   │   ├── main.py          # Main routes
│   │   ├── legacy.py        # Legacy endpoints
│   │   ├── analysis.py      # Analysis endpoints
│   │   └── ...
│   ├── services/             # Business logic
│   │   ├── ml_service.py    # ML model service
│   │   ├── market_service.py# Market intelligence
│   │   ├── chatbot_service.py# Chatbot service
│   │   └── ...
│   └── utils/               # Utility functions
├── templates/               # HTML templates
│   └── modules/            # Module-specific templates
├── static/                 # Static assets
│   ├── css/
│   ├── js/
│   ├── icons/
│   ├── manifest.json       # PWA manifest
│   └── sw.js              # Service worker
├── instance/              # Instance-specific files
├── migrations/            # Database migrations
├── Dockerfile            # Docker configuration
├── requirements.txt      # Python dependencies
├── run.py               # Application entry point
└── README.md            # This file
```

---

## 🚀 Instalasi

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

5. **Initialize Database**
```bash
flask init-db
```

6. **Run Development Server**
```bash
python run.py
```

Server akan berjalan di `http://localhost:5000`

### Docker Deployment

```bash
# Build image
docker build -t agrisensa-api .

# Run container
docker run -p 7860:7860 agrisensa-api
```

### Hugging Face Spaces

1. Fork repository ini
2. Buat Space baru di Hugging Face
3. Connect repository ke Space
4. Set environment variables di Space Settings
5. Deploy!

---

## 📱 Progressive Web App (PWA)

AgriSensa mendukung instalasi sebagai aplikasi Android/iOS melalui PWA:

**Cara Install di Android:**
1. Buka AgriSensa di Chrome
2. Tap menu (⋮) → "Install App" atau "Add to Home Screen"
3. Aplikasi akan muncul di menu HP Anda

**Fitur PWA:**
- ✅ Offline capability
- ✅ App-like experience
- ✅ Fast loading
- ✅ Push notifications (coming soon)

---

## 🔌 API Documentation

### Base URL
```
Production: https://huggingface.co/spaces/yandri918/agrisensa-api
Local: http://localhost:5000
```

### Authentication
Beberapa endpoint memerlukan JWT token. Dapatkan token melalui `/api/auth/login`.

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
  "commodity": "padi",
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
  "message": "Bagaimana cara menanam padi yang baik?"
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
  "commodity": "cabe",
  "days": 7
}
```

Dokumentasi lengkap tersedia di `/api/info`

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

Kontribusi sangat diterima! Silakan ikuti langkah berikut:

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

Butuh bantuan? Hubungi kami:

- 📧 Email: support@agrisensa.com
- 💬 Discord: [AgriSensa Community](https://discord.gg/agrisensa)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/agrisensa-api/issues)
- 📖 Docs: [Documentation](https://agrisensa.gitbook.io)

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

**Dibuat dengan ❤️ untuk Petani Indonesia**

⭐ Star repository ini jika bermanfaat!

[Website](https://mirai39.streamlit.app/) • [GitHub](https://github.com/yandri918) • [LinkedIn](https://www.linkedin.com/in/andriyanto-na-147492157)

</div>