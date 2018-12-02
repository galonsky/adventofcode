from collections import defaultdict

def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.rstrip('\n')

def get_letter_counts(word):
    counts = defaultdict(int)
    for char in word:
        counts[char] += 1
    return counts

# part 1
def get_checksum(filename):
    num_twos = 0
    num_threes = 0
    for line in get_lines(filename):
        counts = get_letter_counts(line)
        values = counts.values()
        if 2 in values:
            num_twos += 1
        if 3 in values:
            num_threes += 1
    return num_twos * num_threes


# part 2
def get_shared_portion_with_one_difference(filename):
    pairs = []
    for line1 in get_lines(filename):
        for line2 in get_lines(filename):
            if line1 != line2:
                num_diff = 0
                shared_portion = ''
                for i in range(len(line1)):
                    if line1[i] != line2[i]:
                        num_diff += 1
                    else:
                        shared_portion += line1[i]
                if num_diff == 1:
                    return shared_portion


assert get_shared_portion_with_one_difference('day2_input.txt') == 'fvstwblgqkhpuixdrnevmaycd'
