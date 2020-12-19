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
    total = 0
    for test_str in strs:
        if test_str in possibilities:
            total += 1
    print(total)


if __name__ == '__main__':
    part1()
