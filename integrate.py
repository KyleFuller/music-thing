from audio import SAMPLE_RATE as _SAMPLE_RATE

import math as _math
from typing import Callable as _Fn
    

def _catmull_rom_interpolate(y0: float, y1: float, y2: float, y3: float) -> _Fn[[float], float]:
    def interpolation(mu: float):
        mu_sq = mu * mu
        a0 = -0.5*y0 + 1.5*y1 - 1.5*y2 + 0.5*y3
        a1 = y0 - 2.5*y1 + 2*y2 - 0.5*y3
        a2 = -0.5*y0 + 0.5*y2
        a3 = y1
        return a0*mu*mu_sq+a1*mu_sq+a2*mu+a3
    return interpolation

def _quadratic_interpolate(y0: float, y1: float, y2: float) -> _Fn[[float], float]:
    def interpolation(mu: float):

        a = 0.5 * (y0 - 2 * y1 + y2)
        b = 0.5 * (y2 - y0)
        c = y1
        
        return a * mu**2 + b * mu + c

    return interpolation

def _quadratic_approximate(y0: float, y1: float, y2: float, y3: float) -> _Fn[[float], float]:
    q_left = _quadratic_interpolate(y0, y1, y2)
    q_right = _quadratic_interpolate(y3, y2, y1)
    def approximation(mu: float):
        return 0.5*q_left(mu) + 0.5*q_right(1 - mu)
    return approximation

def _cubic_approximate(y0: float, y1: float, y2: float, y3: float) -> _Fn[[float], float]:
    cr = _catmull_rom_interpolate(y0, y1, y2, y3)
    q = _quadratic_approximate(y0, y1, y2, y3)
    
    def approximation(mu:float):
        return 1/3*cr(mu) + 2/3*q(mu)
    
    return approximation

def _linear_approximate(y0: float, y1: float) -> _Fn[[float], float]: # type: ignore

    def approximation(mu:float):
        return y0 * (1 - mu) + y1 * mu
    
    return approximation

def integrate_on_unknown_interval(f: _Fn[[float], float]) -> _Fn[[float], float]:
    
    # TODO: Document this mess.

    def integrate_from_zero_to_nonnegative(_f: _Fn[[float], float]):
        from_zero = [0.]

        step_rate = _SAMPLE_RATE
        inv_step_rate = 1 / step_rate
        batch_size = 64

        def integral(t: float):

            ceil_index = _math.ceil(t * step_rate)
            old_len = len(from_zero)
            # the extra 1 added to the whole thing is for the sake of interpolation methods that need
                # an extra point to the right.
            num_new_points = _math.ceil(max(0, ceil_index + 1 - old_len) / batch_size) * batch_size + 1

            from_zero.extend([0. for _ in range(old_len, old_len + num_new_points)])
            
            summ = from_zero[old_len - 1]
            for i in range(old_len, old_len + num_new_points):
                val_midpoint = _f((i - 0.5) * inv_step_rate) # use just this for less overkill precision.
                    # use both for simpson's method.
                val_sides = (_f((i - 1) * inv_step_rate) + _f(i * inv_step_rate)) / 2
                from_zero[i] = summ = summ + (2/3 * val_midpoint + 1/3 * val_sides) * inv_step_rate
            floor_index = _math.floor(t * step_rate)

            if floor_index == ceil_index:
                return from_zero[floor_index]
            floor_index_t = floor_index * inv_step_rate


            y0 = from_zero[floor_index - 1] if floor_index > 0 else -(_f(-0.5 * inv_step_rate) * 2/3 + 1/3 * (_f((- 1) * inv_step_rate) + _f(0)) / 2) * inv_step_rate
            y1 = from_zero[floor_index]
            y2 = from_zero[ceil_index]
            y3 = from_zero[ceil_index + 1]

            mu = ((t - floor_index_t) * step_rate)
            return _cubic_approximate(y0, y1, y2, y3)(mu)

        return integral

    positive_side_integrate = integrate_from_zero_to_nonnegative(f)
    negative_side_integrate = integrate_from_zero_to_nonnegative(lambda t: -f(-t))
    def integral(t: float):
        if t >= 0:
            return positive_side_integrate(t)
        else:
            return negative_side_integrate(-t)
    return integral
            
def integrate_on_known_interval(f: _Fn[[float], float], start: float, stop: float) -> _Fn[[float], float]: # type: ignore
    auditory_duration = stop - start
    step_rate = _SAMPLE_RATE
    inv_step_rate = 1 / _SAMPLE_RATE
    num_steps = _math.ceil(auditory_duration * step_rate)
    from_start = [0. for _ in range(num_steps + 1)]
    for i in range(1, num_steps):
        from_start[i] = from_start[i - 1] + f(start + i * inv_step_rate) * inv_step_rate

    def integral(t: float):
        floor_index = _math.floor((t - start) * step_rate)
        ceil_index = _math.ceil((t - start) * step_rate)
        if floor_index == ceil_index:
            return from_start[floor_index]
        floor_index_t = start + floor_index * inv_step_rate

        return from_start[floor_index] + (from_start[ceil_index] - from_start[floor_index]) * ((t - floor_index_t) * step_rate)
    return integral