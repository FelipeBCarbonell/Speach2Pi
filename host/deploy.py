"""Envia o codigo gerado para o Pololu Zumo 2040 (MicroPython) via USB.

O codigo roda direto na memoria do robo (mpremote run --no-follow): nenhum
arquivo do robo e alterado, entao o menu da Pololu (main.py) continua intacto.
Apertar o botao de reset do robo volta para esse menu.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from serial.tools import list_ports

from config import ROBOT_PORT

# VID/PID da porta serial do MicroPython da Pololu no Zumo 2040
POLOLU_VID = 0x1FFB
ZUMO_2040_PID = 0x2044

# Antes de cada programa novo (e ao sair): motores, buzzer e LEDs desligados
STOP_SNIPPET = """\
from zumo_2040_robot import robot
robot.Motors().off()
robot.Buzzer().off()
robot.RGBLEDs().off()
robot.YellowLED().off()
d = robot.Display()
d.fill(0)
d.show()
"""


def find_port() -> str:
    if ROBOT_PORT != "auto":
        return ROBOT_PORT
    for port in list_ports.comports():
        if port.vid == POLOLU_VID and port.pid == ZUMO_2040_PID:
            return port.device
    raise RuntimeError("Zumo 2040 nao encontrado. Ele esta ligado e conectado pela USB?")


def _mpremote(port: str, *args: str) -> None:
    subprocess.run(
        [sys.executable, "-m", "mpremote", "connect", port, *args],
        check=True,
    )


def deploy_and_run(code: str) -> None:
    """Interrompe o programa atual, desliga motores/LEDs/buzzer e roda o novo."""
    port = find_port()
    with tempfile.TemporaryDirectory() as tmp:
        local_path = Path(tmp) / "speach2pi.py"
        local_path.write_text(code, encoding="utf-8")
        _mpremote(port, "exec", STOP_SNIPPET, "+", "run", "--no-follow", str(local_path))
    print(f"[deploy] rodando no Zumo ({port})")


def stop() -> None:
    """Interrompe o programa atual e deixa o robo parado."""
    _mpremote(find_port(), "exec", STOP_SNIPPET)
