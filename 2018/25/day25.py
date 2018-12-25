from collections import defaultdict


class Constellation:
    def __init__(self, id):
        self.id = id
        self.coords = set()

    def add_coord(self, coord):
        self.coords.add(coord)

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        return isinstance(other, Constellation) and self.id == other.id


def load_coords(filename):
    with open(filename) as file:
        for line in file:
            parts = line.rstrip('\n').split(',')
            yield (int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3]))

def get_1_aways(coord):
    yield (coord[0] + 1, coord[1], coord[2], coord[3])
    yield (coord[0], coord[1] + 1, coord[2], coord[3])
    yield (coord[0], coord[1], coord[2] + 1, coord[3])
    yield (coord[0], coord[1], coord[2], coord[3] + 1)
    yield (coord[0] - 1, coord[1], coord[2], coord[3])
    yield (coord[0], coord[1] - 1, coord[2], coord[3])
    yield (coord[0], coord[1], coord[2] - 1, coord[3])
    yield (coord[0], coord[1], coord[2], coord[3] - 1)


def get_3_aways(start_coord):
    all_neighbors = {start_coord}
    last_neighbors = [start_coord]
    for i in range(3):
        new_neighbors = []
        for coord in last_neighbors:
            new_neighbors.extend(get_1_aways(coord))
        last_neighbors = new_neighbors
        all_neighbors.update(last_neighbors)
    return all_neighbors


def find_constellations(filename):
    coords = list(load_coords(filename))
    universe_points_to_canonical_points = defaultdict(list)
    for coord in coords:
        neighbors = get_3_aways(coord)
        for neighbor in neighbors:
            universe_points_to_canonical_points[neighbor].append(coord)

    constellation_by_coord = {}
    const_id = 0
    for coord in coords:
        if coord in constellation_by_coord:
            continue
        neighbors = universe_points_to_canonical_points[coord]
        constellation = None
        for neighbor in neighbors:
            if not constellation:
                if neighbor in constellation_by_coord:
                    constellation = constellation_by_coord[neighbor]
                else:
                    constellation = Constellation(const_id)
                    const_id += 1
                constellation.add_coord(coord)
                constellation.add_coord(neighbor)
                constellation_by_coord[coord] = constellation
                constellation_by_coord[neighbor] = constellation
            else:
                if not neighbor in constellation_by_coord:
                    constellation.add_coord(neighbor)
                    constellation_by_coord[neighbor] = constellation
                else:
                    other_constellation = constellation_by_coord[neighbor]
                    for other_coord in other_constellation.coords:
                        constellation.add_coord(other_coord)
                        constellation_by_coord[other_coord] = constellation
    unique_constellations = set(constellation_by_coord.values())
    prev_count = len(unique_constellations)
    while True:
        merge_constellations(constellation_by_coord, universe_points_to_canonical_points)
        unique_constellations = set(constellation_by_coord.values())
        if len(unique_constellations) == prev_count:
            return prev_count
        prev_count = len(unique_constellations)


def merge_constellations(constellation_by_coord, universe_points_to_canonical_points):
    constellations = set(constellation_by_coord.values())
    for constellation in constellations:
        coords_copy = list(constellation.coords)
        for coord in coords_copy:
            for neighbor in universe_points_to_canonical_points[coord]:
                if constellation_by_coord[neighbor] != constellation:
                    other_constellation = constellation_by_coord[neighbor]
                    for other_coord in other_constellation.coords:
                        constellation.add_coord(other_coord)
                        constellation_by_coord[other_coord] = constellation

print(find_constellations('day25_input.txt'))