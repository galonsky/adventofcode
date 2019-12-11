import math

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __hash__(self):
        if self.x == 0:
            if self.y < 0:
                return -1
            else:
                return 1
        return (self.y) // (self.x)
    
    def divide(self):
        if self.x == 0:
            if self.y < 0:
                return -math.inf
            else:
                return math.inf
        return (self.y) / (self.x)
    
    def __eq__(self, other):
        signs_are_same = (self.x * other.x >= 0) and (self.y * other.y >= 0)
        return signs_are_same and self.divide() == other.divide()
    
    def __str__(self):
        return '({},{})'.format(self.x, self.y)


def get_input(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines

def get_vector(x, y, vantage_x, vantage_y):
    return Vector(x - vantage_x, y - vantage_y)


def get_num_visible(asteroids, vantage_x, vantage_y):
    visible = 0
    seen_angles = set()
    for y in range(len(asteroids)):
        for x in range(len(asteroids[0])):
            if asteroids[y][x] != '#':
                continue
            if x == vantage_x and y == vantage_y:
                continue

            vector = get_vector(x, y, vantage_x, vantage_y)
            if vector not in seen_angles:
                visible += 1
            seen_angles.add(vector)
    print('{} visible from ({},{})'.format(visible, vantage_x, vantage_y))
    return visible


def find_best_location(filename):
    asteroids = get_input(filename)
    # print(asteroids)
    num_visible_by_coordinate = {}
    for y in range(len(asteroids)):
        for x in range(len(asteroids[0])):
            if asteroids[y][x] != '#':
                continue
            num_visible_by_coordinate[(x, y)] = get_num_visible(asteroids, x, y)
    return max(num_visible_by_coordinate.values())

print(find_best_location('input.txt'))
# vantage_x = 1
# vantage_y = 1
# print(get_vector(1, 0, vantage_x, vantage_y))
# print(get_vector(2, 0, vantage_x, vantage_y))
# print(get_vector(2, 1, vantage_x, vantage_y))
# print(get_vector(2, 2, vantage_x, vantage_y))
# print(get_vector(1, 2, vantage_x, vantage_y))
# print(get_vector(0, 2, vantage_x, vantage_y))
# print(get_vector(0, 1, vantage_x, vantage_y))