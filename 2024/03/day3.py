import re
from dataclasses import dataclass
from typing import Iterable


MUL_PATTERN = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')


@dataclass
class Mul:
    left: int
    right: int

    def result(self) -> int:
        return self.left * self.right


def get_memory(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read().strip()


def get_valid_instructions(memory: str) -> Iterable[Mul]:
    for match in MUL_PATTERN.finditer(memory):
        yield Mul(int(match.group(1)), int(match.group(2)))


def get_sum_of_instructions(instructions: Iterable[Mul]) -> int:
    return sum(m.result() for m in instructions)


if __name__ == '__main__':
    memory = get_memory("input.txt")
    instructions = get_valid_instructions(memory)
    print(get_sum_of_instructions(instructions))