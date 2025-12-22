# 🔄 MIGRATION GUIDE - AgriSensa API v1.0 → v2.0

## ✅ BACKWARD COMPATIBILITY RESTORED!

### 📋 Ringkasan Perubahan

AgriSensa API v2.0 sekarang **FULLY BACKWARD COMPATIBLE** dengan frontend lama (v1.0). Semua endpoint lama masih berfungsi dengan URL yang sama.

---

## 🔗 ENDPOINT MAPPING

### ✅ Legacy Endpoints (Tanpa Prefix - WORKING!)

Semua endpoint ini masih berfungsi seperti di v1.0:

| Endpoint | Method | Deskripsi | Status |
|----------|--------|-----------|--------|
| `/` | GET | Dashboard utama | ✅ Working |
| `/analyze` | POST | Analisis daun (BWD) | ✅ Working |
| `/recommendation` | POST | Rekomendasi pupuk | ✅ Working |
| `/analyze-npk` | POST | Analisis NPK | ✅ Working |
| `/get-prices` | POST | Harga komoditas | ✅ Working |
| `/get-knowledge` | POST | Knowledge base | ✅ Working |
| `/calculate-fertilizer` | POST | Kalkulator pupuk | ✅ Working |
| `/upload-pdf` | POST | Upload dokumen | ✅ Working |
| `/get-pdfs` | GET | List dokumen | ✅ Working |
| `/view-pdf/<filename>` | GET | View dokumen | ✅ Working |
| `/get-integrated-recommendation` | POST | Rekomendasi terintegrasi | ✅ Working |
| `/get-spraying-recommendation` | POST | Strategi penyemprotan | ✅ Working |
| `/get-ticker-prices` | GET | Ticker harga | ✅ Working |
| `/get-historical-prices` | POST | Harga historis | ✅ Working |
| `/get-commodity-guide` | POST | Panduan komoditas | ✅ Working |
| `/get-ph-info` | GET | Informasi pH | ✅ Working |
| `/recommend-crop` | POST | Rekomendasi tanaman | ✅ Working |
| `/predict-yield` | POST | Prediksi panen | ✅ Working |
| `/predict-yield-advanced` | POST | Prediksi XAI | ✅ Working |
| `/calculate-fertilizer-bags` | POST | Hitung karung pupuk | ✅ Working |
| `/get-diagnostic-tree` | GET | Diagnostic tree | ✅ Working |
| `/generate-yield-plan` | POST | Rencana panen | ✅ Working |

### 🆕 New API Endpoints (Dengan Prefix `/api/`)

Endpoint baru dengan struktur yang lebih terorganisir:

#### Authentication (`/api/auth`)
- `POST /api/auth/register` - Register user baru
- `POST /api/auth/login` - Login user
- `POST /api/auth/refresh` - Refresh token
- `GET /api/auth/me` - Get profile (Auth required)
- `PUT /api/auth/me` - Update profile (Auth required)
- `PUT /api/auth/change-password` - Ganti password (Auth required)

#### Analysis (`/api/analysis`)
- `POST /api/analysis/bwd` - Analisis daun
- `POST /api/analysis/npk` - Analisis NPK
- `GET /api/analysis/npk/history` - History NPK (Auth required)

#### Recommendations (`/api/recommendation`)
- `POST /api/recommendation/fertilizer` - Rekomendasi pupuk
- `POST /api/recommendation/calculate-fertilizer` - Kalkulator pupuk
- `POST /api/recommendation/integrated` - Rekomendasi terintegrasi
- `POST /api/recommendation/spraying` - Strategi penyemprotan
- `GET /api/recommendation/history` - History (Auth required)

#### Knowledge Base (`/api/knowledge`)
- `GET /api/knowledge/crop/<commodity>` - Knowledge tanaman
- `GET /api/knowledge/guide/<commodity>` - Panduan budidaya
- `GET /api/knowledge/ph-info` - Informasi pH
- `GET /api/knowledge/diagnostic-tree` - Diagnostic tree
- `GET /api/knowledge/fertilizer-data` - Data pupuk

#### Market Data (`/api/market`)
- `POST /api/market/prices` - Harga saat ini
- `GET /api/market/ticker` - Ticker harga
- `POST /api/market/historical` - Harga historis

#### ML Predictions (`/api/ml`)
- `POST /api/ml/recommend-crop` - Rekomendasi tanaman
- `POST /api/ml/predict-yield` - Prediksi panen
- `POST /api/ml/predict-yield-advanced` - Prediksi XAI
- `POST /api/ml/generate-yield-plan` - Rencana panen
- `POST /api/ml/calculate-fertilizer-bags` - Hitung karung

---

## 🔧 IMPLEMENTASI TEKNIS

### Struktur File Baru

```
app/
├── routes/
│   ├── legacy.py          # ✨ NEW! Backward compatibility layer
│   ├── main.py            # Dashboard & health check
│   ├── auth.py            # Authentication endpoints
│   ├── analysis.py        # Analysis endpoints
│   ├── recommendation.py  # Recommendation endpoints
│   ├── knowledge.py       # Knowledge base endpoints
│   ├── market.py          # Market data endpoints
│   └── ml.py              # ML prediction endpoints
```

### Legacy Routes Implementation

