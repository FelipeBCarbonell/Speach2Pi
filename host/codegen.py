"""Texto (instrucao em linguagem natural) -> codigo MicroPython para o Pololu Zumo 2040."""
import re

from config import (
    ANTHROPIC_API_KEY,
    LLM_MODEL,
    LLM_PROVIDER,
    NVIDIA_API_KEY,
    NVIDIA_BASE_URL,
    OPENAI_API_KEY,
    PROMPTS_DIR,
)


def _system_prompt() -> str:
    return (PROMPTS_DIR / "system_prompt.md").read_text(encoding="utf-8")


def _strip_fences(text: str) -> str:
    """Remove ```python ... ``` se o modelo devolver em bloco de codigo."""
    match = re.search(r"```(?:python|micropython)?\s*\n(.*?)```", text, re.DOTALL)
    return (match.group(1) if match else text).strip()


def generate_code(instruction: str) -> str:
    if LLM_PROVIDER == "anthropic":
        from anthropic import Anthropic

        client = Anthropic(api_key=ANTHROPIC_API_KEY)
        msg = client.messages.create(
            model=LLM_MODEL,
            max_tokens=2000,
            system=_system_prompt(),
            messages=[{"role": "user", "content": instruction}],
        )
        raw = msg.content[0].text

    elif LLM_PROVIDER in ("openai", "nvidia"):
        from openai import OpenAI

        if LLM_PROVIDER == "nvidia":
            # API da NVIDIA (build.nvidia.com) e compativel com a da OpenAI.
            # Modelos que raciocinam gastam tokens antes da resposta: folga no limite.
            client = OpenAI(api_key=NVIDIA_API_KEY, base_url=NVIDIA_BASE_URL)
            extra = {"max_tokens": 16384}
        else:
            client = OpenAI(api_key=OPENAI_API_KEY)
            extra = {}
        resp = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": _system_prompt()},
                {"role": "user", "content": instruction},
            ],
            **extra,
        )
        raw = resp.choices[0].message.content
        if not raw:
            raise RuntimeError("o modelo nao devolveu codigo (resposta vazia)")

    else:
        raise ValueError(f"LLM_PROVIDER invalido: {LLM_PROVIDER}")

    return _strip_fences(raw)


# Guarda-corpo simples: o codigo gerado roda no robo, entao bloqueamos o obvio
# (mexer no sistema de arquivos, reiniciar, entrar no modo BOOTSEL ou abrir uma
# thread no segundo nucleo, que continuaria rodando mesmo apos interromper o programa).
BLOCKLIST = (
    "import os",
    "from os",
    "__import__",
    "eval(",
    "exec(",
    "open(",
    "machine.reset(",
    "bootloader(",
    "_thread",
)


def is_safe(code: str) -> tuple[bool, str]:
    for pattern in BLOCKLIST:
        if pattern in code:
            return False, f"codigo contem padrao bloqueado: {pattern!r}"
    return True, ""
