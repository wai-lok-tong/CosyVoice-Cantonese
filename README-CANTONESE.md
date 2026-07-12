# CosyVoice Cantonese TTS

A **Cantonese (粤语) text-to-speech web UI** built on top of [Fun-CosyVoice 3.0](https://github.com/FunAudioLLM/CosyVoice).

Type Cantonese text, pick a voice style, and generate natural speech. Audio is played in the browser and saved automatically to `outputs/`.

**Repository:** [github.com/wai-lok-tong/CosyVoice-Cantonese](https://github.com/wai-lok-tong/CosyVoice-Cantonese)  
**Upstream:** [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice)

---

## Features

- Web UI (Gradio) for Cantonese text input
- **10 voice presets:** female, male, happy, sad, angry, fast, slow, robot, Peppa Pig style, custom clone
- Speed control (0.5×–2.0×) and reproducible seed
- Auto-save every generation to `outputs/`
- Windows setup scripts (Python 3.10 + venv)
- GPU acceleration (NVIDIA, including RTX 50-series with CUDA 12.8 PyTorch)

---

## Requirements

| Item | Version / notes |
|------|-----------------|
| OS | Windows 10/11 (scripts tested on Windows) |
| Python | **3.10** (via [Python Install Manager](https://docs.python.org/3/using/windows.html) or python.org) |
| GPU | NVIDIA GPU recommended (8 GB+ VRAM); CPU fallback is very slow |
| Disk | ~2 GB for model + dependencies |
| Git | Optional, for cloning |

### RTX 50-series (5060 / 5070 / 5090)

These GPUs need **PyTorch with CUDA 12.8** (`cu128`), not the default `cu121` in `requirements.txt`:

```powershell
.\.venv\Scripts\pip.exe install --upgrade torch torchaudio --index-url https://download.pytorch.org/whl/cu128
```

See [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) for details.

---

## Quick start (Windows)

### 1. Install Python 3.10

If you use **Python Install Manager** (recommended on Windows):

```powershell
py install 3.10
py -0p
```

### 2. Clone this repo

```powershell
git clone https://github.com/wai-lok-tong/CosyVoice-Cantonese.git
cd CosyVoice-Cantonese
git submodule update --init --recursive
```

### 3. Run setup (first time only)

```powershell
.\setup_cantonese_ui_venv.ps1
```

This will:

- Create `.venv` (Python 3.10 virtual environment)
- Install dependencies from `requirements.txt`
- Download **Fun-CosyVoice3-0.5B** (~1.5 GB) into `pretrained_models/`

### 4. Start the UI

```powershell
.\run_cantonese_ui.bat
```

Open **http://localhost:7860** in your browser. Keep the terminal window open while using the UI.

### 5. Stop the UI

```powershell
.\stop_cantonese_ui.bat
```

---

## How to use the web UI

1. **粤语文字** — Enter Cantonese text (e.g. `今日天气好好，我哋出去行下啦。`)
2. **声线选择 Voice** — Pick a preset (female, male, emotional styles, etc.)
3. **语速 Speed** — Adjust speaking rate
4. **随机种子 Seed** — Same seed + text → similar output
5. Click **生成语音 Generate**
6. Listen in the player; check **保存路径 Saved WAV** for the file path

### Voice presets

| Preset | Description |
|--------|-------------|
| 女声 Female | Soft female voice |
| 男声 Male | Deeper male voice |
| 开心 Happy | Cheerful tone |
| 伤心 Sad | Sad tone |
| 生气 Angry | Angry tone |
| 快速 Fast | Faster speech |
| 慢速 Slow | Slower speech |
| 机器人 Robot | Robotic style |
| 小猪佩奇 Peppa Pig | Cute cartoon style |
| 自定义 Custom | Upload 3–30 s reference audio to clone a voice |

### Custom voice

1. Select **自定义 Custom**
2. Upload or record a short reference clip (16 kHz+, 3–30 seconds)
3. Enter Cantonese text and generate

---

## Output files

Generated audio is saved to:

```
outputs/
  20260712_153045_女声_你好我係Kaia.wav
```

Filename format: `YYYYMMDD_HHMMSS_<voice>_<text_snippet>.wav`

This folder is git-ignored and not uploaded to GitHub.

---

## Scripts reference

| Script | Purpose |
|--------|---------|
| `setup_cantonese_ui_venv.ps1` | Full setup with python.org + venv (recommended) |
| `setup_cantonese_ui.ps1` | Setup with Miniconda/conda |
| `run_cantonese_ui.bat` | Start web UI on port 7860 |
| `stop_cantonese_ui.bat` | Stop UI and free port 7860 |
| `scripts/download_model.py` | Download Fun-CosyVoice3 model only |

### Manual commands

```powershell
# Download model only
.\.venv\Scripts\python.exe scripts\download_model.py --source huggingface

# Start UI on a different port
.\.venv\Scripts\python.exe cantonese_webui.py --port 8080

# Public Gradio link (temporary share URL)
.\.venv\Scripts\python.exe cantonese_webui.py --share
```

---

## Project structure

See [docs/STRUCTURE.md](docs/STRUCTURE.md) for a full layout.

Key paths:

```
CosyVoice-Cantonese/
├── cantonese_webui.py      # Cantonese Gradio UI (main entry)
├── run_cantonese_ui.bat    # Launch script
├── stop_cantonese_ui.bat   # Stop script
├── setup_cantonese_ui_venv.ps1
├── scripts/download_model.py
├── asset/                  # Bundled prompt audio for voice presets
├── outputs/                # Generated WAV files (local only)
├── pretrained_models/      # Downloaded model weights (local only)
├── cosyvoice/              # Core CosyVoice library (upstream)
└── docs/                   # This fork's documentation
```

---

## Troubleshooting

Common issues:

| Problem | Fix |
|---------|-----|
| `ERR_CONNECTION_REFUSED` on :7860 | UI not running — run `.\run_cantonese_ui.bat` and wait for `Running on local URL` |
| Port already in use | Run `.\stop_cantonese_ui.bat`, then start again |
| `CUDA error: no kernel image` | Upgrade to PyTorch cu128 (RTX 50-series) |
| `WinError 1114` on `c10.dll` | Restart UI via `run_cantonese_ui.bat` (sets torch DLL path) |
| `Repository not found` on push | Create GitHub repo first |

Full guide: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## Model

This UI uses **Fun-CosyVoice3-0.5B**, which supports Cantonese / Guangdong dialect via instruct mode:

- Model: [HuggingFace](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512) / [ModelScope](https://www.modelscope.cn/models/FunAudioLLM/Fun-CosyVoice3-0.5B-2512)
- Local path: `pretrained_models/Fun-CosyVoice3-0.5B/`

---

## Credits

- [FunAudioLLM / CosyVoice](https://github.com/FunAudioLLM/CosyVoice) — base TTS model and library
- Cantonese UI, Windows scripts, and docs — [wai-lok-tong](https://github.com/wai-lok-tong)

## License

This project inherits the [Apache 2.0 license](LICENSE) from upstream CosyVoice.
