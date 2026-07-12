# Troubleshooting

Common issues when running **CosyVoice Cantonese TTS** on Windows.

---

## Web UI / connection

### `ERR_CONNECTION_REFUSED` on http://localhost:7860

**Cause:** No server is listening on port 7860.

**Fix:**

1. Run `.\run_cantonese_ui.bat`
2. Wait until you see: `Running on local URL: http://0.0.0.0:7860`
3. Then open the browser

### `Cannot find empty port in range: 7860-7860`

**Cause:** You started the UI twice. The first instance still owns port 7860.

**Fix:**

```powershell
.\stop_cantonese_ui.bat
.\run_cantonese_ui.bat
```

Only run **one** UI instance at a time.

### PowerShell: `run_cantonese_ui.bat` not recognized

**Cause:** PowerShell does not run scripts from the current directory by default.

**Fix:** Use `.\run_cantonese_ui.bat` (note the `.\` prefix).

---

## Python / environment

### `Python 3.10 not found`

CosyVoice requires Python **3.10**, not 3.14.

**Fix (Python Install Manager):**

```powershell
py install 3.10
py -0p
.\setup_cantonese_ui_venv.ps1
```

### `ModuleNotFoundError: No module named 'gradio'`

**Cause:** Dependencies not installed or wrong Python used.

**Fix:** Run setup again, then always start via `.\run_cantonese_ui.bat` (uses `.venv`).

### `openai-whisper` build fails during pip install

**Fix:**

```powershell
.\.venv\Scripts\pip.exe install "setuptools<81" wheel
.\.venv\Scripts\pip.exe install --no-build-isolation openai-whisper==20231117
.\.venv\Scripts\pip.exe install -r requirements.txt
```

---

## GPU / CUDA

### `CUDA error: no kernel image is available for execution on the device`

**Cause:** PyTorch was built for older GPUs (cu121 / sm_90). RTX 50-series needs **CUDA 12.8** (sm_120).

**Fix:**

```powershell
.\.venv\Scripts\pip.exe install --upgrade torch torchaudio --index-url https://download.pytorch.org/whl/cu128
```

Verify:

```powershell
.\.venv\Scripts\python.exe -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

Expected: `2.x.x+cu128 True NVIDIA GeForce RTX ...`

### `WinError 1114` loading `c10.dll`

**Cause:** PyTorch CUDA DLLs not found or load order issue on Windows.

**Fix:**

1. Always start via `.\run_cantonese_ui.bat` (adds torch lib to PATH)
2. Close other heavy GPU apps (ComfyUI, etc.) and retry
3. Restart the terminal and run again

### `CUDAExecutionProvider` not available (onnxruntime warning)

This warning is normal on Windows when ONNX Runtime uses CPU. Core TTS still runs on GPU via PyTorch. You can ignore it unless inference is very slow.

---

## Model / generation

### `OSError: model.safetensors not found` in CosyVoice-BlankEN

**Cause:** Model download incomplete.

**Fix:**

```powershell
.\.venv\Scripts\python.exe scripts\download_model.py --source huggingface
```

Wait until all ~1.5 GB finishes before starting the UI.

### Gradio shows `Error` when clicking Generate

Check the terminal running `cantonese_webui.py` for the full traceback. Common causes:

- CUDA mismatch (see above)
- Missing `torchcodec` (install: `pip install torchcodec`)
- Missing prompt WAV in `asset/`

### `ImportError: TorchCodec is required`

**Fix:**

```powershell
.\.venv\Scripts\pip.exe install torchcodec
```

The fork also patches `load_wav()` to fall back to `soundfile` if torchaudio fails.

---

## Git / GitHub

### `Repository not found` on push

**Cause:** GitHub repo does not exist yet, or not logged in.

**Fix:**

```powershell
gh auth login
gh repo create CosyVoice-Cantonese --public
git push -u origin main
```

### `failed to push` / missing git object

**Cause:** Shallow clone missing history objects.

**Fix:**

```powershell
git fetch upstream --unshallow
git push -u origin main
```

---

## Performance tips

- First generation loads the model and is slow (~10–30 s); later runs are faster.
- Use an NVIDIA GPU with 8 GB+ VRAM.
- Keep the terminal open while using the UI.
- Close duplicate UI instances to avoid port conflicts.
