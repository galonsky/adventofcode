from typing import Dict, List, Union, Set, Iterable


def parse_rules(filename: str) -> Dict[int, Union[str, List[List[int]]]]:
    rules = {}
    with open(filename, 'r') as file:
        for line in file:
            rule_possibilities = []
            parts = line.split(':')
            rule_id = int(parts[0])
            rest = parts[1].strip()
            if rest.endswith('"'):
                rules[rule_id] = rest[-2]
            else:
                for possibility_str in rest.split('|'):
                    rule_possibilities.append([
                        int(num.strip()) for num in possibility_str.strip().split()
                    ])
                rules[rule_id] = rule_possibilities
    return rules


def get_possibilities_for_rule(rule_id: int, rules: Dict[int, Union[str, List[List[int]]]]) -> Set[str]:
    rule = rules[rule_id]
    if isinstance(rule, str):
        return {rule}

    all_possibilities = set()
    for rules_list in rule:
        strs_for_this_possibility = set()
        for rule_id in rules_list:
            new_possibilities = get_possibilities_for_rule(rule_id, rules)
            if not strs_for_this_possibility:
                strs_for_this_possibility |= new_possibilities
            else:
                # append everything in strs_for_this_possibility with everything in new_possibilities
                appended_strs = set()
                for original_str in strs_for_this_possibility:
                    for new_str in new_possibilities:
                        appended_strs.add(original_str + new_str)
                strs_for_this_possibility = appended_strs
        all_possibilities |= strs_for_this_possibility
    return all_possibilities


def get_test_strs(filename: str) -> Iterable[str]:
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def part1():
    rules = parse_rules('input_rules.txt')
    strs = get_test_strs('input_strs.txt')
    possibilities = get_possibilities_for_rule(0, rules)
    print(len(possibilities))
    total = 0
    for test_str in strs:
        if test_str in possibilities:
            total += 1
    print(total)


def part2():
    rules = parse_rules('input_rules.txt')
    strs = list(get_test_strs('input_strs.txt'))
    poss31 = get_possibilities_for_rule(31, rules)
    poss42 = get_possibilities_for_rule(42, rules)

    # base rule (0) is 8, 11 so
    # all answers are some 1+ repetition of 42 followed by (42){n}(31){n}
    # (42)+(42){n}(31){n} where n >= 1

    print(poss31)
    print(poss42)

    pattern_size = len(next(iter(poss31)))

    total = 0
    for test_str in strs:
        rest = test_str
        num_42s = 0
        while(any(
            rest.startswith(poss) for poss in poss42
        )):
            rest = rest[pattern_size:]
            num_42s += 1
        if len(rest) == len(test_str):
            continue  # did not start with a 42
        num_31s = 0
        while(any(
            rest.startswith(poss) for poss in poss31
        )):
            rest = rest[pattern_size:]
            num_31s += 1
        if len(rest) == 0 and num_31s >= 1 and num_42s >= 2 and num_42s >= num_31s + 1:
            print(test_str, num_42s, num_31s)
            total += 1
    print(total)


if __name__ == '__main__':
    part2()
