# Panduan Deployment ke Railway

Railway adalah pilihan yang sangat baik untuk aplikasi Python dengan model Machine Learning karena mendukung Docker container secara penuh dan tidak memiliki batasan ukuran seketat Vercel.

## Langkah-langkah Deployment

### 1. Persiapan Repository
Pastikan kode Anda sudah dipush ke GitHub. File penting yang digunakan Railway adalah:
- `Dockerfile`: Instruksi untuk membangun container aplikasi (sudah dikonfigurasi).
- `requirements.txt`: Daftar library Python.
- `run.py`: Entry point aplikasi.

### 2. Buat Project di Railway
1. Buka [Railway Dashboard](https://railway.app/).
2. Klik **"New Project"** > **"Deploy from GitHub repo"**.
3. Pilih repository `agrisensa-api`.
4. Klik **"Deploy Now"**.

### 3. Konfigurasi Environment Variables
Setelah project dibuat, masuk ke tab **"Variables"** dan tambahkan variable berikut:

| Variable | Value (Contoh) | Keterangan |
|----------|----------------|------------|
| `FLASK_ENV` | `production` | Mode produksi |
| `SECRET_KEY` | `(isi_random_string_panjang)` | Keamanan session Flask |
| `JWT_SECRET_KEY` | `(isi_random_string_panjang)` | Keamanan token JWT |
| `PORT` | `5000` | (Opsional) Railway biasanya otomatis inject ini |

**Database (PENTING):**
Karena Railway menggunakan sistem file ephemeral (data hilang saat restart), Anda **HARUS** menggunakan database eksternal.
1. Di dashboard Railway project Anda, klik **"New"** > **"Database"** > **"PostgreSQL"**.
2. Setelah database dibuat, Railway akan otomatis menambahkan variable `DATABASE_URL` ke service aplikasi Anda.
3. Aplikasi AgriSensa sudah dikonfigurasi untuk membaca `DATABASE_URL` ini.

### 4. Domain Publik
1. Masuk ke tab **"Settings"**.
2. Di bagian **"Networking"**, klik **"Generate Domain"** untuk mendapatkan URL publik (misal: `agrisensa-production.up.railway.app`).

## Troubleshooting

### Deployment Gagal?
- Cek tab **"Build Logs"**: Apakah ada error saat install library?
- Cek tab **"Deploy Logs"**: Apakah aplikasi crash saat start?

### Masalah Umum
- **Memory Limit**: Model ML (`yield_prediction_model.pkl` dll) memakan RAM cukup besar. Jika aplikasi crash dengan error "OOM" (Out of Memory), Anda mungkin perlu upgrade ke plan berbayar Railway atau mengoptimalkan model.
- **File Upload**: Ingat, file yang diupload ke folder `uploads/` akan hilang setiap kali Anda deploy ulang atau server restart. Gunakan layanan storage eksternal (seperti AWS S3, Cloudinary, atau Supabase Storage) untuk penyimpanan file permanen.

## Catatan Teknis
File `Dockerfile` telah diperbarui untuk:
- Menginstall dependency sistem (`libglib2.0-0`) yang dibutuhkan `opencv`.
- Menggunakan perintah start yang benar agar bisa membaca port dari Railway (`CMD gunicorn ...`).
