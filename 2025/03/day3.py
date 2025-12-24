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


if __name__ == '__main__':
    print(sum(get_joltage(bank) for bank in get_banks("input.txt")))

