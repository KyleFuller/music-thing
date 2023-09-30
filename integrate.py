from audio import SAMPLE_RATE as _SAMPLE_RATE

import math as _math
from typing import Callable as _Fn
    

def integrate_on_unknown_interval(f: _Fn[[float], float]) -> _Fn[[float], float]:
    
    # TODO: Document this mess.

    def integrate_from_zero_to_nonnegative(f: _Fn[[float], float]):
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
                val_midpoint = f((i - 0.5) * inv_step_rate) # use just this for less overkill precision.
                    # use both for simpson's method.
                val_sides = (f((i - 1) * inv_step_rate) + f(i * inv_step_rate)) / 2
                from_zero[i] = summ = summ + (2/3 * val_midpoint + 1/3 * val_sides) * inv_step_rate
            floor_index = _math.floor(t * step_rate)

            if floor_index == ceil_index:
                return from_zero[floor_index]
            floor_index_t = floor_index * inv_step_rate

            # this is an interpolation method that I hacked up through trial and error
                # and seems to be accurate almost to machine precision for well-behaved
                # functions.  It works by using the error of one cubic interpolation
                # method to cancel out most of the error of another cubic interpolation 
                # method.  It needs clarity, documentation, cleanup, and optimization. 

            if floor_index >= 0:
                # TODO: Put this stuff into functions, stop reusing variable names,
                    # and EXPLAIN.

                mu = ((t - floor_index_t) * step_rate)
                mu2 = mu * mu
                y0 = from_zero[floor_index - 1] if floor_index > 0 else -from_zero[ceil_index]
                y1 = from_zero[floor_index]
                y2 = from_zero[ceil_index]
                y3 = from_zero[ceil_index + 1]
                a0 = -0.5*y0 + 1.5*y1 - 1.5*y2 + 0.5*y3
                a1 = y0 - 2.5*y1 + 2*y2 - 0.5*y3
                a2 = -0.5*y0 + 0.5*y2
                a3 = y1
                v = a0*mu*mu2+a1*mu2+a2*mu+a3

                y0 = from_zero[floor_index - 1] if floor_index > 0 else -from_zero[ceil_index]
                y1 = from_zero[floor_index]
                y2 = from_zero[ceil_index]
                mu = ((t - floor_index_t) * step_rate)

                a = 0.5 * (y0 - 2 * y1 + y2)
                b = 0.5 * (y2 - y0)
                c = y1
                
                g = a * mu**2 + b * mu + c

                y0_ = from_zero[ceil_index + 1]
                y1_ = from_zero[ceil_index]
                y2_ = from_zero[floor_index]
                mu_ = 1 - mu

                a_ = 0.5 * (y0_ - 2 * y1_ + y2_)
                b_ = 0.5 * (y2_ - y0_)
                c_ = y1_

                g_ = a_ * mu_**2 + b_ * mu_ + c_

                other_v = (g + g_) / 2

                return v * 1 / 3 + other_v * 2 / 3
            return from_zero[floor_index] + (from_zero[ceil_index] - from_zero[floor_index]) * ((t - floor_index_t) * step_rate)
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