from typing import List, Iterable
from itertools import permutations, cycle
from dataclasses import dataclass
from collections import defaultdict

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
        param_address = self.program.pc+index+1
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
    def __init__(self, int_codes: List[int]):
        self.int_codes = {idx: code for idx, code in enumerate(int_codes)}
        self.pc = 0
        self.outputs = []
        self.relative_base = 0
        # print(len(int_codes))
        # print(int_codes[203])

    def get_at_address(self, address: int) -> int:
        if address < 0:
            raise Exception('read from negative address')
        return self.int_codes.get(address, 0)

    def run(self, inputs: Iterable[int] = None) -> List[int]:
        self.outputs = []
        self.input_iterator = iter(inputs or [])
        while True:
            # print(self.pc)
            instruction_int = self.get_at_address(self.pc)
            instruction = InstructionFactory.get_instruction(instruction_int, self)
            code = instruction.run_and_update_pc()
            if code in ('halt', 'input'):
                return ProgramStatus(status=code, outputs=self.outputs)

direction_vectors = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
)
def get_direction_vector(index):
    if index >= 0:
        return direction_vectors[index % 4]
    else:
        return direction_vectors[-(abs(index) % 4)]

def print_map(ship_map):
    min_x = min((key[0] for key in ship_map.keys()))
    max_x = max((key[0] for key in ship_map.keys()))
    min_y = min((key[1] for key in ship_map.keys()))
    max_y = max((key[1] for key in ship_map.keys()))

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            color = ship_map[(x, y)]
            if color == 1:
                print('#', end='')
            else:
                print(' ', end='')
        print()

def run_robot(int_codes, starting_color=0):
    program = Program(int_codes)
    ship_map = defaultdict(lambda: 0)
    dir_index = 0

    x = 0
    y = 0

    ship_map[(x, y)] = starting_color

    while True:
        current_color = ship_map[(x, y)]
        result = program.run([current_color])
        if result.status == 'halt':
            # return len(ship_map)
            print_map(ship_map)
            return
        assert len(result.outputs) == 2
        to_paint = result.outputs[0]
        turn_code = result.outputs[1]

        ship_map[(x, y)] = to_paint
        if turn_code == 0:
            dir_index -= 1
        else:
            dir_index += 1
        
        vector = get_direction_vector(dir_index)
        x += vector[0]
        y += vector[1]

print(run_robot([3,8,1005,8,320,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,29,2,1005,1,10,1006,0,11,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,57,1,8,15,10,1006,0,79,1,6,3,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,90,2,103,18,10,1006,0,3,2,105,14,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,123,2,9,2,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1001,8,0,150,1,2,2,10,2,1009,6,10,1,1006,12,10,1006,0,81,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,102,1,8,187,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,209,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,231,1,1008,11,10,1,1001,4,10,2,1104,18,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,264,1,8,14,10,1006,0,36,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,101,0,8,293,1006,0,80,1006,0,68,101,1,9,9,1007,9,960,10,1005,10,15,99,109,642,104,0,104,1,21102,1,846914232732,1,21102,1,337,0,1105,1,441,21102,1,387512115980,1,21101,348,0,0,1106,0,441,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,209533824219,1,1,21102,1,395,0,1106,0,441,21101,0,21477985303,1,21102,406,1,0,1106,0,441,3,10,104,0,104,0,3,10,104,0,104,0,21101,868494234468,0,1,21101,429,0,0,1106,0,441,21102,838429471080,1,1,21102,1,440,0,1106,0,441,99,109,2,21201,-1,0,1,21101,0,40,2,21102,472,1,3,21101,0,462,0,1106,0,505,109,-2,2106,0,0,0,1,0,0,1,109,2,3,10,204,-1,1001,467,468,483,4,0,1001,467,1,467,108,4,467,10,1006,10,499,1102,1,0,467,109,-2,2106,0,0,0,109,4,2101,0,-1,504,1207,-3,0,10,1006,10,522,21101,0,0,-3,21202,-3,1,1,22101,0,-2,2,21102,1,1,3,21102,541,1,0,1106,0,546,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,569,2207,-4,-2,10,1006,10,569,22102,1,-4,-4,1105,1,637,22102,1,-4,1,21201,-3,-1,2,21202,-2,2,3,21102,588,1,0,1105,1,546,22101,0,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,607,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,629,21201,-1,0,1,21102,629,1,0,105,1,504,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2105,1,0], 1))