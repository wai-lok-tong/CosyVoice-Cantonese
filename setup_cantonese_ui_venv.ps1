# CosyVoice Cantonese TTS - setup using python.org Python + venv
# Requires: Python 3.10 from https://www.python.org/downloads/release/python-31011/

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot
$VenvDir = Join-Path $ProjectRoot ".venv"

Write-Host "=== CosyVoice Cantonese TTS Setup (python.org + venv) ===" -ForegroundColor Cyan
Write-Host "Project: $ProjectRoot"

# 1. Find Python 3.10
$py310 = $null
foreach ($cmd in @("py -3.10", "python3.10", "python")) {
    try {
        $version = Invoke-Expression "$cmd -c `"import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')`"" 2>$null
        if ($version -eq "3.10") {
            $py310 = $cmd
            break
        }
    } catch {}
}

if (-not $py310) {
    Write-Host ""
    Write-Host "ERROR: Python 3.10 not found." -ForegroundColor Red
    Write-Host ""
    Write-Host "You have Python 3.14, but CosyVoice needs Python 3.10."
    Write-Host "Install it from python.org (both versions can coexist):"
    Write-Host "  https://www.python.org/downloads/release/python-31011/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "During install, check:"
    Write-Host "  [x] Add python.exe to PATH"
    Write-Host "  [x] Install py launcher"
    Write-Host ""
    Write-Host "Then re-run this script."
    exit 1
}

Write-Host "`n[1/5] Using: $py310"
Write-Host "       version: $(Invoke-Expression "$py310 --version")"

# 2. Create virtual environment
Write-Host "`n[2/5] Creating virtual environment at .venv ..."
if (Test-Path $VenvDir) {
    Write-Host "       .venv already exists, reusing it."
} else {
    Invoke-Expression "$py310 -m venv `"$VenvDir`""
}
$pip = Join-Path $VenvDir "Scripts\pip.exe"
$python = Join-Path $VenvDir "Scripts\python.exe"

# 3. Install dependencies
Write-Host "`n[3/5] Installing dependencies (may take several minutes)..."
& $python -m pip install --upgrade pip setuptools wheel
Push-Location $ProjectRoot
& $pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Some packages failed; retrying core inference dependencies..." -ForegroundColor Yellow
    & $pip install "setuptools<81" wheel
    & $pip install openai-whisper==20231117 pyworld==0.3.4
    & $pip install -r requirements.txt
}
Pop-Location

# 4. Init submodules
Write-Host "`n[4/5] Initializing submodules..."
Push-Location $ProjectRoot
git submodule update --init --recursive
Pop-Location

# 5. Download assets if missing
$assetDir = Join-Path $ProjectRoot "asset"
if (-not (Test-Path (Join-Path $assetDir "zero_shot_prompt.wav"))) {
    Write-Host "Downloading prompt audio assets..."
    New-Item -ItemType Directory -Force -Path $assetDir | Out-Null
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/FunAudioLLM/CosyVoice/main/asset/zero_shot_prompt.wav" `
        -OutFile (Join-Path $assetDir "zero_shot_prompt.wav")
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/FunAudioLLM/CosyVoice/main/asset/cross_lingual_prompt.wav" `
        -OutFile (Join-Path $assetDir "cross_lingual_prompt.wav")
}

# 6. Download model
Write-Host "`n[5/5] Downloading Fun-CosyVoice3 model (~1.5 GB, may take a while)..."
& $python (Join-Path $ProjectRoot "scripts/download_model.py")

Write-Host "`n=== Setup complete! ===" -ForegroundColor Green
Write-Host "To start the Cantonese TTS UI, run:"
Write-Host "  .\run_cantonese_ui.bat" -ForegroundColor Yellow
Write-Host "Then open http://localhost:7860 in your browser."
