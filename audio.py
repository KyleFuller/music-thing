from utils import linspace as _linspace
from SoundFunction import SoundFunction as _SoundFunction

import math as _math
import simpleaudio as sa # type: ignore
import wave
import struct

SAMPLE_RATE = 44_100

def make_audio(start: float, stop: float, sampler: _SoundFunction, /):
    return ([sampler(s) for s in _linspace(start, stop, _math.ceil(SAMPLE_RATE * (stop - start)))])

def audio_to_wav_data(audio: list[float]):
    int_vals = [int(s * (2**15 - 1)) for s in audio]
    return struct.pack(f"<{len(int_vals)}h", *int_vals)

def write_audio(audio: list[float], name:str='untitled.wav', /):
    with wave.open(name, 'w') as f:
        f.setnchannels(1)
        f.setframerate(SAMPLE_RATE)
        f.setsampwidth(2)
        
        f.writeframes(audio_to_wav_data(audio))

def play_audio(audio: list[float]):
    wav_data = audio_to_wav_data(audio)
    play_obj = sa.play_buffer(wav_data, 1, 2, SAMPLE_RATE) # type: ignore
    return play_obj