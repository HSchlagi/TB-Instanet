Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   BESS Simulation Server Starter" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location ".\project"

Write-Host "Aktivierung der virtuellen Umgebung..." -ForegroundColor Yellow
& "..\venv\Scripts\Activate.ps1"

Write-Host ""
Write-Host "Starte BESS Simulation Server..." -ForegroundColor Green
Write-Host "Server läuft auf: http://127.0.0.1:5000" -ForegroundColor Green
Write-Host ""
Write-Host "Drücke STRG+C zum Beenden" -ForegroundColor Yellow
Write-Host ""

python run.py 