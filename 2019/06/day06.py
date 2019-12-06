from typing import Dict, Iterable, List
from dataclasses import dataclass
from collections import defaultdict

class Node:
    def __init__(self):
        self.orbited_by = set()
    
    def __repr__(self):
        return str(self.orbited_by)


def get_input(filename: str) -> Iterable[List[str]]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip().split(')')


def build_graph(filename: str) -> Dict[str, Node]:
    node_dict = defaultdict(Node)
    for orbit in get_input(filename):
        orbited = orbit[0]
        orbiting = orbit[1]
        if orbiting not in node_dict:
            node_dict[orbiting] = Node()
        node_dict[orbited].orbited_by.add(orbiting)
    return node_dict

def get_sum_of_depths(root: Node, graph: Dict[str, Node], depth=0) -> int:
    if not root.orbited_by:
        return depth
    total = 0
    for orbiting in root.orbited_by:
        total += get_sum_of_depths(graph[orbiting], graph, depth + 1)
    return total + depth

def get_path(root: Node, graph: Dict[str, Node], target: str) -> List[str]:
    if not root.orbited_by:
        return None
    if target in root.orbited_by:
        return [target]
    
    for orbiting in root.orbited_by:
        path = get_path(graph[orbiting], graph, target)
        if path:
            new_path = [orbiting]
            new_path.extend(path)
            return new_path


def get_checksum(filename: str) -> int:
    graph = build_graph(filename)
    # print(graph)
    root = graph['COM']
    return get_sum_of_depths(root, graph)

def get_shortest_path(filename: str):
    graph = build_graph(filename)
    # print(graph)
    root = graph['COM']
    you_path = get_path(root, graph, 'YOU')
    san_path = get_path(root, graph, 'SAN')
    i = 0
    while i < max(len(you_path), len(san_path)) and you_path[i] == san_path[i]:
        i += 1
    
    # i is now index after ancestor
    return (len(you_path) - i) + (len(san_path) - i) - 2  # minus 2 since we want what YOU and SAN are orbiting




print(get_shortest_path('input.txt'))
