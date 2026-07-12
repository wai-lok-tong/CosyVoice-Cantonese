# Copyright (c) 2024 Alibaba Inc (authors: Xiang Lyu, Liu Yue)
# Cantonese TTS UI - built on CosyVoice3
import argparse
import os
import random
import re
import sys
from datetime import datetime

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(ROOT_DIR, "outputs")


def _prepare_torch_dll_path():
    """Avoid WinError 1114 when loading torch CUDA DLLs on Windows."""
    candidates = [
        os.path.join(ROOT_DIR, ".venv", "Lib", "site-packages", "torch", "lib"),
        os.path.join(sys.prefix, "Lib", "site-packages", "torch", "lib"),
    ]
    for torch_lib in candidates:
        if not os.path.isdir(torch_lib):
            continue
        os.environ["PATH"] = torch_lib + os.pathsep + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            os.add_dll_directory(torch_lib)
        break


_prepare_torch_dll_path()

# Import torch before Gradio to avoid WinError 1114 DLL init races on Windows.
import torch  # noqa: E402

import gradio as gr
import numpy as np
import soundfile as sf

sys.path.append(os.path.join(ROOT_DIR, "third_party/Matcha-TTS"))

from cosyvoice.cli.cosyvoice import AutoModel
from cosyvoice.utils.common import set_all_random_seed
from cosyvoice.utils.file_utils import logging

CANTONESE_INSTRUCT = "You are a helpful assistant. 请用广东话表达。<|endofprompt|>"

VOICE_PRESETS = {
    "女声 Female": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/zero_shot_prompt.wav"),
        "instruct": CANTONESE_INSTRUCT,
        "description": "柔和女声，适合日常对话",
    },
    "男声 Male": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/cross_lingual_prompt.wav"),
        "instruct": CANTONESE_INSTRUCT,
        "description": "沉稳男声，适合播报解说",
    },
    "开心 Happy": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/zero_shot_prompt.wav"),
        "instruct": "You are a helpful assistant. 请用广东话表达。请非常开心地说一句话。<|endofprompt|>",
        "description": "活泼开心的粤语语气",
    },
    "伤心 Sad": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/zero_shot_prompt.wav"),
        "instruct": "You are a helpful assistant. 请用广东话表达。请非常伤心地说一句话。<|endofprompt|>",
        "description": "低沉伤感的粤语语气",
    },
    "生气 Angry": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/zero_shot_prompt.wav"),
        "instruct": "You are a helpful assistant. 请用广东话表达。请非常生气地说一句话。<|endofprompt|>",
        "description": "带有怒气的粤语语气",
    },
    "快速 Fast": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/zero_shot_prompt.wav"),
        "instruct": "You are a helpful assistant. 请用广东话表达。请用尽可能快地语速说一句话。<|endofprompt|>",
        "description": "语速较快的粤语",
    },
    "慢速 Slow": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/zero_shot_prompt.wav"),
        "instruct": "You are a helpful assistant. 请用广东话表达。请用尽可能慢地语速说一句话。<|endofprompt|>",
        "description": "语速较慢的粤语",
    },
    "机器人 Robot": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/zero_shot_prompt.wav"),
        "instruct": "You are a helpful assistant. 请用广东话表达。你可以尝试用机器人的方式解答吗？<|endofprompt|>",
        "description": "机械感的粤语机器人声线",
    },
    "小猪佩奇 Peppa Pig": {
        "prompt_wav": os.path.join(ROOT_DIR, "asset/zero_shot_prompt.wav"),
        "instruct": "You are a helpful assistant. 请用广东话表达。我想体验一下小猪佩奇风格，可以吗？<|endofprompt|>",
        "description": "可爱童趣的粤语风格",
    },
    "自定义 Custom": {
        "prompt_wav": None,
        "instruct": CANTONESE_INSTRUCT,
        "description": "上传参考音频，克隆任意声线",
    },
}

DEFAULT_TEXT = "你好，我係 CosyVoice 語音合成系統，歡迎使用粵語文字轉語音功能。"
VOICE_CHOICES = list(VOICE_PRESETS.keys())


def generate_seed():
    return random.randint(1, 100_000_000)


def update_voice_description(voice_name):
    return VOICE_PRESETS[voice_name]["description"]


def _safe_filename_part(text, max_len=24):
    cleaned = re.sub(r"[^\w\u4e00-\u9fff]+", "_", text.strip(), flags=re.UNICODE)
    cleaned = cleaned.strip("_") or "tts"
    return cleaned[:max_len]


def save_output_wav(audio, sample_rate, voice_name, tts_text):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    voice_tag = _safe_filename_part(voice_name.split()[0], max_len=12)
    text_tag = _safe_filename_part(tts_text)
    path = os.path.join(OUTPUT_DIR, f"{stamp}_{voice_tag}_{text_tag}.wav")
    sf.write(path, audio, sample_rate)
    logging.info("Saved output wav: %s", path)
    return path


