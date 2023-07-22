import numpy as np
from math import sin, pi
import simpleaudio as sa
import wave




SAMPLE_RATE = 44_100



def make_audio(duration, sampler, /):
    """ TEMPORARY """
    return np.array(list(map(sampler, np.linspace(0, duration, SAMPLE_RATE * duration))));

def audio_to_wav_data(audio):
    """ TEMPORARY """
    return (audio * 2**15).astype(np.int16)

def write_audio(audio, name='untitled.wav', /):
    """ TEMPORARY """
    wav_data = audio_to_wav_data(audio)
    with wave.open(name, 'w') as f:
        f.setnchannels(1)
        f.setframerate(SAMPLE_RATE)
        f.setsampwidth(2)
        f.writeframes(wav_data)

def play_audio(audio):
    """ TEMPORARY """
    wav_data = audio_to_wav_data(audio)
    play_obj = sa.play_buffer(wav_data, 1, 2, SAMPLE_RATE)
    return play_obj




def foo(duration, volume, frequency):

    audio = make_audio(duration, lambda t: sin(t * 2 * pi * frequency(t)) * volume(t))
    return audio


def main():

    """ 
    This code is just meant to be a starting point to pick up from later.  
    It generates some example audio (a sine wave), plays it, and saves it.
    """

    duration = 10
    volume = lambda t: 1 * ((t) * .01)
    frequency = lambda t: 440 - ((t * 44))
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