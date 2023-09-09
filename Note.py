
import abc
import math

class Note(abc.ABC):

    @abc.abstractmethod
    def __init__(self):
        pass

    @abc.abstractmethod
    def get_duration(self):
        pass

    @abc.abstractmethod
    def get_sound(self):
        pass

class ScaleNote:

    def __init__(self, *, scale, degree, duration, volume):
        self._scale = scale
        self._degree = degree
        self._duration = duration

    def get_duration(self):
        return self._duration
    
    def get_sound(self):
        sin, pi = math.sin, math.pi

        nonfudged_frequency = self._scale(self._degree)
        frequency = 1 / round(1 / nonfudged_frequency)
        start = 0
        stop = self._duration
        volume = self._volume
        waving = lambda x, _: sin(2 * pi * x)
        








