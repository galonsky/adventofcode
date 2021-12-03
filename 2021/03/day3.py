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


def get_life_support_rating(report_nums: Iterable[str]) -> int:
    oxygen_nums = set(report_nums)
    co2_nums = set(oxygen_nums)

    pos = 0
    while True:
        if len(oxygen_nums) == 1 and len(co2_nums) == 1:
            return int(next(iter(oxygen_nums)), 2) * int(next(iter(co2_nums)), 2)
        ox_counts = defaultdict(int)
        co2_counts = defaultdict(int)
        one_nums = set()
        zero_nums = set()
        if len(oxygen_nums) > 1:
            for num in oxygen_nums:
                ch = num[pos]
                ox_counts[ch] += 1
                if ch == "0":
                    zero_nums.add(num)
                else:
                    one_nums.add(num)
            one_most_common = ox_counts.get("1", 0) >= ox_counts.get("0", 0)
            if one_most_common:
                oxygen_nums -= zero_nums
            else:
                oxygen_nums -= one_nums

        if len(co2_nums) > 1:
            for num in co2_nums:
                ch = num[pos]
                co2_counts[ch] += 1
                if ch == "0":
                    zero_nums.add(num)
                else:
                    one_nums.add(num)
            zero_least_common = co2_counts.get("0", 0) <= co2_counts.get("1", 0)
            if zero_least_common:
                co2_nums -= one_nums
            else:
                co2_nums -= zero_nums
        pos += 1



if __name__ == '__main__':
    # print(get_power_consumption(get_input("input.txt")))
    print(get_life_support_rating(get_input("input.txt")))