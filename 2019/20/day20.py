from collections import defaultdict
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


if __name__ == '__main__':
    maze = load_maze('sample1.txt')
    print(find_portals(maze))
