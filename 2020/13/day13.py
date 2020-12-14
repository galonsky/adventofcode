from functools import reduce
from itertools import combinations
from math import ceil
from typing import Tuple, List, Dict, Set


def get_input(filename: str) -> Tuple[int, List[int]]:
    with open(filename, 'r') as file:
        contents = file.read()
        lines = contents.split('\n')
        earliest = int(lines[0])
        ids = []
        for id in lines[1].split(','):
            if id == 'x':
                continue
            ids.append(int(id))
        return earliest, ids


def part1():
    earliest, ids = get_input('input.txt')
    next_times = {
        id: ceil(earliest / id) * id for id in ids
    }
    min_id = min(next_times.keys(), key=lambda id: next_times[id])
    return min_id * (next_times[min_id] - earliest)


def part2():
    # offsets_by_id = {
    #     17: 0,
    #     13: 2,
    #     19: 3,
    # }
    # offsets_by_id = {
    #     7: 0,
    #     13: 1,
    #     59: 4,
    #     31: 6,
    #     19: 7
    # }
    # offsets_by_id = {
    #     67: 0,
    #     7: 1,
    #     59: 2,
    #     61: 3,
    # }
    # offsets_by_id = {
    #     67: 0,
    #     7: 2,
    #     59: 3,
    #     61: 4,
    # }
    # offsets_by_id = {
    #     67: 0,
    #     7: 1,
    #     59: 3,
    #     61: 4,
    # }
    # offsets_by_id = {
    #     1789: 0,
    #     37: 1,
    #     47: 2,
    #     1889: 3,
    # }
    offsets_by_id = {
        17: 0,
        37: 11,
        449: 17,
        23: 25,
        13: 30,
        19: 36,
        607: 48,
        41: 58,
        29: 77,
    }

    max_interval = 0
    start_and_interval_by_tuple_by_num_pairs: Dict[int, Dict[Set[int], Tuple[int, int]]] = {}

    for num_pairs in range(1, 10):
        print(f'running for {num_pairs} pairs')
        start_and_interval_by_tuple_by_num_pairs[num_pairs] = {}
        for pairs in combinations(offsets_by_id.items(), num_pairs):
            this_pair_set = frozenset(pair[0] for pair in pairs)
            if (num_pairs - 1) in start_and_interval_by_tuple_by_num_pairs:
                # if we have data on the previous number of pairs, find the one with the highest step/interval is a subset of our current tuple
                previous_pairs = [
                    pair_set for pair_set in start_and_interval_by_tuple_by_num_pairs[num_pairs - 1].keys()
                    if pair_set < this_pair_set
                ]
                best_pair_set = max(previous_pairs, key=lambda ps: start_and_interval_by_tuple_by_num_pairs[num_pairs - 1][ps][1])
                t, step = start_and_interval_by_tuple_by_num_pairs[num_pairs - 1][best_pair_set]
            else:
                pair_with_max = max(pairs, key=lambda pair: pair[0])
                step = pair_with_max[0]
                t = step*3 - pair_with_max[1]  # times 3 since this was going negative for some. assuming none of these end up being in the first 3 steps?
            while True:
                # starting at t (starting point from lesser tuple count)
                # and step (step interval from lesser tuple count)
                # check each value from t in step intervals against all the busses
                if all([
                    (t + offset) % k == 0 for (k, offset) in pairs
                ]):
                    interval = reduce(lambda a, b: a*b, [pair[0] for pair in pairs])
                    # this is the first time we've seen this particular tuple matching.
                    # it seems that it will be repeated every (product of all the divisors) units
                    print(f'Found first match at {t}. Should repeat every {interval}')
                    max_interval = max(max_interval, interval)

                    start_and_interval_by_tuple_by_num_pairs[num_pairs][this_pair_set] = (t, interval)
                    break
                t += step
    print(start_and_interval_by_tuple_by_num_pairs[9])


if __name__ == '__main__':
    part2()
