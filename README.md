
<div align="center">

# 🌾 AgriSensa
### AI-Powered Smart Agriculture Platform for Indonesia
*Empowering farmers with data, intelligence, and automation.*

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mirai39.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Demo](https://mirai39.streamlit.app/) • [Dokumentasi](#-dokumentasi) • [Roadmap](#-roadmap-2025) • [API](#-api-documentation)

</div>

---

## 🚀 Ringkasan Eksekutif

**AgriSensa** adalah platform pertanian cerdas berbasis AI yang dirancang untuk meningkatkan produktivitas, efisiensi, dan keberlanjutan pertanian Indonesia. Dengan lebih dari **25+ modul AI, Machine Learning, dan Computer Vision**, AgriSensa memberdayakan petani untuk mengambil keputusan berbasis data—mulai dari analisis tanah presisi, rekomendasi tanaman, deteksi penyakit dini, hingga prediksi harga pasar yang akurat.

Dibangun dengan arsitektur modern yang modular dan scalable, AgriSensa siap dikembangkan menjadi solusi komersial, SaaS, atau platform enterprise untuk masa depan pertanian digital Indonesia.

---

## 🎯 Nilai Utama (Why AgriSensa Matters)

### 🌱 Tantangan Industri Pertanian
- **Kerugian Panen Tinggi**: 40–60% hasil panen hilang akibat serangan hama & penyakit yang terlambat dideteksi.
- **Keterbatasan Informasi**: Akses terhadap pemupukan yang tepat, harga pasar real-time, dan SOP budidaya masih sangat minim.
- **Keputusan Intuitif**: Petani sering bertani berdasarkan kebiasaan, bukan data, karena kurangnya alat prediksi.
- **Adopsi Teknologi Rendah**: Minimnya integrasi AI dan teknologi modern dalam rantai pasok pertanian lokal.

### 🤖 Solusi AgriSensa
- **Deteksi Dini**: Identifikasi penyakit tanaman secara instan menggunakan Computer Vision.
- **Rekomendasi Presisi**: Algoritma cerdas yang merekomendasikan tanaman berdasarkan NPK, pH, iklim, dan lokasi.
- **Prediksi Cerdas**: Machine Learning untuk memprediksi hasil panen dan tren harga pasar masa depan.
- **Dashboard Terintegrasi**: Satu platform untuk memantau seluruh aspek pertanian, dari hulu ke hilir.
- **Basis Pengetahuan**: Ensiklopedia digital terstruktur untuk 20+ komoditas pertanian utama.

### 📈 Dampak Nyata
- ✅ **Mengurangi risiko kerugian panen** secara signifikan.
- ✅ **Meningkatkan efisiensi** penggunaan pupuk dan pestisida.
- ✅ **Mendongkrak produktivitas** lahan dengan pengelolaan berbasis data.
- ✅ **Demokratisasi data** pertanian real-time bagi petani kecil.

---

## ✨ Fitur Utama

### 🤖 AI & Machine Learning
| Fitur | Deskripsi | Teknologi |
|-------|-----------|-----------|
| **AgriBot** | Asisten pertanian cerdas siap jawab 24/7 | Gemini AI |
| **Crop Recommendation** | Rekomendasi tanaman optimal berdasarkan data tanah & iklim | Random Forest / XGBoost |
| **Yield Prediction (XAI)** | Prediksi hasil panen dengan penjelasan faktor pengaruh (SHAP) | Regresi & SHAP |
| **Price Forecasting** | Prediksi tren harga komoditas masa depan | Time Series Analysis |
| **Explainable AI** | Transparansi model untuk pengambilan keputusan kritis | XAI Frameworks |

### 🔬 Analisis & Diagnostik
- **Dokter Tanaman AI**: Deteksi penyakit otomatis via upload foto (integrasi Roboflow).
- **Analisis BWD**: Deteksi dini penyakit pada daun padi menggunakan indeks warna.
- **Diagnostik Gejala**: Identifikasi hama & penyakit interaktif berbasis gejala visual.
- **Analisis NPK Manual**: Evaluasi tingkat kesuburan tanah dan rekomendasi perbaikan.

### 🧮 Kalkulator & Tools
- **Kalkulator Pupuk Holistik**: Hitung kebutuhan pupuk secara presisi.
- **Konversi Pupuk**: Alat bantu konversi dosis pupuk tunggal ke majemuk (dan sebaliknya).
- **Strategi Penyemprotan**: Jadwal dan dosis penyemprotan hama yang cerdas.
- **Rekomendasi Otomatis**: Saran pemupukan spesifik lokasi dan komoditas.

### 💰 Intelijen Pasar
- **Harga Real-time**: Monitoring harga komoditas di berbagai pasar.
- **Tren Masa Depan**: Analisis pergerakan harga untuk strategi jual.
- **Katalog Pupuk**: Database harga dan ketersediaan pupuk nasional.

### 📚 Basis Pengetahuan
- **SOP Budidaya Lengkap**: Panduan langkah demi langkah untuk 20+ komoditas.
- **Ensiklopedia Hama Penyakit**: Database visual hama dan pengendaliannya.
- **Panduan Input Tani**: Informasi lengkap pupuk, pestisida, dan hormon.
- **Manajemen Tanah**: Panduan pH dan kesuburan tanah berkelanjutan.

### 🗺️ Fitur Lanjutan
- **AgriMap AI**: Pemetaan kesesuaian lahan berbasis geospasial.
- **Smart Planning**: Perencana siklus tanam dan panen otomatis.
- **Unified Dashboard**: Pusat kontrol rekomendasi pertanian terpadu.
- **Digital Library**: Pustaka dokumen dan regulasi pertanian.

---

## 🏗️ Arsitektur Teknologi

### Tech Stack

#### Backend & Framework
- ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) **Python 3.12**: Core logic & computation.
- ![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?logo=streamlit&logoColor=white) **Streamlit 1.32**: Interactive Web UI.
- **Pandas & NumPy**: High-performance data processing.
- **Plotly & Seaborn**: Advanced data visualization.

