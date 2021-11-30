from collections import deque
from enum import Enum


INPUT = 1352


class LocationType(Enum):
    OPEN = 0
    WALL = 1


def compute_location(x: int, y: int) -> LocationType:
    num = x*x + 3*x + 2*x*y + y + y*y + INPUT
    bin_rep = "{0:b}".format(num)
    num_ones = len([bit for bit in bin_rep if bit == "1"])
    return LocationType.OPEN if num_ones % 2 == 0 else LocationType.WALL


class Map:
    def __init__(self, max_x: int, max_y: int):
        self.max_x = max_x
        self.max_y = max_y
        self.cache: dict[tuple[int, int], LocationType] = {}

    def get(self, x: int, y: int) -> LocationType:
        if x < 0 or x > self.max_x or y < 0 or y > self.max_y:
            return LocationType.WALL

        if (x, y) in self.cache:
            return self.cache[(x, y)]

        location = compute_location(x, y)
        self.cache[(x, y)] = location
        return location


VECTORS = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def find_shortest_path(map: Map, target_x: int, target_y: int) -> int:
    dist: dict[tuple[int, int], int] = {}
    x = 1
    y = 1
    queue = deque()
    queue.append((x, y))
    dist[(x, y)] = 0
    while queue:
        coord = min(queue, key=lambda coord: dist.get(coord, float('inf')))
        x, y = coord
        queue.remove(coord)
        if x == target_x and y == target_y:
            return dist[(x, y)]

        for dx, dy in VECTORS:
            new_x = x + dx
            new_y = y + dy
            visited = (new_x, new_y) in dist
            state = map.get(new_x, new_y)
            if state == LocationType.WALL:
                continue
            new_dist = dist[(x, y)] + 1
            if not visited:
                queue.append((new_x, new_y))
            if new_dist < dist.get((new_x, new_y), float("inf")):
                dist[(new_x, new_y)] = new_dist






def print_map(max_x: int, max_y: int):
    for y in range(max_y + 1):
        line = ""
        for x in range(max_x + 1):
            line += "X" if (x == 31 and y == 39) else "#" if compute_location(x, y) == LocationType.WALL else '.'
        print(line)


if __name__ == "__main__":
    map = Map(40, 40)
    print(find_shortest_path(map, 31, 39))

