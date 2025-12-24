from typing import Generator


def get_banks(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


def get_joltage(bank: str) -> int:
    highest = 0
    index = 0
    for i, ch in enumerate(bank[:-1]):
        as_num = int(ch)
        if as_num > highest:
            highest = as_num
            index = i

    second_highest = 0
    for i in range(index + 1, len(bank)):
        as_num = int(bank[i])
        if as_num > second_highest:
            second_highest = as_num

    return highest * 10 + second_highest

def get_max_and_index(corpus: list[int], start: int, end: int) -> tuple[int, int]:
    highest = 0
    index = 0
    for i in range(start, end):
        n = corpus[i]
        if n > highest:
            highest = n
            index = i
    return highest, index


def get_joltage_12(bank: str) -> int:
    num_found = 0
    joltage_str = ""
    last_chosen_index = -1
    while num_found < 12:
        # search space is after the last chosen but leaving enough room for 12 - num_found - 1 more
        corpus = [int(ch) for ch in bank]
        highest, last_chosen_index = get_max_and_index(corpus, last_chosen_index+1, len(bank) -(12-num_found-1))
        joltage_str += str(highest)
        num_found += 1
    # print(joltage_str)
    return int(joltage_str)


if __name__ == '__main__':
    print(sum(get_joltage_12(bank) for bank in get_banks("input.txt")))

