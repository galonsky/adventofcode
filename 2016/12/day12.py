from abc import ABC
from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Iterable


@dataclass
class Instruction:
    command: str
    arguments: List[str]

    @classmethod
    def from_str(cls, instruction: str) -> "Instruction":
        parts = instruction.split()
        return cls(parts[0], parts[1:])


def get_instructions(filename: str) -> Iterable[Instruction]:
    with open(filename, 'r') as file:
        for line in file:
            yield Instruction.from_str(line)


class InstructionHandler(ABC):
    def get_value(self, arg: str, memory: dict[str, int]) -> int:
        if arg.isalpha():
            return memory[arg]
        else:
            return int(arg)

    def handle(self, instruction: Instruction, memory: dict[str, int], pc: int) -> int:
        pass


class CopyHandler(InstructionHandler):

    def handle(self, instruction: Instruction, memory: dict[str, int], pc: int) -> int:
        x = self.get_value(instruction.arguments[0], memory)
        memory[instruction.arguments[1]] = x
        return pc + 1


class IncrementHandler(InstructionHandler):

    def handle(self, instruction: Instruction, memory: dict[str, int], pc: int) -> int:
        memory[instruction.arguments[0]] += 1
        return pc + 1


class DecrementHandler(InstructionHandler):

    def handle(self, instruction: Instruction, memory: dict[str, int], pc: int) -> int:
        memory[instruction.arguments[0]] -= 1
        return pc + 1


class JumpNotZeroHandler(InstructionHandler):

    def handle(self, instruction: Instruction, memory: dict[str, int], pc: int) -> int:
        x = self.get_value(instruction.arguments[0], memory)
        if x != 0:
            return pc + int(instruction.arguments[1])
        return pc + 1


HANDLERS: dict[str, InstructionHandler] = {
    "cpy": CopyHandler(),
    "inc": IncrementHandler(),
    "dec": DecrementHandler(),
    "jnz": JumpNotZeroHandler(),
}


@dataclass
class Program:
    instructions: List[Instruction]
    pc: int = 0
    memory: dict[str, int] = field(default_factory=lambda: defaultdict(int))

    def run(self):
        while 0 <= self.pc < len(self.instructions):
            inst = self.instructions[self.pc]
            handler = HANDLERS[inst.command]
            self.pc = handler.handle(inst, self.memory, self.pc)
        print(self.memory["a"])


if __name__ == '__main__':
    instructions = list(get_instructions("input.txt"))
    Program(instructions).run()
