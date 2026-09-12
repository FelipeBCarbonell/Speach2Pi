"""Speach2Pi — segure ESPACO, fale a instrucao, solte. O Pi passa a obedecer.

Uso:  python host/main.py     (ESC para sair)
"""
import sys

from pynput import keyboard

import codegen
import deploy
from recorder import Recorder

recorder = Recorder()
recording = False


def handle_release() -> None:
    audio_path = recorder.stop()
    if audio_path is None:
        print("[aviso] nenhum audio capturado.")
        return

    print("[2/4] transcrevendo...")
    from transcribe import transcribe

    instruction = transcribe(audio_path)
    print(f'      voce disse: "{instruction}"')

    print("[3/4] gerando codigo...")
    code = codegen.generate_code(instruction)
    ok, reason = codegen.is_safe(code)
    if not ok:
        print(f"[bloqueado] {reason}")
        return
    print("-" * 60)
    print(code)
    print("-" * 60)

    print("[4/4] enviando para o Raspberry Pi...")
    deploy.deploy_and_run(code)
    print("pronto. segure ESPACO para uma nova instrucao.\n")


def on_press(key):
    global recording
    if key == keyboard.Key.space and not recording:
        recording = True
        print("\n[1/4] gravando... (solte o ESPACO para parar)")
        recorder.start()


def on_release(key):
    global recording
    if key == keyboard.Key.esc:
        print("saindo.")
        return False
    if key == keyboard.Key.space and recording:
        recording = False
        try:
            handle_release()
        except Exception as exc:  # noqa: BLE001
            print(f"[erro] {exc}")


def main() -> int:
    print("Speach2Pi pronto. Segure ESPACO e fale a instrucao. ESC para sair.")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
    return 0


if __name__ == "__main__":
    sys.exit(main())
