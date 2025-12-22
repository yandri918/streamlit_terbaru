# Panduan Deployment ke Vercel

Aplikasi AgriSensa API **bisa** dideploy ke Vercel menggunakan konfigurasi Python Serverless Function. Namun, ada beberapa hal penting yang perlu diperhatikan karena batasan platform Vercel.

## 1. Konfigurasi yang Telah Ditambahkan

File `vercel.json` telah ditambahkan ke root project:
```json
{
    "version": 2,
    "builds": [
        {
            "src": "run.py",
            "use": "@vercel/python"
        }
    ],
    "routes": [
        {
            "src": "/(.*)",
            "dest": "run.py"
        }
    ]
}
```

## 2. Batasan Penting (WARNING)

### Ukuran Aplikasi (Size Limit)
Vercel memiliki batasan ukuran Serverless Function (maksimal 250MB unzipped).
Aplikasi ini menggunakan library besar seperti:
- `opencv-python-headless` (~100MB+)
- `pandas` & `numpy` (~100MB+)
- `scikit-learn`
- Model ML (`yield_prediction_model.pkl` ~36MB)

**Risiko:** Deployment mungkin gagal jika total ukuran melebihi 250MB. Jika ini terjadi, pertimbangkan untuk:
1. Menggunakan **Render** (seperti sebelumnya) atau **Railway** yang lebih cocok untuk aplikasi Python/ML berat.
2. Mengurangi dependensi jika memungkinkan.

### File System Read-Only
Vercel bersifat *serverless* dan *ephemeral*.
- Anda **TIDAK BISA** menyimpan file upload secara permanen di folder `uploads/`.
- File yang diupload akan hilang setelah proses selesai.
- Untuk penyimpanan sementara (misal saat memproses gambar), aplikasi harus menggunakan folder `/tmp`.

## 3. Environment Variables

Pastikan Anda mengatur Environment Variables berikut di dashboard Vercel (Settings > Environment Variables):

| Key | Value (Contoh) | Keterangan |
|-----|----------------|------------|
| `FLASK_ENV` | `production` | Mode produksi |
| `SECRET_KEY` | `(generate_random_string)` | Kunci rahasia Flask |
| `JWT_SECRET_KEY` | `(generate_random_string)` | Kunci JWT |
| `UPLOAD_FOLDER` | `/tmp/uploads` | **Wajib** arahkan ke /tmp |
| `TEMP_IMAGE_FOLDER` | `/tmp/temp_images` | **Wajib** arahkan ke /tmp |
| `LOG_FILE` | `/tmp/agrisensa.log` | **Wajib** arahkan ke /tmp atau disable |
| `DATABASE_URL` | `postgresql://...` | URL Database (gunakan Supabase/Neon/dll) |

> **Catatan:** SQLite (`agrisensa.db`) tidak akan berfungsi permanen di Vercel. Anda **HARUS** menggunakan database eksternal seperti PostgreSQL (bisa pakai Supabase, Neon, atau Vercel Postgres).

## 4. Cara Deploy

### Opsi A: Via GitHub (Direkomendasikan)
1. Push kode ke repository GitHub.
2. Buka dashboard Vercel -> "Add New..." -> "Project".
3. Import repository GitHub Anda.
4. Masukkan Environment Variables di bagian konfigurasi.
5. Klik "Deploy".

### Opsi B: Via Vercel CLI
1. Install Vercel CLI: `npm i -g vercel`
2. Login: `vercel login`
3. Jalankan perintah di root folder:
   ```bash
   vercel
   ```
4. Ikuti instruksi di terminal.
