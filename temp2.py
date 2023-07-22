from temp import *
from matplotlib import pyplot as plt


"""simple function that takes a volume function and a frequency function and
 returns the audio that results from the 2"""
def foo(duration, volume, frequency):

    audio = [0 for i in range(SAMPLE_RATE * duration)]
    times = linspace(0, duration, SAMPLE_RATE * duration)

    summ = 0
    for i, t in enumerate(times):
        summ += frequency(t) / SAMPLE_RATE
        audio[i] = sin(summ * 2 * pi) * volume(t)
    plt.plot(audio)
    plt.show()
    return audio


def main():

    """ 
    This code is just meant to be a starting point to pick up from later.  
    It generates some example audio (a sine wave), plays it, and saves it.
    """

    duration = 10
    volume = lambda t: (sin(2 * pi * t * 1 ) + 1 )/2
    frequency = lambda t: 440 - 44 * t
    """
    volume = 0.1
    frequency = 330

    audio = make_audio(duration, lambda t: sin(t * 2 * pi * frequency) * volume)
    """
    audio = foo(duration, volume, frequency )
    play_audio(audio).wait_done()
    write_audio(audio, 'test.wav')


if __name__ == "__main__":
    main()