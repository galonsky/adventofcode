import re


NUM_PATTERN = re.compile(r"\d+")
PAIR_PATTERN = re.compile(r"\[(\d+),(\d+)]")


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


if __name__ == '__main__':
    assert explode("[[[[[9,8],1],2],3],4]") == "[[[[0,9],2],3],4]"
    assert explode("[7,[6,[5,[4,[3,2]]]]]") == "[7,[6,[5,[7,0]]]]"
    assert explode("[[6,[5,[4,[3,2]]]],1]") == "[[6,[5,[7,0]]],3]"
    assert explode("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"
    assert explode("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]") == "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
