from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Point:
    x: int
    y: int

    @classmethod
    def from_str(cls, string: str) -> "Point":
        parts = string.split(",")
        return cls(int(parts[0]), int(parts[1]))


def get_lines(filename: str) -> Iterable[tuple[Point, Point]]:
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(" -> ")
            yield Point.from_str(parts[0]), Point.from_str(parts[1])


def is_horiz(p1: Point, p2: Point) -> bool:
    return p1.y == p2.y


def is_vert(p1: Point, p2: Point) -> bool:
    return p1.x == p2.x


def num_points_that_overlap(lines: Iterable[tuple[Point, Point]]) -> int:
    lines = list(lines)
    horiz_lines = [line for line in lines if is_horiz(*line)]
    num_per_point = defaultdict(int)
    for line in horiz_lines:
        y = line[0].y
        x0, x1 = tuple(sorted([line[0].x, line[1].x]))
        for i in range(x0, x1 + 1):
            num_per_point[(i, y)] += 1

    vert_lines = [line for line in lines if is_vert(*line)]
    for line in vert_lines:
        x = line[0].x
        y0, y1 = tuple(sorted([line[0].y, line[1].y]))
        for i in range(y0, y1 + 1):
            num_per_point[(x, i)] += 1

    # print(num_per_point)
    return len([val for val in num_per_point.values() if val >= 2])


if __name__ == '__main__':
    lines = get_lines("input.txt")
    print(num_points_that_overlap(lines))
