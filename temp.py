
import numpy as np
import simpleaudio as sa
import wave

SAMPLE_RATE = 44_100

def main():

    """ 
    This code is just meant to be a starting point to pick up from later.  
    It generates some example audio (a sine wave), plays it, and saves it.
    """

    duration = 3
    volume = 0.02
    frequency = 330

    audio = np.sin(np.linspace(0, duration, SAMPLE_RATE * duration) * 2 * np.pi * frequency) * volume

    wav_data = (audio * 2**15).astype(np.int16)

    play_obj = sa.play_buffer(wav_data, 1, 2, SAMPLE_RATE)
    play_obj.wait_done()

    with wave.open('untitled.wav', 'w') as f:

        f.setnchannels(1)
        f.setframerate(SAMPLE_RATE)
        f.setsampwidth(2)
        f.writeframes(wav_data)



if __name__ == "__main__":
    main()