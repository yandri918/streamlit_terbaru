# Perbaikan Modul - Endpoint Fix

## Masalah yang Ditemukan
1. Semua modul menggunakan `apiPrefix = '/api/v2'` yang tidak ada
2. Beberapa modul menggunakan endpoint baru yang tidak sesuai dengan legacy routes
3. Format request tidak sesuai dengan yang diharapkan endpoint

## Perbaikan yang Dilakukan

### 1. Fix API Prefix
- **Sebelum**: `const apiPrefix = '/api/v2';`
- **Sesudah**: `const apiPrefix = '';` (menggunakan legacy endpoints)

**File yang diperbaiki (20 file):**
- dokter_tanaman.html
- dokter_tanaman_canggih_roboflow_ai.html
- analis_risiko_keberhasilan_ai.html
- perencana_hasil_panen_ai.html
- diagnostik_gejala_cerdas.html
- intelijen_prediktif_xai.html
- kalkulator_konversi_pupuk.html
- prediksi_hasil_panen_cerdas.html
- rekomendasi_tanaman_cerdas_agrimap_ai.html
- pusat_pengetahuan_ph_tanah.html
- ensiklopedia_komoditas_cerdas.html
- analisis_tren_harga.html
- strategi_penyemprotan_cerdas.html
- dasbor_rekomendasi_terpadu.html
- kalkulator_pupuk_holistik.html
- pustaka_dokumen.html
- pusat_pengetahuan_pertanian.html
- basis_pengetahuan_budidaya.html
- intelijen_harga_pasar.html
- analisis_npk_manual.html
- asisten_agronomi.html

### 2. Fix Endpoint Individual

#### bwd_analysis.html
- **Sebelum**: `/api/analysis/bwd`
- **Sesudah**: `/analyze`

#### fertilizer_rec.html
- **Sebelum**: `/api/recommendation/fertilizer`
- **Sesudah**: `/recommendation`

#### price_intel.html
- **Sebelum**: `/api/market/prices?commodity=...` (GET)
- **Sesudah**: `/get-prices` (POST dengan JSON body)

#### crop_rec.html
- **Sebelum**: `/api/recommendation`
- **Sesudah**: `/recommend-crop` (dengan data lengkap: n_value, p_value, k_value, temperature, humidity, ph, rainfall)

#### pest_guide.html
- **Sebelum**: `/api/knowledge?query=...` (GET)
- **Sesudah**: `/get-knowledge` (POST dengan JSON body: `{commodity: pest}`)

## Endpoint Legacy yang Tersedia

Semua endpoint legacy tersedia di route `/` (root):

1. **BWD Analysis**: `POST /analyze`
2. **Fertilizer Recommendation**: `POST /recommendation`
3. **NPK Analysis**: `POST /analyze-npk`
4. **Market Prices**: `POST /get-prices`
5. **Knowledge Base**: `POST /get-knowledge`
6. **Fertilizer Calculation**: `POST /calculate-fertilizer`
7. **PDF Upload**: `POST /upload-pdf`
8. **PDF List**: `GET /get-pdfs`
9. **View PDF**: `GET /view-pdf/<filename>`
10. **Integrated Recommendation**: `POST /get-integrated-recommendation`
11. **Spraying Recommendation**: `POST /get-spraying-recommendation`
12. **Ticker Prices**: `GET /get-ticker-prices`
13. **Historical Prices**: `POST /get-historical-prices`
14. **Commodity Guide**: `POST /get-commodity-guide`
15. **pH Info**: `GET /get-ph-info`
16. **Crop Recommendation**: `POST /recommend-crop`
17. **Yield Prediction**: `POST /predict-yield`
18. **Advanced Yield Prediction**: `POST /predict-yield-advanced`
19. **Fertilizer Bags Calculation**: `POST /calculate-fertilizer-bags`
20. **Diagnostic Tree**: `GET /get-diagnostic-tree`
21. **Yield Plan**: `POST /generate-yield-plan`
22. **Success Prediction**: `POST /predict-success`
23. **Advanced Disease Analysis**: `POST /analyze-disease-advanced`
24. **Fruit List**: `GET /get-fruit-list`
25. **Fruit Info**: `POST /get-fruit-info`

## Cara Test

1. **Jalankan server**:
   ```bash
   python run.py
   ```

2. **Test endpoint**:
   - Buka browser ke `http://localhost:5000/modules/bwd-analysis`
   - Upload gambar dan klik "Analisis"
   - Cek console browser (F12) untuk melihat error jika ada

3. **Cek Network Tab**:
   - Buka Developer Tools (F12)
   - Tab Network
   - Lihat request yang dikirim dan response yang diterima

## Catatan Penting

- Semua endpoint legacy menggunakan format response: `{success: true/false, data/error: ...}`
- Pastikan request body sesuai dengan format yang diharapkan endpoint
- Beberapa endpoint memerlukan authentication (JWT), tapi legacy endpoints tidak memerlukan auth
- Jika masih ada error, cek console browser dan server logs

