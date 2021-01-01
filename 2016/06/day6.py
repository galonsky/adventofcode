from collections import defaultdict, Counter
from typing import Iterable


def get_input(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def part1():
    words = get_input('input.txt')
    counter_by_position = defaultdict(Counter)
    for word in words:
        for i, ch in enumerate(word):
            counter_by_position[i][ch] += 1
    return ''.join([counter_by_position[pos].most_common(1)[0][0] for pos in sorted(counter_by_position.keys())])


if __name__ == '__main__':
    print(part1())
