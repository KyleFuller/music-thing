from matplotlib import pyplot as plt
from pitches import *
from sound_aspects_to_sound import foo

from audio import *
from math import *








def main():


    duration = 20
    volume = lambda t: 1 
    frequency = lambda t: 440 - 44 * t


    audio = foo(0, duration, lambda x, t: sin(2 * pi * x), frequency, volume)
    play_audio(audio).wait_done()
    write_audio(audio, 'test.wav')


if __name__ == "__main__":
    main()