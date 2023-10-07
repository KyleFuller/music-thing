from typing import Iterable as _Iterable, Callable as _Fn
from collections.abc import Collection as _Collection
from math import ceil as _ceil

from audio import SAMPLE_RATE as _SAMPLE_RATE

_Datum = tuple[float, _Fn[[float], float], float, float]

def sequence_sounds(data_iterable: _Iterable[_Datum], /) -> list[float]:
    if isinstance(data_iterable, _Collection):
        data: _Collection[_Datum] = data_iterable
    else:
        data: _Collection[_Datum] = list(data_iterable)

    total_duration = sum(datum[0] for datum in data)
    num_samples = _ceil(total_duration * _SAMPLE_RATE)
    samples = [0.] * num_samples

    time = 0.
    for datum in data:
        logical_duration, sound, rel_sound_start, rel_sound_stop = datum
        
        sound_start_idx = max(0, round((time + rel_sound_start) * _SAMPLE_RATE))
        sound_stop_idx = min(num_samples - 1, round((time + rel_sound_stop) * _SAMPLE_RATE))

        for i, i0 in enumerate(range(sound_start_idx, sound_stop_idx)):
            samples[i0] += sound(rel_sound_start + i / _SAMPLE_RATE)
        
        time += logical_duration

    return samples