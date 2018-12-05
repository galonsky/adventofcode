from string import ascii_lowercase


def get_polymer(filename):
    with open(filename) as file:
        return next(file)


def reduce_polymer(filename):
    polymer = get_polymer(filename)
    i = 0
    while i < len(polymer) - 1:
        if polymer[i] != polymer[i+1] and (
            polymer[i].upper() == polymer[i+1] or polymer[i] == polymer[i+1].upper()
        ):
            polymer = polymer[0:i] + polymer[i+2:]
            i = max(0, i - 1)
        else:
            i += 1
    return len(polymer)


def with_letter_removed(original, lower_letter):
    return ''.join((c for c in original if c != lower_letter and c != lower_letter.upper()))


def reduce_polymer_with_removed_letters(filename, lower_letter):
    polymer = with_letter_removed(get_polymer(filename), lower_letter)
    i = 0
    while i < len(polymer) - 1:
        if polymer[i] != polymer[i+1] and (
            polymer[i].upper() == polymer[i+1] or polymer[i] == polymer[i+1].upper()
        ):
            polymer = polymer[0:i] + polymer[i+2:]
            i = max(0, i - 1)
        else:
            i += 1
    return len(polymer)


def find_shortest_by_removing(filename):
    lengths = [
        reduce_polymer_with_removed_letters(filename, c) for c in ascii_lowercase
    ]
    return min(lengths)

print(find_shortest_by_removing('day5_input.txt'))