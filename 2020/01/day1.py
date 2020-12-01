from typing import Iterable


def get_input(filename: str) -> Iterable[int]:
    with open(filename, 'r') as file:
        for line in file:
            yield int(line.rstrip())


def part_1():
    nums_set = set(num for num in get_input('input.txt'))
    for num in nums_set:
        diff = 2020 - num
        if diff in nums_set:
            print(num * diff)
            break


def part_2():
    nums_set = set(num for num in get_input('input.txt'))
    remainder_by_num = {}
    for num in nums_set:
        diff = 2020 - num
        remainder_by_num[num] = diff

    # find 2 nums that add up to diff
    for num in nums_set:
        for remain_num, remain in remainder_by_num.items():
            if remain_num == num:
                continue
            new_remain = remain - num
            if new_remain in nums_set:
                print(new_remain * num * remain_num)
                return



if __name__ == '__main__':
    part_2()
