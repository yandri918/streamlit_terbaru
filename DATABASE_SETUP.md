# Panduan Setup Database untuk AgriSensa

Aplikasi AgriSensa membutuhkan database PostgreSQL untuk menyimpan data pengguna, hasil analisis, dan history NPK.

## Pilihan 1: Neon.tech (Rekomendasi) ⭐

**Mengapa Neon?**
- PostgreSQL Serverless (auto-scale)
- Free tier: 0.5GB storage, 3GB data transfer/bulan
- Setup super cepat (1 menit)
- Tidak perlu kartu kredit

### Langkah-langkah:

1. **Buat Akun**
   - Buka [neon.tech](https://neon.tech/)
   - Klik "Sign Up" (bisa pakai GitHub)

2. **Buat Database**
   - Setelah login, klik "Create a project"
   - Pilih region terdekat (Singapore/Tokyo untuk Indonesia)
   - Biarkan nama default atau ganti sesuai keinginan
   - Klik "Create Project"

3. **Copy Connection String**
   - Setelah project dibuat, Anda akan melihat "Connection string"
   - Pilih tab **"Pooled connection"** (lebih stabil untuk web app)
   - Copy string yang mirip seperti ini:
   ```
   postgresql://username:password@ep-xyz-123.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   ```

4. **Tambahkan ke Hugging Face**
   - Buka Space Anda: https://huggingface.co/spaces/yandri918/agrisensa-api
   - Klik tab **"Settings"**
   - Scroll ke bagian **"Variables and secrets"**
   - Klik **"New secret"**
   - Name: `DATABASE_URL`
   - Value: (paste connection string dari Neon)
   - Klik "Save"

5. **Restart Space**
   - Kembali ke tab "App"
   - Space akan otomatis restart dan connect ke database

---

## Pilihan 2: Supabase

**Mengapa Supabase?**
- PostgreSQL + Dashboard UI yang bagus
- Free tier: 500MB storage
- Bonus: Bisa pakai untuk storage file juga

### Langkah-langkah:

1. **Buat Akun**
   - Buka [supabase.com](https://supabase.com/)
   - Klik "Start your project"

2. **Buat Project**
   - Klik "New Project"
   - Isi nama project: `agrisensa`
   - **PENTING**: Catat password database yang Anda buat!
   - Pilih region: Southeast Asia (Singapore)
   - Klik "Create new project" (tunggu 1-2 menit)

3. **Ambil Connection String**
   - Setelah project ready, klik ikon "Settings" (gear) di sidebar
   - Pilih "Database"
   - Scroll ke "Connection string"
   - Pilih tab **"URI"**
   - Copy string, lalu ganti `[YOUR-PASSWORD]` dengan password yang tadi Anda buat
   - Contoh hasil:
   ```
   postgresql://postgres:password123@db.xyz.supabase.co:5432/postgres
   ```

4. **Tambahkan ke Hugging Face**
   - (Sama seperti langkah 4-5 di Neon)

---

## Verifikasi Koneksi

Setelah menambahkan `DATABASE_URL` dan Space restart, cek logs:

1. Di halaman Space, klik tab **"Logs"**
2. Cari baris yang mirip:
   ```
   AgriSensa API started in production mode
   ```
3. Jika ada error `connection refused` atau `authentication failed`, berarti:
   - Connection string salah (cek lagi)
   - Password salah (regenerate di Neon/Supabase)

## Inisialisasi Tabel Database

Aplikasi Anda sudah punya kode untuk auto-create tables (`db.create_all()`), tapi jika ingin manual:

```bash
# Jalankan di terminal lokal (opsional)
flask init-db
```

Atau biarkan otomatis saat aplikasi pertama kali jalan.

---

## Troubleshooting

**Error: "SSL connection required"**
- Pastikan connection string ada `?sslmode=require` di akhir

**Error: "Too many connections"**
- Gunakan "Pooled connection" di Neon (bukan Direct)

**Database kosong terus**
- Cek apakah `DATABASE_URL` sudah benar-benar tersimpan di Secrets (bukan Variables biasa)
