from _operator import mul
from collections import defaultdict
from functools import reduce
from typing import Iterable, Set, Protocol


def get_input(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


def get_power_consumption(report_nums: Iterable[str]) -> int:
    counts_by_position: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for bin_num in report_nums:
        for i, ch in enumerate(bin_num):
            counts_by_position[i][ch] += 1

    print(counts_by_position)

    gamma_bin = ""
    epsilon_bin = ""
    for pos, counts in counts_by_position.items():
        one_more_frequent = counts.get("1", 0) > counts.get("0", 0)

        if one_more_frequent:
            print(f"In position {pos}, 1 is more frequent")
            gamma_bin += "1"
            epsilon_bin += "0"
        else:
            print(f"In position {pos}, 0 is more frequent")
            gamma_bin += "0"
            epsilon_bin += "1"


    gamma_rate = int(gamma_bin, 2)
    epsilon_rate = int(epsilon_bin, 2)
    print(gamma_rate, epsilon_rate)
    return gamma_rate * epsilon_rate


class ShouldRemoveZeroes(Protocol):
    def __call__(self, num_ones: int, num_zeroes: int) -> bool:
        ...


def whiddle_down_numbers(numbers: Set[str], pos: int, predicate: ShouldRemoveZeroes) -> None:
    zero_nums = set()
    one_nums = set()
    counts = defaultdict(int)
    for num in numbers:
        ch = num[pos]
        counts[ch] += 1
        if ch == "0":
            zero_nums.add(num)
        else:
            one_nums.add(num)
    num_ones = counts.get("1", 0)
    num_zeroes = counts.get("0", 0)
    should_remove_zeroes = predicate(num_ones, num_zeroes)
    if should_remove_zeroes:
        numbers -= zero_nums
    else:
        numbers -= one_nums


def get_life_support_rating(report_nums: Set[str]) -> int:
    configs: list[tuple[set[str], ShouldRemoveZeroes]] = [
        (set(report_nums), lambda ones, zeroes: ones >= zeroes),
        (set(report_nums), lambda ones, zeroes: zeroes > ones),
    ]

    pos = 0
    while True:
        if all(len(config[0]) == 1 for config in configs):
            return reduce(mul, map(lambda config: int(next(iter(config[0])), 2), configs))

        for config in configs:
            if len(config[0]) > 1:
                whiddle_down_numbers(config[0], pos, config[1])
        pos += 1


if __name__ == '__main__':
    # print(get_power_consumption(get_input("input.txt")))
    print(get_life_support_rating(set(get_input("input.txt"))))
