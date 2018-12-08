def get_input(filename):
    with open(filename) as file:
        for chunk in file.read().split():
            yield int(chunk)


class Node:
    def __init__(self, children, metadata):
        self.children = children
        self.metadata = metadata

    def value(self):
        if not self.children:
            return sum(self.metadata)
        value_sum = 0
        for metadata in self.metadata:
            index = metadata - 1
            if index >= 0 and index < len(self.children):
                value_sum += self.children[index].value()
        return value_sum

def process_node(nums):
    metadata_sum = 0
    num_children = next(nums)
    num_metadata = next(nums)
    for i in range(num_children):
        metadata_sum += process_node(nums)
    for i in range(num_metadata):
        metadata_sum += next(nums)
    return metadata_sum

def build_node(nums):
    num_children = next(nums)
    num_metadata = next(nums)
    children = []
    metadata = []
    for i in range(num_children):
        children.append(build_node(nums))
    for i in range(num_metadata):
        metadata.append(next(nums))
    return Node(children, metadata)

def get_sum_of_metadata(filename):
    nums = get_input(filename)
    return process_node(nums)

def get_value_of_root(filename):
    nums = get_input(filename)
    root = build_node(nums)
    return root.value()


print(get_value_of_root('day8_input.txt'))