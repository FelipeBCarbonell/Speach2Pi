"""Teste de fumaca (MicroPython, Pololu Zumo 2040): LEDs, buzzer, display, botoes e sensores.

Nao liga os motores. Rodar do computador:
    mpremote connect <COMx> run zumo/test_hardware.py
Para testar os motores, use o motor_test.py que ja vem no robo (menu do botao C).
"""
from zumo_2040_robot import robot
import time

display = robot.Display()
buzzer = robot.Buzzer()
rgb_leds = robot.RGBLEDs()
yellow_led = robot.YellowLED()
button_a = robot.ButtonA()
button_c = robot.ButtonC()
line_sensors = robot.LineSensors()
proximity = robot.ProximitySensors()
battery = robot.Battery()

print("Bateria:", battery.get_level_millivolts(), "mV")

display.fill(0)
display.text("Speach2Pi", 28, 0)
display.text("teste de hardware", 0, 16)
display.show()

print("Buzzer: bip")
buzzer.play("l16 o5 ceg>c")

print("LEDs RGB: 0-2 traseiros, 3-5 frontais")
rgb_leds.set_brightness(4)
cores = [[255, 0, 0], [0, 255, 0], [0, 0, 255], [255, 255, 0], [0, 255, 255], [255, 0, 255]]
for i, cor in enumerate(cores):
    rgb_leds.set(i, cor)
    rgb_leds.show()
    time.sleep_ms(200)

print("LED amarelo: 3 piscadas")
for _ in range(3):
    yellow_led.on()
    time.sleep_ms(200)
    yellow_led.off()
    time.sleep_ms(200)

print("Aperte A ou C; a tela mostra os sensores. Ctrl+C para sair.")
while True:
    linha = line_sensors.read()
    proximity.read()
    frente = proximity.front_counts_with_left_leds() + proximity.front_counts_with_right_leds()

    display.fill(0)
    display.text("A:" + ("SIM" if button_a.is_pressed() else "nao"), 0, 0)
    display.text("C:" + ("SIM" if button_c.is_pressed() else "nao"), 64, 0)
    display.text("linha (0-1024):", 0, 16)
    display.text(" ".join(str(v // 10) for v in linha), 0, 26)
    display.text("frente: " + str(frente) + "/12", 0, 44)
    display.text("bat: " + str(battery.get_level_millivolts()) + " mV", 0, 56)
    display.show()
    time.sleep_ms(100)
