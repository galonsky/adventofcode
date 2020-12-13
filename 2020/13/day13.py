from math import ceil
from typing import Tuple, List


def get_input(filename: str) -> Tuple[int, List[int]]:
    with open(filename, 'r') as file:
        contents = file.read()
        lines = contents.split('\n')
        earliest = int(lines[0])
        ids = []
        for id in lines[1].split(','):
            if id == 'x':
                continue
            ids.append(int(id))
        return earliest, ids


def part1():
    earliest, ids = get_input('input.txt')
    next_times = {
        id: ceil(earliest / id) * id for id in ids
    }
    min_id = min(next_times.keys(), key=lambda id: next_times[id])
    return min_id * (next_times[min_id] - earliest)


if __name__ == '__main__':
    print(part1())
