
from typing import Iterable as _Iterable, Callable as _Fn, Iterator as _Iterator, Literal as _Literal
import itertools as _itertools

from audio import SAMPLE_RATE as _SAMPLE_RATE
from utils import cumul_sum as _cumul_sum

from get_bounds_iterator import get_bounds_iterator as _get_bounds_iterator
_Datum = tuple[float, tuple[_Fn[[float], float], tuple[float, float]]]


def _get_logical_times(data: _Iterable[_Datum], /):
    return _itertools.chain([0.], _cumul_sum(d[0] for d in data))

def _get_rel_intervals(data: _Iterable[_Datum]):
    return (rel_interval for _, (_, rel_interval) in data)

def _get_rel_sounds(data: _Iterable[_Datum], /):
    return (sound for _, (sound, _) in data)

def _get_rel_stops(data: _Iterable[_Datum], /):
    return (rel_stop for _, (_, (_, rel_stop)) in data)

def _get_bounds( 
        logical_times: _Iterable[float], 
        rel_intervals: _Iterable[tuple[float, float]],
        /) -> _Iterator[tuple[float, _Literal[0] | _Literal[1]]]:

    def get_fixed_intervals(
            logical_times: _Iterable[float], 
            rel_intervals: _Iterable[tuple[float, float]],
            /) -> _Iterator[tuple[float, float]]:
        return ((time + rel_start, time + rel_stop) 
                for time, (rel_start, rel_stop) in 
                    zip(logical_times, rel_intervals))  

    return _get_bounds_iterator(get_fixed_intervals(logical_times, rel_intervals))

def _get_logical_stops(logical_times: _Iterator[float], /):
    next(logical_times)
    return logical_times

def _get_fixed_sounds(logical_times: _Iterable[float], rel_sounds: _Iterable[_Fn[[float], float]], /):
    def fix_sound(sound: _Fn[[float], float], time: float) -> _Fn[[float], float]:
        """ This function is needed because creating the lambda directly in the
        comprehension for fixing sounds will result in lambdas capturing 
        non-constant variables, resulting in incorrect results. """
        return lambda t: sound(t - time)
    return (fix_sound(sound, time) for time, sound in zip(logical_times, rel_sounds))

def _get_fixed_stops(logical_times: _Iterable[float], rel_stops: _Iterable[float], /):
    return (time + rel_stop for time, rel_stop in zip(logical_times, rel_stops))

def sequence_sounds(data: _Iterable[_Datum], /
        ) -> _Iterable[float]:
    """
    input:
        an iterable of notes, each formatted as: 
            (<logical duration>, 
                (<sound function>, 
                    (<sound relative start>, <sound relative stop>)))
        the sounds of notes may overlap in time.

    output:
        an iterable of audio samples resulting from playing the notes in sequence
        at the times determined by placing the logical start of each note just 
        after the logical duration of the current note has elapsed.  The logical
        start of the first note is at time = 0.
    """

    data_iters = _itertools.tee(data, 4); del data
    data_for_logical_times, data_for_rel_intervals, data_for_rel_sounds, data_for_rel_stops = data_iters

    logical_times_for_tee = _get_logical_times(data_for_logical_times)
    logical_times_iterators = _itertools.tee(logical_times_for_tee, 4)
    (logical_times_for_bounds, logical_times_for_fixed_sounds, logical_times_for_logical_stops, 
        logical_times_for_fixed_stops) = logical_times_iterators

    rel_intervals = _get_rel_intervals(data_for_rel_intervals)
    rel_sounds = _get_rel_sounds(data_for_rel_sounds)
    rel_stops = _get_rel_stops(data_for_rel_stops)

    bounds = _get_bounds(logical_times_for_bounds, rel_intervals); del rel_intervals
    logical_stops = _get_logical_stops(logical_times_for_logical_stops)
    fixed_sounds = _get_fixed_sounds(logical_times_for_fixed_sounds, rel_sounds); del rel_sounds
    fixed_stops = _get_fixed_stops(logical_times_for_fixed_stops, rel_stops); del rel_stops

    current_sounds_by_stop: list[tuple[float, _Fn[[float], float]]] = []
    logical_stop_after_next = next(logical_stops)
    i = 0
    song_stop = None
    for bound_time, bound_kind in bounds:
        while (t := i / _SAMPLE_RATE) < bound_time and (song_stop is None or t < song_stop):
            v = sum(sound(t) for _, sound in current_sounds_by_stop)
            yield v
            i += 1
        if bound_kind == 0:
            current_sounds_by_stop.append(
                (next(fixed_stops), next(fixed_sounds)))
            logical_stop, logical_stop_after_next = logical_stop_after_next, next(logical_stops, None)
            if logical_stop_after_next is None:
                song_stop = logical_stop
        else:
            current_sounds_by_stop.remove(min(current_sounds_by_stop, key=lambda p: p[0]))