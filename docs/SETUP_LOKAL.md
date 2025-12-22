# 🚀 PANDUAN SETUP & MENJALANKAN AGRISENSA API DI LOKAL

Panduan lengkap step-by-step untuk menjalankan AgriSensa API v2.0 di komputer lokal Anda.

---

## 📋 PRASYARAT

Pastikan Anda sudah menginstall:
- ✅ Python 3.8 atau lebih baru
- ✅ pip (Python package manager)
- ✅ Git (optional, untuk version control)

Cek versi Python:
```bash
python --version
```

---

## 🔧 LANGKAH 1: INSTALL DEPENDENCIES

Buka terminal/command prompt di folder `agrisensa-api`, lalu jalankan:

```bash
pip install -r requirements.txt
```

**Catatan:** Jika ada error, coba gunakan:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Estimasi waktu:** 2-5 menit (tergantung koneksi internet)

---

## ⚙️ LANGKAH 2: VERIFIKASI FILE .ENV

File `.env` sudah dibuat otomatis. Anda bisa cek isinya:

```bash
# Windows
type .env

# Linux/Mac
cat .env
```

File `.env` berisi konfigurasi seperti:
- `SECRET_KEY` - Untuk Flask session
- `JWT_SECRET_KEY` - Untuk JWT authentication
- `DATABASE_URL` - Lokasi database SQLite

**Untuk production, ganti SECRET_KEY dengan yang lebih aman!**

---

## 🗄️ LANGKAH 3: INITIALIZE DATABASE

Jalankan perintah ini untuk membuat tabel database:

```bash
flask init-db
```

**Jika error "flask command not found", gunakan cara alternatif:**

```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized successfully!')"
```

**Output yang diharapkan:**
```
Database initialized successfully!
```

**Catatan:** Ini akan membuat file `agrisensa.db` di folder root project.

---

## 👤 LANGKAH 4: CREATE ADMIN USER (OPTIONAL)

Buat user admin untuk testing:

```bash
flask create-admin
```

**Jika error, gunakan cara alternatif:**

```bash
python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); admin = User(username='admin', email='admin@agrisensa.com', full_name='Administrator', role='admin'); admin.set_password('admin123'); db.session.add(admin); db.session.commit(); print('Admin user created: admin/admin123')"
```

**Credentials:**
- Username: `admin`
- Password: `admin123`

---

## 🚀 LANGKAH 5: JALANKAN APLIKASI

### Cara 1: Development Mode (Recommended untuk testing)

```bash
python run.py
```

### Cara 2: Flask Run

```bash
flask run
```

### Cara 3: Dengan Port Custom

```bash
python run.py --port 8000
```

**Output yang diharapkan:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

## ✅ LANGKAH 6: VERIFIKASI APLIKASI BERJALAN

### Test 1: Buka di Browser

Buka browser dan akses:
```
http://localhost:5000
```

Anda akan melihat halaman dashboard AgriSensa.

### Test 2: Health Check API

Buka di browser atau gunakan curl:
```
http://localhost:5000/health
```

**Response yang diharapkan:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-28T12:00:00"
}
```

### Test 3: API Info

```
http://localhost:5000/api/info
```

**Response yang diharapkan:**
```json
{
  "success": true,
  "data": {
    "name": "AgriSensa API",
    "version": "2.0.0",
    "description": "Smart Agriculture Platform API"
  }
}
```

---

## 🧪 LANGKAH 7: TEST API ENDPOINTS

### Test Register User

Buka terminal baru (jangan tutup yang menjalankan aplikasi), lalu:

**Windows (PowerShell):**
```powershell
$body = @{
    username = "farmer1"
    email = "farmer1@example.com"
    password = "password123"
    full_name = "Petani Satu"
    location = "Bandung"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/auth/register" -Method Post -Body $body -ContentType "application/json"
```

**Linux/Mac (curl):**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer1",
    "email": "farmer1@example.com",
    "password": "password123",
    "full_name": "Petani Satu",
    "location": "Bandung"
  }'
```

**Response yang diharapkan:**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "farmer1",
    "email": "farmer1@example.com"
  }
}
```

### Test Login

**Windows (PowerShell):**
```powershell
$body = @{
    username = "farmer1"
    password = "password123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:5000/api/auth/login" -Method Post -Body $body -ContentType "application/json"
$token = $response.access_token
Write-Host "Access Token: $token"
```

**Linux/Mac (curl):**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "farmer1",
    "password": "password123"
  }'
```

**Response yang diharapkan:**
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "username": "farmer1"
  }
}
```

**Simpan `access_token` untuk request berikutnya!**

### Test Protected Endpoint (Get Profile)

**Windows (PowerShell):**
```powershell
# Ganti YOUR_TOKEN dengan token dari login
$headers = @{
    "Authorization" = "Bearer YOUR_TOKEN"
}

