# 🚀 Panduan Deployment ke Hugging Face Spaces

Panduan ini akan membantu Anda men-deploy aplikasi Weather Prediction ke Hugging Face Spaces secara gratis.

## 📋 Prasyarat
- Akun Hugging Face (Daftar di [huggingface.co](https://huggingface.co/join))
- File-file proyek yang sudah disiapkan (sudah otomatis disiapkan di folder ini)

## 🛠️ Langkah-langkah Deployment

### 1. Buat Space Baru
1. Login ke Hugging Face
2. Klik foto profil > **New Space**
3. Isi detail berikut:
   - **Space name**: `weather-agrisensa` (atau nama lain yang unik)
   - **License**: `MIT`
   - **Select the Space SDK**: `Streamlit`
   - **Hardware**: `CPU basic (free)`
4. Klik **Create Space**

### 2. Upload File
Ada dua cara untuk mengupload file: **via Browser (Mudah)** atau **via Git (Advanced)**.

#### Opsi A: Via Browser (Drag & Drop)
1. Di halaman Space yang baru dibuat, klik menu **Files**
2. Klik tombol **Add file** > **Upload files**
3. Drag & drop file-file berikut dari folder `prediksi-cuaca`:
   - `app.py`
   - `requirements.txt`
   - `packages.txt`
   - `.python-version`
   - `.streamlit/config.toml` (Anda mungkin perlu membuat foldernya manual atau menggunakan Git)
   - Folder `pages/` (Drag semua isinya)
   - Folder `utils/` (Drag semua isinya)
   - `api.py` (Opsional jika tidak dipakai di Streamlit cloud)
4. **PENTING**:
   - Rename file `README_HF.md` menjadi `README.md` dan upload. (Ini akan menimpa README bawaan HF, yang mana bagus karena berisi konfigurasi metadata).
5. Klik **Commit changes to main**

#### Opsi B: Via Git (Disarankan)
Jika Anda sudah menginstall Git:
```bash
# 1. Clone repository space Anda (ganti username)
git clone https://huggingface.co/spaces/USERNAME/weather-agrisensa

# 2. Copy semua file proyek ke folder clonningan
# Pastikan untuk copy juga folder .streamlit

# 3. Rename README_HF.md menjadi README.md (timpa yang lama)
mv README_HF.md README.md

# 4. Push ke Hugging Face
git add .
git commit -m "Initial deploy"
git push
```

### 3. Tunggu Proses Build
1. Setelah upload, klik tab **App**
2. Anda akan melihat status **Building**
3. Proses ini memakan waktu 2-5 menit karena perlu menginstall `tensorflow-cpu` dan library lainnya.
4. Jika berhasil, status berubah menjadi **Running** dan aplikasi siap digunakan!

## ⚠️ Troubleshooting
- **Error "ModuleNotFound"**: Pastikan semua file di `requirements.txt` sudah benar.
- **Build Timeout**: Jika build terlalu lama, coba kurangi library berat. Kita sudah menggunakan `tensorflow-cpu` untuk menghemat memori.
- **Error "File not found"**: Pastikan struktur folder (`pages/`, `utils/`) ter-upload dengan benar.

## 📝 Catatan Penting
- File `README_HF.md` berisi "YAML Frontmatter" di bagian paling atas (di antara tanda `---`). Ini **WAJIB** ada di file `README.md` Hugging Face agar Space bisa berjalan. Jangan hapus bagian ini.
