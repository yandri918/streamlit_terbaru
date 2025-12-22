# 🤖 SETUP ROBOFLOW API - MODUL 20

## ✅ API Key Anda
```
ROBOFLOW_API_KEY=your_key_here
```

---

## 🚀 CARA SETUP (Pilih Salah Satu)

### **Option 1: Environment Variable (Recommended)**

**Windows (PowerShell):**
```powershell
$env:ROBOFLOW_API_KEY="your_key_here"
python run.py
```

**Windows (CMD):**
```cmd
set ROBOFLOW_API_KEY=your_key_here
python run.py
```

**Linux/Mac:**
```bash
export ROBOFLOW_API_KEY=your_key_here
python run.py
```

---

### **Option 2: .env File (Permanent)**

1. **Buat file `.env`** di root folder (jika belum ada)
2. **Tambahkan baris ini:**
   ```
   ROBOFLOW_API_KEY=your_key_here
   ```
3. **Restart server:**
   ```bash
   python run.py
   ```

---

### **Option 3: Hardcode di Code (Not Recommended)**

Edit file `app/routes/legacy.py` line 424:
```python
# Ganti ini:
api_key = os.environ.get('ROBOFLOW_API_KEY', 'YOUR_API_KEY_HERE')

# Menjadi:
api_key = 'your_key_here'
```

---

## 🧪 TESTING

1. **Restart server** (jika sudah running)
2. **Buka browser** → Modul 20
3. **Upload foto tanaman**
4. **Klik "Dapatkan Diagnosis Canggih"**
5. **Lihat hasil deteksi!** 🎉

---

## 📊 EXPECTED RESULTS

Dengan API key yang valid, Anda akan mendapat:
- ✅ Deteksi penyakit tanaman
- ✅ Confidence score (%)
- ✅ Koordinat lokasi penyakit
- ✅ Multiple disease detection

---

## ⚠️ TROUBLESHOOTING

### **Masih Error 403?**
- Pastikan API key benar
- Restart server setelah set environment variable
- Check typo di API key

### **Error "Model not found"?**
- Model ID default: `plant-disease-detection-iefbi/1`
- Bisa diganti di `app/routes/legacy.py` line 425

### **Error "No module named 'inference_sdk'"?**
```bash
pip install inference-sdk==0.9.0
```

---

## 🎊 SELESAI!

Modul 20 Roboflow AI sekarang siap digunakan dengan API key Anda!

**Happy Farming with AI!** 🌾🤖
