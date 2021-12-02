from dataclasses import dataclass
from typing import Iterable


@dataclass
class Command:
    direction: str
    magnitude: int


def get_commands(filename: str) -> Iterable[Command]:
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split()
            yield Command(parts[0], int(parts[1]))


def get_final_position(commands: Iterable[Command]) -> tuple[int, int]:
    horiz = 0
    depth = 0
    for command in commands:
        if command.direction == "forward":
            horiz += command.magnitude
        elif command.direction == "up":
            depth -= command.magnitude
        elif command.direction == "down":
            depth += command.magnitude
        else:
            raise Exception('unexpected!')
    return horiz, depth


def get_final_position_aim(commands: Iterable[Command]) -> tuple[int, int]:
    horiz = 0
    depth = 0
    aim = 0
    for command in commands:
        if command.direction == "forward":
            horiz += command.magnitude
            depth += aim * command.magnitude
        elif command.direction == "up":
            aim -= command.magnitude
        elif command.direction == "down":
            aim += command.magnitude
        else:
            raise Exception('unexpected!')
    return horiz, depth


if __name__ == '__main__':
    commands = list(get_commands("input.txt"))
    horiz, depth = get_final_position(commands)
    print(horiz * depth)
    horiz, depth = get_final_position_aim(commands)
    print(horiz * depth)