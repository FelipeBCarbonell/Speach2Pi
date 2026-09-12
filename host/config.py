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

# Speech-to-text
STT_PROVIDER = os.getenv("STT_PROVIDER", "openai")
STT_MODEL = os.getenv("STT_MODEL", "whisper-1")

# Raspberry Pi
PI_HOST = os.getenv("PI_HOST", "raspberrypi.local")
PI_USER = os.getenv("PI_USER", "pi")
PI_REMOTE_DIR = os.getenv("PI_REMOTE_DIR", "/home/pi/speach2pi")

# Hardware (numeracao BCM)
LED_PIN = int(os.getenv("LED_PIN", 17))
BUTTON_PIN = int(os.getenv("BUTTON_PIN", 27))

# Audio
SAMPLE_RATE = 16_000
CHANNELS = 1
RECORDINGS_DIR = ROOT / "recordings"
PROMPTS_DIR = ROOT / "prompts"
