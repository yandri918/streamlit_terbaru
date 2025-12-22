@echo off
echo ==========================================
echo    STARTING AGRISENSA ECOSYSTEM v4.0
echo ==========================================

echo [1/6] Launching Main Hub (Port 8501)...
start "AgriSensa Main Hub" cmd /k "cd agrisensa_streamlit && python -m streamlit run Home.py --server.port 8501"

echo [2/6] Launching Commodities App (Port 8502)...
start "AgriSensa Commodities" cmd /k "cd agrisensa_commodities && python -m streamlit run Home.py --server.port 8502"

echo [3/6] Launching Tech App (Port 8503)...
start "AgriSensa Tech" cmd /k "cd agrisensa_tech && python -m streamlit run Home.py --server.port 8503"

echo [4/6] Launching Biz App (Port 8504)...
start "AgriSensa Biz" cmd /k "cd agrisensa_biz && python -m streamlit run Home.py --server.port 8504"

echo [5/6] Launching Eco App (Port 8505)...
start "AgriSensa Eco" cmd /k "cd agrisensa_eco && python -m streamlit run Home.py --server.port 8505"

echo [6/6] Launching Livestock App (Port 8506)...
start "AgriSensa Livestock" cmd /k "cd agrisensa_livestock && python -m streamlit run Home.py --server.port 8506"

echo.
echo ==========================================
echo    ALL SYSTEMS DEPLOYED SUCCESSFULLY
echo ==========================================
echo.
echo Access the Main Hub at: http://localhost:8501
pause
