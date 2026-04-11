# 🚀 Panduan Deploy ke Streamlit Cloud

## Langkah-Langkah Deploy

### 1. Akses Streamlit Cloud
- Buka [share.streamlit.io](https://share.streamlit.io)
- Login dengan akun GitHub Anda

### 2. Deploy Aplikasi Baru
1. Klik tombol **"New app"**
2. Isi form deployment:
   - **Repository**: `yandri918/pajak-dan-produksi`
   - **Branch**: `main`
   - **Main file path**: `app.py`
3. Klik **"Deploy!"**

### 3. Tunggu Proses Deployment
- Streamlit Cloud akan otomatis:
  - Clone repository
  - Install dependencies dari `requirements.txt`
  - Menjalankan aplikasi
- Proses biasanya memakan waktu 2-5 menit

### 4. Aplikasi Siap!
- URL aplikasi: `https://[nama-app-anda].streamlit.app`
- Aplikasi akan auto-restart jika ada push baru ke repository

## ⚙️ Konfigurasi (Opsional)

### Custom Domain
Jika ingin menggunakan domain sendiri:
1. Buka Settings di Streamlit Cloud
2. Pilih "Custom subdomain"
3. Masukkan nama subdomain yang diinginkan

### Secrets Management
Jika perlu menyimpan API keys atau credentials:
1. Buka app settings
2. Pilih "Secrets"
3. Tambahkan secrets dalam format TOML

## 🔧 Troubleshooting

### Error: "installer returned a non-zero exit code"
✅ **Sudah diperbaiki!** Requirements.txt telah diupdate dengan versi fleksibel.

### App tidak muncul setelah deploy
- Cek logs di Streamlit Cloud dashboard
- Pastikan `app.py` ada di root repository
- Pastikan semua dependencies terinstall

### Performa lambat
- Streamlit Cloud free tier memiliki resource terbatas
- Upgrade ke paid plan untuk performa lebih baik

## 📱 Fitur Aplikasi

### Kalkulator Pajak
- **PPh 21**: Pajak karyawan dengan PTKP
- **PPh 23**: Pajak potong pungut
- **PPN**: Pajak pertambahan nilai 11%/12%
- **PPh Badan**: Pajak perusahaan dengan fasilitas UMKM

### Manajemen Biaya Produksi
- Input biaya bahan baku, tenaga kerja, overhead
- Analisis biaya per unit
- Rekomendasi harga jual
- Visualisasi breakdown biaya

## 🔄 Update Aplikasi

Untuk update aplikasi:
1. Edit file di local
2. Commit changes: `git commit -m "Update message"`
3. Push ke GitHub: `git push origin main`
4. Streamlit Cloud akan auto-deploy update

## 📞 Support

Jika ada masalah:
- Cek [Streamlit Community Forum](https://discuss.streamlit.io)
- Lihat [Streamlit Documentation](https://docs.streamlit.io)
- Review logs di Streamlit Cloud dashboard

---

**Repository**: https://github.com/yandri918/pajak-dan-produksi  
**Status**: ✅ Ready for Deployment  
**Last Update**: February 8, 2026
