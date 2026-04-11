# 🚀 Deployment Guide - Streamlit Cloud

## Langkah-langkah Deploy ke Streamlit Cloud

### 1️⃣ Persiapan Repository GitHub

#### Inisialisasi Git (jika belum)
```bash
cd c:\Users\yandr\OneDrive\Desktop\agrisensa-api\data_analyst
git init
```

#### Tambahkan semua file
```bash
git add .
git commit -m "Initial commit: Data Analyst Portfolio"
```

#### Buat repository di GitHub
1. Buka [github.com](https://github.com)
2. Klik tombol **"New repository"**
3. Nama repository: `data_analyst`
4. Deskripsi: "Professional Data Analyst Portfolio with Streamlit & Altair"
5. Pilih **Public**
6. **JANGAN** centang "Initialize with README" (karena sudah ada)
7. Klik **"Create repository"**

#### Push ke GitHub
```bash
git remote add origin https://github.com/yandri918/data_analyst.git
git branch -M main
git push -u origin main
```

---

### 2️⃣ Deploy ke Streamlit Cloud

#### Langkah Deploy
1. **Buka Streamlit Cloud**
   - Kunjungi: [share.streamlit.io](https://share.streamlit.io)
   - Login dengan akun GitHub Anda

2. **Create New App**
   - Klik tombol **"New app"**
   
3. **Konfigurasi App**
   - **Repository:** `yandri918/data_analyst`
   - **Branch:** `main`
   - **Main file path:** `Home.py`
   - **App URL (optional):** `data-analyst-portfolio` atau nama custom

4. **Advanced Settings (Optional)**
   - Python version: `3.11` (recommended)
   - Klik **"Deploy!"**

5. **Tunggu Deployment**
   - Proses biasanya 2-5 menit
   - Anda akan melihat log deployment
   - Setelah selesai, app akan otomatis terbuka

---

### 3️⃣ Verifikasi Deployment

#### Cek Halaman
- ✅ Home page loading dengan benar
- ✅ Sidebar navigation berfungsi
- ✅ Stock Price Analysis page menampilkan visualisasi
- ✅ Credit Card Fraud page menampilkan data

#### Troubleshooting Umum

**Problem: Data tidak ditemukan**
```
Error: Failed to load stock data
```
**Solusi:** Pastikan file CSV ada di folder `data/` dan sudah di-commit ke GitHub

**Problem: Module not found**
```
ModuleNotFoundError: No module named 'altair'
```
**Solusi:** Pastikan `requirements.txt` sudah lengkap dan di-commit

**Problem: Memory limit exceeded**
```
MemoryError
```
**Solusi:** Kurangi sample size di Credit Card Fraud page (sudah ada slider)

---

### 4️⃣ Update App (Setelah Deploy)

Setiap kali Anda update code:

```bash
git add .
git commit -m "Update: deskripsi perubahan"
git push
```

Streamlit Cloud akan **otomatis re-deploy** dalam beberapa menit.

---

### 5️⃣ Monitoring & Management

#### Streamlit Cloud Dashboard
- **Logs:** Lihat error dan debug info
- **Settings:** Ubah konfigurasi app
- **Reboot:** Restart app jika ada masalah
- **Delete:** Hapus app

#### Share Your App
Setelah deploy, Anda akan mendapat URL seperti:
```
https://data-analyst-portfolio.streamlit.app
```

Share URL ini di:
- LinkedIn profile
- Resume/CV
- GitHub README
- Portfolio website

---

### 6️⃣ Optimasi untuk Production

#### Performance Tips
1. **Caching:** Sudah diimplementasi dengan `@st.cache_data`
2. **Sampling:** Credit card data menggunakan sampling (default 50K rows)
3. **Lazy Loading:** Data dimuat hanya saat halaman dibuka

#### Resource Limits (Streamlit Cloud Free Tier)
- **Memory:** 1 GB RAM
- **CPU:** Shared
- **Storage:** 1 GB
- **Apps:** 3 public apps

Jika perlu lebih, upgrade ke Streamlit Cloud Pro.

---

### 7️⃣ Custom Domain (Optional)

Untuk menggunakan domain custom:
1. Upgrade ke Streamlit Cloud Pro
2. Tambahkan CNAME record di DNS provider
3. Configure di Streamlit Cloud settings

---

## 📋 Pre-Deployment Checklist

Sebelum deploy, pastikan:

- [x] ✅ Semua file sudah dibuat
- [x] ✅ Data files (CSV) sudah di-copy ke folder `data/`
- [x] ✅ `requirements.txt` sudah lengkap
- [x] ✅ `.gitignore` sudah dibuat
- [x] ✅ README.md sudah informatif
- [ ] ⬜ Git repository sudah diinisialisasi
- [ ] ⬜ Code sudah di-push ke GitHub
- [ ] ⬜ App sudah di-deploy ke Streamlit Cloud

---

## 🎯 Next Steps

Setelah deployment berhasil:

1. **Test thoroughly:** Cek semua fitur dan visualisasi
2. **Share:** Bagikan link portfolio Anda
3. **Monitor:** Pantau logs untuk error
4. **Iterate:** Update dan improve berdasarkan feedback

---

## 📞 Support

Jika ada masalah:
- **Streamlit Docs:** [docs.streamlit.io](https://docs.streamlit.io)
- **Community Forum:** [discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues:** Report bugs di repository

---

**Good luck with your deployment! 🚀**
