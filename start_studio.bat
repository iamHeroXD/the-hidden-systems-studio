@echo off
setlocal enabledelayedexpansion
title THE HIDDEN SYSTEMS STUDIO

echo =======================================================================
echo          THE HIDDEN SYSTEMS STUDIO - PRODUCTION APPLICATION
echo =======================================================================
echo.

set ROOT_DIR=%~dp0
set PYTHONPATH=%ROOT_DIR%

:: Check if backend is already running on port 8000
powershell -NoProfile -ExecutionPolicy Bypass -Command "try { $res = Invoke-WebRequest -Uri 'http://localhost:8000/api/health' -UseBasicParsing -TimeoutSec 1; exit 0 } catch { exit 1 }"
if %ERRORLEVEL% EQU 0 (
    echo [INFO] Studio Engine backend is active on http://localhost:8000.
) else (
    echo [1/2] Starting Studio Engine on http://localhost:8000 ...
    start "The Hidden Systems Engine" /min cmd /c "set PYTHONPATH=%ROOT_DIR% && python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000"
    
    :: Wait up to 5 seconds for backend initialization
    powershell -NoProfile -ExecutionPolicy Bypass -Command "for ($i=0; $i -lt 15; $i++) { try { $r = Invoke-WebRequest -Uri 'http://localhost:8000/api/health' -UseBasicParsing -TimeoutSec 1; if ($r.StatusCode -eq 200) { exit 0 } } catch {}; Start-Sleep -Milliseconds 350 }; exit 0"
)

echo [2/2] Opening Studio Interface ...

if exist "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" (
    start "" "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --app="http://localhost:8000"
) else if exist "C:\Program Files\Google\Chrome\Application\chrome.exe" (
    start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --app="http://localhost:8000"
) else (
    start http://localhost:8000/
)

echo.
echo =======================================================================
echo Studio Engine is now operational at http://localhost:8000
echo =======================================================================
timeout /t 2 /nobreak >nul
exit /b 0
