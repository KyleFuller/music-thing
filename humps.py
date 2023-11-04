from waves import cos_wave as _cos_wave
from math import exp as _exp

def cos_hump(x: float) -> float:
    return ((1 + _cos_wave(x)) / 2) * (-0.5 <= x < 0.5)

def exp_fade_hump(x: float) -> float:
    return (x >= 0) * _exp(-x)