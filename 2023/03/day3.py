import re


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


def get_sum_of_part_numbers(schematic: list[str]) -> int:
    total = 0
    for y, line in enumerate(schematic):
        matches = NUM_PATTERN.finditer(line)
        for match in matches:
            if is_part_number(match.start(), y, schematic):
                total += int(match.group())
    return total


if __name__ == '__main__':
    schematic = get_schematic("input.txt")
    print(get_sum_of_part_numbers(schematic))