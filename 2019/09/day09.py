from typing import List, Iterable
from itertools import permutations, cycle
from dataclasses import dataclass
from collections import defaultdict

def parse_first_instruction(instruction):
    opcode = instruction % 100
    modes_in_order = str(instruction)[:-2][::-1]
    return opcode, modes_in_order

def get_mode(modes, index):
    if index >= len(modes):
        return 0
    return int(modes[index])


def get_value(int_codes, param, mode):
    if mode == 1:
        return param
    return int_codes[param]


@dataclass
class ProgramStatus:
    status: str
    outputs: List[int]


class Program:
    def __init__(self, int_codes: List[int], id: int):
        self.int_codes = list(int_codes)
        self.id = id
        self.pc = 0
        self.outputs = []

    def run(self, inputs: Iterable[int] = None) -> List[int]:
        self.outputs = []
        print('program {} running with inputs {}'.format(self.id, inputs))
        input_iterator = iter(inputs or [])
        while True:
            first_instruction = self.int_codes[self.pc]
            opcode, modes = parse_first_instruction(first_instruction)
            if opcode == 99:
                return ProgramStatus(
                    status='halted',
                    outputs=self.outputs,
                )
            
            if opcode == 1:
                addend1 = get_value(self.int_codes, self.int_codes[self.pc+1], get_mode(modes, 0))
                addend2 = get_value(self.int_codes, self.int_codes[self.pc+2], get_mode(modes, 1))
                self.int_codes[self.int_codes[self.pc+3]] = addend1 + addend2
                self.pc += 4
            elif opcode == 2:
                multiplicand1 = get_value(self.int_codes, self.int_codes[self.pc+1], get_mode(modes, 0))
                multiplicand2 = get_value(self.int_codes, self.int_codes[self.pc+2], get_mode(modes, 1))
                self.int_codes[self.int_codes[self.pc+3]] = multiplicand1 * multiplicand2
                self.pc += 4
            elif opcode == 3:
                param = self.int_codes[self.pc+1]
                try:
                    self.int_codes[param] = next(input_iterator)
                except StopIteration:
                    return ProgramStatus(
                        status='waiting_for_input',
                        outputs=self.outputs,
                    )
                self.pc += 2
            elif opcode == 4:
                output = get_value(self.int_codes, self.int_codes[self.pc+1], get_mode(modes, 0))
                print(output)
                self.outputs.append(output)
                self.pc += 2
            elif opcode == 5:
                to_test = get_value(self.int_codes, self.int_codes[self.pc+1], get_mode(modes, 0))
                if to_test != 0:
                    self.pc = get_value(self.int_codes, self.int_codes[self.pc+2], get_mode(modes, 1))
                else:
                    self.pc += 3
            elif opcode == 6:
                to_test = get_value(self.int_codes, self.int_codes[self.pc+1], get_mode(modes, 0))
                if to_test == 0:
                    self.pc = get_value(self.int_codes, self.int_codes[self.pc+2], get_mode(modes, 1))
                else:
                    self.pc += 3
            elif opcode == 7:
                first = get_value(self.int_codes, self.int_codes[self.pc+1], get_mode(modes, 0))
                second = get_value(self.int_codes, self.int_codes[self.pc+2], get_mode(modes, 1))
                self.int_codes[self.int_codes[self.pc+3]] = int(first < second)
                self.pc += 4
            elif opcode == 8:
                first = get_value(self.int_codes, self.int_codes[self.pc+1], get_mode(modes, 0))
                second = get_value(self.int_codes, self.int_codes[self.pc+2], get_mode(modes, 1))
                self.int_codes[self.int_codes[self.pc+3]] = int(first == second)
                self.pc += 4
            else:
                raise ValueError('unrecognized opcode {}'.format(opcode))