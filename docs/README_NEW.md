# 🌾 AgriSensa API v2.0 - Refactored & Production-Ready

## 🚀 What's New in v2.0

### Major Improvements

✅ **Modular Architecture** - Clean separation of concerns with blueprints, services, and models
✅ **Authentication & Security** - JWT-based authentication with role-based access control
✅ **Rate Limiting** - Protection against abuse with configurable rate limits
✅ **CORS Support** - Proper cross-origin resource sharing configuration
✅ **Environment Configuration** - Separate configs for development, production, and testing
✅ **Database Migrations** - Flask-Migrate (Alembic) for version-controlled schema changes
✅ **Error Handling** - Comprehensive error handlers with proper HTTP status codes
✅ **Logging** - Structured logging with rotation and configurable levels
✅ **API Documentation Ready** - Structure prepared for Swagger/OpenAPI integration

### New Features

🔐 **User Management** - Registration, login, profile management
📊 **Enhanced Models** - User, NPK Reading, Recommendation, Crop tracking
🎯 **Service Layer** - Business logic separated from routes
🔄 **Model Loader** - Lazy loading and caching for ML models
📈 **Better Organization** - Clear folder structure following best practices

---

## 📁 New Project Structure

```
agrisensa-api/
├── app/
│   ├── __init__.py              # Application factory
│   ├── config/                  # Configuration management
│   │   ├── __init__.py
│   │   └── config.py            # Config classes (Dev, Prod, Test)
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── npk_reading.py       # NPK readings
│   │   ├── recommendation.py    # Recommendations
│   │   └── crop.py              # Crop tracking
│   ├── routes/                  # API endpoints (Blueprints)
│   │   ├── __init__.py
│   │   ├── main.py              # Main routes
│   │   ├── auth.py              # Authentication
│   │   ├── analysis.py          # Leaf & soil analysis
│   │   ├── recommendation.py    # Fertilizer recommendations
│   │   ├── knowledge.py         # Knowledge base
│   │   ├── market.py            # Market prices
│   │   └── ml.py                # ML predictions
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── analysis_service.py
│   │   ├── recommendation_service.py
│   │   ├── knowledge_service.py
│   │   ├── market_service.py
│   │   └── ml_service.py
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   └── data_loader.py
│   └── ml_models/               # ML model management
│       ├── __init__.py
│       └── model_loader.py
├── migrations/                  # Database migrations
├── tests/                       # Unit & integration tests
├── templates/                   # HTML templates
├── uploads/                     # File uploads
├── logs/                        # Application logs
├── .env                         # Environment variables
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
├── requirements.txt             # Python dependencies
├── run.py                       # Application entry point
└── README_NEW.md               # This file
```

---

## 🛠️ Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///agrisensa.db
JWT_SECRET_KEY=your-jwt-secret-here
```

### 3. Initialize Database

```bash
# Initialize database tables
flask init-db

# Or using Python
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()"
```

### 4. Create Admin User (Optional)

```bash
flask create-admin
```

Default credentials: `admin` / `admin123`

### 5. Run Application

**Development:**
```bash
python run.py
```

**Production (with Gunicorn):**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

---

## 🔐 API Authentication

### Register New User

```bash
POST /api/auth/register
Content-Type: application/json

{
  "username": "farmer1",
  "email": "farmer1@example.com",
  "password": "securepassword",
  "full_name": "John Doe",
  "location": "Bandung"
}
```

### Login

```bash
POST /api/auth/login
Content-Type: application/json

{
  "username": "farmer1",
  "password": "securepassword"
}
```

Response:
```json
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

### Using Protected Endpoints

```bash
GET /api/auth/me
Authorization: Bearer <access_token>
```

---

## 📡 API Endpoints

### Public Endpoints (No Auth Required)

- `GET /` - Main dashboard
- `GET /health` - Health check
- `GET /api/info` - API information
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user

### Analysis Endpoints

- `POST /api/analysis/bwd` - Analyze leaf image
- `POST /api/analysis/npk` - Analyze NPK values
- `GET /api/analysis/npk/history` - Get NPK history (Auth required)

### Recommendation Endpoints

