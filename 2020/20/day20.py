from collections import defaultdict
from functools import reduce
from operator import mul
from pprint import pp
from typing import Dict, List, Iterable


def get_tiles(filename: str) -> Dict[int, List[str]]:
    tiles = {}
    with open(filename, 'r') as file:
        for block in file.read().split('\n\n'):
            parts = block.split(':\n')
            tile_id = int(parts[0][-4:])
            tiles[tile_id] = get_edges(parts[1].split('\n'))
    return tiles


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


def part1():
    tiles = get_tiles('input.txt')
    tile_ids_by_edges = defaultdict(set)
    edges_by_tile_id = defaultdict(set)

    all_tile_ids = set(tiles.keys())

    for tile_id, edges in tiles.items():
        for permutation_edges in all_permutations(edges):
            for edge in permutation_edges:
                tile_ids_by_edges[edge].add(tile_id)
                edges_by_tile_id[tile_id].add(edge)
    # pp(tile_ids_by_edges)
    # print()
    all_pairs = set()
    for id_set in tile_ids_by_edges.values():
        if len(id_set) == 2:
            all_pairs.add(frozenset(id_set))
    # print(all_pairs)

    corner_tiles = set()
    edge_count_by_id = defaultdict(int)
    for pair_set in all_pairs:
        for tile_id in pair_set:
            edge_count_by_id[tile_id] += 1

    for tile_id, count in edge_count_by_id.items():
        if count == 2:
            corner_tiles.add(tile_id)

    return reduce(mul, corner_tiles)


if __name__ == '__main__':
    print(part1())
