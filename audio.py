from utils import linspace as _linspace

import math as _math
import simpleaudio as _sa # type: ignore
import wave as _wave
import struct as _struct
from typing import Callable as _Fn
from functools import cache as _cache

SAMPLE_RATE = 44_100

@_cache
def make_audio(sound: _Fn[[float], float], start: float, stop: float, /):
    return ([sound(s) for s in _linspace(start, stop, _math.ceil(SAMPLE_RATE * (stop - start)))])

def audio_to_wav_data(audio: list[float]):
    int_vals = [int(s * (2**15 - 1)) for s in audio]
    return _struct.pack(f"<{len(int_vals)}h", *int_vals)

def write_audio(audio: list[float], name:str='untitled.wav', /):
    with _wave.open(name, 'w') as f:
        f.setnchannels(1)
        f.setframerate(SAMPLE_RATE)
        f.setsampwidth(2)
        
        f.writeframes(audio_to_wav_data(audio))

def play_audio(audio: list[float]):
    wav_data = audio_to_wav_data(audio)
    play_obj = _sa.play_buffer(wav_data, 1, 2, SAMPLE_RATE) # type: ignore
    return play_obj