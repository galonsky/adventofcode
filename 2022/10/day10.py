from typing import Generator, Iterable


def get_instructions(filename: str) -> Generator[str, None, None]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


def get_signal_strength(instructions: Iterable[str]) -> int:
    reg_by_cycle = {
        1: 1,
    }
    cycle_count = 1
    instruction_iter = iter(instructions)
    while instruction := next(instruction_iter, None):
        if instruction == "noop":
            reg_by_cycle[cycle_count + 1] = reg_by_cycle[cycle_count]
            cycle_count += 1
        else:
            parts = instruction.split()
            to_add = int(parts[1])
            reg_by_cycle[cycle_count + 1] = reg_by_cycle[cycle_count]
            reg_by_cycle[cycle_count + 2] = reg_by_cycle[cycle_count] + to_add
            cycle_count += 2

    cycles_to_test = [20, 60, 100, 140, 180, 220]
    return sum(cyc * reg_by_cycle[cyc] for cyc in cycles_to_test)


if __name__ == '__main__':
    instructions = get_instructions("input.txt")
    print(get_signal_strength(instructions))

