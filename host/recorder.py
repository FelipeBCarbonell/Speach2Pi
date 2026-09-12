"""Gravacao do microfone enquanto a barra de espaco esta pressionada."""
import queue
import time
from pathlib import Path

import numpy as np
import sounddevice as sd
import soundfile as sf

from config import CHANNELS, RECORDINGS_DIR, SAMPLE_RATE


class Recorder:
    """Grava em streaming; start() abre o stream, stop() salva o .wav."""

    def __init__(self, sample_rate: int = SAMPLE_RATE, channels: int = CHANNELS):
        self.sample_rate = sample_rate
        self.channels = channels
        self._frames: queue.Queue = queue.Queue()
        self._stream: sd.InputStream | None = None

    def _callback(self, indata, frames, time_info, status):  # noqa: ARG002
        if status:
            print(f"[audio] {status}")
        self._frames.put(indata.copy())

    def start(self) -> None:
        if self._stream is not None:
            return
        self._frames = queue.Queue()
        self._stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> Path | None:
        """Fecha o stream e grava o arquivo. Retorna None se nao houve audio."""
        if self._stream is None:
            return None
        self._stream.stop()
        self._stream.close()
        self._stream = None

        chunks = []
        while not self._frames.empty():
            chunks.append(self._frames.get())
        if not chunks:
            return None

        audio = np.concatenate(chunks, axis=0)
        RECORDINGS_DIR.mkdir(exist_ok=True)
        path = RECORDINGS_DIR / f"{int(time.time())}.wav"
        sf.write(path, audio, self.sample_rate)
        return path
