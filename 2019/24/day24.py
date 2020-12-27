from typing import List


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


def biodiversity(bug_map: List[List[str]]) -> int:
    return int(
        ''.join([''.join(line) for line in bug_map])[::-1].replace('#', '1').replace('.', '0'),
        base=2,
    )


def part1():
    seen_before = set()
    bug_map = get_map('input.txt')
    serialized = biodiversity(bug_map)
    while serialized not in seen_before:
        seen_before.add(serialized)
        bug_map = iterate_map(bug_map)
        serialized = biodiversity(bug_map)

    return serialized


if __name__ == '__main__':
    print(part1())
