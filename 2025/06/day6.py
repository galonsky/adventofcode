import re
from functools import reduce
from typing import Iterable


def get_homework(filename: str) -> list[str]:
    with open(filename, 'r') as file:
        return list(line.strip("\n") for line in file)


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


def get_operands(number_rows: list[str], start_inc: int, end_exc: int) -> Iterable[int]:
    for x in range(end_exc, start_inc, -1):
        num_str = ""
        for row in number_rows:
            ch = row[x] if x < len(row) else " "
            if ch != " ":
                num_str += ch
        if num_str:
            yield int(num_str)


def get_sum_of_answers_pt2(lines: list[str]) -> int:
    operations = lines[-1]
    total = 0
    number_rows = [
        line
        for line in lines[:-1]
    ]
    operation_iter = re.finditer(r'[*+]', operations)
    current = next(operation_iter, None)
    while current:
        start = current.start() - 1
        next_match = next(operation_iter, None)
        end = next_match.start() - 2 if next_match else max(len(row) for row in lines)
        operands = list(get_operands(number_rows, start, end))
        print(operands)
        oper = current.group()
        if oper == '+':
            total += reduce(lambda a,b : a+b, operands, 0)
        elif oper == '*':
            total += reduce(lambda a, b: a * b, operands, 1)
        else:
            raise Exception("unsupported!")
        current = next_match
    return total


if __name__ == '__main__':
    print(get_sum_of_answers_pt2(get_homework("input.txt")))