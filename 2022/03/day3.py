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
    if shared_char.islower():
        return ord(shared_char) - ord('a') + 1
    else:
        return ord(shared_char) - ord('A') + 27


def get_sum_of_priorities(filename: str) -> int:
    rucksacks = get_rucksacks(filename)
    return sum(get_priority(sack) for sack in rucksacks)


if __name__ == '__main__':
    print(get_sum_of_priorities("input.txt"))