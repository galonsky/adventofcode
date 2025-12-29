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


def get_num_accessible(roll_map: list[str]) -> int:
    total = 0
    for y, row in enumerate(roll_map):
        for x, ch in enumerate(row):
            if ch != '@':
                continue
            neighbors = get_neighbors(roll_map, x, y)
            roll_neighbors = [n for n in neighbors if n == '@']
            if len(roll_neighbors) < 4:
                total += 1
    return total


if __name__ == '__main__':
    print(get_num_accessible(get_map("input.txt")))
