from typing import Iterable


def get_measurements(filename: str) -> Iterable[int]:
    with open(filename, 'r') as file:
        for line in file:
            yield int(line)


def get_number_increases(measurements: Iterable[int]) -> int:
    last = None
    increases = 0
    for measurement in measurements:
        if last is not None and measurement > last:
            increases += 1
        last = measurement
    return increases


def get_window_increases(measurements: Iterable[int]) -> int:
    measurements = list(measurements)
    last = None
    increases = 0
    for i in range(len(measurements) - 3 + 1):
        window = sum(measurements[i:i+3]) if last is None else (last - measurements[i-1] + measurements[i+2])
        if last is not None and window > last:
            increases += 1
        last = window
    return increases


if __name__ == '__main__':
    print(get_number_increases(get_measurements('input.txt')))
    print(get_window_increases(get_measurements('input.txt')))
