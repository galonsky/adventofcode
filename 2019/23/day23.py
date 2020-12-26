import math

from typing import List, Iterable, Callable
from itertools import permutations, cycle
from dataclasses import dataclass
from collections import defaultdict, deque, OrderedDict
from queue import PriorityQueue


@dataclass
class ProgramStatus:
    status: str
    outputs: List[int]


def parse_first_instruction(instruction):
    opcode = instruction % 100
    modes_in_order = str(instruction)[:-2][::-1]
    return opcode, modes_in_order


def get_mode(modes, index):
    if index >= len(modes):
        return 0
    return int(modes[index])


class HaltException(Exception):
    pass


class Instruction:
    num_params = NotImplementedError

    def __init__(self, program, modes):
        self.program = program
        self.modes = modes

    def get_at_address(self, address: int) -> int:
        if address < 0:
            raise Exception('read from negative address')
        return self.program.int_codes.get(address, 0)

    def get_param_value(self, index):
        if index >= self.num_params:
            raise IndexError('not that many params')
        address = self.get_param_address(index)
        return self.get_at_address(address)

    def get_param_address(self, index):
        param_address = self.program.pc + index + 1
        param = self.get_at_address(param_address)
        mode = get_mode(self.modes, index)
        if mode == 2:
            return self.program.relative_base + param
        elif mode == 1:
            return param_address
        elif mode == 0:
            return param
        else:
            raise ValueError('unrecognized mode')

    def run(self):
        return 'continue'

    def update_pc(self, code):
        self.program.pc += self.num_params + 1

    def run_and_update_pc(self):
        code = self.run()
        self.update_pc(code)
        return code


class AddInstruction(Instruction):
    num_params = 3

    def run(self):
        addend1 = self.get_param_value(0)
        addend2 = self.get_param_value(1)
        self.program.int_codes[self.get_param_address(2)] = addend1 + addend2
        return 'continue'


class MultiplyInstruction(Instruction):
    num_params = 3

    def run(self):
        multiplicand1 = self.get_param_value(0)
        multiplicand2 = self.get_param_value(1)
        self.program.int_codes[self.get_param_address(2)] = multiplicand1 * multiplicand2
        return 'continue'


class InputInstruction(Instruction):
    num_params = 1

    def run(self):
        param = self.get_param_address(0)
        try:
            self.program.int_codes[param] = next(self.program.input_iterator)
        except StopIteration:
            return 'input'
        return 'continue'

    def update_pc(self, code):
        if code == 'input':
            return
        return super().update_pc(code)


class OutputInstruction(Instruction):
    num_params = 1

    def run(self):
        param = self.get_param_value(0)
        self.program.outputs.append(param)
        try:
            print(chr(param), end='')
        except ValueError:
            print(param)
        return 'output'


class JumpNotEqualToZeroInstruction(Instruction):
    num_params = 2

    def update_pc(self, code):
        to_test = self.get_param_value(0)
        if to_test != 0:
            self.program.pc = self.get_param_value(1)
        else:
            super().update_pc(code)


class JumpEqualToZeroInstruction(Instruction):
    num_params = 2

    def update_pc(self, code):
        to_test = self.get_param_value(0)
        if to_test == 0:
            self.program.pc = self.get_param_value(1)
        else:
            super().update_pc(code)


class TestLessThanInstruction(Instruction):
    num_params = 3

    def run(self):
        first = self.get_param_value(0)
        second = self.get_param_value(1)
        self.program.int_codes[self.get_param_address(2)] = int(first < second)
        return 'continue'


class TestEqualInstruction(Instruction):
    num_params = 3

    def run(self):
        first = self.get_param_value(0)
        second = self.get_param_value(1)
        self.program.int_codes[self.get_param_address(2)] = int(first == second)
        return 'continue'


class ChangeRelativeBaseInstruction(Instruction):
    num_params = 1

    def run(self):
        param = self.get_param_value(0)
        self.program.relative_base += param
        return 'continue'


class HaltInstruction(Instruction):
    num_params = 0

    def run(self):
        return 'halt'


class InstructionFactory:
    instructions = {
        99: HaltInstruction,
        1: AddInstruction,
        2: MultiplyInstruction,
        3: InputInstruction,
        4: OutputInstruction,
        5: JumpNotEqualToZeroInstruction,
        6: JumpEqualToZeroInstruction,
        7: TestLessThanInstruction,
        8: TestEqualInstruction,
        9: ChangeRelativeBaseInstruction,
    }

    @classmethod
    def get_instruction(cls, instruction: int, program):
        opcode, modes = parse_first_instruction(instruction)
        return cls.instructions[opcode](program, modes)


class Program:
    def __init__(self, int_codes, pc=0):
        if isinstance(int_codes, dict):
            self.int_codes = dict(int_codes)
        else:
            self.int_codes = {idx: code for idx, code in enumerate(int_codes)}
        self.pc = pc
        self.outputs = []
        self.relative_base = 0
        # print(len(int_codes))
        # print(int_codes[203])

    def get_at_address(self, address: int) -> int:
        if address < 0:
            raise Exception('read from negative address')
        return self.int_codes.get(address, 0)

    def run(self, inputs: Iterable[int] = None) -> ProgramStatus:
        self.outputs = []
        self.input_iterator = iter(inputs or [])
        while True:
            # print(self.pc)
            instruction_int = self.get_at_address(self.pc)
            instruction = InstructionFactory.get_instruction(instruction_int, self)
            code = instruction.run_and_update_pc()
            if code in ('halt', 'input'):
                return ProgramStatus(status=code, outputs=self.outputs)