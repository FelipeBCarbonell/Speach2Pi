"""Configuracao central, lida do .env."""
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

# LLM
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "anthropic")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_BASE_URL = os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")

# Speech-to-text
STT_PROVIDER = os.getenv("STT_PROVIDER", "openai")
STT_MODEL = os.getenv("STT_MODEL", "whisper-1")
# So para STT_PROVIDER=nvidia (Riva no build.nvidia.com)
# function-id = qual modelo chamar; o padrao e o openai/whisper-large-v3
STT_FUNCTION_ID = os.getenv("STT_FUNCTION_ID", "b702f636-f60c-4a3d-a6f4-f3568c13bd7d")
STT_LANGUAGE = os.getenv("STT_LANGUAGE", "pt")
NVIDIA_RIVA_SERVER = os.getenv("NVIDIA_RIVA_SERVER", "grpc.nvcf.nvidia.com:443")

# Pololu Zumo 2040 (porta serial do MicroPython; "auto" detecta pela USB)
ROBOT_PORT = os.getenv("ROBOT_PORT", "auto")

# Audio
SAMPLE_RATE = 16_000
CHANNELS = 1
RECORDINGS_DIR = ROOT / "recordings"
PROMPTS_DIR = ROOT / "prompts"