def generate_cantonese_audio(
    tts_text,
    voice_name,
    custom_prompt_wav,
    speed,
    seed,
):
    if not tts_text or not tts_text.strip():
        gr.Warning("请输入粤语文字 / Please enter Cantonese text.")
        yield (cosyvoice.sample_rate, default_data), ""
        return

    preset = VOICE_PRESETS[voice_name]
    prompt_wav = preset["prompt_wav"]
    instruct_text = preset["instruct"]

    if voice_name == "自定义 Custom":
        if custom_prompt_wav is None:
            gr.Warning("自定义声线需要上传参考音频（3–30 秒，16kHz 以上）。")
            yield (cosyvoice.sample_rate, default_data), ""
            return
        prompt_wav = custom_prompt_wav

    if prompt_wav is None or not os.path.exists(prompt_wav):
        gr.Warning(f"参考音频不存在: {prompt_wav}")
        yield (cosyvoice.sample_rate, default_data), ""
        return

    set_all_random_seed(int(seed))
    logging.info("Cantonese TTS: voice=%s text=%s", voice_name, tts_text[:80])

    pieces = []
    for chunk in cosyvoice.inference_instruct2(
        tts_text.strip(),
        instruct_text,
        prompt_wav,
        stream=False,
        speed=float(speed),
    ):
        pieces.append(chunk["tts_speech"].numpy().flatten())

    if not pieces:
        gr.Warning("未生成音频 / No audio generated.")
        yield (cosyvoice.sample_rate, default_data), ""
        return

    audio = np.concatenate(pieces) if len(pieces) > 1 else pieces[0]
    saved_path = save_output_wav(audio, cosyvoice.sample_rate, voice_name, tts_text.strip())
    gr.Info(f"已保存: {saved_path}")
    yield (cosyvoice.sample_rate, audio), saved_path


def build_ui():
    with gr.Blocks(
        title="CosyVoice 粤语 TTS",
        theme=gr.themes.Soft(
            primary_hue="orange",
            secondary_hue="amber",
            font=gr.themes.GoogleFont("Noto Sans SC"),
        ),
        css="""
        .main-title { text-align: center; margin-bottom: 0.2rem; }
        .sub-title { text-align: center; color: #666; margin-bottom: 1.5rem; }
        """,
    ) as demo:
        gr.Markdown(
            "# 🎙️ CosyVoice 粤语文字转语音\n"
            "### Cantonese Text-to-Speech powered by [Fun-CosyVoice3](https://github.com/FunAudioLLM/CosyVoice)",
            elem_classes=["main-title"],
        )
        gr.Markdown(
            "输入粤语文字，选择声线风格，一键生成自然粤语语音。"
            "支持女声、男声及多种特殊语气。",
            elem_classes=["sub-title"],
        )

        with gr.Row():
            with gr.Column(scale=3):
                tts_text = gr.Textbox(
                    label="粤语文字 Cantonese Text",
                    placeholder="请输入粤语文字，例如：今日天气好好，我哋出去行下啦。",
                    lines=5,
                    value=DEFAULT_TEXT,
                )
            with gr.Column(scale=2):
                voice_dropdown = gr.Dropdown(
                    choices=VOICE_CHOICES,
                    value=VOICE_CHOICES[0],
                    label="声线选择 Voice",
                )
                voice_desc = gr.Textbox(
                    label="声线说明",
                    value=VOICE_PRESETS[VOICE_CHOICES[0]]["description"],
                    interactive=False,
                )
                custom_prompt_wav = gr.Audio(
                    sources=["upload", "microphone"],
                    type="filepath",
                    label="自定义参考音频（仅「自定义」模式）",
                    visible=False,
                )

        with gr.Row():
            speed = gr.Slider(
                minimum=0.5,
                maximum=2.0,
                value=1.0,
                step=0.1,
                label="语速 Speed",
            )
            seed = gr.Number(value=42, label="随机种子 Seed", precision=0)
            seed_btn = gr.Button("🎲 随机种子", scale=0)

        generate_btn = gr.Button("🔊 生成语音 Generate", variant="primary", size="lg")
        audio_output = gr.Audio(label="合成结果 Output", autoplay=True)
        saved_path = gr.Textbox(
            label="保存路径 Saved WAV",
            value="",
            interactive=False,
            placeholder=f"生成后会保存到 {OUTPUT_DIR}",
        )

        example_texts = [
            ["你好，我係 CosyVoice 語音合成系統，歡迎使用粵語文字轉語音功能。"],
            ["今日天气好好，我哋出去行下啦。"],
            ["好少咯，一般系放嗰啲国庆啊，中秋嗰啲可能会咯。"],
            ["你食咗饭未啊？一齐去饮茶啦。"],
            ["呢度嘅风景真系好靓，值得嚟睇下。"],
        ]
        gr.Examples(
            examples=example_texts,
            inputs=[tts_text],
            label="示例文字 Examples",
        )

        def on_voice_change(voice_name):
            is_custom = voice_name == "自定义 Custom"
            return (
                VOICE_PRESETS[voice_name]["description"],
                gr.update(visible=is_custom),
            )

        voice_dropdown.change(
            fn=on_voice_change,
            inputs=[voice_dropdown],
            outputs=[voice_desc, custom_prompt_wav],
        )
        seed_btn.click(fn=generate_seed, inputs=[], outputs=[seed])
        generate_btn.click(
            fn=generate_cantonese_audio,
            inputs=[tts_text, voice_dropdown, custom_prompt_wav, speed, seed],
            outputs=[audio_output, saved_path],
        )

    return demo


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CosyVoice Cantonese TTS Web UI")
    parser.add_argument("--port", type=int, default=7860)
    parser.add_argument(
        "--model_dir",
        type=str,
        default="pretrained_models/Fun-CosyVoice3-0.5B",
        help="Local path or ModelScope/HuggingFace repo id",
    )
    parser.add_argument("--share", action="store_true", help="Create public Gradio link")
    args = parser.parse_args()

    print(f"Loading model from: {args.model_dir}")
    cosyvoice = AutoModel(model_dir=args.model_dir)

    if not hasattr(cosyvoice, "inference_instruct2"):
        raise RuntimeError(
            "This UI requires CosyVoice2/3. Please download Fun-CosyVoice3-0.5B:\n"
            "  python scripts/download_model.py"
        )

    default_data = np.zeros(cosyvoice.sample_rate)
    demo = build_ui()
    demo.queue(max_size=4, default_concurrency_limit=1)
    demo.launch(
        server_name="0.0.0.0",
        server_port=args.port,
        share=args.share,
    )
