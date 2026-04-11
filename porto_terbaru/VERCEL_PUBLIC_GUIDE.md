# Cara Membuat Portfolio Vercel Public

## Masalah
Portfolio masih meminta login saat diakses oleh orang lain.

## Penyebab
Project Vercel kemungkinan di-set sebagai **Private** atau memiliki **Deployment Protection** yang aktif.

## Solusi: Ubah ke Public

### Langkah 1: Buka Vercel Dashboard
1. Kunjungi: https://vercel.com/dashboard
2. Login dengan akun Anda (yandri918)

### Langkah 2: Pilih Project
1. Dari daftar project, klik **porto-terbaru**
2. Anda akan masuk ke halaman overview project

### Langkah 3: Masuk ke Settings
1. Di bagian atas halaman, klik tab **Settings**
2. Anda akan melihat menu settings di sidebar kiri

### Langkah 4: Nonaktifkan Deployment Protection
1. Di sidebar kiri, cari dan klik **"Deployment Protection"** atau **"Security"**
2. Anda akan melihat opsi:
   - **Vercel Authentication** (jika ini aktif, matikan!)
   - **Password Protection** (jika ini aktif, matikan!)
   - **Trusted IPs** (pastikan tidak ada IP yang di-restrict)

3. Pastikan semua protection **DISABLED** atau **OFF**

### Langkah 5: Cek General Settings
1. Klik **"General"** di sidebar
2. Scroll ke bagian **"Access Control"** atau **"Visibility"**
3. Pastikan di-set ke **"Public"** (bukan "Private")

### Langkah 6: Save & Test
1. Klik **Save** atau **Update** jika ada perubahan
2. Tunggu beberapa detik
3. Test dengan membuka di browser incognito:
   **https://porto-terbaru.vercel.app**

## URL Production Anda

Gunakan URL ini untuk LinkedIn dan sharing:
```
https://porto-terbaru.vercel.app
```

URL ini lebih pendek dan profesional!

## Alternatif: Redeploy dengan Flag Public

Jika cara di atas tidak berhasil, coba redeploy dengan command:

```bash
vercel --prod --public
```

## Verifikasi Berhasil

Setelah setting diubah, minta teman/keluarga untuk coba buka link di browser mereka (yang tidak pernah login Vercel). Jika langsung terbuka tanpa login, berarti sudah berhasil!

## Troubleshooting

**Jika masih minta login:**
1. Clear cache browser (Ctrl + Shift + Delete)
2. Coba di browser lain atau incognito mode
3. Tunggu 5-10 menit untuk propagasi DNS
4. Pastikan tidak ada typo di URL

**Jika tidak menemukan opsi Deployment Protection:**
- Mungkin Anda menggunakan Vercel Free Plan yang tidak punya fitur ini
- Dalam kasus ini, project seharusnya sudah public by default
- Masalahnya mungkin di browser cache atau session

## Kontak Support

Jika masih bermasalah, hubungi Vercel Support:
- https://vercel.com/support
- Atau via Twitter: @vercel
