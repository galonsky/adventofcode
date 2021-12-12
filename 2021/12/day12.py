from collections import defaultdict


def get_connections(filename: str) -> dict[str, set[str]]:
    connections = defaultdict(set)
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('-')
            connections[parts[0]].add(parts[1])
            connections[parts[1]].add(parts[0])
    return connections


def find_all_paths(start: str, end: str, visited_small: set[str], prev_path: list[str], connections: dict[str, set[str]]) -> set[str]:
    visited_small = set(visited_small)
    if start.islower():
        visited_small.add(start)
    curr_path = prev_path + [start]
    if start == end:
        return {"-".join(curr_path)}
    ret_set = set()
    for neighbor in connections[start]:
        if neighbor.islower() and neighbor in visited_small:
            continue
        ret_set |= find_all_paths(neighbor, end, visited_small, curr_path, connections)
    return ret_set


if __name__ == '__main__':
    connections = get_connections("input.txt")
    paths = find_all_paths("start", "end", set(), [], connections)
    print(paths)
    print(len(paths))