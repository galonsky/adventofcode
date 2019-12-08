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


def run_in_feedback_loop(int_codes, phase_codes) -> int:
    next_data_input = 0
    phase_code_to_program = {}
    for phase_code in phase_codes:
        program = Program(int_codes, phase_code)
        phase_code_to_program[phase_code] = program
        status = program.run([phase_code, next_data_input])
        assert len(status.outputs) == 1
        next_data_input = status.outputs[0]
    
    phase_codes_cycle = cycle(phase_codes)
    num_halted = 0
    while num_halted < 5:
        phase_code = next(phase_codes_cycle)
        program = phase_code_to_program[phase_code]
        status = program.run([next_data_input])
        if status.status == 'halted':
            num_halted += 1
            print('{} halted'.format(num_halted))
        assert len(status.outputs) == 1, status
        next_data_input = status.outputs[0]
    return next_data_input

def run_for_phase_codes(int_codes, phase_codes) -> int:
    next_data_input = 0
    for phase_code in phase_codes:
        status = Program(int_codes, phase_code).run([phase_code, next_data_input])
        assert len(status.outputs) == 1
        next_data_input = status.outputs[0]
    return next_data_input

def get_phase_permutations():
    return set(permutations([0,1,2,3,4]))

def get_loop_permutations():
    return set(permutations([5,6,7,8,9]))


def maximize_signal(int_codes):
    return max((run_for_phase_codes(int_codes, phase_codes) for phase_codes in get_phase_permutations()))

def maximize_signal_loop(int_codes):
    return max((run_in_feedback_loop(int_codes, phase_codes) for phase_codes in get_loop_permutations()))

print(maximize_signal_loop([3,8,1001,8,10,8,105,1,0,0,21,38,59,84,93,110,191,272,353,434,99999,3,9,101,5,9,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,4,9,9,1002,9,4,9,4,9,99,3,9,102,5,9,9,1001,9,4,9,1002,9,2,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,1002,9,2,9,4,9,99,3,9,1002,9,5,9,101,4,9,9,102,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99]))
# print(run_in_feedback_loop([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,
# 27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5], [9,8,7,6,5]))