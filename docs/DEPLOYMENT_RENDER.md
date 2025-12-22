# Deployment Guide untuk Render

## Persiapan Sebelum Deploy

### 1. Persiapkan Repository
Pastikan semua file berikut sudah ada di repository:
- `render.yaml` - Konfigurasi Render
- `requirements.txt` - Dependencies Python
- `.env.example` - Template environment variables
- `.gitignore` - File yang di-ignore

### 2. Upload ML Models (Opsional)
Jika Anda memiliki model ML yang sudah dilatih, upload ke folder `app/ml_models/`:
- `bwd_model.pkl`
- `recommendation_model.pkl`
- `crop_recommendation_model.pkl`
- `yield_prediction_model.pkl`
- `advanced_yield_model.pkl`
- `shap_explainer.pkl`

## Langkah Deploy ke Render

### 1. Buat Akun Render
- Kunjungi [render.com](https://render.com)
- Daftar akun baru atau login

### 2. Connect Repository
- Klik "New" → "Blueprint"
- Connect ke GitHub repository Anda
- Pilih repository `agrisensa-api`

### 3. Konfigurasi Services
Render akan otomatis mendeteksi `render.yaml` dan membuat:
- **Web Service**: `agrisensa-api`
- **PostgreSQL Database**: `agrisensa-db`
- **Redis**: `agrisensa-redis`

### 4. Set Environment Variables
Di dashboard Render, set environment variables berikut sebagai "Secret":

**Wajib:**
- `SECRET_KEY` - Generate random string
- `JWT_SECRET_KEY` - Generate random string

**Opsional:**
- `SENTRY_DSN` - Untuk error tracking
- `ROBOFLOW_API_KEY` - Jika menggunakan Roboflow API
- `CORS_ORIGINS` - Update dengan domain frontend Anda

### 5. Deploy
- Klik "Create Blueprint"
- Tunggu proses build dan deploy selesai
- URL aplikasi akan tersedia di dashboard

## Konfigurasi Tambahan

### Database Migration
Setelah deploy pertama kali, jalankan migration:
```bash
# Via Render Shell atau SSH
flask db upgrade
```

### Health Check
Test deployment dengan endpoint:
```
GET https://your-app-name.onrender.com/api/status
```

### Monitoring
- Monitor logs di Render dashboard
- Setup alerts untuk downtime
- Monitor resource usage (CPU, Memory, Database)

## Troubleshooting

### Common Issues:

1. **Build Failures:**
   - Pastikan semua dependencies di `requirements.txt`
   - Check Python version compatibility

2. **Database Connection:**
   - Pastikan `DATABASE_URL` tersedia
   - Run migrations setelah deploy

3. **ML Models Not Found:**
   - Upload model files ke `app/ml_models/`
   - Pastikan path di config benar

4. **CORS Issues:**
   - Update `CORS_ORIGINS` dengan domain frontend
   - Pastikan HTTPS enabled

### Logs & Debugging:
- Check logs di Render dashboard
- Gunakan `/api/status` untuk health check
- Test endpoints dengan Postman atau curl

## Environment Variables Lengkap

Copy dari `.env.example` dan sesuaikan dengan environment Render.

## Cost Estimation
- **Web Service**: ~$7/month (starter plan)
- **PostgreSQL**: ~$7/month (starter plan)
- **Redis**: Free tier available

## Security Notes
- Jangan commit `.env` files
- Gunakan strong secrets untuk JWT dan database
- Enable HTTPS (otomatis di Render)
- Regular backup database
