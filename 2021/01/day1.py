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


if __name__ == '__main__':
    print(get_number_increases(get_measurements('input.txt')))
