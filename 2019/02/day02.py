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

def find_noun_and_verb(intcodes):
    for noun in range(100):
        for verb in range(100):
            print(f'testing {noun} and {verb}')
            newlist = list(intcodes)
            newlist[1] = noun
            newlist[2] = verb
            evaluated = run_program(newlist)
            if evaluated[0] == 19690720:
                return noun, verb


# print(run_program([1,0,0,0,99]))
# print(run_program([2,3,0,3,99]))
# print(run_program([2,4,4,5,99,0]))
# print(run_program([1,1,1,4,99,5,6,0,99]))


print(find_noun_and_verb([1,12,2,3,1,1,2,3,1,3,4,3,1,5,0,3,2,6,1,19,1,19,5,23,2,9,23,27,1,5,27,31,1,5,31,35,1,35,13,39,1,39,9,43,1,5,43,47,1,47,6,51,1,51,13,55,1,55,9,59,1,59,13,63,2,63,13,67,1,67,10,71,1,71,6,75,2,10,75,79,2,10,79,83,1,5,83,87,2,6,87,91,1,91,6,95,1,95,13,99,2,99,13,103,1,103,9,107,1,10,107,111,2,111,13,115,1,10,115,119,1,10,119,123,2,13,123,127,2,6,127,131,1,13,131,135,1,135,2,139,1,139,6,0,99,2,0,14,0]))