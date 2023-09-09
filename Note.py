from sound_aspects_to_sound import make_sound as _make_sound
from sound_aspects import (
    WavingFunction as _WavingFunction,
    VolumeFunction as _VolumeFunction,
    FrequencyFunction as _FrequencyFunction)

import abc as _abc
import math as _math
from typing import Callable as _Callable

class Note(_abc.ABC):

    @_abc.abstractmethod
    def __init__(self):
        pass

    @_abc.abstractmethod
    def get_duration(self):
        pass

    @_abc.abstractmethod
    def get_sound(self):
        pass

class ScaleNote:

    def __init__(self, *, scale: _Callable[[int], float], degree: int, duration: float, volume: float):
        self._scale = scale
        self._degree = degree
        self._duration = duration
        self._volume = volume

    def get_duration(self):
        return self._duration
    
    def get_sound(self):
        sin, pi = _math.sin, _math.pi

        nonfudged_frequency = self._scale(self._degree)
        start = 0.
        stop = self._duration
        frequency = _FrequencyFunction(lambda _: 1 / round(1 / nonfudged_frequency), start, stop)
        volume = _VolumeFunction(lambda _: self._volume, start, stop)
        waving = _WavingFunction(lambda _, x: sin(2 * pi * x), start, stop)
        return _make_sound(
            waving, 
            frequency, 
            volume)
        
def main():
    ...

if __name__ == '__main__':
    main()







