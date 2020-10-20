import math
from typing import List, Tuple, Set, Dict
from collections import deque


def get_input(filename: str) -> List[str]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines


# some help from https://repl.it/@joningram/AOC-2019 here
def get_dist_map(x: int, y: int, map: List[str]) -> Dict[str, Tuple[int, str]]:
    dist_map = {}
    visited = set()
    visited.add((x, y))
    queue = deque([(x, y, "", 0)])

    while queue:
        x, y, route, distance = queue.pop()
        ch = map[y][x]
        if ch not in ".@1234#" and distance > 0:
            dist_map[ch] = (distance, route)
            route += ch
        visited.add((x, y))
        for d in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            newx, newy = x + d[0], y + d[1]
            if map[newy][newx] != '#' and (newx, newy) not in visited:
                queue.appendleft((newx, newy, route, distance + 1))
    return dist_map


def precalc_distances(map: List[str]) -> Dict[str, Dict[str, Tuple[int, str]]]:
    distance_maps = {}
    for y, line in enumerate(map):
        for x, ch in enumerate(line):
            if ch.islower() or ch in '@1234':
                dist_map = get_dist_map(x, y, map)
                distance_maps[ch] = dist_map
    return distance_maps


# def print_graph(root: Node):
#     newline = Node('\n', 0, 0)
#     queue = deque([(root, 0), (newline, 0)])
#     while queue:
#         node, distance = queue.popleft()
#         if node == newline:
#             print()
#             if queue:
#                 queue.append((newline, 0))
#         else:
#             print(f"{node} - {distance}", end=' || ')
#             for child, distance in node.children.items():
#                 queue.append((child, distance))


# big help from https://old.reddit.com/r/adventofcode/comments/ec8090/2019_day_18_solutions/fbd8y0b/
def distance_to_get_keys(cur: str, distance_maps: Dict[str, Dict[str, Tuple[int, str]]], keys: Set[str], cache: Dict[Tuple[str, int, int], int]) -> int:
    if not keys:
        return 0

    cache_key = (''.join(sorted(list(keys))), cur)
    if cache_key in cache:
        return cache[cache_key]

    result = math.inf
    current_keys = distance_maps.keys() - keys
    reachable_keys = {
        k for k in keys
        if all((c in current_keys or c.lower() in current_keys for c in list(distance_maps[cur][k][1])))
    }
    for key in reachable_keys:
        distance = distance_maps[cur][key][0]
        new_distance = distance + distance_to_get_keys(key, distance_maps, keys - {key}, cache)
        result = min(result, new_distance)

    cache[cache_key] = result
    return result


ROBOTS = ['1', '2', '3', '4']


def distance_to_get_keys2(robot: str, rob_to_key: Dict[str, str], distance_maps: Dict[str, Dict[str, Tuple[int, str]]], keys: Set[str], cache: Dict[Tuple[str, int, int], int]) -> int:
    if not keys:
        return 0

    cur = rob_to_key[robot]

    cache_key = (''.join(sorted(list(keys))), cur, tuple(sorted(rob_to_key.items())))
    if cache_key in cache:
        return cache[cache_key]

    result = math.inf
    best_rob_to_key = None
    current_keys = distance_maps.keys() - keys
    for r in ROBOTS:
        robloc = rob_to_key[r]
        reachable_keys = {
            k for k in keys
            if distance_maps.get(robloc, {}).get(k) and all((c in current_keys or c.lower() in current_keys for c in list(distance_maps[robloc][k][1])))
        }
        for key in sorted(reachable_keys):
            distance = distance_maps[robloc][key][0]
            new_rob_to_key = dict(rob_to_key)
            new_rob_to_key[r] = key
            # print(f"Robot {r} took {key}")
            new_distance = distance + distance_to_get_keys2(r, new_rob_to_key, distance_maps, keys - {key}, cache)
            if new_distance < result:
                result = new_distance
                best_rob_to_key = new_rob_to_key


    rob_to_key.update(best_rob_to_key)
    cache[cache_key] = result
    return result


def get_all_keys(map: List[str]) -> Set[str]:
    all_keys = set()
    for line in map:
        for ch in line:
            if ch.islower():
                all_keys.add(ch)
    return all_keys


def find_char(map: List[str], char: str) -> Tuple[int, int]:
    for y, line in enumerate(map):
        for x, ch in enumerate(line):
            if ch == char:
                return x, y
    raise Exception


def edit_map(map: List[str], x, y, ch):
    row = map[y]
    chars = list(row)
    chars[x] = ch
    map[y] = ''.join(chars)



def modify_map_for_part2(map: List[str]):
    startx, starty = find_char(map, '@')
    newmap = list(map)
    edit_map(newmap, startx, starty, '#')
    edit_map(newmap, startx+1, starty, '#')
    edit_map(newmap, startx, starty+1, '#')
    edit_map(newmap, startx-1, starty, '#')
    edit_map(newmap, startx, starty-1, '#')
    edit_map(newmap, startx + 1, starty+1, '1')
    edit_map(newmap, startx+1, starty - 1, '2')
    edit_map(newmap, startx - 1, starty-1, '3')
    edit_map(newmap, startx-1, starty + 1, '4')
    return newmap


def run(filename: str):
    map = get_input(filename)
    all_keys = get_all_keys(map)
    distance_maps = precalc_distances(map)

    return distance_to_get_keys("@", distance_maps, all_keys, {})


def run_part_2(filename: str):
    map = get_input(filename)
    newmap = modify_map_for_part2(map)
    all_keys = get_all_keys(map)
    # for line in newmap:
    #     print(line)
    distance_maps = precalc_distances(newmap)
    # print(distance_maps)
    rob_to_key = {
        r: r for r in ROBOTS
    }
    return distance_to_get_keys2("1", rob_to_key, distance_maps, all_keys, {})


if __name__ == "__main__":
    # run('sample1.txt')
    # assert run('sample1.txt') == 8
    # assert run('sample2.txt') == 86
    # assert run('sample3.txt') == 132
    # assert run('sample4.txt') == 136
    # assert run('sample5.txt') == 81
    # assert run("input.txt") == 5262

    # print(run_part_2("sample9.txt"))

    # assert run_part_2("sample6.txt") == 8
    # assert run_part_2("sample7.txt") == 24
    # assert run_part_2("sample8.txt") == 32
    # assert run_part_2("sample9.txt") == 72
    print(run_part_2("input.txt"))
