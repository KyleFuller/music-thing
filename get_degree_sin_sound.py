import math as _math
from typing import Callable as _Fn
from functools import cache as _cache

@_cache
def get_degree_sin_sound(
        degree: int, 
        key: _Fn[[int], float], 
        duration: float, 
        volume: float, 
        /
    ) -> tuple[(_Fn[[float], float]), float, float]:

    sin, pi = _math.sin, _math.pi

    nonfudged_frequency = key(degree)
    start = 0.
    stop = duration
    auditory_duration = stop - start
    fudged_frequency = round(nonfudged_frequency * auditory_duration) / auditory_duration
    return lambda t: sin(2 * pi * t * fudged_frequency) * volume, start, stop

def _s_0_m1_1_0(d: int, /) -> list[int]:

    if d == 0:
        return [0]
    else:
        return _s_0_m1_1_0(d - 1) + [e - 1 for e in _s_0_m1_1_0(d - 1)] + [e + 1 for e in _s_0_m1_1_0(d - 1)] + _s_0_m1_1_0(d - 1)

def main():
    from pitches import C
    
    from scales import ionian_scale, dorian_scale, harmonic_scale, aeolian_scale, phrygian_scale, major_pentatonic_scale, minor_pentatonic_scale # type: ignore

    degrees = _s_0_m1_1_0(6)
    key = aeolian_scale(C(4))
    duration = 0.25
    volume = 0.2

    from audio import make_audio, play_audio # type: ignore
    audio: list[float] = []
    for degree in degrees:
        sound, start, stop = get_degree_sin_sound(degree, key, duration, volume)
        audio.extend(make_audio(sound, start, stop))

    player = play_audio(audio)
    player.wait_done()
    from time import sleep
    sleep(0.5)

if __name__ == '__main__':
    main()







