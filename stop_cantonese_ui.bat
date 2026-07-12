@echo off
REM Stop CosyVoice Cantonese UI and free port 7860
cd /d "%~dp0"

echo Looking for processes on port 7860...
set "FOUND="
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":7860" ^| findstr "LISTENING"') do (
  set "FOUND=1"
  echo Killing PID %%P
  taskkill /PID %%P /F >nul 2>&1
)

if not defined FOUND (
  echo No LISTENING process on port 7860.
) else (
  timeout /t 2 /nobreak >nul
)

echo.
echo Remaining 7860 connections:
netstat -ano | findstr ":7860"
if errorlevel 1 (
  echo Port 7860 is clear.
) else (
  echo Note: TIME_WAIT lines are normal and clear themselves in ~1-2 minutes.
  echo As long as nothing shows LISTENING, you can start the UI again.
)

echo.
pause
