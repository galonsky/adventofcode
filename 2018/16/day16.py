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


ALL_OPCODE_CLASSES = {clz for clz in OpCode.__subclasses__()}

PATTERN = re.compile(r'\w+:\s+\[(\d+), (\d+), (\d+), (\d+)\]')

KNOWN_OPCODES = {
    Mulr, # 7
    Addi, # 14
    Muli, # 3
    Bori, # 6
    Addr, # 12
    Borr, # 5
    Seti, # 9
    Eqri, # 11
    Eqir, # 4
    Gtrr, # 8
    Eqrr, # 1
    Gtri, # 2
    Gtir, # 13
    Setr, # 0
    Bani, # 15
    Banr, # 10
}

OPCODES = {
    0: Setr(),
    1: Eqrr(),
    2: Gtri(),
    3: Muli(),
    4: Eqir(),
    5: Borr(),
    6: Bori(),
    7: Mulr(),
    8: Gtrr(),
    9: Seti(),
    10: Banr(),
    11: Eqri(),
    12: Addr(),
    13: Gtir(),
    14: Addi(),
    15: Bani(),
}

UNKNOWN_OPCODES = {clz() for clz in ALL_OPCODE_CLASSES - KNOWN_OPCODES}

def process_samples(filename):
    num_three_or_more = 0
    with open(filename) as file:
        while True:
            first_line = next(file)
            before_matches = PATTERN.match(first_line.rstrip('\n'))
            before_registers = [int(before_matches.group(1)), int(before_matches.group(2)), int(before_matches.group(3)), int(before_matches.group(4))]
            args = [int(a) for a in next(file).rstrip('\n').split()]
            third_line = next(file).rstrip('\n')
            after_matches = PATTERN.match(third_line)
            after_registers = [int(after_matches.group(1)), int(after_matches.group(2)), int(after_matches.group(3)), int(after_matches.group(4))]
            # print(before_registers)
            # print(args)
            # print(after_registers)
            num_matches = 0
            for opcode in UNKNOWN_OPCODES:
                if after_registers == opcode.operate(before_registers, args[1], args[2], args[3]):
                    num_matches += 1
                    last_type = type(opcode)
            if num_matches >= 3:
                num_three_or_more += 1

            if num_matches == 1:
                print(args[0], last_type)

            try:
                next(file)
            except StopIteration:
                break
    return num_three_or_more


def run_program(filename):
    registers = [0, 0, 0, 0]
    with open(filename) as file:
        for line in file:
            args = [int(arg) for arg in line.rstrip('\n').split()]
            registers = OPCODES[args[0]].operate(registers, args[1], args[2], args[3])

    return registers[0]

print(run_program('day16_program.txt'))
