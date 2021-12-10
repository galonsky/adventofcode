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


def floodfill_size(heights: list[str], x: int, y: int) -> int:
    if x < 0 or y < 0 or y >= len(heights) or x >= len(heights[0]):
        return 0

    if heights[y][x] in {"9", "x"}:
        return 0

    line_arr = list(heights[y])
    line_arr[x] = "x"
    heights[y] = "".join(line_arr)

    neighbor_sizes = sum(
        floodfill_size(heights, x + v[0], y + v[1]) for v in VECTORS
    )
    return 1 + neighbor_sizes


def get_basin_score(heights: list[str]) -> int:
    basins = []
    for y, line in enumerate(heights):
        for x, ch in enumerate(line):
            if heights[y][x] not in {"9", "x"}:
                basins.append(floodfill_size(heights, x, y))
    basins.sort(reverse=True)
    return basins[0] * basins[1] * basins[2]


if __name__ == '__main__':
    # print(get_sum_of_risk(get_map("input.txt")))
    print(get_basin_score(get_map("input.txt")))
