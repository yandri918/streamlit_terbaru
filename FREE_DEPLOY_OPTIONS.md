# Opsi Deployment Gratis untuk AgriSensa (Python + ML)

Karena Railway sekarang sistemnya berbayar (trial credit habis = bayar), berikut adalah alternatif **GRATIS** terbaik untuk aplikasi Python dengan Machine Learning:

| Platform | Status Gratis | Kelebihan | Kekurangan | Cocok Untuk AgriSensa? |
|----------|---------------|-----------|------------|------------------------|
| **1. Render** | ✅ **Free Forever** | - Setup mudah (connect GitHub)<br>- Support Docker<br>- Database PostgreSQL gratis (trial 30 hari) | - **Sleeps**: Mati jika tidak diakses 15 menit (loading awal lambat)<br>- RAM 512MB (mungkin mepet untuk ML) | ⭐⭐⭐ (Paling standar) |
| **2. Hugging Face Spaces** | ✅ **Free Forever** | - **Didesain untuk ML/AI**<br>- CPU cukup kuat (2 vCPU, 16GB RAM)<br>- Support Docker<br>- Tidak "tidur" secepat Render | - Public by default (bisa diprivate)<br>- Tidak ada database bawaan (harus connect ke luar) | ⭐⭐⭐⭐⭐ (Sangat direkomendasikan untuk App ML) |
| **3. Koyeb** | ✅ **Free Forever** | - Performa cepat<br>- Global CDN<br>- Support Docker | - Free tier terbatas (Nano instance)<br>- Database Postgres berbayar setelah trial | ⭐⭐⭐ |
| **4. PythonAnywhere** | ✅ **Free Forever** | - Stabil untuk Python dasar | - **Tidak support Docker** (susah install library sistem seperti `libglib` untuk OpenCV)<br>- Tidak bisa custom domain di free tier | ⭐ (Kurang cocok karena butuh Docker/OpenCV) |

## Rekomendasi Saya: **Hugging Face Spaces**

Mengapa?
1.  **Spesifikasi Tinggi**: Gratis 16GB RAM! Sangat cukup untuk model ML Anda yang berat.
2.  **Support Docker**: Kita bisa pakai `Dockerfile` yang sudah ada.
3.  **Stabil**: Jarang down/sleep dibanding Render free tier.

### Cara Deploy ke Hugging Face Spaces (Gratis)

1.  Daftar di [huggingface.co](https://huggingface.co/).
2.  Klik **New Space**.
3.  Pilih SDK: **Docker**.
4.  Upload file project Anda (bisa via git command yang sama).

Apakah Anda ingin mencoba **Hugging Face Spaces**? Saya bisa bantu buatkan panduannya.
