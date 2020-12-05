from typing import Iterable


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


if __name__ == '__main__':
    # print(get_seat_id('BFFFBBFRRR'))
    # print(get_seat_id('FFFBBBFRRR'))
    # print(get_seat_id('BBFFBBFRLL'))
    highest = 0
    for passport in get_input('input.txt'):
        highest = max(highest, get_seat_id(passport))
    print(highest)

