import re
from dataclasses import dataclass
from typing import Iterable, Optional

SEEDS_PATTERN = re.compile(r'seeds: ([0-9 ]+)')
MAP_TITLE_PATTERN = re.compile(r'(\w+)-to-(\w+) map:')


@dataclass
class Range:
    dest_start: int
    source_start: int
    length: int


@dataclass
class Map:
    source: str
    dest: str
    ranges: list[Range]

    def get_dest_num(self, source_num: int) -> int:
        for r in self.ranges:
            if r.source_start <= source_num < (r.source_start + r.length):
                return r.dest_start + (source_num - r.source_start)
        return source_num

    def translate_source_ranges_to_dest_ranges(self, source_ranges: Iterable[tuple[int, int]]) -> Iterable[tuple[int, int]]:
        for source_range in source_ranges:



def get_input(filename: str) -> tuple[list[int], list[Map]]:
    with open(filename, 'r') as file:
        maps = []
        line_iter = iter(file)
        line = next(line_iter).strip()
        seeds = [int(seed) for seed in SEEDS_PATTERN.match(line).group(1).split()]
        next(line_iter)
        while line_iter:
            line = next(line_iter)
            match = MAP_TITLE_PATTERN.match(line)
            source, dest = match.group(1), match.group(2)
            ranges = []
            try:
                while line := next(line_iter).strip():
                    dest_start, source_start, length = tuple(int(num) for num in line.split())
                    ranges.append(Range(dest_start=dest_start, source_start=source_start, length=length))
            except StopIteration:
                maps.append(Map(source=source, dest=dest, ranges=ranges))
                break
            maps.append(Map(source=source, dest=dest, ranges=ranges))
        return seeds, maps


def seed_to_location(seed: int, maps: Iterable[Map]) -> int:
    source = "seed"
    map_by_source = {m.source: m for m in maps}
    dest = None
    source_num = seed
    dest_num = -1
    while dest != "location":
        map = map_by_source[source]
        dest_num = map.get_dest_num(source_num)
        dest = map.dest
        source_num = dest_num
        source = dest
    return dest_num


def get_lowest_location(seeds: Iterable[int], maps: Iterable[Map]) -> int:
    return min((seed_to_location(seed, maps) for seed in seeds))


def find_overlapping_range(range1: tuple[int, int], range2: tuple[int, int]) -> Optional[tuple[int, int]]:
    one_first = range1[0] <= range2[0]
    if one_first:
        if sum(*range1) < range2[0]:
            return None



def get_seed_ranges(seeds: Iterable[int]) -> Iterable[tuple[int, int]]:
    seed_iter = iter(seeds)
    while True:
        try:
            yield next(seed_iter), next(seed_iter)
        except StopIteration:
            return


def find_min_loc_for_seed_range(seed_range: tuple[int, int], maps: Iterable[Map]) -> int:
    source = "seed"
    map_by_source = {m.source: m for m in maps}
    dest = None
    while dest != "location":
        map = map_by_source[source]
        dest_num = map.get_dest_num(source_num)
        dest = map.dest
        source_num = dest_num
        source = dest
    return dest_num


def get_lowest_location_ranges(seeds: Iterable[int], maps: Iterable[Map]) -> int:
    seed_ranges = get_seed_ranges(seeds)
    return min(find_min_loc_for_seed_range(seed_range) for seed_range in seed_ranges)


if __name__ == '__main__':
    seeds, maps = get_input("input.txt")
    print(get_lowest_location(seeds, maps))