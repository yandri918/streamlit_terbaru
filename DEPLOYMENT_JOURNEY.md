# Walkthrough: Deployment AgriSensa API

Dokumen ini merangkum perjalanan deployment aplikasi AgriSensa API, dari eksplorasi awal hingga berhasil running di Hugging Face Spaces.

## 1. Eksplorasi Vercel
Awalnya kita mencoba deploy ke Vercel.
- **Tindakan**: Membuat `vercel.json` dan `.vercelignore`.
- **Hasil**: Konfigurasi berhasil dibuat, namun dibatalkan karena risiko **Serverless Function Size Limit (250MB)**. Aplikasi ini menggunakan library besar (`pandas`, `numpy`, `opencv`, `scikit-learn`) dan model ML yang kemungkinan besar akan melebihi batas tersebut.

## 2. Eksplorasi Railway
Kita beralih ke Railway sebagai alternatif yang lebih robust untuk Docker.
- **Tindakan**:
    - Membersihkan file konfigurasi Vercel.
    - Memperbaiki `Dockerfile` (mengubah `CMD` ke format shell agar bisa membaca `$PORT`).
    - Membuat panduan `RAILWAY_DEPLOY.md`.
    - Memperbaiki struktur Git (re-init di root folder project).
- **Hasil**: Siap deploy, namun dibatalkan karena user mencari opsi yang **100% Gratis** (Railway menggunakan sistem trial credit).

## 3. Deployment ke Hugging Face Spaces (Final) 🚀
Pilihan jatuh pada Hugging Face Spaces karena menyediakan **Free Tier 16GB RAM**, sangat cocok untuk aplikasi Machine Learning.

### Perubahan yang Dilakukan:
1.  **Dockerfile**:
    - Mengubah default port ke `7860` (Standar Hugging Face).
    - Menambahkan library sistem `libgl1` (dan `libglib2.0-0`) untuk mengatasi error `ImportError: libGL.so.1` dari OpenCV.
2.  **Metadata**:
    - Menambahkan YAML frontmatter di `README.md` (title, sdk: docker, dll) agar dikenali oleh Hugging Face.
3.  **Git**:
    - Menambahkan remote `huggingface`.
    - Melakukan push manual dengan Access Token.

### Status Akhir
✅ **Aplikasi Running** di Hugging Face Spaces.

### Langkah Selanjutnya (Penting!)
Agar aplikasi berfungsi sempurna, pastikan Anda telah mengatur **Environment Variables** di Settings Space Anda:
- `DATABASE_URL`: Koneksi ke database PostgreSQL eksternal (misal: Neon/Supabase).
- `SECRET_KEY`: Untuk keamanan Flask session.
- `JWT_SECRET_KEY`: Untuk token autentikasi.

Tanpa `DATABASE_URL`, fitur login dan penyimpanan data **akan error**.
