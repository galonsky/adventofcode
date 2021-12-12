from collections import defaultdict


def get_connections(filename: str) -> dict[str, set[str]]:
    connections = defaultdict(set)
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split('-')
            connections[parts[0]].add(parts[1])
            connections[parts[1]].add(parts[0])
    return connections


def find_all_paths(start: str, end: str, visited_small: dict[str, int], prev_path: list[str], connections: dict[str, set[str]]) -> set[str]:
    visited_small = defaultdict(int, visited_small)
    if start.islower():
        visited_small[start] += 1
    curr_path = prev_path + [start]
    if start == end:
        return {"-".join(curr_path)}
    ret_set = set()
    for neighbor in connections[start]:
        if neighbor.islower() and visited_small[neighbor] >= 1:
            continue
        ret_set |= find_all_paths(neighbor, end, visited_small, curr_path, connections)
    return ret_set


def find_all_paths_with_one_special_room(connections: dict[str, set[str]]) -> set[str]:
    uber_set = set()
    for lower_room in (key for key in connections.keys() if key.islower() and key not in {'start', 'end'}):
        visited_small = defaultdict(int)
        visited_small[lower_room] = -1
        uber_set |= find_all_paths("start", "end", visited_small, [], connections)
    return uber_set


if __name__ == '__main__':
    connections = get_connections("input.txt")
    # paths = find_all_paths("start", "end", defaultdict(int), [], connections)
    # print(paths)
    # print(len(paths))
    paths = find_all_paths_with_one_special_room(connections)
    print(len(paths))
