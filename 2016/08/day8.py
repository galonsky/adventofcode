import re
from typing import List, Iterable

RECT_PATTERN = re.compile(r'rect (\d+)x(\d+)')
ROW_PATTERN = re.compile(r'rotate row y=(\d+) by (\d+)')
COL_PATTERN = re.compile(r'rotate column x=(\d+) by (\d+)')


def get_input(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def rect(screen: List[List[bool]], x: int, y: int):
    for _y in range(y):
        for _x in range(x):
            screen[_y][_x] = True


def rotate_row(screen: List[List[bool]], y: int, b: int):
    screen[y] = screen[y][-b:] + screen[y][:-b]


def rotate_column(screen: List[List[bool]], x: int, b: int):
    original_col = [row[x] for row in screen]
    new_col = original_col[-b:] + original_col[:-b]
    for y in range(len(screen)):
        screen[y][x] = new_col[y]


def part1and2():
    screen = [
        [False] * 50 for _ in range(6)
    ]
    for instruction in get_input('input.txt'):
        if match := RECT_PATTERN.match(instruction):
            x, y = match.groups()
            rect(screen, int(x), int(y))
        elif match := ROW_PATTERN.match(instruction):
            y, b = match.groups()
            rotate_row(screen, int(y), int(b))
        elif match := COL_PATTERN.match(instruction):
            x, b = match.groups()
            rotate_column(screen, int(x), int(b))
        else:
            raise Exception('unexpected!')

    num_on = 0
    for row in screen:
        for light in row:
            if light:
                num_on += 1
    print(num_on)
    print_screen(screen)


def print_screen(screen: List[List[bool]]):
    for row in screen:
        print(''.join(['#' if pixel else ' ' for pixel in row]))


if __name__ == '__main__':
    part1and2()
