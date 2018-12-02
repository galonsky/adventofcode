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
def get_shared_portion_with_one_difference_v2(filename):
    lines = list(get_lines(filename))
    wordlen = len(lines[0])
    for i in range(wordlen):
        seen = set()
        for line in lines:
            cut_out = line[0:i] + line[i+1:]
            if cut_out in seen:
                return cut_out
            seen.add(cut_out)


assert get_shared_portion_with_one_difference_v2('day2_input.txt') == 'fvstwblgqkhpuixdrnevmaycd'
