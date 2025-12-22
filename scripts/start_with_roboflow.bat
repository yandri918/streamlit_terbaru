@echo off
echo ========================================
echo  AGRISENSA API - START WITH ROBOFLOW
echo ========================================
echo.

REM Set Roboflow API Key
set ROBOFLOW_API_KEY=your_key_here

echo [OK] Roboflow API Key set!
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python first.
    pause
    exit /b 1
)

echo [OK] Python found!
echo.

REM Start the server
echo Starting AgriSensa API with Roboflow AI...
echo.
echo Modul 20 (Roboflow AI) is now ACTIVE!
echo.
echo Open browser: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python run.py

pause
