def linspace(start: float, stop: float, num: int) -> list[float]:
    return [start + i * (stop - start) / num for i in range(num)]