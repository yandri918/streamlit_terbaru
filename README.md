
---

🌾 AgriSensa – AI‑Powered Smart Agriculture Platform for Indonesia
Empowering farmers with data, intelligence, and automation.

Demo • Dokumentasi • Roadmap • API

---

🚀 Ringkasan Eksekutif
AgriSensa adalah platform pertanian cerdas berbasis AI yang dirancang untuk meningkatkan produktivitas, efisiensi, dan keberlanjutan pertanian Indonesia. Dengan lebih dari 25+ modul AI, ML, dan Computer Vision, AgriSensa membantu petani mengambil keputusan berbasis data—mulai dari analisis tanah, rekomendasi tanaman, deteksi penyakit, hingga prediksi harga pasar.

Platform ini dibangun dengan arsitektur modern, modular, dan scalable, sehingga siap dikembangkan menjadi produk komersial, SaaS, atau solusi enterprise.

---

🎯 Nilai Utama (Why AgriSensa Matters)

🌱 Masalah di Industri Pertanian
- 40–60% kerugian hasil panen disebabkan penyakit & hama  
- Akses informasi pupuk, harga pasar, dan SOP budidaya masih terbatas  
- Petani tidak memiliki alat prediksi berbasis data  
- Minimnya integrasi teknologi AI dalam pertanian Indonesia  

🤖 Solusi AgriSensa
- Deteksi penyakit otomatis dengan Computer Vision  
- Rekomendasi tanaman berbasis NPK, pH, iklim, dan lokasi  
- Prediksi hasil panen & harga pasar dengan Machine Learning  
- Dashboard terpadu untuk keputusan cepat dan akurat  
- Basis pengetahuan pertanian terstruktur (20+ komoditas)  

📈 Dampak
- Mengurangi kerugian panen  
- Meningkatkan efisiensi pemupukan  
- Meningkatkan produktivitas  
- Memberikan akses data real‑time kepada petani  

---

✨ Fitur Utama

🤖 AI & Machine Learning
- AgriBot (Gemini AI) – Asisten pertanian cerdas  
- Crop Recommendation – Rekomendasi tanaman berbasis analisis tanah  
- Yield Prediction (XAI) – Prediksi hasil panen dengan SHAP  
- Price Trend Forecasting – Prediksi harga komoditas  
- Explainable AI – Model transparan untuk keputusan kritis  

🔬 Analisis & Diagnostik
- Dokter Tanaman AI – Deteksi penyakit via Roboflow  
- Analisis BWD – Deteksi penyakit padi  
- Diagnostik Gejala – Identifikasi hama & penyakit  
- Analisis NPK Manual – Evaluasi kesuburan tanah  

🧮 Kalkulator & Tools
- Kalkulator pupuk holistik  
- Konversi pupuk  
- Strategi penyemprotan cerdas  
- Rekomendasi pemupukan otomatis  

💰 Intelijen Pasar
- Harga komoditas real‑time  
- Prediksi tren harga  
- Katalog pupuk nasional  

📚 Basis Pengetahuan
- SOP budidaya 20+ komoditas  
- Ensiklopedia hama & penyakit  
- Panduan pupuk, pestisida, hormon tanaman  
- Info pH tanah & manajemen kesuburan  

🗺️ Fitur Lanjutan
- AgriMap AI – Rekomendasi tanaman berbasis lokasi  
- Perencana hasil panen AI  
- Dasbor rekomendasi terpadu  
- Pustaka dokumen pertanian  

---

🏗️ Arsitektur Teknologi

🧩 Tech Stack
Backend & Framework  
- Python 3.12  
- Streamlit 1.32  
- pandas, numpy  
- plotly, seaborn  

Machine Learning & AI  
- scikit‑learn  
- Google Gemini API  
- Roboflow (Computer Vision)  
- SHAP (Explainable AI)  

Data Processing  
- pandas, numpy  
- Pillow  
- openpyxl  

Deployment  
- Streamlit Cloud  
- GitHub  
- Docker (opsional)  

---

📁 Struktur Direktori
`
streamlit_terbaru/
├── agrisensa_main.py
├── agrisensa_tech/
│   └── pages/
├── agrisensa_commodities/
│   └── pages/
├── agrisensa_biz/
│   └── pages/
├── agrisensa_eco/
│   └── pages/
├── agrisensa_livestock/
│   └── pages/
├── data_analysis/
├── services/
│   ├── gemini_service.py
│   ├── roboflow_service.py
├── utils/
├── requirements.txt
└── README.md
`

---

🔌 API Documentation

Crop Recommendation
`
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
`

Fertilizer Recommendation
`
POST /recommend-fertilizer
{
  "commodity": "padi",
  "area_sqm": 1000,
  "ph": 6.5
}
`

Yield Prediction (XAI)
`
POST /predict-yield-advanced
`

Chatbot
`
POST /chat
`

Market Prices
`
GET /get-ticker-prices
`

---

🧪 Testing
`
pytest
pytest --cov=app tests/
pytest tests/testmlservice.py
`

---

🔐 Keamanan
- JWT Authentication  
- Password hashing (Werkzeug)  
- CORS protection  
- Rate limiting  
- Input validation  
- SQL injection prevention  

---

📊 Database Schema
Tabel utama:
- Users  
- NPK Readings  
- Recommendations  

(Detail skema tetap seperti versi kamu)

---

🌍 Roadmap 2025

Q1 2025
- Mobile App (React Native)  
- IoT sensor integration  
- Multi‑language support  
- Weather forecasting  

Q2 2025
- Blockchain supply chain  
- Drone imagery analysis  
- Community forum  
- Marketplace integration  

Q3 2025
- AI‑powered crop insurance  
- Precision agriculture tools  
- Farmer networking platform  

---

👤 Developer
Andriyanto  
Email: yandri918@gmail.com  
GitHub: @yandri918  
LinkedIn: Andriyanto NA  
Website: mirai39.streamlit.app  

---

⭐ Dukungan
Star repository ini untuk mendukung pengembangan AgriSensa.

---

❤️ Dibuat untuk Petani Indonesia

---