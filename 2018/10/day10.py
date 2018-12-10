import re
from collections import defaultdict

PATTERN = re.compile(r'position=<\s*(\-*\d+),\s*(\-*\d+)> velocity=<\s*(\-*\d+),\s*(\-*\d+)>')


class Point:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def tick(self):
        self.x += self.vx
        self.y += self.vy

    def clone(self):
        return Point(self.x, self.y, self.vx, self.vy)


def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.rstrip('\n')


def get_bounds(points):
    min_x = min(points, key=lambda p: p.x).x
    max_x = max(points, key=lambda p: p.x).x
    min_y = min(points, key=lambda p: p.y).y
    max_y = max(points, key=lambda p: p.y).y
    return min_x, max_x, min_y, max_y


def get_area(bounds: tuple):
    return (bounds[1] - bounds[0]) * (bounds[3] - bounds[2])


def print_points(points: list, bounds: tuple):
    points_dict = defaultdict(dict)
    for point in points:
        points_dict[point.x][point.y] = point

    for y in range(bounds[2], bounds[3] + 1):
        for x in range(bounds[0], bounds[1] + 1):
            if y in points_dict[x]:
                print('#', end='')
            else:
                print('.', end='')
        print()


def print_iterations(filename):
    points = [
        Point(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))) for m in [
            PATTERN.match(line) for line in get_lines(filename)
        ]
    ]
    current_area = get_area(get_bounds(points))
    i = 0
    while True:
        for point in points:
            point.tick()

        bounds = get_bounds(points)
        area = get_area(bounds)
        if area > current_area:
            bounds = get_bounds(points_copy)
            print_points(points_copy, bounds)
            return i
        current_area = area
        points_copy = [p.clone() for p in points]
        i += 1
        

print(print_iterations('day10_input.txt'))