Invoke-RestMethod -Uri "http://localhost:5000/api/auth/me" -Method Get -Headers $headers
```

**Linux/Mac (curl):**
```bash
# Ganti YOUR_TOKEN dengan token dari login
curl -X GET http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test NPK Analysis

**Windows (PowerShell):**
```powershell
$body = @{
    n = 80
    p = 40
    k = 40
    ph = 6.5
    commodity = "padi"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/analysis/npk" -Method Post -Body $body -ContentType "application/json"
```

**Linux/Mac (curl):**
```bash
curl -X POST http://localhost:5000/api/analysis/npk \
  -H "Content-Type: application/json" \
  -d '{
    "n": 80,
    "p": 40,
    "k": 40,
    "ph": 6.5,
    "commodity": "padi"
  }'
```

### Test Crop Recommendation (ML)

**Windows (PowerShell):**
```powershell
$body = @{
    N = 90
    P = 42
    K = 43
    temperature = 20.87
    humidity = 82.00
    ph = 6.50
    rainfall = 202.93
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/ml/recommend-crop" -Method Post -Body $body -ContentType "application/json"
```

**Linux/Mac (curl):**
```bash
curl -X POST http://localhost:5000/api/ml/recommend-crop \
  -H "Content-Type: application/json" \
  -d '{
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.87,
    "humidity": 82.00,
    "ph": 6.50,
    "rainfall": 202.93
  }'
```

---

## 📊 LANGKAH 8: MONITORING & LOGS

### Lihat Logs

Aplikasi akan membuat folder `logs/` dengan file log. Untuk melihat:

**Windows:**
```bash
type logs\agrisensa.log
```

**Linux/Mac:**
```bash
tail -f logs/agrisensa.log
```

### Monitor Database

Untuk melihat isi database SQLite:

1. Install SQLite Browser: https://sqlitebrowser.org/
2. Buka file `agrisensa.db`
3. Lihat tabel: `user`, `npk_reading`, `recommendation`, `crop`

---

## 🛑 STOP APLIKASI

Untuk menghentikan aplikasi, tekan:
```
CTRL + C
```

---

## 🔄 RESTART APLIKASI

Jika ada perubahan kode, restart aplikasi:

1. Stop aplikasi (CTRL + C)
2. Jalankan lagi: `python run.py`

**Catatan:** Perubahan di file Python memerlukan restart, tapi Flask debug mode akan auto-reload.

---

## ❌ TROUBLESHOOTING

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solusi:**
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"

**Solusi:** Port 5000 sudah digunakan. Gunakan port lain:
```bash
python run.py --port 8000
```

### Error: "No such table: user"

**Solusi:** Database belum diinisialisasi:
```bash
flask init-db
```

### Error: "SECRET_KEY not found"

**Solusi:** File `.env` tidak terbaca. Pastikan file `.env` ada di root folder.

### Error: "Unable to load model"

**Solusi:** File model ML (.pkl) tidak ditemukan. Pastikan file-file ini ada:
- `bwd_model.pkl`
- `recommendation_model.pkl`
- `crop_recommendation_model.pkl`
- `yield_prediction_model.pkl`
- `advanced_yield_model.pkl`
- `shap_explainer.pkl`

### Error: "Rate limit exceeded"

**Solusi:** Tunggu beberapa menit atau restart aplikasi.

---

## 📱 TESTING DENGAN POSTMAN

1. Download Postman: https://www.postman.com/downloads/
2. Import collection (buat file `AgriSensa.postman_collection.json`)
3. Set base URL: `http://localhost:5000`
4. Test semua endpoints

---

## 🎯 CHECKLIST SETUP BERHASIL

- [ ] Dependencies terinstall (`pip install -r requirements.txt`)
- [ ] File `.env` ada dan terisi
- [ ] Database terinisialisasi (`flask init-db`)
- [ ] Admin user terbuat (optional)
- [ ] Aplikasi berjalan (`python run.py`)
- [ ] Health check berhasil (`http://localhost:5000/health`)
- [ ] Register user berhasil
- [ ] Login berhasil dan dapat token
- [ ] Protected endpoint bisa diakses dengan token
- [ ] ML prediction berfungsi

---

## 🚀 NEXT STEPS

Setelah aplikasi berjalan:

1. **Explore API** - Test semua endpoint di README_NEW.md
2. **Baca Dokumentasi** - Lihat README_NEW.md untuk detail lengkap
3. **Customize** - Sesuaikan konfigurasi di `.env`
4. **Develop** - Tambahkan fitur baru sesuai kebutuhan
5. **Deploy** - Siap untuk production deployment

---

## 📞 BANTUAN

Jika masih ada masalah:

1. Cek file `logs/agrisensa.log` untuk error details
2. Pastikan semua dependencies terinstall
3. Pastikan Python version >= 3.8
4. Restart aplikasi dan coba lagi

---

**Selamat! AgriSensa API v2.0 sudah berjalan di lokal! 🎉**
