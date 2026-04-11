# TaxPro Indonesia API

RESTful API untuk perhitungan pajak Indonesia dan analytics.

## 🚀 Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Run API Server

```bash
# Development mode
uvicorn api:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Authentication

All endpoints require API Key authentication via header:

```
X-API-Key: your-api-key
```

**Demo API Keys:**
- `demo-key-12345` - Demo User
- `prod-key-67890` - Production User

## 📚 API Endpoints

### Tax Calculations

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/tax/pph21` | POST | Calculate PPh 21 (Employee Tax) |
| `/api/v1/tax/pph23` | POST | Calculate PPh 23 (Withholding Tax) |
| `/api/v1/tax/ppn` | POST | Calculate PPN (VAT) |
| `/api/v1/tax/pph-badan` | POST | Calculate PPh Badan (Corporate Tax) |
| `/api/v1/tax/pbb` | POST | Calculate PBB (Property Tax) |
| `/api/v1/tax/pkb` | POST | Calculate PKB (Vehicle Tax) |
| `/api/v1/tax/bphtb` | POST | Calculate BPHTB (Land Transfer Tax) |

### Dashboard & Analytics

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/dashboard/summary` | GET | Get dashboard KPI summary |

### AI & Insights

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/ai/advisor` | POST | Chat with AI tax advisor |

### Reports

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/reports/generate` | POST | Generate PDF tax report |

## 💡 Usage Examples

### Python

```python
import requests

API_BASE = "http://localhost:8000"
API_KEY = "demo-key-12345"

# Calculate PPh 21
response = requests.post(
    f"{API_BASE}/api/v1/tax/pph21",
    headers={"X-API-Key": API_KEY},
    json={
        "gaji_pokok": 10000000,
        "tunjangan": 2000000,
        "status_kawin": "K/1"
    }
)

result = response.json()
print(f"Pajak Bulanan: Rp {result['data']['pajak_bulanan']:,.0f}")
```

### JavaScript (Node.js)

```javascript
const axios = require('axios');

const API_BASE = 'http://localhost:8000';
const API_KEY = 'demo-key-12345';

async function calculatePPh21() {
  const response = await axios.post(
    `${API_BASE}/api/v1/tax/pph21`,
    {
      gaji_pokok: 10000000,
      tunjangan: 2000000,
      status_kawin: 'K/1'
    },
    {
      headers: { 'X-API-Key': API_KEY }
    }
  );
  
  console.log('Pajak Bulanan:', response.data.data.pajak_bulanan);
}
```

### cURL

```bash
curl -X POST "http://localhost:8000/api/v1/tax/pph21" \
  -H "X-API-Key: demo-key-12345" \
  -H "Content-Type: application/json" \
  -d '{
    "gaji_pokok": 10000000,
    "tunjangan": 2000000,
    "status_kawin": "K/1"
  }'
```

## 🔌 Integration Examples

### Mobile App (React Native)

See: `examples/react-native-integration.js`

### ERP System (Python)

See: `examples/erp-integration.py`

### Accounting Software (Node.js)

See: `examples/accounting-integration.js`

## 📦 Response Format

### Success Response

```json
{
  "status": "success",
  "data": {
    "pajak_bulanan": 125000,
    "pajak_tahunan": 1500000
  },
  "message": "PPh 21 calculated successfully",
  "timestamp": "2024-02-09T20:30:00Z"
}
```

### Error Response

```json
{
  "status": "error",
  "error": {
    "code": 400,
    "message": "gaji_pokok must be greater than 0"
  },
  "timestamp": "2024-02-09T20:30:00Z"
}
```

## 🐳 Docker Deployment

```bash
# Build image
docker build -t taxpro-api .

# Run container
docker run -p 8000:8000 taxpro-api
```

## 📝 License

MIT License
