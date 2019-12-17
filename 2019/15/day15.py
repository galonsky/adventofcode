from typing import Callable
from collections import deque
from itertools import cycle


direction_vectors = (
    (0, -1), #n
    (0, 1),  #s
    (-1, 0), #w
    (1, 0),  #e
)
def get_direction_vector(index):
    if index > 0:
        return direction_vectors[(index - 1) % 4]
    else:
        return direction_vectors[-(abs(index - 1) % 4)]


class TestRobot:
    def __init__(self, o2_point, size=3):
        self.o2_point = o2_point
        self.loc = (0, 0)
        self.size = size
    
    def move(self, input: int) -> int:
        vector = get_direction_vector(input)
        new_point = (self.loc[0] + vector[0], self.loc[1] + vector[1])
        if new_point == self.o2_point:
            return 2
        if new_point[0] == -self.size or new_point[0] == self.size or new_point[1] == -self.size or new_point[1] == self.size:
            return 0
        else:
            self.loc = new_point
            return 1

def find_next_direction(x, y, direction_cycle, discovered):
    best = 'z'
    best_direction = 1
    for _ in range(4):
        idx = next(direction_cycle)
        vector = get_direction_vector(idx)
        possible_point = (x + vector[0], y + vector[1])
        status = discovered.get(possible_point, 'a')
        if status < best:  # a is undiscovered, f is discovered, w is wall
            best_direction = idx
            best = status
    return best_direction


def find_oxygen(robot_fn: Callable[[int], int]):
    x = 0
    y = 0

    discovered = {}

    direction_cycle = cycle(range(1, 5))
    discovered[(x, y)] = 'f'

    direction_index = next(direction_cycle)

    while True:
        print('At {},{}'.format(x, y))
        output = robot_fn(direction_index)
        vector = get_direction_vector(direction_index)
        new_point = (x + vector[0], y + vector[1])
        if output == 2:
            return new_point
        if output == 0:
            discovered[new_point] = 'w'
        elif output == 1:
            x, y = new_point
            discovered[new_point] = 'f'
        
        direction_index = find_next_direction(x, y, direction_cycle, discovered)
                    




    # visited = set()
    # stack = deque()
    # stack.appendleft((x, y))
    # while stack:
    #     v = stack.popleft()
    #     if v not in visited:
    #         visited.add(v)


# print(get_direction_vector(1))
# print(get_direction_vector(2))
# print(get_direction_vector(3))
# print(get_direction_vector(4))
# print(get_direction_vector(5))
robot = TestRobot((1, 2), 10)
print(find_oxygen(robot.move))