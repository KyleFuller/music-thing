# type: ignore

import numpy as np
import simpleaudio as sa
import wave

SAMPLE_RATE = 44_100


def make_audio(duration, sampler, /):
    """ TEMPORARY """
    print(np.linspace(0, duration, SAMPLE_RATE * duration))
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