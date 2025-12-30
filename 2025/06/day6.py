from functools import reduce


def get_homework(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        return list(line.strip() for line in file)


def get_sum_of_answers(lines: list[str]) -> int:
    operations = lines[-1]
    total = 0
    number_rows = [
        [int(ch) for ch in line.split()]
        for line in lines[:-1]
    ]
    for x, oper in enumerate(operations.split()):
        operands = (row[x] for row in number_rows)
        if oper == '+':
            total += reduce(lambda a,b : a+b, operands, 0)
        elif oper == '*':
            total += reduce(lambda a, b: a * b, operands, 1)
        else:
            raise Exception("unsupported!")
    return total


if __name__ == '__main__':
    print(get_sum_of_answers(get_homework("input.txt")))