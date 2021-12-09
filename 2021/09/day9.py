from typing import Iterable

VECTORS = (
    (0, 1),
    (1, 0),
    (-1, 0),
    (0, -1),
)


def get_map(filename: str) -> list[str]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


def get_neighbor_heights(heights: list[str], x: int, y: int) -> Iterable[int]:
    for v in VECTORS:
        newx = x + v[0]
        newy = y + v[1]
        if 0 <= newx < len(heights[0]) and 0 <= newy < len(heights):
            yield int(heights[newy][newx])


def get_sum_of_risk(heights: list[str]) -> int:
    risk = 0
    for y, line in enumerate(heights):
        for x, ch in enumerate(line):
            height = int(ch)
            if height < min(get_neighbor_heights(heights, x, y)):
                risk += height + 1
    return risk


if __name__ == '__main__':
    print(get_sum_of_risk(get_map("input.txt")))
