from audio import make_audio as _make_audio, play_audio as _play_audio, SAMPLE_RATE as _SAMPLE_RATE
from utils import linspace as _linspace
from sound_aspects import (
    WavingFunction as _WavingFunction, 
    FrequencyFunction as _FrequencyFunction, 
    VolumeFunction as _VolumeFunction)
from SoundFunction import SoundFunction as _SoundFunction
from FunctionOnFiniteInterval import FunctionOnFiniteInterval as _FunctionOnFiniteInterval
import math as _math
from typing import Callable

# from matplotlib import pyplot as plt
"""simple function that takes a volume function and a frequency function and
 returns the audio that results from the 2"""
def foo(start: float, stop: float, waving: _WavingFunction, frequency: _FrequencyFunction, volume: _VolumeFunction, /):
    audio = [0. for _ in range(_math.ceil(_SAMPLE_RATE * (stop - start)))]
    times = _linspace(start, stop, _math.ceil(_SAMPLE_RATE * (stop - start)))

    summ = 0
    for i, t in enumerate(times):
        summ += frequency(t) / _SAMPLE_RATE
        audio[i] = waving(summ, t) * volume(t)
        # print(volume(t))
    return audio

def make_sound(
        waving: _WavingFunction, 
        frequency: _FrequencyFunction, 
        volume: _VolumeFunction, 
        /
    ) -> _SoundFunction:

    freq_integral = _integrate(frequency)
    return _SoundFunction(lambda t : waving(t, freq_integral(t)) * volume(t), frequency.get_start(), frequency.get_stop())

def _integrate_on_unknown_interval(f: Callable[[float], float]) -> Callable[[float], float]: # type: ignore
    
    def integrate_from_zero_to_nonnegative(f: Callable[[float], float]) -> Callable[[float], float]:

        from_zero = [0.]

        def integral(t: float):

            step_rate = _SAMPLE_RATE
            inv_step_rate = 1 / _SAMPLE_RATE
            batch_size = 64

            ceil_index = _math.ceil(t * step_rate)
            old_len = len(from_zero)
            num_new_points = _math.ceil(max(0, ceil_index + 1 - old_len) / batch_size) * batch_size
            # print(num_new_points)

            from_zero.extend([0. for _ in range(old_len, old_len + num_new_points)])
            
            summ = from_zero[old_len - 1]
            for i in range(old_len, old_len + num_new_points):
                from_zero[i] = summ = summ + f(i * inv_step_rate) * inv_step_rate
            
            # return from_zero[ceil_index]

            floor_index = _math.floor(t * step_rate)

            if floor_index == ceil_index:
                return from_zero[floor_index]
            floor_index_t = floor_index * inv_step_rate

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
            
def _integrate(f: _FunctionOnFiniteInterval) -> _FunctionOnFiniteInterval:
    start, stop = f.get_start(), f.get_stop()
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
    return _FunctionOnFiniteInterval(integral, f.get_start(), f.get_stop())

def main():

    """ 
    This code is just meant to be a starting point to pick up from later.  
    It generates some example audio (a sine wave), plays it, and saves it.
    """

    start = -3
    stop = 3
    volume = _VolumeFunction(lambda t: 0.25, start, stop)
    frequency = _FrequencyFunction(lambda t: 440 + 20 * _math.sin(2*_math.pi*t * 4) + 20 * t, start, stop)
    # frequency = lambda t: 440
    waving = _WavingFunction(lambda t, x: _math.sin(2 * _math.pi * x), start, stop)
    # waving = lambda x, u: sin(2 * math.pi * x)
    audio = _make_audio(start, stop, make_sound(waving, frequency, volume))
    # audio = foo(start, stop, waving, frequency, volume)
    # plt.plot(foo(duration, waving, frequency, volume))
    # plt.show()


    if len(audio) > 0 and stop - start <= 30:
        _play_audio(audio).wait_done()

    # save_audio(audio, 'test.wav')


if __name__ == "__main__":
    main()