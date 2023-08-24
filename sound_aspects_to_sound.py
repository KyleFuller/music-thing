from audio import *
import math

# from matplotlib import pyplot as plt
"""simple function that takes a volume function and a frequency function and
 returns the audio that results from the 2"""
def foo(start, stop, waving, frequency, volume, /):
    audio = [0 for i in range(SAMPLE_RATE * (stop - start))]
    times = linspace(start, stop, SAMPLE_RATE * (stop - start))

    summ = 0
    for i, t in enumerate(times):
        summ += frequency(t) / SAMPLE_RATE
        audio[i] = waving(summ, t) * volume(t)
        # print(volume(t))
    return audio

def bar(waving, frequency, volume, /):
    freq_integral = integral(frequency)
    return lambda t : waving(freq_integral(t), t) * volume(t)

def integral(f):

    def integral_from_zero_to_nonnegative(f):

        from_zero = [0]

        def integral_func(t):

            step_rate = SAMPLE_RATE
            inv_step_rate = 1 / SAMPLE_RATE
            batch_size = 64

            ceil_index = math.ceil(t * step_rate)
            old_len = len(from_zero)
            num_new_points = math.ceil(max(0, ceil_index + 1 - old_len) / batch_size) * batch_size
            # print(num_new_points)

            from_zero.extend([0 for _ in range(old_len, old_len + num_new_points)])
            
            summ = from_zero[old_len - 1]
            for i in range(old_len, old_len + num_new_points):
                from_zero[i] = summ = summ + f(i * inv_step_rate) * inv_step_rate
            
            # return from_zero[ceil_index]

            floor_index = math.floor(t * step_rate)

            if floor_index == ceil_index:
                return from_zero[floor_index]
            floor_index_t = floor_index * inv_step_rate

            return from_zero[floor_index] + (from_zero[ceil_index] - from_zero[floor_index]) * ((t - floor_index_t) * step_rate)
        return integral_func

    positive_side_integral = integral_from_zero_to_nonnegative(f)
    negative_side_integral = integral_from_zero_to_nonnegative(lambda t: -f(-t))
    def integral_func(t):
        if t >= 0:
            return positive_side_integral(t)
        else:
            return negative_side_integral(-t)
    return integral_func
            



def main():

    """ 
    This code is just meant to be a starting point to pick up from later.  
    It generates some example audio (a sine wave), plays it, and saves it.
    """

    start = -3
    stop = 3
    volume = lambda t: 0.25
    frequency = lambda t: 440 + 20 * sin(2*math.pi*t * 4) + 20 * t
    # frequency = lambda t: 440
    waving = lambda x, u: sin(2 * math.pi * x)
    # waving = lambda x, u: sin(2 * math.pi * x)
    audio = make_audio(start, stop, bar(waving, frequency, volume))
    # audio = foo(start, stop, waving, frequency, volume)
    # plt.plot(foo(duration, waving, frequency, volume))
    # plt.show()


    if len(audio) > 0 and stop - start <= 30:
        play_audio(audio).wait_done()

    # write_audio(audio, 'test.wav')


if __name__ == "__main__":
    main()