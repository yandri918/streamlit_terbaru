# Deployment Checklist untuk Render.com

## ✅ Persiapan Sebelum Deploy

### 1. File Konfigurasi
- [x] `render.yaml` - Konfigurasi deployment sudah ada
- [x] `Procfile` - File untuk gunicorn sudah dibuat
- [x] `requirements.txt` - Semua dependencies sudah terdaftar
- [x] `.gitignore` - File sensitif sudah di-exclude

### 2. Environment Variables yang Perlu Diset di Render Dashboard

**Wajib:**
- `ROBOFLOW_API_KEY` - API key untuk Roboflow (jika menggunakan fitur analisis penyakit lanjutan)

**Opsional:**
- `SENTRY_DSN` - Untuk error tracking (opsional)

### 3. Struktur Modul yang Sudah Terdaftar

#### Routes yang Tersedia:
1. **Main Routes** (`/`)
   - Home page
   - Dashboard
   - Semua modul HTML (23 modul)

2. **Analysis Routes** (`/api/analysis`)
   - `/bwd` - Analisis BWD (Blade Width Detection)
   - `/npk` - Analisis NPK tanah
   - `/npk/history` - History analisis NPK
   - `/disease-advanced` - Analisis penyakit dengan Roboflow AI

3. **Recommendation Routes** (`/api/recommendation`)
   - `/fertilizer` - Rekomendasi pupuk
   - `/calculate-fertilizer` - Kalkulasi dosis pupuk
   - `/integrated` - Rekomendasi terpadu
   - `/spraying` - Strategi penyemprotan
   - `/history` - History rekomendasi

4. **Knowledge Routes** (`/api/knowledge`)
   - `/crop/<commodity>` - Pengetahuan komoditas
   - `/guide/<commodity>` - Panduan komoditas
   - `/ph-info` - Informasi pH tanah
   - `/diagnostic-tree` - Pohon diagnostik penyakit
   - `/fertilizer-data` - Data komposisi pupuk

5. **Market Routes** (`/api/market`)
   - `/prices` - Harga pasar saat ini
   - `/ticker` - Ticker harga komoditas
   - `/historical` - Data harga historis

6. **ML Routes** (`/api/ml`)
   - `/recommend-crop` - Rekomendasi tanaman
   - `/predict-yield` - Prediksi hasil panen
   - `/predict-yield-advanced` - Prediksi hasil panen dengan XAI
   - `/generate-yield-plan` - Rencana hasil panen
   - `/calculate-fertilizer-bags` - Kalkulasi kebutuhan pupuk
   - `/predict-success` - Prediksi keberhasilan budidaya

7. **Auth Routes** (`/api/auth`)
   - `/register` - Registrasi user
   - `/login` - Login user
   - `/refresh` - Refresh token
   - `/me` - Info user saat ini
   - `/change-password` - Ubah password

8. **Legacy Routes** (`/`)
   - Semua endpoint legacy untuk backward compatibility

### 4. Services yang Terdaftar

- ✅ AnalysisService
- ✅ RecommendationService
- ✅ KnowledgeService
- ✅ MarketService
- ✅ MLService
- ✅ FruitService

### 5. Database Setup

Database akan dibuat otomatis saat aplikasi pertama kali dijalankan melalui `db.create_all()` di `app/__init__.py`.

Untuk inisialisasi manual:
```bash
flask init-db
```

### 6. ML Models

Pastikan semua file model ada di `app/ml_models/`:
- `bwd_model.pkl`
- `recommendation_model.pkl`
- `crop_recommendation_model.pkl`
- `yield_prediction_model.pkl`
- `advanced_yield_model.pkl`
- `shap_explainer.pkl`
- `success_model.pkl`

## 🚀 Langkah Deploy ke Render

1. **Push ke Git Repository**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Connect Repository ke Render**
   - Login ke Render dashboard
   - Pilih "New" > "Blueprint"
   - Connect repository GitHub/GitLab
   - Render akan membaca `render.yaml` secara otomatis

3. **Set Environment Variables**
   - Di Render dashboard, set `ROBOFLOW_API_KEY` (jika diperlukan)
   - Set `SENTRY_DSN` (opsional)

4. **Deploy**
   - Render akan otomatis build dan deploy
   - Monitor logs untuk memastikan tidak ada error

5. **Verifikasi**
   - Akses `/health` endpoint untuk cek status
   - Akses `/api/info` untuk info API
   - Test beberapa endpoint untuk memastikan berfungsi

## 📝 Catatan Penting

1. **Upload Folder**: Di Render, folder upload menggunakan `/tmp/` yang bersifat sementara. File yang diupload akan hilang saat service restart.

2. **Database**: PostgreSQL akan dibuat otomatis oleh Render berdasarkan `render.yaml`.

3. **Redis**: Redis akan dibuat otomatis untuk caching dan rate limiting.

4. **ML Models**: Pastikan semua model file di-commit ke repository (atau gunakan storage service untuk model besar).

5. **CORS**: Update `CORS_ORIGINS` di `render.yaml` dengan domain frontend yang akan digunakan.

## 🔧 Troubleshooting

### Error: Model tidak ditemukan
- Pastikan path `ML_MODELS_PATH` benar
- Pastikan semua file `.pkl` ada di repository

### Error: Database connection failed
- Pastikan `DATABASE_URL` sudah diset oleh Render
- Cek apakah PostgreSQL service sudah running

### Error: Redis connection failed
- Pastikan `REDIS_URL` sudah diset oleh Render
- Cek apakah Redis service sudah running

### Error: Module tidak berfungsi
- Cek logs di Render dashboard
- Pastikan semua dependencies terinstall
- Pastikan semua routes terdaftar di `app/__init__.py`

