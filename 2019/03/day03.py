from typing import List, Tuple, Set, Callable, Dict

def get_directions(filename: str) -> List[List[Tuple[str, int]]]:
    wires = []
    with open(filename, 'r') as file:
        for line in file:
            directions = []
            for direction in line.strip().split(','):
                directions.append((direction[0], int(direction[1:])))
            wires.append(directions)
    return wires


def get_move_fn(orientation: str) -> Callable[[int, int], Tuple[int, int]]:
    if orientation == 'U':
        return lambda x,y: (x, y+1)
    elif orientation == 'R':
        return lambda x,y: (x+1, y)
    elif orientation == 'D':
        return lambda x,y: (x, y-1)
    elif orientation == 'L':
        return lambda x,y: (x-1, y)


def get_points(directions: List[Tuple[str, int]]) -> Dict[Tuple[int, int], int]:
    time_to_reach = dict()
    x = 0
    y = 0
    steps = 0
    for orientation, magnitude in directions:
        move_fn = get_move_fn(orientation)
        for _ in range(magnitude):
            steps += 1
            x, y = move_fn(x, y)
            if (x, y) not in time_to_reach:
                time_to_reach[(x, y)] = steps
    # print(points)
    return time_to_reach
        



def find_intersections(filename: str):
    wires = get_directions(filename)
    dict1 = get_points(wires[0])
    dict2 = get_points(wires[1])
    common_points = dict1.keys() & dict2.keys()
    
    distances = [abs(pt[0]) + abs(pt[1]) for pt in common_points]
    combined_steps = [dict1[pt] + dict2[pt] for pt in common_points]
    return min(distances), min(combined_steps)


print(find_intersections('input.txt'))