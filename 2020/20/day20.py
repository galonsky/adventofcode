from collections import defaultdict
from functools import reduce
from math import sqrt
from operator import mul
from pprint import pp
from typing import Dict, List, Iterable, Tuple


def get_tiles(filename: str) -> Dict[int, List[str]]:
    tiles = {}
    with open(filename, 'r') as file:
        for block in file.read().split('\n\n'):
            parts = block.split(':\n')
            tile_id = int(parts[0][-4:])
            tiles[tile_id] = parts[1].split('\n')
    return tiles


def rotate_entire_tile(tile: List[str], n: int) -> List[str]:
    new_tile = tile
    for _ in range(n):
        new_tile = [
            ''.join([row[col_i] for row in new_tile])
            for col_i in range(len(tile) - 1, -1, -1)
        ]
    return new_tile


def flip_horiz(tile: List[str]) -> List[str]:
    return [
        row[::-1] for row in tile
    ]


def flip_vert(tile: List[str]) -> List[str]:
    return list(reversed(tile))


def all_full_flips(tile: List[str]) -> Iterable[List[str]]:
    yield tile
    horiz = flip_horiz(tile)
    yield horiz
    yield flip_vert(tile)
    yield flip_vert(horiz)


def rotate(edges: List[str], n: int) -> List[str]:
    new_edges = edges
    for _ in range(n):
        new_edges = [
            new_edges[3][::-1],
            new_edges[0],
            new_edges[1][::-1],
            new_edges[2],
        ]
    return new_edges


def get_edges(tile: List[str]) -> List[str]:
    """
    N E S W, left to right and top to bottom
    """
    return [
        tile[0],
        ''.join([line[-1] for line in tile]),
        tile[-1],
        ''.join([line[0] for line in tile]),
    ]


def all_flips(edges: List[str]) -> Iterable[List[str]]:
    yield edges
    horizontal = [
        edges[0][::-1],
        edges[3],
        edges[2][::-1],
        edges[1],
    ]
    yield horizontal
    yield [
        edges[3],
        edges[1][::-1],
        edges[0],
        edges[2][::-1],
    ]
    yield [
        horizontal[3],
        horizontal[1][::-1],
        horizontal[0],
        horizontal[2][::-1],
    ]


def all_permutations(edges: List[str]) -> Iterable[List[str]]:
    for i in range(4):
        rotated = rotate(edges, i)
        yield from all_flips(rotated)


def all_full_permutations(tile: List[str]) -> Iterable[List[str]]:
    for i in range(4):
        rotated = rotate_entire_tile(tile, i)
        yield from all_full_flips(rotated)


def part1():
    tiles = get_tiles('input.txt')
    tile_ids_by_edges = defaultdict(set)
    edges_by_tile_id = defaultdict(set)

    for tile_id, tile in tiles.items():
        for permutation_tile in all_full_permutations(tile):
            for edge in get_edges(permutation_tile):
                tile_ids_by_edges[edge].add(tile_id)
                edges_by_tile_id[tile_id].add(edge)

    all_pairs = set()
    for id_set in tile_ids_by_edges.values():
        if len(id_set) == 2:
            all_pairs.add(frozenset(id_set))

    corner_tiles = set()
    edge_count_by_id = defaultdict(int)
    for pair_set in all_pairs:
        for tile_id in pair_set:
            edge_count_by_id[tile_id] += 1

    for tile_id, count in edge_count_by_id.items():
        if count == 2:
            corner_tiles.add(tile_id)

    return reduce(mul, corner_tiles)


def part2():
    tiles = get_tiles('sample1.txt')
    tile_ids_by_edges = defaultdict(set)
    edges_by_tile_id = defaultdict(set)

    all_tile_ids = set(tiles.keys())

    for tile_id, tile in tiles.items():
        for permutation_tile in all_full_permutations(tile):
            for edge in get_edges(permutation_tile):
                tile_ids_by_edges[edge].add(tile_id)
                edges_by_tile_id[tile_id].add(edge)

    all_pairs = set()
    for edge, id_set in tile_ids_by_edges.items():
        if len(id_set) == 2:
            all_pairs.add(frozenset(id_set))

    corner_tiles = list()
    edge_count_by_id = defaultdict(int)
    for pair_set in all_pairs:
        for tile_id in pair_set:
            edge_count_by_id[tile_id] += 1

    for tile_id, count in edge_count_by_id.items():
        if count == 2:
            corner_tiles.append(tile_id)


    # print(corner_tiles)
    # expected_edges_by_corner = [
    #     {1, 2},
    #     {0, 1},
    #     {1, 2},
    #     {2, 3},
    # ]

    # orient corners
    # then should be able to find tiles on their edges

    top_left_corner = corner_tiles[0]
    # top_left_corner = 1951
    corner_permutation_tile = None
    for permutation_tile in all_full_permutations(tiles[top_left_corner]):
        permutation_edges = get_edges(permutation_tile)
        if all(
            len(tile_ids_by_edges[edge]) == 2
            for i, edge in enumerate(permutation_edges)
            if i in (1, 2)
        ):
            corner_permutation_tile = permutation_tile
            break

    direction_vector_by_permutation_index = [
        (0, -1),
        (1, 0),
        (0, 1),
        (-1, 0),
    ]

    opposite_permutation_index = {
        0: 2,
        1: 3,
        2: 0,
        3: 1,
    }

    puzzle: Dict[Tuple[int, int], Tuple[int, List[str]]] = {
        (0, 0): (top_left_corner, corner_permutation_tile),
    }
    side_len = int(sqrt(len(all_tile_ids)))

    while len(puzzle) < len(all_tile_ids):
        keys_cpy = list(puzzle.keys())
        for x, y in keys_cpy:
            start_tile_id, permutation_tile = puzzle[(x, y)]
            for i, edge in enumerate(get_edges(permutation_tile)):
                dx, dy = direction_vector_by_permutation_index[i]
                adjacent_ids = tile_ids_by_edges[edge]
                if len(adjacent_ids) != 2:
                    continue
                new_x, new_y = x + dx, y + dy
                if (
                    0 <= new_x < side_len
                    and 0 <= new_y < side_len
                    and (new_x, new_y) not in puzzle
                ):
                    new_id = [tile_id for tile_id in adjacent_ids if tile_id != start_tile_id][0]
                    possible_tiles = [
                        perm_tile for perm_tile in all_full_permutations(tiles[new_id])
                        if get_edges(perm_tile)[opposite_permutation_index[i]] == edge
                    ]
                    # if len(possible_permutations) != 1:
                    #     raise Exception
                    new_tile = possible_tiles[0]
                    puzzle[(new_x, new_y)] = (new_id, new_tile)
    for y in range(side_len):
        for x in range(side_len):
            print(puzzle[(x, y)][0], end=' ')
        print()

    for tile_y in range(side_len):
        for row_i in range(len(tiles[top_left_corner])):
            for tile_x in range(side_len):
                print(puzzle[(tile_x, tile_y)][1][row_i], end=' ')
            print()
        print()



if __name__ == '__main__':
    print(part2())
