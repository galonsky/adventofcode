from typing import List


def get_slope(filename: str) -> List[str]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.rstrip())
    return lines


if __name__ == '__main__':
    slope = get_slope('input.txt')
    width = len(slope[0])
    y = 0
    x = 0
    num_trees = 0
    while y < len(slope):
        if slope[y][x % width] == '#':
            num_trees += 1
        y += 1
        x += 3

    print(num_trees)