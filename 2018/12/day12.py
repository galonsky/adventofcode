import re
from collections import deque

RULE_PATTERN = re.compile(r'([\.#]{5}) => ([\.#])')


def get_lines(filename):
    with open(filename) as file:
        for line in file:
            yield line.rstrip('\n')

def get_substr(state, pot_index):
    substr = ''
    if pot_index == 0:
        substr += '..'
    if pot_index == 1:
        substr += '.'

    substr += state[max(0, pot_index - 2) : min(len(state), pot_index + 3)]
    if pot_index == len(state) - 1:
        substr += '..'
    if pot_index == len(state) - 2:
        substr += '.'
    return substr

def get_sum(state, first_id):
    sum = 0
    for i, c in enumerate(state):
        if c == '#':
            sum += i + first_id
    return sum

def trim_and_pad_state(state, first_pot_id):
    new_state = state
    new_pot_id = first_pot_id
    num_leading_dots = 0
    for c in new_state:
        if c != '.':
            break
        num_leading_dots += 1
    if num_leading_dots > 2:
        dots_to_cut = num_leading_dots - 2
        new_state = new_state[dots_to_cut:]
        new_pot_id += dots_to_cut
    elif num_leading_dots < 2:
        dots_to_add = 2 - num_leading_dots
        for i in range(dots_to_add):
            new_state = '.' + new_state
            new_pot_id -= 1

    num_trailing_dots = 0
    for i in range(len(new_state) - 1, 0, -1):
        if new_state[i] != '.':
            break
        num_trailing_dots += 1

    if num_trailing_dots > 2:
        dots_to_cut = num_trailing_dots - 2
        new_state = new_state[0:-dots_to_cut]
    elif num_trailing_dots < 2:
        dots_to_add = 2 - num_trailing_dots
        for i in range(dots_to_add):
            new_state += '.'

    return new_state, new_pot_id


def get_sum_of_pot_ids(rules_filename, initial_state, generations=20):
    rules = {}
    for line in get_lines(rules_filename):
        m = RULE_PATTERN.match(line)
        rules[m.group(1)] = m.group(2)

    pots = deque()
    state, first_pot_id = trim_and_pad_state(initial_state, 0)

    states = set()
    states.add(state)

    for generation in range(1, generations + 1):
        new_state = ''
        for i in range(len(state)):
            substr = get_substr(state, i)
            rule = rules.get(substr, '.')
            new_state += rule
        state = new_state
        state, first_pot_id = trim_and_pad_state(state, first_pot_id)
        print(state, generation, first_pot_id)
        if state in states:
            print('cycle at {}'.format(generation))
            return get_sum(state, first_pot_id)
        states.add(state)


    return get_sum(state, first_pot_id)

# print(get_sum_of_pot_ids(
#     'day_12_rules.txt', 
#     '##.#############........##.##.####..#.#..#.##...###.##......#.#..#####....##..#####..#.#.##.#.##',
#     200,
# ))

# assert get_substr('.', 0) == '.....'
# assert get_substr('.#.#.####', 0) == '...#.'
# assert get_substr('.#.#.####', 8) == '###..'
# assert get_substr('.#.#.####', 3) == '#.#.#'

# ..#...#...#...#...#...#...#...#...#.####...#...#...#...#...#...#...#...#...#...#...#...#...#...#...#...#...#..####...#...#...#...#...#...#...#...#...#...#...#...#...#...#...#..####.. 153 69
# after gen 153, it moves to the right each generation
# so this string, with starting id (69 + (50000000000 - 153)) = 49999999916

print(get_sum('..#...#...#...#...#...#...#...#...#.####...#...#...#...#...#...#...#...#...#...#...#...#...#...#...#...#...#..####...#...#...#...#...#...#...#...#...#...#...#...#...#...#...#..####..', 49999999916))