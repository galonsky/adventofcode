from heapq import nlargest
from typing import Generator


def iterate_elves(filename: str) -> Generator[list[int], None, None]:
    with open(filename, "r") as file:
        current_elf = []
        for line in file:
            if not line.strip():
                yield current_elf
                current_elf = []
            else:
                current_elf.append(int(line.strip()))
        if current_elf:
            yield current_elf


def find_highest_calorie_elf(filename: str) -> int:
    elves = iterate_elves(filename)
    return max((sum(c_list) for c_list in elves))


def find_3_largest(filename: str) -> int:
    elves = iterate_elves(filename)
    return sum(nlargest(3, (sum(c_list) for c_list in elves)))


if __name__ == '__main__':
    # print(find_highest_calorie_elf("input.txt"))
    print(find_3_largest("input.txt"))