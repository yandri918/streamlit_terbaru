# Panduan Deployment: AgriSensa Ecosystem (Hybrid) ☁️

Karena Anda memilih **OPSI A (`streamlit_terbaru`)**, berikut adalah konfigurasi yang benar.

## Penting Dipahami ⚠️

*   Repository **`streamlit_terbaru`** hanya berisi **Aplikasi Utama (Hub)**.
*   Repository **`agrisensa-streamlit`** berisi **Semua Aplikasi (Hub + Satelit)**.

Jadi, strategi deployment Anda adalah campuran (Hybrid):

### 1. Deploy Main Hub (Dari `streamlit_terbaru`)
Ini yang sudah Anda pilih.
*   **Repo**: `yandri918/streamlit_terbaru`
*   **Main file path**: `Home.py`
*   **URL Hasil**: (Misal) `https://agrisensa-hub-baru.streamlit.app`

### 2. Deploy Aplikasi Satelit (WAJIB dari `agrisensa-streamlit`)
Karena file satelit tidak ada di repo `streamlit_terbaru`, Anda harus mengambilnya dari repo asli.

Lakukan ini untuk Commodities, Tech, Biz, Eco, dan Livestock:

1.  Buat App Baru di Streamlit Cloud.
2.  Pilih Repo: **`yandri918/agrisensa-streamlit`** (Bukan `streamlit_terbaru`!).
3.  Isi **Main file path** sesuai nama foldernya:
    *   **Commodities** ➡️ `agrisensa_commodities/Home.py`
    *   **Tech** ➡️ `agrisensa_tech/Home.py`
    *   **Biz** ➡️ `agrisensa_biz/Home.py`
    *   **Eco** ➡️ `agrisensa_eco/Home.py`
    *   **Livestock** ➡️ `agrisensa_livestock/Home.py`

### 3. Hubungkan (Secrets)
Setelah semua satelit online:
1.  Buka **Settings -> Secrets** di Aplikasi **Main Hub** (`streamlit_terbaru`).
2.  Masukkan link aplikasi satelit tadi:

```toml
[satellites]
commodities = "https://agrisensa-commodities.streamlit.app"
tech = "https://agrisensa-tech.streamlit.app"
# ... dst
```

Selamat! Anda menggunakan repo `streamlit_terbaru` untuk Main Hub yang bersih, tapi tetap bisa mengakses fitur satelit dari repo asli.
