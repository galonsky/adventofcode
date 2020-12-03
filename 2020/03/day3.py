from typing import List


def get_slope(filename: str) -> List[str]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.rstrip())
    return lines


def get_trees_for_pattern(slope: List[str], y_diff: int, x_diff: int) -> int:
    width = len(slope[0])
    y = 0
    x = 0
    num_trees = 0
    while y < len(slope):
        if slope[y][x % width] == '#':
            num_trees += 1
        y += y_diff
        x += x_diff
    return num_trees


if __name__ == '__main__':
    slope = get_slope('input.txt')

    # print(get_trees_for_pattern(slope, 1, 3))

    print(
        get_trees_for_pattern(slope, 1, 1)
        * get_trees_for_pattern(slope, 1, 3)
        * get_trees_for_pattern(slope, 1, 5)
        * get_trees_for_pattern(slope, 1, 7)
        * get_trees_for_pattern(slope, 2, 1)
    )