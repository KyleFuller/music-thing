from sound_aspects_to_sound import make_sound as _make_sound

import abc as _abc
import math as _math
from typing import Callable as _Callable

class Note(_abc.ABC):

    @_abc.abstractmethod
    def __init__(self):
        pass

    @_abc.abstractmethod
    def get_duration(self):
        pass

    @_abc.abstractmethod
    def get_sound(self):
        pass

class KeyNote:

    def __init__(self, *, 
            key: _Callable[[int], float], 
            degree: int, 
            duration: float, 
            volume: float):
        self._scale = key
        self._degree = degree
        self._duration = duration
        self._volume = volume

    def get_duration(self) -> float:
        return self._duration
    
    def get_start(self) -> float:
        return 0.
    
    def get_stop(self) -> float:
        return self._duration

    def get_sound(self) -> _Callable[[float], float]:
        sin, pi = _math.sin, _math.pi

        nonfudged_frequency = self._scale(self._degree)
        start = self.get_start()
        stop = self.get_stop()
        auditory_duration = stop - start
        fudged_frequency = round(nonfudged_frequency * auditory_duration) / auditory_duration
        frequency: _Callable[[float], float] = lambda _: fudged_frequency
        volume: _Callable[[float], float] = lambda _: self._volume
        waving: _Callable[[float, float], float] = lambda _, x: sin(2 * pi * x)
        return _make_sound(
            waving, 
            frequency,
            volume,
            start,
            stop)

def s_0_m1_1_0(d: int) -> list[int]:

    if d == 0:
        return [0]
    else:
        return s_0_m1_1_0(d - 1) + [e - 1 for e in s_0_m1_1_0(d - 1)] + [e + 1 for e in s_0_m1_1_0(d - 1)] + s_0_m1_1_0(d - 1)

def main():
    from pitches import C
    
    from scales import ionian_scale, dorian_scale, harmonic_scale, aeolian_scale, phrygian_scale, major_pentatonic_scale, minor_pentatonic_scale # type: ignore

    notes = [KeyNote(key=minor_pentatonic_scale(C(4)), degree=d, duration=0.25, volume=0.2) for d in range(6)]

    from audio import make_audio, play_audio
    audio: list[float] = []
    for note in notes:
        audio.extend(make_audio(note.get_sound(), note.get_start(), note.get_stop()))

    # from matplotlib import pyplot as plt
    # plt.plot(audio)
    # plt.show()

    player = play_audio(audio)
    player.wait_done()
    from time import sleep
    sleep(0.5)

if __name__ == '__main__':
    main()







