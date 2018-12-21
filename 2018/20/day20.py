from collections import deque


class Node:
    def __init__(self, data):
        self.data = data
        self.edges = {}

    def add_edge(self, edge):
        edge_data = edge.data
        # what if already exists?


    def __str__(self):
        return 'Node: {}'.format(self.data)

    def __repr__(self):
        return str(self)


def reduce_graph(root):
    current = root



def can_match_path(root, path):
    current = root
    for c in path:
        




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
            current.add_edge(end_group_stack[-1])
            # next nodes continue from last node before this group
            current = end_group_stack.pop()
            before_group_stack.pop()
        elif c == '|':
            # close out previous branch
            current.add_edge(end_group_stack[-1])
            # next nodes need to be added as an edge from the last node before this group
            current = before_group_stack[-1]
        else:
            new_node = Node(c)
            current.add_edge(new_node)
            current = new_node
    return root