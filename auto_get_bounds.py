from typing import Callable as _Fn

from audio import SAMPLE_RATE as _SAMPLE_RATE

def auto_get_stop(vol_bound: _Fn[[float], float]) -> float:
    """ similar to auto_get_bounds, but only gets the stop. """
    sample_dur = 1 / _SAMPLE_RATE
    
    outer_bound = sample_dur / 2
    while vol_bound(outer_bound) - 2**-15 > 0:
        outer_bound *= 2

    inner_bound = outer_bound / 2

    while (outer_bound - inner_bound) / inner_bound > 1e-6:
        midpoint = (outer_bound + inner_bound) / 2
        if vol_bound(midpoint) - 2**-15 > 0:
            inner_bound = midpoint
        else:
            outer_bound = midpoint
    return outer_bound

def auto_get_start(vol_func: _Fn[[float], float]) -> float:
    """ similar to auto_get_bounds, but only gets the start. """
    return -auto_get_stop(lambda t: vol_func(-t))

def auto_get_bounds(vol_func: _Fn[[float], float]) -> tuple[float, float]:
    """
    computes an audibility interval given a function that bounds some sound's
    volume from above, is non-increasing and then non-decreasing, and whose
    audibility interval contains t=0.  the audibility interval must be finite.
    """
    return auto_get_start(vol_func), auto_get_stop(vol_func)