from pprint import pp
from typing import Dict, Tuple


def get_map(filename: str) -> Dict[Tuple[int, int, int], str]:
    cube_map: Dict[Tuple[int, int, int], str] = {}
    z = 0
    with open(filename, 'r') as file:
        for y, line in enumerate(file):
            for x, ch in enumerate(line.rstrip('\n')):
                cube_map[(x, y, z)] = ch
    return cube_map


def get_map_4d(filename: str) -> Dict[Tuple[int, int, int, int], str]:
    cube_map: Dict[Tuple[int, int, int, int], str] = {}
    z = 0
    w = 0
    with open(filename, 'r') as file:
        for y, line in enumerate(file):
            for x, ch in enumerate(line.rstrip('\n')):
                cube_map[(x, y, z, w)] = ch
    return cube_map


def num_active_neighbors(cube_map: Dict[Tuple[int, int, int], str], coord: Tuple[int, int, int]) -> int:
    num_active = 0
    x, y, z = coord
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                if dx == 0 and dy == 0 and dz == 0:
                    continue
                if cube_map.get((x + dx, y + dy, z + dz), '.') == '#':
                    num_active += 1
    return num_active


def num_active_neighbors_4d(cube_map: Dict[Tuple[int, int, int, int], str], coord: Tuple[int, int, int, int]) -> int:
    num_active = 0
    x, y, z, w = coord
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            for dz in range(-1, 2):
                for dw in range(-1, 2):
                    if dx == 0 and dy == 0 and dz == 0 and dw == 0:
                        continue
                    if cube_map.get((x + dx, y + dy, z + dz, w + dw), '.') == '#':
                        num_active += 1
    return num_active


def iterate_map(cube_map: Dict[Tuple[int, int, int], str]) -> Dict[Tuple[int, int, int], str]:
    new_map = {}
    x_min, x_max = min(key[0] for key in cube_map), max(key[0] for key in cube_map)
    y_min, y_max = min(key[1] for key in cube_map), max(key[1] for key in cube_map)
    z_min, z_max = min(key[2] for key in cube_map), max(key[2] for key in cube_map)
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                active = cube_map.get((x, y, z), '.') == '#'
                num_neighbors = num_active_neighbors(cube_map, (x, y, z))
                if (
                    active and num_neighbors in (2, 3)
                    or not active and num_neighbors == 3
                ):
                    new_map[(x, y, z)] = '#'
    return new_map


def iterate_map_4d(cube_map: Dict[Tuple[int, int, int, int], str]) -> Dict[Tuple[int, int, int, int], str]:
    new_map = {}
    x_min, x_max = min(key[0] for key in cube_map), max(key[0] for key in cube_map)
    y_min, y_max = min(key[1] for key in cube_map), max(key[1] for key in cube_map)
    z_min, z_max = min(key[2] for key in cube_map), max(key[2] for key in cube_map)
    w_min, w_max = min(key[3] for key in cube_map), max(key[3] for key in cube_map)
    for x in range(x_min - 1, x_max + 2):
        for y in range(y_min - 1, y_max + 2):
            for z in range(z_min - 1, z_max + 2):
                for w in range(w_min - 1, w_max + 2):
                    active = cube_map.get((x, y, z, w), '.') == '#'
                    num_neighbors = num_active_neighbors_4d(cube_map, (x, y, z, w))
                    if (
                        active and num_neighbors in (2, 3)
                        or not active and num_neighbors == 3
                    ):
                        new_map[(x, y, z, w)] = '#'
    return new_map


def part1():
    cube_map = get_map('input.txt')
    for i in range(6):
        cube_map = iterate_map(cube_map)

    return len([val for val in cube_map.values() if val == '#'])


def part2():
    cube_map = get_map_4d('input.txt')
    for i in range(6):
        cube_map = iterate_map_4d(cube_map)

    return len([val for val in cube_map.values() if val == '#'])


if __name__ == '__main__':
    print(part2())
