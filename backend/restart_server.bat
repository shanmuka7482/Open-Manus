@echo off
echo Stopping any existing server processes...
echo.

REM Kill any existing uvicorn/fastapi servers on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do (
    echo Found process using port 8000: %%a
    taskkill /F /PID %%a 2>nul
)

timeout /t 2 /nobreak >nul

echo.
echo Starting new server with proper Windows configuration...
echo.

python start_server.py

pause
