# Preparando o Raspberry Pi

## 1. Dependencias
```bash
sudo apt update
sudo apt install -y python3-gpiozero python3-pip
```

## 2. SSH habilitado
```bash
sudo raspi-config   # Interface Options > SSH > Enable
```

Do computador (host), gere e copie a chave para nao precisar digitar senha:
```bash
ssh-keygen -t ed25519
ssh-copy-id pi@raspberrypi.local
ssh pi@raspberrypi.local   # confirma o host key uma vez (o deploy usa RejectPolicy)
```

## 3. Ligacao do hardware
| Componente | Pino BCM | Ligacao |
|---|---|---|
| LED (anodo) | 17 | em serie com resistor de 330 Ohm para o GND |
| Botao | 27 | outro terminal no GND (pull-up interno ativado) |

## 4. Teste manual
```bash
python3 pi/test_hardware.py
```
