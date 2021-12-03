from collections import defaultdict
from typing import Iterable


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


if __name__ == '__main__':
    print(get_power_consumption(get_input("input.txt")))