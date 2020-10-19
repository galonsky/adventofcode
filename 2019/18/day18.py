import math
from dataclasses import dataclass
from typing import List, Tuple, Set, Dict
from collections import deque


class Node:
    def __init__(self, id: str, x: int, y: int, keys: Set[str] = None, distance: int = 0):
        self.id = id
        self.x = x
        self.y = y
        if not keys:
            keys = set()
        self.keys = keys
        self.children = {}
        self.distance = distance

    def add_child(self, node, distance):
        self.children[node] = distance

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __repr__(self):
        return f"{self.id} @ ({self.x}, {self.y})"



def get_input(filename: str) -> List[str]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


def find_char(map: List[str], char: str) -> Tuple[int, int]:
    for y, line in enumerate(map):
        for x, ch in enumerate(line):
            if ch == char:
                return x, y
    raise Exception


def find_keys(
        x: int, y: int, map: List[str], have_keys: Set[str], distance: int, visited: Set[Tuple[int, int]]
) -> List[Tuple[str, int, int, int]]:
    if (x, y) in visited:
        return []
    visited.add((x, y))
    if y < 0 or y >= len(map) or x < 0 or x >= len(map[0]):
        return []
    if map[y][x] == '#':
        return []

    found = []
    char = map[y][x]
    if char.islower() and char not in have_keys:
        found.append((char, distance, x, y))
    elif char.isupper():
        if char.lower() not in have_keys:
            return []

    return (
        found
        + find_keys(x-1, y, map, have_keys, distance + 1, visited)
        + find_keys(x + 1, y, map, have_keys, distance + 1, visited)
        + find_keys(x, y-1, map, have_keys, distance + 1, visited)
        + find_keys(x, y+1, map, have_keys, distance + 1, visited)
    )


def print_graph(root: Node):
    newline = Node('\n', 0, 0)
    queue = deque([(root, 0), (newline, 0)])
    while queue:
        node, distance = queue.popleft()
        if node == newline:
            print()
            if queue:
                queue.append((newline, 0))
        else:
            print(f"{node} - {distance}", end=' || ')
            for child, distance in node.children.items():
                queue.append((child, distance))


def generate_graph(map: List[str]):
    start_x, start_y = find_char(map, '@')
    # print(start_x, start_y)
    nodes_created = 0

    min_distance_by_keys: Dict[Tuple[str, ...], int] = {}

    min_distance = math.inf

    root = Node(id="root", x=start_x, y=start_y)
    queue = deque([root])
    while queue:
        current = queue.popleft()
        found_keys = find_keys(current.x, current.y, map, current.keys, 0, set())
        # print(found_keys)
        if not found_keys:
            # print(f"last! {current} {current.distance}")
            if current.distance < min_distance:
                min_distance = current.distance
        for (key, distance, x, y) in found_keys:
            new_keys = set(current.keys)
            new_keys.add(key)
            new_node = Node(key, x, y, new_keys, distance=current.distance + distance)
            current.add_child(new_node, distance)
            queue.append(new_node)
            # nodes_created += 1
            # print(nodes_created)

    # print_graph(root)
    return min_distance






def run(filename: str):
    return generate_graph(get_input(filename))


if __name__ == "__main__":
    assert run('sample1.txt') == 8
    assert run('sample2.txt') == 86
    assert run('sample3.txt') == 132
    # assert run('sample4.txt') == 136
    # assert run('sample5.txt') == 81
