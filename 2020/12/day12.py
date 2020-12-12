from abc import ABC
from typing import Tuple, Iterable

DIRECTIONS = [(1, 0),(0, -1),(-1, 0),(0, 1),]

CARDINAL_DIRECTIONS = {
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
    'N': (0, 1),
}


class Command(ABC):
    def __init__(self, action: str, magnitude: int):
        self.action = action
        self.magnitude = magnitude

    def process(self, cur_x: int, cur_y: int, cur_dir: int) -> Tuple[int, int, int]:
        pass


class CardinalDirectionMove(Command):
    def process(self, cur_x: int, cur_y: int, cur_dir: int) -> Tuple[int, int, int]:
        dx, dy = CARDINAL_DIRECTIONS[self.action]
        new_x = cur_x + dx * self.magnitude
        new_y = cur_y + dy * self.magnitude
        return new_x, new_y, cur_dir


class Turn(Command):
    def process(self, cur_x: int, cur_y: int, cur_dir: int) -> Tuple[int, int, int]:
        if self.action == 'L':
            num_turns = (360 - self.magnitude) // 90
        else:
            num_turns = self.magnitude // 90
        return cur_x, cur_y, (cur_dir + num_turns) % 4


class Forward(Command):
    def process(self, cur_x: int, cur_y: int, cur_dir: int) -> Tuple[int, int, int]:
        dx, dy = DIRECTIONS[cur_dir]
        return cur_x + self.magnitude * dx, cur_y + self.magnitude * dy, cur_dir


COMMAND_BY_ACTION = {
    'N': CardinalDirectionMove,
    'E': CardinalDirectionMove,
    'S': CardinalDirectionMove,
    'W': CardinalDirectionMove,
    'L': Turn,
    'R': Turn,
    'F': Forward,
}


def get_commands(filename: str) -> Iterable[Command]:
    with open(filename, 'r') as file:
        for line in file:
            action = line[0]
            magnitude = int(line[1:].strip())
            klass = COMMAND_BY_ACTION[action]
            yield klass(action, magnitude)


def part1():
    commands = get_commands('input.txt')
    dir = 0
    x = 0
    y = 0
    for command in commands:
        x, y, dir = command.process(x, y, dir)

    return abs(x) + abs(y)


if __name__ == '__main__':
    print(part1())