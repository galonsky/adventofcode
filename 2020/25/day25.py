def transform(subject_number: int, loop_size: int) -> int:
    value = 1
    for _ in range(loop_size):
        value *= subject_number
        value %= 20201227
    return value


def find_loop_number(subject_number: int, target_number: int) -> int:
    value = 1
    i = 0
    while value != target_number:
        i += 1
        value *= subject_number
        value %= 20201227
    return i


def part1():
    card_public = 9717666
    door_public = 20089533
    card_loop_size = find_loop_number(7, card_public)
    door_loop_size = find_loop_number(7, door_public)

    print(transform(card_public, door_loop_size))
    print(transform(door_public, card_loop_size))




if __name__ == '__main__':
    part1()