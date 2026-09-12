# Speach2Pi

Controle um Raspberry Pi falando. Você segura a barra de espaço, diz o que quer
— *"quando eu apertar o botão, o LED pisca 3 vezes a 3 Hz"* — solta a tecla, e
alguns segundos depois o Pi já está se comportando assim.

Projeto de horas complementares (Insper).

## Como funciona

```
┌──────────────────────── computador (host) ────────────────────────┐
│                                                                   │
│  [ESPAÇO] ──▶ grava microfone ──▶ API speech-to-text ──▶ texto    │
│                                                          │        │
│                              prompt + instrução ─────────┘        │
│                                        │                          │
│                                        ▼                          │
│                            LLM (Claude / GPT) ──▶ código Python   │
│                                        │                          │
└────────────────────────────────────────┼──────────────────────────┘
                                         │ SSH / SFTP
                                         ▼
                      ┌────────── Raspberry Pi ──────────┐
                      │  executa o script  ──▶ LED + botão │
                      └────────────────────────────────────┘
```

| Etapa | Arquivo |
|---|---|
| Captura de áudio pela barra de espaço | [host/recorder.py](host/recorder.py), [host/main.py](host/main.py) |
| Áudio → texto | [host/transcribe.py](host/transcribe.py) |
| Texto → código Python | [host/codegen.py](host/codegen.py), [prompts/system_prompt.md](prompts/system_prompt.md) |
| Envio e execução no Pi | [host/deploy.py](host/deploy.py) |

## Instalação (no computador)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows;  no Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env        # depois preencha as chaves de API
```

## Raspberry Pi

Ver [pi/setup_pi.md](pi/setup_pi.md) — instalação do `gpiozero`, SSH por chave e
esquema de ligação do LED e do botão.

## Uso

```bash
python host/main.py
```

1. Segure **ESPAÇO** e fale a instrução
2. Solte a tecla
3. O código gerado aparece no terminal e já começa a rodar no Pi
4. **ESC** encerra

## Hardware

| Componente | Pino (BCM) |
|---|---|
| LED (com resistor de 330 Ω) | 17 |
| Botão (pull-up interno) | 27 |

Configurável pelo `.env`.

## Segurança

O código gerado por um LLM é executado no Raspberry Pi, então há duas barreiras:
o *system prompt* restringe o que pode ser gerado, e `codegen.is_safe()` bloqueia
padrões perigosos (`os`, `subprocess`, `eval`, `exec`…) antes do envio. O código é
sempre impresso no terminal antes de rodar.

## Status

Em desenvolvimento. Ver [docs/roadmap.md](docs/roadmap.md).
