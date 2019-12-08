from typing import List, Iterable
from itertools import permutations

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


def run_program(int_codes: List[int], inputs: Iterable[int] = None) -> List[int]:

    input_iterator = iter(inputs or [])
    outputs = []
    int_codes = list(int_codes)
    pc = 0
    while True:
        first_instruction = int_codes[pc]
        opcode, modes = parse_first_instruction(first_instruction)
        if opcode == 99:
            return outputs
        
        if opcode == 1:
            addend1 = get_value(int_codes, int_codes[pc+1], get_mode(modes, 0))
            addend2 = get_value(int_codes, int_codes[pc+2], get_mode(modes, 1))
            int_codes[int_codes[pc+3]] = addend1 + addend2
            pc += 4
        elif opcode == 2:
            multiplicand1 = get_value(int_codes, int_codes[pc+1], get_mode(modes, 0))
            multiplicand2 = get_value(int_codes, int_codes[pc+2], get_mode(modes, 1))
            int_codes[int_codes[pc+3]] = multiplicand1 * multiplicand2
            pc += 4
        elif opcode == 3:
            param = int_codes[pc+1]
            int_codes[param] = next(input_iterator)
            pc += 2
        elif opcode == 4:
            output = get_value(int_codes, int_codes[pc+1], get_mode(modes, 0))
            print(output)
            outputs.append(output)
            pc += 2
        elif opcode == 5:
            to_test = get_value(int_codes, int_codes[pc+1], get_mode(modes, 0))
            if to_test != 0:
                pc = get_value(int_codes, int_codes[pc+2], get_mode(modes, 1))
            else:
                pc += 3
        elif opcode == 6:
            to_test = get_value(int_codes, int_codes[pc+1], get_mode(modes, 0))
            if to_test == 0:
                pc = get_value(int_codes, int_codes[pc+2], get_mode(modes, 1))
            else:
                pc += 3
        elif opcode == 7:
            first = get_value(int_codes, int_codes[pc+1], get_mode(modes, 0))
            second = get_value(int_codes, int_codes[pc+2], get_mode(modes, 1))
            int_codes[int_codes[pc+3]] = int(first < second)
            pc += 4
        elif opcode == 8:
            first = get_value(int_codes, int_codes[pc+1], get_mode(modes, 0))
            second = get_value(int_codes, int_codes[pc+2], get_mode(modes, 1))
            int_codes[int_codes[pc+3]] = int(first == second)
            pc += 4
        else:
            raise ValueError('unrecognized opcode {}'.format(opcode))


def run_for_phase_codes(int_codes, phase_codes) -> int:
    next_data_input = 0
    for phase_code in phase_codes:
        outputs = run_program(int_codes, [phase_code, next_data_input])
        assert len(outputs) == 1
        next_data_input = outputs[0]
    return next_data_input

def get_phase_permutations():
    return set(permutations([0,1,2,3,4]))


def maximize_signal(int_codes):
    return max((run_for_phase_codes(int_codes, phase_codes) for phase_codes in get_phase_permutations()))

print(maximize_signal([3,8,1001,8,10,8,105,1,0,0,21,38,59,84,93,110,191,272,353,434,99999,3,9,101,5,9,9,1002,9,5,9,101,5,9,9,4,9,99,3,9,1001,9,3,9,1002,9,2,9,101,4,9,9,1002,9,4,9,4,9,99,3,9,102,5,9,9,1001,9,4,9,1002,9,2,9,1001,9,5,9,102,4,9,9,4,9,99,3,9,1002,9,2,9,4,9,99,3,9,1002,9,5,9,101,4,9,9,102,2,9,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,1,9,4,9,99]))