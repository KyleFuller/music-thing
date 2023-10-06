# type: ignore
from math import sin as _sin, cos as _cos, exp as _exp, erf as _erf, sqrt as _sqrt, pi as _pi, log as _log
import sys as _sys
_sys.path.append('.')

from integrate import integrate as _integrate
from utils import linspace as _linspace

def _is_approx(x, y, tol):
    return abs(y - x) <= tol

def _integral_value_test(f, integrate, ts, true_integral, tol):
    
    integral = integrate(f)

    computed_vals = [integral(t) for t in ts]
    target_vals =  [true_integral(t) for t in ts]

    for i, _ in enumerate(ts):
        assert _is_approx(computed_vals[i], target_vals[i], tol)

def test():

    
    ts = _linspace(-0.5 + 0.001, 0.5 - 0.001, 10 * 44100)

    def adjust_constant(integral_from_zero):
        return lambda t: integral_from_zero(t) - integral_from_zero(-0.5)

    f = lambda t: 10 * t
    integral = lambda t: 5 * t ** 2
    _integral_value_test(f, _integrate, ts, integral, tol=1e-14)

    f = lambda t: _exp(- (10 * t)**2)
    integral = lambda t: _sqrt(_pi) / 2 * _erf(10 * t) / 10
    _integral_value_test(f, _integrate, ts, integral, tol=1e-15)

    f = lambda t: _exp(5 * t)
    integral = lambda t: (_exp(5 * t) - 1) / 5
    _integral_value_test(f, _integrate, ts, integral, tol=1e-13)

    f = lambda t: _sin(5 * t)
    integral = lambda t: (1 -_cos(5 * t)) / 5
    _integral_value_test(f, _integrate, ts, integral, tol=1e-14)

    f = lambda t: t ** (1/3) if t >= 0 else -(-t)**(1/3)
    integral = lambda t: 3 / 4 * t * f(t)
    _integral_value_test(f, _integrate, ts, integral, tol=1e-7)



if __name__ == '__main__':
    test()