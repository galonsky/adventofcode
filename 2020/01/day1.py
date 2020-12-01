from typing import Iterable


def get_input(filename: str) -> Iterable[int]:
    with open(filename, 'r') as file:
        for line in file:
            yield int(line.rstrip())


if __name__ == '__main__':
    nums_set = set(num for num in get_input('input.txt'))
    for num in nums_set:
        diff = 2020 - num
        if diff in nums_set:
            print(num * diff)
            break
