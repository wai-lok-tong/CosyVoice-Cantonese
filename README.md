# CosyVoice Cantonese TTS · 粵語文字轉語音

A **Cantonese text-to-speech web UI** built on [Fun-CosyVoice 3.0](https://github.com/FunAudioLLM/CosyVoice).

Enter Cantonese text, choose a voice (female, male, emotional styles, or custom clone), and generate natural speech. Results play in the browser and save automatically to `outputs/`.

**Author:** [wai-lok-tong](https://github.com/wai-lok-tong)

**Based on:** [FunAudioLLM/CosyVoice](https://github.com/FunAudioLLM/CosyVoice) · [Upstream README](docs/UPSTREAM-README.md)

---

## Features

- Gradio web UI for Cantonese input
- **10 voice presets** — female, male, happy, sad, angry, fast, slow, robot, Peppa Pig, custom clone
- Speed slider (0.5×–2.0×) and reproducible seed
- Auto-save every generation to `outputs/`
- One-click Windows setup (Python 3.10 + venv)
- NVIDIA GPU support, including RTX 50-series (CUDA 12.8)

---

## Quick start (Windows)

```powershell
# 1. Install Python 3.10 (Python Install Manager)
py install 3.10

# 2. Clone
git clone https://github.com/wai-lok-tong/CosyVoice-Cantonese.git
cd CosyVoice-Cantonese
git submodule update --init --recursive

# 3. Setup (first time — installs deps + downloads ~1.5 GB model)
.\setup_cantonese_ui_venv.ps1

# 4. Run
.\run_cantonese_ui.bat
```

Open **http://localhost:7860** · Stop with `.\stop_cantonese_ui.bat`

> **RTX 5060 / 5070 / 5090:** After setup, upgrade PyTorch to CUDA 12.8 — see [Troubleshooting](docs/TROUBLESHOOTING.md#cuda-error-no-kernel-image-is-available-for-execution-on-the-device).

---

## Using the UI

| Step | Action |
|------|--------|
| 1 | Type Cantonese text — e.g. `今日天气好好，我哋出去行下啦。` |
| 2 | Pick a **voice** preset |
| 3 | Adjust **speed** and **seed** (optional) |
| 4 | Click **生成语音 Generate** |
| 5 | Play audio or find the saved file under **保存路径 Saved WAV** |

### Voice presets

| Preset | 说明 |
|--------|------|
| 女声 Female | Soft female voice |
| 男声 Male | Deeper male voice |
| 开心 / 伤心 / 生气 | Happy / sad / angry tone |
| 快速 / 慢速 | Fast / slow speech |
| 机器人 Robot | Robotic style |
| 小猪佩奇 Peppa Pig | Cute cartoon style |
| 自定义 Custom | Clone from your own 3–30 s reference audio |

---

## Output files

```
outputs/20260712_153045_女声_今日天气好好.wav
```

Format: `YYYYMMDD_HHMMSS_<voice>_<text>.wav` — local only, not committed to git.

---

## Scripts

| File | Purpose |
|------|---------|
| `cantonese_webui.py` | Main Gradio app |
| `setup_cantonese_ui_venv.ps1` | Setup with python.org + venv |
| `run_cantonese_ui.bat` | Start UI |
| `stop_cantonese_ui.bat` | Stop UI / free port 7860 |
| `scripts/download_model.py` | Download model only |

---

## Documentation

| Doc | Contents |
|-----|----------|
| [docs/STRUCTURE.md](docs/STRUCTURE.md) | Project layout and file map |
| [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) | Common errors (GPU, ports, install) |
| [docs/UPSTREAM-README.md](docs/UPSTREAM-README.md) | Original CosyVoice README |

---

## Model

Uses **Fun-CosyVoice3-0.5B** with Cantonese / Guangdong dialect instruct mode.

- [HuggingFace](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512)
- [ModelScope](https://www.modelscope.cn/models/FunAudioLLM/Fun-CosyVoice3-0.5B-2512)
- Local: `pretrained_models/Fun-CosyVoice3-0.5B/`

---

## Credits & license

- TTS engine: [FunAudioLLM / CosyVoice](https://github.com/FunAudioLLM/CosyVoice)
- Cantonese UI, scripts, docs: [wai-lok-tong](https://github.com/wai-lok-tong)
- License: [Apache 2.0](LICENSE)
