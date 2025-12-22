@echo off
echo ========================================
echo   AGRISENSA API v2.0 - QUICK START
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python not found! Please install Python 3.8 or higher.
    pause
    exit /b 1
)
echo.

echo [2/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies!
    pause
    exit /b 1
)
echo.

echo [3/5] Initializing database...
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database initialized successfully!')"
if errorlevel 1 (
    echo ERROR: Failed to initialize database!
    pause
    exit /b 1
)
echo.

echo [4/5] Creating admin user...
python -c "from app import create_app, db; from app.models import User; app = create_app(); app.app_context().push(); admin = User(username='admin', email='admin@agrisensa.com', full_name='Administrator', role='admin'); admin.set_password('admin123'); db.session.add(admin); db.session.commit(); print('Admin user created: admin/admin123')"
echo.

echo [5/5] Starting application...
echo.
echo ========================================
echo   APPLICATION STARTING...
echo   URL: http://localhost:5000
echo   Admin: admin / admin123
echo   Press CTRL+C to stop
echo ========================================
echo.

python run.py
