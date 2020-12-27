from typing import List, Dict

VECTORS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
]


def get_map(filename: str) -> List[List[str]]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(list(line.rstrip('\n')))
    return lines


def num_adjacent_bugs(bug_map: List[List[str]], x: int, y: int) -> int:
    num_adjacent = 0
    for dx, dy in VECTORS:
        newx = x + dx
        newy = y + dy
        if newx < 0 or newy < 0 or newy >= len(bug_map) or newx >= len(bug_map):
            continue
        if bug_map[newy][newx] == '#':
            num_adjacent += 1
    return num_adjacent

def num_adjacent_bugs_across_levels(bug_map_by_level: Dict[int, List[List[str]]], level: int, x: int, y: int) -> int:
    num_adjacent = 0
    bug_map = bug_map_by_level[level]
    for dx, dy in VECTORS:
        newx = x + dx
        newy = y + dy
        if newx == 2 and newy == 2:
            continue
        if newx < 0 or newy < 0 or newy >= len(bug_map) or newx >= len(bug_map):
            continue
        if bug_map[newy][newx] == '#':
            num_adjacent += 1

    if (level + 1) in bug_map_by_level:
        # looking at adjacent tiles in the inner level (+1)
        if (x, y) == (2, 1):
            # on top
            num_adjacent += bug_map_by_level[level+1][0].count('#')
        elif (x, y) == (3, 2):
            # on right
            num_adjacent += [line[-1] for line in bug_map_by_level[level + 1]].count('#')
        elif (x, y) == (2, 3):
            # on bottom
            num_adjacent += bug_map_by_level[level + 1][-1].count('#')
        elif (x, y) == (1, 2):
            # on left
            num_adjacent += [line[0] for line in bug_map_by_level[level + 1]].count('#')

    if (level - 1) in bug_map_by_level:
        # looking at adjacent tiles in the level containing this one (-1)
        if y == 0:
            # below
            if bug_map_by_level[level - 1][1][2] == '#':
                num_adjacent += 1
        if y == 4:
            # above
            if bug_map_by_level[level - 1][3][2] == '#':
                num_adjacent += 1
        if x == 0:
            # on right
            if bug_map_by_level[level - 1][2][1] == '#':
                num_adjacent += 1
        if x == 4:
            # on left
            if bug_map_by_level[level - 1][2][3] == '#':
                num_adjacent += 1
    return num_adjacent


def iterate_map(bug_map: List[List[str]]) -> List[List[str]]:
    new_map = [
        list(line) for line in bug_map
    ]
    for y, line in enumerate(bug_map):
        for x, ch in enumerate(line):
            if ch == '#':
                if num_adjacent_bugs(bug_map, x, y) != 1:
                    new_map[y][x] = '.'
            elif ch == '.':
                if num_adjacent_bugs(bug_map, x, y) in (1, 2):
                    new_map[y][x] = '#'
    return new_map


def has_any_bugs(bug_map: List[List[str]]) -> bool:
    return any(
        '#' in line for line in bug_map
    )


def iterate_map_across_levels(bug_maps: Dict[int, List[List[str]]]) -> Dict[int, List[List[str]]]:
    new_bug_maps = {}

    min_level = min(bug_maps.keys())
    if has_any_bugs(bug_maps[min_level]):
        bug_maps[min_level - 1] = empty_map()
    max_level = max(bug_maps.keys())
    if has_any_bugs(bug_maps[max_level]):
        bug_maps[max_level + 1] = empty_map()

    middle = 2

    for level in list(bug_maps.keys()):
        bug_map = bug_maps[level]
        new_map = [
            list(line) for line in bug_map
        ]
        for y, line in enumerate(bug_map):
            for x, ch in enumerate(line):
                if x == middle and y == middle:
                    continue

                if ch == '#':
                    if num_adjacent_bugs_across_levels(bug_maps, level, x, y) != 1:
                        new_map[y][x] = '.'
                elif ch == '.':
                    if num_adjacent_bugs_across_levels(bug_maps, level, x, y) in (1, 2):
                        new_map[y][x] = '#'
        new_bug_maps[level] = new_map
    return new_bug_maps


def biodiversity(bug_map: List[List[str]]) -> int:
    return int(
        ''.join([''.join(line) for line in bug_map])[::-1].replace('#', '1').replace('.', '0'),
        base=2,
    )


def empty_map(size: int = 5) -> List[List[str]]:
    return [
        [
            '.' for _ in range(size)
        ] for _ in range(size)
    ]


def part1():
    seen_before = set()
    bug_map = get_map('input.txt')
    serialized = biodiversity(bug_map)
    while serialized not in seen_before:
        seen_before.add(serialized)
        bug_map = iterate_map(bug_map)
        serialized = biodiversity(bug_map)

    return serialized


def part2():
    bug_map = get_map('input.txt')
    map_by_level = {
        0: bug_map,
    }
    for _ in range(200):
        map_by_level = iterate_map_across_levels(map_by_level)

    return sum(
        ''.join([''.join(line) for line in bug_map]).count('#')
        for bug_map in map_by_level.values()
    )


if __name__ == '__main__':
    print(part2())
