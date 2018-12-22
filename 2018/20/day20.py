from collections import deque, defaultdict


class Node:
    def __init__(self, data):
        self.data = data
        self.edges = {}

    def add_edge(self, edge_data, node=None):
        if node:
            if edge_data in self.edges:
                raise Exception('already has edge')
            self.edges[edge_data] = node
            return node

        if edge_data in self.edges:
            return self.edges[edge_data]
        new_node = Node(edge_data)
        self.edges[edge_data] = new_node
        return new_node


    def __str__(self):
        return 'Node: {}'.format(self.data)

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.coord_key() == other.coord_key()

    def __hash__(self):
        return hash(self.coord_key())

    def coord_key(self):
        return (self.x, self.y)


def reduce_graph(root):
    root.x = 0
    root.y = 0
    visited_nodes = set()
    nodes_to_visit = deque([root])
    while nodes_to_visit:
        current = nodes_to_visit.popleft()
        visited_nodes.add(current)
        while '' in current.edges:
            empty_node = current.edges.pop('')
            #print('removing empty')
            for edge_data, edge in empty_node.edges.items():
                current.add_edge(edge.data, edge)
        for direction, edge in current.edges.items():
            if direction == 'N':
                edge.x = current.x
                edge.y = current.y - 1
            elif direction == 'E':
                edge.x = current.x + 1
                edge.y = current.y
            elif direction == 'S':
                edge.x = current.x
                edge.y = current.y + 1
            elif direction == 'W':
                edge.x = current.x - 1
                edge.y = current.y
            if edge not in visited_nodes:
                nodes_to_visit.append(edge)
    return root


def calculate_distances(root):
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

        for neighbour in current.edges.values():
            if neighbour in visited_nodes:
                continue
            neighbour_distance = distance_from_start[current] + 1
            if neighbour_distance < distance_from_start[neighbour]:
                distance_from_start[neighbour] = neighbour_distance
                nodes_to_visit.add(neighbour)
    return distance_from_start


def largest_shortest_path(regex):
    root = process_group(regex)
    distances = calculate_distances(root)
    return max(distances.values())


def num_shortest_paths_at_least_1000(regex):
    root = process_group(regex)
    distances = calculate_distances(root)
    return sum((1 for distance in distances.values() if distance >= 1000))



def can_match_path(root, path):
    progress = ''
    current = root
    for c in path:
        while '' in current.edges:
            current = current.edges['']
        if c in current.edges:
            current = current.edges[c]
            progress += c
        else:
            print('matched up to: {}'.format(progress))
            return False
    while '' in current.edges:
        current = current.edges['']
    return len(current.edges) == 0


def process_group(regex):
    # stack of beginning paren nodes?
    # stack of before paren nodes?
    before_group_stack = deque()
    end_group_stack = deque()
    root = Node('')
    current = root

    for c in regex:
        if c == '(':
            before_group_stack.append(current)
            end_group_stack.append(Node(''))
        elif c == ')':
            # close out previous branch
            current.add_edge('', end_group_stack[-1])
            # next nodes continue from last node before this group
            current = end_group_stack.pop()
            before_group_stack.pop()
        elif c == '|':
            # close out previous branch
            current.add_edge('', end_group_stack[-1])
            # next nodes need to be added as an edge from the last node before this group
            current = before_group_stack[-1]
        else:
            current = current.add_edge(c)
    return reduce_graph(root)

def calculate_from_file(filename):
    with open(filename) as file:
        regex = file.read()
        return num_shortest_paths_at_least_1000(regex)

print(calculate_from_file('day20_input.txt'))


class TestCanMatchPath:
    def test_simple(self):
        root = process_group('WNE')
        assert can_match_path(root, 'WNE')

    def test_some_parens(self):
        root = process_group('ENWWW(NEEE|SSE(EE|N))')
        assert can_match_path(root, 'ENWWWNEEE')
        assert can_match_path(root, 'ENWWWSSEEE')
        assert can_match_path(root, 'ENWWWSSEN')

    def test_more_complicated(self):
        root = process_group('ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN')
        assert can_match_path(root, 'ENNWSWWSSSEENEENNN')
        assert can_match_path(root, 'ENNWSWWNEWSSSSEENEENNN')
        assert can_match_path(root, 'ENNWSWWNEWSSSSEENEESWENNNN')
        assert can_match_path(root, 'ENNWSWWSSSEENWNSEEENNN')

class TestLargestShortestPath:
    def test_simple(self):
        assert largest_shortest_path('WNE') == 3

    def test_some_parens(self):
        assert largest_shortest_path('ENWWW(NEEE|SSE(EE|N))') == 10

    def test_more_complicated(self):
        assert largest_shortest_path('ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN') == 18
        assert largest_shortest_path('ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))') == 23
        assert largest_shortest_path('WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))') == 31
