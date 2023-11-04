import math as _math
import wave as _wave
import struct as _struct
from typing import Callable as _Fn, Iterable as _Iterable
import sounddevice as _sd # type: ignore

from utils import linspace as _linspace

SAMPLE_RATE = 44_100

def make_audio(sound: _Fn[[float], float], interval: tuple[float, float], /) -> _Iterable[float]:
    start, stop = interval
    """ returns an iterable of audio samples from evaluating the sound function
    across the given interval, which has format (<start>, <stop>). """
    return (sound(s) for s in _linspace(start, stop, _math.ceil(SAMPLE_RATE * (stop - start))))

def audio_to_bytes(audio: _Iterable[float], /) -> bytes:
    """ converts an iterable of audio samples to a bytes object of a format that
    can be used in audio output. """
    int_vals = [int(s * (2**15 - 1)) for s in audio]
    return _struct.pack(f"<{len(int_vals)}h", *int_vals)

def write_audio(audio: _Iterable[float], name:str, /):
    """ writes the given iterable of audio samples to a single-channel wav file 
    of the given name and in the appropriate format, replacing the original file
    if already present. """
    with _wave.open(name, 'w') as f:
        f.setnchannels(1)
        f.setframerate(SAMPLE_RATE)
        f.setsampwidth(2)
        
        f.writeframes(audio_to_bytes(audio))

def play_audio(audio: _Iterable[float], /):
    """ plays a given iterable of single-channel audio samples in a more-or-less
    demand-driven fashion. thus, very long or infinitely long audio iterables are 
    supported."""
    stream = _sd.RawOutputStream(SAMPLE_RATE, channels=1, dtype='int16')
    stream.start()
    for s in audio:
        the_bytes = audio_to_bytes([s])
        stream.write(the_bytes) # type: ignore
    stream.stop()