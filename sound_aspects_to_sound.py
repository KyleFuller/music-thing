from integrate import integrate_on_unknown_interval as _integrate_on_unknown_interval

from typing import Callable as _Fn

def make_sound(
        get_waveform: _Fn[[float], _Fn[[float], float]],
        get_frequency: _Fn[[float], float],
        get_volume: _Fn[[float], float],
        /
    ) -> _Fn[[float], float]:

    """
    returns a function that at any given point of time, has the waveform given by
    by get_waveform at that time, the frequency given by get_frequency, and scaled by
    get_volume at that time.

    get_waveform, given a time, should return the waveform at that time.
    the waveform should have a period of 1 (but does not need to be perfectly
    periodic), and the output should be bound between -1 and 1.

    get_volume should be bound between -1 and 1.
    """

    freq_integral = _integrate_on_unknown_interval(get_frequency)

    def sound(t: float):
        return get_waveform(t)(freq_integral(t)) * get_volume(t)

    return sound
