import math
from collections import defaultdict, deque
from typing import List, Dict, Tuple, Callable, Optional


def load_maze(filename: str):
    maze = []
    with open(filename, 'r') as file:
        for line in file:
            maze.append(line.rstrip('\n'))
    return maze


def in_bounds_match(maze: List[str], x: int, y: int, predicate: Callable[[str], bool]) -> Optional[Tuple[int, int, str]]:
    if x < 0 or y < 0:
        return None
    if y >= len(maze) or x >= len(maze[y]):
        return None
    if predicate(maze[y][x]):
        return x, y, maze[y][x]
    return None


def find_neighbor(maze: List[str], x: int, y: int, predicate: Callable[[str], bool]) -> Optional[Tuple[int, int, str]]:
    vectors = [
        (0, 1),
        (0, -1),
        (-1, 0),
        (-1, 1),
        (-1, -1),
        (1, 0),
        (1, 1),
        (1, -1),
    ]
    matches = [in_bounds_match(maze, x + v[0], y + v[1], predicate) for v in vectors]
    matches = [m for m in matches if m is not None]
    if not matches:
        return None

    if len(matches) > 1:
        raise Exception('huh?')

    return matches[0]


def is_dot(ch: str) -> bool:
    return ch == '.'


def is_upper(ch: str) -> bool:
    return ch.isupper()


def find_portals(maze: List[str]) -> Dict[str, List[Tuple[int, int]]]:
    portals = defaultdict(list)
    for y, row in enumerate(maze):
        for x, ch in enumerate(row):
            if ch.isupper():
                dot_neighbor = find_neighbor(maze, x, y, is_dot)
                if dot_neighbor:
                    _, _, other_char = find_neighbor(maze, x, y, is_upper)
                    portal_name = ''.join(sorted([ch, other_char]))
                    portals[portal_name].append((dot_neighbor[0], dot_neighbor[1]))
    return dict(portals)


def invert(coords_by_portals: Dict[str, List[Tuple[int, int]]]) -> Dict[Tuple[int, int], str]:
    portals_by_coord = {}
    for portal, coords_list in coords_by_portals.items():
        for coord in coords_list:
            portals_by_coord[coord] = portal
    return portals_by_coord


def get_dist_map(
        x: int,
        y: int,
        maze: List[str],
        portals_by_coords: Dict[Tuple[int, int], str],
        coords_by_portals: Dict[str, List[Tuple[int, int]]],
) -> Dict[str, int]:
    dist_map = {}
    visited = set()
    visited.add((x, y))
    queue = deque([(x, y, 0)])

    while queue:
        x, y, distance = queue.pop()
        portal = portals_by_coords.get((x, y))
        if portal and distance > 0 and distance < dist_map.get(portal, math.inf):
            dist_map[portal] = distance
        visited.add((x, y))
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            newx, newy = x + d[0], y + d[1]
            if maze[newy][newx] == '.' and (newx, newy) not in visited:
                queue.appendleft((newx, newy, distance + 1))
        if portal and len(coords_by_portals[portal]) == 2:
            other_coord = [coord for coord in coords_by_portals[portal] if coord != (x, y)][0]
            if other_coord not in visited:
                queue.appendleft((other_coord[0], other_coord[1], distance + 1))
    return dist_map


if __name__ == '__main__':
    maze = load_maze('input.txt')
    coords_by_portal = find_portals(maze)
    portals_by_coords = invert(coords_by_portal)

    # print(coords_by_portal)
    # print(portals_by_coords)

    aa_coord = coords_by_portal['AA'][0]
    print(get_dist_map(aa_coord[0], aa_coord[1], maze, portals_by_coords, coords_by_portal)['ZZ'])