#### Machine Learning & AI
- **Scikit-learn**: Classical ML algorithms.
- **Google Gemini API**: Generative AI & NLP.
- **Roboflow**: Service-based Computer Vision.
- **SHAP**: Explainable AI framework.

#### Data Processing
- **Pillow**: Image processing.
- **OpenPyXL**: Excel data handling.

#### Deployment & DevOps
- **Streamlit Cloud**: Primary deployment platform.
- **GitHub**: Version control & CI/CD.
- **Docker**: Containerization (Optional).

### 📁 Struktur Direktori

```bash
streamlit_terbaru/
├── agrisensa_main.py             # Entry point aplikasi
├── agrisensa_tech/               # Modul AI & Teknologi
│   └── pages/
├── agrisensa_commodities/        # Modul Komoditas & Budidaya
│   └── pages/
├── agrisensa_biz/                # Modul Bisnis & Pasar
│   └── pages/
├── agrisensa_eco/                # Modul Ekosistem & Lingkungan
│   └── pages/
├── agrisensa_livestock/          # Modul Peternakan
│   └── pages/
├── data_analysis/                # Skrip & Notebook Analisis Data
├── services/                     # Layanan Terintegrasi
│   ├── gemini_service.py         # Integrasi LLM
│   ├── roboflow_service.py       # Integrasi Computer Vision
│   └── ...
├── utils/                        # Fungsi Utilitas
├── requirements.txt              # Dependensi Python
└── README.md                     # Dokumentasi Proyek
```

---

## 🚀 Instalasi & Memulai

1. **Clone Repository**
   ```bash
   git clone https://github.com/yandri918/streamlit_terbaru.git
   cd streamlit_terbaru
   ```

2. **Buat Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi**
   ```bash
   streamlit run agrisensa_main.py
   ```

---

## 🔌 API Documentation

AgriSensa menyediakan endpoint API untuk integrasi pihak ketiga.

### Crop Recommendation
Analisis kecocokan tanaman berdasarkan parameter tanah.
```http
POST /recommend-crop
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

### Fertilizer Recommendation
Rekomendasi pemupukan spesifik komoditas.
```http
POST /recommend-fertilizer
{
  "commodity": "padi",
  "area_sqm": 1000,
  "ph": 6.5
}
```

### Yield Prediction (XAI)
Prediksi hasil panen tingkat lanjut.
```http
POST /predict-yield-advanced
```

### Chatbot
Interaksi dengan AgriBot.
```http
POST /chat
```

### Market Prices
Mendapatkan data harga pasar real-time.
```http
GET /get-ticker-prices
```

---

## 🧪 Testing dan Kualitas Kode

Jalankan test suite untuk memastikan integritas sistem.

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=app tests/

# Run specific test module
pytest tests/testmlservice.py
```

---

## 🔐 Keamanan & Privasi

AgriSensa menerapkan standar keamanan industri:
- **JWT Authentication**: Untuk manajemen sesi pengguna yang aman.
- **Password Hashing**: Menggunakan Werkzeug security hash.
- **CORS Protection**: Melindungi dari akses lintas domain yang tidak sah.
- **Rate Limiting**: Mencegah penyalahgunaan API.
- **Input Validation**: Sanitasi data untuk mencegah injeksi.
- **SQL Injection Prevention**: Penggunaan ORM dan parameterized queries.

---

## 📊 Database Schema

Struktur basis data utama untuk menyimpan informasi pengguna dan rekomendasi.

| Tabel | Deskripsi |
|-------|-----------|
| `Users` | Menyimpan data profil, kredensial, dan preferensi pengguna. |
| `NPK Readings` | Riwayat pembacaan sensor atau input manual kondisi tanah. |
| `Recommendations` | Log rekomendasi yang diberikan sistem untuk analisis historis. |

---

## 🌍 Roadmap 2025

| Kuartal | Fokus Pengembangan |
|:---:|:---|
| **Q1** | Mobile App (React Native), Integrasi IoT Sensor, Multi-language Support, Weather Forecasting |
| **Q2** | Blockchain Supply Chain, Drone Imagery Analysis, Community Forum, Marketplace Integration |
| **Q3** | AI-Powered Crop Insurance, Precision Agriculture Tools (VRA), Farmer Networking Platform |

---

## 👤 Developer

<div align="center">

**Andriyanto**  
*Lead Developer & AI Engineer*

[![Email](https://img.shields.io/badge/Email-yandri918%40gmail.com-red?style=flat-square&logo=gmail)](mailto:yandri918@gmail.com)
[![GitHub](https://img.shields.io/badge/GitHub-@yandri918-181717?style=flat-square&logo=github)](https://github.com/yandri918)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Andriyanto%20NA-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/andriyanto-na-147492157)
[![Website](https://img.shields.io/badge/Website-mirai39.streamlit.app-violet?style=flat-square&logo=google-chrome)](https://mirai39.streamlit.app)

</div>

---

## ⭐ Dukungan

Jika AgriSensa bermanfaat bagi Anda, dukung kami dengan memberikan **Star** pada repository ini! 🌟

---

<div align="center">
  <sub>Dibuat dengan ❤️ untuk Petani Indonesia</sub>
</div>
