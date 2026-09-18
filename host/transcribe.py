"""Audio -> texto."""
from pathlib import Path

from config import (
    NVIDIA_API_KEY,
    NVIDIA_RIVA_SERVER,
    OPENAI_API_KEY,
    STT_FUNCTION_ID,
    STT_LANGUAGE,
    STT_MODEL,
    STT_PROVIDER,
)


def _transcribe_openai(audio_path: Path) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=OPENAI_API_KEY)
    with open(audio_path, "rb") as f:
        result = client.audio.transcriptions.create(
            model=STT_MODEL,
            file=f,
            language="pt",
        )
    return result.text.strip()


def _transcribe_nvidia(audio_path: Path) -> str:
    """Modelos de fala do build.nvidia.com (ex.: whisper-large-v3) via Riva/gRPC."""
    import riva.client

    auth = riva.client.Auth(
        uri=NVIDIA_RIVA_SERVER,
        use_ssl=True,
        metadata_args=[
            ["function-id", STT_FUNCTION_ID],
            ["authorization", f"Bearer {NVIDIA_API_KEY}"],
        ],
    )
    config = riva.client.RecognitionConfig(
        language_code=STT_LANGUAGE,
        max_alternatives=1,
        enable_automatic_punctuation=True,
    )
    riva.client.add_audio_file_specs_to_config(config, audio_path)

    response = riva.client.ASRService(auth).offline_recognize(audio_path.read_bytes(), config)
    return " ".join(
        r.alternatives[0].transcript.strip() for r in response.results if r.alternatives
    ).strip()


def transcribe(audio_path: Path) -> str:
    if STT_PROVIDER == "openai":
        return _transcribe_openai(audio_path)
    if STT_PROVIDER == "nvidia":
        return _transcribe_nvidia(audio_path)
    raise NotImplementedError(f"STT_PROVIDER nao suportado: {STT_PROVIDER}")
