import re
from dataclasses import dataclass
from typing import Iterable


DO_PATTERN = re.compile(r'do\(\)')
DONT_PATTERN = re.compile(r"don't\(\)")
MUL_PATTERN = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
EXPR_PATTERN = re.compile(r"(do\(\))|(don't\(\))|(mul\(\d{1,3},\d{1,3}\))")


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


def get_valid_instructions_do_dont(memory: str) -> Iterable[Mul]:
    enabled = True
    for match in EXPR_PATTERN.finditer(memory):
        if match.lastindex == 1:
            enabled = True
        elif match.lastindex == 2:
            enabled = False
        elif match.lastindex == 3:
            if enabled:
                mul_match = MUL_PATTERN.match(match.group(3))
                yield Mul(int(mul_match.group(1)), int(mul_match.group(2)))
        else:
            raise Exception('huh?')


def get_sum_of_instructions(instructions: Iterable[Mul]) -> int:
    return sum(m.result() for m in instructions)


if __name__ == '__main__':
    memory = get_memory("input.txt")
    instructions = get_valid_instructions_do_dont(memory)
    print(get_sum_of_instructions(instructions))