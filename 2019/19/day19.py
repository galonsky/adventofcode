
from typing import List, Iterable
from dataclasses import dataclass


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
        # print(param)
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


def run(bounds: int, square_size: int):
    map = {}
    count = 0
    output = 0
    startx = 0
    x = startx

    rows = {}
    for y in range(bounds):
        x = startx
        while x < bounds:
            program = Program(int_codes=[109,424,203,1,21101,11,0,0,1106,0,282,21102,1,18,0,1105,1,259,1202,1,1,221,203,1,21101,0,31,0,1105,1,282,21102,1,38,0,1106,0,259,21001,23,0,2,22102,1,1,3,21102,1,1,1,21102,57,1,0,1106,0,303,2101,0,1,222,21002,221,1,3,21001,221,0,2,21101,0,259,1,21101,80,0,0,1105,1,225,21101,158,0,2,21101,0,91,0,1106,0,303,1201,1,0,223,20102,1,222,4,21101,259,0,3,21101,225,0,2,21102,225,1,1,21101,118,0,0,1106,0,225,20102,1,222,3,21101,0,79,2,21102,1,133,0,1106,0,303,21202,1,-1,1,22001,223,1,1,21101,148,0,0,1105,1,259,2102,1,1,223,21001,221,0,4,20102,1,222,3,21101,16,0,2,1001,132,-2,224,1002,224,2,224,1001,224,3,224,1002,132,-1,132,1,224,132,224,21001,224,1,1,21101,0,195,0,106,0,108,20207,1,223,2,20101,0,23,1,21102,-1,1,3,21102,214,1,0,1106,0,303,22101,1,1,1,204,1,99,0,0,0,0,109,5,1201,-4,0,249,21202,-3,1,1,21201,-2,0,2,22101,0,-1,3,21101,250,0,0,1106,0,225,21202,1,1,-4,109,-5,2105,1,0,109,3,22107,0,-2,-1,21202,-1,2,-1,21201,-1,-1,-1,22202,-1,-2,-2,109,-3,2106,0,0,109,3,21207,-2,0,-1,1206,-1,294,104,0,99,21202,-2,1,-2,109,-3,2106,0,0,109,5,22207,-3,-4,-1,1206,-1,346,22201,-4,-3,-4,21202,-3,-1,-1,22201,-4,-1,2,21202,2,-1,-1,22201,-4,-1,1,22101,0,-2,3,21102,343,1,0,1106,0,303,1106,0,415,22207,-2,-3,-1,1206,-1,387,22201,-3,-2,-3,21202,-2,-1,-1,22201,-3,-1,3,21202,3,-1,-1,22201,-3,-1,2,22101,0,-4,1,21101,384,0,0,1105,1,303,1105,1,415,21202,-4,-1,-4,22201,-4,-3,-4,22202,-3,-2,-2,22202,-2,-4,-4,22202,-3,-2,-3,21202,-4,-1,-2,22201,-3,-2,1,21202,1,1,-4,109,-5,2106,0,0])
            status = program.run(inputs=[x, y])
            last_output = output
            output = status.outputs[0]
            if output == 1:
                map[(x, y)] = '#'
            else:
                map[(x, y)] = '.'
            # count += output
            print(map[(x, y)], end='')
            if output == 1 and last_output == 0:
                startx = x
                if rows and (y-1) in rows:
                    last_row = rows[y-1]
                    x += max(last_row[1] - last_row[0], 1)
                    continue
            if output == 0 and last_output == 1:
                endx = x - 1
                print(f"[{startx}, {endx}], size {endx - startx}")
                row = (startx, endx)

                if len(rows) >= square_size and (endx - startx) >= square_size:
                    first_row = rows[y - square_size + 1]
                    if first_row[1] - first_row[0] >= square_size:
                        overlap_x = max(row[0], first_row[0])
                        overlap = min(row[1], first_row[1]) - overlap_x + 1
                        if overlap >= square_size:
                            print(f'found square at y={y - square_size + 1}, row={first_row} overlap_x={overlap_x}')
                            print(f'answer: {overlap_x * 10000 + y - square_size + 1}')
                            return

                rows[y] = row

                break
            x += 1
        print()

    return count

if __name__ == '__main__':
    run(2000, 100)
