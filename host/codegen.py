"""Texto (instrucao em linguagem natural) -> codigo Python para o Raspberry Pi."""
import re

from config import (
    ANTHROPIC_API_KEY,
    BUTTON_PIN,
    LED_PIN,
    LLM_MODEL,
    LLM_PROVIDER,
    OPENAI_API_KEY,
    PROMPTS_DIR,
)


def _system_prompt() -> str:
    template = (PROMPTS_DIR / "system_prompt.md").read_text(encoding="utf-8")
    return template.format(led_pin=LED_PIN, button_pin=BUTTON_PIN)


def _strip_fences(text: str) -> str:
    """Remove ```python ... ``` se o modelo devolver em bloco de codigo."""
    match = re.search(r"```(?:python)?\s*\n(.*?)```", text, re.DOTALL)
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

    elif LLM_PROVIDER == "openai":
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        resp = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": _system_prompt()},
                {"role": "user", "content": instruction},
            ],
        )
        raw = resp.choices[0].message.content

    else:
        raise ValueError(f"LLM_PROVIDER invalido: {LLM_PROVIDER}")

    return _strip_fences(raw)


# Guarda-corpo simples: o codigo gerado roda no Pi, entao bloqueamos o obvio.
BLOCKLIST = ("import os", "import subprocess", "import shutil", "__import__", "eval(", "exec(", "rm -rf")


def is_safe(code: str) -> tuple[bool, str]:
    for pattern in BLOCKLIST:
        if pattern in code:
            return False, f"codigo contem padrao bloqueado: {pattern!r}"
    return True, ""
