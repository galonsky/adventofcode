from collections import deque
from typing import Iterable


def parse_expression(expression: str) -> Iterable[str]:
    for ch in expression:
        if ch == ' ':
            continue
        yield ch


def evaluate_expression(expression: str) -> int:
    characters = iter(parse_expression(expression))
    stack = deque()
    num_open_groups = 0
    while True:
        if len(stack) >= 3 and num_open_groups == 0:
            pop_three(stack)
        try:
            next_char = next(characters)
            if next_char == '(':
                num_open_groups += 1
                stack.append(next_char)
            elif next_char == ')':
                # evaluate everything until start paren
                paren_stack = deque()
                last_char = stack.pop()
                while last_char != '(':
                    paren_stack.appendleft(last_char)
                    last_char = stack.pop()

                while len(paren_stack) > 1:
                    pop_three(paren_stack)
                stack.append(paren_stack.pop())

                num_open_groups -= 1
            else:
                stack.append(next_char)
            # print(stack)

        except StopIteration:
            return stack.pop()


def pop_three(stack):
    operand1 = stack.popleft()
    operator = stack.popleft()
    operand2 = stack.popleft()
    if operator == '+':
        stack.appendleft(int(operand1) + int(operand2))
    else:
        stack.appendleft(int(operand1) * int(operand2))


def part1():
    with open('input.txt', 'r') as file:
        total = 0
        for line in file:
            total += evaluate_expression(line.rstrip('\n'))
        print(total)



if __name__ == '__main__':
    # print(evaluate_expression('1 + 2 * 3 + 4 * 5 + 6'))
    # print(evaluate_expression('1 + (2 * 3) + (4 * (5 + 6))'))
    # print(evaluate_expression('2 * 3 + (4 * 5)'))
    # print(evaluate_expression('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    # print(evaluate_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    # print(evaluate_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
    part1()
