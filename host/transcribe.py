"""Audio -> texto."""
from pathlib import Path

from config import OPENAI_API_KEY, STT_MODEL, STT_PROVIDER


def transcribe(audio_path: Path) -> str:
    if STT_PROVIDER != "openai":
        raise NotImplementedError(f"STT_PROVIDER nao suportado: {STT_PROVIDER}")

    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model=STT_MODEL,
            file=f,
            language="pt",
        )
    return result.text.strip()
