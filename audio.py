
from math import sin, pi
import simpleaudio as sa
import wave
import struct
from time import sleep

SAMPLE_RATE = 44_100

def linspace(start, stop, num):
    return [start + i * (stop - start) / num for i in range(num)]

def make_audio(start, stop, sampler, /):
    return ([sampler(s) for s in linspace(start, stop, SAMPLE_RATE * (stop - start))])

def audio_to_wav_data(audio):
    int_vals = [int(s * (2**15 - 1)) for s in audio]
    return struct.pack(f"<{len(int_vals)}h", *int_vals)

def write_audio(audio, name='untitled.wav', /):
    with wave.open(name, 'w') as f:
        f.setnchannels(1)
        f.setframerate(SAMPLE_RATE)
        f.setsampwidth(2)
        
        f.writeframes(audio_to_wav_data(audio))

def play_audio(audio):
    wav_data = audio_to_wav_data(audio)
    play_obj = sa.play_buffer(wav_data, 1, 2, SAMPLE_RATE)
    return play_obj

def main():

    """ 
    This code is just meant to be a starting point to pick up from later.  
    It generates some example audio (a sine wave), plays it, and saves it.
    """

    duration = 3
    volume = 0.02
    frequency = 330 

    audio = make_audio(duration, lambda t: sin(t * 2 * pi * frequency) * volume)

    play_audio(audio).wait_done()
    write_audio(audio, 'test.wav')


if __name__ == "__main__":
    main()