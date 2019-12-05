from typing import List

def run_program(int_codes: List[int]) -> List[int]:
    int_codes = list(int_codes)
    pc = 0
    while True:
        opcode = int_codes[pc]
        if opcode == 99:
            return int_codes
        
        if opcode == 1:
            addend1 = int_codes[int_codes[pc+1]]
            addend2 = int_codes[int_codes[pc+2]]
            int_codes[int_codes[pc+3]] = addend1 + addend2
        elif opcode == 2:
            multiplicand1 = int_codes[int_codes[pc+1]]
            multiplicand2 = int_codes[int_codes[pc+2]]
            int_codes[int_codes[pc+3]] = multiplicand1 * multiplicand2
        else:
            raise ValueError('unrecognized opcode {}'.format(opcode))
        
        pc += 4