from typing import Iterable


def get_adapters(filename: str) -> Iterable[int]:
    with open(filename, 'r') as file:
        for line in file:
            yield int(line.rstrip('\n'))


def part1():
    