from collections import defaultdict


class CaveRiskCalculator:

    allowed_tools_by_type = {
        0: ['climbing', 'torch'], # rocky
        1: ['climbing', 'neither'], # wet
        2: ['torch', 'neither'], # narrow
    }

    def __init__(self, target_x, target_y, depth):
        self.target = (target_x, target_y)
        self.depth = depth
        self.index_cache = {}
        self.erosion_cache = {}

    def get_erosion_level(self, x, y):
        return (self.get_geologic_index(x, y) + self.depth) % 20183

    def get_region_type(self, x, y):
        return self.get_erosion_level(x, y) % 3

    def get_geologic_index(self, x, y):
        if (x, y) in self.index_cache:
            return self.index_cache[(x, y)]
        index = self._get_geologic_index(x, y)
        self.index_cache[(x, y)] = index
        return index

    def _get_geologic_index(self, x, y):
        if (0, 0) == (x, y):
            return 0

        if self.target == (x, y):
            return 0

        if y == 0:
            return 16807 * x

        if x == 0:
            return 48271 * y

        return self.get_erosion_level(x-1, y) * self.get_erosion_level(x, y-1)

    def calculate_risk(self):
        total_risk = 0
        for x in range(0, self.target[0] + 1):
            for y in range(0, self.target[1] + 1):
                risk = self.get_region_type(x, y)
                total_risk += risk

        return total_risk

    def in_range_neighbors(self, x, y):
        if x - 1 >= 0:
            yield (x-1, y)
        if y - 1 >= 0:
            yield (x, y - 1)
        # arbitrary buffers going past target /shrug
        if x + 1 <= self.target[0] + 100:
            yield (x + 1, y)
        if y + 1 <= self.target[1] + 100:
            yield (x, y + 1)

    def get_neighbors_and_weight_pairs(self, x, y, current_tool):
        current_region_type = self.get_region_type(x, y)
        for tool in self.allowed_tools_by_type[current_region_type]:
            for neighbour in self.in_range_neighbors(x, y):
                region_type = self.get_region_type(*neighbour)
                if tool in self.allowed_tools_by_type[region_type]:
                    change_tool_penalty = 7 if tool != current_tool else 0
                    yield (neighbour, tool, 1 + change_tool_penalty)

    def calculate_distances(self):
        current_tool = 'torch'

        root = ((0, 0), current_tool)
        nodes_to_visit = {root}
        visited_nodes = set()
        distance_from_start = defaultdict(lambda: float("inf"))
        # Distance from start to start is 0
        distance_from_start[root] = 0

        while nodes_to_visit:
            current = min(
                nodes_to_visit, key=lambda node: distance_from_start[node]
            )

            nodes_to_visit.discard(current)
            visited_nodes.add(current)

            for neighbour_triplet in self.get_neighbors_and_weight_pairs(current[0][0], current[0][1], current[1]):
                coord_tool = (neighbour_triplet[0], neighbour_triplet[1])
                if coord_tool in visited_nodes:
                    continue
                neighbour_distance = distance_from_start[current] + neighbour_triplet[2]
                if neighbour_distance < distance_from_start[coord_tool]:
                    distance_from_start[coord_tool] = neighbour_distance
                    nodes_to_visit.add(coord_tool)
        return distance_from_start


def time_to_target(targetx, targety, depth):
    calculator = CaveRiskCalculator(targetx, targety, depth)
    distances = calculator.calculate_distances()
    # print(distances)
    torch_distance = distances.get(((targetx, targety), 'torch'))
    climbing_distance = distances.get(((targetx, targety), 'climbing'))
    return min(torch_distance, climbing_distance + 7)

# print(time_to_target(10, 10, 510))
print(time_to_target(9, 739, 10914))