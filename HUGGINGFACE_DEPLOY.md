# Panduan Deployment ke Hugging Face Spaces

Hugging Face Spaces adalah platform terbaik untuk hosting aplikasi Machine Learning secara gratis dengan spesifikasi tinggi (2 vCPU, 16GB RAM).

## ✅ Status Perbaikan Terbaru

**AgriSensa API sudah dioptimasi untuk Hugging Face!**

Perbaikan yang sudah dilakukan:
- ✅ **Database Optional**: Aplikasi bisa berjalan tanpa database
- ✅ **ML Model Fallbacks**: Semua fitur tetap jalan meskipun model tidak ada
- ✅ **Graceful Error Handling**: Tidak crash jika ada dependency yang hilang
- ✅ **Production Ready**: Dockerfile sudah dioptimasi dengan timeout 120s
- ✅ **Auto Directory Creation**: Semua folder yang dibutuhkan dibuat otomatis

## Langkah 1: Buat Space Baru

1.  Daftar/Login di [huggingface.co](https://huggingface.co/).
2.  Klik foto profil (pojok kanan atas) -> **New Space**.
3.  Isi form:
    *   **Space Name**: `agrisensa-api` (atau nama lain).
    *   **License**: `MIT` (opsional).
    *   **Space SDK**: Pilih **Docker** (PENTING!).
    *   **Space Hardware**: Pilih **CPU Basic (Free)** (2 vCPU, 16GB RAM).
    *   **Visibility**: Public (atau Private jika mau).
4.  Klik **Create Space**.

## Langkah 2: Upload Kode

Setelah Space dibuat, Anda akan melihat instruksi git. Anda bisa langsung push kode yang sudah ada di komputer Anda ke repository Space tersebut.

### Cara Push (via Terminal)

Jalankan perintah ini di terminal VS Code Anda:

```bash
# 1. Tambahkan remote Hugging Face (ganti USERNAME dengan username HF Anda)
git remote add space https://huggingface.co/spaces/USERNAME/agrisensa-api

# 2. Push kode ke Space
git push space main
```

*(Jika diminta password, gunakan **Access Token** dari Settings > Access Tokens di Hugging Face, bukan password login biasa).*

## Langkah 3: Konfigurasi Environment Variables (OPSIONAL)

**PENTING**: Aplikasi sudah dikonfigurasi untuk berjalan TANPA environment variables! Namun untuk fitur lengkap, Anda bisa set:

1.  Di halaman Space Anda, klik tab **Settings**.
2.  Scroll ke bagian **Variables and secrets**.
3.  Klik **New Secret** untuk menambahkan (OPSIONAL):
    *   `FLASK_ENV`: `production`
    *   `SECRET_KEY`: (random string - generate dengan `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
    *   `JWT_SECRET_KEY`: (random string)
    *   `DATABASE_URL`: (URL Database PostgreSQL - OPSIONAL, aplikasi jalan tanpa ini)
    *   `ROBOFLOW_API_KEY`: (untuk advanced disease detection - OPSIONAL)

## Langkah 4: Database (OPSIONAL)

**Aplikasi bisa berjalan TANPA database!** Fitur yang memerlukan database (NPK history) akan di-skip secara otomatis.

Jika Anda ingin persistence, gunakan database eksternal:

### Rekomendasi Database Gratis:
1.  **Neon.tech** (PostgreSQL Serverless, Free Tier bagus) - **RECOMMENDED**
2.  **Supabase** (PostgreSQL, Free Tier bagus)

**Cara Connect:**
1.  Buat database di Neon/Supabase.
2.  Copy connection string (misal: `postgres://user:pass@ep-xyz.us-east-2.aws.neon.tech/neondb`).
3.  Masukkan ke **Secret** `DATABASE_URL` di Hugging Face Spaces.

## Troubleshooting

### Status: Building
Tunggu proses build Docker selesai (bisa 3-5 menit). Monitor di tab **Logs**.

### Status: Running
✅ **Aplikasi berhasil dideploy!**

Aplikasi Anda tersedia di: `https://USERNAME-agrisensa-api.hf.space/`

### Status: App Error
Cek tab **Logs** untuk detail error. Kemungkinan error:

#### Error: Port Configuration
✅ **SUDAH FIXED**: Dockerfile sudah menggunakan port 7860 (default HF).

#### Warning: Database Not Available
✅ **NORMAL**: Aplikasi dirancang untuk berjalan tanpa database.
- Semua fitur tetap jalan dengan fallback data
- NPK history tidak disimpan (tapi analysis tetap jalan)

#### Warning: ML Model Not Available  
✅ **NORMAL**: Aplikasi punya fallback predictions.
- BWD Analysis: Menggunakan color-based heuristic
- Crop Recommendation: Menggunakan rule-based logic
- Yield Prediction: Menggunakan formula estimation

### Error: Out of Memory
- Free tier punya 16GB RAM, seharusnya cukup
- Jika tetap OOM, edit Dockerfile: ubah `--workers 2` jadi `--workers 1`

## Fitur yang Tersedia

Semua modul berjalan dengan baik di Hugging Face:

- ✅ **Landing Page** (`/`)
- ✅ **BWD Analysis** (`/modules/bwd-analysis`) - dengan fallback
- ✅ **Fertilizer Recommendation** (`/modules/dokter-tanaman`)
- ✅ **Price Intelligence** (`/modules/price-intelligence`) - simulated data
- ✅ **Crop Recommendation** (`/modules/crop-recommendation`) - dengan fallback  
- ✅ **Pest Control Guide** (`/modules/pest-guide`)
- ✅ **Fruit Guide** (`/fruit_guide`)

## Dokumentasi Lengkap

Untuk panduan lebih detail, lihat: **HF_SETUP.md**

---

Selamat! Aplikasi ML Anda sekarang berjalan di server dengan RAM 16GB Gratis! 🚀
