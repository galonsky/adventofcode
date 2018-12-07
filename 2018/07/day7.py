import re
from collections import defaultdict

PATTERN = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin\.')


def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.rstrip('\n')


class Node:
    def __init__(self, id):
        self.id = id
        self.dependencies = list()
        self.done = False
        self.claimed = False

    def add_dependency(self, dependency):
        self.dependencies.append(dependency)

    def mark_done(self):
        self.done = True

    def mark_claimed(self):
        self.claimed = True

    def is_ready(self):
        if self.done or self.claimed:
            return False
        for dependency in self.dependencies:
            if not dependency.done:
                return False
        return True

    def get_work_time(self):
        return 60 + ord(self.id) - ord('A') + 1


class Elf:
    def __init__(self):
        self.working_on = None
        self.countdown = None

    def is_free(self):
        return not bool(self.working_on)

    def claim(self, node):
        self.working_on = node
        self.countdown = node.get_work_time()
        node.mark_claimed()

    def tick(self):
        if self.working_on:
            self.countdown -= 1
            if self.countdown == 0:
                self.working_on.mark_done()
                self.working_on = None


def get_next_ready_node(nodes):
    sorted_keys = sorted(nodes.keys())
    for key in sorted_keys:
        node = nodes[key]
        if node.is_ready():
            return node


def get_nodes(filename):
    nodes = {}
    for line in get_lines(filename):
        match = PATTERN.match(line)
        dependency_id = match.group(1)
        dependent_id = match.group(2)
        if not dependency_id in nodes:
            nodes[dependency_id] = Node(dependency_id)
        if not dependent_id in nodes:
            nodes[dependent_id] = Node(dependent_id)
        nodes[dependent_id].add_dependency(nodes[dependency_id])
    return nodes


def get_order(filename):
    nodes = get_nodes(filename)
    order = ''

    ready_node = get_next_ready_node(nodes)
    while(ready_node):
        ready_node.mark_done()
        order += ready_node.id
        ready_node = get_next_ready_node(nodes)
    return order


def next_free_elf(elves):
    for elf in elves:
        if elf.is_free():
            return elf


def get_duration(filename):
    nodes = get_nodes(filename)
    elves = [Elf() for i in range(5)]

    duration = -1

    
    while True:
        ready_node = get_next_ready_node(nodes)
        free_elf = next_free_elf(elves)
        if ready_node and free_elf:
            free_elf.claim(ready_node)
        for elf in elves:
            elf.tick()

        if all([node.done for node in nodes.values()]):
            return duration

        duration += 1


print(get_duration('day7_input.txt'))
