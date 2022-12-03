import pyaudio
import wave
import sys
import numpy as np

from mouthServo import MouthServo

def dbToServo(db):
    position = 5.0
    dbclamp = max([min(40,db),20])
    dbclamp = dbclamp - 20
    movement = dbclamp / 4.0

    return min(max(5.0, position+movement),10.0)


class MagicMouth:

    CHUNK = 1024

    def speak(self, filepath):
        waveFile = wave.open(filepath)
        outputStream = self.pyAudio.open(
            format=self.pyAudio.get_format_from_width(waveFile.getsampwidth()),
            channels=waveFile.getnchannels(),
            rate=waveFile.getframerate(),
            output=True
        )

        data = waveFile.readframes(self.CHUNK)

        while len(data):
            audio_as_np_int16 = np.frombuffer(data, dtype=np.int16)
            currentDecibel = 20 * np.log10( np.sqrt( np.mean(audio_as_np_int16**2)))
            print(currentDecibel)
            self.mouthServo1.moveTo(dbToServo(currentDecibel))
            outputStream.write(data)
            data = waveFile.readframes(self.CHUNK)

        outputStream.stop_stream()
        outputStream.close()
        

    def __init__(self):
        self.pyAudio = pyaudio.PyAudio()
        self.mouthServo1 = MouthServo(17)
        self.mouthServo1.start()

    def __del__(self):
        self.pyAudio.terminate()