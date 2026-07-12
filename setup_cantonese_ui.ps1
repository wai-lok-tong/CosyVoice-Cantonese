# CosyVoice Cantonese TTS - Windows setup script
# Requires: Miniconda/Anaconda (https://docs.conda.io/en/latest/miniconda.html)

$ErrorActionPreference = "Stop"
$ProjectRoot = $PSScriptRoot

Write-Host "=== CosyVoice Cantonese TTS Setup ===" -ForegroundColor Cyan
Write-Host "Project: $ProjectRoot"

# 1. Create conda environment (Python 3.10 required by CosyVoice)
$envName = "cosyvoice"
$condaExists = Get-Command conda -ErrorAction SilentlyContinue
if (-not $condaExists) {
    Write-Host "ERROR: conda not found. Please install Miniconda first." -ForegroundColor Red
    Write-Host "  https://docs.conda.io/en/latest/miniconda.html"
    exit 1
}

Write-Host "`n[1/4] Creating conda environment '$envName' (Python 3.10)..."
conda create -n $envName python=3.10 -y

Write-Host "`n[2/4] Installing dependencies..."
Push-Location $ProjectRoot
conda run -n $envName pip install -r requirements.txt
Pop-Location

# 2. Init git submodules (Matcha-TTS)
Write-Host "`n[3/4] Initializing submodules..."
Push-Location $ProjectRoot
git submodule update --init --recursive
Pop-Location

# 3. Download assets if missing
$assetDir = Join-Path $ProjectRoot "asset"
if (-not (Test-Path (Join-Path $assetDir "zero_shot_prompt.wav"))) {
    Write-Host "Downloading prompt audio assets..."
    New-Item -ItemType Directory -Force -Path $assetDir | Out-Null
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/FunAudioLLM/CosyVoice/main/asset/zero_shot_prompt.wav" `
        -OutFile (Join-Path $assetDir "zero_shot_prompt.wav")
    Invoke-WebRequest -Uri "https://raw.githubusercontent.com/FunAudioLLM/CosyVoice/main/asset/cross_lingual_prompt.wav" `
        -OutFile (Join-Path $assetDir "cross_lingual_prompt.wav")
}

# 4. Download model
Write-Host "`n[4/4] Downloading Fun-CosyVoice3 model (~1.5 GB, may take a while)..."
conda run -n $envName python (Join-Path $ProjectRoot "scripts/download_model.py")

Write-Host "`n=== Setup complete! ===" -ForegroundColor Green
Write-Host "To start the Cantonese TTS UI, run:"
Write-Host "  .\run_cantonese_ui.bat" -ForegroundColor Yellow
Write-Host "Then open http://localhost:7860 in your browser."
