def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.rstrip('\n')


# part 1
def get_ending_frequency(filename):
    freq = 0
    for line in get_lines(filename):
        if line[0] == '+':
            freq += int(line[1:])
        elif line[0] == '-':
            freq -= int(line[1:])
        else:
            raise Exception('first char not plus or minus')
    return freq


# part 2
def get_first_duplicate_frequency(filename):
    freq = 0
    seen_freqs = set()
    seen_freqs.add(freq)
    while True:
        for line in get_lines(filename):
            if line[0] == '+':
                freq += int(line[1:])
            elif line[0] == '-':
                freq -= int(line[1:])
            else:
                raise Exception('first char not plus or minus')
            if freq in seen_freqs:
                return freq
            seen_freqs.add(freq)

print(get_first_duplicate_frequency('day1_input.txt'))