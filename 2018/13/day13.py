from itertools import cycle
from collections import defaultdict

CLOCKWISE_DIRECTIONS = ['up', 'right', 'down', 'left']

class Cart:
    def __init__(self, x, y, direction_index):
        self.x = x
        self.y = y
        self.direction_index = direction_index
        self.to_turn_index_change = cycle([-1, 0, 1])

    @property
    def direction(self):
        return CLOCKWISE_DIRECTIONS[self.direction_index % 4]

    def tick(self, track_map):
        if self.direction == 'up':
            self.y -= 1
        elif self.direction == 'down':
            self.y += 1
        elif self.direction == 'left':
            self.x -= 1
        elif self.direction == 'right':
            self.x += 1

        new_location = track_map[self.x][self.y]

        if new_location == '+':
            index_change = next(self.to_turn_index_change)
            self.direction_index += index_change

        # check curves
        if new_location == '/':
            if self.direction == 'up':
                self.direction_index += 1
            elif self.direction == 'right':
                self.direction_index -= 1
            elif self.direction == 'down':
                self.direction_index += 1
            elif self.direction == 'left':
                self.direction_index -= 1
        elif new_location == '\\':
            if self.direction == 'up':
                self.direction_index -= 1
            elif self.direction == 'right':
                self.direction_index += 1
            elif self.direction == 'down':
                self.direction_index -= 1
            elif self.direction == 'left':
                self.direction_index += 1


    def __str__(self):
        return '({},{}) {}'.format(self.x, self.y, self.direction)


def load_map_and_carts(filename):
    carts = []
    track_map = defaultdict(dict)
    with open(filename) as file:
        for y, line in enumerate(file):
            new_line = ''
            for x, c in enumerate(line.rstrip('\n')):
                if c == 'v':
                    carts.append(Cart(x, y, 2))
                    track_map[x][y] = '|'
                elif c == '^':
                    carts.append(Cart(x, y, 0))
                    track_map[x][y] = '|'
                elif c == '<':
                    carts.append(Cart(x, y, 3))
                    track_map[x][y] = '-'
                elif c == '>':
                    carts.append(Cart(x, y, 1))
                    track_map[x][y] = '-'
                else:
                    track_map[x][y] = c
    return track_map, carts

def print_map(track_map):
    width = len(track_map)
    height = len(track_map[0])
    for y in range(height):
        for x in range(width):
            print(track_map[x][y], end='')
        print()

def find_first_crash(filename):
    track_map, carts = load_map_and_carts(filename)
    carts_by_coordinate = defaultdict(dict)
    for cart in carts:
        carts_by_coordinate[cart.x][cart.y] = cart
    print_map(track_map)
    while True:
        sorted_carts = sorted(carts, key=lambda cart: (cart.y, cart.x))
        for cart in sorted_carts:
            carts_by_coordinate[cart.x].pop(cart.y)
            cart.tick(track_map)
            if carts_by_coordinate.get(cart.x, {}).get(cart.y):
                return (cart.x, cart.y)
            carts_by_coordinate[cart.x][cart.y] = cart

def get_remaining_carts(carts_by_coordinate):
    for cart_map in carts_by_coordinate.values():
        yield from cart_map.values()


def find_last_remaining(filename):
    track_map, carts = load_map_and_carts(filename)
    carts_by_coordinate = defaultdict(dict)
    for cart in carts:
        carts_by_coordinate[cart.x][cart.y] = cart
    print_map(track_map)
    while True:
        sorted_carts = sorted(get_remaining_carts(carts_by_coordinate), key=lambda cart: (cart.y, cart.x))
        for cart in sorted_carts:
            if carts_by_coordinate.get(cart.x, {}).get(cart.y):
                carts_by_coordinate[cart.x].pop(cart.y)
                cart.tick(track_map)
                if carts_by_coordinate.get(cart.x, {}).get(cart.y):
                    carts_by_coordinate[cart.x].pop(cart.y)
                else:
                    carts_by_coordinate[cart.x][cart.y] = cart
        remaining = list(get_remaining_carts(carts_by_coordinate))
        if len(remaining) == 1:
            return (remaining[0].x, remaining[0].y)


print(find_last_remaining('day13_input.txt'))