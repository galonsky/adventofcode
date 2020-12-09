from typing import List, Tuple


def get_instructions(filename: str) -> List[Tuple[str, int]]:
    insts = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.rstrip('\n').split(' ')
            insts.append((parts[0], int(parts[1].lstrip('+'))))
    return insts


def part1():
    instructions = get_instructions('input.txt')
    # print(instructions)

    executed = set()
    pc = 0
    acc = 0
    while True:
        if pc in executed:
            return acc
        executed.add(pc)
        inst, val = instructions[pc]
        if inst == 'nop':
            pc += 1
        elif inst == 'acc':
            acc += val
            pc += 1
        elif inst == 'jmp':
            pc += val
        else:
            raise Exception(f'unrecognized instruction! {inst}')


class InfiniteLoopException(Exception):
    pass


def run_program(instructions: List[Tuple[str, int]]) -> int:
    executed = set()
    pc = 0
    acc = 0
    while True:
        if pc in executed:
            raise InfiniteLoopException
        if pc == len(instructions):
            return acc
        executed.add(pc)
        inst, val = instructions[pc]
        if inst == 'nop':
            pc += 1
        elif inst == 'acc':
            acc += val
            pc += 1
        elif inst == 'jmp':
            pc += val
        else:
            raise Exception(f'unrecognized instruction! {inst}')

def part2():
    instructions = get_instructions('input.txt')
    for i, (inst, val) in enumerate(instructions):
        if inst == 'acc':
            continue
        new_inst = 'nop' if inst == 'jmp' else 'jmp'
        new_instructions = list(instructions)
        new_instructions[i] = (new_inst, val)
        try:
            return run_program(new_instructions)
        except InfiniteLoopException:
            pass


if __name__ == '__main__':
    print(part2())