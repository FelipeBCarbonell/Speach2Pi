"""Teste de fumaca: roda no proprio Raspberry Pi para validar LED e botao."""
from gpiozero import LED, Button
from signal import pause

LED_PIN = 17
BUTTON_PIN = 27

led = LED(LED_PIN)
button = Button(BUTTON_PIN)

button.when_pressed = led.on
button.when_released = led.off

print(f"LED no BCM {LED_PIN}, botao no BCM {BUTTON_PIN}.")
print("Segure o botao: o LED deve acender. Ctrl+C para sair.")
pause()
