def get_data(filename: str) -> list[tuple[list[str], list[str]]]:
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            left, right = tuple(line.split("|"))
            lines.append((left.split(), right.split()))
    return lines


UNIQUES = {2, 3, 4, 7}


def get_count_of_unique_digits(data: list[tuple[list[str], list[str]]]) -> int:
    count = 0
    for _, right in data:
        for digit in right:
            if len(digit) in UNIQUES:
                count += 1
    return count


if __name__ == '__main__':
    data = get_data("input.txt")
    print(get_count_of_unique_digits(data))
