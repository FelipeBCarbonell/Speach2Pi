# Preparando o Pololu Zumo 2040

O Zumo 2040 ja vem com o MicroPython da Pololu e a biblioteca `zumo_2040_robot`
instalados. Nao e preciso gravar firmware.

## 1. Conectar
Ligue o robo no computador pela USB. Ele aparece de dois jeitos:
- uma porta serial (no Windows, `COMx`; VID `1FFB`, PID `2044`), que o Speach2Pi
  encontra sozinho (`ROBOT_PORT=auto` no `.env`);
- um drive chamado **MicroPython**, com a biblioteca e os exemplos da Pololu.

O Speach2Pi **nao grava nada** no drive: o codigo gerado roda direto na memoria do
robo. Apertar o botao de **reset** volta para o menu da Pololu (`main.py`).

## 2. Energia
A USB alimenta so a parte logica. **Os motores precisam das 4 pilhas AA e do
botao de energia ligado.** Sem isso, LEDs, display e sensores funcionam, mas o robo
nao anda.

## 3. Hardware disponivel
| Componente | Acesso na biblioteca |
|---|---|
| 2 motores de esteira (-6000 a 6000) | `robot.Motors()` |
| Encoders dos motores | `robot.Encoders()` |
| Display OLED 128x64 | `robot.Display()` |
| 6 LEDs RGB (0-2 traseiros, 3-5 frontais) | `robot.RGBLEDs()` |
| LED amarelo | `robot.YellowLED()` |
| Buzzer | `robot.Buzzer()` |
| Botoes A, B e C | `robot.ButtonA()`, `ButtonB()`, `ButtonC()` |
| 5 sensores de linha (embaixo) | `robot.LineSensors()` |
| Sensores de proximidade (esquerda, frente, direita) | `robot.ProximitySensors()` |
| IMU (giroscopio, acelerometro, magnetometro) | `robot.IMU()` |
| Bateria | `robot.Battery()` |

## 4. Teste manual
Com o ambiente virtual ativado (troque `COM9` pela porta do robo):
```bash
mpremote connect COM9 run zumo/test_hardware.py
```
Toca um bip, acende os LEDs RGB um a um, pisca o LED amarelo e depois mostra no
display os botoes A/C, os sensores de linha, o sensor de proximidade frontal e a
bateria. Nao liga os motores; para eles, use o `motor_test.py` que ja vem no robo
(menu do botao C). Ctrl+C para sair.

## Seguranca
O *system prompt* exige que programas que usam os motores esperem um aperto do
botao **A** antes de se mover. Ao sair do Speach2Pi (ESC), os motores, LEDs e o
buzzer sao desligados.
