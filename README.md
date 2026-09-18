# Speach2Pi

Controle um robô Pololu Zumo 2040 falando. Você segura a barra de espaço, diz o que
quer — *"anda para frente por dois segundos e depois gira para a direita"* — solta a
tecla, e pouco depois o robô já está se comportando assim.

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
│                       LLM (Claude / GPT) ──▶ código MicroPython   │
│                                        │                          │
└────────────────────────────────────────┼──────────────────────────┘
                                         │ USB (mpremote)
                                         ▼
          ┌──────────── Pololu Zumo 2040 (RP2040) ────────────┐
          │  executa o código ──▶ motores, LEDs, buzzer,       │
          │                       display, botões e sensores   │
          └────────────────────────────────────────────────────┘
```

| Etapa | Arquivo |
|---|---|
| Captura de áudio pela barra de espaço | [host/recorder.py](host/recorder.py), [host/main.py](host/main.py) |
| Áudio → texto | [host/transcribe.py](host/transcribe.py) |
| Texto → código MicroPython | [host/codegen.py](host/codegen.py), [prompts/system_prompt.md](prompts/system_prompt.md) |
| Envio e execução no Zumo | [host/deploy.py](host/deploy.py) |

O código roda direto na memória do robô, sem alterar os arquivos dele: o botão de
reset volta para o menu original da Pololu.

## Instalação (no computador)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows;  no Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env        # depois preencha as chaves de API
```

## Robô Pololu Zumo 2040

Ver [zumo/setup_zumo.md](zumo/setup_zumo.md) — conexão, energia, hardware disponível
e teste do hardware.

## Uso

```bash
python host/main.py
```

1. Segure **ESPAÇO** e fale a instrução
2. Solte a tecla
3. O código gerado aparece no terminal e já começa a rodar no Zumo
4. Se o programa usa os motores, aperte o botão **A** do robô para ele começar a andar
5. **ESC** para o robô e encerra

## Hardware

Tudo já vem no chassi do Zumo 2040: 2 motores com encoders, display OLED, 6 LEDs
RGB, LED amarelo, buzzer, 3 botões, 5 sensores de linha, sensores de proximidade e
IMU. Detalhes em [zumo/setup_zumo.md](zumo/setup_zumo.md).

## Segurança

O código gerado por um LLM é executado no robô, então há três barreiras: o
*system prompt* restringe o que pode ser gerado (e exige apertar o botão A antes de
mover os motores), `codegen.is_safe()` bloqueia padrões perigosos (`os`, `open`,
`eval`, `exec`, `_thread`, `machine.reset`, `bootloader`…) antes do envio, e cada
envio (e o ESC) desliga motores, LEDs e buzzer antes de qualquer outra coisa. O
código é sempre impresso no terminal antes de rodar.

## Status

Em desenvolvimento. Ver [docs/roadmap.md](docs/roadmap.md).
