# The Hidden Systems Studio - Launcher Script
$env:PYTHONPATH = $PSScriptRoot

Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host "         THE HIDDEN SYSTEMS STUDIO - PRODUCTION APPLICATION" -ForegroundColor Yellow
Write-Host "=======================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/2] Starting Studio Backend API on http://localhost:8000 ..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PYTHONPATH='$PSScriptRoot'; python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"

Start-Sleep -Seconds 2
Write-Host "[2/2] Opening Studio Desktop Interface in default browser ..." -ForegroundColor Green
Start-Process "http://localhost:8000/"

Write-Host ""
Write-Host "Studio Engine is active!" -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8000/docs"
Write-Host "Dashboard:   http://localhost:3000"
