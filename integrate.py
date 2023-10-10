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
    """
    Given f from the reals to the reals and a step rate, returns a function approximating the integral of f from 0 to a
    given value, using the given step rate for the quadrature and for interpolating between quadrature points.

    f must be defined on all real numbers.  This requirement is not actively checked, and calling the returned function
    may or may not return a value if the requirement is not met.
    
    A kind of caching is used by the returned function to speed up repeated calls to that returned function.
    As such, if the value of the integral of the same function is needed many times, it is best to integrate once and
    then call the integral many times, rather than integrating each time the integral is needed.
    """
    step_size = 1 / step_rate

    integral_vals = _get_cumulative_int_func_from_indexed_accumulators(
        0., 
        lambda so_far, i: so_far + _calculate_segment_integral_by_index(f, i, 0, step_size), 
        lambda so_far, i: so_far - _calculate_segment_integral_by_index(f, i - 1, 0, step_size))

    return lambda t: _approximate_int_input_func_on_float_input(integral_vals, t * step_rate)

def integrate(f: _Fn[[float], float]) -> _Fn[[float], float]:
    """
    The same as integrate_with_step_rate, but with a default value for the step rate that is small enough to be fairly
    performant but large enough to be quite accurate for well-behaved functions, which tend to be common in practice.
    """
    return integrate_with_step_rate(f, 4096)