File `app/routes/legacy.py` berisi semua endpoint lama yang memanggil service layer baru:

```python
# Contoh: Legacy endpoint memanggil service baru
@legacy_bp.route('/analyze', methods=['POST'])
def analyze_bwd_endpoint():
    # Menggunakan AnalysisService yang baru
    result = analysis_service.analyze_leaf_image(file.read())
    return jsonify({'success': True, **result})
```

### Blueprint Registration

Di `app/__init__.py`:

```python
def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(legacy_bp)  # No prefix!
    app.register_blueprint(analysis_bp, url_prefix='/api/analysis')
    # ... other blueprints with /api/ prefix
```

---

## 🎯 CARA MIGRASI FRONTEND (Opsional)

### Opsi 1: Tetap Gunakan Endpoint Lama (Recommended untuk saat ini)

Tidak perlu ubah apa-apa! Frontend lama akan tetap berfungsi.

```javascript
// Frontend lama - masih berfungsi!
fetch('/analyze', {
    method: 'POST',
    body: formData
})
```

### Opsi 2: Migrasi Bertahap ke Endpoint Baru

Untuk fitur baru, gunakan endpoint dengan prefix `/api/`:

```javascript
// Frontend baru - dengan authentication
fetch('/api/analysis/bwd', {
    method: 'POST',
    headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
```

---

## 🔐 FITUR BARU DI V2.0

### 1. Authentication & Authorization
- JWT-based authentication
- Role-based access control (admin, user)
- Secure password hashing

### 2. Rate Limiting
- 100 requests per hour per IP
- Mencegah abuse

### 3. CORS Support
- Cross-origin requests enabled
- Configurable origins

### 4. Better Error Handling
- Structured error responses
- Proper HTTP status codes
- Detailed error messages

### 5. Logging & Monitoring
- Structured logging
- Log rotation
- Ready for Sentry integration

### 6. Database Enhancements
- 4 models dengan relasi
- Migration support (Alembic)
- Better data tracking

---

## 📊 PERBANDINGAN RESPONSE FORMAT

### Legacy Format (Tetap Sama)

```json
{
    "success": true,
    "bwd_score": 85,
    "avg_hue_value": 45.2,
    "confidence_percent": 92.5
}
```

### New API Format (Sama, tapi dengan tambahan metadata)

```json
{
    "success": true,
    "data": {
        "bwd_score": 85,
        "avg_hue": 45.2,
        "confidence": 92.5
    },
    "timestamp": "2025-10-28T13:36:00Z"
}
```

---

## ✅ TESTING CHECKLIST

### Manual Testing

```bash
# Test legacy endpoint
curl -X POST http://localhost:5000/analyze \
  -F "file=@test_leaf.jpg"

# Test new API endpoint
curl -X POST http://localhost:5000/api/analysis/bwd \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test_leaf.jpg"
```

### Automated Testing (Coming Soon)

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=app tests/
```

---

## 🐛 TROUBLESHOOTING

### Issue: Endpoint tidak ditemukan (404)

**Solusi:**
1. Pastikan aplikasi sudah restart
2. Cek apakah `legacy_bp` sudah diregister
3. Verifikasi URL endpoint

### Issue: CORS error di browser

**Solusi:**
1. Update `.env` dengan CORS_ORIGINS yang benar
2. Restart aplikasi

### Issue: Rate limit exceeded

**Solusi:**
1. Tunggu 1 jam
2. Atau disable rate limiting di development:
   ```python
   # app/__init__.py
   limiter = Limiter(
       key_func=get_remote_address,
       default_limits=[]  # Disable
   )
   ```

---

## 📝 CHANGELOG

### v2.0.0 (2025-10-28)

**Added:**
- ✅ Legacy routes untuk backward compatibility
- ✅ JWT authentication
- ✅ Rate limiting
- ✅ CORS support
- ✅ Structured logging
- ✅ 4 database models dengan relasi
- ✅ Migration support
- ✅ Comprehensive documentation

**Changed:**
- ✅ Refactored monolithic app.py ke modular structure
- ✅ Separated business logic ke service layer
- ✅ Improved error handling

**Fixed:**
- ✅ SQLAlchemy `metadata` reserved word conflict
- ✅ Database initialization issues

**Deprecated:**
- ⚠️ Direct database access (gunakan models)

**Removed:**
- ❌ None (full backward compatibility)

---

## 🎓 BEST PRACTICES

### Untuk Developer Baru

1. **Gunakan endpoint baru (`/api/*`)** untuk fitur baru
2. **Implementasi authentication** untuk fitur yang sensitif
3. **Handle errors** dengan proper try-catch
4. **Log semua actions** untuk debugging
5. **Write tests** untuk setiap endpoint baru

### Untuk Maintenance

1. **Monitor logs** di folder `logs/`
2. **Backup database** secara berkala
3. **Update dependencies** secara teratur
4. **Review security** setiap bulan

---

## 📞 SUPPORT

Jika ada masalah atau pertanyaan:

1. **Check logs:** `logs/agrisensa.log`
2. **Read docs:** `README_NEW.md`, `SETUP_LOKAL.md`
3. **Check issues:** GitHub Issues
4. **Contact:** admin@agrisensa.com

---

**© 2025 AgriSensa - Smart Agriculture Platform**
