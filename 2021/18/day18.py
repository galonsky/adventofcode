import re, functools
from itertools import permutations
from math import ceil
from typing import Iterable

NUM_PATTERN = re.compile(r"\d+")
PAIR_PATTERN = re.compile(r"\[(\d+),(\d+)]")
SPLITTABLE_PATTERN = re.compile(r"[1-9][0-9]+")


def explode(numbers: str) -> str:
    depth = 0
    for i, ch in enumerate(numbers):
        if ch == '[':
            depth += 1
            if depth == 5:
                match = PAIR_PATTERN.match(numbers[i:])
                if match:
                    left, right = int(match.group(1)), int(match.group(2))
                    pair_length = match.end() - match.start()
                    right_segment = numbers[i + pair_length:]
                    next_num_to_right = NUM_PATTERN.search(right_segment)
                    if next_num_to_right:
                        new_num = right + int(next_num_to_right.group(0))
                        right_segment = right_segment.replace(next_num_to_right.group(0), str(new_num), 1)
                    left_segment = numbers[:i]
                    nums_to_left = NUM_PATTERN.finditer(numbers, 0, i)
                    num_to_left = None
                    for num_match in nums_to_left:
                        num_to_left = num_match
                    if num_to_left:
                        new_num = left + int(num_to_left.group(0))
                        left_segment = numbers[:num_to_left.start()] + str(new_num) + numbers[num_to_left.end():i]
                    return left_segment + "0" + right_segment

        elif ch == ']':
            depth -= 1
    return numbers


def split(numbers: str) -> str:
    match = SPLITTABLE_PATTERN.search(numbers)
    if match:
        num = int(match.group(0))
        left = num // 2
        right = ceil(num / 2)
        return numbers.replace(match.group(0), f"[{left},{right}]", 1)
    return numbers


def add(n1: str, n2: str) -> str:
    return f"[{n1},{n2}]"


def reduce(numbers: str) -> str:
    new_numbers = explode(numbers)
    if new_numbers != numbers:
        return reduce(new_numbers)
    new_numbers = split(new_numbers)
    if new_numbers != numbers:
        return reduce(new_numbers)
    return new_numbers


def add_and_reduce(*number_strs: str) -> str:
    return functools.reduce(lambda n1, n2: reduce(add(n1, n2)), number_strs)
    # accum = reduce(add(number_strs[0], number_strs[1]))
    # for num in number_strs[2:]:
    #     accum = reduce(add(accum, num))
    # return accum


def get_homework(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.strip()


def get_magnitude(numbers: str) -> int:
    while match := PAIR_PATTERN.search(numbers):
        left, right = int(match.group(1)), int(match.group(2))
        numbers = numbers.replace(match.group(0), str(3*left + 2*right))
    return int(numbers)


def get_largest_magnitude(numbers: Iterable[str]) -> int:
    return max(get_magnitude(add_and_reduce(*perm)) for perm in permutations(numbers, 2))


if __name__ == '__main__':
    assert explode("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
    assert explode("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
    assert explode("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
    assert explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    assert explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"

    assert add_and_reduce("[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]") == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"
    assert add_and_reduce("[1,1]", "[2,2]", "[3,3]", "[4,4]") == "[[[[1,1],[2,2]],[3,3]],[4,4]]"
    assert add_and_reduce("[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]") == "[[[[3,0],[5,3]],[4,4]],[5,5]]"
    assert add_and_reduce("[1,1]", "[2,2]", "[3,3]", "[4,4]", "[5,5]", "[6,6]") == "[[[[5,0],[7,4]],[5,5]],[6,6]]"

    # res = add_and_reduce("[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]", "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]")
    # print(res)
    # assert res == (
    #     "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"
    # )

    hw = list(get_homework("sample.txt"))
    assert add_and_reduce(*hw) == "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]"

    assert get_magnitude("[[1,2],[[3,4],5]]") == 143
    assert get_magnitude("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]") == 1384
    assert get_magnitude("[[[[1,1],[2,2]],[3,3]],[4,4]]") == 445
    assert get_magnitude("[[[[3,0],[5,3]],[4,4]],[5,5]]") == 791
    assert get_magnitude("[[[[5,0],[7,4]],[5,5]],[6,6]]") == 1137
    assert get_magnitude("[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]") == 3488

    assert get_magnitude(add_and_reduce(*list(get_homework("sample2.txt")))) == 4140

    print(get_magnitude(add_and_reduce(*list(get_homework("input.txt")))))

    assert get_largest_magnitude(get_homework("sample2.txt")) == 3993
    print(get_largest_magnitude(get_homework("input.txt")))