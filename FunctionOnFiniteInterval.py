from typing import Callable as _Callable

class FunctionOnFiniteInterval:
    
    def __init__(self, function: _Callable[[float], float], start: float, stop: float):
        self._function = function
        self._start = start
        self._stop = stop

    def __call__(self, x: float) -> float:
        return self._function(x)
    
    def get_function(self) -> _Callable[[float], float]:
        return self._function
    
    def get_start(self) -> float:
        return self._start
    
    def get_stop(self) -> float:
        return self._stop