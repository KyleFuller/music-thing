# type: ignore
from math import sin as _sin, cos as _cos, exp as _exp, erf as _erf, sqrt as _sqrt, pi as _pi, log as _log
from typing import Callable as _Fn
import sys as _sys
_sys.path.append('.')

from integrate import integrate_on_unknown_interval as _on_unknown
from utils import linspace as _linspace
from audio import SAMPLE_RATE as _SAMPLE_RATE

def _is_approx(x, y, tol):
    return abs(y - x) <= tol

def integral_value_test(f, ts, true_integral, tol):
    integral = _on_unknown(f)
    
    computed_vals = [integral(t) for t in ts]
    target_vals =  [true_integral(t) for t in ts]

    for i, _ in enumerate(ts):
        assert _is_approx(computed_vals[i], target_vals[i], tol)

    return computed_vals, target_vals

def test():
    ts = _linspace(-0.5, 0.5, 10 * 44100)

    f_gauss = lambda t: _exp(- (10 * t)**2)
    gauss_integral = lambda t: _sqrt(_pi) / 2 * _erf(10 * t) / 10
    integral_value_test(f_gauss, ts, gauss_integral, tol=1e-15)

    f_exp = lambda t: _exp(5 * t)
    exp_integral = lambda t: (_exp(5 * t) - 1) / 5
    integral_value_test(f_exp, ts, exp_integral, tol=1e-14)

    f_sin = lambda t: _sin(5 * t)
    sin_integral = lambda t: (1 -_cos(5 * t)) / 5
    integral_value_test(f_sin, ts, sin_integral, tol=1e-14)

    f_cbrt = lambda t: t ** (1/3) if t >= 0 else -(-t)**(1/3)
    cbrt_integral = lambda t: 3 / 4 * t * f_cbrt(t)
    computed_vals, target_vals = integral_value_test(f_cbrt, ts, cbrt_integral, tol=1e-7)

    # from matplotlib import pyplot as plt
    # plt.plot([computed_vals[i] - target_vals[i] for i in range(len(ts))])
    # plt.show()

if __name__ == '__main__':
    test()