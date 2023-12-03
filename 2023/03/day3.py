import re
from collections import defaultdict
from functools import reduce
from itertools import product
from typing import Generator

NUM_PATTERN = re.compile(r'\d+')
SYMBOL_PATTERN = re.compile(r'[^\d0-9.]')
VECTORS = (
    (1, 0),
    (1, 1),
    (0, 1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (-1, 1),
    (-1, -1),
)


class PartNumber:
    def __init__(self, number: int, x: int, y: int):
        self.number = number
        self.coord = f"{x},{y}"

    def __eq__(self, __o):
        return self.coord == __o.coord

    def __hash__(self):
        return hash(self.coord)


def get_schematic(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        return [line.strip() for line in file]


def is_part_number(startx: int, y: int, schematic: list[str]) -> bool:
    x = startx
    while x < len(schematic[0]) and schematic[y][x].isnumeric():
        for v in VECTORS:
            newx = x + v[0]
            newy = y + v[1]
            if newx >= 0 and newy >= 0 and newx < len(schematic[0]) and newy < len(schematic) and SYMBOL_PATTERN.match(schematic[newy][newx]):
                return True
        x += 1
    return False


def get_gear_coords(startx: int, y: int, schematic: list[str]) -> set[str]:
    gears = set()
    x = startx
    while x < len(schematic[0]) and schematic[y][x].isnumeric():
        for v in VECTORS:
            newx = x + v[0]
            newy = y + v[1]
            if 0 <= newx < len(schematic[0]) and 0 <= newy < len(schematic) and schematic[newy][newx] == '*':
                gears.add(f"{newx},{newy}")
        x += 1
    return gears


def get_sum_of_part_numbers(schematic: list[str]) -> int:
    total = 0
    for y, line in enumerate(schematic):
        matches = NUM_PATTERN.finditer(line)
        for match in matches:
            if is_part_number(match.start(), y, schematic):
                total += int(match.group())
    return total


def get_sum_of_gear_ratios(schematic: list[str]) -> int:
    part_numbers_by_gear = defaultdict(set)
    for y, line in enumerate(schematic):
        matches = NUM_PATTERN.finditer(line)
        for match in matches:
            gears = get_gear_coords(match.start(), y, schematic)
            for gear in gears:
                part_numbers_by_gear[gear].add(PartNumber(int(match.group()), match.start(), y))

    total = 0
    for gear, numbers in part_numbers_by_gear.items():
        if len(numbers) != 2:
            continue
        total += reduce(lambda x, y: x*y, (number.number for number in numbers))
    return total


if __name__ == '__main__':
    schematic = get_schematic("input.txt")
    print(get_sum_of_part_numbers(schematic))
    print(get_sum_of_gear_ratios(schematic))