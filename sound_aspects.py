from FunctionOnFiniteInterval import FunctionOnFiniteInterval as _FunctionOnFiniteInterval
from typing import Callable as _Callable

class WavingFunction:
    
    def __init__(self, function: _Callable[[float, float], float], start: float, stop: float):
        self._function = function
        self._start = start
        self._stop = stop

    def __call__(self, t: float, x: float) -> float:
        return self._function(t, x)
    
    def get_function(self) -> _Callable[[float, float], float]:
        return self._function
    
    def get_start(self) -> float:
        return self._start
    
    def get_stop(self) -> float:
        return self._stop

class FrequencyFunction(_FunctionOnFiniteInterval):
    pass

class VolumeFunction(_FunctionOnFiniteInterval):
    pass