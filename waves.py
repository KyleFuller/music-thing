
from math import sin as _sin, cos as _cos, pi as _pi

def sin_wave(x: float) -> float:
    return _sin(2 * _pi * x)

def cos_wave(x: float) -> float:
    return _cos(2 * _pi * x)