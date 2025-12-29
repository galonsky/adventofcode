from typing import Generator

VECTORS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (1, -1),
    (1, 1),
    (-1, 0),
    (-1, 1),
    (-1, -1)
]


def get_map(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        return list(line.strip() for line in file)


def index(roll_map: list[str], x: int, y: int) -> str:
    if x < 0 or y < 0 or y >= len(roll_map) or x >= len(roll_map[0]):
        return '.'
    return roll_map[y][x]


def get_neighbors(roll_map: list[str], x: int, y: int) -> list[str]:
    return [
        index(roll_map, x+dx, y+dy) for (dx, dy) in VECTORS
    ]


def get_accessible(roll_map: list[str]) -> list[tuple[int, int]]:
    accessible = []
    for y, row in enumerate(roll_map):
        for x, ch in enumerate(row):
            if ch != '@':
                continue
            neighbors = get_neighbors(roll_map, x, y)
            roll_neighbors = [n for n in neighbors if n == '@']
            if len(roll_neighbors) < 4:
                accessible.append((x, y))
    return accessible


def remove_rolls(roll_map: list[str], rolls_to_remove: list[tuple[int, int]]) -> list[str]:
    new_map = list(roll_map)
    for x, y in rolls_to_remove:
        row_as_list = [ch for ch in new_map[y]]
        row_as_list[x] = '.'
        new_map[y] = ''.join(row_as_list)
    return new_map


def count_removed_rolls(roll_map: list[str]) -> int:
    current = roll_map
    removed = 0
    while True:
        accessible = get_accessible(current)
        if not accessible:
            return removed
        removed += len(accessible)
        current = remove_rolls(current, accessible)


if __name__ == '__main__':
    # print(len(get_accessible(get_map("input.txt"))))
    print(count_removed_rolls(get_map("input.txt")))
