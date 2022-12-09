from typing import Iterable


def get_map(filename: str) -> list[list[int]]:
    rows = []
    with open(filename, 'r') as file:
        for line in file:
            row = [int(ch) for ch in line.strip()]
            rows.append(row)
    return rows


def is_visible_from_one_edge(tree_map: list[list[int]], x: int, y: int) -> bool:
    max_y = len(tree_map) - 1
    max_x = len(tree_map[0]) - 1
    height = tree_map[y][x]

    if max(tree_map[y][newx] for newx in range(x + 1, max_x + 1)) < height:
        return True
    if max(tree_map[newy][x] for newy in range(y + 1, max_y + 1)) < height:
        return True
    if max(tree_map[y][newx] for newx in range(x - 1, -1, -1)) < height:
        return True
    if max(tree_map[newy][x] for newy in range(y - 1, -1, -1)) < height:
        return True
    return False


def get_viewing_distance(height: int, trees: Iterable[int]) -> int:
    distance = 0
    for tree in trees:
        distance += 1
        if tree >= height:
            return distance

    return distance


def get_scenic_score(tree_map: list[list[int]], x: int, y: int) -> int:
    max_y = len(tree_map) - 1
    max_x = len(tree_map[0]) - 1
    height = tree_map[y][x]
    scenic_score = 1

    scenic_score *= get_viewing_distance(height, (tree_map[y][newx] for newx in range(x + 1, max_x + 1)))
    scenic_score *= get_viewing_distance(height, (tree_map[newy][x] for newy in range(y + 1, max_y + 1)))
    scenic_score *= get_viewing_distance(height, (tree_map[y][newx] for newx in range(x - 1, -1, -1)))
    scenic_score *= get_viewing_distance(height, (tree_map[newy][x] for newy in range(y - 1, -1, -1)))

    return scenic_score


def get_num_trees_visible(tree_map: list[list[int]]) -> int:
    num_visible = 0
    max_y = len(tree_map) - 1
    max_x = len(tree_map[0]) - 1
    for y, row in enumerate(tree_map):
        for x, height in enumerate(row):
            if y == max_y or x == max_x or y == 0 or x == 0:
                num_visible += 1
            elif is_visible_from_one_edge(tree_map, x, y):
                num_visible += 1
    return num_visible


def get_max_scenic_score(tree_map: list[list[int]]) -> int:
    return max(get_scenic_score(tree_map, x, y) for y, row in enumerate(tree_map) for x, _ in enumerate(row))


if __name__ == '__main__':
    tree_map = get_map("input.txt")
    print(get_max_scenic_score(tree_map))

