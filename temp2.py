from temp import *

"def two_notes"

"""simple function that takes a volume function and a frequency function and
 returns the audio that results from the 2"""
def foo(duration, volume, frequency):

    audio = make_audio(duration, lambda t: sin(t * 2 * pi * frequency(t)) * volume(t))
    return audio


def main():

    """ 
    This code is just meant to be a starting point to pick up from later.  
    It generates some example audio (a sine wave), plays it, and saves it.
    """

    duration = 10
    volume = lambda t: (sin(2 * pi * t * 100 ) + 1 )/2
    frequency = lambda t: 440
    """
    volume = 0.02
    frequency = 330

    audio = make_audio(duration, lambda t: sin(t * 2 * pi * frequency) * volume)
    """
    audio = foo(duration, volume, frequency )
    play_audio(audio).wait_done()
    write_audio(audio, 'test.wav')


if __name__ == "__main__":
    main()