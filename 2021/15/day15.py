from queue import PriorityQueue
from typing import Iterable


def get_map(filename: str) -> list[list[int]]:
    rows = []
    with open(filename, 'r') as file:
        for line in file:
            rows.append([int(ch) for ch in line.strip()])
    return rows


def find_lowest_total_risk(cavern_map: list[list[int]]) -> int:
    dest_y = len(cavern_map) - 1
    dest_x = len(cavern_map[dest_y]) - 1

    dist = {}
    prev = {}

    q = PriorityQueue()

    for y, row in enumerate(cavern_map):
        for x, risk in enumerate(row):
            dist[(x, y)] = float("inf")
            q.put((0, (x, y)))

    dist[(0, 0)] = 0
    while q:
        p, u = q.get()
        if p != dist[u]:
            continue

        def neighbors() -> Iterable[tuple[int, int]]:
            for vec in (
                (0, 1),
                (1, 0),
                (-1, 0),
                (0, -1),
            ):
                newx = u[0] + vec[0]
                newy = u[1] + vec[1]
                if 0 <= newx <= dest_x and 0 <= newy <= dest_y:
                    yield newx, newy


        if u == (dest_x, dest_y):
            return dist[(dest_x, dest_y)]

        for v in neighbors():
            alt = dist[u] + cavern_map[v[1]][v[0]]
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                q.put((alt, v))

    return dist[(dest_x, dest_y)]


def get_5_by_5_risk(cavern_map: list[list[int]], x: int, y: int) -> int:
    x_region = x // len(cavern_map)
    y_region = y // len(cavern_map)
    region_addend = x_region + y_region

    original_x = x % len(cavern_map)
    original_y = y % len(cavern_map)

    new_risk = (cavern_map[original_y][original_x] + region_addend)
    if new_risk > 9:
        return new_risk % 9
    return new_risk


def print_5_by_5(cavern_map: list[list[int]]):
    for y in range(5 * len(cavern_map)):
        line = ""
        for x in range(5 * len(cavern_map)):
            line += str(get_5_by_5_risk(cavern_map, x, y))
        print(line)


def find_lowest_total_risk_5_by_5(cavern_map: list[list[int]]) -> int:
    dest_y = 5 * len(cavern_map) - 1
    dest_x = 5 * len(cavern_map) - 1

    dist = {}
    prev = {}

    q = PriorityQueue()

    for y in range(5 * len(cavern_map)):
        for x in range(5 * len(cavern_map)):
            dist[(x, y)] = float("inf")
            q.put((0, (x, y)))

    dist[(0, 0)] = 0
    while q:
        p, u = q.get()
        if p != dist[u]:
            continue

        def neighbors() -> Iterable[tuple[int, int]]:
            for vec in (
                (0, 1),
                (1, 0),
                (-1, 0),
                (0, -1),
            ):
                newx = u[0] + vec[0]
                newy = u[1] + vec[1]
                if 0 <= newx <= dest_x and 0 <= newy <= dest_y:
                    yield newx, newy


        if u == (dest_x, dest_y):
            return dist[(dest_x, dest_y)]

        for v in neighbors():
            alt = dist[u] + get_5_by_5_risk(cavern_map, v[0], v[1])
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                q.put((alt, v))

    return dist[(dest_x, dest_y)]


if __name__ == '__main__':
    cavern_map = get_map("input.txt")
    print_5_by_5(cavern_map)
    # print(cavern_map)
    print(find_lowest_total_risk_5_by_5(cavern_map))