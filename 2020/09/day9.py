from collections import deque
from typing import Iterable, Set


def get_input(filename: str) -> Iterable[int]:
    with open(filename, 'r') as file:
        for line in file:
            yield int(line.rstrip('\n'))


def has_sum(num: int, past_nums: Set[int]) -> bool:
    for other_num in past_nums:
        if (num - other_num) in past_nums:
            return True
    return False


def part1():
    iterator = iter(get_input('input.txt'))
    window = deque(next(iterator) for i in range(25))
    window_set = set(window)
    while iterator:
        num = next(iterator)
        if not has_sum(num, window_set):
            return num
        leaving = window.popleft()
        window_set.remove(leaving)
        window.append(num)
        window_set.add(num)


if __name__ == '__main__':
    print(part1())
