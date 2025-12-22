# Setup dan Deployment ke Hugging Face Spaces

Panduan lengkap deploy AgriSensa API ke Hugging Face Spaces dengan pendekatan yang robust dan production-ready.

## 🎯 Mengapa Hugging Face Spaces?

- **FREE 16GB RAM** dengan 2 vCPU
- **Docker Support** untuk aplikasi kompleks
- **Auto-deployment** dari Git
- **Built-in SSL/HTTPS**
- **Global CDN** untuk performa optimal

## 📋 Prasyarat

1. **Akun Hugging Face**
   - Daftar di [huggingface.co](https://huggingface.co/)
   - Generate Access Token di Settings → Access Tokens

2. **Git Repository**
   - Code sudah di-commit ke Git
   - `.gitignore` sudah dikonfigurasi
   - Tidak ada file sensitif (.env, dll)

## 🚀 Langkah 1: Buat Space Baru

1. Login ke Hugging Face
2. Klik foto profil (kanan atas) → **New Space**
3. Isi form:
   - **Space Name**: `agrisensa-api`
   - **License**: MIT
   - **Space SDK**: **Docker** (PENTING!)
   - **Space Hardware**: CPU Basic (Free - 2 vCPU, 16GB RAM)
   - **Visibility**: Public
4. Klik **Create Space**

## 📤 Langkah 2: Push Kode ke Space

### Via Git Command Line

```bash
# 1. Tambahkan remote Hugging Face (ganti USERNAME)
git remote add space https://huggingface.co/spaces/USERNAME/agrisensa-api

# 2. Push kode
git push space main
```

**Note**: Jika diminta password, gunakan **Access Token** (bukan password akun).

### Via Hugging Face Web UI

1. Zip folder project Anda
2. Upload via web interface Space
3. Extract di Space

## ⚙️ Langkah 3: Konfigurasi Environment Variables

Aplikasi ini sudah dikonfigurasi untuk berjalan **TANPA** environment variables wajib. Namun untuk fitur lengkap:

### Variables Opsional

Di halaman Space → **Settings** → **Variables and secrets**:

| Variable | Value | Keterangan |
|----------|-------|------------|
| `FLASK_ENV` | `production` | Mode environment |
| `SECRET_KEY` | `random-string-here` | Untuk session encryption |
| `JWT_SECRET_KEY` | `another-random-string` | Untuk JWT tokens |
| `DATABASE_URL` | `postgres://...` | Database PostgreSQL (opsional) |
| `ROBOFLOW_API_KEY` | `your-key-here` | Untuk disease detection advanced |

### Generate Random Keys

```bash
# Di terminal/PowerShell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 🗄️ Langkah 4: Database (Opsional)

Aplikasi **BISA BERJALAN TANPEL DATABASE**! Namun jika butuh persistence:

### Rekomendasi Database Gratis

1. **[Neon.tech](https://neon.tech)** (Recommended)
   - PostgreSQL Serverless
   - Free tier: 512MB storage, 1 project
   - Connection pooling built-in

2. **[Supabase](https://supabase.com)**
   - PostgreSQL + Real-time
   - Free tier: 500MB storage

### Setup Database

```bash
# 1. Daftar di Neon.tech
# 2. Buat database baru
# 3. Copy connection string
# 4. Paste di Space Settings → Secrets → DATABASE_URL
```

Format connection string:
```
postgresql://user:password@host.region.postgres.com/dbname
```

## 📝 Langkah 5: Verifikasi Deployment

### 1. Monitor Build Progress

- Di Space, lihat tab **Logs**
- Status **Building**: Docker sedang build (3-5 menit)
- Status **Running**: ✅ Berhasil!
- Status **Error**: ❌ Cek logs untuk troubleshooting

### 2. Test Endpoints

Setelah status **Running**, test URL:

```
https://USERNAME-agrisensa-api.hf.space/
```

Endpoints untuk test:
- `/` - Landing page
- `/health` - Health check
- `/api/info` - API information
- `/modules/bwd-analysis` - BWD Analysis module
- `/modules/dokter-tanaman` - Fertilizer module
- `/modules/price-intelligence` - Price module

## 🔧 Troubleshooting

### Build Error: "Port not found"

**Solusi**: Sudah fixed di Dockerfile, port 7860 (HF default)

### Runtime Error: Database Connection

**Solusi**: 
- Aplikasi dirancang untuk berjalan tanpa database
- Check logs: `⚠️ Database not available` adalah **NORMAL**
- Fitur yang butuh DB: NPK history (optional)

### ML Model Not Found

**Solusi**:
- Aplikasi punya fallback untuk semua ML predictions
- Check logs: `⚠️ Model not available, using fallback`
- Untuk ML models asli, upload files ke folder `app/ml_models/`

### Timeout Errors

**Solusi**:
- Gunicorn timeout sudah dinaikkan ke 120s
- External API calls punya timeout protection
- Market data menggunakan simulated data (fast)

### Memory Issues

**Solusi**:
- Free tier: 16GB RAM (sangat cukup)
- Jika OOM, reduce workers di Dockerfile:
  ```dockerfile
  CMD gunicorn run:app -b 0.0.0.0:${PORT:-7860} --workers 1 --timeout 120
  ```

## 📊 Monitoring

### Logs

```bash
# Di Space → Logs tab
# Real-time logs dari aplikasi
```

Look for:
- `✅ Database initialized successfully` - Database OK
- `⚠️ Database not available` - Normal jika tanpa DB
- `🚀 AgriSensa API started` - App started
- `⚠️ Model not available` - Using fallbacks (OK)

### Health Check

```bash
curl https://USERNAME-agrisensa-api.hf.space/health
```

Response:
```json
{
  "status": "healthy",
  "database": "available" | "unavailable",
  "timestamp": "2025-11-24T14:00:00"
}
```

## 🔄 Update Aplikasi

```bash
# 1. Edit code locally
# 2. Commit changes
git add .
git commit -m "Update features"

# 3. Push ke Hugging Face
git push space main

# Space akan auto-rebuild dan redeploy
```

## 🎉 Selesai!

Aplikasi AgriSensa API sudah berjalan di:
```
https://USERNAME-agrisensa-api.hf.space
```

**Features yang tersedia:**
- ✅ Landing page dengan semua modules
- ✅ BWD Analysis (leaf image analysis)
- ✅ Fertilizer Recommendation
- ✅ Price Intelligence (simulated data)
- ✅ Crop Recommendation (ML fallback)
- ✅ Pest Control Guide
- ✅ Fruit Guide
- ✅ Yield Prediction (ML fallback)

## 📚 Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Flask Production Deployment](https://flask.palletsprojects.com/en/3.0.x/deploying/)

## 🆘 Need Help?

Check:
1. Space **Logs** tab untuk errors
2. **Community** tab untuk tanya jawab
3. Hugging Face [Discord](https://discord.gg/huggingface)

---

**Happy Deploying! 🚀**
