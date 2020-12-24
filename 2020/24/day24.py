from typing import Iterable, Dict, Tuple, Set

POSSIBLE_DIRECTIONS = {
    'e': (1.0, 0.0),
    'se': (0.5, -1.0),
    'sw': (-0.5, -1.0),
    'w': (-1.0, 0.0),
    'nw': (-0.5, 1.0),
    'ne': (0.5, 1.0),
}


def get_tile_directions(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def get_next_direction(dir_string: str) -> str:
    for direction in POSSIBLE_DIRECTIONS:
        if dir_string.startswith(direction):
            return direction


def get_direction_steps(directions: str) -> Iterable[str]:
    i = 0
    while i < len(directions):
        next_dir = get_next_direction(directions[i:])
        yield next_dir
        i += len(next_dir)


def part1():
    directions = get_tile_directions('input.txt')
    tile_colors = get_tile_colors(directions)

    return len([val for val in tile_colors.values() if val])


def get_neighborhood(coords: Iterable[Tuple[float, float]]) -> Set[Tuple[float, float]]:
    neighborhood = set()
    for coord in coords:
        x, y = coord
        neighborhood.add(coord)
        for dx, dy in POSSIBLE_DIRECTIONS.values():
            neighborhood.add((x + dx, y + dy))
    return neighborhood


def flip_tiles(tile_colors: Dict[Tuple[float, float], bool]) -> Dict[Tuple[float, float], bool]:
    new_tile_colors = dict(tile_colors)
    for coord in get_neighborhood(tile_colors.keys()):
        black = tile_colors.get(coord, False)
        white = not black

        coord_neighborhood = get_neighborhood([coord])
        num_black_neighbors = len(
            [neighbor for neighbor in (coord_neighborhood - {coord}) if tile_colors.get(neighbor, False)]
        )

        if black and (
            num_black_neighbors == 0
            or num_black_neighbors > 2
        ):
            del new_tile_colors[coord]
        elif white and num_black_neighbors == 2:
            new_tile_colors[coord] = True
    return new_tile_colors


def part2():
    directions = get_tile_directions('input.txt')
    tile_colors = get_tile_colors(directions)
    for _ in range(100):
        tile_colors = flip_tiles(tile_colors)

    return len([val for val in tile_colors.values() if val])


def get_tile_colors(directions: Iterable[str]) -> Dict[Tuple[float, float], bool]:
    tile_colors: Dict[Tuple[float, float], bool] = {}  # missing/false means white, true means black
    for direction in directions:
        x, y = 0.0, 0.0
        for step in get_direction_steps(direction):
            dx, dy = POSSIBLE_DIRECTIONS[step]
            x += dx
            y += dy
        tile_colors[(x, y)] = not tile_colors.get((x, y), False)
    return tile_colors


if __name__ == '__main__':
    print(part2())