def linspace(start, stop, num):
    return [start + i * (stop - start) / num for i in range(num)]