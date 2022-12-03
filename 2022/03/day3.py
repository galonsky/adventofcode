from functools import reduce
from typing import Generator


def get_rucksacks(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


def _get_shared_char(str1: str, str2: str) -> str:
    return next(iter(set(str1) & set(str2)))


def get_priority(rucksack: str) -> int:
    firsthalf = rucksack[:len(rucksack) // 2]
    secondhalf = rucksack[len(rucksack) // 2:]
    shared_char = _get_shared_char(firsthalf, secondhalf)
    return get_char_priority(shared_char)


def get_char_priority(shared_char):
    if shared_char.islower():
        return ord(shared_char) - ord('a') + 1
    else:
        return ord(shared_char) - ord('A') + 27


def get_sum_of_priorities(filename: str) -> int:
    rucksacks = get_rucksacks(filename)
    return sum(get_priority(sack) for sack in rucksacks)


def get_sum_of_group_priorities(filename: str) -> int:
    rucksack_iter = iter(get_rucksacks(filename))
    priorities = 0
    try:
        while True:
            groups = [set(next(rucksack_iter)) for _ in range(3)]
            char_set = reduce(lambda acc, sack: acc.intersection(sack), groups)
            priorities += get_char_priority(next(iter(char_set)))
    except StopIteration:
        pass
    return priorities


if __name__ == '__main__':
    print(get_sum_of_group_priorities("input.txt"))
