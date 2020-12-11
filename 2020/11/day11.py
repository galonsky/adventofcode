from typing import List, Optional


def get_map(filename: str) -> List[str]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))
    return lines


def access_char(map: List[str], x: int, y: int) -> Optional[str]:
    if y < 0 or y >= len(map):
        return None
    if x < 0 or x >= len(map[y]):
        return None
    return map[y][x]


def get_adjacent_occupied(map: List[str], x: int, y: int) -> int:
    chars = [
        access_char(map, x + 1, y),
        access_char(map, x + 1, y + 1),
        access_char(map, x + 1, y - 1),
        access_char(map, x, y + 1),
        access_char(map, x, y - 1),
        access_char(map, x - 1, y),
        access_char(map, x - 1, y + 1),
        access_char(map, x - 1, y - 1),
    ]
    return len([ch for ch in chars if ch == '#'])


def iterate_map(map: List[str]) -> List[str]:
    new_map = list(map)
    for y, line in enumerate(map):
        new_line = ""
        for x, ch in enumerate(line):
            if ch == '.':
                new_line += '.'
            else:
                num_occupied = get_adjacent_occupied(map, x, y)
                if ch == 'L' and num_occupied == 0:
                    new_line += '#'
                elif ch == '#' and num_occupied >= 4:
                    new_line += 'L'
                else:
                    new_line += ch
        new_map[y] = new_line
    return new_map


def print_map(map: List[str]):
    for line in map:
        print(line)


def part1():
    last_map = get_map('input.txt')
    while True:
        new_map = iterate_map(last_map)
        print_map(new_map)
        print()
        if new_map == last_map:
            return sum((line.count('#') for line in new_map))
        last_map = new_map

if __name__ == '__main__':
    print(part1())