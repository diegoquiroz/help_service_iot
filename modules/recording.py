import sounddevice
import random
from scipy.io.wavfile import write


class Recording:
    """Audio recording module"""

    def __init__(self, duration=5):
        self._duration = duration
        self.__SAMPLING_FRECUENCY = 16000

    def record_audio(self):
        recording = sounddevice.rec(
            (self._duration * self.__SAMPLING_FRECUENCY),
            samplerate=self.__SAMPLING_FRECUENCY,
            channels=1,
        )
        sounddevice.wait()
        return self._save_file(recording)

    def _save_file(self, audio) -> str:
        file_name = str(random.randint(1000, 9999))
        write(file_name, self.__SAMPLING_FRECUENCY, audio)
        return file_name

    def get_duration(self) -> int:
        return self.duration
