
from typing import Callable as _Fn, Iterable as _Iterable

Key = _Fn[[int], float]
""" A key is a strictly increasing function from integer "degrees" to frequencies. """

Scale = _Fn[[float], Key]
""" A scale is a function from a root frequency to a key that returns the root frequency given degree 0. """

def harmonic_scale(root_freq: float, /) -> Key:
    """ A scale with 12 (logarithmically) equally spaced pitches per octave. """
    def key(d: int):
        return root_freq * 2 ** (d / 12)
    return key

def derive_scale(source_scale: Scale, degs_iterable: _Iterable[int], /) -> Scale:
    """ Given a scale and an iterable of degrees, returns another scale that selects only the given degrees from the 
    original scale."""
    degs = list(degs_iterable)
    def scale(root_freq: float):
        source_key = source_scale(root_freq)
        def key(d: int):
            return source_key(degs[d % len(degs)] + (d // len(degs)) * 12)
        return key
    return scale

def make_mode(source_scale: Scale, offset: int, /) -> Scale:
    """ Produces a scale that "starts" at the degree `offset` of the source scale. """
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