from abc import ABC
from typing import Tuple, Iterable, Dict, Type, TypeVar

DIRECTIONS = [(1, 0),(0, -1),(-1, 0),(0, 1),]

CARDINAL_DIRECTIONS = {
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
    'N': (0, 1),
}


class BaseCommand:
    def __init__(self, action: str, magnitude: int):
        self.action = action
        self.magnitude = magnitude


class Command(BaseCommand):
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


class WaypointCommand(BaseCommand):
    def process(self, cur_x: int, cur_y: int, way_x: int, way_y: int) -> Tuple[int, int, int, int]:
        pass


class WaypointCardinalDirection(WaypointCommand):
    def process(self, cur_x: int, cur_y: int, way_x: int, way_y: int) -> Tuple[int, int, int, int]:
        dx, dy = CARDINAL_DIRECTIONS[self.action]
        new_way_x = way_x + dx * self.magnitude
        new_way_y = way_y + dy * self.magnitude
        return cur_x, cur_y, new_way_x, new_way_y


class WaypointRotate(WaypointCommand):

    def process(self, cur_x: int, cur_y: int, way_x: int, way_y: int) -> Tuple[int, int, int, int]:
        if self.action == 'L':
            num_turns = (360 - self.magnitude) // 90
        else:
            num_turns = self.magnitude // 90
        new_way_x = way_x
        new_way_y = way_y
        for _ in range(num_turns):
            # https://limnu.com/sketch-easy-90-degree-rotate-vectors/
            new_way_x, new_way_y = new_way_y, -new_way_x
        return cur_x, cur_y, new_way_x, new_way_y


class ForwardToWaypoint(WaypointCommand):

    def process(self, cur_x: int, cur_y: int, way_x: int, way_y: int) -> Tuple[int, int, int, int]:
        return cur_x + self.magnitude * way_x, cur_y + self.magnitude * way_y, way_x, way_y


COMMAND_BY_ACTION: Dict[str, Type[Command]] = {
    'N': CardinalDirectionMove,
    'E': CardinalDirectionMove,
    'S': CardinalDirectionMove,
    'W': CardinalDirectionMove,
    'L': Turn,
    'R': Turn,
    'F': Forward,
}


WAYPOINT_COMMAND_BY_ACTION: Dict[str, Type[WaypointCommand]] = {
    'N': WaypointCardinalDirection,
    'E': WaypointCardinalDirection,
    'S': WaypointCardinalDirection,
    'W': WaypointCardinalDirection,
    'L': WaypointRotate,
    'R': WaypointRotate,
    'F': ForwardToWaypoint,
}


T = TypeVar('T', bound=BaseCommand)


def get_commands(filename: str, commands: Dict[str, Type[T]]) -> Iterable[T]:
    with open(filename, 'r') as file:
        for line in file:
            action = line[0]
            magnitude = int(line[1:].strip())
            klass = commands[action]
            yield klass(action, magnitude)


def part1():
    commands = get_commands('input.txt', COMMAND_BY_ACTION)
    dir = 0
    x = 0
    y = 0
    for command in commands:
        x, y, dir = command.process(x, y, dir)

    return abs(x) + abs(y)


def part2():
    commands = get_commands('input.txt', WAYPOINT_COMMAND_BY_ACTION)
    x = 0
    y = 0
    way_x = 10
    way_y = 1
    for command in commands:
        x, y, way_x, way_y = command.process(x, y, way_x, way_y)

    return abs(x) + abs(y)


if __name__ == '__main__':
    print(part2())
