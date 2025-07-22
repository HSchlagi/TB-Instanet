@echo off
echo ========================================
echo    BESS Simulation Server Starter
echo ========================================
echo.

cd /d "%~dp0project"

echo Aktivierung der virtuellen Umgebung...
call ..\venv\Scripts\activate.bat

echo.
echo Starte BESS Simulation Server...
echo Server läuft auf: http://127.0.0.1:5000
echo.
echo Drücke STRG+C zum Beenden
echo.

python run.py

pause 