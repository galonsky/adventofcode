import re

def registers_with_change(registers, i, v):
    new_registers = list(registers)
    new_registers[i] = v
    return new_registers


class OpCode:
    def operate(self, registers, a, b, c):
        pass

class Addr(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a] + registers[b])


class Addi(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a] + b)


class Mulr(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a] * registers[b])


class Muli(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a] * b)


class Banr(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a] & registers[b])


class Bani(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a] & b)


class Borr(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a] | registers[b])


class Bori(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a] | b)


class Setr(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, registers[a])


class Seti(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, a)


class Gtir(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, 1 if a > registers[b] else 0)


class Gtri(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, 1 if registers[a] > b else 0)


class Gtrr(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, 1 if registers[a] > registers[b] else 0)


class Eqir(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, 1 if a == registers[b] else 0)


class Eqri(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, 1 if registers[a] == b else 0)


class Eqrr(OpCode):
    def operate(self, registers, a, b, c):
        return registers_with_change(registers, c, 1 if registers[a] == registers[b] else 0)


operators_by_name = {
    clz.__name__.lower(): clz() for clz in OpCode.__subclasses__()
}

def get_instruction_register_and_lines(filename):
    lines = []
    with open(filename) as file:
        instruction_register = int(next(file).rstrip('\n').split()[1])
        lines = [line.rstrip('\n') for line in file]
        return instruction_register, lines

def parse_instruction_line(line):
    parts = line.split()
    return parts[0], int(parts[1]), int(parts[2]), int(parts[3])

def run_program_and_get_register_0(filename):
    instruction_register, lines = get_instruction_register_and_lines(filename)
    #registers = [0, 0, 0, 0, 0, 0]
    # registers = [0, 892, 1, 0, 893, 8]
    registers = [1, 0, 0, 0, 0, 0]
    instruction_pointer = registers[instruction_register]
    steps = 0
    while True:
        if instruction_pointer < 0 or instruction_pointer >= len(lines):
            break

        if steps > 100:
            break

        before_registers = registers
        before_ip = instruction_pointer

        registers[instruction_register] = instruction_pointer
        instruction_line = lines[instruction_pointer]
        instruction, a, b, c = parse_instruction_line(instruction_line)
        operator = operators_by_name[instruction]
        registers = operator.operate(registers, a, b, c)
        instruction_pointer = registers[instruction_register] + 1

        steps += 1

        print('ip={} {} {} {}'.format(before_ip, before_registers, instruction_line, registers))

    return registers[0]



print(run_program_and_get_register_0('day19_input.txt'))