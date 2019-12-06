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

def get_checksum(filename: str) -> int:
    graph = build_graph(filename)
    # print(graph)
    root = graph['COM']
    return get_sum_of_depths(root, graph)



print(get_checksum('input.txt'))
