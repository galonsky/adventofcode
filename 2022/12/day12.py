import math
from typing import Optional


def get_map(filename: str) -> tuple[list[str], tuple[int, int], tuple[int, int]]:
    rows = []
    start = None
    end = None
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            stripped = line.strip()
            s_index = stripped.find('S')
            if s_index != -1:
                start = (s_index, i)
            e_index = stripped.find('E')
            if e_index != -1:
                end = (e_index, i)
            rows.append(stripped)
        return rows, start, end


VECTORS = (
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
)


def _height(trail_map: list[str], coord: tuple[int, int]) -> int:
    ch = trail_map[coord[1]][coord[0]]
    if ch == "S":
        return ord('a')
    if ch == "E":
        return ord('z')
    return ord(ch)



def find_shortest_path(trail_map: list[str], start: tuple[int, int], end: tuple[int, int], cur_min: Optional[int] = None) -> int:
    dist: dict[tuple[int, int], int | float] = {}
    q = set()
    for y, row in enumerate(trail_map):
        for x, ch in enumerate(row):
            dist[(x, y)] = math.inf
            q.add((x, y))
    dist[start] = 0
    while q:
        u = min(q, key=lambda pt: dist[pt])
        q.remove(u)

        if u == end:
            return dist[u]
        u_height = _height(trail_map, u)

        for vec in VECTORS:
            v = (u[0] + vec[0], u[1] + vec[1])
            if v not in dist or v not in q:
                continue
            v_height = _height(trail_map, v)
            if v_height - u_height > 1:
                continue

            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt

            if cur_min is not None and alt > cur_min:
                q.remove(v)


def find_shortest_paths_reverse(trail_map: list[str], end: tuple[int, int], cur_min: Optional[int] = None) -> dict[tuple[int, int], int | float]:
    """
    same as above, but starts at the "end" and finds all shortest paths from the end
    has to follow hill rules backwards
    """
    dist: dict[tuple[int, int], int | float] = {}
    q = set()
    for y, row in enumerate(trail_map):
        for x, ch in enumerate(row):
            dist[(x, y)] = math.inf
            q.add((x, y))
    dist[end] = 0
    while q:
        u = min(q, key=lambda pt: dist[pt])
        q.remove(u)

        u_height = _height(trail_map, u)

        for vec in VECTORS:
            v = (u[0] + vec[0], u[1] + vec[1])
            if v not in dist or v not in q:
                continue
            v_height = _height(trail_map, v)
            if v_height - u_height < -1:
                continue

            alt = dist[u] + 1
            if alt < dist[v]:
                dist[v] = alt

            if cur_min is not None and alt > cur_min:
                q.remove(v)
    return dist


def find_shortest_from_any_a(trail_map: list[str], end: tuple[int, int]) -> int:
    a_coords = set()
    for y, row in enumerate(trail_map):
        for x, ch in enumerate(row):
            if _height(trail_map, (x, y)) == ord('a'):
                a_coords.add((x, y))

    dist_map = find_shortest_paths_reverse(trail_map, end)
    return min([dist_map[c] for c in dist_map if c in a_coords])


if __name__ == '__main__':
    trail_map, start, end = get_map("input.txt")
    print(find_shortest_path(trail_map, start, end))
    print(find_shortest_from_any_a(trail_map, end))