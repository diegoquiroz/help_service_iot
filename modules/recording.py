import sounddevice


class Recording():
    """Audio recording module"""

    def __init__(self, duration=5):
        self._duration = duration
        self.__SAMPLING_FRECUENCY = 16000

    def record_audio(self):
        sounddevice.rec((self._duration * self.__SAMPLING_FRECUENCY),
                        samplerate=self.__SAMPLING_FRECUENCY, channels=2)

    def get_duration(self) -> int:
        return self.duration
