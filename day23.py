import re
import collections
import concurrent.futures

patterns = {
    "set": re.compile('set ([a-z]) ([a-z]|\-?[0-9]+)'),
    "sub": re.compile('sub ([a-z]) ([a-z]|\-?[0-9]+)'),
    "mul": re.compile('mul ([a-z]) ([a-z]|\-?[0-9]+)'),
    "jnz": re.compile('jnz ([a-z]|\-?[0-9]+) ([a-z]|\-?[0-9]+)'), }


def get_instr(str):
    for key in patterns:
        match = patterns[key].match(str)
        if match:
            return (key, match)
    raise Exception('wtf')


def value(registers, str):
    if re.match('[a-z]', str):
        return registers.get(str, 0)
    return int(str)


class Program:

    def __init__(self, instrs):
        self.instrs = instrs
        self.registers = {
            'a': 1
        }
        self.pc = 0

    def run_program(self):
        mul_calls = 0
        while self.pc >= 0 and self.pc < len(self.instrs):
            pc_incr = 1
            cmd_str = self.instrs[self.pc]
            # print(pid, cmd_str)
            instr, match = get_instr(cmd_str)
            if instr == 'set':
                self.registers[match.groups()[0]] = value(self.registers, match.groups()[1])
            elif instr == 'sub':
                reg = match.groups()[0]
                self.registers[reg] = self.registers.get(reg, 0) - value(self.registers, match.groups()[1])
            elif instr == 'mul':
                reg = match.groups()[0]
                self.registers[reg] = self.registers.get(reg, 0) * value(self.registers, match.groups()[1])
                mul_calls += 1
            elif instr == 'jnz':
                if value(self.registers, match.groups()[0]) != 0:
                    pc_incr = value(self.registers, match.groups()[1])

            self.pc += pc_incr
        return mul_calls


with open('day23_input.txt') as file:
    instrs = [line.rstrip('\n') for line in file]

    prg0 = Program(instrs)

    ret0 = prg0.run_program()
    print(ret0)
