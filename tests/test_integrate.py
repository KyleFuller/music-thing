from math import sin as _sin, cos as _cos, exp as _exp, erf as _erf, sqrt as _sqrt, pi as _pi
import sys as _sys
_sys.path.append('.')

from audio import SAMPLE_RATE as _SAMPLE_RATE
from integrate import integrate as _integrate, integrate_with_step_rate as _integrate_with_step_rate
from typing import Callable as _Fn
from utils import linspace as _linspace

_RVFn = _Fn[[float], float] # type alias for real-valued function

def _is_approx(x: float, y: float, tol: float):
    return abs(y - x) <= tol

def _integral_value_test(
        f: _RVFn, 
        integrate: _Fn[[_RVFn], _RVFn],
        ts: list[float], 
        true_integral: _RVFn, 
        tol: float):
    
    integral = integrate(f)

    computed_vals = [integral(t) for t in ts]
    target_vals =  [true_integral(t) for t in ts]

    for i, _ in enumerate(ts):
        assert _is_approx(computed_vals[i], target_vals[i], tol)

def test():
    ts = _linspace(-0.5, 0.5, 10 * _SAMPLE_RATE)

    integrate: _Fn[[_RVFn], _RVFn] = lambda f: _integrate(f)

    f: _RVFn = lambda t: 10 * t
    integral: _RVFn = lambda t: 5 * t ** 2
    _integral_value_test(f, integrate, ts, integral, tol=1e-12)

    f: _RVFn = lambda t: _exp(- (10 * t)**2)
    integral: _RVFn = lambda t: _sqrt(_pi) / 2 * _erf(10 * t) / 10
    _integral_value_test(f, integrate, ts, integral, tol=1e-12)

    f: _RVFn = lambda t: _exp(5 * t)
    integral: _RVFn = lambda t: (_exp(5 * t) - 1) / 5
    _integral_value_test(f, integrate, ts, integral, tol=1e-12)

    f: _RVFn = lambda t: _sin(5 * t)
    integral: _RVFn = lambda t: (1 -_cos(5 * t)) / 5
    _integral_value_test(f, integrate, ts, integral, tol=1e-12)

    f: _RVFn = lambda t: t ** (1/3) if t >= 0 else -(-t)**(1/3)
    integral: _RVFn = lambda t: 3 / 4 * t * f(t)
    _integral_value_test(f, lambda f: _integrate_with_step_rate(f, _SAMPLE_RATE), ts, integral, tol=1e-7)

def benchmark(nsec: int, step_rate:float, /):
    ts = _linspace(-nsec/2, nsec/2, nsec * _SAMPLE_RATE)
    integral = _integrate_with_step_rate(lambda x: _sin(x), step_rate)
    [integral(t) for t in ts]

if __name__ == '__main__':
    test()