- `POST /api/recommendation/fertilizer` - Get fertilizer recommendation
- `POST /api/recommendation/calculate-fertilizer` - Calculate dosage
- `POST /api/recommendation/integrated` - Integrated recommendation
- `POST /api/recommendation/spraying` - Spraying strategy
- `GET /api/recommendation/history` - Recommendation history (Auth required)

### Knowledge Base Endpoints

- `GET /api/knowledge/crop/<commodity>` - Crop knowledge
- `GET /api/knowledge/guide/<commodity>` - Commodity guide
- `GET /api/knowledge/ph-info` - pH information
- `GET /api/knowledge/diagnostic-tree` - Disease diagnostic tree
- `GET /api/knowledge/fertilizer-data` - Fertilizer data

### Market Data Endpoints

- `POST /api/market/prices` - Current prices
- `GET /api/market/ticker` - Ticker prices
- `POST /api/market/historical` - Historical prices

### ML Prediction Endpoints

- `POST /api/ml/recommend-crop` - Crop recommendation
- `POST /api/ml/predict-yield` - Yield prediction
- `POST /api/ml/predict-yield-advanced` - Advanced prediction with XAI
- `POST /api/ml/generate-yield-plan` - Generate yield plan
- `POST /api/ml/calculate-fertilizer-bags` - Calculate fertilizer bags

---

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | development |
| `SECRET_KEY` | Flask secret key | - |
| `DATABASE_URL` | Database connection string | sqlite:///agrisensa.db |
| `JWT_SECRET_KEY` | JWT secret key | - |
| `REDIS_URL` | Redis connection (for caching) | redis://localhost:6379/0 |
| `LOG_LEVEL` | Logging level | INFO |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000 |

### Rate Limiting

Default rate limits:
- General endpoints: 100 requests/hour
- Authentication: 10 requests/hour
- Registration: 5 requests/hour

Configure in `app/config/config.py`

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

---

## 📊 Database Migrations

```bash
# Initialize migrations (first time only)
flask db init

# Create migration after model changes
flask db migrate -m "Description of changes"

# Apply migrations
flask db upgrade

# Rollback migration
flask db downgrade
```

---

## 🚀 Deployment

### Using Gunicorn (Production)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 --timeout 120 "app:create_app()"
```

### Using Docker (Coming Soon)

```bash
docker build -t agrisensa-api .
docker run -p 5000:5000 agrisensa-api
```

### Environment Setup for Production

1. Set `FLASK_ENV=production`
2. Use strong `SECRET_KEY` and `JWT_SECRET_KEY`
3. Use PostgreSQL instead of SQLite
4. Enable Redis for caching
5. Configure proper CORS origins
6. Set up SSL/TLS certificates
7. Enable Sentry for error tracking

---

## 📈 Performance Improvements

- ✅ Lazy loading for ML models
- ✅ Thread-safe model caching
- ✅ Database connection pooling
- ✅ Rate limiting to prevent abuse
- 🔄 Redis caching (ready to enable)
- 🔄 Async task processing with Celery (ready to implement)

---

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Password hashing with Werkzeug
- ✅ Rate limiting
- ✅ CORS configuration
- ✅ Input validation
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ XSS protection (Flask defaults)

---

## 📝 Migration from v1.0

### Breaking Changes

1. **Entry Point Changed**: Use `run.py` instead of `app.py`
2. **Authentication Required**: Some endpoints now require JWT token
3. **URL Structure**: Endpoints now have `/api/` prefix
4. **Database Schema**: New tables added (users, recommendations, crops)

### Migration Steps

1. Backup your old `agrisensa.db`
2. Install new dependencies: `pip install -r requirements.txt`
3. Initialize new database: `flask init-db`
4. Migrate data if needed (custom script)
5. Update frontend to use new API structure
6. Add authentication to API calls

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Developer

**Yandri** - Computer Engineering Graduate, Utel University of Mexico

- GitHub: [@yandri918](https://github.com/yandri918)
- Email: your-email@example.com

---

## 🙏 Acknowledgments

- Flask community for excellent documentation
- Indonesian farmers for inspiration
- Open-source ML libraries (scikit-learn, SHAP, LightGBM)

---

**© 2025 AgriSensa. Built with 🌱 for sustainable agriculture.**
