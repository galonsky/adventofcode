from typing import Iterable


def get_adapters(filename: str) -> Iterable[int]:
    with open(filename, 'r') as file:
        for line in file:
            yield int(line.rstrip('\n'))


def part1():
    adapters = list(get_adapters('input.txt'))
    adapters.append(max(adapters) + 3)
    adapters.sort()
    last = 0

    one_diffs = 0
    three_diffs = 0
    for adapter in adapters:
        diff = adapter - last
        if diff == 1:
            one_diffs += 1
        elif diff == 3:
            three_diffs += 1
        else:
            raise Exception('unexpected!')
        last = adapter

    print(one_diffs * three_diffs)


if __name__ == '__main__':
    part1()
