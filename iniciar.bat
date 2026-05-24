@echo off
title GrowthData Analytics - Project Controls
cd /d "%~dp0"
echo Iniciando GrowthData Analytics...
echo Abrir en el navegador: http://localhost:8502
echo Presiona Ctrl+C para detener.
echo.
python -m streamlit run app.py --server.port 8502 --browser.gatherUsageStats false
pause
