def linspace(start: float, stop: float, num: int, /) -> list[float]:
    step_duration = (stop - start) / num
    return [start + i * step_duration for i in range(num)]