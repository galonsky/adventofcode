from collections import defaultdict

def load_map(filename):
    forest_map = defaultdict(dict)
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.rstrip('\n')):
                forest_map[x][y] = c
    return forest_map

def get_adjacent(forest_map, x, y):
    x_max = len(forest_map) - 1
    y_max = len(forest_map[0]) - 1
    if x - 1 >= 0:
        yield forest_map[x - 1][y]
        if y - 1 >= 0:
            yield forest_map[x - 1][y - 1]
        if y + 1 <= y_max:
            yield forest_map[x - 1][y + 1]
    if x + 1 <= x_max:
        yield forest_map[x+1][y]
        if y - 1 >= 0:
            yield forest_map[x+1][y-1]
        if y + 1 <= y_max:
            yield forest_map[x+1][y+1]
    if y - 1 >= 0:
        yield forest_map[x][y-1]
    if y + 1 <= y_max:
        yield forest_map[x][y+1]


def count(acres, char):
    num = 0
    for c in acres:
        if c == char:
            num += 1
    return num

def all_chars(forest_map):
    for y_map in forest_map.values():
        yield from y_map.values()


def print_map(forest_map):
    x_max = len(forest_map) - 1
    y_max = len(forest_map[0]) - 1
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            print(forest_map[x][y], end='')
        print()
    print()


def iterate(forest_map) -> dict:
    new_map = defaultdict(dict)
    for x, y_map in forest_map.items():
        for y, c in y_map.items():
            adjacent = list(get_adjacent(forest_map, x, y))
            num_trees = count(adjacent, '|')
            num_lumber = count(adjacent, '#')
            if c == '.':
                if num_trees >= 3:
                    new_map[x][y] = '|'
                else:
                    new_map[x][y] = '.'
            elif c == '|':
                if num_lumber >= 3:
                    new_map[x][y] = '#'
                else:
                    new_map[x][y] = '|'
            elif c == '#':
                if num_lumber >= 1 and num_trees >= 1:
                    new_map[x][y] = '#'
                else:
                    new_map[x][y] = '.'
    return new_map

def run_iteration(filename, iterations):
    forest_map = load_map(filename)
    for i in range(iterations):
        print_map(forest_map)
        forest_map = iterate(forest_map)
    print_map(forest_map)

    all_acres = list(all_chars(forest_map))
    num_trees = count(all_acres, '|')
    num_lumber = count(all_acres, '#')
    return num_trees * num_lumber


print(run_iteration('day18_input.txt', 1000000000))
