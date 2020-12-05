from typing import Iterable, List, Optional


def get_seat_id(boarding_pass: str) -> int:
    front_back = boarding_pass[:7].replace('B', '1').replace('F', '0')
    row = int(front_back, base=2)
    left_right = boarding_pass[7:].replace('R', '1').replace('L', '0')
    column = int(left_right, base=2)

    return row * 8 + column


def get_input(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip()


def part1():
    highest = 0
    for passport in get_input('input.txt'):
        highest = max(highest, get_seat_id(passport))
    print(highest)


def part2():
    passports = list(get_input('input.txt'))
    ids = [get_seat_id(passp) for passp in passports]
    ids.sort()
    print(ids)

    last_id = ids[0]
    for i in range(1, len(ids)):
        id = ids[i]
        if id != last_id + 1:
            # means we're the one after our seat
            print(id-1)
            return
        last_id = id


def part2v2():
    """
    Slightly better, N instead of NLOGN
    :return:
    """
    passports = list(get_input('input.txt'))
    all_ids = {get_seat_id(bpass) for bpass in passports}
    first_id = min(all_ids)
    last_id = max(all_ids)

    for i in range(first_id, last_id + 1):
        if i not in all_ids:
            print(i)
            return


if __name__ == '__main__':
    # print(get_seat_id('BFFFBBFRRR'))
    # print(get_seat_id('FFFBBBFRRR'))
    # print(get_seat_id('BBFFBBFRLL'))
    part2v2()

