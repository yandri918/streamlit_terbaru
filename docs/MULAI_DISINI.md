# 🚀 MULAI DARI SINI - AGRISENSA API v2.0

## ⚡ CARA TERCEPAT (1 Klik)

### Windows:
Klik 2x file ini:
```
quick_start.bat
```

Script akan otomatis:
1. ✅ Install dependencies
2. ✅ Setup database
3. ✅ Create admin user
4. ✅ Start aplikasi

**Selesai!** Buka browser: `http://localhost:5000`

---

## 📝 CARA MANUAL (Step by Step)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized!')"
```

### 3. Run Application
```bash
python run.py
```

### 4. Buka Browser
```
http://localhost:5000
```

---

## 🔐 LOGIN CREDENTIALS

**Admin User:**
- Username: `admin`
- Password: `admin123`

**Test User:**
- Buat sendiri via: `http://localhost:5000/api/auth/register`

---

## 📚 DOKUMENTASI LENGKAP

- **Setup Detail:** Baca `SETUP_LOKAL.md`
- **API Documentation:** Baca `README_NEW.md`
- **Changelog:** Baca `CHANGELOG.md`

---

## 🧪 TEST API

### Health Check
```
http://localhost:5000/health
```

### API Info
```
http://localhost:5000/api/info
```

### Register User (POST)
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","email":"farmer1@example.com","password":"password123","full_name":"Petani Satu"}'
```

### Login (POST)
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","password":"password123"}'
```

---

## ❓ TROUBLESHOOTING

### Error: "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
python run.py --port 8000
```

### Error: "No such table"
```bash
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

---

## 📞 BUTUH BANTUAN?

1. Baca `SETUP_LOKAL.md` untuk panduan lengkap
2. Cek file `logs/agrisensa.log` untuk error details
3. Pastikan Python >= 3.8 terinstall

---

## ✅ CHECKLIST

- [ ] Python 3.8+ terinstall
- [ ] Dependencies terinstall
- [ ] Database terinisialisasi
- [ ] Aplikasi berjalan
- [ ] Browser bisa akses `http://localhost:5000`

---

**Selamat menggunakan AgriSensa API v2.0! 🌾**
