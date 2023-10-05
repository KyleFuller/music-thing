import math as _math
from typing import Callable as _Fn

from audio import SAMPLE_RATE as _SAMPLE_RATE
from cumulative_functions import (
    get_cumulative_int_func_from_indexed_accumulators as _get_cumulative_int_func_from_indexed_accumulators)
from function_approximation import (
    approximate_int_input_func_on_float_input as _approximate_int_input_func_on_float_input)

def _calculate_segment_integral(f: _Fn[[float], float], step_size: float, left: float, middle: float, right: float):
    midpoint_rule_estimate = f(middle) * step_size
    trapezoid_rule_estimate = (f(left) + f(right)) / 2 * step_size
    return 2/3 * midpoint_rule_estimate + 1/3 * trapezoid_rule_estimate

def _calculate_segment_integral_by_index(f: _Fn[[float], float], i: int, start: float, step_size: float):
    return _calculate_segment_integral(f, step_size,
        start + i * step_size, 
        start + (i + 0.5) * step_size, 
        start + (i + 1) * step_size)

def integrate_on_unknown_interval(f: _Fn[[float], float]) -> _Fn[[float], float]:
    step_rate = _SAMPLE_RATE
    step_duration = 1 / step_rate

    integral_vals = _get_cumulative_int_func_from_indexed_accumulators(
        0., 
        forward=lambda so_far, i: so_far + _calculate_segment_integral_by_index(f, i, 0, step_duration), 
        backward=lambda so_far, i: so_far - _calculate_segment_integral_by_index(f, i - 1, 0, step_duration))

    return lambda t: _approximate_int_input_func_on_float_input(integral_vals, t * step_rate)
            
def integrate_on_known_interval(f: _Fn[[float], float], start: float, stop: float) -> _Fn[[float], float]:
    step_rate = _SAMPLE_RATE
    step_duration = 1 / _SAMPLE_RATE
    auditory_duration = stop - start
    num_steps = _math.ceil(auditory_duration * step_rate)
    integral_vals_ls = [0.] * (num_steps + 1)
    for i in range(1, num_steps):
        integral_vals_ls[i] = integral_vals_ls[i - 1] + _calculate_segment_integral_by_index(f, i - 1, start, step_duration)
    def integral_vals(i: int): 
        return integral_vals_ls[i]
    return lambda t: _approximate_int_input_func_on_float_input(integral_vals, (t - start) * step_rate)

    