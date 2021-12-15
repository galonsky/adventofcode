from collections import defaultdict
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


if __name__ == '__main__':
    cavern_map = get_map("input.txt")
    # print(cavern_map)
    print(find_lowest_total_risk(cavern_map))