# TaxPro Indonesia API Simulator

🚀 **Live Demo**: [Deploy to Vercel](https://vercel.com)

## 📱 Fitur

Interactive web-based API simulator untuk testing TaxPro Indonesia API endpoints:

- ✅ **7 Tax Calculators**: PPh 21, PPh 23, PPN, PPh Badan, PBB, PKB, BPHTB
- ✅ **Dashboard Analytics**: Get KPI summary
- ✅ **AI Tax Advisor**: Chat dengan AI untuk tax advice
- ✅ **API Configuration**: Custom API URL dan API Key
- ✅ **Real-time Testing**: Test langsung dari browser
- ✅ **Formatted Results**: Display hasil dengan format currency
- ✅ **Error Handling**: Clear error messages

## 🚀 Deploy ke Vercel

### Option 1: Deploy via Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd pajak-dan-produksi
vercel
```

### Option 2: Deploy via GitHub

1. Push code ke GitHub
2. Import project di [vercel.com](https://vercel.com)
3. Deploy otomatis!

### Option 3: Deploy Button

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yandri918/pajak-dan-produksi)

## 🔧 Cara Menggunakan

1. **Buka API Simulator** di browser
2. **Configure API**:
   - API Base URL: `http://localhost:8000` (untuk local) atau URL production
   - API Key: `demo-key-12345` atau API key Anda
3. **Test Connection** untuk verify koneksi
4. **Pilih Endpoint** dari sidebar
5. **Input Data** sesuai calculator
6. **Click Calculate** untuk test API
7. **View Results** dengan format yang jelas

## 📊 Endpoints Available

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/tax/pph21` | POST | Calculate PPh 21 |
| `/api/v1/tax/pph23` | POST | Calculate PPh 23 |
| `/api/v1/tax/ppn` | POST | Calculate PPN |
| `/api/v1/tax/pph-badan` | POST | Calculate PPh Badan |
| `/api/v1/tax/pbb` | POST | Calculate PBB |
| `/api/v1/tax/pkb` | POST | Calculate PKB |
| `/api/v1/tax/bphtb` | POST | Calculate BPHTB |
| `/api/v1/dashboard/summary` | GET | Get Dashboard KPIs |
| `/api/v1/ai/advisor` | POST | AI Tax Advisor |

## 🎨 Features

- **Modern UI**: Glassmorphism design dengan gradient background
- **Responsive**: Works di desktop, tablet, dan mobile
- **Interactive**: Real-time API testing tanpa coding
- **User-Friendly**: Simple dan mudah digunakan
- **Production-Ready**: Siap untuk demo ke client atau testing

## 📝 Files

- `api-simulator.html` - Main simulator page (standalone, no dependencies)
- `vercel.json` - Vercel deployment configuration
- `README_SIMULATOR.md` - Documentation

## 🔐 Security Note

Untuk production:
- Ganti API Key dengan key yang valid
- Update API Base URL ke production server
- Enable HTTPS
- Implement rate limiting

## 💡 Use Cases

1. **Demo untuk Client**: Show API capabilities tanpa coding
2. **Testing**: Quick test API endpoints
3. **Documentation**: Interactive API documentation
4. **Development**: Test API saat development
5. **Training**: Teach team cara menggunakan API

## 📱 Screenshot

Simulator includes:
- API configuration panel
- Endpoint selector sidebar
- Interactive forms untuk each calculator
- Real-time result display
- Error handling

## 🎯 Next Steps

1. Deploy ke Vercel
2. Share link ke team
3. Use untuk testing dan demo
4. Integrate dengan production API

---

**Made with ❤️ for TaxPro Indonesia**
