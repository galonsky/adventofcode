from collections import deque
from typing import Iterable


def parse_expression(expression: str) -> Iterable[str]:
    for ch in expression:
        if ch == ' ':
            continue
        yield ch


def pop_three(stack):
    operand1 = stack.popleft()
    operator = stack.popleft()
    operand2 = stack.popleft()
    if operator == '+':
        stack.appendleft(int(operand1) + int(operand2))
    else:
        stack.appendleft(int(operand1) * int(operand2))


def pop_three_addition_first(stack: deque):
    window = deque()
    remainder = deque()
    while len(stack) > 0:
        # fill window
        if len(stack) == 1:
            remainder.append(stack.pop())
            break
        for _ in range(3 - len(window)):
            window.append(stack.popleft())
        operand1, operator, operand2 = (window.popleft(), window.popleft(), window.popleft())
        if operator == '+':
            sum = int(operand1) + int(operand2)
            stack.appendleft(sum)
        else:
            # we have something like 5 * 3 here
            remainder.append(operand1)
            remainder.append(operator)
            window.append(operand2)
    for num in window:
        remainder.append(num)
    while len(remainder) > 1:
        pop_three(remainder)
    stack.append(remainder.pop())


def evaluate_expression(expression: str, pop_fn=pop_three, wait_for_input=False) -> int:
    characters = iter(parse_expression(expression))
    stack = deque()
    num_open_groups = 0
    depleted = False
    while True:
        if len(stack) >= 3 and num_open_groups == 0 and (not wait_for_input or depleted):
            pop_fn(stack)
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
                    pop_fn(paren_stack)
                stack.append(paren_stack.pop())

                num_open_groups -= 1
            else:
                stack.append(next_char)
            # print(stack)

        except StopIteration:
            depleted = True
            if len(stack) == 1:
                return stack.pop()


def part1():
    with open('input.txt', 'r') as file:
        total = 0
        for line in file:
            total += evaluate_expression(line.rstrip('\n'))
        print(total)


def part2():
    with open('input.txt', 'r') as file:
        total = 0
        for line in file:
            total += evaluate_expression(line.rstrip('\n'), pop_three_addition_first, True)
        print(total)
    # print(evaluate_expression('1 + 2 * 3 + 4 * 5 + 6', pop_three_addition_first, True))
    # print(evaluate_expression('1 + (2 * 3) + (4 * (5 + 6))', pop_three_addition_first, True))
    # print(evaluate_expression('2 * 3 + (4 * 5)', pop_three_addition_first, True))
    # print(evaluate_expression('5 + (8 * 3 + 9 + 3 * 4 * 3)', pop_three_addition_first, True))
    # print(evaluate_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))', pop_three_addition_first, True))
    # print(evaluate_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2', pop_three_addition_first, True))



if __name__ == '__main__':
    # print(evaluate_expression('1 + 2 * 3 + 4 * 5 + 6'))
    # print(evaluate_expression('1 + (2 * 3) + (4 * (5 + 6))'))
    # print(evaluate_expression('2 * 3 + (4 * 5)'))
    # print(evaluate_expression('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
    # print(evaluate_expression('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
    # print(evaluate_expression('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
    part2()
