@echo off
REM CosyVoice Cantonese TTS - launch script
cd /d "%~dp0"

set "PYTHON="
if exist ".venv\Scripts\python.exe" (
    set "PYTHON=.venv\Scripts\python.exe"
    echo Using python.org venv: .venv
) else (
    where conda >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set "USE_CONDA=1"
        echo Using conda environment: cosyvoice
    ) else (
        echo ERROR: No environment found.
        echo.
        echo Run setup first:
        echo   setup_cantonese_ui_venv.ps1   ^(python.org + venv^)
        echo   setup_cantonese_ui.ps1        ^(Miniconda^)
        pause
        exit /b 1
    )
)

if not exist "pretrained_models\Fun-CosyVoice3-0.5B\cosyvoice3.yaml" (
    echo Model not found. Downloading Fun-CosyVoice3...
    if defined USE_CONDA (
        call conda run -n cosyvoice python scripts\download_model.py
    ) else (
        "%PYTHON%" scripts\download_model.py
    )
)

echo.
echo Starting Cantonese TTS UI at http://localhost:7860
echo Keep this window open while using the UI.
echo.

REM Ensure torch CUDA DLLs resolve (fixes WinError 1114 on c10.dll)
if exist ".venv\Lib\site-packages\torch\lib" (
    set "PATH=%CD%\.venv\Lib\site-packages\torch\lib;%PATH%"
)

if defined USE_CONDA (
    call conda run -n cosyvoice python cantonese_webui.py --port 7860
) else (
    "%PYTHON%" cantonese_webui.py --port 7860
)

pause
