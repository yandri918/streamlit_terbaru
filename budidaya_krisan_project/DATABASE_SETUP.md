# 🗄️ Panduan Konfigurasi Database Penyimpanan — Budidaya Krisan Pro

Sistem ini mendukung **Dual-Engine Database**:
1. **SQLite (Lokal)**: Digunakan secara default untuk development offline di laptop/komputer tanpa perlu instalasi database server.
2. **PostgreSQL Cloud (Produksi)**: Digunakan untuk deployment di **Railway**, **Supabase**, atau **Neon** agar data tersimpan permanen dan tidak hilang saat server restart.

---

## 🚀 Opsi 1: Setup di Railway (Otomatis & Direkomendasikan)

Jika Anda mendeploy proyek ini ke [Railway.app](https://railway.app):

1. **Buat Database PostgreSQL di Railway**:
   - Di dashboard Railway project Anda, klik **+ New** > **Database** > **Add PostgreSQL**.
2. **Sambungkan ke Aplikasi Web**:
   - Di tab aplikasi Anda (service Python/FastAPI), buka menu **Variables**.
   - Tambahkan variabel:
     ```env
     DATABASE_URL = ${{Postgres.DATABASE_URL}}
     ```
   - Railway akan otomatis menginjeksi URL koneksi PostgreSQL ke aplikasi.
3. **Inisialisasi Otomatis**:
   - Saat aplikasi pertama kali booting di Railway, sistem secara otomatis mengeksekusi skema `database/01_postgres_schema.sql` dan data awal `database/02_postgres_seeds.sql`.

---

## ⚡ Opsi 2: Setup di Supabase (Gratis & Cepat)

Jika menggunakan [Supabase](https://supabase.com):

1. Buat project baru di Supabase.
2. Masuk ke **Project Settings** > **Database** > bagian **Connection string** > pilih **URI**.
3. Salin connection string tersebut, misalnya:
   ```env
   DATABASE_URL=postgresql://postgres.xxxx:[YOUR-PASSWORD]@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres
   ```
4. Masukkan string tersebut ke file `.env` di komputer lokal atau di environment variables hosting Anda.

---

## 🔄 Migrasi Data dari SQLite Lokal ke PostgreSQL Cloud

Jika Anda sudah memiliki data catatan pertumbuhan di laptop (`krisan.db`) dan ingin menyalinnya ke Cloud:

Jalankan perintah berikut di terminal:

```bash
python utils/migrate_to_postgres.py "postgresql://postgres:password@host:port/database"
```

Skrip ini akan:
- ✅ Memeriksa koneksi ke PostgreSQL Cloud
- ✅ Menerapkan skema tabel (varieties, batches, growth, harvest, cost journal)
- ✅ Menyalin semua data yang ada di `krisan.db` ke Cloud tanpa duplikasi (`ON CONFLICT DO NOTHING`)

---

## 📋 Struktur Tabel Penyimpanan

| No | Nama Tabel | Deskripsi |
|---|---|---|
| 1 | `varieties` | Katalog master varietas krisan spray Jepang (Fiji, Reagent, Princess, Benson) |
| 2 | `cultivation_batches` | Siklus tanam, nomor house, jumlah bedengan, varietas, tanggal tanam & panen |
| 3 | `growth_records` | Monitoring mingguan (tinggi tanaman, jumlah daun, diameter batang, cabang, cuaca, AI health score & grade) |
| 4 | `harvest_records` | Rekapitulasi hasil panen (tangkai, grade, pendapatan kotor, biaya, laba bersih, ROI, BEP) |
| 5 | `harvest_detail_grades` | Rincian ikat-based grading per grade (Grade 60, 80, 100, 120, 160, R-80 s.d. R-200) |
| 6 | `cost_journal` | Jurnal pencatatan pengeluaran harian operasional budidaya |
| 7 | `webhook_config` | Konfigurasi notifikasi WhatsApp / Webhook |

---

## 🔍 Cek Status Database

Anda dapat melihat status database yang sedang aktif melalui endpoint:
- URL: `http://localhost:8000/health` (atau domain Railway Anda)
- Response JSON:
  ```json
  {
    "status": "healthy",
    "service": "Budidaya Krisan Pro",
    "version": "2.0.0",
    "database": {
      "engine": "postgresql",
      "type": "Cloud PostgreSQL (Railway / Supabase / Neon)",
      "url": "postgresql://postgres:****@junction.proxy.rlwy.net:12345/railway",
      "status": "connected"
    }
  }
  ```
