from typing import Callable as _Fn

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

def integrate_with_step_rate(f: _Fn[[float], float], step_rate: float) -> _Fn[[float], float]:
    step_size = 1 / step_rate

    integral_vals = _get_cumulative_int_func_from_indexed_accumulators(
        0., 
        lambda so_far, i: so_far + _calculate_segment_integral_by_index(f, i, 0, step_size), 
        lambda so_far, i: so_far - _calculate_segment_integral_by_index(f, i - 1, 0, step_size))

    return lambda t: _approximate_int_input_func_on_float_input(integral_vals, t * step_rate)

def integrate(f: _Fn[[float], float]) -> _Fn[[float], float]:
    return integrate_with_step_rate(f, 4096)