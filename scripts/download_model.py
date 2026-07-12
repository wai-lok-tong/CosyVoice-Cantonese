"""Download Fun-CosyVoice3 model for Cantonese TTS."""

import argparse
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MODEL_DIR = os.path.join(ROOT_DIR, "pretrained_models/Fun-CosyVoice3-0.5B")


def download_from_modelscope(local_dir: str):
    from modelscope import snapshot_download

    print("Downloading from ModelScope (recommended for China)...")
    snapshot_download("FunAudioLLM/Fun-CosyVoice3-0.5B-2512", local_dir=local_dir)
    print(f"Model saved to: {local_dir}")


def download_from_huggingface(local_dir: str):
    from huggingface_hub import snapshot_download

    print("Downloading from HuggingFace...")
    snapshot_download("FunAudioLLM/Fun-CosyVoice3-0.5B-2512", local_dir=local_dir)
    print(f"Model saved to: {local_dir}")


def main():
    parser = argparse.ArgumentParser(description="Download Fun-CosyVoice3 model")
    parser.add_argument(
        "--output",
        default=DEFAULT_MODEL_DIR,
        help="Local directory to save the model",
    )
    parser.add_argument(
        "--source",
        choices=["modelscope", "huggingface", "auto"],
        default="auto",
        help="Download source (auto tries ModelScope first)",
    )
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    if args.source == "modelscope":
        download_from_modelscope(args.output)
    elif args.source == "huggingface":
        download_from_huggingface(args.output)
    else:
        try:
            download_from_modelscope(args.output)
        except Exception as exc:
            print(f"ModelScope failed ({exc}), trying HuggingFace...")
            download_from_huggingface(args.output)


if __name__ == "__main__":
    main()
