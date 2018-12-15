from collections import defaultdict


class ElfDiedException(Exception):
    pass


class Unit:
    def __init__(self, type, x, y, attack_power):
        self.type = type
        self.x = x
        self.y = y
        self.hp = 200
        self.alive = True
        self.attack_power = attack_power

    def take_damage(self, damage, cave_map, units_by_coord):
        self.hp -= damage
        #print('{} taking damage down to {}'.format(self, self.hp))
        if self.hp <= 0:
            if self.type == 'E':
                raise ElfDiedException()
            self.alive = False
            cave_map[self.x][self.y] = '.'
            units_by_coord[self.x].pop(self.y)

    def attack(self, target, cave_map, units_by_coord):
        #print('{} attacking {}'.format(self, target))
        target.take_damage(self.attack_power, cave_map, units_by_coord)

    def move(self, x, y, cave_map, units_by_coord):
        #print('{} moving to {},{}'.format(self, x, y))
        cave_map[self.x][self.y] = '.'
        units_by_coord[self.x].pop(self.y)
        self.x = x
        self.y = y
        cave_map[x][y] = self.type
        units_by_coord[x][y] = self
        #print_map(cave_map)

    def __str__(self):
        return 'Unit at {},{}'.format(self.x, self.y)


    def take_turn(self, cave_map, units_by_coord):
        #print_map(cave_map)
        #print('{} starting turn'.format(self))
        units = all_units(units_by_coord)
        targets = [unit for unit in units if unit.type != self.type]
        if not targets:
            return False

        in_range_coords = set()
        adjacent_targets = [target for target in targets if adjacent(self.x, self.y, target.x, target.y)]
        if adjacent_targets:
            #for target in adjacent_targets:
                #print('Target {} has {} hp'.format(target, target.hp))
            best_target = min(adjacent_targets, key=lambda target: (target.hp, target.y, target.x))
            self.attack(best_target, cave_map, units_by_coord)
            return True

        for target in targets:
            for coord in get_in_range_coords(target.x, target.y, cave_map):
                in_range_coords.add(coord)

        if not in_range_coords:
            return True

        # find shortest paths
        distances = calculate_distances(self.x, self.y, cave_map)
        min_in_range = min(in_range_coords, key=lambda coord: (distances[coord], coord[1], coord[0]))
        if distances[min_in_range] == float("inf"):
            # no reachable in range coords
            return True

        possible_moves = list(get_in_range_coords(self.x, self.y, cave_map))
        #print(list(possible_moves))
        distance_to_target_by_move = {
            move: calculate_distances(move[0], move[1], cave_map)[min_in_range]
            for move in possible_moves
        }

        best_move = min(possible_moves, key=lambda move: (distance_to_target_by_move[move], move[1], move[0]))
        self.move(best_move[0], best_move[1], cave_map, units_by_coord)

        adjacent_targets = [target for target in targets if adjacent(self.x, self.y, target.x, target.y)]
        if adjacent_targets:
            #for target in adjacent_targets:
                #print('Target {} has {} hp'.format(target, target.hp))
            best_target = min(adjacent_targets, key=lambda target: (target.hp, target.y, target.x))
            self.attack(best_target, cave_map, units_by_coord)

        return True


def adjacent(x1, y1, x2, y2):
    x_diff = abs(x1 - x2)
    y_diff = abs(y1 - y2)
    return (x_diff == 0 and y_diff == 1) or (y_diff == 0 and x_diff == 1)


def calculate_distances(x, y, cave_map):
    # from https://stackoverflow.com/a/37237712

    start = (x, y)
    nodes_to_visit = {start}
    visited_nodes = set()
    distance_from_start = defaultdict(lambda: float("inf"))
    # Distance from start to start is 0
    distance_from_start[start] = 0
    tentative_parents = {}

    while nodes_to_visit:
        current = min(
            nodes_to_visit, key=lambda node: distance_from_start[node]
        )

        nodes_to_visit.discard(current)
        visited_nodes.add(current)

        for neighbour in get_in_range_coords(current[0], current[1], cave_map):
            if neighbour in visited_nodes:
                continue
            neighbour_distance = distance_from_start[current] + 1
            if neighbour_distance < distance_from_start[neighbour]:
                distance_from_start[neighbour] = neighbour_distance
                tentative_parents[neighbour] = current
                nodes_to_visit.add(neighbour)
    return distance_from_start


def get_in_range_coords(x, y, cave_map):
    x_max = len(cave_map) - 1
    y_max = len(cave_map[0]) - 1

    if y - 1 >= 0 and cave_map[x][y-1] == '.':
        yield (x, y-1)
    if y + 1 <= y_max and cave_map[x][y+1] == '.':
        yield (x, y+1)
    if x - 1 >= 0 and cave_map[x - 1][y] == '.':
        yield (x-1, y)
    if x + 1 <= x_max and cave_map[x+1][y] == '.':
        yield (x+1, y)

def build_map(filename):
    cave_map = defaultdict(dict)
    with open(filename) as file:
        for y, line in enumerate(file):
            for x, c in enumerate(line.rstrip('\n')):
                cave_map[x][y] = c
    return cave_map

def all_units(units_by_coord):
    for y_map in units_by_coord.values():
        yield from y_map.values()

def sorted_units(units_by_coord):
    return sorted(all_units(units_by_coord), key=lambda unit: (unit.y, unit.x))

def print_map(cave_map):
    x_len = len(cave_map)
    y_len = len(cave_map[0])
    for y in range(y_len):
        for x in range(x_len):
            c = cave_map[x][y]
            print(c, end='')
        print()

def run_combat(filename, elf_attack_power=3):
    cave_map = build_map(filename)
    units_by_coord = defaultdict(dict)
    for x, y_map in cave_map.items():
        for y, c in y_map.items():
            if c in ('G', 'E'):
                attack_power = elf_attack_power if c == 'E' else 3
                units_by_coord[x][y] = Unit(c, x, y, attack_power)

    #print_map(cave_map)
    i = 1
    while True:
        units = sorted_units(units_by_coord)
        for unit in units:
            if unit.alive:
                result = unit.take_turn(cave_map, units_by_coord)
                if not result:
                    #print_map(cave_map)
                    sum_of_hp = sum([unit.hp for unit in units if unit.alive])
                    #print(sum_of_hp)
                    return sum_of_hp * (i - 1)
        #print('Round {}'.format(i))
        #print_map(cave_map)
        i += 1


def get_combat_where_elves_win(filename):
    power = 4
    while True:
        print(power)
        try:
            return run_combat(filename, power)
        except ElfDiedException:
            pass
        power += 1

print(get_combat_where_elves_win('day15_input.txt'))