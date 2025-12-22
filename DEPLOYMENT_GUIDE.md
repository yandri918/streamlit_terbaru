# Panduan Deployment: AgriSensa V4 (Final) ☁️🚀

**KABAR BAIK:** Semua file (Hub & Satelit) sekarang sudah ada di repository **`streamlit_terbaru`**!

Anda tidak perlu bingung lagi. Cukup gunakan **1 Repository** untuk semuanya.

---

## Langkah Deployment (Untuk 6 Aplikasi)

Ulangi langkah ini 6 kali (untuk Hub, Commodities, Tech, dll).

1.  **Repo**: `yandri918/streamlit_terbaru`
2.  **Branch**: `main`
3.  **Main file path**: (Isi sesuai tabel dibawah)

| Aplikasi | **Main file path** (Ketik manual!) |
| :--- | :--- |
| **1. Main Hub** | `agrisensa_streamlit/Home.py` |
| **2. Commodities** | `agrisensa_commodities/Home.py` |
| **3. Tech** | `agrisensa_tech/Home.py` |
| **4. Biz** | `agrisensa_biz/Home.py` |
| **5. Eco** | `agrisensa_eco/Home.py` |
| **6. Livestock** | `agrisensa_livestock/Home.py` |

> **Catatan:** Jika Anda sebelumnya men-deploy Main Hub dengan path `Home.py` saja, kemungkinan itu akan error sekarang karena filenya sudah masuk ke folder `agrisensa_streamlit`. Silakan update path-nya atau buat app baru.

---

## Menghubungkan Satelit (Secrets)

Setelah semua online, update Secrets di **Main Hub**:

```toml
[satellites]
commodities = "https://budidaya.streamlit.app/"
tech = "https://teknology.streamlit.app/"
biz = "https://busines.streamlit.app/"
eco = "https://ekosistem.streamlit.app/"
livestock = "https://livestoc.streamlit.app/Peternakan_Perikanan"
```

Selesai! Semuanya sekarang terpusat dan rapi. ✅
