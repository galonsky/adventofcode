import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Iterable

STEP_PATTERN = re.compile(r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)")


@dataclass
class Range:
    start: int
    end: int


@dataclass
class Step:
    lit: bool
    x_range: Range
    y_range: Range
    z_range: Range


def get_steps(filename: str) -> Iterable[Step]:
    with open(filename, 'r') as file:
        for line in file:
            match = STEP_PATTERN.match(line.strip())
            yield Step(
                lit=match.group(1) == "on",
                x_range=Range(start=int(match.group(2)), end=int(match.group(3))),
                y_range=Range(start=int(match.group(4)), end=int(match.group(5))),
                z_range=Range(start=int(match.group(6)), end=int(match.group(7))),
            )


def light_em_up(steps: Iterable[Step]) -> int:
    cubes = defaultdict(lambda: False)
    for step in steps:
        for x in range(step.x_range.start, step.x_range.end + 1):
            for y in range(step.y_range.start, step.y_range.end + 1):
                for z in range(step.z_range.start, step.z_range.end + 1):
                    cubes[(x,y,z)] = step.lit
    num_lit = 0
    for x in range(-50, 50+1):
        for y in range(-50, 50+1):
            for z in range(-50, 50+1):
                if cubes[(x,y,z)]:
                    num_lit += 1
    return num_lit


if __name__ == '__main__':
    steps = list(get_steps("input.txt"))
    print(light_em_up(steps))