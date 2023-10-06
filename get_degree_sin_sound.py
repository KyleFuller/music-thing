import math as _math
from typing import Callable as _Fn

def get_degree_sin_sound(
        degree: int, 
        key: _Fn[[int], float], 
        duration: float, 
        volume: float, 
        /
    ) -> tuple[(_Fn[[float], float]), float, float]:

    sin, pi = _math.sin, _math.pi

    nonfudged_frequency = key(degree)
    start = 0.
    stop = duration
    auditory_duration = stop - start
    fudged_frequency = round(nonfudged_frequency * auditory_duration) / auditory_duration
    return lambda t: sin(2 * pi * t * fudged_frequency) * volume, start, stop