# Weather Prediction API - Deployment Guide

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
pip install -r requirements-api.txt
```

2. **Run the API:**
```bash
python api.py
```

Or with uvicorn:
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

3. **Access the API:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 🐳 Docker Deployment

### Build and Run with Docker

1. **Build the image:**
```bash
docker build -t weather-api .
```

2. **Run the container:**
```bash
docker run -d -p 8000:8000 --name weather-api weather-api
```

3. **Check logs:**
```bash
docker logs -f weather-api
```

### Using Docker Compose

1. **Start services:**
```bash
docker-compose up -d
```

2. **View logs:**
```bash
docker-compose logs -f
```

3. **Stop services:**
```bash
docker-compose down
```

---

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

### Current Weather
```bash
GET /api/v1/weather/current?latitude=-6.2&longitude=106.8
```

### Hourly Forecast
```bash
GET /api/v1/weather/hourly?latitude=-6.2&longitude=106.8&hours=24
```

### Daily Forecast
```bash
GET /api/v1/weather/daily?latitude=-6.2&longitude=106.8&days=7
```

### Statistics
```bash
GET /api/v1/weather/statistics?latitude=-6.2&longitude=106.8&days=30
```

### Temperature Prediction
```bash
POST /api/v1/predict/temperature
Content-Type: application/json

{
  "latitude": -6.2,
  "longitude": 106.8
}
```

---

## 🔧 CI/CD Pipeline

### GitHub Actions Workflow

The CI/CD pipeline automatically:

1. **Test**: Runs unit tests with pytest
2. **Lint**: Checks code quality with flake8 and black
3. **Build**: Creates Docker image
4. **Deploy**: Pushes to production (on main branch)

### Required Secrets

Add these secrets to your GitHub repository:

- `DOCKER_USERNAME`: Docker Hub username
- `DOCKER_PASSWORD`: Docker Hub password/token
- `DEPLOY_HOST`: Production server IP/hostname
- `DEPLOY_USER`: SSH username
- `DEPLOY_KEY`: SSH private key

---

## 🧪 Testing

### Run tests locally:
```bash
pytest tests/ -v
```

### With coverage:
```bash
pytest tests/ -v --cov=. --cov-report=html
```

### View coverage report:
```bash
open htmlcov/index.html
```

---

## 🌐 Production Deployment

### Option 1: VPS/Cloud Server

1. **SSH to server:**
```bash
ssh user@your-server.com
```

2. **Clone repository:**
```bash
git clone https://github.com/yandri918/prediksi-cuaca.git
cd prediksi-cuaca
```

3. **Run with Docker Compose:**
```bash
docker-compose up -d
```

### Option 2: Heroku

1. **Login to Heroku:**
```bash
heroku login
heroku container:login
```

2. **Create app:**
```bash
heroku create weather-api-app
```

3. **Deploy:**
```bash
heroku container:push web
heroku container:release web
```

### Option 3: Railway

1. **Install Railway CLI:**
```bash
npm install -g @railway/cli
```

2. **Login and deploy:**
```bash
railway login
railway init
railway up
```

### Option 4: Render

1. Create new Web Service on Render.com
2. Connect GitHub repository
3. Set build command: `pip install -r requirements.txt -r requirements-api.txt`
4. Set start command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

---

## 📊 Monitoring

### Health Check
```bash
curl http://localhost:8000/health
```

### Docker Stats
```bash
docker stats weather-api
```

### Logs
```bash
# Docker
docker logs -f weather-api

# Docker Compose
docker-compose logs -f api
```

---

## 🔒 Security Best Practices

1. **Use environment variables** for sensitive data
2. **Enable HTTPS** in production (use Let's Encrypt)
3. **Implement rate limiting** (use slowapi)
4. **Add API authentication** (JWT tokens)
5. **Keep dependencies updated**

---

## 🚀 Performance Optimization

1. **Enable caching** for frequently requested data
2. **Use Redis** for session storage
3. **Implement connection pooling**
4. **Add CDN** for static assets
5. **Use Gunicorn** with multiple workers:

```bash
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## 📝 API Documentation

Full API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`

---

## 🐛 Troubleshooting

### Port already in use:
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

### Docker build fails:
```bash
# Clean build cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t weather-api .
```

### API not responding:
```bash
# Check container status
docker ps

# Restart container
docker restart weather-api
```

---

## 📞 Support

For issues or questions:
- GitHub Issues: https://github.com/yandri918/prediksi-cuaca/issues
- Email: support@weatherapi.com

---

## 📄 License

MIT License - see LICENSE file for details
