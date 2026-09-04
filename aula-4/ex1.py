import numpy as np
import wave
import winsound


duration = 0.5  # em segundos
frequency1 = 440
frequency2 = 2 * frequency1
amplitude = 0.2
sample_rate = 44100

time = np.arange(0, duration, 1 / sample_rate)
sinewave1 = amplitude * np.sin(2 * np.pi * frequency1 * time)
sinewave2 = amplitude * np.sin(2 * np.pi * frequency2 * time)
audio = (sinewave1 + sinewave2) * np.hanning(len(time))

max_amplitude = np.max(np.abs(audio))
if max_amplitude == 0:
    max_amplitude = 1

audio = audio / max_amplitude
wave_data = np.int16(audio * 32767)

file_name = "ondas_duas.wav"
with wave.open(file_name, "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(wave_data.tobytes())

winsound.PlaySound(file_name, winsound.SND_FILENAME)
print("Som com as duas ondas tocando...")