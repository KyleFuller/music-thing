import math as _math
from typing import Callable as _Fn

from real_function_transformations import (
    mul as _fn_mul, scale_2d as _scale_2d,
    translate_input as _translate_input,
    scale_input as _scale_input,
    scale_output as _scale_output,
    translate_output as _translate_output)
from auto_get_bounds import auto_get_bounds as _auto_get_bounds
from waves import sin_wave as _sin_wave, cos_wave as _cos_wave
from humps import cos_hump as _cos_hump

def get_degree_sin_sound(
        degree: int, 
        key: _Fn[[int], float], 
        duration: float, 
        volume: float, 
        /
    ) -> tuple[(_Fn[[float], float]), tuple[float, float]]:

    sin, pi = _math.sin, _math.pi

    nonfudged_frequency = key(degree)
    start = 0.
    stop = duration
    auditory_duration = stop - start
    fudged_frequency = round(nonfudged_frequency * auditory_duration) / auditory_duration
    return lambda t: sin(2 * pi * t * fudged_frequency) * volume, (start, stop)

def get_degree_cos_hump_sound(
        degree: int, 
        key: _Fn[[int], float], 
        duration: float, 
        volume: float, 
        hump_ratio: float,
        /
    ) -> tuple[(_Fn[[float], float]), tuple[float, float]]:

    frequency = key(degree)
    tone = _scale_input(1 / frequency, _sin_wave)
    vol_func = _translate_input(duration / 2, _scale_2d(duration * hump_ratio, volume, _cos_hump))

    sound = _fn_mul(tone, vol_func)

    return sound, _auto_get_bounds(vol_func)

from humps import exp_fade_hump as _exp_fade_hump

def get_degree_exp_fading_sound(
        degree: int, 
        key: _Fn[[int], float], 
        duration: float, 
        volume: float, 
        hump_ratio: float,
        /
    ) -> tuple[(_Fn[[float], float]), tuple[float, float]]:

    frequency = key(degree)
    tone = _scale_input(1 / frequency, _scale_output(1/2, _translate_output(-1, _cos_wave)))
    vol_func: _Fn[[float], float] = _scale_2d(duration * hump_ratio, volume, _exp_fade_hump)

    sound = _fn_mul(tone, vol_func)
    return sound, _auto_get_bounds(vol_func)