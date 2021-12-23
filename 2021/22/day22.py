import re
from collections import defaultdict, deque
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, Optional

STEP_PATTERN = re.compile(r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)")


@dataclass
class Range:
    start: int
    end: int

    def size(self) -> int:
        return self.end - self.start + 1


@dataclass
class Cuboid:
    x_range: Range
    y_range: Range
    z_range: Range

    def __bool__(self):
        return bool(self.size())

    def size(self) -> int:
        return self.x_range.size() * self.y_range.size() * self.z_range.size()

    def intersection(self, other: "Cuboid") -> "Cuboid":
        """
        x: 0 -> 100
        y: 100 -> 200
        z: 50 -> 75

        x: 75 -> 125
        y: 50 -> 110
        z: 50 -> 60
        :param other:
        :return:
        """
        if other.x_range.start <= self.x_range.start <= other.x_range.end:
            x_range = Range(self.x_range.start, min(self.x_range.end, other.x_range.end))
        elif self.x_range.start <= other.x_range.start <= self.x_range.end:
            x_range = Range(other.x_range.start, min(self.x_range.end, other.x_range.end))
        else:
            return NullCuboid()

        if other.y_range.start <= self.y_range.start <= other.y_range.end:
            y_range = Range(self.y_range.start, min(self.y_range.end, other.y_range.end))
        elif self.y_range.start <= other.y_range.start <= self.y_range.end:
            y_range = Range(other.y_range.start, min(self.y_range.end, other.y_range.end))
        else:
            return NullCuboid()

        if other.z_range.start <= self.z_range.start <= other.z_range.end:
            z_range = Range(self.z_range.start, min(self.z_range.end, other.z_range.end))
        elif self.z_range.start <= other.z_range.start <= self.z_range.end:
            z_range = Range(other.z_range.start, min(self.z_range.end, other.z_range.end))
        else:
            return NullCuboid()

        return Cuboid(x_range, y_range, z_range)

    def difference(self, to_subtract: "Cuboid") -> Iterable["Cuboid"]:
        chunk = self.intersection(to_subtract)
        if not chunk:
            yield self
            return

        # top
        if chunk.z_range.end + 1 <= self.z_range.end:
            yield Cuboid(
                x_range=self.x_range,
                y_range=self.y_range,
                z_range=Range(chunk.z_range.end + 1, self.z_range.end)
            )

        # bottom
        if chunk.z_range.start - 1 >= self.z_range.start:
            yield Cuboid(
                x_range=self.x_range,
                y_range=self.y_range,
                z_range=Range(self.z_range.start, chunk.z_range.start - 1)
            )

        # north
        if chunk.y_range.end + 1 <= self.y_range.end:
            yield Cuboid(
                x_range=self.x_range,
                y_range=Range(chunk.y_range.end + 1, self.y_range.end),
                z_range=chunk.z_range,
            )

        # south
        if chunk.y_range.start - 1 >= self.y_range.start:
            yield Cuboid(
                x_range=self.x_range,
                y_range=Range(self.y_range.start, chunk.y_range.start - 1),
                z_range=chunk.z_range,
            )

        # east
        if chunk.x_range.end + 1 <= self.x_range.end:
            yield Cuboid(
                x_range=Range(chunk.x_range.end + 1, self.x_range.end),
                y_range=chunk.y_range,
                z_range=chunk.z_range,
            )

        # west
        if chunk.x_range.start - 1 >= self.x_range.start:
            yield Cuboid(
                x_range=Range(self.x_range.start, chunk.x_range.start - 1),
                y_range=chunk.y_range,
                z_range=chunk.z_range,
            )


class NullCuboid(Cuboid):

    def __init__(self) -> None:
        super().__init__(
            x_range=None,
            y_range=None,
            z_range=None,
        )

    def size(self) -> int:
        return 0

    def intersection(self, other: "Cuboid") -> "Cuboid":
        return NullCuboid()


@dataclass
class Step(Cuboid):
    lit: bool


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


def light_em_up_v3(steps: list[Step]) -> int:
    lit: deque[Cuboid] = deque()
    for i, step in enumerate(steps):
        print(i)
        if step.lit:
            new_to_check: deque[Cuboid] = deque([step])
            while new_to_check:
                to_add = new_to_check.popleft()
                add_me = True
                for already_lit in lit:
                    if to_add.intersection(already_lit):
                        add_me = False
                        difference = list(to_add.difference(already_lit))
                        if difference:
                            new_to_check.extend(difference)
                        break
                if add_me:
                    lit.append(to_add)
        else:
            new_lit = deque()
            while lit:
                already_lit = lit.popleft()
                if step.intersection(already_lit):
                    remnants = list(already_lit.difference(step))
                    if remnants:
                        new_lit.extend(remnants)
                else:
                    new_lit.append(already_lit)
            lit = new_lit

    intersections = [a.intersection(b) for a, b in combinations(lit, 2)]
    assert not any(intersections)
    return sum(c.size() for c in lit)


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
    steps = list(get_steps("full_input.txt"))
    print(light_em_up_v3(steps))
