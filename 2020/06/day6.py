from typing import Iterable, List


def get_raw_groups(filename: str) -> List[str]:
    with open(filename, 'r') as file:
        contents = file.read()
        groups = contents.split('\n\n')
        return groups


def part1():
    total_count = 0
    for group in get_raw_groups('input.txt'):
        letters = set(iter(group.replace('\n', '')))
        total_count += len(letters)
    print(total_count)


if __name__ == '__main__':
    part1()