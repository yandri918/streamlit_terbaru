# Changelog - AgriSensa API

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-01-28

### 🎉 Major Refactoring - Production-Ready Release

This is a complete rewrite of the AgriSensa API with focus on scalability, security, and maintainability.

### ✨ Added

#### Architecture & Structure
- **Modular Architecture**: Implemented Blueprint pattern for better code organization
- **Service Layer**: Separated business logic from routes
- **Application Factory**: Created `create_app()` factory pattern for better testing
- **Configuration Management**: Environment-based configuration (Development, Production, Testing)

#### Security & Authentication
- **JWT Authentication**: Implemented Flask-JWT-Extended for secure authentication
- **User Management**: Complete user registration, login, and profile management
- **Rate Limiting**: Added Flask-Limiter to prevent API abuse
- **CORS Support**: Proper cross-origin resource sharing configuration
- **Password Hashing**: Secure password storage with Werkzeug

#### Database & Models
- **User Model**: User authentication and profile management
- **Enhanced NPK Reading Model**: Added user relationship and location tracking
- **Recommendation Model**: Track user recommendations with feedback
- **Crop Model**: Track crop cultivation and yield data
- **Database Migrations**: Flask-Migrate (Alembic) for schema versioning

#### API Endpoints
- **Authentication Routes** (`/api/auth`):
  - POST `/register` - User registration
  - POST `/login` - User login
  - POST `/refresh` - Token refresh
  - GET `/me` - Get current user
  - PUT `/me` - Update user profile
  - POST `/change-password` - Change password

- **Analysis Routes** (`/api/analysis`):
  - POST `/bwd` - Leaf analysis
  - POST `/npk` - NPK analysis
  - GET `/npk/history` - NPK reading history

- **Recommendation Routes** (`/api/recommendation`):
  - POST `/fertilizer` - Fertilizer recommendation
  - POST `/calculate-fertilizer` - Calculate dosage
  - POST `/integrated` - Integrated recommendation
  - POST `/spraying` - Spraying strategy
  - GET `/history` - Recommendation history

- **Knowledge Routes** (`/api/knowledge`):
  - GET `/crop/<commodity>` - Crop knowledge
  - GET `/guide/<commodity>` - Commodity guide
  - GET `/ph-info` - pH information
  - GET `/diagnostic-tree` - Disease diagnostic
  - GET `/fertilizer-data` - Fertilizer data

- **Market Routes** (`/api/market`):
  - POST `/prices` - Current prices
  - GET `/ticker` - Ticker prices
  - POST `/historical` - Historical prices

- **ML Routes** (`/api/ml`):
  - POST `/recommend-crop` - Crop recommendation
  - POST `/predict-yield` - Yield prediction
  - POST `/predict-yield-advanced` - Advanced XAI prediction
  - POST `/generate-yield-plan` - Yield planning
  - POST `/calculate-fertilizer-bags` - Fertilizer calculation

#### Error Handling & Logging
- **Custom Error Handlers**: Proper HTTP status codes for all errors
- **Structured Logging**: Rotating file handler with configurable levels
- **Error Tracking Ready**: Prepared for Sentry integration

#### Development Tools
- **CLI Commands**:
  - `flask init-db` - Initialize database
  - `flask seed-db` - Seed sample data
  - `flask create-admin` - Create admin user
- **Environment Variables**: `.env` file support with python-dotenv
- **Testing Framework**: Pytest structure ready

#### Documentation
- **README_NEW.md**: Comprehensive documentation
- **CHANGELOG.md**: Version history tracking
- **.env.example**: Environment variable template
- **API Documentation Ready**: Structure for Swagger/OpenAPI

### 🔄 Changed

#### Breaking Changes
- **Entry Point**: Changed from `app.py` to `run.py`
- **URL Structure**: All API endpoints now have `/api/` prefix
- **Authentication**: Some endpoints now require JWT token
- **Database Schema**: New tables and relationships

#### Improvements
- **ML Model Loading**: Lazy loading with thread-safe caching
- **Code Organization**: Clear separation of concerns
- **Error Messages**: More descriptive and consistent
- **Response Format**: Standardized JSON responses
- **Configuration**: Environment-based settings

### 📦 Dependencies

#### New Dependencies
- `Flask-JWT-Extended==4.6.0` - JWT authentication
- `Flask-Limiter==3.5.0` - Rate limiting
- `Flask-CORS==4.0.0` - CORS support
- `Flask-Migrate==4.0.5` - Database migrations
- `python-dotenv==1.0.0` - Environment variables
- `redis==5.0.1` - Caching support
- `pytest==7.4.3` - Testing framework

#### Updated Dependencies
- `Flask==3.0.0` (from 2.x)
- `SQLAlchemy==2.0.23` (from 1.x)
- `numpy==1.26.2`
- `pandas==2.1.4`
- `scikit-learn==1.3.2`

### 🗂️ File Structure

```
New Structure:
├── app/
│   ├── config/          # Configuration
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── utils/           # Utilities
│   └── ml_models/       # ML model management
├── migrations/          # Database migrations
├── tests/              # Test files
├── .env                # Environment variables
├── run.py              # Entry point
└── README_NEW.md       # Documentation
```

### 🔒 Security Improvements

- Password hashing with Werkzeug
- JWT token-based authentication
- Rate limiting on sensitive endpoints
- CORS configuration
- SQL injection protection (SQLAlchemy ORM)
- Input validation and sanitization
- Secure session management

### 📊 Performance Improvements

- Lazy loading for ML models
- Thread-safe model caching
- Database connection pooling
- Prepared for Redis caching
- Optimized query patterns

### 🐛 Bug Fixes

- Fixed model loading race conditions
- Improved error handling in ML predictions
- Better validation for input data
- Fixed memory leaks in image processing

### 📝 Migration Guide

See README_NEW.md for detailed migration instructions from v1.0 to v2.0.

---

## [1.0.0] - 2024-XX-XX

### Initial Release

- Basic Flask application
- ML model integration
- Leaf and soil analysis
- Fertilizer recommendations
- Knowledge base
- Market price simulation
- Single-file architecture (app.py)

---

## Future Roadmap

### [2.1.0] - Planned
- [ ] Swagger/OpenAPI documentation
- [ ] Redis caching implementation
- [ ] Celery for async tasks
- [ ] WebSocket support for real-time updates
- [ ] Enhanced analytics dashboard

### [2.2.0] - Planned
- [ ] Docker containerization
- [ ] Kubernetes deployment configs
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Automated testing in CI
- [ ] Performance monitoring

### [3.0.0] - Planned
- [ ] GraphQL API
- [ ] Real-time market data integration
- [ ] Mobile app backend support
- [ ] Multi-language support (i18n)
- [ ] Advanced analytics and reporting

---

**Note**: This changelog follows [Keep a Changelog](https://keepachangelog.com/) format.
