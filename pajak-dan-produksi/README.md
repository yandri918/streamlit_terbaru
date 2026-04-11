# 💼 TaxPro Indonesia - Kalkulator Pajak & Biaya Produksi

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

Platform digital terpercaya untuk perhitungan pajak dan manajemen biaya produksi perusahaan di Indonesia. Dilengkapi dengan kalkulator pajak yang akurat sesuai peraturan perpajakan terbaru (UU HPP 2021) dan tools analisis biaya produksi profesional.

![TaxPro Indonesia](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square)

---

## 📋 Daftar Isi

- [Fitur Utama](#-fitur-utama)
- [Demo & Screenshot](#-demo--screenshot)
- [Instalasi](#-instalasi)
- [Cara Penggunaan](#-cara-penggunaan)
- [Teknologi](#-teknologi)
- [Regulasi Pajak](#-regulasi-pajak)
- [Roadmap](#-roadmap)
- [Kontribusi](#-kontribusi)
- [Lisensi](#-lisensi)
- [Kontak](#-kontak)

---

## 🚀 Fitur Utama

### 💰 Kalkulator Pajak Lengkap

#### 1. PPh 21 - Pajak Penghasilan Karyawan
- ✅ Perhitungan pajak progresif sesuai UU HPP 2021
- ✅ 5 bracket pajak: 5%, 15%, 25%, 30%, 35%
- ✅ PTKP (Penghasilan Tidak Kena Pajak) dengan 8 status
- ✅ Perhitungan bonus dan THR
- ✅ Potongan BPJS dan pensiun
- ✅ Breakdown detail tahunan dan bulanan
- ✅ Export hasil ke CSV

#### 2. PPh 23 - Pajak Potong Pungut
- ✅ Tarif 2% untuk jasa (teknik, manajemen, konsultan, sewa)
- ✅ Tarif 15% untuk dividen, royalti, bunga, hadiah
- ✅ Penyesuaian otomatis untuk non-NPWP (tarif 2x lipat)
- ✅ Perhitungan netto otomatis

#### 3. PPN - Pajak Pertambahan Nilai
- ✅ Tarif 11% (standar 2022-sekarang)
- ✅ Tarif 12% (rencana 2025)
- ✅ Perhitungan DPP (Dasar Pengenaan Pajak)
- ✅ Mode: Harga sudah/belum termasuk PPN
- ✅ Visualisasi pie chart komposisi harga

#### 4. PPh Badan - Pajak Perusahaan (ADVANCED) 🌟
Kalkulator PPh Badan dengan 5 tab fitur advanced:

##### **Tab 1: Perhitungan Dasar (Enhanced)**
- ✅ Tarif standar 22%
- ✅ Fasilitas UMKM 11% (PKP ≤ 500 juta)
- ✅ Koreksi fiskal detail:
  - Biaya tidak dapat dikurangkan
  - Penghasilan kena pajak final
  - Koreksi fiskal lainnya
- ✅ Integrasi kredit pajak (PPh 22, PPh 23)
- ✅ Perhitungan PPh Kurang/Lebih Bayar
- ✅ Tarif efektif otomatis

##### **Tab 2: PPh 25 (Angsuran Bulanan)**
- ✅ Kalkulator angsuran pajak bulanan
- ✅ Berdasarkan pajak tahun sebelumnya
- ✅ Jadwal pembayaran 12 bulan
- ✅ Status tracking pembayaran (✅ Dibayar / ⏳ Belum Bayar)
- ✅ Perhitungan sisa angsuran

##### **Tab 3: Proyeksi Multi-Tahun**
- ✅ Proyeksi pajak 3-5 tahun ke depan
- ✅ Skenario pertumbuhan revenue (0-50%/tahun)
- ✅ Analisis margin laba
- ✅ Grafik interaktif (bar chart)
- ✅ Cek eligibilitas UMKM otomatis per tahun
- ✅ Perbandingan year-over-year

##### **Tab 4: Perbandingan Skenario**
- ✅ Bandingkan UMKM vs Non-UMKM
- ✅ Perhitungan penghematan pajak
- ✅ Visualisasi comparison chart
- ✅ Verifikasi eligibilitas UMKM
- ✅ Persentase penghematan

##### **Tab 5: Tax Planning Recommendations**
6 strategi optimasi pajak yang legal:
1. 💡 Manfaatkan fasilitas UMKM
2. 📊 Optimalkan biaya deductible
3. 💳 Kredit pajak (PPh 22, 23, 24)
4. 🏗️ Perencanaan investasi (tax holiday, allowance)
5. ⏰ Timing strategy
6. 🔄 Restrukturisasi bisnis

### 🏭 Manajemen Biaya Produksi

- ✅ **Input Biaya Terstruktur**:
  - Bahan Baku Langsung (Direct Materials)
  - Kemasan (Packaging)
  - Tenaga Kerja Langsung (Direct Labor)
  - Overhead Pabrik (Utilities, Sewa, Pemeliharaan, Depresiasi)

- ✅ **Analisis Komprehensif**:
  - Total biaya produksi
  - Biaya per unit
  - Target margin keuntungan
  - Harga jual optimal
  - Profit per unit dan total
  - Breakdown biaya (pie chart)
  - Export analisis ke CSV

### 🎨 Desain & UX

- ✅ **Glassmorphism UI** - Modern glass-effect design
- ✅ **Gradient Background** - Professional purple-blue theme
- ✅ **Responsive Layout** - Desktop, tablet, mobile friendly
- ✅ **Interactive Charts** - Plotly visualizations
- ✅ **Custom Styling** - Premium CSS dengan Inter font
- ✅ **Smooth Animations** - Hover effects dan transitions

### 🌐 API & Simulator (New!)

Akses layanan kalkulator pajak melalui REST API yang cepat dan handal. Dilengkapi dengan Simulator interaktif untuk testing tanpa koding.

- ✅ **9 Endpoints**: PPh 21, 23, PPN, PPh Badan, PBB, PKB, BPHTB, Dashboard, AI Advisor
- ✅ **Interactive Simulator**: Web interface untuk mencoba semua endpoint
- ✅ **API Documentation**: Swagger UI & Redoc
- ✅ **Vercel Deployment**: Serverless architecture

**Links:**
- 🎮 **Live Simulator**: [https://pajak-dan-produksi.vercel.app/api-simulator.html](https://pajak-dan-produksi.vercel.app/api-simulator.html)
- 📄 **API Docs**: [https://pajak-dan-produksi.vercel.app/docs](https://pajak-dan-produksi.vercel.app/docs)

---

## 🖼️ Demo & Screenshot

### Beranda
![Beranda](https://via.placeholder.com/800x400/667eea/ffffff?text=TaxPro+Indonesia+Homepage)

### Kalkulator PPh Badan Advanced
![PPh Badan](https://via.placeholder.com/800x400/764ba2/ffffff?text=Advanced+Corporate+Tax+Calculator)

### Proyeksi Multi-Tahun
![Proyeksi](https://via.placeholder.com/800x400/f093fb/ffffff?text=Multi-Year+Tax+Projection)

---

## 📦 Instalasi

### Prasyarat
- Python 3.8 atau lebih tinggi
- pip (Python package manager)

### Langkah Instalasi

1. **Clone Repository**
```bash
git clone https://github.com/yandri918/pajak-dan-produksi.git
cd pajak-dan-produksi
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Jalankan Aplikasi**
```bash
streamlit run app.py
```

4. **Akses Aplikasi**
Buka browser dan akses: `http://localhost:8501`

---

## 🎯 Cara Penggunaan

### Kalkulator PPh 21 (Pajak Karyawan)

1. Pilih menu **"💰 Kalkulator Pajak"** di sidebar
2. Pilih tab **"PPh 21"**
3. Masukkan data:
   - Gaji bruto per bulan
   - Status pernikahan (TK/K dengan jumlah tanggungan)
   - Bonus/THR tahunan (opsional)
   - Potongan BPJS/Pensiun (opsional)
4. Klik **"🧮 Hitung PPh 21"**
5. Lihat hasil perhitungan dan download CSV jika perlu

### Kalkulator PPh Badan Advanced

#### Perhitungan Dasar
1. Pilih tab **"PPh Badan"** → **"💼 Perhitungan Dasar"**
2. Input data keuangan:
   - Omzet tahunan
   - Biaya operasional
   - Penghasilan lain
3. Input koreksi fiskal (jika ada)
4. Input kredit pajak (PPh 22, PPh 23)
5. Centang "UMKM" jika omzet < 4.8 Miliar
6. Klik **"🧮 Hitung PPh Badan"**

#### PPh 25 (Angsuran)
1. Pilih tab **"📅 PPh 25 (Angsuran)"**
2. Input PPh Badan tahun lalu
3. Input kredit pajak tahun lalu
4. Pilih bulan berjalan
5. Lihat jadwal angsuran 12 bulan

#### Proyeksi Multi-Tahun
1. Pilih tab **"📈 Proyeksi Multi-Tahun"**
2. Input omzet tahun ini
3. Set proyeksi pertumbuhan (%)
4. Set margin laba (%)
5. Pilih periode proyeksi (3-5 tahun)
6. Klik **"📈 Buat Proyeksi"**
7. Lihat tabel dan grafik proyeksi

### Biaya Produksi

1. Pilih menu **"🏭 Biaya Produksi"**
2. Input semua komponen biaya:
   - Bahan baku dan kemasan
   - Upah tenaga kerja
   - Overhead (listrik, sewa, pemeliharaan, depresiasi)
3. Input volume produksi (unit)
4. Set target margin keuntungan (%)
5. Klik **"🧮 Hitung Biaya Produksi"**
6. Analisis hasil dan download CSV

---

## 🛠️ Teknologi

### Core Framework
- **Streamlit** `>=1.31.0` - Web application framework
- **Python** `3.8+` - Programming language

### Data Processing
- **Pandas** `>=2.0.0` - Data manipulation and analysis
- **NumPy** - Numerical computations

### Visualization
- **Plotly** `>=5.0.0` - Interactive charts and graphs

### Export
- **OpenPyXL** `>=3.0.0` - Excel file handling

### Styling
- **Custom CSS** - Glassmorphism design
- **Google Fonts** - Inter font family
- **Font Awesome** - Icons (via CDN)

---

## 📜 Regulasi Pajak

Aplikasi ini mengikuti peraturan perpajakan Indonesia terbaru:

### PPh 21
- **UU HPP 2021** (Undang-Undang Harmonisasi Peraturan Perpajakan)
- **PMK-252/PMK.03/2008** - Petunjuk pelaksanaan pemotongan PPh 21
- Tarif progresif: 5%, 15%, 25%, 30%, 35%

### PPh 23
- **PMK-9/PMK.03/2018** - Tarif dan objek PPh 23
- Tarif 2% untuk jasa tertentu
- Tarif 15% untuk dividen, royalti, bunga

### PPN
- **UU No. 42 Tahun 2009** tentang PPN
- **UU HPP 2021** - Tarif PPN 11% (2022)
- Rencana kenaikan 12% (2025)

### PPh Badan
- **UU No. 36 Tahun 2008** tentang PPh
- **PP 23 Tahun 2018** - Fasilitas UMKM
- Tarif standar 22%
- Tarif UMKM 11% (PKP ≤ 500 juta)

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Database integration untuk menyimpan riwayat perhitungan
- [ ] User authentication dan multi-user support
- [ ] PDF report generation dengan template profesional
- [ ] Email notification untuk deadline pajak
- [ ] Integrasi API DJP Online
- [ ] Mobile app (React Native)

### Version 2.1 (Future)
- [ ] AI-powered tax optimization recommendations
- [ ] Chatbot konsultasi pajak
- [ ] Perbandingan dengan kompetitor (benchmarking)
- [ ] Dashboard analytics untuk CFO
- [ ] Integration dengan software akuntansi (Accurate, Zahir)

---

## 🤝 Kontribusi

Kontribusi sangat diterima! Berikut cara berkontribusi:

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

### Guidelines
- Ikuti style guide Python (PEP 8)
- Tambahkan docstring untuk fungsi baru
- Update README jika menambah fitur
- Test semua perubahan sebelum PR

---

## ⚠️ Disclaimer

**PENTING**: Aplikasi ini adalah tools bantu perhitungan pajak untuk keperluan estimasi dan perencanaan. Hasil perhitungan sebaiknya dikonfirmasi dengan konsultan pajak profesional atau petugas DJP untuk keperluan pelaporan resmi.

- ✅ Akurat sesuai regulasi terbaru (UU HPP 2021)
- ✅ Cocok untuk perencanaan dan simulasi
- ⚠️ Bukan pengganti konsultasi profesional
- ⚠️ Tidak menjamin keakuratan 100% untuk kasus kompleks

---

## 📄 Lisensi

Distributed under the MIT License. See `LICENSE` for more information.

---

## 📞 Kontak

**TaxPro Indonesia**

- 📧 Email: konsultasi@taxpro.id
- 📱 WhatsApp: +62 812-3456-7890
- 🌐 Website: [taxpro.id](https://taxpro.id)
- 💼 LinkedIn: [TaxPro Indonesia](https://linkedin.com/company/taxpro-indonesia)

**Developer**

- GitHub: [@yandri918](https://github.com/yandri918)
- Repository: [pajak-dan-produksi](https://github.com/yandri918/pajak-dan-produksi)

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io) - Amazing web framework
- [Plotly](https://plotly.com) - Interactive visualizations
- [Direktorat Jenderal Pajak](https://pajak.go.id) - Tax regulations reference
- [Font Awesome](https://fontawesome.com) - Icons
- [Google Fonts](https://fonts.google.com) - Typography

---

<div align="center">

**⭐ Star this repo if you find it useful!**

Made with ❤️ by TaxPro Indonesia Team

[Report Bug](https://github.com/yandri918/pajak-dan-produksi/issues) · [Request Feature](https://github.com/yandri918/pajak-dan-produksi/issues)

</div>
