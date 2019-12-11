import math
import heapq
from collections import defaultdict

class Vector:
    def __init__(self, x, y, vantage_x, vantage_y):
        self.x = x - vantage_x
        self.y = y - vantage_y
        self.x_coord = x
        self.y_coord = y
    
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
    
    def get_angle_from_top(self):
        # add pi/2 so it starts at the top of the y axis
        angle = math.atan2(self.y, self.x)+math.pi/2
        if angle < 0:
            # this makes it so 0 is the top and goes clockwise to 2pi back to the top
            angle += math.pi*2
        return angle
    
    def magnitude(self):
        return math.hypot(self.x, self.y)
    
    def __eq__(self, other):
        signs_are_same = (self.x * other.x >= 0) and (self.y * other.y >= 0)
        return signs_are_same and self.divide() == other.divide()
    
    def __repr__(self):
        return '({},{}) @ {}'.format(self.x_coord, self.y_coord, self.get_angle_from_top())


def get_input(filename):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            lines.append(line.strip())
    return lines

def get_vector(x, y, vantage_x, vantage_y):
    v = Vector(x, y,vantage_x, vantage_y)
    return v


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

def get_vectors(asteroids, vantage_x, vantage_y):
    vectors = defaultdict(list)
    for y in range(len(asteroids)):
        for x in range(len(asteroids[0])):
            if asteroids[y][x] != '#':
                continue
            if x == vantage_x and y == vantage_y:
                continue

            vector = get_vector(x, y, vantage_x, vantage_y)
            heapq.heappush(vectors[vector], (vector.magnitude(), vector))

    return vectors

def iterate_laser(filename, vantage_x, vantage_y):
    asteroids = get_input(filename)
    vectors = get_vectors(asteroids, vantage_x, vantage_y)
    print(vectors)
    sorted_vectors = sorted([v for v in vectors.keys() if vectors[v]], key=lambda vector: vector.get_angle_from_top())
    zap_num = 1
    while sorted_vectors:
        for vector in sorted_vectors:
            if not vectors[vector]:
                continue
            _, nearest_vector = heapq.heappop(vectors[vector])
            print('zap {}: ({}, {})'.format(zap_num, nearest_vector.x_coord, nearest_vector.y_coord))
            zap_num += 1
        # just to remove ones with empty lists
        sorted_vectors = sorted([v for v in vectors.keys() if vectors[v]], key=lambda vector: vector.get_angle_from_top())


def find_best_location(filename):
    asteroids = get_input(filename)
    # print(asteroids)
    num_visible_by_coordinate = {}
    for y in range(len(asteroids)):
        for x in range(len(asteroids[0])):
            if asteroids[y][x] != '#':
                continue
            num_visible_by_coordinate[(x, y)] = get_num_visible(asteroids, x, y)
    max_coord = max(num_visible_by_coordinate.keys(), key=lambda coord: num_visible_by_coordinate[coord])
    return max_coord, num_visible_by_coordinate[max_coord]

# print(find_best_location('input.txt'))
# vantage_x = 1
# vantage_y = 1
# print('top', get_vector(1, 0, vantage_x, vantage_y))
# print('top right', get_vector(2, 0, vantage_x, vantage_y))
# print('right', get_vector(2, 1, vantage_x, vantage_y))
# print('bottom right', get_vector(2, 2, vantage_x, vantage_y))
# print('bottom', get_vector(1, 2, vantage_x, vantage_y))
# print('bottom left', get_vector(0, 2, vantage_x, vantage_y))
# print('left', get_vector(0, 1, vantage_x, vantage_y))
# print('top left', get_vector(0, 0, vantage_x, vantage_y))

# get_vector(0, -1000, 0, 0)

# coordinate is 26, 36

iterate_laser('input.txt', 26, 36)
# print(find_best_location('sample5.txt'))