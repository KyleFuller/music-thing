
from utils import linspace as _linspace
from audio import SAMPLE_RATE as _SAMPLE_RATE
import math as _math
from typing import Callable as _Fn

"""simple function that takes a volume function and a frequency function and
 returns the audio that results from the 2"""
def make_audio_from_shaping_frequency_volume(
      start: float, 
      stop: float, 
      get_waveform: _Fn[[float], _Fn[[float], float]], 
      get_frequency: _Fn[[float], float], 
      get_volume: _Fn[[float], float], /) -> list[float]:
    audio = [0. for _ in range(_math.ceil(_SAMPLE_RATE * (stop - start)))]
    times = _linspace(start, stop, _math.ceil(_SAMPLE_RATE * (stop - start)))

    summ = 0.
    for i, t in enumerate(times):
        summ += get_frequency(t) / _SAMPLE_RATE
        audio[i] = get_waveform(summ)(t) * get_volume(t)

    return audio