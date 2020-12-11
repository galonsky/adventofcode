from typing import Iterable, Set, Dict


def get_adapters(filename: str) -> Iterable[int]:
    with open(filename, 'r') as file:
        for line in file:
            yield int(line.rstrip('\n'))


def part1():
    adapters = list(get_adapters('input.txt'))
    adapters.append(max(adapters) + 3)
    adapters.sort()
    last = 0

    one_diffs = 0
    three_diffs = 0
    for adapter in adapters:
        diff = adapter - last
        if diff == 1:
            one_diffs += 1
        elif diff == 3:
            three_diffs += 1
        else:
            raise Exception('unexpected!')
        last = adapter

    print(one_diffs * three_diffs)


def get_number_of_ways(start_jolt: int, end_jolt: int, adapters: Set[int], cache: Dict[int, int]) -> int:
    if start_jolt == end_jolt:
        return 1

    if start_jolt in cache:
        return cache[start_jolt]

    total = 0
    if start_jolt + 1 in adapters:
        total += get_number_of_ways(start_jolt + 1, end_jolt, adapters, cache)
    if start_jolt + 2 in adapters:
        total += get_number_of_ways(start_jolt + 2, end_jolt, adapters, cache)
    if start_jolt + 3 in adapters:
        total += get_number_of_ways(start_jolt + 3, end_jolt, adapters, cache)
    cache[start_jolt] = total
    return total


def part2():
    adapters = set(get_adapters('input.txt'))
    end_jolt = max(adapters) + 3
    adapters.add(end_jolt)
    cache = {}
    print(get_number_of_ways(0, end_jolt, adapters, cache))


if __name__ == '__main__':
    part2()
