# type: ignore

from pitch_letters import *
from sound_aspects_to_sound import foo
from FunctionOnFiniteInterval import FunctionOnFiniteInterval

from audio import play_audio as _play_audio, write_audio as _write_audio
from math import *

def make_two_notes(duration: float, /):
    def two_notes(t):
        if floor(t) < (duration /2):
            return A(4)
        else:
            return G(5)
    return two_notes

def simple_melody(t, /):
    if t < 5:
        if floor(t) % 2 == 0:
            return A(4)
        else:
            return G(5)
    else:
        if (floor(t*2) /2) == floor(t):
            return A(4)
        else:
            return G(5)
        
def melody(t, /):
    if floor(t) % 4 == 0:
        return C(4)
    if floor(t) % 4 == 1:
        return E(4)
    if floor(t) % 4 == 2:
        return C(4)
    if floor(t) % 4 == 3:
        return A(4)
    

def play_CM7_arpegio(t, /):
    if floor(t) % 4 == 0:
        return C(4)
    if floor(t) % 4 == 1:
        return E(4)
    if floor(t) % 4 == 2:
        return G(4)
    if floor(t) % 4 == 3:
        return B(4)
        
    
# """simple function that takes a volume function and a frequency function and
#  returns the audio that results from the 2"""
# def foo(duration, volume, frequency):

#     audio = [0 for i in range(SAMPLE_RATE * duration)]
#     times = linspace(0, duration, SAMPLE_RATE * duration)

#     summ = 0
#     for i, t in enumerate(times):
#         summ += frequency(t) / SAMPLE_RATE
#         audio[i] = sin(summ * 2 * pi) * volume(t)
#     plt.plot(audio)
#     plt.show()
#     return audio


def main():

    """ 
    This code is just meant to be a starting point to pick up from later.  
    It generates some example audio (a sine wave), plays it, and saves it.
    """

    duration = 20
    volume = lambda t: 1 
    "(sin(2 * pi * t * 1 ) + 1 )/2"
    frequency = lambda t: 440 - 44 * t
    """
    volume = 0.1
    frequency = 330

    audio = make_audio(duration, lambda t: sin(t * 2 * pi * frequency) * volume)
    """
    "audio = foo(duration, volume, frequency )"

    two_notes = make_two_notes(duration)
    audio = foo(0, duration, lambda x, t: sin(2 * pi * x), play_CM7_arpegio, volume)
    _play_audio(audio).wait_done()
    _write_audio(audio, 'test.wav')


if __name__ == "__main__":
    main()