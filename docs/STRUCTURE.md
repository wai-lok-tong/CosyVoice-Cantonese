# Project structure

This document describes the layout of **CosyVoice-Cantonese** — what each part does and what is (or is not) tracked in git.

---

## Overview

```
CosyVoice-Cantonese/
│
├──── Cantonese UI (this fork) ─────────────────────────────
│   ├── cantonese_webui.py          Main Gradio web application
│   ├── run_cantonese_ui.bat        Start UI (Windows)
│   ├── stop_cantonese_ui.bat       Stop UI / free port 7860
│   ├── setup_cantonese_ui_venv.ps1 One-time setup (python.org + venv)
│   ├── setup_cantonese_ui.ps1      One-time setup (Miniconda)
│   ├── scripts/
│   │   └── download_model.py       Download Fun-CosyVoice3 weights
│   ├── docs/
│   │   ├── STRUCTURE.md            This file
│   │   └── TROUBLESHOOTING.md      Common errors and fixes
│   ├── README-CANTONESE.md         Main usage guide for this fork
│   └── outputs/                    Generated WAV files (git-ignored)
│
├──── Runtime data (local only, git-ignored) ───────────────
│   ├── .venv/                      Python virtual environment
│   └── pretrained_models/
│       └── Fun-CosyVoice3-0.5B/    ~1.5 GB model weights
│
├──── Upstream CosyVoice ───────────────────────────────────
│   ├── cosyvoice/                  Core Python package
│   │   ├── cli/                    CLI & inference API
│   │   │   ├── cosyvoice.py        AutoModel, inference_* methods
│   │   │   ├── frontend.py         Text/audio frontend
│   │   │   └── model.py            Neural model wrappers
│   │   ├── llm/                    Language model components
│   │   ├── flow/                   Flow-matching decoder
│   │   ├── hifigan/                Vocoder
│   │   ├── tokenizer/              Text tokenizer
│   │   └── utils/                  Helpers (incl. load_wav patch)
│   ├── third_party/Matcha-TTS/     Git submodule (required)
│   ├── asset/                      Sample prompt WAVs
│   │   ├── zero_shot_prompt.wav    Female-style reference
│   │   └── cross_lingual_prompt.wav Male-style reference
│   ├── webui.py                    Upstream generic Gradio UI
│   ├── example.py                  Upstream usage examples
│   ├── requirements.txt            Python dependencies
│   └── README.md                   Upstream documentation
│
└──── Other upstream folders ───────────────────────────────
    ├── examples/                   Training / fine-tuning scripts
    ├── runtime/                    FastAPI, gRPC, Triton deployment
    └── tools/                      Data prep utilities
```

---

## Cantonese UI flow

```
User browser (localhost:7860)
        │
        ▼
cantonese_webui.py  (Gradio)
        │
        ├── Voice preset → prompt WAV + instruct text
        ├── User text    → Cantonese input
        │
        ▼
cosyvoice.cli.AutoModel  (Fun-CosyVoice3)
        │
        ├── inference_instruct2()
        │
        ▼
outputs/YYYYMMDD_HHMMSS_*.wav
```

---

## Files added by this fork

| File | Role |
|------|------|
| `cantonese_webui.py` | Gradio UI, voice presets, auto-save to `outputs/` |
| `run_cantonese_ui.bat` | Launches UI with correct venv and DLL paths |
| `stop_cantonese_ui.bat` | Kills process on port 7860 |
| `setup_cantonese_ui_venv.ps1` | Creates `.venv`, installs deps, downloads model |
| `setup_cantonese_ui.ps1` | Same via conda |
| `scripts/download_model.py` | Model download helper |
| `cosyvoice/utils/file_utils.py` | Patched `load_wav()` for Windows / torchaudio 2.11 |
| `README-CANTONESE.md` | Usage documentation |
| `docs/` | Structure and troubleshooting |

---

## Git remotes

| Remote | URL | Purpose |
|--------|-----|---------|
| `origin` | `wai-lok-tong/CosyVoice-Cantonese` | Your fork on GitHub |
| `upstream` | `FunAudioLLM/CosyVoice` | Original CosyVoice repo |

Pull upstream updates:

```powershell
git fetch upstream
git merge upstream/main
```

---

## What is NOT in git

These are excluded via `.gitignore` and must be created locally:

| Path | How to get it |
|------|----------------|
| `.venv/` | Run `setup_cantonese_ui_venv.ps1` |
| `pretrained_models/` | Setup script or `scripts/download_model.py` |
| `outputs/` | Created automatically when you generate speech |
| `*.wav` (except `asset/`) | Generated audio |
