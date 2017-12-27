import re


class Node:
    def __init__(self, name):
        self.name = name
        self.edges = []

    def __str__(self):
        return str([edge.name for edge in self.edges])


def build_graph():
    with open('day12_input.txt') as file:
        nodes = {}
        for line in file:
            groups = re.search('([0-9]+) \<\-\> (.+)', line.rstrip('\n')).groups()
            node = groups[0]
            edges = groups[1].split(', ')
            if node not in nodes:
                nodes[node] = Node(node)
            for edge in edges:
                if edge not in nodes:
                    nodes[edge] = Node(edge)
                edge_node = nodes[edge]
                nodes[node].edges.append(edge_node)
        return nodes


def dfs(start_node):
    s = []
    discovered = set()
    s.append(start_node)
    while len(s) > 0:
        v = s.pop()
        if v not in discovered:
            discovered.add(v)
            for edge in v.edges:
                s.append(edge)
    # return len(discovered)
    return frozenset(discovered)


def find_connections():
    nodes = build_graph()
    # print(dfs(nodes['0']))
    set_of_sets = set()
    for node in nodes:
        set_of_sets.add(dfs(nodes[node]))
    print(len(set_of_sets))


find_connections()
