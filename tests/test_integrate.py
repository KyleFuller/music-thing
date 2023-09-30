# type: ignore
from math import sin as _sin, cos as _cos, exp as _exp, erf as _erf, sqrt as _sqrt, pi as _pi
from typing import Callable as _Fn
import sys as _sys
_sys.path.append('.')

from integrate import integrate_on_unknown_interval as _on_unknown
from utils import linspace as _linspace
from audio import SAMPLE_RATE as _SAMPLE_RATE

def _is_approx(x, y):
    if x == 0 and y == 0:
        return True
    elif x <= 0 and y >= 0 or x >= 0 and y <= 0:
        return False
    else:
        return abs((y - x) / x) <= 2 ** -15

def test():

    f: _Fn[[float], float] = lambda t: _exp(- (10 * t)**2)
    integral = _on_unknown(f)
    
    ts = _linspace(-0.5, 0.5, 10 * 44100)
    computed_vals = [integral(t) for t in ts]
    target_vals =  [_sqrt(_pi) / 2 * _erf(10 * t) / 10 for t in ts]

    for i, _ in enumerate(ts):
        assert _is_approx(computed_vals[i], target_vals[i])
    
    from matplotlib import pyplot as plt
    plt.plot([computed_vals[i] - target_vals[i] for i in range(len(ts))])
    plt.show()


if __name__ == '__main__':
    test()