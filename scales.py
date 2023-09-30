
from typing import Callable as _Fn

Key = _Fn[[int], float]
Scale = _Fn[[float], Key]

def harmonic_scale(root_freq: float, /) -> Key:
    def pitch_key(d: int):
        return root_freq * 2 ** (d / 12)
    return pitch_key

def derive_scale(source_scale: Scale, degs: list[int], /) -> Scale:
    def scale(root_freq: float):
        source_key = source_scale(root_freq)
        def key(d: int):
            return source_key(degs[d % len(degs)] + (d // len(degs)) * 12)
        return key
    return scale

def make_mode(source_scale: Scale, offset: int, /) -> Scale:
    def mode(root_freq: float):
        source_key = source_scale(root_freq)
        def key(d: int):
            return source_key(d + offset) * root_freq / source_key(offset)
        return key
    return mode

ionian_scale = derive_scale(harmonic_scale, [0, 2, 4, 5, 7, 9, 11])
dorian_scale = make_mode(ionian_scale, 1)
phrygian_scale = make_mode(ionian_scale, 2)
lydian_scale = make_mode(ionian_scale, 3)
mixolydian_scale = make_mode(ionian_scale, 4)
aeolian_scale = make_mode(ionian_scale, 5)
locrian_scale = make_mode(ionian_scale, 6)

major_pentatonic_scale = derive_scale(harmonic_scale, [0, 2, 4, 7, 9])
suspended_pentatonic_scale = make_mode(major_pentatonic_scale, 1)
blues_minor_pentatonic_scale = make_mode(major_pentatonic_scale, 2)
blues_major_pentatonic_scale = make_mode(major_pentatonic_scale, 3)
minor_pentatonic_scale = make_mode(major_pentatonic_scale, 4)

wholetone_scale = derive_scale(harmonic_scale, [0, 2, 4, 6, 8, 10])

whole_half_scale = derive_scale(harmonic_scale, [0, 2, 3, 5, 6, 8, 9, 11])
half_whole_scale = make_mode(whole_half_scale, 1)